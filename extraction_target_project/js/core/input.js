/**
 * js/core/input.js
 * 키보드, 마우스, 모바일 터치 가상 조이스틱 핸들러 및 네트워크 입력 제어기
 * 
 * [동작 명세]
 * 1. WASD/조이스틱/스페이스바 입력을 정제하여 네트워크 패킷(moveX, moveY, useSkill, timeStamp) 형태로 압축 전송.
 * 2. 이벤트 리스너 참조 시점 문제 해결 (Lazy Evaluation): this.networkManager || window.networkManager 실시간 탐색.
 * 3. 1회성 스킬 트리거 시 timeStamp 부여 및 전달.
 */
export class InputHandler {
    constructor() {
        this.keys = {};
        const canvas = document.getElementById('gameCanvas');
        this.mousePos = {
            x: canvas ? canvas.width / 2 : window.innerWidth / 2,
            y: canvas ? canvas.height / 2 : window.innerHeight / 2
        };
        this.joystick = {
            active: false,
            pointerId: null,
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

    logLocalInput(action, posX, posY) {
        const net = this.getNetworkManager();
        const slot = net && net.mySlotIndex ? net.mySlotIndex : 1;
        console.log(`[LOCAL_INPUT] Slot P${slot} | Key: ${action} | Pos: (${posX ?? 'n/a'}, ${posY ?? 'n/a'})`);
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
                const player = window.gameLoopInstance?.slots?.[(this.getNetworkManager()?.mySlotIndex || 1) - 1];
                this.logLocalInput(e.code, player?.x, player?.y);
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
            const canvas = window.gameLoopInstance?.canvas || document.getElementById('gameCanvas');
            if (!canvas) return;
            const bounds = canvas.getBoundingClientRect();
            if (bounds.width <= 0 || bounds.height <= 0) return;
            this.mousePos.x = (e.clientX - bounds.left) * canvas.width / bounds.width;
            this.mousePos.y = (e.clientY - bounds.top) * canvas.height / bounds.height;
        });

        window.addEventListener('mousedown', (e) => {
            // 💡 [Lazy Evaluation]
            const net = this.getNetworkManager();

            if (e.button === 2) {
                this.skillTriggered = true;
                this.lastSkillTriggerTime = Date.now();
                const player = window.gameLoopInstance?.slots?.[(this.getNetworkManager()?.mySlotIndex || 1) - 1];
                this.logLocalInput('RightClick', player?.x, player?.y);
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('MOUSE', 'Right Click (Skill Trigger)');
                }
            } else if (e.button === 0) {
                // UI 버튼 요소와 캔버스 구분
                const target = e.target;
                const isButton = target && (target.tagName === 'BUTTON' || target.closest('button'));
                const clickType = isButton ? `UI Button Click [${target.id || target.innerText || 'BTN'}]` : `Canvas Field Click (X:${e.clientX}, Y:${e.clientY})`;

                const player = window.gameLoopInstance?.slots?.[(this.getNetworkManager()?.mySlotIndex || 1) - 1];
                this.logLocalInput(clickType, player?.x, player?.y);
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

        joystickZone.style.touchAction = 'none';
        joystickKnob.style.pointerEvents = 'none';

        const updateJoystick = (clientX, clientY) => {
            const rect = joystickZone.getBoundingClientRect();
            this.joystick.startX = rect.left + rect.width / 2;
            this.joystick.startY = rect.top + rect.height / 2;
            const dx = clientX - this.joystick.startX;
            const dy = clientY - this.joystick.startY;
            const dist = Math.hypot(dx, dy);
            const maxDist = 35;

            const angle = Math.atan2(dy, dx);
            const intensity = Math.min(dist, maxDist);

            this.joystick.moveX = Math.cos(angle) * (intensity / maxDist);
            this.joystick.moveY = Math.sin(angle) * (intensity / maxDist);

            const knobX = Math.cos(angle) * intensity;
            const knobY = Math.sin(angle) * intensity;
            joystickKnob.style.transform = `translate(${knobX}px, ${knobY}px)`;
        };

        joystickZone.addEventListener('pointerdown', (e) => {
            if (this.joystick.active || (e.pointerType === 'mouse' && e.button !== 0)) return;
            this.joystick.active = true;
            this.joystick.pointerId = e.pointerId;
            joystickZone.setPointerCapture(e.pointerId);
            updateJoystick(e.clientX, e.clientY);
            e.preventDefault();
        });

        joystickZone.addEventListener('pointermove', (e) => {
            if (!this.joystick.active || e.pointerId !== this.joystick.pointerId) return;
            updateJoystick(e.clientX, e.clientY);
            e.preventDefault();
        });

        const endJoystick = (e) => {
            if (e.pointerId !== this.joystick.pointerId) return;
            this.joystick.active = false;
            this.joystick.pointerId = null;
            this.joystick.moveX = 0;
            this.joystick.moveY = 0;
            joystickKnob.style.transform = `translate(0px, 0px)`;
        };

        joystickZone.addEventListener('pointerup', endJoystick);
        joystickZone.addEventListener('pointercancel', endJoystick);
        joystickZone.addEventListener('lostpointercapture', endJoystick);
    }

    /**
     * AI 상태에서 사용할 입력 액션을 난수 소비 없이 생성
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
                const baseAngle = Math.atan2(dy, dx);
                moveX = Math.cos(baseAngle);
                moveY = Math.sin(baseAngle);
            }

            const boss = (context && context.boss) || (window.gameLoopInstance && window.gameLoopInstance.boss);
            if (boss) {
                mouseX = boss.x;
                mouseY = boss.y;
            }
        }

        const inputAction = {
            moveX,
            moveY,
            dx: moveX,
            dy: moveY,
            mouseX,
            mouseY,
            useSkill,
            timeStamp: Date.now()
        };
        return inputAction;
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
            // 조이스틱 미세 오차 보정 및 안전 정규화
            const jLen = Math.hypot(this.joystick.moveX, this.joystick.moveY);
            if (jLen > 0.05) {
                moveX = this.joystick.moveX / (jLen > 1 ? jLen : 1);
                moveY = this.joystick.moveY / (jLen > 1 ? jLen : 1);
            }
        }

        const useSkill = this.skillTriggered;
        const skillTime = useSkill ? (this.lastSkillTriggerTime || Date.now()) : Date.now();
        this.skillTriggered = false;
        if (useSkill) this.lastSkillTriggerTime = 0;

        const myPlayer = (context && context.player) || 
            (window.gameLoopInstance && window.gameLoopInstance.slots && window.gameLoopInstance.slots[slotIndex]);

        const inputAction = {
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

        return inputAction;
    }
}

export default InputHandler;
