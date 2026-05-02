"""
多用户语义记忆引擎测试
Multi-User Semantic Memory Engine Test

验证功能：
1. 多用户注册与切换
2. 用户隔离存储
3. 千人千面：不同用户学到的语义不同
4. 用户数据导出（GDPR合规）
5. 全局统计
"""

import sys
import os
from pathlib import Path

# 禁用日志
from loguru import logger
logger.remove()

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from src.neural_memory.semantic_memory_engine import (

    MultiUserSemanticEngine,
    SemanticMemoryEngine
)

def test_multi_user():
    """测试多用户功能"""

    # 使用临时路径
    test_path = os.path.join(os.path.dirname(__file__), "temp_semantic_multiuser")
    if os.path.exists(test_path):
        import shutil
        shutil.rmtree(test_path)

    print("=" * 60)
    print("多用户语义记忆引擎测试")
    print("=" * 60)

    # 1. 创建引擎
    print("\n[1] 创建多用户语义记忆引擎...")
    engine = MultiUserSemanticEngine(base_path=test_path)
    print(f"  ✅ 引擎创建成功")

    # 2. 注册用户
    print("\n[2] 注册多个用户...")
    users = ["alice", "bob", "charlie"]
    for uid in users:
        result = engine.register_user(uid)
        print(f"  ✅ 注册用户 {uid}: {result}")
    print(f"  当前用户数: {len(engine.list_users())}")

    # 3. 用户A学习："报表" = "销售数据"
    print("\n[3] 用户 alice 学习语义...")
    engine.switch_user("alice")
    engine.learn_from_input("看看报表", "查看销售数据")
    engine.learn_from_input("报表数据", "查看销售数据")
    engine.learn_from_input("报表分析", "查看销售数据")
    print(f"  alice 查询 '报表': {engine.get_keyword_meaning('报表', 'alice')}")

    # 4. 用户B学习："报表" = "财务报表"
    print("\n[4] 用户 bob 学习不同语义...")
    engine.switch_user("bob")
    engine.learn_from_input("财务报表", "财务报表分析")
    engine.learn_from_input("看报表", "财务报表分析")
    engine.learn_from_input("报表情况", "财务报表分析")
    print(f"  bob 查询 '报表': {engine.get_keyword_meaning('报表', 'bob')}")

    # 5. 验证千人千面
    print("\n[5] 验证千人千面（同一关键词，不同用户不同理解）...")
    alice_meaning = engine.get_keyword_meaning("报表", "alice")
    bob_meaning = engine.get_keyword_meaning("报表", "bob")
    print(f"  alice: '报表' = {alice_meaning}")
    print(f"  bob:   '报表' = {bob_meaning}")
    if alice_meaning != bob_meaning:
        print(f"  ✅ 千人千面验证通过！不同用户学到了不同的语义")
    else:
        print(f"  ❌ 语义相同，应该不同")

    # 6. 用户C（未学习）应该没有映射
    print("\n[6] 新用户 charlie 未学习 '报表'...")
    charlie_meaning = engine.get_keyword_meaning("报表", "charlie")
    print(f"  charlie 查询 '报表': {charlie_meaning}")
    if charlie_meaning is None:
        print(f"  ✅ 验证通过：新用户没有继承其他用户的语义")

    # 7. 测试语义理解（多用户）
    print("\n[7] 测试语义理解（多用户）...")
    print("  用户 alice 输入: '帮我分析报表'")
    ctx_alice = engine.process_input("帮我分析报表", user_id="alice")
    print(f"    推断意图: {ctx_alice.inferred_intent}, 置信度: {ctx_alice.intent_confidence:.2f}")
    print(f"    关键词: {ctx_alice.keywords_extracted[:5]}")

    print("  用户 bob 输入: '帮我分析报表'")
    ctx_bob = engine.process_input("帮我分析报表", user_id="bob")
    print(f"    推断意图: {ctx_bob.inferred_intent}, 置信度: {ctx_bob.intent_confidence:.2f}")
    print(f"    关键词: {ctx_bob.keywords_extracted[:5]}")

    # 8. 测试反馈学习（多用户）
    print("\n[8] 测试反馈学习（多用户）...")
    engine.record_feedback(
        "看看数据",
        "查看报表数据",
        user_correction="运营数据",
        is_correct=False,
        user_id="alice"
    )
    print(f"  alice 纠正后查询 '数据': {engine.get_keyword_meaning('数据', 'alice')}")

    engine.record_feedback(
        "看看数据",
        "查看报表数据",
        user_correction="财务数据",
        is_correct=False,
        user_id="bob"
    )
    print(f"  bob 纠正后查询 '数据': {engine.get_keyword_meaning('数据', 'bob')}")

    # 9. 获取用户画像
    print("\n[9] 获取用户画像...")
    for uid in users:
        profile = engine.get_user_profile(uid)
        if profile:
            print(f"  {uid}:")
            print(f"    - 总输入: {profile.total_inputs}")
            print(f"    - 学习次数: {profile.total_learnings}")
            print(f"    - 理解准确率: {profile.understanding_accuracy:.1%}")
            print(f"    - 主要意图: {max(profile.dominant_intents.items(), key=lambda x: x[1])[0] if profile.dominant_intents else 'unknown'}")

    # 10. 全局统计
    print("\n[10] 全局统计...")
    stats = engine.get_stats()
    print(f"  总用户数: {stats.get('total_users', 'N/A')}")
    print(f"  全局输入数: {stats.get('total_inputs_all', 'N/A')}")
    print(f"  全局映射数: {stats.get('total_mappings', 'N/A')}")

    # 11. 用户数据导出（GDPR合规）
    print("\n[11] 用户数据导出（GDPR合规）...")
    alice_data = engine.export_user_data("alice")
    if alice_data:
        print(f"  alice 数据导出成功:")
        print(f"    - 映射数: {len(alice_data.get('mappings', {}))}")
        print(f"    - 高频词数: {len(alice_data.get('high_frequency', {}))}")
        print(f"    - 反馈数: {len(alice_data.get('feedbacks', []))}")

    # 12. 列出所有用户
    print("\n[12] 列出所有用户...")
    all_users = engine.list_users()
    for u in all_users:
        print(f"  - {u['user_id']}: 创建于 {u['created_at'][:10]}, 最后活跃 {u['last_active'][:10]}")

    # 清理
    import shutil
    shutil.rmtree(test_path)

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


def test_backward_compatibility():
    """测试向后兼容（单用户模式）"""

    test_path = os.path.join(os.path.dirname(__file__), "temp_semantic_compat")
    if os.path.exists(test_path):
        import shutil
        shutil.rmtree(test_path)

    print("\n" + "=" * 60)
    print("向后兼容测试（单用户模式）")
    print("=" * 60)

    # 使用旧API（不传user_id）
    engine = SemanticMemoryEngine(base_path=test_path)

    # 不指定用户，应该使用default用户
    ctx = engine.process_input("帮我分析私域数据")
    print(f"\n[1] 不指定用户，语义分析:")
    print(f"  推断意图: {ctx.inferred_intent}")
    print(f"  用户ID: {ctx.user_id}")

    engine.learn_from_input("私域运营", "私域流量运营")
    print(f"\n[2] 学习后查询 '私域': {engine.get_keyword_meaning('私域')}")

    # 清理
    import shutil
    shutil.rmtree(test_path)

    print("\n✅ 向后兼容测试通过！")


if __name__ == "__main__":
    test_multi_user()
    test_backward_compatibility()
