"""
__all__ = [
    'synthesize_yinyang_answer',
    'yinyang_action_guidance',
    'yinyang_balance_judgment',
    'yinyang_daofa_advice',
    'yinyang_dialectical_reasoning',
    'yinyang_identify_polarities',
    'yinyang_opposition_analysis',
    'yinyang_transformation_reasoning',
]

阴阳辩证推理模块
道家哲学智慧 - 阴阳学说 + 道德经 + 太极 + 八卦
"""
from typing import Dict, List

from ._deep_reasoning_types import ReasoningMode, ThoughtNode, ReasoningResult

def yinyang_dialectical_reasoning(
    problem: str,
    result_id: str,
    context: Dict,
) -> ReasoningResult:
    """
    阴阳辩证推理 - 道家哲学智慧 [v5.0.0 道家哲学增强]

    推理步骤:
    1. 阴阳recognize - recognize问题中的阴阳两面
    2. 对立分析 - 分析阴阳对立的根源
    3. 转化推演 - 推演转化的条件和时机
    4. 平衡judge - judge当前阴阳平衡状态
    5. 道法建议 - generate道德经智慧建议
    6. action指引 - generate具体action指引
    """
    reasoning_trace = []

    # 步骤1: 阴阳recognize
    yinyang_identify = yinyang_identify_polarities(problem, context)
    node1 = ThoughtNode(
        id=f"{result_id}_yinyang_identify",
        content=f"阴阳recognize: 发现{len(yinyang_identify.get('yang_factors', []))}个阳因素, "
                f"{len(yinyang_identify.get('yin_factors', []))}个阴因素",
        reasoning_mode=ReasoningMode.YINYANG_DIALECTICAL,
        confidence=0.85,
        completeness=1.0,
        validity=0.90,
        metadata=yinyang_identify,
        status="completed"
    )
    reasoning_trace.append(node1)

    # 步骤2: 对立分析
    opposition_analysis = yinyang_opposition_analysis(problem, yinyang_identify, context)
    node2 = ThoughtNode(
        id=f"{result_id}_opposition",
        content=f"对立分析: {opposition_analysis['summary']}",
        reasoning_mode=ReasoningMode.YINYANG_DIALECTICAL,
        parent_id=node1.id,
        confidence=0.82,
        completeness=0.9,
        validity=0.88,
        metadata=opposition_analysis,
        status="completed"
    )
    reasoning_trace.append(node2)

    # 步骤3: 转化推演
    transformation = yinyang_transformation_reasoning(problem, yinyang_identify, context)
    node3 = ThoughtNode(
        id=f"{result_id}_transformation",
        content=f"转化推演: {transformation['summary']}",
        reasoning_mode=ReasoningMode.YINYANG_DIALECTICAL,
        parent_id=node1.id,
        confidence=0.80,
        completeness=0.85,
        validity=0.85,
        metadata=transformation,
        status="completed"
    )
    reasoning_trace.append(node3)

    # 步骤4: 平衡judge
    balance_judgment = yinyang_balance_judgment(yinyang_identify, opposition_analysis)
    node4 = ThoughtNode(
        id=f"{result_id}_balance",
        content=f"平衡judge: {balance_judgment['state']} "
                f"(阳:{balance_judgment['yang_ratio']:.0%} vs 阴:{balance_judgment['yin_ratio']:.0%})",
        reasoning_mode=ReasoningMode.YINYANG_DIALECTICAL,
        parent_id=node2.id,
        confidence=0.85,
        completeness=1.0,
        validity=0.90,
        metadata=balance_judgment,
        status="completed"
    )
    reasoning_trace.append(node4)

    # 步骤5: 道法建议(道德经智慧)
    daofa_advice = yinyang_daofa_advice(problem, balance_judgment, transformation)
    node5 = ThoughtNode(
        id=f"{result_id}_daofa",
        content=f"道法建议: {daofa_advice['core_chapter']} - {daofa_advice['core_quote']}",
        reasoning_mode=ReasoningMode.YINYANG_DIALECTICAL,
        parent_id=node4.id,
        confidence=0.88,
        completeness=1.0,
        validity=0.92,
        metadata=daofa_advice,
        status="completed"
    )
    reasoning_trace.append(node5)

    # 步骤6: action指引
    action_guidance = yinyang_action_guidance(balance_judgment, transformation, daofa_advice)
    node6 = ThoughtNode(
        id=f"{result_id}_action",
        content=f"action指引: {action_guidance['primary_action']}",
        reasoning_mode=ReasoningMode.YINYANG_DIALECTICAL,
        parent_id=node5.id,
        confidence=0.85,
        completeness=1.0,
        validity=0.88,
        metadata=action_guidance,
        status="completed"
    )
    reasoning_trace.append(node6)

    # synthesize置信度
    all_confidences = [n.confidence for n in reasoning_trace]
    avg_confidence = sum(all_confidences) / len(all_confidences)

    # generate最终答案
    final_answer = synthesize_yinyang_answer(
        problem, yinyang_identify, opposition_analysis,
        transformation, balance_judgment, daofa_advice, action_guidance
    )

    return ReasoningResult(
        result_id=result_id,
        problem=problem,
        reasoning_mode=ReasoningMode.YINYANG_DIALECTICAL,
        success=True,
        reasoning_trace=reasoning_trace,
        final_answer=final_answer,
        confidence=avg_confidence,
        steps_count=len(reasoning_trace),
        suggestions=action_guidance.get("suggestions", []),
        metadata={
            "reasoning_type": "yinyang_dialectical",
            "yang_ratio": balance_judgment.get("yang_ratio", 0.5),
            "yin_ratio": balance_judgment.get("yin_ratio", 0.5),
            "transformation_potential": transformation.get("potential", "medium"),
            "dao_chapter": daofa_advice.get("chapter_name", ""),
            "bagua_correlation": daofa_advice.get("bagua_correlation", "")
        }
    )

