"""智慧引擎unified调度器 - 融合决策引擎（v8.0 全学派覆盖）"""

__all__ = [
    'make_fusion_decision',
    'get_system_status',
    'get_wisdom_dispatcher',
]

from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

from ._dispatch_enums import WisdomSchool, ProblemType, FusionDecision

def make_fusion_decision(self, problem: str, context: Optional[Dict[str, Any]] = None) -> FusionDecision:
    """fusiondecision - 整合五大智慧体系做出synthesize决策（v1.0.0 含部门路由）"""
    problem_type = self.identify_problem_type(problem)
    schools = self.get_recommended_schools(problem, problem_type)
    # ── v1.0.0: 确定部门路由 ──
    dept_routing = self.get_department_routing(problem_type)
    dispatch_department = dept_routing.get("primary_department", "吏部")
    dispatch_departments = dept_routing.get("all_departments", ["吏部"])
    department_routing = dept_routing.get("routing_detail", "")
    # ── 收集学派输入（统一写入school_inputs字典）──
    school_set = {s[0] for s in schools}
    school_inputs: Dict[str, Dict[str, Any]] = {}
    _collectors = [
        (WisdomSchool.CONFUCIAN, _collect_confucian_input),
        (WisdomSchool.DAOIST, _collect_daoist_input),
        (WisdomSchool.BUDDHIST, _collect_buddhist_input),
        (WisdomSchool.SUFU, _collect_sufu_input),
        (WisdomSchool.MILITARY, _collect_military_input),
        (WisdomSchool.LVSHI, _collect_lvshi_input),
        (WisdomSchool.METAPHYSICS, _collect_metaphysics_input),
        (WisdomSchool.SCI_FI, _collect_scifi_input),
        (WisdomSchool.GROWTH, _collect_growth_input),
        (WisdomSchool.NATURAL_SCIENCE, _collect_natural_science_input),
    ]
    for school_key, collector in _collectors:
        if school_key in school_set:
            school_inputs[school_key.value] = collector(self, problem, context)
    reasoning_chain = _build_reasoning_chain(self, problem, problem_type, schools)
    # 在推理链中加入部门路由信息
    if department_routing:
        reasoning_chain.insert(0, f"[部门路由]{department_routing}")
    final_decision = _generate_final_decision(self, problem, schools, reasoning_chain)
    risk_warnings = _identify_risks(self, problem, schools)
    action_items = _generate_action_items(self, problem, schools, final_decision)
    overall_score = sum(w for _, w in schools[:3])
    ethics_score = _calculate_ethics_score(schools)
    wisdom_score = _calculate_wisdom_score(schools)
    strategy_score = _calculate_strategy_score(schools)
    return FusionDecision(
        timestamp=datetime.now(), problem_type=problem_type,
        primary_school=schools[0][0] if schools else WisdomSchool.CONFUCIAN,
        secondary_schools=[s[0] for s in schools[1:3]],
        # ── v1.0.0 部门字段 ──
        dispatch_department=dispatch_department,
        dispatch_departments=dispatch_departments,
        department_routing=department_routing,
        # ── v6.1 学派输入 ──
        school_inputs=school_inputs,
        # ── 决策输出 ──
        final_decision=final_decision, reasoning_chain=reasoning_chain,
        risk_warnings=risk_warnings, action_items=action_items,
        overall_score=overall_score, ethics_score=ethics_score,
        wisdom_score=wisdom_score, strategy_score=strategy_score,
        growth_score=0.8,
    )

