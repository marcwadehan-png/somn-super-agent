"""
__all__ = [
    'calculate_hash',
    'categorize_file',
    'export_report',
    'get_directory_stats',
    'quick_scan',
    'scan_directory',
    'scan_for_duplicates',
    'to_dict',
]

文件扫描器 - 基于 libraries_scanner.js 迁移
功能:扫描目录,分析文件,generate统计报告
"""

import os
import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from collections import defaultdict
import mimetypes
import threading

logger = logging.getLogger(__name__)

@dataclass
class FileInfo:
    """文件信息数据类"""
    path: str
    name: str
    size: int
    modified_time: float
    created_time: float
    extension: str
    mime_type: str
    category: str  # document, image, video, audio, archive, code, other
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ScanReport:
    """扫描报告"""
    scan_path: str
    scan_time: str
    total_files: int
    total_size: int
    categories: Dict[str, Dict[str, Any]]
    duplicates: List[List[str]]
    large_files: List[Dict[str, Any]]
    old_files: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'scan_path': self.scan_path,
            'scan_time': self.scan_time,
            'total_files': self.total_files,
            'total_size': self.total_size,
            'total_size_human': self._human_readable_size(self.total_size),
            'categories': self.categories,
            'duplicates': self.duplicates,
            'large_files': self.large_files,
            'old_files': self.old_files
        }
    
    @staticmethod
    def _human_readable_size(size_bytes: int) -> str:
        """转换为人类可读的大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

class FileScanner:
    """文件扫描器"""
    
    # 文件分类规则
    CATEGORY_RULES = {
        'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv', '.md'],
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
        'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
        'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
        'archive': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
        'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go', '.rs', '.swift', '.kt'],
        'executable': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage']
    }
    
    def __init__(self, progress_callback: Optional[Callable[[int, int], None]] = None):
        self.progress_callback = progress_callback
        self.scanned_files: List[FileInfo] = []
        self.file_hashes: Dict[str, List[str]] = defaultdict(list)
        
    def categorize_file(self, extension: str) -> str:
        """根据扩展名分类文件"""
        ext_lower = extension.lower()
        for category, extensions in self.CATEGORY_RULES.items():
            if ext_lower in extensions:
                return category
        return 'other'
    
    def calculate_hash(self, filepath: str, block_size: int = 65536, timeout: float = 30.0) -> str:
        """计算文件MD5哈希(用于查重)
        
        Args:
            filepath: 文件路径
            block_size: 读取块大小
            timeout: 超时时间(秒),防止大文件卡死
        
        Returns:
            哈希值,超时或出错时返回空字符串
        """
        result = {'hash': '', 'error': None}
        
        def _hash_worker():
            try:
                hasher = hashlib.md5()
                with open(filepath, 'rb') as f:
                    while chunk := f.read(block_size):
                        hasher.update(chunk)
                result['hash'] = hasher.hexdigest()
            except Exception as e:
                result['error'] = e
                logger.warning(f"哈希计算失败 {filepath}: {e}")
        
        # 创建并启动线程
        thread = threading.Thread(target=_hash_worker)
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            logger.warning(f"哈希计算超时: {filepath}")
            return ""
        
        if result['error']:
            return ""
        
        return result['hash']
    
    def scan_directory(self, 
                       path: str,
                       recursive: bool = True,
                       include_hidden: bool = False,
                       file_pattern: Optional[str] = None) -> ScanReport:
        """
        扫描目录
        
        Args:
            path: 要扫描的目录路径
            recursive: 是否递归扫描子目录
            include_hidden: 是否包含隐藏文件
            file_pattern: 文件匹配模式(如 '*.py')
        """
        scan_path = Path(path).resolve()
        if not scan_path.exists():
            raise FileNotFoundError(f"路径不存在: {path}")
        
        self.scanned_files = []
        self.file_hashes = defaultdict(list)
        
        # 收集所有文件
        files_to_scan = []
        if recursive:
            pattern = file_pattern or '*'
            if include_hidden:
                files_to_scan = list(scan_path.rglob(pattern))
            else:
                files_to_scan = [f for f in scan_path.rglob(pattern) 
                               if not any(part.startswith('.') for part in f.parts)]
        else:
            files_to_scan = [f for f in scan_path.iterdir() if f.is_file()]
            if not include_hidden:
                files_to_scan = [f for f in files_to_scan if not f.name.startswith('.')]
        
        # 过滤出文件
        files_to_scan = [f for f in files_to_scan if f.is_file()]
        total_files = len(files_to_scan)
        
        # 扫描每个文件
        for idx, file_path in enumerate(files_to_scan):
            try:
                stat = file_path.stat()
                extension = file_path.suffix
                mime_type, _ = mimetypes.guess_type(str(file_path))
                
                file_info = FileInfo(
                    path=str(file_path),
                    name=file_path.name,
                    size=stat.st_size,
                    modified_time=stat.st_mtime,
                    created_time=stat.st_ctime,
                    extension=extension,
                    mime_type=mime_type or 'application/octet-stream',
                    category=self.categorize_file(extension)
                )
                
                self.scanned_files.append(file_info)
                
                # 计算哈希用于查重(只对小于100MB的文件)
                if stat.st_size < 100 * 1024 * 1024:
                    file_hash = self.calculate_hash(str(file_path))
                    if file_hash:
                        self.file_hashes[file_hash].append(str(file_path))
                
                # 进度回调
                if self.progress_callback:
                    self.progress_callback(idx + 1, total_files)
                    
            except (OSError, PermissionError) as e:
                logger.warning(f"无法访问文件 {file_path}: {e}")
                continue
        
        return self._generate_report(scan_path)
    
    def _generate_report(self, scan_path: Path) -> ScanReport:
        """generate扫描报告"""
        total_size = sum(f.size for f in self.scanned_files)
        
        # 按类别统计
        categories = defaultdict(lambda: {'count': 0, 'size': 0, 'files': []})
        for file_info in self.scanned_files:
            cat = file_info.category
            categories[cat]['count'] += 1
            categories[cat]['size'] += file_info.size
            categories[cat]['files'].append({
                'name': file_info.name,
                'path': file_info.path,
                'size': file_info.size
            })
        
        # 转换为普通dict并添加人类可读的大小
        categories_dict = {}
        for cat, data in categories.items():
            categories_dict[cat] = {
                'count': data['count'],
                'size': data['size'],
                'size_human': self._human_readable_size(data['size']),
                'files': data['files'][:10]  # 只保留前10个文件示例
            }
        
        # 查找重复文件
        duplicates = [paths for paths in self.file_hashes.values() if len(paths) > 1]
        
        # 查找大文件(大于100MB)
        large_files = [
            {
                'path': f.path,
                'name': f.name,
                'size': f.size,
                'size_human': self._human_readable_size(f.size)
            }
            for f in sorted(self.scanned_files, key=lambda x: x.size, reverse=True)
            if f.size > 100 * 1024 * 1024
        ][:20]  # 前20个大文件
        
        # 查找旧文件(超过1年未访问)
        one_year_ago = datetime.now() - timedelta(days=365)
        old_files = [
            {
                'path': f.path,
                'name': f.name,
                'modified_time': datetime.fromtimestamp(f.modified_time).isoformat(),
                'size': f.size,
                'size_human': self._human_readable_size(f.size)
            }
            for f in self.scanned_files
            if datetime.fromtimestamp(f.modified_time) < one_year_ago
        ]
        old_files.sort(key=lambda x: x['modified_time'])
        old_files = old_files[:50]  # 前50个旧文件
        
        return ScanReport(
            scan_path=str(scan_path),
            scan_time=datetime.now().isoformat(),
            total_files=len(self.scanned_files),
            total_size=total_size,
            categories=categories_dict,
            duplicates=duplicates,
            large_files=large_files,
            old_files=old_files
        )
    
    @staticmethod
    def _human_readable_size(size_bytes: int) -> str:
        """转换为人类可读的大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def export_report(self, report: ScanReport, output_path: str, format: str = 'json'):
        """导出扫描报告"""
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'json':
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
        elif format == 'markdown':
            self._export_markdown(report, output)
        
        return output
    
    def _export_markdown(self, report: ScanReport, output: Path):
        """导出为Markdown格式"""
        with open(output, 'w', encoding='utf-8') as f:
            f.write(f"# 文件扫描报告\n\n")
            f.write(f"**扫描路径**: {report.scan_path}\n\n")
            f.write(f"**扫描时间**: {report.scan_time}\n\n")
            f.write(f"**文件总数**: {report.total_files}\n\n")
            f.write(f"**总大小**: {self._human_readable_size(report.total_size)}\n\n")
            
            f.write("## 文件分类统计\n\n")
            f.write("| 类别 | 数量 | 大小 |\n")
            f.write("|------|------|------|\n")
            for cat, data in sorted(report.categories.items(), 
                                   key=lambda x: x[1]['size'], reverse=True):
                f.write(f"| {cat} | {data['count']} | {data['size_human']} |\n")
            
            if report.duplicates:
                f.write(f"\n## 重复文件 ({len(report.duplicates)} 组)\n\n")
                for i, dup_group in enumerate(report.duplicates[:10], 1):
                    f.write(f"### 重复组 {i}\n")
                    for path in dup_group:
                        f.write(f"- {path}\n")
                    f.write("\n")
            
            if report.large_files:
                f.write(f"\n## 大文件 (Top 10)\n\n")
                f.write("| 文件名 | 大小 | 路径 |\n")
                f.write("|--------|------|------|\n")
                for lf in report.large_files[:10]:
                    f.write(f"| {lf['name']} | {lf['size_human']} | {lf['path']} |\n")

# 便捷函数
def quick_scan(path: str, **kwargs) -> ScanReport:
    """快速扫描目录"""
    scanner = FileScanner()
    return scanner.scan_directory(path, **kwargs)

def scan_for_duplicates(path: str) -> List[List[str]]:
    """仅扫描重复文件"""
    scanner = FileScanner()
    report = scanner.scan_directory(path)
    return report.duplicates

def get_directory_stats(path: str) -> Dict[str, Any]:
    """get目录统计信息"""
    scanner = FileScanner()
    report = scanner.scan_directory(path)
    return {
        'total_files': report.total_files,
        'total_size': report.total_size,
        'total_size_human': report.to_dict()['total_size_human'],
        'categories': {k: {'count': v['count'], 'size_human': v['size_human']} 
                      for k, v in report.categories.items()}
    }
