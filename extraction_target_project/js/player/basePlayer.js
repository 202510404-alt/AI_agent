/**
 * js/player/basePlayer.js
 * 모든 플레이어/봇 슬롯의 기반이 되는 BasePlayer 추상 클래스
 * 
 * [동작 명세 - 4단계 신호 동기화 & 네트워크 예외 처리 적용]
 * 1. IsLocalOwner (로컬 직접 제어) vs RemoteProxy (원격 복제본) 분리.
 * 2. Dead Reckoning: 도착 시간 맞춤 미세 속도 보간 (Ping 기반 속도 가속/감속).
 * 3. DeltaTime Base: 주사율 차이(60Hz, 144Hz 등)와 무관한 일관된 이동 연산.
 * 4. Hard Snap Threshold: 핑 튐으로 예측 위치와 실제 수신 위치 차이가 150px 초과 시 즉시 강제 텔레포트.
 */
import { SLOT_COLORS, AI_CONFIG } from '../config/constants.js';
import { PlayerBullet } from './playerBullet.js';
import { rngPlayerAi } from '../utils/seededRNG.js';

export default class BasePlayer {
    /**
     * @param {number} slotIndex 슬롯 인덱스 (0 ~ TOTAL_SLOTS - 1)
     * @param {string} classType 플레이어 직업 타입 ('bufferPlayer', 'defaultPlayer')
     */
    constructor(slotIndex, classType = 'defaultPlayer') {
        this.slotIndex = slotIndex;
        this.id = slotIndex + 1;
        this.color = SLOT_COLORS[slotIndex % SLOT_COLORS.length];
        this.isHuman = (slotIndex === 0);
        this.classType = classType;

        // 💡 [멀티플레이 권한 시스템]: 0번 슬롯(P1) 또는 단일 플레이 시 기본적으로 isLocalOwner = true 보장
        this.isLocalOwner = (slotIndex === 0);

        // 💡 [Dead Reckoning & 원격 상태 수신 변수]
        this.remoteInputPacket = null;
        this.lastReceivedSeq = 0;
        this.netTargetX = 0;
        this.netTargetY = 0;
        this.netVelocityX = 0;
        this.netVelocityY = 0;
        this.netEstimatedPing = 50; // ms

        // Hard Snap 임계값 (예측 오차가 이 값을 초과하면 즉시 강제 이동)
        this.HARD_SNAP_THRESHOLD = 150;

        // --- 공통 메타 속성 (하위 캐릭터 파일에서 오버라이드) ---
        this.className = '기본 기체';
        this.themeColor = '#06b6d4';
        this.hasActiveSkill = false;
        this.skillIconClass = 'fa-solid fa-bolt';
        this.skillName = 'SKILL';
        this.skillFloatText = 'SKILL ACTIVATED!';

        this.radius = 8;
        this.moveSpeed = 300; // px/sec 기준 (기본)
        this.speed = 5.2;

        // 체력 및 기절 시스템
        this.maxHp = 5;
        this.hp = 5;
        this.stunTimer = 0.0;

        // 위치 및 목표 좌표
        this.x = 0;
        this.y = 0;
        this.targetX = 0;
        this.targetY = 0;

        // 통계 및 상태값
        this.damageDealt = 0;
        this.kills = 0;
        this.mistakesCount = 0;
        this.attackCooldown = 0;
        this.attackSpeed = 8;
        this.invulnerableTimer = 0.0;

        // 델타룬 Graze 게이지
        this.gauge = 0;             
        this.maxGauge = 100;
        this.grazeRadius = 45;   
        this.grazeCheckTimer = 0.0; 
        this.grazeEffectTimer = 0;  

        // 동적 스탯 수정자 파이프라인
        this.modifiers = [];     

        // AI FSM 필드
        this.fsmState = 'IDLE';
        this.actionLockTimer = 0.0;
        this.dodgeFatigue = 0.0;
        this.lastMistakeType = 'NONE';
    }

    /**
     * 동적 스탯 수정자(Modifier) 추가
     */
    addModifier(mod) {
        if (!mod || !mod.key) return;
        this.removeModifier(mod.key);
        this.modifiers.push({
            key: mod.key,
            type: mod.type || 'buff',
            stat: mod.stat || 'all',
            value: mod.value || 0,
            duration: mod.duration || 1.0,
            elapsed: 0
        });
    }

    removeModifier(key) {
        this.modifiers = this.modifiers.filter(m => m.key !== key);
    }

    getModifierValue(stat) {
        let total = 0;
        for (const mod of this.modifiers) {
            if (mod.stat === stat || mod.stat === 'all') {
                total += mod.value;
            }
        }
        return total;
    }

