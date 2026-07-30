import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

# 🧠 SINGLE SOURCE OF TRUTH: import CodeExtractor from agent_code_extractor
try:
    from agent_code_extractor import CodeExtractor
except ImportError:
    idx_path = Path(__file__).parent.resolve()
    if str(idx_path) not in sys.path:
        sys.path.insert(0, str(idx_path))
    from agent_code_extractor import CodeExtractor

# 하위 호환성을 위해 SemanticNavigator를 CodeExtractor의 별칭으로 보존
SemanticNavigator = CodeExtractor

# =====================================================================
# 🎨 GUI INTERFACE LAYER (UPGRADED VERSION)
# =====================================================================
class JjapCursorNavigatorGUI:
    def __init__(self, root, project_root: Path):
        self.root = root
        self.project_root = project_root
        self.extractor = CodeExtractor(project_root)
        self.last_markdown_content = ""

        # GUI Title에 현재 스캔 모드를 가독성 있게 표기
        self.root.title(f"⚡ Jjap-Cursor Agent Navigator v2.0 (Auto-Exporter) | 모드: {self.extractor.scan_mode}")
        self.root.geometry("1000x750")

        self.main_container = ttk.Frame(root, padding="10")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        input_label = ttk.Label(self.main_container, text=f"📥 [에이전트 요청 프롬프트 입력 구역 - 현재 모드: {self.extractor.scan_mode}]", font=("Malgun Gothic", 11, "bold"))
        input_label.pack(anchor=tk.W, pady=(0, 5))

        self.prompt_input = tk.Text(self.main_container, height=6, font=("Malgun Gothic", 10))
        self.prompt_input.pack(fill=tk.X, pady=(0, 10))
        
        # 안내 문구 최적화
        if self.extractor.scan_mode == "SRC":
            self.prompt_input.insert(tk.END, "💡 실전 테스트 양식 예시 (SRC 모드):\nsrc/src/main/java/com/desertcore/deathevent.java:32-60")
        else:
            self.prompt_input.insert(tk.END, "💡 실전 테스트 양식 예시 (ROOT 모드):\nsrc/main/java/com/desertcore/deathevent.java:32-60")

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
            state=tk.DISABLED
        )
        self.export_button.pack(side=tk.RIGHT, padx=(5, 0))

        output_label = ttk.Label(self.main_container, text="📄 [AI 배송용 최적화 켄텍스트 보따리 (출력 결과)]", font=("Malgun Gothic", 11, "bold"))
        output_label.pack(anchor=tk.W, pady=(0, 5))

        self.code_display = tk.Text(self.main_container, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        self.code_display.pack(fill=tk.BOTH, expand=True)

        self.status_label = ttk.Label(self.main_container, text=f"🟢 대기 중... [{self.extractor.scan_mode} 모드] 프롬프트를 입력하고 가동 버튼을 누르십시오.", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=(10, 0))

    def execute_slicing_pipeline(self):
        raw_prompt = self.prompt_input.get("1.0", tk.END).strip()
        if not raw_prompt or raw_prompt.startswith("💡"):
            messagebox.showwarning("입력 오류", "형님, 슬라이싱할 대상 파일 경로와 라인을 입력해 주십시오!")
            return

        result = self.extractor.process(raw_prompt, auto_save=True)
        extracted_slices = result["slices"]

        if not extracted_slices:
            self.status_label.config(text="❌ 추출 실패: 프롬프트에서 타겟 패턴('경로:줄번호')을 인식하지 못했습니다.")
            messagebox.showerror("추출 실패", "지정된 경로 문자열 형식을 확인해 주십시오.")
            return

        self.code_display.delete("1.0", tk.END)
        self.last_markdown_content = result["markdown"]
        self.code_display.insert(tk.END, self.last_markdown_content)
        
        saved_path = result.get("saved_path")
        if saved_path:
            status_msg = f"🟢 [{self.extractor.scan_mode}] 추출 및 마크다운 자동 저장 완료! -> system_maps/{saved_path.name}"
            self.export_button.config(state=tk.NORMAL)
        else:
            status_msg = f"⚠️ 화면 추출 완료했으나 자동 파일 저장 실패"

        self.status_label.config(text=status_msg)
        
    def manual_export_file(self):
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
    current_dir = Path(__file__).parent.resolve()
    
    # 🔄 두 단계 깊이인 tools/universal_indexer/ 구조일 때 마스터 루트 경로 역추적 동기화
    if current_dir.name == "universal_indexer" and current_dir.parent.name == "tools":
        project_root = current_dir.parent.parent
    else:
        project_root = current_dir

    root_window = tk.Tk()
    app = JjapCursorNavigatorGUI(root_window, project_root)
    root_window.mainloop()