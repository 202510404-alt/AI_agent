/**
 * js/core/sceneManager.js
 * 게임의 상태 머신 (MENU -> PLAY -> GAMEOVER) 관리 클래스
 */


export const GameState = {
    LOBBY: 'LOBBY',
    MENU: 'MENU',
    PLAY: 'PLAY',
    GAME: 'PLAY', // 'GAME' 페이즈는 'PLAY'와 동치 매핑
    SCOREBOARD: 'SCOREBOARD',
    GAMEOVER: 'SCOREBOARD' // 'GAMEOVER'는 'SCOREBOARD'와 동치 매핑
};

export class SceneManager {
    /**
     * @param {object} options 
     * @param {Function} [options.onStateChange] 상태 변경 콜백
     */
    constructor(options = {}) {
        this.currentState = GameState.LOBBY; // 기본 시작 상태: LOBBY
        this.onStateChange = options.onStateChange || null;
        
        // 생성 시점 화면 가시성 강제 초기화 (LOBBY 화면 노출)
        setTimeout(() => {
            this.setState(GameState.LOBBY);
        }, 0);
    }

    /**
     * 현재 상태 확인
     * @returns {string} GameState
     */
    getState() {
        return this.currentState;
    }

    /**
     * 상태 변경
     * @param {string} nextState 
     * @param {any} payload 
     */
    setState(nextState, payload = null) {
        if (this.currentState === nextState) return;
        const prevState = this.currentState;
        this.currentState = nextState;

        console.log(`[SceneManager] Scene Changed: ${prevState} -> ${nextState}`);

        // 화면 DOM 엘리먼트 가시성 토글
        const lobbyScreen = document.getElementById('lobby-screen');
        const menuScreen = document.getElementById('menu-screen');
        const uiLayer = document.getElementById('ui-layer');
        const resultScreen = document.getElementById('result-screen');

        const isLobby = (nextState === GameState.LOBBY || nextState === 'LOBBY');
        const isMenu = (nextState === GameState.MENU);
        const isPlay = (nextState === GameState.PLAY || nextState === 'GAME');
        const isScoreboard = (nextState === GameState.SCOREBOARD || nextState === 'GAMEOVER');

        if (lobbyScreen) lobbyScreen.style.display = isLobby ? 'flex' : 'none';
        if (menuScreen) menuScreen.style.display = isMenu ? 'flex' : 'none';
        if (uiLayer) uiLayer.style.display = isPlay ? 'flex' : 'none';
        if (resultScreen) {
            if (isScoreboard) {
                resultScreen.classList.remove('hidden');
                resultScreen.style.display = 'flex';
            } else {
                resultScreen.classList.add('hidden');
                resultScreen.style.display = 'none';
            }
        }

        if (this.onStateChange) {
            this.onStateChange(nextState, prevState, payload);
        }
    }

    /**
     * 게임 플레이 상태인지 확인
     * @returns {boolean}
     */
    isPlaying() {
        return this.currentState === GameState.PLAY;
    }

    /**
     * 게임 종료 상태인지 확인
     * @returns {boolean}
     */
    isGameOver() {
        return this.currentState === GameState.GAMEOVER;
    }
}

export default SceneManager;
