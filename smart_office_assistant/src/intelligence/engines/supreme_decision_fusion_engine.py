# -*- coding: utf-8 -*-
"""
超级decisionfusion引擎 v5.5.0
Supreme Decision Fusion Engine

整合儒家十经,素书五德,儒释道三家,兵法,吕氏春秋,科幻思维,成长思维
打造全维度decision支持系统

版本: v5.5.0
日期: 2026-04-02
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import random

class DecisionDimension(Enum):
    """decision维度"""
    # 儒家维度
    REN = "仁"                    # 仁爱之心
    YI = "义"                     # 适宜之宜
    LI = "礼"                     # 秩序之礼
    ZHI = "智"                    # 明智之智
    XIN = "信"                    # 诚信之本
    
    # 素书五德
    DAO = "道"                    # 规律之道
    DE = "德"                     # 品行之德
    REN_SUFU = "仁"               # 仁爱之仁
    YI_SUFU = "义"                # 适宜之义
    LI_SUFU = "礼(素书)"            # 规范之礼
    
    # 佛家维度
    KONG = "空"                   # 缘起性空
    MING = "明"                   # 心明澄澈
    JIE = "戒"                    # 戒律清净
    DING = "定"                    # 禅定专注
    HUI = "慧"                    # 般若智慧
    
    # 道家维度
    ZIRAN = "自然"                # 道法自然
    WUWEI = "无为"                # 无为而治
    GENTLE = "柔弱"                # 柔弱胜刚强
    RETURN = "复归"                # 复归其根
    
    # 兵法维度
    ZHENG = "正"                  # 正面
    QI = "奇"                     # 出奇制胜
    SHI = "势"                    # 势如破竹
    LI_MILITARY = "力"                     # 力量对比
    
    # 吕氏春秋维度
    GONG = "公"                   # 贵公去私
    SHI_LV = "时"                 # 顺应时令
    YINYANG = "阴阳"              # 阴阳平衡
    XIAN = "先"                   # 先发制人
    
    # 科幻维度
    DIMENSION = "维度"            # 降维/升维
    FOREST = "森林"               # 黑暗森林
    SILENCE = "沉默"              # 宇宙沉默
    SCALE = "尺度"                # 尺度思维
    
    # 成长维度
    GROWTH = "成长"                # 成长型思维
    REVERSE = "逆向"               # 逆向思考
    LOOP = "闭环"                  # 闭环迭代
    TRANSCEND = "超越"             # 自卑超越

class ProblemCategory(Enum):
    """问题类别"""
    # 企业经营
    STRATEGY = "战略规划"
    TALENT = "人才管理"
    MARKET = "市场营销"
    CRISIS = "危机应对"
    INNOVATION = "创新变革"
    GOVERNANCE = "治理decision"
    
    # 人生decision
    CAREER = "职业发展"
    RELATIONSHIP = "人际关系"
    GROWTH = "个人成长"
    WISDOM = "智慧领悟"
    
    # 文化传承
    CULTURE = "文化建设"
    EDUCATION = "教育培养"
    ETHICS = "伦理抉择"

@dataclass
class WisdomPerspective:
    """智慧视角"""
    dimension: DecisionDimension
    score: float                    # 适配度 0-1
    principle: str                  # 核心原则
    guidance: str                  # 指导建议
    quotes: List[str]               # 相关语录
    warnings: List[str]             # 警示提醒

@dataclass
class DecisionResult:
    """decision结果"""
    timestamp: datetime
    problem: str
    category: ProblemCategory
    
    # 维度评分
    dimension_scores: Dict[DecisionDimension, float]
    
    # 各学派视角
    perspectives: List[WisdomPerspective]
    
    # synthesize_decision
    primary_dimension: DecisionDimension
    secondary_dimensions: List[DecisionDimension]
    
    final_recommendation: str
    reasoning_chain: List[str]
    action_plan: List[str]
    risk_warnings: List[str]
    quotes_for_meditation: List[str]
    
    # synthesize评估
    overall_score: float
    ethics_score: float
    wisdom_score: float
    feasibility_score: float

class SupremeDecisionFusionEngine:
    """
    超级decisionfusion引擎
    
    整合八大智慧体系的decision支持系统:
    1. 儒家十经 - 仁义礼智信
    2. 素书五德 - 道德仁义礼
    3. 儒释道三家 - 治世/治身/治心
    4. 兵法三十六计 - 战略战术
    5. 吕氏春秋 - 贵公时令
    6. 科幻思维 - 降维打击
    7. 成长思维 - 持续迭代
    8. 神经科学 - 认知增强
    """
    
    def __init__(self):
        self.dimension_weights = self._initialize_weights()
        self.quotes_database = self._load_quotes_database()
        self.principles_database = self._load_principles_database()
    
    def _initialize_weights(self) -> Dict[DecisionDimension, float]:
        """init维度权重"""
        return {
            # 儒家五常
            DecisionDimension.REN: 0.9,
            DecisionDimension.YI: 0.9,
            DecisionDimension.LI: 0.8,
            DecisionDimension.ZHI: 0.9,
            DecisionDimension.XIN: 0.85,
            
            # 素书五德
            DecisionDimension.DAO: 0.85,
            DecisionDimension.DE: 0.85,
            DecisionDimension.REN_SUFU: 0.8,
            DecisionDimension.YI_SUFU: 0.8,
            DecisionDimension.LI_SUFU: 0.75,
            
            # 佛家
            DecisionDimension.KONG: 0.6,
            DecisionDimension.MING: 0.75,
            DecisionDimension.JIE: 0.6,
            DecisionDimension.DING: 0.7,
            DecisionDimension.HUI: 0.8,
            
            # 道家
            DecisionDimension.ZIRAN: 0.75,
            DecisionDimension.WUWEI: 0.65,
            DecisionDimension.GENTLE: 0.7,
            DecisionDimension.RETURN: 0.6,
            
            # 兵法
            DecisionDimension.ZHENG: 0.75,
            DecisionDimension.QI: 0.8,
            DecisionDimension.SHI: 0.85,
            DecisionDimension.LI: 0.7,
            
            # 吕氏春秋
            DecisionDimension.GONG: 0.75,
            DecisionDimension.SHI_LV: 0.7,
            DecisionDimension.YINYANG: 0.8,
            DecisionDimension.XIAN: 0.65,
            
            # 科幻
            DecisionDimension.DIMENSION: 0.7,
            DecisionDimension.FOREST: 0.6,
            DecisionDimension.SILENCE: 0.5,
            DecisionDimension.SCALE: 0.7,
            
            # 成长
            DecisionDimension.GROWTH: 0.85,
            DecisionDimension.REVERSE: 0.8,
            DecisionDimension.LOOP: 0.85,
            DecisionDimension.TRANSCEND: 0.8,
        }
    
    def _load_quotes_database(self) -> Dict[str, List[str]]:
        """加载语录数据库"""
        return {
            # 儒家十经
            "论语": [
                "仁者爱人,己所不欲勿施于人",
                "君子喻于义,小人喻于利",
                "礼之用,和为贵",
                "知之为知之,不知为不知",
                "人无信不立",
                "学而时习之,不亦说乎",
                "三人行必有我师",
                "君子求诸己,小人求诸人",
                "己欲立而立人,己欲达而达人",
                "克己复礼为仁"
            ],
            "孟子": [
                "性善论:人性本善",
                "民为贵,社稷次之,君为轻",
                "舍生取义",
                "天将降大任于斯人",
                "生于忧患,死于安乐",
                "尽心知命",
                "养心莫善于寡欲",
                "恻隐之心,人皆有之",
                "老吾老以及人之老",
                "君子不怨天不尤人"
            ],
            "大学": [
                "大学之道,在明明德",
                "苟日新,日日新,又日新",
                "格物致知",
                "诚意正心",
                "修身齐家治国平天下",
                "知止而后有定",
                "自天子以至于庶人",
                "壹是皆以修身为本"
            ],
            "中庸": [
                "不偏之谓中,不易之谓庸",
                "天命之谓性,率性之谓道",
                "致中和,天地位焉",
                "诚者,天之道也",
                "诚之者,人之道也",
                "极高明而道中庸",
                "执其两端,用其中于民",
                "上不怨天,下不尤人"
            ],
            "尚书": [
                "德惟善政,政在养民",
                "任贤勿贰",
                "人心惟危,道心惟微",
                "惟精惟一,允执厥中",
                "敬天保民",
                "明德慎罚",
                "罪疑惟轻",
                "功亏一篑"
            ],
            "诗经": [
                "关关雎鸠,在河之洲",
                "桃之夭夭,灼灼其华",
                "执子之手,与子偕老",
                "高山仰止,景行行止",
                "他山之石,可以攻玉",
                "靡不有初,鲜克有终",
                "投我以桃,报之以李",
                "风雨如晦,鸡鸣不已"
            ],
            "易经": [
                "天行健,君子以自强不息",
                "地势坤,君子以厚德载物",
                "穷则变,变则通",
                "物极必反",
                "君子以恐惧修身",
                "积善之家,必有余庆",
                "亢龙有悔",
                "谦受益,满招损",
                "三人行则损一人",
                "立天之道曰阴与阳"
            ],
            "孝经": [
                "夫孝,德之本也",
                "身体发肤,受之父母",
                "孝悌之至,通于神明",
                "爱亲者,不敢恶于人",
                "以孝事君则忠",
                "父母在,不远游",
                "立身行道,扬名于后世",
                "罪莫大于不孝"
            ],
            "素书": [
                "道者,人之所蹈",
                "德者,人之所失",
                "仁者,人之所亲",
                "义者,人之所宜",
                "礼者,人之所履",
                "俊者,人之所羡",
                "豪者,人之所畏",
                "贤者,人之所称",
                "危于利也,害于义也",
                "吉莫吉于知足"
            ],
            "道德经": [
                "道可道,非常道",
                "上善若水",
                "无为而无不为",
                "柔弱胜刚强",
                "知人者智,自知者明",
                "为而不争",
                "致虚极,守静笃",
                "知足者富",
                "飘风不终朝",
                "物壮则老"
            ],
            "孙子兵法": [
                "知己知彼,百战不殆",
                "不战而屈人之兵",
                "上兵伐谋",
                "兵者,诡道也",
                "致人而不致于人",
                "善战者,致人而不致于人",
                "乱生于治,怯生于勇",
                "知彼知己,胜乃不殆",
                "善用兵者,携手若使一人",
                "兵贵胜,不贵久"
            ],
            "三体": [
                "黑暗森林法则",
                "降维打击",
                "维度碾压",
                "文明的第一需求是生存",
                "失去人性,失去很多",
                "失去兽性,失去一切",
                "给岁月以文明",
                "消灭人类暴政",
                "宇宙很大,生活更大",
                "弱小和无知不是生存的障碍"
            ],
            "成长思维": [
                "能力可以培养",
                "失败是成长的机会",
                "挑战是学习的契机",
                "努力是通往成功的道路",
                "批评是改进的信息",
                "他人的成功是灵感",
                "大脑可塑性",
                "从错误中学习",
                "坚持不懈",
                "拥抱未知"
            ]
        }
    
    def _load_principles_database(self) -> Dict[str, Dict]:
        """加载原则数据库"""
        return {
            "儒家": {
                "核心": "仁义礼智信",
                "方法": "修身齐家治国平天下",
                "境界": "内圣外王",
                "原则": ["己所不欲勿施于人", "君子喻于义", "礼之用和为贵"]
            },
            "道家": {
                "核心": "道法自然",
                "方法": "无为而治",
                "境界": "返璞归真",
                "原则": ["柔弱胜刚强", "知足者富", "上善若水"]
            },
            "佛家": {
                "核心": "缘起性空",
                "方法": "戒定慧",
                "境界": "涅槃寂静",
                "原则": ["诸行无常", "诸法无我", "涅槃寂静"]
            },
            "素书": {
                "核心": "道德仁义礼",
                "方法": "五德decision",
                "境界": "遵义章46种警示",
                "原则": ["贤人君子", "明耻教战", "吉莫吉于知足"]
            },
            "兵法": {
                "核心": "知己知彼",
                "方法": "奇正相生",
                "境界": "不战而屈人",
                "原则": ["先为不可胜", "致人而不致于人", "兵贵胜不贵久"]
            },
            "吕氏春秋": {
                "核心": "贵公去私",
                "方法": "顺应时令",
                "境界": "天下为公",
                "原则": ["公则天下平", "阴阳调和", "因时制宜"]
            },
            "科幻": {
                "核心": "维度超越",
                "方法": "降维打击",
                "境界": "宇宙尺度",
                "原则": ["生存第一", "黑暗森林", "沉默是金"]
            },
            "成长": {
                "核心": "持续迭代",
                "方法": "闭环反馈",
                "境界": "超越自我",
                "原则": ["能力可塑", "拥抱挑战", "从失败学习"]
            }
        }
    
    def analyze_problem(self, problem: str, context: Optional[Dict] = None) -> DecisionResult:
        """
        分析问题并给出decision建议
        
        Args:
            problem: 问题描述
            context: 上下文信息
            
        Returns:
            DecisionResult: decision结果
        """
        # 1. 确定问题类别
        category = self._classify_problem(problem)
        
        # 2. 计算各维度适配度
        dimension_scores = self._calculate_dimension_scores(problem, category)
        
        # 3. generate各学派视角
        perspectives = self._generate_perspectives(problem, category, dimension_scores)
        
        # 4. 确定主要和次要维度
        sorted_dims = sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True)
        primary_dimension = sorted_dims[0][0]
        secondary_dimensions = [d[0] for d in sorted_dims[1:4]]
        
        # 5. generatesynthesize_decision
        final_recommendation = self._generate_recommendation(
            problem, category, primary_dimension, perspectives
        )
        
        # 6. generate推理链
        reasoning_chain = self._generate_reasoning_chain(
            problem, category, perspectives
        )
        
        # 7. generateaction方案
        action_plan = self._generate_action_plan(
            problem, category, perspectives
        )
        
        # 8. generate风险警示
        risk_warnings = self._generate_risk_warnings(
            problem, category, perspectives
        )
        
        # 9. generate静心语录
        quotes_for_meditation = self._generate_meditation_quotes(
            category, perspectives
        )
        
        # 10. 计算synthesize评分
        overall_score = sum(d[1] for d in sorted_dims[:5]) / 5
        ethics_score = self._calculate_ethics_score(perspectives)
        wisdom_score = self._calculate_wisdom_score(perspectives)
        feasibility_score = self._calculate_feasibility_score(action_plan)
        
        return DecisionResult(
            timestamp=datetime.now(),
            problem=problem,
            category=category,
            dimension_scores=dimension_scores,
            perspectives=perspectives,
            primary_dimension=primary_dimension,
            secondary_dimensions=secondary_dimensions,
            final_recommendation=final_recommendation,
            reasoning_chain=reasoning_chain,
            action_plan=action_plan,
            risk_warnings=risk_warnings,
            quotes_for_meditation=quotes_for_meditation,
            overall_score=overall_score,
            ethics_score=ethics_score,
            wisdom_score=wisdom_score,
            feasibility_score=feasibility_score
        )
    
    def _classify_problem(self, problem: str) -> ProblemCategory:
        """分类问题"""
        problem_lower = problem.lower()
        
        # 企业经营类
        if any(k in problem_lower for k in ["战略", "规划", "布局", "发展方向"]):
            return ProblemCategory.STRATEGY
        if any(k in problem_lower for k in ["人才", "招聘", "团队", "管理"]):
            return ProblemCategory.TALENT
        if any(k in problem_lower for k in ["市场", "营销", "推广", "获客"]):
            return ProblemCategory.MARKET
        if any(k in problem_lower for k in ["危机", "风险", "紧急", "困境"]):
            return ProblemCategory.CRISIS
        if any(k in problem_lower for k in ["创新", "变革", "转型", "突破"]):
            return ProblemCategory.INNOVATION
        
        # 人生decision类
        if any(k in problem_lower for k in ["职业", "工作", "事业", "发展"]):
            return ProblemCategory.CAREER
        if any(k in problem_lower for k in ["关系", "人际", "合作", "沟通"]):
            return ProblemCategory.RELATIONSHIP
        if any(k in problem_lower for k in ["成长", "提升", "学习", "进步"]):
            return ProblemCategory.GROWTH
        if any(k in problem_lower for k in ["智慧", "领悟", "境界", "心态"]):
            return ProblemCategory.WISDOM
        
        # 文化传承类
        if any(k in problem_lower for k in ["文化", "品牌", "价值观", "使命"]):
            return ProblemCategory.CULTURE
        if any(k in problem_lower for k in ["教育", "培训", "培养", "传承"]):
            return ProblemCategory.EDUCATION
        if any(k in problem_lower for k in ["道德", "伦理", "抉择", "是非"]):
            return ProblemCategory.ETHICS
        
        return ProblemCategory.STRATEGY  # 默认
    
    def _calculate_dimension_scores(
        self, problem: str, category: ProblemCategory
    ) -> Dict[DecisionDimension, float]:
        """计算各维度适配度"""
        scores = {}
        
        for dimension in DecisionDimension:
            base_score = self.dimension_weights.get(dimension, 0.5)
            
            # 根据问题类别调整
            if category == ProblemCategory.ETHICS:
                if dimension in [DecisionDimension.REN, DecisionDimension.YI, DecisionDimension.XIN]:
                    base_score += 0.2
            elif category == ProblemCategory.CRISIS:
                if dimension in [DecisionDimension.ZHENG, DecisionDimension.QI, DecisionDimension.SHI]:
                    base_score += 0.2
            elif category == ProblemCategory.GROWTH:
                if dimension in [DecisionDimension.GROWTH, DecisionDimension.LOOP, DecisionDimension.TRANSCEND]:
                    base_score += 0.2
            elif category == ProblemCategory.INNOVATION:
                if dimension in [DecisionDimension.DIMENSION, DecisionDimension.ZIRAN, DecisionDimension.HUI]:
                    base_score += 0.2
            elif category == ProblemCategory.STRATEGY:
                if dimension in [DecisionDimension.DAO, DecisionDimension.SHI, DecisionDimension.YINYANG]:
                    base_score += 0.2
            
            scores[dimension] = min(base_score, 1.0)
        
        return scores
    
    def _generate_perspectives(
        self, problem: str, category: ProblemCategory,
        dimension_scores: Dict[DecisionDimension, float]
    ) -> List[WisdomPerspective]:
        """generate各学派视角"""
        perspectives = []
        
        # 儒家视角
        confucian_dims = [d for d in dimension_scores.keys() 
                          if d in [DecisionDimension.REN, DecisionDimension.YI, 
                                   DecisionDimension.LI, DecisionDimension.ZHI, 
                                   DecisionDimension.XIN]]
        if confucian_dims:
            scores = [dimension_scores[d] for d in confucian_dims]
            perspectives.append(WisdomPerspective(
                dimension=confucian_dims[0],
                score=sum(scores) / len(scores),
                principle="仁义礼智信",
                guidance=self._get_confucian_guidance(category),
                quotes=self.quotes_database.get("论语", [])[:3],
                warnings=["勿偏执一端", "礼之用和为贵"]
            ))
        
        # 道家视角
        perspectives.append(WisdomPerspective(
            dimension=DecisionDimension.ZIRAN,
            score=dimension_scores.get(DecisionDimension.ZIRAN, 0.5),
            principle="道法自然",
            guidance="顺势而为,无为而治",
            quotes=self.quotes_database.get("道德经", [])[:3],
            warnings=["切忌强求", "过犹不及"]
        ))
        
        # 佛家视角
        perspectives.append(WisdomPerspective(
            dimension=DecisionDimension.KONG,
            score=dimension_scores.get(DecisionDimension.KONG, 0.5),
            principle="缘起性空",
            guidance="看清本质,放下执念",
            quotes=["诸行无常", "诸法无我", "涅槃寂静"],
            warnings=["切忌执着", "放下得失"]
        ))
        
        # 兵法视角
        perspectives.append(WisdomPerspective(
            dimension=DecisionDimension.SHI,
            score=dimension_scores.get(DecisionDimension.SHI, 0.5),
            principle="知己知彼,百战不殆",
            guidance="先谋后动,奇正相生",
            quotes=self.quotes_database.get("孙子兵法", [])[:3],
            warnings=["轻敌必败", "久战必疲"]
        ))
        
        # 成长视角
        perspectives.append(WisdomPerspective(
            dimension=DecisionDimension.GROWTH,
            score=dimension_scores.get(DecisionDimension.GROWTH, 0.5),
            principle="能力可塑,拥抱挑战",
            guidance="将困难视为成长机会",
            quotes=self.quotes_database.get("成长思维", [])[:3],
            warnings=["不要害怕失败", "过程比结果重要"]
        ))
        
        return sorted(perspectives, key=lambda p: p.score, reverse=True)
    
    def _get_confucian_guidance(self, category: ProblemCategory) -> str:
        """get儒家指导"""
        guidance_map = {
            ProblemCategory.ETHICS: "以仁为本,义以为上",
            ProblemCategory.GOVERNANCE: "为政以德,修身齐家",
            ProblemCategory.TALENT: "举贤才,近君子远小人",
            ProblemCategory.CULTURE: "承文脉,彰明德",
            ProblemCategory.STRATEGY: "以义为利,义利合一",
            ProblemCategory.CRISIS: "临危不惧,勇者不惧",
            ProblemCategory.GROWTH: "学而时习,温故知新",
            ProblemCategory.WISDOM: "知之為知之,格物致知"
        }
        return guidance_map.get(category, "君子求诸己")
    
    def _generate_recommendation(
        self, problem: str, category: ProblemCategory,
        primary_dimension: DecisionDimension,
        perspectives: List[WisdomPerspective]
    ) -> str:
        """generatesynthesize建议"""
        recommendations = {
            ProblemCategory.STRATEGY: f"以[{primary_dimension.value}]为核心,结合儒家中庸之道,兼顾义利平衡,制定长期战略规划.",
            ProblemCategory.TALENT: f"遵循素书[任贤使能]原则,以[德才兼备]为标准甄选人才,注重培养与激励.",
            ProblemCategory.MARKET: f"借鉴兵法[知己知彼],深入了解用户需求,以[仁者爱人]之心服务客户.",
            ProblemCategory.CRISIS: f"运用道家[无为]智慧,保持冷静;同时借鉴兵法[奇正相生],危中寻机.",
            ProblemCategory.INNOVATION: f"秉持[苟日新]精神,敢于突破常规;参考科幻思维,进行维度超越.",
            ProblemCategory.CAREER: f"以[修身]为本,不断精进;参考成长思维,将挑战转化为成长机会.",
            ProblemCategory.RELATIONSHIP: f"遵循[己所不欲勿施于人]原则,以诚相待;兼顾义利,求同存异.",
            ProblemCategory.GROWTH: f"拥抱[成长型思维],相信能力可培养;从失败中学习,持续迭代.",
            ProblemCategory.WISDOM: f"以[格物致知]为方法,以[明明德]为目标,不断提升认知境界.",
            ProblemCategory.CULTURE: f"承继[仁义礼智信]传统,fusion时代精神,建设有灵魂的组织文化.",
            ProblemCategory.EDUCATION: f"以[有教无类]精神,因材施教;注重品德育人,而非仅重才能.",
            ProblemCategory.ETHICS: f"以[义以为上]为准绳,坚守底线;吉莫吉于知足,莫被利诱."
        }
        return recommendations.get(category, "synthesize各派智慧,审慎decision.")
    
    def _generate_reasoning_chain(
        self, problem: str, category: ProblemCategory,
        perspectives: List[WisdomPerspective]
    ) -> List[str]:
        """generate推理链"""
        chain = [
            f"[第一步:问题界定]分析为{category.value}问题",
            "[第二步:维度评估]计算各智慧体系适配度"
        ]
        
        for p in perspectives[:3]:
            chain.append(f"[第三步:{p.dimension.value}视角]{p.principle} → {p.guidance}")
        
        chain.extend([
            "[第四步:synthesizefusion]加权整合各学派观点",
            "[第五步:decision输出]形成最终action建议"
        ])
        
        return chain
    
    def _generate_action_plan(
        self, problem: str, category: ProblemCategory,
        perspectives: List[WisdomPerspective]
    ) -> List[str]:
        """generateaction方案"""
        plan = []
        
        if category == ProblemCategory.STRATEGY:
            plan = [
                "1. 深入调研,了解内外部环境",
                "2. 明确使命愿景,确立核心价值观",
                "3. 制定3-5年战略规划",
                "4. 建立阶段性目标与里程碑",
                "5. 配置资源与组织保障"
            ]
        elif category == ProblemCategory.TALENT:
            plan = [
                "1. 明确人才标准:德才兼备",
                "2. 建立招聘选拔机制",
                "3. 设计培养发展体系",
                "4. 完善激励约束机制",
                "5. 定期评估与反馈"
            ]
        elif category == ProblemCategory.CRISIS:
            plan = [
                "1. 保持冷静,分析形势",
                "2. recognize核心问题与关键变量",
                "3. 制定应急响应方案",
                "4. 准备多套应对预案",
                "5. 快速action,动态调整"
            ]
        else:
            plan = [
                "1. 全面分析问题本质",
                "2. 收集相关信息与数据",
                "3. 借鉴多维度智慧思考",
                "4. 制定详细action计划",
                "5. 执行并持续优化"
            ]
        
        return plan
    
    def _generate_risk_warnings(
        self, problem: str, category: ProblemCategory,
        perspectives: List[WisdomPerspective]
    ) -> List[str]:
        """generate风险警示"""
        warnings = []
        
        for p in perspectives[:3]:
            if p.warnings:
                warnings.extend(p.warnings)
        
        warnings.extend([
            "切忌急于求成,要循序渐进",
            "保持开放心态,听取不同意见",
            "action前要充分评估风险"
        ])
        
        return list(set(warnings))[:5]
    
    def _generate_meditation_quotes(
        self, category: ProblemCategory,
        perspectives: List[WisdomPerspective]
    ) -> List[str]:
        """generate静心语录"""
        quotes = []
        
        for p in perspectives:
            quotes.extend(p.quotes)
        
        return quotes[:5]
    
    def _calculate_ethics_score(self, perspectives: List[WisdomPerspective]) -> float:
        """计算伦理评分"""
        ethical_dims = [DecisionDimension.REN, DecisionDimension.YI, 
                        DecisionDimension.XIN, DecisionDimension.GONG]
        scores = [p.score for p in perspectives 
                  if p.dimension in ethical_dims]
        return sum(scores) / len(scores) if scores else 0.5
    
    def _calculate_wisdom_score(self, perspectives: List[WisdomPerspective]) -> float:
        """计算智慧评分"""
        wisdom_dims = [DecisionDimension.ZHI, DecisionDimension.HUI,
                      DecisionDimension.MING, DecisionDimension.ZIRAN]
        scores = [p.score for p in perspectives
                  if p.dimension in wisdom_dims]
        return sum(scores) / len(scores) if scores else 0.5
    
    def _calculate_feasibility_score(self, action_plan: List[str]) -> float:
        """计算可行性评分"""
        # 简单评估:action方案越具体,可行性越高
        score = min(len(action_plan) * 0.15 + 0.3, 0.95)
        return score
    
    def batch_analyze(self, problems: List[str]) -> List[DecisionResult]:
        """批量分析"""
        return [self.analyze_problem(p) for p in problems]

def quick_decide(problem: str) -> str:
    """
    快速decision接口
    
    用法:
    >>> quick_decide("如何实现企业十倍增长")
    """
    engine = SupremeDecisionFusionEngine()
    result = engine.analyze_problem(problem)
    
    output = f"""
{'='*60}
🎯 超级decisionfusion分析
{'='*60}

📋 问题: {result.problem}
📂 类别: {result.category.value}

⭐ 主维度: {result.primary_dimension.value}
⭐ synthesize评分: {result.overall_score:.1%}

{'-'*60}
📖 synthesize建议:
{result.final_recommendation}

{'-'*60}
📝 action方案:
{chr(10).join(result.action_plan)}

{'-'*60}
⚠️ 风险警示:
{chr(10).join(result.risk_warnings)}

{'-'*60}
💭 静心语录:
{chr(10).join(f"  • {q}" for q in result.quotes_for_meditation)}

{'='*60}
"""
    return output

# 导出
__all__ = [
    'SupremeDecisionFusionEngine',
    'DecisionDimension',
    'ProblemCategory',
    'WisdomPerspective',
    'DecisionResult',
    'quick_decide'
]
