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


# 보안상 실행을 즉시 차단할 위험 명령어 목록
FORBIDDEN_COMMANDS = ["rm -rf", "rd /s", "format", "mkfs", "dd", ":(){ :|:& };:"]


class ProcessHandle:
    """
    Subprocess를 비동기/Non-blocking 방식으로 모니터링하고 
    stdout/stderr 수집 및 stdin 주입을 담당하는 래퍼 클래스
    """
    def __init__(self, proc: subprocess.Popen):
        self.proc = proc
        self.pid = proc.pid
        self._output_queue = queue.Queue()
        self._stop_event = threading.Event()
        self.last_output_time = time.time()  # 마지막 출력 시간 타임스탬프 추가

        # 비동기 stdout/stderr 수집 스레드 시작
        self._stdout_thread = threading.Thread(target=self._reader_thread, args=(self.proc.stdout,), daemon=True)
        self._stderr_thread = threading.Thread(target=self._reader_thread, args=(self.proc.stderr,), daemon=True)
        self._stdout_thread.start()
        self._stderr_thread.start()

    def _reader_thread(self, stream):
        """스트림에서 실시간으로 텍스트를 읽어 큐에 적재"""
        try:
            for line in iter(stream.readline, ''):
                if line:
                    self._output_queue.put(line)
                    self.last_output_time = time.time()  # 출력 발생 시 타임스탬프 갱신
                if self._stop_event.is_set():
                    break
        except Exception:
            pass
        finally:
            stream.close()

    def read_stdout(self) -> str:
        """큐에 쌓인 새로운 출력을 비동기로 모두 읽어옴"""
        data = []
        while not self._output_queue.empty():
            try:
                data.append(self._output_queue.get_nowait())
            except queue.Empty:
                break
        return "".join(data)

    def write_stdin(self, text: str):
        """프로세스의 stdin으로 대답 주입"""
        if self.proc.stdin and self.is_alive():
            try:
                self.proc.stdin.write(text)
                self.proc.stdin.flush()
            except (IOError, ValueError):
                pass

    def is_alive(self) -> bool:
        """프로세스 생존 여부 확인"""
        return self.proc.poll() is None

    @property
    def exit_code(self) -> Optional[int]:
        return self.proc.returncode

    def close(self):
        self._stop_event.set()


