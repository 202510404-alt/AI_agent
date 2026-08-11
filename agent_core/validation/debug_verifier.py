import os
import re
import sys
import time
import subprocess
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Optional

from tools.multi_agent_system.terminal_runner import TerminalAgentRunner
from tools.multi_agent_system.browser_tester import BrowserTester


def build_log_regex_pattern(template_msg: str) -> str:
    """미션 디버그 로그 메시지의 변수 표기({x}, {hex_code} 등)를 Regex 패턴으로 자동 변환"""
    escaped = re.escape(template_msg)
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*num[a-zA-Z0-9_]*\\\}|\\\{x\\\}|\\\{y\\\}|\\\{val\\\}', r'[-+]?\\d*\\.?\\d+', escaped)
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*bool[a-zA-Z0-9_]*\\\}', r'(?i)(true|false)', escaped)
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*hex[a-zA-Z0-9_]*\\\}', r'#?[a-fA-F0-9]{3,6}', escaped)
    escaped = re.sub(r'\\\{.*?\\\}', r'[\\s\\S]*?', escaped)
    return escaped


def extract_minimal_mission_payload(mission_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    LLM 및 Runner에 전달할 경량화 페이로드 추출 (토큰 절약)
    미션 파일 전체를 들고 다니지 않고 디버깅 로그 스펙, 목표, 최소 스펙만 정제
    """
    blueprint = mission_data.get("implementation_blueprint", {})
    debug_spec = mission_data.get("debug_log_spec", {})
    browser_spec = mission_data.get("browser_test_spec", {})
    
    use_browser = mission_data.get("use_browser_test", False) or (mission_data.get("test_type") == "browser")
    raw_patterns = mission_data.get("expected_terminal_outputs", [])
    if not raw_patterns and debug_spec.get("log_pattern"):
        raw_patterns = [debug_spec["log_pattern"]]

    return {
        "task_id": mission_data.get("task_id", ""),
        "test_type": mission_data.get("test_type", ""),
        "use_browser_test": use_browser,
        "target_file": mission_data.get("target_file", ""),
        "entrypoint": mission_data.get("entrypoint") or mission_data.get("standalone_entrypoint", ""),
        "debug_log_spec": {
            "toggle_key": debug_spec.get("toggle_key") or blueprint.get("debug_toggle_key", ""),
            "log_pattern": debug_spec.get("log_pattern", "")
        },
        "expected_terminal_outputs": raw_patterns,
        "feature_title": blueprint.get("feature_title", ""),
        "browser_test_spec": browser_spec if use_browser else {}
    }


class DebugVerifier:
    """
    터미널 및 브라우저 검증 통합 모듈 (Debug Verifier)
    - 0.1초 Fast-Check 정적 문법 검사
    - 미션 데이터 경량화 추출을 통한 프롬프트 토큰 절감
    - CLI/터미널 실행(TerminalAgentRunner) 및 조건 충족 시 브라우저 러너(BrowserTester/BrowserAgentRunner) 호출
    - 정규식 패턴 matching 및 런타임 에러 자동 진단
    """
    def __init__(self, root_dir: Path, factory: Any = None):
        self.root_dir = Path(root_dir).resolve()
        self.factory = factory

    def verify(
        self,
        mission_data: Dict[str, Any],
        target_file_path: str,
        target_code: str = ""
    ) -> Dict[str, Any]:
        """검증 통합 엔트리포인트"""
        minimal_spec = extract_minimal_mission_payload(mission_data)

        # Step 1: Fast-Check (0.1초 정적 문법 검사)
        fast_check_res = self._run_fast_check(target_file_path)
        if not fast_check_res["success"]:
            return {
                "verified": False,
                "output": fast_check_res["output"],
                "message": fast_check_res["message"]
            }

        # Step 2: 실행 환경변수 구성 (디버그 토글 키 자동 주입)
        exec_env = os.environ.copy()
        exec_env["BROWSER"] = "none"
        toggle_key = minimal_spec["debug_log_spec"]["toggle_key"]
        if toggle_key:
            exec_env[toggle_key] = "true"

        # Step 3: 브라우저 테스트 vs 터미널 테스트 실행 분기
        if minimal_spec["use_browser_test"]:
            return self._run_browser_verification(minimal_spec, exec_env, mission_data)
        else:
            return self._run_terminal_verification(minimal_spec, target_code, exec_env)

    def _run_fast_check(self, target_file_path: str) -> Dict[str, Any]:
        """패치 직후 문법 오류 빠른 포착"""
        full_target = self.root_dir / target_file_path
        if target_file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
            fast_cmd = f"npx --yes esbuild \"{full_target}\" --loader:.js=jsx"
            try:
                res = subprocess.run(
                    fast_cmd, shell=True, capture_output=True, text=True, input="", timeout=10, cwd=str(self.root_dir)
                )
                if res.returncode != 0:
                    return {
                        "success": False,
                        "output": f"[FAST-CHECK SYNTAX ERROR]\n{res.stderr.strip()}",
                        "message": "정적 문법 검사(Fast-Check) 실패"
                    }
            except Exception:
                pass
        return {"success": True, "output": "", "message": "Fast-Check 통과"}

    def _run_browser_verification(
        self,
        minimal_spec: Dict[str, Any],
        exec_env: Dict[str, str],
        full_mission_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """브라우저 러너 및 자율 에이전트 연동 검증"""
        browser_spec = minimal_spec.get("browser_test_spec", {})
        target_url = browser_spec.get("url", "http://localhost:3000")
        
        servers = full_mission_data.get("servers", [
            {"name": "Client", "cwd": ".", "command": minimal_spec["entrypoint"], "health_check_url": target_url}
        ])
        server_procs = []

        try:
            creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            for cfg in servers:
                srv_cwd = (self.root_dir / cfg.get("cwd", ".")).resolve()
                srv_cmd = cfg.get("command")
                srv_url = cfg.get("health_check_url", target_url)

                if not srv_cwd.exists() or not srv_cmd:
                    continue

                proc = subprocess.Popen(
                    srv_cmd, shell=True, cwd=str(srv_cwd), env=exec_env, creationflags=creation_flags
                )
                server_procs.append(proc)

                # 서버 기동 헬스체크 (최대 30초)
                start_time = time.time()
                while time.time() - start_time < 30:
                    if proc.poll() is not None:
                        break
                    try:
                        with urllib.request.urlopen(srv_url, timeout=2) as res:
                            if 200 <= res.status < 500:
                                break
                    except Exception:
                        time.sleep(1)

            # 1차 정적 브라우저 테스트 (BrowserTester)
            tester = BrowserTester(headless=False)
            actions = browser_spec.get("actions", [])
            wait_selector = browser_spec.get("wait_for_selector")
            raw_patterns = minimal_spec["expected_terminal_outputs"]
            regex_patterns = [build_log_regex_pattern(p) for p in raw_patterns]

            b_result = tester.run_browser_verification(
                target_url=target_url,
                actions=actions,
                expected_patterns=regex_patterns,
                wait_for_selector=wait_selector
            )

            # 2차 자율 브라우저 에이전트 Fallback (BrowserAgentRunner)
            if not b_result["success"] and self.factory:
                from tools.multi_agent_system.browser_agent_runner import BrowserAgentRunner
                agent_runner = BrowserAgentRunner(self.factory)
                
                task_title = minimal_spec.get("feature_title") or minimal_spec["task_id"]
                goal = (
                    f"1. Navigate to {target_url}\n"
                    f"2. Objective: Verify feature '{task_title}'.\n"
                    f"3. Interact with target: '{wait_selector}' using actions: {actions}\n"
                    f"4. Trigger log patterns: {raw_patterns}"
                )
                b_result = agent_runner.run_autonomous_loop(
                    target_url=target_url,
                    goal_description=goal,
                    expected_patterns=regex_patterns
                )

            logs = "\n".join(b_result.get("console_logs", []))
            if not b_result["success"]:
                logs += f"\n[BROWSER ERROR] {b_result.get('message', '')}\n" + "\n".join(b_result.get("page_errors", []))

            return {
                "verified": b_result["success"],
                "output": logs,
                "message": b_result.get("message", "")
            }

        finally:
            for proc in server_procs:
                if os.name == 'nt':
                    subprocess.run(f"taskkill /F /T /PID {proc.pid}", shell=True, capture_output=True)
                else:
                    proc.terminate()

    def _run_terminal_verification(
        self,
        minimal_spec: Dict[str, Any],
        target_code: str,
        exec_env: Dict[str, str]
    ) -> Dict[str, Any]:
        """터미널 러너(TerminalAgentRunner) 기반 CLI 검증"""
        entrypoint = minimal_spec["entrypoint"] or f"python3 {minimal_spec['target_file']}"
        runner = TerminalAgentRunner(factory=self.factory, default_timeout=30)

        # 토큰 절감을 위해 미션 파일 전체 대신 경량화된 minimal_spec 전달
        res = runner.execute(
            command=entrypoint,
            goal_context=minimal_spec["task_id"],
            cwd=str(self.root_dir),
            env=exec_env,
            mission_data=minimal_spec,
            code_context=target_code
        )
        terminal_output = res["clean_output"]
        patterns = minimal_spec["expected_terminal_outputs"]

        is_verified = True
        if patterns:
            for p in patterns:
                regex_pat = build_log_regex_pattern(p)
                if not re.search(regex_pat, terminal_output):
                    is_verified = False
                    break
        else:
            is_verified = False

        # 치명적 예외 키워드 감지
        failure_keywords = ["Traceback (most recent call last):", "FAIL ", "npm ERR!", "Command failed"]
        if is_verified and any(kw in terminal_output for kw in failure_keywords):
            is_verified = False

        return {
            "verified": is_verified,
            "output": terminal_output,
            "message": "로그 패턴 및 실행 검증 성공" if is_verified else "터미널 출력 패턴 불일치 또는 런타임 오류"
        }