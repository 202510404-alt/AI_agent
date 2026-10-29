/**
 * js/ai/aiEngine.js
 * 0.08s 반응 주기(Reaction Cycle), Action Lock 및 FSM (IDLE/DODGE/REPOSITION) 관리
 */
import { AI_CONFIG } from '../config/constants.js';
import { DodgeAlgorithm } from './dodgeAlgorithm.js';
import { getDistance } from '../utils/math.js';
import { rngPlayerAi } from '../utils/seededRNG.js';

export class AIEngine {
    /**
     * AI 슬롯 플레이어의 FSM 및 회피 의사결정 주기 실행
     * @param {object} player 플레이어 엔티티
     * @param {number} dt 경과 시간 (초)
     * @param {Array} allDangerousBullets 적 탄환 배열
     * @param {Array} enemyEntities 적 엔티티 배열
     * @param {Function} onFloatingText 플로팅 텍스트 콜백
     * @param {Array} allySlots 아군 슬롯 배열 (쉴드 탐색용)
     */
    static update(player, dt, allDangerousBullets, enemyEntities = [], onFloatingText, allySlots = []) {
        player.allySlots = allySlots; // player 객체에 아군 목록 바인딩
        // 1. 피로도 회복 처리
        if (player.fsmState !== 'DODGE') {
            player.dodgeFatigue = Math.max(0, player.dodgeFatigue - dt * AI_CONFIG.FATIGUE_RECOVERY_RATE);
        }

        // 2. 적군 속성 탄환만 필터링 (isAlly가 false이거나 적군 탄환)
        const enemyBullets = (allDangerousBullets || []).filter(b => b && b.isAlly === false);

        // 3. 실시간 근접 위협 탄환 수집
        const dangerBullets = this.findAllDangerousBullets(player, enemyBullets, AI_CONFIG.BASE_DANGER_RADIUS);

        // 4. 범용 위험 구역(Hazard Area) 자동 수집 (보스 + 미니언 + 적 탄환)
        const allDangerAreas = [];

        // A. 모든 적 엔티티 고유 위험 영역 수집 (경고선 및 발사중 레이저 모두 위험 영역 수집)
        (enemyEntities || []).forEach(enemy => {
            if (enemy && enemy.dangerAreas) {
                enemy.dangerAreas.forEach(area => {
                    // 경고선 단계(!area.isFiring) 및 실제 발사 단계(area.isFiring) 모두 피해야 하는 위험 구역으로 전송
                    allDangerAreas.push(area);
                });
            }
        });

        // B. 적 탄환 객체(유도 미사일 폭발 경고)가 선언한 범용 Hazard Area 수집
        for (let i = 0; i < enemyBullets.length; i++) {
            const bullet = enemyBullets[i];
            if (typeof bullet.getHazardArea === 'function') {
                const hazard = bullet.getHazardArea();
                if (hazard) {
                    hazard.id = hazard.id || `bullet_hazard_${i}_${bullet.x}_${bullet.y}`;
                    allDangerAreas.push(hazard);
                }
            }
        }

        // AI가 현재 최소 1개 이상의 범위 공격 내부에 속해 있는지 검사
        // AI 반경 1.5배의 Margin을 포함하여 범위 공격 접근 판정
        const safeMarginDist = player.radius ? player.radius * 1.5 : 12;
        const insideHazard = allDangerAreas.some(area => DodgeAlgorithm.isInsideHazard(player.x, player.y, area, safeMarginDist));

        // 💡 [단일 회피 엔진 원칙]: 위협(탄막/레이저) 존재 시 방패 안/밖 구분을 완전히 철거하고 단 하나의 DODGE 회피 알고리즘만 수행!
        const hasThreat = dangerBullets.length > 0 || insideHazard;

        if (hasThreat) {
            if (player.fsmState !== 'DODGE') {
                const angleError = rngPlayerAi.angleOffset(player.slotIndex, AI_CONFIG.ANGLE_OFFSET_MIN_DEG, AI_CONFIG.ANGLE_OFFSET_MAX_DEG);
                player.dodgeAngleOffset = angleError * Math.PI / 180;
            }
            // 위협 감지 시 0프레임 단일 회피 모드(DODGE) 강제 구동
            player.actionLockTimer = 0;
            player.fsmState = 'DODGE';
            player.dodgeFatigue = Math.min(1.0, player.dodgeFatigue + AI_CONFIG.FATIGUE_INCREASE_ON_DODGE);

            const triggerMistake = DodgeAlgorithm.shouldMakeMistake(player.dodgeFatigue, player.slotIndex);

            if (triggerMistake) {
                player.mistakesCount++;
                const refBullet = dangerBullets.length > 0 ? dangerBullets[0] : null;
                const mistake = DodgeAlgorithm.calculateMistakeDodge(player, refBullet);
                player.lastMistakeType = mistake.type;
                player.targetX = mistake.targetX;
                player.targetY = mistake.targetY;
                player.actionLockTimer = mistake.lockTime;

                if (onFloatingText) {
                    onFloatingText(player.x, player.y - 20, mistake.label, mistake.color);
                }
            } else {
                // 단 하나의 통합 회피 알고리즘 실행
                const normalDodge = DodgeAlgorithm.calculateNormalDodge(player, dangerBullets, allDangerAreas, player.dodgeAngleOffset);
                player.targetX = normalDodge.targetX;
                player.targetY = normalDodge.targetY;
            }
        } else {
            // 위협이 전혀 없을 때만 방패 안쪽 세이프존으로 이동(COVER) 또는 자유 배치(REPOSITION)
            const shieldSpot = this.calculateShieldSafeSpot(player, enemyEntities, (player.allySlots || []));

            if (shieldSpot) {
                player.fsmState = 'COVER';
                player.targetX = shieldSpot.x;
                player.targetY = shieldSpot.y;
                player.actionLockTimer = 0;
            } else {
                // REPOSITION 진입 시점에 단 한 번 전략 결정 (APPROACH 또는 RETREAT)
                if (player.fsmState !== 'REPOSITION' && player.fsmState !== 'COVER') {
                    player.fsmState = 'REPOSITION';
                    const stratRng = rngPlayerAi.getSpread(player.slotIndex);
                    const wallRng = rngPlayerAi.getSpread(player.slotIndex);
                    player.repositionStrategy = stratRng < 0.5 ? 'APPROACH' : 'RETREAT';
                    player.wallAvoidSide = wallRng < 0.5 ? 1 : -1;
                    const angleError = rngPlayerAi.angleOffset(player.slotIndex, AI_CONFIG.ANGLE_OFFSET_MIN_DEG, AI_CONFIG.ANGLE_OFFSET_MAX_DEG);
                    player.repositionAngleOffset = angleError * Math.PI / 180;
                }

                const primaryEnemy = (enemyEntities && enemyEntities.length > 0) ? enemyEntities[0] : null;

                if (primaryEnemy) {
                    const dx = primaryEnemy.x - player.x;
                    const dy = primaryEnemy.y - player.y;
                    const currentDist = Math.hypot(dx, dy);
                    const angleToBoss = Math.atan2(dy, dx);

                    const wallMargin = 16;
                    const mapMinX = wallMargin;
                    const mapMaxX = 1280 - wallMargin;
                    const mapMinY = 120;
                    const mapMaxY = 720 - wallMargin;

                    let moveAngle = null;

                    if (player.repositionStrategy === 'APPROACH') {
                        // [APPROACH 모드] 적 방향으로 이동
                        const MIN_SAFE_DIST = 240;
                        if (currentDist >= MIN_SAFE_DIST) {
                            moveAngle = angleToBoss;
                        }
                    } else {
                        // [RETREAT 모드] 적 반대 방향(후퇴) 기반 좌표 계산
                        let baseRetreatAngle = angleToBoss + Math.PI;

                        // 현재 위치 기준 사방 벽까지의 최소 여유 거리 계산
                        const distToLeft = player.x - mapMinX;
                        const distToRight = mapMaxX - player.x;
                        const distToBottom = mapMaxY - player.y;
                        const minDistToWall = Math.min(distToLeft, distToRight, distToBottom);

                        const WALL_THRESHOLD = 80; // 벽 감지 경계 거리

                        if (minDistToWall < WALL_THRESHOLD) {
                            // 벽에 가까워질수록 후퇴 각도에 좌/우 횡이동 성분을 합성하여 미끄러지듯 보간
                            const blendRatio = (WALL_THRESHOLD - minDistToWall) / WALL_THRESHOLD; // 0.0 ~ 1.0
                            const sideAngle = angleToBoss + (Math.PI / 2 * player.wallAvoidSide);
                            
                            // 뒤로 가는 힘 + 옆으로 꺾는 힘 합성
                            const dirX = Math.cos(baseRetreatAngle) * (1 - blendRatio) + Math.cos(sideAngle) * blendRatio;
                            const dirY = Math.sin(baseRetreatAngle) * (1 - blendRatio) + Math.sin(sideAngle) * blendRatio;
                            moveAngle = Math.atan2(dirY, dirX);
                        } else {
                            // 벽과의 여유가 충분할 때는 그대로 직후퇴
                            moveAngle = baseRetreatAngle;
                        }
                    }

                    if (moveAngle !== null) {
                        moveAngle += player.repositionAngleOffset || 0;
                        const stepDist = 15; // 단거리 보폭
                        let nextTargetX = player.x + Math.cos(moveAngle) * stepDist;
                        let nextTargetY = player.y + Math.sin(moveAngle) * stepDist;

                        player.targetX = Math.max(mapMinX, Math.min(mapMaxX, nextTargetX));
                        player.targetY = Math.max(mapMinY, Math.min(mapMaxY, nextTargetY));
                    } else {
                        player.targetX = player.x;
                        player.targetY = player.y;
                    }
                }
            }
        }

        if (player.actionLockTimer > 0) {
            player.actionLockTimer -= dt;
        }
    }

