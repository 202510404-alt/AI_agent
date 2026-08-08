import time
import json
import re
from typing import Dict, Any, List, Literal, Optional
from pydantic import BaseModel, Field
from tools.multi_agent_system.browser_tester import BrowserTester, ensure_playwright

class BrowserActionSchema(BaseModel):
    action: Literal["click", "fill", "type", "press", "wait", "finish"]  # press, wait 추가
    selector: Optional[str] = None
    value: Optional[str] = ""

class BrowserAgentRunner:
    def __init__(self, session_factory):
        self.factory = session_factory

    def run_autonomous_loop(
        self, 
        target_url: str, 
        goal_description: str, 
        expected_patterns: List[str] = None,
        max_steps: int = 15
    ) -> Dict[str, Any]:
        """
        Playwright로 브라우저를 열고 Lite 모델과 토큰 최적화 대화형 루프를 수행
        """
        sync_playwright, PlaywrightTimeoutError = ensure_playwright()
        if not sync_playwright:
            return {"success": False, "message": "Playwright 설치 실패", "console_logs": []}

        captured_logs: List[str] = []
        captured_errors: List[str] = []
        expected_patterns = expected_patterns or []

        tester = BrowserTester(headless=False, default_timeout=15000)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False, slow_mo=500)  # slow_mo(ms)로 동작을 천천히 관찰 가능
                context = browser.new_context()
                page = context.new_page()

                page.on("console", lambda msg: captured_logs.append(f"[{msg.type.upper()}] {msg.text}"))
                page.on("pageerror", lambda err: captured_errors.append(str(err)))

                page.goto(target_url, timeout=tester.default_timeout, wait_until="domcontentloaded")

                action_history: List[str] = []  # 이전 실행 행동 및 결과 기록용 히스토리

                # 교착 상태(Stuck) 감지용 추적 변수 초기화
                consecutive_error_count = 0
                stuck_dom_count = 0
                prev_dom_hash = None

                for step in range(1, max_steps + 1):
                    # 1. 행동 실행 직후의 최신 스크린샷 및 DOM 요소 무조건 즉시 캡처 (화면 무변화 방지)
                    screenshot_bytes = tester.capture_compressed_screenshot(page)
                    elements = tester.extract_interactive_elements(page)

                    # 💡 [STUCK DETECTION] 기능적 대화형 요소(URL + Selector + Value + Disabled) 기반 해시 비교 (애니메이션 소음 제거)
                    current_url = page.url
                    interactive_state_str = f"{current_url}|" + "|".join(
                        f"{el.get('selector')}:{el.get('text')}" for el in elements
                    )
                    
                    if prev_dom_hash is not None and interactive_state_str == prev_dom_hash:
                        stuck_dom_count += 1
                        print(f"⚠️ [STUCK CHECK] 기능적 DOM 상태 변화 없음 ({stuck_dom_count}/3)")
                        if stuck_dom_count >= 3:
                            err_msg = "🚨 [FAIL-FAST] 3스텝 연속 화면 상태(기능적 DOM) 변화 없음 (Stuck 감지)"
                            print(err_msg)
                            captured_errors.append(err_msg)
                            break
                    else:
                        stuck_dom_count = 0
                        prev_dom_hash = interactive_state_str

                    # 2. 매 스텝 이전 행동 히스토리가 명시된 상태 전달 프롬프트 구성
                    prompt = f"""
[MISSION GOAL]
{goal_description}

[PREVIOUS ACTION HISTORY]
{json.dumps(action_history, ensure_ascii=False, indent=2) if action_history else "None (First Step)"}

[CURRENT STATUS]
Step: {step}/{max_steps}
Interactive Elements (DOM):
{json.dumps(elements, ensure_ascii=False)}

Recent Console Logs:
{captured_logs[-5:]}

Page Errors:
{captured_errors[-5:]}

[INSTRUCTION]
Analyze the provided current screenshot image, interactive DOM elements, action history, and console logs.
Select the next single browser action to fulfill the goal.
If the mission objective is already fully satisfied in the UI or console logs, output "finish" action.
"""
                    # system_instruction 구성하여 행동 규격 및 실패 액션 반복 금지 강제
                    system_instruction = """
당신은 브라우저 UI를 제어하는 자율 에이전트입니다.
반드시 아래 JSON 형식으로만 응답하십시오:
{"action": "click" | "fill" | "press" | "wait" | "finish", "selector": "CSS_SELECTOR", "value": "VALUE"}

[최우선 금지 및 우회 수칙]
1. PREVIOUS ACTION HISTORY를 반드시 확인하십시오.
2. 이전 스텝에서 FAILED (Timeout 등) 오류가 발생한 동일한 selector와 action 조합은 절대로 다시 실행하지 마십시오!
3. 특정 입력창 세렉터가 실패했다면, Interactive Elements (DOM)에 제공된 다른 세렉터(예: placeholder 기반)를 선택하거나 click 후 press 액션을 사용하십시오.
4. 텍스트 입력 시 action 이름은 "fill"을 사용하고, 입력 후 제출이 필요하면 다음 스텝에서 action: "press", value: "Enter"를 호출하십시오.
"""

                    # 3. 대화 세션 없이 단발성 워커 스텝 실행 (system_instruction 추가 전달)
                    res_text = self.factory.execute_worker_step(
                        prompt=prompt,
                        system_instruction=system_instruction,
                        image_bytes=screenshot_bytes,
                        response_mime_type="application/json"
                    )

                    # 4. 마크다운 태그 정제 및 JSON Pydantic 파싱
                    clean_json = re.sub(r"^```(?:json)?\n?|\n?```$", "", res_text.strip())
                    action_obj = BrowserActionSchema.model_validate_json(clean_json)
                    action_data = action_obj.model_dump()

                    act = action_data["action"]
                    sel = action_data["selector"]
                    val = action_data["value"]

                    print(f"🤖 [BROWSER AGENT Step {step}] {act} -> {sel} (val: {val})")

                    if act == "finish":
                        action_history.append(f"Step {step}: finish (Mission complete requested)")
                        break

                    # 5. Fail-Fast 예외 처리 및 자체 복구 로직 포함 실행 + 히스토리 기록
                    exec_result_status = "SUCCESS"
                    try:
                        if act == "click" and sel:
                            page.click(sel, timeout=3000)
                        elif act in ["fill", "type"] and sel:
                            page.fill(sel, str(val), timeout=3000)
                        elif act == "press" and sel:
                            page.press(sel, str(val or "Enter"), timeout=3000)
                        elif act == "wait" and sel:
                            page.wait_for_selector(sel, timeout=3000)
                    except PlaywrightTimeoutError:
                        err_msg = f"Timeout(3s) executing '{act}' on '{sel}'"
                        print(f"⚠️ [FAIL-FAST] {err_msg}")
                        captured_errors.append(err_msg)
                        exec_result_status = f"FAILED ({err_msg})"
                        consecutive_error_count += 1
                        # 입력창에 갇혔을 경우 자동 엔터 제출 1차 보완 시도
                        if act in ["fill", "type"] and sel:
                            try:
                                page.press(sel, "Enter", timeout=1500)
                                print("⚡ [SYSTEM AUTO-RECOVERY] 입력 타임아웃 발생으로 Enter 키 자동 제출 시도함")
                                exec_result_status += " -> Auto-recovery Enter pressed"
                            except Exception:
                                pass
                    except Exception as action_err:
                        err_msg = f"Error executing '{act}' on '{sel}': {action_err}"
                        print(f"⚠️ [ACTION ERROR] {err_msg}")
                        captured_errors.append(err_msg)
                        exec_result_status = f"FAILED ({err_msg})"
                        consecutive_error_count += 1
                    else:
                        consecutive_error_count = 0

                    action_history.append(f"Step {step}: action='{act}', selector='{sel}', value='{val}' -> Result: {exec_result_status}")

                    # 💡 [FAIL-FAST] 동일/연속 액션 실패 에러 3회 연속 발생 시 즉시 중단
                    if consecutive_error_count >= 3:
                        err_msg = "🚨 [FAIL-FAST] 액션 실패 에러가 3회 연속 발생하여 테스트를 강제 종료합니다."
                        print(err_msg)
                        captured_errors.append(err_msg)
                        break

                    page.wait_for_timeout(300)

                    # 목표 패턴 달성 여부 빠른 확인
                    all_logs_text = "\n".join(captured_logs)
                    if expected_patterns and all(re.search(p, all_logs_text) for p in expected_patterns):
                        print("✅ [BROWSER AGENT] 자율 탐색 중 목표 콘솔 로그 발견!")
                        break

                browser.close()

            all_logs_text = "\n".join(captured_logs)
            missing_patterns = [p for p in expected_patterns if not re.search(p, all_logs_text)]

            if missing_patterns:
                return {
                    "success": False,
                    "message": f"⚠️ [BROWSER AGENT FAIL] 예상 패턴 미발견: {missing_patterns}",
                    "console_logs": captured_logs,
                    "page_errors": captured_errors
                }

            return {
                "success": True,
                "message": "✅ [BROWSER AGENT SUCCESS] 자율 브라우저 탐색 및 검증 성공",
                "console_logs": captured_logs,
                "page_errors": captured_errors
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"💥 [BROWSER AGENT ERROR] 실행 중 예외: {e}",
                "console_logs": captured_logs,
                "page_errors": captured_errors
            }