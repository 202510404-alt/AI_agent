"""
agent_core/debug_agent/collectors/base.py
-----------------------------------------
로그 수집기(Collector) 추상 인터페이스
"""

from abc import ABC, abstractmethod
from pathlib import Path
from agent_core.debug_agent.schemas import DebugLogSpec, CapturedLogResult


class BaseLogCollector(ABC):
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir).resolve()

    @abstractmethod
    def collect(
        self,
        spec: DebugLogSpec,
        entrypoint_cmd: str,
        env: dict = None
    ) -> CapturedLogResult:
        """
        주어진 entrypoint_cmd 명령어를 실행하거나 감시하여 로그를 캡처한다.
        """
        pass
