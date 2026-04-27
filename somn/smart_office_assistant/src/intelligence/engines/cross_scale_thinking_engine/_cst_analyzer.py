"""
跨尺度思维引擎 - 分析模块
Cross-Scale Thinking Engine - Analyzer Module
"""

import math
from typing import Dict, List, Tuple, Optional, Any

from ._cst_types import ScaleLevel, EmergenceType, EmergenceExample
from ._cst_constants import SCALE_HIERARCHY, EMERGENCE_EXAMPLES, FINE_TUNED_CONSTANTS

def analyze_scale(question: str) -> Dict[str, Any]:
    """
    分析问题涉及的尺度层级
    
    Args:
        question: 问题文本
        
    Returns:
        尺度分析结果
    """
    # 关键词到尺度的映射
    scale_keywords = {
        ScaleLevel.QUANTUM_FOAM: ["量子引力", "弦理论", "普朗克", "时空泡沫", "量子泡沫"],
        ScaleLevel.SUBATOMIC: ["夸克", "轻子", "玻色子", "粒子物理", "量子场论", "标准模型"],
        ScaleLevel.ATOMIC: ["原子", "电子", "轨道", "化学键", "离子", "量子力学"],
        ScaleLevel.MOLECULAR: ["分子", "蛋白质", "DNA", "RNA", "基因", "酶", "有机化学"],
        ScaleLevel.CELLULAR: ["细胞", "线粒体", "细胞核", "膜", "病毒", "细菌"],
        ScaleLevel.ORGANISM: ["生物", "动物", "植物", "人类", "大脑", "神经", "行为", "心理"],
        ScaleLevel.PLANETARY: ["地球", "行星", "大气", "海洋", "气候", "地质", "板块"],
        ScaleLevel.STELLAR: ["恒星", "太阳", "核聚变", "黑洞", "星云", "星系"],
        ScaleLevel.GALACTIC: ["星系", "银河系", "暗物质", "宇宙大尺度结构"],
        ScaleLevel.COSMOLOGICAL: ["宇宙", "大爆炸", "宇宙学", "暗能量", "微波背景"],
    }
    
    matched_scales = []
    for scale, keywords in scale_keywords.items():
        for kw in keywords:
            if kw in question:
                matched_scales.append(scale)
                break
    
    if not matched_scales:
        matched_scales = [ScaleLevel.ORGANISM]  # 默认生物体尺度
    
    # 确定主要尺度和跨度
    primary_scale = matched_scales[0]
    scale_span = len(matched_scales)
    
    return {
        "primary_scales": [s.value for s in matched_scales[:2]],
        "all_matched_scales": [s.value for s in matched_scales],
        "scale_span": scale_span,
        "is_cross_scale": scale_span > 1,
        "scale_info": {
            s.value: {
                "name": SCALE_HIERARCHY[s].name_zh,
                "size": f"10^{math.log10(SCALE_HIERARCHY[s].size_range[0]):.1f} m",
                "theories": SCALE_HIERARCHY[s].key_theories[:3]
            }
            for s in matched_scales
        }
    }

def analyze_cross_scale_relation(s1: ScaleLevel, s2: ScaleLevel) -> Dict[str, Any]:
    """
    分析两个尺度层级之间的关系
    
    Args:
        s1: 起始尺度
        s2: 目标尺度
        
    Returns:
        跨尺度关系分析
    """
    scale_order = list(ScaleLevel)
    idx1 = scale_order.index(s1)
    idx2 = scale_order.index(s2)
    
    # 计算尺度差异
    scale_diff = abs(idx2 - idx1)
    size_ratio = SCALE_HIERARCHY[s2].size_range[0] / SCALE_HIERARCHY[s1].size_range[0]
    
    # 识别涌现事件
    events = []
    for ex in EMERGENCE_EXAMPLES:
        ex_idx1 = scale_order.index(ex.from_level)
        ex_idx2 = scale_order.index(ex.to_level)
        min_idx = min(idx1, idx2)
        max_idx = max(idx1, idx2)
        if min_idx <= ex_idx1 <= max_idx and min_idx <= ex_idx2 <= max_idx:
            events.append(f"{ex.name}({ex.type.value}涌现)")
    
    # 识别知识空白
    gaps = _identify_gaps(s1, s2)
    
    return {
        "from_scale": s1.value,
        "to_scale": s2.value,
        "scale_levels_spanned": scale_diff,
        "size_ratio": size_ratio,
        "emergence_events": events,
        "knowledge_gaps": gaps,
        "reductionism_feasible": scale_diff <= 3,  # 3层以内可尝试还原论
        "requires_multiscale_modeling": scale_diff > 2
    }

