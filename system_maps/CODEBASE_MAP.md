# 🏗️ 짭커서 프로젝트 CODEBASE MAP

현재 인덱싱된 총 파일 수: **30개**

## 🗂️ [Module Index]
- `.vscode/settings.json`
- `agent_core/__init__.py`
- `agent_core/execution/__init__.py`
- `agent_core/memory/__init__.py`
- `agent_core/plan/__init__.py`
- `agent_core/plan/gemini_client.py`
- `agent_core/plan/planner.py`
- `agent_core/plan/prompt_builder.py`
- `agent_core/plan/schemas.py`
- `agent_core/validation/__init__.py`
- `src/src/main/java/com/desertcore/DesertCore.java`
- `src/src/main/java/com/desertcore/deathevent.java`
- `src/src/main/java/com/desertcore/lobbycmd.java`
- `src/src/main/java/com/desertcore/marendumbul.java`
- `src/src/main/java/com/desertcore/samakportal.java`
- `tools/universal_indexer/agent_navigator.py`
- `tools/universal_indexer/context_builder.py`
- `tools/universal_indexer/core_parsers/__init__.py`
- `tools/universal_indexer/core_parsers/cs_parser.py`
- `tools/universal_indexer/core_parsers/java_parser.py`
- `tools/universal_indexer/core_parsers/js_parser.py`
- `tools/universal_indexer/core_parsers/json_parser.py`
- `tools/universal_indexer/core_parsers/py_parser.py`
- `tools/universal_indexer/create_ai_map.py`
- `tools/universal_indexer/indexer.py`
- `tools/universal_indexer/jjap_lookup.py`
- `tools/universal_indexer/jjap_retriever.py`
- `tools/universal_indexer/jjap_watcher.py`
- `tools/universal_indexer/switch.py`
- `tools/universal_indexer/update_map.py`

## 💀 [Skeleton & Dependency 명세서]
### 📄 .vscode/settings.json
#### 🧱 Code Skeleton:
```python
📦 [JSON STRUCTURE MAP]
  ├── "terminal.integrated.sendKeybindingsToShell": bool (val: True)
  ├── "accessibility.verbosity.terminal": bool (val: False)
  ├── "git.autofetch": bool (val: True)
  ├── "explorer.confirmDelete": bool (val: False)
  ├── "git.openRepositoryInParentFolders": str (val: always)
  ├── "terminal.integrated.enableMultiLinePasteWarning": str (val: never)
  ├── "workbench.editor.empty.hint": str (val: hidden)
  ├── "maven.terminal.useJavaHome": bool (val: True)
  ├── "git.confirmSync": bool (val: False)
  ├── "explorer.confirmDragAndDrop": bool (val: False)
  ├── "java.configuration.runtimes": List (len: 1)
  ├── "java.jdt.ls.java.home": str (val: C:/Program Files/Ecl)
  ├── "roo-cline.debug": bool (val: True)
  ├── "roo-cline.allowedCommands": List (len: 0)
  ├── "roo-cline.deniedCommands": List (len: 0)
  ├── "files.exclude": Dict (keys: ['**/__pycache__']...)
  ├── "python.createEnvironment.trigger": str (val: external)
```

--------------------------------------------------

### 📄 agent_core/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/execution/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/memory/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/plan/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/plan/gemini_client.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/plan/planner.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/plan/prompt_builder.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/plan/schemas.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 agent_core/validation/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 src/src/main/java/com/desertcore/DesertCore.java
#### 🧱 Code Skeleton:
```python
public void onEnable() { // L8-14
getServer().getPluginManager().registerEvents(new marendumbul(), this); // L9-17
getLogger().info("desertcore 플러그인이 성공적으로 켜졌습니다!"); // L10-17
getServer().getPluginManager().registerEvents(new samakportal(), this); // L11-17
getServer().getPluginManager().registerEvents(new deathevent(), this); // L12-17
getCommand("로비").setExecutor(new lobbycmd()); // L13-17
public void onDisable() { // L17-18
```

--------------------------------------------------

### 📄 src/src/main/java/com/desertcore/deathevent.java
#### 🧱 Code Skeleton:
```python
class deathevent { // L32-223
    public void onPlayerDeath(PlayerDeathEvent event) { // L38-51
    public void onPlayerRespawn(PlayerRespawnEvent event) { // L54-73
    cancelTimer(player.getUniqueId()); // L66-76
    public void onPlayerMove(PlayerMoveEvent event) { // L76-123
    public void run() { // L91-114
    cancelTimer(uuid); // L93-96
    cancelTimer(uuid); // L98-102
    cancelTimer(uuid); // L106-119
    private void cancelTimer(UUID uuid) { // L125-130
    public void onPlayerJoin(PlayerJoinEvent event) { // L133-148
    cancelTimer(player.getUniqueId()); // L139-146
    unloadAndDeleteInstance(previousWorldName); // L145-151
    public void onPlayerCommand(PlayerCommandPreprocessEvent event) { // L151-178
    cancelTimer(player.getUniqueId()); // L161-170
    unloadAndDeleteInstance(currentWorldName); // L169-172
    cancelTimer(player.getUniqueId()); // L175-181
    private void unloadAndDeleteInstance(String instanceName) { // L181-205
    deleteDirectoryNative(instanceDir.toPath()); // L196-197
    private void deleteDirectoryNative(Path path) throws IOException { // L208-222
    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException { // L211-214
    public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException { // L217-220
```

--------------------------------------------------

### 📄 src/src/main/java/com/desertcore/lobbycmd.java
#### 🧱 Code Skeleton:
```python
class lobbycmd { // L15-49
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String label, @NotNull String[] args) { // L18-48
```

--------------------------------------------------

### 📄 src/src/main/java/com/desertcore/marendumbul.java
#### 🧱 Code Skeleton:
```python
class marendumbul { // L13-62
    public void onPlayerJoin(PlayerJoinEvent event) { // L19-61
```

--------------------------------------------------

### 📄 src/src/main/java/com/desertcore/samakportal.java
#### 🧱 Code Skeleton:
```python
class samakportal { // L22-133
    public void onVillagerClick(PlayerInteractEntityEvent event) { // L25-95
    deleteDirectoryNative(instanceDir.toPath()); // L61-69
    copyDirectoryNative(templateDir.toPath(), instanceDir.toPath()); // L65-74
    private void copyDirectoryNative(Path source, Path target) throws IOException { // L98-115
    public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException { // L101-107
    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException { // L110-113
    private void deleteDirectoryNative(Path path) throws IOException { // L118-132
    public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException { // L121-124
    public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException { // L127-130
```

--------------------------------------------------

