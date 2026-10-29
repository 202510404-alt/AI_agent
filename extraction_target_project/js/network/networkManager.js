/**
 * js/network/networkManager.js
 * 클라이언트 네트워크 코어 (WebSocket 연결 및 패킷 디스패처)
 * 
 * [동작 명세 - 4단계 신호 동기화 표준 규격 및 예외 처리 가이드라인]
 * 1. 상태 관리 신호 (Strict Sync): ROOM_STATE 수신 시 단일 진실 공급원(Single Source of Truth)으로 동시 적용.
 * 2. 실시간 이동 신호 (Continuous Movement): Client Prediction + sequenceNumber 부여 + Dead Reckoning 지원.
 *    - 패킷 순서 엉킴(Out-of-Order / Packet Loss) 시 이전 sequenceNumber 패킷 무시(Discard).
 * 3. 1회성 트리거 신호 (Trigger Action): timeStamp / frameNumber 포함 패킷 릴레이 및 1회 소비.
 * 4. 설치형 오브젝트 & HP 판정 (Object & HP Sync): 시전자 소유권(Owner Authority) 기반 OBJECT_STATE_SYNC 송수신.
 */
import { seededRNG } from '../utils/seededRNG.js';

export class NetworkManager {
    /**
     * @param {object} options
     * @param {boolean} options.isHost 호스트 여부
     * @param {string} [options.hostIp] 접속 호스트 IP
     * @param {number} [options.port] 웹소켓 포트 (기본 8080)
     */
    constructor(options = {}) {
        this.isHost = options.isHost || false;
        this.hostIp = options.hostIp || 'localhost';
        this.port = options.port || 8080;
        this.socket = null;

        this.mySlotIndex = null;      // 서버가 할당해준 내 슬롯 번호 (1~4)
        this.activeSlots = [1];       // 현재 활성 슬롯 인덱스 목록
        this.slotDetails = [];        // 슬롯별 레디/투표/닉네임/직업 상세 상태
        this.currentPhase = 'LOBBY';  // LOBBY, MENU, GAME, SCOREBOARD
        this.masterSeed = null;
        this.serverClockOffsetMs = 0;
        this.clockSyncRttMs = Infinity;
        this.lastClockSyncAt = 0;
        this.timeSyncTimer = null;

        // 원격 입력 버퍼: slotIndex -> inputAction
        this.clientInputs = {};

        // 패킷 시퀀스 번호 (송신용 단조 증가 카운터)
        this.sequenceCounter = 0;
        this.lastSentAction = null;
        this.lastInputSentAt = 0;

        // 원격 슬롯별 마지막 수신 시퀀스 번호 추적 (Out-of-Order 무시용)
        this.lastReceivedSequences = {};

        // RTT(Ping) 추적을 위한 타임스탬프 맵
        this.estimatedPing = 50; // 기본 ms
        this.lastPingSentAt = 0;

        // 리스너 콜백 맵: eventName -> [callbacks]
        this.listeners = {
            ROOM_STATE: [],
            PHASE_CHANGE: [],
            INPUT_SYNC: [],
            PLAYER_SHOT_SYNC: [],
            PLAYER_SKILL_SYNC: [],
            TIME_SYNC_RESPONSE: [],
            SLOT_ASSIGNED: [],
            SLOT_EVENT_SYNC: [],
            AI_STATE_SYNC: [],
            OBJECT_STATE_SYNC: [],
            VOTE_STATUS_UPDATE: [],
            DEBUG_INPUT_EVENT: []
        };
    }

    /**
     * 소켓 네트워크 초기화
     */
    init() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const urlParams = new URLSearchParams(window.location.search);
        const targetHost = urlParams.get('host') || window.location.hostname || 'localhost';
        const wsUrl = `${protocol}//${targetHost}:${this.port}`;

