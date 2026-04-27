# -*- coding: utf-8 -*-
"""
__all__ = [
    'default_p1_output',
    'default_p2_output',
    'default_p3_output',
    'extract_argument_content',
    'extract_perspective_content',
    'extract_strategy_content',
]

三级神经网络调度器 - 引擎知识库模块
Tier-3 Neural Scheduler Knowledge Base
======================================

包含:
- _ENGINE_KNOWLEDGE: 引擎ID → (引擎名称, 核心方法论, strategy模板)
- _default_p1_output(): P1引擎默认输出
- _default_p3_output(): P3引擎默认输出
- _default_p2_output(): P2引擎默认输出

版本: v1.0
日期: 2026-04-06
"""

from typing import Dict, List, Any, Optional

# ==================== 引擎领域知识库 ====================
# 引擎ID → (引擎名称, 核心方法论, strategy模板)
ENGINE_KNOWLEDGE: Dict[str, tuple] = {
    # P1层引擎
    "SUFU": ("素书", "道,德,仁,义,礼五德decision体系",
             ["以道为根,审时度势", "德者本也,财者末也", "明哲保身,忍辱负重", "遵义章风险预警"]),
    "MILITARY": ("兵法", "孙子兵法战略体系",
                 ["上兵伐谋,其次伐交", "知彼知己,百战不殆", "致人而不致于人", "以奇胜,以正合"]),
    "LVSHI": ("吕氏春秋", "杂家治理智慧",
              ["察己知人,审势度理", "天下非一人之天下", "为天下治,不私贤智", "得贤则治,失贤则乱"]),
    "ANCIENT_WISDOM_FUSION": ("古典智慧fusion", "儒道佛兵墨法融通",
                              ["以儒治世,以道治身", "执两用中,不偏不倚", "知行合一,躬行实践", "因时制宜,灵活应变"]),
    "SUPREME_WISDOM_COORDINATOR": ("超级智慧协调", "多学派fusion协调",
                                   ["synthesize七维度分析", "多视角decision整合", "全谱系智慧覆盖", "战略-战术协同"]),
    "STRATEGY": ("战略学", "现代战略分析",
                ["战略定位与竞争壁垒", "资源聚焦与核心优势", "长期主义与复利思维", "动态战略调整"]),
    "GAME_THEORY": ("博弈论", "利益博弈分析",
                   ["零和博弈与双赢strategy", "信息不对称博弈", "重复博弈与信誉机制", "占优strategy与纳什均衡"]),
    "SCI_FI": ("科幻智慧", "未来学与科幻思维",
              ["降维打击与不对称竞争", "黑天鹅与反脆弱", "技术奇点与范式转移", "长期主义与星际视角"]),
    "BEHAVIOR": ("行为塑造", "行为科学",
                ["习惯回路:触发-行为-奖励", "即时反馈与微习惯", "意志力管理与渐进改变", "环境设计与助推strategy"]),
    "POSITIONING": ("定位理论", "特劳特定位",
                   ["差异化定位与心智占领", "战略取舍与聚焦原则", "品牌认知与心智阶梯", "重新定位竞争对手"]),
    "ENTERPRISE_STRATEGY": ("企业战略", "战略规划与执行",
                            ["战略澄清与解码", "组织能力与战略匹配", "商业模式画布", "增长阶梯与路径设计"]),
    "YANGMING": ("王阳明xinxue", "知行合一与致良知",
                ["知行合一,事上磨练", "致良知,循天理", "心即理,心外无物", "此心不动,随机而动"]),
    "GROWTH": ("成长思维", "成长型心智",
              ["能力可通过努力增长", "刻意练习与舒适区边缘", "成长型 vs 固定型思维", "学习型目标设定"]),
    "CONFUCIAN": ("儒家智慧", "仁义礼智信五常",
                 ["仁者爱人,以德服人", "修身齐家治国平天下", "君子求诸己,小人求诸人", "中庸之道,过犹不及"]),
    "COMPLEXITY": ("复杂系统", "非线性思维",
                  ["涌现与自组织", "反馈回路与增强环路", "边界条件与相变", "适度冗余与韧性设计"]),
    "EASTERN_BUSINESS": ("东方商业", "东方式经营哲学",
                        ["义利合一,以义取利", "和气生财,关系经营", "长期主义与百年老店", "中庸稳健与风险控制"]),
    "METAPHYSICS": ("术数智慧", "阴阳五行时空",
                   ["阴阳平衡与动态调节", "五行生克与关系推演", "时空势能与时机选择", "天人合一的整体观"]),
    # P3层引擎
    "LOGIC": ("逻辑学", "形式逻辑与辩证逻辑",
             ["演绎推理与归纳推理", "充分必要条件", "矛盾律与排中律", "逻辑自洽性检验"]),
    "MATH": ("数学", "量化思维与建模",
            ["概率论与风险量化", "优化理论与约束求解", "博弈论数学基础", "统计推断与置信区间"]),
    "DECISION": ("decision科学", "规范decision分析",
                ["期望值最大化", "后悔值最小化", "帕累托最优", "有限理性与启发式"]),
    "CONSULTING_VALIDATOR": ("咨询验证", "咨询方法论验证",
                             ["假设驱动的MECE分析", "80/20法则", "第一性原理追问", "金字塔原理与MECE"]),
    "CIVILIZATION": ("文明演化", "历史大周期律",
                    ["技术-经济-政治周期", "文明竞争与兴衰", "制度创新与适应力", "历史先例参照"]),
    "CIV_WAR_ECONOMY": ("文明经济战争", "地缘经济博弈",
                        ["资源禀赋与比较优势", "供应链安全与冗余", "经济制裁与反制", "产业升级路径"]),
    "WISDOM_REASONING": ("智慧推理", "深度推理引擎",
                        ["多步推理链", "反事实推演", "因果推断", "类比推理与跨域mapping"]),
    "NATURAL_SCIENCE": ("自然科学", "科学方法论",
                       ["可证伪性与实验精神", "第一性原理追问", "跨尺度思维", "还原论与整体论"]),
    "SCIENCE": ("科学思维", "科学哲学",
               ["控制变量法", "可重复性与同行评审", "范式革命", "工具主义 vs 实在论"]),
    "CRITICAL": ("批判性思维", "逻辑谬误recognize",
                ["论据质量评估", "隐含假设recognize", "逻辑谬误检测", "立场中立化"]),
    "SYSTEMS": ("系统思维", "系统动力学",
               ["增强回路与平衡回路", "系统基模recognize", "杠杆点分析", "系统性干预"]),
    "DEEP_REASONING": ("深度推理", "多步逻辑推理",
                      ["因果链推理", "反事实分析", "多角度论证", "不确定性量化"]),
    "REASONING": ("推理引擎", "synthesize推理",
                 ["归纳演绎结合", "类比推理", "溯因推理", "逻辑验证"]),
    # P2层引擎
    "DAOIST": ("道家智慧", "道法自然",
              ["无为而治,顺其自然", "柔弱胜刚强", "为而不争,功成弗居", "返璞归真,绝圣弃智"]),
    "BUDDHIST": ("佛家智慧", "缘起性空与中道",
                ["诸行无常,因缘生灭", "放下执着,减少痛苦", "中道:不落两边", "利他心与慈悲行"]),
    "MYTHOLOGY": ("神话智慧", "原型与集体无意识",
                 ["英雄之旅与成长弧线", "原型形象与人生隐喻", "叙事疗法与意义重建", "文化原型参照"]),
    "LITERARY": ("文学叙事", "叙事智慧与人物分析",
                ["人物弧光与成长曲线", "典型环境中的典型人物", "叙事视角与认知框架", "文学母题与人生模式"]),
    "ANTHROPOLOGY": ("人类学", "文化人类学视角",
                    ["文化相对论与主客位切换", "礼俗与惯例", "符号与意义系统", "文化接触与涵化"]),
    "NEURO": ("神经科学", "认知神经科学",
             ["双系统理论(快慢思考)", "杏仁核劫持与前额叶调节", "多巴胺与奖励预测误差", "神经可塑性"]),
    "PSYCHOLOGY": ("心理学", "行为与认知心理学",
                  ["认知偏误与decision陷阱", "自我效能感与归因style", "认知失调与态度改变", "社会认同与从众"]),
    "SCIENCE_THINKING": ("科学思维", "科学认识论",
                        ["相关性 vs 因果性", "确认偏误与证伪思维", "奥卡姆剃刀", "贝叶斯更新"]),
    "MARKETING": ("营销心理学", "消费者行为学",
                 ["认知失调与购买decision", "锚定效应与价格感知", "稀缺性与紧迫感", "品牌信任与忠诚"]),
    "SOCIAL_SCIENCE": ("社会科学", "社会机制分析",
                      ["社会网络与关系强度", "制度与规范", "集体action困境", "社会资本"]),
    "LITERARY_NARRATIVE": ("文学叙事", "叙事分析与意义建构",
                           ["英雄之旅原型", "叙事身份认同", "文学母题mapping", "悲剧/喜剧视角"]),
    "HONGNING": ("鸿铭智慧", "文化保守主义",
                ["温良的性格characteristics", "名分与秩序", "道德高于物质", "文化认同与精神独立性"]),
    "NARRATIVE": ("叙事智慧", "故事思维",
                 ["故事弧线与人生叙事", "英雄之旅框架", "叙事重构与赋能", "反英雄与灰色人物"]),
    "CROSS_WISDOM_ANALYZER": ("跨智慧分析", "跨学派对比分析",
                             ["学派间共性提炼", "互补性recognize", "张力点发现", "fusion可能性"]),
    "POETRY": ("诗词智慧", "唐诗宋词意境",
              ["意境与象喻", "以景结情", "比兴手法", "豪放与婉约"]),
}