### 📄 tools/universal_indexer/agent_navigator.py
#### 🧱 Code Skeleton:
```python
class SemanticNavigator:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        # 🧠 [불러오기 교정] 묶어낸 격리 폴더(system_memory) 안의 .jjap_symbols.json 정보를 정확하게 가져옵니다.
        self.symbols_path = root_dir / "system_memory" / ".jjap_symbols.json"
        self.symbols_data = self._load_database()

    def _load_database(self):
        if not self.symbols_path.exists():
            return {"symbols": []}
        try:
            with open(self.symbols_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"symbols": []}

    # [📂 실제경로] tools/python_agent_tools/agent_navigator.py
# [📂 실제경로] tools/python_agent_tools/agent_navigator.py

    def extract_multi_slices(self, raw_prompt: str):
        """
        [Multi-Target Protocol Parser - 경로 및 클래스명 종속성 완전 격파 버전]
        1. 입력 프롬프트에서 '파일경로:시작줄-끝줄'을 정규식으로 사냥합니다.
        2. [형님의 2차 탐색 기전] 1단계로 슬라이싱된 텍스트 본체에서 def/class 명칭을 직접 추출합니다.
        3. .jjap_symbols.json 장부와 대조 시, 'tools/' 경로 프리픽스 불일치 및 used_by 내부의 
           'AdvancedIndexerV2.scan_project' vs 'scan_project' 같은 클래스명 유무 오차를 유연하게 필터링하여 2차 기습 징집합니다.
        """
        
        print("\n" + "="*60)
        print("🚨 [DEBUGGER ON] 내비게이터 멀티 슬라이싱 파이프라인 기동!!!")
        print(f"📥 유저 입력 프롬프트: {repr(raw_prompt)}")
        print("="*60)

        pattern = r"([a-zA-Z0-9_\-\./]+)\s*:\s*(\d+)(?:\s*-\s*(\d+))?"
        matches = re.findall(pattern, raw_prompt)

        print(f"🔍 정규식 1차 타겟 스캔 결과: {matches}")
        if not matches:
            print("⚠️ [DEBUG] 매칭되는 파일 경로 및 라인 규격이 없습니다. 빈 배열 리턴.")
            return []

        extracted_slices = []
        req_num = 1

        for match in matches:
            file_rel_path = match[0].strip()
            start_line = int(match[1])
            end_line = int(match[2]) if match[2] else start_line

            print(f"\n🎯 [요청 #{req_num}] 메인 타겟 분석 시작 -> {file_rel_path} ({start_line} ~ {end_line} 라인)")

            # [1단계] 메인 타겟 파일 슬라이싱 추출
            target_file_path = self.root_dir / file_rel_path
            print(f"   📂 검증할 하드디스크 물리 경로: {target_file_path}")
            
            if not target_file_path.exists():
                print(f"   ❌ [ERROR] 해당 파일이 실제 경로에 존재하지 않습니다! 패스합니다.")
                continue

            try:
                with open(target_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                total_lines = len(lines)
                safe_start = max(1, min(start_line, total_lines))
                safe_end = max(safe_start, min(end_line, total_lines))
                print(f"   📏 파일 전체 줄 수: {total_lines} | 보정된 안전 범위: {safe_start} ~ {safe_end}")

                slice_lines = lines[safe_start - 1 : safe_end]
                slice_code = "".join(slice_lines)
                print(f"   🟢 1차 메인 슬라이싱 성공 (길이: {len(slice_code)}자)")

                # 메인 슬라이스 보따리 안착
                extracted_slices.append({
                    "req_num": f"{req_num}",
                    "file": file_rel_path,
                    "line_range": f"{safe_start}-{safe_end}",
                    "code": slice_code
                })

                # [2단계] 🔗 플러스 알파 (+α) - 제이슨 기반 2차 심볼 탐색기 가동
                print(f"   📡 [형님의 2차 사냥기] 잘려 나온 텍스트 내부에서 양방향 심볼 식별 개시...")

                # [방향 1] 역방향 추적용: 내가 정의한 심볼 (나를 부른 함수를 찾기 위함)
                defined_names = re.findall(r"(?:def|class)\s+([a-zA-Z0-9_]+)", slice_code)

                # [방향 2] 정방향 추적용: 본문에서 내가 호출해서 쓰고 있는 함수/메서드 추출 (내가 불러온 함수)
                called_names = re.findall(r"(?:[a-zA-Z0-9_]+\.)?([a-zA-Z0-9_]+)\s*\(", slice_code)

                # 내장 키워드(print, len, open 등)는 노이즈이므로 필터링할 목록 정의
                builtin_filters = {"print", "len", "range", "open", "dict", "list", "set", "any", "all", "max", "min", "append", "get", "strip", "split", "exists", "readlines", "join"}
                filtered_called_names = [name for name in called_names if name not in builtin_filters]

                # 두 목록을 합쳐서 중복 제거 후 하나의 타겟 리스트로 병합!
                target_symbols = list(set(defined_names + filtered_called_names))
                print(f"   📦 [양방향 통합] 징집 대상 심볼 목록: {target_symbols}")
                
                # 장부 메모리 상태 실시간 체크
                symbols_list = self.symbols_data.get("symbols", [])
                print(f"   📚 로드된 JSON 장부 총 심볼 개수: {len(symbols_list)}개")

                # 🔄 [교정 완료] 정의된 심볼만 돌던 루프를 양방향 통합 리스트(target_symbols)로 전면 전환!
                for target_name in target_symbols:
                    print(f"      🔎 [전역 심볼 대조] 이름: '{target_name}' -> 장부 전체 스캔 중...")
                    match_found = False
                    
                    for s in symbols_list:
                        json_file_path = s.get("file", "")
                        
                        # 장부에 등록된 심볼명과 일치하면 무조건 대조 진입 (경로 제한 철폐)
                        if s.get("name") == target_name:
                            match_found = True
                            
                            t_file = s.get("file", "")
                            s_start = s.get("start_line", 1)
                            s_end = s.get("end_line", 1)

                            # ➡️ [정방향 사냥] 내가 불러와서 실행 중인 외부 함수의 본체 소스코드 기습 징집
                            if t_file != file_rel_path:
                                print(f"         ➡️ [정방향] 내가 불러온 함수 본체 포착 -> {t_file} ({s_start}~{s_end}라인)")
                                callee_file_path = self.root_dir / t_file
                                if not callee_file_path.exists():
                                    callee_file_path = self.root_dir / "tools" / t_file
                                    
                                if callee_file_path.exists():
                                    with open(callee_file_path, "r", encoding="utf-8") as cf:
                                        cf_lines = cf.readlines()
                                    
                                    s_start = max(1, min(s_start, len(cf_lines)))
                                    s_end = max(s_start, min(s_end, len(cf_lines)))
                                    callee_code = "".join(cf_lines[s_start - 1 : s_end])
                                    
                                    if not any(x["file"] == t_file and x["line_range"] == f"{s_start}-{s_end}" for x in extracted_slices):
                                        extracted_slices.append({
                                            "req_num": f"{req_num} ➡️ 불러온함수 ({target_name} 본체)",
                                            "file": t_file,
                                            "line_range": f"{s_start}-{s_end}",
                                            "code": callee_code
                                        })

                            # ⬅️ [역방향 사냥] 나를 부르는 상위 호출처(used_by) 추적
                            # 단, 내가 직접 정의한 함수(defined_names) 목록에 속할 때만 상위 역추적 가동
                            if (target_name in defined_names) or (s.get("file") == file_rel_path):
                                ub_list = s.get("used_by", [])
                                if ub_list:
                                    print(f"         ⬅️ [역방향] 나를 부르는 전역 호출처 목록(used_by): {ub_list}")
                                    for ub_id in ub_list:
                                        if "::" in ub_id:
                                            ub_file, ub_symbol_name = ub_id.split("::", 1)
                                            if "." in ub_symbol_name:
                                                ub_symbol_name = ub_symbol_name.split(".")[-1]
                                            
                                            sub_match_found = False
                                            for target_s in symbols_list:
                                                sub_t_file = target_s.get("file", "")
                                                s_id = target_s.get("symbol_id", "")
                                                sub_s_name = target_s.get("name", "")
                                                
                                                if (s_id == ub_id) or (ub_id.endswith(s_id)) or (sub_s_name == ub_symbol_name and (sub_t_file == ub_file or ub_file.endswith(sub_t_file) or sub_t_file.endswith(ub_file))):
                                                    sub_match_found = True
                                                    ub_file_path = self.root_dir / file_rel_path.replace(json_file_path, sub_t_file)
                                                    if not ub_file_path.exists():
                                                        ub_file_path = self.root_dir / sub_t_file
                                                        if not ub_file_path.exists():
                                                            ub_file_path = self.root_dir / "tools" / sub_t_file
                                                    
                                                    if ub_file_path.exists():
                                                        with open(ub_file_path, "r", encoding="utf-8") as ubf:
                                                            ub_lines = ubf.readlines()
                                                        
                                                        ubs_start = max(1, min(target_s.get("start_line", 1), len(ub_lines)))
                                                        ubs_end = max(ubs_start, min(target_s.get("end_line", len(ub_lines)), len(ub_lines)))
                                                        ub_slice_code = "".join(ub_lines[ubs_start - 1 : ubs_end])
                                                        
                                                        if not any(x["file"] == sub_t_file and x["line_range"] == f"{ubs_start}-{ubs_end}" for x in extracted_slices):
                                                            extracted_slices.append({
                                                                "req_num": f"{req_num} 🔗 제이슨연동 ({target_name} 호출처 -> {sub_t_file}의 [{sub_s_name}])",
                                                                "file": sub_t_file,
                                                                "line_range": f"{ubs_start}-{ubs_end}",
                                                                "code": ub_slice_code
                                                            })
                                            if not sub_match_found:
                                                print(f"            ❌ [ERROR] 호출처 구조체 '{ub_id}'를 장부에서 찾지 못했습니다.")
                    
                    if not match_found:
                        print(f"      ❓ [NOT FOUND] 코드엔 찍혀있는데 JSON 장부({file_rel_path})엔 등록 안 된 심볼입니다.")

            except Exception as e:
                import traceback
                print(f"💥 [CRITICAL ERROR] 슬라이싱 중 예외 폭발!!!: {e}")
                traceback.print_exc()

            req_num += 1

        print("\n" + "="*60)
        print(f"🏁 [DEBUG] 최종 반환할 총 슬라이스 묶음 개수: {len(extracted_slices)}개")
        print("="*60 + "\n")
        return extracted_slices

class JjapCursorNavigatorGUI:
    def __init__(self, root, project_root: Path):
        self.root = root
        self.project_root = project_root
        self.navigator = SemanticNavigator(project_root)
        self.last_markdown_content = "" # 외부 파일 저장용 임시 보관소

        self.root.title("⚡ Jjap-Cursor Agent Navigator v2.0 (Auto-Exporter)")
        self.root.geometry("1000x750")

        # 메인 레이아웃 분할
        self.main_container = ttk.Frame(root, padding="10")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # 1. 상단 프롬프트 입력창 구역
        input_label = ttk.Label(self.main_container, text="📥 [에이전트 요청 프롬프트 입력 구역]", font=("Malgun Gothic", 11, "bold"))
        input_label.pack(anchor=tk.W, pady=(0, 5))

        self.prompt_input = tk.Text(self.main_container, height=6, font=("Malgun Gothic", 10))
        self.prompt_input.pack(fill=tk.X, pady=(0, 10))
        self.prompt_input.insert(tk.END, "💡 실전 테스트 양식 예시:\nsrc/player/player_main.py:45-75")

        # 2. 중간 제어 버튼 라인
        self.btn_frame = ttk.Frame(self.main_container)
        self.btn_frame.pack(fill=tk.X, pady=(0, 10))

        self.scan_button = ttk.Button(
            self.btn_frame, 
            text="⚡ 소스코드 정밀 슬라이싱 및 컨텍스트 바인딩 가동 ⚡", 
            command=self.execute_slicing_pipeline
        )
        self.scan_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.export_button = ttk.Button(
            self.btn_frame,
            text="💾 마크다운 파일(.md) 개별 내보내기",
            command=self.manual_export_file,
            state=tk.DISABLED # 처음엔 비활성화
        )
        self.export_button.pack(side=tk.RIGHT, padx=(5, 0))

        # 3. 하단 결과창 구역
        output_label = ttk.Label(self.main_container, text="📄 [AI 배송용 최적화 켄텍스트 보따리 (출력 결과)]", font=("Malgun Gothic", 11, "bold"))
        output_label.pack(anchor=tk.W, pady=(0, 5))

        self.code_display = tk.Text(self.main_container, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        self.code_display.pack(fill=tk.BOTH, expand=True)

        # 4. 최하단 상태 바
        self.status_label = ttk.Label(self.main_container, text="🟢 대기 중... 에이전트 프롬프트를 넣고 가동 버튼을 눌러주십시오.", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=(10, 0))

    def execute_slicing_pipeline(self):
        raw_prompt = self.prompt_input.get("1.0", tk.END).strip()
        if not raw_prompt or raw_prompt.startswith("💡"):
            messagebox.showwarning("입력 오류", "형님, 슬라이싱할 대상 파일 경로와 라인을 입력해 주십시오!")
            return

        # 백그라운드 추출 엔진 구동
        extracted_slices = self.navigator.extract_multi_slices(raw_prompt)

        if not extracted_slices:
            self.status_label.config(text="❌ 추출 실패: 프롬프트에서 타겟 패턴('경로:줄번호')을 인식하지 못했습니다.")
            messagebox.showerror("추출 실패", "지정된 경로 문자열 형식을 확인해 주십시오.")
            return

        # 화면 정화 및 마스터 전역 가이드라인 헤더 선언
        self.code_display.delete("1.0", tk.END)
        
        # 마크다운 스트링 빌드 시작 (기존 규칙 유지 + 형님의 토큰 다이어트/디버그 로그 지침 추가)
        md_lines = []
        md_lines.append("# ==========================================================================")
        md_lines.append("# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드")
        md_lines.append("# [주의] 코드를 리팩토링/분석/작성할 때 아래 핵심 최적화 규칙을 엄격히 준수하십시오.")
        md_lines.append("#")
        md_lines.append("# 1. 라벨 무시: 코드 행 앞의 '[001]' 등 숫자 마커는 절대 줄번호 사격 좌표입니다.")
        md_lines.append("#              새 코드를 출력할 때는 이 숫자 태그를 완전히 제외하고 순수 코드만 출력하십시오.")
        md_lines.append("# 2. 로그 중심: 설명 주석 작성을 기피하고, 대신 On/Off 가변 스위치가 달린 촘촘한 디버깅 로그를")
        md_lines.append("#              도배 수준으로 짜십시오. 메인 실행 파일 없이 로그 흐름만으로 작동 상태를 유추하게 만듭니다.")
        md_lines.append("# 3. 구조 유지: 프로젝트 내 기존 클래스/함수명 명세 및 self.vars 데이터 프로토콜은 엄격히 준수하십시오.")
        md_lines.append("# 4. 환각 방지: 존재하지 않는 가짜 함수 창조 절대 금지! 절대값 연산은 순정 내장 함수 abs()를 쓰십시오.")
        md_lines.append("# 5. 개발 자유: 위 최소 조건 내에서 알고리즘, 물리 수식, 이동 로직은 자유롭고 창의적으로 짜십시오.")
        md_lines.append("# ==========================================================================")

        for slc in extracted_slices:
            # 💡 조인할 때 줄바꿈 규칙을 유지하기 위해 \n 처리 추가
            md_lines.append(f"# 📄 [요청 {slc['req_num']}] TARGET: {slc['file']} ({slc['line_range']}라인)")
            md_lines.append("# ----------------------------------------------------------")
            md_lines.append("```python")
            md_lines.append(slc["code"].rstrip())
            md_lines.append("```\n")

        self.last_markdown_content = "\n".join(md_lines)

        # GUI 창에 렌더링 인쇄
        self.code_display.insert(tk.END, self.last_markdown_content)
        
        # 💾 [내보내기 교정] 프로젝트 루트가 아닌 묶어낸 격리 폴더(system_maps/) 내부로 자동 상시 저장 처리!
        auto_save_path = self.project_root / "system_maps" / "extracted_context.md"
        try:
            with open(auto_save_path, "w", encoding="utf-8") as f:
                f.write(self.last_markdown_content)
            status_msg = f"🟢 추출 및 마크다운 자동 저장 완료! -> system_maps/{auto_save_path.name}"
            self.export_button.config(state=tk.NORMAL)
        except Exception as e:
            status_msg = f"⚠️ 화면 추출 완료했으나 자동 파일 저장 실패: {e}"

        self.status_label.config(text=status_msg)
        
    def manual_export_file(self):
        """사용자가 원하는 다른 경로에 수동으로 저장할 수 있는 다이얼로그 프로토콜"""
        if not self.last_markdown_content:
            return
        
        file_path = filedialog.asksaveasfilename(
            initialdir=str(self.project_root),
            title="마크다운 컨텍스트 파일 저장",
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.last_markdown_content)
                messagebox.showinfo("내보내기 성공", f"형님, 성공적으로 파일을 내보냈습니다!\n📂 경로: {file_path}")
            except Exception as e:
                messagebox.showerror("내보내기 실패", f"파일 저장 중 에러가 발생했습니다: {e}")