    updateModifiers(dt) {
        for (let i = this.modifiers.length - 1; i >= 0; i--) {
            const mod = this.modifiers[i];
            mod.elapsed += dt;
            if (mod.elapsed >= mod.duration) {
                this.modifiers.splice(i, 1);
            }
        }
    }

    /**
     * 델타룬 Graze 판정
     */
    updateGraze(enemyBullets, dt) {
        if (!enemyBullets || enemyBullets.length === 0) return;

        if (this.grazeEffectTimer > 0) {
            this.grazeEffectTimer = Math.max(0, this.grazeEffectTimer - dt);
        }

        for (const b of enemyBullets) {
            if (!b || b.isDead) continue;

            if (!b.grazedSlots) {
                b.grazedSlots = [];
            }

            if (b.grazedSlots.includes(this.slotIndex)) continue;

            const dist = Math.hypot(b.x - this.x, b.y - this.y);

            if (dist > this.radius && dist <= this.grazeRadius) {
                b.grazedSlots.push(this.slotIndex);
                this.gauge = Math.min(this.maxGauge, this.gauge + 1 + this.getModifierValue('gaugeTickRate') / 100);
                this.grazeEffectTimer = 0.2;
            }
        }
    }

    /**
     * 클래스별 개별 maxGauge 기준 100% 충전 여부 판단
     */
    isSkillReady() {
        const isStun = typeof this.isStunned === 'function' ? this.isStunned() : false;
        const targetMax = this.maxGauge || 100;
        const currentGauge = this.gauge || 0;

        if (isStun) return false;
        if (currentGauge < targetMax) return false;

        return true;
    }

    /**
     * 기본 스킬 시전 검사 및 게이지 초기화
     */
    useSkill(params = {}) {
        if (!this.isSkillReady()) return false;
        this.gauge = 0;
        if (this.isLocalOwner) window.gameAudio?.play('skill');
        return true;
    }

    /**
     * 화면 크기에 맞춰 슬롯 위치 초기화
     */
    resetPosition(canvasWidth, canvasHeight, totalSlots) {
        const spacing = canvasWidth / (totalSlots + 1);
        this.x = spacing * (this.slotIndex + 1);
        this.y = canvasHeight - 180;
        this.targetX = this.x;
        this.targetY = this.y;
        this.netTargetX = this.x;
        this.netTargetY = this.y;
    }

    /**
     * 기절 상태 여부 확인
     */
    isStunned() {
        return this.stunTimer > 0;
    }

    /**
     * 피격 대미지 처리 (무적 시간 판정 및 기절 트리거)
     */
    takeDamage(amount = 1) {
        if (this.invulnerableTimer > 0 || this.isStunned()) {
            return false;
        }

        this.hp = Math.max(0, this.hp - amount);
        this.invulnerableTimer = 1.0;
        if (this.isLocalOwner) window.gameAudio?.play('hit');

        if (this.hp <= 0) {
            this.stunTimer = 3.0;
            this.hp = this.maxHp;
        }

        return true;
    }

    /**
     * [IsLocalOwner - 로컬 기체 조작]
     * Client Prediction: 키보드/조이스틱 입력으로 즉시 이동 목표점 계산
     */
    handleHumanInput(keys, joystick, skillParams = null) {
        if (this.isStunned()) return;

        const isSpaceOrRightClick = keys['Space'] || keys['KeySpace'] || keys['RightClick'];
        if (isSpaceOrRightClick && skillParams) {
            keys['Space'] = false;
            keys['KeySpace'] = false;
            keys['RightClick'] = false;
            this.useSkill(skillParams);
        }

        let dx = 0;
        let dy = 0;

        if (keys['KeyW'] || keys['ArrowUp']) dy -= 1;
        if (keys['KeyS'] || keys['ArrowDown']) dy += 1;
        if (keys['KeyA'] || keys['ArrowLeft']) dx -= 1;
        if (keys['KeyD'] || keys['ArrowRight']) dx += 1;

        if (joystick && joystick.active) {
            dx = joystick.moveX;
            dy = joystick.moveY;
        }

        const len = Math.hypot(dx, dy);
        if (len > 0) {
            const factor = len > 1 ? len : 1;
            const normX = dx / factor;
            const normY = dy / factor;
            this.targetX = this.x + normX * this.moveSpeed * 0.1;
            this.targetY = this.y + normY * this.moveSpeed * 0.1;
        } else {
            // 키를 뗐을 때 현재 위치를 목표 지점으로 고정하여 얼어붙음 방지
            this.targetX = this.x;
            this.targetY = this.y;
        }
    }

