"""
__all__ = [
    'get_goal',
    'list_goals',
    'make_goal_id',
    'upsert_goal',
]

目标管理器 - 提供长期目标管理能力
"""

import hashlib
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class GoalManager:
    """目标管理器封装类"""

    def __init__(self, somn_core=None):
        """
        Args:
            somn_core: SomnCore实例引用
        """
        self._core = somn_core
        self._stores_dir = Path("data/autonomy/goals") if somn_core is None else None
        if self._stores_dir:
            self._stores_dir.mkdir(parents=True, exist_ok=True)

    def make_goal_id(self, goal_text: str) -> str:
        """
        基于目标文本生成稳定 goal_id

        Args:
            goal_text: 目标文本

        Returns:
            稳定的goal_id
        """
        return hashlib.md5(goal_text.encode()).hexdigest()[:16]

    def upsert_goal(self, goal_text: str, requirement: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        创建或更新长期目标

        Args:
            goal_text: 目标文本
            requirement: 需求分析结果

        Returns:
            目标记录
        """
        goal_id = self.make_goal_id(goal_text)

        record = {
            "goal_id": goal_id,
            "goal_text": goal_text,
            "created_at": self._get_timestamp(),
            "last_accessed": self._get_timestamp(),
            "requirement_summary": requirement.get("summary", "")[:200],
            "status": "active",
        }

        try:
            self._write_json_store(f"goal_{goal_id}.json", record)
            return record
        except Exception as e:
            logger.warning(f"保存目标失败: {e}")
            return None

    def get_goal(self, goal_id: str) -> Optional[Dict[str, Any]]:
        """
        获取目标记录

        Args:
            goal_id: 目标ID

        Returns:
            目标记录或None
        """
        try:
            return self._read_json_store(f"goal_{goal_id}.json")
        except Exception:
            return None

    def list_goals(self) -> list:
        """列出所有目标"""
        if not self._stores_dir:
            return []
        try:
            return [
                f.stem.replace("goal_", "")
                for f in self._stores_dir.glob("goal_*.json")
            ]
        except Exception:
            return []

    def _read_json_store(self, filename: str) -> Optional[Dict[str, Any]]:
        """读取本地 JSON 存储"""
        if not self._stores_dir:
            return None
        filepath = self._stores_dir / filename
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def _write_json_store(self, filename: str, data: Dict[str, Any]):
        """写入本地 JSON 存储"""
        if not self._stores_dir:
            return
        filepath = self._stores_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _get_timestamp() -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
