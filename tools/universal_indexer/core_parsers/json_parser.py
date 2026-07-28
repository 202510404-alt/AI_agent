import json
import hashlib
import re
from pathlib import Path

def extract_symbols(file_path: Path, project_root: Path):
    """
    📦 [JSON Core Parser v2.0 - Agent 2-Way Slicing Advanced]
    기존 5대 장부 리턴 구조를 100% 준수하면서,
    하위 AI 에이전트가 단번에 연관 파일(Entrypoint, 설정 파일)로 점프할 수 있도록
    calls 및 used_by 연관 고리를 정밀 추출합니다.
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
    lines = content.splitlines()

    # 1. JSON 유효성 검사
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return symbols, {}, {}, {}, []

    skeleton_lines = ["📦 [JSON STRUCTURE MAP]"]
    symbols_info_strings = []

    # 2. 파일 내부 경로/의존성 감지용 정규식 패턴 (2차 calls 추적용)
    # 예: "./src/index.js", "app.py", "config/setting.json" 등
    path_pattern = re.compile(r'[\'"]([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\'"]')
    detected_file_calls = set()

    # 소스 코드 전체에서 언급되는 상대/절대 파일 경로 징집
    for match in path_pattern.findall(content):
        clean_match = match.strip().replace("\\", "/")
        # 자기 자신 경로 제외 및 의미 있는 파일 확장자 형태 필터링
        if clean_match != rel_path_str and ("/" in clean_match or clean_match.endswith(('.js', '.ts', '.py', '.java', '.json'))):
            detected_file_calls.add(clean_match)

    # 3. 최상위 키 및 심볼 추출
    if isinstance(data, dict):
        for key, value in data.items():
            val_type = type(value).__name__
            
            # 줄 번호 탐지 (해당 key가 위치한 소스 코드 줄 계산)
            start_line = 1
            for idx, line in enumerate(lines, start=1):
                if f'"{key}"' in line or f"'{key}'" in line:
                    start_line = idx
                    break

            # 힌트 및 스켈레톤 조립
            if isinstance(value, list):
                hint = f"List (len: {len(value)})"
            elif isinstance(value, dict):
                hint = f"Dict (keys: {list(value.keys())[:3]}...)"
            else:
                hint = f"{val_type} (val: {str(value)[:30]})"

            skeleton_lines.append(f"  ├── \"{key}\": {hint}")
            symbols_info_strings.append(f"🔑 \"{key}\" [{val_type}]")

            # 🎯 키별 calls 세부 추적 (e.g. main, scripts, extends 등 진입점 연관 파일 바인딩)
            key_calls = []
            val_str = str(value)
            for file_call in detected_file_calls:
                if file_call in val_str:
                    key_calls.append(file_call)

            s_id = f"{rel_path_str}::{key}"
            symbols.append({
                "symbol_id": s_id, 
                "name": key, 
                "full_name": f"{rel_path_str}::{key}", 
                "type": "json_key",
                "file": rel_path_str,
                "path": rel_path_str, 
                "start_line": start_line, 
                "end_line": start_line,
                "calls": key_calls, 
                "used_by": []
            })
            definition_map[key] = f"{rel_path_str}:{start_line}"

    elif isinstance(data, list):
        skeleton_lines.append(f"  └── Root Array: List (len: {len(data)})")
        symbols_info_strings.append(f"📦 Root_Array [len: {len(data)}]")

    skeleton_text = "\n".join(skeleton_lines)

    # 4. 파일 한줄 요약 및 컨텍스트 보관
    summary_parts = [f"💡 📦 json_keys: {len(symbols_info_strings)}개 포착"]
    summary_parts.extend(symbols_info_strings[:5])
    if len(symbols_info_strings) > 5:
        summary_parts.append(f"...외 {len(symbols_info_strings)-5}개")
        
    symbols_summary_str = " | ".join(summary_parts)

    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": symbols_summary_str,
        "skeleton": skeleton_text
    }

    # 5. 설정 파일/스펙 문서 레지스트리 분류
    file_name_lower = file_path.name.lower()
    if "protocol" in file_name_lower or "schema" in file_name_lower:
        if isinstance(data, dict):
            data_protocols[file_path.stem] = {k: type(v).__name__ for k, v in data.items()}
    elif "package" in file_name_lower or "config" in file_name_lower or "constant" in file_name_lower:
        registry_constants.append(f"JSON_CONFIG::{file_path.stem.upper()}")

    return symbols, file_context, definition_map, data_protocols, registry_constants