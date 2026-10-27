/**
 * js/network/networkManager.js
 * 오프라인 부스 전용 호스트-클라이언트 웹소켓 배달망 매니저
 */

export class NetworkManager {
    /**
     * @param {object} options
     * @param {boolean} options.isHost 호스트(1번 컴) 여부
     * @param {string} [options.hostIp] 클라이언트 접속용 방장 IP
     * @param {number} [options.port] 웹소켓 포트 (기본 8080)
     */
    constructor(options = {}) {
        this.isHost = options.isHost || false;
        this.hostIp = options.hostIp || 'localhost';
        this.port = options.port || 8080;
        this.socket = null;
        this.mySlotIndex = this.isHost ? 1 : null; // 호스트는 기본 1번, 클라이언트는 서버 수신값
        this.activeSlots = [1]; // 현재 접속 중인 슬롯 배열
        this.clientInputs = {}; // 호스트가 수신한 슬롯별 클라이언트 패킷 저장소 { 1: inputAction, 2: inputAction ... }
        this.onGameStateReceived = null; // 클라이언트가 수신할 상태 업데이트 콜백
    }

    /**
     * 소켓 네트워크 초기화
     */
    init() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const urlParams = new URLSearchParams(window.location.search);
        // URL의 host 파라미터가 있으면 가져오고, 없으면 현재 브라우저가 접속한 호스트 IP 주소를 자동 채택
        const targetHost = urlParams.get('host') || window.location.hostname || 'localhost';
        
        const wsUrl = `${protocol}//${targetHost}:${this.port}`;

        try {
            this.socket = new WebSocket(wsUrl);

            this.socket.onopen = () => {
                console.log(`[NetworkManager] 네트워크 배달망 연결 완료 (${this.isHost ? 'HOST' : 'CLIENT'})`);
            };

            this.socket.onmessage = (event) => {
                try {
                    const packet = JSON.parse(event.data);
                    this.handleIncomingPacket(packet);
                } catch (e) {
                    console.warn('[NetworkManager] 패킷 파싱 에러:', e);
                }
            };

            this.socket.onerror = (err) => {
                console.warn('[NetworkManager] 네트워크 소켓 연결 대기 중 (오프라인 단독 모드 유지)');
            };

            // 💡 끊김 발생 시 3초 후 자동 재연결
            this.socket.onclose = () => {
                console.warn('[NetworkManager] 소켓 연결 끊김. 3초 후 재연결 시도...');
                setTimeout(() => {
                    if (!this.isHost) this.init();
                }, 3000);
            };
        } catch (e) {
            console.warn('[NetworkManager] 소켓 초기화 실패 (로컬 단독 모드로 동작)');
        }
    }

    /**
     * 수신된 패킷 분기 처리
     */
    handleIncomingPacket(packet) {
        if (!packet || !packet.type) return;

        if (packet.type === 'SLOT_ASSIGNED') {
            this.mySlotIndex = packet.slotIndex;
            console.log(`🎮 내 할당 슬롯: P${this.mySlotIndex}`);
        } else if (packet.type === 'ROOM_STATE') {
            this.activeSlots = packet.activeSlots;
            console.log(`👥 현재 접속된 슬롯 목록:`, this.activeSlots);
        } else if (packet.type === 'CLIENT_INPUT') {
            // 호스트/클라이언트 모두 슬롯별 조작 패킷 수신 저장
            this.clientInputs[packet.slotIndex] = packet.inputAction;
        }
    }

    /**
     * [클라이언트 ➔ 호스트] 내 조작 보따리 전송
     */
    sendClientInput(slotIndex, inputAction) {
        if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'CLIENT_INPUT',
            slotIndex,
            inputAction
        }));
    }

    /**
     * [호스트 ➔ 클라이언트] 전체 렌더링 게임 상태 브로드캐스팅
     */
    broadcastGameState(gameState) {
        if (!this.isHost || !this.socket || this.socket.readyState !== WebSocket.OPEN) return;
        this.socket.send(JSON.stringify({
            type: 'HOST_GAME_STATE',
            state: gameState
        }));
    }

    /**
     * 특정 슬롯의 클라이언트 입력 보따리 꺼내기 (호스트 전용)
     */
    consumeClientInput(slotIndex) {
        const input = this.clientInputs[slotIndex] || null;
        this.clientInputs[slotIndex] = null; // 소비 후 초기화
        return input;
    }
}