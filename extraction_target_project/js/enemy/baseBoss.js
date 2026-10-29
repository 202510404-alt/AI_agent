/**
 * js/enemy/baseBoss.js
 * 모든 보스 몬스터의 공통 기반이 되는 BaseBoss 클래스
 */

export default class BaseBoss {
    /**
     * @param {number} x 초기 위치 X
     * @param {number} y 초기 위치 Y
     * @param {number} maxHp 최대 체력
     */
    constructor(x, y, maxHp = 25000) {
        this.x = x;
        this.y = y;
        this.radius = 42;
        this.maxHp = maxHp;
        this.hp = maxHp;
        this.angle = 0;
        this.patternTimer = 0;
        this.patternTick = 0;
        this.color = '#f43f5e';
    }

    /**
     * 보스 체력 바 렌더링
     * @param {CanvasRenderingContext2D} ctx 
     * @param {number} canvasWidth 
     */
    drawHpBar(ctx, canvasWidth) {
        const barW = 340;
        const barH = 8;
        const barX = canvasWidth / 2 - barW / 2;
        const barY = 65;

        // 배경 슬롯
        ctx.fillStyle = 'rgba(0,0,0,0.6)';
        ctx.fillRect(barX, barY, barW, barH);

        // 현재 체력
        const currentW = Math.max(0, (this.hp / this.maxHp) * barW);
        ctx.fillStyle = this.color;
        ctx.fillRect(barX, barY, currentW, barH);

        // 테두리
        ctx.strokeStyle = this.color;
        ctx.strokeRect(barX, barY, barW, barH);
    }

    /**
     * 보스 피격 데미지 적용
     * @param {number} damage 입을 피해량
     * @returns {boolean} 처치 여부
     */
    takeDamage(damage) {
        this.hp -= damage;
        if (this.hp <= 0) {
            this.hp = this.maxHp; // 처치 시 즉시 체력 회복 및 킬 카운트
            return true;
        }
        return false;
    }
}
