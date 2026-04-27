"""数学智慧核心 - 主引擎"""

from typing import Dict, List, Any, Tuple

from ._mw_enums import SequenceType
from ._mw_dataclasses import MathWisdomInsight, OptimizationResult
from ._mw_sequence import SequenceAnalyzer
from ._mw_graph import GraphAnalyzer
from ._mw_combinatorial import CombinatorialOptimizer
from ._mw_probability import DiscreteProbabilityEngine

__all__ = [
    'analyze_growth_trend',
    'analyze_network',
    'evaluate_risk_probability',
    'generate_recommendations',
]

class MathWisdomCore:
    """
    数学智慧核心引擎
    整合数列分析,图论分析,组合优化,概率推断
    提供企业增长决策的数学支持
    """
    
    def __init__(self):
        self.sequence_analyzer = SequenceAnalyzer()
        self.graph_analyzer = GraphAnalyzer()
        self.combinatorial_optimizer = CombinatorialOptimizer()
        self.probability_engine = DiscreteProbabilityEngine()
    
    def analyze_growth_trend(self, historical_data: List[float]) -> MathWisdomInsight:
        """
        分析增长趋势
        
        Args:
            historical_data: 历史数据
            
        Returns:
            数学智慧洞察
        """
        analysis = self.sequence_analyzer.analyze_sequence(historical_data)
        
        # 根据分析结果生成洞察
        if analysis.sequence_type == SequenceType.ARITHMETIC:
            return MathWisdomInsight(
                insight_type="trend_analysis",
                title="线性增长模式识别",
                description=analysis.pattern_description,
                mathematical_basis="等差数列:aₙ = a₁ + (n-1)d",
                application_scenario="稳定线性增长的业务指标",
                confidence=analysis.confidence,
                recommendations=[
                    f"当前增长量:每周期+{analysis.common_diff:.2f}",
                    "建议保持当前增长策略",
                    "注意增长速度的边际效应"
                ]
            )
        
        elif analysis.sequence_type == SequenceType.GEOMETRIC:
            growth_rate = (analysis.common_ratio - 1) * 100
            return MathWisdomInsight(
                insight_type="trend_analysis",
                title="指数增长模式识别",
                description=f"当前增长率:{growth_rate:.1f}%",
                mathematical_basis="等比数列:aₙ = a₁ × q^(n-1)",
                application_scenario="快速增长阶段的业务指标",
                confidence=analysis.confidence,
                recommendations=[
                    "指数增长不可持续,注意增长天花板",
                    f"预测下期值:{analysis.next_value:.2f}",
                    "关注增长质量而非单纯增长量"
                ]
            )
        
        elif analysis.sequence_type == SequenceType.FIBONACCI:
            return MathWisdomInsight(
                insight_type="trend_analysis",
                title="斐波那契增长模式",
                description="呈现斐波那契级增长特征",
                mathematical_basis="斐波那契:Fₙ = Fₙ₋₁ + Fₙ₋₂,趋向黄金分割",
                application_scenario="自然增长,递进式发展",
                confidence=analysis.confidence,
                recommendations=[
                    "斐波那契增长是健康的增长模式",
                    f"预测下期值:{analysis.next_value:.2f}",
                    "这种增长模式通常伴随阶段性跃升"
                ]
            )
        
        return MathWisdomInsight(
            insight_type="trend_analysis",
            title="复杂增长模式",
            description="数据呈现复杂模式,需要更多数据或非线性模型",
            mathematical_basis="可能需要多项式或分段模型",
            application_scenario="数据波动较大或有多重周期",
            confidence=analysis.confidence,
            recommendations=[
                "收集更多数据点",
                "考虑季节性因素",
                "考虑分段分析"
            ]
        )
    
    def analyze_network(self, edges: List[Tuple[str, str]], 
                       weighted: bool = False) -> MathWisdomInsight:
        """
        分析网络关系
        
        Args:
            edges: 边列表 [(from, to), ...]
            weighted: 是否加权
            
        Returns:
            数学智慧洞察
        """
        # 构建图
        self.graph_analyzer = GraphAnalyzer()
        self.graph_analyzer.is_directed = True
        
        for edge in edges:
            if len(edge) == 3:
                self.graph_analyzer.add_edge(edge[0], edge[1], edge[2])
            else:
                self.graph_analyzer.add_edge(edge[0], edge[1])
        
        analysis = self.graph_analyzer.analyze()
        
        # 找出关键节点
        key_nodes = sorted(analysis.centrality.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return MathWisdomInsight(
            insight_type="network_analysis",
            title=f"网络结构分析:{analysis.node_count}个节点,{analysis.edge_count}条边",
            description=f"网络密度:{analysis.density:.2f},{'连通' if analysis.is_connected else '不连通'}",
            mathematical_basis="图论:节点-边结构,连通性,中心性分析",
            application_scenario="实体关系分析,供应链优化,信息传播",
            confidence=0.8,
            recommendations=[
                f"关键节点:{', '.join([n[0] for n in key_nodes])}",
                f"建议加强{'高度中心性' if analysis.density < 0.3 else '节点间连接'}节点的作用",
                "考虑网络优化以提高整体效率"
            ]
        )
    
    def evaluate_risk_probability(self, success_rate: float, 
                                evidence: float) -> Any:
        """
        风险概率评估
        
        Args:
            success_rate: 历史成功率(先验)
            evidence: 新证据的强度
            
        Returns:
            概率分析
        """
        return self.probability_engine.bayesian_inference(
            prior=success_rate,
            likelihood=evidence,
            evidence=0.5  # 简化
        )
    
    def generate_recommendations(self, data: List[float], 
                                options: List[Dict]) -> OptimizationResult:
        """
        生成决策建议
        
        Args:
            data: 历史数据
            options: 可选方案
            
        Returns:
            优化结果
        """
        # 分析趋势
        trend_insight = self.analyze_growth_trend(data)
        
        # 评估方案
        result = self.combinatorial_optimizer.evaluate_plan_options(options, {})
        
        # 综合建议
        if trend_insight.confidence > 0.8:
            if "指数" in trend_insight.description:
                result.optimal_choice = "扩展方案" if "建议加强" in trend_insight.recommendations[0] else "稳健方案"
        
        return result
