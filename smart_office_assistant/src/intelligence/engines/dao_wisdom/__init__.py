"""
道家哲学核心模块 v2.0 - 包入口
向后兼容: 从 .dao_wisdom_core 导入的所有路径仍然有效

模块结构:
- __init__.py      : Facade(重新导出所有内容,定义DaoWisdomCore)
- _dao_enums.py   : 枚举定义和dataclass
- _dao_logic.py   : DaoWisdomCore业务方法
"""

# ============================================================
# 从子模块导入所有枚举和dataclass(保持__all__兼容)
# ============================================================

from ._dao_enums import (
    DaoDeJingCore,
    BaGua,
    BaGuaRelation,
    ZhuangziCore,
    DeJingHierarchy,
    DaoThreeRealms,
    WuXing,
    WuXingCycle,
    SiXiang,
    DaoManagement,
    DaoHealth,
    YinYang,
    YinYangPrinciple,
    LuoShu,
    DaoWisdom,
    DaoDecision,
    TaoistPersona,
)

# ============================================================
# 从逻辑模块导入方法实现(来自3个子文件)
# ============================================================

from ._dao_yin_yang import (
    dao_init,
    analyze_yin_yang,
    analyze_bagua,
    get_daojing_wisdom,
    evaluate_with_taiji,
    make_dao_decision,
    get_luoshu_guidance,
    apply_to_growth_strategy,
)

from ._dao_v2 import (
    get_zhuangzi_wisdom,
    analyze_de_jing_hierarchy,
    analyze_wuxing_cycle,
    analyze_sixiang,
    get_dao_management_advice,
    get_dao_health_guide,
    get_dao_three_realms,
    analyze_xian_tian_hou_tian,
)

from ._dao_comprehensive import (
    comprehensive_dao_analysis,
)

# ============================================================
# DaoWisdomCore Facade类(将方法绑定到子模块实现)
# ============================================================

class DaoWisdomCore:
    """
    道家哲学智慧核心引擎

    将<道德经>+ 阴阳 + 太极 + 八卦 + 九宫 + 洛书融入智能decision:

    核心模块:
    1. 道德经智慧库 - 81章核心思想精选
    2. 阴阳辩证系统 - 五基本原则应用
    3. 八卦分析系统 - 先天/后天八卦分析
    4. 太极decision评估 - 阴阳平衡judge
    5. 九宫洛书应用 - 数字能量与方位
    6. 增长战略fusion - 道家商业智慧
    """

    def __init__(self):
        dao_init(self)

    # 阴阳辩证分析
    def analyze_yin_yang(self, situation: str, factors: dict) -> dict:
        return analyze_yin_yang(self, situation, factors)

    # 八卦分析
    def analyze_bagua(self, domain: str, context: dict) -> dict:
        return analyze_bagua(self, domain, context)

    # 道德经智慧应用
    def get_daojing_wisdom(self, theme: str, situation: str = None) -> dict:
        return get_daojing_wisdom(self, theme, situation)

    # 太极decision评估
    def evaluate_with_taiji(self, yin_score: float, yang_score: float) -> dict:
        return evaluate_with_taiji(self, yin_score, yang_score)

    # synthesize_decision
    def make_dao_decision(self, situation: str, factors: dict,
                          domain: str = None) -> DaoDecision:
        return make_dao_decision(self, situation, factors, domain)

    # 洛书九宫应用
    def get_luoshu_guidance(self, position: str) -> dict:
        return get_luoshu_guidance(self, position)

    # 增长战略应用
    def apply_to_growth_strategy(self, growth_phase: str, current_state: dict) -> dict:
        return apply_to_growth_strategy(self, growth_phase, current_state)

    # v2.0 博士级增强方法
    def get_zhuangzi_wisdom(self, theme: str) -> dict:
        return get_zhuangzi_wisdom(self, theme)

    def analyze_de_jing_hierarchy(self, situation: str) -> dict:
        return analyze_de_jing_hierarchy(self, situation)

    def analyze_wuxing_cycle(self, element: str, action: str) -> dict:
        return analyze_wuxing_cycle(self, element, action)

    def analyze_sixiang(self, season: str = None, state: str = None) -> dict:
        return analyze_sixiang(self, season, state)

    def get_dao_management_advice(self, scenario: str) -> dict:
        return get_dao_management_advice(self, scenario)

    def get_dao_health_guide(self, concern: str) -> dict:
        return get_dao_health_guide(self, concern)

    def get_dao_three_realms(self) -> dict:
        return get_dao_three_realms(self)

    def analyze_xian_tian_hou_tian(self, domain: str) -> dict:
        return analyze_xian_tian_hou_tian(self, domain)

    def comprehensive_dao_analysis(self, question: str, context: dict = None) -> dict:
        return comprehensive_dao_analysis(self, question, context)

# ============================================================
# 向后兼容别名
# ============================================================

DaoPrinciple = YinYangPrinciple
YinYangBalance = YinYangPrinciple  # 兼容 wisdom_fusion_core.py 导入

# ============================================================
# 导出
# ============================================================

__all__ = [
    'DaoWisdomCore',
    'DaoWisdom',
    'DaoDecision',
    'TaoistPersona',
    'DaoDeJingCore',
    'BaGua',
    'BaGuaRelation',
    'YinYang',
    'YinYangPrinciple',
    'LuoShu',
    # v2.0 博士级新增
    'ZhuangziCore',
    'DeJingHierarchy',
    'DaoThreeRealms',
    'WuXing',
    'WuXingCycle',
    'SiXiang',
    'DaoManagement',
    'DaoHealth',
    # 向后兼容别名
    'DaoPrinciple',
]
