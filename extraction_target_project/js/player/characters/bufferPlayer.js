/**
 * js/player/characters/bufferPlayer.js
 * 버퍼 직업 전용 클래스 (스펙, 70 게이지, 3초 오라, 10초 버프격리)
 */
import BasePlayer from '../basePlayer.js';

export class BufferPlayer extends BasePlayer {
    constructor(slotIndex) {
        super(slotIndex, 'bufferPlayer');
        
        // --- 버퍼 전용 독립 설정 ---
        this.className = '버퍼 (Buffer)';
        this.themeColor = '#f97316';               // 주황 테마 색상
        this.hasActiveSkill = true;                // 스킬 버튼 활성화
        this.skillIconClass = 'fa-solid fa-wand-magic-sparkles'; 
        this.skillName = 'AURA';
        this.skillFloatText = 'BUFF AURA!';        // 시전 팝업 텍스트
        
        this.maxGauge = 20;                        // 버퍼 게이지 한도 (자유롭게 수정 가능)
        this.activeAura = null;                    // { radius: 140, timer: 3.0 }
    }

    /**
     * 버퍼 전용 스킬 시전 (게이지 소모 및 3초 오라 생성)
     */
    useSkill(params = {}) {
        if (!super.useSkill(params)) return false;

        this.activeAura = {
            radius: 140,
            timer: 3.0
        };
        return true;
    }

    /**
     * 버퍼 3초 오라 감지 및 범위 내 아군 10초간 공격력 1.5배 부여
     */
    updateMovement(dt, canvasWidth, canvasHeight, enemyBullets = [], allyPlayers = []) {
        super.updateMovement(dt, canvasWidth, canvasHeight, enemyBullets, allyPlayers);

        if (this.activeAura) {
            this.activeAura.timer -= dt;
            if (this.activeAura.timer <= 0) {
                this.activeAura = null;
            } else {
                // allyPlayers가 전달되지 않거나 빈 배열일 때를 대비해 기본값 처리
                const targets = (Array.isArray(allyPlayers) && allyPlayers.length > 0) ? allyPlayers : [this];

                targets.forEach(p => {
                    if (p && typeof p.isStunned === 'function' && !p.isStunned()) {
                        const dist = Math.hypot(p.x - this.x, p.y - this.y);
                        // 기체 피격 반경(p.radius)까지 닿았을 때 즉시 감지
                        if (dist <= (this.activeAura.radius + (p.radius || 8))) {
                            if (typeof p.addModifier === 'function') {
                                p.addModifier({
                                    id: 'buffer_atk_aura',
                                    targetStat: 'damage',
                                    type: 'MULTIPLY',
                                    value: 1.5,
                                    duration: 10.0
                                });
                                // 틱 회복 속도 1.2배 버프 레이어 동시 적용 지원
                                p.addModifier({
                                    id: 'buffer_tick_aura',
                                    targetStat: 'gaugeTickRate',
                                    type: 'MULTIPLY',
                                    value: 1.2,
                                    duration: 0.5
                                });
                            }
                        }
                    }
                });
            }
        }
    }

    /**
     * 버퍼 전용 외형 및 오라 렌더링 + 버프를 적용받는 모든 아군 대상 추적 이펙트
     */
    draw(ctx, allyPlayers = []) {
        // 1. 3초 지속 주황색 범위 오라 (버퍼 본인 위치)
        if (this.activeAura) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.beginPath();
            ctx.arc(0, 0, this.activeAura.radius, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(249, 115, 22, 0.15)';
            ctx.strokeStyle = this.themeColor;
            ctx.lineWidth = 2;
            ctx.setLineDash([8, 6]);
            ctx.shadowColor = this.themeColor;
            ctx.shadowBlur = 15;
            ctx.fill();
            ctx.stroke();
            ctx.restore();
        }

        super.draw(ctx);

        // 2. 버퍼 외형 심볼 (네온 다이아몬드)
        if (!this.isStunned()) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(Math.PI / 4);
            ctx.strokeStyle = this.themeColor;
            ctx.lineWidth = 2;
            ctx.strokeRect(-10, -10, 20, 20);
            ctx.restore();
        }

        // 3. 💡 [버프 상태 아군 추적 이펙트] modifiers 파이프라인 버프가 존재하는 아군 추적 이펙트
        if (Array.isArray(allyPlayers)) {
            allyPlayers.forEach(p => {
                const hasAtkBuff = p && Array.isArray(p.modifiers) && p.modifiers.some(m => m.id === 'buffer_atk_aura');
                if (hasAtkBuff && !p.isStunned()) {
                    ctx.save();
                    ctx.translate(p.x, p.y);
                    
                    // 은은하게 회전하며 맥동하는 반투명 주황색 버프 테두리 링
                    const pulse = Math.sin(Date.now() * 0.008) * 2;
                    ctx.beginPath();
                    ctx.arc(0, 0, p.radius + 6 + pulse, 0, Math.PI * 2);
                    ctx.strokeStyle = 'rgba(249, 115, 22, 0.8)';
                    ctx.lineWidth = 1.5;
                    ctx.shadowColor = '#f97316';
                    ctx.shadowBlur = 8;
                    ctx.stroke();

                    // 상단에 ⚡ATK UP! 소형 네온 라벨 추적 표시
                    ctx.fillStyle = '#f97316';
                    ctx.font = '900 7px Orbitron';
                    ctx.textAlign = 'center';
                    ctx.fillText('⚡ATK x1.5', 0, -p.radius - 22);

                    ctx.restore();
                }
            });
        }
    }
}

export default BufferPlayer;