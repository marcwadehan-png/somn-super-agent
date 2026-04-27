"""
文件系统管理器 - File Manager
安全的文件系统访问封装
"""

import os
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
import mimetypes
import json

from loguru import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent, FileDeletedEvent

from src.core.paths import PROJECT_ROOT

@dataclass
class FileInfo:
    """文件信息"""
    path: str
    name: str
    size: int
    modified_time: datetime
    created_time: datetime
    file_type: str
    extension: str
    is_directory: bool
    hash: Optional[str] = None

class FileChangeHandler(FileSystemEventHandler):
    """文件变更处理器"""
    
    def __init__(self, callback: callable):
        self.callback = callback
    
    def on_created(self, event):
        if not event.is_directory:
            self.callback('created', event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            self.callback('modified', event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.callback('deleted', event.src_path)
    
    def on_moved(self, event):
        if not event.is_directory:
            self.callback('moved', event.src_path, event.dest_path)

class FileManager:
    """
    文件系统管理器
    
    功能:
    - 安全的文件读写操作
    - 文件索引和搜索
    - 目录监控
    - 文件类型检测
    - 批量操作
    """
    
    # 允许的文件扩展名
    ALLOWED_EXTENSIONS = {
        '.txt', '.md', '.doc', '.docx', '.pdf',
        '.ppt', '.pptx', '.xls', '.xlsx', '.csv',
        '.json', '.xml', '.html', '.css', '.js',
        '.py', '.java', '.cpp', '.c', '.h',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg',
        '.mp3', '.mp4', '.avi', '.mov', '.wav',
        '.zip', '.rar', '.7z', '.tar', '.gz'
    }
    
    # 最大文件大小 (50MB)
    MAX_FILE_SIZE = 50 * 1024 * 1024
    
    def __init__(self, base_path: Optional[str] = None):
        """
        init文件管理器
        
        Args:
            base_path: 基础工作目录
        """
        self.base_path = Path(base_path) if base_path else PROJECT_ROOT
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # 文件索引
        self.file_index: Dict[str, FileInfo] = {}
        
        # 文件监控
        self.observer: Optional[Observer] = None
        self.watch_handlers: Dict[str, callable] = {}
        
        logger.info(f"文件管理器init,工作目录: {self.base_path}")
    
    def __del__(self):
        """析构时自动停止文件监控"""
        self.stop_watching()
    
    def _is_allowed_path(self, path: Union[str, Path]) -> bool:
        """检查路径是否在允许范围内"""
        try:
            path = Path(path).resolve()
            base = self.base_path.resolve()
            return str(path).startswith(str(base))
        except (OSError, RuntimeError) as e:
            logger.warning(f"路径解析失败: {e}")
            return False
        except Exception as e:
            logger.error(f"意外错误检查路径: {type(e).__name__} - {e}")
            return False
    
    def _is_allowed_file(self, path: Union[str, Path]) -> bool:
        """检查文件类型是否允许"""
        try:
            path = Path(path)
            extension = path.suffix.lower()
            return extension in self.ALLOWED_EXTENSIONS
        except Exception as e:
            logger.warning(f"检查文件类型失败: {e}")
            return False
    
    def _check_file_size(self, path: Union[str, Path]) -> bool:
        """检查文件大小"""
        try:
            size = Path(path).stat().st_size
            return size <= self.MAX_FILE_SIZE
        except (OSError, PermissionError) as e:
            logger.warning(f"无法get文件大小 {path}: {e}")
            return False
        except Exception as e:
            logger.error(f"意外错误检查文件大小: {type(e).__name__} - {e}")
            return False
    
    def get_file_info(self, path: Union[str, Path]) -> Optional[FileInfo]:
        """
        get文件信息
        
        Args:
            path: 文件路径
        
        Returns:
            文件信息对象
        """
        path = Path(path)
        
        if not path.exists():
            return None
        
        stat = path.stat()
        
        return FileInfo(
            path=str(path),
            name=path.name,
            size=stat.st_size,
            modified_time=datetime.fromtimestamp(stat.st_mtime),
            created_time=datetime.fromtimestamp(stat.st_ctime),
            file_type=mimetypes.guess_type(str(path))[0] or 'unknown',
            extension=path.suffix.lower(),
            is_directory=path.is_dir(),
            hash=None
        )
    
    def read_file(
        self,
        path: Union[str, Path],
        encoding: str = 'utf-8',
        binary: bool = False
    ) -> Union[str, bytes, None]:
        """
        读取文件内容
        
        Args:
            path: 文件路径
            encoding: 文本编码
            binary: 是否以二进制模式读取
        
        Returns:
            文件内容
        """
        path = Path(path)
        
        # 安全检查
        if not self._is_allowed_path(path):
            logger.warning(f"尝试访问受限路径: {path}")
            return None
        
        if not path.exists():
            logger.warning(f"文件不存在: {path}")
            return None
        
        if not self._is_allowed_file(path):
            logger.warning(f"不支持的文件类型: {path.suffix}")
            return None
        
        if not self._check_file_size(path):
            logger.warning(f"文件过大: {path}")
            return None
        
        try:
            if binary:
                with open(path, 'rb') as f:
                    return f.read()
            else:
                with open(path, 'r', encoding=encoding, errors='ignore') as f:
                    return f.read()
        except Exception as e:
            logger.error(f"读取文件失败 {path}: {e}")
            return None
    
    def write_file(
        self,
        path: Union[str, Path],
        content: Union[str, bytes],
        encoding: str = 'utf-8',
        binary: bool = False
    ) -> bool:
        """
        写入文件
        
        Args:
            path: 文件路径
            content: 文件内容
            encoding: 文本编码
            binary: 是否以二进制模式写入
        
        Returns:
            是否成功
        """
        path = Path(path)
        
        # 安全检查
        if not self._is_allowed_path(path):
            logger.warning(f"尝试写入受限路径: {path}")
            return False
        
        # 确保目录存在
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if binary:
                with open(path, 'wb') as f:
                    f.write(content)
            else:
                with open(path, 'w', encoding=encoding) as f:
                    f.write(content)
            
            logger.info(f"文件已保存: {path}")
            return True
            
        except Exception as e:
            logger.error(f"写入文件失败 {path}: {e}")
            return False
    
    def list_directory(
        self,
        path: Optional[Union[str, Path]] = None,
        recursive: bool = False,
        include_hidden: bool = False
    ) -> List[FileInfo]:
        """
        列出目录内容
        
        Args:
            path: 目录路径
            recursive: 是否递归
            include_hidden: 是否包含隐藏文件
        
        Returns:
            文件信息列表
        """
        path = Path(path) if path else self.base_path
        
        if not self._is_allowed_path(path):
            logger.warning(f"尝试访问受限路径: {path}")
            return []
        
        if not path.exists() or not path.is_dir():
            return []
        
        results = []
        
        try:
            if recursive:
                for item in path.rglob('*'):
                    if not include_hidden and item.name.startswith('.'):
                        continue
                    info = self.get_file_info(item)
                    if info:
                        results.append(info)
            else:
                for item in path.iterdir():
                    if not include_hidden and item.name.startswith('.'):
                        continue
                    info = self.get_file_info(item)
                    if info:
                        results.append(info)
        except Exception as e:
            logger.error(f"列出目录失败 {path}: {e}")
        
        return results
    
    def create_directory(self, path: Union[str, Path]) -> bool:
        """
        创建目录
        
        Args:
            path: 目录路径
        
        Returns:
            是否成功
        """
        path = Path(path)
        
        if not self._is_allowed_path(path):
            logger.warning(f"尝试在受限路径创建目录: {path}")
            return False
        
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"创建目录失败 {path}: {e}")
            return False
    
    def delete_file(self, path: Union[str, Path]) -> bool:
        """
        删除文件
        
        Args:
            path: 文件路径
        
        Returns:
            是否成功
        """
        path = Path(path)
        
        if not self._is_allowed_path(path):
            logger.warning(f"尝试删除受限路径: {path}")
            return False
        
        try:
            if path.is_file():
                path.unlink()
                logger.info(f"文件已删除: {path}")
            elif path.is_dir():
                shutil.rmtree(path)
                logger.info(f"目录已删除: {path}")
            return True
        except Exception as e:
            logger.error(f"删除失败 {path}: {e}")
            return False
    
    def copy_file(
        self,
        source: Union[str, Path],
        destination: Union[str, Path]
    ) -> bool:
        """
        复制文件
        
        Args:
            source: 源路径
            destination: 目标路径
        
        Returns:
            是否成功
        """
        source = Path(source)
        destination = Path(destination)
        
        if not self._is_allowed_path(source):
            logger.warning(f"源路径受限: {source}")
            return False
        
        if not self._is_allowed_path(destination):
            logger.warning(f"目标路径受限: {destination}")
            return False
        
        try:
            if source.is_file():
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            elif source.is_dir():
                shutil.copytree(source, destination)
            logger.info(f"已复制: {source} -> {destination}")
            return True
        except Exception as e:
            logger.error(f"复制失败: {e}")
            return False
    
    def move_file(
        self,
        source: Union[str, Path],
        destination: Union[str, Path]
    ) -> bool:
        """
        移动文件
        
        Args:
            source: 源路径
            destination: 目标路径
        
        Returns:
            是否成功
        """
        source = Path(source)
        destination = Path(destination)
        
        if not self._is_allowed_path(source) or not self._is_allowed_path(destination):
            logger.warning("路径受限")
            return False
        
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            logger.info(f"已移动: {source} -> {destination}")
            return True
        except Exception as e:
            logger.error(f"移动失败: {e}")
            return False
    
    def search_files(
        self,
        pattern: str,
        path: Optional[Union[str, Path]] = None,
        recursive: bool = True
    ) -> List[FileInfo]:
        """
        搜索文件
        
        Args:
            pattern: 搜索模式(支持通配符)
            path: 搜索路径
            recursive: 是否递归
        
        Returns:
            匹配的文件列表
        """
        import fnmatch
        
        path = Path(path) if path else self.base_path
        
        if not self._is_allowed_path(path):
            return []
        
        results = []
        
        try:
            if recursive:
                for item in path.rglob('*'):
                    if fnmatch.fnmatch(item.name, pattern):
                        info = self.get_file_info(item)
                        if info:
                            results.append(info)
            else:
                for item in path.iterdir():
                    if fnmatch.fnmatch(item.name, pattern):
                        info = self.get_file_info(item)
                        if info:
                            results.append(info)
        except Exception as e:
            logger.error(f"搜索失败: {e}")
        
        return results
    
    def calculate_hash(self, path: Union[str, Path], algorithm: str = 'md5') -> Optional[str]:
        """
        计算文件哈希
        
        Args:
            path: 文件路径
            algorithm: 哈希算法 (md5, sha1, sha256)
        
        Returns:
            哈希值
        """
        path = Path(path)
        
        if not self._is_allowed_path(path) or not path.is_file():
            return None
        
        try:
            hash_obj = hashlib.new(algorithm)
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            logger.error(f"计算哈希失败 {path}: {e}")
            return None
    
    def start_watching(self, path: Union[str, Path], callback: callable):
        """
        开始监控目录
        
        Args:
            path: 监控路径
            callback: 变更回调函数
        """
        path = Path(path)
        
        if not self._is_allowed_path(path):
            logger.warning(f"无法监控受限路径: {path}")
            return
        
        if self.observer is None:
            self.observer = Observer()
        
        handler = FileChangeHandler(callback)
        self.watch_handlers[str(path)] = callback
        
        self.observer.schedule(handler, str(path), recursive=True)
        self.observer.start()
        
        logger.info(f"开始监控目录: {path}")
    
    def stop_watching(self):
        """停止监控"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            logger.info("停止文件监控")
    
    def get_workspace_tree(self) -> Dict[str, Any]:
        """
        get工作区目录树
        
        Returns:
            目录树结构
        """
        def build_tree(path: Path) -> Dict[str, Any]:
            node = {
                'name': path.name,
                'path': str(path),
                'is_directory': path.is_dir(),
                'children': []
            }
            
            if path.is_dir():
                try:
                    for item in sorted(path.iterdir()):
                        if not item.name.startswith('.'):
                            node['children'].append(build_tree(item))
                except (PermissionError, OSError):
                    pass
            
            return node
        
        return build_tree(self.base_path)
    
    def export_tree_to_json(self, output_path: Optional[str] = None) -> str:
        """
        导出目录树为 JSON
        
        Args:
            output_path: 输出路径
        
        Returns:
            JSON 文件路径
        """
        tree = self.get_workspace_tree()
        
        if output_path is None:
            output_path = self.base_path / "workspace_tree.json"
        
        output_path = Path(output_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(tree, f, ensure_ascii=False, indent=2)
        
        return str(output_path)

# 便捷函数
def get_file_manager() -> FileManager:
    """get默认文件管理器实例"""
    return FileManager()

# ───────────────────────────────────────────────────────────────
# 模块导出
# ───────────────────────────────────────────────────────────────
__all__ = [
    'FileInfo',
    'FileChangeHandler',
    'FileManager',
    'get_file_manager',
]
