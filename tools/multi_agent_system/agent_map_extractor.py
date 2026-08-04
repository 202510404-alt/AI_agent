"""Agent AI Codebase Map Extractor Controller.

[에이전트 AI 코드베이스맵 추출요청 관리자]
기존 create_ai_map.py의 정밀한 심볼/관계망 렌더링 엔진을 계승하면서,
스위치 기반의 고정 범위(ROOT/EXTRACTION_TARGET) 한계를 극복하고
에이전트가 요청한 특정 폴더/파일 경로만 타깃팅하여 유연하게 AI_CODEBASE_MAP을 생성 및 반환합니다.
"""

import json
import os
import sys
from pathlib import Path

# 🔄 프로젝트 루트를 Python 모듈 검색 경로(sys.path) 최상단에 자동 등록
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent if (SCRIPT_DIR.name == "multi_agent_system" and SCRIPT_DIR.parent.name == "tools") else SCRIPT_DIR
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from typing import List, Optional, Union, Dict, Any, Tuple
from tools.universal_indexer.map_formatter import format_symbol_node # ✅ 이제 정상 로드됨

# 🔄 마스터 루트 역추적 (tools/multi_agent_system/ 에 위치함을 보장)
SCRIPT_DIR = Path(__file__).parent.resolve()
if SCRIPT_DIR.name == "multi_agent_system" and SCRIPT_DIR.parent.name == "tools":
    PROJECT_ROOT = SCRIPT_DIR.parent.parent
else:
    PROJECT_ROOT = SCRIPT_DIR

# 장부 경로 정의
SYSTEM_MEMORY_DIR = PROJECT_ROOT / "system_memory"
SYSTEM_MAPS_DIR = PROJECT_ROOT / "system_maps"

CONTEXT_JSON_PATH = SYSTEM_MEMORY_DIR / ".jjap_context.json"
SYMBOLS_JSON_PATH = SYSTEM_MEMORY_DIR / ".jjap_symbols.json"
REGISTRY_JSON_PATH = SYSTEM_MEMORY_DIR / "registry_constants.json"
PROTOCOL_JSON_PATH = SYSTEM_MEMORY_DIR / "data_protocols.json"
CUSTOM_AI_MAP_PATH = SYSTEM_MAPS_DIR / "CUSTOM_AI_CODEBASE_MAP.md"

EXCLUDE_KEYWORDS = [
    "node_modules", ".venv", ".git", "__pycache__",
    "cline_tools", "system_memory", "system_maps", "dist", "build"
]