def _identify_gaps(s1: ScaleLevel, s2: ScaleLevel) -> List[str]:
    """识别知识空白"""
    gaps = []
    scale_order = list(ScaleLevel)
    min_idx = min(scale_order.index(s1), scale_order.index(s2))
    max_idx = max(scale_order.index(s1), scale_order.index(s2))
    
    for i in range(min_idx, max_idx + 1):
        scale = scale_order[i]
        gap_map = {
            ScaleLevel.QUANTUM_FOAM: "量子引力理论缺失",
            ScaleLevel.SUBATOMIC: "暗物质粒子本质不明",
            ScaleLevel.CELLULAR: "蛋白质折叠问题未完全解决",
            ScaleLevel.ORGANISM: "意识困难问题未解",
            ScaleLevel.COSMOLOGICAL: "暗能量本质不明,H₀张力待解",
        }
        if scale in gap_map:
            gaps.append(f"{SCALE_HIERARCHY[scale].name_zh}:{gap_map[scale]}")
    
    return gaps

def analyze_emergence(phenomenon: str) -> Dict[str, Any]:
    """
    分析涌现现象
    
    Args:
        phenomenon: 现象描述
        
    Returns:
        涌现分析结果
    """
    # 关键词匹配已有案例
    matched = []
    for ex in EMERGENCE_EXAMPLES:
        if any(kw in phenomenon for kw in ex.name.split("→")):
            matched.append(ex)
    
    # 理论框架
    anderson_principles = [
        "还原论的破产:在足够复杂的系统中,整体不等于部分之和",
        "对称性破缺:不同尺度上物理定律的有效性可能改变",
        "新定律的出现:每个新尺度层级可能需要全新的描述语言",
        "守恒律的局限:某些守恒量只在特定尺度上有效"
    ]
    
    # 判断涌现类型
    strong_keywords = ["意识", "生命", "主观", "感受", "qualia", "灵魂",
                      "自由意志", "自我意识", "灵魂"]
    is_strong = any(kw in phenomenon for kw in strong_keywords)
    
    return {
        "phenomenon": phenomenon,
        "emergence_type": "强涌现" if is_strong else "弱涌现",
        "matched_examples": [{"name": ex.name, "type": ex.type.value,
                            "mechanism": ex.key_mechanism} for ex in matched],
        "theoretical_framework": {
            "anderson_principles": anderson_principles,
            "reductionism_limit": "当N→∞时,微积分→统计力学→新定律",
            "simulation_approach": "多尺度建模(multiscale modeling)"
        },
        "philosophical_implications": _get_emergence_philosophy(is_strong)
    }

def _get_emergence_philosophy(is_strong: bool) -> Dict[str, str]:
    """涌现的哲学含义"""
    if is_strong:
        return {
            "ontological": "强涌现意味着自然界存在不可还原的层次--整体确实具有部分没有的属性",
            "epistemological": "即使原则上可还原,实际中可能永远无法从低层预测高层行为",
            "practical": "必须在不同尺度上发展独立的描述语言和理论"
        }
    return {
        "ontological": "弱涌现是认识论的--复杂性的结果,不是本体论的新性质",
        "epistemological": "理论上可还原,但计算上不可行--需要统计力学等新方法",
        "practical": "可通过多尺度建模和统计平均来处理"
    }

