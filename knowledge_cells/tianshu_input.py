# -*- coding: utf-8 -*-
"""
tianshu_input.py v1.0.0（最小版）
======================================
天枢输入层 — 文件/附件识别分析

集成 File Scanner 的有价值内容：
1. 文件扫描（FileScanner、FileInfo）
2. 附件识别（邮件附件、压缩包）

定位：天枢输入层（TianShu Input Layer）
- 处理所有外部输入（文件、URL、附件）
- 作为 TianShu 的输入层，按需调用

Version: 1.0.0
Created: 2026-05-01
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
import mimetypes

logger = logging.getLogger("Somn.TianShuInput")

# ============ 路径设置 ============
_project_root = Path(__file__).resolve().parent.parent
_src_path = _project_root / "smart_office_assistant" / "src"
if str(_src_path) not in sys.path:
    sys.path.append(str(_src_path))

# ============ 类型定义 ============

@dataclass
class FileMetadata:
    """文件元数据（提炼自 file_scanner/scanner.py）"""
    path: str
    name: str
    size: int
    modified_time: float
    created_time: float
    extension: str
    mime_type: str
    category: str  # document, image, video, audio, archive, code, other
    hash: Optional[str] = None
    preview: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "name": self.name,
            "size": self.size,
            "size_human": self._human_readable_size(self.size),
            "modified_time": datetime.fromtimestamp(self.modified_time).isoformat(),
            "created_time": datetime.fromtimestamp(self.created_time).isoformat(),
            "extension": self.extension,
            "mime_type": self.mime_type,
            "category": self.category,
            "preview": self.preview[:100] if self.preview else None,
        }
    
    @staticmethod
    def _human_readable_size(size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

@dataclass
class InputResult:
    """输入结果"""
    input_id: str
    input_type: str  # file, url, email, archive, stream
    metadata: Optional[FileMetadata]
    content: Optional[str] = None
    children: List[FileMetadata] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_id": self.input_id,
            "input_type": self.input_type,
            "metadata": self.metadata.to_dict() if self.metadata else None,
            "content_length": len(self.content) if self.content else 0,
            "children_count": len(self.children),
            "errors": self.errors,
            "created_at": self.created_at,
        }

# ============ 核心类 ============

class TianShuInput:
    """
    天枢输入层 — 文件/附件识别分析
    
    功能：
    1. 文件扫描（识别文件类型、提取元数据）
    2. 附件识别（邮件附件、压缩包）
    3. 内容提取（文本文件、PDF、DOCX 等）
    """
    
    def __init__(self, scan_dir: Optional[str] = None):
        self.scan_dir = Path(scan_dir) if scan_dir else Path.cwd()
        self.scan_history: List[InputResult] = []
        self.logger = logging.getLogger("Somn.TianShuInput")
        
        # 初始化 MIME 类型
        mimetypes.init()
        
        self.logger.info("[TianShuInput] v1.0.0 初始化完成")
    
    def _categorize_file(self, file_path: Path) -> str:
        """分类文件"""
        ext = file_path.suffix.lower()
        
        # 文档
        if ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md']:
            return "document"
        # 图片
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']:
            return "image"
        # 视频
        elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']:
            return "video"
        # 音频
        elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg']:
            return "audio"
        # 压缩包
        elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2']:
            return "archive"
        # 代码
        elif ext in ['.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.go', '.rs']:
            return "code"
        # 数据
        elif ext in ['.csv', '.json', '.xml', '.yaml', '.yml', '.sql']:
            return "data"
        else:
            return "other"
    
    def scan_file(self, file_path: str) -> InputResult:
        """
        扫描单个文件
        
        Args:
            file_path: 文件路径
        
        Returns:
            InputResult 输入结果
        """
        path = Path(file_path)
        
        if not path.exists():
            return InputResult(
                input_id=path.stem,
                input_type="file",
                metadata=None,
                errors=[f"文件不存在: {file_path}"],
            )
        
        metadata = FileMetadata(
            path=str(path),
            name=path.name,
            size=path.stat().st_size,
            modified_time=path.stat().st_mtime,
            created_time=path.stat().st_ctime,
            extension=path.suffix,
            mime_type=mimetypes.guess_type(str(path))[0] or "application/octet-stream",
            category=self._categorize_file(path),
        )
        
        # 提取预览文本（仅文本文件）
        if metadata.category == "document" and metadata.extension in ['.txt', '.md', '.csv', '.json', '.xml', '.yaml', '.yml']:
            try:
                metadata.preview = path.read_text(encoding='utf-8', errors='ignore')[:500]
            except Exception:
                pass
        
        result = InputResult(
            input_id=path.stem,
            input_type="file",
            metadata=metadata,
            content=metadata.preview,
        )
        
        self.scan_history.append(result)
        return result
    
    def scan_directory(self, dir_path: Optional[str] = None, recursive: bool = True) -> List[InputResult]:
        """
        扫描目录
        
        Args:
            dir_path: 目录路径（默认扫描目录）
            recursive: 是否递归扫描
        
        Returns:
            扫描结果列表
        """
        target_dir = Path(dir_path) if dir_path else self.scan_dir
        
        if not target_dir.exists():
            self.logger.error(f"[TianShuInput] 目录不存在: {target_dir}")
            return []
        
        results = []
        
        if recursive:
            for file_path in target_dir.rglob('*'):
                if file_path.is_file():
                    result = self.scan_file(str(file_path))
                    results.append(result)
        else:
            for file_path in target_dir.iterdir():
                if file_path.is_file():
                    result = self.scan_file(str(file_path))
                    results.append(result)
        
        self.logger.info(f"[TianShuInput] 扫描完成: {len(results)} 个文件")
        return results
    
    def analyze_attachment(self, attachment_path: str) -> InputResult:
        """
        分析附件（邮件附件、压缩包等）
        
        Args:
            attachment_path: 附件路径
        
        Returns:
            InputResult 输入结果
        """
        path = Path(attachment_path)
        
        if not path.exists():
            return InputResult(
                input_id=path.stem,
                input_type="email_attachment",
                metadata=None,
                errors=[f"附件不存在: {attachment_path}"],
            )
        
        # 检查是否为压缩包
        if path.suffix.lower() in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return self._analyze_archive(path)
        
        # 普通附件
        return self.scan_file(attachment_path)
    
    def _analyze_archive(self, archive_path: Path) -> InputResult:
        """分析压缩包（简化实现）"""
        metadata = FileMetadata(
            path=str(archive_path),
            name=archive_path.name,
            size=archive_path.stat().st_size,
            modified_time=archive_path.stat().st_mtime,
            created_time=archive_path.stat().st_ctime,
            extension=archive_path.suffix,
            mime_type="application/zip",
            category="archive",
        )
        
        children = []
        
        try:
            import zipfile
            if archive_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    for info in zf.infolist():
                        if not info.is_dir():
                            children.append(FileMetadata(
                                path=info.filename,
                                name=Path(info.filename).name,
                                size=info.file_size,
                                modified_time=0,
                                created_time=0,
                                extension=Path(info.filename).suffix,
                                mime_type=mimetypes.guess_type(info.filename)[0] or "application/octet-stream",
                                category=self._categorize_file(Path(info.filename)),
                            ))
        except Exception as e:
            self.logger.warning(f"[TianShuInput] 分析压缩包失败: {e}")
        
        result = InputResult(
            input_id=archive_path.stem,
            input_type="archive",
            metadata=metadata,
            children=children,
        )
        
        self.scan_history.append(result)
        return result
    
    def get_scan_history(self, limit: int = 10) -> List[InputResult]:
        """获取扫描历史"""
        return self.scan_history[-limit:]
    
    def clear_history(self):
        """清空扫描历史"""
        self.scan_history.clear()
        self.logger.info("[TianShuInput] 扫描历史已清空")

# ============ 接口函数 ============

# 全局单例
_TIANSHU_INPUT: Optional[TianShuInput] = None

def get_tianshu_input() -> TianShuInput:
    """获取 TianShuInput 单例"""
    global _TIANSHU_INPUT
    if _TIANSHU_INPUT is None:
        _TIANSHU_INPUT = TianShuInput()
    return _TIANSHU_INPUT

def scan_file(file_path: str) -> Dict[str, Any]:
    """
    扫描文件（便捷函数）
    
    Args:
        file_path: 文件路径
    
    Returns:
        扫描结果
    """
    tsi = get_tianshu_input()
    result = tsi.scan_file(file_path)
    return result.to_dict()

def scan_directory(dir_path: Optional[str] = None, recursive: bool = True) -> List[Dict[str, Any]]:
    """
    扫描目录（便捷函数）
    
    Args:
        dir_path: 目录路径
        recursive: 是否递归扫描
    
    Returns:
        扫描结果列表
    """
    tsi = get_tianshu_input()
    results = tsi.scan_directory(dir_path, recursive=recursive)
    return [r.to_dict() for r in results]

def analyze_attachment(attachment_path: str) -> Dict[str, Any]:
    """
    分析附件（便捷函数）
    
    Args:
        attachment_path: 附件路径
    
    Returns:
        分析结果
    """
    tsi = get_tianshu_input()
    result = tsi.analyze_attachment(attachment_path)
    return result.to_dict()

# ============ 导出 ============

__version__ = "1.0.0"
__all__ = [
    "TianShuInput",
    "FileMetadata",
    "InputResult",
    "get_tianshu_input",
    "scan_file",
    "scan_directory",
    "analyze_attachment",
]

logger.info(f"[TianShuInput] v{__version__} 加载完成")
