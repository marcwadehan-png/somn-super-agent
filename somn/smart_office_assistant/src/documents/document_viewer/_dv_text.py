"""
__all__ = [
    'parse_rtf',
    'parse_text',
    'parse_unknown',
]

文本解析模块
"""

import re
from pathlib import Path
from typing import Dict
from ._dv_types import DocumentContent

def parse_text(viewer, path: Path, options: Dict) -> DocumentContent:
    """解析文本文件"""
    encoding = options.get('encoding', 'utf-8')
    
    try:
        with open(path, 'r', encoding=encoding, errors='ignore') as f:
            text = f.read()
        
        content = DocumentContent(metadata=None, text_content=text)
        return content
    except Exception as e:
        from loguru import logger
        logger.warning(f"文本解析失败,尝试其他编码: {e}")
        # 尝试其他编码
        for enc in ['gbk', 'gb2312', 'latin-1']:
            try:
                with open(path, 'r', encoding=enc) as f:
                    text = f.read()
                content = DocumentContent(
                    metadata=None,
                    text_content=text,
                    warnings=[f"使用{enc}编码解析"]
                )
                return content
            except Exception:
                continue
        
        return DocumentContent(metadata=None, warnings=["无法解析文本编码"])

def parse_rtf(viewer, path: Path, options: Dict) -> DocumentContent:
    """解析RTF文档"""
    content = DocumentContent(metadata=None)
    
    try:
        with open(path, 'rb') as f:
            rtf = f.read()
        
        # 简单RTF文本提取
        text = re.sub(r'\\[a-z]+\d*\s?', '', rtf.decode('utf-8', errors='ignore'))
        text = re.sub(r'\{\\[^}]*\}', '', text)
        content.text_content = text
        
    except Exception as e:
        content.warnings.append(f"RTF解析错误: {e}")
    
    return content

def parse_unknown(viewer, path: Path, options: Dict) -> DocumentContent:
    """解析未知格式"""
    return DocumentContent(
        metadata=None,
        warnings=[f"不支持的格式: {path.suffix}"]
    )
