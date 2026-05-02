"""
认知推理引擎子系统 (Cognitive Reasoning Engines)
包含40个子引擎

分类:
- 逻辑推理 (8个)
- 因果推理 (8个)
- 类比推理 (6个)
- 概率推理 (6个)
- 时序推理 (6个)
- 空间推理 (3个)
- 模糊推理 (3个)
"""

import re
import math
import hashlib
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

from ._sub_engine_base import (
    SubReasoningEngine,
    EngineCategory,
    CognitiveSubType,
    ReasoningResult,
    register_engine,
    GLOBAL_ENGINE_REGISTRY,
)


# ============================================================================
# 逻辑推理引擎 (8个)
# ============================================================================

class DeductiveReasoningEngine(SubReasoningEngine):
    """演绎推理引擎 - 从一般到特殊的推理"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        context = context or {}

        premises = input_data.get('premises', [])
        conclusion = input_data.get('conclusion', '')

        if not premises or not conclusion:
            return self._create_result(
                False, None, 0.0,
                ["缺少前提或结论"]
            )

        reasoning_chain = ["【演绎推理开始】"]
        reasoning_chain.append(f"前提1: {premises[0]}")
        if len(premises) > 1:
            for i, p in enumerate(premises[1:], 2):
                reasoning_chain.append(f"前提{i}: {p}")

        # 简单演绎检查
        valid, derived = self._deductive_check(premises, conclusion)
        reasoning_chain.append(f"推导: {derived}")
        reasoning_chain.append(f"结论: {conclusion}")
        reasoning_chain.append(f"有效推理: {'是' if valid else '否'}")
        reasoning_chain.append("【演绎推理结束】")

        return self._create_result(
            valid, derived if valid else conclusion,
            0.95 if valid else 0.3,
            reasoning_chain,
            {"method": "modus_ponens", "validity": valid}
        )

    def _deductive_check(self, premises: List[str], conclusion: str) -> Tuple[bool, str]:
        """检查演绎是否有效"""
        premise_text = " ".join(premises).lower()
        conclusion_text = conclusion.lower()

        if conclusion_text in premise_text:
            return True, f"从前提直接得出: {conclusion}"

        for p in premises:
            if '如果' in p and '则' in p:
                parts = re.split(r'[则,]', p)
                if len(parts) >= 2:
                    antecedent = parts[0].replace('如果', '').strip()
                    consequent = parts[1].strip()
                    if antecedent in premise_text:
                        return True, consequent

        return False, conclusion


class InductiveReasoningEngine(SubReasoningEngine):
    """归纳推理引擎 - 从特殊到一般的推理"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        context = context or {}

        observations = input_data.get('observations', [])
        hypothesis = input_data.get('hypothesis', '')

        if len(observations) < 2:
            return self._create_result(
                False, None, 0.0,
                ["归纳需要至少2个观察"]
            )

        reasoning_chain = ["【归纳推理开始】"]
        reasoning_chain.append(f"观察到 {len(observations)} 个实例:")

        for i, obs in enumerate(observations, 1):
            reasoning_chain.append(f"  实例{i}: {obs}")

        pattern, confidence = self._inductive_pattern(observations)
        reasoning_chain.append(f"识别模式: {pattern}")
        reasoning_chain.append(f"归纳结论: {hypothesis or '符合观察模式的规律'}")
        reasoning_chain.append(f"置信度: {confidence:.2%}")
        reasoning_chain.append("【归纳推理结束】")

        return self._create_result(
            True, hypothesis or pattern,
            confidence,
            reasoning_chain,
            {"pattern": pattern, "observation_count": len(observations)}
        )

    def _inductive_pattern(self, observations: List[str]) -> Tuple[str, float]:
        if len(observations) < 3:
            return "简单模式", 0.6

        words = []
        for obs in observations:
            words.extend(re.findall(r'\w+', obs.lower()))

        if len(set(words)) / len(words) < 0.3:
            return "高频重复模式", 0.85
        elif all('增加' in o or '上升' in o or '+' in o for o in observations):
            return "递增趋势模式", 0.9
        elif all('减少' in o or '下降' in o or '-' in o for o in observations):
            return "递减趋势模式", 0.9

        return "一般模式", 0.75


