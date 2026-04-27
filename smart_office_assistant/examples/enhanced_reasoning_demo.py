# -*- coding: utf-8 -*-
"""
推理引擎使用示例
Demonstrates usage of Long CoT, ToT, and ReAct reasoning engines

作者: Somn AI
版本: V1.0.0
日期: 2026-04-24
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 模拟LLM调用（实际使用时替换为真实的LLM API调用）
def mock_llm(prompt: str) -> str:
    """模拟LLM调用"""
    # 这里应该是真实的LLM API调用
    # 例如: return openai.Completion.create(prompt=prompt, model="gpt-4").choices[0].text
    return f"[模拟响应] 基于问题: {prompt[:100]}... 的分析回答"


def example_long_cot():
    """Long CoT推理引擎示例"""
    print("\n" + "=" * 60)
    print("Long CoT推理引擎示例")
    print("=" * 60)
    
    from src.intelligence.reasoning._long_cot_engine import (
        LongCoTReasoningEngine,
        LongCoTConfig,
        get_long_cot_engine,
        reason_with_long_cot,
        InsightType
    )
    
    # 创建配置
    config = LongCoTConfig(
        max_thinking_length=1024,
        boundary_threshold=0.8,
        checkpoint_interval=64,
        enable_insight_detection=True,
        enable_self_correction=True,
        max_corrections=2
    )
    
    # 创建引擎
    engine = LongCoTReasoningEngine(
        llm_callable=mock_llm,
        config=config
    )
    
    print(f"\n引擎版本: {engine.VERSION}")
    print(f"配置: 最大推理长度={config.max_thinking_length}, 边界阈值={config.boundary_threshold}")
    
    # 执行推理
    problem = "分析一家互联网公司如何提高用户留存率，需要考虑产品、运营、技术等多个维度。"
    
    print(f"\n问题: {problem}")
    print("\n开始推理...")
    
    result = engine.reason(problem, llm_callable=mock_llm)
    
    # 输出结果
    print(f"\n推理完成!")
    print(f"  - 推理步骤数: {len(result['reasoning_trace'])}")
    print(f"  - 检查点数: {len(result['checkpoints'])}")
    print(f"  - 顿悟时刻: {len(result['insights'])}")
    print(f"  - 自我纠错: {len(result['corrections'])}")
    print(f"  - 思考长度: {result['metadata']['thinking_length']} tokens")
    
    # 统计信息
    stats = engine.get_stats()
    print(f"\n统计信息:")
    print(f"  - 总推理次数: {stats['total_reasoning_count']}")
    print(f"  - 边界检测次数: {stats['boundary_detections']}")
    print(f"  - 检测到的顿悟: {stats['insights_detected']}")
    print(f"  - 自我纠错次数: {stats['self_corrections']}")
    print(f"  - 平均思考长度: {stats['average_thinking_length']:.1f} tokens")


def example_tot():
    """ToT树推理引擎示例"""
    print("\n" + "=" * 60)
    print("ToT树推理引擎示例")
    print("=" * 60)
    
    from src.intelligence.reasoning._tot_engine import (
        TreeOfThoughtsEngine,
        ToTConfig,
        SearchStrategy,
        create_tot_engine,
        solve_with_tot,
        ThoughtTree,
        ThoughtTreeNode
    )
    
    # 创建配置
    config = ToTConfig(
        max_depth=4,
        branching_factor=3,
        pruning_threshold=0.3,
        strategy=SearchStrategy.BEST_FIRST
    )
    
    # 创建引擎
    engine = TreeOfThoughtsEngine(
        llm_callable=mock_llm,
        config=config
    )
    
    print(f"\n引擎版本: {engine.VERSION}")
    print(f"配置: 最大深度={config.max_depth}, 分支因子={config.branching_factor}")
    print(f"搜索策略: {config.strategy.value}")
    
    # 执行搜索
    problem = "制定一个用户增长策略，考虑渠道、内容、活动等多个方面。"
    
    print(f"\n问题: {problem}")
    print("\n开始树搜索...")
    
    result = engine.solve(problem, llm_callable=mock_llm)
    
    # 输出结果
    print(f"\n搜索完成!")
    print(f"  - 解决方案: {result['solution'][:100]}..." if len(result['solution']) > 100 else f"  - 解决方案: {result['solution']}")
    print(f"  - 树节点数: {result['tree_stats']['total_nodes']}")
    print(f"  - 树深度: {result['tree_stats']['depth']}")
    print(f"  - 迭代次数: {result['metadata']['iterations']}")
    
    # 遍历树结构
    if 'tree' in result:
        tree = result['tree']
        print(f"\n树结构统计:")
        for status, count in result['tree_stats']['status_counts'].items():
            if count > 0:
                print(f"  - {status}: {count}")
    
    # 测试不同搜索策略
    print("\n测试不同搜索策略:")
    for strategy in [SearchStrategy.BFS, SearchStrategy.DFS, SearchStrategy.BEAM]:
        engine.set_strategy(strategy)
        result = engine.solve(problem[:50], llm_callable=mock_llm)
        print(f"  - {strategy.value}: 节点数={result['tree_stats']['total_nodes']}")


def example_react():
    """ReAct推理引擎示例"""
    print("\n" + "=" * 60)
    print("ReAct推理引擎示例")
    print("=" * 60)
    
    from src.intelligence.reasoning._react_engine import (
        ReActEngine,
        ReActConfig,
        SearchTool,
        CalculatorTool,
        LookupTool,
        create_react_engine,
        reason_with_react,
        ToolRegistry,
        ToolExecutor
    )
    
    # 创建工具
    def mock_search(query: str, max_results: int = 5):
        """模拟搜索工具"""
        return [
            {"title": f"关于{query}的文章{i}", "url": f"http://example.com/{i}", "snippet": f"这是关于{query}的内容{i}"}
            for i in range(max_results)
        ]
    
    def mock_lookup(entity: str):
        """模拟查询工具"""
        return {
            "entity": entity,
            "description": f"{entity}的相关信息",
            "facts": ["事实1", "事实2"]
        }
    
    tools = [
        SearchTool(search_func=mock_search),
        CalculatorTool(),
        LookupTool(lookup_func=mock_lookup)
    ]
    
    # 创建配置
    config = ReActConfig(
        max_iterations=8,
        enable_context_summary=True
    )
    
    # 创建引擎
    engine = ReActEngine(
        llm_callable=mock_llm,
        config=config,
        tools=tools
    )
    
    print(f"\n引擎版本: {engine.VERSION}")
    print(f"配置: 最大迭代={config.max_iterations}")
    print(f"已注册工具: {[t.name for t in tools]}")
    
    # 执行推理
    problem = "查找最新的AI发展趋势，并计算相关投资回报率。"
    
    print(f"\n问题: {problem}")
    print("\n开始ReAct推理...")
    
    result = engine.reason(problem, llm_callable=mock_llm)
    
    # 输出结果
    print(f"\n推理完成!")
    print(f"  - 状态: {result['status']}")
    print(f"  - 最终答案: {result['final_answer'][:100]}..." if len(result['final_answer']) > 100 else f"  - 最终答案: {result['final_answer']}")
    print(f"  - 迭代次数: {result['metadata']['iterations']}")
    print(f"  - 行动次数: {result['metadata']['total_actions']}")
    print(f"  - 执行时间: {result['metadata']['execution_time']:.2f}s")
    
    # 显示轨迹
    trajectory = result['trajectory']
    print(f"\n推理轨迹 ({trajectory.get_summary()}):")
    for step in trajectory.steps[:5]:  # 显示前5步
        print(f"  [{step.step_type}] {step.content[:60]}...")
    
    # 统计信息
    stats = engine.get_stats()
    print(f"\n统计信息:")
    print(f"  - 总运行次数: {stats['total_runs']}")
    print(f"  - 成功率: {stats['successful_runs']/max(stats['total_runs'], 1)*100:.1f}%")
    print(f"  - 平均迭代: {stats['average_iterations']:.1f}")
    print(f"  - 工具使用: {stats['tool_usage']}")


def example_unified():
    """统一推理协调器示例"""
    print("\n" + "=" * 60)
    print("统一推理协调器示例")
    print("=" * 60)
    
    from src.intelligence.reasoning._long_cot_engine import LongCoTReasoningEngine
    from src.intelligence.reasoning._tot_engine import TreeOfThoughtsEngine, SearchStrategy
    from src.intelligence.reasoning._react_engine import ReActEngine, ReActConfig, SearchTool
    
    # 根据问题复杂度选择推理引擎
    def choose_engine(problem: str):
        """根据问题选择合适的推理引擎"""
        # 简单问题 -> Long CoT
        if len(problem) < 50:
            return "long_cot"
        
        # 需要外部知识 -> ReAct
        knowledge_keywords = ["查找", "搜索", "查询", "最新", "今天的"]
        if any(kw in problem for kw in knowledge_keywords):
            return "react"
        
        # 复杂多路径问题 -> ToT
        complex_keywords = ["策略", "方案", "规划", "多个", "考虑"]
        if any(kw in problem for kw in complex_keywords):
            return "tot"
        
        # 默认 -> Long CoT
        return "long_cot"
    
    # 测试用例
    test_cases = [
        ("解释量子计算的基本原理", "long_cot"),
        ("查找2024年AI领域的最新进展", "react"),
        ("制定一个用户留存优化方案，考虑产品、运营、技术三个维度", "tot"),
    ]
    
    print("\n根据问题类型自动选择推理引擎:")
    
    for problem, expected in test_cases:
        selected = choose_engine(problem)
        status = "✓" if selected == expected else "○"
        print(f"  {status} 问题: {problem[:40]}...")
        print(f"    -> 选择引擎: {selected}")
        print()


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Somn 推理引擎演示")
    print("=" * 60)
    
    try:
        example_long_cot()
        example_tot()
        example_react()
        example_unified()
        
        print("\n" + "=" * 60)
        print("演示完成!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n导入错误: {e}")
        print("请确保所有依赖模块已正确安装。")
    except Exception as e:
        print(f"\n执行错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
