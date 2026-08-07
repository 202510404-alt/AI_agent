"""
agent_core/plan/gemini_client.py
.env 파일 및 환경변수에서 GEMINI_API_KEY를 자동으로 로드하여 Google Gemini API와 통신하는 모듈
"""

import os
import re
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any, Tuple, List
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


def load_env_file(env_path: Path) -> Dict[str, str]:
    """
    .env 파일에서 GEMINI_API_KEY 계열을 모두 탐색하여 딕셔너리로 반환하고 os.environ에 주입합니다.
    """
    keys_dict = {}
    if not env_path.exists():
        if DEBUG_MODE:
            log_debug(lambda: f".env 파일을 찾을 수 없습니다: {env_path}")
        return keys_dict

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("'\"")
                    if key:
                        os.environ[key] = value
                        if "GEMINI_API_KEY" in key:
                            keys_dict[key] = value

        if "GEMINI_API_KEY" not in os.environ and keys_dict:
            first_key_name = list(keys_dict.keys())[0]
            os.environ["GEMINI_API_KEY"] = keys_dict[first_key_name]

        if DEBUG_MODE:
            log_debug(lambda: f".env 파일 로드 성공: 발견된 Gemini API Key {len(keys_dict)}개")
    except Exception as e:
        if DEBUG_MODE:
            log_debug(lambda: f".env 파일 파싱 중 예외 발생: {e}")
            
    return keys_dict


HARDCODED_GEMINI_MODELS = [
    # RPD 500회 이상 (에이전트 연사 가능)
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite",
    # RPD 20~50회 (쿼터 소진 빠름)
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
]


def resolve_best_gemini_model(client=None, blocked_models: set = None) -> str:
    """
    외부 모듈 호환성 보장용 함수.
    HARDCODED_GEMINI_MODELS 리스트 중 차단되지 않은 첫 번째 모델을 순차 반환합니다.
    """
    blocked = blocked_models or set()
    for model in HARDCODED_GEMINI_MODELS:
        if model not in blocked:
            return model
    return HARDCODED_GEMINI_MODELS[0]


class DynamicKeyModelManager:
    """
    [Key x Model] 순차 순환 방식 관리자
    - 하드코딩된 모델 목록(HARDCODED_GEMINI_MODELS)을 숫자가 낮은 버전부터 순서대로 사용합니다.
    - 403 PERMISSION_DENIED: 해당 Key 영구 차단
    - 429 / 503 / 404: 해당 (Key, Model) 60초 Cooldown 후 목록 내 다음 모델로 자동 전환
    """
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.env_path = root_dir / ".env"
        self.keys: Dict[str, str] = load_env_file(self.env_path)

        self.block_matrix: Dict[Tuple[str, str], float] = {}
        self.permanently_disabled_keys: set = set()
        self.last_used_key_name: str = "UNKNOWN"
        self.last_used_model_name: str = HARDCODED_GEMINI_MODELS[0]

    def get_available_pair(self) -> Tuple[str, str, str]:
        if not self.keys:
            self.keys = load_env_file(self.env_path)
            if not self.keys:
                raise RuntimeError("🚨 사용 가능한 GEMINI_API_KEY가 .env 파일에 없습니다.")

        now = time.time()
        active_keys = [(k, v) for k, v in self.keys.items() if k not in self.permanently_disabled_keys]

        if not active_keys:
            raise RuntimeError("🚨 모든 GEMINI_API_KEY가 403 PERMISSION_DENIED 차단되었습니다.")

        # 낮은 버전 모델부터 순서대로 사용 가능한 (Key, Model) 조합 탐색
        for model_name in HARDCODED_GEMINI_MODELS:
            for key_name, api_key_val in active_keys:
                blocked_until = self.block_matrix.get((key_name, model_name), 0)
                if now >= blocked_until:
                    self.last_used_key_name = key_name
                    self.last_used_model_name = model_name
                    return api_key_val, key_name, model_name

        # 모든 조합이 대기 중일 경우 잠시 대기 후 첫 번째 모델 반환
        first_key_name, first_key_val = active_keys[0]
        min_wait = min([b - now for b in self.block_matrix.values() if b > now], default=2.0)
        time.sleep(max(0.5, min_wait))
        
        target_m = HARDCODED_GEMINI_MODELS[0]
        self.last_used_key_name = first_key_name
        self.last_used_model_name = target_m
        return first_key_val, first_key_name, target_m

    def report_error(self, key_name: str, model_name: str, error_str: str):
        now = time.time()

        if "403" in error_str or "PERMISSION_DENIED" in error_str:
            print(f"⛔ [403 DENIED] Key '{key_name}' 차단됨 -> 다음 Key로 전환")
            self.permanently_disabled_keys.add(key_name)
        elif "429" in error_str or "EXHAUSTED" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            # 429 발생 시 모델 전환을 막기 위해 60초 차단 대신 짧은 대기(3초) 후 키만 전환
            print(f"⏳ [429 RATE LIMIT] ({key_name} x {model_name}) 쿼터 초과 -> 3초 대기 후 다음 키 스위칭...")
            time.sleep(3.0)
            self.block_matrix[(key_name, model_name)] = now + 3.0
        else:
            print(f"⚠️ [API ERROR] ({key_name} x {model_name}) 60초 대기 후 다음 모델 스위칭: {error_str[:100]}")
            self.block_matrix[(key_name, model_name)] = now + 60.0


class GeminiPlannerClient:
    def __init__(self, api_key: Optional[str] = None, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or Path.cwd()
        self.manager = DynamicKeyModelManager(self.root_dir)
        self.client = None

    def generate_plan(self, prompt: str, model_name: Optional[str] = None, max_retries: int = 10) -> Dict[str, Any]:
        if not HAS_GENAI:
            return {"status": "success", "mode": "mock", "tasks": []}

        last_error = ""
        current_override_model = model_name

        for attempt in range(1, max_retries + 1):
            api_key_val, key_name, target_model = self.manager.get_available_pair()
            
            # 최초 1회차에만 전달된 model_name 사용, 실패 시 manager의 모델 순환 적용
            if attempt == 1 and current_override_model:
                target_model = current_override_model

            try:
                client = genai.Client(api_key=api_key_val)
                response = client.models.generate_content(
                    model=target_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2,
                    ),
                    request_options={
                        "retry": None  # SDK 내부 대기 차단 (0초 Fail-Fast)
                    }
                )
                return json.loads(response.text)

            except Exception as e:
                err_msg = str(e)
                last_error = err_msg
                # 에러 발생 시 지정 모델 강제 설정을 해제하여 다음 attempt부터 모델 순환 허용
                current_override_model = None
                self.manager.report_error(key_name, target_model, err_msg)

        return {"status": "error", "message": f"호출 실패: {last_error}", "tasks": []}