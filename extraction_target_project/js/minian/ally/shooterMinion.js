/**
 * js/minian/ally/shooterMinion.js
 * 1호: 원거리 궤도 드론
 * 스펙: 무적 판정, 플레이어 연사속도 1/10, AI 오차 조준, 플레이어 기절 시 소멸
 */
import BaseAllyMinion from './baseAllyMinion.js';
import { rngMinion } from '../../utils/seededRNG.js';

export class ShooterMinion extends BaseAllyMinion {
    constructor(owner, orbitAngleOffset = 0) {
        super(owner, {
            radius: 9,
            hp: 9999, // 무적
            maxHp: 9999,
            color: '#34d399',
            fireRate: 2.0 // 공속 1/10 수준
        });

        this.orbitAngleOffset = orbitAngleOffset;
        this.orbitRadius = 42;
    }

    updateMovement(enemyEntities, dt) {
        super.updateMovement(enemyEntities, dt);
        if (this.isDead || !this.owner) return;

        const time = (window.gameLoopInstance?.gameTime ?? 0) * 2;
        const targetX = this.owner.x + Math.cos(time + this.orbitAngleOffset) * this.orbitRadius;
        const targetY = this.owner.y + Math.sin(time + this.orbitAngleOffset) * this.orbitRadius;

        const blend = 1 - Math.pow(0.9, dt * 60);
        this.x += (targetX - this.x) * blend;
        this.y += (targetY - this.y) * blend;
    }

    updateAttack(enemyEntities = [], allyBullets = [], dt = 0.016) {
        if (this.isDead) return;

        this.attackTimer += dt;

        if (this.attackTimer >= this.fireRate) {
            const target = this.findClosestTarget(enemyEntities);
            if (target) {
                this.shoot(target, allyBullets);
                this.attackTimer = 0;
            }
        }
    }

    shoot(target, allyBullets) {
        // AI 특유의 오차 조준 (±0.3 라디안) - 미니언 공격 독립 PRNG 적용
        const baseAngle = Math.atan2(target.y - this.y, target.x - this.x);
        const aimError = (rngMinion.attack() - 0.5) * 0.6;
        const finalAngle = baseAngle + aimError;

        const bulletSpeed = 350;

        allyBullets.push({
            x: this.x,
            y: this.y,
            vx: Math.cos(finalAngle) * bulletSpeed,
            vy: Math.sin(finalAngle) * bulletSpeed,
            radius: 3.5,
            damage: 3,
            color: '#a7f3d0',
            isAlly: true,
            isDead: false,
            update(slots, dt) {
                this.x += this.vx * dt;
                this.y += this.vy * dt;
            },
            draw(ctx) {
                ctx.save();
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.shadowColor = '#34d399';
                ctx.shadowBlur = 8;
                ctx.fill();
                ctx.restore();
            }
        });
    }

    draw(ctx) {
        if (this.isDead) return;

        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate((window.gameLoopInstance?.gameTime ?? 0) * 4);
        ctx.strokeStyle = '#34d399';
        ctx.lineWidth = 1.5;
        ctx.shadowColor = '#059669';
        ctx.shadowBlur = 10;

        ctx.beginPath();
        ctx.moveTo(0, -this.radius);
        ctx.lineTo(this.radius * 0.8, this.radius * 0.8);
        ctx.lineTo(-this.radius * 0.8, this.radius * 0.8);
        ctx.closePath();
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(0, 0, 2.5, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.fill();

        ctx.restore();
    }
}

export default ShooterMinion;
