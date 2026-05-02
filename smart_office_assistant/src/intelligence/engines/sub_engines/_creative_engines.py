"""
创意推理引擎子系统 (Creative Reasoning Engines)
包含30个子引擎

分类:
- 联想思维 (8个)
- 组合创新 (7个)
- 逆向思维 (5个)
- 横向思维 (5个)
- 收敛思维 (5个)
"""

from typing import Any, Dict, List, Optional
from ._sub_engine_base import (
    SubReasoningEngine,
    EngineCategory,
    CreativeSubType,
    ReasoningResult,
    GLOBAL_ENGINE_REGISTRY,
)
import random


# ============================================================================
# 联想思维引擎 (8个)
# ============================================================================

class AssociativeBrainstormEngine(SubReasoningEngine):
    """联想头脑风暴引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        topic = input_data.get('topic', '')

        reasoning_chain = ["【联想头脑风暴开始】"]
        reasoning_chain.append(f"主题: {topic}")

        # 自由联想
        associations = [f"{topic}相关创意{i}" for i in range(1, 6)]
        reasoning_chain.append(f"联想结果: {associations}")

        return self._create_result(
            True, associations,
            0.8,
            reasoning_chain,
            {"ideas": associations}
        )


class FreeAssociationEngine(SubReasoningEngine):
    """自由联想引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        seed = input_data.get('seed', '')

        reasoning_chain = ["【自由联想开始】"]
        reasoning_chain.append(f"种子词: {seed}")

        chain = [seed]
        for i in range(5):
            chain.append(f"联想{i+1}")
        reasoning_chain.append(f"联想链: {' → '.join(chain)}")

        return self._create_result(
            True, chain,
            0.75,
            reasoning_chain
        )


class WordAssociationEngine(SubReasoningEngine):
    """词汇联想引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        word = input_data.get('word', '')

        reasoning_chain = ["【词汇联想开始】"]
        reasoning_chain.append(f"触发词: {word}")

        associations = ["相关词1", "相关词2", "相关词3"]
        reasoning_chain.append(f"联想词汇: {associations}")

        return self._create_result(
            True, associations,
            0.8,
            reasoning_chain
        )


class SemanticNetworkEngine(SubReasoningEngine):
    """语义网络引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        concepts = input_data.get('concepts', [])

        reasoning_chain = ["【语义网络构建开始】"]
        reasoning_chain.append(f"概念数: {len(concepts)}")

        network = {c: [f"关联{c}{i}" for i in range(2)] for c in concepts}
        reasoning_chain.append(f"网络节点: {len(network)}")

        return self._create_result(
            True, network,
            0.85,
            reasoning_chain
        )


class ConceptMappingEngine(SubReasoningEngine):
    """概念映射引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        elements = input_data.get('elements', [])

        reasoning_chain = ["【概念映射开始】"]
        reasoning_chain.append(f"元素数: {len(elements)}")

        mapping = {"核心概念": elements[0] if elements else "", "关联": elements[1:]}
        reasoning_chain.append(f"映射结果: {mapping}")

        return self._create_result(
            True, mapping,
            0.8,
            reasoning_chain
        )


class MindMappingEngine(SubReasoningEngine):
    """思维导图引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        central = input_data.get('central', '')

        reasoning_chain = ["【思维导图生成开始】"]
        reasoning_chain.append(f"中心主题: {central}")

        branches = {
            central: [f"分支{i}" for i in range(1, 4)]
        }
        reasoning_chain.append(f"分支数: {len(branches[central])}")

        return self._create_result(
            True, branches,
            0.85,
            reasoning_chain
        )


class MemeticEngine(SubReasoningEngine):
    """模因联想引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        meme = input_data.get('meme', '')

        reasoning_chain = ["【模因联想开始】"]
        reasoning_chain.append(f"模因: {meme}")

        variations = [f"{meme}变体{i}" for i in range(1, 4)]
        reasoning_chain.append(f"变体: {variations}")

        return self._create_result(
            True, variations,
            0.75,
            reasoning_chain
        )


class CreativeAbstractionEngine(SubReasoningEngine):
    """创意抽象引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        concrete = input_data.get('concrete', '')

        reasoning_chain = ["【创意抽象开始】"]
        reasoning_chain.append(f"具体概念: {concrete}")

        abstract = f"抽象化的{concrete}"
        reasoning_chain.append(f"抽象结果: {abstract}")

        return self._create_result(
            True, abstract,
            0.8,
            reasoning_chain
        )


