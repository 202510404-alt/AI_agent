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
# 현재 스크립트 파일 위치를 기준으로 진짜 프로젝트 마스터 루트를 추적합니다.
# 폴더 구조가 tools/universal_indexer/ 로 1단계 더 깊어졌으므로,
# "universal_indexer" 폴더 안에 있고 그 상위 폴더가 "tools"일 때만
# 두 단계 위(.parent.parent)를 진짜 루트로 판정합니다.
# 그 외의 경우(예: 단독 실행, 다른 위치로 복사됨 등)는 현재 폴더를 루트로 안전하게 폴백합니다.
# ======================================================================
SCRIPT_DIR = Path(__file__).parent.resolve()
# 🔄 폴더 물리 명칭이 변경되었으므로 검사 타깃 문자열을 똑같이 싱크해 줍니다.
if SCRIPT_DIR.name == "universal_indexer" and SCRIPT_DIR.parent.name == "tools":
    PROJECT_ROOT = SCRIPT_DIR.parent.parent
else:
    PROJECT_ROOT = SCRIPT_DIR

# 🚨 [경로 교정 핵심] indexer.py가 "실제로" 파일을 쓰는 위치와 100% 일치시킴
#    - 인덱서 장부(registry/protocol)는 system_memory/ 에 있음
#    - 결과물 지도는 update_map.py와 동일하게 system_maps/ 에 저장
OUTPUT_DIR = PROJECT_ROOT / "system_maps"
OUTPUT_FILE_PATH = OUTPUT_DIR / "AI_CODEBASE_MAP.md"
REGISTRY_JSON_PATH = PROJECT_ROOT / "system_memory" / "registry_constants.json"
PROTOCOL_JSON_PATH = PROJECT_ROOT / "system_memory" / "data_protocols.json"

# 🛡️ indexer.py의 scan_project()와 동일한 제외 규칙
EXCLUDE_KEYWORDS = [".venv", ".git", "__pycache__", "system_memory", "system_maps"]


def parse_python_file(file_path: Path):
    """[형님 원본 규격 100% 완벽 보존] 실시간으로 라인 범위, 클래스/함수, 임포트를 징집합니다."""
    compact_symbols_info = []
    imports = []
    structural_symbols = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)

        for node in tree.body:
            # 1. 외부 모듈 임포트 추적
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                else:
                    module_name = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module_name}.{alias.name}" if module_name else alias.name)

            # 2. 클래스 정의 및 내부 메서드 추적 (라인 범위 포함)
            elif isinstance(node, ast.ClassDef):
                class_start = node.lineno
                class_end = getattr(node, "end_lineno", class_start)
                class_info = f"🧬 class {node.name} [L{class_start}-{class_end}]"
                structural_symbols.append(class_info)

                for sub_node in node.body:
                    if isinstance(sub_node, ast.FunctionDef):
                        func_start = sub_node.lineno
                        func_end = getattr(sub_node, "end_lineno", func_start)

                        args_list = [a.arg for a in sub_node.args.args]
                        if "self" in args_list:
                            args_list.remove("self")
                        args_str = ", ".join(args_list)

                        func_info = f"   └─ def {sub_node.name}({args_str}) [L{func_start}-{func_end}]"
                        structural_symbols.append(func_info)

            # 3. 단독 전역 함수 추적 (라인 범위 포함)
            elif isinstance(node, ast.FunctionDef):
                func_start = node.lineno
                func_end = getattr(node, "end_lineno", func_start)
                args_list = [a.arg for a in node.args.args]
                args_str = ", ".join(args_list)
                func_info = f"🎯 def {node.name}({args_str}) [L{func_start}-{func_end}]"
                structural_symbols.append(func_info)

        if imports:
            clean_imports = sorted(list(set(imports)))[:6]
            compact_symbols_info.append(f"💡 📦 imp: {', '.join(clean_imports)}")
        if structural_symbols:
            compact_symbols_info.extend(structural_symbols)

    except Exception as e:
        return [f"⚠️ [AST 파싱 실패]: {e}"]

    return compact_symbols_info


