"""
高效配色矩阵生成演示脚本
展示品牌LOGO主色调提取和高级配色方案生成
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

OUTPUT_DIR = PROJECT_ROOT / "outputs"

from ppt import PPTService, ColorScheme

from ppt.color_matrix_generator import ColorMatrixGenerator, Color, LogoColorExtractor
import json
import yaml


def demo_color_extraction(logo_path: str = None):
    """演示LOGO主色调提取"""
    print("\n" + "="*60)
    print("演示1: 品牌LOGO主色调提取")
    print("="*60)
    
    if logo_path and os.path.exists(logo_path):
        extractor = LogoColorExtractor(max_colors=3)
        colors = extractor.extract_from_image(logo_path)
        
        print(f"\n从 {logo_path} 提取到 {len(colors)} 种主色调:")
        for i, color in enumerate(colors, 1):
            print(f"  {i}. {color.hex_code}")
            print(f"     RGB: {color.rgb}")
            print(f"     HSL: H={color.hsl[0]:.1f}° S={color.hsl[1]:.1f}% L={color.hsl[2]:.1f}%")
            print()
    else:
        # 使用默认颜色演示
        primary_color = Color.from_hex("#2C3E50")
        print(f"\n使用默认主色调: {primary_color.hex_code}")
        print(f"RGB: {primary_color.rgb}")
        print(f"HSL: H={primary_color.hsl[0]:.1f}° S={primary_color.hsl[1]:.1f}% L={primary_color.hsl[2]:.1f}%")


def demo_color_matrix(primary_hex: str = "#2C3E50"):
    """演示配色矩阵生成"""
    print("\n" + "="*60)
    print("演示2: 高效配色矩阵生成")
    print("="*60)
    
    primary_color = Color.from_hex(primary_hex)
    generator = ColorMatrixGenerator(primary_color)
    
    matrix = generator.generate_color_matrix()
    
    for category, schemes in matrix.items():
        print(f"\n【{category}】")
        for scheme in schemes:
            print(f"\n  {scheme.name}")
            print(f"  描述: {scheme.description}")
            print(f"  用途: {scheme.usage}")
            print(f"  颜色:")
            for i, color in enumerate(scheme.colors, 1):
                print(f"    {i}. {color.hex_code} - RGB{color.rgb}")
    
    return matrix


def demo_60_30_10_rule():
    """演示60-30-10黄金配比"""
    print("\n" + "="*60)
    print("演示3: 60-30-10黄金配比")
    print("="*60)
    
    primary_color = Color.from_hex("#2C3E50")
    generator = ColorMatrixGenerator(primary_color)
    
    scheme = generator.generate_60_30_10_scheme()
    
    print(f"\n{scheme.name}:")
    print(f"  {scheme.description}")
    print(f"\n  {scheme.usage}")
    print(f"\n  颜色配比:")
    for i, color in enumerate(scheme.colors, 1):
        percentage = 60 if i == 1 else 30 if i == 2 else 5 if i < 5 else 0
        if percentage > 0:
            print(f"    {percentage}% {color.hex_code} - {color.hsl}")


def demo_color_harmonies():
    """演示色彩和谐关系"""
    print("\n" + "="*60)
    print("演示4: 色彩和谐关系")
    print("="*60)
    
    primary_color = Color.from_hex("#3498DB")  # 蓝色
    
    print(f"\n基础色: {primary_color.hex_code} (蓝色)")
    print(f"  HSL: H={primary_color.hsl[0]:.1f}° S={primary_color.hsl[1]:.1f}% L={primary_color.hsl[2]:.1f}%")
    
    harmonies = {
        "互补色": primary_color.get_complementary(),
        "类比色 (+30°)": primary_color.get_analogous(1),
        "类比色 (-30°)": primary_color.get_analogous(-1),
        "三角色 (120°)": primary_color.get_triadic(1),
        "四角色 (90°)": primary_color.get_tetradic(1)
    }
    
    print("\n色彩和谐关系:")
    for name, color in harmonies.items():
        print(f"\n  {name}:")
        print(f"    {color.hex_code}")
        print(f"    HSL: H={color.hsl[0]:.1f}° S={color.hsl[1]:.1f}% L={color.hsl[2]:.1f}%")


def demo_brand_color_integration():
    """演示品牌配色集成到PPT"""
    print("\n" + "="*60)
    print("演示5: 品牌配色集成到PPT")
    print("="*60)
    
    # 创建PPT服务（不提供LOGO，使用默认配色）
    print("\n方式1: 使用预设配色方案")
    service = PPTService(theme="business", enable_learning=False)
    print(f"  主题: business")
    print(f"  配色: {service.beautifier.color_palette.name}")
    print(f"  主色: {service.beautifier.color_palette.primary}")
    print(f"  辅助色: {service.beautifier.color_palette.secondary}")
    print(f"  强调色: {service.beautifier.color_palette.accent}")
    
    # 演示生成配色矩阵
    print("\n方式2: 生成配色矩阵")
    primary_color = Color.from_hex("#2C3E50")
    generator = ColorMatrixGenerator(primary_color)
    matrix = generator.generate_all_schemes()
    
    print(f"  基于主色 {primary_color.hex_code} 生成了 {len(matrix)} 种配色方案:")
    for scheme in matrix[:3]:  # 只显示前3种
        print(f"    - {scheme.name}")
    
    # 导出配色方案
    print("\n方式3: 导出配色方案到YAML")
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "color_schemes_export.yaml"
    generator.export_schemes_yaml(matrix, str(output_path))
    print(f"  已导出到: {output_path}")



def demo_contrast_color():
    """演示对比色计算"""
    print("\n" + "="*60)
    print("演示6: 对比色计算（WCAG可访问性）")
    print("="*60)
    
    test_colors = [
        "#2C3E50",  # 深蓝
        "#FFFFFF",  # 白色
        "#FF0000",  # 红色
        "#3498DB",  # 亮蓝
    ]
    
    print("\n测试颜色的最佳对比色:")
    for hex_color in test_colors:
        color = Color.from_hex(hex_color)
        contrast_color = color.get_contrast_color()
        
        print(f"\n  背景色: {color.hex_code}")
        print(f"    亮度: {color.hsl[2]:.1f}%")
        print(f"    最佳文字色: {contrast_color.hex_code} ({'白色' if contrast_color.hex_code == '#FFFFFF' else '黑色'})")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("高效配色矩阵生成器 - 完整演示")
    print("="*60)
    
    # 演示1: LOGO主色调提取（如果提供了LOGO路径）
    # demo_color_extraction("path/to/logo.png")
    demo_color_extraction()
    
    # 演示2: 配色矩阵生成
    matrix = demo_color_matrix("#3498DB")
    
    # 演示3: 60-30-10黄金配比
    demo_60_30_10_rule()
    
    # 演示4: 色彩和谐关系
    demo_color_harmonies()
    
    # 演示5: 品牌配色集成到PPT
    demo_brand_color_integration()
    
    # 演示6: 对比色计算
    demo_contrast_color()
    
    print("\n" + "="*60)
    print("演示完成！")
    print("="*60)
    print("\n核心功能:")
    print("  ✓ 品牌LOGO主色调提取")
    print("  ✓ 高效配色矩阵生成（9种配色方案）")
    print("  ✓ 60-30-10黄金配比")
    print("  ✓ 色彩和谐关系计算")
    print("  ✓ 集成到PPT美化引擎")
    print("  ✓ WCAG对比度标准支持")
    print("\n配色方案类型:")
    print("  基础配色: 单色、互补、类比")
    print("  多色配色: 三角色、四角色、60-30-10")
    print("  场景配色: 商务、科技、教育")


if __name__ == "__main__":
    main()
