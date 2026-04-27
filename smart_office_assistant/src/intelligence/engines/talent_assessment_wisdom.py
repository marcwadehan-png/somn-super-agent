# -*- coding: utf-8 -*-
"""
智慧人才评估系统 v5.5.0
Wisdom Talent Assessment System

fusion儒家人才观,素书人才三境,刘劭人物志
提供多维度的人才评估框架

版本: v5.5.0
日期: 2026-04-02
"""

from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

class TalentLevel(Enum):
    """人才等级 - 素书三境"""
    JUN = "俊"         # 俊者,人之所羡 - 高智商
    HAO = "豪"         # 豪者,人之所畏 - 高情商
    JIE = "杰"         # 杰者,人之所称 - synthesize卓越
    XIAN = "贤"        # 贤者,品学兼优
    SHENG = "圣"       # 圣者,至高境界

class TalentDimension(Enum):
    """人才维度"""
    # 儒家德才维度
    REN = "仁"          # 仁爱之心
    YI = "义"          # 道义之心
    LI = "礼"          # 礼仪之心
    ZHI = "智"         # 智慧之心
    XIN = "信"         # 诚信之心
    
    # 能力维度
    YINGLI = "领导力"   # 领导力
    CHUANGXIN = "创造力"  # 创造力
    XUELI = "学习力"    # 学习力
    ZHIXING = "执行力"  # 执行力
    SOUJING = "沟通力"  # 沟通力

@dataclass
class TalentProfile:
    """人才画像"""
    name: str
    
    # 五常评分 (0-10)
    ren_score: float = 0.0      # 仁
    yi_score: float = 0.0       # 义
    li_score: float = 0.0       # 礼
    zhi_score: float = 0.0      # 智
    xin_score: float = 0.0      # 信
    
    # 能力评分 (0-10)
    leadership: float = 0.0     # 领导力
    creativity: float = 0.0     # 创造力
    learning: float = 0.0       # 学习力
    execution: float = 0.0      # 执行力
    communication: float = 0.0  # 沟通力
    
    # 潜力
    growth_potential: float = 0.0   # 成长潜力
    character_stability: float = 0.0  # 品格稳定性
    
    # 素书评级
    talent_level: TalentLevel = TalentLevel.XIAN
    
    # synthesize评分
    overall_score: float = 0.0
    ethics_score: float = 0.0
    competence_score: float = 0.0

@dataclass
class TalentAssessment:
    """人才评估报告"""
    timestamp: datetime
    candidate: TalentProfile
    
    # 儒家评估
    confucian_assessment: str
    five_virtues_analysis: Dict[str, str]
    
    # 素书评估
    talent_level_analysis: str
    sufu_wisdom: str
    
    # synthesize建议
    placement_suggestion: str        # 岗位建议
    development_path: List[str]      # 发展路径
    coaching_points: List[str]       # 辅导要点
    risks_and_warnings: List[str]    # 风险提示
    
    # 经典指引
    classical_quotes: List[str]      # 相关经典语录
    historical_analogy: str          # 历史人物类比

