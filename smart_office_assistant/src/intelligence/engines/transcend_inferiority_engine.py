# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_inferiority',
    'assess_coping_style',
    'assess_life_meaning',
    'assess_social_interest',
    'comprehensive_analysis',
    'create_transcend_engine',
    'generate_transcend_plan',
    'get_quote',
    'to_dict',
]

自卑超越引擎 v1.0.0
Transcend Inferiority Engine

基于<自卑与超越>(阿尔弗雷德·阿德勒) 核心思想构建

核心思想:
- 自卑感是所有人共同的心理characteristics
- 每个人都有追求优越的内在动力
- 人生的意义在于对社会的贡献
- 正确运用自卑感可以激发成长

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict

class LifeTask(Enum):
    """人生任务"""
    OCCUPATIONAL = "职业与社会"  # 职业发展,社会角色
    SOCIAL = "社会关系"  # 友谊,亲密关系
    LOVE = "两性关系"  # 爱情,婚姻
    SELF = "自我发展"  # 自我认知,成长

class InferiorityType(Enum):
    """自卑类型"""
    ORGAN = "器官自卑"  # 身体缺陷
    SOCIAL = "社会自卑"  # 社会地位
    EDUCATIONAL = "教育自卑"  # 教育程度
    ECONOMIC = "经济自卑"  # 经济状况
    PSYCHOLOGICAL = "心理自卑"  # 心理创伤
    COMPARATIVE = "比较自卑"  # 与他人比较

class CopingStyle(Enum):
    """应对style"""
    COMPENSATION = "过度补偿"  # 在其他方面过度发展
    OVERCOMPENSATION = "夸张补偿"  # 过度强调优势
    UNDERCOMPENSATION = "不足补偿"  # 逃避,退缩
    TRANSFORMATION = "转化超越"  # 将自卑转化为动力
    FANTASY = "幻想补偿"  # 在幻想中寻求优越

@dataclass
class InferiorityAnalysis:
    """自卑分析"""
    inferiority_type: InferiorityType
    source: str  # 自卑来源
    manifestation: str  # 表现方式
    impact: str  # 影响
    severity: float  # 严重程度 (0-10)
    
    def to_dict(self) -> Dict:
        return {
            "type": self.inferiority_type.value,
            "source": self.source,
            "manifestation": self.manifestation,
            "impact": self.impact,
            "severity": self.severity
        }

@dataclass
class SocialInterestScore:
    """社会兴趣评分"""
    cooperation: float = 0.0  # 合作能力
    empathy: float = 0.0  # 同理心
    contribution: float = 0.0  # 贡献意识
    belonging: float = 0.0  # 归属感
    
    total: float = 0.0
    
    def __post_init__(self):
        self.total = (self.cooperation + self.empathy + 
                     self.contribution + self.belonging) / 4
    
    def to_dict(self) -> Dict:
        return {
            "cooperation": round(self.cooperation, 1),
            "empathy": round(self.empathy, 1),
            "contribution": round(self.contribution, 1),
            "belonging": round(self.belonging, 1),
            "total": round(self.total, 1)
        }

@dataclass
class LifeMeaningAssessment:
    """人生意义评估"""
    occupational_score: float = 0.0  # 职业意义
    social_score: float = 0.0  # 社会意义
    love_score: float = 0.0  # 亲密意义
    self_score: float = 0.0  # 自我意义
    
    overall_score: float = 0.0
    assessment: str = ""
    growth_areas: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "occupational": round(self.occupational_score, 1),
            "social": round(self.social_score, 1),
            "love": round(self.love_score, 1),
            "self": round(self.self_score, 1),
            "overall": round(self.overall_score, 1),
            "assessment": self.assessment,
            "growth_areas": self.growth_areas
        }

