# -*- coding: utf-8 -*-
"""诗词分析引擎 - 类型定义模块"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any

__all__ = [
    'to_dict',
    'to_json',
]

class PoetryAnalysisLevel(Enum):
    """诗词分析层级"""
    BASIC = "basic"          # 基础分析:韵律,字数,句式
    INTERMEDIATE = "intermediate"  # 中级分析:imagery,情感,主题
    ADVANCED = "advanced"    # 高级分析:style,影响,创新性
    EXPERT = "expert"        # 专家分析:synthesize深度分析

class PoetryStyle(Enum):
    """诗词style分类"""
    HEROIC = "豪放"          # 豪放派:李白,苏轼,辛弃疾
    DELICATE = "婉约"        # 婉约派:李清照,柳永,秦观
    FRESH = "清新"           # 清新派:王维,孟浩然
    BOLD = "雄浑"            # 雄浑派:杜甫,高适
    ELEGANT = "典雅"         # 典雅派:晏殊,周邦彦
    SIMPLE = "质朴"          # 质朴派:陶渊明,白居易
    MYSTERIOUS = "朦胧"      # 朦胧派:李商隐,李贺

@dataclass
class PoetryAnalysisResult:
    """诗词分析结果数据结构"""
    poem_id: str
    poem_title: str
    author: str
    dynasty: str

    # 基础分析结果
    basic_analysis: Dict[str, Any] = field(default_factory=dict)

    # 中级分析结果
    intermediate_analysis: Dict[str, Any] = field(default_factory=dict)

    # 高级分析结果
    advanced_analysis: Dict[str, Any] = field(default_factory=dict)

    # synthesize评分
    comprehensive_score: Dict[str, float] = field(default_factory=dict)

    # 分析时间戳
    analysis_timestamp: str = ""

    # 原始文本
    original_text: str = ""

    # 注释和翻译
    annotations: List[str] = field(default_factory=list)
    translations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "poem_id": self.poem_id,
            "poem_title": self.poem_title,
            "author": self.author,
            "dynasty": self.dynasty,
            "basic_analysis": self.basic_analysis,
            "intermediate_analysis": self.intermediate_analysis,
            "advanced_analysis": self.advanced_analysis,
            "comprehensive_score": self.comprehensive_score,
            "analysis_timestamp": self.analysis_timestamp,
            "original_text": self.original_text,
            "annotations": self.annotations,
            "translations": self.translations
        }

    def to_json(self) -> str:
        """转换为JSON格式"""
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
