#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 web 集成系统当前状态
"""

import sys
import os

# 设置导入路径
sys.path.insert(0, 'd:/AI/somn')
sys.path.insert(0, 'd:/AI/somn/knowledge_cells')
sys.path.insert(0, 'd:/AI/somn/smart_office_assistant/src')

print("=" * 60)
print("Somn Web 集成系统状态检查")
print("=" * 60)

# 1. 检查 web_search_engine.py
print("\n[1] 检查 web_search_engine.py")
try:
    from web_search_engine import (
        is_online,
        WebSearchEngine,
        SearchResult,
        SearchResponse,
        search_web,
    )
    print("  OK: web_search_engine 导入成功")
    print(f"  - is_online 函数: 存在")
    print(f"  - WebSearchEngine 类: 存在")
    print(f"  - search_web 函数: 存在")
except Exception as e:
    print(f"  FAIL: {e}")

# 2. 检查联网状态
print("\n[2] 检查联网状态")
try:
    online = is_online()
    print(f"  联网状态: {'在线' if online else '离线'}")
except Exception as e:
    print(f"  FAIL: {e}")

# 3. 检查 web_integration.py
print("\n[3] 检查 web_integration.py")
try:
    from web_integration import (
        RefuteCoreWeb,
        NeuralMemoryWeb,
        TianShuWeb,
        TrackAWeb,
        TrackBWeb,
        WebSearchMixin,
        search_with_fallback,
        should_trigger_web_search,
    )
    print("  OK: web_integration 导入成功")
    print(f"  - RefuteCoreWeb: 存在")
    print(f"  - NeuralMemoryWeb: 存在")
    print(f"  - TianShuWeb: 存在")
    print(f"  - TrackAWeb: 存在")
    print(f"  - TrackBWeb: 存在")
except Exception as e:
    print(f"  FAIL: {e}")

# 4. 检查 RefuteCoreWeb 实例化
print("\n[4] 检查 RefuteCoreWeb 实例化")
try:
    rcw = RefuteCoreWeb()
    print(f"  OK: RefuteCoreWeb() 实例化成功")
    print(f"  - is_enabled(): {rcw.is_enabled()}")
except Exception as e:
    print(f"  FAIL: {e}")

# 5. 检查 divine_oversight 集成
print("\n[5] 检查 divine_oversight 集成")
try:
    from divine_oversight import get_oversight, DivineTrackOversight
    oversight = get_oversight()
    print(f"  OK: get_oversight() 成功")
    print(f"  - DivineTrackOversight 版本: {DivineTrackOversight.VERSION}")
    
    if hasattr(oversight, 'refute_web'):
        print(f"  - refute_web 属性: 存在")
        rw = oversight.refute_web
        if rw is not None:
            print(f"  - refute_web 实例化: 成功")
            print(f"  - refute_web.is_enabled(): {rw.is_enabled()}")
        else:
            print(f"  - refute_web 实例化: None (可能离线或导入失败)")
    else:
        print(f"  - refute_web 属性: 不存在")
except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()

# 6. 检查 should_trigger_web_search
print("\n[6] 检查触发关键词检测")
try:
    test_cases = [
        ("2025年AI发展趋势", True),
        ("如何提升用户留存", False),
        ("最新新闻报道", True),
        ("分析市场竞争策略", False),
    ]
    
    for text, expected in test_cases:
        should, keyword = should_trigger_web_search(text)
        status = "OK" if should == expected else "FAIL"
        print(f"  [{status}] '{text}' -> 触发:{should}, 关键词:'{keyword}'")
except Exception as e:
    print(f"  FAIL: {e}")

# 7. 检查 search_with_fallback
print("\n[7] 检查 search_with_fallback")
try:
    result = search_with_fallback("人工智能发展", max_results=3)
    print(f"  OK: search_with_fallback() 调用成功")
    print(f"  - success: {result.get('success')}")
    print(f"  - source: {result.get('source')}")
    print(f"  - online: {result.get('online')}")
    print(f"  - results count: {len(result.get('results', []))}")
    
    if result.get('results'):
        for i, r in enumerate(result['results'][:2]):
            title = r.get('title', 'N/A')[:50]
            print(f"    [{i+1}] {title}...")
except Exception as e:
    print(f"  FAIL: {e}")
    import traceback
    traceback.print_exc()

# 8. 检查 TrackA/TrackB 中的 web 集成
print("\n[8] 检查 TrackA/TrackB web 集成")
try:
    # 检查 track_a.py 中是否有 web 集成代码
    track_a_path = "d:/AI/somn/smart_office_assistant/src/intelligence/dual_track/track_a.py"
    if os.path.exists(track_a_path):
        with open(track_a_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'TrackAWeb' in content:
                print("  OK: track_a.py 包含 TrackAWeb 集成代码")
            if '_get_track_a_web' in content:
                print("  OK: track_a.py 包含 _get_track_a_web() 懒加载函数")
    
    # 检查 track_b.py
    track_b_path = "d:/AI/somn/smart_office_assistant/src/intelligence/dual_track/track_b.py"
    if os.path.exists(track_b_path):
        with open(track_b_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'TrackBWeb' in content:
                print("  OK: track_b.py 包含 TrackBWeb 集成代码")
            if '_get_track_b_web' in content:
                print("  OK: track_b.py 包含 _get_track_b_web() 懒加载函数")
except Exception as e:
    print(f"  FAIL: {e}")

print("\n" + "=" * 60)
print("检查完成")
print("=" * 60)
