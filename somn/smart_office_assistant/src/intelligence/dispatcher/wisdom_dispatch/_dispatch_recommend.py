"""智慧引擎unified调度器 - 问题识别与学派推荐（v10.0 全学派覆盖）"""

__all__ = [
    'get_recommended_schools',
    'get_wisdom_recommendation',
    'identify_problem_type',
    '_lvshi_recommendation',
    '_hongming_recommendation',
    '_civilization_recommendation',
    '_civ_war_economy_recommendation',
    '_scifi_recommendation',
    '_growth_recommendation',
    '_historical_thought_recommendation',
    '_generate_recommendation',
]

from typing import Dict, List, Optional, Tuple

from ._dispatch_enums import WisdomSchool, ProblemType, WisdomRecommendation

def identify_problem_type(self, problem: str) -> ProblemType:
    """recognize问题类型"""
    problem_lower = problem.lower()
    keyword_mapping = {
        ProblemType.ETHICAL: ["道德", "伦理", "善恶", "仁义", "良心", "品德"],
        ProblemType.GOVERNANCE: ["治理", "管理", "制度", "规矩", "组织"],
        ProblemType.TALENT: ["人才", "用人", "选拔", "考核", "激励"],
        ProblemType.CULTURE: ["文化", "传承", "传统", "价值观", "精神"],
        ProblemType.STRATEGY: ["战略", "转型", "规划", "布局", "长远"],
        ProblemType.CRISIS: ["危机", "风险", "紧急", "突发", "困境"],
        ProblemType.CHANGE: ["变革", "创新", "改变", "转型", "调整"],
        ProblemType.BALANCE: ["平衡", "协调", "兼顾", "调和", "中庸"],
        ProblemType.TIMING: ["时机", "择时", "流年", "运势", "节奏", "甲子", "天干", "地支"],
        ProblemType.ENVIRONMENT: ["风水", "布局", "朝向", "明堂", "靠山", "气口", "办公室"],
        ProblemType.PATTERN: ["八字", "命局", "格局", "日主", "用神", "生肖", "五行"],
        ProblemType.MINDSET: ["心态", "情绪", "压力", "焦虑", "困惑"],
        ProblemType.HARMONY: ["和谐", "矛盾", "冲突", "协调", "共识"],
        ProblemType.INTEREST: ["利益", "分配", "共赢", "得失", "取舍"],
        ProblemType.LONGTERM: ["长期", "未来", "可持续发展", "代际"],
        ProblemType.LEADERSHIP: ["领导", "decision", "权威", "影响力"],
        ProblemType.RISK: ["风险", "隐患", "不确定性", "危险", "预警"],
        ProblemType.FORTUNE: ["福祸", "吉凶", "成败", "得失", "利弊"],
        ProblemType.PERSONNEL: ["人事", "团队", "招聘", "培养", "晋升"],
        ProblemType.COMPETITION: ["竞争", "对手", "市场", "博弈"],
        ProblemType.ATTACK: ["进攻", "攻击", "扩张", "突破"],
        ProblemType.DEFENSE: ["防守", "防御", "保守", "守住"],
        ProblemType.NEGOTIATION: ["谈判", "协商", "合作", "交易"],
        ProblemType.WAR_ECONOMY_NEXUS: ["战争经济", "经战", "动员", "税收", "财政军事", "富国强兵"],
        ProblemType.STATE_CAPACITY: ["国家能力", "治理能力", "后勤", "财政能力", "组织能力"],
        ProblemType.INSTITUTIONAL_SEDIMENTATION: ["制度沉淀", "制度化", "官僚", "长期治理", "沉淀为制度"],
        ProblemType.PUBLIC_INTEREST: ["公私", "大公无私", "天下为公", "私利"],
        ProblemType.SEASONAL: ["时令", "季节", "时机", "四时", "十二月"],
        ProblemType.YINYANG: ["阴阳", "刚柔", "动静", "虚实"],
        ProblemType.DIMENSION: ["维度", "降维", "升维", "维度打击", "高维"],
        ProblemType.SURVIVAL: ["生存", "黑暗森林", "文明", "威胁"],
        ProblemType.SCALE: ["尺度", "宇宙", "宏观", "微观", "星际"],
        ProblemType.GROWTH_MINDSET: ["成长", "突破", "超越", "进步", "提升"],
        ProblemType.REVERSE: ["逆向", "反向", "反过来", "反其道"],
        ProblemType.CLOSED_LOOP: ["闭环", "循环", "迭代", "反馈", "PDCA"],
        ProblemType.CREATION_MYTH: ["创世", "起源", "混沌", "开天辟地", "从无到有", "盘古", "女娲"],
        ProblemType.APOCALYPSE: ["灭世", "末日", "洪水", "灾难", "天崩地裂", "共工"],
        ProblemType.CYCLICAL: ["循环", "轮回", "劫运", "周期", "阴阳交替", "生生不息"],
        ProblemType.NARRATIVE: ["叙事", "故事", "讲述", "表达", "写作", "文案", "品牌故事"],
        ProblemType.RESILIENCE: ["韧性", "苦难", "坚持", "逆境", "磨砺", "不屈"],
        ProblemType.CHARACTER: ["人物", "性格", "角色", "形象", "人设", "个性"],
        ProblemType.CROSS_CULTURE: ["跨文化", "国际化", "文化差异", "民族", "全球化", "本土化"],
        ProblemType.RITUAL: ["仪式", "典礼", "礼仪", "象征", "符号", "传统仪式"],
        ProblemType.CULTURAL_CHANGE: ["文化变迁", "文化冲突", "文化fusion", "文明演变"],
        ProblemType.HABIT: ["习惯", "养成", "行为", "改变", "坚持", "自律"],
        ProblemType.WILLPOWER: ["自控", "意志力", "拖延", "专注", "精力管理"],
        ProblemType.NUDGE: ["助推", "引导", "默认", "选择", "行为设计"],
        ProblemType.SCIENTIFIC_METHOD: ["验证", "实验", "假说", "数据", "证据", "可证伪"],
        ProblemType.MARKETING: ["营销", "品牌", "客户", "推广", "广告", "增长", "留存", "转化", "定位", "私域"],
        ProblemType.MARKET_ANALYSIS: ["定价", "供需", "成本", "竞争", "垄断", "弹性", "市场结构", "博弈", "均衡"],
        ProblemType.SOCIAL_DEVELOPMENT: ["社会", "发展", "不平等", "贫困", "城市化", "教育", "福利", "分层", "现代化"],
        ProblemType.SYSTEM_THINKING: ["系统", "整体", "关联", "反馈环", "涌现"],
        ProblemType.EVIDENCE: ["证据", "论证", "逻辑", "谬误", "偏见", "可信度"],
        ProblemType.PHYSICS_ANALYSIS: ["量子", "相对论", "粒子", "原子", "分子", "热力学", "化学键", "催化", "反应动力学", "薛定谔", "波函数"],
        ProblemType.LIFE_SCIENCE: ["DNA", "RNA", "蛋白质", "基因", "细胞", "突变", "进化", "基因组", "转录", "表观遗传", "突触", "神经元", "生态"],
        ProblemType.EARTH_SYSTEM: ["地质", "板块", "地震波", "地幔", "大气层", "洋流", "碳循环", "同位素", "米兰科维奇", "气候模型"],
        ProblemType.COSMOS_EXPLORATION: ["宇宙", "星系", "黑洞", "大爆炸", "暗物质", "暗能量", "恒星演化", "超新星", "宇宙微波", "哈勃常数"],
        ProblemType.SCALE_CROSSING: ["尺度阶梯", "涌现", "复杂性", "普朗克", "可观测宇宙", "跨尺度", "还原论", "人择原理", "物理常数精调"],
        ProblemType.META_PERSPECTIVE: ["元视角", "升维", "高维", "降维", "换个角度", "本质上", "根本上看"],
        ProblemType.CIVILIZATION_ANALYSIS: ["文明", "演化", "历史趋势", "长期", "文明阶段"],
        ProblemType.COSMIC_COGNITION: ["宇宙", "大爆炸", "星系", "星云", "宇宙演化", "天体"],
        ProblemType.SCALE_TRANSFORMATION: ["尺度", "微观", "宏观", "宇观", "跨尺度", "量级"],
        ProblemType.WORLDVIEW_SHIFT: ["世界观", "认知框架", "思维模式", "范式", "视角转换"],
        ProblemType.WISDOM_EVOLUTION: ["智慧", "意识", "智能", "涌现", "认知进化"],
        ProblemType.TECH_EVOLUTION: ["技术", "科技", "AI", "人工智能", "发展轨迹", "技术革命"],
        ProblemType.HISTORICAL_ANALYSIS: ["历史", "思想史", "演进", "发展脉络", "历史规律", "历史视角"],
        ProblemType.THOUGHT_EVOLUTION: ["思想", "哲学", "认识论", "本体论", "思维范式", "思想变革"],
        ProblemType.ECONOMIC_EVOLUTION: ["经济思想", "经济学史", "经济理论", "经济范式", "经济转型"],
        ProblemType.TECH_HISTORY: ["科技史", "技术史", "科学革命", "工业革命", "技术演进"],
        ProblemType.CROSS_DIMENSION: ["跨维度", "互动", "相互影响", "协同演化", "三维度", "synthesize"],
        ProblemType.PARADIGM_SHIFT: ["范式", "范式转换", "范式革命", "科学革命", "库恩", "断裂"],
    }
    scores = {}
    for ptype, keywords in keyword_mapping.items():
        score = sum(1 for kw in keywords if kw in problem)
        if score > 0:
            scores[ptype] = score
    if scores:
        return max(scores, key=scores.get)
    return ProblemType.STRATEGY

