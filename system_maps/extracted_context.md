# ==========================================================================
# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드
# [SCAN_MODE] EXTRACTION_TARGET_PROJECT
# ==========================================================================
# 📄 [요청 1] TARGET: js/main.js (1-111라인)
# ----------------------------------------------------------
```python
/**
 * js/main.js
 * 게임의 최상위 엔트리 포인트 모듈
 */
import { SceneManager } from './core/sceneManager.js';
import { InputHandler } from './core/input.js';
import { UIManager } from './core/ui.js';
import { GameLoop } from './core/gameLoop.js';
import { createImpactParticles } from './player/particle.js';
import { NetworkManager } from './network/networkManager.js';

window.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('gameCanvas');
    if (!canvas) {
        console.error('캔버스 엘리먼트(#gameCanvas)를 찾을 수 없습니다.');
        return;
    }

    const ctx = canvas.getContext('2d');

    // 1. 상태 머신 관리자 초기화
    const sceneManager = new SceneManager();

    // 2. 사용자 입력 처리기 초기화
    const inputHandler = new InputHandler();

    // 3. UI 매니저 초기화 및 콜백 바인딩
    // 3. UI 매니저 초기화 및 콜백 바인딩
    let gameLoopInstance = null;
    const uiManager = new UIManager({
        onSlotToggle: (slot) => {
            if (gameLoopInstance) {
                createImpactParticles(gameLoopInstance.particles, slot.x, slot.y, slot.color, 15);
            }
        },
        onToggleDebug: (show) => {
            if (gameLoopInstance) {
                gameLoopInstance.showAIDebug = show;
            }
        },
        onUseSkill: () => {
            if (gameLoopInstance && typeof gameLoopInstance.useUserSkill === 'function') {
                gameLoopInstance.useUserSkill();
            }
        },
        onUseBomb: () => {
            if (gameLoopInstance) {
                gameLoopInstance.useBomb();
            }
        },
        onRestart: () => {
            window.location.reload();
        }
    });

    // 4. 네트워크 배달망 초기화 (기본 방장 호스트 설정)
    const isHost = !window.location.search.includes('client=true');
    const hostIp = new URLSearchParams(window.location.search).get('host') || window.location.hostname;
    
    window.networkManager = new NetworkManager({
        isHost: isHost,
        hostIp: hostIp
    });
    window.networkManager.init();

    // 5. 게임 메인 루프 초기화 및 실행
    gameLoopInstance = new GameLoop(canvas, ctx, sceneManager, inputHandler, uiManager);

    // 6. [메인 메뉴] -> [게임 시작] 이벤트 및 P3 `k090207` 히든 디버그 트리거 검사
    const btnStart = document.getElementById('btn-start-game');
    if (btnStart) {
        btnStart.addEventListener('click', () => {
            // 💡 메뉴에서 라디오 버튼으로 선택한 슬롯(P1~P4)을 내 조작 슬롯으로 네트워크 매니저에 고정
            const selectedRadio = document.querySelector('input[name="my-slot-select"]:checked');
            if (selectedRadio && window.networkManager) {
                window.networkManager.mySlotIndex = parseInt(selectedRadio.value, 10);
            }

            // 게임 시작 직전 드롭다운에서 고른 캐릭터 기체로 슬롯 재구성
            if (gameLoopInstance) {
                gameLoopInstance.initSlots();
            }

            const p3NicknameInput = document.getElementById('p3-nickname');
            const p3Name = p3NicknameInput ? p3NicknameInput.value.trim() : '';

            // P3 닉네임이 k090207일 때 히든 디버그 모드 감지!
            if (p3Name === 'k090207') {
                gameLoopInstance.showAIDebug = true;
                uiManager.setDebugVisibility(true); // 상단 디버그 ON/OFF 버튼 노출
                console.log('🔓 [HIDDEN CHEAT] DEBUG MODE ACTIVATED (P3: k090207)');
            } else {
                gameLoopInstance.showAIDebug = false;
                uiManager.setDebugVisibility(false); // 상단 디버그 버튼 숨김
            }

            sceneManager.setState('PLAY');
        });
    }

    // [결과 화면] -> [메인 메뉴 이동] 버튼
    const btnMainMenu = document.getElementById('btn-main-menu');
    if (btnMainMenu) {
        btnMainMenu.addEventListener('click', () => {
            sceneManager.setState('MENU');
        });
    }

    // 5. 프레임 애니메이션 시작
    requestAnimationFrame((now) => gameLoopInstance.run(now));
});
```

