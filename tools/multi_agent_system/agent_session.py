"""
tools/multi_agent_system/agent_session.py
프로젝트 규모를 자동 진단하여 '전체 맵 모드' 또는 'AI 범위 선택 모드'로 세션을 가동합니다.
"""

import os
from pathlib import Path
from typing import Optional  # <-- 필수 import 추가
from agent_core.plan.gemini_client import load_env_file, HAS_GENAI
from tools.multi_agent_system.agent_code_extractor import CodeExtractor
from tools.multi_agent_system.terminal_runner import run_terminal_command
from tools.multi_agent_system.code_patcher import CodePatcher
from tools.multi_agent_system.agent_map_extractor import extract_targeted_ai_map
from tools.multi_agent_system.project_scale_detector import ProjectScaleDetector

if HAS_GENAI:
    from google import genai
    from google.genai import types

class KeyManager:
    """env에 등록된 모든 GEMINI_API_KEY 계열 키들을 번호 유무와 상관없이 동적 완전 수집 (상세 디버깅 강화)"""
    def __init__(self, env_path: Path = None):
        self.keys = []
        
        # .env 탐색 (전달받은 경로 -> 현재 작업 디렉토리 -> 상위 디렉토리 추적)
        possible_paths = [
            env_path,
            Path.cwd() / ".env",
            Path(__file__).resolve().parent.parent.parent / ".env"
        ]
        
        target_env = None
        for p in possible_paths:
            print(f"🔍 [.ENV DIAGNOSTIC] 경로 검사 중: {p} (존재 여부: {p.exists() if p else False})")
            if p and p.exists():
                target_env = p
                break

        if target_env and target_env.exists():
            print(f"✅ [.ENV DIAGNOSTIC] 타겟 .env 타깃 매핑 완료: {target_env}")
            try:
                line_count = 0
                matched_count = 0
                with open(target_env, "r", encoding="utf-8") as f:
                    for line in f:
                        line_count += 1
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k.startswith("GEMINI_API_KEY"):
                            matched_count += 1
                            print(f"   └─ 🔑 감지된 변수: '{k}' (값 길이: {len(v)}자)")
                            os.environ[k] = v
                            if v and v not in self.keys:
                                self.keys.append(v)
                print(f"📊 [.ENV DIAGNOSTIC] 읽은 총 라인: {line_count}줄 / 'GEMINI_API_KEY' 매칭: {matched_count}개")
            except Exception as e:
                print(f"⚠️ [.env 파싱 실패]: {e}")
        else:
            print("❌ [.ENV DIAGNOSTIC] 유효한 .env 파일을 찾지 못했습니다!")

        # os.environ에 이미 로드되어 있던 키들도 2차 통합 수집 (GEMINI_API_KEY, GEMINI_API_KEY1~50, GEMINI_API_KEY_1~50)
        base_key = os.environ.get("GEMINI_API_KEY")
        if base_key and base_key not in self.keys:
            self.keys.append(base_key)
        
        for i in range(1, 51):
            key_no_underscore = os.environ.get(f"GEMINI_API_KEY{i}")
            if key_no_underscore and key_no_underscore not in self.keys:
                self.keys.append(key_no_underscore)
                
            key_with_underscore = os.environ.get(f"GEMINI_API_KEY_{i}")
            if key_with_underscore and key_with_underscore not in self.keys:
                self.keys.append(key_with_underscore)

        self.current_index = 0
        print(f"🔑 [KEY MANAGER] 총 {len(self.keys)}개의 Gemini API Key가 성공적으로 로드되었습니다.")

    def get_current_key(self) -> str:
        if not self.keys:
            return None
        return self.keys[self.current_index]

    def rotate_key(self) -> str:
        """다음 API 키로 교체"""
        if not self.keys:
            return None
        self.current_index = (self.current_index + 1) % len(self.keys)
        print(f"🔄 [KEY ROTATION] API 키 변경됨! (현재 Key 번호: {self.current_index + 1}/{len(self.keys)})")
        return self.get_current_key()

