# 🏗️ 짭커서 프로젝트 CODEBASE MAP

현재 인덱싱된 총 파일 수: **11개**

## 🗂️ [Module Index]
- `python_agent_tools/README.md`
- `python_agent_tools/agent_navigator.py`
- `python_agent_tools/context_builder.py`
- `python_agent_tools/create_ai_map.py`
- `python_agent_tools/indexer.py`
- `python_agent_tools/jjap_lookup.py`
- `python_agent_tools/jjap_retriever.py`
- `python_agent_tools/jjap_watcher.py`
- `python_agent_tools/rule.txt`
- `python_agent_tools/switch.py`
- `python_agent_tools/update_map.py`

## 💀 [Skeleton & Dependency 명세서]
### 📄 python_agent_tools/README.md
#### 🧱 Code Skeleton:
```python
Non-Python File (.MD)
```

--------------------------------------------------

### 📄 python_agent_tools/agent_navigator.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[CLASS]** `SemanticNavigator` (Line: 11~208)
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/agent_navigator.py::JjapCursorNavigatorGUI.__init__`
- **[METHOD]** `__init__` (Line: 12~16)
  - 🔗 *Calls (호출하는 것)*: `_load_database`
- **[METHOD]** `_load_database` (Line: 18~25)
  - 🔗 *Calls (호출하는 것)*: `open, exists, load`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/agent_navigator.py::SemanticNavigator.__init__`
- **[METHOD]** `extract_multi_slices` (Line: 30~208)
  - 🔗 *Calls (호출하는 것)*: `len, split, strip, open, int, print_exc, join, replace, get, max, list, readlines, endswith, any, repr, append, set, min, exists, print, findall`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/agent_navigator.py::JjapCursorNavigatorGUI.execute_slicing_pipeline`
- **[CLASS]** `JjapCursorNavigatorGUI` (Line: 213~339)
- **[METHOD]** `__init__` (Line: 214~263)
  - 🔗 *Calls (호출하는 것)*: `Frame, insert, title, Button, Label, SemanticNavigator, pack, Text, geometry`
- **[METHOD]** `execute_slicing_pipeline` (Line: 265~320)
  - 🔗 *Calls (호출하는 것)*: `insert, config, rstrip, startswith, strip, delete, join, open, append, showerror, extract_multi_slices, get, write, showwarning`
- **[METHOD]** `manual_export_file` (Line: 322~339)
  - 🔗 *Calls (호출하는 것)*: `asksaveasfilename, showerror, open, showinfo, str, write`

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

### 📄 python_agent_tools/context_builder.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[CLASS]** `ContextBuilder` (Line: 13~107)
- **[METHOD]** `__init__` (Line: 16~18)
  - 🔗 *Calls (호출하는 것)*: `Path`
- **[METHOD]** `read_and_clean_file` (Line: 20~78)
  - 🔗 *Calls (호출하는 것)*: `len, split, startswith, readlines, strip, endswith, join, open, append, enumerate, exists, FileNotFoundError`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/context_builder.py::ContextBuilder.assemble_ai_prompt`
- **[METHOD]** `assemble_ai_prompt` (Line: 80~107)
  - 🔗 *Calls (호출하는 것)*: `join, str, append, read_and_clean_file`

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

### 📄 python_agent_tools/create_ai_map.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[FUNCTION]** `parse_python_file` (Line: 41~102)
  - 🔗 *Calls (호출하는 것)*: `sorted, parse, isinstance, getattr, list, remove, read, open, extend, join, append, set`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/create_ai_map.py::main`
- **[FUNCTION]** `collect_target_files` (Line: 105~134)
  - 🔗 *Calls (호출하는 것)*: `sorted, Path, any, append, replace, exists, print, walk`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/create_ai_map.py::main`
- **[FUNCTION]** `load_registry` (Line: 137~151)
  - 🔗 *Calls (호출하는 것)*: `as_posix, load, Path, open, rpartition, append, items, exists, get, print, setdefault`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/create_ai_map.py::main`
- **[FUNCTION]** `load_protocols` (Line: 154~169)
  - 🔗 *Calls (호출하는 것)*: `as_posix, load, Path, open, append, items, exists, get, print, setdefault`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/create_ai_map.py::main`
- **[FUNCTION]** `main` (Line: 172~245)
  - 🔗 *Calls (호출하는 것)*: `len, load_registry, open, items, unlink, write, Path, mkdir, join, parse_python_file, replace, endswith, set, exists, print, as_posix, load_protocols, range, collect_target_files, add, relative_to`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/create_ai_map.py::generate_ai_optimized_map`
- **[FUNCTION]** `generate_ai_optimized_map` (Line: 252~254)
  - 🔗 *Calls (호출하는 것)*: `main`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_watcher.py::run_pipeline`

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

### 📄 python_agent_tools/indexer.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[CLASS]** `AdvancedIndexerV2` (Line: 25~310)
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_watcher.py::run_pipeline`
- **[METHOD]** `__init__` (Line: 34~42)
- **[METHOD]** `_get_sha256` (Line: 44~45)
  - 🔗 *Calls (호출하는 것)*: `hexdigest, encode, sha256`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/indexer.py::AdvancedIndexerV2.index_file`
