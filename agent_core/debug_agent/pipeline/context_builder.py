"""
agent_core/pipeline/context_builder.py
---------------------------------------
Step 1 & Step 2: 프로젝트 지형도 파악 및 코드 영역 추출 모듈
"""

import json
from pathlib import Path
from tools.multi_agent_system.project_scale_detector import ProjectScaleDetector
from tools.multi_agent_system.agent_map_extractor import extract_targeted_ai_map
from agent_core.debug_agent.pipeline.mission_loader import safe_execute_step, clean_json_response

def build_codebase_map(root_dir: Path, factory, mission_data: dict) -> str:
    """[Step 1] 프로젝트 규모 측정 및 코드베이스 지형도 생성"""
    target_file_path = mission_data["target_file"]
    mission_str = json.dumps(mission_data, ensure_ascii=False, indent=2)

    scale_detector = ProjectScaleDetector(project_root=root_dir)
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
            raw_dirs = safe_execute_step(factory, prompt=select_prompt, system_instruction=select_sys_instruction)
            target_dirs = json.loads(clean_json_response(raw_dirs))
            if not isinstance(target_dirs, list):
                target_dirs = [target_dirs]
            print(f"🎯 [Step 1 AI 선택 경로] {target_dirs}")
            return extract_targeted_ai_map(target_paths=target_dirs, save_to_file=False)
        except Exception as e:
            print(f"⚠️ [Step 1 Warning] AI 경로 선택 중 예외({e}), 전체 기본 맵으로 대체")
            return extract_targeted_ai_map(save_to_file=False)
    else:
        print("✅ 일반 규모 프로젝트: 전체 AI 코드베이스 맵 생성")
        return extract_targeted_ai_map(save_to_file=True)

def extract_target_code(root_dir: Path, factory, mission_data: dict, codebase_map: str) -> str:
    """[Step 2] 필요 코드 영역 동적 추론 및 Extractor 구동"""
    target_file_path = mission_data["target_file"]
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

[3. REQUIRED FORMAT]
["{target_file_path}:start_line-end_line"]"""

    try:
        raw_slice_targets = safe_execute_step(
            factory, prompt=extract_target_prompt, system_instruction=extract_sys_instruction
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
            target_code = _fallback_full_extract(root_dir, factory, target_file_path)
    except Exception as e:
        print(f"⚠️ [Step 2 Warning] 필요 코드 영역 추출 예외 발생({e}), Fallback 추적 시도")
        target_code = _fallback_full_extract(root_dir, factory, target_file_path)

    return target_code

def _fallback_full_extract(root_dir: Path, factory, target_file_path: str) -> str:
    actual_target = root_dir / target_file_path
    if actual_target.exists():
        with open(actual_target, "r", encoding="utf-8") as f:
            total_lines = len(f.readlines())
        fallback_prompt = f"{target_file_path}:1-{max(1, total_lines)}"
        print(f"⚠️ [Fallback] Target File 전체 범위({fallback_prompt})로 Extractor 재추적 가동")
        slice_res = factory.extractor.process(fallback_prompt, auto_save=False)
        return slice_res.get("markdown", "")
    return "(Target File을 찾을 수 없어 코드 추출에 실패했습니다.)"