/**
 * js/player/particle.js
 * 전역 충돌 이펙트 파티클 및 화면 상단 플로팅 텍스트 헬퍼
 */

/**
 * 기본 이펙트 파티클 클래스
 */
export class Particle {
    /**
     * @param {number} x 생성 위치 X
     * @param {number} y 생성 위치 Y
     * @param {string} color 파티클 색상
     */
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.vx = (Math.random() - 0.5) * 5;
        this.vy = (Math.random() - 0.5) * 5;
        this.life = 1.0;
        this.decay = Math.random() * 0.04 + 0.02;
    }

    /**
     * 파티클 상태 업데이트
     */
    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.life -= this.decay;
    }

    /**
     * 파티클 렌더링
     * @param {CanvasRenderingContext2D} ctx 
     */
    draw(ctx) {
        ctx.save();
        ctx.globalAlpha = Math.max(0, this.life);
        ctx.beginPath();
        ctx.arc(this.x, this.y, 2.5, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.restore();
    }
}

/**
 * 지정된 좌표에 충돌/피격 파티클 무리를 생성합니다.
 * @param {Array<Particle>} particlesContainer 전역 파티클 배열
 * @param {number} x 
 * @param {number} y 
 * @param {string} color 
 * @param {number} count 
 */
export function createImpactParticles(particlesContainer, x, y, color, count = 6) {
    for (let i = 0; i < count; i++) {
        particlesContainer.push(new Particle(x, y, color));
    }
}

/**
 * 플로팅 텍스트 객체 생성 헬퍼
 * @param {number} x 
 * @param {number} y 
 * @param {string} text 
 * @param {string} color 
 * @returns {object}
 */
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