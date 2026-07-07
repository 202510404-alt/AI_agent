import os
import ast
import json
from pathlib import Path

# ======================================================================
# 🎯 [스캔 모드 연동] indexer.py와 완전히 동일한 방식으로 switch.py를 참조합니다.
# cline_tools를 패키지로 import 할 수 없는 실행 환경이면 기본값 "ROOT"로 안전하게 폴백합니다.
# ======================================================================
try:
    from cline_tools.switch import SCAN_MODE
except ImportError:
    SCAN_MODE = "ROOT"

# ======================================================================
# 🎯 [경로 방어선 절대 고정]
# 현재 스크립트 파일 위치를 기준으로 진짜 프로젝트 마스터 루트를 추적합니다.
# cline_tools 내부에 위치할 경우 .parent가 루트가 됩니다.
# ======================================================================
SCRIPT_DIR = Path(__file__).parent.resolve()
if SCRIPT_DIR.name == "cline_tools":
    PROJECT_ROOT = SCRIPT_DIR.parent
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
    """indexer.py의 scan_project()와 동일한 규칙(SCAN_MODE, 제외 폴더, start.py 처리)을 그대로 재현합니다."""
    if SCAN_MODE == "ROOT":
        scan_target = PROJECT_ROOT
        print("🎯 [create_ai_map] Mode: ROOT (프로젝트 전체 경로를 직접 스캔합니다)")
    else:
        scan_target = PROJECT_ROOT / "src"
        print("🎯 [create_ai_map] Mode: SRC (src/ 폴더 내부만 정밀 스캔합니다)")

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
            if file.endswith(".py"):
                target_files.append(Path(root) / file)

    return sorted(target_files)


def load_registry():
    """registered_entities: {"ClassName": "rel/path.py::ClassName"} 포맷을 file -> [class,...] 로 역매핑"""
    path_to_registry = {}
    if REGISTRY_JSON_PATH.exists():
        try:
            with open(REGISTRY_JSON_PATH, "r", encoding="utf-8") as f:
                reg_data = json.load(f).get("registered_entities", {})
            for class_name, loc_str in reg_data.items():
                if "::" in loc_str:
                    file_part, _, _cname = loc_str.rpartition("::")
                    posix_path = Path(file_part).as_posix()
                    path_to_registry.setdefault(posix_path, []).append(class_name)
        except Exception as e:
            print(f"⚠️ 레지스트리 로드 실패: {e}")
    return path_to_registry


def load_protocols():
    """protocols: {"ClassName": {"defined_in": path, "fields": {...}}} 포맷을 file -> [(proto_name, fields), ...] 로 역매핑"""
    path_to_protocol = {}
    if PROTOCOL_JSON_PATH.exists():
        try:
            with open(PROTOCOL_JSON_PATH, "r", encoding="utf-8") as f:
                proto_data = json.load(f).get("protocols", {})
            for proto_name, info in proto_data.items():
                file_rel = info.get("defined_in")
                fields = info.get("fields", {})
                if file_rel:
                    posix_path = Path(file_rel).as_posix()
                    path_to_protocol.setdefault(posix_path, []).append((proto_name, fields))
        except Exception as e:
            print(f"⚠️ 프로토콜 로드 실패: {e}")
    return path_to_protocol


def main():
    target_files = collect_target_files()
    if not target_files:
        return

    print(f"🔍 [디버그] 스캔 타깃 파이썬 파일 수집 완료: 총 {len(target_files)}개 탐색됨")

    path_to_registry = load_registry()
    path_to_protocol = load_protocols()

    # 🚨 system_maps 폴더가 없으면 생성 후, 무조건 그 안에 마스터 장부 재생성 강제
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
            rel_path = file_path.relative_to(PROJECT_ROOT)
            parts = rel_path.parts

            for i in range(1, len(parts)):
                current_dir_path = Path(*parts[:i])
                if current_dir_path not in printed_dirs:
                    dir_indent = "│   " * (i - 1)
                    f.write(f"{dir_indent}├── {parts[i-1]}/\n")
                    printed_dirs.add(current_dir_path)

            indent = "│   " * (len(parts) - 1)
            file_name = parts[-1]
            posix_rel_path = rel_path.as_posix()

            symbols_info = parse_python_file(file_path)
            symbols_str = " | ".join(symbols_info) if symbols_info else ""

            if symbols_str:
                f.write(f"{indent}├── {file_name} [📂 {posix_rel_path}] -> [{symbols_str}]\n")
            else:
                f.write(f"{indent}├── {file_name} [📂 {posix_rel_path}]\n")

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

        f.write("```\n")

    print(f"🎯 [마스터 공장] 'system_maps/AI_CODEBASE_MAP.md'가 {len(target_files)}개의 규격으로 안전하게 자동 갱신되었습니다 형님!")


# ======================================================================
# 🔗 [파이프라인 결합 방어선]
# jjap_watcher.py가 호출하는 함수명을 완벽하게 지원하기 위한 브릿지 래퍼 함수
# ======================================================================
def generate_ai_optimized_map():
    """jjap_watcher.py의 실시간 갱신 요청을 수신하여 내부 메인 공장을 가동합니다."""
    main()


if __name__ == "__main__":
    main()
