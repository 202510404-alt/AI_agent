from pathlib import Path
from typing import Dict, Any, List

def format_symbol_node(sym: Dict[str, Any], symbol_by_id: Dict[str, Dict], current_posix_path: str, indent: str) -> List[str]:
    """심볼 노드 및 CALLS/USED BY 메타데이터 렌더링 포맷터"""
    lines = []
    sym_type = sym.get("type", "function")
    sym_name = sym.get("name", "")
    full_name = sym.get("full_name", sym_name)
    if not sym_name:
        return lines

    # 1. 인자(Arguments) 복원
    raw_args = sym.get("args")
    if isinstance(raw_args, list):
        args_str = f"({', '.join(raw_args)})" if raw_args else ""
    elif isinstance(raw_args, str) and raw_args:
        args_str = f"({raw_args})"
    else:
        args_str = ""

    # 2. 줄범위 계산
    start_line = sym.get("start_line")
    end_line = sym.get("end_line")
    line_str = f"[L{start_line}-L{end_line}]" if start_line and end_line and start_line != end_line else (f"[L{start_line}]" if start_line else "")

    # 3. 타입별 아이콘 설정
    if sym_type == "class":
        icon_str = f"🧬 class {sym_name}"
    elif sym_type == "json_key":
        icon_str = f"🔑 key \"{sym_name}\""
    else:
        icon_str = f"🎯 def {sym_name}{args_str if args_str else '()'}"

    lines.append(f"{indent}│   ├── {icon_str} {line_str}\n".rstrip() + "\n")

    # 4. CALLS
    calls = sym.get("calls", [])
    if calls:
        lines.append(f"{indent}│   │   ├── 📞 [CALLS]: {', '.join(calls)}\n")

    # 5. USED BY
    used_by_ids = sym.get("used_by", [])
    if used_by_ids:
        used_by_info = []
        for u_id in used_by_ids:
            target = symbol_by_id.get(u_id)
            if target:
                u_file = target.get("file") or target.get("path", "")
                u_name = target.get("name", "")
                used_by_info.append(f"::{u_name}" if u_file == current_posix_path else f"{u_file}::{u_name}")
            else:
                used_by_info.append(str(u_id))
        lines.append(f"{indent}│   │   ├── 🔗 [USED BY]: {', '.join(used_by_info)}\n")

    return lines