"""
tools/multi_agent_system/agent_session.py
프로젝트 규모를 자동 진단하여 '전체 맵 모드' 또는 'AI 범위 선택 모드'로 세션을 가동합니다.
"""

import os
from pathlib import Path
from agent_core.plan.gemini_client import load_env_file, HAS_GENAI
from tools.multi_agent_system.agent_code_extractor import CodeExtractor
from tools.multi_agent_system.terminal_runner import run_terminal_command
from tools.multi_agent_system.code_patcher import CodePatcher
from tools.multi_agent_system.agent_map_extractor import extract_targeted_ai_map
from tools.multi_agent_system.project_scale_detector import ProjectScaleDetector

if HAS_GENAI:
    from google import genai
    from google.genai import types


class AgentSessionFactory:
    """AI 에이전트 생성 및 도구 바인딩 팩토리"""
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir.resolve()
        load_env_file(self.root_dir / ".env")
        
        self.extractor = CodeExtractor(self.root_dir)
        self.patcher = CodePatcher(self.root_dir)
        target_scan_dir = self.root_dir / "extraction_target_project" if (self.root_dir / "extraction_target_project").exists() else self.root_dir

        self.scale_detector = ProjectScaleDetector(
            project_root=target_scan_dir
        )
        self.client = None

    def _prepare_codebase_map(self, max_shallow_depth: int = 3) -> tuple[str, bool]:
        """
        규모 진단 후 (맵 텍스트, oversized 여부) 튜플을 반환합니다.
        """
        scan_target = self.root_dir / "extraction_target_project"
        target_dir = scan_target if scan_target.exists() else self.root_dir

        metrics = self.scale_detector.analyze_project_scale(target_dir=target_dir)

        if metrics["is_oversized"]:
            print(f"⚠️ [PROJECT SCALE] 감당 불가 프로젝트 감지! (파일 {metrics['file_count']}개, {metrics['total_lines']}줄)")
            print(f"🔍 상위 {max_shallow_depth}단계 얕은 겉핥기 지도를 생성합니다...")
            shallow_map = self.scale_detector.generate_shallow_structure_map(
                max_depth=max_shallow_depth, 
                target_dir=target_dir
            )
            return shallow_map, True
        else:
            print(f"✅ [PROJECT SCALE] 감당 가능한 적정 규모 프로젝트 (파일 {metrics['file_count']}개, {metrics['total_lines']}줄)")
            # 적정 규모일 경우 대상 폴더 전체 추출
            target_rel_path = "extraction_target_project" if scan_target.exists() else "."
            full_map = extract_targeted_ai_map(target_paths=[target_rel_path], save_to_file=True)
            return full_map, False

    def _build_tools(self):
        """AI에게 전달할 Tool 패키징"""
        def extract_code_slice(file_and_line: str) -> str:
            """특정 파일 및 라인 범위의 코드 슬라이스를 추출합니다."""
            res = self.extractor.process(file_and_line, auto_save=False)
            return res["markdown"] if res["markdown"] else "❌ 해당 코드를 찾을 수 없습니다."

        def patch_code_slice(file_path: str, existing_code: str, replacement_code: str) -> str:
            """파일 내 특정 '기존 코드'를 '수정된 코드'로 1:1 치환합니다."""
            res = self.patcher.apply_patch(file_path, existing_code, replacement_code)
            return res["message"]

        def get_targeted_codebase_map(target_paths: list[str]) -> str:
            """
            [규모 초과 시 사용] 특정 폴더/파일 경로 목록을 전달받아 해당 구역의 정밀 AI 코드베이스 맵을 생성하여 반환합니다.
            예: target_paths = ["extraction_target_project/src/controller", "extraction_target_project/src/models"]
            """
            print(f"\n🗺️ [TOOL EXECUTION] AI가 특정 구간 타깃 맵을 요청함: {target_paths}")
            return extract_targeted_ai_map(target_paths=target_paths, save_to_file=False)

        return [extract_code_slice, run_terminal_command, patch_code_slice, get_targeted_codebase_map]

    def create_chat_session(self, model_name: str = "gemini-2.5-flash", shallow_depth: int = 3):
        """모든 지형도와 도구가 준비된 Gemini Chat 세션을 생성합니다."""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not HAS_GENAI or not api_key:
            raise RuntimeError("Google GenAI 패키지 미설치 또는 API Key가 설정되지 않았습니다.")

        self.client = genai.Client(api_key=api_key)
        codebase_map, is_oversized = self._prepare_codebase_map(max_shallow_depth=shallow_depth)
        tools = self._build_tools()

        oversized_guideline = """
[🚨 주의: 방대한 프로젝트 감지됨]
현재 제공된 지도는 프로젝트의 상위 겉핥기 개요 지도입니다.
작업을 진행하기 전, 분석이나 수정을 진행할 구체적인 폴더 경로를 파악하고 
반드시 `get_targeted_codebase_map(target_paths=["상세경로"])` 도구를 호출하여 
필요한 구역의 정밀 세부 맵을 확보한 후 작업을 수행하십시오.
""" if is_oversized else ""

        system_instruction = f"""
당신은 현재 프로젝트의 코드베이스 구조를 파악하고, 터미널 명령어로 디버깅하며 코드를 정밀 수정하는 AI 에이전트입니다.

[프로젝트 코드베이스 지도]
{codebase_map}
{oversized_guideline}
[사용 가능한 도구]
1. `extract_code_slice("파일경로:시작줄-끝줄")`: 코드의 실제 내용을 확인합니다.
2. `run_terminal_command("명령어")`: 터미널 명령어(테스트 등)를 구동하고 로그를 확인합니다.
3. `patch_code_slice(file_path, existing_code, replacement_code)`: 특정 코드 구간을 1:1 치환합니다.
4. `get_targeted_codebase_map(target_paths=["경로1", "경로2"])`: 지정한 폴더/파일 하위의 정밀 심볼 및 관계망 맵을 새로 가져옵니다.

[🚨 절대 규칙 - 코드 수정 수칙]
1. 절대로 파일 전체 코드를 작성하거나 덮어쓰지 마십시오.
2. 코드를 수정할 때는 반드시 `extract_code_slice`로 확인 후 `patch_code_slice`를 사용하십시오.
3. `existing_code`는 기존 코드와 공백/줄바꿈 포함 100% 토씨 하나 안 틀리고 일치해야 합니다.
"""

        chat = self.client.chats.create(
            model=model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=tools,
                temperature=0.2,
            )
        )
        return chat