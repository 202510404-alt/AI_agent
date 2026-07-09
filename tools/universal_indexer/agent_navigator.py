import json
import sys
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

# =====================================================================
# 🧠 CORE INTELLIGENCE: MULTI-TARGET CODE SLICE LOADER
# =====================================================================
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
    
# =====================================================================
# 🎨 GUI INTERFACE LAYER (UPGRADED VERSION)
# =====================================================================
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

if __name__ == "__main__":
    # 🔄 실행 컨텍스트 루트 자동 정렬 (신규 2단계 깊이 tools/universal_indexer/ 구조 전면 동기화)
    current_dir = Path(__file__).parent.resolve()
    
    # 구형 폴더명들을 걷어내고, 현재 새롭게 안착한 universal_indexer 명칭으로 마스터 루트를 확보합니다.
    if current_dir.name == "universal_indexer" and current_dir.parent.name == "tools":
        project_root = current_dir.parent.parent
    else:
        project_root = current_dir

    root_window = tk.Tk()
    app = JjapCursorNavigatorGUI(root_window, project_root)
    root_window.mainloop()