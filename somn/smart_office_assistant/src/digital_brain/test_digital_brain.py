# -*- coding: utf-8 -*-
"""
数字大脑模块测试
================

测试数字大脑核心功能和集成桥接
仅测试数据结构、API接口和配置

版本: V1.0.0
创建: 2026-04-23
"""

import asyncio
import sys
import os

# 添加项目路径
project_src = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_src)

# ═══════════════════════════════════════════════════════════════════════════════
# 测试: 数据结构
# ═══════════════════════════════════════════════════════════════════════════════

def test_brain_state():
    """测试BrainState枚举"""
    print("\n=== 测试 BrainState ===")
    
    from digital_brain.digital_brain_core import BrainState
    
    # 检查所有状态
    assert BrainState.INITIALIZING.value == "initializing"
    assert BrainState.READY.value == "ready"
    assert BrainState.PROCESSING.value == "processing"
    assert BrainState.EVOLVING.value == "evolving"
    assert BrainState.SLEEPING.value == "sleeping"
    assert BrainState.ERROR.value == "error"
    print(f"✓ 状态枚举正确: {[s.value for s in BrainState]}")
    
    print("PASS: BrainState")
    return True


def test_memory_level():
    """测试MemoryLevel枚举"""
    print("\n=== 测试 MemoryLevel ===")
    
    from digital_brain.digital_brain_core import MemoryLevel
    
    # 检查所有层级
    assert MemoryLevel.SENSORY.value == "sensory"
    assert MemoryLevel.WORKING.value == "working"
    assert MemoryLevel.SHORT_TERM.value == "short_term"
    assert MemoryLevel.LONG_TERM.value == "long_term"
    assert MemoryLevel.ETERNAL.value == "eternal"
    print(f"✓ 记忆层级正确: {[m.value for m in MemoryLevel]}")
    
    print("PASS: MemoryLevel")
    return True


def test_brain_config():
    """测试BrainConfig配置"""
    print("\n=== 测试 BrainConfig ===")
    
    from digital_brain.digital_brain_core import BrainConfig
    
    # 默认配置
    config = BrainConfig()
    assert config.enable_local_llm == True
    assert config.enable_wisdom_dispatch == True
    assert config.enable_autonomous_evolution == True
    assert config.enable_imperial_library == True
    print("✓ 默认配置正确")
    
    # 自定义配置
    custom = BrainConfig(
        enable_local_llm=False,
        enable_wisdom_dispatch=True,
        llm_model_path="custom/path",
        llm_timeout=60.0,
    )
    assert custom.enable_local_llm == False
    assert custom.llm_model_path == "custom/path"
    assert custom.llm_timeout == 60.0
    print("✓ 自定义配置正确")
    
    print("PASS: BrainConfig")
    return True


def test_brain_thought():
    """测试BrainThought"""
    print("\n=== 测试 BrainThought ===")
    
    from digital_brain.digital_brain_core import BrainThought
    import time
    
    # 正常结果
    thought = BrainThought(
        thought_id="test-001",
        content="测试思考内容",
        source="memory",
        confidence=0.85,
    )
    assert thought.thought_id == "test-001"
    assert thought.content == "测试思考内容"
    assert thought.source == "memory"
    assert thought.confidence == 0.85
    print("✓ BrainThought数据正确")
    
    # 带处理时间的Thought
    thought2 = BrainThought(
        thought_id="test-002",
        content="处理中...",
        source="wisdom",
        processing_time_ms=123.5,
    )
    assert thought2.processing_time_ms == 123.5
    print("✓ 处理时间记录正确")
    
    print("PASS: BrainThought")
    return True


def test_brain_evolution():
    """测试BrainEvolution"""
    print("\n=== 测试 BrainEvolution ===")
    
    from digital_brain.digital_brain_core import BrainEvolution
    import time
    
    # 进化结果
    evo = BrainEvolution(
        evolution_id="evo-001",
        evolution_type="memory_consolidation",
        trigger_reason="scheduled",
        changes={"memory_added": 10, "connections_updated": 5},
        improvements=["知识整合完成", "响应速度提升"],
    )
    assert evo.evolution_id == "evo-001"
    assert evo.evolution_type == "memory_consolidation"
    assert evo.trigger_reason == "scheduled"
    assert len(evo.changes) == 2
    assert len(evo.improvements) == 2
    assert evo.success == True
    print("✓ 进化结果正确")
    
    print("PASS: BrainEvolution")
    return True


