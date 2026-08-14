"""
agent_core/pipeline/mission_loader.py
--------------------------------------
미션 파일 로드 및 LLM 안전 실행 래퍼 모듈
"""

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
    """LLM 응답 마크다운 블록 제거 및 JSON 텍스트 정제"""
    text = raw_response.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return text.strip()

def safe_execute_step(factory, prompt: str, system_instruction: str, response_mime_type: str = "application/json", max_attempts: int = 10, temperature: float = 0.0) -> str:
    """Fail-Fast 포착 및 Key/Model 스위칭 기반 안전 실행 래퍼"""
    if not hasattr(factory, "execute_worker_step"):
        raise AttributeError("제공된 factory 객체에 'execute_worker_step' 메서드가 존재하지 않습니다.")

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
            print(f"⚡ [Fail-Fast 감지] ({err_str[:80]}...) | 즉시 다음 Key/Model 스위칭 ({attempt}/{max_attempts})")
            if hasattr(factory, "switch_to_next_key"):
                factory.switch_to_next_key(last_error_msg=err_str)
    raise RuntimeError("🚨 모든 Gemini API Key/Model 조합이 소진되었습니다.")