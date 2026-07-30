"""
run_test.py
에이전트 모듈 기능 검증 및 디버그 로그 파일 출력 테스트 실행기
"""

import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

from agent_core.plan.schemas import to_symbol_ref, LOG_FILE_PATH, DEBUG_MODE
from agent_core.plan.prompt_builder import PromptBuilder


def init_log_file():
    """실행 시 기존 디버그 로그 파일을 싹 비우고 새 파일로 초기화합니다."""
    with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
        f.write("=== [Jjap-Cursor Agent Debug Log Initialized] ===\n")


def main():
    print("🚀 테스트 스크립트를 가동합니다...")
    
    # 1. 실행 시 디버그 로그 파일 초기화
    init_log_file()
    print(f"📝 디버그 로그가 단일 파일에 모입니다: {LOG_FILE_PATH.resolve()}")
    print(f"🎛️ 현재 DEBUG_MODE 상태: {DEBUG_MODE}\n")

    # 2. schemas.py 기능 테스트 (SymbolRef 변환 어댑터)
    print("1️⃣ [테스트] to_symbol_ref() 변환 테스트 진행 중...")
    raw_symbol_data = {
        "name": "login_user",
        "start_line": 15,
        "end_line": 42
    }
    symbol_ref = to_symbol_ref(raw_symbol_data, default_file="auth/service.py")
    print(f"   -> 변환 결과: {symbol_ref.symbol_name} ({symbol_ref.file_path}:{symbol_ref.start_line}~{symbol_ref.end_line})")

    # 3. prompt_builder.py 기능 테스트 (프롬프트 조립)
    print("\n2️⃣ [테스트] PromptBuilder 프롬프트 조립 테스트 진행 중...")
    builder = PromptBuilder(root_dir=ROOT_DIR)
    
    test_goal = "로그인 실패 시 3회 제한 후 계정을 잠그는 로직을 추가해 줘."
    prompt_result = builder.build_plan_prompt(user_goal=test_goal)
    
    print(f"   -> 프롬프트 생성 완 (길이: {len(prompt_result)}자)")
    
    print("\n✅ 모든 동작 완료! 터미널 출력을 최소화하였으며, 상세 내역은 'agent_debug.log'에서 확인하실 수 있습니다.")


if __name__ == "__main__":
    main()
    