import json
import sys
import re
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# =====================================================================
# 🧠 CORE INTELLIGENCE: MULTI-TARGET CODE SLICE LOADER (HEADLESS/AGENT ONLY)
# =====================================================================
class CodeExtractor:
    """
    AI 에이전트 및 파이프라인 전용 코드 정밀 추출기 (Headless Code Extractor)
    - UI(Tkinter 등) 요소를 완전히 제거하고 순수 데이터 처리 및 정보 흐름만 수행
    - 기존 SemanticNavigator의 슬라이싱, 경로 구제, 양방향 심볼 연관 추적 로직 100% 보존
    """
    def __init__(self, root_dir: str | Path):
        self.raw_root_dir = Path(root_dir).resolve()
        self.scan_mode = "ROOT"
        
        # 🎛️ [SCAN_MODE 스위치 반영 - universal_indexer/switch.py 절대 위치 고정]
        try:
            idx_path = str((self.raw_root_dir / "tools" / "universal_indexer").resolve())
            if idx_path not in sys.path:
                sys.path.insert(0, idx_path)
            
            import switch
            self.scan_mode = getattr(switch, "SCAN_MODE", "ROOT")
            print(f"🎛️ [SWITCH DETECTED] 현재 탐색 스위치 모드: {self.scan_mode}")
        except Exception as e:
            print(f"⚠️ [SWITCH WARNING] switch.py를 로드하지 못해 기본 'ROOT' 모드로 동작합니다. (이유: {e})")

        # 🚀 SRC 모드일 경우 하드디스크 탐색 기준점(self.root_dir)에 'src' 폴더를 강제 결합
        if self.scan_mode == "SRC":
            self.root_dir = self.raw_root_dir / "src"
            print(f"📁 [MODE: SRC] 탐색 마스터 루트가 복사/격리용 src 폴더로 변경되었습니다: {self.root_dir}")
        else:
            self.root_dir = self.raw_root_dir
            print(f"📁 [MODE: ROOT] 탐색 마스터 루트가 프로젝트 원본 루트로 설정되었습니다: {self.root_dir}")

        # 🧠 [불러오기 교정] 장부 정보는 언제나 프로젝트의 실제 본체 루트(raw_root_dir) 기준으로 가져옵니다.
        self.symbols_path = self.raw_root_dir / "system_memory" / ".jjap_symbols.json"
        self.symbols_data = self._load_database()

    def _load_database(self) -> dict:
        if not self.symbols_path.exists():
            return {"symbols": []}
        try:
            with open(self.symbols_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"symbols": []}

    def resolve_file_path(self, raw_path_str: str) -> Path | None:
        """
        [경로 구제 통합 레이더]
        SCAN_MODE, 상대 경로, extraction_target_project, tools 등 
        다양한 디렉토리 변수를 추적하여 실제 존재하는 파일의 Absolute Path를 반환합니다.
        """
        clean_path_str = raw_path_str.strip().replace("\\", "/")
        
        # 🚨 [SECURITY GUARD] .env 등 환경변수 및 민감 정보 파일 접근 원천 차단
        if any(part.startswith(".env") or part.endswith(".env") for part in clean_path_str.split("/")):
            print(f"🛡️ [SECURITY BLOCKED] 민감 파일 접근이 차단되었습니다: {clean_path_str}")
            return None

        # 1차 시도: 모드별 스펙에 맞춘 경로 조립
        if self.scan_mode == "SRC":
            if clean_path_str.startswith("src/src/"):
                candidate = self.raw_root_dir / clean_path_str
            elif clean_path_str.startswith("src/"):
                candidate = self.raw_root_dir / clean_path_str
            else:
                candidate = self.raw_root_dir / "src" / clean_path_str
        else:
            candidate = self.raw_root_dir / clean_path_str

        if candidate.exists() and candidate.is_file():
            return candidate

        # 2차 시도 (구제금융): raw_root_dir 기준 직접 탐색
        candidate_raw = self.raw_root_dir / clean_path_str
        if candidate_raw.exists() and candidate_raw.is_file():
            return candidate_raw

        # 3차 시도 (구제금융): extraction_target_project 하위 탐색
        candidate_target = self.raw_root_dir / "extraction_target_project" / clean_path_str
        if candidate_target.exists() and candidate_target.is_file():
            return candidate_target

        # 4차 시도 (구제금융): tools 하위 탐색
        candidate_tools = self.raw_root_dir / "tools" / clean_path_str
        if candidate_tools.exists() and candidate_tools.is_file():
            return candidate_tools

        return None

    def extract_multi_slices(self, raw_prompt: str) -> list[dict]:
        """
        [Multi-Target Protocol Parser - 정규식 통합 및 경로 구제 완전판]
        프롬프트를 파싱하여 코드 슬라이스 묶음(list of dict)을 리턴합니다.
        """
        print("\n" + "="*60)
        print("🚨 [EXTRACTOR ON] 멀티 슬라이싱 파이프라인 기동!!!")
        print(f"📥 유저 입력 프롬프트: {repr(raw_prompt)}")
        print(f"⚙️ 현재 매핑 모드: {self.scan_mode} (기준 경로: {self.root_dir})")
        print("="*60)

        pattern = r"([a-zA-Z0-9_\-\./\\]+)[\s:]+(?:L)?(\d+)(?:\s*-\s*(?:L)?(\d+))?"
        matches = re.findall(pattern, raw_prompt)

        print(f"🔍 정규식 1차 타겟 스캔 결과: {matches}")
        if not matches:
            print("⚠️ 매칭되는 파일 경로 및 라인 규격이 없습니다. 빈 배열 리턴.")
            return []

        extracted_slices = []
        req_num = 1

        for match in matches:
            file_rel_path = match[0].strip().replace("\\", "/")
            start_line = int(match[1])
            end_line = int(match[2]) if match[2] else start_line

            print(f"\n🎯 [요청 #{req_num}] 메인 타겟 분석 시작 -> {file_rel_path} ({start_line} ~ {end_line} 라인)")

            target_file_path = self.resolve_file_path(file_rel_path)
            
            if not target_file_path:
                print(f"   ❌ [ERROR] 해당 파일이 실제 경로에 존재하지 않습니다! 패스합니다: {file_rel_path}")
                continue

            print(f"   🟢 [경로 확정] 디스크 실체 발견: {target_file_path}")

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

                extracted_slices.append({
                    "req_num": f"{req_num}",
                    "file": file_rel_path,
                    "line_range": f"{safe_start}-{safe_end}",
                    "code": slice_code
                })

                # [2단계] 🔗 제이슨 기반 2차 심볼 탐색기 가동
                print(f"   📡 [2차 사냥기] 잘려 나온 텍스트 내부에서 양방향 심볼 식별 개시...")

                defined_names = re.findall(r"(?:def|class)\s+([a-zA-Z0-9_]+)", slice_code)
                called_names = re.findall(r"(?:[a-zA-Z0-9_]+\.)?([a-zA-Z0-9_]+)\s*\(", slice_code)
                file_ref_names = [f for f in re.findall(r'[\'"]([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)[\'"]', slice_code) if f != file_rel_path]

                builtin_filters = {"print", "len", "range", "open", "dict", "list", "set", "any", "all", "max", "min", "append", "get", "strip", "split", "exists", "readlines", "join"}
                filtered_called_names = [name for name in called_names if name not in builtin_filters]

                target_symbols = list(set(defined_names + filtered_called_names + file_ref_names))
                print(f"   📦 [양방향 통합] 징집 대상 심볼 목록: {target_symbols}")
                
                symbols_list = self.symbols_data.get("symbols", [])
                print(f"   📚 로드된 JSON 장부 총 심볼 개수: {len(symbols_list)}개")

                for target_name in target_symbols:
                    print(f"      🔎 [전역 심볼 대조] 이름: '{target_name}' -> 장부 전체 스캔 중...")
                    match_found = False
                    
                    for s in symbols_list:
                        if s.get("name") == target_name:
                            match_found = True
                            t_file = s.get("path") or s.get("file", "")
                            s_start = s.get("start_line", 1)
                            s_end = s.get("end_line", 1)

                            # 정방향 연관 심볼 추적
                            if t_file != file_rel_path:
                                print(f"         ➡️ [정방향] 내가 불러온 함수 본체 포착 -> {t_file} ({s_start}~{s_end}라인)")
                                callee_file_path = self.resolve_file_path(t_file)
                                    
                                if callee_file_path:
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

                            # 역방향 연관 심볼 추적 (used_by)
                            if (target_name in defined_names) or (t_file == file_rel_path):
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
                                                sub_t_file = target_s.get("path") or target_s.get("file", "")
                                                s_id = target_s.get("symbol_id", "")
                                                sub_s_name = target_s.get("name", "")
                                                
                                                if (s_id == ub_id) or (ub_id.endswith(s_id)) or (sub_s_name == ub_symbol_name and (sub_t_file == ub_file or ub_file.endswith(sub_t_file) or sub_t_file.endswith(ub_file))):
                                                    sub_match_found = True
                                                    ub_file_path = self.resolve_file_path(sub_t_file)
                                                        
                                                    if ub_file_path:
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
                print(f"💥 [CRITICAL ERROR] 슬라이싱 중 예외 발생: {e}")
                traceback.print_exc()

            req_num += 1

        print("\n" + "="*60)
        print(f"🏁 최종 반환할 총 슬라이스 묶음 개수: {len(extracted_slices)}개")
        print("="*60 + "\n")
        return extracted_slices

    def format_as_markdown(self, extracted_slices: list[dict]) -> str:
        """
        슬라이싱 데이터 배열을 받아서 LLM 및 에이전트에 주입할 마크다운 문맥으로 변환합니다.
        """
        if not extracted_slices:
            return ""

        md_lines = []
        md_lines.append("# ==========================================================================")
        md_lines.append("# 🎯 AI GLOBAL GUIDELINES: 코드 무결성 및 디버깅 중심 가이드")
        md_lines.append(f"# [SCAN_MODE] {self.scan_mode}")
        md_lines.append("# ==========================================================================")

        for slc in extracted_slices:
            md_lines.append(f"# 📄 [요청 {slc['req_num']}] TARGET: {slc['file']} ({slc['line_range']}라인)")
            md_lines.append("# ----------------------------------------------------------")
            md_lines.append("```python")
            md_lines.append(slc["code"].rstrip())
            md_lines.append("```\n")

        return "\n".join(md_lines)

    def process(self, raw_prompt: str, auto_save: bool = True, output_path: str | Path = None) -> dict:
        """
        [통합 매니저 파이프라인]
        프롬프트를 입력받아 슬라이스를 추출하고, 마크다운 반환 및 마스터 격리 폴더로 내보냅니다.
        
        Returns:
            dict: {
                "slices": list[dict],    # 원본 데이터 객체 목록
                "markdown": str,         # 생성된 마크다운 텍스트
                "saved_path": Path|None  # 저장된 실제 경로
            }
        """
        slices = self.extract_multi_slices(raw_prompt)
        markdown_text = self.format_as_markdown(slices)
        save_target_path = None

        if auto_save and markdown_text:
            if output_path:
                save_target_path = Path(output_path)
            else:
                save_target_path = self.raw_root_dir / "system_maps" / "extracted_context.md"

            try:
                save_target_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_target_path, "w", encoding="utf-8") as f:
                    f.write(markdown_text)
                print(f"💾 마크다운 데이터가 안전하게 저장되었습니다: {save_target_path}")
            except Exception as e:
                print(f"⚠️ 파일 저장 실패: {e}")

        return {
            "slices": slices,
            "markdown": markdown_text,
            "saved_path": save_target_path
        }


# =====================================================================
# 🚀 CLI & EXTERNAL PIPELINE INTERFACE
# =====================================================================
if __name__ == "__main__":
    current_dir = Path(__file__).parent.resolve()
    
    # tools/multi_agent_system/ 또는 tools/universal_indexer/ 위치 모두 고려하여 마스터 루트 역추적
    if current_dir.name in ("multi_agent_system", "universal_indexer") and current_dir.parent.name == "tools":
        project_root = current_dir.parent.parent
    else:
        project_root = current_dir

    extractor = CodeExtractor(project_root)

    # CLI 지원: 터미널에서 인자로 전달받은 경우 실행
    if len(sys.argv) > 1:
        prompt_arg = " ".join(sys.argv[1:])
        result = extractor.process(prompt_arg)
        print("\n--- [RESULT MARKDOWN OUTPUT] ---")
        print(result["markdown"])
    else:
        print("💡 사용법: python agent_code_extractor.py \"<파일경로:줄번호>\"")