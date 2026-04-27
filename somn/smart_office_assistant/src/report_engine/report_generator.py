"""
__all__ = [
    'add_analysis_section',
    'add_comparison_section',
    'add_overview_section',
    'add_section',
    'add_trend_section',
    'create_report',
    'create_report_engine',
    'export_report',
    'generate_learning_report',
    'generate_performance_report',
    'generate_strategy_report',
    'list_reports',
    'to_html',
    'to_markdown',
]

报告generate器 - 从abyss AI迁移
功能:多格式报告generate,数据整合,可视化
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

@dataclass
class ReportSection:
    """报告章节"""
    title: str
    content: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    charts: List[Dict] = field(default_factory=list)
    level: int = 1
    subsections: List['ReportSection'] = field(default_factory=list)

@dataclass
class Report:
    """报告定义"""
    id: str
    title: str
    description: str
    sections: List[ReportSection] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    format_type: str = "markdown"  # markdown, html, json
    
    def add_section(self, section: ReportSection):
        """添加章节"""
        self.sections.append(section)
    
    def to_markdown(self) -> str:
        """转换为Markdown"""
        lines = [
            f"# {self.title}",
            f"",
            f"> generate时间: {self.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"> 描述: {self.description}",
            f"",
            "---",
            f""
        ]
        
        for section in self.sections:
            lines.extend(self._section_to_markdown(section))
        
        return "\n".join(lines)
    
    def _section_to_markdown(self, section: ReportSection, prefix: str = "") -> List[str]:
        """章节转Markdown"""
        lines = []
        
        # 标题
        header = "#" * section.level
        lines.append(f"{header} {section.title}")
        lines.append("")
        
        # 内容
        if section.content:
            lines.append(section.content)
            lines.append("")
        
        # 数据表格
        if section.data:
            lines.append("### 数据概览")
            lines.append("")
            for key, value in section.data.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
        
        # 子章节
        for sub in section.subsections:
            lines.extend(self._section_to_markdown(sub))
        
        return lines
    
    def to_html(self) -> str:
        """转换为HTML"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #1a1a1a; border-bottom: 2px solid #0066cc; padding-bottom: 10px; }}
        h2 {{ color: #333; margin-top: 30px; }}
        h3 {{ color: #555; }}
        .meta {{ color: #666; font-size: 14px; margin: 20px 0; }}
        .section {{ margin: 20px 0; padding: 15px; background: #f9f9f9; border-radius: 8px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background: #0066cc; color: white; }}
        tr:nth-child(even) {{ background: #f2f2f2; }}
        .metric {{ display: inline-block; margin: 10px; padding: 15px; background: #e8f4f8; border-radius: 8px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #0066cc; }}
        .metric-label {{ font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <h1>{self.title}</h1>
    <div class="meta">
        <p>generate时间: {self.created_at.strftime('%Y-%m-%d %H:%M')}</p>
        <p>{self.description}</p>
    </div>
"""
        
        for section in self.sections:
            html += self._section_to_html(section)
        
        html += "</body></html>"
        return html
    
    def _section_to_html(self, section: ReportSection) -> str:
        """章节转HTML"""
        html = f'<div class="section">\n'
        html += f'<h{section.level}>{section.title}</h{section.level}>\n'
        
        if section.content:
            html += f'<p>{section.content}</p>\n'
        
        if section.data:
            html += '<div class="data-section">\n'
            for key, value in section.data.items():
                html += f'<div class="metric">\n'
                html += f'<div class="metric-value">{value}</div>\n'
                html += f'<div class="metric-label">{key}</div>\n'
                html += f'</div>\n'
            html += '</div>\n'
        
        for sub in section.subsections:
            html += self._section_to_html(sub)
        
        html += '</div>\n'
        return html

class ReportEngine:
    """报告引擎 - unified报告generate和管理"""
    
    def __init__(self, output_dir: str = "./reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.reports: Dict[str, Report] = {}
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Any]:
        """加载报告模板"""
        return {
            'performance': {
                'title': '性能分析报告',
                'sections': ['概览', '关键metrics', '趋势分析', '问题诊断', '优化建议']
            },
            'strategy': {
                'title': 'strategy执行报告',
                'sections': ['执行摘要', '目标达成', 'strategy效果', '资源使用', '下一步计划']
            },
            'learning': {
                'title': '学习进度报告',
                'sections': ['学习概览', '知识掌握', '进度追踪', '薄弱环节', '学习计划']
            },
            'analysis': {
                'title': '数据分析报告',
                'sections': ['数据概览', '关键发现', '深度分析', '趋势预测', 'action建议']
            }
        }
    
    def create_report(
        self,
        title: str,
        description: str = "",
        template: Optional[str] = None
    ) -> Report:
        """创建报告"""
        report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        report = Report(
            id=report_id,
            title=title,
            description=description
        )
        
        # 如果指定了模板,添加预设章节
        if template and template in self.templates:
            tmpl = self.templates[template]
            report.title = tmpl['title']
            for section_name in tmpl['sections']:
                report.add_section(ReportSection(title=section_name))
        
        self.reports[report_id] = report
        return report
    
    def add_overview_section(
        self,
        report_id: str,
        metrics: Dict[str, Any],
        summary: str = ""
    ) -> bool:
        """添加概览章节"""
        if report_id not in self.reports:
            return False
        
        report = self.reports[report_id]
        
        section = ReportSection(
            title="执行摘要",
            content=summary,
            data=metrics,
            level=1
        )
        
        report.add_section(section)
        return True
    
    def add_analysis_section(
        self,
        report_id: str,
        title: str,
        findings: List[Dict],
        recommendations: List[str]
    ) -> bool:
        """添加分析章节"""
        if report_id not in self.reports:
            return False
        
        report = self.reports[report_id]
        
        content = "### 关键发现\n\n"
        for i, finding in enumerate(findings, 1):
            content += f"{i}. **{finding.get('title', '发现')}\n"
            content += f"   - {finding.get('description', '')}\n"
            if 'impact' in finding:
                content += f"   - 影响: {finding['impact']}\n"
            content += "\n"
        
        content += "### 建议\n\n"
        for i, rec in enumerate(recommendations, 1):
            content += f"{i}. {rec}\n"
        
        section = ReportSection(
            title=title,
            content=content,
            level=1
        )
        
        report.add_section(section)
        return True
    
    def add_comparison_section(
        self,
        report_id: str,
        title: str,
        items: List[Dict],
        comparison_metrics: List[str]
    ) -> bool:
        """添加对比章节"""
        if report_id not in self.reports:
            return False
        
        report = self.reports[report_id]
        
        # 构建对比表格
        content = f"| 项目 | {' | '.join(comparison_metrics)} |\n"
        content += f"|------|{'|'.join(['------'] * len(comparison_metrics))}|\n"
        
        for item in items:
            row = f"| {item.get('name', 'Unknown')} |"
            for metric in comparison_metrics:
                value = item.get(metric, 'N/A')
                row += f" {value} |"
            content += row + "\n"
        
        section = ReportSection(
            title=title,
            content=content,
            level=1
        )
        
        report.add_section(section)
        return True
    
    def add_trend_section(
        self,
        report_id: str,
        title: str,
        trend_data: Dict[str, List],
        analysis: str = ""
    ) -> bool:
        """添加趋势章节"""
        if report_id not in self.reports:
            return False
        
        report = self.reports[report_id]
        
        content = analysis + "\n\n" if analysis else ""
        content += "### 趋势数据\n\n"
        
        for metric_name, values in trend_data.items():
            if values:
                avg = sum(values) / len(values)
                trend = "上升" if values[-1] > values[0] else "下降" if values[-1] < values[0] else "平稳"
                content += f"- **{metric_name}**: 平均值 {avg:.2f}, 整体趋势 {trend}\n"
        
        section = ReportSection(
            title=title,
            content=content,
            data={k: v[-1] if v else 0 for k, v in trend_data.items()},
            level=1
        )
        
        report.add_section(section)
        return True
    
    def export_report(
        self,
        report_id: str,
        format_type: str = "markdown",
        file_path: Optional[str] = None
    ) -> Optional[str]:
        """导出报告"""
        if report_id not in self.reports:
            return None
        
        report = self.reports[report_id]
        report.format_type = format_type
        
        # generate内容
        if format_type == "markdown":
            content = report.to_markdown()
            ext = "md"
        elif format_type == "html":
            content = report.to_html()
            ext = "html"
        elif format_type == "json":
            content = json.dumps({
                'id': report.id,
                'title': report.title,
                'description': report.description,
                'created_at': report.created_at.isoformat(),
                'sections': [
                    {
                        'title': s.title,
                        'content': s.content,
                        'data': s.data
                    }
                    for s in report.sections
                ]
            }, ensure_ascii=False, indent=2)
            ext = "json"
        else:
            return None
        
        # 保存文件
        if file_path is None:
            file_path = self.output_dir / f"{report_id}.{ext}"
        
        Path(file_path).write_text(content, encoding='utf-8')
        return str(file_path)
    
    def generate_performance_report(
        self,
        metrics: Dict[str, Any],
        period: str = "最近30天"
    ) -> Report:
        """generate性能报告"""
        report = self.create_report(
            title=f"性能分析报告 - {period}",
            description=f"本报告分析了{period}的系统性能表现",
            template='performance'
        )
        
        # 概览
        self.add_overview_section(
            report.id,
            metrics.get('overview', {}),
            f"在{period}期间,系统整体表现{'良好' if metrics.get('overall_score', 0) > 0.7 else '有待提升'}."
        )
        
        # 关键metrics
        if 'key_metrics' in metrics:
            self.add_analysis_section(
                report.id,
                "关键metrics分析",
                [
                    {
                        'title': name,
                        'description': f"当前值: {data.get('current', 'N/A')}, 目标: {data.get('target', 'N/A')}",
                        'impact': f"达成率: {data.get('achievement', 0) * 100:.1f}%"
                    }
                    for name, data in metrics['key_metrics'].items()
                ],
                metrics.get('recommendations', [])
            )
        
        return report
    
    def generate_strategy_report(
        self,
        strategy_data: Dict[str, Any]
    ) -> Report:
        """generatestrategy报告"""
        report = self.create_report(
            title="strategy执行报告",
            description="strategy执行进度和效果分析",
            template='strategy'
        )
        
        # 执行摘要
        self.add_overview_section(
            report.id,
            {
                'strategy名称': strategy_data.get('name', 'Unknown'),
                '执行进度': f"{strategy_data.get('progress', 0) * 100:.1f}%",
                '剩余时间': f"{strategy_data.get('remaining_days', 0)}天",
                '整体评分': strategy_data.get('score', 0)
            },
            strategy_data.get('summary', '')
        )
        
        # 目标达成情况
        if 'goals' in strategy_data:
            self.add_comparison_section(
                report.id,
                "目标达成情况",
                [
                    {
                        'name': goal['name'],
                        '目标值': goal.get('target', 'N/A'),
                        '当前值': goal.get('current', 'N/A'),
                        '达成率': f"{goal.get('progress', 0) * 100:.1f}%",
                        '状态': '已达成' if goal.get('progress', 0) >= 1 else '进行中'
                    }
                    for goal in strategy_data['goals']
                ],
                ['目标值', '当前值', '达成率', '状态']
            )
        
        return report
    
    def generate_learning_report(
        self,
        learning_data: Dict[str, Any]
    ) -> Report:
        """generate学习报告"""
        report = self.create_report(
            title="学习进度报告",
            description="个人学习进度和知识掌握情况",
            template='learning'
        )
        
        # 学习概览
        self.add_overview_section(
            report.id,
            {
                '总学习时长': f"{learning_data.get('total_hours', 0)}小时",
                '完成课程': f"{learning_data.get('completed_courses', 0)}门",
                '知识掌握度': f"{learning_data.get('mastery_rate', 0) * 100:.1f}%",
                '学习天数': learning_data.get('learning_days', 0)
            },
            learning_data.get('summary', '持续学习中,保持良好的学习习惯.')
        )
        
        # 知识领域
        if 'knowledge_areas' in learning_data:
            self.add_analysis_section(
                report.id,
                "知识掌握情况",
                [
                    {
                        'title': area['name'],
                        'description': f"掌握程度: {area.get('level', 'beginner')}",
                        'impact': f"进度: {area.get('progress', 0) * 100:.1f}%"
                    }
                    for area in learning_data['knowledge_areas']
                ],
                learning_data.get('next_steps', [])
            )
        
        return report
    
    def list_reports(self) -> List[Dict]:
        """列出所有报告"""
        return [
            {
                'id': r.id,
                'title': r.title,
                'created_at': r.created_at.isoformat(),
                'section_count': len(r.sections)
            }
            for r in self.reports.values()
        ]

# 便捷函数
def create_report_engine(output_dir: str = "./reports") -> ReportEngine:
    """创建报告引擎"""
    return ReportEngine(output_dir)

# 向后兼容别名
ReportGenerator = ReportEngine  # _agent_types.py 期望的类名
