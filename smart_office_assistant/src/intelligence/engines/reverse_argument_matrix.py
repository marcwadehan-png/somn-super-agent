# -*- coding: utf-8 -*-
"""
逆向论证推荐引擎矩阵 v1.0.0
Reverse Argument Recommendation Matrix Engine

串联 感性/人性/反驳/人情世故/情绪/逆向论证/黑暗森林/行为学 8大维度，
构建独立运行的逆向论证推荐引擎矩阵。

矩阵设计:
- 8×8 引擎交叉矩阵 → 64个论证组合节点
- 每个节点 = 维度A(主视角) × 维度B(反向审视) → 逆向论证推荐
- 矩阵核心逻辑: 从一个维度的正向结论出发，用另一个维度进行逆向审视，
  生成反直觉的论证推荐

架构:
1. 八大维度定义与引擎映射
2. 矩阵交叉节点计算
3. 逆向论证生成引擎
4. 多维度串联推理链
5. 推荐输出与置信度评估

版本: v1.0.0
日期: 2026-04-28
"""

import logging
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# 第一层: 八大维度定义
# ═══════════════════════════════════════════════════════════════

class ReverseDimension(Enum):
    """逆向论证八大维度"""
    SENTIENT = "感性"           # 情感/直觉/非理性
    HUMAN_NATURE = "人性"       # 弱点/欲望/本能
    REFUTATION = "反驳"         # 证伪/批判/辩论
    SOCIAL_WISDOM = "人情世故"  # 潜规则/关系/世故
    EMOTION = "情绪"            # 情绪操控/共情/波动
    REVERSE_ARG = "逆向论证"    # 逆向思维/反直觉
    DARK_FOREST = "黑暗森林"    # 博弈/零和/生存优先
    BEHAVIORAL = "行为学"       # 认知偏差/助推/决策陷阱


@dataclass
class DimensionProfile:
    """维度画像"""
    dimension: ReverseDimension
    core_question: str           # 该维度核心追问
    reverse_prompt: str          # 逆向审视提示
    dark_assumption: str         # 暗面假设
    blind_spot: str              # 盲区揭示
    strength_bias: str           # 优势偏误
    typical_fallacy: str         # 典型谬误
    counter_narrative: str       # 反叙事
    source_engines: List[str]    # 来源引擎


