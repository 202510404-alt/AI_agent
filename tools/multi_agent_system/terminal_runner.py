"""
tools/multi_agent_system/terminal_runner.py
AI 에이전트 전용 인터랙티브/데몬 터미널 실행 모듈
"""

import os
import re
import sys
import time
import queue
import select
import threading
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List

import psutil

FORBIDDEN_COMMANDS = ["rm -rf", "rd /s", "format", "mkfs", "dd", ":(){ :|:& };:"]


class ProcessHandle:
    """subprocess.Popen을 감싸 비동기 입출력 및 상태를 관리하는 핸들러 클래스"""
    def __init__(self, proc: subprocess.Popen):
        self.proc = proc
        self._output_queue: queue.Queue = queue.Queue()
        self._stop_event = threading.Event()
        
        # 백그라운드에서 stdout을 읽어 큐에 저장하는 스레드 가동
        self._reader_thread = threading.Thread(target=self._read_stdout_loop, daemon=True)
        self._reader_thread.start()

    def _read_stdout_loop(self):
        if self.proc.stdout:
            while not self._stop_event.is_set():
                line = self.proc.stdout.readline()
                if not line:
                    break
                self._output_queue.put(line)

    @property
    def pid(self) -> int:
        return self.proc.pid

    def read_stdout(self) -> str:
        data = []
        while not self._output_queue.empty():
            try:
                data.append(self._output_queue.get_nowait())
            except queue.Empty:
                break
        return "".join(data)

    def write_stdin(self, text: str):
        if self.proc.stdin and self.is_alive():
            try:
                self.proc.stdin.write(text)
                self.proc.stdin.flush()
            except (IOError, ValueError):
                pass

    def is_alive(self) -> bool:
        return self.proc.poll() is None

    @property
    def exit_code(self) -> Optional[int]:
        return self.proc.returncode

    def close(self):
        self._stop_event.set()
        if self.proc.stdin:
            try:
                self.proc.stdin.close()
            except Exception:
                pass


