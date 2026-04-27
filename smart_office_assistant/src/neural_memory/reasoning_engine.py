"""
__all__ = [
    'get_enhanced_engine',
    'get_reasoning_engine',
    'reason',
    'reason_with_wisdom',
    'select_reasoning_mode',
    'select_wisdom_modes',
]

增强版深度推理引擎
==================

集成儒道佛素兵 + 文明演化/文明经战七大智慧体系的深度推理引擎

版本: v2.1.0 (文明演化集成版)

作者: Somn AI
日期: 2026-04-02
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime

class ReasoningMode(Enum):
    """推理模式"""
    CHAIN_OF_THOUGHT = "chain_of_thought"
    TREE_OF_THOUGHTS = "tree_of_thoughts"
    GRAPH_OF_THOUGHTS = "graph_of_thoughts"
    META_REASONING = "meta_reasoning"
    NARRATIVE_REASONING = "narrative_reasoning"
    CONSULTING_REASONING = "consulting_reasoning"
    YINYANG_DIALECTICAL = "yinyang_dialectical"

class WisdomMode(Enum):
    """智慧模式 - 七大智慧体系"""
    CONFUCIAN = "儒家智慧"      # 以儒治世
    DAOIST = "道家智慧"         # 以道治身
    BUDDHIST = "佛家智慧"       # 以佛治心
    SUFU = "素书智慧"          # 五德decision
    MILITARY = "兵法智慧"      # 三十六计
    CIVILIZATION = "文明演化"   # 文明形成与长期连续性
    WAR_ECONOMY = "文明经战"    # 财政,动员,国家能力

@dataclass
class WisdomIntegratedReason:
    """智慧集成推理结果"""
    # 推理链
    reasoning_chain: List[str]
    
    # 七大智慧输入
    confucian_insight: str = ""      # 儒家洞察
    daoist_insight: str = ""         # 道家洞察
    buddhist_insight: str = ""       # 佛家洞察
    sufu_insight: str = ""          # 素书洞察
    military_insight: str = ""      # 兵法洞察
    civilization_insight: str = ""   # 文明演化洞察
    war_economy_insight: str = ""    # 文明经战洞察

    
    # fusiondecision
    fused_decision: str = ""
    confidence: float = 0.0
    
    # 评估维度
    ethics_score: float = 0.0       # 伦理评分
    wisdom_score: float = 0.0       # 智慧评分
    strategy_score: float = 0.0     # strategy评分
    
    # 风险提示
    warnings: List[str] = field(default_factory=list)

class EnhancedDeepReasoningEngine:
    """
    增强版深度推理引擎
    
    在原有7种推理模式基础上,集成七大智慧体系:
    1. 儒家智慧 - 仁义礼智信五常体系
    2. 道家智慧 - 道法自然阴阳平衡
    3. 佛家智慧 - 因缘和合平常心
    4. 素书智慧 - 五德decision修身指南
    5. 兵法智慧 - 三十六计攻防strategy
    6. 文明演化 - 文明形成,连续性与长期制度
    7. 文明经战 - 财政提取,资源动员与国家能力
    
    核心特性:
    - 智能选择最佳智慧组合
    - 多智慧fusion推理
    - 风险预警与评估
    """

    
    def __init__(self, project_root: str = None):
        self.project_root = project_root
        self.reasoning_modes = {mode.value: mode for mode in ReasoningMode}
        self.wisdom_modes = {mode.value: mode for mode in WisdomMode}
        
        # init智慧引擎调度器
        self._init_wisdom_dispatcher()
        
        # 关键词匹配规则
        self._init_keyword_rules()
    
    def _init_wisdom_dispatcher(self):
        """init智慧调度器"""
        self.wisdom_dispatcher = None
        try:
            from .wisdom_dispatcher import get_wisdom_dispatcher
            self.wisdom_dispatcher = get_wisdom_dispatcher()
        except ImportError:
            pass
    
    def _init_keyword_rules(self):
        """init关键词规则"""
        # 推理模式关键词
        self.mode_keywords = {
            ReasoningMode.CHAIN_OF_THOUGHT: ["步骤", "流程", "一步一步", "逻辑"],
            ReasoningMode.TREE_OF_THOUGHTS: ["选择", "方案", "多个", "分支"],
            ReasoningMode.GRAPH_OF_THOUGHTS: ["关系", "联系", "网络", "关联"],
            ReasoningMode.META_REASONING: ["反思", "思考思维", "自我", "元认知"],
            ReasoningMode.NARRATIVE_REASONING: ["故事", "案例", "叙事", "讲述"],
            ReasoningMode.CONSULTING_REASONING: ["咨询", "诊断", "方案", "增长"],
            ReasoningMode.YINYANG_DIALECTICAL: ["矛盾", "对立", "阴阳", "平衡"],
        }
        
        # 智慧模式关键词
        self.wisdom_keywords = {
            WisdomMode.CONFUCIAN: ["道德", "伦理", "仁义", "礼", "秩序", "人际关系"],
            WisdomMode.DAOIST: ["自然", "无为", "顺势", "平衡", "阴阳", "道法"],
            WisdomMode.BUDDHIST: ["心态", "平常心", "放下", "因缘", "解脱", "执念"],
            WisdomMode.SUFU: ["decision", "领导", "风险", "人才", "五德", "修身"],
            WisdomMode.MILITARY: ["竞争", "攻防", "strategy", "博弈", "知己知彼", "奇正"],
            WisdomMode.CIVILIZATION: ["文明", "制度", "连续性", "形成", "长期主义", "历史记忆"],
            WisdomMode.WAR_ECONOMY: ["财政", "税收", "动员", "国家能力", "后勤", "制度沉淀"],
        }

    
    def select_reasoning_mode(self, problem: str) -> ReasoningMode:
        """自动选择推理模式"""
        scores = {}
        
        for mode, keywords in self.mode_keywords.items():
            score = sum(1 for kw in keywords if kw in problem.lower())
            if score > 0:
                scores[mode] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return ReasoningMode.CONSULTING_REASONING  # 默认咨询推理
    
    def select_wisdom_modes(self, problem: str) -> List[WisdomMode]:
        """自动选择适用的智慧模式"""
        scores = {}
        
        for mode, keywords in self.wisdom_keywords.items():
            score = sum(1 for kw in keywords if kw in problem.lower())
            if score > 0:
                scores[mode] = score
        
        if not scores:
            return [WisdomMode.CONFUCIAN]  # 默认儒家
        
        # 返回得分最高的1-3个模式
        sorted_modes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [mode for mode, _ in sorted_modes[:3]]
    
    def reason_with_wisdom(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None,
        reasoning_mode: Optional[ReasoningMode] = None,
        wisdom_modes: Optional[List[WisdomMode]] = None
    ) -> WisdomIntegratedReason:
        """
        智慧集成推理 - 核心方法
        
        结合七大智慧体系进行深度推理
        """
        result = WisdomIntegratedReason(reasoning_chain=[])
        
        # 1. 选择推理模式
        reasoning_mode = reasoning_mode or self.select_reasoning_mode(problem)
        result.reasoning_chain.append(f"[推理模式]{reasoning_mode.value}")
        
        # 2. 选择智慧模式
        wisdom_modes = wisdom_modes or self.select_wisdom_modes(problem)
        wisdom_names = [wm.value for wm in wisdom_modes]
        result.reasoning_chain.append(f"[智慧模式]{' + '.join(wisdom_names)}")

        
        # 3. 调用智慧调度器
        if self.wisdom_dispatcher:
            fusion_result = self.wisdom_dispatcher.make_fusion_decision(
                problem, context
            )
            result.reasoning_chain.extend(fusion_result.reasoning_chain)
            result.fused_decision = fusion_result.final_decision
            result.confidence = fusion_result.overall_score
            result.ethics_score = fusion_result.ethics_score
            result.wisdom_score = fusion_result.wisdom_score
            result.strategy_score = fusion_result.strategy_score
            result.warnings = fusion_result.risk_warnings
        else:
            # 降级处理
            result = self._fallback_reasoning(problem, wisdom_modes)
        
        # 4. 各智慧洞察
        result = self._enrich_wisdom_insights(problem, wisdom_modes, result)
        
        return result
    
    def _fallback_reasoning(
        self,
        problem: str,
        wisdom_modes: List[WisdomMode]
    ) -> WisdomIntegratedReason:
        """降级推理(当智慧调度器不可用时)"""
        result = WisdomIntegratedReason(reasoning_chain=[])
        
        wisdom_names = [wm.value for wm in wisdom_modes]
        result.reasoning_chain.append(f"[智慧模式]{' + '.join(wisdom_names)}")
        
        # generate基本decision
        result.fused_decision = f"synthesize{''.join(wisdom_names)}处理"
        result.confidence = 0.7
        
        # 各智慧洞察
        result = self._enrich_wisdom_insights(problem, wisdom_modes, result)
        
        return result
    
    def _enrich_wisdom_insights(
        self,
        problem: str,
        wisdom_modes: List[WisdomMode],
        result: WisdomIntegratedReason
    ) -> WisdomIntegratedReason:
        """丰富各智慧洞察"""
        for mode in wisdom_modes:
            if mode == WisdomMode.CONFUCIAN:
                result.confucian_insight = self._get_confucian_insight(problem)
            elif mode == WisdomMode.DAOIST:
                result.daoist_insight = self._get_daoist_insight(problem)
            elif mode == WisdomMode.BUDDHIST:
                result.buddhist_insight = self._get_buddhist_insight(problem)
            elif mode == WisdomMode.SUFU:
                result.sufu_insight = self._get_sufu_insight(problem)
            elif mode == WisdomMode.MILITARY:
                result.military_insight = self._get_military_insight(problem)
            elif mode == WisdomMode.CIVILIZATION:
                result.civilization_insight = self._get_civilization_insight(problem)
            elif mode == WisdomMode.WAR_ECONOMY:
                result.war_economy_insight = self._get_war_economy_insight(problem)

        
        return result
    
    def _get_confucian_insight(self, problem: str) -> str:
        """儒家洞察"""
        return (
            "[儒家视角]\n"
            "仁者爱人:以仁爱之心对待相关方\n"
            "义者宜也:judge行为的正当性\n"
            "礼之用,和为贵:追求和谐有序\n"
            "推荐strategy:以德服人,建立长期信任关系"
        )
    
    def _get_daoist_insight(self, problem: str) -> str:
        """道家洞察"""
        return (
            "[道家视角]\n"
            "道法自然:顺应事物发展规律\n"
            "无为而治:有所为有所不为\n"
            "阴阳平衡:把握对立unified的规律\n"
            "推荐strategy:顺势而为,以柔克刚"
        )
    
    def _get_buddhist_insight(self, problem: str) -> str:
        """佛家洞察"""
        return (
            "[佛家视角]\n"
            "因缘和合:认清事物的因果关系\n"
            "平常心:保持平和的心态\n"
            "放下执念:不执着于成败得失\n"
            "推荐strategy:看淡得失,专注当下"
        )
    
    def _get_sufu_insight(self, problem: str) -> str:
        """素书洞察"""
        return (
            "[素书视角]\n"
            "道,德,仁,义,礼五德decision\n"
            "知人善任:识人用人之道\n"
            "遵义章46:风险预警系统\n"
            "推荐strategy:以五德为准则,审慎decision"
        )
    
    def _get_military_insight(self, problem: str) -> str:
        """兵法洞察"""
        return (
            "[兵法视角]\n"
            "知己知彼:全面了解情况\n"
            "先胜后战:充分准备再action\n"
            "奇正相生:常规与变通结合\n"
            "推荐strategy:谋定后动,出奇制胜"
        )

    def _get_civilization_insight(self, problem: str) -> str:
        """文明演化洞察"""
        return (
            "[文明演化视角]\n"
            "先看是否形成稳定剩余,秩序结构,跨代记忆与整合能力\n"
            "再看当前体系靠什么延续,哪些环节还停留在短期拼装\n"
            "推荐strategy:把长期制度,历史记忆与组织复制能力前置设计"
        )

    def _get_war_economy_insight(self, problem: str) -> str:
        """文明经战洞察"""
        return (
            "[文明经战视角]\n"
            "先定位问题卡在剩余形成,财政提取,资源动员,政治整合还是制度沉淀\n"
            "真正的长期能力,不是一次动员成功,而是能否沉淀为稳定机制\n"
            "推荐strategy:沿着剩余→提取→动员→整合→沉淀五段主链逐段补强"
        )
    
    def reason(

        self,
        problem: str,
        mode: Optional[ReasoningMode] = None,
        wisdom_modes: Optional[List[WisdomMode]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        unified推理接口
        
        Args:
            problem: 问题描述
            mode: 推理模式(可选,自动选择)
            wisdom_modes: 智慧模式列表(可选,自动选择)
            context: 上下文信息
        
        Returns:
            推理结果字典
        """
        # 自动选择模式
        if mode is None:
            mode = self.select_reasoning_mode(problem)
        
        if wisdom_modes is None:
            wisdom_modes = self.select_wisdom_modes(problem)
        
        # 智慧集成推理
        wisdom_result = self.reason_with_wisdom(
            problem,
            context=context,
            reasoning_mode=mode,
            wisdom_modes=wisdom_modes,
        )

        
        return {
            "problem": problem,
            "reasoning_mode": mode.value,
            "wisdom_modes": [wm.value for wm in wisdom_modes],
            "wisdom_result": wisdom_result,
            "timestamp": datetime.now().isoformat()
        }

