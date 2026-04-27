"""
PPT风格智能推荐系统演示

展示十大平台设计风格分析的成果：
1. 场景识别与风格推荐
2. 配色方案智能推荐
3. 设计规则应用
4. Beautiful.ai风格自动排版
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)


from src.ppt.ppt_style_recommender import (
    PPTStyleRecommender,
    SceneType,
    format_style_recommendation
)
from src.ppt.ppt_design_rules import (
    SmartDesignEngine,
    Element,
    HierarchyLevel,
    Alignment
)


def demo_scene_style_recommendation():
    """
    演示1: 场景识别与风格推荐
    """
    print("=" * 80)
    print("演示1: 场景识别与风格推荐")
    print("=" * 80)

    recommender = PPTStyleRecommender()

    # 测试不同场景
    test_scenes = [
        "年度工作总结报告",
        "项目路演融资",
        "员工培训课程",
        "创意设计提案",
        "技术产品发布",
        "学术论文答辩",
        "年度营销策划方案"
    ]

    for scene in test_scenes:
        print(f"\n{'─' * 80}")
        print(f"场景: {scene}")
        print(f"{'─' * 80}")

        recommendation = recommender.recommend_by_scene(scene)
        print(format_style_recommendation(recommendation))

    print("\n" + "=" * 80 + "\n")


def demo_content_style_recommendation():
    """
    演示2: 根据内容和受众推荐风格
    """
    print("=" * 80)
    print("演示2: 根据内容和受众推荐风格")
    print("=" * 80)

    recommender = PPTStyleRecommender()

    # 测试不同内容和受众组合
    test_cases = [
        {
            "content": "本季度销售额同比增长25%，用户留存率达到78%，主要增长来自线上渠道。通过数据图表展示销售趋势，对比去年同期数据，分析增长驱动因素。",
            "audience": "公司高管"
        },
        {
            "content": "课程内容包括产品功能介绍、使用场景演示、案例分析和实战练习。通过图文结合的方式，让学员快速掌握产品使用技巧。包含互动环节和课后练习。",
            "audience": "新员工"
        },
        {
            "content": "项目目标、时间节点、关键里程碑、资源需求、风险评估。需要展示甘特图、资源分配表、风险矩阵等专业图表。",
            "audience": "投资人"
        },
        {
            "content": "研究背景、文献综述、研究方法、数据分析、研究结论、未来展望。需要详细展示实验数据、统计分析结果和结论验证过程。",
            "audience": "学术专家"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'─' * 80}")
        print(f"案例 {i}")
        print(f"{'─' * 80}")
        print(f"内容摘要: {test_case['content'][:50]}...")
        print(f"受众: {test_case['audience']}")
        print(f"{'─' * 80}")

        recommendation = recommender.recommend_by_content(
            test_case["content"],
            test_case["audience"]
        )
        print(format_style_recommendation(recommendation))

    print("\n" + "=" * 80 + "\n")


def demo_color_mood_recommendation():
    """
    演示3: 根据情绪/氛围推荐配色
    """
    print("=" * 80)
    print("演示3: 根据情绪/氛围推荐配色")
    print("=" * 80)

    recommender = PPTStyleRecommender()

    # 测试不同情绪
    test_moods = [
        "稳重专业",
        "活泼创意",
        "温馨舒适",
        "现代科技",
        "高端优雅"
    ]

    for mood in test_moods:
        print(f"\n{'─' * 80}")
        print(f"情绪/氛围: {mood}")
        print(f"{'─' * 80}")

        palette = recommender.recommend_color_by_mood(mood)
        harmony_score = recommender.get_color_harmony_score(palette)

        print(f"主色(60%):  {palette.primary}")
        print(f"辅色(30%):  {palette.secondary}")
        print(f"强调色(10%): {palette.accent}")
        print(f"背景色:     {palette.background}")
        print(f"文字色:     {palette.text}")
        print(f"配色和谐度:  {harmony_score:.0f}/100")

    print("\n" + "=" * 80 + "\n")


def demo_design_rules_engine():
    """
    演示4: Beautiful.ai风格智能设计规则引擎
    """
    print("=" * 80)
    print("演示4: Beautiful.ai风格智能设计规则引擎")
    print("=" * 80)

    engine = SmartDesignEngine()

    # 打印设计规则
    print("\n【设计规则列表】")
    print(f"{'─' * 80}")
    rules = engine.get_design_rules()
    for i, rule in enumerate(rules, 1):
        print(f"{i}. {rule.name} (优先级: {rule.priority})")
        print(f"   {rule.description}")

    # 演示自动布局
    print(f"\n{'─' * 80}")
    print("【自动布局演示】")
    print(f"{'─' * 80}")

    # 创建示例元素
    elements = [
        Element(
            id="1",
            type="text",
            x=100,
            y=50,
            width=800,
            height=60,
            content="标题",
            hierarchy=HierarchyLevel.TITLE
        ),
        Element(
            id="2",
            type="text",
            x=100,
            y=150,
            width=350,
            height=200,
            content="左侧内容",
            hierarchy=HierarchyLevel.BODY
        ),
        Element(
            id="3",
            type="text",
            x=550,
            y=150,
            width=350,
            height=200,
            content="右侧内容",
            hierarchy=HierarchyLevel.BODY
        ),
        Element(
            id="4",
            type="text",
            x=100,
            y=400,
            width=800,
            height=40,
            content="说明文字",
            hierarchy=HierarchyLevel.CAPTION
        )
    ]

    # 自动布局
    print("\n布局前:")
    print(f"元素数量: {len(elements)}")
    for element in elements:
        print(f"  元素{element.id}: ({element.x:.0f}, {element.y:.0f}) - {element.content}")

    layout = engine.auto_layout(elements, page_width=1000, page_height=750)

    print("\n布局后:")
    print(f"元素数量: {len(layout.elements)}")
    print(f"间距: {layout.spacing:.2f}")
    print(f"对齐方式: {layout.alignment.value}")
    for element in layout.elements:
        print(f"  元素{element.id}: ({element.x:.0f}, {element.y:.0f}) - {element.content}")
        if hasattr(element, 'font_size'):
            print(f"    字号: {element.font_size:.0f}pt")

    # 演示响应式排版
    print(f"\n{'─' * 80}")
    print("【响应式排版演示】")
    print(f"{'─' * 80}")

    # 添加内容
    new_element = Element(
        id="5",
        type="text",
        x=100,
        y=500,
        width=800,
        height=60,
        content="新增内容",
        hierarchy=HierarchyLevel.BODY
    )
    elements.append(new_element)

    responsive_layout = engine.responsive_layout(elements, content_change="add")

    print("\n添加内容后:")
    print(f"元素数量: {len(responsive_layout.elements)}")
    print(f"间距: {responsive_layout.spacing:.2f}")

    print("\n" + "=" * 80 + "\n")


def demo_integrated_ppt_service():
    """
    演示5: 集成PPT服务应用
    """
    print("=" * 80)
    print("演示5: 集成PPT服务应用")
    print("=" * 80)

    from src.ppt.ppt_service import PPTService

    # 创建PPT服务
    service = PPTService(theme="business", enable_charts=False)

    # 1. 场景风格推荐
    print("\n【1. 场景风格推荐】")
    print(f"{'─' * 80}")
    style_rec = service.recommend_style_by_scene("年度工作总结报告")
    print(f"场景类型: {style_rec['scene_type']}")
    print(f"参考平台: {style_rec['reference_platform']}")
    print(f"配色方案: {style_rec['color_scheme']}")
    print(f"排版布局: {style_rec['layout']}")
    print(f"推荐置信度: {style_rec['confidence']*100:.0f}%")

    # 2. 内容风格推荐
    print(f"\n【2. 内容风格推荐】")
    print(f"{'─' * 80}")
    content = "本季度销售额增长25%，用户留存率提升15%。通过数据图表展示趋势。"
    audience = "公司高管"
    style_rec = service.recommend_style_by_content(content, audience)
    print(f"场景类型: {style_rec['scene_type']}")
    print(f"参考平台: {style_rec['reference_platform']}")
    print(f"配色方案: {style_rec['color_scheme']}")
    print(f"排版布局: {style_rec['layout']}")

    # 3. 情绪配色推荐
    print(f"\n【3. 情绪配色推荐】")
    print(f"{'─' * 80}")
    color_rec = service.recommend_color_by_mood("稳重专业")
    print(f"主色: {color_rec['primary']}")
    print(f"辅色: {color_rec['secondary']}")
    print(f"强调色: {color_rec['accent']}")

    # 4. 设计原则
    print(f"\n【4. 设计原则】")
    print(f"{'─' * 80}")
    principles = service.get_design_principles()
    for i, (key, value) in enumerate(principles.items(), 1):
        print(f"{i}. {value}")

    print("\n" + "=" * 80 + "\n")


def demo_cross_platform_comparison():
    """
    演示6: 跨平台风格对比
    """
    print("=" * 80)
    print("演示6: 跨平台风格对比")
    print("=" * 80)

    recommender = PPTStyleRecommender()

    # 测试同一场景在不同平台的表现
    scene = "商务汇报"

    print(f"\n场景: {scene}")
    print(f"{'─' * 80}")

    # 获取推荐
    recommendation = recommender.recommend_by_scene(scene)

    # 分析参考平台的特点
    platform_features = {
        "OfficePLUS": {
            "定位": "微软官方平台",
            "风格": "商务专业",
            "配色": "深蓝、灰色系",
            "特点": "严谨、稳重、易用"
        },
        "稻壳儿": {
            "定位": "WPS生态",
            "风格": "本土化优化",
            "配色": "灵活多变",
            "特点": "场景化、垂直分类"
        },
        "优品PPT": {
            "定位": "免费优质平台",
            "风格": "简约扁平",
            "配色": "舒适不刺眼",
            "特点": "留白充足、清晰易读"
        },
        "Canva": {
            "定位": "全球化设计平台",
            "风格": "模板驱动",
            "配色": "丰富多样",
            "特点": "36种风格分类"
        },
        "Beautiful.ai": {
            "定位": "AI智能设计",
            "风格": "自动排版",
            "配色": "智能适配",
            "特点": "设计规则引擎"
        },
        "Gamma": {
            "定位": "AI一键生成",
            "风格": "智能布局",
            "配色": "自动生成",
            "特点": "分钟级完成"
        }
    }

    print(f"\n推荐参考平台: {recommendation.platform}")
    print(f"{'─' * 80}")

    platform = platform_features.get(recommendation.platform)
    if platform:
        print(f"定位: {platform['定位']}")
        print(f"风格: {platform['风格']}")
        print(f"配色特点: {platform['配色']}")
        print(f"核心优势: {platform['特点']}")

    print(f"\n{'─' * 80}")
    print("其他平台对比:")
    print(f"{'─' * 80}")

    for platform_name, features in platform_features.items():
        if platform_name != recommendation.platform:
            print(f"\n{platform_name}:")
            print(f"  {features['特点']}")

    print("\n" + "=" * 80 + "\n")


def main():
    """
    主函数
    """
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "PPT风格智能推荐系统演示" + " " * 31 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    print("基于十大平台设计风格分析的智能推荐系统")
    print("整合OfficePLUS、稻壳儿、优品PPT、Canva、Gamma、Beautiful.ai等平台的设计理念")
    print("\n")

    demos = [
        ("场景识别与风格推荐", demo_scene_style_recommendation),
        ("根据内容和受众推荐风格", demo_content_style_recommendation),
        ("根据情绪/氛围推荐配色", demo_color_mood_recommendation),
        ("Beautiful.ai风格智能设计规则引擎", demo_design_rules_engine),
        ("集成PPT服务应用", demo_integrated_ppt_service),
        ("跨平台风格对比", demo_cross_platform_comparison)
    ]

    for i, (name, func) in enumerate(demos, 1):
        print(f"演示 {i}/{len(demos)}: {name}")
        print()

        try:
            func()
        except Exception as e:
            print(f"❌ 演示失败: {e}")
            import traceback
            traceback.print_exc()

    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 30 + "演示完成！" + " " * 35 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")


if __name__ == "__main__":
    main()
