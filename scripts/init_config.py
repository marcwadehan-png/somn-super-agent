#!/usr/bin/env python3
"""
Somn AI 配置引导脚本 v2.0
=========================
帮助用户完成首次配置

用法:
  python scripts/init_config.py        # 交互式配置
  python scripts/init_config.py --reset  # 重置为默认配置
  python scripts/init_config.py --check  # 检查当前配置

版本: 2.0.0
日期: 2026-04-24
"""

import sys
import os
import shutil
from pathlib import Path
import argparse

# ───────────────────────────────────────────────────────────────
# 路径初始化
# ───────────────────────────────────────────────────────────────

def setup_paths():
    """初始化项目路径"""
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    if str(project_root / "smart_office_assistant") not in sys.path:
        sys.path.insert(0, str(project_root / "smart_office_assistant"))
    if str(project_root / "smart_office_assistant" / "src") not in sys.path:
        sys.path.insert(0, str(project_root / "smart_office_assistant" / "src"))

    return project_root

PROJECT_ROOT = setup_paths()


# ───────────────────────────────────────────────────────────────
# 配置管理
# ───────────────────────────────────────────────────────────────

CONFIG_TEMPLATE = PROJECT_ROOT / "config" / "local_config.yaml"
CONFIG_FILE = PROJECT_ROOT / "config" / "config.yaml"


def check_config():
    """检查当前配置"""
    print("=" * 60)
    print("  Somn AI 配置检查")
    print("=" * 60)
    print()

    # 检查配置文件
    if CONFIG_FILE.exists():
        print(f"  [OK] 配置文件存在: {CONFIG_FILE}")
        # 读取并显示关键配置
        try:
            import yaml
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            print()
            print("  系统信息:")
            print(f"    版本: {config.get('system', {}).get('version', 'N/A')}")
            print(f"    环境: {config.get('system', {}).get('environment', 'N/A')}")
            print(f"    调试模式: {config.get('system', {}).get('debug', False)}")

            print()
            print("  LLM配置:")
            print(f"    默认模式: {config.get('llm', {}).get('default_mode', 'local')}")
            print(f"    默认模型: {config.get('llm', {}).get('default_model', 'local-default')}")

            local_api = config.get('llm', {}).get('local', {}).get('api_base', '')
            print(f"    本地API: {local_api if local_api else '未配置'}")

            print()
            print("  功能开关:")
            for key, enabled in config.get('features', {}).items():
                status = "启用" if enabled else "禁用"
                print(f"    {key}: {status}")

            print()
            return True
        except Exception as e:
            print(f"  [错误] 读取配置失败: {e}")
            return False
    else:
        print(f"  [警告] 配置文件不存在")
        print(f"  提示: 运行 python scripts/init_config.py 进行首次配置")
        return False


def reset_config():
    """重置配置为默认"""
    print("=" * 60)
    print("  Somn AI 配置重置")
    print("=" * 60)
    print()

    # 备份现有配置
    if CONFIG_FILE.exists():
        backup = CONFIG_FILE.with_suffix('.yaml.backup')
        shutil.copy2(CONFIG_FILE, backup)
        print(f"  [OK] 已备份现有配置到: {backup}")

    # 复制模板
    if CONFIG_TEMPLATE.exists():
        shutil.copy2(CONFIG_TEMPLATE, CONFIG_FILE)
        print(f"  [OK] 已重置为默认配置: {CONFIG_FILE}")
    else:
        print(f"  [错误] 配置模板不存在: {CONFIG_TEMPLATE}")
        return False

    print()
    print("  配置已重置，请编辑 config/config.yaml 调整设置")
    return True


def interactive_config():
    """交互式配置引导"""
    print("=" * 60)
    print("  Somn AI 首次配置向导")
    print("=" * 60)
    print()

    # 复制模板（如果不存在）
    if not CONFIG_FILE.exists():
        if CONFIG_TEMPLATE.exists():
            shutil.copy2(CONFIG_TEMPLATE, CONFIG_FILE)
            print(f"  [OK] 已创建配置文件: {CONFIG_FILE}")
        else:
            print(f"  [错误] 配置模板不存在")
            return False
    else:
        print(f"  [OK] 使用现有配置: {CONFIG_FILE}")

    print()
    print("  当前配置参数（直接回车使用默认值）:")
    print()

    try:
        import yaml

        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        # LLM模式
        print("  1. LLM运行模式:")
        print("     local = 本地优先（推荐，需要Ollama）")
        print("     cloud = 云端优先（需要API密钥）")
        print("     auto  = 自动选择")
        mode = input(f"     选择 [默认: {config.get('llm', {}).get('default_mode', 'local')}]: ").strip()
        if mode:
            config.setdefault('llm', {})['default_mode'] = mode

        # 本地API
        print()
        print("  2. 本地API地址（Ollama默认: http://localhost:11434/v1）:")
        local_api = input(f"     输入地址 [默认: {config.get('llm', {}).get('local', {}).get('api_base', 'http://localhost:11434/v1')}]: ").strip()
        if local_api:
            config.setdefault('llm', {}).setdefault('local', {})['api_base'] = local_api

        # 调试模式
        print()
        debug_current = config.get('system', {}).get('debug', False)
        print(f"  3. 调试模式: {'是' if debug_current else '否'}")
        debug = input("     启用调试模式? (y/N): ").strip().lower()
        if debug == 'y':
            config.setdefault('system', {})['debug'] = True
        else:
            config.setdefault('system', {})['debug'] = False

        # 功能开关
        print()
        print("  4. 功能开关:")
        print("     (直接回车保持当前设置，输入数字切换)")

        features = config.setdefault('features', {})
        for key in ['enable_gui', 'enable_web_search', 'enable_ml_engine', 'enable_emotion_wave']:
            current = features.get(key, True)
            status = "启用" if current else "禁用"
            toggle = input(f"     {key}: {status} - 切换? (y/N): ").strip().lower()
            if toggle == 'y':
                features[key] = not current

        # 保存配置
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print()
        print("=" * 60)
        print("  配置完成！")
        print("=" * 60)
        print()
        print(f"  配置文件: {CONFIG_FILE}")
        print()
        print("  启动方式:")
        print("    Windows: 双击 start_independent.bat")
        print("    Linux/macOS: 运行 ./start_independent.sh")
        print("    Python: python start_independent.py")
        print()
        print("  或直接运行: python run.py --cli")
        print()

        return True

    except ImportError:
        print("  [错误] 需要PyYAML库: pip install pyyaml")
        return False
    except Exception as e:
        print(f"  [错误] 配置失败: {e}")
        import traceback
        traceback.print_exc()
        return False


# ───────────────────────────────────────────────────────────────
# 主入口
# ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Somn AI 配置引导脚本 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/init_config.py        # 交互式配置
  python scripts/init_config.py --check  # 检查当前配置
  python scripts/init_config.py --reset  # 重置为默认配置
        """,
    )
    parser.add_argument("--check", action="store_true", help="检查当前配置")
    parser.add_argument("--reset", action="store_true", help="重置为默认配置")

    args = parser.parse_args()

    print()

    if args.check:
        return 0 if check_config() else 1
    elif args.reset:
        return 0 if reset_config() else 1
    else:
        return 0 if interactive_config() else 1


if __name__ == "__main__":
    sys.exit(main() or 0)