def get_recommended_schools(self, problem: str, problem_type: Optional[ProblemType] = None) -> List[Tuple[WisdomSchool, float]]:
    """get推荐的智慧学派及权重"""
    if problem_type is None:
        problem_type = identify_problem_type(self, problem)
    return self.problem_school_mapping.get(
        problem_type,
        [(WisdomSchool.CONFUCIAN, 0.7), (WisdomSchool.DAOIST, 0.5)]
    )

def get_wisdom_recommendation(self, problem: str, problem_type: Optional[ProblemType] = None) -> List[WisdomRecommendation]:
    """get智慧建议"""
    recommendations = []
    schools = get_recommended_schools(self, problem, problem_type)
    for school, weight in schools:
        engine = self._get_engine(school)
        if not engine:
            continue
        rec = _generate_recommendation(self, school, problem, weight)
        if rec:
            recommendations.append(rec)
    return recommendations

def _generate_recommendation(self, school: WisdomSchool, problem: str, weight: float) -> Optional[WisdomRecommendation]:
    """generate单个学派的建议（表驱动，替代22个elif分支）"""
    try:
        _fn = _RECOMMENDATION_TABLE.get(school)
        if _fn:
            return _fn(school, weight)
    except Exception:
        return None
    return None


def _confucian_recommendation(school, weight):
    quotes = {"仁": "<论语·颜渊>:'克己复礼为仁.一日克己复礼,天下归仁焉.'",
               "义": "<论语·为政>:'见义不为,无勇也.'",
               "礼": "<论语·学而>:'礼之用,和为贵.'",
               "知": "<论语·为政>:'知之为知之,不知为不知,是知也.'",
               "信": "<论语·学而>:'与朋友交,言而有信.'"}
    return WisdomRecommendation(school=school, confidence=weight, primary_method="仁义礼智信五常",
        reasoning="儒家以仁为核心,强调社会秩序与人伦关系",
        advice="建议以仁爱之心待人,以礼义之道行事",
        ancient_source=quotes.get("仁", ""), modern_application="企业文化建设,团队凝聚力提升")

