# -*- coding: utf-8 -*-
"""
逻辑推理引擎性能基准测试 v1.0

测试四个推理引擎的性能：
- LongCoT: 长思维链推理
- ToT: 树状推理
- GoT: 图推理
- ReAct: 协同推理

作者: Somn AI
版本: V1.0.0
日期: 2026-04-24
"""

import sys
import os
import time
import json
from typing import Dict, List, Any

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def format_time(seconds: float) -> str:
    """格式化时间"""
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f}μs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.2f}s"


def format_size(bytes_size: int) -> str:
    """格式化字节大小"""
    if bytes_size < 1024:
        return f"{bytes_size}B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.2f}KB"
    else:
        return f"{bytes_size / 1024 / 1024:.2f}MB"


# ═══════════════════════════════════════════════════════════════════════════════
# 模拟LLM函数
# ═══════════════════════════════════════════════════════════════════════════════

def mock_llm(prompt: str) -> str:
    """模拟LLM响应"""
    # 模拟token生成延迟
    time.sleep(0.001)
    
    if "分析" in prompt or "推理" in prompt:
        return "基于问题的深入分析，我得出以下结论：这是一个需要系统性思考的复杂问题。"
    elif "选择" in prompt or "方案" in prompt:
        return "经过多路径探索，最优方案是方案B，因为它在成本和效果之间取得了最佳平衡。"
    elif "图" in prompt or "关系" in prompt:
        return "通过图网络推理，发现节点A、B、C之间存在强关联关系。"
    else:
        return "[模拟推理响应] 系统分析完成，建议继续深入研究。"


# ═══════════════════════════════════════════════════════════════════════════════
# 基准测试用例
# ═══════════════════════════════════════════════════════════════════════════════

