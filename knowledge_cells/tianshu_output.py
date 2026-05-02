# -*- coding: utf-8 -*-
"""
tianshu_output.py v1.0.0
======================================
天枢输出层 — 第10个子系统

集成 Report Engine 和 Slide Forge 的有价值内容：
1. 报告生成（ReportSection、Report、to_markdown、to_html）
2. 幻灯片生成（PPTContentGenerator、PPTBeautifier、PPTService）
3. 图表生成（ChartGenerator、ColorMatrixGenerator）

定位：天枢输出层（TianShu Output Layer）
- 作为 TianShu 的输出层，按需调用
- 支持多格式输出（Markdown、HTML、PPTX、图表）
- 接入九大子系统，作为输出终端

Version: 1.0.0
Created: 2026-05-01
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

logger = logging.getLogger("Somn.TianShuOutput")

# ============ 路径设置 ============
_project_root = Path(__file__).resolve().parent.parent
_src_path = _project_root / "smart_office_assistant" / "src"
if str(_src_path) not in sys.path:
    sys.path.append(str(_src_path))

# ============ 类型定义 ============

class OutputFormat(Enum):
    """输出格式"""
    MARKDOWN = "markdown"
    HTML = "html"
    PPTX = "pptx"
    CHART = "chart"
    JSON = "json"

class ReportType(Enum):
    """报告类型"""
    ANALYSIS = "analysis"           # 分析报告
    STRATEGY = "strategy"           # 策略报告
    PERFORMANCE = "performance"     # 性能报告
    LEARNING = "learning"           # 学习报告
    COMPARISON = "comparison"       # 比较报告
    TREND = "trend"               # 趋势报告

class ChartType(Enum):
    """图表类型"""
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    HEATMAP = "heatmap"
    RADAR = "radar"

@dataclass
class ReportSection:
    """报告章节（提炼自 report_engine/report_generator.py）"""
    title: str
    content: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    charts: List[Dict] = field(default_factory=list)
    level: int = 1
    subsections: List['ReportSection'] = field(default_factory=list)

@dataclass
class ReportSpec:
    """报告规格"""
    id: str
    title: str
    description: str
    report_type: ReportType
    format: OutputFormat
    sections: List[ReportSection] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

@dataclass
class SlideSpec:
    """幻灯片规格（提炼自 slide_forge/）"""
    title: str
    subtitle: str = ""
    slides: List[Dict[str, Any]] = field(default_factory=list)
    style: str = "professional"  # professional, creative, minimal
    color_scheme: str = "blue"

@dataclass
class ChartSpec:
    """图表规格（提炼自 slide_forge/chart_generator.py）"""
    title: str
    chart_type: ChartType
    data: List[Dict[str, Any]]
    x_label: str = ""
    y_label: str = ""
    color_scheme: str = "default"

@dataclass
class OutputResult:
    """输出结果"""
    output_id: str
    output_type: OutputFormat
    content: str  # 文件路径或文本内容
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

# ============ 核心类 ============

class TianShuOutput:
    """
    天枢输出层 — 第10个子系统
    
    功能：
    1. 报告生成（多格式：Markdown、HTML、JSON）
    2. 幻灯片生成（PPTX，支持美化）
    3. 图表生成（柱状图、折线图、饼图等）
    4. 输出管理（版本控制、格式转换）
    
    接入：
    - 作为 TianShu 的输出层，按需调用
    - 九大子系统可调用本系统生成输出
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "outputs"
        self.output_dir.mkdir(exist_ok=True)
        
        self.report_engine = None   # 报告生成引擎（懒加载）
        self.slide_engine = None    # 幻灯片生成引擎（懒加载）
        self.chart_engine = None    # 图表生成引擎（懒加载）
        
        self.generation_history: List[OutputResult] = []
        self.logger = logging.getLogger("Somn.TianShuOutput")
        self.logger.info("[TianShuOutput] v1.0.0 初始化完成")
    
    def _load_report_engine(self):
        """懒加载报告生成引擎"""
        if self.report_engine is not None:
            return
        
        try:
            from report_engine.report_generator import create_report_engine
            self.report_engine = create_report_engine()
            self.logger.info("[TianShuOutput] 报告生成引擎加载完成")
        except ImportError as e:
            self.logger.warning(f"[TianShuOutput] 报告生成引擎加载失败: {e}")
            self.report_engine = None
    
    def _load_slide_engine(self):
        """懒加载幻灯片生成引擎"""
        if self.slide_engine is not None:
            return
        
        try:
            from slide_forge.ppt_service import PPTService
            self.slide_engine = PPTService()
            self.logger.info("[TianShuOutput] 幻灯片生成引擎加载完成")
        except ImportError as e:
            self.logger.warning(f"[TianShuOutput] 幻灯片生成引擎加载失败: {e}")
            self.slide_engine = None
    
    def _load_chart_engine(self):
        """懒加载图表生成引擎"""
        if self.chart_engine is not None:
            return
        
        try:
            from slide_forge.chart_generator import ChartGenerator
            self.chart_engine = ChartGenerator()
            self.logger.info("[TianShuOutput] 图表生成引擎加载完成")
        except ImportError as e:
            self.logger.warning(f"[TianShuOutput] 图表生成引擎加载失败: {e}")
            self.chart_engine = None
    
    def generate_report(self, spec: ReportSpec) -> OutputResult:
        """
        生成报告
        
        Args:
            spec: 报告规格
        
        Returns:
            OutputResult 输出结果
        """
        self._load_report_engine()
        
        if self.report_engine is None:
            # 降级：生成 Markdown 报告
            return self._generate_markdown_report(spec)
        
        try:
            report = self.report_engine.create_report(spec)
            
            if spec.format == OutputFormat.MARKDOWN:
                content = report.to_markdown()
                output_path = self.output_dir / f"{spec.id}.md"
                output_path.write_text(content, encoding='utf-8')
            elif spec.format == OutputFormat.HTML:
                content = report.to_html()
                output_path = self.output_dir / f"{spec.id}.html"
                output_path.write_text(content, encoding='utf-8')
            else:
                content = json.dumps(asdict(report), ensure_ascii=False, indent=2)
                output_path = self.output_dir / f"{spec.id}.json"
                output_path.write_text(content, encoding='utf-8')
            
            result = OutputResult(
                output_id=spec.id,
                output_type=spec.format,
                content=str(output_path),
            )
            self.generation_history.append(result)
            return result
        except Exception as e:
            self.logger.error(f"[TianShuOutput] 生成报告失败: {e}")
            return self._generate_markdown_report(spec)
    
    def _generate_markdown_report(self, spec: ReportSpec) -> OutputResult:
        """降级：生成 Markdown 报告"""
        lines = [
            f"# {spec.title}",
            "",
            f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"> 描述: {spec.description}",
            "",            "---",            "",        ]
        
        for section in spec.sections:
            lines.extend(self._section_to_markdown(section))
        
        content = "\n".join(lines)
        output_path = self.output_dir / f"{spec.id}.md"
        output_path.write_text(content, encoding='utf-8')
        
        result = OutputResult(
            output_id=spec.id,
            output_type=OutputFormat.MARKDOWN,
            content=str(output_path),
        )
        self.generation_history.append(result)
        return result
    
    def _section_to_markdown(self, section: ReportSection, level: int = 1) -> List[str]:
        """章节转 Markdown"""
        lines = []
        header = "#" * level
        lines.append(f"{header} {section.title}")
        lines.append("")
        lines.append(section.content)
        lines.append("")
        
        for subsection in section.subsections:
            lines.extend(self._section_to_markdown(subsection, level + 1))
        
        return lines
    
    def generate_slides(self, spec: SlideSpec) -> OutputResult:
        """
        生成幻灯片
        
        Args:
            spec: 幻灯片规格
        
        Returns:
            OutputResult 输出结果
        """
        self._load_slide_engine()
        
        if self.slide_engine is None:
            # 降级：生成 Markdown 幻灯片
            return self._generate_markdown_slides(spec)
        
        try:
            presentation = self.slide_engine.generate(spec)
            output_path = self.output_dir / f"{spec.title}.pptx"
            presentation.save(output_path)
            
            result = OutputResult(
                output_id=spec.title,
                output_type=OutputFormat.PPTX,
                content=str(output_path),
            )
            self.generation_history.append(result)
            return result
        except Exception as e:
            self.logger.error(f"[TianShuOutput] 生成幻灯片失败: {e}")
            return self._generate_markdown_slides(spec)
    
    def _generate_markdown_slides(self, spec: SlideSpec) -> OutputResult:
        """降级：生成 Markdown 幻灯片"""
        lines = [
            f"# {spec.title}",
            "",
            f"> {spec.subtitle}" if spec.subtitle else "",
            "",            "---",            "",        ]
        
        for i, slide in enumerate(spec.slides, 1):
            lines.append(f"## 第{i}页: {slide.get('title', '')}")
            lines.append("")
            lines.append(slide.get('content', ''))
            lines.append("")
            lines.append("---")
            lines.append("")
        
        content = "\n".join(lines)
        output_path = self.output_dir / f"{spec.title}.md"
        output_path.write_text(content, encoding='utf-8')
        
        result = OutputResult(
            output_id=spec.title,
            output_type=OutputFormat.MARKDOWN,
            content=str(output_path),
        )
        self.generation_history.append(result)
        return result
    
    def generate_chart(self, spec: ChartSpec) -> OutputResult:
        """
        生成图表
        
        Args:
            spec: 图表规格
        
        Returns:
            OutputResult 输出结果
        """
        self._load_chart_engine()
        
        if self.chart_engine is None:
            # 降级：生成文本描述
            return self._generate_text_chart(spec)
        
        try:
            chart = self.chart_engine.generate(spec)
            output_path = self.output_dir / f"{spec.title}.png"
            chart.save(output_path)
            
            result = OutputResult(
                output_id=spec.title,
                output_type=OutputFormat.CHART,
                content=str(output_path),
            )
            self.generation_history.append(result)
            return result
        except Exception as e:
            self.logger.error(f"[TianShuOutput] 生成图表失败: {e}")
            return self._generate_text_chart(spec)
    
    def _generate_text_chart(self, spec: ChartSpec) -> OutputResult:
        """降级：生成文本图表"""
        lines = [
            f"# {spec.title}",
            "",
            f"类型: {spec.chart_type.value}",
            f"X轴: {spec.x_label}",
            f"Y轴: {spec.y_label}",
            "",            "数据:",        ]
        
        for item in spec.data:
            lines.append(f"  - {item.get('label', '')}: {item.get('value', '')}")
        
        content = "\n".join(lines)
        output_path = self.output_dir / f"{spec.title}.txt"
        output_path.write_text(content, encoding='utf-8')
        
        result = OutputResult(
            output_id=spec.title,
            output_type=OutputFormat.CHART,
            content=str(output_path),
        )
        self.generation_history.append(result)
        return result
    
    def get_generation_history(self, limit: int = 10) -> List[OutputResult]:
        """获取生成历史"""
        return self.generation_history[-limit:]
    
    def clear_history(self):
        """清空生成历史"""
        self.generation_history.clear()
        self.logger.info("[TianShuOutput] 生成历史已清空")

