# ==========================================================================
# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드
# [SCAN_MODE] EXTRACTION_TARGET_PROJECT
# ==========================================================================
# 📄 [요청 1] TARGET: js/ai/aiEngine.js (1-255라인)
# ----------------------------------------------------------
```python
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
```

# 📄 [요청 1 ➡️ 불러온함수 (getDistance 본체)] TARGET: extraction_target_project/js/utils/math.js (29-31라인)
# ----------------------------------------------------------
```python
export function getDistance(x1, y1, x2, y2) {
    return Math.hypot(x2 - x1, y2 - y1);
}
```

# 📄 [요청 1 ➡️ 불러온함수 (AIEngine 본체)] TARGET: extraction_target_project/js/ai/aiEngine.js (10-255라인)
# ----------------------------------------------------------
```python
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
```

# 📄 [요청 2] TARGET: js/core/input.js (1-298라인)
# ----------------------------------------------------------
```python
/**
 * js/core/input.js
 * 키보드, 마우스, 모바일 터치 가상 조이스틱 핸들러 및 네트워크 입력 제어기
 * 
 * [동작 명세]
 * 1. WASD/조이스틱/스페이스바 입력을 정제하여 네트워크 패킷(moveX, moveY, useSkill, timeStamp) 형태로 압축 전송.
 * 2. 이벤트 리스너 참조 시점 문제 해결 (Lazy Evaluation): this.networkManager || window.networkManager 실시간 탐색.
 * 3. 1회성 스킬 트리거 시 timeStamp 부여 및 전달.
 */
import { rngPlayerAi } from '../utils/seededRNG.js';

export class InputHandler {
    constructor() {
        this.keys = {};
        this.mousePos = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
        this.joystick = {
            active: false,
            pointerId: null,
            startX: 0,
            startY: 0,
            moveX: 0,
            moveY: 0
        };

        // 스킬 전용 1회성 트리거 큐 플래그
        this.skillTriggered = false;
        this.lastSkillTriggerTime = 0;

        // AI 자율 주행 모드 여부
        this.isAiMode = false;

        this.initKeyboard();
        this.initMouse();
        this.initJoystick();
    }

    /**
     * Lazy Evaluation 헬퍼: 현재 유효한 networkManager 인스턴스 실시간 탐색
     * @returns {import('../network/networkManager.js').NetworkManager|null}
     */
    getNetworkManager() {
        return this.networkManager || window.networkManager || null;
    }

    logLocalInput(action, posX, posY) {
        const net = this.getNetworkManager();
        const slot = net && net.mySlotIndex ? net.mySlotIndex : 1;
        console.log(`[LOCAL_INPUT] Slot P${slot} | Key: ${action} | Pos: (${posX ?? 'n/a'}, ${posY ?? 'n/a'})`);
    }

    /**
     * AI 모드 토글 및 설정
     * @param {boolean} [enable] 
     */
    setAiMode(enable) {
        if (typeof enable === 'boolean') {
            this.isAiMode = enable;
        } else {
            this.isAiMode = !this.isAiMode;
        }
        console.log(`🤖 [InputHandler] AI 모드 상태: ${this.isAiMode ? 'ON (AUTO)' : 'OFF (MANUAL)'}`);
        return this.isAiMode;
    }

    /**
     * 키보드 이벤트 리스너 등록
     */
    initKeyboard() {
        window.addEventListener('keydown', (e) => {
            if (!this.keys[e.code]) {
                if (e.code === 'Space' || e.key === ' ' || e.keyCode === 32) {
                    this.skillTriggered = true;
                    this.lastSkillTriggerTime = Date.now();
                    e.preventDefault();
                }
                // 💡 [Lazy Evaluation]: this.networkManager || window.networkManager 실시간 탐색
                const net = this.getNetworkManager();
                const player = window.gameLoopInstance?.slots?.[(this.getNetworkManager()?.mySlotIndex || 1) - 1];
                this.logLocalInput(e.code, player?.x, player?.y);
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('KEYBOARD', `Key Down: ${e.code}`);
                }
            }
            this.keys[e.code] = true;
        });

        window.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
    }

    /**
     * 마우스 리스너 등록 (UI 버튼과 캔버스 좌클릭 구별)
     */
    initMouse() {
        window.addEventListener('mousemove', (e) => {
            this.mousePos.x = e.clientX;
            this.mousePos.y = e.clientY;
        });

        window.addEventListener('mousedown', (e) => {
            // 💡 [Lazy Evaluation]
            const net = this.getNetworkManager();

            if (e.button === 2) {
                this.skillTriggered = true;
                this.lastSkillTriggerTime = Date.now();
                const player = window.gameLoopInstance?.slots?.[(this.getNetworkManager()?.mySlotIndex || 1) - 1];
                this.logLocalInput('RightClick', player?.x, player?.y);
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('MOUSE', 'Right Click (Skill Trigger)');
                }
            } else if (e.button === 0) {
                // UI 버튼 요소와 캔버스 구분
                const target = e.target;
                const isButton = target && (target.tagName === 'BUTTON' || target.closest('button'));
                const clickType = isButton ? `UI Button Click [${target.id || target.innerText || 'BTN'}]` : `Canvas Field Click (X:${e.clientX}, Y:${e.clientY})`;

                const player = window.gameLoopInstance?.slots?.[(this.getNetworkManager()?.mySlotIndex || 1) - 1];
                this.logLocalInput(clickType, player?.x, player?.y);
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('MOUSE_LEFT', clickType);
                }
            }
        });

        window.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
    }

    /**
     * 모바일 터치 조이스틱 인터랙션 초기화
     */
    initJoystick() {
        const joystickZone = document.getElementById('joystickZone');
        const joystickKnob = document.getElementById('joystickKnob');

        if (!joystickZone || !joystickKnob) return;

        joystickZone.style.touchAction = 'none';
        joystickKnob.style.pointerEvents = 'none';

        const updateJoystick = (clientX, clientY) => {
            const rect = joystickZone.getBoundingClientRect();
            this.joystick.startX = rect.left + rect.width / 2;
            this.joystick.startY = rect.top + rect.height / 2;
            const dx = clientX - this.joystick.startX;
            const dy = clientY - this.joystick.startY;
            const dist = Math.hypot(dx, dy);
            const maxDist = 35;

            const angle = Math.atan2(dy, dx);
            const intensity = Math.min(dist, maxDist);

            this.joystick.moveX = Math.cos(angle) * (intensity / maxDist);
            this.joystick.moveY = Math.sin(angle) * (intensity / maxDist);

            const knobX = Math.cos(angle) * intensity;
            const knobY = Math.sin(angle) * intensity;
            joystickKnob.style.transform = `translate(${knobX}px, ${knobY}px)`;
        };

        joystickZone.addEventListener('pointerdown', (e) => {
            if (this.joystick.active || (e.pointerType === 'mouse' && e.button !== 0)) return;
            this.joystick.active = true;
            this.joystick.pointerId = e.pointerId;
            joystickZone.setPointerCapture(e.pointerId);
            updateJoystick(e.clientX, e.clientY);
            e.preventDefault();
        });

        joystickZone.addEventListener('pointermove', (e) => {
            if (!this.joystick.active || e.pointerId !== this.joystick.pointerId) return;
            updateJoystick(e.clientX, e.clientY);
            e.preventDefault();
        });

        const endJoystick = (e) => {
            if (e.pointerId !== this.joystick.pointerId) return;
            this.joystick.active = false;
            this.joystick.pointerId = null;
            this.joystick.moveX = 0;
            this.joystick.moveY = 0;
            joystickKnob.style.transform = `translate(0px, 0px)`;
        };

        joystickZone.addEventListener('pointerup', endJoystick);
        joystickZone.addEventListener('pointercancel', endJoystick);
        joystickZone.addEventListener('lostpointercapture', endJoystick);
    }

    /**
     * playerAiSpread 독립 시드 기반 결정론적 AI 입력 액션 생성
     */
    getAiInputAction(slotIndex = 0, context = null) {
        let moveX = 0;
        let moveY = 0;
        let mouseX = this.mousePos.x;
        let mouseY = this.mousePos.y;
        let useSkill = false;

        const player = (context && context.player) || 
            (window.gameLoopInstance && window.gameLoopInstance.slots && window.gameLoopInstance.slots[slotIndex]);

        if (player) {
            const dx = (player.targetX || player.x) - player.x;
            const dy = (player.targetY || player.y) - player.y;
            const dist = Math.hypot(dx, dy);

            if (dist > 5) {
                const spreadAngle = (rngPlayerAi.getSpread(slotIndex) - 0.5) * 0.1;
                const baseAngle = Math.atan2(dy, dx) + spreadAngle;
                moveX = Math.cos(baseAngle);
                moveY = Math.sin(baseAngle);
            }

            const boss = (context && context.boss) || (window.gameLoopInstance && window.gameLoopInstance.boss);
            if (boss) {
                const aimSpread = (rngPlayerAi.getSpread(slotIndex) - 0.5) * 20;
                mouseX = boss.x + aimSpread;
                mouseY = boss.y + aimSpread;
            }

            if (player.dodgeFatigue > 0.8 && player.hasActiveSkill && !player.isSkillOnCooldown) {
                useSkill = rngPlayerAi.getSpread(slotIndex) < 0.3;
            }
        }

        const inputAction = {
            moveX,
            moveY,
            dx: moveX,
            dy: moveY,
            mouseX,
            mouseY,
            useSkill,
            timeStamp: Date.now()
        };
        return inputAction;
    }

    /**
     * 현재 프레임의 클라이언트 조작 상태 패킷 추출 (Continuous Movement & Trigger Action)
     */
    getInputAction(slotIndex = 0, context = null) {
        if (this.isAiMode) {
            return this.getAiInputAction(slotIndex, context);
        }

        let moveX = 0;
        let moveY = 0;

        if (this.keys['KeyW'] || this.keys['ArrowUp']) moveY -= 1;
        if (this.keys['KeyS'] || this.keys['ArrowDown']) moveY += 1;
        if (this.keys['KeyA'] || this.keys['ArrowLeft']) moveX -= 1;
        if (this.keys['KeyD'] || this.keys['ArrowRight']) moveX += 1;

        // 대각선 이동 정규화
        const len = Math.hypot(moveX, moveY);
        if (len > 0) {
            moveX /= len;
            moveY /= len;
        }

        if (this.joystick && this.joystick.active) {
            // 조이스틱 미세 오차 보정 및 안전 정규화
            const jLen = Math.hypot(this.joystick.moveX, this.joystick.moveY);
            if (jLen > 0.05) {
                moveX = this.joystick.moveX / (jLen > 1 ? jLen : 1);
                moveY = this.joystick.moveY / (jLen > 1 ? jLen : 1);
            }
        }

        const useSkill = this.skillTriggered;
        const skillTime = this.lastSkillTriggerTime || Date.now();
        this.skillTriggered = false;

        const myPlayer = (context && context.player) || 
            (window.gameLoopInstance && window.gameLoopInstance.slots && window.gameLoopInstance.slots[slotIndex]);

        const inputAction = {
            moveX,
            moveY,
            dx: moveX,
            dy: moveY,
            mouseX: this.mousePos.x,
            mouseY: this.mousePos.y,
            useSkill,
            timeStamp: skillTime,
            posX: myPlayer ? myPlayer.x : undefined,
            posY: myPlayer ? myPlayer.y : undefined,
            speed: myPlayer ? myPlayer.speed : undefined
        };

        return inputAction;
    }
}
```

