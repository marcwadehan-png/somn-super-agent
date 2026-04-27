"""
__all__ = [
    'probe_class_methods',
    'probe_module_exports',
]

自动探查所有模块的真实API签名
用法:python smart_office_assistant/src/api_probe.py > smart_office_assistant/data/api_probe_results.txt 2>&1
"""

from __future__ import annotations

import sys
import os
import io
import traceback
import glob
import inspect
from pathlib import Path
from typing import List, Optional, Tuple, Union

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def probe_class_methods(module_path: str, class_name: str) -> List[str]:
    """探查一个类的所有公共方法签名"""
    try:
        mod = __import__(module_path, fromlist=[class_name])
        cls = getattr(mod, class_name)
        methods: List[str] = []
        for name in dir(cls):
            if not name.startswith('_'):
                attr = getattr(cls, name)
                if callable(attr):
                    # Try to get signature
                    try:
                        sig = inspect.signature(attr)
                        methods.append(f"  {name}{sig}")
                    except Exception:
                        methods.append(f"  {name}(...)")
        return methods
    except Exception as e:
        return [f"  ERROR: {e}"]


def probe_module_exports(module_path: str) -> List[str]:
    """探查一个模块的所有导出"""
    try:
        mod = __import__(module_path, fromlist=['*'])
        exports: List[str] = []
        for name in dir(mod):
            if not name.startswith('_'):
                attr = getattr(mod, name)
                if isinstance(attr, type):
                    exports.append(f"  class {name}")
                elif callable(attr):
                    try:
                        sig = inspect.signature(attr)
                        exports.append(f"  def {name}{sig}")
                    except Exception:
                        exports.append(f"  def {name}(...)")
        return exports
    except Exception as e:
        return [f"  ERROR: {e}"]

# Type alias for probe items
ProbeItem = Tuple[str, Optional[str]]
ProbesDict = dict[str, List[ProbeItem]]


# === 探查列表 ===
probes: ProbesDict = {
    "=== AUTONOMOUS CORE ===": [
        ("src.autonomous_core.state_manager", "StateManager"),
        ("src.autonomous_core.value_system", "ValueSystem"),
        ("src.autonomous_core.autonomous_scheduler", "AutonomousScheduler"),
    ],
    "=== WISDOM ENGINES ===": [
        ("src.intelligence.ru_wisdom_core", "RuWisdomCore"),
        ("src.intelligence.dao_wisdom_core", "DaoWisdomCore"),
        ("src.intelligence.sufu_wisdom_core", "SufuWisdomCore"),
        ("src.intelligence.military_strategy_engine", "MilitaryStrategyEngine"),
        ("src.intelligence.lvshi_wisdom_engine", "LvShiWisdomEngine"),
        ("src.intelligence.hongming_wisdom_core", "HongMingWisdomCore"),
        ("src.intelligence.mythology_wisdom_engine", "MythologyWisdomEngine"),
        ("src.intelligence.literary_narrative_engine", "LiteraryNarrativeEngine"),
        ("src.intelligence.metaphysics_wisdom_unified", "MetaphysicsWisdomUnified"),
        ("src.intelligence.thinking_growth_unified", "ThinkingGrowthUnifiedSystem"),
        ("src.intelligence.marvel_wisdom_unified", "MarvelWisdomUnified"),
        ("src.intelligence.yangming_xinxue_engine", "YangmingXinxueEngine"),
        ("src.intelligence.civilization_wisdom_core", "CivilizationWisdomCore"),
        ("src.intelligence.behavior_shaping_engine", "BehaviorShapingEngine"),
        ("src.intelligence.anthropology_wisdom_engine", "AnthropologyWisdomEngine"),
    ],
    "=== NEURAL MEMORY ===": [
        ("src.neural_memory.neural_memory_system_v3", None),  # probe module
        ("src.neural_memory.hebbian_learning_engine", "HebbianLearningEngine"),
        ("src.neural_memory.memory_encoding_system_v31", "MemoryEncodingSystemV31"),
        ("src.neural_memory.learning_engine", "LearningEngine"),
    ],
    "=== DEEP REASONING ===": [
        ("src.intelligence.deep_reasoning_engine", "DeepReasoningEngine"),
        ("src.intelligence.enhanced_reasoning_engine", None),  # probe module for class names
        ("src.intelligence.wisdom_reasoning_engine", "WisdomReasoningEngine"),
    ],
    "=== CORE SYSTEMS ===": [
        ("src.intelligence.unified_intelligence_coordinator", "UnifiedIntelligenceCoordinator"),
        ("src.intelligence.supreme_decision_fusion_engine", "SupremeDecisionFusionEngine"),
    ],
    "=== GROWTH / KNOWLEDGE / LEARNING ===": [
        ("src.intelligence.super_learning_engine", "SuperLearningEngine"),
    ],
}