# ============ 接口函数 ============

# 全局单例
_TIANSHU_OUTPUT: Optional[TianShuOutput] = None

def get_tianshu_output() -> TianShuOutput:
    """获取 TianShuOutput 单例"""
    global _TIANSHU_OUTPUT
    if _TIANSHU_OUTPUT is None:
        _TIANSHU_OUTPUT = TianShuOutput()
    return _TIANSHU_OUTPUT

def generate_report(report_type: str, title: str, sections: List[Dict], output_format: str = "markdown") -> Dict[str, Any]:
    """
    生成报告（便捷函数）
    
    Args:
        report_type: 报告类型（analysis/strategy/performance/learning/comparison/trend）
        title: 报告标题
        sections: 章节列表 [{"title": ..., "content": ...}]
        output_format: 输出格式（markdown/html/json）
    
    Returns:
        生成结果 {"output_id": ..., "output_type": ..., "content": ...}
    """
    tso = get_tianshu_output()
    
    # 构建 ReportSpec
    spec = ReportSpec(
        id=title.replace(' ', '_').lower(),
        title=title,
        description=f"{report_type} 报告",
        report_type=ReportType(report_type),
        format=OutputFormat(output_format),
    )
    
    # 构建章节
    for sec in sections:
        section = ReportSection(
            title=sec.get('title', ''),
            content=sec.get('content', ''),
            level=1,
        )
        spec.sections.append(section)
    
    result = tso.generate_report(spec)
    return asdict(result)

