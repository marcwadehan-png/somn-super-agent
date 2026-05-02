"""
__all__ = [
    'apply_five_step_method',
    'apply_thinking_type',
    'assess_thinking_habits',
    'create_training_plan',
    'five_step_thinking',
    'get_critical_thinking_checklist',
    'get_doing_learning',
    'get_doing_learning_guidance',
    'guide_five_step',
    'guide_step',
    'integrate_with_somn',
]

杜威思维训练引擎 - Dewey Thinking Training Engine
v7.0.0 版本

fusion约翰·杜威<思维的本质>核心思想,构建反省思维训练系统:

[杜威核心思想]
1. 反省思维的本质 - 对问题深入思考,系统分析,寻找解决方案
2. 思维五步法 - 暗示→困难→假设→推理→验证
3. 教育即生活 - 教育本身就是生活,在生活中学习
4. 做中学 - 从经验中学习,动手操作

[思维五步法]
1. 暗示:问题出现,感到困惑
2. 困难:感到难以解决
3. 假设:提出可能的解释或解决方案
4. 推理:推演假设的结果
5. 验证:检验假设是否成立

[思维习惯培养]
1. 质疑习惯 - 不盲从,问为什么
2. 探究习惯 - 深入探索,寻求真相
3. 反思习惯 - 回看过程,总结经验

[民主与思维]
民主需要独立思考的公民,批判性思维是民主的基础

版本历史:
- v7.0.0 (2026-04-02): 初始版本,fusion杜威反省思维理论
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class ThinkingStep(Enum):
    """思维五步法"""
    SUGGESTION = "暗示"     # 问题出现,感到困惑
    DIFFICULTY = "困难"     # 感到难以解决
    HYPOTHESIS = "假设"     # 提出可能的解释或解决方案
    REASONING = "推理"      # 推演假设的结果
    VERIFICATION = "验证"   # 检验假设是否成立

class ThinkingHabit(Enum):
    """思维习惯"""
    QUESTIONING = "质疑"    # 不盲从,问为什么
    INQUIRING = "探究"      # 深入探索,寻求真相
    REFLECTIVE = "反思"     # 回看过程,总结经验

class ThinkingType(Enum):
    """思维方式"""
    DIVERGENT = "发散思维"   # 多角度思考
    CONVERGENT = "收敛思维"   # 评估选择最佳
    CRITICAL = "批判性思维"   # 质疑验证
    CREATIVE = "创造性思维"   # 突破创新
    SYSTEMATIC = "系统性思维" # 整体全局

@dataclass
class FiveStepAnalysis:
    """五步思维分析"""
    step: ThinkingStep
    description: str
    prompt_questions: List[str]
    output: str = ""
    quality_score: float = 0.0  # 0-1

@dataclass
class ThinkingProcess:
    """完整思维过程"""
    problem: str
    context: str
    steps: List[FiveStepAnalysis]
    final_solution: str
    confidence: float
    alternatives: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)

@dataclass
class HabitAssessment:
    """思维习惯评估"""
    habit: ThinkingHabit
    current_level: float  # 0-3
    indicators: List[str]
    improvement_suggestions: List[str]

@dataclass
class ThinkingTrainingPlan:
    """思维训练计划"""
    target_habit: ThinkingHabit
    daily_practices: List[str]
    weekly_exercises: List[str]
    progress_indicators: List[str]
    expected_outcomes: List[str]

class DeweyThinkingEngine:
    """
    杜威思维训练引擎
    
    功能:
    1. 思维五步法 - 完整的反省思维过程
    2. 问题解决训练 - 系统的思维过程
    3. 思维习惯评估 - 质疑/探究/反思能力
    4. 思维训练计划 - 每日练习方案
    5. 做中学指导 - 实践导向学习
    
    应用场景:
    - 复杂问题分析
    - decision思维训练
    - 批判性思维培养
    - 创造性思维激发
    """
    
    # 杜威经典语录
    DEWEY_QUOTES = {
        "思维本质": "思维是我们用于解决实际问题的一种工具.",
        "反省思维": "教育必须以反省思维为目的.",
        "做中学": "从经验中学习是最好的学习方式.",
        "问题解决": "问题不是被解答的,而是被理解的.",
        "民主思维": "民主社会需要能够独立思考的公民."
    }
    
    # 五步法详细指南
    FIVE_STEP_GUIDE = {
        ThinkingStep.SUGGESTION: {
            "description": "问题出现,感到困惑",
            "key_questions": [
                "我真正的问题是什么?",
                "是什么让我感到困惑?",
                "有什么异常或矛盾的现象?",
                "我为什么会关注这个问题?"
            ],
            "techniques": [
                "保持开放心态",
                "接受不确定性",
                "不急于下结论"
            ]
        },
        ThinkingStep.DIFFICULTY: {
            "description": "感到难以解决",
            "key_questions": [
                "具体困难在哪里?",
                "我已知什么?未知什么?",
                "障碍是什么?",
                "需要什么信息或资源?"
            ],
            "techniques": [
                "分解问题为小问题",
                "recognize关键变量",
                "明确已知与未知"
            ]
        },
        ThinkingStep.HYPOTHESIS: {
            "description": "提出可能的解释或解决方案",
            "key_questions": [
                "可能的解释有哪些?",
                "有哪些解决方案?",
                "有没有类似的成功案例?",
                "别人的观点是什么?"
            ],
            "techniques": [
                "头脑风暴",
                "多角度思考",
                "借鉴相关经验"
            ]
        },
        ThinkingStep.REASONING: {
            "description": "推演假设的结果",
            "key_questions": [
                "如果这个假设成立,会怎样?",
                "逻辑推理的链条是什么?",
                "有没有矛盾或漏洞?",
                "支持或反对的证据有哪些?"
            ],
            "techniques": [
                "逻辑推理",
                "证据评估",
                "假设检验准备"
            ]
        },
        ThinkingStep.VERIFICATION: {
            "description": "检验假设是否成立",
            "key_questions": [
                "这个假设能被验证吗?",
                "证据是否充分?",
                "结论是否可靠?",
                "有什么遗漏或偏差?"
            ],
            "techniques": [
                "实践检验",
                "证据synthesize",
                "结论修正"
            ]
        }
    }
    
    # 思维习惯训练方法
    HABIT_TRAINING = {
        ThinkingHabit.QUESTIONING: {
            "name": "质疑习惯",
            "description": "不盲从,问为什么,寻求证据",
            "daily_practices": [
                "每天质疑一个'常识'",
                "问5个'为什么'直到找到根本原因",
                "区分事实与观点"
            ],
            "weekly_exercises": [
                "写一篇质疑性分析",
                "辩论:站在反对角度思考"
            ],
            "progress_indicators": [
                "能提出有质量的质疑",
                "不轻易接受表面答案",
                "能看到问题的多个方面"
            ]
        },
        ThinkingHabit.INQUIRING: {
            "name": "探究习惯",
            "description": "深入探索,系统分析,寻求真相",
            "daily_practices": [
                "深入了解一个感兴趣的话题",
                "多查证一个信息来源",
                "记录探究过程中的发现"
            ],
            "weekly_exercises": [
                "完成一个小课题研究",
                "做一次深度访谈"
            ],
            "progress_indicators": [
                "能进行系统性的探究",
                "能找到可靠的资料来源",
                "能形成完整的分析框架"
            ]
        },
        ThinkingHabit.REFLECTIVE: {
            "name": "反思习惯",
            "description": "回看过程,总结经验,持续改进",
            "daily_practices": [
                "每天写反思日记",
                "复盘一个重要decision",
                "记录错误和教训"
            ],
            "weekly_exercises": [
                "分析一周的学习/工作",
                "调整下一周的strategy"
            ],
            "progress_indicators": [
                "能从经验中学习",
                "不重复同样的错误",
                "能提炼普适性的教训"
            ]
        }
    }
    
    # 思维方式应用
    THINKING_TYPE_APPLICATION = {
        ThinkingType.DIVERGENT: {
            "when": "需要创意,多方案选择时",
            "how": "自由发散,延迟评判,数量优先",
            "tools": ["头脑风暴", "思维导图", "SCAMPER"]
        },
        ThinkingType.CONVERGENT: {
            "when": "需要评估选择,做出decision时",
            "how": "标准评估,加权打分,逻辑推理",
            "tools": ["decision矩阵", "成本收益分析", "SWOT"]
        },
        ThinkingType.CRITICAL: {
            "when": "需要验证假设,评估论证时",
            "how": "质疑前提,检查逻辑,评估证据",
            "tools": ["逻辑谬误recognize", "证据评估", "苏格拉底提问"]
        },
        ThinkingType.CREATIVE: {
            "when": "需要突破常规,创新解决方案时",
            "how": "打破框架,跨界借鉴,极端思考",
            "tools": ["六顶思考帽", "反向思考", "类比思维"]
        },
        ThinkingType.SYSTEMATIC: {
            "when": "需要整体把握,复杂分析时",
            "how": "分解要素,理清关系,整体优化",
            "tools": ["系统动力学", "因果图", "利益相关者分析"]
        }
    }
    
    def __init__(self):
        """init杜威思维引擎"""
        self.name = "杜威思维训练引擎"
        self.version="6.2.0"
        logger.info(f"{self.name} {self.version} init完成")
    
    def apply_five_step_method(self,
                                problem: str,
                                context: str = "") -> ThinkingProcess:
        """
        应用思维五步法
        
        Args:
            problem: 待解决的问题
            context: 背景上下文
        
        Returns:
            完整的思维过程
        """
        steps = []
        
        for step in ThinkingStep:
            guide = self.FIVE_STEP_GUIDE[step]
            step_analysis = FiveStepAnalysis(
                step=step,
                description=guide["description"],
                prompt_questions=guide["key_questions"],
                output="",
                quality_score=0.0
            )
            steps.append(step_analysis)
        
        # generate结果
        process = ThinkingProcess(
            problem=problem,
            context=context,
            steps=steps,
            final_solution="",
            confidence=0.0,
            alternatives=["方案A", "方案B", "方案C"],
            evidence=["证据1", "证据2"],
            limitations=["限制1", "限制2"]
        )
        
        return process
    
    def guide_five_step(self,
                        problem: str,
                        current_step: ThinkingStep,
                        previous_outputs: Dict[ThinkingStep, str]) -> Dict[str, Any]:
        """
        引导五步法某一步
        
        Args:
            problem: 问题描述
            current_step: 当前步骤
            previous_outputs: 前几步的输出
        
        Returns:
            指导建议
        """
        guide = self.FIVE_STEP_GUIDE[current_step]
        
        guidance = {
            "current_step": current_step.value,
            "description": guide["description"],
            "questions_to_ask": guide["key_questions"],
            "techniques": guide["techniques"],
            "tips": [],
            "next_step": None
        }
        
        # 添加提示
        if current_step == ThinkingStep.SUGGESTION:
            guidance["tips"] = [
                "不要急于解决问题,先理解问题",
                "用一句话描述你的真正问题",
                "注意那些让你感到'不对劲'的地方"
            ]
            guidance["next_step"] = ThinkingStep.DIFFICULTY.value
            
        elif current_step == ThinkingStep.DIFFICULTY:
            guidance["tips"] = [
                "将大困难分解为小困难",
                "明确你知道什么,不知道什么",
                "列出解决问题需要的信息"
            ]
            guidance["next_step"] = ThinkingStep.HYPOTHESIS.value
            
        elif current_step == ThinkingStep.HYPOTHESIS:
            guidance["tips"] = [
                "尽可能多地提出假设,不要评判",
                "考虑最简单的解释",
                "借鉴他人的成功经验"
            ]
            guidance["next_step"] = ThinkingStep.REASONING.value
            
        elif current_step == ThinkingStep.REASONING:
            guidance["tips"] = [
                "画出推理的逻辑链条",
                "检查每个环节是否通顺",
                "寻找可能的反例"
            ]
            guidance["next_step"] = ThinkingStep.VERIFICATION.value
            
        else:  # VERIFICATION
            guidance["tips"] = [
                "设计可行的验证方法",
                "准备好修正你的假设",
                "记录验证结果和教训"
            ]
            guidance["next_step"] = "完成"
        
        return guidance
    
    def assess_thinking_habits(self,
                                habit_responses: Dict[ThinkingHabit, int]) -> List[HabitAssessment]:
        """
        评估思维习惯
        
        Args:
            habit_responses: 各习惯的评估分数(0-3)
        
        Returns:
            习惯评估结果
        """
        assessments = []
        
        for habit, score in habit_responses.items():
            training = self.HABIT_TRAINING[habit]
            
            assessment = HabitAssessment(
                habit=habit,
                current_level=score,
                indicators=self._get_habit_indicators(habit, score),
                improvement_suggestions=training["daily_practices"][:2]
            )
            assessments.append(assessment)
        
        return assessments
    
    def _get_habit_indicators(self,
                             habit: ThinkingHabit,
                             level: int) -> List[str]:
        """get习惯评估metrics"""
        indicators = {
            ThinkingHabit.QUESTIONING: {
                0: "倾向于接受表面答案",
                1: "偶尔会质疑,但不够深入",
                2: "经常质疑,能找到部分原因",
                3: "系统性质疑,能找到根本原因"
            },
            ThinkingHabit.INQUIRING: {
                0: "浅尝辄止,不深入",
                1: "偶尔深入,但缺乏系统性",
                2: "经常深入研究,形成框架",
                3: "系统探究,形成完整知识体系"
            },
            ThinkingHabit.REFLECTIVE: {
                0: "不反思,重复同样错误",
                1: "偶尔反思,但不够系统",
                2: "经常反思,能提炼经验",
                3: "深度反思,形成方法论"
            }
        }
        
        return [indicators[habit].get(level, "")]
    
    def create_training_plan(self,
                            target_habits: List[ThinkingHabit],
                            duration_weeks: int = 4) -> List[ThinkingTrainingPlan]:
        """
        创建思维训练计划
        
        Args:
            target_habits: 目标培养的习惯
            duration_weeks: 训练周期(周)
        
        Returns:
            训练计划
        """
        plans = []
        
        for habit in target_habits:
            training = self.HABIT_TRAINING[habit]
            
            plan = ThinkingTrainingPlan(
                target_habit=habit,
                daily_practices=training["daily_practices"],
                weekly_exercises=training["weekly_exercises"],
                progress_indicators=training["progress_indicators"],
                expected_outcomes=[
                    f"{training['name']}能力显著提升",
                    "能将该习惯应用于日常工作",
                    "形成稳定的思维方式"
                ]
            )
            plans.append(plan)
        
        return plans
    
    def get_doing_learning_guidance(self,
                                    topic: str,
                                    current_level: str) -> Dict[str, Any]:
        """
        做中学学习指导
        
        Args:
            topic: 学习主题
            current_level: 当前水平
        
        Returns:
            学习方案
        """
        guidance = {
            "topic": topic,
            "philosophy": "做中学 - 从经验中学习是最好的学习方式",
            "approach": "杜威实用主义学习法",
            "steps": [
                {
                    "step": 1,
                    "name": "体验",
                    "description": "亲身参与,动手实践",
                    "action": f"找机会实际接触{topic}"
                },
                {
                    "step": 2,
                    "name": "反思",
                    "description": "回看经验,思考意义",
                    "action": "记录做了什么,感受如何"
                },
                {
                    "step": 3,
                    "name": "概念化",
                    "description": "提炼规律,形成理解",
                    "action": "从经验中总结出原则"
                },
                {
                    "step": 4,
                    "name": "应用",
                    "description": "将理解应用于新情境",
                    "action": "在类似但不同的情境中实践"
                }
            ],
            "example_project": self._generate_practice_project(topic, current_level)
        }
        
        return guidance
    
    def _generate_practice_project(self,
                                  topic: str,
                                  level: str) -> Dict[str, str]:
        """generate实践项目"""
        projects = {
            "beginner": {
                "name": f"{topic}入门项目",
                "duration": "1周",
                "tasks": [
                    "完成一个基础任务",
                    "记录过程和结果",
                    "反思学到了什么"
                ]
            },
            "intermediate": {
                "name": f"{topic}进阶项目",
                "duration": "2-4周",
                "tasks": [
                    "完成一个有一定难度的任务",
                    "教授他人学到的知识",
                    "总结可复用的方法"
                ]
            },
            "advanced": {
                "name": f"{topic}精通项目",
                "duration": "1-3个月",
                "tasks": [
                    "完成一个复杂/创新项目",
                    "形成自己的方法论",
                    "帮助初学者入门"
                ]
            }
        }
        
        return projects.get(level, projects["beginner"])
    
    def apply_thinking_type(self,
                           problem: str,
                           thinking_type: ThinkingType) -> Dict[str, Any]:
        """
        应用特定思维方式
        
        Args:
            problem: 问题描述
            thinking_type: 思维方式
        
        Returns:
            思维指导
        """
        app = self.THINKING_TYPE_APPLICATION[thinking_type]
        
        result = {
            "thinking_type": thinking_type.value,
            "when_to_use": app["when"],
            "how_to_apply": app["how"],
            "tools": app["tools"],
            "problem": problem,
            "questions": [],
            "process": []
        }
        
        if thinking_type == ThinkingType.DIVERGENT:
            result["questions"] = [
                "有哪些可能的解决方案?",
                "有没有完全不同的思路?",
                "跨界能否借鉴?",
                "最疯狂的想法是什么?"
            ]
            result["process"] = ["收集想法", "合并相似想法", "完善可行想法"]
            
        elif thinking_type == ThinkingType.CONVERGENT:
            result["questions"] = [
                "评估标准是什么?",
                "各方案的优缺点?",
                "权重如何分配?",
                "最终选择哪个?"
            ]
            result["process"] = ["定义标准", "评估方案", "加权计算", "做出decision"]
            
        elif thinking_type == ThinkingType.CRITICAL:
            result["questions"] = [
                "前提假设是什么?",
                "逻辑推理是否通顺?",
                "证据是否充分?",
                "有什么替代解释?"
            ]
            result["process"] = ["质疑前提", "检验逻辑", "评估证据", "修正结论"]
            
        elif thinking_type == ThinkingType.CREATIVE:
            result["questions"] = [
                "为什么必须这样做?",
                "反面是什么?",
                "能组合什么?",
                "能缩小/放大什么?"
            ]
            result["process"] = ["打破框架", "反向思考", "跨界组合", "极端化"]
            
        else:  # SYSTEMATIC
            result["questions"] = [
                "有哪些关键要素?",
                "要素之间有什么关系?",
                "谁是利益相关者?",
                "系统如何演化?"
            ]
            result["process"] = ["分解要素", "recognize关系", "建模分析", "整体优化"]
        
        return result
    
    def get_critical_thinking_checklist(self) -> List[str]:
        """
        get批判性思维检查清单
        
        Returns:
            检查要点
        """
        return [
            "问题的核心是什么?",
            "前提假设是什么?这些假设是否可靠?",
            "推理过程是否通顺?有没有逻辑漏洞?",
            "证据是否充分?来源是否可靠?",
            "有没有遗漏重要信息?",
            "有没有其他可能的解释?",
            "是否存在偏见或利益冲突?",
            "结论是否超出了证据支持的范围?",
            "这个问题与其他问题有什么关系?",
            "我的立场是什么?为什么持有这个立场?"
        ]
    
    def integrate_with_somn(self,
                           user_query: str,
                           context: Dict[str, Any]) -> Dict[str, Any]:
        """
        与Somn系统fusion
        
        Args:
            user_query: 用户查询
            context: 上下文
        
        Returns:
            杜威思维分析结果
        """
        query_lower = user_query.lower()
        
        # 确定思维方式
        if any(word in query_lower for word in ["创意", "创新", "突破"]):
            thinking_type = ThinkingType.CREATIVE
        elif any(word in query_lower for word in ["分析", "评估", "judge"]):
            thinking_type = ThinkingType.CRITICAL
        elif any(word in query_lower for word in ["decision", "选择", "方案"]):
            thinking_type = ThinkingType.CONVERGENT
        else:
            thinking_type = ThinkingType.SYSTEMATIC
        
        # get杜威语录
        quote_key = "反省思维" if "思维" in user_query else "做中学"
        quote = self.DEWEY_QUOTES.get(quote_key, "")
        
        result = {
            "engine": "杜威思维训练引擎",
            "thinking_type": thinking_type.value,
            "dewey_quote": quote,
            "philosophy": "教育必须以反省思维为目的",
            "method": "思维五步法",
            "five_steps": [step.value for step in ThinkingStep],
            "thinking_guidance": self.apply_thinking_type(user_query, thinking_type),
            "habits": [habit.value for habit in ThinkingHabit],
            "critical_checklist": self.get_critical_thinking_checklist()[:5]
        }
        
        return result

# 便捷函数
def five_step_thinking(problem: str) -> ThinkingProcess:
    """快速五步思维"""
    engine = DeweyThinkingEngine()
    return engine.apply_five_step_method(problem)

def guide_step(problem: str, step: str) -> Dict[str, Any]:
    """引导某一步思维"""
    engine = DeweyThinkingEngine()
    step_enum = ThinkingStep[step.upper()]
    return engine.guide_five_step(problem, step_enum, {})

def get_doing_learning(topic: str, level: str = "beginner") -> Dict[str, Any]:
    """快速做中学指导"""
    engine = DeweyThinkingEngine()
    return engine.get_doing_learning_guidance(topic, level)

# 向后兼容别名
DeweyStep = ThinkingStep  # 兼容 supreme_wisdom_coordinator.py 导入

# 存根类:supreme_wisdom_coordinator.py 导入了但未使用
@dataclass
class ReflectiveThinkingResult:
    """反省思维结果(存根,supreme_wisdom_coordinator.py 导入了但未使用)"""
    pass

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
