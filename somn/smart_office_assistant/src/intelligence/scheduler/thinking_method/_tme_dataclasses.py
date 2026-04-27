"""
思维方法数据类定义
"""



__all__ = [
    'ThinkingAnalysis',
    'ThinkingPath',
    'MethodSuggestion',
    'ThinkingMethodResult',
]
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

@dataclass
class ThinkingAnalysis:
    """思维分析结果"""
    method: str
    title: str
    description: str
    keywords: List[str]
    process: List[str]
    applications: List[str]
    depth: str
    insight: str
    warnings: List[str] = field(default_factory=list)

@dataclass
class ThinkingPath:
    """思维路径"""
    step: int
    method: str
    description: str
    thinking: str
    outcome: str

@dataclass
class MethodSuggestion:
    """方法建议"""
    method: str
    title: str
    description: str
    suitability: str
    expected_outcome: str

@dataclass
class ThinkingMethodResult:
    """思维方法分析结果"""
    original_query: str
    selected_methods: List[MethodSuggestion]
    thinking_paths: List[ThinkingPath]
    comprehensive_analysis: ThinkingAnalysis
    depth_assessment: Dict[str, Any]
    recommendations: List[str]
    summary: str
