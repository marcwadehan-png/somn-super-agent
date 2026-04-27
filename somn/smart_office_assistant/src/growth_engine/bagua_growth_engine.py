"""
八卦增长解决方案引擎 v1.0
BaGua Growth Solution Engine

将八卦哲学融入商业增长战略分析:

八卦与商业领域对应:
- 乾(天): 战略规划,领导力,品牌定位
- 坤(地): 团队建设,企业文化,客户关系
- 震(雷): 变革创新,危机应对,市场突破
- 巽(风): 营销传播,渠道渗透,品牌传播
- 坎(水): 风险管理,财务管理,产品迭代
- 离(火): 客户服务,品牌公关,用户体验
- 艮(山): 核心竞争力,专业壁垒,稳定发展
- 兑(泽): 商务谈判,合作共赢,销售转化

版本: v1.0
更新: 2026-04-02
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

class BaGua(Enum):
    """八卦枚举"""
    QIAN = ("乾", "☰", "天", "健", "领导力", "战略规划", "刚健进取")
    DUI = ("兑", "☱", "泽", "悦", "销售转化", "商务谈判", "喜悦沟通")
    LI = ("离", "☲", "火", "丽", "品牌公关", "客户服务", "光明照耀")
    ZHEN = ("震", "☳", "雷", "动", "变革创新", "危机应对", "雷厉风行")
    XUN = ("巽", "☴", "风", "入", "营销传播", "渠道渗透", "风化天下")
    KAN = ("坎", "☵", "水", "陷", "风险管理", "财务管理", "险中求胜")
    GEN = ("艮", "☶", "山", "止", "核心竞争力", "专业壁垒", "稳重如山")
    KUN = ("坤", "☷", "地", "顺", "团队建设", "企业文化", "厚德载物")

    def __init__(self, name: str, symbol: str, element: str, virtue: str,
                 domain1: str, domain2: str, action: str):
        self.name = name
        self.symbol = symbol
        self.element = element
        self.virtue = virtue
        self.domain1 = domain1
        self.domain2 = domain2
        self.action = action

@dataclass
class BaGuaAnalysis:
    """八卦分析结果"""
    dominant_bagua: str              # 主卦
    supporting_bagua: List[str]     # 辅卦
    strengths: List[str]             # 优势
    weaknesses: List[str]           # 劣势
    opportunities: List[str]        # 机会
    threats: List[str]              # 威胁
    recommendations: List[str]       # 建议

@dataclass
class GrowthStrategy:
    """增长战略"""
    strategy_name: str              # 战略名称
    bagua_framework: Dict[str, Any] # 八卦框架
    phases: List[Dict[str, Any]]    # 阶段规划
    metrics: Dict[str, float]       # 关键metrics
    risks: List[str]                # 风险提示
    taoist_wisdom: str              # 道家智慧

class BaGuaGrowthEngine:
    """
    八卦增长解决方案引擎

    核心功能:
    1. 八卦SWOT分析 - 将SWOT与八卦对应
    2. 企业八卦诊断 - 诊断企业的八卦属性
    3. 增长战略八卦化 - 用八卦框架制定战略
    4. 竞争八卦分析 - 分析竞争对手的八卦属性
    5. 道家战略建议 - 融入道德经智慧
    """

    def __init__(self):
        """init八卦增长引擎"""
        # 八卦-商业mapping
        self.bagua_business_map = {
            "乾": {
                "domains": ["战略规划", "领导力", "品牌定位", "资本运营"],
                "strengths": ["战略眼光", "领导力强", "品牌溢价"],
                "development_needs": ["执行力", "团队协作", "灵活性"],
                "recommended_bagua": ["坤(团队)", "巽(传播)", "坎(风控)"]
            },
            "坤": {
                "domains": ["团队建设", "企业文化", "客户关系", "运营管理"],
                "strengths": ["团队稳定", "客户忠诚", "执行力强"],
                "development_needs": ["创新能力", "市场拓展", "品牌影响力"],
                "recommended_bagua": ["乾(战略)", "离(品牌)", "震(创新)"]
            },
            "震": {
                "domains": ["变革创新", "危机应对", "市场突破", "品牌重塑"],
                "strengths": ["创新能力", "危机处理", "市场敏感"],
                "development_needs": ["稳定性", "风险管理", "持续执行"],
                "recommended_bagua": ["艮(稳定)", "坎(风控)", "坤(团队)"]
            },
            "巽": {
                "domains": ["营销传播", "渠道渗透", "品牌传播", "用户get"],
                "strengths": ["传播能力", "渠道布局", "用户运营"],
                "development_needs": ["产品深度", "品牌溢价", "客户留存"],
                "recommended_bagua": ["乾(品牌)", "离(服务)", "坎(留存)"]
            },
            "坎": {
                "domains": ["风险管理", "财务管理", "产品迭代", "合规运营"],
                "strengths": ["风险意识", "财务稳健", "合规性好"],
                "development_needs": ["创新突破", "市场拓展", "品牌建设"],
                "recommended_bagua": ["震(创新)", "乾(战略)", "离(品牌)"]
            },
            "离": {
                "domains": ["客户服务", "品牌公关", "用户体验", "内容运营"],
                "strengths": ["客户口碑", "品牌美誉", "用户体验"],
                "development_needs": ["销售转化", "渠道拓展", "运营效率"],
                "recommended_bagua": ["兑(销售)", "乾(战略)", "巽(渠道)"]
            },
            "艮": {
                "domains": ["核心竞争力", "专业壁垒", "产品质量", "技术研发"],
                "strengths": ["技术壁垒", "产品质量", "专业形象"],
                "development_needs": ["市场敏感", "品牌传播", "团队扩张"],
                "recommended_bagua": ["乾(品牌)", "震(市场)", "坤(团队)"]
            },
            "兑": {
                "domains": ["商务谈判", "合作共赢", "销售转化", "渠道拓展"],
                "strengths": ["谈判能力", "合作关系", "销售转化"],
                "development_needs": ["产品深度", "品牌建设", "团队稳定"],
                "recommended_bagua": ["乾(品牌)", "艮(产品)", "坤(团队)"]
            }
        }

        # 发展阶段八卦配置
        self.phase_bagua_config = {
            "初创期": {
                "primary": "坎",  # 生存第一,风控优先
                "secondary": ["巽", "坤"],
                "focus": "生存,验证,积累",
                "dao_chapter": "第六章 - 谷神不死",
                "dao_quote": "谷神不死,是谓玄牝.玄牝之门,是谓天地根"
            },
            "成长期": {
                "primary": "震",  # 突破扩张
                "secondary": ["乾", "巽"],
                "focus": "扩张,突破,品牌",
                "dao_chapter": "第二十四章 - 企者不立",
                "dao_quote": "企者不立,跨者不行.自见者不明,自是者不彰"
            },
            "成熟期": {
                "primary": "乾",  # 战略引领
                "secondary": ["坤", "艮"],
                "focus": "稳定,创新,传承",
                "dao_chapter": "第九章 - 功遂身退",
                "dao_quote": "功遂身退,天之道"
            },
            "转型期": {
                "primary": "震",  # 变革重生
                "secondary": ["坎", "离"],
                "focus": "变革,转型,重生",
                "dao_chapter": "第四十章 - 反者道之动",
                "dao_quote": "反者道之动,弱者道之用"
            },
            "衰退期": {
                "primary": "巽",  # 渗透转型
                "secondary": ["兑", "坎"],
                "focus": "转型,收缩,转型",
                "dao_chapter": "第七十八章 - 柔弱胜刚强",
                "dao_quote": "天下莫柔弱于水,而攻坚强者莫之能胜"
            }
        }

        # 洛书九宫与商业方位
        self.luoshu_commercial_map = {
            (0, 0): {"position": "东南", "number": 4, "bagua": "巽", "commercial": "渠道布局", "action": "渗透扩张"},
            (0, 1): {"position": "南", "number": 9, "bagua": "离", "commercial": "品牌建设", "action": "提升溢价"},
            (0, 2): {"position": "西南", "number": 2, "bagua": "坤", "commercial": "团队管理", "action": "稳定发展"},
            (1, 0): {"position": "东", "number": 3, "bagua": "震", "commercial": "创新突破", "action": "变革进取"},
            (1, 1): {"position": "中", "number": 5, "bagua": "中宫", "commercial": "战略统筹", "action": "平衡协调"},
            (1, 2): {"position": "西", "number": 7, "bagua": "兑", "commercial": "销售转化", "action": "商务拓展"},
            (2, 0): {"position": "东北", "number": 8, "bagua": "艮", "commercial": "核心竞争力", "action": "壁垒建设"},
            (2, 1): {"position": "北", "number": 1, "bagua": "坎", "commercial": "风险管理", "action": "稳健经营"},
            (2, 2): {"position": "西北", "number": 6, "bagua": "乾", "commercial": "战略规划", "action": "领导decision"}
        }

    def diagnose_enterprise_bagua(self, enterprise_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        企业八卦诊断

        Args:
            enterprise_info: 企业信息

        Returns:
            八卦诊断结果
        """
        business_desc = enterprise_info.get("business_description", "")
        strengths = enterprise_info.get("strengths", [])
        challenges = enterprise_info.get("challenges", [])
        industry = enterprise_info.get("industry", "")
        stage = enterprise_info.get("stage", "成长期")

        bagua_scores = self._analyze_bagua_scores(
            business_desc, strengths, challenges, industry
        )

        dominant_bagua = max(bagua_scores, key=bagua_scores.get)
        sorted_bagua = sorted(bagua_scores.items(), key=lambda x: x[1], reverse=True)
        supporting_bagua = [b[0] for b in sorted_bagua[1:3]]

        dominant_info = self.bagua_business_map.get(dominant_bagua, {})

        return {
            "enterprise_name": enterprise_info.get("name", "企业"),
            "dominant_bagua": {
                "name": dominant_bagua,
                "symbol": getattr(BaGua, dominant_bagua.upper()).value.symbol,
                "meaning": getattr(BaGua, dominant_bagua.upper()).value.virtue,
                "domains": dominant_info.get("domains", []),
                "strengths": dominant_info.get("strengths", []),
                "development_needs": dominant_info.get("development_needs", [])
            },
            "supporting_bagua": supporting_bagua,
            "bagua_scores": bagua_scores,
            "stage_analysis": self._analyze_stage_bagua(stage),
            "industry_bagua": self._get_industry_bagua(industry)
        }

    def _analyze_bagua_scores(self, business_desc: str, strengths: List[str],
                              challenges: List[str], industry: str) -> Dict[str, float]:
        """分析八卦得分"""
        scores = {"乾": 0, "坤": 0, "震": 0, "巽": 0, "坎": 0, "离": 0, "艮": 0, "兑": 0}

        bagua_keywords = {
            "乾": ["战略", "领导", "品牌", "资本", "愿景", "规划", "高端", "溢价"],
            "坤": ["团队", "文化", "客户", "运营", "稳定", "忠诚", "服务", "踏实"],
            "震": ["创新", "变革", "突破", "危机", "改革", "颠覆", "灵活"],
            "巽": ["营销", "传播", "渠道", "渗透", "用户", "流量", "推广", "扩张"],
            "坎": ["风险", "财务", "合规", "安全", "稳健", "控制", "产品", "迭代"],
            "离": ["品牌", "公关", "口碑", "体验", "用户", "服务", "光明", "美誉"],
            "艮": ["技术", "专业", "壁垒", "质量", "研发", "专注", "精品", "深度"],
            "兑": ["销售", "谈判", "合作", "共赢", "商务", "转化", "拓展", "关系"]
        }

        all_text = business_desc + " " + " ".join(strengths) + " " + " ".join(challenges)

        for bagua, keywords in bagua_keywords.items():
            for keyword in keywords:
                if keyword in all_text:
                    scores[bagua] += 1

        industry_bagua = self._get_industry_bagua(industry)
        if industry_bagua in scores:
            scores[industry_bagua] += 2

        max_score = max(scores.values()) if max(scores.values()) > 0 else 1
        for bagua in scores:
            scores[bagua] = round(scores[bagua] / max_score, 2)

        return scores

    def _analyze_stage_bagua(self, stage: str) -> Dict[str, Any]:
        """分析企业发展阶段的八卦配置"""
        stage_config = self.phase_bagua_config.get(stage, self.phase_bagua_config["成长期"])
        return {
            "stage": stage,
            "primary_bagua": stage_config["primary"],
            "secondary_bagua": stage_config["secondary"],
            "focus": stage_config["focus"],
            "dao_chapter": stage_config["dao_chapter"],
            "dao_quote": stage_config["dao_quote"]
        }

    def _get_industry_bagua(self, industry: str) -> Optional[str]:
        """get行业对应的八卦"""
        industry_bagua_map = {
            "科技": "震", "互联网": "巽", "金融": "坎", "房地产": "艮",
            "制造业": "乾", "零售": "兑", "教育": "离", "医疗": "坤",
            "咨询": "乾", "媒体": "离", "娱乐": "震", "旅游": "巽"
        }
        return industry_bagua_map.get(industry)

    def bagua_swot_analysis(self, swot_data: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        八卦SWOT分析

        Args:
            swot_data: SWOT数据

        Returns:
            八卦SWOT分析结果
        """
        swot_bagua_mapping = {
            "strengths": {"bagua": "乾", "description": "刚健进取的优势"},
            "weaknesses": {"bagua": "坤", "description": "柔顺包容的劣势"},
            "opportunities": {"bagua": "震", "description": "震动变革的机会"},
            "threats": {"bagua": "坎", "description": "陷险风险的威胁"}
        }

        swot_analysis = {}
        for dimension, items in swot_data.items():
            mapping = swot_bagua_mapping.get(dimension, {})
            swot_analysis[dimension] = {
                "items": items,
                "bagua": mapping.get("bagua", "乾"),
                "symbol": getattr(BaGua, mapping.get("bagua", "乾").upper()).value.symbol,
                "description": mapping.get("description", "")
            }

        strategies = self._generate_bagua_swot_strategies()

        return {
            "swot_analysis": swot_analysis,
            "strategies": strategies
        }

    def _generate_bagua_swot_strategies(self) -> List[Dict[str, str]]:
        """generate八卦SWOTstrategy"""
        return [
            {"type": "SO", "bagua": "乾+震", "name": "刚健进取,抓住机遇"},
            {"type": "WO", "bagua": "坤+震", "name": "以柔化刚,借势突破"},
            {"type": "ST", "bagua": "乾+坎", "name": "以刚御险,稳健发展"},
            {"type": "WT", "bagua": "坤+坎", "name": "静待时机,蓄势待发"}
        ]

__all__ = ['BaGuaGrowthEngine', 'BaGuaAnalysis', 'GrowthStrategy', 'BaGua']
