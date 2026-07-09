# 🏗️ 짭커서 프로젝트 CODEBASE MAP

현재 인덱싱된 총 파일 수: **33개**

## 🗂️ [Module Index]
- `System Prompt.md`
- `a`
- `agent_core/__init__.py`
- `agent_core/execution/__init__.py`
- `agent_core/memory/__init__.py`
- `agent_core/plan/__init__.py`
- `agent_core/plan/gemini_client.py`
- `agent_core/plan/planner.py`
- `agent_core/plan/prompt_builder.py`
- `agent_core/plan/schemas.py`
- `agent_core/validation/__init__.py`
- `agent_plan.md`
- `b`
- `oldplan/agent_plan1.md`
- `oldplan/agent_plan2.md`
- `oldplan/agent_plan3.md`
- `prompt.md`
- `tools/universal_indexer/README.md`
- `tools/universal_indexer/agent_navigator.py`
- `tools/universal_indexer/context_builder.py`
- `tools/universal_indexer/core_parsers/__init__.py`
- `tools/universal_indexer/core_parsers/cs_parser.py`
- `tools/universal_indexer/core_parsers/js_parser.py`
- `tools/universal_indexer/core_parsers/json_parser.py`
- `tools/universal_indexer/core_parsers/py_parser.py`
- `tools/universal_indexer/create_ai_map.py`
- `tools/universal_indexer/indexer.py`
- `tools/universal_indexer/jjap_lookup.py`
- `tools/universal_indexer/jjap_retriever.py`
- `tools/universal_indexer/jjap_watcher.py`
- `tools/universal_indexer/rule.txt`
- `tools/universal_indexer/switch.py`
- `tools/universal_indexer/update_map.py`

## 💀 [Skeleton & Dependency 명세서]
### 📄 System Prompt.md
#### 🧱 Code Skeleton:
```python
Non-Python File (.MD)
```

--------------------------------------------------

### 📄 a
#### 🧱 Code Skeleton:
```python
Non-Python File ()
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
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/plan/planner.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/plan/prompt_builder.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/plan/schemas.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/validation/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_plan.md
#### 🧱 Code Skeleton:
```python
Non-Python File (.MD)
```

--------------------------------------------------

### 📄 b
#### 🧱 Code Skeleton:
```python
Non-Python File ()
```

--------------------------------------------------

### 📄 oldplan/agent_plan1.md
#### 🧱 Code Skeleton:
```python
Non-Python File (.MD)
```

--------------------------------------------------

### 📄 oldplan/agent_plan2.md
#### 🧱 Code Skeleton:
```python
Non-Python File (.MD)
```

--------------------------------------------------

### 📄 oldplan/agent_plan3.md
#### 🧱 Code Skeleton:
```python
Non-Python File (.MD)
```

--------------------------------------------------

### 📄 prompt.md
#### 🧱 Code Skeleton:
```python
Non-Python File (.MD)
```

--------------------------------------------------

### 📄 tools/universal_indexer/README.md
#### 🧱 Code Skeleton:
```python
Non-Python File (.MD)
```

--------------------------------------------------

### 📄 tools/universal_indexer/agent_navigator.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[CLASS]** `SemanticNavigator` (Line: 11~208)
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/agent_navigator.py::JjapCursorNavigatorGUI.__init__`
- **[METHOD]** `__init__` (Line: 12~16)
  - 🔗 *Calls (호출하는 것)*: `_load_database`
- **[METHOD]** `_load_database` (Line: 18~25)
  - 🔗 *Calls (호출하는 것)*: `exists, load, open`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/agent_navigator.py::SemanticNavigator.__init__`
- **[METHOD]** `extract_multi_slices` (Line: 30~208)
  - 🔗 *Calls (호출하는 것)*: `print_exc, any, append, open, readlines, set, int, findall, replace, min, exists, strip, split, print, max, join, get, repr, endswith, list, len`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/agent_navigator.py::JjapCursorNavigatorGUI.execute_slicing_pipeline`
- **[CLASS]** `JjapCursorNavigatorGUI` (Line: 213~339)
- **[METHOD]** `__init__` (Line: 214~263)
  - 🔗 *Calls (호출하는 것)*: `geometry, Text, title, insert, Button, SemanticNavigator, pack, Label, Frame`
- **[METHOD]** `execute_slicing_pipeline` (Line: 265~320)
  - 🔗 *Calls (호출하는 것)*: `startswith, showerror, extract_multi_slices, write, join, strip, insert, delete, get, append, config, showwarning, open, rstrip`
- **[METHOD]** `manual_export_file` (Line: 322~339)
  - 🔗 *Calls (호출하는 것)*: `showerror, showinfo, write, str, asksaveasfilename, open`

#### 🧱 Code Skeleton:
```python
class SemanticNavigator:
    def __init__(...):
        ...
    def _load_database(...):
        ...
    def extract_multi_slices(...):
        ...
class JjapCursorNavigatorGUI:
    def __init__(...):
        ...
    def execute_slicing_pipeline(...):
        ...
    def manual_export_file(...):
        ...
```