# 📄 [요청 2 ➡️ 불러온함수 (updateJoystick 본체)] TARGET: extraction_target_project/js/core/input.js (144-162라인)
# ----------------------------------------------------------
```python
        const updateJoystick = (clientX, clientY) => {
            const rect = joystickZone.getBoundingClientRect();
            this.joystick.startX = rect.left + rect.width / 2;
            this.joystick.startY = rect.top + rect.height / 2;
            const dx = clientX - this.joystick.startX;
            const dy = clientY - this.joystick.startY;
            const dist = Math.hypot(dx, dy);
            const maxDist = 35;

            const angle = Math.atan2(dy, dx);
            const intensity = Math.min(dist, maxDist);

            this.joystick.moveX = Math.cos(angle) * (intensity / maxDist);
            this.joystick.moveY = Math.sin(angle) * (intensity / maxDist);

            const knobX = Math.cos(angle) * intensity;
            const knobY = Math.sin(angle) * intensity;
            joystickKnob.style.transform = `translate(${knobX}px, ${knobY}px)`;
        };
```

# 📄 [요청 2 ➡️ 불러온함수 (InputHandler 본체)] TARGET: extraction_target_project/js/core/input.js (12-298라인)
# ----------------------------------------------------------
```python
export class InputHandler {
    constructor() {
        this.keys = {};
        this.mousePos = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
        this.joystick = {
            active: false,
            pointerId: null,
            startX: 0,
            startY: 0,
            moveX: 0,
            moveY: 0
        };

        // 스킬 전용 1회성 트리거 큐 플래그
        this.skillTriggered = false;
        this.lastSkillTriggerTime = 0;

        // AI 자율 주행 모드 여부
        this.isAiMode = false;

        this.initKeyboard();
        this.initMouse();
        this.initJoystick();
    }

    /**
     * Lazy Evaluation 헬퍼: 현재 유효한 networkManager 인스턴스 실시간 탐색
     * @returns {import('../network/networkManager.js').NetworkManager|null}
     */
    getNetworkManager() {
        return this.networkManager || window.networkManager || null;
    }

    logLocalInput(action, posX, posY) {
        const net = this.getNetworkManager();
        const slot = net && net.mySlotIndex ? net.mySlotIndex : 1;
        console.log(`[LOCAL_INPUT] Slot P${slot} | Key: ${action} | Pos: (${posX ?? 'n/a'}, ${posY ?? 'n/a'})`);
    }

    /**
     * AI 모드 토글 및 설정
     * @param {boolean} [enable] 
     */
    setAiMode(enable) {
        if (typeof enable === 'boolean') {
            this.isAiMode = enable;
        } else {
            this.isAiMode = !this.isAiMode;
        }
        console.log(`🤖 [InputHandler] AI 모드 상태: ${this.isAiMode ? 'ON (AUTO)' : 'OFF (MANUAL)'}`);
        return this.isAiMode;
    }

    /**
     * 키보드 이벤트 리스너 등록
     */
    initKeyboard() {
        window.addEventListener('keydown', (e) => {
            if (!this.keys[e.code]) {
                if (e.code === 'Space' || e.key === ' ' || e.keyCode === 32) {
                    this.skillTriggered = true;
                    this.lastSkillTriggerTime = Date.now();
                    e.preventDefault();
                }
                // 💡 [Lazy Evaluation]: this.networkManager || window.networkManager 실시간 탐색
                const net = this.getNetworkManager();
                const player = window.gameLoopInstance?.slots?.[(this.getNetworkManager()?.mySlotIndex || 1) - 1];
                this.logLocalInput(e.code, player?.x, player?.y);
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('KEYBOARD', `Key Down: ${e.code}`);
                }
            }
            this.keys[e.code] = true;
        });

        window.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
    }

    /**
     * 마우스 리스너 등록 (UI 버튼과 캔버스 좌클릭 구별)
     */
    initMouse() {
        window.addEventListener('mousemove', (e) => {
            this.mousePos.x = e.clientX;
            this.mousePos.y = e.clientY;
        });

        window.addEventListener('mousedown', (e) => {
            // 💡 [Lazy Evaluation]
            const net = this.getNetworkManager();

            if (e.button === 2) {
                this.skillTriggered = true;
                this.lastSkillTriggerTime = Date.now();
                const player = window.gameLoopInstance?.slots?.[(this.getNetworkManager()?.mySlotIndex || 1) - 1];
                this.logLocalInput('RightClick', player?.x, player?.y);
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('MOUSE', 'Right Click (Skill Trigger)');
                }
            } else if (e.button === 0) {
                // UI 버튼 요소와 캔버스 구분
                const target = e.target;
                const isButton = target && (target.tagName === 'BUTTON' || target.closest('button'));
                const clickType = isButton ? `UI Button Click [${target.id || target.innerText || 'BTN'}]` : `Canvas Field Click (X:${e.clientX}, Y:${e.clientY})`;

                const player = window.gameLoopInstance?.slots?.[(this.getNetworkManager()?.mySlotIndex || 1) - 1];
                this.logLocalInput(clickType, player?.x, player?.y);
                if (net && typeof net.sendDebugInput === 'function') {
                    net.sendDebugInput('MOUSE_LEFT', clickType);
                }
            }
        });

        window.addEventListener('contextmenu', (e) => {
            e.preventDefault();
        });
    }

    /**
     * 모바일 터치 조이스틱 인터랙션 초기화
     */
    initJoystick() {
        const joystickZone = document.getElementById('joystickZone');
        const joystickKnob = document.getElementById('joystickKnob');

        if (!joystickZone || !joystickKnob) return;

        joystickZone.style.touchAction = 'none';
        joystickKnob.style.pointerEvents = 'none';

        const updateJoystick = (clientX, clientY) => {
            const rect = joystickZone.getBoundingClientRect();
            this.joystick.startX = rect.left + rect.width / 2;
            this.joystick.startY = rect.top + rect.height / 2;
            const dx = clientX - this.joystick.startX;
            const dy = clientY - this.joystick.startY;
            const dist = Math.hypot(dx, dy);
            const maxDist = 35;

            const angle = Math.atan2(dy, dx);
            const intensity = Math.min(dist, maxDist);

            this.joystick.moveX = Math.cos(angle) * (intensity / maxDist);
            this.joystick.moveY = Math.sin(angle) * (intensity / maxDist);

            const knobX = Math.cos(angle) * intensity;
            const knobY = Math.sin(angle) * intensity;
            joystickKnob.style.transform = `translate(${knobX}px, ${knobY}px)`;
        };

        joystickZone.addEventListener('pointerdown', (e) => {
            if (this.joystick.active || (e.pointerType === 'mouse' && e.button !== 0)) return;
            this.joystick.active = true;
            this.joystick.pointerId = e.pointerId;
            joystickZone.setPointerCapture(e.pointerId);
            updateJoystick(e.clientX, e.clientY);
            e.preventDefault();
        });

        joystickZone.addEventListener('pointermove', (e) => {
            if (!this.joystick.active || e.pointerId !== this.joystick.pointerId) return;
            updateJoystick(e.clientX, e.clientY);
            e.preventDefault();
        });

        const endJoystick = (e) => {
            if (e.pointerId !== this.joystick.pointerId) return;
            this.joystick.active = false;
            this.joystick.pointerId = null;
            this.joystick.moveX = 0;
            this.joystick.moveY = 0;
            joystickKnob.style.transform = `translate(0px, 0px)`;
        };

        joystickZone.addEventListener('pointerup', endJoystick);
        joystickZone.addEventListener('pointercancel', endJoystick);
        joystickZone.addEventListener('lostpointercapture', endJoystick);
    }

    /**
     * playerAiSpread 독립 시드 기반 결정론적 AI 입력 액션 생성
     */
    getAiInputAction(slotIndex = 0, context = null) {
        let moveX = 0;
        let moveY = 0;
        let mouseX = this.mousePos.x;
        let mouseY = this.mousePos.y;
        let useSkill = false;

        const player = (context && context.player) || 
            (window.gameLoopInstance && window.gameLoopInstance.slots && window.gameLoopInstance.slots[slotIndex]);

        if (player) {
            const dx = (player.targetX || player.x) - player.x;
            const dy = (player.targetY || player.y) - player.y;
            const dist = Math.hypot(dx, dy);

            if (dist > 5) {
                const spreadAngle = (rngPlayerAi.getSpread(slotIndex) - 0.5) * 0.1;
                const baseAngle = Math.atan2(dy, dx) + spreadAngle;
                moveX = Math.cos(baseAngle);
                moveY = Math.sin(baseAngle);
            }

            const boss = (context && context.boss) || (window.gameLoopInstance && window.gameLoopInstance.boss);
            if (boss) {
                const aimSpread = (rngPlayerAi.getSpread(slotIndex) - 0.5) * 20;
                mouseX = boss.x + aimSpread;
                mouseY = boss.y + aimSpread;
            }

            if (player.dodgeFatigue > 0.8 && player.hasActiveSkill && !player.isSkillOnCooldown) {
                useSkill = rngPlayerAi.getSpread(slotIndex) < 0.3;
            }
        }

        const inputAction = {
            moveX,
            moveY,
            dx: moveX,
            dy: moveY,
            mouseX,
            mouseY,
            useSkill,
            timeStamp: Date.now()
        };
        return inputAction;
    }

    /**
     * 현재 프레임의 클라이언트 조작 상태 패킷 추출 (Continuous Movement & Trigger Action)
     */
    getInputAction(slotIndex = 0, context = null) {
        if (this.isAiMode) {
            return this.getAiInputAction(slotIndex, context);
        }

        let moveX = 0;
        let moveY = 0;

        if (this.keys['KeyW'] || this.keys['ArrowUp']) moveY -= 1;
        if (this.keys['KeyS'] || this.keys['ArrowDown']) moveY += 1;
        if (this.keys['KeyA'] || this.keys['ArrowLeft']) moveX -= 1;
        if (this.keys['KeyD'] || this.keys['ArrowRight']) moveX += 1;

        // 대각선 이동 정규화
        const len = Math.hypot(moveX, moveY);
        if (len > 0) {
            moveX /= len;
            moveY /= len;
        }

        if (this.joystick && this.joystick.active) {
            // 조이스틱 미세 오차 보정 및 안전 정규화
            const jLen = Math.hypot(this.joystick.moveX, this.joystick.moveY);
            if (jLen > 0.05) {
                moveX = this.joystick.moveX / (jLen > 1 ? jLen : 1);
                moveY = this.joystick.moveY / (jLen > 1 ? jLen : 1);
            }
        }

        const useSkill = this.skillTriggered;
        const skillTime = this.lastSkillTriggerTime || Date.now();
        this.skillTriggered = false;

        const myPlayer = (context && context.player) || 
            (window.gameLoopInstance && window.gameLoopInstance.slots && window.gameLoopInstance.slots[slotIndex]);

        const inputAction = {
            moveX,
            moveY,
            dx: moveX,
            dy: moveY,
            mouseX: this.mousePos.x,
            mouseY: this.mousePos.y,
            useSkill,
            timeStamp: skillTime,
            posX: myPlayer ? myPlayer.x : undefined,
            posY: myPlayer ? myPlayer.y : undefined,
            speed: myPlayer ? myPlayer.speed : undefined
        };

        return inputAction;
    }
}
```

