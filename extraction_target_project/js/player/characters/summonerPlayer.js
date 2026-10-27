/**
 * js/player/characters/summonerPlayer.js
 * 서머너 전용 클래스 (스펙: 무적 드론 + 관성 유도 탱커 버서커 2마리 동시 소환)
 */
import BasePlayer from '../basePlayer.js';
import ShooterMinion from '../../minian/ally/shooterMinion.js';
import BerserkerMinion from '../../minian/ally/berserkerMinion.js';

export class SummonerPlayer extends BasePlayer {
    constructor(slotIndex) {
        super(slotIndex, 'summonerPlayer');

        this.className = '서머너 (Summoner)';
        this.themeColor = '#10b981';
        this.hasActiveSkill = true;
        this.skillIconClass = 'fa-solid fa-robot';
        this.skillName = 'SUMMON ALL';
        this.skillFloatText = 'BERSERKERS & DRONE SUMMONED!';

        this.maxGauge = 120;
    }

    /**
     * 게이지 120 소모 시 무적 드론 1마리 + 탱커 버서커 2마리 동시 소환
     */
    useSkill(context = {}) {
        if (!super.useSkill(context)) return false;

        if (context.allyMinions && Array.isArray(context.allyMinions)) {
            // 1. 원거리 무적 궤도 드론 1마리 소환
            context.allyMinions.push(new ShooterMinion(this, 0));

            // 2. 스폰 위치 중첩 방지 (좌/우 35px 오프셋)
            const leftX = Math.max(20, this.x - 35);
            const rightX = Math.min(580, this.x + 35);

            context.allyMinions.push(new BerserkerMinion(this, leftX, this.y));
            context.allyMinions.push(new BerserkerMinion(this, rightX, this.y));
        }

        return true;
    }

    draw(ctx, allyPlayers = []) {
        super.draw(ctx, allyPlayers);

        if (!this.isStunned()) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(Date.now() * 0.002);
            ctx.strokeStyle = this.themeColor;
            ctx.lineWidth = 1.5;

            ctx.beginPath();
            for (let i = 0; i < 3; i++) {
                const a = (Math.PI * 2 / 3) * i;
                const hx = Math.cos(a) * 12;
                const hy = Math.sin(a) * 12;
                if (i === 0) ctx.moveTo(hx, hy);
                else ctx.lineTo(hx, hy);
            }
            ctx.closePath();
            ctx.stroke();

            ctx.restore();
        }
    }
}

export default SummonerPlayer;