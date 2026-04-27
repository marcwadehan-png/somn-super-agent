"""
__all__ = [
    'export_schemes_yaml',
    'extract_dominant_color',
    'extract_from_image',
    'from_hex',
    'from_rgb',
    'generate_60_30_10_scheme',
    'generate_all_schemes',
    'generate_analogous_scheme',
    'generate_business_scheme',
    'generate_color_matrix',
    'generate_complementary_scheme',
    'generate_education_scheme',
    'generate_monochromatic_scheme',
    'generate_tech_scheme',
    'generate_tetradic_scheme',
    'generate_triadic_scheme',
    'get_analogous',
    'get_complementary',
    'get_contrast_color',
    'get_hue_shifted',
    'get_lightness_adjusted',
    'get_monochromatic',
    'get_saturation_adjusted',
    'get_tetradic',
    'get_triadic',
    'hue_to_rgb',
    'to_dict',
]

高效配色矩阵generate器 (Color Matrix Generator)
支持品牌LOGO主色调提取和高级配色方案generate
"""

import colorsys
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from PIL import Image
import numpy as np
from collections import Counter

@dataclass
class Color:
    """颜色类,支持多种色彩空间"""
    hex_code: str
    rgb: Tuple[int, int, int]
    hsl: Tuple[float, float, float]
    
    @classmethod
    def from_hex(cls, hex_code: str) -> 'Color':
        """从HEX代码创建颜色"""
        hex_code = hex_code.lstrip('#')
        rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
        hsl = Color._rgb_to_hsl(rgb)
        return cls(hex_code.upper(), rgb, hsl)
    
    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> 'Color':
        """从RGB创建颜色"""
        rgb = (r, g, b)
        hsl = Color._rgb_to_hsl(rgb)
        hex_code = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        return cls(hex_code.upper(), rgb, hsl)
    
    @staticmethod
    def _rgb_to_hsl(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """RGB转HSL"""
        r, g, b = [x / 255.0 for x in rgb]
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        
        h = s = 0.0
        l = (max_val + min_val) / 2.0
        
        if max_val != min_val:
            d = max_val - min_val
            s = d / (2.0 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)
            
            if max_val == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_val == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            h /= 6.0
        
        return (h * 360, s * 100, l * 100)
    
    @staticmethod
    def _hsl_to_rgb(hsl: Tuple[float, float, float]) -> Tuple[int, int, int]:
        """HSL转RGB"""
        h, s, l = [hsl[0] / 360.0, hsl[1] / 100.0, hsl[2] / 100.0]
        
        if s == 0:
            r = g = b = l
        else:
            def hue_to_rgb(p: float, q: float, t: float) -> float:
                if t < 0:
                    t += 1
                if t > 1:
                    t -= 1
                if t < 1/6:
                    return p + (q - p) * 6 * t
                if t < 1/2:
                    return q
                if t < 2/3:
                    return p + (q - p) * (2/3 - t) * 6
                return p
            
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h + 1/3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1/3)
        
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def get_hue_shifted(self, shift_degrees: float) -> 'Color':
        """色相偏移"""
        h, s, l = self.hsl
        new_h = (h + shift_degrees) % 360
        new_rgb = self._hsl_to_rgb((new_h, s, l))
        return Color.from_rgb(*new_rgb)
    
    def get_saturation_adjusted(self, adjustment: float) -> 'Color':
        """饱和度调整(-100到100)"""
        h, s, l = self.hsl
        new_s = max(0, min(100, s + adjustment))
        new_rgb = self._hsl_to_rgb((h, new_s, l))
        return Color.from_rgb(*new_rgb)
    
    def get_lightness_adjusted(self, adjustment: float) -> 'Color':
        """亮度调整(-100到100)"""
        h, s, l = self.hsl
        new_l = max(0, min(100, l + adjustment))
        new_rgb = self._hsl_to_rgb((h, s, new_l))
        return Color.from_rgb(*new_rgb)
    
    def get_complementary(self) -> 'Color':
        """互补色"""
        return self.get_hue_shifted(180)
    
    def get_analogous(self, direction: int = 1) -> 'Color':
        """类比色(30度偏移)"""
        return self.get_hue_shifted(30 * direction)
    
    def get_triadic(self, index: int = 0) -> 'Color':
        """三角色(120度偏移)"""
        return self.get_hue_shifted(120 * index)
    
    def get_tetradic(self, index: int = 0) -> 'Color':
        """四角色(90度偏移)"""
        return self.get_hue_shifted(90 * index)
    
    def get_monochromatic(self, lightness_change: float) -> 'Color':
        """单色(亮度变化)"""
        return self.get_lightness_adjusted(lightness_change)
    
    def get_contrast_color(self, threshold: float = 0.5) -> 'Color':
        """对比色(根据亮度决定黑或白)"""
        luminance = (0.299 * self.rgb[0] + 0.587 * self.rgb[1] + 0.114 * self.rgb[2]) / 255
        if luminance > threshold:
            return Color.from_rgb(0, 0, 0)  # 黑色
        else:
            return Color.from_rgb(255, 255, 255)  # 白色
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'hex': self.hex_code,
            'rgb': self.rgb,
            'hsl': self.hsl
        }

