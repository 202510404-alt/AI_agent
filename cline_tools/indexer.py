
import ast
import json
import hashlib
import os
from pathlib import Path
from typing import Dict, Any, List

# 🎯 영문 switch.py 콘솔 원격 연동
try:
    from cline_tools.switch import SCAN_MODE
except ImportError:
    SCAN_MODE = "ROOT"

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent  # 🔥 상위의 진짜 프로젝트 루트 강제 추적

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
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return

        rel_path = file_path.relative_to(self.project_root)
        rel_path_str = rel_path.as_posix()

        file_hash = self._get_sha256(content)
        skeleton = self._extract_skeleton(content)
        self.files_context[rel_path_str] = {
            "hash": file_hash,
            "mtime": int(file_path.stat().st_mtime),
            "skeleton": skeleton
        }

        # 동적 분배기 기동
        self.parse_protocols_and_registries(content, rel_path_str)

        try:
            tree = ast.parse(content)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    class_id = f"{rel_path_str}::{node.name}"
                    self.definition_map[node.name] = f"{rel_path_str}:{node.lineno}"
                    end_lineno = getattr(node, "end_lineno", node.lineno)
                    
                    self.symbols.append({
                        "symbol_id": class_id, "full_name": node.name, "name": node.name,
                        "type": "class", "parent": None, "file": rel_path_str,
                        "start_line": node.lineno, "end_line": end_lineno, "range": [node.lineno, end_lineno],
                        "decorators": [ast.dump(d) for d in node.decorator_list], "signature": f"class {node.name}",
                        "calls": [], "used_by": []
                    })
                    
                    for sub in node.body:
                        if isinstance(sub, ast.FunctionDef):
                            method_id = f"{class_id}.{sub.name}"
                            self.definition_map[f"{node.name}.{sub.name}"] = f"{rel_path_str}:{sub.lineno}"
                            sub_end_lineno = getattr(sub, "end_lineno", sub.lineno)
                            
                            calls = []
                            for expr in ast.walk(sub):
                                if isinstance(expr, ast.Call) and isinstance(expr.func, ast.Name):
                                    calls.append(expr.func.id)
                                elif isinstance(expr, ast.Call) and isinstance(expr.func, ast.Attribute):
                                    calls.append(expr.func.attr)

                            self.symbols.append({
                                "symbol_id": method_id, "full_name": f"{node.name}.{sub.name}", "name": sub.name,
                                "type": "method", "parent": node.name, "file": rel_path_str,
                                "start_line": sub.lineno, "end_line": sub_end_lineno, "range": [sub.lineno, sub_end_lineno],
                                "decorators": [ast.dump(d) for d in sub.decorator_list], "signature": f"def {sub.name}(...)",
                                "calls": list(set(calls)), "used_by": []
                            })
                            
                elif isinstance(node, ast.FunctionDef):
                    func_id = f"{rel_path_str}::{node.name}"
                    self.definition_map[node.name] = f"{rel_path_str}:{node.lineno}"
                    func_end_lineno = getattr(node, "end_lineno", node.lineno)
                    
                    self.symbols.append({
                        "symbol_id": func_id, "full_name": node.name, "name": node.name,
                        "type": "function", "parent": None, "file": rel_path_str,
                        "start_line": node.lineno, "end_line": func_end_lineno, "range": [node.lineno, func_end_lineno],
                        "decorators": [ast.dump(d) for d in node.decorator_list], "signature": f"def {node.name}(...)",
                        "calls": [], "used_by": []
                    })
        except Exception:
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

        for root, dirs, files in os.walk(scan_target, followlinks=True):
            normalized_root = root.replace("\\", "/")
            
            # 🚨 [여기 주의] 꼬인 중복 경로 예방선 유지
            if "src/project_root/src" in normalized_root:
                continue

            # 🛠️ [형님 수술 구역]: 무시 대상 목록에서 깡통 생성기였던 "src" 강제 추가를 제거합니다.
            # system_memory와 system_maps를 무시하여 인덱서 무한루프는 칼같이 방어합니다.
            excludes = [".venv", ".git", "__pycache__", "system_memory", "system_maps"]

            # 폴더명 단위가 아니라 전체 경로(normalized_root)를 기준으로 영리하게 검문합니다.
            if any(kw in normalized_root for kw in excludes):
                continue

            for file in files:
                # SRC 모드일 때는 최상단 start.py 수집을 패스합니다.
                if file == "start.py" and SCAN_MODE == "SRC":
                    continue
                if file.endswith(".py"):
                    # 🎯 정확하게 개별 파일 징집 입고
                    self.index_file(Path(root) / file)

        for s in self.symbols:
            name_to_check = s["name"]
            for target in self.symbols:
                if name_to_check in target.get("calls", []) and s["symbol_id"] != target["symbol_id"]:
                    s["used_by"].append(target["symbol_id"])
            s["used_by"] = sorted(list(set(s["used_by"])))

        # 🛠️ [격리 개조 포인트 2] 장부 출력 타겟 리다이렉트
        # 혹시 폴더가 없으면 에러가 터지므로 안전하게 자동 생성 로직 투입
        os.makedirs("system_memory", exist_ok=True)

        with open("system_memory/.jjap_context.json", "w", encoding="utf-8") as f:
            json.dump({"files": self.files_context}, f, indent=2, ensure_ascii=False)
        with open("system_memory/.jjap_symbols.json", "w", encoding="utf-8") as f:
            json.dump({"symbols": self.symbols}, f, indent=2, ensure_ascii=False)
        with open("system_memory/definition_map.json", "w", encoding="utf-8") as f:
            json.dump(self.definition_map, f, indent=2, ensure_ascii=False)
        with open("system_memory/data_protocols.json", "w", encoding="utf-8") as f:
            json.dump({"protocols": self.data_protocols}, f, indent=2, ensure_ascii=False)
        with open("system_memory/registry_constants.json", "w", encoding="utf-8") as f:
            json.dump({"registered_entities": self.registry_constants}, f, indent=2, ensure_ascii=False)

        print(f"🧬 [Jjap-Indexer Universal] 5대 장부를 'system_memory/' 구역으로 안전하게 격리 저장 완료!")

if __name__ == "__main__":
    root = Path(__file__).parent.resolve()
    indexer = AdvancedIndexerV2(root)
    indexer.scan_project()