class WisdomTalentAssessor:
    """
    智慧人才评估系统
    
    fusion:
    1. 儒家人才观 - 德才兼备,君子品格
    2. 素书三境 - 俊豪杰贤圣
    3. 刘劭人物志 - 九征,十二才
    4. 现代能力模型 - 领导力,执行力
    """
    
    def __init__(self):
        self.talent_database = {}
        self.classical_analogies = self._build_analogies()
        self.assessment_matrix = self._build_matrix()
    
    def _build_analogies(self) -> Dict[str, str]:
        """构建历史类比"""
        return {
            TalentLevel.JUN: "张良(运筹帷幄,智谋超群)",
            TalentLevel.HAO: "管仲(治国理财,善用人心)",
            TalentLevel.JIE: "孔子(德才兼备,百世师范)",
            TalentLevel.XIAN: "颜渊(品学兼优,贤德有方)",
            TalentLevel.SHENG: "周公(立德立功立言,三不朽)"
        }
    
    def _build_matrix(self) -> Dict[str, Any]:
        """构建评估矩阵"""
        return {
            "high_zhi_low_ren": {
                "type": "术士",
                "warning": "智慧有余,仁爱不足,需防才胜于德",
                "guidance": "培养仁爱之心,学习儒家仁道"
            },
            "high_ren_low_zhi": {
                "type": "仁者",
                "warning": "仁爱有余,智慧不足,需防好心办坏事",
                "guidance": "提升专业能力,学习格物致知"
            },
            "balanced_virtue": {
                "type": "君子",
                "warning": "德才均衡,是理想人才",
                "guidance": "持续精进,向圣人境界迈进"
            },
            "high_ren_high_zhi": {
                "type": "英才",
                "warning": "德才兼备,可堪大用",
                "guidance": "担当重任,发挥引领作用"
            }
        }
    
    def assess(self, profile: TalentProfile) -> TalentAssessment:
        """
        评估人才
        
        Args:
            profile: 人才画像
            
        Returns:
            TalentAssessment: 评估结果
        """
        # 计算synthesize评分
        ethics_score = (
            profile.ren_score + profile.yi_score + 
            profile.li_score + profile.zhi_score + 
            profile.xin_score
        ) / 5
        
        competence_score = (
            profile.leadership + profile.creativity + 
            profile.learning + profile.execution + 
            profile.communication
        ) / 5
        
        profile.ethics_score = ethics_score
        profile.competence_score = competence_score
        profile.overall_score = (ethics_score * 0.4 + competence_score * 0.6)
        
        # 确定人才等级
        profile.talent_level = self._determine_level(ethics_score, competence_score)
        
        # 五常分析
        five_virtues = {
            "仁": self._analyze_virtue("仁", profile.ren_score),
            "义": self._analyze_virtue("义", profile.yi_score),
            "礼": self._analyze_virtue("礼", profile.li_score),
            "智": self._analyze_virtue("智", profile.zhi_score),
            "信": self._analyze_virtue("信", profile.xin_score)
        }
        
        # get历史类比
        analogy = self.classical_analogies.get(
            profile.talent_level, "synthesize型人才"
        )
        
        return TalentAssessment(
            timestamp=datetime.now(),
            candidate=profile,
            confucian_assessment=self._confucian_assessment(profile),
            five_virtues_analysis=five_virtues,
            talent_level_analysis=self._level_analysis(profile.talent_level),
            sufu_wisdom=self._sufu_wisdom(profile.talent_level),
            placement_suggestion=self._suggest_placement(profile),
            development_path=self._development_path(profile),
            coaching_points=self._coaching_points(profile),
            risks_and_warnings=self._risk_warnings(profile),
            classical_quotes=self._select_quotes(profile),
            historical_analogy=analogy
        )
    
    def _determine_level(self, ethics: float, competence: float) -> TalentLevel:
        """确定人才等级"""
        if ethics >= 9 and competence >= 9:
            return TalentLevel.SHENG
        elif ethics >= 8.5 and competence >= 8.5:
            return TalentLevel.JIE
        elif competence >= 9 and ethics >= 7:
            return TalentLevel.JUN
        elif ethics >= 9 and competence >= 7:
            return TalentLevel.XIAN
        else:
            return TalentLevel.HAO
    
    def _analyze_virtue(self, virtue: str, score: float) -> str:
        """分析单项美德"""
        if score >= 9:
            return f"{virtue}性极高({score}/10),功德圆满"
        elif score >= 7:
            return f"{virtue}性较高({score}/10),基础扎实"
        elif score >= 5:
            return f"{virtue}性一般({score}/10),有待提升"
        else:
            return f"{virtue}性不足({score}/10),需重点培养"
    
    def _confucian_assessment(self, profile: TalentProfile) -> str:
        """儒家评估"""
        return f"""
[儒家视角评估]

品德synthesize:{profile.ethics_score:.1f}/10

分析:
• 仁爱指数:{profile.ren_score:.1f}/10 - {'仁心厚重,利他精神强' if profile.ren_score >= 7 else '仁心有待培育'}
• 义气指数:{profile.yi_score:.1f}/10 - {'道义坚守,原则鲜明' if profile.yi_score >= 7 else '义气不足,易受利益驱动'}
• 礼仪指数:{profile.li_score:.1f}/10 - {'礼数周全,规矩守法' if profile.li_score >= 7 else '礼仪欠缺,边界感弱'}
• 智慧指数:{profile.zhi_score:.1f}/10 - {'智慧过人,见识独到' if profile.zhi_score >= 7 else '智慧一般,需持续学习'}
• 诚信指数:{profile.xin_score:.1f}/10 - {'言而有信,值得托付' if profile.xin_score >= 7 else '信誉不稳,需重点关注'}

synthesizejudge:{'德才兼备,可堪重任' if profile.ethics_score >= 7 else '有所欠缺,需重点培养'}
"""
    
    def _level_analysis(self, level: TalentLevel) -> str:
        """等级分析"""
        analyses = {
            TalentLevel.JUN: "俊者:思维敏锐,智谋过人,善于分析与创新",
            TalentLevel.HAO: "豪者:意志坚定,有胆有识,善于决断与影响",
            TalentLevel.JIE: "杰者:德才兼备,文武兼修,能独当一面",
            TalentLevel.XIAN: "贤者:品学兼优,稳重踏实,可信赖委任",
            TalentLevel.SHENG: "圣者:大德大才,超凡入圣,可担历史重任"
        }
        return analyses.get(level, "synthesize人才")
    
    def _sufu_wisdom(self, level: TalentLevel) -> str:
        """素书智慧"""
        wisdom = {
            TalentLevel.JUN: "俊者,人之所羡;小人见之,如明珠在侧.当慎防嫉妒之心.",
            TalentLevel.HAO: "豪者,人之所畏;领袖之才,能感化众人,可担领导重任.",
            TalentLevel.JIE: "杰者,人之所服;才德皆佳,众心所向,能成大事.",
            TalentLevel.XIAN: "贤者,人之所称;品行端正,学识渊博,是稳定组织的中坚力量.",
            TalentLevel.SHENG: "圣者,人之所敬;修身治人,无所不通,乃千古罕见之才."
        }
        return wisdom.get(level, "synthesize评价,待进一步考察.")
    
    def _suggest_placement(self, profile: TalentProfile) -> str:
        """岗位建议"""
        if profile.talent_level in [TalentLevel.JIE, TalentLevel.SHENG]:
            return "可担任高级管理岗,参与战略decision"
        elif profile.talent_level == TalentLevel.JUN:
            return "适合战略分析,产品研发,创新类岗位"
        elif profile.talent_level == TalentLevel.HAO:
            return "适合项目管理,销售,对外关系类岗位"
        else:
            return "适合专业技能类岗位,可逐步培养管理能力"
    
    def _development_path(self, profile: TalentProfile) -> List[str]:
        """发展路径"""
        path = []
        
        if profile.ren_score < 7:
            path.append("短期:参加仁爱文化培训,培育利他思维")
        if profile.zhi_score < 7:
            path.append("短期:建立系统学习计划,提升专业智慧")
        if profile.leadership < 7:
            path.append("中期:担任小项目负责人,锻炼领导力")
        if profile.execution < 7:
            path.append("中期:建立目标管理机制,提升执行力")
        
        path.extend([
            "长期:持续修身,追求德才兼备的君子境界",
            "长期:参与重大项目,积累synthesize能力"
        ])
        
        return path
    
    def _coaching_points(self, profile: TalentProfile) -> List[str]:
        """辅导要点"""
        points = []
        
        min_scores = [
            (profile.ren_score, "仁爱:多关爱他人,培养同理心"),
            (profile.yi_score, "义气:坚守原则,做正确的事"),
            (profile.li_score, "礼仪:尊重规矩,注重细节"),
            (profile.zhi_score, "智慧:持续学习,深度思考"),
            (profile.xin_score, "诚信:言出必行,恪守承诺")
        ]
        
        # 取分数最低的三项
        min_scores.sort(key=lambda x: x[0])
        for _, guidance in min_scores[:3]:
            points.append(guidance)
        
        return points
    
    def _risk_warnings(self, profile: TalentProfile) -> List[str]:
        """风险警示"""
        warnings = []
        
        if profile.zhi_score > 9 and profile.ren_score < 6:
            warnings.append("才胜于德:智慧高但仁爱不足,需防止'聪明反被聪明误'")
        if profile.leadership > 8 and profile.xin_score < 6:
            warnings.append("有威无信:领导力强但诚信不足,可能引发团队信任危机")
        if profile.execution > 8 and profile.yi_score < 6:
            warnings.append("有行无义:执行力强但道义不足,可能做了'正确的错事'")
        if profile.creativity > 8 and profile.li_score < 6:
            warnings.append("有奇无礼:创造力强但礼仪不足,可能破坏规则和边界")
        
        if not warnings:
            warnings.append("当前未发现明显风险点,但需持续关注品德修养")
        
        return warnings
    
    def _select_quotes(self, profile: TalentProfile) -> List[str]:
        """选择相关语录"""
        quotes = []
        
        if profile.zhi_score >= 8:
            quotes.append("知之为知之,不知为不知,是知也 --论语")
        if profile.ren_score >= 8:
            quotes.append("仁者爱人,己所不欲勿施于人 --论语")
        if profile.talent_level == TalentLevel.JUN:
            quotes.append("俊者,人之所羡 --素书")
        if profile.talent_level in [TalentLevel.JIE, TalentLevel.SHENG]:
            quotes.append("君子求诸己,小人求诸人 --论语")
        
        quotes.append("天行健,君子以自强不息 --易经")
        
        return quotes[:5]
    
    def create_profile(self, name: str, **scores) -> TalentProfile:
        """
        创建人才画像
        
        用法:
        >>> assessor.create_profile("张某", ren_score=8, zhi_score=9, leadership=8)
        """
        return TalentProfile(name=name, **scores)

