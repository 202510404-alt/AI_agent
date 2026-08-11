"""
agent_core/execution/file_lock.py
Level 4 Manager Layer 확장: 파일 단위 락(Lock) 안전구조
- 동일 파일에 대한 동시 쓰기를 원천 차단하여 멀티 작업/멀티 세션 충돌 방지
- system_memory/locks/ 디렉토리에 JSON 형태 영속화
"""

import os
import json
import time
import hashlib
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, List, Dict, Any


@dataclass(frozen=True)
class LockInfo:
    file_path: str          # [📂 실제경로] 규격
    owner_task_id: str
    owner_session_id: str   # 어느 터미널 세션이 잡았는지 (§3.7 연동)
    acquired_at: float      # UNIX timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "owner_task_id": self.owner_task_id,
            "owner_session_id": self.owner_session_id,
            "acquired_at": self.acquired_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LockInfo":
        return cls(
            file_path=data["file_path"],
            owner_task_id=data["owner_task_id"],
            owner_session_id=data["owner_session_id"],
            acquired_at=float(data["acquired_at"]),
        )


class FileLockManager(ABC):
    @abstractmethod
    def acquire(self, file_path: str, task_id: str, session_id: str) -> bool:
        """락 획득 시도. 이미 잠겨 있으면 False를 즉시 반환한다."""
        raise NotImplementedError

    @abstractmethod
    def release(self, file_path: str, task_id: str) -> None:
        """락 해제"""
        raise NotImplementedError

    @abstractmethod
    def get_lock(self, file_path: str) -> Optional[LockInfo]:
        """특정 파일의 현재 락 정보 조회"""
        raise NotImplementedError

    @abstractmethod
    def sweep_stale_locks(self, max_age_sec: int) -> List[str]:
        """비정상 종료로 반환되지 않은 락 정리. 반환값: 정리된 file_path 목록"""
        raise NotImplementedError


class LocalDiskFileLockManager(FileLockManager):
    """
    디스크 파일(system_memory/locks/*.lock) 기반 영속 FileLockManager 구현체.
    프로세스 재시작 및 동시성 제어 지원.
    """
    def __init__(self, root_dir: Optional[Path] = None, lock_dir_name: str = "system_memory/locks"):
        if root_dir is None:
            root_dir = Path(__file__).resolve().parent.parent.parent
        self.root_dir = Path(root_dir).resolve()
        self.lock_dir = self.root_dir / lock_dir_name
        self.lock_dir.mkdir(parents=True, exist_ok=True)
        self._thread_lock = threading.Lock()

    def _normalize_path(self, file_path: str) -> str:
        """경로 표준화 (윈도우/리눅스 슬래시 통일 및 상대경로 정규화)"""
        p = Path(file_path)
        if p.is_absolute():
            try:
                p = p.relative_to(self.root_dir)
            except ValueError:
                pass
        return str(p).replace("\\", "/")

    def _get_lock_file_path(self, norm_file_path: str) -> Path:
        """파일 경로별 안전한 락파일명 생성 (SHA256 해시 사용)"""
        path_hash = hashlib.sha256(norm_file_path.encode("utf-8")).hexdigest()[:16]
        safe_name = norm_file_path.replace("/", "_").replace("\\", "_").replace(":", "_")
        if len(safe_name) > 50:
            safe_name = safe_name[:50]
        return self.lock_dir / f"{safe_name}_{path_hash}.lock"

    def acquire(self, file_path: str, task_id: str, session_id: str) -> bool:
        norm_path = self._normalize_path(file_path)
        lock_file = self._get_lock_file_path(norm_path)

        with self._thread_lock:
            existing = self._read_lock_file(lock_file)
            if existing is not None:
                # 동일 task_id가 재획득하는 경우는 허용
                if existing.owner_task_id == task_id:
                    return True
                return False

            # 락 파일 생성
            info = LockInfo(
                file_path=norm_path,
                owner_task_id=task_id,
                owner_session_id=session_id,
                acquired_at=time.time()
            )
            self._write_lock_file(lock_file, info)
            return True

    def release(self, file_path: str, task_id: str) -> None:
        norm_path = self._normalize_path(file_path)
        lock_file = self._get_lock_file_path(norm_path)

        with self._thread_lock:
            existing = self._read_lock_file(lock_file)
            if existing is not None and existing.owner_task_id == task_id:
                if lock_file.exists():
                    try:
                        lock_file.unlink()
                    except OSError:
                        pass

    def get_lock(self, file_path: str) -> Optional[LockInfo]:
        norm_path = self._normalize_path(file_path)
        lock_file = self._get_lock_file_path(norm_path)

        with self._thread_lock:
            return self._read_lock_file(lock_file)

    def sweep_stale_locks(self, max_age_sec: int) -> List[str]:
        now = time.time()
        swept_paths: List[str] = []

        with self._thread_lock:
            for lock_file in self.lock_dir.glob("*.lock"):
                info = self._read_lock_file(lock_file)
                if info is not None:
                    if (now - info.acquired_at) > max_age_sec:
                        try:
                            lock_file.unlink()
                            swept_paths.append(info.file_path)
                        except OSError:
                            pass
        return swept_paths

    def _read_lock_file(self, lock_file: Path) -> Optional[LockInfo]:
        if not lock_file.exists():
            return None
        try:
            with open(lock_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return LockInfo.from_dict(data)
        except Exception:
            return None

    def _write_lock_file(self, lock_file: Path, info: LockInfo) -> None:
        temp_file = lock_file.with_suffix(".tmp")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(info.to_dict(), f, ensure_ascii=False, indent=2)
            temp_file.replace(lock_file)
        except Exception:
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except OSError:
                    pass
            raise


# 기본 기본 구현체 앨리어스
DefaultFileLockManager = LocalDiskFileLockManager
