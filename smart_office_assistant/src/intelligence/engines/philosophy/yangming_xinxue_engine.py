"""
__all__ = [
    'analyze_decision',
    'analyze_knowledge_action_gap',
    'anti_friction',
    'assess_mind_realm',
    'diagnose_heart_thieves',
    'diagnose_thieves',
    'generate_daily_practice',
    'get_anti_internal_friction_method',
    'get_classic_quote',
    'get_xinxue_decision',
    'get_xinxue_insight',
    'integrate_with_somn',
]

王阳明xinxue深度fusion引擎 - Wang Yangming Xinxue Fusion Engine
v7.0.0 版本

fusion王阳明xinxue核心思想,构建知行合一的智慧decision系统:

[xinxue三大核心]
1. 心即理 - 心外无理,心外无物,一切道理在心中
2. 知行合一 - 知是行的开始,行是知的完成,真知必行
3. 致良知 - 发挥良知的作用,事上磨练,去私欲

[破心中三贼]
1. 坐中静 - 破焦虑之贼,静坐息心
2. 舍中得 - 破欲望之贼,简化生活
3. 事上练 - 破犹豫之贼,立即action

[反内耗心法]
- 认清楚:内耗源于心向外求
- 收回来:把注意力收回到内心
- 动起来:在事上磨练,不空想
- 平常心:保持内心平静

[最高境界]
"此心不动,随机而动" - 内心平静,灵动应对

版本历史:
- v7.0.0 (2026-04-02): 初始版本,fusion王阳明xinxue核心思想
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class XinxueCore(Enum):
    """xinxue三大核心"""
    MIND_IS_REASON = "心即理"           # 心外无理,心外无物
    UNITY_KNOWLEDGE_ACTION = "知行合一"  # 知行一体,真知必行
    EXTEND_INNOCENCE = "致良知"         # 发挥良知,事上磨练

class HeartThief(Enum):
    """心中三贼"""
    ANXIETY = "焦虑之贼"    # 坐中静破之
    DESIRE = "欲望之贼"    # 舍中得破之
    HESITATION = "犹豫之贼" # 事上练破之

class PracticeLevel(Enum):
    """修炼境界层次"""
    COMMON = "常人"        # 未入门
    LEARNING = "学者"      # 知道但做不到
    PRACTICING = "修行者"   # 事上磨练
    ENLIGHTENED = "觉悟者"  # 此心不动
    SAGE = "圣人"          # 随心所欲不逾矩

@dataclass
class XinxueInsight:
    """xinxue智慧洞察"""
    core_teaching: str = ""           # 核心教义
    application_scenario: str = ""     # 应用场景
    mind_state: str = ""              # 心境状态
    action_guidance: str = ""         # action指引
    classic_quote: str = ""           # 经典语录
    integration_with_modern: str = "" # 现代fusion
    practice_method: str = ""         # 修炼方法
    expected_result: str = ""          # 预期效果

@dataclass
class ThiefAnalysis:
    """三贼分析"""
    dominant_thief: HeartThief        # 主要心贼
    severity: float                    # 严重程度 0-1
    manifestation: List[str] = field(default_factory=list)  # 具体表现
    solution: str = ""                 # 解决方法
    practice_steps: List[str] = field(default_factory=list)  # 实践步骤
    quote: str = ""                    # 阳明语录

@dataclass
class WisdomActionAnalysis:
    """知行合一分析"""
    knowledge_level: str = ""          # 知的层次
    action_gap: str = ""               # 知行差距
    integration_path: str = ""          # fusion路径
    immediate_action: str = ""          # 立即action
    reflection_questions: List[str] = field(default_factory=list)  # 反思问题
    progress_indicator: str = ""       # 进步metrics

@dataclass
class XinxueAnalysisResult:
    """xinxuesynthesize分析结果"""
    primary_core: XinxueCore = None           # 主要核心教义
    secondary_cores: List[XinxueCore] = field(default_factory=list)  # 次要核心
    current_state: PracticeLevel = None        # 当前境界
    thief_analysis: Optional[ThiefAnalysis] = None  # 三贼分析
    wisdom_action: Optional[WisdomActionAnalysis] = None  # 知行分析
    mind_realm: str = ""                # 心境境界描述
    recommended_practice: str = ""       # 推荐修炼
    action_plan: List[str] = field(default_factory=list)  # action方案
    daily_routine: Dict[str, str] = field(default_factory=dict)  # 日常修行
    ancient_wisdom_modern: str = ""     # 古智今用
    transformation_potential: float = 0.0  # 转变潜力 0-1

class YangmingXinxueEngine:
    """
    王阳明xinxue深度fusion引擎
    
    功能:
    1. 心即理decision - 内在judge,心外无理
    2. 知行合一分析 - 真知必行,行即是知
    3. 致良知指导 - 发挥良知,事上磨练
    4. 破三贼诊断 - 焦虑,欲望,犹豫
    5. 反内耗心法 - 内心平静,减少消耗
    6. 此心不动 - 最高境界修炼
    
    应用场景:
    - 重大decision时的良知judge
    - 知行不合一时的问题诊断
    - 内耗严重时的反内耗指导
    - 焦虑,犹豫时的破贼方法
    """
    
    # 王阳明核心语录库
    CLASSIC_QUOTES = {
        "心即理": [
            "圣人之道,吾性自足,不假外求.",
            "心外无理,心外无物.",
            "心之本体,无所不该.",
            "天地虽大,但心存良知,则万物皆备于我."
        ],
        "知行合一": [
            "知之真切笃实处即是行,行之明觉精察处即是知.",
            "知是行的开始,行是知的完成.",
            "知而不行,只是未知.",
            "未有知而不行者,知而不行,只是未知."
        ],
        "致良知": [
            "致吾心之良知于事事物物,则事事物物皆得其理.",
            "良知是,人人本有,不待学而后能.",
            "良知之外,更无知;致知之外,更无学.",
            "人胸中各有个圣人,只因自信不及,都自埋倒了."
        ],
        "破三贼": [
            "静坐是息心养心的功夫.",
            "知足者富.",
            "人须在事上磨,方立得住."
        ],
        "此心不动": [
            "此心不动,随机而动.",
            "越是艰难处,越是修心时.",
            "破山中贼易,破心中贼难."
        ]
    }
    
    # xinxue与现代decision的mapping
    DECISION_MAPPING = {
        "内心冲突": {
            "xinxue视角": "私欲遮蔽良知",
            "解决方法": "静心观照,致良知",
            "阳明语": "人欲胜,则天理灭"
        },
        "犹豫不决": {
            "xinxue视角": "心中贼作祟",
            "解决方法": "事上练,立即action",
            "阳明语": "人须在事上磨"
        },
        "焦虑不安": {
            "xinxue视角": "心向外求",
            "解决方法": "坐中静,收回内心",
            "阳明语": "静坐是息心养心的功夫"
        },
        "action无力": {
            "xinxue视角": "知而不行",
            "解决方法": "知行合一,真知必行",
            "阳明语": "知是行的开始"
        },
        "自我怀疑": {
            "xinxue视角": "不信良知",
            "解决方法": "致良知,信己心",
            "阳明语": "人胸中各有个圣人"
        }
    }
    
    # 日常修炼指南
    DAILY_PRACTICE = {
        "早晨": {
            "activity": "静坐冥想",
            "duration": "15-30分钟",
            "method": "盘腿而坐,脊背挺直,闭目专注呼吸",
            "goal": "息心静气,准备一天"
        },
        "日中": {
            "activity": "事上磨练",
            "duration": "随时",
            "method": "将每件事当作修炼的机会",
            "goal": "在action中致良知"
        },
        "傍晚": {
            "activity": "反思日记",
            "duration": "10-15分钟",
            "method": "记录今天的知行是否合一",
            "goal": "发现问题,持续改进"
        },
        "夜间": {
            "activity": "读传习录",
            "duration": "15-30分钟",
            "method": "学习阳明语录,深化理解",
            "goal": "理论学习,指导实践"
        }
    }
    
    def __init__(self):
        """initxinxue引擎"""
        self.name = "王阳明xinxuefusion引擎"
        self.version = "v7.0.0"
        logger.info(f"{self.name} {self.version} init完成")
    
    def analyze_decision(self, 
                        situation: str,
                        options: List[str],
                        concerns: List[str]) -> Dict[str, Any]:
        """
        心即理decision分析
        
        Args:
            situation: decision情境描述
            options: 可选方案列表
            concerns: 顾虑因素列表
        
        Returns:
            xinxue视角的decision分析
        """
        analysis = {
            "method": "心即理decision法",
            "situation": situation,
            "options_analysis": [],
            "recommended_option": "",
            "reasoning": "",
            "innocence_test": [],  # 良知检验问题
            "action": ""
        }
        
        # 提取关键词
        situation_keywords = situation.lower()
        
        # 应用xinxuemapping
        for concern_type, mapping in self.DECISION_MAPPING.items():
            if any(keyword in situation_keywords for keyword in [concern_type]):
                analysis["reasoning"] += f"\n[xinxue诊断]{mapping['xinxue视角']}\n"
                analysis["reasoning"] += f"[解决方法]{mapping['解决方法']}\n"
                analysis["reasoning"] += f"[阳明遗训]{mapping['阳明语']}\n"
        
        # 良知检验
        analysis["innocence_test"] = [
            "这个选择是否让我心安?",
            "如果是圣人,会如何选择?",
            "十年后回看,这个选择对吗?",
            "这个选择是否只为自己,还是利益他人?"
        ]
        
        # 推荐action
        analysis["action"] = "静下心来,让良知做judge.不要被私欲遮蔽,相信内心的声音."
        
        return analysis
    
    def analyze_knowledge_action_gap(self,
                                     knowledge: str,
                                     behavior: str) -> WisdomActionAnalysis:
        """
        知行差距分析
        
        Args:
            knowledge: 知道的道理
            behavior: 实际行为
        
        Returns:
            知行合一分析
        """
        gap_analysis = WisdomActionAnalysis(
            knowledge_level="已理解",
            action_gap="存在知行差距",
            integration_path="",
            immediate_action="",
            reflection_questions=[],
            progress_indicator=""
        )
        
        # 分析差距根源
        gap_analysis.integration_path = """
        [知行合一修炼路径]
        1. 认清楚:知道和做到之间有"私欲"阻隔
        2. 收回来:把注意力从外在收回内心
        3. 动起来:不要等到完全知道才action
        4. 平常心:接受过程中的不完美
        """
        
        gap_analysis.immediate_action = "立即去做一件小事,不要等到准备好."
        
        gap_analysis.reflection_questions = [
            "我为什么知道却做不到?",
            "是什么在阻碍我action?",
            "如果这是知行合一的境界,我会怎么做?",
            "今天的action是否对得起我知道的道理?"
        ]
        
        gap_analysis.progress_indicator = """
        [知行合一进步metrics]
        - 从"知道但做不到"到"边做边知道"
        - 从"追求完美才开始"到"在action中完善"
        - 从"知而不行"到"知行合一"
        """
        
        return gap_analysis
    
    def diagnose_heart_thieves(self,
                               symptoms: List[str]) -> ThiefAnalysis:
        """
        心中三贼诊断
        
        Args:
            symptoms: 症状列表
        
        Returns:
            三贼分析结果
        """
        symptom_str = " ".join(symptoms).lower()
        
        # judge主要心贼
        if any(word in symptom_str for word in ["焦虑", "不安", "担忧", "恐惧", "未来"]):
            dominant = HeartThief.ANXIETY
        elif any(word in symptom_str for word in ["欲望", "想要", "贪", "多", "不够"]):
            dominant = HeartThief.DESIRE
        else:
            dominant = HeartThief.HESITATION
        
        # 构建分析
        analysis = ThiefAnalysis(
            dominant_thief=dominant,
            severity=0.7,
            manifestation=symptoms,
            solution="",
            practice_steps=[],
            quote=""
        )
        
        if dominant == HeartThief.ANXIETY:
            analysis.solution = "坐中静 - 静坐冥想,收回内心"
            analysis.practice_steps = [
                "找一个安静的地方",
                "盘腿而坐,脊背挺直",
                "闭目,将注意力放在呼吸上",
                "杂念来了,不追随,只是观察",
                "每天坚持15-30分钟"
            ]
            analysis.quote = "静坐是息心养心的功夫."
            
        elif dominant == HeartThief.DESIRE:
            analysis.solution = "舍中得 - 简化生活,减少欲望"
            analysis.practice_steps = [
                "列出真正需要的东西",
                "减少不必要的追求",
                "珍惜已有的事物",
                "学会分享和给予",
                "知足常乐"
            ]
            analysis.quote = "知足者富."
            
        else:  # HESITATION
            analysis.solution = "事上练 - 立即action,不要等待"
            analysis.practice_steps = [
                "设定小目标,立即action",
                "把大任务分解为小步骤",
                "每完成一步就给自己肯定",
                "不要追求完美,先完成再完善",
                "复盘总结,持续改进"
            ]
            analysis.quote = "人须在事上磨,方立得住."
        
        return analysis
    
    def get_anti_internal_friction_method(self,
                                          problem_description: str) -> Dict[str, Any]:
        """
        反内耗心法
        
        Args:
            problem_description: 问题描述
        
        Returns:
            反内耗指导方案
        """
        method = {
            "problem": problem_description,
            "root_cause": "内耗源于心向外求",
            "core_approach": "四步反内耗心法",
            "steps": [
                {
                    "step": 1,
                    "name": "认清楚",
                    "description": "内耗是内心两个声音的对抗",
                    "action": "观察内心的两个声音,问自己:哪个是真相,哪个是妄想?"
                },
                {
                    "step": 2,
                    "name": "收回来",
                    "description": "把注意力从外在收回内心",
                    "action": "停止追逐外在评价,专注于内心真正想要的"
                },
                {
                    "step": 3,
                    "name": "动起来",
                    "description": "在事上磨练,不空想",
                    "action": "不要等到准备好,立即action一件小事"
                },
                {
                    "step": 4,
                    "name": "平常心",
                    "description": "保持一颗平常心",
                    "action": "接受不完美,接受过程中的挫折"
                }
            ],
            "zen_state": "此心不动,随机而动",
            "practice_reminder": "反内耗不是消除所有想法,而是让心安住"
        }
        
        return method
    
    def assess_mind_realm(self,
                          mental_state: str,
                          recent_behaviors: List[str]) -> Tuple[PracticeLevel, str]:
        """
        心境境界评估
        
        Args:
            mental_state: 心理状态描述
            recent_behaviors: 最近行为列表
        
        Returns:
            (境界层次, 境界描述)
        """
        state_lower = mental_state.lower()
        behaviors_str = " ".join(recent_behaviors).lower()
        
        # 评估标准
        enlightened_indicators = ["平静", "安定", "专注", "内在", "良知"]
        practicing_indicators = ["action", "开始", "尝试", "面对", "磨练"]
        struggling_indicators = ["焦虑", "犹豫", "纠结", "内耗", "拖延"]
        
        enlightened_count = sum(1 for i in enlightened_indicators 
                                  if i in state_lower or i in behaviors_str)
        practicing_count = sum(1 for i in practicing_indicators 
                                if i in state_lower or i in behaviors_str)
        struggling_count = sum(1 for i in struggling_indicators 
                               if i in state_lower or i in behaviors_str)
        
        if enlightened_count >= 3:
            level = PracticeLevel.ENLIGHTENED
            description = """
            [觉悟者境界]
            你已能够保持内心的平静与安定,在纷繁的事务中不为外物所动.
            阳明先生说:"此心不动,随机而动."
            
            继续修炼方向:
            - 在更大的事上磨练
            - 帮助他人破心中贼
            - 追求更高层次的"此心不动"
            """
        elif enlightened_count >= 1 and practicing_count >= 2:
            level = PracticeLevel.PRACTICING
            description = """
            [修行者境界]
            你已开始将xinxue思想付诸实践,在事上磨练,不断进步.
            阳明先生说:"人须在事上磨,方立得住."
            
            继续修炼方向:
            - 加大action力度
            - 深化对良知的认知
            - 减少知行差距
            """
        elif practicing_count >= 2:
            level = PracticeLevel.LEARNING
            description = """
            [学者境界]
            你已学习xinxue思想,但知行之间还有差距.
            阳明先生说:"知而不行,只是未知."
            
            继续修炼方向:
            - 不要等准备好再action
            - 先做一件小事
            - 在action中深化认知
            """
        else:
            level = PracticeLevel.COMMON
            description = """
            [常人境界]
            心被三贼(焦虑,欲望,犹豫)所困扰,需要从基础开始修炼.
            
            建议从以下开始:
            - 每日静坐15分钟
            - recognize自己被哪种心贼困扰
            - 用相应的方法破贼
            """
        
        return level, description
    
    def get_classic_quote(self, theme: str) -> str:
        """
        get经典语录
        
        Args:
            theme: 主题关键词
        
        Returns:
            经典语录
        """
        quotes = self.CLASSIC_QUOTES.get(theme, [])
        if quotes:
            return quotes[0]
        
        # 模糊匹配
        for key, quote_list in self.CLASSIC_QUOTES.items():
            if key in theme or theme in key:
                return quote_list[0]
        
        return "圣人之道,吾性自足,不假外求."
    
    def generate_daily_practice(self, focus_area: str = None) -> Dict[str, Any]:
        """
        generate日常修炼计划
        
        Args:
            focus_area: 重点领域(可选)
        
        Returns:
            日常修炼方案
        """
        practice = {
            "title": "xinxue日常修炼指南",
            "duration": "21天养成习惯",
            "daily_routine": self.DAILY_PRACTICE.copy(),
            "weekly_focus": {}
        }
        
        # 根据重点领域调整
        if focus_area == "焦虑":
            practice["weekly_focus"] = {
                "week1": "坐中静 - 每天静坐30分钟",
                "week2": "观照内心 - recognize焦虑的根源",
                "week3": "放下执着 - 接受不确定性"
            }
        elif focus_area == "action力":
            practice["weekly_focus"] = {
                "week1": "事上练 - 每天做一件拖延的事",
                "week2": "分解任务 - 大事化小",
                "week3": "持续迭代 - 完成比完美重要"
            }
        elif focus_area == "decision":
            practice["weekly_focus"] = {
                "week1": "静心 - 做决定前先静坐",
                "week2": "良知检验 - 问自己四个问题",
                "week3": "立即action - 不要犹豫"
            }
        else:
            practice["weekly_focus"] = {
                "week1": "静坐 - 培养平静的心",
                "week2": "action - 知行合一",
                "week3": "反思 - 持续改进"
            }
        
        return practice
    
    def integrate_with_somn(self,
                            user_query: str,
                            context: Dict[str, Any]) -> XinxueAnalysisResult:
        """
        与Somn系统fusion的核心接口
        
        Args:
            user_query: 用户查询
            context: 上下文信息
        
        Returns:
            xinxuesynthesize分析结果
        """
        query_lower = user_query.lower()
        
        # 确定主要核心
        if any(word in query_lower for word in ["decision", "选择", "judge", "决定"]):
            primary = XinxueCore.MIND_IS_REASON
        elif any(word in query_lower for word in ["知道", "做到", "action", "实践"]):
            primary = XinxueCore.UNITY_KNOWLEDGE_ACTION
        elif any(word in query_lower for word in ["良知", "良心", "对错", "道德"]):
            primary = XinxueCore.EXTEND_INNOCENCE
        else:
            primary = XinxueCore.EXTEND_INNOCENCE
        
        # 确定次要核心
        secondary = []
        if primary != XinxueCore.MIND_IS_REASON:
            secondary.append(XinxueCore.MIND_IS_REASON)
        if primary != XinxueCore.UNITY_KNOWLEDGE_ACTION:
            secondary.append(XinxueCore.UNITY_KNOWLEDGE_ACTION)
        
        # get经典语录
        classic_quote = self.get_classic_quote(primary.value)
        
        # 构建结果
        result = XinxueAnalysisResult(
            primary_core=primary,
            secondary_cores=secondary,
            current_state=PracticeLevel.LEARNING,
            thief_analysis=None,
            wisdom_action=None,
            mind_realm="学习者",
            recommended_practice="每日静坐,事上磨练",
            action_plan=["静坐15分钟", "反思今日知行", "记录心得"],
            daily_routine=self.DAILY_PRACTICE.copy(),
            ancient_wisdom_modern="将王阳明xinxue思想应用于现代生活与工作",
            transformation_potential=0.7
        )
        
        # 添加相关分析
        if any(word in query_lower for word in ["焦虑", "不安", "内耗"]):
            result.thief_analysis = self.diagnose_heart_thieves([user_query])
            result.mind_realm = "被焦虑之贼困扰"
            result.recommended_practice = "坐中静 - 每日静坐"
            
        if any(word in query_lower for word in ["action", "执行", "拖延"]):
            result.wisdom_action = self.analyze_knowledge_action_gap(
                "我知道应该action", "但实际拖延"
            )
            result.mind_realm = "知行不合一"
            result.recommended_practice = "事上练 - 立即action"
        
        return result
    
    def get_xinxue_insight(self, topic: str) -> XinxueInsight:
        """
        getxinxue洞察
        
        Args:
            topic: 主题
        
        Returns:
            xinxue智慧洞察
        """
        insights = {
            "心即理": XinxueInsight(
                core_teaching="心外无理,心外无物,一切道理都在心中",
                application_scenario="遇到困惑时,向内心求答案,不要外求",
                mind_state="安定,清明,不外逐",
                action_guidance="静心观照,让良知做judge",
                classic_quote="圣人之道,吾性自足,不假外求.",
                integration_with_modern="相信自己的judge,不被权威束缚",
                practice_method="每日静坐,观照内心",
                expected_result="内心安定,不被外物所扰"
            ),
            "知行合一": XinxueInsight(
                core_teaching="知是行的开始,行是知的完成,真知必行",
                application_scenario="知道却做不到时,问题不在于知,而在于行",
                mind_state="action,专注,实践",
                action_guidance="不要等到完全知道才action,在action中深化认知",
                classic_quote="知之真切笃实处即是行,行之明觉精察处即是知.",
                integration_with_modern="边做边学,快速迭代",
                practice_method="设定小目标,立即action",
                expected_result="知行合一,做事效率提升"
            ),
            "致良知": XinxueInsight(
                core_teaching="良知人人本有,只需发挥良知的作用",
                application_scenario="面对是非对错的judge时,相信良知",
                mind_state="清明,善良,正义",
                action_guidance="去除私欲,让良知做主",
                classic_quote="致吾心之良知于事事物物,则事事物物皆得其理.",
                integration_with_modern="做正确的事,即使困难",
                practice_method="每日反思,问自己是否对得起良知",
                expected_result="内心无愧,坦荡自在"
            )
        }
        
        return insights.get(topic, insights["知行合一"])

# 便捷函数
def get_xinxue_decision(situation: str, options: List[str]) -> Dict[str, Any]:
    """快速心即理decision"""
    engine = YangmingXinxueEngine()
    return engine.analyze_decision(situation, options, [])

def diagnose_thieves(symptoms: List[str]) -> Dict[str, Any]:
    """快速三贼诊断"""
    engine = YangmingXinxueEngine()
    result = engine.diagnose_heart_thieves(symptoms)
    return {
        "主要心贼": result.dominant_thief.value,
        "严重程度": f"{result.severity * 100:.0f}%",
        "解决方法": result.solution,
        "实践步骤": result.practice_steps,
        "阳明语录": result.quote
    }

def anti_friction(problem: str) -> Dict[str, Any]:
    """快速反内耗"""
    engine = YangmingXinxueEngine()
    return engine.get_anti_internal_friction_method(problem)

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

# 向后兼容别名
XinxueLifeStage = PracticeLevel
王阳明心学引擎 = YangmingXinxueEngine
