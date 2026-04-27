"""
数字大脑Somn集成API测试
Test Digital Brain Somn Integration API

测试内容:
1. DigitalBrainSomnConfig配置
2. ThroughResult数据结构
3. DigitalBrainSomnIntegrator集成器
4. 工厂函数

Author: Somn Digital Brain Team
"""

import asyncio
import sys
from pathlib import Path

# 添加项目路径
project_src = Path(__file__).parent.parent  # digital_brain/tests -> digital_brain/ -> src/
sys.path.insert(0, str(project_src))

# ═══════════════════════════════════════════════════════════════════════════════
# 测试: 配置和数据结构
# ═══════════════════════════════════════════════════════════════════════════════

def test_digital_brain_somn_config():
    """测试数字大脑Somn配置"""
    print("\n=== 测试 DigitalBrainSomnConfig ===")
    
    from digital_brain._somn_digital_brain_api import DigitalBrainSomnConfig
    
    # 默认配置
    config = DigitalBrainSomnConfig()
    assert config.auto_integrate == True
    assert config.enable_through_somn == True
    assert config.somn_weight == 0.6
    assert config.brain_weight == 0.4
    assert config.default_think_mode == "integrated"
    assert config.timeout_seconds == 30.0
    print("✓ 默认配置正确")
    
    # 自定义配置
    custom_config = DigitalBrainSomnConfig(
        auto_integrate=False,
        somn_weight=0.7,
        brain_weight=0.3,
        timeout_seconds=60.0,
    )
    assert custom_config.auto_integrate == False
    assert custom_config.somn_weight == 0.7
    assert custom_config.brain_weight == 0.3
    assert custom_config.timeout_seconds == 60.0
    print("✓ 自定义配置正确")
    
    print("PASS: DigitalBrainSomnConfig")
    return True


def test_through_result():
    """测试穿越结果数据结构"""
    print("\n=== 测试 ThroughResult ===")
    
    from digital_brain._somn_digital_brain_api import ThroughResult
    
    # 成功结果
    result = ThroughResult(
        success=True,
        somn_result="Somn处理结果",
        brain_result={"thought": "数字大脑思考", "confidence": 0.85},
        fusion_result="融合结果",
        thinking_trace=["Step 1", "Step 2"],
        metrics={"mode": "integrated", "duration": 1.5}
    )
    assert result.success == True
    assert result.somn_result == "Somn处理结果"
    assert result.brain_result["confidence"] == 0.85
    assert len(result.thinking_trace) == 2
    print("✓ 成功结果正确")
    
    # 失败结果
    error_result = ThroughResult(
        success=False,
        error="测试错误"
    )
    assert error_result.success == False
    assert error_result.error == "测试错误"
    print("✓ 失败结果正确")
    
    print("PASS: ThroughResult")
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# 测试: 集成器
# ═══════════════════════════════════════════════════════════════════════════════

def test_digital_brain_somn_integrator():
    """测试数字大脑Somn集成器"""
    print("\n=== 测试 DigitalBrainSomnIntegrator ===")
    
    from digital_brain._somn_digital_brain_api import (
        DigitalBrainSomnIntegrator,
        DigitalBrainSomnConfig,
    )
    
    # 创建模拟SomnCore
    class MockSomnCore:
        pass
    
    somn_core = MockSomnCore()
    config = DigitalBrainSomnConfig()
    
    # 创建集成器
    integrator = DigitalBrainSomnIntegrator(somn_core, config)
    
    # 检查属性
    assert integrator.digital_brain is None
    assert integrator.digital_brain_config == config
    assert integrator.is_digital_brain_ready == False
    assert integrator.stats['total_thinks'] == 0
    print("✓ 集成器初始化正确")
    
    # 检查统计
    stats = integrator.stats
    assert 'total_thinks' in stats
    assert 'successful_thinks' in stats
    assert 'failed_thinks' in stats
    assert 'total_evolutions' in stats
    assert 'total_purifications' in stats
    print("✓ 统计信息正确")
    
    print("PASS: DigitalBrainSomnIntegrator")
    return True


def test_factory_function():
    """测试工厂函数"""
    print("\n=== 测试 create_digital_brain_somn_integrator ===")
    
    from digital_brain._somn_digital_brain_api import (
        create_digital_brain_somn_integrator,
        DigitalBrainSomnConfig,
    )
    
    # 创建模拟SomnCore
    class MockSomnCore:
        pass
    
    somn_core = MockSomnCore()
    
    # 使用默认配置
    integrator1 = create_digital_brain_somn_integrator(somn_core)
    assert integrator1 is not None
    assert integrator1.is_digital_brain_ready == False
    print("✓ 默认配置工厂函数正确")
    
    # 使用自定义配置
    config = DigitalBrainSomnConfig(auto_integrate=False)
    integrator2 = create_digital_brain_somn_integrator(somn_core, config)
    assert integrator2.digital_brain_config.auto_integrate == False
    print("✓ 自定义配置工厂函数正确")
    
    print("PASS: create_digital_brain_somn_integrator")
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# 主函数
# ═══════════════════════════════════════════════════════════════════════════════

def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("数字大脑Somn集成API测试")
    print("=" * 60)
    
    tests = [
        test_digital_brain_somn_config,
        test_through_result,
        test_digital_brain_somn_integrator,
        test_factory_function,
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
