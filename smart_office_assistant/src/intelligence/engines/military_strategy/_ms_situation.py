"""
__all__ = [
    'analyze',
]

形势分析器 - 分析当前形势并确定策略类别
"""

from typing import Dict
from ._ms_enums import StrategyCategory

class SituationAnalyzer:
    """形势分析器"""
    
    def analyze(self, self_state: Dict, enemy_state: Dict, context: Dict) -> tuple:
        """分析形势，返回(策略类别, 优势比)"""
        # 计算双方实力
        self_strength = self._calculate_strength(self_state)
        enemy_strength = self._calculate_strength(enemy_state)
        
        # 计算优势比
        advantage = self_strength / enemy_strength if enemy_strength > 0 else 2.0
        
        # 考虑环境因素
        advantage = self._adjust_for_context(advantage, context)
        
        # 确定策略类别
        category = self._determine_category(advantage, context)
        
        return category, advantage
    
    def _calculate_strength(self, state: Dict) -> float:
        """计算实力"""
        strength = state.get('resources', 100)
        strength *= (1 + state.get('morale', 0.5))
        strength *= (1 + state.get('position', 0.0))
        return max(1.0, strength)
    
    def _adjust_for_context(self, advantage: float, context: Dict) -> float:
        """根据环境调整优势"""
        # 地形因素
        terrain = context.get('terrain', 'plain')
        if terrain == 'mountain':
            advantage *= 1.2
        elif terrain == 'river':
            advantage *= 0.9
        
        # 天气因素
        weather = context.get('weather', 'clear')
        if weather == 'rain':
            advantage *= 0.95
        
        # 时机因素
        timing = context.get('timing', 'normal')
        if timing == 'favorable':
            advantage *= 1.15
        elif timing == 'unfavorable':
            advantage *= 0.85
        
        return advantage
    
    def _determine_category(self, advantage: float, context: Dict) -> StrategyCategory:
        """确定策略类别"""
        # 根据优势比确定类别
        if advantage >= 1.5:
            return StrategyCategory.VICTORY
        elif advantage >= 1.0:
            return StrategyCategory.CONFRONTATION
        elif advantage >= 0.7:
            return StrategyCategory.ATTACK
        elif advantage >= 0.4:
            return StrategyCategory.CHAOS
        elif advantage >= 0.2:
            return StrategyCategory.MERGE
        else:
            return StrategyCategory.RETREAT