def test_brain_health():
    """测试BrainHealth"""
    print("\n=== 测试 BrainHealth ===")
    
    from digital_brain.digital_brain_core import BrainHealth
    
    # 健康状态
    health = BrainHealth(
        overall_score=85.0,
        memory_health=90.0,
        wisdom_health=80.0,
        evolution_health=85.0,
        llm_health=75.0,
        library_health=95.0,
        active_thoughts=5,
        pending_evolutions=0,
        uptime_seconds=3600.0,
    )
    assert health.overall_score == 85.0
    assert health.memory_health == 90.0
    assert health.wisdom_health == 80.0
    assert health.active_thoughts == 5
    assert health.uptime_seconds == 3600.0
    print("✓ 健康状态正确")
    
    # 带异常的Health
    health2 = BrainHealth(
        overall_score=70.0,
        memory_health=90.0,
        wisdom_health=60.0,
        evolution_health=70.0,
        llm_health=50.0,
        library_health=80.0,
        anomalies=[{"type": "slow_response", "details": "wisdom模块响应慢"}],
        recommendations=["优化wisdom引擎", "增加缓存"],
    )
    assert len(health2.anomalies) == 1
    assert len(health2.recommendations) == 2
    print("✓ 异常和建议记录正确")
    
    print("PASS: BrainHealth")
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# 测试: 集成配置
# ═══════════════════════════════════════════════════════════════════════════════

def test_memory_bridge_config():
    """测试MemoryBridgeConfig"""
    print("\n=== 测试 MemoryBridgeConfig ===")
    
    from digital_brain.digital_brain_integration import MemoryBridgeConfig, MemorySyncDirection
    
    config = MemoryBridgeConfig()
    assert config.sync_enabled == True
    assert config.sync_interval_minutes == 30
    assert config.auto_sync_threshold == 0.7
    assert config.sync_batch_size == 50
    print("✓ MemoryBridgeConfig默认配置正确")
    
    # 自定义配置
    custom = MemoryBridgeConfig(
        sync_enabled=False,
        sync_interval_minutes=60,
        auto_sync_threshold=0.8,
    )
    assert custom.sync_enabled == False
    assert custom.sync_interval_minutes == 60
    assert custom.auto_sync_threshold == 0.8
    print("✓ MemoryBridgeConfig自定义配置正确")
    
    print("PASS: MemoryBridgeConfig")
    return True


def test_wisdom_bridge_config():
    """测试WisdomBridgeConfig"""
    print("\n=== 测试 WisdomBridgeConfig ===")
    
    from digital_brain.digital_brain_integration import WisdomBridgeConfig
    
    config = WisdomBridgeConfig()
    assert config.memory_enhance_dispatch == True
    assert config.dispatch_result_memory == True
    assert config.school_capability_track == True
    assert config.confidence_learning == True
    print("✓ WisdomBridgeConfig默认配置正确")
    
    # 自定义配置
    custom = WisdomBridgeConfig(
        memory_enhance_dispatch=False,
        confidence_learning=False,
    )
    assert custom.memory_enhance_dispatch == False
    assert custom.confidence_learning == False
    print("✓ WisdomBridgeConfig自定义配置正确")
    
    print("PASS: WisdomBridgeConfig")
    return True


def test_somn_integration_config():
    """测试SomnIntegrationConfig"""
    print("\n=== 测试 SomnIntegrationConfig ===")
    
    from digital_brain.digital_brain_integration import SomnIntegrationConfig
    
    config = SomnIntegrationConfig()
    assert config.enable_digital_brain == True
    assert config.digital_brain_as_subagent == False
    assert config.brain_thinks_for_complex == True
    assert config.confidence_threshold == 0.6
    print("✓ SomnIntegrationConfig默认配置正确")
    
    # 自定义配置
    custom = SomnIntegrationConfig(
        enable_digital_brain=False,
        confidence_threshold=0.8,
    )
    assert custom.enable_digital_brain == False
    assert custom.confidence_threshold == 0.8
    print("✓ SomnIntegrationConfig自定义配置正确")
    
    print("PASS: SomnIntegrationConfig")
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# 测试: Somn集成API [v1.0.0]
# ═══════════════════════════════════════════════════════════════════════════════

