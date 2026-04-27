# -*- coding: utf-8 -*-
"""
企业战略decision系统 v5.5.0
Enterprise Strategy Decision System

fusion儒家治国,素书decision,兵法战略的智能战略decision系统

版本: v5.5.0
日期: 2026-04-02
"""

from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

class DecisionType(Enum):
    """decision类型"""
    STRATEGIC = "战略decision"        # 战略层
    TACTICAL = "战术decision"        # 战术层
    OPERATIONAL = "运营decision"     # 运营层

class RiskLevel(Enum):
    """风险等级"""
    LOW = "低风险"
    MEDIUM = "中风险"
    HIGH = "高风险"
    CRITICAL = "极高风险"

@dataclass
class StrategyOption:
    """战略选项"""
    name: str
    description: str
    pros: List[str]
    cons: List[str]
    risk_level: RiskLevel
    resource_requirements: Dict[str, Any]
    classical_wisdom: str              # 相关古典智慧
    expected_outcomes: List[str]

@dataclass
class StrategicDecision:
    """战略decision"""
    decision_type: DecisionType
    title: str
    description: str
    
    # 选项分析
    options: List[StrategyOption]
    recommended_option: str
    
    # 儒家视角
    confucian_analysis: str           # 仁义礼智信分析
    confucian_quote: str               # 相关语录
    
    # 兵法视角
    military_analysis: str             # 知己知彼分析
    military_quote: str
    
    # 素书视角
    sufu_analysis: str                 # 五德分析
    sufu_quote: str
    
    # synthesize_decision
    final_recommendation: str
    implementation_steps: List[str]
    risk_mitigation: List[str]
    
    # 评估
    confidence: float
    potential_obstacles: List[str]

