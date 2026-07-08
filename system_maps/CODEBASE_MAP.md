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
- **[FUNCTION]** `__init__` (Line: 12~16)
- **[FUNCTION]** `_load_database` (Line: 18~25)
- **[FUNCTION]** `extract_multi_slices` (Line: 30~208)
- **[CLASS]** `JjapCursorNavigatorGUI` (Line: 213~339)
- **[FUNCTION]** `__init__` (Line: 214~263)
- **[FUNCTION]** `execute_slicing_pipeline` (Line: 265~320)
- **[FUNCTION]** `manual_export_file` (Line: 322~339)

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
- **[FUNCTION]** `__init__` (Line: 16~18)
- **[FUNCTION]** `read_and_clean_file` (Line: 20~78)
- **[FUNCTION]** `assemble_ai_prompt` (Line: 80~107)

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
- **[FUNCTION]** `collect_target_files` (Line: 105~134)
- **[FUNCTION]** `load_registry` (Line: 137~151)
- **[FUNCTION]** `load_protocols` (Line: 154~169)
- **[FUNCTION]** `main` (Line: 172~245)
- **[FUNCTION]** `generate_ai_optimized_map` (Line: 252~254)

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
- **[CLASS]** `AdvancedIndexerV2` (Line: 25~242)
- **[FUNCTION]** `__init__` (Line: 34~42)
- **[FUNCTION]** `_get_sha256` (Line: 44~45)
- **[FUNCTION]** `_extract_skeleton` (Line: 47~63)
- **[FUNCTION]** `parse_protocols_and_registries` (Line: 65~98)
- **[FUNCTION]** `index_file` (Line: 100~173)
- **[FUNCTION]** `scan_project` (Line: 175~242)

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
- **[FUNCTION]** `__init__` (Line: 16~21)
- **[FUNCTION]** `_load_symbols` (Line: 23~37)
- **[FUNCTION]** `retrieve_symbol` (Line: 39~98)
- **[FUNCTION]** `_find_best_match` (Line: 100~117)
- **[FUNCTION]** `_safe_truncate` (Line: 119~129)
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
- **[CLASS]** `CodeChangeHandler` (Line: 76~99)
- **[FUNCTION]** `__init__` (Line: 77~79)
- **[FUNCTION]** `dispatch` (Line: 81~99)
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

#### 🧱 Code Skeleton:
```python
def update_map(...):
    ...
```

--------------------------------------------------

