/**
 * js/enemy/bossFactory.js
 * 보스 인스턴스 생성을 전담하는 팩토리 클래스
 */
import { NeonDragon } from './bosses/neonDragon/neonDragon.js';
import { Necromancer } from './bosses/necromancer/necromancer.js';
import { seededRNG } from '../utils/seededRNG.js';

export class BossFactory {
    /**
     * 지원되는 보스 목록 중 시드 기반 다음 보스 추첨 지원
     */
    static getNextBossType(previousType, round = 1) {
        const types = ['neonDragon', 'necromancer'].filter(type => type !== previousType);
        if (!types.length) return null;
        const idx = Math.floor(seededRNG.get(`nextBoss_round_${round}`).next() * types.length);
        return types[idx];
    }
    /**
     * 지정된 타입의 보스를 생성합니다.
     * @param {string} type 
     * @param {number} x 
     * @param {number} y 
     * @returns {BaseBoss}
     */
    static createBoss(type = 'neonDragon', x, y) {
        switch (type.toLowerCase()) {
            case 'necromancer':
                return new Necromancer(x, y);
            case 'neondragon':
            default:
                return new NeonDragon(x, y);
        }
    }
}

export default BossFactory;