# 全局单例
_enhanced_engine = None

# ============================================================
# 兼容层：为保持向后兼容，提供类型别名
# ============================================================

class ReasoningType(Enum):
    """推理类型枚举"""
    DEDUCTION = "deduction"
    INDUCTION = "induction"
    ABDUCTION = "abduction"
    ANALOGY = "analogy"
    CAUSAL = "causal"

@dataclass
class Premise:
    """前提条件"""
    content: str
    confidence: float = 0.8
    source: str = ""

@dataclass
class Conclusion:
    """推理结论"""
    content: str
    confidence: float = 0.8
    evidence: List[str] = None
    reasoning_chain: List[str] = None
    
    def __post_init__(self):
        if self.evidence is None:
            self.evidence = []
        if self.reasoning_chain is None:
            self.reasoning_chain = []

def get_reasoning_engine():
    """get推理引擎实例 - 兼容接口"""
    global _enhanced_engine
    if _enhanced_engine is None:
        _enhanced_engine = EnhancedDeepReasoningEngine()
    return _enhanced_engine

# 别名：ReasoningEngine = EnhancedDeepReasoningEngine
ReasoningEngine = EnhancedDeepReasoningEngine

def get_enhanced_engine() -> EnhancedDeepReasoningEngine:
    """get增强推理引擎单例"""
    global _enhanced_engine
    if _enhanced_engine is None:
        _enhanced_engine = EnhancedDeepReasoningEngine()
    return _enhanced_engine
