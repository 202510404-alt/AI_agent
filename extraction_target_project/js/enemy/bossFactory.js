/**
 * js/enemy/bossFactory.js
 * 보스 인스턴스 생성을 전담하는 팩토리 클래스
 */
import { NeonDragon } from './bosses/neonDragon/neonDragon.js';

export class BossFactory {
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
