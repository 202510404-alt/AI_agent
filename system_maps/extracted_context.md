# ==========================================================================
# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드
# [주의] 코드를 리팩토링/분석/작성할 때 아래 핵심 최적화 규칙을 엄격히 준수하십시오.
#
# 1. 라벨 무시: 코드 행 앞의 '[001]' 등 숫자 마커는 절대 줄번호 사격 좌표입니다.
#              새 코드를 출력할 때는 이 숫자 태그를 완전히 제외하고 순수 코드만 출력하십시오.
# 2. 로그 중심: 설명 주석 작성을 기피하고, 대신 On/Off 가변 스위치가 달린 촘촘한 디버깅 로그를
#              도배 수준으로 짜십시오. 메인 실행 파일 없이 로그 흐름만으로 작동 상태를 유추하게 만듭니다.
# 3. 구조 유지: 프로젝트 내 기존 클래스/함수명 명세 및 self.vars 데이터 프로토콜은 엄격히 준수하십시오.
# 4. 환각 방지: 존재하지 않는 가짜 함수 창조 절대 금지! 절대값 연산은 순정 내장 함수 abs()를 쓰십시오.
# 5. 개발 자유: 위 최소 조건 내에서 알고리즘, 물리 수식, 이동 로직은 자유롭고 창의적으로 짜십시오.
# ==========================================================================
# 📄 [요청 1] TARGET: tools/universal_indexer/create_ai_map.py (10-40라인)
# ----------------------------------------------------------
```python
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
```

# 📄 [요청 1 🔗 제이슨연동 (parse_python_file 호출처 -> python_agent_tools/create_ai_map.py의 [main])] TARGET: python_agent_tools/create_ai_map.py (172-245라인)
# ----------------------------------------------------------
```python

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
            rel_path = file_path.relative_to(PROJECT_ROOT)
            parts = rel_path.parts

            # 디렉터리 트리 라인 출력 생성
            for i in range(1, len(parts)):
                current_dir_path = Path(*parts[:i])
                if current_dir_path not in printed_dirs:
                    dir_indent = "│   " * (i - 1)
                    f.write(f"{dir_indent}├── {parts[i-1]}/\n")
                    printed_dirs.add(current_dir_path)

            indent = "│   " * (len(parts) - 1)
            file_name = parts[-1]
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

        f.write("```\n")

    print(f"🎯 [마스터 공장] 'system_maps/AI_CODEBASE_MAP.md'가 모든 파일 구조를 포함하여 안전하게 자동 갱신되었습니다 형님!")


# ======================================================================
# 🔗 [파이프라인 결합 방어선]
```
