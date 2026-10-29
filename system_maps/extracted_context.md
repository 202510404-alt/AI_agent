# ==========================================================================
# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드
# [SCAN_MODE] EXTRACTION_TARGET_PROJECT
# ==========================================================================
# 📄 [요청 1] TARGET: js/network/networkManager.js (14-407라인)
# ----------------------------------------------------------
```python
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

        // 원격 입력 버퍼: slotIndex -> inputAction
        this.clientInputs = {};

        // 패킷 시퀀스 번호 (송신용 단조 증가 카운터)
        this.sequenceCounter = 0;

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
            SLOT_ASSIGNED: [],
            SLOT_EVENT_SYNC: [],
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

                // 2. 패킷 순서 엉킴 및 손실 방지 (Out-of-Order / Packet Loss)
                const seq = packet.sequenceNumber;
                if (typeof seq === 'number') {
                    const lastSeq = this.lastReceivedSequences[sIdx] || 0;
                    if (seq < lastSeq) {
                        // 오래된 순번의 패킷은 즉시 폐기 (Discard)
                        return;
                    }
                    this.lastReceivedSequences[sIdx] = seq;
                }

                // 핑(Ping) 계산: timeStamp 기반 RTT 근사치 갱신
                if (packet.timeStamp) {
                    const latency = Math.max(0, Date.now() - packet.timeStamp);
                    this.estimatedPing = Math.round(this.estimatedPing * 0.8 + latency * 0.2);
                }

                // 원격 조작 입력 패킷 캐싱
                const action = packet.inputAction || {};
                action.sequenceNumber = seq;
                action.timeStamp = packet.timeStamp || Date.now();
                action.estimatedPing = this.estimatedPing;

                this.clientInputs[sIdx] = action;
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
        
        this.sequenceCounter = (this.sequenceCounter + 1) >>> 0;

        const payload = {
            type: 'INPUT_SYNC',
            slotIndex: slotIndex || this.mySlotIndex,
            sequenceNumber: this.sequenceCounter,
            timeStamp: inputAction.timeStamp || Date.now(),
            inputAction: {
                moveX: inputAction.moveX || 0,
                moveY: inputAction.moveY || 0,
                dx: inputAction.dx !== undefined ? inputAction.dx : inputAction.moveX || 0,
                dy: inputAction.dy !== undefined ? inputAction.dy : inputAction.moveY || 0,
                mouseX: inputAction.mouseX,
                mouseY: inputAction.mouseY,
                useSkill: !!inputAction.useSkill,
                posX: inputAction.posX,
                posY: inputAction.posY,
                speed: inputAction.speed
            }
        };

        this.socket.send(JSON.stringify(payload));
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
```

# 📄 [요청 1 ➡️ 불러온함수 (NetworkManager 본체)] TARGET: extraction_target_project/js/network/networkManager.js (14-407라인)
# ----------------------------------------------------------
```python
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

        // 원격 입력 버퍼: slotIndex -> inputAction
        this.clientInputs = {};

        // 패킷 시퀀스 번호 (송신용 단조 증가 카운터)
        this.sequenceCounter = 0;

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
            SLOT_ASSIGNED: [],
            SLOT_EVENT_SYNC: [],
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

                // 2. 패킷 순서 엉킴 및 손실 방지 (Out-of-Order / Packet Loss)
                const seq = packet.sequenceNumber;
                if (typeof seq === 'number') {
                    const lastSeq = this.lastReceivedSequences[sIdx] || 0;
                    if (seq < lastSeq) {
                        // 오래된 순번의 패킷은 즉시 폐기 (Discard)
                        return;
                    }
                    this.lastReceivedSequences[sIdx] = seq;
                }

                // 핑(Ping) 계산: timeStamp 기반 RTT 근사치 갱신
                if (packet.timeStamp) {
                    const latency = Math.max(0, Date.now() - packet.timeStamp);
                    this.estimatedPing = Math.round(this.estimatedPing * 0.8 + latency * 0.2);
                }

                // 원격 조작 입력 패킷 캐싱
                const action = packet.inputAction || {};
                action.sequenceNumber = seq;
                action.timeStamp = packet.timeStamp || Date.now();
                action.estimatedPing = this.estimatedPing;

                this.clientInputs[sIdx] = action;
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
        
        this.sequenceCounter = (this.sequenceCounter + 1) >>> 0;

        const payload = {
            type: 'INPUT_SYNC',
            slotIndex: slotIndex || this.mySlotIndex,
            sequenceNumber: this.sequenceCounter,
            timeStamp: inputAction.timeStamp || Date.now(),
            inputAction: {
                moveX: inputAction.moveX || 0,
                moveY: inputAction.moveY || 0,
                dx: inputAction.dx !== undefined ? inputAction.dx : inputAction.moveX || 0,
                dy: inputAction.dy !== undefined ? inputAction.dy : inputAction.moveY || 0,
                mouseX: inputAction.mouseX,
                mouseY: inputAction.mouseY,
                useSkill: !!inputAction.useSkill,
                posX: inputAction.posX,
                posY: inputAction.posY,
                speed: inputAction.speed
            }
        };

        this.socket.send(JSON.stringify(payload));
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
```

