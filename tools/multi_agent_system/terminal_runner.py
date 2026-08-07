"""
tools/multi_agent_system/terminal_runner.py
AI 에이전트가 터미널 명령어를 실행하고 로그/에러를 수집하는 도구
"""

import subprocess
from pathlib import Path

# 보안상 실행 차단할 위험 명령어
FORBIDDEN_COMMANDS = ["rm -rf", "rd /s", "format", "mkfs", "dd"]

def run_terminal_command(command: str, cwd: str = None, timeout: int = 30, env: dict = None) -> str:
    """
    터미널 명령어를 실행하고 stdout 및 stderr 결과를 반환합니다.
    
    Args:
        command: 실행할 명령어 (예: "python run_test.py", "pytest", "npm test")
        cwd: 명령어를 실행할 작업 디렉토리 경로 (기본값: 프로젝트 루트)
        timeout: 최대 실행 대기 시간(초)
        env: 실행 환경변수 딕셔너리
    """
    for forbidden in FORBIDDEN_COMMANDS:
        if forbidden in command.lower():
            return f"❌ [보안 거부] 위험 키워드가 포함된 명령어는 실행이 차단되었습니다: '{forbidden}'"

    # 프로젝트 루트 경로 자동 설정
    work_dir = cwd if cwd else str(Path(__file__).parent.parent.parent.resolve())

    print(f"\n💻 [TERMINAL TOOL] 명령어 실행 중: `{command}` (경로: {work_dir})")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=work_dir,
            timeout=timeout,
            env=env
        )

        output = []
        if result.stdout:
            output.append(f"--- [STDOUT (정상 출력)] ---\n{result.stdout.strip()}")
        if result.stderr:
            output.append(f"--- [STDERR (에러 로그)] ---\n{result.stderr.strip()}")

        if not output:
            return f"✅ 명령어 실행 완료 (반환 코드: {result.returncode}, 출력 없음)"

        status_msg = "✅ 실행 성공" if result.returncode == 0 else f"⚠️ 실행 종료 (오류 코드: {result.returncode})"
        return f"{status_msg}\n\n" + "\n\n".join(output)

    except subprocess.TimeoutExpired:
        return f"⏰ [타임아웃] 명령어 실행 시간이 {timeout}초를 초과하여 강제 종료되었습니다."
    except Exception as e:
        return f"💥 [실행 예외 발생] {str(e)}"