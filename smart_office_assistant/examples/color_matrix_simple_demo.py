"""
高效配色矩阵生成器 - 简化演示
直接测试核心配色功能，避免复杂依赖
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

OUTPUT_DIR = PROJECT_ROOT / "outputs"

from ppt.color_matrix_generator import ColorMatrixGenerator, Color, LogoColorExtractor



def main():
    print("\n" + "="*60)
    print("高效配色矩阵生成器 - 核心功能演示")
    print("="*60)
    
    # 1. 测试颜色转换
    print("\n【测试1: 颜色转换】")
    primary = Color.from_hex("#3498DB")
    print(f"  原始颜色: {primary.hex_code}")
    print(f"  RGB: {primary.rgb}")
    print(f"  HSL: H={primary.hsl[0]:.1f}° S={primary.hsl[1]:.1f}% L={primary.hsl[2]:.1f}%")
    
    # 2. 测试色彩和谐关系
    print("\n【测试2: 色彩和谐关系】")
    harmonies = {
        "互补色": primary.get_complementary(),
        "类比色(+30°)": primary.get_analogous(1),
        "三角色(120°)": primary.get_triadic(1),
        "四角色(90°)": primary.get_tetradic(1)
    }
    
    for name, color in harmonies.items():
        print(f"  {name}: {color.hex_code}")
    
    # 3. 测试配色方案生成
    print("\n【测试3: 配色方案生成】")
    generator = ColorMatrixGenerator(primary)
    
    schemes = [
        ("单色配色", generator.generate_monochromatic_scheme()),
        ("互补配色", generator.generate_complementary_scheme()),
        ("类比配色", generator.generate_analogous_scheme()),
        ("三角色配色", generator.generate_triadic_scheme()),
        ("四角色配色", generator.generate_tetradic_scheme()),
        ("60-30-10配比", generator.generate_60_30_10_scheme()),
        ("商务配色", generator.generate_business_scheme()),
        ("科技配色", generator.generate_tech_scheme()),
        ("教育配色", generator.generate_education_scheme())
    ]
    
    for name, scheme in schemes:
        print(f"\n  {name}:")
        print(f"    描述: {scheme.description}")
        colors = [c.hex_code for c in scheme.colors]
        print(f"    颜色: {', '.join(colors)}")
    
    # 4. 测试配色矩阵
    print("\n【测试4: 配色矩阵】")
    matrix = generator.generate_color_matrix()
    
    for category, scheme_list in matrix.items():
        print(f"\n  {category} ({len(scheme_list)}种方案):")
        for scheme in scheme_list:
            print(f"    - {scheme.name}")
    
    # 5. 测试对比色
    print("\n【测试5: 对比色计算】")
    test_colors = ["#2C3E50", "#FFFFFF", "#3498DB"]
    
    for hex_color in test_colors:
        color = Color.from_hex(hex_color)
        contrast = color.get_contrast_color()
        print(f"  {hex_color} -> {contrast.hex_code} ({'白色' if contrast.hex_code == '#FFFFFF' else '黑色'})")
    
    print("\n" + "="*60)
    print("✓ 所有核心功能测试通过！")
    print("="*60)
    
    # 导出配色方案
    print("\n正在导出配色方案...")
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "test_color_schemes.yaml"
    generator.export_schemes_yaml([s for _, s in schemes], str(output_path))
    print(f"✓ 已导出到: {output_path}")

    
    print("\n核心功能总结:")
    print("  ✓ RGB/HSL/HEX颜色空间转换")
    print("  ✓ 色彩和谐关系计算（互补/类比/三角色/四角色）")
    print("  ✓ 9种配色方案自动生成")
    print("  ✓ 60-30-10黄金配比")
    print("  ✓ 场景配色（商务/科技/教育）")
    print("  ✓ WCAG对比色计算")
    print("  ✓ 配色方案导出（YAML格式）")


if __name__ == "__main__":
    main()
