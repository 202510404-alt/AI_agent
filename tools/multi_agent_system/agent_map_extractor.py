"""Agent AI Codebase Map Extractor Controller.

[에이전트 AI 코드베이스맵 추출요청 관리자]
기존 create_ai_map.py의 정밀한 심볼/관계망 렌더링 엔진을 계승하면서,
스위치 기반의 고정 범위(ROOT/EXTRACTION_TARGET) 한계를 극복하고
에이전트가 요청한 특정 폴더/파일 경로만 타깃팅하여 유연하게 AI_CODEBASE_MAP을 생성 및 반환합니다.
"""

import json
import os
from pathlib import Path
from typing import List, Optional, Union, Dict, Any, Tuple

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

    def collect_files_in_targets(
        self, 
        target_paths: List[Union[str, Path]], 
        exclude_paths: Optional[List[Union[str, Path]]] = None
    ) -> List[Path]:
        """지정한 상대 경로/폴더 목록 내부의 파일들을 정밀 수집합니다."""
        target_files = set()
        excludes = [Path(e).as_posix() for e in (exclude_paths or [])]

        for target in target_paths:
            abs_target = self.project_root / target
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
        target_paths: List[Union[str, Path]], 
        exclude_paths: Optional[List[Union[str, Path]]] = None,
        save_to_file: bool = True
    ) -> str:
        """
        에이전트가 지시한 target_paths 영역만 정밀하게 쪼개어 AI 코드베이스 맵 문자열을 생성합니다.
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
                sym_type = sym.get("type", "function")
                sym_name = sym.get("name", "")
                full_name = sym.get("full_name", sym_name)
                if not sym_name:
                    continue

                raw_args = sym.get("args")
                if isinstance(raw_args, list):
                    args_str = f"({', '.join(raw_args)})" if raw_args else ""
                elif isinstance(raw_args, str) and raw_args:
                    args_str = f"({raw_args})"
                else:
                    args_str = ""

                start_line = sym.get("start_line")
                end_line = sym.get("end_line")
                line_str = f"[L{start_line}-L{end_line}]" if start_line and end_line and start_line != end_line else (f"[L{start_line}]" if start_line else "")

                if sym_type == "class":
                    icon_str = f"🧬 class {sym_name}"
                elif sym_type == "json_key":
                    icon_str = f"🔑 key \"{sym_name}\""
                else:
                    icon_str = f"🎯 def {sym_name}{args_str if args_str else '()'}"

                output_lines.append(f"{indent}│   ├── {icon_str} {line_str}\n".rstrip() + "\n")

                # CALLS & USED BY
                calls = sym.get("calls", [])
                if calls:
                    output_lines.append(f"{indent}│   │   ├── 📞 [CALLS]: {', '.join(calls)}\n")

                used_by_ids = sym.get("used_by", [])
                if used_by_ids:
                    used_by_info = []
                    for u_id in used_by_ids:
                        target = symbol_by_id.get(u_id)
                        if target:
                            u_file = target.get("file") or target.get("path", "")
                            u_name = target.get("name", "")
                            used_by_info.append(f"::{u_name}" if u_file == posix_rel_path else f"{u_file}::{u_name}")
                        else:
                            used_by_info.append(str(u_id))
                    output_lines.append(f"{indent}│   │   ├── 🔗 [USED BY]: {', '.join(used_by_info)}\n")

        output_lines.append("```\n")
        final_map_str = "".join(output_lines)

        if save_to_file:
            CUSTOM_AI_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(CUSTOM_AI_MAP_PATH, "w", encoding="utf-8") as f:
                f.write(final_map_str)
            print(f"🎯 [에이전트 맵 추출기] Custom AI Map 생성 완료: {CUSTOM_AI_MAP_PATH}")

        return final_map_str


# 💡 간단 가동 모듈 함수 인터페이스
def extract_targeted_ai_map(target_paths: List[str], exclude_paths: Optional[List[str]] = None) -> str:
    extractor = AgentMapExtractor()
    return extractor.generate_custom_map(target_paths, exclude_paths)


if __name__ == "__main__":
    # 테스트 구동: 원하는 특정 폴더만 타깃으로 맵 생성
    sample_targets = ["agent_core/plan", "tools/multi_agent_system"]
    result = extract_targeted_ai_map(sample_targets)
    print(result[:500] + "\n... [중략] ...")