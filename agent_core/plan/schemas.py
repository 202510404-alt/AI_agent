"""
agent_core/plan/schemas.py
에이전트 파이프라인 전반에서 사용되는 표준 데이터 스키마 및 어댑터 모듈
"""

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from pathlib import Path

# ===========================================================================
# 🎛️ [디버그 설정] True: 파일로 상세 출력 / False: 연산 소모 0% 완전 차단
# ===========================================================================
DEBUG_MODE = True
LOG_FILE_PATH = Path("agent_debug.log")


def log_debug(message_func):
    """
    DEBUG_MODE가 False일 때는 문자열 생성 연산 자체를 호출하지 않아 자원 소모를 0으로 만듭니다.
    """
    if not DEBUG_MODE:
        return
    
    # 람다 함수나 콜백을 통해 로그 메시지를 지연 평가(Lazy Evaluation)
    msg = message_func() if callable(message_func) else message_func
    
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"[SCHEMAS DEBUG] {msg}\n")
    except Exception:
        pass


class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class SymbolRef:
    """코드 내 심볼(함수, 클래스 등) 위치 정보"""
    file_path: str
    symbol_name: str
    start_line: int
    end_line: int


@dataclass
class DebugLogSpec:
    """작업 단위별 예상 디버깅 로그 스펙"""
    expected_logs: List[str] = field(default_factory=list)
    log_targets: List[str] = field(default_factory=list)


@dataclass
class Task:
    """플래너가 생성하는 최소 실행 작업 단위"""
    task_id: str
    description: str
    target_files: List[str]
    read_symbols: List[SymbolRef] = field(default_factory=list)
    write_symbols: List[SymbolRef] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    debug_spec: Optional[DebugLogSpec] = None


@dataclass
class ExecutionResult:
    """단독 실행 및 검증 결과"""
    task_id: str
    success: bool
    output_log: str
    error_message: Optional[str] = None


def to_symbol_ref(raw_dict: Dict[str, Any], default_file: str = "") -> SymbolRef:
    """
    Indexer 및 Parsers가 리턴하는 딕셔너리 데이터를 에이전트 용 SymbolRef로 정규화합니다.
    """
    if DEBUG_MODE:
        log_debug(lambda: f"to_symbol_ref 변환 시작 - Raw Input: {raw_dict}, Default File: {default_file}")

    file_path = raw_dict.get("file_path", default_file)
    symbol_name = raw_dict.get("name", raw_dict.get("symbol_name", "unknown"))
    start_line = raw_dict.get("start_line", raw_dict.get("line_start", 0))
    end_line = raw_dict.get("end_line", raw_dict.get("line_end", 0))

    result = SymbolRef(
        file_path=file_path,
        symbol_name=symbol_name,
        start_line=start_line,
        end_line=end_line
    )

    if DEBUG_MODE:
        log_debug(lambda: f"to_symbol_ref 변환 완료 - Result SymbolRef: {result}")

    return result