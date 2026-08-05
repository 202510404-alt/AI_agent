import os
import sys
from pathlib import Path
import time
from google.genai.errors import APIError

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
            time.sleep(1.5)  # ⏱️ 연속 요청 간 RPM 안정화 대기
            
            # ---------------------------------------------------------
            # 💡 [API Key 돌려막기 & 429 전원 제한 시 대기 방어 루프]
            # ---------------------------------------------------------
            from google import genai

            response = None
            keys_count = len(factory.key_manager.keys)
            max_rounds = 3  # 모든 키를 순환하는 총 라운드 수
            
            for round_idx in range(max_rounds):
                # 등록된 모든 키를 1번씩 순차 시도
                for _ in range(keys_count):
                    try:
                        response = chat.send_message(user_input)
                        break  # 호출 성공 시 내부 루프 탈출
                    except APIError as e:
                        if e.code == 429 or "RESOURCE_EXHAUSTED" in str(e):
                            print(f"\n⚠️ [429 QUOTA HIT] Key 번호 {factory.key_manager.current_index + 1} 한도 초과!")
                            
                            # 다음 키로 순환 스위칭
                            next_key = factory.key_manager.rotate_key()
                            factory.client = genai.Client(api_key=next_key)
                            
                            # 기존 chat 객체의 internal client 바인딩 업데이트
                            if hasattr(chat, "_modules"):
                                chat._modules.client = factory.client
                        else:
                            raise e  # 429 외의 다른 예외는 즉시 발생

                if response is not None:
                    break  # 성공했으므로 전체 라운드 탈출

                # 🚨 모든 키가 다 429로 막혔을 때만 대기 진입
                wait_time = 20 * (round_idx + 1)
                print(f"\n🚨 [ALL KEYS EXHAUSTED] 등록된 모든 API 키({keys_count}개)가 한도에 도달했습니다!")
                print(f"⏳ {wait_time}초 동안 대기 후 1번 키부터 다시 순환 시도합니다... (라운드 {round_idx + 1}/{max_rounds})")
                time.sleep(wait_time)

            if response is None:
                print("❌ [ERROR] 최대 재시도 횟수를 초과하여 요청을 처리하지 못했습니다.\n")
                continue

            # AI가 도구를 호출했는지 디버그 출력
            if hasattr(response, "function_calls") and response.function_calls:
                print(f"🛠️ [DEBUG] AI가 호출한 도구 목록: {[call.name for call in response.function_calls]}")
            else:
                print("ℹ️ [DEBUG] AI가 도구 호출 없이 direct 텍스트 답변을 생성했습니다.")

            print(f"\n🤖 AI > {response.text}\n")
        except KeyboardInterrupt:
            print("\n👋 대화를 종료합니다.")
            break
        except Exception as e:
            print(f"\n💥 예외 발생: {e}\n")
            # 💡 [개선] 자세한 에러 추적을 위해 traceback 함께 출력
            import traceback
            traceback.print_exc()

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