```

--------------------------------------------------

### 📄 tools/universal_indexer/context_builder.py
#### 🧱 Code Skeleton:
```python
class ContextBuilder:
    """날것의 소스코드를 정화하여 AI가 가장 좋아하는 영양가 있는 형태로 가공하는 비서 클래스입니다."""

    def __init__(self, project_root: str) -> None:
        """비서관을 초기화하며 기준이 되는 프로젝트 루트 경로를 지정합니다."""
        self.project_root = Path(project_root)

    def read_and_clean_file(self, relative_path: str) -> str:
        """파일을 읽어서 사람용 주석(# INFO:) 내용은 완전히 비우되,
        줄바꿈과 콤팩트한 줄 번호 태그만 강제로 남겨서 토큰을 최소화하고
        AI와 인간의 라인 인덱스를 100% 동기화하는 개조 함수입니다.
        """
        file_path = self.project_root / relative_path
        
        if not file_path.exists():
            raise FileNotFoundError(f"요청하신 경로에 파일이 존재하지 않습니다: {relative_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        cleaned_lines = []
        in_multiline_comment = False

        # enumerate를 사용해 파일 원본의 물리적인 줄 번호(1부터 시작)를 정확히 추적합니다.
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            # 1. 다중행 주석(""") 처리 블록
            if stripped.startswith('"""') or stripped.endswith('"""'):
                if '"""' in stripped and len(stripped) > 3:
                    pass 
                else:
                    in_multiline_comment = not in_multiline_comment
                    # 토큰 최소화: 라벨과 원본 줄바꿈만 남김
                    cleaned_lines.append(f"[{idx:03d}]\n")
                    continue

            if in_multiline_comment:
                # 다중행 주석 내부도 토큰 절약을 위해 내용을 비우고 줄만 유지
                cleaned_lines.append(f"[{idx:03d}]\n")
                continue

            # ⭐ 형님의 핵심 지시사항: 주석 부분은 내용을 비운 채 억지로 줄 표시를 유지!
            # 2. # INFO: 로 시작하는 주석행 처리
            if stripped.startswith("# INFO:"):
                # 💡 핵심: 긴 주석 텍스트를 다 날려버리고 오직 줄 번호 태그와 개행만 주입 (토큰 최소화!)
                cleaned_lines.append(f"[{idx:03d}]\n")
                continue

            # 3. 코드 옆에 붙은 꼬리표 주석 예외 처리 (`x = 1  # INFO: ...`)
            if " # INFO:" in line:
                # 주석 내용만 잘라내고, 코드 앞단에 줄 번호를 붙여서 재조립
                pure_code = line.split(" # INFO:")[0]
                cleaned_lines.append(f"[{idx:03d}]{pure_code}\n")
                continue

            # 4. 일반 빈 줄 처리
            if not stripped:
                cleaned_lines.append(f"[{idx:03d}]\n")
                continue

            # 5. 그 외의 순수 실행 코드 및 보존 주석 (# HISTORY:, # FIX:)
            # AI가 토큰을 해석할 때 밀리지 않도록 고정형 태그를 맨 앞에 강제 주입합니다.
            cleaned_lines.append(f"[{idx:03d}]{line}")

        return "".join(cleaned_lines)

    def assemble_ai_prompt(self, user_query: str, affected_files: list[str]) -> str:
        """검열된 파일 소스코드들과 형님의 최종 질문을 엮어서 저(Gemini)에게 배송할 최종 프롬프트 보따리를 조립합니다.
        
        🛠️ 내가 내부에서 부려먹는 함수:
          - `self.read_and_clean_file()`: 각 파일들을 돌면서 `# INFO:` 주석을 청소하라고 지시함.
        """
        prompt_parts = []
        prompt_parts.append(f"=== USER REQUEST ===\n{user_query}\n\n")
        prompt_parts.append("=== CLEANED CONTEXT CODEBASE ===\n")
        prompt_parts.append("아래 소스코드들은 토큰 절약을 위해 불필요한 설명 주석(# INFO:)이 제거되고, ")
        prompt_parts.append("과거 오류 수정 내역(# HISTORY:)만 온전히 보존된 청정 코드입니다.\n\n")

        for rel_path in affected_files:
            # 🛡️ [격리 방어선] 장부 보관소(system_memory) 및 마스터 지도(system_maps) 내부 파일은 컨텍스트 수집 대상에서 완전 무시
            if "system_memory" in str(rel_path) or "system_maps" in str(rel_path):
                continue

            prompt_parts.append(f"--- FILE: {rel_path} ---")
            try:
                # 위에 만들어 둔 청소 함수를 실행시켜 알짜배기 코드만 받아옵니다.
                purified_code = self.read_and_clean_file(rel_path)
                prompt_parts.append(purified_code)
            except Exception as e:
                prompt_parts.append(f"파일을 읽는 중 오류 발생: {str(e)}")
            prompt_parts.append("\n")

        # 최종적으로 저(Gemini)의 뇌세포로 들어올 텍스트 보따리가 완성되는 순간입니다.
        return "\n".join(prompt_parts)
```

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/__init__.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/cs_parser.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/java_parser.py
#### 🧱 Code Skeleton:
```python
def log(message: str):
    if DEBUG_LOG:
        print(f"📡 [Java-Parser Log] {message}")

def _find_matching_curly_brace(lines: list, start_line_idx: int) -> int:
    """
    자바의 중괄호 { } 쌍을 정밀 추적하여 메서드/클래스의 실제 종료 줄 번호(1-based)를 반환합니다.
    """
    brace_count = 0
    opened = False
    
    for idx in range(start_line_idx, len(lines)):
        line = lines[idx]
        # 주석 제거 후 블록 검사
        cleaned_line = re.sub(r'//.*|/\*.*?\*/', '', line)
        
        for char in cleaned_line:
            if char == '{':
                brace_count += 1
                opened = True
            elif char == '}':
                brace_count -= 1
                
        if opened and brace_count <= 0:
            return idx + 1  # 1-based line number
            
    return start_line_idx + 1

def extract_symbols(file_path: Path, project_root: Path):
    """
    ☕ [Java Core Advanced Parser v2.0]
    파이썬과 100% 동일한 5대 장부 규격을 만족하도록 자바 소스를 정밀 해부합니다.
    - 중첩 경로(src/src) 방어선 구축 완료
    - imp: 임포트 패키지 완벽 추출
    - calls: 메서드 내부 호출 분석 엔진 탑재
    - 줄 범위 (시작줄-끝줄) 매칭 완벽 지원
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
        log(f"❌ 파일 읽기 실패: {file_path} | 에러: {e}")
        return symbols, {}, {}, {}, []

# 🚨 [교정] 독단적인 src/src/ 축약을 제거하고 실제 디스크 상대 경로 규격을 그대로 보존합니다.
    try:
        raw_rel = file_path.relative_to(project_root).as_posix()
    except ValueError:
        raw_rel = file_path.name

    # 별도의 치환 없이 디스크 실제 경로를 단일 진실 공급원(Single Source of Truth) 키값으로 확정
    rel_path_str = raw_rel

    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    lines = content.splitlines()

    # 1. 🧲 임포트(Imports) 및 패키지 징집
    imports = []
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith("import ") and line_strip.endswith(";"):
            imp_target = line_strip.replace("import ", "").replace(";", "").strip()
            imports.append(imp_target)
            
    imports_str = f"💡 📦 imp: {', '.join(sorted(list(set(imports))))}" if imports else ""

    # 2. 🩻 클래스 및 메서드 심볼 다차원 스캔
    symbols_info_strings = []
    skeleton_segments = []
    
    current_class = None
    class_start_idx = -1

    # 자바 클래스/인터페이스/메서드 탐색 정규식
    class_patt = re.compile(r'(?:public|protected|private|static|\s)+\s+(?:class|interface|enum)\s+([a-zA-Z0-9_]+)')
    method_patt = re.compile(r'(?:public|protected|private|static|\s)+\s+[\w<>\s?\[\]]+\s+([a-zA-Z0-9_]+)\s*\([^)]*\)\s*(?:throws\s+[\w\s,]+)?\s*\{?')

    for idx, line in enumerate(lines):
        line_num = idx + 1
        line_stripped = line.strip()
        
        # 주석이나 공백 라인은 스킵
        if line_stripped.startswith("//") or line_stripped.startswith("*") or not line_stripped:
            continue

        # A. 클래스 탐지
        class_match = class_patt.search(line)
        if class_match:
            c_name = class_match.group(1)
            current_class = c_name
            class_start_idx = idx
            end_line = _find_matching_curly_brace(lines, idx)
            
            symbols_info_strings.append(f"🧬 class {c_name} [L{line_num}-{end_line}]")
            skeleton_segments.append(f"class {c_name} {{ // L{line_num}-{end_line}")
            
            symbols.append({
                "symbol_id": f"{rel_path_str}::{c_name}",
                "name": c_name, "full_name": c_name, "type": "class",
                "path": rel_path_str, "start_line": line_num, "end_line": end_line,
                "calls": [], "used_by": []
            })
            definition_map[c_name] = f"{rel_path_str}:{line_num}"
            continue

# B. 메서드 탐지 및 인자(파라미터) 정밀 추출로 변경
        method_match = method_patt.search(line)
        if method_match and ("(" in line_stripped and "import " not in line_stripped):
            m_name = method_match.group(1)
            
            if m_name in ["if", "for", "while", "switch", "catch", "return"]:
                continue
                
            # 💡 [추가] 메서드 선언 전체 라인에서 괄호 ( ) 내부의 인자 정보만 파싱
            param_match = re.search(r'\((.*?)\)', line_stripped)
            params_str = ""
            if param_match:
                # 예: "String player, int score" -> "String, int" 형태로 타입만 콤팩트하게 정렬
                raw_params = param_match.group(1).strip()
                if raw_params:
                    # 공백 기준으로 나눠서 변수명은 버리고 타입명만 수집
                    param_types = [p.strip().split()[0] for p in raw_params.split(",") if p.strip()]
                    params_str = ", ".join(param_types)

            end_line = _find_matching_curly_brace(lines, idx)
            
            
            # 메서드 바디 본문 추출 (내부 호출 함수 파싱용)
            body_lines = lines[idx:end_line]
            body_text = "\n".join(body_lines)
            
            # 내부 호출 추적 (간이 자바 식별자 파서: 다른 함수명 호출부 스캔)
            possible_calls = re.findall(r'([a-zA-Z0-9_]+)\s*\(', body_text)
            detected_calls = [
                name for name in possible_calls 
                if name not in ["if", "for", "while", "switch", "catch", "synchronized", "super", "this", m_name]
            ]
            detected_calls = list(set(detected_calls))

            # =================================================================
            # 🎯 [수정 완료] 파이썬 규격과 완벽 동기화하여 줄 범위 [L시작-끝] 복원
            # =================================================================
            if current_class:
                m_id = f"{rel_path_str}::{current_class}.{m_name}"
                full_name = f"{current_class}.{m_name}"
                # ✅ [교정] 클래스 내부의 메서드 정보와 줄 범위를 정확하게 매핑합니다.
                symbols_info_strings.append(f"🎯 def {m_name}({params_str}) [L{line_num}-{end_line}]")
                skeleton_segments.append(f"    {line_stripped} // L{line_num}-{end_line}")
                def_key = full_name
            else:
                m_id = f"{rel_path_str}::{m_name}"
                full_name = m_name
                # ✅ [교정] 단독 메서드 정보와 줄 범위를 정확하게 매핑합니다.
                symbols_info_strings.append(f"🎯 def {m_name}({params_str}) [L{line_num}-{end_line}]")
                skeleton_segments.append(f"{line_stripped} // L{line_num}-{end_line}")
                def_key = m_name

            symbols.append({
                "symbol_id": m_id, "name": m_name, "full_name": full_name, "type": "method",
                "path": rel_path_str, "start_line": line_num, "end_line": end_line,
                "calls": detected_calls, "used_by": []
            })
            definition_map[def_key] = f"{rel_path_str}:{line_num}"

    # 3. 🧱 소스 스켈레톤 마감 처리
    skeleton_text = "\n".join(skeleton_segments)

    # 4. 🎚️ 파이썬 마스터 규격 한줄 요약 문자열 조립 완료
    summary_parts = [imports_str] if imports_str else []
    summary_parts.extend(symbols_info_strings)
    symbols_summary_str = " | ".join(summary_parts)

    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": symbols_summary_str,
        "skeleton": skeleton_text
    }

    log(f"✅ 자바 소스 스캔 완료 -> 경로: {rel_path_str} | 심볼: {len(symbols)}개 포착")
    return symbols, file_context, definition_map, data_protocols, registry_constants
```

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/js_parser.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/json_parser.py
#### 🧱 Code Skeleton:
```python
def extract_symbols(file_path: Path, project_root: Path):
    """
    📦 [JSON Core Parser v1.0]
    새로운 자동화 임포터 인터페이스 계약(5대 장부 리턴 구조)을 100% 준수합니다.
    JSON 파일 내부의 주요 루트 키(Root Keys) 및 스키마 구조를 탐지하여 스켈레톤과 심볼로 등록합니다.
    """
    # 🤝 새로운 사령탑이 한 번에 흡수할 5대 데이터 규격 초기화
    symbols = []
    file_context = {}
    definition_map = {}
    data_protocols = {}
    registry_constants = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        # 파일 읽기 실패 시 안전 패스 프로토콜
        return symbols, {}, {}, {}, []

    rel_path_str = file_path.relative_to(project_root).as_posix()
    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    # 1. JSON 문법 유효성 검사 및 파싱
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # 깨진 JSON 파일 방어선
        return symbols, {}, {}, {}, []

    # 2. 🧱 스켈레톤(뼈대) 및 요약 텍스트 생성
    # AI 비서들이 JSON의 전체 덩어리를 다 먹어서 컨텍스트가 터지는 것을 막기 위해,
    # 최상위 키 레이아웃과 데이터 타입만 예쁘게 요약 요리합니다.
    skeleton_lines = ["📦 [JSON STRUCTURE MAP]"]
    symbols_info_strings = []

    if isinstance(data, dict):
        for key, value in data.items():
            val_type = type(value).__name__
            # 요소 개수나 문자열 길이 힌트 제공
            if isinstance(value, list):
                hint = f"List (len: {len(value)})"
            elif isinstance(value, dict):
                hint = f"Dict (keys: {list(value.keys())[:3]}...)"
            else:
                hint = f"{val_type} (val: {str(value)[:20]})"

            skeleton_lines.append(f"  ├── \"{key}\": {hint}")
            
            # 심볼 장부 등록용 문자열 적립
            symbols_info_strings.append(f"🔑 \"{key}\" [{val_type}]")
            
            # 5대 장부 중 1번 'symbols'에 개별 키를 심볼 ID로 정밀 바느질
            s_id = f"{rel_path_str}::{key}"
            symbols.append({
                "symbol_id": s_id, "name": key, "full_name": f"json.{key}", "type": "json_key",
                "path": rel_path_str, "start_line": 1, "end_line": 1,
                "calls": [], "used_by": []
            })
            # 정의 맵 매핑 등록
            definition_map[key] = f"{rel_path_str}:1"

    elif isinstance(data, list):
        skeleton_lines.append(f"  └── Root Array: List (len: {len(data)})")
        symbols_info_strings.append(f"📦 Root_Array [len: {len(data)}]")

    skeleton_text = "\n".join(skeleton_lines)

    # 3. 파일 한줄 요약 및 컨텍스트 바느질
    summary_parts = [f"💡 📦 json_keys: {len(symbols_info_strings)}개 포착"]
    summary_parts.extend(symbols_info_strings[:5]) # 너무 길어지면 끊기 (가독성 유지)
    if len(symbols_info_strings) > 5:
        summary_parts.append(f"...외 {len(symbols_info_strings)-5}개")
        
    symbols_summary_str = " | ".join(summary_parts)

    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": symbols_summary_str,
        "skeleton": skeleton_text
    }

    # 4. JSON 파일의 특정 네이밍이 들어올 때 데이터 프로토콜이나 레지스트리로 귀속해주는 유연성 필터
    file_name_lower = file_path.name.lower()
    if "protocol" in file_name_lower or "schema" in file_name_lower:
        # JSON 구조 자체를 데이터 프로토콜 레이아웃으로 복사 탑재
        if isinstance(data, dict):
            data_protocols[file_path.stem] = {k: type(v).__name__ for k, v in data.items()}
    elif "constant" in file_name_lower or "registry" in file_name_lower:
        registry_constants.append(f"JSON_CONFIG::{file_path.stem.upper()}")

    # 🤝 최종 5대 규격 튜플 리턴
    return symbols, file_context, definition_map, data_protocols, registry_constants
```

--------------------------------------------------

### 📄 tools/universal_indexer/core_parsers/py_parser.py
#### 🧱 Code Skeleton:
```python
def extract_symbols(file_path: Path, project_root: Path):
    """
    🐍 [Python Core Parser v1.0]
    기존 indexer.py 내부의 순정 파이썬 AST 스캔, 스켈레톤 추출, 레지스트리/프로토콜 징집 로직을
    단 하나의 약속된 마스터 함수 구조로 완벽 격리 이사 완료했습니다 형님!
    
    리턴값: (symbols_list, file_context_dict, definition_map_dict, data_protocols_dict, registry_constants_dict)
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
        # 파일 읽기 실패 시 빈 규격 레이아웃으로 안전 패스
        return symbols, {}, {}, {}, []

    rel_path_str = file_path.relative_to(project_root).as_posix()
    file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    try:
        root = ast.parse(content)
    except SyntaxError:
        # 문법 에러 파일 방어선
        return symbols, {}, {}, {}, []

    # 1. 🧱 스켈레톤(뼈대) 소스 정밀 요약
    lines = content.splitlines()
    skeleton_lines = []
    for node in root.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            start_idx = node.lineno - 1
            end_idx = min(node.end_lineno, len(lines)) if getattr(node, "end_lineno", None) else start_idx + 1
            skeleton_lines.extend(lines[start_idx:end_idx])
            skeleton_lines.append("")
    skeleton_text = "\n".join(skeleton_lines)

    # 2. 🧬 내부 상호 호출 관계 자백용 1차 지도 빌드
    func_lines = {}
    for node in ast.walk(root):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_lines[node.name] = (node.lineno, node.end_lineno)
        elif isinstance(node, ast.ClassDef):
            func_lines[node.name] = (node.lineno, node.end_lineno)

    # 3. 🔑 레지스트리 & 프로토콜 징집 레이더 가동
    for node in root.body:
        if isinstance(node, ast.ClassDef):
            has_vars = False
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name) and (target.id == "vars" or "variables" in target.id.lower()):
                            has_vars = True
            
            if has_vars:
                # 데이터 프로토콜 장부 등록
                fields = {}
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name) and target.id != "vars":
                                if isinstance(item.value, ast.Constant):
                                    fields[target.id] = f"{type(item.value.value).__name__} (기본값: {item.value.value})"
                                else:
                                    fields[target.id] = "Any"
                data_protocols[node.name] = fields
            else:
                # 일반 핵심 클래스는 레지스트리 상수로 귀속
                KEYWORDS = ["entity", "platform", "camera", "sensor", "agent", "navigator", "indexer", "retriever", "handler"]
                if any(kw in node.name.lower() for kw in KEYWORDS):
                    registry_constants.append(node.name)

    # 4. 🎯 클래스/메서드/함수 트리 구조 정밀 추적 및 심볼 바느질
    symbols_info_strings = []
    
    # 탑레벨 함수/클래스 1차 등록
    for node in root.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            s_name = node.name
            s_id = f"{rel_path_str}::{s_name}"
            symbols_info_strings.append(f"🎯 def {s_name}() [L{node.lineno}-{node.end_lineno}]")
            
            calls = []
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                    if child.func.id in func_lines and child.func.id != s_name:
                        calls.append(child.func.id)
            
            symbols.append({
                "symbol_id": s_id, "name": s_name, "full_name": s_name, "type": "function",
                "path": rel_path_str, "start_line": node.lineno, "end_line": node.end_lineno,
                "calls": list(set(calls)), "used_by": []
            })
            definition_map[s_name] = f"{rel_path_str}:{node.lineno}"

        elif isinstance(node, ast.ClassDef):
            c_name = node.name
            c_id = f"{rel_path_str}::{c_name}"
            symbols_info_strings.append(f"🧬 class {c_name} [L{node.lineno}-{node.end_lineno}]")
            
            symbols.append({
                "symbol_id": c_id, "name": c_name, "full_name": c_name, "type": "class",
                "path": rel_path_str, "start_line": node.lineno, "end_line": node.end_lineno,
                "calls": [], "used_by": []
            })
            definition_map[c_name] = f"{rel_path_str}:{node.lineno}"

            # 클래스 내부 메서드 슬라이싱
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    m_name = sub.name
                    m_id = f"{rel_path_str}::{c_name}.{m_name}"
                    symbols_info_strings.append(f"    └─ def {m_name}() [L{sub.lineno}-{sub.end_lineno}]")
                    
                    sub_calls = []
                    for child in ast.walk(sub):
                        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                            if child.func.id in func_lines and child.func.id != m_name:
                                sub_calls.append(child.func.id)
                    
                    symbols.append({
                        "symbol_id": m_id, "name": m_name, "full_name": f"{c_name}.{m_name}", "type": "method",
                        "path": rel_path_str, "start_line": sub.lineno, "end_line": sub.end_lineno,
                        "calls": list(set(sub_calls)), "used_by": []
                    })
                    definition_map[f"{c_name}.{m_name}"] = f"{rel_path_str}:{sub.lineno}"

    # 임포트 내역 파싱
    imports = []
    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    imports_str = f"💡 📦 imp: {', '.join(sorted(list(set(imports))))}" if imports else ""

    # 최종 한줄 요약 문자열 조립
    summary_parts = [imports_str] if imports_str else []
    summary_parts.extend(symbols_info_strings)
    symbols_summary_str = " | ".join(summary_parts)

    file_context[rel_path_str] = {
        "hash": file_hash,
        "symbols_summary": symbols_summary_str,
        "skeleton": skeleton_text
    }

    return symbols, file_context, definition_map, data_protocols, registry_constants
