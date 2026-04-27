"""PPT智能generate与美化模块

注意：此模块依赖 python-pptx 第三方库。如未安装，导入时提供空桩，
使用 PPT 功能前请执行 pip install python-pptx。
"""

import warnings

_PPTX_AVAILABLE = False
try:
    import pptx  # noqa: F401
    _PPTX_AVAILABLE = True
except ImportError:
    warnings.warn(
        "python-pptx 未安装，PPT模块将以降级模式运行。"
        "安装命令: pip install python-pptx",
        ImportWarning,
        stacklevel=2,
    )

if _PPTX_AVAILABLE:
    from .ppt_generator import PPTContentGenerator, ContentFormat, SlideType, ContentNode, SlideSpec
    from .ppt_beautifier import PPTBeautifier, ColorScheme, LayoutType, ColorPalette, FontPair
    from .ppt_learning import PPTLearningEngine, LearningCategory, SearchResult, PPTKnowledge
    from .ppt_memory_integration import PPTMemoryIntegrator
    from .ppt_service import PPTService, quick_generate, quick_beautify
else:
    # 空桩降级 — 模块可导入但功能不可用
    PPTContentGenerator = PPTBeautifier = PPTLearningEngine = PPTMemoryIntegrator = PPTService = None
    ContentFormat = SlideType = ColorScheme = LayoutType = ColorPalette = FontPair = None
    ContentNode = SlideSpec = SearchResult = PPTKnowledge = None
    quick_generate = quick_beautify = None

__version__ = "1.0.0"
__pptx_available__ = _PPTX_AVAILABLE
__all__ = [
    "PPTContentGenerator", "PPTBeautifier", "PPTLearningEngine",
    "PPTMemoryIntegrator", "PPTService", "ContentFormat", "SlideType",
    "ColorScheme", "LayoutType", "ContentNode", "SlideSpec",
    "SearchResult", "PPTKnowledge", "ColorPalette", "FontPair",
    "quick_generate", "quick_beautify",
]
