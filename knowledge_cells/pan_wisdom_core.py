"""
Pan-Wisdom Tree 核心模块 V2.0.0
万法智慧树 - 预加载+懒加载快速模式

特性:
- 42个智慧学派 (WisdomSchool)
- 165个问题类型 (ProblemType)
- 智能问题类型识别（L1预加载正则）
- 学派推荐与融合（L2 LRU缓存）
- 与神行轨集成（L3按需加载）
- 四层加载架构：L0（瞬时）/L1(<1ms)/L2(<5ms)/L3(按需)

使用方式:
    from knowledge_cells.pan_wisdom_core import (
        WisdomSchool, ProblemType,
        get_pan_wisdom_tree,
        solve_with_wisdom,
        preload,     # 可选：手动触发预加载
    )
    
    # 可选：手动预加载（推荐在应用启动时调用一次）
    preload()
    
    result = solve_with_wisdom("如何提升公司GMV？")
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import re
import uuid
import os
import json
import threading

# 导入懒加载模块
from .pan_wisdom_lazy_loader import (
    PanWisdomPreloader,
    PanWisdomLRUCache,
    PanWisdomOnDemandLoader,
    preload_pan_wisdom,
    get_pan_wisdom_cache,
    get_pan_wisdom_on_demand,
    is_pan_wisdom_ready,
    get_pan_wisdom_load_info,
    clear_pan_wisdom_cache,
    benchmark_pan_wisdom_load,
)

# 网络搜索导入（延迟导入，避免循环依赖）
_web_search_available: bool = None  # None = 未检测，True/False = 已检测

# 向后兼容别名
preload = preload_pan_wisdom
is_ready = lambda: PanWisdomPreloader.is_preloaded()


# ============================================================
# 枚举定义 - WisdomSchool (42个智慧学派)
# ============================================================

class WisdomSchool(Enum):
    """智慧学派 S1.0 - 42个学派"""
    # 东方哲学经典 (8)
    CONFUCIAN = "儒家"
    DAOIST = "道家"
    BUDDHIST = "佛家"
    SUFU = "素书"
    MILITARY = "兵法"
    LVSHI = "吕氏春秋"
    HONGMING = "辜鸿铭"
    METAPHYSICS = "术数时空"

    # 增长与行业 (3)  — v2.0.0 新增
    GROWTH_STRATEGY = "增长战略"
    INDUSTRY_WISDOM = "行业智慧"
    MARKETING = "市场营销"
    
    # 文明与科幻 (5)
    CIVILIZATION = "文明演化"
    CIV_WAR_ECONOMY = "文明经战"
    SCI_FI = "科幻思维"
    GROWTH = "成长思维"
    MYTHOLOGY = "神话智慧"
    
    # 文化与叙事 (3)
    LITERARY = "文学叙事"
    ANTHROPOLOGY = "人类学"
    BEHAVIOR = "行为塑造"
    
    # 思维方法 (6)
    SCIENCE = "科学思维"
    SOCIAL_SCIENCE = "社会科学"
    YANGMING = "王阳明xinxue"
    DEWEY = "杜威反省思维"
    TOP_METHODS = "顶级思维法"
    NATURAL_SCIENCE = "自然科学"
    
    # 中国消费与WCC (2)
    CHINESE_CONSUMER = "中国社会消费文化"
    WCC = "WCC智慧演化"
    
    # 历史思想 (1)
    HISTORICAL_THOUGHT = "历史思想三维度"
    
    # V6.0 第二阶段新增 (5)
    PSYCHOLOGY = "心理学"
    SYSTEMS = "系统论"
    MANAGEMENT = "管理学"
    ZONGHENG = "纵横家"
    MOZI = "墨家"
    FAJIA = "法家"
    
    # V6.0 第三阶段新增 (4)
    ECONOMICS = "经济学"
    MINGJIA = "名家"
    WUXING = "阴阳家"
    COMPLEXITY = "复杂性科学"
    
    # V6.2 社会科学智慧版 (8)
    SOCIOLOGY = "社会学"
    BEHAVIORAL_ECONOMICS = "行为经济学"
    COMMUNICATION = "传播学"
    CULTURAL_ANTHROPOLOGY = "文化人类学"
    POLITICAL_ECONOMICS = "政治经济学"
    ORGANIZATIONAL_PSYCHOLOGY = "组织心理学"
    SOCIAL_PSYCHOLOGY = "社会心理学"


# ============================================================
# 枚举定义 - ProblemType (165个问题类型)
# ============================================================

class ProblemType(Enum):
    """问题类型 S1.0 - 165个问题类型"""
    # 儒家 (5)
    ETHICAL = "伦理道德"
    GOVERNANCE = "组织治理"
    TALENT = "人才选用"
    CULTURE = "文化传承"
    CONFUCIAN_SUB_SCHOOL = "儒家子学派应用"
    
    # 道家 (8)
    STRATEGY = "战略转型"
    CRISIS = "危机处理"
    CHANGE = "变革管理"
    BALANCE = "阴阳平衡"
    TIMING = "时机判断"
    ENVIRONMENT = "环境布局"
    PATTERN = "结构格局"
    DAOIST_SUB_SCHOOL = "道家子学派应用"
    
    # 佛家 (4)
    MINDSET = "心态调适"
    HARMONY = "团队和谐"
    INTEREST = "利益协调"
    LONGTERM = "长期规划"
    BUDDHIST_SUB_SCHOOL = "佛家子学派应用"
    
    # 素书 (4)
    LEADERSHIP = "领导决策"
    RISK = "风险管理"
    FORTUNE = "福祸评估"
    PERSONNEL = "人才识别"
    
    # 兵法 (8)
    COMPETITION = "竞争策略"
    ATTACK = "市场攻击"
    DEFENSE = "市场防御"
    NEGOTIATION = "谈判博弈"
    WAR_ECONOMY_NEXUS = "经战主链"
    STATE_CAPACITY = "国家能力"
    INSTITUTIONAL_SEDIMENTATION = "制度沉淀"
    MILITARY_SUB_SCHOOL = "兵法子学派应用"
    
    # 吕氏春秋 (3)
    PUBLIC_INTEREST = "公私抉择"
    SEASONAL = "时令管理"
    YINYANG = "阴阳调和"
    
    # 科幻思维 (3)
    DIMENSION = "维度超越"
    SURVIVAL = "生存法则"
    SCALE = "尺度思维"
    
    # 成长思维 (3)
    GROWTH_MINDSET = "成长突破"
    REVERSE = "逆向思考"
    CLOSED_LOOP = "闭环执行"
    
    # 神话智慧 (3)
    CREATION_MYTH = "创世叙事"
    APOCALYPSE = "灭世危机"
    CYCLICAL = "循环哲学"
    
    # 文学叙事 (3)
    NARRATIVE = "叙事构建"
    RESILIENCE = "韧性评估"
    CHARACTER = "人物分析"
    
    # 人类学 (3)
    CROSS_CULTURE = "跨文化沟通"
    RITUAL = "仪式分析"
    CULTURAL_CHANGE = "文化变迁"
    
    # 行为塑造 (3)
    HABIT = "习惯设计"
    WILLPOWER = "自控力管理"
    NUDGE = "助推设计"
    
    # 科学思维 (3)
    SCIENTIFIC_METHOD = "科学验证"
    SYSTEM_THINKING = "系统分析"
    EVIDENCE = "证据评估"
    
    # 社会科学 (4)
    MARKETING = "营销策略"
    MARKET_ANALYSIS = "市场分析"
    SOCIAL_DEVELOPMENT = "社会发展"
    PSYCHOLOGICAL_INSIGHT = "心理洞察"
    
    # 营销战略 (4)
    CONSUMER_MARKETING = "C端营销"
    BRAND_STRATEGY = "品牌战略"
    SOCIAL_STABILITY = "社会稳定"
    
    # 自然科学 (5)
    PHYSICS_ANALYSIS = "物理分析"
    LIFE_SCIENCE = "生命科学"
    EARTH_SYSTEM = "地球系统"
    COSMOS_EXPLORATION = "宇宙探索"
    SCALE_CROSSING = "跨尺度思维"
    
    # WCC智慧演化 (7)
    META_PERSPECTIVE = "元视角升维"
    CIVILIZATION_ANALYSIS = "文明诊断"
    COSMIC_COGNITION = "宇宙认知"
    SCALE_TRANSFORMATION = "尺度转换"
    WORLDVIEW_SHIFT = "世界观转换"
    WISDOM_EVOLUTION = "智慧演化"
    TECH_EVOLUTION = "技术进化"
    
    # 历史思想 (6)
    HISTORICAL_ANALYSIS = "历史分析"
    THOUGHT_EVOLUTION = "思想演进"
    ECONOMIC_EVOLUTION = "经济演进"
    TECH_HISTORY = "科技演进"
    CROSS_DIMENSION = "跨维度洞察"
    PARADIGM_SHIFT = "范式转换"
    
    # 心理学 (8)
    PERSONALITY_ANALYSIS = "人格分析"
    GROUP_DYNAMICS = "群体动力学"
    COGNITIVE_BIAS = "认知偏差识别"
    MOTIVATION_ANALYSIS = "动机分析"
    PSYCHOLOGICAL_ARITHMETIC = "心理运算"
    TRAUMA_HEALING = "心理创伤修复"
    SELF_ACTUALIZATION = "自我实现"
    INTERPERSONAL_RELATIONSHIP = "人际关系处理"
    
    # 系统论 (5)
    COMPLEX_SYSTEM = "复杂系统建模"
    FEEDBACK_LOOP = "反馈回路设计"
    EMERGENT_BEHAVIOR = "涌现行为预测"
    SYSTEM_EQUILIBRIUM = "系统均衡分析"
    ADAPTIVE_SYSTEM = "自适应系统优化"
    
    # 管理学 (6)
    STRATEGIC_PLANNING = "战略规划制定"
    ORGANIZATIONAL_DESIGN = "组织架构设计"
    PERFORMANCE_MANAGEMENT = "绩效管理体系"
    KNOWLEDGE_MANAGEMENT = "知识管理体系"
    CHANGE_MANAGEMENT = "变革管理实施"
    INNOVATION_MANAGEMENT = "创新管理推进"
    
    # 纵横家 (3)
    DIPLOMATIC_NEGOTIATION = "外交谈判策略"
    ALLIANCE_BUILDING = "联盟构建策略"
    POWER_BALANCE = "权力平衡博弈"
    
    # 墨家 (5)
    ENGINEERING_INNOVATION = "工程技术创新"
    COST_OPTIMIZATION = "成本效率优化"
    UNIVERSAL_BENEFIT = "普惠利益设计"
    DEFENSE_FORTIFICATION = "防御工事设计"
    LOGICAL_DEDUCTION = "逻辑推理论证"
    
    # 法家 (6)
    INSTITUTIONAL_DESIGN = "制度体系设计"
    LAW_ENFORCEMENT = "法治执行策略"
    POWER_STRUCTURING = "权力架构设计"
    REWARD_PUNISHMENT = "赏罚激励机制"
    HUMAN_NATURE_ANALYSIS = "人性利害分析"
    STATE_CONSOLIDATION = "国家集权巩固"
    
    # 经济学 (5)
    RESOURCE_ALLOCATION = "资源配置优化"
    SUPPLY_DEMAND_BALANCE = "供需平衡分析"
    ECONOMIC_INCENTIVE = "经济激励机制设计"
    MARKET_EFFICIENCY = "市场效率评估"
    INVESTMENT_DECISION = "投资决策分析"
    
    # 名家 (3)
    LOGICAL_PARADOX = "逻辑悖论分析"
    CLASSIFICATION_REFINEMENT = "名实关系辨析"
    DIALECTICAL_REASONING = "辩证推理应用"
    
    # 阴阳家 (5)
    WUXING_ANALYSIS = "五行生克分析"
    YINYANG_DIALECTICS = "阴阳辩证思维"
    SEASONAL_RHYTHM = "时节节律运用"
    COSMIC_HARMONY = "天人合一境界"
    CYCLICAL_TRANSFORMATION = "循环转化规律"
    
    # 复杂性科学 (3)
    EMERGENT_ORDER = "涌现秩序识别"
    NETWORK_DYNAMICS = "网络动力学分析"
    ADAPTIVE_EVOLUTION = "自适应演化预测"
    
    # 精细优化 (4)
    TALENT_PIPELINE = "人才梯队建设"
    ORGANIZATIONAL_CULTURE = "组织文化塑造"
    BRAND_CULTURE = "品牌文化构建"
    PHILOSOPHY_OF_MIND = "心学实践应用"
    DECISION_FRAMEWORK = "决策框架构建"
    RESOURCE_ECOLOGY = "资源生态分析"
    INNOVATION_ECOLOGY = "创新生态分析"
    
    # 社会学 (5)
    SOCIAL_STRUCTURE_ANALYSIS = "社会结构分析"
    CLASS_MOBILITY = "阶层流动性分析"
    INSTITUTIONAL_SOCIOLOGY = "制度社会学分析"
    SOCIAL_STRATIFICATION = "社会分层分析"
    COLLECTIVE_ACTION = "集体行动分析"
    
    # 行为经济学 (5)
    COGNITIVE_BIAS_V62 = "认知偏差识别"
    DECISION_MAKING_BEHAVIOR = "决策行为分析"
    MARKET_BEHAVIOR = "市场行为预测"
    INCENTIVE_DESIGN = "激励设计分析"
    NUDGE_POLICY = "助推政策设计"
    
    # 传播学 (5)
    MEDIA_EFFECT = "媒介效果分析"
    PUBLIC_OPINION_FORMATION = "舆论形成分析"
    INFORMATION_CASCADE = "信息级联效应"
    DISCOURSE_ANALYSIS = "话语分析"
    INTERPERSONAL_COMMUNICATION = "人际传播分析"
    
    # 文化人类学 (4)
    CULTURAL_PATTERN_RECOGNITION = "文化模式识别"
    SYMBOL_SYSTEM_ANALYSIS = "符号系统分析"
    RITUAL_CONTEXT_ANALYSIS = "仪式语境分析"
    CROSS_CULTURAL_ADAPTATION = "跨文化适应分析"
    
    # 政治经济学 (4)
    INSTITUTIONAL_POLITICAL_ANALYSIS = "制度政治分析"
    POLICY_GAME_THEORY = "政策博弈分析"
    MARKET_REGULATION_ANALYSIS = "市场监管分析"
    PUBLIC_CHOICE = "公共选择分析"
    
    # 组织心理学 (4)
    ORGANIZATIONAL_CHANGE_V62 = "组织变革分析"
    LEADERSHIP_STYLE_ANALYSIS = "领导风格分析"
    TEAM_COHESION_ANALYSIS = "团队凝聚力分析"
    ORGANIZATIONAL_CULTURE_V62 = "组织文化诊断"
    
    # 社会心理学 (4)
    CONFORMITY_BEHAVIOR = "从众行为分析"
    AUTHORITY_OBEDIENCE = "权威服从分析"
    SOCIAL_INFLUENCE_MECHANISM = "社会影响机制"
    GROUP_THINK_ANALYSIS = "群体思维分析"

    # 增长与行业 (5) — v2.0.0 新增（Growth+Industry整合）
    GROWTH_STRATEGY = "增长战略制定"
    INDUSTRY_ADAPTATION = "行业适配分析"
    GROWTH_DIAGNOSIS = "增长诊断"
    AARRR_FRAMEWORK = "海盗指标分析"
    INDUSTRY_BENCHMARK = "行业基准对比"


# ============================================================
# 问题类型 → 学派映射矩阵
# ============================================================

PROBLEM_TO_SCHOOLS: Dict[ProblemType, List[Tuple[WisdomSchool, float]]] = {
    # 儒家问题类型
    ProblemType.ETHICAL: [(WisdomSchool.CONFUCIAN, 0.95), (WisdomSchool.BUDDHIST, 0.7), (WisdomSchool.MOZI, 0.6)],
    ProblemType.GOVERNANCE: [(WisdomSchool.CONFUCIAN, 0.9), (WisdomSchool.FAJIA, 0.8), (WisdomSchool.MANAGEMENT, 0.75)],
    ProblemType.TALENT: [(WisdomSchool.CONFUCIAN, 0.85), (WisdomSchool.MILITARY, 0.7), (WisdomSchool.MOZI, 0.65)],
    ProblemType.CULTURE: [(WisdomSchool.CONFUCIAN, 0.95), (WisdomSchool.ANTHROPOLOGY, 0.75), (WisdomSchool.LITERARY, 0.7)],
    ProblemType.CONFUCIAN_SUB_SCHOOL: [(WisdomSchool.CONFUCIAN, 1.0), (WisdomSchool.YANGMING, 0.8)],
    
    # 道家问题类型
    ProblemType.STRATEGY: [(WisdomSchool.DAOIST, 0.9), (WisdomSchool.MILITARY, 0.85), (WisdomSchool.ZONGHENG, 0.7)],
    ProblemType.CRISIS: [(WisdomSchool.DAOIST, 0.9), (WisdomSchool.MILITARY, 0.8), (WisdomSchool.SYSTEMS, 0.7)],
    ProblemType.CHANGE: [(WisdomSchool.DAOIST, 0.85), (WisdomSchool.COMPLEXITY, 0.8), (WisdomSchool.MANAGEMENT, 0.75)],
    ProblemType.BALANCE: [(WisdomSchool.DAOIST, 0.95), (WisdomSchool.WUXING, 0.9), (WisdomSchool.SYSTEMS, 0.7)],
    ProblemType.TIMING: [(WisdomSchool.DAOIST, 0.9), (WisdomSchool.METAPHYSICS, 0.85), (WisdomSchool.MILITARY, 0.7)],
    ProblemType.ENVIRONMENT: [(WisdomSchool.DAOIST, 0.9), (WisdomSchool.SYSTEMS, 0.8), (WisdomSchool.CIVILIZATION, 0.7)],
    ProblemType.PATTERN: [(WisdomSchool.DAOIST, 0.85), (WisdomSchool.WUXING, 0.8), (WisdomSchool.SYSTEMS, 0.75)],
    ProblemType.DAOIST_SUB_SCHOOL: [(WisdomSchool.DAOIST, 1.0)],
    
    # 佛家问题类型
    ProblemType.MINDSET: [(WisdomSchool.BUDDHIST, 0.95), (WisdomSchool.PSYCHOLOGY, 0.8), (WisdomSchool.CONFUCIAN, 0.6)],
    ProblemType.HARMONY: [(WisdomSchool.BUDDHIST, 0.9), (WisdomSchool.CONFUCIAN, 0.8), (WisdomSchool.PSYCHOLOGY, 0.7)],
    ProblemType.INTEREST: [(WisdomSchool.BUDDHIST, 0.85), (WisdomSchool.ECONOMICS, 0.8), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.75)],
    ProblemType.LONGTERM: [(WisdomSchool.BUDDHIST, 0.9), (WisdomSchool.DAOIST, 0.85), (WisdomSchool.CIVILIZATION, 0.7)],
    ProblemType.BUDDHIST_SUB_SCHOOL: [(WisdomSchool.BUDDHIST, 1.0)],
    
    # 素书问题类型
    ProblemType.LEADERSHIP: [(WisdomSchool.SUFU, 0.95), (WisdomSchool.CONFUCIAN, 0.8), (WisdomSchool.MILITARY, 0.75)],
    ProblemType.RISK: [(WisdomSchool.SUFU, 0.9), (WisdomSchool.MILITARY, 0.85), (WisdomSchool.COMPLEXITY, 0.7)],
    ProblemType.FORTUNE: [(WisdomSchool.SUFU, 0.9), (WisdomSchool.METAPHYSICS, 0.85), (WisdomSchool.DAOIST, 0.7)],
    ProblemType.PERSONNEL: [(WisdomSchool.SUFU, 0.9), (WisdomSchool.MILITARY, 0.85), (WisdomSchool.PSYCHOLOGY, 0.7)],
    
    # 兵法问题类型
    ProblemType.COMPETITION: [(WisdomSchool.MILITARY, 0.95), (WisdomSchool.ECONOMICS, 0.8), (WisdomSchool.ZONGHENG, 0.75)],
    ProblemType.ATTACK: [(WisdomSchool.MILITARY, 0.95), (WisdomSchool.COMMUNICATION, 0.8)],
    ProblemType.DEFENSE: [(WisdomSchool.MILITARY, 0.95), (WisdomSchool.DAOIST, 0.8), (WisdomSchool.SYSTEMS, 0.7)],
    ProblemType.NEGOTIATION: [(WisdomSchool.MILITARY, 0.9), (WisdomSchool.ZONGHENG, 0.85), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.7)],
    ProblemType.WAR_ECONOMY_NEXUS: [(WisdomSchool.CIV_WAR_ECONOMY, 0.95), (WisdomSchool.ECONOMICS, 0.8)],
    ProblemType.STATE_CAPACITY: [(WisdomSchool.CIVILIZATION, 0.9), (WisdomSchool.POLITICAL_ECONOMICS, 0.85)],
    ProblemType.INSTITUTIONAL_SEDIMENTATION: [(WisdomSchool.CIVILIZATION, 0.9), (WisdomSchool.FAJIA, 0.8)],
    ProblemType.MILITARY_SUB_SCHOOL: [(WisdomSchool.MILITARY, 1.0)],
    
    # 吕氏春秋问题类型
    ProblemType.PUBLIC_INTEREST: [(WisdomSchool.LVSHI, 0.95), (WisdomSchool.CONFUCIAN, 0.8), (WisdomSchool.MOZI, 0.75)],
    ProblemType.SEASONAL: [(WisdomSchool.LVSHI, 0.95), (WisdomSchool.WUXING, 0.85), (WisdomSchool.WUXING, 0.7)],
    ProblemType.YINYANG: [(WisdomSchool.LVSHI, 0.9), (WisdomSchool.WUXING, 0.95), (WisdomSchool.DAOIST, 0.8)],
    
    # 科幻思维问题类型
    ProblemType.DIMENSION: [(WisdomSchool.SCI_FI, 0.95), (WisdomSchool.COMPLEXITY, 0.8), (WisdomSchool.SYSTEMS, 0.7)],
    ProblemType.SURVIVAL: [(WisdomSchool.SCI_FI, 0.9), (WisdomSchool.MILITARY, 0.75), (WisdomSchool.MILITARY, 0.7)],
    ProblemType.SCALE: [(WisdomSchool.SCI_FI, 0.9), (WisdomSchool.SYSTEMS, 0.85), (WisdomSchool.COMPLEXITY, 0.8)],
    
    # 成长思维问题类型
    ProblemType.GROWTH_MINDSET: [(WisdomSchool.GROWTH, 0.95), (WisdomSchool.PSYCHOLOGY, 0.8), (WisdomSchool.PSYCHOLOGY, 0.7)],
    ProblemType.REVERSE: [(WisdomSchool.GROWTH, 0.9), (WisdomSchool.DAOIST, 0.8), (WisdomSchool.MANAGEMENT, 0.75)],
    ProblemType.CLOSED_LOOP: [(WisdomSchool.GROWTH, 0.9), (WisdomSchool.SYSTEMS, 0.85), (WisdomSchool.MANAGEMENT, 0.75)],
    
    # 神话智慧问题类型
    ProblemType.CREATION_MYTH: [(WisdomSchool.MYTHOLOGY, 0.95), (WisdomSchool.CIVILIZATION, 0.8), (WisdomSchool.LITERARY, 0.7)],
    ProblemType.APOCALYPSE: [(WisdomSchool.MYTHOLOGY, 0.9), (WisdomSchool.MILITARY, 0.85), (WisdomSchool.CIVILIZATION, 0.75)],
    ProblemType.CYCLICAL: [(WisdomSchool.MYTHOLOGY, 0.9), (WisdomSchool.DAOIST, 0.85), (WisdomSchool.HISTORICAL_THOUGHT, 0.75)],
    
    # 文学叙事问题类型
    ProblemType.NARRATIVE: [(WisdomSchool.LITERARY, 0.95), (WisdomSchool.CHINESE_CONSUMER, 0.8), (WisdomSchool.COMMUNICATION, 0.7)],
    ProblemType.RESILIENCE: [(WisdomSchool.LITERARY, 0.9), (WisdomSchool.PSYCHOLOGY, 0.85), (WisdomSchool.HISTORICAL_THOUGHT, 0.7)],
    ProblemType.CHARACTER: [(WisdomSchool.LITERARY, 0.95), (WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.ANTHROPOLOGY, 0.7)],
    
    # 人类学问题类型
    ProblemType.CROSS_CULTURE: [(WisdomSchool.ANTHROPOLOGY, 0.95), (WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.9), (WisdomSchool.COMMUNICATION, 0.75)],
    ProblemType.RITUAL: [(WisdomSchool.ANTHROPOLOGY, 0.95), (WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.9), (WisdomSchool.SOCIOLOGY, 0.7)],
    ProblemType.CULTURAL_CHANGE: [(WisdomSchool.ANTHROPOLOGY, 0.9), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.7)],
    
    # 行为塑造问题类型
    ProblemType.HABIT: [(WisdomSchool.BEHAVIOR, 0.95), (WisdomSchool.PSYCHOLOGY, 0.85), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.8)],
    ProblemType.WILLPOWER: [(WisdomSchool.BEHAVIOR, 0.9), (WisdomSchool.PSYCHOLOGY, 0.85), (WisdomSchool.BUDDHIST, 0.7)],
    ProblemType.NUDGE: [(WisdomSchool.BEHAVIOR, 0.95), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.9), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.85)],
    
    # 科学思维问题类型
    ProblemType.SCIENTIFIC_METHOD: [(WisdomSchool.SCIENCE, 0.95), (WisdomSchool.NATURAL_SCIENCE, 0.85), (WisdomSchool.SYSTEMS, 0.7)],
    ProblemType.SYSTEM_THINKING: [(WisdomSchool.SCIENCE, 0.9), (WisdomSchool.SYSTEMS, 0.95), (WisdomSchool.COMPLEXITY, 0.85)],
    ProblemType.EVIDENCE: [(WisdomSchool.SCIENCE, 0.95), (WisdomSchool.SCIENCE, 0.85), (WisdomSchool.SCIENCE, 0.8)],
    
    # 社会科学问题类型
    ProblemType.MARKETING: [(WisdomSchool.SOCIAL_SCIENCE, 0.9), (WisdomSchool.CHINESE_CONSUMER, 0.85), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.8)],
    ProblemType.MARKET_ANALYSIS: [(WisdomSchool.SOCIAL_SCIENCE, 0.9), (WisdomSchool.ECONOMICS, 0.85), (WisdomSchool.SOCIAL_SCIENCE, 0.8)],
    ProblemType.SOCIAL_DEVELOPMENT: [(WisdomSchool.SOCIAL_SCIENCE, 0.9), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.POLITICAL_ECONOMICS, 0.75)],
    ProblemType.PSYCHOLOGICAL_INSIGHT: [(WisdomSchool.SOCIAL_SCIENCE, 0.85), (WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.CHINESE_CONSUMER, 0.8)],
    
    # 营销战略问题类型
    ProblemType.CONSUMER_MARKETING: [(WisdomSchool.CHINESE_CONSUMER, 0.95), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.85), (WisdomSchool.CHINESE_CONSUMER, 0.9)],
    ProblemType.BRAND_STRATEGY: [(WisdomSchool.CHINESE_CONSUMER, 0.9), (WisdomSchool.LITERARY, 0.85), (WisdomSchool.ANTHROPOLOGY, 0.75)],
    ProblemType.SOCIAL_STABILITY: [(WisdomSchool.SOCIOLOGY, 0.9), (WisdomSchool.POLITICAL_ECONOMICS, 0.85), (WisdomSchool.CIVILIZATION, 0.75)],
    
    # 心理学问题类型
    ProblemType.PERSONALITY_ANALYSIS: [(WisdomSchool.PSYCHOLOGY, 0.95), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.8)],
    ProblemType.GROUP_DYNAMICS: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.9), (WisdomSchool.SOCIOLOGY, 0.75)],
    ProblemType.COGNITIVE_BIAS: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.95), (WisdomSchool.SCIENCE, 0.7)],
    ProblemType.MOTIVATION_ANALYSIS: [(WisdomSchool.PSYCHOLOGY, 0.95), (WisdomSchool.ECONOMICS, 0.8), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.85)],
    ProblemType.PSYCHOLOGICAL_ARITHMETIC: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.85)],
    ProblemType.TRAUMA_HEALING: [(WisdomSchool.PSYCHOLOGY, 0.95), (WisdomSchool.BUDDHIST, 0.8), (WisdomSchool.BUDDHIST, 0.7)],
    ProblemType.SELF_ACTUALIZATION: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.YANGMING, 0.9), (WisdomSchool.CONFUCIAN, 0.75)],
    ProblemType.INTERPERSONAL_RELATIONSHIP: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.CONFUCIAN, 0.85), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.8)],
    
    # 系统论问题类型
    ProblemType.COMPLEX_SYSTEM: [(WisdomSchool.SYSTEMS, 0.95), (WisdomSchool.COMPLEXITY, 0.9), (WisdomSchool.SCIENCE, 0.75)],
    ProblemType.FEEDBACK_LOOP: [(WisdomSchool.SYSTEMS, 0.95), (WisdomSchool.SCIENCE, 0.85), (WisdomSchool.COMPLEXITY, 0.8)],
    ProblemType.EMERGENT_BEHAVIOR: [(WisdomSchool.SYSTEMS, 0.9), (WisdomSchool.COMPLEXITY, 0.95), (WisdomSchool.CIVILIZATION, 0.75)],
    ProblemType.SYSTEM_EQUILIBRIUM: [(WisdomSchool.SYSTEMS, 0.9), (WisdomSchool.ECONOMICS, 0.85), (WisdomSchool.WUXING, 0.8)],
    ProblemType.ADAPTIVE_SYSTEM: [(WisdomSchool.SYSTEMS, 0.9), (WisdomSchool.COMPLEXITY, 0.9), (WisdomSchool.CIVILIZATION, 0.8)],
    
    # 管理学问题类型
    ProblemType.STRATEGIC_PLANNING: [(WisdomSchool.MANAGEMENT, 0.95), (WisdomSchool.CONFUCIAN, 0.8), (WisdomSchool.MILITARY, 0.75)],
    ProblemType.ORGANIZATIONAL_DESIGN: [(WisdomSchool.MANAGEMENT, 0.95), (WisdomSchool.SYSTEMS, 0.85), (WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.8)],
    ProblemType.PERFORMANCE_MANAGEMENT: [(WisdomSchool.MANAGEMENT, 0.95), (WisdomSchool.ECONOMICS, 0.8), (WisdomSchool.FAJIA, 0.75)],
    ProblemType.KNOWLEDGE_MANAGEMENT: [(WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.WCC, 0.85), (WisdomSchool.SYSTEMS, 0.75)],
    ProblemType.CHANGE_MANAGEMENT: [(WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.MANAGEMENT, 0.85), (WisdomSchool.PSYCHOLOGY, 0.8)],
    ProblemType.INNOVATION_MANAGEMENT: [(WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.MANAGEMENT, 0.85), (WisdomSchool.SCIENCE, 0.8)],
    
    # 纵横家问题类型
    ProblemType.DIPLOMATIC_NEGOTIATION: [(WisdomSchool.ZONGHENG, 0.95), (WisdomSchool.MILITARY, 0.85), (WisdomSchool.COMMUNICATION, 0.75)],
    ProblemType.ALLIANCE_BUILDING: [(WisdomSchool.ZONGHENG, 0.95), (WisdomSchool.MILITARY, 0.8), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.75)],
    ProblemType.POWER_BALANCE: [(WisdomSchool.ZONGHENG, 0.95), (WisdomSchool.POLITICAL_ECONOMICS, 0.9), (WisdomSchool.MILITARY, 0.8)],
    
    # 墨家问题类型
    ProblemType.ENGINEERING_INNOVATION: [(WisdomSchool.MOZI, 0.95), (WisdomSchool.SCIENCE, 0.85), (WisdomSchool.MANAGEMENT, 0.75)],
    ProblemType.COST_OPTIMIZATION: [(WisdomSchool.MOZI, 0.9), (WisdomSchool.ECONOMICS, 0.9), (WisdomSchool.MANAGEMENT, 0.85)],
    ProblemType.UNIVERSAL_BENEFIT: [(WisdomSchool.MOZI, 0.95), (WisdomSchool.CONFUCIAN, 0.8), (WisdomSchool.MOZI, 0.75)],
    ProblemType.DEFENSE_FORTIFICATION: [(WisdomSchool.MOZI, 0.9), (WisdomSchool.MILITARY, 0.9)],
    ProblemType.LOGICAL_DEDUCTION: [(WisdomSchool.MOZI, 0.95), (WisdomSchool.MINGJIA, 0.9), (WisdomSchool.SCIENCE, 0.8)],
    
    # 法家问题类型
    ProblemType.INSTITUTIONAL_DESIGN: [(WisdomSchool.FAJIA, 0.95), (WisdomSchool.MANAGEMENT, 0.85), (WisdomSchool.POLITICAL_ECONOMICS, 0.8)],
    ProblemType.LAW_ENFORCEMENT: [(WisdomSchool.FAJIA, 0.95), (WisdomSchool.MANAGEMENT, 0.8)],
    ProblemType.POWER_STRUCTURING: [(WisdomSchool.FAJIA, 0.95), (WisdomSchool.POLITICAL_ECONOMICS, 0.9), (WisdomSchool.ZONGHENG, 0.8)],
    ProblemType.REWARD_PUNISHMENT: [(WisdomSchool.FAJIA, 0.95), (WisdomSchool.ECONOMICS, 0.85), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.8)],
    ProblemType.HUMAN_NATURE_ANALYSIS: [(WisdomSchool.FAJIA, 0.9), (WisdomSchool.PSYCHOLOGY, 0.85), (WisdomSchool.CONFUCIAN, 0.75)],
    ProblemType.STATE_CONSOLIDATION: [(WisdomSchool.FAJIA, 0.95), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.POLITICAL_ECONOMICS, 0.8)],
    
    # 经济学问题类型
    ProblemType.RESOURCE_ALLOCATION: [(WisdomSchool.ECONOMICS, 0.95), (WisdomSchool.MANAGEMENT, 0.85), (WisdomSchool.SYSTEMS, 0.75)],
    ProblemType.SUPPLY_DEMAND_BALANCE: [(WisdomSchool.ECONOMICS, 0.95), (WisdomSchool.SYSTEMS, 0.85), (WisdomSchool.ECONOMICS, 0.8)],
    ProblemType.ECONOMIC_INCENTIVE: [(WisdomSchool.ECONOMICS, 0.9), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.95), (WisdomSchool.MANAGEMENT, 0.75)],
    ProblemType.MARKET_EFFICIENCY: [(WisdomSchool.ECONOMICS, 0.95), (WisdomSchool.POLITICAL_ECONOMICS, 0.85), (WisdomSchool.SYSTEMS, 0.75)],
    ProblemType.INVESTMENT_DECISION: [(WisdomSchool.ECONOMICS, 0.9), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.85), (WisdomSchool.SUFU, 0.8)],
    
    # 名家问题类型
    ProblemType.LOGICAL_PARADOX: [(WisdomSchool.MINGJIA, 0.95), (WisdomSchool.MOZI, 0.85), (WisdomSchool.SCIENCE, 0.8)],
    ProblemType.CLASSIFICATION_REFINEMENT: [(WisdomSchool.MINGJIA, 0.95), (WisdomSchool.SYSTEMS, 0.8), (WisdomSchool.SCIENCE, 0.75)],
    ProblemType.DIALECTICAL_REASONING: [(WisdomSchool.MINGJIA, 0.9), (WisdomSchool.DAOIST, 0.85), (WisdomSchool.WUXING, 0.8)],
    
    # 阴阳家问题类型
    ProblemType.WUXING_ANALYSIS: [(WisdomSchool.WUXING, 0.95), (WisdomSchool.WUXING, 0.9), (WisdomSchool.DAOIST, 0.8)],
    ProblemType.YINYANG_DIALECTICS: [(WisdomSchool.WUXING, 0.95), (WisdomSchool.DAOIST, 0.9), (WisdomSchool.DAOIST, 0.85)],
    ProblemType.SEASONAL_RHYTHM: [(WisdomSchool.WUXING, 0.9), (WisdomSchool.LVSHI, 0.85), (WisdomSchool.WUXING, 0.8)],
    ProblemType.COSMIC_HARMONY: [(WisdomSchool.WUXING, 0.9), (WisdomSchool.DAOIST, 0.85), (WisdomSchool.CIVILIZATION, 0.8)],
    ProblemType.CYCLICAL_TRANSFORMATION: [(WisdomSchool.WUXING, 0.9), (WisdomSchool.DAOIST, 0.9), (WisdomSchool.MYTHOLOGY, 0.85)],
    
    # 复杂性科学问题类型
    ProblemType.EMERGENT_ORDER: [(WisdomSchool.COMPLEXITY, 0.95), (WisdomSchool.SYSTEMS, 0.9), (WisdomSchool.CIVILIZATION, 0.75)],
    ProblemType.NETWORK_DYNAMICS: [(WisdomSchool.COMPLEXITY, 0.95), (WisdomSchool.SYSTEMS, 0.9), (WisdomSchool.COMPLEXITY, 0.8)],
    ProblemType.ADAPTIVE_EVOLUTION: [(WisdomSchool.COMPLEXITY, 0.95), (WisdomSchool.CIVILIZATION, 0.9), (WisdomSchool.SYSTEMS, 0.85)],
    
    # 社会学问题类型
    ProblemType.SOCIAL_STRUCTURE_ANALYSIS: [(WisdomSchool.SOCIOLOGY, 0.95), (WisdomSchool.POLITICAL_ECONOMICS, 0.85), (WisdomSchool.CIVILIZATION, 0.8)],
    ProblemType.CLASS_MOBILITY: [(WisdomSchool.SOCIOLOGY, 0.95), (WisdomSchool.ECONOMICS, 0.85), (WisdomSchool.POLITICAL_ECONOMICS, 0.8)],
    ProblemType.INSTITUTIONAL_SOCIOLOGY: [(WisdomSchool.SOCIOLOGY, 0.9), (WisdomSchool.FAJIA, 0.85), (WisdomSchool.FAJIA, 0.75)],
    ProblemType.SOCIAL_STRATIFICATION: [(WisdomSchool.SOCIOLOGY, 0.95), (WisdomSchool.POLITICAL_ECONOMICS, 0.9), (WisdomSchool.ECONOMICS, 0.8)],
    ProblemType.COLLECTIVE_ACTION: [(WisdomSchool.SOCIOLOGY, 0.9), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.85), (WisdomSchool.POLITICAL_ECONOMICS, 0.8)],
    
    # 行为经济学问题类型
    ProblemType.COGNITIVE_BIAS_V62: [(WisdomSchool.BEHAVIORAL_ECONOMICS, 0.95), (WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.PSYCHOLOGY, 0.85)],
    ProblemType.DECISION_MAKING_BEHAVIOR: [(WisdomSchool.BEHAVIORAL_ECONOMICS, 0.95), (WisdomSchool.PSYCHOLOGY, 0.85), (WisdomSchool.ECONOMICS, 0.8)],
    ProblemType.MARKET_BEHAVIOR: [(WisdomSchool.BEHAVIORAL_ECONOMICS, 0.9), (WisdomSchool.ECONOMICS, 0.9), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.75)],
    ProblemType.INCENTIVE_DESIGN: [(WisdomSchool.BEHAVIORAL_ECONOMICS, 0.9), (WisdomSchool.ECONOMICS, 0.85), (WisdomSchool.MANAGEMENT, 0.8)],
    ProblemType.NUDGE_POLICY: [(WisdomSchool.BEHAVIORAL_ECONOMICS, 0.95), (WisdomSchool.BEHAVIOR, 0.9), (WisdomSchool.POLITICAL_ECONOMICS, 0.8)],
    
    # 传播学问题类型
    ProblemType.MEDIA_EFFECT: [(WisdomSchool.COMMUNICATION, 0.95), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.85), (WisdomSchool.COMMUNICATION, 0.75)],
    ProblemType.PUBLIC_OPINION_FORMATION: [(WisdomSchool.COMMUNICATION, 0.95), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.9), (WisdomSchool.SOCIOLOGY, 0.8)],
    ProblemType.INFORMATION_CASCADE: [(WisdomSchool.COMMUNICATION, 0.9), (WisdomSchool.COMPLEXITY, 0.85), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.8)],
    ProblemType.DISCOURSE_ANALYSIS: [(WisdomSchool.COMMUNICATION, 0.95), (WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.85), (WisdomSchool.LITERARY, 0.8)],
    ProblemType.INTERPERSONAL_COMMUNICATION: [(WisdomSchool.COMMUNICATION, 0.95), (WisdomSchool.PSYCHOLOGY, 0.85), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.8)],
    
    # 文化人类学问题类型
    ProblemType.CULTURAL_PATTERN_RECOGNITION: [(WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.95), (WisdomSchool.ANTHROPOLOGY, 0.9), (WisdomSchool.CIVILIZATION, 0.8)],
    ProblemType.SYMBOL_SYSTEM_ANALYSIS: [(WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.95), (WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.85), (WisdomSchool.LITERARY, 0.75)],
    ProblemType.RITUAL_CONTEXT_ANALYSIS: [(WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.95), (WisdomSchool.ANTHROPOLOGY, 0.9), (WisdomSchool.SOCIOLOGY, 0.75)],
    ProblemType.CROSS_CULTURAL_ADAPTATION: [(WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.95), (WisdomSchool.ANTHROPOLOGY, 0.9), (WisdomSchool.ANTHROPOLOGY, 0.85)],
    
    # 政治经济学问题类型
    ProblemType.INSTITUTIONAL_POLITICAL_ANALYSIS: [(WisdomSchool.POLITICAL_ECONOMICS, 0.95), (WisdomSchool.SOCIOLOGY, 0.85), (WisdomSchool.FAJIA, 0.8)],
    ProblemType.POLICY_GAME_THEORY: [(WisdomSchool.POLITICAL_ECONOMICS, 0.9), (WisdomSchool.ZONGHENG, 0.85), (WisdomSchool.ZONGHENG, 0.9)],
    ProblemType.MARKET_REGULATION_ANALYSIS: [(WisdomSchool.POLITICAL_ECONOMICS, 0.9), (WisdomSchool.ECONOMICS, 0.9), (WisdomSchool.FAJIA, 0.8)],
    ProblemType.PUBLIC_CHOICE: [(WisdomSchool.POLITICAL_ECONOMICS, 0.95), (WisdomSchool.ECONOMICS, 0.85), (WisdomSchool.SOCIOLOGY, 0.8)],
    
    # 组织心理学问题类型
    ProblemType.ORGANIZATIONAL_CHANGE_V62: [(WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.95), (WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.PSYCHOLOGY, 0.85)],
    ProblemType.LEADERSHIP_STYLE_ANALYSIS: [(WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.9), (WisdomSchool.SUFU, 0.9), (WisdomSchool.PSYCHOLOGY, 0.85)],
    ProblemType.TEAM_COHESION_ANALYSIS: [(WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.9), (WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.85)],
    ProblemType.ORGANIZATIONAL_CULTURE_V62: [(WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.9), (WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.9), (WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.8)],
    
    # 社会心理学问题类型
    ProblemType.CONFORMITY_BEHAVIOR: [(WisdomSchool.SOCIAL_PSYCHOLOGY, 0.95), (WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.BEHAVIOR, 0.8)],
    ProblemType.AUTHORITY_OBEDIENCE: [(WisdomSchool.SOCIAL_PSYCHOLOGY, 0.95), (WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.SOCIOLOGY, 0.75)],
    ProblemType.SOCIAL_INFLUENCE_MECHANISM: [(WisdomSchool.SOCIAL_PSYCHOLOGY, 0.95), (WisdomSchool.COMMUNICATION, 0.9), (WisdomSchool.POLITICAL_ECONOMICS, 0.75)],
    ProblemType.GROUP_THINK_ANALYSIS: [(WisdomSchool.SOCIAL_PSYCHOLOGY, 0.95), (WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.85)],

    # 增长与行业 (5) — v2.0.0 新增（Growth+Industry整合）
    ProblemType.GROWTH_STRATEGY: [(WisdomSchool.GROWTH_STRATEGY, 0.95), (WisdomSchool.ECONOMICS, 0.85), (WisdomSchool.MANAGEMENT, 0.8)],
    ProblemType.INDUSTRY_ADAPTATION: [(WisdomSchool.INDUSTRY_WISDOM, 0.95), (WisdomSchool.ECONOMICS, 0.85), (WisdomSchool.SOCIAL_SCIENCE, 0.8)],
    ProblemType.GROWTH_DIAGNOSIS: [(WisdomSchool.GROWTH_STRATEGY, 0.9), (WisdomSchool.SYSTEMS, 0.85), (WisdomSchool.ECONOMICS, 0.8)],
    ProblemType.AARRR_FRAMEWORK: [(WisdomSchool.GROWTH_STRATEGY, 0.95), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.9), (WisdomSchool.MARKETING, 0.85)],
    ProblemType.INDUSTRY_BENCHMARK: [(WisdomSchool.INDUSTRY_WISDOM, 0.95), (WisdomSchool.ECONOMICS, 0.9), (WisdomSchool.MANAGEMENT, 0.85)],
    
    # 通用问题类型
    ProblemType.TALENT_PIPELINE: [(WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.PSYCHOLOGY, 0.85), (WisdomSchool.CONFUCIAN, 0.75)],
    ProblemType.ORGANIZATIONAL_CULTURE: [(WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.9), (WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.85), (WisdomSchool.MANAGEMENT, 0.8)],
    ProblemType.BRAND_CULTURE: [(WisdomSchool.LITERARY, 0.9), (WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.85), (WisdomSchool.COMMUNICATION, 0.8)],
    ProblemType.PHILOSOPHY_OF_MIND: [(WisdomSchool.YANGMING, 0.95), (WisdomSchool.CONFUCIAN, 0.85), (WisdomSchool.PSYCHOLOGY, 0.8)],
    ProblemType.DECISION_FRAMEWORK: [(WisdomSchool.SYSTEMS, 0.9), (WisdomSchool.PSYCHOLOGY, 0.85), (WisdomSchool.MILITARY, 0.8)],
    ProblemType.RESOURCE_ECOLOGY: [(WisdomSchool.ECONOMICS, 0.9), (WisdomSchool.SYSTEMS, 0.85), (WisdomSchool.DAOIST, 0.8)],
    ProblemType.INNOVATION_ECOLOGY: [(WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.COMPLEXITY, 0.85)],
    
    # WCC智慧演化缺失映射
    ProblemType.META_PERSPECTIVE: [(WisdomSchool.WCC, 0.95), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.SYSTEMS, 0.75)],
    ProblemType.CIVILIZATION_ANALYSIS: [(WisdomSchool.CIVILIZATION, 0.95), (WisdomSchool.HISTORICAL_THOUGHT, 0.9), (WisdomSchool.SOCIOLOGY, 0.75)],
    ProblemType.COSMIC_COGNITION: [(WisdomSchool.WCC, 0.95), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.METAPHYSICS, 0.7)],
    ProblemType.SCALE_TRANSFORMATION: [(WisdomSchool.WCC, 0.9), (WisdomSchool.COMPLEXITY, 0.85), (WisdomSchool.SYSTEMS, 0.8)],
    ProblemType.WORLDVIEW_SHIFT: [(WisdomSchool.WCC, 0.9), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.HISTORICAL_THOUGHT, 0.75)],
    ProblemType.WISDOM_EVOLUTION: [(WisdomSchool.WCC, 0.95), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.HISTORICAL_THOUGHT, 0.75)],
    ProblemType.TECH_EVOLUTION: [(WisdomSchool.WCC, 0.9), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.COMPLEXITY, 0.75)],
    
    # 历史思想三维度缺失映射
    ProblemType.HISTORICAL_ANALYSIS: [(WisdomSchool.HISTORICAL_THOUGHT, 0.95), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.SYSTEMS, 0.7)],
    ProblemType.THOUGHT_EVOLUTION: [(WisdomSchool.HISTORICAL_THOUGHT, 0.9), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.WCC, 0.75)],
    ProblemType.ECONOMIC_EVOLUTION: [(WisdomSchool.HISTORICAL_THOUGHT, 0.9), (WisdomSchool.ECONOMICS, 0.85), (WisdomSchool.CIVILIZATION, 0.75)],
    ProblemType.TECH_HISTORY: [(WisdomSchool.HISTORICAL_THOUGHT, 0.9), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.WCC, 0.75)],
    ProblemType.CROSS_DIMENSION: [(WisdomSchool.HISTORICAL_THOUGHT, 0.85), (WisdomSchool.SYSTEMS, 0.85), (WisdomSchool.COMPLEXITY, 0.8)],
    ProblemType.PARADIGM_SHIFT: [(WisdomSchool.HISTORICAL_THOUGHT, 0.9), (WisdomSchool.CIVILIZATION, 0.85), (WisdomSchool.WCC, 0.8)],
    
    # 自然科学缺失映射
    ProblemType.PHYSICS_ANALYSIS: [(WisdomSchool.NATURAL_SCIENCE, 0.95), (WisdomSchool.SCIENCE, 0.85), (WisdomSchool.SYSTEMS, 0.7)],
    ProblemType.LIFE_SCIENCE: [(WisdomSchool.NATURAL_SCIENCE, 0.95), (WisdomSchool.SCIENCE, 0.85), (WisdomSchool.SYSTEMS, 0.75)],
    ProblemType.EARTH_SYSTEM: [(WisdomSchool.NATURAL_SCIENCE, 0.9), (WisdomSchool.SYSTEMS, 0.85), (WisdomSchool.COMPLEXITY, 0.75)],
    ProblemType.COSMOS_EXPLORATION: [(WisdomSchool.NATURAL_SCIENCE, 0.9), (WisdomSchool.CIVILIZATION, 0.8), (WisdomSchool.SCI_FI, 0.75)],
    ProblemType.SCALE_CROSSING: [(WisdomSchool.NATURAL_SCIENCE, 0.85), (WisdomSchool.COMPLEXITY, 0.85), (WisdomSchool.SYSTEMS, 0.8)],
}


# ============================================================
# 问题类型识别关键词
# ============================================================

PROBLEM_KEYWORDS: Dict[ProblemType, List[str]] = {
    ProblemType.ETHICAL: ["道德", "伦理", "善恶", "仁义", "品德"],
    ProblemType.GOVERNANCE: ["治理", "管理", "制度", "规范", "秩序"],
    ProblemType.TALENT: ["人才", "选用", "招聘", "团队", "人力"],
    ProblemType.CULTURE: ["文化", "传承", "传统", "风俗", "价值观"],
    ProblemType.CONFUCIAN_SUB_SCHOOL: ["理学", "心学", "经学", "儒学"],
    
    ProblemType.STRATEGY: ["战略", "策略", "规划", "布局", "长期"],
    ProblemType.CRISIS: ["危机", "紧急", "风险", "问题", "困境"],
    ProblemType.CHANGE: ["变革", "转型", "变化", "改变", "改革"],
    ProblemType.BALANCE: ["平衡", "协调", "调和", "中庸", "和谐"],
    ProblemType.TIMING: ["时机", "时机把握", "时间节点", "窗口期"],
    ProblemType.ENVIRONMENT: ["环境", "生态", "氛围", "外部", "内部"],
    ProblemType.PATTERN: ["格局", "结构", "模式", "规律", "趋势"],
    
    ProblemType.MINDSET: ["心态", "心性", "心境", "态度", "心理"],
    ProblemType.HARMONY: ["和谐", "和睦", "融洽", "团结", "和平"],
    ProblemType.INTEREST: ["利益", "好处", "收益", "利润", "分配"],
    ProblemType.LONGTERM: ["长期", "长远", "未来", "持续", "永续"],
    
    ProblemType.LEADERSHIP: ["领导", "领袖", "指引", "带领", "统帅"],
    ProblemType.RISK: ["风险", "危险", "隐患", "不确定性", "损失"],
    ProblemType.FORTUNE: ["福祸", "吉凶", "运气", "命运", "好坏"],
    ProblemType.PERSONNEL: ["人事", "人员", "用人", "识人", "人才", "流失"],
    
    ProblemType.COMPETITION: ["竞争", "博弈", "对抗", "竞赛", "比拼"],
    ProblemType.ATTACK: ["攻击", "进攻", "打击", "抢占", "争夺"],
    ProblemType.DEFENSE: ["防御", "防守", "保护", "保守", "守住"],
    ProblemType.NEGOTIATION: ["谈判", "协商", "洽谈", "议价", "交涉"],
    
    ProblemType.PUBLIC_INTEREST: ["公私", "公益", "公共", "集体", "个人"],
    ProblemType.SEASONAL: ["时令", "季节", "时节", "周期", "节点"],
    ProblemType.YINYANG: ["阴阳", "两面", "正反", "好坏", "对立"],
    
    ProblemType.DIMENSION: ["维度", "层次", "层面", "角度", "视角"],
    ProblemType.SURVIVAL: ["生存", "存活", "存亡", "生死", "活下来"],
    ProblemType.SCALE: ["尺度", "规模", "体量", "大小", "范围"],
    
    ProblemType.GROWTH_MINDSET: ["成长", "突破", "进步", "发展", "提升"],
    ProblemType.REVERSE: ["逆向", "反向", "倒推", "反思", "颠覆"],
    ProblemType.CLOSED_LOOP: ["闭环", "循环", "迭代", "反馈", "回路"],
    
    ProblemType.NARRATIVE: ["叙事", "故事", "叙述", "讲述", "表达"],
    ProblemType.RESILIENCE: ["韧性", "弹性", "抗压", "恢复", "适应"],
    ProblemType.CHARACTER: ["人物", "角色", "性格", "特质", "个性"],
    
    ProblemType.CROSS_CULTURE: ["跨文化", "异域", "国际化", "本土化", "文化差异"],
    ProblemType.RITUAL: ["仪式", "典礼", "礼节", "习俗", "惯例"],
    ProblemType.CULTURAL_CHANGE: ["文化变迁", "演变", "演进", "转型", "变迁"],
    
    ProblemType.HABIT: ["习惯", "行为", "惯性", "常规", "养成"],
    ProblemType.WILLPOWER: ["意志", "自制", "自律", "坚持", "毅力"],
    ProblemType.NUDGE: ["助推", "引导", "激励", "鼓励", "推动"],
    
    ProblemType.SCIENTIFIC_METHOD: ["科学", "实验", "验证", "假设", "方法论"],
    ProblemType.SYSTEM_THINKING: ["系统", "全局", "整体", "关联", "动态"],
    ProblemType.EVIDENCE: ["证据", "事实", "数据", "依据", "证明"],
    
    ProblemType.MARKETING: ["营销", "推广", "销售", "运营", "获客"],
    ProblemType.MARKET_ANALYSIS: ["市场分析", "行情", "趋势", "竞品", "调研"],
    ProblemType.SOCIAL_DEVELOPMENT: ["社会发展", "文明", "进步", "演化", "进程"],
    ProblemType.PSYCHOLOGICAL_INSIGHT: ["心理洞察", "用户心理", "消费心理", "动机", "需求"],
    
    ProblemType.CONSUMER_MARKETING: ["消费者", "C端", "用户", "客户", "买家"],
    ProblemType.BRAND_STRATEGY: ["品牌", "定位", "形象", "知名度", "口碑"],
    ProblemType.SOCIAL_STABILITY: ["社会稳定", "安定", "和谐", "秩序", "稳定"],
    
    ProblemType.PERSONALITY_ANALYSIS: ["人格", "性格", "个性", "特质", "心理"],
    ProblemType.GROUP_DYNAMICS: ["群体", "团队", "人际", "互动", "动态"],
    ProblemType.COGNITIVE_BIAS: ["认知偏差", "偏见", "误区", "思维陷阱", "启发式"],
    ProblemType.MOTIVATION_ANALYSIS: ["动机", "激励", "驱动力", "诱因", "原因"],
    ProblemType.SELF_ACTUALIZATION: ["自我实现", "成长", "成就", "价值", "意义"],
    
    ProblemType.COMPLEX_SYSTEM: ["复杂系统", "混沌", "涌现", "自组织", "非线性"],
    ProblemType.FEEDBACK_LOOP: ["反馈", "回路", "循环", "因果", "互动"],
    ProblemType.EMERGENT_BEHAVIOR: ["涌现", "突现", "集体行为", "自发", "自组织"],
    ProblemType.SYSTEM_EQUILIBRIUM: ["均衡", "平衡", "稳定态", "稳态", "调和"],
    ProblemType.ADAPTIVE_SYSTEM: ["自适应", "适应", "进化", "演化", "学习"],
    
    ProblemType.STRATEGIC_PLANNING: ["战略规划", "计划", "方案", "路线图", "蓝图"],
    ProblemType.ORGANIZATIONAL_DESIGN: ["组织设计", "架构", "结构", "体系", "制度"],
    ProblemType.PERFORMANCE_MANAGEMENT: ["绩效", "考核", "评估", "KPI", "评价"],
    ProblemType.KNOWLEDGE_MANAGEMENT: ["知识管理", "学习", "经验", "沉淀", "传承"],
    ProblemType.CHANGE_MANAGEMENT: ["变革管理", "转型管理", "变革", "推进", "落地"],
    ProblemType.INNOVATION_MANAGEMENT: ["创新管理", "创意", "发明", "突破", "革新"],
    
    ProblemType.DIPLOMATIC_NEGOTIATION: ["外交", "谈判", "协商", "斡旋", "折冲"],
    ProblemType.ALLIANCE_BUILDING: ["联盟", "合作", "结盟", "联合", "抱团"],
    ProblemType.POWER_BALANCE: ["权力平衡", "势力均衡", "制衡", "博弈", "格局"],
    
    ProblemType.ENGINEERING_INNOVATION: ["工程", "技术", "发明", "创新", "创造"],
    ProblemType.COST_OPTIMIZATION: ["成本", "效率", "优化", "节流", "降本"],
    ProblemType.UNIVERSAL_BENEFIT: ["普惠", "共赢", "互利", "惠及", "普遍"],
    ProblemType.LOGICAL_DEDUCTION: ["逻辑", "推理", "论证", "演绎", "推论"],
    
    ProblemType.INSTITUTIONAL_DESIGN: ["制度设计", "机制", "体系", "规则", "体制"],
    ProblemType.LAW_ENFORCEMENT: ["执法", "执行", "落实", "贯彻", "推行"],
    ProblemType.POWER_STRUCTURING: ["权力结构", "权势", "架构", "配置", "分配"],
    ProblemType.REWARD_PUNISHMENT: ["赏罚", "激励", "奖惩", "考核", "奖惩制度"],
    ProblemType.HUMAN_NATURE_ANALYSIS: ["人性", "善恶", "自私", "本能", "欲望"],
    
    ProblemType.RESOURCE_ALLOCATION: ["资源配置", "分配", "调度", "安排", "整合"],
    ProblemType.SUPPLY_DEMAND_BALANCE: ["供需", "平衡", "匹配", "调节", "调节"],
    ProblemType.ECONOMIC_INCENTIVE: ["激励机制", "激励", "刺激", "驱动", "鼓励"],
    ProblemType.MARKET_EFFICIENCY: ["市场效率", "效益", "性价比", "价值", "产出"],
    ProblemType.INVESTMENT_DECISION: ["投资", "决策", "选择", "判断", "判断"],
    
    ProblemType.LOGICAL_PARADOX: ["悖论", "矛盾", "佯谬", "吊诡", "二律背反"],
    ProblemType.CLASSIFICATION_REFINEMENT: ["名实", "概念", "分类", "定义", "辨析"],
    ProblemType.DIALECTICAL_REASONING: ["辩证", "思辨", "诡辩", "论证", "推理"],
    
    ProblemType.WUXING_ANALYSIS: ["五行", "生克", "相生", "相克", "属性"],
    ProblemType.YINYANG_DIALECTICS: ["阴阳", "辩证", "转化", "消长", "互根"],
    ProblemType.CYCLICAL_TRANSFORMATION: ["循环", "周期", "轮回", "轮转", "流转"],
    
    ProblemType.EMERGENT_ORDER: ["涌现", "秩序", "自发秩序", "自组织", "规律"],
    ProblemType.NETWORK_DYNAMICS: ["网络", "连接", "关系", "互动", "动态"],
    ProblemType.ADAPTIVE_EVOLUTION: ["适应", "演化", "进化", "淘汰", "选择"],
    
    ProblemType.SOCIAL_STRUCTURE_ANALYSIS: ["社会结构", "阶层", "分层", "分化", "结构"],
    ProblemType.CLASS_MOBILITY: ["阶层流动", "上升", "下沉", "通道", "壁垒"],
    ProblemType.SOCIAL_STRATIFICATION: ["社会分层", "等级", "分化", "差距", "分化"],
    ProblemType.COLLECTIVE_ACTION: ["集体行动", "群体行为", "协调", "合作", "困境"],
    
    ProblemType.COGNITIVE_BIAS_V62: ["认知偏差", "偏见", "判断失误", "心理陷阱"],
    ProblemType.DECISION_MAKING_BEHAVIOR: ["决策行为", "判断", "选择", "偏好", "偏差"],
    ProblemType.MARKET_BEHAVIOR: ["市场行为", "消费行为", "购买", "选择", "偏好"],
    ProblemType.NUDGE_POLICY: ["助推政策", "行为政策", "引导", "设计", "激励"],
    
    ProblemType.MEDIA_EFFECT: ["媒介效果", "传播效果", "影响", "覆盖", "触达"],
    ProblemType.PUBLIC_OPINION_FORMATION: ["舆论", "舆情", "民意", "观点", "形成"],
    ProblemType.INFORMATION_CASCADE: ["信息级联", "传播", "扩散", "蔓延", "传染"],
    ProblemType.DISCOURSE_ANALYSIS: ["话语", "语篇", "文本", "分析", "解读"],
    ProblemType.INTERPERSONAL_COMMUNICATION: ["人际传播", "沟通", "交流", "互动", "交往"],
    
    ProblemType.CULTURAL_PATTERN_RECOGNITION: ["文化模式", "类型", "模板", "套路", "形态"],
    ProblemType.SYMBOL_SYSTEM_ANALYSIS: ["符号", "象征", "意义", "解码", "解读"],
    ProblemType.RITUAL_CONTEXT_ANALYSIS: ["仪式", "语境", "背景", "情境", "场景"],
    
    ProblemType.INSTITUTIONAL_POLITICAL_ANALYSIS: ["制度", "政治分析", "治理", "政策"],
    ProblemType.POLICY_GAME_THEORY: ["政策博弈", "博弈", "策略互动", "竞合"],
    ProblemType.MARKET_REGULATION_ANALYSIS: ["市场监管", "规制", "监管", "合规"],
    ProblemType.PUBLIC_CHOICE: ["公共选择", "政府", "官员", "寻租", "利益集团"],
    
    ProblemType.ORGANIZATIONAL_CHANGE_V62: ["组织变革", "转型", "变革", "调整", "改造"],
    ProblemType.LEADERSHIP_STYLE_ANALYSIS: ["领导风格", "领导力", "风格", "类型", "特质"],
    ProblemType.TEAM_COHESION_ANALYSIS: ["团队凝聚力", "凝聚力", "士气", "氛围"],
    
    ProblemType.CONFORMITY_BEHAVIOR: ["从众", "随大流", "跟随", "效仿", "模仿"],
    ProblemType.AUTHORITY_OBEDIENCE: ["服从", "顺从", "权威", "盲从", "屈服"],
    ProblemType.SOCIAL_INFLUENCE_MECHANISM: ["社会影响", "影响机制", "传染", "模仿"],
    ProblemType.GROUP_THINK_ANALYSIS: ["群体思维", "集体思考", "思维", "极化", "盲从"],
    
    ProblemType.TALENT_PIPELINE: ["人才梯队", "后备", "培养", "储备", "梯队"],
    ProblemType.ORGANIZATIONAL_CULTURE: ["组织文化", "文化", "氛围", "价值观", "理念"],
    ProblemType.BRAND_CULTURE: ["品牌文化", "品牌", "内涵", "调性", "定位"],
    ProblemType.PHILOSOPHY_OF_MIND: ["心学", "良知", "知行合一", "致良知", "修行"],
    ProblemType.DECISION_FRAMEWORK: ["决策框架", "框架", "方法论", "工具", "模型"],
    ProblemType.RESOURCE_ECOLOGY: ["资源生态", "生态", "资源", "配置", "整合"],
    ProblemType.INNOVATION_ECOLOGY: ["创新生态", "生态", "环境", "土壤", "氛围"],
    
    # 历史思想三维度缺失关键词
    ProblemType.HISTORICAL_ANALYSIS: ["历史分析", "历史", "朝代", "演变", "溯源"],
    ProblemType.THOUGHT_EVOLUTION: ["思想演进", "思想", "流派", "学派", "演变"],
    ProblemType.ECONOMIC_EVOLUTION: ["经济演进", "经济", "产业", "发展", "演变"],
    ProblemType.TECH_HISTORY: ["科技演进", "科技", "技术", "发明", "演变"],
    ProblemType.CROSS_DIMENSION: ["跨维度洞察", "跨维度", "跨界", "融合", "综合"],
    ProblemType.PARADIGM_SHIFT: ["范式转换", "范式", "转型", "革命", "突破"],
    
    # WCC智慧演化缺失关键词
    ProblemType.META_PERSPECTIVE: ["元视角", "升维", "维度", "层次", "抽象"],
    ProblemType.CIVILIZATION_ANALYSIS: ["文明诊断", "文明", "演化", "进程", "阶段"],
    ProblemType.COSMIC_COGNITION: ["宇宙认知", "宇宙", "世界观", "宏观", "尺度"],
    ProblemType.SCALE_TRANSFORMATION: ["尺度转换", "尺度", "规模", "体量", "转换"],
    ProblemType.WORLDVIEW_SHIFT: ["世界观转换", "世界观", "认知", "观念", "转变"],
    ProblemType.WISDOM_EVOLUTION: ["智慧演化", "智慧", "思想", "演进", "升级"],
    ProblemType.TECH_EVOLUTION: ["技术进化", "技术", "创新", "迭代", "升级"],
    
    # 自然科学缺失关键词
    ProblemType.PHYSICS_ANALYSIS: ["物理分析", "物理", "力学", "能量", "规律"],
    ProblemType.LIFE_SCIENCE: ["生命科学", "生物", "生命", "演化", "生态"],
    ProblemType.EARTH_SYSTEM: ["地球系统", "地球", "生态", "环境", "系统"],
    ProblemType.COSMOS_EXPLORATION: ["宇宙探索", "宇宙", "星际", "太空", "探索"],
    ProblemType.SCALE_CROSSING: ["跨尺度思维", "跨尺度", "微观", "宏观", "尺度"],
    
    # 其他缺失关键词
    ProblemType.APOCALYPSE: ["灭世危机", "末日", "灾难", "危机", "崩溃"],
    ProblemType.BUDDHIST_SUB_SCHOOL: ["佛家子学", "禅宗", "净土", "密宗", "佛学"],
    ProblemType.COSMIC_HARMONY: ["天人合一", "天道", "和谐", "宇宙", "自然"],
    ProblemType.CREATION_MYTH: ["创世叙事", "创世", "神话", "起源", "传说"],
    ProblemType.CROSS_CULTURAL_ADAPTATION: ["跨文化适应", "跨文化", "本土化", "适应", "文化"],
    ProblemType.CYCLICAL: ["循环哲学", "循环", "周期", "轮回", "轮回"],
    ProblemType.DAOIST_SUB_SCHOOL: ["道家子学", "道教", "玄学", "老庄", "道家"],
    ProblemType.DEFENSE_FORTIFICATION: ["防御工事", "防御", "防守", "城防", "筑城"],
    ProblemType.INCENTIVE_DESIGN: ["激励设计", "激励", "奖励", "动机", "设计"],
    ProblemType.INSTITUTIONAL_SEDIMENTATION: ["制度沉淀", "制度", "惯性", "沉淀", "积累"],
    ProblemType.INSTITUTIONAL_SOCIOLOGY: ["制度社会学", "制度", "社会", "结构", "规范"],
    ProblemType.INTERPERSONAL_RELATIONSHIP: ["人际关系", "人际", "关系", "社交", "相处"],
    ProblemType.MILITARY_SUB_SCHOOL: ["兵法子学", "兵家", "战法", "兵法", "战术"],
    ProblemType.ORGANIZATIONAL_CULTURE_V62: ["组织文化诊断", "组织文化", "诊断", "氛围", "价值观"],
    ProblemType.PSYCHOLOGICAL_ARITHMETIC: ["心理运算", "心理", "计算", "决策", "权衡"],
    ProblemType.SEASONAL_RHYTHM: ["时节节律", "时节", "季节", "节律", "周期"],
    ProblemType.STATE_CAPACITY: ["国家能力", "国家", "政府", "能力", "治理"],
    ProblemType.STATE_CONSOLIDATION: ["国家集权", "集权", "中央", "统一", "巩固"],
    ProblemType.TRAUMA_HEALING: ["心理创伤修复", "创伤", "修复", "治愈", "心理"],
    ProblemType.WAR_ECONOMY_NEXUS: ["经战主链", "经战", "战争", "经济", "联动"],

    # 增长与行业 (5) — v2.0.0 新增（Growth+Industry整合）
    ProblemType.GROWTH_STRATEGY: ["增长战略", "增长", "拉新", "获客", "GMV", "ARR", "MRR", "增长引擎", "增长杠杆"],
    ProblemType.INDUSTRY_ADAPTATION: ["行业适配", "行业分析", "行业特性", "赛道", "行业基准", "行业画像"],
    ProblemType.GROWTH_DIAGNOSIS: ["增长诊断", "增长瓶颈", "增长停滞", "增长分析", "增长健康度", "北极星指标"],
    ProblemType.AARRR_FRAMEWORK: ["海盗指标", "AARRR", "获客", "激活", "留存", "变现", "推荐", "增长漏斗"],
    ProblemType.INDUSTRY_BENCHMARK: ["行业基准", "行业对比", "竞品基准", "行业均值", "benchmark", "行业最佳实践"],
}


# ============================================================
# 数据结构
# ============================================================

@dataclass
class WisdomRecommendation:
    """智慧推荐"""
    school: WisdomSchool
    confidence: float
    primary_method: str
    reasoning: str
    advice: str
    ancient_source: str
    modern_application: str


@dataclass
class PanWisdomResult:
    """Pan-Wisdom Tree 推理结果"""
    request_id: str
    problem: str
    identified_types: List[ProblemType]
    recommended_schools: List[WisdomRecommendation]
    fusion_insights: List[str]
    final_recommendations: List[str]
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================
# 问题类型识别器
# ============================================================

class ProblemIdentifier:
    """问题类型识别器（L1预加载优化版）"""
    
    # 类级别标志：是否已预加载
    _preloaded = False
    
    @classmethod
    def _ensure_preloaded(cls):
        """确保预加载完成"""
        if not cls._preloaded:
            PanWisdomPreloader.preload()
            cls._preloaded = True
    
    @classmethod
    def identify(cls, text: str) -> List[Tuple[ProblemType, float]]:
        """
        识别问题类型（使用预加载索引，O(1)查找）
        
        Args:
            text: 问题文本
            
        Returns:
            [(问题类型, 置信度), ...] 按置信度排序
        """
        # 确保预加载
        cls._ensure_preloaded()
        
        text_lower = text.lower()
        scores: Dict[ProblemType, float] = {}
        
        # 使用预加载的关键词集合进行O(1)查找
        # KEYWORD_SET_INDEX 的 key 是字符串（枚举名），需要转回枚举
        for problem_type_name, keyword_set in PanWisdomPreloader.KEYWORD_SET_INDEX.items():
            score = 0
            for keyword in keyword_set:
                if keyword in text_lower:
                    score += 1.0
            if score > 0:
                # 归一化并添加基础分
                confidence = min(0.95, 0.3 + score * 0.15)
                # 转回 ProblemType 枚举
                try:
                    problem_type_enum = ProblemType[problem_type_name]
                except KeyError:
                    continue
                scores[problem_type_enum] = confidence
        
        # 按置信度排序
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:5]  # 返回前5个最可能的问题类型
    
    @classmethod
    def identify_fast(cls, text: str) -> List[Tuple[ProblemType, float]]:
        """
        快速识别（使用扁平化映射，O(n)单次扫描，无正则）
        
        Args:
            text: 问题文本
            
        Returns:
            [(问题类型, 置信度), ...]
        """
        cls._ensure_preloaded()
        text_lower = text.lower()
        
        # 使用扁平化映射：直接查找关键词对应的问题类型
        # O(n) 单次扫描，n = 文本长度
        scores: Dict[ProblemType, int] = {}
        
        # 方法：遍历文本中的每个位置，尝试匹配关键词
        # 优化：只对长度>=2的子串进行查找
        for i in range(len(text_lower)):
            # 尝试不同长度的关键词（2-8个字符）
            for kw_len in range(2, min(9, len(text_lower) - i + 1)):
                substr = text_lower[i:i + kw_len]
                problem_names = PanWisdomPreloader.get_keyword_to_problem(substr)
                if problem_names:
                    for pname in problem_names:
                        # 转换为 ProblemType 枚举
                        try:
                            pt = ProblemType[pname]
                            scores[pt] = scores.get(pt, 0) + 1
                        except KeyError:
                            pass
                    # 找到匹配后，跳过已匹配的部分
                    i += kw_len - 1
                    break
        
        # 如果没有匹配到任何关键词，回退到普通方法
        if not scores:
            return cls.identify(text)
        
        # 转换为置信度
        result = []
        for pt, score in scores.items():
            confidence = min(0.95, 0.3 + score * 0.15)
            result.append((pt, confidence))
        
        return sorted(result, key=lambda x: x[1], reverse=True)[:5]
    
    @classmethod
    def get_primary_type(cls, text: str) -> Optional[ProblemType]:
        """获取最主要的问题类型"""
        identified = cls.identify(text)
        if identified:
            return identified[0][0]
        return None


# ============================================================
# 学派推荐器
# ============================================================

class SchoolRecommender:
    """学派推荐器（L2 LRU缓存优化版）"""
    
    # 类级别缓存引用
    _cache = None
    
    # 学派特性映射（42个学派完整信息 — 类级别，只初始化一次）
    _SCHOOL_INFO_MAP: Dict = None
    
    @classmethod
    def _ensure_cache(cls):
        """确保缓存已初始化"""
        if cls._cache is None:
            cls._cache = get_pan_wisdom_cache()
    
    @classmethod
    def _ensure_school_info_map(cls):
        """确保学派信息映射已初始化（懒加载，仅一次）"""
        if cls._SCHOOL_INFO_MAP is not None:
            return
        cls._SCHOOL_INFO_MAP = {
            # 东方哲学经典
            WisdomSchool.DAOIST: ("道法自然", "顺应自然规律，无为而治", 
                                 "《道德经》", "战略规划、危机处理、长期平衡"),
            WisdomSchool.CONFUCIAN: ("仁义礼智", "以德治国，修身齐家", 
                                    "《论语》", "人才培养、组织治理、文化建设"),
            WisdomSchool.BUDDHIST: ("因果轮回", "放下执念，内心平静", 
                                   "《金刚经》", "心态调适、团队和谐、利益协调"),
            WisdomSchool.SUFU: ("素书三章", "以德为本，知人善任", 
                               "《素书》", "领导决策、风险管理、人才识别"),
            WisdomSchool.MILITARY: ("知己知彼", "兵贵神速，出奇制胜", 
                                   "《孙子兵法》", "竞争策略、市场攻防、谈判博弈"),
            WisdomSchool.LVSHI: ("杂家融合", "兼容并蓄，因时制宜", 
                                "《吕氏春秋》", "公私抉择、时令管理、阴阳调和"),
            WisdomSchool.HONGMING: ("东西融合", "中学为体，西学为用", 
                                  "《中国人的精神》", "跨文化融合、文明诊断"),
            WisdomSchool.METAPHYSICS: ("术数时空", "天时地利，阴阳五行", 
                                     "《易经》", "时机判断、福祸评估、运势分析"),
            
            # 文明与科幻
            WisdomSchool.CIVILIZATION: ("文明演化", "历史规律，演进规律", 
                                       "《文明》系列", "文明诊断、国家能力、制度沉淀"),
            WisdomSchool.CIV_WAR_ECONOMY: ("经战主链", "战争经济，互相转化", 
                                          "克劳塞维茨", "经战联动、军事经济"),
            WisdomSchool.SCI_FI: ("科幻思维", "未来视角，维度超越", 
                                 "科幻文学", "维度超越、生存法则、尺度思维"),
            WisdomSchool.GROWTH: ("成长思维", "突破局限，持续进化", 
                                "《终身成长》", "成长突破、逆向思考、闭环执行"),
            WisdomSchool.MYTHOLOGY: ("神话智慧", "原型叙事，文化基因", 
                                     "世界神话", "创世叙事、灭世危机、循环哲学"),
            
            # 文化与叙事
            WisdomSchool.LITERARY: ("文学叙事", "故事力量，叙事构建", 
                                  "经典文学", "叙事构建、韧性评估、人物分析"),
            WisdomSchool.ANTHROPOLOGY: ("人类学", "文化田野，跨文化洞察", 
                                        "马林诺夫斯基", "跨文化沟通、仪式分析、文化变迁"),
            WisdomSchool.BEHAVIOR: ("行为塑造", "习惯养成，助推设计", 
                                  "《助推》", "习惯设计、自控力管理、助推设计"),
            
            # 思维方法
            WisdomSchool.SCIENCE: ("科学思维", "假设验证，实验精神", 
                                 "《科学革命》", "科学验证、系统分析、证据评估"),
            WisdomSchool.SOCIAL_SCIENCE: ("社会科学", "社会规律，人类行为", 
                                          "涂尔干/韦伯", "营销策略、市场分析、社会发展"),
            WisdomSchool.YANGMING: ("心学实践", "知行合一，致良知", 
                                  "王阳明", "自我实现、心学实践、修炼提升"),
            WisdomSchool.DEWEY: ("反省思维", "持续反思，不断改进", 
                                "杜威", "反省思维、批判性思考"),
            WisdomSchool.TOP_METHODS: ("顶级思维法", "多元思维模型", 
                                     "芒格", "多元思维、跨学科整合"),
            WisdomSchool.NATURAL_SCIENCE: ("自然科学", "物理法则，生命演化", 
                                          "《自然》期刊", "物理分析、生命科学、地球系统"),
            
            # 中国消费与WCC
            WisdomSchool.CHINESE_CONSUMER: ("中国社会消费", "本土洞察，消费者心理解析", 
                                           "中国市场", "C端营销、品牌战略、消费心理"),
            WisdomSchool.WCC: ("WCC智慧演化", "智慧升级，维度跃迁", 
                              "WCC体系", "元视角、文明诊断、宇宙认知"),
            
            # 历史思想
            WisdomSchool.HISTORICAL_THOUGHT: ("历史思想", "以史为鉴，古今对话", 
                                             "历史学派", "历史分析、思想演进、范式转换"),
            
            # V6.0 第二阶段
            WisdomSchool.PSYCHOLOGY: ("心理学", "行为动机，心理解析", 
                                    "弗洛伊德/荣格", "人格分析、动机分析、人际关系"),
            WisdomSchool.SYSTEMS: ("系统论", "整体涌现，动态平衡", 
                                  "《系统之美》", "复杂系统建模、反馈回路、系统均衡"),
            WisdomSchool.MANAGEMENT: ("管理学", "效率驱动，目标达成", 
                                     "德鲁克", "战略规划、绩效管理、变革管理"),
            WisdomSchool.ZONGHENG: ("纵横家", "联盟博弈，外交策略", 
                                  "《战国策》", "外交谈判、联盟构建、权力平衡"),
            WisdomSchool.MOZI: ("墨家", "兼爱非攻，逻辑推理", 
                               "《墨子》", "逻辑推论、成本优化、技术创新"),
            WisdomSchool.FAJIA: ("法家", "法术势，赏罚分明", 
                                "《韩非子》", "制度建设、绩效管理、权力架构"),
            
            # V6.0 第三阶段
            WisdomSchool.ECONOMICS: ("经济学", "供需均衡，资源配置", 
                                    "亚当·斯密", "资源配置、投资决策、市场效率"),
            WisdomSchool.MINGJIA: ("名家", "名实关系，逻辑思辨", 
                                  "公孙龙/惠施", "逻辑悖论、名实辨析、辩证推理"),
            WisdomSchool.WUXING: ("阴阳家", "五行生克，阴阳辩证", 
                                "邹衍", "五行分析、时节节律、天人合一"),
            WisdomSchool.COMPLEXITY: ("复杂性科学", "涌现秩序，自适应演化", 
                                     "圣塔菲", "涌现识别、网络动力学、自适应演化"),
            
            # V6.2 社会科学智慧版
            WisdomSchool.SOCIOLOGY: ("社会学", "社会结构，集体行动", 
                                    "马克思/韦伯", "社会结构分析、阶层流动、集体行动"),
            WisdomSchool.BEHAVIORAL_ECONOMICS: ("行为经济学", "有限理性，行为偏差", 
                                                "卡尼曼/塞勒", "认知偏差、激励设计、助推政策"),
            WisdomSchool.COMMUNICATION: ("传播学", "信息传播，舆论形成", 
                                        "拉斯韦尔", "媒介效果、舆论分析、信息级联"),
            WisdomSchool.CULTURAL_ANTHROPOLOGY: ("文化人类学", "文化模式，符号系统", 
                                                 "格尔茨", "文化模式识别、符号分析、仪式语境"),
            WisdomSchool.POLITICAL_ECONOMICS: ("政治经济学", "制度政治，政策博弈", 
                                               "布坎南", "制度政治分析、政策博弈、公共选择"),
            WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY: ("组织心理学", "组织文化，领导风格", 
                                                     "阿吉里斯", "组织变革、领导风格、团队凝聚力"),
            WisdomSchool.SOCIAL_PSYCHOLOGY: ("社会心理学", "从众服从，社会影响", 
                                             "阿希/米尔格拉姆", "从众行为、权威服从、群体思维"),
        }
        # 默认回退
        cls._DEFAULT_INFO = ("综合智慧", "因时制宜", "古今融合", "通用问题")
    
    @classmethod
    def recommend(cls, problem_type: Any, top_k: int = 5) -> List[WisdomRecommendation]:
        """
        根据问题类型推荐学派（使用LRU缓存）
        
        Args:
            problem_type: 问题类型（ProblemType枚举或字符串）
            top_k: 返回前k个推荐
            
        Returns:
            学派推荐列表
        """
        # 类型兼容：支持 ProblemType 或 str
        if isinstance(problem_type, str):
            try:
                problem_type = ProblemType[problem_type]
            except KeyError:
                # 如果是value（中文名），反向查找
                for pt in ProblemType:
                    if pt.value == problem_type:
                        problem_type = pt
                        break
                else:
                    # 都没找到，使用第一个枚举作为默认值
                    problem_type = list(ProblemType)[0]
        
        # 检查缓存
        cls._ensure_cache()
        cache_key = f"rec_{problem_type.name}_{top_k}"
        cached = cls._cache.get_recommendation(cache_key)
        if cached:
            # 将缓存的dict转换回WisdomRecommendation
            return [WisdomRecommendation(**d) for d in cached]
        
        # 从映射矩阵获取
        school_weights = PROBLEM_TO_SCHOOLS.get(problem_type, [])
        
        recommendations = []
        for school, weight in school_weights[:top_k]:
            rec = cls._create_recommendation(school, weight, problem_type)
            recommendations.append(rec)
        
        # 缓存结果（存储为dict，避免序列化问题）
        cls._cache.cache_recommendation(
            cache_key, 
            [rec.__dict__ for rec in recommendations]
        )
        
        return recommendations
    
    @classmethod
    def recommend_for_text(cls, text: str, top_k: int = 5) -> List[WisdomRecommendation]:
        """
        根据文本推荐学派（自动识别问题类型）
        
        Args:
            text: 问题文本
            top_k: 返回前k个推荐
            
        Returns:
            学派推荐列表
        """
        # 识别问题类型
        primary_type = ProblemIdentifier.get_primary_type(text)
        
        if primary_type:
            return cls.recommend(primary_type, top_k)
        
        # 默认推荐（通用问题）
        return cls._get_default_recommendations(top_k)
    
    @classmethod
    def _create_recommendation(cls, school: WisdomSchool, weight: float, 
                               problem_type: ProblemType) -> WisdomRecommendation:
        """创建学派推荐（使用类级别学派信息映射 + LRU缓存）"""
        cls._ensure_school_info_map()
        
        # 使用缓存获取信息
        cls._ensure_cache()
        cache_key = f"school_info_{school.name}"
        info = cls._cache.get_school_info(cache_key)
        
        if info is None:
            info = cls._SCHOOL_INFO_MAP.get(school, cls._DEFAULT_INFO)
            cls._cache.cache_school_info(cache_key, info)
        
        return WisdomRecommendation(
            school=school,
            confidence=weight,
            primary_method=info[0],
            reasoning=f"基于{problem_type.value}问题，{school.value}学派提供独特视角",
            advice=info[1],
            ancient_source=info[2],
            modern_application=info[3]
        )
    
    @classmethod
    def _get_default_recommendations(cls, top_k: int) -> List[WisdomRecommendation]:
        """获取默认推荐"""
        default_schools = [
            WisdomSchool.DAOIST,
            WisdomSchool.CONFUCIAN,
            WisdomSchool.MILITARY,
            WisdomSchool.SYSTEMS,
            WisdomSchool.PSYCHOLOGY,
        ]
        
        recommendations = []
        for i, school in enumerate(default_schools[:top_k]):
            rec = cls._create_recommendation(school, 0.7 - i * 0.1, 
                                            ProblemType.STRATEGY)
            recommendations.append(rec)
        
        return recommendations


# ============================================================
# Pan-Wisdom Tree 核心引擎
# ============================================================

class PanWisdomTree:
    """
    Pan-Wisdom Tree 核心引擎 V2.0.0
    万法智慧树 - 智能学派融合推理系统（预加载+懒加载版）
    
    加载层级：
    - L0（零级）: 枚举、类定义 → 瞬时
    - L1（一级）: 预加载正则+索引 → <1ms
    - L2（二级）: LRU缓存 → 首次<5ms，后续<0.1ms
    - L3（三级）: Track B神行轨 → 按需加载
    """
    
    def __init__(self, enable_track_b: bool = False):
        self.name = "Pan-Wisdom Tree"
        self.version = "7.0.0"
        self._identifier = ProblemIdentifier()
        self._recommender = SchoolRecommender()
        self._track_b_enabled = enable_track_b
        self._track_b = None
        self._track_b_loaded = False
        # Growth + Industry 引擎（懒加载）
        self._growth_bridge = None
        self._growth_loaded = False
    
    def reason(self, problem: str, context: Dict[str, Any] = None) -> PanWisdomResult:
        """
        执行 Pan-Wisdom Tree 推理
        
        Args:
            problem: 问题描述
            context: 上下文信息
            
        Returns:
            推理结果
        """
        # 1. 识别问题类型
        identified_types = self._identifier.identify(problem)
        primary_type = identified_types[0][0] if identified_types else None
        
        # 2. 推荐学派
        if primary_type:
            recommended_schools = self._recommender.recommend(primary_type)
        else:
            recommended_schools = self._recommender.recommend_for_text(problem)
        
        # 3. 生成融合洞察
        fusion_insights = self._generate_fusion_insights(
            problem, primary_type, recommended_schools
        )

        # 3.5 集成 Growth+Industry 引擎（v7.0 新增）
        growth_insights = self._integrate_growth_industry(
            problem, primary_type, identified_types
        )
        if growth_insights:
            fusion_insights.extend(growth_insights)

        # 4. 生成最终建议
        final_recommendations = self._generate_recommendations(
            problem, primary_type, recommended_schools
        )

        # 4.5 集成 Growth+Industry 建议（v7.0 新增）
        growth_recs = self._integrate_growth_recommendations(
            problem, primary_type
        )
        if growth_recs:
            final_recommendations.extend(growth_recs)

        # 5. 计算整体置信度
        confidence = self._calculate_confidence(identified_types, recommended_schools)
        
        return PanWisdomResult(
            request_id=str(uuid.uuid4())[:8],
            problem=problem,
            identified_types=[t[0] for t in identified_types],
            recommended_schools=recommended_schools,
            fusion_insights=fusion_insights,
            final_recommendations=final_recommendations,
            confidence=confidence
        )
    
    def _generate_fusion_insights(self, problem: str, 
                                  primary_type: Optional[ProblemType],
                                  schools: List[WisdomRecommendation]) -> List[str]:
        """生成融合洞察"""
        insights = []
        
        # 问题本质洞察
        insights.append(f"问题聚焦: {primary_type.value if primary_type else '综合分析'}")
        
        # 学派视角洞察
        if len(schools) >= 2:
            insights.append(f"多元视角: 融合{schools[0].school.value}与{schools[1].school.value}的智慧")
        
        # 深度洞察
        if len(schools) >= 3:
            top_3 = [s.school.value for s in schools[:3]]
            insights.append(f"立体分析: 【{'/'.join(top_3)}】三学派的互补视角")
        
        return insights
    
    def _generate_recommendations(self, problem: str,
                                   primary_type: Optional[ProblemType],
                                   schools: List[WisdomRecommendation]) -> List[str]:
        """生成最终建议"""
        recommendations = []
        
        # 主建议
        if schools:
            top = schools[0]
            recommendations.append(
                f"核心建议({top.school.value}): {top.advice}"
            )
            recommendations.append(
                f"方法论: {top.primary_method}"
            )
            recommendations.append(
                f"现代应用: {top.modern_application}"
            )
        
        # 补充建议
        if len(schools) >= 2:
            sec = schools[1]
            recommendations.append(
                f"补充视角({sec.school.value}): {sec.advice}"
            )
        
        return recommendations
    
    def _calculate_confidence(self, 
                             identified_types: List[Tuple[ProblemType, float]],
                             schools: List[WisdomRecommendation]) -> float:
        """计算置信度"""
        if not identified_types or not schools:
            return 0.6
        
        type_confidence = identified_types[0][1] if identified_types else 0.5
        school_confidence = schools[0].confidence if schools else 0.5
        
        # 综合置信度
        confidence = (type_confidence * 0.4 + school_confidence * 0.6)
        return min(0.95, max(0.5, confidence))

    def _is_growth_or_industry(self, primary_type: Optional[ProblemType]) -> bool:
        """判断是否为增长/行业相关问题"""
        if primary_type is None:
            return False
        growth_types = {
            ProblemType.GROWTH_STRATEGY,
            ProblemType.INDUSTRY_ADAPTATION,
            ProblemType.GROWTH_DIAGNOSIS,
            ProblemType.AARRR_FRAMEWORK,
            ProblemType.INDUSTRY_BENCHMARK,
        }
        return primary_type in growth_types

    def _integrate_growth_industry(
        self, problem: str,
        primary_type: Optional[ProblemType],
        identified_types: List[Tuple[ProblemType, float]],
    ) -> List[str]:
        """
        集成 Growth+Industry 引擎，生成增长/行业融合洞察
        v7.0 新增
        """
        if not self._is_growth_or_industry(primary_type):
            return []

        bridge = self._get_growth_bridge()
        if not bridge:
            return []

        insights = []
        get_rec = bridge["get_growth_recommendation"]
        get_bagua = bridge["get_bagua_analysis"]

        # 增长战略推荐
        recs = get_rec(problem, top_n=3)
        if recs:
            top = recs[0]
            insights.append(f"增长战略推荐: {top['template'].name}（置信度 {top['confidence']:.2f}）")
            insights.append(f"增长杠杆: {', '.join(top['template'].primary_levers)}")

        # 八卦增长分析
        bagua = get_bagua(problem)
        if bagua:
            insights.append(
                f"八卦增长分析: 主导卦={bagua['dominant_bagua']} {bagua['symbol']}，"
                f"涉及领域: {', '.join(bagua['domains'])}"
            )

        return insights

    def _integrate_growth_recommendations(
        self, problem: str,
        primary_type: Optional[ProblemType],
    ) -> List[str]:
        """
        集成 Growth+Industry 引擎，生成增长/行业具体建议
        v7.0 新增
        """
        if not self._is_growth_or_industry(primary_type):
            return []

        bridge = self._get_growth_bridge()
        if not bridge:
            return []

        recommendations = []
        get_rec = bridge["get_growth_recommendation"]

        recs = get_rec(problem, top_n=2)
        for rec in recs:
            tpl = rec["template"]
            recommendations.append(f"【{tpl.name}】")
            recommendations.append(f"  关键策略: {', '.join(tpl.key_strategies)}")
            recommendations.append(f"  关键指标: {', '.join(tpl.key_metrics)}")
            for k, v in tpl.benchmarks.items():
                recommendations.append(f"  基准 {k}: {v}")

        return recommendations

    def _get_track_b(self):
        """懒加载获取Track B（仅当启用时）"""
        if not self._track_b_enabled:
            return None

        if self._track_b_loaded:
            return self._track_b

        try:
            on_demand = get_pan_wisdom_on_demand()
            self._track_b = on_demand.get_track_b()
            self._track_b_loaded = True
            return self._track_b
        except Exception:
            self._track_b_loaded = True
            return None

    def _get_growth_bridge(self):
        """懒加载 Growth+Industry 桥接模块"""
        if self._growth_loaded:
            return self._growth_bridge

        try:
            from .growth_industry_bridge import (
                get_growth_recommendation,
                get_industry_profile,
                get_bagua_analysis,
                list_growth_templates,
                list_industry_profiles,
            )
            self._growth_bridge = {
                "get_growth_recommendation": get_growth_recommendation,
                "get_industry_profile": get_industry_profile,
                "get_bagua_analysis": get_bagua_analysis,
                "list_growth_templates": list_growth_templates,
                "list_industry_profiles": list_industry_profiles,
            }
            self._growth_loaded = True
        except Exception:
            self._growth_bridge = None
            self._growth_loaded = True
        return self._growth_bridge

    def _check_web_search_available(self) -> bool:
        """检查网络搜索是否可用"""
        global _web_search_available
        if _web_search_available is not None:
            return _web_search_available
        try:
            from .web_search_engine import is_online
            _web_search_available = is_online()
        except ImportError:
            try:
                from web_search_engine import is_online
                _web_search_available = is_online()
            except Exception:
                _web_search_available = False
        return _web_search_available

    def _enhance_with_web_search(
        self,
        problem: str,
        schools: List[WisdomRecommendation]
    ) -> Dict[str, Any]:
        """
        使用网络搜索增强学派推荐

        当本地知识不足以提供足够置信度时，
        自动触发网络搜索获取最新信息
        """
        # 检查是否需要网络搜索
        need_web_search = (
            not schools or
            all(s.confidence < 0.7 for s in schools) or
            any(kw in problem for kw in ["最新", "2024", "2025", "2026", "趋势", "动态"])
        )

        if not need_web_search:
            return {"enhanced": False, "reason": "本地知识足够"}

        # 尝试网络搜索
        try:
            from .web_search_engine import search_web
        except ImportError:
            try:
                from web_search_engine import search_web
            except ImportError:
                return {"enhanced": False, "reason": "WebSearchEngine不可用"}

        if not self._check_web_search_available():
            return {"enhanced": False, "reason": "网络不可用"}

        try:
            # 构建搜索查询：结合问题和学派
            search_queries = []
            for school in schools[:2]:
                query = f"{school.school.value} {problem[:20]}"
                search_queries.append(query)

            # 执行搜索
            web_results = []
            for query in search_queries[:2]:
                response = search_web(query, max_results=3)
                if response.success:
                    web_results.extend(response.results[:2])

            if not web_results:
                return {"enhanced": False, "reason": "搜索无结果"}

            # 提取网络洞察
            web_insights = []
            for r in web_results[:3]:
                web_insights.append({
                    "title": r.title[:50] if r.title else "",
                    "snippet": r.snippet[:100] if r.snippet else "",
                    "source": r.source,
                })

            return {
                "enhanced": True,
                "reason": "网络搜索增强",
                "web_insights": web_insights,
                "total_results": len(web_results),
            }

        except Exception as e:
            return {"enhanced": False, "reason": f"搜索异常: {str(e)[:30]}"}

    def enable_track_b(self):
        """启用Track B神行轨集成"""
        self._track_b_enabled = True
    
    def is_track_b_enabled(self) -> bool:
        """检查Track B是否启用"""
        return self._track_b_enabled
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        return get_pan_wisdom_cache().get_cache_stats()


# ============================================================
# 全局单例和快捷函数
# ============================================================

_pan_wisdom_instance: Optional[PanWisdomTree] = None
_pan_wisdom_lock = threading.Lock()


def get_pan_wisdom_tree() -> PanWisdomTree:
    """获取 Pan-Wisdom Tree 单例（线程安全双重检查锁）"""
    global _pan_wisdom_instance
    if _pan_wisdom_instance is None:
        with _pan_wisdom_lock:
            if _pan_wisdom_instance is None:
                _pan_wisdom_instance = PanWisdomTree()
    return _pan_wisdom_instance


# 别名，兼容 closed_loop_solver 等模块的导入
get_pan_wisdom = get_pan_wisdom_tree

# 兼容 closed_loop_solver 等模块的导入\get_pan_wisdom = get_pan_wisdom_tree

def solve_with_wisdom(problem: str, context: Dict[str, Any] = None) -> PanWisdomResult:
    """
    使用 Pan-Wisdom Tree 解决问题
    
    Args:
        problem: 问题描述
        context: 上下文信息
        
    Returns:
        推理结果
    """
    tree = get_pan_wisdom_tree()
    return tree.reason(problem, context)


def identify_problem_type(text: str) -> List[ProblemType]:
    """识别问题类型"""
    identified = ProblemIdentifier.identify(text)
    return [t[0] for t in identified]


def recommend_schools(problem_type: ProblemType, top_k: int = 5) -> List[WisdomRecommendation]:
    """推荐学派"""
    return SchoolRecommender.recommend(problem_type, top_k)


def recommend_schools_for_text(text: str, top_k: int = 5) -> List[WisdomRecommendation]:
    """根据文本推荐学派"""
    return SchoolRecommender.recommend_for_text(text, top_k)


# ============================================================
# 导出
# ============================================================

__all__ = [
    # 版本信息
    "__version__",
    # 枚举
    "WisdomSchool",
    "ProblemType",
    # 数据结构
    "WisdomRecommendation",
    "PanWisdomResult",
    # 核心类
    "PanWisdomTree",
    "ProblemIdentifier",
    "SchoolRecommender",
    # 懒加载类
    "PanWisdomPreloader",
    "PanWisdomLRUCache",
    "PanWisdomOnDemandLoader",
    # 快捷函数
    "get_pan_wisdom_tree",
    "solve_with_wisdom",
    "identify_problem_type",
    "recommend_schools",
    "recommend_schools_for_text",
    # 懒加载快捷函数
    "preload",
    "is_ready",
    "preload_pan_wisdom",
    "get_pan_wisdom_cache",
    "get_pan_wisdom_on_demand",
    "get_pan_wisdom_load_info",
    "clear_pan_wisdom_cache",
    "benchmark_pan_wisdom_load",
    # 常量
    "PROBLEM_TO_SCHOOLS",
    "PROBLEM_KEYWORDS",
    # 向后兼容别名 (V1.0 → V2.0/V2.1)
    "WisdomTreeCore",
    "reason_with_wisdom_tree",
]

__version__ = "6.2.0"


# ============================================================
# 向后兼容别名 (V1.0 → V2.0/V2.1)
# ============================================================
WisdomTreeCore = PanWisdomTree  # V1.0 的类名
reason_with_wisdom_tree = solve_with_wisdom  # V1.0 的函数名


# ============================================================
# 可视化生成功能
# ============================================================

def generate_visualization(output_path: str = None) -> str:
    """
    生成 Pan-Wisdom Tree 可视化 HTML 文件
    
    Args:
        output_path: 输出 HTML 文件路径，默认为 'pan_wisdom_tree_v2_visualization.html'
    
    Returns:
        输出文件的路径
    """
    if output_path is None:
        output_path = "pan_wisdom_tree_visualization.html"
    
    # 读取现有 HTML 模板
    html_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "WISDOM_TREE_V2.html")
    
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 更新标题和版本号
        html_content = re.sub(
            r'<title>.*?</title>',
            '<title>Pan-Wisdom Tree 可视化 - V2.1</title>',
            html_content
        )
        html_content = re.sub(
            r'<p>.*?智慧树.*?</p>',
            '<p>V2.1 - 42个智慧学派 × 165个问题类型</p>',
            html_content
        )
        
        # 保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"可视化文件已生成: {output_path}")
        return output_path
    else:
        # 如果 HTML 模板不存在，生成一个简化版
        print(f"警告: 未找到模板文件 {html_file}")
        print("生成简化版可视化...")
        
        # 生成简化 HTML
        html = _generate_simple_visualization()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"简化版可视化已生成: {output_path}")
        return output_path


def _generate_simple_visualization() -> str:
    """生成简化版可视化 HTML"""
    # 收集数据
    schools_data = []
    for s in WisdomSchool:
        schools_data.append({'id': s.name, 'name': s.value})
    
    problems_data = []
    for pt in ProblemType:
        problems_data.append({'id': pt.name, 'name': pt.value})
    
    # 生成 HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pan-Wisdom Tree 可视化 - V2.1</title>
    <script src="https://unpkg.com/@antv/g6@4.8.24/dist/g6.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; color: #fff; }}
        .header {{ background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; }}
        .header h1 {{ font-size: 2em; margin-bottom: 10px; }}
        .stats {{ display: flex; justify-content: center; gap: 30px; margin-top: 15px; }}
        .stat-item {{ background: rgba(255,255,255,0.15); padding: 10px 20px; border-radius: 20px; }}
        .stat-num {{ font-size: 1.5em; font-weight: bold; color: #ffd700; }}
        .container {{ display: flex; height: calc(100vh - 150px); }}
        #graph {{ flex: 1; margin: 15px; background: rgba(0,0,0,0.2); border-radius: 15px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Pan-Wisdom Tree 可视化</h1>
        <p>V2.1 - {len(schools_data)} 个智慧学派 × {len(problems_data)} 个问题类型</p>
        <div class="stats">
            <div class="stat-item"><div class="stat-num">{len(schools_data)}</div><div>智慧学派</div></div>
            <div class="stat-item"><div class="stat-num">{len(problems_data)}</div><div>问题类型</div></div>
            <div class="stat-item"><div class="stat-num">V2.1</div><div>版本</div></div>
        </div>
    </div>
    <div class="container">
        <div id="graph"></div>
    </div>
    <script>
        const schools = {json.dumps(schools_data, ensure_ascii=False)};
        const problems = {json.dumps(problems_data, ensure_ascii=False)};
        
        const nodes = [];
        const edges = [];
        
        // 中心节点
        const centerX = window.innerWidth / 2;
        const centerY = (window.innerHeight - 150) / 2;
        nodes.push({{ id: 'center', label: 'Pan-Wisdom', x: centerX, y: centerY, size: 80, style: {{ fill: '#667eea', stroke: '#fff', lineWidth: 3 }} }});
        
        // 学派节点
        schools.forEach((s, i) => {{
            const angle = (i / schools.length) * Math.PI * 2;
            const radius = Math.min(centerX, centerY) * 0.35;
            nodes.push({{
                id: s.id,
                label: s.name,
                x: centerX + Math.cos(angle) * radius,
                y: centerY + Math.sin(angle) * radius,
                size: 50,
                style: {{ fill: '#f093fb', stroke: '#fff', lineWidth: 2 }}
            }});
            edges.push({{ source: 'center', target: s.id, style: {{ stroke: '#4facfe', lineWidth: 1, opacity: 0.5 }} }});
        }});
        
        const graph = new G6.Graph({{
            container: 'graph',
            width: window.innerWidth,
            height: window.innerHeight - 150,
            modes: {{ default: ['drag-canvas', 'zoom-canvas', 'drag-node'] }},
            defaultNode: {{
                size: 50,
                style: {{ fill: '#f093fb', stroke: '#fff' }},
                labelCfg: {{ style: {{ fill: '#fff', fontSize: 10 }} }}
            }}
        }});
        
        graph.data({{ nodes, edges }});
        graph.render();
    </script>
</body>
</html>"""
    
    return html


# 添加到 __all__
__all__.append("generate_visualization")