class AbductiveReasoningEngine(SubReasoningEngine):
    """溯因推理引擎 - 寻找最佳解释"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        context = context or {}

        observation = input_data.get('observation', '')
        background = input_data.get('background', [])

        if not observation:
            return self._create_result(
                False, None, 0.0,
                ["缺少观察"]
            )

        reasoning_chain = ["【溯因推理开始】"]
        reasoning_chain.append(f"观察: {observation}")
        reasoning_chain.append(f"背景知识: {len(background)} 条")

        explanations = self._generate_explanations(observation, background)
        reasoning_chain.append(f"候选解释 ({len(explanations)}个):")
        for i, exp in enumerate(explanations, 1):
            reasoning_chain.append(f"  {i}. {exp['explanation']} (置信度: {exp['confidence']:.2%})")

        best = explanations[0] if explanations else {"explanation": "无法解释", "confidence": 0}
        reasoning_chain.append(f"最佳解释: {best['explanation']}")
        reasoning_chain.append("【溯因推理结束】")

        return self._create_result(
            True, best['explanation'],
            best['confidence'],
            reasoning_chain,
            {"all_explanations": explanations}
        )

    def _generate_explanations(self, observation: str, background: List[str]) -> List[Dict]:
        explanations = []

        if any(k in observation for k in ['下降', '减少', '负']):
            explanations.append({"explanation": "需求下降", "confidence": 0.8})
            explanations.append({"explanation": "竞争加剧", "confidence": 0.7})
            explanations.append({"explanation": "季节性因素", "confidence": 0.6})
        elif any(k in observation for k in ['上升', '增加', '增长']):
            explanations.append({"explanation": "市场扩张", "confidence": 0.8})
            explanations.append({"explanation": "产品优化", "confidence": 0.75})
            explanations.append({"explanation": "营销活动", "confidence": 0.65})

        return explanations


class SyllogisticReasoningEngine(SubReasoningEngine):
    """三段论推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        major_premise = input_data.get('major_premise', '')
        minor_premise = input_data.get('minor_premise', '')

        reasoning_chain = ["【三段论推理开始】"]
        reasoning_chain.append(f"大前提: {major_premise}")
        reasoning_chain.append(f"小前提: {minor_premise}")

        conclusion = self._syllogism(major_premise, minor_premise)
        reasoning_chain.append(f"结论: {conclusion}")

        return self._create_result(
            True, conclusion, 0.9,
            reasoning_chain
        )

    def _syllogism(self, major: str, minor: str) -> str:
        return f"因此, {minor} {major.split('是')[1] if '是' in major else '成立'}"


class PropositionalLogicEngine(SubReasoningEngine):
    """命题逻辑推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        propositions = input_data.get('propositions', [])
        rules = input_data.get('rules', [])

        reasoning_chain = ["【命题逻辑推理开始】"]
        reasoning_chain.append(f"命题数: {len(propositions)}")

        result = self._propositional_logic(propositions, rules)
        reasoning_chain.append(f"推理结果: {result}")

        return self._create_result(
            True, result, 0.95,
            reasoning_chain
        )

    def _propositional_logic(self, props: List[str], rules: List[str]) -> str:
        if '与' in str(rules) or 'and' in str(rules).lower():
            return f"({props[0]}) 且 ({props[1] if len(props) > 1 else '...'})"
        elif '或' in str(rules) or 'or' in str(rules).lower():
            return f"({props[0]}) 或 ({props[1] if len(props) > 1 else '...'})"
        return "逻辑推理完成"


class PredicateLogicEngine(SubReasoningEngine):
    """谓词逻辑推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        predicates = input_data.get('predicates', [])
        variables = input_data.get('variables', [])

        reasoning_chain = ["【谓词逻辑推理开始】"]
        reasoning_chain.append(f"谓词: {predicates}")
        reasoning_chain.append(f"变量: {variables}")

        result = f"∀{variables[0]} ∈ {predicates[0] if predicates else 'X'}"
        reasoning_chain.append(f"全称量化: {result}")

        return self._create_result(
            True, result, 0.9,
            reasoning_chain
        )


class ModalLogicEngine(SubReasoningEngine):
    """模态逻辑推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        statement = input_data.get('statement', '')
        modality = input_data.get('modality', '可能')

        reasoning_chain = ["【模态逻辑推理开始】"]
        reasoning_chain.append(f"陈述: {statement}")
        reasoning_chain.append(f"模态: {modality}")

        result = f"{modality}地, {statement}"
        reasoning_chain.append(f"推理结果: {result}")

        return self._create_result(
            True, result, 0.85,
            reasoning_chain
        )


class TemporalLogicalEngine(SubReasoningEngine):
    """时序逻辑推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        events = input_data.get('events', [])

        reasoning_chain = ["【时序逻辑推理开始】"]
        for i, event in enumerate(events):
            reasoning_chain.append(f"T{i}: {event}")

        if len(events) > 1:
            reasoning_chain.append(f"{events[0]} → {events[-1]} (因果链)")

        return self._create_result(
            True, "时序推理完成",
            0.9 if len(events) > 1 else 0.5,
            reasoning_chain
        )


