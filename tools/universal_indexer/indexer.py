
import ast
import json
import hashlib
import os
import importlib.util
from pathlib import Path
from typing import Dict, Any, List

# 🎯 영문 switch.py 콘솔 원격 연동
try:
    from switch import SCAN_MODE
except ImportError:
    SCAN_MODE = "ROOT"

SCRIPT_DIR = Path(__file__).parent.resolve()
# 🔄 폴더명이 universal_indexer로 변경되었으므로 진입 조건문 검사 명칭을 치환하여 진짜 마스터 루트를 확보합니다.
if SCRIPT_DIR.name == "universal_indexer" and SCRIPT_DIR.parent.name == "tools":
    PROJECT_ROOT = SCRIPT_DIR.parent.parent
else:
    PROJECT_ROOT = SCRIPT_DIR

OUTPUT_FILE_PATH = PROJECT_ROOT / "system_maps" / "AI_CODEBASE_MAP.md"
REGISTRY_JSON_PATH = PROJECT_ROOT / "system_memory" / "registry_constants.json"
PROTOCOL_JSON_PATH = PROJECT_ROOT / "system_memory" / "data_protocols.json"

class AdvancedIndexerV2:
    """
    [Jjap-Cursor Core Indexer V3.5 - Ultra Universal Engine]
    
    🛠️ 형님의 무제한 범용성 계약 조건 완벽 반영:
      - 특정 폴더 제한 완전 철폐! 설정에 따라 프로젝트 전체 혹은 src/ 내부를 자동 스캔합니다.
      - core_parsers 폴더의 파서들을 동적 로드하여 다국어/다양한 포맷을 확장 흡수합니다.
    """

    def __init__(self, project_root: Path):
        """⚙️ 클래스 내부로 올바르게 편입된 생성자 마스터 엔진"""
        self.project_root = project_root
        self.symbols: List[Dict[str, Any]] = []
        self.files_context: Dict[str, Any] = {}
        self.definition_map: Dict[str, str] = {}
        self.data_protocols: Dict[str, Any] = {}
        self.registry_constants: List[str] = []
        
        # 🧠 [형님의 확장자 자동화 장부 계좌 개설]
        self.parsers = {}
        
        # 🚀 인덱서 기동과 동시에 core_parsers 레이더 가동!
        self._auto_load_parsers()

    def _auto_load_parsers(self):
        """
        📡 [Auto-Discovery Engine]
        core_parsers 폴더 내부의 파일을 자동 스캔하여 형님과의 단일 마스터 함수 계약을 검증합니다.
        성공/실패 사유를 터미널에 실시간으로 자백합니다.
        """
        parsers_dir = Path(__file__).parent / "core_parsers"
        
        print("\n" + "="*70)
        print("⚡ [Jjap-Compiler] core_parsers 플러그인 자동 징집 레이더 가동...")
        print(f"📂 탐색 기지 경로: {parsers_dir}")
        print("="*70)

        if not parsers_dir.exists():
            print("ℹ️ [엔진 안내] core_parsers 폴더가 존재하지 않아 동적 로드를 스킵합니다.")
            print("="*70 + "\n")
            return

        for parser_file in parsers_dir.glob("*_parser.py"):
            if parser_file.name == "__init__.py":
                continue
                
            file_name = parser_file.name
            
            try:
                parts = file_name.split('_')
                if len(parts) < 2:
                    print(f"❌ [불러오기 실패] 파일명 규격 미달: '{file_name}' (형식은 '[확장자]_parser.py' 여야 합니다.)")
                    continue
                    
                ext = f".{parts[0]}".lower()
                
                # 실시간 물리 스크립트 로드
                spec = importlib.util.spec_from_file_location(parser_file.stem, parser_file)
                if spec is None or spec.loader is None:
                    print(f"❌ [불러오기 실패] Spec 추출 불가: '{file_name}'")
                    continue
                    
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 🤝 단일 마스터 함수 계약 검증
                if hasattr(module, "extract_symbols"):
                    self.parsers[ext] = module.extract_symbols
                    print(f"✅ [임포트 성공 / 형식 통과] 확장자 [{ext}] 처리 엔진 탑재 완료!")
                    print(f"    └─ 파일: {file_name}")
                else:
                    print(f"⚠️ [임포트 성공 / 계약 위반 탈락] 파일 로드는 성공했으나 규격 미달!")
                    print(f"    └─ 파일: {file_name}")
                    print(f"    └─ 탈락 사유: 내부에 'extract_symbols' 함수가 존재하지 않습니다.")
                    
            except Exception as e:
                print(f"❌ [불러오기 실패] '{file_name}' 컴파일/실행 단계에서 예외 크래시 발생!")
                print(f"    └─ 치명적 에러 내용: {e}")
                
        print("="*70 + "\n")
        
    def _get_sha256(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _extract_skeleton(self, content: str) -> str:
        try:
            tree = ast.parse(content)
            skeleton_lines = []
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    skeleton_lines.append(f"class {node.name}:")
                    for sub_node in node.body:
                        if isinstance(sub_node, ast.FunctionDef):
                            skeleton_lines.append(f"    def {sub_node.name}(...):")
                            skeleton_lines.append(f"        ...")
                elif isinstance(node, ast.FunctionDef):
                    skeleton_lines.append(f"def {node.name}(...):")
                    skeleton_lines.append(f"    ...")
            return "\n".join(skeleton_lines)
        except Exception:
            return ""

    def parse_protocols_and_registries(self, content: str, rel_path_str: str):
        """[범용성 자동 지능 엔진] 하드코딩 없이 클래스의 성격을 파악하여 장부에 자동 분배"""
        try:
            tree = ast.parse(content)
            for node in tree.body:
                if not isinstance(node, ast.ClassDef):
                    continue

                # 🛡️ 1. 데이터 프로토콜 스캔: 이름에 Variables 또는 vars가 들어가면 데이터 명세서로 징집
                if "Variables" in node.name or "vars" in node.name.lower():
                    fields = {}
                    for sub_node in node.body:
                        if isinstance(sub_node, ast.FunctionDef) and sub_node.name == "__init__":
                            for stmt in sub_node.body:
                                if isinstance(stmt, ast.Assign):
                                    for target in stmt.targets:
                                        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self":
                                            val_str = "Unknown"
                                            if isinstance(stmt.value, ast.Constant):
                                                val_str = f"{type(stmt.value.value).__name__} (기본값: {stmt.value.value})"
                                            fields[target.attr] = val_str
                    
                    self.data_protocols[node.name] = {
                        "defined_in": rel_path_str,
                        "fields": fields
                    }
                
                # 🧱 2. 범용 레지스트리 상수 스캔: 폴더 불문! 모든 핵심 구동 클래스(플랫폼, 플레이어, 적 등)를 상수로 맵핑
                else:
                    if node.name not in ["AppState"]:
                        self.registry_constants[node.name] = f"{rel_path_str}::{node.name}"
                        
        except Exception:
            pass

    def index_file(self, file_path: Path):
        """
        ⚡ [Jjap-Compiler Core Router]
        더 이상 if/elif로 확장자를 구걸하지 않습니다. 
        core_parsers에서 동적 임포트된 플러그인 장부를 기반으로 무제한 자동 라우팅을 수행합니다.
        """
        ext = file_path.suffix.lower()
        
        # 🎯 1. 레이더 장부(self.parsers)에 현재 파일의 확장자가 등록되어 있는지 핀포인트 체크!
        if ext in self.parsers:
            # 장부에서 함수 오브젝트 자체를 낚아챕니다. (예: py_parser의 extract_symbols)
            extract_func = self.parsers[ext]
            
            try:
                # 🤝 약속된 마스터 단일 계약 조건에 따라 5대 장부를 통째로 징집합니다.
                symbols, file_ctx, def_map, protocols, registries = extract_func(file_path, self.project_root)
                
                # 💾 징집된 파서의 데이터를 메인 인덱서 통합 저장소에 실시간 누적 병합(Merge)
                self.symbols.extend(symbols)
                self.files_context.update(file_ctx)
                self.definition_map.update(def_map)
                self.data_protocols.update(protocols)
                
                # 중복 방지를 고려한 레지스트리 상수 등록
                for reg in registries:
                    if reg not in self.registry_constants:
                        self.registry_constants.append(reg)
                        
            except Exception as e:
                print(f"❌ [라우터 치명적 에러] {file_path.name} 파싱 중 외부 파서 플러그인 크래시 발생: {e}")
        else:
            # ℹ️ 지원하지 않는 확장자나 빈 파일은 가볍게 패스해 주는 방어선
            pass

    def scan_project(self):
        if SCAN_MODE == "ROOT":
            scan_target = self.project_root
            print("🎯 [Indexer] Mode: ROOT (프로젝트 원본 경로를 직접 진입하여 경로 에러를 완전 차단합니다)")
        else:
            scan_target = self.project_root / "src"
            print("🎯 [Indexer] Mode: SRC (순정 규격인 src/ 폴더 내부만 정밀 스캔합니다)")

        if not scan_target.exists():
            print(f"⚠️ [Indexer] 스캔 대상 경로가 존재하지 않아 중단합니다: {scan_target}")
            return

        # 🛡️ 인덱서가 수집 중에 절대 건드려서는 안 될 원자력 발전소(장부 및 지도 보관소) 선언
        EXCLUDE_KEYWORDS = [".venv", ".git", "__pycache__", "cline_tools", "system_memory", "system_maps"]

        for root, dirs, files in os.walk(scan_target, followlinks=True):
            normalized_root = root.replace("\\", "/")
            
            if "src/project_root/src" in normalized_root:
                continue

            # 폴더 전체 경로를 기준으로 시스템 제외 목록 필터링
            if any(kw in normalized_root for kw in EXCLUDE_KEYWORDS):
                continue

            for file in files:
                file_path = Path(root) / file

                # 🛡️ 장부 파일 자체를 열어서 인덱싱 장부에 수집하려는 무한 루프(꼬리물기) 방어
                if file_path.suffix in [".json", ".md"] and any(kw in file_path.as_posix() for kw in ["system_memory", "system_maps"]):
                    continue

                # SRC 모드일 때는 최상단 start.py 수집 패스
                if file == "start.py" and SCAN_MODE == "SRC":
                    continue

                # 💡 [형님 맞춤형 분기 정밀 보강]:
                # SRC 모드일 때는 무조건 파이썬만 수집 (.py)
                # ROOT 모드일 때는 파이썬이 아니더라도 모두 수집 대상으로 징집!
                if SCAN_MODE == "SRC" and file_path.suffix != ".py":
                    continue

                # 🎯 안전하게 수집 엔진으로 입고
                self.index_file(file_path)

                # ⭕ 안전핀만 채운 교체 코드 (기존 기능 유지, 에러만 차단)
                for s in self.symbols:
                    name_to_check = s.get("name")
                    s_id = s.get("symbol_id", "")  # 클래스 등 symbol_id가 없는 경우 방어
                    
                    if not name_to_check:
                        continue
                        
                    for target in self.symbols:
                        target_calls = target.get("calls", [])
                        target_id = target.get("symbol_id", "")
                        
                        # 안전하게 키가 존재할 때만 대조하여 종속성 연결
                        if name_to_check in target_calls and s_id and target_id and s_id != target_id:
                            if target_id not in s["used_by"]:
                                s["used_by"].append(target_id)
                                
                    s["used_by"] = sorted(list(set(s["used_by"])))

        # 🛠️ [격리 개조 포인트 2] 진짜 최상위 PROJECT_ROOT 기준으로 타깃 경로 절대 고정
        TARGET_MEMORY_DIR = PROJECT_ROOT / "system_memory"
        os.makedirs(TARGET_MEMORY_DIR, exist_ok=True)

        with open(TARGET_MEMORY_DIR / ".jjap_context.json", "w", encoding="utf-8") as f:
            json.dump({"files": self.files_context}, f, indent=2, ensure_ascii=False)
        with open(TARGET_MEMORY_DIR / ".jjap_symbols.json", "w", encoding="utf-8") as f:
            json.dump({"symbols": self.symbols}, f, indent=2, ensure_ascii=False)
        with open(TARGET_MEMORY_DIR / "definition_map.json", "w", encoding="utf-8") as f:
            json.dump(self.definition_map, f, indent=2, ensure_ascii=False)
        with open(TARGET_MEMORY_DIR / "data_protocols.json", "w", encoding="utf-8") as f:
            json.dump({"protocols": self.data_protocols}, f, indent=2, ensure_ascii=False)
        with open(TARGET_MEMORY_DIR / "registry_constants.json", "w", encoding="utf-8") as f:
            json.dump({"registered_entities": self.registry_constants}, f, indent=2, ensure_ascii=False)

        print(f"🧬 [Jjap-Indexer Universal] 5대 장부를 마스터 루트 하위 '{TARGET_MEMORY_DIR}' 구역으로 안전하게 격리 저장 완료!")


if __name__ == "__main__":
    # 🚨 기존 root = Path(__file__).parent.resolve() 방식을 버리고,
    # 상단에서 지독하게 정화해 둔 상위 마스터 PROJECT_ROOT를 직접 찔러 넣어 단독 실행 시에도 절대 오차가 없도록 고정합니다.
    print(f"⚡ [테스트 기동] 마스터 프로젝트 루트 탐색 좌표: {PROJECT_ROOT}")
    indexer = AdvancedIndexerV2(PROJECT_ROOT)
    indexer.scan_project()