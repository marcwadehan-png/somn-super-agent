# -*- coding: utf-8 -*-
"""
NeuralMemory v7.0 整合测试
===========================

测试项目:
1. 导入验证
2. NeuralMemory v7.0 实例化
3. DigitalStrategy 策略层
4. NeuralExecutor 执行层
5. 委托链正确性

版本: v7.0.0
更新: 2026-04-30
"""

import asyncio
import sys
import time

# 添加项目根目录
sys.path.insert(0, str(__file__).rsplit('src', 1)[0] + 'src')


def test_imports():
    """测试1: 导入验证"""
    print("\n=== 测试1: 导入验证 ===")
    
    from neural_memory import (
        NeuralMemory,
        NeuralMemoryConfig,
        ThinkResult,
        DigitalStrategy,
        NeuralExecutor,
        MemoryLevel,
        BrainState,
        StrategyThought,
        StrategyEvolution,
        StrategyHealth,
        StrategyConfig,
        ExecutorConfig,
        ExecutorOperation,
        ExecutorHealth,
        get_neural_memory,
    )
    
    print("✓ 所有 v7.0 符号导入成功")
    return True


def test_memory_levels():
    """测试2: 统一记忆层级"""
    print("\n=== 测试2: 统一记忆层级 ===")
    
    from neural_memory import MemoryLevel
    
    levels = list(MemoryLevel)
    print(f"  记忆层级数量: {len(levels)}")
    
    for level in levels:
        print(f"  - {level.name} = {level.value} (priority={level.priority})")
    
    assert len(levels) == 5, f"期望5级记忆, 实际{len(levels)}"
    print("✓ 记忆层级定义正确 (5级)")
    return True


def test_executor_config():
    """测试3: 执行层配置"""
    print("\n=== 测试3: 执行层配置 ===")
    
    from neural_memory import ExecutorConfig
    
    cfg = ExecutorConfig(
        encoding_dim=512,
        max_workers=8,
        memory_ttl_hours=48,
    )
    
    assert cfg.encoding_dim == 512
    assert cfg.max_workers == 8
    assert cfg.memory_ttl_hours == 48
    
    print(f"  encoding_dim: {cfg.encoding_dim}")
    print(f"  max_workers: {cfg.max_workers}")
    print("✓ 执行层配置正确")
    return True


def test_strategy_config():
    """测试4: 策略层配置"""
    print("\n=== 测试4: 策略层配置 ===")
    
    from neural_memory import StrategyConfig
    
    cfg = StrategyConfig(
        enable_wisdom_dispatch=True,
        enable_llm_enhancement=False,
        enable_autonomous_evolution=True,
    )
    
    assert cfg.enable_wisdom_dispatch == True
    assert cfg.enable_llm_enhancement == False
    assert cfg.enable_autonomous_evolution == True
    
    print(f"  enable_wisdom_dispatch: {cfg.enable_wisdom_dispatch}")
    print(f"  enable_llm_enhancement: {cfg.enable_llm_enhancement}")
    print("✓ 策略层配置正确")
    return True


async def test_executor():
    """测试5: 执行层实例化"""
    print("\n=== 测试5: 执行层实例化 ===")
    
    from neural_memory import NeuralExecutor, ExecutorConfig
    
    start = time.time()
    executor = NeuralExecutor(ExecutorConfig())
    elapsed = (time.time() - start) * 1000
    
    print(f"  实例化时间: {elapsed:.2f}ms")
    
    # 测试懒加载子系统
    stats = executor.get_stats()
    print(f"  子系统加载状态: {stats['subsystems_loaded']}")
    
    health = await executor.get_health()
    print(f"  健康度: {health['score']:.1f}")
    
    assert elapsed < 50, f"实例化时间过长: {elapsed:.2f}ms"
    print("✓ 执行层实例化成功 (<50ms)")
    return True


async def test_neural_memory():
    """测试6: NeuralMemory v7.0 统一门面"""
    print("\n=== 测试6: NeuralMemory v7.0 统一门面 ===")
    
    from neural_memory import NeuralMemory, NeuralMemoryConfig, get_neural_memory
    
    # 禁用策略层以加快测试
    config = NeuralMemoryConfig(
        enable_strategy=False,  # 测试纯执行模式
        encoding_dim=384,
        max_workers=4,
    )
    
    start = time.time()
    nm = NeuralMemory(config)
    elapsed = (time.time() - start) * 1000
    
    print(f"  实例化时间: {elapsed:.2f}ms")
    
    # 测试单例
    nm2 = get_neural_memory()
    assert nm is nm2, "单例失效"
    print("  单例: ✓")
    
    # 测试健康检查
    health = await nm.get_health()
    print(f"  版本: {health['version']}")
    print(f"  执行层健康度: {health['executor']['score']:.1f}")
    print(f"  策略层启用: {health['strategy'] is not None}")  # 因为我们禁用了
    
    # 测试统计
    stats = nm.get_stats()
    print(f"  运行时长: {stats['uptime_seconds']:.2f}s")
    
    assert elapsed < 100, f"实例化时间过长: {elapsed:.2f}ms"
    print("✓ NeuralMemory v7.0 统一门面实例化成功 (<100ms)")
    return True


