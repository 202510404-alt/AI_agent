/**
 * js/enemy/bosses/neonDragon/neonDragon.js
 * BaseBoss를 상속받은 네온 드래곤 보스 클래스
 */
import BaseBoss from '../../baseBoss.js';
import { NeonDragonPattern } from './neonDragonPattern.js';
import { rngBoss } from '../../../utils/seededRNG.js';
import { NeonDragonHatchling } from '../../../minian/enemy/neonDragonHatchling/neonDragonHatchling.js';

export class NeonDragon extends BaseBoss {
    /**
     * @param {number} x 
     * @param {number} y 
     */
    constructor(x, y) {
        super(x, y, 25000);
        this.dangerAreas = []; // AI 연동용 위험 구역 (레이저)

        // 부드러운 곡선 선회 이동용 웨이포인트 상태
        this.targetX = x;
        this.targetY = y;
        this.moveTimer = 0;
        this.moveInterval = 3.0; // 3초마다 다음 목적지 갱신
        this.moveSpeed = 120;    // 고정 이동 속도 (초당 120px 등속 이동)

        // 소환 관리 데이터
        this.hasSpawnedHatchlings = false;
        this.hatchlings = [];
    }

    /**
     * 상단 영역 내 새로운 목표점 추첨 (보스 이동 전용 PRNG 시드 적용)
     */
    pickNewTarget(canvasWidth) {
        const marginX = 150;
        this.targetX = marginX + rngBoss.move() * (canvasWidth - marginX * 2);
        this.targetY = 120 + rngBoss.move() * 120;
    }

    /**
     * 경고선 레이저 생성 (0.7초 경고)
     */
    addLaserWarning(x, y, angle, width = 40, duration = 0.7) {
        const length = 1200;
        this.dangerAreas.push({
            type: 'laser',
            x1: x,
            y1: y,
            x2: x + Math.cos(angle) * length,
            y2: y + Math.sin(angle) * length,
            width: width,
            angle: angle,
            timer: duration,
            maxDuration: duration,
            isFiring: false
        });
    }

    /**
     * 보스 이동 및 탄막/레이저 패턴 업데이트
     */
    update(bulletContainer, canvasWidth, players = [], dt = 0.016) {
        this.angle += 0.02;

        // 1. 주기적인 웨이포인트 산출 및 곡선 파동 이동
        this.moveTimer += dt;
        if (this.moveTimer >= this.moveInterval) {
            this.moveTimer = 0;
            this.pickNewTarget(canvasWidth);
        }

        const dx = this.targetX - this.x;
        const dy = this.targetY - this.y;
        const dist = Math.hypot(dx, dy);

        // 거리가 멀든 가깝든 step(속도 * dt) 단위로 항상 일정한 속도로 이동
        const step = this.moveSpeed * dt;

        if (dist > step) {
            const moveAngle = Math.atan2(dy, dx);
            const perpAngle = moveAngle + Math.PI / 2;
            const waveOffset = Math.sin(this.moveTimer * 4.0) * 1.5; // 곡선 선회 성분

            // 직진 등속 이동 힘 + 측면 곡선 파동 힘 합성
            this.x += (Math.cos(moveAngle) * step) + Math.cos(perpAngle) * waveOffset;
            this.y += (Math.sin(moveAngle) * step) + Math.sin(perpAngle) * waveOffset;
        } else {
            this.x = this.targetX;
            this.y = this.targetY;
        }

        // Danger Areas (레이저) 타이머 및 상태(경고 vs 발사) 관리
        for (let i = this.dangerAreas.length - 1; i >= 0; i--) {
            const area = this.dangerAreas[i];
            area.timer -= dt;

            if (area.timer <= 0 && !area.isFiring) {
                // 경고(0.7초) 종료 -> 레이저 0.35초 실제 발사(위험 최고조)
                area.isFiring = true;
                area.timer = 0.35; // 실제 발사 레이저 유지 시간
            } else if (area.timer <= 0 && area.isFiring) {
                // 발사 완료 후 소멸
                this.dangerAreas.splice(i, 1);
            }
        }

        // 등장 시 단 1회 해츨링 2마리 대칭 스폰 (재소환 없음)
        if (!this.hasSpawnedHatchlings) {
            this.hasSpawnedHatchlings = true;

            const h1 = new NeonDragonHatchling(this.x, this.y, this, 0);
            const h2 = new NeonDragonHatchling(this.x, this.y, this, Math.PI);

            this.hatchlings.push(h1, h2);

            if (window.gameLoopInstance && window.gameLoopInstance.enemyMinions) {
                window.gameLoopInstance.enemyMinions.push(h1, h2);
            }
        }

        this.patternTimer++;
        NeonDragonPattern.execute(bulletContainer, this.x, this.y, this.angle, this.patternTimer, players, this);
    }

