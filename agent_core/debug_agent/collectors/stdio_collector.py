"""
agent_core/debug_agent/collectors/stdio_collector.py
---------------------------------------------------
CLI / 콘솔 표준 출력(stdout/stderr) 수집기
"""

import os
import sys
import subprocess
from pathlib import Path
from agent_core.debug_agent.schemas import DebugLogSpec, CapturedLogResult
from agent_core.debug_agent.collectors.base import BaseLogCollector


class StdioCollector(BaseLogCollector):
    """
    Subprocess를 사용하여 엔트리포인트 명령어를 실행하고,
    stdout/stderr 스트림을 캡처하는 표준 콘솔 로그 수집기
    """
    def collect(
        self,
        spec: DebugLogSpec,
        entrypoint_cmd: str,
        env: dict = None
    ) -> CapturedLogResult:
        exec_env = os.environ.copy()
        exec_env["PYTHONUNBUFFERED"] = "1"
        exec_env["PYTHONIOENCODING"] = "utf-8"
        if env:
            exec_env.update(env)

        # 디버그 토글 환경변수 주입
        for k, v in spec.env_toggles.items():
            exec_env[k] = str(v)

        timeout = spec.timeout_seconds or 15

        # 윈도우 환경에서 cmd.exe를 거치되 stdin 대기 블로킹 차단
        if isinstance(entrypoint_cmd, str) and os.name == 'nt':
            cmd = f'cmd.exe /c "{entrypoint_cmd}"'
        else:
            cmd = entrypoint_cmd

        try:
            res = subprocess.run(
                cmd,
                shell=False if isinstance(cmd, list) else True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout,
                cwd=str(self.root_dir),
                env=exec_env
            )
            raw_logs = (res.stdout or "") + "\n" + (res.stderr or "")
            return CapturedLogResult(
                success=True,
                channel_type="stdio",
                raw_logs=raw_logs.strip(),
                returncode=res.returncode
            )
        except subprocess.TimeoutExpired as e:
            stdout_str = e.stdout.decode("utf-8", errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
            stderr_str = e.stderr.decode("utf-8", errors="replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
            partial_logs = (stdout_str + "\n" + stderr_str).strip()
            return CapturedLogResult(
                success=False,
                channel_type="stdio",
                raw_logs=partial_logs,
                returncode=-1,
                error_message=f"프로세스 실행 타임아웃 초과 ({timeout}초)"
            )
        except Exception as e:
            return CapturedLogResult(
                success=False,
                channel_type="stdio",
                raw_logs="",
                returncode=-1,
                error_message=f"Stdio 수집 도중 예외 발생: {str(e)}"
            )
