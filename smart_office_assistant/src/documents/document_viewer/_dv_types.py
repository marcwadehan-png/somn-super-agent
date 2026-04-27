"""
__all__ = [
    'size_display',
]

文档查看器类型定义
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

class DocumentType(Enum):
    """文档类型枚举"""
    # Office文档
    PDF = "pdf"
    WORD = "word"          # docx, doc
    EXCEL = "excel"        # xlsx, xls, csv
    POWERPOINT = "powerpoint"  # pptx, ppt
    
    # 文本文件
    TEXT = "text"          # txt, md
    MARKDOWN = "markdown"  # md
    JSON = "json"
    XML = "xml"
    HTML = "html"
    
    # 图片
    IMAGE = "image"        # jpg, png, gif, bmp, webp
    
    # 压缩包
    ZIP = "zip"
    RAR = "rar"
    SEVEN_ZIP = "7z"
    TAR = "tar"
    GZIP = "gz"
    
    # 其他
    RTF = "rtf"
    ODT = "odt"            # LibreOffice文档
    
    UNKNOWN = "unknown"

@dataclass
class DocumentMetadata:
    """文档元数据"""
    file_path: str
    file_name: str
    file_size: int
    file_type: DocumentType
    mime_type: str
    created_time: Optional[datetime] = None
    modified_time: Optional[datetime] = None
    page_count: Optional[int] = None  # PDF/Office页数
    word_count: Optional[int] = None
    encoding: Optional[str] = None
    
    @property
    def size_display(self) -> str:
        """人类可读的文件大小"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"

@dataclass
class DocumentContent:
    """文档内容"""
    metadata: DocumentMetadata
    text_content: str = ""
    pages: List[str] = field(default_factory=list)  # 分页内容
    tables: List[List[List[str]]] = field(default_factory=list)  # 表格数据
    images: List[Dict] = field(default_factory=list)  # 图片列表
    attachments: List[Dict] = field(default_factory=list)  # 附件列表(压缩包内)
    ocr_text: str = ""  # OCRrecognize文字
    warnings: List[str] = field(default_factory=list)  # 警告信息

# 格式到类型的mapping
EXTENSION_MAP = {
    # PDF
    '.pdf': DocumentType.PDF,
    
    # Word
    '.docx': DocumentType.WORD,
    '.doc': DocumentType.WORD,
    
    # Excel
    '.xlsx': DocumentType.EXCEL,
    '.xls': DocumentType.EXCEL,
    '.csv': DocumentType.EXCEL,
    
    # PowerPoint
    '.pptx': DocumentType.POWERPOINT,
    '.ppt': DocumentType.POWERPOINT,
    
    # 文本
    '.txt': DocumentType.TEXT,
    '.md': DocumentType.MARKDOWN,
    '.markdown': DocumentType.MARKDOWN,
    '.json': DocumentType.JSON,
    '.xml': DocumentType.XML,
    '.html': DocumentType.HTML,
    '.htm': DocumentType.HTML,
    '.css': DocumentType.TEXT,
    '.js': DocumentType.TEXT,
    '.ts': DocumentType.TEXT,
    '.py': DocumentType.TEXT,
    '.java': DocumentType.TEXT,
    '.c': DocumentType.TEXT,
    '.cpp': DocumentType.TEXT,
    '.h': DocumentType.TEXT,
    
    # 图片
    '.jpg': DocumentType.IMAGE,
    '.jpeg': DocumentType.IMAGE,
    '.png': DocumentType.IMAGE,
    '.gif': DocumentType.IMAGE,
    '.bmp': DocumentType.IMAGE,
    '.webp': DocumentType.IMAGE,
    '.svg': DocumentType.IMAGE,
    '.ico': DocumentType.IMAGE,
    
    # 压缩包
    '.zip': DocumentType.ZIP,
    '.rar': DocumentType.RAR,
    '.7z': DocumentType.SEVEN_ZIP,
    '.tar': DocumentType.TAR,
    '.gz': DocumentType.GZIP,
    '.tgz': DocumentType.TAR,
    
    # 其他
    '.rtf': DocumentType.RTF,
    '.odt': DocumentType.ODT,
    '.ods': DocumentType.ODT,
    '.odp': DocumentType.ODT,
}

# MIME类型mapping
MIME_MAP = {
    '.pdf': 'application/pdf',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.doc': 'application/msword',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.xls': 'application/vnd.ms-excel',
    '.csv': 'text/csv',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.txt': 'text/plain',
    '.md': 'text/markdown',
    '.json': 'application/json',
    '.xml': 'application/xml',
    '.html': 'text/html',
    '.htm': 'text/html',
    '.zip': 'application/zip',
    '.rar': 'application/x-rar-compressed',
    '.7z': 'application/x-7z-compressed',
    '.tar': 'application/x-tar',
    '.gz': 'application/gzip',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.bmp': 'image/bmp',
    '.webp': 'image/webp',
}
