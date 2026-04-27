# -*- coding: utf-8 -*-
"""
__all__ = [
    'evaluate',
    'get_phase_strategy',
]

道家决策模块 - DaoDecision
负责道家视角的决策分析、太极评估、增长策略等
"""
from typing import Any, Dict, List, Optional

class TaiJiDecision:
    """
    太极决策评估

    职责：
    1. 阴阳评估
    2. 太极平衡分析
    3. 决策方向建议
    """

    def __init__(self):
        """空初始化 - TaiJiDecision使用静态方法模式"""
        self._initialized = True

    def evaluate(self, yin_score: float, yang_score: float,
                 context: str = None) -> Dict[str, Any]:
        """
        太极决策评估

        Args:
            yin_score: 阴的得分 (0-10)
            yang_score: 阳的得分 (0-10)
            context: 决策上下文

        Returns:
            评估结果
        """
        total = yin_score + yang_score
        balance = abs(yin_score - yang_score)

        # 判断阴阳偏向
        if balance < 2:
            tendency = 'balanced'
            recommendation = '阴阳平衡，适合稳步推进'
        elif yin_score > yang_score:
            tendency = 'yin_heavy'
            recommendation = '偏阴，适合保守策略，考虑沉淀和积累'
        else:
            tendency = 'yang_heavy'
            recommendation = '偏阳，适合进取策略，考虑扩展和创新'

        # 计算太极值
        taiji_value = (yin_score * yang_score) ** 0.5 if yin_score > 0 and yang_score > 0 else 0

        return {
            'yin_score': yin_score,
            'yang_score': yang_score,
            'tendency': tendency,
            'balance_score': balance,
            'taiji_value': round(taiji_value, 2),
            'recommendation': recommendation,
            'direction': self._get_direction(tendency),
        }

    def _get_direction(self, tendency: str) -> str:
        """获取最佳方向"""
        directions = {
            'yin_heavy': '内向、沉淀、等待时机',
            'yang_heavy': '外向、行动、把握机会',
            'balanced': '灵活、顺势、动态平衡',
        }
        return directions.get(tendency, '顺势而为')

class GrowthStrategy:
    """
    增长战略应用

    职责：
    1. 增长阶段分析
    2. 阶段策略建议
    3. 阴阳平衡调整
    """

    PHASES = {
        '初创期': {
            'yin_yang': 'yang_heavy',
            'focus': '扩张、探索、抢占市场',
            'dao_advice': '上善若水 - 以滋养为导向，快速迭代',
        },
        '成长期': {
            'yin_yang': 'balanced',
            'focus': '平衡规模与效率，建立体系',
            'dao_advice': '无为而治 - 建立机制而非事必躬亲',
        },
        '成熟期': {
            'yin_yang': 'yin_heavy',
            'focus': '稳定、优化、深化价值',
            'dao_advice': '返璞归真 - 回归核心，去除冗余',
        },
        '转型期': {
            'yin_yang': 'yang_heavy',
            'focus': '创新、变革、寻找新增长点',
            'dao_advice': '柔弱胜刚强 - 以灵活应对不确定性',
        },
    }

    def get_phase_strategy(self, growth_phase: str,
                          current_state: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        获取阶段策略

        Args:
            growth_phase: 增长阶段
            current_state: 当前状态

        Returns:
            策略建议
        """
        phase_data = self.PHASES.get(growth_phase, self.PHASES['成长期'])

        return {
            'phase': growth_phase,
            'focus': phase_data['focus'],
            'yin_yang': phase_data['yin_yang'],
            'dao_advice': phase_data['dao_advice'],
            'recommendations': self._generate_recommendations(phase_data, current_state),
        }

    def _generate_recommendations(self, phase_data: Dict,
                                 current_state: Dict = None) -> List[str]:
        """生成具体建议"""
        recommendations = [
            f"重点关注：{phase_data['focus']}",
            f"道家指导：{phase_data['dao_advice']}",
        ]

        if phase_data['yin_yang'] == 'yang_heavy':
            recommendations.append('建议增加一些内敛和沉淀的动作')
        elif phase_data['yin_yang'] == 'yin_heavy':
            recommendations.append('建议增加一些进取和创新的动作')

        return recommendations
