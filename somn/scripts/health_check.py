#!/usr/bin/env python3
"""
Somn v1.0.0 综合健康检查脚本
快速验证系统核心组件状态
"""
import sys
import os

# 添加项目路径 - 支持从不同目录运行
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)  # scripts/ -> 项目根目录
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'smart_office_assistant'))

def check_import(module_name, class_name=None):
    """检查模块导入"""
    try:
        module = __import__(module_name, fromlist=[class_name or ''])
        if class_name:
            cls = getattr(module, class_name, None)
            if cls:
                return True, f"{class_name} OK"
            return False, f"{class_name} 不存在"
        return True, f"{module_name} OK"
    except Exception as e:
        return False, f"{type(e).__name__}"

def main():
    os.chdir(project_root)  # 确保在项目根目录

    print("=" * 60)
    print("Somn v1.0.0 综合健康检查")
    print("=" * 60)
    print()

    results = []

    # 1. 包信息检查
    print("[1] 包信息")
    try:
        import smart_office_assistant
        version = getattr(smart_office_assistant, '__version__', '未知')
        print(f"    包版本: {version}")
        results.append(("包版本", version == "6.1.0"))
    except Exception as e:
        print(f"    FAIL: 包导入失败 - {e}")
        results.append(("包导入", False))

    print()

    # 2. 核心模块检查
    print("[2] 核心模块导入")
    modules = [
        ('src.core.somn_core', 'SomnCore'),
        ('src.intelligence.dispatcher', 'WisdomDispatcher'),
        ('src.intelligence.claws', 'ClawArchitect'),
        ('src.intelligence.dispatcher.wisdom_fusion_core', 'WisdomFusionCore'),
        ('src.intelligence.reasoning.deep_reasoning_engine', 'DeepReasoningEngine'),
        ('src.intelligence.wisdom_encoding', 'WisdomEncodingRegistry'),
    ]

    for module_name, class_name in modules:
        ok, msg = check_import(module_name, class_name)
        status = "OK" if ok else "FAIL"
        print(f"    [{status}] {class_name}")
        results.append((class_name, ok))

    print()

    # 3. 配置文件检查
    print("[3] 配置文件检查")
    configs = [
        'pyproject.toml',
        'pytest.ini',
        'smart_office_assistant/__init__.py',
    ]

    for cfg in configs:
        exists = os.path.exists(cfg)
        status = "OK" if exists else "MISSING"
        print(f"    [{status}] {cfg}")
        results.append((cfg, exists))

    print()

    # 4. 目录结构检查
    print("[4] 目录结构检查")
    dirs = [
        'smart_office_assistant/src',
        'smart_office_assistant/src/intelligence',
        'smart_office_assistant/src/core',
        'tests',
        'file',
        'docs',
    ]

    for d in dirs:
        exists = os.path.isdir(d)
        status = "OK" if exists else "MISSING"
        print(f"    [{status}] {d}/")
        results.append((d, exists))

    print()
    print("=" * 60)

    # 总结
    total = len(results)
    passed = sum(1 for _, ok in results if ok)

    print(f"结果: {passed}/{total} 通过")

    if passed == total:
        print("All checks passed!")
        return 0
    else:
        failed = [name for name, ok in results if not ok]
        print(f"Failed: {', '.join(failed)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
