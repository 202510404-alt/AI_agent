"""
run_test.py
에이전트 모듈 기능 검증, 디버그 로그 파일 출력 및 대화형 AI Tool Calling 2-Step 자동 루프 실행기
"""

import os
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

from agent_core.plan.schemas import to_symbol_ref, LOG_FILE_PATH, DEBUG_MODE
from agent_core.plan.prompt_builder import PromptBuilder
from agent_core.plan.gemini_client import load_env_file, HAS_GENAI
from tools.multi_agent_system.agent_code_extractor import CodeExtractor
from tools.multi_agent_system.terminal_runner import run_terminal_command

if HAS_GENAI:
    from google import genai
    from google.genai import types

# .env 자동 로드
load_env_file(ROOT_DIR / ".env")


def init_log_file():
    """실행 시 기존 디버그 로그 파일을 싹 비우고 새 파일로 초기화합니다."""
    with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
        f.write("=== [Jjap-Cursor Agent Debug Log Initialized] ===\n")


# =====================================================================
# 🛠️ AI에게 제공할 도구(Tools) 정의
# =====================================================================
extractor = CodeExtractor(ROOT_DIR)

def extract_code_slice(file_and_line: str) -> str:
    """
    특정 파일 및 라인 범위의 코드 슬라이스를 추출하고 관련 심볼 정보까지 정밀 검색합니다.
    
    Args:
        file_and_line: "파일경로:시작줄-끝줄" 형태의 문자열 (예: "agent_core/plan/schemas.py:15-40" 또는 "system_maps/create_ai_map.py:1-100")
    """
    print(f"\n⚙️ [SYSTEM TOOL EXECUTION] 'extract_code_slice' 실행 중... Target: {file_and_line}")
    res = extractor.process(file_and_line, auto_save=False)
    if res["markdown"]:
        return res["markdown"]
    return "❌ 해당 파일 또는 라인 범위를 찾을 수 없거나 코드 추출에 실패했습니다."


# =====================================================================
# 💬 대화형 AI 테스트 실행기 (2-Step Automatic Execution Loop)
# =====================================================================
def run_interactive_chat():
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not HAS_GENAI:
        print("❌ 'google-genai' 패키지가 설치되어 있지 않습니다. (pip install google-genai)")
        return
        
    if not api_key:
        print("⚠️ GEMINI_API_KEY가 존재하지 않습니다. .env 파일에 키를 설정해주세요.")
        return

    client = genai.Client(api_key=api_key)
    
    # AI_CODEBASE_MAP.md 실제 경로 보정 탐색
    map_path = ROOT_DIR / "system_maps" / "AI_CODEBASE_MAP.md"
    if not map_path.exists():
        map_path = ROOT_DIR / "AI_CODEBASE_MAP.md"

    codebase_map_content = ""
    if map_path.exists():
        codebase_map_content = map_path.read_text(encoding="utf-8")
    else:
        codebase_map_content = "[안내] 코드베이스 지도를 찾을 수 없습니다."

    # 지형도와 시스템 프로토콜 준비
    system_instruction = f"""
당신은 현재 프로젝트의 코드베이스 구조를 파악하고, 터미널 명령어를 직접 실행하여 오류를 분석 및 디버깅하는 AI 에이전트입니다.

[프로젝트 코드베이스 지도 (AI_CODEBASE_MAP)]
{codebase_map_content}

[사용 가능한 도구]
1. `extract_code_slice("파일경로:시작줄-끝줄")`: 코드의 실제 내용을 확인합니다.
2. `run_terminal_command("명령어")`: 터미널 명령어(예: 테스트 실행, 스크립트 실행 등)를 직접 구동하고 출력/에러 로그를 확인합니다.

[작동 지침]
1. 코드 테스트나 오류 확인이 필요한 경우 `run_terminal_command`를 사용해 명령어를 구동하십시오.
2. 실행 결과로 출력된 `STDERR` (에러 로그)나 스택 트레이스(Stack Trace)를 읽고 원인을 분석하십시오.
3. 문제 지점을 파악한 뒤 필요시 `extract_code_slice`로 관련 코드를 열람하여 정확한 해결책을 제시하십시오.
"""

    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[extract_code_slice, run_terminal_command], # <- 터미널 도구 추가 등록!
            temperature=0.2,
        )
    )

    print("\n==================================================================")
    print("🤖 ASE-OS v1.3 Interactive AI Chat (Auto 2-Step Execution Loop)")
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

            print("\n🤖 [Step 1] AI가 코드베이스 지도를 분석하고 도구 호출 여부를 판단 중...")
            
            # 1차 실행: 사용자의 질의 전달 및 도구 호출 자동 수행
            response = chat.send_message(user_input)
            
            # 최종 AI 응답 출력
            print(f"\n🤖 AI > {response.text}\n")

        except KeyboardInterrupt:
            print("\n👋 대화를 종료합니다.")
            break
        except Exception as e:
            print(f"\n💥 예외 발생: {e}\n")


def main():
    print("🚀 테스트 스크립트를 가동합니다...")
    
    # 1. 실행 시 디버그 로그 파일 초기화
    init_log_file()
    print(f"📝 디버그 로그가 단일 파일에 모입니다: {LOG_FILE_PATH.resolve()}")
    print(f"🎛️ 현재 DEBUG_MODE 상태: {DEBUG_MODE}\n")

    # 2. schemas.py 기능 테스트
    print("1️⃣ [테스트] to_symbol_ref() 변환 테스트 진행 중...")
    raw_symbol_data = {
        "name": "login_user",
        "start_line": 15,
        "end_line": 42
    }
    symbol_ref = to_symbol_ref(raw_symbol_data, default_file="auth/service.py")
    print(f"   -> 변환 결과: {symbol_ref.symbol_name} ({symbol_ref.file_path}:{symbol_ref.start_line}~{symbol_ref.end_line})")

    # 3. prompt_builder.py 기능 테스트
    print("\n2️⃣ [테스트] PromptBuilder 프롬프트 조립 테스트 진행 중...")
    builder = PromptBuilder(root_dir=ROOT_DIR)
    test_goal = "로그인 실패 시 3회 제한 후 계정을 잠그는 로직을 추가해 줘."
    prompt_result = builder.build_plan_prompt(user_goal=test_goal)
    print(f"   -> 프롬프트 생성 완 (길이: {len(prompt_result)}자)")
    print("\n✅ 기존 모듈 기초 검증 완료!")

    # 4. 대화형 AI 인터랙션 진입
    print("\n3️⃣ [테스트] 대화형 AI 및 자동 도구 실행 테스트 모드로 진입합니다...")
    run_interactive_chat()


if __name__ == "__main__":
    main()