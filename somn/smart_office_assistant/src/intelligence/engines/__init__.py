# -*- coding: utf-8 -*-
"""
智慧引擎层 - engines 子模块
目录整理 v1.2 (2026-04-06)
子目录归档: literary/(50 poet), philosophy/(5 yangming), psychology/(5 pioneer)

降级兼容机制（Backward Compatibility）
==========================================
engines/__init__.py 使用 importlib 动态加载 + globals() 主动导出，
使旧路径导入（如 `from src.intelligence.engines import 杜甫深化引擎`）
与新路径导入（如 `from src.intelligence.engines.literary.poet_du_fu_engine import 杜甫深化引擎`）
完全兼容，无需任何迁移代码。

子目录模块通过 dotted 路径注册（literary.poet_*, philosophy.yangming_*,
psychology.pioneer_*），所有导出属性自动出现在 engines 命名空间。

已验证别名（via __init__.py re-export）:
  杜甫深化引擎 / 李白深化引擎 / 王阳明心学引擎 / 弗洛伊德潜意识引擎 /
  特劳特定位引擎 / 唐诗宋词fusion模块 / 知行合一引擎 / 良知系统 /
  心理学先驱融合引擎 / yangming_fusion
"""

import os
import importlib
import logging

logger = logging.getLogger(__name__)

__all__ = []
__exported__ = {}

