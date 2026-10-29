/**
 * js/enemy/bosses/neonDragon/neonDragonPattern.js
 * 18-Way Ring Blast 및 Triple Target Spiral 탄막 발사 패턴 로직
 */
import { BossBullet } from './neonDragonBullet.js';
import { rngBoss } from '../../../utils/seededRNG.js';

export class NeonDragonPattern {
    static currentTargetIndex = 0;

    /**
     * @param {Array} bulletContainer 보스 탄환 배열
     * @param {number} x 보스 X
     * @param {number} y 보스 Y
     * @param {number} currentAngle 현재 회전 각도
     * @param {number} timer 패턴 카운터
     * @param {Array} players 플레이어 배열
     * @param {object} bossRef 보스 인스턴스 (dangerAreas 업데이트용)
     */
    static execute(bulletContainer, x, y, currentAngle, timer, players = [], bossRef = null) {
        if (timer % 5 !== 0) return;

        const cycle = timer % 400;

        // 패턴 1: 전방향 14-Way 링 탄막 (0 ~ 120틱)
        if (cycle < 120) {
            const ways = 14;
            for (let i = 0; i < ways; i++) {
                const angle = (Math.PI * 2 / ways) * i + currentAngle;
                bulletContainer.push(new BossBullet(x, y, angle, 3.5, '#ec4899'));
            }
        } 
        // 패턴 2 [복원]: Triple Target Spiral (3갈래 빠른 나선 탄막) (130 ~ 220틱)
        else if (cycle >= 130 && cycle < 220) {
            for (let i = 0; i < 3; i++) {
                const angle = currentAngle * 2.2 + (Math.PI * 2 / 3 * i);
                bulletContainer.push(new BossBullet(x, y, angle, 5.2, '#f59e0b')); // 빠른 탄속 5.2 적용
            }
        }
        // 패턴 3: 가장 가까운 플레이어 향 유도 미사일 (230 ~ 310틱)
        else if (cycle >= 230 && cycle < 310) {
            if (timer % 20 === 0) {
                bulletContainer.push(new BossBullet(x, y, currentAngle, 2.8, '#a855f7', true));
            }
        }
        // 패턴 4: 순차 타깃 0.7초 경고선 레이저 (320 ~ 390틱)
        else if (cycle >= 320 && cycle < 390) {
            if (timer % 35 === 0 && players.length > 0 && bossRef) {
                const targetPlayer = players[this.currentTargetIndex % players.length];
                this.currentTargetIndex++;

                if (targetPlayer) {
                    const angle = Math.atan2(targetPlayer.y - y, targetPlayer.x - x);
                    bossRef.addLaserWarning(x, y, angle, 40, 0.7); // 0.7초 경고선 레이저
                }
            }
        }
    }
}

export default NeonDragonPattern;