def anthropic_reasoning(question: str) -> Dict[str, Any]:
    """
    基于人择原理的推理
    
    Args:
        question: 关于物理常数或宇宙条件的问题
        
    Returns:
        人择推理结果
    """
    # 匹配相关常数
    relevant_constants = []
    for key, const in FINE_TUNED_CONSTANTS.items():
        if const.name in question or const.symbol in question:
            relevant_constants.append({
                "name": const.name,
                "symbol": const.symbol,
                "value": const.value,
                "sensitivity": const.fine_tuning_sensitivity,
                "relevance": const.anthropic_relevance
            })
    
    # 人择原理的三种形式
    anthropic_principles = {
        "弱人择原理(WAP)": "我们观测到的宇宙参数必须允许观测者存在",
        "强人择原理(SAP)": "宇宙必须有允许生命发展的属性(在某个时刻)",
        "最终人择原理(FAP)": "智能信息处理必须在宇宙中产生,且一旦产生就不会消失"
    }
    
    # 可能的解释
    explanations = [
        "微调巧合论:纯属偶然,我们只是中了宇宙彩票",
        "多重宇宙论:存在10^500+个宇宙,我们自然在允许生命的那个",
        "自然选择论:宇宙参数通过某种宇宙演化机制自我选择",
        "数学必然论:当前参数是唯一数学上一致的解",
        "目的论:宇宙被设计为能产生生命"
    ]
    
    return {
        "question": question,
        "relevant_constants": relevant_constants,
        "anthropic_principles": anthropic_principles,
        "possible_explanations": explanations,
        "implications": {
            "scientific": "人择原理不能替代物理理论,但可指导研究方向",
            "philosophical": "微调问题触及科学解释的边界",
            "caution": "避免人择推理的滥用--不能用它解释所有巧合"
        }
    }

def analyze_complexity(question: str) -> Dict[str, Any]:
    """
    分析问题的复杂性特征
    
    Args:
        question: 问题文本
        
    Returns:
        复杂性分析结果
    """
    # 复杂性类型检测
    complexity_types = []
    
    chaos_keywords = ["混沌", "蝴蝶效应", "敏感依赖", "非周期", "湍流", "天气"]
    if any(kw in question for kw in chaos_keywords):
        complexity_types.append({
            "type": "混沌系统",
            "characteristics": ["确定性但不可预测", "敏感依赖初始条件", "奇异吸引子"],
            "examples": ["天气系统", "三体问题", "双摆"],
            "description": "确定性动力学产生看似随机的行为"
        })
    
    fractal_keywords = ["分形", "自相似", "标度律", "幂律", "曼德勃罗", "海岸线"]
    if any(kw in question for kw in fractal_keywords):
        complexity_types.append({
            "type": "分形结构",
            "characteristics": ["自相似性", "无特征尺度", "分数维数"],
            "examples": ["海岸线", "血管网络", "股市波动"],
            "description": "跨尺度的自相似模式"
        })
    
    network_keywords = ["网络", "连接", "节点", "度分布", "小世界", "无标度"]
    if any(kw in question for kw in network_keywords):
        complexity_types.append({
            "type": "复杂网络",
            "characteristics": ["非平凡拓扑", "涌现集体行为", "鲁棒性与脆弱性并存"],
            "examples": ["互联网", "社交网络", "代谢网络"],
            "description": "节点间相互作用产生全局模式"
        })
    
    criticality_keywords = ["临界", "相变", "自组织临界", "雪崩", "级联", "突现"]
    if any(kw in question for kw in criticality_keywords):
        complexity_types.append({
            "type": "自组织临界性",
            "characteristics": ["幂律分布", "无特征尺度", "长程关联"],
            "examples": ["地震", "森林火灾", "股市崩盘"],
            "description": "系统自发演化到临界状态"
        })
    
    return {
        "detected_types": complexity_types,
        "general_principles": [
            "非线性:输出不与输入成正比",
            "反馈:正反馈导致增长/不稳定,负反馈导致稳定/振荡",
            "延迟:时间延迟导致振荡和过冲",
            "路径依赖:历史 matters",
            "涌现:整体大于部分之和"
        ],
        "analysis_methods": [
            "寻找序参量(order parameter)",
            "识别反馈环路",
            "分析时间尺度和空间尺度",
            "考虑边界条件和初始条件"
        ]
    }

