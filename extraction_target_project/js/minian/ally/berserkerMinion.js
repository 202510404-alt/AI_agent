/**
 * js/minian/ally/berserkerMinion.js
 * 탱커형 유도 관성 버서커: 캔버스 동적 크기(ctx.canvas) 자동 감지 맵 이탈 방지 적용
 */
import BaseAllyMinion from './baseAllyMinion.js';

export class BerserkerMinion extends BaseAllyMinion {
    constructor(owner, spawnX = 0, spawnY = 0) {
        super(owner, {
            radius: 13,
            hp: 120,        // 체력 120 고체력 탱커
            maxHp: 120,
            color: '#ef4444',
            fireRate: 1.3 // 와리가리 도끼 스윙 연사력
        });

        if (spawnX && spawnY) {
            this.x = spawnX;
            this.y = spawnY;
        }

        this.baseSpeed = 20; // 이동속도 1/2 감축 (90 px/s)
        this.weaponLength = 32;

        this.vx = 0;
        this.vy = 0;

        // 2초 소환중 연출 (검붉은 삼각형 회전 소환진, 소환 중 무적)
        this.spawnTimer = 2;
        this.isSpawning = true;

        // 광폭화 (HP 50% / 20 이하 시 +12 HP 회복 & 5초간 피격 50% 감쇄)
        this.isBerserkMode = false;
        this.berserkBuffTimer = 0;

        // 도끼 와리가리 애니메이션 변수
        this.axeSwingAngle = 0;
        this.axeSwingDir = 1;
        this.isSwinging = false;
        this.swingProgress = 0;
        this.targetAngle = 0;
    }

    takeDamage(amount) {
        if (this.isDead || this.isSpawning) return;

        // 광폭화 5초 버프 활성화 시 탄막 피해 50% 반감
        const finalDamage = (this.isBerserkMode && this.berserkBuffTimer > 0) ? amount * 0.5 : amount;

        this.hp -= finalDamage;

        // 체력 50% (20 HP) 이하에서 광폭화 1회 트리거
        if (this.hp <= 20 && !this.isBerserkMode) {
            this.isBerserkMode = true;
            this.hp = Math.min(this.maxHp, this.hp + 50); // +50 HP 회복
            this.berserkBuffTimer = 5.0;                   // 5초간 50% 반감 버프
        }

        if (this.hp <= 0) {
            this.hp = 0;
            this.isDead = true;
        }
    }

    updateMovement(enemyEntities = [], dt = 0.016) {
        super.updateMovement(enemyEntities, dt);
        if (this.isDead) return;

        // 소환 대기 연출 처리
        if (this.isSpawning) {
            this.spawnTimer -= dt;
            if (this.spawnTimer <= 0) {
                this.isSpawning = false;
            }
            return;
        }

        if (this.berserkBuffTimer > 0) {
            this.berserkBuffTimer -= dt;
        }

        // 유도미사일식 관성 곡선 이동
        const target = this.findClosestTarget(enemyEntities);
        if (target) {
            const dist = Math.hypot(target.x - this.x, target.y - this.y);
            this.targetAngle = Math.atan2(target.y - this.y, target.x - this.x);

            const idealDistance = (target.radius || 25) + this.radius + this.weaponLength;

            if (dist > idealDistance + 5) {
                const desiredVx = Math.cos(this.targetAngle) * this.baseSpeed;
                const desiredVy = Math.sin(this.targetAngle) * this.baseSpeed;

                this.vx = this.vx * 0.85 + desiredVx * 0.15;
                this.vy = this.vy * 0.85 + desiredVy * 0.15;
            } else {
                this.vx *= 0.8;
                this.vy *= 0.8;
            }

            this.x += this.vx * dt;
            this.y += this.vy * dt;
        }

        // 도끼 와리가리 스윙 애니메이션
        if (this.isSwinging) {
            this.swingProgress += dt * 18;
            this.axeSwingAngle = Math.sin(this.swingProgress) * 0.9 * this.axeSwingDir;

            if (this.swingProgress >= Math.PI) {
                this.isSwinging = false;
                this.swingProgress = 0;
                this.axeSwingAngle = 0;
                this.axeSwingDir *= -1;
            }
        }
    }