# 📄 [요청 2] TARGET: js/player/basePlayer.js (15-462라인)
# ----------------------------------------------------------
```python
export default class BasePlayer {
    /**
     * @param {number} slotIndex 슬롯 인덱스 (0 ~ TOTAL_SLOTS - 1)
     * @param {string} classType 플레이어 직업 타입 ('bufferPlayer', 'defaultPlayer')
     */
    constructor(slotIndex, classType = 'defaultPlayer') {
        this.slotIndex = slotIndex;
        this.id = slotIndex + 1;
        this.color = SLOT_COLORS[slotIndex % SLOT_COLORS.length];
        this.isHuman = (slotIndex === 0);
        this.classType = classType;

        // 💡 [멀티플레이 권한 시스템]: 내가 직접 키보드/마우스로 조종하는 기체인지 여부 (IsLocalOwner)
        this.isLocalOwner = false;

        // 💡 [Dead Reckoning & 원격 상태 수신 변수]
        this.remoteInputPacket = null;
        this.lastReceivedSeq = 0;
        this.netTargetX = 0;
        this.netTargetY = 0;
        this.netVelocityX = 0;
        this.netVelocityY = 0;
        this.netEstimatedPing = 50; // ms

        // Hard Snap 임계값 (예측 오차가 이 값을 초과하면 즉시 강제 이동)
        this.HARD_SNAP_THRESHOLD = 150;

        // --- 공통 메타 속성 (하위 캐릭터 파일에서 오버라이드) ---
        this.className = '기본 기체';
        this.themeColor = '#06b6d4';
        this.hasActiveSkill = false;
        this.skillIconClass = 'fa-solid fa-bolt';
        this.skillName = 'SKILL';
        this.skillFloatText = 'SKILL ACTIVATED!';

        this.radius = 8;
        this.moveSpeed = 300; // px/sec 기준 (기본)
        this.speed = 5.2;

        // 체력 및 기절 시스템
        this.maxHp = 5;
        this.hp = 5;
        this.stunTimer = 0.0;

        // 위치 및 목표 좌표
        this.x = 0;
        this.y = 0;
        this.targetX = 0;
        this.targetY = 0;

        // 통계 및 상태값
        this.damageDealt = 0;
        this.kills = 0;
        this.mistakesCount = 0;
        this.attackCooldown = 0;
        this.attackSpeed = 8;
        this.invulnerableTimer = 0.0;

        // 델타룬 Graze 게이지
        this.gauge = 0;             
        this.maxGauge = 100;
        this.grazeRadius = 45;   
        this.grazeCheckTimer = 0.0; 
        this.grazeEffectTimer = 0;  

        // 동적 스탯 수정자 파이프라인
        this.modifiers = [];     

        // AI FSM 필드
        this.fsmState = 'IDLE';
        this.actionLockTimer = 0.0;
        this.dodgeFatigue = 0.0;
        this.lastMistakeType = 'NONE';
    }

    /**
     * 동적 스탯 수정자(Modifier) 추가
     */
    addModifier(mod) {
        if (!mod || !mod.key) return;
        this.removeModifier(mod.key);
        this.modifiers.push({
            key: mod.key,
            type: mod.type || 'buff',
            stat: mod.stat || 'all',
            value: mod.value || 0,
            duration: mod.duration || 1.0,
            elapsed: 0
        });
    }

    removeModifier(key) {
        this.modifiers = this.modifiers.filter(m => m.key !== key);
    }

    getModifierValue(stat) {
        let total = 0;
        for (const mod of this.modifiers) {
            if (mod.stat === stat || mod.stat === 'all') {
                total += mod.value;
            }
        }
        return total;
    }

    updateModifiers(dt) {
        for (let i = this.modifiers.length - 1; i >= 0; i--) {
            const mod = this.modifiers[i];
            mod.elapsed += dt;
            if (mod.elapsed >= mod.duration) {
                this.modifiers.splice(i, 1);
            }
        }
    }

    /**
     * 델타룬 Graze 판정
     */
    updateGraze(enemyBullets, dt) {
        if (!enemyBullets || enemyBullets.length === 0) return;

        if (this.grazeEffectTimer > 0) {
            this.grazeEffectTimer = Math.max(0, this.grazeEffectTimer - dt);
        }

        for (const b of enemyBullets) {
            if (!b || b.isDead) continue;

            if (!b.grazedSlots) {
                b.grazedSlots = [];
            }

            if (b.grazedSlots.includes(this.slotIndex)) continue;

            const dist = Math.hypot(b.x - this.x, b.y - this.y);

            if (dist > this.radius && dist <= this.grazeRadius) {
                b.grazedSlots.push(this.slotIndex);
                this.gauge = Math.min(this.maxGauge, this.gauge + 1);
                this.grazeEffectTimer = 0.2;
            }
        }
    }

    /**
     * 클래스별 개별 maxGauge 기준 100% 충전 여부 판단
     */
    isSkillReady() {
        const isStun = typeof this.isStunned === 'function' ? this.isStunned() : false;
        const targetMax = this.maxGauge || 100;
        const currentGauge = this.gauge || 0;

        if (isStun) return false;
        if (currentGauge < targetMax) return false;

        return true;
    }

    /**
     * 기본 스킬 시전 검사 및 게이지 초기화
     */
    useSkill(params = {}) {
        if (!this.isSkillReady()) return false;
        this.gauge = 0;
        return true;
    }

    /**
     * 화면 크기에 맞춰 슬롯 위치 초기화
     */
    resetPosition(canvasWidth, canvasHeight, totalSlots) {
        const spacing = canvasWidth / (totalSlots + 1);
        this.x = spacing * (this.slotIndex + 1);
        this.y = canvasHeight - 180;
        this.targetX = this.x;
        this.targetY = this.y;
        this.netTargetX = this.x;
        this.netTargetY = this.y;
    }

    /**
     * 기절 상태 여부 확인
     */
    isStunned() {
        return this.stunTimer > 0;
    }

    /**
     * 피격 대미지 처리 (무적 시간 판정 및 기절 트리거)
     */
    takeDamage(amount = 1) {
        if (this.invulnerableTimer > 0 || this.isStunned()) {
            return false;
        }

        this.hp = Math.max(0, this.hp - amount);
        this.invulnerableTimer = 1.0;

        if (this.hp <= 0) {
            this.stunTimer = 3.0;
            this.hp = this.maxHp;
        }

        return true;
    }

    /**
     * [IsLocalOwner - 로컬 기체 조작]
     * Client Prediction: 키보드/조이스틱 입력으로 즉시 이동 목표점 계산
     */
    handleHumanInput(keys, joystick, skillParams = null) {
        if (this.isStunned()) return;

        const isSpaceOrRightClick = keys['Space'] || keys['KeySpace'] || keys['RightClick'];
        if (isSpaceOrRightClick && skillParams) {
            keys['Space'] = false;
            keys['KeySpace'] = false;
            keys['RightClick'] = false;
            this.useSkill(skillParams);
        }

        let dx = 0;
        let dy = 0;

        if (keys['KeyW'] || keys['ArrowUp']) dy -= 1;
        if (keys['KeyS'] || keys['ArrowDown']) dy += 1;
        if (keys['KeyA'] || keys['ArrowLeft']) dx -= 1;
        if (keys['KeyD'] || keys['ArrowRight']) dx += 1;

        if (joystick && joystick.active) {
            dx = joystick.moveX;
            dy = joystick.moveY;
        }

        const len = Math.hypot(dx, dy);
        if (len > 0) {
            const factor = len > 1 ? len : 1;
            // deltaTime 연산을 위해 속도 벡터로 저장
            const normX = dx / factor;
            const normY = dy / factor;
            this.targetX = this.x + normX * this.moveSpeed * 0.1;
            this.targetY = this.y + normY * this.moveSpeed * 0.1;
        } else {
            this.targetX = this.x;
            this.targetY = this.y;
        }
    }

    /**
     * [RemoteProxy - 원격 기체 패킷 적용 & Dead Reckoning 설정]
     * @param {object} inputAction 릴레이 수신된 원격 패킷
     * @param {object} skillParams
     */
    handleHumanInputPacket(inputAction, skillParams = null) {
        if (this.isStunned() || !inputAction) return;

        if (typeof inputAction.mouseX === 'number' && typeof inputAction.mouseY === 'number') {
            this.lastMousePos = { x: inputAction.mouseX, y: inputAction.mouseY };
        }

        const moveX = inputAction.moveX !== undefined ? inputAction.moveX : inputAction.dx || 0;
        const moveY = inputAction.moveY !== undefined ? inputAction.moveY : inputAction.dy || 0;
        const len = Math.hypot(moveX, moveY);

        // 1. 송신지 실제 좌표가 포함되어 있는 경우 Dead Reckoning 목적지 설정
        if (typeof inputAction.posX === 'number' && typeof inputAction.posY === 'number') {
            const pingSec = Math.max(0.01, (inputAction.estimatedPing || 50) / 1000);
            
            // 상대방의 현재 속도 추정
            const speed = this.moveSpeed;
            const vx = len > 0 ? (moveX / len) * speed : 0;
            const vy = len > 0 ? (moveY / len) * speed : 0;

            this.netVelocityX = vx;
            this.netVelocityY = vy;

            // Ping 지연 시간만큼 미래의 예측 위치 계산 (Dead Reckoning)
            this.netTargetX = inputAction.posX + vx * pingSec;
            this.netTargetY = inputAction.posY + vy * pingSec;

            // 💡 [Hard Snap / Teleport Threshold]: 150px 이상 오차 시 강제 스냅
            const distFromCurrent = Math.hypot(this.x - inputAction.posX, this.y - inputAction.posY);
            if (distFromCurrent > this.HARD_SNAP_THRESHOLD) {
                this.x = inputAction.posX;
                this.y = inputAction.posY;
                this.targetX = inputAction.posX;
                this.targetY = inputAction.posY;
            } else {
                this.targetX = this.netTargetX;
                this.targetY = this.netTargetY;
            }
        } else {
            // 위치 좌표가 없을 경우 기존 방향 벡터 누적
            if (len > 0) {
                const factor = len > 1 ? len : 1;
                this.targetX = this.x + (moveX / factor) * this.moveSpeed * 0.1;
                this.targetY = this.y + (moveY / factor) * this.moveSpeed * 0.1;
            } else {
                this.targetX = this.x;
                this.targetY = this.y;
            }
        }

        // 3. 1회성 스킬 트리거 실행 (useSkill)
        if (inputAction.useSkill && skillParams) {
            this.useSkill(skillParams);
            inputAction.useSkill = false; // 1회성 소모
        }
    }

    /**
     * 프레임 업데이트 공통 처리 (DeltaTime Base 보간)
     */
    updateMovement(dt, canvasWidth, canvasHeight, enemyBullets = [], allyPlayers = []) {
        if (this.invulnerableTimer > 0) {
            this.invulnerableTimer = Math.max(0, this.invulnerableTimer - dt);
        }

        // 동적 스탯 수정자 업데이트
        this.updateModifiers(dt);

        // 델타룬 스치기 체크
        this.updateGraze(enemyBullets, dt);

        if (this.stunTimer > 0) {
            this.stunTimer = Math.max(0, this.stunTimer - dt);
            this.targetX = this.x;
            this.targetY = this.y;
            return;
        }

        // 💡 [DeltaTime Base & Dead Reckoning 미세 속도 보간]
        const dx = this.targetX - this.x;
        const dy = this.targetY - this.y;
        const dist = Math.hypot(dx, dy);

        if (dist > this.HARD_SNAP_THRESHOLD) {
            // 임계치 초과 시 즉시 Hard Snap
            this.x = this.targetX;
            this.y = this.targetY;
        } else if (dist > 1) {
            // 원격 기체(RemoteProxy)는 거리에 따라 미세 가속/감속 보정 (도착 시간 맞춤)
            let currentSpeed = this.moveSpeed;
            if (!this.isLocalOwner && this.isHuman) {
                // 오차가 크면 약간 가속(최대 1.5배), 거의 도착하면 감속
                const speedMultiplier = Math.min(1.8, Math.max(0.6, dist / 30));
                currentSpeed *= speedMultiplier;
            }

            const step = Math.min(dist, currentSpeed * dt);
            this.x += (dx / dist) * step;
            this.y += (dy / dist) * step;
        } else {
            this.x = this.targetX;
            this.y = this.targetY;
        }

        // 맵 경계 제한
        this.x = Math.max(this.radius, Math.min(canvasWidth - this.radius, this.x));
        this.y = Math.max(120, Math.min(canvasHeight - this.radius, this.y));
    }

    /**
     * 탄환 생성 및 사격 처리
     */
    shoot(bulletContainer, targetInfo) {
        if (this.isStunned()) return;

        let targetAngle = -Math.PI / 2;

        if (this.isHuman) {
            const mousePos = (targetInfo && targetInfo.mousePos) ? targetInfo.mousePos : { x: this.x, y: this.y - 100 };
            targetAngle = Math.atan2(mousePos.y - this.y, mousePos.x - this.x);
        } else {
            const boss = targetInfo ? targetInfo.boss : null;
            const enemyMinions = targetInfo ? (targetInfo.enemyMinions || []) : [];
            const allEnemies = [boss, ...enemyMinions].filter(e => e && !e.isDead);

            let closestEnemy = null;
            let minDist = Infinity;

            for (const enemy of allEnemies) {
                const dist = Math.hypot(enemy.x - this.x, enemy.y - this.y);
                if (dist < minDist) {
                    minDist = dist;
                    closestEnemy = enemy;
                }
            }

            if (closestEnemy) {
                targetAngle = Math.atan2(closestEnemy.y - this.y, closestEnemy.x - this.x);
            }
        }

        bulletContainer.push(new PlayerBullet(this.x, this.y, targetAngle, this.color, this));
    }

    updateAttack(onShoot) {
        if (this.isStunned()) return;

        const currentAttackSpeed = this.attackSpeed * (1 + this.getModifierValue('attackSpeed') / 100);
        this.attackCooldown += currentAttackSpeed;
        if (this.attackCooldown >= 60) {
            this.attackCooldown = 0;
            if (typeof onShoot === 'function') {
                onShoot();
            }
        }
    }

    draw(ctx, allyPlayers = []) {
        ctx.save();

        if (this.isStunned()) {
            ctx.globalAlpha = 0.4 + 0.3 * Math.sin(Date.now() * 0.01);
        }

        // Graze 연출
        if (this.grazeEffectTimer > 0) {
            ctx.save();
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.grazeRadius, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(255, 255, 255, ${this.grazeEffectTimer * 4})`;
            ctx.lineWidth = 1.5;
            ctx.setLineDash([4, 4]);
            ctx.stroke();
            ctx.restore();
        }

        // 본체 렌더링
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#ffffff';
        ctx.stroke();

        // 닉네임 / 소유자 표시
        ctx.font = '10px sans-serif';
        ctx.fillStyle = this.isLocalOwner ? '#22d3ee' : '#cbd5e1';
        ctx.textAlign = 'center';
        const label = this.isLocalOwner ? `[YOU] P${this.id}` : `P${this.id}`;
        ctx.fillText(label, this.x, this.y - this.radius - 6);

        ctx.restore();
    }
}
```

# 📄 [요청 2 ➡️ 불러온함수 (PlayerBullet 본체)] TARGET: extraction_target_project/js/player/playerBullet.js (6-70라인)
# ----------------------------------------------------------
```python
export class PlayerBullet {
    /**
     * @param {number} x 시작 X
     * @param {number} y 시작 Y
     * @param {number} angle 진행 각도 (라디안)
     * @param {number} slotIndex 발사한 플레이어의 슬롯 인덱스
     * @param {string} color 탄환 네온 색상
     */
    constructor(x, y, angle, slotIndex, color) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.speed = 14;
        this.radius = 4;
        this.slotIndex = slotIndex;
        this.color = color;
        this.baseDamage = 22;
        this.damage = 22;
        this.modifiers = [];
    }

    /**
     * 탄환 자체 스탯 수정자 파이프라인 산출
     */
    getModifiedDamage() {
        let finalDmg = this.damage;
        for (const m of this.modifiers) {
            if (m.targetStat === 'bulletDamage' && m.type === 'MULTIPLY') {
                finalDmg *= m.value;
            }
        }
        return Math.round(finalDmg);
    }

    /**
     * 탄환 위치 업데이트
     */
    update() {
        this.x += Math.cos(this.angle) * this.speed;
        this.y += Math.sin(this.angle) * this.speed;
    }

    /**
     * 탄환 렌더링
     * @param {CanvasRenderingContext2D} ctx 
     */
    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 8;
        ctx.fill();
    }

    /**
     * 화면 바깥으로 나갔는지 확인
     * @param {number} width 캔버스 너비
     * @param {number} height 캔버스 높이
     * @returns {boolean}
     */
    isOutOfBounds(width, height) {
        return (this.y < -10 || this.x < -10 || this.x > width + 10 || this.y > height + 10);
    }
}
```

# 📄 [요청 2 ➡️ 불러온함수 (BasePlayer 본체)] TARGET: extraction_target_project/js/player/basePlayer.js (15-462라인)
# ----------------------------------------------------------
```python
export default class BasePlayer {
    /**
     * @param {number} slotIndex 슬롯 인덱스 (0 ~ TOTAL_SLOTS - 1)
     * @param {string} classType 플레이어 직업 타입 ('bufferPlayer', 'defaultPlayer')
     */
    constructor(slotIndex, classType = 'defaultPlayer') {
        this.slotIndex = slotIndex;
        this.id = slotIndex + 1;
        this.color = SLOT_COLORS[slotIndex % SLOT_COLORS.length];
        this.isHuman = (slotIndex === 0);
        this.classType = classType;

        // 💡 [멀티플레이 권한 시스템]: 내가 직접 키보드/마우스로 조종하는 기체인지 여부 (IsLocalOwner)
        this.isLocalOwner = false;

        // 💡 [Dead Reckoning & 원격 상태 수신 변수]
        this.remoteInputPacket = null;
        this.lastReceivedSeq = 0;
        this.netTargetX = 0;
        this.netTargetY = 0;
        this.netVelocityX = 0;
        this.netVelocityY = 0;
        this.netEstimatedPing = 50; // ms

        // Hard Snap 임계값 (예측 오차가 이 값을 초과하면 즉시 강제 이동)
        this.HARD_SNAP_THRESHOLD = 150;

        // --- 공통 메타 속성 (하위 캐릭터 파일에서 오버라이드) ---
        this.className = '기본 기체';
        this.themeColor = '#06b6d4';
        this.hasActiveSkill = false;
        this.skillIconClass = 'fa-solid fa-bolt';
        this.skillName = 'SKILL';
        this.skillFloatText = 'SKILL ACTIVATED!';

        this.radius = 8;
        this.moveSpeed = 300; // px/sec 기준 (기본)
        this.speed = 5.2;

        // 체력 및 기절 시스템
        this.maxHp = 5;
        this.hp = 5;
        this.stunTimer = 0.0;

        // 위치 및 목표 좌표
        this.x = 0;
        this.y = 0;
        this.targetX = 0;
        this.targetY = 0;

        // 통계 및 상태값
        this.damageDealt = 0;
        this.kills = 0;
        this.mistakesCount = 0;
        this.attackCooldown = 0;
        this.attackSpeed = 8;
        this.invulnerableTimer = 0.0;

        // 델타룬 Graze 게이지
        this.gauge = 0;             
        this.maxGauge = 100;
        this.grazeRadius = 45;   
        this.grazeCheckTimer = 0.0; 
        this.grazeEffectTimer = 0;  

        // 동적 스탯 수정자 파이프라인
        this.modifiers = [];     

        // AI FSM 필드
        this.fsmState = 'IDLE';
        this.actionLockTimer = 0.0;
        this.dodgeFatigue = 0.0;
        this.lastMistakeType = 'NONE';
    }

