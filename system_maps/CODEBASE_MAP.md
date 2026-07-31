# 🏗️ 짭커서 프로젝트 CODEBASE MAP

현재 인덱싱된 총 파일 수: **53개**

## 🗂️ [Module Index]
- `.vscode/settings.json`
- `agent_core/__init__.py`
- `agent_core/execution/__init__.py`
- `agent_core/memory/__init__.py`
- `agent_core/plan/__init__.py`
- `agent_core/plan/gemini_client.py`
- `agent_core/plan/planner.py`
- `agent_core/plan/prompt_builder.py`
- `agent_core/plan/schemas.py`
- `agent_core/plan/test_ai_chat.py`
- `agent_core/validation/__init__.py`
- `extraction_target_project/client/package-lock.json`
- `extraction_target_project/client/package.json`
- `extraction_target_project/client/public/manifest.json`
- `extraction_target_project/client/src/App.js`
- `extraction_target_project/client/src/App.test.js`
- `extraction_target_project/client/src/Button.js`
- `extraction_target_project/client/src/Canvas.js`
- `extraction_target_project/client/src/Home.js`
- `extraction_target_project/client/src/Input.js`
- `extraction_target_project/client/src/UploadFile.js`
- `extraction_target_project/client/src/hooks/useWebRTC.js`
- `extraction_target_project/client/src/index.js`
- `extraction_target_project/client/src/reportWebVitals.js`
- `extraction_target_project/client/src/setupTests.js`
- `extraction_target_project/client/src/socket.js`
- `extraction_target_project/index.js`
- `extraction_target_project/package-lock.json`
- `extraction_target_project/package.json`
- `run_test.py`
- `tools/multi_agent_system/__init__.py`
- `tools/multi_agent_system/agent_code_extractor.py`
- `tools/multi_agent_system/agent_session.py`
- `tools/multi_agent_system/code_patcher.py`
- `tools/multi_agent_system/terminal_runner.py`
- `tools/universal_indexer/agent_navigator.py`
- `tools/universal_indexer/config.py`
- `tools/universal_indexer/context_builder.py`
- `tools/universal_indexer/core_parsers/__init__.py`
- `tools/universal_indexer/core_parsers/cs_parser.py`
- `tools/universal_indexer/core_parsers/gitignore_parser.py`
- `tools/universal_indexer/core_parsers/java_parser.py`
- `tools/universal_indexer/core_parsers/js_parser.py`
- `tools/universal_indexer/core_parsers/json_parser.py`
- `tools/universal_indexer/core_parsers/py_parser.py`
- `tools/universal_indexer/create_ai_map.py`
- `tools/universal_indexer/indexer.py`
- `tools/universal_indexer/jjap_lookup.py`
- `tools/universal_indexer/jjap_retriever.py`
- `tools/universal_indexer/jjap_watcher.py`
- `tools/universal_indexer/switch.py`
- `tools/universal_indexer/tree_sitter_parser.py`
- `tools/universal_indexer/update_map.py`

## 💀 [Skeleton & Dependency 명세서]
### 📄 .vscode/settings.json
#### 🔍 내부 심볼 및 의존성 관계:
- **[JSON_KEY]** `terminal.integrated.sendKeybindingsToShell` (Line: 2~2)
- **[JSON_KEY]** `accessibility.verbosity.terminal` (Line: 3~3)
- **[JSON_KEY]** `git.autofetch` (Line: 4~4)
- **[JSON_KEY]** `explorer.confirmDelete` (Line: 5~5)
- **[JSON_KEY]** `git.openRepositoryInParentFolders` (Line: 6~6)
- **[JSON_KEY]** `terminal.integrated.enableMultiLinePasteWarning` (Line: 7~7)
- **[JSON_KEY]** `workbench.editor.empty.hint` (Line: 8~8)
- **[JSON_KEY]** `maven.terminal.useJavaHome` (Line: 9~9)
- **[JSON_KEY]** `git.confirmSync` (Line: 10~10)
- **[JSON_KEY]** `explorer.confirmDragAndDrop` (Line: 11~11)
- **[JSON_KEY]** `java.configuration.runtimes` (Line: 12~12)
- **[JSON_KEY]** `java.jdt.ls.java.home` (Line: 19~19)
- **[JSON_KEY]** `roo-cline.debug` (Line: 20~20)
- **[JSON_KEY]** `roo-cline.allowedCommands` (Line: 21~21)
- **[JSON_KEY]** `roo-cline.deniedCommands` (Line: 22~22)
- **[JSON_KEY]** `files.exclude` (Line: 23~23)
- **[JSON_KEY]** `python.createEnvironment.trigger` (Line: 26~26)
- **[JSON_KEY]** `java.configuration.updateBuildConfiguration` (Line: 27~27)
- **[JSON_KEY]** `python-envs.defaultEnvManager` (Line: 28~28)

#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "terminal.integrated.sendKeybindingsToShell": bool (val: True)
  ├── "accessibility.verbosity.terminal": bool (val: False)
  ├── "git.autofetch": bool (val: True)
  ├── "explorer.confirmDelete": bool (val: False)
  ├── "git.openRepositoryInParentFolders": str (val: always)
  ├── "terminal.integrated.enableMultiLinePasteWarning": str (val: never)
  ├── "workbench.editor.empty.hint": str (val: hidden)
  ├── "maven.terminal.useJavaHome": bool (val: True)
  ├── "git.confirmSync": bool (val: False)
  ├── "explorer.confirmDragAndDrop": bool (val: False)
  ├── "java.configuration.runtimes": List (len: 1)
  ├── "java.jdt.ls.java.home": str (val: C:/Program Files/Eclipse Adopt)
  ├── "roo-cline.debug": bool (val: True)
  ├── "roo-cline.allowedCommands": List (len: 0)
  ├── "roo-cline.deniedCommands": List (len: 0)
  ├── "files.exclude": Dict (keys: ['**/__pycache__']...)
  ├── "python.createEnvironment.trigger": str (val: external)
  ├── "java.configuration.updateBuildConfiguration": str (val: interactive)
  ├── "python-envs.defaultEnvManager": str (val: ms-python.python:system)
