/**
 * server.js
 * 페이즈 순환 및 masterSeed 발행 서버
 * 
 * [동작 명세]
 * 1. State Machine: LOBBY -> MENU -> GAME -> SCOREBOARD -> MENU... 순환 관리.
 * 2. masterSeed 발행: GAME 시작 시 단일 masterSeed 생성 및 전체 브로드캐스트.
 * 3. 슬롯 관리: P1~P4 슬롯 자동 할당/해제, ROOM_STATE 방송 (active: true 인원 추적).
 * 4. 만장일치 표결:
 *    - LOBBY / MENU: active: true인 모든 접속자가 ready === true 일 때 다음 Phase로 전환.
 *    - SCOREBOARD: 전원 표결(REPLAY/MENU) 일치 시 이동, 불일치 시 VOTE_STATUS_UPDATE 방송.
 */

const { execSync } = require('child_process');
const path = require('path');
const os = require('os');
const http = require('http');
const fs = require('fs');

function ensureModule(moduleName) {
    try {
        return require(moduleName);
    } catch (e) {
        console.log(`📦 [Auto Setup] 필수 모듈 '${moduleName}' 설치 중...`);
        execSync(`npm install ${moduleName}`, { stdio: 'inherit' });
        return require(moduleName);
    }
}

const express = ensureModule('express');
const WebSocket = ensureModule('ws');

const app = express();
const PORT = 3000;
const WS_PORT = 8080;

let targetStaticPath = __dirname;
if (fs.existsSync(path.join(__dirname, 'extraction_target_project'))) {
    targetStaticPath = path.join(__dirname, 'extraction_target_project');
} else if (fs.existsSync(path.join(__dirname, 'AI_agent', 'extraction_target_project'))) {
    targetStaticPath = path.join(__dirname, 'AI_agent', 'extraction_target_project');
}

app.use(express.static(targetStaticPath));
console.log(`📂 [Static Directory] 게임 정적 파일 서빙: ${targetStaticPath}`);

const server = http.createServer(app);
const wss = new WebSocket.Server({ port: WS_PORT });

// --- 페이즈(State Machine) 정의 ---
const Phase = {
    LOBBY: 'LOBBY',
    MENU: 'MENU',
    GAME: 'GAME',
    SCOREBOARD: 'SCOREBOARD'
};

let currentPhase = Phase.LOBBY;
let currentMasterSeed = null;

// 슬롯 상태: P1~P4 (최대 4명)
// 각 슬롯 구조: { slotIndex: 1~4, active: boolean, ready: boolean, vote: string|null, isAiMode: boolean, nickname: string, classType: string, ws: WebSocket|null }
const slots = {
    1: { slotIndex: 1, active: false, ready: false, vote: null, isAiMode: false, nickname: 'PLAYER 1', classType: 'bufferPlayer', ws: null },
    2: { slotIndex: 2, active: false, ready: false, vote: null, isAiMode: false, nickname: 'PLAYER 2', classType: 'empPlayer', ws: null },
    3: { slotIndex: 3, active: false, ready: false, vote: null, isAiMode: false, nickname: 'PLAYER 3', classType: 'shielderPlayer', ws: null },
    4: { slotIndex: 4, active: false, ready: false, vote: null, isAiMode: false, nickname: 'PLAYER 4', classType: 'summonerPlayer', ws: null }
};

/**
 * 0 ~ 4294967295 범위의 단일 masterSeed 생성
 */
function generateMasterSeed() {
    return Math.floor(Math.random() * 0xFFFFFFFF) >>> 0;
}

/**
 * 전체 클라이언트에게 브로드캐스트
 */
function broadcast(payloadObj) {
    const jsonStr = JSON.stringify(payloadObj);
    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(jsonStr);
        }
    });
}

/**
 * 현재 ROOM_STATE 패킷 생성 및 전송
 */
function broadcastRoomState() {
    const activeSlots = [];
    const slotDetails = [];

    for (let i = 1; i <= 4; i++) {
        const s = slots[i];
        if (s.active) {
            activeSlots.push(i);
        }
        slotDetails.push({
            slotIndex: i,
            active: s.active,
            ready: s.ready,
            vote: s.vote,
            isAiMode: s.isAiMode,
            nickname: s.nickname,
            classType: s.classType
        });
    }

    broadcast({
        type: 'ROOM_STATE',
        phase: currentPhase,
        activeSlots,
        slotDetails,
        masterSeed: currentMasterSeed
    });
}

/**
 * 투표 현황(VOTE_STATUS_UPDATE) 방송
 */
function broadcastVoteStatus() {
    const votes = {};
    for (let i = 1; i <= 4; i++) {
        if (slots[i].active) {
            votes[i] = slots[i].vote;
        }
    }
    broadcast({
        type: 'VOTE_STATUS_UPDATE',
        phase: currentPhase,
        votes
    });
}

/**
 * 페이즈 전환 함수
 * @param {string} nextPhase 
 */