    /**
     * 동적 스탯 수정자(Modifier) 추가
     */
    addModifier(mod) {
        if (!mod || !mod.key) return;
        this.removeModifier(mod.key);
        this.modifiers.push({
            key: mod.key,
            type: mod.type || 'buff',
            stat: mod.stat || 'all',
            value: mod.value || 0,
            duration: mod.duration || 1.0,
            elapsed: 0
        });
    }

    removeModifier(key) {
        this.modifiers = this.modifiers.filter(m => m.key !== key);
    }

    getModifierValue(stat) {
        let total = 0;
        for (const mod of this.modifiers) {
            if (mod.stat === stat || mod.stat === 'all') {
                total += mod.value;
            }
        }
        return total;
    }

    updateModifiers(dt) {
        for (let i = this.modifiers.length - 1; i >= 0; i--) {
            const mod = this.modifiers[i];
            mod.elapsed += dt;
            if (mod.elapsed >= mod.duration) {
                this.modifiers.splice(i, 1);
            }
        }
    }

    /**
     * 델타룬 Graze 판정
     */
    updateGraze(enemyBullets, dt) {
        if (!enemyBullets || enemyBullets.length === 0) return;

        if (this.grazeEffectTimer > 0) {
            this.grazeEffectTimer = Math.max(0, this.grazeEffectTimer - dt);
        }

        for (const b of enemyBullets) {
            if (!b || b.isDead) continue;

            if (!b.grazedSlots) {
                b.grazedSlots = [];
            }

            if (b.grazedSlots.includes(this.slotIndex)) continue;

            const dist = Math.hypot(b.x - this.x, b.y - this.y);

            if (dist > this.radius && dist <= this.grazeRadius) {
                b.grazedSlots.push(this.slotIndex);
                this.gauge = Math.min(this.maxGauge, this.gauge + 1);
                this.grazeEffectTimer = 0.2;
            }
        }
    }

    /**
     * 클래스별 개별 maxGauge 기준 100% 충전 여부 판단
     */
    isSkillReady() {
        const isStun = typeof this.isStunned === 'function' ? this.isStunned() : false;
        const targetMax = this.maxGauge || 100;
        const currentGauge = this.gauge || 0;

        if (isStun) return false;
        if (currentGauge < targetMax) return false;

        return true;
    }

    /**
     * 기본 스킬 시전 검사 및 게이지 초기화
     */
    useSkill(params = {}) {
        if (!this.isSkillReady()) return false;
        this.gauge = 0;
        return true;
    }

    /**
     * 화면 크기에 맞춰 슬롯 위치 초기화
     */
    resetPosition(canvasWidth, canvasHeight, totalSlots) {
        const spacing = canvasWidth / (totalSlots + 1);
        this.x = spacing * (this.slotIndex + 1);
        this.y = canvasHeight - 180;
        this.targetX = this.x;
        this.targetY = this.y;
        this.netTargetX = this.x;
        this.netTargetY = this.y;
    }

    /**
     * 기절 상태 여부 확인
     */
    isStunned() {
        return this.stunTimer > 0;
    }

    /**
     * 피격 대미지 처리 (무적 시간 판정 및 기절 트리거)
     */
    takeDamage(amount = 1) {
        if (this.invulnerableTimer > 0 || this.isStunned()) {
            return false;
        }

        this.hp = Math.max(0, this.hp - amount);
        this.invulnerableTimer = 1.0;

        if (this.hp <= 0) {
            this.stunTimer = 3.0;
            this.hp = this.maxHp;
        }

        return true;
    }

    /**
     * [IsLocalOwner - 로컬 기체 조작]
     * Client Prediction: 키보드/조이스틱 입력으로 즉시 이동 목표점 계산
     */
    handleHumanInput(keys, joystick, skillParams = null) {
        if (this.isStunned()) return;

        const isSpaceOrRightClick = keys['Space'] || keys['KeySpace'] || keys['RightClick'];
        if (isSpaceOrRightClick && skillParams) {
            keys['Space'] = false;
            keys['KeySpace'] = false;
            keys['RightClick'] = false;
            this.useSkill(skillParams);
        }

        let dx = 0;
        let dy = 0;

        if (keys['KeyW'] || keys['ArrowUp']) dy -= 1;
        if (keys['KeyS'] || keys['ArrowDown']) dy += 1;
        if (keys['KeyA'] || keys['ArrowLeft']) dx -= 1;
        if (keys['KeyD'] || keys['ArrowRight']) dx += 1;

        if (joystick && joystick.active) {
            dx = joystick.moveX;
            dy = joystick.moveY;
        }

        const len = Math.hypot(dx, dy);
        if (len > 0) {
            const factor = len > 1 ? len : 1;
            // deltaTime 연산을 위해 속도 벡터로 저장
            const normX = dx / factor;
            const normY = dy / factor;
            this.targetX = this.x + normX * this.moveSpeed * 0.1;
            this.targetY = this.y + normY * this.moveSpeed * 0.1;
        } else {
            this.targetX = this.x;
            this.targetY = this.y;
        }
    }

    /**
     * [RemoteProxy - 원격 기체 패킷 적용 & Dead Reckoning 설정]
     * @param {object} inputAction 릴레이 수신된 원격 패킷
     * @param {object} skillParams
     */
    handleHumanInputPacket(inputAction, skillParams = null) {
        if (this.isStunned() || !inputAction) return;

        if (typeof inputAction.mouseX === 'number' && typeof inputAction.mouseY === 'number') {
            this.lastMousePos = { x: inputAction.mouseX, y: inputAction.mouseY };
        }

        const moveX = inputAction.moveX !== undefined ? inputAction.moveX : inputAction.dx || 0;
        const moveY = inputAction.moveY !== undefined ? inputAction.moveY : inputAction.dy || 0;
        const len = Math.hypot(moveX, moveY);

        // 1. 송신지 실제 좌표가 포함되어 있는 경우 Dead Reckoning 목적지 설정
        if (typeof inputAction.posX === 'number' && typeof inputAction.posY === 'number') {
            const pingSec = Math.max(0.01, (inputAction.estimatedPing || 50) / 1000);
            
            // 상대방의 현재 속도 추정
            const speed = this.moveSpeed;
            const vx = len > 0 ? (moveX / len) * speed : 0;
            const vy = len > 0 ? (moveY / len) * speed : 0;

            this.netVelocityX = vx;
            this.netVelocityY = vy;

            // Ping 지연 시간만큼 미래의 예측 위치 계산 (Dead Reckoning)
            this.netTargetX = inputAction.posX + vx * pingSec;
            this.netTargetY = inputAction.posY + vy * pingSec;

            // 💡 [Hard Snap / Teleport Threshold]: 150px 이상 오차 시 강제 스냅
            const distFromCurrent = Math.hypot(this.x - inputAction.posX, this.y - inputAction.posY);
            if (distFromCurrent > this.HARD_SNAP_THRESHOLD) {
                this.x = inputAction.posX;
                this.y = inputAction.posY;
                this.targetX = inputAction.posX;
                this.targetY = inputAction.posY;
            } else {
                this.targetX = this.netTargetX;
                this.targetY = this.netTargetY;
            }
        } else {
            // 위치 좌표가 없을 경우 기존 방향 벡터 누적
            if (len > 0) {
                const factor = len > 1 ? len : 1;
                this.targetX = this.x + (moveX / factor) * this.moveSpeed * 0.1;
                this.targetY = this.y + (moveY / factor) * this.moveSpeed * 0.1;
            } else {
                this.targetX = this.x;
                this.targetY = this.y;
            }
        }

        // 3. 1회성 스킬 트리거 실행 (useSkill)
        if (inputAction.useSkill && skillParams) {
            this.useSkill(skillParams);
            inputAction.useSkill = false; // 1회성 소모
        }
    }

    /**
     * 프레임 업데이트 공통 처리 (DeltaTime Base 보간)
     */
    updateMovement(dt, canvasWidth, canvasHeight, enemyBullets = [], allyPlayers = []) {
        if (this.invulnerableTimer > 0) {
            this.invulnerableTimer = Math.max(0, this.invulnerableTimer - dt);
        }

        // 동적 스탯 수정자 업데이트
        this.updateModifiers(dt);

        // 델타룬 스치기 체크
        this.updateGraze(enemyBullets, dt);

        if (this.stunTimer > 0) {
            this.stunTimer = Math.max(0, this.stunTimer - dt);
            this.targetX = this.x;
            this.targetY = this.y;
            return;
        }

        // 💡 [DeltaTime Base & Dead Reckoning 미세 속도 보간]
        const dx = this.targetX - this.x;
        const dy = this.targetY - this.y;
        const dist = Math.hypot(dx, dy);

        if (dist > this.HARD_SNAP_THRESHOLD) {
            // 임계치 초과 시 즉시 Hard Snap
            this.x = this.targetX;
            this.y = this.targetY;
        } else if (dist > 1) {
            // 원격 기체(RemoteProxy)는 거리에 따라 미세 가속/감속 보정 (도착 시간 맞춤)
            let currentSpeed = this.moveSpeed;
            if (!this.isLocalOwner && this.isHuman) {
                // 오차가 크면 약간 가속(최대 1.5배), 거의 도착하면 감속
                const speedMultiplier = Math.min(1.8, Math.max(0.6, dist / 30));
                currentSpeed *= speedMultiplier;
            }

            const step = Math.min(dist, currentSpeed * dt);
            this.x += (dx / dist) * step;
            this.y += (dy / dist) * step;
        } else {
            this.x = this.targetX;
            this.y = this.targetY;
        }

        // 맵 경계 제한
        this.x = Math.max(this.radius, Math.min(canvasWidth - this.radius, this.x));
        this.y = Math.max(120, Math.min(canvasHeight - this.radius, this.y));
    }

