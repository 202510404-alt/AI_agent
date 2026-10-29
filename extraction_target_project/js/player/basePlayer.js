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
import { SLOT_COLORS } from '../config/constants.js';
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

        // 💡 [멀티플레이 권한 시스템]: 내가 직접 키보드/마우스로 조종하는 기체인지 여부 (IsLocalOwner)
        this.isLocalOwner = false;

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
                this.gauge = Math.min(this.maxGauge, this.gauge + 1);
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
            // deltaTime 연산을 위해 속도 벡터로 저장
            const normX = dx / factor;
            const normY = dy / factor;
            this.targetX = this.x + normX * this.moveSpeed * 0.1;
            this.targetY = this.y + normY * this.moveSpeed * 0.1;
        } else {
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

        // 1. 송신지 실제 좌표가 포함되어 있는 경우 Dead Reckoning 목적지 설정
        if (typeof inputAction.posX === 'number' && typeof inputAction.posY === 'number') {
            const pingSec = Math.max(0.01, (inputAction.estimatedPing || 50) / 1000);
            
            // 상대방의 현재 속도 추정
            const speed = this.moveSpeed;
            const vx = len > 0 ? (moveX / len) * speed : 0;
            const vy = len > 0 ? (moveY / len) * speed : 0;

            this.netVelocityX = vx;
            this.netVelocityY = vy;

            // Ping 지연 시간만큼 미래의 예측 위치 계산 (Dead Reckoning)
            this.netTargetX = inputAction.posX + vx * pingSec;
            this.netTargetY = inputAction.posY + vy * pingSec;

            // 💡 [Hard Snap / Teleport Threshold]: 150px 이상 오차 시 강제 스냅
            const distFromCurrent = Math.hypot(this.x - inputAction.posX, this.y - inputAction.posY);
            if (distFromCurrent > this.HARD_SNAP_THRESHOLD) {
                this.x = inputAction.posX;
                this.y = inputAction.posY;
                this.targetX = inputAction.posX;
                this.targetY = inputAction.posY;
            } else {
                this.targetX = this.netTargetX;
                this.targetY = this.netTargetY;
            }
        } else {
            // 위치 좌표가 없을 경우 기존 방향 벡터 누적
            if (len > 0) {
                const factor = len > 1 ? len : 1;
                this.targetX = this.x + (moveX / factor) * this.moveSpeed * 0.1;
                this.targetY = this.y + (moveY / factor) * this.moveSpeed * 0.1;
            } else {
                this.targetX = this.x;
                this.targetY = this.y;
            }
        }

        // 3. 1회성 스킬 트리거 실행 (useSkill)
        if (inputAction.useSkill && skillParams) {
            this.useSkill(skillParams);
            inputAction.useSkill = false; // 1회성 소모
        }
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

        if (dist > this.HARD_SNAP_THRESHOLD) {
            // 임계치 초과 시 즉시 Hard Snap
            this.x = this.targetX;
            this.y = this.targetY;
        } else if (dist > 1) {
            // 원격 기체(RemoteProxy)는 거리에 따라 미세 가속/감속 보정 (도착 시간 맞춤)
            let currentSpeed = this.moveSpeed;
            if (!this.isLocalOwner && this.isHuman) {
                // 오차가 크면 약간 가속(최대 1.5배), 거의 도착하면 감속
                const speedMultiplier = Math.min(1.8, Math.max(0.6, dist / 30));
                currentSpeed *= speedMultiplier;
            }

            const step = Math.min(dist, currentSpeed * dt);
            this.x += (dx / dist) * step;
            this.y += (dy / dist) * step;
        } else {
            this.x = this.targetX;
            this.y = this.targetY;
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
                targetAngle = Math.atan2(closestEnemy.y - this.y, closestEnemy.x - this.x);
            }
        }

        bulletContainer.push(new PlayerBullet(this.x, this.y, targetAngle, this.color, this));
    }

    updateAttack(onShoot) {
        if (this.isStunned()) return;

        const currentAttackSpeed = this.attackSpeed * (1 + this.getModifierValue('attackSpeed') / 100);
        this.attackCooldown += currentAttackSpeed;
        if (this.attackCooldown >= 60) {
            this.attackCooldown = 0;
            if (typeof onShoot === 'function') {
                onShoot();
            }
        }
    }

    draw(ctx, allyPlayers = []) {
        ctx.save();

        if (this.isStunned()) {
            ctx.globalAlpha = 0.4 + 0.3 * Math.sin(Date.now() * 0.01);
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

        ctx.restore();
    }
}
