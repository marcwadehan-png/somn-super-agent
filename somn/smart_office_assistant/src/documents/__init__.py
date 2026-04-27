"""
文档模块 [v1.0 智能文档处理升级 - 完整版]
Document Modules - 智能化文档处理能力

提供六大功能:
1. 文档生成 - Word,PPT,PDF,Excel 文档的生成和编辑
2. 文档查看 - 支持打开,查看,阅读主流文档格式
3. 自然语言处理 - 自然语言驱动的智能文档处理
4. 智能模板 - 模板填充/批量处理/格式转换
5. 智能分析 - 内容理解/实体识别/结构提取/摘要生成
6. 依赖完善 - python-pptx/python-docx/openpyxl 完整集成

支持格式:
- 文档查看: PDF, Word, Excel, PowerPoint, TXT, Markdown, JSON, XML, HTML, 图片, 压缩包
- 图片OCR: 支持中文简体,英文等多种语言
- 压缩包: ZIP, RAR, 7Z, TAR, GZ 等
- 自然语言: 支持意图识别,自动处理各类文档任务

[v1.0 优化]
- 修复模块导出：ContentAnalyzer/LibreOfficeConverter/PDFAdvancedTools
- DocumentHub统一入口完整导出
- 所有v1.0-v1.0类100%可导入

版本: v1.0.0
日期: 2026-04-25
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    # 文档查看器
    from .document_viewer import (
        DocumentViewer, DocumentType, DocumentMetadata, DocumentContent,
        view_document, get_document_info, extract_text_from_pdf, ocr_image,
    )
    # 文档生成
    from .docx_generator import (
        DOCXGenerator, DocumentTemplates, DocumentSection, TableData, ImageData
    )
    from .pptx_generator import (
        PPTXGenerator, PresentationTemplates, SlideContent, SlideLayout, ChartData
    )
    from .pdf_generator import PDFGenerator, PDFTemplates, PDFSection
    from .excel_generator import ExcelGenerator, ExcelTemplates, ColumnConfig, ChartConfig
    # 自然语言文档服务 [v1.0新增]
    from .nlp_document_service import (
        NaturalLanguageDocumentService, DocumentIntent, DocumentFormat,
        DocumentResult, quick_process
    )
    # 智能模板填充 [v1.0 Phase3新增]
    from .template_filler import (
        TemplateFiller, TemplateType, TemplateVariable, TemplateContext,
        BatchTemplateFiller, FillResult, quick_fill, fill_file
    )
    # 批量文档处理 [v1.0 Phase3新增]
    from .batch_processor import (
        BatchDocumentProcessor, BatchTask, BatchResult, TaskStatus,
        batch_generate, batch_convert
    )
    # 文档转换工具 [v1.0 Phase3新增]
    from .document_converter import (
        DocumentConverter, Format, ConversionResult, quick_convert
    )
    # 文档智能分析 [v1.0 Phase4新增]
    from .document_intelligence import (
        DocumentIntelligenceService, EntityRecognizer, DocumentStructureAnalyzer,
        TableExtractor, DocumentSummarizer,
        EntityType, DocumentEntity, DocumentSection, TableData, DocumentSummary,
        DocumentAnalysis, AnalysisResult,
        analyze_document, extract_entities, extract_tables, summarize_document
    )


def __getattr__(name: str) -> Any:
    """[v1.0 优化] 延迟加载 - 毫秒级启动 + 自然语言支持 + Phase3-4"""

    # ===== Phase 4 新增模块 =====
    # 文档智能分析 [v1.0 Phase4新增]
    if name in ('DocumentIntelligenceService', 'EntityRecognizer', 'DocumentStructureAnalyzer',
                'TableExtractor', 'DocumentSummarizer',
                'EntityType', 'DocumentEntity', 'DocumentSection', 'TableData', 'DocumentSummary',
                'DocumentAnalysis', 'AnalysisResult',
                'analyze_document', 'extract_entities', 'extract_tables', 'summarize_document'):
        from . import document_intelligence as _m
        return getattr(_m, name)
    
    # ===== v1.0 DocumentHub 统一入口 =====
    elif name in ('DocumentHub', 'DocumentIntent', 'DocumentType', 'DocumentRequest', 'DocumentResponse'):
        from . import document_hub as _m
        return getattr(_m, name)
    
    # ===== v1.0 AI推荐 & LO转换 =====
    elif name in ('ContentAnalyzer', 'ContentType'):
        from . import content_recommender as _m
        return getattr(_m, name)
    
    elif name in ('LibreOfficeConverter',):
        from . import libreoffice_integration as _m
        return getattr(_m, name)
    
    elif name in ('PDFAdvancedTools', 'PDFFeature', 'PDFResult'):
        from . import pdf_tools as _m
        return getattr(_m, name)
    
    # ===== Phase 3 新增模块 =====
    # 智能模板填充 [v1.0 Phase3新增]
    elif name in ('TemplateFiller', 'TemplateType', 'TemplateVariable', 'TemplateContext',
                  'FillResult', 'quick_fill', 'fill_file'):
        from . import template_filler as _m
        return getattr(_m, name)
    
    # 批量文档处理 [v1.0 Phase3新增]
    elif name in ('BatchDocumentProcessor', 'BatchTask', 'BatchResult', 'TaskStatus',
                  'batch_generate', 'batch_convert'):
        from . import batch_processor as _m
        return getattr(_m, name)
    
    # 文档转换工具 [v1.0 Phase3新增]
    elif name in ('DocumentConverter', 'Format', 'ConversionResult', 'quick_convert'):
        from . import document_converter as _m
        return getattr(_m, name)
    
    # 自然语言文档服务 [v1.0新增]
    elif name in ('NaturalLanguageDocumentService', 'DocumentIntent', 'DocumentFormat',
                  'DocumentResult', 'quick_process'):
        from . import nlp_document_service as _m
        return getattr(_m, name)

    # 文档查看器 - 核心功能
    elif name in ('DocumentViewer', 'DocumentType', 'DocumentMetadata', 'DocumentContent',
                  'view_document', 'get_document_info', 'extract_text_from_pdf', 'ocr_image'):
        from . import document_viewer as _m
        return getattr(_m, name)

    # DOCX生成器
    elif name in ('DOCXGenerator', 'DocumentTemplates', 'DocumentSection', 'TableData', 'ImageData'):
        from . import docx_generator as _m
        return getattr(_m, name)

    # PPTX生成器
    elif name in ('PPTXGenerator', 'PresentationTemplates', 'SlideContent', 'SlideLayout', 'ChartData'):
        from . import pptx_generator as _m
        return getattr(_m, name)

    # PDF生成器
    elif name in ('PDFGenerator', 'PDFTemplates', 'PDFSection'):
        from . import pdf_generator as _m
        return getattr(_m, name)

    # Excel生成器
    elif name in ('ExcelGenerator', 'ExcelTemplates', 'ColumnConfig', 'ChartConfig'):
        from . import excel_generator as _m
        return getattr(_m, name)

    raise AttributeError(f"module 'documents' has no attribute '{name}'")


__all__ = [
    # ===== 文档查看 =====
    'DocumentViewer', 'DocumentType', 'DocumentMetadata', 'DocumentContent',
    'view_document', 'get_document_info', 'extract_text_from_pdf', 'ocr_image',
    # ===== 文档生成 =====
    'DOCXGenerator', 'DocumentTemplates', 'DocumentSection', 'TableData', 'ImageData',
    'PPTXGenerator', 'PresentationTemplates', 'SlideContent', 'SlideLayout', 'ChartData',
    'PDFGenerator', 'PDFTemplates', 'PDFSection',
    'ExcelGenerator', 'ExcelTemplates', 'ColumnConfig', 'ChartConfig',
    # ===== 自然语言处理 [v1.0新增] =====
    'NaturalLanguageDocumentService', 'DocumentIntent', 'DocumentFormat',
    'DocumentResult', 'quick_process',
    # ===== 智能模板填充 [v1.0 Phase3新增] =====
    'TemplateFiller', 'TemplateType', 'TemplateVariable', 'TemplateContext',
    'BatchTemplateFiller', 'FillResult', 'quick_fill', 'fill_file',
    # ===== 批量文档处理 [v1.0 Phase3新增] =====
    'BatchDocumentProcessor', 'BatchTask', 'BatchResult', 'TaskStatus',
    'batch_generate', 'batch_convert',
    # ===== 文档转换工具 [v1.0 Phase3新增] =====
    'DocumentConverter', 'Format', 'ConversionResult', 'quick_convert',
    # ===== 文档智能分析 [v1.0 Phase4新增] =====
    'DocumentIntelligenceService', 'EntityRecognizer', 'DocumentStructureAnalyzer',
    'TableExtractor', 'DocumentSummarizer',
    'EntityType', 'DocumentEntity', 'DocumentSection', 'TableData', 'DocumentSummary',
    'DocumentAnalysis', 'AnalysisResult',
    'analyze_document', 'extract_entities', 'extract_tables', 'summarize_document',
    # ===== v1.0 DocumentHub统一入口 =====
    'DocumentHub', 'DocumentIntent', 'DocumentType', 'DocumentRequest', 'DocumentResponse',
    # ===== v1.0 AI推荐 & LO转换 =====
    'ContentAnalyzer', 'ContentType',
    'LibreOfficeConverter',
    'PDFAdvancedTools', 'PDFFeature', 'PDFResult',
]
