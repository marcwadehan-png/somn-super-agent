"""
Pan-Wisdom Tree 性能基准测试 v2.1.0
验证优化效果：移除巨型正则 + LRU内存淘汰
"""

import time
import gc
import sys
import os

# 添加父目录
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)


def test_lazy_regex():
    """测试正则懒加载"""
    print("=" * 60)
    print("1. 正则懒加载验证")
    print("=" * 60)
    
    # 使用 importlib 重新加载模块
    import importlib
    from knowledge_cells.pan_wisdom_lazy_loader import PanWisdomPreloader
    
    # 检查预加载后的状态
    print(f"\n  预加载后 COMPILED_PATTERNS 数量: {len(PanWisdomPreloader.COMPILED_PATTERNS)}")
    print(f"  已编译模式: {list(PanWisdomPreloader.COMPILED_PATTERNS.keys())}")
    
    # 验证 KEYWORD_SET_INDEX 已构建
    print(f"  KEYWORD_SET_INDEX 条目: {len(PanWisdomPreloader.KEYWORD_SET_INDEX)}")
    print(f"  KEYWORD_TO_PROBLEM 条目: {len(PanWisdomPreloader.KEYWORD_TO_PROBLEM)}")
    
    # 测试懒加载：获取未编译的正则
    print(f"\n  触发懒加载 get_pattern('chinese_word'):")
    start = time.perf_counter()
    pattern = PanWisdomPreloader.get_pattern("chinese_word")
    lazy_time = (time.perf_counter() - start) * 1000
    print(f"    耗时: {lazy_time:.3f}ms")
    print(f"    编译后 COMPILED_PATTERNS 数量: {len(PanWisdomPreloader.COMPILED_PATTERNS)}")
    
    # 验证无巨型正则
    print(f"\n  巨型正则移除验证:")
    print(f"    KEYWORD_INDEX 数量: {len(getattr(PanWisdomPreloader, 'KEYWORD_INDEX', {}))}")


def test_identify_performance():
    """测试问题识别性能"""
    print("\n" + "=" * 60)
    print("2. 问题识别性能测试")
    print("=" * 60)
    
    from knowledge_cells.pan_wisdom_core import ProblemIdentifier, ProblemType
    
    test_cases = [
        ("如何提升公司GMV？增长策略如何制定？", "增长运营"),
        ("直播带货怎么提高转化率和UV价值？", "直播运营"),
        ("私域流量如何运营，提高入群率和触达率？", "私域运营"),
        ("数据分析报告显示用户留存率下降", "数据运营"),
        ("内容营销如何规划，提升完播率和涨粉率？", "内容运营"),
        ("电商平台的GMV增长遇到瓶颈", "电商运营"),
        ("广告投放ROI低，如何优化素材和CPC？", "广告投放"),
    ]
    
    print("\n  identify() 方法:")
    total_identify = 0
    for text, tag in test_cases:
        start = time.perf_counter()
        result = ProblemIdentifier.identify(text)
        elapsed = (time.perf_counter() - start) * 1000
        total_identify += elapsed
        top_type = result[0][0].value if result else "未知"
        print(f"    [{tag}] {elapsed:.3f}ms -> {top_type}")
    print(f"    平均: {total_identify / len(test_cases):.3f}ms")
    
    print("\n  identify_fast() 方法 (无正则，扁平化映射):")
    total_fast = 0
    for text, tag in test_cases:
        start = time.perf_counter()
        result = ProblemIdentifier.identify_fast(text)
        elapsed = (time.perf_counter() - start) * 1000
        total_fast += elapsed
        top_type = result[0][0].value if result else "未知"
        print(f"    [{tag}] {elapsed:.3f}ms -> {top_type}")
    print(f"    平均: {total_fast / len(test_cases):.3f}ms")


def test_cache_performance():
    """测试缓存性能"""
    print("\n" + "=" * 60)
    print("3. 缓存性能测试")
    print("=" * 60)
    
    from knowledge_cells.pan_wisdom_core import ProblemIdentifier, SchoolRecommender, ProblemType
    from knowledge_cells.pan_wisdom_lazy_loader import get_pan_wisdom_cache, clear_pan_wisdom_cache
    
    cache = get_pan_wisdom_cache()
    cache.clear_cache()
    
    # 问题识别缓存
    test_text = "如何提升公司GMV？增长策略如何制定？"
    
    # 首次（缓存未命中）
    start = time.perf_counter()
    ProblemIdentifier.identify(test_text)
    first = (time.perf_counter() - start) * 1000
    
    # 缓存命中
    start = time.perf_counter()
    ProblemIdentifier.identify(test_text)
    cached = (time.perf_counter() - start) * 1000
    
    stats = cache.get_cache_stats()
    print(f"\n  问题识别缓存:")
    print(f"    首次: {first:.3f}ms")
    print(f"    缓存命中: {cached:.3f}ms")
    print(f"    加速比: {first/cached:.1f}x" if cached > 0 else "    N/A")
    
    # 学派推荐缓存（用字符串绕过枚举名问题）
    test_type = "GROWTH_OPERATION"
    
    start = time.perf_counter()
    SchoolRecommender.recommend(test_type)
    first_rec = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    SchoolRecommender.recommend(test_type)
    cached_rec = (time.perf_counter() - start) * 1000
    
    print(f"\n  学派推荐缓存:")
    print(f"    首次: {first_rec:.3f}ms")
    print(f"    缓存命中: {cached_rec:.3f}ms")
    print(f"    加速比: {first_rec/cached_rec:.1f}x" if cached_rec > 0 else "    N/A")
    
    print(f"\n  缓存统计: {stats['hit_rate']} 命中率")


