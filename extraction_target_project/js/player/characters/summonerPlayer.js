/**
 * js/player/characters/summonerPlayer.js
 * 서머너 전용 클래스 (스펙: 무적 드론 + 관성 유도 탱커 버서커 2마리 동시 소환)
 * 
 * [Object & HP Sync]:
 * - 미니언 소환 및 생명주기 판정은 소유자(Owner Authority)에서 주도 관리.
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
            const drone = new ShooterMinion(this, 0);
            context.allyMinions.push(drone);

            // 2. 스폰 위치 중첩 방지 (좌/우 35px 오프셋)
            const leftX = Math.max(20, this.x - 35);
            const rightX = Math.min(1260, this.x + 35);

            const b1 = new BerserkerMinion(this, leftX, this.y);
            const b2 = new BerserkerMinion(this, rightX, this.y);
            context.allyMinions.push(b1);
            context.allyMinions.push(b2);

            // 소유자(Owner)인 경우 OBJECT_STATE_SYNC 브로드캐스트
            if (this.isLocalOwner && window.networkManager) {
                const minionStates = [
                    { id: `drone_${this.slotIndex}_${Date.now()}`, type: 'drone', hp: drone.hp, maxHp: drone.maxHp, x: drone.x, y: drone.y },
                    { id: `b1_${this.slotIndex}_${Date.now()}`, type: 'berserker', hp: b1.hp, maxHp: b1.maxHp, x: b1.x, y: b1.y },
                    { id: `b2_${this.slotIndex}_${Date.now()}`, type: 'berserker', hp: b2.hp, maxHp: b2.maxHp, x: b2.x, y: b2.y }
                ];
                window.networkManager.sendObjectStateSync(this.slotIndex + 1, minionStates);
            }
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