class AgentMapExtractor:
    """에이전트의 유연한 부분 코드베이스 맵 추출 요청을 처리하는 클래스"""

    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.project_root = project_root

    def _load_jjap_context(self) -> Dict[str, Any]:
        if CONTEXT_JSON_PATH.exists():
            try:
                with open(CONTEXT_JSON_PATH, "r", encoding="utf-8") as f:
                    return json.load(f).get("files", {})
            except Exception as e:
                print(f"⚠️ [SWITCH WARNING] switch.py를 로드하지 못해 기본 'ROOT' 모드로 동작합니다. (이유: {str(e)})")
        return {}

    def _load_all_symbols(self) -> Tuple[Dict[str, List[Dict]], Dict[str, Dict]]:
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
                print(f"⚠️ [.jjap_symbols.json] 로드 실패: {e}")
        return symbols_by_file, symbol_by_id

    def _load_registry_and_protocols(self) -> Tuple[Dict[str, set], Dict[str, Any]]:
        path_to_registry = {}
        path_to_protocol = {}
        
        registry_data = set()
        if REGISTRY_JSON_PATH.exists():
            try:
                with open(REGISTRY_JSON_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    entities = data.get("registered_entities", [])
                    registry_data = set(entities) if isinstance(entities, list) else set(entities.keys())
            except Exception:
                pass

        protocol_data = {}
        if PROTOCOL_JSON_PATH.exists():
            try:
                with open(PROTOCOL_JSON_PATH, "r", encoding="utf-8") as f:
                    protocol_data = json.load(f).get("protocols", {})
            except Exception:
                pass

        symbols_by_file, _ = self._load_all_symbols()
        for file_path, sym_list in symbols_by_file.items():
            for sym in sym_list:
                if sym.get("type") != "class":
                    continue
                cls_name = sym.get("name")
                if not cls_name:
                    continue
                
                posix_rel_path = Path(file_path).as_posix()
                if cls_name in registry_data:
                    path_to_registry.setdefault(posix_rel_path, set()).add(cls_name)
                if cls_name in protocol_data:
                    path_to_protocol.setdefault(posix_rel_path, []).append((cls_name, protocol_data[cls_name]))

        return path_to_registry, path_to_protocol

    def _normalize_path(self, raw_path: Union[str, Path]) -> Path:
        """💡 외부/에이전트 입력 경로를 PROJECT_ROOT 기준 안전 정규화 (하드코딩 방지)"""
        path_obj = Path(raw_path)
        if path_obj.is_absolute():
            try:
                return path_obj.relative_to(self.project_root)
            except ValueError:
                return path_obj
        return path_obj

    def collect_files_in_targets(
        self, 
        target_paths: Optional[List[Union[str, Path]]] = None, 
        exclude_paths: Optional[List[Union[str, Path]]] = None
    ) -> List[Path]:
        """지정한 상대 경로/폴더 목록 내부의 파일들을 정밀 수집합니다. (지정 안 할 시 ROOT 전체)"""
        target_files = set()
        excludes = [self._normalize_path(e).as_posix() for e in (exclude_paths or [])]

        # 💡 범위가 전달되지 않거나 빈 리스트일 경우 루트 디렉토리 전체 지정
        effective_targets = target_paths if target_paths else [self.project_root]

        for target in effective_targets:
            norm_target = self._normalize_path(target)
            abs_target = (self.project_root / norm_target).resolve()
            if not abs_target.exists():
                print(f"⚠️ [경고] 요청한 경로가 존재하지 않습니다: {target}")
                continue

            if abs_target.is_file():
                rel_posix = abs_target.relative_to(self.project_root).as_posix()
                if not any(ex in rel_posix for ex in excludes):
                    target_files.add(abs_target)
            elif abs_target.is_dir():
                for root, dirs, files in os.walk(abs_target, followlinks=True):
                    normalized_root = root.replace("\\", "/")
                    if any(kw in normalized_root for kw in EXCLUDE_KEYWORDS):
                        continue
                    
                    rel_root = Path(root).relative_to(self.project_root).as_posix()
                    if any(ex in rel_root for ex in excludes):
                        continue

                    for file in files:
                        full_path = Path(root) / file
                        rel_file = full_path.relative_to(self.project_root).as_posix()
                        if not any(ex in rel_file for ex in excludes):
                            target_files.add(full_path)

        return sorted(list(target_files))

    def generate_custom_map(
        self, 
        target_paths: Optional[List[Union[str, Path]]] = None, 
        exclude_paths: Optional[List[Union[str, Path]]] = None,
        save_to_file: bool = True
    ) -> str:
        """
        에이전트가 지시한 target_paths 영역을 정밀하게 쪼개어 AI 코드베이스 맵 문자열을 생성합니다.
        (target_paths 미입력 시 프로젝트 전체 추출)
        """
        target_files = self.collect_files_in_targets(target_paths, exclude_paths)
        jjap_context = self._load_jjap_context()
        symbols_by_file, symbol_by_id = self._load_all_symbols()
        path_to_registry, path_to_protocol = self._load_registry_and_protocols()

        output_lines = []
        output_lines.append("# 🏗️ CUSTOM TARGETED AI-OPTIMIZED CODEBASE MAP\n")
        output_lines.append(f"> **[추출 범위 지정]** Target Paths: `{target_paths}`\n")
        output_lines.append("```markdown\nproject_root/\n")

        printed_dirs = set()

        for file_path in target_files:
            rel_path = file_path.relative_to(self.project_root)
            posix_rel_path = rel_path.as_posix()
            file_name = file_path.name

            parts = Path(posix_rel_path).parts
            for i in range(len(parts) - 1):
                current_dir_path = Path(*parts[:i + 1]).as_posix()
                if current_dir_path not in printed_dirs:
                    printed_dirs.add(current_dir_path)
                    indent = "│   " * i
                    output_lines.append(f"{indent}├── {parts[i]}/\n")

            indent = "│   " * (len(parts) - 1)
            file_meta = jjap_context.get(posix_rel_path, {})
            symbols_info = file_meta.get("symbols_summary", "")

            if symbols_info:
                output_lines.append(f"{indent}├── {file_name} [📂 {posix_rel_path}] -> [{symbols_info}]\n")
            else:
                output_lines.append(f"{indent}├── {file_name} [📂 {posix_rel_path}]\n")

            # 레지스트리 / 프로토콜 표시
            if posix_rel_path in path_to_registry:
                for reg_const in path_to_registry[posix_rel_path]:
                    output_lines.append(f"{indent}│     ├── 🔑 [REGISTRY]: \"{reg_const}\"\n")

            if posix_rel_path in path_to_protocol:
                for proto_name, fields in path_to_protocol[posix_rel_path]:
                    output_lines.append(f"{indent}│     ├── 📊 [PROTOCOL]: \"{proto_name}\"\n")

            # 심볼 상세 트리 (L라인, CALLS, USED BY)
            file_symbols = symbols_by_file.get(posix_rel_path, [])
            for sym in file_symbols:
                formatted_lines = format_symbol_node(sym, symbol_by_id, posix_rel_path, indent)
                output_lines.extend(formatted_lines)

        output_lines.append("```\n")
        final_map_str = "".join(output_lines)

        if save_to_file:
            CUSTOM_AI_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(CUSTOM_AI_MAP_PATH, "w", encoding="utf-8") as f:
                f.write(final_map_str)
            print(f"🎯 [에이전트 맵 추출기] Custom AI Map 생성 완료: {CUSTOM_AI_MAP_PATH}")

        return final_map_str


# 💡 간단 가동 모듈 함수 인터페이스 (target_paths 기본값을 None으로 지정)
def extract_targeted_ai_map(target_paths: Optional[List[str]] = None, exclude_paths: Optional[List[str]] = None) -> str:
    extractor = AgentMapExtractor()
    return extractor.generate_custom_map(target_paths, exclude_paths)


if __name__ == "__main__":
    # 테스트 구동: 인자 없이 호출 시 ROOT 전체 맵 추출
    result = extract_targeted_ai_map()
    print(result[:500] + "\n... [중략] ...")