    updateAttack(enemyEntities = [], allyBullets = [], dt = 0.016) {
        if (this.isDead || this.isSpawning) return;

        this.attackTimer += dt;

        if (this.attackTimer >= this.fireRate) {
            const target = this.findClosestTarget(enemyEntities);
            if (target) {
                const dist = Math.hypot(target.x - this.x, target.y - this.y);
                const idealDistance = (target.radius || 25) + this.radius + this.weaponLength;

                if (dist <= idealDistance + 15) {
                    this.isSwinging = true;
                    this.swingProgress = 0;

                    if (typeof target.takeDamage === 'function') {
                        target.takeDamage(1); // 공격력 1
                    }
                    this.attackTimer = 0;
                }
            }
        }
    }

    draw(ctx) {
        if (this.isDead) return;

        // 💡 [동적 캔버스 크기 기반 맵 이탈 방지] 렌더링 시점의 캔버스 너비/높이에 맞춰 위치 클램핑
        if (ctx && ctx.canvas) {
            const margin = this.radius + 12;
            this.x = Math.max(margin, Math.min(ctx.canvas.width - margin, this.x));
            this.y = Math.max(margin, Math.min(ctx.canvas.height - margin, this.y));
        }

        ctx.save();
        ctx.translate(this.x, this.y);

        // 1. 2초 검붉은 선 회전 삼각형 소환진 연출
        if (this.isSpawning) {
            const spawnProgress = Math.max(0, 1 - (this.spawnTimer / 2));
            const scale = 0.3 + spawnProgress * 0.9;
            const rotAngle = Date.now() * 0.01;

            ctx.rotate(rotAngle);
            ctx.strokeStyle = '#dc2626';
            ctx.lineWidth = 2.5;
            ctx.shadowColor = '#991b1b';
            ctx.shadowBlur = 15;

            ctx.beginPath();
            for (let i = 0; i < 3; i++) {
                const a = (Math.PI * 2 / 3) * i;
                const sx = Math.cos(a) * (26 * scale);
                const sy = Math.sin(a) * (26 * scale);
                if (i === 0) ctx.moveTo(sx, sy);
                else ctx.lineTo(sx, sy);
            }
            ctx.closePath();
            ctx.stroke();

            ctx.restore();
            return;
        }

        // 2. 버서커 본체 렌더링 (광폭화 시 1.35배 거대화)
        const currentRadius = this.isBerserkMode ? this.radius * 1.35 : this.radius;

        if (this.isBerserkMode && this.berserkBuffTimer > 0) {
            const pulse = Math.sin(Date.now() * 0.02) * 5;
            ctx.shadowColor = '#ef4444';
            ctx.shadowBlur = 20 + pulse;
            ctx.fillStyle = '#b91c1c';
        } else {
            ctx.shadowColor = '#dc2626';
            ctx.shadowBlur = 8;
            ctx.fillStyle = '#f87171';
        }

        ctx.beginPath();
        ctx.arc(0, 0, currentRadius, 0, Math.PI * 2);
        ctx.fill();

        // 뿔 연출
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(-currentRadius * 0.5, -currentRadius * 0.5);
        ctx.lineTo(-currentRadius * 1.0, -currentRadius * 1.2);
        ctx.moveTo(currentRadius * 0.5, -currentRadius * 0.5);
        ctx.lineTo(currentRadius * 1.0, -currentRadius * 1.2);
        ctx.stroke();

        // 🪓 양날도끼 와리가리 스윙
        ctx.rotate(this.targetAngle + this.axeSwingAngle);

        const handleLen = currentRadius + 18;
        const axeSize = currentRadius * 0.85;

        // 도끼 자루
        ctx.strokeStyle = '#d97706';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(handleLen, 0);
        ctx.stroke();

        // 양날도끼 헤드
        ctx.fillStyle = this.isBerserkMode ? '#fca5a5' : '#e2e8f0';
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 1.5;

        ctx.beginPath();
        ctx.moveTo(handleLen - 2, 0);
        ctx.lineTo(handleLen + axeSize, -axeSize);
        ctx.lineTo(handleLen + axeSize * 1.2, 0);
        ctx.lineTo(handleLen + axeSize, axeSize);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        ctx.restore();
    }
}

export default BerserkerMinion;