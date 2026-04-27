# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_cleanup',
    'execute_cleanup',
    'find_large_files',
    'scan_directory',
]

文件操作模块 - FileOperations
负责文件扫描、清理、分析等操作
"""
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)
class FileScanner:
    """
    文件扫描器

    职责：
    1. 目录扫描
    2. 文件统计
    3. 大文件/临时文件识别
    """

    # 临时文件扩展名
    TEMP_EXTENSIONS = {
        '.tmp', '.temp', '.bak', '.old', '.log',
        '.cache', '.swp', '.swo', '~'
    }

    def __init__(self):
        self._scan_cache: Dict[str, Any] = {}

    def scan_directory(self, path: str, recursive: bool = True,
                       include_hidden: bool = False) -> Dict[str, Any]:
        """
        扫描目录

        Args:
            path: 目录路径
            recursive: 是否递归
            include_hidden: 是否包含隐藏文件

        Returns:
            扫描结果
        """
        result = {
            'path': path,
            'timestamp': time.time(),
            'files': [],
            'total_count': 0,
            'total_size': 0,
            'extensions': {},
            'temp_files': [],
        }

        try:
            p = Path(path)
            if not p.exists() or not p.is_dir():
                return {'error': 'Invalid directory', 'path': path}

            for item in p.rglob('*') if recursive else p.iterdir():
                if not include_hidden and item.name.startswith('.'):
                    continue
                if not item.is_file():
                    continue

                try:
                    size = item.stat().st_size
                    ext = item.suffix.lower()

                    result['files'].append({
                        'path': str(item),
                        'name': item.name,
                        'size': size,
                        'extension': ext,
                        'modified': item.stat().st_mtime,
                    })
                    result['total_count'] += 1
                    result['total_size'] += size

                    # 统计扩展名
                    if ext:
                        result['extensions'][ext] = result['extensions'].get(ext, 0) + 1

                    # 检测临时文件
                    if self._is_temp_file(item.name):
                        result['temp_files'].append(str(item))

                except Exception as e:
                    logger.debug(f"目录扫描失败: {e}")

        except Exception as e:
            logger.error(f"文件操作失败 ({path}): {e}")
            return {'error': '文件操作失败', 'path': path}

        return result

    def _is_temp_file(self, filename: str) -> bool:
        """判断是否为临时文件"""
        name_lower = filename.lower()

        # 检查扩展名
        for ext in self.TEMP_EXTENSIONS:
            if filename.endswith(ext) or name_lower.endswith(ext):
                return True

        # 检查前缀/后缀
        if filename.startswith('~') or filename.startswith('.'):
            return True

        return False

    def find_large_files(self, path: str, min_size_mb: int = 10,
                        recursive: bool = True) -> List[Dict[str, Any]]:
        """
        查找大文件

        Args:
            path: 目录路径
            min_size_mb: 最小文件大小(MB)
            recursive: 是否递归

        Returns:
            大文件列表
        """
        min_bytes = min_size_mb * 1024 * 1024
        large_files = []

        try:
            p = Path(path)
            if not p.exists():
                return []

            pattern = p.rglob('*') if recursive else p.iterdir()

            for item in pattern:
                if not item.is_file():
                    continue
                try:
                    size = item.stat().st_size
                    if size >= min_bytes:
                        large_files.append({
                            'path': str(item),
                            'name': item.name,
                            'size': size,
                            'size_mb': round(size / (1024 * 1024), 2),
                            'extension': item.suffix,
                        })
                except Exception as e:
                    logger.debug(f"文件操作失败: {e}")

        except Exception as e:
                logger.debug(f"文件操作失败: {e}")

        # 按大小排序
        large_files.sort(key=lambda x: x['size'], reverse=True)
        return large_files

class FileCleaner:
    """
    文件清理器

    职责：
    1. 分析清理建议
    2. 执行清理操作
    3. 生成清理报告
    """

    def __init__(self):
        pass

    def analyze_cleanup(self, scan_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析清理建议

        Args:
            scan_result: 扫描结果

        Returns:
            清理建议
        """
        suggestions = []
        total_cleanable = 0

        # 临时文件建议
        temp_files = scan_result.get('temp_files', [])
        if temp_files:
            temp_size = sum(
                f.get('size', 0) for f in scan_result.get('files', [])
                if f['path'] in temp_files
            )
            suggestions.append({
                'type': 'temp_files',
                'description': '临时文件清理',
                'count': len(temp_files),
                'size': temp_size,
                'files': temp_files[:20],  # 只显示前20个
            })
            total_cleanable += temp_size

        return {
            'suggestions': suggestions,
            'total_cleanable_size': total_cleanable,
            'total_files': scan_result.get('total_count', 0),
        }

    def execute_cleanup(self, files_to_delete: List[str],
                       dry_run: bool = True) -> Dict[str, Any]:
        """
        执行清理

        Args:
            files_to_delete: 要删除的文件列表
            dry_run: 试运行模式（不实际删除）

        Returns:
            清理结果
        """
        deleted = []
        failed = []
        freed_space = 0

        for file_path in files_to_delete:
            try:
                p = Path(file_path)
                if not p.exists():
                    continue

                size = p.stat().st_size if p.is_file() else 0

                if not dry_run:
                    p.unlink()

                deleted.append(file_path)
                freed_space += size

            except Exception as e:
                failed.append({'file': file_path, 'error': '文件操作失败'})

        return {
            'deleted_count': len(deleted),
            'failed_count': len(failed),
            'freed_space_bytes': freed_space,
            'freed_space_mb': round(freed_space / (1024 * 1024), 2),
            'dry_run': dry_run,
            'failed': failed,
        }
