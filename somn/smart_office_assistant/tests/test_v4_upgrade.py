"""神之架构V4.0.0 升级验证脚本"""
import sys
import traceback
from pathlib import Path

# 动态项目路径
_PROJECT_ROOT = Path(__file__).resolve().parent.parent

def test_module(name, import_path):
    """测试单个模块导入"""
    try:
        mod = __import__(import_path, fromlist=[''])
        # 获取版本
        version = getattr(mod, '__version__', 'N/A')
        return True, version, None
    except Exception as e:
        return False, str(e), traceback.format_exc()

def main():
    tests = [
        ("_court_positions", "src.intelligence.engines.cloning._court_positions"),
        ("_dispatch_court", "src.intelligence.dispatcher.wisdom_dispatch._dispatch_court"),
        ("_dispatch_enums", "src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums"),
        ("_dispatch_mapping", "src.intelligence.dispatcher.wisdom_dispatch._dispatch_mapping"),
        ("_hanlin_review", "src.intelligence.dispatcher.wisdom_dispatch._hanlin_review"),
        ("_imperial_library", "src.intelligence.dispatcher.wisdom_dispatch._imperial_library"),
        ("_decision_congress", "src.intelligence.dispatcher.wisdom_dispatch._decision_congress"),
        ("_daqin_metrics", "src.intelligence.dispatcher.wisdom_dispatch._daqin_metrics"),
        ("_whip_engine", "src.intelligence.dispatcher.wisdom_dispatch._whip_engine"),
    ]

    passed = 0
    failed = 0
    results = []

    for name, path in tests:
        ok, info, err = test_module(name, path)
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1
        results.append(f"[{status}] {name}: {info}")
        if err:
            results.append(f"  ERROR: {err[:500]}")

    # Count key metrics
    try:
        from src.intelligence.dispatcher.wisdom_dispatch._dispatch_enums import WisdomSchool, ProblemType
        results.append(f"\nWisdomSchool count: {len(WisdomSchool)}")
        results.append(f"ProblemType count: {len(ProblemType)}")
    except Exception as e:
        results.append(f"\nFailed to count enums: {e}")

    try:
        from src.intelligence.engines.cloning._court_positions import CourtPositionRegistry
        reg = CourtPositionRegistry()
        stats = reg.get_stats()
        results.append(f"Position count: {stats.get('total_positions', 'N/A')}")
    except Exception as e:
        results.append(f"Failed to count positions: {e}")

    summary = f"\n{'='*50}\nV4 Upgrade Verification: {passed}/{passed+failed} PASSED\n{'='*50}"
    results.append(summary)

    output = "\n".join(results)
    print(output)

    with open(_PROJECT_ROOT / "v4_verify_result.txt", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    main()
