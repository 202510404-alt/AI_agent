# 🏗️ CUSTOM TARGETED AI-OPTIMIZED CODEBASE MAP
> **[추출 범위 지정]** Target Paths: `['agent_core/plan', 'tools/multi_agent_system']`
```markdown
project_root/
├── agent_core/
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
│   │   │   │   ├── 📞 [CALLS]: SymbolRef, log_debug
│   │   ├── test_ai_chat.py [📂 agent_core/plan/test_ai_chat.py] -> [💡 📦 imp: agent_core.plan.gemini_client, agent_core.plan.prompt_builder, google, google.genai, json, os, pathlib, sys, tools.multi_agent_system.agent_code_extractor | 🎯 def extract_code_slice(file_and_line) [L32-43] | 🎯 def run_interactive_chat() [L49-104]]
│   │   │   ├── 🎯 def extract_code_slice() [L32-L43]
│   │   │   ├── 🎯 def run_interactive_chat() [L49-L104]
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
│   │   ├── agent_map_extractor.py [📂 tools/multi_agent_system/agent_map_extractor.py] -> [💡 📦 imp: json, os, pathlib, typing | 🧬 class AgentMapExtractor [L37-258] |     └─ def __init__(project_root) [L40-41] |     └─ def _load_jjap_context() [L43-50] |     └─ def _load_all_symbols() [L52-70] |     └─ def _load_registry_and_protocols() [L72-109] |     └─ def collect_files_in_targets(target_paths, exclude_paths) [L111-146] |     └─ def generate_custom_map(target_paths, exclude_paths, save_to_file) [L148-258] | 🎯 def extract_targeted_ai_map(target_paths, exclude_paths) [L262-264]]
│   │   │     ├── 🔑 [REGISTRY]: "AgentMapExtractor"
│   │   │   ├── 🧬 class AgentMapExtractor [L37-L258]
│   │   │   │   ├── 🔗 [USED BY]: ::extract_targeted_ai_map
│   │   │   ├── 🎯 def __init__() [L40-L41]
│   │   │   ├── 🎯 def _load_jjap_context() [L43-L50]
│   │   │   ├── 🎯 def _load_all_symbols() [L52-L70]
│   │   │   ├── 🎯 def _load_registry_and_protocols() [L72-L109]
│   │   │   ├── 🎯 def collect_files_in_targets() [L111-L146]
│   │   │   ├── 🎯 def generate_custom_map() [L148-L258]
│   │   │   ├── 🎯 def extract_targeted_ai_map() [L262-L264]
│   │   │   │   ├── 📞 [CALLS]: AgentMapExtractor
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
```
