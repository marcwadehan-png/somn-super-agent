"""
通用文档查看器 - Universal Document Viewer
支持打开,查看,阅读主流文档格式

支持格式:
- PDF: .pdf (文本PDF + 图片扫描PDF/OCR)
- Word: .docx, .doc
- Excel: .xlsx, .xls, .csv
- PowerPoint: .pptx, .ppt
- 文本: .txt, .md, .json, .xml, .html, .css, .js
- 图片: .jpg, .jpeg, .png, .gif, .bmp, .webp (支持OCR)
- 压缩包: .zip, .rar, .7z, .tar, .gz (支持解压查看)
- 其他: .rtf, .odt, .ods, .odp

版本: v1.0 -> v1.0 (模块化拆分)
日期: 2026-04-08
"""

__all__ = [
    'detect_type',
    'extract_archive',
    'extract_from_archive',
    'extract_text_from_pdf',
    'get_document_info',
    'get_metadata',
    'get_summary',
    'list_archive_contents',
    'ocr_image',
    'read',
    'view_document',
]

import os
import io
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

from loguru import logger

# 子模块导入
from ._dv_types import (
    DocumentType, DocumentMetadata, DocumentContent,
    EXTENSION_MAP, MIME_MAP
)
from . import _dv_pdf as pdf_parser
from . import _dv_office as office_parser
from . import _dv_image as image_parser
from . import _dv_archive as archive_parser
from . import _dv_text as text_parser

