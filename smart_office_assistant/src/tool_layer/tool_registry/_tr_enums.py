"""枚举定义模块"""

from enum import Enum

class ToolCategory(Enum):
    """工具分类"""
    LLM = "llm"
    DATA_ANALYSIS = "data_analysis"
    VISUALIZATION = "visualization"
    COMMUNICATION = "communication"
    STORAGE = "storage"
    SEARCH = "search"
    CALCULATION = "calculation"
    AUTOMATION = "automation"

class ToolStatus(Enum):
    """工具状态"""
    ACTIVE = "active"
    DISABLED = "disabled"
    ERROR = "error"
    DEPRECATED = "deprecated"