def _daoist_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight, primary_method="道法自然,无为而治",
        reasoning="道家强调顺应自然规律,以柔克刚,以静制动",
        advice="建议顺应时势,不强求,以柔克刚",
        ancient_source="<道德经>:'人法地,地法天,天法道,道法自然.'",
        modern_application="战略转型,危机处理,变革管理")

def _buddhist_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight, primary_method="因缘和合,解脱智慧",
        reasoning="佛家认为一切皆因缘和合,应以平常心对待得失",
        advice="建议放下执念,以平常心看待成败",
        ancient_source="<金刚经>:'凡所有相,皆是虚妄.若见诸相非相,即见如来.'",
        modern_application="心态调适,团队和谐,长期规划")

def _sufu_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight, primary_method="道,德,仁,义,礼五德decision",
        reasoning="素书以道,德,仁,义,礼为decision准则,强调知人善任",
        advice="建议以五德为标准评估风险与机遇",
        ancient_source="<素书·原始>:'道,德,仁,义,礼,五者一体也.'",
        modern_application="领导decision,风险管理,人才recognize")

def _military_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight, primary_method="知己知彼,百战不殆",
        reasoning="兵法强调战略思维,攻守兼备,奇正相生",
        advice="建议先谋后动,以奇制胜",
        ancient_source="<孙子兵法>:'知己知彼,胜乃不殆;知天知地,胜乃可全.'",
        modern_application="竞争strategy,市场攻防,谈判博弈")

