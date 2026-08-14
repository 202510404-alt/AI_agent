"""
agent_core/pipeline/recovery_strategy.py
-----------------------------------------
Step 6: 실패 복구, 자가 진단 및 시야 확장(Broad Re-exploration) 모듈
"""

import json
from pathlib import Path
from tools.multi_agent_system.project_scale_detector import ProjectScaleDetector
from tools.multi_agent_system.agent_map_extractor import extract_targeted_ai_map
from agent_core.debug_agent.pipeline.mission_loader import safe_execute_step, clean_json_response

def evaluate_and_recover(root_dir: Path, factory, mission_data: dict, target_code: str, terminal_output: str, diagnosis_hint: str, retry_count: int) -> tuple[str, str]:
    """[Step 6] 실패 원인 진단 및 복구용 패치 재생성 (수정된 raw_response, target_code 반환)"""
    target_file_path = mission_data["target_file"]
    mission_str = json.dumps(mission_data, ensure_ascii=False, indent=2)

    system_prompt = f"STRICT EXECUTION PROTOCOL:\nTarget File: Strictly '{target_file_path}'. Output raw SEARCH/REPLACE blocks."

    # 2회 이상 실패 시 자가 진단 생략 후 바로 broad 탐색
    if retry_count >= 2:
        print("⚠️ [강제 재탐색] 2회 이상 실패: 강제 broad 시야 확장으로 전환합니다.")
        is_sufficient = False
    else:
        diag_prompt = f"""Target File: {target_file_path}
Mission Data: {mission_str}
Current Sliced Code: {target_code}
Terminal Output: {terminal_output}
Verifier Diagnosis: {diagnosis_hint}

Can you fix the code with the CURRENT provided code slice, verifier diagnosis, and terminal output alone?
Output raw JSON ONLY: {{"is_sufficient": true/false, "reason": "short explanation"}}"""

        try:
            diag_res = safe_execute_step(
                factory, prompt=diag_prompt, system_instruction="STRICT PROTOCOL: Output raw JSON object with 'is_sufficient' boolean field only."
            )
            diag_data = json.loads(clean_json_response(diag_res))
            is_sufficient = diag_data.get("is_sufficient", False)
        except Exception:
            is_sufficient = False

    if is_sufficient:
        print("🔄 [Step 6-2] 진단 힌트 기반 패치 재작성...")
        fix_prompt = f"""<MISSION_SPEC>\n{mission_str}\n</MISSION_SPEC>
<READ_ONLY_CONTEXT>\n{target_code}\n</READ_ONLY_CONTEXT>
<PREVIOUS_FAILURE_LOG>\n{terminal_output}\n</PREVIOUS_FAILURE_LOG>
<VERIFIER_AGENT_DIAGNOSIS>\n{diagnosis_hint}\n</VERIFIER_AGENT_DIAGNOSIS>

Output corrected SEARCH/REPLACE blocks:
<<<<<<< SEARCH
[Exact original code snippet]
=======
[New replacement code snippet]
>>>>>>> REPLACE"""
        raw_response = safe_execute_step(factory, prompt=fix_prompt, system_instruction=system_prompt, response_mime_type="text/plain")
        return raw_response, target_code
    else:
        print("🌐 [Retry Step 1] Broad 시야 확장 및 다중 경로 재탐색...")
        scale_detector = ProjectScaleDetector(project_root=root_dir)
        shallow_map = scale_detector.generate_shallow_structure_map()
        
        broad_prompt = f"""Target File: {target_file_path}
Mission Data: {mission_str}
Project Structure: {shallow_map}
Previous Error Log: {terminal_output}

Select ALL relevant directory/file relative paths to inspect.
Output JSON string array matching: ["path/1", "path/2"]"""
        try:
            raw_dirs = safe_execute_step(factory, prompt=broad_prompt, system_instruction="STRICT PROTOCOL: Output JSON string array.")
            target_dirs = json.loads(clean_json_response(raw_dirs))
            if not isinstance(target_dirs, list):
                target_dirs = [target_dirs]
            extract_targeted_ai_map(target_paths=target_dirs, save_to_file=False)
        except Exception:
            extract_targeted_ai_map(save_to_file=False)

        actual_target = root_dir / target_file_path
        if actual_target.exists():
            with open(actual_target, "r", encoding="utf-8") as f:
                total_lines = len(f.readlines())
            slice_prompt = f"{target_file_path}:1-{max(1, total_lines)}"
        else:
            slice_prompt = f"{target_file_path}:1-500"

        new_target_code = factory.extractor.process(slice_prompt, auto_save=False).get("markdown", "")

        retry_fix_prompt = f"""<MISSION_SPEC>\n{mission_str}\n</MISSION_SPEC>
<READ_ONLY_CONTEXT>\n{new_target_code}\n</READ_ONLY_CONTEXT>
<PREVIOUS_FAILURE_LOG>\n{terminal_output}\n</PREVIOUS_FAILURE_LOG>
<VERIFIER_AGENT_DIAGNOSIS>\n{diagnosis_hint}\n</VERIFIER_AGENT_DIAGNOSIS>

Output corrected SEARCH/REPLACE blocks:
<<<<<<< SEARCH
[Exact original code snippet]
=======
[New replacement code snippet]
>>>>>>> REPLACE"""
        raw_response = safe_execute_step(factory, prompt=retry_fix_prompt, system_instruction=system_prompt, response_mime_type="text/plain")
        return raw_response, new_target_code