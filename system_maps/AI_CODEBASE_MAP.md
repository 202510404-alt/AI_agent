# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)

> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.
> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.

```markdown
project_root/
├── cline_tools/
│   ├── agent_navigator.py [📂 cline_tools/agent_navigator.py] -> [💡 📦 imp: json, pathlib.Path, re, sys, tkinter, tkinter.filedialog | 🧬 class SemanticNavigator [L11-118] |    └─ def __init__(root_dir) [L12-16] |    └─ def _load_database() [L18-25] |    └─ def extract_multi_slices(raw_prompt) [L27-118] | 🧬 class JjapCursorNavigatorGUI [L123-244] |    └─ def __init__(root, project_root) [L124-173] |    └─ def execute_slicing_pipeline() [L175-225] |    └─ def manual_export_file() [L227-244]]
│   │     ├── 🔑 [REGISTRY]: "SemanticNavigator"
│   │     ├── 🔑 [REGISTRY]: "JjapCursorNavigatorGUI"
│   ├── context_builder.py [📂 cline_tools/context_builder.py] -> [💡 📦 imp: os, pathlib.Path | 🧬 class ContextBuilder [L13-106] |    └─ def __init__(project_root) [L16-18] |    └─ def read_and_clean_file(relative_path) [L20-77] |    └─ def assemble_ai_prompt(user_query, affected_files) [L79-106]]
│   │     ├── 🔑 [REGISTRY]: "ContextBuilder"
│   ├── create_ai_map.py [📂 cline_tools/create_ai_map.py] -> [💡 📦 imp: ast, json, os, pathlib.Path | 🎯 def parse_python_file(file_path) [L38-99] | 🎯 def collect_target_files() [L102-130] | 🎯 def load_registry() [L133-147] | 🎯 def load_protocols() [L150-165] | 🎯 def main() [L168-236] | 🎯 def generate_ai_optimized_map() [L243-245]]
│   ├── indexer.py [📂 cline_tools/indexer.py] -> [💡 📦 imp: ast, hashlib, json, os, pathlib.Path, typing.Any | 🧬 class AdvancedIndexerV2 [L22-227] |    └─ def __init__(project_root) [L31-39] |    └─ def _get_sha256(content) [L41-42] |    └─ def _extract_skeleton(content) [L44-60] |    └─ def parse_protocols_and_registries(content, rel_path_str) [L62-95] |    └─ def index_file(file_path) [L97-168] |    └─ def scan_project() [L170-227]]
│   │     ├── 🔑 [REGISTRY]: "AdvancedIndexerV2"
│   ├── jjap_lookup.py [📂 cline_tools/jjap_lookup.py] -> [💡 📦 imp: argparse, json, pathlib.Path, sys | 🎯 def load_json(file_path) [L9-14] | 🎯 def lookup_symbol(symbol_name) [L16-43] | 🎯 def show_skeleton(file_path) [L45-61]]
│   ├── jjap_retriever.py [📂 cline_tools/jjap_retriever.py] -> [💡 📦 imp: json, os, pathlib.Path, typing.Any, typing.Dict, typing.List | 🧬 class JjapRetriever [L9-129] |    └─ def __init__(project_root) [L16-21] |    └─ def _load_symbols() [L23-37] |    └─ def retrieve_symbol(query) [L39-98] |    └─ def _find_best_match(query) [L100-117] |    └─ def _safe_truncate(text) [L119-129] | 🎯 def main() [L132-140]]
│   │     ├── 🔑 [REGISTRY]: "JjapRetriever"
│   ├── jjap_watcher.py [📂 cline_tools/jjap_watcher.py] -> [💡 📦 imp: importlib.util, os, pathlib.Path, sys, time | 🎯 def import_file_directly(module_name, file_path) [L20-28] | 🎯 def run_pipeline() [L30-73] | 🧬 class CodeChangeHandler [L76-99] |    └─ def __init__() [L77-79] |    └─ def dispatch(event) [L81-99] | 🎯 def main() [L101-127]]
│   │     ├── 🔑 [REGISTRY]: "CodeChangeHandler"
│   ├── switch.py [📂 cline_tools/switch.py]
│   ├── update_map.py [📂 cline_tools/update_map.py] -> [💡 📦 imp: json, pathlib.Path | 🎯 def update_map() [L4-88]]
├── start.py [📂 start.py] -> [💡 📦 imp: os, pathlib.Path, shutil, stat, subprocess, sys | 🎯 def get_best_python() [L32-48] | 🎯 def auto_install_dependencies() [L57-78] | 🎯 def main() [L80-196]]
```
