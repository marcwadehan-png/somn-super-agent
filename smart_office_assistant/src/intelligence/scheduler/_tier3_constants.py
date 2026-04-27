# -*- coding: utf-8 -*-
"""
三级神经网络调度器 - 常量定义模块
Tier-3 Neural Scheduler Constants
=================================

包含所有配置常量:
- TIER_CLASSIFICATION: 引擎三级分类
- P1_CANDIDATES / P3_CANDIDATES / P2_CANDIDATES: 各层引擎候选池
- DOMAIN_ENGINE_KEYWORDS: 中文关键词 → 引擎ID mapping
- DOMAIN_KEYWORD_TO_ENG: 中文关键词 → 英文引擎域 mapping

版本: v1.0
日期: 2026-04-06
"""

from typing import Dict, List

# ==================== 引擎三级分类 ====================
# P1: 核心strategy引擎 - 直接产出战略建议,decision方案
# P2: 交叉验证引擎 - 多元视角,补充,反方观点
# P3: 论证可行性引擎 - 验证,证明,论据支撑

TIER_CLASSIFICATION = {
    # ---- P1: 核心strategy引擎 (6个基准 + 按域扩展) ----
    # 直接产出战略/decision/方案
    "SUFU": {"tier": "P1", "weight": 1.0, "domains": ["leadership", "risk", "strategy", "ethics", "personnel"]},
    "MILITARY": {"tier": "P1", "weight": 1.0, "domains": ["competition", "strategy", "war", "negotiation", "marketing"]},
    "STRATEGY": {"tier": "P1", "weight": 1.0, "domains": ["business_strategy", "competitive_advantage", "corporate_strategy"]},
    "SOCIAL_SCIENCE": {"tier": "P1", "weight": 0.95, "domains": ["marketing", "economics", "growth", "business", "competitive_strategy"]},
    "CREATIVITY": {"tier": "P1", "weight": 0.95, "domains": ["creative_problem", "innovation", "cross_domain", "design_thinking"]},
    "ANCIENT_WISDOM_FUSION": {"tier": "P1", "weight": 0.9, "domains": ["ethics", "governance", "strategy", "crisis", "culture", "talent"]},

    # ---- P3: 论证可行性引擎 (4个基准 + 按域扩展) ----
    # 验证/论证P1strategy的可行性
    "CIVILIZATION": {"tier": "P3", "weight": 1.0, "domains": ["civilization", "history", "strategy", "institutional", "cultural_change"]},
    "CIV_WAR_ECONOMY": {"tier": "P3", "weight": 1.0, "domains": ["war_economy", "state_capacity", "risk", "civilization", "competition"]},
    "SCIENTIFIC_AD_VERIFICATION": {"tier": "P3", "weight": 0.9, "domains": ["evidence", "verification", "scientific_method", "analysis"]},
    "CONSULTING_VALIDATOR": {"tier": "P3", "weight": 0.85, "domains": ["consulting", "validation", "feasibility", "business"]},
    "DECISION": {"tier": "P3", "weight": 0.85, "domains": ["decision_making", "cognitive_bias", "risk_perception"]},
    "CRITICAL": {"tier": "P3", "weight": 0.8, "domains": ["critical_analysis", "logical_fallacy", "evidence_evaluation", "reflection"]},

    # ---- P2: 交叉验证引擎 (4个基准 + 按域扩展) ----
    # 多元视角,补充,反方观点
    "PSYCHOLOGY": {"tier": "P2", "weight": 1.0, "domains": ["deep_psychology", "motivation", "personality", "unconscious"]},
    "MARKETING": {"tier": "P2", "weight": 0.95, "domains": ["consumer_psychology", "persuasion", "brand_narrative", "user_experience"]},
    "SYSTEMS": {"tier": "P2", "weight": 0.9, "domains": ["system_dynamics", "feedback_loops", "emergence", "leverage"]},
    "LITERARY": {"tier": "P2", "weight": 0.9, "domains": ["narrative", "resilience", "character", "human_insight"]},
    "ANTHROPOLOGY": {"tier": "P2", "weight": 0.85, "domains": ["cross_culture", "ritual", "cultural_change", "social_structure"]},
    "METAPHYSICS": {"tier": "P2", "weight": 0.8, "domains": ["timing", "environment", "balance", "yin_yang", "fortune"]},
    "REASONING": {"tier": "P2", "weight": 0.8, "domains": ["reasoning", "causal_inference", "counterfactual", "analogical"]},
}

