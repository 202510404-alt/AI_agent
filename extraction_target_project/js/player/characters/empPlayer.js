import BasePlayer from '../basePlayer.js';

export class EmpPlayer extends BasePlayer {
    constructor(slotIndex) {
        super(slotIndex, 'empPlayer');

        this.className = 'EMP 펄서 (EMP)';
        this.themeColor = '#a855f7';
        this.hasActiveSkill = true;
        this.skillIconClass = 'fa-solid fa-burst';
        this.skillName = 'EMP';
        this.skillFloatText = 'EMP WAVE ACTIVATED!';

        this.maxGauge = 60;
        this.empWaveRadius = 0;
        this.empWaveActive = false;
        
        // 원본 탄환 배열 참조 저장용
        this.targetBulletContainers = [];
    }

    /**
     * EMP 발동 시 원본 탄환 객체들을 완전 무력화 (isDead = true & 배열 비우기)
     */
    useSkill(context = {}) {
        if (!super.useSkill(context)) return false;

        this.empWaveRadius = 10;
        this.empWaveActive = true;

        // 전달받은 원본 탄환 컨테이너들 수집
        const containers = [
            context.bossBullets,
            context.minionBullets,
            context.enemyBullets
        ].filter(Boolean);

        this.targetBulletContainers = containers;

        // 1. 현재 존재하는 모든 적 탄환 객체에 즉시 사망 플래그 처리 및 배열 소멸
        containers.forEach(container => {
            if (Array.isArray(container)) {
                container.forEach(bullet => {
                    if (bullet) bullet.isDead = true;
                });
                container.length = 0; // 배열 비우기
            }
        });

        return true;
    }

    /**
     * EMP 충격파가 확장되는 동안 화면 내 적 탄환 지속 소멸 처리
     */
    updateMovement(dt, canvasWidth, canvasHeight, enemyBullets = [], allyPlayers = []) {
        super.updateMovement(dt, canvasWidth, canvasHeight, enemyBullets, allyPlayers);

        if (this.empWaveActive) {
            this.empWaveRadius += dt * 1400; // 파동 확장 속도

            // 충격파 링이 퍼져나가는 동안 탄환 지속 제거
            if (Array.isArray(enemyBullets)) {
                for (let i = enemyBullets.length - 1; i >= 0; i--) {
                    const b = enemyBullets[i];
                    if (b) {
                        const dist = Math.hypot(b.x - this.x, b.y - this.y);
                        // EMP 파동 전면부에 닿은 적 탄환 무조건 소멸
                        if (dist <= this.empWaveRadius) {
                            b.isDead = true;
                            enemyBullets.splice(i, 1);
                        }
                    }
                }
            }

            // 화면 밖으로 파동이 모두 나갔을 때 종료
            if (this.empWaveRadius > Math.max(canvasWidth, canvasHeight) * 1.5) {
                this.empWaveActive = false;
                this.empWaveRadius = 0;
                this.targetBulletContainers = [];
            }
        }
    }

    /**
     * EMP 충격파 파동 및 네온 펄스 링 렌더링
     */
    draw(ctx, allyPlayers = []) {
        if (this.empWaveActive) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.beginPath();
            ctx.arc(0, 0, this.empWaveRadius, 0, Math.PI * 2);
            ctx.strokeStyle = '#a855f7';
            ctx.lineWidth = 6;
            ctx.shadowColor = '#c084fc';
            ctx.shadowBlur = 25;
            ctx.stroke();
            ctx.restore();
        }

        super.draw(ctx, allyPlayers);

        // EMP 펄서 외형 디테일 (회전하는 4방향 방전 핀 & 링)
        if (!this.isStunned()) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate((window.gameLoopInstance?.gameTime ?? 0) * 3);

            ctx.strokeStyle = this.themeColor;
            ctx.lineWidth = 1.5;
            ctx.shadowColor = '#c084fc';
            ctx.shadowBlur = 10;

            for (let i = 0; i < 4; i++) {
                ctx.rotate(Math.PI / 2);
                ctx.beginPath();
                ctx.moveTo(this.radius + 3, 0);
                ctx.lineTo(this.radius + 9, 0);
                ctx.stroke();
            }

            ctx.beginPath();
            ctx.arc(0, 0, this.radius + 4, 0, Math.PI * 2);
            ctx.setLineDash([4, 4]);
            ctx.stroke();

            ctx.restore();
        }
    }
}

export default EmpPlayer;
