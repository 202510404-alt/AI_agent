import sys
import subprocess
from pathlib import Path

# 0. 필수 패키지 누락 시 자동 설치
for pkg in ["psutil", "pydantic"]:
    try:
        __import__(pkg)
    except ImportError:
        print(f"📦 필수 패키지 '{pkg}' 미설치 감지 -> 자동 설치를 진행합니다...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# 1. ROOT_DIR 초기화 및 경로 설정
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

from agent_core.plan.schemas import LOG_FILE_PATH
from agent_core.worker import StepWorkerPipeline

def main():
    print("🚀 ASE-OS v1.3 Step Worker Pipeline 테스트 가동...")

    if LOG_FILE_PATH.exists():
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            f.write("=== [Step Worker Pipeline Debug Log Initialized] ===\n")

    mission_file_path = "agent_core/tasks/task_01/checklist_01/mission_01.json"
    
    # 모듈화된 일꾼 파이프라인 가동
    pipeline = StepWorkerPipeline(root_dir=ROOT_DIR)
    pipeline.run(mission_file_path)

if __name__ == "__main__":
    main()