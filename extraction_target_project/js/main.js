/**
 * js/main.js
 * 게임의 최상위 엔트리 포인트 모듈
 */
import { SceneManager } from './core/sceneManager.js';
import { InputHandler } from './core/input.js';
import { UIManager } from './core/ui.js';
import { GameLoop } from './core/gameLoop.js';
import { createImpactParticles } from './player/particle.js';
import { NetworkManager } from './network/networkManager.js';

window.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('gameCanvas');
    if (!canvas) {
        console.error('캔버스 엘리먼트(#gameCanvas)를 찾을 수 없습니다.');
        return;
    }

    const ctx = canvas.getContext('2d');

    // 1. 상태 머신 관리자 초기화
    const sceneManager = new SceneManager();

    // 2. 사용자 입력 처리기 초기화
    const inputHandler = new InputHandler();

    // 3. UI 매니저 초기화 및 콜백 바인딩
    // 3. UI 매니저 초기화 및 콜백 바인딩
    let gameLoopInstance = null;
    const uiManager = new UIManager({
        onSlotToggle: (slot) => {
            if (gameLoopInstance) {
                createImpactParticles(gameLoopInstance.particles, slot.x, slot.y, slot.color, 15);
            }
        },
        onToggleDebug: (show) => {
            if (gameLoopInstance) {
                gameLoopInstance.showAIDebug = show;
            }
        },
        onUseSkill: () => {
            if (gameLoopInstance && typeof gameLoopInstance.useUserSkill === 'function') {
                gameLoopInstance.useUserSkill();
            }
        },
        onUseBomb: () => {
            if (gameLoopInstance) {
                gameLoopInstance.useBomb();
            }
        },
        onRestart: () => {
            window.location.reload();
        }
    });

    // 4. 네트워크 배달망 초기화 (기본 방장 호스트 설정)
    const isHost = !window.location.search.includes('client=true');
    const hostIp = new URLSearchParams(window.location.search).get('host') || window.location.hostname;
    
    window.networkManager = new NetworkManager({
        isHost: isHost,
        hostIp: hostIp
    });
    window.networkManager.init();

    // 5. 게임 메인 루프 초기화 및 실행
    gameLoopInstance = new GameLoop(canvas, ctx, sceneManager, inputHandler, uiManager);

    // 6. [메인 메뉴] -> [게임 시작] 이벤트 및 P3 `k090207` 히든 디버그 트리거 검사
    const btnStart = document.getElementById('btn-start-game');
    if (btnStart) {
        btnStart.addEventListener('click', () => {
            // 💡 메뉴에서 라디오 버튼으로 선택한 슬롯(P1~P4)을 내 조작 슬롯으로 네트워크 매니저에 고정
            const selectedRadio = document.querySelector('input[name="my-slot-select"]:checked');
            if (selectedRadio && window.networkManager) {
                window.networkManager.mySlotIndex = parseInt(selectedRadio.value, 10);
            }

            // 게임 시작 직전 드롭다운에서 고른 캐릭터 기체로 슬롯 재구성
            if (gameLoopInstance) {
                gameLoopInstance.initSlots();
            }

            const p3NicknameInput = document.getElementById('p3-nickname');
            const p3Name = p3NicknameInput ? p3NicknameInput.value.trim() : '';

            // P3 닉네임이 k090207일 때 히든 디버그 모드 감지!
            if (p3Name === 'k090207') {
                gameLoopInstance.showAIDebug = true;
                uiManager.setDebugVisibility(true); // 상단 디버그 ON/OFF 버튼 노출
                console.log('🔓 [HIDDEN CHEAT] DEBUG MODE ACTIVATED (P3: k090207)');
            } else {
                gameLoopInstance.showAIDebug = false;
                uiManager.setDebugVisibility(false); // 상단 디버그 버튼 숨김
            }

            sceneManager.setState('PLAY');
        });
    }

    // [결과 화면] -> [메인 메뉴 이동] 버튼
    const btnMainMenu = document.getElementById('btn-main-menu');
    if (btnMainMenu) {
        btnMainMenu.addEventListener('click', () => {
            sceneManager.setState('MENU');
        });
    }

    // 5. 프레임 애니메이션 시작
    requestAnimationFrame((now) => gameLoopInstance.run(now));
});
