# ==========================================================================
# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드
# [SCAN_MODE] ROOT
# ==========================================================================
# 📄 [요청 1] TARGET: tools/universal_indexer/config.py (1-35라인)
# ----------------------------------------------------------
```python
# tools/universal_indexer/config.py
import sys
from pathlib import Path

# =====================================================================
# 📌 1. PROJECT ROOT RESOLUTION
# =====================================================================
def get_project_root() -> Path:
    """
    현재 파일의 위치를 기준으로 프로젝트의 마스터 루트 디렉토리를 역추적하여 반환합니다.
    `tools/universal_indexer` 구조 내부 또는 루트에 위치한 경우 모두 대응합니다.
    """
    script_dir = Path(__file__).parent.resolve()
    if script_dir.name == "universal_indexer" and script_dir.parent.name == "tools":
        return script_dir.parent.parent
    return script_dir

PROJECT_ROOT = get_project_root()

# =====================================================================
# 🎛️ 2. SCAN MODE INTERFACE
# =====================================================================
def get_scan_mode() -> str:
    """switch.py의 SCAN_MODE 상태를 동적으로 확인합니다."""
    try:
        from switch import SCAN_MODE
        return SCAN_MODE
    except ImportError:
        try:
            from tools.universal_indexer.switch import SCAN_MODE
            return SCAN_MODE
        except ImportError:
            return "ROOT"

# =====================================================================
```

# 📄 [요청 2] TARGET: tools/universal_indexer/switch.py (1-13라인)
# ----------------------------------------------------------
```python
"""Jjap-Cursor Path Targeting Toggle Controller.

[switch.py]
형님이 프로젝트 소스코드를 수색할 때, 실제 디스크 경로와 1대1로 일치시킬지("ROOT"),
아니면 기존 격리 구조 내부만 스캔할지("EXTRACTION_TARGET_PROJECT") 딸깍 결정하는 영문 마스터 콘솔 스위치입니다.
"""

# 🎛️ 마스터 토글 스위치 
# "ROOT" -> 프로젝트 전체 원본 경로 직접 징집 (경로 불일치 에러 완벽 해결! 실제 경로 유지)
# "EXTRACTION_TARGET_PROJECT"  -> 기존 방식 (오직 extraction_target_project/ 폴더 내부만 검사)
SCAN_MODE = "ROOT"

SYSTEM_EXCLUDES = ["system_memory", "system_maps"]
```

# 📄 [요청 3] TARGET: tools/universal_indexer/indexer.py (1-206라인)
# ----------------------------------------------------------
```python
import json
import hashlib
import os
import importlib.util
from pathlib import Path
from typing import Dict, Any, List

from config import (
    PROJECT_ROOT,
    get_scan_mode,
    EXCLUDE_KEYWORDS,
    SYSTEM_MEMORY_DIR,
    CONTEXT_JSON_PATH,
    SYMBOLS_JSON_PATH,
    DEFINITION_MAP_PATH,
    REGISTRY_JSON_PATH,
    PROTOCOL_JSON_PATH
)

DEBUG_LOG = False

def log(message: str):
    if DEBUG_LOG:
        print(f"📡 [Indexer-Core Log] {message}")

class AdvancedIndexerV2:
    """
    [Jjap-Cursor Core Indexer V3.6 - Ultra Universal Engine]
    동적 플러그인 로딩 및 5대 장부 동기화의 모든 파이프라인에 디버깅 레이더를 도배했습니다.
    """
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = project_root
        self.parsers: Dict[str, Any] = {}
        self.symbols: List[Dict[str, Any]] = []
        self.files_context: Dict[str, Any] = {}
        self.definition_map: Dict[str, str] = {}
        self.data_protocols: Dict[str, Any] = {}
        self.registry_constants: List[str] = []
        
        # log(f"🏗️ 인덱서 코어 초기화 완료 (마스터 루트 주소: {self.project_root})")
        self._auto_load_parsers()

    def _auto_load_parsers(self):
        """core_parsers 폴더 내부의 파서들을 동적 로드하여 확장자별로 바인딩합니다."""
        parsers_dir = Path(__file__).parent.resolve() / "core_parsers" # ✅ 수정완료
        # log(f"🔌 동적 파서 폴더 탐색 시작 -> 경로: {parsers_dir}")
        
        if not parsers_dir.exists():
            # log(f"⚠️ [경고] core_parsers 폴더가 물리적으로 존재하지 않습니다: {parsers_dir}")
            return

        file_list = os.listdir(parsers_dir)
        # log(f"📂 폴더 내부 파일 목록 검색 완료 (총 {len(file_list)}개 탐지됨)")

        for file in file_list:
            if file.endswith("_parser.py"):
                ext = f".{file.split('_parser.py')[0]}"
                full_path = parsers_dir / file
                # log(f"   ⚙️ 파서 후보 발견: '{file}' -> 매핑 타깃 확장자: '{ext}'")
                
                try:
                    spec = importlib.util.spec_from_file_location(f"parser_{ext}", full_path)
                    if spec and spec.loader:
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                        if hasattr(mod, "extract_symbols"):
                            self.parsers[ext] = mod.extract_symbols
                            # log(f"   └── 🟢 [바인딩 성공] 확장자 [{ext}] 엔진 탑재 완료!")
                        else:
                            # log(f"   └── ❌ [인터페이스 불일치] '{file}' 내부에 'extract_symbols' 함수가 없습니다.")
                            pass
                except Exception as ex:
                    # log(f"   └── 💥 [런타임 컴파일 에러] 파서 플러그인 로딩 실패: {file} | 사유: {ex}")
                    pass

        # log(f"📊 파서 동적 마운트 최종 정산: 총 {len(self.parsers)}개의 다국어 컴포넌트 활성화.")

    def scan_project(self):
        scan_mode = get_scan_mode()
        scan_target = self.project_root if scan_mode == "ROOT" else self.project_root / "extraction_target_project"
        # log(f"🛡️ 고유 스캔 제외 키워드 목록: {EXCLUDE_KEYWORDS}")
        
        if not scan_target.exists():
            # log(f"❌ [치명적 오류] 지정된 스캔 타깃 경로가 디스크에 존재하지 않습니다: {scan_target}")
            return

        total_scanned_count = 0
        total_ignored_count = 0

        for root, dirs, files in os.walk(scan_target, followlinks=True):
            normalized_root = root.replace("\\", "/")
            
            # 제외 폴더 조건 검사 및 로깅
            if any(kw in normalized_root for kw in EXCLUDE_KEYWORDS):
                # log(f"🚫 [패스] 제외 필터 경로 스킵: {normalized_root}")
                continue

            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                # 동적으로 로드된 파서 대상 확장자 범위에 포함되는지 확인
                if ext in self.parsers:
                    # log(f"🔍 [타깃 포착] 파일 발견: {file_path.name} (확장자: {ext})")
                    self.index_file(file_path, ext)
                    total_scanned_count += 1
                else:
                    total_ignored_count += 1

        # 🔗 [글로벌 used_by 역방향 바인딩 후처리 엔진]
        # 🛡️ [동명 메서드 오매칭 방지] 단순 이름(run, save 등) 모호성에 따른 오기입 방지 안전 알고리즘
        from collections import defaultdict
        sym_by_name = defaultdict(list)
        for s in self.symbols:
            if "name" in s:
                sym_by_name[s["name"]].append(s)

        for s in self.symbols:
            caller_id = s.get("symbol_id")
            if not caller_id:
                continue

            for called_name in s.get("calls", []):
                short_name = called_name.split(".")[-1] if "." in called_name else called_name
                candidates = sym_by_name.get(short_name, [])

                if len(candidates) == 1:
                    # 1. 전역에서 유일한 심볼명인 경우 바인딩
                    target_sym = candidates[0]
                    if caller_id not in target_sym.setdefault("used_by", []):
                        target_sym["used_by"].append(caller_id)
                elif len(candidates) > 1:
                    # 2. 동명 심볼이 여럿 존재하는 경우: 같은 파일 내 심볼 1개 우선 탐색
                    same_file_candidates = [c for c in candidates if c.get("file") == s.get("file") or c.get("path") == s.get("path")]
                    if len(same_file_candidates) == 1:
                        target_sym = same_file_candidates[0]
                        if caller_id not in target_sym.setdefault("used_by", []):
                            target_sym["used_by"].append(caller_id)

        # 🗂️ 수집 완료 후 디스크 정밀 장부 보관소로 직행 쓰기
        self.save_index_data()

    def index_file(self, file_path: Path, ext: str):
        """개별 파일을 파서를 통해 쪼개어 마스터 장부에 바느질합니다."""
        try:
            rel_path_str = file_path.relative_to(self.project_root).as_posix()
        except ValueError:
            rel_path_str = file_path.resolve().relative_to(self.project_root.resolve()).as_posix()

        # log(f"🧵 [장부 바느질 개시] 상대 경로 키: '{rel_path_str}'")
        parser_func = self.parsers[ext]
        
        try:
            # log(f"   📡 플러그인 함수 {parser_func.__name__} 원격 연산 제어권 이양 중...")
            res = parser_func(file_path, self.project_root)
            
            if not res or len(res) < 5:
                # log(f"   ⚠️ [규격 위반] '{rel_path_str}' 파서의 반환 데이터가 5대 규격을 충족하지 못해 드롭합니다.")
                return

            f_symbols, f_context, f_def_map, f_protocols, f_registry = res

            # 데이터 적재 현황 세부 체크 로그
            # log(f"   📥 수집 결과 피드백 받음 -> 심볼: {len(f_symbols)}개, 정의 매핑: {len(f_def_map)}개, 프로토콜: {len(f_protocols)}개, 레지스트리: {len(f_registry)}개")

            # 1. 글로벌 심볼 리스트 누적
            self.symbols.extend(f_symbols)
            
            # 2. 파일 요약 정보 컨텍스트 병합
            self.files_context.update(f_context)
            
            # 3. 정의 맵 및 레지스트리 병합
            self.definition_map.update(f_def_map)
            self.data_protocols.update(f_protocols)
            
            for item in f_registry:
                if item not in self.registry_constants:
                    self.registry_constants.append(item)

            # log(f"   📈 [바느질 완료] 마스터 메모리 장부 적재 성공: '{rel_path_str}'")
        except Exception as e:
            # log(f"   💥 [인덱싱 내부 크래시] 파일 처리 중 예외 발생: {rel_path_str} | 에러 내용: {e}")
            pass

    def save_index_data(self):
        try:
            SYSTEM_MEMORY_DIR.mkdir(parents=True, exist_ok=True)

            with open(CONTEXT_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump({"files": self.files_context}, f, indent=2, ensure_ascii=False)

            with open(SYMBOLS_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump({"symbols": self.symbols}, f, indent=2, ensure_ascii=False)

            with open(DEFINITION_MAP_PATH, "w", encoding="utf-8") as f:
                json.dump(self.definition_map, f, indent=2, ensure_ascii=False)

            with open(PROTOCOL_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump({"protocols": self.data_protocols}, f, indent=2, ensure_ascii=False)

            with open(REGISTRY_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump({"registered_entities": self.registry_constants}, f, indent=2, ensure_ascii=False)

            print(f"🧬 [Jjap-Indexer Universal] 5대 장부 전체 동기화 성공! 보관된 총 파일 수: {len(self.files_context)}개")
        except Exception as write_err:
            pass
```

# 📄 [요청 3 🔗 제이슨연동 (log 호출처 -> tools/universal_indexer/core_parsers/java_parser.py의 [extract_symbols])] TARGET: tools/universal_indexer/core_parsers/java_parser.py (39-194라인)
# ----------------------------------------------------------
```python
def extract_symbols(file_path: Path, project_root: Path):
    """
    ☕ [Java Core Advanced Parser v2.0]
    파이썬과 100% 동일한 5대 장부 규격을 만족하도록 자바 소스를 정밀 해부합니다.
    - 중첩 경로(src/src) 방어선 구축 완료
    - imp: 임포트 패키지 완벽 추출
    - calls: 메서드 내부 호출 분석 엔진 탑재
    - 줄 범위 (시작줄-끝줄) 매칭 완벽 지원
    """
    symbols = []
    file_context = {}
    definition_map = {}
    data_protocols = {}
    registry_constants = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        log(f"❌ 파일 읽기 실패: {file_path} | 에러: {e}")
        return symbols, {}, {}, {}, []

    # 🚨 [교정] 독단적인 src/src/ 축약을 제거하고 실제 디스크 상대 경로 규격을 그대로 보존합니다.
    try:
        raw_rel = file_path.relative_to(project_root).as_posix()
    except ValueError:
        raw_rel = file_path.name

    # 별도의 치환 없이 디스크 실제 경로를 단일 진실 공급원(Single Source of Truth) 키값으로 확정
    rel_path_str = raw_rel

    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    lines = content.splitlines()

    # 1. 🧲 임포트(Imports) 및 패키지 징집
    imports = []
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith("import ") and line_strip.endswith(";"):
            imp_target = line_strip.replace("import ", "").replace(";", "").strip()
            imports.append(imp_target)
            
    imports_str = f"💡 📦 imp: {', '.join(sorted(list(set(imports))))}" if imports else ""

    # 2. 🩻 클래스 및 메서드 심볼 다차원 스캔
    symbols_info_strings = []
    skeleton_segments = []
    
    current_class = None
    class_start_idx = -1

    # 자바 클래스/인터페이스/메서드 탐색 정규식
    class_patt = re.compile(r'(?:public|protected|private|static|\s)+\s+(?:class|interface|enum)\s+([a-zA-Z0-9_]+)')
    method_patt = re.compile(r'(?:public|protected|private|static|\s)+\s+[\w<>\s?\[\]]+\s+([a-zA-Z0-9_]+)\s*\([^)]*\)\s*(?:throws\s+[\w\s,]+)?\s*\{?')

    for idx, line in enumerate(lines):
        line_num = idx + 1
        line_stripped = line.strip()
        
        # 주석이나 공백 라인은 스킵
        if line_stripped.startswith("//") or line_stripped.startswith("*") or not line_stripped:
            continue

        # A. 클래스 탐지
        class_match = class_patt.search(line)
        if class_match:
            c_name = class_match.group(1)
            current_class = c_name
            class_start_idx = idx
            end_line = _find_matching_curly_brace(lines, idx)
            
            param_match = re.search(r'\((.*?)\)', line_stripped)
            params_str = ""
            if param_match:
                raw_params = param_match.group(1).strip()
                if raw_params:
                    param_types = [p.strip().split()[0] for p in raw_params.split(",") if p.strip()]
                    params_str = ", ".join(param_types)

            symbols_info_strings.append(f"🧬 class {c_name} [L{line_num}-{end_line}]")
            skeleton_segments.append(f"class {c_name} {{ // L{line_num}-{end_line}")
            
            c_id = f"{rel_path_str}::{c_name}"
            symbols.append({
                "symbol_id": c_id,
                "name": c_name, "full_name": c_name, "type": "class",
                "path": rel_path_str, "start_line": line_num, "end_line": end_line,
                "calls": [], "used_by": []
            })
            definition_map[c_id] = f"{rel_path_str}:{line_num}"
            continue

        # B. 메서드 탐지 및 인자(파라미터) 정밀 추출
        method_match = method_patt.search(line)
        if method_match and ("(" in line_stripped and "import " not in line_stripped):
            m_name = method_match.group(1)
            
            if m_name in ["if", "for", "while", "switch", "catch", "return"]:
                continue
                
            param_match = re.search(r'\((.*?)\)', line_stripped)
            params_str = ""
            if param_match:
                raw_params = param_match.group(1).strip()
                if raw_params:
                    param_types = [p.strip().split()[0] for p in raw_params.split(",") if p.strip()]
                    params_str = ", ".join(param_types)

            end_line = _find_matching_curly_brace(lines, idx)
            
            # 메서드 바디 본문 추출 (내부 호출 함수 파싱용)
            body_lines = lines[idx:end_line]
            body_text = "\n".join(body_lines)
            
            # 내부 호출 추적
            possible_calls = re.findall(r'([a-zA-Z0-9_]+)\s*\(', body_text)
            detected_calls = [
                name for name in possible_calls 
                if name not in ["if", "for", "while", "switch", "catch", "synchronized", "super", "this", m_name]
            ]
            detected_calls = list(set(detected_calls))

            if current_class:
                m_id = f"{rel_path_str}::{current_class}.{m_name}"
                full_name = f"{current_class}.{m_name}"
                symbols_info_strings.append(f"🎯 def {m_name}({params_str}) [L{line_num}-{end_line}]")
                skeleton_segments.append(f"    {line_stripped} // L{line_num}-{end_line}")
            else:
                m_id = f"{rel_path_str}::{m_name}"
                full_name = m_name
                symbols_info_strings.append(f"🎯 def {m_name}({params_str}) [L{line_num}-{end_line}]")
                skeleton_segments.append(f"{line_stripped} // L{line_num}-{end_line}")

            symbols.append({
                "symbol_id": m_id, "name": m_name, "full_name": full_name, "type": "method",
                "path": rel_path_str, "start_line": line_num, "end_line": end_line,
                "calls": detected_calls, "used_by": []
            })
            definition_map[m_id] = f"{rel_path_str}:{line_num}"

    # 3. 🧱 소스 스켈레톤 마감 처리
    skeleton_text = "\n".join(skeleton_segments)

    # 4. 🎚️ 파이썬 마스터 규격 한줄 요약 문자열 조립 완료
    summary_parts = [imports_str] if imports_str else []
    summary_parts.extend(symbols_info_strings)
    symbols_summary_str = " | ".join(summary_parts)

    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": symbols_summary_str,
        "skeleton": skeleton_text
    }

    log(f"✅ 자바 소스 스캔 완료 -> 경로: {rel_path_str} | 심볼: {len(symbols)}개 포착")
    return symbols, file_context, definition_map, data_protocols, registry_constants
```