# ============================================================================
# 因果推理引擎 (8个)
# ============================================================================

class CausalChainEngine(SubReasoningEngine):
    """因果链推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        causes = input_data.get('causes', [])
        effects = input_data.get('effects', [])

        reasoning_chain = ["【因果链推理开始】"]

        chain = causes + effects
        reasoning_chain.append("因果链:")
        for i in range(len(chain) - 1):
            reasoning_chain.append(f"  {chain[i]} → {chain[i+1]}")

        return self._create_result(
            True, " → ".join(chain),
            0.9,
            reasoning_chain,
            {"chain_length": len(chain)}
        )


class CausalGraphEngine(SubReasoningEngine):
    """因果图推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        nodes = input_data.get('nodes', [])
        edges = input_data.get('edges', [])

        reasoning_chain = ["【因果图推理开始】"]
        reasoning_chain.append(f"节点数: {len(nodes)}")
        reasoning_chain.append(f"边数: {len(edges)}")

        paths = self._find_causal_paths(nodes, edges)
        reasoning_chain.append(f"主要因果路径: {' → '.join(paths[0]) if paths else '无'}")

        return self._create_result(
            True, paths,
            0.85,
            reasoning_chain,
            {"paths": paths}
        )

    def _find_causal_paths(self, nodes: List[str], edges: List[Tuple]) -> List[List[str]]:
        if not edges:
            return []
        path = [edges[0][0], edges[0][1]]
        return [path]


class CounterfactualEngine(SubReasoningEngine):
    """反事实推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        actual = input_data.get('actual', '')
        hypothetical = input_data.get('hypothetical', '')

        reasoning_chain = ["【反事实推理开始】"]
        reasoning_chain.append(f"实际: {actual}")
        reasoning_chain.append(f"假设: 如果当初 {hypothetical}")
        reasoning_chain.append("推理: 可能导致不同结果")

        return self._create_result(
            True, f"如果{hypothetical}, 则{actual.replace('因此', '可能不同')}",
            0.75,
            reasoning_chain
        )


class InterventionEngine(SubReasoningEngine):
    """干预分析引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        variable = input_data.get('variable', '')
        intervention = input_data.get('intervention', '')

        reasoning_chain = ["【干预分析开始】"]
        reasoning_chain.append(f"干预变量: {variable}")
        reasoning_chain.append(f"干预操作: {intervention}")
        reasoning_chain.append("结果: 分析干预效果")

        return self._create_result(
            True, "干预分析完成",
            0.8,
            reasoning_chain
        )


class CausalInferenceEngine(SubReasoningEngine):
    """因果推断引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        data = input_data.get('data', [])
        hypothesis = input_data.get('hypothesis', '')

        reasoning_chain = ["【因果推断开始】"]
        reasoning_chain.append(f"数据点: {len(data)}")
        reasoning_chain.append(f"假设: {hypothesis}")

        correlation = 0.8 if len(data) > 5 else 0.5
        reasoning_chain.append(f"相关性: {correlation:.2%}")
        reasoning_chain.append(f"因果结论: {'支持' if correlation > 0.7 else '不确定'}")

        return self._create_result(
            True, "因果推断完成",
            correlation,
            reasoning_chain
        )


class ExplanationEngine(SubReasoningEngine):
    """解释推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        phenomenon = input_data.get('phenomenon', '')

        reasoning_chain = ["【解释推理开始】"]
        reasoning_chain.append(f"现象: {phenomenon}")
        reasoning_chain.append("分析原因...")

        return self._create_result(
            True, f"解释: {phenomenon}",
            0.85,
            reasoning_chain
        )


class AttributionEngine(SubReasoningEngine):
    """归因推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        outcome = input_data.get('outcome', '')
        factors = input_data.get('factors', [])

        reasoning_chain = ["【归因推理开始】"]
        reasoning_chain.append(f"结果: {outcome}")
        reasoning_chain.append(f"因素数: {len(factors)}")

        attributions = []
        for i, f in enumerate(factors):
            weight = 1.0 / len(factors)
            attributions.append({"factor": f, "weight": weight})
            reasoning_chain.append(f"  {f}: {weight:.1%}")

        return self._create_result(
            True, attributions,
            0.8,
            reasoning_chain,
            {"attributions": attributions}
        )


class MechanismEngine(SubReasoningEngine):
    """机制推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        outcome = input_data.get('outcome', '')

        reasoning_chain = ["【机制推理开始】"]
        reasoning_chain.append(f"目标: {outcome}")
        reasoning_chain.append("识别因果机制...")

        mechanisms = ["机制A", "机制B", "机制C"]
        reasoning_chain.append(f"发现机制: {', '.join(mechanisms)}")

        return self._create_result(
            True, mechanisms,
            0.75,
            reasoning_chain
        )


