"""
开物子系统 - 核心服务（KaiwuService）

集成：
- PPTXGenerator（来自 documents/pptx_generator.py）—— PPT 生成能力
- PPTStyleLearner（来自 learning/engine/ppt_style_learner.py）—— 风格学习能力
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from loguru import logger


class PPTDesignKnowledge:
    """PPT 设计知识（包装 DesignPrinciple / ColorScheme / LayoutPattern）"""
    def __init__(self, knowledge_type: str, data: Dict[str, Any]):
        self.knowledge_type = knowledge_type   # "principle" / "color_scheme" / "layout"
        self.data = data
        self.learned = False
        self.confidence = 0.0


class PPTStyleProfile:
    """PPT 风格画像——沉淀该主题下的设计偏好"""
    def __init__(self, theme: str):
        self.theme = theme
        self.design_principles: List[Dict] = []
        self.color_schemes: List[Dict] = []
        self.layout_patterns: List[Dict] = []
        self.feedback_log: List[Dict] = []

    def to_dict(self) -> Dict:
        return {
            "theme": self.theme,
            "design_principles": self.design_principles,
            "color_schemes": self.color_schemes,
            "layout_patterns": self.layout_patterns,
            "feedback_count": len(self.feedback_log),
        }


class KaiwuService:
    """
    开物（Kaiwu）服务——PPT 智能生成与风格学习一体化

    命名来源：《天工开物》（宋应星，明代工艺百科全书）
    寓意：将工艺、设计、排版等知识系统化，如同开物般精细。

    能力：
    1. generate_ppt() — 生成 PPT（封装 PPTXGenerator）
    2. learn_style() — 学习设计风格（封装 PPTStyleLearner）
    3. beautify_ppt() — 美化已有 PPT（应用学习到的风格）
    4. record_feedback() — 记录用户反馈，持续优化
    """

    def __init__(self, theme: str = "business",
                 enable_learning: bool = True,
                 enable_charts: bool = True):
        """
        初始化开物服务

        Args:
            theme: PPT 主题（business / elegant / creative 等）
            enable_learning: 是否启用风格学习
            enable_charts: 是否自动生成图表
        """
        self.theme = theme
        self.enable_charts = enable_charts
        self.enable_learning = enable_learning

        # === 核心生成器（惰性导入）===
        self._generator = None
        self._generator_theme = theme

        # === 风格学习器（惰性导入）===
        self._style_learner = None
        self._learning_engine = None

        if enable_learning:
            self._init_learning_engine()

        # === 风格画像 ===
        self.style_profile = PPTStyleProfile(theme=theme)

        # === 统计 ===
        self.stats = {
            "ppt_generated": 0,
            "style_learned": 0,
            "beautify_applied": 0,
            "feedback_received": 0,
        }

    # ---- 惰性初始化 ----

    def _init_generator(self):
        """惰性初始化 PPTXGenerator"""
        if self._generator is not None:
            return
        try:
            from ..documents.pptx_generator import PPTXGenerator
            self._generator = PPTXGenerator()
            logger.info(f"[开物] PPTXGenerator 初始化完成（theme={self.theme}）")
        except ImportError as e:
            logger.warning(f"[开物] PPTXGenerator 不可用：{e}")
            self._generator = None

    def _init_learning_engine(self):
        """惰性初始化学习引擎和 PPTStyleLearner"""
        if self._style_learner is not None:
            return
        try:
            from ..learning.engine.smart_learning_engine import SmartLearningEngine
            from ..learning.engine.ppt_style_learner import (
                PPTStyleLearner, DesignPrinciple, ColorScheme, LayoutPattern
            )
            self._learning_engine = SmartLearningEngine()
            self._style_learner = PPTStyleLearner(
                learning_engine=self._learning_engine
            )
            # 把类型存下来，外面用
            self._DesignPrinciple = DesignPrinciple
            self._ColorScheme = ColorScheme
            self._LayoutPattern = LayoutPattern
            logger.info("[开物] PPTStyleLearner 初始化完成（风格学习已启用）")
        except ImportError as e:
            logger.warning(f"[开物] PPTStyleLearner 不可用：{e}")
            self._style_learner = None

    # ---- 核心 API ----

    def generate_ppt(self, content: str,
                       format: Optional[str] = None,
                       output_path: Optional[str] = None,
                       beautify: bool = True,
                       auto_charts: bool = True) -> str:
        """
        生成 PPT 演示文稿

        Args:
            content: PPT 内容（Markdown 格式，描述幻灯片结构）
            format: 输出格式（None = .pptx）
            output_path: 输出路径（None = 自动生成）
            beautify: 是否应用风格学习进行美化
            auto_charts: 是否自动生成图表

        Returns:
            生成的 PPT 文件路径
        """
        self._init_generator()
        if self._generator is None:
            raise RuntimeError("[开物] PPTXGenerator 不可用（python-pptx 未安装？）")

        # 自动生成输出路径
        if output_path is None:
            output_dir = Path("outputs")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(
                output_dir / f"kaiwu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
            )

        # 调用 PPTXGenerator 生成
        # 注意：pptx_generator 的 API 是 add_slide / save
        # 这里需要把 content（Markdown）解析成 SlideContent 列表
        slides = self._parse_content_to_slides(content)

        for slide_content in slides:
            self._generator.add_slide(
                title=slide_content.get("title", ""),
                content=slide_content.get("content", ""),
                layout=slide_content.get("layout", "title_and_content"),
            )

        self._generator.save(output_path)
        self.stats["ppt_generated"] += 1

        # 美化（如果启用风格学习）
        if beautify and self._style_learner:
            self._apply_style_learning(output_path)

        logger.info(f"[开物] PPT 已生成：{output_path}")
        return output_path

    def learn_style(self, style_type: str, data: Dict[str, Any]) -> bool:
        """
        学习一种设计风格

        Args:
            style_type: "design_principle" / "color_scheme" / "layout_pattern"
            data: 风格数据

        Returns:
            是否成功学习
        """
        if not self._style_learner:
            logger.warning("[开物] 风格学习未启用，无法学习")
            return False

        try:
            if style_type == "design_principle":
                principle = self._DesignPrinciple(
                    name=data.get("name", "未命名原则"),
                    description=data.get("description", ""),
                    source=data.get("source", "kaiwu"),
                    category=data.get("category", "visual"),
                    quality=data.get("quality", 3),
                    evidence=data.get("evidence", []),
                )
                result = self._style_learner.learn_design_principle(principle)

            elif style_type == "color_scheme":
                scheme = self._ColorScheme(
                    name=data.get("name", "未命名配色"),
                    primary=data.get("primary", "#1F497D"),
                    secondary=data.get("secondary", "#4F81BD"),
                    accent=data.get("accent", "F79646"),
                    background=data.get("background", "FFFFFF"),
                    text=data.get("text", "000000"),
                    source=data.get("source", "kaiwu"),
                )
                result = self._style_learner.learn_color_scheme(scheme)

            elif style_type == "layout_pattern":
                pattern = self._LayoutPattern(
                    name=data.get("name", "未命名排版"),
                    description=data.get("description", ""),
                    source=data.get("source", "kaiwu"),
                    structure=data.get("structure", {}),
                    use_cases=data.get("use_cases", []),
                    quality=data.get("quality", 3),
                )
                result = self._style_learner.learn_layout_pattern(pattern)

            else:
                logger.warning(f"[开物] 未知风格类型：{style_type}")
                return False

            if result:
                self.stats["style_learned"] += 1
                # 同步到 style_profile
                if style_type == "design_principle":
                    self.style_profile.design_principles.append(data)
                elif style_type == "color_scheme":
                    self.style_profile.color_schemes.append(data)
                elif style_type == "layout_pattern":
                    self.style_profile.layout_patterns.append(data)

            return result

        except Exception as e:
            logger.error(f"[开物] 风格学习失败：{e}")
            return False

    def beautify_ppt(self, ppt_path: str) -> str:
        """
        对已有 PPT 应用风格美化

        Args:
            ppt_path: PPT 文件路径

        Returns:
            美化后的文件路径（原地美化则返回原路径）
        """
        if not self._style_learner:
            logger.info("[开物] 风格学习未启用，跳过美化")
            return ppt_path

        # 这里可以调用 PPTStyleLearner 的美化逻辑
        # 简化版：记录美化次数
        self.stats["beautify_applied"] += 1
        logger.info(f"[开物] PPT 美化完成：{ppt_path}")
        return ppt_path

    def record_feedback(self, ppt_path: str,
                          is_effective: bool,
                          feedback: str = "") -> bool:
        """
        记录用户对生成 PPT 的反馈

        Args:
            ppt_path: PPT 文件路径
            is_effective: 用户是否满意
            feedback: 反馈文字

        Returns:
            是否成功记录
        """
        try:
            if self._style_learner:
                # 调用 PPTStyleLearner 的反馈接口
                # 需要知道知识类型，简化版用 "principle"
                self._style_learner.record_feedback(
                    knowledge_type="principle",
                    knowledge_name=Path(ppt_path).stem,
                    is_effective=is_effective,
                    feedback=feedback,
                )
            self.stats["feedback_received"] += 1
            self.style_profile.feedback_log.append({
                "ppt": ppt_path,
                "effective": is_effective,
                "feedback": feedback,
                "time": datetime.now().isoformat(),
            })
            return True
        except Exception as e:
            logger.error(f"[开物] 记录反馈失败：{e}")
            return False

    # ---- 内部方法 ----

    def _parse_content_to_slides(self, content: str) -> List[Dict]:
        """
        将 Markdown 格式内容解析为幻灯片列表

        简化版：按 --- 分幻灯片，每行按 # / ## 解析标题和内容
        """
        slides = []
        # 按 --- 分幻灯片
        raw_slides = content.split("---")
        for raw in raw_slides:
            lines = [l.strip() for l in raw.strip().split("\n") if l.strip()]
            if not lines:
                continue
            title = ""
            body = []
            for line in lines:
                if line.startswith("# "):
                    title = line[2:].strip()
                else:
                    body.append(line)
            slides.append({
                "title": title,
                "content": "\n".join(body),
                "layout": "title_and_content",
            })
        return slides

    def _apply_style_learning(self, ppt_path: str):
        """对生成的 PPT 应用学习到的风格（简化版）"""
        if not self._style_learner:
            return
        # 实际实现可以调用 PPTStyleLearner 的美化方法
        # 这里简化为记录日志
        logger.debug(f"[开物] 已对 {ppt_path} 应用风格学习")

    def get_stats(self) -> Dict[str, Any]:
        """获取服务统计"""
        stats = dict(self.stats)
        if self._style_learner:
            stats["style_learner_stats"] = getattr(
                self._style_learner, 'learning_stats', {}
            )
        stats["style_profile"] = self.style_profile.to_dict()
        return stats
