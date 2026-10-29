# ==========================================================================
# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드
# [SCAN_MODE] EXTRACTION_TARGET_PROJECT
# ==========================================================================
# 📄 [요청 1] TARGET: index.html (1-336라인)
# ----------------------------------------------------------
```python
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Human-like AI Bullet Hell Arena</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="css/style.css">
</head>
<body class="h-screen w-screen flex flex-col justify-between items-center relative overflow-hidden bg-slate-950">

    <!-- GAME CANVAS CONTAINER -->
    <div class="absolute inset-0 z-0">
        <canvas id="gameCanvas" class="w-full h-full block"></canvas>
        <div class="scanline absolute inset-0"></div>
    </div>

    <!-- 1. 로비 화면 (LOBBY State) -->
    <div id="lobby-screen" class="absolute inset-0 z-50 flex flex-col items-center justify-center bg-slate-950/90 backdrop-blur-md p-4">
        <div class="text-center space-y-6 max-w-2xl w-full bg-slate-900/80 p-8 rounded-2xl border border-cyan-500/50 shadow-2xl neon-border-cyan">
            <!-- 로비 타이틀 -->
            <div>
                <h1 class="text-3xl sm:text-4xl font-black tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-pink-500 to-yellow-400 animate-pulse">
                    MULTIPLAYER LOBBY
                </h1>
                <p class="text-xs text-cyan-300/80 mt-1">대기실에서 모든 참가자가 준비를 완료하면 게임이 시작됩니다.</p>
            </div>

            <!-- P1~P4 슬롯 카드 그리드 -->
            <div id="lobby-slots-container" class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-left">
                <!-- P1 슬롯 카드 -->
                <div id="lobby-slot-card-1" class="bg-black/60 p-4 rounded-xl border border-cyan-500/30 flex flex-col justify-between transition-all">
                    <div class="flex items-center justify-between border-b border-gray-700/60 pb-2 mb-2">
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-black text-cyan-400">SLOT 1</span>
                            <span class="slot-conn-badge text-[9px] px-1.5 py-0.5 rounded font-bold bg-gray-700 text-gray-400">WAITING</span>
                        </div>
                        <span class="slot-ready-badge text-[10px] px-2 py-0.5 rounded font-black bg-gray-700 text-gray-400">NOT READY</span>
                    </div>
                    <div class="space-y-1">
                        <p class="text-sm font-bold text-white slot-nickname truncate">대기 중...</p>
                        <p class="text-xs text-gray-400 slot-class truncate"><i class="fa-solid fa-crosshairs mr-1"></i>기본 기체</p>
                    </div>
                </div>

                <!-- P2 슬롯 카드 -->
                <div id="lobby-slot-card-2" class="bg-black/60 p-4 rounded-xl border border-pink-500/30 flex flex-col justify-between transition-all">
                    <div class="flex items-center justify-between border-b border-gray-700/60 pb-2 mb-2">
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-black text-pink-400">SLOT 2</span>
                            <span class="slot-conn-badge text-[9px] px-1.5 py-0.5 rounded font-bold bg-gray-700 text-gray-400">WAITING</span>
                        </div>
                        <span class="slot-ready-badge text-[10px] px-2 py-0.5 rounded font-black bg-gray-700 text-gray-400">NOT READY</span>
                    </div>
                    <div class="space-y-1">
                        <p class="text-sm font-bold text-white slot-nickname truncate">대기 중...</p>
                        <p class="text-xs text-gray-400 slot-class truncate"><i class="fa-solid fa-crosshairs mr-1"></i>기본 기체</p>
                    </div>
                </div>

                <!-- P3 슬롯 카드 -->
                <div id="lobby-slot-card-3" class="bg-black/60 p-4 rounded-xl border border-emerald-500/30 flex flex-col justify-between transition-all">
                    <div class="flex items-center justify-between border-b border-gray-700/60 pb-2 mb-2">
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-black text-emerald-400">SLOT 3</span>
                            <span class="slot-conn-badge text-[9px] px-1.5 py-0.5 rounded font-bold bg-gray-700 text-gray-400">WAITING</span>
                        </div>
                        <span class="slot-ready-badge text-[10px] px-2 py-0.5 rounded font-black bg-gray-700 text-gray-400">NOT READY</span>
                    </div>
                    <div class="space-y-1">
                        <p class="text-sm font-bold text-white slot-nickname truncate">대기 중...</p>
                        <p class="text-xs text-gray-400 slot-class truncate"><i class="fa-solid fa-crosshairs mr-1"></i>기본 기체</p>
                    </div>
                </div>

                <!-- P4 슬롯 카드 -->
                <div id="lobby-slot-card-4" class="bg-black/60 p-4 rounded-xl border border-amber-500/30 flex flex-col justify-between transition-all">
                    <div class="flex items-center justify-between border-b border-gray-700/60 pb-2 mb-2">
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-black text-amber-400">SLOT 4</span>
                            <span class="slot-conn-badge text-[9px] px-1.5 py-0.5 rounded font-bold bg-gray-700 text-gray-400">WAITING</span>
                        </div>
                        <span class="slot-ready-badge text-[10px] px-2 py-0.5 rounded font-black bg-gray-700 text-gray-400">NOT READY</span>
                    </div>
                    <div class="space-y-1">
                        <p class="text-sm font-bold text-white slot-nickname truncate">대기 중...</p>
                        <p class="text-xs text-gray-400 slot-class truncate"><i class="fa-solid fa-crosshairs mr-1"></i>기본 기체</p>
                    </div>
                </div>
            </div>

            <!-- READY 토글 버튼 -->
            <div class="pt-2">
                <button id="btn-lobby-ready" class="w-full py-3.5 bg-gradient-to-r from-cyan-500 via-teal-500 to-emerald-500 hover:from-cyan-400 hover:to-emerald-400 text-black font-black text-lg rounded-xl shadow-lg transition active:scale-95 flex items-center justify-center gap-2">
                    <i class="fa-solid fa-check"></i> READY
                </button>
            </div>
        </div>
    </div>

    <!-- 2. 메인 메뉴 화면 (MENU State) -->
    <div id="menu-screen" class="absolute inset-0 z-50 flex flex-col items-center justify-center bg-slate-950/90 backdrop-blur-md p-4" style="display: none;">
        <div class="text-center space-y-6 max-w-lg w-full bg-slate-900/80 p-8 rounded-2xl border border-cyan-500/50 shadow-2xl neon-border-cyan">
            <!-- 깔끔한 단독 네온 타이틀 -->
            <h1 class="text-4xl sm:text-5xl font-black tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-pink-500 to-yellow-400 animate-pulse">
                BULLET MATRIX
            </h1>

            <!-- P1~P4 슬롯 & 닉네임 / 직업 선택 -->
            <div class="space-y-3 text-left">
                <p class="text-xs font-bold text-cyan-400 tracking-wider uppercase border-b border-gray-700 pb-1">
                    <i class="fa-solid fa-users"></i> Pilot Slots & Class Selection
                </p>
                
                <div class="grid grid-cols-2 gap-2 text-xs">
                    <div class="bg-black/50 p-2 rounded border border-cyan-500/30 relative">
                        <div class="flex items-center justify-between mb-0.5">
                            <label class="text-[10px] text-cyan-300 font-bold">P1 SLOT</label>
                            <label class="flex items-center gap-1 cursor-pointer">
                                <input type="radio" name="my-slot-select" value="1" checked class="accent-cyan-400" />
                                <span class="text-[9px] text-cyan-400 font-black">내 기체</span>
                            </label>
                        </div>
                        <input type="text" id="p1-nickname" value="PLAYER 1" class="w-full bg-slate-800 text-white px-2 py-0.5 rounded border border-slate-700 text-xs mb-1" />
                        <select id="p1-class" class="w-full bg-slate-800 text-cyan-300 px-1 py-0.5 rounded border border-slate-700 text-[10px] font-bold">
                            <!-- JS 동적 생성 -->
                        </select>
                    </div>
                    <div class="bg-black/50 p-2 rounded border border-pink-500/30 relative">
                        <div class="flex items-center justify-between mb-0.5">
                            <label class="text-[10px] text-pink-300 font-bold">P2 SLOT</label>
                            <label class="flex items-center gap-1 cursor-pointer">
                                <input type="radio" name="my-slot-select" value="2" class="accent-pink-400" />
                                <span class="text-[9px] text-pink-400 font-black">내 기체</span>
                            </label>
                        </div>
                        <input type="text" id="p2-nickname" value="BOT-ALPHA" class="w-full bg-slate-800 text-white px-2 py-0.5 rounded border border-slate-700 text-xs mb-1" />
                        <select id="p2-class" class="w-full bg-slate-800 text-pink-300 px-1 py-0.5 rounded border border-slate-700 text-[10px] font-bold">
                            <!-- JS 동적 생성 -->
                        </select>
                    </div>
                    <div class="bg-black/50 p-2 rounded border border-emerald-500/30 relative">
                        <div class="flex items-center justify-between mb-0.5">
                            <label class="text-[10px] text-emerald-300 font-bold">P3 SLOT <span class="text-[8px] text-gray-500">(Cheat Zone)</span></label>
                            <label class="flex items-center gap-1 cursor-pointer">
                                <input type="radio" name="my-slot-select" value="3" class="accent-emerald-400" />
                                <span class="text-[9px] text-emerald-400 font-black">내 기체</span>
                            </label>
                        </div>
                        <input type="text" id="p3-nickname" placeholder="Callsign" value="BOT-BETA" class="w-full bg-slate-800 text-white px-2 py-0.5 rounded border border-slate-700 text-xs mb-1" />
                        <select id="p3-class" class="w-full bg-slate-800 text-emerald-300 px-1 py-0.5 rounded border border-slate-700 text-[10px] font-bold">
                            <!-- JS 동적 생성 -->
                        </select>
                    </div>
                    <div class="bg-black/50 p-2 rounded border border-amber-500/30 relative">
                        <div class="flex items-center justify-between mb-0.5">
                            <label class="text-[10px] text-amber-300 font-bold">P4 SLOT</label>
                            <label class="flex items-center gap-1 cursor-pointer">
                                <input type="radio" name="my-slot-select" value="4" class="accent-amber-400" />
                                <span class="text-[9px] text-amber-400 font-black">내 기체</span>
                            </label>
                        </div>
                        <input type="text" id="p4-nickname" value="BOT-GAMMA" class="w-full bg-slate-800 text-white px-2 py-0.5 rounded border border-slate-700 text-xs mb-1" />
                        <select id="p4-class" class="w-full bg-slate-800 text-amber-300 px-1 py-0.5 rounded border border-slate-700 text-[10px] font-bold">
                            <!-- JS 동적 생성 -->
                        </select>
                    </div>
                </div>
            </div>

            <!-- 메뉴 시작 버튼 -->
            <div class="pt-2 space-y-2">
                <button id="btn-start-game" class="w-full py-3.5 bg-gradient-to-r from-cyan-500 via-teal-500 to-emerald-500 hover:from-cyan-400 hover:to-emerald-400 text-black font-black text-lg rounded-xl shadow-lg transition active:scale-95 flex items-center justify-center gap-2">
                    <i class="fa-solid fa-play"></i> GAME START
                </button>
            </div>
        </div>
    </div>

    <!-- 2. 게임 인게임 HEADER / HUD (PLAY State) -->
    <header id="ui-layer" class="relative z-10 w-full max-w-7xl p-3 flex flex-wrap justify-between items-center gap-2 bg-slate-900/85 backdrop-blur-md rounded-b-2xl border-b border-cyan-500/40 shadow-xl" style="display: none;">
        <div class="flex items-center gap-3">
            <i class="fa-solid fa-brain text-cyan-400 text-2xl animate-pulse"></i>
            <div>
                <h1 class="text-lg font-black tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-pink-500 to-yellow-400">
                    HUMAN-LIKE AI BULLET HELL
                </h1>
                <p class="text-[10px] text-cyan-300/80 font-normal">FSM + Action Lock + Fatigue System Demo</p>
            </div>
        </div>

        <!-- Global Match Timer & Score & AI Mode Toggle -->
        <div class="flex items-center gap-3">
            <div class="bg-black/60 px-3 py-1 rounded-lg border border-pink-500/40 flex items-center gap-2">
                <i class="fa-solid fa-stopwatch text-pink-400"></i>
                <span id="matchTimerDisplay" class="font-bold text-base text-pink-300 tracking-wider">02:00</span>
            </div>
            <div class="text-right">
                <p class="text-[9px] text-gray-400 uppercase tracking-widest">Team DPS Score</p>
                <p id="teamScoreDisplay" class="font-black text-lg text-emerald-400">000000</p>
            </div>
            <div class="h-6 w-px bg-slate-800"></div>

            <!-- 상단 미니멀 [AI ON/OFF] 토글 버튼 -->
            <button id="btn-top-ai-toggle" class="flex items-center gap-1.5 px-3 py-1 bg-slate-800 hover:bg-slate-700 active:scale-95 border border-cyan-500/40 rounded-lg transition">
                <i class="fa-solid fa-robot text-xs text-cyan-400"></i>
                <div class="text-left text-[10px] leading-tight">
                    <span class="block text-[8px] text-slate-400">MODE</span>
                    <span id="top-ai-status-text" class="text-cyan-400 font-bold">USER (MANUAL)</span>
                </div>
            </button>
        </div>

        <!-- Debug Visualizer Toggle (히든 치트키 발동 시만 노출) -->
        <button id="btnToggleDebug" class="hidden px-3 py-1.5 rounded-lg bg-cyan-950 border border-cyan-500/60 hover:bg-cyan-900 text-cyan-300 text-xs font-bold flex items-center gap-2 transition active:scale-95 shadow-md">
            <i class="fa-solid fa-eye"></i>
            <span>AI 디버그 시각화: <strong id="debugStatusText" class="text-emerald-400">OFF</strong></span>
        </button>
    </header>

    <!-- RIGHT FLOATING PANEL: SLOT CONTROL & LIVE STATS -->
    <div id="right-debug-panel" class="hidden absolute right-4 top-20 z-20 w-80 bg-slate-900/90 backdrop-blur-md rounded-xl p-3 border border-cyan-500/40 shadow-2xl text-xs space-y-3">
        <!-- Slot Handover Controls -->
        <div>
            <div class="flex justify-between items-center border-b border-gray-700 pb-1.5 mb-2">
                <span class="font-bold text-cyan-400 flex items-center gap-1.5">
                    <i class="fa-solid fa-users"></i> 슬롯 제어 (유저 난입 / AI)
                </span>
                <span class="text-[9px] text-pink-400 bg-pink-950/80 px-1.5 py-0.5 rounded border border-pink-600/50">SLOTS: 4</span>
            </div>
            <div id="slotControlsContainer" class="grid grid-cols-2 gap-1.5">
                <!-- 동적 렌더링 영역 -->
            </div>
        </div>

        <!-- Live Real-Time AI Stats -->
        <div>
            <div class="flex justify-between items-center border-b border-gray-700 pb-1.5 mb-2">
                <span class="font-bold text-yellow-400 flex items-center gap-1.5">
                    <i class="fa-solid fa-chart-line"></i> 실시간 딜량 & AI 실수 집계
                </span>
            </div>
            <div id="liveStatsContainer" class="space-y-1.5 max-h-48 overflow-y-auto pr-1">
                <!-- 동적 렌더링 영역 -->
            </div>
        </div>

        <!-- 💡 [k090207 치트키 전용]: 폰 접속용 QR 코드 및 HOST IP 세팅 영역 -->
        <div id="debug-network-info" class="hidden mt-3 p-2 bg-slate-950/90 rounded-xl border border-cyan-500/40 text-center space-y-1">
            <p class="text-[9px] font-bold text-cyan-300">📱 MOBILE CLIENT JOIN QR</p>
            <div class="flex justify-center my-1">
                <img id="qr-code-img" class="w-24 h-24 rounded border border-cyan-400/50 bg-white p-1" alt="Join QR Code" />
            </div>
            <p id="host-ip-url" class="text-[9px] font-mono text-emerald-400 select-all font-bold break-all">http://localhost:3000?client=true</p>
        </div>
    </div>

    <!-- BOTTOM MOBILE CONTROLS / GUIDANCE -->
    <footer class="relative z-10 w-full max-w-7xl p-3 flex justify-between items-end pointer-events-none mb-1">
        <!-- Touch Joystick Zone -->
        <div id="joystickZone" class="pointer-events-auto w-28 h-28 rounded-full border-2 border-cyan-500/40 bg-slate-900/40 backdrop-blur-sm relative flex items-center justify-center md:opacity-40 hover:opacity-100 transition">
            <div id="joystickKnob" class="w-10 h-10 rounded-full bg-cyan-400/80 shadow-lg border border-white absolute transform transition-transform duration-75"></div>
            <span class="text-[8px] text-cyan-300/60 absolute bottom-1.5 pointer-events-none">TOUCH JOYSTICK</span>
        </div>

        <!-- PC Keyboard Guidance -->
        <div class="bg-slate-900/80 backdrop-blur-md px-4 py-2 rounded-xl border border-cyan-500/30 text-center pointer-events-auto hidden sm:block">
            <p class="text-xs text-gray-300 font-medium">
                <span class="px-1.5 py-0.5 bg-slate-800 border border-slate-600 rounded text-cyan-400 font-bold">WASD / 방향키</span> 유저 이동 &nbsp;|&nbsp;
                <span class="px-1.5 py-0.5 bg-slate-800 border border-slate-600 rounded text-pink-400 font-bold">마우스 조준</span> 자동 사격
            </p>
        </div>

        <!-- EMP Bomb & Active Skill Buttons -->
        <div class="pointer-events-auto flex items-center gap-2">
            <!-- 게이지 차오름 스킬 버튼 + [SPACE] 조작 안내 라벨 -->
            <div class="relative flex flex-col items-center gap-1">
                <span class="px-1.5 py-0.5 bg-cyan-950/90 border border-cyan-400/80 rounded text-[9px] font-mono text-cyan-300 font-black tracking-wider shadow-md animate-pulse">
                    [SPACE]
                </span>
                <button id="btnActiveSkill" class="relative w-16 h-16 rounded-full bg-slate-900 border-2 border-amber-400 text-amber-300 font-bold overflow-hidden shadow-lg flex flex-col items-center justify-center active:scale-95 transition">
                    <!-- 하단에서 위로 불투명 차오르는 게이지 레이어 -->
                    <div id="skillGaugeFill" class="absolute bottom-0 left-0 right-0 bg-amber-500/80 transition-all duration-100" style="height: 0%;"></div>
                    <div class="relative z-10 flex flex-col items-center">
                        <i class="fa-solid fa-wand-magic-sparkles text-base mb-0.5"></i>
                        <span id="skillGaugeText" class="text-[8px] font-black">0%</span>
                    </div>
                </button>
            </div>

            <!-- EMP 특수 폭탄 -->
            <button id="btnSpecialBomb" class="w-16 h-16 rounded-full bg-gradient-to-tr from-pink-600 to-purple-600 active:scale-90 border-2 border-pink-300 text-white font-bold flex flex-col items-center justify-center shadow-lg neon-border-pink">
                <i class="fa-solid fa-bolt text-lg mb-0.5"></i>
                <span class="text-[8px]">EMP BOMB</span>
            </button>
        </div>
    </footer>

    <!-- 3. RESULT STATE MODAL -->
    <div id="result-screen" class="hidden absolute inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4">
        <div class="max-w-md w-full bg-slate-900 border-2 border-pink-500 rounded-2xl p-6 text-center space-y-4 shadow-2xl neon-border-pink">
            <h2 id="result-title" class="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-pink-500 via-purple-400 to-cyan-400 tracking-wider">
                MISSION CLEAR
            </h2>
            
            <!-- 종합 최종 점수 -->
            <div class="bg-black/60 p-3 rounded-xl border border-pink-500/30">
                <p class="text-[10px] text-gray-400 uppercase tracking-widest">FINAL SCORE</p>
                <p id="final-score-val" class="text-3xl font-black text-yellow-400 tracking-wider">000000</p>
            </div>

            <!-- 슬롯별 딜량 및 실수 집계 표 -->
            <div id="finalScoreboardList" class="bg-black/60 rounded-xl p-3 border border-slate-800 space-y-1.5 text-left text-xs max-h-52 overflow-y-auto">
                <!-- 동적 렌더링 영역 -->
            </div>

            <!-- 하단 재도전 및 메인 메뉴 버튼 -->
            <div class="grid grid-cols-2 gap-2 pt-2">
                <button id="btnRestartMatch" class="py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-black rounded-xl shadow-lg transition transform active:scale-95 text-xs">
                    🔄 REPLAY
                </button>
                <button id="btn-main-menu" class="py-2.5 bg-slate-800 hover:bg-slate-700 border border-slate-600 text-gray-200 font-black rounded-xl transition transform active:scale-95 text-xs">
                    🏠 MAIN MENU
                </button>
            </div>
        </div>
    </div>

    <!-- ES6 MODULE ENTRY POINT -->
    <script type="module" src="js/main.js" defer></script>
</body>
</html>
```

