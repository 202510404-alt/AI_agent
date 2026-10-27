/**
 * js/minian/ally/bannerMinion.js
 * 3호: 깃발 고정형 버퍼
 * 스펙: HP 2, 고정 거점, 넓은 오라 범위 내 아군 틱 회복 속도 1.2배 부여
 */
import BaseAllyMinion from './baseAllyMinion.js';

export class BannerMinion extends BaseAllyMinion {
    constructor(owner) {
        super(owner, {
            radius: 14,
            hp: 2,
            maxHp: 2,
            color: '#f97316'
        });

        this.auraRadius = 130; // 넓은 버프 범위
    }

    updateMovement(enemyEntities = [], dt = 0.016) {
        super.updateMovement(enemyEntities, dt);
        // 이동하지 않고 소환 자리에 딱 박혀서 깃발 역할 수행
    }

    updateAttack(enemyEntities = [], allyBullets = [], dt = 0.016, allyPlayers = []) {
        if (this.isDead) return;

        // 범위 내에 존재하는 아군 플레이어들에게 틱 1.2배 버프 부여
        const targets = Array.isArray(allyPlayers) && allyPlayers.length > 0 ? allyPlayers : [this.owner];

        targets.forEach(p => {
            if (p && typeof p.isStunned === 'function' && !p.isStunned()) {
                const dist = Math.hypot(p.x - this.x, p.y - this.y);
                if (dist <= this.auraRadius) {
                    if (typeof p.addModifier === 'function') {
                        p.addModifier({
                            id: 'banner_tick_buff',
                            targetStat: 'gaugeTickRate',
                            type: 'MULTIPLY',
                            value: 1.2,
                            duration: 0.3
                        });
                    }
                }
            }
        });
    }

    draw(ctx) {
        if (this.isDead) return;

        ctx.save();
        ctx.translate(this.x, this.y);

        // 1. 깃발 순백색(White) 아우라 링
        ctx.beginPath();
        ctx.arc(0, 0, this.auraRadius, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.06)';
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([6, 4]);
        ctx.shadowColor = '#ffffff';
        ctx.shadowBlur = 10;
        ctx.fill();
        ctx.stroke();

        // 2. 깃발 폴대 및 하얀색 네온 깃발 아이콘
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(-4, 12);
        ctx.lineTo(-4, -14);
        ctx.stroke();

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.moveTo(-4, -14);
        ctx.lineTo(12, -8);
        ctx.lineTo(-4, -2);
        ctx.closePath();
        ctx.fill();

        ctx.restore();
    }
}

export default BannerMinion;