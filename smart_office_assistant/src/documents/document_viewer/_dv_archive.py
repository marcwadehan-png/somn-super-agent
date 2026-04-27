"""
__all__ = [
    'extract_archive',
    'extract_from_archive',
    'parse_gzip',
    'parse_tar',
    'parse_zip',
]

压缩包解析模块
"""

import zipfile
import tarfile
import gzip
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from ._dv_types import DocumentContent

def parse_zip(viewer, path: Path, options: Dict) -> DocumentContent:
    """解析ZIP压缩包"""
    content = DocumentContent(metadata=None)
    
    try:
        with zipfile.ZipFile(path, 'r') as zf:
            file_list = []
            total_size = 0
            
            for info in zf.infolist():
                if info.file_size > 0:  # 跳过目录
                    file_list.append({
                        'name': info.filename,
                        'size': info.file_size,
                        'compressed_size': info.compress_size,
                        'date': datetime(*info.date_time).isoformat() if info.date_time else None
                    })
                    total_size += info.file_size
            
            content.attachments = file_list
            content.text_content = _format_archive_list(file_list)
            
    except Exception as e:
        content.warnings.append(f"ZIP解析错误: {e}")
    
    return content

def parse_tar(viewer, path: Path, options: Dict) -> DocumentContent:
    """解析TAR压缩包"""
    content = DocumentContent(metadata=None)
    
    try:
        with tarfile.open(path, 'r:*') as tf:
            file_list = []
            
            for member in tf.getmembers():
                if member.isfile():
                    file_list.append({
                        'name': member.name,
                        'size': member.size,
                        'date': datetime.fromtimestamp(member.mtime).isoformat()
                    })
            
            content.attachments = file_list
            content.text_content = _format_archive_list(file_list)
            
    except Exception as e:
        content.warnings.append(f"TAR解析错误: {e}")
    
    return content

def parse_gzip(viewer, path: Path, options: Dict) -> DocumentContent:
    """解析GZIP文件"""
    content = DocumentContent(metadata=None)
    
    try:
        with gzip.open(path, 'rb') as f:
            data = f.read()
        
        # 尝试解压内容
        try:
            text = data.decode('utf-8')
            content.text_content = f"[GZIP内容预览]\n{text[:10000]}"
        except Exception:
            content.text_content = f"[二进制GZIP文件]\n大小: {len(data)} bytes"
        
        content.attachments = [{
            'name': path.stem,
            'size': len(data),
            'note': 'GZIP内部文件'
        }]
        
    except Exception as e:
        content.warnings.append(f"GZIP解析错误: {e}")
    
    return content

def _format_archive_list(file_list: List[Dict]) -> str:
    """格式化压缩包文件列表"""
    if not file_list:
        return "压缩包为空"
    
    lines = [f"共 {len(file_list)} 个文件:\n"]
    lines.append("-" * 60)
    
    for f in sorted(file_list, key=lambda x: x['name']):
        size = f['size']
        if size < 1024:
            size_str = f"{size}B"
        elif size < 1024 * 1024:
            size_str = f"{size/1024:.1f}KB"
        else:
            size_str = f"{size/1024/1024:.1f}MB"
        
        lines.append(f"  {f['name']:<40} {size_str:>10}")
    
    return "\n".join(lines)

def extract_from_archive(archive_path: Path, member_name: str) -> Optional[bytes]:
    """从压缩包中提取单个文件"""
    try:
        extension = archive_path.suffix.lower()
        
        if extension == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zf:
                return zf.read(member_name)
        elif extension in ['.tar', '.tgz']:
            with tarfile.open(archive_path, 'r:*') as tf:
                member = tf.getmember(member_name)
                f = tf.extractfile(member)
                return f.read() if f else None
                
    except Exception as e:
        from loguru import logger
        logger.error(f"从压缩包提取文件失败: {e}")
    
    return None

def extract_archive(viewer, archive_path: Path, output_dir: Path = None) -> str:
    """解压压缩包到目录"""
    from loguru import logger
    
    path = Path(archive_path)
    
    if output_dir is None:
        output_dir = path.parent / path.stem
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        extension = path.suffix.lower()
        
        if extension == '.zip':
            with zipfile.ZipFile(path, 'r') as zf:
                for member in zf.namelist():
                    member_path = output_dir / member
                    # 防止 Zip Slip：确保解压路径在目标目录内
                    if not member_path.resolve().is_relative_to(output_dir.resolve()):
                        logger.warning(f"跳过危险路径（可能Zip Slip攻击）: {member}")
                        continue
                    if member.endswith('/'):
                        member_path.mkdir(parents=True, exist_ok=True)
                    else:
                        member_path.parent.mkdir(parents=True, exist_ok=True)
                        with zf.open(member) as src, open(member_path, 'wb') as dst:
                            shutil.copyfileobj(src, dst)
        elif extension in ['.tar', '.tgz']:
            with tarfile.open(path, 'r:*') as tf:
                # tarfile.extractall 存在路径遍历风险，改用安全解压
                for member in tf.getmembers():
                    member_path = output_dir / member.name
                    if not member_path.resolve().is_relative_to(output_dir.resolve()):
                        logger.warning(f"跳过危险路径（可能Zip Slip攻击）: {member.name}")
                        continue
                    if member.isdir():
                        member_path.mkdir(parents=True, exist_ok=True)
                    else:
                        member_path.parent.mkdir(parents=True, exist_ok=True)
                        with tf.extractfile(member) as src:
                            if src:
                                with open(member_path, 'wb') as dst:
                                    shutil.copyfileobj(src, dst)
        elif extension == '.gz':
            output_file = output_dir / path.stem
            with gzip.open(path, 'rb') as f_in:
                with open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        
        logger.info(f"已解压到: {output_dir}")
        return str(output_dir)
        
    except Exception as e:
        logger.error(f"解压失败: {e}")
        return ""