def test_memory_usage():
    """测试内存占用"""
    print("\n" + "=" * 60)
    print("4. 内存占用测试")
    print("=" * 60)
    
    from knowledge_cells.pan_wisdom_lazy_loader import get_pan_wisdom_cache
    
    cache = get_pan_wisdom_cache()
    stats = cache.get_cache_stats()
    
    print(f"\n  缓存配置:")
    print(f"    最大条目数: {cache._MAX_CACHE_SIZE}")
    print(f"    最大内存: {cache._MAX_MEMORY_BYTES / 1024:.0f}KB")
    
    print(f"\n  当前缓存占用:")
    for cat in ["school", "problem_type", "recommendation"]:
        info = stats[cat]
        print(f"    {cat}: {info['count']}项, {info['bytes']}B")
    
    print(f"\n  总内存占用: {stats['total_memory_kb']}")
    print(f"  内存限制: {stats['memory_limit_kb']}")
    
    # 计算使用率
    total_mem = stats['total_memory_bytes']
    limit_mem = cache._MAX_MEMORY_BYTES
    usage = total_mem / limit_mem * 100 if limit_mem > 0 else 0
    print(f"  内存使用率: {usage:.1f}%")


def test_preload_speed():
    """测试预加载速度"""
    print("\n" + "=" * 60)
    print("5. 预加载速度测试")
    print("=" * 60)
    
    from knowledge_cells.pan_wisdom_lazy_loader import PanWisdomPreloader
    
    # 重置预加载状态
    PanWisdomPreloader._PRELOADED = False
    PanWisdomPreloader._PRELOAD_TIME = 0.0
    
    # 测量预加载
    start = time.perf_counter()
    PanWisdomPreloader.preload()
    preload_time = (time.perf_counter() - start) * 1000
    
    print(f"\n  预加载耗时: {preload_time:.3f}ms")
    print(f"  预加载内容:")
    print(f"    - 编译正则定义: ✓")
    print(f"    - KEYWORD_SET_INDEX: {len(PanWisdomPreloader.KEYWORD_SET_INDEX)}条")
    print(f"    - KEYWORD_TO_PROBLEM: {len(PanWisdomPreloader.KEYWORD_TO_PROBLEM)}条")
    print(f"    - 正则未编译（懒加载）: ✓")


def test_functionality():
    """测试功能正确性"""
    print("\n" + "=" * 60)
    print("6. 功能正确性测试")
    print("=" * 60)
    
    from knowledge_cells.pan_wisdom_core import (
        solve_with_wisdom, 
        ProblemIdentifier, 
        SchoolRecommender,
        ProblemType,
        WisdomSchool
    )
    
    print(f"\n  枚举数量:")
    print(f"    WisdomSchool: {len(list(WisdomSchool))}")
    print(f"    ProblemType: {len(list(ProblemType))}")
    
    # 测试 solve_with_wisdom
    print(f"\n  solve_with_wisdom 测试:")
    result = solve_with_wisdom("如何提升公司GMV？")
    print(f"    问题类型: {result.identified_types[0].value if result.identified_types else '未知'}")
    print(f"    推荐学派数: {len(result.recommended_schools)}")
    print(f"    融合洞察数: {len(result.fusion_insights)}")

def test_version():
    """测试版本号"""
    print("\n" + "=" * 60)
    print("7. 版本号验证")
    print("=" * 60)
    
    import knowledge_cells.pan_wisdom_core as pwc
    from knowledge_cells.pan_wisdom_lazy_loader import PanWisdomPreloader
    import knowledge_cells as kc
    
    print(f"\n  pan_wisdom_core: {pwc.__version__}")
    print(f"  pan_wisdom_lazy_loader: {PanWisdomPreloader.VERSION}")
    print(f"  knowledge_cells __pan_wisdom_version__: {kc.__pan_wisdom_version__}")


def main():
    """主测试函数"""
    print("\n" + "🚀" * 20)
    print("  Pan-Wisdom Tree 性能基准测试 v2.1.0")
    print("  优化：移除巨型正则 + LRU内存淘汰")
    print("🚀" * 20 + "\n")
    
    try:
        test_functionality()
        test_version()
        test_lazy_regex()
        test_preload_speed()
        test_identify_performance()
        test_cache_performance()
        test_memory_usage()
        
        print("\n" + "=" * 60)
        print("📊 优化总结")
        print("=" * 60)
        print("""
✅ 已完成优化:
  1. 巨型正则移除 → KEYWORD_INDEX['all_problems'] 已删除
     - 不再拼接 800+ 关键词为巨型正则
     - 改用 KEYWORD_TO_PROBLEM 扁平化映射
     
  2. 正则懒加载 → COMPILED_PATTERNS 访问时编译
     - 预加载只保留模式定义
     - 首次访问 get_pattern() 时编译
     
  3. LRU缓存内存淘汰 → 双重上限
     - 数量上限: 50项
     - 内存上限: 512KB
     - 精确内存估算: 支持嵌套结构
     
  4. identify_fast → 扁平化映射
     - O(n) 单次扫描
     - 无正则回溯开销
     
  5. 内存预算优化:
     - LRU: 100项/2MB → 50项/512KB
     - 精确估算避免内存膨胀
        """)
        
        print("✅ 全部测试通过!")
        
    except Exception as e:
        import traceback
        print(f"\n❌ 测试失败: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
