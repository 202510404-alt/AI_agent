"""
agent_core/plan/prompt_builder.py
사용자 목표와 인덱싱된 프로젝트 지도를 결합하여 LLM용 계획 프롬프트를 생성
"""

from pathlib import Path
from typing import Optional
from agent_core.plan.schemas import DEBUG_MODE, LOG_FILE_PATH


def log_debug(message_func):
    """DEBUG_MODE가 False일 때는 메시지 생성을 아예 하지 않아 성능 저하를 방지합니다."""
    if not DEBUG_MODE:
        return
    
    msg = message_func() if callable(message_func) else message_func
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"[PROMPT_BUILDER DEBUG] {msg}\n")
    except Exception:
        pass


class PromptBuilder:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        # system_maps/ 경로 우선 탐색 후 루트 fallback
        self.map_file = root_dir / "system_maps" / "AI_CODEBASE_MAP.md"
        if not self.map_file.exists():
            self.map_file = root_dir / "AI_CODEBASE_MAP.md"
            
        if DEBUG_MODE:
            log_debug(lambda: f"PromptBuilder 초기화 완료 - Root: {self.root_dir}, Map File Path: {self.map_file}")

    def _load_codebase_map(self) -> str:
        """create_ai_map.py로 생성된 요약 지도를 읽어옵니다."""
        if DEBUG_MODE:
            log_debug(lambda: "[DEBUG_LOG] Attempting to read codebase map file from target path.")

        if self.map_file.exists():
            try:
                content = self.map_file.read_text(encoding="utf-8")
                if DEBUG_MODE:
                    log_debug(lambda: f"코드베이스 지도 로드 성공 (총 {len(content)} 글자 읽음)")
                return content
            except Exception as e:
                err_msg = f"[경고] AI_CODEBASE_MAP.md 로드 실패: {e}"
                if DEBUG_MODE:
                    log_debug(lambda: f"코드베이스 지도 로드 실패 에러: {err_msg}")
                return err_msg

        if DEBUG_MODE:
            log_debug(lambda: "AI_CODEBASE_MAP.md 파일이 없어 기본 안내 문구를 반환합니다.")
        return "[안내] AI_CODEBASE_MAP.md 파일이 존재하지 않습니다."

    def build_plan_prompt(self, user_goal: str, extra_context: Optional[str] = None) -> str:
        """
        사용자 요구사항 + 요약 지도를 조합하여 플래너 LLM 제출용 프롬프트 완성
        """
        if DEBUG_MODE:
            log_debug(lambda: f"build_plan_prompt 호출 - Goal: '{user_goal}', Extra Context 여부: {extra_context is not None}")

        codebase_map = self._load_codebase_map()

        prompt = f"""# ROLE
당신은 최고 수준의 소프트웨어 아키텍트 겸 Master Planner입니다.
제시된 [프로젝트 코드베이스 지도]와 [사용자 요구사항]을 분석하여, 수정 작업을 최소 단위의 Task들로 분할하십시오.

# RULES
1. 전체 코드를 다시 작성하지 말고, 수정이 꼭 필요한 파일과 심볼(함수/클래스)만 핀포인트로 타겟팅하십시오.
2. 각 Task 간의 의존성(dependencies)을 명확히 명시하십시오.
3. 작업 결과물은 정해진 JSON 스키마 규격에 맞추어 출력하십시오.

# PROJECT CODEBASE MAP
{codebase_map}

# USER GOAL
{user_goal}
"""

        if extra_context:
            prompt += f"\n# ADDITIONAL CONTEXT\n{extra_context}\n"
            if DEBUG_MODE:
                log_debug(lambda: f"추가 컨텍스트(extra_context) 병합 완료 ({len(extra_context)} 글자)")

        if DEBUG_MODE:
            log_debug(lambda: f"최종 프롬프트 생성 완료 (총 {len(prompt)} 글자 결과물)")

        return prompt