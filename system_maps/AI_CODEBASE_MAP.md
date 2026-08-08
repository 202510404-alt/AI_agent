# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)

> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.
> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.

```markdown
project_root/
├── .env [📂 .env] -> [General File (6 lines)]
├── .gitignore [📂 .gitignore] -> [General File (23 lines)]
├── .idea/
│   ├── .gitignore [📂 .idea/.gitignore] -> [General File (10 lines)]
│   ├── AI_agent.iml [📂 .idea/AI_agent.iml] -> [General File (9 lines)]
│   ├── gradle.xml [📂 .idea/gradle.xml] -> [General File (17 lines)]
│   ├── misc.xml [📂 .idea/misc.xml] -> [General File (7 lines)]
│   ├── modules.xml [📂 .idea/modules.xml] -> [General File (8 lines)]
│   ├── vcs.xml [📂 .idea/vcs.xml] -> [General File (6 lines)]
│   ├── workspace.xml [📂 .idea/workspace.xml] -> [General File (185 lines)]
├── .vscode/
│   ├── settings.json [📂 .vscode/settings.json] -> [💡 📦 json_keys: 19개 포착 | 🔑 "terminal.integrated.sendKeybindingsToShell" [bool] | 🔑 "accessibility.verbosity.terminal" [bool] | 🔑 "git.autofetch" [bool] | 🔑 "explorer.confirmDelete" [bool] | 🔑 "git.openRepositoryInParentFolders" [str] | ...외 14개]
│   │   ├── 🔑 key "terminal.integrated.sendKeybindingsToShell" [L2]
│   │   ├── 🔑 key "accessibility.verbosity.terminal" [L3]
│   │   ├── 🔑 key "git.autofetch" [L4]
│   │   ├── 🔑 key "explorer.confirmDelete" [L5]
│   │   ├── 🔑 key "git.openRepositoryInParentFolders" [L6]
│   │   ├── 🔑 key "terminal.integrated.enableMultiLinePasteWarning" [L7]
│   │   ├── 🔑 key "workbench.editor.empty.hint" [L8]
│   │   ├── 🔑 key "maven.terminal.useJavaHome" [L9]
│   │   ├── 🔑 key "git.confirmSync" [L10]
│   │   ├── 🔑 key "explorer.confirmDragAndDrop" [L11]
│   │   ├── 🔑 key "java.configuration.runtimes" [L12]
│   │   ├── 🔑 key "java.jdt.ls.java.home" [L19]
│   │   ├── 🔑 key "roo-cline.debug" [L20]
│   │   ├── 🔑 key "roo-cline.allowedCommands" [L21]
│   │   ├── 🔑 key "roo-cline.deniedCommands" [L22]
│   │   ├── 🔑 key "files.exclude" [L23]
│   │   ├── 🔑 key "python.createEnvironment.trigger" [L26]
│   │   ├── 🔑 key "java.configuration.updateBuildConfiguration" [L27]
│   │   ├── 🔑 key "python-envs.defaultEnvManager" [L28]
├── a [📂 a] -> [General File (643 lines)]
├── agent_core/
│   ├── __init__.py [📂 agent_core/__init__.py]
│   ├── execution/
│   │   ├── __init__.py [📂 agent_core/execution/__init__.py]
│   │   ├── step_worker.py [📂 agent_core/execution/step_worker.py] -> [💡 📦 imp: agent_core.plan.schemas, json, os, pathlib, re, sys, tools.multi_agent_system.agent_map_extractor, tools.multi_agent_system.agent_session, tools.multi_agent_system.project_scale_detector, tools.multi_agent_system.terminal_runner, typing | 🧬 class ExecutionResult [L20-34] |     └─ def __init__(success, message, logs, patch_applied) [L22-26] |     └─ def to_dict() [L28-34] | 🧬 class StepExecutionWorker [L37-413] |     └─ def __init__(project_root) [L43-46] |     └─ def build_log_regex_pattern(template_msg) [L52-58] |     └─ def clean_json_response(raw_response) [L61-67] |     └─ def load_mission(mission_input) [L69-86] |     └─ def _safe_execute_step(prompt, system_instruction, response_mime_type, max_attempts) [L88-101] |     └─ def execute(mission_input) [L106-413]]
│   │   │   ├── 🧬 class ExecutionResult [L20-L34]
│   │   │   ├── 🎯 def __init__() [L22-L26]
│   │   │   ├── 🎯 def to_dict() [L28-L34]
│   │   │   ├── 🧬 class StepExecutionWorker [L37-L413]
│   │   │   ├── 🎯 def __init__() [L43-L46]
│   │   │   ├── 🎯 def build_log_regex_pattern() [L52-L58]
│   │   │   ├── 🎯 def clean_json_response() [L61-L67]
│   │   │   ├── 🎯 def load_mission() [L69-L86]
│   │   │   ├── 🎯 def _safe_execute_step() [L88-L101]
│   │   │   ├── 🎯 def execute() [L106-L413]
│   │   │   │   ├── 📞 [CALLS]: ExecutionResult
│   ├── llm/
│   │   ├── gemini_client.py [📂 agent_core/llm/gemini_client.py] -> [💡 📦 imp: agent_core.plan.schemas, google, google.genai, json, os, pathlib, pydantic, re, time, typing | 🎯 def log_debug(message_func) [L24-33] | 🎯 def load_env_file(env_path) [L36-71] | 🎯 def resolve_best_gemini_model(client, blocked_models) [L88-97] | 🧬 class PlanTask [L99-101] | 🧬 class PlanResponse [L103-105] | 🧬 class DynamicKeyModelManager [L107-168] |     └─ def __init__(root_dir) [L114-122] |     └─ def get_available_pair() [L124-153] |     └─ def report_error(key_name, model_name, error_str) [L155-168] | 🧬 class GeminiPlannerClient [L171-215] |     └─ def __init__(api_key, root_dir) [L172-175] |     └─ def generate_plan(prompt, model_name, max_retries) [L177-215]]
│   │   │   ├── 🎯 def log_debug() [L24-L33]
│   │   │   ├── 🎯 def load_env_file() [L36-L71]
│   │   │   │   ├── 📞 [CALLS]: log_debug
│   │   │   │   ├── 🔗 [USED BY]: ::__init__, ::get_available_pair
│   │   │   ├── 🎯 def resolve_best_gemini_model() [L88-L97]
│   │   │   ├── 🧬 class PlanTask [L99-L101]
│   │   │   ├── 🧬 class PlanResponse [L103-L105]
│   │   │   ├── 🧬 class DynamicKeyModelManager [L107-L168]
│   │   │   │   ├── 🔗 [USED BY]: ::__init__
│   │   │   ├── 🎯 def __init__() [L114-L122]
│   │   │   │   ├── 📞 [CALLS]: load_env_file
│   │   │   ├── 🎯 def get_available_pair() [L124-L153]
│   │   │   │   ├── 📞 [CALLS]: load_env_file
│   │   │   ├── 🎯 def report_error() [L155-L168]
│   │   │   ├── 🧬 class GeminiPlannerClient [L171-L215]
│   │   │   ├── 🎯 def __init__() [L172-L175]
│   │   │   │   ├── 📞 [CALLS]: DynamicKeyModelManager
│   │   │   ├── 🎯 def generate_plan() [L177-L215]
│   ├── memory/
│   │   ├── __init__.py [📂 agent_core/memory/__init__.py]
│   ├── plan/
│   │   ├── __init__.py [📂 agent_core/plan/__init__.py]
│   │   ├── planner.py [📂 agent_core/plan/planner.py]
│   │   ├── prompt_builder.py [📂 agent_core/plan/prompt_builder.py] -> [💡 📦 imp: agent_core.plan.schemas, pathlib, typing | 🎯 def log_debug(message_func) [L11-21] | 🧬 class PromptBuilder [L24-89] |     └─ def __init__(root_dir) [L25-33] |     └─ def _load_codebase_map() [L35-54] |     └─ def build_plan_prompt(user_goal, extra_context) [L56-89]]
│   │   │   ├── 🎯 def log_debug() [L11-L21]
│   │   │   ├── 🧬 class PromptBuilder [L24-L89]
│   │   │   ├── 🎯 def __init__() [L25-L33]
│   │   │   │   ├── 📞 [CALLS]: log_debug
│   │   │   ├── 🎯 def _load_codebase_map() [L35-L54]
│   │   │   │   ├── 📞 [CALLS]: log_debug
│   │   │   ├── 🎯 def build_plan_prompt() [L56-L89]
│   │   │   │   ├── 📞 [CALLS]: log_debug
│   │   ├── schemas.py [📂 agent_core/plan/schemas.py] -> [💡 📦 imp: dataclasses, enum, os, pathlib, typing | 🎯 def log_debug(message_func) [L20-34] | 🧬 class TaskStatus [L37-41] | 🧬 class SymbolRef [L45-50] | 🧬 class DebugLogSpec [L54-57] | 🧬 class Task [L61-70] | 🧬 class ExecutionResult [L74-79] | 🎯 def to_symbol_ref(raw_dict, default_file) [L82-104]]
│   │   │   ├── 🎯 def log_debug() [L20-L34]
│   │   │   ├── 🧬 class TaskStatus [L37-L41]
│   │   │   ├── 🧬 class SymbolRef [L45-L50]
│   │   │   │   ├── 🔗 [USED BY]: ::to_symbol_ref
│   │   │   ├── 🧬 class DebugLogSpec [L54-L57]
│   │   │   ├── 🧬 class Task [L61-L70]
│   │   │   ├── 🧬 class ExecutionResult [L74-L79]
│   │   │   ├── 🎯 def to_symbol_ref() [L82-L104]
│   │   │   │   ├── 📞 [CALLS]: log_debug, SymbolRef
│   │   ├── test_ai_chat.py [📂 agent_core/plan/test_ai_chat.py] -> [💡 📦 imp: agent_core.llm.gemini_client, agent_core.plan.prompt_builder, google, google.genai, json, os, pathlib, sys, tools.multi_agent_system.agent_code_extractor | 🎯 def extract_code_slice(file_and_line) [L32-43] | 🎯 def run_interactive_chat() [L49-104]]
│   │   │   ├── 🎯 def extract_code_slice() [L32-L43]
│   │   │   ├── 🎯 def run_interactive_chat() [L49-L104]
│   ├── tasks/
│   │   ├── task_01/
│   │   │   ├── checklist_01/
│   │   │   │   ├── mission_01.json [📂 agent_core/tasks/task_01/checklist_01/mission_01.json] -> [💡 📦 json_keys: 8개 포착 | 🔑 "task_id" [str] | 🔑 "target_file" [str] | 🔑 "entrypoint" [str] | 🔑 "test_type" [str] | 🔑 "use_browser_test" [bool] | ...외 3개]
│   │   │   │   │   ├── 🔑 key "task_id" [L2]
│   │   │   │   │   ├── 🔑 key "target_file" [L3]
│   │   │   │   │   │   ├── 📞 [CALLS]: extraction_target_project/client/src/Canvas.js, Canvas.js
│   │   │   │   │   ├── 🔑 key "entrypoint" [L4]
│   │   │   │   │   ├── 🔑 key "test_type" [L6]
│   │   │   │   │   ├── 🔑 key "use_browser_test" [L7]
│   │   │   │   │   ├── 🔑 key "implementation_blueprint" [L9]
│   │   │   │   │   │   ├── 📞 [CALLS]: Canvas.js
│   │   │   │   │   ├── 🔑 key "browser_test_spec" [L26]
│   │   │   │   │   ├── 🔑 key "expected_terminal_outputs" [L38]
│   │   │   │   ├── mission_012.json [📂 agent_core/tasks/task_01/checklist_01/mission_012.json] -> [💡 📦 json_keys: 7개 포착 | 🔑 "task_id" [str] | 🔑 "target_file" [str] | 🔑 "entrypoint" [str] | 🔑 "test_type" [str] | 🔑 "use_browser_test" [bool] | ...외 2개]
│   │   │   │   │   ├── 🔑 key "task_id" [L2]
│   │   │   │   │   ├── 🔑 key "target_file" [L3]
│   │   │   │   │   │   ├── 📞 [CALLS]: extraction_target_project/chess_game.py, chess_game.py
│   │   │   │   │   ├── 🔑 key "entrypoint" [L4]
│   │   │   │   │   │   ├── 📞 [CALLS]: extraction_target_project/chess_game.py, chess_game.py
│   │   │   │   │   ├── 🔑 key "test_type" [L6]
│   │   │   │   │   ├── 🔑 key "use_browser_test" [L7]
│   │   │   │   │   ├── 🔑 key "implementation_blueprint" [L9]
│   │   │   │   │   │   ├── 📞 [CALLS]: extraction_target_project/chess_game.py, chess_game.py
│   │   │   │   │   ├── 🔑 key "expected_terminal_outputs" [L26]
│   │   │   │   ├── mission_03.json [📂 agent_core/tasks/task_01/checklist_01/mission_03.json]
│   ├── validation/
│   │   ├── __init__.py [📂 agent_core/validation/__init__.py]
├── agent_debug.log [📂 agent_debug.log] -> [General File (3 lines)]
├── agent_plan.md [📂 agent_plan.md] -> [General File (1101 lines)]
├── extraction_target_project/
│   ├── .gitignore [📂 extraction_target_project/.gitignore] -> [General File (4 lines)]
│   ├── AI_agent.code-workspace [📂 extraction_target_project/AI_agent.code-workspace] -> [General File (26 lines)]
│   ├── client/
│   │   ├── .gitignore [📂 extraction_target_project/client/.gitignore] -> [General File (21 lines)]
│   │   ├── package-lock.json [📂 extraction_target_project/client/package-lock.json] -> [💡 📦 json_keys: 5개 포착 | 🔑 "name" [str] | 🔑 "version" [str] | 🔑 "lockfileVersion" [int] | 🔑 "requires" [bool] | 🔑 "packages" [dict]]
│   │   │   ├── 🔑 key "name" [L2]
│   │   │   │   ├── 🔗 [USED BY]: ::packages
│   │   │   ├── 🔑 key "version" [L3]
│   │   │   ├── 🔑 key "lockfileVersion" [L4]
│   │   │   ├── 🔑 key "requires" [L5]
│   │   │   ├── 🔑 key "packages" [L6]
│   │   │   │   ├── 📞 [CALLS]: node_modules/string.prototype.trimend, bin/react-scripts.js, bin/jest.js, bin/js-yaml.js, node_modules/lodash.memoize, node_modules/socket.io, node_modules/arraybuffer.prototype.slice, node_modules/iterator.prototype, bin/webpack-dev-server.js, node_modules/object.assign, node_modules/object.values, bin/cli.js, node_modules/decimal.js, bin/esvalidate.js, node_modules/ipaddr.js, node_modules/object.entries, fraction.js, node_modules/proxy-addr/node_modules/ipaddr.js, node_modules/lodash.merge, bin/webpack.js, bin/jiti.js, bin/semver.js, lib/cli.js, node_modules/util.promisify, node_modules/fs.realpath, node_modules/array.prototype.flat, big.js, node_modules/css.escape, bin/cmd.js, node_modules/array.prototype.reduce, node_modules/sanitize.css, node_modules/lodash.uniq, node_modules/array.prototype.tosorted, node_modules/big.js, node_modules/array.prototype.toreversed, node_modules/array.prototype.flatmap, node_modules/function.prototype.name, bin/esparse.js, node_modules/regexp.prototype.flags, hpack.js, node_modules/string.prototype.trim, bin/babel-parser.js, dist/cli.cjs, cli.js, node_modules/reflect.getprototypeof, dist/esm/bin.mjs, node_modules/lodash.debounce, node_modules/object.hasown, node_modules/engine.io, node_modules/object.fromentries, bin/nopt.js, bin/eslint.js, node_modules/string.prototype.trimstart, node_modules/array.prototype.findlast, node_modules/array.prototype.findlastindex, node_modules/hpack.js, node_modules/lodash.sortby, bin/nanoid.cjs, ipaddr.js, bin.js, bin/escodegen.js, decimal.js, node_modules/object.groupby, node_modules/object.getownpropertydescriptors, node_modules/resolve.exports, node_modules/string.prototype.matchall, bin/esgenerate.js, fixtures/cli.js, bin/bin.js, node_modules/fraction.js
│   │   ├── package.json [📂 extraction_target_project/client/package.json] -> [💡 📦 json_keys: 7개 포착 | 🔑 "name" [str] | 🔑 "version" [str] | 🔑 "private" [bool] | 🔑 "dependencies" [dict] | 🔑 "scripts" [dict] | ...외 2개]
│   │   │   ├── 🔑 key "name" [L2]
│   │   │   ├── 🔑 key "version" [L3]
│   │   │   ├── 🔑 key "private" [L4]
│   │   │   ├── 🔑 key "dependencies" [L5]
│   │   │   ├── 🔑 key "scripts" [L21]
│   │   │   ├── 🔑 key "eslintConfig" [L27]
│   │   │   ├── 🔑 key "browserslist" [L33]
│   │   ├── public/
│   │   │   ├── favicon.ico [📂 extraction_target_project/client/public/favicon.ico] -> [General File (91 lines)]
│   │   │   ├── favicon.svg [📂 extraction_target_project/client/public/favicon.svg] -> [General File (19 lines)]
│   │   │   ├── index.html [📂 extraction_target_project/client/public/index.html] -> [General File (21 lines)]
│   │   │   ├── logo.svg [📂 extraction_target_project/client/public/logo.svg] -> [General File (19 lines)]
│   │   │   ├── logo192.png [📂 extraction_target_project/client/public/logo192.png] -> [General File (243 lines)]
│   │   │   ├── logo512.png [📂 extraction_target_project/client/public/logo512.png] -> [General File (1639 lines)]
│   │   │   ├── manifest.json [📂 extraction_target_project/client/public/manifest.json] -> [💡 📦 json_keys: 7개 포착 | 🔑 "short_name" [str] | 🔑 "name" [str] | 🔑 "icons" [list] | 🔑 "start_url" [str] | 🔑 "display" [str] | ...외 2개]
│   │   │   │   ├── 🔑 key "short_name" [L2]
│   │   │   │   ├── 🔑 key "name" [L3]
│   │   │   │   ├── 🔑 key "icons" [L4]
│   │   │   │   ├── 🔑 key "start_url" [L27]
│   │   │   │   ├── 🔑 key "display" [L28]
│   │   │   │   ├── 🔑 key "theme_color" [L29]
│   │   │   │   ├── 🔑 key "background_color" [L30]
│   │   ├── src/
│   │   │   ├── App.css [📂 extraction_target_project/client/src/App.css] -> [General File (38 lines)]
│   │   │   ├── App.js [📂 extraction_target_project/client/src/App.js] -> [💡 📦 imp: ./Canvas, ./Home, react, react-hot-toast, react-router-dom | 🎯 def App() [L11~L20]]
│   │   │   │   ├── 🎯 def App() [L11-L20]
│   │   │   ├── App.test.js [📂 extraction_target_project/client/src/App.test.js] -> [💡 📦 imp: ./App, @testing-library/react]
│   │   │   ├── Button.js [📂 extraction_target_project/client/src/Button.js] -> [💡 📦 imp: react | 🎯 def Button({ value, name, buttonFunction }) [L4~L24]]
│   │   │   │   ├── 🎯 def Button() [L4-L24]
│   │   │   ├── Canvas.js [📂 extraction_target_project/client/src/Canvas.js] -> [💡 📦 imp: ./Button, ./UploadFile, ./hooks/useWebRTC, ./socket, react, react-hot-toast, react-icons/ai, react-icons/fa6, react-router-dom | 🎯 def RemoteAudio({ stream }) [L24~L54] | 🎯 def playAudio() [L32~L47] | 🎯 def handleUserInteraction() [L38~L43] | 🎯 def Canvas(props) [L56~L486] | 🎯 def changeColour(e) [L83~L89] | 🎯 def lineWidth(event) [L91~L97] | 🎯 def handleImageUploadSuccess(imageUrl) [L99~L107] | 🎯 def init() [L110~L158] | 🎯 def handleError(err) [L121~L125] | 🎯 def handleDraw(e) [L190~L206] | 🎯 def handleMoveDraw(e) [L208~L227] | 🎯 def handleNotDraw() [L229~L242] | 🎯 def undo() [L244~L257] | 🎯 def redrawCanvas(context, history = linesHistory) [L259~L281] | 🎯 def handleCanvasChange() [L287~L292] | 🎯 def clearCanvas() [L301~L308] | 🎯 def copyBoardId() [L310~L313] | 🎯 def leaveBoard() [L315~L317]]
│   │   │   │   ├── 🎯 def RemoteAudio() [L24-L54]
│   │   │   │   ├── 🎯 def playAudio() [L32-L47]
│   │   │   │   ├── 🎯 def handleUserInteraction() [L38-L43]
│   │   │   │   ├── 🎯 def Canvas() [L56-L486]
│   │   │   │   ├── 🎯 def changeColour() [L83-L89]
│   │   │   │   ├── 🎯 def lineWidth() [L91-L97]
│   │   │   │   ├── 🎯 def handleImageUploadSuccess() [L99-L107]
│   │   │   │   ├── 🎯 def init() [L110-L158]
│   │   │   │   ├── 🎯 def handleError() [L121-L125]
│   │   │   │   ├── 🎯 def handleDraw() [L190-L206]
│   │   │   │   ├── 🎯 def handleMoveDraw() [L208-L227]
│   │   │   │   ├── 🎯 def handleNotDraw() [L229-L242]
│   │   │   │   ├── 🎯 def undo() [L244-L257]
│   │   │   │   ├── 🎯 def redrawCanvas() [L259-L281]
│   │   │   │   ├── 🎯 def handleCanvasChange() [L287-L292]
│   │   │   │   ├── 🎯 def clearCanvas() [L301-L308]
│   │   │   │   ├── 🎯 def copyBoardId() [L310-L313]
│   │   │   │   ├── 🎯 def leaveBoard() [L315-L317]
│   │   │   ├── Home.js [📂 extraction_target_project/client/src/Home.js] -> [💡 📦 imp: react, react-hot-toast, react-router-dom, uuid | 🎯 def Home() [L8~L63] | 🎯 def writeId(event) [L14~L18] | 🎯 def writeUserName(event) [L20~L22] | 🎯 def generateUniqueId(event) [L24~L29] | 🎯 def joinBoard() [L31~L39]]
│   │   │   │   ├── 🎯 def Home() [L8-L63]
│   │   │   │   ├── 🎯 def writeId() [L14-L18]
│   │   │   │   ├── 🎯 def writeUserName() [L20-L22]
│   │   │   │   ├── 🎯 def generateUniqueId() [L24-L29]
│   │   │   │   ├── 🎯 def joinBoard() [L31-L39]
│   │   │   ├── hooks/
│   │   │   │   ├── useWebRTC.js [📂 extraction_target_project/client/src/hooks/useWebRTC.js] -> [💡 📦 imp: react, react-hot-toast | 🎯 def useWebRTC(socketRef, boardId, userName) [L32~L358]]
│   │   │   │   │   ├── 🎯 def useWebRTC() [L32-L358]
│   │   │   ├── index.css [📂 extraction_target_project/client/src/index.css] -> [General File (42 lines)]
│   │   │   ├── index.js [📂 extraction_target_project/client/src/index.js] -> [💡 📦 imp: ./App, ./reportWebVitals, react, react-dom/client]
│   │   │   ├── Input.js [📂 extraction_target_project/client/src/Input.js] -> [💡 📦 imp: react | 🎯 def Input(props) [L3~L9]]
│   │   │   │   ├── 🎯 def Input() [L3-L9]
│   │   │   ├── reportWebVitals.js [📂 extraction_target_project/client/src/reportWebVitals.js]
│   │   │   ├── setupTests.js [📂 extraction_target_project/client/src/setupTests.js]
│   │   │   ├── socket.js [📂 extraction_target_project/client/src/socket.js] -> [💡 📦 imp: socket.io-client | 🎯 def initSocket() [L5~L35]]
│   │   │   │   ├── 🎯 def initSocket() [L5-L35]
│   │   │   ├── style.css [📂 extraction_target_project/client/src/style.css] -> [General File (202 lines)]
│   │   │   ├── styleCanvas.css [📂 extraction_target_project/client/src/styleCanvas.css] -> [General File (389 lines)]
│   │   │   ├── UploadFile.js [📂 extraction_target_project/client/src/UploadFile.js] -> [💡 📦 imp: react, react-icons/fa6 | 🎯 def UploadFile(props) [L5~L31] | 🎯 def upload(event) [L8~L15]]
│   │   │   │   ├── 🎯 def UploadFile() [L5-L31]
│   │   │   │   ├── 🎯 def upload() [L8-L15]
│   ├── extraction_target_project.code-workspace [📂 extraction_target_project/extraction_target_project.code-workspace] -> [General File (14 lines)]
│   ├── index.js [📂 extraction_target_project/index.js] -> [💡 📦 imp: express, http, os, path, socket.io, url | 🎯 def getAllConnectedClients(boardId) [L35~L41] | 🎯 def getLocalExternalIP() [L209~L219]]
│   │   ├── 🎯 def getAllConnectedClients() [L35-L41]
│   │   ├── 🎯 def getLocalExternalIP() [L209-L219]
│   ├── package-lock.json [📂 extraction_target_project/package-lock.json] -> [💡 📦 json_keys: 5개 포착 | 🔑 "name" [str] | 🔑 "version" [str] | 🔑 "lockfileVersion" [int] | 🔑 "requires" [bool] | 🔑 "packages" [dict]]
│   │   ├── 🔑 key "name" [L2]
│   │   ├── 🔑 key "version" [L3]
│   │   ├── 🔑 key "lockfileVersion" [L4]
│   │   ├── 🔑 key "requires" [L5]
│   │   ├── 🔑 key "packages" [L6]
│   │   │   ├── 📞 [CALLS]: node_modules/pstree.remy, bin/semver.js, cli.js, node_modules/socket.io, ipaddr.js, node_modules/engine.io, bin/nodetouch.js, bin/nodemon.js, node_modules/ipaddr.js
│   ├── package.json [📂 extraction_target_project/package.json] -> [💡 📦 json_keys: 8개 포착 | 🔑 "name" [str] | 🔑 "version" [str] | 🔑 "type" [str] | 🔑 "description" [str] | 🔑 "main" [str] | ...외 3개]
│   │   ├── 🔑 key "name" [L2]
│   │   ├── 🔑 key "version" [L3]
│   │   ├── 🔑 key "type" [L4]
│   │   ├── 🔑 key "description" [L5]
│   │   ├── 🔑 key "main" [L6]
│   │   │   ├── 📞 [CALLS]: index.js
│   │   ├── 🔑 key "scripts" [L7]
│   │   │   ├── 📞 [CALLS]: index.js
│   │   ├── 🔑 key "license" [L15]
│   │   ├── 🔑 key "dependencies" [L16]
│   ├── prompt.md [📂 extraction_target_project/prompt.md] -> [General File (319 lines)]
│   ├── README.md [📂 extraction_target_project/README.md] -> [General File (126 lines)]
│   ├── start.bat [📂 extraction_target_project/start.bat] -> [General File (25 lines)]
├── oldplan/
│   ├── agent_plan1.md [📂 oldplan/agent_plan1.md] -> [General File (324 lines)]
│   ├── agent_plan2.md [📂 oldplan/agent_plan2.md] -> [General File (592 lines)]
│   ├── agent_plan3.md [📂 oldplan/agent_plan3.md] -> [General File (980 lines)]
├── prompt.md [📂 prompt.md] -> [General File (113 lines)]
├── README.md [📂 README.md] -> [General File (220 lines)]
├── run_test.py [📂 run_test.py] -> [💡 📦 imp: agent_core.plan.schemas, json, os, pathlib, pydantic, re, subprocess, sys, time, tools.multi_agent_system.agent_map_extractor, tools.multi_agent_system.agent_session, tools.multi_agent_system.browser_agent_runner, tools.multi_agent_system.browser_tester, tools.multi_agent_system.project_scale_detector, tools.multi_agent_system.terminal_runner, typing, urllib.request | 🧬 class PatchItem [L24-27] | 🧬 class PatchPayload [L29-30] | 🎯 def build_log_regex_pattern(template_msg) [L32-38] | 🎯 def load_mission_file(mission_rel_path) [L40-55] | 🎯 def clean_json_response(raw_response) [L57-63] | 🎯 def run_step_worker_pipeline(mission_rel_path) [L68-602] | 🎯 def main() [L607-616]]
│   ├── 🧬 class PatchItem [L24-L27]
│   ├── 🧬 class PatchPayload [L29-L30]
│   ├── 🎯 def build_log_regex_pattern() [L32-L38]
│   ├── 🎯 def load_mission_file() [L40-L55]
│   │   ├── 🔗 [USED BY]: ::run_step_worker_pipeline
│   ├── 🎯 def clean_json_response() [L57-L63]
│   ├── 🎯 def run_step_worker_pipeline() [L68-L602]
│   │   ├── 📞 [CALLS]: load_mission_file, safe_execute_step, build_log_regex_pattern, clean_json_response
│   │   ├── 🔗 [USED BY]: ::main
│   ├── 🎯 def main() [L607-L616]
│   │   ├── 📞 [CALLS]: run_step_worker_pipeline
├── scan_debug.txt [📂 scan_debug.txt] -> [General File (296 lines)]
├── setup_architecture.bat [📂 setup_architecture.bat] -> [General File (104 lines)]
├── start.py [📂 start.py] -> [💡 📦 imp: os, pathlib, shutil, stat, subprocess, sys, time | 🎯 def get_best_python() [L33-50] | 🎯 def auto_install_dependencies() [L59-80] | 🎯 def main() [L82-201]]
│   ├── 🎯 def get_best_python() [L33-L50]
│   ├── 🎯 def auto_install_dependencies() [L59-L80]
│   │   ├── 🔗 [USED BY]: ::main
│   ├── 🎯 def main() [L82-L201]
│   │   ├── 📞 [CALLS]: auto_install_dependencies
├── System Prompt.md [📂 System Prompt.md] -> [General File (29 lines)]
├── tools/
│   ├── multi_agent_system/
│   │   ├── __init__.py [📂 tools/multi_agent_system/__init__.py]
│   │   ├── agent_code_extractor.py [📂 tools/multi_agent_system/agent_code_extractor.py] -> [💡 📦 imp: json, pathlib, re, switch, sys, traceback | 🧬 class CodeExtractor [L16-318] |     └─ def __init__(root_dir) [L22-48] |     └─ def _load_database() [L50-57] |     └─ def resolve_file_path(raw_path_str) [L59-101] |     └─ def extract_multi_slices(raw_prompt) [L103-260] |     └─ def format_as_markdown(extracted_slices) [L262-282] |     └─ def process(raw_prompt, auto_save, output_path) [L284-318]]
│   │   │   ├── 🧬 class CodeExtractor [L16-L318]
│   │   │   ├── 🎯 def __init__() [L22-L48]
│   │   │   ├── 🎯 def _load_database() [L50-L57]
│   │   │   ├── 🎯 def resolve_file_path() [L59-L101]
│   │   │   ├── 🎯 def extract_multi_slices() [L103-L260]
│   │   │   ├── 🎯 def format_as_markdown() [L262-L282]
│   │   │   ├── 🎯 def process() [L284-L318]
│   │   ├── agent_map_extractor.py [📂 tools/multi_agent_system/agent_map_extractor.py] -> [💡 📦 imp: json, os, pathlib, sys, tools.universal_indexer.core_parsers.gitignore_parser, tools.universal_indexer.map_formatter, typing | 🧬 class AgentMapExtractor [L46-251] |     └─ def __init__(project_root) [L49-50] |     └─ def _load_jjap_context() [L52-59] |     └─ def _load_all_symbols() [L61-79] |     └─ def _load_registry_and_protocols() [L81-118] |     └─ def _normalize_path(raw_path) [L120-128] |     └─ def collect_files_in_targets(target_paths, exclude_paths) [L130-181] |     └─ def generate_custom_map(target_paths, exclude_paths, save_to_file) [L183-251] | 🎯 def extract_targeted_ai_map(target_paths, exclude_paths, save_to_file) [L254-260]]
│   │   │     ├── 🔑 [REGISTRY]: "AgentMapExtractor"
│   │   │   ├── 🧬 class AgentMapExtractor [L46-L251]
│   │   │   │   ├── 🔗 [USED BY]: ::extract_targeted_ai_map
│   │   │   ├── 🎯 def __init__() [L49-L50]
│   │   │   ├── 🎯 def _load_jjap_context() [L52-L59]
│   │   │   ├── 🎯 def _load_all_symbols() [L61-L79]
│   │   │   ├── 🎯 def _load_registry_and_protocols() [L81-L118]
│   │   │   ├── 🎯 def _normalize_path() [L120-L128]
│   │   │   ├── 🎯 def collect_files_in_targets() [L130-L181]
│   │   │   ├── 🎯 def generate_custom_map() [L183-L251]
│   │   │   ├── 🎯 def extract_targeted_ai_map() [L254-L260]
│   │   │   │   ├── 📞 [CALLS]: AgentMapExtractor
│   │   ├── agent_session.py [📂 tools/multi_agent_system/agent_session.py] -> [💡 📦 imp: agent_core.llm.gemini_client, google, google.genai, os, pathlib, time, tools.multi_agent_system.agent_code_extractor, tools.multi_agent_system.agent_map_extractor, tools.multi_agent_system.code_patcher, tools.multi_agent_system.project_scale_detector, tools.multi_agent_system.terminal_runner, typing | 🧬 class KeyManager [L20-93] |     └─ def __init__(env_path) [L22-80] |     └─ def get_current_key() [L82-85] |     └─ def rotate_key() [L87-93] | 🧬 class AgentSessionFactory [L97-327] |     └─ def __init__(root_dir) [L99-113] |     └─ def switch_to_next_key(last_error_msg) [L115-119] |     └─ def prepare_step1_map(max_shallow_depth) [L121-143] |     └─ def execute_worker_step(prompt, system_instruction, response_mime_type, max_retries) [L146-198] |     └─ def _build_tools() [L200-231] |     └─ def create_browser_agent_session(preferred_lite_model) [L233-258] |     └─ def create_chat_session(model_name, shallow_depth) [L260-327]]
│   │   │     ├── 🔑 [REGISTRY]: "AgentSessionFactory"
│   │   │   ├── 🧬 class KeyManager [L20-L93]
│   │   │   │   ├── 🔗 [USED BY]: ::__init__
│   │   │   ├── 🎯 def __init__() [L22-L80]
│   │   │   ├── 🎯 def get_current_key() [L82-L85]
│   │   │   ├── 🎯 def rotate_key() [L87-L93]
│   │   │   ├── 🧬 class AgentSessionFactory [L97-L327]
│   │   │   ├── 🎯 def __init__() [L99-L113]
│   │   │   │   ├── 📞 [CALLS]: KeyManager
│   │   │   ├── 🎯 def switch_to_next_key() [L115-L119]
│   │   │   ├── 🎯 def prepare_step1_map() [L121-L143]
│   │   │   ├── 🎯 def execute_worker_step() [L146-L198]
│   │   │   ├── 🎯 def _build_tools() [L200-L231]
│   │   │   ├── 🎯 def create_browser_agent_session() [L233-L258]
│   │   │   ├── 🎯 def create_chat_session() [L260-L327]
│   │   ├── browser_agent_runner.py [📂 tools/multi_agent_system/browser_agent_runner.py] -> [💡 📦 imp: json, pydantic, re, time, tools.multi_agent_system.browser_tester, typing | 🧬 class BrowserActionSchema [L8-11] | 🧬 class BrowserAgentRunner [L13-133] |     └─ def __init__(session_factory) [L14-15] |     └─ def run_autonomous_loop(target_url, goal_description, expected_patterns, max_steps) [L17-133]]
│   │   │     ├── 🔑 [REGISTRY]: "BrowserAgentRunner"
│   │   │   ├── 🧬 class BrowserActionSchema [L8-L11]
│   │   │   ├── 🧬 class BrowserAgentRunner [L13-L133]
│   │   │   ├── 🎯 def __init__() [L14-L15]
│   │   │   ├── 🎯 def run_autonomous_loop() [L17-L133]
│   │   ├── browser_tester.py [📂 tools/multi_agent_system/browser_tester.py] -> [💡 📦 imp: pathlib, playwright.sync_api, re, subprocess, sys, time, typing | 🎯 def ensure_playwright() [L12-27] | 🧬 class BrowserTester [L29-190] |     └─ def __init__(headless, default_timeout) [L30-32] |     └─ def extract_interactive_elements(page) [L34-58] |     └─ def capture_compressed_screenshot(page) [L60-68] |     └─ def run_browser_verification(target_url, actions, expected_patterns, wait_for_selector) [L70-190]]
│   │   │   ├── 🎯 def ensure_playwright() [L12-L27]
│   │   │   │   ├── 🔗 [USED BY]: ::run_browser_verification
│   │   │   ├── 🧬 class BrowserTester [L29-L190]
│   │   │   ├── 🎯 def __init__() [L30-L32]
│   │   │   ├── 🎯 def extract_interactive_elements() [L34-L58]
│   │   │   ├── 🎯 def capture_compressed_screenshot() [L60-L68]
│   │   │   ├── 🎯 def run_browser_verification() [L70-L190]
│   │   │   │   ├── 📞 [CALLS]: ensure_playwright
│   │   ├── code_patcher.py [📂 tools/multi_agent_system/code_patcher.py] -> [💡 📦 imp: pathlib | 🧬 class CodePatcher [L9-81] |     └─ def __init__(root_dir) [L10-11] |     └─ def apply_patch(rel_path, existing_code, replacement_code) [L13-81]]
│   │   │   ├── 🧬 class CodePatcher [L9-L81]
│   │   │   ├── 🎯 def __init__() [L10-L11]
│   │   │   ├── 🎯 def apply_patch() [L13-L81]
│   │   ├── project_scale_detector.py [📂 tools/multi_agent_system/project_scale_detector.py] -> [💡 📦 imp: mimetypes, os, pathlib, tools.universal_indexer.core_parsers.gitignore_parser, typing | 🧬 class ProjectScaleDetector [L31-178] |     └─ def __init__(project_root, max_files, max_total_lines, max_estimated_tokens, max_file_size_bytes, sample_line_limit) [L32-47] |     └─ def _is_binary_file(file_path) [L49-66] |     └─ def analyze_project_scale(target_dir) [L68-138] |     └─ def generate_shallow_structure_map(max_depth, target_dir) [L140-178]]
│   │   │   ├── 🧬 class ProjectScaleDetector [L31-L178]
│   │   │   ├── 🎯 def __init__() [L32-L47]
│   │   │   ├── 🎯 def _is_binary_file() [L49-L66]
│   │   │   ├── 🎯 def analyze_project_scale() [L68-L138]
│   │   │   ├── 🎯 def generate_shallow_structure_map() [L140-L178]
│   │   │   │   ├── 📞 [CALLS]: _build_tree
│   │   ├── terminal_runner.py [📂 tools/multi_agent_system/terminal_runner.py] -> [💡 📦 imp: pathlib, subprocess | 🎯 def run_terminal_command(command, cwd, timeout, env) [L12-59]]
│   │   │   ├── 🎯 def run_terminal_command() [L12-L59]
│   ├── universal_indexer/
│   │   ├── agent_navigator.py [📂 tools/universal_indexer/agent_navigator.py] -> [💡 📦 imp: json, pathlib, re, switch, sys, tkinter, traceback | 🧬 class CodeExtractor [L18-281] |     └─ def __init__(root_dir) [L23-46] |     └─ def _load_database() [L48-55] |     └─ def resolve_file_path(raw_path_str) [L57-85] |     └─ def extract_multi_slices(raw_prompt) [L87-237] |     └─ def format_as_markdown(extracted_slices) [L239-256] |     └─ def process(raw_prompt, auto_save, output_path) [L258-281] | 🧬 class JjapCursorNavigatorGUI [L288-384] |     └─ def __init__(root, project_root) [L289-339] |     └─ def execute_slicing_pipeline() [L341-366] |     └─ def manual_export_file() [L368-384]]
│   │   │     ├── 🔑 [REGISTRY]: "JjapCursorNavigatorGUI"
│   │   │   ├── 🧬 class CodeExtractor [L18-L281]
│   │   │   ├── 🎯 def __init__() [L23-L46]
│   │   │   ├── 🎯 def _load_database() [L48-L55]
│   │   │   ├── 🎯 def resolve_file_path() [L57-L85]
│   │   │   ├── 🎯 def extract_multi_slices() [L87-L237]
│   │   │   ├── 🎯 def format_as_markdown() [L239-L256]
│   │   │   ├── 🎯 def process() [L258-L281]
│   │   │   ├── 🧬 class JjapCursorNavigatorGUI [L288-L384]
│   │   │   ├── 🎯 def __init__() [L289-L339]
│   │   │   │   ├── 📞 [CALLS]: CodeExtractor
│   │   │   ├── 🎯 def execute_slicing_pipeline() [L341-L366]
│   │   │   ├── 🎯 def manual_export_file() [L368-L384]
│   │   ├── config.py [📂 tools/universal_indexer/config.py] -> [💡 📦 imp: pathlib, switch, sys, tools.universal_indexer.switch | 🎯 def get_project_root() [L8-16] | 🎯 def get_scan_mode() [L23-33]]
│   │   │   ├── 🎯 def get_project_root() [L8-L16]
│   │   │   ├── 🎯 def get_scan_mode() [L23-L33]
│   │   ├── context_builder.py [📂 tools/universal_indexer/context_builder.py] -> [💡 📦 imp: os, pathlib, tools.universal_indexer.core_parsers.gitignore_parser | 🧬 class ContextBuilder [L14-119] |     └─ def __init__(project_root) [L17-20] |     └─ def read_and_clean_file(relative_path) [L22-86] |     └─ def assemble_ai_prompt(user_query, affected_files) [L88-119]]
│   │   │   ├── 🧬 class ContextBuilder [L14-L119]
│   │   │   ├── 🎯 def __init__() [L17-L20]
│   │   │   ├── 🎯 def read_and_clean_file() [L22-L86]
│   │   │   ├── 🎯 def assemble_ai_prompt() [L88-L119]
│   │   ├── core_parsers/
│   │   │   ├── __init__.py [📂 tools/universal_indexer/core_parsers/__init__.py]
│   │   │   ├── cs_parser.py [📂 tools/universal_indexer/core_parsers/cs_parser.py]
│   │   │   ├── gitignore_parser.py [📂 tools/universal_indexer/core_parsers/gitignore_parser.py] -> [💡 📦 imp: os, pathlib, pathspec | 🧬 class GitIgnoreMatcher [L8-57] |     └─ def __init__(project_root) [L11-13] |     └─ def _load_specs() [L15-44] |     └─ def is_ignored(relative_path) [L46-57]]
│   │   │   │   ├── 🧬 class GitIgnoreMatcher [L8-L57]
│   │   │   │   ├── 🎯 def __init__() [L11-L13]
│   │   │   │   ├── 🎯 def _load_specs() [L15-L44]
│   │   │   │   ├── 🎯 def is_ignored() [L46-L57]
│   │   │   ├── java_parser.py [📂 tools/universal_indexer/core_parsers/java_parser.py] -> [💡 📦 imp: hashlib, pathlib, re | 🎯 def _find_matching_curly_brace(lines, start_line_idx) [L15-37] | 🎯 def extract_symbols(file_path, project_root) [L39-194]]
│   │   │   │   ├── 🎯 def _find_matching_curly_brace() [L15-L37]
│   │   │   │   │   ├── 🔗 [USED BY]: ::extract_symbols
│   │   │   │   ├── 🎯 def extract_symbols() [L39-L194]
│   │   │   │   │   ├── 📞 [CALLS]: log, _find_matching_curly_brace
│   │   │   ├── js_parser.py [📂 tools/universal_indexer/core_parsers/js_parser.py] -> [💡 📦 imp: hashlib, pathlib, re, sys | 🎯 def debug_log(message) [L12-14] | 🎯 def find_end_line_by_braces(lines, start_line_idx, max_search_range) [L17-47] | 🎯 def extract_symbols(file_path, project_root) [L50-171]]
│   │   │   │   ├── 🎯 def debug_log() [L12-L14]
│   │   │   │   ├── 🎯 def find_end_line_by_braces() [L17-L47]
│   │   │   │   │   ├── 🔗 [USED BY]: ::extract_symbols
│   │   │   │   ├── 🎯 def extract_symbols() [L50-L171]
│   │   │   │   │   ├── 📞 [CALLS]: find_end_line_by_braces
│   │   │   ├── json_parser.py [📂 tools/universal_indexer/core_parsers/json_parser.py] -> [💡 📦 imp: hashlib, json, pathlib, re | 🎯 def extract_symbols(file_path, project_root) [L6-127]]
│   │   │   │   ├── 🎯 def extract_symbols() [L6-L127]
│   │   │   ├── py_parser.py [📂 tools/universal_indexer/core_parsers/py_parser.py] -> [💡 📦 imp: ast, hashlib, pathlib | 🎯 def _extract_py_args(node) [L5-15] | 🎯 def extract_symbols(file_path, project_root) [L17-176]]
│   │   │   │   ├── 🎯 def _extract_py_args() [L5-L15]
│   │   │   │   │   ├── 🔗 [USED BY]: ::extract_symbols
│   │   │   │   ├── 🎯 def extract_symbols() [L17-L176]
│   │   │   │   │   ├── 📞 [CALLS]: _extract_py_args
│   │   ├── create_ai_map.py [📂 tools/universal_indexer/create_ai_map.py] -> [💡 📦 imp: ast, json, map_formatter, os, pathlib, tools.universal_indexer.config | 🎯 def load_jjap_context() [L19-30] | 🎯 def collect_target_files() [L33-64] | 🎯 def load_registry() [L67-97] | 🎯 def load_protocols() [L100-117] | 🎯 def parse_protocols_and_registries() [L120-159] | 🎯 def load_all_symbols() [L163-184] | 🎯 def main() [L187-318] | 🎯 def generate_ai_optimized_map() [L321-322]]
│   │   │   ├── 🎯 def load_jjap_context() [L19-L30]
│   │   │   │   ├── 🔗 [USED BY]: ::main
│   │   │   ├── 🎯 def collect_target_files() [L33-L64]
│   │   │   │   ├── 🔗 [USED BY]: ::main
│   │   │   ├── 🎯 def load_registry() [L67-L97]
│   │   │   │   ├── 🔗 [USED BY]: ::parse_protocols_and_registries
│   │   │   ├── 🎯 def load_protocols() [L100-L117]
│   │   │   │   ├── 🔗 [USED BY]: ::parse_protocols_and_registries
│   │   │   ├── 🎯 def parse_protocols_and_registries() [L120-L159]
│   │   │   │   ├── 📞 [CALLS]: load_registry, load_protocols
│   │   │   │   ├── 🔗 [USED BY]: ::main
│   │   │   ├── 🎯 def load_all_symbols() [L163-L184]
│   │   │   │   ├── 🔗 [USED BY]: ::main
│   │   │   ├── 🎯 def main() [L187-L318]
│   │   │   │   ├── 📞 [CALLS]: collect_target_files, load_all_symbols, load_jjap_context, parse_protocols_and_registries
│   │   │   ├── 🎯 def generate_ai_optimized_map() [L321-L322]
│   │   │   │   ├── 📞 [CALLS]: main
│   │   ├── indexer.py [📂 tools/universal_indexer/indexer.py] -> [💡 📦 imp: collections, config, hashlib, importlib.util, json, os, pathlib, typing | 🎯 def log(message) [L22-24] | 🧬 class AdvancedIndexerV2 [L26-217] |     └─ def __init__(project_root) [L31-41] |     └─ def _auto_load_parsers() [L43-74] |     └─ def scan_project() [L78-152] |     └─ def index_file(file_path, ext) [L154-194] |     └─ def save_index_data() [L196-217]]
│   │   │     ├── 🔑 [REGISTRY]: "AdvancedIndexerV2"
│   │   │   ├── 🎯 def log() [L22-L24]
│   │   │   │   ├── 🔗 [USED BY]: tools/universal_indexer/core_parsers/java_parser.py::extract_symbols
│   │   │   ├── 🧬 class AdvancedIndexerV2 [L26-L217]
│   │   │   ├── 🎯 def __init__() [L31-L41]
│   │   │   ├── 🎯 def _auto_load_parsers() [L43-L74]
│   │   │   ├── 🎯 def scan_project() [L78-L152]
│   │   │   ├── 🎯 def index_file() [L154-L194]
│   │   │   ├── 🎯 def save_index_data() [L196-L217]
│   │   ├── jjap_lookup.py [📂 tools/universal_indexer/jjap_lookup.py] -> [💡 📦 imp: argparse, json, pathlib, sys | 🎯 def load_json(file_path) [L17-22] | 🎯 def lookup_symbol(symbol_name) [L24-51] | 🎯 def show_skeleton(file_path) [L53-69]]
│   │   │   ├── 🎯 def load_json() [L17-L22]
│   │   │   │   ├── 🔗 [USED BY]: ::lookup_symbol, ::show_skeleton
│   │   │   ├── 🎯 def lookup_symbol() [L24-L51]
│   │   │   │   ├── 📞 [CALLS]: load_json
│   │   │   ├── 🎯 def show_skeleton() [L53-L69]
│   │   │   │   ├── 📞 [CALLS]: load_json
│   │   ├── jjap_retriever.py [📂 tools/universal_indexer/jjap_retriever.py] -> [💡 📦 imp: json, os, pathlib, sys, typing | 🧬 class JjapRetriever [L9-136] |     └─ def __init__(project_root) [L16-21] |     └─ def _load_symbols() [L23-38] |     └─ def retrieve_symbol(query) [L40-102] |     └─ def _find_best_match(query) [L104-124] |     └─ def _safe_truncate(text) [L126-136] | 🎯 def main() [L139-147]]
│   │   │     ├── 🔑 [REGISTRY]: "JjapRetriever"
│   │   │   ├── 🧬 class JjapRetriever [L9-L136]
│   │   │   │   ├── 🔗 [USED BY]: ::main
│   │   │   ├── 🎯 def __init__() [L16-L21]
│   │   │   ├── 🎯 def _load_symbols() [L23-L38]
│   │   │   ├── 🎯 def retrieve_symbol() [L40-L102]
│   │   │   ├── 🎯 def _find_best_match() [L104-L124]
│   │   │   ├── 🎯 def _safe_truncate() [L126-L136]
│   │   │   ├── 🎯 def main() [L139-L147]
│   │   │   │   ├── 📞 [CALLS]: JjapRetriever
│   │   ├── jjap_watcher.py [📂 tools/universal_indexer/jjap_watcher.py] -> [💡 📦 imp: importlib.util, os, pathlib, sys, time, traceback, watchdog.observers, watchdog.observers.polling | 🎯 def import_file_directly(module_name, file_path) [L25-33] | 🎯 def run_pipeline() [L35-78] | 🧬 class CodeChangeHandler [L81-126] |     └─ def __init__() [L82-84] |     └─ def dispatch(event) [L86-126] | 🎯 def main() [L128-154]]
│   │   │     ├── 🔑 [REGISTRY]: "CodeChangeHandler"
│   │   │   ├── 🎯 def import_file_directly() [L25-L33]
│   │   │   │   ├── 🔗 [USED BY]: ::run_pipeline
│   │   │   ├── 🎯 def run_pipeline() [L35-L78]
│   │   │   │   ├── 📞 [CALLS]: import_file_directly
│   │   │   │   ├── 🔗 [USED BY]: ::dispatch, ::main
│   │   │   ├── 🧬 class CodeChangeHandler [L81-L126]
│   │   │   │   ├── 🔗 [USED BY]: ::main
│   │   │   ├── 🎯 def __init__() [L82-L84]
│   │   │   ├── 🎯 def dispatch() [L86-L126]
│   │   │   │   ├── 📞 [CALLS]: run_pipeline
│   │   │   ├── 🎯 def main() [L128-L154]
│   │   │   │   ├── 📞 [CALLS]: run_pipeline, CodeChangeHandler
│   │   ├── map_formatter.py [📂 tools/universal_indexer/map_formatter.py] -> [💡 📦 imp: pathlib, typing | 🎯 def get_file_symbols_summary(file_meta) [L4-8] | 🎯 def format_symbol_node(sym, symbol_by_id, current_posix_path, indent) [L10-73]]
│   │   │   ├── 🎯 def get_file_symbols_summary() [L4-L8]
│   │   │   ├── 🎯 def format_symbol_node() [L10-L73]
│   │   ├── README.md [📂 tools/universal_indexer/README.md] -> [General File (35 lines)]
│   │   ├── rule.txt [📂 tools/universal_indexer/rule.txt] -> [General File (24 lines)]
│   │   ├── switch.py [📂 tools/universal_indexer/switch.py]
│   │   ├── tree_sitter_parser.py [📂 tools/universal_indexer/tree_sitter_parser.py] -> [💡 📦 imp: collections, config, hashlib, pathlib, tree_sitter_languages | 🎯 def extract_symbols(file_path, project_root) [L24-179]]
│   │   │   ├── 🎯 def extract_symbols() [L24-L179]
│   │   │   │   ├── 📞 [CALLS]: traverse
│   │   ├── update_map.py [📂 tools/universal_indexer/update_map.py] -> [💡 📦 imp: json, pathlib | 🎯 def update_map() [L4-103]]
│   │   │   ├── 🎯 def update_map() [L4-L103]