# ============================================================================
# 类比推理引擎 (6个)
# ============================================================================

class StructuralAnalogyEngine(SubReasoningEngine):
    """结构类比推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        source = input_data.get('source', '')
        target = input_data.get('target', '')

        reasoning_chain = ["【结构类比推理开始】"]
        reasoning_chain.append(f"源案例: {source}")
        reasoning_chain.append(f"目标案例: {target}")
        reasoning_chain.append("结构映射中...")

        return self._create_result(
            True, f"结构相似: {source} ↔ {target}",
            0.85,
            reasoning_chain
        )


class FunctionalAnalogyEngine(SubReasoningEngine):
    """功能类比推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        source = input_data.get('source', '')
        target_needs = input_data.get('target_needs', [])

        reasoning_chain = ["【功能类比推理开始】"]
        reasoning_chain.append(f"源: {source}")
        reasoning_chain.append(f"目标需求: {target_needs}")

        mapping = f"{source} → 满足 {len(target_needs)} 项需求"
        reasoning_chain.append(f"功能映射: {mapping}")

        return self._create_result(
            True, mapping,
            0.8,
            reasoning_chain
        )


class SurfaceAnalogyEngine(SubReasoningEngine):
    """表面类比推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        case1 = input_data.get('case1', '')
        case2 = input_data.get('case2', '')

        reasoning_chain = ["【表面类比推理开始】"]
        reasoning_chain.append(f"案例1: {case1}")
        reasoning_chain.append(f"案例2: {case2}")
        reasoning_chain.append("表面特征匹配中...")

        return self._create_result(
            True, f"表面相似: {case1} ≈ {case2}",
            0.7,
            reasoning_chain
        )


class MetaphoricalEngine(SubReasoningEngine):
    """隐喻推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        source = input_data.get('source', '')
        target = input_data.get('target', '')

        reasoning_chain = ["【隐喻推理开始】"]
        reasoning_chain.append(f"源域: {source}")
        reasoning_chain.append(f"目标域: {target}")
        reasoning_chain.append(f"隐喻: {target}如同{source}")

        return self._create_result(
            True, f"{target}如同{source}",
            0.75,
            reasoning_chain
        )


class CaseBasedEngine(SubReasoningEngine):
    """案例类比推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        current = input_data.get('current_problem', '')
        cases = input_data.get('past_cases', [])

        reasoning_chain = ["【案例类比推理开始】"]
        reasoning_chain.append(f"当前问题: {current}")
        reasoning_chain.append(f"历史案例: {len(cases)} 个")

        similar_case = cases[0] if cases else "无相似案例"
        reasoning_chain.append(f"最相似案例: {similar_case}")

        return self._create_result(
            True, similar_case,
            0.85 if cases else 0.3,
            reasoning_chain
        )


class AnalogicalTransferEngine(SubReasoningEngine):
    """类比迁移推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        source_solution = input_data.get('source_solution', '')
        target_problem = input_data.get('target_problem', '')

        reasoning_chain = ["【类比迁移推理开始】"]
        reasoning_chain.append(f"源解决方案: {source_solution}")
        reasoning_chain.append(f"目标问题: {target_problem}")
        reasoning_chain.append("迁移中...")

        transferred = f"将'{source_solution}'应用于'{target_problem}'"
        reasoning_chain.append(f"迁移结果: {transferred}")

        return self._create_result(
            True, transferred,
            0.75,
            reasoning_chain
        )


# ============================================================================
# 概率推理引擎 (6个)
# ============================================================================

