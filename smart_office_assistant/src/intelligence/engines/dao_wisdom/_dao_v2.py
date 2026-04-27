"""
__all__ = [
    'analyze_de_jing_hierarchy',
    'analyze_sixiang',
    'analyze_wuxing_cycle',
    'analyze_xian_tian_hou_tian',
    'get_dao_health_guide',
    'get_dao_management_advice',
    'get_dao_three_realms',
    'get_zhuangzi_wisdom',
]

道家智慧业务逻辑 - 第二组：v2.0 增强方法
庄子/德经/五行/四象/管理/养生/三重境界/先后天八卦
"""

from typing import Dict, List, Any

from ._dao_enums import (
    ZhuangziCore, DeJingHierarchy,
    WuXing, WuXingCycle, SiXiang,
    DaoManagement, DaoHealth, DaoThreeRealms,
    BaGua,
)

def get_zhuangzi_wisdom(self, theme: str) -> Dict[str, Any]:
    """get庄子哲学智慧 v2.0"""
    chapters = self.zhuangzi_by_theme.get(theme, self.zhuangzi_by_theme["自由逍遥"])
    wisdom_list = []
    for ch in chapters:
        wisdom_list.append({
            "title": ch.title,
            "quote": ch.quote,
            "interpretation": ch.interpretation,
        })
    return {
        "theme": theme,
        "source": "庄子哲学",
        "wisdom_list": wisdom_list,
        "core_insight": _get_zhuangzi_insight(theme),
    }

def _get_zhuangzi_insight(theme: str) -> str:
    """get庄子核心洞见"""
    insights = {
        "自由逍遥": "真正的自由不是外在的,而是内在的超越--打破有用/无用,大/小,是/非的执念,达到'无待'的逍遥境界",
        "处世智慧": "心斋坐忘,虚己以游世.不要试图改变世界,先修炼自己的内心",
        "生命哲学": "安时而处顺,哀乐不能入.超越生死恐惧,与道合一",
        "认知突破": "井蛙不可语海,夏虫不可语冰.认知的边界就是你世界的边界",
        "无为管理": "无为而尊者,天道也;有为而累者,人道也.最好的管理是让人感觉不到管理",
    }
    return insights.get(theme, "天地与我并生,而万物与我为一")

def analyze_de_jing_hierarchy(self, situation: str) -> Dict[str, Any]:
    """德经五层递降分析 v2.0"""
    levels = list(DeJingHierarchy)
    nature_keywords = {
        "上德": ["自然", "无为", "真诚", "朴实", "不刻意"],
        "下德": ["形式", "表面", "装", "刻意", "表演"],
        "上仁": ["关爱", "善良", "温暖", "利他"],
        "上义": ["正义", "规则", "责任", "义务", "公平"],
        "上礼": ["礼仪", "礼节", "制度", "流程", "规范"],
    }

    matched_level = levels[4]
    max_score = 0
    for level in levels:
        score = sum(1 for kw in nature_keywords[level.level] if kw in situation)
        if score > max_score:
            max_score = score
            matched_level = level

    level_index = levels.index(matched_level)
    if level_index <= 1:
        trend = "德行充盈,道在身边"
        advice = "保持无为自然的境界,这是最高层的管理智慧"
    elif level_index <= 2:
        trend = "德有所失,仁义可补"
        advice = "已从德降为仁,建议回归不刻意的自然状态"
    elif level_index <= 3:
        trend = "仁义不足,需靠规则"
        advice = "已从仁降为义,需注意不要完全依赖制度,回归人文关怀"
    else:
        trend = "礼为忠信之薄,乱之首"
        advice = "已到礼的阶段,制度越多越乱.'夫礼者,忠信之薄而乱之首',需要从根本反思"

    return {
        "current_level": matched_level.level,
        "quote": matched_level.quote,
        "meaning": matched_level.meaning,
        "hierarchy_order": [l.level for l in levels],
        "trend": trend,
        "advice": advice,
        "dao_reference": "道德经第三十八章:失道而后德,失德而后仁,失仁而后义,失义而后礼",
    }