# 八大维度画像定义
DIMENSION_PROFILES: Dict[ReverseDimension, DimensionProfile] = {
    ReverseDimension.SENTIENT: DimensionProfile(
        dimension=ReverseDimension.SENTIENT,
        core_question="感性驱动的决策，理性如何审视？",
        reverse_prompt="如果最吸引你的恰恰是最危险的？",
        dark_assumption="人的直觉偏爱短期舒适，规避长期真相",
        blind_spot="感性偏好让我们忽视代价和风险",
        strength_bias="感性判断的'快'被误认为'准'",
        typical_fallacy="情感启发式谬误——喜欢=正确",
        counter_narrative="你想要的，正在毁灭你想要的",
        source_engines=["emotion_wave_engine", "emotion_research_core", "yangming_reasoning_engine"],
    ),
    ReverseDimension.HUMAN_NATURE: DimensionProfile(
        dimension=ReverseDimension.HUMAN_NATURE,
        core_question="人性弱点如何被利用又如何反噬？",
        reverse_prompt="如果对方的好意恰恰是最精密的控制？",
        dark_assumption="人性趋利避害，'为你好'往往是'为我好'的包装",
        blind_spot="我们高估自己的独立性，低估被操控的程度",
        strength_bias="自信于识人能力，实则被第一印象锚定",
        typical_fallacy="基本归因错误——把行为归因于性格而非情境",
        counter_narrative="利用人性的人，终被人性利用",
        source_engines=["subconscious_demand_analyzer", "subliminal_persuasion_engine", "behavioral_economics_wisdom"],
    ),
    ReverseDimension.REFUTATION: DimensionProfile(
        dimension=ReverseDimension.REFUTATION,
        core_question="你的论点最大的漏洞是什么？",
        reverse_prompt="如果你是自己的反对者，怎么反驳？",
        dark_assumption="所有论点都有反例，'自洽'只是盲区的产物",
        blind_spot="反驳者只看漏洞，不见全貌；支持者只看全貌，不见漏洞",
        strength_bias="逻辑自洽≠事实正确，形式完美≠内容真实",
        typical_fallacy="稻草人谬误——反驳的不是对方真正的论点",
        counter_narrative="最强的反驳不是否定结论，而是否定前提",
        source_engines=["mingjia_wisdom_engine", "dewey_thinking_engine", "reverse_thinking_engine"],
    ),
    ReverseDimension.SOCIAL_WISDOM: DimensionProfile(
        dimension=ReverseDimension.SOCIAL_WISDOM,
        core_question="表面规则下，真实运作的潜规则是什么？",
        reverse_prompt="如果'不得罪人'才是最大的得罪？",
        dark_assumption="人情世故的本质是利益交换的隐性协议",
        blind_spot="太懂人情世故的人，往往被世故困住——讨好所有人=得罪所有人",
        strength_bias="情商高被误认为智慧高，世故被误认为通透",
        typical_fallacy="虚假共识效应——以为别人都跟你一样想",
        counter_narrative="最会做人的人，往往做不成事",
        source_engines=["zongheng_wisdom_engine", "social_psychology_wisdom"],
    ),
    ReverseDimension.EMOTION: DimensionProfile(
        dimension=ReverseDimension.EMOTION,
        core_question="情绪是信号还是噪音？你被操控了吗？",
        reverse_prompt="如果你的愤怒恰好是对方想要的反应？",
        dark_assumption="情绪可以被设计、被触发、被利用——你的情绪不是你的",
        blind_spot="情绪的即时性让我们忽视其来源和目的",
        strength_bias="情绪的真实感被误认为情绪的可靠性",
        typical_fallacy="情绪推理谬误——我感觉到了=它是真的",
        counter_narrative="你的情绪，可能是别人的工具",
        source_engines=["emotion_wave_engine", "emotion_research_core", "behavior_shaping_engine"],
    ),
    ReverseDimension.REVERSE_ARG: DimensionProfile(
        dimension=ReverseDimension.REVERSE_ARG,
        core_question="结论的反面是否更接近真相？",
        reverse_prompt="如果正确答案是你最不想接受的那个？",
        dark_assumption="越被广泛接受的结论，越值得怀疑——共识往往是妥协",
        blind_spot="逆向思维本身也可能成为一种执念——'反着来'≠'对的'",
        strength_bias="反直觉的洞见被过度追捧，导致为反而反",
        typical_fallacy="为反而反谬误——逆向只是方向，不是方法",
        counter_narrative="逆向论证的终点不是反对，而是超越",
        source_engines=["reverse_thinking_engine", "yinyang_reasoning", "mingjia_wisdom_engine"],
    ),
    ReverseDimension.DARK_FOREST: DimensionProfile(
        dimension=ReverseDimension.DARK_FOREST,
        core_question="在零和博弈中，谁是猎人谁是猎物？",
        reverse_prompt="如果你的善意暴露了你的弱点？",
        dark_assumption="生存是第一需求，善意可能是最危险的信号",
        blind_spot="零和思维让我们看不见正和博弈的可能",
        strength_bias="警惕性被误认为智慧，冷酷被误认为深刻",
        typical_fallacy="敌意归因偏差——把中性事件解读为恶意",
        counter_narrative="活在黑暗森林的人，最终成为黑暗本身",
        source_engines=["strategic_reasoning_engine", "zongheng_wisdom_engine"],
    ),
    ReverseDimension.BEHAVIORAL: DimensionProfile(
        dimension=ReverseDimension.BEHAVIORAL,
        core_question="你的'自由选择'有多少是被设计的？",
        reverse_prompt="如果你的决定在你以为选择之前就已做出？",
        dark_assumption="人的决策90%由系统一(直觉)驱动，所谓理性选择多为事后合理化",
        blind_spot="我们意识不到自己的认知偏差，正如鱼意识不到水",
        strength_bias="知道偏差≠避免偏差——知识的幻觉比无知更危险",
        typical_fallacy="事后诸葛亮偏误——事后觉得'我早知道'，当时却不知道",
        counter_narrative="你以为你在选择，其实是选择架构在选择你",
        source_engines=["behavioral_economics_wisdom", "behavior_shaping_engine", "social_psychology_wisdom"],
    ),
}


# ═══════════════════════════════════════════════════════════════
# 第二层: 矩阵交叉节点
# ═══════════════════════════════════════════════════════════════

@dataclass
class MatrixNode:
    """矩阵交叉节点"""
    primary: ReverseDimension       # 主视角维度
    cross: ReverseDimension         # 交叉审视维度
    synergy_type: str               # 协同类型
    reverse_argument: str           # 逆向论证
    insight: str                    # 洞察
    blind_spot_reveal: str          # 揭示盲区
    counter_narrative: str          # 反叙事
    confidence: float               # 置信度
    application: str                # 应用场景


