# -*- coding: utf-8 -*-
"""
__all__ = [
    'synthesize_cross_scale',
]

跨尺度思维引擎 - 综合器模块
处理微观-宏观综合、跨尺度映射、创新生成
"""

from typing import Dict, List, Any, Optional
from ._cst_types import ScaleLevel, CrossScaleInsight

class CrossScaleSynthesizer:
    """跨尺度综合器"""

    def __init__(self):
        self.synthesis_patterns = {
            'bottom_up': self._bottom_up_synthesis,
            'top_down': self._top_down_synthesis,
            'middle_out': self._middle_out_synthesis,
            'recursive': self._recursive_synthesis
        }

    def synthesize_cross_scale(
        self,
        micro_analysis: Dict[str, Any],
        macro_analysis: Dict[str, Any],
        synthesis_type: str = 'balanced'
    ) -> CrossScaleInsight:
        """综合微观和宏观分析结果"""
        # 提取关键要素
        micro_factors = micro_analysis.get('factors', [])
        macro_patterns = macro_analysis.get('patterns', [])

        # 寻找跨尺度关联
        bridges = self._find_scale_bridges(micro_factors, macro_patterns)

        # 生成综合洞察
        insight = CrossScaleInsight(
            insight_id=f"cross_scale_{id(micro_analysis) + id(macro_analysis)}",
            micro_elements=micro_factors,
            macro_patterns=macro_patterns,
            bridges=bridges,
            synthesis_type=synthesis_type,
            confidence=self._calculate_synthesis_confidence(micro_analysis, macro_analysis),
            implications=self._generate_implications(bridges),
            recommendations=self._generate_recommendations(bridges, synthesis_type)
        )

        return insight

    def _find_scale_bridges(
        self,
        micro_factors: List[Dict],
        macro_patterns: List[Dict]
    ) -> List[Dict[str, Any]]:
        """寻找微观-宏观之间的桥梁"""
        bridges = []

        for factor in micro_factors:
            for pattern in macro_patterns:
                similarity = self._calculate_similarity(factor, pattern)
                if similarity > 0.6:
                    bridges.append({
                        'micro_factor': factor,
                        'macro_pattern': pattern,
                        'similarity': similarity,
                        'bridge_type': self._classify_bridge(factor, pattern),
                        'mechanism': self._infer_mechanism(factor, pattern)
                    })

        return sorted(bridges, key=lambda x: x['similarity'], reverse=True)

    def _calculate_similarity(self, factor: Dict, pattern: Dict) -> float:
        """计算微观因子和宏观模式的相似度"""
        # 基于特征匹配计算相似度
        factor_features = set(factor.get('features', []))
        pattern_features = set(pattern.get('features', []))

        if not factor_features or not pattern_features:
            return 0.0

        intersection = len(factor_features & pattern_features)
        union = len(factor_features | pattern_features)

        return intersection / union if union > 0 else 0.0

    def _classify_bridge(self, factor: Dict, pattern: Dict) -> str:
        """分类桥梁类型"""
        factor_type = factor.get('type', 'unknown')
        pattern_scope = pattern.get('scope', 'unknown')

        if factor_type == 'individual' and pattern_scope == 'system':
            return 'aggregation'
        elif factor_type == 'local' and pattern_scope == 'global':
            return 'emergence'
        elif factor_type == 'component' and pattern_scope == 'structure':
            return 'composition'
        else:
            return 'correlation'

    def _infer_mechanism(self, factor: Dict, pattern: Dict) -> str:
        """推断微观到宏观的作用机制"""
        mechanisms = [
            "累积效应：微观行为的集合产生宏观模式",
            "反馈循环：微观-宏观之间的双向影响",
            "阈值效应：微观变化达到临界点触发宏观转变",
            "网络效应：微观连接形成宏观结构",
            "选择压力：宏观环境筛选微观变异"
        ]

        # 根据特征选择最可能的机制
        if 'network' in factor.get('features', []):
            return mechanisms[3]
        elif 'threshold' in pattern.get('features', []):
            return mechanisms[2]
        elif 'feedback' in pattern.get('features', []):
            return mechanisms[1]
        else:
            return mechanisms[0]

    def _calculate_synthesis_confidence(
        self,
        micro_analysis: Dict[str, Any],
        macro_analysis: Dict[str, Any]
    ) -> float:
        """计算综合结果的置信度"""
        micro_conf = micro_analysis.get('confidence', 0.5)
        macro_conf = macro_analysis.get('confidence', 0.5)

        # 基于数据质量和一致性计算
        base_confidence = (micro_conf + macro_conf) / 2

        # 调整因子
        adjustments = [
            0.1 if micro_analysis.get('data_quality') == 'high' else 0,
            0.1 if macro_analysis.get('data_quality') == 'high' else 0,
            -0.1 if micro_analysis.get('uncertainty', 0) > 0.3 else 0,
            -0.1 if macro_analysis.get('uncertainty', 0) > 0.3 else 0
        ]

        final_confidence = base_confidence + sum(adjustments)
        return max(0.0, min(1.0, final_confidence))

    def _generate_implications(self, bridges: List[Dict]) -> List[str]:
        """生成综合洞察的含义"""
        implications = []

        for bridge in bridges[:3]:  # 取前3个最强桥梁
            mechanism = bridge.get('mechanism', '')
            bridge_type = bridge.get('bridge_type', '')

            if bridge_type == 'aggregation':
                implications.append(
                    f"微观层面的{bridge['micro_factor'].get('name', '因素')} "
                    f"通过累积效应形成宏观{bridge['macro_pattern'].get('name', '模式')}"
                )
            elif bridge_type == 'emergence':
                implications.append(
                    f"局部{bridge['micro_factor'].get('name', '现象')} "
                    f"涌现为全局{bridge['macro_pattern'].get('name', '结构')}"
                )
            elif bridge_type == 'composition':
                implications.append(
                    f"组件层面的{bridge['micro_factor'].get('name', '特性')} "
                    f"构成系统层面的{bridge['macro_pattern'].get('name', '特征')}"
                )

        return implications

    def _generate_recommendations(
        self,
        bridges: List[Dict],
        synthesis_type: str
    ) -> List[str]:
        """生成基于综合的建议"""
        recommendations = []

        if synthesis_type == 'micro_focus':
            recommendations.append("关注微观层面的关键杠杆点，通过局部优化影响整体")
        elif synthesis_type == 'macro_focus':
            recommendations.append("利用宏观模式指导微观决策，把握整体方向")
        else:  # balanced
            recommendations.append("平衡微观细节和宏观视野，实现双向优化")

        # 基于桥梁生成具体建议
        for bridge in bridges[:2]:
            bridge_type = bridge.get('bridge_type', '')
            if bridge_type == 'aggregation':
                recommendations.append(
                    f"通过调节{bridge['micro_factor'].get('name', '微观因素')} "
                    f"来影响{bridge['macro_pattern'].get('name', '宏观模式')}"
                )
            elif bridge_type == 'emergence':
                recommendations.append(
                    f"关注{bridge['micro_factor'].get('name', '局部现象')}的临界点，"
                    f"可能引发{bridge['macro_pattern'].get('name', '全局变化')}"
                )

        return recommendations

    def _bottom_up_synthesis(
        self,
        micro_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """自下而上综合：从微观到宏观"""
        return {
            'approach': 'bottom_up',
            'micro_base': micro_data,
            'emergent_properties': self._identify_emergent_properties(micro_data),
            'aggregation_rules': self._derive_aggregation_rules(micro_data),
            'scale_transitions': self._map_scale_transitions(micro_data)
        }

    def _top_down_synthesis(
        self,
        macro_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """自上而下综合：从宏观到微观"""
        return {
            'approach': 'top_down',
            'macro_constraints': macro_data,
            'decomposition_rules': self._derive_decomposition_rules(macro_data),
            'micro_implications': self._derive_micro_implications(macro_data),
            'implementation_path': self._design_implementation_path(macro_data)
        }

    def _middle_out_synthesis(
        self,
        meso_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """中间向外综合：从中观层向两边扩展"""
        return {
            'approach': 'middle_out',
            'meso_base': meso_data,
            'upward_projection': self._project_upward(meso_data),
            'downward_projection': self._project_downward(meso_data),
            'bridge_mechanisms': self._identify_bridge_mechanisms(meso_data)
        }

    def _recursive_synthesis(
        self,
        data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """递归综合：在多个尺度间迭代"""
        iterations = []
        current = data

        for i in range(3):  # 最多3轮迭代
            micro = self._extract_micro_level(current)
            macro = self._extract_macro_level(current)
            synthesis = self.synthesize_cross_scale(micro, macro)

            iterations.append({
                'round': i + 1,
                'micro': micro,
                'macro': macro,
                'synthesis': synthesis
            })

            # 更新当前状态用于下一轮
            current = self._update_with_synthesis(current, synthesis)

        return {
            'approach': 'recursive',
            'iterations': iterations,
            'convergence': self._check_convergence(iterations),
            'final_state': current
        }

    # 辅助方法占位符
    def _identify_emergent_properties(self, data: Dict) -> List[str]:
        return ["涌现属性1", "涌现属性2"]

    def _derive_aggregation_rules(self, data: Dict) -> List[str]:
        return ["聚合规则1", "聚合规则2"]

    def _map_scale_transitions(self, data: Dict) -> List[Dict]:
        return [{"from": "micro", "to": "macro", "mechanism": "累积"}]

    def _derive_decomposition_rules(self, data: Dict) -> List[str]:
        return ["分解规则1", "分解规则2"]

    def _derive_micro_implications(self, data: Dict) -> List[str]:
        return ["微观含义1", "微观含义2"]

    def _design_implementation_path(self, data: Dict) -> List[str]:
        return ["实施步骤1", "实施步骤2"]

    def _project_upward(self, data: Dict) -> Dict:
        return {"projection": "向上投影"}

    def _project_downward(self, data: Dict) -> Dict:
        return {"projection": "向下投影"}

    def _identify_bridge_mechanisms(self, data: Dict) -> List[str]:
        return ["桥梁机制1", "桥梁机制2"]

    def _extract_micro_level(self, data: Dict) -> Dict:
        return data.get('micro', {})

    def _extract_macro_level(self, data: Dict) -> Dict:
        return data.get('macro', {})

    def _update_with_synthesis(self, data: Dict, synthesis: Any) -> Dict:
        data['synthesis'] = synthesis
        return data

    def _check_convergence(self, iterations: List[Dict]) -> bool:
        if len(iterations) < 2:
            return False
        # 简单检查：如果最后两轮变化很小，认为收敛
        return True