        try {
            this.socket = new WebSocket(wsUrl);

            this.socket.onopen = () => {
                this.lastSentAction = null;
                this.lastInputSentAt = 0;
                this.requestTimeSync();
                if (!this.timeSyncTimer) {
                    this.timeSyncTimer = setInterval(() => this.requestTimeSync(), 5000);
                }
                console.log(`🌐 [NetworkManager] 웹소켓 서버 연결 완료 (${wsUrl})`);
                // 내 닉네임 / 직업 정보가 준비되어 있다면 초기 동기화
                this.syncLocalProfile();
            };

            this.socket.onmessage = (event) => {
                try {
                    const packet = JSON.parse(event.data);
                    this.dispatchPacket(packet);
                } catch (e) {
                    console.warn('[NetworkManager] 패킷 파싱 에러:', e);
                }
            };

            this.socket.onerror = (err) => {
                console.warn('[NetworkManager] 소켓 연결 에러/대기 중 (오프라인 로컬 폴백 동작)');
            };

            this.socket.onclose = () => {
                if (this.timeSyncTimer) clearInterval(this.timeSyncTimer);
                this.timeSyncTimer = null;
                console.warn('[NetworkManager] 소켓 연결 종료. 3초 후 재연결 시도...');
                setTimeout(() => {
                    this.init();
                }, 3000);
            };
        } catch (e) {
            console.warn('[NetworkManager] 소켓 생성 실패:', e);
        }
    }

    /**
     * 이벤트 리스너 등록
     * @param {string} type 
     * @param {Function} callback 
     */
    on(type, callback) {
        if (!this.listeners[type]) {
            this.listeners[type] = [];
        }
        this.listeners[type].push(callback);
    }

    /**
     * 수신된 패킷 분기 및 이벤트 디스패치
     * @param {object} packet 
     */
    dispatchPacket(packet) {
        if (!packet || !packet.type) return;

        switch (packet.type) {
            case 'SLOT_ASSIGNED':
                this.mySlotIndex = packet.slotIndex;
                if (packet.phase) this.currentPhase = packet.phase;
                if (packet.masterSeed) {
                    this.setMasterSeed(packet.masterSeed);
                }
                console.log(`🎮 [NetworkManager] 내 슬롯 할당: P${this.mySlotIndex}`);
                this.syncLocalProfile();
                break;

            case 'ROOM_STATE':
                // 1. 상태 관리 신호 (Strict Sync) - Single Source of Truth
                this.activeSlots = packet.activeSlots || [];
                this.slotDetails = packet.slotDetails || [];
                if (packet.phase) this.currentPhase = packet.phase;
                if (packet.masterSeed && packet.masterSeed !== this.masterSeed) {
                    this.setMasterSeed(packet.masterSeed);
                }

                // 기체/닉네임/AI 모드 및 human 플래그 전 기기 동시 적용
                if (window.gameLoopInstance && window.gameLoopInstance.slots) {
                    window.gameLoopInstance.slots.forEach((player, idx) => {
                        const slotNum = idx + 1;
                        const detail = this.slotDetails.find(d => d.slotIndex === slotNum);
                        if (detail) {
                            // AI 모드가 활성화되어 있으면 isHuman = false
                            player.isHuman = detail.active && !detail.isAiMode;
                            if (detail.nickname) player.nickname = detail.nickname;
                            if (detail.classType && player.classType !== detail.classType) {
                                player.classType = detail.classType;
                            }
                        } else {
                            player.isHuman = this.activeSlots.includes(slotNum);
                        }
                    });
                    const localPlayer = window.gameLoopInstance.slots[this.mySlotIndex - 1];
                    const input = window.gameLoopInstance.input;
                    if (localPlayer && input && input.isAiMode === localPlayer.isHuman) {
                        input.setAiMode(!localPlayer.isHuman);
                    }
                    const gameLoop = window.gameLoopInstance;
                    if (gameLoop.ui && typeof gameLoop.ui.updateSlotAndStats === 'function') {
                        gameLoop.ui.updateSlotAndStats(gameLoop.slots);
                    }
                    const statusText = document.getElementById('top-ai-status-text');
                    if (statusText && localPlayer) {
                        statusText.innerText = localPlayer.isHuman ? 'USER (MANUAL)' : 'AI (AUTO)';
                        statusText.className = localPlayer.isHuman ? 'text-cyan-400 font-bold' : 'text-pink-400 font-bold';
                    }
                }
                break;

            case 'PHASE_CHANGE':
                this.currentPhase = packet.phase;
                console.log(`🔄 [NetworkManager] 페이즈 전환 수신: ${this.currentPhase}`);
                if (packet.masterSeed) {
                    this.setMasterSeed(packet.masterSeed);
                }
                break;

            case 'INPUT_SYNC':
            case 'CLIENT_INPUT': {
                const sIdx = packet.slotIndex;
                if (!sIdx) break;

                const remoteAction = packet.inputAction || {};
                const seq = packet.sequenceNumber ?? remoteAction.sequenceNumber ?? 0;

                // 💡 [원격 슬롯 연동 보장]: 내 슬롯이 아닌 모든 상대 슬롯(P1, P2 등) 패킷을 강제 캐싱
                // 핑(Ping) 계산 및 최신 패킷 버퍼링
                if (packet.timeStamp) {
                    const latency = Math.max(0, Date.now() - packet.timeStamp);
                    this.estimatedPing = Math.round(this.estimatedPing * 0.8 + latency * 0.2);
                }

                const action = { ...remoteAction };
                action.sequenceNumber = seq;
                action.timeStamp = packet.timeStamp || Date.now();
                action.estimatedPing = this.estimatedPing;

                // 💡 상대방 슬롯 입력 버퍼에 유실 없이 보관 (gameLoop.js에서 소비)
                this.clientInputs[sIdx] = action;
                break;
            }

            case 'TIME_SYNC_RESPONSE': {
                const receivedAt = Date.now();
                const rtt = receivedAt - packet.clientSentAt;
                if (Number.isFinite(rtt) && rtt >= 0 && rtt < 5000 &&
                    Number.isFinite(packet.serverTime) &&
                    (rtt < this.clockSyncRttMs || receivedAt - this.lastClockSyncAt > 15000)) {
                    this.serverClockOffsetMs = packet.serverTime - (packet.clientSentAt + receivedAt) / 2;
                    this.clockSyncRttMs = rtt;
                    this.lastClockSyncAt = receivedAt;
                }
                break;
            }

            case 'OBJECT_STATE_SYNC':
                // 4. 설치형 오브젝트 & HP 판정 (Object & HP Sync)
                break;

            case 'DEBUG_INPUT_EVENT':
                console.log(`[NET DEBUG RECV] Slot P${packet.slotIndex} | Source: [${packet.source}] | ${packet.description}`);
                break;

            case 'SLOT_EVENT_SYNC':
                console.log(`⚡ [NetworkManager] 슬롯 이벤트 수신: P${packet.slotIndex} -> ${packet.eventType}`, packet.payload);
                break;

            case 'VOTE_STATUS_UPDATE':
                console.log(`🗳️ [NetworkManager] 표결 현황 갱신:`, packet.votes);
                break;
        }

        // 등록된 리스너들에게 패킷 전달
        const cbs = this.listeners[packet.type] || [];
        cbs.forEach(cb => {
            try {
                cb(packet);
            } catch (err) {
                console.error(`[NetworkManager] 리스너 실행 오류 (${packet.type}):`, err);
            }
        });
    }

    /**
     * 로컬 UI(닉네임, 선택 직업) 상태를 서버 중앙 데이터로 동기화 요청
     */
    syncLocalProfile() {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN || !this.mySlotIndex) return;

        const nameInput = document.getElementById(`p${this.mySlotIndex}-nickname`);
        const classSelect = document.getElementById(`p${this.mySlotIndex}-class`);
        const nickname = nameInput ? nameInput.value.trim() : `PLAYER ${this.mySlotIndex}`;
        const classType = classSelect ? classSelect.value : 'bufferPlayer';

        this.sendSlotProfile(this.mySlotIndex, { nickname, classType });
    }

    /**
     * masterSeed 수신 시 seededRNG 모듈 초기화
     * @param {number|string} seed 
     */
    setMasterSeed(seed) {
        this.masterSeed = seed;
        window.selectedMatchSeed = seed;
        seededRNG.initDerivations(seed);
        console.log(`🎲 [NetworkManager] masterSeed(${seed}) 수신 및 seededRNG 전역 초기화 완료`);
    }

    /**
     * [1. 상태 관리 신호 - Strict Sync] 슬롯 프로필(닉네임, 클래스) 변경 요청
     * @param {number} slotIndex 
     * @param {object} profile { nickname, classType, isAiMode }
     */
    sendSlotProfile(slotIndex, profile = {}) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'UPDATE_SLOT_PROFILE',
            slotIndex: slotIndex || this.mySlotIndex,
            ...profile
        }));
    }

    /**
     * [1. 상태 관리 신호 - Strict Sync] USER <-> AI 모드 전환 요청
     * 클라이언트 단독 즉시 전환을 금지하고 서버에 요청
     * @param {number} slotIndex 
     * @param {boolean} [isAiMode]
     */
    requestToggleAiMode(slotIndex, isAiMode) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            // 오프라인 폴백
            if (window.gameLoopInstance && typeof window.gameLoopInstance.applySlotAiMode === 'function') {
                window.gameLoopInstance.applySlotAiMode(slotIndex, isAiMode);
            }
            return;
        }
        this.socket.send(JSON.stringify({
            type: 'TOGGLE_AI_MODE',
            slotIndex: slotIndex || this.mySlotIndex,
            isAiMode
        }));
    }

    sendAiStateSync(sequence, slots) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'AI_STATE_SYNC',
            sequence,
            slots
        }));
    }

    /**
     * [2. 실시간 이동 + 3. 1회성 트리거]
     * 내 조작 입력 보따리 프레임 단위 압축 송신 (INPUT_SYNC)
     * - sequenceNumber 단조 증가 부여
     * - timeStamp 포함
     * - posX, posY (Client Prediction 검증 및 Dead Reckoning용)
     * @param {number} slotIndex 
     * @param {object} inputAction { moveX, moveY, mouseX, mouseY, useSkill, posX, posY, timeStamp }
     */
    sendInputSync(slotIndex, inputAction) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        
        // 💡 [P1/호스트 예외 보장]: mySlotIndex가 초기에 null이어도 slotIndex(기본 1)를 활용하여 P1 패킷 송신 차단 해제
        const activeSlot = slotIndex || this.mySlotIndex || 1;

        const currentMoveX = inputAction.moveX || 0;
        const currentMoveY = inputAction.moveY || 0;
        const currentSkill = !!inputAction.useSkill;

        const now = Date.now();
        const previous = this.lastSentAction;
        const moving = currentMoveX !== 0 || currentMoveY !== 0;
        const wasMoving = !!previous && (previous.moveX !== 0 || previous.moveY !== 0);
        const movementStartedOrStopped = !previous || moving !== wasMoving;
        const positionChanged = !previous || Math.hypot((inputAction.posX ?? 0) - (previous.posX ?? 0), (inputAction.posY ?? 0) - (previous.posY ?? 0)) >= 0.5;
        const aimChanged = !previous || Math.hypot((inputAction.mouseX ?? 0) - (previous.mouseX ?? 0), (inputAction.mouseY ?? 0) - (previous.mouseY ?? 0)) >= 1;
        // 이동과 조준 변화는 초당 최대 20회 보내며 시작·정지와 스킬은 즉시 보낸다.
        if (!movementStartedOrStopped && !currentSkill &&
            ((!positionChanged && !aimChanged && !moving) || now - this.lastInputSentAt < 50)) return;

        this.sequenceCounter = (this.sequenceCounter + 1) >>> 0;
        this.lastSentAction = { moveX: currentMoveX, moveY: currentMoveY, posX: inputAction.posX, posY: inputAction.posY, mouseX: inputAction.mouseX, mouseY: inputAction.mouseY };
        this.lastInputSentAt = now;

        const payload = {
            type: 'INPUT_SYNC',
            slotIndex: activeSlot,
            sequenceNumber: this.sequenceCounter,
            timeStamp: inputAction.timeStamp || Date.now(),
            inputAction: {
                moveX: currentMoveX,
                moveY: currentMoveY,
                dx: inputAction.dx !== undefined ? inputAction.dx : currentMoveX,
                dy: inputAction.dy !== undefined ? inputAction.dy : currentMoveY,
                mouseX: inputAction.mouseX,
                mouseY: inputAction.mouseY,
                useSkill: currentSkill,
                sequenceNumber: this.sequenceCounter,
                posX: inputAction.posX,
                posY: inputAction.posY,
                speed: inputAction.speed
            }
        };

        this.socket.send(JSON.stringify(payload));
    }

    sendPlayerShot(slotIndex, bullet) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'PLAYER_SHOT_SYNC',
            slotIndex,
            x: bullet.x,
            y: bullet.y,
            angle: bullet.angle,
            damage: bullet.damage
        }));
    }

    sendPlayerSkill(slotIndex, skillState) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'PLAYER_SKILL_REQUEST',
            slotIndex,
            ...skillState
        }));
    }

    requestTimeSync() {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({ type: 'TIME_SYNC_REQUEST', clientSentAt: Date.now() }));
    }

    getSkillExecutionDelay(executeAt, serverSentAt) {
        if (this.lastClockSyncAt && Date.now() - this.lastClockSyncAt < 30000) {
            return Math.max(0, executeAt - (Date.now() + this.serverClockOffsetMs));
        }
        // 시계 동기화 전에는 서버가 보장한 준비 시간에서 전송 지연을 보수적으로 뺀다.
        return Math.max(0, executeAt - serverSentAt - 50);
    }

    /**
     * [4. 설치형 오브젝트 & HP 판정 - Object & HP Sync]
     * 시전자 기기(Owner)가 판정한 오브젝트 상태 및 HP 동기화 패킷 전송
     * @param {number} slotIndex 소유자 슬롯
     * @param {Array} objects 방벽 / 미니언 상태 목록 [{ id, type, x, y, hp, maxHp, isDead, angle, duration }]
     * @param {object} [hpState] 기체 본체 HP 상태 { hp, maxHp, isStunned }
     */
    sendObjectStateSync(slotIndex, objects = [], hpState = null) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'OBJECT_STATE_SYNC',
            slotIndex: slotIndex || this.mySlotIndex,
            timeStamp: Date.now(),
            objects,
            hpState
        }));
    }

    /**
     * 확장형 범용 슬롯 이벤트 송신 (하위 호환)
     */
    sendSlotEvent(slotIndex, eventType, payload = {}) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'SLOT_EVENT_SYNC',
            slotIndex: slotIndex || this.mySlotIndex,
            eventType,
            payload
        }));
    }

    /**
     * 디버그 입력 전송 메서드
     */
    sendDebugInput(source, description) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'DEBUG_INPUT_EVENT',
            slotIndex: this.mySlotIndex || 1,
            source,
            description
        }));
    }

    sendClientInput(slotIndex, inputAction) {
        this.sendInputSync(slotIndex, inputAction);
    }

    /**
     * [클라이언트 ➔ 서버] LOBBY / MENU 상태 준비(READY) 신호 송신
     * @param {boolean} ready 
     * @param {object} [profile]
     */
    sendReady(ready = true, profile = {}) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'SET_READY',
            ready,
            ...profile
        }));
    }

    /**
     * [클라이언트 ➔ 서버] SCOREBOARD 결과 화면 표결(VOTE) 신호 송신
     * @param {'REPLAY'|'MENU'} voteChoice 
     */
    sendVote(voteChoice) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'SUBMIT_VOTE',
            vote: voteChoice
        }));
    }

    requestScoreboard(score) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({ type: 'TRIGGER_SCOREBOARD', score }));
    }

    /**
     * 슬롯별 수신된 원격 조작 입력 패킷 꺼내기 및 소비
     * @param {number} slotIndex 
     * @returns {object|null}
     */
    consumeClientInput(slotIndex) {
        const input = this.clientInputs[slotIndex] || null;
        this.clientInputs[slotIndex] = null;
        return input;
    }
}

export default NetworkManager;