def information_theory_analysis(question: str) -> Dict[str, Any]:
    """
    从信息论角度分析问题
    
    Args:
        question: 问题文本
        
    Returns:
        信息论分析结果
    """
    return {
        "entropy_perspective": {
            "shannon_entropy": "系统的不确定性度量--高熵=高不确定性=高信息量",
            "thermodynamic_entropy": "能量品质退化--热力学第二定律",
            "connection": "Landauer原理:擦除1比特信息至少耗散kTln2能量"
        },
        "information_flow": {
            "causal_influence": "Granger因果:预测能力的提升",
            "transfer_entropy": "定向信息传递的量化",
            "synergistic_info": "多源信息的整合效应"
        },
        "complexity_measures": {
            "kolmogorov_complexity": "描述系统所需的最短程序长度",
            "effective_complexity": "既有规律又有随机性的平衡",
            "logical_depth": "从简单规则生成复杂结构所需的计算时间"
        },
        "key_insights": [
            "信息是物理的:信息处理受物理定律约束",
            "计算是热力学的:计算有能量成本",
            "生命是信息处理:生物体维持低熵状态",
            "意识可能是信息整合:IIT理论"
        ]
    }

def dust_to_wisdom_chain() -> Dict[str, Any]:
    """
    从宇宙大爆炸到人类智慧的完整因果链
    
    Returns:
        从尘埃到智慧的因果链
    """
    return {
        "title": "从尘埃到智慧--138亿年的因果链",
        "chain": [
            {
                "time": "t=0 (13.8 Gya)",
                "event": "大爆炸",
                "physics": "真空量子涨落→暴胀→ reheating→夸克-胶子等离子体",
                "significance": "四种基本力unified→对称性破缺→力分离"
            },
            {
                "time": "t=3分钟",
                "event": "太初核合成",
                "physics": "质子+中子→氢、氦、微量锂",
                "significance": "宇宙化学元素的基础"
            },
            {
                "time": "t=38万年",
                "event": "复合时期",
                "physics": "电子与原子核结合→中性原子→光子自由传播(CMB)",
                "significance": "宇宙变得透明"
            },
            {
                "time": "t=1-2亿年",
                "event": "第一代恒星",
                "physics": "氢氦气体云坍缩→核聚变点火→重元素合成",
                "significance": "碳、氧、铁等生命必需元素的产生"
            },
            {
                "time": "t=46亿年",
                "event": "太阳系形成",
                "physics": "分子云坍缩→原行星盘→行星分化",
                "significance": "地球的诞生"
            },
            {
                "time": "t=38-40亿年",
                "event": "生命起源",
                "physics": "化学演化→自复制分子→原始细胞",
                "significance": "达尔文演化开始"
            },
            {
                "time": "t=5.4亿年",
                "event": "寒武纪大爆发",
                "physics": "多细胞生物快速多样化",
                "significance": "复杂生命形式的涌现"
            },
            {
                "time": "t=2000万年",
                "event": "灵长类大脑扩张",
                "physics": "社会复杂性选择压力→新皮层扩张",
                "significance": "认知能力的跃升"
            },
            {
                "time": "t=7-20万年",
                "event": "智人出现",
                "physics": "FOXP2基因突变→语言能力→文化演化",
                "significance": "符号思维的诞生"
            },
            {
                "time": "t=1.2万年",
                "event": "农业革命",
                "physics": "定居→食物剩余→社会分层→技术积累",
                "significance": "文明的基础"
            },
            {
                "time": "t=400年",
                "event": "科学革命",
                "physics": "数学+实验→系统知识积累",
                "significance": "理解宇宙的开始"
            }
        ],
        "meta_reflection": {
            "contingency": "如果任何一步不同,我们都不会在这里",
            "necessity": "但物理定律使这种复杂性成为可能",
            "emergence": "每一步都是涌现--新属性在更高层级出现"
        }
    }