    /**
     * 지정된 탐지 반경(40px) 내에 존재하는 모든 위협 탄환 목록을 수집합니다.
     * @param {object} player 
     * @param {Array} bossBullets 
     * @param {number} dangerRadius 
     * @returns {Array}
     */
    static findAllDangerousBullets(player, bossBullets, dangerRadius) {
        const result = [];
        for (const bullet of bossBullets) {
            const dist = getDistance(player.x, player.y, bullet.x, bullet.y);
            if (dist <= dangerRadius) {
                result.push(bullet);
            }
        }
        // 가장 가까운 순서로 정렬
        return result.sort((a, b) => {
            const dA = getDistance(player.x, player.y, a.x, a.y);
            const dB = getDistance(player.x, player.y, b.x, b.y);
            return dA - dB;
        });
    }
    /**
     * 적->쉴드 오므라드는 그림자 기하학 및 안전 마진 갉아먹기를 적용한 AI 소형 스윗스팟 계산
     * @param {object} player 
     * @param {Array} enemyEntities 
     * @param {Array} allySlots 
     * @returns {{x: number, y: number}|null}
     */
    static calculateShieldSafeSpot(player, enemyEntities, allySlots) {
        // 1. 내구도가 남아있고 safeSpot이 선언된 아군 쉴드 탐색
        let activeShield = null;
        for (const ally of allySlots) {
            if (ally && ally.activeShield && ally.activeShield.hp > 0 && ally.activeShield.safeSpot) {
                activeShield = ally.activeShield;
                break;
            }
        }
        if (!activeShield) return null;

        // 2. [비상 회피 판정] 방패가 막지 못하는 측면 탄환/직격 레이저 범위 진입 시 COVER 해제
        const primaryEnemy = (enemyEntities && enemyEntities.length > 0) ? enemyEntities[0] : null;
        if (primaryEnemy && primaryEnemy.dangerAreas) {
            const safeMargin = (player.radius || 10) * 1.2;
            const insideUnblockedLaser = primaryEnemy.dangerAreas.some(area => {
                if (!area.isFiring || area.isBlockedByShield) return false;
                return DodgeAlgorithm.isInsideHazard(player.x, player.y, area, safeMargin);
            });

            if (insideUnblockedLaser) {
                return null; // 방패가 차단하지 못한 레이저는 DODGE 모드로 즉시 이탈
            }
        }

        const spot = activeShield.safeSpot;
        const distToSpot = Math.hypot(spot.x - player.x, spot.y - player.y);

        // 3. 스윗스팟 진입 판정 및 신속 진입 (12px 안착 반경 적용)
        if (distToSpot <= 320) {
            // 12px 이내로 안착 성공 시 흔들림 없이 즉시 제자리 사격
            if (distToSpot <= (spot.radius || 12)) {
                return { x: player.x, y: player.y };
            }
            // 스윗스팟 중심점으로 신속 이동
            return { x: spot.x, y: spot.y };
        }
        return null;
    }
}

export default AIEngine;