@dataclass
class ColorScheme:
    """配色方案类"""
    name: str
    colors: List[Color]
    description: str
    usage: str
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'name': self.name,
            'description': self.description,
            'usage': self.usage,
            'colors': [c.to_dict() for c in self.colors]
        }

class LogoColorExtractor:
    """品牌LOGO主色调提取器"""
    
    def __init__(self, max_colors: int = 5):
        self.max_colors = max_colors
    
    def extract_from_image(self, image_path: str) -> List[Color]:
        """
        从图片中提取主色调
        
        Args:
            image_path: 图片路径
            
        Returns:
            主色调列表(按出现频率排序)
        """
        try:
            img = Image.open(image_path)
            # 转换为RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 缩小图片以提高性能
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            
            # 提取像素
            pixels = list(img.getdata())
            
            # 统计颜色频率
            color_counter = Counter(pixels)
            
            # 忽略接近白色或黑色的像素
            filtered_colors = []
            for (r, g, b), count in color_counter.items():
                # 跳过过于接近纯白或纯黑的颜色
                if (r, g, b) == (255, 255, 255) or (r, g, b) == (0, 0, 0):
                    continue
                # 跳过低饱和度颜色(接近灰度)
                max_val = max(r, g, b)
                min_val = min(r, g, b)
                if max_val - min_val < 30:
                    continue
                filtered_colors.append(((r, g, b), count))
            
            # 按频率排序
            filtered_colors.sort(key=lambda x: x[1], reverse=True)
            
            # 转换为Color对象
            colors = []
            for (rgb, _) in filtered_colors[:self.max_colors]:
                colors.append(Color.from_rgb(*rgb))
            
            return colors if colors else [Color.from_rgb(0, 102, 204)]  # 默认蓝色
            
        except Exception as e:
            print(f"提取LOGO颜色失败: {e}")
            return [Color.from_rgb(0, 102, 204)]  # 默认蓝色
    
    def extract_dominant_color(self, image_path: str) -> Color:
        """提取最主要的颜色"""
        colors = self.extract_from_image(image_path)
        return colors[0] if colors else Color.from_rgb(0, 102, 204)

