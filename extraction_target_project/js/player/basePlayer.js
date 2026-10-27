/**
 * js/player/basePlayer.js
 * 모든 플레이어/봇 슬롯의 기반이 되는 BasePlayer 추상 클래스
 * 입력 처리(Human Input), 사격(Shoot) 및 HP/기절/무적 시스템 통합 완료
 */
import { SLOT_COLORS } from '../config/constants.js';
import { PlayerBullet } from './playerBullet.js';

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

        // --- 공통 메타 속성 (하위 캐릭터 파일에서 오버라이드) ---
        this.className = '기본 기체';
        this.themeColor = '#06b6d4';
        this.hasActiveSkill = false;
        this.skillIconClass = 'fa-solid fa-bolt';
        this.skillName = 'SKILL';
        this.skillFloatText = 'SKILL ACTIVATED!';

        this.radius = 8;
        this.moveSpeed = 300;
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

        // --- 동적 스탯 수정자 (Stat Modifiers & Status Effects) 파이프라인 ---
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
    addModifier(modifier) {
        if (!modifier || !modifier.id) return;
        // 동일 ID가 이미 존재하면 지속시간만 리셋 또는 교체
        const existingIdx = this.modifiers.findIndex(m => m.id === modifier.id);
        if (existingIdx >= 0) {
            this.modifiers[existingIdx] = { ...this.modifiers[existingIdx], ...modifier };
        } else {
            this.modifiers.push({ ...modifier });
        }
    }

    /**
     * ID 기반 수정자 제거
     */
    removeModifier(id) {
        this.modifiers = this.modifiers.filter(m => m.id !== id);
    }

    /**
     * 지정된 스탯의 최종 수정 수치 파이프라인 산출 (ADD -> MULTIPLY -> OVERRIDE)
     * @param {string} statName 'damage', 'moveSpeed', 'defense', 'damageTaken'
     * @param {number} baseValue 기본 원본값
     * @returns {number}
     */
    getModifiedStat(statName, baseValue) {
        let finalValue = baseValue;

        // 1. 합연산 (ADD)
        for (const m of this.modifiers) {
            if (m.targetStat === statName && m.type === 'ADD') {
                finalValue += m.value;
            }
        }

        // 2. 곱연산 (MULTIPLY)
        for (const m of this.modifiers) {
            if (m.targetStat === statName && m.type === 'MULTIPLY') {
                finalValue *= m.value;
            }
        }

        // 3. 고정값 덮어쓰기 (OVERRIDE)
        for (const m of this.modifiers) {
            if (m.targetStat === statName && m.type === 'OVERRIDE') {
                finalValue = m.value;
            }
        }

        // 4. 💡 깃발 버퍼/특수 상태이상 등 틱 회복 속도(gaugeTickRate) 곱연산 수치 추가 보정
        if (statName === 'gaugeTickRate') {
            let tickMult = 1.0;
            for (const m of this.modifiers) {
                if (m.targetStat === 'gaugeTickRate' && m.type === 'MULTIPLY') {
                    tickMult *= m.value;
                }
            }
            finalValue *= tickMult;
        }

        return finalValue;
    }

    /**
     * 프레임별 지속시간 차감 및 도트 상태이상(onTick) 업데이트
     */
    updateModifiers(dt) {
        for (let i = this.modifiers.length - 1; i >= 0; i--) {
            const m = this.modifiers[i];

            // 도트 대미지/치유 등 주기적 효과 실행
            if (typeof m.onTick === 'function') {
                m.onTick(this, dt);
            }

            // 지속시간 차감
            if (typeof m.duration === 'number') {
                m.duration -= dt;
                if (m.duration <= 0) {
                    this.modifiers.splice(i, 1);
                }
            }
        }
    }

    /**
     * 탄막 스치기 검사 (탄환 1개당 슬롯별 최초 1회만 확정 게이지 수급)
     */
    updateGraze(enemyBullets = [], dt = 0.016) {
        if (this.isStunned()) return;

        if (this.grazeEffectTimer > 0) {
            this.grazeEffectTimer = Math.max(0, this.grazeEffectTimer - dt);
        }

        for (const b of enemyBullets) {
            if (!b || b.isDead) continue;

            // 탄환에 이미 스친 슬롯 목록(grazedSlots) 배열이 없으면 생성
            if (!b.grazedSlots) {
                b.grazedSlots = [];
            }

            // 이미 이 슬롯(P1~P4)이 스친 탄환이라면 패스
            if (b.grazedSlots.includes(this.slotIndex)) continue;

            const dist = Math.hypot(b.x - this.x, b.y - this.y);

            // 판정 범위 안으로 들어온 '새로운' 탄환 발견!
            if (dist > this.radius && dist <= this.grazeRadius) {
                b.grazedSlots.push(this.slotIndex); // 해당 탄환 목록에 이 슬롯 등록 (재수급 방지)
                this.gauge = Math.min(this.maxGauge, this.gauge + 1); // 게이지 1 증가
                this.grazeEffectTimer = 0.2; // 스치기 링 피드백 연출
            }
        }
    }

    /**
     * 클래스별 개별 maxGauge 기준 100% 충전 여부 판단 및 실시간 변수 출력
     */
    isSkillReady() {
        const isStun = typeof this.isStunned === 'function' ? this.isStunned() : false;
        const targetMax = this.maxGauge || 100;
        const currentGauge = this.gauge || 0;
        const percent = Math.floor((currentGauge / targetMax) * 100);

        console.log(`🔍 [Skill Check] Class: ${this.className} | Gauge: ${currentGauge.toFixed(1)} / ${targetMax} (${percent}%) | Stunned: ${isStun} | HasActiveSkill: ${this.hasActiveSkill}`);

        if (isStun) {
            console.warn(`❌ [Skill Blocked] 이유: 기절 상태입니다. (StunTimer: ${this.stunTimer}s)`);
            return false;
        }

        if (currentGauge < targetMax) {
            console.warn(`❌ [Skill Blocked] 이유: 게이지 부족 (${currentGauge.toFixed(1)} < ${targetMax})`);
            return false;
        }

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
     * @param {number} canvasWidth 
     * @param {number} canvasHeight 
     * @param {number} totalSlots 
     */
    resetPosition(canvasWidth, canvasHeight, totalSlots) {
        const spacing = canvasWidth / (totalSlots + 1);
        this.x = spacing * (this.slotIndex + 1);
        this.y = canvasHeight - 180;
        this.targetX = this.x;
        this.targetY = this.y;
    }

    /**
     * 기절 상태 여부 확인
     * @returns {boolean}
     */
    isStunned() {
        return this.stunTimer > 0;
    }

    /**
     * 피격 대미지 처리 (무적 시간 판정 및 기절 트리거)
     * @param {number} amount 대미지 양 (기본 1)
     * @returns {boolean} 실제 피격 성공 여부
     */
    takeDamage(amount = 1) {
        // 이미 무적 상태이거나 기절 상태면 대미지 계산 무시
        if (this.invulnerableTimer > 0 || this.isStunned()) {
            return false;
        }

        // 대미지 차감
        this.hp = Math.max(0, this.hp - amount);
        
        // 피격 성공 시 1초간 무적 타임 부여
        this.invulnerableTimer = 1.0;

        // 체력이 0에 도달하면 3초간 전면 기절 발동 후 체력 완충
        if (this.hp <= 0) {
            this.stunTimer = 3.0; // 3초간 기절
            this.hp = this.maxHp; // 기절 해제 후 체력 풀회복
        }

        return true;
    }

    /**
     * 유저 조작(키보드/조이스틱/스페이스바 스킬)에 의한 목표 위치 갱신 및 스킬 발동
     * @param {object} keys 키 입력 상태 맵
     * @param {object} joystick 조이스틱 상태 객체
     * @param {object} skillParams 스킬 발동용 인자 객체 (gameLoop 상태)
     */
    handleHumanInput(keys, joystick, skillParams = null) {
        // 기절 중에는 조작 완전히 차단
        if (this.isStunned()) return;

        // 💡 [스페이스바 / 우클릭 스킬 다이렉트 트리거]: 스페이스바 또는 우클릭 시 스킬 직접 실행
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
            this.targetX = this.x + (dx / factor) * this.speed * 8;
            this.targetY = this.y + (dy / factor) * this.speed * 8;
        } else {
            this.targetX = this.x;
            this.targetY = this.y;
        }
    }

    /**
     * 유저/클라이언트 조작 패킷 수신 및 이동 처리
     * @param {object} inputAction 네트워크 입력 패킷
     * @param {object} skillParams 스킬 발동용 인자 객체
     */
    handleHumanInputPacket(inputAction, skillParams = null) {
        if (this.isStunned() || !inputAction) return;

        if (typeof inputAction.mouseX === 'number' && typeof inputAction.mouseY === 'number') {
            this.lastMousePos = { x: inputAction.mouseX, y: inputAction.mouseY };
        }

        // 💡 이동 및 마우스 좌표 업데이트만 전담 (스킬 이중 실행 유발 구문 제거)

        const len = Math.hypot(inputAction.dx, inputAction.dy);
        if (len > 0) {
            const factor = len > 1 ? len : 1;
            this.targetX = this.x + (inputAction.dx / factor) * this.speed * 8;
            this.targetY = this.y + (inputAction.dy / factor) * this.speed * 8;
        } else {
            this.targetX = this.x;
            this.targetY = this.y;
        }
    }

    /**
     * 프레임 업데이트 공통 처리
     * @param {number} dt 델타 타임
     * @param {number} canvasWidth 
     * @param {number} canvasHeight 
     * @param {Array} enemyBullets 적 탄환 배열
     * @param {Array} allyPlayers 아군 플레이어 배열
     */
    updateMovement(dt, canvasWidth, canvasHeight, enemyBullets = [], allyPlayers = []) {
        if (this.invulnerableTimer > 0) {
            this.invulnerableTimer = Math.max(0, this.invulnerableTimer - dt);
        }

        // 1. 동적 스탯 수정자/상태이상 파이프라인 타임 틱 업데이트
        this.updateModifiers(dt);

        // 2. 델타룬 스치기 체크 (BasePlayer에서 버퍼 오라 잔재 완전 제거)
        this.updateGraze(enemyBullets, dt);

        if (this.stunTimer > 0) {
            this.stunTimer = Math.max(0, this.stunTimer - dt);
            this.targetX = this.x;
            this.targetY = this.y;
            return;
        }

        const dx = this.targetX - this.x;
        const dy = this.targetY - this.y;
        const dist = Math.hypot(dx, dy);

        if (dist > 1) {
            const step = Math.min(dist, this.moveSpeed * dt);
            this.x += (dx / dist) * step;
            this.y += (dy / dist) * step;
        } else {
            this.x = this.targetX;
            this.y = this.targetY;
        }

        this.x = Math.max(this.radius, Math.min(canvasWidth - this.radius, this.x));
        this.y = Math.max(120, Math.min(canvasHeight - this.radius, this.y));
    }

    /**
     * 탄환 생성 및 사격 처리
     * @param {Array} bulletContainer 전역 플레이어 탄환 배열
     * @param {object} targetInfo 유저 마우스 위치 또는 보스 위치
     */
    shoot(bulletContainer, targetInfo) {
        // 기절 상태에서는 사격 완전 차단
        if (this.isStunned()) return;

        let targetAngle = -Math.PI / 2;

        if (this.isHuman) {
            // 유저 마우스 지점 지향 사격
            const mousePos = (targetInfo && targetInfo.mousePos) ? targetInfo.mousePos : { x: this.x, y: this.y - 100 };
            targetAngle = Math.atan2(mousePos.y - this.y, mousePos.x - this.x);
        } else {
            // AI 타겟팅: 보스 및 적 미니언 목록 전체 중 가장 가까운 적을 탐색
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
                const spread = (Math.random() - 0.5) * 0.15;
                targetAngle = Math.atan2(closestEnemy.y - this.y, closestEnemy.x - this.x) + spread;
            }
        }

        const bullet = new PlayerBullet(this.x, this.y, targetAngle, this.slotIndex, this.color);
        // 동적 스탯 파이프라인으로 최종 데미지 산출
        bullet.damage = Math.round(this.getModifiedStat('damage', bullet.damage));
        
        // 기체에 적용된 버프/상태이상 파이프라인을 탄환에도 전이
        bullet.modifiers = this.modifiers.map(m => ({ ...m }));
        bulletContainer.push(bullet);
    }

    /**
     * 공격 주기 업데이트 및 발사 트리거
     * @param {Function} shootCallback 사격 실행 함수
     */
    updateAttack(shootCallback) {
        // 기절 상태에서는 사격 쿨다운 차단
        if (this.isStunned()) return;

        this.attackCooldown++;
        if (this.attackCooldown >= this.attackSpeed) {
            shootCallback();
            this.attackCooldown = 0;
        }
    }

    /**
     * 기본 본체, HP 바 및 기절 연출 렌더링
     * @param {CanvasRenderingContext2D} ctx 
     */
    draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);

        // 1. 기절 상태 연출 (체력 0일 때 회색으로 변경 및 STUNNED 문구 표시)
        if (this.isStunned()) {
            ctx.globalAlpha = 0.6;
            
            // 회색 기체 바디
            ctx.beginPath();
            ctx.arc(0, 0, this.radius + 3, 0, Math.PI * 2);
            ctx.fillStyle = '#475569';
            ctx.fill();

            ctx.beginPath();
            ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = '#94a3b8';
            ctx.fill();

            // STUNNED 라벨 표기
            ctx.fillStyle = '#f43f5e';
            ctx.font = 'bold 9px Orbitron';
            ctx.textAlign = 'center';
            ctx.fillText(`STUNNED (${this.stunTimer.toFixed(1)}s)`, 0, -this.radius - 14);

            ctx.restore();
            return; // 기절 중에는 이하 오라/스치기 연출을 진행하지 않고 즉시 리턴
        }

        // 2. 델타룬 스치기(Graze) 피드백: 흰색 네온 테두리 원 깜빡임 (1:1 동일 크기)
        if (this.grazeEffectTimer > 0) {
            const alpha = this.grazeEffectTimer / 0.3;
            ctx.save();
            ctx.beginPath();
            ctx.arc(0, 0, this.grazeRadius, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`;
            ctx.lineWidth = 2;
            ctx.shadowColor = '#ffffff';
            ctx.shadowBlur = 10;
            ctx.stroke();
            ctx.restore();
        }

        // 7. 외곽 네온 글로우
        ctx.beginPath();
        ctx.arc(0, 0, this.radius + 5, 0, Math.PI * 2);
        ctx.fillStyle = this.color + '33';
        ctx.fill();

        // 8. 중앙 코어 바디
        ctx.beginPath();
        ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 10;
        ctx.fill();

        // 5. 상단 슬롯 및 제어 타입 라벨
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 9px Orbitron';
        ctx.textAlign = 'center';
        ctx.fillText(`P${this.id} [${this.isHuman ? 'USER' : 'AI'}]`, 0, -this.radius - 12);

        // 6. 하단 미니 HP 바 (5칸)
        const barWidth = 24;
        const barHeight = 3;
        const startX = -barWidth / 2;
        const startY = this.radius + 6;

        // 배경 바
        ctx.fillStyle = 'rgba(15, 23, 42, 0.8)';
        ctx.fillRect(startX, startY, barWidth, barHeight);

        // 현재 체력 비율 바
        const hpRatio = this.hp / this.maxHp;
        ctx.fillStyle = hpRatio > 0.4 ? '#22c55e' : '#f43f5e';
        ctx.fillRect(startX, startY, barWidth * hpRatio, barHeight);

        ctx.restore();

        // 💡 [깃발 버프 이펙트] 깃발 범위 내 아군 머리 위 하얀색 🚩 아이콘 및 오라 렌더링
        const hasBannerBuff = Array.isArray(this.modifiers) && this.modifiers.some(m => m.id === 'banner_tick_buff');
        if (hasBannerBuff && !this.isStunned()) {
            ctx.save();
            ctx.translate(this.x, this.y);

            // 하얀색 맥동 테두리 링
            const pulse = Math.sin(Date.now() * 0.01) * 2;
            ctx.beginPath();
            ctx.arc(0, 0, this.radius + 5 + pulse, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.9)';
            ctx.lineWidth = 1.5;
            ctx.shadowColor = '#ffffff';
            ctx.shadowBlur = 12;
            ctx.stroke();

            // 머리 위 🚩 깃발 아이콘 및 하얀색 TICK x1.2 표시
            ctx.fillStyle = '#ffffff';
            ctx.font = '12px "Font Awesome 6 Free", Orbitron, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('🚩', 0, -this.radius - 18);

            ctx.font = '900 8px Orbitron';
            ctx.fillText('TICK x1.2', 0, -this.radius - 8);

            ctx.restore();
        }
    }
}