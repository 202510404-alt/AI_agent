import os
import sys
import json
import re
from pathlib import Path

# 1. ROOT_DIR 초기화 및 경로 설정
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

from agent_core.plan.schemas import LOG_FILE_PATH, DEBUG_MODE
from tools.multi_agent_system.agent_session import AgentSessionFactory

# =====================================================================
# ⚙️ Step 기반 순차 실행 일꾼 파이프라인 (Worker Pipeline)
# =====================================================================
def run_step_worker_pipeline(user_goal: str):
    print(f"\n🚀 [WORKER PIPELINE] 파이프라인 가동: '{user_goal}'")
    factory = AgentSessionFactory(ROOT_DIR)

    # -----------------------------------------------------------------
    # 🔍 [Step 1] 프로젝트 규모 진단 및 코드베이스 지형도 생성
    # -----------------------------------------------------------------
    print("\n🗺️ [Step 1] 프로젝트 지도 작성 및 범위 분석 중...")
    codebase_map, is_oversized = factory.prepare_step1_map()
    
    # -----------------------------------------------------------------
    # 📄 [Step 2] 정규식/슬라이서 이용 필요 코드 영역 준비
    # -----------------------------------------------------------------
    print("\n📄 [Step 2] 분석 및 수정 필요 코드 영역 추출...")
    # 예시: extraction_target_project 내 main.py 코드 슬라이스 추출
    target_file_rel = "extraction_target_project/main.py"
    target_file_abs = factory.root_dir / target_file_rel

    if target_file_abs.exists():
        slice_res = factory.extractor.process(f"{target_file_rel}:1-100", auto_save=False)
        target_code = slice_res.get("markdown", "")
    else:
        target_code = "(대상 파일이 없어 기본 맵 정보를 기초로 수정 작업을 진행합니다.)"

    # -----------------------------------------------------------------
    # 🤖 [Step 3] LLM 단발성(Stateless) 패치 생성 요청
    # -----------------------------------------------------------------
    print("\n🤖 [Step 3] LLM 단발성 수정 패치 생성 중...")
    
    # 💡 백틱(```)을 제거하여 UI/검은박스가 깨지는 현상을 방지했습니다.
    system_prompt = """당신은 정밀한 코드 수정안(Patch)을 생성하는 핵심 AI Worker입니다.
반드시 아래 JSON 포맷에 맞추어 응답해야 하며, 다른 설명 텍스트를 포함하지 마십시오.

{
  "file_path": "대상_파일_상대_경로",
  "existing_code": "치환할_기존_코드_구간",
  "replacement_code": "새롭게_교체할_코드_구간"
}
"""

    user_prompt = f"""[사용자 수정 목표]
{user_goal}

[프로젝트 구조 정보]
{codebase_map}

[현재 관련 코드 영역]
{target_code}

위 내용을 기반으로 코드를 수정하기 위한 정확한 JSON 패치를 생성해 주세요."""

    raw_response = factory.execute_worker_step(
        prompt=user_prompt,
        system_instruction=system_prompt,
        response_mime_type="application/json"
    )

    # -----------------------------------------------------------------
    # 🛠️ [Step 4] CodePatcher 1:1 검증 및 치환 적용
    # -----------------------------------------------------------------
    print("\n🛠️ [Step 4] CodePatcher 1:1 검증 및 치환 적용...")
    try:
        # JSON 블록 정제
        cleaned_json_text = raw_response.strip()
        if cleaned_json_text.startswith("```"):
            cleaned_json_text = re.sub(r"^```(?:json)?\n?", "", cleaned_json_text)
            cleaned_json_text = re.sub(r"\n?```$", "", cleaned_json_text)

        patch_data = json.loads(cleaned_json_text)
        file_path = patch_data.get("file_path")
        existing_code = patch_data.get("existing_code")
        replacement_code = patch_data.get("replacement_code")

        if file_path and existing_code and replacement_code:
            patch_result = factory.patcher.apply_patch(file_path, existing_code, replacement_code)
            print(f"📌 [PATCH RESULT] {patch_result['message']}")
        else:
            print(f"⚠️ [PATCH FAIL] 필수 파라미터가 유효하지 않습니다: {patch_data}")

    except Exception as e:
        print(f"❌ [STEP 4 ERROR] 패치 응답 해석 또는 적용 중 오류 발생: {e}")
        print(f"📄 Raw LLM Response:\n{raw_response}")

# =====================================================================
# 🚀 메인 실행 진입점
# =====================================================================
def main():
    print("🚀 ASE-OS v1.3 Step Worker Pipeline 테스트 가동...")

    if LOG_FILE_PATH.exists():
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            f.write("=== [Step Worker Pipeline Debug Log Initialized] ===\n")

    # 사용자 목표 설정 후 순차 파이프라인 실행
    user_goal = "main.py 파일의 메인 실행부 예외 처리를 보강하고 디버그 로그 기록 기능을 추가해 줘."
    run_step_worker_pipeline(user_goal)

if __name__ == "__main__":
    main()