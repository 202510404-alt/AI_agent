/**
 * js/minion/enemy/neonDragonHatchling/neonDragonHatchling.js
 * 네온드래곤 본체에서 튀어나와 가장 가까운 플레이어를 추격하는 소형 해츨링 미니언
 */
import { BaseMinion, MINION_MOVE_MODE } from '../../baseMinion.js';
import { rngMinion } from '../../../utils/seededRNG.js';

export class NeonDragonHatchling extends BaseMinion {
    /**
     * @param {number} spawnX 보스 본체 사출 위치 X
     * @param {number} spawnY 보스 본체 사출 위치 Y
     * @param {object} parentBoss 네온드래곤 보스 인스턴스
     * @param {number} orbitAngle initial 회전 각도 (라디안)
     */
    constructor(spawnX, spawnY, parentBoss = null, orbitAngle = 0) {
        // isAlly = false (적군), 강렬한 네온 레드/핑크 색상
        super(spawnX, spawnY, false, '#f43f5e');

        this.radius = 12; // 강한 미니언에 맞춰 크기 살짝 확대
        this.maxHp = 2200;  
        this.hp = 2200;

        // 소멸 타이머 제거 (처치할 때까지 무제한 생존)
        this.lifeTimer = null;

        // 곡선/궤적 이동 전용 변수 (미니언 이동 독립 PRNG 적용)
        this.parentBoss = parentBoss;
        this.orbitRadius = 90 + rngMinion.move() * 40; // 보스 주변 90~130px 거리 유지
        this.orbitAngle = orbitAngle;               // 현재 회전 각도
        this.orbitSpeed = 1.8 + rngMinion.move() * 0.8; // 각속도 (초당 라디안)
        this.waveTime = rngMinion.move() * Math.PI * 2; // 곡선 파동 오프셋 타이머

        // 사격 능력치 
        this.attackInterval = 24; 
        this.bulletSpeed = 3;

        // 3번 ATTACH_PARENT 기반으로 보스 참조
        this.setMoveMode(MINION_MOVE_MODE.ATTACH_PARENT, { parentEntity: parentBoss });
    }

    /**
     * 보스 주변부 곡선/궤적 이동 커스텀 업데이트
     * @param {Array} targets 플레이어 슬롯 배열
     * @param {number} dt 델타 타임
     */
    updateMovement(targets = [], dt = 0.016) {
        if (this.isDead) return;

        // 수명 타이머 차감 및 제한시간 도달 시 사망
        if (this.lifeTimer !== null) {
            this.lifeTimer -= dt;
            if (this.lifeTimer <= 0) {
                this.isDead = true;
                return;
            }
        }

        if (this.parentBoss) {
            // 1. 보스 주변을 각속도에 따라 회전
            this.orbitAngle += this.orbitSpeed * dt;

            // 2. Sine Wave를 적용하여 딱딱한 원이 아닌 자연스럽게 부풀고 줄어드는 곡선 궤적 형성
            this.waveTime += dt * 3.0;
            const dynamicRadius = this.orbitRadius + Math.sin(this.waveTime) * 20;

            // 3. 보스 중심점 기준 회전 및 곡선 좌표 계산
            this.x = this.parentBoss.x + Math.cos(this.orbitAngle) * dynamicRadius;
            this.y = this.parentBoss.y + Math.sin(this.orbitAngle) * dynamicRadius;
        }
    }
    /**
     * 네온드래곤 해츨링 전용 렌더링 (체력 바 표시 포함)
     * @param {CanvasRenderingContext2D} ctx 
     */
    draw(ctx) {
        if (this.isDead) return;

        ctx.save();
        ctx.translate(this.x, this.y);

        // 외곽 네온 글로우 피라미드
        ctx.beginPath();
        ctx.moveTo(0, -this.radius - 3);
        ctx.lineTo(this.radius + 3, this.radius);
        ctx.lineTo(-this.radius - 3, this.radius);
        ctx.closePath();

        ctx.fillStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 10;
        ctx.fill();

        // 중앙 코어 세모
        ctx.beginPath();
        ctx.moveTo(0, -this.radius + 2);
        ctx.lineTo(this.radius - 2, this.radius - 2);
        ctx.lineTo(-this.radius + 2, this.radius - 2);
        ctx.closePath();
        ctx.fillStyle = '#ffffff';
        ctx.fill();

        // 상단 미니 체력 바 표시 (3 HP)
        const barW = 18;
        const barH = 2;
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(-barW / 2, -this.radius - 8, barW, barH);

        const currentW = Math.max(0, (this.hp / this.maxHp) * barW);
        ctx.fillStyle = '#f43f5e';
        ctx.fillRect(-barW / 2, -this.radius - 8, currentW, barH);

        ctx.restore();
    }
}

export default NeonDragonHatchling;