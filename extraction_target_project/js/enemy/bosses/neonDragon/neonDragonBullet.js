/**
 * js/enemy/bosses/neonDragon/neonDragonBullet.js
 * 네온 드래곤 보스의 탄환 클래스
 */

export class BossBullet {
    /**
     * @param {number} x 발사 위치 X
     * @param {number} y 발사 위치 Y
     * @param {number} angle 이동 각도 (라디안)
     * @param {number} speed 탄속
     * @param {string} color 네온 색상
     * @param {boolean} isHoming 유도 미사일 여부
     */
    constructor(x, y, angle, speed = 4, color = '#ec4899', isHoming = false) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.speed = speed;
        this.radius = isHoming ? 8 : 5;
        this.color = color;
        this.isHoming = isHoming;
        this.isAlly = false; // 적군 속성 명시 (아군 AI 회피 및 충돌 파이프라인 연동)

        // 2단계 경고/폭발 타이머 상태
        this.isWarning = false;       // 0.5초 경고 단계 (대미지 없음, AI 회피용 장판)
        this.warningTimer = 0.5;
        this.isDetonated = false;     // 경고 끝난 직후 실제 폭발 단계 (실제 대미지 발생)
        this.detonateTimer = 0.15;    // 0.15초 동안 진한 폭발 장판 유지

        this.explosionRadius = 32;   // 폭발 위험 범위
        this.proximityRadius = 22;   // 접근 시 기폭 유도 반경
        this.hasHitDamage = false;
    }

    /**
     * AI 범용 위험 구역 표준 규격(Hazard Area) 반환
     * @returns {object|null}
     */
    getHazardArea() {
        if (this.isWarning || this.isDetonated) {
            return {
                type: 'circle',
                x: this.x,
                y: this.y,
                radius: this.explosionRadius,
                isFiring: this.isDetonated, // 폭발 중일 때는 isFiring = true
                isWarning: this.isWarning   // 경고 중일 때는 isWarning = true
            };
        }
        return null;
    }

    /**
     * 탄환 위치 갱신 (경고 -> 폭발 2단계 제어)
     * @param {Array} players 플레이어 슬롯 배열
     * @param {number} dt 델타 타임 (초)
     */
    update(players = [], dt = 0.016) {
        // 2단계: 실제 폭발 진행 중 (진한 장판 0.15초 유지 후 완전히 소멸)
        if (this.isDetonated) {
            this.detonateTimer -= dt;
            if (this.detonateTimer <= 0) {
                this.isDead = true; // 폭발 완료 후 수명 종료 플래그 설정
            }
            return;
        }

        // 1단계: 0.5초 경고 타이머 진행 중 (정지 및 경고 원 표시)
        if (this.isWarning) {
            this.warningTimer -= dt;
            if (this.warningTimer <= 0) {
                this.isWarning = false;
                this.isDetonated = true; // 경고 종료 후 실제 폭발 전환
            }
            return;
        }

        // 유도 미사일 이동 추적
        if (this.isHoming && players.length > 0) {
            let closestPlayer = null;
            let minDist = Infinity;
            for (const p of players) {
                const dist = Math.hypot(p.x - this.x, p.y - this.y);
                if (dist < minDist) {
                    minDist = dist;
                    closestPlayer = p;
                }
            }

            if (closestPlayer) {
                const targetAngle = Math.atan2(closestPlayer.y - this.y, closestPlayer.x - this.x);
                let diff = targetAngle - this.angle;
                while (diff < -Math.PI) diff += Math.PI * 2;
                while (diff > Math.PI) diff -= Math.PI * 2;
                this.angle += Math.sign(diff) * Math.min(Math.abs(diff), 3 * dt);
            }
        }

        this.x += Math.cos(this.angle) * this.speed * dt * 60;
        this.y += Math.sin(this.angle) * this.speed * dt * 60;
    }

    /**
     * 유도탄 도달/적중 시 0.5초 경고 트리거
     */
    triggerExplosion() {
        if (!this.isWarning && !this.isDetonated) {
            this.isWarning = true;
            this.warningTimer = 0.5;
        }
    }

    /**
     * 탄환 렌더링
     * @param {CanvasRenderingContext2D} ctx 
     */
    draw(ctx) {
        // [실제 폭발 상태]: 0.15초간 붉은색 찐한 불꽃 장판 (이때만 플레이어 피격 대미지)
        if (this.isDetonated) {
            ctx.save();
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.explosionRadius, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(244, 63, 94, 0.85)';
            ctx.strokeStyle = '#ffe4e6';
            ctx.lineWidth = 3;
            ctx.shadowColor = '#f43f5e';
            ctx.shadowBlur = 24;
            ctx.fill();
            ctx.stroke();
            ctx.restore();
            return;
        }

        // [경고 상태]: 0.5초간 반투명 점선 원 깜빡임 (대미지 없음, AI는 미리 회피)
        if (this.isWarning) {
            ctx.save();
            const flashAlpha = Math.floor((window.gameLoopInstance?.gameTime ?? 0) / 0.08) % 2 === 0 ? 0.45 : 0.15;

            // 1. 깜빡이는 반투명 경고 원
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.explosionRadius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(244, 63, 94, ${flashAlpha})`;
            ctx.strokeStyle = '#f43f5e';
            ctx.lineWidth = 2;
            ctx.setLineDash([6, 6]);
            ctx.fill();
            ctx.stroke();

            // 2. 폭발 대기 중인 탄환 코어
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = '#f43f5e';
            ctx.shadowColor = '#f43f5e';
            ctx.shadowBlur = 12;
            ctx.fill();

            ctx.restore();
            return;
        }

        // [일반 비행 상태]
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = this.isHoming ? 12 : 6;
        ctx.fill();
    }

    /**
     * 화면 이탈 또는 폭발 완료(소멸) 여부 반환
     * @param {number} width 
     * @param {number} height 
     * @returns {boolean}
     */
    isOutOfBounds(width, height) {
        if (this.isDead) return true; // 폭발 종료 시 바로 배열에서 제거되도록 설정
        return (this.y > height + 10 || this.x < -10 || this.x > width + 10 || this.y < -10);
    }
}

export default BossBullet;