# 所有P1候选引擎(可按域扩展)
P1_CANDIDATES = {
    # 战略decision核心
    "SUFU": {"weight": 1.0, "domains": ["leadership", "risk", "strategy", "ethics", "personnel", "decision"]},
    "MILITARY": {"weight": 1.0, "domains": ["competition", "strategy", "war", "negotiation", "marketing", "attack", "defense"]},
    "STRATEGY": {"weight": 1.0, "domains": ["business_strategy", "competitive_advantage", "corporate_strategy", "transformation"]},
    "CONFUCIAN": {"weight": 0.9, "domains": ["ethics", "governance", "talent", "culture", "order", "harmony"]},
    "LVSHI": {"weight": 0.9, "domains": ["public_interest", "seasonal", "governance", "fairness"]},
    "YANGMING": {"weight": 0.9, "domains": ["inner_growth", "ethics", "action", "wisdom", "self_cultivation"]},
    "DAOIST": {"weight": 0.85, "domains": ["strategy", "crisis", "change", "balance", "timing", "natural"]},
    "GROWTH": {"weight": 0.85, "domains": ["growth_mindset", "iteration", "breakthrough", "learning", "improvement"]},
    "SCI_FI": {"weight": 0.8, "domains": ["dimension", "survival", "scale", "disruption", "breakthrough"]},
    "SOCIAL_SCIENCE": {"weight": 0.95, "domains": ["marketing", "economics", "growth", "business", "STP", "4P", "competitive_strategy"]},
    "POSITIONING": {"weight": 0.9, "domains": ["positioning", "competitive_cognition", "brand_differentiation", "market_mind"]},
    "BEHAVIOR": {"weight": 0.85, "domains": ["habit", "willpower", "nudge", "behavior_change", "self_management"]},
    "CREATIVITY": {"weight": 0.9, "domains": ["creative_problem", "innovation", "cross_domain", "design_thinking", "brainstorm"]},
    "ANCIENT_WISDOM_FUSION": {"weight": 0.9, "domains": ["ethics", "governance", "strategy", "crisis", "culture", "talent", "growth"]},
    "SUPREME_WISDOM_COORDINATOR": {"weight": 0.85, "domains": ["general", "complex", "multi_domain", "integration"]},
    "ENTERPRISE_STRATEGY": {"weight": 0.9, "domains": ["business_strategy", "competitive_advantage", "corporate_strategy"]},
    "EASTERN_BUSINESS": {"weight": 0.8, "domains": ["chinese_management", "relationship", "long_term", "family_business"]},
    "WESTERN_MGMT": {"weight": 0.8, "domains": ["management", "performance_measurement", "organizational_design", "Daqin_Metrics", "KPI"]},
    "COMPLEXITY": {"weight": 0.8, "domains": ["complex_systems", "emergence", "self_organization", "adaptation", "chaos"]},
    "EVOLUTION": {"weight": 0.8, "domains": ["evolutionary_dynamics", "adaptation", "competition", "cooperation"]},
    "GAME_THEORY": {"weight": 0.85, "domains": ["strategic_interaction", "competitive_strategy", "negotiation", "contract_design"]},
    "FINANCE": {"weight": 0.8, "domains": ["financial_analysis", "investment_decision", "valuation", "capital_structure"]},
    "OPERATIONS": {"weight": 0.8, "domains": ["operations_efficiency", "process_optimization", "supply_chain", "quality"]},
    
    # v9.0.0 WCC智慧演化 - 元视角战略思考
    "WCC": {"weight": 0.85, "domains": ["meta_perspective", "scale_transformation", "wisdom_evolution", "tech_evolution", "civilization_stages"]},
}

