/** 네크로맨서 패턴과 벽에서 직진하는 좀비. */
import BaseMinion from '../../../minian/baseMinion.js';
import { rngBoss } from '../../../utils/seededRNG.js';
import { NecromancerBullet } from './necromancerBullet.js';

// 명세에서 간격이 정해지지 않은 항목은 초기 조정값으로 둔다.
export const NECROMANCER_TIMING = {
    stageTicks: 240,
    staffIntervalTicks: 8,
    staffBullets: 3,
    staffSpreadRadians: 0.48,
    radialIntervalTicks: 12,
    radialBullets: 6
};
export const NECROMANCER_PATTERNS = [
    { id: 'zombieSpawn', name: '8방향 사방 좀비 스폰', count: 8, perWall: 2,
        walls: ['top', 'bottom', 'left', 'right'], targeting: 'nearestPlayerAtSpawn', movement: 'straight', positionSeed: 'bossPattern' },
    { id: 'staffBarrage', name: '지팡이 집중 사격', origin: 'staffOrb',
        targeting: 'nearestPlayer', bulletColor: 'purple', randomChannel: 'bossPattern' },
    { id: 'homingToStraight', name: '유도 후 직선 전환 회전 탄막',
        targeting: 'nearestPlayer', movement: 'homingThenStraight', randomChannel: 'bossPattern' },
    { id: 'poisonMist', name: '타깃팅 범위 독안개', targeting: 'nearestPlayer', shape: 'circle',
        warningSeconds: 1.5, durationSeconds: 2, damageTicks: 2, color: 'lightGreen', randomChannel: 'bossPattern' }
];

export function closestPlayer(x, y, players = []) {
    let closest = null;
    let distance = Infinity;
    for (const player of players) {
        if (!player || player.isDead) continue;
        const next = Math.hypot(player.x - x, player.y - y);
        if (next < distance) { closest = player; distance = next; }
    }
    return closest;
}

export class NecromancerZombie extends BaseMinion {
    constructor(x, y, target, boss) {
        super(x, y, false, '#65a30d');
        this.radius = 12;
        this.hp = this.maxHp = 44;
        this.ownerBoss = boss;
        this.direction = target ? Math.atan2(target.y - y, target.x - x) : Math.PI / 2;
        this.moveSpeed = 110;
    }

    updateMovement(players = [], dt = 1 / 60) {
        if (this.isDead) return;
        this.x += Math.cos(this.direction) * this.moveSpeed * dt;
        this.y += Math.sin(this.direction) * this.moveSpeed * dt;
        for (const player of players) {
            if (player && Math.hypot(player.x - this.x, player.y - this.y) <= this.radius + player.radius) {
                if (player.takeDamage?.(1)) this.isDead = true;
                break;
            }
        }
        if (this.x < -30 || this.x > 1310 || this.y < -30 || this.y > 750) this.isDead = true;
    }

    updateAttack() {}
}

export class NecromancerPattern {
    static execute(boss, bullets, players, tick, canvasWidth) {
        const stageTicks = NECROMANCER_TIMING.stageTicks;
        const stage = Math.floor((tick - 1) / stageTicks) % 4;
        const phaseTick = (tick - 1) % stageTicks;
        const target = closestPlayer(boss.x, boss.y, players);

        if (stage === 0 && phaseTick === 0) {
            for (let wall = 0; wall < 4; wall++) {
                for (let i = 0; i < 2; i++) {
                    const along = 40 + rngBoss.pattern() * ((wall < 2 ? canvasWidth : 720) - 80);
                    const x = wall < 2 ? along : wall === 2 ? 0 : canvasWidth;
                    const y = wall < 2 ? (wall === 0 ? 0 : 720) : along;
                    const zombie = new NecromancerZombie(x, y, closestPlayer(x, y, players), boss);
                    boss.zombies.push(zombie);
                    if (globalThis.window?.gameLoopInstance?.enemyMinions) window.gameLoopInstance.enemyMinions.push(zombie);
                }
            }
        } else if (stage === 1 && phaseTick % NECROMANCER_TIMING.staffIntervalTicks === 0 && target) {
            const orb = boss.getOrbPosition();
            const baseAngle = Math.atan2(target.y - orb.y, target.x - orb.x);
            for (let i = 0; i < NECROMANCER_TIMING.staffBullets; i++) {
                const angle = baseAngle + (rngBoss.pattern() - 0.5) * NECROMANCER_TIMING.staffSpreadRadians;
                bullets.push(new NecromancerBullet(orb.x, orb.y, angle));
            }
        } else if (stage === 2 && phaseTick % NECROMANCER_TIMING.radialIntervalTicks === 0) {
            const rotation = phaseTick * 0.035;
            for (let i = 0; i < NECROMANCER_TIMING.radialBullets; i++) {
                bullets.push(new NecromancerBullet(boss.x, boss.y, rotation + Math.PI * 2 * i / NECROMANCER_TIMING.radialBullets, 'homing'));
            }
        } else if (stage === 3 && phaseTick === 0 && target) {
            boss.addPoisonMist(target.x, target.y);
        }
    }
}

export default NecromancerPattern;
