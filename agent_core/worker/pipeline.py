import json
from pathlib import Path
from tools.multi_agent_system.agent_session import AgentSessionFactory
from tools.multi_agent_system.project_scale_detector import ProjectScaleDetector
from tools.multi_agent_system.agent_map_extractor import extract_targeted_ai_map
from agent_core.debug_agent.verifier import DebugVerifier
from agent_core.worker.utils import load_mission_file, safe_execute_step, clean_json_response
from agent_core.worker.pipeline_steps import (
    execute_step1_map_building,
    execute_step2_code_slicing,
    execute_step3_patch_generation,
)

class StepWorkerPipeline:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.factory = AgentSessionFactory(root_dir)

    def run(self, mission_rel_path: str, max_retries: int = 3):
        print(f"\n🚀 [WORKER PIPELINE] 파이프라인 가동: '{mission_rel_path}'")
        
        mission_data = load_mission_file(self.root_dir, mission_rel_path)
        target_file_path = mission_data["target_file"]
        mission_str = json.dumps(mission_data, ensure_ascii=False, indent=2)

        # Step 1: 지형도 분석
        codebase_map = execute_step1_map_building(self.root_dir, self.factory, mission_data, target_file_path)

        # Step 2: 필요 영역 슬라이싱
        target_code = execute_step2_code_slicing(self.root_dir, self.factory, mission_data, target_file_path, codebase_map)

        # Step 3: 초기 패치 생성
        raw_response = execute_step3_patch_generation(self.factory, mission_data, target_file_path, target_code)

        # Step 4 ~ 6: 검증 및 자율 복구 루프
        retry_count = 0
        system_prompt = f"""STRICT EXECUTION PROTOCOL:
1. Target File: Strictly '{target_file_path}'.
2. Output code edits using EXACTLY the SEARCH/REPLACE block format shown below.
3. Include enough surrounding lines in SEARCH block to uniquely identify the code to change.
4. Keep exact whitespace/indentation.
5. Do NOT output JSON. Use raw SEARCH/REPLACE text blocks only. No markdown wrapped JSON, no explanations."""

        while retry_count <= max_retries:
            print(f"\n🛠️ [Step 4] CodePatcher 1:1 검증 및 치환 적용 (시도 {retry_count + 1}/{max_retries + 1})...")
            patch_success = False
            patch_list = []

            try:
                patch_list = self.factory.patcher.parse_blocks(raw_response)
                if patch_list:
                    all_patches_ok = True
                    for idx, item in enumerate(patch_list, 1):
                        existing_code = item["existing_code"]
                        replacement_code = item["replacement_code"]

                        patch_result = self.factory.patcher.apply_patch(target_file_path, existing_code, replacement_code)
                        print(f"📌 [PATCH RESULT {idx}/{len(patch_list)}] {patch_result['message']}")
                        print(f"   ├─ [BEFORE]: {existing_code.strip()[:60]}...")
                        print(f"   └─ [AFTER] : {replacement_code.strip()[:60]}...")
                        if not patch_result.get("success", False):
                            all_patches_ok = False
                    patch_success = all_patches_ok
                else:
                    print("⚠️ [PATCH FAIL] SEARCH/REPLACE 패치 블록이 비어 있거나 인식되지 않았습니다.")
            except Exception as e:
                print(f"❌ [STEP 4 ERROR] 패치 파싱 또는 적용 오류: {e}")

            # Step 5: 실행 및 로그 검증
            print("\n💻 [Step 5] DebugVerifier 실행 및 로그 패턴 검증 중...")
            diagnosis_hint = ""
            if patch_success:
                verifier = DebugVerifier(self.root_dir, self.factory)
                ver_res = verifier.verify(mission_data, target_file_path, target_code)

                is_verified = ver_res.get("verified", False)
                terminal_output = ver_res.get("output", "")
                diagnosis_hint = ver_res.get("message", "")

                print(f"📄 [VERIFICATION OUTPUT]\n{terminal_output}")
                print(f"📌 [VERIFICATION RESULT] {'검증 성공' if is_verified else '검증 실패'}: {diagnosis_hint}")
            else:
                is_verified = False
                terminal_output = "[PATCH FAIL] 패치 적용 실패로 인해 실행 검증을 스킵합니다."
                diagnosis_hint = "SEARCH/REPLACE 패치 블록 적용 실패"

            if patch_success and is_verified:
                created_temp_files = [
                    item.get("file_path") for item in patch_list 
                    if item.get("file_path") and item.get("file_path") != target_file_path 
                    and ("test" in item.get("file_path").lower() or "temp" in item.get("file_path").lower())
                ]
                for temp_file in created_temp_files:
                    temp_path = (self.root_dir / temp_file).resolve()
                    if temp_path.exists():
                        temp_path.unlink()
                        print(f"🧹 [CLEANUP] 검증 완료 후 임시 테스트 파일 삭제: {temp_file}")

                print("\n🎉 [SUCCESS] 모든 디버깅 로그 및 작업 검증 완료!")
                return

            retry_count += 1
            if retry_count > max_retries:
                print("\n🚨 [FAIL] 최대 재시도 횟수를 초과하여 작업을 중단합니다.")
                return

            # Step 6: 피드백 수집 및 복구 전략
            print(f"\n🩺 [Step 6-1] 검증 에이전트 진단 피드백 적용 (재시도 {retry_count}/{max_retries})...")
            
            if retry_count >= 2:
                print("⚠️ [강제 재탐색 발동] 2회 이상 실패 감지: LLM 자가 진단 생략 후 강제 broad 시야 확장(Retry Step 1)으로 전환합니다.")
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
                        self.factory,
                        prompt=diag_prompt,
                        system_instruction="STRICT PROTOCOL: Output raw JSON object with 'is_sufficient' boolean field only.",
                        response_mime_type="application/json"
                    )
                    diag_data = json.loads(clean_json_response(diag_res))
                    is_sufficient = diag_data.get("is_sufficient", False)
                except Exception:
                    is_sufficient = False

            if is_sufficient:
                print("🔄 [Step 6-2] 검증 에이전트 힌트 기반 다중 수정 패치 재작성 중...")
                fix_user_prompt = f"""<MISSION_SPEC>\n{mission_str}\n</MISSION_SPEC>
<READ_ONLY_CONTEXT>\n{target_code}\n</READ_ONLY_CONTEXT>
<PREVIOUS_FAILURE_LOG>\n{terminal_output}\n</PREVIOUS_FAILURE_LOG>
<VERIFIER_AGENT_DIAGNOSIS>\n{diagnosis_hint}\n</VERIFIER_AGENT_DIAGNOSIS>

Output corrected SEARCH/REPLACE blocks:
<<<<<<< SEARCH
[Exact original code snippet]
=======
[New replacement code snippet]
>>>>>>> REPLACE"""
                raw_response = safe_execute_step(
                    self.factory,
                    prompt=fix_user_prompt,
                    system_instruction=system_prompt,
                    response_mime_type="text/plain"
                )
            else:
                print("🌐 [Retry Step 1] 정보 부족 / 2회차 실패 -> 시야 확장 및 다중 경로 재탐색 진행...")
                scale_detector = ProjectScaleDetector(project_root=self.root_dir)
                shallow_map = scale_detector.generate_shallow_structure_map()
                
                broad_prompt = f"""Target File: {target_file_path}
Mission Data: {mission_str}
Project Structure: {shallow_map}
Previous Error Log: {terminal_output}

Select ALL relevant directory/file relative paths to inspect.
Output JSON string array matching: ["path/1", "path/2"]"""
                try:
                    raw_dirs = safe_execute_step(
                        self.factory,
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

                actual_target = self.root_dir / target_file_path
                if actual_target.exists():
                    with open(actual_target, "r", encoding="utf-8") as f:
                        total_lines = len(f.readlines())
                    dynamic_slice_prompt = f"{target_file_path}:1-{max(1, total_lines)}"
                else:
                    dynamic_slice_prompt = f"{target_file_path}:1-500"

                slice_res = self.factory.extractor.process(dynamic_slice_prompt, auto_save=False)
                target_code = slice_res.get("markdown", "")
                
                retry_fix_prompt = f"""<MISSION_SPEC>\n{mission_str}\n</MISSION_SPEC>
<READ_ONLY_CONTEXT>\n{target_code}\n</READ_ONLY_CONTEXT>
<PREVIOUS_FAILURE_LOG>\n{terminal_output}\n</PREVIOUS_FAILURE_LOG>
<VERIFIER_AGENT_DIAGNOSIS>\n{diagnosis_hint}\n</VERIFIER_AGENT_DIAGNOSIS>

Output corrected SEARCH/REPLACE blocks:
<<<<<<< SEARCH
[Exact original code snippet]
=======
[New replacement code snippet]
>>>>>>> REPLACE"""
                raw_response = safe_execute_step(
                    self.factory,
                    prompt=retry_fix_prompt,
                    system_instruction=system_prompt,
                    response_mime_type="text/plain"
                )