function changePhase(nextPhase) {
    console.log(`🔄 [Phase Transition] ${currentPhase} ➔ ${nextPhase}`);
    currentPhase = nextPhase;

    // 모든 슬롯의 준비 및 표결 상태 초기화
    for (let i = 1; i <= 4; i++) {
        slots[i].ready = false;
        slots[i].vote = null;
    }

    let payload = {
        type: 'PHASE_CHANGE',
        phase: currentPhase
    };

    // GAME 페이즈 진입 시 단일 masterSeed 생성 및 하사
    if (currentPhase === Phase.GAME) {
        currentMasterSeed = generateMasterSeed();
        payload.masterSeed = currentMasterSeed;
        console.log(`🎲 [masterSeed Issued] 신규 게임 마스터 시드 생성: ${currentMasterSeed}`);
    }

    broadcast(payload);
    broadcastRoomState();
}

/**
 * LOBBY / MENU 상태 만장일치 레디 검사
 */
function checkReadyUnanimity() {
    const activeList = Object.values(slots).filter(s => s.active);
    if (activeList.length === 0) return;

    const allReady = activeList.every(s => s.ready === true);
    if (allReady) {
        if (currentPhase === Phase.LOBBY || currentPhase === Phase.MENU) {
            changePhase(Phase.GAME);
        }
    }
}

/**
 * SCOREBOARD 상태 표결 일치 검사
 */
function checkScoreboardVoting() {
    const activeList = Object.values(slots).filter(s => s.active);
    if (activeList.length === 0) return;

    // 모든 접속자가 투표를 마쳤는지 확인
    const allVoted = activeList.every(s => s.vote !== null);
    broadcastVoteStatus();

    if (allVoted) {
        const firstVote = activeList[0].vote;
        const isUnanimous = activeList.every(s => s.vote === firstVote);

        if (isUnanimous) {
            console.log(`🗳️ [Scoreboard Vote] 전원 일치 표결 완료: ${firstVote}`);
            if (firstVote === 'REPLAY') {
                changePhase(Phase.GAME);
            } else if (firstVote === 'MENU') {
                changePhase(Phase.MENU);
            }
        } else {
            console.log(`⚠️ [Scoreboard Vote] 표결 불일치 발생. 현 상태 유지`);
        }
    }
}

// 로컬 IP 검색
function getLocalIpAddress() {
    const interfaces = os.networkInterfaces();
    for (const name of Object.keys(interfaces)) {
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal) {
                return iface.address;
            }
        }
    }
    return 'localhost';
}

const localIp = getLocalIpAddress();

console.log('====================================================');
console.log(`🚀 [Bullet Hell Server] 웹소켓 & 멀티플레이어 마스터 서버 가동`);
console.log(`📱 클라이언트 접속 주소: http://${localIp}:${PORT}?client=true`);
console.log(`⚡ 웹소켓 포트: ${WS_PORT}`);
console.log('====================================================');