def default_p1_output(engine_id: str, query: str) -> Dict[str, Any]:
    """P1引擎默认输出 - 基于领域知识的合成strategy"""
    info = ENGINE_KNOWLEDGE.get(engine_id, (engine_id, "synthesize智慧", []))
    name, methodology, insights = info

    # 根据查询关键词调整strategy方向
    query_lower = query.lower()
    crisis_keywords = any(k in query_lower for k in ["危机", "亏损", "生死", "绝境", "竞争", "失败", "风险"])
    growth_keywords = any(k in query_lower for k in ["成长", "发展", "提升", "突破", "转型", "创新"])
    people_keywords = any(k in query_lower for k in ["团队", "人才", "员工", "领导", "管理", "文化"])

    # generate领域特定的strategy
    strategy_map = {
        "SUFU": [
            "遵循五德原则:危机时以'道'定方向,以'义'聚人心,以'礼'规范行为",
            "素书遵义章警示:避免急功近利,过度扩张,妇人之仁,聚焦核心竞争力",
            "修身为本:领导者以身作则,忍辱负重,方能带领团队走出困境"
        ] if crisis_keywords else [
            "以德为本,义利合一,在发展中保持战略定力",
            "人才recognize:辨明俊杰,分层培养,建立忠诚的核心团队",
            "修身二十法:戒骄戒躁,保持清醒的战略judge力"
        ],
        "MILITARY": [
            "上兵伐谋:以战略智慧化解竞争,而非单纯价格战",
            "知彼知己:深入分析竞争对手,找到不对称竞争点",
            "致人而不致于人:掌握主动权,先发制人或后发先至"
        ] if crisis_keywords else [
            "不战而屈人之兵:通过战略威慑和合作而非对抗实现目标",
            "兵贵胜,不贵久:保持战略节奏,避免持久战消耗",
            "知可以战与不可以战者胜:精准judge战略时机"
        ],
        "LVSHI": [
            "为天下治,不私贤智:打破常规,引进外部视角",
            "察己知人:先审视自身问题,再寻求外部机会",
            "得贤则治:寻找关键人才,委托重任"
        ] if crisis_keywords else [
            "兼听则明:广泛收集信息,避免单一视角盲区",
            "循名责实:建立清晰的绩效考核,确保执行力",
            "任公去私:公正用人,建立信任文化"
        ],
        "YANGMING": [
            "此心不动,随机而动:危机中保持冷静,不被情绪左右decision",
            "知行合一:快速action,在action中验证和调整strategy",
            "致良知:做出符合长远和根本利益的decision,而非短期机会主义"
        ] if crisis_keywords else [
            "事上磨练:在实际挑战中锻炼团队和问题解决能力",
            "知行合一:战略制定与执行同步,避免空谈",
            "心外无物:专注于真正重要的事,不被噪音干扰"
        ],
    }

    # 根据引擎IDgenerate通用strategy
    if engine_id in strategy_map:
        strategy_items = strategy_map[engine_id]
    elif crisis_keywords:
        strategy_items = [
            f"运用{name}的{methodology},在危机中找到破局点",
            f"以{name}智慧审视当前困境:recognize核心问题与次要矛盾",
            f"{name}视角的逆转strategy:变被动为主动,化危为机"
        ]
    elif growth_keywords:
        strategy_items = [
            f"以{name}的{methodology}指导发展方向",
            f"{name}视角的增长strategy:聚焦核心优势,循序渐进",
            f"运用{name}智慧设计可持续的增长飞轮"
        ]
    elif people_keywords:
        strategy_items = [
            f"以{name}智慧处理人的问题:建立信任,激发主动性",
            f"{name}视角的团队建设:文化塑造与能力提升并重",
            f"借鉴{name}的{methodology}设计激励机制"
        ]
    else:
        strategy_items = [
            f"运用{name}的{methodology}分析当前问题",
            f"{name}视角的核心洞察:{methodology}",
            f"基于{name}智慧的可行路径:{insights[0] if insights else '多维度synthesize研判'}"
        ]

    return {
        "engine_id": engine_id,
        "tier": "P1",
        "engine_name": name,
        "methodology": methodology,
        "strategy": ";".join(strategy_items),
        "key_points": [f"{name}视角:{ins}" for ins in insights[:3]] if insights else [f"{name}的核心洞见"],
        "action_items": [f"运用{name}方法论制定action方案", "分阶段实施并持续评估效果", "保持战略定力与灵活调整"]
    }

