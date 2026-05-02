"""
纵横家智慧引擎 V1.0.0
====================
版本: V1.0.0
日期: 2026-04-23
来源: V6.0 第二阶段新增学派集成

整合纵横家（合纵连横）智慧与现代外交博弈理论:

1. 外交谈判策略 - 立场/利益/权力动态
2. 联盟构建策略 - 利益联盟/势力均衡
3. 权力平衡博弈 - 多极博弈/均势理论

核心理论来源:
- 苏秦: 合纵战略（六国联盟抗秦）
- 张仪: 连横战略（秦与诸国个别联合）
- 鬼谷子: 纵横捭阖之术
- 修昔底德: 修昔底德陷阱
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class 博弈类型(Enum):
    """博弈类型"""
    零和博弈 = "zero_sum"
    非零和博弈 = "non_zero_sum"
    协调博弈 = "coordination"
    囚徒困境 = "prisoner"
    斗鸡博弈 = "chicken"


class 联盟策略(Enum):
    """联盟策略"""
    合纵 = "vertical"
    连横 = "horizontal"
    均衡 = "balance"
    追随 = "bandwagon"


class 谈判阶段(Enum):
    """谈判阶段"""
    准备 = "preparation"
    开局 = "opening"
    探索 = "exploration"
    磋商 = "negotiation"
    收尾 = "closing"


class 权力态势(Enum):
    """权力态势"""
    优势 = "dominant"
    均势 = "balanced"
    劣势 = "weak"
    变化中 = "shifting"


@dataclass
class 外交态势:
    """外交态势分析"""
    各方立场: Dict[str, str]
    利益诉求: Dict[str, List[str]]
    权力关系: Dict[str, float]
    潜在联盟: List[Dict]
    风险因素: List[str]


@dataclass
class 谈判策略:
    """谈判策略"""
    推荐策略: str
    谈判路径: List[str]
    筹码分析: Dict[str, Any]
    让步方案: List[Dict]
    备选方案: List[str]


@dataclass
class 联盟方案:
    """联盟构建方案"""
    联盟类型: str
    成员分析: List[Dict]
    共同利益: List[str]
    利益分配: Dict[str, str]
    稳定性评估: str
    风险控制: List[str]


class ZonghengWisdomEngine:
    """
    纵横家智慧引擎
    
    整合古代纵横家智慧与现代地缘政治博弈理论，
    提供外交谈判、联盟构建、权力平衡等战略智慧。
    """
    
    VERSION = "6.2.0"
    
    def __init__(self):
        self.name = "纵横家智慧引擎"
        self.先贤知识库 = self._初始化先贤知识库()
        self.博弈模型库 = self._初始化博弈模型库()
        self.策略工具库 = self._初始化策略工具库()
    
    def _初始化先贤知识库(self) -> Dict:
        """初始化纵横家先贤知识库"""
        return {
            "苏秦": {
                "时代": "战国中期",
                "核心战略": "合纵：六国联合抗秦",
                "方法论": ["游说六国国君", "建立盟约机制", "保持军事协调"],
                "代表成就": "身佩六国相印"
            },
            "张仪": {
                "时代": "战国中期",
                "核心战略": "连横：秦与诸国个别联合",
                "方法论": ["瓦解各国合纵意图", "以土地利益为诱饵", "针对弱点各个击破"],
                "代表成就": "为秦破纵连横"
            },
            "鬼谷子": {
                "时代": "战国初期",
                "核心思想": "纵横捭阖，天下之牖",
                "方法论": ["捭之贵开", "阖之贵密", "揣情摩意", "量权立势"],
                "核心理念": "因事为制，随事而立"
            },
            "范雎": {
                "时代": "战国后期",
                "核心战略": "远交近攻",
                "方法论": ["与远方国家建立友好", "对邻近国家军事行动", "分化潜在联盟"]
            }
        }
    
    def _初始化博弈模型库(self) -> Dict:
        """初始化博弈论模型库"""
        return {
            "修昔底德陷阱": {
                "定义": "新兴大国必然挑战现有大国",
                "应对策略": ["建立危机管理", "寻求共同利益", "管控分歧"]
            },
            "囚徒困境": {
                "启示": "单次博弈不利于合作，多次博弈促进合作",
                "破局": ["增加背叛成本", "建立互惠机制"]
            },
            "猎鹿博弈": {
                "启示": "合作需要信任和承诺",
                "应用": "联盟合作中的风险分担"
            }
        }
    
    def _初始化策略工具库(self) -> Dict:
        """初始化策略工具库"""
        return {
            "谈判策略": {
                "硬球策略": "强硬立场施压",
                "软球策略": "友好协商共赢",
                "原则性谈判": "关注利益而非立场"
            },
            "联盟策略": {
                "三角制衡": "利用第三方力量",
                "势力范围": "划分势力避免冲突",
                "威慑战略": "展示实力遏制冒险"
            }
        }
    
    def analyze_diplomatic_situation(
        self,
        stakeholders: List[Dict],
        context: Dict = None
    ) -> 外交态势:
        """分析外交态势"""
        各方立场 = {}
        利益诉求 = {}
        权力关系 = {}
        
        for party in stakeholders:
            name = party.get("name", "未知")
            各方立场[name] = party.get("position", "待明确")
            利益诉求[name] = party.get("interests", [])
            权力关系[name] = party.get("power", 0.5)
        
        潜在联盟 = self._识别潜在联盟(stakeholders)
        风险因素 = self._识别外交风险(stakeholders)
        
        return 外交态势(
            各方立场=各方立场,
            利益诉求=利益诉求,
            权力关系=权力关系,
            潜在联盟=潜在联盟,
            风险因素=风险因素
        )
    
    def _识别潜在联盟(self, stakeholders: List[Dict]) -> List[Dict]:
        """识别潜在联盟"""
        联盟候选 = []
        all_interests = {}
        for party in stakeholders:
            for interest in party.get("interests", []):
                if interest not in all_interests:
                    all_interests[interest] = []
                all_interests[interest].append(party.get("name"))
        
        for interest, parties in all_interests.items():
            if len(parties) >= 2:
                联盟候选.append({
                    "基础": interest,
                    "成员": parties,
                    "类型": "利益联盟"
                })
        
        return 联盟候选[:5]
    
    def _识别外交风险(self, stakeholders: List[Dict]) -> List[str]:
        """识别外交风险"""
        风险 = []
        powers = [p.get("power", 0.5) for p in stakeholders]
        if max(powers) - min(powers) > 0.7:
            风险.append("存在权力极度不平衡")
        风险.append("各方核心利益可能存在冲突")
        风险.append("历史恩怨可能影响合作")
        return 风险
    
    def design_negotiation_strategy(
        self,
        negotiation_data: Dict,
        my_position: Dict = None
    ) -> 谈判策略:
        """设计谈判策略"""
        谈判主题 = negotiation_data.get("topic", "待定")
        参与方 = negotiation_data.get("parties", [])
        
        推荐策略 = self._推荐谈判策略(参与方, my_position)
        谈判路径 = self._设计谈判路径(谈判主题)
        筹码分析 = self._分析谈判筹码(参与方, my_position)
        让步方案 = self._设计让步方案(谈判主题, my_position)
        备选方案 = ["寻求第三方调解", "暂时搁置分歧", "扩大谈判范围"]
        
        return 谈判策略(
            推荐策略=推荐策略,
            谈判路径=谈判路径,
            筹码分析=筹码分析,
            让步方案=让步方案,
            备选方案=备选方案
        )
    
    def _推荐谈判策略(self, parties: List, my_position: Dict) -> str:
        """推荐谈判策略"""
        我方实力 = my_position.get("strength", 0.5) if my_position else 0.5
        if 我方实力 > 0.7:
            return "优势策略：利用实力争取更多利益，避免过度施压"
        elif 我方实力 < 0.3:
            return "劣势策略：寻求联盟支持，核心坚守非核心灵活"
        return "均势策略：原则性谈判，追求互利共赢"
    
    def _设计谈判路径(self, topic: str) -> List[str]:
        """设计谈判路径"""
        return [
            "第一步：建立信任和沟通渠道",
            "第二步：明确各方核心利益",
            "第三步：寻找共同点和交易空间",
            "第四步：就具体议题磋商",
            "第五步：达成原则性协议",
            "第六步：细节谈判和文本确认",
            "第七步：签署协议和后续跟进"
        ]
    
    def _分析谈判筹码(self, parties: List, my_position: Dict) -> Dict:
        """分析谈判筹码"""
        我方筹码 = my_position.get("leverage", []) if my_position else []
        return {
            "我方筹码": 我方筹码 or ["承诺和信用", "让步能力", "替代方案"],
            "对方筹码": ["资源和影响力", "替代选择", "内部压力"],
            "共同筹码": ["合作利益", "和平稳定", "长远关系"]
        }
    
    def _设计让步方案(self, topic: str, my_position: Dict) -> List[Dict]:
        """设计让步方案"""
        我方底线 = my_position.get("bottom_line", {}) if my_position else {}
        return [{
            "议题": topic,
            "理想结果": 我方底线.get("理想", "最大化利益"),
            "可接受底线": 我方底线.get("底线", "核心利益不受损"),
            "让步空间": ["非核心议题可让步", "条件性让步", "渐进式让步"]
        }]
    
    def design_alliance_strategy(
        self,
        objective: str,
        current_allies: List[str] = None,
        potential_partners: List[Dict] = None
    ) -> 联盟方案:
        """设计联盟策略"""
        if current_allies is None:
            current_allies = []
        if potential_partners is None:
            potential_partners = []
        
        联盟类型 = self._判定联盟类型(objective)
        
        成员分析 = []
        for ally in current_allies:
            成员分析.append({"名称": ally, "类型": "现有盟友", "稳定性": "高"})
        for partner in potential_partners:
            成员分析.append({
                "名称": partner.get("name", "未知"),
                "类型": "潜在伙伴",
                "稳定性": partner.get("stability", "待评估")
            })
        
        共同利益 = self._识别联盟共同利益(objective, current_allies, potential_partners)
        利益分配 = {m["名称"]: "按贡献比例分配" for m in 成员分析}
        稳定性评估 = self._评估联盟稳定性(成员分析)
        风险控制 = ["建立沟通机制", "明确权义关系", "设立争议解决"]
        
        return 联盟方案(
            联盟类型=联盟类型,
            成员分析=成员分析,
            共同利益=共同利益,
            利益分配=利益分配,
            稳定性评估=稳定性评估,
            风险控制=风险控制
        )
    
    def _判定联盟类型(self, objective: str) -> str:
        """判定联盟类型"""
        if "对抗" in objective:
            return 联盟策略.合纵.value
        elif "合作" in objective:
            return 联盟策略.均衡.value
        return 联盟策略.连横.value
    
    def _识别联盟共同利益(self, objective: str, allies: List, partners: List) -> List[str]:
        """识别联盟共同利益"""
        return [f"实现{objective}", "维护共同利益", "应对共同挑战"]
    
    def _评估联盟稳定性(self, members: List[Dict]) -> str:
        """评估联盟稳定性"""
        if len(members) <= 2:
            return "双边联盟相对稳定"
        elif len(members) <= 5:
            return "多边联盟稳定性中等"
        return "大型联盟协调成本高"
    
    def analyze_power_balance(
        self,
        power_centers: List[Dict],
        strategic_context: Dict = None
    ) -> Dict:
        """权力平衡分析"""
        if not power_centers:
            return {"态势": "数据不足"}
        
        max_power = max(p.get("power", 0) for p in power_centers)
        min_power = min(p.get("power", 0) for p in power_centers)
        gap = max_power - min_power
        
        if gap > 0.5:
            态势 = "优势"
        elif gap < 0.2:
            态势 = "均势"
        else:
            态势 = "变化中"
        
        return {
            "权力分布": {p.get("name", "未知"): f"{p.get('power', 0):.0%}" for p in power_centers},
            "态势判定": 态势,
            "策略建议": self._生成权力博弈策略(态势, power_centers)
        }
    
    def _生成权力博弈策略(self, 态势: str, centers: List[Dict]) -> List[str]:
        """生成权力博弈策略"""
        if 态势 == "优势":
            return ["保持战略克制", "利用优势争取有利条款", "建立规则固化优势"]
        elif 态势 == "劣势":
            return ["寻求联盟支持", "核心利益坚守", "积蓄力量等待时机"]
        return ["保持灵活性", "促进各方对话", "建立信任措施"]
    
    def apply_zongheng_wisdom(
        self,
        situation: str,
        parties: List[Dict],
        my_position: Dict = None
    ) -> Dict:
        """综合运用纵横家智慧"""
        鬼谷分析 = self._鬼谷子分析(situation, parties)
        外交态势 = self.analyze_diplomatic_situation(parties)
        谈判策略 = self.design_negotiation_strategy(
            {"topic": situation, "parties": parties}, my_position
        )
        联盟策略 = self.design_alliance_strategy(
            situation,
            my_position.get("allies", []) if my_position else [],
            parties
        )
        
        return {
            "局势判断": 鬼谷分析,
            "外交态势": {
                "各方立场": 外交态势.各方立场,
                "权力关系": 外交态势.权力关系,
                "潜在联盟": 外交态势.潜在联盟
            },
            "谈判策略": {"推荐": 谈判策略.推荐策略, "路径": 谈判策略.谈判路径},
            "联盟策略": {"类型": 联盟策略.联盟类型, "成员": [m["名称"] for m in 联盟策略.成员分析]},
            "历史借鉴": ["战国合纵连横", "苏秦张仪博弈", "三角制衡智慧"],
            "综合建议": ["纵横捭阖因势利导", "原则谈判互利共赢", "联盟稳定风险控制"],
            "置信度": 0.80
        }
    
    def _鬼谷子分析(self, situation: str, parties: List[Dict]) -> Dict:
        """鬼谷子式局势分析"""
        return {
            "捭之时机": "当前是否适合开启谈判？",
            "阖之策略": "哪些信息应保密？",
            "揣情要诀": "各方真实意图是什么？",
            "量权要点": "各方实力对比如何？"
        }


# 全局单例与便捷函数
_engine_instance = None

def get_zongheng_engine() -> ZonghengWisdomEngine:
    """获取纵横家引擎单例"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = ZonghengWisdomEngine()
    return _engine_instance


def quick_diplomatic_analysis(stakeholders: List[Dict]) -> Dict:
    """快速外交态势分析"""
    result = get_zongheng_engine().analyze_diplomatic_situation(stakeholders)
    return {"各方立场": result.各方立场, "权力关系": result.权力关系, "潜在联盟": result.潜在联盟}


def quick_negotiation_strategy(negotiation_data: Dict, my_position: Dict = None) -> Dict:
    """快速谈判策略设计"""
    result = get_zongheng_engine().design_negotiation_strategy(negotiation_data, my_position)
    return {"推荐策略": result.推荐策略, "谈判路径": result.谈判路径}


def zongheng_wisdom_application(situation: str, parties: List[Dict], my_position: Dict = None) -> Dict:
    """纵横家智慧综合运用"""
    return get_zongheng_engine().apply_zongheng_wisdom(situation, parties, my_position)


__all__ = [
    'ZonghengWisdomEngine', 'get_zongheng_engine',
    'quick_diplomatic_analysis', 'quick_negotiation_strategy',
    'zongheng_wisdom_application',
    '博弈类型', '联盟策略', '谈判阶段', '权力态势',
]
