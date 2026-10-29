/**
 * js/minion/baseMinion.js
 * 모든 미니언(적/아군)의 기반이 되는 BaseMinion 추상 클래스
 */
import { MinionBullet } from './minionBullet.js';
import { rngMinion } from '../utils/seededRNG.js';

export const MINION_MOVE_MODE = {
    FOLLOW_TARGET: 'FOLLOW_TARGET', // 1모드: 가장 가까운 타깃과 일정 거리 유지하며 추적
    PATH_WAYPOINT: 'PATH_WAYPOINT', // 2모드: 지정된 궤적 경로(Waypoint) 따라 이동
    ATTACH_PARENT: 'ATTACH_PARENT'  // 3모드: 특정 부모 엔티티(보스/플레이어/다른 미니언) 옆에 부착되어 이동
};

export class BaseMinion {
    /**
     * @param {number} x 초기 X
     * @param {number} y 초기 Y
     * @param {boolean} isAlly 아군 여부 (true: 아군, false: 적군)
     * @param {string} color 네온 색상
     */
    constructor(x, y, isAlly = false, color = '#f59e0b') {
        this.x = x;
        this.y = y;
        this.radius = 8;
        this.color = color;
        this.isAlly = isAlly;

        // 체력 및 생존 능력치 (기본 3 HP)
        this.maxHp = 3;
        this.hp = 3;
        this.moveSpeed = 140; // px/s
        this.isDead = false;

        // 자연 소멸(수명 제한) 타이머 (null이면 무제한 생존, 숫자 지정 시 해당 초(s) 후 자동 소멸)
        this.lifeTimer = null; 

        // 사격 능력치 (플레이어 발사 속도의 약 1/4 ~ 1/3 수준)
        this.attackCooldown = 0;
        this.attackInterval = 28; // 프레임 주기
        this.bulletSpeed = 5;

        // 이동 모드 및 세부 변수
        this.moveMode = MINION_MOVE_MODE.FOLLOW_TARGET;
        
        // Mode 1: FOLLOW_TARGET 용
        this.keepDistance = 160; // 타깃과 유지할 일정 거리

        // Mode 2: PATH_WAYPOINT 용
        this.waypoints = [];     // [{x, y}, {x, y}, ...]
        this.currentWaypointIdx = 0;

        // Mode 3: ATTACH_PARENT 용
        this.parentEntity = null; // 부착될 대상 (보스, 플레이어 등)
        this.offsetX = 0;         // 부모 기준 상대 X 좌표
        this.offsetY = 0;         // 부모 기준 상대 Y 좌표
    }

    /**
     * 수명 제한 시간 설정 (초 단위)
     * @param {number} seconds 
     */
    setLifeTime(seconds) {
        this.lifeTimer = seconds;
    }

    /**
     * 대미지 피격 처리 (HP 차감 및 0 도달 시 사망 및 KILLED 반환)
     * @param {number} amount 
     * @returns {boolean} 사망 여부 (true일 경우 처치 인정)
     */
    takeDamage(amount = 1) {
        if (this.isDead) return false;

        this.hp -= amount;
        if (this.hp <= 0) {
            this.hp = 0;
            this.isDead = true;
            return true; // 처치 성공
        }
        return false;
    }

    /**
     * 이동 모드 및 매개변수 설정
     * @param {string} mode 
     * @param {object} params 
     */
    setMoveMode(mode, params = {}) {
        this.moveMode = mode;
        if (params.keepDistance !== undefined) this.keepDistance = params.keepDistance;
        if (params.waypoints !== undefined) this.waypoints = params.waypoints;
        if (params.parentEntity !== undefined) this.parentEntity = params.parentEntity;
        if (params.offsetX !== undefined) this.offsetX = params.offsetX;
        if (params.offsetY !== undefined) this.offsetY = params.offsetY;
    }

    /**
     * 대미지 입기
     * @param {number} amount 
     * @returns {boolean} 처치 여부
     */
    takeDamage(amount = 1) {
        this.hp -= amount;
        if (this.hp <= 0) {
            this.isDead = true;
            return true;
        }
        return false;
    }

