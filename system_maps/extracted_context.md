# ==========================================================================# 🎯 AI 전역 가이드라인: 무결성과 확장성의 황금 밸런스 규칙# 소스를 분석, 리팩토링 및 수정 요청할 때 아래 최적화 규칙을 무조건 엄격히 준수하십시오.## 1. 구조 유지: 프로젝트 내 기존 클래스/함수명 명세 및 self.vars 데이터 프로토콜은 엄격히 준수하십시오.# 2. 환각 방지: 존재하지 않는 가짜 함수 창조 절대 금지! 절대값 연산은 순정 내장 함수 abs()를 쓰십시오.# 3. 개발 자유: 위 최소 조건 내에서 알고리즘, 물리 수식, 이동 로직은 자유롭고 창의적으로 짜십시오.# ==========================================================================# 📄 [요청 1] TARGET: tools/python_agent_tools/indexer.py (97-120라인)# ----------------------------------------------------------```python    def index_file(self, file_path: Path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return

        rel_path = file_path.relative_to(self.project_root)
        rel_path_str = rel_path.as_posix()

        file_hash = self._get_sha256(content)
        skeleton = self._extract_skeleton(content)
        self.files_context[rel_path_str] = {
            "hash": file_hash,
            "mtime": int(file_path.stat().st_mtime),
            "skeleton": skeleton
        }

        # 동적 분배기 기동
        self.parse_protocols_and_registries(content, rel_path_str)

        try:
            tree = ast.parse(content)
            for node in tree.body:```# 📄 [요청 1 🔗 제이슨연동 (index_file 호출부 -> python_agent_tools/indexer.py의 [scan_project])] TARGET: python_agent_tools/indexer.py (170-227라인)# ----------------------------------------------------------```python    def scan_project(self):
        if SCAN_MODE == "ROOT":
            scan_target = self.project_root
            print("🎯 [Indexer] Mode: ROOT (프로젝트 원본 경로를 직접 진입하여 경로 에러를 완전 차단합니다)")
        else:
            scan_target = self.project_root / "src"
            print("🎯 [Indexer] Mode: SRC (순정 규격인 src/ 폴더 내부만 정밀 스캔합니다)")

        if not scan_target.exists():
            print(f"⚠️ [Indexer] 스캔 대상 경로가 존재하지 않아 중단합니다: {scan_target}")
            return

        for root, dirs, files in os.walk(scan_target, followlinks=True):
            normalized_root = root.replace("\\", "/")
            
            # 🚨 [여기 주의] 꼬인 중복 경로 예방선 유지
            if "src/project_root/src" in normalized_root:
                continue

            # 🛠️ [형님 수술 구역]: 무시 대상 목록에서 깡통 생성기였던 "src" 강제 추가를 제거합니다.
            # system_memory와 system_maps를 무시하여 인덱서 무한루프는 칼같이 방어합니다.
            excludes = [".venv", ".git", "__pycache__", "system_memory", "system_maps"]

            # 폴더명 단위가 아니라 전체 경로(normalized_root)를 기준으로 영리하게 검문합니다.
            if any(kw in normalized_root for kw in excludes):
                continue

            for file in files:
                # SRC 모드일 때는 최상단 start.py 수집을 패스합니다.
                if file == "start.py" and SCAN_MODE == "SRC":
                    continue
                if file.endswith(".py"):
                    # 🎯 정확하게 개별 파일 징집 입고
                    self.index_file(Path(root) / file)

        for s in self.symbols:
            name_to_check = s["name"]
            for target in self.symbols:
                if name_to_check in target.get("calls", []) and s["symbol_id"] != target["symbol_id"]:
                    s["used_by"].append(target["symbol_id"])
            s["used_by"] = sorted(list(set(s["used_by"])))

        # 🛠️ [격리 개조 포인트 2] 장부 출력 타겟 리다이렉트
        # 혹시 폴더가 없으면 에러가 터지므로 안전하게 자동 생성 로직 투입
        os.makedirs("system_memory", exist_ok=True)

        with open("system_memory/.jjap_context.json", "w", encoding="utf-8") as f:
            json.dump({"files": self.files_context}, f, indent=2, ensure_ascii=False)
        with open("system_memory/.jjap_symbols.json", "w", encoding="utf-8") as f:
            json.dump({"symbols": self.symbols}, f, indent=2, ensure_ascii=False)
        with open("system_memory/definition_map.json", "w", encoding="utf-8") as f:
            json.dump(self.definition_map, f, indent=2, ensure_ascii=False)
        with open("system_memory/data_protocols.json", "w", encoding="utf-8") as f:
            json.dump({"protocols": self.data_protocols}, f, indent=2, ensure_ascii=False)
        with open("system_memory/registry_constants.json", "w", encoding="utf-8") as f:
            json.dump({"registered_entities": self.registry_constants}, f, indent=2, ensure_ascii=False)

        print(f"🧬 [Jjap-Indexer Universal] 5대 장부를 'system_memory/' 구역으로 안전하게 격리 저장 완료!")```