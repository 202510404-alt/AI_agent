"""
agent_core/debug_agent/cli/cli_runner.py
----------------------------------
Debug Agent CLI 메인 엔트리포인트 (argparse 기반)
"""

import sys
import argparse
from pathlib import Path
from agent_core.debug_agent.runner import run_debug_pipeline


def main():
    parser = argparse.ArgumentParser(
        prog="python -m agent_core.debug_agent.cli.cli_runner",
        description="ASE-OS Debug Agent CLI Runner",
    )
    
    parser.add_argument(
        "--mission", "-m",
        type=str,
        required=True,
        help="실행할 미션 JSON 파일의 상대 경로 (예: agent_core/tasks/task_01/checklist_01/mission_01.json)"
    )
    parser.add_argument(
        "--max-retries", "-r",
        type=int,
        default=3,
        help="실패 시 자기 복구 루프 최대 시도 횟수 (기본값: 3)"
    )

    args = parser.parse_args()
    root_dir = Path(__file__).resolve().parents[3]

    success = run_debug_pipeline(
        root_dir=root_dir,
        mission_rel_path=args.mission,
        max_retries=args.max_retries
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()