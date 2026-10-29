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
    ANGLE_OFFSET_MIN_DEG: 1,         // 오차각 기본 최소치 (도)
    ANGLE_OFFSET_MAX_DEG: 1        // 오차각 기본 최대치 (도)
};

// 원격 랭킹 서버 기본 엔드포인트 URL
export const SERVER_CONFIG = {
    DEFAULT_LEADERBOARD_URL: 'http://localhost:3000/api/ranking',
    GAME_NAME: 'HumanLike_BulletHell_Arena'
};