def _metaphysics_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="五行平衡+干支时机+风水环境+八字结构",
        reasoning="术数时空体系擅长从结构,节奏,环境和资源分布四个层面judge问题",
        advice="建议先看结构格局,再看时机窗口,最后用环境与分工做补偏救弊",
        ancient_source="<易经>:'观乎天文,以察时变;观乎人文,以化成天下.'",
        modern_application="时机judge,办公室布局,组织结构分析,资源配置")

def _mythology_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="混沌→创世→秩序→失衡→灭世→再创世循环模型",
        reasoning="中国神话以循环宇宙观为核心,混沌并非终结而是新生的前奏",
        advice="从创世叙事中汲取'从无到有'的勇气,从灭世神话中理解'失衡即变革信号'",
        ancient_source="<三五历纪>:'天地浑沌如鸡子,盘古生其中.万八千岁,天地开辟.'",
        modern_application="组织变革,危机周期理解,创新方法论,韧性文化建设")

def _literary_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="多声部叙事+韧性模型+土地叙事+魔幻现实",
        reasoning="莫言多声部叙事揭示真理的多元性,路遥苦难叙事锻造不屈韧性",
        advice="用多声部思维理解复杂问题,用苦难韧性模型面对逆境,用土地叙事扎根现实",
        ancient_source="路遥<平凡的世界>:'生活不能等待别人来安排,要自己去争取和奋斗.'",
        modern_application="品牌叙事,组织文化建设,逆境领导力,复杂问题多维解读")

def _anthropology_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="文化相对主义+结构主义分析+仪式解码+文化变迁预测",
        reasoning="人类学教我们悬置自身文化偏见,以参与者观察理解异文化逻辑",
        advice="在跨文化场景中保持谦逊和好奇,用结构主义寻找表层行为背后的深层逻辑",
        ancient_source="<礼记·王制>:'中国戎夷,五方之民,皆有性也,不可推移.'",
        modern_application="跨文化管理,国际化战略,组织人类学,用户行为研究")

def _behavior_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="习惯回路设计+助推系统+精力管理+意志力strategy",
        reasoning="行为改变的关键不是意志力本身,而是设计好环境和习惯回路",
        advice="用微习惯启动改变,用环境设计降低阻力,用助推引导默认选择",
        ancient_source="<荀子·劝学>:'不积跬步,无以至千里;不积小流,无以成江海.'",
        modern_application="习惯养成,产品设计(助推),团队行为管理,个人效能提升")

def _science_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="科学方法论+系统思维+证据评估+逻辑谬误检测",
        reasoning="科学思维的核心是可证伪性--好的judge必须能被检验和修正",
        advice="先建立可检验的假设,再用数据和证据验证,警惕确认偏误和幸存者偏差",
        ancient_source="<大学>:'致知在格物,物格而后知至.'",
        modern_application="decision验证,数据分析,战略假设检验,逻辑谬误防范")

def _natural_science_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="跨尺度unified+物理四力+生命分子+地球系统+宇宙演化",
        reasoning="自然科学提供从普朗克长度到可观测宇宙的完整知识图景,以实验验证和数学推导为根基",
        advice="以科学事实为锚点,用尺度思维定位问题层次,以跨学科视角寻找unified原理",
        ancient_source="<易经>:'仰以观于天文,俯以察于地理.' / <大学>:'致知在格物'",
        modern_application="技术创新judge,科学decision支撑,跨学科问题分析,系统性思维训练")

def _social_science_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="STP市场细分+4P营销组合+CBBE品牌资产+波特五力+蓝海战略",
        reasoning="社会科学以实证方法研究人类社会行为,提供营销学/经济学/社会学的系统分析框架",
        advice="先用STP做市场细分定位,再用4P设计营销组合,结合波特五力分析竞争格局",
        ancient_source="<孙子兵法>:'知彼知己者,百战不殆.' / 波特:战略竞争五力分析",
        modern_application="营销strategy制定,品牌建设,市场分析,商业模式设计,竞争战略规划")

def _yangming_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="知行合一+致良知+事上磨练+万物一体",
        reasoning="王阳明xinxue强调'心即理',认为真正的智慧必须通过action来验证",
        advice="遇到问题时,先问自己的良知,而非仅凭私智;action中修正认知,而非空想后action",
        ancient_source="<传习录>:'知是行的主意,行是知的功夫;知者行之始,行者知之成.'",
        modern_application="个人成长,领导力开发,危机应对,道德decision,知行合一实践")

