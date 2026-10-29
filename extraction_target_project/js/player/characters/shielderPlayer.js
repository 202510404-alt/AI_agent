/**
 * js/player/characters/shielderPlayer.js
 * 쉴더 직업 전용 클래스 (스펙: 70 게이지, 100 HP 방어막, 곡선 배리어 설치)
 * 
 * [Object & HP Sync]:
 * - 배리어 설치 및 HP 충돌 연산은 시전자(Owner) 기기에서 주도 수행 (Owner Authority).
 * - 상대 기기는 원격 방벽 상태를 동기화하여 표시.
 */
import BasePlayer from '../basePlayer.js';

export class ShielderPlayer extends BasePlayer {
    constructor(slotIndex) {
        super(slotIndex, 'shielderPlayer');

        // --- 쉴더 전용 메타 설정 ---
        this.className = '쉴더 (Shielder)';
        this.themeColor = '#3b82f6';                // 파란색 테마
        this.hasActiveSkill = true;
        this.skillIconClass = 'fa-solid fa-shield-halved';
        this.skillName = 'SHIELD';
        this.skillFloatText = 'BARRIER DEPLOYED!';

        this.maxGauge = 70;                         // 스킬 게이지 70
        this.activeShield = null;                   // 현재 설치된 배리어 정보
    }

    /**
     * 쉴더 전용 스킬 시전 (방어막 설치)
     * @param {object} targetInfo 마우스/조작 입력 및 보스 정보
     */
    useSkill(targetInfo = {}) {
        if (!super.useSkill(targetInfo)) return false;

        let deployAngle = -Math.PI / 2; // 기본 방향: 위쪽

        if (this.isHuman) {
            const keys = targetInfo.keys || {};
            let dx = 0;
            let dy = 0;

            if (keys['KeyW'] || keys['ArrowUp']) dy -= 1;
            if (keys['KeyS'] || keys['ArrowDown']) dy += 1;
            if (keys['KeyA'] || keys['ArrowLeft']) dx -= 1;
            if (keys['KeyD'] || keys['ArrowRight']) dx += 1;

            if (dx !== 0 || dy !== 0) {
                deployAngle = Math.atan2(dy, dx);
            } else {
                const mousePos = targetInfo.mousePos;
                if (mousePos) {
                    deployAngle = Math.atan2(mousePos.y - this.y, mousePos.x - this.x);
                }
            }
        } else {
            const boss = targetInfo.boss;
            const enemyMinions = targetInfo.enemyMinions || [];
            const allEnemies = [boss, ...enemyMinions].filter(e => e && !e.isDead);

            let closest = null;
            let minDist = Infinity;
            for (const enemy of allEnemies) {
                const d = Math.hypot(enemy.x - this.x, enemy.y - this.y);
                if (d < minDist) {
                    minDist = d;
                    closest = enemy;
                }
            }

            if (closest) {
                deployAngle = Math.atan2(closest.y - this.y, closest.x - this.x);
            }
        }

        // 곡선 배리어 생성 (체력 100, 반지름 70px, 90도 호)
        this.activeShield = {
            id: `shield_${this.slotIndex}_${Date.now()}`,
            x: this.x,
            y: this.y,
            angle: deployAngle,
            radius: 70,
            arcAngle: Math.PI / 2,
            hp: 100,
            maxHp: 100,
            thickness: 12,
            duration: 20.0
        };

        // 소유자(Owner)인 경우 전체 기기에 방벽 생성 브로드캐스트
        if (this.isLocalOwner && window.networkManager) {
            window.networkManager.sendObjectStateSync(this.slotIndex + 1, [this.activeShield]);
        }

        return true;
    }

