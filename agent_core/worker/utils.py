import json
import re
from pathlib import Path

def load_mission_file(root_dir: Path, mission_rel_path: str) -> dict:
    """JSON 미션 파일 로더 및 규격 검증"""
    mission_path = root_dir / mission_rel_path
    if not mission_path.exists():
        raise FileNotFoundError(f"미션 파일을 찾을 수 없습니다: {mission_path}")
    
    with open(mission_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    required_keys = ["task_id", "target_file", "debug_log_spec"]
    for key in required_keys:
        if key not in data:
            raise KeyError(f"미션 JSON에 필수 키가 누락되었습니다: '{key}'")
            
    return data


def clean_json_response(raw_response: str) -> str:
    """LLM 응답에서 마크다운 코드 블록(```json ...)을 제거하고 순수 JSON 문자열 추출"""
    text = raw_response.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return text.strip()


def safe_execute_step(
    factory, 
    prompt: str, 
    system_instruction: str, 
    response_mime_type: str = "application/json", 
    max_attempts: int = 10, 
    temperature: float = 0.0
) -> str:
    """Fail-Fast 감지 및 API Key/Model 자동 스위칭 실행기"""
    for attempt in range(1, max_attempts + 1):
        try:
            return factory.execute_worker_step(
                prompt=prompt,
                system_instruction=system_instruction,
                response_mime_type=response_mime_type,
                temperature=temperature
            )
        except Exception as e:
            err_str = str(e)
            print(f"⚡ [Fail-Fast 감지] 0초 만에 예외 포착 -> ({err_str[:80]}...) | 즉시 다음 Key/Model 조합 스위칭 ({attempt}/{max_attempts})")
            if hasattr(factory, "switch_to_next_key"):
                factory.switch_to_next_key(last_error_msg=err_str)
    raise RuntimeError("🚨 모든 Gemini API Key/Model 조합이 소진되었거나 오류로 인해 중단되었습니다.")