class DocumentViewer:
    """
    通用文档查看器
    支持多种文档格式的内容提取和解析
    """
    
    def __init__(self, enable_ocr: bool = True, ocr_languages: List[str] = None):
        """
        初始化文档查看器
        
        Args:
            enable_ocr: 是否启用OCR功能
            ocr_languages: OCR语言列表,默认['chi_sim', 'eng']
        """
        self.enable_ocr = enable_ocr
        self.ocr_languages = ocr_languages or ['chi_sim', 'eng']
        self._ocr_engine = None
        
        # 缓存已解析的压缩包内容
        self._archive_cache: Dict[str, List[Dict]] = {}
    
    def _get_ocr_engine(self):
        """获取OCR引擎(延迟加载) - 支持多种OCR方案"""
        if self._ocr_engine is None and self.enable_ocr:
            # 方案1: Tesseract OCR (需要安装Tesseract引擎)
            try:
                import pytesseract
                from PIL import Image
                # 验证tesseract是否可用
                pytesseract.get_tesseract_version()
                self._ocr_engine = {'type': 'tesseract', 'pytesseract': pytesseract, 'PIL': Image}
                logger.info("OCR引擎已加载: Tesseract " + str(pytesseract.get_tesseract_version()))
                return self._ocr_engine
            except ImportError:
                logger.debug("pytesseract Python包未安装")
            except Exception as e:
                logger.warning(f"Tesseract引擎未安装: {e}")
            
            # 所有方案都不可用
            self._ocr_engine = {'type': None}
            self._show_ocr_installation_guide()
            self.enable_ocr = False
        return self._ocr_engine
    
    def _show_ocr_installation_guide(self):
        """显示OCR安装指引"""
        logger.warning("=" * 60)
        logger.warning("OCR功能需要安装Tesseract OCR引擎")
        logger.warning("=" * 60)
        logger.warning("安装步骤:")
        logger.warning("1. 下载: https://github.com/UB-Mannheim/tesseract/releases")
        logger.warning("   下载: tesseract-ocr-w64-setup-5.5.0.20241111.exe")
        logger.warning("2. 运行安装程序")
        logger.warning("3. 安装时勾选: 中文简体语言包 (chi_sim)")
        logger.warning("4. 安装完成后重启终端")
        logger.warning("=" * 60)
    
    def detect_type(self, file_path: Union[str, Path]) -> DocumentType:
        """检测文件类型"""
        path = Path(file_path)
        extension = path.suffix.lower()
        return EXTENSION_MAP.get(extension, DocumentType.UNKNOWN)
    
    def get_metadata(self, file_path: Union[str, Path]) -> Optional[DocumentMetadata]:
        """获取文档元数据"""
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"文件不存在: {path}")
            return None
        
        try:
            stat = path.stat()
            extension = path.suffix.lower()
            doc_type = EXTENSION_MAP.get(extension, DocumentType.UNKNOWN)
            mime_type = MIME_MAP.get(extension, 'application/octet-stream')
            
            metadata = DocumentMetadata(
                file_path=str(path.absolute()),
                file_name=path.name,
                file_size=stat.st_size,
                file_type=doc_type,
                mime_type=mime_type,
                created_time=datetime.fromtimestamp(stat.st_ctime),
                modified_time=datetime.fromtimestamp(stat.st_mtime),
            )
            
            # 尝试获取页数
            if doc_type == DocumentType.PDF:
                metadata.page_count = pdf_parser.get_pdf_page_count(path)
            
            return metadata
            
        except Exception as e:
            logger.error(f"获取元数据失败: {e}")
            return None
    
    def read(self, file_path: Union[str, Path], options: Dict = None) -> Optional[DocumentContent]:
        """
        读取文档内容
        
        Args:
            file_path: 文件路径
            options: 读取选项
        
        Returns:
            DocumentContent对象
        """
        path = Path(file_path)
        options = options or {}
        
        if not path.exists():
            logger.error(f"文件不存在: {path}")
            return None
        
        metadata = self.get_metadata(path)
        if not metadata:
            return None
        
        # 根据类型选择解析方法
        parse_method = {
            DocumentType.PDF: pdf_parser.parse_pdf,
            DocumentType.WORD: office_parser.parse_word,
            DocumentType.EXCEL: office_parser.parse_excel,
            DocumentType.POWERPOINT: office_parser.parse_powerpoint,
            DocumentType.TEXT: text_parser.parse_text,
            DocumentType.MARKDOWN: text_parser.parse_text,
            DocumentType.JSON: text_parser.parse_text,
            DocumentType.XML: text_parser.parse_text,
            DocumentType.HTML: text_parser.parse_text,
            DocumentType.IMAGE: image_parser.parse_image,
            DocumentType.ZIP: archive_parser.parse_zip,
            DocumentType.TAR: archive_parser.parse_tar,
            DocumentType.GZIP: archive_parser.parse_gzip,
            DocumentType.RTF: text_parser.parse_rtf,
        }.get(metadata.file_type, text_parser.parse_unknown)
        
        try:
            content = parse_method(self, path, options)
            if content:
                content.metadata = metadata
                return content
        except Exception as e:
            logger.error(f"解析文档失败: {e}")
            return DocumentContent(
                metadata=metadata,
                warnings=["解析失败"]
            )
        
        return None
    
    def extract_from_archive(self, archive_path: Union[str, Path], 
                            member_name: str) -> Optional[bytes]:
        """从压缩包中提取单个文件"""
        return archive_parser.extract_from_archive(Path(archive_path), member_name)
    
    def list_archive_contents(self, archive_path: Union[str, Path]) -> List[Dict]:
        """列出压缩包内容"""
        path = Path(archive_path)
        
        if str(path) in self._archive_cache:
            return self._archive_cache[str(path)]
        
        content = self.read(path)
        if content:
            self._archive_cache[str(path)] = content.attachments
            return content.attachments
        
        return []
    
    def extract_archive(self, archive_path: Union[str, Path], 
                       output_dir: Union[str, Path] = None) -> str:
        """解压压缩包到目录"""
        return archive_parser.extract_archive(self, Path(archive_path), Path(output_dir) if output_dir else None)
    
    def get_summary(self, content: DocumentContent, max_length: int = 2000) -> str:
        """获取文档摘要"""
        lines = []
        
        # 元数据
        m = content.metadata
        if m:
            lines.append(f"文件: {m.file_name}")
            lines.append(f"类型: {m.file_type.value}")
            lines.append(f"大小: {m.size_display}")
            if m.page_count:
                lines.append(f"页数: {m.page_count}")
            lines.append("")
        
        # 文本内容
        if content.text_content:
            text = content.text_content.strip()
            if len(text) > max_length:
                text = text[:max_length] + "..."
            lines.append("内容预览:")
            lines.append(text)
        
        # OCR内容
        elif content.ocr_text:
            text = content.ocr_text.strip()
            if len(text) > max_length:
                text = text[:max_length] + "..."
            lines.append("OCR识别内容:")
            lines.append(text)
        
        # 表格数量
        if content.tables:
            lines.append(f"\n表格数: {len(content.tables)}")
        
        # 图片数量
        if content.images:
            lines.append(f"图片数: {len(content.images)}")
        
        # 压缩包文件数
        if content.attachments:
            lines.append(f"压缩包内文件: {len(content.attachments)}")
        
        # 警告
        if content.warnings:
            lines.append("\n警告:")
            for w in content.warnings:
                lines.append(f"  - {w}")
        
        return "\n".join(lines)

# 便捷函数
def view_document(file_path: str, options: Dict = None) -> Optional[DocumentContent]:
    """查看文档的便捷函数"""
    viewer = DocumentViewer()
    return viewer.read(file_path, options)

def get_document_info(file_path: str) -> Optional[DocumentMetadata]:
    """获取文档信息的便捷函数"""
    viewer = DocumentViewer()
    return viewer.get_metadata(file_path)

def extract_text_from_pdf(pdf_path: str, pages: List[int] = None) -> str:
    """从PDF提取文本的便捷函数"""
    viewer = DocumentViewer()
    content = viewer.read(pdf_path, {'max_pages': 1000})
    
    if content and pages:
        return "\n\n".join([content.pages[i-1] for i in pages if i <= len(content.pages)])
    return content.text_content if content else ""

def ocr_image(image_path: str) -> str:
    """对图片执行OCR的便捷函数"""
    viewer = DocumentViewer(enable_ocr=True)
    content = viewer.read(image_path)
    return content.ocr_text if content else ""