def yinyang_identify_polarities(problem: str, context: Dict) -> Dict:
    """recognize阴阳因素"""
    yang_keywords = ["强", "动", "进", "攻", "快", "大", "刚", "显", "明", "阳",
                    "竞争", "扩张", "增长", "激进", "主动", "出击", "规模化", "速度"]
    yin_keywords = ["弱", "静", "退", "守", "慢", "小", "柔", "隐", "暗", "阴",
                   "合作", "收缩", "保守", "被动", "观望", "深耕", "质量", "稳健"]

    yang_factors = []
    yin_factors = []
    yang_weight = 0
    yin_weight = 0

    words = problem.split()
    for word in words:
        word_clean = word.strip(',.!?,;:""\'\'()')
        if any(kw in word_clean for kw in yang_keywords):
            yang_factors.append(word_clean)
            yang_weight += 1
        if any(kw in word_clean for kw in yin_keywords):
            yin_factors.append(word_clean)
            yin_weight += 1

    # 从上下文get额外信息
    if context:
        for key, val in context.items():
            if isinstance(val, str):
                for kw in yang_keywords:
                    if kw in val:
                        yang_factors.append(f"[{key}]: {val[:20]}")
                        yang_weight += 0.5
                for kw in yin_keywords:
                    if kw in val:
                        yin_factors.append(f"[{key}]: {val[:20]}")
                        yin_weight += 0.5

    total = yang_weight + yin_weight
    if total == 0:
        yang_ratio = 0.5
        yin_ratio = 0.5
    else:
        yang_ratio = yang_weight / total
        yin_ratio = yin_weight / total

    # judge主导因素
    if yang_ratio > 0.6:
        dominant = "阳盛"
        description = "阳性力量占优,需要阴柔调和"
    elif yin_ratio > 0.6:
        dominant = "阴盛"
        description = "阴性力量占优,需要阳刚激发"
    else:
        dominant = "平衡"
        description = "阴阳相对平衡,可顺势而为"

    return {
        "yang_factors": list(set(yang_factors))[:10],
        "yin_factors": list(set(yin_factors))[:10],
        "yang_weight": yang_weight,
        "yin_weight": yin_weight,
        "yang_ratio": round(yang_ratio, 3),
        "yin_ratio": round(yin_ratio, 3),
        "dominant": dominant,
        "description": description
    }

