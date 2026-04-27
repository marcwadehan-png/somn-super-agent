#!/usr/bin/env python3
"""
Somn CLI - 命令行入口
支持从终端直接调用 Somn 智能体

用法:
  # 交互式对话（REPL）
  python somn_cli.py

  # 单次查询
  python somn_cli.py -q "茅台为什么永垂不朽"

  # 带上下文查询
  python somn_cli.py -q "帮我制定增长策略" --industry saas_b2b

  # 查看系统状态
  python somn_cli.py --status

  # 列出所有解决方案
  python somn_cli.py --solutions

  # 健康检查
  python somn_cli.py --health
"""

import sys
import os
import argparse
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def create_agent():
    """创建 AgentCore 实例"""
    from src.core.memory_system import MemorySystem
    from src.core.knowledge_base import KnowledgeBase
    from src.core.agent_core import AgentCore

    memory = MemorySystem()
    kb = KnowledgeBase()
    agent = AgentCore(memory, kb)
    return agent


def query_mode(agent, query: str, industry: str = None):
    """单次查询模式"""
    start = time.time()
    try:
        context = {}
        if industry:
            context["industry"] = industry

        response = agent.process_input(query, context=context)
        elapsed = time.time() - start

        print(f"\n{response}\n")
        print(f"⏱ {elapsed:.2f}s")
    except KeyboardInterrupt:
        print("\n[已中断]")
    except Exception as e:
        print(f"\n❌ 错误: {e}")


def repl_mode(agent):
    """交互式对话模式（REPL）"""
    print("=" * 60)
    print("  Somn CLI - 命令行智能体")
    print("  输入问题开始对话，Ctrl+C 或输入 quit/exit 退出")
    print("=" * 60)
    print()

    while True:
        try:
            user_input = input("你: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n再见。")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("再见。")
            break

        if user_input.lower() == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue

        if user_input.lower() == "status":
            status = agent.get_learning_status()
            print(f"\n📊 系统状态:")
            print(f"  会话交互次数: {status['session_interactions']}")
            print(f"  学习系统: {'✅' if status['learning_system_available'] else '❌'}")
            print(f"  迁移模块: {'✅' if status['migrated_modules_available'] else '❌'}")
            print(f"  可用功能: {', '.join(status['available_features'])}")
            print()
            continue

        start = time.time()
        try:
            response = agent.process_input(user_input)
            elapsed = time.time() - start
            print(f"\nSomn: {response}\n")
            if elapsed > 1:
                print(f"⏱ {elapsed:.2f}s")
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")


def show_status(agent):
    """显示系统状态"""
    print("=" * 60)
    print("  Somn 系统状态")
    print("=" * 60)

    status = agent.get_learning_status()
    print(f"\n📊 核心状态:")
    print(f"  会话交互次数: {status['session_interactions']}")
    print(f"  学习系统: {'✅ 可用' if status['learning_system_available'] else '❌ 不可用'}")
    print(f"  迁移模块: {'✅ 可用' if status['migrated_modules_available'] else '❌ 不可用'}")
    print(f"  迁移模块就绪: {'✅' if status.get('migrated_modules_ready') else '❌'}")

    print(f"\n🔧 可用功能:")
    for feat in status.get("available_features", []):
        print(f"  • {feat}")

    if agent.somn_core:
        print(f"\n🧠 Somn 主链: ✅ 已加载")
    else:
        print(f"\n🧠 Somn 主链: ❌ 未加载")

    if agent.persona:
        print(f"🎭 人设引擎: ✅ 已加载")
    else:
        print(f"🎭 人设引擎: ❌ 未加载")

    if hasattr(agent, "emotion_wave") and agent.emotion_wave:
        print(f"🎭 情绪波动: ✅ {agent.emotion_wave.current_mood.value}")
    else:
        print(f"🎭 情绪波动: ❌ 未加载")

    print()


def show_solutions(agent):
    """列出所有可用解决方案"""
    if not agent.somn_core:
        print("❌ Somn 主链未加载，无法获取解决方案列表")
        return

    from src.somn import Somn, SomnConfig

    config = SomnConfig(enable_web_search=False, enable_ml_engine=False)
    somn = Somn(config)
    result = somn.list_all_solutions()

    print("=" * 60)
    print(f"  Somn 解决方案库 (共 {result['total_count']} 个)")
    print("=" * 60)

    for sol in result["solutions"]:
        print(f"\n  📦 {sol['name']}")
        print(f"     类型: {sol['type']} | 分类: {sol['category']}")
        print(f"     {sol['description']}")

    print()


def health_check(agent):
    """健康检查"""
    from src.somn import Somn, SomnConfig

    config = SomnConfig(enable_web_search=False, enable_ml_engine=False)
    somn = Somn(config)
    result = somn.health_check()

    print("=" * 60)
    print("  Somn 健康检查")
    print("=" * 60)
    print(f"\n  状态: {'✅ 健康' if result['status'] == 'healthy' else '⚠️ 部分组件不可用'}")
    print(f"  组件: {result['healthy_components']}/{result['total_components']} 正常")
    print(f"  解决方案: {result['solution_count']} 个")

    if result["status"] != "healthy":
        print(f"\n  ⚠️ 异常组件:")
        for name, ok in result["checks"].items():
            if not ok:
                print(f"    ❌ {name}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Somn CLI - 命令行智能体",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python somn_cli.py                           # 交互式对话
  python somn_cli.py -q "茅台为什么永垂不朽"      # 单次查询
  python somn_cli.py -q "增长策略" --industry ecommerce  # 带行业上下文
  python somn_cli.py --status                   # 查看状态
  python somn_cli.py --health                   # 健康检查
  python somn_cli.py --solutions                # 列出解决方案
        """,
    )

    parser.add_argument(
        "-q", "--query", type=str, help="单次查询模式（查询后退出）"
    )
    parser.add_argument(
        "--industry", type=str, default=None, help="指定行业（与 -q 配合使用）"
    )
    parser.add_argument(
        "--status", action="store_true", help="显示系统状态"
    )
    parser.add_argument(
        "--health", action="store_true", help="执行健康检查"
    )
    parser.add_argument(
        "--solutions", action="store_true", help="列出所有可用解决方案"
    )

    args = parser.parse_args()

    # 创建智能体
    print("正在初始化 Somn...")
    agent = create_agent()
    print("初始化完成。\n")

    # 根据参数执行不同模式
    if args.query:
        query_mode(agent, args.query, args.industry)
    elif args.status:
        show_status(agent)
    elif args.health:
        health_check(agent)
    elif args.solutions:
        show_solutions(agent)
    else:
        repl_mode(agent)


if __name__ == "__main__":
    main()
