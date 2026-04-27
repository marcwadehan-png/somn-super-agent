# -*- coding: utf-8 -*-
"""
文件数据源连接器 - 监控文件系统变化

功能:
- 目录监控
- 文件变化检测
- 自动增量读取

版本: v1.0.0
"""

from __future__ import annotations
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import hashlib

from ._openclaw_core import DataSourceConnector, DataSourceType, KnowledgeItem

logger = logging.getLogger(__name__)


@dataclass
class FileConfig:
    """文件数据源配置"""
    watch_paths: List[str] = field(default_factory=list)
    extensions: Set[str] = field(default_factory=lambda: {'.txt', '.md', '.pdf', '.docx'})
    ignore_patterns: Set[str] = field(default_factory=lambda: {'__pycache__', '.git', 'node_modules'})
    encoding: str = 'utf-8'


class FileDataSource(DataSourceConnector):
    """文件系统数据源连接器"""
    
    def __init__(self, config: FileConfig):
        super().__init__(DataSourceType.FILE, config.__dict__)
        self.config = config
        self._file_states: Dict[str, datetime] = {}
        self._last_scan: Optional[datetime] = None
    
    async def connect(self) -> bool:
        """建立连接"""
        self.connected = True
        # 初始化扫描
        await self._scan_files()
        return True
    
    async def disconnect(self) -> bool:
        """断开连接"""
        self.connected = False
        return True
    
    async def _scan_files(self) -> Dict[str, datetime]:
        """扫描文件状态"""
        states = {}
        
        for watch_path in self.config.watch_paths:
            path = Path(watch_path)
            if path.exists():
                for f in path.rglob('*'):
                    if f.is_file() and f.suffix in self.config.extensions:
                        # 检查是否忽略
                        if any(ig in str(f) for ig in self.config.ignore_patterns):
                            continue
                        states[str(f)] = datetime.fromtimestamp(f.stat().st_mtime)
        
        self._file_states = states
        self._last_scan = datetime.now()
        return states
    
    async def fetch(self, query: str) -> List[KnowledgeItem]:
        """获取变化的文件"""
        await self._scan_files()
        
        items = []
        
        for path_str, mtime in self._file_states.items():
            path = Path(path_str)
            if path.suffix in ['.txt', '.md']:
                try:
                    with open(path, 'r', encoding=self.config.encoding) as f:
                        content = f.read()
                    
                    if query.lower() in content.lower():
                        items.append(KnowledgeItem(
                            id=f"file_{path.stem}",
                            content=content[:2000],
                            source=str(path),
                            metadata={
                                "mtime": mtime.isoformat(),
                                "size": path.stat().st_size
                            }
                        ))
                except Exception as e:
                    logger.debug(f"文件扫描异常: {e}")
        
        return items
    
    def get_changed_files(self) -> List[str]:
        """获取变更文件列表"""
        changed = []
        for path_str, mtime in self._file_states.items():
            if mtime > (self._last_scan or datetime.min):
                changed.append(path_str)
        return changed


__all__ = ['FileDataSource', 'FileConfig']