def yinyang_opposition_analysis(problem: str, yinyang_identify: Dict,
                                 context: Dict) -> Dict:
    """对立分析"""
    oppositions = []
    summary_parts = []

    # recognize明显的对立
    if yinyang_identify["yang_ratio"] > 0.6:
        oppositions.append({
            "type": "yang_dominant",
            "yin_aspect": "过度阳刚导致失衡",
            "yang_aspect": "阳盛阴衰",
            "resolution": "需要引入阴柔力量平衡"
        })
        summary_parts.append("阳盛阴衰,需要阴柔调和")
    elif yinyang_identify["yin_ratio"] > 0.6:
        oppositions.append({
            "type": "yin_dominant",
            "yang_aspect": "缺乏阳刚之气",
            "yin_aspect": "阴盛阳衰",
            "resolution": "需要激发阳刚力量"
        })
        summary_parts.append("阴盛阳衰,需要阳刚激发")
    else:
        oppositions.append({
            "type": "balanced",
            "yin_aspect": "阴阳相对平衡",
            "yang_aspect": "阴阳相对平衡",
            "resolution": "保持平衡,顺势而为"
        })
        summary_parts.append("阴阳相对平衡,可顺势而为")

    # recognize具体矛盾
    contradiction_keywords = [
        ("规模与质量", ["规模", "规模化"], ["质量", "精品"]),
        ("速度与稳健", ["速度", "快速"], ["稳健", "保守"]),
        ("进攻与防守", ["进攻", "扩张"], ["防守", "收缩"]),
        ("开放与封闭", ["开放", "合作"], ["封闭", "自主"]),
        ("显性与隐性", ["显性", "曝光"], ["隐性", "潜藏"]),
    ]

    for name, yang_kws, yin_kws in contradiction_keywords:
        yang_hit = any(kw in problem for kw in yang_kws)
        yin_hit = any(kw in problem for kw in yin_kws)
        if yang_hit and yin_hit:
            oppositions.append({
                "type": name,
                "yin_aspect": f"偏{yin_kws[0]}",
                "yang_aspect": f"偏{yang_kws[0]}",
                "resolution": f"在{name}之间寻找平衡点"
            })
            summary_parts.append(f"存在{name}矛盾")

    return {
        "oppositions": oppositions,
        "summary": ";".join(summary_parts) if summary_parts else "未发现明显对立",
        "contradiction_count": len([o for o in oppositions if o["type"] not in ["yang_dominant", "yin_dominant", "balanced"]])
    }

def yinyang_transformation_reasoning(problem: str, yinyang_identify: Dict,
                                      context: Dict) -> Dict:
    """转化推演 - 道德经'反者道之动'"""
    transformations = []

    # 基于当前状态推演转化
    yang_ratio = yinyang_identify["yang_ratio"]
    yin_ratio = yinyang_identify["yin_ratio"]

    # 物极必反
    if yang_ratio > 0.8:
        transformations.append({
            "trigger": "阳极生阴",
            "condition": "阳刚达到极致时",
            "outcome": "开始向阴柔转化",
            "dao_chapter": "第四十章",
            "dao_quote": "反者道之动"
        })
    elif yin_ratio > 0.8:
        transformations.append({
            "trigger": "阴极生阳",
            "condition": "阴柔达到极致时",
            "outcome": "开始向阳刚转化",
            "dao_chapter": "第四十章",
            "dao_quote": "弱者道之用"
        })

    # 祸福相依
    if any(kw in problem for kw in ["危机", "困境", "失败", "危机"]):
        transformations.append({
            "trigger": "祸兮福倚",
            "condition": "危机中蕴含机遇",
            "outcome": "危中有机,转化可期",
            "dao_chapter": "第五十八章",
            "dao_quote": "祸兮,福之所倚"
        })

    if any(kw in problem for kw in ["成功", "顺利", "高峰", "巅峰"]):
        transformations.append({
            "trigger": "福兮祸伏",
            "condition": "成功中蕴含危机",
            "outcome": "盛极而衰,需要警惕",
            "dao_chapter": "第九章",
            "dao_quote": "功遂身退,天之道"
        })

    # 柔弱胜刚强
    if yang_ratio > 0.7:
        transformations.append({
            "trigger": "柔弱胜刚",
            "condition": "阳刚过盛时",
            "outcome": "以柔克刚,四两拨千斤",
            "dao_chapter": "第七十八章",
            "dao_quote": "天下莫柔弱于水,而攻坚强者莫之能胜"
        })

    # 转化潜力评估
    if yang_ratio > 0.8 or yin_ratio > 0.8:
        potential = "high"
        potential_desc = "临界状态,转化在即"
    elif 0.4 <= yang_ratio <= 0.6:
        potential = "medium"
        potential_desc = "相对平衡,稳步变化"
    else:
        potential = "low"
        potential_desc = "稳定状态,需要催化剂"

    return {
        "transformations": transformations,
        "potential": potential,
        "potential_desc": potential_desc,
        "summary": f"转化潜力{potential_desc},{'有' if transformations else '无'}明确的转化路径"
    }