- **[METHOD]** `_extract_skeleton` (Line: 47~63)
  - 🔗 *Calls (호출하는 것)*: `join, append, parse, isinstance`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/indexer.py::AdvancedIndexerV2.index_file`
- **[METHOD]** `parse_protocols_and_registries` (Line: 65~98)
  - 🔗 *Calls (호출하는 것)*: `parse, lower, isinstance, type`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/indexer.py::AdvancedIndexerV2.index_file`
- **[METHOD]** `index_file` (Line: 100~229)
  - 🔗 *Calls (호출하는 것)*: `parse, isinstance, len, open, items, type, keys, int, read, load, _get_sha256, list, upper, append, set, print, walk, parse_protocols_and_registries, as_posix, stat, getattr, relative_to, str, lower, _extract_skeleton`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/indexer.py::AdvancedIndexerV2.scan_project`
- **[METHOD]** `scan_project` (Line: 231~310)
  - 🔗 *Calls (호출하는 것)*: `sorted, as_posix, Path, list, makedirs, dump, open, any, append, set, replace, exists, get, print, index_file, walk`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_watcher.py::run_pipeline`

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

### 📄 python_agent_tools/jjap_lookup.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[FUNCTION]** `load_json` (Line: 9~14)
  - 🔗 *Calls (호출하는 것)*: `load, exit, open, exists, print`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_lookup.py::lookup_symbol, python_agent_tools/jjap_lookup.py::show_skeleton`
- **[FUNCTION]** `lookup_symbol` (Line: 16~43)
  - 🔗 *Calls (호출하는 것)*: `len, upper, print, get, load_json, lower`
- **[FUNCTION]** `show_skeleton` (Line: 45~61)
  - 🔗 *Calls (호출하는 것)*: `keys, get, load_json, print`

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

### 📄 python_agent_tools/jjap_retriever.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[CLASS]** `JjapRetriever` (Line: 9~129)
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_retriever.py::main`
- **[METHOD]** `__init__` (Line: 16~21)
  - 🔗 *Calls (호출하는 것)*: `_load_symbols`
- **[METHOD]** `_load_symbols` (Line: 23~37)
  - 🔗 *Calls (호출하는 것)*: `load, len, open, exists, get, print`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_retriever.py::JjapRetriever.__init__`
- **[METHOD]** `retrieve_symbol` (Line: 39~98)
  - 🔗 *Calls (호출하는 것)*: `rstrip, len, next, startswith, _safe_truncate, readlines, strip, open, extend, join, append, _find_best_match, min, exists, get, print, max`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_retriever.py::main`
- **[METHOD]** `_find_best_match` (Line: 100~117)
  - 🔗 *Calls (호출하는 것)*: `get, print, lower`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_retriever.py::JjapRetriever.retrieve_symbol`
- **[METHOD]** `_safe_truncate` (Line: 119~129)
  - 🔗 *Calls (호출하는 것)*: `len, join, append, print, splitlines`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_retriever.py::JjapRetriever.retrieve_symbol`
- **[FUNCTION]** `main` (Line: 132~140)
  - 🔗 *Calls (호출하는 것)*: `len, JjapRetriever, print, retrieve_symbol, cwd`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/create_ai_map.py::generate_ai_optimized_map`

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

### 📄 python_agent_tools/jjap_watcher.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[FUNCTION]** `import_file_directly` (Line: 20~28)
  - 🔗 *Calls (호출하는 것)*: `ImportError, module_from_spec, exec_module, str, spec_from_file_location`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_watcher.py::run_pipeline`
- **[FUNCTION]** `run_pipeline` (Line: 30~73)
  - 🔗 *Calls (호출하는 것)*: `generate_ai_optimized_map, update_map, import_file_directly, scan_project, print_exc, AdvancedIndexerV2, get, print`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_watcher.py::CodeChangeHandler.dispatch, python_agent_tools/jjap_watcher.py::main`
- **[CLASS]** `CodeChangeHandler` (Line: 76~99)
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_watcher.py::main`
- **[METHOD]** `__init__` (Line: 77~79)
- **[METHOD]** `dispatch` (Line: 81~99)
  - 🔗 *Calls (호출하는 것)*: `as_posix, Path, time, any, run_pipeline, print`
- **[FUNCTION]** `main` (Line: 101~127)
  - 🔗 *Calls (호출하는 것)*: `CodeChangeHandler, schedule, join, start, str, run_pipeline, print, Observer, stop, sleep`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/create_ai_map.py::generate_ai_optimized_map`

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

### 📄 python_agent_tools/rule.txt
#### 🧱 Code Skeleton:
```python
Non-Python File (.TXT)
```

--------------------------------------------------

### 📄 python_agent_tools/switch.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 python_agent_tools/update_map.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[FUNCTION]** `update_map` (Line: 4~89)
  - 🔗 *Calls (호출하는 것)*: `sorted, Path, load, len, upper, strip, open, any, join, append, items, keys, exists, get, print, write`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_watcher.py::run_pipeline`

#### 🧱 Code Skeleton:
```python
def update_map(...):
    ...
```

--------------------------------------------------

