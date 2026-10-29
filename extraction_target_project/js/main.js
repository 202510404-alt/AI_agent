/**
 * js/main.js
 * 게임의 최상위 엔트리 포인트 모듈
 */
import { SceneManager } from './core/sceneManager.js';
import { InputManager } from './core/InputManager.js';
import { UIManager } from './core/ui.js';
import { GameLoop } from './core/gameLoop.js';
import { createImpactParticles } from './player/particle.js';
import { NetworkManager } from './network/networkManager.js';
import { AudioManager } from './core/audioManager.js';

window.addEventListener('DOMContentLoaded', () => {
    const audio = new AudioManager();
    window.gameAudio = audio;
    window.addEventListener('pointerdown', () => audio.unlock(), { passive: true });
    window.addEventListener('keydown', () => audio.unlock());
    const audioButton = document.createElement('button');
    audioButton.type = 'button';
    audioButton.textContent = audio.enabled ? '🔊 Sound' : '🔇 Sound';
    audioButton.setAttribute('aria-label', 'Toggle game sound');
    audioButton.style.cssText = 'position:fixed;right:12px;top:12px;z-index:10000;padding:8px 12px;border:1px solid #67e8f9;border-radius:8px;background:#081322;color:white;cursor:pointer';
    audioButton.addEventListener('click', () => {
        audio.setEnabled(!audio.enabled);
        audioButton.textContent = audio.enabled ? '🔊 Sound' : '🔇 Sound';
    });
    document.body.appendChild(audioButton);
    const canvas = document.getElementById('gameCanvas');
    if (!canvas) {
        console.error('캔버스 엘리먼트(#gameCanvas)를 찾을 수 없습니다.');
        return;
    }

    const ctx = canvas.getContext('2d');

    // 0. 논리적 고정 해상도 및 스케일링 설정 (모든 기기 맵 크기 고정)
    const GAME_WIDTH = 1280;
    const GAME_HEIGHT = 720;

    canvas.width = GAME_WIDTH;
    canvas.height = GAME_HEIGHT;

    function resizeCanvas() {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const scale = Math.min(windowWidth / GAME_WIDTH, windowHeight / GAME_HEIGHT);

        canvas.style.width = `${GAME_WIDTH * scale}px`;
        canvas.style.height = `${GAME_HEIGHT * scale}px`;
        canvas.style.position = 'absolute';
        canvas.style.left = `${(windowWidth - GAME_WIDTH * scale) / 2}px`;
        canvas.style.top = `${(windowHeight - GAME_HEIGHT * scale) / 2}px`;
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // 1. 상태 머신 관리자 초기화
    const sceneManager = new SceneManager({ onStateChange: (state) => audio.setPlaying(state === 'PLAY') });

    // 2. 사용자 입력 처리기 초기화
    const inputHandler = new InputManager();

    // 3. UI 매니저 초기화 및 콜백 바인딩
    // 3. UI 매니저 초기화 및 콜백 바인딩
    let gameLoopInstance = null;
    let awaitingGameRoomState = false;
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
        }
    });

    // 4. 네트워크 배달망 초기화 (기본 방장 호스트 설정)
    const isHost = !window.location.search.includes('client=true');
    const hostIp = new URLSearchParams(window.location.search).get('host') || window.location.hostname;
    
    window.networkManager = new NetworkManager({
        isHost: isHost,
        hostIp: hostIp
    });
    inputHandler.attachNetworkManager(window.networkManager);
    window.networkManager.init();

    // 네트워크 페이즈 변경 이벤트 수신 시 SceneManager 동기화
    window.networkManager.on('PHASE_CHANGE', (packet) => {
        if (packet.phase === 'GAME') {
            if (gameLoopInstance) {
                // masterSeed 및 방 상태를 전달받아 기기 간 화면 및 난수 시드 동기화
                gameLoopInstance.initSlots(packet.masterSeed, packet.slotDetails);
            }
            sceneManager.setState('PLAY');
        } else if (packet.phase === 'LOBBY') {
            sceneManager.setState('LOBBY');
        } else if (packet.phase === 'MENU') {
            sceneManager.setState('MENU');
        } else if (packet.phase === 'SCOREBOARD') {
            if (gameLoopInstance) gameLoopInstance.enterScoreboard();
        }
    });

    // 슬롯 할당(SLOT_ASSIGNED) 및 방 상태(ROOM_STATE) 수신 시 로비 슬롯 UI 갱신 및 화면 전환
    window.networkManager.on('SLOT_ASSIGNED', (packet) => {
        console.log(`[Main] 슬롯 할당 수신: P${packet.slotIndex}`);
        if (window.networkManager.slotDetails) {
            uiManager.updateLobbySlots(window.networkManager.slotDetails, packet.slotIndex);
        }
        
        const currentPhase = packet.phase || window.networkManager.currentPhase || 'LOBBY';
        if (currentPhase === 'GAME') {
            awaitingGameRoomState = true;
        } else if (currentPhase === 'LOBBY') {
            sceneManager.setState('LOBBY');
        } else if (currentPhase === 'MENU') {
            sceneManager.setState('MENU');
        } else if (currentPhase === 'SCOREBOARD') {
            if (gameLoopInstance) gameLoopInstance.enterScoreboard();
        }
    });

    window.networkManager.on('ROOM_STATE', (packet) => {
        if (packet.slotDetails) {
            uiManager.updateLobbySlots(packet.slotDetails, window.networkManager.mySlotIndex);
        }
        if (awaitingGameRoomState && packet.phase === 'GAME') {
            awaitingGameRoomState = false;
            if (gameLoopInstance) gameLoopInstance.initSlots(packet.masterSeed, packet.slotDetails);
            sceneManager.setState('PLAY');
        }
    });

    window.networkManager.on('VOTE_STATUS_UPDATE', (packet) => {
        uiManager.updateVoteStatus(packet.votes, window.networkManager.mySlotIndex);
    });

    // 네트워크를 통해 들어오는 다른 플레이어의 키 입력(INPUT_SYNC) 수신 처리
    window.networkManager.on('INPUT_SYNC', (packet) => {
        if (gameLoopInstance && typeof gameLoopInstance.handleNetworkInput === 'function') {
            gameLoopInstance.handleNetworkInput(packet.slotIndex, packet.inputAction);
        }
    });

    // 5. 게임 메인 루프 초기화 및 실행
    gameLoopInstance = new GameLoop(canvas, ctx, sceneManager, inputHandler, uiManager);

    // 6. [로비 화면] -> [READY / NOT READY] 토글 버튼 이벤트
    let isLobbyReady = false;
    const btnLobbyReady = document.getElementById('btn-lobby-ready');
    if (btnLobbyReady) {
        btnLobbyReady.addEventListener('click', () => {
            isLobbyReady = !isLobbyReady;
            if (isLobbyReady) {
                btnLobbyReady.innerHTML = '<i class="fa-solid fa-xmark"></i> CANCEL READY';
                btnLobbyReady.className = 'w-full py-3.5 bg-gradient-to-r from-pink-600 to-rose-600 hover:from-pink-500 hover:to-rose-500 text-white font-black text-lg rounded-xl shadow-lg transition active:scale-95 flex items-center justify-center gap-2';
            } else {
                btnLobbyReady.innerHTML = '<i class="fa-solid fa-check"></i> READY';
                btnLobbyReady.className = 'w-full py-3.5 bg-gradient-to-r from-cyan-500 via-teal-500 to-emerald-500 hover:from-cyan-400 hover:to-emerald-400 text-black font-black text-lg rounded-xl shadow-lg transition active:scale-95 flex items-center justify-center gap-2';
            }

            // 히든 치트키 검사 (P3: k090207)
            const p3NicknameInput = document.getElementById('p3-nickname');
            const p3Name = p3NicknameInput ? p3NicknameInput.value.trim() : '';
            if (p3Name === 'k090207') {
                gameLoopInstance.showAIDebug = true;
                uiManager.setDebugVisibility(true);
                console.log('🔓 [HIDDEN CHEAT] DEBUG MODE ACTIVATED (P3: k090207)');
            } else {
                gameLoopInstance.showAIDebug = false;
                uiManager.setDebugVisibility(false);
            }

            // 💡 [Strict Sync]: 현재 내 닉네임과 직업을 포함하여 서버로 READY 패킷 송신
            if (window.networkManager) {
                const mySlot = window.networkManager.mySlotIndex || 1;
                const nameInput = document.getElementById(`p${mySlot}-nickname`);
                const classSelect = document.getElementById(`p${mySlot}-class`);
                const nickname = nameInput ? nameInput.value.trim() : `PLAYER ${mySlot}`;
                const classType = classSelect ? classSelect.value : 'bufferPlayer';

                window.networkManager.sendReady(isLobbyReady, { nickname, classType });
            }
        });
    }

    // 7. [메인 메뉴] -> [게임 시작] 버튼 이벤트 연동
    const btnStart = document.getElementById('btn-start-game');
    if (btnStart) {
        btnStart.addEventListener('click', () => {
            if (window.networkManager) {
                window.networkManager.sendReady(true);
            } else {
                if (gameLoopInstance) {
                    gameLoopInstance.initSlots();
                }
                sceneManager.setState('PLAY');
            }
        });
    }

    // [결과 화면] -> [REPLAY] 버튼 (SCOREBOARD 표결 전송)
    const btnRestartMatch = document.getElementById('btnRestartMatch');
    if (btnRestartMatch) {
        btnRestartMatch.addEventListener('click', () => {
            if (window.networkManager) {
                window.networkManager.sendVote('REPLAY');
            } else {
                window.location.reload();
            }
        });
    }

    // [결과 화면] -> [메인 메뉴 이동] 버튼 (SCOREBOARD 표결 전송)
    const btnMainMenu = document.getElementById('btn-main-menu');
    if (btnMainMenu) {
        btnMainMenu.addEventListener('click', () => {
            if (window.networkManager) {
                window.networkManager.sendVote('MENU');
            } else {
                sceneManager.setState('MENU');
            }
        });
    }

    // 5. 프레임 애니메이션 시작
    requestAnimationFrame((now) => gameLoopInstance.run(now));
});
