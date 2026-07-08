# 🏗️ 짭커서 프로젝트 CODEBASE MAP

현재 인덱싱된 총 파일 수: **9개**

## 🗂️ [Module Index]
- `python_agent_tools/agent_navigator.py`
- `python_agent_tools/context_builder.py`
- `python_agent_tools/create_ai_map.py`
- `python_agent_tools/indexer.py`
- `python_agent_tools/jjap_lookup.py`
- `python_agent_tools/jjap_retriever.py`
- `python_agent_tools/jjap_watcher.py`
- `python_agent_tools/switch.py`
- `python_agent_tools/update_map.py`

## 💀 [Skeleton & Dependency 명세서]
### 📄 python_agent_tools/agent_navigator.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[CLASS]** `SemanticNavigator` (Line: 11~342)
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/agent_navigator.py::JjapCursorNavigatorGUI.__init__`
- **[METHOD]** `SemanticNavigator.__init__` (Line: 12~16)
  - 🔗 *Calls (호출하는 것)*: `_load_database`
- **[METHOD]** `SemanticNavigator._load_database` (Line: 18~25)
  - 🔗 *Calls (호출하는 것)*: `exists, open, load`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/agent_navigator.py::SemanticNavigator.__init__`
- **[METHOD]** `SemanticNavigator.extract_multi_slices` (Line: 30~342)
  - 🔗 *Calls (호출하는 것)*: `findall, max, append, len, repr, endswith, exists, join, readlines, printExec, open, print, split, int, any, get, min, strip, print_exc, replace`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/agent_navigator.py::JjapCursorNavigatorGUI.execute_slicing_pipeline`
- **[CLASS]** `JjapCursorNavigatorGUI` (Line: 347~468)
- **[METHOD]** `JjapCursorNavigatorGUI.__init__` (Line: 348~397)
  - 🔗 *Calls (호출하는 것)*: `SemanticNavigator, Button, title, Label, insert, geometry, Text, Frame, pack`
- **[METHOD]** `JjapCursorNavigatorGUI.execute_slicing_pipeline` (Line: 399~449)
  - 🔗 *Calls (호출하는 것)*: `open, rstrip, config, join, insert, delete, write, showerror, startswith, strip, get, extract_multi_slices, append, showwarning`
- **[METHOD]** `JjapCursorNavigatorGUI.manual_export_file` (Line: 451~468)
  - 🔗 *Calls (호출하는 것)*: `open, showinfo, write, showerror, str, asksaveasfilename`

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
- **[CLASS]** `ContextBuilder` (Line: 13~106)
- **[METHOD]** `ContextBuilder.__init__` (Line: 16~18)
  - 🔗 *Calls (호출하는 것)*: `Path`
- **[METHOD]** `ContextBuilder.read_and_clean_file` (Line: 20~77)
  - 🔗 *Calls (호출하는 것)*: `exists, open, join, split, readlines, startswith, strip, len, append, endswith, FileNotFoundError`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/context_builder.py::ContextBuilder.assemble_ai_prompt`
- **[METHOD]** `ContextBuilder.assemble_ai_prompt` (Line: 79~106)
  - 🔗 *Calls (호출하는 것)*: `read_and_clean_file, str, join, append`

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
- **[FUNCTION]** `collect_target_files` (Line: 105~133)
- **[FUNCTION]** `load_registry` (Line: 136~150)
- **[FUNCTION]** `load_protocols` (Line: 153~168)
- **[FUNCTION]** `main` (Line: 171~239)
- **[FUNCTION]** `generate_ai_optimized_map` (Line: 246~248)

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
- **[CLASS]** `AdvancedIndexerV2` (Line: 22~227)
- **[METHOD]** `AdvancedIndexerV2.__init__` (Line: 31~39)
- **[METHOD]** `AdvancedIndexerV2._get_sha256` (Line: 41~42)
  - 🔗 *Calls (호출하는 것)*: `encode, hexdigest, sha256`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/indexer.py::AdvancedIndexerV2.index_file`
- **[METHOD]** `AdvancedIndexerV2._extract_skeleton` (Line: 44~60)
  - 🔗 *Calls (호출하는 것)*: `parse, isinstance, join, append`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/indexer.py::AdvancedIndexerV2.index_file`
- **[METHOD]** `AdvancedIndexerV2.parse_protocols_and_registries` (Line: 62~95)
  - 🔗 *Calls (호출하는 것)*: `parse, type, isinstance, lower`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/indexer.py::AdvancedIndexerV2.index_file`
- **[METHOD]** `AdvancedIndexerV2.index_file` (Line: 97~168)
  - 🔗 *Calls (호출하는 것)*: `list, parse, open, stat, getattr, parse_protocols_and_registries, _get_sha256, as_posix, _extract_skeleton, read, walk, int, relative_to, dump, set, isinstance, append`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/indexer.py::AdvancedIndexerV2.scan_project`
- **[METHOD]** `AdvancedIndexerV2.scan_project` (Line: 170~227)
  - 🔗 *Calls (호출하는 것)*: `list, exists, open, print, append, Path, walk, set, any, get, dump, makedirs, index_file, replace, endswith, sorted`

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
- **[FUNCTION]** `lookup_symbol` (Line: 16~43)
- **[FUNCTION]** `show_skeleton` (Line: 45~61)

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
- **[METHOD]** `JjapRetriever.__init__` (Line: 16~21)
  - 🔗 *Calls (호출하는 것)*: `_load_symbols`
- **[METHOD]** `JjapRetriever._load_symbols` (Line: 23~37)
  - 🔗 *Calls (호출하는 것)*: `exists, open, print, load, get, len`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_retriever.py::JjapRetriever.__init__`
- **[METHOD]** `JjapRetriever.retrieve_symbol` (Line: 39~98)
  - 🔗 *Calls (호출하는 것)*: `exists, open, print, _safe_truncate, rstrip, join, extend, next, _find_best_match, readlines, get, startswith, strip, max, min, len, append`
- **[METHOD]** `JjapRetriever._find_best_match` (Line: 100~117)
  - 🔗 *Calls (호출하는 것)*: `get, print, lower`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_retriever.py::JjapRetriever.retrieve_symbol`
- **[METHOD]** `JjapRetriever._safe_truncate` (Line: 119~129)
  - 🔗 *Calls (호출하는 것)*: `print, join, splitlines, len, append`
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_retriever.py::JjapRetriever.retrieve_symbol`
- **[FUNCTION]** `main` (Line: 132~140)

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
- **[FUNCTION]** `run_pipeline` (Line: 30~73)
  - 🎯 *Used By (나를 부르는 곳)*: `python_agent_tools/jjap_watcher.py::CodeChangeHandler.dispatch`
- **[CLASS]** `CodeChangeHandler` (Line: 76~99)
- **[METHOD]** `CodeChangeHandler.__init__` (Line: 77~79)
- **[METHOD]** `CodeChangeHandler.dispatch` (Line: 81~99)
  - 🔗 *Calls (호출하는 것)*: `print, Path, as_posix, any, run_pipeline, time`
- **[FUNCTION]** `main` (Line: 101~127)

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

### 📄 python_agent_tools/switch.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 python_agent_tools/update_map.py
#### 🔍 내부 심볼 및 의존성 관계:
- **[FUNCTION]** `update_map` (Line: 4~88)

#### 🧱 Code Skeleton:
```python
def update_map(...):
    ...
```

--------------------------------------------------

