/** 네크로맨서를 보호하는 엘리트 좀비. */
import BaseMinion from '../baseMinion.js';
import { closestPlayer } from '../../enemy/bosses/necromancer/necromancerPattern.js';

export class NecromancerEliteZombie extends BaseMinion {
    constructor(x, y, boss) {
        super(x, y, false, '#166534');
        this.ownerBoss = boss;
        this.radius = 22;
        this.hp = this.maxHp = 800;
        this.moveSpeed = 45;
        this.facingAngle = Math.PI / 2;
        this.contactCooldown = 0;
    }

    takeDamage(amount) {
        const loop = globalThis.window?.gameLoopInstance;
        const net = globalThis.window?.networkManager;
        if (this.isDead || !Number.isFinite(amount) || amount <= 0) return false;
        if (loop?.boss === this.ownerBoss && net?.socket?.readyState === 1 && !loop.isAiAuthority()) return false;
        this.hp = Math.max(0, this.hp - amount);
        this.isDead = this.hp === 0;
        return this.isDead;
    }

    updateMovement(players = [], dt = 1 / 60) {
        if (this.isDead) return;
        this.contactCooldown = Math.max(0, this.contactCooldown - dt);
        const target = closestPlayer(this.x, this.y, players);
        if (!target) return;
        const dx = target.x - this.x;
        const dy = target.y - this.y;
        const distance = Math.hypot(dx, dy);
        if (distance > 0) this.facingAngle = Math.atan2(dy, dx);
        const contactDistance = this.radius + (target.radius || 0);
        if (distance > contactDistance) {
            const step = Math.min(this.moveSpeed * dt, distance - contactDistance);
            this.x += Math.cos(this.facingAngle) * step;
            this.y += Math.sin(this.facingAngle) * step;
        } else if (this.contactCooldown <= 0) {
            if (target.takeDamage?.(1)) this.contactCooldown = 1;
        }
    }

    updateAttack() {}

    draw(ctx) {
        if (this.isDead) return;
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.facingAngle);
        ctx.fillStyle = '#14532d';
        ctx.strokeStyle = '#86efac';
        ctx.lineWidth = 2;
        ctx.shadowColor = '#22c55e';
        ctx.shadowBlur = 10;
        for (const side of [-1, 1]) {
            ctx.beginPath();
            ctx.arc(17, side * 17, 9, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
        }
        ctx.beginPath();
        ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
        ctx.restore();
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(this.x - 24, this.y - this.radius - 12, 48, 5);
        ctx.fillStyle = '#4ade80';
        ctx.fillRect(this.x - 24, this.y - this.radius - 12, 48 * this.hp / this.maxHp, 5);
    }
}
