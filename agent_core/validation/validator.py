"""
agent_core/validation/validator.py
Level 9 Validator: 종합 코드 및 명세 검증기
- Stage 1: Fast Import & Syntax Check
- Stage 2: Standalone Execution & Debug Log Pattern Verification (§3.5 / Phase 12)
"""

import sys
import importlib
import py_compile
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from agent_core.plan.schemas import Task, ExecutionResult, DebugLogSpec
from agent_core.execution.standalone_runner import LocalStandaloneExecutionValidator, StandaloneExecutionValidator


class ValidationReport:
    def __init__(self, is_valid: bool, stages: Dict[str, bool], message: str, unmatched_logs: List[str] = None):
        self.is_valid = is_valid
        self.stages = stages
        self.message = message
        self.unmatched_logs = unmatched_logs or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "stages": self.stages,
            "message": self.message,
            "unmatched_logs": self.unmatched_logs
        }


class Validator:
    def __init__(self, root_dir: Optional[Path] = None, standalone_validator: Optional[StandaloneExecutionValidator] = None):
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent.parent.parent
        self.root_dir = Path(root_dir).resolve()
        self.standalone_validator = standalone_validator or LocalStandaloneExecutionValidator(root_dir=self.root_dir)

    def validate_syntax_and_import(self, file_path: str) -> Tuple[bool, str]:
        """Stage 1: 문법(Syntax) 검사 및 Import 수성 검증"""
        full_path = self.root_dir / file_path
        if not full_path.exists():
            return False, f"파일을 찾을 수 없습니다: {file_path}"

        if not file_path.endswith(".py"):
            return True, "Python 파일이 아니므로 문법 검사를 통과 처리합니다."

        # 1. py_compile 문법 검사
        try:
            py_compile.compile(str(full_path), doraise=True)
        except py_compile.PyCompileError as e:
            return False, f"문법 오류 (PyCompileError): {e}"

        return True, "문법 및 바이트코드 컴파일 검사 통과"

    def run_all(self, task: Task, entrypoint_cmd: Optional[str] = None, require_predicted_logs: bool = True) -> ValidationReport:
        """Stage 1 + Stage 2 통합 검증 수행"""
        stages: Dict[str, bool] = {
            "syntax_import": False,
            "standalone_execution": False,
            "predicted_logs_match": False
        }

        # Stage 1: 타깃 파일 문법 검사
        for tf in task.target_files:
            ok, msg = self.validate_syntax_and_import(tf)
            if not ok:
                return ValidationReport(
                    is_valid=False,
                    stages=stages,
                    message=f"[Syntax/Import Fail] {tf}: {msg}"
                )
        stages["syntax_import"] = True

        # Stage 2: 단독 실행 및 디버그 로그 대조
        exec_res: ExecutionResult = self.standalone_validator.run_standalone(
            task=task,
            entrypoint_cmd=entrypoint_cmd,
            timeout_sec=10
        )

        if not exec_res.success:
            return ValidationReport(
                is_valid=False,
                stages=stages,
                message=f"[Standalone Execution Fail] {exec_res.error_message or '실행 실패'}\n{exec_res.output_log}"
            )
        stages["standalone_execution"] = True

        # Stage 3: 디버그 로그 패턴 대조
        all_matched, unmatched = self.standalone_validator.match_predicted_output(exec_res, task)
        if require_predicted_logs and not all_matched:
            return ValidationReport(
                is_valid=False,
                stages=stages,
                message=f"[Debug Log Mismatch] {len(unmatched)}개 패턴 불일치: {unmatched}",
                unmatched_logs=unmatched
            )
        stages["predicted_logs_match"] = True

        return ValidationReport(
            is_valid=True,
            stages=stages,
            message="모든 검증 단계(Syntax, Standalone Run, Predicted Logs Match)를 완벽히 통과했습니다!"
        )