def _dewey_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="反省思维五步法:感觉困难→recognize问题→假设方案→推理论证→验证检验",
        reasoning="杜威认为思维起源于困惑和疑难,通过系统的反省思维可以将混沌的经验转化为清晰的知识",
        advice="面对复杂问题时,采用五步反省思维:先感受困难所在,再明确定义问题,提出多种假设,选择最优方案,最后验证效果",
        ancient_source="杜威<我们如何思维>:'反省思维是'对任何信念或知识形式的根据,价值和意义进行主动,持续和细致的思考'",
        modern_application="问题诊断,decision优化,批判性思维训练,科学方法论,经验复盘")

def _top_methods_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="七法合一:战略思维+批判性思维+创造性思维+系统思维+设计思维+博弈思维+第一性原理",
        reasoning="顶级思维法整合七大实战思维体系,根据问题类型动态选择最合适的方法组合",
        advice="战略问题用第一性原理+博弈论,竞争问题用批判性思维+逆向思维,创新问题用设计思维+创造性思维",
        ancient_source="各学科经典方法论的系统整合",
        modern_application="商业decision,创新突破,战略规划,问题解决,复杂系统分析")

def _chinese_consumer_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="面子机制+人情网络+关系社会+国潮自信+Z世代洞察+银发经济",
        reasoning="中国社会消费具有独特的本土characteristics:面子驱动消费,人情礼尚往来,差序格局的社交网络",
        advice="理解'面子'背后的身份认同诉求,用'人情'构建长期关系网络,把握'国潮'的文化自信机遇",
        ancient_source="费孝通<乡土中国>差序格局 / 儒家伦理'礼尚往来'",
        modern_application="中国市场竞争strategy,品牌本土化,Z世代营销,银发经济,直播电商,情绪消费")

def _wcc_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="宇宙演化路径+智慧涌现机制+文明演化诊断+技术进化评估",
        reasoning="WCC智慧演化体系基于科学实证,提供从宇宙演化到智慧涌现的完整演化视角",
        advice="从宇宙138亿年,智慧涌现,文明演化的视角审视当前问题,recognize所在演化阶段,judge发展趋势",
        ancient_source="现代宇宙学/生物学/考古学/技术史的科学实证研究",
        modern_application="战略预判,技术趋势分析,文明阶段诊断,认知升维,未来学思考")

def _lvshi_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="贵公去私+天下为公+因时制宜+天人合一+月令时序",
        reasoning="吕氏春秋融合儒道墨法,以'贵公去私'为政治理想,'因时制宜'为行动纲领,强调天人合一与时令协调",
        advice="先问'此公还是私',再问'此时与彼时',以天下为公之心,顺时令自然之序处理问题",
        ancient_source="<吕氏春秋·贵公>:'天下非一人之天下也,天下之天下也.'",
        modern_application="公共利益决策,可持续发展规划,时令节奏管理,系统性资源协调")

def _hongming_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="良民宗教+温良五德+名分秩序+跨文化翻译+道德文明观",
        reasoning="辜鸿铭以'良民宗教'和'温良'为文明核心,强调道德自觉优于制度约束,跨文化语境下的文化自信与翻译智慧",
        advice="以温良之力化解冲突,以良民宗教重建信任,在跨文化场景中做概念的精确翻译与价值传递",
        ancient_source="辜鸿铭<中国人的精神>:'要估价一个文明,必须问的问题是:它能产生什么样的人.'",
        modern_application="跨文化沟通,品牌出海,企业文化价值观建设,中国话语体系构建")

def _civilization_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="文明生命周期+技术革命诊断+制度沉淀评估+文明三维度分析",
        reasoning="文明演化智慧从农业革命到AI革命的五次大断裂中提炼规律,以文明阶段诊断定位问题所处的历史方位",
        advice="先诊断文明所处阶段(萌芽/扩张/成熟/转型/衰退),再匹配相应阶段的治理模式和战略节奏",
        ancient_source="雅斯贝尔斯'轴心时代'理论 + 汤因比'挑战与应战'文明模型",
        modern_application="行业生命周期分析,组织成熟度诊断,战略转型时机判断,文明比较研究")