# 📄 [요청 3] TARGET: js/player/basePlayer.js (350-420라인)
# ----------------------------------------------------------
```python

        // 💡 [이동 연산 및 권한 판정 완치]
        if (this.isLocalOwner) {
            // [로컬 기체]: 내 키보드/조이스틱 입력으로 부드럽고 정확하게 실시간 이동
            if (dist > 1) {
                const step = Math.min(dist, this.moveSpeed * dt);
                this.x += (dx / dist) * step;
                this.y += (dy / dist) * step;
            } else {
                this.x = this.targetX;
                this.y = this.targetY;
            }
        } else {
            // [원격 기체]: 네트워크 수신 좌표 부드러운 Lerp 추적 (상대방 위치 튀김 방지)
            if (dist > 150) {
                this.x = this.targetX;
                this.y = this.targetY;
            } else if (dist > 0.5) {
                this.x += dx * 0.25;
                this.y += dy * 0.25;
            }
        }
        // 맵 경계 제한
        this.x = Math.max(this.radius, Math.min(canvasWidth - this.radius, this.x));
        this.y = Math.max(120, Math.min(canvasHeight - this.radius, this.y));
    }

    /**
     * 탄환 생성 및 사격 처리
     */
    shoot(bulletContainer, targetInfo) {
        if (this.isStunned()) return;

        let targetAngle = -Math.PI / 2;

        if (this.isHuman) {
            const mousePos = (targetInfo && targetInfo.mousePos) ? targetInfo.mousePos : { x: this.x, y: this.y - 100 };
            targetAngle = Math.atan2(mousePos.y - this.y, mousePos.x - this.x);
        } else {
            const boss = targetInfo ? targetInfo.boss : null;
            const enemyMinions = targetInfo ? (targetInfo.enemyMinions || []) : [];
            const allEnemies = [boss, ...enemyMinions].filter(e => e && !e.isDead);

            let closestEnemy = null;
            let minDist = Infinity;

            for (const enemy of allEnemies) {
                const dist = Math.hypot(enemy.x - this.x, enemy.y - this.y);
                if (dist < minDist) {
                    minDist = dist;
                    closestEnemy = enemy;
                }
            }

            if (closestEnemy) {
                const baseAngle = Math.atan2(closestEnemy.y - this.y, closestEnemy.x - this.x);
                // 💡 [플레이어 AI 전용 오차각 적용]: AI_CONFIG 오차각 범위를 결정론적 시드 난수로 추출하여 발사 각도에 가산
                const minDeg = (typeof AI_CONFIG !== 'undefined' && AI_CONFIG.ANGLE_OFFSET_MIN_DEG) ? AI_CONFIG.ANGLE_OFFSET_MIN_DEG : 20;
                const maxDeg = (typeof AI_CONFIG !== 'undefined' && AI_CONFIG.ANGLE_OFFSET_MAX_DEG) ? AI_CONFIG.ANGLE_OFFSET_MAX_DEG : 30;
                const degError = rngPlayerAi.angleOffset(this.slotIndex, minDeg, maxDeg);
                const radError = (degError * Math.PI) / 180;
                
                targetAngle = baseAngle + radError;
            }
        }

        bulletContainer.push(new PlayerBullet(this.x, this.y, targetAngle, this.color, this));
    }

    updateAttack(onShoot) {
        if (this.isStunned()) return;
```

