/**
 * js/core/ui.js
 * 슬롯 제어 패널, 실시간 딜량/실수 통계 표기, 게임 종료 모달 제어
 */

import { getAutoDiscoveredClasses } from '../player/characters/index.js';

export class UIManager {
    /**
     * @param {object} callbacks 
     * @param {Function} callbacks.onSlotToggle 슬롯 모드(User/AI) 변경 시 호출
     * @param {Function} callbacks.onToggleDebug 디버그 시각화 토글 시 호출
     * @param {Function} callbacks.onUseSkill 액티브 스킬 발동 시 호출
     * @param {Function} callbacks.onUseBomb EMP 특수폭탄 발동 시 호출
     * @param {Function} callbacks.onRestart 새 매치 시작 시 호출
     */
    constructor(callbacks = {}) {
        this.callbacks = callbacks;
        this.showAIDebug = true;

        this.elTimer = document.getElementById('matchTimerDisplay');
        this.elTeamScore = document.getElementById('teamScoreDisplay');
        this.elSlotContainer = document.getElementById('slotControlsContainer');
        this.elLiveStats = document.getElementById('liveStatsContainer');
        this.elDebugBtn = document.getElementById('btnToggleDebug');
        this.elDebugStatus = document.getElementById('debugStatusText');
        this.elBombBtn = document.getElementById('btnSpecialBomb');
        this.elModal = document.getElementById('gameOverModal');
        this.elScoreboardList = document.getElementById('finalScoreboardList');
        this.elRestartBtn = document.getElementById('btnRestartMatch');

        // 스킬 버튼 요소
        this.elSkillBtn = document.getElementById('btnActiveSkill');
        this.elSkillFill = document.getElementById('skillGaugeFill');
        this.elSkillText = document.getElementById('skillGaugeText');
        this.elSkillIcon = this.elSkillBtn ? this.elSkillBtn.querySelector('i') : null;

        this.populateClassDropdowns();
        this.bindEvents();
    }

    /**
     * characters 폴더 자동 검색을 통해 메뉴 드롭다운 갱신
     */
    populateClassDropdowns() {
        const discoveredClasses = getAutoDiscoveredClasses();

        for (let i = 1; i <= 4; i++) {
            const select = document.getElementById(`p${i}-class`);
            if (select) {
                select.innerHTML = '';
                discoveredClasses.forEach(cls => {
                    const opt = document.createElement('option');
                    opt.value = cls.id;       // 파일명 ID (예: 'bufferPlayer')
                    opt.innerText = cls.name; // 캐릭터 내부 이름
                    select.appendChild(opt);
                });
                
                // 각 슬롯별로 다양한 초기 캐릭터 배치
                const defaultClasses = ['bufferPlayer', 'empPlayer', 'shielderPlayer', 'summonerPlayer'];
                const defaultChoice = defaultClasses[i - 1] || 'defaultPlayer';
                if (select.querySelector(`option[value="${defaultChoice}"]`)) {
                    select.value = defaultChoice;
                }
            }
        }

        // 💡 [다른 사람 슬롯 수정 방지]: 라디오 버튼 변경 시 내 슬롯 외에는 전부 disabled 잠금 처리
        const updateSlotLockStatus = () => {
            const selectedRadio = document.querySelector('input[name="my-slot-select"]:checked');
            const mySlotNum = selectedRadio ? parseInt(selectedRadio.value, 10) : 1;

            for (let i = 1; i <= 4; i++) {
                const nameInput = document.getElementById(`p${i}-nickname`);
                const classSelect = document.getElementById(`p${i}-class`);
                const isMySlot = (i === mySlotNum);

                if (nameInput) {
                    nameInput.disabled = !isMySlot;
                    nameInput.style.opacity = isMySlot ? '1.0' : '0.4';
                }
                if (classSelect) {
                    classSelect.disabled = !isMySlot;
                    classSelect.style.opacity = isMySlot ? '1.0' : '0.4';
                }
            }
        };

        // 라디오 버튼 이벤트 바인딩 및 최초 실행
        const radios = document.querySelectorAll('input[name="my-slot-select"]');
        radios.forEach(radio => {
            radio.addEventListener('change', updateSlotLockStatus);
        });
        updateSlotLockStatus();
    }

