"""
tests/test_validator_standalone.py
Phase 12: StandaloneExecutionValidator 및 Level 9 Validator 단위 테스트
"""

import sys
import unittest
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agent_core.plan.schemas import Task, DebugLogSpec
from agent_core.execution.standalone_runner import LocalStandaloneExecutionValidator
from agent_core.validation.validator import Validator


class TestValidatorStandalone(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name)

        # 테스트용 샘플 스크립트 작성
        self.sample_script = self.root_path / "sample_app.py"
        with open(self.sample_script, "w", encoding="utf-8") as f:
            f.write('''import os
import sys

print("[DEBUG_LOG][Module] status: active")
print("[DEBUG_LOG][Module] processed count: 42")
print("Process completed successfully.")
''')

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_standalone_execution_and_pattern_matching(self):
        validator = Validator(root_dir=self.root_path)

        task = Task(
            task_id="task_test_01",
            description="Sample Task with Debug Log Spec",
            target_files=["sample_app.py"],
            debug_spec=DebugLogSpec(
                expected_logs=[
                    "[DEBUG_LOG][Module] status: active",
                    "[DEBUG_LOG][Module] processed count: {val}"
                ]
            )
        )

        report = validator.run_all(task, require_predicted_logs=True)
        self.assertTrue(report.is_valid)
        self.assertTrue(report.stages["syntax_import"])
        self.assertTrue(report.stages["standalone_execution"])
        self.assertTrue(report.stages["predicted_logs_match"])
        self.assertEqual(len(report.unmatched_logs), 0)

    def test_standalone_log_mismatch(self):
        validator = Validator(root_dir=self.root_path)

        task = Task(
            task_id="task_test_02",
            description="Sample Task with Invalid Debug Log Spec",
            target_files=["sample_app.py"],
            debug_spec=DebugLogSpec(
                expected_logs=[
                    "[DEBUG_LOG][Module] status: active",
                    "[DEBUG_LOG][Module] NON_EXISTENT_PATTERN"
                ]
            )
        )

        report = validator.run_all(task, require_predicted_logs=True)
        self.assertFalse(report.is_valid)
        self.assertTrue(report.stages["syntax_import"])
        self.assertTrue(report.stages["standalone_execution"])
        self.assertFalse(report.stages["predicted_logs_match"])
        self.assertEqual(len(report.unmatched_logs), 1)
        self.assertEqual(report.unmatched_logs[0], "[DEBUG_LOG][Module] NON_EXISTENT_PATTERN")


if __name__ == "__main__":
    unittest.main()