class EnterpriseStrategySystem:
    """
    企业战略decision系统
    
    fusion三大智慧体系:
    1. 儒家治国 - 以德治国,以民为本
    2. 素书decision - 道德仁义礼五德
    3. 兵法战略 - 知己知彼,奇正相生
    
    功能:
    1. 多维度战略分析
    2. 古典智慧与现代管理fusion
    3. 风险评估与缓解
    4. decision质量评估
    """
    
    def __init__(self):
        self.decision_templates = self._build_templates()
        self.classical_quotes = self._build_quotes()
    
    def _build_templates(self) -> Dict[str, Dict]:
        """构建decision模板"""
        return {
            "market_expansion": {
                "title": "市场扩张decision",
                "options": [
                    {
                        "name": "激进扩张",
                        "pros": ["快速占领市场", "形成规模效应"],
                        "cons": ["资源压力大", "风险高"],
                        "risk": RiskLevel.HIGH
                    },
                    {
                        "name": "稳步扩张",
                        "pros": ["风险可控", "资源匹配"],
                        "cons": ["速度较慢", "可能错失机会"],
                        "risk": RiskLevel.MEDIUM
                    },
                    {
                        "name": "聚焦深耕",
                        "pros": ["精耕细作", "壁垒高"],
                        "cons": ["市场空间有限", "增长慢"],
                        "risk": RiskLevel.LOW
                    }
                ],
                "confucian": "子曰:'无欲速,无见小利.欲速则不达,见小利则大事不成.'",
                "military": "孙子曰:'知己知彼,百战不殆.'",
                "sufu": "素书曰:'危于利也,害于义也.'"
            },
            "talent_decision": {
                "title": "人才decision",
                "options": [
                    {
                        "name": "外部引进",
                        "pros": ["快速补充能力", "带来新思维"],
                        "cons": ["融入风险", "成本高"],
                        "risk": RiskLevel.MEDIUM
                    },
                    {
                        "name": "内部培养",
                        "pros": ["忠诚度高", "文化契合"],
                        "cons": ["周期长", "能力有天花板"],
                        "risk": RiskLevel.LOW
                    },
                    {
                        "name": "内外结合",
                        "pros": ["优势互补", "平衡风险"],
                        "cons": ["管理复杂度高"],
                        "risk": RiskLevel.MEDIUM
                    }
                ],
                "confucian": "子曰:'举直错诸枉,能使枉者直.'",
                "military": "孙子曰:'善战者,致人而不致于人.'",
                "sufu": "素书曰:'俊者,人之所羡;豪者,人之所畏.'"
            },
            "competition_strategy": {
                "title": "竞争strategydecision",
                "options": [
                    {
                        "name": "正面竞争",
                        "pros": ["展示实力", "争夺市场份额"],
                        "cons": ["消耗资源", "可能引发价格战"],
                        "risk": RiskLevel.HIGH
                    },
                    {
                        "name": "差异化竞争",
                        "pros": ["避开红海", "建立壁垒"],
                        "cons": ["需要创新", "教育市场"],
                        "risk": RiskLevel.MEDIUM
                    },
                    {
                        "name": "合作共赢",
                        "pros": ["资源共享", "降低风险"],
                        "cons": ["控制力弱", "利益分配难"],
                        "risk": RiskLevel.MEDIUM
                    }
                ],
                "confucian": "子曰:'君子和而不同,小人同而不和.'",
                "military": "孙子曰:'不战而屈人之兵,善之善者也.'",
                "sufu": "素书曰:'义者,人之所宜.'"
            },
            "investment_decision": {
                "title": "投资decision",
                "options": [
                    {
                        "name": "大胆投资",
                        "pros": ["高风险高回报", "抢占先机"],
                        "cons": ["失败代价大", "资金压力大"],
                        "risk": RiskLevel.CRITICAL
                    },
                    {
                        "name": "稳健投资",
                        "pros": ["风险可控", "可持续"],
                        "cons": ["回报有限", "可能错失机会"],
                        "risk": RiskLevel.LOW
                    },
                    {
                        "name": "分步投资",
                        "pros": ["灵活调整", "降低风险"],
                        "cons": ["周期长", "可能失去先发优势"],
                        "risk": RiskLevel.MEDIUM
                    }
                ],
                "confucian": "子曰:'君子喻于义,小人喻于利.'",
                "military": "孙子曰:'兵贵胜,不贵久.'",
                "sufu": "素书曰:'吉莫吉于知足.'"
            }
        }
    
    def _build_quotes(self) -> Dict[str, List[str]]:
        """构建语录库"""
        return {
            "confucian": {
                "仁": ["仁者爱人", "己所不欲勿施于人", "克己复礼为仁"],
                "义": ["君子喻于义", "见得思义", "义以为上"],
                "礼": ["礼之用和为贵", "不知礼无以立", "克己复礼"],
                "智": ["知之为知之", "学而不思则罔", "三思而后行"],
                "信": ["人无信不立", "言必信行必果", "与朋友交言而有信"]
            },
            "military": {
                "知己知彼": ["知己知彼百战不殆", "知彼知己胜乃不殆"],
                "奇正": ["奇正相生", "以正合以奇胜", "善出奇者无穷"],
                "势": ["善战者求之于势", "势如破竹", "审时度势"],
                "速": ["兵贵胜不贵久", "兵之情主速", "速战速决"]
            },
            "sufu": {
                "道": ["道者人之所蹈", "得道多助失道寡助"],
                "德": ["德者人之所失", "以德服人", "德不孤必有邻"],
                "仁": ["仁者人之所亲", "仁者无敌", "仁者不忧"],
                "义": ["义者人之所宜", "义以为上", "义利合一"],
                "礼": ["礼者人之所履", "不知礼无以立", "礼尚往来"]
            }
        }
    
    def analyze_decision(
        self,
        decision_type: str,
        context: Dict[str, Any]
    ) -> StrategicDecision:
        """
        分析decision
        
        Args:
            decision_type: decision类型
            context: decision上下文
            
        Returns:
            StrategicDecision: 战略decision结果
        """
        template = self.decision_templates.get(decision_type, {})
        
        if not template:
            return self._generic_decision(decision_type, context)
        
        # 构建选项
        options = []
        for opt in template.get("options", []):
            options.append(StrategyOption(
                name=opt["name"],
                description="",
                pros=opt["pros"],
                cons=opt["cons"],
                risk_level=opt["risk"],
                resource_requirements={},
                classical_wisdom="",
                expected_outcomes=[]
            ))
        
        # 确定推荐
        recommended = self._recommend_option(options)
        
        return StrategicDecision(
            decision_type=DecisionType.STRATEGIC,
            title=template["title"],
            description=context.get("description", ""),
            options=options,
            recommended_option=recommended.name,
            confucian_analysis=self._confucian_analysis(template),
            confucian_quote=template.get("confucian", ""),
            military_analysis=self._military_analysis(template),
            military_quote=template.get("military", ""),
            sufu_analysis=self._sufu_analysis(template),
            sufu_quote=template.get("sufu", ""),
            final_recommendation=self._generate_recommendation(template, recommended),
            implementation_steps=self._generate_steps(recommended),
            risk_mitigation=self._generate_risk_mitigation(recommended),
            confidence=0.85,
            potential_obstacles=["资源约束", "执行偏差", "市场变化"]
        )
    
    def _recommend_option(self, options: List[StrategyOption]) -> StrategyOption:
        """推荐选项"""
        # 简化逻辑:优先选择中等风险
        for opt in options:
            if opt.risk_level == RiskLevel.MEDIUM:
                return opt
        return options[1] if len(options) > 1 else options[0]
    
    def _confucian_analysis(self, template: Dict) -> str:
        """儒家分析"""
        return f"""
[儒家五常视角]

仁:decision是否体现仁爱之心?
  - 是否关爱员工利益?
  - 是否考虑客户价值?

义:decision是否合乎道义?
  - 是否正当合法?
  - 是否合乎商业伦理?

礼:decision是否遵循规范?
  - 是否按程序decision?
  - 是否尊重相关方?

智:decision是否明智?
  - 是否经过深思熟虑?
  - 是否有多方案比较?

信:decision是否诚信?
  - 是否言出必行?
  - 是否对各方负责?
"""
    
    def _military_analysis(self, template: Dict) -> str:
        """兵法分析"""
        return f"""
[孙子兵法视角]

知己知彼:
  - 是否充分了解自身实力?
  - 是否深入分析竞争对手?

奇正相生:
  - 是否有正面竞争strategy?
  - 是否有出奇制胜的方案?

审时度势:
  - 时机是否成熟?
  - 形势是否有利?

先为不可胜:
  - 是否先确保立于不败之地?
  - 是否控制最大风险?
"""
    
    def _sufu_analysis(self, template: Dict) -> str:
        """素书分析"""
        return f"""
[素书五德视角]

道:decision是否符合规律?
  - 是否顺应市场规律?
  - 是否符合行业发展趋势?

德:decision是否体现德行?
  - 是否以德服人?
  - 是否积累德望资本?

仁:decision是否体现仁爱?
  - 是否仁者爱人?
  - 是否照顾各方利益?

义:decision是否适宜得当?
  - 是否做该做的事?
  - 是否把握好分寸?

礼:decision是否规范有序?
  - 是否有章可循?
  - 是否按规矩行事?
"""
    
    def _generate_recommendation(self, template: Dict, option: StrategyOption) -> str:
        """generate建议"""
        return f"""
基于多维度分析,推荐[{option.name}]方案.

核心理由:
1. 风险适中,兼顾发展与稳健
2. 符合{option.risk_level.value}控制原则
3. 资源投入与回报预期匹配

实施要点:
- 稳扎稳打,不冒进
- 持续评估,动态调整
- 关注风险,及时应对
"""
    
    def _generate_steps(self, option: StrategyOption) -> List[str]:
        """generate步骤"""
        return [
            "第一阶段:准备期 - 完善方案,配置资源",
            "第二阶段:试点期 - 小范围验证,积累经验",
            "第三阶段:推广期 - 逐步扩大,稳定推进",
            "第四阶段:优化期 - 持续改进,追求卓越"
        ]
    
    def _generate_risk_mitigation(self, option: StrategyOption) -> List[str]:
        """generate风险缓解"""
        return [
            f"风险监控:建立{option.name}风险预警机制",
            "资源配置:预留应急资源,应对突发情况",
            "动态调整:根据实际情况及时调整strategy",
            "沟通机制:保持与各利益相关方的沟通"
        ]
    
    def _generic_decision(self, decision_type: str, context: Dict) -> StrategicDecision:
        """通用decision"""
        return StrategicDecision(
            decision_type=DecisionType.STRATEGIC,
            title=decision_type,
            description=context.get("description", ""),
            options=[],
            recommended_option="待分析",
            confucian_analysis="需要进行儒家五常分析",
            confucian_quote="子曰:三思而后行",
            military_analysis="需要进行兵法分析",
            military_quote="知己知彼,百战不殆",
            sufu_analysis="需要进行素书五德分析",
            sufu_quote="道者,人之所蹈",
            final_recommendation="请提供更详细的decision信息",
            implementation_steps=[],
            risk_mitigation=[],
            confidence=0.5,
            potential_obstacles=[]
        )
    
    def batch_analyze(
        self, decisions: List[Dict]
    ) -> List[StrategicDecision]:
        """批量分析"""
        return [self.analyze_decision(d["type"], d["context"]) 
                for d in decisions]