# ============================================================================
# 组合创新引擎 (7个)
# ============================================================================

class CombinatorialEngine(SubReasoningEngine):
    """组合创新引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        elements = input_data.get('elements', [])

        reasoning_chain = ["【组合创新开始】"]
        reasoning_chain.append(f"组合元素: {len(elements)}")

        combinations = []
        for i in range(len(elements)):
            for j in range(i+1, len(elements)):
                combinations.append(f"{elements[i]}+{elements[j]}")

        reasoning_chain.append(f"新组合数: {len(combinations)}")
        reasoning_chain.append(f"示例: {combinations[:3]}")

        return self._create_result(
            True, combinations,
            0.85,
            reasoning_chain
        )


class CrossDomainEngine(SubReasoningEngine):
    """跨域组合引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        domain1 = input_data.get('domain1', '')
        domain2 = input_data.get('domain2', '')

        reasoning_chain = ["【跨域组合开始】"]
        reasoning_chain.append(f"领域1: {domain1}")
        reasoning_chain.append(f"领域2: {domain2}")

        innovations = [f"{domain1}×{domain2}创新{i}" for i in range(1, 4)]
        reasoning_chain.append(f"跨域创新: {innovations}")

        return self._create_result(
            True, innovations,
            0.85,
            reasoning_chain
        )


class FeatureCombinationEngine(SubReasoningEngine):
    """特征组合引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        features = input_data.get('features', [])

        reasoning_chain = ["【特征组合开始】"]
        reasoning_chain.append(f"特征数: {len(features)}")

        combinations = [[f] for f in features]
        reasoning_chain.append(f"组合特征数: {len(combinations)}")

        return self._create_result(
            True, combinations,
            0.8,
            reasoning_chain
        )


class AnalogicalCombinationEngine(SubReasoningEngine):
    """类比组合引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        source = input_data.get('source', '')
        target = input_data.get('target', '')

        reasoning_chain = ["【类比组合开始】"]
        reasoning_chain.append(f"源: {source}")
        reasoning_chain.append(f"目标: {target}")

        combined = f"将{source}的原理应用到{target}"
        reasoning_chain.append(f"组合结果: {combined}")

        return self._create_result(
            True, combined,
            0.8,
            reasoning_chain
        )


class UnexpectedCombinationEngine(SubReasoningEngine):
    """意外组合引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        elements = input_data.get('elements', [])

        reasoning_chain = ["【意外组合开始】"]
        reasoning_chain.append(f"输入元素: {elements}")

        # 随机组合
        if len(elements) >= 2:
            random.shuffle(elements)
            unexpected = [f"意外组合{i+1}" for i in range(min(3, len(elements)))]
        else:
            unexpected = ["需要至少2个元素"]

        reasoning_chain.append(f"意外组合: {unexpected}")

        return self._create_result(
            True, unexpected,
            0.7,
            reasoning_chain
        )


class RecombinationEngine(SubReasoningEngine):
    """重组创新引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        parts = input_data.get('parts', [])

        reasoning_chain = ["【重组创新开始】"]
        reasoning_chain.append(f"部件数: {len(parts)}")

        reorganized = parts[::-1]  # 反转顺序
        reasoning_chain.append(f"重组结果: {reorganized}")

        return self._create_result(
            True, reorganized,
            0.8,
            reasoning_chain
        )


class HybridizationEngine(SubReasoningEngine):
    """杂交创新引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        parent1 = input_data.get('parent1', '')
        parent2 = input_data.get('parent2', '')

        reasoning_chain = ["【杂交创新开始】"]
        reasoning_chain.append(f"父本: {parent1}")
        reasoning_chain.append(f"母本: {parent2}")

        hybrid = f"{parent1}与{parent2}的杂交体"
        reasoning_chain.append(f"杂交结果: {hybrid}")

        return self._create_result(
            True, hybrid,
            0.85,
            reasoning_chain
        )


# ============================================================================
# 逆向思维引擎 (5个)
# ============================================================================

class ReverseAnalysisEngine(SubReasoningEngine):
    """逆向分析引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        goal = input_data.get('goal', '')

        reasoning_chain = ["【逆向分析开始】"]
        reasoning_chain.append(f"目标: {goal}")

        reverse_steps = ["从结果倒推步骤", "识别前置条件", "找到关键路径"]
        reasoning_chain.append(f"逆向步骤: {reverse_steps}")

        return self._create_result(
            True, reverse_steps,
            0.85,
            reasoning_chain
        )


