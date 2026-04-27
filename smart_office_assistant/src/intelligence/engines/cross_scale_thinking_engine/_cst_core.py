# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze',
    'clear_history',
    'generate_strategy',
    'get_analysis_summary',
    'get_scale_bridges',
    'identify_emergence',
    'map_macro_to_micro',
    'map_micro_to_macro',
    'think',
    'validate_cross_scale_consistency',
]

跨尺度思维引擎 - 核心兼容层

原 cross_scale_thinking_engine.py 的兼容层实现
保持原有API不变，内部委托给子模块
"""

from typing import Dict, List, Any, Optional, Tuple
import logging

from ._cst_types import (
    ScaleLevel, MicroElement, MacroPattern,
    CrossScaleBridge, CrossScaleInsight, ThinkingMode
)
from ._cst_analyzer import MicroAnalyzer, MacroAnalyzer, CrossScaleAnalyzer
from ._cst_synthesizer import CrossScaleSynthesizer
from ._cst_strategy import CrossScaleStrategyEngine, CrossScaleStrategy

logger = logging.getLogger(__name__)

class CrossScaleThinkingEngine:
    """
    跨尺度思维引擎

    整合微观-中观-宏观三个尺度的分析能力，
    实现从细节到全局的系统性思考。
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化跨尺度思维引擎

        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)

        # 初始化子模块
        self.micro_analyzer = MicroAnalyzer()
        self.macro_analyzer = MacroAnalyzer()
        self.cross_scale_analyzer = CrossScaleAnalyzer()
        self.synthesizer = CrossScaleSynthesizer()
        self.strategy_engine = CrossScaleStrategyEngine()

        # 状态
        self.analysis_history: List[Dict[str, Any]] = []
        self.active_insights: List[CrossScaleInsight] = []

    def analyze(
        self,
        data: Dict[str, Any],
        target_scale: ScaleLevel = ScaleLevel.ORGANISM,
        context: Optional[Dict[str, Any]] = None
    ) -> CrossScaleInsight:
        """
        执行跨尺度分析

        Args:
            data: 输入数据
            target_scale: 目标分析尺度
            context: 上下文信息

        Returns:
            CrossScaleInsight: 跨尺度洞察
        """
        context = context or {}

        # 1. 微观分析
        micro_result = self.micro_analyzer.analyze(data)

        # 2. 宏观分析
        macro_result = self.macro_analyzer.analyze(data)

        # 3. 跨尺度分析
        cross_scale_result = self.cross_scale_analyzer.analyze(
            micro_result, macro_result, target_scale
        )

        # 4. 综合
        insight = self.synthesizer.synthesize_cross_scale(
            micro_result, macro_result
        )

        # 记录历史
        self.analysis_history.append({
            'data_summary': str(data)[:100],
            'target_scale': target_scale,
            'insight_id': insight.title
        })
        self.active_insights.append(insight)

        return insight

    def think(
        self,
        problem: str,
        mode: ThinkingMode = ThinkingMode.CROSS_SCALE,
        depth: int = 3
    ) -> Dict[str, Any]:
        """
        跨尺度思考

        Args:
            problem: 问题描述
            mode: 思考模式
            depth: 思考深度

        Returns:
            思考结果
        """
        # 解析问题
        problem_data = {'description': problem, 'mode': mode, 'depth': depth}

        # 执行分析
        insight = self.analyze(problem_data)

        # 根据模式调整输出
        if mode == ThinkingMode.MICRO_FOCUS:
            focus = '微观层面分析'
        elif mode == ThinkingMode.MACRO_FOCUS:
            focus = '宏观层面分析'
        else:
            focus = '平衡视角分析'

        return {
            'problem': problem,
            'mode': mode.value,
            'focus': focus,
            'insight': insight,
            'bridges': insight.bridges,
            'implications': insight.implications,
            'recommendations': insight.recommendations
        }

    def generate_strategy(
        self,
        problem_analysis: Dict[str, Any],
        constraints: Optional[Dict[str, Any]] = None
    ) -> List[CrossScaleStrategy]:
        """
        生成跨尺度策略

        Args:
            problem_analysis: 问题分析结果
            constraints: 约束条件

        Returns:
            策略列表
        """
        constraints = constraints or {}

        strategies = self.strategy_engine.generate_strategy(
            problem_analysis,
            constraints,
            problem_analysis.get('objectives', [])
        )

        return strategies

    def get_scale_bridges(
        self,
        scale_from: ScaleLevel,
        scale_to: ScaleLevel
    ) -> List[CrossScaleBridge]:
        """
        获取两个尺度之间的桥梁

        Args:
            scale_from: 起始尺度
            scale_to: 目标尺度

        Returns:
            桥梁列表
        """
        bridges = []

        # 从活跃洞察中提取桥梁
        for insight in self.active_insights:
            for bridge_data in insight.bridges:
                bridge = CrossScaleBridge(
                    bridge_id=f"bridge_{len(bridges)}",
                    source_scale=scale_from,
                    target_scale=scale_to,
                    source_elements=[bridge_data.get('micro_factor', {})],
                    target_patterns=[bridge_data.get('macro_pattern', {})],
                    mechanism=bridge_data.get('mechanism', ''),
                    strength=bridge_data.get('similarity', 0.5)
                )
                bridges.append(bridge)

        return bridges

    def map_micro_to_macro(
        self,
        micro_elements: List[MicroElement]
    ) -> List[MacroPattern]:
        """
        将微观元素映射到宏观模式

        Args:
            micro_elements: 微观元素列表

        Returns:
            宏观模式列表
        """
        macro_patterns = []

        for element in micro_elements:
            # 分析元素的宏观含义
            pattern = self.macro_analyzer.infer_from_micro(element)
            if pattern:
                macro_patterns.append(pattern)

        return macro_patterns

    def map_macro_to_micro(
        self,
        macro_patterns: List[MacroPattern]
    ) -> List[MicroElement]:
        """
        将宏观模式分解为微观元素

        Args:
            macro_patterns: 宏观模式列表

        Returns:
            微观元素列表
        """
        micro_elements = []

        for pattern in macro_patterns:
            # 分解模式为微观要素
            elements = self.micro_analyzer.decompose_from_macro(pattern)
            micro_elements.extend(elements)

        return micro_elements

    def identify_emergence(
        self,
        micro_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        识别涌现现象

        Args:
            micro_data: 微观数据

        Returns:
            涌现现象列表
        """
        return self.macro_analyzer.identify_emergent_patterns(micro_data)

    def validate_cross_scale_consistency(
        self,
        micro_model: Dict[str, Any],
        macro_model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        验证跨尺度一致性

        Args:
            micro_model: 微观模型
            macro_model: 宏观模型

        Returns:
            验证结果
        """
        inconsistencies = []

        # 检查微观预测与宏观观察的一致性
        micro_predictions = micro_model.get('predictions', [])
        macro_observations = macro_model.get('observations', [])

        for pred in micro_predictions:
            pred_macro = pred.get('macro_implication')
            matching_obs = None

            for obs in macro_observations:
                if self._is_matching(pred_macro, obs):
                    matching_obs = obs
                    break

            if matching_obs:
                consistency = self._calculate_consistency(pred, matching_obs)
                if consistency < 0.7:
                    inconsistencies.append({
                        'type': 'prediction_mismatch',
                        'micro_prediction': pred,
                        'macro_observation': matching_obs,
                        'consistency': consistency
                    })
            else:
                inconsistencies.append({
                    'type': 'missing_observation',
                    'micro_prediction': pred,
                    'message': '微观预测缺乏宏观验证'
                })

        return {
            'is_consistent': len(inconsistencies) == 0,
            'consistency_score': 1.0 - (len(inconsistencies) * 0.1),
            'inconsistencies': inconsistencies
        }

    def _is_matching(self, prediction: Any, observation: Any) -> bool:
        """检查预测和观察是否匹配"""
        if isinstance(prediction, dict) and isinstance(observation, dict):
            return prediction.get('target') == observation.get('target')
        return str(prediction) == str(observation)

    def _calculate_consistency(self, prediction: Dict, observation: Dict) -> float:
        """计算一致性分数"""
        pred_value = prediction.get('value', 0)
        obs_value = observation.get('value', 0)

        if pred_value == 0:
            return 1.0 if obs_value == 0 else 0.0

        diff = abs(pred_value - obs_value) / abs(pred_value)
        return max(0.0, 1.0 - diff)

    def get_analysis_summary(self) -> Dict[str, Any]:
        """获取分析摘要"""
        return {
            'total_analyses': len(self.analysis_history),
            'active_insights': len(self.active_insights),
            'scale_distribution': self._calculate_scale_distribution(),
            'recent_insights': [
                {
                    'id': i.title,
                    'confidence': i.confidence,
                    'type': i.synthesis_type
                }
                for i in self.active_insights[-5:]
            ]
        }

    def _calculate_scale_distribution(self) -> Dict[str, int]:
        """计算尺度分布"""
        distribution = {'micro': 0, 'meso': 0, 'macro': 0}

        for insight in self.active_insights:
            if insight.synthesis_type == 'micro_focus':
                distribution['micro'] += 1
            elif insight.synthesis_type == 'macro_focus':
                distribution['macro'] += 1
            else:
                distribution['meso'] += 1

        return distribution

    def clear_history(self) -> None:
        """清除历史记录"""
        self.analysis_history.clear()
        self.active_insights.clear()