def _generate_matrix_nodes() -> Dict[Tuple[ReverseDimension, ReverseDimension], MatrixNode]:
    """生成8×8矩阵的所有交叉节点"""
    nodes = {}
    
    # 定义关键交叉组合（不重复生成，A×B 与 B×A 侧重不同）
    key_combinations = [
        # (主视角, 交叉审视, 协同类型, 逆向论证, 洞察, 盲区揭示, 反叙事, 置信度, 应用场景)
        (ReverseDimension.SENTIENT, ReverseDimension.BEHAVIORAL,
         "感性×行为学: 情感启发式陷阱",
         "你'感觉对'的决策，可能只是认知偏差的情感包装",
         "感性偏好+锚定效应 = 对第一印象的盲目信任",
         "把'喜欢'当成了'靠谱'",
         "最心动的选择，往往是偏差最大的选择",
         0.88, "消费决策/投资判断/人事选择"),
        
        (ReverseDimension.SENTIENT, ReverseDimension.DARK_FOREST,
         "感性×黑暗森林: 善意的代价",
         "你的共情能力，在零和博弈中是最大弱点",
         "感性驱动信任+零和博弈 = 被利用的善良",
         "高估了善意被回报的概率",
         "在黑暗森林中，最感性的猎人最先暴露",
         0.85, "商业谈判/竞争策略/危机应对"),
        
        (ReverseDimension.HUMAN_NATURE, ReverseDimension.SOCIAL_WISDOM,
         "人性×人情世故: 利益的隐秘协议",
         "人情是包装，利益是内核——越讲情义，越要看清利益",
         "趋利本能+隐性规则 = 看不见的利益输送链",
         "以为'帮你是情分'，实则是'帮你是投资'",
         "最讲人情的地方，利益计算最精密",
         0.92, "组织管理/客户关系/合伙创业"),
        
        (ReverseDimension.HUMAN_NATURE, ReverseDimension.EMOTION,
         "人性×情绪: 情绪操控的底层逻辑",
         "你的愤怒不是你的——它是被设计出来的反应",
         "趋利本能+情绪触发 = 精准的情绪操控方案",
         "以为情绪是自发的，实则是被触发的",
         "最高级的操控，是让你以为自己在自由表达",
         0.90, "营销策略/舆论分析/谈判博弈"),
        
        (ReverseDimension.REFUTATION, ReverseDimension.REVERSE_ARG,
         "反驳×逆向论证: 论证的自毁程序",
         "最强反驳不是否定结论，而是证明结论的前提不成立",
         "证伪思维+逆向推理 = 釜底抽薪式论证",
         "反驳表面结论，忽略了更深层的前提谬误",
         "拆掉地基，整栋楼不需要推",
         0.87, "方案评审/风险评估/竞争分析"),
        
        (ReverseDimension.REFUTATION, ReverseDimension.BEHAVIORAL,
         "反驳×行为学: 理性的幻觉",
         "你以为在理性反驳，其实只是在为直觉找理由",
         "证伪冲动+确认偏误 = 披着批判性思维外衣的偏见",
         "反驳者常犯的错误：只反驳不想听的，不想反驳的才是关键",
         "最自信的反驳，往往最可能被偏差扭曲",
         0.86, "决策审核/逻辑审查/方案辩论"),
        
        (ReverseDimension.SOCIAL_WISDOM, ReverseDimension.DARK_FOREST,
         "人情世故×黑暗森林: 关系的暗面",
         "在黑暗森林中，最亲密的关系可能是最大的信息泄露",
         "人情网络+零和博弈 = 关系即弱点",
         "以为关系是保护，在博弈中关系是把柄",
         "你信任的人，是敌人首先策反的目标",
         0.83, "信息安全/组织防线/危机管理"),
        
        (ReverseDimension.SOCIAL_WISDOM, ReverseDimension.HUMAN_NATURE,
         "人情世故×人性: 社交博弈的囚徒困境",
         "每个人都在算，却假装不算——这就是人情世故",
         "隐性规则+趋利本能 = 表面和谐下的利益暗战",
         "以为对方讲情义，其实对方在计算",
         "最圆滑的人，算得最深——'懂事'就是'懂利'",
         0.91, "职场博弈/商务社交/利益分配"),
        
        (ReverseDimension.EMOTION, ReverseDimension.SENTIENT,
         "情绪×感性: 双重感性陷阱",
         "情绪确认了你的感性判断——但两重偏见不等于一重真相",
         "情绪波动+直觉偏好 = 感性确认偏差的超级放大",
         "情绪让你相信直觉，直觉让情绪更强烈——恶性循环",
         "情绪+直觉 ≠ 2倍正确，= 2倍偏差",
         0.89, "重要决策/情绪化消费/关系冲突"),
        
        (ReverseDimension.EMOTION, ReverseDimension.REFUTATION,
         "情绪×反驳: 情绪绑架论证",
         "你反驳的不是对方，是对方引发的你的情绪",
         "情绪反应+证伪冲动 = 带着愤怒的反驳=无效反驳",
         "以为在理性反驳，其实在情绪宣泄",
         "最激烈的反驳，往往最远离事实",
         0.84, "争论场景/意见分歧/批评反馈"),
        
        (ReverseDimension.REVERSE_ARG, ReverseDimension.DARK_FOREST,
         "逆向论证×黑暗森林: 反直觉生存法则",
         "最安全的策略往往最反直觉——因为直觉本身就是暴露",
         "逆向思维+零和博弈 = 在对手想不到的维度出手",
         "以为逆向就是创新，在博弈中逆向可能是自杀",
         "在黑暗森林里，最聪明的做法是让别人以为你不聪明",
         0.82, "竞争策略/安全防御/博弈决策"),
        
        (ReverseDimension.REVERSE_ARG, ReverseDimension.SOCIAL_WISDOM,
         "逆向论证×人情世故: 世故的反面",
         "最不懂人情世故的人，可能看得最透——因为他们在局外",
         "逆向审视+隐性规则 = 用局外人视角看破潜规则",
         "以为世故是智慧，逆向看世故是枷锁",
         "真正的高手，是看透世故后选择不世故",
         0.80, "组织变革/创新突破/跨界合作"),
        
        (ReverseDimension.DARK_FOREST, ReverseDimension.EMOTION,
         "黑暗森林×情绪: 恐惧的设计",
         "恐惧是最有效的控制——你害怕的，正是对方设计的",
         "零和博弈+情绪操控 = 通过制造恐惧实现控制",
         "以为恐惧是自然的，实则是被投放的",
         "在黑暗森林中，不怕的人不是勇敢，是被操控了恐惧阈值",
         0.88, "危机公关/舆情管理/竞争对抗"),
        
        (ReverseDimension.DARK_FOREST, ReverseDimension.HUMAN_NATURE,
         "黑暗森林×人性: 生存本能的博弈",
         "生存本能是最可靠的，也是最容易被利用的",
         "零和博弈+趋利避害 = 用安全感需求控制行为",
         "以为在自保，实则在按对方的剧本行动",
         "最高级的猎手，让你自己走进陷阱还以为是安全屋",
         0.86, "风控管理/安全策略/竞争博弈"),
        
        (ReverseDimension.BEHAVIORAL, ReverseDimension.HUMAN_NATURE,
         "行为学×人性: 设计好的'自由意志'",
         "你的自由选择是在别人设计的选择架构里做的",
         "认知偏差+趋利本能 = 可预测的非理性行为",
         "以为在独立决策，实则被助推引导",
         "最自由的消费者，是选择架构最精心设计的产物",
         0.93, "产品设计/营销策略/政策制定"),
        
        (ReverseDimension.BEHAVIORAL, ReverseDimension.EMOTION,
         "行为学×情绪: 理性的事后合理化",
         "你的理性分析，只是为情绪决定找的体面理由",
         "系统一直觉+情绪驱动 = 先决定后论证的经典模式",
         "以为决策是理性过程，实则是情绪决定+理性包装",
         "最自信的理性决策，可能是最精致的情绪合理化",
         0.91, "投资决策/消费行为/战略选择"),
        
        # 补充剩余关键交叉
        (ReverseDimension.BEHAVIORAL, ReverseDimension.DARK_FOREST,
         "行为学×黑暗森林: 被设计的博弈",
         "你以为在博弈，其实博弈规则本身就是被设计的",
         "认知偏差+零和博弈 = 在不公平的规则下'公平'博弈",
         "以为改变策略能赢，实则规则本身就是赢不了的",
         "改变不了规则的人，再聪明也只是在笼子里跑得更快",
         0.85, "市场策略/平台经济/制度博弈"),
        
        (ReverseDimension.BEHAVIORAL, ReverseDimension.SOCIAL_WISDOM,
         "行为学×人情世故: 从众的精密操控",
         "你以为从众是自由的，其实从众是被精心设计的默认选项",
         "从众效应+隐性规则 = 看不见的社会操控网",
         "以为跟大流是安全选择，实则大流是被引导的",
         "最安全的'从众'，可能是最危险的——因为羊群的方向是牧羊人选的",
         0.87, "组织文化/社会运动/消费趋势"),
        
        (ReverseDimension.EMOTION, ReverseDimension.HUMAN_NATURE,
         "情绪×人性: 情感操控的本质",
         "你以为是真心，其实是人性弱点的精准打击",
         "情绪共鸣+趋利本能 = 最高级的情感操控让你感觉不到被操控",
         "以为对方是真的在乎，实则在精准触发你的需求",
         "最真的感动，可能是最精心设计的操控",
         0.90, "品牌营销/客户关系/公共关系"),
        
        (ReverseDimension.REVERSE_ARG, ReverseDimension.BEHAVIORAL,
         "逆向论证×行为学: 反直觉的偏差陷阱",
         "你以为逆向思维能避免偏差，逆向思维本身就是偏差",
         "逆向推理+确认偏误 = '反着来'也是一种确认偏误",
         "以为逆向=独立思考，实则可能是另一种从众（逆向从众）",
         "最危险的偏差，是让你以为自己在避免偏差的偏差",
         0.84, "创新决策/逆向投资/批判性思维"),
        
        (ReverseDimension.SENTIENT, ReverseDimension.REFUTATION,
         "感性×反驳: 直觉的证伪困境",
         "你的直觉无法被证伪——这恰恰是直觉最危险的地方",
         "感性判断+不可证伪 = '感觉不对'是最难反驳的反对",
         "以为直觉是不可言传的智慧，实则可能是偏见的直觉化",
         "最无法反驳的论点，往往最值得怀疑",
         0.83, "判断审查/直觉决策/创意评估"),
        
        (ReverseDimension.SENTIENT, ReverseDimension.HUMAN_NATURE,
         "感性×人性: 共情的操控面",
         "共情能力越强，越容易被人性弱点利用",
         "感性共鸣+趋利本能 = 你感同身受的，正是对方利用的入口",
         "以为共情是优势，在博弈中共情是可利用的弱点",
         "最懂你的人，最容易操控你",
         0.86, "社交博弈/谈判策略/信任建立"),
        
        (ReverseDimension.SOCIAL_WISDOM, ReverseDimension.EMOTION,
         "人情世故×情绪: 情绪的社交伪装",
         "社交中表现的情绪，90%是策略而非真实",
         "隐性规则+情绪管理 = 情绪是人情世故中最精密的工具",
         "以为对方是真的高兴/愤怒，实则是社交表演",
         "在社交场上，最真实的情绪是赢家不露的微笑",
         0.85, "社交策略/领导力/公共演讲"),
        
        (ReverseDimension.HUMAN_NATURE, ReverseDimension.DARK_FOREST,
         "人性×黑暗森林: 弱点的猎杀",
         "你的弱点，就是黑暗森林中暴露你位置的信号",
         "趋利本能+零和博弈 = 弱点=信息泄露=被猎杀",
         "以为隐藏弱点就行，但弱点会通过行为模式暴露",
         "在黑暗森林中，越想证明自己强，越暴露自己弱",
         0.84, "安全防护/竞争优势/风险管理"),
        
        (ReverseDimension.REVERSE_ARG, ReverseDimension.EMOTION,
         "逆向论证×情绪: 用情绪做逆向论证",
         "最有效的逆向论证，不是逻辑反转而是情绪反转",
         "逆向推理+情绪触发 = 用相反的情绪体验推翻原来的判断",
         "以为逆向论证需要逻辑，实则情绪反转更有效",
         "让对手从得意变恐惧，论证就完成了",
         0.81, "辩论策略/说服力/竞标方案"),
        
        (ReverseDimension.HUMAN_NATURE, ReverseDimension.REFUTATION,
         "人性×反驳: 用人性弱点反驳人性论点",
         "反驳一个人的论点，最有效的是暴露他的利益立场",
         "趋利本能+证伪方法 = '你这么说是因为对你有利'",
         "以为在反驳论点，实则在暗示对方动机不纯",
         "最强反驳不是打倒论点，而是质疑论者",
         0.82, "辩论策略/公关危机/竞争分析"),
        
        (ReverseDimension.SENTIENT, ReverseDimension.SOCIAL_WISDOM,
         "感性×人情世故: 感觉的社交编码",
         "你以为的'心有灵犀'，其实是人情世故的默契表演",
         "直觉判断+隐性规则 = 你感觉到的'对'是社交训练的结果",
         "以为感性是真实的，在社交中感性是被规则编程的",
         "最真实的'感觉对了'，可能是最精密的社交编程",
         0.79, "社交判断/关系评估/文化适应"),
        
        (ReverseDimension.DARK_FOREST, ReverseDimension.REFUTATION,
         "黑暗森林×反驳: 证伪即暴露",
         "反驳对方的同时，你暴露了自己的立场和弱点",
         "零和博弈+证伪冲动 = 反驳=信息泄露=被利用",
         "以为反驳是进攻，在博弈中反驳是暴露",
         "在黑暗森林中，沉默比反驳更有力",
         0.83, "信息战/安全策略/沉默权"),
        
        (ReverseDimension.EMOTION, ReverseDimension.DARK_FOREST,
         "情绪×黑暗森林: 恐惧的反向利用",
         "你的恐惧可以反制对方——让猎手也害怕猎物",
         "情绪操控+零和博弈 = 制造对方的恐惧来保护自己",
         "以为恐惧只能被动承受，实则恐惧可以被武器化",
         "最弱者的武器，是让强者害怕失控",
         0.80, "危机反击/谈判策略/不对称博弈"),
        
        (ReverseDimension.SOCIAL_WISDOM, ReverseDimension.REFUTATION,
         "人情世故×反驳: 不反驳的反驳",
         "最高级的反驳不是否定，而是让对方自己否定自己",
         "隐性规则+证伪方法 = 用提问代替否定，用情境代替论据",
         "以为直说才是反驳，在人情世故中暗示才是",
         "最狠的反驳，是让对方自己说出你想要的答案",
         0.78, "高情商沟通/谈判技巧/说服策略"),
        
        (ReverseDimension.REVERSE_ARG, ReverseDimension.SENTIENT,
         "逆向论证×感性: 反转感受的论证力",
         "如果你能让人'感受'到反面，逻辑论证就不再需要",
         "逆向推理+感性共鸣 = 用'感受反转'完成论证",
         "以为逆向论证是逻辑工具，用感性才是最锋利的逆向",
         "让人从'感觉对'变成'感觉不对'，论证完成",
         0.81, "体验设计/品牌反转/认知颠覆"),
        
        (ReverseDimension.DARK_FOREST, ReverseDimension.BEHAVIORAL,
         "黑暗森林×行为学: 可预测的非理性",
         "在黑暗森林中，可预测=可猎杀——认知偏差让你成为靶子",
         "零和博弈+认知偏差 = 你的偏差模式就是你的暴露模式",
         "以为自己在随机应变，实则行为模式可被预测",
         "最致命的不是弱点，是可被预测的弱点",
         0.87, "信息安全/行为风控/对抗博弈"),
        
        (ReverseDimension.DARK_FOREST, ReverseDimension.SOCIAL_WISDOM,
         "黑暗森林×人情世故: 关系即情报",
         "在黑暗森林中，关系网络就是情报网络——朋友越多的猎人越危险",
         "零和博弈+隐性规则 = 关系=信息=权力",
         "以为社交是善意，在博弈中社交是情报收集",
         "最热情的社交者，可能是最危险的情报者",
         0.82, "信息安全/商业情报/社交边界"),
        
        (ReverseDimension.HUMAN_NATURE, ReverseDimension.BEHAVIORAL,
         "人性×行为学: 弱点的科学化利用",
         "人性弱点+行为科学 = 可批量复制的操控方案",
         "趋利本能+认知偏差 = 科学化的'人性弱点利用手册'",
         "以为了解偏差就能避免，了解偏差反而让你更自信地犯错",
         "最了解你的人，不是最爱你的人，是最想利用你的人",
         0.92, "产品设计/增长策略/用户运营"),
    ]
    
    for combo in key_combinations:
        primary, cross, synergy, argument, insight, blind, counter, conf, app = combo
        node = MatrixNode(
            primary=primary,
            cross=cross,
            synergy_type=synergy,
            reverse_argument=argument,
            insight=insight,
            blind_spot_reveal=blind,
            counter_narrative=counter,
            confidence=conf,
            application=app,
        )
        nodes[(primary, cross)] = node
    
    return nodes