    /**
     * 탄환 생성 및 사격 처리
     */
    shoot(bulletContainer, targetInfo) {
        if (this.isStunned()) return;

        let targetAngle = -Math.PI / 2;

        if (this.isHuman) {
            const mousePos = (targetInfo && targetInfo.mousePos) ? targetInfo.mousePos : { x: this.x, y: this.y - 100 };
            targetAngle = Math.atan2(mousePos.y - this.y, mousePos.x - this.x);
        } else {
            const boss = targetInfo ? targetInfo.boss : null;
            const enemyMinions = targetInfo ? (targetInfo.enemyMinions || []) : [];
            const allEnemies = [boss, ...enemyMinions].filter(e => e && !e.isDead);

            let closestEnemy = null;
            let minDist = Infinity;

            for (const enemy of allEnemies) {
                const dist = Math.hypot(enemy.x - this.x, enemy.y - this.y);
                if (dist < minDist) {
                    minDist = dist;
                    closestEnemy = enemy;
                }
            }

            if (closestEnemy) {
                targetAngle = Math.atan2(closestEnemy.y - this.y, closestEnemy.x - this.x);
            }
        }

        bulletContainer.push(new PlayerBullet(this.x, this.y, targetAngle, this.color, this));
    }

    updateAttack(onShoot) {
        if (this.isStunned()) return;

        const currentAttackSpeed = this.attackSpeed * (1 + this.getModifierValue('attackSpeed') / 100);
        this.attackCooldown += currentAttackSpeed;
        if (this.attackCooldown >= 60) {
            this.attackCooldown = 0;
            if (typeof onShoot === 'function') {
                onShoot();
            }
        }
    }

