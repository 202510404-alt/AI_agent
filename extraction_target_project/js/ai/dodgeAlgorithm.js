/**
 * js/ai/dodgeAlgorithm.js
 * 피로도(Fatigue) 기반 실수 확률(5%~35%) 및 Angle Offset 오차각, MISTAKE A/B/C 회피 궤적 계산 모듈
 */
import { AI_CONFIG } from '../config/constants.js';
import { degToRad, radToDeg } from '../utils/math.js';

export class DodgeAlgorithm {
    /**
     * 현재 피로도에 비례한 실수 발생 여부를 판정합니다.
     * @param {number} fatigue (0.0 ~ 1.0)
     * @returns {boolean} 실수 발생 여부
     */
    static shouldMakeMistake(fatigue) {
        const mistakeChance = AI_CONFIG.FATIGUE_MISTAKE_MIN + 
            (fatigue * (AI_CONFIG.FATIGUE_MISTAKE_MAX - AI_CONFIG.FATIGUE_MISTAKE_MIN));
        return Math.random() < mistakeChance;
    }

    /**
     * 점(point)과 선분(segment p1-p2) 사이의 최단 수직 거리를 계산합니다.
     */
    static getMinDistanceToSegment(px, py, x1, y1, x2, y2) {
        const dx = x2 - x1;
        const dy = y2 - y1;
        if (dx === 0 && dy === 0) return Math.hypot(px - x1, py - y1);

        let t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy);
        t = Math.max(0, Math.min(1, t));

