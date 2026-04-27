"""
__all__ = [
    'analyze_for_cleanup',
    'clean_temp_files',
    'execute_cleanup',
    'find_temp_files',
    'preview_cleanup',
    'quick_clean_suggestion',
    'safe_clean',
]

文件清理器 - 智能清理建议和执行
功能:基于扫描结果提供清理建议,安全删除文件
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import sys

@dataclass
class CleanupSuggestion:
    """清理建议"""
    category: str  # duplicate, old_file, temp_file, large_file, empty_folder
    description: str
    files: List[Dict[str, Any]]
    potential_savings: int  # bytes
    risk_level: str  # low, medium, high
    action: str  # delete, move, archive

@dataclass
class CleanupResult:
    """清理结果"""
    success: bool
    message: str
    files_processed: int
    space_freed: int
    errors: List[str]

class FileCleaner:
    """文件清理器"""
    
    # 临时文件模式
    TEMP_PATTERNS = [
        '*.tmp', '*.temp', '~$*',  # 通用临时文件
        '*.log', '*.old', '*.bak', '*.backup',
        'Thumbs.db', '.DS_Store',  # 系统文件
        '*.cache', '*.pyc', '__pycache__',  # Python
        'node_modules', '.npm',  # Node.js
        '.gradle', 'build', 'target',  # 构建目录
    ]
    
    def __init__(self, dry_run: bool = True):
        """
        init清理器
        
        Args:
            dry_run: 如果为True,只模拟执行不实际删除
        """
        self.dry_run = dry_run
        self.deleted_files: List[str] = []
        self.errors: List[str] = []
    
    def _move_to_trash(self, path: Path):
        """
        将文件或目录移动到回收站
        
        Args:
            path: 文件或目录路径
        """
        if sys.platform == 'win32':
            # Windows - 使用PowerShell的Recycle cmdlet
            try:
                import winshell
                winshell.delete_file(str(path))
            except ImportError:
                # 如果没有winshell,使用PowerShell
                subprocess.run(
                    ['powershell', '-Command', f'Remove-Item "{path}" -Recurse -Force'],
                    check=True
                )
        elif sys.platform == 'darwin':
            # macOS
            subprocess.run(['osascript', '-e', f'tell app "Finder" to delete POSIX file "{path}"'], check=True)
        else:
            # Linux - 尝试使用gio trash或trash-cli
            try:
                subprocess.run(['gio', 'trash', str(path)], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    subprocess.run(['trash-put', str(path)], check=True)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # 如果都没有,移动到临时目录
                    trash_dir = Path.home() / '.local/share/Trash/files'
                    trash_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(path), str(trash_dir / path.name))
        
    def analyze_for_cleanup(self, scan_report: Dict[str, Any]) -> List[CleanupSuggestion]:
        """
        分析扫描报告,generate清理建议
        
        Args:
            scan_report: FileScannergenerate的报告字典
        """
        suggestions = []
        
        # 1. 重复文件
        if scan_report.get('duplicates'):
            dup_savings = 0
            dup_files = []
            for dup_group in scan_report['duplicates']:
                # 保留第一个,删除其余的
                for dup_path in dup_group[1:]:
                    try:
                        size = Path(dup_path).stat().st_size
                        dup_savings += size
                        dup_files.append({
                            'path': dup_path,
                            'size': size,
                            'reason': f'重复文件(保留: {dup_group[0]})'
                        })
                    except (OSError, IOError) as e:
                        logger.debug(f"[Cleaner] 获取重复文件信息失败: {e}")

            if dup_files:
                suggestions.append(CleanupSuggestion(
                    category='duplicate',
                    description=f'发现 {len(scan_report["duplicates"])} 组重复文件',
                    files=dup_files,
                    potential_savings=dup_savings,
                    risk_level='low',
                    action='delete'
                ))
        
        # 2. 旧文件(超过2年未修改)
        if scan_report.get('old_files'):
            old_suggestions = []
            old_savings = 0
            two_years_ago = datetime.now() - timedelta(days=730)
            
            for old_file in scan_report['old_files']:
                modified_time = datetime.fromisoformat(old_file['modified_time'])
                if modified_time < two_years_ago:
                    old_suggestions.append({
                        'path': old_file['path'],
                        'size': old_file['size'],
                        'reason': f'超过2年未修改 ({old_file["modified_time"][:10]})'
                    })
                    old_savings += old_file['size']
            
            if old_suggestions:
                suggestions.append(CleanupSuggestion(
                    category='old_file',
                    description=f'发现 {len(old_suggestions)} 个超过2年未修改的文件',
                    files=old_suggestions[:20],  # 只显示前20个
                    potential_savings=old_savings,
                    risk_level='medium',
                    action='archive'
                ))
        
        # 3. 大文件分析
        if scan_report.get('large_files'):
            large_suggestions = []
            large_savings = 0
            
            for large_file in scan_report['large_files'][:10]:
                large_suggestions.append({
                    'path': large_file['path'],
                    'size': large_file['size'],
                    'reason': f'大文件 ({large_file["size_human"]})'
                })
                large_savings += large_file['size']
            
            if large_suggestions:
                suggestions.append(CleanupSuggestion(
                    category='large_file',
                    description=f'发现 {len(scan_report["large_files"])} 个大文件(>100MB)',
                    files=large_suggestions,
                    potential_savings=large_savings,
                    risk_level='high',
                    action='review'
                ))
        
        # 按可释放空间排序
        suggestions.sort(key=lambda x: x.potential_savings, reverse=True)
        return suggestions
    
    def find_temp_files(self, path: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """查找临时文件"""
        temp_files = []
        scan_path = Path(path)
        
        for pattern in self.TEMP_PATTERNS:
            if recursive:
                matches = list(scan_path.rglob(pattern))
            else:
                matches = list(scan_path.glob(pattern))
            
            for match in matches:
                if match.is_file():
                    try:
                        stat = match.stat()
                        temp_files.append({
                            'path': str(match),
                            'size': stat.st_size,
                            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                        })
                    except (OSError, IOError) as e:
                        logger.debug(f"[Cleaner] 获取临时文件信息失败: {e}")
                elif match.is_dir() and pattern in ['node_modules', '__pycache__', '.gradle', 'build', 'target']:
                    # 计算目录大小
                    dir_size = self._get_dir_size(match)
                    temp_files.append({
                        'path': str(match),
                        'size': dir_size,
                        'is_directory': True
                    })
        
        return temp_files
    
    def _get_dir_size(self, path: Path) -> int:
        """get目录大小"""
        total = 0
        try:
            for entry in path.rglob('*'):
                if entry.is_file():
                    total += entry.stat().st_size
        except (OSError, PermissionError) as e:
            logger.debug(f"[Cleaner] 计算目录大小失败: {e}")
        return total
    
    def execute_cleanup(self, 
                       files: List[Dict[str, Any]], 
                       action: str = 'delete',
                       backup_dir: Optional[str] = None,
                       progress_callback: Optional[Callable[[int, int], None]] = None) -> CleanupResult:
        """
        执行清理操作
        
        Args:
            files: 要处理的文件列表
            action: delete(删除到回收站), permanent(永久删除), move(移动)
            backup_dir: 备份目录(action为move时使用)
            progress_callback: 进度回调函数
        """
        if self.dry_run:
            return CleanupResult(
                success=True,
                message=f"[模拟模式] 将处理 {len(files)} 个文件",
                files_processed=0,
                space_freed=0,
                errors=[]
            )
        
        processed = 0
        freed = 0
        errors = []
        
        total = len(files)
        
        for idx, file_info in enumerate(files):
            filepath = file_info.get('path')
            if not filepath:
                continue
            
            try:
                path = Path(filepath)
                if not path.exists():
                    errors.append(f"文件不存在: {filepath}")
                    continue
                
                # get文件大小(用于统计)
                if path.is_file():
                    file_size = path.stat().st_size
                elif path.is_dir():
                    file_size = self._get_dir_size(path)
                else:
                    file_size = 0
                
                # 执行操作
                if action == 'delete':
                    # 移动到回收站(系统原生方式)
                    self._move_to_trash(path)
                        
                elif action == 'permanent':
                    if path.is_file():
                        path.unlink()
                    elif path.is_dir():
                        shutil.rmtree(path)
                        
                elif action == 'move':
                    if backup_dir:
                        backup_path = Path(backup_dir) / path.name
                        shutil.move(str(path), str(backup_path))
                
                processed += 1
                freed += file_size
                self.deleted_files.append(filepath)
                
            except Exception as e:
                errors.append(f"处理失败 {filepath}")
            
            if progress_callback:
                progress_callback(idx + 1, total)
        
        return CleanupResult(
            success=len(errors) == 0,
            message=f"清理完成: 处理 {processed}/{total} 个文件",
            files_processed=processed,
            space_freed=freed,
            errors=errors
        )
    
    def safe_clean(self, 
                   path: str,
                   auto_clean: bool = False,
                   min_age_days: int = 30) -> Dict[str, Any]:
        """
        安全清理模式 - 只清理明显的临时文件
        
        Args:
            path: 要清理的路径
            auto_clean: 是否自动执行(否则只返回建议)
            min_age_days: 最小文件年龄(天)
        """
        results = {
            'temp_files_found': [],
            'action_taken': 'none',
            'files_cleaned': 0,
            'space_freed': 0,
            'errors': []
        }
        
        # 查找临时文件
        temp_files = self.find_temp_files(path)
        
        # 过滤:只处理超过指定天数的文件
        min_age = datetime.now() - timedelta(days=min_age_days)
        old_temp_files = []
        
        for tf in temp_files:
            try:
                modified = datetime.fromisoformat(tf.get('modified', datetime.now().isoformat()))
                if modified < min_age:
                    old_temp_files.append(tf)
            except (OSError, ValueError):
                # 如果无法解析时间,保守起见不包含
                pass
        
        results['temp_files_found'] = old_temp_files
        
        if auto_clean and old_temp_files and not self.dry_run:
            cleanup_result = self.execute_cleanup(old_temp_files, action='delete')
            results['action_taken'] = 'deleted'
            results['files_cleaned'] = cleanup_result.files_processed
            results['space_freed'] = cleanup_result.space_freed
            results['errors'] = cleanup_result.errors
        elif auto_clean:
            results['action_taken'] = 'dry_run'
        
        return results
    
    def preview_cleanup(self, suggestions: List[CleanupSuggestion]) -> str:
        """generate清理预览报告"""
        lines = ["# 清理建议预览\n", f"**模式**: {'模拟运行' if self.dry_run else '实际执行'}\n"]
        
        total_savings = sum(s.potential_savings for s in suggestions)
        lines.append(f"**预计可释放空间**: {self._human_readable_size(total_savings)}\n")
        lines.append(f"**建议数量**: {len(suggestions)} 项\n\n")
        
        for i, suggestion in enumerate(suggestions, 1):
            lines.append(f"## {i}. {suggestion.description}\n")
            lines.append(f"- **类别**: {suggestion.category}\n")
            lines.append(f"- **风险等级**: {suggestion.risk_level}\n")
            lines.append(f"- **建议操作**: {suggestion.action}\n")
            lines.append(f"- **可释放空间**: {self._human_readable_size(suggestion.potential_savings)}\n")
            lines.append(f"- **涉及文件**: {len(suggestion.files)} 个\n\n")
            
            # 显示前5个文件
            for file_info in suggestion.files[:5]:
                lines.append(f"  - {file_info['path']}\n")
                lines.append(f"    原因: {file_info.get('reason', 'N/A')}\n")
            
            if len(suggestion.files) > 5:
                lines.append(f"  ... 还有 {len(suggestion.files) - 5} 个文件\n")
            
            lines.append("\n")
        
        return ''.join(lines)
    
    @staticmethod
    def _human_readable_size(size_bytes: int) -> str:
        """转换为人类可读的大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

# 便捷函数
def quick_clean_suggestion(scan_report: Dict[str, Any]) -> List[CleanupSuggestion]:
    """快速generate清理建议"""
    cleaner = FileCleaner(dry_run=True)
    return cleaner.analyze_for_cleanup(scan_report)

def clean_temp_files(path: str, min_age_days: int = 7) -> Dict[str, Any]:
    """清理临时文件"""
    cleaner = FileCleaner(dry_run=False)
    return cleaner.safe_clean(path, auto_clean=True, min_age_days=min_age_days)
