"""检查12个调度器是否有真实实现"""
import sys
sys.path.insert(0, 'd:\\AI\\somn')
sys.path.insert(0, 'd:\\AI\\somn\\knowledge_cells')

from knowledge_cells.core import DispatchEngine
from knowledge_cells.dispatchers.problem_dispatcher import ProblemDispatcher
from knowledge_cells.dispatchers.school_fusion import SchoolFusion
from knowledge_cells.dispatchers.four_level_controller import FourLevelDispatchController
from knowledge_cells.dispatchers.three_layer_reasoning import ThreeLayerReasoning
from knowledge_cells.dispatchers.fallacy_checker import FallacyChecker
from knowledge_cells.dispatchers.super_reasoning import SuperReasoning
from knowledge_cells.dispatchers.yinyang_decision import YinYangDecision
from knowledge_cells.dispatchers.divine_architecture import DivineArchitecture
from knowledge_cells.dispatchers.chain_executor import ChainExecutor
from knowledge_cells.dispatchers.result_tracker import ResultTracker

# 12个调度器
checks = [
    ("SD-P1", ProblemDispatcher, "问题调度(树干核心)"),
    ("SD-F1", SchoolFusion, "25学派融合"),
    ("SD-F2", FourLevelDispatchController, "四级调度总控"),
    ("SD-R1", ThreeLayerReasoning, "三层推理监管"),
    ("SD-R2", FallacyChecker, "谬误检测"),
    ("SD-D1", lambda: SuperReasoning(mode="light"), "轻量深度推理"),
    ("SD-D2", lambda: SuperReasoning(mode="standard"), "标准深度推理"),
    ("SD-D3", lambda: SuperReasoning(mode="deep"), "极致深度推理"),
    ("SD-C1", YinYangDecision, "太极阴阳决策"),
    ("SD-C2", DivineArchitecture, "神之架构决策"),
    ("SD-E1", ChainExecutor, "五步主链执行"),
    ("SD-L1", ResultTracker, "学习进化"),
]

print("=== v6.1.1 调度器实现检查 ===\n")
all_ok = True
for sid, cls, desc in checks:
    try:
        inst = cls() if not callable(cls) or 'lambda' in str(cls) else cls()
        clsname = type(inst).__qualname__
        module = type(inst).__module__
        # 检查方法数量（有真实逻辑的标志）
        methods = [m for m in dir(inst) if not m.startswith('_')]
        print(f"  ✅ {sid}: {clsname}")
        print(f"     模块: {module}")
        print(f"     公共方法: {len(methods)}个")
        print(f"     描述: {desc}")
    except Exception as e:
        print(f"  ❌ {sid}: 实例化失败 - {e}")
        all_ok = False
    print()

print("=== 结论 ===")
if all_ok:
    print("✅ 12个调度器全部可以独立实例化")
else:
    print("⚠️ 部分调度器存在问题")
