"""
agent_core/execution/standalone_runner.py
Phase 12: 디버깅 로그 예측-검증 파이프라인 (Predictive Debug-Log Verification)
- Planner가 예측한 출력 패턴과 실제 단독 실행 출력을 대조 검증
- 전체 파이프라인 기동 없이 파일/함수 단위 격리 단독 실행
"""

import os
import re
import sys
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional

from agent_core.plan.schemas import Task, ExecutionResult, DebugLogSpec, LOG_FILE_PATH, DEBUG_MODE


class StandaloneExecutionValidator(ABC):
    @abstractmethod
    def run_standalone(self, task: Task, entrypoint_cmd: Optional[str] = None, timeout_sec: int = 10) -> ExecutionResult:
        """
        task.target_files 또는 지정된 entrypoint_cmd를 격리된 subprocess에서 실행합니다.
        timeout_sec 초과 시 강제 종료됩니다.
        """
        raise NotImplementedError

    @abstractmethod
    def match_predicted_output(self, result: ExecutionResult, task: Task) -> Tuple[bool, List[str]]:
        """
        task.debug_spec에 적힌 예측 출력 패턴을 result.output_log에서 정규식으로 매칭 대조합니다.
        반환: (전부 매칭 성공 여부, 매칭 실패한 패턴 목록)
        """
        raise NotImplementedError


class LocalStandaloneExecutionValidator(StandaloneExecutionValidator):
    def __init__(self, root_dir: Optional[Path] = None):
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent.parent.parent
        self.root_dir = Path(root_dir).resolve()

    def run_standalone(self, task: Task, entrypoint_cmd: Optional[str] = None, timeout_sec: int = 10) -> ExecutionResult:
        if entrypoint_cmd:
            cmd = entrypoint_cmd
        elif task.target_files:
            main_target = task.target_files[0]
            cmd = f"{sys.executable} {main_target}"
        else:
            return ExecutionResult(
                task_id=task.task_id,
                success=False,
                output_log="",
                error_message="실행할 대상 파일 또는 진입점 명령어가 지정되지 않았습니다."
            )

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUNBUFFERED"] = "1"
        env["ASE_DEBUG"] = "1"

        try:
            res = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_sec,
                cwd=str(self.root_dir),
                env=env
            )

            combined_output = f"[STDOUT]\n{res.stdout}\n[STDERR]\n{res.stderr}"
            success = (res.returncode == 0)

            return ExecutionResult(
                task_id=task.task_id,
                success=success,
                output_log=combined_output,
                error_message=None if success else f"Return code: {res.returncode}"
            )

        except subprocess.TimeoutExpired as e:
            stdout = e.stdout.decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
            stderr = e.stderr.decode("utf-8", errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
            return ExecutionResult(
                task_id=task.task_id,
                success=False,
                output_log=f"[TIMEOUT EXPIRED ({timeout_sec}s)]\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}",
                error_message=f"단독 실행 시간 초과 ({timeout_sec}초)"
            )
        except Exception as e:
            return ExecutionResult(
                task_id=task.task_id,
                success=False,
                output_log="",
                error_message=f"단독 실행 예외 발생: {str(e)}"
            )

    def match_predicted_output(self, result: ExecutionResult, task: Task) -> Tuple[bool, List[str]]:
        if not task.debug_spec or not task.debug_spec.expected_logs:
            # 디버그 명세가 없는 경우 출력이 정상 캡처되었으면 통과
            return (result.success, [])

        unmatched_patterns: List[str] = []
        output_text = result.output_log

        for pattern in task.debug_spec.expected_logs:
            # 변수 템플릿 {x}, {val} 등을 정규식 패턴으로 자동 치환
            regex_pat = self._build_regex(pattern)
            if not re.search(regex_pat, output_text, re.MULTILINE):
                unmatched_patterns.append(pattern)

        all_matched = (len(unmatched_patterns) == 0)
        return (all_matched, unmatched_patterns)

    def _build_regex(self, template: str) -> str:
        escaped = re.escape(template)
        escaped = re.sub(r'\\\{[a-zA-Z0-9_]*num[a-zA-Z0-9_]*\\\}|\\\{x\\\}|\\\{y\\\}|\\\{val\\\}', r'[-+]?\\d*\\.?\\d+', escaped)
        escaped = re.sub(r'\\\{[a-zA-Z0-9_]*bool[a-zA-Z0-9_]*\\\}', r'(?i)(true|false)', escaped)
        escaped = re.sub(r'\\\{[a-zA-Z0-9_]*hex[a-zA-Z0-9_]*\\\}', r'#?[a-fA-F0-9]{3,6}', escaped)
        escaped = re.sub(r'\\\{.*?\\\}', r'[\\s\\S]*?', escaped)
        return escaped


DefaultStandaloneExecutionValidator = LocalStandaloneExecutionValidator
