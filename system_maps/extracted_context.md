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
# 📄 [요청 1] TARGET: tools/universal_indexer/indexer.py (115-145라인)
# ----------------------------------------------------------
```python
                    total_ignored_count += 1

        log(f"🏁 스캔 타임라인 종료 -> 분석 통계 [처리 완료: {total_scanned_count}개 | 미지원/패스: {total_ignored_count}개]")

        # 🗂️ 수집 완료 후 디스크 정밀 장부 보관소로 직행 쓰기
        self.save_index_data()

    def index_file(self, file_path: Path, ext: str):
        """개별 파일을 파서를 통해 쪼개어 마스터 장부에 바느질합니다."""
        try:
            rel_path_str = file_path.relative_to(self.project_root).as_posix()
        except ValueError:
            rel_path_str = file_path.resolve().relative_to(self.project_root.resolve()).as_posix()

        log(f"🧵 [장부 바느질 개시] 상대 경로 키: '{rel_path_str}'")
        parser_func = self.parsers[ext]
        
        try:
            log(f"   📡 플러그인 함수 {parser_func.__name__} 원격 연산 제어권 이양 중...")
            res = parser_func(file_path, self.project_root)
            
            if not res or len(res) < 5:
                log(f"   ⚠️ [규격 위반] '{rel_path_str}' 파서의 반환 데이터가 5대 규격을 충족하지 못해 드롭합니다.")
                return

            f_symbols, f_context, f_def_map, f_protocols, f_registry = res

            # 데이터 적재 현황 세부 체크 로그
            log(f"   📥 수집 결과 피드백 받음 -> 심볼: {len(f_symbols)}개, 정의 매핑: {len(f_def_map)}개, 프로토콜: {len(f_protocols)}개, 레지스트리: {len(f_registry)}개")

            # 1. 글로벌 심볼 리스트 누적
```

# 📄 [요청 2] TARGET: tools/universal_indexer/create_ai_map.py (101-135라인)
# ----------------------------------------------------------
```python
def collect_target_files():
    """[수정] .py 제한을 해제하고, 제외 키워드가 없는 프로젝트 내의 '모든 파일'을 수집합니다."""
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
            
            # 💡 [교정] 특정 확장자 차단 해제 -> 모든 파일을 수집 대상으로 포함
            target_files.append(Path(root) / file)

    return sorted(target_files)


def load_registry():
    """
    🔑 [Universal Registry Loader]
```

# 📄 [요청 3] TARGET: tools/universal_indexer/indexer.py (200-202라인)
# ----------------------------------------------------------
```python
if __name__ == "__main__":
    indexer = AdvancedIndexerV2(PROJECT_ROOT)
    indexer.scan_project()
```

# 📄 [요청 4] TARGET: tools/universal_indexer/create_ai_map.py (110-135라인)
# ----------------------------------------------------------
```python
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
            
            # 💡 [교정] 특정 확장자 차단 해제 -> 모든 파일을 수집 대상으로 포함
            target_files.append(Path(root) / file)

    return sorted(target_files)


def load_registry():
    """
    🔑 [Universal Registry Loader]
```