    draw(ctx, allyPlayers = []) {
        ctx.save();

        if (this.isStunned()) {
            ctx.globalAlpha = 0.4 + 0.3 * Math.sin(Date.now() * 0.01);
        }

        // Graze 연출
        if (this.grazeEffectTimer > 0) {
            ctx.save();
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.grazeRadius, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(255, 255, 255, ${this.grazeEffectTimer * 4})`;
            ctx.lineWidth = 1.5;
            ctx.setLineDash([4, 4]);
            ctx.stroke();
            ctx.restore();
        }

        // 본체 렌더링
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#ffffff';
        ctx.stroke();

        // 닉네임 / 소유자 표시
        ctx.font = '10px sans-serif';
        ctx.fillStyle = this.isLocalOwner ? '#22d3ee' : '#cbd5e1';
        ctx.textAlign = 'center';
        const label = this.isLocalOwner ? `[YOU] P${this.id}` : `P${this.id}`;
        ctx.fillText(label, this.x, this.y - this.radius - 6);

        ctx.restore();
    }
}
```

# 📄 [요청 3] TARGET: js/core/input.js (12-268라인)
# ----------------------------------------------------------
```python
export class InputHandler {
    constructor() {
        this.keys = {};
        this.mousePos = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
        this.joystick = {
            active: false,
            startX: 0,
            startY: 0,
            moveX: 0,
            moveY: 0
        };

        // 스킬 전용 1회성 트리거 큐 플래그
        this.skillTriggered = false;
        this.lastSkillTriggerTime = 0;

        // AI 자율 주행 모드 여부
        this.isAiMode = false;

        this.initKeyboard();
        this.initMouse();
        this.initJoystick();
    }

    /**
     * Lazy Evaluation 헬퍼: 현재 유효한 networkManager 인스턴스 실시간 탐색
     * @returns {import('../network/networkManager.js').NetworkManager|null}
     */
    getNetworkManager() {
        return this.networkManager || window.networkManager || null;
    }

    /**
     * AI 모드 토글 및 설정
     * @param {boolean} [enable] 
     */
    setAiMode(enable) {
        if (typeof enable === 'boolean') {
            this.isAiMode = enable;
        } else {
            this.isAiMode = !this.isAiMode;
        }
        console.log(`🤖 [InputHandler] AI 모드 상태: ${this.isAiMode ? 'ON (AUTO)' : 'OFF (MANUAL)'}`);
        return this.isAiMode;
    }

    /**
     * 키보드 이벤트 리스너 등록
     */
    initKeyboard() {
        window.addEventListener('keydown', (e) => {
            if (!this.keys[e.code]) {
                if (e.code === 'Space' || e.key === ' ' || e.keyCode === 32) {
                    this.skillTriggered = true;
                    this.lastSkillTriggerTime = Date.now();
                    e.preventDefault();
                }
                // 💡 [Lazy Evaluation]: this.networkManager || window.networkManager 실시간 탐색
                const net = this.getNetworkManager();
                console.log(`[LOCAL KEY LOG] Key Down: ${e.code}`);
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('KEYBOARD', `Key Down: ${e.code}`);
                }
            }
            this.keys[e.code] = true;
        });

        window.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
    }

    /**
     * 마우스 리스너 등록 (UI 버튼과 캔버스 좌클릭 구별)
     */
    initMouse() {
        window.addEventListener('mousemove', (e) => {
            this.mousePos.x = e.clientX;
            this.mousePos.y = e.clientY;
        });

        window.addEventListener('mousedown', (e) => {
            // 💡 [Lazy Evaluation]
            const net = this.getNetworkManager();

            if (e.button === 2) {
                this.skillTriggered = true;
                this.lastSkillTriggerTime = Date.now();
                console.log('[LOCAL MOUSE LOG] Right Click (Skill Trigger)');
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('MOUSE', 'Right Click (Skill Trigger)');
                }
            } else if (e.button === 0) {
                // UI 버튼 요소와 캔버스 구분
                const target = e.target;
                const isButton = target && (target.tagName === 'BUTTON' || target.closest('button'));
                const clickType = isButton ? `UI Button Click [${target.id || target.innerText || 'BTN'}]` : `Canvas Field Click (X:${e.clientX}, Y:${e.clientY})`;

                console.log(`[LOCAL MOUSE LOG] ${clickType}`);
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('MOUSE_LEFT', clickType);
                }
            }
        });

        window.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
    }

    /**
     * 모바일 터치 조이스틱 인터랙션 초기화
     */
    initJoystick() {
        const joystickZone = document.getElementById('joystickZone');
        const joystickKnob = document.getElementById('joystickKnob');

        if (!joystickZone || !joystickKnob) return;

        joystickZone.addEventListener('touchstart', (e) => {
            this.joystick.active = true;
            const touch = e.touches[0];
            const rect = joystickZone.getBoundingClientRect();
            this.joystick.startX = rect.left + rect.width / 2;
            this.joystick.startY = rect.top + rect.height / 2;
            e.preventDefault();
        }, { passive: false });

        window.addEventListener('touchmove', (e) => {
            if (!this.joystick.active) return;
            const touch = e.touches[0];
            const dx = touch.clientX - this.joystick.startX;
            const dy = touch.clientY - this.joystick.startY;
            const dist = Math.hypot(dx, dy);
            const maxDist = 35;

            const angle = Math.atan2(dy, dx);
            const intensity = Math.min(dist, maxDist);

            this.joystick.moveX = Math.cos(angle) * (intensity / maxDist);
            this.joystick.moveY = Math.sin(angle) * (intensity / maxDist);

            const knobX = Math.cos(angle) * intensity;
            const knobY = Math.sin(angle) * intensity;
            joystickKnob.style.transform = `translate(${knobX}px, ${knobY}px)`;
        }, { passive: true });

        const endTouch = () => {
            this.joystick.active = false;
            this.joystick.moveX = 0;
            this.joystick.moveY = 0;
            joystickKnob.style.transform = `translate(0px, 0px)`;
        };

        window.addEventListener('touchend', endTouch);
        window.addEventListener('touchcancel', endTouch);
    }

    /**
     * playerAiSpread 독립 시드 기반 결정론적 AI 입력 액션 생성
     */
    getAiInputAction(slotIndex = 0, context = null) {
        let moveX = 0;
        let moveY = 0;
        let mouseX = this.mousePos.x;
        let mouseY = this.mousePos.y;
        let useSkill = false;

        const player = (context && context.player) || 
            (window.gameLoopInstance && window.gameLoopInstance.slots && window.gameLoopInstance.slots[slotIndex]);

        if (player) {
            const dx = (player.targetX || player.x) - player.x;
            const dy = (player.targetY || player.y) - player.y;
            const dist = Math.hypot(dx, dy);

            if (dist > 5) {
                const spreadAngle = (rngPlayerAi.getSpread(slotIndex) - 0.5) * 0.1;
                const baseAngle = Math.atan2(dy, dx) + spreadAngle;
                moveX = Math.cos(baseAngle);
                moveY = Math.sin(baseAngle);
            }

            const boss = (context && context.boss) || (window.gameLoopInstance && window.gameLoopInstance.boss);
            if (boss) {
                const aimSpread = (rngPlayerAi.getSpread(slotIndex) - 0.5) * 20;
                mouseX = boss.x + aimSpread;
                mouseY = boss.y + aimSpread;
            }

            if (player.dodgeFatigue > 0.8 && player.hasActiveSkill && !player.isSkillOnCooldown) {
                useSkill = rngPlayerAi.getSpread(slotIndex) < 0.3;
            }
        }

        return {
            moveX,
            moveY,
            dx: moveX,
            dy: moveY,
            mouseX,
            mouseY,
            useSkill,
            timeStamp: Date.now()
        };
    }

    /**
     * 현재 프레임의 클라이언트 조작 상태 패킷 추출 (Continuous Movement & Trigger Action)
     */
    getInputAction(slotIndex = 0, context = null) {
        if (this.isAiMode) {
            return this.getAiInputAction(slotIndex, context);
        }

        let moveX = 0;
        let moveY = 0;

        if (this.keys['KeyW'] || this.keys['ArrowUp']) moveY -= 1;
        if (this.keys['KeyS'] || this.keys['ArrowDown']) moveY += 1;
        if (this.keys['KeyA'] || this.keys['ArrowLeft']) moveX -= 1;
        if (this.keys['KeyD'] || this.keys['ArrowRight']) moveX += 1;

        // 대각선 이동 정규화
        const len = Math.hypot(moveX, moveY);
        if (len > 0) {
            moveX /= len;
            moveY /= len;
        }

        if (this.joystick && this.joystick.active) {
            moveX = this.joystick.moveX;
            moveY = this.joystick.moveY;
        }

        const useSkill = this.skillTriggered;
        const skillTime = this.lastSkillTriggerTime || Date.now();
        this.skillTriggered = false;

        const myPlayer = (context && context.player) || 
            (window.gameLoopInstance && window.gameLoopInstance.slots && window.gameLoopInstance.slots[slotIndex]);

        return {
            moveX,
            moveY,
            dx: moveX,
            dy: moveY,
            mouseX: this.mousePos.x,
            mouseY: this.mousePos.y,
            useSkill,
            timeStamp: skillTime,
            posX: myPlayer ? myPlayer.x : undefined,
            posY: myPlayer ? myPlayer.y : undefined,
            speed: myPlayer ? myPlayer.speed : undefined
        };
    }
}
```

# 📄 [요청 3 ➡️ 불러온함수 (InputHandler 본체)] TARGET: extraction_target_project/js/core/input.js (12-268라인)
# ----------------------------------------------------------
```python
export class InputHandler {
    constructor() {
        this.keys = {};
        this.mousePos = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
        this.joystick = {
            active: false,
            startX: 0,
            startY: 0,
            moveX: 0,
            moveY: 0
        };

        // 스킬 전용 1회성 트리거 큐 플래그
        this.skillTriggered = false;
        this.lastSkillTriggerTime = 0;

        // AI 자율 주행 모드 여부
        this.isAiMode = false;

        this.initKeyboard();
        this.initMouse();
        this.initJoystick();
    }

    /**
     * Lazy Evaluation 헬퍼: 현재 유효한 networkManager 인스턴스 실시간 탐색
     * @returns {import('../network/networkManager.js').NetworkManager|null}
     */
    getNetworkManager() {
        return this.networkManager || window.networkManager || null;
    }

    /**
     * AI 모드 토글 및 설정
     * @param {boolean} [enable] 
     */
    setAiMode(enable) {
        if (typeof enable === 'boolean') {
            this.isAiMode = enable;
        } else {
            this.isAiMode = !this.isAiMode;
        }
        console.log(`🤖 [InputHandler] AI 모드 상태: ${this.isAiMode ? 'ON (AUTO)' : 'OFF (MANUAL)'}`);
        return this.isAiMode;
    }

    /**
     * 키보드 이벤트 리스너 등록
     */
    initKeyboard() {
        window.addEventListener('keydown', (e) => {
            if (!this.keys[e.code]) {
                if (e.code === 'Space' || e.key === ' ' || e.keyCode === 32) {
                    this.skillTriggered = true;
                    this.lastSkillTriggerTime = Date.now();
                    e.preventDefault();
                }
                // 💡 [Lazy Evaluation]: this.networkManager || window.networkManager 실시간 탐색
                const net = this.getNetworkManager();
                console.log(`[LOCAL KEY LOG] Key Down: ${e.code}`);
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('KEYBOARD', `Key Down: ${e.code}`);
                }
            }
            this.keys[e.code] = true;
        });

        window.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
    }

    /**
     * 마우스 리스너 등록 (UI 버튼과 캔버스 좌클릭 구별)
     */
    initMouse() {
        window.addEventListener('mousemove', (e) => {
            this.mousePos.x = e.clientX;
            this.mousePos.y = e.clientY;
        });

        window.addEventListener('mousedown', (e) => {
            // 💡 [Lazy Evaluation]
            const net = this.getNetworkManager();

            if (e.button === 2) {
                this.skillTriggered = true;
                this.lastSkillTriggerTime = Date.now();
                console.log('[LOCAL MOUSE LOG] Right Click (Skill Trigger)');
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('MOUSE', 'Right Click (Skill Trigger)');
                }
            } else if (e.button === 0) {
                // UI 버튼 요소와 캔버스 구분
                const target = e.target;
                const isButton = target && (target.tagName === 'BUTTON' || target.closest('button'));
                const clickType = isButton ? `UI Button Click [${target.id || target.innerText || 'BTN'}]` : `Canvas Field Click (X:${e.clientX}, Y:${e.clientY})`;

                console.log(`[LOCAL MOUSE LOG] ${clickType}`);
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('MOUSE_LEFT', clickType);
                }
            }
        });

        window.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
    }

    /**
     * 모바일 터치 조이스틱 인터랙션 초기화
     */
    initJoystick() {
        const joystickZone = document.getElementById('joystickZone');
        const joystickKnob = document.getElementById('joystickKnob');

        if (!joystickZone || !joystickKnob) return;

        joystickZone.addEventListener('touchstart', (e) => {
            this.joystick.active = true;
            const touch = e.touches[0];
            const rect = joystickZone.getBoundingClientRect();
            this.joystick.startX = rect.left + rect.width / 2;
            this.joystick.startY = rect.top + rect.height / 2;
            e.preventDefault();
        }, { passive: false });

        window.addEventListener('touchmove', (e) => {
            if (!this.joystick.active) return;
            const touch = e.touches[0];
            const dx = touch.clientX - this.joystick.startX;
            const dy = touch.clientY - this.joystick.startY;
            const dist = Math.hypot(dx, dy);
            const maxDist = 35;

            const angle = Math.atan2(dy, dx);
            const intensity = Math.min(dist, maxDist);

            this.joystick.moveX = Math.cos(angle) * (intensity / maxDist);
            this.joystick.moveY = Math.sin(angle) * (intensity / maxDist);

            const knobX = Math.cos(angle) * intensity;
            const knobY = Math.sin(angle) * intensity;
            joystickKnob.style.transform = `translate(${knobX}px, ${knobY}px)`;
        }, { passive: true });

        const endTouch = () => {
            this.joystick.active = false;
            this.joystick.moveX = 0;
            this.joystick.moveY = 0;
            joystickKnob.style.transform = `translate(0px, 0px)`;
        };

        window.addEventListener('touchend', endTouch);
        window.addEventListener('touchcancel', endTouch);
    }

    /**
     * playerAiSpread 독립 시드 기반 결정론적 AI 입력 액션 생성
     */
    getAiInputAction(slotIndex = 0, context = null) {
        let moveX = 0;
        let moveY = 0;
        let mouseX = this.mousePos.x;
        let mouseY = this.mousePos.y;
        let useSkill = false;

        const player = (context && context.player) || 
            (window.gameLoopInstance && window.gameLoopInstance.slots && window.gameLoopInstance.slots[slotIndex]);

        if (player) {
            const dx = (player.targetX || player.x) - player.x;
            const dy = (player.targetY || player.y) - player.y;
            const dist = Math.hypot(dx, dy);

            if (dist > 5) {
                const spreadAngle = (rngPlayerAi.getSpread(slotIndex) - 0.5) * 0.1;
                const baseAngle = Math.atan2(dy, dx) + spreadAngle;
                moveX = Math.cos(baseAngle);
                moveY = Math.sin(baseAngle);
            }

            const boss = (context && context.boss) || (window.gameLoopInstance && window.gameLoopInstance.boss);
            if (boss) {
                const aimSpread = (rngPlayerAi.getSpread(slotIndex) - 0.5) * 20;
                mouseX = boss.x + aimSpread;
                mouseY = boss.y + aimSpread;
            }

            if (player.dodgeFatigue > 0.8 && player.hasActiveSkill && !player.isSkillOnCooldown) {
                useSkill = rngPlayerAi.getSpread(slotIndex) < 0.3;
            }
        }

        return {
            moveX,
            moveY,
            dx: moveX,
            dy: moveY,
            mouseX,
            mouseY,
            useSkill,
            timeStamp: Date.now()
        };
    }

    /**
     * 현재 프레임의 클라이언트 조작 상태 패킷 추출 (Continuous Movement & Trigger Action)
     */
    getInputAction(slotIndex = 0, context = null) {
        if (this.isAiMode) {
            return this.getAiInputAction(slotIndex, context);
        }

        let moveX = 0;
        let moveY = 0;

        if (this.keys['KeyW'] || this.keys['ArrowUp']) moveY -= 1;
        if (this.keys['KeyS'] || this.keys['ArrowDown']) moveY += 1;
        if (this.keys['KeyA'] || this.keys['ArrowLeft']) moveX -= 1;
        if (this.keys['KeyD'] || this.keys['ArrowRight']) moveX += 1;

        // 대각선 이동 정규화
        const len = Math.hypot(moveX, moveY);
        if (len > 0) {
            moveX /= len;
            moveY /= len;
        }

        if (this.joystick && this.joystick.active) {
            moveX = this.joystick.moveX;
            moveY = this.joystick.moveY;
        }

        const useSkill = this.skillTriggered;
        const skillTime = this.lastSkillTriggerTime || Date.now();
        this.skillTriggered = false;

        const myPlayer = (context && context.player) || 
            (window.gameLoopInstance && window.gameLoopInstance.slots && window.gameLoopInstance.slots[slotIndex]);

        return {
            moveX,
            moveY,
            dx: moveX,
            dy: moveY,
            mouseX: this.mousePos.x,
            mouseY: this.mousePos.y,
            useSkill,
            timeStamp: skillTime,
            posX: myPlayer ? myPlayer.x : undefined,
            posY: myPlayer ? myPlayer.y : undefined,
            speed: myPlayer ? myPlayer.speed : undefined
        };
    }
}
```

# 📄 [요청 4] TARGET: js/core/gameLoop.js (14-23라인)
# ----------------------------------------------------------
```python
export class GameLoop {
    /**
     * @param {HTMLCanvasElement} canvas 
     * @param {CanvasRenderingContext2D} ctx 
     * @param {import('./sceneManager.js').SceneManager} sceneManager 
     * @param {import('./input.js').InputHandler} input 
     * @param {import('./ui.js').UIManager} ui 
     */
```

# 📄 [요청 4 ➡️ 불러온함수 (GameLoop 본체)] TARGET: extraction_target_project/js/core/gameLoop.js (14-23라인)
# ----------------------------------------------------------
```python
export class GameLoop {
    /**
     * @param {HTMLCanvasElement} canvas 
     * @param {CanvasRenderingContext2D} ctx 
     * @param {import('./sceneManager.js').SceneManager} sceneManager 
     * @param {import('./input.js').InputHandler} input 
     * @param {import('./ui.js').UIManager} ui 
     */
```

# 📄 [요청 5] TARGET: js/core/ui.js (248-278라인)
# ----------------------------------------------------------
```python
        const triggerSkill = () => {
            const userPlayer = typeof getUserPlayerFn === 'function' ? getUserPlayerFn() : null;
            if (!userPlayer || typeof userPlayer.useSkill !== 'function') return;

            const allEnemyBullets = [
                ...(gameLoopInstance.bossBullets || []),
                ...(gameLoopInstance.minionBullets || [])
            ];

            const success = userPlayer.useSkill({
                boss: gameLoopInstance.boss,
                enemyMinions: gameLoopInstance.enemyMinions,
                bossBullets: gameLoopInstance.bossBullets,
                minionBullets: gameLoopInstance.minionBullets,
                enemyBullets: allEnemyBullets,
                allyMinions: gameLoopInstance.allyMinions,
                allyPlayers: gameLoopInstance.slots
            });

            if (success && Array.isArray(gameLoopInstance.floatingTexts)) {
                gameLoopInstance.floatingTexts.push({
                    x: userPlayer.x,
                    y: userPlayer.y - 20,
                    text: userPlayer.skillFloatText || 'SKILL ACTIVATED!',
                    color: userPlayer.themeColor || '#10b981',
                    alpha: 1.0,
                    vy: -1.5,
                    life: 1.0
                });
            }
        };
```

# 📄 [요청 6] TARGET: server.js (92-119라인)
# ----------------------------------------------------------
```python
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
```

# 📄 [요청 6 ➡️ 불러온함수 (broadcast 본체)] TARGET: extraction_target_project/server.js (80-87라인)
# ----------------------------------------------------------
```python
function broadcast(payloadObj) {
    const jsonStr = JSON.stringify(payloadObj);
    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(jsonStr);
        }
    });
}
```

# 📄 [요청 6 ➡️ 불러온함수 (broadcastRoomState 본체)] TARGET: extraction_target_project/server.js (92-119라인)
# ----------------------------------------------------------
```python
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
```

# 📄 [요청 7] TARGET: js/player/characters/shielderPlayer.js (11-238라인)
# ----------------------------------------------------------
```python
export class ShielderPlayer extends BasePlayer {
    constructor(slotIndex) {
        super(slotIndex, 'shielderPlayer');

        // --- 쉴더 전용 메타 설정 ---
        this.className = '쉴더 (Shielder)';
        this.themeColor = '#3b82f6';                // 파란색 테마
        this.hasActiveSkill = true;
        this.skillIconClass = 'fa-solid fa-shield-halved';
        this.skillName = 'SHIELD';
        this.skillFloatText = 'BARRIER DEPLOYED!';

        this.maxGauge = 70;                         // 스킬 게이지 70
        this.activeShield = null;                   // 현재 설치된 배리어 정보
    }

    /**
     * 쉴더 전용 스킬 시전 (방어막 설치)
     * @param {object} targetInfo 마우스/조작 입력 및 보스 정보
     */
    useSkill(targetInfo = {}) {
        if (!super.useSkill(targetInfo)) return false;

        let deployAngle = -Math.PI / 2; // 기본 방향: 위쪽

        if (this.isHuman) {
            const keys = targetInfo.keys || {};
            let dx = 0;
            let dy = 0;

            if (keys['KeyW'] || keys['ArrowUp']) dy -= 1;
            if (keys['KeyS'] || keys['ArrowDown']) dy += 1;
            if (keys['KeyA'] || keys['ArrowLeft']) dx -= 1;
            if (keys['KeyD'] || keys['ArrowRight']) dx += 1;

            if (dx !== 0 || dy !== 0) {
                deployAngle = Math.atan2(dy, dx);
            } else {
                const mousePos = targetInfo.mousePos;
                if (mousePos) {
                    deployAngle = Math.atan2(mousePos.y - this.y, mousePos.x - this.x);
                }
            }
        } else {
            const boss = targetInfo.boss;
            const enemyMinions = targetInfo.enemyMinions || [];
            const allEnemies = [boss, ...enemyMinions].filter(e => e && !e.isDead);

            let closest = null;
            let minDist = Infinity;
            for (const enemy of allEnemies) {
                const d = Math.hypot(enemy.x - this.x, enemy.y - this.y);
                if (d < minDist) {
                    minDist = d;
                    closest = enemy;
                }
            }

            if (closest) {
                deployAngle = Math.atan2(closest.y - this.y, closest.x - this.x);
            }
        }

        // 곡선 배리어 생성 (체력 100, 반지름 70px, 90도 호)
        this.activeShield = {
            id: `shield_${this.slotIndex}_${Date.now()}`,
            x: this.x,
            y: this.y,
            angle: deployAngle,
            radius: 70,
            arcAngle: Math.PI / 2,
            hp: 100,
            maxHp: 100,
            thickness: 12,
            duration: 20.0
        };

        // 소유자(Owner)인 경우 전체 기기에 방벽 생성 브로드캐스트
        if (this.isLocalOwner && window.networkManager) {
            window.networkManager.sendObjectStateSync(this.slotIndex + 1, [this.activeShield]);
        }

        return true;
    }

    /**
     * 프레임 업데이트 및 배리어-적 탄환 충돌 상호작용 (Owner Authority)
     */
    updateMovement(dt, canvasWidth, canvasHeight, enemyBullets = [], allyPlayers = []) {
        super.updateMovement(dt, canvasWidth, canvasHeight, enemyBullets, allyPlayers);

        if (this.activeShield) {
            const shield = this.activeShield;
            shield.duration -= dt;

            if (shield.duration <= 0 || shield.hp <= 0) {
                this.activeShield = null;
                if (this.isLocalOwner && window.networkManager) {
                    window.networkManager.sendObjectStateSync(this.slotIndex + 1, []);
                }
                return;
            }

            // 💡 [Owner Authority]: 내 소유 기체(isLocalOwner)이거나 AI인 경우만 직접 HP 차감 연산
            const hasAuthority = this.isLocalOwner || !this.isHuman;

            if (hasAuthority) {
                let shieldDamaged = false;

                // 적 탄환 소멸 처리
                for (let i = enemyBullets.length - 1; i >= 0; i--) {
                    const b = enemyBullets[i];
                    if (!b || b.isDead) continue;

                    const dist = Math.hypot(b.x - shield.x, b.y - shield.y);

                    if (Math.abs(dist - shield.radius) <= shield.thickness + (b.radius || 4)) {
                        let bAngle = Math.atan2(b.y - shield.y, b.x - shield.x);
                        let diff = bAngle - shield.angle;

                        while (diff < -Math.PI) diff += Math.PI * 2;
                        while (diff > Math.PI) diff -= Math.PI * 2;

                        if (Math.abs(diff) <= shield.arcAngle / 2) {
                            b.isDead = true;
                            shield.hp -= 1;
                            shieldDamaged = true;

                            if (shield.hp <= 0) {
                                this.activeShield = null;
                                break;
                            }
                        }
                    }
                }

                // 보스 레이저(dangerAreas) 선분 차단 및 방패 내구도 차감
                if (this.activeShield && window.gameLoopInstance && window.gameLoopInstance.boss) {
                    const boss = window.gameLoopInstance.boss;
                    if (Array.isArray(boss.dangerAreas)) {
                        boss.dangerAreas.forEach(area => {
                            if (area.isFiring && this.activeShield) {
                                const A = shield.x - area.x1;
                                const B = shield.y - area.y1;
                                const C = area.x2 - area.x1;
                                const D = area.y2 - area.y1;
                                const dot = A * C + B * D;
                                const lenSq = C * C + D * D;
                                let param = -1;
                                if (lenSq !== 0) param = dot / lenSq;

                                let xx, yy;
                                if (param < 0) { xx = area.x1; yy = area.y1; }
                                else if (param > 1) { xx = area.x2; yy = area.y2; }
                                else { xx = area.x1 + param * C; yy = area.y1 + param * D; }

                                const distToLaser = Math.hypot(shield.x - xx, shield.y - yy);

                                if (Math.abs(distToLaser - shield.radius) <= shield.thickness + (area.width / 2)) {
                                    let laserAngle = Math.atan2(yy - shield.y, xx - shield.x);
                                    let diff = laserAngle - shield.angle;
                                    while (diff < -Math.PI) diff += Math.PI * 2;
                                    while (diff > Math.PI) diff -= Math.PI * 2;

                                    if (Math.abs(diff) <= shield.arcAngle / 2) {
                                        shield.hp -= 15 * dt;
                                        shieldDamaged = true;
                                        area.isBlockedByShield = true;
                                        if (shield.hp <= 0) {
                                            this.activeShield = null;
                                        }
                                    }
                                }
                            }
                        });
                    }
                }

                // 피해가 발생했거나 일정 주기마다 OBJECT_STATE_SYNC 전송
                if (this.isLocalOwner && window.networkManager && (shieldDamaged || Math.random() < 0.1)) {
                    window.networkManager.sendObjectStateSync(
                        this.slotIndex + 1,
                        this.activeShield ? [this.activeShield] : []
                    );
                }
            }

            // SafeSpot 계산
            if (this.activeShield) {
                const wallCenterX = shield.x + Math.cos(shield.angle) * shield.radius;
                const wallCenterY = shield.y + Math.sin(shield.angle) * shield.radius;
                const BODY_MARGIN = 22;

                const insideAngle = shield.angle + Math.PI;
                shield.safeSpot = {
                    x: wallCenterX + Math.cos(insideAngle) * BODY_MARGIN,
                    y: wallCenterY + Math.sin(insideAngle) * BODY_MARGIN,
                    radius: 18
                };
            }
        }
    }

    draw(ctx, allyPlayers = []) {
        super.draw(ctx, allyPlayers);

        // 배리어 호 렌더링
        if (this.activeShield) {
            const s = this.activeShield;
            ctx.save();
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.radius, s.angle - s.arcAngle / 2, s.angle + s.arcAngle / 2);
            ctx.lineWidth = s.thickness;
            ctx.strokeStyle = `rgba(59, 130, 246, ${Math.min(1.0, s.hp / s.maxHp)})`;
            ctx.stroke();

            // 배리어 HP 바 표기
            ctx.font = '9px Orbitron';
            ctx.fillStyle = '#60a5fa';
            ctx.textAlign = 'center';
            const textX = s.x + Math.cos(s.angle) * (s.radius + 15);
            const textY = s.y + Math.sin(s.angle) * (s.radius + 15);
            ctx.fillText(`SHIELD: ${Math.ceil(s.hp)}`, textX, textY);

            ctx.restore();
        }
    }
}
```

# 📄 [요청 7 ➡️ 불러온함수 (ShielderPlayer 본체)] TARGET: extraction_target_project/js/player/characters/shielderPlayer.js (11-238라인)
# ----------------------------------------------------------
```python
export class ShielderPlayer extends BasePlayer {
    constructor(slotIndex) {
        super(slotIndex, 'shielderPlayer');

        // --- 쉴더 전용 메타 설정 ---
        this.className = '쉴더 (Shielder)';
        this.themeColor = '#3b82f6';                // 파란색 테마
        this.hasActiveSkill = true;
        this.skillIconClass = 'fa-solid fa-shield-halved';
        this.skillName = 'SHIELD';
        this.skillFloatText = 'BARRIER DEPLOYED!';

        this.maxGauge = 70;                         // 스킬 게이지 70
        this.activeShield = null;                   // 현재 설치된 배리어 정보
    }

    /**
     * 쉴더 전용 스킬 시전 (방어막 설치)
     * @param {object} targetInfo 마우스/조작 입력 및 보스 정보
     */
    useSkill(targetInfo = {}) {
        if (!super.useSkill(targetInfo)) return false;

        let deployAngle = -Math.PI / 2; // 기본 방향: 위쪽

        if (this.isHuman) {
            const keys = targetInfo.keys || {};
            let dx = 0;
            let dy = 0;

            if (keys['KeyW'] || keys['ArrowUp']) dy -= 1;
            if (keys['KeyS'] || keys['ArrowDown']) dy += 1;
            if (keys['KeyA'] || keys['ArrowLeft']) dx -= 1;
            if (keys['KeyD'] || keys['ArrowRight']) dx += 1;

            if (dx !== 0 || dy !== 0) {
                deployAngle = Math.atan2(dy, dx);
            } else {
                const mousePos = targetInfo.mousePos;
                if (mousePos) {
                    deployAngle = Math.atan2(mousePos.y - this.y, mousePos.x - this.x);
                }
            }
        } else {
            const boss = targetInfo.boss;
            const enemyMinions = targetInfo.enemyMinions || [];
            const allEnemies = [boss, ...enemyMinions].filter(e => e && !e.isDead);

            let closest = null;
            let minDist = Infinity;
            for (const enemy of allEnemies) {
                const d = Math.hypot(enemy.x - this.x, enemy.y - this.y);
                if (d < minDist) {
                    minDist = d;
                    closest = enemy;
                }
            }

            if (closest) {
                deployAngle = Math.atan2(closest.y - this.y, closest.x - this.x);
            }
        }

        // 곡선 배리어 생성 (체력 100, 반지름 70px, 90도 호)
        this.activeShield = {
            id: `shield_${this.slotIndex}_${Date.now()}`,
            x: this.x,
            y: this.y,
            angle: deployAngle,
            radius: 70,
            arcAngle: Math.PI / 2,
            hp: 100,
            maxHp: 100,
            thickness: 12,
            duration: 20.0
        };

        // 소유자(Owner)인 경우 전체 기기에 방벽 생성 브로드캐스트
        if (this.isLocalOwner && window.networkManager) {
            window.networkManager.sendObjectStateSync(this.slotIndex + 1, [this.activeShield]);
        }

        return true;
    }

    /**
     * 프레임 업데이트 및 배리어-적 탄환 충돌 상호작용 (Owner Authority)
     */
    updateMovement(dt, canvasWidth, canvasHeight, enemyBullets = [], allyPlayers = []) {
        super.updateMovement(dt, canvasWidth, canvasHeight, enemyBullets, allyPlayers);

        if (this.activeShield) {
            const shield = this.activeShield;
            shield.duration -= dt;

            if (shield.duration <= 0 || shield.hp <= 0) {
                this.activeShield = null;
                if (this.isLocalOwner && window.networkManager) {
                    window.networkManager.sendObjectStateSync(this.slotIndex + 1, []);
                }
                return;
            }

            // 💡 [Owner Authority]: 내 소유 기체(isLocalOwner)이거나 AI인 경우만 직접 HP 차감 연산
            const hasAuthority = this.isLocalOwner || !this.isHuman;

            if (hasAuthority) {
                let shieldDamaged = false;

                // 적 탄환 소멸 처리
                for (let i = enemyBullets.length - 1; i >= 0; i--) {
                    const b = enemyBullets[i];
                    if (!b || b.isDead) continue;

                    const dist = Math.hypot(b.x - shield.x, b.y - shield.y);

                    if (Math.abs(dist - shield.radius) <= shield.thickness + (b.radius || 4)) {
                        let bAngle = Math.atan2(b.y - shield.y, b.x - shield.x);
                        let diff = bAngle - shield.angle;

                        while (diff < -Math.PI) diff += Math.PI * 2;
                        while (diff > Math.PI) diff -= Math.PI * 2;

                        if (Math.abs(diff) <= shield.arcAngle / 2) {
                            b.isDead = true;
                            shield.hp -= 1;
                            shieldDamaged = true;

                            if (shield.hp <= 0) {
                                this.activeShield = null;
                                break;
                            }
                        }
                    }
                }

                // 보스 레이저(dangerAreas) 선분 차단 및 방패 내구도 차감
                if (this.activeShield && window.gameLoopInstance && window.gameLoopInstance.boss) {
                    const boss = window.gameLoopInstance.boss;
                    if (Array.isArray(boss.dangerAreas)) {
                        boss.dangerAreas.forEach(area => {
                            if (area.isFiring && this.activeShield) {
                                const A = shield.x - area.x1;
                                const B = shield.y - area.y1;
                                const C = area.x2 - area.x1;
                                const D = area.y2 - area.y1;
                                const dot = A * C + B * D;
                                const lenSq = C * C + D * D;
                                let param = -1;
                                if (lenSq !== 0) param = dot / lenSq;

                                let xx, yy;
                                if (param < 0) { xx = area.x1; yy = area.y1; }
                                else if (param > 1) { xx = area.x2; yy = area.y2; }
                                else { xx = area.x1 + param * C; yy = area.y1 + param * D; }

                                const distToLaser = Math.hypot(shield.x - xx, shield.y - yy);

                                if (Math.abs(distToLaser - shield.radius) <= shield.thickness + (area.width / 2)) {
                                    let laserAngle = Math.atan2(yy - shield.y, xx - shield.x);
                                    let diff = laserAngle - shield.angle;
                                    while (diff < -Math.PI) diff += Math.PI * 2;
                                    while (diff > Math.PI) diff -= Math.PI * 2;

                                    if (Math.abs(diff) <= shield.arcAngle / 2) {
                                        shield.hp -= 15 * dt;
                                        shieldDamaged = true;
                                        area.isBlockedByShield = true;
                                        if (shield.hp <= 0) {
                                            this.activeShield = null;
                                        }
                                    }
                                }
                            }
                        });
                    }
                }

                // 피해가 발생했거나 일정 주기마다 OBJECT_STATE_SYNC 전송
                if (this.isLocalOwner && window.networkManager && (shieldDamaged || Math.random() < 0.1)) {
                    window.networkManager.sendObjectStateSync(
                        this.slotIndex + 1,
                        this.activeShield ? [this.activeShield] : []
                    );
                }
            }

            // SafeSpot 계산
            if (this.activeShield) {
                const wallCenterX = shield.x + Math.cos(shield.angle) * shield.radius;
                const wallCenterY = shield.y + Math.sin(shield.angle) * shield.radius;
                const BODY_MARGIN = 22;

                const insideAngle = shield.angle + Math.PI;
                shield.safeSpot = {
                    x: wallCenterX + Math.cos(insideAngle) * BODY_MARGIN,
                    y: wallCenterY + Math.sin(insideAngle) * BODY_MARGIN,
                    radius: 18
                };
            }
        }
    }

    draw(ctx, allyPlayers = []) {
        super.draw(ctx, allyPlayers);

        // 배리어 호 렌더링
        if (this.activeShield) {
            const s = this.activeShield;
            ctx.save();
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.radius, s.angle - s.arcAngle / 2, s.angle + s.arcAngle / 2);
            ctx.lineWidth = s.thickness;
            ctx.strokeStyle = `rgba(59, 130, 246, ${Math.min(1.0, s.hp / s.maxHp)})`;
            ctx.stroke();

            // 배리어 HP 바 표기
            ctx.font = '9px Orbitron';
            ctx.fillStyle = '#60a5fa';
            ctx.textAlign = 'center';
            const textX = s.x + Math.cos(s.angle) * (s.radius + 15);
            const textY = s.y + Math.sin(s.angle) * (s.radius + 15);
            ctx.fillText(`SHIELD: ${Math.ceil(s.hp)}`, textX, textY);

            ctx.restore();
        }
    }
}
```

# 📄 [요청 8] TARGET: js/player/characters/summonerPlayer.js (12-84라인)
# ----------------------------------------------------------
```python
export class SummonerPlayer extends BasePlayer {
    constructor(slotIndex) {
        super(slotIndex, 'summonerPlayer');

        this.className = '서머너 (Summoner)';
        this.themeColor = '#10b981';
        this.hasActiveSkill = true;
        this.skillIconClass = 'fa-solid fa-robot';
        this.skillName = 'SUMMON ALL';
        this.skillFloatText = 'BERSERKERS & DRONE SUMMONED!';

        this.maxGauge = 120;
    }

    /**
     * 게이지 120 소모 시 무적 드론 1마리 + 탱커 버서커 2마리 동시 소환
     */
    useSkill(context = {}) {
        if (!super.useSkill(context)) return false;

        if (context.allyMinions && Array.isArray(context.allyMinions)) {
            // 1. 원거리 무적 궤도 드론 1마리 소환
            const drone = new ShooterMinion(this, 0);
            context.allyMinions.push(drone);

            // 2. 스폰 위치 중첩 방지 (좌/우 35px 오프셋)
            const leftX = Math.max(20, this.x - 35);
            const rightX = Math.min(1260, this.x + 35);

            const b1 = new BerserkerMinion(this, leftX, this.y);
            const b2 = new BerserkerMinion(this, rightX, this.y);
            context.allyMinions.push(b1);
            context.allyMinions.push(b2);

            // 소유자(Owner)인 경우 OBJECT_STATE_SYNC 브로드캐스트
            if (this.isLocalOwner && window.networkManager) {
                const minionStates = [
                    { id: `drone_${this.slotIndex}_${Date.now()}`, type: 'drone', hp: drone.hp, maxHp: drone.maxHp, x: drone.x, y: drone.y },
                    { id: `b1_${this.slotIndex}_${Date.now()}`, type: 'berserker', hp: b1.hp, maxHp: b1.maxHp, x: b1.x, y: b1.y },
                    { id: `b2_${this.slotIndex}_${Date.now()}`, type: 'berserker', hp: b2.hp, maxHp: b2.maxHp, x: b2.x, y: b2.y }
                ];
                window.networkManager.sendObjectStateSync(this.slotIndex + 1, minionStates);
            }
        }

        return true;
    }

    draw(ctx, allyPlayers = []) {
        super.draw(ctx, allyPlayers);

        if (!this.isStunned()) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(Date.now() * 0.002);
            ctx.strokeStyle = this.themeColor;
            ctx.lineWidth = 1.5;

            ctx.beginPath();
            for (let i = 0; i < 3; i++) {
                const a = (Math.PI * 2 / 3) * i;
                const hx = Math.cos(a) * 12;
                const hy = Math.sin(a) * 12;
                if (i === 0) ctx.moveTo(hx, hy);
                else ctx.lineTo(hx, hy);
            }
            ctx.closePath();
            ctx.stroke();

            ctx.restore();
        }
    }
}
```

# 📄 [요청 8 ➡️ 불러온함수 (SummonerPlayer 본체)] TARGET: extraction_target_project/js/player/characters/summonerPlayer.js (12-84라인)
# ----------------------------------------------------------
```python
export class SummonerPlayer extends BasePlayer {
    constructor(slotIndex) {
        super(slotIndex, 'summonerPlayer');

        this.className = '서머너 (Summoner)';
        this.themeColor = '#10b981';
        this.hasActiveSkill = true;
        this.skillIconClass = 'fa-solid fa-robot';
        this.skillName = 'SUMMON ALL';
        this.skillFloatText = 'BERSERKERS & DRONE SUMMONED!';

        this.maxGauge = 120;
    }

    /**
     * 게이지 120 소모 시 무적 드론 1마리 + 탱커 버서커 2마리 동시 소환
     */
    useSkill(context = {}) {
        if (!super.useSkill(context)) return false;

        if (context.allyMinions && Array.isArray(context.allyMinions)) {
            // 1. 원거리 무적 궤도 드론 1마리 소환
            const drone = new ShooterMinion(this, 0);
            context.allyMinions.push(drone);

            // 2. 스폰 위치 중첩 방지 (좌/우 35px 오프셋)
            const leftX = Math.max(20, this.x - 35);
            const rightX = Math.min(1260, this.x + 35);

            const b1 = new BerserkerMinion(this, leftX, this.y);
            const b2 = new BerserkerMinion(this, rightX, this.y);
            context.allyMinions.push(b1);
            context.allyMinions.push(b2);

            // 소유자(Owner)인 경우 OBJECT_STATE_SYNC 브로드캐스트
            if (this.isLocalOwner && window.networkManager) {
                const minionStates = [
                    { id: `drone_${this.slotIndex}_${Date.now()}`, type: 'drone', hp: drone.hp, maxHp: drone.maxHp, x: drone.x, y: drone.y },
                    { id: `b1_${this.slotIndex}_${Date.now()}`, type: 'berserker', hp: b1.hp, maxHp: b1.maxHp, x: b1.x, y: b1.y },
                    { id: `b2_${this.slotIndex}_${Date.now()}`, type: 'berserker', hp: b2.hp, maxHp: b2.maxHp, x: b2.x, y: b2.y }
                ];
                window.networkManager.sendObjectStateSync(this.slotIndex + 1, minionStates);
            }
        }

        return true;
    }

    draw(ctx, allyPlayers = []) {
        super.draw(ctx, allyPlayers);

        if (!this.isStunned()) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(Date.now() * 0.002);
            ctx.strokeStyle = this.themeColor;
            ctx.lineWidth = 1.5;

            ctx.beginPath();
            for (let i = 0; i < 3; i++) {
                const a = (Math.PI * 2 / 3) * i;
                const hx = Math.cos(a) * 12;
                const hy = Math.sin(a) * 12;
                if (i === 0) ctx.moveTo(hx, hy);
                else ctx.lineTo(hx, hy);
            }
            ctx.closePath();
            ctx.stroke();

            ctx.restore();
        }
    }
}
```

# 📄 [요청 8 ➡️ 불러온함수 (BerserkerMinion 본체)] TARGET: extraction_target_project/js/minian/ally/berserkerMinion.js (7-241라인)
# ----------------------------------------------------------
```python
export class BerserkerMinion extends BaseAllyMinion {
    constructor(owner, spawnX = 0, spawnY = 0) {
        super(owner, {
            radius: 13,
            hp: 120,        // 체력 120 고체력 탱커
            maxHp: 120,
            color: '#ef4444',
            fireRate: 1.3 // 와리가리 도끼 스윙 연사력
        });

        if (spawnX && spawnY) {
            this.x = spawnX;
            this.y = spawnY;
        }

        this.baseSpeed = 20; // 이동속도 1/2 감축 (90 px/s)
        this.weaponLength = 32;

        this.vx = 0;
        this.vy = 0;

        // 2초 소환중 연출 (검붉은 삼각형 회전 소환진, 소환 중 무적)
        this.spawnTimer = 2;
        this.isSpawning = true;

        // 광폭화 (HP 50% / 20 이하 시 +12 HP 회복 & 5초간 피격 50% 감쇄)
        this.isBerserkMode = false;
        this.berserkBuffTimer = 0;

        // 도끼 와리가리 애니메이션 변수
        this.axeSwingAngle = 0;
        this.axeSwingDir = 1;
        this.isSwinging = false;
        this.swingProgress = 0;
        this.targetAngle = 0;
    }

    takeDamage(amount) {
        if (this.isDead || this.isSpawning) return;

        // 광폭화 5초 버프 활성화 시 탄막 피해 50% 반감
        const finalDamage = (this.isBerserkMode && this.berserkBuffTimer > 0) ? amount * 0.5 : amount;

        this.hp -= finalDamage;

        // 체력 50% (20 HP) 이하에서 광폭화 1회 트리거
        if (this.hp <= 20 && !this.isBerserkMode) {
            this.isBerserkMode = true;
            this.hp = Math.min(this.maxHp, this.hp + 50); // +50 HP 회복
            this.berserkBuffTimer = 5.0;                   // 5초간 50% 반감 버프
        }

        if (this.hp <= 0) {
            this.hp = 0;
            this.isDead = true;
        }
    }

    updateMovement(enemyEntities = [], dt = 0.016) {
        super.updateMovement(enemyEntities, dt);
        if (this.isDead) return;

        // 소환 대기 연출 처리
        if (this.isSpawning) {
            this.spawnTimer -= dt;
            if (this.spawnTimer <= 0) {
                this.isSpawning = false;
            }
            return;
        }

        if (this.berserkBuffTimer > 0) {
            this.berserkBuffTimer -= dt;
        }

        // 유도미사일식 관성 곡선 이동
        const target = this.findClosestTarget(enemyEntities);
        if (target) {
            const dist = Math.hypot(target.x - this.x, target.y - this.y);
            this.targetAngle = Math.atan2(target.y - this.y, target.x - this.x);

            const idealDistance = (target.radius || 25) + this.radius + this.weaponLength;

            if (dist > idealDistance + 5) {
                const desiredVx = Math.cos(this.targetAngle) * this.baseSpeed;
                const desiredVy = Math.sin(this.targetAngle) * this.baseSpeed;

                this.vx = this.vx * 0.85 + desiredVx * 0.15;
                this.vy = this.vy * 0.85 + desiredVy * 0.15;
            } else {
                this.vx *= 0.8;
                this.vy *= 0.8;
            }

            this.x += this.vx * dt;
            this.y += this.vy * dt;
        }

        // 도끼 와리가리 스윙 애니메이션
        if (this.isSwinging) {
            this.swingProgress += dt * 18;
            this.axeSwingAngle = Math.sin(this.swingProgress) * 0.9 * this.axeSwingDir;

            if (this.swingProgress >= Math.PI) {
                this.isSwinging = false;
                this.swingProgress = 0;
                this.axeSwingAngle = 0;
                this.axeSwingDir *= -1;
            }
        }
    }

    updateAttack(enemyEntities = [], allyBullets = [], dt = 0.016) {
        if (this.isDead || this.isSpawning) return;

        this.attackTimer += dt;

        if (this.attackTimer >= this.fireRate) {
            const target = this.findClosestTarget(enemyEntities);
            if (target) {
                const dist = Math.hypot(target.x - this.x, target.y - this.y);
                const idealDistance = (target.radius || 25) + this.radius + this.weaponLength;

                if (dist <= idealDistance + 15) {
                    this.isSwinging = true;
                    this.swingProgress = 0;

                    if (typeof target.takeDamage === 'function') {
                        target.takeDamage(1); // 공격력 1
                    }
                    this.attackTimer = 0;
                }
            }
        }
    }

    draw(ctx) {
        if (this.isDead) return;

        // 💡 [동적 캔버스 크기 기반 맵 이탈 방지] 렌더링 시점의 캔버스 너비/높이에 맞춰 위치 클램핑
        if (ctx && ctx.canvas) {
            const margin = this.radius + 12;
            this.x = Math.max(margin, Math.min(ctx.canvas.width - margin, this.x));
            this.y = Math.max(margin, Math.min(ctx.canvas.height - margin, this.y));
        }

        ctx.save();
        ctx.translate(this.x, this.y);

        // 1. 2초 검붉은 선 회전 삼각형 소환진 연출
        if (this.isSpawning) {
            const spawnProgress = Math.max(0, 1 - (this.spawnTimer / 2));
            const scale = 0.3 + spawnProgress * 0.9;
            const rotAngle = Date.now() * 0.01;

            ctx.rotate(rotAngle);
            ctx.strokeStyle = '#dc2626';
            ctx.lineWidth = 2.5;
            ctx.shadowColor = '#991b1b';
            ctx.shadowBlur = 15;

            ctx.beginPath();
            for (let i = 0; i < 3; i++) {
                const a = (Math.PI * 2 / 3) * i;
                const sx = Math.cos(a) * (26 * scale);
                const sy = Math.sin(a) * (26 * scale);
                if (i === 0) ctx.moveTo(sx, sy);
                else ctx.lineTo(sx, sy);
            }
            ctx.closePath();
            ctx.stroke();

            ctx.restore();
            return;
        }

        // 2. 버서커 본체 렌더링 (광폭화 시 1.35배 거대화)
        const currentRadius = this.isBerserkMode ? this.radius * 1.35 : this.radius;

        if (this.isBerserkMode && this.berserkBuffTimer > 0) {
            const pulse = Math.sin(Date.now() * 0.02) * 5;
            ctx.shadowColor = '#ef4444';
            ctx.shadowBlur = 20 + pulse;
            ctx.fillStyle = '#b91c1c';
        } else {
            ctx.shadowColor = '#dc2626';
            ctx.shadowBlur = 8;
            ctx.fillStyle = '#f87171';
        }

        ctx.beginPath();
        ctx.arc(0, 0, currentRadius, 0, Math.PI * 2);
        ctx.fill();

        // 뿔 연출
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(-currentRadius * 0.5, -currentRadius * 0.5);
        ctx.lineTo(-currentRadius * 1.0, -currentRadius * 1.2);
        ctx.moveTo(currentRadius * 0.5, -currentRadius * 0.5);
        ctx.lineTo(currentRadius * 1.0, -currentRadius * 1.2);
        ctx.stroke();

        // 🪓 양날도끼 와리가리 스윙
        ctx.rotate(this.targetAngle + this.axeSwingAngle);

        const handleLen = currentRadius + 18;
        const axeSize = currentRadius * 0.85;

        // 도끼 자루
        ctx.strokeStyle = '#d97706';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(handleLen, 0);
        ctx.stroke();

        // 양날도끼 헤드
        ctx.fillStyle = this.isBerserkMode ? '#fca5a5' : '#e2e8f0';
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 1.5;

        ctx.beginPath();
        ctx.moveTo(handleLen - 2, 0);
        ctx.lineTo(handleLen + axeSize, -axeSize);
        ctx.lineTo(handleLen + axeSize * 1.2, 0);
        ctx.lineTo(handleLen + axeSize, axeSize);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        ctx.restore();
    }
}
```

# 📄 [요청 8 ➡️ 불러온함수 (ShooterMinion 본체)] TARGET: extraction_target_project/js/minian/ally/shooterMinion.js (9-109라인)
# ----------------------------------------------------------
```python
export class ShooterMinion extends BaseAllyMinion {
    constructor(owner, orbitAngleOffset = 0) {
        super(owner, {
            radius: 9,
            hp: 9999, // 무적
            maxHp: 9999,
            color: '#34d399',
            fireRate: 2.0 // 공속 1/10 수준
        });

        this.orbitAngleOffset = orbitAngleOffset;
        this.orbitRadius = 42;
    }

    updateMovement(enemyEntities, dt) {
        super.updateMovement(enemyEntities, dt);
        if (this.isDead || !this.owner) return;

        const time = Date.now() * 0.002;
        const targetX = this.owner.x + Math.cos(time + this.orbitAngleOffset) * this.orbitRadius;
        const targetY = this.owner.y + Math.sin(time + this.orbitAngleOffset) * this.orbitRadius;

        this.x += (targetX - this.x) * dt * 6;
        this.y += (targetY - this.y) * dt * 6;
    }

    updateAttack(enemyEntities = [], allyBullets = [], dt = 0.016) {
        if (this.isDead) return;

        this.attackTimer += dt;

        if (this.attackTimer >= this.fireRate) {
            const target = this.findClosestTarget(enemyEntities);
            if (target) {
                this.shoot(target, allyBullets);
                this.attackTimer = 0;
            }
        }
    }

    shoot(target, allyBullets) {
        // AI 특유의 오차 조준 (±0.3 라디안) - 미니언 공격 독립 PRNG 적용
        const baseAngle = Math.atan2(target.y - this.y, target.x - this.x);
        const aimError = (rngMinion.attack() - 0.5) * 0.6;
        const finalAngle = baseAngle + aimError;

        const bulletSpeed = 350;

        allyBullets.push({
            x: this.x,
            y: this.y,
            vx: Math.cos(finalAngle) * bulletSpeed,
            vy: Math.sin(finalAngle) * bulletSpeed,
            radius: 3.5,
            damage: 3,
            color: '#a7f3d0',
            isAlly: true,
            isDead: false,
            update(slots, dt) {
                this.x += this.vx * dt;
                this.y += this.vy * dt;
            },
            draw(ctx) {
                ctx.save();
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.shadowColor = '#34d399';
                ctx.shadowBlur = 8;
                ctx.fill();
                ctx.restore();
            }
        });
    }

    draw(ctx) {
        if (this.isDead) return;

        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(Date.now() * 0.004);
        ctx.strokeStyle = '#34d399';
        ctx.lineWidth = 1.5;
        ctx.shadowColor = '#059669';
        ctx.shadowBlur = 10;

        ctx.beginPath();
        ctx.moveTo(0, -this.radius);
        ctx.lineTo(this.radius * 0.8, this.radius * 0.8);
        ctx.lineTo(-this.radius * 0.8, this.radius * 0.8);
        ctx.closePath();
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(0, 0, 2.5, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.fill();

        ctx.restore();
    }
}
```

# 📄 [요청 9] TARGET: js/main.js (28-38라인)
# ----------------------------------------------------------
```python
    function resizeCanvas() {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const scale = Math.min(windowWidth / GAME_WIDTH, windowHeight / GAME_HEIGHT);

        canvas.style.width = `${GAME_WIDTH * scale}px`;
        canvas.style.height = `${GAME_HEIGHT * scale}px`;
        canvas.style.position = 'absolute';
        canvas.style.left = `${(windowWidth - GAME_WIDTH * scale) / 2}px`;
        canvas.style.top = `${(windowHeight - GAME_HEIGHT * scale) / 2}px`;
    }
```

# 📄 [요청 9 ➡️ 불러온함수 (resizeCanvas 본체)] TARGET: extraction_target_project/js/main.js (28-38라인)
# ----------------------------------------------------------
```python
    function resizeCanvas() {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const scale = Math.min(windowWidth / GAME_WIDTH, windowHeight / GAME_HEIGHT);

        canvas.style.width = `${GAME_WIDTH * scale}px`;
        canvas.style.height = `${GAME_HEIGHT * scale}px`;
        canvas.style.position = 'absolute';
        canvas.style.left = `${(windowWidth - GAME_WIDTH * scale) / 2}px`;
        canvas.style.top = `${(windowHeight - GAME_HEIGHT * scale) / 2}px`;
    }
```