def find_unifying_structures(domains: List[str]) -> Dict[str, Any]:
    """
    寻找跨学科的unified数学结构
    
    Args:
        domains: 领域列表
        
    Returns:
        unified结构分析
    """
    # 跨学科共享的数学结构
    shared_structures = {
        "微分方程": {
            "physics": "牛顿定律,麦克斯韦方程,Schrödinger方程",
            "biology": "种群动力学,神经脉冲传播",
            "economics": "Black-Scholes期权定价",
            "engineering": "控制系统,电路分析",
            "unifying": "变化率的数学语言"
        },
        "概率与统计": {
            "physics": "统计力学,量子测量",
            "biology": "遗传漂变,演化动力学",
            "social": "民意调查,社会网络",
            "ml": "贝叶斯推断,随机过程",
            "unifying": "不确定性下的推理"
        },
        "图论与网络": {
            "physics": "费曼图,自旋网络",
            "biology": "代谢网络,蛋白质互作",
            "social": "社交网络,传播动力学",
            "cs": "算法,数据结构",
            "unifying": "关系与连接的抽象"
        },
        "优化与变分": {
            "physics": "最小作用量原理",
            "biology": "最优觅食,进化稳定策略",
            "economics": "理性选择,市场均衡",
            "ml": "损失函数最小化",
            "unifying": "极值原理是跨学科通用语言"
        },
        "信息论": {
            "physics": "熵,Landauer原理",
            "biology": "遗传信息,神经编码",
            "cs": "压缩,传输,计算复杂性",
            "cognition": "感知,学习,注意力",
            "unifying": "信息是物理的,也是认知的"
        }
    }
    
    # 匹配领域
    relevant_structures = {}
    domain_keywords = {
        "物理": "physics", "化学": "physics", "材料": "physics",
        "生物": "biology", "医学": "biology", "生命": "biology", "基因": "biology",
        "经济": "economics", "金融": "economics", "市场": "economics", "社会": "social",
        "计算机": "cs", "AI": "cs", "机器学习": "cs", "算法": "cs",
        "数学": "mathematics", "统计": "mathematics"
    }
    
    domain_tags = set()
    for d in domains:
        for kw, tag in domain_keywords.items():
            if kw in d:
                domain_tags.add(tag)
                break
    
    for name, structure in shared_structures.items():
        matching_domains = [tag for tag in domain_tags if tag in structure]
        if matching_domains:
            relevant_structures[name] = {
                "matching_domains": matching_domains,
                "examples": {k: structure[k] for k in matching_domains + ["unifying"]
                           if k in structure}
            }
    
    return {
        "domains": domains,
        "detected_domain_tags": list(domain_tags),
        "unifying_structures": relevant_structures,
        "meta_principle": {
            "name": "自然的unified性原理",
            "content": "自然界在不同尺度上使用相同的数学结构和动力学模式--"
                      "这不是巧合,而是因为物理定律在最底层规定了所有系统的基本约束",
            "caution": "类比推理有边界--必须验证数学同构性,不能仅凭直觉相似"
        }
    }

__all__ = [
    'MicroAnalyzer',
    'MacroAnalyzer',
    'CrossScaleAnalyzer',
    'analyze_scale',
    'analyze_cross_scale_relation',
    'analyze_emergence',
    'anthropic_reasoning',
    'analyze_complexity',
    'information_theory_analysis',
    'dust_to_wisdom_chain',
    'find_unifying_structures',
]


class MicroAnalyzer:
    """微观分析器 - 分析微观尺度的元素和模式"""

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """分析数据中的微观特征"""
        if isinstance(data, str):
            return {"level": "micro", "elements": [], "patterns": [], "source": data[:100]}
        return {"level": "micro", "elements": [], "patterns": [], "source": str(data)[:100]}

    def decompose_from_macro(self, macro_pattern) -> list:
        """将宏观模式分解为微观元素"""
        from ._cst_types import MicroElement, ScaleLevel
        name = getattr(macro_pattern, 'name', str(macro_pattern))
        return [MicroElement(name=f"{name}的微观要素", scale_level=ScaleLevel.ATOMIC)]


class MacroAnalyzer:
    """宏观分析器 - 分析宏观尺度的模式和结构"""

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """分析数据中的宏观特征"""
        if isinstance(data, str):
            return {"level": "macro", "patterns": [], "structures": [], "source": data[:100]}
        return {"level": "macro", "patterns": [], "structures": [], "source": str(data)[:100]}

    def infer_from_micro(self, micro_element) -> Any:
        """从微观元素推断宏观模式"""
        from ._cst_types import MacroPattern, ScaleLevel
        name = getattr(micro_element, 'name', str(micro_element))
        return MacroPattern(name=f"由{name}涌现的宏观模式", scale_level=ScaleLevel.ORGANISM)


class CrossScaleAnalyzer:
    """跨尺度分析器 - 分析不同尺度之间的桥接关系"""

    def analyze(self, micro_result: Dict, macro_result: Dict, target_scale=None) -> Dict[str, Any]:
        """执行跨尺度分析"""
        return {
            "level": "cross_scale",
            "micro_insights": micro_result,
            "macro_insights": macro_result,
            "bridges": [],
            "target_scale": str(target_scale) if target_scale else "auto",
        }
