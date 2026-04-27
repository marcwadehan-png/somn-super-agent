"""
__all__ = [
    'analyze_scenario',
    'get_daily_practice',
    'get_practice_guidance',
    'transform_problem',
    'verify_knowledge',
]

王阳明xinxue - 事上磨练引擎
Yangming Wisdom - Practice Through Affairs Engine
=============================================
版本: v1.0.0
创建时间: 2026-04-03
来源: 王阳明<传习录>"人须在事上磨,方立得住"

核心功能:
1. 实践场景分类 - 根据情境类型选择磨练strategy
2. 事上磨心法 - 将事务转化为修行
3. 困境突破 - 在困难中成长的方法论
4. 成就评估 - 衡量磨练成效
5. 知行验证 - 验证知是否真知
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

class 磨砺场景(Enum):
    """磨练场景类型"""
    急难 = "急难"           # 紧急危难情境
    繁忙 = "繁忙"           # 工作繁忙情境
    困境 = "困境"           # 遭遇困境情境
    抉择 = "抉择"           # 重大抉择情境
    诱惑 = "诱惑"           # 面对诱惑情境
    冲突 = "冲突"           # 人际冲突情境
    孤独 = "孤独"           # 独处寂寞情境
    疲劳 = "疲劳"           # 身心疲劳情境

class 事上磨练引擎:
    """
    事上磨练引擎 - 王阳明xinxue实践方法论
    
    核心理念: "人须在事上磨,方立得住"
    - 静处体悟:静坐冥想,澄心静虑
    - 事上磨炼:在具体事务中修炼心性
    - 知行合一:知道与做到unified
    """
    
    def __init__(self):
        self.name = "事上磨练引擎"
        self.version = "8.1.0"
        
        # 场景-心法mapping
        self.场景心法表 = {
            磨砺场景.急难: {
                "原则": "定心定性,临危不乱",
                "方法": ["主一持志", "集义养气", "不动心"],
                "spiritual_insight": "猝然临之而不惊,无故加之而不怒"
            },
            磨砺场景.繁忙: {
                "原则": "忙中修定,杂中求简",
                "方法": ["收放心", "主一功夫", "循序精进"],
                "spiritual_insight": "事物虽多,良知一贯"
            },
            磨砺场景.困境: {
                "原则": "困知勉行,转危为机",
                "方法": ["反求诸己", "变化气质", "扩充良知"],
                "spiritual_insight": "吃得苦中苦,方为人上人;困于心,衡于虑,而后作"
            },
            磨砺场景.抉择: {
                "原则": "致知格物,择善而从",
                "方法": ["深穷其事", "精察天理", "诚意正心"],
                "spiritual_insight": "格物致知,正心诚意;去人欲,存天理"
            },
            磨砺场景.诱惑: {
                "原则": "不动于欲,守志如一",
                "方法": ["志有定向", "操存舍亡", "戒慎恐惧"],
                "spiritual_insight": "从善如登,从恶如崩;一念天堂,一念地狱"
            },
            磨砺场景.冲突: {
                "原则": "和而不争,中而不倚",
                "方法": ["感化以诚", "勿助勿忘", "致其良知"],
                "spiritual_insight": "以直报怨,以德报德;和而不同"
            },
            磨砺场景.孤独: {
                "原则": "慎独存养,独处修心",
                "方法": ["戒慎乎其所不睹", "恐惧乎其所不闻", "主一内省"],
                "spiritual_insight": "君子慎独,不欺暗室"
            },
            磨砺场景.疲劳: {
                "原则": "养心养气,蓄势待发",
                "方法": ["静坐息虑", "调息养气", "简易功夫"],
                "spiritual_insight": "精神愈用则愈出,意志愈磨则愈坚"
            }
        }
        
        # 知行验证标准
        self.知行验证表 = {
            "真知": {
                "标准": "知之真切笃实处即是行",
                "表现": ["明知故犯(不是真知)", "知而能守", "知行合一"],
                "检验": "真知必能行,不能行只是未知"
            },
            "浅知": {
                "标准": "知之明切处不足",
                "表现": ["似懂非懂", "知而不行", "半信半疑"],
                "检验": "需要更多事上磨练"
            },
            "假知": {
                "标准": "道听途说,人云亦云",
                "表现": ["鹦鹉学舌", "表面理解", "缺乏体悟"],
                "检验": "需要在事上验证"
            }
        }
        
        # 磨练阶段
        self.磨练阶段表 = [
            {"阶段": "初磨", "characteristics": "被动应对,手忙脚乱", "目标": "变被动为主动"},
            {"阶段": "渐磨", "characteristics": "渐入佳境,有所感悟", "目标": "深化体悟"},
            {"阶段": "纯磨", "characteristics": "心有所主,从容应对", "目标": "固化能力"},
            {"阶段": "化境", "characteristics": "出神入化,不勉而中", "目标": "知行合一"}
        ]
    
    def analyze_scenario(self, situation: str) -> Dict:
        """
        分析场景类型
        
        Args:
            situation: 情境描述
            
        Returns:
            场景分析结果
        """
        # 关键词匹配
        keywords_map = {
            磨砺场景.急难: ["紧急", "危机", "突发", "危难", "险境", "紧迫"],
            磨砺场景.繁忙: ["忙碌", "繁忙", "事情多", "应接不暇", "事务缠身"],
            磨砺场景.困境: ["困难", "困境", "难题", "逆境", "挫折", "失败"],
            磨砺场景.抉择: ["选择", "抉择", "决定", "decision", "取舍", "两难"],
            磨砺场景.诱惑: ["诱惑", "欲望", "贪念", "松懈", "享乐"],
            磨砺场景.冲突: ["冲突", "矛盾", "争执", "争吵", "对抗", "对立"],
            磨砺场景.孤独: ["孤独", "寂寞", "无聊", "独处", "无人理解"],
            磨砺场景.疲劳: ["疲劳", "疲惫", "疲倦", "劳累", "力竭"]
        }
        
        matched = []
        for scenario, keywords in keywords_map.items():
            for keyword in keywords:
                if keyword in situation:
                    matched.append(scenario)
                    break
        
        if not matched:
            # 默认归为繁忙场景
            matched = [磨砺场景.繁忙]
        
        return {
            "primary_scenario": matched[0],
            "all_scenarios": list(set(matched)),
            "analysis": "多场景交织,需synthesize应对"
        }
    
    def get_practice_guidance(self, scenario: 磨砺场景, level: str = "初磨") -> Dict:
        """
        get磨练指导
        
        Args:
            scenario: 场景类型
            level: 当前磨练阶段
            
        Returns:
            磨练指导方案
        """
        base_guidance = self.场景心法表.get(scenario, self.场景心法表[磨砺场景.繁忙])
        
        # 根据阶段调整指导
        stage_adjustments = {
            "初磨": {"重点": "建立觉知", "方法": base_guidance["方法"][:2], "难度": "低"},
            "渐磨": {"重点": "深化体悟", "方法": base_guidance["方法"], "难度": "中"},
            "纯磨": {"重点": "固化能力", "方法": base_guidance["方法"][::-1], "难度": "高"},
            "化境": {"重点": "出神入化", "方法": ["默而识之", "不勉而中"], "难度": "圆满"}
        }
        
        adjustment = stage_adjustments.get(level, stage_adjustments["初磨"])
        
        return {
            "场景": scenario.value,
            "当前阶段": level,
            "核心原则": base_guidance["原则"],
            "修习重点": adjustment["重点"],
            "修习方法": adjustment["方法"],
            "实践spiritual_insight": base_guidance["spiritual_insight"],
            "难度": adjustment["难度"],
            "经典basis": self._get_classic_reference(scenario)
        }
    
    def _get_classic_reference(self, scenario: 磨砺场景) -> Dict:
        """get经典basis"""
        references = {
            磨砺场景.急难: {
                "原文": "凡人狼狈,大抵皆扰于私意",
                "出处": "<传习录>",
                "解读": "人在危难时容易慌乱,是因为私心作祟,应保持心体光明"
            },
            磨砺场景.繁忙: {
                "原文": "人,要在事上磨,方立得住",
                "出处": "<传习录>",
                "解读": "静坐冥想是基础,但必须在具体事务中修炼才能真正立住"
            },
            磨砺场景.困境: {
                "原文": "艰难困苦,正是磨炼心志之时",
                "出处": "王阳明",
                "解读": "困境是上天给予的磨砺机会,能使人超越自我"
            },
            磨砺场景.抉择: {
                "原文": "知善知恶是良知,为善去恶是格物",
                "出处": "<传习录>",
                "解读": "以良知为标准,在具体事物上为善去恶"
            },
            磨砺场景.诱惑: {
                "原文": "一念不善,此心便是私意",
                "出处": "<传习录>",
                "解读": "要时刻警惕一念之私,及时克去"
            },
            磨砺场景.冲突: {
                "原文": "仇莫深于害善,害善无如毁人",
                "出处": "王阳明",
                "解读": "与人为善,即使冲突也应以诚意感化"
            },
            磨砺场景.孤独: {
                "原文": "戒慎乎其所不睹,恐惧乎其所不闻",
                "出处": "<中庸>",
                "解读": "独处时更要谨慎,因为此时无人监督,最易放失本心"
            },
            磨砺场景.疲劳: {
                "原文": "精神愈用则愈出,意志愈磨则愈坚",
                "出处": "王阳明",
                "解读": "疲劳时更要养护精神,但不能因此懈怠"
            }
        }
        return references.get(scenario, references[磨砺场景.繁忙])
    
    def verify_knowledge(self, knowledge: str, action: str) -> Dict:
        """
        验证知行是否合一
        
        Args:
            knowledge: 所知
            action: 所行
            
        Returns:
            验证结果
        """
        # 简化验证逻辑
        knowledge_keywords = ["知道", "理解", "明白", "懂得", "深知", "体悟"]
        action_keywords = ["做到", "实践", "执行", "action", "落实"]
        
        know_level = sum(1 for k in knowledge_keywords if k in knowledge)
        act_level = sum(1 for a in action_keywords if a in action)
        
        if know_level >= 2 and act_level >= 2:
            verdict = "真知"
            detail = self.知行验证表["真知"]
        elif know_level >= 1 and act_level >= 1:
            verdict = "浅知"
            detail = self.知行验证表["浅知"]
        elif know_level >= 2 and act_level == 0:
            verdict = "假知"
            detail = self.知行验证表["假知"]
        else:
            verdict = "未知"
            detail = {"标准": "知之甚少,需加强学习", "表现": ["认知不足"], "检验": "先明理再力行"}
        
        return {
            "验证结果": verdict,
            "标准": detail["标准"],
            "表现分析": detail["表现"],
            "指导": detail["检验"],
            "建议": self._get_verification_advice(verdict)
        }
    
    def _get_verification_advice(self, verdict: str) -> str:
        """get验证建议"""
        advices = {
            "真知": "继续保持,在更多情境中验证和深化",
            "浅知": "需要更多事上磨练,将认知转化为action",
            "假知": "停止空谈,立即在事上验证",
            "未知": "先静xinxue习,明理后再实践"
        }
        return advices.get(verdict, "持续修炼")
    
    def get_daily_practice(self, focus_area: Optional[str] = None) -> Dict:
        """
        get每日磨练功课
        
        Args:
            focus_area: 重点领域
            
        Returns:
            每日功课安排
        """
        default_practices = [
            {
                "时段": "晨起",
                "功课": "静坐省心",
                "时长": "15-30分钟",
                "要点": "澄心静虑,回想昨夜梦境,检点内心起心动念"
            },
            {
                "时段": "日中",
                "功课": "事上磨练",
                "时长": "持续进行",
                "要点": "专注于当下事务,以良知为标准,为善去恶"
            },
            {
                "时段": "暮时",
                "功课": "省察克治",
                "时长": "15-30分钟",
                "要点": "回顾一日所为,有无私意萌动,有则克之"
            },
            {
                "时段": "睡前",
                "功课": "涵养蓄势",
                "时长": "10-15分钟",
                "要点": "静坐调息,不起杂念,养浩然正气"
            }
        ]
        
        return {
            "修习总纲": "有事时修学,无事时涵养",
            "核心功课": default_practices,
            "注意事项": [
                "循序渐进,不求速成",
                "持之以恒,日日不断",
                "动静结合,文武之道",
                "知行合一,事上验证"
            ],
            "经典背诵": "每日诵读<教条示龙场诸生>或<传习录>数则"
        }
    
    def transform_problem(self, problem: str) -> Dict:
        """
        将问题转化为磨练机会
        
        Args:
            problem: 问题描述
            
        Returns:
            转化方案
        """
        analysis = self.analyze_scenario(problem)
        scenario = analysis["primary_scenario"]
        guidance = self.get_practice_guidance(scenario)
        
        return {
            "问题诊断": problem,
            "场景定位": scenario.value,
            "心法应对": {
                "原则": guidance["核心原则"],
                "方法": guidance["修习方法"],
                "spiritual_insight": guidance["实践spiritual_insight"]
            },
            "转化思路": {
                "第一步": f"以{guidance['核心原则'].split(',')[0]}应对",
                "第二步": "依指导方法切实修行",
                "第三步": "以spiritual_insight提醒自己",
                "第四步": "事后反思,验证知行"
            },
            "预期成效": "将困难转化为成长的阶梯"
        }

# 全局实例
shiyan_engine = 事上磨练引擎()