# ═══════════════════════════════════════════════════════════════
# 第三层: 推荐引擎主类
# ═══════════════════════════════════════════════════════════════

@dataclass
class ReverseArgumentResult:
    """逆向论证推荐结果"""
    problem: str                                    # 原始问题
    primary_dimension: ReverseDimension             # 主视角维度
    cross_dimension: ReverseDimension               # 交叉审视维度
    reverse_argument: str                           # 逆向论证
    insight: str                                    # 洞察
    blind_spot_reveal: str                          # 盲区揭示
    counter_narrative: str                          # 反叙事
    confidence: float                               # 置信度
    application: str                                # 应用场景
    dimension_profiles: Dict[str, str]              # 两个维度的画像摘要
    reasoning_chain: List[str]                      # 推理链


@dataclass
class MatrixAnalysisResult:
    """矩阵分析完整结果"""
    problem: str
    dominant_dimension: ReverseDimension
    dimension_scores: Dict[ReverseDimension, float] # 各维度关联度
    top_arguments: List[ReverseArgumentResult]       # Top N 逆向论证
    chain_reasoning: List[str]                       # 串联推理链
    meta_insight: str                                # 元洞察
    risk_warning: str                                # 风险警示
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class ReverseArgumentMatrixEngine:
    """
    逆向论证推荐引擎矩阵
    
    8大维度 × 8大维度 = 64交叉论证节点
    串联感性/人性/反驳/人情世故/情绪/逆向论证/黑暗森林/行为学
    
    使用方式:
    1. 输入问题 → 自动识别关联维度
    2. 矩阵交叉计算 → 生成逆向论证推荐
    3. 多维度串联 → 构建完整推理链
    
    Example:
        engine = ReverseArgumentMatrixEngine()
        result = engine.analyze("如何提高团队凝聚力")
        for arg in result.top_arguments[:3]:
            print(arg.reverse_argument)
    """
    
    VERSION = "6.2.0"
    
    def __init__(self):
        self.dimension_profiles = DIMENSION_PROFILES
        self.matrix_nodes = _generate_matrix_nodes()
        self._init_dimension_keywords()
        logger.info(f"逆向论证推荐引擎矩阵 {self.VERSION} 初始化完成")
    
    def _init_dimension_keywords(self):
        """初始化维度关键词映射"""
        self.dimension_keywords: Dict[ReverseDimension, List[str]] = {
            ReverseDimension.SENTIENT: [
                "感觉", "直觉", "感性", "喜欢", "心动", "直觉判断",
                "第一印象", "直觉决策", "好感", "吸引力",
            ],
            ReverseDimension.HUMAN_NATURE: [
                "人性", "弱点", "欲望", "本能", "自私", "贪婪",
                "恐惧", "虚荣", "嫉妒", "利益", "动机",
            ],
            ReverseDimension.REFUTATION: [
                "反驳", "质疑", "证伪", "批判", "辩论", "否定",
                "漏洞", "逻辑", "论证", "反驳论点", "审查",
            ],
            ReverseDimension.SOCIAL_WISDOM: [
                "人情", "世故", "关系", "潜规则", "社交", "圆滑",
                "面子", "情商", "人脉", "圈子", "社交智慧",
            ],
            ReverseDimension.EMOTION: [
                "情绪", "愤怒", "焦虑", "恐惧", "开心", "悲伤",
                "情绪操控", "共情", "同理心", "情绪化", "心态",
            ],
            ReverseDimension.REVERSE_ARG: [
                "逆向", "反直觉", "反面", "倒推", "反转", "逆向思维",
                "逆向论证", "反面教材", "物极必反", "逆推",
            ],
            ReverseDimension.DARK_FOREST: [
                "博弈", "零和", "生存", "黑暗森林", "降维", "猎杀",
                "威慑", "暴露", "防守", "攻击", "对手", "竞争",
            ],
            ReverseDimension.BEHAVIORAL: [
                "行为", "偏差", "助推", "选择", "决策", "认知偏差",
                "理性", "非理性", "习惯", "从众", "锚定", "损失厌恶",
            ],
        }
    
    def analyze(
        self,
        problem: str,
        top_n: int = 5,
        focus_dimensions: Optional[List[ReverseDimension]] = None,
    ) -> MatrixAnalysisResult:
        """
        执行逆向论证矩阵分析
        
        Args:
            problem: 待分析的问题
            top_n: 返回Top N论证
            focus_dimensions: 聚焦维度（可选，默认自动识别）
        
        Returns:
            MatrixAnalysisResult: 完整矩阵分析结果
        """
        # 1. 计算各维度关联度
        dimension_scores = self._calculate_dimension_scores(problem)
        
        # 2. 确定主导维度
        if focus_dimensions:
            dominant = focus_dimensions[0]
        else:
            dominant = max(dimension_scores, key=dimension_scores.get)
        
        # 3. 选择最佳交叉组合
        cross_pairs = self._select_cross_pairs(dimension_scores, focus_dimensions)
        
        # 4. 生成逆向论证推荐
        top_arguments = []
        for primary, cross in cross_pairs[:top_n]:
            node = self.matrix_nodes.get((primary, cross))
            if node:
                result = ReverseArgumentResult(
                    problem=problem,
                    primary_dimension=primary,
                    cross_dimension=cross,
                    reverse_argument=node.reverse_argument,
                    insight=node.insight,
                    blind_spot_reveal=node.blind_spot_reveal,
                    counter_narrative=node.counter_narrative,
                    confidence=node.confidence,
                    application=node.application,
                    dimension_profiles={
                        f"{primary.value}": self.dimension_profiles[primary].core_question,
                        f"{cross.value}": self.dimension_profiles[cross].core_question,
                    },
                    reasoning_chain=self._build_reasoning_chain(primary, cross, problem),
                )
                top_arguments.append(result)
        
        # 5. 构建串联推理链
        chain_reasoning = self._build_full_chain(problem, dimension_scores, top_arguments)
        
        # 6. 生成元洞察
        meta_insight = self._generate_meta_insight(problem, top_arguments)
        
        # 7. 风险警示
        risk_warning = self._generate_risk_warning(dominant, top_arguments)
        
        return MatrixAnalysisResult(
            problem=problem,
            dominant_dimension=dominant,
            dimension_scores=dimension_scores,
            top_arguments=top_arguments,
            chain_reasoning=chain_reasoning,
            meta_insight=meta_insight,
            risk_warning=risk_warning,
        )
    
    def _calculate_dimension_scores(self, problem: str) -> Dict[ReverseDimension, float]:
        """计算问题与各维度的关联度"""
        scores = {}
        problem_lower = problem.lower()
        
        for dim, keywords in self.dimension_keywords.items():
            score = 0.0
            for kw in keywords:
                if kw in problem_lower:
                    score += 1.0
            # 归一化到0-1
            max_possible = len(keywords)
            scores[dim] = min(score / max(max_possible * 0.3, 1.0), 1.0) if score > 0 else 0.1
        
        return scores
    
    def _select_cross_pairs(
        self,
        scores: Dict[ReverseDimension, float],
        focus: Optional[List[ReverseDimension]] = None,
    ) -> List[Tuple[ReverseDimension, ReverseDimension]]:
        """选择最佳交叉组合"""
        # 按关联度排序维度
        sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # 如果有聚焦维度，优先使用
        if focus:
            primary_dims = focus
        else:
            primary_dims = [dim for dim, _ in sorted_dims[:4]]
        
        pairs = []
        # 生成交叉组合并按得分排序
        for i, primary in enumerate(primary_dims):
            for j, (cross, score) in enumerate(sorted_dims):
                if cross != primary and (primary, cross) in self.matrix_nodes:
                    pair_score = scores[primary] * score
                    pairs.append(((primary, cross), pair_score))
        
        # 去重并排序
        pairs.sort(key=lambda x: x[1], reverse=True)
        seen = set()
        result = []
        for pair, _ in pairs:
            if pair not in seen:
                seen.add(pair)
                result.append(pair)
        
        return result
    
    def _build_reasoning_chain(
        self, primary: ReverseDimension, cross: ReverseDimension, problem: str
    ) -> List[str]:
        """构建单条推理链"""
        p = self.dimension_profiles[primary]
        c = self.dimension_profiles[cross]
        
        return [
            f"【{primary.value}视角】{p.core_question}",
            f"→ 正向判断: {p.strength_bias}",
            f"→ 暗面假设: {p.dark_assumption}",
            f"→ 典型谬误: {p.typical_fallacy}",
            f"【{cross.value}逆向审视】{c.reverse_prompt}",
            f"→ 盲区揭示: {c.blind_spot}",
            f"→ 反叙事: {c.counter_narrative}",
        ]
    
    def _build_full_chain(
        self,
        problem: str,
        scores: Dict[ReverseDimension, float],
        arguments: List[ReverseArgumentResult],
    ) -> List[str]:
        """构建完整串联推理链"""
        chain = [
            f"═══ 逆向论证推理链 ═══",
            f"问题: {problem}",
            f"",
        ]
        
        # 第一层: 维度扫描
        chain.append("【第一层: 维度扫描】")
        sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for dim, score in sorted_dims[:4]:
            p = self.dimension_profiles[dim]
            chain.append(f"  {dim.value} (关联度:{score:.1f}) → {p.core_question}")
        chain.append("")
        
        # 第二层: 逆向论证
        chain.append("【第二层: 交叉逆向论证】")
        for i, arg in enumerate(arguments[:3], 1):
            chain.append(f"  {i}. [{arg.primary_dimension.value}×{arg.cross_dimension.value}]")
            chain.append(f"     论证: {arg.reverse_argument}")
            chain.append(f"     盲区: {arg.blind_spot_reveal}")
            chain.append(f"     反叙事: {arg.counter_narrative}")
        chain.append("")
        
        # 第三层: 元洞察
        chain.append("【第三层: 元洞察】")
        if arguments:
            chain.append(f"  → {arguments[0].counter_narrative}")
        
        return chain
    
    def _generate_meta_insight(
        self, problem: str, arguments: List[ReverseArgumentResult]
    ) -> str:
        """生成元洞察"""
        if not arguments:
            return "无足够数据生成元洞察"
        
        # 收集所有反叙事
        counter_narratives = [a.counter_narrative for a in arguments[:3]]
        
        return (
            f"逆向论证矩阵揭示: 关于'{problem[:20]}...'，"
            f"核心盲区在于——{arguments[0].blind_spot_reveal}。"
            f"最深刻的反叙事: {counter_narratives[0]}。"
            f"记住: 所有论证都可能被另一个维度推翻，包括这条元洞察本身。"
        )
    
    def _generate_risk_warning(
        self, dominant: ReverseDimension, arguments: List[ReverseArgumentResult]
    ) -> str:
        """生成风险警示"""
        p = self.dimension_profiles[dominant]
        
        warnings = [
            f"⚠️ 主导维度[{dominant.value}]的固有偏误: {p.strength_bias}",
            f"⚠️ 逆向论证本身的风险: {p.typical_fallacy}",
            "⚠️ 过度使用逆向论证可能导致'为反而反'——逆向是方法，不是目的",
            "⚠️ 矩阵推荐仅供参考，所有逆向论证都应回到事实和逻辑验证",
        ]
        
        return " | ".join(warnings)
    
    def get_dimension_detail(self, dimension: ReverseDimension) -> Dict[str, str]:
        """获取维度详细信息"""
        p = self.dimension_profiles[dimension]
        return {
            "维度": dimension.value,
            "核心追问": p.core_question,
            "逆向审视": p.reverse_prompt,
            "暗面假设": p.dark_assumption,
            "盲区揭示": p.blind_spot,
            "优势偏误": p.strength_bias,
            "典型谬误": p.typical_fallacy,
            "反叙事": p.counter_narrative,
            "来源引擎": ", ".join(p.source_engines),
        }
    
    def get_matrix_summary(self) -> Dict[str, Any]:
        """获取矩阵摘要"""
        return {
            "engine": "逆向论证推荐引擎矩阵",
            "version": self.VERSION,
            "dimensions": len(ReverseDimension),
            "dimension_names": [d.value for d in ReverseDimension],
            "matrix_nodes": len(self.matrix_nodes),
            "theoretical_combinations": len(ReverseDimension) * (len(ReverseDimension) - 1),
        }
    
    def quick_analyze(self, problem: str) -> str:
        """快速分析，返回格式化文本"""
        result = self.analyze(problem, top_n=3)
        
        lines = [
            "═" * 60,
            f"逆向论证推荐引擎矩阵 {self.VERSION}",
            "═" * 60,
            f"",
            f"📋 问题: {result.problem}",
            f"🎯 主导维度: {result.dominant_dimension.value}",
            f"",
        ]
        
        # 维度关联度
        lines.append("【维度关联度】")
        for dim, score in sorted(result.dimension_scores.items(), key=lambda x: x[1], reverse=True)[:4]:
            bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
            lines.append(f"  {dim.value:6s} [{bar}] {score:.2f}")
        lines.append("")
        
        # Top逆向论证
        for i, arg in enumerate(result.top_arguments, 1):
            lines.append(f"【逆向论证 {i}: {arg.primary_dimension.value} × {arg.cross_dimension.value}】")
            lines.append(f"  💡 论证: {arg.reverse_argument}")
            lines.append(f"  🔍 洞察: {arg.insight}")
            lines.append(f"  👁 盲区: {arg.blind_spot_reveal}")
            lines.append(f"  🔄 反叙事: {arg.counter_narrative}")
            lines.append(f"  📊 置信度: {arg.confidence:.0%}")
            lines.append(f"  🎯 应用: {arg.application}")
            lines.append("")
        
        # 元洞察
        lines.append("【元洞察】")
        lines.append(f"  {result.meta_insight}")
        lines.append("")
        
        # 风险警示
        lines.append("【风险警示】")
        lines.append(f"  {result.risk_warning}")
        lines.append("")
        lines.append("═" * 60)
        
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 全局单例与便捷函数
# ═══════════════════════════════════════════════════════════════

