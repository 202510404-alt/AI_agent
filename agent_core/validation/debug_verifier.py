"""
agent_core/validation/debug_verifier.py
고도화 자율 디버깅 로그 검증기 (Autonomous Debug Verifier Pipeline v2.0)
-------------------------------------------------------------------------
[설계 제약조건 & 원칙]
1. 토큰 절약 (Token Optimization): 최소 페이로드(Minimal Spec) 및 필요 텍스트만 슬라이싱하여 LLM에 전달.
2. 무상태(Stateless) & 0-Temperature JSON 스키마 강제: 기억력 미의존, 0도 온도, application/json 타입 응답 강제.
3. 체계화된 파이프라인 구조 (Pipeline Architecture):
   Stage 1: Fast-Check (0.1초 정적 문법 검사)
   Stage 2: 환경변수 이중 주입 (1 및 true 호환성 보장)
   Stage 3: CLI 대화형 자동 입력 주입 & 터미널/브라우저 이중 트랙 실행
   Stage 4: 다중 패턴 정규식 자동 대조 & 예외 트레이스 감지
   Stage 5: 파이프라인 구조화 결과 리포팅 (run_test.py 연동)
"""

import os
import re
import sys
import time
import subprocess
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field

from tools.multi_agent_system.terminal_runner import TerminalAgentRunner
from tools.multi_agent_system.browser_tester import BrowserTester


class VerificationDecisionSchema(BaseModel):
    """LLM 대화형 입력 결정 시 사용하는 Pydantic 스키마 (Temperature 0.0)"""
    is_verified: bool = Field(description="디버그 로그 패턴이 정상 출력되었는지 여부")
    suggested_stdin_input: Optional[str] = Field(default=None, description="대화형 CLI에 주입할 다음 입력 (예: 'go', 'quit')")
    reason: str = Field(description="판단 사유 요약")



class SemanticJudgeSchema(BaseModel):
    """정규식 패턴 불일치 시 작동하는 LLM 의미론적 2차 판정 스키마"""
    is_log_present: bool = Field(description="단순 포맷/공백/대소문자 차이를 제외하고 기대하는 디버그 정보가 터미널에 실질적으로 출력되었는지 여부")
    reason: str = Field(description="판단 사유 요약")


class VerificationDiagnosisSchema(BaseModel):
    """검증 실패 시 메인 루프/엔트리포인트를 읽고 원인을 자율 진단하는 자율 검증 에이전트 스키마"""
    root_cause: str = Field(description="실패 근본 원인 (예: CLI 대기 교착, 메인 루프 호출 누락 등)")
    recommended_action: str = Field(description="패치 일꾼 및 실행기에게 전달할 구체적 개선 힌트")
    suggested_stdin_input: Optional[str] = Field(default=None, description="시도해볼 CLI 입력 명령어 (예: 'go')")


def build_log_regex_pattern(template_msg: str) -> str:
    """미션 디버그 로그 메시지의 변수 표기({x}, {val}, {eval_score} 등)를 Regex 유연 패턴으로 자동 변환"""
    escaped = re.escape(template_msg)
    # 수치형 변수 (정수, 실수, 음수)
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*num[a-zA-Z0-9_]*\\\}|\\\{x\\\}|\\\{y\\\}|\\\{val\\\}|\\\{eval_score\\\}|\\\{nps_count\\\}', r'[-+]?\\d*\\.?\\d+', escaped)
    # 불리언형 변수 (true/false, 1/0)
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*bool[a-zA-Z0-9_]*\\\}', r'(?i)(true|false|1|0)', escaped)
    # Hex/Color 변수
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*hex[a-zA-Z0-9_]*\\\}', r'#?[a-fA-F0-9]{3,6}', escaped)
    # 기타 일반 변수
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

    # 대화형 CLI 입력을 위한 기본 트리거 키워드 수집 (예: ["go", "quit"])
    interactive_inputs = mission_data.get("interactive_inputs", ["go", "quit"])

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
        "interactive_inputs": interactive_inputs,
        "feature_title": blueprint.get("feature_title", ""),
        "browser_test_spec": browser_spec if use_browser else {}
    }


