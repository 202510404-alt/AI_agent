/**
 * js/core/input.js
 * 키보드, 마우스, 모바일 터치 가상 조이스틱 핸들러
 */

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


export default InputHandler;
