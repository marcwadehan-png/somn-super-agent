"""
__all__ = [
    'add_bullet_list',
    'add_heading',
    'add_image',
    'add_numbered_list',
    'add_page_break',
    'add_paragraph',
    'add_spacer',
    'add_table',
    'add_title',
    'build_report',
    'create_analysis_report',
    'create_cover_page',
    'create_meeting_summary',
    'create_toc',
    'save',
]

PDF 报告generate器 - PDF Generator
基于 ReportLab 的 PDF generate功能
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, ListFlowable, ListItem, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from loguru import logger

@dataclass
class PDFSection:
    """PDF 章节"""
    title: str
    content: Union[str, List[str], List[Dict[str, Any]]]
    level: int = 1

@dataclass
class PDFTable:
    """PDF 表格"""
    data: List[List[str]]
    col_widths: Optional[List[float]] = None
    style: Optional[TableStyle] = None

class PDFGenerator:
    """
    PDF 报告generate器
    
    功能:
    - 创建专业 PDF 文档
    - 支持文字,表格,图片
    - 自定义样式和布局
    - 页眉页脚
    - 目录generate
    """
    
    def __init__(
        self,
        title: str = "",
        author: str = "",
        page_size: Tuple[float, float] = A4
    ):
        """
        initgenerate器
        
        Args:
            title: 文档标题
            author: 作者
            page_size: 页面尺寸
        """
        self.title = title
        self.author = author
        self.page_size = page_size
        
        # 内容元素列表
        self.elements: List[Any] = []
        
        # 样式
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # 尝试注册中文字体
        self._register_chinese_fonts()
    
    def _register_chinese_fonts(self):
        """注册中文字体"""
        try:
            # 尝试注册常见中文字体
            from src.core.paths import FONT_MS_YAHEI, FONT_SIMHEI, FONT_SIMSUN
            font_paths = [
                str(FONT_MS_YAHEI),  # 微软雅黑
                str(FONT_SIMHEI),    # 黑体
                str(FONT_SIMSUN),    # 宋体
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # Linux 文泉驿
                "/System/Library/Fonts/PingFang.ttc",  # macOS 苹方
            ]
            
            for font_path in font_paths:
                if Path(font_path).exists():
                    try:
                        pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                        self.chinese_font = 'ChineseFont'
                        logger.info(f"注册中文字体: {font_path}")
                        return
                    except (OSError, IOError, PermissionError):
                        continue
            
            # 如果没有找到中文字体,使用默认字体
            self.chinese_font = 'Helvetica'
            logger.warning("未找到中文字体,使用默认字体")
            
        except Exception as e:
            self.chinese_font = 'Helvetica'
            logger.error(f"字体注册失败: {e}")
    
    def _setup_custom_styles(self):
        """设置自定义样式"""
        # 标题样式
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2C3E50')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.HexColor('#34495E'),
            borderPadding=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=10,
            textColor=colors.HexColor('#34495E')
        ))
        
        # 正文样式
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=18,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # 页眉样式
        self.styles.add(ParagraphStyle(
            name='Header',
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_RIGHT
        ))
        
        # 页脚样式
        self.styles.add(ParagraphStyle(
            name='Footer',
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))
    
    def add_title(self, title: str, subtitle: str = ""):
        """
        添加标题
        
        Args:
            title: 主标题
            subtitle: 副标题
        """
        self.elements.append(Spacer(1, 2*inch))
        
        title_para = Paragraph(title, self.styles['CustomTitle'])
        self.elements.append(title_para)
        
        if subtitle:
            self.elements.append(Spacer(1, 0.3*inch))
            subtitle_style = ParagraphStyle(
                name='Subtitle',
                parent=self.styles['Normal'],
                fontSize=14,
                alignment=TA_CENTER,
                textColor=colors.grey
            )
            subtitle_para = Paragraph(subtitle, subtitle_style)
            self.elements.append(subtitle_para)
        
        self.elements.append(Spacer(1, 1*inch))
    
    def add_heading(self, text: str, level: int = 1):
        """
        添加章节标题
        
        Args:
            text: 标题文本
            level: 标题级别 1-3
        """
        style_name = f'CustomHeading{level}'
        if style_name not in self.styles:
            style_name = 'CustomHeading1'
        
        heading = Paragraph(text, self.styles[style_name])
        self.elements.append(heading)
        self.elements.append(Spacer(1, 0.1*inch))
    
    def add_paragraph(self, text: str, style: Optional[str] = None):
        """
        添加段落
        
        Args:
            text: 段落文本
            style: 样式名称
        """
        style_name = style or 'CustomBody'
        if style_name not in self.styles:
            style_name = 'Normal'
        
        # 处理换行
        text = text.replace('\n', '<br/>')
        
        para = Paragraph(text, self.styles[style_name])
        self.elements.append(para)
        self.elements.append(Spacer(1, 0.1*inch))
    
    def add_bullet_list(self, items: List[str], bullet_char: str = "•"):
        """
        添加项目符号列表
        
        Args:
            items: 列表项
            bullet_char: 项目符号
        """
        bullet_style = ParagraphStyle(
            name='Bullet',
            parent=self.styles['CustomBody'],
            leftIndent=20,
            bulletIndent=10,
            bulletFontName=self.chinese_font
        )
        
        for item in items:
            para = Paragraph(f"{bullet_char} {item}", bullet_style)
            self.elements.append(para)
        
        self.elements.append(Spacer(1, 0.1*inch))
    
    def add_numbered_list(self, items: List[str]):
        """
        添加编号列表
        
        Args:
            items: 列表项
        """
        numbered_style = ParagraphStyle(
            name='Numbered',
            parent=self.styles['CustomBody'],
            leftIndent=20
        )
        
        for i, item in enumerate(items, 1):
            para = Paragraph(f"{i}. {item}", numbered_style)
            self.elements.append(para)
        
        self.elements.append(Spacer(1, 0.1*inch))
    
    def add_table(
        self,
        data: List[List[str]],
        col_widths: Optional[List[float]] = None,
        header_style: bool = True
    ):
        """
        添加表格
        
        Args:
            data: 表格数据
            col_widths: 列宽列表
            header_style: 是否使用表头样式
        """
        if not data:
            return
        
        # 创建表格
        table = Table(data, colWidths=col_widths, repeatRows=1 if header_style else 0)
        
        # 设置样式
        style_commands = [
            ('FONTNAME', (0, 0), (-1, -1), self.chinese_font),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ]
        
        if header_style:
            style_commands.extend([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), self.chinese_font),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ])
        
        table.setStyle(TableStyle(style_commands))
        
        self.elements.append(table)
        self.elements.append(Spacer(1, 0.2*inch))
    
    def add_image(
        self,
        image_path: str,
        width: Optional[float] = None,
        height: Optional[float] = None,
        caption: str = ""
    ):
        """
        添加图片
        
        Args:
            image_path: 图片路径
            width: 宽度
            height: 高度
            caption: 图片说明
        """
        if not Path(image_path).exists():
            logger.warning(f"图片不存在: {image_path}")
            return
        
        img = Image(image_path)
        
        # 调整尺寸
        if width:
            img.drawWidth = width
        if height:
            img.drawHeight = height
        
        self.elements.append(img)
        
        if caption:
            caption_style = ParagraphStyle(
                name='Caption',
                parent=self.styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                textColor=colors.grey,
                spaceBefore=5
            )
            self.elements.append(Paragraph(caption, caption_style))
        
        self.elements.append(Spacer(1, 0.2*inch))
    
    def add_page_break(self):
        """添加分页符"""
        self.elements.append(PageBreak())
    
    def add_spacer(self, height: float):
        """添加空白间距"""
        self.elements.append(Spacer(1, height))
    
    def create_cover_page(
        self,
        title: str,
        subtitle: str = "",
        author: str = "",
        date: str = ""
    ):
        """创建封面"""
        self.add_title(title, subtitle)
        
        if author:
            author_style = ParagraphStyle(
                name='CoverAuthor',
                parent=self.styles['Normal'],
                fontSize=12,
                alignment=TA_CENTER,
                spaceBefore=20
            )
            self.elements.append(Paragraph(f"作者: {author}", author_style))
        
        if date:
            date_style = ParagraphStyle(
                name='CoverDate',
                parent=self.styles['Normal'],
                fontSize=11,
                alignment=TA_CENTER,
                textColor=colors.grey,
                spaceBefore=10
            )
            self.elements.append(Paragraph(date, date_style))
        
        self.add_page_break()
    
    def create_toc(self, sections: List[str]):
        """
        创建目录
        
        Args:
            sections: 章节标题列表
        """
        self.add_heading("目录", level=1)
        
        toc_style = ParagraphStyle(
            name='TOC',
            parent=self.styles['CustomBody'],
            leftIndent=20,
            spaceAfter=5
        )
        
        for i, section in enumerate(sections, 1):
            self.elements.append(Paragraph(f"{i}. {section}", toc_style))
        
        self.add_page_break()
    
    def build_report(
        self,
        sections: List[PDFSection],
        include_toc: bool = True
    ):
        """
        构建完整报告
        
        Args:
            sections: 章节列表
            include_toc: 是否包含目录
        """
        # 目录
        if include_toc:
            section_titles = [s.title for s in sections]
            self.create_toc(section_titles)
        
        # 章节内容
        for section in sections:
            self.add_heading(section.title, level=section.level)
            
            if isinstance(section.content, str):
                self.add_paragraph(section.content)
            elif isinstance(section.content, list):
                for item in section.content:
                    if isinstance(item, str):
                        self.add_paragraph(item)
                    elif isinstance(item, dict):
                        # 处理结构化内容
                        if item.get('type') == 'list':
                            self.add_bullet_list(item.get('items', []))
                        elif item.get('type') == 'numbered_list':
                            self.add_numbered_list(item.get('items', []))
                        elif item.get('type') == 'table':
                            self.add_table(item.get('data', []))
    
    def save(self, output_path: str) -> str:
        """
        保存 PDF 文档
        
        Args:
            output_path: 输出路径
        
        Returns:
            保存的文件路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建文档
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=self.page_size,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # 构建文档
        doc.build(self.elements)
        
        logger.info(f"PDF 已保存: {output_path}")
        return str(output_path)