class ColorMatrixGenerator:
    """高效配色矩阵generate器"""
    
    def __init__(self, primary_color: Optional[Color] = None):
        """
        init配色矩阵generate器
        
        Args:
            primary_color: 主色调,如果为None则使用默认蓝色
        """
        self.primary_color = primary_color or Color.from_rgb(0, 102, 204)
    
    def generate_monochromatic_scheme(self) -> ColorScheme:
        """generate单色配色方案(同色系)"""
        colors = []
        
        # 主色
        colors.append(self.primary_color)
        
        # 亮色和暗色变体
        colors.append(self.primary_color.get_lightness_adjusted(30))
        colors.append(self.primary_color.get_lightness_adjusted(-20))
        colors.append(self.primary_color.get_lightness_adjusted(45))
        colors.append(self.primary_color.get_lightness_adjusted(-40))
        
        return ColorScheme(
            name="单色配色(同色系)",
            colors=colors,
            description="使用同一色相,通过亮度变化创造层次感",
            usage="适合专业,简约,强调专业性的场景"
        )
    
    def generate_complementary_scheme(self) -> ColorScheme:
        """generate互补配色方案"""
        colors = []
        
        # 主色
        colors.append(self.primary_color)
        
        # 互补色
        complementary = self.primary_color.get_complementary()
        colors.append(complementary)
        
        # 主色的深浅变体
        colors.append(self.primary_color.get_lightness_adjusted(25))
        colors.append(self.primary_color.get_lightness_adjusted(-15))
        
        # 互补色的深浅变体
        colors.append(complementary.get_lightness_adjusted(-20))
        
        return ColorScheme(
            name="互补配色",
            colors=colors,
            description="使用色轮上相对的两种颜色,创造强烈对比",
            usage="适合需要强调对比,突出重点的场景"
        )
    
    def generate_analogous_scheme(self) -> ColorScheme:
        """generate类比配色方案(相邻色系)"""
        colors = []
        
        # 主色
        colors.append(self.primary_color)
        
        # 相邻色
        colors.append(self.primary_color.get_analogous(-1))
        colors.append(self.primary_color.get_analogous(1))
        
        # 主色的深浅变体
        colors.append(self.primary_color.get_lightness_adjusted(30))
        colors.append(self.primary_color.get_lightness_adjusted(-25))
        
        return ColorScheme(
            name="类比配色(相邻色系)",
            colors=colors,
            description="使用色轮上相邻的颜色,和谐unified",
            usage="适合自然,柔和,连贯的视觉体验"
        )
    
    def generate_triadic_scheme(self) -> ColorScheme:
        """generate三角色配方案"""
        colors = []
        
        # 主色和三角色
        colors.append(self.primary_color)
        colors.append(self.primary_color.get_triadic(1))
        colors.append(self.primary_color.get_triadic(2))
        
        # 主色的深浅变体
        colors.append(self.primary_color.get_lightness_adjusted(30))
        colors.append(self.primary_color.get_triadic(1).get_lightness_adjusted(-25))
        
        return ColorScheme(
            name="三角色配色",
            colors=colors,
            description="使用色轮上等距的三种颜色,丰富活泼",
            usage="适合创意,活力,多样化的设计"
        )
    
    def generate_tetradic_scheme(self) -> ColorScheme:
        """generate四角色配方案"""
        colors = []
        
        # 主色和四角色
        colors.append(self.primary_color)
        colors.append(self.primary_color.get_tetradic(1))
        colors.append(self.primary_color.get_tetradic(2))
        colors.append(self.primary_color.get_tetradic(3))
        
        # 主色的浅色变体
        colors.append(self.primary_color.get_lightness_adjusted(40))
        
        return ColorScheme(
            name="四角色配色",
            colors=colors,
            description="使用色轮上等距的四种颜色,丰富多彩",
            usage="适合需要多种颜色区分不同元素的复杂场景"
        )
    
    def generate_60_30_10_scheme(self) -> ColorScheme:
        """generate60-30-10黄金配比方案"""
        # 60% - 主色(背景/大面积)
        # 30% - 辅助色(次要元素)
        # 10% - 强调色(重点/按钮)
        
        # 主色
        dominant = self.primary_color
        
        # 辅助色(类比色或互补色的浅色)
        secondary = self.primary_color.get_analogous(1).get_lightness_adjusted(20)
        
        # 强调色(互补色)
        accent = self.primary_color.get_complementary()
        
        colors = [
            dominant,
            dominant.get_lightness_adjusted(15),
            dominant.get_lightness_adjusted(-10),
            secondary,
            accent
        ]
        
        return ColorScheme(
            name="60-30-10黄金配比",
            colors=colors,
            description="经典的60%主色,30%辅助色,10%强调色配比",
            usage="适用于PPT,网页,品牌设计等场景"
        )
    
    def generate_business_scheme(self) -> ColorScheme:
        """generate商务配色方案(专业稳重)"""
        h, s, l = self.primary_color.hsl
        
        # 保持专业感,降低饱和度,提高亮度
        professional_primary = Color.from_hsl(h, min(s * 0.8, 100), min(l + 10, 100))
        
        colors = []
        colors.append(professional_primary)
        colors.append(professional_primary.get_lightness_adjusted(30))
        colors.append(professional_primary.get_lightness_adjusted(-15))
        colors.append(Color.from_rgb(80, 80, 80))  # 中性灰
        colors.append(Color.from_rgb(240, 240, 240))  # 浅灰背景
        
        return ColorScheme(
            name="商务配色",
            colors=colors,
            description="专业稳重的商务配色,降低饱和度提升专业感",
            usage="适用于商务汇报,企业展示,专业文档"
        )
    
    def generate_tech_scheme(self) -> ColorScheme:
        """generate科技配色方案(现代创新)"""
        colors = []
        
        # 主色
        colors.append(self.primary_color)
        
        # 添加科技感的亮色(通常偏蓝或紫)
        tech_accent = Color.from_rgb(0, 140, 255)  # 科技蓝
        colors.append(tech_accent)
        
        # 主色的深浅变体
        colors.append(self.primary_color.get_lightness_adjusted(35))
        colors.append(self.primary_color.get_lightness_adjusted(-20))
        
        # 深色背景
        colors.append(Color.from_rgb(30, 30, 40))
        
        return ColorScheme(
            name="科技配色",
            colors=colors,
            description="现代科技感的配色,强调创新和未来感",
            usage="适用于科技产品展示,技术汇报,创新方案"
        )
    
    def generate_education_scheme(self) -> ColorScheme:
        """generate教育配色方案(温暖友好)"""
        h, s, l = self.primary_color.hsl
        
        # 提高饱和度和亮度,营造温暖感
        warm_primary = Color.from_hsl(h, min(s * 1.1, 100), min(l + 15, 100))
        
        colors = []
        colors.append(warm_primary)
        colors.append(warm_primary.get_lightness_adjusted(25))
        colors.append(warm_primary.get_lightness_adjusted(-10))
        colors.append(Color.from_rgb(255, 180, 100))  # 温暖的橙色
        colors.append(Color.from_rgb(250, 250, 245))  # 温暖的米白背景
        
        return ColorScheme(
            name="教育配色",
            colors=colors,
            description="温暖友好的教育配色,适合学习场景",
            usage="适用于教育培训,知识分享,学习材料"
        )
    
    def generate_all_schemes(self) -> List[ColorScheme]:
        """generate所有配色方案"""
        return [
            self.generate_monochromatic_scheme(),
            self.generate_complementary_scheme(),
            self.generate_analogous_scheme(),
            self.generate_triadic_scheme(),
            self.generate_tetradic_scheme(),
            self.generate_60_30_10_scheme(),
            self.generate_business_scheme(),
            self.generate_tech_scheme(),
            self.generate_education_scheme()
        ]
    
    def generate_color_matrix(self) -> Dict[str, List[ColorScheme]]:
        """generate完整配色矩阵"""
        schemes = self.generate_all_schemes()
        
        # 按类型分组
        matrix = {
            '基础配色': [
                self.generate_monochromatic_scheme(),
                self.generate_complementary_scheme(),
                self.generate_analogous_scheme()
            ],
            '多色配色': [
                self.generate_triadic_scheme(),
                self.generate_tetradic_scheme(),
                self.generate_60_30_10_scheme()
            ],
            '场景配色': [
                self.generate_business_scheme(),
                self.generate_tech_scheme(),
                self.generate_education_scheme()
            ]
        }
        
        return matrix
    
    def export_schemes_yaml(self, schemes: List[ColorScheme], output_path: str):
        """导出配色方案为YAML"""
        import yaml
        
        data = {
            'primary_color': self.primary_color.to_dict(),
            'schemes': [scheme.to_dict() for scheme in schemes]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

# 扩展Color类,添加from_hsl方法
@staticmethod
def _color_from_hsl(h: float, s: float, l: float) -> Color:
    """从HSL创建颜色"""
    rgb = Color._hsl_to_rgb((h, s, l))
    return Color.from_rgb(*rgb)

Color.from_hsl = _color_from_hsl

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