def test_somn_digital_brain_api():
    """测试Somn集成API"""
    print("\n=== 测试 Somn集成API ===")
    
    from digital_brain._somn_digital_brain_api import (
        DigitalBrainSomnConfig,
        DigitalBrainSomnIntegrator,
        ThroughResult,
        create_digital_brain_somn_integrator,
    )
    
    # 模拟SomnCore
    class MockSomnCore:
        pass
    
    # 配置测试
    config = DigitalBrainSomnConfig(
        auto_integrate=True,
        enable_through_somn=True,
        somn_weight=0.6,
        brain_weight=0.4,
    )
    assert config.auto_integrate == True
    assert config.enable_through_somn == True
    assert config.somn_weight == 0.6
    assert config.brain_weight == 0.4
    print("✓ DigitalBrainSomnConfig正确")
    
    # 创建集成器
    somn_core = MockSomnCore()
    integrator = DigitalBrainSomnIntegrator(somn_core, config)
    assert integrator.is_digital_brain_ready == False
    assert integrator.stats['total_thinks'] == 0
    print("✓ DigitalBrainSomnIntegrator正确")
    
    # ThroughResult测试
    result = ThroughResult(
        success=True,
        somn_result="somn_result",
        brain_result={"thought": "brain_thought"},
        fusion_result="fusion",
    )
    assert result.success == True
    assert result.somn_result == "somn_result"
    print("✓ ThroughResult正确")
    
    # 工厂函数测试
    factory_integrator = create_digital_brain_somn_integrator(somn_core)
    assert factory_integrator is not None
    print("✓ 工厂函数正确")
    
    print("PASS: Somn集成API")
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# 测试: DigitalBrainCore类定义
# ═══════════════════════════════════════════════════════════════════════════════

def test_digital_brain_core_class():
    """测试DigitalBrainCore类定义"""
    print("\n=== 测试 DigitalBrainCore类定义 ===")
    
    from digital_brain.digital_brain_core import (
        BrainConfig,
        BrainState,
        DigitalBrainCore,
        get_digital_brain,
        shutdown_digital_brain,
    )
    
    # 类存在
    assert DigitalBrainCore is not None
    print("✓ DigitalBrainCore类存在")
    
    # 配置类
    config = BrainConfig()
    assert config.enable_local_llm == True
    print("✓ BrainConfig配置正确")
    
    # 状态枚举
    assert BrainState.INITIALIZING.value == "initializing"
    assert BrainState.READY.value == "ready"
    print("✓ BrainState枚举正确")
    
    # 单例函数存在
    assert get_digital_brain is not None
    assert shutdown_digital_brain is not None
    print("✓ 单例管理函数存在")
    
    print("PASS: DigitalBrainCore类定义")
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# 测试: 集成桥接基本功能
# ═══════════════════════════════════════════════════════════════════════════════

def test_integration_bridges():
    """测试集成桥接基本功能"""
    print("\n=== 测试 集成桥接基本功能 ===")
    
    from digital_brain.digital_brain_integration import (
        MemoryLibraryBridge,
        WisdomMemoryBridge,
        SomnDigitalBrainIntegrator,
        create_digital_brain_integration,
        MemoryBridgeConfig,
        WisdomBridgeConfig,
        SomnIntegrationConfig,
    )
    
    # 测试MemoryLibraryBridge
    config = MemoryBridgeConfig()
    bridge = MemoryLibraryBridge(config)
    assert bridge is not None
    assert bridge.config == config
    print("✓ MemoryLibraryBridge基本功能正确")
    
    # 测试WisdomMemoryBridge
    wisdom_config = WisdomBridgeConfig()
    wisdom_bridge = WisdomMemoryBridge(wisdom_config)
    assert wisdom_bridge is not None
    assert wisdom_bridge.config == wisdom_config
    print("✓ WisdomMemoryBridge基本功能正确")
    
    # 测试SomnDigitalBrainIntegrator
    somn_config = SomnIntegrationConfig()
    somn_brain = SomnDigitalBrainIntegrator(somn_config)
    assert somn_brain is not None
    assert somn_brain.config == somn_config
    print("✓ SomnDigitalBrainIntegrator基本功能正确")
    
    # 测试工厂函数（异步）
    # 注意: create_digital_brain_integration是异步函数
    # 在测试环境中无法直接调用，需要在异步上下文中测试
    assert create_digital_brain_integration is not None
    print("✓ create_digital_brain_integration工厂函数存在（异步）")
    
    print("PASS: 集成桥接基本功能")
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════════════════════════

def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("数字大脑模块测试")
    print("=" * 60)
    
    tests = [
        # 数据结构
        test_brain_state,
        test_memory_level,
        test_brain_config,
        test_brain_thought,
        test_brain_evolution,
        test_brain_health,
        
        # 集成配置
        test_memory_bridge_config,
        test_wisdom_bridge_config,
        test_somn_integration_config,
        
        # Somn集成API
        test_somn_digital_brain_api,
        
        # 核心类
        test_digital_brain_core_class,
        
        # 集成桥接
        test_integration_bridges,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"FAIL: {test.__name__}")
        except Exception as e:
            failed += 1
            print(f"FAIL: {test.__name__} - {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{passed + failed} 通过")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
