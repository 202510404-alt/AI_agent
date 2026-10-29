/**
 * js/utils/seededRNG.js
 * 단일 masterSeed 기반의 독립 난수 시드 파생 시스템 (PRNG)
 * 
 * Mulberry32 알고리즘 기반으로 각 게임 시스템(보스, 플레이어 AI, 미니언, 증강)에
 * 완전히 격리된 독립 결정론적 난수 생성기를 파생합니다.
 */

/**
 * 32비트 정수 해시 함수 (시드 문자열/숫자를 고르게 분산)
 * @param {string|number} seed 
 * @returns {number} 32비트 부호 없는 정수
 */
function hashSeed(seed) {
    if (typeof seed === 'number') {
        let h = seed >>> 0;
        h = Math.imul(h ^ (h >>> 16), 0x85ebca6b);
        h = Math.imul(h ^ (h >>> 13), 0xc2b2ae35);
        return (h ^ (h >>> 16)) >>> 0;
    }
    const str = String(seed);
    let h = 0x811c9dc5;
    for (let i = 0; i < str.length; i++) {
        h ^= str.charCodeAt(i);
        h = Math.imul(h, 0x01000193);
    }
    return h >>> 0;
}

/**
 * Mulberry32 알고리즘 인스턴스 생성기
 * @param {number} initialSeed 
 */
export class Mulberry32PRNG {
    constructor(initialSeed) {
        this.seed = initialSeed >>> 0;
    }

    /**
     * 0.0 이상 1.0 미만의 부동소수점 난수 반환 [0, 1)
     * @returns {number}
     */
    next() {
        let t = (this.seed += 0x6D2B79F5);
        t = Math.imul(t ^ (t >>> 15), t | 1);
        t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    }

    /**
     * min 이상 max 미만의 부동소수점 난수 반환
     * @param {number} min 
     * @param {number} max 
     * @returns {number}
     */
    range(min, max) {
        return min + this.next() * (max - min);
    }

    /**
     * min 이상 max 이하의 정수 난수 반환
     * @param {number} min 
     * @param {number} max 
     * @returns {number}
     */
    rangeInt(min, max) {
        return Math.floor(this.range(min, max + 1));
    }

    /**
     * 지정된 확률(0.0 ~ 1.0)에 따른 boolean 반환
     * @param {number} chance 
     * @returns {boolean}
     */
    boolean(chance = 0.5) {
        return this.next() < chance;
    }
}

/**
 * 단일 masterSeed로부터 독립된 하위 시드 인스턴스들을 파생 관리하는 싱글톤 컨테이너
 */
class SeededRNGManager {
    constructor() {
        this.masterSeed = 1004;
        this.instances = {};
        this.initDerivations(this.masterSeed);
    }

    /**
     * 서버에서 동기화받은 단일 masterSeed로 모든 하위 난수 인스턴스를 파생 초기화
     * @param {number|string} masterSeed 
     */
    initDerivations(masterSeed) {
        this.masterSeed = masterSeed;
        const baseHash = hashSeed(masterSeed);

        // 요구된 독립 채널 목록 정의
        const channels = [
            'nextBoss',
            'bossMove',
            'bossAttack',
            'bossPattern',
            'playerAiSpread_P1',
            'playerAiSpread_P2',
            'playerAiSpread_P3',
            'playerAiSpread_P4',
            'minionMove',
            'minionAttack',
            'minionPattern',
            'randomUpgrade',
            'general' // 기타 범용
        ];

        this.instances = {};
        channels.forEach((name) => {
            // masterSeed 해시와 채널 문자열 해시를 결합하여 완벽히 독립된 시드 부여
            const subSeed = (baseHash ^ hashSeed(name)) >>> 0;
            this.instances[name] = new Mulberry32PRNG(subSeed);
        });

        console.log(`🎲 [SeededRNG] masterSeed(${masterSeed}) 기반 독립 난수 인스턴스 ${channels.length}개 파생 완료`);
    }

    /**
     * 파생 인스턴스 반환
     * @param {string} channelName 
     * @returns {Mulberry32PRNG}
     */
    get(channelName) {
        if (!this.instances[channelName]) {
            const baseHash = hashSeed(this.masterSeed);
            const subSeed = (baseHash ^ hashSeed(channelName)) >>> 0;
            this.instances[channelName] = new Mulberry32PRNG(subSeed);
        }
        return this.instances[channelName];
    }
}

// 전역 싱글톤 인스턴스 생성 및 export
export const seededRNG = new SeededRNGManager();

// 편의를 위한 독립 모듈별 바로가기 Getter
export const rngBoss = {
    nextBoss: () => seededRNG.get('nextBoss').next(),
    move: () => seededRNG.get('bossMove').next(),
    attack: () => seededRNG.get('bossAttack').next(),
    pattern: () => seededRNG.get('bossPattern').next()
};

export const rngPlayerAi = {
    getSpread: (slotIndex) => {
        const slotKey = `playerAiSpread_P${Math.max(1, Math.min(4, (slotIndex || 0) + 1))}`;
        return seededRNG.get(slotKey).next();
    },
    mistakeChance: (slotIndex) => {
        const slotKey = `playerAiSpread_P${Math.max(1, Math.min(4, (slotIndex || 0) + 1))}`;
        return seededRNG.get(slotKey).next();
    },
    mistakeChoice: (slotIndex) => {
        const slotKey = `playerAiSpread_P${Math.max(1, Math.min(4, (slotIndex || 0) + 1))}`;
        return seededRNG.get(slotKey).next();
    }
};

export const rngMinion = {
    move: () => seededRNG.get('minionMove').next(),
    attack: () => seededRNG.get('minionAttack').next(),
    pattern: () => seededRNG.get('minionPattern').next()
};

export const rngUpgrade = {
    randomUpgrade: () => seededRNG.get('randomUpgrade').next()
};

export default seededRNG;
