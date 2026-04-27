# -*- coding: utf-8 -*-
"""
统一文档处理中枢 [v22.4]
Document Hub - Unified Document Processing Center

功能:
- 统一的文档处理入口
- 智能意图识别和路由
- 一站式文档生成/转换/分析
- 模板管理和批量处理

版本: v22.4.0
日期: 2026-04-25
"""

from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class DocumentIntent(Enum):
    """文档意图类型"""
    GENERATE_PPT = "generate_ppt"
    GENERATE_WORD = "generate_word"
    GENERATE_EXCEL = "generate_excel"
    GENERATE_PDF = "generate_pdf"
    READ_DOCUMENT = "read_document"
    CONVERT_FORMAT = "convert_format"
    ANALYZE_DOCUMENT = "analyze_document"
    TEMPLATE_FILL = "template_fill"
    BATCH_PROCESS = "batch_process"
    MERGE_DOCUMENTS = "merge_documents"
    UNKNOWN = "unknown"


class DocumentType(Enum):
    """文档类型"""
    PPT = "pptx"
    WORD = "docx"
    EXCEL = "xlsx"
    PDF = "pdf"
    MARKDOWN = "md"
    HTML = "html"
    TEXT = "txt"


@dataclass
class DocumentRequest:
    """文档处理请求"""
    intent: DocumentIntent
    command: str                      # 原始命令
    doc_type: Optional[DocumentType] = None
    content: Optional[str] = None     # 内容或文件路径
    data: Optional[Dict[str, Any]] = None
    template: Optional[str] = None     # 模板名称
    output_path: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentResponse:
    """文档处理响应"""
    success: bool
    message: str
    file_path: Optional[str] = None
    data: Optional[Any] = None
    errors: List[str] = field(default_factory=list)


