import os
import sys
import json
import re
import time
import subprocess
import urllib.request
from pathlib import Path
from pydantic import BaseModel
from typing import List

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

from agent_core.plan.schemas import LOG_FILE_PATH, DEBUG_MODE
from tools.multi_agent_system.agent_session import AgentSessionFactory
from tools.multi_agent_system.project_scale_detector import ProjectScaleDetector
from tools.multi_agent_system.agent_map_extractor import extract_targeted_ai_map
from agent_core.validation.debug_verifier import DebugVerifier

# 패치 스니펫 출력 구조 완전 강제화
class PatchItem(BaseModel):
    file_path: str
    existing_code: str
    replacement_code: str

class PatchPayload(BaseModel):
    patches: List[PatchItem]

def build_log_regex_pattern(template_msg: str) -> str:
    """미션의 디버그 로그 메시지 내 변수 표기({x}, {hex_code} 등)를 Regex 유연 패턴으로 자동 변환"""
    escaped = re.escape(template_msg)
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*num[a-zA-Z0-9_]*\\\}|\\\{x\\\}|\\\{y\\\}|\\\{val\\\}', r'[-+]?\\d*\\.?\\d+', escaped)
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*bool[a-zA-Z0-9_]*\\\}', r'(?i)(true|false)', escaped)
    escaped = re.sub(r'\\\{[a-zA-Z0-9_]*hex[a-zA-Z0-9_]*\\\}', r'#?[a-fA-F0-9]{3,6}', escaped)  # Hex Color 지원 추가
    escaped = re.sub(r'\\\{.*?\\\}', r'[\\s\\S]*?', escaped)
    return escaped

