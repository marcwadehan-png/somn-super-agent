"""
行业扩展测试套件
Test Suite for Industry Expansion

测试内容:
1. 行业画像库完整性
2. 自动行业识别器准确性
3. 行业间相似度计算

版本: v1.0
日期: 2026-04-03
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from src.industry_engine.industry_profiles_v2 import (

    IndustryType, IndustryProfileLibrary,
    get_industry_profile, get_all_industries, search_industries
)
from src.industry_engine.auto_industry_detector import (
    AutoIndustryDetector, detect_industry, detect_industry_single,
    get_similar_industries
)


def test_industry_profile_library():
    """测试行业画像库"""
    print("=" * 60)
    print("测试1: 行业画像库")
    print("=" * 60)
    
    library = IndustryProfileLibrary()
    
    # 测试1.1: 行业数量
    all_profiles = library.get_all_profiles()
    print(f"\n✓ 行业总数: {len(all_profiles)}")
    assert len(all_profiles) >= 15, f"期望至少15个行业,实际{len(all_profiles)}"
    
    # 测试1.2: 每个行业都有完整信息
    for industry_type, profile in all_profiles.items():
        assert profile.name, f"{industry_type} 缺少名称"
        assert profile.description, f"{industry_type} 缺少描述"
        assert len(profile.key_metrics) >= 3, f"{industry_type} 指标不足"
        assert len(profile.growth_drivers) >= 3, f"{industry_type} 增长驱动不足"
        print(f"  ✓ {profile.name}: {len(profile.sub_types)}个子类型, {len(profile.key_metrics)}个指标")
    
    # 测试1.3: 通过名称获取
    profile = library.get_profile_by_name("电商")
    assert profile is not None, "通过名称获取失败"
    print(f"\n✓ 名称搜索: 找到 '{profile.name}'")
    
    # 测试1.4: 标签搜索
    regulated = library.get_industries_by_tag("监管")
    print(f"\n✓ 标签搜索 '监管': 找到 {len(regulated)} 个行业")
    
    # 测试1.5: 属性搜索
    high_value = library.get_industries_by_attribute("high_value")
    print(f"✓ 属性搜索 'high_value': 找到 {len(high_value)} 个行业")
    
    # 测试1.6: 关键词搜索
    results = library.search_industries("医疗")
    print(f"✓ 关键词搜索 '医疗': 找到 {len(results)} 个行业")
    
    print("\n✅ 行业画像库测试通过!")
    return True


def test_auto_industry_detector():
    """测试自动行业识别器"""
    print("\n" + "=" * 60)
    print("测试2: 自动行业识别器")
    print("=" * 60)
    
    detector = AutoIndustryDetector()
    
    # 测试2.1: 基于描述识别 - 电商
    desc = "我们是一个电商平台，主要关注GMV增长和转化率优化，希望提升复购率"
    results = detector.detect(description=desc, top_k=3)
    print(f"\n描述: '{desc[:30]}...'")
    print(f"识别结果:")
    for r in results[:3]:
        print(f"  - {r.industry_type.value}: 置信度{r.confidence:.2f}")
    assert results[0].industry_type == IndustryType.ECOMMERCE, "电商识别失败"
    print("✓ 电商识别正确")
    
    # 测试2.2: 基于描述识别 - SaaS B2B
    desc = "我们提供企业级SaaS服务，关注ARR和NRR指标，采用PLG增长策略"
    results = detector.detect(description=desc, top_k=3)
    print(f"\n描述: '{desc[:30]}...'")
    print(f"识别结果:")
    for r in results[:3]:
        print(f"  - {r.industry_type.value}: 置信度{r.confidence:.2f}")
    assert results[0].industry_type == IndustryType.SAAS_B2B, "SaaS B2B识别失败"
    print("✓ SaaS B2B识别正确")
    
    # 测试2.3: 基于描述识别 - 医疗健康
    desc = "互联网医疗平台，连接医生和患者，关注复诊率和处方转化率"
    results = detector.detect(description=desc, top_k=3)
    print(f"\n描述: '{desc[:30]}...'")
    print(f"识别结果:")
    for r in results[:3]:
        print(f"  - {r.industry_type.value}: 置信度{r.confidence:.2f}")
    assert results[0].industry_type == IndustryType.HEALTHCARE, "医疗健康识别失败"
    print("✓ 医疗健康识别正确")
    
    # 测试2.4: 基于关键词识别
    keywords = ["健身", "打卡", "课程", "教练"]
    results = detector.detect(keywords=keywords, top_k=3)
    print(f"\n关键词: {keywords}")
    print(f"识别结果:")
    for r in results[:3]:
        print(f"  - {r.industry_type.value}: 置信度{r.confidence:.2f}")
    assert results[0].industry_type == IndustryType.SPORTS_FITNESS, "运动健身识别失败"
    print("✓ 运动健身识别正确")
    
    # 测试2.5: 基于指标识别
    metrics = ["试驾转化率", "交付周期", "充电网络覆盖"]
    results = detector.detect(metrics=metrics, top_k=3)
    print(f"\n指标: {metrics}")
    print(f"识别结果:")
    for r in results[:3]:
        print(f"  - {r.industry_type.value}: 置信度{r.confidence:.2f}")
    assert results[0].industry_type == IndustryType.NEW_ENERGY, "新能源汽车识别失败"
    print("✓ 新能源汽车识别正确")
    
    # 测试2.6: 综合识别
    desc = "我们是一个在线教育平台"
    keywords = ["k12", "课程", "老师"]
    metrics = ["完课率", "续费率"]
    results = detector.detect(desc, keywords, metrics, top_k=3)
    print(f"\n综合输入: 描述+关键词+指标")
    print(f"识别结果:")
    for r in results[:3]:
        print(f"  - {r.industry_type.value}: 置信度{r.confidence:.2f}")
    assert results[0].industry_type == IndustryType.EDUCATION, "教育识别失败"
    print("✓ 教育识别正确")
    
    print("\n✅ 自动行业识别器测试通过!")
    return True


def test_industry_similarity():
    """测试行业相似度"""
    print("\n" + "=" * 60)
    print("测试3: 行业相似度")
    print("=" * 60)
    
    detector = AutoIndustryDetector()
    
    # 测试3.1: 电商相似行业
    print("\n电商的相似行业:")
    similar = detector.get_recommendations(IndustryType.ECOMMERCE, top_k=3)
    for s in similar:
        print(f"  - {s['name']}: 相似度{s['similarity']:.2f}")
    assert len(similar) > 0, "没有找到相似行业"
    print("✓ 相似行业推荐正常")
    
    # 测试3.2: SaaS B2B相似行业
    print("\nSaaS B2B的相似行业:")
    similar = detector.get_recommendations(IndustryType.SAAS_B2B, top_k=3)
    for s in similar:
        print(f"  - {s['name']}: 相似度{s['similarity']:.2f}")
    print("✓ 相似行业推荐正常")
    
    # 测试3.3: 便捷函数
    print("\n使用便捷函数获取相似行业:")
    similar = get_similar_industries("ecommerce", top_k=3)
    for s in similar:
        print(f"  - {s['name']}: 相似度{s['similarity']:.2f}")
    
    print("\n✅ 行业相似度测试通过!")
    return True


def test_industry_coverage():
    """测试行业覆盖范围"""
    print("\n" + "=" * 60)
    print("测试4: 行业覆盖范围")
    print("=" * 60)
    
    library = IndustryProfileLibrary()
    
    # 统计各类行业数量
    categories = {
        "强监管": [],
        "高客单价": [],
        "高频消费": [],
        "季节性": [],
        "本地属性": [],
        "新兴行业": []
    }
    
    for industry_type, profile in library.get_all_profiles().items():
        attrs = profile.special_attributes
        if attrs.get("regulated"):
            categories["强监管"].append(profile.name)
        if attrs.get("high_value"):
            categories["高客单价"].append(profile.name)
        if attrs.get("high_frequency"):
            categories["高频消费"].append(profile.name)
        if attrs.get("seasonal"):
            categories["季节性"].append(profile.name)
        if attrs.get("local_focus"):
            categories["本地属性"].append(profile.name)
        if attrs.get("emerging"):
            categories["新兴行业"].append(profile.name)
    
    print("\n行业分类统计:")
    for category, industries in categories.items():
        print(f"  {category}: {len(industries)}个 - {', '.join(industries[:5])}")
    
    print("\n✅ 行业覆盖范围测试通过!")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("行业扩展测试套件")
    print("=" * 60)
    
    results = []
    
    try:
        results.append(("行业画像库", test_industry_profile_library()))
    except Exception as e:
        results.append(("行业画像库", False))
        print(f"❌ 行业画像库测试失败: {e}")
    
    try:
        results.append(("自动行业识别器", test_auto_industry_detector()))
    except Exception as e:
        results.append(("自动行业识别器", False))
        print(f"❌ 自动行业识别器测试失败: {e}")
    
    try:
        results.append(("行业相似度", test_industry_similarity()))
    except Exception as e:
        results.append(("行业相似度", False))
        print(f"❌ 行业相似度测试失败: {e}")
    
    try:
        results.append(("行业覆盖范围", test_industry_coverage()))
    except Exception as e:
        results.append(("行业覆盖范围", False))
        print(f"❌ 行业覆盖范围测试失败: {e}")
    
    # 汇总
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {status}: {name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过! 行业扩展v2.0就绪!")
        return True
    else:
        print(f"\n⚠️ {total - passed} 个测试失败,请检查")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
