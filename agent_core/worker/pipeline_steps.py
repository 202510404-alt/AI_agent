import json
from pathlib import Path
from tools.multi_agent_system.project_scale_detector import ProjectScaleDetector
from tools.multi_agent_system.agent_map_extractor import extract_targeted_ai_map
from agent_core.worker.utils import safe_execute_step, clean_json_response

def execute_step1_map_building(root_dir: Path, factory, mission_data: dict, target_file_path: str) -> str:
    """[Step 1] 프로젝트 규모 진단 및 동적 지형도 생성"""
    print("\n🗺️ [Step 1] 프로젝트 규모 측정 및 코드베이스 맵 준비...")
    scale_detector = ProjectScaleDetector(project_root=root_dir)
    scale_info = scale_detector.analyze_project_scale()
    mission_str = json.dumps(mission_data, ensure_ascii=False, indent=2)

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
                factory,
                prompt=select_prompt,
                system_instruction=select_sys_instruction,
                response_mime_type="application/json"
            )
            target_dirs = json.loads(clean_json_response(raw_dirs))
            if not isinstance(target_dirs, list):
                target_dirs = [target_dirs]
                
            print(f"🎯 [Step 1 AI 선택 경로] {target_dirs}")
            return extract_targeted_ai_map(target_paths=target_dirs, save_to_file=False)
        except Exception as e:
            print(f"⚠️ [Step 1 Warning] AI 경로 선택 처리 중 예외 발생({e}), 전체 기본 맵으로 대체 진행")
            return extract_targeted_ai_map(save_to_file=False)
    else:
        print("✅ 일반 규모 프로젝트: AI 호출 없이 전체 AI 코드베이스 맵 direct 생성")
        return extract_targeted_ai_map(save_to_file=True)


def execute_step2_code_slicing(root_dir: Path, factory, mission_data: dict, target_file_path: str, codebase_map: str) -> str:
    """[Step 2] 미션 기반 동적 필요 코드 영역 추론 및 추출"""
    print("\n📄 [Step 2] 미션 및 지형도 맵 기반 필요 코드 영역 동적 추출...")
    mission_str = json.dumps(mission_data, ensure_ascii=False, indent=2)
    
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
            factory,
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

        if not target_code.strip():
            target_code = fallback_extract_full_target(root_dir, factory, target_file_path)
    except Exception as e:
        print(f"⚠️ [Step 2 Warning] 필요 코드 영역 동적 추출 예외 발생({e}), Fallback 전체 파일 추적 시도")
        target_code = fallback_extract_full_target(root_dir, factory, target_file_path)

    print(f"📄 [Step 2 준비 완료] 추출된 코드 영역 길이: {len(target_code)}자")
    return target_code


def fallback_extract_full_target(root_dir: Path, factory, target_file_path: str) -> str:
    """Target File 전체 범위를 재추적하는 Fallback 함수"""
    actual_target = root_dir / target_file_path
    if actual_target.exists():
        with open(actual_target, "r", encoding="utf-8") as f:
            total_lines = len(f.readlines())
        fallback_prompt = f"{target_file_path}:1-{max(1, total_lines)}"
        print(f"⚠️ [Step 2 Fallback] Target File 전체 범위({fallback_prompt})로 Extractor 재추적 가동")
        slice_res = factory.extractor.process(fallback_prompt, auto_save=False)
        return slice_res.get("markdown", "")
    return "(Target File을 찾을 수 없어 코드 추출에 실패했습니다.)"


def execute_step3_patch_generation(factory, mission_data: dict, target_file_path: str, target_code: str) -> str:
    """[Step 3] LLM 단발성 수정 패치 생성 요청"""
    print("\n🤖 [Step 3] LLM 단발성 수정 패치(다중 스니펫) 생성 중...")
    mission_str = json.dumps(mission_data, ensure_ascii=False, indent=2)

    system_prompt = f"""STRICT EXECUTION PROTOCOL:
1. Target File: Strictly '{target_file_path}'.
2. Output code edits using EXACTLY the SEARCH/REPLACE block format shown below.
3. Include enough surrounding lines in SEARCH block to uniquely identify the code to change.
4. Keep exact whitespace/indentation.
5. Do NOT output JSON. Use raw SEARCH/REPLACE text blocks only. No markdown wrapped JSON, no explanations."""

    user_prompt = f"""<MISSION_SPEC>
Target File Path: {target_file_path}
Mission Details:
{mission_str}
</MISSION_SPEC>

<READ_ONLY_CONTEXT>
{target_code}
</READ_ONLY_CONTEXT>

<OUTPUT_FORMAT>
For each code change, output exactly:

<<<<<<< SEARCH
[Exact original code snippet to replace]
=======
[New replacement code snippet]
>>>>>>> REPLACE
</OUTPUT_FORMAT>"""

    return safe_execute_step(
        factory,
        prompt=user_prompt,
        system_instruction=system_prompt,
        response_mime_type="text/plain"
    )