# 📄 [요청 3 ➡️ 불러온함수 (PlayerBullet 본체)] TARGET: extraction_target_project/js/player/playerBullet.js (6-70라인)
# ----------------------------------------------------------
```python
export class PlayerBullet {
    /**
     * @param {number} x 시작 X
     * @param {number} y 시작 Y
     * @param {number} angle 진행 각도 (라디안)
     * @param {number} slotIndex 발사한 플레이어의 슬롯 인덱스
     * @param {string} color 탄환 네온 색상
     */
    constructor(x, y, angle, slotIndex, color) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.speed = 14;
        this.radius = 4;
        this.slotIndex = slotIndex;
        this.color = color;
        this.baseDamage = 22;
        this.damage = 22;
        this.modifiers = [];
    }

    /**
     * 탄환 자체 스탯 수정자 파이프라인 산출
     */
    getModifiedDamage() {
        let finalDmg = this.damage;
        for (const m of this.modifiers) {
            if (m.targetStat === 'bulletDamage' && m.type === 'MULTIPLY') {
                finalDmg *= m.value;
            }
        }
        return Math.round(finalDmg);
    }

    /**
     * 탄환 위치 업데이트
     */
    update() {
        this.x += Math.cos(this.angle) * this.speed;
        this.y += Math.sin(this.angle) * this.speed;
    }

    /**
     * 탄환 렌더링
     * @param {CanvasRenderingContext2D} ctx 
     */
    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 8;
        ctx.fill();
    }

    /**
     * 화면 바깥으로 나갔는지 확인
     * @param {number} width 캔버스 너비
     * @param {number} height 캔버스 높이
     * @returns {boolean}
     */
    isOutOfBounds(width, height) {
        return (this.y < -10 || this.x < -10 || this.x > width + 10 || this.y > height + 10);
    }
}
```