    /**
     * P3 k090207 치트키 성공 여부에 따라 상단 디버그 버튼 및 무한 EMP 버튼 표시 제어
     * @param {boolean} isDebug 
     */
    setDebugVisibility(isDebug) {
        if (this.elDebugBtn) {
            if (isDebug) {
                this.elDebugBtn.classList.remove('hidden');
                this.showAIDebug = true;
                if (this.elDebugStatus) {
                    this.elDebugStatus.innerText = 'ON';
                    this.elDebugStatus.className = 'text-emerald-400';
                }
            } else {
                this.elDebugBtn.classList.add('hidden');
                this.showAIDebug = false;
                if (this.elDebugStatus) {
                    this.elDebugStatus.innerText = 'OFF';
                    this.elDebugStatus.className = 'text-gray-500';
                }
            }
        }

        // k090207 치트키 성공시에만 무제한 EMP 폭탄 버튼 표시
        if (this.elBombBtn) {
            if (isDebug) {
                this.elBombBtn.classList.remove('hidden');
            } else {
                this.elBombBtn.classList.add('hidden');
            }
        }

        // 💡 [우측 패널 디버그 모드 연동]: 디버그 모드 시에만 우측 슬롯 제어/통계 창 표시
        const rightPanel = document.getElementById('right-debug-panel');
        if (rightPanel) {
            if (isDebug) {
                rightPanel.classList.remove('hidden');
            } else {
                rightPanel.classList.add('hidden');
            }
        }

        // 💡 [k090207 디버그 모드]: 폰 접속용 QR 코드 및 IP URL 표시
        const netInfoContainer = document.getElementById('debug-network-info');
        const qrImg = document.getElementById('qr-code-img');
        const hostUrlText = document.getElementById('host-ip-url');

        if (netInfoContainer) {
            if (isDebug) {
                netInfoContainer.classList.remove('hidden');
                
                // 현재 호스트 IP 조합 (localhost인 경우 안내 문구)
                const currentHost = window.location.hostname || 'localhost';
                const port = window.location.port ? `:${window.location.port}` : '';
                const joinUrl = `http://${currentHost}${port}?client=true&host=${currentHost}`;

                if (hostUrlText) hostUrlText.innerText = joinUrl;
                if (qrImg) {
                    qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(joinUrl)}`;
                }
            } else {
                netInfoContainer.classList.add('hidden');
            }
        }
    }
    /**
     * 버튼 이벤트 리스너 등록
     */
    bindEvents() {
        if (this.elDebugBtn) {
            this.elDebugBtn.addEventListener('click', () => {
                this.showAIDebug = !this.showAIDebug;
                if (this.elDebugStatus) {
                    this.elDebugStatus.innerText = this.showAIDebug ? 'ON' : 'OFF';
                    this.elDebugStatus.className = this.showAIDebug ? 'text-emerald-400' : 'text-gray-500';
                }
                if (this.callbacks.onToggleDebug) {
                    this.callbacks.onToggleDebug(this.showAIDebug);
                }
            });
        }

        if (this.elSkillBtn) {
            this.elSkillBtn.addEventListener('click', () => {
                if (this.callbacks.onUseSkill) {
                    this.callbacks.onUseSkill();
                }
            });
        }

        if (this.elBombBtn) {
            this.elBombBtn.addEventListener('click', () => {
                if (this.callbacks.onUseBomb) {
                    this.callbacks.onUseBomb();
                }
            });
        }

        if (this.elRestartBtn) {
            this.elRestartBtn.addEventListener('click', () => {
                if (this.callbacks.onRestart) {
                    this.callbacks.onRestart();
                } else {
                    window.location.reload();
                }
            });
        }
    }

    /**
     * 💡 [유저 스킬 버튼 및 상단 점수창 옆 AI ON/OFF 토글 버튼 연동]
     */
    bindSkillButton(getUserPlayerFn, gameLoopInstance) {
        // 1. 상단 점수창 옆 AI ON/OFF 토글 버튼 이벤트 바인딩
        const topAiToggleBtn = document.getElementById('btn-top-ai-toggle');
        if (topAiToggleBtn) {
            topAiToggleBtn.onclick = () => {
                const mySlotIdx = (window.networkManager && window.networkManager.mySlotIndex) 
                    ? window.networkManager.mySlotIndex - 1 
                    : 0;
                
                // 내 컴퓨터에 할당된 기체 슬롯을 정확히 탐색
                const myPlayer = gameLoopInstance.slots ? gameLoopInstance.slots[mySlotIdx] : null;

                if (myPlayer) {
                    myPlayer.isHuman = !myPlayer.isHuman; // 내 기체만 유저/AI 수동 전환
                    const statusText = document.getElementById('top-ai-status-text');
                    if (statusText) {
                        statusText.innerText = myPlayer.isHuman ? 'USER (MANUAL)' : 'AI (AUTO)';
                        statusText.className = myPlayer.isHuman ? 'text-cyan-400 font-bold' : 'text-pink-400 font-bold';
                    }
                }
            };
        }

        // 2. 우측 하단 스킬 버튼 클릭/터치 이벤트 핸들러 연동
        if (!this.elSkillBtn) return;

        const triggerSkill = () => {
            const userPlayer = typeof getUserPlayerFn === 'function' ? getUserPlayerFn() : null;
            if (!userPlayer || typeof userPlayer.useSkill !== 'function') return;

            const allEnemyBullets = [
                ...(gameLoopInstance.bossBullets || []),
                ...(gameLoopInstance.minionBullets || [])
            ];

            const success = userPlayer.useSkill({
                boss: gameLoopInstance.boss,
                enemyMinions: gameLoopInstance.enemyMinions,
                bossBullets: gameLoopInstance.bossBullets,
                minionBullets: gameLoopInstance.minionBullets,
                enemyBullets: allEnemyBullets,
                allyMinions: gameLoopInstance.allyMinions,
                allyPlayers: gameLoopInstance.slots
            });

            if (success && Array.isArray(gameLoopInstance.floatingTexts)) {
                gameLoopInstance.floatingTexts.push({
                    x: userPlayer.x,
                    y: userPlayer.y - 20,
                    text: userPlayer.skillFloatText || 'SKILL ACTIVATED!',
                    color: userPlayer.themeColor || '#10b981',
                    alpha: 1.0,
                    vy: -1.5,
                    life: 1.0
                });
            }
        };

        // 기존 이벤트 중복 방지 후 신규 등록
        this.elSkillBtn.onclick = triggerSkill;
    }

    /**
     * 캐릭터 스펙(hasActiveSkill, maxGauge, themeColor, skillIconClass) 기반 UI 동적 조립
     */
    updateSkillButton(userPlayer) {
        if (!this.elSkillBtn || !userPlayer) return;

        if (!userPlayer.hasActiveSkill) {
            this.elSkillBtn.classList.add('hidden');
            return;
        }

        this.elSkillBtn.classList.remove('hidden');

        // 캐릭터 아이콘 및 테마 색상 적용
        if (this.elSkillIcon && userPlayer.skillIconClass) {
            this.elSkillIcon.className = `${userPlayer.skillIconClass} text-base mb-0.5`;
        }
        this.elSkillBtn.style.borderColor = userPlayer.themeColor;
        this.elSkillBtn.style.color = userPlayer.themeColor;

        if (!this.elSkillFill || !this.elSkillText) return;

        // 게이지 비율 동적 산출 (70, 50, 100 등)
        const ratio = Math.min(1.0, userPlayer.gauge / userPlayer.maxGauge);
        const percent = Math.floor(ratio * 100);

        this.elSkillFill.style.height = `${percent}%`;
        this.elSkillFill.style.backgroundColor = userPlayer.themeColor;
        this.elSkillText.innerText = `${percent}%`;

        if (percent >= 100) {
            this.elSkillBtn.classList.add('animate-bounce');
        } else {
            this.elSkillBtn.classList.remove('animate-bounce');
        }
    }

    /**
     * HUD 타이머 및 팀 점수 표기 갱신
     * @param {number} timeRemaining 
     * @param {number} score 
     */
    updateHeader(timeRemaining, score) {
        if (this.elTimer) {
            const m = Math.floor(Math.max(0, timeRemaining) / 60).toString().padStart(2, '0');
            const s = (Math.floor(Math.max(0, timeRemaining)) % 60).toString().padStart(2, '0');
            this.elTimer.innerText = `${m}:${s}`;
        }
        if (this.elTeamScore) {
            this.elTeamScore.innerText = Math.floor(score).toString().padStart(6, '0');
        }
    }

    /**
     * 슬롯 제어 버튼 및 실시간 딜량/실수 통계 렌더링
     * @param {Array} slots 
     */
    updateSlotAndStats(slots) {
        if (!this.elSlotContainer || !this.elLiveStats) return;

        // 1. 슬롯 제어 UI (유저 난입 / AI 제어 토글)
        this.elSlotContainer.innerHTML = '';
        slots.forEach((slot) => {
            const btn = document.createElement('button');
            btn.className = `p-1.5 rounded-lg text-left border transition ${
                slot.isHuman 
                    ? 'bg-cyan-950 border-cyan-400 text-cyan-200 hover:bg-cyan-900' 
                    : 'bg-slate-800 border-slate-700 text-gray-300 hover:bg-slate-700'
            }`;

            btn.innerHTML = `
                <div class="flex justify-between items-center">
                    <span class="font-bold text-[10px]" style="color: ${slot.color}">SLOT ${slot.id}</span>
                    <span class="text-[8px] px-1 rounded ${slot.isHuman ? 'bg-cyan-500 text-black font-extrabold' : 'bg-gray-700 text-gray-300'}">
                        ${slot.isHuman ? 'USER' : 'AI'}
                    </span>
                </div>
                <span class="text-[9px] text-gray-400 block mt-0.5">${slot.isHuman ? 'AI로 전환' : '유저 난입'}</span>
            `;

            btn.onclick = () => {
                slot.isHuman = !slot.isHuman;
                if (this.callbacks.onSlotToggle) {
                    this.callbacks.onSlotToggle(slot);
                }
                this.updateSlotAndStats(slots);
            };
            this.elSlotContainer.appendChild(btn);
        });

        // 2. 실시간 딜량 & AI 실수 랭킹 집계
        this.elLiveStats.innerHTML = '';
        slots.forEach((s) => {
            const row = document.createElement('div');
            row.className = "bg-slate-950 p-1.5 rounded border border-slate-800 flex justify-between items-center text-[10px]";
            row.innerHTML = `
                <div class="flex items-center gap-1.5">
                    <span class="font-bold" style="color: ${s.color}">P${s.id} [${s.isHuman ? 'USER' : 'AI'}]</span>
                </div>
                <div class="text-right">
                    <span class="text-cyan-300 font-bold">${Math.floor(s.damageDealt).toLocaleString()} DMG</span>
                    ${!s.isHuman ? `<span class="text-pink-400 font-bold ml-1.5">(${s.mistakesCount} 실수)</span>` : ''}
                </div>
            `;
            this.elLiveStats.appendChild(row);
        });
    }

    /**
     * 경기 종료 후 최종 스코어보드 모달 표시
     * @param {Array} slots 
     */
    showGameOverModal(slots) {
        if (!this.elScoreboardList || !this.elModal) return;

        this.elScoreboardList.innerHTML = '';
        const sorted = [...slots].sort((a, b) => b.damageDealt - a.damageDealt);

        sorted.forEach((s, idx) => {
            const row = document.createElement('div');
            row.className = "flex justify-between items-center p-2 rounded bg-slate-900 border border-slate-800";
            row.innerHTML = `
                <div class="flex items-center gap-2">
                    <span class="font-bold text-gray-500">${idx + 1}.</span>
                    <span class="font-bold" style="color: ${s.color}">SLOT ${s.id} (${s.isHuman ? '유저' : 'AI 봇'})</span>
                </div>
                <div class="text-right">
                    <span class="text-cyan-300 font-bold">${Math.floor(s.damageDealt).toLocaleString()} DMG</span>
                    <span class="text-pink-400 text-[10px] ml-2">(${s.mistakesCount} 실수)</span>
                </div>
            `;
            this.elScoreboardList.appendChild(row);
        });

        this.elModal.classList.remove('hidden');
    }
}

export default UIManager;
