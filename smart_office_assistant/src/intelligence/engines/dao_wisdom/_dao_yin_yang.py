"""
__all__ = [
    'analyze_bagua',
    'analyze_yin_yang',
    'apply_to_growth_strategy',
    'dao_init',
    'evaluate_with_taiji',
    'get_daojing_wisdom',
    'get_luoshu_guidance',
    'make_dao_decision',
]

道家智慧业务逻辑 - 第一组：阴阳/道德经/太极/决策
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from ._dao_enums import (
    DaoDeJingCore, BaGua, BaGuaRelation,
    ZhuangziCore, DaoManagement, DaoHealth,
    YinYangPrinciple, LuoShu,
    DaoDecision, TaoistPersona,
)

def dao_init(self) -> None:
    """init道家智慧核心"""
    self.daojing_core = {e.name: e.value for e in DaoDeJingCore}
    self.bagua_map = {e.value[0]: e.value for e in BaGua}
    self.yinyang_attributes = {
        "yang": ["刚", "强", "动", "进", "开", "热", "明", "健", "创造", "主导"],
        "yin": ["柔", "弱", "静", "退", "闭", "寒", "暗", "顺", "包容", "守成"]
    }
    self.daojing_by_theme = {
        "自然无为": [
            DaoDeJingCore.CHAPTER_25, DaoDeJingCore.CHAPTER_5,
            DaoDeJingCore.CHAPTER_17, DaoDeJingCore.CHAPTER_60,
        ],
        "柔弱胜刚强": [
            DaoDeJingCore.CHAPTER_40, DaoDeJingCore.CHAPTER_43,
            DaoDeJingCore.CHAPTER_76, DaoDeJingCore.CHAPTER_78,
        ],
        "知足不争": [
            DaoDeJingCore.CHAPTER_46, DaoDeJingCore.CHAPTER_44,
            DaoDeJingCore.CHAPTER_9, DaoDeJingCore.CHAPTER_81,
        ],
        "辩证思维": [
            DaoDeJingCore.CHAPTER_2, DaoDeJingCore.CHAPTER_58,
            DaoDeJingCore.CHAPTER_36, DaoDeJingCore.CHAPTER_22,
        ],
        "修身养性": [
            DaoDeJingCore.CHAPTER_8, DaoDeJingCore.CHAPTER_16,
            DaoDeJingCore.CHAPTER_12, DaoDeJingCore.CHAPTER_48,
        ],
        "战略智慧": [
            DaoDeJingCore.CHAPTER_57, DaoDeJingCore.CHAPTER_30,
            DaoDeJingCore.CHAPTER_69, DaoDeJingCore.CHAPTER_67,
        ],
        "德经递降": [
            DaoDeJingCore.CHAPTER_38, DaoDeJingCore.CHAPTER_39,
            DaoDeJingCore.CHAPTER_41, DaoDeJingCore.CHAPTER_45,
        ],
        "认识论": [
            DaoDeJingCore.CHAPTER_47, DaoDeJingCore.CHAPTER_48,
            DaoDeJingCore.CHAPTER_1, DaoDeJingCore.CHAPTER_14,
        ],
        "处世哲学": [
            DaoDeJingCore.CHAPTER_13, DaoDeJingCore.CHAPTER_49,
            DaoDeJingCore.CHAPTER_63, DaoDeJingCore.CHAPTER_64,
        ],
        "军事外交": [
            DaoDeJingCore.CHAPTER_30, DaoDeJingCore.CHAPTER_31,
            DaoDeJingCore.CHAPTER_68, DaoDeJingCore.CHAPTER_69,
        ],
    }
    self.zhuangzi_by_theme = {
        "自由逍遥": [ZhuangziCore.XIAO_YAO_YOU, ZhuangziCore.QI_WU_LUN],
        "处世智慧": [ZhuangziCore.REN_JIAN_SHI, ZhuangziCore.YANG_SHENG_ZHU],
        "生命哲学": [ZhuangziCore.DA_ZONG_SHI, ZhuangziCore.DE_CHONG_FU],
        "认知突破": [ZhuangziCore.QI_SHUI_LUN, ZhuangziCore.QI_WU_LUN],
        "无为管理": [ZhuangziCore.YING_DI_WANG],
    }
    self.management_scenarios = {
        "团队管理": DaoManagement.WU_WEI,
        "战略规划": DaoManagement.WEI_YU_WEI_SHI,
        "领导力": DaoManagement.SHANG_SHAN_RUO_SHUI,
        "组织变革": DaoManagement.TUO_QI_RUI,
        "大型组织": DaoManagement.ZHI_DA_GUO,
        "企业文化": DaoManagement.CI_JIAN_BU_GAN,
        "远程管理": DaoManagement.BU_XING_ER_ZHI,
    }

def analyze_yin_yang(self, situation: str, factors: Dict[str, Any]) -> Dict[str, Any]:
    """阴阳分析"""
    yang_count = 0
    yin_count = 0
    yang_factors = []
    yin_factors = []

    yang_keywords = ["强", "动", "进", "攻", "快", "大", "刚", "显", "明", "阳", "竞争", "扩张"]
    yin_keywords = ["弱", "静", "退", "守", "慢", "小", "柔", "隐", "暗", "阴", "合作", "收缩"]

    for factor, weight in factors.items():
        factor_lower = factor.lower()
        if any(kw in factor_lower for kw in yang_keywords):
            yang_count += weight
            yang_factors.append(factor)
        elif any(kw in factor_lower for kw in yin_keywords):
            yin_count += weight
            yin_factors.append(factor)

    total = yang_count + yin_count
    yang_ratio = yang_count / total if total > 0 else 0.5

    if yang_ratio > 0.7:
        state = "偏阳过盛"
        advice = "宜静不宜动,宜守不宜攻,遵循'柔弱胜刚强'的智慧"
        dao_chapter = DaoDeJingCore.CHAPTER_40
    elif yang_ratio < 0.3:
        state = "偏阴过盛"
        advice = "宜动不宜静,宜进不宜退,需要激发阳刚之气"
        dao_chapter = DaoDeJingCore.CHAPTER_76
    else:
        state = "阴阳平衡"
        advice = "宜顺势而为,保持中道"
        dao_chapter = DaoDeJingCore.CHAPTER_22

    return {
        "yang_ratio": yang_ratio,
        "yin_ratio": 1 - yang_ratio,
        "state": state,
        "yang_factors": yang_factors,
        "yin_factors": yin_factors,
        "advice": advice,
        "dao_chapter": dao_chapter.value[1] + " - " + dao_chapter.value[2],
        "yin_yang_principle": _get_yin_yang_principle(yang_ratio),
    }

def _get_yin_yang_principle(yang_ratio: float) -> str:
    """get适用的阴阳原则"""
    if yang_ratio > 0.7:
        return YinYangPrinciple.XIAO_CHANG.value[1]
    elif yang_ratio < 0.3:
        return YinYangPrinciple.XIAO_CHANG.value[1]
    elif yang_ratio == 0.5:
        return YinYangPrinciple.HU_GEN.value[1]
    else:
        return YinYangPrinciple.DUAN_ZHI.value[1]

def analyze_bagua(self, domain: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """八卦分析"""
    domain_bagua_map = {
        "领导力": [BaGua.QIAN, BaGua.KUN],
        "创新": [BaGua.LI, BaGua.ZHEN],
        "市场": [BaGua.KAN, BaGua.XUN],
        "团队": [BaGua.GEN, BaGua.DUI],
        "战略": [BaGua.QIAN, BaGua.LI],
        "执行": [BaGua.ZHEN, BaGua.KAN],
        "品牌": [BaGua.LI, BaGua.DUI],
        "渠道": [BaGua.XUN, BaGua.KUN],
    }

    primary_bagua = domain_bagua_map.get(domain, [BaGua.QIAN])[0]
    secondary_bagua = domain_bagua_map.get(domain, [BaGua.KUN])[1] if len(domain_bagua_map.get(domain, [])) > 1 else None

    bagua_advice = _generate_bagua_advice(primary_bagua, context)

    return {
        "primary_bagua": {
            "name": primary_bagua.name,
            "symbol": primary_bagua.symbol,
            "meaning": primary_bagua.meaning,
            "virtue": primary_bagua.virtue,
            "element": primary_bagua.element,
        },
        "secondary_bagua": {
            "name": secondary_bagua.name,
            "symbol": secondary_bagua.symbol,
            "meaning": secondary_bagua.meaning,
            "virtue": secondary_bagua.virtue,
            "element": secondary_bagua.element,
        } if secondary_bagua else None,
        "advice": bagua_advice,
        "trigrams_hexagram": _generate_hexagram(primary_bagua, secondary_bagua),
    }

def _generate_bagua_advice(bagua: BaGua, context: Dict[str, Any]) -> List[str]:
    """generate八卦建议"""
    advice_map = {
        BaGua.QIAN: ["刚健进取,自强不息", "创造主导,把握先机", "坚守正道,不偏不倚"],
        BaGua.KUN: ["柔顺包容,厚德载物", "雌柔守静,以退为进", "承载承载,顺势而为"],
        BaGua.ZHEN: ["震动action,把握时机", "果断出击,雷厉风行", "破旧立新,勇于变革"],
        BaGua.XUN: ["顺从渗透,润物无声", "渐进入化,耐心布局", "风化天下,无孔不入"],
        BaGua.KAN: ["危险警示,谨慎行事", "以柔克刚,险中求胜", "智慧内敛,深谋远虑"],
        BaGua.LI: ["光明照临,正大光明", "文采飞扬,文化赋能", "美丽外在,智慧内在"],
        BaGua.GEN: ["静止稳定,坚守原则", "稳重如山,不轻举妄动", "适时而止,见好就收"],
        BaGua.DUI: ["喜悦和谐,以言服人", "柔性沟通,愉悦协作", "口才外交,谈判制胜"],
    }
    return advice_map.get(bagua, ["因地制宜,随机应变"])

def _generate_hexagram(upper: BaGua, lower: BaGua) -> str:
    """generate卦象"""
    return f"{lower.symbol}{upper.symbol} ({lower.name}上{upper.name}下)"

def get_daojing_wisdom(self, theme: str, situation: Optional[str] = None) -> Dict[str, Any]:
    """get道德经智慧"""
    chapters = self.daojing_by_theme.get(theme, self.daojing_by_theme["辩证思维"])

    wisdom_list = []
    for chapter in chapters:
        wisdom_list.append({
            "chapter": chapter.value[0],
            "quote": chapter.value[1],
            "interpretation": chapter.value[2],
            "application": _apply_to_situation(chapter, situation) if situation else chapter.value[2]
        })

    return {
        "theme": theme,
        "wisdom_count": len(wisdom_list),
        "wisdom_list": wisdom_list,
        "core_insight": _generate_core_insight(theme, wisdom_list)
    }

def _apply_to_situation(chapter: DaoDeJingCore, situation: str) -> str:
    """将道德经智慧应用到具体情境"""
    interpretation = chapter.value[2]
    if "竞争" in situation or "挑战" in situation:
        if "柔" in interpretation or "弱" in interpretation:
            return f"面对{situation},应借鉴'{chapter.value[1]}'的智慧,以柔克刚"
    if "困境" in situation or "危机" in situation:
        return f"面对{situation},应体悟'{chapter.value[1]}'的深意,转危为机"
    return interpretation

def _generate_core_insight(theme: str, wisdom_list: List[Dict]) -> str:
    """generate核心洞见"""
    theme_insights = {
        "自然无为": "遵循事物发展的自然规律,不过度干预,顺势而为.",
        "柔弱胜刚强": "最柔弱的往往最有力量,水滴石穿,绳锯木断.",
        "知足不争": "知足者富,不争者无敌,为而不争才是最高境界.",
        "辩证思维": "祸福相依,美丑相生,事物在一定条件下相互转化.",
        "修身养性": "致虚极,守静笃,回归本心,方能洞察大道.",
        "战略智慧": "以正治国,以奇用兵,正奇相生,变化无穷.",
    }
    return theme_insights.get(theme, "道法自然,顺势而为.")

def evaluate_with_taiji(self, yin_score: float, yang_score: float) -> Dict[str, Any]:
    """太极decision评估"""
    total = yin_score + yang_score
    yin_ratio = yin_score / total if total > 0 else 0.5
    yang_ratio = yang_score / total if total > 0 else 0.5

    balance_score = 1 - abs(yin_ratio - yang_ratio)
    balance_score = round(balance_score, 3)

    if balance_score > 0.8:
        state = "太极平衡"
        description = "阴阳和谐,最佳decision时机"
        recommendation = "可以全面推进,阴阳互补,相得益彰"
    elif yin_ratio > yang_ratio:
        state = "偏阴"
        description = "阴性力量占优,宜静不宜动"
        recommendation = "暂时观望,积蓄力量,等待时机"
    else:
        state = "偏阳"
        description = "阳性力量占优,宜进不宜退"
        recommendation = "主动出击,积极进取,趁势而上"

    rotation = "clockwise" if yang_ratio > yin_ratio else "counter-clockwise"

    return {
        "yin_score": yin_score,
        "yang_score": yang_score,
        "yin_ratio": round(yin_ratio, 3),
        "yang_ratio": round(yang_ratio, 3),
        "balance_score": balance_score,
        "state": state,
        "description": description,
        "recommendation": recommendation,
        "taiji_rotation": rotation,
        "best_direction": _get_best_direction(yin_ratio, yang_ratio)
    }

def _get_best_direction(yin_ratio: float, yang_ratio: float) -> str:
    """get最佳方向"""
    if yin_ratio > yang_ratio:
        return "东南(巽)- 进入,渗透方向"
    elif yang_ratio > yin_ratio:
        return "西北(乾)- 刚健,进取方向"
    else:
        return "中央(中宫)- 调和,平衡方向"

def make_dao_decision(self, situation: str, factors: Dict[str, Any],
                      domain: Optional[str] = None) -> DaoDecision:
    """道家synthesize_decision"""
    decision_id = f"dao_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    yin_yang_result = self.analyze_yin_yang(situation, factors)
    bagua_result = self.analyze_bagua(domain or "战略", {}) if domain else None

    if "竞争" in situation or "对抗" in situation:
        theme = "柔弱胜刚强"
    elif "困境" in situation or "危机" in situation:
        theme = "辩证思维"
    elif "长期" in situation or "规划" in situation:
        theme = "自然无为"
    else:
        theme = "修身养性"

    dao_wisdom = self.get_daojing_wisdom(theme, situation)
    recommended_action = _generate_action(yin_yang_result, bagua_result, dao_wisdom)

    return DaoDecision(
        decision_id=decision_id,
        situation=situation,
        yin_yang_analysis=yin_yang_result,
        bagua_analysis=bagua_result or {},
        dao_advice=[w["quote"] for w in dao_wisdom["wisdom_list"]],
        recommended_action=recommended_action,
        wisdom_source=f"道德经-{theme}",
        balance_score=yin_yang_result["yang_ratio"],
        transformation_potential=_assess_transformation(yin_yang_result)
    )

def _generate_action(yin_yang: Dict, bagua: Optional[Dict], dao_wisdom: Dict) -> str:
    """generate推荐action"""
    actions = []

    if yin_yang["state"] == "偏阳过盛":
        actions.append("宜静守,借鉴'致虚极,守静笃'的智慧")
    elif yin_yang["state"] == "偏阴过盛":
        actions.append("宜进取,秉持'天行健,君子以自强不息'的精神")
    else:
        actions.append("阴阳平衡,可顺势而为")

    if bagua:
        actions.append(f"主卦{bagua['primary_bagua']['name']}:{bagua['advice'][0]}")

    actions.append(f"核心洞见:{dao_wisdom['core_insight']}")

    return ";".join(actions)

def _assess_transformation(yin_yang: Dict) -> str:
    """评估转化潜力"""
    ratio = yin_yang["yang_ratio"]
    if 0.3 <= ratio <= 0.7:
        return "高 - 阴阳相对平衡,转化潜力大"
    elif ratio < 0.2 or ratio > 0.8:
        return "临界 - 即将发生质变转化"
    else:
        return "中 - 稳定中酝酿变化"

def get_luoshu_guidance(self, position: str) -> Dict[str, Any]:
    """洛书九宫方位指导"""
    position_map = {
        "东南": {"row": 0, "col": 0, "number": 4, "bagua": "巽", "virtue": "进入"},
        "南": {"row": 0, "col": 1, "number": 9, "bagua": "离", "virtue": "光明"},
        "西南": {"row": 0, "col": 2, "number": 2, "bagua": "坤", "virtue": "柔顺"},
        "东": {"row": 1, "col": 0, "number": 3, "bagua": "震", "virtue": "震动"},
        "中": {"row": 1, "col": 1, "number": 5, "bagua": "中宫", "virtue": "调和"},
        "西": {"row": 1, "col": 2, "number": 7, "bagua": "兑", "virtue": "喜悦"},
        "东北": {"row": 2, "col": 0, "number": 8, "bagua": "艮", "virtue": "静止"},
        "北": {"row": 2, "col": 1, "number": 1, "bagua": "坎", "virtue": "危险"},
        "西北": {"row": 2, "col": 2, "number": 6, "bagua": "乾", "virtue": "刚健"},
    }

    info = position_map.get(position, position_map["中"])

    return {
        "position": position,
        "number": info["number"],
        "bagua": info["bagua"],
        "virtue": info["virtue"],
        "guidance": _get_position_guidance(info),
        "lo_shu": LuoShu.GRID,
    }

def _get_position_guidance(info: Dict) -> str:
    """get方位指导"""
    virtue_guidance = {
        "进入": "适合布局渗透,长远规划",
        "光明": "适合品牌建设,文化传播",
        "柔顺": "适合合作协商,关系维护",
        "震动": "适合变革创新,突破困局",
        "调和": "适合统筹协调,平衡各方",
        "喜悦": "适合对外沟通,谈判签约",
        "静止": "适合稳重守成,坚守原则",
        "危险": "需要谨慎行事,防范风险",
        "刚健": "适合战略decision,领导指挥",
    }
    return virtue_guidance.get(info["virtue"], "因地制宜")

def apply_to_growth_strategy(self, growth_phase: str, current_state: Dict) -> Dict[str, Any]:
    """道家增长战略应用"""
    phase_strategy = {
        "初创期": {
            "dao_chapter": DaoDeJingCore.CHAPTER_40,
            "strategy": "柔弱胜刚强",
            "advice": "新事物如同婴儿,需要循序渐进,不可急于求成.'天下之至柔,驰骋天下之至坚'",
            "action": "深耕细分市场,以柔克刚,稳扎稳打"
        },
        "成长期": {
            "dao_chapter": DaoDeJingCore.CHAPTER_67,
            "strategy": "三宝之道",
            "advice": "慈故能勇,俭故能广,不敢为天下先故能成器长",
            "action": "慈爱客户,勤俭经营,谦退不争"
        },
        "成熟期": {
            "dao_chapter": DaoDeJingCore.CHAPTER_9,
            "strategy": "功遂身退",
            "advice": "物壮则老,是谓不道,不道早已.成功时要知道退让",
            "action": "转型升级,寻找新的增长点"
        },
        "转型期": {
            "dao_chapter": DaoDeJingCore.CHAPTER_58,
            "strategy": "祸福相依",
            "advice": "祸兮,福之所倚;福兮,祸之所伏.危机中蕴含机遇",
            "action": "化危为机,逆向思维,寻找新的可能性"
        },
        "衰退期": {
            "dao_chapter": DaoDeJingCore.CHAPTER_76,
            "strategy": "柔弱生刚强",
            "advice": "人之生也柔弱,其死也坚强.柔软是生命力的象征",
            "action": "创新求变,保持灵活,等待转机"
        },
    }

    strategy = phase_strategy.get(growth_phase, phase_strategy["成长期"])

    return {
        "phase": growth_phase,
        "strategy_name": strategy["strategy"],
        "dao_chapter": f"{strategy['dao_chapter'].value[0]}:{strategy['dao_chapter'].value[1]}",
        "advice": strategy["advice"],
        "recommended_action": strategy["action"],
        "yin_yang_balance": _get_phase_yin_yang(growth_phase),
    }

def _get_phase_yin_yang(phase: str) -> str:
    """get阶段阴阳属性"""
    phase_yang = {
        "初创期": "阴盛(柔弱,潜藏)",
        "成长期": "阴阳平衡",
        "成熟期": "阳盛(刚强,外显)",
        "转型期": "阴阳转化",
        "衰退期": "阴盛(收敛,沉寂)",
    }
    return phase_yang.get(phase, "阴阳平衡")