def default_p3_output(engine_id: str, query: str, p1_strategies: List[str]) -> Dict[str, Any]:
    """P3引擎默认输出 - 基于领域知识的可行性论证"""
    info = ENGINE_KNOWLEDGE.get(engine_id, (engine_id, "synthesize分析", []))
    name, methodology, _ = info

    # 论证方向
    evidence_items = [
        f"从{name}视角验证P1strategy与{methodology}的一致性",
        f"基于{name}历史成功案例,论证该strategy的可行性",
        f"{name}的{methodology}提供了具体的检验标准"
    ]

    # 风险预判
    risk_map = {
        "LOGIC": ["需确保推理前提正确", "避免循环论证", "注意归纳不完全性"],
        "MATH": ["模型假设可能不符合现实", "概率估计存在不确定性", "历史数据未必预测未来"],
        "DECISION": ["有限理性限制decision质量", "信息不完全性", "执行中的意外变量"],
        "CONSULTING_VALIDATOR": ["理论框架与现实差距", "实施路径可能遇到阻力", "假设条件可能变化"],
        "CIVILIZATION": ["历史类比存在局限", "文明周期并非精确规律", "当前情境与历史有差异"],
        "SCIENCE": ["科学结论的渐进性", "同行评审的局限性", "研究可重复性问题"],
        "CRITICAL": ["批判性太强可能阻碍action", "完美信息不存在", "需要平衡质疑与信任"],
    }

    risks = risk_map.get(engine_id, [
        "strategy实施需要资源和能力支撑",
        "外部环境变化可能影响strategy有效性",
        "执行过程中的偏差需要及时校正"
    ])

    # 边界条件
    boundary_conditions = [
        "strategy在假设条件成立时有效",
        "团队执行能力和资源充足",
        "外部环境未发生根本性变化"
    ]

    return {
        "engine_id": engine_id,
        "tier": "P3",
        "engine_name": name,
        "feasibility": "有条件可行",
        "supporting_evidence": evidence_items,
        "key_arguments": [
            f"{name}提供了支撑P1strategy的理论基础",
            f"{methodology}的分析支持当前方向的合理性",
            f"从{name}视角,当前条件满足strategy实施的基本要求"
        ],
        "risk_preconditions": risks,
        "boundary_conditions": boundary_conditions,
        "assessment": f"{name}视角:P1strategy在满足一定条件时具备可行性"
    }

