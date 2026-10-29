/**
 * js/core/gameLoop.js
 * 메인 60fps requestAnimationFrame 루프, 충돌 판정, AI 시각화 및 렌더링 결합
 */
import { TOTAL_SLOTS, MATCH_CONFIG, CANVAS_GRID_SIZE } from '../config/constants.js';
import { PlayerFactory } from '../player/playerFactory.js';
import { PlayerBullet } from '../player/playerBullet.js';
import { BossFactory } from '../enemy/bossFactory.js';
import { AIEngine } from '../ai/aiEngine.js';
import { createImpactParticles, createFloatingText } from '../player/particle.js';
import { setGameSeed } from '../utils/math.js';
import { GameState } from './sceneManager.js';

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
        this.gameTime = 0;
        this.matchSecondAccumulator = 0;
        this.simulationAccumulator = 0;
        this.aiSyncAccumulator = 0;
        this.aiStateSequence = 0;
        this.lastAiStateSequence = -1;
        this.lastAiAuthoritySlot = null;
        this.hasRemoteAiState = false;
        this.scoreboardRequestSent = false;
        this.scoreboardShown = false;
        this.localSkillSequence = 0;
        this.lastRemoteSkillSequence = {};
        this.pendingSkillSlots = new Map();
        this.matchGeneration = 0;
        this.bossRevision = 0;
        this.pendingBossTransition = false;

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
            this.ui.bindSkillButton(() => this.slots.find(s => s.isLocalOwner) || this.slots.find(s => s.isHuman), this);
        }

        // 💡 [네트워크 이벤트 바인딩 - 4단계 신호 표준 규격]
        if (window.networkManager) {
            // A. 상태 관리 신호 (Strict Sync): AI 모드 전환 등
            window.networkManager.on('SLOT_EVENT_SYNC', (packet) => {
                if (packet.eventType === 'TOGGLE_AI_MODE' && packet.payload) {
                    this.applySlotAiMode(packet.slotIndex, packet.payload.isAiMode);
                }
            });

            // B. 설치형 오브젝트 & HP 동기화 (Object & HP Sync - Owner Authority)
            window.networkManager.on('OBJECT_STATE_SYNC', (packet) => {
                this.handleObjectStateSync(packet);
            });
            window.networkManager.on('AI_STATE_SYNC', (packet) => {
                this.applyAiStateSync(packet);
            });
            window.networkManager.on('PLAYER_SHOT_SYNC', (packet) => {
                const net = window.networkManager;
                const slot = this.slots?.[packet.slotIndex - 1];
                if (!this.sceneManager.isPlaying() || packet.slotIndex === net.mySlotIndex ||
                    !slot || !slot.isHuman || !Number.isFinite(packet.x) ||
                    !Number.isFinite(packet.y) || !Number.isFinite(packet.angle) ||
                    !Number.isFinite(packet.damage)) return;
                const bullet = new PlayerBullet(packet.x, packet.y, packet.angle, slot.slotIndex, slot.color);
                bullet.damage = packet.damage;
                this.playerBullets.push(bullet);
            });
            window.networkManager.on('AI_SHOT_SYNC', (packet) => {
                const slot = this.slots?.[packet.slotIndex - 1];
                if (!this.sceneManager.isPlaying() || !slot || slot.isHuman ||
                    !Number.isFinite(packet.x) || !Number.isFinite(packet.y) ||
                    !Number.isFinite(packet.angle) || !Number.isFinite(packet.damage) ||
                    !Number.isFinite(packet.executeAt) || !Number.isFinite(packet.serverSentAt)) return;
                const generation = this.matchGeneration;
                const delay = window.networkManager.getSkillExecutionDelay(packet.executeAt, packet.serverSentAt);
                setTimeout(() => {
                    if (generation !== this.matchGeneration || !this.sceneManager.isPlaying()) return;
                    const bullet = new PlayerBullet(packet.x, packet.y, packet.angle, slot.slotIndex, slot.color);
                    bullet.damage = packet.damage;
                    this.playerBullets.push(bullet);
                    if (slot.isLocalOwner) window.gameAudio?.play('shoot');
                }, delay);
            });
            window.networkManager.on('PLAYER_SKILL_SYNC', (packet) => {
                this.applyRemoteSkill(packet);
            });
            window.networkManager.on('BOSS_TRANSITION', (packet) => {
                this.syncBossState(packet.bossType, packet.revision, true);
            });
        }

        this.init();
    }

    /**
     * 메인 프레임 업데이트 중 유저 입력 처리 연동 (네트워크 동기화 포함)
     * [IsLocalOwner / RemoteProxy 권한 분리 및 Client Prediction]
     */
    updateInputs(dt = 0.016) {
        const net = window.networkManager;
        const mySlotNum = (net && net.mySlotIndex) ? net.mySlotIndex : 1;
        const mySlotIdx = mySlotNum - 1;

        this.slots.forEach((player, idx) => {
            player.isLocalOwner = idx === mySlotIdx;
        });

        // 1. 내 기체 입력 액션 추출 (isAiMode 여부에 따라 수동/AI 자동 생성)
        const myPlayer = this.slots ? this.slots[mySlotIdx] : null;
        let localInputAction = null;

        if (myPlayer && myPlayer.isLocalOwner && myPlayer.isHuman && mySlotIdx === mySlotNum - 1) {
            localInputAction = this.input.getInputAction(mySlotIdx, {
                player: myPlayer,
                boss: this.boss,
                gameLoop: this
            });

            // 내 위치 좌표를 입력 패킷에 실어 Dead Reckoning 기준점 제공
            localInputAction.posX = myPlayer.x;
            localInputAction.posY = myPlayer.y;
            localInputAction.speed = myPlayer.speed;

            // 2. 내 컴퓨터 슬롯 조작 신호를 네트워크 소켓으로 프레임 단위 송신 (INPUT_SYNC)
            if (net && net.mySlotIndex === mySlotNum) {
                net.sendInputSync(net.mySlotIndex, localInputAction);
            }
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

        // 3. 각 슬롯별 권한 분리(IsLocalOwner vs RemoteProxy) 및 위치 보간
        this.slots.forEach((player, idx) => {
            const slotNum = idx + 1;
            const isMySlot = slotNum === mySlotNum;
            player.isLocalOwner = isMySlot; // 내 소유 기체 권한 플래그

            if (isMySlot) {
                // 💡 [Local Owner]: 키보드/마우스 입력을 내 기기에 즉시 실행 (Client Prediction)
                if (player.isHuman && localInputAction) {
                    player.handleHumanInputPacket(localInputAction, skillParams);
                    if (localInputAction.useSkill) this.useUserSkill();
                }
            } else {
                // 💡 [Remote Proxy]: 상대방 기기에서 릴레이된 원격 패킷 소비
                const remoteInput = net ? net.consumeClientInput(slotNum) : null;
                if (remoteInput) {
                    if (typeof remoteInput.isAiMode === 'boolean') {
                        player.isHuman = !remoteInput.isAiMode;
                    }
                    player.remoteInputPacket = remoteInput;
                    
                    if (player.isHuman) {
                        // Dead Reckoning 미세 속도 보간 및 1회성 스킬 적용
                        player.handleHumanInputPacket(remoteInput, skillParams);
                    }
                }
            }
        });
    }

    isAiAuthority() {
        const net = window.networkManager;
        if (!net || !net.socket || net.socket.readyState !== 1) return true;
        const activeSlots = (net.activeSlots || []).filter(Number.isInteger);
        return net.mySlotIndex === Math.min(...activeSlots);
    }

    syncBossState(bossType, revision, awardKill = false) {
        if (!['neonDragon', 'necromancer'].includes(bossType) ||
            !Number.isInteger(revision) || revision <= this.bossRevision) return false;
        if (Array.isArray(this.boss?.hatchlings)) this.boss.hatchlings.forEach(h => { h.isDead = true; });
        if (awardKill) this.matchState.teamScore += MATCH_CONFIG.SCORE_ON_BOSS_KILL;
        this.boss = BossFactory.createBoss(bossType, this.canvas.width / 2, 150);
        this.bossRevision = revision;
        this.pendingBossTransition = false;
        return true;
    }

    handleBossDeath() {
        if (!this.boss?.isDead || this.pendingBossTransition || !this.isAiAuthority()) return;
        const revision = this.bossRevision + 1;
        const nextType = BossFactory.getNextBossType(this.boss.type, revision);
        if (!nextType) return;
        this.pendingBossTransition = true;
        const net = window.networkManager;
        if (!net?.socket || net.socket.readyState !== 1) {
            this.syncBossState(nextType, revision, true);
        } else {
            net.requestBossTransition(this.boss.type, nextType, revision);
        }
    }

    applyAiStateSync(packet) {
        if (this.isAiAuthority() || !this.sceneManager.isPlaying() || !Array.isArray(packet.slots)) return;
        if (packet.authoritySlot !== this.lastAiAuthoritySlot) {
            this.lastAiAuthoritySlot = packet.authoritySlot;
            this.lastAiStateSequence = -1;
        }
        if (!Number.isInteger(packet.sequence) || packet.sequence <= this.lastAiStateSequence) return;
        this.lastAiStateSequence = packet.sequence;

        for (const state of packet.slots) {
            if (!state || !Number.isInteger(state.slotIndex)) continue;
            const player = this.slots[state.slotIndex];
            if (!player || player.isHuman || !Number.isFinite(state.x) || !Number.isFinite(state.y) ||
                !Number.isFinite(state.targetX) || !Number.isFinite(state.targetY)) continue;
            for (const key of ['x', 'y', 'targetX', 'targetY', 'fsmState', 'dodgeFatigue',
                'actionLockTimer', 'repositionStrategy', 'wallAvoidSide', 'repositionAngleOffset',
                'dodgeAngleOffset', 'mistakesCount', 'attackCooldown', 'hp', 'stunTimer', 'gauge']) {
                if (state[key] !== undefined) player[key] = state[key];
            }
            if (player.classType === 'shielderPlayer') player.activeShield = state.activeShield || null;
        }
        this.hasRemoteAiState = true;
    }

    sendAiStateSync(dt) {
        const net = window.networkManager;
        if (!net || !net.socket || net.socket.readyState !== 1 || !this.isAiAuthority()) return;
        this.aiSyncAccumulator += dt;

        // 💡 [5배 빠른 10ms(0.01초) 동기화]: 뚝뚝 끊김 완치 및 초고속 갱신
        if (this.aiSyncAccumulator < 0.01) return;
        this.aiSyncAccumulator %= 0.01;
        net.sendAiStateSync(++this.aiStateSequence, this.slots.filter(player => !player.isHuman).map(player => ({
            slotIndex: player.slotIndex,
            x: player.x, y: player.y, targetX: player.targetX, targetY: player.targetY,
            fsmState: player.fsmState, dodgeFatigue: player.dodgeFatigue,
            actionLockTimer: player.actionLockTimer, repositionStrategy: player.repositionStrategy,
            wallAvoidSide: player.wallAvoidSide, repositionAngleOffset: player.repositionAngleOffset,
            dodgeAngleOffset: player.dodgeAngleOffset, mistakesCount: player.mistakesCount,
            attackCooldown: player.attackCooldown, hp: player.hp, stunTimer: player.stunTimer,
            gauge: player.gauge,
            activeShield: player.classType === 'shielderPlayer' ? player.activeShield : undefined
        })));
    }

    /**
     * 메인 메뉴의 드롭다운 선택값(p1-class ~ p4-class)을 읽어서 각 슬롯 기체를 동적으로 생성
     */
    initSlots(masterSeed = null, slotDetails = null) {
        if (masterSeed !== null && masterSeed !== undefined) this.matchSeed = masterSeed;
        const net = window.networkManager;
        const mySlot = (net && net.mySlotIndex) ? net.mySlotIndex : 1;
        const activeSlots = (net && net.activeSlots) ? net.activeSlots : [1];
        const serverSlots = slotDetails || (net && net.slotDetails) || [];

        if (!this.sceneManager.isPlaying()) {
            this.gameTime = 0;
            this.matchSecondAccumulator = 0;
            this.simulationAccumulator = 0;
            this.aiSyncAccumulator = 0;
            this.aiStateSequence = 0;
            this.lastAiStateSequence = -1;
            this.lastAiAuthoritySlot = null;
            this.hasRemoteAiState = false;
            this.scoreboardRequestSent = false;
            this.scoreboardShown = false;
            this.localSkillSequence = 0;
            this.lastRemoteSkillSequence = {};
            this.pendingSkillSlots.clear();
            this.matchGeneration++;
            this.bossRevision = 0;
            this.pendingBossTransition = false;
            this.matchState.timeRemaining = MATCH_CONFIG.DEFAULT_DURATION_SEC;
            this.matchState.teamScore = 0;
            // 재도전 시작 시 이전 경기의 보스와 탄환·미니언을 모두 초기화한다.
            if (this.boss) {
                this.boss = BossFactory.createBoss('neonDragon', this.canvas.width / 2, 150);
                this.playerBullets = [];
                this.bossBullets = [];
                this.minionBullets = [];
                this.enemyMinions = [];
                this.allyMinions = [];
                this.particles = [];
                this.floatingTexts = [];
            }
        }

        this.slots = Array.from({ length: TOTAL_SLOTS }, (_, i) => {
            const slotId = i + 1;
            const classSelect = document.getElementById(`p${slotId}-class`);
            const serverSlot = serverSlots.find(detail => detail.slotIndex === slotId);
            const classType = (serverSlot && serverSlot.classType) || (classSelect ? classSelect.value : 'defaultPlayer');
            
            const player = PlayerFactory.createPlayer(i, classType);
            
            // 실제 멀티 접속 중인 인간 유저 슬롯(activeSlots에 포함된 슬롯)은 AI 제어를 해제(isHuman = true)
            player.isHuman = serverSlot ? serverSlot.active && !serverSlot.isAiMode : activeSlots.includes(slotId);
            return player;
        });

        const localPlayer = this.slots[mySlot - 1];
        if (localPlayer && this.input && this.input.isAiMode === localPlayer.isHuman) {
            this.input.setAiMode(!localPlayer.isHuman);
        }

        if (this.canvas) {
            this.slots.forEach(slot => slot.resetPosition(1280, 720, TOTAL_SLOTS));
        }
        if (this.ui) {
            this.ui.updateSlotAndStats(this.slots);
        }
    }

    /**
     * 엔티티 초기 위치 및 화면 크기 변경 처리
     */
    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());

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

    }

    /**
     * 💡 [Object & HP Sync]: 원격 기기의 설치형 오브젝트 및 HP 상태 패킷 수신 동기화
     * 소유자(Owner)가 브로드캐스트한 데이터를 기반으로 원격 화면의 오브젝트/체력을 맞춤
     * @param {object} packet 
     */
    handleObjectStateSync(packet) {
        if (!packet || !packet.slotIndex) return;
        const ownerSlotIdx = packet.slotIndex - 1;
        const ownerPlayer = this.slots ? this.slots[ownerSlotIdx] : null;

        // 내가 소유자인 경우 자신의 판정이 우선이므로 무시
        if (ownerPlayer && ownerPlayer.isLocalOwner) return;

        // 1. 방벽(Shield) 동기화 (쉴더 기체)
        if (ownerPlayer && ownerPlayer.classType === 'shielderPlayer') {
            const shieldObj = (packet.objects || []).find(o => o.radius !== undefined && o.arcAngle !== undefined);
            if (shieldObj) {
                ownerPlayer.activeShield = {
                    ...shieldObj
                };
            } else {
                ownerPlayer.activeShield = null;
            }
        }

        // 2. 미니언(AllyMinions) 동기화 (서머너 기체)
        if (ownerPlayer && packet.objects && Array.isArray(packet.objects)) {
            packet.objects.forEach(obj => {
                if (obj.type === 'berserker' || obj.type === 'drone') {
                    // 기존 미니언 매칭
                    const existing = (this.allyMinions || []).find(m => m.owner === ownerPlayer && m.id === obj.id);
                    if (existing) {
                        existing.hp = obj.hp;
                        if (obj.isDead || obj.hp <= 0) {
                            existing.isDead = true;
                        }
                    }
                }
            });
        }

        // 3. 기체 본체 HP 상태 동기화
        if (ownerPlayer && packet.hpState) {
            ownerPlayer.hp = packet.hpState.hp;
            if (packet.hpState.isStunned && !ownerPlayer.isStunned()) {
                ownerPlayer.stunTimer = 3.0;
            }
        }
    }

    /** 스킬마다 동일한 월드 컨테이너를 전달한다. */
    getSkillContext(keys, mousePos) {
        return {
            keys, mousePos,
            boss: this.boss,
            enemyMinions: this.enemyMinions,
            bossBullets: this.bossBullets,
            minionBullets: this.minionBullets,
            enemyBullets: [...this.bossBullets, ...this.minionBullets],
            allyMinions: this.allyMinions,
            allyPlayers: this.slots
        };
    }

    /** 시전 전에 서버에 예약하고, 서버가 지정한 시각까지 중복 요청을 막는다. */
    requestSkillCast(player, source, keys = {}, mousePos = null) {
        const slotIndex = player.slotIndex + 1;
        if (!player.isSkillReady() || this.pendingSkillSlots.has(slotIndex)) return false;
        const sequence = ++this.localSkillSequence;
        const request = {
            source, sequence, x: player.x, y: player.y,
            mouseX: mousePos?.x, mouseY: mousePos?.y, keys
        };
        const net = window.networkManager;
        if (net?.socket?.readyState === 1) {
            const pending = { sequence };
            this.pendingSkillSlots.set(slotIndex, pending);
            net.sendPlayerSkill(slotIndex, request);
            setTimeout(() => {
                if (this.pendingSkillSlots.get(slotIndex) === pending) this.pendingSkillSlots.delete(slotIndex);
            }, 1500);
        } else {
            this.performScheduledSkill({ ...request, slotIndex, classType: player.classType });
        }
        return true;
    }

    /** 로컬 슬롯의 스킬을 서버 예약 경로로 보낸다. */
    useUserSkill() {
        if (!this.sceneManager.isPlaying()) return false;
        const net = window.networkManager;
        const player = this.slots[(net?.mySlotIndex || 1) - 1];
        if (!player?.isHuman || !player.hasActiveSkill || !player.isSkillReady()) return false;

        const keys = Object.fromEntries(['KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight']
            .map(key => [key, !!this.input.keys[key]]));
        const mousePos = { ...this.input.mousePos };
        return this.requestSkillCast(player, 'HUMAN', keys, mousePos);
    }

    /** 서버가 배포한 예약 시각에 맞춰 모든 기기의 시전을 실행한다. */
    applyRemoteSkill(packet) {
        const net = window.networkManager;
        const player = this.slots?.[packet.slotIndex - 1];
        if (!this.sceneManager.isPlaying() || !player?.hasActiveSkill ||
            player.classType !== packet.classType ||
            !Number.isInteger(packet.sequence) ||
            packet.sequence <= (this.lastRemoteSkillSequence[packet.slotIndex] || 0) ||
            !Number.isFinite(packet.x) || !Number.isFinite(packet.y) ||
            !Number.isFinite(packet.executeAt)) return false;

        this.lastRemoteSkillSequence[packet.slotIndex] = packet.sequence;
        const pending = { sequence: packet.sequence };
        this.pendingSkillSlots.set(packet.slotIndex, pending);
        const matchGeneration = this.matchGeneration;
        const delay = net?.getSkillExecutionDelay?.(packet.executeAt, packet.serverSentAt) ?? 0;
        setTimeout(() => {
            if (this.pendingSkillSlots.get(packet.slotIndex) !== pending) return;
            this.pendingSkillSlots.delete(packet.slotIndex);
            if (this.matchGeneration === matchGeneration && this.sceneManager.isPlaying()) {
                this.performScheduledSkill(packet);
            }
        }, delay);
        return true;
    }

    /** 예약된 스킬을 소유 기기까지 포함해 동일한 입력으로 재생한다. */
    performScheduledSkill(packet) {
        const player = this.slots?.[packet.slotIndex - 1];
        if (!player || !this.sceneManager.isPlaying()) return false;
        const net = window.networkManager;
        const mousePos = Number.isFinite(packet.mouseX) && Number.isFinite(packet.mouseY)
            ? { x: packet.mouseX, y: packet.mouseY } : null;
        const context = this.getSkillContext(packet.keys || {}, mousePos);
        context.castX = packet.x;
        context.castY = packet.y;
        context.castId = packet.sequence;
        context.scheduledNetworkCast = net?.socket?.readyState === 1;
        const wasLocalOwner = player.isLocalOwner;
        const previousStunTimer = player.stunTimer;
        player.isLocalOwner = packet.source === 'HUMAN' && packet.slotIndex === (net?.mySlotIndex || 1);
        player.stunTimer = 0;
        player.gauge = player.maxGauge;
        let success;
        try {
            success = player.useSkill(context);
        } finally {
            player.isLocalOwner = wasLocalOwner;
            player.stunTimer = previousStunTimer;
        }
        if (!success) return false;
        this.floatingTexts.push(createFloatingText(packet.x, packet.y - 20, player.skillFloatText, player.themeColor));
        return true;
    }

    /**
     * EMP 특수폭탄 발동 (전 화면 보스 탄막 소거)
     */
    useBomb() {
        this.bossBullets = [];
        createImpactParticles(this.particles, this.canvas.width / 2, this.canvas.height / 2, '#ec4899', 30);
    }

    /**
     * 💡 [신규 - 슬롯 AI 모드 수신 적용 메서드]:
     * 네트워크 신호를 받아 타 PC 화면에서도 해당 슬롯 기체의 AI 모드와 UI 상태를 즉시 일치시킴
     * @param {number} slotIndex 슬롯 번호 (1~4)
     * @param {boolean} isAiMode AI 모드 활성화 여부
     */
    applySlotAiMode(slotIndex, isAiMode) {
        const slotIdx = slotIndex - 1;
        const player = this.slots ? this.slots[slotIdx] : null;

        if (player) {
            player.isHuman = !isAiMode; // isAiMode가 true면 isHuman = false

            // 수신받은 슬롯이 내 슬롯일 경우 InputHandler 내 AI 플래그도 동기화
            const mySlotNum = (window.networkManager && window.networkManager.mySlotIndex) ? window.networkManager.mySlotIndex : 1;
            if (slotIndex === mySlotNum && this.input && typeof this.input.setAiMode === 'function') {
                this.input.setAiMode(isAiMode);
            }

            // 상단 HUD 상태 텍스트 동기화 (내 슬롯 변경 시)
            if (slotIndex === mySlotNum) {
                const statusText = document.getElementById('top-ai-status-text');
                if (statusText) {
                    statusText.innerText = player.isHuman ? 'USER (MANUAL)' : 'AI (AUTO)';
                    statusText.className = player.isHuman ? 'text-cyan-400 font-bold' : 'text-pink-400 font-bold';
                }
            }

            // 우측 슬롯 디버그 패널 렌더링 갱신
            if (this.ui && typeof this.ui.updateSlotAndStats === 'function') {
                this.ui.updateSlotAndStats(this.slots);
            }

            console.log(`🤖 [GameLoop] P${slotIndex} AI 모드 원격 전환 완료: ${isAiMode ? 'AI (AUTO)' : 'USER (MANUAL)'}`);
        }
    }

    /**
     * 매치 종료 및 서버 랭킹 전송
     */
    endMatch() {
        const net = window.networkManager;
        if (net?.socket?.readyState === 1) {
            if (this.isAiAuthority() && !this.scoreboardRequestSent) {
                this.scoreboardRequestSent = true;
                net.requestScoreboard(this.matchState.teamScore);
            }
            return;
        }
        this.enterScoreboard();
    }

    enterScoreboard(result = null) {
        if (this.scoreboardShown) return;
        this.scoreboardShown = true;
        this.sceneManager.setState(GameState.GAMEOVER);

        if (Number.isFinite(result?.score)) this.matchState.teamScore = result.score;
        this.ui.showGameOverModal(this.slots, this.matchState.teamScore, result?.players);
    }

    /**
     * 메인 틱 업데이트
     * @param {number} dt 델타 타임(초)
     */
    update(dt) {
        if (!this.sceneManager.isPlaying()) return;

        this.gameTime += dt;
        this.matchSecondAccumulator += dt;
        while (this.matchSecondAccumulator >= 1) {
            this.matchSecondAccumulator -= 1;
            this.matchState.timeRemaining--;
            this.matchState.teamScore += MATCH_CONFIG.SCORE_PER_TICK;
            if (this.matchState.timeRemaining <= 0) {
                this.matchState.timeRemaining = 0;
                this.ui.updateHeader(0, this.matchState.teamScore);
                this.endMatch();
                return;
            }
        }

        // 💡 [입력 및 네트워크 동기화 프레임 틱 호출]
        this.updateInputs(dt);

        // 보스 기동 및 탄막 발생 (플레이어 정보 전달)
        if (!this.boss.isDead) this.boss.update(this.bossBullets, this.canvas.width, this.slots, dt);

        // 💡 [보스 레이저(dangerAreas) 광역 다중 피격 및 쉴드 연동 정밀 판정 로직]
        if (this.boss && Array.isArray(this.boss.dangerAreas)) {
            this.boss.dangerAreas.forEach(area => {
                if (this.boss.isDead) return;
                if (area.isFiring) {
                    // 차단 상태 초기화 후 판정
                    area.isBlockedByShield = false;

                    const allTargets = [...this.slots, ...this.allyMinions];
                    
                    // 범위 내 모든 캐릭터 독립 순회 타격 (단일 대상 break 차단)
                    for (let i = 0; i < allTargets.length; i++) {
                        const target = allTargets[i];
                        if (!target || target.isDead) continue;

                        const A = target.x - area.x1;
                        const B = target.y - area.y1;
                        const C = area.x2 - area.x1;
                        const D = area.y2 - area.y1;

                        const dot = A * C + B * D;
                        const lenSq = C * C + D * D;
                        let param = -1;
                        if (lenSq !== 0) param = dot / lenSq;

                        let xx, yy;
                        if (param < 0) { xx = area.x1; yy = area.y1; }
                        else if (param > 1) { xx = area.x2; yy = area.y2; }
                        else { xx = area.x1 + param * C; yy = area.y1 + param * D; }

                        const dist = Math.hypot(target.x - xx, target.y - yy);
                        const hitRadius = (area.width / 2) + (target.radius || 10);

                        if (dist <= hitRadius) {
                            // target 본래의 takeDamage 메서드를 활용하여 기절 및 HP 0 다운 상태 전환 보장
                            if (typeof target.takeDamage === 'function') {
                                const hitSuccess = target.takeDamage(18 * dt);
                                if (hitSuccess) {
                                    createImpactParticles(this.particles, target.x, target.y, '#f43f5e', 1);
                                }
                            } else if (target.hp !== undefined) {
                                target.hp = Math.max(0, target.hp - (18 * dt));
                                createImpactParticles(this.particles, target.x, target.y, '#f43f5e', 1);
                                if (target.hp <= 0) {
                                    target.isDead = true;
                                    if (typeof target.onKilled === 'function') target.onKilled();
                                }
                            }
                        }
                    }
                }
            });
        }

        // 플레이어 / AI 슬롯 업데이트
        const allEnemyBullets = [...this.bossBullets, ...this.minionBullets];
        const allEnemies = [this.boss, ...this.enemyMinions].filter(Boolean);

        // 💡 [아군 미니언 관리 배열 초기화 방어 및 전달 준비]
        if (!this.allyMinions) this.allyMinions = [];

        this.slots.forEach(slot => {
            if (slot.isHuman) {
                // updateInputs(dt)에서 패킷 소비 및 위치 보간이 처리되므로
                // 프레임 틱 단위 개별 업데이트만 수행 (불필요한 중복 return 지움)
                if (typeof slot.update === 'function') {
                    slot.update(dt);
                }
            } else if (this.isAiAuthority() || !this.hasRemoteAiState) {
                // 아군 전체 슬롯(this.slots)을 마지막 인자로 전달하여 쉴드 탐색 가능하게 수정
                AIEngine.update(
                    slot,
                    dt,
                    allEnemyBullets,
                    allEnemies,
                    (x, y, text, color) => this.floatingTexts.push(createFloatingText(x, y, text, color)),
                    this.slots
                );

                // AI 스킬 연동: 원본 탄환 배열 및 아군 미니언 컨테이너 전달 (100게이지 3종 동시 소환 지원)
                if (this.isAiAuthority() && slot.hasActiveSkill && slot.gauge >= slot.maxGauge) {
                    this.requestSkillCast(slot, 'AI');
                }
            }

            // 이동 및 델타룬 스치기/버프 업데이트
            if (slot.isHuman || this.isAiAuthority() || !this.hasRemoteAiState) {
                slot.updateMovement(dt, this.canvas.width, this.canvas.height, allEnemyBullets, this.slots);
            } else {
                // 위치는 방장 스냅샷을 따르되 원격 AI 버프와 스킬 이펙트 시간은 진행한다.
                slot.updateModifiers?.(dt);
                slot.updateSkillEffect?.(dt, this.canvas.width, this.canvas.height, allEnemyBullets, this.slots);
            }

            // 💡 [유저 인간 슬롯 스킬 사용 시에도 allyMinions 인자 전달 보완]
            if (slot.isHuman && this.input.keys['KeyE']) { // 혹은 UI 스킬 버튼
                // UI에서 스킬을 시전할 때 allyMinions 전달
            }

            // 💡 [아군 미니언 기동/피격/사격/버프 통합 처리]
            if (Array.isArray(this.allyMinions)) {
                for (let i = this.allyMinions.length - 1; i >= 0; i--) {
                    const minion = this.allyMinions[i];
                    if (!minion || minion.isDead) {
                        this.allyMinions.splice(i, 1);
                        continue;
                    }
                    minion.updateMovement(allEnemies, dt);
                    minion.updateAttack(allEnemies, this.playerBullets, dt, this.slots);

                    // 💡 [적 탄환과 아군 미니언 피격 충돌 검사 - 광폭화 탱킹 및 소환 무적 적용]
                    if (!minion.isDead && Array.isArray(allEnemyBullets)) {
                        // 소환 중(isSpawning)이거나 영구 무적 드론(hp > 9000)만 탄막 통과
                        const isTotallyInvulnerable = minion.isSpawning || minion.hp > 9000;
                        if (!isTotallyInvulnerable) {
                            for (let j = allEnemyBullets.length - 1; j >= 0; j--) {
                                const b = allEnemyBullets[j];
                                if (b && !b.isDead) {
                                    const dist = Math.hypot(b.x - minion.x, b.y - minion.y);
                                    if (dist <= minion.radius + (b.radius || 4)) {
                                        b.isDead = true; // 적 탄환 소멸
                                        minion.takeDamage(b.damage || 1); // 버서커 광폭화 시 50% 반감 데미지 자동 반영
                                        break;
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // 💡 [스킬 게이지 HUD 연동]: 내 컴퓨터 조작 슬롯(mySlotIndex)의 게이지는 AI 모드일 때도 실시간 갱신
            const mySlotIdx = (window.networkManager && window.networkManager.mySlotIndex) 
                ? window.networkManager.mySlotIndex - 1 
                : 0;
            if (slot.slotIndex === mySlotIdx) {
                this.ui.updateSkillButton(slot);
            }

            // 유저 탄환은 소유 기기가 생성한 방향과 좌표를 그대로 중계한다.
            const net = window.networkManager;
            const remoteHuman = slot.isHuman && !slot.isLocalOwner && net?.socket?.readyState === 1;
            const remoteAi = !slot.isHuman && net?.socket?.readyState === 1 && !this.isAiAuthority();
            if (remoteHuman || remoteAi) return;
            slot.updateAttack(dt, () => {
                slot.shoot(this.playerBullets, {
                    mousePos: slot.isLocalOwner ? this.input.mousePos : slot.lastMousePos,
                    boss: this.boss,
                    enemyMinions: this.enemyMinions
                });
                if (slot.isHuman && slot.isLocalOwner && net?.socket?.readyState === 1) {
                    net.sendPlayerShot(slot.slotIndex + 1, this.playerBullets[this.playerBullets.length - 1]);
                } else if (!slot.isHuman && net?.socket?.readyState === 1) {
                    const bullet = this.playerBullets.pop();
                    if (bullet) net.sendAiShot(slot.slotIndex + 1, bullet);
                }
                if (slot.isLocalOwner && (slot.isHuman || net?.socket?.readyState !== 1)) window.gameAudio?.play('shoot');
            });
        });

        // 1. 미니언 기동 및 사격 업데이트
        this.enemyMinions.forEach(m => {
            m.updateMovement(this.slots, dt);
            m.updateAttack(this.slots, this.minionBullets, dt);
        });
        this.allyMinions.forEach(m => {
            m.updateMovement([this.boss], dt);
            m.updateAttack([this.boss], this.minionBullets, dt);
        });

        // 2. isAlly 속성 기반 통합 탄환 충돌 파이프라인
        const bulletGroups = [
            { container: this.playerBullets, defaultAlly: true },
            { container: this.bossBullets, defaultAlly: false },
            { container: this.minionBullets, defaultAlly: false }
        ];

        const allyTargets = [...this.slots, ...this.allyMinions];
        const enemyTargets = [this.boss, ...this.enemyMinions].filter(Boolean);

        for (const group of bulletGroups) {
            const bullets = group.container;

            for (let i = bullets.length - 1; i >= 0; i--) {
                const b = bullets[i];
                if (typeof b.update === 'function') b.update(this.slots, dt);

                const isAllyBullet = b.isAlly !== undefined ? b.isAlly : group.defaultAlly;

                if (!isAllyBullet) {
                    // [적군 탄환] -> 아군 피격 대상(플레이어 / 아군 미니언)
                    for (const target of allyTargets) {
                        if (!target || target.isDead) continue;
                        const dist = Math.hypot(b.x - target.x, b.y - target.y);

                        if (b.isHoming && !b.isWarning && !b.isDetonated) {
                            if (dist < (b.proximityRadius || 22) + (target.radius || 8)) {
                                if (typeof b.triggerExplosion === 'function') b.triggerExplosion();
                                break;
                            }
                        }

                        const isHarmful = !b.isHoming || b.isDetonated;
                        const isTargetStunned = typeof target.isStunned === 'function' ? target.isStunned() : false;

                        if (isHarmful && !isTargetStunned && (target.invulnerableTimer === undefined || target.invulnerableTimer <= 0)) {
                            const checkRadius = b.isDetonated ? (b.explosionRadius || 32) : (b.radius || 4);

                            if (dist < checkRadius + target.radius) {
                                const hitSuccess = typeof target.takeDamage === 'function' ? target.takeDamage(b.damage || 1) : false;
                                if (hitSuccess) {
                                    if (this.matchState) {
                                        this.matchState.teamScore = Math.max(0, this.matchState.teamScore - MATCH_CONFIG.SCORE_PENALTY_HIT);
                                    }
                                    createImpactParticles(this.particles, target.x, target.y, target.color || '#f43f5e', 10);

                                    if (!b.isHoming && !b.isPenetrating) {
                                        b.isDead = true;
                                        break;
                                    }
                                }
                            }
                        }
                    }
                } else {
                    // [아군 탄환] -> 적군 피격 대상(보스 / 적군 미니언)
                    for (const target of enemyTargets) {
                        if (!target || target.isDead) continue;
                        const dist = Math.hypot(b.x - target.x, b.y - target.y);

                        if (dist < (b.radius || 4) + target.radius) {
                            const damage = b.damage || 10;
                            const isKilled = typeof target.takeDamage === 'function' ? target.takeDamage(damage) : false;

                            if (b.slotIndex !== undefined && this.slots[b.slotIndex]) {
                                this.slots[b.slotIndex].damageDealt += damage;
                                if (isKilled) this.slots[b.slotIndex].kills++;
                            }

                            if (this.matchState) {
                                this.matchState.teamScore += damage * MATCH_CONFIG.DAMAGE_SCORE_RATIO;
                                if (isKilled && target !== this.boss) this.matchState.teamScore += MATCH_CONFIG.SCORE_ON_BOSS_KILL;
                            }

                            createImpactParticles(this.particles, b.x, b.y, b.color || '#06b6d4', 4);

                            if (!b.isPenetrating) {
                                b.isDead = true;
                                break;
                            }
                        }
                    }
                }

                // 사망 및 화면 이탈 소멸 처리
                const isOut = typeof b.isOutOfBounds === 'function' && b.isOutOfBounds(this.canvas.width, this.canvas.height);
                if (b.isDead || isOut) {
                    bullets.splice(i, 1);
                }
            }
        }

        this.handleBossDeath();

        // 사망한 미니언 객체 청소
        this.enemyMinions = this.enemyMinions.filter(m => !m.isDead);
        this.allyMinions = this.allyMinions.filter(m => !m.isDead);

        // 3. 플로팅 텍스트 업데이트
        for (let i = this.floatingTexts.length - 1; i >= 0; i--) {
            const ft = this.floatingTexts[i];
            ft.y += ft.vy * dt * 60;
            ft.life -= dt * 1.5;
            if (ft.life <= 0) this.floatingTexts.splice(i, 1);
        }

        // 4. 파티클 업데이트
        for (let i = this.particles.length - 1; i >= 0; i--) {
            this.particles[i].update(dt);
            if (this.particles[i].life <= 0) this.particles.splice(i, 1);
        }

        // 실시간 HUD 및 통계 업데이트
        this.sendAiStateSync(dt);
        this.ui.updateHeader(this.matchState.timeRemaining, this.matchState.teamScore);
    }

    /**
     * 메인 프레임 렌더링
     */
    render() {
        // 배경 클리어
        this.ctx.fillStyle = '#030712';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        // 네온 그리드 라인 렌더링
        this.ctx.strokeStyle = 'rgba(6, 182, 212, 0.04)';
        this.ctx.lineWidth = 1;
        for (let x = 0; x < this.canvas.width; x += CANVAS_GRID_SIZE) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        for (let y = 0; y < this.canvas.height; y += CANVAS_GRID_SIZE) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }

        // 엔티티 렌더링 (버퍼의 아군 추적 이펙트를 위해 slots 인자 전달)
        this.boss.draw(this.ctx, this.canvas.width);
        this.slots.forEach(s => s.draw(this.ctx, this.slots));
        this.enemyMinions.forEach(m => m.draw(this.ctx));
        this.allyMinions.forEach(m => m.draw(this.ctx));
        this.playerBullets.forEach(pb => pb.draw(this.ctx));
        this.bossBullets.forEach(bb => bb.draw(this.ctx));
        this.minionBullets.forEach(mb => mb.draw(this.ctx));
        this.particles.forEach(pt => pt.draw(this.ctx));

        // AI 디버그 오버레이 시각화
        if (this.showAIDebug) {
            this.renderAIDebug();
        }

        // 플로팅 텍스트 렌더링
        this.floatingTexts.forEach(ft => {
            this.ctx.save();
            this.ctx.globalAlpha = Math.max(0, ft.life);
            this.ctx.font = '900 11px Orbitron';
            this.ctx.fillStyle = ft.color;
            this.ctx.textAlign = 'center';
            this.ctx.fillText(ft.text, ft.x, ft.y);
            this.ctx.restore();
        });
    }

    /**
     * AI 의사결정 상태 및 궤적 디버그 시각화
     */
    renderAIDebug() {
        this.slots.forEach(s => {
            if (s.isHuman) return;

            // 목표 지점 연결 점선
            this.ctx.strokeStyle = s.color + '88';
            this.ctx.lineWidth = 1;
            this.ctx.setLineDash([3, 3]);
            this.ctx.beginPath();
            this.ctx.moveTo(s.x, s.y);
            this.ctx.lineTo(s.targetX, s.targetY);
            this.ctx.stroke();
            this.ctx.setLineDash([]);

            // 목표 지점 포인트
            this.ctx.beginPath();
            this.ctx.arc(s.targetX, s.targetY, 4, 0, Math.PI * 2);
            this.ctx.fillStyle = s.color;
            this.ctx.fill();

            // FSM 상태 & 액션 락 타이머 텍스트
            this.ctx.font = '8px Orbitron';
            this.ctx.fillStyle = '#67e8f9';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(`${s.fsmState} (${s.actionLockTimer.toFixed(1)}s)`, s.x, s.y + s.radius + 12);

            // 하단 피로도(Fatigue) 게이지 바
            const barW = 28;
            const barH = 3;
            const barX = s.x - barW / 2;
            const barY = s.y + s.radius + 16;

            this.ctx.fillStyle = 'rgba(0,0,0,0.8)';
            this.ctx.fillRect(barX, barY, barW, barH);
            this.ctx.fillStyle = s.dodgeFatigue > 0.6 ? '#f43f5e' : '#f59e0b';
            this.ctx.fillRect(barX, barY, barW * s.dodgeFatigue, barH);
        });
    }

    /**
     * 메인 루프 실행 진입점
     * @param {number} now 
     */
    run(now) {
        const dt = Math.min(0.1, (now - this.lastTimestamp) / 1000);
        this.lastTimestamp = now;

        this.simulationAccumulator += dt;
        const fixedDt = 1 / 60;
        while (this.simulationAccumulator + 1e-9 >= fixedDt) {
            this.update(fixedDt);
            this.simulationAccumulator -= fixedDt;
        }
        this.render();

        requestAnimationFrame((time) => this.run(time));
    }
}

export default GameLoop;