```

--------------------------------------------------

### 📄 tools/universal_indexer/create_ai_map.py
#### 🧱 Code Skeleton:
```python
def load_jjap_context():
    """
    Indexer가 모든 언어(Python, Java, JSON)를 스캔해서 만들어둔 
    통합 .jjap_context.json 장부를 읽어옵니다. (단일 진실 공급원)
    """
    context_path = PROJECT_ROOT / "system_memory" / ".jjap_context.json"
    if not context_path.exists():
        # 만약 해당 위치에 없으면 프로젝트 루트 폴더도 확인 (폴백 방어선)
        context_path = PROJECT_ROOT / ".jjap_context.json"
        
    if context_path.exists():
        try:
            with open(context_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("files", {})
        except Exception as e:
            print(f"⚠️ [.jjap_context.json] 로드 중 오류 발생: {e}")
    else:
        print("⚠️ [.jjap_context.json] 통합 장부 파일을 찾을 수 없습니다. 인덱서를 먼저 실행해 주세요.")
    return {}

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
    통합 심볼 장부를 기반으로 어떤 파일에 어떤 클래스(Registry, Protocol)가 
    정의되어 있는지 역추적하여 최종 매칭 테이블을 완성합니다 형님!
    """
    path_to_registry = {}
    path_to_protocol = {}

    # 1. 원본 장부 로드 (레지스트리 상수 및 프로토콜 명세 리스트)
    registry_data = load_registry()      # 기존의 load_registry 활용
    protocol_data = load_protocols()    # 기존의 load_protocols 활용

    # 2. 글로벌 심볼 장부(.jjap_symbols.json)에서 class 타입 추출
    symbols_path = PROJECT_ROOT / "system_memory" / ".jjap_symbols.json"
    if not symbols_path.exists():
        symbols_path = PROJECT_ROOT / ".jjap_symbols.json"

    all_symbols = []
    if symbols_path.exists():
        try:
            with open(symbols_path, "r", encoding="utf-8") as f:
                all_symbols = json.load(f).get("symbols", [])
        except Exception as e:
            print(f"⚠️ [.jjap_symbols.json] 읽기 실패: {e}")

    # 3. 심볼 장부를 순회하며 클래스 단위로 레지스트리/프로토콜 싱크 매칭
    for sym in all_symbols:
        if sym.get("type") != "class":
            continue
            
        cls_name = sym.get("name")
        rel_path = sym.get("path") # 예: "src/src/main/java/com/desertcore/lobbycmd.java"
        
        if not cls_name or not rel_path:
            continue

        # Posix 표준 경로 문자열로 정규화
        posix_rel_path = Path(rel_path).as_posix()

        # [A] 레지스트리 매칭 검사
        if cls_name in registry_data:
            if posix_rel_path not in path_to_registry:
                path_to_registry[posix_rel_path] = set()
            path_to_registry[posix_rel_path].add(cls_name)

        # [B] 프로토콜 명세 매칭 검사
        if cls_name in protocol_data:
            if posix_rel_path not in path_to_protocol:
                path_to_protocol[posix_rel_path] = []
            # 중복 추가 방어
            if (cls_name, protocol_data[cls_name]) not in path_to_protocol[posix_rel_path]:
                path_to_protocol[posix_rel_path].append((cls_name, protocol_data[cls_name]))

    return path_to_registry, path_to_protocol

def main():
    target_files = collect_target_files()
    
    # 1. 🛠️ [통합 개조] 인덱서가 작성한 모든 언어의 통합 컨텍스트 장부 미리 로드
    jjap_context = load_jjap_context()

    # 2. 🛠️ [통합 개조] 리팩터링된 글로벌 심볼 기반 레지스트리/프로토콜 역추적 매칭 데이터 획득
    path_to_registry, path_to_protocol = parse_protocols_and_registries()

    # 출력 타깃 폴더(system_maps/) 자동 확보 안전망
    OUTPUT_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as f:
        # 🎯 [메모리 오염 방어] 바깥에 있던 printed_dirs를 이 안쪽으로 이사시켰습니다 형님!
        # 파일이 새로 열려 쓰여질 때마다 기존 장부를 깨끗하게 초기화하여 모드 전환 시 뒤엉킴을 막습니다.
        printed_dirs = set()

        # 마스터 헤더 사양 작성 (순정 코드 100% 유지)
        f.write("# 🏗️ AI-OPTIMIZED ULTRA COMPACT CODEBASE MAP (INTELLIGENT SCAN)\n\n")
        f.write("> **[AI 프로토콜 매뉴얼]** 이 문서는 다른 AI 비서들의 경로 오해를 차단하기 위해 파일마다 **실제 하드디스크 상대 경로 `[📂 실제경로]`**를 강제 명시해 둔 특수 지도입니다.\n")
        f.write("> AI 비서는 절대 눈치로 경로를 추측하지 말고, 파일명 뒤에 박혀있는 `[📂 실제경로]` 규격을 그대로 복사하여 agent_navigator를 호출하십시오.\n\n")
        f.write("```markdown\nproject_root/\n")
        
        # 파일 스캔 및 맵 생성 순회 루프
        for file_path in target_files:
            rel_path = file_path.relative_to(PROJECT_ROOT)
            posix_rel_path = rel_path.as_posix()
            file_name = file_path.name

            # 🎯 [형님 제안 반영] SRC 모드일 때만 가장 바깥의 'src/' 문자열 제거 (출력용 display_path 생성)
            if SCAN_MODE == "SRC" and posix_rel_path.startswith("src/"):
                display_path = posix_rel_path[4:]  # "src/" 4글자 컷
            else:
                display_path = posix_rel_path

            # 🌲 트리 계층 디렉토리 라인 생성 및 중복 출력 방지 (display_path 기준 트리 생성)
            parts = Path(display_path).parts
            for i in range(len(parts) - 1):
                current_dir_path = Path(*parts[:i + 1]).as_posix()
                if current_dir_path not in printed_dirs:
                    printed_dirs.add(current_dir_path)
                    indent = "│   " * i
                    f.write(f"{indent}├── {parts[i]}/\n")

            indent = "│   " * (len(parts) - 1)

            # 🛠️ [기존 순정 장부 조회 유지] 데이터 대조용 장부 조회는 원래 수집 경로(posix_rel_path)로 수행하여 누락 방지
            file_meta = jjap_context.get(posix_rel_path, {})
            symbols_info = file_meta.get("symbols_summary", "")

            # 🛠️ [경로 유틸 불일치 폴백 방어선] (순정 유지)
            if not symbols_info and posix_rel_path.startswith("src/src/"):
                shorter_path = posix_rel_path.replace("src/src/", "src/", 1)
                symbols_info = jjap_context.get(shorter_path, {}).get("symbols_summary", "")

            # 코드맵에 최종 파일 사양 한 줄 출력 (출력값만 display_path 적용)
            if symbols_info:
                f.write(f"{indent}├── {file_name} [📂 {display_path}] -> [{symbols_info}]\n")
            else:
                f.write(f"{indent}├── {file_name} [📂 {display_path}]\n")

            # 🔑 하위 레지스트리 매칭 블록 출력 (순정 원래 키값 유지)
            if posix_rel_path in path_to_registry:
                for reg_const in path_to_registry[posix_rel_path]:
                    f.write(f"{indent}│     ├── 🔑 [REGISTRY]: \"{reg_const}\"\n")

            # 📊 하위 프로토콜 청크 매칭 블록 출력 (순정 원래 키값 유지)
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
    
    # 하단 디버그 로그 및 요약 보고서 파일 쓰기 (순정 유지)
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

def generate_ai_optimized_map():
    """jjap_watcher.py의 실시간 갱신 요청을 수신하여 내부 메인 공장을 가동합니다."""
    main()
```

--------------------------------------------------

### 📄 tools/universal_indexer/indexer.py
#### 🧱 Code Skeleton:
```python
def log(message: str):
    if DEBUG_LOG:
        print(f"📡 [Indexer-Core Log] {message}")

class AdvancedIndexerV2:
    """
    [Jjap-Cursor Core Indexer V3.6 - Ultra Universal Engine]
    동적 플러그인 로딩 및 5대 장부 동기화의 모든 파이프라인에 디버깅 레이더를 도배했습니다.
    """
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.parsers: Dict[str, Any] = {}
        self.symbols: List[Dict[str, Any]] = []
        self.files_context: Dict[str, Any] = {}
        self.definition_map: Dict[str, str] = {}
        self.data_protocols: Dict[str, Any] = {}
        self.registry_constants: List[str] = []
        
        log(f"🏗️ 인덱서 코어 초기화 완료 (마스터 루트 주소: {self.project_root})")
        self._auto_load_parsers()

    def _auto_load_parsers(self):
        """core_parsers 폴더 내부의 파서들을 동적 로드하여 확장자별로 바인딩합니다."""
        parsers_dir = SCRIPT_DIR / "core_parsers"
        log(f"🔌 동적 파서 폴더 탐색 시작 -> 경로: {parsers_dir}")
        
        if not parsers_dir.exists():
            log(f"⚠️ [경고] core_parsers 폴더가 물리적으로 존재하지 않습니다: {parsers_dir}")
            return

        file_list = os.listdir(parsers_dir)
        log(f"📂 폴더 내부 파일 목록 검색 완료 (총 {len(file_list)}개 탐지됨)")

        for file in file_list:
            if file.endswith("_parser.py"):
                ext = f".{file.split('_parser.py')[0]}"
                full_path = parsers_dir / file
                log(f"   ⚙️ 파서 후보 발견: '{file}' -> 매핑 타깃 확장자: '{ext}'")
                
                try:
                    spec = importlib.util.spec_from_file_location(f"parser_{ext}", full_path)
                    if spec and spec.loader:
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                        if hasattr(mod, "extract_symbols"):
                            self.parsers[ext] = mod.extract_symbols
                            log(f"   └── 🟢 [바인딩 성공] 확장자 [{ext}] 엔진 탑재 완료!")
                        else:
                            log(f"   └── ❌ [인터페이스 불일치] '{file}' 내부에 'extract_symbols' 함수가 없습니다.")
                except Exception as ex:
                    log(f"   └── 💥 [런타임 컴파일 에러] 파서 플러그인 로딩 실패: {file} | 사유: {ex}")

        log(f"📊 파서 동적 마운트 최종 정산: 총 {len(self.parsers)}개의 다국어 컴포넌트 활성화.")

    def scan_project(self):
        """설정된 SCAN_MODE에 따라 프로젝트 내의 모든 등록된 언어 파일을 스캔합니다."""
        scan_target = self.project_root if SCAN_MODE == "ROOT" else self.project_root / "src"
        log(f"🚀 [디버깅 레이더 가동] 모드: {SCAN_MODE} | 물리 스캔 범위: {scan_target}")

        EXCLUDE_KEYWORDS = [".venv", ".git", "__pycache__", "system_memory", "system_maps"]
        log(f"🛡️ 고유 스캔 제외 키워드 목록: {EXCLUDE_KEYWORDS}")
        
        if not scan_target.exists():
            log(f"❌ [치명적 오류] 지정된 스캔 타깃 경로가 디스크에 존재하지 않습니다: {scan_target}")
            return

        total_scanned_count = 0
        total_ignored_count = 0

        for root, dirs, files in os.walk(scan_target, followlinks=True):
            normalized_root = root.replace("\\", "/")
            
            # 제외 폴더 조건 검사 및 로깅
            if any(kw in normalized_root for kw in EXCLUDE_KEYWORDS):
                log(f"🚫 [패스] 제외 필터 경로 스킵: {normalized_root}")
                continue

            for file in files:
                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                # 동적으로 로드된 파서 대상 확장자 범위에 포함되는지 확인
                if ext in self.parsers:
                    log(f"🔍 [타깃 포착] 파일 발견: {file_path.name} (확장자: {ext})")
                    self.index_file(file_path, ext)
                    total_scanned_count += 1
                else:
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
            self.symbols.extend(f_symbols)
            
            # 2. 파일 요약 정보 컨텍스트 병합
            self.files_context.update(f_context)
            
            # 3. 정의 맵 및 레지스트리 병합
            self.definition_map.update(f_def_map)
            self.data_protocols.update(f_protocols)
            
            for item in f_registry:
                if item not in self.registry_constants:
                    self.registry_constants.append(item)

            log(f"   📈 [바느질 완료] 마스터 메모리 장부 적재 성공: '{rel_path_str}'")
        except Exception as e:
            log(f"   💥 [인덱싱 내부 크래시] 파일 처리 중 예외 발생: {rel_path_str} | 에러 내용: {e}")

    def save_index_data(self):
        """메모리에 적재된 5대 장부를 디스크에 격리 저장합니다."""
        TARGET_MEMORY_DIR = self.project_root / "system_memory"
        log(f"💾 [디스크 동기화] system_memory 보관소 직인 쓰기 시작 -> 폴더 위치: {TARGET_MEMORY_DIR}")
        
        try:
            os.makedirs(TARGET_MEMORY_DIR, exist_ok=True)

            ctx_path = TARGET_MEMORY_DIR / ".jjap_context.json"
            with open(ctx_path, "w", encoding="utf-8") as f:
                json.dump({"files": self.files_context}, f, indent=2, ensure_ascii=False)
            log(f"   ├── 📄 [.jjap_context.json] 저장 완료 (총 {len(self.files_context)}개 파일 컨텍스트)")

            sym_path = TARGET_MEMORY_DIR / ".jjap_symbols.json"
            with open(sym_path, "w", encoding="utf-8") as f:
                json.dump({"symbols": self.symbols}, f, indent=2, ensure_ascii=False)
            log(f"   ├── 📄 [.jjap_symbols.json] 저장 완료 (총 {len(self.symbols)}개 글로벌 심볼)")

            def_path = TARGET_MEMORY_DIR / "definition_map.json"
            with open(def_path, "w", encoding="utf-8") as f:
                json.dump(self.definition_map, f, indent=2, ensure_ascii=False)
            log(f"   ├── 📄 [definition_map.json] 저장 완료 (총 {len(self.definition_map)}개 빠른 추적 정의 노드)")

            proto_path = TARGET_MEMORY_DIR / "data_protocols.json"
            with open(proto_path, "w", encoding="utf-8") as f:
                json.dump({"protocols": self.data_protocols}, f, indent=2, ensure_ascii=False)
            log(f"   ├── 📄 [data_protocols.json] 저장 완료 (총 {len(self.data_protocols)}개 명세 프로토콜)")

            reg_path = TARGET_MEMORY_DIR / "registry_constants.json"
            with open(reg_path, "w", encoding="utf-8") as f:
                json.dump({"registered_entities": self.registry_constants}, f, indent=2, ensure_ascii=False)
            log(f"   └── 📄 [registry_constants.json] 저장 완료 (총 {len(self.registry_constants)}개 엔티티 레지스트리)")

            print(f"🧬 [Jjap-Indexer Universal] 5대 장부 전체 동기화 성공! 보관된 총 파일 수: {len(self.files_context)}개")
        except Exception as write_err:
            log(f"💥 [디스크 파일 쓰기 치명적 실패] 장부 동동화 중 에러 발생: {write_err}")
```

--------------------------------------------------

### 📄 tools/universal_indexer/jjap_lookup.py
#### 🧱 Code Skeleton:
```python
def load_json(file_path: Path):
    if not file_path.exists():
        print(f"❌ Error: {file_path} not found. Please run the indexer first.")
        sys.exit(1)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def lookup_symbol(symbol_name: str):
    """특정 함수나 클래스의 시그니처와 사용처를 검색합니다."""
    data = load_json(SYMBOLS_FILE)
    symbols = data.get("symbols", [])
    
    # 부분 일치 검색 (대소문자 무시)
    results = [s for s in symbols if symbol_name.lower() in s.get("name", "").lower()]
    
    if not results:
        print(f"⚠️ 심볼 '{symbol_name}'을(를) 찾을 수 없습니다.")
        return

    print(f"🔍 '{symbol_name}' 검색 결과 ({len(results)}건 찾음):\n")
    for s in results:
        print(f"[{s.get('type', 'symbol').upper()}] {s.get('full_name', s.get('name'))}")
        print(f"  - File: {s.get('file')} (Lines: {s.get('start_line')}-{s.get('end_line')})")
        print(f"  - Signature: {s.get('name')}{s.get('signature', '()')}")
        
        used_by = s.get("used_by", [])
        if used_by:
            print(f"  - Used By: {len(used_by)} places")
            for u in used_by[:5]: # 최대 5개까지만 출력 (토큰 절약)
                print(f"    * {u}")
            if len(used_by) > 5:
                print(f"    * ... and {len(used_by) - 5} more")
        else:
            print("  - Used By: None (Not used anywhere or it's a top-level entry)")
        print("-" * 40)

def show_skeleton(file_path: str):
    """특정 파일의 뼈대(Skeleton)를 보여줍니다."""
    data = load_json(CONTEXT_FILE)
    files = data.get("files", {})
    
    # 경로 매칭 (부분 일치)
    matched_keys = [k for k in files.keys() if file_path in k]
    
    if not matched_keys:
        print(f"⚠️ 파일 경로에 '{file_path}'이(가) 포함된 파일을 찾을 수 없습니다.")
        return
        
    for key in matched_keys:
        skeleton = files[key].get("skeleton", "No skeleton available.")
        print(f"📄 [FILE SKELETON] {key}")
        print(skeleton)
        print("=" * 40)
```

--------------------------------------------------

### 📄 tools/universal_indexer/jjap_retriever.py
#### 🧱 Code Skeleton:
```python
class JjapRetriever:
    """
    Roo Code를 위한 Context Surgeon V2.
    1. Exact Match 우선 탐색 (Disambiguation 해결)
    2. 라인 단위 Truncation (코드 파손 방지)
    3. 엄격한 스키마 계약 (Indexer V2 전제)
    """
    def __init__(self, project_root: Path):
        self.project_root = project_root
        # 🧠 [불러오기 교정] 격리 폴더(system_memory) 안으로 이사 간 인덱싱 장부를 정확하게 바라보도록 관로를 꺾어줍니다.
        self.symbols_file = self.project_root / "system_memory" / ".jjap_symbols.json"
        self.max_context_lines = 300
        self.symbols_db = self._load_symbols()

    def _load_symbols(self) -> List[Dict[str, Any]]:
        if self.symbols_file.exists():
            try:
                with open(self.symbols_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    symbols = data.get("symbols", [])
                    if DEBUG_MODE:
                        print(f"📦 [Retriever 디버그] 인덱싱 장부 로드 완료! (총 {len(symbols)}개 심볼 탑재됨)")
                    return symbols
            except Exception as e:
                print(f"⚠️ [Retriever 에러] 스키마 로드 실패: {e}")
        else:
            if DEBUG_MODE:
                print(f"⚠️ [Retriever 디버그] 장부 파일이 없습니다: {self.symbols_file}")
        return []

    def retrieve_symbol(self, query: str) -> str:
        """심볼 검색 및 정밀 문맥 조립"""
        if DEBUG_MODE:
            print(f"📡 [Retriever 디버그] 수술 쿼리 수신: '{query}'")

        # [지피티 지적 1 해결] 심볼 식별 최적화 (Exact -> Partial -> Fallback)
        target = self._find_best_match(query)
        
        if not target:
            if DEBUG_MODE:
                print(f"❌ [Retriever 디버그] 매칭 실패 -> 장부에서 '{query}'를 찾지 못함")
            return f"❌ '{query}'와 일치하는 심볼을 찾을 수 없습니다. (ID 또는 Name을 확인하세요)"

        file_rel_path = target.get('file')
        file_path = self.project_root / file_rel_path
        
        if DEBUG_MODE:
            print(f"🎯 [Retriever 디버그] 타깃 징집 성공! 심볼ID: {target['symbol_id']} ➡️ 타깃 파일: {file_rel_path}")

        if not file_path.exists():
            return f"❌ 파일을 찾을 수 없습니다: {file_rel_path}"

        with open(file_path, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()

        # [Surgery 시작]
        context = []
        context.append(f"### [RETRIEVED CONTEXT: {target['symbol_id']}] ###")
        
        # 1. Imports (상단 50줄)
        context.append("\n# --- Imports ---")
        imports = [line.strip() for line in all_lines[:50] if line.strip().startswith(('import ', 'from '))]
        context.extend(imports)
        context.append("    ...")
        if DEBUG_MODE:
            print(f"🧹 [Retriever 디버그] 상단 공통 Import {len(imports)}줄 추출 완료")

        # 2. Parent Context (Class Header)
        if target.get('parent'):
            parent = next((s for s in self.symbols_db if s['name'] == target['parent'] and s['file'] == target['file']), None)
            if parent:
                p_start = parent['range'][0]
                context.append(f"\n# --- Class: {target['parent']} ---")
                context.append(all_lines[p_start-1].rstrip())
                context.append("    \"\"\" (Internal methods hidden) \"\"\"")
                if DEBUG_MODE:
                    print(f"🧱 [Retriever 디버그] 부모 클래스 뼈대 '{target['parent']}' 바느질 바인딩")

        # 3. Target Snippet (Range 준수)
        start, end = target['range']
        context.append(f"\n# --- Target: {target['name']} (Lines {start}-{end}) ---")
        
        # 인덱스 범위 안전하게 가져오기
        snippet = all_lines[max(0, start-1) : min(len(all_lines), end)]
        context.extend([line.rstrip() for line in snippet])
        if DEBUG_MODE:
            print(f"✂️ [Retriever 디버그] 정밀 문맥 수술실(Surgeon) 작동 완료 ({start}~{end} 라인 발췌)")

        # [지피티 지적 2 해결] 라인 단위 안전 절삭
        return self._safe_truncate("\n".join(context))

    def _find_best_match(self, query: str) -> Optional[Dict]:
        """심볼 중복 문제를 해결하기 위한 매칭 로직"""
        # 1. symbol_id 완전 일치 (가장 정확)
        for s in self.symbols_db:
            if s.get('symbol_id') == query: 
                if DEBUG_MODE: print(f"🔍 [Retriever 디버그] 1순위 완전 매칭성공 (Symbol ID): {query}")
                return s
        # 2. name 완전 일치
        for s in self.symbols_db:
            if s.get('name') == query: 
                if DEBUG_MODE: print(f"🔍 [Retriever 디버그] 2순위 명칭 매칭성공 (Name): {query}")
                return s
        # 3. 부분 일치 (Fallback)
        for s in self.symbols_db:
            if query.lower() in s.get('name', '').lower(): 
                if DEBUG_MODE: print(f"🔍 [Retriever 디버그] 3순위 느슨한 부분 매칭성공: {s.get('name')}")
                return s
        return None

    def _safe_truncate(self, text: str) -> str:
        """문자열 단위가 아닌 라인 단위로 끊어서 코드 파손 방지"""
        lines = text.splitlines()
        if len(lines) <= self.max_context_lines:
            return text
        
        if DEBUG_MODE:
            print(f"⚠️ [Retriever 디버그] 경고: 컨텍스트가 한계선({self.max_context_lines}줄)을 초과하여 꼬리 절단단행!")
        truncated = lines[:self.max_context_lines]
        truncated.append("\n... [⚠️ WARNING: Context truncated by line limit to protect token budget] ...")
        return "\n".join(truncated)

def main():
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    if not query:
        print("💡 Usage: python cline_tools/jjap_retriever.py <symbol_id_or_name>")
        return
    
    retriever = JjapRetriever(Path.cwd())
    print(retriever.retrieve_symbol(query))
```

--------------------------------------------------

### 📄 tools/universal_indexer/jjap_watcher.py
#### 🧱 Code Skeleton:
```python
def import_file_directly(module_name: str, file_path: Path):
    """파이썬 모듈 캐시를 우회하고 하드디스크의 파일을 날것 그대로 강제 로드합니다."""
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"❌ '{file_path}' 경로에서 spec을 추출할 수 없습니다.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def run_pipeline():
    """소스코드 변경 포착 시 인덱싱 공장과 지도 제작소를 연쇄 가동하는 마스터 파이프라인"""
    print("\n🔄 [파이프라인 트리거] 소스코드 변동 정밀 포착! 정렬 재인덱싱 작전 개시...")
    
    try:
        # [Step 3-1] 메모리 찌꺼기 청소 (캐시 크래시 원천 방지)
        for key in ["indexer", "update_map", "create_ai_map"]:
            if key in sys.modules:
                del sys.modules[key]

        # 🎯 1단계: 인덱서 강제 가동 (AdvancedIndexerV2)
        indexer_path = CURRENT_DIR / "indexer.py"
        indexer_module = import_file_directly("indexer", indexer_path)
        print("  ➡️ 1/3 단계: 신형 인덱서 V2 스캔 엔진 가동 중...")
        
        indexer_obj = indexer_module.AdvancedIndexerV2(PROJECT_ROOT)
        indexer_obj.scan_project()
        
        # 디버그 모드일 때만 심볼 정밀 스캔 내역 도배
        if DEBUG_MODE:
            classes = [s["name"] for s in indexer_obj.symbols if s.get("type") == "class"]
            methods = [s["name"] for s in indexer_obj.symbols if s.get("type") in ["function", "method"]]
            print(f"    🧬 [디버그] 클래스 목록 추출: {classes}")
            print(f"    🎯 [디버그] 함수/메서드 목록 추출: {methods}")
            
        # 🎯 2단계: 기존 인간용 백과사전 지도 제작 (update_map.py)
        update_map_path = CURRENT_DIR / "update_map.py"
        update_map_module = import_file_directly("update_map", update_map_path)
        print("  ➡️ 2/3 단계: 인간용 CODEBASE_MAP.md 장부 최신화 중...")
        update_map_module.update_map()        
        
        # 🎯 3단계: 형님의 특명! AI 전용 초경량 극한 요약 지도 실시간 동기화 (신설 🔥)
        create_ai_map_path = CURRENT_DIR / "create_ai_map.py"
        create_ai_map_module = import_file_directly("create_ai_map", create_ai_map_path)
        print("  ➡️ 3/3 단계: AI용 AI_CODEBASE_MAP.md 초경량 압축 시그니처 지도 생산 중...")
        create_ai_map_module.generate_ai_optimized_map()
        
        print("✅ [동기화 완료] 모든 장부와 AI 가성비 지도가 최신 상태로 바느질되었습니다!\n")
        
    except Exception as e:
        print(f"❌ [에러 발생] 파이프라인 구동 중 사고 발생: {e}")
        import traceback
        if DEBUG_MODE:
            traceback.print_exc()

class CodeChangeHandler:
    def __init__(self):
        self.last_trigger_time = 0
        self.debounce_duration = 0.5  # 디바운스 초단위 설정
        
    def dispatch(self, event):
        if event.is_directory:
            return
            
        src_path = Path(event.src_path)
        
        # 검열 검문소: 백그라운드 찌꺼기나 결과물 파일은 가볍게 무시
        # 🛡️ [격리 방어선] 무한 루프 폭파 방지용 system_memory 및 system_maps 폴더 무시 키워드 추가 주입!
        EXCLUDE_KEYWORDS = [".venv", ".git", "__pycache__", "cline_tools", ".json", ".md", "system_memory", "system_maps"]
        if any(kw in src_path.as_posix() for kw in EXCLUDE_KEYWORDS):
            return
            
        if src_path.suffix == ".py":
            current_time = time.time()
            if current_time - self.last_trigger_time > self.debounce_duration:
                self.last_trigger_time = current_time
                if DEBUG_MODE:
                    print(f"🔔 [감시망 포착] 파일 변경 감지됨: {src_path.name}")
                run_pipeline()

def main():
    print("=" * 70)
    print("🚀 [Jjap-Cursor Watcher] 실시간 백그라운드 감시망 기동!")
    print(f"📂 감시 대상 진짜 루트 절대 경로: {PROJECT_ROOT}")
    print(f"⚙️  초정밀 디버깅 모드 상태: {'🔴 ON' if DEBUG_MODE else '⚪ OFF'}")
    print("💡 소스코드를 수정하고 저장(Ctrl+S)하면 AI 초경량 지도가 무한 자동 갱신됩니다.")
    print("=" * 70)
    
    # 초도 기동 시 장부가 없을 수 있으므로 파이프라인 1회 선제 타격 가동
    run_pipeline()
    
    try:
        from watchdog.observers.polling import PollingObserver as Observer
    except ImportError:
        from watchdog.observers import Observer

    event_handler = CodeChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=str(PROJECT_ROOT), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

--------------------------------------------------

### 📄 tools/universal_indexer/switch.py
*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*

--------------------------------------------------

### 📄 tools/universal_indexer/update_map.py
#### 🧱 Code Skeleton:
```python
def update_map():
    # 🔄 [안전 보장] 실행 환경에 구애받지 않도록 현재 스크립트 위치 기준 진짜 프로젝트 마스터 루트를 추적합니다.
    SCRIPT_DIR = Path(__file__).parent.resolve()
    if SCRIPT_DIR.name == "universal_indexer" and SCRIPT_DIR.parent.name == "tools":
        PROJECT_ROOT = SCRIPT_DIR.parent.parent
    else:
        PROJECT_ROOT = SCRIPT_DIR

    # 🧠 마스터 루트 기준으로 경로를 확실하게 조준하여 불러오기 및 출력을 고정합니다.
    context_file = PROJECT_ROOT / "system_memory" / ".jjap_context.json"
    symbols_file = PROJECT_ROOT / "system_memory" / ".jjap_symbols.json"
    output_file = PROJECT_ROOT / "system_maps" / "CODEBASE_MAP.md"
    
    if not context_file.exists() or not symbols_file.exists():
        print("❌ Error: 인덱서 데이터 파일(.jjap_context 또는 .jjap_symbols)이 없습니다.")
        print("💡 해결책: 인덱서(indexer.py)를 먼저 실행한 뒤 이 스크립트를 돌리세요.")
        return

    # 1. 최신 데이터 로드
    with open(context_file, "r", encoding="utf-8") as f:
        context_data = json.load(f).get("files", {})
        
    with open(symbols_file, "r", encoding="utf-8") as f:
        symbols_list = json.load(f).get("symbols", [])

    # 🚨 [검열 시스템 동기화] 인덱서와 싱크로율 100% 맞추기
    # 혹시라도 장부에 흔적이 남아있거나, 루트의 실행 파일들이 맵에 찍히는 걸 원천 차단합니다.
    EXCLUDE_KEYWORDS = [".venv", ".git", "__pycache__", "cline_tools"]

    # 2. 에이전트 분석을 돕기 위해 파일별 심볼 및 관계 매핑 구조 생성
    symbols_by_file = {}
    for s in symbols_list:
        file_path = s.get("file", "")
        
        # 🚨 검열 컷 1: 심볼 리스트 중에 제외 폴더나 start.py가 있으면 장부에서 누락 처리
        if any(p in file_path for p in EXCLUDE_KEYWORDS) or "start.py" in file_path:
            continue
            
        if file_path not in symbols_by_file:
            symbols_by_file[file_path] = []
        symbols_by_file[file_path].append(s)

    # 3. CODEBASE_MAP.md 최종 렌더링
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 🏗️ 짭커서 프로젝트 CODEBASE MAP\n\n")
        
        # 🚨 검열 컷 2: 순수 유효 파일만 발라내기 (start.py 및 도구 폴더 완전히 소멸시킴)
        valid_files = {}
        for path, info in context_data.items():
            if any(p in path for p in EXCLUDE_KEYWORDS) or "start.py" in path:
                continue
            valid_files[path] = info

        f.write(f"현재 인덱싱된 총 파일 수: **{len(valid_files)}개**\n\n")
        
        # 📂 모듈 인덱스 구역
        f.write("## 🗂️ [Module Index]\n")
        for path in sorted(valid_files.keys()):
            f.write(f"- `{path}`\n")
        
        # 💀 뼈대 및 의존성 관계 상세 구역
        f.write("\n## 💀 [Skeleton & Dependency 명세서]\n")
        for path, info in sorted(valid_files.items()):
            f.write(f"### 📄 {path}\n")
            
            # 해당 파일에 속한 상세 심볼(클래스/함수)의 호출 관계 먼저 요약
            file_symbols = symbols_by_file.get(path, [])
            if file_symbols:
                f.write("#### 🔍 내부 심볼 및 의존성 관계:\n")
                for s in file_symbols:
                   # 수정 코드: s['full_name']을 s['name']으로 변경
                    f.write(f"- **[{s['type'].upper()}]** `{s['name']}` (Line: {s['start_line']}~{s['end_line']})\n")
                    if s.get("calls"):
                        f.write(f"  - 🔗 *Calls (호출하는 것)*: `{', '.join(s['calls'])}`\n")
                    if s.get("used_by"):
                        f.write(f"  - 🎯 *Used By (나를 부르는 곳)*: `{', '.join(s['used_by'])}`\n")
                f.write("\n")

            # 실제 코드 뼈대(Skeleton) 출력
            skeleton_text = info.get("skeleton", "").strip()
            if skeleton_text:
                f.write("#### 🧱 Code Skeleton:\n")
                f.write("```python\n")
                f.write(f"{skeleton_text}\n")
                f.write("```\n\n")
            else:
                f.write("*선언된 클래스나 함수가 없는 파일이거나 모듈입니다.*\n\n")
                
            f.write("-" * 50 + "\n\n")

    print(f"✅ [SUCCESS] V2 인덱스 정밀 데이터를 결합하여 {output_file.name} 업데이트 완료! (스텔스 필터 적용)")
```

--------------------------------------------------