class DebugVerifier:
    """
    고도화 자율 디버깅 로그 검증 오케스트레이터 (Debug Verifier v2.0)
    - 0.1초 Fast-Check 정적 문법 검사
    - 환경변수 이중 주입 ("1" 및 "true" 완전 호환)
    - CLI 대화형 자동 입력 주입 & 터미널/브라우저 이중 트랙 검증
    - 정규식 패턴 matching & 예외 트레이스 자동 감지
    - 무상태 0-Temperature JSON 스키마 강제
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
        """
        통합 파이프라인 검증 진입점 (추적 로그 및 명확한 failure_type 포함)
        """
        execution_steps = []
        minimal_spec = extract_minimal_mission_payload(mission_data)
        execution_steps.append(f"[STAGE 0] Minimal Spec 페이로드 정제 완료 (Task ID: {minimal_spec['task_id']})")

        # -------------------------------------------------------------
        # Stage 1: Fast-Check (0.1초 정적 문법 검사)
        # -------------------------------------------------------------
        execution_steps.append(f"[STAGE 1] Fast-Check 문법 검사 수행 중: {target_file_path}")
        fast_check_res = self._run_fast_check(target_file_path)
        if not fast_check_res["success"]:
            execution_steps.append(f"[STAGE 1 FAIL] 문법 검사 실패: {fast_check_res.get('failure_type', 'FAST_CHECK_ERROR')}")
            return {
                "verified": False,
                "failure_type": fast_check_res.get("failure_type", "FAST_CHECK_ERROR"),
                "output": fast_check_res["output"],
                "message": fast_check_res["message"],
                "execution_steps": execution_steps,
                "matched_patterns": [],
                "missing_patterns": minimal_spec["expected_terminal_outputs"]
            }
        execution_steps.append("[STAGE 1 PASSED] 문법 검사 성공")

        # -------------------------------------------------------------
        # Stage 2: 환경변수 구성 (1 및 true 이중 호환 주입)
        # -------------------------------------------------------------
        exec_env = os.environ.copy()
        exec_env["BROWSER"] = "none"
        exec_env["PYTHONUNBUFFERED"] = "1"
        exec_env["PYTHONIOENCODING"] = "utf-8"

        toggle_key = minimal_spec["debug_log_spec"]["toggle_key"]
        if toggle_key:
            exec_env[toggle_key] = "1"
            exec_env[f"{toggle_key}_ENABLE"] = "true"
            execution_steps.append(f"[STAGE 2] 디버그 환경변수 이중 주입 완료 ({toggle_key}=1, {toggle_key}_ENABLE=true)")
        else:
            execution_steps.append("[STAGE 2] 디버그 토글 키 없음, 기본 환경변수로 진행")

        # -------------------------------------------------------------
        # Stage 3 & 4: 브라우저 테스트 vs 터미널 테스트 파이프라인 실행
        # -------------------------------------------------------------
        if minimal_spec["use_browser_test"]:
            execution_steps.append("[STAGE 3] 브라우저 E2E 검증 트랙진입")
            result = self._run_browser_verification(minimal_spec, exec_env, mission_data)
        else:
            execution_steps.append("[STAGE 3] 터미널 CLI 검증 트랙 진입")
            result = self._run_terminal_verification(minimal_spec, target_code, exec_env)

        result["execution_steps"] = execution_steps
        return result

    def _run_fast_check(self, target_file_path: str) -> Dict[str, Any]:
        """Stage 1: 패치 직후 문법 오류 빠른 포착"""
        full_target = self.root_dir / target_file_path
        if not full_target.exists():
            return {
                "success": False,
                "failure_type": "FILE_NOT_FOUND",
                "output": f"[FILE NOT FOUND] 대상 파일을 찾을 수 없습니다: {target_file_path}",
                "message": "대상 파일 부재"
            }

        if target_file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
            fast_cmd = f"npx --yes esbuild \"{full_target}\" --loader:.js=jsx"
            try:
                res = subprocess.run(
                    fast_cmd, shell=True, capture_output=True, text=True, input="", timeout=10, cwd=str(self.root_dir)
                )
                if res.returncode != 0:
                    return {
                        "success": False,
                        "failure_type": "FAST_CHECK_SYNTAX_ERROR",
                        "output": f"[FAST-CHECK SYNTAX ERROR]\n{res.stderr.strip()}",
                        "message": "정적 문법 검사(Fast-Check) 실패"
                    }
            except Exception:
                pass
        elif target_file_path.endswith('.py'):
            import py_compile
            try:
                py_compile.compile(str(full_target), doraise=True)
            except py_compile.PyCompileError as e:
                return {
                    "success": False,
                    "failure_type": "FAST_CHECK_SYNTAX_ERROR",
                    "output": f"[PYTHON SYNTAX ERROR]\n{e}",
                    "message": "파이썬 문법 검사(py_compile) 실패"
                }

        return {"success": True, "output": "", "message": "Fast-Check 통과"}

    def _get_interactive_decision(
        self,
        terminal_output: str,
        missing_patterns: List[str],
        interactive_inputs: List[str]
    ) -> Optional[VerificationDecisionSchema]:
        """LLM을 호출하여 CLI 대화형 입력(suggested_stdin_input) 결정 (Temperature 0.0)"""
        if not self.factory or not hasattr(self.factory, "execute_worker_step"):
            return None

        prompt = f"""[MISSING LOG PATTERNS]
{missing_patterns}