def collect_target_files():
    """[수정] .py 제한을 해제하고, 제외 키워드가 없는 프로젝트 내의 '모든 파일'을 수집합니다."""
    print("=" * 80)
    print("[DEBUG] collect_target_files() 시작")
    print(f"[DEBUG] PROJECT_ROOT = {PROJECT_ROOT}")
    print(f"[DEBUG] SCAN_MODE    = {SCAN_MODE}")
    print("=" * 80)
    if SCAN_MODE == "ROOT":
        scan_target = PROJECT_ROOT
        print("🎯 [create_ai_map] Mode: ROOT (프로젝트 전체 경로를 직접 스캔합니다)")
    else:
        scan_target = PROJECT_ROOT / "src"
        print("🎯 [create_ai_map] Mode: SRC (src/ 폴더 내부만 정밀 스캔합니다)")

    if not scan_target.exists():
        print(f"❌ [오류] 스캔 대상 경로가 존재하지 않습니다: {scan_target}")
        return []

    print(f"[DEBUG] SCAN_TARGET  = {scan_target}")

    target_files = []
    for root, dirs, files in os.walk(scan_target, followlinks=True):
        normalized_root = root.replace("\\", "/")

        print("\n------------------------------------------------------")
        print(f"[DEBUG] WALK ROOT : {root}")
        print(f"[DEBUG] DIR COUNT : {len(dirs)}")
        print(f"[DEBUG] FILE COUNT: {len(files)}")

        if "src/project_root/src" in normalized_root:
            print(f"[SKIP] duplicated path : {normalized_root}")
            continue
        if any(kw in normalized_root for kw in EXCLUDE_KEYWORDS):
            print(f"[SKIP] excluded keyword : {normalized_root}")
            continue

        print("[DIRS]")
        for d in dirs:
            print("   ", d)

        print("[FILES]")
        for file in files:
            print("   ", file)

        for file in files:
            if file == "start.py" and SCAN_MODE == "SRC":
                continue
            
            # 💡 [교정] 특정 확장자 차단 해제 -> 모든 파일을 수집 대상으로 포함
            full_path = Path(root) / file
            print(f"[ADD] {full_path}")
            target_files.append(full_path)

    print("=" * 80)
    print("[DEBUG] collect_target_files END")
    print(f"[DEBUG] TOTAL FILES = {len(target_files)}")
    print("=" * 80)

    return sorted(target_files)


