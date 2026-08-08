"""
tools/multi_agent_system/browser_tester.py
Headless Browser(Playwright) 기반 웹 프론트엔드 E2E 및 런타임 실체 검증 도구
"""

import sys
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any

def ensure_playwright():
    """Playwright 패키지 및 브라우저 바이너리 자동 감지 및 설치 함수"""
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
        return sync_playwright, PlaywrightTimeoutError
    except ImportError:
        print("\n📦 [AUTO INSTALL] Playwright 패키지가 설치되어 있지 않아 자동 설치를 진행합니다...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
            subprocess.check_call([sys.executable, "-m", "playwright", "install"])
            print("✅ [AUTO INSTALL] Playwright 및 브라우저 패키지 설치가 완료되었습니다!\n")
            from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
            return sync_playwright, PlaywrightTimeoutError
        except Exception as e:
            print(f"❌ [AUTO INSTALL FAIL] Playwright 자동 설치 실패: {e}")
            return None, None

class BrowserTester:
    def __init__(self, headless: bool = True, default_timeout: int = 5000):
        self.headless = headless
        self.default_timeout = default_timeout

    def extract_interactive_elements(self, page) -> List[Dict[str, str]]:
        """
        페이지 내 클릭/입력 가능한 대화형 요소(Accessibility Elements)를 경량화하여 추출 (토큰 다이어트)
        """
        js_script = """
        () => {
            const elements = Array.from(document.querySelectorAll('button, a, input, select, textarea, [role="button"]'));
            return elements.map((el, idx) => {
                let idStr = el.id ? `#${el.id}` : '';
                let nameStr = el.name ? `[name="${el.name}"]` : '';
                let text = (el.innerText || el.value || el.placeholder || '').trim().replace(/\\s+/g, ' ');
                let selector = idStr || nameStr || (el.className ? `${el.tagName.toLowerCase()}.${el.className.trim().replace(/\s+/g, '.')}` : `${el.tagName.toLowerCase()}`);
                return {
                    tag: el.tagName.toLowerCase(),
                    selector: selector,
                    text: text.slice(0, 50),
                    type: el.type || ''
                };
            });
        }
        """
        try:
            return page.evaluate(js_script)
        except Exception:
            return []

    def capture_compressed_screenshot(self, page) -> bytes:
        """
        이미지 토큰 절감을 위해 뷰포트를 제한하고 JPEG 포맷으로 압축 캡처
        """
        try:
            page.set_viewport_size({"width": 800, "height": 600})
            return page.screenshot(type="jpeg", quality=50)
        except Exception:
            return b""

    def run_browser_verification(
        self, 
        target_url: str, 
        actions: List[Dict[str, Any]] = None, 
        expected_patterns: List[str] = None,
        wait_for_selector: str = None
    ) -> Dict[str, Any]:
        """
        미션 파일 규격에 맞춰 가상 브라우저 접속, 요소 대기, DOM 액션 수행, 콘솔 로그를 검증합니다.
        """
        # 패키지 미설치 시 자동 설치 시도 및 모듈 동적 로드
        sync_playwright, PlaywrightTimeoutError = ensure_playwright()

        if not sync_playwright:
            return {
                "success": False,
                "message": "❌ [BROWSER TEST FAIL] 'playwright' 패키지 자동 설치에 실패하였습니다.",
                "console_logs": [],
                "page_errors": []
            }
        captured_logs: List[str] = []
        captured_errors: List[str] = []
        actions = actions or []
        expected_patterns = expected_patterns or []

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                page = context.new_page()

                # 브라우저 콘솔 로그 및 런타임 에러 수집 이벤트 리스너 등록
                page.on("console", lambda msg: captured_logs.append(f"[{msg.type.upper()}] {msg.text}"))
                page.on("pageerror", lambda err: captured_errors.append(str(err)))

                # 1. 페이지 이동 (SPA 프론트엔드 환경에 맞춘 domcontentloaded 사용)
                print(f"🌐 [BROWSER TEST] 페이지 접속 시도: {target_url}")
                page.goto(target_url, timeout=self.default_timeout, wait_until="domcontentloaded")

                # 2. 특정 주요 엘리먼트 렌더링 대기 (설정된 경우)
                if wait_for_selector:
                    page.wait_for_selector(wait_for_selector, timeout=self.default_timeout)

                # 3. 지정된 DOM 액션 실행 (클릭, 값 변경 등)
                for idx, action in enumerate(actions, 1):
                    act_type = action.get("type")
                    selector = action.get("selector")
                    value = action.get("value")

                    print(f" └─ [Action {idx}] type={act_type}, selector='{selector}', value='{value}'")

                    if selector:
                        page.wait_for_selector(selector, timeout=self.default_timeout)

                    if act_type == "click":
                        page.click(selector)
                    elif act_type in ["fill", "type"]:
                        page.fill(selector, str(value))
                    elif act_type == "press":
                        page.press(selector, str(value or "Enter"))
                    elif act_type == "wait":
                        page.wait_for_selector(selector, timeout=self.default_timeout)
                    elif act_type == "change_color_input":
                        # HTML5 Color Picker (<input type='color'>) 값 변경 이벤트 강제 트리거
                        page.eval_on_selector(
                            selector,
                            """(el, val) => { 
                                el.value = val; 
                                el.dispatchEvent(new Event('input', { bubbles: true })); 
                                el.dispatchEvent(new Event('change', { bubbles: true })); 
                            }""",
                            arg=str(value)
                        )

                    page.wait_for_timeout(300)  # 브라우저 이벤트 처리 대기

                browser.close()

            # 4. 런타임 에러 존재 여부 검증
            if captured_errors:
                return {
                    "success": False,
                    "message": f"❌ [BROWSER TEST FAIL] 브라우저 런타임 예외 발생 ({len(captured_errors)}건)",
                    "console_logs": captured_logs,
                    "page_errors": captured_errors
                }

            # 5. expected_patterns 정규식/문자열 매칭 검증
            all_logs_text = "\n".join(captured_logs)
            missing_patterns = []

            for pattern in expected_patterns:
                import re
                if not re.search(pattern, all_logs_text):
                    missing_patterns.append(pattern)

            if missing_patterns:
                return {
                    "success": False,
                    "message": f"⚠️ [BROWSER TEST FAIL] 수집된 콘솔 로그에서 예상 패턴을 찾을 수 없습니다: {missing_patterns}",
                    "console_logs": captured_logs,
                    "page_errors": []
                }

            return {
                "success": True,
                "message": "✅ [BROWSER TEST SUCCESS] 브라우저 실제 실행 및 로그 검증 완료!",
                "console_logs": captured_logs,
                "page_errors": []
            }

        except PlaywrightTimeoutError as te:
            return {
                "success": False,
                "message": f"💥 [BROWSER TEST TIMEOUT] 요소를 찾을 수 없거나 접속 시간 초과: {te}",
                "console_logs": captured_logs,
                "page_errors": captured_errors
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"💥 [BROWSER TEST ERROR] 가상 브라우저 검증 중 예외 발생: {e}",
                "console_logs": captured_logs,
                "page_errors": captured_errors
            }