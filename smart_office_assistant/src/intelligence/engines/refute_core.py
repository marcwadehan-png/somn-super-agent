# -*- coding: utf-8 -*-
"""
驳心引擎 (RefuteCore) S1.0
Reverse Argument & Refutation Intelligence Engine

以反驳为核心驱动的论证智慧引擎。
串联 感性/人性/反驳/人情世故/情绪/逆向论证/黑暗森林/行为学 8大维度，
实现完整的论证解析 → 反驳生成 → 漏洞检测 → 辩论对抗 → 论证修复 → 解决方案输出。

v3.0.1 优化 (核心质量修复):
1. 修复强度评分公式 — 从"几乎全F/D"调整为合理分布(D/B为主)
2. 修复反驳强度计算 — 从100%满分调整为80-90%有区分度
3. 修复SPO主谓宾解析 — 过滤代词前缀，提取有意义的实体主语
4. 修复批量矛盾检测 — 5层检测(直接否定/主体冲突/否定重叠/关键词态度/假设互斥)
5. 重构辩论进化机制 — 3轮递进深化，真正推动论点演进
6. 修复维度亲和力计算 — 对数缩放归一化替代错误公式
7. 修复前提提取 — 支持无后续连接词的因果句
8. 重构策略base值 — 扩展范围至0.65-0.85确保区分度
9. 智能策略选择 — 基于维度亲和力动态选择策略

v3.0.2 优化 (鲁棒性+输出质量):
10. 修复测试版本号断言 v3.0.0 → v3.0.1
11. 修复_absurd()缺少return兜底 + 扩充归谬规则(是/需要)
12. 空输入/极短文本防护 — parse()和refute()入口校验
13. _extract_core_claim_v2空句子防护
14. _detect_attitude改进 — 长词优先匹配避免"不"字误判
15. _fill_template_v2领域覆盖扩充 — 新增8个领域完整填充字典
16. _gen_evidence_v2/_pc_evidence/_counterexample领域扩充
17. Markdown输出增加截断保护(tr/safe_join)
18. refute()方法异常输入防护

v3.0.3 优化 (代码质量+确定性):
19. 修复_find_contradictions层级5缺break — 同一矛盾对不再重复报告
20. 重构_detect_attitude — 消除海象运算符，提高可读性和正确性
21. 修复双重惩罚 — assess()和_assess_reasoning()不再重复惩罚反驳强度
22. 修复_hedge_claim — 用字符串长度替代hash()，确保跨进程确定性

v3.0.4 优化 (A/B测试驱动):
23. 修复领域识别 — 个人决策扩充关键词(辞职/创业/梦想/追求/转型)
24. 修复领域识别 — 人际社交扩充关键词(朋友/友情/义气/人情/借钱)
25. 修复_detect_attitude — '问题'改为上下文敏感(只在'有问题'时算负面)

v3.2.0 性能与内存优化:
32. 预编译正则常量池 — 28处内联re.xxx改为模块级re.compile()常量
33. 局部字典提升为类常量 — keyword_assumptions/type_assumptions/domain_assumptions/evidence_types不再每次调用重建
34. domain_fills+generic_fills提升为RefutationStrategist类常量 — ~180行数据只构建一次
35. 消除代码重复 — _soften_claim和_repair_claim共享ArgumentParser.SOFTEN_MAP
36. 版本: v3.2.0

版本: v3.2.0
日期: 2026-04-28
"""

import logging
import re
import time
import hashlib
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# v3.2.0: 预编译正则常量池 — 避免每次调用重复编译
# ═══════════════════════════════════════════════════════════════
_RE_SPLIT_SENTENCE = re.compile(r'[。！？]')
_RE_SPLIT_SEMICOLON = re.compile(r'[；]')
_RE_SPLIT_COMMA = re.compile(r'[，,]')
_RE_CHINESE_SHORT = re.compile(r'[\u4e00-\u9fff]{2,4}')
_RE_CHINESE_MID = re.compile(r'[\u4e00-\u9fff]{2,5}')
_RE_CHINESE_LONG = re.compile(r'[\u4e00-\u9fff]{2,8}')
_RE_CHINESE_WORD_BOUNDARY = re.compile(r'([\u4e00-\u9fff]{2,4})(?:是|的|了|着|过|和|与|或)')
_RE_CHINESE_WORD_BOUNDARY_REV = re.compile(r'(?:是|的|了|着|过|和|与|或)([\u4e00-\u9fff]{2,4})')
_RE_NUMBER_SUFFIX = re.compile(r'\d+[%年月日倍万]')
_RE_PRONOUN_PREFIX = [
    re.compile(r'^(我们|我|你|他|她|它|他们|它们|大家|所有人|人们)\s*'),
    re.compile(r'^(也|都|就|还|又|才|已|正|将|最|很|太)\s*'),
]
_RE_PREDICATE_PATTERNS = [
    re.compile(r'(应该|必须|需要|导致|造成|使得|引起|带来|意味着|说明|证明)'),
    re.compile(r'(可以|能够|将会|可能|必然|势必|建议|推荐|决定)'),
    re.compile(r'(是|有|会|能)'),
]
_RE_NOUN_ENTITY = [
    re.compile(r'([\u4e00-\u9fff]{2,8}(?:公司|团队|项目|产品|市场|用户|企业|系统|技术|方案|策略|方法|模式|平台|品牌|降价|竞争))'),
    re.compile(r'([\u4e00-\u9fff]{2,6})(?:的)'),
]
_RE_STOP_WORDS_CLEAN = re.compile(r'[的了着过很非常更加最为确实一定必然大概]')
_RE_CLAIM_CLEAN_PREFIX = re.compile(r'^(修正:\s*|限定:\s*|最终版:\s*)+')
_RE_CLAIM_CLEAN_SUFFIXES = [
    re.compile(r'（[^）]*重新论证[^）]*）$'),
    re.compile(r'（[^）]*补充证据[^）]*）$'),
    re.compile(r'（[^）]*限定条件[^）]*）$'),
]
_RE_OBJ_PREFIX = re.compile(r'^[的了着过很非常更加最为确实一定必然大概]')
_RE_TEMPLATE_PLACEHOLDER = re.compile(r'\{(\w+)\}')
_RE_TEMPLATE_REMAINDER = re.compile(r'\{(\w+)\}')
_RE_HASTY_GENERALIZATION = re.compile(r'所有|一切|全部|从不|永远|必然')
_RE_FALSE_DILEMMA = re.compile(r'要么|非此即彼|只有两种')
_RE_NEUTRAL_NOT = re.compile(r'不同|不仅|不断|不如|不过')
_RE_CASUAL_FULL = [
    (re.compile(r'因为(.+?)(所以|因此|从而|使得)'), 1),
    (re.compile(r'由于(.+?)(导致|造成|使得|引起)'), 1),
    (re.compile(r'既然(.+?)(那么|就|则)'), 1),
]
_RE_CASUAL_SHORT_BECAUSE = [re.compile(r'因为(.+?)$'), re.compile(r'因为(.+?)[，。！？]')]
_RE_CASUAL_SHORT_DUE = [re.compile(r'由于(.+?)$'), re.compile(r'由于(.+?)[，。！？]')]
_RE_CONDITIONAL = [
    (re.compile(r'如果(.+?)(那么|就|则|会)'), 1),
    (re.compile(r'只要(.+?)(就|便|则)'), 1),
    (re.compile(r'只有(.+?)(才|方)'), 1),
]
_RE_EVIDENCE = [re.compile(r'数据显示(.+?)[。，]'), re.compile(r'研究表明(.+?)[。，]'),
                re.compile(r'统计(.+?)[。，]'), re.compile(r'调查(.+?)[。，]')]
_RE_KEYWORD_BOUNDARY = [
    re.compile(r'([\u4e00-\u9fff]{2,4})(?:是|的|了|着|过|和|与|或)'),
    re.compile(r'(?:是|的|了|着|过|和|与|或)([\u4e00-\u9fff]{2,4})'),
]


# ═══════════════════════════════════════════════════════════════
# 第一层: 枚举与核心数据结构
# ═══════════════════════════════════════════════════════════════

class RefuteDimension(Enum):
    """驳心8大维度"""
    SENTIENT = "感性"
    HUMAN_NATURE = "人性"
    REFUTATION = "反驳"
    SOCIAL_WISDOM = "人情世故"
    EMOTION = "情绪"
    REVERSE_ARG = "逆向论证"
    DARK_FOREST = "黑暗森林"
    BEHAVIORAL = "行为学"


class ArgumentType(Enum):
    """论证类型"""
    PROPOSITION = "命题"
    DECISION = "决策"
    PREDICTION = "预测"
    CAUSAL = "因果"
    VALUE = "价值判断"
    STRATEGY = "策略"
    MIXED = "混合"


class FallacyType(Enum):
    """逻辑谬误类型"""
    AD_HOMINEM = "人身攻击"
    STRAW_MAN = "稻草人"
    FALSE_DILEMMA = "虚假二难"
    SLIPPERY_SLOPE = "滑坡谬误"
    CIRCULAR = "循环论证"
    APPEAL_AUTHORITY = "诉诸权威"
    HASTY_GENERALIZATION = "以偏概全"
    CONFIRMATION_BIAS = "确认偏误"
    EMOTIONAL_APPEAL = "诉诸情感"
    POST_HOC = "事后归因"
    SURVIVOR_BIAS = "幸存者偏差"
    SUNK_COST = "沉没成本"


class DebateRole(Enum):
    """辩论角色"""
    PROPOSER = "正方"
    REFUTER = "反方"
    JUDGE = "裁判"


# ═══════════════════════════════════════════════════════════════
# 第二层: 论证解析器 (ArgumentParser) — v3.0 增强版
# ═══════════════════════════════════════════════════════════════

@dataclass
class ParsedArgument:
    """解析后的论证结构 v3.0"""
    raw_text: str
    argument_type: ArgumentType
    core_claim: str
    premises: List[str]
    reasoning_chain: List[str]
    implicit_assumptions: List[str]
    evidence_type: str
    confidence_level: float
    dimension_affinity: Dict[RefuteDimension, float]
    keywords: List[str]
    vulnerability_score: float
    # v3.0 新增字段
    claim_subject: str
    claim_predicate: str
    claim_object: str
    negated_claim: str
    context_domain: str
    strength_indicators: List[str]
    weakness_indicators: List[str]


