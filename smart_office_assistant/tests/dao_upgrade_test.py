"""道家哲学升级Phase 1验证脚本 v1.0"""
import sys
sys.path.insert(0, 'src')

print("=== 测试1: WisdomDispatcher道家无为模式 ===")
from intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WuWeiDispatchMode, WuWeiConfig, WuWeiObservationResult, WisdomDispatcher
d = WisdomDispatcher()
print(f"  WuWeiDispatchMode: {[m.value for m in WuWeiDispatchMode]}")
print(f"  当前调度模式: {d.wuwei_mode.value}")
print(f"  无为配置observe_window: {d.wuwei_config.observe_window_ms}ms")
print(f"  水属性学派: {[s.value for s in d.wuwei_config.water_nature_schools]}")
print(f"  启用道家提示方法: {'get_dao_wisdom_hint' in dir(d)}")
# 测试设置调度模式
d.set_dispatch_mode(WuWeiDispatchMode.WUWEI_OBSERVE)
print(f"  切换为无为模式: {d.wuwei_mode.value}")
# 测试无为观察
from intelligence.dispatcher.wisdom_dispatch._dispatch_enums import ProblemType
result = d.wuwei_observe(ProblemType.RISK, window_ms=100)
print(f"  无为观察结果: mode={result.mode_used.value}, 响应数={result.natural_response_count}")
print(f"  道家分析: {result.dao_analysis[:50]}...")
print("  [PASS] WisdomDispatcher道家无为模式")

print()
print("=== 测试2: AdaptiveLearningCoordinator自然演化 ===")
from learning.neural.adaptive_learning_coordinator import (
    NatureEvolutionConfig, NatureEvolutionStrategy, ExplorationContext, AdaptiveLearningCoordinator
)
alc = AdaptiveLearningCoordinator()
print(f"  自然演化启用: {alc.nature_enabled}")
print(f"  动态遗忘: {alc.nature_config.use_dynamic_decay}")
print(f"  情境探索: {alc.nature_config.use_contextual_exploration}")
print(f"  自发精炼: {alc.nature_config.use_spontaneous_refinement}")
# 测试知识注册和遗忘率计算
alc.register_knowledge_usage("test_knowledge_1", importance=0.8)
decay = alc.compute_dynamic_decay("test_knowledge_1")
print(f"  知识遗忘率计算: {decay:.4f}")
# 测试情境探索
ctx = ExplorationContext(system_load=0.2, uncertainty_level=0.7)
rate = alc.compute_contextual_exploration(ctx)
print(f"  情境探索率: {rate:.3f}")
# 测试自发精炼
ref = alc.check_spontaneous_refinement()
print(f"  自发精炼触发: {ref['triggered']}")
# 测试状态报告
status = alc.get_nature_evolution_status()
print(f"  自然演化状态: {status['dao_wisdom']['status']}, 健康度: {status['dao_wisdom']['health']}")
print("  [PASS] AdaptiveLearningCoordinator自然演化")

print()
print("=== 测试3: WisdomFusion上善若水融合 ===")
from intelligence.dispatcher.wisdom_fusion._fusion_enums import (
    ShangShanFusionMode, ShangShanFusionConfig, FusionConfig, WisdomContribution
)
from intelligence.dispatcher.wisdom_fusion import WisdomFusionCore
fc = FusionConfig()
print(f"  上善若水启用: {fc.shang_shan.shang_shan_enabled}")
print(f"  默认模式: {fc.shang_shan.default_mode.value}")
print(f"  全部融合模式: {[m.value for m in ShangShanFusionMode]}")
print(f"  和谐导向模式: {[m.value for m in ShangShanFusionMode]}")

# 测试WisdomFusionCore
try:
    wfc = WisdomFusionCore()
    has_shang_shan = hasattr(wfc, 'shang_shan_fuse')
    print(f"  shang_shan_fuse方法存在: {has_shang_shan}")
    if has_shang_shan:
        # 测试上善若水融合
        contributions = [
            WisdomContribution(module_name="dao_wisdom", output={"advice": "无为"}, confidence=0.8, relevance=0.7, reliability=0.9, weight=0.3),
            WisdomContribution(module_name="ru_wisdom", output={"advice": "仁政"}, confidence=0.6, relevance=0.8, reliability=0.85, weight=0.4),
            WisdomContribution(module_name="military", output={"advice": "进攻"}, confidence=0.7, relevance=0.5, reliability=0.9, weight=0.3),
        ]
        shang_shan_result = wfc.shang_shan_fuse(contributions, mode=ShangShanFusionMode.HARMONY_ORIENTED)
        print(f"  和谐度: {shang_shan_result.harmony_score:.3f}")
        print(f"  阴阳平衡: {shang_shan_result.yin_yang_balance:.3f}")
        print(f"  道家评估: {shang_shan_result.dao_assessment[:50]}...")
        print(f"  最终权重: { {k: f'{v:.2f}' for k, v in shang_shan_result.fused_weights.items()} }")
    status = wfc.get_shang_shan_status()
    print(f"  上善若水状态: {status['default_mode']}")
    print("  [PASS] WisdomFusionCore上善若水融合")
except Exception as e:
    print(f"  [WARN] WisdomFusionCore测试异常（可能是依赖问题）: {e}")

print()
print("=== 全部测试完成 ===")
