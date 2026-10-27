/**
 * js/player/characters/index.js
 * characters 폴더 내의 캐릭터 모듈 동적 등록 및 자동 스캔 시스템
 */
import DefaultPlayer from './defaultPlayer.js';
import BufferPlayer from './bufferPlayer.js';
import ShielderPlayer from './shielderPlayer.js';
import EmpPlayer from './empPlayer.js';
import SummonerPlayer from './summonerPlayer.js';

// 새 캐릭터 추가 시 이 맵에 파일명 및 클래스 명세 등록
export const CHARACTER_MODULES = {
    defaultPlayer: DefaultPlayer,
    bufferPlayer: BufferPlayer,
    shielderPlayer: ShielderPlayer,
    empPlayer: EmpPlayer,
    summonerPlayer: SummonerPlayer
};

/**
 * 등록된 캐릭터들로부터 메뉴 선택용 인스턴스 정보 자동 수집
 */
export function getAutoDiscoveredClasses() {
    return Object.keys(CHARACTER_MODULES).map(fileName => {
        const CharClass = CHARACTER_MODULES[fileName];
        const dummy = new CharClass(-1);
        return {
            id: fileName,          // 파일명 ID (예: 'bufferPlayer')
            name: dummy.className,  // 파일 내부 정의 이름 (예: '버퍼 (Buffer)')
            color: dummy.themeColor
        };
    });
}