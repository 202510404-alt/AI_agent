/**
 * js/player/playerBullet.js
 * 플레이어 기체의 기본 탄환 클래스
 */

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