# -*- coding: utf-8 -*-
"""王阳明知行合一引擎包

模块化重构后的知行合一执行引擎

子模块:
    _yze_types: 类型定义
    _yze_knowledge: 知识库
    _yze_core: 核心引擎
"""

from ._yze_core import ZhixingEngine
from ._yze_types import (
    KnowingLevel, ActionStage, ZhixingBarrier,
    KnowingAnalysis, ActionAnalysis, ZhixingLoop,
    TrueKnowledgeValidator, ActionStarterConfig, IterationDeepener
)

def diagnose(knowing: str, action: str) -> dict:
    """快速知行闭环诊断"""
    engine = ZhixingEngine()
    result = engine.diagnose_zhixing(knowing, action)
    return {
        "知的层次": result.knowing.level.value,
        "知之得分": f"{result.knowing.score:.0f}/100",
        "行之所处": result.action.stage.value,
        "行之得分": f"{result.action.score:.0f}/100",
        "知行合一": f"{result.integration_score:.0f}/100",
        "是否真知": "是" if result.is_true_knowledge else "否",
        "差距类型": result.gap_type,
        "闭环路径": result.closure_path,
        "立即action": result.immediate_action
    }

def validate_true_knowing(knowing: str, action: str) -> dict:
    """快速真知验证"""
    engine = ZhixingEngine()
    result = engine.validate_true_knowledge(knowing, action)
    return {
        "是否真知": "是" if result.is_true_knowledge else "否",
        "置信度": f"{result.confidence*100:.0f}%",
        "支持证据": result.evidence_for,
        "反对证据": result.evidence_against,
        "建议": result.recommendation
    }

def start_action(task: str, barrier: str = "") -> dict:
    """快速action启动"""
    engine = ZhixingEngine()
    result = engine.start_action(task, barrier)
    return {
        "任务": result.task,
        "最小action": result.mini_action,
        "障碍类型": result.barrier_analysis[0]["barrier_type"],
        "解决方案": result.barrier_analysis[0]["solution"],
        "动力提升": result.motivation_boost,
        "减少阻力": result.friction_reducers,
        "启动触发": result.start_trigger
    }

__all__ = [
    "ZhixingEngine",
    "KnowingLevel",
    "ActionStage",
    "ZhixingBarrier",
    "KnowingAnalysis",
    "ActionAnalysis",
    "ZhixingLoop",
    "TrueKnowledgeValidator",
    "ActionStarterConfig",
    "IterationDeepener",
    "diagnose",
    "validate_true_knowing",
    "start_action",
    # 中文别名（兼容 yangming_autonomous_fusion.py 导入）
    "知行合一引擎",
    "知行场景",
]

# 中文别名
知行合一引擎 = ZhixingEngine
知行场景 = KnowingLevel
