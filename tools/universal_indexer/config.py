# tools/universal_indexer/config.py
import sys
from pathlib import Path

# =====================================================================
# 📌 1. PROJECT ROOT RESOLUTION
# =====================================================================
def get_project_root() -> Path:
    """
    현재 파일의 위치를 기준으로 프로젝트의 마스터 루트 디렉토리를 역추적하여 반환합니다.
    `tools/universal_indexer` 구조 내부 또는 루트에 위치한 경우 모두 대응합니다.
    """
    script_dir = Path(__file__).parent.resolve()
    if script_dir.name == "universal_indexer" and script_dir.parent.name == "tools":
        return script_dir.parent.parent
    return script_dir

PROJECT_ROOT = get_project_root()

# =====================================================================
# 🎛️ 2. SCAN MODE INTERFACE
# =====================================================================
def get_scan_mode() -> str:
    """switch.py의 SCAN_MODE 상태를 동적으로 확인합니다."""
    try:
        from switch import SCAN_MODE
        return SCAN_MODE
    except ImportError:
        try:
            from tools.universal_indexer.switch import SCAN_MODE
            return SCAN_MODE
        except ImportError:
            return "ROOT"

# =====================================================================
# 🛡️ 3. CENTRALIZED EXCLUSION & PATH CONFIG
# =====================================================================
EXCLUDE_KEYWORDS = [
    "node_modules",
    ".venv",
    ".git",
    "__pycache__",
    "cline_tools",
    "system_memory",
    "system_maps",
    "dist",
    "build",
    ".jjap_context.json",
    ".jjap_symbols.json"
]

EXCLUDE_EXTENSIONS = [
    ".md",
    ".txt",
    ".pyc"
]

# 💡 AST 분석 시 등록 대상 클래스 추적 키워드 (하드코딩 제거)
REGISTRY_KEYWORDS = [
    "entity", "platform", "camera", "sensor", "agent", 
    "navigator", "indexer", "retriever", "handler", "service", "controller"
]

# 💡 파서 노드 매핑 및 확장자 별 언어 매핑
LANG_MAP = {
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".py": "python",
    ".go": "go",
    ".rs": "rust",
    ".c": "c",
    ".cpp": "cpp",
    ".java": "java"
}

# 디렉토리 경로 정의
SYSTEM_MEMORY_DIR = PROJECT_ROOT / "system_memory"
SYSTEM_MAPS_DIR = PROJECT_ROOT / "system_maps"

# 주요 장부 파일 경로
CONTEXT_JSON_PATH = SYSTEM_MEMORY_DIR / ".jjap_context.json"
SYMBOLS_JSON_PATH = SYSTEM_MEMORY_DIR / ".jjap_symbols.json"
DEFINITION_MAP_PATH = SYSTEM_MEMORY_DIR / "definition_map.json"
REGISTRY_JSON_PATH = SYSTEM_MEMORY_DIR / "registry_constants.json"
PROTOCOL_JSON_PATH = SYSTEM_MEMORY_DIR / "data_protocols.json"
AI_MAP_MD_PATH = SYSTEM_MAPS_DIR / "AI_CODEBASE_MAP.md"
CODEBASE_MAP_MD_PATH = SYSTEM_MAPS_DIR / "CODEBASE_MAP.md"