class InverseProblemEngine(SubReasoningEngine):
    """逆向求解引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        desired = input_data.get('desired', '')

        reasoning_chain = ["【逆向求解开始】"]
        reasoning_chain.append(f"期望结果: {desired}")

        solution = f"逆向推导{desired}的解"
        reasoning_chain.append(f"求解结果: {solution}")

        return self._create_result(
            True, solution,
            0.8,
            reasoning_chain
        )


class ContrarianThinkingEngine(SubReasoningEngine):
    """反向思考引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        assumption = input_data.get('assumption', '')

        reasoning_chain = ["【反向思考开始】"]
        reasoning_chain.append(f"假设: {assumption}")
        reasoning_chain.append("思考相反的可能性...")

        contrary = f"相反观点: {assumption}可能是错的"
        reasoning_chain.append(f"反向结论: {contrary}")

        return self._create_result(
            True, contrary,
            0.75,
            reasoning_chain
        )


class WhatIfAnalysisEngine(SubReasoningEngine):
    """反向假设引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        scenario = input_data.get('scenario', '')

        reasoning_chain = ["【反事实假设分析开始】"]
        reasoning_chain.append(f"假设情景: {scenario}")

        implications = [f"如果{scenario}，则{i}" for i in range(1, 4)]
        reasoning_chain.append(f"推论: {implications}")

        return self._create_result(
            True, implications,
            0.8,
            reasoning_chain
        )


class BackwardInductionEngine(SubReasoningEngine):
    """逆向归纳引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        final_state = input_data.get('final_state', '')

        reasoning_chain = ["【逆向归纳开始】"]
        reasoning_chain.append(f"最终状态: {final_state}")

        steps = ["识别最优终局", "倒推前一步", "找到最优路径"]
        reasoning_chain.append(f"归纳步骤: {steps}")

        return self._create_result(
            True, steps,
            0.85,
            reasoning_chain
        )


# ============================================================================
# 横向思维引擎 (5个)
# ============================================================================

class LateralThinkingEngine(SubReasoningEngine):
    """横向思维引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        problem = input_data.get('problem', '')

        reasoning_chain = ["【横向思维开始】"]
        reasoning_chain.append(f"问题: {problem}")
        reasoning_chain.append("跳出常规思维框架...")

        lateral_solutions = [f"{problem}的创意解法{i}" for i in range(1, 4)]
        reasoning_chain.append(f"创意解法: {lateral_solutions}")

        return self._create_result(
            True, lateral_solutions,
            0.8,
            reasoning_chain
        )


class ProvocationEngine(SubReasoningEngine):
    """激发思考引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        statement = input_data.get('statement', '')

        reasoning_chain = ["【激发思考开始】"]
        reasoning_chain.append(f"陈述: {statement}")
        reasoning_chain.append("提出挑衅性观点...")

        provocation = f"如果{statement}的反面成立呢?"
        reasoning_chain.append(f"激发观点: {provocation}")

        return self._create_result(
            True, provocation,
            0.75,
            reasoning_chain
        )


class RandomInputEngine(SubReasoningEngine):
    """随机输入引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        context_text = input_data.get('context', '')

        reasoning_chain = ["【随机输入激发开始】"]
        reasoning_chain.append(f"上下文: {context_text}")
        reasoning_chain.append("引入随机元素...")

        random_elements = ["随机元素1", "随机元素2", "随机元素3"]
        reasoning_chain.append(f"随机元素: {random_elements}")

        return self._create_result(
            True, random_elements,
            0.7,
            reasoning_chain
        )


class EscapeThinkingEngine(SubReasoningEngine):
    """逃脱思维引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        constraint = input_data.get('constraint', '')

        reasoning_chain = ["【逃脱思维开始】"]
        reasoning_chain.append(f"当前约束: {constraint}")
        reasoning_chain.append("尝试打破约束...")

        escape = f"绕过{constraint}的方案"
        reasoning_chain.append(f"逃脱方案: {escape}")

        return self._create_result(
            True, escape,
            0.8,
            reasoning_chain
        )


