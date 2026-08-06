"""
tools/multi_agent_system/code_patcher.py
AI가 출력한 기존 코드(existing_code)를 대상 파일에서 100% 일치 탐색하여
수정된 코드(replacement_code)로 정밀 치환(Partial Patching)하는 도구
"""

from pathlib import Path

class CodePatcher:
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir).resolve()

    def apply_patch(self, rel_path: str, existing_code: str, replacement_code: str) -> dict:
        """
        파일 내에서 existing_code를 검증하여 replacement_code로 1:1 교체합니다.
        """
        target_path = (self.root_dir / rel_path.strip().replace("\\", "/")).resolve()
        
        if not target_path.exists() or not target_path.is_file():
            return {
                "success": False,
                "message": f"❌ [PATCH FAIL] 대상 파일을 찾을 수 없습니다: {rel_path}"
            }

        try:
            with open(target_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 줄바꿈 단일화 (들여쓰기 파괴 방지를 위해 .strip() 제거)
            clean_content = content.replace("\r\n", "\n")
            clean_existing = existing_code.replace("\r\n", "\n")
            clean_replacement = replacement_code.replace("\r\n", "\n")

            # A. 신규 작성 또는 빈 파일 덮어쓰기 처리 (existing_code가 빈 문자열인 경우)
            if not clean_existing:
                patched_content = clean_replacement
            else:
                # B. 100% 완전 일치 여부 검증
                if clean_existing not in clean_content:
                    return {
                        "success": False,
                        "message": f"❌ [PATCH FAIL] 입력한 '기존 코드'가 {rel_path} 파일 내에 100% 일치하는 구간이 없습니다."
                    }

                # C. 중복 구간 존재 여부 검증
                match_count = clean_content.count(clean_existing)
                if match_count > 1:
                    return {
                        "success": False,
                        "message": f"⚠️ [PATCH FAIL] 지정한 '기존 코드'가 {rel_path} 내에 {match_count}개 존재합니다. 문맥을 더 포함하세요."
                    }

                # D. 1:1 정밀 치환 실행
                patched_content = clean_content.replace(clean_existing, clean_replacement, 1)

            # 4. 파일 저장
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(patched_content)

            return {
                "success": True,
                "message": f"✅ [PATCH SUCCESS] {rel_path} 파일의 특정 구간이 성공적으로 수정되었습니다!"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"💥 [PATCH ERROR] 파일 수정 중 예외 발생: {e}"
            }