class DocumentHub:
    """
    统一文档处理中枢
    
    提供单一的文档处理接口，智能路由到对应的处理模块。
    
    使用示例:
    ```python
    hub = DocumentHub()
    
    # 自然语言命令
    result = hub.process("生成项目报告PPT，包含季度总结")
    
    # 模板填充
    result = hub.process("填充报告模板", template="report", data={...})
    
    # 格式转换
    result = hub.process("转换PDF", input="doc.docx", to="pdf")
    ```
    """

    # 意图关键词映射
    INTENT_KEYWORDS = {
        DocumentIntent.GENERATE_PPT: ["ppt", "演示", "幻灯片", "presentation", "做PPT"],
        DocumentIntent.GENERATE_WORD: ["word", "文档", "报告", "docx", "写文档"],
        DocumentIntent.GENERATE_EXCEL: ["excel", "表格", "报表", "xlsx", "做表格"],
        DocumentIntent.GENERATE_PDF: ["pdf", "生成PDF"],
        DocumentIntent.READ_DOCUMENT: ["读取", "打开", "查看", "分析", "read"],
        DocumentIntent.CONVERT_FORMAT: ["转换", "转成", "export", "convert"],
        DocumentIntent.ANALYZE_DOCUMENT: ["分析", "提取", "理解"],
        DocumentIntent.TEMPLATE_FILL: ["模板", "填充", "template"],
        DocumentIntent.BATCH_PROCESS: ["批量", "batch"],
        DocumentIntent.MERGE_DOCUMENTS: ["合并", "merge"],
    }

    def __init__(self):
        """初始化文档处理中枢"""
        self._init_services()
        logger.info("DocumentHub 初始化完成")

    def _init_services(self):
        """初始化各服务模块"""
        # 延迟导入，避免循环依赖
        self._nlp_service = None
        self._ppt_generator = None
        self._docx_generator = None
        self._excel_generator = None
        self._pdf_generator = None
        self._converter = None
        self._analyzer = None
        self._template_filler = None
        self._batch_processor = None

    def _get_nlp_service(self):
        """获取NLP服务"""
        if self._nlp_service is None:
            try:
                from .nlp_document_service import NaturalLanguageDocumentService
                self._nlp_service = NaturalLanguageDocumentService()
            except ImportError:
                logger.warning("NLP服务未安装")
        return self._nlp_service

    def _get_ppt_generator(self):
        """获取PPT生成器"""
        if self._ppt_generator is None:
            try:
                from .pptx_generator import PPTXGenerator
                self._ppt_generator = PPTXGenerator()
            except ImportError as e:
                logger.warning(f"PPT生成器未安装: {e}")
        return self._ppt_generator

    def _get_docx_generator(self):
        """获取Word生成器"""
        if self._docx_generator is None:
            try:
                from .docx_generator import DOCXGenerator
                self._docx_generator = DOCXGenerator()
            except ImportError as e:
                logger.warning(f"Word生成器未安装: {e}")
        return self._docx_generator

    def _get_excel_generator(self):
        """获取Excel生成器"""
        if self._excel_generator is None:
            try:
                from .excel_generator import ExcelGenerator
                self._excel_generator = ExcelGenerator()
            except ImportError as e:
                logger.warning(f"Excel生成器未安装: {e}")
        return self._excel_generator

    def _get_pdf_generator(self):
        """获取PDF生成器"""
        if self._pdf_generator is None:
            try:
                from .pdf_generator import PDFGenerator
                self._pdf_generator = PDFGenerator()
            except ImportError as e:
                logger.warning(f"PDF生成器未安装: {e}")
        return self._pdf_generator

    def _get_converter(self):
        """获取格式转换器"""
        if self._converter is None:
            try:
                from .document_converter import DocumentConverter
                self._converter = DocumentConverter()
            except ImportError as e:
                logger.warning(f"转换器未安装: {e}")
        return self._converter

    def _get_analyzer(self):
        """获取文档分析器"""
        if self._analyzer is None:
            try:
                from .document_intelligence import DocumentIntelligenceService
                self._analyzer = DocumentIntelligenceService()
            except ImportError as e:
                logger.warning(f"分析器未安装: {e}")
        return self._analyzer

    def _get_template_filler(self):
        """获取模板填充器"""
        if self._template_filler is None:
            try:
                from .template_filler import TemplateFiller
                self._template_filler = TemplateFiller()
            except ImportError as e:
                logger.warning(f"模板填充器未安装: {e}")
        return self._template_filler

    def _get_batch_processor(self):
        """获取批量处理器"""
        if self._batch_processor is None:
            try:
                from .batch_processor import BatchDocumentProcessor
                self._batch_processor = BatchDocumentProcessor()
            except ImportError as e:
                logger.warning(f"批量处理器未安装: {e}")
        return self._batch_processor

    def classify_intent(self, command: str) -> DocumentIntent:
        """识别用户意图"""
        command_lower = command.lower()
        
        # 遍历所有意图关键词
        for intent, keywords in self.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in command_lower:
                    return intent
        
        return DocumentIntent.UNKNOWN

    def detect_document_type(self, command: str) -> Optional[DocumentType]:
        """检测文档类型"""
        command_lower = command.lower()
        
        type_map = {
            DocumentType.PPT: ["ppt", "演示", "幻灯片", "presentation"],
            DocumentType.WORD: ["word", "文档", "报告", "docx"],
            DocumentType.EXCEL: ["excel", "表格", "报表", "xlsx"],
            DocumentType.PDF: ["pdf"],
            DocumentType.MARKDOWN: ["md", "markdown"],
            DocumentType.HTML: ["html"],
        }
        
        for doc_type, keywords in type_map.items():
            for keyword in keywords:
                if keyword in command_lower:
                    return doc_type
        
        return None

    def process(self, command: str, **kwargs) -> DocumentResponse:
        """
        处理文档请求
        
        Args:
            command: 自然语言命令
            **kwargs: 额外参数 (data, template, output_path等)
        
        Returns:
            DocumentResponse: 处理结果
        """
        try:
            # 1. 意图识别
            intent = self.classify_intent(command)
            doc_type = kwargs.get('doc_type') or self.detect_document_type(command)
            
            logger.info(f"意图识别: {intent.value}, 类型: {doc_type}")
            
            # 2. 构建请求
            request = DocumentRequest(
                intent=intent,
                command=command,
                doc_type=doc_type,
                content=kwargs.get('content'),
                data=kwargs.get('data'),
                template=kwargs.get('template'),
                output_path=kwargs.get('output_path'),
                parameters=kwargs
            )
            
            # 3. 执行处理
            return self._dispatch(request)
            
        except Exception as e:
            logger.exception(f"文档处理失败: {command}")
            return DocumentResponse(
                success=False,
                message="处理失败"
            )

    def _dispatch(self, request: DocumentRequest) -> DocumentResponse:
        """分发请求到对应处理器"""
        intent = request.intent
        
        if intent == DocumentIntent.GENERATE_PPT:
            return self._handle_generate_ppt(request)
        elif intent == DocumentIntent.GENERATE_WORD:
            return self._handle_generate_word(request)
        elif intent == DocumentIntent.GENERATE_EXCEL:
            return self._handle_generate_excel(request)
        elif intent == DocumentIntent.GENERATE_PDF:
            return self._handle_generate_pdf(request)
        elif intent == DocumentIntent.CONVERT_FORMAT:
            return self._handle_convert(request)
        elif intent == DocumentIntent.ANALYZE_DOCUMENT:
            return self._handle_analyze(request)
        elif intent == DocumentIntent.TEMPLATE_FILL:
            return self._handle_template_fill(request)
        elif intent == DocumentIntent.BATCH_PROCESS:
            return self._handle_batch_process(request)
        elif intent == DocumentIntent.READ_DOCUMENT:
            return self._handle_read(request)
        else:
            return self._handle_unknown(request)

    def _handle_generate_ppt(self, request: DocumentRequest) -> DocumentResponse:
        """处理PPT生成"""
        generator = self._get_ppt_generator()
        if not generator:
            return DocumentResponse(
                success=False,
                message="PPT生成器未安装，请安装python-pptx"
            )
        
        try:
            data = request.data or {}
            if request.content:
                data['content'] = request.content
            
            output_path = request.output_path or "output/presentation.pptx"
            
            # 使用PPTXGenerator
            from .pptx_generator import PPTXGenerator
            gen = PPTXGenerator()
            result = gen.generate(data, output_path)
            
            return DocumentResponse(
                success=True,
                message="PPT生成成功",
                file_path=result
            )
        except Exception as e:
            return DocumentResponse(
                success=False,
                message="PPT生成失败"
            )

    def _handle_generate_word(self, request: DocumentRequest) -> DocumentResponse:
        """处理Word生成"""
        generator = self._get_docx_generator()
        if not generator:
            return DocumentResponse(
                success=False,
                message="Word生成器未安装，请安装python-docx"
            )
        
        try:
            data = request.data or {}
            if request.content:
                data['content'] = request.content
            
            output_path = request.output_path or "output/document.docx"
            
            from .docx_generator import DOCXGenerator
            gen = DOCXGenerator()
            result = gen.generate(data, output_path)
            
            return DocumentResponse(
                success=True,
                message="Word文档生成成功",
                file_path=result
            )
        except Exception as e:
            return DocumentResponse(
                success=False,
                message="Word生成失败"
            )

    def _handle_generate_excel(self, request: DocumentRequest) -> DocumentResponse:
        """处理Excel生成"""
        generator = self._get_excel_generator()
        if not generator:
            return DocumentResponse(
                success=False,
                message="Excel生成器未安装，请安装openpyxl"
            )
        
        try:
            data = request.data or {}
            if request.content:
                data['content'] = request.content
            
            output_path = request.output_path or "output/spreadsheet.xlsx"
            
            from .excel_generator import ExcelGenerator
            gen = ExcelGenerator()
            result = gen.generate(data, output_path)
            
            return DocumentResponse(
                success=True,
                message="Excel表格生成成功",
                file_path=result
            )
        except Exception as e:
            return DocumentResponse(
                success=False,
                message="Excel生成失败"
            )

    def _handle_generate_pdf(self, request: DocumentRequest) -> DocumentResponse:
        """处理PDF生成"""
        try:
            from .pdf_generator import PDFGenerator, PDFSection
            
            data = request.data or {}
            content = request.content or data.get('content', '')
            
            output_path = request.output_path or "output/document.pdf"
            
            gen = PDFGenerator(title=data.get('title', 'PDF Document'))
            
            if isinstance(content, str):
                sections = [
                    PDFSection(
                        title=data.get('title', 'Document'),
                        content=content,
                        level=1
                    )
                ]
                gen.build_report(sections)
            else:
                gen.add_title(data.get('title', 'PDF Document'))
                gen.add_paragraph(content)
            
            result = gen.save(output_path)
            
            return DocumentResponse(
                success=True,
                message="PDF生成成功",
                file_path=result
            )
        except Exception as e:
            return DocumentResponse(
                success=False,
                message="PDF生成失败"
            )

    def _handle_convert(self, request: DocumentRequest) -> DocumentResponse:
        """处理格式转换"""
        converter = self._get_converter()
        if not converter:
            return DocumentResponse(
                success=False,
                message="格式转换器未安装"
            )
        
        try:
            input_path = request.content
            to_format = request.parameters.get('to_format', 'pdf')
            output_path = request.output_path
            
            result = converter.convert(input_path, output_path, to_format)
            
            if result.success:
                return DocumentResponse(
                    success=True,
                    message=f"转换成功: {to_format}",
                    file_path=str(result.output_path)
                )
            else:
                return DocumentResponse(
                    success=False,
                    message=f"转换失败: {result.error}",
                    errors=[result.error] if result.error else []
                )
        except Exception as e:
            return DocumentResponse(
                success=False,
                message="格式转换失败"
            )

    def _handle_analyze(self, request: DocumentRequest) -> DocumentResponse:
        """处理文档分析"""
        analyzer = self._get_analyzer()
        if not analyzer:
            return DocumentResponse(
                success=False,
                message="文档分析器未安装"
            )
        
        try:
            file_path = request.content
            
            result = analyzer.analyze_document(file_path)
            
            if result.success:
                return DocumentResponse(
                    success=True,
                    message="文档分析完成",
                    data=result.summary
                )
            else:
                return DocumentResponse(
                    success=False,
                    message=f"分析失败: {result.error}",
                    errors=[result.error] if result.error else []
                )
        except Exception as e:
            return DocumentResponse(
                success=False,
                message="文档分析失败"
            )

    def _handle_template_fill(self, request: DocumentRequest) -> DocumentResponse:
        """处理模板填充"""
        filler = self._get_template_filler()
        if not filler:
            return DocumentResponse(
                success=False,
                message="模板填充器未安装"
            )
        
        try:
            template = request.template
            data = request.data or {}
            output_path = request.output_path
            
            result = filler.fill_template_file(template, data, output_path)
            
            if result.success:
                return DocumentResponse(
                    success=True,
                    message="模板填充成功",
                    file_path=str(result.output_path),
                    data=result.data
                )
            else:
                return DocumentResponse(
                    success=False,
                    message=f"填充失败: {result.error}",
                    errors=[result.error] if result.error else []
                )
        except Exception as e:
            return DocumentResponse(
                success=False,
                message="模板填充失败"
            )

    def _handle_batch_process(self, request: DocumentRequest) -> DocumentResponse:
        """处理批量处理"""
        processor = self._get_batch_processor()
        if not processor:
            return DocumentResponse(
                success=False,
                message="批量处理器未安装"
            )
        
        try:
            tasks = request.data.get('tasks', [])
            
            for task in tasks:
                task_type = task.get('type')
                if task_type == 'generate':
                    processor.add_generate_task(
                        task['template'],
                        task['data_list'],
                        output_dir=task.get('output_dir')
                    )
                elif task_type == 'convert':
                    processor.add_convert_task(
                        task['input_path'],
                        output_dir=task.get('output_dir'),
                        to_format=task.get('to_format')
                    )
            
            result = processor.execute()
            
            return DocumentResponse(
                success=True,
                message=f"批量处理完成: {result.success}/{result.total}",
                data={
                    'total': result.total,
                    'success': result.success,
                    'failed': result.failed
                }
            )
        except Exception as e:
            return DocumentResponse(
                success=False,
                message="批量处理失败"
            )

    def _handle_read(self, request: DocumentRequest) -> DocumentResponse:
        """处理文档读取"""
        try:
            from .document_viewer import DocumentViewer
            
            file_path = request.content
            viewer = DocumentViewer()
            content = viewer.read_document(file_path)
            
            return DocumentResponse(
                success=True,
                message="文档读取成功",
                data={'content': content}
            )
        except Exception as e:
            return DocumentResponse(
                success=False,
                message="文档读取失败"
            )

    def _handle_unknown(self, request: DocumentRequest) -> DocumentResponse:
        """处理未知意图"""
        return DocumentResponse(
            success=False,
            message=f"无法理解命令: {request.command}。支持的命令类型: 生成PPT/Word/Excel、转换格式、分析文档、模板填充等"
        )

    def get_capabilities(self) -> Dict[str, Any]:
        """获取能力清单"""
        return {
            'intents': [i.value for i in DocumentIntent],
            'document_types': [d.value for d in DocumentType],
            'features': {
                'ppt_generation': self._get_ppt_generator() is not None,
                'word_generation': self._get_docx_generator() is not None,
                'excel_generation': self._get_excel_generator() is not None,
                'pdf_generation': self._get_pdf_generator() is not None,
                'conversion': self._get_converter() is not None,
                'analysis': self._get_analyzer() is not None,
                'template_filling': self._get_template_filler() is not None,
                'batch_processing': self._get_batch_processor() is not None,
            }
        }


# 便捷函数
def create_document(command: str, **kwargs) -> DocumentResponse:
    """快速创建文档"""
    hub = DocumentHub()
    return hub.process(command, **kwargs)


def convert_document(input_path: str, output_format: str, output_path: str = None) -> DocumentResponse:
    """快速转换文档格式"""
    hub = DocumentHub()
    return hub.process(
        f"转换{output_format}",
        content=input_path,
        output_path=output_path,
        to_format=output_format
    )


def analyze_document(file_path: str) -> DocumentResponse:
    """快速分析文档"""
    hub = DocumentHub()
    return hub.process("分析文档", content=file_path)
