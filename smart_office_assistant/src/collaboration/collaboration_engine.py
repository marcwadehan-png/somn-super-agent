"""
__all__ = [
    'acquire_lock',
    'add_collaborator',
    'apply_change',
    'create_document',
    'detect_conflicts',
    'get_collaboration_stats',
    'get_document',
    'get_document_history',
    'release_lock',
    'remove_collaborator',
    'resolve_conflict',
    'resolve_conflicts',
    'to_dict',
]

协作引擎 - Collaboration Engine
实时协作实现:
"人类命运共同体,协作才能生存"

核心哲学:
1. 实时协作:多人同时编辑,实时同步
2. 冲突解决:智能处理编辑冲突
3. 资源共享:文档,知识,模板共享
4. 版本管理:保留所有版本,可回溯

参考<流浪地球>中的协作:
- 150万人协同运输火石
- 全球联合政府
- "联合起来,我们才有希望"
"""

import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import json
from loguru import logger

class ChangeType(Enum):
    """变更类型"""
    INSERT = "insert"     # 插入
    DELETE = "delete"     # 删除
    REPLACE = "replace"   # 替换
    MOVE = "move"         # 移动

@dataclass
class Change:
    """变更"""
    change_id: str
    document_id: str
    user_id: str
    change_type: ChangeType
    position: int
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'change_id': self.change_id,
            'document_id': self.document_id,
            'user_id': self.user_id,
            'change_type': self.change_type.value,
            'position': self.position,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }

@dataclass
class Document:
    """文档"""
    document_id: str
    title: str
    content: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None
    version: int = 1
    collaborators: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_collaborator(self, user_id: str):
        """添加协作者"""
        if user_id not in self.collaborators:
            self.collaborators.append(user_id)
    
    def remove_collaborator(self, user_id: str):
        """移除协作者"""
        if user_id in self.collaborators:
            self.collaborators.remove(user_id)

@dataclass
class Lock:
    """文档锁"""
    document_id: str
    user_id: str
    acquired_at: datetime
    expires_at: datetime
    section: Optional[str] = None  # 锁定的部分(可选)

class ConflictResolver:
    """冲突解决器"""
    
    def __init__(self):
        self.conflict_resolution_strategies = {
            'last_writes_wins': self._last_writes_wins,
            'first_writes_wins': self._first_writes_wins,
            'manual': self._manual_resolution
        }
        self.default_strategy = 'last_writes_wins'
    
    def resolve_conflict(
        self,
        changes: List[Change],
        strategy: str = None
    ) -> Tuple[List[Change], List[Change]]:
        """
        解决冲突
        
        Args:
            changes: 变更列表(包含冲突的变更)
            strategy: 解决strategy
            
        Returns:
            (应用变更, 丢弃变更)
        """
        strategy = strategy or self.default_strategy
        
        if strategy in self.conflict_resolution_strategies:
            resolver = self.conflict_resolution_strategies[strategy]
            return resolver(changes)
        else:
            logger.warning(f"未知的冲突解决strategy: {strategy}, 使用默认strategy")
            return self._last_writes_wins(changes)
    
    def _last_writes_wins(self, changes: List[Change]) -> Tuple[List[Change], List[Change]]:
        """最后写入者胜出"""
        # 按时间排序,保留最后的变更
        changes_sorted = sorted(changes, key=lambda c: c.timestamp)
        
        if changes_sorted:
            return [changes_sorted[-1]], changes_sorted[:-1]
        
        return [], []
    
    def _first_writes_wins(self, changes: List[Change]) -> Tuple[List[Change], List[Change]]:
        """最先写入者胜出"""
        # 按时间排序,保留最早的变更
        changes_sorted = sorted(changes, key=lambda c: c.timestamp)
        
        if changes_sorted:
            return [changes_sorted[0]], changes_sorted[1:]
        
        return [], []
    
    def _manual_resolution(self, changes: List[Change]) -> Tuple[List[Change], List[Change]]:
        """手动解决(暂不实现)"""
        logger.warning("手动冲突解决暂不实现")
        return [], changes
    
    def detect_conflicts(self, changes: List[Change]) -> List[List[Change]]:
        """
        检测冲突
        
        Args:
            changes: 变更列表
            
        Returns:
            冲突组列表
        """
        # 按文档分组
        changes_by_doc = defaultdict(list)
        for change in changes:
            changes_by_doc[change.document_id].append(change)
        
        conflicts = []
        
        # 检测位置冲突
        for doc_id, doc_changes in changes_by_doc.items():
            # 按位置分组
            changes_by_position = defaultdict(list)
            for change in doc_changes:
                changes_by_position[change.position].append(change)
            
            # 如果同一位置有多个变更,则是冲突
            for position, pos_changes in changes_by_position.items():
                if len(pos_changes) > 1:
                    conflicts.append(pos_changes)
        
        return conflicts

