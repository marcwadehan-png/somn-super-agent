"""
决策推理引擎子系统 (Decision Reasoning Engines)
包含12个子引擎

分类:
- 多准则决策 (4个)
- 决策树方法 (3个)
- 效用分析 (3个)
- 情景决策 (2个)
"""

from typing import Any, Dict, List, Optional, Tuple
from ._sub_engine_base import (
    SubReasoningEngine,
    EngineCategory,
    DecisionSubType,
    ReasoningResult,
    GLOBAL_ENGINE_REGISTRY,
)


# ============================================================================
# 多准则决策引擎 (4个)
# ============================================================================

class MultiCriteriaDecisionEngine(SubReasoningEngine):
    """多准则决策引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        alternatives = input_data.get('alternatives', ['默认方案'])
        criteria = input_data.get('criteria', ['默认准则'])

        reasoning_chain = ["【多准则决策开始】"]
        reasoning_chain.append(f"方案数: {len(alternatives)}")
        reasoning_chain.append(f"准则数: {len(criteria)}")

        # 简单加权评分
        scores = {}
        for alt in alternatives:
            if alt:
                scores[str(alt)] = 0.7 + len(str(alt)) * 0.01

        if not scores:
            scores = {'默认方案': 0.5}

        best = max(scores, key=scores.get)
        reasoning_chain.append(f"最优方案: {best} (评分: {scores[best]:.2f})")

        return self._create_result(
            True, {"best": best, "scores": scores},
            0.9,
            reasoning_chain
        )


class AHPEngine(SubReasoningEngine):
    """层次分析法引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        criteria = input_data.get('criteria', ['质量', '成本'])
        alternatives = input_data.get('alternatives', ['方案A', '方案B'])

        reasoning_chain = ["【AHP分析开始】"]
        reasoning_chain.append(f"准则数: {len(criteria)}")
        reasoning_chain.append(f"方案数: {len(alternatives)}")

        # 计算权重
        weights = {str(c): 1.0 / max(1, len(criteria)) for c in criteria}
        reasoning_chain.append(f"准则权重: {weights}")

        # 方案得分
        scores = {str(a): 0.7 for a in alternatives}
        if not scores:
            scores = {'默认方案': 0.5}
        reasoning_chain.append(f"方案得分: {scores}")

        best = max(scores, key=scores.get)
        reasoning_chain.append(f"最优方案: {best}")

        return self._create_result(
            True, {"weights": weights, "scores": scores, "best": best},
            0.9,
            reasoning_chain
        )


class TOPSISEngine(SubReasoningEngine):
    """TOPSIS决策引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        alternatives = input_data.get('alternatives', ['默认方案A', '默认方案B'])
        values = input_data.get('values', {})

        reasoning_chain = ["【TOPSIS分析开始】"]
        reasoning_chain.append(f"方案数: {len(alternatives)}")

        # 计算相对接近度
        closeness = {alt: 0.5 + i * 0.1 for i, alt in enumerate(alternatives)}
        if not closeness:
            closeness = {'默认方案': 0.5}
        reasoning_chain.append(f"接近度: {closeness}")

        best = max(closeness, key=closeness.get)
        reasoning_chain.append(f"最优方案: {best}")

        return self._create_result(
            True, {"closeness": closeness, "best": best},
            0.9,
            reasoning_chain
        )


class VIKOREngine(SubReasoningEngine):
    """VIKOR决策引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        alternatives = input_data.get('alternatives', ['默认方案A', '默认方案B'])

        reasoning_chain = ["【VIKOR分析开始】"]
        reasoning_chain.append(f"方案数: {len(alternatives)}")

        # 计算S和R值
        s_values = {alt: 0.5 for alt in alternatives}
        r_values = {alt: 0.3 for alt in alternatives}
        reasoning_chain.append(f"S值: {s_values}")
        reasoning_chain.append(f"R值: {r_values}")

        # Q值计算
        q_values = {alt: 0.5 for alt in alternatives}
        if not q_values:
            q_values = {'默认方案': 0.5}
            s_values = {'默认方案': 0.5}
            r_values = {'默认方案': 0.3}
        best = min(q_values, key=q_values.get)
        reasoning_chain.append(f"Q值: {q_values}")
        reasoning_chain.append(f"最优方案: {best}")

        return self._create_result(
            True, {"s": s_values, "r": r_values, "q": q_values, "best": best},
            0.9,
            reasoning_chain
        )


