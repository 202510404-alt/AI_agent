import { rngBoss } from '../utils/seededRNG.js';

/** 네온 드래곤과 네크로맨서가 공유하는 상단 웨이포인트 이동. */
export function updateBossMovement(boss, canvasWidth, dt) {
    boss.moveTimer += dt;
    if (boss.moveTimer >= boss.moveInterval) {
        boss.moveTimer = 0;
        boss.targetX = 150 + rngBoss.move() * (canvasWidth - 300);
        boss.targetY = 120 + rngBoss.move() * 120;
    }
    const dx = boss.targetX - boss.x;
    const dy = boss.targetY - boss.y;
    const distance = Math.hypot(dx, dy);
    const step = boss.moveSpeed * dt;
    if (distance > step) {
        const angle = Math.atan2(dy, dx);
        const wave = Math.sin(boss.moveTimer * 4) * 1.5 * dt * 60;
        boss.x += Math.cos(angle) * step + Math.cos(angle + Math.PI / 2) * wave;
        boss.y += Math.sin(angle) * step + Math.sin(angle + Math.PI / 2) * wave;
    } else {
        boss.x = boss.targetX;
        boss.y = boss.targetY;
    }
}
