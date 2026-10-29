/** 네크로맨서 본체, 독안개와 지팡이 렌더링. */
import BaseBoss from '../../baseBoss.js';
import { updateBossMovement } from '../../bossMovement.js';
import { NecromancerPattern, NECROMANCER_TIMING, closestPlayer } from './necromancerPattern.js';
import { createNecromancerParticles } from './necromancerParticle.js';
import { NecromancerEliteZombie } from '../../../minian/enemy/necromancerEliteZombie.js';

export class Necromancer extends BaseBoss {
    constructor(x, y) {
        super(x, y, 25000);
        this.type = 'necromancer';
        this.implemented = true;
        this.color = '#22c55e';
        this.dangerAreas = [];
        this.movementModel = 'neonDragon';
        this.targeting = 'nearestPlayer';
        this.targetX = x;
        this.targetY = y;
        this.moveTimer = 0;
        this.moveInterval = 3;
        this.moveSpeed = 120;
        this.facingAngle = Math.PI / 2;
        this.elapsed = 0;
        this.zombies = [];
        this.eliteZombies = [-1, 1].map(side => new NecromancerEliteZombie(x + side * 90, y + 65, this));
        this.elitesRegistered = false;
        this.appearance = { body: 'greenCircle', cloak: 'black', staff: 'crescent', orb: 'purple', orbAura: 'purpleSmoke' };
    }

    getOrbPosition() {
        const angle = this.facingAngle;
        return { x: this.x + Math.cos(angle) * 65 - Math.sin(angle) * 23,
            y: this.y + Math.sin(angle) * 65 + Math.cos(angle) * 23 };
    }

    addPoisonMist(x, y) {
        this.dangerAreas.push({ type: 'circle', x, y, radius: 90, isFiring: false,
            elapsed: 0, warningSeconds: 1.5, durationSeconds: 2, nextDamageTick: 0 });
    }

    updatePoisonMist(players, dt) {
        for (let i = this.dangerAreas.length - 1; i >= 0; i--) {
            const area = this.dangerAreas[i];
            area.elapsed += dt;
            area.isFiring = area.elapsed >= area.warningSeconds;
            const activeTime = area.elapsed - area.warningSeconds;
            while (area.isFiring && area.nextDamageTick < 2 && activeTime + 1e-9 >= area.nextDamageTick * (area.durationSeconds / 2)) {
                for (const player of players) {
                    if (player && Math.hypot(player.x - area.x, player.y - area.y) <= area.radius + (player.radius || 0)) {
                        player.takeDamage?.(1);
                    }
                }
                area.nextDamageTick++;
            }
            if (activeTime >= area.durationSeconds) this.dangerAreas.splice(i, 1);
        }
    }

    update(bulletContainer, canvasWidth, players = [], dt = 1 / 60) {
        if (this.isDead) return;
        if (!this.elitesRegistered && globalThis.window?.gameLoopInstance?.enemyMinions) {
            this.elitesRegistered = true;
            window.gameLoopInstance.enemyMinions.push(...this.eliteZombies.filter(zombie => !zombie.isDead));
        }
        updateBossMovement(this, canvasWidth, dt);
        const target = closestPlayer(this.x, this.y, players);
        if (target) this.facingAngle = Math.atan2(target.y - this.y, target.x - this.x);
        this.elapsed += dt;
        this.updatePoisonMist(players, dt);
        const elapsedTicks = Math.floor(this.elapsed * 60 + 1e-9);
        while (this.patternTick < elapsedTicks) {
            NecromancerPattern.execute(this, bulletContainer, players, ++this.patternTick, canvasWidth);
        }
    }

    takeDamage(damage) {
        const aliveElites = this.eliteZombies.filter(zombie => !zombie.isDead).length;
        if (!super.takeDamage(damage / (aliveElites + 1))) return false;
        this.zombies.forEach(zombie => { zombie.isDead = true; });
        this.eliteZombies.forEach(zombie => { zombie.isDead = true; });
        this.dangerAreas.length = 0;
        return true;
    }

    draw(ctx, canvasWidth) {
        // 생존한 엘리트와 보스 사이의 보호 연결선을 표시한다.
        ctx.save();
        ctx.strokeStyle = '#c084fc';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#a855f7';
        ctx.shadowBlur = 14;
        for (const zombie of this.eliteZombies) {
            if (zombie.isDead) continue;
            ctx.beginPath();
            ctx.moveTo(this.x, this.y);
            ctx.lineTo(zombie.x, zombie.y);
            ctx.stroke();
        }
        ctx.restore();
        for (const area of this.dangerAreas) {
            ctx.save();
            ctx.beginPath();
            ctx.arc(area.x, area.y, area.radius, 0, Math.PI * 2);
            ctx.fillStyle = area.isFiring ? 'rgba(134, 239, 172, 0.24)' : 'rgba(74, 222, 128, 0.12)';
            ctx.strokeStyle = area.isFiring ? '#86efac' : '#4ade80';
            ctx.lineWidth = 2;
            if (!area.isFiring) ctx.setLineDash([8, 6]);
            ctx.fill();
            ctx.stroke();
            ctx.restore();
        }
        const orb = this.getOrbPosition();
        if (this.patternTick > 0 && Math.floor((this.patternTick - 1) / NECROMANCER_TIMING.stageTicks) % 4 === 2) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.elapsed * 3);
            ctx.beginPath();
            ctx.arc(0, 0, this.radius + 5, 0, Math.PI * 2);
            ctx.setLineDash([12, 8]);
            ctx.strokeStyle = '#c084fc';
            ctx.lineWidth = 3;
            ctx.stroke();
            ctx.restore();
        }
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.facingAngle);
        // 망토는 시선 반대편에 둔다.
        ctx.beginPath();
        ctx.moveTo(-10, -25);
        ctx.quadraticCurveTo(-55, -40, -62, 0);
        ctx.quadraticCurveTo(-55, 40, -10, 25);
        ctx.closePath();
        ctx.fillStyle = '#090a10';
        ctx.fill();
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(0, 0, this.radius * 0.65, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#bbf7d0';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(-28, 23);
        ctx.lineTo(55, 23);
        ctx.strokeStyle = '#7c3aed';
        ctx.lineWidth = 5;
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(51, 23, 13, -1.3, 1.3);
        ctx.strokeStyle = '#ddd6fe';
        ctx.lineWidth = 3;
        ctx.stroke();
        ctx.restore();
        createNecromancerParticles(ctx, orb.x, orb.y, this.elapsed);
        ctx.save();
        ctx.beginPath();
        ctx.arc(orb.x, orb.y, 9, 0, Math.PI * 2);
        ctx.fillStyle = '#a855f7';
        ctx.shadowColor = '#c084fc';
        ctx.shadowBlur = 20;
        ctx.fill();
        ctx.restore();
        this.drawHpBar(ctx, canvasWidth);
    }
}

export default Necromancer;