[CANDIDATE INTERACTIVE INPUTS]
{interactive_inputs}

[RECENT TERMINAL OUTPUT]
{terminal_output[-3000:]}

[TASK]
Analyze the terminal output. Determine if the CLI is waiting for input (e.g. prompt awaiting command like 'go', 'quit').
If input is needed to trigger code execution for missing logs, pick or suggest the next input string into suggested_stdin_input.
Output JSON matching VerificationDecisionSchema only."""

        try:
            res = self.factory.execute_worker_step(
                prompt=prompt,
                system_instruction="STRICT PROTOCOL: Output raw JSON object matching VerificationDecisionSchema.",
                response_mime_type="application/json",
                temperature=0.0
            )
            clean_res = re.sub(r"^```(?:json)?\n?|\n?```$", "", res.strip())
            return VerificationDecisionSchema.model_validate_json(clean_res)
        except Exception:
            return None

    def _run_terminal_verification(
        self,
        minimal_spec: Dict[str, Any],
        target_code: str,
        exec_env: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Stage 3 & 4: CLI 터미널 자율 대화형 제어 및 디버그 로그 정규식 대조 (피드백 루프 지원)
        """
        base_entrypoint = minimal_spec["entrypoint"] or f"python {minimal_spec['target_file']}"
        runner = TerminalAgentRunner(factory=self.factory, default_timeout=30)
        patterns = minimal_spec["expected_terminal_outputs"]
        interactive_inputs = minimal_spec.get("interactive_inputs", ["go", "quit"])

        test_type = minimal_spec.get("test_type", "").lower()
        is_standalone_test = test_type in ["python_test", "unit_test"] or ("python -c" in base_entrypoint)

        current_command = base_entrypoint
        terminal_output = ""
        matched_patterns: List[str] = []
        missing_patterns: List[str] = []
        is_verified = False
        has_runtime_error = False

        # 단독 함수 실행 테스트일 경우 대화형 피드백 루프 없이 1회 실행
        max_attempts = 1 if is_standalone_test else 3
        for attempt in range(max_attempts):
            res = runner.execute(
                command=current_command,
                goal_context=minimal_spec["task_id"],
                cwd=str(self.root_dir),
                env=exec_env,
                mission_data=minimal_spec,
                code_context=target_code
            )

            terminal_output = res.get("clean_output", "") or res.get("raw_output", "")
            matched_patterns = []
            missing_patterns = []

            # 1. 정규식 패턴 대조
            if patterns:
                for p in patterns:
                    regex_pat = build_log_regex_pattern(p)
                    if re.search(regex_pat, terminal_output, re.MULTILINE):
                        matched_patterns.append(p)
                    else:
                        missing_patterns.append(p)

            is_verified = (len(patterns) > 0 and len(missing_patterns) == 0)

            # 2. 치명적 예외 키워드 감지
            failure_keywords = ["Traceback (most recent call last):", "SyntaxError:", "ImportError:", "ModuleNotFoundError:", "npm ERR!"]
            has_runtime_error = any(kw in terminal_output for kw in failure_keywords)

            # 이미 검증 성공했거나 런타임 에러 발생 시, 또는 단독 테스트일 경우 즉시 종료
            if is_verified or has_runtime_error or is_standalone_test:
                break

            # 3. LLM 대화형 입력 판단 루프 (VerificationDecisionSchema 활용)
            decision = self._get_interactive_decision(
                terminal_output=terminal_output,
                missing_patterns=missing_patterns,
                interactive_inputs=interactive_inputs
            )

            if decision:
                if decision.is_verified:
                    is_verified = True
                    matched_patterns.extend(missing_patterns)
                    missing_patterns = []
                    break
                elif decision.suggested_stdin_input:
                    stdin_cmd = decision.suggested_stdin_input.strip()
                    # echo 구문으로 입력값을 파이프라인에 주입하여 다음 실행 시도
                    if os.name == 'nt':
                        current_command = f"cmd /c \"echo {stdin_cmd} | {base_entrypoint}\""
                    else:
                        current_command = f"echo {stdin_cmd} | {base_entrypoint}"
                    continue

            # 다음 입력을 제시받지 못했다면 루프 종료
            break

        # 4. 2차 만능 Fallback: 정규식/대화형 루프 실패 시 LLM Semantic Judge로 의미론적 검증 시도
        if not is_verified and not has_runtime_error:
            if self._run_semantic_llm_judge(terminal_output, missing_patterns, target_code):
                is_verified = True
                matched_patterns.extend(missing_patterns)
                missing_patterns = []

        # 5. 실패 시 자율 검증 에이전트(Verifier Agent) 진단 및 메인 루프 시야 확장 가동
        diagnosis_hint = ""
        if not is_verified and not has_runtime_error:
            diagnosis_res = self._run_autonomous_diagnosis(
                minimal_spec=minimal_spec,
                terminal_output=terminal_output,
                missing_patterns=missing_patterns
            )
            if diagnosis_res:
                diagnosis_hint = f"🔍 [자율 검증 에이전트 진단]\n- 원인: {diagnosis_res.root_cause}\n- 권장 사항: {diagnosis_res.recommended_action}"

        # 6. 세부 원인 구별 (failure_type 세분화 및 힌트 포함)
        if has_runtime_error:
            is_verified = False
            failure_type = "RUNTIME_ERROR"
            msg = "❌ 런타임 예외 발생 (Traceback/Error 포착)"
        elif not is_verified:
            failure_type = "LOG_PATTERN_MISMATCH"
            msg = f"⚠️ 디버그 로그 패턴 불일치 (미감지: {missing_patterns})\n{diagnosis_hint}"
        else:
            failure_type = "NONE"
            msg = f"✅ 디버그 로그 및 실행 검증 통과 ({len(matched_patterns)}/{len(patterns)} 매칭)"

        return {
            "verified": is_verified,
            "failure_type": failure_type,
            "output": terminal_output,
            "message": msg,
            "diagnosis_hint": diagnosis_hint,
            "matched_patterns": matched_patterns,
            "missing_patterns": missing_patterns
        }

    def _run_autonomous_diagnosis(
        self,
        minimal_spec: Dict[str, Any],
        terminal_output: str,
        missing_patterns: List[str]
    ) -> Optional[VerificationDiagnosisSchema]:
        """[검증 에이전트] 실패 시 엔트리포인트 파일 전체를 읽어 메인 루프/CLI 트리거 원인을 자율 진단"""
        if not self.factory or not hasattr(self.factory, "execute_worker_step"):
            return None

        entrypoint_file = minimal_spec.get("target_file") or minimal_spec.get("entrypoint", "").replace("python ", "").strip()
        full_path = self.root_dir / entrypoint_file
        
        entrypoint_code = ""
        if full_path.exists():
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    entrypoint_code = f.read()[:4000]  # 메인 루프 관찰을 위한 코드 로드
            except Exception:
                pass

        prompt = f"""[MISSING LOG PATTERNS]
{missing_patterns}

[ENTRYPOINT CODE CONTEXT (Main Loop / CLI)]
{entrypoint_code}

[ACTUAL TERMINAL OUTPUT]
{terminal_output[-2000:]}

[TASK]
Analyze why the debug log was NOT triggered. Inspect the entrypoint/main loop code.
1. Is the CLI stuck waiting for standard input? (What command triggers the target function?)
2. Is the target function never called in the main loop?
Provide diagnostic root cause and recommended action for the code patcher.
Output JSON matching VerificationDiagnosisSchema only."""

        try:
            res = self.factory.execute_worker_step(
                prompt=prompt,
                system_instruction="STRICT PROTOCOL: Output raw JSON object matching VerificationDiagnosisSchema.",
                response_mime_type="application/json",
                temperature=0.0
            )
            clean_res = re.sub(r"^```(?:json)?\n?|\n?```$", "", res.strip())
            return VerificationDiagnosisSchema.model_validate_json(clean_res)
        except Exception:
            return None

    def _run_semantic_llm_judge(
        self,
        terminal_output: str,
        missing_patterns: List[str],
        target_code: str = ""
    ) -> bool:
        """정규식 매칭 실패 시 작동하는 LLM 의미론적(Semantic) 만능 2차 검증기"""
        if not self.factory or not hasattr(self.factory, "execute_worker_step"):
            return False

        prompt = f"""[EXPECTED PATTERNS]
{missing_patterns}

[TARGET CODE CONTEXT]
{target_code[:2000]}

[ACTUAL TERMINAL OUTPUT]
{terminal_output[:3000]}

[TASK]
Determine if the required debug information/values are substantially present in the terminal output.
Ignore minor formatting differences (spaces, capitalization, quotes, exact text templates).
Output JSON matching SemanticJudgeSchema only."""

        try:
            res = self.factory.execute_worker_step(
                prompt=prompt,
                system_instruction="STRICT PROTOCOL: Output raw JSON object matching SemanticJudgeSchema.",
                response_mime_type="application/json",
                temperature=0.0
            )
            clean_res = re.sub(r"^```(?:json)?\n?|\n?```$", "", res.strip())
            judge_obj = SemanticJudgeSchema.model_validate_json(clean_res)
            return judge_obj.is_log_present
        except Exception:
            return False

    def _run_browser_verification(
        self,
        minimal_spec: Dict[str, Any],
        exec_env: Dict[str, str],
        full_mission_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Stage 3 & 4: 웹 브라우저 E2E 및 자율 에이전트 연동 검증"""
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

            matched_patterns = []
            missing_patterns = []
            for p in raw_patterns:
                reg = build_log_regex_pattern(p)
                if re.search(reg, logs):
                    matched_patterns.append(p)
                else:
                    missing_patterns.append(p)

            return {
                "verified": b_result["success"],
                "output": logs,
                "message": b_result.get("message", ""),
                "matched_patterns": matched_patterns,
                "missing_patterns": missing_patterns
            }

        finally:
            for proc in server_procs:
                if os.name == 'nt':
                    subprocess.run(f"taskkill /F /T /PID {proc.pid}", shell=True, capture_output=True)
                else:
                    proc.terminate()