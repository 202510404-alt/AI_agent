import os
from pathlib import Path
try:
    import pathspec
except ImportError:
    pathspec = None

class GitIgnoreMatcher:
    """프로젝트 내 모든 .gitignore 패턴을 수집하고 정밀 검증하는 전용 파서"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self._spec = None

    def _load_specs(self):
        """지연 로딩(Lazy Loading)으로 모든 .gitignore 파일 수집 및 통합 파싱"""
        patterns = []
        
        # 디폴트 제외 대상 기본 포함 (최적화 및 필수 방어)
        default_ignores = [
            ".git/", ".venv/", "node_modules/", "__pycache__/",
            "system_memory/", "system_maps/"
        ]
        patterns.extend(default_ignores)

        for root, _, files in os.walk(self.project_root):
            if ".gitignore" in files:
                gitignore_path = Path(root) / ".gitignore"
                rel_dir = Path(root).relative_to(self.project_root).as_posix()
                prefix = "" if rel_dir == "." else f"{rel_dir}/"

                try:
                    with open(gitignore_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                patterns.append(f"{prefix}{line}")
                except Exception:
                    pass

        if pathspec:
            self._spec = pathspec.PathSpec.from_lines("gitwildmatch", patterns)
        else:
            self._spec = patterns

    def is_ignored(self, relative_path: str) -> bool:
        """파일 경로가 .gitignore 패턴에 연관되는지 평가 (O(1) 캐싱 스펙 활용)"""
        if self._spec is None:
            self._load_specs()

        posix_path = Path(relative_path).as_posix()

        if pathspec and isinstance(self._spec, pathspec.PathSpec):
            return self._spec.match_file(posix_path)

        # Fallback: simple prefix checking
        return any(posix_path.startswith(pat.rstrip("/")) for pat in self._spec)