def analyze_wuxing_cycle(self, element: str, action: str) -> Dict[str, Any]:
    """五行生克分析 v2.0"""
    element_map = {e.name: e for e in WuXing}
    target = element_map.get(element)
    if not target:
        for e in WuXing:
            if e.value[0] in element:
                target = e
                break
    if not target:
        return {"error": f"未找到五行元素: {element}"}

    sheng_chain = ["木", "火", "土", "金", "水", "木"]
    ke_chain = ["木", "土", "水", "火", "金", "木"]

    name = target.name
    result = {
        "element": name,
        "attributes": {
            "方位": target.direction,
            "季节": target.season,
            "功能": target.function,
            "脏腑": target.organ,
            "德性": target.virtue,
            "颜色": target.color,
        },
    }

    if action == "生":
        idx = sheng_chain.index(name)
        result["action"] = f"{name}生{sheng_chain[idx + 1]}"
        result["generated"] = sheng_chain[idx + 1]
        result["interpretation"] = f"{name}({target.function})促进{sheng_chain[idx + 1]}的生长"
    elif action == "克":
        idx = ke_chain.index(name)
        result["action"] = f"{name}克{ke_chain[idx + 1]}"
        result["controlled"] = ke_chain[idx + 1]
        result["interpretation"] = f"{name}制约{ke_chain[idx + 1]},防止过度"
    else:
        result["action"] = "synthesize"
        idx_s = sheng_chain.index(name)
        idx_k = ke_chain.index(name)
        result["generates"] = sheng_chain[idx_s + 1]
        result["controls"] = ke_chain[idx_k + 1]
        result["interpretation"] = f"{name}生{sheng_chain[idx_s + 1]},克{ke_chain[idx_k + 1]}"

    return result

def analyze_sixiang(self, season: str = None, state: str = None) -> Dict[str, Any]:
    """四象分析 v2.0"""
    season_map = {"春": SiXiang.SHAO_YANG, "夏": SiXiang.TAI_YANG,
                   "秋": SiXiang.SHAO_YIN, "冬": SiXiang.TAI_YIN}

    if season:
        sxiang = season_map.get(season, SiXiang.SHAO_YANG)
    elif state:
        if any(kw in state for kw in ["萌发", "开始", "起步", "新生"]):
            sxiang = SiXiang.SHAO_YANG
        elif any(kw in state for kw in ["旺盛", "巅峰", "鼎盛", "极盛"]):
            sxiang = SiXiang.TAI_YANG
        elif any(kw in state for kw in ["收敛", "收获", "成熟", "衰退"]):
            sxiang = SiXiang.SHAO_YIN
        else:
            sxiang = SiXiang.TAI_YIN
    else:
        sxiang = SiXiang.SHAO_YANG

    all_sixiang = list(SiXiang)
    idx = all_sixiang.index(sxiang)
    next_phase = all_sixiang[(idx + 1) % 4]

    return {
        "current_phase": {
            "name": sxiang.name,
            "nature": sxiang.nature,
            "time": sxiang.time,
            "meaning": sxiang.meaning,
        },
        "next_phase": {
            "name": next_phase.name,
            "meaning": next_phase.meaning,
        },
        "cycle_order": [s.name for s in all_sixiang],
        "advice": _get_sixiang_advice(sxiang),
    }

def _get_sixiang_advice(sxiang: SiXiang) -> str:
    """get四象阶段建议"""
    advices = {
        SiXiang.SHAO_YANG: "少阳阶段--阳气初生,宜静待时机,蓄积力量,不可冒进",
        SiXiang.TAI_YANG: "太阳阶段--阳气极盛,宜乘势而上,但警惕'阳极生阴'",
        SiXiang.SHAO_YIN: "少阴阶段--阴气渐长,宜收敛节制,未雨绸缪",
        SiXiang.TAI_YIN: "太阴阶段--阴气极盛,宜守藏蛰伏,静待阳生",
    }
    return advices.get(sxiang, "顺势而为")

def get_dao_management_advice(self, scenario: str) -> Dict[str, Any]:
    """道家管理哲学应用 v2.0"""
    mgmt = self.management_scenarios.get(scenario)
    if not mgmt:
        mgmt = DaoManagement.WU_WEI

    return {
        "scenario": scenario,
        "strategy_name": mgmt.name,
        "dao_quote": mgmt.quote,
        "interpretation": mgmt.interpretation,
        "application": _apply_dao_management(scenario, mgmt),
    }

def _apply_dao_management(scenario: str, mgmt: DaoManagement) -> str:
    """将道家管理哲学应用到具体场景"""
    applications = {
        "团队管理": "减少微观管理,信任团队能力,用'太上不知有之'的方式让团队自主运转",
        "战略规划": "在问题尚未出现时就提前布局,'为之于未有,治之于未乱'",
        "领导力": "像水一样服务团队,处低不争,滋养万物而不居功",
        "组织变革": "钝化变革的锋芒,化解抵触情绪,和光同尘,渐进式推进",
        "大型组织": "减少不必要的折腾和干预,'治大国若烹小鲜',稳定压倒一切",
        "企业文化": "以慈爱对待员工,以俭朴经营企业,以谦虚定位品牌",
        "远程管理": "建立完善的系统和文化,'不出户知天下',无需事必躬亲",
    }
    return applications.get(scenario, "道法自然,顺势而为")