class AgentSessionFactory:
    """AI 에이전트 생성 및 도구 바인딩 팩토리"""
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir.resolve()
        load_env_file(self.root_dir / ".env")
        
        # 💡 객체 생성 시점에 KeyManager를 미리 초기화하여 속성을 생성합니다.
        self.key_manager = KeyManager(env_path=self.root_dir / ".env")
        
        self.extractor = CodeExtractor(self.root_dir)
        self.patcher = CodePatcher(self.root_dir)
        target_scan_dir = self.root_dir / "extraction_target_project" if (self.root_dir / "extraction_target_project").exists() else self.root_dir

        self.scale_detector = ProjectScaleDetector(
            project_root=target_scan_dir
        )
        self.client = None

    def prepare_step1_map(self, max_shallow_depth: int = 3) -> tuple[str, bool]:
        """
        [Step 1 인터페이스] 프로젝트 규모를 진단하고 (맵 텍스트, oversized 여부) 튜플을 반환합니다.
        """
        scan_target = self.root_dir / "extraction_target_project"
        target_dir = scan_target if scan_target.exists() else self.root_dir

        metrics = self.scale_detector.analyze_project_scale(target_dir=target_dir)
        effective_depth = metrics.get("recommended_depth", max_shallow_depth)

        if metrics["is_oversized"]:
            print(f"⚠️ [PROJECT SCALE] 대규모 프로젝트 감지! (유효 코드 파일 {metrics['file_count']}개, {metrics['total_lines']}줄)")
            print(f"🔍 동적 Depth({effective_depth}단계) 겉핥기 지도를 생성합니다...")
            shallow_map = self.scale_detector.generate_shallow_structure_map(
                max_depth=effective_depth, 
                target_dir=target_dir
            )
            return shallow_map, True
        else:
            print(f"✅ [PROJECT SCALE] 적정 규모 프로젝트 (유효 코드 파일 {metrics['file_count']}개, {metrics['total_lines']}줄)")
            target_rel_path = "extraction_target_project" if scan_target.exists() else "."
            full_map = extract_targeted_ai_map(target_paths=[target_rel_path], save_to_file=True)
            return full_map, False


    def execute_worker_step(self, prompt: str, system_instruction: str, response_mime_type: str = "application/json", max_retries: int = 5) -> str:
        """
        [Step 3 인터페이스] 단발성 LLM 요청을 수행합니다. (429 Quota 초과 시 API Key 자동 Rotate 처리)
        """
        if not HAS_GENAI:
            raise RuntimeError("Google GenAI 패키지가 설치되지 않았습니다.")

        from agent_core.plan.gemini_client import resolve_best_gemini_model

        for attempt in range(1, max_retries + 1):
            current_api_key = self.key_manager.get_current_key()
            if not current_api_key:
                raise RuntimeError(".env에 등록된 유효한 GEMINI_API_KEY가 없습니다.")

            try:
                self.client = genai.Client(api_key=current_api_key)
                target_model = resolve_best_gemini_model(self.client)

                response = self.client.models.generate_content(
                    model=target_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        response_mime_type=response_mime_type,
                        temperature=0.1
                    )
                )
                return response.text

            except Exception as e:
                err_msg = str(e)
                # 1. 429 쿼터 초과 -> Key Rotate 후 즉시 재시도
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    print(f"⚠️ [API 429 EXHAUSTED] Key 번호 {self.key_manager.current_index + 1} 쿼터 초과. 다음 Key로 교체합니다... ({attempt}/{max_retries})")
                    self.key_manager.rotate_key()
                    continue

                # 2. 503 서버 과부하 -> Key Rotate + 대기
                elif "503" in err_msg or "UNAVAILABLE" in err_msg:
                    import time
                    wait_sec = 2 * attempt
                    print(f"⚠️ [API 503 UNAVAILABLE] 서버 과부하 발생! Key 교체 후 {wait_sec}초 대기... ({attempt}/{max_retries})")
                    self.key_manager.rotate_key()
                    time.sleep(wait_sec)
                    continue

                else:
                    raise e

        raise RuntimeError("모든 GEMINI_API_KEY의 쿼터가 소진되었거나 요청 실패했습니다.")

    def _build_tools(self):
        """AI에게 전달할 Tool 패키징 (RPM 폭주 방지 딜레이 포함)"""
        import time

        def extract_code_slice(file_and_line: str) -> str:
            """특정 파일 및 라인 범위의 코드 슬라이스를 추출합니다."""
            time.sleep(2)  # ⏱️ Rate Limit(RPM) 방어 딜레이
            res = self.extractor.process(file_and_line, auto_save=False)
            return res["markdown"] if res["markdown"] else "❌ 해당 코드를 찾을 수 없습니다."

        def patch_code_slice(file_path: str, existing_code: str, replacement_code: str) -> str:
            """파일 내 특정 '기존 코드'를 '수정된 코드'로 1:1 치환합니다."""
            time.sleep(2)  # ⏱️ Rate Limit(RPM) 방어 딜레이
            res = self.patcher.apply_patch(file_path, existing_code, replacement_code)
            return res["message"]

        def get_targeted_codebase_map(target_paths: list[str]) -> str:
            """
            [규모 초과 시 사용] 특정 폴더/파일 경로 목록을 전달받아 해당 구역의 정밀 AI 코드베이스 맵을 생성하여 반환합니다.
            예: target_paths = ["extraction_target_project/src/controller", "extraction_target_project/src/models"]
            """
            time.sleep(2)  # ⏱️ Rate Limit(RPM) 방어 딜레이
            print(f"\n🗺️ [TOOL EXECUTION] AI가 특정 구간 타깃 맵을 요청함: {target_paths}")
            return extract_targeted_ai_map(target_paths=target_paths, save_to_file=False)

        # terminal_runner 래핑
        def safe_run_terminal_command(command: str) -> str:
            """터미널 명령어를 실행합니다."""
            time.sleep(2)  # ⏱️ Rate Limit(RPM) 방어 딜레이
            return run_terminal_command(command)

        return [extract_code_slice, safe_run_terminal_command, patch_code_slice, get_targeted_codebase_map]

    def create_chat_session(self, model_name: Optional[str] = None, shallow_depth: int = 3):
        """동적으로 사용 가능한 모델을 선별하여 지형도와 도구가 준비된 Gemini Chat 세션을 생성합니다."""
        current_api_key = self.key_manager.get_current_key()

        if not HAS_GENAI or not current_api_key:
            raise RuntimeError("Google GenAI 패키지 미설치 또는 .env에 등록된 GEMINI_API_KEY가 없습니다.")

        self.client = genai.Client(api_key=current_api_key)

        # 하드코딩 매핑 제거 -> 전체 사용 가능한 모델 중 최적 모델을 동적으로 추출
        target_model = model_name
        if not target_model:
            from agent_core.plan.gemini_client import resolve_best_gemini_model
            target_model = resolve_best_gemini_model(self.client)

        self.current_model = target_model  # 💡 디버깅용 모델 저장
        print(f"🤖 [SESSION MODEL] Chat 세션 가동 모델: {target_model}")

        codebase_map, is_oversized = self._prepare_codebase_map(max_shallow_depth=shallow_depth)
        tools = self._build_tools()

        oversized_guideline = """
[🚨 주의: 방대한 프로젝트 감지됨]
현재 제공된 지도는 프로젝트의 상위 겉핥기 개요 지도입니다.
작업을 진행하기 전, 분석이나 수정을 진행할 구체적인 폴더 경로를 파악하고 
반드시 `get_targeted_codebase_map(target_paths=["상세경로"])` 도구를 호출하여 
필요한 구역의 정밀 세부 맵을 확보한 후 작업을 수행하십시오.
""" if is_oversized else ""

        # tools/multi_agent_system/agent_session.py 수정 구간

        system_instruction = f"""
당신은 현재 프로젝트의 코드베이스 구조를 파악하고, 터미널 명령어로 디버깅하며 코드를 정밀 수정하는 AI 에이전트입니다.

[프로젝트 코드베이스 지도]
{codebase_map}
{oversized_guideline}

[사용 가능한 도구]
1. `extract_code_slice("파일경로:시작줄-끝줄")`: 코드의 실제 내용을 확인합니다.
2. `run_terminal_command("명령어")`: 터미널 명령어(dir, find, pytest 등)를 구동합니다.
3. `patch_code_slice(file_path, existing_code, replacement_code)`: 특정 코드 구간을 1:1 치환합니다.
4. `get_targeted_codebase_map(target_paths=["경로1"])`: 지정한 폴더/파일의 정밀 맵을 가져옵니다.

[🚨 절대 규칙 - 검색 및 도구 호출 수칙]
1. 지상 지도에 요구된 파일이 명확히 보이지 않거나 오타가 의심될 경우, 추측하여 "없다"고 답변하지 말고 즉시 `run_terminal_command`로 디렉토리를 직접 검색(예: dir /s /b)하여 실체 경로를 확인하십시오.
2. 파일 전체 수정 요구 시, 함부로 통째로 덮어쓰지 말고 `extract_code_slice` 및 `patch_code_slice`를 조합하여 작업을 수행하십시오.
"""

        # Tool call 설정을 필요에 맞춰 AUTO 또는 사용자 지정 조건으로 변경
        tool_config_dict = {
            "function_calling_config": {
                "mode": "AUTO"  # 필요 시 도구를 선택적으로 호출할 수 있도록 AUTO로 변경
            }
        }

        chat = self.client.chats.create(
            model=target_model,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=tools,
                temperature=0.2,
                tool_config=tool_config_dict
            )
        )
        
        return chat