# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)

> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.
> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.

```markdown
project_root/
├── .env [📂 .env]
├── .gitignore [📂 .gitignore]
├── .idea/
│   ├── .gitignore [📂 .idea/.gitignore]
│   ├── AI_agent.iml [📂 .idea/AI_agent.iml]
│   ├── gradle.xml [📂 .idea/gradle.xml]
│   ├── misc.xml [📂 .idea/misc.xml]
│   ├── modules.xml [📂 .idea/modules.xml]
│   ├── vcs.xml [📂 .idea/vcs.xml]
│   ├── workspace.xml [📂 .idea/workspace.xml]
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
├── a [📂 a]
├── agent_core/
│   ├── __init__.py [📂 agent_core/__init__.py]
│   ├── execution/
│   │   ├── __init__.py [📂 agent_core/execution/__init__.py]
│   ├── memory/
│   │   ├── __init__.py [📂 agent_core/memory/__init__.py]
│   ├── plan/
│   │   ├── __init__.py [📂 agent_core/plan/__init__.py]
│   │   ├── gemini_client.py [📂 agent_core/plan/gemini_client.py] -> [💡 📦 imp: agent_core.plan.schemas, google, google.genai, json, os, pathlib, typing | 🎯 def log_debug(message_func) [L21-30] | 🎯 def load_env_file(env_path) [L33-58] | 🧬 class GeminiPlannerClient [L61-146] |     └─ def __init__(api_key, root_dir) [L62-88] |     └─ def generate_plan(prompt, model_name) [L90-146]]
│   │   │   ├── 🎯 def log_debug() [L21-L30]
│   │   │   ├── 🎯 def load_env_file() [L33-L58]
│   │   │   │   ├── 📞 [CALLS]: log_debug
│   │   │   │   ├── 🔗 [USED BY]: ::__init__
│   │   │   ├── 🧬 class GeminiPlannerClient [L61-L146]
│   │   │   ├── 🎯 def __init__() [L62-L88]
│   │   │   │   ├── 📞 [CALLS]: log_debug, load_env_file
│   │   │   ├── 🎯 def generate_plan() [L90-L146]
│   │   │   │   ├── 📞 [CALLS]: log_debug
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
├── agent_debug.log [📂 agent_debug.log]
├── agent_plan.md [📂 agent_plan.md]
├── extraction_target_project/
│   ├── .gitignore [📂 extraction_target_project/.gitignore]
│   ├── AI_agent.code-workspace [📂 extraction_target_project/AI_agent.code-workspace]
│   ├── client/
│   │   ├── .gitignore [📂 extraction_target_project/client/.gitignore]
│   │   ├── package-lock.json [📂 extraction_target_project/client/package-lock.json] -> [💡 📦 json_keys: 5개 포착 | 🔑 "name" [str] | 🔑 "version" [str] | 🔑 "lockfileVersion" [int] | 🔑 "requires" [bool] | 🔑 "packages" [dict]]
│   │   │   ├── 🔑 key "name" [L2]
│   │   │   │   ├── 🔗 [USED BY]: ::packages
│   │   │   ├── 🔑 key "version" [L3]
│   │   │   ├── 🔑 key "lockfileVersion" [L4]
│   │   │   ├── 🔑 key "requires" [L5]
│   │   │   ├── 🔑 key "packages" [L6]
│   │   │   │   ├── 📞 [CALLS]: node_modules/util.promisify, bin/babel-parser.js, node_modules/string.prototype.trim, dist/esm/bin.mjs, bin/esgenerate.js, bin/cli.js, node_modules/lodash.merge, node_modules/lodash.memoize, node_modules/string.prototype.trimstart, bin/webpack.js, node_modules/object.values, node_modules/regexp.prototype.flags, node_modules/array.prototype.flat, bin/jest.js, bin/jiti.js, big.js, node_modules/lodash.debounce, bin/cmd.js, node_modules/css.escape, node_modules/socket.io, bin/webpack-dev-server.js, bin/escodegen.js, bin/esparse.js, node_modules/lodash.sortby, bin/nopt.js, node_modules/object.hasown, node_modules/lodash.uniq, node_modules/decimal.js, node_modules/iterator.prototype, node_modules/object.entries, node_modules/array.prototype.findlast, node_modules/array.prototype.findlastindex, node_modules/sanitize.css, bin/semver.js, bin/bin.js, node_modules/array.prototype.flatmap, bin/eslint.js, node_modules/proxy-addr/node_modules/ipaddr.js, bin/nanoid.cjs, node_modules/big.js, ipaddr.js, node_modules/function.prototype.name, bin/js-yaml.js, node_modules/fs.realpath, node_modules/resolve.exports, fraction.js, bin/react-scripts.js, node_modules/array.prototype.tosorted, node_modules/arraybuffer.prototype.slice, node_modules/ipaddr.js, cli.js, node_modules/object.groupby, node_modules/reflect.getprototypeof, node_modules/string.prototype.trimend, node_modules/engine.io, bin/esvalidate.js, node_modules/array.prototype.reduce, fixtures/cli.js, node_modules/object.assign, decimal.js, node_modules/object.getownpropertydescriptors, hpack.js, node_modules/array.prototype.toreversed, node_modules/fraction.js, lib/cli.js, node_modules/hpack.js, node_modules/object.fromentries, node_modules/string.prototype.matchall, dist/cli.cjs, bin.js
│   │   ├── package.json [📂 extraction_target_project/client/package.json] -> [💡 📦 json_keys: 7개 포착 | 🔑 "name" [str] | 🔑 "version" [str] | 🔑 "private" [bool] | 🔑 "dependencies" [dict] | 🔑 "scripts" [dict] | ...외 2개]
│   │   │   ├── 🔑 key "name" [L2]
│   │   │   ├── 🔑 key "version" [L3]
│   │   │   ├── 🔑 key "private" [L4]
│   │   │   ├── 🔑 key "dependencies" [L5]
│   │   │   ├── 🔑 key "scripts" [L21]
│   │   │   ├── 🔑 key "eslintConfig" [L27]
│   │   │   ├── 🔑 key "browserslist" [L33]
│   │   ├── public/
│   │   │   ├── favicon.ico [📂 extraction_target_project/client/public/favicon.ico]
│   │   │   ├── favicon.svg [📂 extraction_target_project/client/public/favicon.svg]
│   │   │   ├── index.html [📂 extraction_target_project/client/public/index.html]
│   │   │   ├── logo.svg [📂 extraction_target_project/client/public/logo.svg]
│   │   │   ├── logo192.png [📂 extraction_target_project/client/public/logo192.png]
│   │   │   ├── logo512.png [📂 extraction_target_project/client/public/logo512.png]
│   │   │   ├── manifest.json [📂 extraction_target_project/client/public/manifest.json] -> [💡 📦 json_keys: 7개 포착 | 🔑 "short_name" [str] | 🔑 "name" [str] | 🔑 "icons" [list] | 🔑 "start_url" [str] | 🔑 "display" [str] | ...외 2개]
│   │   │   │   ├── 🔑 key "short_name" [L2]
│   │   │   │   ├── 🔑 key "name" [L3]
│   │   │   │   ├── 🔑 key "icons" [L4]
│   │   │   │   ├── 🔑 key "start_url" [L27]
│   │   │   │   ├── 🔑 key "display" [L28]
│   │   │   │   ├── 🔑 key "theme_color" [L29]
│   │   │   │   ├── 🔑 key "background_color" [L30]
│   │   ├── src/
│   │   │   ├── App.css [📂 extraction_target_project/client/src/App.css]
│   │   │   ├── App.js [📂 extraction_target_project/client/src/App.js] -> [💡 📦 imp: ./Canvas, ./Home, react, react-hot-toast, react-router-dom | 🎯 def App() [L11~L20]]
│   │   │   │   ├── 🎯 def App() [L11-L20]
│   │   │   ├── App.test.js [📂 extraction_target_project/client/src/App.test.js] -> [💡 📦 imp: ./App, @testing-library/react]
│   │   │   ├── Button.js [📂 extraction_target_project/client/src/Button.js] -> [💡 📦 imp: react | 🎯 def Button({ value, name, buttonFunction }) [L4~L24]]
│   │   │   │   ├── 🎯 def Button() [L4-L24]
│   │   │   ├── Canvas.js [📂 extraction_target_project/client/src/Canvas.js] -> [💡 📦 imp: ./Button, ./UploadFile, ./hooks/useWebRTC, ./socket, react, react-hot-toast, react-icons/ai, react-icons/fa6, react-router-dom | 🎯 def RemoteAudio({ stream }) [L24~L54] | 🎯 def playAudio() [L32~L47] | 🎯 def handleUserInteraction() [L38~L43] | 🎯 def Canvas(props) [L56~L481] | 🎯 def changeColour(event) [L83~L86] | 🎯 def lineWidth(event) [L88~L94] | 🎯 def handleImageUploadSuccess(imageUrl) [L96~L104] | 🎯 def init() [L107~L155] | 🎯 def handleError(err) [L118~L122] | 🎯 def handleDraw(e) [L187~L203] | 🎯 def handleMoveDraw(e) [L205~L224] | 🎯 def handleNotDraw() [L226~L239] | 🎯 def undo() [L241~L254] | 🎯 def redrawCanvas(context, history = linesHistory) [L256~L278] | 🎯 def handleCanvasChange() [L284~L289] | 🎯 def clearCanvas() [L298~L305] | 🎯 def copyBoardId() [L307~L310] | 🎯 def leaveBoard() [L312~L314]]
│   │   │   │   ├── 🎯 def RemoteAudio() [L24-L54]
│   │   │   │   ├── 🎯 def playAudio() [L32-L47]
│   │   │   │   ├── 🎯 def handleUserInteraction() [L38-L43]
│   │   │   │   ├── 🎯 def Canvas() [L56-L481]
│   │   │   │   ├── 🎯 def changeColour() [L83-L86]
│   │   │   │   ├── 🎯 def lineWidth() [L88-L94]
│   │   │   │   ├── 🎯 def handleImageUploadSuccess() [L96-L104]
│   │   │   │   ├── 🎯 def init() [L107-L155]
│   │   │   │   ├── 🎯 def handleError() [L118-L122]
│   │   │   │   ├── 🎯 def handleDraw() [L187-L203]
│   │   │   │   ├── 🎯 def handleMoveDraw() [L205-L224]
│   │   │   │   ├── 🎯 def handleNotDraw() [L226-L239]
│   │   │   │   ├── 🎯 def undo() [L241-L254]
│   │   │   │   ├── 🎯 def redrawCanvas() [L256-L278]
│   │   │   │   ├── 🎯 def handleCanvasChange() [L284-L289]
│   │   │   │   ├── 🎯 def clearCanvas() [L298-L305]
│   │   │   │   ├── 🎯 def copyBoardId() [L307-L310]
│   │   │   │   ├── 🎯 def leaveBoard() [L312-L314]
│   │   │   ├── Home.js [📂 extraction_target_project/client/src/Home.js] -> [💡 📦 imp: react, react-hot-toast, react-router-dom, uuid | 🎯 def Home() [L8~L63] | 🎯 def writeId(event) [L14~L18] | 🎯 def writeUserName(event) [L20~L22] | 🎯 def generateUniqueId(event) [L24~L29] | 🎯 def joinBoard() [L31~L39]]
│   │   │   │   ├── 🎯 def Home() [L8-L63]
│   │   │   │   ├── 🎯 def writeId() [L14-L18]
│   │   │   │   ├── 🎯 def writeUserName() [L20-L22]
│   │   │   │   ├── 🎯 def generateUniqueId() [L24-L29]
│   │   │   │   ├── 🎯 def joinBoard() [L31-L39]
│   │   │   ├── hooks/
│   │   │   │   ├── useWebRTC.js [📂 extraction_target_project/client/src/hooks/useWebRTC.js] -> [💡 📦 imp: react, react-hot-toast | 🎯 def useWebRTC(socketRef, boardId, userName) [L32~L358]]
│   │   │   │   │   ├── 🎯 def useWebRTC() [L32-L358]
│   │   │   ├── index.css [📂 extraction_target_project/client/src/index.css]
│   │   │   ├── index.js [📂 extraction_target_project/client/src/index.js] -> [💡 📦 imp: ./App, ./reportWebVitals, react, react-dom/client]
│   │   │   ├── Input.js [📂 extraction_target_project/client/src/Input.js] -> [💡 📦 imp: react | 🎯 def Input(props) [L3~L9]]
│   │   │   │   ├── 🎯 def Input() [L3-L9]
│   │   │   ├── reportWebVitals.js [📂 extraction_target_project/client/src/reportWebVitals.js]
│   │   │   ├── setupTests.js [📂 extraction_target_project/client/src/setupTests.js]
│   │   │   ├── socket.js [📂 extraction_target_project/client/src/socket.js] -> [💡 📦 imp: socket.io-client | 🎯 def initSocket() [L5~L35]]
│   │   │   │   ├── 🎯 def initSocket() [L5-L35]
│   │   │   ├── style.css [📂 extraction_target_project/client/src/style.css]
│   │   │   ├── styleCanvas.css [📂 extraction_target_project/client/src/styleCanvas.css]
│   │   │   ├── UploadFile.js [📂 extraction_target_project/client/src/UploadFile.js] -> [💡 📦 imp: react, react-icons/fa6 | 🎯 def UploadFile(props) [L5~L31] | 🎯 def upload(event) [L8~L15]]
│   │   │   │   ├── 🎯 def UploadFile() [L5-L31]
│   │   │   │   ├── 🎯 def upload() [L8-L15]
│   ├── extraction_target_project.code-workspace [📂 extraction_target_project/extraction_target_project.code-workspace]
│   ├── index.js [📂 extraction_target_project/index.js] -> [💡 📦 imp: express, http, os, path, socket.io, url | 🎯 def getAllConnectedClients(boardId) [L35~L41] | 🎯 def getLocalExternalIP() [L209~L219]]
│   │   ├── 🎯 def getAllConnectedClients() [L35-L41]
│   │   ├── 🎯 def getLocalExternalIP() [L209-L219]
│   ├── package-lock.json [📂 extraction_target_project/package-lock.json] -> [💡 📦 json_keys: 5개 포착 | 🔑 "name" [str] | 🔑 "version" [str] | 🔑 "lockfileVersion" [int] | 🔑 "requires" [bool] | 🔑 "packages" [dict]]
│   │   ├── 🔑 key "name" [L2]
│   │   ├── 🔑 key "version" [L3]
│   │   ├── 🔑 key "lockfileVersion" [L4]
│   │   ├── 🔑 key "requires" [L5]
│   │   ├── 🔑 key "packages" [L6]
│   │   │   ├── 📞 [CALLS]: node_modules/pstree.remy, bin/nodemon.js, ipaddr.js, bin/semver.js, node_modules/ipaddr.js, cli.js, bin/nodetouch.js, node_modules/socket.io, node_modules/engine.io
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
│   ├── prompt.md [📂 extraction_target_project/prompt.md]
│   ├── README.md [📂 extraction_target_project/README.md]
│   ├── start.bat [📂 extraction_target_project/start.bat]
├── oldplan/
│   ├── agent_plan1.md [📂 oldplan/agent_plan1.md]
│   ├── agent_plan2.md [📂 oldplan/agent_plan2.md]
│   ├── agent_plan3.md [📂 oldplan/agent_plan3.md]
├── prompt.md [📂 prompt.md]
├── README.md [📂 README.md]
├── run_test.py [📂 run_test.py] -> [💡 📦 imp: agent_core.plan.schemas, os, pathlib, sys, tools.multi_agent_system.agent_session | 🎯 def run_interactive_chat() [L17-49] | 🎯 def main() [L53-66]]
│   ├── 🎯 def run_interactive_chat() [L17-L49]
│   ├── 🎯 def main() [L53-L66]
│   │   ├── 📞 [CALLS]: run_interactive_chat
├── scan_debug.txt [📂 scan_debug.txt]
├── setup_architecture.bat [📂 setup_architecture.bat]
├── start.py [📂 start.py] -> [💡 📦 imp: os, pathlib, shutil, stat, subprocess, sys, time | 🎯 def get_best_python() [L33-50] | 🎯 def auto_install_dependencies() [L59-80] | 🎯 def main() [L82-201]]
│   ├── 🎯 def get_best_python() [L33-L50]
│   ├── 🎯 def auto_install_dependencies() [L59-L80]
│   │   ├── 🔗 [USED BY]: ::main
│   ├── 🎯 def main() [L82-L201]
│   │   ├── 📞 [CALLS]: auto_install_dependencies
├── System Prompt.md [📂 System Prompt.md]
├── tools/
│   ├── multi_agent_system/
│   │   ├── __init__.py [📂 tools/multi_agent_system/__init__.py]
│   │   ├── agent_code_extractor.py [📂 tools/multi_agent_system/agent_code_extractor.py] -> [💡 📦 imp: json, pathlib, re, switch, sys, traceback | 🧬 class CodeExtractor [L16-313] |     └─ def __init__(root_dir) [L22-48] |     └─ def _load_database() [L50-57] |     └─ def resolve_file_path(raw_path_str) [L59-96] |     └─ def extract_multi_slices(raw_prompt) [L98-255] |     └─ def format_as_markdown(extracted_slices) [L257-277] |     └─ def process(raw_prompt, auto_save, output_path) [L279-313]]
│   │   │   ├── 🧬 class CodeExtractor [L16-L313]
│   │   │   ├── 🎯 def __init__() [L22-L48]
│   │   │   ├── 🎯 def _load_database() [L50-L57]
│   │   │   ├── 🎯 def resolve_file_path() [L59-L96]
│   │   │   ├── 🎯 def extract_multi_slices() [L98-L255]
│   │   │   ├── 🎯 def format_as_markdown() [L257-L277]
│   │   │   ├── 🎯 def process() [L279-L313]
│   │   ├── agent_session.py [📂 tools/multi_agent_system/agent_session.py] -> [💡 📦 imp: agent_core.plan.gemini_client, google, google.genai, os, pathlib, tools.multi_agent_system.agent_code_extractor, tools.multi_agent_system.code_patcher, tools.multi_agent_system.terminal_runner | 🧬 class AgentSessionFactory [L18-91] |     └─ def __init__(root_dir) [L20-27] |     └─ def _load_codebase_map() [L29-37] |     └─ def _build_tools() [L39-54] |     └─ def create_chat_session(model_name) [L56-91]]
│   │   │     ├── 🔑 [REGISTRY]: "AgentSessionFactory"
│   │   │   ├── 🧬 class AgentSessionFactory [L18-L91]
│   │   │   ├── 🎯 def __init__() [L20-L27]
│   │   │   ├── 🎯 def _load_codebase_map() [L29-L37]
│   │   │   ├── 🎯 def _build_tools() [L39-L54]
│   │   │   ├── 🎯 def create_chat_session() [L56-L91]
│   │   ├── code_patcher.py [📂 tools/multi_agent_system/code_patcher.py] -> [💡 📦 imp: pathlib | 🧬 class CodePatcher [L9-65] |     └─ def __init__(root_dir) [L10-11] |     └─ def apply_patch(rel_path, existing_code, replacement_code) [L13-65]]
│   │   │   ├── 🧬 class CodePatcher [L9-L65]
│   │   │   ├── 🎯 def __init__() [L10-L11]
│   │   │   ├── 🎯 def apply_patch() [L13-L65]
│   │   ├── terminal_runner.py [📂 tools/multi_agent_system/terminal_runner.py] -> [💡 📦 imp: pathlib, subprocess | 🎯 def run_terminal_command(command, cwd, timeout) [L12-57]]
│   │   │   ├── 🎯 def run_terminal_command() [L12-L57]
│   ├── universal_indexer/
│   │   ├── agent_navigator.py [📂 tools/universal_indexer/agent_navigator.py] -> [💡 📦 imp: agent_code_extractor, pathlib, sys, tkinter, tools.multi_agent_system.agent_code_extractor | 🧬 class JjapCursorNavigatorGUI [L23-119] |     └─ def __init__(root, project_root) [L24-74] |     └─ def execute_slicing_pipeline() [L76-101] |     └─ def manual_export_file() [L103-119]]
│   │   │     ├── 🔑 [REGISTRY]: "JjapCursorNavigatorGUI"
│   │   │   ├── 🧬 class JjapCursorNavigatorGUI [L23-L119]
│   │   │   ├── 🎯 def __init__() [L24-L74]
│   │   │   ├── 🎯 def execute_slicing_pipeline() [L76-L101]
│   │   │   ├── 🎯 def manual_export_file() [L103-L119]
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
│   │   ├── create_ai_map.py [📂 tools/universal_indexer/create_ai_map.py] -> [💡 📦 imp: ast, config, json, os, pathlib | 🎯 def load_jjap_context() [L18-29] | 🎯 def collect_target_files() [L32-63] | 🎯 def load_registry() [L66-96] | 🎯 def load_protocols() [L99-116] | 🎯 def parse_protocols_and_registries() [L119-158] | 🎯 def load_all_symbols() [L162-183] | 🎯 def main() [L186-317] | 🎯 def generate_ai_optimized_map() [L320-321]]
│   │   │   ├── 🎯 def load_jjap_context() [L18-L29]
│   │   │   │   ├── 🔗 [USED BY]: ::main
│   │   │   ├── 🎯 def collect_target_files() [L32-L63]
│   │   │   │   ├── 🔗 [USED BY]: ::main
│   │   │   ├── 🎯 def load_registry() [L66-L96]
│   │   │   │   ├── 🔗 [USED BY]: ::parse_protocols_and_registries
│   │   │   ├── 🎯 def load_protocols() [L99-L116]
│   │   │   │   ├── 🔗 [USED BY]: ::parse_protocols_and_registries
│   │   │   ├── 🎯 def parse_protocols_and_registries() [L119-L158]
│   │   │   │   ├── 📞 [CALLS]: load_protocols, load_registry
│   │   │   │   ├── 🔗 [USED BY]: ::main
│   │   │   ├── 🎯 def load_all_symbols() [L162-L183]
│   │   │   │   ├── 🔗 [USED BY]: ::main
│   │   │   ├── 🎯 def main() [L186-L317]
│   │   │   │   ├── 📞 [CALLS]: load_all_symbols, parse_protocols_and_registries, load_jjap_context, collect_target_files
│   │   │   ├── 🎯 def generate_ai_optimized_map() [L320-L321]
│   │   │   │   ├── 📞 [CALLS]: main
│   │   ├── indexer.py [📂 tools/universal_indexer/indexer.py] -> [💡 📦 imp: collections, config, hashlib, importlib.util, json, os, pathlib, typing | 🎯 def log(message) [L22-24] | 🧬 class AdvancedIndexerV2 [L26-206] |     └─ def __init__(project_root) [L31-41] |     └─ def _auto_load_parsers() [L43-74] |     └─ def scan_project() [L78-141] |     └─ def index_file(file_path, ext) [L143-183] |     └─ def save_index_data() [L185-206]]
│   │   │     ├── 🔑 [REGISTRY]: "AdvancedIndexerV2"
│   │   │   ├── 🎯 def log() [L22-L24]
│   │   │   │   ├── 🔗 [USED BY]: tools/universal_indexer/core_parsers/java_parser.py::extract_symbols
│   │   │   ├── 🧬 class AdvancedIndexerV2 [L26-L206]
│   │   │   ├── 🎯 def __init__() [L31-L41]
│   │   │   ├── 🎯 def _auto_load_parsers() [L43-L74]
│   │   │   ├── 🎯 def scan_project() [L78-L141]
│   │   │   ├── 🎯 def index_file() [L143-L183]
│   │   │   ├── 🎯 def save_index_data() [L185-L206]
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
│   │   ├── README.md [📂 tools/universal_indexer/README.md]
│   │   ├── rule.txt [📂 tools/universal_indexer/rule.txt]
│   │   ├── switch.py [📂 tools/universal_indexer/switch.py]
│   │   ├── tree_sitter_parser.py [📂 tools/universal_indexer/tree_sitter_parser.py] -> [💡 📦 imp: collections, hashlib, pathlib, tree_sitter_languages | 🎯 def extract_symbols(file_path, project_root) [L23-178]]
│   │   │   ├── 🎯 def extract_symbols() [L23-L178]
│   │   │   │   ├── 📞 [CALLS]: traverse
│   │   ├── update_map.py [📂 tools/universal_indexer/update_map.py] -> [💡 📦 imp: json, pathlib | 🎯 def update_map() [L4-103]]
│   │   │   ├── 🎯 def update_map() [L4-L103]