```

--------------------------------------------------

### 📄 agent_core/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/execution/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/memory/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/plan/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/plan/gemini_client.py
#### 🧱 Code Skeleton:
```python
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

    def generate_plan(self, prompt: str, model_name: str = "gemini-2.5-flash") -> Dict[str, Any]:
        """
        Gemini 모델에 프롬프트를 전달하고 구조화된 응답(JSON)을 추출합니다.
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

        # 실제 Gemini API 호출
        try:
            if DEBUG_MODE:
                log_debug(lambda: f"Gemini API 실시간 요청 발송 중 ({model_name})...")

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
            err_str = f"Gemini API 호출 오류: {e}"
            if DEBUG_MODE:
                log_debug(lambda: err_str)
            return {
                "status": "error",
                "message": err_str,
                "tasks": []
            }
```

--------------------------------------------------

### 📄 agent_core/plan/planner.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/plan/prompt_builder.py
#### 🧱 Code Skeleton:
```python
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
            log_debug(lambda: f"코드베이스 지도 파일 읽기 시도: {self.map_file}")

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
```

--------------------------------------------------

### 📄 agent_core/plan/schemas.py
#### 🧱 Code Skeleton:
```python
def log_debug(message_func):
    """
    DEBUG_MODE가 False일 때는 문자열 생성 연산 자체를 호출하지 않아 자원 소모를 0으로 만듭니다.
    """
    if not DEBUG_MODE:
        return
    
    # 람다 함수나 콜백을 통해 로그 메시지를 지연 평가(Lazy Evaluation)
    msg = message_func() if callable(message_func) else message_func
    
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(f"[SCHEMAS DEBUG] {msg}\n")
    except Exception:
        pass

class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class SymbolRef:
    """코드 내 심볼(함수, 클래스 등) 위치 정보"""
    file_path: str
    symbol_name: str
    start_line: int
    end_line: int

class DebugLogSpec:
    """작업 단위별 예상 디버깅 로그 스펙"""
    expected_logs: List[str] = field(default_factory=list)
    log_targets: List[str] = field(default_factory=list)

class Task:
    """플래너가 생성하는 최소 실행 작업 단위"""
    task_id: str
    description: str
    target_files: List[str]
    read_symbols: List[SymbolRef] = field(default_factory=list)
    write_symbols: List[SymbolRef] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    debug_spec: Optional[DebugLogSpec] = None

class ExecutionResult:
    """단독 실행 및 검증 결과"""
    task_id: str
    success: bool
    output_log: str
    error_message: Optional[str] = None

def to_symbol_ref(raw_dict: Dict[str, Any], default_file: str = "") -> SymbolRef:
    """
    Indexer 및 Parsers가 리턴하는 딕셔너리 데이터를 에이전트 용 SymbolRef로 정규화합니다.
    """
    if DEBUG_MODE:
        log_debug(lambda: f"to_symbol_ref 변환 시작 - Raw Input: {raw_dict}, Default File: {default_file}")

    file_path = raw_dict.get("file_path", default_file)
    symbol_name = raw_dict.get("name", raw_dict.get("symbol_name", "unknown"))
    start_line = raw_dict.get("start_line", raw_dict.get("line_start", 0))
    end_line = raw_dict.get("end_line", raw_dict.get("line_end", 0))

    result = SymbolRef(
        file_path=file_path,
        symbol_name=symbol_name,
        start_line=start_line,
        end_line=end_line
    )

    if DEBUG_MODE:
        log_debug(lambda: f"to_symbol_ref 변환 완료 - Result SymbolRef: {result}")

    return result
```

--------------------------------------------------

### 📄 agent_core/plan/test_ai_chat.py
#### 🧱 Code Skeleton:
```python
def extract_code_slice(file_and_line: str) -> str:
    """
    특정 파일 및 라인 범위의 코드 슬라이스를 추출하고 관련 심볼 정보까지 정밀 검색합니다.
    
    Args:
        file_and_line: "파일경로:시작줄-끝줄" 형태의 문자열 (예: "agent_core/plan/schemas.py:15-40")
    """
    print(f"\n⚙️ [SYSTEM TOOL EXECUTION] 'extract_code_slice' 실행 중... Target: {file_and_line}")
    res = extractor.process(file_and_line, auto_save=False)
    if res["markdown"]:
        return res["markdown"]
    return "❌ 해당 파일 또는 라인 범위를 찾을 수 없거나 코드 추출에 실패했습니다."

def run_interactive_chat():
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not HAS_GENAI:
        print("❌ 'google-genai' 패키지가 설치되어 있지 않습니다. (pip install google-genai)")
        return
        
    if not api_key:
        print("⚠️ GEMINI_API_KEY가 존재하지 않습니다. .env 파일에 키를 설정해주세요.")
        return

    client = genai.Client(api_key=api_key)
    prompt_builder = PromptBuilder(root_dir=ROOT_DIR)
    
    # 1. AI 지형도 시스템 프롬프트 준비
    system_instruction = prompt_builder.build_plan_prompt(
        user_goal="사용자의 질의에 따라 필요한 경우 도구(Tool)를 호출하여 코드나 정보를 확인하고 답변하십시오."
    )

    # 2. Chat 세션 초기화 (Tool 등록 및 Chat 자동 컨텍스트 관리)
    # gemini-2.5-flash 모델을 사용하여 대화 및 Tool Calling 처리
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[extract_code_slice], # AI가 스스로 호출 가능한 함수 전달
            temperature=0.2,
        )
    )

    print("\n==================================================================")
    print("🤖 ASE-OS v1.3 Interactive AI Chat & Tool Calling Validation")
    print("==================================================================")
    print("💡 사용자가 질의를 입력하면 AI가 필요 시 자동으로 도구를 실행합니다.")
    print("💡 종료하시려면 'exit' 또는 'quit'를 입력하세요.\n")

    while True:
        try:
            user_input = input("👤 User > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("👋 대화를 종료합니다.")
                break

            print("🤖 AI 생각 중...")
            response = chat.send_message(user_input)
            
            # AI의 최종 응답 출력
            print(f"\n🤖 AI > {response.text}\n")

        except KeyboardInterrupt:
            print("\n👋 대화를 종료합니다.")
            break
        except Exception as e:
            print(f"\n💥 예외 발생: {e}\n")
```

--------------------------------------------------

### 📄 agent_core/validation/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 extraction_target_project/client/package-lock.json
#### 🔍 내부 심볼 및 의존성 관계:
- **[JSON_KEY]** `name` (Line: 2~2)
  - 🎯 *Used By (나를 부르는 곳)*: `extraction_target_project/client/package-lock.json::packages`
- **[JSON_KEY]** `version` (Line: 3~3)
- **[JSON_KEY]** `lockfileVersion` (Line: 4~4)
- **[JSON_KEY]** `requires` (Line: 5~5)
- **[JSON_KEY]** `packages` (Line: 6~6)
  - 🔗 *Calls (호출하는 것)*: `node_modules/css.escape, node_modules/string.prototype.trim, node_modules/string.prototype.trimend, node_modules/hpack.js, big.js, bin/semver.js, bin/nanoid.cjs, node_modules/reflect.getprototypeof, bin/escodegen.js, bin/esparse.js, bin/cmd.js, bin/webpack.js, node_modules/array.prototype.findlast, node_modules/array.prototype.flat, node_modules/object.fromentries, node_modules/object.hasown, node_modules/array.prototype.findlastindex, node_modules/engine.io, dist/esm/bin.mjs, node_modules/array.prototype.tosorted, node_modules/lodash.merge, node_modules/lodash.uniq, node_modules/string.prototype.trimstart, node_modules/object.groupby, bin/babel-parser.js, node_modules/big.js, node_modules/sanitize.css, node_modules/decimal.js, node_modules/array.prototype.flatmap, fraction.js, cli.js, node_modules/iterator.prototype, node_modules/string.prototype.matchall, node_modules/util.promisify, node_modules/lodash.memoize, bin/nopt.js, node_modules/resolve.exports, hpack.js, bin/esgenerate.js, node_modules/fs.realpath, node_modules/function.prototype.name, node_modules/array.prototype.toreversed, fixtures/cli.js, node_modules/object.entries, bin/jiti.js, node_modules/object.getownpropertydescriptors, bin.js, bin/js-yaml.js, dist/cli.cjs, node_modules/array.prototype.reduce, node_modules/ipaddr.js, node_modules/socket.io, node_modules/fraction.js, decimal.js, node_modules/lodash.debounce, bin/cli.js, bin/esvalidate.js, node_modules/proxy-addr/node_modules/ipaddr.js, bin/webpack-dev-server.js, bin/bin.js, ipaddr.js, node_modules/regexp.prototype.flags, bin/eslint.js, lib/cli.js, bin/react-scripts.js, node_modules/object.values, node_modules/lodash.sortby, node_modules/arraybuffer.prototype.slice, bin/jest.js, node_modules/object.assign`

#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "name": str (val: whiteboard)
  ├── "version": str (val: 0.1.0)
  ├── "lockfileVersion": int (val: 3)
  ├── "requires": bool (val: True)
  ├── "packages": Dict (keys: ['', 'node_modules/@aashutoshrathi/word-wrap', 'node_modules/@adobe/css-tools']...)
```

--------------------------------------------------

### 📄 extraction_target_project/client/package.json
#### 🔍 내부 심볼 및 의존성 관계:
- **[JSON_KEY]** `name` (Line: 2~2)
- **[JSON_KEY]** `version` (Line: 3~3)
- **[JSON_KEY]** `private` (Line: 4~4)
- **[JSON_KEY]** `dependencies` (Line: 5~5)
- **[JSON_KEY]** `scripts` (Line: 21~21)
- **[JSON_KEY]** `eslintConfig` (Line: 27~27)
- **[JSON_KEY]** `browserslist` (Line: 33~33)

#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "name": str (val: whiteboard)
  ├── "version": str (val: 0.1.0)
  ├── "private": bool (val: True)
  ├── "dependencies": Dict (keys: ['@testing-library/jest-dom', '@testing-library/react', '@testing-library/user-event']...)
  ├── "scripts": Dict (keys: ['start', 'build', 'test']...)
  ├── "eslintConfig": Dict (keys: ['extends']...)
  ├── "browserslist": Dict (keys: ['production', 'development']...)
```

--------------------------------------------------

### 📄 extraction_target_project/client/public/manifest.json
#### 🔍 내부 심볼 및 의존성 관계:
- **[JSON_KEY]** `short_name` (Line: 2~2)
- **[JSON_KEY]** `name` (Line: 3~3)
- **[JSON_KEY]** `icons` (Line: 4~4)
- **[JSON_KEY]** `start_url` (Line: 27~27)
- **[JSON_KEY]** `display` (Line: 28~28)
- **[JSON_KEY]** `theme_color` (Line: 29~29)
- **[JSON_KEY]** `background_color` (Line: 30~30)

#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "short_name": str (val: 화이트보드)
  ├── "name": str (val: 실시간 협업 화이트보드)
  ├── "icons": List (len: 4)
  ├── "start_url": str (val: .)
  ├── "display": str (val: standalone)
  ├── "theme_color": str (val: #243b55)
  ├── "background_color": str (val: #141e30)
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/App.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./Canvas, ./Home, react, react-hot-toast, react-router-dom
🎯 def App() [L11~L20]
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/App.test.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./App, @testing-library/react
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/Button.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: react
🎯 def Button({ value, name, buttonFunction }) [L4~L24]
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/Canvas.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./Button, ./UploadFile, ./hooks/useWebRTC, ./socket, react, react-hot-toast, react-icons/ai, react-icons/fa6, react-router-dom
🎯 def RemoteAudio({ stream }) [L24~L54]
🎯 def playAudio() [L32~L47]
🎯 def handleUserInteraction() [L38~L43]
🎯 def Canvas(props) [L56~L481]
🎯 def changeColour(event) [L83~L86]
🎯 def lineWidth(event) [L88~L94]
🎯 def handleImageUploadSuccess(imageUrl) [L96~L104]
🎯 def init() [L107~L155]
🎯 def handleError(err) [L118~L122]
🎯 def handleDraw(e) [L187~L203]
🎯 def handleMoveDraw(e) [L205~L224]
🎯 def handleNotDraw() [L226~L239]
🎯 def undo() [L241~L254]
🎯 def redrawCanvas(context, history = linesHistory) [L256~L278]
🎯 def handleCanvasChange() [L284~L289]
🎯 def clearCanvas() [L298~L305]
🎯 def copyBoardId() [L307~L310]
🎯 def leaveBoard() [L312~L314]
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/Home.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: react, react-hot-toast, react-router-dom, uuid
🎯 def Home() [L8~L63]
🎯 def writeId(event) [L14~L18]
🎯 def writeUserName(event) [L20~L22]
🎯 def generateUniqueId(event) [L24~L29]
🎯 def joinBoard() [L31~L39]
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/Input.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: react
🎯 def Input(props) [L3~L9]
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/UploadFile.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: react, react-icons/fa6
🎯 def UploadFile(props) [L5~L31]
🎯 def upload(event) [L8~L15]
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/hooks/useWebRTC.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: react, react-hot-toast
🎯 def useWebRTC(socketRef, boardId, userName) [L32~L358]
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/index.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: ./App, ./reportWebVitals, react, react-dom/client
```

--------------------------------------------------

### 📄 extraction_target_project/client/src/reportWebVitals.js
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 extraction_target_project/client/src/setupTests.js
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 extraction_target_project/client/src/socket.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: socket.io-client
🎯 def initSocket() [L5~L35]
```

--------------------------------------------------

### 📄 extraction_target_project/index.js
#### 🧱 Code Skeleton:
```python
💡 📦 imp: express, http, os, path, socket.io, url
🎯 def getAllConnectedClients(boardId) [L35~L41]
🎯 def getLocalExternalIP() [L209~L219]
```

--------------------------------------------------

### 📄 extraction_target_project/package-lock.json
#### 🔍 내부 심볼 및 의존성 관계:
- **[JSON_KEY]** `name` (Line: 2~2)
- **[JSON_KEY]** `version` (Line: 3~3)
- **[JSON_KEY]** `lockfileVersion` (Line: 4~4)
- **[JSON_KEY]** `requires` (Line: 5~5)
- **[JSON_KEY]** `packages` (Line: 6~6)
  - 🔗 *Calls (호출하는 것)*: `node_modules/engine.io, bin/nodemon.js, ipaddr.js, bin/semver.js, bin/nodetouch.js, node_modules/ipaddr.js, cli.js, node_modules/socket.io, node_modules/pstree.remy`

#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "name": str (val: real-time-collaborative)
  ├── "version": str (val: 1.0.0)
  ├── "lockfileVersion": int (val: 3)
  ├── "requires": bool (val: True)
  ├── "packages": Dict (keys: ['', 'node_modules/@socket.io/component-emitter', 'node_modules/@types/cors']...)
```

--------------------------------------------------

### 📄 extraction_target_project/package.json
#### 🔍 내부 심볼 및 의존성 관계:
- **[JSON_KEY]** `name` (Line: 2~2)
- **[JSON_KEY]** `version` (Line: 3~3)
- **[JSON_KEY]** `type` (Line: 4~4)
- **[JSON_KEY]** `description` (Line: 5~5)
- **[JSON_KEY]** `main` (Line: 6~6)
  - 🔗 *Calls (호출하는 것)*: `index.js`
- **[JSON_KEY]** `scripts` (Line: 7~7)
  - 🔗 *Calls (호출하는 것)*: `index.js`
- **[JSON_KEY]** `license` (Line: 15~15)
- **[JSON_KEY]** `dependencies` (Line: 16~16)

#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "name": str (val: real-time-collaborative)
  ├── "version": str (val: 1.0.0)
  ├── "type": str (val: module)
  ├── "description": str (val: Real-time collaborative)
  ├── "main": str (val: index.js)
  ├── "scripts": Dict (keys: ['start', 'dev', 'dev:client']...)
  ├── "license": str (val: ISC)
  ├── "dependencies": Dict (keys: ['dateuuidv2', 'express', 'nodemon']...)
```

--------------------------------------------------

### 📄 run_test.py
#### 🧱 Code Skeleton:
```python
def run_interactive_chat():
    try:
        # AI 세션을 '구워주는' 팩토리 호출
        factory = AgentSessionFactory(ROOT_DIR)
        chat = factory.create_chat_session()
    except Exception as e:
        print(f"❌ 세션 생성 실패: {e}")
        return

    print("\n==================================================================")
    print("🤖 ASE-OS v1.3 Interactive AI Chat (Auto Execution Loop)")
    print("==================================================================")
    print("💡 사용자가 질의를 입력하면 AI가 필요 시 자동으로 도구를 실행합니다.")
    print("💡 종료하시려면 'exit' 또는 'quit'를 입력하세요.\n")

    while True:
        try:
            user_input = input("👤 User > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("👋 대화를 종료합니다.")
                break

            print("\n🤖 [Step 1] AI 판단 및 도구 실행 중...")
            response = chat.send_message(user_input)
            print(f"\n🤖 AI > {response.text}\n")

        except KeyboardInterrupt:
            print("\n👋 대화를 종료합니다.")
            break
        except Exception as e:
            print(f"\n💥 예외 발생: {e}\n")

def main():
    print("🚀 테스트 스크립트를 가동합니다...")
    
    # 1. 실행 시 디버그 로그 파일 초기화
    if LOG_FILE_PATH.exists():
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            f.write("=== [Jjap-Cursor Agent Debug Log Initialized] ===\n")
            
    print(f"📝 디버그 로그 위치: {LOG_FILE_PATH.resolve()}")
    print(f"🎛️ 현재 DEBUG_MODE 상태: {DEBUG_MODE}\n")

    # 2. 대화형 AI 인터랙션 진입
    print("🤖 대화형 AI 테스트 모드로 진입합니다...")
    run_interactive_chat()
```

--------------------------------------------------

### 📄 tools/multi_agent_system/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/multi_agent_system/agent_code_extractor.py
#### 🧱 Code Skeleton:
```python
class CodeExtractor:
    """
    AI 에이전트 및 파이프라인 전용 코드 정밀 추출기 (Headless Code Extractor)
    - UI(Tkinter 등) 요소를 완전히 제거하고 순수 데이터 처리 및 정보 흐름만 수행
    - 기존 SemanticNavigator의 슬라이싱, 경로 구제, 양방향 심볼 연관 추적 로직 100% 보존
    """
    def __init__(self, root_dir: str | Path):
        self.raw_root_dir = Path(root_dir).resolve()
        self.scan_mode = "ROOT"
        
        # 🎛️ [SCAN_MODE 스위치 반영 - universal_indexer/switch.py 절대 위치 고정]
        try:
            idx_path = str((self.raw_root_dir / "tools" / "universal_indexer").resolve())
            if idx_path not in sys.path:
                sys.path.insert(0, idx_path)
            
            import switch
            self.scan_mode = getattr(switch, "SCAN_MODE", "ROOT")
            print(f"🎛️ [SWITCH DETECTED] 현재 탐색 스위치 모드: {self.scan_mode}")
        except Exception as e:
            print(f"⚠️ [SWITCH WARNING] switch.py를 로드하지 못해 기본 'ROOT' 모드로 동작합니다. (이유: {e})")

        # 🚀 SRC 모드일 경우 하드디스크 탐색 기준점(self.root_dir)에 'src' 폴더를 강제 결합
        if self.scan_mode == "SRC":
            self.root_dir = self.raw_root_dir / "src"
            print(f"📁 [MODE: SRC] 탐색 마스터 루트가 복사/격리용 src 폴더로 변경되었습니다: {self.root_dir}")
        else:
            self.root_dir = self.raw_root_dir
            print(f"📁 [MODE: ROOT] 탐색 마스터 루트가 프로젝트 원본 루트로 설정되었습니다: {self.root_dir}")

        # 🧠 [불러오기 교정] 장부 정보는 언제나 프로젝트의 실제 본체 루트(raw_root_dir) 기준으로 가져옵니다.
        self.symbols_path = self.raw_root_dir / "system_memory" / ".jjap_symbols.json"
        self.symbols_data = self._load_database()

    def _load_database(self) -> dict:
        if not self.symbols_path.exists():
            return {"symbols": []}
        try:
            with open(self.symbols_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"symbols": []}

    def resolve_file_path(self, raw_path_str: str) -> Path | None:
        """
        [경로 구제 통합 레이더]
        SCAN_MODE, 상대 경로, extraction_target_project, tools 등 
        다양한 디렉토리 변수를 추적하여 실제 존재하는 파일의 Absolute Path를 반환합니다.
        """
        clean_path_str = raw_path_str.strip().replace("\\", "/")
        
        # 1차 시도: 모드별 스펙에 맞춘 경로 조립
        if self.scan_mode == "SRC":
            if clean_path_str.startswith("src/src/"):
                candidate = self.raw_root_dir / clean_path_str
            elif clean_path_str.startswith("src/"):
                candidate = self.raw_root_dir / clean_path_str
            else:
                candidate = self.raw_root_dir / "src" / clean_path_str
        else:
            candidate = self.raw_root_dir / clean_path_str

        if candidate.exists() and candidate.is_file():
            return candidate

        # 2차 시도 (구제금융): raw_root_dir 기준 직접 탐색
        candidate_raw = self.raw_root_dir / clean_path_str
        if candidate_raw.exists() and candidate_raw.is_file():
            return candidate_raw

        # 3차 시도 (구제금융): extraction_target_project 하위 탐색
        candidate_target = self.raw_root_dir / "extraction_target_project" / clean_path_str
        if candidate_target.exists() and candidate_target.is_file():
            return candidate_target

        # 4차 시도 (구제금융): tools 하위 탐색
        candidate_tools = self.raw_root_dir / "tools" / clean_path_str
        if candidate_tools.exists() and candidate_tools.is_file():
            return candidate_tools

        return None

    def extract_multi_slices(self, raw_prompt: str) -> list[dict]:
        """
        [Multi-Target Protocol Parser - 정규식 통합 및 경로 구제 완전판]
        프롬프트를 파싱하여 코드 슬라이스 묶음(list of dict)을 리턴합니다.
        """
        print("\n" + "="*60)
        print("🚨 [EXTRACTOR ON] 멀티 슬라이싱 파이프라인 기동!!!")
        print(f"📥 유저 입력 프롬프트: {repr(raw_prompt)}")
        print(f"⚙️ 현재 매핑 모드: {self.scan_mode} (기준 경로: {self.root_dir})")
        print("="*60)

        pattern = r"([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\s:]+(?:L)?(\d+)(?:\s*-\s*(?:L)?(\d+))?"
        matches = re.findall(pattern, raw_prompt)

        print(f"🔍 정규식 1차 타겟 스캔 결과: {matches}")
        if not matches:
            print("⚠️ 매칭되는 파일 경로 및 라인 규격이 없습니다. 빈 배열 리턴.")
            return []

        extracted_slices = []
        req_num = 1

        for match in matches:
            file_rel_path = match[0].strip().replace("\\", "/")
            start_line = int(match[1])
            end_line = int(match[2]) if match[2] else start_line

            print(f"\n🎯 [요청 #{req_num}] 메인 타겟 분석 시작 -> {file_rel_path} ({start_line} ~ {end_line} 라인)")

            target_file_path = self.resolve_file_path(file_rel_path)
            
            if not target_file_path:
                print(f"   ❌ [ERROR] 해당 파일이 실제 경로에 존재하지 않습니다! 패스합니다: {file_rel_path}")
                continue

            print(f"   🟢 [경로 확정] 디스크 실체 발견: {target_file_path}")

            try:
                with open(target_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                total_lines = len(lines)
                safe_start = max(1, min(start_line, total_lines))
                safe_end = max(safe_start, min(end_line, total_lines))
                print(f"   📏 파일 전체 줄 수: {total_lines} | 보정된 안전 범위: {safe_start} ~ {safe_end}")

                slice_lines = lines[safe_start - 1 : safe_end]
                slice_code = "".join(slice_lines)
                print(f"   🟢 1차 메인 슬라이싱 성공 (길이: {len(slice_code)}자)")

                extracted_slices.append({
                    "req_num": f"{req_num}",
                    "file": file_rel_path,
                    "line_range": f"{safe_start}-{safe_end}",
                    "code": slice_code
                })

                # [2단계] 🔗 제이슨 기반 2차 심볼 탐색기 가동
                print(f"   📡 [2차 사냥기] 잘려 나온 텍스트 내부에서 양방향 심볼 식별 개시...")

                defined_names = re.findall(r"(?:def|class)\s+([a-zA-Z0-9_]+)", slice_code)
                called_names = re.findall(r"(?:[a-zA-Z0-9_]+\.)?([a-zA-Z0-9_]+)\s*\(", slice_code)
                file_ref_names = [f for f in re.findall(r'[\'"]([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\'"]', slice_code) if f != file_rel_path]

                builtin_filters = {"print", "len", "range", "open", "dict", "list", "set", "any", "all", "max", "min", "append", "get", "strip", "split", "exists", "readlines", "join"}
                filtered_called_names = [name for name in called_names if name not in builtin_filters]

                target_symbols = list(set(defined_names + filtered_called_names + file_ref_names))
                print(f"   📦 [양방향 통합] 징집 대상 심볼 목록: {target_symbols}")
                
                symbols_list = self.symbols_data.get("symbols", [])
                print(f"   📚 로드된 JSON 장부 총 심볼 개수: {len(symbols_list)}개")

                for target_name in target_symbols:
                    print(f"      🔎 [전역 심볼 대조] 이름: '{target_name}' -> 장부 전체 스캔 중...")
                    match_found = False
                    
                    for s in symbols_list:
                        if s.get("name") == target_name:
                            match_found = True
                            t_file = s.get("path") or s.get("file", "")
                            s_start = s.get("start_line", 1)
                            s_end = s.get("end_line", 1)

                            # 정방향 연관 심볼 추적
                            if t_file != file_rel_path:
                                print(f"         ➡️ [정방향] 내가 불러온 함수 본체 포착 -> {t_file} ({s_start}~{s_end}라인)")
                                callee_file_path = self.resolve_file_path(t_file)
                                    
                                if callee_file_path:
                                    with open(callee_file_path, "r", encoding="utf-8") as cf:
                                        cf_lines = cf.readlines()
                                    
                                    s_start = max(1, min(s_start, len(cf_lines)))
                                    s_end = max(s_start, min(s_end, len(cf_lines)))
                                    callee_code = "".join(cf_lines[s_start - 1 : s_end])
                                    
                                    if not any(x["file"] == t_file and x["line_range"] == f"{s_start}-{s_end}" for x in extracted_slices):
                                        extracted_slices.append({
                                            "req_num": f"{req_num} ➡️ 불러온함수 ({target_name} 본체)",
                                            "file": t_file,
                                            "line_range": f"{s_start}-{s_end}",
                                            "code": callee_code
                                        })

                            # 역방향 연관 심볼 추적 (used_by)
                            if (target_name in defined_names) or (t_file == file_rel_path):
                                ub_list = s.get("used_by", [])
                                if ub_list:
                                    print(f"         ⬅️ [역방향] 나를 부르는 전역 호출처 목록(used_by): {ub_list}")
                                    for ub_id in ub_list:
                                        if "::" in ub_id:
                                            ub_file, ub_symbol_name = ub_id.split("::", 1)
                                            if "." in ub_symbol_name:
                                                ub_symbol_name = ub_symbol_name.split(".")[-1]
                                            
                                            sub_match_found = False
                                            for target_s in symbols_list:
                                                sub_t_file = target_s.get("path") or target_s.get("file", "")
                                                s_id = target_s.get("symbol_id", "")
                                                sub_s_name = target_s.get("name", "")
                                                
                                                if (s_id == ub_id) or (ub_id.endswith(s_id)) or (sub_s_name == ub_symbol_name and (sub_t_file == ub_file or ub_file.endswith(sub_t_file) or sub_t_file.endswith(ub_file))):
                                                    sub_match_found = True
                                                    ub_file_path = self.resolve_file_path(sub_t_file)
                                                        
                                                    if ub_file_path:
                                                        with open(ub_file_path, "r", encoding="utf-8") as ubf:
                                                            ub_lines = ubf.readlines()
                                                        
                                                        ubs_start = max(1, min(target_s.get("start_line", 1), len(ub_lines)))
                                                        ubs_end = max(ubs_start, min(target_s.get("end_line", len(ub_lines)), len(ub_lines)))
                                                        ub_slice_code = "".join(ub_lines[ubs_start - 1 : ubs_end])
                                                        
                                                        if not any(x["file"] == sub_t_file and x["line_range"] == f"{ubs_start}-{ubs_end}" for x in extracted_slices):
                                                            extracted_slices.append({
                                                                "req_num": f"{req_num} 🔗 제이슨연동 ({target_name} 호출처 -> {sub_t_file}의 [{sub_s_name}])",
                                                                "file": sub_t_file,
                                                                "line_range": f"{ubs_start}-{ubs_end}",
                                                                "code": ub_slice_code
                                                            })
                                            if not sub_match_found:
                                                print(f"            ❌ [ERROR] 호출처 구조체 '{ub_id}'를 장부에서 찾지 못했습니다.")
                    
                    if not match_found:
                        print(f"      ❓ [NOT FOUND] 코드엔 찍혀있는데 JSON 장부({file_rel_path})엔 등록 안 된 심볼입니다.")

            except Exception as e:
                import traceback
                print(f"💥 [CRITICAL ERROR] 슬라이싱 중 예외 발생: {e}")
                traceback.print_exc()

            req_num += 1

        print("\n" + "="*60)
        print(f"🏁 최종 반환할 총 슬라이스 묶음 개수: {len(extracted_slices)}개")
        print("="*60 + "\n")
        return extracted_slices

    def format_as_markdown(self, extracted_slices: list[dict]) -> str:
        """
        슬라이싱 데이터 배열을 받아서 LLM 및 에이전트에 주입할 마크다운 문맥으로 변환합니다.
        """
        if not extracted_slices:
            return ""

        md_lines = []
        md_lines.append("# ==========================================================================")
        md_lines.append("# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드")
        md_lines.append(f"# [SCAN_MODE] {self.scan_mode}")
        md_lines.append("# ==========================================================================")

        for slc in extracted_slices:
            md_lines.append(f"# 📄 [요청 {slc['req_num']}] TARGET: {slc['file']} ({slc['line_range']}라인)")
            md_lines.append("# ----------------------------------------------------------")
            md_lines.append("```python")
            md_lines.append(slc["code"].rstrip())
            md_lines.append("```\n")

        return "\n".join(md_lines)

    def process(self, raw_prompt: str, auto_save: bool = True, output_path: str | Path = None) -> dict:
        """
        [통합 매니저 파이프라인]
        프롬프트를 입력받아 슬라이스를 추출하고, 마크다운 반환 및 마스터 격리 폴더로 내보냅니다.
        
        Returns:
            dict: {
                "slices": list[dict],    # 원본 데이터 객체 목록
                "markdown": str,         # 생성된 마크다운 텍스트
                "saved_path": Path|None  # 저장된 실제 경로
            }
        """
        slices = self.extract_multi_slices(raw_prompt)
        markdown_text = self.format_as_markdown(slices)
        save_target_path = None

        if auto_save and markdown_text:
            if output_path:
                save_target_path = Path(output_path)
            else:
                save_target_path = self.raw_root_dir / "system_maps" / "extracted_context.md"

            try:
                save_target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_target_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)
                print(f"💾 마크다운 데이터가 안전하게 저장되었습니다: {save_target_path}")
            except Exception as e:
                print(f"⚠️ 파일 저장 실패: {e}")

        return {
            "slices": slices,
            "markdown": markdown_text,
            "saved_path": save_target_path
        }
```

--------------------------------------------------

### 📄 tools/multi_agent_system/agent_session.py
#### 🧱 Code Skeleton:
```python
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
```

--------------------------------------------------

### 📄 tools/multi_agent_system/code_patcher.py
#### 🧱 Code Skeleton:
```python
class CodePatcher:
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir).resolve()

    def apply_patch(self, rel_path: str, existing_code: str, replacement_code: str) -> dict:
        """
        파일 내에서 existing_code를 검증하여 replacement_code로 1:1 교체합니다.
        """
        target_path = (self.root_dir / rel_path.strip().replace("\\", "/")).resolve()
        
        if not target_path.exists() or not target_path.is_file():
            return {
                "success": False,
                "message": f"❌ [PATCH FAIL] 대상 파일을 찾을 수 없습니다: {rel_path}"
            }

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 줄바꿈 단일화 (CRLF / LF 오차로 인한 매칭 실패 방지)
            clean_content = content.replace("\r\n", "\n")
            clean_existing = existing_code.replace("\r\n", "\n").strip()
            clean_replacement = replacement_code.replace("\r\n", "\n").strip()

            # 1. 100% 완전 일치 여부 검증
            if clean_existing not in clean_content:
                return {
                    "success": False,
                    "message": f"❌ [PATCH FAIL] 입력한 '기존 코드'가 {rel_path} 파일 내에 100% 일치하는 구간이 없습니다. 정확한 슬라이스를 지정하세요."
                }

            # 2. 파일 내 동일한 기존 코드가 2개 이상 존재하는지 출현 횟수 검증 (중복 치환 방지)
            match_count = clean_content.count(clean_existing)
            if match_count > 1:
                return {
                    "success": False,
                    "message": f"⚠️ [PATCH FAIL] 지정한 '기존 코드'가 {rel_path} 내에 {match_count}개 존재합니다. 문맥(전후 라인)을 더 포함하여 유일하게 지정하세요."
                }

            # 3. 핀포인트 1:1 정밀 치환 실행
            patched_content = clean_content.replace(clean_existing, clean_replacement, 1)

            # 4. 파일 저장
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(patched_content)

            return {
                "success": True,
                "message": f"✅ [PATCH SUCCESS] {rel_path} 파일의 특정 구간이 성공적으로 수정되었습니다!"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"💥 [PATCH ERROR] 파일 수정 중 예외 발생: {e}"
            }
```

--------------------------------------------------

### 📄 tools/multi_agent_system/terminal_runner.py
#### 🧱 Code Skeleton:
```python
def run_terminal_command(command: str, cwd: str = None, timeout: int = 30) -> str:
    """
    터미널 명령어를 실행하고 stdout 및 stderr 결과를 반환합니다.
    
    Args:
        command: 실행할 명령어 (예: "python run_test.py", "pytest", "npm test")
        cwd: 명령어를 실행할 작업 디렉토리 경로 (기본값: 프로젝트 루트)
        timeout: 최대 실행 대기 시간(초)
    """
    for forbidden in FORBIDDEN_COMMANDS:
        if forbidden in command.lower():
            return f"❌ [보안 거부] 위험 키워드가 포함된 명령어는 실행이 차단되었습니다: '{forbidden}'"

    # 프로젝트 루트 경로 자동 설정
    work_dir = cwd if cwd else str(Path(__file__).parent.parent.parent.resolve())

    print(f"\n💻 [TERMINAL TOOL] 명령어 실행 중: `{command}` (경로: {work_dir})")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=work_dir,
            timeout=timeout
        )

        output = []
        if result.stdout:
            output.append(f"--- [STDOUT (정상 출력)] ---\n{result.stdout.strip()}")
        if result.stderr:
            output.append(f"--- [STDERR (에러 로그)] ---\n{result.stderr.strip()}")

        if not output:
            return f"✅ 명령어 실행 완료 (반환 코드: {result.returncode}, 출력 없음)"

        status_msg = "✅ 실행 성공" if result.returncode == 0 else f"⚠️ 실행 종료 (오류 코드: {result.returncode})"
        return f"{status_msg}\n\n" + "\n\n".join(output)

    except subprocess.TimeoutExpired:
        return f"⏰ [타임아웃] 명령어 실행 시간이 {timeout}초를 초과하여 강제 종료되었습니다."
    except Exception as e:
        return f"💥 [실행 예외 발생] {str(e)}"
```

--------------------------------------------------

### 📄 tools/universal_indexer/agent_navigator.py
#### 🧱 Code Skeleton:
```python
class CodeExtractor:
    """
    UI(Navigator) 전용 독립 코드 추출기
    - agent_code_extractor.py의 수정 및 위치 변경에 절대 영향을 받지 않는 독자 엔진
    """
    def __init__(self, root_dir: str | Path):
        self.raw_root_dir = Path(root_dir).resolve()
        self.scan_mode = "ROOT"
        
        try:
            idx_path = str((self.raw_root_dir / "tools" / "universal_indexer").resolve())
            if idx_path not in sys.path:
                sys.path.insert(0, idx_path)
            
            import switch
            self.scan_mode = getattr(switch, "SCAN_MODE", "ROOT")
            print(f"🎛️ [SWITCH DETECTED] 현재 탐색 스위치 모드: {self.scan_mode}")
        except Exception as e:
            print(f"⚠️ [SWITCH WARNING] switch.py를 로드하지 못해 기본 'ROOT' 모드로 동작합니다. (이유: {e})")

        if self.scan_mode == "SRC":
            self.root_dir = self.raw_root_dir / "src"
            print(f"📁 [MODE: SRC] 탐색 마스터 루트가 복사/격리용 src 폴더로 변경되었습니다: {self.root_dir}")
        else:
            self.root_dir = self.raw_root_dir
            print(f"📁 [MODE: ROOT] 탐색 마스터 루트가 프로젝트 원본 루트로 설정되었습니다: {self.root_dir}")

        self.symbols_path = self.raw_root_dir / "system_memory" / ".jjap_symbols.json"
        self.symbols_data = self._load_database()

    def _load_database(self) -> dict:
        if not self.symbols_path.exists():
            return {"symbols": []}
        try:
            with open(self.symbols_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"symbols": []}

    def resolve_file_path(self, raw_path_str: str) -> Path | None:
        clean_path_str = raw_path_str.strip().replace("\\", "/")
        
        if self.scan_mode == "SRC":
            if clean_path_str.startswith("src/src/"):
                candidate = self.raw_root_dir / clean_path_str
            elif clean_path_str.startswith("src/"):
                candidate = self.raw_root_dir / clean_path_str
            else:
                candidate = self.raw_root_dir / "src" / clean_path_str
        else:
            candidate = self.raw_root_dir / clean_path_str

        if candidate.exists() and candidate.is_file():
            return candidate

        candidate_raw = self.raw_root_dir / clean_path_str
        if candidate_raw.exists() and candidate_raw.is_file():
            return candidate_raw

        candidate_target = self.raw_root_dir / "extraction_target_project" / clean_path_str
        if candidate_target.exists() and candidate_target.is_file():
            return candidate_target

        candidate_tools = self.raw_root_dir / "tools" / clean_path_str
        if candidate_tools.exists() and candidate_tools.is_file():
            return candidate_tools

        return None

    def extract_multi_slices(self, raw_prompt: str) -> list[dict]:
        print("\n" + "="*60)
        print("🚨 [EXTRACTOR ON] 멀티 슬라이싱 파이프라인 기동!!!")
        print(f"📥 유저 입력 프롬프트: {repr(raw_prompt)}")
        print(f"⚙️ 현재 매핑 모드: {self.scan_mode} (기준 경로: {self.root_dir})")
        print("="*60)

        pattern = r"([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\s:]+(?:L)?(\d+)(?:\s*-\s*(?:L)?(\d+))?"
        matches = re.findall(pattern, raw_prompt)

        print(f"🔍 정규식 1차 타겟 스캔 결과: {matches}")
        if not matches:
            print("⚠️ 매칭되는 파일 경로 및 라인 규격이 없습니다. 빈 배열 리턴.")
            return []

        extracted_slices = []
        req_num = 1

        for match in matches:
            file_rel_path = match[0].strip().replace("\\", "/")
            start_line = int(match[1])
            end_line = int(match[2]) if match[2] else start_line

            print(f"\n🎯 [요청 #{req_num}] 메인 타겟 분석 시작 -> {file_rel_path} ({start_line} ~ {end_line} 라인)")

            target_file_path = self.resolve_file_path(file_rel_path)
            
            if not target_file_path:
                print(f"   ❌ [ERROR] 해당 파일이 실제 경로에 존재하지 않습니다! 패스합니다: {file_rel_path}")
                continue

            print(f"   🟢 [경로 확정] 디스크 실체 발견: {target_file_path}")

            try:
                with open(target_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                total_lines = len(lines)
                safe_start = max(1, min(start_line, total_lines))
                safe_end = max(safe_start, min(end_line, total_lines))
                print(f"   📏 파일 전체 줄 수: {total_lines} | 보정된 안전 범위: {safe_start} ~ {safe_end}")

                slice_lines = lines[safe_start - 1 : safe_end]
                slice_code = "".join(slice_lines)
                print(f"   🟢 1차 메인 슬라이싱 성공 (길이: {len(slice_code)}자)")

                extracted_slices.append({
                    "req_num": f"{req_num}",
                    "file": file_rel_path,
                    "line_range": f"{safe_start}-{safe_end}",
                    "code": slice_code
                })

                print(f"   📡 [2차 사냥기] 잘려 나온 텍스트 내부에서 양방향 심볼 식별 개시...")

                defined_names = re.findall(r"(?:def|class)\s+([a-zA-Z0-9_]+)", slice_code)
                called_names = re.findall(r"(?:[a-zA-Z0-9_]+\.)?([a-zA-Z0-9_]+)\s*\(", slice_code)
                file_ref_names = [f for f in re.findall(r'[\'"]([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\'"]', slice_code) if f != file_rel_path]

                builtin_filters = {"print", "len", "range", "open", "dict", "list", "set", "any", "all", "max", "min", "append", "get", "strip", "split", "exists", "readlines", "join"}
                filtered_called_names = [name for name in called_names if name not in builtin_filters]

                target_symbols = list(set(defined_names + filtered_called_names + file_ref_names))
                print(f"   📦 [양방향 통합] 징집 대상 심볼 목록: {target_symbols}")
                
                symbols_list = self.symbols_data.get("symbols", [])
                print(f"   📚 로드된 JSON 장부 총 심볼 개수: {len(symbols_list)}개")

                for target_name in target_symbols:
                    print(f"      🔎 [전역 심볼 대조] 이름: '{target_name}' -> 장부 전체 스캔 중...")
                    match_found = False
                    
                    for s in symbols_list:
                        if s.get("name") == target_name:
                            match_found = True
                            t_file = s.get("path") or s.get("file", "")
                            s_start = s.get("start_line", 1)
                            s_end = s.get("end_line", 1)

                            if t_file != file_rel_path:
                                print(f"         ➡️ [정방향] 내가 불러온 함수 본체 포착 -> {t_file} ({s_start}~{s_end}라인)")
                                callee_file_path = self.resolve_file_path(t_file)
                                    
                                if callee_file_path:
                                    with open(callee_file_path, "r", encoding="utf-8") as cf:
                                        cf_lines = cf.readlines()
                                    
                                    s_start = max(1, min(s_start, len(cf_lines)))
                                    s_end = max(s_start, min(s_end, len(cf_lines)))
                                    callee_code = "".join(cf_lines[s_start - 1 : s_end])
                                    
                                    if not any(x["file"] == t_file and x["line_range"] == f"{s_start}-{s_end}" for x in extracted_slices):
                                        extracted_slices.append({
                                            "req_num": f"{req_num} ➡️ 불러온함수 ({target_name} 본체)",
                                            "file": t_file,
                                            "line_range": f"{s_start}-{s_end}",
                                            "code": callee_code
                                        })

                            if (target_name in defined_names) or (t_file == file_rel_path):
                                ub_list = s.get("used_by", [])
                                if ub_list:
                                    print(f"         ⬅️ [역방향] 나를 부르는 전역 호출처 목록(used_by): {ub_list}")
                                    for ub_id in ub_list:
                                        if "::" in ub_id:
                                            ub_file, ub_symbol_name = ub_id.split("::", 1)
                                            if "." in ub_symbol_name:
                                                ub_symbol_name = ub_symbol_name.split(".")[-1]
                                            
                                            sub_match_found = False
                                            for target_s in symbols_list:
                                                sub_t_file = target_s.get("path") or target_s.get("file", "")
                                                s_id = target_s.get("symbol_id", "")
                                                sub_s_name = target_s.get("name", "")
                                                
                                                if (s_id == ub_id) or (ub_id.endswith(s_id)) or (sub_s_name == ub_symbol_name and (sub_t_file == ub_file or ub_file.endswith(sub_t_file) or sub_t_file.endswith(ub_file))):
                                                    sub_match_found = True
                                                    ub_file_path = self.resolve_file_path(sub_t_file)
                                                        
                                                    if ub_file_path:
                                                        with open(ub_file_path, "r", encoding="utf-8") as ubf:
                                                            ub_lines = ubf.readlines()
                                                        
                                                        ubs_start = max(1, min(target_s.get("start_line", 1), len(ub_lines)))
                                                        ubs_end = max(ubs_start, min(target_s.get("end_line", len(ub_lines)), len(ub_lines)))
                                                        ub_slice_code = "".join(ub_lines[ubs_start - 1 : ubs_end])
                                                        
                                                        if not any(x["file"] == sub_t_file and x["line_range"] == f"{ubs_start}-{ubs_end}" for x in extracted_slices):
                                                            extracted_slices.append({
                                                                "req_num": f"{req_num} 🔗 제이슨연동 ({target_name} 호출처 -> {sub_t_file}의 [{sub_s_name}])",
                                                                "file": sub_t_file,
                                                                "line_range": f"{ubs_start}-{ubs_end}",
                                                                "code": ub_slice_code
                                                            })
                                            if not sub_match_found:
                                                print(f"            ❌ [ERROR] 호출처 구조체 '{ub_id}'를 장부에서 찾지 못했습니다.")
                    
                    if not match_found:
                        print(f"      ❓ [NOT FOUND] 코드엔 찍혀있는데 JSON 장부({file_rel_path})엔 등록 안 된 심볼입니다.")

            except Exception as e:
                import traceback
                print(f"💥 [CRITICAL ERROR] 슬라이싱 중 예외 발생: {e}")
                traceback.print_exc()

            req_num += 1

        print("\n" + "="*60)
        print(f"🏁 최종 반환할 총 슬라이스 묶음 개수: {len(extracted_slices)}개")
        print("="*60 + "\n")
        return extracted_slices

    def format_as_markdown(self, extracted_slices: list[dict]) -> str:
        if not extracted_slices:
            return ""

        md_lines = []
        md_lines.append("# ==========================================================================")
        md_lines.append("# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드")
        md_lines.append(f"# [SCAN_MODE] {self.scan_mode}")
        md_lines.append("# ==========================================================================")

        for slc in extracted_slices:
            md_lines.append(f"# 📄 [요청 {slc['req_num']}] TARGET: {slc['file']} ({slc['line_range']}라인)")
            md_lines.append("# ----------------------------------------------------------")
            md_lines.append("```python")
            md_lines.append(slc["code"].rstrip())
            md_lines.append("```\n")

        return "\n".join(md_lines)

    def process(self, raw_prompt: str, auto_save: bool = True, output_path: str | Path = None) -> dict:
        slices = self.extract_multi_slices(raw_prompt)
        markdown_text = self.format_as_markdown(slices)
        save_target_path = None

        if auto_save and markdown_text:
            if output_path:
                save_target_path = Path(output_path)
            else:
                save_target_path = self.raw_root_dir / "system_maps" / "extracted_context.md"

            try:
                save_target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_target_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)
                print(f"💾 마크다운 데이터가 안전하게 저장되었습니다: {save_target_path}")
            except Exception as e:
                print(f"⚠️ 파일 저장 실패: {e}")

        return {
            "slices": slices,
            "markdown": markdown_text,
            "saved_path": save_target_path
        }

class JjapCursorNavigatorGUI:
    def __init__(self, root, project_root: Path):
        self.root = root
        self.project_root = project_root
        self.extractor = CodeExtractor(project_root)
        self.last_markdown_content = ""

        # GUI Title에 현재 스캔 모드를 가독성 있게 표기
        self.root.title(f"⚡ Jjap-Cursor Agent Navigator v2.0 (Auto-Exporter) | 모드: {self.extractor.scan_mode}")
        self.root.geometry("1000x750")

        self.main_container = ttk.Frame(root, padding="10")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        input_label = ttk.Label(self.main_container, text=f"📥 [에이전트 요청 프롬프트 입력 구역 - 현재 모드: {self.extractor.scan_mode}]", font=("Malgun Gothic", 11, "bold"))
        input_label.pack(anchor=tk.W, pady=(0, 5))

        self.prompt_input = tk.Text(self.main_container, height=6, font=("Malgun Gothic", 10))
        self.prompt_input.pack(fill=tk.X, pady=(0, 10))
        
        # 안내 문구 최적화
        if self.extractor.scan_mode == "SRC":
            self.prompt_input.insert(tk.END, "💡 실전 테스트 양식 예시 (SRC 모드):\nsrc/src/main/java/com/desertcore/deathevent.java:32-60")
        else:
            self.prompt_input.insert(tk.END, "💡 실전 테스트 양식 예시 (ROOT 모드):\nsrc/main/java/com/desertcore/deathevent.java:32-60")

        self.btn_frame = ttk.Frame(self.main_container)
        self.btn_frame.pack(fill=tk.X, pady=(0, 10))

        self.scan_button = ttk.Button(
            self.btn_frame, 
            text="⚡ 소스코드 정밀 슬라이싱 및 컨텍스트 바인딩 가동 ⚡", 
            command=self.execute_slicing_pipeline
        )
        self.scan_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.export_button = ttk.Button(
            self.btn_frame,
            text="💾 마크다운 파일(.md) 개별 내보내기",
            command=self.manual_export_file,
            state=tk.DISABLED
        )
        self.export_button.pack(side=tk.RIGHT, padx=(5, 0))

        output_label = ttk.Label(self.main_container, text="📄 [AI 배송용 최적화 켄텍스트 보따리 (출력 결과)]", font=("Malgun Gothic", 11, "bold"))
        output_label.pack(anchor=tk.W, pady=(0, 5))

        self.code_display = tk.Text(self.main_container, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        self.code_display.pack(fill=tk.BOTH, expand=True)

        self.status_label = ttk.Label(self.main_container, text=f"🟢 대기 중... [{self.extractor.scan_mode} 모드] 프롬프트를 입력하고 가동 버튼을 누르십시오.", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=(10, 0))

    def execute_slicing_pipeline(self):
        raw_prompt = self.prompt_input.get("1.0", tk.END).strip()
        if not raw_prompt or raw_prompt.startswith("💡"):
            messagebox.showwarning("입력 오류", "형님, 슬라이싱할 대상 파일 경로와 라인을 입력해 주십시오!")
            return

        result = self.extractor.process(raw_prompt, auto_save=True)
        extracted_slices = result["slices"]

        if not extracted_slices:
            self.status_label.config(text="❌ 추출 실패: 프롬프트에서 타겟 패턴('경로:줄번호')을 인식하지 못했습니다.")
            messagebox.showerror("추출 실패", "지정된 경로 문자열 형식을 확인해 주십시오.")
            return

        self.code_display.delete("1.0", tk.END)
        self.last_markdown_content = result["markdown"]
        self.code_display.insert(tk.END, self.last_markdown_content)
        
        saved_path = result.get("saved_path")
        if saved_path:
            status_msg = f"🟢 [{self.extractor.scan_mode}] 추출 및 마크다운 자동 저장 완료! -> system_maps/{saved_path.name}"
            self.export_button.config(state=tk.NORMAL)
        else:
            status_msg = f"⚠️ 화면 추출 완료했으나 자동 파일 저장 실패"

        self.status_label.config(text=status_msg)
        
    def manual_export_file(self):
        if not self.last_markdown_content:
            return
        
        file_path = filedialog.asksaveasfilename(
            initialdir=str(self.project_root),
            title="마크다운 컨텍스트 파일 저장",
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.last_markdown_content)
                messagebox.showinfo("내보내기 성공", f"형님, 성공적으로 파일을 내보냈습니다!\n📂 경로: {file_path}")
            except Exception as e:
                messagebox.showerror("내보내기 실패", f"파일 저장 중 에러가 발생했습니다: {e}")
```

--------------------------------------------------

### 📄 tools/universal_indexer/config.py
#### 🧱 Code Skeleton:
```python
def get_project_root() -> Path:
    """
    현재 파일의 위치를 기준으로 프로젝트의 마스터 루트 디렉토리를 역추적하여 반환합니다.
    `tools/universal_indexer` 구조 내부 또는 루트에 위치한 경우 모두 대응합니다.
    """
    script_dir = Path(__file__).parent.resolve()
    if script_dir.name == "universal_indexer" and script_dir.parent.name == "tools":
        return script_dir.parent.parent
    return script_dir

def get_scan_mode() -> str:
    """switch.py의 SCAN_MODE 상태를 동적으로 확인합니다."""
    try:
        from switch import SCAN_MODE
        return SCAN_MODE
    except ImportError:
        try:
            from tools.universal_indexer.switch import SCAN_MODE
            return SCAN_MODE
        except ImportError:
            return "ROOT"
```

--------------------------------------------------

### 📄 tools/universal_indexer/context_builder.py
#### 🧱 Code Skeleton:
```python
class ContextBuilder:
    """날것의 소스코드를 정화하여 AI가 가장 좋아하는 영양가 있는 형태로 가공하는 비서 클래스입니다."""

    def __init__(self, project_root: str) -> None:
        """비서관을 초기화하며 기준이 되는 프로젝트 루트 경로를 지정합니다."""
        self.project_root = Path(project_root)
        self.ignore_matcher = GitIgnoreMatcher(self.project_root)

    def read_and_clean_file(self, relative_path: str) -> str:
        """파일을 읽어서 사람용 주석(# INFO:) 내용은 완전히 비우되,
        줄바꿈과 콤팩트한 줄 번호 태그만 강제로 남겨서 토큰을 최소화하고
        AI와 인간의 라인 인덱스를 100% 동기화하는 개조 함수입니다.
        """
        file_path = self.project_root / relative_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"요청하신 경로에 파일이 존재하지 않습니다: {relative_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        cleaned_lines = []
        in_multiline_comment = False

        # enumerate를 사용해 파일 원본의 물리적인 줄 번호(1부터 시작)를 정확히 추적합니다.
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            # 1. 다중행 주석(""") 상태 머신 처리 블록
            if in_multiline_comment:
                cleaned_lines.append(f"[{idx:03d}]\n")
                if '"""' in stripped or "'''" in stripped:
                    in_multiline_comment = False
                continue
            else:
                if '"""' in stripped or "'''" in stripped:
                    quote_symbol = '"""' if '"""' in stripped else "'''"
                    quote_count = stripped.count(quote_symbol)
                    
                    if quote_count % 2 == 0:
                        # 한 줄짜리 Docstring (""" text """) -> 주석 처리 후 multiline 플래그는 False 유지
                        cleaned_lines.append(f"[{idx:03d}]\n")
                        continue
                    else:
                        # 홀수 개 -> 멀티라인 주석 시작
                        in_multiline_comment = True
                        cleaned_lines.append(f"[{idx:03d}]\n")
                        continue

            # ⭐ 형님의 핵심 지시사항: 주석 부분은 내용을 비운 채 억지로 줄 표시를 유지!
            # 2. # INFO: 로 시작하는 주석행 처리
            if stripped.startswith("# INFO:"):
                # 💡 핵심: 긴 주석 텍스트를 다 날려버리고 오직 줄 번호 태그와 개행만 주입 (토큰 최소화!)
                cleaned_lines.append(f"[{idx:03d}]\n")
                continue

            # 3. 코드 옆에 붙은 꼬리표 주석 예외 처리 (`x = 1  # INFO: ...`)
            if " # INFO:" in line:
                # 주석 내용만 잘라내고, 코드 앞단에 줄 번호를 붙여서 재조립
                pure_code = line.split(" # INFO:")[0]
                cleaned_lines.append(f"[{idx:03d}]{pure_code}\n")
                continue

            # 4. 일반 빈 줄 처리
            if not stripped:
                cleaned_lines.append(f"[{idx:03d}]\n")
                continue

            # 5. 그 외의 순수 실행 코드 및 보존 주석 (# HISTORY:, # FIX:)
            # AI가 토큰을 해석할 때 밀리지 않도록 고정형 태그를 맨 앞에 강제 주입합니다.
            cleaned_lines.append(f"[{idx:03d}]{line}")

        return "".join(cleaned_lines)

    def assemble_ai_prompt(self, user_query: str, affected_files: list[str]) -> str:
        """검열된 파일 소스코드들과 형님의 최종 질문을 엮어서 저(Gemini)에게 배송할 최종 프롬프트 보따리를 조립합니다.
        
        🛠️ 내가 내부에서 부려먹는 함수:
        - `self.read_and_clean_file()`: 각 파일들을 돌면서 `# INFO:` 주석을 청소하라고 지시함.
        """
        prompt_parts = []
        prompt_parts.append(f"=== USER REQUEST ===\n{user_query}\n\n")
        prompt_parts.append("=== CLEANED CONTEXT CODEBASE ===\n")
        prompt_parts.append("아래 소스코드들은 토큰 절약을 위해 불필요한 설명 주석(# INFO:)이 제거되고, ")
        prompt_parts.append("과거 오류 수정 내역(# HISTORY:)만 온전히 보존된 청정 코드입니다.\n\n")

        for rel_path in affected_files:
            # 🛡️ 1차 방어선: 장부 보관소(system_memory) 파일만 절대 차단!
            # (system_maps는 AI 지도 용도이므로 프롬프트 탑재 허용)
            str_path = str(rel_path)
            if "system_memory" in str_path:
                continue

            # 🛡️ 2차 방어선: .gitignore 지능형 파서 적용
            if self.ignore_matcher.is_ignored(rel_path):
                continue

            prompt_parts.append(f"--- FILE: {rel_path} ---")
            try:
                purified_code = self.read_and_clean_file(rel_path)
                prompt_parts.append(purified_code)
            except Exception as e:
                prompt_parts.append(f"파일을 읽는 중 오류 발생: {str(e)}")
            prompt_parts.append("\n")

        return "\n".join(prompt_parts)
