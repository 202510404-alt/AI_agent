/**
 * js/network/scoreSender.js
 * 게임 매치 종료 시 랭킹 서버로 결과 데이터를 HTTP POST 전송하는 모듈
 */
import { SERVER_CONFIG } from '../config/constants.js';

/**
 * 게임 종료 시 점수, 닉네임, 기여도 및 날짜를 Wi-Fi 랭킹 서버로 HTTP POST 전송
 * @param {object} payload 
 * @param {number} payload.score 최종 팀 스코어
 * @param {string} [payload.nickname] 유저 닉네임
 * @param {Array} [payload.slotsStats] 각 슬롯별 기여도 및 딜량 데이터
 * @param {string} [payload.serverUrl] 대상 서버 엔드포인트 URL
 * @returns {Promise<object>} 응답 JSON 또는 에러 객체
 */
export async function sendScoreToServer(payload) {
    const targetUrl = payload.serverUrl || SERVER_CONFIG.DEFAULT_LEADERBOARD_URL;

    const bodyData = {
        game: SERVER_CONFIG.GAME_NAME,
        score: Math.floor(payload.score || 0),
        nickname: payload.nickname || 'Pilot-01',
        playedAt: new Date().toISOString(),
        details: payload.slotsStats || []
    };

    try {
        const response = await fetch(targetUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bodyData)
        });

        if (!response.ok) {
            console.warn(`[ScoreSender] 랭킹 서버 전송 상태 코드: ${response.status}`);
            return { success: false, status: response.status };
        }

        const data = await response.json().catch(() => ({ success: true }));
        console.log('[ScoreSender] 랭킹 전송 성공:', data);
        return { success: true, data };
    } catch (error) {
        // 네트워크 연결 불가 환경(오프라인 / 로컬 단독 시연 등)에서도 게임 흐름이 끊기지 않도록 방어
        console.warn('[ScoreSender] 랭킹 서버 연결 실패 (로컬 모드 진행):', error.message);
        return { success: false, error: error.message };
    }
}

export default sendScoreToServer;