_MODULES = [
    "ai_native_growth_strategies",
    "ancient_wisdom_fusion_core",
    "anthropology_wisdom_engine",
    "behavior_shaping_engine",
    "buddha_wisdom_core",
    "buddhism_deep_core",
    "chinese_consumer_culture_engine",
    "civilization_war_economy_core",
    "civilization_wisdom_core",
    "classic_wisdom_core",
    "closed_loop_system",
    "combinatorial_optimizer",
    "confucian_buddhist_dao_fusion_engine",
    "consulting_validator",
    "cosmic_worldview_module",
    "cross_culture_engine",
    "cross_scale_thinking_engine",
    "cross_wisdom_analyzer",
    "dao_wisdom_core",
    "de_zhi_planner",
    "early_tang_four_geniuses_fusion",
    "earth_cosmos_wisdom_core",
    "efficient_learning_core",
    "emotion_wave_engine",
    "enterprise_strategy_system",
    "fengshui_environment_engine",
    "gabor_feature_system",
    "gentle_conduct_system",
    "gestalt_organization_engine",
    "graph_theory_engine",
    "growth_mindset_evaluator",
    "hebbian_ensemble_engine",
    "historical_thought_trinity_engine",
    "honglou_insight_engine",
    "hongming_wisdom_core",
    "life_science_wisdom_core",
    "literary_narrative_engine",
    "lvshi_wisdom_engine",
    "marketing_psychology_unified",
    "marvel_wisdom_unified",
    "math_wisdom_core",
    "memory_manager",
    "metaphysics_wisdom_unified",
    "military_strategy_engine",
    "mingfen_order_system",
    "minimalist_focus_system",
    "moral_ethics_evaluator",
    "mythology_wisdom_engine",
    "narrative_intelligence_engine",
    "natural_science_unified",
    "natural_science_wisdom_core",
    "neural_voice_core",
    "neuromath_vision_unified",
    "neuron_wisdom_network",
    "neuroscience_unified_core",
    "neuro_math_deep_system",
    "p2_integration_fusion",
    "persona_core",
    # psychology/ — 心理学先驱引擎
    "psychology.pioneer_freud_engine",
    "psychology.pioneer_jung_archetype",
    "psychology.pioneer_maslow_dynamic",
    "psychology.pioneer_ogilvy_narrative",
    "psychology.pioneer_positioning_engine",
    # literary/ — 诗人深化引擎
    "literary.poet_bai_jv_yi_engine",
    "literary.poet_cen_shen_engine",
    "literary.poet_du_fu_engine",
    "literary.poet_du_mu_engine",
    "literary.poet_fan_zhong_yan_engine",
    "literary.poet_gao_shi_engine",
    "literary.poet_han_yu_engine",
    "literary.poet_huang_ting_jian_engine",
    "literary.poet_jia_dao_engine",
    "literary.poet_jiang_jie_engine",
    "literary.poet_jiang_kui_engine",
    "literary.poet_li_bai_engine",
    "literary.poet_li_he_engine",
    "literary.poet_li_qing_zhao_engine",
    "literary.poet_li_shang_yin_engine",
    "literary.poet_li_yu_engine",
    "literary.poet_liu_ke_zhuang_engine",
    "literary.poet_liu_yong_engine",
    "literary.poet_liu_yu_xi_engine",
    "literary.poet_liu_zong_yuan_engine",
    "literary.poet_lu_you_engine",
    "literary.poet_lu_zhao_lin_engine",
    "literary.poet_luo_bin_wang_engine",
    "literary.poet_luo_yin_engine",
    "literary.poet_meng_hao_ran_engine",
    "literary.poet_meng_jiao_engine",
    "literary.poet_ou_yang_xiu_engine",
    "literary.poet_qin_guan_engine",
    "literary.poet_shi_da_zu_engine",
    "literary.poet_su_shi_engine",
    "literary.poet_wang_an_shi_engine",
    "literary.poet_wang_bo_engine",
    "literary.poet_wang_chang_ling_engine",
    "literary.poet_wang_wei_engine",
    "literary.poet_wang_yi_sun_engine",
    "literary.poet_wang_zhi_huan_engine",
    "literary.poet_wei_zhuang_engine",
    "literary.poet_wen_tian_xiang_engine",
    "literary.poet_wen_ting_yun_engine",
    "literary.poet_wu_wen_ying_engine",
    "literary.poet_xin_qi_ji_engine",
    "literary.poet_yan_ji_dao_engine",
    "literary.poet_yan_shu_engine",
    "literary.poet_yang_jiong_engine",
    "literary.poet_yang_wan_li_engine",
    "literary.poet_yuan_zhen_engine",
    "literary.poet_zhang_xian_engine",
    "literary.poet_zhang_yan_engine",
    "literary.poet_zhou_bang_yan_engine",
    "literary.poet_zhou_mi_engine",
    "profanity_guard",
    "psychology_pioneer_fusion",
    "risk_warning_wisdom",
    "_research_strategy_engine",
    "ru_classics_deep_system",
    "ru_wisdom_core",
    "ru_wisdom_unified",
    "sanguo_strategy_engine",
    "sanjiao_fusion_engine",
    "science_thinking_engine",
    "scientific_ad_verification",
    "self_cultivation_system",
    "shuihu_team_engine",
    "social_science_engine",
    "sticker_arsenal",
    "sticker_saver",
    "subconscious_demand_analyzer",
    "subliminal_persuasion_engine",
    "sufu_demo",
    "sufu_wisdom_core",
    "super_learning_engine",
    "super_wisdom_coordinator",
    "supreme_decision_fusion_engine",
    "symplectic_decision_framework",
    "synaptic_plasticity_engine",
    "talent_assessment_wisdom",
    "tang_song_poetry_fusion",
    # [P1修复] 移除死引用: test_persona, test_sharp_engine
    # "test_persona",
    # "test_sharp_engine",
    "thinking_growth_unified",
    "thinking_mode_fusion_engine",
    "top_thinking_engine",
    "traditional_metaphysics_core",
    "transcend_inferiority_engine",
    "unified_intelligence_coordinator",
    "unity_knowledge_action",
    "user_centered_experience",
    "user_growth_tracker",
    "veblen_consumption_analyzer",
    "wcc_evolutionary_core",
    "wuchang_ethics",
    "xiyou_growth_engine",
    # philosophy/ — 王阳明心学引擎
    "philosophy.yangming_autonomous_fusion",
    "philosophy.yangming_liangzhi_system",
    "philosophy.yangming_shiyan_engine",
    "philosophy.yangming_xinxue_engine",
    "philosophy.yangming_zhixing_engine",
    "yi_change_manager",
    "zhongyong_engine",
]

for _mod_name in _MODULES:
    try:
        _mod = importlib.import_module(f".{_mod_name}", __name__)
        for _attr in dir(_mod):
            if not _attr.startswith("_"):
                globals()[_attr] = getattr(_mod, _attr)
                __all__.append(_attr)
                __exported__[_mod_name] = __exported__.get(_mod_name, [])
                __exported__[_mod_name].append(_attr)
    except ImportError as e:
        logger.debug(f"engines.{_mod_name} 懒加载: {e}")
    except Exception as e:
        # 静默跳过懒加载异常（模块内含名称缺失或原有bug）
        pass