for section, items in probes.items():
    print(f"\n{'='*60}")
    print(section)
    print('='*60)
    for mod_path, cls_name in items:
        print(f"\n[{mod_path}]")
        if cls_name:
            print(f"  class: {cls_name}")
            methods = probe_class_methods(mod_path, cls_name)
        else:
            print(f"  (module probe)")
            methods = probe_module_exports(mod_path)
        for m in methods:
            print(m)

# 额外探查:实际存在的模块路径
print(f"\n{'='*60}")
print("=== PATH CHECKS ===")
print('='*60)
paths_to_check = [
    "src.growth_engine.growth_solution_engine",
    "src.growth_engine",
    "src.knowledge_graph.graph_engine",
    "src.learning.three_tier_learning",
    "src.learning.enhanced_three_tier_learning",
    "src.neural_memory.memory_encoding_system_v3",
]
for p in paths_to_check:
    try:
        __import__(p)
        print(f"  OK: {p}")
    except ImportError as e:
        print(f"  MISSING: {p} -> {e}")

# 查找实际growth engine路径
print(f"\n=== GROWTH ENGINE ACTUAL PATH ===")
growth_dir = Path("src/growth_engine") if Path("src/growth_engine").exists() else None
if growth_dir:
    print(f"  Directory exists: {growth_dir}")
    for f in sorted(growth_dir.glob("*.py")):
        print(f"    - {f.name}")
else:
    # 搜索
    import glob
    matches = glob.glob("src/**/growth*.py", recursive=True)
    for m in matches:
        print(f"    Found: {m}")
    if not matches:
        matches = glob.glob("src/**/*solution*.py", recursive=True)
        for m in matches:
            print(f"    Found solution: {m}")

# 查找实际knowledge graph路径
print(f"\n=== KNOWLEDGE GRAPH ACTUAL PATH ===")
kg_dir = Path("src/knowledge_graph") if Path("src/knowledge_graph").exists() else None
if kg_dir:
    print(f"  Directory exists: {kg_dir}")
    for f in sorted(kg_dir.glob("*.py")):
        print(f"    - {f.name}")

# 查找实际learning路径
print(f"\n=== LEARNING ACTUAL PATH ===")
learn_dir = Path("src/learning") if Path("src/learning").exists() else None
if learn_dir:
    print(f"  Directory exists: {learn_dir}")
    for f in sorted(learn_dir.glob("*.py")):
        print(f"    - {f.name}")

# 检查 DaoDeJingCore 的问题
print(f"\n=== DING DE JING CORE CHECK ===")
try:
    from src.intelligence.dao_wisdom_core import DaoDeJingCore
    attrs = [a for a in dir(DaoDeJingCore) if 'CHAPTER' in a.upper() or a.startswith('_CH')]
    print(f"  DaoDeJingCore found. CHAPTER attrs: {attrs[:10]}")
except Exception as e:
    print(f"  Error: {e}")

# 检查 TopThinkingEngine
print(f"\n=== TOP THINKING ENGINE CHECK ===")
try:
    mod = __import__("src.intelligence.top_thinking_engine", fromlist=['*'])
    classes = [a for a in dir(mod) if isinstance(getattr(mod, a), type)]
    print(f"  Available classes: {classes}")
except Exception as e:
    print(f"  Error: {e}")

print("\n=== PROBE COMPLETE ===")