def default_p2_output(engine_id: str, query: str, p1_strategies: List[str]) -> Dict[str, Any]:
    """P2引擎默认输出 - 基于领域知识的多元视角"""
    info = ENGINE_KNOWLEDGE.get(engine_id, (engine_id, "补充视角", []))
    name, methodology, insights = info

    p1_summary = p1_strategies[0][:50] if p1_strategies else "P1strategy"
    p1_keywords = [s[:20] for s in p1_strategies[:3]]

    # 质疑论点
    challenging_map = {
        "DAOIST": ["action过多可能适得其反,有时无为胜有为", "过度理性算计违背自然规律", "强竞争strategy可能破坏生态平衡"],
        "BUDDHIST": ["执着于成功本身是痛苦的根源", "竞争和胜负是二元执念", "以柔克刚,不争之争"],
        "MYTHOLOGY": ["英雄叙事可能掩盖系统性结构问题", "过度个人英雄主义忽视团队", "神话叙事可能美化decision过程"],
        "LITERARY": ["文学视角可能过度浪漫化现实困境", "故事化叙事可能简化复杂问题", "情感共鸣不等于正确decision"],
        "ANTHROPOLOGY": ["文化差异使通用strategy失效", "本地化需求可能与标准化冲突", "文化变革需要漫长时间"],
        "NEURO": ["理性分析受限于神经机制", "情绪在decision中有积极作用", "压力下decision质量急剧下降"],
        "PSYCHOLOGY": ["认知偏误难以完全克服", "群体心理可能压倒个体理性", "动机和能力是两回事"],
        "SCIENCE_THINKING": ["相关性不等于因果性", "当前科学共识可能出错", "复杂性无法完全还原分析"],
    }

    # 支持论点
    supporting_args = [
        f"{name}为{p1_summary}提供了价值层面的支撑",
        f"从{name}的{methodology}角度,P1strategy符合深层逻辑",
        f"{name}智慧确认了action方向的精神正确性"
    ]

    challenging_args = challenging_map.get(engine_id, [
        f"{name}视角对P1strategy提出根本性质疑",
        f"从{name}角度,{p1_keywords[0] if p1_keywords else 'P1核心strategy'}可能忽略了重要因素",
        f"{name}提醒:过度单一视角的战略存在结构性风险"
    ])

    return {
        "engine_id": engine_id,
        "tier": "P2",
        "engine_name": name,
        "alternative_view": f"{name}提供了{methodology}的补充视角",
        "supporting_arguments": supporting_args,
        "challenging_arguments": challenging_args,
        "neutral_views": [
            f"{name}既支持也质疑P1strategy,需要权衡",
            f"{name}揭示了{p1_summary}未涉及的维度",
            f"从{name}视角看,P1strategy的实施路径需要优化"
        ] if insights else [],
        "synthesis": f"fusion{p1_summary}与{name}的{methodology},形成更完整的decision视角"
    }

