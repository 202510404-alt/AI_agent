/**
 * js/player/characters/defaultPlayer.js
 * 스킬이 없는 기본 기체 클래스
 */
import BasePlayer from '../basePlayer.js';

export class DefaultPlayer extends BasePlayer {
    constructor(slotIndex) {
        super(slotIndex, 'defaultPlayer');
        
        this.className = '기본 기체';
        this.themeColor = '#06b6d4';
        this.hasActiveSkill = false; // 기본 기체는 스킬 버튼 숨김
    }

    draw(ctx) {
        super.draw(ctx);
    }
}

export default DefaultPlayer;