# 预设模板
class PDFTemplates:
    """PDF 文档模板"""
    
    @staticmethod
    def create_analysis_report(
        title: str,
        summary: str,
        findings: List[Dict[str, Any]],
        recommendations: List[str],
        output_path: str
    ) -> str:
        """创建分析报告"""
        gen = PDFGenerator(title=title)
        
        # 封面
        gen.create_cover_page(
            title=title,
            subtitle="数据分析报告",
            date=datetime.now().strftime("%Y年%m月%d日")
        )
        
        # 执行摘要
        gen.add_heading("执行摘要", level=1)
        gen.add_paragraph(summary)
        
        # 主要发现
        gen.add_heading("主要发现", level=1)
        for finding in findings:
            gen.add_heading(finding.get('title', ''), level=2)
            gen.add_paragraph(finding.get('description', ''))
            
            if 'data' in finding:
                gen.add_table(finding['data'])
        
        # 建议
        gen.add_heading("建议", level=1)
        gen.add_numbered_list(recommendations)
        
        return gen.save(output_path)
    
    @staticmethod
    def create_meeting_summary(
        meeting_title: str,
        date: str,
        attendees: List[str],
        key_points: List[str],
        decisions: List[str],
        action_items: List[Dict[str, str]],
        output_path: str
    ) -> str:
        """创建会议纪要"""
        gen = PDFGenerator(title=meeting_title)
        
        # 封面
        gen.create_cover_page(
            title=meeting_title,
            subtitle="会议纪要",
            date=date
        )
        
        # 基本信息
        gen.add_heading("会议信息", level=1)
        info_data = [
            ["会议主题", meeting_title],
            ["日期", date],
            ["参会人员", ", ".join(attendees)]
        ]
        gen.add_table(info_data, col_widths=[100, 350], header_style=False)
        
        # 要点
        gen.add_heading("会议要点", level=1)
        gen.add_bullet_list(key_points)
        
        # 决议
        gen.add_heading("决议事项", level=1)
        gen.add_numbered_list(decisions)
        
        # action项
        gen.add_heading("action项", level=1)
        action_data = [["事项", "负责人", "截止日期"]]
        action_data.extend([
            [item.get('task', ''), item.get('owner', ''), item.get('deadline', '')]
            for item in action_items
        ])
        gen.add_table(action_data)
        
        return gen.save(output_path)