# 所有P3候选引擎
P3_CANDIDATES = {
    # 论证/验证/可行性评估
    "CIVILIZATION": {"weight": 1.0, "domains": ["civilization", "history", "strategy", "institutional", "cultural_change"]},
    "CIV_WAR_ECONOMY": {"weight": 1.0, "domains": ["war_economy", "state_capacity", "risk", "civilization", "competition", "mobilization"]},
    "HONGMING": {"weight": 0.9, "domains": ["cross_culture", "ethical", "culture", "moral_civilization", "chinese_spirit"]},
    "SCIENTIFIC_AD_VERIFICATION": {"weight": 0.9, "domains": ["evidence", "verification", "scientific_method", "analysis", "proof"]},
    "CONSULTING_VALIDATOR": {"weight": 0.85, "domains": ["consulting", "validation", "feasibility", "business", "risk_assessment"]},
    "DECISION": {"weight": 0.85, "domains": ["decision_making", "cognitive_bias", "risk_perception", "bounded_rationality"]},
    "CRITICAL": {"weight": 0.85, "domains": ["critical_analysis", "logical_fallacy", "evidence_evaluation", "reflection", "question"]},
    "SCIENCE": {"weight": 0.85, "domains": ["scientific_method", "evidence", "hypothesis", "system_thinking", "analysis"]},
    "LOGIC": {"weight": 0.8, "domains": ["logical_reasoning", "deduction", "induction", "proof", "consistency"]},
    "NATURAL_SCIENCE": {"weight": 0.8, "domains": ["physics", "chemistry", "biology", "earth", "cosmos", "cross_scale"]},
    "WISDOM_REASONING": {"weight": 0.85, "domains": ["reasoning", "wisdom_chain", "integration", "reflection"]},
    "CLOSED_LOOP_SYSTEM": {"weight": 0.8, "domains": ["closed_loop", "feedback", "iteration", "verification", "improvement"]},
    "MATH": {"weight": 0.8, "domains": ["probability", "game_theory", "optimization", "pattern_recognition", "statistics"]},
    
    # v9.0.0 WCC智慧演化 - 长期演化视角分析
    "WCC": {"weight": 0.9, "domains": ["meta_perspective", "civilization_analysis", "cosmic_cognition", "scale_transformation", "worldview_shift", "wisdom_evolution", "tech_evolution"]},
}

# 所有P2候选引擎
P2_CANDIDATES = {
    # 交叉验证/多元视角/补充
    "PSYCHOLOGY": {"weight": 1.0, "domains": ["deep_psychology", "motivation", "personality", "unconscious", "Freud", "Jung", "Maslow"]},
    "MARKETING": {"weight": 0.95, "domains": ["consumer_psychology", "persuasion", "brand_narrative", "user_experience", "subconscious"]},
    "SYSTEMS": {"weight": 0.9, "domains": ["system_dynamics", "feedback_loops", "emergence", "leverage", "nonlinear"]},
    "LITERARY": {"weight": 0.9, "domains": ["narrative", "resilience", "character", "human_insight", "fate", "struggle"]},
    "ANTHROPOLOGY": {"weight": 0.9, "domains": ["cross_culture", "ritual", "cultural_change", "social_structure", "relative"]},
    "BUDDHIST": {"weight": 0.85, "domains": ["mindset", "harmony", "spiritual", "letting_go", "karma", "emptiness"]},
    "DAOIST": {"weight": 0.85, "domains": ["strategy", "crisis", "change", "balance", "natural", "wuwei", "yin_yang"]},
    "METAPHYSICS": {"weight": 0.8, "domains": ["timing", "environment", "balance", "yin_yang", "fortune", "five_elements"]},
    "REASONING": {"weight": 0.8, "domains": ["reasoning", "causal_inference", "counterfactual", "analogical", "abduction"]},
    "MYTHOLOGY": {"weight": 0.8, "domains": ["creation_myth", "apocalypse", "cyclical", "archetype", "hero", "fate"]},
    "NEURO": {"weight": 0.8, "domains": ["neural_learning", "synaptic_plasticity", "neural_dynamics", "cognition"]},
    "CROSS_WISDOM_ANALYZER": {"weight": 0.85, "domains": ["cross_axis", "multi_perspective", "comparison", "synthesis"]},
    "POETRY": {"weight": 0.75, "domains": ["aesthetics", "expression", "metaphor", "cultural_literacy", "imagery"]},
    "SCIENCE_THINKING": {"weight": 0.8, "domains": ["scientific_method", "evidence", "system_thinking", "concept_transfer"]},
    "SUB_CONSCIOUS_DEMAND": {"weight": 0.8, "domains": ["subconscious", "latent_demand", "hidden_motivation", "unconscious"]},
    "MINGFEN_ORDER": {"weight": 0.75, "domains": ["role", "order", "responsibility", "social_structure", "hierarchy"]},
    "GENTLE_CONDUCT": {"weight": 0.75, "domains": ["conduct", "gentle", "moral", "character", "integrity"]},
    "BEHAVIOR": {"weight": 0.8, "domains": ["habit", "willpower", "nudge", "behavior_change", "self_management"]},
    "MORAL_ETHICS": {"weight": 0.8, "domains": ["ethics", "morality", "virtue", "conscience", "right_wrong"]},
    "LITERARY_NARRATIVE": {"weight": 0.8, "domains": ["narrative", "story", "character", "growth", "resilience", "truth"]},
}

