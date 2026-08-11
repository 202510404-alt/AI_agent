"""
tests/test_file_lock.py
Phase 11: File Lock Manager 단위 테스트
"""

import sys
import time
import tempfile
import unittest
from pathlib import Path

# 프로젝트 루트 경로 추가
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agent_core.execution.file_lock import LocalDiskFileLockManager, LockInfo


class TestFileLockManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name)
        self.lock_manager = LocalDiskFileLockManager(root_dir=self.root_path, lock_dir_name="system_memory/locks")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_acquire_and_release(self):
        file_path = "tools/universal_indexer/indexer.py"
        task1 = "task_01"
        session1 = "session_A"

        # 1. 락 획득 성공
        acquired = self.lock_manager.acquire(file_path, task1, session1)
        self.assertTrue(acquired)

        # 2. get_lock 검증
        lock_info = self.lock_manager.get_lock(file_path)
        self.assertIsNotNone(lock_info)
        self.assertEqual(lock_info.owner_task_id, task1)
        self.assertEqual(lock_info.owner_session_id, session1)

        # 3. 다른 task의 충돌 시도 -> 실패
        acquired_other = self.lock_manager.acquire(file_path, "task_02", "session_B")
        self.assertFalse(acquired_other)

        # 4. 동일 task의 재획득 -> 성공 (re-entrant)
        acquired_same = self.lock_manager.acquire(file_path, task1, session1)
        self.assertTrue(acquired_same)

        # 5. 해제
        self.lock_manager.release(file_path, task1)
        self.assertIsNone(self.lock_manager.get_lock(file_path))

        # 6. 해제 후 다른 task 획득 -> 성공
        acquired_other_after = self.lock_manager.acquire(file_path, "task_02", "session_B")
        self.assertTrue(acquired_other_after)

    def test_sweep_stale_locks(self):
        file_path = "agent_core/plan/planner.py"
        task1 = "task_stale"
        session1 = "session_stale"

        self.lock_manager.acquire(file_path, task1, session1)
        
        # 1. 만료 시간 미도달 시 sweep 안 됨
        swept = self.lock_manager.sweep_stale_locks(max_age_sec=10)
        self.assertEqual(len(swept), 0)
        self.assertIsNotNone(self.lock_manager.get_lock(file_path))

        # 2. 수동으로 acquired_at 조작하여 만료 상태 연출
        lock_info = self.lock_manager.get_lock(file_path)
        lock_file = self.lock_manager._get_lock_file_path(self.lock_manager._normalize_path(file_path))
        stale_info = LockInfo(
            file_path=lock_info.file_path,
            owner_task_id=lock_info.owner_task_id,
            owner_session_id=lock_info.owner_session_id,
            acquired_at=time.time() - 100
        )
        self.lock_manager._write_lock_file(lock_file, stale_info)

        # 3. max_age_sec=10 초로 sweep 실행 -> 정리됨
        swept = self.lock_manager.sweep_stale_locks(max_age_sec=10)
        self.assertEqual(len(swept), 1)
        self.assertEqual(swept[0], self.lock_manager._normalize_path(file_path))
        self.assertIsNone(self.lock_manager.get_lock(file_path))


if __name__ == "__main__":
    unittest.main()
