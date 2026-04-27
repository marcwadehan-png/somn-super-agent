# -*- coding: utf-8 -*-
"""
文档处理异常和错误处理 [v22.4]
Document Processing Exceptions

功能:
- 统一的异常类定义
- 错误码规范
- 错误恢复建议

版本: v22.4.0
日期: 2026-04-25
"""

from typing import Optional, Dict, Any, List
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ErrorCode(Enum):
    """错误码"""
    # 通用错误 (1000-1999)
    UNKNOWN_ERROR = (1000, "未知错误")
    INVALID_PARAMETER = (1001, "参数无效")
    FILE_NOT_FOUND = (1002, "文件不存在")
    PERMISSION_DENIED = (1003, "权限不足")
    DEPENDENCY_MISSING = (1004, "依赖未安装")
    
    # 文档生成错误 (2000-2999)
    GENERATION_FAILED = (2000, "生成失败")
    TEMPLATE_NOT_FOUND = (2001, "模板不存在")
    TEMPLATE_VARIABLE_MISSING = (2002, "模板变量缺失")
    CONTENT_TOO_LONG = (2003, "内容过长")
    INVALID_FORMAT = (2004, "格式无效")
    
    # 转换错误 (3000-3999)
    CONVERSION_FAILED = (3000, "转换失败")
    UNSUPPORTED_FORMAT = (3001, "不支持的格式")
    CONVERSION_TIMEOUT = (3002, "转换超时")
    
    # 读取错误 (4000-4999)
    READ_FAILED = (4000, "读取失败")
    ENCRYPTED_FILE = (4001, "文件已加密")
    CORRUPTED_FILE = (4002, "文件损坏")
    
    # 分析错误 (5000-5999)
    ANALYSIS_FAILED = (5000, "分析失败")
    PARSING_ERROR = (5001, "解析错误")
    EXTRACTION_FAILED = (5002, "提取失败")


class DocumentError(Exception):
    """
    文档处理基础异常
    
    提供错误码和恢复建议。
    """
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        details: Optional[Dict[str, Any]] = None,
        suggestions: Optional[List[str]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.code = error_code.value[0]
        self.description = error_code.value[1]
        self.details = details or {}
        self.suggestions = suggestions or self._get_default_suggestions()
    
    def _get_default_suggestions(self) -> List[str]:
        """获取默认恢复建议"""
        suggestions_map = {
            ErrorCode.UNKNOWN_ERROR: ["检查日志以获取更多信息"],
            ErrorCode.INVALID_PARAMETER: ["检查输入参数是否正确"],
            ErrorCode.FILE_NOT_FOUND: ["确认文件路径是否正确"],
            ErrorCode.PERMISSION_DENIED: ["检查文件权限设置"],
            ErrorCode.DEPENDENCY_MISSING: ["安装缺失的依赖包"],
            ErrorCode.GENERATION_FAILED: ["检查内容格式和数据"],
            ErrorCode.TEMPLATE_NOT_FOUND: ["确认模板文件存在"],
            ErrorCode.TEMPLATE_VARIABLE_MISSING: ["检查模板变量是否完整"],
            ErrorCode.UNSUPPORTED_FORMAT: ["使用支持的格式"],
            ErrorCode.CONVERSION_FAILED: ["尝试其他转换方式"],
            ErrorCode.READ_FAILED: ["确认文件完整性"],
            ErrorCode.ENCRYPTED_FILE: ["提供解密密钥"],
            ErrorCode.CORRUPTED_FILE: ["尝试恢复或使用原文件"],
        }
        return suggestions_map.get(self.error_code, ["联系技术支持"])
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "error": {
                "code": self.code,
                "type": self.error_code.name,
                "message": self.message,
                "description": self.description,
                "details": self.details,
                "suggestions": self.suggestions
            }
        }
    
    def __str__(self) -> str:
        return f"[{self.code}] {self.description}: {self.message}"


class TemplateError(DocumentError):
    """模板相关错误"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.TEMPLATE_NOT_FOUND,
            **kwargs
        )


class ConversionError(DocumentError):
    """格式转换错误"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.CONVERSION_FAILED,
            **kwargs
        )


class GenerationError(DocumentError):
    """文档生成错误"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.GENERATION_FAILED,
            **kwargs
        )


class ReadingError(DocumentError):
    """文档读取错误"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.READ_FAILED,
            **kwargs
        )


class AnalysisError(DocumentError):
    """文档分析错误"""
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message,
            error_code=ErrorCode.ANALYSIS_FAILED,
            **kwargs
        )


def handle_document_error(
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    reraise: bool = False
) -> Optional[DocumentError]:
    """
    处理文档处理错误
    
    Args:
        error: 原始异常
        context: 错误上下文
        reraise: 是否重新抛出
    
    Returns:
        DocumentError: 转换后的错误对象
    """
    context = context or {}
    
    # 已经是DocumentError
    if isinstance(error, DocumentError):
        doc_error = error
        if context:
            doc_error.details.update(context)
        if reraise:
            raise doc_error
        return doc_error
    
    # 转换常见异常
    error_mapping = {
        FileNotFoundError: ErrorCode.FILE_NOT_FOUND,
        PermissionError: ErrorCode.PERMISSION_DENIED,
        ValueError: ErrorCode.INVALID_PARAMETER,
        ImportError: ErrorCode.DEPENDENCY_MISSING,
        TimeoutError: ErrorCode.CONVERSION_TIMEOUT,
    }
    
    error_code = ErrorCode.UNKNOWN_ERROR
    for exc_type, code in error_mapping.items():
        if isinstance(error, exc_type):
            error_code = code
            break
    
    doc_error = DocumentError(
        message=str(error),
        error_code=error_code,
        details=context
    )
    
    logger.error(f"文档处理错误: {doc_error}")
    
    if reraise:
        raise doc_error
    
    return doc_error


class ErrorRecovery:
    """
    错误恢复策略
    
    提供自动错误恢复建议。
    """
    
    @staticmethod
    def suggest_recovery(error: DocumentError) -> Dict[str, Any]:
        """建议错误恢复方案"""
        recovery_map = {
            ErrorCode.DEPENDENCY_MISSING: {
                "action": "install_dependency",
                "packages": {
                    "python-docx": "pip install python-docx",
                    "python-pptx": "pip install python-pptx",
                    "openpyxl": "pip install openpyxl",
                    "PyPDF2": "pip install PyPDF2",
                    "reportlab": "pip install reportlab",
                }
            },
            ErrorCode.FILE_NOT_FOUND: {
                "action": "check_path",
                "suggestions": [
                    "确认文件路径正确",
                    "检查文件是否被移动或删除",
                    "使用绝对路径"
                ]
            },
            ErrorCode.CONVERSION_FAILED: {
                "action": "alternative_conversion",
                "suggestions": [
                    "尝试使用LibreOffice转换",
                    "分步转换（如docx->pdf->其他格式）",
                    "检查源文件是否损坏"
                ]
            }
        }
        
        return recovery_map.get(error.error_code, {"action": "manual"})


# 便捷函数
def require_dependency(package: str, feature: str) -> None:
    """检查依赖，如果缺失则抛出错误"""
    try:
        __import__(package)
    except ImportError:
        raise DocumentError(
            f"功能 '{feature}' 需要 {package} 依赖",
            error_code=ErrorCode.DEPENDENCY_MISSING,
            suggestions=[f"运行: pip install {package}"]
        )