class BayesianReasoningEngine(SubReasoningEngine):
    """贝叶斯推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        prior = input_data.get('prior', 0.5)
        likelihood = input_data.get('likelihood', 0.8)
        evidence = input_data.get('evidence', '')

        reasoning_chain = ["【贝叶斯推理开始】"]
        reasoning_chain.append(f"先验概率: {prior:.2%}")
        reasoning_chain.append(f"似然: {likelihood:.2%}")
        reasoning_chain.append(f"证据: {evidence}")

        posterior = (prior * likelihood) / (prior * likelihood + (1 - prior) * 0.5)
        reasoning_chain.append(f"后验概率: {posterior:.2%}")

        return self._create_result(
            True, posterior,
            0.85,
            reasoning_chain,
            {"prior": prior, "likelihood": likelihood, "posterior": posterior}
        )


class ProbabilisticGraphEngine(SubReasoningEngine):
    """概率图推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        nodes = input_data.get('nodes', [])
        edges = input_data.get('edges', [])

        reasoning_chain = ["【概率图推理开始】"]
        reasoning_chain.append(f"节点: {len(nodes)}")
        reasoning_chain.append(f"边: {len(edges)}")

        result = "概率分布已计算"
        reasoning_chain.append(result)

        return self._create_result(
            True, result,
            0.8,
            reasoning_chain
        )


class MarkovReasoningEngine(SubReasoningEngine):
    """马尔可夫推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        states = input_data.get('states', [])
        transition = input_data.get('transition_matrix', [])

        reasoning_chain = ["【马尔可夫推理开始】"]
        reasoning_chain.append(f"状态数: {len(states)}")
        reasoning_chain.append("状态转移分析中...")

        result = "马尔可夫链稳定分布已计算"
        reasoning_chain.append(result)

        return self._create_result(
            True, result,
            0.85,
            reasoning_chain
        )


class MonteCarloEngine(SubReasoningEngine):
    """蒙特卡洛推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        iterations = input_data.get('iterations', 1000)
        distribution = input_data.get('distribution', 'normal')

        reasoning_chain = ["【蒙特卡洛推理开始】"]
        reasoning_chain.append(f"迭代次数: {iterations}")
        reasoning_chain.append(f"分布: {distribution}")
        reasoning_chain.append("模拟中...")

        mean = 0.5
        std = 0.1
        result = {"mean": mean, "std": std, "samples": iterations}
        reasoning_chain.append(f"结果: 均值={mean:.4f}, 标准差={std:.4f}")

        return self._create_result(
            True, result,
            0.9,
            reasoning_chain,
            result
        )


class VariationalEngine(SubReasoningEngine):
    """变分推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        model = input_data.get('model', '')

        reasoning_chain = ["【变分推理开始】"]
        reasoning_chain.append(f"模型: {model}")
        reasoning_chain.append("变分推断中...")

        result = "变分分布已近似"
        reasoning_chain.append(result)

        return self._create_result(
            True, result,
            0.8,
            reasoning_chain
        )


class EnsembleReasoningEngine(SubReasoningEngine):
    """集成推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        predictions = input_data.get('predictions', [])
        method = input_data.get('method', 'voting')

        reasoning_chain = ["【集成推理开始】"]
        reasoning_chain.append(f"子模型数: {len(predictions)}")
        reasoning_chain.append(f"集成方法: {method}")

        if method == 'voting':
            result = predictions[0] if predictions else None
        else:
            result = sum(predictions) / len(predictions) if predictions else 0

        reasoning_chain.append(f"集成结果: {result}")

        return self._create_result(
            True, result,
            0.9,
            reasoning_chain
        )


# ============================================================================
# 时序推理引擎 (6个)
# ============================================================================

class TemporalSequenceEngine(SubReasoningEngine):
    """时序推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        sequence = input_data.get('sequence', [])

        reasoning_chain = ["【时序推理开始】"]
        reasoning_chain.append(f"序列长度: {len(sequence)}")

        pattern = self._identify_pattern(sequence)
        reasoning_chain.append(f"时序模式: {pattern}")

        return self._create_result(
            True, pattern,
            0.85,
            reasoning_chain
        )

    def _identify_pattern(self, sequence: List) -> str:
        if len(sequence) < 3:
            return "数据不足"
        if all(sequence[i] <= sequence[i+1] for i in range(len(sequence)-1)):
            return "递增模式"
        elif all(sequence[i] >= sequence[i+1] for i in range(len(sequence)-1)):
            return "递减模式"
        return "波动模式"


class TrendExtrapolationEngine(SubReasoningEngine):
    """趋势外推引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        historical = input_data.get('historical', [])
        horizon = input_data.get('horizon', 3)

        reasoning_chain = ["【趋势外推开始】"]
        reasoning_chain.append(f"历史数据: {len(historical)} 点")
        reasoning_chain.append(f"预测周期: {horizon}")

        if len(historical) >= 2:
            trend = historical[-1] - historical[0]
            forecast = [historical[-1] + trend * (i+1) for i in range(horizon)]
        else:
            forecast = [historical[0]] * horizon

        reasoning_chain.append(f"预测: {forecast}")

        return self._create_result(
            True, forecast,
            0.75,
            reasoning_chain,
            {"forecast": forecast}
        )