wss.on('connection', (ws) => {
    // 1. 빈 슬롯 자동 할당 (P1 ~ P4)
    let assignedSlot = null;
    for (let i = 1; i <= 4; i++) {
        if (!slots[i].active) {
            assignedSlot = i;
            slots[i].active = true;
            slots[i].ready = false;
            slots[i].vote = null;
            slots[i].ws = ws;
            break;
        }
    }

    if (!assignedSlot) {
        console.warn(`🚫 [Connection Rejected] 방이 가득 찼습니다 (4/4 Max).`);
        ws.send(JSON.stringify({ type: 'ROOM_FULL', error: '방이 가득 찼습니다.' }));
        ws.close();
        return;
    }

    ws.slotIndex = assignedSlot;
    console.log(`🌐 [Client Connected] P${assignedSlot} 슬롯 할당 (현재 활성: ${Object.values(slots).filter(s => s.active).length}명)`);

    // 신규 접속자에게 슬롯 할당 알림
    ws.send(JSON.stringify({
        type: 'SLOT_ASSIGNED',
        slotIndex: assignedSlot,
        phase: currentPhase,
        masterSeed: currentMasterSeed
    }));

    // 전원에게 방 상태 방송
    broadcastRoomState();

    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message.toString());

            // A. 준비(READY) 신호 수신
            if (data.type === 'SET_READY') {
                const s = slots[ws.slotIndex];
                if (s && s.active) {
                    s.ready = !!data.ready;
                    if (data.nickname) s.nickname = String(data.nickname).slice(0, 20);
                    if (data.classType) s.classType = String(data.classType);
                    console.log(`👍 [Ready Changed] P${ws.slotIndex} Ready: ${s.ready} (${s.nickname}, ${s.classType})`);
                    broadcastRoomState();
                    checkReadyUnanimity();
                }
            }
            // A-1. 상태 관리 신호 (Strict Sync): 프로필/슬롯 상태 변경 요청
            else if (data.type === 'UPDATE_SLOT_PROFILE') {
                const s = slots[ws.slotIndex];
                if (s && s.active) {
                    if (data.nickname) s.nickname = String(data.nickname).slice(0, 20);
                    if (data.classType) s.classType = String(data.classType);
                    if (typeof data.isAiMode === 'boolean') s.isAiMode = data.isAiMode;
                    console.log(`👤 [Slot Profile Updated] P${ws.slotIndex} Nickname: ${s.nickname}, Class: ${s.classType}, AiMode: ${s.isAiMode}`);
                    broadcastRoomState();
                }
            }
            // A-2. USER <-> AI 모드 토글 (서버 검증 후 ROOM_STATE 동기화)
            else if (data.type === 'TOGGLE_AI_MODE') {
                const targetSlot = (typeof data.slotIndex === 'number') ? data.slotIndex : ws.slotIndex;
                const s = slots[targetSlot];
                if (s && s.active) {
                    s.isAiMode = (typeof data.isAiMode === 'boolean') ? data.isAiMode : !s.isAiMode;
                    console.log(`🤖 [AI Mode Toggled] P${targetSlot} AiMode: ${s.isAiMode}`);
                    broadcastRoomState();
                }
            }
            // B. SCOREBOARD 표결(VOTE) 신호 수신 (REPLAY 또는 MENU)
            else if (data.type === 'SUBMIT_VOTE') {
                const s = slots[ws.slotIndex];
                if (s && s.active) {
                    s.vote = data.vote; // 'REPLAY' | 'MENU'
                    console.log(`🗳️ [Vote Submitted] P${ws.slotIndex} Vote: ${s.vote}`);
                    checkScoreboardVoting();
                }
            }
            // C. 조작 입력 동기화 (Continuous Movement & Trigger Action Relay)
            else if (data.type === 'INPUT_SYNC' || data.type === 'CLIENT_INPUT') {
                // 💡 ws.slotIndex가 미할당된 P1 소켓이라도 패킷 내 slotIndex(기본 1)를 사용하여 P1 릴레이 누락 차단
                const effectiveSlot = ws.slotIndex || data.slotIndex || 1;

                const relayPacket = {
                    type: 'INPUT_SYNC',
                    slotIndex: effectiveSlot,
                    sequenceNumber: data.sequenceNumber ?? data.inputAction?.sequenceNumber ?? 0,
                    timeStamp: data.timeStamp || Date.now(),
                    inputAction: data.inputAction
                };

                broadcast(relayPacket);
            }
            // D. 설치형 오브젝트 및 HP 상태 동기화 (Object & HP Sync - Owner Authority)
            else if (data.type === 'OBJECT_STATE_SYNC') {
                // 소유자(Owner)가 판정한 오브젝트 및 HP 상태를 전체 브로드캐스트
                broadcast({
                    type: 'OBJECT_STATE_SYNC',
                    slotIndex: ws.slotIndex,
                    timeStamp: data.timeStamp || Date.now(),
                    objects: data.objects || [],
                    hpState: data.hpState || null
                });
            }
            // C-1. 💡 [신규 - 입력 디버그 로그 브로드캐스트]: 키보드/마우스 입력 수신 시 서버 터미널 출력 및 전체 방송
            else if (data.type === 'DEBUG_INPUT_EVENT') {
                console.log(`📡 [Server Debug Sync] P${ws.slotIndex} (${data.source}): ${data.description}`);
                broadcast({
                    type: 'DEBUG_INPUT_EVENT',
                    slotIndex: ws.slotIndex,
                    source: data.source,
                    description: data.description,
                    timestamp: Date.now()
                });
            }
            // C-2. 확장형 슬롯 이벤트 릴레이
            else if (data.type === 'SLOT_EVENT_SYNC') {
                broadcast(data);
            }
            // D. 관리자/게임 트리거: 게임 종료 및 결과 화면 이동 요청
            else if (data.type === 'TRIGGER_SCOREBOARD') {
                changePhase(Phase.SCOREBOARD);
            }
            // E. 기타 범용 중계 패킷
            else {
                broadcast(data);
            }
        } catch (e) {
            console.warn('[Server] 패킷 처리 오류:', e);
        }
    });

    ws.on('close', () => {
        const slotIdx = ws.slotIndex;
        if (slotIdx && slots[slotIdx]) {
            slots[slotIdx].active = false;
            slots[slotIdx].ready = false;
            slots[slotIdx].vote = null;
            slots[slotIdx].ws = null;
            console.log(`❌ [Client Disconnected] P${slotIdx} 슬롯 퇴장 (남은 인원: ${Object.values(slots).filter(s => s.active).length}명)`);

            // 퇴장 후 인원 변동에 따른 갱신 및 표결/레디 재검사
            broadcastRoomState();

            if (currentPhase === Phase.LOBBY || currentPhase === Phase.MENU) {
                checkReadyUnanimity();
            } else if (currentPhase === Phase.SCOREBOARD) {
                checkScoreboardVoting();
            }
        }
    });
});

server.listen(PORT, () => {
    console.log(`🌐 HTTP 정적 웹 서버가 포트 ${PORT}에서 정상 대기 중입니다.`);
});
