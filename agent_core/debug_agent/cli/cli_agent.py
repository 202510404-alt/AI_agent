"""
agent_core/cli/cli_agent.py
---------------------------
DebugAgent 하위에서 대화형/범용 CLI 프로세스 구동 및 
실시간 터미널 인터랙션을 전담하는 자율형 서브 에이전트
"""

import os
import sys
import traceback
from pathlib import Path
from typing import Dict, Any, Optional

from agent_core.debug_agent.schemas import CapturedLogResult
from tools.multi_agent_system.terminal_agent_runner import TerminalAgentRunner


class CliPipelineAgent:
    """
    어떠한 CLI 프로젝트(단순 인자, 대화형 stdin, 다중 명령 등)에도 
    동적으로 대응 가능한 터미널 실행 서브 에이전트
    """
    def __init__(self, root_dir: Path, factory: Any = None, max_retries: int = 3):
        self.root_dir = Path(root_dir).resolve()
        self.factory = factory
        self.max_retries = max_retries
        self.terminal_runner = TerminalAgentRunner(
            factory=factory,
            max_retries=max_retries,
            default_timeout=30.0
        )

    def execute_and_collect(
        self, 
        mission_data: Dict[str, Any], 
        entrypoint_cmd: str,
        target_code: str = ""
    ) -> CapturedLogResult:
        """
        TerminalAgentRunner를 호출하여 대화형 CLI 세션을 구동하고 최종 로그를 수집
        """
        debug_spec = mission_data.get("debug_log_spec", {})
        blueprint = mission_data.get("implementation_blueprint", {})
        
        # 1. 환경변수 구성 (시스템 환경변수 + 미션 지정 env + 디버그 토글 주입)
        env = dict(os.environ)
        mission_env = mission_data.get("env", {})
        if isinstance(mission_env, dict):
            env.update(mission_env)

        toggle_key = debug_spec.get("toggle_key") or blueprint.get("debug_toggle_key")
        if toggle_key:
            env[toggle_key] = "1"
            env[f"{toggle_key}_ENABLE"] = "true"

        # 2. LLM 의사결정 맥락(Goal Context) 상세화
        expected_outputs = mission_data.get("expected_terminal_outputs", [])
        goal_context = (
            f"Target Task: {mission_data.get('task_id', 'CLI Task')}\n"
            f"Expected Terminal Patterns: {expected_outputs}\n"
            f"Mission Spec: {mission_data.get('description', '')}\n"
            f"Instruction: Interact with the CLI prompt intelligently to satisfy expected output patterns."
        )

        print(f"🖥️ [CliPipelineAgent] 대화형 PTY 터미널 세션 가동: '{entrypoint_cmd}'")

        # 3. TerminalAgentRunner 실행 및 예외 안전망 적용
        try:
            run_result = self.terminal_runner.execute(
                command=entrypoint_cmd,
                goal_context=goal_context,
                cwd=str(self.root_dir),
                env=env,
                mission_data=mission_data,
                code_context=target_code
            )

            raw_logs = run_result.get("buffer", "")
            status = run_result.get("status", "FAIL")
            success = (status == "SUCCESS")
            exit_code = run_result.get("exit_code", 0 if success else -1)
            error_msg = run_result.get("error_msg", "")

        except Exception as e:
            print(f"❌ [CliPipelineAgent] 실행 중 예외 발생: {e}")
            raw_logs = f"[CLI EXECUTION EXCEPTION]\n{traceback.format_exc()}"
            success = False
            exit_code = -1
            error_msg = str(e)

        return CapturedLogResult(
            channel_type="cli",
            raw_logs=raw_logs,
            returncode=exit_code,
            error_message=error_msg,
            success=success
        )