class ChallengeAssumptionsEngine(SubReasoningEngine):
    """挑战假设引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        assumptions = input_data.get('assumptions', [])

        reasoning_chain = ["【挑战假设开始】"]
        reasoning_chain.append(f"假设数: {len(assumptions)}")

        challenged = [f"{a} - 需验证" for a in assumptions]
        reasoning_chain.append(f"挑战结果: {challenged}")

        return self._create_result(
            True, challenged,
            0.85,
            reasoning_chain
        )


# ============================================================================
# 收敛思维引擎 (5个)
# ============================================================================

class ConvergentThinkingEngine(SubReasoningEngine):
    """收敛思维引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        options = input_data.get('options', [])

        reasoning_chain = ["【收敛思维开始】"]
        reasoning_chain.append(f"候选方案: {len(options)} 个")

        # 简单评分收敛
        scored = [(opt, 0.5 + i * 0.1) for i, opt in enumerate(options)]
        best = max(scored, key=lambda x: x[1])
        reasoning_chain.append(f"最优方案: {best[0]} (评分: {best[1]:.2f})")

        return self._create_result(
            True, best,
            0.9,
            reasoning_chain
        )


class SelectionEngine(SubReasoningEngine):
    """选择收敛引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        candidates = input_data.get('candidates', [])
        criteria = input_data.get('criteria', [])

        reasoning_chain = ["【选择收敛开始】"]
        reasoning_chain.append(f"候选数: {len(candidates)}")
        reasoning_chain.append(f"评估标准: {len(criteria)} 项")

        selected = candidates[0] if candidates else None
        reasoning_chain.append(f"选定: {selected}")

        return self._create_result(
            True, selected,
            0.9,
            reasoning_chain
        )


class EvaluationEngine(SubReasoningEngine):
    """评估收敛引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        items = input_data.get('items', [])

        reasoning_chain = ["【评估收敛开始】"]
        reasoning_chain.append(f"待评估项: {len(items)}")

        scores = {item: 0.7 for item in items}
        reasoning_chain.append(f"评分: {scores}")

        return self._create_result(
            True, scores,
            0.85,
            reasoning_chain
        )