class ArgumentParser:
    """
    论证解析器 v3.0
    
    增强:
    - 中文智能分句（区分层次）
    - 核心主张精准提取（结论词定位+主张指示词）
    - 主谓宾拆解（SPO结构）
    - 隐含假设上下文推断（领域+论点类型+关键词三重推断）
    - 否定主张自动构造
    - 领域识别
    - 强度/弱点指示词检测
    """
    
    TYPE_PATTERNS = {
        ArgumentType.PROPOSITION: [
            r"是", r"不是", r"等于", r"意味着", r"本质", r"核心",
            r"关键", r"根本", r"其实",
        ],
        ArgumentType.DECISION: [
            r"应该", r"必须", r"需要", r"决定", r"选择", r"最好",
            r"建议", r"推荐", r"计划", r"打算",
        ],
        ArgumentType.PREDICTION: [
            r"将会", r"可能", r"预计", r"趋势", r"未来", r"必然",
            r"势必", r"大概率",
        ],
        ArgumentType.CAUSAL: [
            r"因为", r"导致", r"由于", r"造成", r"使得", r"引起",
            r"所以", r"因此", r"从而",
        ],
        ArgumentType.VALUE: [
            r"好", r"坏", r"对", r"错", r"值得", r"重要", r"正确",
            r"应该", r"不该", r"合理", r"不合理",
        ],
        ArgumentType.STRATEGY: [
            r"如何", r"怎么", r"策略", r"方案", r"方法", r"路径",
            r"方式", r"手段", r"步骤",
        ],
    }
    
    DIMENSION_KEYWORDS: Dict[RefuteDimension, List[str]] = {
        RefuteDimension.SENTIENT: [
            "感觉", "直觉", "感性", "喜欢", "心动", "第一印象",
            "好感", "吸引力", "本能反应", "共感",
        ],
        RefuteDimension.HUMAN_NATURE: [
            "人性", "弱点", "欲望", "本能", "自私", "贪婪",
            "恐惧", "虚荣", "嫉妒", "利益", "动机", "趋利",
        ],
        RefuteDimension.REFUTATION: [
            "反驳", "质疑", "证伪", "批判", "辩论", "否定",
            "漏洞", "逻辑", "论证", "审查", "推翻",
        ],
        RefuteDimension.SOCIAL_WISDOM: [
            "人情", "世故", "关系", "潜规则", "社交", "圆滑",
            "面子", "情商", "人脉", "圈子", "默契",
        ],
        RefuteDimension.EMOTION: [
            "情绪", "愤怒", "焦虑", "恐惧", "开心", "悲伤",
            "操控", "共情", "同理心", "心态", "冲动",
        ],
        RefuteDimension.REVERSE_ARG: [
            "逆向", "反直觉", "反面", "倒推", "反转", "逆向思维",
            "物极必反", "逆推", "颠覆", "反转逻辑",
        ],
        RefuteDimension.DARK_FOREST: [
            "博弈", "零和", "生存", "黑暗森林", "降维", "猎杀",
            "威慑", "暴露", "对手", "竞争", "攻防",
        ],
        RefuteDimension.BEHAVIORAL: [
            "行为", "偏差", "助推", "选择", "决策", "认知偏差",
            "理性", "非理性", "从众", "锚定", "损失厌恶",
        ],
    }

    DOMAIN_PATTERNS = {
        "投资理财": ["投资", "收益", "风险", "回报", "股票", "基金", "市场", "资产", "理财", "涨跌"],
        "企业管理": ["团队", "管理", "战略", "组织", "绩效", "KPI", "领导", "员工", "文化", "流程"],
        "市场营销": ["用户", "营销", "品牌", "流量", "转化", "增长", "获客", "留存", "推广", "渠道"],
        "产品开发": ["产品", "需求", "功能", "体验", "迭代", "设计", "开发", "上线", "反馈", "MVP"],
        "个人决策": ["选择", "职业", "人生", "规划", "机会", "放弃", "坚持", "改变", "成长", "方向", "辞职", "创业", "梦想", "追求", "转型"],
        "技术选型": ["技术", "架构", "框架", "性能", "扩展", "稳定", "方案", "实现", "部署", "运维", "语言", "Go", "Python", "Java", "后端", "前端", "数据库"],
        "商业竞争": ["竞争", "对手", "份额", "定价", "差异化", "壁垒", "优势", "护城河", "领先", "垄断"],
        "人际社交": ["关系", "沟通", "合作", "信任", "利益", "冲突", "妥协", "边界", "期望", "承诺", "朋友", "友情", "义气", "人情", "借钱"],
    }

    STRENGTH_INDICATORS = {
        "强": ["必然", "一定", "绝对", "毫无疑问", "确实", "证明", "验证", "数据表明", "统计显示"],
        "中": ["可能", "大概", "也许", "倾向于", "应该是", "大概率", "通常", "往往"],
        "弱": ["感觉", "好像", "似乎", "也许吧", "不确定", "说不清", "直觉"],
    }

    WEAKNESS_INDICATORS = [
        "一定", "必然", "绝对", "不可能", "所有人都", "永远", "从不",
        "必须", "只能", "大家都知道", "显然", "当然", "毫无疑问",
        "简直", "太", "过分", "受不了", "气死",
    ]

    # v3.2.0: 从方法内局部字典提升为类常量，避免每次调用重建
    KEYWORD_ASSUMPTIONS = {
        "应该": "假设存在一个'应该'的标准，且此标准普遍适用",
        "必须": "假设没有其他替代方案，且当前路径唯一可行解",
        "因为": "假设因果关联确定（而非仅仅是相关性）",
        "所有": "假设不存在任何例外情况",
        "必然": "假设不存在其他可能性，确定性100%",
        "显然": "假设结论不证自明，无需验证（但'显然'常掩盖漏洞）",
        "大家都知道": "假设多数人认知=事实（从众谬误）",
        "一直以来": "假设过去规律未来也成立（归纳问题）",
        "专家说": "假设专家在该问题上不会出错且无利益冲突",
        "数据显示": "假设数据采集客观、样本有代表性、解读无偏",
        "肯定": "假设确定性成立，'肯定'往往意味过度自信",
        "只要": "假设条件充分且唯一，无其他隐性约束",
    }

    TYPE_ASSUMPTIONS = {
        ArgumentType.CAUSAL: "假设A→B因果链中无中间变量干扰（无混淆变量）",
        ArgumentType.PREDICTION: "假设未来延续过去趋势（趋势外推假设）",
        ArgumentType.DECISION: "假设决策信息充分且可选方案已穷举",
        ArgumentType.VALUE: "假设存在客观的价值评判标准",
        ArgumentType.STRATEGY: "假设执行环境稳定且资源充足",
        ArgumentType.PROPOSITION: "假设命题定义明确无歧义",
    }

    DOMAIN_ASSUMPTIONS = {
        "投资理财": ["假设过去收益预测未来表现", "假设风险可量化可控"],
        "企业管理": ["假设组织行为与个体行为一致", "假设管理效果可线性归因"],
        "市场营销": ["假设用户行为理性可预测", "假设市场环境相对稳定"],
        "商业竞争": ["假设竞争格局不变", "假设对手行为可预测"],
        "个人决策": ["假设个人偏好稳定自洽", "假设决策信息足够支撑"],
        "技术选型": ["假设技术成熟度足够", "假设团队能力匹配"],
        "人际社交": ["假设对方意图可正确解读", "假设承诺会被遵守"],
    }

    EVIDENCE_TYPES = {
        "数据证据": [r"数据", r"统计", r"数字", r"%", r"比例"],
        "案例证据": [r"案例", r"例子", r"比如", r"如", r"例如"],
        "权威证据": [r"专家", r"研究", r"论文", r"报告", r"权威"],
        "经验证据": [r"经验", r"实践", r"亲历", r"感受", r"体会"],
        "逻辑证据": [r"因此", r"所以", r"推论", r"必然", r"逻辑"],
    }

    # v3.2.0: 共享的软化/修复替换映射（消除_debate_soften和_repair_claim重复）
    SOFTEN_MAP = {"一定":"很可能", "必然":"大概率", "绝对":"在很大程度上",
                  "不可能":"不太可能", "所有人都":"大多数", "永远":"长期来看",
                  "从不":"很少", "必须":"建议", "只能":"优先考虑"}

    def parse(self, text: str) -> ParsedArgument:
        # v3.0.2: 输入防护 — 空值/极短/非字符串
        if not text or not isinstance(text, str):
            text = "未提供有效论点"
        text = text.strip()
        if len(text) < 3:
            text = f"论点内容过短: {text}"
        
        arg_type = self._identify_argument_type(text)
        sentences = self._smart_split(text)
        core_claim = self._extract_core_claim_v2(text, sentences)
        subject, predicate, obj = self._extract_spo(core_claim)
        premises = self._extract_premises_v2(text, sentences)
        reasoning_chain = self._build_reasoning_chain(text, premises, core_claim)
        implicit_assumptions = self._infer_implicit_assumptions_v2(
            text, premises, core_claim, arg_type
        )
        evidence_type = self._identify_evidence_type(text)
        dimension_affinity = self._calculate_dimension_affinity(text)
        keywords = self._extract_keywords_v2(text)
        context_domain = self._identify_domain(text)
        strength_indicators = self._find_strength_indicators(text)
        weakness_indicators = self._find_weakness_indicators(text)
        negated_claim = self._construct_negation(core_claim, arg_type)
        vulnerability = self._assess_vulnerability_v2(
            text, premises, implicit_assumptions, weakness_indicators
        )
        confidence = 1.0 - vulnerability
        
        return ParsedArgument(
            raw_text=text,
            argument_type=arg_type,
            core_claim=core_claim,
            premises=premises,
            reasoning_chain=reasoning_chain,
            implicit_assumptions=implicit_assumptions,
            evidence_type=evidence_type,
            confidence_level=confidence,
            dimension_affinity=dimension_affinity,
            keywords=keywords,
            vulnerability_score=vulnerability,
            claim_subject=subject,
            claim_predicate=predicate,
            claim_object=obj,
            negated_claim=negated_claim,
            context_domain=context_domain,
            strength_indicators=strength_indicators,
            weakness_indicators=weakness_indicators,
        )
    
    def _smart_split(self, text: str) -> List[str]:
        """智能中文分句"""
        main_sentences = _RE_SPLIT_SENTENCE.split(text)
        result = []
        
        for main in main_sentences:
            main = main.strip()
            if not main:
                continue
            sub_sentences = _RE_SPLIT_SEMICOLON.split(main)
            for sub in sub_sentences:
                sub = sub.strip()
                if not sub:
                    continue
                comma_parts = _RE_SPLIT_COMMA.split(sub)
                if len(comma_parts) <= 2:
                    result.append(sub)
                else:
                    i = 0
                    while i < len(comma_parts):
                        part = comma_parts[i].strip()
                        if not part:
                            i += 1
                            continue
                        if i + 1 < len(comma_parts):
                            combined = f"{part}，{comma_parts[i + 1].strip()}"
                            if self._is_logical_unit(combined):
                                result.append(combined)
                                i += 2
                                continue
                        result.append(part)
                        i += 1
        return [s for s in result if len(s) > 2]

    def _is_logical_unit(self, text: str) -> bool:
        logical_connectors = ["因为", "所以", "如果", "那么", "虽然", "但是", "只要", "就", "由于", "因此"]
        return any(c in text for c in logical_connectors)

    def _extract_core_claim_v2(self, text: str, sentences: List[str]) -> str:
        """精准提取核心主张"""
        if not sentences:
            return text[:50] if len(text) > 2 else text
        
        # 结论性句子优先
        conclusion_indicators = [
            "所以", "因此", "总之", "综上", "最终", "结论是", "这意味着",
            "由此可见", "不难看出", "显然", "说明", "足以证明",
        ]
        for indicator in conclusion_indicators:
            for s in reversed(sentences):
                if indicator in s:
                    idx = s.index(indicator) + len(indicator)
                    claim = s[idx:].strip()
                    if len(claim) > 3:
                        return claim
                    return s
        
        # 主张指示词
        claim_indicators = [
            "应该", "必须", "是", "不是", "意味着", "关键", "核心",
            "根本", "本质", "其实", "需要", "最好", "决定",
        ]
        for indicator in claim_indicators:
            for s in sentences:
                if indicator in s:
                    return s
        
        best = sentences[0]
        for s in sentences:
            has_claim_verb = any(v in s for v in ["是", "有", "会", "能", "应该", "需要", "导致"])
            if has_claim_verb and len(s) > len(best):
                best = s
        return best

    def _extract_spo(self, claim: str) -> Tuple[str, str, str]:
        """v3.0.2: 重构主谓宾拆解 — 修复代词/助词主语、谓语混入主语等问题"""
        subject = ""
        predicate = ""
        obj = ""
        
        # ─── 预处理: 去掉无意义的代词/副词前缀 ───
        # "我们也必须降价" → "必须降价"
        # "所有人都应该努力" → "应该努力"
        cleaned = claim
        for pp in _RE_PRONOUN_PREFIX:
            cleaned = pp.sub('', cleaned).strip()
        # 重复清理（"我们也" → 先清"也"再清"我们"或反过来）
        for pp in _RE_PRONOUN_PREFIX:
            cleaned = pp.sub('', cleaned).strip()
        
        if not cleaned or len(cleaned) < 2:
            cleaned = claim
        
        # ─── 停用词 — 不作为主语 ───
        stop_words = {"我们","我","你","他","她","它","他们","它们","这","那",
                      "也","都","不","没","很","太","最","已","正","将",
                      "应该","必须","需要","可以","能够","会","能","是"}
        
        # ─── v3.0.2: 先提取谓语，再从谓语前提取主语 ───
        # 谓语动词（按优先级匹配）
        predicate = ""
        for p in _RE_PREDICATE_PATTERNS:
            m = p.search(cleaned)
            if m:
                predicate = m.group(1)
                break
        
        # ─── 从谓语位置分割出主语和宾语 ───
        if predicate and predicate in cleaned:
            pre_pred = cleaned[:cleaned.index(predicate)].strip()
            post_pred = cleaned[cleaned.index(predicate) + len(predicate):].strip()
        else:
            pre_pred = ""
            post_pred = cleaned
        
        # ─── 提取主语（谓语前的实体词） ───
        if pre_pred:
            # 优先匹配已知的实体词模式
            for p in _RE_NOUN_ENTITY:
                m = p.search(pre_pred)
                if m:
                    candidate = m.group(1).strip()
                    if candidate and candidate not in stop_words and len(candidate) >= 2:
                        subject = candidate
                        break
            
            # 兜底: 谓语前的所有非停用词中文字符
            if not subject or subject in stop_words:
                chars = _RE_CHINESE_LONG.findall(pre_pred)
                for w in chars:
                    if w not in stop_words and len(w) >= 2:
                        subject = w
                        break
            
            # 最后兜底: 取谓语前2-4字
            if not subject or subject in stop_words:
                c = _RE_STOP_WORDS_CLEAN.sub('', pre_pred).strip()
                if len(c) >= 2:
                    subject = c[:min(6, len(c))]
        
        # 如果没有谓语或谓语前为空，用原始claim提取实体词
        if not subject or subject in stop_words:
            # 尝试在原始claim上找实体词
            entity_words = [
                "竞争对手", "市场份额", "投资回报", "团队绩效", "KPI考核",
                "价格战", "品牌价值", "用户体验", "产品迭代", "降价策略",
                "管理方案", "市场竞争", "风险收益", "核心团队", "行业趋势",
                "MVP", "先发优势", "技术架构", "后端性能",
            ]
            for ew in entity_words:
                if ew in claim:
                    subject = ew
                    break
        
        # 最终兜底
        if not subject or subject in stop_words:
            context_words = _RE_CHINESE_MID.findall(claim)
            for w in context_words:
                if w not in stop_words and len(w) >= 2:
                    subject = w
                    break
            if not subject:
                subject = claim[:min(4, len(claim))]
        
        # ─── 提取宾语 ───
        if post_pred:
            obj = _RE_OBJ_PREFIX.sub("", post_pred).strip()
        
        # ─── 后处理 ───
        if not predicate: predicate = "是"
        if not obj: 
            if predicate != "是" and predicate in claim:
                obj = claim[claim.index(predicate) + len(predicate):].strip()
            else:
                obj = ""
        
        return subject, predicate, obj

    def _extract_premises_v2(self, text: str, sentences: List[str]) -> List[str]:
        """v3.0.1: 增强版前提提取 — 修复无后置连接词的因果句"""
        premises = []
        
        # 因果模式（带后续连接词的完整因果句）
        for pattern, group in _RE_CASUAL_FULL:
            matches = pattern.findall(text)
            premises.extend([m[group - 1].strip() for m in matches if m[group - 1].strip()])
        
        # v3.0.1: 无后续连接词的因果句 — "因为X"（没有所以Y）
        if "因为" in text and not any(kw in text for kw in ["所以", "因此", "从而", "使得"]):
            cause_match = _RE_CASUAL_SHORT_BECAUSE[0].search(text)
            if not cause_match:
                cause_match = _RE_CASUAL_SHORT_BECAUSE[1].search(text)
            if cause_match:
                cause_text = cause_match.group(1).strip()
                if cause_text and len(cause_text) > 2:
                    premises.append(cause_text)
        
        if "由于" in text and not any(kw in text for kw in ["导致", "造成", "使得", "引起"]):
            cause_match = _RE_CASUAL_SHORT_DUE[0].search(text)
            if not cause_match:
                cause_match = _RE_CASUAL_SHORT_DUE[1].search(text)
            if cause_match:
                cause_text = cause_match.group(1).strip()
                if cause_text and len(cause_text) > 2:
                    premises.append(cause_text)
        
        for pattern, group in _RE_CONDITIONAL:
            matches = pattern.findall(text)
            premises.extend([m[group - 1].strip() for m in matches if m[group - 1].strip()])
        
        for pattern in _RE_EVIDENCE:
            matches = pattern.findall(text)
            premises.extend([m.strip() for m in matches if m.strip()])
        
        if not premises and sentences:
            for s in sentences:
                if any(c in s for c in ["所以", "因此", "总之", "应该", "必须"]):
                    continue
                if len(s) > 5:
                    premises.append(s)
                    if len(premises) >= 4:
                        break
        return premises[:5]

    def _infer_implicit_assumptions_v2(self, text: str, premises: List[str], core_claim: str, arg_type: ArgumentType) -> List[str]:
        """上下文感知隐含假设推断"""
        assumptions = []
        
        # v3.2.0: 使用类常量替代方法内局部字典
        for kw, assumption in self.KEYWORD_ASSUMPTIONS.items():
            if kw in text:
                assumptions.append(assumption)
        
        if arg_type in self.TYPE_ASSUMPTIONS:
            assumptions.append(self.TYPE_ASSUMPTIONS[arg_type])
        
        domain = self._identify_domain(text)
        if domain in self.DOMAIN_ASSUMPTIONS:
            assumptions.extend(self.DOMAIN_ASSUMPTIONS[domain])
        
        seen = set(); unique = []
        for a in assumptions:
            if a not in seen:
                seen.add(a); unique.append(a)
        return unique[:6]

    def _identify_domain(self, text: str) -> str:
        domain_scores: Dict[str, int] = defaultdict(int)
        for domain, keywords in self.DOMAIN_PATTERNS.items():
            for kw in keywords:
                if kw in text:
                    domain_scores[domain] += 1
        return max(domain_scores, key=domain_scores.get) if domain_scores else "通用"

    def _construct_negation(self, core_claim: str, arg_type: ArgumentType) -> str:
        negation_rules = {
            "应该": "不应该", "必须": "不必须/并非必须", "是": "不是",
            "不是": "是", "会": "不会", "能": "不能", "需要": "不需要",
            "导致": "不导致/不一定是原因", "意味着": "不意味着",
            "好": "不好", "对": "不对", "值得": "不值得", "重要": "不重要", "正确": "不正确",
        }
        negated = core_claim
        for positive, negative in negation_rules.items():
            if positive in core_claim:
                negated = core_claim.replace(positive, negative, 1); break
        else:
            if arg_type == ArgumentType.PROPOSITION:
                negated = f"并非{core_claim}"
            elif arg_type == ArgumentType.DECISION:
                negated = f"不应该{core_claim}"
            elif arg_type == ArgumentType.PREDICTION:
                negated = f"不一定{core_claim}"
            else:
                negated = f"反面: {core_claim}"
        return negated

    def _find_strength_indicators(self, text: str) -> List[str]:
        found = []
        for level, indicators in self.STRENGTH_INDICATORS.items():
            for ind in indicators:
                if ind in text:
                    found.append(f"[{level}]{ind}")
        return found[:8]

    def _find_weakness_indicators(self, text: str) -> List[str]:
        return [w for w in self.WEAKNESS_INDICATORS if w in text][:8]

    def _identify_argument_type(self, text: str) -> ArgumentType:
        type_scores: Dict[ArgumentType, int] = defaultdict(int)
        for arg_type, patterns in self.TYPE_PATTERNS.items():
            for pattern in patterns:
                type_scores[arg_type] += len(re.findall(pattern, text))
        if not type_scores or max(type_scores.values()) == 0:
            return ArgumentType.MIXED
        primary = max(type_scores, key=type_scores.get)
        sorted_scores = sorted(type_scores.values(), reverse=True)
        if len(sorted_scores) >= 2 and sorted_scores[0] > 0 and sorted_scores[1] / max(sorted_scores[0], 1) > 0.7:
            return ArgumentType.MIXED
        return primary

    def _identify_evidence_type(self, text: str) -> str:
        # v3.2.0: 使用类常量替代方法内局部字典
        scores = {}
        for etype, patterns in self.EVIDENCE_TYPES.items():
            score = sum(len(re.findall(p, text)) for p in patterns)
            scores[etype] = score
        if not scores or max(scores.values()) == 0:
            return "无明确证据"
        return max(scores, key=scores.get)

    def _calculate_dimension_affinity(self, text: str) -> Dict[RefuteDimension, float]:
        """v3.0.1: 修复维度亲和力计算 — 使用合理的归一化"""
        affinity = {}
        text_lower = text.lower()
        for dim, keywords in self.DIMENSION_KEYWORDS.items():
            match_count = sum(1 for kw in keywords if kw in text_lower)
            # 使用对数缩放: match_count=0→0.03, 1→0.25, 2→0.40, 3→0.50, 5+→0.60~0.70
            if match_count == 0:
                affinity[dim] = 0.03  # 基础低亲和力，而非0
            elif match_count == 1:
                affinity[dim] = 0.25
            elif match_count == 2:
                affinity[dim] = 0.40
            elif match_count == 3:
                affinity[dim] = 0.50
            else:
                affinity[dim] = min(0.50 + (match_count - 3) * 0.05, 0.75)
        return affinity

    def _extract_keywords_v2(self, text: str) -> List[str]:
        found = []
        for keywords in self.DIMENSION_KEYWORDS.values():
            found.extend([kw for kw in keywords if kw in text])
        for dk in self.DOMAIN_PATTERNS.values():
            found.extend([kw for kw in dk if kw in text])
        additional_patterns = _RE_KEYWORD_BOUNDARY
        for pattern in additional_patterns:
            found.extend(pattern.findall(text)[:5])
        number_patterns = _RE_NUMBER_SUFFIX.findall(text)
        found.extend(number_patterns)
        return list(dict.fromkeys(found))[:15]

    def _build_reasoning_chain(self, text: str, premises: List[str], core_claim: str) -> List[str]:
        chain = []
        if premises:
            for i, premise in enumerate(premises, 1):
                chain.append(f"前提{i}: {premise}")
            chain.append("═══ 推理 ═══")
        chain.append(f"结论: {core_claim}")
        return chain

    def _assess_vulnerability_v2(self, text: str, premises: List[str], assumptions: List[str], weaknesses: List[str]) -> float:
        score = 0.0
        if len(premises) == 0: score += 0.3
        elif len(premises) == 1: score += 0.15
        score += len(assumptions) * 0.06
        score += len(weaknesses) * 0.08
        if "数据" not in text and "研究" not in text and "统计" not in text:
            score += 0.1
        if "因为" in text and "所以" in text:
            cause = text.split("因为")[-1].split("所以")[0] if "因为" in text else ""
            if len(cause) < 8: score += 0.1
        if len(text) < 15: score += 0.15
        return min(score, 1.0)


