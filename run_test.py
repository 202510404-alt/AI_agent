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
from tools.multi_agent_system.project_scale_detector import ProjectScaleDetector
from tools.multi_agent_system.agent_map_extractor import extract_targeted_ai_map

def load_mission_file(mission_rel_path: str) -> dict:
    """JSON 미션 파일 로더 및 규격 검증"""
    mission_path = ROOT_DIR / mission_rel_path
    if not mission_path.exists():
        raise FileNotFoundError(f"미션 파일을 찾을 수 없습니다: {mission_path}")
    
    with open(mission_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 필수 키 검증
    required_keys = ["task_id", "target_file", "description"]
    for key in required_keys:
        if key not in data:
            raise KeyError(f"미션 JSON에 필수 키가 누락되었습니다: '{key}'")
            
    return data

def clean_json_response(raw_response: str) -> str:
    """LLM 응답에서 마크다운 코드 블록(```json ... ```)을 제거하고 순수 JSON 문자열 추출"""
    text = raw_response.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    return text.strip()

# =====================================================================
# ⚙️ Step 기반 순차 실행 일꾼 파이프라인 (Worker Pipeline)
# =====================================================================
def run_step_worker_pipeline(mission_rel_path: str):
    print(f"\n🚀 [WORKER PIPELINE] 파이프라인 가동: '{mission_rel_path}'")
    factory = AgentSessionFactory(ROOT_DIR)
    
    # JSON 미션 데이터 로드
    mission_data = load_mission_file(mission_rel_path)
    target_file_path = mission_data["target_file"]
    mission_str = json.dumps(mission_data, ensure_ascii=False, indent=2)

    # -----------------------------------------------------------------
    # 🔍 [Step 1] 프로젝트 규모 진단 및 동적 지형도 생성 (1-Step / 2-Step 분기)
    # -----------------------------------------------------------------
    print("\n🗺️ [Step 1] 프로젝트 규모 측정 및 코드베이스 맵 준비...")
    scale_detector = ProjectScaleDetector(project_root=ROOT_DIR)
    scale_info = scale_detector.analyze_project_scale()

    if scale_info["is_oversized"]:
        print(f"⚠️ 대형 프로젝트 감지 ({scale_info['file_count']}개 파일, {scale_info['total_lines']}줄): 2단계 지형도 탐색 진행")
        shallow_map = scale_detector.generate_shallow_structure_map(
            max_depth=scale_info["recommended_depth"]
        )
        
        select_sys_instruction = (
            "STRICT PROTOCOL: Output raw JSON string array only. No commentary. "
            "Select ONLY minimum directories directly related to mission target."
        )

        select_prompt = f"""[1. CURRENT STATE & CONTEXT]
Target File: {target_file_path}
Mission Data:
{mission_str}

Project Shallow Structure Map:
{shallow_map}

[2. OUTPUT CONSTRAINTS]
- Extract ONLY the absolute minimum relative directory/file paths directly required for the mission.
- NO extra explanations, markdown tags, or conversational fluff.

[3. REQUIRED FORMAT]
["path/to/dir_or_file"]"""
        
        try:
            raw_dirs = factory.execute_worker_step(
                prompt=select_prompt,
                system_instruction=select_sys_instruction,
                response_mime_type="application/json"
            )
            target_dirs = json.loads(clean_json_response(raw_dirs))
            if not isinstance(target_dirs, list):
                target_dirs = [target_dirs]
                
            print(f"🎯 [Step 1 AI 선택 경로] {target_dirs}")
            codebase_map = extract_targeted_ai_map(target_paths=target_dirs, save_to_file=False)
        except Exception as e:
            print(f"⚠️ [Step 1 Warning] AI 경로 선택 처리 중 예외 발생({e}), 전체 기본 맵으로 대체 진행")
            codebase_map = extract_targeted_ai_map(save_to_file=False)
    else:
        print("✅ 일반 규모 프로젝트: AI 호출 없이 전체 AI 코드베이스 맵 direct 생성")
        codebase_map = extract_targeted_ai_map(save_to_file=False)

    # -----------------------------------------------------------------
    # 📄 [Step 2] 미션 기반 동적 필요 코드 영역 추론 및 추출 (하드코딩 제거)
    # -----------------------------------------------------------------
    print("\n📄 [Step 2] 미션 및 지형도 맵 기반 필요 코드 영역 동적 추출...")
    
    extract_sys_instruction = (
        "STRICT PROTOCOL: Output JSON string array matching [\"relative/path.py:start-end\"] only. "
        "Strictly limit targets to the mission's designated Target File or mandatory reference files. "
        "Do NOT slice unrequested system files."
    )

    extract_target_prompt = f"""[1. CURRENT STATE & CONTEXT]
Target File: {target_file_path}
Mission Data:
{mission_str}

Current Codebase Map:
{codebase_map}

[2. OUTPUT CONSTRAINTS]
- Specify target relative file paths and line ranges required to fulfill the mission.
- Do NOT request code slices for unreferenced system architecture files.

[3. REQUIRED FORMAT]
["{target_file_path}:start_line-end_line"]"""

    try:
        raw_slice_targets = factory.execute_worker_step(
            prompt=extract_target_prompt,
            system_instruction=extract_sys_instruction,
            response_mime_type="application/json"
        )
        slice_target_list = json.loads(clean_json_response(raw_slice_targets))
        
        if isinstance(slice_target_list, list) and len(slice_target_list) > 0:
            slice_prompt_str = " ".join(slice_target_list)
            print(f"🔍 [Step 2 AI 요청 슬라이스 Target] {slice_prompt_str}")
            slice_res = factory.extractor.process(slice_prompt_str, auto_save=False)
            target_code = slice_res.get("markdown", "")
        else:
            target_code = "(AI가 추출할 별도 코드 영역을 지정하지 않아 맵 기본 정보로 진행합니다.)"
    except Exception as e:
        print(f"⚠️ [Step 2 Warning] 필요 코드 영역 동적 추출 실패({e}), 기본 맵 정보 활용")
        target_code = "(코드 슬라이스 추출 중 예외가 발생하여 맵 정보만을 기반으로 진행합니다.)"

    print(f"📄 [Step 2 준비 완료] 추출된 코드 영역 길이: {len(target_code)}자")

    # -----------------------------------------------------------------
    # 🤖 [Step 3] LLM 단발성(Stateless) 패치 생성 요청
    # -----------------------------------------------------------------
    print("\n🤖 [Step 3] LLM 단발성 수정 패치 생성 중...")
    
    system_prompt = f"""STRICT EXECUTION PROTOCOL & SANDBOX RULES:
1. TARGET FILE BINDING: 'file_path' MUST be strictly set to '{target_file_path}'.
2. READ-ONLY SCOPE: Provided reference code slices from system files are READ-ONLY context. NEVER attempt to modify them.
3. ZERO CONVERSATIONAL FLUFF: Output valid raw JSON ONLY. NO markdown tags, NO preamble, NO postscript, NO explanations.
4. EXACT MATCH REPLACEMENT: 'existing_code' must match the target code section exactly for string replacement. If creating a new file or target file is empty, use an empty string "".
5. NO UNSANCTIONED REFACTORS: Do not add unrequested code, comments, or refactor existing architectures."""

    user_prompt = f"""[1. CURRENT STATE & CONTEXT]
■ Exact Target File Path:
{target_file_path}

■ Mission Data:
{mission_str}

■ Read-Only Context Code (DO NOT MODIFY THESE FILES):
{target_code}

[2. OUTPUT CONSTRAINTS]
- Target file_path MUST be exactly: "{target_file_path}"
- Modifications to system infrastructure files are strictly prohibited.

[3. REQUIRED FORMAT]
{{
  "file_path": "{target_file_path}",
  "existing_code": "exact_string_to_be_replaced",
  "replacement_code": "exact_new_string_to_apply"
}}"""

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
        cleaned_json_text = clean_json_response(raw_response)
        patch_data = json.loads(cleaned_json_text)
        file_path = patch_data.get("file_path")
        existing_code = patch_data.get("existing_code")
        replacement_code = patch_data.get("replacement_code")

        # 기존 bool 조건문 버그 수정: is not None 체크를 통해 ""(신규 생성/빈 기존 코드) 허용
        if file_path is not None and existing_code is not None and replacement_code is not None:
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

    # Target File이 'a'로 정상 수정된 JSON 규격 미션 파일 지정
    mission_file_path = "agent_core/tasks/task_01/checklist_01/mission_01.json"
    run_step_worker_pipeline(mission_file_path)

if __name__ == "__main__":
    main()