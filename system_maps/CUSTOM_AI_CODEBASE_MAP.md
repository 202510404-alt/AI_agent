# 🏗️ CUSTOM TARGETED AI-OPTIMIZED CODEBASE MAP
> **[추출 범위 지정]** Target Paths: `None`
```markdown
project_root/
├── .gitignore [📂 .gitignore] -> [General File (23 lines)]
├── .idea/
│   ├── .gitignore [📂 .idea/.gitignore] -> [General File (10 lines)]
│   ├── AI_agent.iml [📂 .idea/AI_agent.iml] -> [General File (9 lines)]
│   ├── gradle.xml [📂 .idea/gradle.xml] -> [General File (17 lines)]
│   ├── misc.xml [📂 .idea/misc.xml] -> [General File (7 lines)]
│   ├── modules.xml [📂 .idea/modules.xml] -> [General File (8 lines)]
│   ├── vcs.xml [📂 .idea/vcs.xml] -> [General File (6 lines)]
│   ├── workspace.xml [📂 .idea/workspace.xml] -> [General File (185 lines)]
├── a [📂 a] -> [General File (22 lines)]
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
│   │   ├── gemini_client.py [📂 agent_core/llm/gemini_client.py] -> [💡 📦 imp: agent_core.plan.schemas, google, google.genai, json, os, pathlib, re, time, typing | 🎯 def log_debug(message_func) [L23-32] | 🎯 def load_env_file(env_path) [L35-70] | 🎯 def resolve_best_gemini_model(client, blocked_models) [L96-105] | 🧬 class DynamicKeyModelManager [L108-169] |     └─ def __init__(root_dir) [L115-123] |     └─ def get_available_pair() [L125-154] |     └─ def report_error(key_name, model_name, error_str) [L156-169] | 🧬 class GeminiPlannerClient [L172-214] |     └─ def __init__(api_key, root_dir) [L173-176] |     └─ def generate_plan(prompt, model_name, max_retries) [L178-214]]
│   │   │   ├── 🎯 def log_debug() [L23-L32]
│   │   │   ├── 🎯 def load_env_file() [L35-L70]
│   │   │   │   ├── 📞 [CALLS]: log_debug
│   │   │   │   ├── 🔗 [USED BY]: ::__init__, ::get_available_pair
│   │   │   ├── 🎯 def resolve_best_gemini_model() [L96-L105]
│   │   │   ├── 🧬 class DynamicKeyModelManager [L108-L169]
│   │   │   │   ├── 🔗 [USED BY]: ::__init__
│   │   │   ├── 🎯 def __init__() [L115-L123]
│   │   │   │   ├── 📞 [CALLS]: load_env_file
│   │   │   ├── 🎯 def get_available_pair() [L125-L154]
│   │   │   │   ├── 📞 [CALLS]: load_env_file
│   │   │   ├── 🎯 def report_error() [L156-L169]
│   │   │   ├── 🧬 class GeminiPlannerClient [L172-L214]
│   │   │   ├── 🎯 def __init__() [L173-L176]
│   │   │   │   ├── 📞 [CALLS]: DynamicKeyModelManager
│   │   │   ├── 🎯 def generate_plan() [L178-L214]
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
│   │   ├── test_ai_chat.py [📂 agent_core/plan/test_ai_chat.py] -> [💡 📦 imp: agent_core.plan.gemini_client, agent_core.plan.prompt_builder, google, google.genai, json, os, pathlib, sys, tools.multi_agent_system.agent_code_extractor | 🎯 def extract_code_slice(file_and_line) [L32-43] | 🎯 def run_interactive_chat() [L49-104]]
│   │   │   ├── 🎯 def extract_code_slice() [L32-L43]
│   │   │   ├── 🎯 def run_interactive_chat() [L49-L104]
│   ├── validation/
│   │   ├── __init__.py [📂 agent_core/validation/__init__.py]
├── agent_debug.log [📂 agent_debug.log] -> [General File (3 lines)]
├── agent_plan.md [📂 agent_plan.md] -> [General File (1101 lines)]
├── extraction_target_project/
│   ├── .gitignore [📂 extraction_target_project/.gitignore] -> [General File (4 lines)]
│   ├── AI_agent.code-workspace [📂 extraction_target_project/AI_agent.code-workspace] -> [General File (26 lines)]
│   ├── client/
│   │   ├── .gitignore [📂 extraction_target_project/client/.gitignore] -> [General File (21 lines)]
│   │   ├── public/
│   │   │   ├── favicon.svg [📂 extraction_target_project/client/public/favicon.svg] -> [General File (19 lines)]
│   │   │   ├── index.html [📂 extraction_target_project/client/public/index.html] -> [General File (21 lines)]
│   │   │   ├── logo.svg [📂 extraction_target_project/client/public/logo.svg] -> [General File (19 lines)]
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
│   ├── prompt.md [📂 extraction_target_project/prompt.md] -> [General File (319 lines)]
│   ├── README.md [📂 extraction_target_project/README.md] -> [General File (126 lines)]
│   ├── start.bat [📂 extraction_target_project/start.bat] -> [General File (25 lines)]
├── oldplan/
│   ├── agent_plan1.md [📂 oldplan/agent_plan1.md] -> [General File (324 lines)]
│   ├── agent_plan2.md [📂 oldplan/agent_plan2.md] -> [General File (592 lines)]
│   ├── agent_plan3.md [📂 oldplan/agent_plan3.md] -> [General File (980 lines)]
├── prompt.md [📂 prompt.md] -> [General File (113 lines)]
├── README.md [📂 README.md] -> [General File (220 lines)]
├── run_test.py [📂 run_test.py] -> [💡 📦 imp: agent_core.plan.schemas, json, os, pathlib, re, sys, tools.multi_agent_system.agent_map_extractor, tools.multi_agent_system.agent_session, tools.multi_agent_system.browser_tester, tools.multi_agent_system.project_scale_detector, tools.multi_agent_system.terminal_runner | 🎯 def build_log_regex_pattern(template_msg) [L18-24] | 🎯 def load_mission_file(mission_rel_path) [L26-41] | 🎯 def clean_json_response(raw_response) [L43-49] | 🎯 def run_step_worker_pipeline(mission_rel_path) [L54-484] | 🎯 def main() [L489-498]]
│   ├── 🎯 def build_log_regex_pattern() [L18-L24]
│   ├── 🎯 def load_mission_file() [L26-L41]
│   │   ├── 🔗 [USED BY]: ::run_step_worker_pipeline
│   ├── 🎯 def clean_json_response() [L43-L49]
│   ├── 🎯 def run_step_worker_pipeline() [L54-L484]
│   │   ├── 📞 [CALLS]: clean_json_response, build_log_regex_pattern, safe_execute_step, load_mission_file
│   │   ├── 🔗 [USED BY]: ::main
│   ├── 🎯 def main() [L489-L498]
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
│   │   ├── agent_session.py [📂 tools/multi_agent_system/agent_session.py] -> [💡 📦 imp: agent_core.llm.gemini_client, google, google.genai, os, pathlib, time, tools.multi_agent_system.agent_code_extractor, tools.multi_agent_system.agent_map_extractor, tools.multi_agent_system.code_patcher, tools.multi_agent_system.project_scale_detector, tools.multi_agent_system.terminal_runner, typing | 🧬 class KeyManager [L20-93] |     └─ def __init__(env_path) [L22-80] |     └─ def get_current_key() [L82-85] |     └─ def rotate_key() [L87-93] | 🧬 class AgentSessionFactory [L97-296] |     └─ def __init__(root_dir) [L99-113] |     └─ def switch_to_next_key(last_error_msg) [L115-119] |     └─ def prepare_step1_map(max_shallow_depth) [L121-143] |     └─ def execute_worker_step(prompt, system_instruction, response_mime_type, max_retries) [L146-195] |     └─ def _build_tools() [L197-228] |     └─ def create_chat_session(model_name, shallow_depth) [L230-296]]
│   │   │     ├── 🔑 [REGISTRY]: "AgentSessionFactory"
│   │   │   ├── 🧬 class KeyManager [L20-L93]
│   │   │   │   ├── 🔗 [USED BY]: ::__init__
│   │   │   ├── 🎯 def __init__() [L22-L80]
│   │   │   ├── 🎯 def get_current_key() [L82-L85]
│   │   │   ├── 🎯 def rotate_key() [L87-L93]
│   │   │   ├── 🧬 class AgentSessionFactory [L97-L296]
│   │   │   ├── 🎯 def __init__() [L99-L113]
│   │   │   │   ├── 📞 [CALLS]: KeyManager
│   │   │   ├── 🎯 def switch_to_next_key() [L115-L119]
│   │   │   ├── 🎯 def prepare_step1_map() [L121-L143]
│   │   │   ├── 🎯 def execute_worker_step() [L146-L195]
│   │   │   ├── 🎯 def _build_tools() [L197-L228]
│   │   │   ├── 🎯 def create_chat_session() [L230-L296]
│   │   ├── browser_tester.py [📂 tools/multi_agent_system/browser_tester.py] -> [💡 📦 imp: pathlib, playwright.sync_api, re, subprocess, sys, time, typing | 🎯 def ensure_playwright() [L12-27] | 🧬 class BrowserTester [L29-149] |     └─ def __init__(headless, default_timeout) [L30-32] |     └─ def run_browser_verification(target_url, actions, expected_patterns, wait_for_selector) [L34-149]]
│   │   │   ├── 🎯 def ensure_playwright() [L12-L27]
│   │   │   │   ├── 🔗 [USED BY]: ::run_browser_verification
│   │   │   ├── 🧬 class BrowserTester [L29-L149]
│   │   │   ├── 🎯 def __init__() [L30-L32]
│   │   │   ├── 🎯 def run_browser_verification() [L34-L149]
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
│   │   │   │   │   ├── 📞 [CALLS]: _find_matching_curly_brace, log
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
│   │   │   │   ├── 📞 [CALLS]: collect_target_files, parse_protocols_and_registries, load_jjap_context, load_all_symbols
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
│   │   │   │   ├── 📞 [CALLS]: CodeChangeHandler, run_pipeline
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
```