    /**
     * [RemoteProxy - 원격 기체 패킷 적용 & Dead Reckoning 설정]
     * @param {object} inputAction 릴레이 수신된 원격 패킷
     * @param {object} skillParams
     */
    handleHumanInputPacket(inputAction, skillParams = null) {
        if (this.isStunned() || !inputAction) return;

        if (typeof inputAction.mouseX === 'number' && typeof inputAction.mouseY === 'number') {
            this.lastMousePos = { x: inputAction.mouseX, y: inputAction.mouseY };
        }

        const moveX = inputAction.moveX !== undefined ? inputAction.moveX : inputAction.dx || 0;
        const moveY = inputAction.moveY !== undefined ? inputAction.moveY : inputAction.dy || 0;
        const len = Math.hypot(moveX, moveY);

        // 로컬 기체는 현재 위치가 담긴 전송 패킷보다 직접 입력한 방향을 우선한다.
        if (this.isLocalOwner) {
            if (len > 0) {
                const factor = len > 1 ? len : 1;
                this.targetX = this.x + (moveX / factor) * this.moveSpeed * 0.1;
                this.targetY = this.y + (moveY / factor) * this.moveSpeed * 0.1;
            } else {
                this.targetX = this.x;
                this.targetY = this.y;
            }
        } else if (typeof inputAction.posX === 'number' && typeof inputAction.posY === 'number') {
            const distFromCurrent = Math.hypot(this.x - inputAction.posX, this.y - inputAction.posY);

            if (distFromCurrent > 120) {
                // 오차가 심할 때만 강제위치 고정
                this.x = inputAction.posX;
                this.y = inputAction.posY;
                this.targetX = inputAction.posX;
                this.targetY = inputAction.posY;
            } else {
                // 예측식(Dead Reckoning) 전면 제거 -> 실시간 보간용 목표 좌표로 직결
                this.targetX = inputAction.posX;
                this.targetY = inputAction.posY;
            }
        } else {
            // 위치 좌표 누락 시 수신받은 방향 벡터 기반 연속 관성 이동
            if (len > 0) {
                const normX = moveX / (len > 1 ? len : 1);
                const normY = moveY / (len > 1 ? len : 1);
                this.targetX = this.x + normX * this.moveSpeed * 0.05;
                this.targetY = this.y + normY * this.moveSpeed * 0.05;
            } else {
                this.targetX = this.x;
                this.targetY = this.y;
            }
        }

        // 스킬은 성공한 시전 이벤트를 별도로 수신하여 재생한다.
    }

    /**
     * 프레임 업데이트 공통 처리 (DeltaTime Base 보간)
     */
    updateMovement(dt, canvasWidth, canvasHeight, enemyBullets = [], allyPlayers = []) {
        if (this.invulnerableTimer > 0) {
            this.invulnerableTimer = Math.max(0, this.invulnerableTimer - dt);
        }

        // 동적 스탯 수정자 업데이트
        this.updateModifiers(dt);

        // 델타룬 스치기 체크
        this.updateGraze(enemyBullets, dt);

        if (this.stunTimer > 0) {
            this.stunTimer = Math.max(0, this.stunTimer - dt);
            this.targetX = this.x;
            this.targetY = this.y;
            return;
        }

        // 💡 [DeltaTime Base & Dead Reckoning 미세 속도 보간]
        const dx = this.targetX - this.x;
        const dy = this.targetY - this.y;
        const dist = Math.hypot(dx, dy);

        // 💡 [이동 연산 및 권한 판정 완치]
        if (this.isLocalOwner) {
            // [로컬 기체]: 내 키보드/조이스틱 입력으로 부드럽고 정확하게 실시간 이동
            if (dist > 1) {
                const step = Math.min(dist, this.moveSpeed * dt);
                this.x += (dx / dist) * step;
                this.y += (dy / dist) * step;
            } else {
                this.x = this.targetX;
                this.y = this.targetY;
            }
        } else {
            // [원격 기체]: 네트워크 수신 좌표 부드러운 Lerp 추적 (상대방 위치 튀김 방지)
            if (dist > 150) {
                this.x = this.targetX;
                this.y = this.targetY;
            } else if (dist > 0.5) {
                const blend = 1 - Math.pow(0.75, dt * 60);
                this.x += dx * blend;
                this.y += dy * blend;
            }
        }
        // 맵 경계 제한
        this.x = Math.max(this.radius, Math.min(canvasWidth - this.radius, this.x));
        this.y = Math.max(120, Math.min(canvasHeight - this.radius, this.y));
    }