# 📄 [요청 4] TARGET: js/core/gameLoop.js (1-23라인)
# ----------------------------------------------------------
```python
/**
 * js/core/gameLoop.js
 * 메인 60fps requestAnimationFrame 루프, 충돌 판정, AI 시각화 및 렌더링 결합
 */
import { TOTAL_SLOTS, MATCH_CONFIG, CANVAS_GRID_SIZE } from '../config/constants.js';
import { PlayerFactory } from '../player/playerFactory.js';
import { BossFactory } from '../enemy/bossFactory.js';
import { AIEngine } from '../ai/aiEngine.js';
import { createImpactParticles, createFloatingText } from '../player/particle.js';
import { setGameSeed } from '../utils/math.js';
import { GameState } from './sceneManager.js';
import { sendScoreToServer } from '../network/scoreSender.js';

export class GameLoop {
    /**
     * @param {HTMLCanvasElement} canvas 
     * @param {CanvasRenderingContext2D} ctx 
     * @param {import('./sceneManager.js').SceneManager} sceneManager 
     * @param {import('./input.js').InputHandler} input 
     * @param {import('./ui.js').UIManager} ui 
     */
```

# 📄 [요청 4 ➡️ 불러온함수 (GameLoop 본체)] TARGET: extraction_target_project/js/core/gameLoop.js (14-23라인)
# ----------------------------------------------------------
```python
export class GameLoop {
    /**
     * @param {HTMLCanvasElement} canvas 
     * @param {CanvasRenderingContext2D} ctx 
     * @param {import('./sceneManager.js').SceneManager} sceneManager 
     * @param {import('./input.js').InputHandler} input 
     * @param {import('./ui.js').UIManager} ui 
     */
```

