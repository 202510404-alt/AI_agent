/**
 * js/enemy/bossFactory.js
 * 보스 인스턴스 생성을 전담하는 팩토리 클래스
 */
import { NeonDragon } from './bosses/neonDragon/neonDragon.js';
import { rngBoss } from '../utils/seededRNG.js';

export class BossFactory {
    /**
     * 지원되는 보스 목록 중 시드 기반 다음 보스 추첨 지원
     */
    static getNextBossType() {
        const types = ['neonDragon'];
        const idx = Math.floor(rngBoss.nextBoss() * types.length);
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
            case 'neondragon':
            default:
                return new NeonDragon(x, y);
        }
    }
}

export default BossFactory;