class TerminalAgentRunner:
    """
    AI 에이전트 전용 터미널 실행기
    - 모드 자동 분류 (BATCH / INTERACTIVE / DAEMON)
    - OS 커널 레벨 input() 감지 & 3단계 동적 대답 주입
    - LLM 디버깅용 Minimal Context Payload 자동 생성
    - 안전성 확보 (위험 명령어 차단, 프로세스 트리 완벽 cleanup)
    """

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
        """
        터미널 명령어 안전 실행 엔트리포인트
        """
        # 0. 보안 검사
        for forbidden in FORBIDDEN_COMMANDS:
            if forbidden in command.lower():
                return self._build_result(
                    status="FORBIDDEN_ABORT",
                    buffer="",
                    error_msg=f"❌ [보안 거부] 위험 키워드가 포함된 명령어 차단: '{forbidden}'"
                )

        # 환경변수 기본 세팅
        exec_env = os.environ.copy()
        if env:
            exec_env.update(env)

        # 작업 디렉토리 설정
        work_dir = cwd if cwd else os.getcwd()

        # 1. 실행 모드 자동 분류
        mode = self._classify_command(command)

        # 2. 모드별 실행 분기
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
        """명령어 패턴을 분석하여 실행 모드 분류"""
        cmd_lower = command.lower()

        # 백그라운드 서버/데몬 모드
        daemon_keywords = ["npm start", "python -m http.server", "uvicorn", "flask run", "gunicorn", "vite", "next dev"]
        if any(dk in cmd_lower for dk in daemon_keywords) or cmd_lower.endswith("&"):
            return "DAEMON"

        # 대화형 CLI 모드 (추가 확장이 가능한 인터랙티브 명령어)
        interactive_keywords = ["python", "node", "npm init", "pip install", "git clone", "bash", "sh"]
        if any(ik in cmd_lower for ik in interactive_keywords):
            return "INTERACTIVE"

        return "BATCH"

    def _spawn_process(self, command: str, cwd: str, env: Dict[str, str]) -> ProcessHandle:
        """하위 프로세스를 생성하고 ProcessHandle로 래핑"""
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        
        proc = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # stderr를 stdout으로 병합 수집
            stdin=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,  # Line buffered
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
        """
        PTY/Subprocess 기반 실시간 모니터링 & 자율 입력 루프
        """
        proc_handle = self._spawn_process(command, cwd, env)
        buffer = ""
        start_time = time.time()

        try:
            while True:
                time.sleep(0.1)  # CPU 점유율 방지

                # A. 타임아웃 검사
                if time.time() - start_time > self.default_timeout:
                    self._kill_process_tree(proc_handle.pid)
                    return self._build_result(
                        status="TIMEOUT",
                        buffer=buffer,
                        error_msg=f"⏰ [타임아웃] 지정된 실행 시간({self.default_timeout}초) 초과",
                        debug_payload=self._build_llm_debug_payload(
                            goal, command, cwd, env, "TIMEOUT", buffer, mission_data, code_context
                        )
                    )

                # B. 실시간 출력 수집
                new_data = proc_handle.read_stdout()
                if new_data:
                    buffer += new_data
                    start_time = time.time()  # 출력이 발생하면 타임아웃 타이머 리셋

                # C. 프로세스 정상/오류 종료 완료 여부 확인
                if not proc_handle.is_alive():
                    # 남아있는 출력 최종 긁어오기
                    buffer += proc_handle.read_stdout()
                    status = "SUCCESS" if proc_handle.exit_code == 0 else "FAILED"
                    return self._build_result(
                        status=status,
                        buffer=buffer,
                        exit_code=proc_handle.exit_code,
                        debug_payload=self._build_llm_debug_payload(
                            goal, command, cwd, env, status, buffer, mission_data, code_context
                        )
                    )

                # D. Quiet Period + Tail Pattern 기반 실시간 입력 대기 감지 및 동적 응답 주입
                if self._is_waiting_for_input(proc_handle, buffer):
                    response = self._resolve_input(
                        current_buffer=buffer,
                        goal=goal,
                        mission_data=mission_data,
                        code_context=code_context
                    )
                    
                    if response is None:
                        # 보안 경보 또는 대답 불가 시 프로세스 안전 차단
                        self._kill_process_tree(proc_handle.pid)
                        return self._build_result(
                            status="SECURITY_ABORT",
                            buffer=buffer,
                            error_msg="🚨 보안 가드레일 작동 또는 대답 불가로 인한 프로세스 안전 종료"
                        )

                    # 대답 주입
                    proc_handle.write_stdin(response + "\n")
                    buffer += f"\n[Agent Input Inject]: {response}\n"
                    start_time = time.time()

        finally:
            proc_handle.close()

    def _run_daemon_mode(self, command: str, cwd: str, env: Dict[str, str]) -> Dict[str, Any]:
        """데몬/서버 프로세스 실행 모드"""
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
            time.sleep(2)  # 서버 기동 초기 로그 수집 대기

            if proc.poll() is not None:
                # 2초 만에 즉시 종료된 경우 (실패)
                out, _ = proc.communicate()
                return self._build_result("DAEMON_FAILED", out, exit_code=proc.returncode, error_msg="데몬 서버 구동 실패")

            return self._build_result("DAEMON_RUNNING", f"🚀 백그라운드 데몬 서버 실행 완료 (PID: {proc.pid})")
        except Exception as e:
            return self._build_result("DAEMON_ERROR", "", error_msg=str(e))

    def _is_waiting_for_input(self, proc_handle: ProcessHandle, buffer: str, quiet_time_sec: float = 0.3) -> bool:
        """
        Quiet Period(출력 정지 시간) + Tail Pattern(프롬프트 패턴) 기반 감지
        """
        if not proc_handle.is_alive():
            return False

        # 1. Quiet Period 검사: 지정된 시간(0.3초) 동안 아무 출력이 없었는지 확인
        if time.time() - proc_handle.last_output_time < quiet_time_sec:
            return False

        # 2. Tail Pattern 검사: 버퍼의 마지막 줄이 입력 유도 패턴으로 끝나는지 확인
        clean_tail = buffer.strip().splitlines()[-1] if buffer.strip() else ""
        interactive_indicators = [">", ":", "?", "Turn:", "Enter", "input", "[y/n]"]

        return any(clean_tail.endswith(ind) or ind in clean_tail for ind in interactive_indicators)

    def _resolve_input(
        self,
        current_buffer: str,
        goal: str,
        mission_data: Optional[Dict[str, Any]] = None,
        code_context: Optional[str] = None
    ) -> Optional[str]:
        """
        3단계 자율 대답 판단 레이어 (Regex -> Security Guardrail -> LLM)
        """
        buffer_lower = current_buffer.lower()

        # Tier 1: Regex 단순 질문 패스트트랙
        if "[y/n]" in buffer_lower or "(y/n)" in buffer_lower or "proceed? [y/n]" in buffer_lower:
            return "y"

        # Tier 3: 보안 가드레일 (비밀번호 입력, 강제 삭제 확인 등 위험 동작 중단)
        security_patterns = ["password:", "sudo password", "confirm delete", "are you sure you want to delete"]
        if any(sp in buffer_lower for sp in security_patterns):
            return None  # 중단 요청

        # Tier 2: LLM Context 기반 동적 판단
        return self._call_fast_llm_decision(current_buffer, goal, mission_data, code_context)

    def _call_fast_llm_decision(
        self,
        current_buffer: str,
        goal: str,
        mission_data: Optional[Dict[str, Any]],
        code_context: Optional[str]
    ) -> str:
        """LLM을 호출하여 인터랙티브 대약 프롬프트에 입력할 최적의 응답 문자열 도출"""
        if not self.factory:
            return "y"  # LLM 팩토리가 없을 경우 Fallback 기본값

        prompt = f"""[INTERACTIVE TERMINAL PROMPT DETECTED]
Goal: {goal}
Mission Spec: {mission_data.get('task_id') if mission_data else 'N/A'}
Terminal Output Buffer Tail:
{current_buffer[-1000:]}

Provide ONLY the single-line input string to answer the terminal prompt. No commentary."""

        try:
            response = self.factory.execute_worker_step(
                prompt=prompt,
                system_instruction="STRICT PROTOCOL: Output the raw single-line response string only.",
                response_mime_type="text/plain"
            )
            return response.strip()
        except Exception:
            return "y"

    def _build_llm_debug_payload(
        self,
        goal: str,
        command: str,
        cwd: str,
        env: Dict[str, str],
        trigger: str,
        buffer: str,
        mission_data: Optional[Dict[str, Any]] = None,
        code_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """LLM 디버깅을 위한 5대 핵심 전달 데이터(Minimal Context Payload) 조립"""
        # ANSI 색상 제어 코드 제거
        clean_buffer = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', buffer)
        
        # 최근 100줄 / 마지막 3KB 로그만 추출 (Tail)
        log_lines = clean_buffer.splitlines()
        log_tail = "\n".join(log_lines[-100:])

        return {
            "task_goal": goal,
            "mission_spec": mission_data,
            "command_info": {
                "command": command,
                "cwd": cwd,
                "debug_env_toggles": {k: v for k, v in env.items() if "DEBUG" in k or "LOG" in k}
            },
            "execution_status": {
                "trigger": trigger,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "cleaned_log_tail": log_tail,
            "code_context_slice": code_context if code_context else "N/A"
        }

    def _kill_process_tree(self, pid: int):
        """하위 프로세스를 포함한 전체 프로세스 트리 강제 종료 (좀비 방지)"""
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.kill()
                except psutil.NoSuchProcess:
                    pass
            parent.kill()
        except psutil.NoSuchProcess:
            pass
        except Exception as e:
            # OS별 명령어로 보완 강제 종료
            if os.name == 'nt':
                subprocess.run(f"taskkill /F /T /PID {pid}", shell=True, capture_output=True)
            else:
                subprocess.run(f"kill -9 {pid}", shell=True, capture_output=True)

    def _build_result(
        self,
        status: str,
        buffer: str,
        exit_code: Optional[int] = None,
        error_msg: str = "",
        debug_payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """결과 표준화 dictionary 생성"""
        clean_buffer = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', buffer)
        return {
            "status": status,
            "exit_code": exit_code,
            "raw_output": buffer,
            "clean_output": clean_buffer,
            "error_msg": error_msg,
            "debug_payload": debug_payload
        }