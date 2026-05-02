"""
Sub-Engines 子引擎系统统一入口
================================

两个完全独立的推理系统：

1. DivineReason (神之推理)
   - 142个子推理引擎
   - 基于问题类型(ProblemType)调度
   - 包含: 认知/战略/创意/分析/决策 五大类

2. PanWisdomTree (万法智慧树)
   - 基于学派哲学的推理系统
   - 基于学派(WisdomSchool)调度
   - 包含: 道家/儒家/兵家/阴阳家/法家/墨家等十家

两个系统完全独立，互不交叉，各自运行。
"""

# ═══════════════════════════════════════════════════════════════════════════
# DivineReason - 神之推理 (142个引擎)
# ═══════════════════════════════════════════════════════════════════════════

from ._divine_reason_engine import (
    DivineReasonEngine,
    get_divine_reason_engine,
    ReasoningRequest,
    ReasoningResponse,
    ProblemAnalyzer,
    IntelligentResultFuser,
    diagnose_reasoning_problem,
)

from ._sub_engine_base import (
    EngineCategory,
    ReasoningResult,
)

# 导出子类型枚举 (用于查询)
from ._cognitive_engines import CognitiveSubType
from ._strategic_engines import StrategicSubType
from ._creative_engines import CreativeSubType
from ._analytical_engines import AnalyticalSubType
from ._decision_engines import DecisionSubType

# ═══════════════════════════════════════════════════════════════════════════
# PanWisdomTree - 万法智慧树 (基于学派)
# ═══════════════════════════════════════════════════════════════════════════

# V2.0/V2.1 导入 (原 V1.0 已删除)
# 添加 knowledge_cells 路径
import sys
import os
_knowledge_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), 'knowledge_cells')
if _knowledge_path not in sys.path:
    sys.path.insert(0, _knowledge_path)

from knowledge_cells.pan_wisdom_core import (
    PanWisdomTree,
    PanWisdomResult,
    WisdomSchool,
    ProblemType,
    get_pan_wisdom_tree,
    solve_with_wisdom,
    preload_pan_wisdom,
    is_pan_wisdom_ready,
)

# 向后兼容别名
WisdomTreeCore = PanWisdomTree
reason_with_wisdom_tree = solve_with_wisdom

# ═══════════════════════════════════════════════════════════════════════════
# 统一导出
# ═══════════════════════════════════════════════════════════════════════════

__all__ = [
    # DivineReason 系统
    'DivineReasonEngine',
    'get_divine_reason_engine',
    'ReasoningRequest',
    'ReasoningResponse',
    'ReasoningResult',
    'EngineCategory',
    
    # DivineReason 子类型
    'CognitiveSubType',
    'StrategicSubType',
    'CreativeSubType',
    'AnalyticalSubType',
    'DecisionSubType',
    
    # PanWisdomTree 系统 (V2.0/V2.1)
    'PanWisdomTree',
    'get_pan_wisdom_tree',
    'solve_with_wisdom',
    'PanWisdomResult',
    'WisdomSchool',
    'ProblemType',
    'preload_pan_wisdom',
    'is_pan_wisdom_ready',
    
    # 向后兼容 (V1.0 → V2.0)
    'WisdomTreeCore',
    'reason_with_wisdom_tree',
]
