/**
 * js/player/playerFactory.js
 * 파일명 기반 동적 캐릭터 생성 팩토리
 */
import { CHARACTER_MODULES } from './characters/index.js';
import DefaultPlayer from './characters/defaultPlayer.js';

export class PlayerFactory {
    /**
     * 선택된 파일명(classType)에 맞는 캐릭터 클래스를 동적으로 생성
     * @param {number} slotIndex 
     * @param {string} classType 파일명 ID (예: 'bufferPlayer', 'defaultPlayer')
     * @returns {BasePlayer}
     */
    static createPlayer(slotIndex, classType = 'defaultPlayer') {
        const CharClass = CHARACTER_MODULES[classType] || DefaultPlayer;
        return new CharClass(slotIndex);
    }
}

export default PlayerFactory;