# 📄 [요청 1 ➡️ 불러온함수 (truncate 본체)] TARGET: extraction_target_project/js/core/ui.js (461-473라인)
# ----------------------------------------------------------
```python
                    classEl.className = 'text-xs text-cyan-300/80 slot-class truncate';
                }

                // 레디 상태 표시 (ready: 초록색 / 회색 뱃지)
                if (readyBadge) {
                    if (slot.ready) {
                        readyBadge.textContent = 'READY';
                        readyBadge.className = 'slot-ready-badge text-[10px] px-2 py-0.5 rounded font-black bg-emerald-500 text-black shadow-md shadow-emerald-500/30';
                    } else {
                        readyBadge.textContent = 'NOT READY';
                        readyBadge.className = 'slot-ready-badge text-[10px] px-2 py-0.5 rounded font-black bg-slate-700 text-gray-400';
                    }
                }
```

# 📄 [요청 1 ➡️ 불러온함수 (truncate 본체)] TARGET: extraction_target_project/js/core/ui.js (499-508라인)
# ----------------------------------------------------------
```python
                    classEl.className = 'text-xs text-gray-600 slot-class truncate';
                }
                card.style.borderColor = '';
                card.style.boxShadow = '';
            }
        });
    }
}

export default UIManager;
```

# 📄 [요청 2] TARGET: js/main.js (120-216라인)
# ----------------------------------------------------------
```python
            sceneManager.setState('MENU');
        } else if (currentPhase === 'SCOREBOARD') {
            sceneManager.setState('GAMEOVER');
        }
    });

    window.networkManager.on('ROOM_STATE', (packet) => {
        if (packet.slotDetails) {
            uiManager.updateLobbySlots(packet.slotDetails, window.networkManager.mySlotIndex);
        }
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

            // 서버로 READY 상태 패킷 송신
            if (window.networkManager) {
                window.networkManager.sendReady(isLobbyReady);
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
```

