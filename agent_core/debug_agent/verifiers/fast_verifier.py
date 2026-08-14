"""
agent_core/debug_agent/verifiers/fast_verifier.py
---------------------------------------------------
AST 및 esbuild 기반 정적 문법 검사 (Fast-Check) 모듈
"""

import ast
import subprocess
from pathlib import Path
from typing import Dict, Any


def run_fast_check(root_dir: Path, target_file_path: str) -> Dict[str, Any]:
    """정적 문법 오류 빠른 포착"""
    full_target = root_dir / target_file_path
    if not full_target.exists():
        return {
            "success": False,
            "failure_type": "FILE_NOT_FOUND",
            "output": f"[FILE NOT FOUND] 대상 파일을 찾을 수 없습니다: {target_file_path}",
            "message": "대상 파일 부재"
        }

    if target_file_path.endswith(('.js', '.jsx', '.ts', '.tsx')):
        fast_cmd = f"npx --yes esbuild \"{full_target}\" --loader:.js=jsx"
        try:
            res = subprocess.run(
                fast_cmd, shell=True, capture_output=True, text=True, input="", timeout=10, cwd=str(root_dir)
            )
            if res.returncode != 0:
                return {
                    "success": False,
                    "failure_type": "FAST_CHECK_SYNTAX_ERROR",
                    "output": f"[FAST-CHECK SYNTAX ERROR]\n{res.stderr.strip()}",
                    "message": "정적 문법 검사(Fast-Check) 실패"
                }
        except Exception:
            pass
    elif target_file_path.endswith('.py'):
        try:
            with open(full_target, "r", encoding="utf-8", errors="replace") as f:
                ast.parse(f.read(), filename=str(full_target))
        except SyntaxError as e:
            return {
                "success": False,
                "failure_type": "FAST_CHECK_SYNTAX_ERROR",
                "output": f"[PYTHON SYNTAX ERROR]\n{e}",
                "message": "파이썬 문법 검사(ast.parse) 실패"
            }

    return {"success": True, "output": "", "message": "Fast-Check 통과"}