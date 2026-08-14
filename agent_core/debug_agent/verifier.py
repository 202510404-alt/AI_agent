"""
agent_core/debug_agent/verifier.py
-----------------------------------
단일화된 고도화 디버그 로그 검증기 (Debug Verifier Core Engine)
- Fast-Check 문법 검사 (verifiers.fast_verifier 위임)
- Stdio & File Collector 어댑터 바인딩
- 정규식 패턴 대조 & 예외 감지 (verifiers.log_verifier 위임)
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

from agent_core.debug_agent.schemas import DebugLogSpec, CapturedLogResult, VerificationResult
from agent_core.debug_agent.collectors import BaseLogCollector, StdioCollector, FileCollector
from agent_core.debug_agent.cli.cli_agent import CliPipelineAgent
from agent_core.debug_agent.verifiers import build_log_regex_pattern, parse_mission_to_debug_spec, run_fast_check


class DebugVerifier:
    """
    체계화된 디버그 로그 검증 오케스트레이터 (Debug Agent Engine)
    - Fast-Check 정적 문법 검사 (0.1초 포착)
    - 수집기 바인딩 (Stdio / File Collector 선택 실행)
    - 정규식 매칭 및 런타임 예외 트레이스 포착
    """
    def __init__(self, root_dir: Path, factory: Any = None):
        self.root_dir = Path(root_dir).resolve()
        self.factory = factory
        self.collectors: Dict[str, BaseLogCollector] = {
            "stdio": StdioCollector(self.root_dir),
            "file": FileCollector(self.root_dir)
        }
        self.cli_agent = CliPipelineAgent(self.root_dir, factory=self.factory)

    def verify(
        self,
        mission_data: Dict[str, Any],
        target_file_path: str,
        target_code: str = ""
    ) -> Dict[str, Any]:
        """
        통합 디버그 검증 진입점 (하위 호환성 dict 형태 반환)
        """
        execution_steps = []
        spec = parse_mission_to_debug_spec(mission_data)
        execution_steps.append(f"[STAGE 0] DebugLogSpec 정제 완료 (채널: {spec.channel_type}, 패턴 수: {len(spec.expected_patterns)})")

        # -------------------------------------------------------------
        # Stage 1: Fast-Check (정적 문법 검사)
        # -------------------------------------------------------------
        execution_steps.append(f"[STAGE 1] Fast-Check 문법 검사 수행 중: {target_file_path}")
        fast_res = run_fast_check(self.root_dir, target_file_path)
        if not fast_res["success"]:
            execution_steps.append(f"[STAGE 1 FAIL] 문법 검사 실패: {fast_res['failure_type']}")
            return VerificationResult(
                verified=False,
                failure_type=fast_res["failure_type"],
                output=fast_res["output"],
                message=fast_res["message"],
                execution_steps=execution_steps,
                missing_patterns=spec.expected_patterns
            ).model_dump()

        execution_steps.append("[STAGE 1 PASSED] 문법 검사 통과")

        # -------------------------------------------------------------
        # Stage 2: 수집기 선택 및 실행 (Log Collection)
        # -------------------------------------------------------------
        entrypoint_cmd = mission_data.get("entrypoint") or mission_data.get("standalone_entrypoint") or f"python {target_file_path}"

        # CLI 프로젝트 판별 조건 및 서브 에이전트 분기
        is_cli_project = (
            mission_data.get("test_type") in ["cli_test", "cli", "interactive_cli"] or
            mission_data.get("is_cli", False) or
            "input(" in target_code
        )

        if is_cli_project:
            execution_steps.append(f"[STAGE 2] 🤖 CliPipelineAgent 서브 에이전트 가동 (명령어: '{entrypoint_cmd}')")
            captured: CapturedLogResult = self.cli_agent.execute_and_collect(
                mission_data=mission_data,
                entrypoint_cmd=entrypoint_cmd,
                target_code=target_code
            )
        else:
            collector = self.collectors.get(spec.channel_type, self.collectors["stdio"])
            execution_steps.append(f"[STAGE 2] {collector.__class__.__name__} 가동 (명령어: '{entrypoint_cmd}')")
            captured: CapturedLogResult = collector.collect(spec, entrypoint_cmd)

        if not captured.success and captured.returncode == -1:
            execution_steps.append(f"[STAGE 2 FAIL] 수집 실패: {captured.error_message}")
            return VerificationResult(
                verified=False,
                failure_type="COLLECTION_ERROR",
                output=captured.raw_logs,
                message=captured.error_message or "로그 수집 중 오류 발생",
                execution_steps=execution_steps,
                missing_patterns=spec.expected_patterns
            ).model_dump()

        # -------------------------------------------------------------
        # Stage 3: 패턴 매칭 & 런타임 예외 트레이스 검증
        # -------------------------------------------------------------
        execution_steps.append("[STAGE 3] 정규식 패턴 대조 및 예외 트레이스 검사")
        raw_logs = captured.raw_logs

        # 1. 런타임 예외 감지
        failure_keywords = ["Traceback (most recent call last):", "SyntaxError:", "ImportError:", "ModuleNotFoundError:", "npm ERR!"]
        has_runtime_error = any(kw in raw_logs for kw in failure_keywords)

        matched_patterns = []
        missing_patterns = []

        if spec.expected_patterns:
            for p in spec.expected_patterns:
                regex_pat = build_log_regex_pattern(p)
                if re.search(regex_pat, raw_logs, re.MULTILINE):
                    matched_patterns.append(p)
                else:
                    missing_patterns.append(p)

        is_verified = (len(spec.expected_patterns) > 0 and len(missing_patterns) == 0 and not has_runtime_error)

        if has_runtime_error:
            failure_type = "RUNTIME_ERROR"
            msg = "[ERROR] Runtime Exception Detected (Traceback/Error captured)"
        elif not is_verified:
            failure_type = "LOG_PATTERN_MISMATCH"
            msg = f"[WARNING] Debug log pattern mismatch (Missing {len(missing_patterns)} patterns: {missing_patterns})"
        else:
            failure_type = "NONE"
            msg = f"[SUCCESS] Debug log & execution verification passed ({len(matched_patterns)}/{len(spec.expected_patterns)} matched)"

        execution_steps.append(f"[FINAL] 검증 결과: {'통과' if is_verified else '실패'} ({failure_type})")

        return VerificationResult(
            verified=is_verified,
            failure_type=failure_type,
            matched_patterns=matched_patterns,
            missing_patterns=missing_patterns,
            output=raw_logs,
            message=msg,
            execution_steps=execution_steps
        ).model_dump()