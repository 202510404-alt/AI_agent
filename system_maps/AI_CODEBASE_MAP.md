# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)

> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.
> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.

```markdown
project_root/
├── .gitignore [📂 .gitignore]
├── System Prompt.md [📂 System Prompt.md]
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
├── agent_plan.md [📂 agent_plan.md]
├── oldplan/
│   ├── agent_plan1.md [📂 oldplan/agent_plan1.md]
│   ├── agent_plan2.md [📂 oldplan/agent_plan2.md]
│   ├── agent_plan3.md [📂 oldplan/agent_plan3.md]
├── prompt.md [📂 prompt.md]
├── start.py [📂 start.py] -> [💡 📦 imp: os, pathlib.Path, shutil, stat, subprocess, sys | 🎯 def get_best_python() [L34-50] | 🎯 def auto_install_dependencies() [L59-80] | 🎯 def main() [L82-202]]
├── tools/
│   ├── universal_indexer/
│   │   ├── README.md [📂 tools/universal_indexer/README.md]
│   │   ├── agent_navigator.py [📂 tools/universal_indexer/agent_navigator.py] -> [💡 📦 imp: json, pathlib.Path, re, sys, tkinter, tkinter.filedialog | 🧬 class SemanticNavigator [L11-208] |    └─ def __init__(root_dir) [L12-16] |    └─ def _load_database() [L18-25] |    └─ def extract_multi_slices(raw_prompt) [L30-208] | 🧬 class JjapCursorNavigatorGUI [L213-339] |    └─ def __init__(root, project_root) [L214-263] |    └─ def execute_slicing_pipeline() [L265-320] |    └─ def manual_export_file() [L322-339]]
│   │   ├── context_builder.py [📂 tools/universal_indexer/context_builder.py] -> [💡 📦 imp: os, pathlib.Path | 🧬 class ContextBuilder [L13-107] |    └─ def __init__(project_root) [L16-18] |    └─ def read_and_clean_file(relative_path) [L20-78] |    └─ def assemble_ai_prompt(user_query, affected_files) [L80-107]]
│   │   ├── core_parsers/
│   │   │   ├── __init__.py [📂 tools/universal_indexer/core_parsers/__init__.py]
│   │   │   ├── cs_parser.py [📂 tools/universal_indexer/core_parsers/cs_parser.py]
│   │   │   ├── js_parser.py [📂 tools/universal_indexer/core_parsers/js_parser.py]
│   │   │   ├── json_parser.py [📂 tools/universal_indexer/core_parsers/json_parser.py] -> [💡 📦 imp: hashlib, json, pathlib.Path | 🎯 def extract_symbols(file_path, project_root) [L5-97]]
│   │   │   ├── py_parser.py [📂 tools/universal_indexer/core_parsers/py_parser.py] -> [💡 📦 imp: ast, hashlib, pathlib.Path | 🎯 def extract_symbols(file_path, project_root) [L5-158]]
│   │   ├── create_ai_map.py [📂 tools/universal_indexer/create_ai_map.py] -> [💡 📦 imp: ast, json, os, pathlib.Path | 🎯 def parse_python_file(file_path) [L37-98] | 🎯 def collect_target_files() [L101-130] | 🎯 def load_registry() [L133-170] | 🎯 def load_protocols() [L173-195] | 🎯 def parse_protocols_and_registries() [L198-240] | 🎯 def main() [L243-316] | 🎯 def generate_ai_optimized_map() [L323-325]]
│   │   ├── indexer.py [📂 tools/universal_indexer/indexer.py] -> [💡 📦 imp: ast, hashlib, importlib.util, json, os, pathlib.Path | 🧬 class AdvancedIndexerV2 [L27-277] |    └─ def __init__(project_root) [L36-49] |    └─ def _auto_load_parsers() [L51-106] |    └─ def _get_sha256(content) [L108-109] |    └─ def _extract_skeleton(content) [L111-127] |    └─ def parse_protocols_and_registries(content, rel_path_str) [L129-162] |    └─ def index_file(file_path) [L164-196] |    └─ def scan_project() [L198-277]]
│   │   ├── jjap_lookup.py [📂 tools/universal_indexer/jjap_lookup.py] -> [💡 📦 imp: argparse, json, pathlib.Path, sys | 🎯 def load_json(file_path) [L17-22] | 🎯 def lookup_symbol(symbol_name) [L24-51] | 🎯 def show_skeleton(file_path) [L53-69]]
│   │   ├── jjap_retriever.py [📂 tools/universal_indexer/jjap_retriever.py] -> [💡 📦 imp: json, os, pathlib.Path, typing.Any, typing.Dict, typing.List | 🧬 class JjapRetriever [L9-129] |    └─ def __init__(project_root) [L16-21] |    └─ def _load_symbols() [L23-37] |    └─ def retrieve_symbol(query) [L39-98] |    └─ def _find_best_match(query) [L100-117] |    └─ def _safe_truncate(text) [L119-129] | 🎯 def main() [L132-140]]
│   │   ├── jjap_watcher.py [📂 tools/universal_indexer/jjap_watcher.py] -> [💡 📦 imp: importlib.util, os, pathlib.Path, sys, time | 🎯 def import_file_directly(module_name, file_path) [L25-33] | 🎯 def run_pipeline() [L35-78] | 🧬 class CodeChangeHandler [L81-104] |    └─ def __init__() [L82-84] |    └─ def dispatch(event) [L86-104] | 🎯 def main() [L106-132]]
│   │   ├── rule.txt [📂 tools/universal_indexer/rule.txt]
│   │   ├── switch.py [📂 tools/universal_indexer/switch.py]
│   │   ├── update_map.py [📂 tools/universal_indexer/update_map.py] -> [💡 📦 imp: json, pathlib.Path | 🎯 def update_map() [L4-94]]
```