# 📄 [요청 5] TARGET: js/config/constants.js (1-42라인)
# ----------------------------------------------------------
```python
/**
 * js/config/constants.js
 * 게임 내 모든 전역 설정 및 상수를 정의하는 모듈
 */

// 화면 및 슬롯 설정
export const TOTAL_SLOTS = 4;
export const CANVAS_GRID_SIZE = 40;

// 각 플레이어 슬롯 고유 색상 (1번: Cyan, 2번: Pink, 3번: Emerald, 4번: Amber)
export const SLOT_COLORS = [
    '#06b6d4', // Cyan (User 기본 슬롯)
    '#ec4899', // Pink
    '#10b981', // Emerald
    '#f59e0b'  // Amber
];

// 게임 매치 기본 설정
export const MATCH_CONFIG = {
    DEFAULT_DURATION_SEC: 120, // 매치 지속 시간 (초)
    SCORE_PER_TICK: 80,        // 시간 경과 시 획득 기본 점수
    SCORE_ON_BOSS_KILL: 5000,  // 보스 처치 보너스 점수
    SCORE_PENALTY_HIT: 150,    // 피격 시 감점
    DAMAGE_SCORE_RATIO: 1.5    // 딜량 당 획득 점수 배율
};

export const AI_CONFIG = {
    REACTION_CYCLE: 0.01,             // AI 반응 및 판단 주기 (초 - 실시간 프레임 동기화)
    BASE_DANGER_RADIUS: 40,           // 탄막 감지 위험 반경 (px)
    FATIGUE_MISTAKE_MIN: 0.005,       // 최소 실수 확률 
    FATIGUE_MISTAKE_MAX: 0.02,       // 최대 피로 시 실수 확률 
    FATIGUE_INCREASE_ON_DODGE: 0.008, // 회피 기동 1회당 증가하는 피로도
    FATIGUE_RECOVERY_RATE: 0.6,       // 평상시 초당 피로도 회복량
    ANGLE_OFFSET_MIN_DEG: 10,        // 오차각 기본 최소치 (도)
    ANGLE_OFFSET_MAX_DEG: 15         // 오차각 기본 최대치 (도)
};

// 원격 랭킹 서버 기본 엔드포인트 URL
export const SERVER_CONFIG = {
    DEFAULT_LEADERBOARD_URL: 'http://localhost:3000/api/ranking',
    GAME_NAME: 'HumanLike_BulletHell_Arena'
};
```