# 📄 [요청 2 ➡️ 불러온함수 (GameLoop 본체)] TARGET: extraction_target_project/js/core/gameLoop.js (14-23라인)
# ----------------------------------------------------------
```python
export class GameLoop {
    /**
     * @param {HTMLCanvasElement} canvas 
     * @param {CanvasRenderingContext2D} ctx 
     * @param {import('./sceneManager.js').SceneManager} sceneManager 
     * @param {import('./input.js').InputHandler} input 
     * @param {import('./ui.js').UIManager} ui 
     */
```

# 📄 [요청 3] TARGET: js/core/gameLoop.js (1-250라인)
# ----------------------------------------------------------
```python
/**
 * js/core/gameLoop.js
 * 메인 60fps requestAnimationFrame 루프, 충돌 판정, AI 시각화 및 렌더링 결합
 */
import { TOTAL_SLOTS, MATCH_CONFIG, CANVAS_GRID_SIZE } from '../config/constants.js';
import { PlayerFactory } from '../player/playerFactory.js';
import { BossFactory } from '../enemy/bossFactory.js';
import { AIEngine } from '../ai/aiEngine.js';
import { createImpactParticles, createFloatingText } from '../player/particle.js';
import { setGameSeed } from '../utils/math.js';
import { GameState } from './sceneManager.js';
import { sendScoreToServer } from '../network/scoreSender.js';

export class GameLoop {
    /**
     * @param {HTMLCanvasElement} canvas 
     * @param {CanvasRenderingContext2D} ctx 
     * @param {import('./sceneManager.js').SceneManager} sceneManager 
     * @param {import('./input.js').InputHandler} input 
     * @param {import('./ui.js').UIManager} ui 
     */

    
    constructor(canvas, ctx, sceneManager, input, ui, options = {}) {
        this.canvas = canvas;
        this.ctx = ctx;
        this.sceneManager = sceneManager;
        this.input = input;
        this.ui = ui;

        this.showAIDebug = false; // 기본 NORMAL 모드 (디버그 오버레이 비활성화)
        this.lastTimestamp = performance.now();

        // 전역 참조 등록
        window.gameLoopInstance = this;

        // 멀티플레이 시드 바인딩 (서버 수신 시드 사용, 없을 경우 고정 시드 1004)
        this.matchSeed = (options && options.seed) || window.selectedMatchSeed || 1004;
        setGameSeed(this.matchSeed);

        // 매치 상태 데이터
        this.matchState = {
            timeRemaining: MATCH_CONFIG.DEFAULT_DURATION_SEC,
            teamScore: 0
        };

        // 메뉴 드롭다운에서 선택된 직업(bufferPlayer, defaultPlayer 등)을 읽어와 슬롯 초기화
        this.initSlots();
        this.boss = BossFactory.createBoss('neonDragon', this.canvas.width / 2, 150);
        this.playerBullets = [];
        this.bossBullets = [];
        this.minionBullets = []; // 전역 미니언 탄환 배열
        this.enemyMinions = [];  // 적군 미니언 엔티티 배열
        this.allyMinions = [];   // 아군 미니언 엔티티 배열
        this.particles = [];
        this.floatingTexts = [];

        // 💡 [UI 스킬 버튼 바인딩 연동]
        if (this.ui && typeof this.ui.bindSkillButton === 'function') {
            this.ui.bindSkillButton(() => this.slots.find(s => s.isHuman), this);
        }

        // 💡 [신규 - 네트워크 슬롯 이벤트 바인딩]: 수신된 AI 모드 전환 신호를 실시간 처리
        if (window.networkManager) {
            window.networkManager.on('SLOT_EVENT_SYNC', (packet) => {
                if (packet.eventType === 'TOGGLE_AI_MODE' && packet.payload) {
                    this.applySlotAiMode(packet.slotIndex, packet.payload.isAiMode);
                }
            });
        }

        this.init();
    }

    /**
     * 💡 [유저 스킬 시전 처리 메서드 - E키 및 UI 전용]
     */
    useUserSkill() {
        const userSlot = this.slots.find(s => s.isHuman && !s.isStunned());
        if (!userSlot || !userSlot.hasActiveSkill) return;

        const allEnemyBullets = [...this.bossBullets, ...this.minionBullets];
        const success = userSlot.useSkill({
            boss: this.boss,
            enemyMinions: this.enemyMinions,
            bossBullets: this.bossBullets,
            minionBullets: this.minionBullets,
            enemyBullets: allEnemyBullets,
            allyMinions: this.allyMinions,
            allyPlayers: this.slots
        });

        if (success) {
            this.floatingTexts.push(createFloatingText(userSlot.x, userSlot.y - 20, userSlot.skillFloatText, userSlot.themeColor));
        }
    }

    /**
     * 메인 프레임 업데이트 중 유저 입력 처리 연동 (네트워크 동기화 포함)
     */
    updateInputs() {
        const net = window.networkManager;
        const mySlotNum = (net && net.mySlotIndex) ? net.mySlotIndex : 1;
        const mySlotIdx = mySlotNum - 1;

        // 1. 내 기체 입력 액션 추출 (isAiMode 여부에 따라 수동/AI 자동 생성)
        const myPlayer = this.slots ? this.slots[mySlotIdx] : null;
        const localInputAction = this.input.getInputAction(mySlotIdx, {
            player: myPlayer,
            boss: this.boss,
            gameLoop: this
        });

        // 2. 내 컴퓨터 슬롯 조작 신호를 네트워크 소켓으로 송신 (INPUT_SYNC)
        if (net && net.mySlotIndex) {
            net.sendInputSync(net.mySlotIndex, localInputAction);
        }

        // 3. 각 슬롯별 권한 분리 및 입력/네트워크 위치 보간 동기화
        this.slots.forEach((player, idx) => {
            const slotNum = idx + 1;
            const isMySlot = (net && net.mySlotIndex === slotNum);
            player.isLocalOwner = isMySlot; // 내 소유 기체 설정

            const remoteInput = net ? net.consumeClientInput(slotNum) : null;
            if (remoteInput) {
                if (typeof remoteInput.isAiMode === 'boolean') {
                    player.isHuman = !remoteInput.isAiMode;
                }
                player.remoteInputPacket = remoteInput;
            }

            const skillParams = {
                boss: this.boss,
                enemyMinions: this.enemyMinions,
                bossBullets: this.bossBullets,
                minionBullets: this.minionBullets,
                enemyBullets: [...(this.bossBullets || []), ...(this.minionBullets || [])],
                allyMinions: this.allyMinions,
                allyPlayers: this.slots
            };

            // 💡 [핵심 - 권한 분리]: 내 슬롯(Local Owner)만 키보드/마우스 입력을 직접 계산
            if (isMySlot && player.isHuman) {
                player.handleHumanInputPacket(localInputAction, skillParams);
            } 
            // 💡 [상대 슬롯 - Remote Proxy]: 수신받은 네트워크 패킷(remoteInputPacket)으로 위치 및 스킬 1회성 적용
            else if (!isMySlot && player.isHuman && player.remoteInputPacket) {
                const pkt = player.remoteInputPacket;
                player.handleHumanInputPacket(pkt, skillParams);

                // 스킬 연속 발동 방지 플래그 소모
                if (pkt.useSkill) {
                    pkt.useSkill = false;
                }
            }
        });
    }

    /**
     * 메인 메뉴의 드롭다운 선택값(p1-class ~ p4-class)을 읽어서 각 슬롯 기체를 동적으로 생성
     */
    initSlots() {
        const net = window.networkManager;
        const mySlot = (net && net.mySlotIndex) ? net.mySlotIndex : 1;
        const activeSlots = (net && net.activeSlots) ? net.activeSlots : [1];

        this.slots = Array.from({ length: TOTAL_SLOTS }, (_, i) => {
            const slotId = i + 1;
            const classSelect = document.getElementById(`p${slotId}-class`);
            const classType = classSelect ? classSelect.value : 'defaultPlayer';
            
            const player = PlayerFactory.createPlayer(i, classType);
            
            // 실제 멀티 접속 중인 인간 유저 슬롯(activeSlots에 포함된 슬롯)은 AI 제어를 해제(isHuman = true)
            player.isHuman = activeSlots.includes(slotId);
            return player;
        });

        if (this.canvas) {
            this.slots.forEach(slot => slot.resetPosition(1280, 720, TOTAL_SLOTS));
        }
        if (this.ui) {
            this.ui.updateSlotAndStats(this.slots);
        }
    }

    /**
     * 엔티티 초기 위치 및 타이머 루프 시작
     */
    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());

        // 초당 매치 타이머 및 주기 점수 증가
        this.timerInterval = setInterval(() => {
            if (!this.sceneManager.isPlaying()) return;

            this.matchState.timeRemaining--;
            this.matchState.teamScore += MATCH_CONFIG.SCORE_PER_TICK;
            this.ui.updateHeader(this.matchState.timeRemaining, this.matchState.teamScore);

            if (this.matchState.timeRemaining <= 0) {
                this.endMatch();
            }
        }, 1000);

        this.ui.updateSlotAndStats(this.slots);
    }

    /**
     * 캔버스 리사이즈 및 슬롯 좌표 재정렬 (1280x720 고정 좌표계 유지)
     */
    resize() {
        const GAME_WIDTH = 1280;
        const GAME_HEIGHT = 720;
        this.canvas.width = GAME_WIDTH;
        this.canvas.height = GAME_HEIGHT;

        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const scale = Math.min(windowWidth / GAME_WIDTH, windowHeight / GAME_HEIGHT);

        this.canvas.style.width = `${GAME_WIDTH * scale}px`;
        this.canvas.style.height = `${GAME_HEIGHT * scale}px`;
        this.canvas.style.position = 'absolute';
        this.canvas.style.left = `${(windowWidth - GAME_WIDTH * scale) / 2}px`;
        this.canvas.style.top = `${(windowHeight - GAME_HEIGHT * scale) / 2}px`;

        if (this.slots) {
            this.slots.forEach(slot => slot.resetPosition(GAME_WIDTH, GAME_HEIGHT, TOTAL_SLOTS));
        }
    }

    /**
     * 유저 조작 슬롯의 액티브 스킬 발동 트리거 (조작 키 및 위치 타겟 전달)
     */
    useUserSkill() {
        const humanSlot = this.slots.find(s => s.isHuman && !s.isStunned());
        if (humanSlot && humanSlot.hasActiveSkill && humanSlot.gauge >= humanSlot.maxGauge) {
            const success = humanSlot.useSkill({
                keys: this.input.keys,
                mousePos: this.input.mousePos,
                boss: this.boss,
                enemyMinions: this.enemyMinions
            });
            if (success) {
                this.floatingTexts.push(createFloatingText(humanSlot.x, humanSlot.y - 20, humanSlot.skillFloatText, humanSlot.themeColor));
            }
        }
```

# 📄 [요청 3 ➡️ 불러온함수 (createFloatingText 본체)] TARGET: extraction_target_project/js/player/particle.js (71-81라인)
# ----------------------------------------------------------
```python
export function createFloatingText(x, y, text, color = '#ec4899') {
    return {
        x,
        y,
        text,
        color,
        alpha: 1.0,
        vy: -1.5,
        life: 1.0
    };
}
```

# 📄 [요청 3 ➡️ 불러온함수 (setGameSeed 본체)] TARGET: extraction_target_project/js/utils/math.js (18-23라인)
# ----------------------------------------------------------
```python
export function setGameSeed(seed) {
    currentSeed = seed;
    seededRNG.initDerivations(seed);
    // 전역 Math.random()을 독립 PRNG의 범용 난수로 덮어씌움
    Math.random = seededRandom;
}
```