def yinyang_balance_judgment(yinyang_identify: Dict,
                              opposition_analysis: Dict) -> Dict:
    """平衡judge"""
    yang_ratio = yinyang_identify["yang_ratio"]
    yin_ratio = yinyang_identify["yin_ratio"]

    # 计算平衡度
    balance_score = 1 - abs(yang_ratio - yin_ratio)
    balance_score = round(balance_score, 3)

    # judge状态
    if balance_score > 0.8:
        state = "太极平衡"
        description = "阴阳和谐,最佳decision时机"
        recommendation = "全面推进,阴阳互补"
    elif balance_score > 0.6:
        if yang_ratio > yin_ratio:
            state = "偏阳微失衡"
            description = "阳刚略盛,需要阴柔调和"
            recommendation = "适当引入阴柔strategy"
        else:
            state = "偏阴微失衡"
            description = "阴柔略盛,需要阳刚激发"
            recommendation = "适当激发阳刚之气"
    else:
        if yang_ratio > yin_ratio:
            state = "阳盛阴衰"
            description = "阳刚过盛,阴柔不足"
            recommendation = "大力引入阴柔力量"
        else:
            state = "阴盛阳衰"
            description = "阴柔过盛,阳刚不足"
            recommendation = "大力激发阳刚之气"

    # get对应的八卦
    bagua_map = {
        "太极平衡": "中宫(5) - 调和",
        "偏阳微失衡": "乾(6) - 刚健",
        "偏阴微失衡": "坤(2) - 柔顺",
        "阳盛阴衰": "乾(9) - 亢阳",
        "阴盛阳衰": "坤(2) - 重阴"
    }

    return {
        "yang_ratio": yang_ratio,
        "yin_ratio": yin_ratio,
        "balance_score": balance_score,
        "state": state,
        "description": description,
        "recommendation": recommendation,
        "bagua_correlation": bagua_map.get(state, "")
    }

def yinyang_daofa_advice(problem: str, balance_judgment: Dict,
                          transformation: Dict) -> Dict:
    """道法建议 - 道德经智慧"""
    state = balance_judgment["state"]
    potential = transformation.get("potential", "medium")

    # 根据状态选择道德经章节
    chapter_map = {
        "太极平衡": {
            "chapter_name": "第二十二章",
            "core_chapter": "曲则全",
            "core_quote": "曲则全,枉则直,洼则盈,敝则新,少则得,多则惑",
            "application": "阴阳和谐时,可以'曲'的方式保全整体,以'枉'的方式达成目标",
            "bagua": "☷☰ 泰卦 - 天地交泰"
        },
        "偏阳微失衡": {
            "chapter_name": "第三章",
            "core_chapter": "不尚贤",
            "core_quote": "不尚贤,使民不争;不贵难得之货,使民不为盗",
            "application": "阳刚略盛时,不宜进一步激化竞争,应以柔化刚",
            "bagua": "☴巽 - 风,柔入"
        },
        "偏阴微失衡": {
            "chapter_name": "第二十四章",
            "core_chapter": "企者不立",
            "core_quote": "企者不立,跨者不行,自见者不明,自是者不彰",
            "application": "阴柔略盛时,需要适当表现阳刚,不可过于低调",
            "bagua": "☳震 - 雷,动出"
        },
        "阳盛阴衰": {
            "chapter_name": "第四十章",
            "core_chapter": "反者道之动",
            "core_quote": "反者道之动,弱者道之用.天下万物生于有,有生于无",
            "application": "阳盛阴衰时,'反者道之动'提醒向对立面转化是道的规律",
            "bagua": "☵坎 - 水,陷险"
        },
        "阴盛阳衰": {
            "chapter_name": "第七十六章",
            "core_chapter": "人之生也柔弱",
            "core_quote": "人之生也柔弱,其死也坚强.万物草木之生也柔脆,其死也枯槁",
            "application": "阴盛阳衰时,柔弱是生命力的象征,应以柔化生",
            "bagua": "☲离 - 火,光明"
        }
    }

    advice = chapter_map.get(state, chapter_map["太极平衡"])

    # 根据转化潜力调整
    if potential == "high":
        advice["additional_note"] = "[转化时机]物极必反,当前处于转化临界点,宜主动寻求转变"
    elif potential == "medium":
        advice["additional_note"] = "[渐进变化]平稳变化中,宜耐心等待时机"
    else:
        advice["additional_note"] = "[稳定期]宜保持现状,等待催化剂出现"

    return advice