# ═══════════════════════════════════════════════════════════════
# 第三层: 8大反驳策略引擎 (RefutationStrategist) — v3.0 智能填充
# ═══════════════════════════════════════════════════════════════

@dataclass
class Refutation:
    dimension: RefuteDimension
    target: str
    strategy: str
    counter_argument: str
    evidence: str
    logical_structure: str
    strength: float
    fallacy_exposed: Optional[FallacyType] = None

@dataclass
class MultiDimensionRefutation:
    original_argument: str
    refutations: List[Refutation]
    strongest_refutation: Refutation
    combined_strength: float
    dimension_coverage: float
    key_insight: str
    critical_flaw: str


class RefutationStrategist:
    """反驳策略引擎 v3.0 — 智能填充"""

    # v3.2.0: domain_fills 从方法内局部变量提升为类常量，避免每次调用重建 (~162行数据)
    DOMAIN_FILLS = {
        "投资理财": {
            "positive_feeling": "看好前景、乐观",
            "opposite_scenario": "市场暴跌",
            "source_of_intuition": "近期市场走势或他人成功案例",
            "opposite_stakeholder": "市场的对手方",
            "vanity_image": "有投资眼光",
            "fear_consequence": "踏空、错过机会",
            "hidden_dynamics": "信息不对称下的利益输送",
            "beneficiary": "金融中介和卖方",
            "peer_group": "其他投资者",
            "current_emotion": "贪婪或恐惧",
            "triggered_emotion": "贪婪（错失恐惧）",
            "unexplained_anomaly": "市场在极度乐观后往往暴跌",
            "reverse_premise": "市场存在不确定性，需分散风险",
            "real_cause": "系统性风险和随机性",
            "vulnerability_exposed": "全部资金押注单一方向的敞口",
            "worst_case_scenario": "市场崩盘+流动性枯竭",
            "hidden_better_option": "分散投资+设置止损",
            "premise_counter_extra": "——市场存在黑天鹅事件",
        },
        "企业管理": {
            "positive_feeling": "掌控感、安全感",
            "opposite_scenario": "核心人员离职",
            "source_of_intuition": "过往管理经验或行业惯例",
            "opposite_stakeholder": "被管理的一方",
            "vanity_image": "英明的决策者",
            "fear_consequence": "失控、被质疑",
            "hidden_dynamics": "权力博弈和资源分配",
            "beneficiary": "管理层或现有权力结构",
            "peer_group": "同行企业",
            "current_emotion": "焦虑或自负",
            "triggered_emotion": "焦虑（不确定性恐惧）",
            "unexplained_anomaly": "最严管控的团队创新力最低",
            "reverse_premise": "组织需要弹性而非刚性管控",
            "real_cause": "组织文化和制度设计",
            "vulnerability_exposed": "对单一管理模式的路径依赖",
            "worst_case_scenario": "核心团队集体离职",
            "hidden_better_option": "先小范围试点再推广",
            "premise_counter_extra": "——组织环境变化时管理假设可能失效",
        },
        "市场营销": {
            "positive_feeling": "数据驱动、方向明确",
            "opposite_scenario": "用户偏好突然转变",
            "source_of_intuition": "行业趋势或竞品策略",
            "opposite_stakeholder": "对营销免疫的用户群",
            "vanity_image": "营销高手",
            "fear_consequence": "用户流失、ROI归零",
            "hidden_dynamics": "流量成本持续攀升的不可逆趋势",
            "beneficiary": "流量平台和广告中介",
            "peer_group": "其他营销人员",
            "current_emotion": "焦虑或兴奋",
            "triggered_emotion": "紧迫感（竞品威胁）",
            "unexplained_anomaly": "大品牌砸钱推广却效果递减",
            "reverse_premise": "产品力才是长期增长的根本驱动力",
            "real_cause": "产品-市场匹配度(PMF)未到位",
            "vulnerability_exposed": "对单一渠道的过度依赖",
            "worst_case_scenario": "渠道政策变更+用户反感",
            "hidden_better_option": "深耕留存和口碑而非疯狂获客",
            "premise_counter_extra": "——用户行为的不可预测性远超模型假设",
        },
        "商业竞争": {
            "positive_feeling": "胜券在握、领先感",
            "opposite_scenario": "对手突然发动价格战",
            "source_of_intuition": "市场份额数据或行业报告",
            "opposite_stakeholder": "竞争对手和替代品提供者",
            "vanity_image": "行业领袖、赢家",
            "fear_consequence": "失去竞争优势、被边缘化",
            "hidden_dynamics": "竞争格局的暗流——潜在进入者和替代品",
            "beneficiary": "行业龙头或寡头",
            "peer_group": "同赛道企业",
            "current_emotion": "焦虑或好胜心",
            "triggered_emotion": "危机感（对手动作）",
            "unexplained_anomaly": "行业老大也经常被颠覆",
            "reverse_premise": "差异化比价格战更可持续",
            "real_cause": "护城河深度和用户粘性",
            "vulnerability_exposed": "过度依赖价格优势的单点竞争",
            "worst_case_scenario": "价格战+需求萎缩+新进入者",
            "hidden_better_option": "构建差异化壁垒而非正面硬刚",
            "premise_counter_extra": "——竞争格局的动态性远超静态分析",
        },
        "产品开发": {
            "positive_feeling": "创新感、突破感",
            "opposite_scenario": "用户完全不用新功能",
            "source_of_intuition": "行业标杆或用户反馈",
            "opposite_stakeholder": "非目标用户群",
            "vanity_image": "产品天才",
            "fear_consequence": "产品失败、白费资源",
            "hidden_dynamics": "技术债务和隐性需求错位",
            "beneficiary": "技术供应商或内部技术团队",
            "peer_group": "其他产品经理",
            "current_emotion": "兴奋或焦虑",
            "triggered_emotion": "FOMO（竞品上线新功能）",
            "unexplained_anomaly": "最炫的功能往往使用率最低",
            "reverse_premise": "用户需要的是解决痛点而非更多功能",
            "real_cause": "用户场景理解深度不足",
            "vulnerability_exposed": "功能堆砌带来的复杂度失控",
            "worst_case_scenario": "核心用户流失+新用户不买账",
            "hidden_better_option": "MVP快速验证再迭代",
            "premise_counter_extra": "——用户需求的不确定性和变化速度",
        },
        "技术选型": {
            "positive_feeling": "技术先进感",
            "opposite_scenario": "技术栈出现严重缺陷或社区弃用",
            "source_of_intuition": "技术社区热度或KOL推荐",
            "opposite_stakeholder": "维护遗留系统的团队",
            "vanity_image": "技术专家",
            "fear_consequence": "技术债爆发、系统不可维护",
            "hidden_dynamics": "技术选型背后的利益和人事博弈",
            "beneficiary": "技术供应商或方案推动者",
            "peer_group": "其他技术团队",
            "current_emotion": "自信或焦虑",
            "triggered_emotion": "技术崇拜（盲目追新）",
            "unexplained_anomaly": "最流行的技术不一定最可靠",
            "reverse_premise": "简单成熟方案往往优于时髦方案",
            "real_cause": "团队能力匹配度而非技术本身优劣",
            "vulnerability_exposed": "对单一技术栈的锁定风险",
            "worst_case_scenario": "核心组件漏洞+无人可维护",
            "hidden_better_option": "渐进式迁移而非全面重构",
            "premise_counter_extra": "——技术成熟度曲线和市场不确定性",
        },
        "个人决策": {
            "positive_feeling": "方向感、掌控感",
            "opposite_scenario": "选择后结果远不如预期",
            "source_of_intuition": "身边人的经历或社会舆论",
            "opposite_stakeholder": "受你决定影响的他人",
            "vanity_image": "理性果断的人",
            "fear_consequence": "后悔、浪费时间",
            "hidden_dynamics": "自我认知偏差和社会期待压力",
            "beneficiary": "建议你这么做的人（利益相关）",
            "peer_group": "同龄人或同行",
            "current_emotion": "迷茫或冲动",
            "triggered_emotion": "紧迫感（怕错过时机）",
            "unexplained_anomaly": "大多数人后悔的是'没做的'而非'做错的'",
            "reverse_premise": "维持现状也可能是最优解",
            "real_cause": "内在价值观冲突而非外部条件限制",
            "vulnerability_exposed": "信息不足就做不可逆决策",
            "worst_case_scenario": "最坏结果发生且无法回头",
            "hidden_better_option": "保持选择权，小步试错再All-in",
            "premise_counter_extra": "——个人认知的局限性远大于想象",
        },
        "人际社交": {
            "positive_feeling": "被认可、归属感",
            "opposite_scenario": "关系破裂或被背叛",
            "source_of_intuition": "过往社交经验或他人评价",
            "opposite_stakeholder": "关系中的另一方",
            "vanity_image": "情商高、人缘好",
            "fear_consequence": "被孤立、失去关系",
            "hidden_dynamics": "权力不对等和隐性期待",
            "beneficiary": "关系中占主导的一方",
            "peer_group": "社交圈中的人",
            "current_emotion": "焦虑或委屈",
            "triggered_emotion": "内疚感（怕伤害关系）",
            "unexplained_anomaly": "越讨好关系反而越差",
            "reverse_premise": "清晰的边界感比一味迁就更能维系关系",
            "real_cause": "利益和价值观的深层不匹配",
            "vulnerability_exposed": "为维系关系牺牲自身原则",
            "worst_case_scenario": "关系破裂+声誉受损",
            "hidden_better_option": "坦诚沟通设定边界而非委曲求全",
            "premise_counter_extra": "——人际关系的复杂度超出简单模型",
        },
    }

    GENERIC_FILLS = {
        "positive_feeling": "确定、有信心",
        "opposite_scenario": "情境完全改变",
        "source_of_intuition": "过往经验或他人影响",
        "opposite_stakeholder": "利益受损的一方",
        "vanity_image": "聪明、正确、有远见",
        "fear_consequence": "最坏的结果",
        "hidden_dynamics": "利益驱动的真实逻辑",
        "beneficiary": "既得利益者",
        "peer_group": "周围的人",
        "current_emotion": "当前的直觉感受",
        "triggered_emotion": "特定情绪反应",
        "unexplained_anomaly": "正向论证无法覆盖的异常",
        "reverse_premise": "与原假设相反的前提",
        "real_cause": "被忽略的深层原因",
        "vulnerability_exposed": "关键弱点",
        "worst_case_scenario": "最坏情况",
        "hidden_better_option": "被忽略的更优选项",
        "premise_counter_extra": "——存在反例和例外情况",
    }
    
    STRATEGIES: Dict[RefuteDimension, Dict[str, Any]] = {
        RefuteDimension.SENTIENT: {
            "name": "感性反观", "core_tactic": "用感性体验本身反驳感性判断",
            "strategies": [
                {"tactic": "感受反转", "template": "你此刻感觉{positive_feeling}，但换个场景——比如{opposite_scenario}——你会感觉截然相反。感受是场景的产物，不是真相的信号", "strength_base": 0.72},
                {"tactic": "直觉溯源", "template": "你的直觉来自{source_of_intuition}，而不是来自对{subject}的事实分析。直觉的本质是经验的快捷方式，但捷径不等于正途", "strength_base": 0.65},
                {"tactic": "共情陷阱", "template": "你的共情让你认同了{empathy_target}，但共情是偏见放大器——你共情谁，就偏向谁。试着共情{opposite_stakeholder}，你的判断会完全不同", "strength_base": 0.75},
            ],
            "fallacies": [FallacyType.EMOTIONAL_APPEAL, FallacyType.CONFIRMATION_BIAS],
        },
        RefuteDimension.HUMAN_NATURE: {
            "name": "人性照妖镜", "core_tactic": "揭示人性弱点如何扭曲了论证",
            "strategies": [
                {"tactic": "利益溯源", "template": "这个论证的提出者获益于你相信它——谁从你对{claim_short}的相信中获利，谁就最不值得相信。利益一致性检验: {stakeholder_analysis}", "strength_base": 0.78},
                {"tactic": "虚荣解构", "template": "你相信'{claim_short}'，部分原因是它让你看起来{vanity_image}——虚荣是最隐蔽的认知扭曲。问自己: 如果相信这个不会让你显得高明，你还会信吗？", "strength_base": 0.70},
                {"tactic": "恐惧剖析", "template": "你的判断被恐惧驱动——怕{fear_consequence}导致你选择了{current_choice}，但恐惧驱动的决策几乎都是错的。冷静时你会选什么？", "strength_base": 0.74},
            ],
            "fallacies": [FallacyType.AD_HOMINEM, FallacyType.SUNK_COST],
        },
        RefuteDimension.REFUTATION: {
            "name": "逻辑证伪", "core_tactic": "用形式逻辑找出论证的结构性缺陷",
            "strategies": [
                {"tactic": "前提攻击", "template": "这个论证的前提'{first_premise}'不成立——拆掉地基，整栋楼不需要推。{premise_counter_evidence}", "strength_base": 0.82},
                {"tactic": "反例构造", "template": "存在反例: {counterexample_for_claim}——一个反例就能推翻全称命题。'{claim_short}'并非普遍成立", "strength_base": 0.85},
                {"tactic": "归谬推导", "template": "如果这个论证成立，那么{absurd_consequence_from_claim}也成立——但后者显然荒谬，因此论证的结构有缺陷", "strength_base": 0.76},
            ],
            "fallacies": [FallacyType.CIRCULAR, FallacyType.STRAW_MAN, FallacyType.FALSE_DILEMMA],
        },
        RefuteDimension.SOCIAL_WISDOM: {
            "name": "世故透视", "core_tactic": "揭示论证背后的社会博弈和潜规则",
            "strategies": [
                {"tactic": "潜规则拆解", "template": "表面上说的是'{surface_claim}'，真实运作的是'{hidden_dynamics}'——在社交场中，语言是遮羞布，利益是驱动力", "strength_base": 0.73},
                {"tactic": "权力分析", "template": "这个论证符合{beneficiary}的利益——话语权决定了什么被认为是'正确'的。谁在推{claim_short}，谁就在获利", "strength_base": 0.76},
                {"tactic": "群体压力", "template": "你接受'{claim_short}'，部分原因是{peer_group}都这么认为——从众不等于正确，羊群走得最多的路通向屠宰场", "strength_base": 0.68},
            ],
            "fallacies": [FallacyType.APPEAL_AUTHORITY, FallacyType.HASTY_GENERALIZATION],
        },
        RefuteDimension.EMOTION: {
            "name": "情绪解剖", "core_tactic": "分析情绪如何操控了论证过程",
            "strategies": [
                {"tactic": "情绪溯源", "template": "你当前的情绪状态({current_emotion})让'{claim_short}'看起来{emotion_quality}——但情绪不是滤镜，是哈哈镜。去掉情绪，论点还成立吗？", "strength_base": 0.74},
                {"tactic": "情绪设计识别", "template": "这个论证被设计来触发你的{triggered_emotion}——当你感觉到{triggered_emotion}时，正是被操控之时。冷静下来重新审视", "strength_base": 0.77},
                {"tactic": "情绪替换实验", "template": "假设你现在是完全冷静的，你还会接受'{claim_short}'吗？如果不会，那你的'接受'是{current_emotion}的产物而非理性的结论", "strength_base": 0.70},
            ],
            "fallacies": [FallacyType.EMOTIONAL_APPEAL, FallacyType.POST_HOC],
        },
        RefuteDimension.REVERSE_ARG: {
            "name": "逆向推演", "core_tactic": "假设结论反面成立，反推是否更合理",
            "strategies": [
                {"tactic": "结论反转", "template": "假设'{negated_claim}'成立——反向推演后发现它解释了正向结论无法解释的{unexplained_anomaly}。反面可能更接近真相", "strength_base": 0.71},
                {"tactic": "目的倒推", "template": "如果结果是{actual_result}，那么什么前提会导致这个结果？倒推发现前提可能是{reverse_premise}，而非你假设的{assumed_premise}", "strength_base": 0.74},
                {"tactic": "时间反转", "template": "把时间线倒过来看——从结果看原因，{subject}的{outcome}不是因为{assumed_cause}，而是因为{real_cause}", "strength_base": 0.68},
            ],
            "fallacies": [FallacyType.POST_HOC, FallacyType.CIRCULAR],
        },
        RefuteDimension.DARK_FOREST: {
            "name": "黑暗森林审视", "core_tactic": "在零和博弈框架下审视论证安全性",
            "strategies": [
                {"tactic": "暴露分析", "template": "接受'{claim_short}'会让你在博弈中暴露{vulnerability_exposed}——在黑暗森林中，善意是最危险的信号", "strength_base": 0.72},
                {"tactic": "逆向博弈", "template": "如果对手知道你接受'{claim_short}'，他会怎么做？他会希望你接受——这本身就是不接受的理由。博弈中的信息优势不在你这边", "strength_base": 0.77},
                {"tactic": "生存测试", "template": "在最坏情况下（{worst_case_scenario}），'{claim_short}'还能成立吗？如果不能，它的成立依赖运气而非逻辑", "strength_base": 0.73},
            ],
            "fallacies": [FallacyType.SLIPPERY_SLOPE, FallacyType.SUNK_COST],
        },
        RefuteDimension.BEHAVIORAL: {
            "name": "偏差检测", "core_tactic": "识别认知偏差如何扭曲了论证",
            "strategies": [
                {"tactic": "偏差映射", "template": "你的论证中至少存在{bias_count}个认知偏差: {detected_biases}。知道偏差≠避免偏差，知识的幻觉比无知更危险", "strength_base": 0.76},
                {"tactic": "选择架构分析", "template": "这个论证提供了一个选择架构，默认选项是'{default_option}'——但你没看到的选项可能是{hidden_better_option}", "strength_base": 0.70},
                {"tactic": "事后合理化检测", "template": "你的论证很可能是先有'{claim_short}'的结论，再找理由支撑——先决定后论证是系统一(直觉)的经典模式，理性只是它的律师", "strength_base": 0.79},
            ],
            "fallacies": [FallacyType.SURVIVOR_BIAS, FallacyType.CONFIRMATION_BIAS, FallacyType.HASTY_GENERALIZATION],
        },
    }

    def generate_refutations(self, parsed: ParsedArgument, top_n: int = 3, focus_dimensions: Optional[List[RefuteDimension]] = None) -> MultiDimensionRefutation:
        refutations = []
        dimensions = focus_dimensions or list(RefuteDimension)
        sorted_dims = sorted(dimensions, key=lambda d: parsed.dimension_affinity.get(d, 0.05), reverse=True)
        for dim in sorted_dims:
            ref = self._generate_dimension_refutation(dim, parsed)
            if ref: refutations.append(ref)
        refutations.sort(key=lambda r: r.strength, reverse=True)
        top = refutations[:top_n]
        strongest = top[0] if top else (refutations[0] if refutations else None)
        if not strongest:
            strongest = Refutation(RefuteDimension.REFUTATION, parsed.core_claim, "通用逻辑质疑",
                f"论点'{parsed.core_claim[:30]}'缺乏充分逻辑支撑和证据链", "论证结构中存在未验证的隐含假设", "前提不足→结论不可靠", 0.5)
            top = [strongest]
        combined = sum(r.strength for r in top) / len(top)
        coverage = len(set(r.dimension for r in refutations)) / len(RefuteDimension)
        return MultiDimensionRefutation(parsed.raw_text, top, strongest, combined, coverage,
            self._gen_key_insight(parsed, top), self._gen_critical_flaw(parsed, top))

    def _generate_dimension_refutation(self, dim: RefuteDimension, parsed: ParsedArgument) -> Optional[Refutation]:
        cfg = self.STRATEGIES.get(dim)
        if not cfg: return None
        
        # v3.0.1: 智能策略选择 — 基于维度亲和力选择最匹配的策略
        dim_affinity = parsed.dimension_affinity.get(dim, 0.03)
        if dim_affinity >= 0.4:
            # 高亲和力: 选最强策略
            strategy = max(cfg["strategies"], key=lambda s: s["strength_base"])
        elif dim_affinity >= 0.2:
            # 中亲和力: 选中等策略
            sorted_strategies = sorted(cfg["strategies"], key=lambda s: s["strength_base"])
            strategy = sorted_strategies[len(sorted_strategies) // 2]
        else:
            # 低亲和力: 选最弱策略（减少噪音）
            strategy = min(cfg["strategies"], key=lambda s: s["strength_base"])
        counter = self._fill_template_v2(strategy["template"], parsed, dim)
        structures = {RefuteDimension.SENTIENT: "感性判断→感性可被场景操控→场景非真相→判断不可靠",
            RefuteDimension.HUMAN_NATURE: "论证→谁获益→获益者≠真相→利益扭曲论证",
            RefuteDimension.REFUTATION: "前提→前提不成立→推理链断裂→结论不可靠",
            RefuteDimension.SOCIAL_WISDOM: "表面论证→利益分析→权力结构→真实动机≠表面理由",
            RefuteDimension.EMOTION: "情绪状态→情绪滤镜→扭曲判断→去情绪后结论改变",
            RefuteDimension.REVERSE_ARG: "正向结论→假设反面成立→反面解释力更强→正面被推翻",
            RefuteDimension.DARK_FOREST: "论证→博弈分析→接受论证=暴露弱点→安全性存疑",
            RefuteDimension.BEHAVIORAL: "论证→偏差检测→偏差扭曲推理→去偏差后结论不同"}
        fallacy = None
        fallacies = cfg.get("fallacies", [])
        if fallacies:
            fallacy_indicators = {FallacyType.AD_HOMINEM: ["人品","动机","身份"], FallacyType.STRAW_MAN: ["曲解","误解"],
                FallacyType.FALSE_DILEMMA: ["只有两种","非此即彼","要么"], FallacyType.SLIPPERY_SLOPE: ["然后就会","最终"],
                FallacyType.CIRCULAR: ["因为所以","本身就是"], FallacyType.APPEAL_AUTHORITY: ["专家说","权威","领导说"],
                FallacyType.HASTY_GENERALIZATION: ["所有","每个","从来"], FallacyType.CONFIRMATION_BIAS: ["你看","证明","果然"],
                FallacyType.EMOTIONAL_APPEAL: ["可怜","不公平","太过分"], FallacyType.POST_HOC: ["之后","结果","造成了"],
                FallacyType.SURVIVOR_BIAS: ["成功","案例","经验"], FallacyType.SUNK_COST: ["已经投入","都做了","不能白费"]}
            for f in fallacies:
                if any(ind in parsed.raw_text for ind in fallacy_indicators.get(f, [])):
                    fallacy = f; break
            if not fallacy: fallacy = fallacies[0]
        # v3.0.1: 重构反驳强度公式 — 原公式几乎总是输出1.0
        # 新策略: 以strategy base为基准，用对数衰减+质量因子调节
        base = strategy["strength_base"]
        dim_affinity = parsed.dimension_affinity.get(dim, 0.05)
        vuln_factor = parsed.vulnerability_score
        assumption_count = len(parsed.implicit_assumptions)
        
        # 质量因子：论证越弱，反驳越有效
        quality_factor = (vuln_factor * 0.08 + assumption_count * 0.01)
        
        # 领域匹配度加成（有上限）
        domain_match_bonus = min(dim_affinity * 0.08, 0.06)
        
        # 组合强度 — 确保不会轻易达到1.0
        raw_strength = base + quality_factor + domain_match_bonus
        
        # 最终约束: 强度上限=base+0.12，确保区分度
        cap = min(base + 0.12, 0.96)
        strength = min(raw_strength, cap)
        return Refutation(dim, parsed.core_claim, f"[{cfg['name']}] {strategy['tactic']}", counter,
            self._gen_evidence_v2(dim, parsed), structures.get(dim, "前提质疑→推理质疑→结论质疑"), strength, fallacy)

    def _fill_template_v2(self, template: str, parsed: ParsedArgument, dim: RefuteDimension) -> str:
        """v3.0.2: 智能填充 — 扩充领域覆盖"""
        dm = parsed.context_domain
        
        # v3.2.0: 使用类常量替代方法内 ~180行 局部字典
        df = self.DOMAIN_FILLS.get(dm, {})
        generic_fills = self.GENERIC_FILLS
        
        fills = {
            "claim_short": parsed.core_claim[:30], "subject": parsed.claim_subject,
            "negated_claim": parsed.negated_claim,
            "first_premise": parsed.premises[0] if parsed.premises else "未明确的前提",
            "premise_counter_evidence": self._pc_evidence(parsed),
            "counterexample_for_claim": self._counterexample(parsed),
            "absurd_consequence_from_claim": self._absurd(parsed),
            "stakeholder_analysis": f"如果'{parsed.core_claim[:20]}'被广泛接受，谁最受益？谁最受损？",
            "current_choice": parsed.core_claim[:20],
            "surface_claim": parsed.core_claim[:25],
            "emotion_quality": "可信、有道理、有吸引力",
            "actual_result": parsed.claim_object or "实际观察到的结果",
            "assumed_premise": parsed.premises[0][:20] if parsed.premises else "当前假设",
            "outcome": parsed.claim_object or "结果",
            "assumed_cause": parsed.premises[0][:15] if parsed.premises else "表面原因",
            "empathy_target": parsed.claim_subject or "当前立场",
            "bias_count": str(max(len(parsed.implicit_assumptions), 1)),
            "detected_biases": self._detect_biases_text(parsed),
            "default_option": parsed.core_claim[:20],
        }
        # 合并领域填充（领域优先，通用兜底）
        for key in generic_fills:
            fills[key] = df.get(key, generic_fills[key])
        
        result = template
        for ph in _RE_TEMPLATE_PLACEHOLDER.findall(template):
            if ph in fills: result = result.replace(f"{{{ph}}}", fills[ph])
        return _RE_TEMPLATE_REMAINDER.sub('', result)

    def _pc_evidence(self, p: ParsedArgument) -> str:
        if not p.premises: return "前提完全缺失，无法验证"
        base = f"事实上，'{p.premises[0][:20]}'并不总是成立"
        domain_extra = {
            "投资理财": "——市场存在黑天鹅事件",
            "企业管理": "——组织环境变化时管理假设可能失效",
            "市场营销": "——用户行为不可预测且随时间演变",
            "商业竞争": "——竞争对手策略和反应无法预判",
            "产品开发": "——用户需求和场景远比假设复杂",
            "技术选型": "——技术栈的长期演进方向难以预测",
            "个人决策": "——个体偏好和环境都在变化",
            "人际社交": "——人的行为和关系动态变化极快",
        }
        return base + domain_extra.get(p.context_domain, "——存在反例和例外情况")

    def _counterexample(self, p: ParsedArgument) -> str:
        return {
            "投资理财": "巴菲特逆势投资反而获利，说明'随大势'并非万能",
            "企业管理": "谷歌实行20%自由时间制，说明'严格管控'并非唯一解",
            "市场营销": "小众品牌通过差异化突围，说明'大投入推广'不是唯一路径",
            "商业竞争": "Costco不打价格战却长期盈利，说明'必须降价'不是唯一出路",
            "产品开发": "Slack最初只是游戏公司内部工具，说明'MVP先做再改'比完美设计更有效",
            "技术选型": "WhatsApp用Erlang支撑十亿用户，说明'主流技术栈'不是唯一正确答案",
            "个人决策": "很多人辞职创业失败后回归大厂获得更好发展，说明'稳定选择'未必是退步",
        }.get(p.context_domain, f"存在'{p.core_claim[:15]}'不成立的实际案例")

    def _absurd(self, p: ParsedArgument) -> str:
        rules = {"应该": f"那么任何'{p.claim_subject}应该X'的主张都成立，不论X多荒谬",
            "必须": "那么没有选择余地，但现实中总有替代方案",
            "导致": f"那么任何与'{p.claim_object}'相关的事都会被同样原因导致",
            "因为": "那么任何相关性都可以被当作因果性",
            "是": f"那么任何关于'{p.claim_subject}'的陈述都成立——显然荒谬",
            "需要": f"那么任何'需要X'的主张都无条件成立——需求不等于可行性"}
        for kw, absurd in rules.items():
            if kw in p.core_claim: return absurd
        # 兜底：使用否定主张构造归谬
        return f"那么'{p.negated_claim[:30] if len(p.negated_claim)>2 else p.core_claim[:30]}'的反面也成立——两者矛盾说明原论证结构有缺陷"

    def _detect_biases_text(self, p: ParsedArgument) -> str:
        biases = []
        bias_pats = {"确认偏误": ["证明","果然","你看"], "锚定效应": ["去年","之前","原来"],
            "从众偏差": ["大家都","所有人"], "幸存者偏差": ["成功的","案例"],
            "沉没成本": ["已经投入","都做了","不能白费","已经"], "损失厌恶": ["至少","保底","不要亏"],
            "过度自信": ["一定","必然","绝对","肯定"], "可得性偏差": ["最近","刚刚","听说"]}
        for bias, inds in bias_pats.items():
            if any(i in p.raw_text for i in inds): biases.append(bias)
        if not biases: biases = ["确认偏误", "过度自信"]
        return "、".join(biases[:4])

    def _gen_evidence_v2(self, dim: RefuteDimension, p: ParsedArgument) -> str:
        """v3.0.2: 扩充领域证据"""
        dm = p.context_domain
        domain_t = {
            "投资理财": "行为金融学证明：投资者在做出此类决策时，认知偏差影响远大于理性分析",
            "企业管理": "组织行为学表明：管理决策中'理性'只是表象，实际受组织政治和个人利益深刻影响",
            "市场营销": "消费者行为研究显示：用户决策中超过60%是潜意识驱动的",
            "商业竞争": "博弈论和竞争战略研究表明：价格战等零和策略长期期望收益为负",
            "产品开发": "产品心理学发现：功能越多用户越难用——帕金森定律的软件版本",
            "技术选型": "软件工程研究：技术选型中80%的决定基于非技术因素（团队能力/历史包袱/组织偏好）",
            "个人决策": "行为经济学揭示：人在做个人选择时存在系统性偏差（锚定效应、现状偏差、损失厌恶）",
            "人际社交": "社会心理学证明：人际关系中的判断70%以上受情绪和第一印象影响",
        }.get(dm, "认知科学表明：人类在此类决策中存在系统性偏差")
        
        evidences = {
            RefuteDimension.SENTIENT: f"感性判断实验证据：同一问题在不同情绪状态下得出相反判断（心理学反复验证）。领域: {dm}",
            RefuteDimension.HUMAN_NATURE: f"利益分析：在{dm}领域中，论证提出者的利益立场往往决定论证方向。{domain_t}",
            RefuteDimension.REFUTATION: f"逻辑检验：论证包含{len(p.implicit_assumptions)}个未验证隐含假设，每个都是潜在断裂点。关键前提: {p.premises[0][:20] if p.premises else '未明确'}",
            RefuteDimension.SOCIAL_WISDOM: f"社会心理学证据：群体压力和从众效应能使70%的人否认明显事实（阿希从众实验）。在{dm}领域尤为显著",
            RefuteDimension.EMOTION: f"神经科学证据：情绪中枢(杏仁核)反应速度比理性中枢(前额叶)快200ms，先有情绪后有理由",
            RefuteDimension.REVERSE_ARG: f"逆向验证：将'{p.core_claim[:20]}'取反后，反向结论'{p.negated_claim[:20]}'能解释正向无法覆盖的异常",
            RefuteDimension.DARK_FOREST: f"博弈论证据：在非合作博弈中，单方面善意策略期望收益低于防御策略。{domain_t}",
            RefuteDimension.BEHAVIORAL: f"认知偏差统计：检测到偏差: {self._detect_biases_text(p)}。{domain_t}"}
        return evidences.get(dim, "通用反驳证据")

    def _gen_key_insight(self, p: ParsedArgument, refs: List[Refutation]) -> str:
        if not refs: return "论证结构较完整，未发现重大缺陷"
        s = refs[0]
        prefix = f"在{p.context_domain}领域，" if p.context_domain != "通用" else ""
        return f"{prefix}从{s.dimension.value}维度看，'{p.core_claim[:25]}'的核心缺陷: {s.counter_argument[:60]}"

    def _gen_critical_flaw(self, p: ParsedArgument, refs: List[Refutation]) -> str:
        if not refs: return "未发现关键缺陷"
        s = refs[0]
        if s.fallacy_exposed: return f"关键缺陷: {s.fallacy_exposed.value} — {s.counter_argument[:50]}"
        return f"关键缺陷: {s.strategy} — {s.counter_argument[:50]}"


# ═══════════════════════════════════════════════════════════════
# 第四层: 论证强度评估器
# ═══════════════════════════════════════════════════════════════

@dataclass
class StrengthAssessment:
    overall_strength: float
    premise_strength: float
    reasoning_strength: float
    evidence_strength: float
    assumption_strength: float
    vulnerabilities: List[str]
    detected_fallacies: List[FallacyType]
    improvement_suggestions: List[str]
    strength_grade: str

class ArgumentStrengthAssessor:
    GRADE_THRESHOLDS = {"S": 0.90, "A": 0.75, "B": 0.60, "C": 0.40, "D": 0.20, "F": 0.00}

    def assess(self, parsed: ParsedArgument, refutation: MultiDimensionRefutation) -> StrengthAssessment:
        ps = self._assess_premises(parsed)
        rs = self._assess_reasoning(parsed)
        es = self._assess_evidence(parsed)
        asum = self._assess_assumptions(parsed)
        # v3.0.3: 修复双重惩罚 — 反驳强度只在总评中惩罚一次，不在推理子项中重复惩罚
        raw = ps * 0.30 + rs * 0.25 + es * 0.25 + asum * 0.20
        refutation_penalty = refutation.combined_strength ** 1.5 * 0.12  # 非线性衰减，惩罚更温和
        overall = max(0.05, min(raw - refutation_penalty, 1.0))
        vulns = self._identify_vulnerabilities(parsed, refutation)
        fallacies = self._detect_fallacies(parsed, refutation)
        improvements = self._generate_improvements(parsed, refutation, vulns)
        grade = self._calculate_grade(overall)
        return StrengthAssessment(overall, ps, rs, es, asum, vulns, fallacies, improvements, grade)

    def _assess_premises(self, p: ParsedArgument) -> float:
        if not p.premises: return 0.20
        s = 0.45
        if len(p.premises) >= 3: s += 0.15
        elif len(p.premises) >= 2: s += 0.10
        for pr in p.premises:
            if any(kw in pr for kw in ["数据","统计","研究","%","显示","表明"]): s += 0.08
        # 有因果链的前提加分
        if any(any(c in pr for c in ["因为","由于","导致","所以"]) for pr in p.premises): s += 0.05
        return min(s, 1.0)

    def _assess_reasoning(self, p: ParsedArgument) -> float:
        s = 0.50
        if len(p.reasoning_chain) >= 3: s += 0.10
        if len(p.reasoning_chain) >= 5: s += 0.05
        # 有明确推理链加分
        if any("前提" in step for step in p.reasoning_chain): s += 0.10
        # v3.0.3: 移除反驳惩罚 — 已在 assess() 总评中统一惩罚，避免双重惩罚
        return max(0.10, min(s, 1.0))

    def _assess_evidence(self, p: ParsedArgument) -> float:
        return {"数据证据": 0.85, "权威证据": 0.70, "案例证据": 0.55, "逻辑证据": 0.60, "经验证据": 0.40, "无明确证据": 0.15}.get(p.evidence_type, 0.3)

    def _assess_assumptions(self, p: ParsedArgument) -> float:
        c = len(p.implicit_assumptions)
        return {0: 0.7, 1: 0.8}.get(c, max(0.8 - (c - 1) * 0.2, 0.2))

    def _identify_vulnerabilities(self, p: ParsedArgument, r: MultiDimensionRefutation) -> List[str]:
        v = []
        if not p.premises: v.append("无明确前提支撑")
        if p.implicit_assumptions: v.append(f"{len(p.implicit_assumptions)}个未验证的隐含假设")
        if p.evidence_type == "无明确证据": v.append("缺乏支撑证据")
        if p.vulnerability_score > 0.5: v.append("存在绝对化表述")
        if p.weakness_indicators: v.append(f"发现{len(p.weakness_indicators)}个弱点指示词")
        for ref in r.refutations:
            if ref.strength > 0.85: v.append(f"[{ref.dimension.value}] {ref.strategy}")
        return v[:6]

    def _detect_fallacies(self, p: ParsedArgument, r: MultiDimensionRefutation) -> List[FallacyType]:
        f = []
        for ref in r.refutations:
            if ref.fallacy_exposed and ref.fallacy_exposed not in f: f.append(ref.fallacy_exposed)
        if _RE_HASTY_GENERALIZATION.search(p.raw_text) and FallacyType.HASTY_GENERALIZATION not in f:
            f.append(FallacyType.HASTY_GENERALIZATION)
        if _RE_FALSE_DILEMMA.search(p.raw_text) and FallacyType.FALSE_DILEMMA not in f:
            f.append(FallacyType.FALSE_DILEMMA)
        return f[:5]

    def _generate_improvements(self, p: ParsedArgument, r: MultiDimensionRefutation, v: List[str]) -> List[str]:
        imp = []
        if not p.premises: imp.append("补充明确的前提，使推理链完整")
        if p.evidence_type == "无明确证据": imp.append("增加数据或案例支撑，提升论证说服力")
        if p.implicit_assumptions: imp.append(f"验证{len(p.implicit_assumptions)}个隐含假设的成立性")
        if r.critical_flaw: imp.append(f"修复关键缺陷: {r.critical_flaw[:40]}")
        if p.weakness_indicators: imp.append(f"消除{len(p.weakness_indicators)}个绝对化/情感化表述")
        for ref in r.refutations[:2]:
            imp.append(f"从{ref.dimension.value}维度加强: {ref.counter_argument[:40]}")
        return imp[:5]

    def _calculate_grade(self, overall: float) -> str:
        for g, t in sorted(self.GRADE_THRESHOLDS.items(), key=lambda x: -x[1]):
            if overall >= t: return g
        return "F"


# ═══════════════════════════════════════════════════════════════
# 第五层: 辩论对抗场 (DebateArena) — v3.0 上下文感知
# ═══════════════════════════════════════════════════════════════

@dataclass
class DebateRound:
    round_number: int
    proposer_argument: str
    refuter_counter: str
    proposer_defense: str
    round_verdict: str
    remaining_issues: List[str]

@dataclass
class DebateResult:
    original_argument: str
    rounds: List[DebateRound]
    final_verdict: str
    truth_approximation: float
    remaining_blind_spots: List[str]
    evolved_argument: str

class DebateArena:
    MAX_ROUNDS = 3

    # 每轮辩论的进化策略 — 根据轮次递进深化
    ROUND_FOCUS = {
        1: {"focus": "表层逻辑检验", "defense_threshold": 0.5},
        2: {"focus": "深层假设质疑", "defense_threshold": 0.4},
        3: {"focus": "元论证审视", "defense_threshold": 0.3},
    }

    def debate(self, parsed: ParsedArgument, refutation: MultiDimensionRefutation, assessment: StrengthAssessment) -> DebateResult:
        rounds = []
        current_claim = parsed.core_claim
        original_strength = assessment.overall_strength
        issues = list(assessment.vulnerabilities)
        
        for rn in range(1, self.MAX_ROUNDS + 1):
            round_cfg = self.ROUND_FOCUS.get(rn, {})
            
            # 正方提出论点（每轮内容不同）
            pa = self._proposer_evolved(current_claim, rn, issues, parsed)
            
            # 反方选择对应维度的反驳（轮次递进：从弱到强）
            ref_idx = min(rn - 1, len(refutation.refutations) - 1)
            cr = refutation.refutations[ref_idx]
            rc = f"反方反驳[{cr.dimension.value}维]: {cr.counter_argument} (强度:{cr.strength:.0%})。逻辑链: {cr.logical_structure}"
            
            # v3.0.1: 正方防御 — 基于当前轮次的动态评估而非固定等级
            dynamic_score = max(original_strength - rn * 0.08, 0.15)  # 随轮次衰减
            pd = self._defender_evolved(rc, dynamic_score, rn, parsed, cr)
            
            # 裁判判定
            verdict = self._judge_evolved(pd, cr, rn)
            
            # 更新问题追踪
            issues = self._update_issues_evolved(issues, pd, cr, rn)
            
            rounds.append(DebateRound(rn, pa, rc, pd, verdict, issues))
            
            # v3.0.1: 真正的论点进化 — 每轮都基于本轮反馈修改论点
            current_claim = self._evolve_claim(current_claim, pd, rn, parsed, cr)

        fv = self._final_verdict(rounds, assessment, parsed)
        
        # v3.0.1: 真理逼近度基于实际辩论结果
        defender_wins = sum(1 for r in rounds if "反方胜出" in r.round_verdict or "反方占优" in r.round_verdict)
        proposer_wins = sum(1 for r in rounds if "正方守住" in r.round_verdict or "平局" in r.round_verdict)
        
        if defender_wins >= 2:
            ta = min(original_strength * 0.5, 0.45)
        elif proposer_wins >= 2:
            ta = min(original_strength * 1.15, 0.85)
        else:
            ta = min(original_strength * 0.8, 0.65)
        
        bs = issues if issues else ["辩论未发现明显盲区"]
        return DebateResult(parsed.raw_text, rounds, fv, ta, bs, current_claim)

    def _proposer_evolved(self, claim: str, rn: int, issues: List[str], p: ParsedArgument) -> str:
        """v3.0.1: 进化版正方主张 — 每轮根据前一轮反馈调整"""
        if rn == 1:
            return (f"正方主张(R1): {claim}。论据: {p.premises[0] if p.premises else '基于经验判断'}。"
                    f"类型: {p.argument_type.value} | 领域: {p.context_domain}")
        elif rn == 2:
            # R2: 针对R1的反驳做回应
            focus_issue = issues[0] if issues else "反驳意见"
            refined = self._soften_claim(claim, p)
            return (f"正方回应(R2): 针对'{focus_issue[:25]}'，修正为'{refined}'。"
                    f"补充前提: {p.premises[1] if len(p.premises)>1 else '增加限定条件'}")
        else:
            # R3: 最终立场
            final_version = self._hedge_claim(claim, p)
            return (f"正方最终立场(R3): '{final_version}'。承认存在{min(len(p.implicit_assumptions), 4)}个需验证假设。"
                    f"结论在{p.context_domain}特定情境下有条件成立")

    def _defender_evolved(self, counter: str, dynamic_score: float, rn: int, 
                          p: ParsedArgument, ref: Refutation) -> str:
        """v3.0.1: 进化版防御 — 动态评分驱动"""
        premise_ref = p.premises[0][:20] if p.premises else '核心论点'
        
        if dynamic_score >= 0.65:
            return (f"正方强力防御(R{rn}): 论证强度较高({dynamic_score:.0%})"
                    f"，{ref.dimension.value}维反驳({ref.strength:.0%})未推翻核心前提'{premise_ref}'"
                    f"。但该维度提出了值得关注的视角")
        elif dynamic_score >= 0.40:
            return (f"正方策略性退让(R{rn}): {ref.dimension.value}维反驳({ref.strength:.0%})"
                    f"揭示了论证中的薄弱环节——具体来说: {ref.counter_argument[:40]}"
                    f"。但核心结论在'{p.context_domain}'限定条件下仍有价值")
        else:
            assumption_count = min(len(p.implicit_assumptions), 5)
            return (f"正方实质性退让(R{rn}): {ref.dimension.value}维反驳有力地击中了要害"
                    f"——原论证的{assumption_count}个隐含假设中至少{max(1, assumption_count//2)}个缺乏支撑"
                    f"。需要从根本上重构论证基础")

    def _judge_evolved(self, defense: str, ref: Refutation, rn: int) -> str:
        """v3.2.0: 进化版裁判 — 基于数值评分 + 关键词的混合判定

        修复 v3.0.1 的纯关键词判定偏差：
        - 纯文本关键词判定太脆弱，同一语义的不同表述会导致判定不一致
        - 增加数值维度：反驳强度(ref.strength) 和 轮次递进权重
        - 当数值判定与关键词判定冲突时，以数值为主
        """
        # 数值评分：综合反驳强度和轮次递进权重
        round_weight = 1.0 + (rn - 1) * 0.15  # R1=1.0, R2=1.15, R3=1.30
        effective_strength = ref.strength * round_weight

        # 数值判定阈值
        if effective_strength >= 0.85:
            return f"反方胜出(R{rn})——{ref.dimension.value}维反驳有效且致命(强度{ref.strength:.0%})"
        elif effective_strength >= 0.65:
            return f"反方占优(R{rn})——{ref.dimension.value}维反驳部分有效(强度{ref.strength:.0%})"
        elif effective_strength >= 0.45:
            # 中等区间：结合防御文本辅助判定
            if "实质性退让" in defense:
                return f"反方占优(R{rn})——{ref.dimension.value}维反驳有效且正方退让"
            return f"微弱反方优势(R{rn})——{ref.dimension.value}维反驳留下合理质疑"
        else:
            # 低强度反驳
            if "实质性退让" in defense:
                return f"反方占优(R{rn})——虽然反驳强度不高，但正方主动退让"
            return f"正方守住(R{rn})——{ref.dimension.value}维反驳力度不足，但提供了外部视角"

    def _update_issues_evolved(self, issues: List[str], defense: str, ref: Refutation, rn: int) -> List[str]:
        """v3.0.1: 进化版问题追踪"""
        result = list(issues)
        if "实质性退让" in defense:
            issue_text = f"[R{rn}|{ref.dimension.value}] 关键缺陷: {ref.counter_argument[:35]}"
            if issue_text not in result:
                result.append(issue_text)
        elif "策略性退让" in defense:
            issue_text = f"[R{rn}|{ref.dimension.value}] 薄弱点需补充: {ref.strategy}"
            if issue_text not in result:
                result.append(issue_text)
        elif "有力地" in defense:
            issue_text = f"[R{rn}|{ref.dimension.value}] 结构性风险被识别"
            if issue_text not in result:
                result.append(issue_text)
        return result[:6]

    def _evolve_claim(self, current_claim: str, defense: str, rn: int,
                       parsed: ParsedArgument, ref: Refutation) -> str:
        """v3.0.1: 真正的论点进化 — 每轮生成实质不同的版本"""
        # 清理之前的前缀
        base = _RE_CLAIM_CLEAN_PREFIX.sub('', current_claim).strip()
        base = _RE_CLAIM_CLEAN_SUFFIXES[0].sub('', base)
        base = _RE_CLAIM_CLEAN_SUFFIXES[1].sub('', base)
        base = _RE_CLAIM_CLEAN_SUFFIXES[2].sub('', base)
        
        if not base or len(base) < 3:
            base = parsed.core_claim
        
        if rn == 1:
            if "实质性退让" in defense:
                return self._soften_claim(base, parsed)
            return base
        
        elif rn == 2:
            if "策略性退让" in defense or "实质性退让" in defense:
                return self._hedge_claim(base, parsed)
            # 即使是强力防御，也加入限定
            return self._add_context_qualifier(base, parsed)
        
        else:  # R3 最终版本
            if "实质性退让" in defense:
                return self._reconstruct_claim(parsed)
            if "策略性退让" in defense:
                return self._hedge_claim(base, parsed)
            return f"限定版: {self._add_context_qualifier(base, parsed)}"
    
    def _soften_claim(self, claim: str, p: ParsedArgument) -> str:
        """软化绝对化表述 — v3.2.0: 使用 ArgumentParser.SOFTEN_MAP 共享常量"""
        c = claim
        for old, new in ArgumentParser.SOFTEN_MAP.items():
            c = c.replace(old, new, 1)
        if c != claim:
            return c
        return f"{c}（在特定条件下）"

    def _hedge_claim(self, claim: str, p: ParsedArgument) -> str:
        """添加不确定性限定 — v3.0.3: 用字符串长度替代hash，确保跨进程确定性"""
        hedge_phrases = ["在理想情况下,", "从概率角度,", "考虑到市场不确定性,"]
        # 确定性选择：基于论点字符串长度，跨进程一致
        idx = len(claim) % len(hedge_phrases)
        prefix = hedge_phrases[idx]
        return f"{prefix}{claim}"

    def _add_context_qualifier(self, claim: str, p: ParsedArgument) -> str:
        """添加领域/情境限定"""
        domain_quals = {
            "投资理财": "（在风险可控的前提下）",
            "企业管理": "（在组织环境稳定的前提下）",
            "市场营销": "（在目标用户明确的前提下）",
            "商业竞争": "（在短期战术层面）",
            "人际社交": "（在双方信息对称的前提下）",
        }
        qual = domain_quals.get(p.context_domain, "（在特定条件下）")
        return f"{claim}{qual}"

    def _reconstruct_claim(self, p: ParsedArgument) -> str:
        """重构论证 — 当原论证被严重击溃时使用"""
        subject = p.claim_subject or "此观点"
        domain = p.context_domain
        return (f"'{subject}'相关的主张需要更严谨的证据链支撑，"
                f"尤其在{domain}领域中应考虑更多变量和边界条件")

    def _final_verdict(self, rounds: List[DebateRound], a: StrengthAssessment, p: ParsedArgument) -> str:
        rw = sum(1 for r in rounds if "反方" in r.round_verdict)
        ph = sum(1 for r in rounds if "正方" in r.round_verdict)
        claim_short = p.core_claim[:20]
        if rw >= 2:
            return f"最终裁决: 反驳有效——'{claim_short}'存在显著缺陷(强度:{a.strength_grade})，需重大修正。核心问题: {a.vulnerabilities[0] if a.vulnerabilities else '结构性不足'}"
        if ph >= 2:
            return f"最终裁决: 论证基本成立(强度:{a.strength_grade})——'{claim_short}'虽有可攻击之处，但核心结论在限定条件下可接受"
        return f"最终裁决: 部分成立(强度:{a.strength_grade})——论证需修正和限定"


# ═══════════════════════════════════════════════════════════════
# 第六层: 论证修复器 (ArgumentRepair) — v3.0 新增
# ═══════════════════════════════════════════════════════════════

@dataclass
class RepairedArgument:
    original_claim: str
    repaired_claim: str
    added_premises: List[str]
    removed_assumptions: List[str]
    added_conditions: List[str]
    evidence_suggestions: List[str]
    repaired_strength_estimate: float
    repair_rationale: str

class ArgumentRepair:
    """自动生成加固后的论点版本"""

    def repair(self, parsed: ParsedArgument, refutation: MultiDimensionRefutation,
               assessment: StrengthAssessment, debate: DebateResult) -> RepairedArgument:
        repaired_claim = self._repair_claim(parsed, assessment)
        added_premises = self._add_premises(parsed, refutation)
        removed = self._remove_unreliable(parsed, refutation)
        conditions = self._add_conditions(parsed, assessment)
        evidence_sug = self._suggest_evidence(parsed, refutation)
        estimate = min(assessment.overall_strength + len(added_premises) * 0.05 + len(conditions) * 0.03, 0.95)
        rationale = (f"原论证强度{assessment.strength_grade}级({assessment.overall_strength:.0%})，"
            f"存在{len(assessment.vulnerabilities)}个脆弱点。修复策略: 去绝对化+补前提+加限定+增证据，"
            f"预计修复后强度{estimate:.0%}")
        return RepairedArgument(parsed.core_claim, repaired_claim, added_premises, removed,
            conditions, evidence_sug, estimate, rationale)

    def _repair_claim(self, p: ParsedArgument, a: StrengthAssessment) -> str:
        # v3.2.0: 使用 ArgumentParser.SOFTEN_MAP 共享常量
        c = p.core_claim
        for old, new in ArgumentParser.SOFTEN_MAP.items():
            c = c.replace(old, new)
        if a.strength_grade in ("D","F") and not c.startswith("在限定条件下"):
            c = f"在限定条件下，{c}"
        return c

    def _add_premises(self, p: ParsedArgument, r: MultiDimensionRefutation) -> List[str]:
        added = []
        if not p.premises: added.append(f"前提: {p.context_domain}领域的基本规律支持此判断")
        for ref in r.refutations[:2]:
            if ref.fallacy_exposed == FallacyType.CIRCULAR: added.append("前提: 独立于结论的外部验证存在")
            if ref.fallacy_exposed == FallacyType.HASTY_GENERALIZATION: added.append("前提: 样本量足够且具有代表性")
        dp = {"投资理财":"前提: 风险收益比经过量化评估","企业管理":"前提: 组织能力和资源配置可支撑此决策",
            "市场营销":"前提: 用户需求经过验证而非假设"}
        if p.context_domain in dp: added.append(dp[p.context_domain])
        return added[:4]

    def _remove_unreliable(self, p: ParsedArgument, r: MultiDimensionRefutation) -> List[str]:
        unreliable = []
        for a in p.implicit_assumptions:
            if any(kw in a for kw in ["因果","必然","普遍","不会出错","客观"]):
                unreliable.append(a)
        return unreliable[:4]

    def _add_conditions(self, p: ParsedArgument, a: StrengthAssessment) -> List[str]:
        c = []
        if a.strength_grade in ("C","D","F"): c.append(f"限定条件: 仅在{p.context_domain}领域特定情境下适用")
        if p.implicit_assumptions: c.append("限定条件: 上述隐含假设成立的前提下")
        return c[:3]

    def _suggest_evidence(self, p: ParsedArgument, r: MultiDimensionRefutation) -> List[str]:
        s = []
        if p.evidence_type == "无明确证据":
            s.append("建议补充: 定量数据支撑（统计/调查/实验结果）")
            s.append("建议补充: 同领域成功/失败案例对比")
        elif p.evidence_type == "经验证据":
            s.append("建议升级: 将经验证据升级为数据证据，避免主观偏差")
        else:
            s.append("建议补充: 反面证据的分析和回应，增强论证全面性")
        return s[:4]


# ═══════════════════════════════════════════════════════════════
# 第七层: 解决方案生成器 (SolutionGenerator) — v3.0
# ═══════════════════════════════════════════════════════════════

@dataclass
class Solution:
    title: str
    description: str
    actions: List[str]
    addresses_vulnerability: str
    dimension: RefuteDimension
    priority: int
    expected_improvement: float

@dataclass
class SolutionSet:
    original_argument: str
    solutions: List[Solution]
    quick_wins: List[Solution]
    deep_fixes: List[Solution]
    overall_assessment: str
    recommended_approach: str

class SolutionGenerator:
    DIMENSION_FIXES = {
        RefuteDimension.SENTIENT: ("感性校准方案", ["列出当前情绪状态，评估其对判断的影响权重", "在冷静状态下重新审视核心主张", "寻找与直觉相反但逻辑合理的观点", "设定24小时冷静期后再做最终判断"], 0.25),
        RefuteDimension.HUMAN_NATURE: ("利益链脱钩方案", ["列出论证提出者的利益立场", "识别自身偏见来源（虚荣/恐惧/贪婪）", "假设自己是中立第三方重新评估", "设计利益无关的验证方法"], 0.30),
        RefuteDimension.REFUTATION: ("逻辑重构方案", ["逐条验证每个前提的成立性", "为每个隐含假设寻找反例", "用归谬法测试结论的极限", "重新构建从前提到结论的完整推理链"], 0.35),
        RefuteDimension.SOCIAL_WISDOM: ("社交滤镜清洗方案", ["识别群体压力和从众因素", "分析谁从你接受这个论证中获益", "假设你在完全独立的情况下会如何判断", "找到与主流意见相左但有力的观点"], 0.20),
        RefuteDimension.EMOTION: ("情绪去噪方案", ["标注当前情绪状态（1-10分）", "识别论证中被情绪触发的部分", "用'情绪替换实验'：假设冷静状态下的判断", "延迟决策至情绪平复后"], 0.22),
        RefuteDimension.REVERSE_ARG: ("逆向验证方案", ["假设结论的反面成立，推演其后果", "比较正反两种结论的解释力", "寻找正向结论无法解释的异常", "评估反转后的论证是否更简洁(Occam's Razor)"], 0.18),
        RefuteDimension.DARK_FOREST: ("安全加固方案", ["评估接受论证后的暴露面", "设计最坏情况下的止损方案", "识别博弈中的信息不对称", "增加可逆性，保留退出机制"], 0.20),
        RefuteDimension.BEHAVIORAL: ("偏差清除方案", ["列出可能存在的3-5个认知偏差", "对每个偏差设计去偏差检查", "寻找反面证据（主动搜索而非被动接受）", "用'事前验尸法'：假设决策失败，倒推原因"], 0.28),
    }

    def generate(self, parsed: ParsedArgument, refutation: MultiDimensionRefutation,
                 assessment: StrengthAssessment, debate: DebateResult,
                 repair: Optional[RepairedArgument] = None) -> SolutionSet:
        solutions = []
        for ref in refutation.refutations:
            fix = self.DIMENSION_FIXES.get(ref.dimension, ("通用改进方案", ["重新审视核心前提","补充支撑证据","验证隐含假设"], 0.15))
            solutions.append(Solution(fix[0], f"针对{ref.dimension.value}维: {ref.counter_argument[:50]}",
                fix[1], ref.counter_argument[:40], ref.dimension,
                1 if ref.strength > 0.85 else 2, fix[2]))
        for vuln in assessment.vulnerabilities[:3]:
            solutions.append(Solution(f"修复: {vuln[:20]}", f"解决: {vuln}",
                [f"针对'{vuln}'专项加固", "补充缺失的前提或证据", "重新验证修复后的论证强度"],
                vuln, RefuteDimension.REFUTATION, 3, 0.12))
        solutions.append(Solution("辩论驱动进化方案", f"基于{len(debate.rounds)}轮辩论: {debate.final_verdict[:60]}",
            [f"采纳进化论点: {debate.evolved_argument[:40]}", "针对辩论盲区补充验证", "在进化论点基础上重构论证"],
            debate.remaining_blind_spots[0] if debate.remaining_blind_spots else "辩论已解决主要问题",
            RefuteDimension.REVERSE_ARG, 1, 0.20))
        if repair:
            solutions.append(Solution("论证修复方案", repair.repair_rationale,
                [f"采用修复后论点: {repair.repaired_claim[:40]}"] +
                [f"补充: {p}" for p in repair.added_premises[:2]],
                repair.repair_rationale[:40], RefuteDimension.REFUTATION, 1, 0.25))
        solutions.sort(key=lambda s: s.priority)
        qw = [s for s in solutions if s.expected_improvement >= 0.2][:3]
        df = [s for s in solutions if s.expected_improvement < 0.2][:3]
        oa = (f"原始强度: {assessment.strength_grade}级({assessment.overall_strength:.0%}) | "
              f"辩论逼近度: {debate.truth_approximation:.0%} | 类型: {parsed.argument_type.value} | "
              f"领域: {parsed.context_domain} | 发现{len(assessment.detected_fallacies)}个谬误")
        if assessment.strength_grade in ("S","A"): ra = "论证强度较高，建议微调——重点修补1-2个最突出脆弱点"
        elif assessment.strength_grade == "B": ra = "论证中等强度，建议分两步——先解决关键缺陷，再加固推理链"
        elif assessment.strength_grade == "C": ra = "论证较弱，建议重构——从前提重新出发，逐条验证后再构建结论"
        else: ra = "论证极弱，建议推倒重来——当前结构无法支撑结论，需从根本假设开始反思"
        return SolutionSet(parsed.raw_text, solutions[:7], qw, df, oa, ra)


# ═══════════════════════════════════════════════════════════════
# 第八层: 批量反驳模式 (BatchRefuter) — v3.0 新增
# ═══════════════════════════════════════════════════════════════

@dataclass
class BatchContradiction:
    """两个论点之间的矛盾"""
    argument_a: str
    argument_b: str
    contradiction_type: str
    explanation: str
    severity: float

@dataclass
class BatchResult:
    """批量反驳结果"""
    arguments: List[str]
    individual_results: List[Any]  # List[RefuteCoreResult]
    contradictions: List[BatchContradiction]
    consistency_score: float
    strongest_argument_index: int
    weakest_argument_index: int
    overall_assessment: str

class BatchRefuter:
    """批量反驳模式——同时分析多个关联论点并找出矛盾"""

    def batch_refute(self, arguments: List[str], engine: Any) -> BatchResult:
        results = []
        for arg in arguments:
            results.append(engine.refute(arg))
        
        # 找矛盾
        contradictions = self._find_contradictions(arguments, results)
        
        # 一致性评分
        consistency = self._calculate_consistency(contradictions)
        
        # 最强/最弱论点
        strengths = [r.assessment.overall_strength for r in results]
        strongest_idx = strengths.index(max(strengths))
        weakest_idx = strengths.index(min(strengths))
        
        oa = (f"分析了{len(arguments)}个论点，发现{len(contradictions)}个矛盾，"
              f"一致性评分{consistency:.0%}，最强论点[{strongest_idx}]强度{max(strengths):.0%}，"
              f"最弱论点[{weakest_idx}]强度{min(strengths):.0%}")
        
        return BatchResult(arguments, results, contradictions, consistency,
                          strongest_idx, weakest_idx, oa)

    def _find_contradictions(self, args: List[str], results: List[Any]) -> List[BatchContradiction]:
        """v3.0.1: 重构矛盾检测 — 多层检测策略"""
        contradictions = []
        
        # 预定义的否定词对
        negation_pairs = [
            ("应该", "不应该"), ("必须", "不需要"), ("是", "不是"),
            ("会", "不会"), ("能", "不能"), ("好", "不好"), ("值得", "不值得"),
            ("应该", "不该"), ("要", "不要"),
        ]
        
        for i in range(len(args)):
            for j in range(i + 1, len(args)):
                text_i = args[i]
                text_j = args[j]
                
                # ─── 层级1: 直接否定词检测（最可靠） ───
                found_negation_conflict = False
                for pos, neg in negation_pairs:
                    if (pos in text_i and neg in text_j) or (neg in text_i and pos in text_j):
                        # 找到共同话题词
                        topic = self._find_common_topic(text_i, text_j)
                        contradictions.append(BatchContradiction(
                            text_i[:40], text_j[:40], "直接主张矛盾",
                            f"论点{i}包含'{pos}'而论点{j}包含'{neg}'，对{topic}持相反立场",
                            0.92
                        ))
                        found_negation_conflict = True
                        break
                
                if found_negation_conflict:
                    continue
                
                # ─── 层级2: 相同主体不同结论 ───
                subj_i = results[i].parsed_argument.claim_subject
                subj_j = results[j].parsed_argument.claim_subject
                
                # 模糊主体匹配：包含关系也算
                if subj_i and subj_j:
                    subject_match = (subj_i == subj_j or 
                                    (len(subj_i) > 2 and len(subj_j) > 2 and 
                                     (subj_i in subj_j or subj_j in subj_i)))
                    
                    if subject_match:
                        pred_i = results[i].parsed_argument.claim_predicate
                        pred_j = results[j].parsed_argument.claim_predicate
                        if pred_i != pred_j:
                            contradictions.append(BatchContradiction(
                                text_i[:40], text_j[:40], "主张矛盾",
                                f"同一主体'{subj_i}'在不同论点中得出不同结论: '{pred_i}' vs '{pred_j}'",
                                0.85
                            ))
                        continue
                
                # ─── 层级3: 核心关键词冲突 + 否定 ───
                claim_i = results[i].parsed_argument.core_claim
                claim_j = results[j].parsed_argument.core_claim
                neg_i = results[i].parsed_argument.negated_claim
                neg_j = results[j].parsed_argument.negated_claim
                
                # 论点A的核心主张与论点B的否定主张相似 → 矛盾
                if self._claim_similarity(claim_i, neg_j) > 0.5 or \
                   self._claim_similarity(claim_j, neg_i) > 0.5:
                    contradictions.append(BatchContradiction(
                        text_i[:40], text_j[:40], "核心主张互斥",
                        f"论点i的核心主张与论点j的否定主张存在语义重叠",
                        0.78
                    ))
                    continue
                
                # ─── 层级4: 关键词重叠+态度相反 ───
                kw_i = set(results[i].parsed_argument.keywords)
                kw_j = set(results[j].parsed_argument.keywords)
                common_kw = kw_i & kw_j
                
                if len(common_kw) >= 1 and any(kw in ["降价","价格","竞争","市场","投资"] for kw in common_kw):
                    # 有共同关键词但结论方向不同
                    att_i = self._detect_attitude(text_i)
                    att_j = self._detect_attitude(text_j)
                    if att_i != att_j and att_i != "neutral" and att_j != "neutral":
                        contradictions.append(BatchContradiction(
                            text_i[:40], text_j[:40], "态度不一致",
                            f"共同话题{list(common_kw)[:3]}上，两个论点态度分别为{att_i}和{att_j}",
                            0.65
                        ))
                        continue
                
                # ─── 层级5: 隐含假设冲突 ───
                assumptions_i = set(results[i].parsed_argument.implicit_assumptions)
                assumptions_j = set(results[j].parsed_argument.implicit_assumptions)
                
                for a in assumptions_i:
                    found_conflict = False
                    for b in assumptions_j:
                        if self._are_contradictory(a, b):
                            contradictions.append(BatchContradiction(
                                text_i[:40], text_j[:40], "假设冲突",
                                f"论点{i}假设'{a[:30]}'与论点{j}假设'{b[:30]}'互相矛盾",
                                0.70
                            ))
                            found_conflict = True
                            break
                    if found_conflict:
                        break
        
        return contradictions[:6]
    
    def _find_common_topic(self, text_a: str, text_b: str) -> str:
        """找两个文本的共同话题"""
        words_a = set(_RE_CHINESE_SHORT.findall(text_a))
        words_b = set(_RE_CHINESE_SHORT.findall(text_b))
        common = words_a & words_b
        if common:
            # 返回最长的一个
            return max(common, key=len)
        return "同一议题"
    
    def _claim_similarity(self, a: str, b: str) -> float:
        """简单文本相似度（基于共同字）""" 
        if not a or not b: return 0.0
        set_a = set(a.replace(" ", ""))
        set_b = set(b.replace(" ", ""))
        common = set_a & set_b
        total = set_a | set_b
        return len(common) / max(len(total), 1)
    
    def _detect_attitude(self, text: str) -> str:
        """v3.0.4: 改进态度检测 — 上下文感知，避免中性词误判"""
        positive_words = ["应该", "必须", "值得", "有效", "成功", "好", "重要", "优势", "建议", "推荐"]
        negative_words = ["不应该", "不该", "不能", "损害", "风险", "失败", "坏", "缺陷", "不可能", "有害", "损失"]
        # 上下文敏感的负面词 — 只在特定搭配中才算负面
        context_negative = [("有问题", "问题"), ("出了问题", "问题")]
        
        pos_count = sum(1 for w in positive_words if w in text)
        neg_count = sum(1 for w in negative_words if w in text)
        
        # 上下文敏感检测
        for pattern, _ in context_negative:
            if pattern in text:
                neg_count += 1
                break  # 避免重复计数
        
        # 单独"不"只在对立场景才算（避免"不同"等被误判）
        if "不" in text:
            # 排除"不同""不仅""不断""不如""不过"等中性用法
            neutral_uses = len(_RE_NEUTRAL_NOT.findall(text))
            bare_not = text.count("不") - neutral_uses
            # 如果"不"的次数远超已知否定词，额外算一些
            extra_neg = max(0, bare_not - neg_count - 1)
            neg_count += min(extra_neg, 2)
        
        if pos_count > neg_count * 1.5:
            return "支持"
        elif neg_count > pos_count * 1.5:
            return "反对"
        return "neutral"

    def _are_contradictory(self, a: str, b: str) -> bool:
        """简单检测两个假设是否互斥"""
        opposites = [("确定", "不确定"), ("理性", "非理性"), ("稳定", "变化"),
                     ("可控", "不可控"), ("客观", "主观"), ("普遍", "特定")]
        for p, q in opposites:
            if (p in a and q in b) or (q in a and p in b):
                return True
        return False

    def _calculate_consistency(self, contradictions: List[BatchContradiction]) -> float:
        if not contradictions: return 1.0
        penalty = sum(c.severity * 0.15 for c in contradictions)
        return max(0, 1.0 - penalty)


# ═══════════════════════════════════════════════════════════════
# 第九层: 驳心引擎主类 (RefuteCoreEngine) v3.0
# ═══════════════════════════════════════════════════════════════

@dataclass
class RefuteCoreResult:
    """驳心引擎完整输出 v3.0"""
    input_text: str
    engine_version: str
    timestamp: str
    parsed_argument: ParsedArgument
    refutation: MultiDimensionRefutation
    assessment: StrengthAssessment
    debate: DebateResult
    repair: RepairedArgument
    solutions: SolutionSet
    executive_summary: str
    risk_level: str
    key_takeaway: str

class RefuteCoreEngine:
    """
    驳心引擎 (RefuteCore) v3.2.0
    
    以反驳为核心驱动的论证智慧引擎。
    
    能力:
    1. 论证解析 — 拆解任意论点的论证结构（含主谓宾+领域+否定主张）
    2. 8大维度反驳 — 智能填充的反驳模板
    3. 强度评估 — 量化论证强度和漏洞
    4. 辩论对抗 — 上下文感知多轮辩论
    5. 论证修复 — 自动生成加固后论点
    6. 解决方案 — 从反驳到行动
    7. 批量反驳 — 多论点矛盾检测（通过batch_refute方法）
    
    v3.1 快速加载模式:
    - 预加载: 核心元数据（枚举/常量）— 类定义时自动完成，<0.01ms
    - 懒加载: 子组件按需实例化 — 首次调用时创建，之后缓存复用
    - 轻量级 __init__: 零子组件开销，实例化<0.05ms
    
    使用:
        engine = RefuteCoreEngine()
        result = engine.refute("我们应该投资这个项目因为市场很大")
        print(result.executive_summary)
        
        # 批量模式
        batch = engine.batch_refute(["论点1", "论点2", "论点3"])
        
        # 加载统计
        stats = engine.get_loading_stats()
    """
    
    VERSION = "3.2.0"
    
    # ─── 预加载常量: 类级定义，零实例化成本 ───
    _COMPONENT_MAP = {
        'parser': 'ArgumentParser',
        'strategist': 'RefutationStrategist',
        'assessor': 'ArgumentStrengthAssessor',
        'arena': 'DebateArena',
        'repair_engine': 'ArgumentRepair',
        'solution_generator': 'SolutionGenerator',
        'batch_refuter': 'BatchRefuter',
    }
    _COMPONENT_CLASSES = {
        'parser': ArgumentParser,
        'strategist': RefutationStrategist,
        'assessor': ArgumentStrengthAssessor,
        'arena': DebateArena,
        'repair_engine': ArgumentRepair,
        'solution_generator': SolutionGenerator,
        'batch_refuter': BatchRefuter,
    }
    
    def __init__(self):
        # v3.1: 轻量级初始化 — 零子组件开销
        self._components: Dict[str, Any] = {}
        self._init_time_ms: float = 0.0
        self._loaded_components: List[str] = []
        # v7.1: 解析结果缓存（相同文本5分钟内直接返回）
        self._parse_cache: Dict[str, Tuple[float, Any]] = {}
        self._parse_cache_max = 64
    
    def __getattr__(self, name: str) -> Any:
        """v3.1: 懒加载 — 首次访问子组件时才实例化"""
        if name in self._COMPONENT_MAP:
            return self._get_component(name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
    
    def _get_component(self, name: str) -> Any:
        """获取或懒加载子组件"""
        if name not in self._components:
            cls = self._COMPONENT_CLASSES[name]
            self._components[name] = cls()
            self._loaded_components.append(name)
        return self._components[name]
    
    @property
    def is_fully_loaded(self) -> bool:
        """是否所有子组件都已加载"""
        return len(self._components) == len(self._COMPONENT_MAP)
    
    def preload_all(self) -> None:
        """预加载所有子组件（可选，通常不需要手动调用）"""
        for name in self._COMPONENT_MAP:
            self._get_component(name)
    
    def get_loading_stats(self) -> Dict[str, Any]:
        """获取加载统计信息"""
        total = len(self._COMPONENT_MAP)
        loaded = len(self._components)
        return {
            "version": self.VERSION,
            "total_components": total,
            "loaded_components": loaded,
            "load_ratio": f"{loaded}/{total}",
            "component_status": {
                name: name in self._components for name in self._COMPONENT_MAP
            },
            "init_time_ms": self._init_time_ms,
        }
    
    def refute(self, text: str, focus_dimensions: Optional[List[RefuteDimension]] = None,
               top_n: int = 3, enable_debate: bool = True, enable_repair: bool = True,
               enable_solutions: bool = True) -> RefuteCoreResult:
        """核心方法: 对任意论点进行完整反驳分析"""
        timestamp = datetime.now().isoformat()
        
        # v3.0.2: 输入防护
        if not text or not isinstance(text, str):
            text = "未提供有效论点"
        text = text.strip()
        if not text:
            text = "空论点"
        
        # v7.1: 解析缓存检查（相同输入5分钟内直接返回）
        cache_key = hashlib.md5(text.encode('utf-8')).hexdigest()
        cached = self._parse_cache.get(cache_key)
        if cached is not None:
            ts, result = cached
            if time.time() - ts < 300:  # 5分钟TTL
                return result
            del self._parse_cache[cache_key]
        
        # 解析论证
        logger.info(f"驳心引擎: 解析论证 → '{text[:30]}...'")
        parsed = self.parser.parse(text)
        
        # v7.1: LLM 增强论证解析（当 LLM 可用时）
        llm_enhancement = self._llm_enhance_parsed(parsed, text)
        
        # v3.2.0: Web 搜索增强 — 为反驳提供最新事实依据
        web_evidence = self._web_search_enhance(text, parsed)
        
        # 生成多维度反驳
        logger.info("驳心引擎: 生成多维度反驳")
        refutation = self.strategist.generate_refutations(parsed, top_n=top_n, focus_dimensions=focus_dimensions)
        
        # v3.2.0: 将 Web 证据注入反驳结果
        if web_evidence:
            refutation = self._inject_web_evidence(refutation, web_evidence)
        
        # 评估论证强度
        logger.info("驳心引擎: 评估论证强度")
        assessment = self.assessor.assess(parsed, refutation)
        
        # v7.1: LLM 增强反驳质量评估（当 LLM 可用时）
        llm_assessment = self._llm_enhance_assessment(parsed, refutation, assessment, text)
        if llm_assessment:
            # 合并 LLM 评估结果到最终 assessment
            assessment = llm_assessment
        
        # 辩论对抗
        if enable_debate:
            logger.info("驳心引擎: 启动辩论对抗")
            debate = self.arena.debate(parsed, refutation, assessment)
        else:
            debate = DebateResult(text, [], "辩论模式未启用", assessment.overall_strength, ["未进行辩论对抗"], parsed.core_claim)
        
        # 论证修复
        if enable_repair:
            logger.info("驳心引擎: 修复论证")
            repair = self.repair_engine.repair(parsed, refutation, assessment, debate)
        else:
            repair = RepairedArgument(parsed.core_claim, parsed.core_claim, [], [], [], [], assessment.overall_strength, "修复未启用")
        
        # 解决方案
        if enable_solutions:
            logger.info("驳心引擎: 生成解决方案")
            solutions = self.solution_generator.generate(parsed, refutation, assessment, debate, repair)
        else:
            solutions = SolutionSet(text, [], [], [], "解决方案生成未启用", "")
        
        # 生成摘要
        exec_summary = self._gen_exec_summary(parsed, refutation, assessment, debate, repair, solutions)
        risk_level = self._calc_risk_level(assessment)
        key_takeaway = self._gen_key_takeaway(parsed, refutation, assessment, debate, repair)
        
        logger.info(f"驳心引擎: 分析完成 — 强度{assessment.strength_grade}级, 风险{risk_level}")
        
        result = RefuteCoreResult(text, self.VERSION, timestamp, parsed, refutation, assessment,
            debate, repair, solutions, exec_summary, risk_level, key_takeaway)
        
        # v7.1: 存入解析缓存
        if len(self._parse_cache) >= self._parse_cache_max:
            # LRU淘汰最旧的25%
            sorted_keys = sorted(self._parse_cache.keys(), key=lambda k: self._parse_cache[k][0])
            for k in sorted_keys[:max(1, len(sorted_keys)//4)]:
                del self._parse_cache[k]
        self._parse_cache[cache_key] = (time.time(), result)
        
        return result
    
    def _llm_enhance_parsed(self, parsed: 'ParsedArgument', original_text: str) -> Optional[Dict]:
        """v7.1: 使用 LLM 增强论证解析"""
        try:
            from knowledge_cells.llm_rule_layer import call_module_llm
            prompt = f"""请分析以下论证的结构：

论证内容：{original_text[:500]}

请指出：
1. 核心论点是什么？
2. 前提假设有哪些？
3. 论证中可能存在的逻辑漏洞

回复格式简洁，每点一行。"""

            response = call_module_llm("RefuteCore", prompt, max_tokens=300)
            return {"llm_analysis": response, "source": "llm_enhanced"}
        except Exception as e:
            logger.debug(f"[RefuteCore] LLM增强解析失败: {e}")
            return None
    
    def _llm_enhance_assessment(self, parsed: 'ParsedArgument', refutation: 'MultiDimensionRefutation',
                                  assessment: 'StrengthAssessment', original_text: str) -> Optional['StrengthAssessment']:
        """v7.1: 使用 LLM 辅助评估论证强度"""
        try:
            from knowledge_cells.llm_rule_layer import call_module_llm
            
            # 构建论证摘要
            core_claim = parsed.core_claim or "未知论点"
            refutation_count = len(refutation.refutations) if hasattr(refutation, 'refutations') else 0
            strongest = refutation.strongest_refutation.dimension.value if hasattr(refutation, 'strongest_refutation') else "未知"
            
            prompt = f"""请评估以下论证的强度：

核心论点：{core_claim[:200]}
反驳维度数：{refutation_count}
最强反驳维度：{strongest}

请在以下等级中选择一个：S(极强) / A(强) / B(中等) / C(较弱) / D(弱) / F(极弱)
并简要说明理由。"""

            response = call_module_llm("RefuteCore", prompt, max_tokens=200)
            
            # 尝试从 LLM 响应中提取强度等级
            grade_map = {"S": "S", "A": "A", "B": "B", "C": "C", "D": "D", "F": "F"}
            for grade in ["S", "A", "B", "C", "D", "F"]:
                if f"{grade}(" in response or f"{grade}级" in response or f"{grade}：" in response:
                    # 如果 LLM 认为论证比规则引擎评估的更弱，使用 LLM 的评估
                    llm_strength_map = {"S": 0.95, "A": 0.85, "B": 0.70, "C": 0.55, "D": 0.40, "F": 0.20}
                    llm_strength = llm_strength_map.get(grade, assessment.overall_strength)
                    
                    # 只有当 LLM 评估与规则引擎差异较大时才使用
                    if abs(llm_strength - assessment.overall_strength) > 0.15:
                        logger.info(f"[RefuteCore] LLM评估强度{grade}级({llm_strength:.0%}) vs 规则引擎{assessment.strength_grade}级({assessment.overall_strength:.0%})，使用LLM评估")
                        # 创建新的 assessment 对象
                        new_assessment = StrengthAssessment(
                            core_claim=parsed.core_claim,
                            overall_strength=llm_strength,
                            strength_grade=grade,
                            premise_strength=llm_strength * 0.95,
                            reasoning_strength=llm_strength * 0.90,
                            evidence_strength=llm_strength * 0.85,
                        )
                        return new_assessment
                    break
        except Exception as e:
            logger.debug(f"[RefuteCore] LLM增强评估失败: {e}")
        return None
    
    def _web_search_enhance(self, text: str, parsed: 'ParsedArgument') -> Optional[List[Dict]]:
        """v3.2.0: Web 搜索增强 — 为反驳提供最新事实依据

        当论点涉及实时数据、最新趋势或可验证事实时，
        通过网络搜索获取相关证据来增强反驳质量。

        触发条件：
        - 论点包含时间敏感关键词（最新、最近、今天等）
        - 论点包含可验证的数据/统计/研究声明
        - 论点涉及具体人/公司/事件
        """
        # 触发关键词检测
        time_keywords = ["最新", "最近", "今天", "昨日", "本周", "本月", "2024", "2025", "2026"]
        data_keywords = ["数据", "统计", "报告", "研究", "调查", "排名", "增长", "下降"]
        entity_indicators = ["公司", "企业", "品牌", "平台", "产品"]

        should_search = (
            any(kw in text for kw in time_keywords)
            or any(kw in text for kw in data_keywords)
            or (parsed.claim_subject and any(ind in (parsed.claim_subject or "") for ind in entity_indicators))
        )

        if not should_search:
            return None

        try:
            from knowledge_cells.web_integration import RefuteCoreWeb
            web = RefuteCoreWeb()
            results = web.search_evidence(text, max_results=3)
            if results:
                logger.info(f"[RefuteCore] Web搜索增强: 获取{len(results)}条相关证据")
                return results
        except ImportError:
            pass
        except Exception as e:
            logger.debug(f"[RefuteCore] Web搜索增强失败: {e}")

        return None

    def _inject_web_evidence(self, refutation: 'MultiDimensionRefutation',
                              web_evidence: List[Dict]) -> 'MultiDimensionRefutation':
        """v3.2.0: 将 Web 证据注入反驳结果

        将网络搜索获取的事实证据附加到最强反驳的支撑论据中，
        使反驳从"纯逻辑推演"升级为"逻辑+事实双重支撑"。
        """
        if not web_evidence or not hasattr(refutation, 'refutations') or not refutation.refutations:
            return refutation

        # 为前 N 个反驳附加 Web 证据
        evidence_summary = "; ".join(
            e.get("snippet", e.get("title", ""))[:80] for e in web_evidence[:3]
        )

        for i, ref in enumerate(refutation.refutations):
            if i >= 3:  # 只增强前3个反驳
                break
            # 附加 Web 证据到逻辑结构
            if hasattr(ref, 'logical_structure') and evidence_summary:
                ref.logical_structure = f"{ref.logical_structure} [Web证据: {evidence_summary[:120]}]"

        return refutation
    
    def batch_refute(self, arguments: List[str]) -> BatchResult:
        """批量反驳——同时分析多个关联论点并找出矛盾"""
        return self.batch_refuter.batch_refute(arguments, self)
    
    def quick_refute_text(self, text: str) -> str:
        """快速反驳 — 返回格式化文本"""
        result = self.refute(text)
        return self._format_result(result)
    
    def quick_refute_markdown(self, text: str) -> str:
        """快速反驳 — 返回Markdown格式"""
        result = self.refute(text)
        return self._format_markdown(result)
    
    def get_dimension_info(self, dim: RefuteDimension) -> Dict[str, Any]:
        cfg = RefutationStrategist.STRATEGIES.get(dim, {})
        return {"维度": dim.value, "名称": cfg.get("name", ""), "核心策略": cfg.get("core_tactic", ""),
                "可用策略数": len(cfg.get("strategies", [])), "可检测谬误": [f.value for f in cfg.get("fallacies", [])]}
    
    def get_engine_info(self) -> Dict[str, Any]:
        return {"名称": "驳心引擎 RefuteCore", "版本": self.VERSION, "维度数": len(RefuteDimension),
                "维度列表": [d.value for d in RefuteDimension], "谬误类型数": len(FallacyType),
                "能力": ["论证解析","8大维度反驳","强度评估","辩论对抗","论证修复","解决方案生成","批量反驳"]}
    
    # ─── 内部方法 ───
    
    def _gen_exec_summary(self, p, r, a, d, repair, s) -> str:
        return (f"论证类型[{p.argument_type.value}] 领域[{p.context_domain}] "
                f"强度{a.strength_grade}级({a.overall_strength:.0%}) "
                f"脆弱性{p.vulnerability_score:.0%} | "
                f"最强反驳[{r.strongest_refutation.dimension.value}] "
                f"强度{r.strongest_refutation.strength:.0%} | "
                f"关键缺陷: {r.critical_flaw[:40]} | "
                f"辩论逼近度{d.truth_approximation:.0%} | "
                f"修复后预估{repair.repaired_strength_estimate:.0%}")
    
    def _calc_risk_level(self, a: StrengthAssessment) -> str:
        if a.overall_strength < 0.3: return "🔴 极高风险"
        if a.overall_strength < 0.5: return "🟠 高风险"
        if a.overall_strength < 0.7: return "🟡 中等风险"
        return "🟢 低风险"
    
    def _gen_key_takeaway(self, p, r, a, d, repair) -> str:
        if a.strength_grade in ("S","A"):
            return f"论证强度{a.strength_grade}级，基本成立。但需注意: {r.key_insight[:50]}"
        elif a.strength_grade == "B":
            return f"论证中等强度，需修正。核心问题: {r.critical_flaw[:50]}。建议: {repair.repaired_claim[:40]}"
        else:
            return f"论证较弱({a.strength_grade})，{r.critical_flaw[:50]}。建议推倒重来或采纳修复版: {repair.repaired_claim[:40]}"
    
    def _format_result(self, result: RefuteCoreResult) -> str:
        lines = [
            "╔" + "═" * 58 + "╗",
            f"║  驳心引擎 RefuteCore {result.engine_version}",
            f"║  📋 输入: {result.input_text[:50]}",
            f"║  🎯 类型: {result.parsed_argument.argument_type.value} | 领域: {result.parsed_argument.context_domain} | 强度: {result.assessment.strength_grade}级 | 风险: {result.risk_level[:6]}",
            "╠" + "═" * 58 + "╣",
            "║  【反驳结果】",
        ]
        for i, r in enumerate(result.refutation.refutations[:3], 1):
            lines.append(f"║  {i}. [{r.dimension.value}] {r.counter_argument[:50]}")
            lines.append(f"║     策略: {r.strategy[:50]}  强度: {r.strength:.0%}")
        lines += ["╠" + "═" * 58 + "╣", "║  【强度评估】",
            f"║  总体: {result.assessment.overall_strength:.0%} | 前提: {result.assessment.premise_strength:.0%} | 推理: {result.assessment.reasoning_strength:.0%}",
            f"║  证据: {result.assessment.evidence_strength:.0%} | 假设: {result.assessment.assumption_strength:.0%}"]
        if result.assessment.detected_fallacies:
            lines.append(f"║  谬误: {'、'.join(f.value for f in result.assessment.detected_fallacies[:3])}")
        lines += ["╠" + "═" * 58 + "╣", "║  【辩论结果】",
            f"║  {result.debate.final_verdict[:55]}",
            f"║  真理逼近度: {result.debate.truth_approximation:.0%}",
            f"║  进化论点: {result.debate.evolved_argument[:45]}"]
        lines += ["╠" + "═" * 58 + "╣", "║  【论证修复】",
            f"║  修复后: {result.repair.repaired_claim[:50]}",
            f"║  修复后预估强度: {result.repair.repaired_strength_estimate:.0%}"]
        lines += ["╠" + "═" * 58 + "╣", "║  【解决方案】"]
        for i, s in enumerate(result.solutions.solutions[:3], 1):
            lines.append(f"║  {i}. {s.title} (优先级:{s.priority}, 改善:{s.expected_improvement:.0%})")
            if s.actions: lines.append(f"║     → {s.actions[0][:50]}")
        lines += ["╠" + "═" * 58 + "╣",
            f"║  💡 核心结论: {result.key_takeaway[:55]}",
            "╚" + "═" * 58 + "╝"]
        return "\n".join(lines)
    
    def _format_markdown(self, result: RefuteCoreResult) -> str:
        """v3.0.2: Markdown输出 — 增加截断保护和格式健壮性"""
        p = result.parsed_argument
        a = result.assessment
        r = result.refutation
        d = result.debate
        repair = result.repair
        s = result.solutions
        
        # 截断辅助函数
        def tr(s: str, n: int=80) -> str:
            """截断字符串到指定长度，不截断中文字符"""
            if not s: return "(空)"
            if len(s) <= n: return s
            # 粗略截断（中文2字符/字）
            return s[:n] + "..."
        
        def safe_join(items, sep="、", limit=5):
            if not items: return "(无)"
            return sep.join(str(x)[:30] for x in items[:limit])
        
        md = f"""# 驳心引擎分析报告

## 📋 基本信息
- **输入**: {tr(result.input_text, 100)}
- **类型**: {p.argument_type.value} | **领域**: {p.context_domain}
- **主语**: {tr(p.claim_subject, 20)} | **谓语**: {tr(p.claim_predicate, 10)} | **宾语**: {tr(p.claim_object, 20)}
- **否定主张**: {tr(p.negated_claim, 50)}
- **强度**: {a.strength_grade}级({a.overall_strength:.0%}) | **风险**: {result.risk_level}

## 🎯 反驳结果
"""
        for i, ref in enumerate(r.refutations[:3], 1):
            md += f"""### {i}. [{ref.dimension.value}] {tr(ref.strategy, 40)}
- **反驳论点**: {tr(ref.counter_argument, 120)}
- **反驳强度**: {ref.strength:.0%}
- **逻辑链**: {tr(ref.logical_structure, 80)}
- **证据**: {tr(ref.evidence, 100)}
"""
            if ref.fallacy_exposed:
                md += f"- **揭露谬误**: {ref.fallacy_exposed.value}\n"
        
        md += f"""
## 📊 强度评估
| 维度 | 得分 |
|------|------|
| 总体 | {a.overall_strength:.0%} |
| 前提 | {a.premise_strength:.0%} |
| 推理 | {a.reasoning_strength:.0%} |
| 证据 | {a.evidence_strength:.0%} |
| 假设 | {a.assumption_strength:.0%} |

**脆弱点**: {safe_join(a.vulnerabilities)}
**谬误**: {safe_join(a.detected_fallacies)}

## ⚔️ 辩论结果
- **裁决**: {tr(d.final_verdict, 80)}
- **真理逼近度**: {d.truth_approximation:.0%}
- **进化论点**: {tr(d.evolved_argument, 60)}
"""
        for rnd in d.rounds:
            md += f"""### 第{rnd.round_number}轮
- 正方: {tr(rnd.proposer_argument, 70)}
- 反方: {tr(rnd.refuter_counter, 70)}
- 正方防御: {tr(rnd.proposer_defense, 70)}
- 裁决: {tr(rnd.round_verdict, 50)}
"""
        
        md += f"""
## 🔧 论证修复
- **修复后主张**: {tr(repair.repaired_claim, 60)}
- **修复后预估强度**: {repair.repaired_strength_estimate:.0%}
- **新增前提**: {safe_join(repair.added_premises)}
- **限定条件**: {safe_join(repair.added_conditions)}
- **证据建议**: {safe_join(repair.evidence_suggestions)}

## 💡 核心结论
{tr(result.key_takeaway, 100)}
"""
        return md


# ═══════════════════════════════════════════════════════════════
# 全局单例与便捷函数
# ═══════════════════════════════════════════════════════════════

_engine_instance: Optional[RefuteCoreEngine] = None
_engine_lock = __import__('threading').Lock()

def get_refute_core() -> RefuteCoreEngine:
    global _engine_instance
    if _engine_instance is None:
        with _engine_lock:
            if _engine_instance is None:
                _engine_instance = RefuteCoreEngine()
    return _engine_instance

def quick_refute(text: str) -> str:
    """便捷函数: 快速反驳（格式化文本）"""
    return get_refute_core().quick_refute_text(text)

def quick_refute_md(text: str) -> str:
    """便捷函数: 快速反驳（Markdown格式）"""
    return get_refute_core().quick_refute_markdown(text)

def refute_and_solve(text: str, focus_dimensions: Optional[List[RefuteDimension]] = None) -> RefuteCoreResult:
    """便捷函数: 完整反驳分析（返回结构化结果）"""
    return get_refute_core().refute(text, focus_dimensions=focus_dimensions)

def batch_refute(arguments: List[str]) -> BatchResult:
    """便捷函数: 批量反驳"""
    return get_refute_core().batch_refute(arguments)


# ═══════════════════════════════════════════════════════════════
# v3.1.0: 快速加载性能基准测试
# ═══════════════════════════════════════════════════════════════

def benchmark_loading(iterations: int = 10) -> Dict[str, Any]:
    """
    RefuteCore v3.1.0 快速加载基准测试
    
    测试项:
    1. 空实例化 (引擎创建，不触发任何子组件)
    2. 全量预加载 (preload_all)
    3. 单次反驳首字延迟 (parse + refute 首次调用)
    4. 二次反驳延迟 (后续调用，所有组件已缓存)
    
    返回: {
        "cold_init": {"avg_ms": ..., "min_ms": ..., "max_ms": ...},
        "preload_all": {"avg_ms": ..., ...},
        "first_refute": {"avg_ms": ..., ...},
        "cached_refute": {"avg_ms": ..., ...},
    }
    """
    import time
    
    results: Dict[str, Any] = {}
    
    # 1. 空实例化
    init_times = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        _engine_instance_backup = _engine_instance
        engine = RefuteCoreEngine()
        elapsed = (time.perf_counter() - t0) * 1000
        init_times.append(elapsed)
        # 不影响全局单例
        if _engine_instance_backup is not None:
            pass  # 恢复在循环外
    results["cold_init"] = {
        "avg_ms": round(sum(init_times) / len(init_times), 4),
        "min_ms": round(min(init_times), 4),
        "max_ms": round(max(init_times), 4),
    }
    
    # 2. 全量预加载
    preload_times = []
    for _ in range(iterations):
        engine = RefuteCoreEngine()
        t0 = time.perf_counter()
        engine.preload_all()
        elapsed = (time.perf_counter() - t0) * 1000
        preload_times.append(elapsed)
    results["preload_all"] = {
        "avg_ms": round(sum(preload_times) / len(preload_times), 4),
        "min_ms": round(min(preload_times), 4),
        "max_ms": round(max(preload_times), 4),
    }
    
    # 3. 首次反驳（冷启动 + 懒加载）
    first_times = []
    test_text = "我们应该立即投资这个项目，因为市场前景非常好"
    for _ in range(iterations):
        engine = RefuteCoreEngine()  # 空实例
        t0 = time.perf_counter()
        _ = engine.refute(test_text)  # 触发所有懒加载
        elapsed = (time.perf_counter() - t0) * 1000
        first_times.append(elapsed)
    results["first_refute"] = {
        "avg_ms": round(sum(first_times) / len(first_times), 4),
        "min_ms": round(min(first_times), 4),
        "max_ms": round(max(first_times), 4),
    }
    
    # 4. 缓存反驳（所有组件已加载）
    engine = RefuteCoreEngine()
    engine.refute(test_text)  # 预热
    cached_times = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        _ = engine.refute(test_text)
        elapsed = (time.perf_counter() - t0) * 1000
        cached_times.append(elapsed)
    results["cached_refute"] = {
        "avg_ms": round(sum(cached_times) / len(cached_times), 4),
        "min_ms": round(min(cached_times), 4),
        "max_ms": round(max(cached_times), 4),
    }
    
    return results