class TranscendInferiorityEngine:
    """
    自卑超越引擎
    
    基于阿德勒<自卑与超越>构建,帮助用户recognize自卑模式,
    培养社会兴趣,实现积极超越.
    
    主要功能:
    1. 自卑感recognize与分析
    2. 社会兴趣评估
    3. 人生意义探索
    4. 超越路径指导
    """
    
    # 自卑关键词
    INFERIORITY_KEYWORDS = {
        "不如人": InferiorityType.COMPARATIVE,
        "比不上": InferiorityType.COMPARATIVE,
        "太差": InferiorityType.COMPARATIVE,
        "笨": InferiorityType.PSYCHOLOGICAL,
        "没用": InferiorityType.PSYCHOLOGICAL,
        "不配": InferiorityType.PSYCHOLOGICAL,
        "穷": InferiorityType.ECONOMIC,
        "没文化": InferiorityType.EDUCATIONAL,
        "出身差": InferiorityType.SOCIAL,
        "没关系": InferiorityType.SOCIAL,
        "身体不好": InferiorityType.ORGAN,
        "长得丑": InferiorityType.ORGAN
    }
    
    # 超越关键词
    TRANSCEND_KEYWORDS = {
        "我要努力": CopingStyle.TRANSFORMATION,
        "我要改变": CopingStyle.TRANSFORMATION,
        "我可以": CopingStyle.TRANSFORMATION,
        "证明给": CopingStyle.OVERCOMPENSATION,
        "让他们看看": CopingStyle.OVERCOMPENSATION,
        "我要超过": CopingStyle.OVERCOMPENSATION,
        "算了": CopingStyle.UNDERCOMPENSATION,
        "反正": CopingStyle.UNDERCOMPENSATION,
        "我要是": CopingStyle.FANTASY,
        "要是能": CopingStyle.FANTASY
    }
    
    # 人生意义陈述
    MEANINGFUL_STATEMENTS = [
        "我能为他人做些什么",
        "如何让世界变得更好",
        "我的工作对社会有什么贡献",
        "如何建立有意义的人际关系"
    ]
    
    def __init__(self):
        self.analysis_history: List[InferiorityAnalysis] = []
        self.social_interest_scores: List[SocialInterestScore] = []
    
    def analyze_inferiority(self, text: str) -> List[InferiorityAnalysis]:
        """
        分析文本中的自卑感
        
        Args:
            text: 待分析的文本
            
        Returns:
            List[InferiorityAnalysis]: 自卑感分析列表
        """
        analyses = []
        text_lower = text.lower()
        
        # 检测自卑类型
        for keyword, inf_type in self.INFERIORITY_KEYWORDS.items():
            if keyword in text_lower:
                # judge严重程度
                severity = 5.0
                if "非常" in text or "特别" in text:
                    severity = 8.0
                elif "有点" in text or "稍微" in text:
                    severity = 3.0
                
                analysis = InferiorityAnalysis(
                    inferiority_type=inf_type,
                    source=keyword,
                    manifestation=self._get_manifestation(inf_type, text),
                    impact=self._get_impact(inf_type),
                    severity=severity
                )
                analyses.append(analysis)
                self.analysis_history.append(analysis)
        
        return analyses
    
    def _get_manifestation(self, inf_type: InferiorityType, text: str) -> str:
        """get自卑表现"""
        manifestations = {
            InferiorityType.ORGAN: "身体上的自卑可能导致过度关注外表或回避社交",
            InferiorityType.SOCIAL: "社会自卑可能导致退缩或过度追求认可",
            InferiorityType.EDUCATIONAL: "教育自卑可能导致过度学习或逃避学习",
            InferiorityType.ECONOMIC: "经济自卑可能导致拜金或过度节俭",
            InferiorityType.PSYCHOLOGICAL: "心理自卑可能导致自我否定或防御",
            InferiorityType.COMPARATIVE: "比较自卑可能导致嫉妒或过度竞争"
        }
        return manifestations.get(inf_type, "需要进一步分析")
    
    def _get_impact(self, inf_type: InferiorityType) -> str:
        """get自卑影响"""
        impacts = {
            InferiorityType.ORGAN: "可能影响社交自信和职业选择",
            InferiorityType.SOCIAL: "可能影响人际关系和团队合作",
            InferiorityType.EDUCATIONAL: "可能限制职业发展和社会流动",
            InferiorityType.ECONOMIC: "可能影响生活质量和心理安全感",
            InferiorityType.PSYCHOLOGICAL: "可能影响自我认同和情绪健康",
            InferiorityType.COMPARATIVE: "可能导致焦虑和持续的不满足感"
        }
        return impacts.get(inf_type, "需要进一步分析")
    
    def assess_coping_style(self, text: str) -> Dict:
        """
        评估应对style
        
        Args:
            text: 待评估的文本
            
        Returns:
            Dict: 应对style分析
        """
        text_lower = text.lower()
        
        style_scores = defaultdict(float)
        for keyword, style in self.TRANSCEND_KEYWORDS.items():
            if keyword in text_lower:
                style_scores[style] += 1
        
        if not style_scores:
            dominant_style = CopingStyle.TRANSFORMATION
            confidence = 0.5
        else:
            dominant_style = max(style_scores, key=style_scores.get)
            confidence = min(style_scores[dominant_style] / 3, 1.0)
        
        style_descriptions = {
            CopingStyle.COMPENSATION: {
                "name": "补偿型",
                "description": "在某一方面有自卑时,会在其他方面努力发展",
                "advice": "继续保持,但要注意平衡"
            },
            CopingStyle.OVERCOMPENSATION: {
                "name": "过度补偿型",
                "description": "过度强调自己的优势来掩盖自卑",
                "advice": "尝试接纳自己的不足,适度即可"
            },
            CopingStyle.UNDERCOMPENSATION: {
                "name": "逃避型",
                "description": "面对自卑时选择逃避或放弃",
                "advice": "勇敢面对,小步尝试,逐步建立自信"
            },
            CopingStyle.TRANSFORMATION: {
                "name": "转化超越型",
                "description": "将自卑感转化为成长动力",
                "advice": "这是最健康的应对方式,保持这种态度"
            },
            CopingStyle.FANTASY: {
                "name": "幻想补偿型",
                "description": "在幻想中寻求优越感",
                "advice": "将幻想转化为实际action,从小目标开始"
            }
        }
        
        desc = style_descriptions.get(dominant_style, style_descriptions[CopingStyle.TRANSFORMATION])
        
        return {
            "dominant_style": dominant_style.value,
            "confidence": round(confidence, 2),
            "description": desc["name"] + ": " + desc["description"],
            "advice": desc["advice"]
        }
    
    def assess_social_interest(self, text: str) -> SocialInterestScore:
        """
        评估社会兴趣
        
        阿德勒认为,社会兴趣是个体心理健康的重要metrics.
        高社会兴趣的人更能实现积极的超越.
        
        Args:
            text: 待评估的文本
            
        Returns:
            SocialInterestScore: 社会兴趣评分
        """
        text_lower = text.lower()
        
        # 合作能力
        cooperation_keywords = ["合作", "配合", "团队", "一起", "协作", "分享", "帮助"]
        cooperation = sum(5 for kw in cooperation_keywords if kw in text_lower)
        cooperation = min(cooperation, 100)
        
        # 同理心
        empathy_keywords = ["理解", "体谅", "感受", "关心", "在乎", "换位", "共情"]
        empathy = sum(5 for kw in empathy_keywords if kw in text_lower)
        empathy = min(empathy, 100)
        
        # 贡献意识
        contribution_keywords = ["贡献", "付出", "价值", "意义", "帮助", "服务", "给予"]
        contribution = sum(5 for kw in contribution_keywords if kw in text_lower)
        contribution = min(contribution, 100)
        
        # 归属感
        belonging_keywords = ["归属", "集体", "家庭", "朋友", "归属感", "认同", "融入"]
        belonging = sum(5 for kw in belonging_keywords if kw in text_lower)
        belonging = min(belonging, 100)
        
        score = SocialInterestScore(
            cooperation=cooperation,
            empathy=empathy,
            contribution=contribution,
            belonging=belonging
        )
        
        self.social_interest_scores.append(score)
        return score
    
    def assess_life_meaning(self, occupational: str = "", social: str = "",
                           love: str = "", self_text: str = "") -> LifeMeaningAssessment:
        """
        评估人生意义
        
        Args:
            occupational: 职业相关描述
            social: 社会关系描述
            love: 亲密关系描述
            self_text: 自我发展描述
            
        Returns:
            LifeMeaningAssessment: 人生意义评估
        """
        # 评估各维度
        occ_score = self._score_dimension(occupational, 
            ["贡献", "价值", "意义", "成长", "学习", "帮助"])
        soc_score = self._score_dimension(social,
            ["连接", "关系", "朋友", "归属", "支持", "分享"])
        love_score = self._score_dimension(love,
            ["爱", "关心", "理解", "尊重", "亲密", "承诺"])
        self_score = self._score_dimension(self_text,
            ["成长", "进步", "实现", "价值", "意义", "目标"])
        
        overall = (occ_score + soc_score + love_score + self_score) / 4
        
        # generate评估
        if overall >= 70:
            assessment = "你正在寻找有意义的生活,保持这种追求."
        elif overall >= 40:
            assessment = "你的人生意义感有提升空间,建议更多关注贡献而非get."
        else:
            assessment = "建议重新审视人生目标,寻找能让自己感到有意义的方向."
        
        # recognize成长领域
        scores = {"职业": occ_score, "社会": soc_score, "亲密": love_score, "自我": self_score}
        growth = [k for k, v in scores.items() if v < 50]
        
        return LifeMeaningAssessment(
            occupational_score=occ_score,
            social_score=soc_score,
            love_score=love_score,
            self_score=self_score,
            overall_score=overall,
            assessment=assessment,
            growth_areas=growth
        )
    
    def _score_dimension(self, text: str, keywords: List[str]) -> float:
        """评估某一维度"""
        if not text:
            return 50.0  # 默认分数
        
        text_lower = text.lower()
        score = 50.0
        
        for kw in keywords:
            if kw in text_lower:
                score += 10
        
        return min(score, 100)
    
    def generate_transcend_plan(self, analyses: List[InferiorityAnalysis],
                               coping_style: Dict,
                               social_interest: SocialInterestScore) -> Dict:
        """
        generate超越计划
        
        Args:
            analyses: 自卑分析列表
            coping_style: 应对style
            social_interest: 社会兴趣评分
            
        Returns:
            Dict: 超越计划
        """
        plan = {
            "understanding": [],
            "immediate_actions": [],
            "long_term_goals": [],
            "daily_practices": []
        }
        
        # 理解阶段
        plan["understanding"] = [
            f"自卑感是人类的共同characteristics,适度自卑可以激发成长",
            f"你的应对style是:{coping_style['dominant_style']}",
            f"建议:{coping_style['advice']}"
        ]
        
        # recognize自卑来源
        if analyses:
            sources = [a.source for a in analyses]
            plan["understanding"].append(
                f"你的自卑可能来源于:{', '.join(sources)}"
            )
        
        # 立即action
        plan["immediate_actions"] = [
            "recognize自己的自卑触发点,记录何时何地会产生自卑感",
            "当自卑感出现时,先接受它,不要压抑或逃避",
            "问自己:'这种自卑感背后,我在追求什么?'",
            "将追求优越的目标从'战胜他人'转向'自我超越'"
        ]
        
        # 长期目标
        plan["long_term_goals"] = [
            "培养社会兴趣,多参与合作性活动",
            "建立有意义的人际关系,服务他人",
            "找到能让自己感到有价值的事业或兴趣",
            "发展健康的自我认同,不依赖他人评价"
        ]
        
        # 日常实践
        plan["daily_practices"] = [
            "每天做一件帮助他人的小事",
            "记录自己的进步,无论多小",
            "练习感恩,关注自己拥有的而非缺乏的",
            "与支持性的人交流,避免过度比较"
        ]
        
        return plan
    
    def get_quote(self) -> str:
        """get阿德勒名言"""
        quotes = [
            "人生的意义在于对社会的贡献.",
            "我们不能期待别人了解我们,我们必须自己了解自己.",
            "每个人都有自卑感,因为我们都想让自己变得更好.",
            "决定一个人的不是环境和经历,而是他赋予经历的意义.",
            "真正的幸福来自于对社会的贡献.",
            "合作能力是人类面对生活挑战的最大武器.",
            "不要被过去束缚,要专注于未来的目标.",
            "生活的意义不在于get,而在于贡献."
        ]
        import random
        return random.choice(quotes)
    
    def comprehensive_analysis(self, text: str) -> Dict:
        """
        synthesize分析
        
        Args:
            text: 待分析的文本
            
        Returns:
            Dict: synthesize分析结果
        """
        # 1. 自卑分析
        inferiority_analyses = self.analyze_inferiority(text)
        
        # 2. 应对style
        coping = self.assess_coping_style(text)
        
        # 3. 社会兴趣
        social_interest = self.assess_social_interest(text)
        
        # 4. generate超越计划
        transcend_plan = self.generate_transcend_plan(
            inferiority_analyses, coping, social_interest
        )
        
        return {
            "inferiority_analysis": [a.to_dict() for a in inferiority_analyses],
            "coping_style": coping,
            "social_interest": social_interest.to_dict(),
            "transcend_plan": transcend_plan,
            "adler_quote": self.get_quote()
        }

def create_transcend_engine() -> TranscendInferiorityEngine:
    """工厂函数"""
    return TranscendInferiorityEngine()