    /**
     * 프레임 업데이트 및 배리어-적 탄환 충돌 상호작용 (Owner Authority)
     */
    updateMovement(dt, canvasWidth, canvasHeight, enemyBullets = [], allyPlayers = []) {
        super.updateMovement(dt, canvasWidth, canvasHeight, enemyBullets, allyPlayers);

        if (this.activeShield) {
            const shield = this.activeShield;
            shield.duration -= dt;

            if (shield.duration <= 0 || shield.hp <= 0) {
                this.activeShield = null;
                if (this.isLocalOwner && window.networkManager) {
                    window.networkManager.sendObjectStateSync(this.slotIndex + 1, []);
                }
                return;
            }

            // 💡 [Owner Authority]: 내 소유 기체(isLocalOwner)이거나 AI인 경우만 직접 HP 차감 연산
            const hasAuthority = this.isLocalOwner || !this.isHuman;

            if (hasAuthority) {
                let shieldDamaged = false;

                // 적 탄환 소멸 처리
                for (let i = enemyBullets.length - 1; i >= 0; i--) {
                    const b = enemyBullets[i];
                    if (!b || b.isDead) continue;

                    const dist = Math.hypot(b.x - shield.x, b.y - shield.y);

                    if (Math.abs(dist - shield.radius) <= shield.thickness + (b.radius || 4)) {
                        let bAngle = Math.atan2(b.y - shield.y, b.x - shield.x);
                        let diff = bAngle - shield.angle;

                        while (diff < -Math.PI) diff += Math.PI * 2;
                        while (diff > Math.PI) diff -= Math.PI * 2;

                        if (Math.abs(diff) <= shield.arcAngle / 2) {
                            b.isDead = true;
                            shield.hp -= 1;
                            shieldDamaged = true;

                            if (shield.hp <= 0) {
                                this.activeShield = null;
                                break;
                            }
                        }
                    }
                }

                // 보스 레이저(dangerAreas) 선분 차단 및 방패 내구도 차감
                if (this.activeShield && window.gameLoopInstance && window.gameLoopInstance.boss) {
                    const boss = window.gameLoopInstance.boss;
                    if (Array.isArray(boss.dangerAreas)) {
                        boss.dangerAreas.forEach(area => {
                            if (area.isFiring && this.activeShield) {
                                const A = shield.x - area.x1;
                                const B = shield.y - area.y1;
                                const C = area.x2 - area.x1;
                                const D = area.y2 - area.y1;
                                const dot = A * C + B * D;
                                const lenSq = C * C + D * D;
                                let param = -1;
                                if (lenSq !== 0) param = dot / lenSq;

                                let xx, yy;
                                if (param < 0) { xx = area.x1; yy = area.y1; }
                                else if (param > 1) { xx = area.x2; yy = area.y2; }
                                else { xx = area.x1 + param * C; yy = area.y1 + param * D; }

                                const distToLaser = Math.hypot(shield.x - xx, shield.y - yy);

                                if (Math.abs(distToLaser - shield.radius) <= shield.thickness + (area.width / 2)) {
                                    let laserAngle = Math.atan2(yy - shield.y, xx - shield.x);
                                    let diff = laserAngle - shield.angle;
                                    while (diff < -Math.PI) diff += Math.PI * 2;
                                    while (diff > Math.PI) diff -= Math.PI * 2;

                                    if (Math.abs(diff) <= shield.arcAngle / 2) {
                                        shield.hp -= 15 * dt;
                                        shieldDamaged = true;
                                        area.isBlockedByShield = true;
                                        if (shield.hp <= 0) {
                                            this.activeShield = null;
                                        }
                                    }
                                }
                            }
                        });
                    }
                }

                // 피해가 발생했거나 일정 주기마다 OBJECT_STATE_SYNC 전송
                if (this.isLocalOwner && window.networkManager && (shieldDamaged || Math.random() < 0.1)) {
                    window.networkManager.sendObjectStateSync(
                        this.slotIndex + 1,
                        this.activeShield ? [this.activeShield] : []
                    );
                }
            }

            // SafeSpot 계산
            if (this.activeShield) {
                const wallCenterX = shield.x + Math.cos(shield.angle) * shield.radius;
                const wallCenterY = shield.y + Math.sin(shield.angle) * shield.radius;
                const BODY_MARGIN = 22;

                const insideAngle = shield.angle + Math.PI;
                shield.safeSpot = {
                    x: wallCenterX + Math.cos(insideAngle) * BODY_MARGIN,
                    y: wallCenterY + Math.sin(insideAngle) * BODY_MARGIN,
                    radius: 18
                };
            }
        }
    }

    draw(ctx, allyPlayers = []) {
        super.draw(ctx, allyPlayers);

        // 배리어 호 렌더링
        if (this.activeShield) {
            const s = this.activeShield;
            ctx.save();
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.radius, s.angle - s.arcAngle / 2, s.angle + s.arcAngle / 2);
            ctx.lineWidth = s.thickness;
            ctx.strokeStyle = `rgba(59, 130, 246, ${Math.min(1.0, s.hp / s.maxHp)})`;
            ctx.stroke();

            // 배리어 HP 바 표기
            ctx.font = '9px Orbitron';
            ctx.fillStyle = '#60a5fa';
            ctx.textAlign = 'center';
            const textX = s.x + Math.cos(s.angle) * (s.radius + 15);
            const textY = s.y + Math.sin(s.angle) * (s.radius + 15);
            ctx.fillText(`SHIELD: ${Math.ceil(s.hp)}`, textX, textY);

            ctx.restore();
        }
    }
}

export default ShielderPlayer;