def load_registry():
    """
    🔑 [Universal Registry Loader]
    신형 인덱서가 내뱉는 어떠한 형태의 데이터 구조도 유연하게 수용합니다.
    자바스크립트, C# 등 미래의 노동자 파서가 합류하여 형식이 변해도 절대 크래시가 나지 않습니다.
    """
    if not REGISTRY_JSON_PATH.exists():
        return set()
    try:
        with open(REGISTRY_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Case A: {"registered_entities": [...]} 로 감싸진 완벽한 신형 포맷
            if isinstance(data, dict) and "registered_entities" in data:
                entities = data["registered_entities"]
                if isinstance(entities, list):
                    return set(entities)
                elif isinstance(entities, dict):
                    return set(entities.keys())

            # Case B: 파일 경로별 딕셔너리 구조 { "path": [...] } 로 유입될 경우 호환
            if isinstance(data, dict):
                extracted = set()
                for k, v in data.items():
                    if isinstance(v, list):
                        for item in v: extracted.add(str(item))
                    else:
                        extracted.add(str(k))
                return extracted

            # Case C: 단순 순정 리스트 구조로 유입될 경우
            if isinstance(data, list):
                return set(str(x) for x in data)

            return set()
    except Exception as e:
        print(f"⚠️ [맵메이커 방어선] 레지스트리 로드 실패 우회: {e}")
        return set()


def load_protocols():
    """
    📊 [Universal Protocol Loader]
    신형 인덱서의 {"protocols": {...}} 마스터 구조를 안전하게 분해 및 흡수합니다.
    """
    if not PROTOCOL_JSON_PATH.exists():
        return {}
    try:
        with open(PROTOCOL_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Case A: {"protocols": {...}} 신형 포맷 대응
            if isinstance(data, dict) and "protocols" in data:
                return data["protocols"]
                
            # Case B: 평평한 순정 딕셔너리 구조
            if isinstance(data, dict):
                return data
                
            return {}
    except Exception as e:
        print(f"⚠️ [맵메이커 방어선] 프로토콜 로드 실패 우회: {e}")
        return {}


def parse_protocols_and_registries():
    """
    🧠 [Dynamic Map Matcher]
    장부에서 수집된 레지스트리와 프로토콜 데이터를 기반으로 
    소스코드 맵에 이정표(🔑, 📊)를 꽂아주기 위한 매칭 딕셔너리를 유연하게 생성합니다.
    """
    path_to_registry = {}
    path_to_protocol = {}

    # 유연하게 진화한 로더를 통해 데이터를 정제된 형태로 징집
    registry_set = load_registry()
    protocols_dict = load_protocols()

    # 인덱서가 가공해 둔 컨텍스트 장부(.jjap_context.json)를 참조하여 파일별 매칭 링크를 완성합니다.
    context_path = PROJECT_ROOT / "system_memory" / ".jjap_context.json"
    if context_path.exists():
        try:
            with open(context_path, "r", encoding="utf-8") as f:
                ctx_data = json.load(f)
                files_info = ctx_data.get("files", {})
                
                for rel_path, f_meta in files_info.items():
                    # 해당 파일에 포함된 클래스 목록 추적
                    classes_in_file = f_meta.get("classes", [])
                    
                    # 1. 레지스트리 매칭
                    for cls in classes_in_file:
                        if cls in registry_set:
                            if rel_path not in path_to_registry:
                                path_to_registry[rel_path] = []
                            if cls not in path_to_registry[rel_path]:
                                path_to_registry[rel_path].append(cls)
                                
                    # 2. 프로토콜 매칭
                    for cls in classes_in_file:
                        if cls in protocols_dict:
                            if rel_path not in path_to_protocol:
                                path_to_protocol[rel_path] = []
                            path_to_protocol[rel_path].append((cls, protocols_dict[cls]))
        except Exception as e:
            print(f"⚠️ [맵메이커 방어선] 컨텍스트 연동 중 오류 발생: {e}")

    return path_to_registry, path_to_protocol


def main():
    target_files = collect_target_files()
    print(f"[MAIN] target_files received : {len(target_files)}")
    if not target_files:
        return

    print(f"🔍 [디버그] 스캔 타깃 파일 수집 완료: 총 {len(target_files)}개 탐색됨 (비-파이썬 파일 포함)")

    path_to_registry = load_registry()
    path_to_protocol = load_protocols()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if OUTPUT_FILE_PATH.exists():
        try:
            OUTPUT_FILE_PATH.unlink()
        except Exception:
            pass

    with open(OUTPUT_FILE_PATH, "w", encoding="utf-8", newline="") as f:
        f.write("# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)\n\n")
        f.write("> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.\n")
        f.write("> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.\n\n")

        f.write("```markdown\n")
        f.write("project_root/\n")

        printed_dirs = set()

        for file_path in target_files:
            print(f"[WRITE] {file_path}")
            rel_path = file_path.relative_to(PROJECT_ROOT)
            parts = rel_path.parts

            print(f"[REL] {rel_path}")
            print(f"[PARTS] {parts}")

            # 디렉터리 트리 라인 출력 생성
            print("[DIR CREATE]")
            for i in range(1, len(parts)):
                current_dir_path = Path(*parts[:i])
                print(current_dir_path)
                if current_dir_path not in printed_dirs:
                    dir_indent = "│   " * (i - 1)
                    f.write(f"{dir_indent}├── {parts[i-1]}/\n")
                    printed_dirs.add(current_dir_path)

            indent = "│   " * (len(parts) - 1)
            file_name = parts[-1]
            print(f"[WRITE FILE] {file_name}")
            posix_rel_path = rel_path.as_posix()

            # 💡 [교정] 파이썬 파일일 때만 내부 심볼(AST)을 분석하고, 나머지는 경로만 출력합니다.
            if file_name.endswith(".py"):
                symbols_info = parse_python_file(file_path)
                symbols_str = " | ".join(symbols_info) if symbols_info else ""
            else:
                symbols_str = "" # 파이썬이 아니면 심볼 분석 생략

            if symbols_str:
                f.write(f"{indent}├── {file_name} [📂 {posix_rel_path}] -> [{symbols_str}]\n")
            else:
                f.write(f"{indent}├── {file_name} [📂 {posix_rel_path}]\n")

            # 레지스트리 및 프로토콜 정보 출력 유지
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
    print("=" * 80)
    print("[SUMMARY]")
    print(f"Directories Printed : {len(printed_dirs)}")
    print(f"Files Written       : {len(target_files)}")
    print("=" * 80)

    with open("scan_debug.txt", "w", encoding="utf-8") as dbg:
        dbg.write("==== ALL FILES ====\n")
        for p in target_files:
            dbg.write(str(p) + "\n")

    print(f"🎯 [마스터 공장] 'system_maps/AI_CODEBASE_MAP.md'가 모든 파일 구조를 포함하여 안전하게 자동 갱신되었습니다 형님!")


# ======================================================================
# 🔗 [파이프라인 결합 방어선]
# jjap_watcher.py가 호출하는 함수명을 완벽하게 지원하기 위한 브릿지 래퍼 함수
# ======================================================================
def generate_ai_optimized_map():
    """jjap_watcher.py의 실시간 갱신 요청을 수신하여 내부 메인 공장을 가동합니다."""
    main()


if __name__ == "__main__":
    main()
