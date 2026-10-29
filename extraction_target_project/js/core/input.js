/**
 * js/core/input.js
 * 키보드, 마우스, 모바일 터치 가상 조이스틱 핸들러 및 네트워크 입력 제어기
 * 
 * [동작 명세]
 * 1. WASD/조이스틱/스페이스바 입력을 정제하여 네트워크 패킷(moveX, moveY, useSkill) 형태로 압축 전송.
 * 2. isAiMode === true일 경우 파생된 playerAiSpread 시드 기반의 getAiInputAction() 연산값으로 자동 전환되어 전 클라이언트 동일 보장.
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

        // AI 자율 주행 모드 여부
        this.isAiMode = false;

        this.initKeyboard();
        this.initMouse();
        this.initJoystick();
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
                    e.preventDefault();
                }
                // 💡 [네트워크 매니저 추적]: this.networkManager 우선 참조 후 전역 fallback
                const net = this.networkManager || window.networkManager;
                console.log(`[LOCAL KEY LOG] Key Down: ${e.code}`); // 로컬 콘솔 즉시 출력
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
            const net = this.networkManager || window.networkManager;

            if (e.button === 2) {
                this.skillTriggered = true;
                console.log('[LOCAL MOUSE LOG] Right Click');
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('MOUSE', 'Right Click (Skill Trigger)');
                }
            } else if (e.button === 0) {
                // 💡 [좌클릭 구별]: 클릭 대상이 UI 버튼 요소인지 캔버스인지 구분
                const target = e.target;
                const isButton = target && (target.tagName === 'BUTTON' || target.closest('button'));
                const clickType = isButton ? `UI Button Click [${target.id || target.innerText || 'BTN'}]` : `Canvas Field Click (X:${e.clientX}, Y:${e.clientY})`;

                console.log(`[LOCAL MOUSE LOG] ${clickType}`); // 로컬 콘솔 즉시 출력
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
     * @param {number} slotIndex 
     * @param {object} [context] { player, boss, gameLoop }
     * @returns {{moveX: number, moveY: number, dx: number, dy: number, mouseX: number, mouseY: number, useSkill: boolean}}
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
            // AI FSM에 의해 계산된 targetX, targetY 방향으로 조작 생성
            const dx = (player.targetX || player.x) - player.x;
            const dy = (player.targetY || player.y) - player.y;
            const dist = Math.hypot(dx, dy);

            if (dist > 5) {
                // 파생된 playerAiSpread 시드를 적용한 미세 조향 오차각 부여
                const spreadAngle = (rngPlayerAi.getSpread(slotIndex) - 0.5) * 0.1;
                const baseAngle = Math.atan2(dy, dx) + spreadAngle;
                moveX = Math.cos(baseAngle);
                moveY = Math.sin(baseAngle);
            }

            // 가장 가까운 적(보스)을 향해 마우스 조준점 동기화
            const boss = (context && context.boss) || (window.gameLoopInstance && window.gameLoopInstance.boss);
            if (boss) {
                const aimSpread = (rngPlayerAi.getSpread(slotIndex) - 0.5) * 20;
                mouseX = boss.x + aimSpread;
                mouseY = boss.y + aimSpread;
            }

            // 위급 상황 시 시드 기반 확률적 스킬 시전
            if (player.dodgeFatigue > 0.8 && player.hasActiveSkill && !player.isSkillOnCooldown) {
                useSkill = rngPlayerAi.getSpread(slotIndex) < 0.3;
            }
        }

        return {
            moveX,
            moveY,
            dx: moveX, // 하위 호환
            dy: moveY, // 하위 호환
            mouseX,
            mouseY,
            useSkill
        };
    }

    /**
     * 현재 프레임의 클라이언트 조작 상태 패킷 추출 (압축 및 네트워크 규격 동기화)
     * isAiMode === true일 경우 파생된 playerAiSpread 시드 기반 getAiInputAction()으로 자동 전환
     * @param {number} [slotIndex] 
     * @param {object} [context] 
     * @returns {{moveX: number, moveY: number, dx: number, dy: number, mouseX: number, mouseY: number, useSkill: boolean}}
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

        // 대각선 이동 시 단위 벡터 정규화
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
        this.skillTriggered = false;

        return {
            moveX,
            moveY,
            dx: moveX, // 기존 코드 호환
            dy: moveY, // 기존 코드 호환
            mouseX: this.mousePos.x,
            mouseY: this.mousePos.y,
            useSkill
        };
    }
}

export default InputHandler;