def yinyang_action_guidance(balance_judgment: Dict,
                             transformation: Dict,
                             daofa_advice: Dict) -> Dict:
    """action指引"""
    state = balance_judgment["state"]
    potential = transformation.get("potential", "medium")

    # 根据状态generateaction指引
    action_map = {
        "太极平衡": {
            "primary_action": "顺势而为,全面推进",
            "secondary_actions": [
                "利用当前的平衡态势,全面推进各项计划",
                "保持阴阳互补,刚柔并济",
                "关注细微变化,及时调整"
            ],
            "taiji_direction": "中宫 - 调和"
        },
        "偏阳微失衡": {
            "primary_action": "以柔化刚,引入阴柔",
            "secondary_actions": [
                "减少激进strategy,增加稳健措施",
                "加强团队协作,减少竞争对抗",
                "增加内敛型人才和strategy"
            ],
            "taiji_direction": "东南(巽) - 进入"
        },
        "偏阴微失衡": {
            "primary_action": "激发阳刚,主动出击",
            "secondary_actions": [
                "增加进攻性strategy,打破僵局",
                "提升团队士气,激发斗志",
                "增加外向型人才和strategy"
            ],
            "taiji_direction": "东(震) - 震动"
        },
        "阳盛阴衰": {
            "primary_action": "大力补阴,以柔克刚",
            "secondary_actions": [
                "战略转型,从进攻转为防守",
                "强调合作共赢,减少竞争",
                "重视文化软实力建设"
            ],
            "taiji_direction": "西北(乾)→北(坎) - 转化方向"
        },
        "阴盛阳衰": {
            "primary_action": "大力振阳,激发活力",
            "secondary_actions": [
                "变革创新,打破陈规",
                "提升执行力,加快节奏",
                "强化品牌影响力,主动出击"
            ],
            "taiji_direction": "西南(坤)→南(离) - 转化方向"
        }
    }

    action = action_map.get(state, action_map["太极平衡"])

    # generate建议
    suggestions = [
        f"核心建议: {action['primary_action']}",
        f"方向指引: {action['taiji_direction']}",
        f"智慧来源: {daofa_advice['chapter_name']} - {daofa_advice['core_chapter']}"
    ]

    if daofa_advice.get("additional_note"):
        suggestions.append(daofa_advice["additional_note"])

    return {
        "primary_action": action["primary_action"],
        "secondary_actions": action["secondary_actions"],
        "taiji_direction": action["taiji_direction"],
        "suggestions": suggestions
    }

def synthesize_yinyang_answer(problem: str,
                               yinyang_identify: Dict,
                               opposition_analysis: Dict,
                               transformation: Dict,
                               balance_judgment: Dict,
                               daofa_advice: Dict,
                               action_guidance: Dict) -> str:
    """synthesize阴阳推理答案"""
    lines = ["=" * 60]
    lines.append("阴阳辩证推理结果")
    lines.append("=" * 60)

    # 阴阳分析
    lines.append(f"\n[阴阳recognize]")
    lines.append(f"  阳因素({len(yinyang_identify['yang_factors'])}): {', '.join(yinyang_identify['yang_factors'][:5])}")
    lines.append(f"  阴因素({len(yinyang_identify['yin_factors'])}): {', '.join(yinyang_identify['yin_factors'][:5])}")
    lines.append(f"  比例: 阳{balance_judgment['yang_ratio']:.0%} vs 阴{balance_judgment['yin_ratio']:.0%}")

    # 对立分析
    lines.append(f"\n[对立分析]")
    lines.append(f"  {opposition_analysis['summary']}")
    if opposition_analysis.get('contradiction_count', 0) > 0:
        lines.append(f"  发现{opposition_analysis['contradiction_count']}对具体矛盾")

    # 转化推演
    lines.append(f"\n[转化推演]")
    lines.append(f"  {transformation['potential_desc']}")
    if transformation.get('transformations'):
        for t in transformation['transformations'][:2]:
            lines.append(f"  • {t['trigger']}: {t['outcome']} ({t['dao_chapter']})")

    # 平衡judge
    lines.append(f"\n[平衡judge]")
    lines.append(f"  状态: {balance_judgment['state']}")
    lines.append(f"  描述: {balance_judgment['description']}")
    lines.append(f"  建议: {balance_judgment['recommendation']}")
    lines.append(f"  八卦: {balance_judgment['bagua_correlation']}")

    # 道法建议
    lines.append(f"\n[道法建议]")
    lines.append(f"  章节: {daofa_advice['chapter_name']} - {daofa_advice['core_chapter']}")
    core_quote = daofa_advice['core_quote']
    lines.append(f'  引文: "{core_quote}"')
    lines.append(f"  应用: {daofa_advice['application']}")
    if daofa_advice.get('additional_note'):
        lines.append(f"  注: {daofa_advice['additional_note']}")

    # action指引
    lines.append(f"\n[action指引]")
    lines.append(f"  ⭐ {action_guidance['primary_action']}")
    lines.append(f"  📍 方向: {action_guidance['taiji_direction']}")
    for action in action_guidance['secondary_actions']:
        lines.append(f"  • {action}")

    lines.append("\n" + "=" * 60)

    return "\n".join(lines)