def _civ_war_economy_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="战争经济互锁模型+动员能力评估+财政军事协同+经战主链推演",
        reasoning="文明经战体系揭示'战争是经济延续,经济是战争准备'的互锁关系,从财政、后勤、动员三维度评估国家韧性",
        advice="评估问题时先看财政健康度,再看后勤保障能力,最后看动员效率,三者缺一则体系脆弱",
        ancient_source="<孙子兵法·作战篇>:'凡用兵之法,驰车千驷,革车千乘.' / 管仲'富国强兵'思想",
        modern_application="企业资源调配,竞争对抗预算规划,组织韧性评估,商业战争模拟")

def _scifi_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="黑暗森林法则+降维打击+费米悖论+技术奇点+宇宙社会学",
        reasoning="科幻思维将问题投射到宇宙尺度,以黑暗森林的猜疑链和降维打击的技术代差重新审视竞争本质",
        advice="拉高时间维度(百年尺度)和空间维度(星际尺度),审视当前问题是否属于'降维打击'或'猜疑链'困局",
        ancient_source="刘慈欣<三体>:'宇宙就是一座黑暗森林,每个文明都是带枪的猎人.' / 费米悖论",
        modern_application="颠覆式创新防御,技术代差预警,竞争格局升维分析,长远战略预判")

def _growth_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="成长型思维+闭环迭代+逆向思考+刻意练习+复利效应",
        reasoning="成长思维以卡罗尔·德韦克理论为根基,强调能力可塑性和持续迭代,将问题视为成长机会而非威胁",
        advice="将当前问题视为成长课题,建立'尝试-反馈-修正'闭环,用刻意练习突破能力瓶颈",
        ancient_source="<荀子·劝学>:'不积跬步,无以至千里.' / 卡罗尔·德韦克<终身成长>",
        modern_application="个人成长规划,团队能力建设,产品迭代策略,学习型组织构建")

def _historical_thought_recommendation(school, weight):
    return WisdomRecommendation(school=school, confidence=weight,
        primary_method="思想史三维度+范式转换分析+跨时代思想对话+历史周期律+知识考古",
        reasoning="历史思想三维度体系从思想演进、经济转型、技术变革三个维度重构历史脉络,揭示思想范式如何推动文明跃迁",
        advice="先梳理问题的思想史根源(哪些范式在主导),再跨时代对话(古代先贤如何面对类似问题),最后预判范式转换方向",
        ancient_source="库恩<科学革命的结构>范式理论 / 梁启超'中国近三百年学术史'",
        modern_application="战略思想溯源,竞争范式分析,组织文化变革路径,知识管理架构设计")


# ── 表驱动：学派 → 推荐函数映射（替代 _generate_recommendation 中的 if-elif 链）──
_RECOMMENDATION_TABLE = {
    WisdomSchool.CONFUCIAN: _confucian_recommendation,
    WisdomSchool.DAOIST: _daoist_recommendation,
    WisdomSchool.BUDDHIST: _buddhist_recommendation,
    WisdomSchool.SUFU: _sufu_recommendation,
    WisdomSchool.MILITARY: _military_recommendation,
    WisdomSchool.METAPHYSICS: _metaphysics_recommendation,
    WisdomSchool.MYTHOLOGY: _mythology_recommendation,
    WisdomSchool.LITERARY: _literary_recommendation,
    WisdomSchool.ANTHROPOLOGY: _anthropology_recommendation,
    WisdomSchool.BEHAVIOR: _behavior_recommendation,
    WisdomSchool.SCIENCE: _science_recommendation,
    WisdomSchool.NATURAL_SCIENCE: _natural_science_recommendation,
    WisdomSchool.SOCIAL_SCIENCE: _social_science_recommendation,
    WisdomSchool.YANGMING: _yangming_recommendation,
    WisdomSchool.DEWEY: _dewey_recommendation,
    WisdomSchool.TOP_METHODS: _top_methods_recommendation,
    WisdomSchool.CHINESE_CONSUMER: _chinese_consumer_recommendation,
    WisdomSchool.WCC: _wcc_recommendation,
    WisdomSchool.LVSHI: _lvshi_recommendation,
    WisdomSchool.HONGMING: _hongming_recommendation,
    WisdomSchool.CIVILIZATION: _civilization_recommendation,
    WisdomSchool.CIV_WAR_ECONOMY: _civ_war_economy_recommendation,
    WisdomSchool.SCI_FI: _scifi_recommendation,
    WisdomSchool.GROWTH: _growth_recommendation,
    WisdomSchool.HISTORICAL_THOUGHT: _historical_thought_recommendation,
}