    /**
     * 프레임 이동 업데이트
     * @param {Array} targets 공격/추적 대상 목록 (적군이면 플레이어 배열, 아군이면 보스 배열)
     * @param {number} dt 델타 타임
     */
    updateMovement(targets = [], dt = 0.016) {
        if (this.isDead) return;

        // 수명 타이머 차감 및 제한시간 도달 시 자동 사망
        if (this.lifeTimer !== null) {
            this.lifeTimer -= dt;
            if (this.lifeTimer <= 0) {
                this.isDead = true;
                return;
            }
        }

        switch (this.moveMode) {
            // [모드 1] 타깃과 일정 거리를 유지하며 이동
            case MINION_MOVE_MODE.FOLLOW_TARGET: {
                const closest = this.getClosestTarget(targets);
                if (closest) {
                    const dx = closest.x - this.x;
                    const dy = closest.y - this.y;
                    const dist = Math.hypot(dx, dy);

                    // 일정 거리(keepDistance)보다 멀면 접근, 너무 가까우면 뒤로 물러남
                    if (Math.abs(dist - this.keepDistance) > 10) {
                        const dir = dist > this.keepDistance ? 1 : -1;
                        const moveStep = this.moveSpeed * dt * dir;
                        this.x += (dx / dist) * moveStep;
                        this.y += (dy / dist) * moveStep;
                    }
                }
                break;
            }

            // [모드 2] 지정된 경로(Waypoint)를 순차 이동
            case MINION_MOVE_MODE.PATH_WAYPOINT: {
                if (this.waypoints.length === 0) break;

                const targetPt = this.waypoints[this.currentWaypointIdx];
                const dx = targetPt.x - this.x;
                const dy = targetPt.y - this.y;
                const dist = Math.hypot(dx, dy);

                if (dist < 5) {
                    // 다음 웨이포인트로 전환 (순환 방식)
                    this.currentWaypointIdx = (this.currentWaypointIdx + 1) % this.waypoints.length;
                } else {
                    const step = Math.min(dist, this.moveSpeed * dt);
                    this.x += (dx / dist) * step;
                    this.y += (dy / dist) * step;
                }
                break;
            }

            // [모드 3] 부모 객체 옆에 고정되어 오프셋 위치 유지
            case MINION_MOVE_MODE.ATTACH_PARENT: {
                if (this.parentEntity) {
                    this.x = this.parentEntity.x + this.offsetX;
                    this.y = this.parentEntity.y + this.offsetY;
                }
                break;
            }
        }
    }

    /**
     * 사격 업데이트 (±15도, 총 30도 오차각 오프셋 사격)
     * @param {Array} targets 
     * @param {Array} minionBulletsContainer 전역 미니언 탄환 배열
     */
    updateAttack(targets = [], minionBulletsContainer = []) {
        if (this.isDead) return;

        this.attackCooldown++;
        if (this.attackCooldown >= this.attackInterval) {
            const closest = this.getClosestTarget(targets);
            if (closest) {
                // 타깃을 향한 기본 라디안 각도
                const baseAngle = Math.atan2(closest.y - this.y, closest.x - this.x);

                // ±15도 범위 내 무작위 오차각 적용 (미니언 공격 PRNG 시드 적용)
                const spreadAngle = (rngMinion.attack() - 0.5) * (Math.PI / 6);
                const finalAngle = baseAngle + spreadAngle;

                const bullet = new MinionBullet(
                    this.x,
                    this.y,
                    finalAngle,
                    this.bulletSpeed,
                    this.color,
                    this.isAlly
                );
                minionBulletsContainer.push(bullet);
            }
            this.attackCooldown = 0;
        }
    }

    /**
     * 가장 가까운 타깃 검색 헬퍼
     * @param {Array} targets 
     * @returns {object|null}
     */
    getClosestTarget(targets = []) {
        let closest = null;
        let minDist = Infinity;
        for (const t of targets) {
            if (t.isStunned && t.isStunned()) continue; // 기절한 플레이어 제외
            const dist = Math.hypot(t.x - this.x, t.y - this.y);
            if (dist < minDist) {
                minDist = dist;
                closest = t;
            }
        }
        return closest;
    }

    /**
     * 미니언 렌더링
     * @param {CanvasRenderingContext2D} ctx 
     */
    draw(ctx) {
        if (this.isDead) return;

        ctx.save();
        ctx.translate(this.x, this.y);

        ctx.beginPath();
        ctx.moveTo(0, -this.radius - 2);
        ctx.lineTo(this.radius + 2, this.radius);
        ctx.lineTo(-this.radius - 2, this.radius);
        ctx.closePath();

        ctx.fillStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 8;
        ctx.fill();

        ctx.restore();
    }
}

export default BaseMinion;