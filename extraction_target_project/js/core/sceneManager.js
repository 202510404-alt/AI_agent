/**
 * js/core/sceneManager.js
 * 게임의 상태 머신 (MENU -> PLAY -> GAMEOVER) 관리 클래스
 */


export const GameState = {
    MENU: 'MENU',
    PLAY: 'PLAY',
    GAMEOVER: 'GAMEOVER'
};

export class SceneManager {
    /**
     * @param {object} options 
     * @param {Function} [options.onStateChange] 상태 변경 콜백
     */
    constructor(options = {}) {
        this.currentState = GameState.MENU; // 메인 로비(MENU)에서 시작
        this.onStateChange = options.onStateChange || null;
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
        const menuScreen = document.getElementById('menu-screen');
        const uiLayer = document.getElementById('ui-layer');
        const resultScreen = document.getElementById('result-screen');

        if (menuScreen) menuScreen.style.display = (nextState === GameState.MENU) ? 'flex' : 'none';
        if (uiLayer) uiLayer.style.display = (nextState === GameState.PLAY) ? 'flex' : 'none';
        if (resultScreen) {
            if (nextState === GameState.GAMEOVER) {
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
