# -*- coding: utf-8 -*-
"""藏书阁桥接模块测试"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.intelligence.dispatcher.wisdom_dispatch._library_bridge import (
    get_library_bridge,
    reset_library_bridge,
    LibraryBridge,
    BridgeConfig,
)

def test_roi_bridge():
    """测试ROI桥接"""
    reset_library_bridge()
    bridge = get_library_bridge()

    # 模拟ROI汇报
    record = bridge.report_roi(
        task_id="task_test_001",
        claw_name="孔子",
        efficiency=0.85,
        quality=0.90,
        satisfaction=0.75,
        roi_score=0.82,
    )

    print(f"[OK] report_roi: {record.id if record else 'None'}")

    # 查询验证
    results = bridge.query_roi_by_claw("孔子")
    print(f"[OK] query_roi_by_claw: {len(results)}条记录")

def test_learning_bridge():
    """测试学习桥接"""
    reset_library_bridge()
    bridge = get_library_bridge()

    record = bridge.report_learning(
        strategy_type="THREE_TIER",
        insight="发现新的推理模式",
        sage="孔子",
    )

    print(f"[OK] report_learning: {record.id if record else 'None'}")

def test_claw_bridge():
    """测试Claw桥接"""
    reset_library_bridge()
    bridge = get_library_bridge()

    record = bridge.report_claw_execution(
        claw_name="孔子",
        task="分析用户问题",
        result="完成分析",
        success=True,
        duration=1.5,
    )

    print(f"[OK] report_claw_execution: {record.id if record else 'None'}")

def test_research_bridge():
    """测试研究桥接"""
    reset_library_bridge()
    bridge = get_library_bridge()

    record = bridge.report_research(
        research_type="深度研究",
        finding="新的解决方案",
        depth="博士生级别",
    )

    print(f"[OK] report_research: {record.id if record else 'None'}")

def test_emotion_bridge():
    """测试情绪桥接"""
    reset_library_bridge()
    bridge = get_library_bridge()

    record = bridge.report_emotion(
        emotion_type="喜悦",
        pattern="任务成功触发",
        intensity=0.8,
    )

    print(f"[OK] report_emotion: {record.id if record else 'None'}")

def test_bridge_stats():
    """测试桥接统计"""
    reset_library_bridge()
    bridge = get_library_bridge()

    # 先触发一些汇报
    bridge.report_roi(
        task_id="task_001",
        claw_name="孔子",
        efficiency=0.8,
        quality=0.85,
    )

    stats = bridge.get_bridge_stats()
    print(f"[OK] get_bridge_stats: {len(stats['registered_bridges'])}个已注册桥接")

def test_bridge_config():
    """测试桥接配置"""
    print(f"[OK] ROI_CONFIG wing: {BridgeConfig.ROI_CONFIG['wing']}, source: {BridgeConfig.ROI_CONFIG['source']}")
    print(f"[OK] LEARNING_CONFIG wing: {BridgeConfig.LEARNING_CONFIG['wing']}, source: {BridgeConfig.LEARNING_CONFIG['source']}")
    print(f"[OK] NEURAL_MEMORY_CONFIG wing: {BridgeConfig.NEURAL_MEMORY_CONFIG['wing']}, source: {BridgeConfig.NEURAL_MEMORY_CONFIG['source']}")
    print(f"[OK] RESEARCH_CONFIG wing: {BridgeConfig.RESEARCH_CONFIG['wing']}, source: {BridgeConfig.RESEARCH_CONFIG['source']}")
    print(f"[OK] EMOTION_CONFIG wing: {BridgeConfig.EMOTION_CONFIG['wing']}, source: {BridgeConfig.EMOTION_CONFIG['source']}")

if __name__ == "__main__":
    print("=" * 50)
    print("藏书阁桥接模块测试")
    print("=" * 50)

    test_bridge_config()
    print()

    test_roi_bridge()
    test_learning_bridge()
    test_claw_bridge()
    test_research_bridge()
    test_emotion_bridge()
    test_bridge_stats()

    print()
    print("=" * 50)
    print("藏书阁桥接模块测试通过")
    print("=" * 50)
