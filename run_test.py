
import os
import sys
from pathlib import Path

# 1. ROOT_DIR을 '가장 먼저' 정의하고 sys.path에 추가
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

# 2. 그 이후에 내부 모듈 import 실행
from agent_core.plan.schemas import to_symbol_ref, LOG_FILE_PATH, DEBUG_MODE
from tools.multi_agent_system.agent_session import AgentSessionFactory

# =====================================================================
# 💬 대화형 AI 테스트 실행기
# =====================================================================
def run_interactive_chat():
    try:
        # AI 세션을 '구워주는' 팩토리 호출
        factory = AgentSessionFactory(ROOT_DIR)
        chat = factory.create_chat_session()
    except Exception as e:
        print(f"❌ 세션 생성 실패: {e}")
        return

    print("\n==================================================================")
    print("🤖 ASE-OS v1.3 Interactive AI Chat (Auto Execution Loop)")
    print("==================================================================")
    print("💡 사용자가 질의를 입력하면 AI가 필요 시 자동으로 도구를 실행합니다.")
    print("💡 종료하시려면 'exit' 또는 'quit'를 입력하세요.\n")

    while True:
        try:
            user_input = input("👤 User > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("👋 대화를 종료합니다.")
                break

            print("\n🤖 [Step 1] AI 판단 및 도구 실행 중...")
            response = chat.send_message(user_input)
            print(f"\n🤖 AI > {response.text}\n")

        except KeyboardInterrupt:
            print("\n👋 대화를 종료합니다.")
            break
        except Exception as e:
            print(f"\n💥 예외 발생: {e}\n")
# =====================================================================
# 🚀 메인 실행 진입점
# =====================================================================
def main():
    print("🚀 테스트 스크립트를 가동합니다...")
    
    # 1. 실행 시 디버그 로그 파일 초기화
    if LOG_FILE_PATH.exists():
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            f.write("=== [Jjap-Cursor Agent Debug Log Initialized] ===\n")
            
    print(f"📝 디버그 로그 위치: {LOG_FILE_PATH.resolve()}")
    print(f"🎛️ 현재 DEBUG_MODE 상태: {DEBUG_MODE}\n")

    # 2. 대화형 AI 인터랙션 진입
    print("🤖 대화형 AI 테스트 모드로 진입합니다...")
    run_interactive_chat()


if __name__ == "__main__":
    main()