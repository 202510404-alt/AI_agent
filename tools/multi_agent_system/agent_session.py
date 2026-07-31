"""
tools/multi_agent_system/agent_session.py
코드베이스 지도를 로드하고 Tool들을 바인딩하여 완전히 준비된 AI Chat 세션을 생성하는 모듈
"""

import os
from pathlib import Path
from agent_core.plan.gemini_client import load_env_file, HAS_GENAI
from tools.multi_agent_system.agent_code_extractor import CodeExtractor
from tools.multi_agent_system.terminal_runner import run_terminal_command
from tools.multi_agent_system.code_patcher import CodePatcher

if HAS_GENAI:
    from google import genai
    from google.genai import types


class AgentSessionFactory:
    """AI 에이전트 생성 및 도구 바인딩 팩토리"""
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir.resolve()
        load_env_file(self.root_dir / ".env")
        
        # 1. 사용 도구 인스턴스화
        self.extractor = CodeExtractor(self.root_dir)
        self.patcher = CodePatcher(self.root_dir)
        self.client = None

    def _load_codebase_map(self) -> str:
        """코드베이스 지도 탐색 및 로드"""
        map_path = self.root_dir / "system_maps" / "AI_CODEBASE_MAP.md"
        if not map_path.exists():
            map_path = self.root_dir / "AI_CODEBASE_MAP.md"

        if map_path.exists():
            return map_path.read_text(encoding="utf-8")
        return "[안내] 코드베이스 지도를 찾을 수 없습니다."

    def _build_tools(self):
        """AI에게 전달할 Tool 함수 패키징"""
        def extract_code_slice(file_and_line: str) -> str:
            """특정 파일 및 라인 범위의 코드 슬라이스를 추출합니다."""
            print(f"\n⚙️ [TOOL] 'extract_code_slice' Target: {file_and_line}")
            res = self.extractor.process(file_and_line, auto_save=False)
            return res["markdown"] if res["markdown"] else "❌ 해당 코드를 찾을 수 없습니다."

        def patch_code_slice(file_path: str, existing_code: str, replacement_code: str) -> str:
            """파일 내 특정 '기존 코드'를 '수정된 코드'로 1:1 치환합니다."""
            print(f"\n🛠️ [TOOL] 'patch_code_slice' Target: {file_path}")
            res = self.patcher.apply_patch(file_path, existing_code, replacement_code)
            print(res["message"])
            return res["message"]

        return [extract_code_slice, run_terminal_command, patch_code_slice]

    def create_chat_session(self, model_name: str = "gemini-2.5-flash"):
        """모든 지형도와 도구가 준비된 Gemini Chat 세션을 '구워서' 반환합니다."""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not HAS_GENAI or not api_key:
            raise RuntimeError("Google GenAI 패키지 미설치 또는 API Key가 설정되지 않았습니다.")

        self.client = genai.Client(api_key=api_key)
        codebase_map = self._load_codebase_map()
        tools = self._build_tools()

        system_instruction = f"""
당신은 현재 프로젝트의 코드베이스 구조를 파악하고, 터미널 명령어로 디버깅하며 코드를 정밀 수정하는 AI 에이전트입니다.

[프로젝트 코드베이스 지도 (AI_CODEBASE_MAP)]
{codebase_map}

[사용 가능한 도구]
1. `extract_code_slice("파일경로:시작줄-끝줄")`: 코드의 실제 내용을 확인합니다.
2. `run_terminal_command("명령어")`: 터미널 명령어(테스트 등)를 구동하고 로그를 확인합니다.
3. `patch_code_slice(file_path, existing_code, replacement_code)`: 특정 코드 구간을 1:1 치환합니다.

[🚨 절대 규칙 - 코드 수정 수칙]
1. 절대로 파일 전체 코드를 작성하거나 덮어쓰지 마십시오.
2. 코드를 수정할 때는 반드시 `extract_code_slice`로 확인 후 `patch_code_slice`를 사용하십시오.
3. `existing_code`는 기존 코드와 **공백/줄바꿈 포함 100% 토씨 하나 안 틀리고 일치**해야 합니다.
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