"""
__all__ = [
    'add_design_rule',
    'auto_layout',
    'get_design_rules',
    'remove_design_rule',
    'responsive_layout',
]

PPT智能设计规则引擎

智能设计规则和自动排版原理
将专业设计准则嵌入到软件中,实现实时,自动调整幻灯片格式和布局

核心功能:
1. 自动对齐
2. 智能间距计算
3. 层级自动调整
4. 对比度与平衡管理
5. style一致性保持
6. 响应式排版
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math

# ============= 枚举定义 =============

class Alignment(Enum):
    """对齐方式"""
    LEFT = "左对齐"
    CENTER = "居中对齐"
    RIGHT = "右对齐"
    JUSTIFY = "两端对齐"

class HierarchyLevel(Enum):
    """层级级别"""
    TITLE = 0      # 标题
    SUBTITLE = 1   # 副标题
    BODY = 2       # 正文
    CAPTION = 3    # 说明文字

# ============= 数据类定义 =============

@dataclass
class Element:
    """幻灯片元素"""
    id: str
    type: str  # text, image, chart, shape
    x: float
    y: float
    width: float
    height: float
    content: Optional[str] = None
    hierarchy: Optional[HierarchyLevel] = None

@dataclass
class SlideLayout:
    """幻灯片布局"""
    elements: List[Element]
    alignment: Alignment
    spacing: float
    grid_visible: bool = False

@dataclass
class DesignRule:
    """设计规则"""
    name: str
    description: str
    priority: int  # 1-10, 10为最高优先级
    apply_function: callable

# ============= 智能设计规则引擎 =============

class SmartDesignEngine:
    """
    智能设计规则引擎

    将专业设计准则转化为可执行的规则
    实现自动对齐,间距调整,层级管理,对比度控制等功能
    """

    def __init__(self):
        """init设计引擎"""
        self.golden_ratio = 1.618  # 黄金比例
        self.base_spacing_ratio = 0.05  # 基础间距比例
        self.hierarchy_ratios = {
            HierarchyLevel.TITLE: 2.5,
            HierarchyLevel.SUBTITLE: 1.8,
            HierarchyLevel.BODY: 1.0,
            HierarchyLevel.CAPTION: 0.7
        }
        self.design_rules = self._init_design_rules()

    def _init_design_rules(self) -> List[DesignRule]:
        """
        init设计规则

        Returns:
            List[DesignRule]: 设计规则列表
        """
        rules = [
            DesignRule(
                name="自动对齐",
                description="确保文本,图像等元素在幻灯片内及跨幻灯片之间保持视觉上的整齐",
                priority=10,
                apply_function=self._apply_alignment
            ),
            DesignRule(
                name="智能间距",
                description="自动调整元素周围的边距和填充,避免拥挤或过于松散,保持呼吸感",
                priority=9,
                apply_function=self._apply_spacing
            ),
            DesignRule(
                name="层级管理",
                description="根据内容重要性自动调整字体大小和样式",
                priority=8,
                apply_function=self._apply_hierarchy
            ),
            DesignRule(
                name="对比度控制",
                description="管理颜色对比度以确保可读性,并保持版面的视觉平衡",
                priority=8,
                apply_function=self._apply_contrast
            ),
            DesignRule(
                name="style一致",
                description="自动unified整个演示文稿的字体,颜色和视觉style",
                priority=7,
                apply_function=self._apply_consistency
            ),
            DesignRule(
                name="视觉平衡",
                description="保持版面的视觉平衡,避免某一侧过重",
                priority=7,
                apply_function=self._apply_balance
            )
        ]
        return rules

    # ============= 核心功能 =============

    def auto_layout(self, elements: List[Element], page_width: float, page_height: float) -> SlideLayout:
        """
        自动布局

        Args:
            elements (List[Element]): 元素列表
            page_width (float): 页面宽度
            page_height (float): 页面高度

        Returns:
            SlideLayout: 自动布局结果
        """
        # 1. 按优先级应用设计规则
        for rule in sorted(self.design_rules, key=lambda r: r.priority, reverse=True):
            elements = rule.apply_function(elements, page_width, page_height)

        # 2. 计算间距
        spacing = self._calculate_spacing(len(elements), page_width, page_height)

        # 3. 创建布局
        layout = SlideLayout(
            elements=elements,
            alignment=Alignment.LEFT,
            spacing=spacing
        )

        return layout

    # ============= 设计规则应用函数 =============

    def _apply_alignment(self, elements: List[Element], page_width: float, page_height: float) -> List[Element]:
        """
        应用自动对齐规则

        Args:
            elements (List[Element]): 元素列表
            page_width (float): 页面宽度
            page_height (float): 页面高度

        Returns:
            List[Element]: 对齐后的元素列表
        """
        # 1. 按x坐标排序
        elements_sorted = sorted(elements, key=lambda e: e.x)

        # 2. 检测对齐参考线
        reference_lines = []
        for i in range(len(elements_sorted)):
            for j in range(i + 1, len(elements_sorted)):
                diff = abs(elements_sorted[i].x - elements_sorted[j].x)
                if diff < 20:  # 20像素容差
                    avg_x = (elements_sorted[i].x + elements_sorted[j].x) / 2
                    reference_lines.append(avg_x)

        # 3. 应用对齐
        for element in elements:
            # 检查是否有合适的参考线
            aligned = False
            for ref_x in reference_lines:
                if abs(element.x - ref_x) < 30:
                    element.x = ref_x
                    aligned = True
                    break

            # 如果没有对齐到参考线,对齐到网格
            if not aligned:
                grid_size = 50  # 网格大小
                element.x = round(element.x / grid_size) * grid_size

        return elements

    def _apply_spacing(self, elements: List[Element], page_width: float, page_height: float) -> List[Element]:
        """
        应用智能间距规则

        Args:
            elements (List[Element]): 元素列表
            page_width (float): 页面宽度
            page_height (float): 页面高度

        Returns:
            List[Element]: 调整间距后的元素列表
        """
        # 1. 计算基础间距
        base_spacing = min(page_width, page_height) * self.base_spacing_ratio

        # 2. 黄金比例调整
        adjusted_spacing = base_spacing / self.golden_ratio

        # 3. 根据元素数量调整
        num_elements = len(elements)
        if num_elements <= 3:
            spacing = adjusted_spacing * 1.2
        elif num_elements <= 6:
            spacing = adjusted_spacing
        else:
            spacing = adjusted_spacing * 0.8

        # 4. 应用间距
        # 按y坐标排序
        elements_sorted = sorted(elements, key=lambda e: e.y)

        for i in range(1, len(elements_sorted)):
            elements_sorted[i].y = elements_sorted[i-1].y + elements_sorted[i-1].height + spacing

        return elements

    def _apply_hierarchy(self, elements: List[Element], page_width: float, page_height: float) -> List[Element]:
        """
        应用层级管理规则

        Args:
            elements (List[Element]): 元素列表
            page_width (float): 页面宽度
            page_height (float): 页面高度

        Returns:
            List[Element]: 调整层级后的元素列表
        """
        base_font_size = 14  # 基准字号

        for element in elements:
            if element.hierarchy is not None:
                ratio = self.hierarchy_ratios[element.hierarchy]
                element.font_size = base_font_size * ratio
            else:
                element.font_size = base_font_size

        return elements

    def _apply_contrast(self, elements: List[Element], page_width: float, page_height: float) -> List[Element]:
        """
        应用对比度控制规则

        Args:
            elements (List[Element]): 元素列表
            page_width (float): 页面宽度
            page_height (float): 页面高度

        Returns:
            List[Element]: 调整对比度后的元素列表
        """
        # 简化版对比度检查
        # 实际应用中可使用更精确的亮度计算
        for element in elements:
            if hasattr(element, 'text_color') and hasattr(element, 'background_color'):
                # 计算亮度差
                brightness_diff = self._calculate_brightness_diff(
                    element.text_color,
                    element.background_color
                )

                # WCAG 4.5:1标准
                if brightness_diff < 4.5:
                    # 调整颜色
                    element.text_color = self._adjust_color_for_contrast(
                        element.text_color,
                        element.background_color
                    )

        return elements

    def _apply_consistency(self, elements: List[Element], page_width: float, page_height: float) -> List[Element]:
        """
        应用style一致性规则

        Args:
            elements (List[Element]): 元素列表
            page_width (float): 页面宽度
            page_height (float): 页面高度

        Returns:
            List[Element]: unifiedstyle后的元素列表
        """
        # 1. 提取相同类型元素的样式
        style_map = {}
        for element in elements:
            if element.type not in style_map:
                style_map[element.type] = {
                    'font_name': element.font_name,
                    'font_color': element.font_color,
                    'font_size': element.font_size
                }
            else:
                # unified样式
                element.font_name = style_map[element.type]['font_name']
                element.font_color = style_map[element.type]['font_color']
                element.font_size = style_map[element.type]['font_size']

        return elements

    def _apply_balance(self, elements: List[Element], page_width: float, page_height: float) -> List[Element]:
        """
        应用视觉平衡规则

        Args:
            elements (List[Element]): 元素列表
            page_width (float): 页面宽度
            page_height (float): 页面高度

        Returns:
            List[Element]: 平衡后的元素列表
        """
        # 1. 计算重心
        center_x = sum(e.x + e.width/2 for e in elements) / len(elements)
        center_y = sum(e.y + e.height/2 for e in elements) / len(elements)

        # 2. 计算页面中心
        page_center_x = page_width / 2
        page_center_y = page_height / 2

        # 3. 计算偏移量
        offset_x = page_center_x - center_x
        offset_y = page_center_y - center_y

        # 4. 应用偏移(只移动非对齐元素)
        for element in elements:
            element.x += offset_x
            element.y += offset_y

        return elements

    # ============= 辅助函数 =============

    def _calculate_spacing(self, num_elements: int, page_width: float, page_height: float) -> float:
        """
        计算元素间距

        Args:
            num_elements (int): 元素数量
            page_width (float): 页面宽度
            page_height (float): 页面高度

        Returns:
            float: 间距
        """
        base_spacing = min(page_width, page_height) * self.base_spacing_ratio
        adjusted_spacing = base_spacing / self.golden_ratio

        if num_elements <= 3:
            return adjusted_spacing * 1.2
        elif num_elements <= 6:
            return adjusted_spacing
        else:
            return adjusted_spacing * 0.8

    def _calculate_brightness_diff(self, color1: str, color2: str) -> float:
        """
        计算颜色亮度差(简化版)

        Args:
            color1 (str): 颜色1 (HEX格式)
            color2 (str): 颜色2 (HEX格式)

        Returns:
            float: 亮度差
        """
        # 简化实现,实际应使用完整亮度计算公式
        # 这里假设输入格式为 #RRGGBB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

        brightness1 = (r1 * 299 + g1 * 587 + b1 * 114) / 1000
        brightness2 = (r2 * 299 + g2 * 587 + b2 * 114) / 1000

        diff = (max(brightness1, brightness2) + 0.05) / (min(brightness1, brightness2) + 0.05)

        return diff

    def _adjust_color_for_contrast(self, text_color: str, background_color: str) -> str:
        """
        调整颜色以满足对比度要求

        Args:
            text_color (str): 文字颜色 (HEX格式)
            background_color (str): 背景颜色 (HEX格式)

        Returns:
            str: 调整后的文字颜色
        """
        # 简化实现:如果背景较亮,返回黑色;否则返回白色
        brightness = int(background_color[1:3], 16) * 299 + \
                     int(background_color[3:5], 16) * 587 + \
                     int(background_color[5:7], 16) * 114

        if brightness > 128 * 1000:
            return "#000000"
        else:
            return "#FFFFFF"

    # ============= 响应式排版 =============

    def responsive_layout(self, elements: List[Element], content_change: str) -> SlideLayout:
        """
        响应式排版

        Args:
            elements (List[Element]): 元素列表
            content_change (str): 内容变化类型

        Returns:
            SlideLayout: 响应式布局结果
        """
        # 根据内容变化类型调整布局
        if content_change == "add":
            # 添加内容:重新计算间距
            spacing = self._calculate_spacing(len(elements), 1000, 750)
        elif content_change == "remove":
            # 删除内容:重新平衡
            elements = self._apply_balance(elements, 1000, 750)
        elif content_change == "resize":
            # 内容长度变化:调整字号和间距
            elements = self._apply_spacing(elements, 1000, 750)
        else:
            # 默认:应用所有规则
            elements = self.auto_layout(elements, 1000, 750).elements

        return SlideLayout(
            elements=elements,
            alignment=Alignment.LEFT,
            spacing=50  # 默认间距
        )

    # ============= 设计规则管理 =============

    def get_design_rules(self) -> List[DesignRule]:
        """
        get设计规则列表

        Returns:
            List[DesignRule]: 设计规则列表
        """
        return self.design_rules.copy()

    def add_design_rule(self, rule: DesignRule):
        """
        添加设计规则

        Args:
            rule (DesignRule): 设计规则
        """
        self.design_rules.append(rule)

    def remove_design_rule(self, rule_name: str):
        """
        移除设计规则

        Args:
            rule_name (str): 规则名称
        """
        self.design_rules = [r for r in self.design_rules if r.name != rule_name]

# ============= 示例使用 =============

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

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
            width=800,
            height=200,
            content="正文内容",
            hierarchy=HierarchyLevel.BODY
        )
    ]

    # 自动布局
    layout = engine.auto_layout(elements, 1000, 750)

    print("=" * 60)
    print("自动布局结果")
    print("=" * 60)
    print(f"元素数量: {len(layout.elements)}")
    print(f"间距: {layout.spacing:.2f}")
    print(f"对齐方式: {layout.alignment.value}")

    for element in layout.elements:
        print(f"\n元素 {element.id}:")
        print(f"  类型: {element.type}")
        print(f"  位置: ({element.x:.2f}, {element.y:.2f})")
        print(f"  大小: {element.width:.2f} x {element.height:.2f}")
        if hasattr(element, 'font_size'):
            print(f"  字号: {element.font_size:.2f}")

    # 打印设计规则
    print("\n" + "=" * 60)
    print("设计规则")
    print("=" * 60)
    for i, rule in enumerate(engine.get_design_rules(), 1):
        print(f"{i}. {rule.name} (优先级: {rule.priority})")
        print(f"   {rule.description}")