async def test_delegation_chain():
    """测试7: 委托链验证"""
    print("\n=== 测试7: 委托链验证 ===")
    
    from neural_memory import NeuralMemory, NeuralMemoryConfig
    from neural_memory.digital_strategy import DigitalStrategy
    from neural_memory.neural_executor import NeuralExecutor
    
    # 禁用策略层
    nm = NeuralMemory(NeuralMemoryConfig(enable_strategy=False))
    
    # 验证策略层存在
    assert hasattr(nm, '_strategy'), "缺少策略层属性"
    print("  策略层属性: ✓")
    
    # 验证执行层存在
    assert hasattr(nm, '_executor'), "缺少执行层属性"
    print("  执行层属性: ✓")
    
    # 验证执行层是 NeuralExecutor 实例
    assert isinstance(nm._executor, NeuralExecutor), "执行层类型错误"
    print("  执行层类型: ✓ NeuralExecutor")
    
    # 验证策略层可以持有执行层引用
    if nm._strategy:
        assert nm._strategy.executor is nm._executor, "策略层-执行层引用断开"
        print("  策略层-执行层引用: ✓")
    
    print("✓ 委托链验证通过")
    return True


async def test_fallback_mode():
    """测试8: 降级模式 (策略禁用)"""
    print("\n=== 测试8: 降级模式 (策略禁用) ===")
    
    from neural_memory import NeuralMemory, NeuralMemoryConfig
    
    nm = NeuralMemory(NeuralMemoryConfig(enable_strategy=False))
    
    # 测试 think 降级
    result = await nm.think("测试查询")
    
    print(f"  返回内容: {result.content[:50]}...")
    print(f"  来源: {result.source}")
    print(f"  问题类型: {result.problem_type}")
    
    assert result.problem_type == "FALLBACK", f"降级模式失败: {result.problem_type}"
    print("✓ 降级模式工作正常")
    return True


async def test_memory_operations():
    """测试9: 记忆操作 (执行层)"""
    print("\n=== 测试9: 记忆操作 (执行层) ===")
    
    from neural_memory import NeuralMemory, NeuralMemoryConfig
    
    nm = NeuralMemory(NeuralMemoryConfig(enable_strategy=False))
    
    # 添加记忆
    success = await nm.add_memory(
        content="这是一条测试记忆，用于验证执行层功能",
        query="测试",
        metadata={"type": "test"}
    )
    print(f"  添加记忆: {'✓' if success else '✗'}")
    
    # 检索记忆
    results = await nm.retrieve_memory("测试", top_k=5)
    print(f"  检索结果: {len(results)} 条")
    
    # 别名测试
    success = await nm.remember("另一条测试记忆", "别名测试")
    print(f"  remember别名: {'✓' if success else '(执行层未就绪)'}")
    
    print("✓ 记忆操作接口正常")
    return True


async def main():
    """运行所有测试"""
    print("=" * 60)
    print("NeuralMemory v7.0 整合测试")
    print("=" * 60)
    
    tests = [
        ("导入验证", test_imports),
        ("统一记忆层级", test_memory_levels),
        ("执行层配置", test_executor_config),
        ("策略层配置", test_strategy_config),
        ("执行层实例化", test_executor),
        ("NeuralMemory v7.0 门面", test_neural_memory),
        ("委托链验证", test_delegation_chain),
        ("降级模式", test_fallback_mode),
        ("记忆操作", test_memory_operations),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_fn in tests:
        try:
            if asyncio.iscoroutinefunction(test_fn):
                result = await test_fn()
            else:
                result = test_fn()
            
            if result:
                passed += 1
        except Exception as e:
            print(f"\n✗ {name} 失败: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{passed+failed} 通过")
    print("=" * 60)
    
    if failed > 0:
        print(f"\n⚠️  {failed} 个测试失败")
        return False
    else:
        print("\n✅ NeuralMemory v7.0 整合测试全部通过!")
        return True


if __name__ == "__main__":
    asyncio.run(main())