# 📄 [요청 1 ➡️ 불러온함수 (InputHandler 본체)] TARGET: extraction_target_project/js/core/input.js (6-145라인)
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

        // 💡 스킬 전용 1회성 트리거 큐(Queue) 플래그 신설
        this.skillTriggered = false;

        this.initKeyboard();
        this.initMouse();
        this.initJoystick();
    }

    /**
     * 키보드 이벤트 리스너 등록
     */
    initKeyboard() {
        window.addEventListener('keydown', (e) => {
            // 키를 처음 누른 타이밍(Down Edge)에만 버튼 클릭처럼 1회 트리거
            if (!this.keys[e.code]) {
                if (e.code === 'Space' || e.key === ' ' || e.keyCode === 32) {
                    this.skillTriggered = true;
                    e.preventDefault();
                }
            }
            this.keys[e.code] = true;
        });

        window.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
    }

    /**
     * 마우스 리스너 등록 (우클릭 스킬 트리거)
     */
    initMouse() {
        window.addEventListener('mousemove', (e) => {
            this.mousePos.x = e.clientX;
            this.mousePos.y = e.clientY;
        });

        window.addEventListener('mousedown', (e) => {
            // 우클릭을 클릭한 첫 순간에만 버튼 클릭처럼 1회 트리거
            if (e.button === 2) {
                this.skillTriggered = true;
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
     * 💡 [네트워크 전송용] 현재 프레임의 클라이언트 조작 상태 패킷 추출
     * @returns {{dx: number, dy: number, mouseX: number, mouseY: number, useSkill: boolean}}
     */
    getInputAction() {
        let dx = 0;
        let dy = 0;

        if (this.keys['KeyW'] || this.keys['ArrowUp']) dy -= 1;
        if (this.keys['KeyS'] || this.keys['ArrowDown']) dy += 1;
        if (this.keys['KeyA'] || this.keys['ArrowLeft']) dx -= 1;
        if (this.keys['KeyD'] || this.keys['ArrowRight']) dx += 1;

        if (this.joystick && this.joystick.active) {
            dx = this.joystick.moveX;
            dy = this.joystick.moveY;
        }

        // 💡 누른 순간에만 1회성 트리거로 발동시키고 소모(Consume)
        const useSkill = this.skillTriggered;
        this.skillTriggered = false;

        return {
            dx,
            dy,
            mouseX: this.mousePos.x,
            mouseY: this.mousePos.y,
            useSkill: useSkill
        };
    }
}
```

# 📄 [요청 1 ➡️ 불러온함수 (GameLoop 본체)] TARGET: extraction_target_project/js/core/gameLoop.js (14-23라인)
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

# 📄 [요청 1 ➡️ 불러온함수 (createImpactParticles 본체)] TARGET: extraction_target_project/js/player/particle.js (57-61라인)
# ----------------------------------------------------------
```python
export function createImpactParticles(particlesContainer, x, y, color, count = 6) {
    for (let i = 0; i < count; i++) {
        particlesContainer.push(new Particle(x, y, color));
    }
}
```

# 📄 [요청 1 ➡️ 불러온함수 (NetworkManager 본체)] TARGET: extraction_target_project/js/network/networkManager.js (6-116라인)
# ----------------------------------------------------------
```python
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
```

# 📄 [요청 1 ➡️ 불러온함수 (UIManager 본체)] TARGET: extraction_target_project/js/core/ui.js (8-407라인)
# ----------------------------------------------------------
```python
export class UIManager {
    /**
     * @param {object} callbacks 
     * @param {Function} callbacks.onSlotToggle 슬롯 모드(User/AI) 변경 시 호출
     * @param {Function} callbacks.onToggleDebug 디버그 시각화 토글 시 호출
     * @param {Function} callbacks.onUseSkill 액티브 스킬 발동 시 호출
     * @param {Function} callbacks.onUseBomb EMP 특수폭탄 발동 시 호출
     * @param {Function} callbacks.onRestart 새 매치 시작 시 호출
     */
    constructor(callbacks = {}) {
        this.callbacks = callbacks;
        this.showAIDebug = true;

        this.elTimer = document.getElementById('matchTimerDisplay');
        this.elTeamScore = document.getElementById('teamScoreDisplay');
        this.elSlotContainer = document.getElementById('slotControlsContainer');
        this.elLiveStats = document.getElementById('liveStatsContainer');
        this.elDebugBtn = document.getElementById('btnToggleDebug');
        this.elDebugStatus = document.getElementById('debugStatusText');
        this.elBombBtn = document.getElementById('btnSpecialBomb');
        this.elModal = document.getElementById('gameOverModal');
        this.elScoreboardList = document.getElementById('finalScoreboardList');
        this.elRestartBtn = document.getElementById('btnRestartMatch');

        // 스킬 버튼 요소
        this.elSkillBtn = document.getElementById('btnActiveSkill');
        this.elSkillFill = document.getElementById('skillGaugeFill');
        this.elSkillText = document.getElementById('skillGaugeText');
        this.elSkillIcon = this.elSkillBtn ? this.elSkillBtn.querySelector('i') : null;

        this.populateClassDropdowns();
        this.bindEvents();
    }

    /**
     * characters 폴더 자동 검색을 통해 메뉴 드롭다운 갱신
     */
    populateClassDropdowns() {
        const discoveredClasses = getAutoDiscoveredClasses();

        for (let i = 1; i <= 4; i++) {
            const select = document.getElementById(`p${i}-class`);
            if (select) {
                select.innerHTML = '';
                discoveredClasses.forEach(cls => {
                    const opt = document.createElement('option');
                    opt.value = cls.id;       // 파일명 ID (예: 'bufferPlayer')
                    opt.innerText = cls.name; // 캐릭터 내부 이름
                    select.appendChild(opt);
                });
                
                // 각 슬롯별로 다양한 초기 캐릭터 배치
                const defaultClasses = ['bufferPlayer', 'empPlayer', 'shielderPlayer', 'summonerPlayer'];
                const defaultChoice = defaultClasses[i - 1] || 'defaultPlayer';
                if (select.querySelector(`option[value="${defaultChoice}"]`)) {
                    select.value = defaultChoice;
                }
            }
        }

        // 💡 [다른 사람 슬롯 수정 방지]: 라디오 버튼 변경 시 내 슬롯 외에는 전부 disabled 잠금 처리
        const updateSlotLockStatus = () => {
            const selectedRadio = document.querySelector('input[name="my-slot-select"]:checked');
            const mySlotNum = selectedRadio ? parseInt(selectedRadio.value, 10) : 1;

            for (let i = 1; i <= 4; i++) {
                const nameInput = document.getElementById(`p${i}-nickname`);
                const classSelect = document.getElementById(`p${i}-class`);
                const isMySlot = (i === mySlotNum);

                if (nameInput) {
                    nameInput.disabled = !isMySlot;
                    nameInput.style.opacity = isMySlot ? '1.0' : '0.4';
                }
                if (classSelect) {
                    classSelect.disabled = !isMySlot;
                    classSelect.style.opacity = isMySlot ? '1.0' : '0.4';
                }
            }
        };

        // 라디오 버튼 이벤트 바인딩 및 최초 실행
        const radios = document.querySelectorAll('input[name="my-slot-select"]');
        radios.forEach(radio => {
            radio.addEventListener('change', updateSlotLockStatus);
        });
        updateSlotLockStatus();
    }

    /**
     * P3 k090207 치트키 성공 여부에 따라 상단 디버그 버튼 및 무한 EMP 버튼 표시 제어
     * @param {boolean} isDebug 
     */
    setDebugVisibility(isDebug) {
        if (this.elDebugBtn) {
            if (isDebug) {
                this.elDebugBtn.classList.remove('hidden');
                this.showAIDebug = true;
                if (this.elDebugStatus) {
                    this.elDebugStatus.innerText = 'ON';
                    this.elDebugStatus.className = 'text-emerald-400';
                }
            } else {
                this.elDebugBtn.classList.add('hidden');
                this.showAIDebug = false;
                if (this.elDebugStatus) {
                    this.elDebugStatus.innerText = 'OFF';
                    this.elDebugStatus.className = 'text-gray-500';
                }
            }
        }

        // k090207 치트키 성공시에만 무제한 EMP 폭탄 버튼 표시
        if (this.elBombBtn) {
            if (isDebug) {
                this.elBombBtn.classList.remove('hidden');
            } else {
                this.elBombBtn.classList.add('hidden');
            }
        }

        // 💡 [우측 패널 디버그 모드 연동]: 디버그 모드 시에만 우측 슬롯 제어/통계 창 표시
        const rightPanel = document.getElementById('right-debug-panel');
        if (rightPanel) {
            if (isDebug) {
                rightPanel.classList.remove('hidden');
            } else {
                rightPanel.classList.add('hidden');
            }
        }

        // 💡 [k090207 디버그 모드]: 폰 접속용 QR 코드 및 IP URL 표시
        const netInfoContainer = document.getElementById('debug-network-info');
        const qrImg = document.getElementById('qr-code-img');
        const hostUrlText = document.getElementById('host-ip-url');

        if (netInfoContainer) {
            if (isDebug) {
                netInfoContainer.classList.remove('hidden');
                
                // 현재 호스트 IP 조합 (localhost인 경우 안내 문구)
                const currentHost = window.location.hostname || 'localhost';
                const port = window.location.port ? `:${window.location.port}` : '';
                const joinUrl = `http://${currentHost}${port}?client=true&host=${currentHost}`;

                if (hostUrlText) hostUrlText.innerText = joinUrl;
                if (qrImg) {
                    qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(joinUrl)}`;
                }
            } else {
                netInfoContainer.classList.add('hidden');
            }
        }
    }
    /**
     * 버튼 이벤트 리스너 등록
     */
    bindEvents() {
        if (this.elDebugBtn) {
            this.elDebugBtn.addEventListener('click', () => {
                this.showAIDebug = !this.showAIDebug;
                if (this.elDebugStatus) {
                    this.elDebugStatus.innerText = this.showAIDebug ? 'ON' : 'OFF';
                    this.elDebugStatus.className = this.showAIDebug ? 'text-emerald-400' : 'text-gray-500';
                }
                if (this.callbacks.onToggleDebug) {
                    this.callbacks.onToggleDebug(this.showAIDebug);
                }
            });
        }

        if (this.elSkillBtn) {
            this.elSkillBtn.addEventListener('click', () => {
                if (this.callbacks.onUseSkill) {
                    this.callbacks.onUseSkill();
                }
            });
        }

        if (this.elBombBtn) {
            this.elBombBtn.addEventListener('click', () => {
                if (this.callbacks.onUseBomb) {
                    this.callbacks.onUseBomb();
                }
            });
        }

        if (this.elRestartBtn) {
            this.elRestartBtn.addEventListener('click', () => {
                if (this.callbacks.onRestart) {
                    this.callbacks.onRestart();
                } else {
                    window.location.reload();
                }
            });
        }
    }

    /**
     * 💡 [유저 스킬 버튼 및 상단 점수창 옆 AI ON/OFF 토글 버튼 연동]
     */
    bindSkillButton(getUserPlayerFn, gameLoopInstance) {
        // 1. 상단 점수창 옆 AI ON/OFF 토글 버튼 이벤트 바인딩
        const topAiToggleBtn = document.getElementById('btn-top-ai-toggle');
        if (topAiToggleBtn) {
            topAiToggleBtn.onclick = () => {
                const mySlotIdx = (window.networkManager && window.networkManager.mySlotIndex) 
                    ? window.networkManager.mySlotIndex - 1 
                    : 0;
                
                // 내 컴퓨터에 할당된 기체 슬롯을 정확히 탐색
                const myPlayer = gameLoopInstance.slots ? gameLoopInstance.slots[mySlotIdx] : null;

                if (myPlayer) {
                    myPlayer.isHuman = !myPlayer.isHuman; // 내 기체만 유저/AI 수동 전환
                    const statusText = document.getElementById('top-ai-status-text');
                    if (statusText) {
                        statusText.innerText = myPlayer.isHuman ? 'USER (MANUAL)' : 'AI (AUTO)';
                        statusText.className = myPlayer.isHuman ? 'text-cyan-400 font-bold' : 'text-pink-400 font-bold';
                    }
                }
            };
        }

        // 2. 우측 하단 스킬 버튼 클릭/터치 이벤트 핸들러 연동
        if (!this.elSkillBtn) return;

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

        // 기존 이벤트 중복 방지 후 신규 등록
        this.elSkillBtn.onclick = triggerSkill;
    }

    /**
     * 캐릭터 스펙(hasActiveSkill, maxGauge, themeColor, skillIconClass) 기반 UI 동적 조립
     */
    updateSkillButton(userPlayer) {
        if (!this.elSkillBtn || !userPlayer) return;

        if (!userPlayer.hasActiveSkill) {
            this.elSkillBtn.classList.add('hidden');
            return;
        }

        this.elSkillBtn.classList.remove('hidden');

        // 캐릭터 아이콘 및 테마 색상 적용
        if (this.elSkillIcon && userPlayer.skillIconClass) {
            this.elSkillIcon.className = `${userPlayer.skillIconClass} text-base mb-0.5`;
        }
        this.elSkillBtn.style.borderColor = userPlayer.themeColor;
        this.elSkillBtn.style.color = userPlayer.themeColor;

        if (!this.elSkillFill || !this.elSkillText) return;

        // 게이지 비율 동적 산출 (70, 50, 100 등)
        const ratio = Math.min(1.0, userPlayer.gauge / userPlayer.maxGauge);
        const percent = Math.floor(ratio * 100);

        this.elSkillFill.style.height = `${percent}%`;
        this.elSkillFill.style.backgroundColor = userPlayer.themeColor;
        this.elSkillText.innerText = `${percent}%`;

        if (percent >= 100) {
            this.elSkillBtn.classList.add('animate-bounce');
        } else {
            this.elSkillBtn.classList.remove('animate-bounce');
        }
    }

    /**
     * HUD 타이머 및 팀 점수 표기 갱신
     * @param {number} timeRemaining 
     * @param {number} score 
     */
    updateHeader(timeRemaining, score) {
        if (this.elTimer) {
            const m = Math.floor(Math.max(0, timeRemaining) / 60).toString().padStart(2, '0');
            const s = (Math.floor(Math.max(0, timeRemaining)) % 60).toString().padStart(2, '0');
            this.elTimer.innerText = `${m}:${s}`;
        }
        if (this.elTeamScore) {
            this.elTeamScore.innerText = Math.floor(score).toString().padStart(6, '0');
        }
    }

    /**
     * 슬롯 제어 버튼 및 실시간 딜량/실수 통계 렌더링
     * @param {Array} slots 
     */
    updateSlotAndStats(slots) {
        if (!this.elSlotContainer || !this.elLiveStats) return;

        // 1. 슬롯 제어 UI (유저 난입 / AI 제어 토글)
        this.elSlotContainer.innerHTML = '';
        slots.forEach((slot) => {
            const btn = document.createElement('button');
            btn.className = `p-1.5 rounded-lg text-left border transition ${
                slot.isHuman 
                    ? 'bg-cyan-950 border-cyan-400 text-cyan-200 hover:bg-cyan-900' 
                    : 'bg-slate-800 border-slate-700 text-gray-300 hover:bg-slate-700'
            }`;

            btn.innerHTML = `
                <div class="flex justify-between items-center">
                    <span class="font-bold text-[10px]" style="color: ${slot.color}">SLOT ${slot.id}</span>
                    <span class="text-[8px] px-1 rounded ${slot.isHuman ? 'bg-cyan-500 text-black font-extrabold' : 'bg-gray-700 text-gray-300'}">
                        ${slot.isHuman ? 'USER' : 'AI'}
                    </span>
                </div>
                <span class="text-[9px] text-gray-400 block mt-0.5">${slot.isHuman ? 'AI로 전환' : '유저 난입'}</span>
            `;

            btn.onclick = () => {
                slot.isHuman = !slot.isHuman;
                if (this.callbacks.onSlotToggle) {
                    this.callbacks.onSlotToggle(slot);
                }
                this.updateSlotAndStats(slots);
            };
            this.elSlotContainer.appendChild(btn);
        });

        // 2. 실시간 딜량 & AI 실수 랭킹 집계
        this.elLiveStats.innerHTML = '';
        slots.forEach((s) => {
            const row = document.createElement('div');
            row.className = "bg-slate-950 p-1.5 rounded border border-slate-800 flex justify-between items-center text-[10px]";
            row.innerHTML = `
                <div class="flex items-center gap-1.5">
                    <span class="font-bold" style="color: ${s.color}">P${s.id} [${s.isHuman ? 'USER' : 'AI'}]</span>
                </div>
                <div class="text-right">
                    <span class="text-cyan-300 font-bold">${Math.floor(s.damageDealt).toLocaleString()} DMG</span>
                    ${!s.isHuman ? `<span class="text-pink-400 font-bold ml-1.5">(${s.mistakesCount} 실수)</span>` : ''}
                </div>
            `;
            this.elLiveStats.appendChild(row);
        });
    }

    /**
     * 경기 종료 후 최종 스코어보드 모달 표시
     * @param {Array} slots 
     */
    showGameOverModal(slots) {
        if (!this.elScoreboardList || !this.elModal) return;

        this.elScoreboardList.innerHTML = '';
        const sorted = [...slots].sort((a, b) => b.damageDealt - a.damageDealt);

        sorted.forEach((s, idx) => {
            const row = document.createElement('div');
            row.className = "flex justify-between items-center p-2 rounded bg-slate-900 border border-slate-800";
            row.innerHTML = `
                <div class="flex items-center gap-2">
                    <span class="font-bold text-gray-500">${idx + 1}.</span>
                    <span class="font-bold" style="color: ${s.color}">SLOT ${s.id} (${s.isHuman ? '유저' : 'AI 봇'})</span>
                </div>
                <div class="text-right">
                    <span class="text-cyan-300 font-bold">${Math.floor(s.damageDealt).toLocaleString()} DMG</span>
                    <span class="text-pink-400 text-[10px] ml-2">(${s.mistakesCount} 실수)</span>
                </div>
            `;
            this.elScoreboardList.appendChild(row);
        });

        this.elModal.classList.remove('hidden');
    }
}
```

# 📄 [요청 1 ➡️ 불러온함수 (SceneManager 본체)] TARGET: extraction_target_project/js/core/sceneManager.js (13-80라인)
# ----------------------------------------------------------
```python
export class SceneManager {
    /**
     * @param {object} options 
     * @param {Function} [options.onStateChange] 상태 변경 콜백
     */
    constructor(options = {}) {
        this.currentState = GameState.MENU; // 메인 로비(MENU)에서 시작
        this.onStateChange = options.onStateChange || null;
    }

    /**
     * 현재 상태 확인
     * @returns {string} GameState
     */
    getState() {
        return this.currentState;
    }

    /**
     * 상태 변경
     * @param {string} nextState 
     * @param {any} payload 
     */
    setState(nextState, payload = null) {
        if (this.currentState === nextState) return;
        const prevState = this.currentState;
        this.currentState = nextState;

        console.log(`[SceneManager] Scene Changed: ${prevState} -> ${nextState}`);

        // 화면 DOM 엘리먼트 가시성 토글
        const menuScreen = document.getElementById('menu-screen');
        const uiLayer = document.getElementById('ui-layer');
        const resultScreen = document.getElementById('result-screen');

        if (menuScreen) menuScreen.style.display = (nextState === GameState.MENU) ? 'flex' : 'none';
        if (uiLayer) uiLayer.style.display = (nextState === GameState.PLAY) ? 'flex' : 'none';
        if (resultScreen) {
            if (nextState === GameState.GAMEOVER) {
                resultScreen.classList.remove('hidden');
                resultScreen.style.display = 'flex';
            } else {
                resultScreen.classList.add('hidden');
                resultScreen.style.display = 'none';
            }
        }

        if (this.onStateChange) {
            this.onStateChange(nextState, prevState, payload);
        }
    }

    /**
     * 게임 플레이 상태인지 확인
     * @returns {boolean}
     */
    isPlaying() {
        return this.currentState === GameState.PLAY;
    }

    /**
     * 게임 종료 상태인지 확인
     * @returns {boolean}
     */
    isGameOver() {
        return this.currentState === GameState.GAMEOVER;
    }
}
```

# 📄 [요청 2] TARGET: js/network/networkManager.js (1-116라인)
# ----------------------------------------------------------
```python
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
```

# 📄 [요청 3] TARGET: server.js (1-112라인)
# ----------------------------------------------------------
```python
/**
 * server.js
 * 방장(Host) 노트북 전용 Node.js 웹소켓 & 정적 파일 서버
 * 
 * [실행 방법]
 * 1. 터미널/CMD 열기: npm install ws express
 * 2. 서버 실행: node server.js
 */

const { execSync } = require('child_process');
const path = require('path');
const os = require('os');

// 💡 [자동 라이브러리 감지 & 설치 구역]
function ensureModule(moduleName) {
    try {
        return require(moduleName);
    } catch (e) {
        console.log(`📦 [Auto Setup] 필수 모듈 '${moduleName}'을(를) 찾을 수 없습니다. 자동으로 설치 중...`);
        execSync(`npm install ${moduleName}`, { stdio: 'inherit' });
        return require(moduleName);
    }
}

const express = ensureModule('express');
const WebSocket = ensureModule('ws');
const http = require('http');

const app = express();
const PORT = 3000;
const WS_PORT = 8080;

const fs = require('fs');

// 💡 [실행 경로 자동 추적]: 어느 위치에서 실행되어도 extraction_target_project 내부 경로 자동 조준
let targetStaticPath = __dirname;

if (fs.existsSync(path.join(__dirname, 'extraction_target_project'))) {
    targetStaticPath = path.join(__dirname, 'extraction_target_project');
} else if (fs.existsSync(path.join(__dirname, 'AI_agent', 'extraction_target_project'))) {
    targetStaticPath = path.join(__dirname, 'AI_agent', 'extraction_target_project');
}

app.use(express.static(targetStaticPath));
console.log(`📂 [Static Directory] 게임 정적 경로 자동 로드 완료: ${targetStaticPath}`);

const server = http.createServer(app);

// 웹소켓 서버 인스턴스 생성 (포트 8080)
const wss = new WebSocket.Server({ port: WS_PORT });

// 현재 호스트 노트북의 로컬 IP 주소 추출
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
console.log(`🚀 [Bullet Hell Host Server] 오프라인 LAN 서버 가동 중`);
console.log(`📱 폰/클라이언트 접속 주소: http://${localIp}:${PORT}?client=true`);
console.log(`⚡ 웹소켓 포트: ${WS_PORT}`);
console.log('====================================================');

// 연결된 모든 클라이언트 패킷 중계 및 슬롯 관리
const connectedSlots = {}; // { wsId: slotIndex }

wss.on('connection', (ws) => {
    // 1~4 중 사용 가능한 빈 슬롯 찾기
    const assignedSlots = Object.values(connectedSlots);
    let mySlot = 1;
    for (let i = 1; i <= 4; i++) {
        if (!assignedSlots.includes(i)) {
            mySlot = i;
            break;
        }
    }
    const socketId = Math.random();
    ws.socketId = socketId;
    ws.slotIndex = mySlot;
    connectedSlots[socketId] = mySlot;

    console.log(`🌐 [WebSocket] 노드 연결됨 - 슬롯 P${mySlot} 할당`);

    // 새로 들어온 클라이언트에게 할당된 슬롯 전달
    ws.send(JSON.stringify({ type: 'SLOT_ASSIGNED', slotIndex: mySlot }));

    // 접속한 전원에게 현재 연결된 슬롯 상태 전파
    const sendRoomState = () => {
        const activeSlots = Object.values(connectedSlots);
        const payload = JSON.stringify({ type: 'ROOM_STATE', activeSlots });
        wss.clients.forEach(c => {
            if (c.readyState === WebSocket.OPEN) c.send(payload);
        });
    };
    sendRoomState();

    ws.on('message', (message) => {
        // 💡 송신자를 포함한 연결된 모든 클라이언트 노드에 조작 및 방 상태 공유
        wss.clients.forEach((client) => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(message.toString());
            }
        });
```

# 📄 [요청 3 ➡️ 불러온함수 (ensureModule 본체)] TARGET: extraction_target_project/server.js (15-23라인)
# ----------------------------------------------------------
```python
function ensureModule(moduleName) {
    try {
        return require(moduleName);
    } catch (e) {
        console.log(`📦 [Auto Setup] 필수 모듈 '${moduleName}'을(를) 찾을 수 없습니다. 자동으로 설치 중...`);
        execSync(`npm install ${moduleName}`, { stdio: 'inherit' });
        return require(moduleName);
    }
}
```

# 📄 [요청 3 ➡️ 불러온함수 (sendRoomState 본체)] TARGET: extraction_target_project/server.js (97-103라인)
# ----------------------------------------------------------
```python
    const sendRoomState = () => {
        const activeSlots = Object.values(connectedSlots);
        const payload = JSON.stringify({ type: 'ROOM_STATE', activeSlots });
        wss.clients.forEach(c => {
            if (c.readyState === WebSocket.OPEN) c.send(payload);
        });
    };
```

# 📄 [요청 3 ➡️ 불러온함수 (getLocalIpAddress 본체)] TARGET: extraction_target_project/server.js (53-63라인)
# ----------------------------------------------------------
```python
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
```

# 📄 [요청 4] TARGET: js/core/gameLoop.js (1-250라인)
# ----------------------------------------------------------
```python
/**
 * js/core/gameLoop.js
 * 메인 60fps requestAnimationFrame 루프, 충돌 판정, AI 시각화 및 렌더링 결합
 */
import { TOTAL_SLOTS, MATCH_CONFIG, CANVAS_GRID_SIZE } from '../config/constants.js';
import { PlayerFactory } from '../player/playerFactory.js';
import { BossFactory } from '../enemy/bossFactory.js';
import { AIEngine } from '../ai/aiEngine.js';
import { createImpactParticles, createFloatingText } from '../player/particle.js';
import { setGameSeed } from '../utils/math.js';
import { GameState } from './sceneManager.js';
import { sendScoreToServer } from '../network/scoreSender.js';

export class GameLoop {
    /**
     * @param {HTMLCanvasElement} canvas 
     * @param {CanvasRenderingContext2D} ctx 
     * @param {import('./sceneManager.js').SceneManager} sceneManager 
     * @param {import('./input.js').InputHandler} input 
     * @param {import('./ui.js').UIManager} ui 
     */

    
    constructor(canvas, ctx, sceneManager, input, ui, options = {}) {
        this.canvas = canvas;
        this.ctx = ctx;
        this.sceneManager = sceneManager;
        this.input = input;
        this.ui = ui;

        this.showAIDebug = false; // 기본 NORMAL 모드 (디버그 오버레이 비활성화)
        this.lastTimestamp = performance.now();

        // 전역 참조 등록
        window.gameLoopInstance = this;

        // 멀티플레이 시드 바인딩 (서버 수신 시드 사용, 없을 경우 고정 시드 1004)
        this.matchSeed = (options && options.seed) || window.selectedMatchSeed || 1004;
        setGameSeed(this.matchSeed);

        // 매치 상태 데이터
        this.matchState = {
            timeRemaining: MATCH_CONFIG.DEFAULT_DURATION_SEC,
            teamScore: 0
        };

        // 메뉴 드롭다운에서 선택된 직업(bufferPlayer, defaultPlayer 등)을 읽어와 슬롯 초기화
        this.initSlots();
        this.boss = BossFactory.createBoss('neonDragon', this.canvas.width / 2, 150);
        this.playerBullets = [];
        this.bossBullets = [];
        this.minionBullets = []; // 전역 미니언 탄환 배열
        this.enemyMinions = [];  // 적군 미니언 엔티티 배열
        this.allyMinions = [];   // 아군 미니언 엔티티 배열
        this.particles = [];
        this.floatingTexts = [];

        // 💡 [UI 스킬 버튼 바인딩 연동]
        if (this.ui && typeof this.ui.bindSkillButton === 'function') {
            this.ui.bindSkillButton(() => this.slots.find(s => s.isHuman), this);
        }

        this.init();
    }

    /**
     * 💡 [유저 스킬 시전 처리 메서드 - E키 및 UI 전용]
     */
    useUserSkill() {
        const userSlot = this.slots.find(s => s.isHuman && !s.isStunned());
        if (!userSlot || !userSlot.hasActiveSkill) return;

        const allEnemyBullets = [...this.bossBullets, ...this.minionBullets];
        const success = userSlot.useSkill({
            boss: this.boss,
            enemyMinions: this.enemyMinions,
            bossBullets: this.bossBullets,
            minionBullets: this.minionBullets,
            enemyBullets: allEnemyBullets,
            allyMinions: this.allyMinions,
            allyPlayers: this.slots
        });

        if (success) {
            this.floatingTexts.push(createFloatingText(userSlot.x, userSlot.y - 20, userSlot.skillFloatText, userSlot.themeColor));
        }
    }

    /**
     * 메인 프레임 업데이트 중 유저 입력 처리 연동 (네트워크 동기화 포함)
     */
    updateInputs() {
        const localInputAction = this.input.getInputAction();
        const net = window.networkManager;

        // 1. 내 컴퓨터 슬롯 조작 신호를 네트워크 소켓으로 송신
        if (net && net.mySlotIndex) {
            net.sendClientInput(net.mySlotIndex, localInputAction);
        }

        // 2. 각 슬롯별 입력 처리 (내 슬롯 = 내 조작, 타 컴퓨터 = 수신된 원격 조작)
        this.slots.forEach((player, idx) => {
            const slotNum = idx + 1;
            const isMySlot = (net && net.mySlotIndex === slotNum);
            
            // 네트워크 수신 입력이 존재하면 꺼내오기
            const remoteInput = net ? net.consumeClientInput(slotNum) : null;
            const inputPacket = isMySlot ? localInputAction : (remoteInput || player.remoteInputPacket);

            if (player.isHuman || remoteInput) {
                const allEnemyBullets = [
                    ...(this.bossBullets || []),
                    ...(this.minionBullets || [])
                ];

                const skillParams = {
                    boss: this.boss,
                    enemyMinions: this.enemyMinions,
                    bossBullets: this.bossBullets,
                    minionBullets: this.minionBullets,
                    enemyBullets: allEnemyBullets,
                    allyMinions: this.allyMinions,
                    allyPlayers: this.slots
                };

                if (inputPacket && inputPacket.useSkill && typeof player.useSkill === 'function') {
                    const success = player.useSkill(skillParams);
                    if (success && Array.isArray(this.floatingTexts)) {
                        this.floatingTexts.push(createFloatingText(
                            player.x, 
                            player.y - 20, 
                            player.skillFloatText || 'SKILL ACTIVATED!', 
                            player.themeColor || '#10b981'
                        ));
                    }
                }

                if (inputPacket) {
                    player.handleHumanInputPacket(inputPacket, skillParams);
                }
            }
        });
    }

    /**
     * 메인 메뉴의 드롭다운 선택값(p1-class ~ p4-class)을 읽어서 각 슬롯 기체를 동적으로 생성
     */
    initSlots() {
        const mySlot = (window.networkManager && window.networkManager.mySlotIndex) ? window.networkManager.mySlotIndex : 1;

        this.slots = Array.from({ length: TOTAL_SLOTS }, (_, i) => {
            const slotId = i + 1;
            const classSelect = document.getElementById(`p${slotId}-class`);
            const classType = classSelect ? classSelect.value : 'defaultPlayer';
            
            const player = PlayerFactory.createPlayer(i, classType);
            
            // 접속자가 실제 존재하는 슬롯이며, 내 컴퓨터의 슬롯일 때만 유저(Human) 조작으로 설정
            player.isHuman = (slotId === mySlot);
            return player;
        });

        if (this.canvas) {
            this.slots.forEach(slot => slot.resetPosition(this.canvas.width, this.canvas.height, TOTAL_SLOTS));
        }
        if (this.ui) {
            this.ui.updateSlotAndStats(this.slots);
        }
    }

    /**
     * 엔티티 초기 위치 및 타이머 루프 시작
     */
    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());

        // 초당 매치 타이머 및 주기 점수 증가
        this.timerInterval = setInterval(() => {
            if (!this.sceneManager.isPlaying()) return;

            this.matchState.timeRemaining--;
            this.matchState.teamScore += MATCH_CONFIG.SCORE_PER_TICK;
            this.ui.updateHeader(this.matchState.timeRemaining, this.matchState.teamScore);

            if (this.matchState.timeRemaining <= 0) {
                this.endMatch();
            }
        }, 1000);

        this.ui.updateSlotAndStats(this.slots);
    }

    /**
     * 캔버스 리사이즈 및 슬롯 좌표 재정렬
     */
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.slots.forEach(slot => slot.resetPosition(this.canvas.width, this.canvas.height, TOTAL_SLOTS));
    }

    /**
     * 유저 조작 슬롯의 액티브 스킬 발동 트리거 (조작 키 및 위치 타겟 전달)
     */
    useUserSkill() {
        const humanSlot = this.slots.find(s => s.isHuman && !s.isStunned());
        if (humanSlot && humanSlot.hasActiveSkill && humanSlot.gauge >= humanSlot.maxGauge) {
            const success = humanSlot.useSkill({
                keys: this.input.keys,
                mousePos: this.input.mousePos,
                boss: this.boss,
                enemyMinions: this.enemyMinions
            });
            if (success) {
                this.floatingTexts.push(createFloatingText(humanSlot.x, humanSlot.y - 20, humanSlot.skillFloatText, humanSlot.themeColor));
            }
        }
    }

    /**
     * EMP 특수폭탄 발동 (전 화면 보스 탄막 소거)
     */
    useBomb() {
        this.bossBullets = [];
        createImpactParticles(this.particles, this.canvas.width / 2, this.canvas.height / 2, '#ec4899', 30);
    }

    /**
     * 매치 종료 및 서버 랭킹 전송
     */
    endMatch() {
        this.sceneManager.setState(GameState.GAMEOVER);
        clearInterval(this.timerInterval);

        this.ui.showGameOverModal(this.slots);

        // Wi-Fi 랭킹 서버로 결과 비동기 전송
        sendScoreToServer({
            score: this.matchState.teamScore,
            slotsStats: this.slots.map(s => ({
                id: s.id,
                isHuman: s.isHuman,
                damageDealt: s.damageDealt,
                mistakesCount: s.mistakesCount
            }))
        });
    }

    /**
```

# 📄 [요청 4 ➡️ 불러온함수 (setGameSeed 본체)] TARGET: extraction_target_project/js/utils/math.js (17-21라인)
# ----------------------------------------------------------
```python
export function setGameSeed(seed) {
    currentSeed = seed;
    // 전역 Math.random()을 시드 기반 난수 함수로 덮어씌움 (기존 모든 Math.random 자동 동기화)
    Math.random = seededRandom;
}
```

# 📄 [요청 4 ➡️ 불러온함수 (createFloatingText 본체)] TARGET: extraction_target_project/js/player/particle.js (71-81라인)
# ----------------------------------------------------------
```python
export function createFloatingText(x, y, text, color = '#ec4899') {
    return {
        x,
        y,
        text,
        color,
        alpha: 1.0,
        vy: -1.5,
        life: 1.0
    };
}
```

# 📄 [요청 4 ➡️ 불러온함수 (sendScoreToServer 본체)] TARGET: extraction_target_project/js/network/scoreSender.js (16-49라인)
# ----------------------------------------------------------
```python
export async function sendScoreToServer(payload) {
    const targetUrl = payload.serverUrl || SERVER_CONFIG.DEFAULT_LEADERBOARD_URL;

    const bodyData = {
        game: SERVER_CONFIG.GAME_NAME,
        score: Math.floor(payload.score || 0),
        nickname: payload.nickname || 'Pilot-01',
        playedAt: new Date().toISOString(),
        details: payload.slotsStats || []
    };

    try {
        const response = await fetch(targetUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bodyData)
        });

        if (!response.ok) {
            console.warn(`[ScoreSender] 랭킹 서버 전송 상태 코드: ${response.status}`);
            return { success: false, status: response.status };
        }

        const data = await response.json().catch(() => ({ success: true }));
        console.log('[ScoreSender] 랭킹 전송 성공:', data);
        return { success: true, data };
    } catch (error) {
        // 네트워크 연결 불가 환경(오프라인 / 로컬 단독 시연 등)에서도 게임 흐름이 끊기지 않도록 방어
        console.warn('[ScoreSender] 랭킹 서버 연결 실패 (로컬 모드 진행):', error.message);
        return { success: false, error: error.message };
    }
}
```
