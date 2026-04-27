#!/usr/bin/env python3
"""
神经网络布局全链路验证脚本

验证全局神经网络布局的完整性和连通性
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from src.neural_layout import (
    NetworkLayoutManager, GlobalNeuralBridge, get_global_neural_bridge,
    verify_network, visualize_network, NeuronType
)


def print_header(title: str):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_section(title: str):
    """打印小节标题"""
    print(f"\n📌 {title}")
    print("-" * 40)


def verify_neural_layout():
    """验证神经网络布局"""
    print_header("🧠 Somn 神经网络布局全链路验证")
    
    # 1. 初始化布局管理器
    print_section("初始化神经网络布局")
    layout_manager = NetworkLayoutManager()
    
    if not layout_manager.initialize_global_layout():
        print("❌ 布局初始化失败")
        return False
    
    print("✅ 神经网络布局初始化成功")
    
    # 2. 获取布局状态
    print_section("布局状态概览")
    status = layout_manager.get_layout_status()
    
    print(f"  初始化状态: {'✅ 已初始化' if status['initialized'] else '❌ 未初始化'}")
    print(f"  主链路节点: {status['main_chain_nodes']}")
    print(f"  智慧学派节点: {status['wisdom_nodes']}")
    print(f"  记忆系统节点: {status['memory_nodes']}")
    print(f"  自主系统节点: {status['autonomy_nodes']}")
    
    # 3. 网络拓扑
    print_section("网络拓扑结构")
    topology = status['network_topology']
    print(f"  神经元总数: {topology['neuron_count']}")
    print(f"  突触连接数: {topology['synapse_count']}")
    
    print("\n  神经元类型分布:")
    for neuron_type, count in topology['neurons_by_type'].items():
        if count > 0:
            print(f"    - {neuron_type}: {count}")
    
    # 4. 验证网络
    print_section("网络结构验证")
    verification = verify_network(layout_manager.network)
    
    print(f"  总体状态: {verification['overall_status']}")
    print(f"  问题总数: {verification['total_issues']}")
    print(f"\n  验证摘要: {verification['summary']}")
    
    # 详细验证结果
    print("\n  详细验证结果:")
    for check_name, check_result in verification['details'].items():
        status_icon = "✅" if check_result.get('passed', False) else "⚠️"
        print(f"    {status_icon} {check_name}: {'通过' if check_result.get('passed', False) else '需关注'}")
    
    # 5. 测试信号流动
    print_section("测试信号流动")
    test_input = {
        "query": "如何制定增长策略",
        "context": {"industry": "tech", "stage": "growth"}
    }
    
    activation_result = layout_manager.activate_main_chain(test_input)
    
    print(f"  发射信号数: {activation_result['signals_emitted']}")
    print(f"  通路步数: {len(activation_result['pathway'])}")
    
    # 显示通路
    print("\n  信号通路:")
    for i, step in enumerate(activation_result['pathway'][:5]):
        source = step.get('source', 'unknown')
        targets = step.get('targets', [])
        print(f"    {i+1}. {source} -> {', '.join(targets[:3])}")
    
    if len(activation_result['pathway']) > 5:
        print(f"    ... 还有 {len(activation_result['pathway']) - 5} 步")
    
    # 6. 测试全局桥梁
    print_section("测试全局神经桥梁")
    bridge = get_global_neural_bridge()
    
    if bridge.setup_global_bridge():
        print("✅ 全局桥梁设置成功")
        
        bridge_status = bridge.get_bridge_status()
        print(f"  已注册桥梁数: {bridge_status['bridges_registered']}")
        print(f"  桥梁列表: {', '.join(bridge_status['bridge_names'])}")
        
        # 测试处理
        print("\n  测试全链路处理:")
        result = bridge.process_through_network(test_input)
        print(f"    网络激活信号数: {result['network_activation']['signals_emitted']}")
        print(f"    模块输出数: {len(result['module_outputs'])}")
    else:
        print("❌ 全局桥梁设置失败")
    
    # 7. 生成可视化
    print_section("生成可视化")
    try:
        html = visualize_network(layout_manager.network)
        output_path = "neural_layout_visualization.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ 可视化已保存到: {output_path}")
    except Exception as e:
        print(f"⚠️ 可视化生成失败: {e}")
    
    # 8. 路径查找测试
    print_section("路径查找测试")
    path = layout_manager.find_optimal_path("AgentCore", "ROITracker")
    if path:
        print(f"  AgentCore -> ROITracker 路径:")
        print(f"    {' -> '.join(path[:5])}")
        if len(path) > 5:
            print(f"    ... 共 {len(path)} 个节点")
    else:
        print("  未找到路径")
    
    # 9. 最终总结
    print_header("验证总结")
    
    all_passed = verification['overall_status'] == "PASSED"
    
    if all_passed:
        print("✅ 神经网络布局验证通过！")
        print("\n  全链路状态: 已打通")
        print(f"  神经元总数: {topology['neuron_count']}")
        print(f"  突触连接数: {topology['synapse_count']}")
        print(f"  智慧学派数: {status['wisdom_nodes']}")
        print("\n  所有功能板块已部署在各自最合适的位置")
        print("  主链路已串联，形成神经网络状态布局")
    else:
        print("⚠️ 神经网络布局验证完成，但存在一些问题")
        print(f"\n  问题数: {verification['total_issues']}")
        print("  请查看详细验证结果")
    
    return all_passed


if __name__ == "__main__":
    try:
        success = verify_neural_layout()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 验证过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