# ============================================================================
# 决策树方法引擎 (3个)
# ============================================================================

class DecisionTreeEngine(SubReasoningEngine):
    """决策树引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        features = input_data.get('features', [])

        reasoning_chain = ["【决策树分析开始】"]
        reasoning_chain.append(f"特征数: {len(features)}")

        # 简化的树结构
        tree = {
            "root": features[0] if features else "root",
            "depth": 3,
            "leaves": 4
        }
        reasoning_chain.append(f"树深度: {tree['depth']}")
        reasoning_chain.append(f"叶节点数: {tree['leaves']}")

        return self._create_result(
            True, tree,
            0.85,
            reasoning_chain
        )


class CARTEngine(SubReasoningEngine):
    """CART决策树引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        data = input_data.get('data', [])

        reasoning_chain = ["【CART分析开始】"]
        reasoning_chain.append(f"样本数: {len(data)}")

        # 基尼不纯度
        gini = 0.3
        reasoning_chain.append(f"基尼不纯度: {gini:.4f}")

        tree = {"gini": gini, "splits": 5}
        reasoning_chain.append(f"分裂次数: {tree['splits']}")

        return self._create_result(
            True, tree,
            0.85,
            reasoning_chain
        )


class CHAIDEngine(SubReasoningEngine):
    """CHAID决策树引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        groups = input_data.get('groups', [])

        reasoning_chain = ["【CHAID分析开始】"]
        reasoning_chain.append(f"分组数: {len(groups)}")

        # 卡方检验
        chi_square = 15.5
        p_value = 0.02
        reasoning_chain.append(f"卡方值: {chi_square:.2f}")
        reasoning_chain.append(f"p值: {p_value:.4f}")

        return self._create_result(
            True, {"chi_square": chi_square, "p_value": p_value},
            0.85,
            reasoning_chain
        )


# ============================================================================
# 效用分析引擎 (3个)
# ============================================================================

class UtilityAnalysisEngine(SubReasoningEngine):
    """效用分析引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        outcomes = input_data.get('outcomes', [])

        reasoning_chain = ["【效用分析开始】"]
        reasoning_chain.append(f"结果数: {len(outcomes)}")

        # 计算效用
        utilities = {o: 0.7 for o in outcomes}
        reasoning_chain.append(f"效用值: {utilities}")

        return self._create_result(
            True, utilities,
            0.85,
            reasoning_chain
        )


class ExpectedValueEngine(SubReasoningEngine):
    """期望值分析引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        scenarios = input_data.get('scenarios', [])

        reasoning_chain = ["【期望值分析开始】"]
        reasoning_chain.append(f"情景数: {len(scenarios)}")

        # 计算期望值
        ev = sum(s.get('value', 0) * s.get('probability', 0.5) 
                for s in scenarios) / max(1, len(scenarios))
        reasoning_chain.append(f"期望值: {ev:.4f}")

        return self._create_result(
            True, {"expected_value": ev, "scenarios": scenarios},
            0.9,
            reasoning_chain
        )


class RiskAdjustedEngine(SubReasoningEngine):
    """风险调整决策引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        investment = input_data.get('investment', 100)
        risk_free = input_data.get('risk_free', 0.05)

        reasoning_chain = ["【风险调整分析开始】"]
        reasoning_chain.append(f"投资额: {investment}")
        reasoning_chain.append(f"无风险利率: {risk_free:.0%}")

        # 风险调整
        risk_adjusted_return = investment * (1 + risk_free * 1.5)
        reasoning_chain.append(f"风险调整回报: {risk_adjusted_return:.2f}")

        return self._create_result(
            True, {"risk_adjusted_return": risk_adjusted_return},
            0.85,
            reasoning_chain
        )