BENCHMARK_CASES = {
    "simple": {
        "description": "简单问题（短文本）",
        "problem": "1+1等于几？",
        "iterations": 10
    },
    "medium": {
        "description": "中等复杂度问题",
        "problem": "分析一家互联网公司的增长策略，包括用户获取、留存和变现三个维度。",
        "iterations": 5
    },
    "complex": {
        "description": "复杂多步骤推理",
        "problem": "深入分析当前经济形势下，中小企业数字化转型的挑战与机遇，需要考虑资金、技术、人才、市场等多方面因素。",
        "iterations": 3
    },
    "selection": {
        "description": "方案选择问题",
        "problem": "公司在考虑三个扩张方案：方案A是进入一线城市，方案B是深耕二三线城市，方案C是专注细分市场。请分析各方案的优劣势。",
        "iterations": 3
    },
    "graph": {
        "description": "图推理问题",
        "problem": "分析供应链网络中各节点之间的依赖关系和传导路径。",
        "iterations": 3
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# LongCoT基准测试
# ═══════════════════════════════════════════════════════════════════════════════

def benchmark_long_cot(iterations: int = 5) -> Dict[str, Any]:
    """LongCoT基准测试"""
    results = {
        "engine": "LongCoT",
        "tests": [],
        "summary": {}
    }
    
    try:
        from src.intelligence.reasoning._long_cot_engine import LongCoTReasoningEngine, LongCoTConfig
        
        config = LongCoTConfig(
            max_thinking_length=512,
            boundary_threshold=0.8,
            checkpoint_interval=64,
            enable_insight_detection=True,
            enable_self_correction=False
        )
        engine = LongCoTReasoningEngine(config)
        
        times = []
        for i in range(iterations):
            problem = f"分析这个问题并给出深入解答（第{i+1}次测试）"
            
            start = time.perf_counter()
            result = engine.reason(problem, {}, mock_llm)
            elapsed = time.perf_counter() - start
            
            times.append(elapsed)
        
        results["tests"] = [{
            "name": f"LongCoT_{i+1}",
            "time": t,
            "time_formatted": format_time(t)
        } for i, t in enumerate(times)]
        
        results["summary"] = {
            "count": len(times),
            "total_time": sum(times),
            "avg_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "avg_formatted": format_time(sum(times) / len(times))
        }
        
    except ImportError as e:
        results["error"] = f"导入失败: {e}"
    except Exception as e:
        results["error"] = str(e)
    
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# ToT基准测试
# ═══════════════════════════════════════════════════════════════════════════════

def benchmark_tot(iterations: int = 5) -> Dict[str, Any]:
    """ToT基准测试"""
    results = {
        "engine": "ToT",
        "tests": [],
        "summary": {}
    }
    
    try:
        from src.intelligence.reasoning._tot_engine import TreeOfThoughtsEngine, TreeOfThoughtsConfig
        
        config = TreeOfThoughtsConfig(
            max_depth=3,
            branching_factor=2,
            max_iterations=10,
            pruning_threshold=0.3
        )
        engine = TreeOfThoughtsEngine(config)
        
        times = []
        for i in range(iterations):
            problem = f"比较两个方案的优劣（第{i+1}次测试）"
            
            start = time.perf_counter()
            result = engine.solve(problem, None, max_iterations=10, goal=None, llm_callable=mock_llm)
            elapsed = time.perf_counter() - start
            
            times.append(elapsed)
        
        results["tests"] = [{
            "name": f"ToT_{i+1}",
            "time": t,
            "time_formatted": format_time(t)
        } for i, t in enumerate(times)]
        
        results["summary"] = {
            "count": len(times),
            "total_time": sum(times),
            "avg_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "avg_formatted": format_time(sum(times) / len(times))
        }
        
    except ImportError as e:
        results["error"] = f"导入失败: {e}"
    except Exception as e:
        results["error"] = str(e)
    
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# GoT基准测试
# ═══════════════════════════════════════════════════════════════════════════════

def benchmark_got(iterations: int = 5) -> Dict[str, Any]:
    """GoT基准测试"""
    results = {
        "engine": "GoT",
        "tests": [],
        "summary": {}
    }
    
    try:
        from src.intelligence.reasoning._got_engine import GraphOfThoughtsEngine, GoTConfig
        
        config = GoTConfig(
            max_nodes=50,
            max_depth=5,
            max_children=3,
            enable_attention=True,
            search_strategy="best"
        )
        engine = GraphOfThoughtsEngine(config)
        
        times = []
        for i in range(iterations):
            problem = f"分析节点间关系网络（第{i+1}次测试）"
            
            start = time.perf_counter()
            result = engine.solve(problem, reasoning_mode="hybrid", llm_callable=mock_llm)
            elapsed = time.perf_counter() - start
            
            times.append(elapsed)
        
        results["tests"] = [{
            "name": f"GoT_{i+1}",
            "time": t,
            "time_formatted": format_time(t)
        } for i, t in enumerate(times)]
        
        results["summary"] = {
            "count": len(times),
            "total_time": sum(times),
            "avg_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "avg_formatted": format_time(sum(times) / len(times))
        }
        
    except ImportError as e:
        results["error"] = f"导入失败: {e}"
    except Exception as e:
        results["error"] = str(e)
    
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# ReAct基准测试
# ═══════════════════════════════════════════════════════════════════════════════

def benchmark_react(iterations: int = 5) -> Dict[str, Any]:
    """ReAct基准测试"""
    results = {
        "engine": "ReAct",
        "tests": [],
        "summary": {}
    }
    
    try:
        from src.intelligence.reasoning._react_engine import (
            ReActEngine, ReActConfig, ToolRegistry,
            SearchTool, CalculatorTool, LookupTool
        )
        from src.intelligence.reasoning._react_extended_tools import get_extended_tools
        
        # 创建配置
        config = ReActConfig(
            max_iterations=5,
            max_consecutive_failures=3,
            enable_context_summary=False
        )
        
        # 创建引擎
        engine = ReActEngine(config)
        
        # 注册工具
        engine.tool_registry.register(SearchTool(lambda q, n: [{"title": "结果", "snippet": "搜索结果"}]))
        engine.tool_registry.register(CalculatorTool())
        engine.tool_registry.register(LookupTool(lambda e: {"entity": e, "data": "知识"}))
        
        # 注册扩展工具
        extended_tools = get_extended_tools()
        for tool in extended_tools[:3]:  # 只注册前3个扩展工具
            engine.tool_registry.register(tool)
        
        times = []
        for i in range(iterations):
            problem = f"查询相关信息并计算数据（第{i+1}次测试）"
            
            start = time.perf_counter()
            result = engine.reason(problem, {}, mock_llm)
            elapsed = time.perf_counter() - start
            
            times.append(elapsed)
        
        results["tests"] = [{
            "name": f"ReAct_{i+1}",
            "time": t,
            "time_formatted": format_time(t)
        } for i, t in enumerate(times)]
        
        results["summary"] = {
            "count": len(times),
            "total_time": sum(times),
            "avg_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "avg_formatted": format_time(sum(times) / len(times)),
            "tools_registered": len(engine.tool_registry.list_tools())
        }
        
    except ImportError as e:
        results["error"] = f"导入失败: {e}"
    except Exception as e:
        results["error"] = str(e)
    
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# 全局调度基准测试
# ═══════════════════════════════════════════════════════════════════════════════

def benchmark_uic(iterations: int = 5) -> Dict[str, Any]:
    """UnifiedIntelligenceCoordinator基准测试"""
    results = {
        "engine": "UIC",
        "tests": [],
        "summary": {}
    }
    
    try:
        from src.intelligence.engines.unified_intelligence_coordinator import UnifiedIntelligenceCoordinator
        
        coordinator = UnifiedIntelligenceCoordinator()
        
        times = []
        for i in range(iterations):
            problem = "分析市场趋势并给出建议"
            
            start = time.perf_counter()
            result = coordinator.execute_task("tier3_analysis", {"problem": problem}, None)
            elapsed = time.perf_counter() - start
            
            times.append(elapsed)
        
        results["tests"] = [{
            "name": f"UIC_{i+1}",
            "time": t,
            "time_formatted": format_time(t)
        } for i, t in enumerate(times)]
        
        results["summary"] = {
            "count": len(times),
            "total_time": sum(times),
            "avg_time": sum(times) / len(times),
            "min_time": min(times),
            "max_time": max(times),
            "avg_formatted": format_time(sum(times) / len(times)),
            "modules_loaded": len(coordinator.modules)
        }
        
    except ImportError as e:
        results["error"] = f"导入失败: {e}"
    except Exception as e:
        results["error"] = str(e)
    
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════════════════════════

def run_benchmark():
    """运行完整基准测试"""
    print("=" * 80)
    print("逻辑推理引擎性能基准测试 v1.0.0".center(70))
    print("=" * 80)
    print()
    
    all_results = {}
    
    # 1. LongCoT测试
    print("[1/5] 测试 LongCoT 长思维链推理引擎...")
    result = benchmark_long_cot(iterations=5)
    all_results["long_cot"] = result
    if "error" in result:
        print(f"    错误: {result['error']}")
    else:
        print(f"    平均耗时: {result['summary']['avg_formatted']}")
    print()
    
    # 2. ToT测试
    print("[2/5] 测试 ToT 树状推理引擎...")
    result = benchmark_tot(iterations=5)
    all_results["tot"] = result
    if "error" in result:
        print(f"    错误: {result['error']}")
    else:
        print(f"    平均耗时: {result['summary']['avg_formatted']}")
    print()
    
    # 3. GoT测试
    print("[3/5] 测试 GoT 图推理引擎...")
    result = benchmark_got(iterations=5)
    all_results["got"] = result
    if "error" in result:
        print(f"    错误: {result['error']}")
    else:
        print(f"    平均耗时: {result['summary']['avg_formatted']}")
    print()
    
    # 4. ReAct测试
    print("[4/5] 测试 ReAct 协同推理引擎...")
    result = benchmark_react(iterations=5)
    all_results["react"] = result
    if "error" in result:
        print(f"    错误: {result['error']}")
    else:
        tools_count = result['summary'].get('tools_registered', 0)
        print(f"    平均耗时: {result['summary']['avg_formatted']}, 工具数: {tools_count}")
    print()
    
    # 5. UIC测试
    print("[5/5] 测试 UnifiedIntelligenceCoordinator 全局调度...")
    result = benchmark_uic(iterations=5)
    all_results["uic"] = result
    if "error" in result:
        print(f"    错误: {result['error']}")
    else:
        modules = result['summary'].get('modules_loaded', 0)
        print(f"    平均耗时: {result['summary']['avg_formatted']}, 模块数: {modules}")
    print()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # 输出汇总
    # ═══════════════════════════════════════════════════════════════════════════
    
    print("=" * 80)
    print("基准测试汇总".center(70))
    print("=" * 80)
    print()
    
    print(f"{'引擎':<15} {'平均耗时':<15} {'最小':<15} {'最大':<15} {'状态':<10}")
    print("-" * 70)
    
    engine_order = ["long_cot", "tot", "got", "react", "uic"]
    engine_names = {
        "long_cot": "LongCoT",
        "tot": "TreeOfThoughts",
        "got": "GraphOfThoughts",
        "react": "ReAct",
        "uic": "UIC"
    }
    
    for key in engine_order:
        result = all_results.get(key, {})
        if "error" in result:
            status = "失败"
            avg = "-"
            min_t = "-"
            max_t = "-"
        else:
            status = "通过"
            summary = result.get("summary", {})
            avg = summary.get("avg_formatted", "-")
            min_t = format_time(summary.get("min_time", 0))
            max_t = format_time(summary.get("max_time", 0))
        
        name = engine_names.get(key, key)
        print(f"{name:<15} {avg:<15} {min_t:<15} {max_t:<15} {status:<10}")
    
    print()
    print("=" * 80)
    print("测试完成".center(70))
    print("=" * 80)
    
    return all_results


if __name__ == "__main__":
    results = run_benchmark()