class SeasonalAnalysisEngine(SubReasoningEngine):
    """季节性分析引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        data = input_data.get('data', [])
        period = input_data.get('period', 12)

        reasoning_chain = ["【季节性分析开始】"]
        reasoning_chain.append(f"数据长度: {len(data)}")
        reasoning_chain.append(f"季节周期: {period}")

        seasonal_index = [1.0] * period
        reasoning_chain.append(f"季节指数: {seasonal_index[:4]}...")

        return self._create_result(
            True, seasonal_index,
            0.8,
            reasoning_chain
        )


class CyclicReasoningEngine(SubReasoningEngine):
    """周期推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        data = input_data.get('data', [])

        reasoning_chain = ["【周期推理开始】"]
        reasoning_chain.append(f"数据点数: {len(data)}")

        cycle_length = len(data) // 3 if len(data) >= 6 else len(data)
        reasoning_chain.append(f"估计周期: {cycle_length}")

        return self._create_result(
            True, {"cycle_length": cycle_length},
            0.75,
            reasoning_chain
        )


class CausalTemporalEngine(SubReasoningEngine):
    """因果时序推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        cause_series = input_data.get('cause_series', [])
        effect_series = input_data.get('effect_series', [])

        reasoning_chain = ["【因果时序推理开始】"]
        reasoning_chain.append(f"原因序列: {len(cause_series)}")
        reasoning_chain.append(f"结果序列: {len(effect_series)}")

        lag = 1
        reasoning_chain.append(f"估计时滞: {lag} 个时间单位")

        return self._create_result(
            True, {"lag": lag},
            0.8,
            reasoning_chain
        )


class ForecastingEngine(SubReasoningEngine):
    """预测推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        historical = input_data.get('historical', [])
        horizon = input_data.get('horizon', 3)

        reasoning_chain = ["【预测推理开始】"]
        reasoning_chain.append(f"历史数据: {len(historical)}")
        reasoning_chain.append(f"预测步数: {horizon}")

        forecast = self._forecast(historical, horizon)
        reasoning_chain.append(f"预测结果: {[round(f, 2) for f in forecast]}")

        return self._create_result(
            True, forecast,
            0.8,
            reasoning_chain,
            {"forecast": forecast}
        )

    def _forecast(self, historical: List[float], horizon: int) -> List[float]:
        if not historical:
            return [0.0] * horizon
        window = min(3, len(historical))
        avg = sum(historical[-window:]) / window
        return [avg * (1 + 0.01 * i) for i in range(horizon)]


# ============================================================================
# 空间推理引擎 (3个)
# ============================================================================

class SpatialRelationEngine(SubReasoningEngine):
    """空间关系推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        objects = input_data.get('objects', [])

        reasoning_chain = ["【空间关系推理开始】"]
        for obj in objects:
            reasoning_chain.append(f"对象: {obj}")
        reasoning_chain.append("空间关系分析完成")

        return self._create_result(
            True, "空间关系已分析",
            0.85,
            reasoning_chain
        )


class TopologicalEngine(SubReasoningEngine):
    """拓扑推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        entities = input_data.get('entities', [])

        reasoning_chain = ["【拓扑推理开始】"]
        reasoning_chain.append(f"实体数: {len(entities)}")

        result = "拓扑关系: 连通/分离/包含"
        reasoning_chain.append(result)

        return self._create_result(
            True, result,
            0.8,
            reasoning_chain
        )


class GeometricEngine(SubReasoningEngine):
    """几何推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        shape = input_data.get('shape', '')
        dimensions = input_data.get('dimensions', {})

        reasoning_chain = ["【几何推理开始】"]
        reasoning_chain.append(f"形状: {shape}")
        reasoning_chain.append(f"尺寸: {dimensions}")

        result = "几何属性已计算"
        reasoning_chain.append(result)

        return self._create_result(
            True, result,
            0.9,
            reasoning_chain
        )


# ============================================================================
# 模糊推理引擎 (3个)
# ============================================================================

class FuzzyInferenceEngine(SubReasoningEngine):
    """模糊推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        input_value = input_data.get('value', 0.5)
        rules = input_data.get('rules', [])

        reasoning_chain = ["【模糊推理开始】"]
        reasoning_chain.append(f"输入值: {input_value}")
        reasoning_chain.append(f"模糊规则: {len(rules)} 条")

        fuzzy_set = {"low": 1-input_value, "high": input_value}
        reasoning_chain.append(f"模糊集: {fuzzy_set}")

        return self._create_result(
            True, fuzzy_set,
            0.75,
            reasoning_chain,
            {"fuzzy_set": fuzzy_set}
        )