--------------------------------------------------

### 📄 tools/universal_indexer/context_builder.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[CLASS]** `ContextBuilder` (Line: 13~107)
- **[METHOD]** `__init__` (Line: 16~18)
  - 🔗 *Calls (호출하는 것)*: `Path`
- **[METHOD]** `read_and_clean_file` (Line: 20~78)
  - 🔗 *Calls (호출하는 것)*: `FileNotFoundError, startswith, join, exists, strip, len, append, open, enumerate, readlines, split, endswith`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/context_builder.py::ContextBuilder.assemble_ai_prompt`
- **[METHOD]** `assemble_ai_prompt` (Line: 80~107)
  - 🔗 *Calls (호출하는 것)*: `join, read_and_clean_file, append, str`

#### 🧱 Code Skeleton:
```python
class ContextBuilder:
    def __init__(...):
        ...
    def read_and_clean_file(...):
        ...
    def assemble_ai_prompt(...):
        ...
```

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/cs_parser.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/js_parser.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/json_parser.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/py_parser.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/create_ai_map.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[FUNCTION]** `parse_python_file` (Line: 37~98)
  - 🔗 *Calls (호출하는 것)*: `getattr, sorted, parse, extend, isinstance, join, read, append, remove, open, list, set`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/create_ai_map.py::main`
- **[FUNCTION]** `collect_target_files` (Line: 101~130)
  - 🔗 *Calls (호출하는 것)*: `print, replace, sorted, walk, exists, any, append, Path`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/create_ai_map.py::main`
- **[FUNCTION]** `load_registry` (Line: 133~147)
  - 🔗 *Calls (호출하는 것)*: `print, setdefault, exists, get, items, append, open, rpartition, as_posix, load, Path`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/create_ai_map.py::main`
- **[FUNCTION]** `load_protocols` (Line: 150~165)
  - 🔗 *Calls (호출하는 것)*: `print, setdefault, exists, get, items, append, open, as_posix, load, Path`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/create_ai_map.py::main`
- **[FUNCTION]** `main` (Line: 168~241)
  - 🔗 *Calls (호출하는 것)*: `write, open, load_registry, set, unlink, add, items, range, as_posix, mkdir, replace, relative_to, exists, print, collect_target_files, join, parse_python_file, endswith, len, load_protocols, Path`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/create_ai_map.py::generate_ai_optimized_map`
- **[FUNCTION]** `generate_ai_optimized_map` (Line: 248~250)
  - 🔗 *Calls (호출하는 것)*: `main`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_watcher.py::run_pipeline`

#### 🧱 Code Skeleton:
```python
def parse_python_file(...):
    ...
def collect_target_files(...):
    ...
def load_registry(...):
    ...
def load_protocols(...):
    ...
def main(...):
    ...
def generate_ai_optimized_map(...):
    ...
```

--------------------------------------------------

### 📄 tools/universal_indexer/indexer.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[CLASS]** `AdvancedIndexerV2` (Line: 26~311)
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_watcher.py::run_pipeline`
- **[METHOD]** `__init__` (Line: 35~43)
- **[METHOD]** `_get_sha256` (Line: 45~46)
  - 🔗 *Calls (호출하는 것)*: `hexdigest, sha256, encode`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/indexer.py::AdvancedIndexerV2.index_file`
- **[METHOD]** `_extract_skeleton` (Line: 48~64)
  - 🔗 *Calls (호출하는 것)*: `join, isinstance, append, parse`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/indexer.py::AdvancedIndexerV2.index_file`
- **[METHOD]** `parse_protocols_and_registries` (Line: 66~99)
  - 🔗 *Calls (호출하는 것)*: `isinstance, lower, type, parse`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/indexer.py::AdvancedIndexerV2.index_file`
- **[METHOD]** `index_file` (Line: 101~230)
  - 🔗 *Calls (호출하는 것)*: `_extract_skeleton, isinstance, stat, append, open, set, int, getattr, parse_protocols_and_registries, parse, walk, read, items, lower, as_posix, relative_to, upper, type, print, str, _get_sha256, list, keys, len, load`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/indexer.py::AdvancedIndexerV2.scan_project`
- **[METHOD]** `scan_project` (Line: 232~311)
  - 🔗 *Calls (호출하는 것)*: `print, replace, sorted, dump, walk, exists, get, any, append, makedirs, open, list, set, as_posix, index_file, Path`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_watcher.py::run_pipeline`

#### 🧱 Code Skeleton:
```python
class AdvancedIndexerV2:
    def __init__(...):
        ...
    def _get_sha256(...):
        ...
    def _extract_skeleton(...):
        ...
    def parse_protocols_and_registries(...):
        ...
    def index_file(...):
        ...
    def scan_project(...):
        ...