# 📄 [요청 3 ➡️ 불러온함수 (get_scan_mode 본체)] TARGET: tools/universal_indexer/config.py (23-33라인)
# ----------------------------------------------------------
```python
def get_scan_mode() -> str:
    """switch.py의 SCAN_MODE 상태를 동적으로 확인합니다."""
    try:
        from switch import SCAN_MODE
        return SCAN_MODE
    except ImportError:
        try:
            from tools.universal_indexer.switch import SCAN_MODE
            return SCAN_MODE
        except ImportError:
            return "ROOT"
```

# 📄 [요청 3 ➡️ 불러온함수 (__init__ 본체)] TARGET: agent_core/plan/gemini_client.py (62-88라인)
# ----------------------------------------------------------
```python
    def __init__(self, api_key: Optional[str] = None, root_dir: Optional[Path] = None):
        # 1. 루트 경로 지정 및 .env 선제 자동 로드
        self.root_dir = root_dir or Path.cwd()
        env_file = self.root_dir / ".env"
        load_env_file(env_file)

        # 2. API Key 확보 (인자값 -> os.environ)
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = None
        
        if DEBUG_MODE:
            log_debug(lambda: f"GeminiPlannerClient 초기화 - API Key 존재 여부: {bool(self.api_key)}")

        if not HAS_GENAI:
            if DEBUG_MODE:
                log_debug(lambda: "[경고] 'google-genai' 패키지가 없습니다. 'pip install google-genai'가 필요합니다.")
            return

        if self.api_key:
            try:
                # 공식 SDK 클라이언트 초기화
                self.client = genai.Client(api_key=self.api_key)
                if DEBUG_MODE:
                    log_debug(lambda: "Google GenAI Client (API 키 연결) 초기화 완")
            except Exception as e:
                if DEBUG_MODE:
                    log_debug(lambda: f"Google GenAI Client 초기화 실패: {e}")
```

# 📄 [요청 3 ➡️ 불러온함수 (__init__ 본체)] TARGET: agent_core/plan/prompt_builder.py (25-33라인)
# ----------------------------------------------------------
```python
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        # system_maps/ 경로 우선 탐색 후 루트 fallback
        self.map_file = root_dir / "system_maps" / "AI_CODEBASE_MAP.md"
        if not self.map_file.exists():
            self.map_file = root_dir / "AI_CODEBASE_MAP.md"
            
        if DEBUG_MODE:
            log_debug(lambda: f"PromptBuilder 초기화 완료 - Root: {self.root_dir}, Map File Path: {self.map_file}")
```

# 📄 [요청 3 ➡️ 불러온함수 (__init__ 본체)] TARGET: tools/multi_agent_system/agent_code_extractor.py (22-48라인)
# ----------------------------------------------------------
```python
    def __init__(self, root_dir: str | Path):
        self.raw_root_dir = Path(root_dir).resolve()
        self.scan_mode = "ROOT"
        
        # 🎛️ [SCAN_MODE 스위치 반영 - universal_indexer/switch.py 절대 위치 고정]
        try:
            idx_path = str((self.raw_root_dir / "tools" / "universal_indexer").resolve())
            if idx_path not in sys.path:
                sys.path.insert(0, idx_path)
            
            import switch
            self.scan_mode = getattr(switch, "SCAN_MODE", "ROOT")
            print(f"🎛️ [SWITCH DETECTED] 현재 탐색 스위치 모드: {self.scan_mode}")
        except Exception as e:
            print(f"⚠️ [SWITCH WARNING] switch.py를 로드하지 못해 기본 'ROOT' 모드로 동작합니다. (이유: {e})")

        # 🚀 SRC 모드일 경우 하드디스크 탐색 기준점(self.root_dir)에 'src' 폴더를 강제 결합
        if self.scan_mode == "SRC":
            self.root_dir = self.raw_root_dir / "src"
            print(f"📁 [MODE: SRC] 탐색 마스터 루트가 복사/격리용 src 폴더로 변경되었습니다: {self.root_dir}")
        else:
            self.root_dir = self.raw_root_dir
            print(f"📁 [MODE: ROOT] 탐색 마스터 루트가 프로젝트 원본 루트로 설정되었습니다: {self.root_dir}")

        # 🧠 [불러오기 교정] 장부 정보는 언제나 프로젝트의 실제 본체 루트(raw_root_dir) 기준으로 가져옵니다.
        self.symbols_path = self.raw_root_dir / "system_memory" / ".jjap_symbols.json"
        self.symbols_data = self._load_database()
```

# 📄 [요청 3 ➡️ 불러온함수 (__init__ 본체)] TARGET: tools/multi_agent_system/agent_session.py (20-27라인)
# ----------------------------------------------------------
```python
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir.resolve()
        load_env_file(self.root_dir / ".env")
        
        # 1. 사용 도구 인스턴스화
        self.extractor = CodeExtractor(self.root_dir)
        self.patcher = CodePatcher(self.root_dir)
        self.client = None
```

# 📄 [요청 3 ➡️ 불러온함수 (__init__ 본체)] TARGET: tools/multi_agent_system/code_patcher.py (10-11라인)
# ----------------------------------------------------------
```python
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir).resolve()
```

# 📄 [요청 3 ➡️ 불러온함수 (__init__ 본체)] TARGET: tools/universal_indexer/agent_navigator.py (23-46라인)
# ----------------------------------------------------------
```python
    def __init__(self, root_dir: str | Path):
        self.raw_root_dir = Path(root_dir).resolve()
        self.scan_mode = "ROOT"
        
        try:
            idx_path = str((self.raw_root_dir / "tools" / "universal_indexer").resolve())
            if idx_path not in sys.path:
                sys.path.insert(0, idx_path)
            
            import switch
            self.scan_mode = getattr(switch, "SCAN_MODE", "ROOT")
            print(f"🎛️ [SWITCH DETECTED] 현재 탐색 스위치 모드: {self.scan_mode}")
        except Exception as e:
            print(f"⚠️ [SWITCH WARNING] switch.py를 로드하지 못해 기본 'ROOT' 모드로 동작합니다. (이유: {e})")

        if self.scan_mode == "SRC":
            self.root_dir = self.raw_root_dir / "src"
            print(f"📁 [MODE: SRC] 탐색 마스터 루트가 복사/격리용 src 폴더로 변경되었습니다: {self.root_dir}")
        else:
            self.root_dir = self.raw_root_dir
            print(f"📁 [MODE: ROOT] 탐색 마스터 루트가 프로젝트 원본 루트로 설정되었습니다: {self.root_dir}")

        self.symbols_path = self.raw_root_dir / "system_memory" / ".jjap_symbols.json"
        self.symbols_data = self._load_database()
```

# 📄 [요청 3 ➡️ 불러온함수 (__init__ 본체)] TARGET: tools/universal_indexer/agent_navigator.py (289-339라인)
# ----------------------------------------------------------
```python
    def __init__(self, root, project_root: Path):
        self.root = root
        self.project_root = project_root
        self.extractor = CodeExtractor(project_root)
        self.last_markdown_content = ""

        # GUI Title에 현재 스캔 모드를 가독성 있게 표기
        self.root.title(f"⚡ Jjap-Cursor Agent Navigator v2.0 (Auto-Exporter) | 모드: {self.extractor.scan_mode}")
        self.root.geometry("1000x750")

        self.main_container = ttk.Frame(root, padding="10")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        input_label = ttk.Label(self.main_container, text=f"📥 [에이전트 요청 프롬프트 입력 구역 - 현재 모드: {self.extractor.scan_mode}]", font=("Malgun Gothic", 11, "bold"))
        input_label.pack(anchor=tk.W, pady=(0, 5))

        self.prompt_input = tk.Text(self.main_container, height=6, font=("Malgun Gothic", 10))
        self.prompt_input.pack(fill=tk.X, pady=(0, 10))
        
        # 안내 문구 최적화
        if self.extractor.scan_mode == "SRC":
            self.prompt_input.insert(tk.END, "💡 실전 테스트 양식 예시 (SRC 모드):\nsrc/src/main/java/com/desertcore/deathevent.java:32-60")
        else:
            self.prompt_input.insert(tk.END, "💡 실전 테스트 양식 예시 (ROOT 모드):\nsrc/main/java/com/desertcore/deathevent.java:32-60")

        self.btn_frame = ttk.Frame(self.main_container)
        self.btn_frame.pack(fill=tk.X, pady=(0, 10))

        self.scan_button = ttk.Button(
            self.btn_frame, 
            text="⚡ 소스코드 정밀 슬라이싱 및 컨텍스트 바인딩 가동 ⚡", 
            command=self.execute_slicing_pipeline
        )
        self.scan_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.export_button = ttk.Button(
            self.btn_frame,
            text="💾 마크다운 파일(.md) 개별 내보내기",
            command=self.manual_export_file,
            state=tk.DISABLED
        )
        self.export_button.pack(side=tk.RIGHT, padx=(5, 0))

        output_label = ttk.Label(self.main_container, text="📄 [AI 배송용 최적화 켄텍스트 보따리 (출력 결과)]", font=("Malgun Gothic", 11, "bold"))
        output_label.pack(anchor=tk.W, pady=(0, 5))

        self.code_display = tk.Text(self.main_container, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        self.code_display.pack(fill=tk.BOTH, expand=True)

        self.status_label = ttk.Label(self.main_container, text=f"🟢 대기 중... [{self.extractor.scan_mode} 모드] 프롬프트를 입력하고 가동 버튼을 누르십시오.", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=(10, 0))
```

# 📄 [요청 3 ➡️ 불러온함수 (__init__ 본체)] TARGET: tools/universal_indexer/context_builder.py (17-20라인)
# ----------------------------------------------------------
```python
    def __init__(self, project_root: str) -> None:
        """비서관을 초기화하며 기준이 되는 프로젝트 루트 경로를 지정합니다."""
        self.project_root = Path(project_root)
        self.ignore_matcher = GitIgnoreMatcher(self.project_root)
```

# 📄 [요청 3 ➡️ 불러온함수 (__init__ 본체)] TARGET: tools/universal_indexer/jjap_retriever.py (16-21라인)
# ----------------------------------------------------------
```python
    def __init__(self, project_root: Path):
        self.project_root = project_root
        # 🧠 [불러오기 교정] 격리 폴더(system_memory) 안으로 이사 간 인덱싱 장부를 정확하게 바라보도록 관로를 꺾어줍니다.
        self.symbols_file = self.project_root / "system_memory" / ".jjap_symbols.json"
        self.max_context_lines = 300
        self.symbols_db = self._load_symbols()
```

# 📄 [요청 3 ➡️ 불러온함수 (__init__ 본체)] TARGET: tools/universal_indexer/jjap_watcher.py (82-84라인)
# ----------------------------------------------------------
```python
    def __init__(self):
        self.last_trigger_time = 0
        self.debounce_duration = 0.5  # 디바운스 초단위 설정
```

# 📄 [요청 3 ➡️ 불러온함수 (__init__ 본체)] TARGET: tools/universal_indexer/core_parsers/gitignore_parser.py (11-13라인)
# ----------------------------------------------------------
```python
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self._spec = None
```

# 📄 [요청 4] TARGET: tools/universal_indexer/create_ai_map.py (1-321라인)
# ----------------------------------------------------------
```python
import os
import ast
import json
from pathlib import Path

from config import (
    PROJECT_ROOT,
    get_scan_mode,
    EXCLUDE_KEYWORDS,
    CONTEXT_JSON_PATH,
    SYMBOLS_JSON_PATH,
    REGISTRY_JSON_PATH,
    PROTOCOL_JSON_PATH,
    AI_MAP_MD_PATH
)


def load_jjap_context():
    """통합 .jjap_context.json 장부 로드"""
    if CONTEXT_JSON_PATH.exists():
        try:
            with open(CONTEXT_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("files", {})
        except Exception as e:
            print(f"⚠️ [.jjap_context.json] 로드 중 오류 발생: {e}")
    else:
        print("⚠️ [.jjap_context.json] 통합 장부 파일을 찾을 수 없습니다. 인덱서를 먼저 실행해 주세요.")
    return {}


def collect_target_files():
    """프로젝트 내 대상 파일 수집 (원래 수집 로직 100% 동일)"""
    scan_mode = get_scan_mode()
    if scan_mode == "ROOT":
        scan_target = PROJECT_ROOT
        print("🎯 [create_ai_map] Mode: ROOT (프로젝트 전체 스캔)")
    else:
        scan_target = PROJECT_ROOT / "extraction_target_project"
        print("🎯 [create_ai_map] Mode: EXTRACTION_TARGET_PROJECT (타깃 폴더 스캔)")

    if not scan_target.exists():
        print(f"❌ [오류] 스캔 대상 경로가 존재하지 않습니다: {scan_target}")
        return []

    target_files = []
    for root, dirs, files in os.walk(scan_target, followlinks=True):
        normalized_root = root.replace("\\", "/")

        if "src/project_root/src" in normalized_root:
            continue
        if any(kw in normalized_root for kw in EXCLUDE_KEYWORDS):
            continue

        for file in files:
            if file == "start.py" and scan_mode == "SRC":
                continue
            
            full_path = Path(root) / file
            target_files.append(full_path)

    print(f"✅ 총 {len(target_files)}개 파일 수집 완료")
    return sorted(target_files)


def load_registry():
    """Universal Registry Loader"""
    if not REGISTRY_JSON_PATH.exists():
        return set()
    try:
        with open(REGISTRY_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if isinstance(data, dict) and "registered_entities" in data:
                entities = data["registered_entities"]
                if isinstance(entities, list):
                    return set(entities)
                elif isinstance(entities, dict):
                    return set(entities.keys())

            if isinstance(data, dict):
                extracted = set()
                for k, v in data.items():
                    if isinstance(v, list):
                        for item in v: extracted.add(str(item))
                    else:
                        extracted.add(str(k))
                return extracted

            if isinstance(data, list):
                return set(str(x) for x in data)

            return set()
    except Exception as e:
        print(f"⚠️ [맵메이커 방어선] 레지스트리 로드 실패 우회: {e}")
        return set()


def load_protocols():
    """Universal Protocol Loader"""
    if not PROTOCOL_JSON_PATH.exists():
        return {}
    try:
        with open(PROTOCOL_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            if isinstance(data, dict) and "protocols" in data:
                return data["protocols"]
                
            if isinstance(data, dict):
                return data
                
            return {}
    except Exception as e:
        print(f"⚠️ [맵메이커 방어선] 프로토콜 로드 실패 우회: {e}")
        return {}


def parse_protocols_and_registries():
    """심볼 장부 기반 매칭 테이블 완성 (원래 로직 100% 복원)"""
    path_to_registry = {}
    path_to_protocol = {}

    registry_data = load_registry()
    protocol_data = load_protocols()

    all_symbols = []
    if SYMBOLS_JSON_PATH.exists():
        try:
            with open(SYMBOLS_JSON_PATH, "r", encoding="utf-8") as f:
                all_symbols = json.load(f).get("symbols", [])
        except Exception as e:
            print(f"⚠️ [.jjap_symbols.json] 읽기 실패: {e}")

    for sym in all_symbols:
        if sym.get("type") != "class":
            continue
            
        cls_name = sym.get("name")
        rel_path = sym.get("path")
        
        if not cls_name or not rel_path:
            continue

        posix_rel_path = Path(rel_path).as_posix()

        if cls_name in registry_data:
            if posix_rel_path not in path_to_registry:
                path_to_registry[posix_rel_path] = set()
            path_to_registry[posix_rel_path].add(cls_name)

        if cls_name in protocol_data:
            if posix_rel_path not in path_to_protocol:
                path_to_protocol[posix_rel_path] = []
            if (cls_name, protocol_data[cls_name]) not in path_to_protocol[posix_rel_path]:
                path_to_protocol[posix_rel_path].append((cls_name, protocol_data[cls_name]))

    return path_to_registry, path_to_protocol


# [추가된 로더 함수]
def load_all_symbols():
    """통합 .jjap_symbols.json 장부 로드 및 파일별/심볼ID별 인덱싱"""
    symbols_by_file = {}
    symbol_by_id = {}
    
    if SYMBOLS_JSON_PATH.exists():
        try:
            with open(SYMBOLS_JSON_PATH, "r", encoding="utf-8") as f:
                symbols_list = json.load(f).get("symbols", [])
                for sym in symbols_list:
                    rel_path = sym.get("file") or sym.get("path")
                    if rel_path:
                        posix_path = Path(rel_path).as_posix()
                        symbols_by_file.setdefault(posix_path, []).append(sym)
                    
                    sym_id = sym.get("symbol_id")
                    if sym_id:
                        symbol_by_id[sym_id] = sym
        except Exception as e:
            print(f"⚠️ [.jjap_symbols.json] 로드 오류: {e}")
            
    return symbols_by_file, symbol_by_id


def main():
    scan_mode = get_scan_mode()
    target_files = collect_target_files()
    jjap_context = load_jjap_context()
    symbols_by_file, symbol_by_id = load_all_symbols()  # 💡 심볼 장부 로드 추가
    path_to_registry, path_to_protocol = parse_protocols_and_registries()

    AI_MAP_MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(AI_MAP_MD_PATH, "w", encoding="utf-8") as f:
        printed_dirs = set()

        f.write("# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)\n\n")
        f.write("> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.\n")
        f.write("> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.\n\n")
        
        if scan_mode == "EXTRACTION_TARGET_PROJECT":
            f.write("```markdown\nextraction_target_project/\n")
        else:
            f.write("```markdown\nproject_root/\n")
        
        for file_path in target_files:
            rel_path = file_path.relative_to(PROJECT_ROOT)
            posix_rel_path = rel_path.as_posix()
            file_name = file_path.name

            if scan_mode == "EXTRACTION_TARGET_PROJECT" and posix_rel_path.startswith("extraction_target_project/"):
                display_path = posix_rel_path[26:]
            else:
                display_path = posix_rel_path

            parts = Path(display_path).parts
            for i in range(len(parts) - 1):
                current_dir_path = Path(*parts[:i + 1]).as_posix()
                if current_dir_path not in printed_dirs:
                    printed_dirs.add(current_dir_path)
                    indent = "│   " * i
                    f.write(f"{indent}├── {parts[i]}/\n")

            indent = "│   " * (len(parts) - 1)

            file_meta = jjap_context.get(posix_rel_path, {})
            symbols_info = file_meta.get("symbols_summary", "")

            if not symbols_info and posix_rel_path.startswith("extraction_target_project/extraction_target_project/"):
                shorter_path = posix_rel_path.replace("extraction_target_project/extraction_target_project/", "extraction_target_project/", 1)
                symbols_info = jjap_context.get(shorter_path, {}).get("symbols_summary", "")

            if symbols_info:
                f.write(f"{indent}├── {file_name} [📂 {display_path}] -> [{symbols_info}]\n")
            else:
                f.write(f"{indent}├── {file_name} [📂 {display_path}]\n")

            if posix_rel_path in path_to_registry:
                for reg_const in path_to_registry[posix_rel_path]:
                    f.write(f"{indent}│     ├── 🔑 [REGISTRY]: \"{reg_const}\"\n")

            if posix_rel_path in path_to_protocol:
                for proto_name, fields in path_to_protocol[posix_rel_path]:
                    f.write(f"{indent}│     ├── 📊 [PROTOCOL]: \"{proto_name}\"\n")
                    field_items = [
                        f"{k}({v.replace(' (기본값: ', ':').replace(')', '')})"
                        for k, v in fields.items()
                    ]
                    chunks = [field_items[x:x + 4] for x in range(0, len(field_items), 4)]
                    for chunk in chunks:
                        f.write(f"{indent}│     │     ├── {', '.join(chunk)}\n")