    /**
     * 보스 체력 차감 및 체력 0 도달 시 해츨링 동시 사망 처리
     */
    takeDamage(damage) {
        this.hp -= damage;
        if (this.hp <= 0) {
            this.hp = this.maxHp;

            // 보스 사망 시 동시 사망 처리
            this.hatchlings.forEach(h => {
                if (h) h.isDead = true;
            });

            return true;
        }
        return false;
    }

    /**
     * 보스 및 경고선/레이저 렌더링
     */
    draw(ctx, canvasWidth) {
        // 1. 레이저 경고선 및 레이저 포격 렌더링
        this.dangerAreas.forEach(area => {
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(area.x1, area.y1);
            ctx.lineTo(area.x2, area.y2);

            if (area.isFiring) {
                // 실제 레이저 포격 (굵고 진한 네온)
                ctx.strokeStyle = '#f43f5e';
                ctx.lineWidth = area.width;
                ctx.shadowColor = '#f43f5e';
                ctx.shadowBlur = 20;
            } else {
                // 0.5초 빨간색 반투명 경고선
                ctx.strokeStyle = 'rgba(244, 63, 94, 0.35)';
                ctx.lineWidth = area.width;
                ctx.setLineDash([10, 10]);
            }
            ctx.stroke();
            ctx.restore();
        });

        // 2. [네온 드래곤 전용] 잔상 꼬리 궤적(Segments) 및 머리/코어 다각형 연출

        // A. 이동 히스토리 잔상(꼬리 마디) 기록 관리
        if (!this.history) this.history = [];
        this.history.unshift({ x: this.x, y: this.y });
        if (this.history.length > 12) this.history.pop(); // 꼬리 마디 개수 12개

        ctx.save();

        // B. 유연하게 따라오는 꼬리 마디(Tail Segments) 렌더링
        for (let i = this.history.length - 1; i >= 1; i--) {
            const pos = this.history[i];
            const ratio = 1 - (i / this.history.length); // 뒤로 갈수록 작아짐
            const segRadius = (this.radius * 0.4) * ratio;

            ctx.beginPath();
            ctx.arc(pos.x, pos.y, segRadius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(244, 63, 94, ${ratio * 0.6})`;
            ctx.shadowColor = '#f43f5e';
            ctx.shadowBlur = 12 * ratio;
            ctx.fill();
        }

        // C. 보스 머리/코어 (다이아몬드 네온 엠블럼 + 맥동 오라)
        ctx.translate(this.x, this.y);
        ctx.rotate(this.angle);

        // 외곽 회전 네온 링 (에너지 회전)
        ctx.beginPath();
        ctx.arc(0, 0, this.radius * 0.65, 0, Math.PI * 2);
        ctx.strokeStyle = '#f43f5e';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#f43f5e';
        ctx.shadowBlur = 15;
        ctx.stroke();

        // 중심 날카로운 네온 드래곤 다이아몬드 코어
        ctx.beginPath();
        const coreSize = this.radius * 0.5;
        ctx.moveTo(0, -coreSize);
        ctx.lineTo(coreSize * 0.7, 0);
        ctx.moveTo(0, -coreSize);
        ctx.lineTo(0, coreSize);
        ctx.lineTo(-coreSize * 0.7, 0);
        ctx.closePath();

        ctx.fillStyle = '#fda4af';
        ctx.shadowColor = '#e11d48';
        ctx.shadowBlur = 25;
        ctx.fill();

        ctx.restore();

        // 공통 HP 바 렌더링
        this.drawHpBar(ctx, canvasWidth);
    }
}

export default NeonDragon;