class CollaborationEngine:
    """
    协作引擎
    
    基于<流浪地球>集体主义:
    - 实时协作,同步编辑
    - 智能冲突解决
    - 版本管理
    - 资源共享
    
    功能:
    1. 文档协作 - 多人实时编辑
    2. 变更追踪 - 记录所有变更
    3. 冲突解决 - 智能处理冲突
    4. 版本控制 - 管理文档版本
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # 文档存储
        self.documents: Dict[str, Document] = {}
        
        # 变更历史
        self.change_history: Dict[str, List[Change]] = defaultdict(list)
        
        # 文档锁
        self.document_locks: Dict[str, Lock] = {}
        
        # 冲突解决器
        self.conflict_resolver = ConflictResolver()
        
        # 协作统计
        self.collaboration_stats = defaultdict(lambda: {
            'total_changes': 0,
            'conflicts_resolved': 0,
            'documents_collaborated': set()
        })
        
        logger.info("协作引擎init完成")
    
    def create_document(
        self,
        title: str,
        content: str,
        user_id: str
    ) -> Document:
        """
        创建文档
        
        Args:
            title: 标题
            content: 内容
            user_id: 创建者ID
            
        Returns:
            Document: 创建的文档
        """
        document = Document(
            document_id=str(uuid.uuid4()),
            title=title,
            content=content,
            created_by=user_id
        )
        
        self.documents[document.document_id] = document
        document.add_collaborator(user_id)
        
        logger.info(f"创建文档: {title} (ID: {document.document_id})")
        
        return document
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """
        get文档
        
        Args:
            document_id: 文档ID
            
        Returns:
            Document: 文档,如果不存在则返回None
        """
        return self.documents.get(document_id)
    
    def acquire_lock(
        self,
        document_id: str,
        user_id: str,
        section: Optional[str] = None,
        duration_minutes: int = 30
    ) -> bool:
        """
        get文档锁
        
        Args:
            document_id: 文档ID
            user_id: 用户ID
            section: 锁定的部分
            duration_minutes: 锁定时长(分钟)
            
        Returns:
            是否成功get锁
        """
        document = self.get_document(document_id)
        
        if not document:
            return False
        
        # 检查是否已有锁
        if document_id in self.document_locks:
            existing_lock = self.document_locks[document_id]
            
            # 检查锁是否过期
            if datetime.now() < existing_lock.expires_at:
                # 锁仍然有效
                if existing_lock.user_id != user_id:
                    logger.warning(f"文档已被锁定: {document_id}")
                    return False
        
        # 创建新锁
        lock = Lock(
            document_id=document_id,
            user_id=user_id,
            acquired_at=datetime.now(),
            expires_at=datetime.now() + timedelta(minutes=duration_minutes),
            section=section
        )
        
        self.document_locks[document_id] = lock
        
        logger.info(f"get文档锁: {document_id} (用户: {user_id})")
        
        return True
    
    def release_lock(self, document_id: str, user_id: str) -> bool:
        """
        释放文档锁
        
        Args:
            document_id: 文档ID
            user_id: 用户ID
            
        Returns:
            是否成功释放锁
        """
        if document_id not in self.document_locks:
            return False
        
        lock = self.document_locks[document_id]
        
        if lock.user_id != user_id:
            logger.warning(f"用户无权释放锁: {user_id}")
            return False
        
        del self.document_locks[document_id]
        
        logger.info(f"释放文档锁: {document_id}")
        
        return True
    
    def apply_change(
        self,
        document_id: str,
        user_id: str,
        change_type: ChangeType,
        position: int,
        content: str
    ) -> Tuple[bool, Optional[str]]:
        """
        应用变更
        
        Args:
            document_id: 文档ID
            user_id: 用户ID
            change_type: 变更类型
            position: 位置
            content: 内容
            
        Returns:
            (是否成功, 错误信息)
        """
        document = self.get_document(document_id)
        
        if not document:
            return False, "文档不存在"
        
        # 检查锁
        if document_id in self.document_locks:
            lock = self.document_locks[document_id]
            if lock.user_id != user_id and datetime.now() < lock.expires_at:
                return False, "文档被锁定"
        
        # 创建变更
        change = Change(
            change_id=str(uuid.uuid4()),
            document_id=document_id,
            user_id=user_id,
            change_type=change_type,
            position=position,
            content=content
        )
        
        # 应用变更
        try:
            if change_type == ChangeType.INSERT:
                document.content = document.content[:position] + content + document.content[position:]
            elif change_type == ChangeType.DELETE:
                if position + len(content) <= len(document.content):
                    document.content = document.content[:position] + document.content[position + len(content):]
            elif change_type == ChangeType.REPLACE:
                if position + len(content) <= len(document.content):
                    document.content = document.content[:position] + content + document.content[position + len(content):]
            elif change_type == ChangeType.MOVE:
                # 移动操作暂不实现
                pass
            
            # 更新文档
            document.updated_by = user_id
            document.updated_at = datetime.now()
            document.version += 1
            
            # 记录变更历史
            self.change_history[document_id].append(change)
            
            # 更新统计
            self.collaboration_stats[user_id]['total_changes'] += 1
            self.collaboration_stats[user_id]['documents_collaborated'].add(document_id)
            
            logger.info(f"应用变更: {document_id} (用户: {user_id})")
            
            return True, None
        except Exception as e:
            logger.error(f"应用变更失败: {e}")
            return False, "应用变更失败"
    
    def get_document_history(self, document_id: str, limit: int = 100) -> List[Change]:
        """
        get文档历史
        
        Args:
            document_id: 文档ID
            limit: 限制数量
            
        Returns:
            变更历史
        """
        changes = self.change_history.get(document_id, [])
        return sorted(changes, key=lambda c: c.timestamp, reverse=True)[:limit]
    
    def detect_conflicts(self, document_id: str) -> List[List[Change]]:
        """
        检测文档冲突
        
        Args:
            document_id: 文档ID
            
        Returns:
            冲突组列表
        """
        changes = self.change_history.get(document_id, [])
        
        # 只检测最近1分钟的变更
        recent_changes = [
            c for c in changes
            if datetime.now() - c.timestamp < timedelta(minutes=1)
        ]
        
        return self.conflict_resolver.detect_conflicts(recent_changes)
    
    def resolve_conflicts(
        self,
        document_id: str,
        strategy: str = None
    ) -> Tuple[int, List[List[Change]]]:
        """
        解决文档冲突
        
        Args:
            document_id: 文档ID
            strategy: 解决strategy
            
        Returns:
            (解决的冲突数, 冲突列表)
        """
        conflicts = self.detect_conflicts(document_id)
        
        resolved_count = 0
        
        for conflict_group in conflicts:
            applied, discarded = self.conflict_resolver.resolve_conflict(conflict_group, strategy)
            
            if applied:
                # 应用解决的变更
                for change in applied:
                    self.apply_change(
                        change.document_id,
                        change.user_id,
                        change.change_type,
                        change.position,
                        change.content
                    )
                
                resolved_count += 1
                
                # 更新统计
                for change in conflict_group:
                    self.collaboration_stats[change.user_id]['conflicts_resolved'] += 1
        
        return resolved_count, conflicts
    
    def get_collaboration_stats(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        get协作统计
        
        Args:
            user_id: 用户ID(可选)
            
        Returns:
            统计信息
        """
        if user_id:
            stats = self.collaboration_stats.get(user_id, {})
            return {
                'total_changes': stats.get('total_changes', 0),
                'conflicts_resolved': stats.get('conflicts_resolved', 0),
                'documents_collaborated': len(stats.get('documents_collaborated', set()))
            }
        else:
            # 全局统计
            total_changes = sum(
                stats['total_changes']
                for stats in self.collaboration_stats.values()
            )
            total_conflicts_resolved = sum(
                stats['conflicts_resolved']
                for stats in self.collaboration_stats.values()
            )
            total_collaborators = len(self.collaboration_stats)
            
            return {
                'total_documents': len(self.documents),
                'total_changes': total_changes,
                'total_conflicts_resolved': total_conflicts_resolved,
                'total_collaborators': total_collaborators,
                'avg_changes_per_collaborator': total_changes / total_collaborators if total_collaborators > 0 else 0
            }

# 添加timedelta导入
from datetime import timedelta

# 测试代码
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