def quick_assess(name: str, scores: Dict[str, float]) -> str:
    """
    快速人才评估
    
    用法:
    >>> quick_assess("候选人", {"ren_score": 8, "zhi_score": 9, "leadership": 8})
    """
    assessor = WisdomTalentAssessor()
    
    profile = TalentProfile(name=name, **scores)
    result = assessor.assess(profile)
    
    output = f"""
{'='*60}
👤 智慧人才评估报告
{'='*60}

📋 评估对象: {name}
🏅 人才等级: {result.candidate.talent_level.name}({result.candidate.talent_level.value})
📊 synthesize评分: {result.candidate.overall_score:.1f}/10

{'-'*60}
🏛️ 儒家五常评估:
{result.confucian_assessment}

{'-'*60}
📜 素书智慧评级:
{result.talent_level_analysis}

{result.sufu_wisdom}

{'-'*60}
🎯 岗位建议:
{result.placement_suggestion}

{'-'*60}
📈 发展路径:
{chr(10).join(f"  {i+1}. {p}" for i, p in enumerate(result.development_path))}

{'-'*60}
💡 辅导要点:
{chr(10).join(f"  • {c}" for c in result.coaching_points)}

{'-'*60}
⚠️ 风险提示:
{chr(10).join(f"  • {w}" for w in result.risks_and_warnings)}

{'-'*60}
📚 经典指引:
{chr(10).join(f"  '{q}'" for q in result.classical_quotes)}

{'-'*60}
🔗 历史类比: {result.historical_analogy}

{'='*60}
"""
    
    return output

# 导出
__all__ = [
    'WisdomTalentAssessor',
    'TalentLevel',
    'TalentDimension',
    'TalentProfile',
    'TalentAssessment',
    'quick_assess'
]
