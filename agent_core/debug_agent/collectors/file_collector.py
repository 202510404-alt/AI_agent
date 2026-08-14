"""
agent_core/debug_agent/collectors/file_collector.py
--------------------------------------------------
파일 기반 (.log, .txt) 디버그 로그 수집기
"""

import os
import subprocess
from pathlib import Path
from agent_core.debug_agent.schemas import DebugLogSpec, CapturedLogResult
from agent_core.debug_agent.collectors.base import BaseLogCollector


class FileCollector(BaseLogCollector):
    """
    명령어를 실행하거나 지정된 log_file_path 파일을 읽어들여
    디버그 텍스트 로그를 수집하는 수집기
    """
    def collect(
        self,
        spec: DebugLogSpec,
        entrypoint_cmd: str = None,
        env: dict = None
    ) -> CapturedLogResult:
        if not spec.log_file_path:
            return CapturedLogResult(
                success=False,
                channel_type="file",
                raw_logs="",
                error_message="log_file_path 가 지정되지 않았습니다."
            )

        log_path = self.root_dir / spec.log_file_path
        
        # 엔트리포인트 명령어가 명시적으로 주어졌고, 대상 파일이 없는 경우에만 1회 실행
        if entrypoint_cmd and not log_path.exists():
            exec_env = os.environ.copy()
            if env:
                exec_env.update(env)
            for k, v in spec.env_toggles.items():
                exec_env[k] = str(v)

            cmd = f'cmd.exe /c "{entrypoint_cmd}"' if (isinstance(entrypoint_cmd, str) and os.name == 'nt') else entrypoint_cmd

            try:
                subprocess.run(
                    cmd,
                    shell=False if isinstance(cmd, list) else True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=spec.timeout_seconds or 15,
                    cwd=str(self.root_dir),
                    env=exec_env
                )
            except Exception:
                pass

        # 파일 존재 및 내용 수집
        if not log_path.exists():
            return CapturedLogResult(
                success=False,
                channel_type="file",
                raw_logs="",
                error_message=f"지정된 로그 파일을 찾을 수 없습니다: {spec.log_file_path}"
            )

        try:
            with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            return CapturedLogResult(
                success=True,
                channel_type="file",
                raw_logs=content.strip(),
                returncode=0
            )
        except Exception as e:
            return CapturedLogResult(
                success=False,
                channel_type="file",
                raw_logs="",
                error_message=f"로그 파일 읽기 실패 ({spec.log_file_path}): {str(e)}"
            )
