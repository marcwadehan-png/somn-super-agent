# -*- coding: utf-8 -*-
"""
推理引擎全局调度演示 v1.0 (2026-04-24)

展示如何通过UnifiedIntelligenceCoordinator全局调度三个新推理引擎。
"""

import time
from typing import Dict, Any

# ═══════════════════════════════════════════════════════════════════════════
# 1. 基础导入
# ═══════════════════════════════════════════════════════════════════════════

from src.intelligence.engines.unified_intelligence_coordinator import UnifiedIntelligenceCoordinator
from src.intelligence.engines.unified_intelligence_coordinator._unified_base import TaskType, TaskContext

# ═══════════════════════════════════════════════════════════════════════════
# 2. 模拟LLM函数（实际使用时替换为真实LLM调用）
# ═══════════════════════════════════════════════════════════════════════════

def mock_llm(prompt: str) -> str:
    """模拟LLM响应"""
    time.sleep(0.1)  # 模拟延迟
    return f"[模拟推理] 基于问题分析: {prompt[:80]}..."

# ═══════════════════════════════════════════════════════════════════════════
# 3. 全局调度器初始化
# ═══════════════════════════════════════════════════════════════════════════

def demo_global_dispatcher():
    """演示全局调度器"""
    print("=" * 60)
    print("推理引擎全局调度演示")
    print("=" * 60)
    
    # 初始化调度器
    uic = UnifiedIntelligenceCoordinator()
    
    # 创建测试上下文
    context = TaskContext(
        task_id='demo_001',
        task_type=TaskType.PROBLEM_SOLVING,
        priority=1,
        user_id='demo_user',
        session_id='demo_session'
    )
    
    # ════════════════════════════════════════════════════════════════════
    # 4. Long CoT引擎测试 - 深层逻辑分析
    # ════════════════════════════════════════════════════════════════════
    print("\n[1] Long CoT引擎 - 深层逻辑分析")
    print("-" * 40)
    
    result1 = uic._execute_module(
        'long_cot_reasoning',
        TaskType.PROBLEM_SOLVING,
        {
            'problem': '分析人工智能对就业市场的影响及其应对策略',
            'llm_callable': mock_llm
        },
        context
    )
    
    print(f"  结果键: {list(result1.keys())}")
    print(f"  推理步骤数: {len(result1.get('reasoning_trace', []))}")
    print(f"  检查点数: {len(result1.get('checkpoints', []))}")
    
    # ════════════════════════════════════════════════════════════════════
    # 5. ToT引擎测试 - 多方案比较
    # ════════════════════════════════════════════════════════════════════
    print("\n[2] ToT引擎 - 多路径探索")
    print("-" * 40)
    
    result2 = uic._execute_module(
        'tot_reasoning',
        TaskType.PROBLEM_SOLVING,
        {
            'problem': '选择最佳职业发展路径',
            'goal': '找到最优职业规划方案',
            'llm_callable': mock_llm
        },
        context
    )
    
    print(f"  结果键: {list(result2.keys())}")
    print(f"  解决方案: {result2.get('solution', 'N/A')[:50]}...")
    print(f"  树统计: {result2.get('tree_stats', {})}")
    
    # ════════════════════════════════════════════════════════════════════
    # 6. ReAct引擎测试 - 知识查询
    # ════════════════════════════════════════════════════════════════════
    print("\n[3] ReAct引擎 - 推理行动协同")
    print("-" * 40)
    
    result3 = uic._execute_module(
        'react_reasoning',
        TaskType.PROBLEM_SOLVING,
        {
            'problem': '计算 123 * 456 + 789 的值',
            'llm_callable': mock_llm
        },
        context
    )
    
    print(f"  结果键: {list(result3.keys())}")
    print(f"  成功: {result3.get('success', False)}")
    traj = result3.get('trajectory')
    if traj:
        print(f"  TAO步骤数: {len(traj.steps) if hasattr(traj, 'steps') else 1}")
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)

# ═══════════════════════════════════════════════════════════════════════════
# 7. 直接引擎调用演示
# ═══════════════════════════════════════════════════════════════════════════

def demo_direct_engine():
    """演示直接调用引擎"""
    print("\n\n" + "=" * 60)
    print("直接引擎调用演示")
    print("=" * 60)
    
    # 获取引擎实例
    uic = UnifiedIntelligenceCoordinator()
    
    long_cot = uic._get_module('long_cot_reasoning')
    tot = uic._get_module('tot_reasoning')
    react = uic._get_module('react_reasoning')
    
    print(f"\nLongCoT引擎: {type(long_cot).__name__}")
    print(f"ToT引擎: {type(tot).__name__}")
    print(f"ReAct引擎: {type(react).__name__}")
    
    # 直接调用reason方法
    print("\n[直接调用] LongCoT.reason()")
    result = long_cot.reason(
        problem="解释量子计算的基本原理",
        context={},
        llm_callable=mock_llm
    )
    print(f"  推理轨迹数: {len(result.get('reasoning_trace', []))}")
    print(f"  最终答案: {result.get('final_answer', '')[:50]}...")

# ═══════════════════════════════════════════════════════════════════════════
# 8. 主入口
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    demo_global_dispatcher()
    demo_direct_engine()
