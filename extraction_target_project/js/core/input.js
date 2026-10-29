/**
 * js/core/input.js
 * 키보드, 마우스, 모바일 터치 가상 조이스틱 핸들러 및 네트워크 입력 제어기
 * 
 * [동작 명세]
 * 1. WASD/조이스틱/스페이스바 입력을 정제하여 네트워크 패킷(moveX, moveY, useSkill, timeStamp) 형태로 압축 전송.
 * 2. 이벤트 리스너 참조 시점 문제 해결 (Lazy Evaluation): this.networkManager || window.networkManager 실시간 탐색.
 * 3. 1회성 스킬 트리거 시 timeStamp 부여 및 전달.
 */
import { rngPlayerAi } from '../utils/seededRNG.js';

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

export default InputHandler;
