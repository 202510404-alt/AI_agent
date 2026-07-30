import re
import hashlib
import sys
from pathlib import Path

# ==========================================
# 🚨 [DEBUG CONFIG] 디버깅 로그 ON / OFF 스위치
# ==========================================
DEBUG = False                                      


def debug_log(message: str):
    if DEBUG:
        print(f"[🐛 DEBUG_JS_PARSER] {message}", file=sys.stderr)


def find_end_line_by_braces(lines: list, start_line_idx: int, max_search_range: int = 500) -> int:
    """
    start_line_idx(0-based)부터 연산량을 제한하여 괄호 짝을 추적합니다.
    - max_search_range: 한 함수/클래스당 최대 500줄만 탐색하여 $O(N^2)$ 폭증 방지
    """
    brace_count = 0
    found_first_open = False
    
    # 탐색 한계선 설정 (파일 끝 또는 최대 500줄 아래)
    max_idx = min(len(lines), start_line_idx + max_search_range)

    for i in range(start_line_idx, max_idx):
        line = lines[i]
        
        # 간단한 주석(//) 제거 후 괄호 카운트 (불필요한 과도 탐색 방지)
        clean_line = line.split('//')[0]
        opens = clean_line.count('{')
        closes = clean_line.count('}')

        if opens > 0 and not found_first_open:
            found_first_open = True
            
        if found_first_open:
            brace_count += (opens - closes)
            
            # 괄호 짝이 맞춰진 순간 연산 즉시 종료
            if brace_count <= 0:
                return i + 1

    # 500줄 안에서 못 찾았거나 닫는 괄호가 없을 경우 기본값 안전하게 반환
    return min(len(lines), start_line_idx + 10)


def extract_symbols(file_path: Path, project_root: Path):
    """
    ⚡ [JavaScript / TypeScript Parser v1.5 - High Performance]
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
        # debug_log(f"❌ 파일 읽기 실패: {file_path} - 에러: {e}")
        return symbols, {}, {}, {}, []

    try:
        rel_path_str = file_path.relative_to(project_root).as_posix()
    except ValueError:
        rel_path_str = file_path.resolve().relative_to(project_root.resolve()).as_posix()

    # debug_log(f"📂 [File Start] {rel_path_str}")

    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    lines = content.splitlines()

    # 1. 임포트 모듈 포착
    imports = []
    import_matches = re.findall(r'(?:import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]|require\([\'"]([^\'"]+)[\'"]\))', content)
    for m in import_matches:
        imp = m[0] if m[0] else m[1]
        imports.append(imp)
    
    imports_str = f"💡 📦 imp: {', '.join(sorted(list(set(imports))))}" if imports else ""
    symbols_info_strings = []

    class_pattern = re.compile(r'class\s+([A-Za-z0-9_]+)')
    func_pattern = re.compile(
        r'(?:async\s+)?function\s+([A-Za-z0-9_]+)\s*\((.*?)\)|(?:const|let|var)\s+([A-Za-z0-9_]+)\s*=\s*(?:async\s*)?\((.*?)\)\s*=>'
    )
    object_pattern = re.compile(r'(?:const|let|var)\s+([A-Za-z0-9_]+)\s*=\s*\{([^}]+)\}')

    KEYWORDS = ["entity", "platform", "camera", "sensor", "agent", "navigator", "indexer", "retriever", "handler", "service", "controller"]

    for idx, line in enumerate(lines, start=1):
        line_str = line.strip()

        # [A] 클래스 스캔
        c_match = class_pattern.search(line_str)
        if c_match:
            c_name = c_match.group(1)
            c_id = f"{rel_path_str}::{c_name}"
            
            end_line = find_end_line_by_braces(lines, idx - 1)

            symbols_info_strings.append(f"🧬 class {c_name} [L{idx}~L{end_line}]")
            symbols.append({
                "symbol_id": c_id, "name": c_name, "full_name": c_name, "type": "class",
                "path": rel_path_str, "start_line": idx, "end_line": end_line,
                "calls": [], "used_by": []
            })
            definition_map[c_id] = f"{rel_path_str}:{idx}"

            if any(kw in c_name.lower() for kw in KEYWORDS):
                registry_constants.append(c_name)

        # [B] 함수/메서드 스캔
        f_match = func_pattern.search(line_str)
        if f_match:
            # 💡 [변경 1] f_name: 일반 함수는 group(1), 화살표 함수는 group(3)에 들어옵니다.
            f_name = f_match.group(1) or f_match.group(3)
            
            # 💡 [변경 2] f_args: 일반 함수 인자는 group(2), 화살표 함수 인자는 group(4)에 들어옵니다.
            f_args = f_match.group(2) if f_match.group(1) is not None else f_match.group(4)
            f_args = f_args.strip() if f_args else ""

            if f_name and f_name not in ["require", "import"]:
                f_id = f"{rel_path_str}::{f_name}"
                
                end_line = find_end_line_by_braces(lines, idx - 1)

                # 💡 [변경 3] () 대신 ({f_args})를 매핑하여 실제 파라미터를 출력합니다.
                symbols_info_strings.append(f"🎯 def {f_name}({f_args}) [L{idx}~L{end_line}]")
                symbols.append({
                    "symbol_id": f_id, "name": f_name, "full_name": f_name, "type": "function",
                    "path": rel_path_str, "start_line": idx, "end_line": end_line,
                    "calls": [], "used_by": []
                })
                definition_map[f_id] = f"{rel_path_str}:{idx}"

    # [C] 데이터 프로토콜 스캔
    for obj_match in object_pattern.finditer(content):
        obj_name = obj_match.group(1)
        obj_body = obj_match.group(2)
        
        fields = {}
        kv_pairs = re.findall(r'([A-Za-z0-9_]+)\s*:\s*([^,\n]+)', obj_body)
        for k, v in kv_pairs:
            v_clean = v.strip().strip("'\"")
            fields[k] = f"Any (기본값: {v_clean})"
            
        if fields:
            data_protocols[obj_name] = fields

    summary_parts = [imports_str] if imports_str else []
    summary_parts.extend(symbols_info_strings)
    symbols_summary_str = " | ".join(summary_parts)

    # 🧱 스켈레톤 문맥 정밀 구성
    skeleton_lines = [imports_str] if imports_str else []
    skeleton_lines.extend(symbols_info_strings)
    skeleton_text = "\n".join(skeleton_lines)

    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": symbols_summary_str,
        "skeleton": skeleton_text
    }

    # debug_log(f"✅ [File Scan Complete] {rel_path_str} (추출 심볼: {len(symbols)}개)")
    return symbols, file_context, definition_map, data_protocols, registry_constants