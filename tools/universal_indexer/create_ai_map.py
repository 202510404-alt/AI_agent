import os
import ast
import json
from pathlib import Path

try:
    from tools.universal_indexer.switch import SCAN_MODE
except ImportError:
    SCAN_MODE = "ROOT"

# ======================================================================
# 🎯 [경로 방어선 절대 고정]
# ======================================================================
SCRIPT_DIR = Path(__file__).parent.resolve()

if SCRIPT_DIR.name == "universal_indexer" and SCRIPT_DIR.parent.name == "tools":
    PROJECT_ROOT = SCRIPT_DIR.parent.parent
else:
    PROJECT_ROOT = SCRIPT_DIR

OUTPUT_DIR = PROJECT_ROOT / "system_maps"
OUTPUT_FILE_PATH = OUTPUT_DIR / "AI_CODEBASE_MAP.md"
REGISTRY_JSON_PATH = PROJECT_ROOT / "system_memory" / "registry_constants.json"
PROTOCOL_JSON_PATH = PROJECT_ROOT / "system_memory" / "data_protocols.json"

# 🛡️ 제외 키워드 목록
EXCLUDE_KEYWORDS = [
    "node_modules",
    ".venv", 
    ".git", 
    "__pycache__", 
    "cline_tools", 
    ".json", 
    ".md", 
    "system_memory", 
    "system_maps"
]


def load_jjap_context():
    """통합 .jjap_context.json 장부 로드"""
    context_path = PROJECT_ROOT / "system_memory" / ".jjap_context.json"
    if not context_path.exists():
        context_path = PROJECT_ROOT / ".jjap_context.json"
        
    if context_path.exists():
        try:
            with open(context_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("files", {})
        except Exception as e:
            print(f"⚠️ [.jjap_context.json] 로드 중 오류 발생: {e}")
    else:
        print("⚠️ [.jjap_context.json] 통합 장부 파일을 찾을 수 없습니다. 인덱서를 먼저 실행해 주세요.")
    return {}


def collect_target_files():
    """프로젝트 내 대상 파일 수집 (디버그 도배 제거 버전)"""
    if SCAN_MODE == "ROOT":
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
            if file == "start.py" and SCAN_MODE == "SRC":
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
    """심볼 장부 기반 매칭 테이블 완성"""
    path_to_registry = {}
    path_to_protocol = {}

    registry_data = load_registry()
    protocol_data = load_protocols()

    symbols_path = PROJECT_ROOT / "system_memory" / ".jjap_symbols.json"
    if not symbols_path.exists():
        symbols_path = PROJECT_ROOT / ".jjap_symbols.json"

    all_symbols = []
    if symbols_path.exists():
        try:
            with open(symbols_path, "r", encoding="utf-8") as f:
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


def main():
    target_files = collect_target_files()
    jjap_context = load_jjap_context()
    path_to_registry, path_to_protocol = parse_protocols_and_registries()

    OUTPUT_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as f:
        printed_dirs = set()

        f.write("# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)\n\n")
        f.write("> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.\n")
        f.write("> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.\n\n")
        
        if SCAN_MODE == "EXTRACTION_TARGET_PROJECT":
            f.write("```markdown\nextraction_target_project/\n")
        else:
            f.write("```markdown\nproject_root/\n")
        
        for file_path in target_files:
            rel_path = file_path.relative_to(PROJECT_ROOT)
            posix_rel_path = rel_path.as_posix()
            file_name = file_path.name

            if SCAN_MODE == "EXTRACTION_TARGET_PROJECT" and posix_rel_path.startswith("extraction_target_project/"):
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

    print("🎯 [마스터 공장] 'system_maps/AI_CODEBASE_MAP.md'가 모든 파일 구조를 포함하여 안전하게 자동 갱신되었습니다!")


def generate_ai_optimized_map():
    main()


if __name__ == "__main__":
    main()