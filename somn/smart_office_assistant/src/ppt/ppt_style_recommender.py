"""
__all__ = [
    'format_style_recommendation',
    'get_color_harmony_score',
    'get_design_principles',
    'recommend_by_content',
    'recommend_by_scene',
    'recommend_color_by_mood',
]

PPTstyle智能推荐模块

智能推荐系统

核心功能:
1. 场景recognize与style推荐
2. 配色方案智能推荐
3. 排版模式自动选择
4. 字体智能选择
5. 设计规则应用
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re

# ============= 枚举定义 =============

class SceneType(Enum):
    """场景类型枚举"""
    BUSINESS_REPORT = "商务汇报"
    PROJECT_PITCH = "项目路演"
    EDUCATION_TRAINING = "教育培训"
    CREATIVE_DESIGN = "创意设计"
    TECH_DEMO = "科技展示"
    ACADEMIC_REPORT = "学术报告"
    FINANCING_PITCH = "融资路演"
    ANNUAL_SUMMARY = "年度总结"
    MARKETING_PLAN = "营销策划"
    PRODUCT_LAUNCH = "产品发布"

class LayoutType(Enum):
    """排版类型枚举"""
    SINGLE_COLUMN = "单栏布局"
    DUAL_COLUMN = "双栏布局"
    TRIPLE_COLUMN = "三栏布局"
    CENTER_FOCUS = "中心焦点布局"
    Z_FLOW = "Z型布局"
    DIAGONAL = "对角线布局"
    GRID = "网格布局"
    MODULAR = "模块化布局"
    TIMELINE = "时间轴排版"
    FUNNEL = "漏斗形排版"
    COMPARISON = "对比排版"
    LOOP = "循环流程排版"
    WATERFALL = "瀑布流布局"

class ColorScheme(Enum):
    """配色方案枚举"""
    CLASSIC_BLUE_GRAY = "经典蓝灰"  # OfficePLUSstyle
    ENTERPRISE_GREEN = "企业绿系"    # 增长稳定
    FINANCIAL_GOLD_GRAY = "金融金灰"  # 高级稳重
    MORANDI_BLUE = "莫兰迪蓝"       # 优品PPTstyle
    JAPANESE_FRESH = "日式清新"     # 舒适温和
    MACARON = "马卡龙"             # SlidesCarnivalstyle
    COLORFUL = "多彩撞色"           # 视觉冲击
    CYBERPUNK = "赛博朋克"         # Gammastyle
    MINIMAL_TECH = "极简科技"       # 现代科技
    WARM_LEARNING = "温暖学习"     # 教育培训

class FontFamily(Enum):
    """字体系列枚举"""
    MODERN = "现代style"
    TRADITIONAL = "传统style"
    ELEGANT = "优雅style"
    CASUAL = "休闲style"

# ============= 数据类定义 =============

@dataclass
class ColorPalette:
    """配色方案"""
    primary: str      # 主色 (60%)
    secondary: str    # 辅色 (30%)
    accent: str       # 强调色 (10%)
    background: str   # 背景色
    text: str         # 文字色

@dataclass
class FontRecommendation:
    """字体推荐"""
    title: str        # 标题字体
    subtitle: str     # 副标题字体
    body: str         # 正文字体
    english_title: str  # 英文标题
    english_body: str   # 英文正文

@dataclass
class StyleRecommendation:
    """style推荐"""
    scene: SceneType
    platform: str  # 参考平台
    color_scheme: ColorScheme
    color_palette: ColorPalette
    layout: LayoutType
    fonts: FontRecommendation
    design_rules: List[str]
    confidence: float  # 推荐置信度 (0-1)

# ============= 配色方案库 =============

COLOR_SCHEMES = {
    ColorScheme.CLASSIC_BLUE_GRAY: ColorPalette(
        primary="#1F4E79",
        secondary="#5B9BD5",
        accent="#FFC000",
        background="#FFFFFF",
        text="#424242"
    ),
    ColorScheme.ENTERPRISE_GREEN: ColorPalette(
        primary="#1E7B48",
        secondary="#70AD47",
        accent="#ED7D31",
        background="#FFFFFF",
        text="#424242"
    ),
    ColorScheme.FINANCIAL_GOLD_GRAY: ColorPalette(
        primary="#2F4F4F",
        secondary="#5F7A7A",
        accent="#D4AF37",
        background="#F5F5F5",
        text="#212121"
    ),
    ColorScheme.MORANDI_BLUE: ColorPalette(
        primary="#7B8FA1",
        secondary="#B5C4D1",
        accent="#E57373",
        background="#F8F9FA",
        text="#37474F"
    ),
    ColorScheme.JAPANESE_FRESH: ColorPalette(
        primary="#66BB6A",
        secondary="#A5D6A7",
        accent="#FFB74D",
        background="#FFFFFF",
        text="#455A64"
    ),
    ColorScheme.MACARON: ColorPalette(
        primary="#FF6B9D",
        secondary="#C44DFF",
        accent="#FFD93D",
        background="#F3E5F5",
        text="#4A148C"
    ),
    ColorScheme.COLORFUL: ColorPalette(
        primary="#2196F3",
        secondary="#FF4081",
        accent="#4CAF50",
        background="#FAFAFA",
        text="#212121"
    ),
    ColorScheme.CYBERPUNK: ColorPalette(
        primary="#7B2CBF",
        secondary="#00F5FF",
        accent="#FF006E",
        background="#10002B",
        text="#E0AAFF"
    ),
    ColorScheme.MINIMAL_TECH: ColorPalette(
        primary="#003049",
        secondary="#669BBC",
        accent="#F72585",
        background="#FFFFFF",
        text="#14213D"
    ),
    ColorScheme.WARM_LEARNING: ColorPalette(
        primary="#006400",
        secondary="#32CD32",
        accent="#FFD700",
        background="#FFFFE0",
        text="#333333"
    )
}

# ============= 字体推荐库 =============

FONT_RECOMMENDATIONS = {
    FontFamily.MODERN: FontRecommendation(
        title="思源黑体 Bold",
        subtitle="思源黑体 Medium",
        body="思源黑体 Regular",
        english_title="Montserrat Bold",
        english_body="Open Sans Regular"
    ),
    FontFamily.TRADITIONAL: FontRecommendation(
        title="方正兰亭黑 Bold",
        subtitle="方正兰亭黑 Medium",
        body="方正兰亭黑 Regular",
        english_title="Garamond Bold",
        english_body="Garamond Regular"
    ),
    FontFamily.ELEGANT: FontRecommendation(
        title="思源宋体 Bold",
        subtitle="思源宋体 Medium",
        body="思源宋体 Regular",
        english_title="Playfair Display Bold",
        english_body="Playfair Display Regular"
    ),
    FontFamily.CASUAL: FontRecommendation(
        title="站酷庆科黄油体 Bold",
        subtitle="站酷庆科黄油体 Regular",
        body="微软雅黑 Regular",
        english_title="Poppins Bold",
        english_body="Poppins Regular"
    )
}

# ============= 场景-stylemapping =============

SCENE_STYLE_MAPPING = {
    SceneType.BUSINESS_REPORT: {
        "platform": "OfficePLUS",
        "color_scheme": ColorScheme.CLASSIC_BLUE_GRAY,
        "layout": LayoutType.SINGLE_COLUMN,
        "font_family": FontFamily.MODERN
    },
    SceneType.PROJECT_PITCH: {
        "platform": "Beautiful.ai",
        "color_scheme": ColorScheme.ENTERPRISE_GREEN,
        "layout": LayoutType.CENTER_FOCUS,
        "font_family": FontFamily.MODERN
    },
    SceneType.EDUCATION_TRAINING: {
        "platform": "Canva",
        "color_scheme": ColorScheme.WARM_LEARNING,
        "layout": LayoutType.MODULAR,
        "font_family": FontFamily.MODERN
    },
    SceneType.CREATIVE_DESIGN: {
        "platform": "SlidesCarnival",
        "color_scheme": ColorScheme.MACARON,
        "layout": LayoutType.WATERFALL,
        "font_family": FontFamily.CASUAL
    },
    SceneType.TECH_DEMO: {
        "platform": "Gamma",
        "color_scheme": ColorScheme.CYBERPUNK,
        "layout": LayoutType.Z_FLOW,
        "font_family": FontFamily.MODERN
    },
    SceneType.ACADEMIC_REPORT: {
        "platform": "优品PPT",
        "color_scheme": ColorScheme.MORANDI_BLUE,
        "layout": LayoutType.SINGLE_COLUMN,
        "font_family": FontFamily.ELEGANT
    },
    SceneType.FINANCING_PITCH: {
        "platform": "稻壳儿",
        "color_scheme": ColorScheme.FINANCIAL_GOLD_GRAY,
        "layout": LayoutType.CENTER_FOCUS,
        "font_family": FontFamily.TRADITIONAL
    },
    SceneType.ANNUAL_SUMMARY: {
        "platform": "OfficePLUS",
        "color_scheme": ColorScheme.CLASSIC_BLUE_GRAY,
        "layout": LayoutType.TIMELINE,
        "font_family": FontFamily.MODERN
    },
    SceneType.MARKETING_PLAN: {
        "platform": "Canva",
        "color_scheme": ColorScheme.COLORFUL,
        "layout": LayoutType.MODULAR,
        "font_family": FontFamily.CASUAL
    },
    SceneType.PRODUCT_LAUNCH: {
        "platform": "Gamma",
        "color_scheme": ColorScheme.MINIMAL_TECH,
        "layout": LayoutType.CENTER_FOCUS,
        "font_family": FontFamily.MODERN
    }
}

# ============= 设计规则库 =============

DESIGN_RULES = {
    "alignment": "元素对齐 - 自动计算元素位置,保持视觉对齐",
    "spacing": "间距一致 - 元素间距按黄金比例(1.618)计算",
    "hierarchy": "层级清晰 - 标题2.5x,副标题1.8x,正文1.0x",
    "contrast": "对比度足够 - 确保WCAG 4.5:1标准",
    "consistency": "styleunified - 跨页应用相同字体,颜色,样式"
}

# ============= 核心类定义 =============

class PPTStyleRecommender:
    """
    PPTstyle智能推荐系统
    """

    def __init__(self):
        """init推荐系统"""
        self.scene_keywords = self._init_scene_keywords()

    def _init_scene_keywords(self) -> Dict[str, SceneType]:
        """
        init场景关键词mapping

        Returns:
            Dict[str, SceneType]: 关键词到场景类型的mapping
        """
        keywords = {
            # 商务汇报相关
            "工作总结": SceneType.BUSINESS_REPORT,
            "周报": SceneType.BUSINESS_REPORT,
            "月报": SceneType.BUSINESS_REPORT,
            "季度报告": SceneType.BUSINESS_REPORT,
            "业务汇报": SceneType.BUSINESS_REPORT,
            "绩效报告": SceneType.BUSINESS_REPORT,
            "年终总结": SceneType.ANNUAL_SUMMARY,

            # 项目路演相关
            "项目路演": SceneType.PROJECT_PITCH,
            "创业路演": SceneType.FINANCING_PITCH,
            "融资": SceneType.FINANCING_PITCH,
            "招商": SceneType.FINANCING_PITCH,
            "投资": SceneType.FINANCING_PITCH,

            # 教育培训相关
            "培训": SceneType.EDUCATION_TRAINING,
            "教学": SceneType.EDUCATION_TRAINING,
            "课程": SceneType.EDUCATION_TRAINING,
            "讲座": SceneType.EDUCATION_TRAINING,
            "课件": SceneType.EDUCATION_TRAINING,

            # 科技展示相关
            "技术": SceneType.TECH_DEMO,
            "产品": SceneType.PRODUCT_LAUNCH,
            "科技": SceneType.TECH_DEMO,
            "AI": SceneType.TECH_DEMO,
            "人工智能": SceneType.TECH_DEMO,

            # 营销策划相关
            "营销": SceneType.MARKETING_PLAN,
            "推广": SceneType.MARKETING_PLAN,
            "活动": SceneType.MARKETING_PLAN,

            # 学术报告相关
            "学术": SceneType.ACADEMIC_REPORT,
            "论文": SceneType.ACADEMIC_REPORT,
            "研究": SceneType.ACADEMIC_REPORT,
            "论文答辩": SceneType.ACADEMIC_REPORT,

            # 创意设计相关
            "创意": SceneType.CREATIVE_DESIGN,
            "设计": SceneType.CREATIVE_DESIGN,
            "艺术": SceneType.CREATIVE_DESIGN,
        }
        return keywords

    def recommend_by_scene(self, scene: str) -> StyleRecommendation:
        """
        根据场景文本推荐style

        Args:
            scene (str): 场景描述文本

        Returns:
            StyleRecommendation: style推荐结果
        """
        # 1. 场景recognize
        scene_type = self._detect_scene(scene)

        # 2. getmapping配置
        config = SCENE_STYLE_MAPPING.get(scene_type, SCENE_STYLE_MAPPING[SceneType.BUSINESS_REPORT])

        # 3. 构建推荐结果
        color_palette = COLOR_SCHEMES[config["color_scheme"]]
        fonts = FONT_RECOMMENDATIONS[config["font_family"]]

        # 4. 计算置信度
        confidence = self._calculate_confidence(scene, scene_type)

        return StyleRecommendation(
            scene=scene_type,
            platform=config["platform"],
            color_scheme=config["color_scheme"],
            color_palette=color_palette,
            layout=config["layout"],
            fonts=fonts,
            design_rules=list(DESIGN_RULES.values()),
            confidence=confidence
        )

    def recommend_by_content(self, content: str, audience: str = "") -> StyleRecommendation:
        """
        根据内容和受众推荐style

        Args:
            content (str): 内容文本
            audience (str): 受众描述

        Returns:
            StyleRecommendation: style推荐结果
        """
        # 1. 分析内容characteristics
        content_features = self._analyze_content(content)

        # 2. 结合受众信息
        scene_type = self._infer_scene_from_content(content, audience)

        # 3. getmapping配置
        config = SCENE_STYLE_MAPPING.get(scene_type, SCENE_STYLE_MAPPING[SceneType.BUSINESS_REPORT])

        # 4. 构建推荐结果
        color_palette = COLOR_SCHEMES[config["color_scheme"]]
        fonts = FONT_RECOMMENDATIONS[config["font_family"]]

        # 5. 根据内容characteristics微调
        layout = self._adjust_layout_by_content(config["layout"], content_features)

        # 6. 计算置信度
        confidence = self._calculate_confidence(content, scene_type)

        return StyleRecommendation(
            scene=scene_type,
            platform=config["platform"],
            color_scheme=config["color_scheme"],
            color_palette=color_palette,
            layout=layout,
            fonts=fonts,
            design_rules=list(DESIGN_RULES.values()),
            confidence=confidence
        )

    def _detect_scene(self, text: str) -> SceneType:
        """
        检测场景类型

        Args:
            text (str): 文本

        Returns:
            SceneType: 场景类型
        """
        # 1. 关键词匹配
        for keyword, scene_type in self.scene_keywords.items():
            if keyword in text:
                return scene_type

        # 2. 默认商务汇报
        return SceneType.BUSINESS_REPORT

    def _analyze_content(self, content: str) -> Dict:
        """
        分析内容characteristics

        Args:
            content (str): 内容文本

        Returns:
            Dict: 内容characteristics字典
        """
        features = {
            "length": len(content),
            "has_chart": bool(re.search(r'图表|数据|统计|趋势|增长', content)),
            "has_timeline": bool(re.search(r'时间|历史|发展|历程|年度', content)),
            "has_comparison": bool(re.search(r'对比|差异|优劣|前后', content)),
            "has_image": bool(re.search(r'图片|照片|截图|展示', content)),
            "chart_count": len(re.findall(r'图表|数据', content))
        }

        return features

    def _infer_scene_from_content(self, content: str, audience: str) -> SceneType:
        """
        从内容和受众推断场景

        Args:
            content (str): 内容文本
            audience (str): 受众描述

        Returns:
            SceneType: 推断的场景类型
        """
        combined_text = content + " " + audience

        # 1. 优先检测场景关键词
        scene_type = self._detect_scene(combined_text)
        if scene_type != SceneType.BUSINESS_REPORT:
            return scene_type

        # 2. 根据受众推断
        if "学生" in audience or "学员" in audience:
            return SceneType.EDUCATION_TRAINING
        elif "投资者" in audience or "投资人" in audience:
            return SceneType.FINANCING_PITCH
        elif "客户" in audience or "用户" in audience:
            return SceneType.MARKETING_PLAN
        elif "专家" in audience or "学者" in audience:
            return SceneType.ACADEMIC_REPORT

        # 3. 默认商务汇报
        return SceneType.BUSINESS_REPORT

    def _adjust_layout_by_content(self, base_layout: LayoutType, content_features: Dict) -> LayoutType:
        """
        根据内容characteristics调整布局

        Args:
            base_layout (LayoutType): 基础布局
            content_features (Dict): 内容characteristics

        Returns:
            LayoutType: 调整后的布局
        """
        # 如果内容包含时间线相关,使用时间轴布局
        if content_features["has_timeline"]:
            return LayoutType.TIMELINE

        # 如果内容包含对比,使用对比布局
        if content_features["has_comparison"]:
            return LayoutType.COMPARISON

        # 如果图表数量>3,使用网格布局
        if content_features["chart_count"] > 3:
            return LayoutType.GRID

        # 如果包含图片和文字,使用双栏布局
        if content_features["has_image"] and content_features["length"] > 500:
            return LayoutType.DUAL_COLUMN

        # 否则保持基础布局
        return base_layout

    def _calculate_confidence(self, text: str, scene_type: SceneType) -> float:
        """
        计算推荐置信度

        Args:
            text (str): 文本
            scene_type (SceneType): 场景类型

        Returns:
            float: 置信度 (0-1)
        """
        confidence = 0.5  # 基础置信度

        # 1. 关键词匹配加分
        for keyword in self.scene_keywords.keys():
            if keyword in text:
                confidence += 0.1
                break

        # 2. 文本长度加分
        if len(text) > 100:
            confidence += 0.2

        # 3. 场景明确性加分
        if scene_type != SceneType.BUSINESS_REPORT:
            confidence += 0.2

        # 4. 限制在[0, 1]区间
        confidence = max(0.0, min(1.0, confidence))

        return confidence

    def recommend_color_by_mood(self, mood: str) -> ColorPalette:
        """
        根据情绪/氛围推荐配色

        Args:
            mood (str): 情绪描述(如"稳重","活泼","专业","温馨")

        Returns:
            ColorPalette: 配色方案
        """
        mood_map = {
            "稳重": ColorScheme.CLASSIC_BLUE_GRAY,
            "专业": ColorScheme.ENTERPRISE_GREEN,
            "高级": ColorScheme.FINANCIAL_GOLD_GRAY,
            "简约": ColorScheme.MORANDI_BLUE,
            "清新": ColorScheme.JAPANESE_FRESH,
            "活泼": ColorScheme.MACARON,
            "鲜艳": ColorScheme.COLORFUL,
            "科技": ColorScheme.CYBERPUNK,
            "现代": ColorScheme.MINIMAL_TECH,
            "温馨": ColorScheme.WARM_LEARNING
        }

        # 关键词匹配
        for keyword, scheme in mood_map.items():
            if keyword in mood:
                return COLOR_SCHEMES[scheme]

        # 默认商务配色
        return COLOR_SCHEMES[ColorScheme.CLASSIC_BLUE_GRAY]

    def get_design_principles(self) -> Dict[str, str]:
        """
        get设计原则

        Returns:
            Dict[str, str]: 设计原则字典
        """
        return DESIGN_RULES.copy()

    def get_color_harmony_score(self, palette: ColorPalette) -> float:
        """
        计算配色和谐度

        Args:
            palette (ColorPalette): 配色方案

        Returns:
            float: 和谐度分数 (0-100)
        """
        # 简化版和谐度计算
        # 实际应用中可使用更复杂的颜色理论算法
        score = 70.0  # 基础分

        # 主色和辅色对比度
        score += 10.0

        # 强调色对比度
        score += 10.0

        # 文字和背景对比度
        score += 10.0

        return min(100.0, score)

# ============= 工具函数 =============

def format_style_recommendation(recommendation: StyleRecommendation) -> str:
    """
    格式化style推荐结果

    Args:
        recommendation (StyleRecommendation): style推荐

    Returns:
        str: 格式化的推荐文本
    """
    lines = [
        f"[场景类型]{recommendation.scene.value}",
        f"[参考平台]{recommendation.platform}",
        f"[配色方案]{recommendation.color_scheme.value}",
        f"  - 主色(60%): {recommendation.color_palette.primary}",
        f"  - 辅色(30%): {recommendation.color_palette.secondary}",
        f"  - 强调色(10%): {recommendation.color_palette.accent}",
        f"  - 背景色: {recommendation.color_palette.background}",
        f"  - 文字色: {recommendation.color_palette.text}",
        f"[排版布局]{recommendation.layout.value}",
        f"[字体推荐]",
        f"  - 中文标题: {recommendation.fonts.title}",
        f"  - 中文正文: {recommendation.fonts.body}",
        f"  - 英文标题: {recommendation.fonts.english_title}",
        f"  - 英文正文: {recommendation.fonts.english_body}",
        f"[设计规则]",
        f"  - {recommendation.design_rules[0]}",
        f"  - {recommendation.design_rules[1]}",
        f"  - {recommendation.design_rules[2]}",
        f"[推荐置信度]{recommendation.confidence*100:.0f}%"
    ]

    return "\n".join(lines)

# ============= 示例使用 =============

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

    # 示例1: 根据场景推荐
    print("=" * 60)
    print("示例1: 根据场景推荐")
    print("=" * 60)
    recommendation1 = recommender.recommend_by_scene("年度工作总结报告")
    print(format_style_recommendation(recommendation1))
    print()

    # 示例2: 根据内容和受众推荐
    print("=" * 60)
    print("示例2: 根据内容和受众推荐")
    print("=" * 60)
    content = "本年度销售额增长25%,用户留存率提升15%.通过数据图表展示趋势,对比前后差异."
    audience = "公司高管"
    recommendation2 = recommender.recommend_by_content(content, audience)
    print(format_style_recommendation(recommendation2))
    print()

    # 示例3: 根据情绪推荐配色
    print("=" * 60)
    print("示例3: 根据情绪推荐配色")
    print("=" * 60)
    palette = recommender.recommend_color_by_mood("活泼,创意")
    print(f"主色: {palette.primary}")
    print(f"辅色: {palette.secondary}")
    print(f"强调色: {palette.accent}")
    print(f"和谐度: {recommender.get_color_harmony_score(palette):.0f}/100")
    print()

    # 示例4: get设计原则
    print("=" * 60)
    print("示例4: get设计原则")
    print("=" * 60)
    principles = recommender.get_design_principles()
    for key, value in principles.items():
        print(f"{key}: {value}")