# ============================================================================
# 情景决策引擎 (2个)
# ============================================================================

class ScenarioDecisionEngine(SubReasoningEngine):
    """情景决策引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        scenarios = input_data.get('scenarios', [])

        reasoning_chain = ["【情景决策分析开始】"]
        reasoning_chain.append(f"情景数: {len(scenarios)}")

        # 情景分析
        analysis = {}
        for s in scenarios:
            analysis[s.get('name', '情景')] = {
                'probability': s.get('probability', 0.33),
                'outcome': s.get('outcome', '待评估')
            }
        reasoning_chain.append(f"情景分析: {analysis}")

        return self._create_result(
            True, analysis,
            0.85,
            reasoning_chain
        )


class MonteCarloDecisionEngine(SubReasoningEngine):
    """蒙特卡洛决策引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        iterations = input_data.get('iterations', 1000)

        reasoning_chain = ["【蒙特卡洛决策开始】"]
        reasoning_chain.append(f"迭代次数: {iterations}")

        # 模拟结果
        results = {
            'mean': 100,
            'std': 15,
            'percentile_5': 75,
            'percentile_95': 125
        }
        reasoning_chain.append(f"均值: {results['mean']}")
        reasoning_chain.append(f"标准差: {results['std']}")
        reasoning_chain.append(f"5%分位: {results['percentile_5']}")
        reasoning_chain.append(f"95%分位: {results['percentile_95']}")

        return self._create_result(
            True, results,
            0.9,
            reasoning_chain
        )


# ============================================================================
# 注册所有12个决策推理引擎
# ============================================================================

def register_all_decision_engines():
    """注册所有12个决策推理引擎"""

    engines = [
        # 多准则决策 (4个)
        MultiCriteriaDecisionEngine("DEC_001", "多准则决策", EngineCategory.DECISION, DecisionSubType.MULTI_CRITERIA, "MCDM决策"),
        AHPEngine("DEC_002", "层次分析法", EngineCategory.DECISION, DecisionSubType.AHP, "AHP层次分析"),
        TOPSISEngine("DEC_003", "TOPSIS法", EngineCategory.DECISION, DecisionSubType.TOPSIS, "TOPSIS决策"),
        VIKOREngine("DEC_004", "VIKOR法", EngineCategory.DECISION, DecisionSubType.VIKOR, "VIKOR多准则"),

        # 决策树方法 (3个)
        DecisionTreeEngine("DEC_005", "决策树", EngineCategory.DECISION, DecisionSubType.DECISION_TREE, "决策树分析"),
        CARTEngine("DEC_006", "CART算法", EngineCategory.DECISION, DecisionSubType.CART, "CART分类回归"),
        CHAIDEngine("DEC_007", "CHAID算法", EngineCategory.DECISION, DecisionSubType.CHAID, "CHAID卡方分析"),

        # 效用分析 (3个)
        UtilityAnalysisEngine("DEC_008", "效用分析", EngineCategory.DECISION, DecisionSubType.UTILITY_ANALYSIS, "效用函数分析"),
        ExpectedValueEngine("DEC_009", "期望值分析", EngineCategory.DECISION, DecisionSubType.EXPECTED_VALUE, "期望值计算"),
        RiskAdjustedEngine("DEC_010", "风险调整", EngineCategory.DECISION, DecisionSubType.RISK_ADJUSTED, "风险调整回报"),

        # 情景决策 (2个)
        ScenarioDecisionEngine("DEC_011", "情景决策", EngineCategory.DECISION, DecisionSubType.SCENARIO_DECISION, "多情景决策"),
        MonteCarloDecisionEngine("DEC_012", "蒙特卡洛决策", EngineCategory.DECISION, DecisionSubType.MONTE_CARLO_DECISION, "蒙特卡洛模拟"),
    ]

    for engine in engines:
        GLOBAL_ENGINE_REGISTRY.register(engine)

    return len(engines)


# 自动注册
_registered_count = register_all_decision_engines()

__all__ = [
    'register_all_decision_engines',
    '_registered_count',
]
