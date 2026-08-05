"""
agent_core/plan/gemini_client.py
.env 파일 및 환경변수에서 GEMINI_API_KEY를 자동으로 로드하여 Google Gemini API와 통신하는 모듈
"""

import os
import re
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any
from agent_core.plan.schemas import DEBUG_MODE, LOG_FILE_PATH

# Google GenAI 공식 라이브러리 연동 시도
try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


def log_debug(message_func):
    """DEBUG_MODE가 False일 때는 성능 저하를 방지하기 위해 로그 연산을 차단합니다."""
    if not DEBUG_MODE:
        return
    msg = message_func() if callable(message_func) else message_func
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"[GEMINI_CLIENT DEBUG] {msg}\n")
    except Exception:
        pass


def load_env_file(env_path: Path) -> None:
    """
    python-dotenv가 없어도 .env 파일에서 GEMINI_API_KEY를 직접 읽어서 os.environ에 주입합니다.
    """
    if not env_path.exists():
        if DEBUG_MODE:
            log_debug(lambda: f".env 파일을 찾을 수 없습니다: {env_path}")
        return

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("'\"")  # 따옴표 제거
                    if key and not os.environ.get(key):
                        os.environ[key] = value
        if DEBUG_MODE:
            log_debug(lambda: f".env 파일 로드 성공: {env_path}")
    except Exception as e:
        if DEBUG_MODE:
            log_debug(lambda: f".env 파일 파싱 중 예외 발생: {e}")


class GeminiPlannerClient:
    def __init__(self, api_key: Optional[str] = None, root_dir: Optional[Path] = None):
        # 1. 루트 경로 지정 및 .env 선제 자동 로드
        self.root_dir = root_dir or Path.cwd()
        env_file = self.root_dir / ".env"
        load_env_file(env_file)

        # 2. API Key 확보 (인자값 -> os.environ)
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = None
        
        if DEBUG_MODE:
            log_debug(lambda: f"GeminiPlannerClient 초기화 - API Key 존재 여부: {bool(self.api_key)}")

        if not HAS_GENAI:
            if DEBUG_MODE:
                log_debug(lambda: "[경고] 'google-genai' 패키지가 없습니다. 'pip install google-genai'가 필요합니다.")
            return

        if self.api_key:
            try:
                # 공식 SDK 클라이언트 초기화
                self.client = genai.Client(api_key=self.api_key)
                if DEBUG_MODE:
                    log_debug(lambda: "Google GenAI Client (API 키 연결) 초기화 완")
            except Exception as e:
                if DEBUG_MODE:
                    log_debug(lambda: f"Google GenAI Client 초기화 실패: {e}")

    def generate_plan(self, prompt: str, model_name: str = "gemini-2.5-flash", max_retries: int = 3) -> Dict[str, Any]:
        """
        Gemini 모델에 프롬프트를 전달하고 구조화된 응답(JSON)을 추출합니다. (429 처리 자동 재시도 포함)
        """
        if DEBUG_MODE:
            log_debug(lambda: f"generate_plan 호출 - 모델: {model_name}, 프롬프트 길이: {len(prompt)}자")

        # API 통신 환경 미구축 시 안전한 Mock 응답 반환
        if not self.client or not HAS_GENAI:
            if DEBUG_MODE:
                log_debug(lambda: "[안내] API 클라이언트 미활성화로 MOCK 플랜 데이터를 반환합니다.")
            
            return {
                "status": "success",
                "mode": "mock",
                "tasks": [
                    {
                        "task_id": "task_1",
                        "description": "MOCK: 인증 서비스에 로그인 실패 제한 로직 추가",
                        "target_files": ["auth/service.py"],
                        "read_symbols": [{"file_path": "auth/service.py", "symbol_name": "login_user", "start_line": 15, "end_line": 42}],
                        "write_symbols": [{"file_path": "auth/service.py", "symbol_name": "login_user", "start_line": 15, "end_line": 42}],
                        "dependencies": []
                    }
                ]
            }

        # ✅ [핵심 개선] 429 RESOURCE_EXHAUSTED 감지 및 자동 재시도 Loop
        for attempt in range(1, max_retries + 1):
            try:
                if DEBUG_MODE:
                    log_debug(lambda: f"Gemini API 실시간 요청 발송 중 ({model_name}) [시도 {attempt}/{max_retries}]...")

                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2,
                    ),
                )

                raw_text = response.text
                if DEBUG_MODE:
                    log_debug(lambda: f"Gemini 응답 수신 성공 (응답 길이: {len(raw_text)}자)")

                parsed_data = json.loads(raw_text)
                return parsed_data

            except Exception as e:
                err_msg = str(e)
                
                # 429 Quota 초과 예외 감지
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    # Retry-After delay 파싱 시도 (예: "retryDelay: '54s'")
                    delay_match = re.search(r"retryDelay':\s*['\"](\d+)s['\"]", err_msg)
                    wait_time = int(delay_match.group(1)) + 1 if delay_match else 20 * attempt

                    notice = f"⚠️ [API Quota 429 초과] {wait_time}초 후 자동으로 재시도합니다... ({attempt}/{max_retries})"
                    print(f"\n{notice}")
                    if DEBUG_MODE:
                        log_debug(lambda: notice)

                    if attempt < max_retries:
                        time.sleep(wait_time)
                        continue
                
                # 재시도 실패 혹은 다른 예외인 경우
                err_str = f"Gemini API 호출 오류: {e}"
                if DEBUG_MODE:
                    log_debug(lambda: err_str)
                return {
                    "status": "error",
                    "message": err_str,
                    "tasks": []
                }

        return {
            "status": "error",
            "message": "Gemini API 최대 재시도 횟수를 초과했습니다.",
            "tasks": []
        }