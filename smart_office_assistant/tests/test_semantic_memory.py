"""
语义记忆引擎测试脚本
测试语义理解与关键词-语义映射功能
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from src.neural_memory.semantic_memory_engine import SemanticMemoryEngine, SomnSemanticIntegration



def test_semantic_understanding():
    """测试语义理解功能"""
    print("=" * 60)
    print("测试1: 语义理解")
    print("=" * 60)

    engine = SemanticMemoryEngine()

    test_cases = [
        "帮我分析一下私域流量的转化率",
        "怎么优化系统性能",
        "研究一下量子计算的发展趋势",
        "写一个Python脚本处理文件",
        "那个项目的进度怎么样了",
        "论证一下这个商业模式的可行性",
        "深入研究人工智能在医疗领域的应用"
    ]

    for text in test_cases:
        print(f"\n[输入] {text}")
        context = engine.process_input(text)

        print(f"  意图: {context.inferred_intent}")
        print(f"  置信度: {context.intent_confidence:.2f}")
        print(f"  关键词: {context.keywords_extracted}")

        if context.matched_mappings:
            print(f"  已匹配映射: {len(context.matched_mappings)} 条")

        if context.needs_clarification:
            print(f"  ⚠️ 需要澄清: {context.clarification_question}")

        # 打印推理链
        print("  推理链:")
        for step in context.reasoning_chain[:3]:
            print(f"    {step}")


def test_learning():
    """测试学习功能"""
    print("\n" + "=" * 60)
    print("测试2: 学习功能")
    print("=" * 60)

    engine = SemanticMemoryEngine()

    # 模拟多次输入同一主题，建立高频词
    learning_pairs = [
        ("帮我分析私域运营数据", "需要分析私域相关运营指标数据"),
        ("私域用户怎么获取", "询问私域流量的获取方法"),
        ("私域和公域的区别是什么", "了解私域与公域的概念差异"),
        ("私域运营策略有哪些", "学习私域运营的具体方法"),
        ("私域转化率怎么算", "计算私域流量转化率的方法"),
    ]

    for input_text, meaning in learning_pairs:
        print(f"\n[学习] {input_text}")
        print(f"  理解: {meaning}")
        engine.learn_from_input(input_text, meaning)

    # 查询学习结果
    print("\n" + "-" * 40)
    print("查询学习结果:")
    meaning = engine.get_keyword_meaning("私域")
    print(f"  '私域' 的已知语义: {meaning}")

    # 搜索功能
    print("\n  搜索 '运营' 相关映射:")
    results = engine.search_mappings("运营")
    for r in results[:3]:
        print(f"    - {r.keyword} → {r.primary_meaning}")


def test_feedback_learning():
    """测试反馈学习功能"""
    print("\n" + "=" * 60)
    print("测试3: 反馈学习")
    print("=" * 60)

    engine = SemanticMemoryEngine()

    # 预先学习一个映射
    engine.learn_from_input("看看那个报表", "查看某个报表数据")

    # 查询初始状态
    initial_mapping = engine.get_keyword_meaning("报表")
    print(f"\n[初始] '报表' 的语义: {initial_mapping}")

    # 模拟用户纠正
    print("\n[反馈] 用户纠正: 系统理解为'查看报表'，实际想看'销售数据报表'")
    engine.record_feedback(
        user_input="看看那个报表",
        system_understanding="查看某个报表数据",
        user_correction="查看销售数据报表",
        is_correct=False
    )

    # 查询更新后的状态
    updated_mapping = engine.get_keyword_meaning("报表")
    print(f"\n[更新后] '报表' 的语义: {updated_mapping}")

    # 查询统计
    stats = engine.get_stats("default")
    print(f"\n理解准确率: {stats['understanding_accuracy']*100:.1f}%")



def test_somn_integration():
    """测试与 SomnCore 的集成"""
    print("\n" + "=" * 60)
    print("测试4: SomnCore 集成")
    print("=" * 60)

    try:
        from src.core.somn_core import SomnCore

        print("\n初始化 SomnCore（含语义记忆）...")
        # 使用临时路径避免污染已有数据
        import tempfile
        temp_dir = tempfile.mkdtemp()

        somn = SomnCore(base_path=temp_dir)

        # 检查语义记忆引擎是否加载
        if somn.semantic_memory:
            print("✅ 语义记忆引擎已加载")

            # 测试语义分析
            print("\n运行语义分析测试...")
            result = somn._run_semantic_analysis("帮我分析一下私域运营数据")
            print(f"  意图: {result.get('inferred_intent')}")
            print(f"  置信度: {result.get('intent_confidence', 0):.2f}")
            print(f"  关键词: {result.get('keywords', [])[:5]}")

            # 获取统计
            stats = somn.get_semantic_memory_stats()
            print(f"\n语义记忆统计:")
            print(f"  处理输入总数: {stats.get('total_inputs_processed', 0)}")
            print(f"  学习次数: {stats.get('total_learnings', 0)}")
        else:
            print("⚠️ 语义记忆引擎未启用（可能缺少依赖）")

    except ImportError as e:
        print(f"⚠️ 无法导入 SomnCore: {e}")
    except Exception as e:
        print(f"⚠️ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("=" * 60)
    print("语义记忆引擎 - 完整测试套件")
    print("=" * 60)

    test_semantic_understanding()
    test_learning()
    test_feedback_learning()
    test_somn_integration()

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