```

--------------------------------------------------

### 📄 tools/universal_indexer/jjap_lookup.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[FUNCTION]** `load_json` (Line: 17~22)
  - 🔗 *Calls (호출하는 것)*: `print, exists, exit, open, load`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_lookup.py::lookup_symbol, tools/universal_indexer/jjap_lookup.py::show_skeleton`
- **[FUNCTION]** `lookup_symbol` (Line: 24~51)
  - 🔗 *Calls (호출하는 것)*: `print, load_json, upper, get, len, lower`
- **[FUNCTION]** `show_skeleton` (Line: 53~69)
  - 🔗 *Calls (호출하는 것)*: `print, get, keys, load_json`

#### 🧱 Code Skeleton:
```python
def load_json(...):
    ...
def lookup_symbol(...):
    ...
def show_skeleton(...):
    ...
```

--------------------------------------------------

### 📄 tools/universal_indexer/jjap_retriever.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[CLASS]** `JjapRetriever` (Line: 9~129)
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_retriever.py::main`
- **[METHOD]** `__init__` (Line: 16~21)
  - 🔗 *Calls (호출하는 것)*: `_load_symbols`
- **[METHOD]** `_load_symbols` (Line: 23~37)
  - 🔗 *Calls (호출하는 것)*: `print, exists, get, open, len, load`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_retriever.py::JjapRetriever.__init__`
- **[METHOD]** `retrieve_symbol` (Line: 39~98)
  - 🔗 *Calls (호출하는 것)*: `print, startswith, max, min, extend, _find_best_match, exists, strip, get, join, append, open, readlines, next, len, rstrip, _safe_truncate`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_retriever.py::main`
- **[METHOD]** `_find_best_match` (Line: 100~117)
  - 🔗 *Calls (호출하는 것)*: `print, lower, get`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_retriever.py::JjapRetriever.retrieve_symbol`
- **[METHOD]** `_safe_truncate` (Line: 119~129)
  - 🔗 *Calls (호출하는 것)*: `print, join, splitlines, append, len`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_retriever.py::JjapRetriever.retrieve_symbol`
- **[FUNCTION]** `main` (Line: 132~140)
  - 🔗 *Calls (호출하는 것)*: `print, cwd, retrieve_symbol, len, JjapRetriever`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/create_ai_map.py::generate_ai_optimized_map`

#### 🧱 Code Skeleton:
```python
class JjapRetriever:
    def __init__(...):
        ...
    def _load_symbols(...):
        ...
    def retrieve_symbol(...):
        ...
    def _find_best_match(...):
        ...
    def _safe_truncate(...):
        ...
def main(...):
    ...
```

--------------------------------------------------

### 📄 tools/universal_indexer/jjap_watcher.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[FUNCTION]** `import_file_directly` (Line: 25~33)
  - 🔗 *Calls (호출하는 것)*: `str, ImportError, module_from_spec, exec_module, spec_from_file_location`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_watcher.py::run_pipeline`
- **[FUNCTION]** `run_pipeline` (Line: 35~78)
  - 🔗 *Calls (호출하는 것)*: `print, import_file_directly, print_exc, get, scan_project, generate_ai_optimized_map, AdvancedIndexerV2, update_map`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_watcher.py::CodeChangeHandler.dispatch, tools/universal_indexer/jjap_watcher.py::main`
- **[CLASS]** `CodeChangeHandler` (Line: 81~104)
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_watcher.py::main`
- **[METHOD]** `__init__` (Line: 82~84)
- **[METHOD]** `dispatch` (Line: 86~104)
  - 🔗 *Calls (호출하는 것)*: `print, any, run_pipeline, as_posix, time, Path`
- **[FUNCTION]** `main` (Line: 106~132)
  - 🔗 *Calls (호출하는 것)*: `print, stop, str, CodeChangeHandler, join, sleep, schedule, run_pipeline, start, Observer`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/create_ai_map.py::generate_ai_optimized_map`

#### 🧱 Code Skeleton:
```python
def import_file_directly(...):
    ...
def run_pipeline(...):
    ...
class CodeChangeHandler:
    def __init__(...):
        ...
    def dispatch(...):
        ...
def main(...):
    ...
```

--------------------------------------------------

### 📄 tools/universal_indexer/rule.txt
#### 🧱 Code Skeleton:
```python
Non-Python File (.TXT)
```

--------------------------------------------------

### 📄 tools/universal_indexer/switch.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/update_map.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[FUNCTION]** `update_map` (Line: 4~94)
  - 🔗 *Calls (호출하는 것)*: `print, write, resolve, sorted, join, exists, strip, get, any, items, append, upper, open, keys, len, load, Path`
  - 🎯 *Used By (나를 부르는 곳)*: `tools/universal_indexer/jjap_watcher.py::run_pipeline`

#### 🧱 Code Skeleton:
```python
def update_map(...):
    ...
```

--------------------------------------------------

