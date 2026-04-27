"""
__all__ = [
    'comprehensive_dao_analysis',
]

道家智慧业务逻辑 - 第三组：综合分析
comprehensive_dao_analysis + 主题匹配 + 智慧综合
"""

from typing import Dict, List, Any

def comprehensive_dao_analysis(self, question: str, context: Dict = None) -> Dict[str, Any]:
    """道家synthesize分析(博士级)v2.0"""
    result = {"question": question, "version": "v2.0 博士级"}

    factors = context.get("factors", {}) if context else {}
    yin_yang = self.analyze_yin_yang(question, factors)
    result["yin_yang_analysis"] = yin_yang

    theme = _match_theme(question)
    result["daodejing_wisdom"] = self.get_daojing_wisdom(theme, question)

    zhuangzi_theme = _match_zhuangzi_theme(question)
    result["zhuangzi_wisdom"] = self.get_zhuangzi_wisdom(zhuangzi_theme)

    result["de_jing_level"] = self.analyze_de_jing_hierarchy(question)

    result["synthesis"] = _synthesize_dao_advice(result)
    return result

def _match_theme(question: str) -> str:
    """根据问题匹配道德经主题"""
    theme_keywords = {
        "自然无为": ["自然", "规律", "不要干预", "顺其自然", "趋势"],
        "柔弱胜刚强": ["竞争", "对抗", "力量", "强大", "以柔克刚"],
        "知足不争": ["满足", "够了", "不争", "放下", "退出"],
        "辩证思维": ["转化", "变化", "反例", "相对", "矛盾"],
        "修身养性": ["修养", "内心", "平静", "焦虑", "修炼"],
        "战略智慧": ["管理", "战略", "领导", "组织", "三宝"],
        "德经递降": ["形式", "制度", "礼仪", "道德", "规范"],
        "认识论": ["认知", "理解", "知识", "学习", "本质"],
        "处世哲学": ["处困", "人际", "积累", "小事", "防微杜渐"],
        "军事外交": ["战争", "对手", "谈判", "冲突", "退让"],
    }
    for theme, keywords in theme_keywords.items():
        if any(kw in question for kw in keywords):
            return theme
    return "辩证思维"

def _match_zhuangzi_theme(question: str) -> str:
    """根据问题匹配庄子主题"""
    if any(kw in question for kw in ["自由", "束缚", "限制", "框架"]):
        return "自由逍遥"
    if any(kw in question for kw in ["处理", "应对", "关系", "社会"]):
        return "处世智慧"
    if any(kw in question for kw in ["生命", "死亡", "意义", "存在"]):
        return "生命哲学"
    if any(kw in question for kw in ["认知", "偏见", "局限", "视野"]):
        return "认知突破"
    if any(kw in question for kw in ["管理", "组织", "制度"]):
        return "无为管理"
    return "自由逍遥"

def _synthesize_dao_advice(analysis: Dict) -> str:
    """synthesize道家智慧generate建议"""
    parts = []
    yin_yang = analysis["yin_yang_analysis"]
    if yin_yang["state"] == "偏阳过盛":
        parts.append("当前阳气过盛,宜'致虚极守静笃',收敛锋芒,以退为进")
    elif yin_yang["state"] == "偏阴过盛":
        parts.append("当前阴气偏盛,宜激发阳气,'天下之至柔,驰骋天下之至坚'")
    else:
        parts.append("阴阳相对平衡,可顺势而为,保持'清静为天下正'")

    ddj = analysis["daodejing_wisdom"]
    parts.append(f"道德经洞见:{ddj['core_insight']}")

    zz = analysis["zhuangzi_wisdom"]
    parts.append(f"庄子视角:{zz['core_insight']}")

    dejing = analysis["de_jing_level"]
    parts.append(f"德经层次:当前处于'{dejing['current_level']}'--{dejing['advice']}")

    return "\n".join(parts)
