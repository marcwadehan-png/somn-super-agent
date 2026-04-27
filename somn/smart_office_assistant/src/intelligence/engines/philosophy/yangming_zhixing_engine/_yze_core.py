# -*- coding: utf-8 -*-
"""王阳明知行合一引擎 - 核心引擎模块"""
import logging
from typing import Dict, List, Any, Tuple

from ._yze_types import (
    KnowingLevel, ActionStage, ZhixingBarrier,
    KnowingAnalysis, ActionAnalysis, ZhixingLoop,
    TrueKnowledgeValidator, ActionStarterConfig, IterationDeepener
)
from ._yze_knowledge import ZhixingKnowledgeBase

__all__ = [
    'diagnose_zhixing',
    'iterate_deepen',
    'start_action',
    'validate_true_knowledge',
]

logger = logging.getLogger(__name__)

class ZhixingEngine(ZhixingKnowledgeBase):
    """
    王阳明知行合一执行引擎

    核心功能:
    1. 知行闭环诊断 - 完整分析知与行的关系
    2. 真知验证 - 区分假知与真知
    3. action启动 - 帮助打破知而不行
    4. 迭代深化 - 在action中持续深化认知
    5. 障碍破解 - 针对不同障碍的解决方案
    """

    def __init__(self):
        self.name = "王阳明知行合一执行引擎"
        self.version = "v1.0.0"
        logger.info(f"{self.name} {self.version} init完成")

    # ==================== 核心功能 ====================

    def diagnose_zhixing(self, knowing: str, action: str, context: str = "") -> ZhixingLoop:
        """知行闭环诊断 - 核心功能"""
        knowing_analysis = self._analyze_knowing(knowing)
        action_analysis = self._analyze_action(action)

        integration_score = self._calc_integration(knowing_analysis.score, action_analysis.score)
        is_true_knowledge = self._is_true_knowledge(knowing_analysis, action_analysis)
        is_zhi_action = self._is_zhi_action(action_analysis, knowing_analysis)

        gap_type, gap_reason = self._analyze_gap(knowing_analysis, action_analysis)
        closure_path = self._generate_closure_path(gap_type, knowing_analysis, action_analysis)
        immediate_action = self._get_immediate_action(gap_type, knowing_analysis, action_analysis)

        return ZhixingLoop(
            knowing=knowing_analysis,
            action=action_analysis,
            integration_score=integration_score,
            is_true_knowledge=is_true_knowledge,
            is_zhi_action=is_zhi_action,
            gap_type=gap_type,
            gap_reason=gap_reason,
            closure_path=closure_path,
            immediate_action=immediate_action,
            quote=self.ZHIXING_QUOTES["知行本质"][0]
        )

    def validate_true_knowledge(self, knowing: str, action: str) -> TrueKnowledgeValidator:
        """真知验证 - judge是真知还是假知"""
        validation_criteria = [
            {"criterion": "能用自己的话解释", "check": "理解深度", "weight": 0.2},
            {"criterion": "有实践经验和体会", "check": "实践经验", "weight": 0.3},
            {"criterion": "能够在压力下保持", "check": "知之坚定", "weight": 0.2},
            {"criterion": "能够教授他人", "check": "知之通透", "weight": 0.15},
            {"criterion": "自然带来action", "check": "知行一体", "weight": 0.15}
        ]

        knowing_analysis = self._analyze_knowing(knowing)
        action_analysis = self._analyze_action(action)

        confidence = 0.0
        evidence_for = []
        evidence_against = []

        if knowing_analysis.score >= 60:
            confidence += 0.2
            evidence_for.append("认知理解程度较高")
        else:
            evidence_against.append("认知理解程度不足")

        if action_analysis.score >= 60:
            confidence += 0.35
            evidence_for.append("有实际action和持续")
        else:
            evidence_against.append("缺乏action或action不足")

        if action_analysis.score > knowing_analysis.score:
            confidence += 0.15
            evidence_for.append("行先于知,说明知已内化")
        elif knowing_analysis.score > action_analysis.score + 20:
            evidence_against.append("知多行少,可能只是假知")

        is_true_knowledge = confidence >= 0.6 and action_analysis.score >= 40

        recommendation = ""
        if is_true_knowledge:
            recommendation = "你已获得真知,继续在事上磨练,使知行更加纯熟."
        else:
            recommendation = "你目前的知可能还停留在理论层面,需要通过action来验证和深化."

        return TrueKnowledgeValidator(
            is_true_knowledge=is_true_knowledge,
            validation_criteria=validation_criteria,
            evidence_for=evidence_for,
            evidence_against=evidence_against,
            confidence=confidence,
            recommendation=recommendation
        )

    def start_action(self, task: str, barrier_description: str = "") -> ActionStarterConfig:
        """action启动 - 帮助打破知而不行"""
        barrier_type = self._identify_barrier(barrier_description or task)
        barrier_info = self.BARRIER_SOLUTIONS.get(barrier_type, self.BARRIER_SOLUTIONS["MOTIVATION"])

        mini_action = self._generate_mini_action(task, barrier_type)
        motivation_boost = self._generate_motivation_boost(task)
        friction_reducers = self._generate_friction_reducers(task, barrier_type)
        start_trigger = self._generate_start_trigger(task, mini_action)

        return ActionStarterConfig(
            task=task,
            mini_action=mini_action,
            barrier_analysis=[{
                "barrier_type": barrier_type,
                "barrier_problem": barrier_info["problem"],
                "solution": barrier_info["solution"],
                "mini_action_suggestion": barrier_info["mini_action"]
            }],
            motivation_boost=motivation_boost,
            friction_reducers=friction_reducers,
            start_trigger=start_trigger,
            quote=self.ZHIXING_QUOTES["action启动"][0]
        )

    def iterate_deepen(self, current_knowing: str, current_action: str, cycle: int = 1) -> IterationDeepener:
        """迭代深化 - 在action中持续深化认知"""
        knowing_analysis = self._analyze_knowing(current_knowing)
        action_analysis = self._analyze_action(current_action)

        new_insight = self._generate_new_insight(knowing_analysis, action_analysis)
        improved_practice = self._generate_improved_practice(knowing_analysis, action_analysis, cycle)
        next_action = self._generate_next_action(knowing_analysis, action_analysis, cycle)
        wisdom_gain = self._generate_wisdom_gain(knowing_analysis, action_analysis, cycle)

        return IterationDeepener(
            cycle=cycle,
            current_knowing=knowing_analysis.level,
            current_action_stage=action_analysis.stage,
            new_insight=new_insight,
            improved_practice=improved_practice,
            next_action=next_action,
            wisdom_gain=wisdom_gain,
            quote=self.ZHIXING_QUOTES["迭代深化"][cycle % 3]
        )

    # ==================== 辅助方法 ====================

    def _analyze_knowing(self, knowing: str) -> KnowingAnalysis:
        """分析知的层次"""
        text_lower = knowing.lower()
        score = 50.0
        level = KnowingLevel.UNDERSTANDING

        level_keywords = {
            KnowingLevel.NATURAL: ["自然", "无条件", "本能", "身心合一"],
            KnowingLevel.INTEGRATED: ["融会贯通", "彻底明白", "透彻"],
            KnowingLevel.PRACTICED: ["做过", "实践过", "有经验", "体验过"],
            KnowingLevel.UNDERSTANDING: ["理解", "知道", "明白"],
            KnowingLevel.HEARSAY: ["听说过", "好像", "大概"],
            KnowingLevel.UNKNOWN: ["不知道", "不了解", "不清楚"]
        }

        for lv, keywords in level_keywords.items():
            if any(kw in text_lower for kw in keywords):
                level = lv
                break

        level_def = self.KNOWING_LEVELS[level.name]
        base_score = (level_def["score_range"][0] + level_def["score_range"][1]) / 2

        boosters = ["深刻", "真正", "彻底", "本质"]
        for b in boosters:
            if b in knowing:
                base_score += 10

        reducers = ["大概", "好像", "可能", "也许"]
        for r in reducers:
            if r in knowing:
                base_score -= 15

        score = max(0, min(100, base_score))
        elements = self._extract_knowing_elements(knowing)
        depth_path = self._generate_deepening_path(level)

        return KnowingAnalysis(
            level=level,
            score=score,
            elements=elements,
            barriers=[],
            depth_path=depth_path,
            evidence=knowing,
            quote=self.ZHIXING_QUOTES["知行本质"][0]
        )

    def _analyze_action(self, action: str) -> ActionAnalysis:
        """分析行的阶段"""
        text_lower = action.lower()
        stage = ActionStage.NOT_STARTED
        score = 10.0

        for st_name, stage_def in self.ACTION_STAGES.items():
            for indicator in stage_def["indicators"]:
                if indicator in text_lower:
                    stage = ActionStage[st_name]
                    score = (stage_def["score_range"][0] + stage_def["score_range"][1]) / 2
                    break

        action_words = ["做", "开始", "坚持", "执行", "完成"]
        count = sum(1 for w in action_words if w in text_lower)
        score += count * 5

        delay_words = ["等", "以后", "还没", "没做", "拖延"]
        count = sum(1 for w in delay_words if w in text_lower)
        score -= count * 10

        score = max(0, min(100, score))
        obstacles = self._extract_obstacles(action)
        improvement = self._generate_improvement(stage)

        return ActionAnalysis(
            stage=stage,
            score=score,
            quality=self._assess_quality(score),
            obstacles=obstacles,
            improvement=improvement,
            evidence=action,
            quote=self.ZHIXING_QUOTES["知行本质"][1]
        )

    def _calc_integration(self, knowing_score: float, action_score: float) -> float:
        """计算知行合一程度"""
        if knowing_score == 0 and action_score == 0:
            return 0.0

        gap = abs(knowing_score - action_score)
        avg = (knowing_score + action_score) / 2
        penalty = gap * 0.4

        bonus = 0
        if 50 <= knowing_score <= 80 and 50 <= action_score <= 80:
            bonus = 15

        integration = avg - penalty + bonus
        return max(0, min(100, integration))

    def _is_true_knowledge(self, knowing: KnowingAnalysis, action: ActionAnalysis) -> bool:
        """judge是否是真知"""
        return knowing.score >= 60 and action.score >= 40

    def _is_zhi_action(self, action: ActionAnalysis, knowing: KnowingAnalysis) -> bool:
        """judge是否是知之action"""
        if knowing.score == 0:
            return False
        return action.score >= knowing.score * 0.6

    def _analyze_gap(self, knowing: KnowingAnalysis, action: ActionAnalysis) -> Tuple[str, str]:
        """分析知行差距"""
        gap = knowing.score - action.score

        if gap > 25:
            return ("知多行少", "认知丰富但action不足,需要将知转化为行")
        elif gap < -25:
            return ("行多知少", "埋头action但反思不足,需要深化认知")
        else:
            return ("知行平衡", "知行相对平衡,可进一步深化")

    def _generate_closure_path(self, gap_type: str, knowing: KnowingAnalysis,
                               action: ActionAnalysis) -> List[str]:
        """generate闭环路径"""
        paths = {
            "知多行少": [
                "1. 设定最小action:从一件小事开始",
                "2. 立即执行:不要等到完美再开始",
                "3. 在action中验证认知",
                "4. 复盘总结:action带来了什么新认知?"
            ],
            "行多知少": [
                "1. 暂停action:留出反思时间",
                "2. 提炼经验:这次action学到了什么?",
                "3. 深化理解:上升到规律和原则",
                "4. 再次实践:用深化后的认知指导新action"
            ],
            "知行平衡": [
                "1. 持续迭代:在知与行之间循环",
                "2. 追求精进:从80分到90分",
                "3. 传授他人:教是最好的学",
                "4. 挑战更高:在更大事情上磨练"
            ]
        }
        return paths.get(gap_type, paths["知行平衡"])

    def _get_immediate_action(self, gap_type: str, knowing: KnowingAnalysis,
                              action: ActionAnalysis) -> str:
        """确定立即action"""
        if gap_type == "知多行少":
            return "不要想了,现在就做一件最小的事.哪怕只做5分钟,也比一直想强."
        elif gap_type == "行多知少":
            return "先停下来想一想,这次action的本质是什么?学到了什么?"
        else:
            return "知行已经接近,找一个小的切入口,继续迭代深化."

    def _identify_barrier(self, description: str) -> str:
        """recognize障碍类型"""
        text = description.lower()

        if any(w in text for w in ["怎么", "不会", "不知道怎么做", "方法"]):
            return "CAPABILITY"
        elif any(w in text for w in ["为什么", "意义", "不想", "动力"]):
            return "MOTIVATION"
        elif any(w in text for w in ["环境", "条件", "时间", "没空"]):
            return "ENVIRONMENT"
        elif any(w in text for w in ["欲望", "贪", "私", "私欲"]):
            return "DESIRE"
        else:
            return "COGNITIVE"

    def _generate_mini_action(self, task: str, barrier: str) -> str:
        """generate最小action"""
        return f"立即做{task}的第一步,哪怕只做1分钟"

    def _generate_motivation_boost(self, task: str) -> List[str]:
        """generate动力提升strategy"""
        return [
            f"想象完成{task}后带来的三个好处",
            "找到做这件事的内在意义",
            "给自己一个承诺:现在就做"
        ]

    def _generate_friction_reducers(self, task: str, barrier: str) -> List[str]:
        """generate减少阻力strategy"""
        reducers = {
            "COGNITIVE": ["先理解一个核心要点", "找一个具体例子"],
            "MOTIVATION": ["降低期望,先做5分钟", "找一个同伴互相监督"],
            "CAPABILITY": ["把任务分解为最简单的一步", "找一个人工智能帮你"],
            "ENVIRONMENT": ["找一个5分钟的窗口", "先清理书桌/准备工具"],
            "DESIRE": ["问自己:什么更重要?", "想象不做这件事的后果"]
        }
        return reducers.get(barrier, ["先做再说"])

    def _generate_start_trigger(self, task: str, mini_action: str) -> str:
        """generate启动触发器"""
        return f"设置一个计时器,现在就开始:{mini_action}"

    def _generate_new_insight(self, knowing: KnowingAnalysis,
                             action: ActionAnalysis) -> str:
        """generate新洞察"""
        insights = {
            KnowingLevel.HEARSAY: "知与行之间的距离,比你想象的更大",
            KnowingLevel.UNDERSTANDING: "理论理解只是开始,真正的理解在action中",
            KnowingLevel.PRACTICED: "实践出真知,但还需要提炼规律",
            KnowingLevel.INTEGRATED: "知行已近一体,继续深化可达自然",
            KnowingLevel.NATURAL: "你已经接近圣人境界,分享你的智慧"
        }
        return insights.get(knowing.level, "")

    def _generate_improved_practice(self, knowing: KnowingAnalysis,
                                   action: ActionAnalysis,
                                   cycle: int) -> str:
        """generate改进action"""
        return f"第{cycle+1}轮迭代:在上一轮基础上,提升10%action量"

    def _generate_next_action(self, knowing: KnowingAnalysis,
                             action: ActionAnalysis,
                             cycle: int) -> str:
        """generate下一步action"""
        if action.stage == ActionStage.NOT_STARTED:
            return "立即开始,做第一件事"
        elif action.stage == ActionStage.DELAYED:
            return "打破拖延,现在就做"
        elif action.stage == ActionStage.STARTED:
            return "坚持10分钟,形成惯性"
        else:
            return "保持节奏,持续迭代"

    def _generate_wisdom_gain(self, knowing: KnowingAnalysis,
                             action: ActionAnalysis,
                             cycle: int) -> str:
        """generate智慧收获"""
        return f"经过第{cycle}轮知行迭代,你对这件事的理解更加深刻,action更加自然"

    def _extract_knowing_elements(self, text: str) -> List[str]:
        """提取知的构成要素"""
        elements = []
        patterns = {
            "what": ["是什么", "定义", "概念"],
            "why": ["为什么", "原因"],
            "how": ["怎么", "方法"],
            "when": ["何时", "时机"]
        }
        for key, words in patterns.items():
            if any(w in text for w in words):
                elements.append(f"要素-{key}:已理解")
        return elements or ["待分析"]

    def _extract_obstacles(self, text: str) -> List[str]:
        """提取action障碍"""
        obstacles = []
        patterns = {
            "恐惧": ["怕", "不敢", "担心"],
            "拖延": ["等", "以后", "算了"],
            "困难": ["难", "做不到"],
            "懒惰": ["懒", "不想动"]
        }
        for key, words in patterns.items():
            if any(w in text for w in words):
                obstacles.append(key)
        return obstacles

    def _generate_deepening_path(self, level: KnowingLevel) -> List[str]:
        """generate深化路径"""
        paths = {
            KnowingLevel.HEARSAY: ["系统学习理论", "做笔记", "与人讨论"],
            KnowingLevel.UNDERSTANDING: ["联系实际案例", "尝试应用", "反思效果"],
            KnowingLevel.PRACTICED: ["提炼规律", "总结经验", "分享传授"],
            KnowingLevel.INTEGRATED: ["持续精进", "挑战更高", "帮助他人"],
            KnowingLevel.NATURAL: ["保持觉知", "传承智慧"]
        }
        return paths.get(level, [])

    def _generate_improvement(self, stage: ActionStage) -> List[str]:
        """generate改进action"""
        improvements = {
            ActionStage.NOT_STARTED: ["设定起始点", "立即开始"],
            ActionStage.DELAYED: ["设定截止时间", "找人监督"],
            ActionStage.STARTED: ["建立习惯", "加入反馈"],
            ActionStage.PERSISTING: ["优化方法", "提升效率"],
            ActionStage.HABITUAL: ["挑战更高目标"],
            ActionStage.MASTERED: ["传承分享"]
        }
        return improvements.get(stage, [])

    def _assess_quality(self, score: float) -> str:
        """评估action质量"""
        if score >= 90:
            return "卓越"
        elif score >= 70:
            return "良好"
        elif score >= 50:
            return "一般"
        else:
            return "待改进"

    # ---- fusion 兼容方法（v1.0.0）----
    def analyze_zhixing(self, situation: str) -> Dict:
        """
        分析知行状态，包装 diagnose_zhixing。
        Args:
            situation: 情境描述（用于提取 knowing/action）
        Returns:
            适配 fusion 期望的字典结构
        """
        result = self.diagnose_zhixing(
            knowing=situation,
            action="",
            context="analyze_zhixing"
        )
        return {
            "知行合一度": f"{result.integration_score:.0f}%",
            "是否真知": "是" if result.is_true_knowledge else "否",
            "存在问题": "" if result.is_true_knowledge else f"知行差距:{result.gap_type}",
            "知之得分": result.knowing.score,
            "行之所处": result.action.stage.value,
            "gap_type": result.gap_type,
            "immediate_action": result.immediate_action
        }

    def get_daily_routine(self) -> Dict:
        """
        每日知行合一实践日程，包装 diagnose_zhixing。
        Returns:
            适配 fusion 期望的字典结构
        """
        # 通用每日实践：知行诊断框架
        result = self.diagnose_zhixing(
            knowing="每日三省吾身",
            action="知行合一实践",
            context="daily_routine"
        )
        return {
            "晨起": {
                "功课": "静坐省心 - 澄心静虑",
                "要点": "觉知内心善恶，知之真切笃实处即是行"
            },
            "日中": {
                "功课": "事上磨练 - 专注当下",
                "要点": "良知指引，为善去恶，知而不行只是未知"
            },
            "暮时": {
                "功课": "省察克治 - 检点起心动念",
                "要点": "知行合一否？是否私欲遮蔽？"
            },
            "睡前": {
                "功课": "涵养蓄势 - 静坐调息",
                "要点": "养护心体，良知愈明则知行愈一",
                "知行合一度": f"{result.integration_score:.0f}%",
                "是否真知": "是" if result.is_true_knowledge else "否"
            },
            "经典": "知是行的主意，行是知的功夫；知之真切笃实处即是行"
        }
