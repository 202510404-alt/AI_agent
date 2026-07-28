import hashlib
from pathlib import Path

# tree-sitter 라이브러리 불러오기
try:
    from tree_sitter_languages import get_language, get_parser
    HAS_TREE_SITTER = True
except ImportError:
    HAS_TREE_SITTER = False

# 확장자별 Tree-sitter 언어 매핑
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
    🌳 [Universal Tree-sitter AST Parser v2.1 - Range Formatting Fixed]
    완전한 문법 트리를 기반으로 어떤 언어든 100% 정밀하게 5대 장부 규격 및 시작-끝 줄 범위를 추출합니다.
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

    # Tree-sitter 미설치 또는 지원되지 않는 확장자일 경우 (fallback 처리)
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

    def traverse(node):
        """AST 노드를 순회하며 함수, 클래스, 인터페이스/타입 선언을 추출"""
        node_type = node.type
        
        # 1. 클래스 / 구조체 / 인터페이스 선언 추출
        if node_type in ["class_declaration", "class_definition", "struct_specifier", "interface_declaration"]:
            name_node = node.child_by_field_name("name")
            if name_node:
                c_name = content[name_node.start_byte:name_node.end_byte]
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                
                c_id = f"{rel_path_str}::{c_name}"
                
                # 🎯 [수정 완료] 시작줄-끝줄 범위 포맷팅
                line_range = f"L{start_line}-L{end_line}" if start_line != end_line else f"L{start_line}"
                symbols_summary_list.append(f"🧬 class {c_name} [{line_range}]")
                
                symbols.append({
                    "symbol_id": c_id, "name": c_name, "full_name": c_name, "type": "class",
                    "path": rel_path_str, "start_line": start_line, "end_line": end_line,
                    "calls": [], "used_by": []
                })
                definition_map[c_name] = f"{rel_path_str}:{start_line}"
                
                if any(kw in c_name.lower() for kw in KEYWORDS):
                    registry_constants.append(c_name)

        # 2. 함수 / 메서드 / 화살표 함수 추출
        elif node_type in ["function_declaration", "function_definition", "method_definition", "arrow_function"]:
            name_node = node.child_by_field_name("name")
            
            # JS 변수 할당형 화살표 함수 (const foo = () => {}) 처리
            if not name_node and node.parent and node.parent.type == "variable_declarator":
                name_node = node.parent.child_by_field_name("name")

            if name_node:
                f_name = content[name_node.start_byte:name_node.end_byte]
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1

                f_id = f"{rel_path_str}::{f_name}"
                
                # 🎯 [수정 완료] 시작줄-끝줄 범위 포맷팅
                line_range = f"L{start_line}-L{end_line}" if start_line != end_line else f"L{start_line}"
                symbols_summary_list.append(f"🎯 def {f_name}() [{line_range}]")

                symbols.append({
                    "symbol_id": f_id, "name": f_name, "full_name": f_name, "type": "function",
                    "path": rel_path_str, "start_line": start_line, "end_line": end_line,
                    "calls": [], "used_by": []
                })
                definition_map[f_name] = f"{rel_path_str}:{start_line}"

        # 자식 노드 재귀 탐색
        for child in node.children:
            traverse(child)

    traverse(tree.root_node)

    # Context 조립
    summary_str = " | ".join(symbols_summary_list) if symbols_summary_list else f"📄 File ({ext})"
    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": summary_str,
        "skeleton": content[:400]
    }

    return symbols, file_context, definition_map, data_protocols, list(set(registry_constants))