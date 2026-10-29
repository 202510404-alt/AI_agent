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
        this.elModal = document.getElementById('result-screen');
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
                // 모든 슬롯의 직업 선택을 서버에 공유한다.
                select.addEventListener('change', () => {
                    window.networkManager?.sendSlotClass(i, select.value);
                });
            }
        }

        // 닉네임은 본인 슬롯만 수정할 수 있다.
        const updateSlotLockStatus = () => {
            const selectedRadio = document.querySelector('input[name="my-slot-select"]:checked');
            const mySlotNum = selectedRadio ? parseInt(selectedRadio.value, 10) : 1;

            for (let i = 1; i <= 4; i++) {
                const nameInput = document.getElementById(`p${i}-nickname`);
                const isMySlot = (i === mySlotNum);

                if (nameInput) {
                    nameInput.disabled = !isMySlot;
                    nameInput.style.opacity = isMySlot ? '1.0' : '0.4';
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
            this.elBombBtn.style.display = isDebug ? 'flex' : 'none';
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
                if (window.networkManager) {
                    window.networkManager.sendDebugInput('UI_BUTTON', `Debug Toggle Click (Status: ${this.showAIDebug})`);
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

    }

    /**
     * 💡 [유저 스킬 버튼 및 상단 점수창 옆 AI ON/OFF 토글 버튼 연동]
     */
    bindSkillButton(getUserPlayerFn, gameLoopInstance) {
        // 1. 상단 점수창 옆 AI ON/OFF 토글 버튼 이벤트 바인딩
        const topAiToggleBtn = document.getElementById('btn-top-ai-toggle');
        if (topAiToggleBtn) {
            topAiToggleBtn.onclick = () => {
                const mySlotNum = (window.networkManager && window.networkManager.mySlotIndex) 
                    ? window.networkManager.mySlotIndex 
                    : 1;
                const mySlotIdx = mySlotNum - 1;
                
                const myPlayer = gameLoopInstance.slots ? gameLoopInstance.slots[mySlotIdx] : null;

                if (myPlayer) {
                    // 전환할 목표 AI 모드 상태 (현재 isHuman이 true이면 AI 모드 true로 전환)
                    const targetAiMode = myPlayer.isHuman; 

                    // 💡 [Strict Sync]: 클라이언트 단독 즉시 변경 금지 -> 서버로 요청 후 ROOM_STATE로 수신 적용
                    if (window.networkManager && typeof window.networkManager.requestToggleAiMode === 'function') {
                        window.networkManager.requestToggleAiMode(mySlotNum, targetAiMode);
                    } else if (window.networkManager && typeof window.networkManager.sendSlotEvent === 'function') {
                        window.networkManager.sendSlotEvent(mySlotNum, 'TOGGLE_AI_MODE', {
                            isAiMode: targetAiMode
                        });
                    } else {
                        // 소켓 연결 없는 오프라인 폴백 처리
                        if (gameLoopInstance && typeof gameLoopInstance.applySlotAiMode === 'function') {
                            gameLoopInstance.applySlotAiMode(mySlotNum, targetAiMode);
                        }
                    }
                }
            };
        }

        // 스킬 버튼은 bindEvents의 단일 핸들러를 통해 GameLoop로 전달한다.
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
                const net = window.networkManager;
                const nextAiMode = slot.isHuman;
                if (net && typeof net.requestToggleAiMode === 'function') {
                    net.requestToggleAiMode(slot.slotIndex + 1, nextAiMode);
                } else if (window.gameLoopInstance && typeof window.gameLoopInstance.applySlotAiMode === 'function') {
                    window.gameLoopInstance.applySlotAiMode(slot.slotIndex + 1, nextAiMode);
                }
                if (this.callbacks.onSlotToggle) {
                    this.callbacks.onSlotToggle(slot);
                }
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
    showGameOverModal(slots, score = 0, players = null) {
        if (!this.elScoreboardList || !this.elModal) return;

        const scoreDisplay = document.getElementById('final-score-val');
        if (scoreDisplay) scoreDisplay.textContent = Math.floor(score).toString().padStart(6, '0');
        this.elScoreboardList.innerHTML = '';
        const sorted = [...slots].sort((a, b) => b.damageDealt - a.damageDealt);

        sorted.forEach((s, idx) => {
            const row = document.createElement('div');
            row.className = "flex justify-between items-center p-2 rounded bg-slate-900 border border-slate-800";
            const participant = players?.find(p => p.slotIndex === s.id);
            const connected = participant ? participant.connected : !!window.networkManager?.activeSlots?.includes(s.id);
            const name = document.createElement('span');
            name.className = 'font-bold';
            name.style.color = s.color;
            name.textContent = `${idx + 1}. ${participant?.nickname || s.nickname || `SLOT ${s.id}`} (${connected ? '유저' : 'AI 봇'})`;
            const damage = document.createElement('span');
            damage.className = 'text-cyan-300 font-bold';
            damage.textContent = `${Math.floor(s.damageDealt).toLocaleString()} DMG`;
            row.appendChild(name);
            row.appendChild(damage);
            this.elScoreboardList.appendChild(row);
        });

        this.elModal.classList.remove('hidden');
        const voteStatus = document.getElementById('vote-status');
        if (voteStatus) voteStatus.textContent = '전원 같은 선택을 하면 함께 이동합니다.';
    }

    async loadRankings() {
        const list = document.getElementById('ranking-list');
        if (!list) return;
        list.textContent = '랭킹을 불러오는 중...';
        try {
            const response = await fetch('/api/rankings', { cache: 'no-store' });
            if (!response.ok) throw new Error('랭킹 조회 실패');
            const rankings = await response.json();
            list.textContent = '';
            if (!rankings.length) list.textContent = '아직 기록이 없습니다.';
            rankings.slice(0, 20).forEach((entry, index) => {
                const row = document.createElement('div');
                row.className = 'rounded bg-slate-900 p-2 border border-slate-700';
                const title = document.createElement('div');
                title.className = 'font-bold text-cyan-300';
                title.textContent = `${index + 1}위 · ${Number(entry.score).toLocaleString()}점 · ${new Date(entry.playedAt).toLocaleDateString('ko-KR')}`;
                const names = document.createElement('div');
                names.className = 'mt-1 text-slate-300 break-words';
                names.textContent = (entry.players || []).map(p => p.nickname).join(' · ');
                row.appendChild(title);
                row.appendChild(names);
                list.appendChild(row);
            });
        } catch (error) {
            list.textContent = '랭킹을 불러오지 못했습니다.';
        }
    }

    updateVoteStatus(votes = {}, mySlotIndex = null) {
        const status = document.getElementById('vote-status');
        if (!status) return;
        const choices = Object.values(votes);
        const voted = choices.filter(Boolean).length;
        const mine = votes[mySlotIndex];
        status.textContent = `투표 ${voted}/${choices.length}명 · 내 선택: ${mine === 'REPLAY' ? '다시 시작' : mine === 'MENU' ? '메인 메뉴' : '대기 중'} · 전원 같은 선택 시 이동`;
    }

    /**
     * LOBBY 페이즈 슬롯 카드 상태 갱신
     * @param {Array} slotDetails 서버에서 수신한 슬롯 상세 배열 [{ slotIndex, active, ready, vote }]
     * @param {number} mySlotIndex 내 슬롯 번호 (1~4)
     */
    updateLobbySlots(slotDetails = [], mySlotIndex = null) {
        if (!slotDetails || !Array.isArray(slotDetails)) return;

        slotDetails.forEach(slot => {
            const idx = slot.slotIndex;
            const card = document.getElementById(`lobby-slot-card-${idx}`);
            if (!card) return;

            const connBadge = card.querySelector('.slot-conn-badge');
            const readyBadge = card.querySelector('.slot-ready-badge');
            const nicknameEl = card.querySelector('.slot-nickname');
            const classEl = card.querySelector('.slot-class');

            // 닉네임 및 선택 캐릭터 정보 가져오기 (인풋 또는 서버 detail 우선)
            const nicknameInput = document.getElementById(`p${idx}-nickname`);
            const classSelect = document.getElementById(`p${idx}-class`);
            
            // 💡 [Strict Sync]: 서버가 보낸 slot.nickname, slot.classType 우선 적용
            const nickname = slot.nickname || ((nicknameInput && nicknameInput.value.trim()) ? nicknameInput.value.trim() : `PLAYER ${idx}`);
            let className = '기본 기체';
            if (slot.classType && classSelect) {
                const opt = classSelect.querySelector(`option[value="${slot.classType}"]`);
                if (opt) className = opt.text;
            } else if (classSelect && classSelect.options[classSelect.selectedIndex]) {
                className = classSelect.options[classSelect.selectedIndex].text;
            }

            // 인풋 값도 서버 중앙 데이터와 동기화
            if (nicknameInput && slot.nickname && nicknameInput.value !== slot.nickname) {
                nicknameInput.value = slot.nickname;
            }
            if (classSelect && slot.classType && classSelect.value !== slot.classType) {
                classSelect.value = slot.classType;
            }

            const isMySlot = (mySlotIndex === idx);

            // 접속 상태 표시 (active)
            if (slot.active) {
                if (connBadge) {
                    connBadge.textContent = isMySlot ? 'YOU' : 'ONLINE';
                    connBadge.className = `slot-conn-badge text-[9px] px-1.5 py-0.5 rounded font-bold ${
                        isMySlot ? 'bg-cyan-500 text-black' : 'bg-blue-600 text-white'
                    }`;
                }
                if (nicknameEl) {
                    nicknameEl.textContent = nickname;
                    nicknameEl.className = 'text-sm font-bold text-white slot-nickname truncate';
                }
                if (classEl) {
                    classEl.innerHTML = `<i class="fa-solid fa-gamepad mr-1"></i>${className}`;
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

                // 카드 테두리 강조
                if (slot.ready) {
                    card.style.borderColor = 'rgba(16, 185, 129, 0.8)';
                    card.style.boxShadow = '0 0 10px rgba(16, 185, 129, 0.2)';
                } else {
                    card.style.borderColor = '';
                    card.style.boxShadow = '';
                }
            } else {
                // 미접속 상태
                if (connBadge) {
                    connBadge.textContent = 'EMPTY';
                    connBadge.className = 'slot-conn-badge text-[9px] px-1.5 py-0.5 rounded font-bold bg-gray-800 text-gray-500';
                }
                if (readyBadge) {
                    readyBadge.textContent = 'WAITING';
                    readyBadge.className = 'slot-ready-badge text-[10px] px-2 py-0.5 rounded font-black bg-gray-800 text-gray-600';
                }
                if (nicknameEl) {
                    nicknameEl.textContent = '대기 중...';
                    nicknameEl.className = 'text-sm font-bold text-gray-600 slot-nickname truncate';
                }
                if (classEl) {
                    classEl.innerHTML = `<i class="fa-solid fa-crosshairs mr-1"></i>미선택`;
                    classEl.className = 'text-xs text-gray-600 slot-class truncate';
                }
                card.style.borderColor = '';
                card.style.boxShadow = '';
            }
        });
    }
}

export default UIManager;
