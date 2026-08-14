import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

from agent_core.debug_agent.runner import run_debug_pipeline

def main():
    print("🚀 ASE-OS Step Worker Pipeline 테스트 가동...")
    mission_file_path = "agent_core/tasks/task_01/checklist_01/mission_01.json"
    
    # 핵심 엔진 직접 호출
    success = run_debug_pipeline(
        root_dir=ROOT_DIR,
        mission_rel_path=mission_file_path,
        max_retries=3
    )
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()