_engine_instance: Optional[ReverseArgumentMatrixEngine] = None


def get_reverse_argument_matrix() -> ReverseArgumentMatrixEngine:
    """获取逆向论证矩阵引擎单例"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = ReverseArgumentMatrixEngine()
    return _engine_instance


def quick_reverse_analyze(problem: str) -> str:
    """便捷函数: 快速逆向论证分析"""
    engine = get_reverse_argument_matrix()
    return engine.quick_analyze(problem)


def reverse_argument_recommend(
    problem: str,
    focus_dimensions: Optional[List[str]] = None,
    top_n: int = 5,
) -> MatrixAnalysisResult:
    """
    便捷函数: 逆向论证推荐
    
    Args:
        problem: 待分析问题
        focus_dimensions: 聚焦维度名称列表 (如 ["感性", "人性"])
        top_n: 返回Top N
    
    Returns:
        MatrixAnalysisResult
    """
    engine = get_reverse_argument_matrix()
    
    # 转换维度名称
    dims = None
    if focus_dimensions:
        dim_map = {d.value: d for d in ReverseDimension}
        dims = [dim_map[name] for name in focus_dimensions if name in dim_map]
    
    return engine.analyze(problem, top_n=top_n, focus_dimensions=dims)


__all__ = [
    'ReverseArgumentMatrixEngine',
    'ReverseDimension',
    'DimensionProfile',
    'MatrixNode',
    'ReverseArgumentResult',
    'MatrixAnalysisResult',
    'DIMENSION_PROFILES',
    'get_reverse_argument_matrix',
    'quick_reverse_analyze',
    'reverse_argument_recommend',
]