# 🎯 [알맹이 보강] 정밀 심볼 트리 (클래스/함수/인자/줄범위/CALLS/USED_BY) 생성
            file_symbols = symbols_by_file.get(posix_rel_path, [])
            for sym in file_symbols:
                sym_type = sym.get("type", "function")
                sym_name = sym.get("name", "")
                full_name = sym.get("full_name", sym_name)
                if not sym_name:
                    continue

                # 1. 인자(Arguments) 복원 (args 리스트 또는 raw 파라미터 대응)
                raw_args = sym.get("args")
                if isinstance(raw_args, list):
                    args_str = f"({', '.join(raw_args)})" if raw_args else ""
                elif isinstance(raw_args, str) and raw_args:
                    args_str = f"({raw_args})"
                else:
                    args_str = ""

                # 2. 줄범위(Start Line - End Line) 계산
                start_line = sym.get("start_line")
                end_line = sym.get("end_line")
                if start_line and end_line and start_line != end_line:
                    line_str = f"[L{start_line}-L{end_line}]"
                elif start_line:
                    line_str = f"[L{start_line}]"
                else:
                    line_str = ""

                # 3. 타입별 아이콘 및 표현 구분
                if sym_type == "class":
                    icon_str = f"🧬 class {sym_name}"
                elif sym_type == "json_key":
                    icon_str = f"🔑 key \"{sym_name}\""
                elif sym_type == "method" or "." in full_name:
                    icon_str = f"🎯 def {sym_name}{args_str if args_str else '()'}"
                else:
                    icon_str = f"🎯 def {sym_name}{args_str if args_str else '()'}"

                f.write(f"{indent}│   ├── {icon_str} {line_str}\n".rstrip() + "\n")

                # 4. 호출 관계 (CALLS)
                calls = sym.get("calls", [])
                if calls:
                    f.write(f"{indent}│   │   ├── 📞 [CALLS]: {', '.join(calls)}\n")

                # 5. 역방향 참조 관계 (USED BY)
                used_by_ids = sym.get("used_by", [])
                if used_by_ids:
                    used_by_info = []
                    for u_id in used_by_ids:
                        target = symbol_by_id.get(u_id)
                        if target:
                            u_file = target.get("file") or target.get("path", "")
                            u_name = target.get("name", "")
                            # 동일 파일 내 호출이면 함수명만, 타 파일이면 파일 경로 포함
                            if u_file == posix_rel_path:
                                used_by_info.append(f"::{u_name}")
                            else:
                                used_by_info.append(f"{u_file}::{u_name}")
                        else:
                            used_by_info.append(str(u_id))
                    f.write(f"{indent}│   │   ├── 🔗 [USED BY]: {', '.join(used_by_info)}\n")

    print("🎯 [마스터 공장] 'system_maps/AI_CODEBASE_MAP.md'가 (인자, calls, used_by 관계망 포함) 정밀 자동 갱신되었습니다!")


def generate_ai_optimized_map():
    main()
```

# 📄 [요청 4 🔗 제이슨연동 (load_registry 호출처 -> tools/universal_indexer/create_ai_map.py의 [parse_protocols_and_registries])] TARGET: tools/universal_indexer/create_ai_map.py (119-158라인)
# ----------------------------------------------------------
```python
def parse_protocols_and_registries():
    """심볼 장부 기반 매칭 테이블 완성 (원래 로직 100% 복원)"""
    path_to_registry = {}
    path_to_protocol = {}

    registry_data = load_registry()
    protocol_data = load_protocols()

    all_symbols = []
    if SYMBOLS_JSON_PATH.exists():
        try:
            with open(SYMBOLS_JSON_PATH, "r", encoding="utf-8") as f:
                all_symbols = json.load(f).get("symbols", [])
        except Exception as e:
            print(f"⚠️ [.jjap_symbols.json] 읽기 실패: {e}")

    for sym in all_symbols:
        if sym.get("type") != "class":
            continue
            
        cls_name = sym.get("name")
        rel_path = sym.get("path")
        
        if not cls_name or not rel_path:
            continue

        posix_rel_path = Path(rel_path).as_posix()

        if cls_name in registry_data:
            if posix_rel_path not in path_to_registry:
                path_to_registry[posix_rel_path] = set()
            path_to_registry[posix_rel_path].add(cls_name)

        if cls_name in protocol_data:
            if posix_rel_path not in path_to_protocol:
                path_to_protocol[posix_rel_path] = []
            if (cls_name, protocol_data[cls_name]) not in path_to_protocol[posix_rel_path]:
                path_to_protocol[posix_rel_path].append((cls_name, protocol_data[cls_name]))

    return path_to_registry, path_to_protocol
```

# 📄 [요청 4 ➡️ 불러온함수 (main 본체)] TARGET: run_test.py (53-66라인)
# ----------------------------------------------------------
```python
def main():
    print("🚀 테스트 스크립트를 가동합니다...")
    
    # 1. 실행 시 디버그 로그 파일 초기화
    if LOG_FILE_PATH.exists():
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            f.write("=== [Jjap-Cursor Agent Debug Log Initialized] ===\n")
            
    print(f"📝 디버그 로그 위치: {LOG_FILE_PATH.resolve()}")
    print(f"🎛️ 현재 DEBUG_MODE 상태: {DEBUG_MODE}\n")

    # 2. 대화형 AI 인터랙션 진입
    print("🤖 대화형 AI 테스트 모드로 진입합니다...")
    run_interactive_chat()
