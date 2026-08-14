"""
agent_core/debug_agent/runner.py
----------------------------------
Debug Agent 핵심 실행 파이프라인 엔진
"""

from pathlib import Path
from agent_core.plan.schemas import LOG_FILE_PATH
from tools.multi_agent_system.agent_session import AgentSessionFactory
from agent_core.debug_agent.verifier import DebugVerifier
from agent_core.debug_agent.pipeline.context_builder import build_codebase_map, extract_target_code
from agent_core.debug_agent.pipeline.mission_loader import load_mission_file
from agent_core.debug_agent.pipeline.patch_runner import generate_patch, apply_patch_blocks, cleanup_temp_files
from agent_core.debug_agent.pipeline.recovery_strategy import evaluate_and_recover


def run_debug_pipeline(root_dir: Path, mission_rel_path: str, max_retries: int = 3) -> bool:
    """디버그 에이전트 메인 실행 엔진"""
    print(f"\n🚀 [DEBUG WORKER PIPELINE] 가동 시작: '{mission_rel_path}'")
    
    if LOG_FILE_PATH.exists():
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            f.write("=== [Debug Agent Pipeline Log Initialized] ===\n")

    factory = AgentSessionFactory(root_dir)
    mission_data = load_mission_file(root_dir, mission_rel_path)
    target_file_path = mission_data["target_file"]

    # 1. Context Build
    codebase_map = build_codebase_map(root_dir, factory, mission_data)
    target_code = extract_target_code(root_dir, factory, mission_data, codebase_map)

    # 2. Patch Generation
    raw_response = generate_patch(factory, mission_data, target_code)

    # 3. Apply, Verify & Self-Healing Loop
    retry_count = 0
    while retry_count <= max_retries:
        print(f"\n🛠️ [Step 4] 패치 검증 및 적용 (시도 {retry_count + 1}/{max_retries + 1})...")
        patch_success, patch_list = apply_patch_blocks(factory, target_file_path, raw_response)

        # Step 5: Verification
        terminal_output = ""
        diagnosis_hint = ""
        if patch_success:
            verifier = DebugVerifier(root_dir, factory)
            ver_res = verifier.verify(mission_data, target_file_path, target_code)
            is_verified = ver_res.get("verified", False)
            terminal_output = ver_res.get("output", "")
            diagnosis_hint = ver_res.get("message", "")
        else:
            is_verified = False
            terminal_output = "[PATCH FAIL] 패치 적용 실패로 실행 검증 스킵"
            diagnosis_hint = "SEARCH/REPLACE 패치 블록 적용 실패"

        print(f"📄 [VERIFICATION OUTPUT]\n{terminal_output}")
        print(f"📌 [RESULT] {'성공' if is_verified else '실패'}: {diagnosis_hint}")

        if patch_success and is_verified:
            cleanup_temp_files(root_dir, patch_list, target_file_path)
            print("\n🎉 [SUCCESS] 미션 수행 및 디버그 검증 성공!")
            return True

        retry_count += 1
        if retry_count > max_retries:
            print("\n🚨 [FAIL] 최대 재시도 횟수를 초과하였습니다.")
            return False

        # Step 6: Recovery
        print(f"\n🩺 [Step 6] 실패 진단 및 피드백 적용 중 (재시도 {retry_count}/{max_retries})...")
        raw_response, target_code = evaluate_and_recover(
            root_dir, factory, mission_data, target_code, terminal_output, diagnosis_hint, retry_count
        )

    return False