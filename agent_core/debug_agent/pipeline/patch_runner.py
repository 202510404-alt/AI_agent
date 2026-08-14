"""
agent_core/pipeline/patch_runner.py
------------------------------------
Step 3 & Step 4: 패치 생성 및 CodePatcher 실행 모듈
"""

import json
from pathlib import Path
from agent_core.debug_agent.pipeline.mission_loader import safe_execute_step, clean_json_response

def generate_patch(factory, mission_data: dict, target_code: str) -> str:
    """[Step 3] LLM 기반 SEARCH/REPLACE 패치 생성"""
    target_file_path = mission_data["target_file"]
    mission_str = json.dumps(mission_data, ensure_ascii=False, indent=2)

    system_prompt = f"""STRICT EXECUTION PROTOCOL:
1. Target File: Strictly '{target_file_path}'.
2. Output code edits using EXACTLY the SEARCH/REPLACE block format shown below.
3. Include enough surrounding lines in SEARCH block to uniquely identify the code to change.
4. Keep exact whitespace/indentation.
5. Do NOT output JSON. Use raw SEARCH/REPLACE text blocks only. No markdown wrapped JSON, no explanations.
6. CLI Interaction Rule: If target code uses interactive `input()`, handle EOFError gracefully or separate main logic so background execution does not fail."""

    user_prompt = f"""<MISSION_SPEC>
Target File Path: {target_file_path}
Mission Details:
{mission_str}
</MISSION_SPEC>

<READ_ONLY_CONTEXT>
{target_code}
</READ_ONLY_CONTEXT>

<OUTPUT_FORMAT>
<<<<<<< SEARCH
[Exact original code snippet to replace]
=======
[New replacement code snippet]
>>>>>>> REPLACE
</OUTPUT_FORMAT>"""

    return safe_execute_step(
        factory, prompt=user_prompt, system_instruction=system_prompt, response_mime_type="text/plain"
    )

def apply_patch_blocks(factory, target_file_path: str, raw_response: str) -> tuple[bool, list]:
    """[Step 4] SEARCH/REPLACE 패치 적용"""
    try:
        patch_list = factory.patcher.parse_blocks(raw_response)
        if not patch_list:
            print("⚠️ [PATCH FAIL] SEARCH/REPLACE 패치 블록이 비어있음")
            return False, []

        all_patches_ok = True
        for idx, item in enumerate(patch_list, 1):
            existing_code = item["existing_code"]
            replacement_code = item["replacement_code"]
            patch_result = factory.patcher.apply_patch(target_file_path, existing_code, replacement_code)
            
            print(f"📌 [PATCH RESULT {idx}/{len(patch_list)}] {patch_result['message']}")
            if not patch_result.get("success", False):
                all_patches_ok = False
        return all_patches_ok, patch_list
    except Exception as e:
        print(f"❌ [STEP 4 ERROR] 패치 파싱/적용 오류: {e}")
        return False, []

def cleanup_temp_files(root_dir: Path, patch_list: list, target_file_path: str):
    """검증 성공 후 생성된 임시 테스트 파일 정리"""
    for item in patch_list:
        file_p = item.get("file_path", target_file_path)
        if file_p and file_p != target_file_path and ("test" in file_p.lower() or "temp" in file_p.lower()):
            temp_path = (root_dir / file_p).resolve()
            if temp_path.exists():
                temp_path.unlink()
                print(f"🧹 [CLEANUP] 임시 테스트 파일 삭제: {file_p}")