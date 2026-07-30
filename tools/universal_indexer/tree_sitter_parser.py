import hashlib
from pathlib import Path

try:
    from tree_sitter_languages import get_language, get_parser
    HAS_TREE_SITTER = True
except ImportError:
    HAS_TREE_SITTER = False

LANG_MAP = {
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".py": "python",
    ".go": "go",
    ".rs": "rust",
    ".c": "c",
    ".cpp": "cpp",
    ".java": "java"
}

def extract_symbols(file_path: Path, project_root: Path):
    """
    🌳 [Universal Tree-sitter AST Parser v3.0 - Call & Used_by Graph Engine]
    양방향 호출 관계(calls / used_by)까지 완벽 추출하는 고도화 파서
    """
    symbols = []
    file_context = {}
    definition_map = {}
    data_protocols = {}
    registry_constants = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return symbols, {}, {}, {}, []

    try:
        rel_path_str = file_path.relative_to(project_root).as_posix()
    except ValueError:
        rel_path_str = file_path.resolve().relative_to(project_root.resolve()).as_posix()

    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    ext = file_path.suffix.lower()

    if not HAS_TREE_SITTER or ext not in LANG_MAP:
        file_context[rel_path_str] = {
            "hash": file_hash,
            "symbols_summary": f"📄 Raw File ({ext})",
            "skeleton": content[:300]
        }
        return symbols, file_context, definition_map, data_protocols, registry_constants

    lang_name = LANG_MAP[ext]
    parser = get_parser(lang_name)
    tree = parser.parse(bytes(content, "utf8"))

    symbols_summary_list = []
    KEYWORDS = ["entity", "platform", "camera", "sensor", "agent", "navigator", "indexer", "retriever", "handler", "service", "controller"]

    def traverse(node, current_symbol=None):
        """
        AST 재귀 순회: current_symbol 인자를 전달하여 
        함수 내부에서 발생하는 호출문(call_expression)을 추적합니다.
        """
        node_type = node.type
        active_symbol = current_symbol

        # 1. 클래스 선언 수집
        if node_type in ["class_declaration", "class_definition", "struct_specifier", "interface_declaration"]:
            name_node = node.child_by_field_name("name")
            if name_node:
                c_name = content[name_node.start_byte:name_node.end_byte]
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                c_id = f"{rel_path_str}::{c_name}"
                
                line_range = f"L{start_line}-L{end_line}" if start_line != end_line else f"L{start_line}"
                symbols_summary_list.append(f"🧬 class {c_name} [{line_range}]")
                
                sym_obj = {
                    "symbol_id": c_id, "name": c_name, "full_name": c_name, "type": "class",
                    "file": rel_path_str, "path": rel_path_str, "start_line": start_line, "end_line": end_line,
                    "calls": [], "used_by": []
                }
                definition_map[c_id] = f"{rel_path_str}:{start_line}"
                
                symbols.append(sym_obj)
                definition_map[c_name] = f"{rel_path_str}:{start_line}"
                active_symbol = sym_obj

                if any(kw in c_name.lower() for kw in KEYWORDS):
                    registry_constants.append(c_name)

        # 2. 함수 / 메서드 선언 수집
        elif node_type in ["function_declaration", "function_definition", "method_definition", "arrow_function"]:
            name_node = node.child_by_field_name("name")
            if not name_node and node.parent and node.parent.type == "variable_declarator":
                name_node = node.parent.child_by_field_name("name")

            if name_node:
                f_name = content[name_node.start_byte:name_node.end_byte]
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                f_id = f"{rel_path_str}::{f_name}"
                
                line_range = f"L{start_line}-L{end_line}" if start_line != end_line else f"L{start_line}"
                symbols_summary_list.append(f"🎯 def {f_name}() [{line_range}]")

                sym_obj = {
                    "symbol_id": f_id, "name": f_name, "full_name": f_name, "type": "function",
                    "file": rel_path_str, "path": rel_path_str, "start_line": start_line, "end_line": end_line,
                    "calls": [], "used_by": []
                }
                symbols.append(sym_obj)
                definition_map[f_name] = f"{rel_path_str}:{start_line}"
                active_symbol = sym_obj

        # 3. [핵심 추가] 함수 호출문(call) 추적
        elif node_type in ["call_expression", "function_call"]:
            func_node = node.child_by_field_name("function") or (node.children[0] if node.children else None)
            if func_node:
                called_name = content[func_node.start_byte:func_node.end_byte]
                # 예: console.log -> log / obj.method -> method
                if "." in called_name:
                    called_name = called_name.split(".")[-1]
                
                # 내 안에 다른 함수를 호출하는 코드가 있다면 calls에 등록
                if active_symbol and called_name not in active_symbol["calls"]:
                    active_symbol["calls"].append(called_name)

        # 자식 노드 재귀 탐색 (현재 활성화된 심볼 전달)
        for child in node.children:
            traverse(child, active_symbol)

    traverse(tree.root_node)

    # 4. [핵심 추가] 파일 내부 후처리: calls 관계를 바탕으로 used_by 역방향 주소 바인딩
    sym_lookup = {s["name"]: s for s in symbols}
    for s in symbols:
        for called_fn in s["calls"]:
            if called_fn in sym_lookup:
                target_sym = sym_lookup[called_fn]
                caller_id = s["symbol_id"]
                if caller_id not in target_sym["used_by"]:
                    target_sym["used_by"].append(caller_id)

    # Context 조립
    summary_str = " | ".join(symbols_summary_list) if symbols_summary_list else f"📄 File ({ext})"
    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": summary_str,
        "skeleton": content[:400]
    }

    return symbols, file_context, definition_map, data_protocols, list(set(registry_constants))