def quick_decide(decision_type: str, description: str) -> str:
    """
    快速decision分析
    
    用法:
    >>> quick_decide("market_expansion", "是否进入新市场")
    """
    system = EnterpriseStrategySystem()
    result = system.analyze_decision(decision_type, {"description": description})
    
    output = f"""
{'='*60}
🎯 企业战略decision分析
{'='*60}

📋 decision类型: {result.title}
📝 decision描述: {result.description}

{'='*60}
🏛️ 儒家视角 (仁义礼智信)
{result.confucian_quote}

{result.confucian_analysis}

{'='*60}
⚔️ 兵法视角 (知己知彼)
{result.military_quote}

{result.military_analysis}

{'='*60}
📜 素书视角 (道德仁义礼)
{result.sufu_quote}

{result.sufu_analysis}

{'='*60}
✅ 最终建议: {result.recommended_option}

{result.final_recommendation}

{'-'*60}
📝 实施步骤:
{chr(10).join(f"  {i+1}. {s}" for i, s in enumerate(result.implementation_steps))}

{'-'*60}
⚠️ 风险缓解:
{chr(10).join(f"  • {r}" for r in result.risk_mitigation)}

{'-'*60}
🎲 置信度: {result.confidence:.0%}

{'='*60}
"""
    
    return output

# 导出
__all__ = [
    'EnterpriseStrategySystem',
    'DecisionType',
    'RiskLevel',
    'StrategyOption',
    'StrategicDecision',
    'quick_decide'
]