def extract_strategy_content(raw: Any) -> Optional[str]:
    """从P1输出中提取strategy内容"""
    if not isinstance(raw, dict):
        return str(raw)[:200] if raw else None

    for key in ["strategy", "recommendation", "advice", "action", "decision", "guidance", "plan", "方案", "建议", "decision"]:
        if key in raw:
            val = raw[key]
            if isinstance(val, list):
                return "; ".join(str(v) for v in val[:3])
            return str(val)[:500]

    return str(raw)[:200] if raw else None

def extract_argument_content(raw: Any) -> Optional[str]:
    """从P3输出中提取论证内容"""
    if not isinstance(raw, dict):
        return str(raw)[:200] if raw else None

    for key in ["论证", "assessment", "feasibility", "evidence", "support", "argument",
                "risk_preconditions", "boundary_conditions", "支撑", "论据", "风险预判"]:
        if key in raw:
            val = raw[key]
            if isinstance(val, list):
                return "; ".join(str(v) for v in val[:3])
            return str(val)[:500]

    return str(raw)[:200] if raw else None

def extract_perspective_content(raw: Any) -> Optional[str]:
    """从P2输出中提取视角内容"""
    if not isinstance(raw, dict):
        return str(raw)[:200] if raw else None

    for key in ["alternative_view", "synthesis", "perspective", "补充", "视角",
                "supporting_arguments", "challenging_arguments", "synthesize"]:
        if key in raw:
            val = raw[key]
            if isinstance(val, list):
                return "; ".join(str(v) for v in val[:3])
            return str(val)[:500]

    return str(raw)[:200] if raw else None
