/**
 * js/utils/math.js
 * 벡터, 거리/각도 계산, 보간(Lerp) 등을 담당하는 유틸리티 모듈
 */

/**
 * 2D 점 간의 유클리드 거리를 계산합니다.
 * @param {number} x1 
 * @param {number} y1 
 * @param {number} x2 
 * @param {number} y2 
 * @returns {number} 거리
 */
import { seededRNG } from './seededRNG.js';

let currentSeed = 12345;

export function setGameSeed(seed) {
    currentSeed = seed;
    seededRNG.initDerivations(seed);
    // 전역 Math.random()을 독립 PRNG의 범용 난수로 덮어씌움
    Math.random = seededRandom;
}

export function seededRandom() {
    return seededRNG.get('general').next();
}

export function getDistance(x1, y1, x2, y2) {
    return Math.hypot(x2 - x1, y2 - y1);
}

/**
 * 두 점 사이의 방향 각도(Radian)를 계산합니다.
 * @param {number} fromX 
 * @param {number} fromY 
 * @param {number} toX 
 * @param {number} toY 
 * @returns {number} 각도 (라디안)
 */
export function getAngle(fromX, fromY, toX, toY) {
    return Math.atan2(toY - fromY, toX - fromX);
}

/**
 * 선형 보간(Lerp: Linear Interpolation) 함수
 * @param {number} start 시작 값
 * @param {number} end 목표 값
 * @param {number} factor 보간 비율 (0.0 ~ 1.0)
 * @returns {number} 보간된 값
 */
export function lerp(start, end, factor) {
    return start + (end - start) * factor;
}

/**
 * 도(degree) 단위를 라디안(radian) 단위로 변환합니다.
 * @param {number} deg 도
 * @returns {number} 라디안
 */
export function degToRad(deg) {
    return (deg * Math.PI) / 180;
}

/**
 * 라디안(radian) 단위를 도(degree) 단위로 변환합니다.
 * @param {number} rad 라디안
 * @returns {number} 도
 */
export function radToDeg(rad) {
    return (rad * 180) / Math.PI;
}

/**
 * 2D 벡터 연산 헬퍼 클래스
 */
export class Vector2D {
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }

    /**
     * 벡터의 크기(길이) 반환
     */
    length() {
        return Math.hypot(this.x, this.y);
    }

    /**
     * 벡터 정규화 (크기를 1로 맞춤)
     */
    normalize() {
        const len = this.length();
        if (len > 0) {
            this.x /= len;
            this.y /= len;
        }
        return this;
    }

    /**
     * 각도와 길이로부터 벡터 생성
     */
    static fromAngle(angle, length = 1) {
        return new Vector2D(Math.cos(angle) * length, Math.sin(angle) * length);
    }
}
