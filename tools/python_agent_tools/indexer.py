
import ast
import json
import hashlib
import os
from pathlib import Path
from typing import Dict, Any, List

# 🎯 영문 switch.py 콘솔 원격 연동
try:
    from switch import SCAN_MODE
except ImportError:
    SCAN_MODE = "ROOT"

SCRIPT_DIR = Path(__file__).parent.resolve()
if SCRIPT_DIR.name == "python_agent_tools" and SCRIPT_DIR.parent.name == "tools":
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
      - 파일 내부에 'Variables'나 'vars'가 들어간 클래스가 있으면 데이터 프로토콜 장부로 자동 분류.
      - 그 외에 일반적인 엔티티, 플랫폼, 카메라 등의 모든 핵심 클래스는 레지스트리 상수로 100% 자동 징집.
    """
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.symbols: List[Dict[str, Any]] = []
        self.files_context: Dict[str, Any] = {}
        self.definition_map: Dict[str, str] = {}
        
        # 🎯 [보조 지식 장부 변수]
        self.data_protocols: Dict[str, Any] = {}
        self.registry_constants: Dict[str, str] = {}

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
        # 마스터 루트 기준의 올바른 상대 경로 추출
        rel_path_str = file_path.relative_to(self.project_root).as_posix()
        
        try:
            mtime = int(file_path.stat().st_mtime)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            file_hash = self._get_sha256(content)

            # 💡 [형님 맞춤형 분기] 파이썬 파일일 때만 내부 클래스/함수 정밀 분석
            if file_path.suffix == ".py":
                skeleton = self._extract_skeleton(content)
                self.parse_protocols_and_registries(content, rel_path_str)
                
                # 심볼 맵 구성 로직
                try:
                    tree = ast.parse(content)
                    for node in tree.body:
                        if isinstance(node, ast.ClassDef):
                            self.definition_map[node.name] = f"{rel_path_str}:{node.lineno}"
                            for sub in node.body:
                                if isinstance(sub, ast.FunctionDef):
                                    self.definition_map[f"{node.name}.{sub.name}"] = f"{rel_path_str}:{sub.lineno}"
                        elif isinstance(node, ast.FunctionDef):
                            self.definition_map[node.name] = f"{rel_path_str}:{node.lineno}"
                except Exception:
                    pass
            else:
                # 💡 [형님 맞춤형 분기] 비-파이썬 파일은 문법 에러를 내지 않고 안전하게 경로와 기본 정보만 보존!
                skeleton = f"Non-Python File ({file_path.suffix.upper()})"

            # 장부에 안전하게 세이브
            self.files_context[rel_path_str] = {
                "hash": file_hash,
                "mtime": mtime,
                "skeleton": skeleton
            }
        except Exception as e:
            print(f"⚠️ [파일 수집 예외 패스] {rel_path_str}: {str(e)}")

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

        for s in self.symbols:
            name_to_check = s["name"]
            for target in self.symbols:
                if name_to_check in target.get("calls", []) and s["symbol_id"] != target["symbol_id"]:
                    s["used_by"].append(target["symbol_id"])
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