```

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/cs_parser.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/gitignore_parser.py
#### 🧱 Code Skeleton:
```python
class GitIgnoreMatcher:
    """프로젝트 내 모든 .gitignore 패턴을 수집하고 정밀 검증하는 전용 파서"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self._spec = None

    def _load_specs(self):
        """지연 로딩(Lazy Loading)으로 모든 .gitignore 파일 수집 및 통합 파싱"""
        patterns = []
        
        # 디폴트 제외 대상 기본 포함 (최적화 및 필수 방어)
        default_ignores = [
            ".git/", ".venv/", "node_modules/", "__pycache__/",
            "system_memory/", "system_maps/"
        ]
        patterns.extend(default_ignores)

        for root, _, files in os.walk(self.project_root):
            if ".gitignore" in files:
                gitignore_path = Path(root) / ".gitignore"
                rel_dir = Path(root).relative_to(self.project_root).as_posix()
                prefix = "" if rel_dir == "." else f"{rel_dir}/"

                try:
                    with open(gitignore_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                patterns.append(f"{prefix}{line}")
                except Exception:
                    pass

        if pathspec:
            self._spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
        else:
            self._spec = patterns

    def is_ignored(self, relative_path: str) -> bool:
        """파일 경로가 .gitignore 패턴에 연관되는지 평가 (O(1) 캐싱 스펙 활용)"""
        if self._spec is None:
            self._load_specs()

        posix_path = Path(relative_path).as_posix()

        if pathspec and isinstance(self._spec, pathspec.PathSpec):
            return self._spec.match_file(posix_path)

        # Fallback: simple prefix checking
        return any(posix_path.startswith(pat.rstrip("/")) for pat in self._spec)
```

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/java_parser.py
#### 🧱 Code Skeleton:
```python
def _find_matching_curly_brace(lines: list, start_line_idx: int) -> int:
    """
    자바의 중괄호 { } 쌍을 정밀 추적하여 메서드/클래스의 실제 종료 줄 번호(1-based)를 반환합니다.
    """
    brace_count = 0
    opened = False
    
    for idx in range(start_line_idx, len(lines)):
        line = lines[idx]
        # 주석 제거 후 블록 검사
        cleaned_line = re.sub(r'//.*|/\*.*?\*/', '', line)
        
        for char in cleaned_line:
            if char == '{':
                brace_count += 1
                opened = True
            elif char == '}':
                brace_count -= 1
                
        if opened and brace_count <= 0:
            return idx + 1  # 1-based line number
            
    return start_line_idx + 1

def extract_symbols(file_path: Path, project_root: Path):
    """
    ☕ [Java Core Advanced Parser v2.0]
    파이썬과 100% 동일한 5대 장부 규격을 만족하도록 자바 소스를 정밀 해부합니다.
    - 중첩 경로(src/src) 방어선 구축 완료
    - imp: 임포트 패키지 완벽 추출
    - calls: 메서드 내부 호출 분석 엔진 탑재
    - 줄 범위 (시작줄-끝줄) 매칭 완벽 지원
    """
    symbols = []
    file_context = {}
    definition_map = {}
    data_protocols = {}
    registry_constants = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        log(f"❌ 파일 읽기 실패: {file_path} | 에러: {e}")
        return symbols, {}, {}, {}, []

    # 🚨 [교정] 독단적인 src/src/ 축약을 제거하고 실제 디스크 상대 경로 규격을 그대로 보존합니다.
    try:
        raw_rel = file_path.relative_to(project_root).as_posix()
    except ValueError:
        raw_rel = file_path.name

    # 별도의 치환 없이 디스크 실제 경로를 단일 진실 공급원(Single Source of Truth) 키값으로 확정
    rel_path_str = raw_rel

    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    lines = content.splitlines()

    # 1. 🧲 임포트(Imports) 및 패키지 징집
    imports = []
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith("import ") and line_strip.endswith(";"):
            imp_target = line_strip.replace("import ", "").replace(";", "").strip()
            imports.append(imp_target)
            
    imports_str = f"💡 📦 imp: {', '.join(sorted(list(set(imports))))}" if imports else ""

    # 2. 🩻 클래스 및 메서드 심볼 다차원 스캔
    symbols_info_strings = []
    skeleton_segments = []
    
    current_class = None
    class_start_idx = -1

    # 자바 클래스/인터페이스/메서드 탐색 정규식
    class_patt = re.compile(r'(?:public|protected|private|static|\s)+\s+(?:class|interface|enum)\s+([a-zA-Z0-9_]+)')
    method_patt = re.compile(r'(?:public|protected|private|static|\s)+\s+[\w<>\s?\[\]]+\s+([a-zA-Z0-9_]+)\s*\([^)]*\)\s*(?:throws\s+[\w\s,]+)?\s*\{?')

    for idx, line in enumerate(lines):
        line_num = idx + 1
        line_stripped = line.strip()
        
        # 주석이나 공백 라인은 스킵
        if line_stripped.startswith("//") or line_stripped.startswith("*") or not line_stripped:
            continue

        # A. 클래스 탐지
        class_match = class_patt.search(line)
        if class_match:
            c_name = class_match.group(1)
            current_class = c_name
            class_start_idx = idx
            end_line = _find_matching_curly_brace(lines, idx)
            
            param_match = re.search(r'\((.*?)\)', line_stripped)
            params_str = ""
            if param_match:
                raw_params = param_match.group(1).strip()
                if raw_params:
                    param_types = [p.strip().split()[0] for p in raw_params.split(",") if p.strip()]
                    params_str = ", ".join(param_types)

            symbols_info_strings.append(f"🧬 class {c_name} [L{line_num}-{end_line}]")
            skeleton_segments.append(f"class {c_name} {{ // L{line_num}-{end_line}")
            
            c_id = f"{rel_path_str}::{c_name}"
            symbols.append({
                "symbol_id": c_id,
                "name": c_name, "full_name": c_name, "type": "class",
                "path": rel_path_str, "start_line": line_num, "end_line": end_line,
                "calls": [], "used_by": []
            })
            definition_map[c_id] = f"{rel_path_str}:{line_num}"
            continue

        # B. 메서드 탐지 및 인자(파라미터) 정밀 추출
        method_match = method_patt.search(line)
        if method_match and ("(" in line_stripped and "import " not in line_stripped):
            m_name = method_match.group(1)
            
            if m_name in ["if", "for", "while", "switch", "catch", "return"]:
                continue
                
            param_match = re.search(r'\((.*?)\)', line_stripped)
            params_str = ""
            if param_match:
                raw_params = param_match.group(1).strip()
                if raw_params:
                    param_types = [p.strip().split()[0] for p in raw_params.split(",") if p.strip()]
                    params_str = ", ".join(param_types)

            end_line = _find_matching_curly_brace(lines, idx)
            
            # 메서드 바디 본문 추출 (내부 호출 함수 파싱용)
            body_lines = lines[idx:end_line]
            body_text = "\n".join(body_lines)
            
            # 내부 호출 추적
            possible_calls = re.findall(r'([a-zA-Z0-9_]+)\s*\(', body_text)
            detected_calls = [
                name for name in possible_calls 
                if name not in ["if", "for", "while", "switch", "catch", "synchronized", "super", "this", m_name]
            ]
            detected_calls = list(set(detected_calls))

            if current_class:
                m_id = f"{rel_path_str}::{current_class}.{m_name}"
                full_name = f"{current_class}.{m_name}"
                symbols_info_strings.append(f"🎯 def {m_name}({params_str}) [L{line_num}-{end_line}]")
                skeleton_segments.append(f"    {line_stripped} // L{line_num}-{end_line}")
            else:
                m_id = f"{rel_path_str}::{m_name}"
                full_name = m_name
                symbols_info_strings.append(f"🎯 def {m_name}({params_str}) [L{line_num}-{end_line}]")
                skeleton_segments.append(f"{line_stripped} // L{line_num}-{end_line}")

            symbols.append({
                "symbol_id": m_id, "name": m_name, "full_name": full_name, "type": "method",
                "path": rel_path_str, "start_line": line_num, "end_line": end_line,
                "calls": detected_calls, "used_by": []
            })
            definition_map[m_id] = f"{rel_path_str}:{line_num}"

    # 3. 🧱 소스 스켈레톤 마감 처리
    skeleton_text = "\n".join(skeleton_segments)

    # 4. 🎚️ 파이썬 마스터 규격 한줄 요약 문자열 조립 완료
    summary_parts = [imports_str] if imports_str else []
    summary_parts.extend(symbols_info_strings)
    symbols_summary_str = " | ".join(summary_parts)

    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": symbols_summary_str,
        "skeleton": skeleton_text
    }

    log(f"✅ 자바 소스 스캔 완료 -> 경로: {rel_path_str} | 심볼: {len(symbols)}개 포착")
    return symbols, file_context, definition_map, data_protocols, registry_constants
```

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/js_parser.py
#### 🧱 Code Skeleton:
```python
def debug_log(message: str):
    if DEBUG:
        print(f"[🐛 DEBUG_JS_PARSER] {message}", file=sys.stderr)

def find_end_line_by_braces(lines: list, start_line_idx: int, max_search_range: int = 500) -> int:
    """
    start_line_idx(0-based)부터 연산량을 제한하여 괄호 짝을 추적합니다.
    - max_search_range: 한 함수/클래스당 최대 500줄만 탐색하여 $O(N^2)$ 폭증 방지
    """
    brace_count = 0
    found_first_open = False
    
    # 탐색 한계선 설정 (파일 끝 또는 최대 500줄 아래)
    max_idx = min(len(lines), start_line_idx + max_search_range)

    for i in range(start_line_idx, max_idx):
        line = lines[i]
        
        # 간단한 주석(//) 제거 후 괄호 카운트 (불필요한 과도 탐색 방지)
        clean_line = line.split('//')[0]
        opens = clean_line.count('{')
        closes = clean_line.count('}')

        if opens > 0 and not found_first_open:
            found_first_open = True
            
        if found_first_open:
            brace_count += (opens - closes)
            
            # 괄호 짝이 맞춰진 순간 연산 즉시 종료
            if brace_count <= 0:
                return i + 1

    # 500줄 안에서 못 찾았거나 닫는 괄호가 없을 경우 기본값 안전하게 반환
    return min(len(lines), start_line_idx + 10)

def extract_symbols(file_path: Path, project_root: Path):
    """
    ⚡ [JavaScript / TypeScript Parser v1.5 - High Performance]
    """
    symbols = []
    file_context = {}
    definition_map = {}
    data_protocols = {}
    registry_constants = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        # debug_log(f"❌ 파일 읽기 실패: {file_path} - 에러: {e}")
        return symbols, {}, {}, {}, []

    try:
        rel_path_str = file_path.relative_to(project_root).as_posix()
    except ValueError:
        rel_path_str = file_path.resolve().relative_to(project_root.resolve()).as_posix()

    # debug_log(f"📂 [File Start] {rel_path_str}")

    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    lines = content.splitlines()

    # 1. 임포트 모듈 포착
    imports = []
    import_matches = re.findall(r'(?:import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]|require\([\'"]([^\'"]+)[\'"]\))', content)
    for m in import_matches:
        imp = m[0] if m[0] else m[1]
        imports.append(imp)
    
    imports_str = f"💡 📦 imp: {', '.join(sorted(list(set(imports))))}" if imports else ""
    symbols_info_strings = []

    class_pattern = re.compile(r'class\s+([A-Za-z0-9_]+)')
    func_pattern = re.compile(
        r'(?:async\s+)?function\s+([A-Za-z0-9_]+)\s*\((.*?)\)|(?:const|let|var)\s+([A-Za-z0-9_]+)\s*=\s*(?:async\s*)?\((.*?)\)\s*=>'
    )
    object_pattern = re.compile(r'(?:const|let|var)\s+([A-Za-z0-9_]+)\s*=\s*\{([^}]+)\}')

    KEYWORDS = ["entity", "platform", "camera", "sensor", "agent", "navigator", "indexer", "retriever", "handler", "service", "controller"]

    for idx, line in enumerate(lines, start=1):
        line_str = line.strip()

        # [A] 클래스 스캔
        c_match = class_pattern.search(line_str)
        if c_match:
            c_name = c_match.group(1)
            c_id = f"{rel_path_str}::{c_name}"
            
            end_line = find_end_line_by_braces(lines, idx - 1)

            symbols_info_strings.append(f"🧬 class {c_name} [L{idx}~L{end_line}]")
            symbols.append({
                "symbol_id": c_id, "name": c_name, "full_name": c_name, "type": "class",
                "path": rel_path_str, "start_line": idx, "end_line": end_line,
                "calls": [], "used_by": []
            })
            definition_map[c_id] = f"{rel_path_str}:{idx}"

            if any(kw in c_name.lower() for kw in KEYWORDS):
                registry_constants.append(c_name)

        # [B] 함수/메서드 스캔
        f_match = func_pattern.search(line_str)
        if f_match:
            # 💡 [변경 1] f_name: 일반 함수는 group(1), 화살표 함수는 group(3)에 들어옵니다.
            f_name = f_match.group(1) or f_match.group(3)
            
            # 💡 [변경 2] f_args: 일반 함수 인자는 group(2), 화살표 함수 인자는 group(4)에 들어옵니다.
            f_args = f_match.group(2) if f_match.group(1) is not None else f_match.group(4)
            f_args = f_args.strip() if f_args else ""

            if f_name and f_name not in ["require", "import"]:
                f_id = f"{rel_path_str}::{f_name}"
                
                end_line = find_end_line_by_braces(lines, idx - 1)

                # 💡 [변경 3] () 대신 ({f_args})를 매핑하여 실제 파라미터를 출력합니다.
                symbols_info_strings.append(f"🎯 def {f_name}({f_args}) [L{idx}~L{end_line}]")
                symbols.append({
                    "symbol_id": f_id, "name": f_name, "full_name": f_name, "type": "function",
                    "path": rel_path_str, "start_line": idx, "end_line": end_line,
                    "calls": [], "used_by": []
                })
                definition_map[f_id] = f"{rel_path_str}:{idx}"

    # [C] 데이터 프로토콜 스캔
    for obj_match in object_pattern.finditer(content):
        obj_name = obj_match.group(1)
        obj_body = obj_match.group(2)
        
        fields = {}
        kv_pairs = re.findall(r'([A-Za-z0-9_]+)\s*:\s*([^,\n]+)', obj_body)
        for k, v in kv_pairs:
            v_clean = v.strip().strip("'\"")
            fields[k] = f"Any (기본값: {v_clean})"
            
        if fields:
            data_protocols[obj_name] = fields

    summary_parts = [imports_str] if imports_str else []
    summary_parts.extend(symbols_info_strings)
    symbols_summary_str = " | ".join(summary_parts)

    # 🧱 스켈레톤 문맥 정밀 구성
    skeleton_lines = [imports_str] if imports_str else []
    skeleton_lines.extend(symbols_info_strings)
    skeleton_text = "\n".join(skeleton_lines)

    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": symbols_summary_str,
        "skeleton": skeleton_text
    }

    # debug_log(f"✅ [File Scan Complete] {rel_path_str} (추출 심볼: {len(symbols)}개)")
    return symbols, file_context, definition_map, data_protocols, registry_constants
```

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/json_parser.py
#### 🧱 Code Skeleton:
```python
def extract_symbols(file_path: Path, project_root: Path):
    """
    📦 [JSON Core Parser v2.0 - Agent 2-Way Slicing Advanced]
    기존 5대 장부 리턴 구조를 100% 준수하면서,
    하위 AI 에이전트가 단번에 연관 파일(Entrypoint, 설정 파일)로 점프할 수 있도록
    calls 및 used_by 연관 고리를 정밀 추출합니다.
    """
    symbols = []
    file_context = {}
    definition_map = {}
    data_protocols = {}
    registry_constants = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return symbols, {}, {}, {}, []

    try:
        rel_path_str = file_path.relative_to(project_root).as_posix()
    except ValueError:
        rel_path_str = file_path.resolve().relative_to(project_root.resolve()).as_posix()

    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    lines = content.splitlines()

    # 1. JSON 유효성 검사
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return symbols, {}, {}, {}, []

    skeleton_lines = ["📦 [JSON STRUCTURE MAP]"]
    symbols_info_strings = []

    # 2. 파일 내부 경로/의존성 감지용 정규식 패턴 (2차 calls 추적용)
    # 예: "./src/index.js", "app.py", "config/setting.json" 등
    path_pattern = re.compile(r'[\'"]([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\'"]')
    detected_file_calls = set()

    # 소스 코드 전체에서 언급되는 상대/절대 파일 경로 징집
    for match in path_pattern.findall(content):
        clean_match = match.strip().replace("\\", "/")
        # 자기 자신 경로 제외 및 의미 있는 파일 확장자 형태 필터링
        if clean_match != rel_path_str and ("/" in clean_match or clean_match.endswith(('.js', '.ts', '.py', '.java', '.json'))):
            detected_file_calls.add(clean_match)

    # 3. 최상위 키 및 심볼 추출
    if isinstance(data, dict):
        for key, value in data.items():
            val_type = type(value).__name__
            
            # 줄 번호 탐지 (해당 key가 위치한 소스 코드 줄 계산)
            start_line = 1
            for idx, line in enumerate(lines, start=1):
                if f'"{key}"' in line or f"'{key}'" in line:
                    start_line = idx
                    break

            # 힌트 및 스켈레톤 조립
            if isinstance(value, list):
                hint = f"List (len: {len(value)})"
            elif isinstance(value, dict):
                hint = f"Dict (keys: {list(value.keys())[:3]}...)"
            else:
                hint = f"{val_type} (val: {str(value)[:30]})"

            skeleton_lines.append(f"  ├── \"{key}\": {hint}")
            symbols_info_strings.append(f"🔑 \"{key}\" [{val_type}]")

            # 🎯 키별 calls 세부 추적 (e.g. main, scripts, extends 등 진입점 연관 파일 바인딩)
            key_calls = []
            val_str = str(value)
            for file_call in detected_file_calls:
                if file_call in val_str:
                    key_calls.append(file_call)

            s_id = f"{rel_path_str}::{key}"
            symbols.append({
                "symbol_id": s_id, 
                "name": key, 
                "full_name": f"{rel_path_str}::{key}", 
                "type": "json_key",
                "file": rel_path_str,
                "path": rel_path_str, 
                "start_line": start_line, 
                "end_line": start_line,
                "calls": key_calls, 
                "used_by": []
            })
            definition_map[key] = f"{rel_path_str}:{start_line}"

    elif isinstance(data, list):
        skeleton_lines.append(f"  └── Root Array: List (len: {len(data)})")
        symbols_info_strings.append(f"📦 Root_Array [len: {len(data)}]")

    skeleton_text = "\n".join(skeleton_lines)

    # 4. 파일 한줄 요약 및 컨텍스트 보관
    summary_parts = [f"💡 📦 json_keys: {len(symbols_info_strings)}개 포착"]
    summary_parts.extend(symbols_info_strings[:5])
    if len(symbols_info_strings) > 5:
        summary_parts.append(f"...외 {len(symbols_info_strings)-5}개")
        
    symbols_summary_str = " | ".join(summary_parts)

    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": symbols_summary_str,
        "skeleton": skeleton_text
    }

    # 5. 설정 파일/스펙 문서 레지스트리 분류
    file_name_lower = file_path.name.lower()
    if "protocol" in file_name_lower or "schema" in file_name_lower:
        if isinstance(data, dict):
            data_protocols[file_path.stem] = {k: type(v).__name__ for k, v in data.items()}
    elif "package" in file_name_lower or "config" in file_name_lower or "constant" in file_name_lower:
        registry_constants.append(f"JSON_CONFIG::{file_path.stem.upper()}")

    return symbols, file_context, definition_map, data_protocols, registry_constants
```

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/py_parser.py
#### 🧱 Code Skeleton:
```python
def _extract_py_args(node):
    """ast.FunctionDef 노드에서 parameter 이름을 추출합니다."""
    args = []
    for arg in node.args.args:
        if arg.arg != 'self' and arg.arg != 'cls':  # self, cls 제외
            args.append(arg.arg)
    if node.args.vararg:
        args.append(f"*{node.args.vararg.arg}")
    if node.args.kwarg:
        args.append(f"**{node.args.kwarg.arg}")
    return ", ".join(args)

def extract_symbols(file_path: Path, project_root: Path):
    """
    🐍 [Python Core Parser v1.0]
    기존 indexer.py 내부의 순정 파이썬 AST 스캔, 스켈레톤 추출, 레지스트리/프로토콜 징집 로직을
    단 하나의 약속된 마스터 함수 구조로 완벽 격리 이사 완료했습니다 형님!
    
    리턴값: (symbols_list, file_context_dict, definition_map_dict, data_protocols_dict, registry_constants_dict)
    """
    symbols = []
    file_context = {}
    definition_map = {}
    data_protocols = {}
    registry_constants = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        # 파일 읽기 실패 시 빈 규격 레이아웃으로 안전 패스
        return symbols, {}, {}, {}, []

    rel_path_str = file_path.relative_to(project_root).as_posix()
    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    try:
        root = ast.parse(content)
    except SyntaxError:
        # 문법 에러 파일 방어선
        return symbols, {}, {}, {}, []

    # 1. 🧱 스켈레톤(뼈대) 소스 정밀 요약
    lines = content.splitlines()
    skeleton_lines = []
    for node in root.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            start_idx = node.lineno - 1
            end_idx = min(node.end_lineno, len(lines)) if getattr(node, "end_lineno", None) else start_idx + 1
            skeleton_lines.extend(lines[start_idx:end_idx])
            skeleton_lines.append("")
    skeleton_text = "\n".join(skeleton_lines)

    # 2. 🧬 내부 상호 호출 관계 자백용 1차 지도 빌드
    func_lines = {}
    for node in ast.walk(root):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_lines[node.name] = (node.lineno, node.end_lineno)
        elif isinstance(node, ast.ClassDef):
            func_lines[node.name] = (node.lineno, node.end_lineno)

    # 3. 🔑 레지스트리 & 프로토콜 징집 레이더 가동
    for node in root.body:
        if isinstance(node, ast.ClassDef):
            has_vars = False
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name) and (target.id == "vars" or "variables" in target.id.lower()):
                            has_vars = True
            
            if has_vars:
                # 데이터 프로토콜 장부 등록
                fields = {}
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name) and target.id != "vars":
                                if isinstance(item.value, ast.Constant):
                                    fields[target.id] = f"{type(item.value.value).__name__} (기본값: {item.value.value})"
                                else:
                                    fields[target.id] = "Any"
                data_protocols[node.name] = fields
            else:
                # 일반 핵심 클래스는 레지스트리 상수로 귀속
                KEYWORDS = ["entity", "platform", "camera", "sensor", "agent", "navigator", "indexer", "retriever", "handler"]
                if any(kw in node.name.lower() for kw in KEYWORDS):
                    registry_constants.append(node.name)

    # 4. 🎯 클래스/메서드/함수 트리 구조 정밀 추적 및 심볼 바느질
    symbols_info_strings = []
    
    # 탑레벨 함수/클래스 1차 등록
    for node in root.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            s_name = node.name  # 💡 1. 변수 선언 먼저!
            s_args = _extract_py_args(node)  # 💡 2. 상단 헬퍼 함수로 인자 추출
            s_id = f"{rel_path_str}::{s_name}"
            
            # 💡 3. 인자가 포함된 단 하나의 깔끔한 요약줄 추가
            symbols_info_strings.append(f"🎯 def {s_name}({s_args}) [L{node.lineno}-{node.end_lineno}]")
            
            calls = []
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                    if child.func.id in func_lines and child.func.id != s_name:
                        calls.append(child.func.id)
            
            symbols.append({
                "symbol_id": s_id, "name": s_name, "full_name": s_name, "type": "function",
                "path": rel_path_str, "start_line": node.lineno, "end_line": node.end_lineno,
                "calls": list(set(calls)), "used_by": []
            })
            definition_map[s_id] = f"{rel_path_str}:{node.lineno}"

        elif isinstance(node, ast.ClassDef):
            c_name = node.name
            c_id = f"{rel_path_str}::{c_name}"
            
            symbols_info_strings.append(f"🧬 class {c_name} [L{node.lineno}-{node.end_lineno}]")
            
            symbols.append({
                "symbol_id": c_id, "name": c_name, "full_name": c_name, "type": "class",
                "path": rel_path_str, "start_line": node.lineno, "end_line": node.end_lineno,
                "calls": [], "used_by": []
            })
            definition_map[c_id] = f"{rel_path_str}:{node.lineno}"

            # 클래스 내부 메서드 슬라이싱
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    m_name = sub.name
                    m_args = _extract_py_args(sub)  # 💡 4. 클래스 내부 메서드 인자도 추출!
                    m_id = f"{rel_path_str}::{c_name}.{m_name}"
                    
                    symbols_info_strings.append(f"    └─ def {m_name}({m_args}) [L{sub.lineno}-{sub.end_lineno}]")
                    
                    sub_calls = []
                    for child in ast.walk(sub):
                        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                            if child.func.id in func_lines and child.func.id != m_name:
                                sub_calls.append(child.func.id)
                    
                    symbols.append({
                        "symbol_id": m_id, "name": m_name, "full_name": f"{c_name}.{m_name}", "type": "method",
                        "path": rel_path_str, "start_line": sub.lineno, "end_line": sub.end_lineno,
                        "calls": list(set(sub_calls)), "used_by": []
                    })
                    definition_map[m_id] = f"{rel_path_str}:{sub.lineno}"

    # 임포트 내역 파싱
    imports = []
    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    imports_str = f"💡 📦 imp: {', '.join(sorted(list(set(imports))))}" if imports else ""

    # 최종 한줄 요약 문자열 조립
    summary_parts = [imports_str] if imports_str else []
    summary_parts.extend(symbols_info_strings)
    symbols_summary_str = " | ".join(summary_parts)

    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": symbols_summary_str,
        "skeleton": skeleton_text
    }

    return symbols, file_context, definition_map, data_protocols, registry_constants
```

--------------------------------------------------

### 📄 tools/universal_indexer/create_ai_map.py
#### 🧱 Code Skeleton:
```python
def load_jjap_context():
    """통합 .jjap_context.json 장부 로드"""
    if CONTEXT_JSON_PATH.exists():
        try:
            with open(CONTEXT_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("files", {})
        except Exception as e:
            print(f"⚠️ [.jjap_context.json] 로드 중 오류 발생: {e}")
    else:
        print("⚠️ [.jjap_context.json] 통합 장부 파일을 찾을 수 없습니다. 인덱서를 먼저 실행해 주세요.")
    return {}

def collect_target_files():
    """프로젝트 내 대상 파일 수집 (원래 수집 로직 100% 동일)"""
    scan_mode = get_scan_mode()
    if scan_mode == "ROOT":
        scan_target = PROJECT_ROOT
        print("🎯 [create_ai_map] Mode: ROOT (프로젝트 전체 스캔)")
    else:
        scan_target = PROJECT_ROOT / "extraction_target_project"
        print("🎯 [create_ai_map] Mode: EXTRACTION_TARGET_PROJECT (타깃 폴더 스캔)")

    if not scan_target.exists():
        print(f"❌ [오류] 스캔 대상 경로가 존재하지 않습니다: {scan_target}")
        return []

    target_files = []
    for root, dirs, files in os.walk(scan_target, followlinks=True):
        normalized_root = root.replace("\\", "/")

        if "src/project_root/src" in normalized_root:
            continue
        if any(kw in normalized_root for kw in EXCLUDE_KEYWORDS):
            continue

        for file in files:
            if file == "start.py" and scan_mode == "SRC":
                continue
            
            full_path = Path(root) / file
            target_files.append(full_path)

    print(f"✅ 총 {len(target_files)}개 파일 수집 완료")
    return sorted(target_files)

def load_registry():
    """Universal Registry Loader"""
    if not REGISTRY_JSON_PATH.exists():
        return set()
    try:
        with open(REGISTRY_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if isinstance(data, dict) and "registered_entities" in data:
                entities = data["registered_entities"]
                if isinstance(entities, list):
                    return set(entities)
                elif isinstance(entities, dict):
                    return set(entities.keys())

            if isinstance(data, dict):
                extracted = set()
                for k, v in data.items():
                    if isinstance(v, list):
                        for item in v: extracted.add(str(item))
                    else:
                        extracted.add(str(k))
                return extracted

            if isinstance(data, list):
                return set(str(x) for x in data)

            return set()
    except Exception as e:
        print(f"⚠️ [맵메이커 방어선] 레지스트리 로드 실패 우회: {e}")
        return set()

def load_protocols():
    """Universal Protocol Loader"""
    if not PROTOCOL_JSON_PATH.exists():
        return {}
    try:
        with open(PROTOCOL_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if isinstance(data, dict) and "protocols" in data:
                return data["protocols"]
                
            if isinstance(data, dict):
                return data
                
            return {}
    except Exception as e:
        print(f"⚠️ [맵메이커 방어선] 프로토콜 로드 실패 우회: {e}")
        return {}

def parse_protocols_and_registries():
    """심볼 장부 기반 매칭 테이블 완성 (원래 로직 100% 복원)"""
    path_to_registry = {}
    path_to_protocol = {}

    registry_data = load_registry()
    protocol_data = load_protocols()

    all_symbols = []
    if SYMBOLS_JSON_PATH.exists():
        try:
            with open(SYMBOLS_JSON_PATH, "r", encoding="utf-8") as f:
                all_symbols = json.load(f).get("symbols", [])
        except Exception as e:
            print(f"⚠️ [.jjap_symbols.json] 읽기 실패: {e}")

    for sym in all_symbols:
        if sym.get("type") != "class":
            continue
            
        cls_name = sym.get("name")
        rel_path = sym.get("path")
        
        if not cls_name or not rel_path:
            continue

        posix_rel_path = Path(rel_path).as_posix()

        if cls_name in registry_data:
            if posix_rel_path not in path_to_registry:
                path_to_registry[posix_rel_path] = set()
            path_to_registry[posix_rel_path].add(cls_name)

        if cls_name in protocol_data:
            if posix_rel_path not in path_to_protocol:
                path_to_protocol[posix_rel_path] = []
            if (cls_name, protocol_data[cls_name]) not in path_to_protocol[posix_rel_path]:
                path_to_protocol[posix_rel_path].append((cls_name, protocol_data[cls_name]))

    return path_to_registry, path_to_protocol

def load_all_symbols():
    """통합 .jjap_symbols.json 장부 로드 및 파일별/심볼ID별 인덱싱"""
    symbols_by_file = {}
    symbol_by_id = {}
    
    if SYMBOLS_JSON_PATH.exists():
        try:
            with open(SYMBOLS_JSON_PATH, "r", encoding="utf-8") as f:
                symbols_list = json.load(f).get("symbols", [])
                for sym in symbols_list:
                    rel_path = sym.get("file") or sym.get("path")
                    if rel_path:
                        posix_path = Path(rel_path).as_posix()
                        symbols_by_file.setdefault(posix_path, []).append(sym)
                    
                    sym_id = sym.get("symbol_id")
                    if sym_id:
                        symbol_by_id[sym_id] = sym
        except Exception as e:
            print(f"⚠️ [.jjap_symbols.json] 로드 오류: {e}")
            
    return symbols_by_file, symbol_by_id

def main():
    scan_mode = get_scan_mode()
    target_files = collect_target_files()
    jjap_context = load_jjap_context()
    symbols_by_file, symbol_by_id = load_all_symbols()  # 💡 심볼 장부 로드 추가
    path_to_registry, path_to_protocol = parse_protocols_and_registries()

    AI_MAP_MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(AI_MAP_MD_PATH, "w", encoding="utf-8") as f:
        printed_dirs = set()

        f.write("# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)\n\n")
        f.write("> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.\n")
        f.write("> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.\n\n")
        
        if scan_mode == "EXTRACTION_TARGET_PROJECT":
            f.write("```markdown\nextraction_target_project/\n")
        else:
            f.write("```markdown\nproject_root/\n")
        
        for file_path in target_files:
            rel_path = file_path.relative_to(PROJECT_ROOT)
            posix_rel_path = rel_path.as_posix()
            file_name = file_path.name

            if scan_mode == "EXTRACTION_TARGET_PROJECT" and posix_rel_path.startswith("extraction_target_project/"):
                display_path = posix_rel_path[26:]
            else:
                display_path = posix_rel_path

            parts = Path(display_path).parts
            for i in range(len(parts) - 1):
                current_dir_path = Path(*parts[:i + 1]).as_posix()
                if current_dir_path not in printed_dirs:
                    printed_dirs.add(current_dir_path)
                    indent = "│   " * i
                    f.write(f"{indent}├── {parts[i]}/\n")

            indent = "│   " * (len(parts) - 1)

            file_meta = jjap_context.get(posix_rel_path, {})
            symbols_info = file_meta.get("symbols_summary", "")

            if not symbols_info and posix_rel_path.startswith("extraction_target_project/extraction_target_project/"):
                shorter_path = posix_rel_path.replace("extraction_target_project/extraction_target_project/", "extraction_target_project/", 1)
                symbols_info = jjap_context.get(shorter_path, {}).get("symbols_summary", "")

            if symbols_info:
                f.write(f"{indent}├── {file_name} [📂 {display_path}] -> [{symbols_info}]\n")
            else:
                f.write(f"{indent}├── {file_name} [📂 {display_path}]\n")

            if posix_rel_path in path_to_registry:
                for reg_const in path_to_registry[posix_rel_path]:
                    f.write(f"{indent}│     ├── 🔑 [REGISTRY]: \"{reg_const}\"\n")

            if posix_rel_path in path_to_protocol:
                for proto_name, fields in path_to_protocol[posix_rel_path]:
                    f.write(f"{indent}│     ├── 📊 [PROTOCOL]: \"{proto_name}\"\n")
                    field_items = [
                        f"{k}({v.replace(' (기본값: ', ':').replace(')', '')})"
                        for k, v in fields.items()
                    ]
                    chunks = [field_items[x:x + 4] for x in range(0, len(field_items), 4)]
                    for chunk in chunks:
                        f.write(f"{indent}│     │     ├── {', '.join(chunk)}\n")

# 🎯 [알맹이 보강] 정밀 심볼 트리 (클래스/함수/인자/줄범위/CALLS/USED_BY) 생성
            file_symbols = symbols_by_file.get(posix_rel_path, [])
            for sym in file_symbols:
                sym_type = sym.get("type", "function")
                sym_name = sym.get("name", "")
                full_name = sym.get("full_name", sym_name)
                if not sym_name:
                    continue

                # 1. 인자(Arguments) 복원 (args 리스트 또는 raw 파라미터 대응)
                raw_args = sym.get("args")
                if isinstance(raw_args, list):
                    args_str = f"({', '.join(raw_args)})" if raw_args else ""
                elif isinstance(raw_args, str) and raw_args:
                    args_str = f"({raw_args})"
                else:
                    args_str = ""

                # 2. 줄범위(Start Line - End Line) 계산
                start_line = sym.get("start_line")
                end_line = sym.get("end_line")
                if start_line and end_line and start_line != end_line:
                    line_str = f"[L{start_line}-L{end_line}]"
                elif start_line:
                    line_str = f"[L{start_line}]"
                else:
                    line_str = ""

                # 3. 타입별 아이콘 및 표현 구분
                if sym_type == "class":
                    icon_str = f"🧬 class {sym_name}"
                elif sym_type == "json_key":
                    icon_str = f"🔑 key \"{sym_name}\""
                elif sym_type == "method" or "." in full_name:
                    icon_str = f"🎯 def {sym_name}{args_str if args_str else '()'}"
                else:
                    icon_str = f"🎯 def {sym_name}{args_str if args_str else '()'}"

                f.write(f"{indent}│   ├── {icon_str} {line_str}\n".rstrip() + "\n")

                # 4. 호출 관계 (CALLS)
                calls = sym.get("calls", [])
                if calls:
                    f.write(f"{indent}│   │   ├── 📞 [CALLS]: {', '.join(calls)}\n")

                # 5. 역방향 참조 관계 (USED BY)
                used_by_ids = sym.get("used_by", [])
                if used_by_ids:
                    used_by_info = []
                    for u_id in used_by_ids:
                        target = symbol_by_id.get(u_id)
                        if target:
                            u_file = target.get("file") or target.get("path", "")
                            u_name = target.get("name", "")
                            # 동일 파일 내 호출이면 함수명만, 타 파일이면 파일 경로 포함
                            if u_file == posix_rel_path:
                                used_by_info.append(f"::{u_name}")
                            else:
                                used_by_info.append(f"{u_file}::{u_name}")
                        else:
                            used_by_info.append(str(u_id))
                    f.write(f"{indent}│   │   ├── 🔗 [USED BY]: {', '.join(used_by_info)}\n")

    print("🎯 [마스터 공장] 'system_maps/AI_CODEBASE_MAP.md'가 (인자, calls, used_by 관계망 포함) 정밀 자동 갱신되었습니다!")

def generate_ai_optimized_map():
    main()
```

--------------------------------------------------

### 📄 tools/universal_indexer/indexer.py
#### 🧱 Code Skeleton:
```python
def log(message: str):
    if DEBUG_LOG:
        print(f"📡 [Indexer-Core Log] {message}")

class AdvancedIndexerV2:
    """
    [Jjap-Cursor Core Indexer V3.6 - Ultra Universal Engine]
    동적 플러그인 로딩 및 5대 장부 동기화의 모든 파이프라인에 디버깅 레이더를 도배했습니다.
    """
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = project_root
        self.parsers: Dict[str, Any] = {}
        self.symbols: List[Dict[str, Any]] = []
        self.files_context: Dict[str, Any] = {}
        self.definition_map: Dict[str, str] = {}
        self.data_protocols: Dict[str, Any] = {}
        self.registry_constants: List[str] = []
        
        # log(f"🏗️ 인덱서 코어 초기화 완료 (마스터 루트 주소: {self.project_root})")
        self._auto_load_parsers()

    def _auto_load_parsers(self):
        """core_parsers 폴더 내부의 파서들을 동적 로드하여 확장자별로 바인딩합니다."""
        parsers_dir = Path(__file__).parent.resolve() / "core_parsers" # ✅ 수정완료
        # log(f"🔌 동적 파서 폴더 탐색 시작 -> 경로: {parsers_dir}")
        
        if not parsers_dir.exists():
            # log(f"⚠️ [경고] core_parsers 폴더가 물리적으로 존재하지 않습니다: {parsers_dir}")
            return

        file_list = os.listdir(parsers_dir)
        # log(f"📂 폴더 내부 파일 목록 검색 완료 (총 {len(file_list)}개 탐지됨)")

        for file in file_list:
            if file.endswith("_parser.py"):
                ext = f".{file.split('_parser.py')[0]}"
                full_path = parsers_dir / file
                # log(f"   ⚙️ 파서 후보 발견: '{file}' -> 매핑 타깃 확장자: '{ext}'")
                
                try:
                    spec = importlib.util.spec_from_file_location(f"parser_{ext}", full_path)
                    if spec and spec.loader:
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                        if hasattr(mod, "extract_symbols"):
                            self.parsers[ext] = mod.extract_symbols
                            # log(f"   └── 🟢 [바인딩 성공] 확장자 [{ext}] 엔진 탑재 완료!")
                        else:
                            # log(f"   └── ❌ [인터페이스 불일치] '{file}' 내부에 'extract_symbols' 함수가 없습니다.")
                            pass
                except Exception as ex:
                    # log(f"   └── 💥 [런타임 컴파일 에러] 파서 플러그인 로딩 실패: {file} | 사유: {ex}")
                    pass

        # log(f"📊 파서 동적 마운트 최종 정산: 총 {len(self.parsers)}개의 다국어 컴포넌트 활성화.")

    def scan_project(self):
        scan_mode = get_scan_mode()
        scan_target = self.project_root if scan_mode == "ROOT" else self.project_root / "extraction_target_project"
        # log(f"🛡️ 고유 스캔 제외 키워드 목록: {EXCLUDE_KEYWORDS}")
        
        if not scan_target.exists():
            # log(f"❌ [치명적 오류] 지정된 스캔 타깃 경로가 디스크에 존재하지 않습니다: {scan_target}")
            return

        total_scanned_count = 0
        total_ignored_count = 0

        for root, dirs, files in os.walk(scan_target, followlinks=True):
            normalized_root = root.replace("\\", "/")
            
            # 제외 폴더 조건 검사 및 로깅
            if any(kw in normalized_root for kw in EXCLUDE_KEYWORDS):
                # log(f"🚫 [패스] 제외 필터 경로 스킵: {normalized_root}")
                continue

            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                # 동적으로 로드된 파서 대상 확장자 범위에 포함되는지 확인
                if ext in self.parsers:
                    # log(f"🔍 [타깃 포착] 파일 발견: {file_path.name} (확장자: {ext})")
                    self.index_file(file_path, ext)
                    total_scanned_count += 1
                else:
                    total_ignored_count += 1

        # 🔗 [글로벌 used_by 역방향 바인딩 후처리 엔진]
        # 🛡️ [동명 메서드 오매칭 방지] 단순 이름(run, save 등) 모호성에 따른 오기입 방지 안전 알고리즘
        from collections import defaultdict
        sym_by_name = defaultdict(list)
        for s in self.symbols:
            if "name" in s:
                sym_by_name[s["name"]].append(s)

        for s in self.symbols:
            caller_id = s.get("symbol_id")
            if not caller_id:
                continue

            for called_name in s.get("calls", []):
                short_name = called_name.split(".")[-1] if "." in called_name else called_name
                candidates = sym_by_name.get(short_name, [])

                if len(candidates) == 1:
                    # 1. 전역에서 유일한 심볼명인 경우 바인딩
                    target_sym = candidates[0]
                    if caller_id not in target_sym.setdefault("used_by", []):
                        target_sym["used_by"].append(caller_id)
                elif len(candidates) > 1:
                    # 2. 동명 심볼이 여럿 존재하는 경우: 같은 파일 내 심볼 1개 우선 탐색
                    same_file_candidates = [c for c in candidates if c.get("file") == s.get("file") or c.get("path") == s.get("path")]
                    if len(same_file_candidates) == 1:
                        target_sym = same_file_candidates[0]
                        if caller_id not in target_sym.setdefault("used_by", []):
                            target_sym["used_by"].append(caller_id)

        # 🗂️ 수집 완료 후 디스크 정밀 장부 보관소로 직행 쓰기
        self.save_index_data()

    def index_file(self, file_path: Path, ext: str):
        """개별 파일을 파서를 통해 쪼개어 마스터 장부에 바느질합니다."""
        try:
            rel_path_str = file_path.relative_to(self.project_root).as_posix()
        except ValueError:
            rel_path_str = file_path.resolve().relative_to(self.project_root.resolve()).as_posix()

        # log(f"🧵 [장부 바느질 개시] 상대 경로 키: '{rel_path_str}'")
        parser_func = self.parsers[ext]
        
        try:
            # log(f"   📡 플러그인 함수 {parser_func.__name__} 원격 연산 제어권 이양 중...")
            res = parser_func(file_path, self.project_root)
            
            if not res or len(res) < 5:
                # log(f"   ⚠️ [규격 위반] '{rel_path_str}' 파서의 반환 데이터가 5대 규격을 충족하지 못해 드롭합니다.")
                return

            f_symbols, f_context, f_def_map, f_protocols, f_registry = res

            # 데이터 적재 현황 세부 체크 로그
            # log(f"   📥 수집 결과 피드백 받음 -> 심볼: {len(f_symbols)}개, 정의 매핑: {len(f_def_map)}개, 프로토콜: {len(f_protocols)}개, 레지스트리: {len(f_registry)}개")

            # 1. 글로벌 심볼 리스트 누적
            self.symbols.extend(f_symbols)
            
            # 2. 파일 요약 정보 컨텍스트 병합
            self.files_context.update(f_context)
            
            # 3. 정의 맵 및 레지스트리 병합
            self.definition_map.update(f_def_map)
            self.data_protocols.update(f_protocols)
            
            for item in f_registry:
                if item not in self.registry_constants:
                    self.registry_constants.append(item)

            # log(f"   📈 [바느질 완료] 마스터 메모리 장부 적재 성공: '{rel_path_str}'")
        except Exception as e:
            # log(f"   💥 [인덱싱 내부 크래시] 파일 처리 중 예외 발생: {rel_path_str} | 에러 내용: {e}")
            pass

    def save_index_data(self):
        try:
            SYSTEM_MEMORY_DIR.mkdir(parents=True, exist_ok=True)

            with open(CONTEXT_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump({"files": self.files_context}, f, indent=2, ensure_ascii=False)

            with open(SYMBOLS_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump({"symbols": self.symbols}, f, indent=2, ensure_ascii=False)

            with open(DEFINITION_MAP_PATH, "w", encoding="utf-8") as f:
                json.dump(self.definition_map, f, indent=2, ensure_ascii=False)

            with open(PROTOCOL_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump({"protocols": self.data_protocols}, f, indent=2, ensure_ascii=False)

            with open(REGISTRY_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump({"registered_entities": self.registry_constants}, f, indent=2, ensure_ascii=False)

            print(f"🧬 [Jjap-Indexer Universal] 5대 장부 전체 동기화 성공! 보관된 총 파일 수: {len(self.files_context)}개")
        except Exception as write_err:
            pass
```

--------------------------------------------------

### 📄 tools/universal_indexer/jjap_lookup.py
#### 🧱 Code Skeleton:
```python
def load_json(file_path: Path):
    if not file_path.exists():
        print(f"❌ Error: {file_path} not found. Please run the indexer first.")
        sys.exit(1)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def lookup_symbol(symbol_name: str):
    """특정 함수나 클래스의 시그니처와 사용처를 검색합니다."""
    data = load_json(SYMBOLS_FILE)
    symbols = data.get("symbols", [])
    
    # 부분 일치 검색 (대소문자 무시)
    results = [s for s in symbols if symbol_name.lower() in s.get("name", "").lower()]
    
    if not results:
        print(f"⚠️ 심볼 '{symbol_name}'을(를) 찾을 수 없습니다.")
        return

    print(f"🔍 '{symbol_name}' 검색 결과 ({len(results)}건 찾음):\n")
    for s in results:
        print(f"[{s.get('type', 'symbol').upper()}] {s.get('full_name', s.get('name'))}")
        print(f"  - File: {s.get('file')} (Lines: {s.get('start_line')}-{s.get('end_line')})")
        print(f"  - Signature: {s.get('name')}{s.get('signature', '()')}")
        
        used_by = s.get("used_by", [])
        if used_by:
            print(f"  - Used By: {len(used_by)} places")
            for u in used_by[:5]: # 최대 5개까지만 출력 (토큰 절약)
                print(f"    * {u}")
            if len(used_by) > 5:
                print(f"    * ... and {len(used_by) - 5} more")
        else:
            print("  - Used By: None (Not used anywhere or it's a top-level entry)")
        print("-" * 40)

def show_skeleton(file_path: str):
    """특정 파일의 뼈대(Skeleton)를 보여줍니다."""
    data = load_json(CONTEXT_FILE)
    files = data.get("files", {})
    
    # 경로 매칭 (부분 일치)
    matched_keys = [k for k in files.keys() if file_path in k]
    
    if not matched_keys:
        print(f"⚠️ 파일 경로에 '{file_path}'이(가) 포함된 파일을 찾을 수 없습니다.")
        return
        
    for key in matched_keys:
        skeleton = files[key].get("skeleton", "No skeleton available.")
        print(f"📄 [FILE SKELETON] {key}")
        print(skeleton)
        print("=" * 40)
```

--------------------------------------------------

### 📄 tools/universal_indexer/jjap_retriever.py
#### 🧱 Code Skeleton:
```python
class JjapRetriever:
    """
    Roo Code를 위한 Context Surgeon V2.
    1. Exact Match 우선 탐색 (Disambiguation 해결)
    2. 라인 단위 Truncation (코드 파손 방지)
    3. 엄격한 스키마 계약 (Indexer V2 전제)
    """
    def __init__(self, project_root: Path):
        self.project_root = project_root
        # 🧠 [불러오기 교정] 격리 폴더(system_memory) 안으로 이사 간 인덱싱 장부를 정확하게 바라보도록 관로를 꺾어줍니다.
        self.symbols_file = self.project_root / "system_memory" / ".jjap_symbols.json"
        self.max_context_lines = 300
        self.symbols_db = self._load_symbols()

    def _load_symbols(self) -> List[Dict[str, Any]]:
        if self.symbols_file.exists():
            try:
                with open(self.symbols_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    symbols = data.get("symbols", [])
                    # ⚡ DEBUG_MODE가 False면 포맷팅 및 출력 연산 0초 커트!
                    if DEBUG_MODE:
                        print(f"📦 [Retriever 디버그] 인덱싱 장부 로드 완료! (총 {len(symbols)}개 심볼 탑재됨)")
                    return symbols
            except Exception as e:
                print(f"⚠️ [Retriever 에러] 스키마 로드 실패: {e}")
        else:
            if DEBUG_MODE:
                print(f"⚠️ [Retriever 디버그] 장부 파일이 없습니다: {self.symbols_file}")
        return []

    def retrieve_symbol(self, query: str) -> str:
        """심볼 검색 및 정밀 문맥 조립"""
        if DEBUG_MODE:
            print(f"📡 [Retriever 디버그] 수술 쿼리 수신: '{query}'")

        # [지피티 지적 1 해결] 심볼 식별 최적화 (Exact -> Partial -> Fallback)
        target = self._find_best_match(query)
        
        if not target:
            if DEBUG_MODE:
                print(f"❌ [Retriever 디버그] 매칭 실패 -> 장부에서 '{query}'를 찾지 못함")
            return f"❌ '{query}'와 일치하는 심볼을 찾을 수 없습니다. (ID 또는 Name을 확인하세요)"

        file_rel_path = target.get('path') or target.get('file', '')
        file_path = self.project_root / file_rel_path
        
        if DEBUG_MODE:
            print(f"🎯 [Retriever 디버그] 타깃 징집 성공! 심볼ID: {target.get('symbol_id', '')} ➡️ 타깃 파일: {file_rel_path}")

        if not file_path.exists():
            return f"❌ 파일을 찾을 수 없습니다: {file_rel_path}"

        with open(file_path, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()

        # [Surgery 시작]
        context = []
        symbol_id = target.get('symbol_id', query)
        context.append(f"### [RETRIEVED CONTEXT: {symbol_id}] ###")
        
        # 1. Imports (상단 50줄)
        context.append("\n# --- Imports ---")
        imports = [line.strip() for line in all_lines[:50] if line.strip().startswith(('import ', 'from '))]
        context.extend(imports)
        context.append("    ...")
        if DEBUG_MODE:
            print(f"🧹 [Retriever 디버그] 상단 공통 Import {len(imports)}줄 추출 완료")

        # 2. Parent Context (Class Header)
        if target.get('parent'):
            parent = next((s for s in self.symbols_db if s.get('name') == target['parent'] and (s.get('path') == file_rel_path or s.get('file') == file_rel_path)), None)
            if parent:
                p_range = parent.get('range') or [parent.get('start_line', 1), parent.get('end_line', 1)]
                p_start = p_range[0]
                context.append(f"\n# --- Class: {target['parent']} ---")
                context.append(all_lines[p_start-1].rstrip())
                context.append("    \"\"\" (Internal methods hidden) \"\"\"")
                if DEBUG_MODE:
                    print(f"🧱 [Retriever 디버그] 부모 클래스 뼈대 '{target['parent']}' 바느질 바인딩")

        # 3. Target Snippet (Range 준수)
        t_range = target.get('range') or [target.get('start_line', 1), target.get('end_line', len(all_lines))]
        start, end = t_range[0], t_range[1]
        context.append(f"\n# --- Target: {target.get('name', query)} (Lines {start}-{end}) ---")
        
        # 인덱스 범위 안전하게 가져오기
        snippet = all_lines[max(0, start-1) : min(len(all_lines), end)]
        context.extend([line.rstrip() for line in snippet])
        if DEBUG_MODE:
            print(f"✂️ [Retriever 디버그] 정밀 문맥 수술실(Surgeon) 작동 완료 ({start}~{end} 라인 발췌)")

        # [지피티 지적 2 해결] 라인 단위 안전 절삭
        return self._safe_truncate("\n".join(context))

    def _find_best_match(self, query: str) -> Optional[Dict]:
        """심볼 중복 문제를 해결하기 위한 매칭 로직"""
        # 1. symbol_id 완전 일치 (가장 정확)
        for s in self.symbols_db:
            if s.get('symbol_id') == query: 
                if DEBUG_MODE:
                    print(f"🔍 [Retriever 디버그] 1순위 완전 매칭성공 (Symbol ID): {query}")
                return s
        # 2. name 완전 일치
        for s in self.symbols_db:
            if s.get('name') == query: 
                if DEBUG_MODE:
                    print(f"🔍 [Retriever 디버그] 2순위 명칭 매칭성공 (Name): {query}")
                return s
        # 3. 부분 일치 (Fallback)
        for s in self.symbols_db:
            if query.lower() in s.get('name', '').lower(): 
                if DEBUG_MODE:
                    print(f"🔍 [Retriever 디버그] 3순위 느슨한 부분 매칭성공: {s.get('name')}")
                return s
        return None

    def _safe_truncate(self, text: str) -> str:
        """문자열 단위가 아닌 라인 단위로 끊어서 코드 파손 방지"""
        lines = text.splitlines()
        if len(lines) <= self.max_context_lines:
            return text
        
        if DEBUG_MODE:
            print(f"⚠️ [Retriever 디버그] 경고: 컨텍스트가 한계선({self.max_context_lines}줄)을 초과하여 꼬리 절단단행!")
        truncated = lines[:self.max_context_lines]
        truncated.append("\n... [⚠️ WARNING: Context truncated by line limit to protect token budget] ...")
        return "\n".join(truncated)

def main():
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    if not query:
        print("💡 Usage: python cline_tools/jjap_retriever.py <symbol_id_or_name>")
        return
    
    retriever = JjapRetriever(Path.cwd())
    print(retriever.retrieve_symbol(query))
```

--------------------------------------------------

### 📄 tools/universal_indexer/jjap_watcher.py
#### 🧱 Code Skeleton:
```python
def import_file_directly(module_name: str, file_path: Path):
    """파이썬 모듈 캐시를 우회하고 하드디스크의 파일을 날것 그대로 강제 로드합니다."""
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"❌ '{file_path}' 경로에서 spec을 추출할 수 없습니다.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def run_pipeline():
    """소스코드 변경 포착 시 인덱싱 공장과 지도 제작소를 연쇄 가동하는 마스터 파이프라인"""
    print("\n🔄 [파이프라인 트리거] 소스코드 변동 정밀 포착! 정렬 재인덱싱 작전 개시...")
    
    try:
        # [Step 3-1] 메모리 찌꺼기 청소 (캐시 크래시 원천 방지)
        for key in ["indexer", "update_map", "create_ai_map"]:
            if key in sys.modules:
                del sys.modules[key]

        # 🎯 1단계: 인덱서 강제 가동 (AdvancedIndexerV2)
        indexer_path = CURRENT_DIR / "indexer.py"
        indexer_module = import_file_directly("indexer", indexer_path)
        print("  ➡️ 1/3 단계: 신형 인덱서 V2 스캔 엔진 가동 중...")
        
        indexer_obj = indexer_module.AdvancedIndexerV2(PROJECT_ROOT)
        indexer_obj.scan_project()
        
        # ⚡ DEBUG_MODE가 False면 아래 추출/연산 코드 전체를 아예 실행하지 않고 0.00초만에 건너뜁니다!
        if DEBUG_MODE:
            classes = [s["name"] for s in indexer_obj.symbols if s.get("type") == "class"]
            methods = [s["name"] for s in indexer_obj.symbols if s.get("type") in ["function", "method"]]
            print(f"    🧬 [디버그] 클래스 목록 추출: {classes}")
            print(f"    🎯 [디버그] 함수/메서드 목록 추출: {methods}")
            
        # 🎯 2단계: 기존 인간용 백과사전 지도 제작 (update_map.py)
        update_map_path = CURRENT_DIR / "update_map.py"
        update_map_module = import_file_directly("update_map", update_map_path)
        print("  ➡️ 2/3 단계: 인간용 CODEBASE_MAP.md 장부 최신화 중...")
        update_map_module.update_map()        
        
        # 🎯 3단계: 형님의 특명! AI 전용 초경량 극한 요약 지도 실시간 동기화 (신설 🔥)
        create_ai_map_path = CURRENT_DIR / "create_ai_map.py"
        create_ai_map_module = import_file_directly("create_ai_map", create_ai_map_path)
        print("  ➡️ 3/3 단계: AI용 AI_CODEBASE_MAP.md 초경량 압축 시그니처 지도 생산 중...")
        create_ai_map_module.generate_ai_optimized_map()
        
        print("✅ [동기화 완료] 모든 장부와 AI 가성비 지도가 최신 상태로 바느질되었습니다!\n")
        
    except Exception as e:
        print(f"❌ [에러 발생] 파이프라인 구동 중 사고 발생: {e}")
        if DEBUG_MODE:
            import traceback
            traceback.print_exc()

class CodeChangeHandler:
    def __init__(self):
        self.last_trigger_time = 0
        self.debounce_duration = 0.5  # 디바운스 초단위 설정
        
    def dispatch(self, event):
        if event.is_directory:
            return
            
        src_path = Path(event.src_path)
        posix_path = src_path.as_posix().lower()
        suffix = src_path.suffix.lower()

        # 🛡️ [무한 루프 차단 방어선] 파이프라인 생성 파일 및 격리 폴더 무조건 예외 처리
        EXCLUDE_KEYWORDS = [
            "node_modules",
            ".venv", 
            ".git", 
            "__pycache__", 
            "cline_tools", 
            "system_memory", 
            "system_maps",
            ".idea",
            ".vscode",
            ".gemini",
            "dist",
            "build"
        ]

        # 1. 생성/장부/지도 파일 확장자 무조건 차단
        EXCLUDE_EXTENSIONS = [".md", ".json", ".log", ".tmp", ".txt", ".bak"]
        if suffix in EXCLUDE_EXTENSIONS:
            return

        # 2. 격리 폴더 및 키워드 경로 차단
        if any(kw in posix_path for kw in EXCLUDE_KEYWORDS):
            return

        # 3. 오직 소스코드(.py) 변경 시에만 디바운스 타임 확인 후 파이프라인 재실행
        if suffix == ".py":
            current_time = time.time()
            if current_time - self.last_trigger_time > self.debounce_duration:
                self.last_trigger_time = current_time
                if DEBUG_MODE:
                    print(f"🔔 [감시망 포착] 파일 변경 감지됨: {src_path.name}")
                run_pipeline()

def main():
    print("=" * 70)
    print("🚀 [Jjap-Cursor Watcher] 실시간 백그라운드 감시망 기동!")
    print(f"📂 감시 대상 진짜 루트 절대 경로: {PROJECT_ROOT}")
    print(f"⚙️  초정밀 디버깅 모드 상태: {'🔴 ON' if DEBUG_MODE else '⚪ OFF'}")
    print("💡 소스코드를 수정하고 저장(Ctrl+S)하면 AI 초경량 지도가 무한 자동 갱신됩니다.")
    print("=" * 70)
    
    # 초도 기동 시 장부가 없을 수 있으므로 파이프라인 1회 선제 타격 가동
    run_pipeline()
    
    try:
        from watchdog.observers.polling import PollingObserver as Observer
    except ImportError:
        from watchdog.observers import Observer

    event_handler = CodeChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(PROJECT_ROOT), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

--------------------------------------------------

### 📄 tools/universal_indexer/switch.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/tree_sitter_parser.py
#### 🧱 Code Skeleton:
```python
def extract_symbols(file_path: Path, project_root: Path):
    """
    🌳 [Universal Tree-sitter AST Parser v3.0 - Call & Used_by Graph Engine]
    양방향 호출 관계(calls / used_by)까지 완벽 추출하는 고도화 파서
    """
    symbols = []
    file_context = {}
    definition_map = {}
    data_protocols = {}
    registry_constants = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return symbols, {}, {}, {}, []

    try:
        rel_path_str = file_path.relative_to(project_root).as_posix()
    except ValueError:
        rel_path_str = file_path.resolve().relative_to(project_root.resolve()).as_posix()

    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    ext = file_path.suffix.lower()

    if not HAS_TREE_SITTER or ext not in LANG_MAP:
        file_context[rel_path_str] = {
            "hash": file_hash,
            "symbols_summary": f"📄 Raw File ({ext})",
            "skeleton": content[:300]
        }
        return symbols, file_context, definition_map, data_protocols, registry_constants

    lang_name = LANG_MAP[ext]
    parser = get_parser(lang_name)
    tree = parser.parse(bytes(content, "utf8"))

    symbols_summary_list = []
    KEYWORDS = ["entity", "platform", "camera", "sensor", "agent", "navigator", "indexer", "retriever", "handler", "service", "controller"]

    def traverse(node, current_symbol=None):
        """
        AST 재귀 순회: current_symbol 인자를 전달하여 
        함수 내부에서 발생하는 호출문(call_expression)을 추적합니다.
        """
        node_type = node.type
        active_symbol = current_symbol

        # 1. 클래스 선언 수집
        if node_type in ["class_declaration", "class_definition", "struct_specifier", "interface_declaration"]:
            name_node = node.child_by_field_name("name")
            if name_node:
                c_name = content[name_node.start_byte:name_node.end_byte]
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                c_id = f"{rel_path_str}::{c_name}"
                
                line_range = f"L{start_line}-L{end_line}" if start_line != end_line else f"L{start_line}"
                symbols_summary_list.append(f"🧬 class {c_name} [{line_range}]")
                
                sym_obj = {
                    "symbol_id": c_id, "name": c_name, "full_name": c_name, "type": "class",
                    "file": rel_path_str, "path": rel_path_str, "start_line": start_line, "end_line": end_line,
                    "calls": [], "used_by": []
                }
                definition_map[c_id] = f"{rel_path_str}:{start_line}"
                
                symbols.append(sym_obj)
                definition_map[c_name] = f"{rel_path_str}:{start_line}"
                active_symbol = sym_obj

                if any(kw in c_name.lower() for kw in KEYWORDS):
                    registry_constants.append(c_name)

        # 2. 함수 / 메서드 선언 수집
        elif node_type in ["function_declaration", "function_definition", "method_definition", "arrow_function"]:
            name_node = node.child_by_field_name("name")
            if not name_node and node.parent and node.parent.type == "variable_declarator":
                name_node = node.parent.child_by_field_name("name")

            if name_node:
                f_name = content[name_node.start_byte:name_node.end_byte]
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                f_id = f"{rel_path_str}::{f_name}"
                
                line_range = f"L{start_line}-L{end_line}" if start_line != end_line else f"L{start_line}"
                symbols_summary_list.append(f"🎯 def {f_name}() [{line_range}]")

                sym_obj = {
                    "symbol_id": f_id, "name": f_name, "full_name": f_name, "type": "function",
                    "file": rel_path_str, "path": rel_path_str, "start_line": start_line, "end_line": end_line,
                    "calls": [], "used_by": []
                }
                symbols.append(sym_obj)
                definition_map[f_name] = f"{rel_path_str}:{start_line}"
                active_symbol = sym_obj

        # 3. [핵심 추가] 함수 호출문(call) 추적
        elif node_type in ["call_expression", "function_call"]:
            func_node = node.child_by_field_name("function") or (node.children[0] if node.children else None)
            if func_node:
                called_name = content[func_node.start_byte:func_node.end_byte]
                # 예: console.log -> log / obj.method -> method
                if "." in called_name:
                    called_name = called_name.split(".")[-1]
                
                # 내 안에 다른 함수를 호출하는 코드가 있다면 calls에 등록
                if active_symbol and called_name not in active_symbol["calls"]:
                    active_symbol["calls"].append(called_name)

        # 자식 노드 재귀 탐색 (현재 활성화된 심볼 전달)
        for child in node.children:
            traverse(child, active_symbol)

    traverse(tree.root_node)

    # 4. [핵심 추가] 파일 내부 후처리: calls 관계를 바탕으로 used_by 역방향 주소 바인딩
    # 🛡️ [동명 메서드 오매칭 방지] 단순 이름(run, save 등) 모호성에 따른 오기입 방지 안전 알고리즘
    from collections import defaultdict
    sym_by_name = defaultdict(list)
    for s in symbols:
        if "name" in s:
            sym_by_name[s["name"]].append(s)

    for s in symbols:
        caller_id = s.get("symbol_id")
        if not caller_id:
            continue

        for called_fn in s.get("calls", []):
            short_name = called_fn.split(".")[-1] if "." in called_fn else called_fn
            candidates = sym_by_name.get(short_name, [])

            if len(candidates) == 1:
                # 1. 파일 내 유일 심볼인 경우 안전 바인딩
                target_sym = candidates[0]
                if caller_id not in target_sym.setdefault("used_by", []):
                    target_sym["used_by"].append(caller_id)
            elif len(candidates) > 1:
                # 2. 동명 메서드가 2개 이상인 경우 동일 파일 후보 1개 우선 탐색
                same_file_candidates = [c for c in candidates if c.get("file") == s.get("file")]
                if len(same_file_candidates) == 1:
                    target_sym = same_file_candidates[0]
                    if caller_id not in target_sym.setdefault("used_by", []):
                        target_sym["used_by"].append(caller_id)

    # Context 조립
    summary_str = " | ".join(symbols_summary_list) if symbols_summary_list else f"📄 File ({ext})"
    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": summary_str,
        "skeleton": content[:400]
    }

    return symbols, file_context, definition_map, data_protocols, list(set(registry_constants))
```

--------------------------------------------------

### 📄 tools/universal_indexer/update_map.py
#### 🧱 Code Skeleton:
```python
def update_map():
    # 🔄 [안전 보장] 실행 환경에 구애받지 않도록 현재 스크립트 위치 기준 진짜 프로젝트 마스터 루트를 추적합니다.
    SCRIPT_DIR = Path(__file__).parent.resolve()
    if SCRIPT_DIR.name == "universal_indexer" and SCRIPT_DIR.parent.name == "tools":
        PROJECT_ROOT = SCRIPT_DIR.parent.parent
    else:
        PROJECT_ROOT = SCRIPT_DIR

    # 🧠 마스터 루트 기준으로 경로를 확실하게 조준하여 불러오기 및 출력을 고정합니다.
    context_file = PROJECT_ROOT / "system_memory" / ".jjap_context.json"
    symbols_file = PROJECT_ROOT / "system_memory" / ".jjap_symbols.json"
    output_file = PROJECT_ROOT / "system_maps" / "CODEBASE_MAP.md"
    
    if not context_file.exists() or not symbols_file.exists():
        print("❌ Error: 인덱서 데이터 파일(.jjap_context 또는 .jjap_symbols)이 없습니다.")
        print("💡 해결책: 인덱서(indexer.py)를 먼저 실행한 뒤 이 스크립트를 돌리세요.")
        return

    # 1. 최신 데이터 로드
    with open(context_file, "r", encoding="utf-8") as f:
        context_data = json.load(f).get("files", {})
        
    with open(symbols_file, "r", encoding="utf-8") as f:
        symbols_list = json.load(f).get("symbols", [])

    # 🚨 [검열 시스템 동기화] 인덱서와 싱크로율 100% 맞추기
    # 혹시라도 장부에 흔적이 남아있거나, 루트의 실행 파일들이 맵에 찍히는 걸 원천 차단합니다.
    # 🚨 [검열 시스템 동기화] 인덱서 및 기타 도구들과 검열 필터 규격 100% 동기화
    EXCLUDE_KEYWORDS = [
        "node_modules",
        ".venv", 
        ".git", 
        "__pycache__", 
        "cline_tools", 
        "system_memory", 
        "system_maps"
    ]

    # 2. 에이전트 분석을 돕기 위해 파일별 심볼 및 관계 매핑 구조 생성
    symbols_by_file = {}
    for s in symbols_list:
        file_path = s.get("file", "")
        
        # 🚨 검열 컷 1: 심볼 리스트 중에 제외 폴더나 start.py가 있으면 장부에서 누락 처리
        if any(p in file_path for p in EXCLUDE_KEYWORDS) or "start.py" in file_path:
            continue
            
        if file_path not in symbols_by_file:
            symbols_by_file[file_path] = []
        symbols_by_file[file_path].append(s)

    # 3. CODEBASE_MAP.md 최종 렌더링
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 🏗️ 짭커서 프로젝트 CODEBASE MAP\n\n")
        
        # 🚨 검열 컷 2: 순수 유효 파일만 발라내기 (start.py 및 도구 폴더 완전히 소멸시킴)
        valid_files = {}
        for path, info in context_data.items():
            if any(p in path for p in EXCLUDE_KEYWORDS) or "start.py" in path:
                continue
            valid_files[path] = info

        f.write(f"현재 인덱싱된 총 파일 수: **{len(valid_files)}개**\n\n")
        
        # 📂 모듈 인덱스 구역
        f.write("## 🗂️ [Module Index]\n")
        for path in sorted(valid_files.keys()):
            f.write(f"- `{path}`\n")
        
        # 💀 뼈대 및 의존성 관계 상세 구역
        f.write("\n## 💀 [Skeleton & Dependency 명세서]\n")
        for path, info in sorted(valid_files.items()):
            f.write(f"### 📄 {path}\n")
            
            # 해당 파일에 속한 상세 심볼(클래스/함수)의 호출 관계 먼저 요약
            file_symbols = symbols_by_file.get(path, [])
            if file_symbols:
                f.write("#### 🔍 내부 심볼 및 의존성 관계:\n")
                for s in file_symbols:
                   # 수정 코드: s['full_name']을 s['name']으로 변경
                    f.write(f"- **[{s['type'].upper()}]** `{s['name']}` (Line: {s['start_line']}~{s['end_line']})\n")
                    if s.get("calls"):
                        f.write(f"  - 🔗 *Calls (호출하는 것)*: `{', '.join(s['calls'])}`\n")
                    if s.get("used_by"):
                        f.write(f"  - 🎯 *Used By (나를 부르는 곳)*: `{', '.join(s['used_by'])}`\n")
                f.write("\n")

            # 실제 코드 뼈대(Skeleton) 출력
            skeleton_text = info.get("skeleton", "").strip()
            if skeleton_text:
                f.write("#### 🧱 Code Skeleton:\n")
                f.write("```python\n")
                f.write(f"{skeleton_text}\n")
                f.write("```\n\n")
            else:
                f.write("*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*\n\n")
                
            f.write("-" * 50 + "\n\n")

    print(f"✅ [SUCCESS] V2 인덱스 정밀 데이터를 결합하여 {output_file.name} 업데이트 완료! (스텔스 필터 적용)")
```

--------------------------------------------------