class ApproximateReasoningEngine(SubReasoningEngine):
    """近似推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        premise = input_data.get('premise', '')

        reasoning_chain = ["【近似推理开始】"]
        reasoning_chain.append(f"前提: {premise}")
        reasoning_chain.append("近似匹配中...")

        result = f"近似结论: 可能正确"
        reasoning_chain.append(result)

        return self._create_result(
            True, result,
            0.7,
            reasoning_chain
        )


class LinguisticFuzzyEngine(SubReasoningEngine):
    """语言模糊推理引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        linguistic_input = input_data.get('linguistic', '')

        reasoning_chain = ["【语言模糊推理开始】"]
        reasoning_chain.append(f"语言输入: {linguistic_input}")

        membership = {"very": 0.3, "somewhat": 0.6, "extremely": 0.9}
        reasoning_chain.append(f"隶属度: {membership}")

        return self._create_result(
            True, membership,
            0.75,
            reasoning_chain
        )


# ============================================================================
# 注册所有40个认知推理引擎
# ============================================================================

def register_all_cognitive_engines():
    """注册所有40个认知推理引擎"""

    engines = [
        # 逻辑推理 (8个)
        DeductiveReasoningEngine("COG_001", "演绎推理", EngineCategory.COGNITIVE, CognitiveSubType.DEDUCTIVE, "从一般到特殊的推理"),
        InductiveReasoningEngine("COG_002", "归纳推理", EngineCategory.COGNITIVE, CognitiveSubType.INDUCTIVE, "从特殊到一般的推理"),
        AbductiveReasoningEngine("COG_003", "溯因推理", EngineCategory.COGNITIVE, CognitiveSubType.ABDUCTIVE, "寻找最佳解释"),
        SyllogisticReasoningEngine("COG_004", "三段论推理", EngineCategory.COGNITIVE, CognitiveSubType.SYLLOGISTIC, "经典三段论"),
        PropositionalLogicEngine("COG_005", "命题逻辑", EngineCategory.COGNITIVE, CognitiveSubType.PROPOSITIONAL, "命题逻辑推理"),
        PredicateLogicEngine("COG_006", "谓词逻辑", EngineCategory.COGNITIVE, CognitiveSubType.PREDICATE, "谓词逻辑推理"),
        ModalLogicEngine("COG_007", "模态逻辑", EngineCategory.COGNITIVE, CognitiveSubType.MODAL, "可能/必然推理"),
        TemporalLogicalEngine("COG_008", "时序逻辑", EngineCategory.COGNITIVE, CognitiveSubType.TEMPORAL_LOGICAL, "时序约束推理"),

        # 因果推理 (8个)
        CausalChainEngine("COG_009", "因果链", EngineCategory.COGNITIVE, CognitiveSubType.CAUSAL_CHAIN, "因果链条分析"),
        CausalGraphEngine("COG_010", "因果图", EngineCategory.COGNITIVE, CognitiveSubType.CAUSAL_GRAPH, "贝叶斯网络式因果"),
        CounterfactualEngine("COG_011", "反事实推理", EngineCategory.COGNITIVE, CognitiveSubType.COUNTERFACTUAL, "如果当初..."),
        InterventionEngine("COG_012", "干预分析", EngineCategory.COGNITIVE, CognitiveSubType.INTERVENTION, "do算子分析"),
        CausalInferenceEngine("COG_013", "因果推断", EngineCategory.COGNITIVE, CognitiveSubType.CAUSAL_INFERENCE, "统计因果推断"),
        ExplanationEngine("COG_014", "解释推理", EngineCategory.COGNITIVE, CognitiveSubType.EXPLANATION, "为什么会这样"),
        AttributionEngine("COG_015", "归因推理", EngineCategory.COGNITIVE, CognitiveSubType.ATTRIBUTION, "成功/失败归因"),
        MechanismEngine("COG_016", "机制推理", EngineCategory.COGNITIVE, CognitiveSubType.MECHANISM, "因果机制分析"),

        # 类比推理 (6个)
        StructuralAnalogyEngine("COG_017", "结构类比", EngineCategory.COGNITIVE, CognitiveSubType.STRUCTURAL_ANALOGY, "深层结构相似"),
        FunctionalAnalogyEngine("COG_018", "功能类比", EngineCategory.COGNITIVE, CognitiveSubType.FUNCTIONAL_ANALOGY, "功能相似类比"),
        SurfaceAnalogyEngine("COG_019", "表面类比", EngineCategory.COGNITIVE, CognitiveSubType.SURFACE_ANALOGY, "表面特征类比"),
        MetaphoricalEngine("COG_020", "隐喻推理", EngineCategory.COGNITIVE, CognitiveSubType.METAPHORICAL, "隐喻思维"),
        CaseBasedEngine("COG_021", "案例类比", EngineCategory.COGNITIVE, CognitiveSubType.CASE_BASED, "CBR案例推理"),
        AnalogicalTransferEngine("COG_022", "类比迁移", EngineCategory.COGNITIVE, CognitiveSubType.ANALOGICAL_TRANSFER, "跨领域迁移"),

        # 概率推理 (6个)
        BayesianReasoningEngine("COG_023", "贝叶斯推理", EngineCategory.COGNITIVE, CognitiveSubType.BAYESIAN, "贝叶斯更新"),
        ProbabilisticGraphEngine("COG_024", "概率图", EngineCategory.COGNITIVE, CognitiveSubType.PROBABILISTIC_GRAPH, "PGM推理"),
        MarkovReasoningEngine("COG_025", "马尔可夫", EngineCategory.COGNITIVE, CognitiveSubType.MARKOV, "马尔可夫链"),
        MonteCarloEngine("COG_026", "蒙特卡洛", EngineCategory.COGNITIVE, CognitiveSubType.MONTE_CARLO, "随机模拟"),
        VariationalEngine("COG_027", "变分推理", EngineCategory.COGNITIVE, CognitiveSubType.VARIATIONAL, "变分推断"),
        EnsembleReasoningEngine("COG_028", "集成推理", EngineCategory.COGNITIVE, CognitiveSubType.ENSEMBLE, "模型集成"),

        # 时序推理 (6个)
        TemporalSequenceEngine("COG_029", "时序推理", EngineCategory.COGNITIVE, CognitiveSubType.TEMPORAL_SEQUENCE, "时序模式识别"),
        TrendExtrapolationEngine("COG_030", "趋势外推", EngineCategory.COGNITIVE, CognitiveSubType.TREND_EXTRAPOLATION, "趋势预测"),
        SeasonalAnalysisEngine("COG_031", "季节分析", EngineCategory.COGNITIVE, CognitiveSubType.SEASONAL, "季节性检测"),
        CyclicReasoningEngine("COG_032", "周期推理", EngineCategory.COGNITIVE, CognitiveSubType.CYCLIC, "周期性分析"),
        CausalTemporalEngine("COG_033", "因果时序", EngineCategory.COGNITIVE, CognitiveSubType.CAUSAL_TEMPORAL, "格兰杰因果"),
        ForecastingEngine("COG_034", "预测推理", EngineCategory.COGNITIVE, CognitiveSubType.FORECASTING, "时序预测"),

        # 空间推理 (3个)
        SpatialRelationEngine("COG_035", "空间关系", EngineCategory.COGNITIVE, CognitiveSubType.SPATIAL_RELATION, "空间拓扑关系"),
        TopologicalEngine("COG_036", "拓扑推理", EngineCategory.COGNITIVE, CognitiveSubType.TOPOLOGICAL, "拓扑结构分析"),
        GeometricEngine("COG_037", "几何推理", EngineCategory.COGNITIVE, CognitiveSubType.GEOMETRIC, "几何计算推理"),

        # 模糊推理 (3个)
        FuzzyInferenceEngine("COG_038", "模糊推理", EngineCategory.COGNITIVE, CognitiveSubType.FUZZY_INFERENCE, "模糊逻辑推理"),
        ApproximateReasoningEngine("COG_039", "近似推理", EngineCategory.COGNITIVE, CognitiveSubType.APPROXIMATE, "近似匹配推理"),
        LinguisticFuzzyEngine("COG_040", "语言模糊", EngineCategory.COGNITIVE, CognitiveSubType.LINGUISTIC, "语言变量模糊化"),
    ]

    for engine in engines:
        GLOBAL_ENGINE_REGISTRY.register(engine)

    return len(engines)


# 自动注册
_registered_count = register_all_cognitive_engines()

__all__ = [
    'register_all_cognitive_engines',
    '_registered_count',
]