        const projX = x1 + t * dx;
        const projY = y1 + t * dy;
        return Math.hypot(px - projX, py - projY);
    }

    /**
     * AI 위치가 특정 Hazard 영역 내부이거나, 안전거리(margin) 이내인지 검사
     */
    static isInsideHazard(px, py, area, margin = 0) {
        if (area.type === 'circle') {
            return Math.hypot(px - area.x, py - area.y) <= (area.radius + margin);
        } else if (area.type === 'laser') {
            const dist = this.getMinDistanceToSegment(px, py, area.x1, area.y1, area.x2, area.y2);
            return dist <= (area.width / 2 + margin);
        } else if (area.type === 'rect') {
            return px >= (area.minX - margin) && px <= (area.maxX + margin) &&
                   py >= (area.minY - margin) && py <= (area.maxY + margin);
        }
        return false;
    }

    /**
     * 도형별 최단 외곽 탈출 방향 단위 벡터(dirX, dirY)만 순수하게 산출
     */
    static getClosestBoundaryVector(px, py, area) {
        // 1. 원형 장판
        if (area.type === 'circle') {
            const dist = Math.hypot(px - area.x, py - area.y);
            if (dist === 0) return { dirX: 1, dirY: 0 };
            return {
                dirX: (px - area.x) / dist,
                dirY: (py - area.y) / dist
            };
        }

        // 2. 직선 / 레이저
        if (area.type === 'laser') {
            const dx = area.x2 - area.x1;
            const dy = area.y2 - area.y1;
            let t = ((px - area.x1) * dx + (py - area.y1) * dy) / (dx * dx + dy * dy);
            t = Math.max(0, Math.min(1, t));
            const projX = area.x1 + t * dx;
            const projY = area.y1 + t * dy;

            let perpX = px - projX;
            let perpY = py - projY;
            let pDist = Math.hypot(perpX, perpY);

            if (pDist === 0) {
                const angle = Math.atan2(dy, dx) + Math.PI / 2;
                perpX = Math.cos(angle);
                perpY = Math.sin(angle);
                pDist = 1;
            }

            return {
                dirX: perpX / pDist,
                dirY: perpY / pDist
            };
        }

        // 3. 사각형 구역
        if (area.type === 'rect') {
            const dLeft = px - area.minX;
            const dRight = area.maxX - px;
            const dTop = py - area.minY;
            const dBottom = area.maxY - py;
            const minD = Math.min(dLeft, dRight, dTop, dBottom);

            if (minD === dLeft) return { dirX: -1, dirY: 0 };
            if (minD === dRight) return { dirX: 1, dirY: 0 };
            if (minD === dTop) return { dirX: 0, dirY: -1 };
            return { dirX: 0, dirY: 1 };
        }

        return { dirX: 0, dirY: -1 };
    }

    /**
     * 3가지 위협 분기 상황별 정밀 회피 알고리즘
     */
    static calculateNormalDodge(player, dangerousBullets, dangerAreas = []) {
        const stepDist = 20; // 미세 자율 조향 보폭
        const predictTime = 0.22;
        const playerHitboxRadius = player.radius || 8;

        const wallMargin = 16;
        const mapMinX = wallMargin;
        const mapMaxX = 800 - wallMargin;
        const mapMinY = wallMargin;
        const mapMaxY = 600 - wallMargin;

        // A. 탄환 이동 진행 방향 선분 데이터 수집
        const bulletSegments = dangerousBullets.map(b => {
            const vx = b.vx || (b.speed ? Math.cos(b.angle || 0) * b.speed : 0);
            const vy = b.vy || (b.speed ? Math.sin(b.angle || 0) * b.speed : 0);
            return {
                x1: b.x, y1: b.y,
                x2: b.x + vx * predictTime, y2: b.y + vy * predictTime,
                // 플레이어 크기의 1.5배로 안전 반경 확대 (안전지대 여유 확보)
                safeBoundary: (b.radius || 5) + (playerHitboxRadius * 2) + 8
            };
        });

        // AI 몸통 1.5배 크기의 안전거리 Margin 정의
        const safeMarginDist = playerHitboxRadius * 1.5;

        // B. 현재 침범 중이거나 안전거리(safeMarginDist) 이내인 범위 공격 수집 및 중첩 탈출 방향 합성
        let combinedDirX = 0;
        let combinedDirY = 0;
        let insideHazardCount = 0;

        for (const area of dangerAreas) {
            // 경계선 밖이라도 몸통 1.5배 안전거리가 확보될 때까지 탈출 방향 유지
            if (this.isInsideHazard(player.x, player.y, area, safeMarginDist)) {
                const vectorInfo = this.getClosestBoundaryVector(player.x, player.y, area);
                combinedDirX += vectorInfo.dirX;
                combinedDirY += vectorInfo.dirY;
                insideHazardCount++;
            }
        }

        // 중첩된 벡터의 합산 정규화 (단위 방향 벡터로 변환)
        let combinedEscapeAngle = null;
        const vecLen = Math.hypot(combinedDirX, combinedDirY);
        if (insideHazardCount > 0 && vecLen > 0) {
            combinedDirX /= vecLen;
            combinedDirY /= vecLen;
            combinedEscapeAngle = Math.atan2(combinedDirY, combinedDirX);
        }

        const hasBullets = bulletSegments.length > 0;
        const hasActiveHazard = insideHazardCount > 0;

        // 1. [순수 탄환 상황]: 범위 공격이 없고 오직 탄환만 있을 때 현재 위치 고수 우선 검사
        if (!hasActiveHazard) {
            let currentPositionSafe = true;
            for (const seg of bulletSegments) {
                const distToTrajectory = this.getMinDistanceToSegment(player.x, player.y, seg.x1, seg.y1, seg.x2, seg.y2);
                if (distToTrajectory < seg.safeBoundary) {
                    currentPositionSafe = false;
                    break;
                }
            }

            if (currentPositionSafe) {
                return { targetX: player.x, targetY: player.y };
            }
        }

        // 2. [가중치 0% 정통 벡터 합성]: 탄환 궤적 차단 필터링 후 범위 공격 탈출 방향각 선택
        const sampleCount = 32;
        let bestTarget = { targetX: player.x, targetY: player.y };
        let maxAlignment = -Infinity;
        let safestFallbackTarget = { targetX: player.x, targetY: player.y };
        let minBulletOverlap = Infinity;

        for (let i = 0; i < sampleCount; i++) {
            const rad = (Math.PI * 2 / sampleCount) * i;
            const candX = player.x + Math.cos(rad) * stepDist;
            const candY = player.y + Math.sin(rad) * stepDist;

            // 맵 경계 이탈은 탐색 후보에서 즉시 배제
            if (candX < mapMinX || candX > mapMaxX || candY < mapMinY || candY > mapMaxY) {
                continue;
            }

            // [Step A] 탄환 궤적 선분 충돌 여부 절대 검사
            let hitsBullet = false;
            let bulletOverlapDist = 0;

            for (const seg of bulletSegments) {
                const distToTrajectory = this.getMinDistanceToSegment(candX, candY, seg.x1, seg.y1, seg.x2, seg.y2);
                if (distToTrajectory < seg.safeBoundary) {
                    hitsBullet = true;
                    bulletOverlapDist += (seg.safeBoundary - distToTrajectory);
                }
            }

            // 사방이 막혔을 때를 대비해 가장 덜 위험한 후보 저장
            if (bulletOverlapDist < minBulletOverlap) {
                minBulletOverlap = bulletOverlapDist;
                safestFallbackTarget = { targetX: candX, targetY: candY };
            }

            // 탄환 궤도를 침범하는 후보 각도는 즉시 탈락! (탄환 회피 최우선)
            if (hitsBullet) {
                continue;
            }

            // [Step B] 탄환으로부터 안전한 각도들 중 범위 탈출 방향 벡터(combinedEscapeAngle)와 가장 일치하는 각도 선택
            if (combinedEscapeAngle !== null) {
                const candDirX = Math.cos(rad);
                const candDirY = Math.sin(rad);
                const alignment = candDirX * combinedDirX + candDirY * combinedDirY;

                if (alignment > maxAlignment) {
                    maxAlignment = alignment;
                    bestTarget = { targetX: candX, targetY: candY };
                }
            } else {
                // 범위 공격이 없는 순수 탄환 상황이면 가장 먼저 발견된 안전각 스텝 채택 후 탈출
                bestTarget = { targetX: candX, targetY: candY };
                maxAlignment = 1.0;
                break;
            }
        }

        // 탄환을 피할 수 있는 완전한 안전 각도를 찾았다면 해당 위치로 스텝 이동
        if (maxAlignment !== -Infinity || !hasBullets) {
            return bestTarget;
        }

        // 탄환으로 사방이 갇힌 비상 상황 시 최소 피격 방향 선택
        return safestFallbackTarget;
    }

    /**
     * 실수(Mistake A, B, C) 회피 궤적 계산
     * @param {object} player 
     * @param {object} bullet 
     * @returns {{type: string, targetX: number, targetY: number, lockTime: number, label: string, color: string}}
     */
    static calculateMistakeDodge(player, bullet = null) {
        const mistakeType = Math.floor(Math.random() * 3);

        if (mistakeType === 0) {
            // MISTAKE A: 순간 패닉 / 조작 정지 (0.25초 동안 제자리 정지)
            return {
                type: 'PANIC!',
                label: 'PANIC!',
                color: '#f43f5e',
                targetX: player.x,
                targetY: player.y,
                lockTime: 0.25
            };
        } else if (mistakeType === 1) {
            // MISTAKE B: 과도한 오버스티어 (탄환이 없어 null일 때도 safe 처리)
            const hasBullet = bullet && typeof bullet.x === 'number' && typeof bullet.y === 'number';
            const refX = hasBullet ? bullet.x : (player.x + 50);
            const refY = hasBullet ? bullet.y : (player.y - 50);

            const panicAngle = Math.atan2(player.y - refY, player.x - refX) + (Math.random() - 0.5) * 2.0;
            return {
                type: 'OVERSTEER',
                label: 'OVERSTEER!',
                color: '#f59e0b',
                targetX: player.x + Math.cos(panicAngle) * 45,
                targetY: player.y + Math.sin(panicAngle) * 45,
                lockTime: 0.3
            };
        } else {
            // MISTAKE C: 판단 미스 (불필요하게 살짝 피하거나 주춤거림)
            return {
                type: 'MISJUDGE',
                label: 'MISJUDGE!',
                color: '#8b5cf6',
                targetX: player.x + (Math.random() - 0.5) * 12,
                targetY: player.y + (Math.random() - 0.5) * 12,
                lockTime: 0.2
            };
        }
    }
}

export default DodgeAlgorithm;
