# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)

> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.
> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.

```markdown
project_root/
├── agent_core/
│   ├── __init__.py [📂 agent_core/__init__.py]
│   ├── execution/
│   │   ├── __init__.py [📂 agent_core/execution/__init__.py]
│   ├── memory/
│   │   ├── __init__.py [📂 agent_core/memory/__init__.py]
│   ├── plan/
│   │   ├── __init__.py [📂 agent_core/plan/__init__.py]
│   │   ├── gemini_client.py [📂 agent_core/plan/gemini_client.py]
│   │   ├── planner.py [📂 agent_core/plan/planner.py]
│   │   ├── prompt_builder.py [📂 agent_core/plan/prompt_builder.py]
│   │   ├── schemas.py [📂 agent_core/plan/schemas.py]
│   ├── validation/
│   │   ├── __init__.py [📂 agent_core/validation/__init__.py]
├── start.py [📂 start.py] -> [💡 📦 imp: os, pathlib.Path, shutil, stat, subprocess, sys | 🎯 def _handle_remove_readonly(func, path, exc_info) [L51-57] | 🎯 def migrate_legacy_cline_tools_directory() [L60-116] | 🎯 def get_best_python() [L124-140] | 🎯 def auto_install_dependencies() [L149-170] | 🎯 def main() [L172-293]]
├── tools/
│   ├── python_agent_tools/
│   │   ├── agent_navigator.py [📂 tools/python_agent_tools/agent_navigator.py] -> [💡 📦 imp: json, pathlib.Path, re, sys, tkinter, tkinter.filedialog | 🧬 class SemanticNavigator [L11-341] |    └─ def __init__(root_dir) [L12-16] |    └─ def _load_database() [L18-25] |    └─ def extract_multi_slices(raw_prompt) [L30-341] | 🧬 class JjapCursorNavigatorGUI [L346-467] |    └─ def __init__(root, project_root) [L347-396] |    └─ def execute_slicing_pipeline() [L398-448] |    └─ def manual_export_file() [L450-467]]
│   │   ├── context_builder.py [📂 tools/python_agent_tools/context_builder.py] -> [💡 📦 imp: os, pathlib.Path | 🧬 class ContextBuilder [L13-106] |    └─ def __init__(project_root) [L16-18] |    └─ def read_and_clean_file(relative_path) [L20-77] |    └─ def assemble_ai_prompt(user_query, affected_files) [L79-106]]
│   │   ├── create_ai_map.py [📂 tools/python_agent_tools/create_ai_map.py] -> [💡 📦 imp: ast, json, os, pathlib.Path | 🎯 def parse_python_file(file_path) [L41-102] | 🎯 def collect_target_files() [L105-133] | 🎯 def load_registry() [L136-150] | 🎯 def load_protocols() [L153-168] | 🎯 def main() [L171-239] | 🎯 def generate_ai_optimized_map() [L246-248]]
│   │   ├── indexer.py [📂 tools/python_agent_tools/indexer.py] -> [💡 📦 imp: ast, hashlib, json, os, pathlib.Path, typing.Any | 🧬 class AdvancedIndexerV2 [L22-227] |    └─ def __init__(project_root) [L31-39] |    └─ def _get_sha256(content) [L41-42] |    └─ def _extract_skeleton(content) [L44-60] |    └─ def parse_protocols_and_registries(content, rel_path_str) [L62-95] |    └─ def index_file(file_path) [L97-168] |    └─ def scan_project() [L170-227]]
│   │   ├── jjap_lookup.py [📂 tools/python_agent_tools/jjap_lookup.py] -> [💡 📦 imp: argparse, json, pathlib.Path, sys | 🎯 def load_json(file_path) [L9-14] | 🎯 def lookup_symbol(symbol_name) [L16-43] | 🎯 def show_skeleton(file_path) [L45-61]]
│   │   ├── jjap_retriever.py [📂 tools/python_agent_tools/jjap_retriever.py] -> [💡 📦 imp: json, os, pathlib.Path, typing.Any, typing.Dict, typing.List | 🧬 class JjapRetriever [L9-129] |    └─ def __init__(project_root) [L16-21] |    └─ def _load_symbols() [L23-37] |    └─ def retrieve_symbol(query) [L39-98] |    └─ def _find_best_match(query) [L100-117] |    └─ def _safe_truncate(text) [L119-129] | 🎯 def main() [L132-140]]
│   │   ├── jjap_watcher.py [📂 tools/python_agent_tools/jjap_watcher.py] -> [💡 📦 imp: importlib.util, os, pathlib.Path, sys, time | 🎯 def import_file_directly(module_name, file_path) [L20-28] | 🎯 def run_pipeline() [L30-73] | 🧬 class CodeChangeHandler [L76-99] |    └─ def __init__() [L77-79] |    └─ def dispatch(event) [L81-99] | 🎯 def main() [L101-127]]
│   │   ├── switch.py [📂 tools/python_agent_tools/switch.py]
│   │   ├── update_map.py [📂 tools/python_agent_tools/update_map.py] -> [💡 📦 imp: json, pathlib.Path | 🎯 def update_map() [L4-88]]
```
