"""
__all__ = [
    'delete_user',
    'export_user_data',
    'get_user_stats',
    'list_users',
    'register_user',
    'switch_user',
]

语义记忆管理器 - 多用户语义记忆空间管理

从 SomnCore 用户管理方法提取
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class SemanticMemoryManager:
    """多用户语义记忆管理器"""

    def __init__(self, semantic_memory=None):
        """
        Args:
            semantic_memory: 底层语义记忆引擎
        """
        self.semantic_memory = semantic_memory

    def register_user(self, user_id: str) -> bool:
        """
        注册新用户语义记忆空间

        Args:
            user_id: 用户唯一标识

        Returns:
            是否成功
        """
        if not self.semantic_memory:
            return False
        return self.semantic_memory.register_user(user_id)

    def switch_user(self, user_id: str) -> bool:
        """
        切换当前语义记忆用户

        Args:
            user_id: 用户ID

        Returns:
            是否成功
        """
        if not self.semantic_memory:
            return False
        return self.semantic_memory.switch_user(user_id)

    def list_users(self) -> List[Dict[str, Any]]:
        """
        列出所有语义记忆用户

        Returns:
            用户列表
        """
        if not self.semantic_memory:
            return []
        return self.semantic_memory.list_users()

    def export_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        导出用户语义数据(GDPR合规)

        Args:
            user_id: 用户ID

        Returns:
            用户完整语义数据
        """
        if not self.semantic_memory:
            return None
        return self.semantic_memory.export_user_data(user_id)

    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """获取指定用户的统计信息"""
        if not self.semantic_memory:
            return {"enabled": False}
        return self.semantic_memory.get_stats(user_id=user_id)

    def delete_user(self, user_id: str) -> bool:
        """
        删除用户语义记忆空间

        Args:
            user_id: 用户ID

        Returns:
            是否成功
        """
        if not self.semantic_memory:
            return False
        if hasattr(self.semantic_memory, 'delete_user'):
            return self.semantic_memory.delete_user(user_id)
        return False
