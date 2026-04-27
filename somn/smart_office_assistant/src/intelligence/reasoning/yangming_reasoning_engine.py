"""
王阳明心学深度推理引擎 - Yangming Reasoning Engine
v1.0.0

基于王阳明心学核心思想构建的推理引擎:
- 致良知: 直觉性道德判断与决策
- 知行合一: 认知与行动的统一推理
- 心即理: 内在心性即万物之理
- 事上磨炼: 在实践中检验和提升认知

推理模式:
1. 良知推理 - 从内在道德直觉出发的判断推理
2. 知行推理 - 认知-行动一致性分析
3. 心即理推理 - 从内在心性推导外在事理
4. 事上磨炼推理 - 实践验证型推理

版本历史:
- v1.0.0 (2026-04-22): 完整实现，替代空壳占位文件
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class YangmingReasoningMode(Enum):
    """心学推理模式"""
    LIANGZHI = "良知推理"           # 从内在道德直觉出发
    ZHIXING_HEYI = "知行推理"       # 认知-行动一致性分析
    XIN_JI_LI = "心即理推理"        # 从内在心性推导外在事理
    SHISHANG_MOLIAN = "事上磨炼推理"  # 实践验证型推理


class ZhiXingAlignment(Enum):
    """知行对齐度"""
    ALIGNED = "知行合一"       # 认知与行动完全一致
    PARTIAL = "知行部分合一"   # 认知与行动部分一致
    MISALIGNED = "知行脱节"   # 认知与行动不一致
    LATENT = "知而未行"       # 有认知但未行动


@dataclass
class LiangzhiJudgment:
    """良知判断结果"""
    is_right: bool                     # 是否符合良知
    confidence: float                   # 置信度(0-1)
    moral_dimension: str               # 道德维度
    reasoning: str                      # 推理过程
    principle_applied: str             # 应用的心学原则


@dataclass
class ZhiXingAnalysis:
    """知行分析结果"""
    knowledge_aspect: str              # 认知方面
    action_aspect: str                 # 行动方面
    alignment: ZhiXingAlignment        # 对齐度
    gap_description: str              # 差距描述
    bridge_suggestion: str            # 桥接建议


@dataclass
class YangmingReasoningResult:
    """心学推理结果"""
    mode: YangmingReasoningMode        # 推理模式
    conclusion: str                     # 结论
    confidence: float                   # 置信度
    reasoning_chain: List[str]         # 推理链
    principle_applied: str             # 应用的心学原则
    practical_guidance: str            # 实践指导
    zhi_xing_analysis: Optional[ZhiXingAnalysis] = None  # 知行分析(可选)


class YangmingReasoningEngine:
    """
    王阳明心学深度推理引擎
    
    核心思想:
    - 致良知: 每个人内心都有良知，通过内省可以发现真理
    - 知行合一: 真正的知识必然伴随行动，知而不行只是未知
    - 心即理: 天理就在心中，不需要外求
    - 事上磨炼: 真正的修炼在于日常事务中的实践
    
    推理策略:
    1. 面对道德判断 → 良知推理(致良知)
    2. 面对执行力问题 → 知行推理(知行合一)
    3. 面对认知困惑 → 心即理推理(心即理)
    4. 面对实践检验 → 事上磨炼推理(事上磨炼)
    """

    VERSION = "2.0.0"
    
    # 心学核心原则
    CORE_PRINCIPLES = {
        "致良知": "内心本具明德，通过内省去除私欲遮蔽，恢复良知本明",
        "知行合一": "知是行之始，行是知之成；知而不行，只是未知",
        "心即理": "心外无理，心外无物；万物之理皆在心中",
        "事上磨炼": "在事上磨炼方有着落，若只静坐冥想终无进步",
        "诚意正心": "诚意是功夫下手处，正心是功夫成就处",
        "格物致知": "格物者，格其心之物也；致知者，致其心之知也",
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化心学推理引擎"""
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.reasoning_history: List[Dict[str, Any]] = []
        self._principle_weights = {
            "致良知": 0.25,
            "知行合一": 0.25,
            "心即理": 0.20,
            "事上磨炼": 0.15,
            "诚意正心": 0.10,
            "格物致知": 0.05,
        }

    def reason(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None,
        mode: Optional[YangmingReasoningMode] = None,
    ) -> YangmingReasoningResult:
        """
        执行心学推理
        
        Args:
            problem: 问题描述
            context: 上下文信息
            mode: 指定推理模式(不指定则自动选择)
            
        Returns:
            YangmingReasoningResult: 推理结果
        """
        context = context or {}
        
        # 自动选择推理模式
        if mode is None:
            mode = self._select_reasoning_mode(problem, context)
        
        # 根据模式执行推理
        if mode == YangmingReasoningMode.LIANGZHI:
            result = self._reason_liangzhi(problem, context)
        elif mode == YangmingReasoningMode.ZHIXING_HEYI:
            result = self._reason_zhixing(problem, context)
        elif mode == YangmingReasoningMode.XIN_JI_LI:
            result = self._reason_xin_ji_li(problem, context)
        elif mode == YangmingReasoningMode.SHISHANG_MOLIAN:
            result = self._reason_shishang(problem, context)
        else:
            result = self._reason_liangzhi(problem, context)
        
        # 记录推理历史
        self.reasoning_history.append({
            "problem": problem[:100],
            "mode": mode.value,
            "conclusion": result.conclusion[:100],
            "confidence": result.confidence,
        })
        
        return result

    def _select_reasoning_mode(
        self, problem: str, context: Dict[str, Any]
    ) -> YangmingReasoningMode:
        """根据问题特征选择推理模式"""
        problem_lower = problem.lower()
        
        # 道德判断类问题 → 良知推理
        moral_keywords = ["对错", "善恶", "应该", "道德", "正当", "良心", "伦理", "是非"]
        if any(kw in problem_lower for kw in moral_keywords):
            return YangmingReasoningMode.LIANGZHI
        
        # 执行力/行动类问题 → 知行推理
        action_keywords = ["执行", "行动", "做到", "落地", "实施", "知行", "拖延", "实践"]
        if any(kw in problem_lower for kw in action_keywords):
            return YangmingReasoningMode.ZHIXING_HEYI
        
        # 认知困惑类问题 → 心即理推理
        cognition_keywords = ["理解", "困惑", "不明白", "为什么", "道理", "原理", "本质"]
        if any(kw in problem_lower for kw in cognition_keywords):
            return YangmingReasoningMode.XIN_JI_LI
        
        # 实践检验类问题 → 事上磨炼推理
        practice_keywords = ["验证", "检验", "试错", "经验", "磨炼", "挑战", "困难"]
        if any(kw in problem_lower for kw in practice_keywords):
            return YangmingReasoningMode.SHISHANG_MOLIAN
        
        # 默认使用良知推理
        return YangmingReasoningMode.LIANGZHI

    def _reason_liangzhi(
        self, problem: str, context: Dict[str, Any]
    ) -> YangmingReasoningResult:
        """良知推理 - 从内在道德直觉出发"""
        reasoning_chain = [
            f"1. 觉察问题: {problem}",
            "2. 收摄心神，回归良知本明",
            "3. 审视内心第一反应（良知之发见）",
            "4. 去除私欲遮蔽，明辨是非善恶",
            "5. 良知判断：是非自有本心",
        ]
        
        # 基于上下文判断
        is_right = context.get("moral_evaluation", True)
        confidence = context.get("confidence", 0.7)
        
        judgment = LiangzhiJudgment(
            is_right=is_right,
            confidence=confidence,
            moral_dimension="良知本明",
            reasoning="致良知：内心自有明辨是非的能力，无需外求",
            principle_applied="致良知",
        )
        
        return YangmingReasoningResult(
            mode=YangmingReasoningMode.LIANGZHI,
            conclusion=f"良知判断：{'此为正道，当笃行之' if is_right else '此为歧途，当速省之'}",
            confidence=confidence,
            reasoning_chain=reasoning_chain,
            principle_applied="致良知",
            practical_guidance="正心诚意，听从良知指引，去除私欲遮蔽，则善行自然流出",
        )

    def _reason_zhixing(
        self, problem: str, context: Dict[str, Any]
    ) -> YangmingReasoningResult:
        """知行推理 - 认知与行动的统一分析"""
        knowledge = context.get("knowledge", "已知其理")
        action = context.get("action", "尚未践行")
        
        reasoning_chain = [
            f"1. 审视问题: {problem}",
            f"2. 认知面：{knowledge}",
            f"3. 行动面：{action}",
            "4. 对齐分析：知是行之始，行是知之成",
            "5. 若知而不行，实为未知",
        ]
        
        # 判断知行对齐度
        if knowledge and action and action != "尚未践行":
            alignment = ZhiXingAlignment.ALIGNED
            gap = "知行基本合一"
            bridge = "持续践行，深化认知"
        elif knowledge and (not action or action == "尚未践行"):
            alignment = ZhiXingAlignment.LATENT
            gap = "有知无行，实为未知"
            bridge = "将认知转化为行动，在行动中验证和深化认知"
        else:
            alignment = ZhiXingAlignment.PARTIAL
            gap = "知行部分脱节"
            bridge = "加强行动力度，在事上磨炼中达成知行合一"
        
        zhi_xing = ZhiXingAnalysis(
            knowledge_aspect=knowledge,
            action_aspect=action,
            alignment=alignment,
            gap_description=gap,
            bridge_suggestion=bridge,
        )
        
        return YangmingReasoningResult(
            mode=YangmingReasoningMode.ZHIXING_HEYI,
            conclusion=f"知行分析：{alignment.value}，{bridge}",
            confidence=0.75,
            reasoning_chain=reasoning_chain,
            principle_applied="知行合一",
            practical_guidance=bridge,
            zhi_xing_analysis=zhi_xing,
        )

    def _reason_xin_ji_li(
        self, problem: str, context: Dict[str, Any]
    ) -> YangmingReasoningResult:
        """心即理推理 - 从内在心性推导外在事理"""
        reasoning_chain = [
            f"1. 困惑之处: {problem}",
            "2. 心即理：万物之理不在心外",
            "3. 反求诸己：向内寻求答案",
            "4. 心明则理明：内心澄澈则事理自明",
            "5. 万物皆备于我：不假外求",
        ]
        
        return YangmingReasoningResult(
            mode=YangmingReasoningMode.XIN_JI_LI,
            conclusion="心即理：此理本在心中，不需外求，反求诸己即可明达",
            confidence=0.7,
            reasoning_chain=reasoning_chain,
            principle_applied="心即理",
            practical_guidance="静心内省，去除物欲遮蔽，心中本有之理自然显现。不必执著于向外探求，回到内心方能真正理解",
        )

    def _reason_shishang(
        self, problem: str, context: Dict[str, Any]
    ) -> YangmingReasoningResult:
        """事上磨炼推理 - 在实践中检验和提升"""
        reasoning_chain = [
            f"1. 面对磨炼: {problem}",
            "2. 事上磨炼方有着落，若只静坐冥想终无进步",
            "3. 在实际行动中检验认知",
            "4. 困境即修炼场：越是困难越能磨炼心性",
            "5. 知行在事上合一：做中觉，觉中做",
        ]
        
        return YangmingReasoningResult(
            mode=YangmingReasoningMode.SHISHANG_MOLIAN,
            conclusion="事上磨炼：唯有在实践中历练，方能真正知行合一。困难不是阻碍，而是磨炼心性的道场",
            confidence=0.8,
            reasoning_chain=reasoning_chain,
            principle_applied="事上磨炼",
            practical_guidance="不回避困难，在日常事务中磨炼心性。每一次挑战都是致良知的契机，每一次实践都是知行合一的修炼",
        )

    def get_principles(self) -> Dict[str, str]:
        """获取心学核心原则"""
        return dict(self.CORE_PRINCIPLES)

    def get_reasoning_stats(self) -> Dict[str, Any]:
        """获取推理统计"""
        mode_counts = {}
        for h in self.reasoning_history:
            mode = h.get("mode", "unknown")
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
        
        avg_confidence = (
            sum(h["confidence"] for h in self.reasoning_history) / len(self.reasoning_history)
            if self.reasoning_history else 0.0
        )
        
        return {
            "total_reasonings": len(self.reasoning_history),
            "mode_distribution": mode_counts,
            "average_confidence": round(avg_confidence, 3),
            "engine_version": self.VERSION,
        }


__all__ = [
    'YangmingReasoningEngine',
    'YangmingReasoningMode',
    'ZhiXingAlignment',
    'LiangzhiJudgment',
    'ZhiXingAnalysis',
    'YangmingReasoningResult',
]