# 问题域关键词 → 引擎ID 的mapping
DOMAIN_ENGINE_KEYWORDS: Dict[str, List[str]] = {
    # 战略/竞争
    "战略": ["MILITARY", "SUFU", "STRATEGY", "CIVILIZATION", "CIV_WAR_ECONOMY"],
    "竞争": ["MILITARY", "POSITIONING", "SOCIAL_SCIENCE", "GAME_THEORY"],
    "decision": ["SUFU", "DECISION", "STRATEGY", "MILITARY", "CRITICAL"],
    "规划": ["STRATEGY", "CONFUCIAN", "GROWTH", "COMPLEXITY"],
    "商业": ["STRATEGY", "SOCIAL_SCIENCE", "FINANCE", "OPERATIONS"],
    # 伦理/文化
    "伦理": ["CONFUCIAN", "HONGMING", "MORAL_ETHICS", "YANGMING"],
    "道德": ["CONFUCIAN", "SUFU", "MORAL_ETHICS", "HONGMING"],
    "文化": ["ANTHROPOLOGY", "LITERARY", "MYTHOLOGY", "CIVILIZATION", "HONGMING"],
    "传统": ["CONFUCIAN", "DAOIST", "BUDDHIST", "ANCIENT_WISDOM_FUSION"],
    # 心理/行为
    "心理": ["PSYCHOLOGY", "MARKETING", "SUB_CONSCIOUS_DEMAND", "BEHAVIOR"],
    "心态": ["YANGMING", "BUDDHIST", "DAOIST", "GROWTH", "PSYCHOLOGY"],
    "情绪": ["BUDDHIST", "PSYCHOLOGY", "BEHAVIOR", "DAOIST"],
    "习惯": ["BEHAVIOR", "GROWTH", "CLOSED_LOOP_SYSTEM", "PSYCHOLOGY"],
    "成长": ["GROWTH", "YANGMING", "SCI_FI", "BEHAVIOR", "EVOLUTION"],
    # 市场/营销
    "营销": ["SOCIAL_SCIENCE", "MARKETING", "POSITIONING", "BEHAVIOR"],
    "品牌": ["MARKETING", "POSITIONING", "LITERARY", "OGILVY_NARRATIVE"],
    "用户": ["MARKETING", "ANTHROPOLOGY", "BEHAVIOR", "PSYCHOLOGY"],
    "增长": ["SOCIAL_SCIENCE", "GROWTH", "FINANCE", "OPERATIONS", "CREATIVITY"],
    # 危机/风险
    "危机": ["MILITARY", "SUFU", "DAOIST", "CIVILIZATION", "CIV_WAR_ECONOMY"],
    "风险": ["SUFU", "CIV_WAR_ECONOMY", "CONSULTING_VALIDATOR", "CRITICAL", "DECISION"],
    "生死": ["MILITARY", "CIVILIZATION", "CIV_WAR_ECONOMY", "COMPLEXITY"],
    # 危机/风险 - 商业危机扩展
    "亏损": ["MILITARY", "SUFU", "CIV_WAR_ECONOMY", "FINANCE", "OPERATIONS"],
    "现金流": ["FINANCE", "OPERATIONS", "CIV_WAR_ECONOMY", "CONSULTING_VALIDATOR"],
    "士气": ["PSYCHOLOGY", "BEHAVIOR", "YANGMING", "CONFUCIAN", "BUDDHIST"],
    "绝地反击": ["MILITARY", "SUFU", "SCI_FI", "CIV_WAR_ECONOMY", "COMPLEXITY", "GAME_THEORY"],
    "翻盘": ["MILITARY", "GAME_THEORY", "SCI_FI", "COMPLEXITY", "STRATEGY"],
    "客户流失": ["MARKETING", "POSITIONING", "BEHAVIOR", "PSYCHOLOGY"],
    "竞对": ["MILITARY", "POSITIONING", "GAME_THEORY", "SOCIAL_SCIENCE", "STRATEGY"],
    # 自然/科学
    "科学": ["SCIENCE", "NATURAL_SCIENCE", "SCIENTIFIC_AD_VERIFICATION", "LOGIC"],
    "自然": ["NATURAL_SCIENCE", "DAOIST", "METAPHYSICS", "COMPLEXITY"],
    "数学": ["MATH", "GAME_THEORY", "LOGIC", "FINANCE"],
    # 团队/管理
    "团队": ["CONFUCIAN", "HONGMING", "BEHAVIOR", "OPERATIONS"],
    "管理": ["WESTERN_MGMT", "CONFUCIAN", "STRATEGY", "OPERATIONS", "BEHAVIOR"],
    "人才": ["SUFU", "CONFUCIAN", "HONGMING", "WISDOM_TALENT_ASSESSOR"],
    # 创新/思维
    "创新": ["CREATIVITY", "SCI_FI", "GROWTH", "COMPLEXITY"],
    "思维": ["CRITICAL", "REASONING", "SYSTEMS", "DEWEY_THINKING", "TOP_THINKING"],
    "逻辑": ["LOGIC", "CRITICAL", "REASONING", "SCIENCE"],
    # 跨文化/沟通
    "跨文化": ["ANTHROPOLOGY", "HONGMING", "CROSS_WISDOM_ANALYZER"],
    "沟通": ["HONGMING", "LITERARY", "MARKETING", "ANTHROPOLOGY"],
    # 宇宙/宏观
    "文明": ["CIVILIZATION", "CIV_WAR_ECONOMY", "MYTHOLOGY", "COMPLEXITY", "EVOLUTION"],
    "演化": ["CIVILIZATION", "EVOLUTION", "COMPLEXITY", "GROWTH"],
    "宇宙": ["NATURAL_SCIENCE", "SCI_FI", "MYTHOLOGY", "METAPHYSICS"],
    # 经营/效率
    "经营": ["STRATEGY", "OPERATIONS", "FINANCE", "EASTERN_BUSINESS"],
    "效率": ["OPERATIONS", "BEHAVIOR", "SYSTEMS", "WESTERN_MGMT"],
    "成本": ["OPERATIONS", "FINANCE", "CIV_WAR_ECONOMY"],
    # 定位/差异化
    "定位": ["POSITIONING", "MARKETING", "MILITARY", "ANTHROPOLOGY"],
    "品类": ["POSITIONING", "MARKETING", "SOCIAL_SCIENCE"],
    # 人性/洞察
    "人性": ["LITERARY", "PSYCHOLOGY", "BUDDHIST", "MYTHOLOGY"],
    "命运": ["MYTHOLOGY", "LITERARY", "BUDDHIST", "METAPHYSICS"],
    "苦难": ["LITERARY", "BUDDHIST", "GROWTH", "MYTHOLOGY"],
    # 心性/修行
    "心性": ["YANGMING", "BUDDHIST", "DAOIST", "SUFU"],
    "修行": ["BUDDHIST", "DAOIST", "YANGMING", "SUFU"],
    "致良知": ["YANGMING", "CONFUCIAN", "SUFU"],
    "知行合一": ["YANGMING", "GROWTH", "BEHAVIOR"],
    # 博弈
    "博弈": ["GAME_THEORY", "MILITARY", "CIV_WAR_ECONOMY", "MATH"],
    "纳什": ["GAME_THEORY", "MATH", "COMPLEXITY"],
    # 复杂系统
    "复杂": ["COMPLEXITY", "SYSTEMS", "COMPLEXITY", "SCIENCE"],
    "涌现": ["COMPLEXITY", "SYSTEMS", "NEURO", "EVOLUTION"],
    # 诗词/意境
    "诗词": ["POETRY", "LITERARY", "DAOIST", "CONFUCIAN"],
    "意境": ["POETRY", "DAOIST", "LITERARY", "METAPHYSICS"],
}

