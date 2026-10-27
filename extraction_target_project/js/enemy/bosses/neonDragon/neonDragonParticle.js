/**
 * js/enemy/bosses/neonDragon/neonDragonParticle.js
 * 네온 드래곤 보스 전용 폭발 및 피격 이펙트 파티클 헬퍼
 */
import { Particle } from '../../../player/particle.js';

/**
 * 보스 주변에 대형 충격/피격 파티클 무리를 생성합니다.
 * @param {Array} particlesContainer 
 * @param {number} x 
 * @param {number} y 
 * @param {string} color 
 * @param {number} count 
 */
export function createBossExplosionParticles(particlesContainer, x, y, color = '#f43f5e', count = 30) {
    for (let i = 0; i < count; i++) {
        particlesContainer.push(new Particle(x, y, color));
    }
}
