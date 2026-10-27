/**
 * js/player/characters/shielderPlayer.js
 * 쉴더 직업 전용 클래스 (스펙: 70 게이지, 50 HP 방어막, 곡선 배리어 설치)
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
            // 유저 조작 시: 입력 중인 방향이 있으면 그 방향, 없으면 가장 가까운 적 방향
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
                // 가만히 있는 경우: 마우스 포인터 방향 또는 가장 가까운 적 향함
                const mousePos = targetInfo.mousePos;
                if (mousePos) {
                    deployAngle = Math.atan2(mousePos.y - this.y, mousePos.x - this.x);
                }
            }
        } else {
            // AI 슬롯: 가장 가까운 적(보스/미니언)을 향해 방어막 설치
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

        // 휘어진 곡선 배리어 생성 (체력 50, 반지름 70px, 각도 폭 Math.PI / 2)
        this.activeShield = {
            x: this.x,
            y: this.y,
            angle: deployAngle,
            radius: 70,              // 배리어 곡선 반지름
            arcAngle: Math.PI / 2,   // 90도 범위 곡선
            hp: 100,                  // 체력 100
            maxHp: 100,
            thickness: 12,           // 배리어 두께
            duration: 20.0           // 최대 20초 유지
        };

        return true;
    }

    /**
     * 프레임 업데이트 및 배리어-적 탄환 충돌 상호작용
     */
    updateMovement(dt, canvasWidth, canvasHeight, enemyBullets = [], allyPlayers = []) {
        super.updateMovement(dt, canvasWidth, canvasHeight, enemyBullets, allyPlayers);

        // 설치된 배리어가 있을 때 적 탄막 충돌 검사
        if (this.activeShield) {
            const shield = this.activeShield;
            shield.duration -= dt;

            // 적 탄환 소멸 처리
            for (let i = enemyBullets.length - 1; i >= 0; i--) {
                const b = enemyBullets[i];
                if (!b || b.isDead) continue;

                // 배리어 중심점(쉴더 위치)과의 거리
                const dist = Math.hypot(b.x - shield.x, b.y - shield.y);

                // 1. 반지름 호 범위에 들어왔는지 검사
                if (Math.abs(dist - shield.radius) <= shield.thickness + (b.radius || 4)) {
                    // 2. 탄환이 배리어의 각도 범주 내에 들어왔는지 검사
                    let bAngle = Math.atan2(b.y - shield.y, b.x - shield.x);
                    let diff = bAngle - shield.angle;

                    // Angle normalisation (-PI ~ PI)
                    while (diff < -Math.PI) diff += Math.PI * 2;
                    while (diff > Math.PI) diff -= Math.PI * 2;

                    if (Math.abs(diff) <= shield.arcAngle / 2) {
                        // 탄환 제거 및 배리어 HP 차감
                        b.isDead = true;
                        shield.hp -= 1;

                        if (shield.hp <= 0) {
                            this.activeShield = null;
                            break;
                        }
                    }
                }
            }

            // 2-B. 보스 레이저(dangerAreas) 선분 차단 및 방패 내구도 차감
            if (window.gameLoopInstance && window.gameLoopInstance.boss) {
                const boss = window.gameLoopInstance.boss;
                if (Array.isArray(boss.dangerAreas)) {
                    boss.dangerAreas.forEach(area => {
                        if (area.isFiring) {
                            // 선분(x1,y1 - x2,y2)과 방패 중심점(shield.x, y) 간 최단거리 산출
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

                            // 레이저가 방패 호(Arc) 배리어 영역을 통과하는지 검사
                            if (Math.abs(distToLaser - shield.radius) <= shield.thickness + (area.width / 2)) {
                                let laserAngle = Math.atan2(yy - shield.y, xx - shield.x);
                                let diff = laserAngle - shield.angle;
                                while (diff < -Math.PI) diff += Math.PI * 2;
                                while (diff > Math.PI) diff -= Math.PI * 2;

                                if (Math.abs(diff) <= shield.arcAngle / 2) {
                                    // 레이저 막아내며 지속 방패 HP 차감
                                    shield.hp -= 15 * dt;
                                    area.isBlockedByShield = true; // 레이저 흡수/차단 플래그
                                }
                            }
                        }
                    });
                }
            }

            // 🚨 [절대불변의 법칙]: safeSpot 기준점은 설치 원점(shield.x/y)이 아니라
            // "실제 방패 곡선 호(Arc) 벽면의 중앙선 위치(shield.radius = 70px)"이다.
            let closestEnemy = window.gameLoopInstance ? window.gameLoopInstance.boss : null;

            // 1. 방패 곡선 호(Arc) 벽면 중앙 좌표 산출 (원점 + 반지름 70px)
            const wallCenterX = shield.x + Math.cos(shield.angle) * shield.radius;
            const wallCenterY = shield.y + Math.sin(shield.angle) * shield.radius;

            // 2. 방패 벽면 중심에서 보스 반대편(방패 안쪽 깊숙한 곳)으로 캐릭터 몸통 유격(22px)만큼 들어간 스윗스팟
            const BODY_MARGIN = 22; // 캐릭터 히트박스가 방패 두께에 닿지 않는 안쪽 거리

            if (closestEnemy && !closestEnemy.isDead) {
                // [보스 -> 방패 벽면] 방향 연장선각
                const shadowAngle = Math.atan2(wallCenterY - closestEnemy.y, wallCenterX - closestEnemy.x);

                shield.safeSpot = {
                    x: wallCenterX + Math.cos(shadowAngle) * BODY_MARGIN,
                    y: wallCenterY + Math.sin(shadowAngle) * BODY_MARGIN,
                    radius: 18 // 18px 초정밀 안착 반경
                };
            } else {
                // 기본 방패 호 벽면 안쪽 깊이 지정
                const insideAngle = shield.angle + Math.PI;
                shield.safeSpot = {
                    x: wallCenterX + Math.cos(insideAngle) * BODY_MARGIN,
                    y: wallCenterY + Math.sin(insideAngle) * BODY_MARGIN,
                    radius: 18
                };
            }

            // 지속시간 다 되거나 HP 0이면 소멸
            if (shield && shield.duration <= 0) {
                this.activeShield = null;
            }
        }
    }

    /**
     * 쉴더 기체 외형 및 곡선 에너제틱 배리어 렌더링
     */
    draw(ctx, allyPlayers = []) {
        // 1. 휘어진 아름다운 곡선 배리어 (에너지 쉴드) 렌더링
        if (this.activeShield) {
            const shield = this.activeShield;
            ctx.save();
            ctx.translate(shield.x, shield.y);

            const startAngle = shield.angle - shield.arcAngle / 2;
            const endAngle = shield.angle + shield.arcAngle / 2;

            // 네온 외곽 글로우
            ctx.beginPath();
            ctx.arc(0, 0, shield.radius, startAngle, endAngle);
            ctx.lineWidth = shield.thickness;
            ctx.lineCap = 'round'; // 끝부분 둥근 모양!
            ctx.strokeStyle = `rgba(59, 130, 246, ${0.4 + (shield.hp / shield.maxHp) * 0.5})`;
            ctx.shadowColor = '#60a5fa';
            ctx.shadowBlur = 18;
            ctx.stroke();

            // 코어 빔 링
            ctx.beginPath();
            ctx.arc(0, 0, shield.radius, startAngle, endAngle);
            ctx.lineWidth = 4;
            ctx.strokeStyle = '#ffffff';
            ctx.stroke();

            // 배리어 잔여 HP 미니 내구도 텍스트
            ctx.font = '900 9px Orbitron';
            ctx.fillStyle = '#93c5fd';
            ctx.textAlign = 'center';
            const textX = Math.cos(shield.angle) * (shield.radius + 16);
            const textY = Math.sin(shield.angle) * (shield.radius + 16);
            ctx.fillText(`SHIELD: ${shield.hp}/${shield.maxHp}`, textX, textY);

            ctx.restore();
        }

        super.draw(ctx, allyPlayers);

        // 2. 쉴더 전용 기체 외형 (육각형 방패 심볼)
        if (!this.isStunned()) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.strokeStyle = this.themeColor;
            ctx.lineWidth = 1.5;

            ctx.beginPath();
            for (let i = 0; i < 6; i++) {
                const a = (Math.PI / 3) * i;
                const hx = Math.cos(a) * 11;
                const hy = Math.sin(a) * 11;
                if (i === 0) ctx.moveTo(hx, hy);
                else ctx.lineTo(hx, hy);
            }
            ctx.closePath();
            ctx.stroke();
            ctx.restore();
        }
    }
}

export default ShielderPlayer;