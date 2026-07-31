"""
test_ai_chat.py
AI와 실시간 대화하며 Tool Calling (명령어/도구 호출) 및 시스템 작동 상태를 검증하는 테스트 인터페이스
"""

import os
import sys
import json
from pathlib import Path

# 프로젝트 루트 경로 설정
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

from agent_core.plan.gemini_client import load_env_file, HAS_GENAI
from agent_core.plan.prompt_builder import PromptBuilder
from tools.multi_agent_system.agent_code_extractor import CodeExtractor

if HAS_GENAI:
    from google import genai
    from google.genai import types

# .env 로드
load_env_file(ROOT_DIR / ".env")


# =====================================================================
# 🛠️ AI에게 제공할 도구(Tools) 정의
# =====================================================================
extractor = CodeExtractor(ROOT_DIR)

def extract_code_slice(file_and_line: str) -> str:
    """
    특정 파일 및 라인 범위의 코드 슬라이스를 추출하고 관련 심볼 정보까지 정밀 검색합니다.
    
    Args:
        file_and_line: "파일경로:시작줄-끝줄" 형태의 문자열 (예: "agent_core/plan/schemas.py:15-40")
    """
    print(f"\n⚙️ [SYSTEM TOOL EXECUTION] 'extract_code_slice' 실행 중... Target: {file_and_line}")
    res = extractor.process(file_and_line, auto_save=False)
    if res["markdown"]:
        return res["markdown"]
    return "❌ 해당 파일 또는 라인 범위를 찾을 수 없거나 코드 추출에 실패했습니다."


# =====================================================================
# 💬 AI 대화 및 Tool Calling 검증 루프
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
    prompt_builder = PromptBuilder(root_dir=ROOT_DIR)
    
    # 1. AI 지형도 시스템 프롬프트 준비
    system_instruction = prompt_builder.build_plan_prompt(
        user_goal="사용자의 질의에 따라 필요한 경우 도구(Tool)를 호출하여 코드나 정보를 확인하고 답변하십시오."
    )

    # 2. Chat 세션 초기화 (Tool 등록 및 Chat 자동 컨텍스트 관리)
    # gemini-2.5-flash 모델을 사용하여 대화 및 Tool Calling 처리
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[extract_code_slice], # AI가 스스로 호출 가능한 함수 전달
            temperature=0.2,
        )
    )

    print("\n==================================================================")
    print("🤖 ASE-OS v1.3 Interactive AI Chat & Tool Calling Validation")
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

            print("🤖 AI 생각 중...")
            response = chat.send_message(user_input)
            
            # AI의 최종 응답 출력
            print(f"\n🤖 AI > {response.text}\n")

        except KeyboardInterrupt:
            print("\n👋 대화를 종료합니다.")
            break
        except Exception as e:
            print(f"\n💥 예외 발생: {e}\n")


if __name__ == "__main__":
    run_interactive_chat()