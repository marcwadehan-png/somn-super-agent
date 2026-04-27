# -*- coding: utf-8 -*-
"""
增量更新引擎 - 知识差异计算与合并

功能:
- 版本差异计算
- 智能合并策略
- 版本控制

版本: v1.0.0
"""

from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime
from enum import Enum
import hashlib
import json
import os

logger = logging.getLogger(__name__)


class MergeStrategy(Enum):
    """合并策略"""
    NEWER = "newer"      # 保留最新
    OLDER = "older"      # 保留最旧
    MANUAL = "manual"    # 手动处理
    APPEND = "append"     # 追加


class DiffType(Enum):
    """差异类型"""
    ADDED = "added"       # 新增
    MODIFIED = "modified"  # 修改
    DELETED = "deleted"   # 删除
    UNCHANGED = "unchanged" # 未变


@dataclass
class DiffResult:
    """差异结果"""
    diff_type: DiffType
    key: str
    old_value: Any = None
    new_value: Any = None
    confidence: float = 1.0


class DiffEngine:
    """差异计算引擎"""
    
    @staticmethod
    def compute(old: Dict, new: Dict) -> List[DiffResult]:
        """计算两个版本的差异"""
        results = []
        
        all_keys = set(old.keys()) | set(new.keys())
        
        for key in all_keys:
            old_val = old.get(key)
            new_val = new.get(key)
            
            if old_val is None and new_val is not None:
                results.append(DiffResult(DiffType.ADDED, key, new_value=new_val))
            elif old_val is not None and new_val is None:
                results.append(DiffResult(DiffType.DELETED, key, old_value=old_val))
            elif old_val != new_val:
                results.append(DiffResult(DiffType.MODIFIED, key, old_val, new_val))
            else:
                results.append(DiffResult(DiffType.UNCHANGED, key, old_val, new_val))
        
        return results
    
    @staticmethod
    def compute_hash(content: str) -> str:
        """计算内容哈希"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]


class Merger:
    """知识合并引擎"""
    
    def __init__(self, strategy: MergeStrategy = MergeStrategy.NEWER):
        self.strategy = strategy
    
    def merge(self, old: Dict, diffs: List[DiffResult]) -> Dict:
        """应用差异合并"""
        result = old.copy()
        
        for d in diffs:
            if d.diff_type == DiffType.ADDED:
                result[d.key] = d.new_value
            elif d.diff_type == DiffType.MODIFIED:
                result[d.key] = self._resolve_conflict(old.get(d.key), d.new_value)
            elif d.diff_type == DiffType.DELETED:
                if self.strategy == MergeStrategy.NEWER:
                    pass  # 保留旧值
                else:
                    result.pop(d.key, None)
        
        return result
    
    def _resolve_conflict(self, old: Any, new: Any) -> Any:
        """解决冲突"""
        if self.strategy == MergeStrategy.NEWER:
            return new
        elif self.strategy == MergeStrategy.OLDER:
            return old
        elif self.strategy == MergeStrategy.APPEND:
            if isinstance(old, list) and isinstance(new, list):
                return list(set(old + new))
        return new  # 默认保留新的


class VersionControl:
    """版本控制系统（内存+文件持久化）"""
    
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.versions: Dict[str, List[Dict]] = {}
        self.max_versions = 10
        # 尝试从文件加载已有数据
        self._load()
    
    def _storage_file(self) -> str:
        """获取存储文件路径"""
        return os.path.join(self.storage_path, "versions.json")
    
    def _load(self):
        """从文件加载版本数据"""
        try:
            fpath = self._storage_file()
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    self.versions = json.load(f)
        except Exception:
            self.versions = {}
    
    def _save(self):
        """将版本数据持久化到文件"""
        try:
            os.makedirs(self.storage_path, exist_ok=True)
            with open(self._storage_file(), "w", encoding="utf-8") as f:
                # ★ v1.2 修复: 使用 default=str 兜底，防止 ClawMetadata 等非JSON对象导致 TypeError
                json.dump(self.versions, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            logger.error(f"版本数据持久化失败 ({self._storage_file()}): {e}")
    
    def save_version(self, key: str, data: Dict) -> str:
        """保存版本"""
        version_id = DiffEngine.compute_hash(json.dumps(data, sort_keys=True))
        
        if key not in self.versions:
            self.versions[key] = []
        
        version = {
            "id": version_id,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        self.versions[key].append(version)
        
        # 限制版本数量
        if len(self.versions[key]) > self.max_versions:
            self.versions[key] = self.versions[key][-self.max_versions:]
        
        # 持久化
        self._save()
        
        return version_id
    
    def get_versions(self, key: str) -> List[Dict]:
        """获取版本历史"""
        return self.versions.get(key, [])
    
    def rollback(self, key: str, version_id: str) -> Optional[Dict]:
        """回滚到指定版本"""
        for v in self.versions.get(key, []):
            if v['id'] == version_id:
                return v['data']
        return None


__all__ = ['DiffEngine', 'Merger', 'VersionControl', 'MergeStrategy', 'DiffType', 'DiffResult']