# ============================================================
# 中文关键词 → 英文引擎域关键词mapping(覆盖率提升核心)
# 覆盖 extract_domains() 返回的所有中文关键词 + 语义标签
# ============================================================
DOMAIN_KEYWORD_TO_ENG: Dict[str, List[str]] = {
    # === 战略/竞争/博弈 ===
    "战略":     ["strategy", "strategic", "business_strategy", "corporate_strategy",
                "competitive_strategy", "strategic_interaction"],
    "strategy":     ["strategy", "decision", "game_theory", "competitive_strategy", "strategic_interaction"],
    "规划":     ["strategy", "business", "growth", "long_term", "corporate_strategy"],
    "博弈":     ["game_theory", "strategic_interaction", "competition", "negotiation", "war", "cooperation"],
    "纳什":     ["game_theory", "equilibrium", "decision"],
    "竞争":     ["competition", "competitive_advantage", "competitive_strategy", "competitive_cognition", "war"],
    "竞对":     ["competition", "competitive_strategy", "positioning", "war"],
    "对抗":     ["war", "competition", "attack", "defense", "game_theory"],
    # === 危机/风险/生存 ===
    "危机":     ["crisis", "risk", "disruption", "survival", "dimension", "war_economy", "state_capacity"],
    "风险":     ["risk", "risk_assessment", "risk_perception", "uncertainty", "probability", "war_economy"],
    "生死":     ["survival", "war", "crisis", "state_capacity", "resilience"],
    "困境":     ["crisis", "survival", "struggle", "resilience", "adaptation"],
    "亏损":     ["financial_analysis", "risk", "operations_efficiency", "capital_structure", "valuation"],
    "现金流":   ["financial_analysis", "capital_structure", "investment_decision", "valuation", "supply_chain"],
    "绝地反击": ["survival", "crisis", "war", "disruption", "resilience", "breakthrough", "transformation"],
    "翻盘":     ["survival", "resilience", "breakthrough", "transformation", "competitive_advantage"],
    "客户流失": ["marketing", "positioning", "brand_differentiation", "consumer_psychology", "latent_demand"],
    "竞品":     ["competition", "competitive_strategy", "positioning", "market_mind"],
    "对手":     ["competition", "competitive_strategy", "war", "game_theory"],
    # === 伦理/道德/人性 ===
    "伦理":     ["ethics", "ethical", "morality", "virtue", "conscience", "right_wrong"],
    "道德":     ["moral", "morality", "ethics", "virtue", "conscience", "public_interest"],
    "人性":     ["psychology", "deep_psychology", "human_insight", "motivation", "personality", "neural_dynamics"],
    "善":       ["ethics", "virtue", "morality", "conscience", "fairness"],
    "恶":       ["ethics", "moral", "conscience", "fairness", "strategic_interaction"],
    "苦难":     ["struggle", "resilience", "hero", "narrative", "truth", "karma"],
    "命运":     ["fate", "chaos", "cosmos", "truth", "character"],
    # === 心理/行为/成长 ===
    "心理":     ["psychology", "consumer_psychology", "deep_psychology", "motivation", "cognitive_bias", "neural_dynamics"],
    "心态":     ["mindset", "growth_mindset", "psychology", "motivation", "self_management", "willpower"],
    "情绪":     ["psychology", "neural_dynamics", "motivation", "willpower", "resilience"],
    "成长":     ["growth", "growth_mindset", "improvement", "breakthrough", "learning", "iteration", "inner_growth"],
    "习惯":     ["habit", "behavior_change", "nudge", "willpower", "self_management"],
    "意志":     ["willpower", "will", "motivation", "self_management", "growth"],
    "突破":     ["breakthrough", "innovation", "growth", "transformation", "creative_problem"],
    # === 市场/营销/品牌 ===
    "营销":     ["marketing", "STP", "4P", "brand", "consumer_psychology", "market_mind", "latent_demand"],
    "品牌":     ["brand", "brand_differentiation", "brand_narrative", "positioning", "story", "narrative"],
    "用户":     ["consumer_psychology", "user_experience", "market_mind", "latent_demand", "behavior_change"],
    "增长":     ["growth", "business_strategy", "iteration", "optimization", "market_mind", "innovation"],
    "定位":     ["positioning", "brand_differentiation", "STP", "competitive_advantage", "market_mind"],
    "品类":     ["positioning", "STP", "market_mind", "brand_differentiation"],
    "市场":     ["market_mind", "marketing", "business", "STP", "competition"],
    # === 团队/管理/人才 ===
    "团队":     ["team", "leadership", "organizational_design", "personnel", "hierarchy", "management", "governance"],
    "管理":     ["management", "leadership", "organizational_design", "team", "performance_measurement", "OKR", "KPI"],
    "人才":     ["talent", "personnel", "leadership", "organizational_design", "self_cultivation"],
    "组织":     ["organizational_design", "team", "management", "institutional", "social_structure", "hierarchy"],
    "制度":     ["institutional", "organizational_design", "hierarchy", "governance", "performance_measurement"],
    "激励":     ["motivation", "willpower", "nudge", "behavior_change", "leadership"],
    # === 创新/思维/逻辑 ===
    "创新":     ["innovation", "creative_problem", "design_thinking", "growth", "transformation", "breakthrough"],
    "思维":     ["critical_analysis", "system_thinking", "logical_reasoning", "cognition", "pattern_recognition"],
    "逻辑":     ["logical_reasoning", "deduction", "induction", "proof", "evidence", "abduction", "logical_fallacy"],
    "推理":     ["reasoning", "logical_reasoning", "causal_inference", "counterfactual", "abduction"],
    "分析":     ["analysis", "comparison", "pattern_recognition", "evidence", "hypothesis", "evidence_evaluation"],
    "批判":     ["critical_analysis", "evidence_evaluation", "logical_fallacy", "question", "verification"],
    "复杂":     ["complex_systems", "complex", "emergence", "feedback_loops", "nonlinear", "system_dynamics"],
    "涌现":     ["emergence", "complex_systems", "self_organization", "evolutionary_dynamics", "neural_dynamics"],
    # === 跨文化/沟通 ===
    "跨文化":   ["cross_culture", "cultural_literacy", "negotiation", "comparison", "cultural_change"],
    "沟通":     ["negotiation", "persuasion", "cross_culture", "relationship", "narrative"],
    "文化":     ["culture", "cultural_literacy", "narrative", "ritual", "cross_culture", "chinese_management"],
    "传统":     ["culture", "tradition", "ritual", "cultural_literacy", "wisdom", "history"],
    # === 宇宙/宏观/文明 ===
    "文明":     ["civilization", "history", "cyclical", "state_capacity", "war_economy", "cultural_literacy"],
    "演化":     ["evolutionary_dynamics", "growth", "adaptation", "change", "emergence", "complex_systems"],
    "宇宙":     ["cosmos", "natural", "earth", "physics", "cross_axis", "apocalypse"],
    "宏观":     ["system_dynamics", "civilization", "history", "cyclical", "state_capacity"],
    "周期":     ["cyclical", "seasonal", "war_economy", "civilization", "history"],
    "兴衰":     ["civilization", "state_capacity", "war_economy", "cyclical", "evolutionary_dynamics"],
    # === 经营/效率/财务 ===
    "经营":     ["business_strategy", "management", "growth", "operations_efficiency", "financial_analysis"],
    "效率":     ["operations_efficiency", "process_optimization", "optimization", "performance_measurement", "quality"],
    "成本":     ["financial_analysis", "operations_efficiency", "capital_structure", "investment_decision"],
    "财务":     ["financial_analysis", "valuation", "capital_structure", "investment_decision", "risk"],
    # === 心性/修行/哲学 ===
    "心性":     ["wisdom", "self_cultivation", "conscience", "inner_growth", "psychology", "mindset"],
    "修行":     ["self_cultivation", "inner_growth", "wisdom", "karma", "emptiness", "wuwei"],
    "致良知":   ["conscience", "wisdom", "right_wrong", "morality", "integrity"],
    "知行合一": ["wisdom_chain", "integration", "action", "learning", "self_cultivation"],
    "中庸":     ["balance", "harmony", "yin_yang", "integration"],
    "无为":     ["wuwei", "natural", "harmony", "letting_go", "balance"],
    "道法自然": ["natural", "wuwei", "harmony", "cosmos", "yin_yang"],
    # === 诗词/意境/文学 ===
    "诗词":     ["poetry", "aesthetics", "imagery", "expression", "metaphor"],
    "意境":     ["aesthetics", "imagery", "metaphor", "poetry", "harmony"],
    "文学":     ["narrative", "story", "character", "literary_narrative"],
    "叙事":     ["narrative", "story", "character", "metaphor", "hero"],
    # === 神经/认知/科学 ===
    "神经":     ["neural_dynamics", "neural_learning", "synaptic_plasticity", "cognition", "brain"],
    "认知":     ["cognition", "pattern_recognition", "psychology", "neural_dynamics", "decision_making"],
    "decision":     ["decision", "decision_making", "bounded_rationality", "game_theory", "strategic_interaction"],
    "科学":     ["scientific_method", "evidence", "physics", "chemistry", "biology", "cross_scale", "hypothesis"],
    "自然":     ["natural", "physics", "chemistry", "biology", "earth", "cosmos", "cross_scale"],
    "数学":     ["optimization", "probability", "statistics", "game_theory", "risk_assessment"],
    # === 商业/咨询 ===
    "商业":     ["business_strategy", "business", "market_mind", "operations_efficiency"],
    "咨询":     ["consulting", "evidence_evaluation", "hypothesis", "validation"],
    # === 资源/供应链 ===
    "资源":     ["supply_chain", "investment_decision", "capital_structure", "operations_efficiency", "state_capacity"],
    "供应链":   ["supply_chain", "operations_efficiency", "risk", "investment_decision"],
    # === 谈判/外交 ===
    "谈判":     ["negotiation", "strategic_interaction", "persuasion", "competitive_cognition", "game_theory"],
    "外交":     ["strategic_interaction", "cooperation", "negotiation", "war", "cross_culture"],
    # ============================================
    # 语义标签 → 英文域(10大标签全覆盖)
    # ============================================
    "战略相关": ["strategy", "strategic", "business_strategy", "competitive_advantage", "corporate_strategy"],
    "危机相关": ["risk", "crisis", "war", "competition", "war_economy", "survival", "disruption", "dimension", "state_capacity"],
    "伦理相关": ["ethics", "moral", "virtue", "conscience", "right_wrong", "ethical", "morality"],
    "人心相关": ["psychology", "deep_psychology", "motivation", "personality", "consumer_psychology", "subconscious", "neural_dynamics"],
    "成长相关": ["growth", "growth_mindset", "learning", "improvement", "breakthrough", "iteration", "self_cultivation"],
    "文化相关": ["cultural_literacy", "culture", "tradition", "cross_culture", "narrative", "chinese_management"],
    "自然相关": ["physics", "chemistry", "biology", "scientific_method", "natural", "cosmos", "cross_scale", "earth"],
    "市场相关": ["marketing", "market_mind", "STP", "4P", "brand", "consumer_psychology", "user_experience"],
    "竞争相关": ["competitive", "competition", "competitive_strategy", "game_theory", "war", "negotiation", "strategic_interaction"],
    "管理相关": ["management", "organizational_design", "team", "performance_measurement", "leadership", "OKR", "KPI"],
}

