"""
tools/multi_agent_system/project_scale_detector.py
프로젝트의 규모를 정밀 측정하여 AI 처리 한계 초과 여부를 판단하고,
필요 시 유연한 깊이(depth)의 얕은 폴더 구조(Shallow Tree Map)를 생성합니다.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

import mimetypes
from tools.universal_indexer.core_parsers.gitignore_parser import GitIgnoreMatcher

EXCLUDE_KEYWORDS = [
    "node_modules", ".venv", ".git", "__pycache__",
    "cline_tools", "system_memory", "system_maps", "dist", "build"
]

# 제외할 미디어/바이너리 확장자 모음 (1차 속도 보장용)
BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico", ".svg",
    ".mp3", ".mp4", ".avi", ".mov", ".wav", ".flac",
    ".zip", ".tar", ".gz", ".7z", ".rar", ".exe", ".dll", ".so", ".dylib",
    ".pdf", ".docx", ".xlsx", ".pptx", ".ttf", ".woff", ".woff2", ".eot"
}

# 구조적 데이터 반복 파일 확장자 (상위 N개 샘플링 처리)
REPETITIVE_DATA_EXTENSIONS = {".json", ".csv", ".tsv", ".xml", ".yaml", ".yml", ".lock"}


class ProjectScaleDetector:
    def __init__(
        self, 
        project_root: Path,
        max_files: int = 500,             # 상향 조정된 최대 파일 수
        max_total_lines: int = 50000,     # 상향 조정된 최대 소스코드 줄 수
        max_estimated_tokens: int = 200000, # 상향 조정된 최대 토큰 수
        max_file_size_bytes: int = 300 * 1024, # 300KB 초과 시 대용량 파일 스킵
        sample_line_limit: int = 20        # 반복 데이터 파일 샘플링 라인 수
    ):
        self.project_root = Path(project_root).resolve()
        self.max_files = max_files
        self.max_total_lines = max_total_lines
        self.max_estimated_tokens = max_estimated_tokens
        self.max_file_size_bytes = max_file_size_bytes
        self.sample_line_limit = sample_line_limit
        self.gitignore_matcher = GitIgnoreMatcher(self.project_root)

    def _is_binary_file(self, file_path: Path) -> bool:
        """확장자, MIME Type, Null Byte 검사로 바이너리/미디어 파일 판별"""
        if file_path.suffix.lower() in BINARY_EXTENSIONS:
            return True
            
        mime, _ = mimetypes.guess_type(file_path)
        if mime and not (mime.startswith("text/") or mime in ["application/json", "application/javascript", "application/xml"]):
            return True

        try:
            with open(file_path, "rb") as f:
                chunk = f.read(1024)
                if b"\x00" in chunk: # Null byte 감지 시 바이너리로 판단
                    return True
        except Exception:
            return True

        return False

    def analyze_project_scale(self, target_dir: Optional[Path] = None) -> Dict[str, Any]:
        """프로젝트 규모를 정밀 측정하며, Dynamic Depth를 계산합니다."""
        scan_dir = target_dir or self.project_root
        file_count = 0
        total_lines = 0

        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_KEYWORDS]
            if any(kw in root for kw in EXCLUDE_KEYWORDS):
                continue

            for file in files:
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.project_root)

                # 1. gitignore 필터링
                if self.gitignore_matcher.is_ignored(rel_path):
                    continue

                # 2. 미디어/바이너리 파일 차단
                if self._is_binary_file(file_path):
                    continue

                # 3. 300KB 초과 대용량 파일은 1개 파일로 카운트하되 줄 수 산출 스킵
                if file_path.stat().st_size > self.max_file_size_bytes:
                    file_count += 1
                    total_lines += 50 # 대용량 스킵 가상 산정값
                    continue

                file_count += 1
                ext = file_path.suffix.lower()

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        # 4. JSON/CSV 등 반복 구조 데이터 파일은 상위 N줄만 샘플링
                        if ext in REPETITIVE_DATA_EXTENSIONS:
                            sample_count = 0
                            for _ in f:
                                sample_count += 1
                                if sample_count >= self.sample_line_limit:
                                    break
                            total_lines += sample_count
                        else:
                            total_lines += sum(1 for _ in f)
                except Exception:
                    pass

        estimated_tokens = total_lines * 9
        is_oversized = (
            file_count > self.max_files or 
            total_lines > self.max_total_lines or 
            estimated_tokens > self.max_estimated_tokens
        )

        # 5. Dynamic Depth 계산 (규모에 맞춰 탐색 깊이 2~5 단계 자동 산출)
        if file_count > 1500 or total_lines > 100000:
            recommended_depth = 2
        elif file_count > 800 or total_lines > 60000:
            recommended_depth = 3
        elif file_count > 400 or total_lines > 30000:
            recommended_depth = 4
        else:
            recommended_depth = 5

        return {
            "file_count": file_count,
            "total_lines": total_lines,
            "estimated_tokens": estimated_tokens,
            "is_oversized": is_oversized,
            "recommended_depth": recommended_depth
        }

    def generate_shallow_structure_map(self, max_depth: int = 3, target_dir: Optional[Path] = None) -> str:
        """
        AI가 감당 불가능할 때 전체 맵 대신 제공하는 겉핥기 얕은 구조 지도를 생성합니다.
        max_depth를 통해 2~7단계 등 깊이를 유연하게 제어합니다.
        """
        scan_dir = target_dir or self.project_root
        lines = [
            "# 🗺️ HIGH-LEVEL PROJECT STRUCTURE MAP (OVERSIZED PROJECT DETECTED)",
            f"> **[안내]** 프로젝트 규모가 커 상위 {max_depth}단계 개요 구조만 표시되었습니다.",
            "> **[AI 수칙]** 분석이 필요한 세부 폴더 경로를 확인한 후 `extract_targeted_ai_map` 도구를 사용해 타깃 지도를 요청하십시오.",
            "```markdown",
            "project_root/"
        ]

        def _build_tree(current_dir: Path, current_depth: int):
            if current_depth > max_depth:
                return

            try:
                entries = sorted(list(current_dir.iterdir()), key=lambda x: (not x.is_dir(), x.name))
            except PermissionError:
                return

            indent = "│   " * (current_depth - 1)
            for entry in entries:
                if entry.name in EXCLUDE_KEYWORDS or entry.name.startswith("."):
                    continue

                rel_path = entry.relative_to(self.project_root).as_posix()
                if entry.is_dir():
                    lines.append(f"{indent}├── {entry.name}/ [📂 {rel_path}]")
                    if current_depth < max_depth:
                        _build_tree(entry, current_depth + 1)
                else:
                    lines.append(f"{indent}├── {entry.name} [📄 {rel_path}]")

        _build_tree(scan_dir, 1)
        lines.append("```\n")
        return "\n".join(lines)