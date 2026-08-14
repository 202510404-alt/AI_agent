"""
agent_core/debug_agent/collectors
----------------------------------
수집기(Collector) 어댑터패키지
"""

from agent_core.debug_agent.collectors.base import BaseLogCollector
from agent_core.debug_agent.collectors.stdio_collector import StdioCollector
from agent_core.debug_agent.collectors.file_collector import FileCollector

__all__ = ["BaseLogCollector", "StdioCollector", "FileCollector"]
