"""
炫耀性消费分析器 - Conspicuous Consumption Analyzer
基于托斯丹·凡勃伦(Thorstein Veblen)制度经济学的消费心理分析系统

核心思想:
1. 炫耀性消费 - 消费是为了展示而非满足
2. 有闲阶级 - 闲暇和消费是身份的标志
3. 金钱荣誉竞赛 - 消费竞争是社会地位的争夺
4. 品味是阶级区隔 - 品味区分社会阶层

版本: v1.0.0
"""

import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)

class ConsumptionType(Enum):
    CONSPICUOUS = "conspicuous"           # 炫耀性消费
    VICARIOUS = "vicarious"               # 代理消费
    DISCRIMINATING = "discriminating"     # 歧视性消费
    FUNCTIONAL = "functional"             # 功能性消费

@dataclass
class ConsumptionAnalysis:
    """消费分析结果"""
    consumption_type: ConsumptionType
    status_signals: List[str]
    symbolic_meanings: List[str]
    recommendations: List[str]

class VeblenAnalyzer:
    """凡勃伦炫耀性消费分析器"""
    
    VEBLEN_INDICATORS = ['奢侈品', '限量', '定制', '稀缺', '昂贵', '名牌']
    CLASS_MARKERS = ['品味', '格调', '身份', '地位', '阶层', '精英']
    
    def analyze(self, user_behavior: Dict, product: str) -> ConsumptionAnalysis:
        """分析消费行为"""
        # recognize凡勃伦商品characteristics
        is_veblen = any(ind in product for ind in self.VEBLEN_INDICATORS)
        display_ratio = user_behavior.get('display_ratio', 0.5)
        
        # 分类消费类型
        if display_ratio > 0.7 or is_veblen:
            ctype = ConsumptionType.CONSPICUOUS
        elif display_ratio > 0.4:
            ctype = ConsumptionType.DISCRIMINATING
        else:
            ctype = ConsumptionType.FUNCTIONAL

        
        # 状态信号
        status_signals = self._extract_status_signals(product)
        
        # 符号意义
        symbolic_meanings = self._extract_symbolic_meanings(product)
        
        # 建议
        recommendations = self._generate_recommendations(ctype, is_veblen)
        
        return ConsumptionAnalysis(
            consumption_type=ctype,
            status_signals=status_signals,
            symbolic_meanings=symbolic_meanings,
            recommendations=recommendations
        )
    
    def _extract_status_signals(self, product: str) -> List[str]:
        """提取状态信号"""
        signals = []
        if any(k in product for k in ['奢侈品', '限量', '顶级']):
            signals.append("财富展示")
        if any(k in product for k in ['品味', '格调', '优雅']):
            signals.append("品味彰显")
        if any(k in product for k in ['身份', '地位', '阶层']):
            signals.append("身份认同")
        return signals if signals else ["实用功能"]
    
    def _extract_symbolic_meanings(self, product: str) -> List[str]:
        """提取符号意义"""
        meanings = []
        symbol_map = {
            '金': '财富', '钻': '永恒', '皮': '品质',
            '丝': '优雅', '手': '匠心', '限': '稀缺'
        }
        for sym, meaning in symbol_map.items():
            if sym in product:
                meanings.append(f"{sym}象征{meaning}")
        return meanings if meanings else ["功能性符号"]
    
    def _generate_recommendations(self, ctype: ConsumptionType, is_veblen: bool) -> List[str]:
        """generate凡勃伦式营销建议"""
        if ctype == ConsumptionType.CONSPICUOUS:
            return [
                "强调稀缺性和独特编号",
                "突出价格和品质",
                "展示社会名流的选择"
            ]

        elif ctype == ConsumptionType.DISCRIMINATING:
            return [
                "强调独特设计和文化内涵",
                "讲述工艺传承和匠心",
                "展示独特品味"
            ]
        else:
            return ["强调功能价值和性价比"]

__all__ = ['VeblenAnalyzer', 'ConsumptionType', 'ConsumptionAnalysis']