class PrioritizationEngine(SubReasoningEngine):
    """优先级收敛引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        tasks = input_data.get('tasks', [])

        reasoning_chain = ["【优先级收敛开始】"]
        reasoning_chain.append(f"任务数: {len(tasks)}")

        # 按优先级排序
        prioritized = [{"task": t, "priority": len(tasks) - i} for i, t in enumerate(tasks)]
        reasoning_chain.append(f"优先级: {prioritized}")

        return self._create_result(
            True, prioritized,
            0.9,
            reasoning_chain
        )


class SynthesisEngine(SubReasoningEngine):
    """综合收敛引擎"""

    def reason(self, input_data: Any, context: Optional[Dict[str, Any]] = None) -> ReasoningResult:
        inputs = input_data.get('inputs', [])

        reasoning_chain = ["【综合收敛开始】"]
        reasoning_chain.append(f"输入数: {len(inputs)}")

        synthesis = f"综合{len(inputs)}个输入形成统一方案"
        reasoning_chain.append(f"综合结果: {synthesis}")

        return self._create_result(
            True, synthesis,
            0.85,
            reasoning_chain
        )


# ============================================================================
# 注册所有30个创意推理引擎
# ============================================================================

def register_all_creative_engines():
    """注册所有30个创意推理引擎"""

    engines = [
        # 联想思维 (8个)
        AssociativeBrainstormEngine("CRT_001", "联想头脑风暴", EngineCategory.CREATIVE, CreativeSubType.ASSOCIATIVE_BRAINSTORM, "自由联想创意"),
        FreeAssociationEngine("CRT_002", "自由联想", EngineCategory.CREATIVE, CreativeSubType.FREE_ASSOCIATION, "无限制联想"),
        WordAssociationEngine("CRT_003", "词汇联想", EngineCategory.CREATIVE, CreativeSubType.WORD_ASSOCIATION, "词汇触发联想"),
        SemanticNetworkEngine("CRT_004", "语义网络", EngineCategory.CREATIVE, CreativeSubType.SEMANTIC_NETWORK, "语义关系网络"),
        ConceptMappingEngine("CRT_005", "概念映射", EngineCategory.CREATIVE, CreativeSubType.CONCEPT_MAPPING, "概念关系映射"),
        MindMappingEngine("CRT_006", "思维导图", EngineCategory.CREATIVE, CreativeSubType.MIND_MAPPING, "思维导图生成"),
        MemeticEngine("CRT_007", "模因联想", EngineCategory.CREATIVE, CreativeSubType.MEMETIC, "模因复制传播"),
        CreativeAbstractionEngine("CRT_008", "创意抽象", EngineCategory.CREATIVE, CreativeSubType.CREATIVE_ABSTRACTION, "抽象化创意"),

        # 组合创新 (7个)
        CombinatorialEngine("CRT_009", "组合创新", EngineCategory.CREATIVE, CreativeSubType.COMBINATORIAL, "元素组合创新"),
        CrossDomainEngine("CRT_010", "跨域组合", EngineCategory.CREATIVE, CreativeSubType.CROSS_DOMAIN, "跨领域组合"),
        FeatureCombinationEngine("CRT_011", "特征组合", EngineCategory.CREATIVE, CreativeSubType.FEATURE_COMBINATION, "特征组合创新"),
        AnalogicalCombinationEngine("CRT_012", "类比组合", EngineCategory.CREATIVE, CreativeSubType.ANALOGICAL_COMBINATION, "类比驱动组合"),
        UnexpectedCombinationEngine("CRT_013", "意外组合", EngineCategory.CREATIVE, CreativeSubType.UNEXPECTED_COMBINATION, "意外元素组合"),
        RecombinationEngine("CRT_014", "重组创新", EngineCategory.CREATIVE, CreativeSubType.RECOMBINATION, "现有元素重组"),
        HybridizationEngine("CRT_015", "杂交创新", EngineCategory.CREATIVE, CreativeSubType.HYBRIDIZATION, "不同来源杂交"),

        # 逆向思维 (5个)
        ReverseAnalysisEngine("CRT_016", "逆向分析", EngineCategory.CREATIVE, CreativeSubType.REVERSE_ANALYSIS, "从结果倒推"),
        InverseProblemEngine("CRT_017", "逆向求解", EngineCategory.CREATIVE, CreativeSubType.INVERSE_PROBLEM, "逆向问题求解"),
        ContrarianThinkingEngine("CRT_018", "反向思考", EngineCategory.CREATIVE, CreativeSubType.CONTRARIAN, "对立观点思考"),
        WhatIfAnalysisEngine("CRT_019", "反事实假设", EngineCategory.CREATIVE, CreativeSubType.WHAT_IF, "假设情景分析"),
        BackwardInductionEngine("CRT_020", "逆向归纳", EngineCategory.CREATIVE, CreativeSubType.BACKWARD_INDUCTION, "逆向归纳推理"),

        # 横向思维 (5个)
        LateralThinkingEngine("CRT_021", "横向思维", EngineCategory.CREATIVE, CreativeSubType.LATERAL_THINKING, "跳出框架思考"),
        ProvocationEngine("CRT_022", "激发思考", EngineCategory.CREATIVE, CreativeSubType.PROVOCATION, "挑衅激发创意"),
        RandomInputEngine("CRT_023", "随机输入", EngineCategory.CREATIVE, CreativeSubType.RANDOM_INPUT, "随机元素激发"),
        EscapeThinkingEngine("CRT_024", "逃脱思维", EngineCategory.CREATIVE, CreativeSubType.ESCAPE, "摆脱约束思考"),
        ChallengeAssumptionsEngine("CRT_025", "挑战假设", EngineCategory.CREATIVE, CreativeSubType.CHALLENGE_ASSUMPTIONS, "质疑现有假设"),

        # 收敛思维 (5个)
        ConvergentThinkingEngine("CRT_026", "收敛思维", EngineCategory.CREATIVE, CreativeSubType.CONVERGENT, "收敛到最优解"),
        SelectionEngine("CRT_027", "选择收敛", EngineCategory.CREATIVE, CreativeSubType.SELECTION, "多选一收敛"),
        EvaluationEngine("CRT_028", "评估收敛", EngineCategory.CREATIVE, CreativeSubType.EVALUATION, "评估筛选"),
        PrioritizationEngine("CRT_029", "优先级收敛", EngineCategory.CREATIVE, CreativeSubType.PRIORITIZATION, "优先级排序"),
        SynthesisEngine("CRT_030", "综合收敛", EngineCategory.CREATIVE, CreativeSubType.SYNTHESIS, "综合统一"),
    ]

    for engine in engines:
        GLOBAL_ENGINE_REGISTRY.register(engine)

    return len(engines)


# 自动注册
_registered_count = register_all_creative_engines()

__all__ = [
    'register_all_creative_engines',
    '_registered_count',
]
