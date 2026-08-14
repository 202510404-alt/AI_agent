"""
agent_core/debug_agent/verifiers/log_verifier.py
--------------------------------------------------
로그 정규식 패턴 자동 생성 및 레거시 미션 JSON 스펙 파싱 모듈
"""

import re
from typing import Dict, Any, List
from agent_core.debug_agent.schemas import DebugLogSpec


def build_log_regex_pattern(template_msg: str) -> str:
    """미션 디버그 로그 메시지의 변수 표기({step_id}, {eval_score} 등)를 Regex 유연 패턴으로 변환"""
    escaped = re.escape(template_msg.strip())
    # 1. 수치형/스코어 변수 ({eval_score}, {num}, {score} 등)
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*(?:num|score|val|count|x|y|id|index)[a-zA-Z0-9_]*\\\}', r'[-+]?\\d*\\.?\\d+', escaped)
    # 2. 불리언 변수
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*bool[a-zA-Z0-9_]*\\\}', r'(?i)(true|false|1|0)', escaped)
    # 3. Hex/Color 변수
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*hex[a-zA-Z0-9_]*\\\}', r'#?[a-fA-F0-9]{3,6}', escaped)
    # 4. 와일드카드 변수 및 공백 유연화
    escaped = re.sub(r'\\\{.*?\\\}', r'[\\s\\S]*?', escaped)
    escaped = re.sub(r'\\\s+', r'\\s+', escaped)
    return escaped


def parse_mission_to_debug_spec(mission_data: Dict[str, Any]) -> DebugLogSpec:
    """
    다양한 레거시 미션 JSON 키(debug_log_spec, expected_terminal_outputs, log_pattern 등)를
    표준 DebugLogSpec 타입으로 파싱/자동 변환해주는 어댑터 함수
    """
    debug_spec = mission_data.get("debug_log_spec", {})
    blueprint = mission_data.get("implementation_blueprint", {})

    # 1. 수집 채널 판단 ('stdio' or 'file')
    channel_type = debug_spec.get("channel_type") or mission_data.get("channel_type", "stdio")
    log_file_path = debug_spec.get("log_file_path") or mission_data.get("log_file_path")

    # 2. 패턴 통합 수집
    patterns: List[str] = []
    if mission_data.get("expected_terminal_outputs"):
        patterns.extend(mission_data["expected_terminal_outputs"])
    if debug_spec.get("log_pattern") and debug_spec["log_pattern"] not in patterns:
        patterns.append(debug_spec["log_pattern"])
    if debug_spec.get("expected_patterns"):
        for p in debug_spec["expected_patterns"]:
            if p not in patterns:
                patterns.append(p)

    # 3. 환경변수 토글 주입
    env_toggles = {}
    toggle_key = debug_spec.get("toggle_key") or blueprint.get("debug_toggle_key")
    if toggle_key:
        env_toggles[toggle_key] = "1"
        env_toggles[f"{toggle_key}_ENABLE"] = "true"

    return DebugLogSpec(
        channel_type=channel_type,
        log_file_path=log_file_path,
        expected_patterns=patterns,
        env_toggles=env_toggles,
        timeout_seconds=debug_spec.get("timeout_seconds", 15)
    )