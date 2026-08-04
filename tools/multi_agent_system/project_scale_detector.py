"""
tools/multi_agent_system/project_scale_detector.py
프로젝트의 규모를 정밀 측정하여 AI 처리 한계 초과 여부를 판단하고,
필요 시 유연한 깊이(depth)의 얕은 폴더 구조(Shallow Tree Map)를 생성합니다.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any, Union

EXCLUDE_KEYWORDS = [
    "node_modules", ".venv", ".git", "__pycache__",
    "cline_tools", "system_memory", "system_maps", "dist", "build"
]

class ProjectScaleDetector:
    def __init__(
        self, 
        project_root: Path,
        max_files: int = 150,           # 감당 가능 최대 파일 수
        max_total_lines: int = 15000,    # 감당 가능 최대 코드 줄 수
        max_estimated_tokens: int = 60000 # 감당 가능 최대 토큰 수
    ):
        self.project_root = Path(project_root).resolve()
        self.max_files = max_files
        self.max_total_lines = max_total_lines
        self.max_estimated_tokens = max_estimated_tokens

    def analyze_project_scale(self, target_dir: Optional[Path] = None) -> Dict[str, Any]:
        """프로젝트 또는 특정 대상 폴더의 규모 수치를 측정합니다."""
        scan_dir = target_dir or self.project_root
        file_count = 0
        total_lines = 0

        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_KEYWORDS]
            if any(kw in root for kw in EXCLUDE_KEYWORDS):
                continue

            for file in files:
                file_count += 1
                file_path = Path(root) / file
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        total_lines += sum(1 for _ in f)
                except Exception:
                    pass

        # 대략적인 토큰 수 산출 (1줄당 평균 8~10 토큰 환산)
        estimated_tokens = total_lines * 9
        is_oversized = (
            file_count > self.max_files or 
            total_lines > self.max_total_lines or 
            estimated_tokens > self.max_estimated_tokens
        )

        return {
            "file_count": file_count,
            "total_lines": total_lines,
            "estimated_tokens": estimated_tokens,
            "is_oversized": is_oversized
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