def load_mission_file(mission_rel_path: str) -> dict:
    """JSON 미션 파일 로더 및 규격 검증 (v1.3 신규 규격 적용)"""
    mission_path = ROOT_DIR / mission_rel_path
    if not mission_path.exists():
        raise FileNotFoundError(f"미션 파일을 찾을 수 없습니다: {mission_path}")
    
    with open(mission_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 신규 미션 JSON 규격 필수 키 검증 (task_id, target_file)
    required_keys = ["task_id", "target_file"]
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

    # 🛡️ 파이프라인 상단 단일 통합 정의 (0초 Fail-Fast 포착 및 로테이션)
    def safe_execute_step(prompt: str, system_instruction: str, response_mime_type: str = "application/json", max_attempts: int = 10) -> str:
        for attempt in range(1, max_attempts + 1):
            try:
                return factory.execute_worker_step(
                    prompt=prompt,
                    system_instruction=system_instruction,
                    response_mime_type=response_mime_type
                )
            except Exception as e:
                err_str = str(e)
                print(f"⚡ [Fail-Fast 감지] 0초 만에 예외 포착 -> ({err_str[:80]}...) | 즉시 다음 Key/Model 조합 스위칭 ({attempt}/{max_attempts})")
                if hasattr(factory, "switch_to_next_key"):
                    # 💡 발생한 예외 문자열(err_str)을 전달하여 403/429/503 분기 처리 유도
                    factory.switch_to_next_key(last_error_msg=err_str)
        raise RuntimeError("🚨 모든 Gemini API Key/Model 조합이 소진되었거나 오류로 인해 중단되었습니다.")

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
            raw_dirs = safe_execute_step(
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
        # 🛡️ [수정] 실제 target_file이 읽을 수 있도록 디스크에 codebase_map.json 파일 생성 보장
        codebase_map = extract_targeted_ai_map(save_to_file=True)

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
        raw_slice_targets = safe_execute_step(
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
            target_code = ""

        # ⚠️ 추출 결과가 비어있다면 Target File 전체 범위로 Extractor를 재호출하여 used_by/callee 심볼 추적 강제 가동
        if not target_code.strip():
            actual_target = ROOT_DIR / target_file_path
            if actual_target.exists():
                with open(actual_target, "r", encoding="utf-8") as f:
                    total_lines = len(f.readlines())
                fallback_prompt = f"{target_file_path}:1-{max(1, total_lines)}"
                print(f"⚠️ [Step 2 Fallback] Target File 전체 범위({fallback_prompt})로 Extractor 재추적 가동")
                slice_res = factory.extractor.process(fallback_prompt, auto_save=False)
                target_code = slice_res.get("markdown", "")
    except Exception as e:
        print(f"⚠️ [Step 2 Warning] 필요 코드 영역 동적 추출 예외 발생({e}), Fallback 전체 파일 추적 시도")
        actual_target = ROOT_DIR / target_file_path
        if actual_target.exists():
            with open(actual_target, "r", encoding="utf-8") as f:
                total_lines = len(f.readlines())
            fallback_prompt = f"{target_file_path}:1-{max(1, total_lines)}"
            slice_res = factory.extractor.process(fallback_prompt, auto_save=False)
            target_code = slice_res.get("markdown", "")
        else:
            target_code = "(Target File을 찾을 수 없어 코드 추출에 실패했습니다.)"

    print(f"📄 [Step 2 준비 완료] 추출된 코드 영역 길이: {len(target_code)}자")

    # -----------------------------------------------------------------
    # 🤖 [Step 3] LLM 단발성(Stateless) 다중 패치 생성 요청
    # -----------------------------------------------------------------
    print("\n🤖 [Step 3] LLM 단발성 수정 패치(다중 스니펫) 생성 중...")
    
    system_prompt = f"""STRICT EXECUTION PROTOCOL:
1. 'file_path': Strictly '{target_file_path}'.
2. 'existing_code': Exact raw string to replace. Keep context minimal to reduce token size.
3. 'replacement_code': Minimum modified code only.
4. OUTPUT: Raw JSON Object matching PatchPayload schema ONLY. No markdown, no explanations.
5. NO hardcoded env vars (e.g., os.environ). Rely on runtime env."""

    user_prompt = f"""<MISSION_SPEC>
Target File Path: {target_file_path}
Mission Details:
{mission_str}
</MISSION_SPEC>

<READ_ONLY_CONTEXT>
{target_code}
</READ_ONLY_CONTEXT>

<OUTPUT_INSTRUCTIONS>
Generate a JSON object matching PatchPayload schema:
{{
  "patches": [
    {{
      "file_path": "{target_file_path}",
      "existing_code": "exact_raw_string_to_be_replaced",
      "replacement_code": "exact_new_code_to_apply"
    }}
  ]
}}
</OUTPUT_INSTRUCTIONS>"""

    raw_response = safe_execute_step(
        prompt=user_prompt,
        system_instruction=system_prompt,
        response_mime_type="application/json"
    )

    # -----------------------------------------------------------------
    # 🛠️ [Step 4 ~ Step 6] 검증 및 자기 복구 실행 루프
    # -----------------------------------------------------------------
    max_retries = 3
    retry_count = 0

    while retry_count <= max_retries:
        print(f"\n🛠️ [Step 4] CodePatcher 1:1 검증 및 치환 적용 (시도 {retry_count + 1}/{max_retries + 1})...")
        patch_success = False
        try:
            # Pydantic 파싱으로 스키마 틀에 박힌 정확한 객체 검증
            payload = PatchPayload.model_validate_json(clean_json_response(raw_response))
            patch_list = [p.model_dump() for p in payload.patches]

            if patch_list:
                all_patches_ok = True
                for idx, item in enumerate(patch_list, 1):
                    file_path = item["file_path"]
                    existing_code = item["existing_code"]
                    replacement_code = item["replacement_code"]

                    patch_result = factory.patcher.apply_patch(file_path, existing_code, replacement_code)
                    print(f"📌 [PATCH RESULT {idx}/{len(patch_list)}] {patch_result['message']}")
                    print(f"   ├─ [BEFORE]: {existing_code.strip()[:60]}...")
                    print(f"   └─ [AFTER] : {replacement_code.strip()[:60]}...")
                    if not patch_result.get("success", False):
                        all_patches_ok = False
                patch_success = all_patches_ok
            else:
                print("⚠️ [PATCH FAIL] 패치 항목(patches)이 비어 있습니다.")

        except Exception as e:
            print(f"❌ [STEP 4 ERROR] Pydantic 스키마 검증 실패 또는 패치 적용 오류: {e}")

        # -------------------------------------------------------------
        # 💻 [Step 5] DebugVerifier 기반 검증 모듈 실행 (통합 검증)
        # -------------------------------------------------------------
        print("\n💻 [Step 5] DebugVerifier 통합 실행 및 실체 검증 가동...")

        if patch_success:
            verifier = DebugVerifier(root_dir=ROOT_DIR, factory=factory)
            verifier_res = verifier.verify(
                mission_data=mission_data,
                target_file_path=target_file_path,
                target_code=target_code
            )
            is_verified = verifier_res["verified"]
            terminal_output = verifier_res["output"]
            print(f"📄 [VERIFICATION OUTPUT]\n{terminal_output}")
            print(f"📌 [VERIFICATION RESULT] {verifier_res['message']}")
        else:
            is_verified = False
            terminal_output = "[PATCH FAIL] 패치 적용 실패로 인해 검증을 스킵합니다."

        if patch_success and is_verified:
            # 🧹 임시 생성된 검증용 테스트 파일 자동 청소 (Clean-up)
            created_temp_files = [
                item.get("file_path") for item in patch_list 
                if item.get("file_path") and item.get("file_path") != target_file_path 
                and ("test" in item.get("file_path").lower() or "temp" in item.get("file_path").lower())
            ]
            for temp_file in created_temp_files:
                temp_path = (ROOT_DIR / temp_file).resolve()
                if temp_path.exists():
                    temp_path.unlink()
                    print(f"🧹 [CLEANUP] 검증 완료 후 임시 테스트 파일 삭제: {temp_file}")

            print("\n🎉 [SUCCESS] 모든 디버깅 로그 및 작업 검증 완료!")
            return
        
        retry_count += 1
        if retry_count > max_retries:
            print("\n🚨 [FAIL] 최대 재시도 횟수를 초과하여 작업을 중단합니다.")
            return

        # -------------------------------------------------------------
        # 🩺 [Step 6-1] 정보 충분성 진단 및 피드백 분기 (Self-Diagnosis & Retry)
        # -------------------------------------------------------------
        print(f"\n🩺 [Step 6-1] 정보 충분성 진단 (재시도 {retry_count}/{max_retries})...")
        
        # 🛡️ 1회 실패 후(2회차 실행 이상)부터는 자기 과신 방지를 위해 Self-Diagnosis 호출을 생략하고 강제 broad 재탐색으로 전환
        if retry_count >= 2:
            print("⚠️ [강제 재탐색 발동] 2회 이상 실패 감지: LLM 자가 진단 생략 후 강제 broad 시야 확장(Retry Step 1)으로 전환합니다.")
            is_sufficient = False
        else:
            diag_prompt = f"""Target File: {target_file_path}
Mission Data: {mission_str}
Current Sliced Code: {target_code}
Terminal Output: {terminal_output}

Can you fix the code with the CURRENT provided code slice and terminal output alone?
Output raw JSON ONLY: {{"is_sufficient": true/false, "reason": "short explanation"}}"""

            try:
                diag_res = safe_execute_step(
                    prompt=diag_prompt,
                    system_instruction="STRICT PROTOCOL: Output raw JSON object with 'is_sufficient' boolean field only.",
                    response_mime_type="application/json"
                )
                diag_data = json.loads(clean_json_response(diag_res))
                is_sufficient = diag_data.get("is_sufficient", False)
            except Exception:
                is_sufficient = False

        if is_sufficient:
            # ---------------------------------------------------------
            # 🔄 [Step 6-2] 다중 패치 재수정 (Direct Fix)
            # ---------------------------------------------------------
            print("🔄 [Step 6-2] 정보 충분 -> 다중 수정 패치 재작성 중...")
            fix_user_prompt = f"""<MISSION_SPEC>\n{mission_str}\n</MISSION_SPEC>
<READ_ONLY_CONTEXT>\n{target_code}\n</READ_ONLY_CONTEXT>
<PREVIOUS_FAILURE_LOG>\n{terminal_output}\n</PREVIOUS_FAILURE_LOG>
Generate corrected JSON patch object matching PatchPayload schema:
{{
  "patches": [
    {{"file_path": "{target_file_path}", "existing_code": "exact_string", "replacement_code": "new_code"}}
  ]
}}"""
            raw_response = safe_execute_step(
                prompt=fix_user_prompt,
                system_instruction=system_prompt,
                response_mime_type="application/json"
            )
        else:
            # ---------------------------------------------------------
            # 🌐 [Retry Step 1] 시야 확장 재탐색 및 피드백 강화 (Broad Re-exploration)
            # ---------------------------------------------------------
            print("🌐 [Retry Step 1] 정보 부족 / 2회차 실패 -> 시야 확장 및 다중 경로 재탐색 진행...")
            scale_detector = ProjectScaleDetector(project_root=ROOT_DIR)
            shallow_map = scale_detector.generate_shallow_structure_map()
            
            broad_prompt = f"""Target File: {target_file_path}
Mission Data: {mission_str}
Project Structure: {shallow_map}
Previous Error Log: {terminal_output}

Select ALL relevant directory/file relative paths to inspect.
Output JSON string array matching: ["path/1", "path/2"]"""
            try:
                raw_dirs = safe_execute_step(
                    prompt=broad_prompt,
                    system_instruction="STRICT PROTOCOL: Output JSON string array of multiple target paths only.",
                    response_mime_type="application/json"
                )
                target_dirs = json.loads(clean_json_response(raw_dirs))
                if not isinstance(target_dirs, list):
                    target_dirs = [target_dirs]
                codebase_map = extract_targeted_ai_map(target_paths=target_dirs, save_to_file=False)
            except Exception:
                codebase_map = extract_targeted_ai_map(save_to_file=False)

            # 🛠️ [보완 1] 하드코딩된 '1-200' 삭제 -> 타깃 파일 전체 라인 수 동적 계측 후 Extractor 추적 실행
            actual_target = ROOT_DIR / target_file_path
            if actual_target.exists():
                with open(actual_target, "r", encoding="utf-8") as f:
                    total_lines = len(f.readlines())
                dynamic_slice_prompt = f"{target_file_path}:1-{max(1, total_lines)}"
            else:
                dynamic_slice_prompt = f"{target_file_path}:1-500"

            slice_res = factory.extractor.process(dynamic_slice_prompt, auto_save=False)
            target_code = slice_res.get("markdown", "")
            
            # 🛠️ [보완 2] 이전 실행 실패 로그(<PREVIOUS_FAILURE_LOG>)를 프롬프트에 필수 전달하여 피드백 강화
            retry_fix_prompt = f"""<MISSION_SPEC>\n{mission_str}\n</MISSION_SPEC>
<READ_ONLY_CONTEXT>\n{target_code}\n</READ_ONLY_CONTEXT>
<PREVIOUS_FAILURE_LOG>\n{terminal_output}\n</PREVIOUS_FAILURE_LOG>
Generate corrected JSON patch object matching PatchPayload schema:
{{
  "patches": [
    {{"file_path": "{target_file_path}", "existing_code": "exact_string", "replacement_code": "new_code"}}
  ]
}}"""
            raw_response = safe_execute_step(
                prompt=retry_fix_prompt,
                system_instruction=system_prompt,
                response_mime_type="application/json"
            )

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