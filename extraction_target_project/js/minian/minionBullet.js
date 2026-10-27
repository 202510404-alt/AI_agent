/**
 * js/minion/minionBullet.js
 * 미니언 전용 탄환 클래스
 */

export class MinionBullet {
    /**
     * @param {number} x 시작 X
     * @param {number} y 시작 Y
     * @param {number} angle 진행 각도 (라디안)
     * @param {number} speed 탄속
     * @param {string} color 탄환 색상
     * @param {boolean} isAlly 아군 탄환 여부 (true: 보스 공격, false: 플레이어 공격)
     */
    constructor(x, y, angle, speed = 6, color = '#f59e0b', isAlly = false) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.speed = speed;
        this.radius = 3;
        this.color = color;
        this.isAlly = isAlly;
        this.damage = 10;
        this.isDead = false;
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
        ctx.shadowBlur = 6;
        ctx.fill();
    }

    /**
     * 화면 이탈 검사
     * @param {number} width 
     * @param {number} height 
     * @returns {boolean}
     */
    isOutOfBounds(width, height) {
        if (this.isDead) return true;
        return (this.y < -10 || this.x < -10 || this.x > width + 10 || this.y > height + 10);
    }
}

export default MinionBullet;