def generate_slides(title: str, slides: List[Dict], style: str = "professional") -> Dict[str, Any]:
    """
    生成幻灯片（便捷函数）
    
    Args:
        title: 幻灯片标题
        slides: 幻灯片列表 [{"title": ..., "content": ...}]
        style: 风格（professional/creative/minimal）
    
    Returns:
        生成结果
    """
    tso = get_tianshu_output()
    
    spec = SlideSpec(
        title=title,
        style=style,
    )
    
    for slide in slides:
        spec.slides.append(slide)
    
    result = tso.generate_slides(spec)
    return asdict(result)

def generate_chart(title: str, chart_type: str, data: List[Dict], x_label: str = "", y_label: str = "") -> Dict[str, Any]:
    """
    生成图表（便捷函数）
    
    Args:
        title: 图表标题
        chart_type: 图表类型（bar/line/pie/scatter/heatmap/radar）
        data: 数据列表 [{"label": ..., "value": ...}]
        x_label: X轴标签
        y_label: Y轴标签
    
    Returns:
        生成结果
    """
    tso = get_tianshu_output()
    
    spec = ChartSpec(
        title=title,
        chart_type=ChartType(chart_type),
        data=data,
        x_label=x_label,
        y_label=y_label,
    )
    
    result = tso.generate_chart(spec)
    return asdict(result)

# ============ 导出 ============

__version__ = "1.0.0"
__all__ = [
    "TianShuOutput",
    "OutputFormat",
    "ReportType",
    "ChartType",
    "ReportSection",
    "ReportSpec",
    "SlideSpec",
    "ChartSpec",
    "OutputResult",
    "get_tianshu_output",
    "generate_report",
    "generate_slides",
    "generate_chart",
]

logger.info(f"[TianShuOutput] v{__version__} 加载完成")