def _collect_confucian_input(self, problem: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {"核心原则": "仁义礼智信", "适用场景": "组织治理,人才培养,文化建设", "经典指导": "<论语>", "action准则": "以德服人,以礼待人"}

def _collect_daoist_input(self, problem: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {"核心原则": "道法自然,无为而治", "适用场景": "战略转型,危机处理,阴阳平衡", "经典指导": "<道德经>", "action准则": "顺势而为,以柔克刚"}

def _collect_buddhist_input(self, problem: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {"核心原则": "因缘和合,解脱智慧", "适用场景": "心态调适,团队和谐,利益协调", "经典指导": "<金刚经>", "action准则": "放下执念平常心"}

def _collect_sufu_input(self, problem: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {"核心原则": "道,德,仁,义,礼五德", "适用场景": "领导decision,风险管理,人才recognize", "经典指导": "<素书>", "action准则": "知人善任,遵义章46"}

def _collect_military_input(self, problem: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {"核心原则": "知己知彼,百战不殆", "适用场景": "竞争strategy,市场攻防,谈判博弈", "经典指导": "<孙子兵法>", "action准则": "先谋后动,奇正相生"}

def _collect_lvshi_input(self, problem: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {"核心原则": "贵公去私,天下为公", "适用场景": "公私抉择,时令管理,阴阳调和", "经典指导": "<吕氏春秋>", "action准则": "顺应时令,阴阳平衡"}

def _collect_metaphysics_input(self, problem: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    context = context or {}
    return {
        "核心原则": "顺天时,察地利,调人和,看结构",
        "适用场景": "时机judge,风水布局,五行平衡,八字结构分析",
        "经典指导": "<易经><黄帝宅经><滴天髓>",
        "action准则": "先定主轴与短板,再定节奏与环境补位",
        "关键输入": {
            "element_weights": context.get("element_weights"),
            "pillars": context.get("pillars") or context.get("bazi"),
            "environment": context.get("environment") or context.get("layout"),
            "zodiacs": context.get("zodiacs"),
        },
    }

def _collect_scifi_input(self, problem: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {"核心原则": "黑暗森林,降维打击", "适用场景": "维度超越,生存法则,宇宙尺度", "经典指导": "刘慈欣<三体>", "action准则": "保持威慑,提升维度"}

def _collect_growth_input(self, problem: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {"核心原则": "成长型思维,持续迭代", "适用场景": "成长突破,逆向思考,闭环执行", "经典指导": "卡罗尔·德韦克<终身成长>", "action准则": "拥抱挑战,从失败中学习"}

def _collect_natural_science_input(self, problem: str, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "核心原则": "从量子到宇宙的跨尺度unified认知",
        "适用场景": "物理分析,生命科学,地球系统,宇宙探索,跨尺度思维",
        "经典指导": "自然科学全景深度研究报告 v1.0 博士生级",
        "action准则": "以实验为锚,以数学为骨,以尺度为维度,以unified为追求",
        "知识模块": {
            "物理化学": "量子力学,粒子物理,热力学,统计物理,量子化学",
            "生命科学": "分子生物学,演化论,基因组学,神经科学,生态学",
            "地球宇宙": "地质学,大气科学,宇宙学,天体物理,广义相对论",
            "跨尺度": "复杂系统,信息论,涌现,人择原理,物理常数精调",
        },
        "尺度范围": "10^-35 m (普朗克长度) ~ 10^27 m (可观测宇宙)",
    }

def _build_reasoning_chain(self, problem: str, problem_type: ProblemType, schools: List[Tuple[WisdomSchool, float]]) -> List[str]:
    chain = []
    chain.append(f"[问题recognize]问题类型:{problem_type.value}")
    school_names = [f"{s[0].value}({s[1]:.2f})" for s in schools[:3]]
    chain.append(f"[学派匹配]推荐学派:{' + '.join(school_names)}")
    for school in [s[0] for s in schools]:
        perspective = _PERSPECTIVE_TEMPLATES.get(school)
        if perspective:
            chain.append(perspective)
    return chain


# ── 表驱动：学派 → 推理链视角（替代 _build_reasoning_chain 中的 25 个 if 分支）──
_PERSPECTIVE_TEMPLATES = {
    WisdomSchool.CONFUCIAN: "[儒家视角]以仁义礼智信为准则,强调社会秩序与人际关系",
    WisdomSchool.DAOIST: "[道家视角]顺应自然规律,以柔克刚,把握阴阳平衡",
    WisdomSchool.METAPHYSICS: "[术数时空视角]先看五行强弱,再看时机窗口与环境结构,最后做补偏救弊",
    WisdomSchool.BUDDHIST: "[佛家视角]以平常心看待成败,因缘和合,放下执念",
    WisdomSchool.SUFU: "[素书视角]以五德为decision标准,知人善任,遵义预警",
    WisdomSchool.MILITARY: "[兵法视角]知己知彼,先谋后动,奇正相生",
    WisdomSchool.LVSHI: "[吕氏春秋视角]贵公去私,天下为公,顺应时令",
    WisdomSchool.SCI_FI: "[科幻思维视角]黑暗森林,降维打击,宇宙尺度",
    WisdomSchool.GROWTH: "[成长思维视角]拥抱挑战,闭环迭代,持续超越",
    WisdomSchool.MYTHOLOGY: "[神话智慧视角]混沌→创世→秩序→失衡→再创世,理解周期与变革",
    WisdomSchool.LITERARY: "[文学叙事视角]多声部理解复杂性,苦难叙事锻造韧性,土地叙事扎根现实",
    WisdomSchool.ANTHROPOLOGY: "[人类学视角]悬置偏见,文化相对主义,深层结构分析",
    WisdomSchool.BEHAVIOR: "[行为塑造视角]设计习惯回路,优化环境,降低行为阻力",
    WisdomSchool.SCIENCE: "[科学思维视角]可证伪假设,证据驱动,警惕认知偏误",
    WisdomSchool.SOCIAL_SCIENCE: "[社会科学视角]营销洞察(STP/4P/CBBE)+经济分析+社会发展三维fusion",
    WisdomSchool.NATURAL_SCIENCE: "[自然科学视角]以跨尺度unified思维定位问题层次,以科学事实和数学推导为decision根基",
    WisdomSchool.HONGMING: "[辜鸿铭视角]以温良五德化解冲突,以良民宗教建立信任,跨文化翻译传递价值",
    WisdomSchool.CIVILIZATION: "[文明演化视角]诊断文明所处阶段,从萌芽/扩张/成熟/转型/衰退匹配治理模式",
    WisdomSchool.CIV_WAR_ECONOMY: "[文明经战视角]战争经济互锁,评估财政健康度与后勤保障能力和动员效率",
    WisdomSchool.YANGMING: "[王阳明视角]知行合一,致良知,事上磨练,不空想不盲动",
    WisdomSchool.DEWEY: "[杜威视角]反省思维五步法:感觉困难→定义问题→假设方案→推理论证→验证检验",
    WisdomSchool.TOP_METHODS: "[顶级思维法视角]七法合一:战略思维+批判性思维+创造性思维+系统思维+设计思维+博弈思维+第一性原理",
    WisdomSchool.CHINESE_CONSUMER: "[中国社会消费文化视角]面子机制+人情网络+关系社会+国潮自信+Z世代洞察",
    WisdomSchool.WCC: "[WCC智慧演化视角]从宇宙演化到智慧涌现的138亿年演化视角审视问题",
    WisdomSchool.HISTORICAL_THOUGHT: "[历史思想视角]思想演进×经济转型×技术变革三维度重构历史脉络,识别范式转换",
}

def _generate_final_decision(self, problem: str, schools: List[Tuple[WisdomSchool, float]], reasoning_chain: List[str]) -> str:
    primary = schools[0][0] if schools else WisdomSchool.CONFUCIAN
    decision_templates = {
        WisdomSchool.CONFUCIAN: f"以儒家仁义为本,{problem}",
        WisdomSchool.DAOIST: f"以道家无为之道,顺势处理{problem}",
        WisdomSchool.BUDDHIST: f"以佛家平常之心,平和应对{problem}",
        WisdomSchool.SUFU: f"以素书五德为纲,审慎decision{problem}",
        WisdomSchool.MILITARY: f"以兵法奇正之术,战略应对{problem}",
        WisdomSchool.LVSHI: f"以吕氏春秋贵公去私与因时制宜之法,统筹处理{problem}",
        WisdomSchool.METAPHYSICS: f"以术数时空之法,先校准结构与节奏,再处理{problem}",
        WisdomSchool.SCI_FI: f"以科幻尺度思维拉高时间与竞争尺度,重新审视{problem}",
        WisdomSchool.GROWTH: f"以成长思维闭环迭代之法,逐步突破{problem}",
        WisdomSchool.MYTHOLOGY: f"以神话循环之眼,从混沌中recognize创世机遇,应对{problem}",
        WisdomSchool.LITERARY: f"以文学多声部叙事之法,多维度理解并应对{problem}",
        WisdomSchool.ANTHROPOLOGY: f"以人类学跨文化深度之法,悬置偏见理解{problem}",
        WisdomSchool.BEHAVIOR: f"以行为塑造科学之法,通过习惯设计和助推应对{problem}",
        WisdomSchool.SCIENCE: f"以科学思维验证之法,用可证伪假设和系统分析处理{problem}",
        WisdomSchool.NATURAL_SCIENCE: f"以自然科学跨尺度之法,从物理本质和系统演化规律重新审视{problem}",
        WisdomSchool.HONGMING: f"以辜鸿铭温良之道与良民宗教,跨文化翻译并化解{problem}",
        WisdomSchool.CIVILIZATION: f"以文明演化诊断之法,定位历史阶段后应对{problem}",
        WisdomSchool.CIV_WAR_ECONOMY: f"以经战主链之法,从财政军事协同角度处理{problem}",
        WisdomSchool.SOCIAL_SCIENCE: f"以社会科学实证之法,用营销洞察和社会分析处理{problem}",
        WisdomSchool.YANGMING: f"以王阳明知行合一之法,致良知并事上磨练以应对{problem}",
        WisdomSchool.DEWEY: f"以杜威反省思维五步法,系统思考并验证{problem}",
        WisdomSchool.TOP_METHODS: f"以顶级思维法七法合一,多框架融合分析{problem}",
        WisdomSchool.CHINESE_CONSUMER: f"以中国社会消费文化洞察之法,从面子/人情/关系中处理{problem}",
        WisdomSchool.WCC: f"以WCC智慧演化之法,从宇宙138亿年演化视角审视{problem}",
        WisdomSchool.HISTORICAL_THOUGHT: f"以历史思想三维度之法,梳理思想脉络后应对{problem}",
    }
    return decision_templates.get(primary, f"synthesize智慧处理{problem}")

def _identify_risks(self, problem: str, schools: List[Tuple[WisdomSchool, float]]) -> List[str]:
    risks = []
    risk_templates = {
        WisdomSchool.CONFUCIAN: "过于强调道德可能缺乏执行力",
        WisdomSchool.DAOIST: "过于消极可能错失机遇",
        WisdomSchool.BUDDHIST: "过于超脱可能脱离实际",
        WisdomSchool.SUFU: "过于严苛可能失去人心",
        WisdomSchool.MILITARY: "过于激进可能树敌过多",
        WisdomSchool.METAPHYSICS: "若把结构judge绝对化,容易把可调整问题误判成宿命问题",
        WisdomSchool.MYTHOLOGY: "循环思维可能导致被动等待'劫运'而非主动变革",
        WisdomSchool.LITERARY: "叙事思维可能沉溺于故事而忽略数据和事实",
        WisdomSchool.ANTHROPOLOGY: "文化相对主义可能导致价值虚无",
        WisdomSchool.BEHAVIOR: "过度依赖助推可能忽视人的主体性和自由意志",
        WisdomSchool.SCIENCE: "过度强调证据可能忽视直觉和经验智慧",
        WisdomSchool.LVSHI: "因时制宜可能变成机会主义,贵公去私可能忽视个体差异",
        WisdomSchool.HONGMING: "文化自信可能滑向文化傲慢,温良之道在强对抗场景可能力不从心",
        WisdomSchool.CIVILIZATION: "文明阶段论可能陷入历史决定论,忽视个体突破和突变",
        WisdomSchool.CIV_WAR_ECONOMY: "经战思维可能过度军事化商业竞争,忽视合作共赢",
        WisdomSchool.SCI_FI: "尺度拉得过高可能导致落地困难,黑暗森林思维可能加剧敌意螺旋",
        WisdomSchool.GROWTH: "成长思维可能陷入'永远在成长'的焦虑,忽视当前能力边界",
        WisdomSchool.NATURAL_SCIENCE: "科学还原论可能忽视人文维度和社会复杂性",
        WisdomSchool.SOCIAL_SCIENCE: "营销框架可能把复杂问题过度简化为用户画像和转化漏斗",
        WisdomSchool.YANGMING: "致良知可能变成自以为是的道德独断,忽视外部约束",
        WisdomSchool.DEWEY: "五步反省思维可能在紧急情况下过于繁琐",
        WisdomSchool.TOP_METHODS: "多框架可能让决策者陷入分析瘫痪",
        WisdomSchool.CHINESE_CONSUMER: "本土洞察可能在全球化场景中失效",
        WisdomSchool.WCC: "宏观演化视角可能导致忽视微观执行细节",
        WisdomSchool.HISTORICAL_THOUGHT: "历史类比可能误判当下独特性,陷入后见之明偏误",
    }
    for school, weight in schools:
        if weight > 0.5:
            r = risk_templates.get(school, "")
            if r:
                risks.append(r)
    return risks

def _generate_action_items(self, problem: str, schools: List[Tuple[WisdomSchool, float]], decision: str) -> List[str]:
    items = ["[修身]保持内心平静,以平常心看待得失", "[明辨]明确目标与底线,不偏离核心价值", "[action]果断decision,稳步推进,及时调整"]
    for school, weight in schools[:2]:
        if weight > 0.7:
            action = _ACTION_TEMPLATES.get(school)
            if action:
                items.append(action)
    return items


# ── 表驱动：学派 → 行动建议（替代 _generate_action_items 中的 elif 链）──
_ACTION_TEMPLATES = {
    WisdomSchool.CONFUCIAN: "[儒家]以德服人,建立信任与威信",
    WisdomSchool.DAOIST: "[道家]顺势而为,等待时机",
    WisdomSchool.BUDDHIST: "[佛家]放下执念,平常心应对",
    WisdomSchool.SUFU: "[素书]知人善任,关注人才",
    WisdomSchool.MILITARY: "[兵法]知己知彼,先谋后动",
    WisdomSchool.METAPHYSICS: "[术数时空]先做五行强弱与环境结构盘点,再决定节奏,分工与布局",
    WisdomSchool.LVSHI: "[吕氏春秋]先辨公私,再顺时令,最后统筹资源",
    WisdomSchool.HONGMING: "[辜鸿铭]以温良之力沟通,做跨文化的精确翻译与价值传递",
    WisdomSchool.CIVILIZATION: "[文明演化]诊断当前组织所处文明阶段,匹配对应治理模式",
    WisdomSchool.CIV_WAR_ECONOMY: "[文明经战]评估财政韧性和动员效率,确保资源调配体系稳固",
    WisdomSchool.SCI_FI: "[科幻思维]拉高时间维度和竞争尺度,审视是否存在降维打击风险",
    WisdomSchool.GROWTH: "[成长思维]建立尝试-反馈-修正闭环,用刻意练习突破瓶颈",
    WisdomSchool.NATURAL_SCIENCE: "[自然科学]以实验数据为锚点,用尺度思维定位问题层次",
    WisdomSchool.SOCIAL_SCIENCE: "[社会科学]用STP定位+4P组合+波特五力分析,构建系统营销方案",
    WisdomSchool.YANGMING: "[王阳明]问良知而非私智,在行动中修正认知",
    WisdomSchool.DEWEY: "[杜威]用五步反省思维:感受困难→定义问题→假设→推理→验证",
    WisdomSchool.TOP_METHODS: "[顶级思维法]用第一性原理拆解问题本质,用博弈论分析竞争格局",
    WisdomSchool.CHINESE_CONSUMER: "[中国社会消费文化]理解面子/人情/关系驱动的消费行为,设计本土化策略",
    WisdomSchool.WCC: "[WCC智慧演化]从演化阶段定位问题,预判技术趋势和文明走向",
    WisdomSchool.HISTORICAL_THOUGHT: "[历史思想]梳理问题的思想史根源,跨时代对话后预判范式转换方向",
}

def _calculate_ethics_score(schools: List[Tuple[WisdomSchool, float]]) -> float:
    return _calculate_dimension_score(schools, _ETHICS_WEIGHTS)


def _calculate_wisdom_score(schools: List[Tuple[WisdomSchool, float]]) -> float:
    return _calculate_dimension_score(schools, _WISDOM_WEIGHTS)


def _calculate_strategy_score(schools: List[Tuple[WisdomSchool, float]]) -> float:
    return _calculate_dimension_score(schools, _STRATEGY_WEIGHTS)


def _calculate_dimension_score(schools: List[Tuple[WisdomSchool, float]], weights: Dict[WisdomSchool, float]) -> float:
    """通用维度评分：遍历学派并累加权重×权重系数"""
    return min(1.0, sum(weights.get(s, 0) * w for s, w in schools))


# ── 表驱动：维度评分权重映射 ──
_ETHICS_WEIGHTS = {
    WisdomSchool.CONFUCIAN: 1.0, WisdomSchool.SUFU: 0.8,
    WisdomSchool.BUDDHIST: 0.6, WisdomSchool.LVSHI: 0.7,
    WisdomSchool.HONGMING: 0.65, WisdomSchool.YANGMING: 0.75,
}
_WISDOM_WEIGHTS = {
    WisdomSchool.DAOIST: 1.0, WisdomSchool.METAPHYSICS: 0.95,
    WisdomSchool.BUDDHIST: 0.9, WisdomSchool.CONFUCIAN: 0.7,
    WisdomSchool.WCC: 0.85, WisdomSchool.HISTORICAL_THOUGHT: 0.8,
    WisdomSchool.NATURAL_SCIENCE: 0.75, WisdomSchool.DEWEY: 0.7,
}
_STRATEGY_WEIGHTS = {
    WisdomSchool.MILITARY: 1.0, WisdomSchool.METAPHYSICS: 0.85,
    WisdomSchool.SUFU: 0.8, WisdomSchool.DAOIST: 0.7,
    WisdomSchool.CIV_WAR_ECONOMY: 0.9, WisdomSchool.TOP_METHODS: 0.85,
    WisdomSchool.CIVILIZATION: 0.75, WisdomSchool.GROWTH: 0.7,
}

def get_system_status(self) -> Dict[str, Any]:
    """get系统状态"""
    return {
        "available_schools": list(self._engines.keys()),
        "total_engines": len(self._engines),
        "problem_types_count": len(ProblemType),
        "mappings_count": len(self.problem_school_mapping),
        "version": "v1.0.0",
        "core_function": "智慧引擎unified调度(25大智慧体系·全学派覆盖)",
        "wisdom_schools": [s.value for s in WisdomSchool],
        "new_features": [
            "吕氏春秋智慧体系", "鸿铭智慧体系", "术数时空智慧体系",
            "文明演化智慧体系", "文明-经济-战争主链推演", "科幻思维体系", "成长思维体系",
            "神话智慧体系(创世/灭世/生化循环模型)", "文学叙事智慧", "人类学跨文化智慧",
            "行为塑造智慧(习惯回路/助推/精力管理)", "科学思维框架",
            "自然科学智慧体系(物理/化学/生命/地球/宇宙/跨尺度unified)",
        ]
    }

# 全局单例
_wisdom_dispatcher = None

def get_wisdom_dispatcher() -> "WisdomDispatcher":
    """get智慧调度器单例"""
    global _wisdom_dispatcher
    if _wisdom_dispatcher is None:
        from ._dispatch_mapping import WisdomDispatcher
        _wisdom_dispatcher = WisdomDispatcher()
    return _wisdom_dispatcher