# 中文语义标签 → 英文引擎域关键词mapping (供内部使用)
SEMANTIC_TO_ENG_DOMAINS: Dict[str, List[str]] = {
    "战略相关": ["strategy", "strategic", "business_strategy", "competitive_advantage",
                "corporate_strategy", "competitive_strategy"],
    "危机相关": ["risk", "crisis", "war", "competition", "war_economy", "survival",
                "crisis_management", "dimension", "disruption"],
    "伦理相关": ["ethics", "moral", "virtue", "conscience", "right_wrong", "ethical"],
    "人心相关": ["psychology", "deep_psychology", "motivation", "personality",
               "consumer_psychology", "subconscious", "neural"],
    "成长相关": ["growth", "growth_mindset", "learning", "improvement", "breakthrough",
                "iteration", "self_cultivation", "inner_growth"],
    "文化相关": ["cultural", "culture", "tradition", "cross_culture", "narrative",
               "chinese_management", "chinese_spirit"],
    "自然相关": ["physics", "chemistry", "biology", "scientific_method", "natural",
               "cosmos", "cross_scale"],
    "市场相关": ["marketing", "market", "STP", "4P", "brand", "consumer", "user_experience"],
    "竞争相关": ["competitive", "competition", "competitive_strategy", "game_theory",
                "博弈", "war", "negotiation", "strategic_interaction"],
    "管理相关": ["management", "organizational", "team", "performance", "leadership",
               "Daqin_Metrics", "KPI", "personnel", "talent"],
}
