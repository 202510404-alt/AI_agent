import os
import ast
import json
from pathlib import Path

from tools.universal_indexer.config import (
    PROJECT_ROOT,
    get_scan_mode,
    EXCLUDE_KEYWORDS,
    CONTEXT_JSON_PATH,
    SYMBOLS_JSON_PATH,
    REGISTRY_JSON_PATH,
    PROTOCOL_JSON_PATH,
    AI_MAP_MD_PATH
)
from map_formatter import format_symbol_node, get_file_symbols_summary


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
            symbols_info = get_file_symbols_summary(file_meta)

            if not symbols_info and posix_rel_path.startswith("extraction_target_project/extraction_target_project/"):
                shorter_path = posix_rel_path.replace("extraction_target_project/extraction_target_project/", "extraction_target_project/", 1)
                symbols_info = get_file_symbols_summary(jjap_context.get(shorter_path, {}))

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


if __name__ == "__main__":
    main()