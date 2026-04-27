# -*- coding: utf-8 -*-
"""
神之架构 - 部门调度矩阵数据 v1.0
_dispatch_matrix_data.py

跨部门能力调用矩阵数据
格式: ProblemType → List[(Department, DepartmentRole, List[Tuple[WisdomSchool, float]])]

使用字符串存储枚举名称，主模块负责转换

版本: v1.0.0 | 2026-04-24
"""

from typing import Dict, List, Tuple, Any

# 缓存已加载的枚举
_enums_loaded = False
_enum_map: Dict[str, Any] = {}


def _load_enums():
    """加载枚举到缓存"""
    global _enums_loaded, _enum_map
    if not _enums_loaded:
        from ._dispatch_enums import WisdomSchool, ProblemType
        from ._dispatch_court import Department, DepartmentRole
        _enum_map = {
            'Department': Department,
            'DepartmentRole': DepartmentRole,
            'WisdomSchool': WisdomSchool,
            'ProblemType': ProblemType,
        }
        _enums_loaded = True


def get_matrix_data() -> Dict:
    """
    获取 DEPARTMENT_SCHOOL_MATRIX 数据。
    首次调用时加载枚举并构建数据。
    """
    _load_enums()

    D = _enum_map['Department']
    DR = _enum_map['DepartmentRole']
    WS = _enum_map['WisdomSchool']
    PT = _enum_map['ProblemType']

    return {
        # ── 兵部（调度层）场景 ──
        PT.COMPETITION: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.MILITARY, 0.9), (WS.DAOIST, 0.5), (WS.SUFU, 0.4)]),
        ],
        PT.CRISIS: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.DAOIST, 0.9), (WS.MILITARY, 0.5), (WS.BUDDHIST, 0.4)]),
        ],
        PT.ATTACK: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.MILITARY, 0.9), (WS.DAOIST, 0.4), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.DEFENSE: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.MILITARY, 0.85), (WS.DAOIST, 0.6), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.NEGOTIATION: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.MILITARY, 0.7), (WS.DAOIST, 0.6), (WS.BUDDHIST, 0.5)]),
        ],
        PT.WAR_ECONOMY_NEXUS: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.MILITARY, 0.88), (WS.CONFUCIAN, 0.55), (WS.LVSHI, 0.4)]),
        ],

        # ── 户部（数据层）场景 ──
        PT.MARKET_ANALYSIS: [
            (D.HUBU, DR.PRIMARY,
             [(WS.SOCIAL_SCIENCE, 0.9), (WS.SCIENCE, 0.4), (WS.MILITARY, 0.3)]),
        ],
        PT.MARKETING: [
            (D.HUBU, DR.PRIMARY,
             [(WS.CHINESE_CONSUMER, 0.95), (WS.BEHAVIOR, 0.85),
              (WS.SOCIAL_SCIENCE, 0.8), (WS.LITERARY, 0.6),
              (WS.DAOIST, 0.4)]),
        ],
        PT.CONSUMER_MARKETING: [
            (D.HUBU, DR.PRIMARY,
             [(WS.CHINESE_CONSUMER, 0.95), (WS.BEHAVIOR, 0.9),
              (WS.SOCIAL_SCIENCE, 0.7), (WS.LITERARY, 0.5)]),
            (D.GONGBU, DR.SECONDARY,
             [(WS.GROWTH, 0.8), (WS.SUFU, 0.5)]),
        ],
        PT.BRAND_STRATEGY: [
            (D.HUBU, DR.PRIMARY,
             [(WS.CHINESE_CONSUMER, 0.9), (WS.LITERARY, 0.8),
              (WS.BEHAVIOR, 0.7), (WS.CONFUCIAN, 0.5)]),
        ],
        PT.SOCIAL_STABILITY: [
            (D.HUBU, DR.PRIMARY,
             [(WS.SOCIAL_SCIENCE, 0.9), (WS.CONFUCIAN, 0.7),
              (WS.DAOIST, 0.5), (WS.LVSHI, 0.4)]),
            (D.HANLIN, DR.SECONDARY,
             [(WS.BEHAVIOR, 0.8), (WS.MILITARY, 0.6)]),
        ],
        PT.PSYCHOLOGICAL_INSIGHT: [
            (D.HUBU, DR.PRIMARY,
             [(WS.BEHAVIOR, 0.95), (WS.CHINESE_CONSUMER, 0.8),
              (WS.SOCIAL_SCIENCE, 0.6), (WS.DAOIST, 0.4)]),
        ],
        PT.SOCIAL_DEVELOPMENT: [
            (D.HUBU, DR.PRIMARY,
             [(WS.SOCIAL_SCIENCE, 0.9), (WS.ANTHROPOLOGY, 0.6), (WS.CIVILIZATION, 0.4)]),
        ],
        PT.SEASONAL: [
            (D.HUBU, DR.PRIMARY,
             [(WS.LVSHI, 0.85), (WS.DAOIST, 0.5), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.FORTUNE: [
            (D.HUBU, DR.PRIMARY,
             [(WS.SUFU, 0.9), (WS.DAOIST, 0.5), (WS.BUDDHIST, 0.3)]),
        ],

        # ── 礼部（记忆层）场景 ──
        PT.GROWTH_MINDSET: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.GROWTH, 0.9), (WS.CONFUCIAN, 0.4), (WS.SUFU, 0.3)]),
        ],
        PT.LONGTERM: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.BUDDHIST, 0.85), (WS.CONFUCIAN, 0.5), (WS.DAOIST, 0.5)]),
        ],
        PT.NARRATIVE: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.LITERARY, 0.9), (WS.CONFUCIAN, 0.4), (WS.DAOIST, 0.3)]),
        ],
        PT.CHARACTER: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.LITERARY, 0.9), (WS.CONFUCIAN, 0.4), (WS.BUDDHIST, 0.3)]),
        ],
        PT.CROSS_CULTURE: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.ANTHROPOLOGY, 0.9), (WS.HONGMING, 0.5), (WS.CONFUCIAN, 0.4)]),
        ],

        # ── 工部（执行层）场景 ──
        PT.CLOSED_LOOP: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.GROWTH, 0.9), (WS.SUFU, 0.5), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.SCIENTIFIC_METHOD: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.SCIENCE, 0.9), (WS.MILITARY, 0.4), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.SYSTEM_THINKING: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.SCIENCE, 0.9), (WS.DAOIST, 0.6), (WS.METAPHYSICS, 0.4)]),
            (D.BINGBU, DR.SECONDARY,
             [(WS.TOP_METHODS, 0.9), (WS.GROWTH, 0.5)]),
        ],
        PT.NUDGE: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.BEHAVIOR, 0.9), (WS.DAOIST, 0.5), (WS.MILITARY, 0.3)]),
        ],
        PT.HABIT: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.BEHAVIOR, 0.9), (WS.CONFUCIAN, 0.5), (WS.DAOIST, 0.3)]),
        ],
        PT.DIMENSION: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.SCI_FI, 0.9), (WS.DAOIST, 0.5), (WS.MILITARY, 0.4)]),
        ],

        # ── 刑部（监察层）场景 ──
        PT.RISK: [
            (D.XINGBU, DR.PRIMARY,
             [(WS.SUFU, 0.9), (WS.MILITARY, 0.5), (WS.DAOIST, 0.4)]),
            (D.SANFASI, DR.SECONDARY,
             [(WS.SUFU, 0.9), (WS.BUDDHIST, 0.5), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.ETHICAL: [
            (D.XINGBU, DR.PRIMARY,
             [(WS.CONFUCIAN, 0.9), (WS.SUFU, 0.5), (WS.BUDDHIST, 0.3)]),
        ],
        PT.MINDSET: [
            (D.XINGBU, DR.PRIMARY,
             [(WS.BUDDHIST, 0.9), (WS.DAOIST, 0.5), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.EVIDENCE: [
            (D.XINGBU, DR.PRIMARY,
             [(WS.SCIENCE, 0.9), (WS.CONFUCIAN, 0.4), (WS.DAOIST, 0.3)]),
            (D.SANFASI, DR.SECONDARY,
             [(WS.SCIENCE, 0.9), (WS.SUFU, 0.5), (WS.CONFUCIAN, 0.4)]),
        ],

        # ── 吏部（能力层）场景 ──
        PT.GOVERNANCE: [
            (D.LIBU, DR.PRIMARY,
             [(WS.CONFUCIAN, 0.85), (WS.SUFU, 0.6), (WS.DAOIST, 0.4)]),
        ],
        PT.TALENT: [
            (D.LIBU, DR.PRIMARY,
             [(WS.SUFU, 0.9), (WS.CONFUCIAN, 0.5), (WS.BUDDHIST, 0.3)]),
        ],
        PT.LEADERSHIP: [
            (D.LIBU, DR.PRIMARY,
             [(WS.SUFU, 0.9), (WS.CONFUCIAN, 0.5), (WS.DAOIST, 0.4)]),
        ],
        PT.PERSONNEL: [
            (D.LIBU, DR.PRIMARY,
             [(WS.SUFU, 0.9), (WS.CONFUCIAN, 0.5), (WS.BUDDHIST, 0.3)]),
        ],
        PT.CULTURE: [
            (D.LIBU, DR.PRIMARY,
             [(WS.CONFUCIAN, 0.9), (WS.DAOIST, 0.4), (WS.BUDDHIST, 0.3)]),
        ],

        # ── 厂卫（秘密监控）场景 ──
        PT.BALANCE: [
            (D.CHANGWEI, DR.PRIMARY,
             [(WS.DAOIST, 0.95), (WS.METAPHYSICS, 0.7), (WS.CONFUCIAN, 0.4)]),
        ],
        PT.ENVIRONMENT: [
            (D.CHANGWEI, DR.PRIMARY,
             [(WS.METAPHYSICS, 0.95), (WS.DAOIST, 0.55), (WS.CONFUCIAN, 0.25)]),
            (D.CHANGWEI, DR.SECONDARY,
             [(WS.SCIENCE, 0.9), (WS.METAPHYSICS, 0.7), (WS.MILITARY, 0.5)]),
        ],

        # ── WCC / 历史思想 / 五军都督府场景 ──
        PT.META_PERSPECTIVE: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.WCC, 0.9), (WS.NATURAL_SCIENCE, 0.6), (WS.SCI_FI, 0.4)]),
        ],
        PT.PARADIGM_SHIFT: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.HISTORICAL_THOUGHT, 0.95), (WS.WCC, 0.7), (WS.SCIENCE, 0.6)]),
        ],

        # ── 多部门联合调度（问题同时触发多个部门） ──
        PT.STRATEGY: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.DAOIST, 0.85), (WS.CONFUCIAN, 0.5), (WS.MILITARY, 0.4)]),
        ],
        PT.CHANGE: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.DAOIST, 0.85), (WS.CONFUCIAN, 0.5), (WS.SUFU, 0.4)]),
        ],
        PT.HARMONY: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.BUDDHIST, 0.85), (WS.CONFUCIAN, 0.6), (WS.DAOIST, 0.4)]),
        ],
        PT.INTEREST: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.BUDDHIST, 0.8), (WS.CONFUCIAN, 0.6), (WS.MILITARY, 0.4)]),
        ],
        PT.TIMING: [
            (D.CHANGWEI, DR.PRIMARY,
             [(WS.METAPHYSICS, 0.92), (WS.DAOIST, 0.65), (WS.LVSHI, 0.45)]),
        ],
        PT.PATTERN: [
            (D.CHANGWEI, DR.PRIMARY,
             [(WS.METAPHYSICS, 0.9), (WS.DAOIST, 0.55), (WS.GROWTH, 0.3)]),
        ],
        PT.PUBLIC_INTEREST: [
            (D.HUBU, DR.PRIMARY,
             [(WS.LVSHI, 0.9), (WS.CONFUCIAN, 0.5), (WS.SUFU, 0.4)]),
        ],
        PT.YINYANG: [
            (D.CHANGWEI, DR.PRIMARY,
             [(WS.LVSHI, 0.9), (WS.DAOIST, 0.8), (WS.CONFUCIAN, 0.4)]),
        ],
        PT.SURVIVAL: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.SCI_FI, 0.85), (WS.MILITARY, 0.5), (WS.DAOIST, 0.4)]),
        ],
        PT.SCALE: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.SCI_FI, 0.9), (WS.CONFUCIAN, 0.4), (WS.LVSHI, 0.3)]),
        ],
        PT.REVERSE: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.GROWTH, 0.9), (WS.MILITARY, 0.5), (WS.DAOIST, 0.4)]),
        ],
        PT.CREATION_MYTH: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.MYTHOLOGY, 0.9), (WS.DAOIST, 0.5), (WS.BUDDHIST, 0.3)]),
        ],
        PT.APOCALYPSE: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.MYTHOLOGY, 0.9), (WS.MILITARY, 0.5), (WS.DAOIST, 0.4)]),
        ],
        PT.CYCLICAL: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.MYTHOLOGY, 0.9), (WS.DAOIST, 0.7), (WS.METAPHYSICS, 0.5)]),
        ],
        PT.RESILIENCE: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.LITERARY, 0.9), (WS.BUDDHIST, 0.5), (WS.CONFUCIAN, 0.4)]),
        ],
        PT.RITUAL: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.ANTHROPOLOGY, 0.9), (WS.CONFUCIAN, 0.5), (WS.DAOIST, 0.3)]),
        ],
        PT.CULTURAL_CHANGE: [
            (D.HUBU, DR.PRIMARY,
             [(WS.ANTHROPOLOGY, 0.9), (WS.CIVILIZATION, 0.6), (WS.MYTHOLOGY, 0.4)]),
        ],
        PT.WILLPOWER: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.BEHAVIOR, 0.9), (WS.BUDDHIST, 0.5), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.PHYSICS_ANALYSIS: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.NATURAL_SCIENCE, 0.95), (WS.SCIENCE, 0.6), (WS.SCI_FI, 0.4)]),
        ],
        PT.LIFE_SCIENCE: [
            (D.HUBU, DR.PRIMARY,
             [(WS.NATURAL_SCIENCE, 0.95), (WS.SCIENCE, 0.6), (WS.DAOIST, 0.3)]),
        ],
        PT.EARTH_SYSTEM: [
            (D.HUBU, DR.PRIMARY,
             [(WS.NATURAL_SCIENCE, 0.95), (WS.METAPHYSICS, 0.5), (WS.DAOIST, 0.4)]),
        ],
        PT.COSMOS_EXPLORATION: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.NATURAL_SCIENCE, 0.95), (WS.SCI_FI, 0.7), (WS.DAOIST, 0.4)]),
        ],
        PT.SCALE_CROSSING: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.NATURAL_SCIENCE, 0.9), (WS.SCI_FI, 0.6), (WS.DAOIST, 0.5)]),
        ],
        PT.CIVILIZATION_ANALYSIS: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.WCC, 0.9), (WS.CIVILIZATION, 0.8), (WS.CIV_WAR_ECONOMY, 0.5)]),
        ],
        PT.COSMIC_COGNITION: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.WCC, 0.9), (WS.NATURAL_SCIENCE, 0.8), (WS.DAOIST, 0.4)]),
        ],
        PT.SCALE_TRANSFORMATION: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.WCC, 0.9), (WS.NATURAL_SCIENCE, 0.7), (WS.SCI_FI, 0.5)]),
        ],
        PT.WORLDVIEW_SHIFT: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.WCC, 0.9), (WS.NATURAL_SCIENCE, 0.6), (WS.DEWEY, 0.4)]),
        ],
        PT.WISDOM_EVOLUTION: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.WCC, 0.9), (WS.CIVILIZATION, 0.7), (WS.NATURAL_SCIENCE, 0.6)]),
        ],
        PT.TECH_EVOLUTION: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.WCC, 0.9), (WS.CIVILIZATION, 0.7), (WS.NATURAL_SCIENCE, 0.5)]),
        ],
        PT.HISTORICAL_ANALYSIS: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.HISTORICAL_THOUGHT, 0.95), (WS.CIVILIZATION, 0.7), (WS.WCC, 0.6)]),
        ],
        PT.THOUGHT_EVOLUTION: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.HISTORICAL_THOUGHT, 0.95), (WS.CIVILIZATION, 0.6), (WS.SCIENCE, 0.5)]),
        ],
        PT.ECONOMIC_EVOLUTION: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.HISTORICAL_THOUGHT, 0.95), (WS.CIV_WAR_ECONOMY, 0.7), (WS.CIVILIZATION, 0.5)]),
        ],
        PT.TECH_HISTORY: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.HISTORICAL_THOUGHT, 0.95), (WS.WCC, 0.6), (WS.NATURAL_SCIENCE, 0.5)]),
        ],
        PT.CROSS_DIMENSION: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.HISTORICAL_THOUGHT, 0.95), (WS.WCC, 0.6), (WS.NATURAL_SCIENCE, 0.5)]),
        ],
        PT.STATE_CAPACITY: [
            (D.HUBU, DR.PRIMARY,
             [(WS.CONFUCIAN, 0.86), (WS.SUFU, 0.52), (WS.LVSHI, 0.45)]),
        ],
        PT.INSTITUTIONAL_SEDIMENTATION: [
            (D.HUBU, DR.PRIMARY,
             [(WS.CONFUCIAN, 0.82), (WS.LVSHI, 0.56), (WS.DAOIST, 0.36)]),
        ],

        # ── V6.0 第二阶段: 心理学ProblemType（礼部+厂卫联合） ──
        PT.PERSONALITY_ANALYSIS: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.PSYCHOLOGY, 0.9), (WS.BEHAVIOR, 0.6), (WS.BUDDHIST, 0.4)]),
        ],
        PT.GROUP_DYNAMICS: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.PSYCHOLOGY, 0.9), (WS.CONFUCIAN, 0.5), (WS.DAOIST, 0.4)]),
        ],
        PT.COGNITIVE_BIAS: [
            (D.CHANGWEI, DR.PRIMARY,
             [(WS.PSYCHOLOGY, 0.9), (WS.BEHAVIOR, 0.5), (WS.SCIENCE, 0.4)]),
        ],
        PT.MOTIVATION_ANALYSIS: [
            (D.HUBU, DR.PRIMARY,
             [(WS.PSYCHOLOGY, 0.9), (WS.BEHAVIOR, 0.6), (WS.DAOIST, 0.3)]),
        ],
        PT.PSYCHOLOGICAL_ARITHMETIC: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.PSYCHOLOGY, 0.9), (WS.NATURAL_SCIENCE, 0.5), (WS.SCIENCE, 0.4)]),
        ],
        PT.TRAUMA_HEALING: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.PSYCHOLOGY, 0.9), (WS.BUDDHIST, 0.6), (WS.DAOIST, 0.4)]),
        ],
        PT.SELF_ACTUALIZATION: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.PSYCHOLOGY, 0.9), (WS.BUDDHIST, 0.5), (WS.GROWTH, 0.4)]),
        ],
        PT.INTERPERSONAL_RELATIONSHIP: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.PSYCHOLOGY, 0.9), (WS.CONFUCIAN, 0.6), (WS.BUDDHIST, 0.3)]),
        ],

        # ── V6.0 第二阶段: 系统论ProblemType（五军都督府+工部） ──
        PT.COMPLEX_SYSTEM: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.SYSTEMS, 0.9), (WS.SCIENCE, 0.6), (WS.DAOIST, 0.5)]),
        ],
        PT.FEEDBACK_LOOP: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.SYSTEMS, 0.9), (WS.SCIENCE, 0.5), (WS.GROWTH, 0.4)]),
        ],
        PT.EMERGENT_BEHAVIOR: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.SYSTEMS, 0.9), (WS.DAOIST, 0.6), (WS.SCI_FI, 0.3)]),
        ],
        PT.SYSTEM_EQUILIBRIUM: [
            (D.CHANGWEI, DR.PRIMARY,
             [(WS.SYSTEMS, 0.9), (WS.DAOIST, 0.5), (WS.METAPHYSICS, 0.4)]),
        ],
        PT.ADAPTIVE_SYSTEM: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.SYSTEMS, 0.9), (WS.GROWTH, 0.5), (WS.SCIENCE, 0.3)]),
        ],

        # ── V6.0 第二阶段: 管理学ProblemType（吏部+户部联合） ──
        PT.STRATEGIC_PLANNING: [
            (D.LIBU, DR.PRIMARY,
             [(WS.MANAGEMENT, 0.9), (WS.CONFUCIAN, 0.5), (WS.DAOIST, 0.4)]),
        ],
        PT.ORGANIZATIONAL_DESIGN: [
            (D.LIBU, DR.PRIMARY,
             [(WS.MANAGEMENT, 0.9), (WS.FAJIA, 0.5), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.PERFORMANCE_MANAGEMENT: [
            (D.LIBU, DR.PRIMARY,
             [(WS.MANAGEMENT, 0.9), (WS.FAJIA, 0.4), (WS.SUFU, 0.3)]),
        ],
        PT.KNOWLEDGE_MANAGEMENT: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.MANAGEMENT, 0.9), (WS.GROWTH, 0.5), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.CHANGE_MANAGEMENT: [
            (D.LIBU, DR.PRIMARY,
             [(WS.MANAGEMENT, 0.9), (WS.DAOIST, 0.5), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.INNOVATION_MANAGEMENT: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.MANAGEMENT, 0.9), (WS.SCI_FI, 0.4), (WS.GROWTH, 0.4)]),
        ],

        # ── V6.0 第二阶段: 纵横家ProblemType（兵部+户部联合） ──
        PT.DIPLOMATIC_NEGOTIATION: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.ZONGHENG, 0.9), (WS.MILITARY, 0.6), (WS.DAOIST, 0.4)]),
        ],
        PT.ALLIANCE_BUILDING: [
            (D.HUBU, DR.PRIMARY,
             [(WS.ZONGHENG, 0.9), (WS.CONFUCIAN, 0.5), (WS.DAOIST, 0.4)]),
        ],
        PT.POWER_BALANCE: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.ZONGHENG, 0.9), (WS.FAJIA, 0.5), (WS.DAOIST, 0.4)]),
        ],

        # ── V6.0 第三阶段: 墨家（工部主调度） ──
        PT.ENGINEERING_INNOVATION: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.MOZI, 0.9), (WS.SCIENCE, 0.6), (WS.NATURAL_SCIENCE, 0.4)]),
            (D.BINGBU, DR.SECONDARY,
             [(WS.MILITARY, 0.5), (WS.SCI_FI, 0.3)]),
        ],
        PT.COST_OPTIMIZATION: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.MOZI, 0.9), (WS.SUFU, 0.5), (WS.MANAGEMENT, 0.4)]),
        ],
        PT.UNIVERSAL_BENEFIT: [
            (D.HUBU, DR.PRIMARY,
             [(WS.MOZI, 0.9), (WS.CONFUCIAN, 0.5), (WS.BUDDHIST, 0.4)]),
            (D.LIBU_LI, DR.SECONDARY,
             [(WS.BEHAVIOR, 0.6), (WS.GROWTH, 0.4)]),
        ],
        PT.DEFENSE_FORTIFICATION: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.MOZI, 0.9), (WS.MILITARY, 0.6), (WS.SCIENCE, 0.4)]),
            (D.GONGBU, DR.SECONDARY,
             [(WS.SCIENCE, 0.7), (WS.NATURAL_SCIENCE, 0.4)]),
        ],
        PT.LOGICAL_DEDUCTION: [
            (D.HANLIN, DR.PRIMARY,
             [(WS.MOZI, 0.9), (WS.SCIENCE, 0.6), (WS.TOP_METHODS, 0.4)]),
        ],

        # ── V6.0 第三阶段: 法家（刑部主调度） ──
        PT.INSTITUTIONAL_DESIGN: [
            (D.XINGBU, DR.PRIMARY,
             [(WS.FAJIA, 0.9), (WS.CONFUCIAN, 0.4), (WS.MANAGEMENT, 0.3)]),
            (D.LIBU, DR.SECONDARY,
             [(WS.MANAGEMENT, 0.6), (WS.CONFUCIAN, 0.4)]),
        ],
        PT.LAW_ENFORCEMENT: [
            (D.XINGBU, DR.PRIMARY,
             [(WS.FAJIA, 0.9), (WS.SUFU, 0.5), (WS.MILITARY, 0.3)]),
            (D.SANFASI, DR.SECONDARY,
             [(WS.FAJIA, 0.8), (WS.CONFUCIAN, 0.4)]),
        ],
        PT.POWER_STRUCTURING: [
            (D.XINGBU, DR.PRIMARY,
             [(WS.FAJIA, 0.9), (WS.ZONGHENG, 0.5), (WS.CONFUCIAN, 0.3)]),
            (D.BINGBU, DR.SECONDARY,
             [(WS.MILITARY, 0.5), (WS.ZONGHENG, 0.4)]),
        ],
        PT.REWARD_PUNISHMENT: [
            (D.XINGBU, DR.PRIMARY,
             [(WS.FAJIA, 0.9), (WS.SUFU, 0.6), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.HUMAN_NATURE_ANALYSIS: [
            (D.XINGBU, DR.PRIMARY,
             [(WS.FAJIA, 0.9), (WS.PSYCHOLOGY, 0.5), (WS.BEHAVIOR, 0.4)]),
            (D.HUBU, DR.SECONDARY,
             [(WS.PSYCHOLOGY, 0.7), (WS.BEHAVIOR, 0.5)]),
        ],
        PT.STATE_CONSOLIDATION: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.FAJIA, 0.9), (WS.MILITARY, 0.5), (WS.CONFUCIAN, 0.4)]),
            (D.XINGBU, DR.SECONDARY,
             [(WS.FAJIA, 0.8), (WS.SUFU, 0.4)]),
        ],

        # ── V6.0 第三阶段: 经济学（户部主调度） ──
        PT.RESOURCE_ALLOCATION: [
            (D.HUBU, DR.PRIMARY,
             [(WS.ECONOMICS, 0.95), (WS.SOCIAL_SCIENCE, 0.7), (WS.MILITARY, 0.5)]),
        ],
        PT.SUPPLY_DEMAND_BALANCE: [
            (D.HUBU, DR.PRIMARY,
             [(WS.ECONOMICS, 0.95), (WS.SOCIAL_SCIENCE, 0.7), (WS.MILITARY, 0.5)]),
        ],
        PT.ECONOMIC_INCENTIVE: [
            (D.HUBU, DR.PRIMARY,
             [(WS.ECONOMICS, 0.95), (WS.BEHAVIOR, 0.7), (WS.SOCIAL_SCIENCE, 0.6)]),
        ],
        PT.MARKET_EFFICIENCY: [
            (D.HUBU, DR.PRIMARY,
             [(WS.ECONOMICS, 0.95), (WS.SOCIAL_SCIENCE, 0.7), (WS.SCIENCE, 0.5)]),
        ],
        PT.INVESTMENT_DECISION: [
            (D.HUBU, DR.PRIMARY,
             [(WS.ECONOMICS, 0.95), (WS.SUFU, 0.7), (WS.MILITARY, 0.5)]),
        ],

        # ── V6.0 第三阶段: 名家（翰林院主调度） ──
        PT.LOGICAL_PARADOX: [
            (D.HANLIN, DR.PRIMARY,
             [(WS.MINGJIA, 0.95), (WS.DAOIST, 0.6), (WS.SCIENCE, 0.4)]),
        ],
        PT.CLASSIFICATION_REFINEMENT: [
            (D.HANLIN, DR.PRIMARY,
             [(WS.MINGJIA, 0.95), (WS.CONFUCIAN, 0.6), (WS.SCIENCE, 0.4)]),
        ],
        PT.DIALECTICAL_REASONING: [
            (D.HANLIN, DR.PRIMARY,
             [(WS.MINGJIA, 0.95), (WS.DAOIST, 0.7), (WS.MILITARY, 0.5)]),
        ],

        # ── V6.0 第三阶段: 阴阳家（厂卫主调度） ──
        PT.WUXING_ANALYSIS: [
            (D.CHANGWEI, DR.PRIMARY,
             [(WS.WUXING, 0.95), (WS.METAPHYSICS, 0.8), (WS.DAOIST, 0.6)]),
        ],
        PT.YINYANG_DIALECTICS: [
            (D.CHANGWEI, DR.PRIMARY,
             [(WS.WUXING, 0.95), (WS.DAOIST, 0.8), (WS.METAPHYSICS, 0.6)]),
        ],
        PT.SEASONAL_RHYTHM: [
            (D.HUBU, DR.PRIMARY,
             [(WS.WUXING, 0.95), (WS.LVSHI, 0.7), (WS.METAPHYSICS, 0.6)]),
        ],
        PT.COSMIC_HARMONY: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.WUXING, 0.95), (WS.DAOIST, 0.8), (WS.METAPHYSICS, 0.6)]),
        ],
        PT.CYCLICAL_TRANSFORMATION: [
            (D.CHANGWEI, DR.PRIMARY,
             [(WS.WUXING, 0.95), (WS.METAPHYSICS, 0.8), (WS.DAOIST, 0.7)]),
        ],

        # ── V6.0 第三阶段: 复杂性科学（五军都督府主调度） ──
        PT.EMERGENT_ORDER: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.COMPLEXITY, 0.95), (WS.SCIENCE, 0.7), (WS.SYSTEMS, 0.6)]),
        ],
        PT.NETWORK_DYNAMICS: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.COMPLEXITY, 0.95), (WS.SOCIAL_SCIENCE, 0.7), (WS.SCIENCE, 0.6)]),
        ],
        PT.ADAPTIVE_EVOLUTION: [
            (D.WUJUN, DR.PRIMARY,
             [(WS.COMPLEXITY, 0.95), (WS.BEHAVIOR, 0.7), (WS.SYSTEMS, 0.6)]),
        ],

        # ── V6.0 精细优化: 学派子领域细分ProblemType部门路由 ──
        PT.CONFUCIAN_SUB_SCHOOL: [
            (D.LIBU, DR.PRIMARY,
             [(WS.CONFUCIAN, 0.95), (WS.YANGMING, 0.7), (WS.DAOIST, 0.3)]),
        ],
        PT.DAOIST_SUB_SCHOOL: [
            (D.CHANGWEI, DR.PRIMARY,
             [(WS.DAOIST, 0.95), (WS.METAPHYSICS, 0.6), (WS.BUDDHIST, 0.4)]),
        ],
        PT.BUDDHIST_SUB_SCHOOL: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.BUDDHIST, 0.95), (WS.DAOIST, 0.5), (WS.CONFUCIAN, 0.3)]),
        ],
        PT.MILITARY_SUB_SCHOOL: [
            (D.BINGBU, DR.PRIMARY,
             [(WS.MILITARY, 0.95), (WS.DAOIST, 0.5), (WS.FAJIA, 0.4)]),
        ],
        PT.TALENT_PIPELINE: [
            (D.LIBU, DR.PRIMARY,
             [(WS.CONFUCIAN, 0.85), (WS.SUFU, 0.7), (WS.YANGMING, 0.5)]),
        ],
        PT.ORGANIZATIONAL_CULTURE: [
            (D.LIBU, DR.PRIMARY,
             [(WS.CONFUCIAN, 0.8), (WS.DAOIST, 0.5), (WS.PSYCHOLOGY, 0.4)]),
        ],
        PT.BRAND_CULTURE: [
            (D.HUBU, DR.PRIMARY,
             [(WS.CHINESE_CONSUMER, 0.9), (WS.LITERARY, 0.7), (WS.CONFUCIAN, 0.5)]),
        ],
        PT.PHILOSOPHY_OF_MIND: [
            (D.LIBU_LI, DR.PRIMARY,
             [(WS.YANGMING, 0.95), (WS.CONFUCIAN, 0.7), (WS.BUDDHIST, 0.5)]),
        ],
        PT.DECISION_FRAMEWORK: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.TOP_METHODS, 0.85), (WS.SCIENCE, 0.6), (WS.CONFUCIAN, 0.5)]),
        ],
        PT.RESOURCE_ECOLOGY: [
            (D.HUBU, DR.PRIMARY,
             [(WS.ECONOMICS, 0.85), (WS.DAOIST, 0.6), (WS.SYSTEMS, 0.5)]),
        ],
        PT.INNOVATION_ECOLOGY: [
            (D.GONGBU, DR.PRIMARY,
             [(WS.MANAGEMENT, 0.85), (WS.SCI_FI, 0.6), (WS.MOZI, 0.5)]),
        ],
    }