def get_dao_health_guide(self, concern: str) -> Dict[str, Any]:
    """道家养生指导 v2.0"""
    concern_map = {
        "失眠": [DaoHealth.ZHI_XU_SHOU_JING, DaoHealth.GU_GEN_FU_MING],
        "焦虑": [DaoHealth.ZHI_XU_SHOU_JING, DaoHealth.BAO_QUAN_GUI_ZHEN],
        "疲劳": [DaoHealth.CHI_JIAN_YANG_SHEN, DaoHealth.WEI_FU_BU_WEI_MU],
        "情绪": [DaoHealth.SHAN_YANG_XIN, DaoHealth.ZHI_XU_SHOU_JING],
        "欲望": [DaoHealth.BAO_QUAN_GUI_ZHEN, DaoHealth.WEI_FU_BU_WEI_MU],
        "内耗": [DaoHealth.WEI_XUE_RI_YI_WEI_DAO_RI_SUN, DaoHealth.ZHI_XU_SHOU_JING],
        "四季": [DaoHealth.SI_XING_BING_LUN],
        "压力": [DaoHealth.GU_GEN_FU_MING, DaoHealth.CHI_JIAN_YANG_SHEN],
    }

    matched = None
    for key, value in concern_map.items():
        if key in concern:
            matched = value
            break
    if not matched:
        matched = [DaoHealth.ZHI_XU_SHOU_JING]

    return {
        "concern": concern,
        "guidance": [
            {"name": h.name, "quote": h.quote, "advice": h.interpretation}
            for h in matched
        ],
        "core_principle": "致虚极,守静笃--道家养生以虚静为根本,减少欲望,回归自然",
    }

def get_dao_three_realms(self) -> Dict[str, Any]:
    """道的三重境界 v2.0"""
    realms = list(DaoThreeRealms)
    return {
        "realms": [
            {"name": r.name, "definition": r.definition, "wisdom": r.wisdom}
            for r in realms
        ],
        "progression": "可道(现象)→ 常道(本质)→ 道法自然(合一)",
        "practice": "从语言和概念入手(可道),超越语言直达本质(常道),最终达到天人合一(道法自然)",
    }

def analyze_xian_tian_hou_tian(self, domain: str) -> Dict[str, Any]:
    """先天八卦与后天八卦方位分析 v2.0"""
    xian_tian = {
        "乾(南)": "创造/领导", "坤(北)": "承载/包容",
        "离(东)": "文化/光明", "坎(西)": "智慧/深邃",
        "震(东北)": "action/变革", "巽(西南)": "渗透/柔入",
        "艮(西北)": "稳定/坚守", "兑(东南)": "喜悦/沟通",
    }
    hou_tian = {
        "震(东)": "春分-action", "离(南)": "夏至-光明",
        "兑(西)": "秋分-收敛", "坎(北)": "冬至-藏匿",
        "巽(东南)": "立夏-柔入", "坤(西南)": "立秋-承载",
        "乾(西北)": "立冬-刚健", "艮(东北)": "立春-新生",
    }

    domain_xiantian = {
        "战略": "乾(南)", "创新": "震(东北)", "文化": "离(东)",
        "团队": "坤(北)", "渠道": "巽(西南)", "品牌": "兑(东南)",
    }

    matched_xt = domain_xiantian.get(domain, "乾(南)")
    matched_ht = {
        "战略": "离(南)", "创新": "震(东)", "文化": "离(南)",
        "团队": "坤(西南)", "渠道": "巽(东南)", "品牌": "兑(西)",
    }.get(domain, "乾(西北)")

    return {
        "domain": domain,
        "xian_tian": {
            "matched": matched_xt,
            "meaning": xian_tian.get(matched_xt, "创造领导"),
            "principle": "先天八卦体现宇宙本原秩序,适合战略定位",
        },
        "hou_tian": {
            "matched": matched_ht,
            "meaning": hou_tian.get(matched_ht, "刚健进取"),
            "principle": "后天八卦对应地理方位与季节流转,适合战术执行",
        },
        "integration": f"以先天'{matched_xt}'定战略方向,以后天'{matched_ht}'指导落地执行",
    }