    /**
     * 탄환 생성 및 사격 처리
     */
    shoot(bulletContainer, targetInfo) {
        if (this.isStunned()) return;

        let targetAngle = -Math.PI / 2;

        if (this.isHuman) {
            const mousePos = (targetInfo && targetInfo.mousePos) ? targetInfo.mousePos : { x: this.x, y: this.y - 100 };
            targetAngle = Math.atan2(mousePos.y - this.y, mousePos.x - this.x);
        } else {
            const boss = targetInfo ? targetInfo.boss : null;
            const enemyMinions = targetInfo ? (targetInfo.enemyMinions || []) : [];
            const allEnemies = [boss, ...enemyMinions].filter(e => e && !e.isDead);

            let closestEnemy = null;
            let minDist = Infinity;

            for (const enemy of allEnemies) {
                const dist = Math.hypot(enemy.x - this.x, enemy.y - this.y);
                if (dist < minDist) {
                    minDist = dist;
                    closestEnemy = enemy;
                }
            }

            if (closestEnemy) {
                const baseAngle = Math.atan2(closestEnemy.y - this.y, closestEnemy.x - this.x);

                // 💡 [constants.js 의 AI_CONFIG 변수 실시간 동기화]
                const minDeg = AI_CONFIG?.ANGLE_OFFSET_MIN_DEG ?? 1;
                const maxDeg = AI_CONFIG?.ANGLE_OFFSET_MAX_DEG ?? 1;

                // 1. constants.js 의 설정 범위 기반 기본 오차각 산출
                const baseDegError = rngPlayerAi.angleOffset(this.slotIndex, minDeg, maxDeg);

                // 2. 회피 누적 피로도(dodgeFatigue: 0.0 ~ 1.0)에 비례하여 오차각 증폭
                const fatigue = this.dodgeFatigue || 0;
                const fatigueMultiplier = 1.0 + (fatigue * 1.5);

                const finalDegError = baseDegError * fatigueMultiplier;
                const radError = (finalDegError * Math.PI) / 180;

                targetAngle = baseAngle + radError;
            }
        }

        const bullet = new PlayerBullet(this.x, this.y, targetAngle, this.slotIndex, this.color);
        bullet.damage = Math.round(bullet.damage * (1 + this.getModifierValue('damage') / 100));
        bulletContainer.push(bullet);
    }

    updateAttack(dt, onShoot) {
        if (this.isStunned()) return;

        const currentAttackSpeed = this.attackSpeed * (1 + this.getModifierValue('attackSpeed') / 100);
        if (currentAttackSpeed <= 0) return;
        const interval = Math.max(1, Math.ceil(60 / currentAttackSpeed)) / 60;
        this.attackCooldown += dt;
        if (this.attackCooldown + 1e-9 >= interval) {
            this.attackCooldown = Math.max(0, this.attackCooldown - interval);
            if (typeof onShoot === 'function') {
                onShoot();
            }
        }
    }

    draw(ctx, allyPlayers = []) {
        ctx.save();

        if (this.isStunned()) {
            ctx.globalAlpha = 0.4 + 0.3 * Math.sin((window.gameLoopInstance?.gameTime ?? 0) * 10);
        }

        // Graze 연출
        if (this.grazeEffectTimer > 0) {
            ctx.save();
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.grazeRadius, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(255, 255, 255, ${this.grazeEffectTimer * 4})`;
            ctx.lineWidth = 1.5;
            ctx.setLineDash([4, 4]);
            ctx.stroke();
            ctx.restore();
        }

        // 본체 렌더링
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#ffffff';
        ctx.stroke();

        // 닉네임 / 소유자 표시
        ctx.font = '10px sans-serif';
        ctx.fillStyle = this.isLocalOwner ? '#22d3ee' : '#cbd5e1';
        ctx.textAlign = 'center';
        const label = this.isLocalOwner ? `[YOU] P${this.id}` : `P${this.id}`;
        ctx.fillText(label, this.x, this.y - this.radius - 6);

        // Keep every player's HP visible above the name, including AI slots.
        const barWidth = 44;
        const barHeight = 5;
        const barX = this.x - barWidth / 2;
        const barY = this.y - this.radius - 29;
        const hpRatio = this.maxHp > 0 ? Math.max(0, Math.min(1, this.hp / this.maxHp)) : 0;
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(barX, barY, barWidth, barHeight);
        ctx.fillStyle = hpRatio > 0.5 ? '#22c55e' : hpRatio > 0.25 ? '#f59e0b' : '#ef4444';
        ctx.fillRect(barX, barY, barWidth * hpRatio, barHeight);
        ctx.strokeStyle = '#e2e8f0';
        ctx.lineWidth = 1;
        ctx.strokeRect(barX, barY, barWidth, barHeight);

        ctx.restore();
    }
}
