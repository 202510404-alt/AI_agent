/**
 * js/network/networkManager.js
 * 클라이언트 네트워크 코어 (WebSocket 연결 및 패킷 디스패처)
 * 
 * [동작 명세]
 * 1. WebSocket 연결 생명주기 관리 및 자동 재연결.
 * 2. masterSeed 수신 시 seededRNG 모듈 초기화.
 * 3. ROOM_STATE, PHASE_CHANGE, INPUT_SYNC 패킷 디스패처 구축.
 * 4. 표결 및 레디 패킷 송신 (SET_READY, SUBMIT_VOTE).
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

        this.mySlotIndex = null;      // 서버가 할당해줄 슬롯 번호 (1~4)
        this.activeSlots = [1];       // 현재 활성 슬롯 인덱스 목록
        this.slotDetails = [];        // 슬롯별 레디/투표 상세 상태
        this.currentPhase = 'LOBBY';  // LOBBY, MENU, GAME, SCOREBOARD
        this.masterSeed = null;

        // 원격 입력 버퍼: { 1: inputAction, 2: inputAction, 3: inputAction, 4: inputAction }
        this.clientInputs = {};

        // 리스너 콜백 맵: eventName -> [callbacks]
        this.listeners = {
            ROOM_STATE: [],
            PHASE_CHANGE: [],
            INPUT_SYNC: [],
            SLOT_ASSIGNED: [],
            SLOT_EVENT_SYNC: [],
            VOTE_STATUS_UPDATE: []
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
                console.log(`🌐 [NetworkManager] 웹소켓 서버 연결 완료 (${wsUrl})`);
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
                break;

            case 'ROOM_STATE':
                this.activeSlots = packet.activeSlots || [];
                this.slotDetails = packet.slotDetails || [];
                if (packet.phase) this.currentPhase = packet.phase;
                if (packet.masterSeed && packet.masterSeed !== this.masterSeed) {
                    this.setMasterSeed(packet.masterSeed);
                }
                
                // 현재 게임 진행 중일 경우 접속된 유저 슬롯들의 isHuman 제어 플래그 실시간 갱신
                if (window.gameLoopInstance && window.gameLoopInstance.slots) {
                    window.gameLoopInstance.slots.forEach((player, idx) => {
                        const slotNum = idx + 1;
                        player.isHuman = this.activeSlots.includes(slotNum);
                    });
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
            case 'CLIENT_INPUT':
                // 원격 조작 입력 패킷 캐싱
                if (packet.slotIndex) {
                    this.clientInputs[packet.slotIndex] = packet.inputAction;
                }
                break;

            // 💡 [신규 - 디버그 수신 전역 로그]: 상대방 및 전체 노드에서 전달된 입력 로그 출력
            case 'DEBUG_INPUT_EVENT':
                console.log(`[NET DEBUG RECV] Slot P${packet.slotIndex} | Source: [${packet.source}] | ${packet.description}`);
                break;

            // 💡 [신규 - 슬롯 이벤트 수신 로그]: 원격 슬롯 이벤트 수신 로깅
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
     * [클라이언트 ➔ 서버] 내 조작 입력 보따리 압축 송신 (INPUT_SYNC)
     * @param {number} slotIndex 
     * @param {object} inputAction { moveX, moveY, useSkill, mouseX, mouseY }
     */
    sendInputSync(slotIndex, inputAction) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'INPUT_SYNC',
            slotIndex: slotIndex || this.mySlotIndex,
            inputAction
        }));
    }

    /**
     * 💡 [신규 - 확장형 범용 슬롯 이벤트 송신]: AI 모드 전환, 스킬, 상태 동기화 통일 규격 패킷
     * @param {number} slotIndex 슬롯 번호 (1~4)
     * @param {string} eventType 이벤트 이름 (예: 'TOGGLE_AI_MODE')
     * @param {object} payload 상세 데이터 ({ isAiMode: true 등 })
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
     * 💡 [신규 - 디버그 입력 전송 메서드]: 키/마우스 클릭 발생 시 서버로 신호 송신
     */
    sendDebugInput(source, description) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
            console.warn(`⚠️ [Debug Send Failed] Socket not open. (${source}: ${description})`);
            return;
        }
        this.socket.send(JSON.stringify({
            type: 'DEBUG_INPUT_EVENT',
            slotIndex: this.mySlotIndex || 1,
            source,
            description
        }));
    }

    /**
     * 하위 호환용 sendClientInput alias
     */
    sendClientInput(slotIndex, inputAction) {
        this.sendInputSync(slotIndex, inputAction);
    }

    /**
     * [클라이언트 ➔ 서버] LOBBY / MENU 상태 준비(READY) 신호 송신
     * @param {boolean} ready 
     */
    sendReady(ready = true) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'SET_READY',
            ready
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
