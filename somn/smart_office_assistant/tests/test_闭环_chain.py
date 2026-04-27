"""
技术债务闭环全链路测试
Test: ROI追踪 → 反馈管道 → 强化学习 → 迁移学习 → 每日学习整合
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

project_root = bootstrap_project_paths(__file__, change_cwd=True)
TEST_BASE = str(project_root / "src/neural_memory/learning")


from datetime import datetime
from src.neural_memory.roi_tracker import ROITracker
from src.neural_memory.feedback_pipeline import FeedbackPipeline
from src.neural_memory.reinforcement_trigger import ReinforcementTrigger
from src.neural_memory.transfer_learner import TransferLearner, ScenarioProfile


def test_roi_tracker():
    """测试1: ROI追踪器"""
    print("\n=== 测试1: ROI追踪器 ===")
    tracker = ROITracker(base_path=os.path.join(TEST_BASE, "test_roi"))
    
    # 记录任务
    task_id = tracker.track_task_start("T001", "增长分析", "私域运营", estimated_minutes=30)
    tracker.record_interaction(task_id, "查询", duration_seconds=120)
    
    # 完成任务
    record_id = tracker.track_task_complete(task_id, {
        "completed": True,
        "quality_score": 0.85,
        "actual_minutes": 25,
        "time_saved_minutes": 5,
        "adopted": True,
        "error_count": 0,
    })
    print(f"  ✅ 任务完成，记录ID: {record_id}")
    
    # 记录反馈
    fb_id = tracker.record_user_feedback("T001", {
        "type": "rating", "value": 5,
        "task_type": "增长分析",
    })
    print(f"  ✅ 反馈记录ID: {fb_id}")
    
    # ROI分析
    roi = tracker.get_strategy_roi("私域运营")
    print(f"  ✅ 策略ROI: {roi}")
    
    baseline = tracker.get_baseline()
    print(f"  ✅ 基线: {baseline}")
    assert roi["avg_efficiency_score"] > 0, "效率分应为正"
    print("  ✅ ROI追踪器测试通过")


def test_feedback_pipeline():
    """测试2: 反馈管道"""
    print("\n=== 测试2: 反馈管道 ===")
    pipeline = FeedbackPipeline(base_path=os.path.join(TEST_BASE, "test_fb"))
    
    # 接收多种反馈
    fb1 = pipeline.receive_feedback({
        "task_id": "T002", "task_type": "策略设计",
        "strategy": "小红书运营", "type": "adoption", "value": True,
        "timestamp": datetime.now().isoformat(),
    })
    fb2 = pipeline.receive_feedback({
        "task_id": "T002", "task_type": "策略设计",
        "strategy": "小红书运营", "type": "rating", "value": 4,
        "timestamp": datetime.now().isoformat(),
    })
    fb3 = pipeline.receive_feedback({
        "task_id": "T003", "task_type": "策略设计",
        "strategy": "抖音运营", "type": "correction", "value": -1,
        "timestamp": datetime.now().isoformat(),
    })
    print(f"  ✅ 收到反馈: {fb1}, {fb2}, {fb3}")
    
    # 隐式信号
    implicit_id = pipeline.receive_implicit_signal(
        "T004", "增长分析", "私域运营",
        {"type": "iteration", "value": 3}
    )
    print(f"  ✅ 隐式信号: {implicit_id}")
    
    # 获取可学习反馈
    learnable = pipeline.get_learnable_feedbacks()
    print(f"  ✅ 可学习反馈数: {len(learnable)}")
    assert len(learnable) >= 3, "应有>=3条反馈"
    print("  ✅ 反馈管道测试通过")


def test_reinforcement_trigger():
    """测试3: 强化学习触发器"""
    print("\n=== 测试3: 强化学习触发器 ===")
    trigger = ReinforcementTrigger(
        base_path=os.path.join(TEST_BASE, "test_rl")
    )
    trigger.params["batch_threshold"] = 2  # 测试用低阈值
    
    # 推送奖励
    trigger.push_feedback("私域运营", 0.8)
    trigger.push_feedback("私域运营", 0.6)
    trigger.push_feedback("私域运营", 0.7)
    trigger.push_feedback("小红书运营", 0.5)
    trigger.push_feedback("小红书运营", 0.4)
    print("  ✅ 奖励信号已推送")
    
    # 检查触发条件
    should = trigger.should_trigger()
    print(f"  ✅ 满足触发条件: {should}")
    assert should, "应满足批量触发条件"
    
    # 执行Q-learning更新
    updates = trigger.trigger_update(force=True)
    for u in updates:
        print(f"  ✅ Q更新: {u.action} {u.q_value_before:.3f} → {u.q_value_after:.3f} (样本={u.n_samples})")
    assert len(updates) >= 2, "应有>=2个策略更新"
    
    # 最优动作
    best_action, best_q = trigger.get_best_action()
    print(f"  ✅ 最优策略: {best_action} (Q={best_q:.3f})")
    assert best_action is not None, "应有最优策略"
    print("  ✅ 强化学习触发器测试通过")


def test_transfer_learner():
    """测试4: 迁移学习场景匹配器"""
    print("\n=== 测试4: 迁移学习场景匹配器 ===")
    learner = TransferLearner(
        base_path=os.path.join(TEST_BASE, "test_tl")
    )
    
    # 注册知识
    k1 = learner.register_knowledge(
        concept="私域流量运营",
        domain="电商",
        confidence=0.78,
        source_scenario="零售电商"
    )
    k2 = learner.register_knowledge(
        concept="内容种草",
        domain="内容",
        confidence=0.72,
        source_scenario="美妆内容"
    )
    print(f"  ✅ 知识注册: {k1}, {k2}")
    
    # 注册场景
    scene1 = ScenarioProfile(
        scenario_id="SCENE_医美",
        name="医美行业增长",
        industry="电商",  # 跨行业迁移：医美→电商
        keywords=["医美", "客户获取", "私域", "复购"],
        features={},
    )
    learner.register_scenario(scene1)
    print("  ✅ 场景注册: 医美行业增长")
    
    # 查找可迁移知识
    candidates = learner.find_transferable_knowledge(scene1, top_k=5)
    print(f"  ✅ 可迁移知识: {[(k.concept, round(s, 3)) for k, s in candidates]}")
    
    # 创建迁移假设
    if candidates:
        knowledge, sim = candidates[0]
        h = learner.create_transfer_hypothesis(knowledge, scene1)
        if h:
            print(f"  ✅ 迁移假设: {h.hypothesis_id} 置信度={h.transfer_confidence:.3f}")
    
    # 报告验证结果
    if learner._hypotheses:
        h_id = list(learner._hypotheses.keys())[0]
        learner.report_validation_result(h_id, {"passed": True, "effect_size": 0.15})
        print(f"  ✅ 验证结果已回传")
    
    # 获取迁移报告
    report = learner.get_transfer_report()
    print(f"  ✅ 迁移报告: 知识={report['total_knowledge']}, "
          f"假设={report['total_hypotheses']}, "
          f"验证通过={report['validated']}")
    print("  ✅ 迁移学习测试通过")


def main():
    print("=" * 60)
    print("Somn 技术债务闭环全链路测试")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        test_roi_tracker()
        test_feedback_pipeline()
        test_reinforcement_trigger()
        test_transfer_learner()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！技术债务闭环链路验证成功")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
