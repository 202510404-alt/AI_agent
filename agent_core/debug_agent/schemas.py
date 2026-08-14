"""
agent_core/debug_agent/schemas.py
----------------------------------
디버그 로그 표준 Pydantic 스키마 명세
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DebugLogSpec(BaseModel):
    """미션 파일 및 Worker Task에 정의되는 디버그 검증 스펙"""
    channel_type: str = Field(default="stdio", description="로그 수집 채널 ('stdio' | 'file')")
    log_file_path: Optional[str] = Field(default=None, description="channel_type이 'file'일 때 감시/읽기 대상 파일 경로")
    expected_patterns: List[str] = Field(default_factory=list, description="출력되어야 하는 정규식 또는 문자열 패턴 목록")
    env_toggles: Dict[str, str] = Field(default_factory=dict, description="디버그 활성화를 위해 실행 시 주입할 환경변수")
    timeout_seconds: int = Field(default=15, description="수집 및 실행 타임아웃(초)")


class CapturedLogResult(BaseModel):
    """수집기(Collector)가 실행/감시를 통해 캡처해온 표준 로그 결과 데이터"""
    success: bool = Field(description="로그 수집 및 프로세스 실행 성공 여부")
    channel_type: str = Field(description="사용된 수집 채널 ('stdio' | 'file')")
    raw_logs: str = Field(default="", description="수집된 원본 텍스트 로그")
    returncode: int = Field(default=0, description="프로세스 종료 코드 (stdio일 경우)")
    error_message: Optional[str] = Field(default=None, description="수집 중 발생한 예외/오류 메시지")


class VerificationResult(BaseModel):
    """DebugVerifier가 패턴 대조 및 검증 후 반환하는 최종 리포트"""
    verified: bool = Field(description="모든 기댓값이 정상 매칭되었는지 여부")
    failure_type: str = Field(default="NONE", description="실패 원인 구분 ('NONE' | 'FAST_CHECK_ERROR' | 'COLLECTION_ERROR' | 'LOG_PATTERN_MISMATCH' | 'RUNTIME_ERROR')")
    matched_patterns: List[str] = Field(default_factory=list, description="매칭 성공한 패턴 목록")
    missing_patterns: List[str] = Field(default_factory=list, description="매칭 실패한 패턴 목록")
    output: str = Field(default="", description="수집된 텍스트 로그")
    message: str = Field(default="", description="사용자 친화적 요약 메시지")
    execution_steps: List[str] = Field(default_factory=list, description="수행 단계별 추적 로그")
