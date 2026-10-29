/** 네크로맨서 본체의 미구현 더미. */
import BaseBoss from '../../baseBoss.js';

export class Necromancer extends BaseBoss {
    constructor(x, y) {
        super(x, y, 25000);
        this.type = 'necromancer';
        this.implemented = false;
        this.color = '#22c55e';
        this.dangerAreas = [];
        this.movementModel = 'neonDragon';
        this.targeting = 'nearestPlayer';
        this.appearance = { body: 'greenCircle', cloak: 'black', staff: 'crescent', orb: 'purple', orbAura: 'purpleSmoke' };
    }

    // 이동과 렌더링은 본 구현 단계에서 연결한다.
    update() {}
    draw(ctx, canvasWidth) {
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#fff';
        ctx.textAlign = 'center';
        ctx.font = '12px sans-serif';
        ctx.fillText('NECROMANCER (DUMMY)', this.x, this.y - this.radius - 8);
        ctx.restore();
        this.drawHpBar(ctx, canvasWidth);
    }
}

export default Necromancer;