```

# 📄 [요청 4 ➡️ 불러온함수 (main 본체)] TARGET: start.py (82-201라인)
# ----------------------------------------------------------
```python
def main():
    print("======================================================================")
    print("🔥 [Jjap-Cursor Launchpad] 짭커서 통합 마스터 사령탑 기동 시작!")
    print(f"📂 프로젝트 루트: {ROOT_DIR}")
    print(f"🤖 매칭된 파이썬 사령관: {TARGET_PYTHON}")
    print("======================================================================")

    # 🚚 [0단계 이전] 원샷 폴더 이전 마이그레이션 선제 가동
    print("----------------------------------------------------------------------")

    # 🛠️ watchdog 자동 검사 및 누락 시 핀포인트 자동 설치
    auto_install_dependencies()
    print("----------------------------------------------------------------------")

    # 🚀 [0-A단계: 선제 청소 및 동적 복제 리빌드 발동]
    print("----------------------------------------------------------------------")

    # 환경변수 세팅 복사 및 조립 (import 크래시 방지 및 실시간 무버퍼 강제)
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.pathsep.join([str(ROOT_DIR), str(CLINE_TOOLS_DIR), env.get("PYTHONPATH", "")])
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    # 🔥 [0-B단계: 최신 코드로 완벽 채워진 src/ 폴더 순정 인덱싱 메커니즘 가동]
    print("➡️ 0단계: 기동 전 AI 초경량 요약 지도(AI_CODEBASE_MAP.md) 선제 강제 빌드...")
    if CREATE_AI_MAP_SCRIPT.exists():
        try:
            # 1단계 인덱서 선제 요격 가동
            indexer_script = CLINE_TOOLS_DIR / "indexer.py"
            if indexer_script.exists():
                subprocess.run(
                    [TARGET_PYTHON, "-c", "from indexer import AdvancedIndexerV2; from pathlib import Path; AdvancedIndexerV2(Path('.')).scan_project()"],
                    cwd=str(ROOT_DIR),
                    env=env,
                    check=True,
                    stdout=subprocess.DEVNULL
                )
            
            # 2단계 AI 마스터 지도 제작 실행
            subprocess.run(
                [TARGET_PYTHON, str(CREATE_AI_MAP_SCRIPT)],
                cwd=str(ROOT_DIR),
                env=env,
                check=True
            )
        except Exception as e:
            print(f"⚠️ [경고] 초도 AI 맵 생산 중 경미한 지연 또는 예외 발생 (워처 가동 시 자동 회복 예정): {e}")
    else:
        print(f"⚠️ [경고] {CREATE_AI_MAP_SCRIPT.name} 스크립트를 찾을 수 없어 0단계를 건너뜁니다.")
    print("----------------------------------------------------------------------")

    # 📡 1단계: 실시간 백그라운드 워처(jjap_watcher.py) 가동
    print("➡️ 1단계: 실시간 백그라운드 자동 감시망(Watcher) 투입 중...")
    
    if not WATCHER_SCRIPT.exists():
        print(f"❌ [경로 에러] 워처 스크립트가 지정된 궤도에 존재하지 않습니다: {WATCHER_SCRIPT}")
        return

    # ⚡ DEBUG_MODE가 False면 DEVNULL로 출력을 완전히 차단하여 부모 터미널의 IO 병목 현상을 방지합니다.
    watcher_process = subprocess.Popen(
        [TARGET_PYTHON, str(WATCHER_SCRIPT)],
        cwd=str(ROOT_DIR),
        env=env,
        stdout=sys.stdout if DEBUG_MODE else subprocess.DEVNULL,
        stderr=sys.stderr if DEBUG_MODE else subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    
    time.sleep(1.0)  # 워처 안착용 시동 대기 타임 보정
    
    if watcher_process.poll() is None:
        print("✅ [SUCCESS] 감시망이 백그라운드 메모리에 안착 후 정상 동작 중입니다.")
    else:
        print(f"❌ [기동 즉사] 감시망 프로세스가 실행 즉시 사망했습니다. (리턴코드: {watcher_process.poll()})")
        print("💡 상단에 출력된 파이썬 문법/모듈 에러 내역을 추적하십시오.")
        return

    # 🧠 2단계: 에이전트 네비게이터(agent_navigator.py) GUI 창 띄우기
    print("➡️ 2단계: 세맨틱 네비게이터 검색기(GUI) 전면 배치 중...")
    if not NAVIGATOR_SCRIPT.exists():
        print(f"❌ [경로 에러] 네비게이터 GUI 스크립트가 없습니다: {NAVIGATOR_SCRIPT}")
        watcher_process.terminate()
        return
        
    print("💡 [안내] 검색기 창을 닫으면 백그라운드 감시망도 함께 안전하게 종료됩니다.")
    print("----------------------------------------------------------------------")
    
    try:
        subprocess.run(
            [TARGET_PYTHON, str(NAVIGATOR_SCRIPT)],
            cwd=str(ROOT_DIR),
            env=env,
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 [사용자 중단] 터미널에서 종료 신호를 수신했습니다.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ [런타임 사고] 검색기(GUI) 내부에서 무단 크래시 예외 발생! 리턴코드: {e.returncode}")
    except Exception as e:
        print(f"\n❌ [런타임 사고] 검색기 실행 중 치명적 시스템 오류 발생: {e}")
    finally:
        # 🧼 3단계: 청소 작전
        print("----------------------------------------------------------------------")
        print("🧼 3단계: 검색기 종료 감지 -> 백그라운드 감시망 자원 회수(종료) 중...")
        try:
            if watcher_process.poll() is None:
                watcher_process.terminate()
                watcher_process.wait(timeout=3)
                print("✅ [CLEANUP] 백그라운드 프로세스가 안전하게 전원 종료되었습니다.")
            else:
                print("ℹ️ [CLEANUP] 백그라운드 감시망 프로세스가 이미 종료되어 있습니다.")
        except Exception as ex:
            if DEBUG_MODE:
                print(f"🔍 [디버그] 자원 정리 중 내부 예외 유출: {ex}")
            watcher_process.kill()
            print("⚡ [FORCE KILL] 프로세스를 강제 종료 처리했습니다.")
            
    print("======================================================================")
    print("🏁 [Jjap-Cursor] 마스터 사령탑 철수 완료. 깔끔하게 정리되었습니다!")
    print("======================================================================")
```

# 📄 [요청 4 ➡️ 불러온함수 (main 본체)] TARGET: extraction_target_project/package.json (6-6라인)
# ----------------------------------------------------------
```python
  "main": "index.js",
```

# 📄 [요청 4 ➡️ 불러온함수 (main 본체)] TARGET: tools/universal_indexer/jjap_retriever.py (139-147라인)
# ----------------------------------------------------------
```python
def main():
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    if not query:
        print("💡 Usage: python cline_tools/jjap_retriever.py <symbol_id_or_name>")
        return
    
    retriever = JjapRetriever(Path.cwd())
    print(retriever.retrieve_symbol(query))
```

# 📄 [요청 4 ➡️ 불러온함수 (main 본체)] TARGET: tools/universal_indexer/jjap_watcher.py (128-154라인)
# ----------------------------------------------------------
```python
def main():
    print("=" * 70)
    print("🚀 [Jjap-Cursor Watcher] 실시간 백그라운드 감시망 기동!")
    print(f"📂 감시 대상 진짜 루트 절대 경로: {PROJECT_ROOT}")
    print(f"⚙️  초정밀 디버깅 모드 상태: {'🔴 ON' if DEBUG_MODE else '⚪ OFF'}")
    print("💡 소스코드를 수정하고 저장(Ctrl+S)하면 AI 초경량 지도가 무한 자동 갱신됩니다.")
    print("=" * 70)
    
    # 초도 기동 시 장부가 없을 수 있으므로 파이프라인 1회 선제 타격 가동
    run_pipeline()
    
    try:
        from watchdog.observers.polling import PollingObserver as Observer
    except ImportError:
        from watchdog.observers import Observer

    event_handler = CodeChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(PROJECT_ROOT), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

# 📄 [요청 4 🔗 제이슨연동 (load_all_symbols 호출처 -> tools/universal_indexer/create_ai_map.py의 [main])] TARGET: tools/universal_indexer/create_ai_map.py (186-317라인)
# ----------------------------------------------------------
```python
def main():
    scan_mode = get_scan_mode()
    target_files = collect_target_files()
    jjap_context = load_jjap_context()
    symbols_by_file, symbol_by_id = load_all_symbols()  # 💡 심볼 장부 로드 추가
    path_to_registry, path_to_protocol = parse_protocols_and_registries()

    AI_MAP_MD_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(AI_MAP_MD_PATH, "w", encoding="utf-8") as f:
        printed_dirs = set()

        f.write("# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)\n\n")
        f.write("> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.\n")
        f.write("> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.\n\n")
        
        if scan_mode == "EXTRACTION_TARGET_PROJECT":
            f.write("```markdown\nextraction_target_project/\n")
        else:
            f.write("```markdown\nproject_root/\n")
        
        for file_path in target_files:
            rel_path = file_path.relative_to(PROJECT_ROOT)
            posix_rel_path = rel_path.as_posix()
            file_name = file_path.name

            if scan_mode == "EXTRACTION_TARGET_PROJECT" and posix_rel_path.startswith("extraction_target_project/"):
                display_path = posix_rel_path[26:]
            else:
                display_path = posix_rel_path

            parts = Path(display_path).parts
            for i in range(len(parts) - 1):
                current_dir_path = Path(*parts[:i + 1]).as_posix()
                if current_dir_path not in printed_dirs:
                    printed_dirs.add(current_dir_path)
                    indent = "│   " * i
                    f.write(f"{indent}├── {parts[i]}/\n")

            indent = "│   " * (len(parts) - 1)

            file_meta = jjap_context.get(posix_rel_path, {})
            symbols_info = file_meta.get("symbols_summary", "")

            if not symbols_info and posix_rel_path.startswith("extraction_target_project/extraction_target_project/"):
                shorter_path = posix_rel_path.replace("extraction_target_project/extraction_target_project/", "extraction_target_project/", 1)
                symbols_info = jjap_context.get(shorter_path, {}).get("symbols_summary", "")

            if symbols_info:
                f.write(f"{indent}├── {file_name} [📂 {display_path}] -> [{symbols_info}]\n")
            else:
                f.write(f"{indent}├── {file_name} [📂 {display_path}]\n")

            if posix_rel_path in path_to_registry:
                for reg_const in path_to_registry[posix_rel_path]:
                    f.write(f"{indent}│     ├── 🔑 [REGISTRY]: \"{reg_const}\"\n")

            if posix_rel_path in path_to_protocol:
                for proto_name, fields in path_to_protocol[posix_rel_path]:
                    f.write(f"{indent}│     ├── 📊 [PROTOCOL]: \"{proto_name}\"\n")
                    field_items = [
                        f"{k}({v.replace(' (기본값: ', ':').replace(')', '')})"
                        for k, v in fields.items()
                    ]
                    chunks = [field_items[x:x + 4] for x in range(0, len(field_items), 4)]
                    for chunk in chunks:
                        f.write(f"{indent}│     │     ├── {', '.join(chunk)}\n")

# 🎯 [알맹이 보강] 정밀 심볼 트리 (클래스/함수/인자/줄범위/CALLS/USED_BY) 생성
            file_symbols = symbols_by_file.get(posix_rel_path, [])
            for sym in file_symbols:
                sym_type = sym.get("type", "function")
                sym_name = sym.get("name", "")
                full_name = sym.get("full_name", sym_name)
                if not sym_name:
                    continue

                # 1. 인자(Arguments) 복원 (args 리스트 또는 raw 파라미터 대응)
                raw_args = sym.get("args")
                if isinstance(raw_args, list):
                    args_str = f"({', '.join(raw_args)})" if raw_args else ""
                elif isinstance(raw_args, str) and raw_args:
                    args_str = f"({raw_args})"
                else:
                    args_str = ""

                # 2. 줄범위(Start Line - End Line) 계산
                start_line = sym.get("start_line")
                end_line = sym.get("end_line")
                if start_line and end_line and start_line != end_line:
                    line_str = f"[L{start_line}-L{end_line}]"
                elif start_line:
                    line_str = f"[L{start_line}]"
                else:
                    line_str = ""

                # 3. 타입별 아이콘 및 표현 구분
                if sym_type == "class":
                    icon_str = f"🧬 class {sym_name}"
                elif sym_type == "json_key":
                    icon_str = f"🔑 key \"{sym_name}\""
                elif sym_type == "method" or "." in full_name:
                    icon_str = f"🎯 def {sym_name}{args_str if args_str else '()'}"
                else:
                    icon_str = f"🎯 def {sym_name}{args_str if args_str else '()'}"

                f.write(f"{indent}│   ├── {icon_str} {line_str}\n".rstrip() + "\n")

                # 4. 호출 관계 (CALLS)
                calls = sym.get("calls", [])
                if calls:
                    f.write(f"{indent}│   │   ├── 📞 [CALLS]: {', '.join(calls)}\n")

                # 5. 역방향 참조 관계 (USED BY)
                used_by_ids = sym.get("used_by", [])
                if used_by_ids:
                    used_by_info = []
                    for u_id in used_by_ids:
                        target = symbol_by_id.get(u_id)
                        if target:
                            u_file = target.get("file") or target.get("path", "")
                            u_name = target.get("name", "")
                            # 동일 파일 내 호출이면 함수명만, 타 파일이면 파일 경로 포함
                            if u_file == posix_rel_path:
                                used_by_info.append(f"::{u_name}")
                            else:
                                used_by_info.append(f"{u_file}::{u_name}")
                        else:
                            used_by_info.append(str(u_id))
                    f.write(f"{indent}│   │   ├── 🔗 [USED BY]: {', '.join(used_by_info)}\n")

    print("🎯 [마스터 공장] 'system_maps/AI_CODEBASE_MAP.md'가 (인자, calls, used_by 관계망 포함) 정밀 자동 갱신되었습니다!")
```

# 📄 [요청 5] TARGET: tools/universal_indexer/update_map.py (1-103라인)
# ----------------------------------------------------------
```python
import json
from pathlib import Path

def update_map():
    # 🔄 [안전 보장] 실행 환경에 구애받지 않도록 현재 스크립트 위치 기준 진짜 프로젝트 마스터 루트를 추적합니다.
    SCRIPT_DIR = Path(__file__).parent.resolve()
    if SCRIPT_DIR.name == "universal_indexer" and SCRIPT_DIR.parent.name == "tools":
        PROJECT_ROOT = SCRIPT_DIR.parent.parent
    else:
        PROJECT_ROOT = SCRIPT_DIR

    # 🧠 마스터 루트 기준으로 경로를 확실하게 조준하여 불러오기 및 출력을 고정합니다.
    context_file = PROJECT_ROOT / "system_memory" / ".jjap_context.json"
    symbols_file = PROJECT_ROOT / "system_memory" / ".jjap_symbols.json"
    output_file = PROJECT_ROOT / "system_maps" / "CODEBASE_MAP.md"
    
    if not context_file.exists() or not symbols_file.exists():
        print("❌ Error: 인덱서 데이터 파일(.jjap_context 또는 .jjap_symbols)이 없습니다.")
        print("💡 해결책: 인덱서(indexer.py)를 먼저 실행한 뒤 이 스크립트를 돌리세요.")
        return

    # 1. 최신 데이터 로드
    with open(context_file, "r", encoding="utf-8") as f:
        context_data = json.load(f).get("files", {})
        
    with open(symbols_file, "r", encoding="utf-8") as f:
        symbols_list = json.load(f).get("symbols", [])

    # 🚨 [검열 시스템 동기화] 인덱서와 싱크로율 100% 맞추기
    # 혹시라도 장부에 흔적이 남아있거나, 루트의 실행 파일들이 맵에 찍히는 걸 원천 차단합니다.
    # 🚨 [검열 시스템 동기화] 인덱서 및 기타 도구들과 검열 필터 규격 100% 동기화
    EXCLUDE_KEYWORDS = [
        "node_modules",
        ".venv", 
        ".git", 
        "__pycache__", 
        "cline_tools", 
        "system_memory", 
        "system_maps"
    ]

    # 2. 에이전트 분석을 돕기 위해 파일별 심볼 및 관계 매핑 구조 생성
    symbols_by_file = {}
    for s in symbols_list:
        file_path = s.get("file", "")
        
        # 🚨 검열 컷 1: 심볼 리스트 중에 제외 폴더나 start.py가 있으면 장부에서 누락 처리
        if any(p in file_path for p in EXCLUDE_KEYWORDS) or "start.py" in file_path:
            continue
            
        if file_path not in symbols_by_file:
            symbols_by_file[file_path] = []
        symbols_by_file[file_path].append(s)

    # 3. CODEBASE_MAP.md 최종 렌더링
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 🏗️ 짭커서 프로젝트 CODEBASE MAP\n\n")
        
        # 🚨 검열 컷 2: 순수 유효 파일만 발라내기 (start.py 및 도구 폴더 완전히 소멸시킴)
        valid_files = {}
        for path, info in context_data.items():
            if any(p in path for p in EXCLUDE_KEYWORDS) or "start.py" in path:
                continue
            valid_files[path] = info

        f.write(f"현재 인덱싱된 총 파일 수: **{len(valid_files)}개**\n\n")
        
        # 📂 모듈 인덱스 구역
        f.write("## 🗂️ [Module Index]\n")
        for path in sorted(valid_files.keys()):
            f.write(f"- `{path}`\n")
        
        # 💀 뼈대 및 의존성 관계 상세 구역
        f.write("\n## 💀 [Skeleton & Dependency 명세서]\n")
        for path, info in sorted(valid_files.items()):
            f.write(f"### 📄 {path}\n")
            
            # 해당 파일에 속한 상세 심볼(클래스/함수)의 호출 관계 먼저 요약
            file_symbols = symbols_by_file.get(path, [])
            if file_symbols:
                f.write("#### 🔍 내부 심볼 및 의존성 관계:\n")
                for s in file_symbols:
                   # 수정 코드: s['full_name']을 s['name']으로 변경
                    f.write(f"- **[{s['type'].upper()}]** `{s['name']}` (Line: {s['start_line']}~{s['end_line']})\n")
                    if s.get("calls"):
                        f.write(f"  - 🔗 *Calls (호출하는 것)*: `{', '.join(s['calls'])}`\n")
                    if s.get("used_by"):
                        f.write(f"  - 🎯 *Used By (나를 부르는 곳)*: `{', '.join(s['used_by'])}`\n")
                f.write("\n")

            # 실제 코드 뼈대(Skeleton) 출력
            skeleton_text = info.get("skeleton", "").strip()
            if skeleton_text:
                f.write("#### 🧱 Code Skeleton:\n")
                f.write("```python\n")
                f.write(f"{skeleton_text}\n")
                f.write("```\n\n")
            else:
                f.write("*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*\n\n")
                
            f.write("-" * 50 + "\n\n")

    print(f"✅ [SUCCESS] V2 인덱스 정밀 데이터를 결합하여 {output_file.name} 업데이트 완료! (스텔스 필터 적용)")
```

# 📄 [요청 6] TARGET: tools/universal_indexer/agent_navigator.py (1-280라인)
# ----------------------------------------------------------
```python
import json
import re
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# =====================================================================
# 🧠 CORE INTELLIGENCE: UI 내장 독립형 CODE EXTRACTOR
# =====================================================================
class CodeExtractor:
    """
    UI(Navigator) 전용 독립 코드 추출기
    - agent_code_extractor.py의 수정 및 위치 변경에 절대 영향을 받지 않는 독자 엔진
    """
    def __init__(self, root_dir: str | Path):
        self.raw_root_dir = Path(root_dir).resolve()
        self.scan_mode = "ROOT"
        
        try:
            idx_path = str((self.raw_root_dir / "tools" / "universal_indexer").resolve())
            if idx_path not in sys.path:
                sys.path.insert(0, idx_path)
            
            import switch
            self.scan_mode = getattr(switch, "SCAN_MODE", "ROOT")
            print(f"🎛️ [SWITCH DETECTED] 현재 탐색 스위치 모드: {self.scan_mode}")
        except Exception as e:
            print(f"⚠️ [SWITCH WARNING] switch.py를 로드하지 못해 기본 'ROOT' 모드로 동작합니다. (이유: {e})")

        if self.scan_mode == "SRC":
            self.root_dir = self.raw_root_dir / "src"
            print(f"📁 [MODE: SRC] 탐색 마스터 루트가 복사/격리용 src 폴더로 변경되었습니다: {self.root_dir}")
        else:
            self.root_dir = self.raw_root_dir
            print(f"📁 [MODE: ROOT] 탐색 마스터 루트가 프로젝트 원본 루트로 설정되었습니다: {self.root_dir}")

        self.symbols_path = self.raw_root_dir / "system_memory" / ".jjap_symbols.json"
        self.symbols_data = self._load_database()

    def _load_database(self) -> dict:
        if not self.symbols_path.exists():
            return {"symbols": []}
        try:
            with open(self.symbols_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"symbols": []}

    def resolve_file_path(self, raw_path_str: str) -> Path | None:
        clean_path_str = raw_path_str.strip().replace("\\", "/")
        
        if self.scan_mode == "SRC":
            if clean_path_str.startswith("src/src/"):
                candidate = self.raw_root_dir / clean_path_str
            elif clean_path_str.startswith("src/"):
                candidate = self.raw_root_dir / clean_path_str
            else:
                candidate = self.raw_root_dir / "src" / clean_path_str
        else:
            candidate = self.raw_root_dir / clean_path_str

        if candidate.exists() and candidate.is_file():
            return candidate

        candidate_raw = self.raw_root_dir / clean_path_str
        if candidate_raw.exists() and candidate_raw.is_file():
            return candidate_raw

        candidate_target = self.raw_root_dir / "extraction_target_project" / clean_path_str
        if candidate_target.exists() and candidate_target.is_file():
            return candidate_target

        candidate_tools = self.raw_root_dir / "tools" / clean_path_str
        if candidate_tools.exists() and candidate_tools.is_file():
            return candidate_tools

        return None

    def extract_multi_slices(self, raw_prompt: str) -> list[dict]:
        print("\n" + "="*60)
        print("🚨 [EXTRACTOR ON] 멀티 슬라이싱 파이프라인 기동!!!")
        print(f"📥 유저 입력 프롬프트: {repr(raw_prompt)}")
        print(f"⚙️ 현재 매핑 모드: {self.scan_mode} (기준 경로: {self.root_dir})")
        print("="*60)

        pattern = r"([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\s:]+(?:L)?(\d+)(?:\s*-\s*(?:L)?(\d+))?"
        matches = re.findall(pattern, raw_prompt)

        print(f"🔍 정규식 1차 타겟 스캔 결과: {matches}")
        if not matches:
            print("⚠️ 매칭되는 파일 경로 및 라인 규격이 없습니다. 빈 배열 리턴.")
            return []

        extracted_slices = []
        req_num = 1

        for match in matches:
            file_rel_path = match[0].strip().replace("\\", "/")
            start_line = int(match[1])
            end_line = int(match[2]) if match[2] else start_line

            print(f"\n🎯 [요청 #{req_num}] 메인 타겟 분석 시작 -> {file_rel_path} ({start_line} ~ {end_line} 라인)")

            target_file_path = self.resolve_file_path(file_rel_path)
            
            if not target_file_path:
                print(f"   ❌ [ERROR] 해당 파일이 실제 경로에 존재하지 않습니다! 패스합니다: {file_rel_path}")
                continue

            print(f"   🟢 [경로 확정] 디스크 실체 발견: {target_file_path}")

            try:
                with open(target_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                total_lines = len(lines)
                safe_start = max(1, min(start_line, total_lines))
                safe_end = max(safe_start, min(end_line, total_lines))
                print(f"   📏 파일 전체 줄 수: {total_lines} | 보정된 안전 범위: {safe_start} ~ {safe_end}")

                slice_lines = lines[safe_start - 1 : safe_end]
                slice_code = "".join(slice_lines)
                print(f"   🟢 1차 메인 슬라이싱 성공 (길이: {len(slice_code)}자)")

                extracted_slices.append({
                    "req_num": f"{req_num}",
                    "file": file_rel_path,
                    "line_range": f"{safe_start}-{safe_end}",
                    "code": slice_code
                })

                print(f"   📡 [2차 사냥기] 잘려 나온 텍스트 내부에서 양방향 심볼 식별 개시...")

                defined_names = re.findall(r"(?:def|class)\s+([a-zA-Z0-9_]+)", slice_code)
                called_names = re.findall(r"(?:[a-zA-Z0-9_]+\.)?([a-zA-Z0-9_]+)\s*\(", slice_code)
                file_ref_names = [f for f in re.findall(r'[\'"]([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\'"]', slice_code) if f != file_rel_path]

                builtin_filters = {"print", "len", "range", "open", "dict", "list", "set", "any", "all", "max", "min", "append", "get", "strip", "split", "exists", "readlines", "join"}
                filtered_called_names = [name for name in called_names if name not in builtin_filters]

                target_symbols = list(set(defined_names + filtered_called_names + file_ref_names))
                print(f"   📦 [양방향 통합] 징집 대상 심볼 목록: {target_symbols}")
                
                symbols_list = self.symbols_data.get("symbols", [])
                print(f"   📚 로드된 JSON 장부 총 심볼 개수: {len(symbols_list)}개")

                for target_name in target_symbols:
                    print(f"      🔎 [전역 심볼 대조] 이름: '{target_name}' -> 장부 전체 스캔 중...")
                    match_found = False
                    
                    for s in symbols_list:
                        if s.get("name") == target_name:
                            match_found = True
                            t_file = s.get("path") or s.get("file", "")
                            s_start = s.get("start_line", 1)
                            s_end = s.get("end_line", 1)

                            if t_file != file_rel_path:
                                print(f"         ➡️ [정방향] 내가 불러온 함수 본체 포착 -> {t_file} ({s_start}~{s_end}라인)")
                                callee_file_path = self.resolve_file_path(t_file)
                                    
                                if callee_file_path:
                                    with open(callee_file_path, "r", encoding="utf-8") as cf:
                                        cf_lines = cf.readlines()
                                    
                                    s_start = max(1, min(s_start, len(cf_lines)))
                                    s_end = max(s_start, min(s_end, len(cf_lines)))
                                    callee_code = "".join(cf_lines[s_start - 1 : s_end])
                                    
                                    if not any(x["file"] == t_file and x["line_range"] == f"{s_start}-{s_end}" for x in extracted_slices):
                                        extracted_slices.append({
                                            "req_num": f"{req_num} ➡️ 불러온함수 ({target_name} 본체)",
                                            "file": t_file,
                                            "line_range": f"{s_start}-{s_end}",
                                            "code": callee_code
                                        })

                            if (target_name in defined_names) or (t_file == file_rel_path):
                                ub_list = s.get("used_by", [])
                                if ub_list:
                                    print(f"         ⬅️ [역방향] 나를 부르는 전역 호출처 목록(used_by): {ub_list}")
                                    for ub_id in ub_list:
                                        if "::" in ub_id:
                                            ub_file, ub_symbol_name = ub_id.split("::", 1)
                                            if "." in ub_symbol_name:
                                                ub_symbol_name = ub_symbol_name.split(".")[-1]
                                            
                                            sub_match_found = False
                                            for target_s in symbols_list:
                                                sub_t_file = target_s.get("path") or target_s.get("file", "")
                                                s_id = target_s.get("symbol_id", "")
                                                sub_s_name = target_s.get("name", "")
                                                
                                                if (s_id == ub_id) or (ub_id.endswith(s_id)) or (sub_s_name == ub_symbol_name and (sub_t_file == ub_file or ub_file.endswith(sub_t_file) or sub_t_file.endswith(ub_file))):
                                                    sub_match_found = True
                                                    ub_file_path = self.resolve_file_path(sub_t_file)
                                                        
                                                    if ub_file_path:
                                                        with open(ub_file_path, "r", encoding="utf-8") as ubf:
                                                            ub_lines = ubf.readlines()
                                                        
                                                        ubs_start = max(1, min(target_s.get("start_line", 1), len(ub_lines)))
                                                        ubs_end = max(ubs_start, min(target_s.get("end_line", len(ub_lines)), len(ub_lines)))
                                                        ub_slice_code = "".join(ub_lines[ubs_start - 1 : ubs_end])
                                                        
                                                        if not any(x["file"] == sub_t_file and x["line_range"] == f"{ubs_start}-{ubs_end}" for x in extracted_slices):
                                                            extracted_slices.append({
                                                                "req_num": f"{req_num} 🔗 제이슨연동 ({target_name} 호출처 -> {sub_t_file}의 [{sub_s_name}])",
                                                                "file": sub_t_file,
                                                                "line_range": f"{ubs_start}-{ubs_end}",
                                                                "code": ub_slice_code
                                                            })
                                            if not sub_match_found:
                                                print(f"            ❌ [ERROR] 호출처 구조체 '{ub_id}'를 장부에서 찾지 못했습니다.")
                    
                    if not match_found:
                        print(f"      ❓ [NOT FOUND] 코드엔 찍혀있는데 JSON 장부({file_rel_path})엔 등록 안 된 심볼입니다.")

            except Exception as e:
                import traceback
                print(f"💥 [CRITICAL ERROR] 슬라이싱 중 예외 발생: {e}")
                traceback.print_exc()

            req_num += 1

        print("\n" + "="*60)
        print(f"🏁 최종 반환할 총 슬라이스 묶음 개수: {len(extracted_slices)}개")
        print("="*60 + "\n")
        return extracted_slices

    def format_as_markdown(self, extracted_slices: list[dict]) -> str:
        if not extracted_slices:
            return ""

        md_lines = []
        md_lines.append("# ==========================================================================")
        md_lines.append("# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드")
        md_lines.append(f"# [SCAN_MODE] {self.scan_mode}")
        md_lines.append("# ==========================================================================")

        for slc in extracted_slices:
            md_lines.append(f"# 📄 [요청 {slc['req_num']}] TARGET: {slc['file']} ({slc['line_range']}라인)")
            md_lines.append("# ----------------------------------------------------------")
            md_lines.append("```python")
            md_lines.append(slc["code"].rstrip())
            md_lines.append("```\n")

        return "\n".join(md_lines)

    def process(self, raw_prompt: str, auto_save: bool = True, output_path: str | Path = None) -> dict:
        slices = self.extract_multi_slices(raw_prompt)
        markdown_text = self.format_as_markdown(slices)
        save_target_path = None

        if auto_save and markdown_text:
            if output_path:
                save_target_path = Path(output_path)
            else:
                save_target_path = self.raw_root_dir / "system_maps" / "extracted_context.md"

            try:
                save_target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_target_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)
                print(f"💾 마크다운 데이터가 안전하게 저장되었습니다: {save_target_path}")
            except Exception as e:
                print(f"⚠️ 파일 저장 실패: {e}")

        return {
            "slices": slices,
            "markdown": markdown_text,
            "saved_path": save_target_path
```

# 📄 [요청 6 ➡️ 불러온함수 (CodeExtractor 본체)] TARGET: tools/multi_agent_system/agent_code_extractor.py (16-313라인)
# ----------------------------------------------------------
```python
class CodeExtractor:
    """
    AI 에이전트 및 파이프라인 전용 코드 정밀 추출기 (Headless Code Extractor)
    - UI(Tkinter 등) 요소를 완전히 제거하고 순수 데이터 처리 및 정보 흐름만 수행
    - 기존 SemanticNavigator의 슬라이싱, 경로 구제, 양방향 심볼 연관 추적 로직 100% 보존
    """
    def __init__(self, root_dir: str | Path):
        self.raw_root_dir = Path(root_dir).resolve()
        self.scan_mode = "ROOT"
        
        # 🎛️ [SCAN_MODE 스위치 반영 - universal_indexer/switch.py 절대 위치 고정]
        try:
            idx_path = str((self.raw_root_dir / "tools" / "universal_indexer").resolve())
            if idx_path not in sys.path:
                sys.path.insert(0, idx_path)
            
            import switch
            self.scan_mode = getattr(switch, "SCAN_MODE", "ROOT")
            print(f"🎛️ [SWITCH DETECTED] 현재 탐색 스위치 모드: {self.scan_mode}")
        except Exception as e:
            print(f"⚠️ [SWITCH WARNING] switch.py를 로드하지 못해 기본 'ROOT' 모드로 동작합니다. (이유: {e})")

        # 🚀 SRC 모드일 경우 하드디스크 탐색 기준점(self.root_dir)에 'src' 폴더를 강제 결합
        if self.scan_mode == "SRC":
            self.root_dir = self.raw_root_dir / "src"
            print(f"📁 [MODE: SRC] 탐색 마스터 루트가 복사/격리용 src 폴더로 변경되었습니다: {self.root_dir}")
        else:
            self.root_dir = self.raw_root_dir
            print(f"📁 [MODE: ROOT] 탐색 마스터 루트가 프로젝트 원본 루트로 설정되었습니다: {self.root_dir}")

        # 🧠 [불러오기 교정] 장부 정보는 언제나 프로젝트의 실제 본체 루트(raw_root_dir) 기준으로 가져옵니다.
        self.symbols_path = self.raw_root_dir / "system_memory" / ".jjap_symbols.json"
        self.symbols_data = self._load_database()

    def _load_database(self) -> dict:
        if not self.symbols_path.exists():
            return {"symbols": []}
        try:
            with open(self.symbols_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"symbols": []}

    def resolve_file_path(self, raw_path_str: str) -> Path | None:
        """
        [경로 구제 통합 레이더]
        SCAN_MODE, 상대 경로, extraction_target_project, tools 등 
        다양한 디렉토리 변수를 추적하여 실제 존재하는 파일의 Absolute Path를 반환합니다.
        """
        clean_path_str = raw_path_str.strip().replace("\\", "/")
        
        # 1차 시도: 모드별 스펙에 맞춘 경로 조립
        if self.scan_mode == "SRC":
            if clean_path_str.startswith("src/src/"):
                candidate = self.raw_root_dir / clean_path_str
            elif clean_path_str.startswith("src/"):
                candidate = self.raw_root_dir / clean_path_str
            else:
                candidate = self.raw_root_dir / "src" / clean_path_str
        else:
            candidate = self.raw_root_dir / clean_path_str

        if candidate.exists() and candidate.is_file():
            return candidate

        # 2차 시도 (구제금융): raw_root_dir 기준 직접 탐색
        candidate_raw = self.raw_root_dir / clean_path_str
        if candidate_raw.exists() and candidate_raw.is_file():
            return candidate_raw

        # 3차 시도 (구제금융): extraction_target_project 하위 탐색
        candidate_target = self.raw_root_dir / "extraction_target_project" / clean_path_str
        if candidate_target.exists() and candidate_target.is_file():
            return candidate_target

        # 4차 시도 (구제금융): tools 하위 탐색
        candidate_tools = self.raw_root_dir / "tools" / clean_path_str
        if candidate_tools.exists() and candidate_tools.is_file():
            return candidate_tools

        return None

    def extract_multi_slices(self, raw_prompt: str) -> list[dict]:
        """
        [Multi-Target Protocol Parser - 정규식 통합 및 경로 구제 완전판]
        프롬프트를 파싱하여 코드 슬라이스 묶음(list of dict)을 리턴합니다.
        """
        print("\n" + "="*60)
        print("🚨 [EXTRACTOR ON] 멀티 슬라이싱 파이프라인 기동!!!")
        print(f"📥 유저 입력 프롬프트: {repr(raw_prompt)}")
        print(f"⚙️ 현재 매핑 모드: {self.scan_mode} (기준 경로: {self.root_dir})")
        print("="*60)

        pattern = r"([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\s:]+(?:L)?(\d+)(?:\s*-\s*(?:L)?(\d+))?"
        matches = re.findall(pattern, raw_prompt)

        print(f"🔍 정규식 1차 타겟 스캔 결과: {matches}")
        if not matches:
            print("⚠️ 매칭되는 파일 경로 및 라인 규격이 없습니다. 빈 배열 리턴.")
            return []

        extracted_slices = []
        req_num = 1

        for match in matches:
            file_rel_path = match[0].strip().replace("\\", "/")
            start_line = int(match[1])
            end_line = int(match[2]) if match[2] else start_line

            print(f"\n🎯 [요청 #{req_num}] 메인 타겟 분석 시작 -> {file_rel_path} ({start_line} ~ {end_line} 라인)")

            target_file_path = self.resolve_file_path(file_rel_path)
            
            if not target_file_path:
                print(f"   ❌ [ERROR] 해당 파일이 실제 경로에 존재하지 않습니다! 패스합니다: {file_rel_path}")
                continue

            print(f"   🟢 [경로 확정] 디스크 실체 발견: {target_file_path}")

            try:
                with open(target_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                total_lines = len(lines)
                safe_start = max(1, min(start_line, total_lines))
                safe_end = max(safe_start, min(end_line, total_lines))
                print(f"   📏 파일 전체 줄 수: {total_lines} | 보정된 안전 범위: {safe_start} ~ {safe_end}")

                slice_lines = lines[safe_start - 1 : safe_end]
                slice_code = "".join(slice_lines)
                print(f"   🟢 1차 메인 슬라이싱 성공 (길이: {len(slice_code)}자)")

                extracted_slices.append({
                    "req_num": f"{req_num}",
                    "file": file_rel_path,
                    "line_range": f"{safe_start}-{safe_end}",
                    "code": slice_code
                })

                # [2단계] 🔗 제이슨 기반 2차 심볼 탐색기 가동
                print(f"   📡 [2차 사냥기] 잘려 나온 텍스트 내부에서 양방향 심볼 식별 개시...")

                defined_names = re.findall(r"(?:def|class)\s+([a-zA-Z0-9_]+)", slice_code)
                called_names = re.findall(r"(?:[a-zA-Z0-9_]+\.)?([a-zA-Z0-9_]+)\s*\(", slice_code)
                file_ref_names = [f for f in re.findall(r'[\'"]([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\'"]', slice_code) if f != file_rel_path]

                builtin_filters = {"print", "len", "range", "open", "dict", "list", "set", "any", "all", "max", "min", "append", "get", "strip", "split", "exists", "readlines", "join"}
                filtered_called_names = [name for name in called_names if name not in builtin_filters]

                target_symbols = list(set(defined_names + filtered_called_names + file_ref_names))
                print(f"   📦 [양방향 통합] 징집 대상 심볼 목록: {target_symbols}")
                
                symbols_list = self.symbols_data.get("symbols", [])
                print(f"   📚 로드된 JSON 장부 총 심볼 개수: {len(symbols_list)}개")

                for target_name in target_symbols:
                    print(f"      🔎 [전역 심볼 대조] 이름: '{target_name}' -> 장부 전체 스캔 중...")
                    match_found = False
                    
                    for s in symbols_list:
                        if s.get("name") == target_name:
                            match_found = True
                            t_file = s.get("path") or s.get("file", "")
                            s_start = s.get("start_line", 1)
                            s_end = s.get("end_line", 1)

                            # 정방향 연관 심볼 추적
                            if t_file != file_rel_path:
                                print(f"         ➡️ [정방향] 내가 불러온 함수 본체 포착 -> {t_file} ({s_start}~{s_end}라인)")
                                callee_file_path = self.resolve_file_path(t_file)
                                    
                                if callee_file_path:
                                    with open(callee_file_path, "r", encoding="utf-8") as cf:
                                        cf_lines = cf.readlines()
                                    
                                    s_start = max(1, min(s_start, len(cf_lines)))
                                    s_end = max(s_start, min(s_end, len(cf_lines)))
                                    callee_code = "".join(cf_lines[s_start - 1 : s_end])
                                    
                                    if not any(x["file"] == t_file and x["line_range"] == f"{s_start}-{s_end}" for x in extracted_slices):
                                        extracted_slices.append({
                                            "req_num": f"{req_num} ➡️ 불러온함수 ({target_name} 본체)",
                                            "file": t_file,
                                            "line_range": f"{s_start}-{s_end}",
                                            "code": callee_code
                                        })

                            # 역방향 연관 심볼 추적 (used_by)
                            if (target_name in defined_names) or (t_file == file_rel_path):
                                ub_list = s.get("used_by", [])
                                if ub_list:
                                    print(f"         ⬅️ [역방향] 나를 부르는 전역 호출처 목록(used_by): {ub_list}")
                                    for ub_id in ub_list:
                                        if "::" in ub_id:
                                            ub_file, ub_symbol_name = ub_id.split("::", 1)
                                            if "." in ub_symbol_name:
                                                ub_symbol_name = ub_symbol_name.split(".")[-1]
                                            
                                            sub_match_found = False
                                            for target_s in symbols_list:
                                                sub_t_file = target_s.get("path") or target_s.get("file", "")
                                                s_id = target_s.get("symbol_id", "")
                                                sub_s_name = target_s.get("name", "")
                                                
                                                if (s_id == ub_id) or (ub_id.endswith(s_id)) or (sub_s_name == ub_symbol_name and (sub_t_file == ub_file or ub_file.endswith(sub_t_file) or sub_t_file.endswith(ub_file))):
                                                    sub_match_found = True
                                                    ub_file_path = self.resolve_file_path(sub_t_file)
                                                        
                                                    if ub_file_path:
                                                        with open(ub_file_path, "r", encoding="utf-8") as ubf:
                                                            ub_lines = ubf.readlines()
                                                        
                                                        ubs_start = max(1, min(target_s.get("start_line", 1), len(ub_lines)))
                                                        ubs_end = max(ubs_start, min(target_s.get("end_line", len(ub_lines)), len(ub_lines)))
                                                        ub_slice_code = "".join(ub_lines[ubs_start - 1 : ubs_end])
                                                        
                                                        if not any(x["file"] == sub_t_file and x["line_range"] == f"{ubs_start}-{ubs_end}" for x in extracted_slices):
                                                            extracted_slices.append({
                                                                "req_num": f"{req_num} 🔗 제이슨연동 ({target_name} 호출처 -> {sub_t_file}의 [{sub_s_name}])",
                                                                "file": sub_t_file,
                                                                "line_range": f"{ubs_start}-{ubs_end}",
                                                                "code": ub_slice_code
                                                            })
                                            if not sub_match_found:
                                                print(f"            ❌ [ERROR] 호출처 구조체 '{ub_id}'를 장부에서 찾지 못했습니다.")
                    
                    if not match_found:
                        print(f"      ❓ [NOT FOUND] 코드엔 찍혀있는데 JSON 장부({file_rel_path})엔 등록 안 된 심볼입니다.")

            except Exception as e:
                import traceback
                print(f"💥 [CRITICAL ERROR] 슬라이싱 중 예외 발생: {e}")
                traceback.print_exc()

            req_num += 1

        print("\n" + "="*60)
        print(f"🏁 최종 반환할 총 슬라이스 묶음 개수: {len(extracted_slices)}개")
        print("="*60 + "\n")
        return extracted_slices

    def format_as_markdown(self, extracted_slices: list[dict]) -> str:
        """
        슬라이싱 데이터 배열을 받아서 LLM 및 에이전트에 주입할 마크다운 문맥으로 변환합니다.
        """
        if not extracted_slices:
            return ""

        md_lines = []
        md_lines.append("# ==========================================================================")
        md_lines.append("# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드")
        md_lines.append(f"# [SCAN_MODE] {self.scan_mode}")
        md_lines.append("# ==========================================================================")

        for slc in extracted_slices:
            md_lines.append(f"# 📄 [요청 {slc['req_num']}] TARGET: {slc['file']} ({slc['line_range']}라인)")
            md_lines.append("# ----------------------------------------------------------")
            md_lines.append("```python")
            md_lines.append(slc["code"].rstrip())
            md_lines.append("```\n")

        return "\n".join(md_lines)

    def process(self, raw_prompt: str, auto_save: bool = True, output_path: str | Path = None) -> dict:
        """
        [통합 매니저 파이프라인]
        프롬프트를 입력받아 슬라이스를 추출하고, 마크다운 반환 및 마스터 격리 폴더로 내보냅니다.
        
        Returns:
            dict: {
                "slices": list[dict],    # 원본 데이터 객체 목록
                "markdown": str,         # 생성된 마크다운 텍스트
                "saved_path": Path|None  # 저장된 실제 경로
            }
        """
        slices = self.extract_multi_slices(raw_prompt)
        markdown_text = self.format_as_markdown(slices)
        save_target_path = None

        if auto_save and markdown_text:
            if output_path:
                save_target_path = Path(output_path)
            else:
                save_target_path = self.raw_root_dir / "system_maps" / "extracted_context.md"

            try:
                save_target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_target_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)
                print(f"💾 마크다운 데이터가 안전하게 저장되었습니다: {save_target_path}")
            except Exception as e:
                print(f"⚠️ 파일 저장 실패: {e}")

        return {
            "slices": slices,
            "markdown": markdown_text,
            "saved_path": save_target_path
        }
```

# 📄 [요청 6 ➡️ 불러온함수 (format_as_markdown 본체)] TARGET: tools/multi_agent_system/agent_code_extractor.py (257-277라인)
# ----------------------------------------------------------
```python
    def format_as_markdown(self, extracted_slices: list[dict]) -> str:
        """
        슬라이싱 데이터 배열을 받아서 LLM 및 에이전트에 주입할 마크다운 문맥으로 변환합니다.
        """
        if not extracted_slices:
            return ""

        md_lines = []
        md_lines.append("# ==========================================================================")
        md_lines.append("# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드")
        md_lines.append(f"# [SCAN_MODE] {self.scan_mode}")
        md_lines.append("# ==========================================================================")

        for slc in extracted_slices:
            md_lines.append(f"# 📄 [요청 {slc['req_num']}] TARGET: {slc['file']} ({slc['line_range']}라인)")
            md_lines.append("# ----------------------------------------------------------")
            md_lines.append("```python")
            md_lines.append(slc["code"].rstrip())
            md_lines.append("```\n")

        return "\n".join(md_lines)
```

# 📄 [요청 6 ➡️ 불러온함수 (extract_multi_slices 본체)] TARGET: tools/multi_agent_system/agent_code_extractor.py (98-255라인)
# ----------------------------------------------------------
```python
    def extract_multi_slices(self, raw_prompt: str) -> list[dict]:
        """
        [Multi-Target Protocol Parser - 정규식 통합 및 경로 구제 완전판]
        프롬프트를 파싱하여 코드 슬라이스 묶음(list of dict)을 리턴합니다.
        """
        print("\n" + "="*60)
        print("🚨 [EXTRACTOR ON] 멀티 슬라이싱 파이프라인 기동!!!")
        print(f"📥 유저 입력 프롬프트: {repr(raw_prompt)}")
        print(f"⚙️ 현재 매핑 모드: {self.scan_mode} (기준 경로: {self.root_dir})")
        print("="*60)

        pattern = r"([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\s:]+(?:L)?(\d+)(?:\s*-\s*(?:L)?(\d+))?"
        matches = re.findall(pattern, raw_prompt)

        print(f"🔍 정규식 1차 타겟 스캔 결과: {matches}")
        if not matches:
            print("⚠️ 매칭되는 파일 경로 및 라인 규격이 없습니다. 빈 배열 리턴.")
            return []

        extracted_slices = []
        req_num = 1

        for match in matches:
            file_rel_path = match[0].strip().replace("\\", "/")
            start_line = int(match[1])
            end_line = int(match[2]) if match[2] else start_line

            print(f"\n🎯 [요청 #{req_num}] 메인 타겟 분석 시작 -> {file_rel_path} ({start_line} ~ {end_line} 라인)")

            target_file_path = self.resolve_file_path(file_rel_path)
            
            if not target_file_path:
                print(f"   ❌ [ERROR] 해당 파일이 실제 경로에 존재하지 않습니다! 패스합니다: {file_rel_path}")
                continue

            print(f"   🟢 [경로 확정] 디스크 실체 발견: {target_file_path}")

            try:
                with open(target_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                total_lines = len(lines)
                safe_start = max(1, min(start_line, total_lines))
                safe_end = max(safe_start, min(end_line, total_lines))
                print(f"   📏 파일 전체 줄 수: {total_lines} | 보정된 안전 범위: {safe_start} ~ {safe_end}")

                slice_lines = lines[safe_start - 1 : safe_end]
                slice_code = "".join(slice_lines)
                print(f"   🟢 1차 메인 슬라이싱 성공 (길이: {len(slice_code)}자)")

                extracted_slices.append({
                    "req_num": f"{req_num}",
                    "file": file_rel_path,
                    "line_range": f"{safe_start}-{safe_end}",
                    "code": slice_code
                })

                # [2단계] 🔗 제이슨 기반 2차 심볼 탐색기 가동
                print(f"   📡 [2차 사냥기] 잘려 나온 텍스트 내부에서 양방향 심볼 식별 개시...")

                defined_names = re.findall(r"(?:def|class)\s+([a-zA-Z0-9_]+)", slice_code)
                called_names = re.findall(r"(?:[a-zA-Z0-9_]+\.)?([a-zA-Z0-9_]+)\s*\(", slice_code)
                file_ref_names = [f for f in re.findall(r'[\'"]([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\'"]', slice_code) if f != file_rel_path]

                builtin_filters = {"print", "len", "range", "open", "dict", "list", "set", "any", "all", "max", "min", "append", "get", "strip", "split", "exists", "readlines", "join"}
                filtered_called_names = [name for name in called_names if name not in builtin_filters]

                target_symbols = list(set(defined_names + filtered_called_names + file_ref_names))
                print(f"   📦 [양방향 통합] 징집 대상 심볼 목록: {target_symbols}")
                
                symbols_list = self.symbols_data.get("symbols", [])
                print(f"   📚 로드된 JSON 장부 총 심볼 개수: {len(symbols_list)}개")

                for target_name in target_symbols:
                    print(f"      🔎 [전역 심볼 대조] 이름: '{target_name}' -> 장부 전체 스캔 중...")
                    match_found = False
                    
                    for s in symbols_list:
                        if s.get("name") == target_name:
                            match_found = True
                            t_file = s.get("path") or s.get("file", "")
                            s_start = s.get("start_line", 1)
                            s_end = s.get("end_line", 1)

                            # 정방향 연관 심볼 추적
                            if t_file != file_rel_path:
                                print(f"         ➡️ [정방향] 내가 불러온 함수 본체 포착 -> {t_file} ({s_start}~{s_end}라인)")
                                callee_file_path = self.resolve_file_path(t_file)
                                    
                                if callee_file_path:
                                    with open(callee_file_path, "r", encoding="utf-8") as cf:
                                        cf_lines = cf.readlines()
                                    
                                    s_start = max(1, min(s_start, len(cf_lines)))
                                    s_end = max(s_start, min(s_end, len(cf_lines)))
                                    callee_code = "".join(cf_lines[s_start - 1 : s_end])
                                    
                                    if not any(x["file"] == t_file and x["line_range"] == f"{s_start}-{s_end}" for x in extracted_slices):
                                        extracted_slices.append({
                                            "req_num": f"{req_num} ➡️ 불러온함수 ({target_name} 본체)",
                                            "file": t_file,
                                            "line_range": f"{s_start}-{s_end}",
                                            "code": callee_code
                                        })

                            # 역방향 연관 심볼 추적 (used_by)
                            if (target_name in defined_names) or (t_file == file_rel_path):
                                ub_list = s.get("used_by", [])
                                if ub_list:
                                    print(f"         ⬅️ [역방향] 나를 부르는 전역 호출처 목록(used_by): {ub_list}")
                                    for ub_id in ub_list:
                                        if "::" in ub_id:
                                            ub_file, ub_symbol_name = ub_id.split("::", 1)
                                            if "." in ub_symbol_name:
                                                ub_symbol_name = ub_symbol_name.split(".")[-1]
                                            
                                            sub_match_found = False
                                            for target_s in symbols_list:
                                                sub_t_file = target_s.get("path") or target_s.get("file", "")
                                                s_id = target_s.get("symbol_id", "")
                                                sub_s_name = target_s.get("name", "")
                                                
                                                if (s_id == ub_id) or (ub_id.endswith(s_id)) or (sub_s_name == ub_symbol_name and (sub_t_file == ub_file or ub_file.endswith(sub_t_file) or sub_t_file.endswith(ub_file))):
                                                    sub_match_found = True
                                                    ub_file_path = self.resolve_file_path(sub_t_file)
                                                        
                                                    if ub_file_path:
                                                        with open(ub_file_path, "r", encoding="utf-8") as ubf:
                                                            ub_lines = ubf.readlines()
                                                        
                                                        ubs_start = max(1, min(target_s.get("start_line", 1), len(ub_lines)))
                                                        ubs_end = max(ubs_start, min(target_s.get("end_line", len(ub_lines)), len(ub_lines)))
                                                        ub_slice_code = "".join(ub_lines[ubs_start - 1 : ubs_end])
                                                        
                                                        if not any(x["file"] == sub_t_file and x["line_range"] == f"{ubs_start}-{ubs_end}" for x in extracted_slices):
                                                            extracted_slices.append({
                                                                "req_num": f"{req_num} 🔗 제이슨연동 ({target_name} 호출처 -> {sub_t_file}의 [{sub_s_name}])",
                                                                "file": sub_t_file,
                                                                "line_range": f"{ubs_start}-{ubs_end}",
                                                                "code": ub_slice_code
                                                            })
                                            if not sub_match_found:
                                                print(f"            ❌ [ERROR] 호출처 구조체 '{ub_id}'를 장부에서 찾지 못했습니다.")
                    
                    if not match_found:
                        print(f"      ❓ [NOT FOUND] 코드엔 찍혀있는데 JSON 장부({file_rel_path})엔 등록 안 된 심볼입니다.")

            except Exception as e:
                import traceback
                print(f"💥 [CRITICAL ERROR] 슬라이싱 중 예외 발생: {e}")
                traceback.print_exc()

            req_num += 1

        print("\n" + "="*60)
        print(f"🏁 최종 반환할 총 슬라이스 묶음 개수: {len(extracted_slices)}개")
        print("="*60 + "\n")
        return extracted_slices
```

# 📄 [요청 6 ➡️ 불러온함수 (process 본체)] TARGET: tools/multi_agent_system/agent_code_extractor.py (279-313라인)
# ----------------------------------------------------------
```python
    def process(self, raw_prompt: str, auto_save: bool = True, output_path: str | Path = None) -> dict:
        """
        [통합 매니저 파이프라인]
        프롬프트를 입력받아 슬라이스를 추출하고, 마크다운 반환 및 마스터 격리 폴더로 내보냅니다.
        
        Returns:
            dict: {
                "slices": list[dict],    # 원본 데이터 객체 목록
                "markdown": str,         # 생성된 마크다운 텍스트
                "saved_path": Path|None  # 저장된 실제 경로
            }
        """
        slices = self.extract_multi_slices(raw_prompt)
        markdown_text = self.format_as_markdown(slices)
        save_target_path = None

        if auto_save and markdown_text:
            if output_path:
                save_target_path = Path(output_path)
            else:
                save_target_path = self.raw_root_dir / "system_maps" / "extracted_context.md"

            try:
                save_target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_target_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)
                print(f"💾 마크다운 데이터가 안전하게 저장되었습니다: {save_target_path}")
            except Exception as e:
                print(f"⚠️ 파일 저장 실패: {e}")

        return {
            "slices": slices,
            "markdown": markdown_text,
            "saved_path": save_target_path
        }
```

# 📄 [요청 6 ➡️ 불러온함수 (_load_database 본체)] TARGET: tools/multi_agent_system/agent_code_extractor.py (50-57라인)
# ----------------------------------------------------------
```python
    def _load_database(self) -> dict:
        if not self.symbols_path.exists():
            return {"symbols": []}
        try:
            with open(self.symbols_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"symbols": []}
```

# 📄 [요청 6 ➡️ 불러온함수 (__init__ 본체)] TARGET: tools/universal_indexer/indexer.py (31-41라인)
# ----------------------------------------------------------
```python
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = project_root
        self.parsers: Dict[str, Any] = {}
        self.symbols: List[Dict[str, Any]] = []
        self.files_context: Dict[str, Any] = {}
        self.definition_map: Dict[str, str] = {}
        self.data_protocols: Dict[str, Any] = {}
        self.registry_constants: List[str] = []
        
        # log(f"🏗️ 인덱서 코어 초기화 완료 (마스터 루트 주소: {self.project_root})")
        self._auto_load_parsers()
```

# 📄 [요청 6 ➡️ 불러온함수 (resolve_file_path 본체)] TARGET: tools/multi_agent_system/agent_code_extractor.py (59-96라인)
# ----------------------------------------------------------
```python
    def resolve_file_path(self, raw_path_str: str) -> Path | None:
        """
        [경로 구제 통합 레이더]
        SCAN_MODE, 상대 경로, extraction_target_project, tools 등 
        다양한 디렉토리 변수를 추적하여 실제 존재하는 파일의 Absolute Path를 반환합니다.
        """
        clean_path_str = raw_path_str.strip().replace("\\", "/")
        
        # 1차 시도: 모드별 스펙에 맞춘 경로 조립
        if self.scan_mode == "SRC":
            if clean_path_str.startswith("src/src/"):
                candidate = self.raw_root_dir / clean_path_str
            elif clean_path_str.startswith("src/"):
                candidate = self.raw_root_dir / clean_path_str
            else:
                candidate = self.raw_root_dir / "src" / clean_path_str
        else:
            candidate = self.raw_root_dir / clean_path_str

        if candidate.exists() and candidate.is_file():
            return candidate

        # 2차 시도 (구제금융): raw_root_dir 기준 직접 탐색
        candidate_raw = self.raw_root_dir / clean_path_str
        if candidate_raw.exists() and candidate_raw.is_file():
            return candidate_raw

        # 3차 시도 (구제금융): extraction_target_project 하위 탐색
        candidate_target = self.raw_root_dir / "extraction_target_project" / clean_path_str
        if candidate_target.exists() and candidate_target.is_file():
            return candidate_target

        # 4차 시도 (구제금융): tools 하위 탐색
        candidate_tools = self.raw_root_dir / "tools" / clean_path_str
        if candidate_tools.exists() and candidate_tools.is_file():
            return candidate_tools

        return None
```

# 📄 [요청 7] TARGET: tools/multi_agent_system/agent_code_extractor.py (1-313라인)
# ----------------------------------------------------------
```python
import json
import sys
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# =====================================================================
# 🧠 CORE INTELLIGENCE: MULTI-TARGET CODE SLICE LOADER (HEADLESS/AGENT ONLY)
# =====================================================================
class CodeExtractor:
    """
    AI 에이전트 및 파이프라인 전용 코드 정밀 추출기 (Headless Code Extractor)
    - UI(Tkinter 등) 요소를 완전히 제거하고 순수 데이터 처리 및 정보 흐름만 수행
    - 기존 SemanticNavigator의 슬라이싱, 경로 구제, 양방향 심볼 연관 추적 로직 100% 보존
    """
    def __init__(self, root_dir: str | Path):
        self.raw_root_dir = Path(root_dir).resolve()
        self.scan_mode = "ROOT"
        
        # 🎛️ [SCAN_MODE 스위치 반영 - universal_indexer/switch.py 절대 위치 고정]
        try:
            idx_path = str((self.raw_root_dir / "tools" / "universal_indexer").resolve())
            if idx_path not in sys.path:
                sys.path.insert(0, idx_path)
            
            import switch
            self.scan_mode = getattr(switch, "SCAN_MODE", "ROOT")
            print(f"🎛️ [SWITCH DETECTED] 현재 탐색 스위치 모드: {self.scan_mode}")
        except Exception as e:
            print(f"⚠️ [SWITCH WARNING] switch.py를 로드하지 못해 기본 'ROOT' 모드로 동작합니다. (이유: {e})")

        # 🚀 SRC 모드일 경우 하드디스크 탐색 기준점(self.root_dir)에 'src' 폴더를 강제 결합
        if self.scan_mode == "SRC":
            self.root_dir = self.raw_root_dir / "src"
            print(f"📁 [MODE: SRC] 탐색 마스터 루트가 복사/격리용 src 폴더로 변경되었습니다: {self.root_dir}")
        else:
            self.root_dir = self.raw_root_dir
            print(f"📁 [MODE: ROOT] 탐색 마스터 루트가 프로젝트 원본 루트로 설정되었습니다: {self.root_dir}")

        # 🧠 [불러오기 교정] 장부 정보는 언제나 프로젝트의 실제 본체 루트(raw_root_dir) 기준으로 가져옵니다.
        self.symbols_path = self.raw_root_dir / "system_memory" / ".jjap_symbols.json"
        self.symbols_data = self._load_database()

    def _load_database(self) -> dict:
        if not self.symbols_path.exists():
            return {"symbols": []}
        try:
            with open(self.symbols_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"symbols": []}

    def resolve_file_path(self, raw_path_str: str) -> Path | None:
        """
        [경로 구제 통합 레이더]
        SCAN_MODE, 상대 경로, extraction_target_project, tools 등 
        다양한 디렉토리 변수를 추적하여 실제 존재하는 파일의 Absolute Path를 반환합니다.
        """
        clean_path_str = raw_path_str.strip().replace("\\", "/")
        
        # 1차 시도: 모드별 스펙에 맞춘 경로 조립
        if self.scan_mode == "SRC":
            if clean_path_str.startswith("src/src/"):
                candidate = self.raw_root_dir / clean_path_str
            elif clean_path_str.startswith("src/"):
                candidate = self.raw_root_dir / clean_path_str
            else:
                candidate = self.raw_root_dir / "src" / clean_path_str
        else:
            candidate = self.raw_root_dir / clean_path_str

        if candidate.exists() and candidate.is_file():
            return candidate

        # 2차 시도 (구제금융): raw_root_dir 기준 직접 탐색
        candidate_raw = self.raw_root_dir / clean_path_str
        if candidate_raw.exists() and candidate_raw.is_file():
            return candidate_raw

        # 3차 시도 (구제금융): extraction_target_project 하위 탐색
        candidate_target = self.raw_root_dir / "extraction_target_project" / clean_path_str
        if candidate_target.exists() and candidate_target.is_file():
            return candidate_target

        # 4차 시도 (구제금융): tools 하위 탐색
        candidate_tools = self.raw_root_dir / "tools" / clean_path_str
        if candidate_tools.exists() and candidate_tools.is_file():
            return candidate_tools

        return None

    def extract_multi_slices(self, raw_prompt: str) -> list[dict]:
        """
        [Multi-Target Protocol Parser - 정규식 통합 및 경로 구제 완전판]
        프롬프트를 파싱하여 코드 슬라이스 묶음(list of dict)을 리턴합니다.
        """
        print("\n" + "="*60)
        print("🚨 [EXTRACTOR ON] 멀티 슬라이싱 파이프라인 기동!!!")
        print(f"📥 유저 입력 프롬프트: {repr(raw_prompt)}")
        print(f"⚙️ 현재 매핑 모드: {self.scan_mode} (기준 경로: {self.root_dir})")
        print("="*60)

        pattern = r"([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\s:]+(?:L)?(\d+)(?:\s*-\s*(?:L)?(\d+))?"
        matches = re.findall(pattern, raw_prompt)

        print(f"🔍 정규식 1차 타겟 스캔 결과: {matches}")
        if not matches:
            print("⚠️ 매칭되는 파일 경로 및 라인 규격이 없습니다. 빈 배열 리턴.")
            return []

        extracted_slices = []
        req_num = 1

        for match in matches:
            file_rel_path = match[0].strip().replace("\\", "/")
            start_line = int(match[1])
            end_line = int(match[2]) if match[2] else start_line

            print(f"\n🎯 [요청 #{req_num}] 메인 타겟 분석 시작 -> {file_rel_path} ({start_line} ~ {end_line} 라인)")

            target_file_path = self.resolve_file_path(file_rel_path)
            
            if not target_file_path:
                print(f"   ❌ [ERROR] 해당 파일이 실제 경로에 존재하지 않습니다! 패스합니다: {file_rel_path}")
                continue

            print(f"   🟢 [경로 확정] 디스크 실체 발견: {target_file_path}")

            try:
                with open(target_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                total_lines = len(lines)
                safe_start = max(1, min(start_line, total_lines))
                safe_end = max(safe_start, min(end_line, total_lines))
                print(f"   📏 파일 전체 줄 수: {total_lines} | 보정된 안전 범위: {safe_start} ~ {safe_end}")

                slice_lines = lines[safe_start - 1 : safe_end]
                slice_code = "".join(slice_lines)
                print(f"   🟢 1차 메인 슬라이싱 성공 (길이: {len(slice_code)}자)")

                extracted_slices.append({
                    "req_num": f"{req_num}",
                    "file": file_rel_path,
                    "line_range": f"{safe_start}-{safe_end}",
                    "code": slice_code
                })

                # [2단계] 🔗 제이슨 기반 2차 심볼 탐색기 가동
                print(f"   📡 [2차 사냥기] 잘려 나온 텍스트 내부에서 양방향 심볼 식별 개시...")

                defined_names = re.findall(r"(?:def|class)\s+([a-zA-Z0-9_]+)", slice_code)
                called_names = re.findall(r"(?:[a-zA-Z0-9_]+\.)?([a-zA-Z0-9_]+)\s*\(", slice_code)
                file_ref_names = [f for f in re.findall(r'[\'"]([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\'"]', slice_code) if f != file_rel_path]

                builtin_filters = {"print", "len", "range", "open", "dict", "list", "set", "any", "all", "max", "min", "append", "get", "strip", "split", "exists", "readlines", "join"}
                filtered_called_names = [name for name in called_names if name not in builtin_filters]

                target_symbols = list(set(defined_names + filtered_called_names + file_ref_names))
                print(f"   📦 [양방향 통합] 징집 대상 심볼 목록: {target_symbols}")
                
                symbols_list = self.symbols_data.get("symbols", [])
                print(f"   📚 로드된 JSON 장부 총 심볼 개수: {len(symbols_list)}개")

                for target_name in target_symbols:
                    print(f"      🔎 [전역 심볼 대조] 이름: '{target_name}' -> 장부 전체 스캔 중...")
                    match_found = False
                    
                    for s in symbols_list:
                        if s.get("name") == target_name:
                            match_found = True
                            t_file = s.get("path") or s.get("file", "")
                            s_start = s.get("start_line", 1)
                            s_end = s.get("end_line", 1)

                            # 정방향 연관 심볼 추적
                            if t_file != file_rel_path:
                                print(f"         ➡️ [정방향] 내가 불러온 함수 본체 포착 -> {t_file} ({s_start}~{s_end}라인)")
                                callee_file_path = self.resolve_file_path(t_file)
                                    
                                if callee_file_path:
                                    with open(callee_file_path, "r", encoding="utf-8") as cf:
                                        cf_lines = cf.readlines()
                                    
                                    s_start = max(1, min(s_start, len(cf_lines)))
                                    s_end = max(s_start, min(s_end, len(cf_lines)))
                                    callee_code = "".join(cf_lines[s_start - 1 : s_end])
                                    
                                    if not any(x["file"] == t_file and x["line_range"] == f"{s_start}-{s_end}" for x in extracted_slices):
                                        extracted_slices.append({
                                            "req_num": f"{req_num} ➡️ 불러온함수 ({target_name} 본체)",
                                            "file": t_file,
                                            "line_range": f"{s_start}-{s_end}",
                                            "code": callee_code
                                        })

                            # 역방향 연관 심볼 추적 (used_by)
                            if (target_name in defined_names) or (t_file == file_rel_path):
                                ub_list = s.get("used_by", [])
                                if ub_list:
                                    print(f"         ⬅️ [역방향] 나를 부르는 전역 호출처 목록(used_by): {ub_list}")
                                    for ub_id in ub_list:
                                        if "::" in ub_id:
                                            ub_file, ub_symbol_name = ub_id.split("::", 1)
                                            if "." in ub_symbol_name:
                                                ub_symbol_name = ub_symbol_name.split(".")[-1]
                                            
                                            sub_match_found = False
                                            for target_s in symbols_list:
                                                sub_t_file = target_s.get("path") or target_s.get("file", "")
                                                s_id = target_s.get("symbol_id", "")
                                                sub_s_name = target_s.get("name", "")
                                                
                                                if (s_id == ub_id) or (ub_id.endswith(s_id)) or (sub_s_name == ub_symbol_name and (sub_t_file == ub_file or ub_file.endswith(sub_t_file) or sub_t_file.endswith(ub_file))):
                                                    sub_match_found = True
                                                    ub_file_path = self.resolve_file_path(sub_t_file)
                                                        
                                                    if ub_file_path:
                                                        with open(ub_file_path, "r", encoding="utf-8") as ubf:
                                                            ub_lines = ubf.readlines()
                                                        
                                                        ubs_start = max(1, min(target_s.get("start_line", 1), len(ub_lines)))
                                                        ubs_end = max(ubs_start, min(target_s.get("end_line", len(ub_lines)), len(ub_lines)))
                                                        ub_slice_code = "".join(ub_lines[ubs_start - 1 : ubs_end])
                                                        
                                                        if not any(x["file"] == sub_t_file and x["line_range"] == f"{ubs_start}-{ubs_end}" for x in extracted_slices):
                                                            extracted_slices.append({
                                                                "req_num": f"{req_num} 🔗 제이슨연동 ({target_name} 호출처 -> {sub_t_file}의 [{sub_s_name}])",
                                                                "file": sub_t_file,
                                                                "line_range": f"{ubs_start}-{ubs_end}",
                                                                "code": ub_slice_code
                                                            })
                                            if not sub_match_found:
                                                print(f"            ❌ [ERROR] 호출처 구조체 '{ub_id}'를 장부에서 찾지 못했습니다.")
                    
                    if not match_found:
                        print(f"      ❓ [NOT FOUND] 코드엔 찍혀있는데 JSON 장부({file_rel_path})엔 등록 안 된 심볼입니다.")

            except Exception as e:
                import traceback
                print(f"💥 [CRITICAL ERROR] 슬라이싱 중 예외 발생: {e}")
                traceback.print_exc()

            req_num += 1

        print("\n" + "="*60)
        print(f"🏁 최종 반환할 총 슬라이스 묶음 개수: {len(extracted_slices)}개")
        print("="*60 + "\n")
        return extracted_slices

    def format_as_markdown(self, extracted_slices: list[dict]) -> str:
        """
        슬라이싱 데이터 배열을 받아서 LLM 및 에이전트에 주입할 마크다운 문맥으로 변환합니다.
        """
        if not extracted_slices:
            return ""

        md_lines = []
        md_lines.append("# ==========================================================================")
        md_lines.append("# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드")
        md_lines.append(f"# [SCAN_MODE] {self.scan_mode}")
        md_lines.append("# ==========================================================================")

        for slc in extracted_slices:
            md_lines.append(f"# 📄 [요청 {slc['req_num']}] TARGET: {slc['file']} ({slc['line_range']}라인)")
            md_lines.append("# ----------------------------------------------------------")
            md_lines.append("```python")
            md_lines.append(slc["code"].rstrip())
            md_lines.append("```\n")

        return "\n".join(md_lines)

    def process(self, raw_prompt: str, auto_save: bool = True, output_path: str | Path = None) -> dict:
        """
        [통합 매니저 파이프라인]
        프롬프트를 입력받아 슬라이스를 추출하고, 마크다운 반환 및 마스터 격리 폴더로 내보냅니다.
        
        Returns:
            dict: {
                "slices": list[dict],    # 원본 데이터 객체 목록
                "markdown": str,         # 생성된 마크다운 텍스트
                "saved_path": Path|None  # 저장된 실제 경로
            }
        """
        slices = self.extract_multi_slices(raw_prompt)
        markdown_text = self.format_as_markdown(slices)
        save_target_path = None

        if auto_save and markdown_text:
            if output_path:
                save_target_path = Path(output_path)
            else:
                save_target_path = self.raw_root_dir / "system_maps" / "extracted_context.md"

            try:
                save_target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_target_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)
                print(f"💾 마크다운 데이터가 안전하게 저장되었습니다: {save_target_path}")
            except Exception as e:
                print(f"⚠️ 파일 저장 실패: {e}")

        return {
            "slices": slices,
            "markdown": markdown_text,
            "saved_path": save_target_path
        }
```

# 📄 [요청 7 ➡️ 불러온함수 (CodeExtractor 본체)] TARGET: tools/universal_indexer/agent_navigator.py (18-281라인)
# ----------------------------------------------------------
```python
class CodeExtractor:
    """
    UI(Navigator) 전용 독립 코드 추출기
    - agent_code_extractor.py의 수정 및 위치 변경에 절대 영향을 받지 않는 독자 엔진
    """
    def __init__(self, root_dir: str | Path):
        self.raw_root_dir = Path(root_dir).resolve()
        self.scan_mode = "ROOT"
        
        try:
            idx_path = str((self.raw_root_dir / "tools" / "universal_indexer").resolve())
            if idx_path not in sys.path:
                sys.path.insert(0, idx_path)
            
            import switch
            self.scan_mode = getattr(switch, "SCAN_MODE", "ROOT")
            print(f"🎛️ [SWITCH DETECTED] 현재 탐색 스위치 모드: {self.scan_mode}")
        except Exception as e:
            print(f"⚠️ [SWITCH WARNING] switch.py를 로드하지 못해 기본 'ROOT' 모드로 동작합니다. (이유: {e})")

        if self.scan_mode == "SRC":
            self.root_dir = self.raw_root_dir / "src"
            print(f"📁 [MODE: SRC] 탐색 마스터 루트가 복사/격리용 src 폴더로 변경되었습니다: {self.root_dir}")
        else:
            self.root_dir = self.raw_root_dir
            print(f"📁 [MODE: ROOT] 탐색 마스터 루트가 프로젝트 원본 루트로 설정되었습니다: {self.root_dir}")

        self.symbols_path = self.raw_root_dir / "system_memory" / ".jjap_symbols.json"
        self.symbols_data = self._load_database()

    def _load_database(self) -> dict:
        if not self.symbols_path.exists():
            return {"symbols": []}
        try:
            with open(self.symbols_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"symbols": []}

    def resolve_file_path(self, raw_path_str: str) -> Path | None:
        clean_path_str = raw_path_str.strip().replace("\\", "/")
        
        if self.scan_mode == "SRC":
            if clean_path_str.startswith("src/src/"):
                candidate = self.raw_root_dir / clean_path_str
            elif clean_path_str.startswith("src/"):
                candidate = self.raw_root_dir / clean_path_str
            else:
                candidate = self.raw_root_dir / "src" / clean_path_str
        else:
            candidate = self.raw_root_dir / clean_path_str

        if candidate.exists() and candidate.is_file():
            return candidate

        candidate_raw = self.raw_root_dir / clean_path_str
        if candidate_raw.exists() and candidate_raw.is_file():
            return candidate_raw

        candidate_target = self.raw_root_dir / "extraction_target_project" / clean_path_str
        if candidate_target.exists() and candidate_target.is_file():
            return candidate_target

        candidate_tools = self.raw_root_dir / "tools" / clean_path_str
        if candidate_tools.exists() and candidate_tools.is_file():
            return candidate_tools

        return None

    def extract_multi_slices(self, raw_prompt: str) -> list[dict]:
        print("\n" + "="*60)
        print("🚨 [EXTRACTOR ON] 멀티 슬라이싱 파이프라인 기동!!!")
        print(f"📥 유저 입력 프롬프트: {repr(raw_prompt)}")
        print(f"⚙️ 현재 매핑 모드: {self.scan_mode} (기준 경로: {self.root_dir})")
        print("="*60)

        pattern = r"([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\s:]+(?:L)?(\d+)(?:\s*-\s*(?:L)?(\d+))?"
        matches = re.findall(pattern, raw_prompt)

        print(f"🔍 정규식 1차 타겟 스캔 결과: {matches}")
        if not matches:
            print("⚠️ 매칭되는 파일 경로 및 라인 규격이 없습니다. 빈 배열 리턴.")
            return []

        extracted_slices = []
        req_num = 1

        for match in matches:
            file_rel_path = match[0].strip().replace("\\", "/")
            start_line = int(match[1])
            end_line = int(match[2]) if match[2] else start_line

            print(f"\n🎯 [요청 #{req_num}] 메인 타겟 분석 시작 -> {file_rel_path} ({start_line} ~ {end_line} 라인)")

            target_file_path = self.resolve_file_path(file_rel_path)
            
            if not target_file_path:
                print(f"   ❌ [ERROR] 해당 파일이 실제 경로에 존재하지 않습니다! 패스합니다: {file_rel_path}")
                continue

            print(f"   🟢 [경로 확정] 디스크 실체 발견: {target_file_path}")

            try:
                with open(target_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                total_lines = len(lines)
                safe_start = max(1, min(start_line, total_lines))
                safe_end = max(safe_start, min(end_line, total_lines))
                print(f"   📏 파일 전체 줄 수: {total_lines} | 보정된 안전 범위: {safe_start} ~ {safe_end}")

                slice_lines = lines[safe_start - 1 : safe_end]
                slice_code = "".join(slice_lines)
                print(f"   🟢 1차 메인 슬라이싱 성공 (길이: {len(slice_code)}자)")

                extracted_slices.append({
                    "req_num": f"{req_num}",
                    "file": file_rel_path,
                    "line_range": f"{safe_start}-{safe_end}",
                    "code": slice_code
                })

                print(f"   📡 [2차 사냥기] 잘려 나온 텍스트 내부에서 양방향 심볼 식별 개시...")

                defined_names = re.findall(r"(?:def|class)\s+([a-zA-Z0-9_]+)", slice_code)
                called_names = re.findall(r"(?:[a-zA-Z0-9_]+\.)?([a-zA-Z0-9_]+)\s*\(", slice_code)
                file_ref_names = [f for f in re.findall(r'[\'"]([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\'"]', slice_code) if f != file_rel_path]

                builtin_filters = {"print", "len", "range", "open", "dict", "list", "set", "any", "all", "max", "min", "append", "get", "strip", "split", "exists", "readlines", "join"}
                filtered_called_names = [name for name in called_names if name not in builtin_filters]

                target_symbols = list(set(defined_names + filtered_called_names + file_ref_names))
                print(f"   📦 [양방향 통합] 징집 대상 심볼 목록: {target_symbols}")
                
                symbols_list = self.symbols_data.get("symbols", [])
                print(f"   📚 로드된 JSON 장부 총 심볼 개수: {len(symbols_list)}개")

                for target_name in target_symbols:
                    print(f"      🔎 [전역 심볼 대조] 이름: '{target_name}' -> 장부 전체 스캔 중...")
                    match_found = False
                    
                    for s in symbols_list:
                        if s.get("name") == target_name:
                            match_found = True
                            t_file = s.get("path") or s.get("file", "")
                            s_start = s.get("start_line", 1)
                            s_end = s.get("end_line", 1)

                            if t_file != file_rel_path:
                                print(f"         ➡️ [정방향] 내가 불러온 함수 본체 포착 -> {t_file} ({s_start}~{s_end}라인)")
                                callee_file_path = self.resolve_file_path(t_file)
                                    
                                if callee_file_path:
                                    with open(callee_file_path, "r", encoding="utf-8") as cf:
                                        cf_lines = cf.readlines()
                                    
                                    s_start = max(1, min(s_start, len(cf_lines)))
                                    s_end = max(s_start, min(s_end, len(cf_lines)))
                                    callee_code = "".join(cf_lines[s_start - 1 : s_end])
                                    
                                    if not any(x["file"] == t_file and x["line_range"] == f"{s_start}-{s_end}" for x in extracted_slices):
                                        extracted_slices.append({
                                            "req_num": f"{req_num} ➡️ 불러온함수 ({target_name} 본체)",
                                            "file": t_file,
                                            "line_range": f"{s_start}-{s_end}",
                                            "code": callee_code
                                        })

                            if (target_name in defined_names) or (t_file == file_rel_path):
                                ub_list = s.get("used_by", [])
                                if ub_list:
                                    print(f"         ⬅️ [역방향] 나를 부르는 전역 호출처 목록(used_by): {ub_list}")
                                    for ub_id in ub_list:
                                        if "::" in ub_id:
                                            ub_file, ub_symbol_name = ub_id.split("::", 1)
                                            if "." in ub_symbol_name:
                                                ub_symbol_name = ub_symbol_name.split(".")[-1]
                                            
                                            sub_match_found = False
                                            for target_s in symbols_list:
                                                sub_t_file = target_s.get("path") or target_s.get("file", "")
                                                s_id = target_s.get("symbol_id", "")
                                                sub_s_name = target_s.get("name", "")
                                                
                                                if (s_id == ub_id) or (ub_id.endswith(s_id)) or (sub_s_name == ub_symbol_name and (sub_t_file == ub_file or ub_file.endswith(sub_t_file) or sub_t_file.endswith(ub_file))):
                                                    sub_match_found = True
                                                    ub_file_path = self.resolve_file_path(sub_t_file)
                                                        
                                                    if ub_file_path:
                                                        with open(ub_file_path, "r", encoding="utf-8") as ubf:
                                                            ub_lines = ubf.readlines()
                                                        
                                                        ubs_start = max(1, min(target_s.get("start_line", 1), len(ub_lines)))
                                                        ubs_end = max(ubs_start, min(target_s.get("end_line", len(ub_lines)), len(ub_lines)))
                                                        ub_slice_code = "".join(ub_lines[ubs_start - 1 : ubs_end])
                                                        
                                                        if not any(x["file"] == sub_t_file and x["line_range"] == f"{ubs_start}-{ubs_end}" for x in extracted_slices):
                                                            extracted_slices.append({
                                                                "req_num": f"{req_num} 🔗 제이슨연동 ({target_name} 호출처 -> {sub_t_file}의 [{sub_s_name}])",
                                                                "file": sub_t_file,
                                                                "line_range": f"{ubs_start}-{ubs_end}",
                                                                "code": ub_slice_code
                                                            })
                                            if not sub_match_found:
                                                print(f"            ❌ [ERROR] 호출처 구조체 '{ub_id}'를 장부에서 찾지 못했습니다.")
                    
                    if not match_found:
                        print(f"      ❓ [NOT FOUND] 코드엔 찍혀있는데 JSON 장부({file_rel_path})엔 등록 안 된 심볼입니다.")

            except Exception as e:
                import traceback
                print(f"💥 [CRITICAL ERROR] 슬라이싱 중 예외 발생: {e}")
                traceback.print_exc()

            req_num += 1

        print("\n" + "="*60)
        print(f"🏁 최종 반환할 총 슬라이스 묶음 개수: {len(extracted_slices)}개")
        print("="*60 + "\n")
        return extracted_slices

    def format_as_markdown(self, extracted_slices: list[dict]) -> str:
        if not extracted_slices:
            return ""

        md_lines = []
        md_lines.append("# ==========================================================================")
        md_lines.append("# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드")
        md_lines.append(f"# [SCAN_MODE] {self.scan_mode}")
        md_lines.append("# ==========================================================================")

        for slc in extracted_slices:
            md_lines.append(f"# 📄 [요청 {slc['req_num']}] TARGET: {slc['file']} ({slc['line_range']}라인)")
            md_lines.append("# ----------------------------------------------------------")
            md_lines.append("```python")
            md_lines.append(slc["code"].rstrip())
            md_lines.append("```\n")

        return "\n".join(md_lines)

    def process(self, raw_prompt: str, auto_save: bool = True, output_path: str | Path = None) -> dict:
        slices = self.extract_multi_slices(raw_prompt)
        markdown_text = self.format_as_markdown(slices)
        save_target_path = None

        if auto_save and markdown_text:
            if output_path:
                save_target_path = Path(output_path)
            else:
                save_target_path = self.raw_root_dir / "system_maps" / "extracted_context.md"

            try:
                save_target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_target_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)
                print(f"💾 마크다운 데이터가 안전하게 저장되었습니다: {save_target_path}")
            except Exception as e:
                print(f"⚠️ 파일 저장 실패: {e}")

        return {
            "slices": slices,
            "markdown": markdown_text,
            "saved_path": save_target_path
        }
```

# 📄 [요청 7 ➡️ 불러온함수 (format_as_markdown 본체)] TARGET: tools/universal_indexer/agent_navigator.py (239-256라인)
# ----------------------------------------------------------
```python
    def format_as_markdown(self, extracted_slices: list[dict]) -> str:
        if not extracted_slices:
            return ""

        md_lines = []
        md_lines.append("# ==========================================================================")
        md_lines.append("# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드")
        md_lines.append(f"# [SCAN_MODE] {self.scan_mode}")
        md_lines.append("# ==========================================================================")

        for slc in extracted_slices:
            md_lines.append(f"# 📄 [요청 {slc['req_num']}] TARGET: {slc['file']} ({slc['line_range']}라인)")
            md_lines.append("# ----------------------------------------------------------")
            md_lines.append("```python")
            md_lines.append(slc["code"].rstrip())
            md_lines.append("```\n")

        return "\n".join(md_lines)
```

# 📄 [요청 7 ➡️ 불러온함수 (extract_multi_slices 본체)] TARGET: tools/universal_indexer/agent_navigator.py (87-237라인)
# ----------------------------------------------------------
```python
    def extract_multi_slices(self, raw_prompt: str) -> list[dict]:
        print("\n" + "="*60)
        print("🚨 [EXTRACTOR ON] 멀티 슬라이싱 파이프라인 기동!!!")
        print(f"📥 유저 입력 프롬프트: {repr(raw_prompt)}")
        print(f"⚙️ 현재 매핑 모드: {self.scan_mode} (기준 경로: {self.root_dir})")
        print("="*60)

        pattern = r"([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\s:]+(?:L)?(\d+)(?:\s*-\s*(?:L)?(\d+))?"
        matches = re.findall(pattern, raw_prompt)

        print(f"🔍 정규식 1차 타겟 스캔 결과: {matches}")
        if not matches:
            print("⚠️ 매칭되는 파일 경로 및 라인 규격이 없습니다. 빈 배열 리턴.")
            return []

        extracted_slices = []
        req_num = 1

        for match in matches:
            file_rel_path = match[0].strip().replace("\\", "/")
            start_line = int(match[1])
            end_line = int(match[2]) if match[2] else start_line

            print(f"\n🎯 [요청 #{req_num}] 메인 타겟 분석 시작 -> {file_rel_path} ({start_line} ~ {end_line} 라인)")

            target_file_path = self.resolve_file_path(file_rel_path)
            
            if not target_file_path:
                print(f"   ❌ [ERROR] 해당 파일이 실제 경로에 존재하지 않습니다! 패스합니다: {file_rel_path}")
                continue

            print(f"   🟢 [경로 확정] 디스크 실체 발견: {target_file_path}")

            try:
                with open(target_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                total_lines = len(lines)
                safe_start = max(1, min(start_line, total_lines))
                safe_end = max(safe_start, min(end_line, total_lines))
                print(f"   📏 파일 전체 줄 수: {total_lines} | 보정된 안전 범위: {safe_start} ~ {safe_end}")

                slice_lines = lines[safe_start - 1 : safe_end]
                slice_code = "".join(slice_lines)
                print(f"   🟢 1차 메인 슬라이싱 성공 (길이: {len(slice_code)}자)")

                extracted_slices.append({
                    "req_num": f"{req_num}",
                    "file": file_rel_path,
                    "line_range": f"{safe_start}-{safe_end}",
                    "code": slice_code
                })

                print(f"   📡 [2차 사냥기] 잘려 나온 텍스트 내부에서 양방향 심볼 식별 개시...")

                defined_names = re.findall(r"(?:def|class)\s+([a-zA-Z0-9_]+)", slice_code)
                called_names = re.findall(r"(?:[a-zA-Z0-9_]+\.)?([a-zA-Z0-9_]+)\s*\(", slice_code)
                file_ref_names = [f for f in re.findall(r'[\'"]([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\'"]', slice_code) if f != file_rel_path]

                builtin_filters = {"print", "len", "range", "open", "dict", "list", "set", "any", "all", "max", "min", "append", "get", "strip", "split", "exists", "readlines", "join"}
                filtered_called_names = [name for name in called_names if name not in builtin_filters]

                target_symbols = list(set(defined_names + filtered_called_names + file_ref_names))
                print(f"   📦 [양방향 통합] 징집 대상 심볼 목록: {target_symbols}")
                
                symbols_list = self.symbols_data.get("symbols", [])
                print(f"   📚 로드된 JSON 장부 총 심볼 개수: {len(symbols_list)}개")

                for target_name in target_symbols:
                    print(f"      🔎 [전역 심볼 대조] 이름: '{target_name}' -> 장부 전체 스캔 중...")
                    match_found = False
                    
                    for s in symbols_list:
                        if s.get("name") == target_name:
                            match_found = True
                            t_file = s.get("path") or s.get("file", "")
                            s_start = s.get("start_line", 1)
                            s_end = s.get("end_line", 1)

                            if t_file != file_rel_path:
                                print(f"         ➡️ [정방향] 내가 불러온 함수 본체 포착 -> {t_file} ({s_start}~{s_end}라인)")
                                callee_file_path = self.resolve_file_path(t_file)
                                    
                                if callee_file_path:
                                    with open(callee_file_path, "r", encoding="utf-8") as cf:
                                        cf_lines = cf.readlines()
                                    
                                    s_start = max(1, min(s_start, len(cf_lines)))
                                    s_end = max(s_start, min(s_end, len(cf_lines)))
                                    callee_code = "".join(cf_lines[s_start - 1 : s_end])
                                    
                                    if not any(x["file"] == t_file and x["line_range"] == f"{s_start}-{s_end}" for x in extracted_slices):
                                        extracted_slices.append({
                                            "req_num": f"{req_num} ➡️ 불러온함수 ({target_name} 본체)",
                                            "file": t_file,
                                            "line_range": f"{s_start}-{s_end}",
                                            "code": callee_code
                                        })

                            if (target_name in defined_names) or (t_file == file_rel_path):
                                ub_list = s.get("used_by", [])
                                if ub_list:
                                    print(f"         ⬅️ [역방향] 나를 부르는 전역 호출처 목록(used_by): {ub_list}")
                                    for ub_id in ub_list:
                                        if "::" in ub_id:
                                            ub_file, ub_symbol_name = ub_id.split("::", 1)
                                            if "." in ub_symbol_name:
                                                ub_symbol_name = ub_symbol_name.split(".")[-1]
                                            
                                            sub_match_found = False
                                            for target_s in symbols_list:
                                                sub_t_file = target_s.get("path") or target_s.get("file", "")
                                                s_id = target_s.get("symbol_id", "")
                                                sub_s_name = target_s.get("name", "")
                                                
                                                if (s_id == ub_id) or (ub_id.endswith(s_id)) or (sub_s_name == ub_symbol_name and (sub_t_file == ub_file or ub_file.endswith(sub_t_file) or sub_t_file.endswith(ub_file))):
                                                    sub_match_found = True
                                                    ub_file_path = self.resolve_file_path(sub_t_file)
                                                        
                                                    if ub_file_path:
                                                        with open(ub_file_path, "r", encoding="utf-8") as ubf:
                                                            ub_lines = ubf.readlines()
                                                        
                                                        ubs_start = max(1, min(target_s.get("start_line", 1), len(ub_lines)))
                                                        ubs_end = max(ubs_start, min(target_s.get("end_line", len(ub_lines)), len(ub_lines)))
                                                        ub_slice_code = "".join(ub_lines[ubs_start - 1 : ubs_end])
                                                        
                                                        if not any(x["file"] == sub_t_file and x["line_range"] == f"{ubs_start}-{ubs_end}" for x in extracted_slices):
                                                            extracted_slices.append({
                                                                "req_num": f"{req_num} 🔗 제이슨연동 ({target_name} 호출처 -> {sub_t_file}의 [{sub_s_name}])",
                                                                "file": sub_t_file,
                                                                "line_range": f"{ubs_start}-{ubs_end}",
                                                                "code": ub_slice_code
                                                            })
                                            if not sub_match_found:
                                                print(f"            ❌ [ERROR] 호출처 구조체 '{ub_id}'를 장부에서 찾지 못했습니다.")
                    
                    if not match_found:
                        print(f"      ❓ [NOT FOUND] 코드엔 찍혀있는데 JSON 장부({file_rel_path})엔 등록 안 된 심볼입니다.")

            except Exception as e:
                import traceback
                print(f"💥 [CRITICAL ERROR] 슬라이싱 중 예외 발생: {e}")
                traceback.print_exc()

            req_num += 1

        print("\n" + "="*60)
        print(f"🏁 최종 반환할 총 슬라이스 묶음 개수: {len(extracted_slices)}개")
        print("="*60 + "\n")
        return extracted_slices
```

# 📄 [요청 7 ➡️ 불러온함수 (process 본체)] TARGET: tools/universal_indexer/agent_navigator.py (258-281라인)
# ----------------------------------------------------------
```python
    def process(self, raw_prompt: str, auto_save: bool = True, output_path: str | Path = None) -> dict:
        slices = self.extract_multi_slices(raw_prompt)
        markdown_text = self.format_as_markdown(slices)
        save_target_path = None

        if auto_save and markdown_text:
            if output_path:
                save_target_path = Path(output_path)
            else:
                save_target_path = self.raw_root_dir / "system_maps" / "extracted_context.md"

            try:
                save_target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_target_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)
                print(f"💾 마크다운 데이터가 안전하게 저장되었습니다: {save_target_path}")
            except Exception as e:
                print(f"⚠️ 파일 저장 실패: {e}")

        return {
            "slices": slices,
            "markdown": markdown_text,
            "saved_path": save_target_path
        }
```

# 📄 [요청 7 ➡️ 불러온함수 (_load_database 본체)] TARGET: tools/universal_indexer/agent_navigator.py (48-55라인)
# ----------------------------------------------------------
```python
    def _load_database(self) -> dict:
        if not self.symbols_path.exists():
            return {"symbols": []}
        try:
            with open(self.symbols_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"symbols": []}
```

# 📄 [요청 7 ➡️ 불러온함수 (resolve_file_path 본체)] TARGET: tools/universal_indexer/agent_navigator.py (57-85라인)
# ----------------------------------------------------------
```python
    def resolve_file_path(self, raw_path_str: str) -> Path | None:
        clean_path_str = raw_path_str.strip().replace("\\", "/")
        
        if self.scan_mode == "SRC":
            if clean_path_str.startswith("src/src/"):
                candidate = self.raw_root_dir / clean_path_str
            elif clean_path_str.startswith("src/"):
                candidate = self.raw_root_dir / clean_path_str
            else:
                candidate = self.raw_root_dir / "src" / clean_path_str
        else:
            candidate = self.raw_root_dir / clean_path_str

        if candidate.exists() and candidate.is_file():
            return candidate

        candidate_raw = self.raw_root_dir / clean_path_str
        if candidate_raw.exists() and candidate_raw.is_file():
            return candidate_raw

        candidate_target = self.raw_root_dir / "extraction_target_project" / clean_path_str
        if candidate_target.exists() and candidate_target.is_file():
            return candidate_target

        candidate_tools = self.raw_root_dir / "tools" / clean_path_str
        if candidate_tools.exists() and candidate_tools.is_file():
            return candidate_tools

        return None
```