class TerminalAgentRunner:
    """AI 에이전트 전용 터미널 실행기 엔진"""
    def __init__(self, factory: Any = None, max_retries: int = 3, default_timeout: int = 30):
        self.factory = factory
        self.max_retries = max_retries
        self.default_timeout = default_timeout

    def execute(
        self,
        command: str,
        goal_context: str = "",
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        mission_data: Optional[Dict[str, Any]] = None,
        code_context: Optional[str] = None
    ) -> Dict[str, Any]:
        for forbidden in FORBIDDEN_COMMANDS:
            if forbidden in command.lower():
                return self._build_result(
                    status="FORBIDDEN_ABORT",
                    buffer="",
                    error_msg=f"❌ [보안 거부] 위험 키워드가 포함된 명령어 차단: '{forbidden}'"
                )

        exec_env = os.environ.copy()
        if env:
            exec_env.update(env)

        work_dir = cwd if cwd else str(Path(__file__).parent.parent.parent.resolve())
        mode = self._classify_command(command)

        if mode == "DAEMON":
            return self._run_daemon_mode(command, work_dir, exec_env)
        else:
            return self._run_interactive_loop(
                command=command,
                goal=goal_context,
                cwd=work_dir,
                env=exec_env,
                mode=mode,
                mission_data=mission_data,
                code_context=code_context
            )

    def _classify_command(self, command: str) -> str:
        cmd_lower = command.lower()
        daemon_keywords = ["npm start", "python -m http.server", "uvicorn", "flask run", "gunicorn", "vite", "next dev"]
        if any(dk in cmd_lower for dk in daemon_keywords) or cmd_lower.endswith("&"):
            return "DAEMON"

        interactive_keywords = ["python", "node", "npm init", "pip install", "git clone", "bash", "sh"]
        if any(ik in cmd_lower for ik in interactive_keywords):
            return "INTERACTIVE"

        return "BATCH"

    def _spawn_process(self, command: str, cwd: str, env: Dict[str, str]) -> ProcessHandle:
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        proc = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            cwd=cwd,
            env=env,
            creationflags=creation_flags
        )
        return ProcessHandle(proc)

    def _run_interactive_loop(
        self,
        command: str,
        goal: str,
        cwd: str,
        env: Dict[str, str],
        mode: str,
        mission_data: Optional[Dict[str, Any]] = None,
        code_context: Optional[str] = None
    ) -> Dict[str, Any]:
        proc_handle = self._spawn_process(command, cwd, env)
        buffer = ""
        start_time = time.time()

        try:
            while True:
                time.sleep(0.1)

                if time.time() - start_time > self.default_timeout:
                    self._kill_process_tree(proc_handle.pid)
                    return self._build_result(
                        status="TIMEOUT",
                        buffer=buffer,
                        error_msg=f"⏰ [타임아웃] 지정된 실행 시간({self.default_timeout}초) 초과"
                    )

                new_data = proc_handle.read_stdout()
                if new_data:
                    buffer += new_data
                    start_time = time.time()

                if not proc_handle.is_alive():
                    buffer += proc_handle.read_stdout()
                    status = "SUCCESS" if proc_handle.exit_code == 0 else "FAILED"
                    return self._build_result(
                        status=status,
                        buffer=buffer,
                        exit_code=proc_handle.exit_code
                    )

                if self._is_kernel_waiting_stdin(proc_handle.pid):
                    response = self._resolve_input(buffer, goal, mission_data, code_context)
                    if response is None:
                        self._kill_process_tree(proc_handle.pid)
                        return self._build_result(
                            status="SECURITY_ABORT",
                            buffer=buffer,
                            error_msg="🚨 보안 가드레일 작동으로 프로세스 종료"
                        )
                    proc_handle.write_stdin(response + "\n")
                    buffer += f"\n[Agent Input Inject]: {response}\n"
                    start_time = time.time()
        finally:
            proc_handle.close()

    def _run_daemon_mode(self, command: str, cwd: str, env: Dict[str, str]) -> Dict[str, Any]:
        try:
            creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            proc = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                cwd=cwd,
                env=env,
                creationflags=creation_flags
            )
            time.sleep(2)
            if proc.poll() is not None:
                out, _ = proc.communicate()
                return self._build_result("DAEMON_FAILED", out, exit_code=proc.returncode, error_msg="데몬 구동 실패")
            return self._build_result("DAEMON_RUNNING", f"🚀 백그라운드 데몬 서버 실행 완료 (PID: {proc.pid})")
        except Exception as e:
            return self._build_result("DAEMON_ERROR", "", error_msg=str(e))

    def _is_kernel_waiting_stdin(self, pid: int) -> bool:
        try:
            proc = psutil.Process(pid)
            if proc.status() == psutil.STATUS_WAITING:
                return True
        except Exception:
            pass
        return False

    def _resolve_input(self, current_buffer: str, goal: str, mission_data: Optional[Dict[str, Any]], code_context: Optional[str]) -> Optional[str]:
        buffer_lower = current_buffer.lower()
        if any(sp in buffer_lower for sp in ["password:", "confirm delete"]):
            return None
        if "[y/n]" in buffer_lower or "(y/n)" in buffer_lower:
            return "y"
        return "y"

    def _kill_process_tree(self, pid: int):
        try:
            parent = psutil.Process(pid)
            for child in parent.children(recursive=True):
                try:
                    child.kill()
                except psutil.NoSuchProcess:
                    pass
            parent.kill()
        except Exception:
            if os.name == 'nt':
                subprocess.run(f"taskkill /F /T /PID {pid}", shell=True, capture_output=True)

    def _build_result(self, status: str, buffer: str, exit_code: Optional[int] = None, error_msg: str = "", debug_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        clean_buffer = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', buffer)
        return {
            "status": status,
            "exit_code": exit_code,
            "raw_output": buffer,
            "clean_output": clean_buffer,
            "error_msg": error_msg,
            "debug_payload": debug_payload
        }


def run_terminal_command(command: str, cwd: str = None, timeout: int = 30, env: dict = None) -> str:
    """기존 함수 시그니처 하위 호환 래퍼"""
    runner = TerminalAgentRunner(default_timeout=timeout)
    res = runner.execute(command=command, cwd=cwd, env=env)
    
    if res["status"] in ["SUCCESS", "DAEMON_RUNNING"]:
        return f"✅ 실행 성공\n\n{res['clean_output']}"
    else:
        err = res.get("error_msg") or res.get("clean_output")
        return f"⚠️ 실행 종료 ({res['status']})\n\n{err}"