#!/usr/bin/env python3
"""
每日学习报告生成器
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from collections import Counter


@dataclass
class DailyReport:
    """每日学习报告"""
    date: str
    total_sessions: int
    total_duration_minutes: float
    average_confidence: float
    dimensions_covered: List[str]
    dimensions_count: Dict[str, int]
    top_insights: List[Dict[str, Any]]
    action_items_summary: List[str]
    knowledge_growth: Dict[str, float]
    recommendations: List[str]
    next_day_plan: List[str]


class LearningReportGenerator:
    """学习报告生成器"""
    
    def __init__(self):
        self.output_dir = Path("data/learning/super_learning")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _group_sessions_by_date(self, sessions: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """按日期分组学习会话"""
        grouped = {}
        for session in sessions:
            date = session['timestamp'][:10]
            if date not in grouped:
                grouped[date] = []
            grouped[date].append(session)
        return grouped
    
    def _extract_insights_by_dimension(self, sessions: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """按维度提取洞察"""
        insights_by_dim = {}
        for session in sessions:
            dim = session['dimension']
            if dim not in insights_by_dim:
                insights_by_dim[dim] = []
            insights_by_dim[dim].extend(session['insights'])
        return insights_by_dim
    
    def _generate_report_content(self, sessions: List[Dict[str, Any]]) -> str:
        """生成HTML报告内容"""
        if not sessions:
            return self._generate_empty_report()
        
        # 统计数据
        total_sessions = len(sessions)
        total_duration = sum(s['duration_seconds'] for s in sessions) / 60
        avg_confidence = sum(s['confidence_score'] for s in sessions) / total_sessions
        
        # 维度统计
        dimensions = [s['dimension'] for s in sessions]
        dimensions_count = Counter(dimensions)
        
        # 提取洞察
        all_insights = []
        for session in sessions:
            for insight in session['insights']:
                all_insights.append({
                    'dimension': session['dimension'],
                    'topic': session['topic'],
                    'insight': insight,
                    'confidence': session['confidence_score']
                })
        
        # 按置信度排序，取前20条
        top_insights = sorted(all_insights, key=lambda x: x['confidence'], reverse=True)[:20]
        
        # 提取行动项
        action_items = []
        for session in sessions:
            action_items.extend(session['action_items'])
        action_items_summary = list(set(action_items))[:15]
        
        # 知识增长评估
        knowledge_growth = {dim: count / total_sessions for dim, count in dimensions_count.items()}
        
        # 生成推荐
        recommendations = self._generate_recommendations(dimensions_count)
        next_day_plan = self._generate_next_day_plan(dimensions_count)
        
        # 生成HTML
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日学习报告 - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
        h1 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #764ba2;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-bottom: 8px;
            border-bottom: 2px solid #eee;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        .stat-card h3 {{
            margin: 0 0 10px 0;
            font-size: 14px;
            opacity: 0.9;
        }}
        .stat-card .value {{
            font-size: 32px;
            font-weight: bold;
            margin: 0;
        }}
        .dimension-bar {{
            margin: 15px 0;
        }}
        .dimension-name {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-weight: 500;
        }}
        .bar {{
            background: #f0f0f0;
            border-radius: 10px;
            overflow: hidden;
            height: 30px;
        }}
        .bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            padding-left: 10px;
            color: white;
            font-size: 14px;
            transition: width 0.5s ease;
        }}
        .insight-card {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .insight-dimension {{
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
        }}
        .insight-topic {{
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        .insight-text {{
            color: #555;
            font-size: 14px;
        }}
        .confidence-badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 10px;
        }}
        .action-item {{
            background: #e7f3ff;
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }}
        .recommendation {{
            background: #fff3cd;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #ffc107;
        }}
        .next-plan-item {{
            background: #d4edda;
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            border-left: 4px solid #28a745;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 14px;
        }}
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 每日学习报告</h1>
        
        <div style="text-align: center; color: #666; margin-bottom: 30px;">
            <strong>报告日期:</strong> {datetime.now().strftime('%Y年%m月%d日')} &nbsp;&nbsp;
            <strong>生成时间:</strong> {datetime.now().strftime('%H:%M:%S')}
        </div>
        
        <h2>📊 学习统计</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <h3>学习会话数</h3>
                <p class="value">{total_sessions}</p>
            </div>
            <div class="stat-card">
                <h3>总学习时长</h3>
                <p class="value">{total_duration:.1f}分钟</p>
            </div>
            <div class="stat-card">
                <h3>平均置信度</h3>
                <p class="value">{avg_confidence:.2%}</p>
            </div>
            <div class="stat-card">
                <h3>覆盖维度数</h3>
                <p class="value">{len(dimensions_count)}</p>
            </div>
        </div>
        
        <h2>📈 学习维度分布</h2>
        <div style="margin-top: 20px;">
"""
        
        # 添加维度分布条
        sorted_dims = sorted(dimensions_count.items(), key=lambda x: x[1], reverse=True)
        for dim, count in sorted_dims:
            percentage = (count / total_sessions) * 100
            html_content += f"""
            <div class="dimension-bar">
                <div class="dimension-name">
                    <span>{dim}</span>
                    <span>{count}次 ({percentage:.1f}%)</span>
                </div>
                <div class="bar">
                    <div class="bar-fill" style="width: {percentage}%"></div>
                </div>
            </div>
"""
        
        html_content += """
        </div>
        
        <h2>💡 核心洞察 (Top 20)</h2>
"""
        
        for insight in top_insights:
            html_content += f"""
        <div class="insight-card">
            <div class="insight-dimension">
                <span>🎯 {insight['dimension']}</span>
                <span class="confidence-badge">置信度: {insight['confidence']:.2%}</span>
            </div>
            <div class="insight-topic">📌 {insight['topic']}</div>
            <div class="insight-text">{insight['insight']}</div>
        </div>
"""
        
        html_content += """
        
        <h2>✓ 待执行行动项</h2>
"""
        
        for action in action_items_summary:
            html_content += f"""
        <div class="action-item">
            <strong>• {action}</strong>
        </div>
"""
        
        html_content += f"""
        
        <h2>🎯 知识增长评估</h2>
        <div style="margin-top: 20px;">
"""
        
        sorted_growth = sorted(knowledge_growth.items(), key=lambda x: x[1], reverse=True)
        for dim, growth in sorted_growth:
            percentage = growth * 100
            html_content += f"""
            <div class="dimension-bar">
                <div class="dimension-name">
                    <span>{dim}</span>
                    <span>增长: {percentage:.1f}%</span>
                </div>
                <div class="bar">
                    <div class="bar-fill" style="width: {percentage}%"></div>
                </div>
            </div>
"""
        
        html_content += """
        </div>
        
        <h2>💭 改进建议</h2>
"""
        
        for rec in recommendations:
            html_content += f"""
        <div class="recommendation">
            <strong>💡 {rec}</strong>
        </div>
"""
        
        html_content += """
        
        <h2>🚀 明日学习计划</h2>
"""
        
        for plan in next_day_plan:
            html_content += f"""
        <div class="next-plan-item">
            <strong>→ {plan}</strong>
        </div>
"""
        
        html_content += f"""
        
        <div class="footer">
            <p>🤖 Somn 智能学习系统 | 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>持续进化，每日成长 🌱</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html_content
    
    def _generate_empty_report(self) -> str:
        """生成空报告"""
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>每日学习报告 - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
        }}
        h1 {{
            color: #999;
            font-size: 24px;
        }}
        .icon {{
            font-size: 64px;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">📝</div>
        <h1>暂无学习会话</h1>
        <p style="color: #666; margin: 20px 0;">今日尚未执行任何学习会话</p>
        <p style="color: #999; font-size: 14px;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>
"""
    
    def _generate_recommendations(self, dimensions_count) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        total = sum(dimensions_count.values())
        
        # 检查学习不均衡的维度
        for dim, count in dimensions_count.items():
            percentage = count / total
            if percentage < 0.05:
                recommendations.append(f"维度 '{dim}' 学习较少，建议加强关注")
        
        if not recommendations:
            recommendations.append("各维度学习均衡，继续保持")
            recommendations.append("可以尝试更深入地研究已覆盖的维度")
        
        # 通用建议
        recommendations.append("定期回顾学习成果，将洞察转化为实际行动")
        recommendations.append("保持对新知识的好奇心，探索跨维度的关联")
        
        return recommendations[:5]
    
    def _generate_next_day_plan(self, dimensions_count) -> List[str]:
        """生成明日学习计划"""
        plan = []
        
        total = sum(dimensions_count.values())
        
        # 找出学习最少的维度
        if dimensions_count:
            sorted_dims = sorted(dimensions_count.items(), key=lambda x: x[1])
            bottom_dims = sorted_dims[:3]
            
            for dim, _ in bottom_dims:
                plan.append(f"重点学习 '{dim}' 维度的新主题")
        
        # 通用计划
        plan.extend([
            "继续执行每日深度学习计划",
            "执行今日行动项",
            "记录学习中的疑问和思考"
        ])
        
        return plan[:5]
    
    def generate_report(self, sessions: List) -> DailyReport:
        """生成报告数据结构"""
        if not sessions:
            return DailyReport(
                date=datetime.now().strftime('%Y-%m-%d'),
                total_sessions=0,
                total_duration_minutes=0,
                average_confidence=0,
                dimensions_covered=[],
                dimensions_count={},
                top_insights=[],
                action_items_summary=[],
                knowledge_growth={},
                recommendations=["请开始学习会话"],
                next_day_plan=["启动超级学习计划"]
            )
        
        # 统计数据
        total_sessions = len(sessions)
        total_duration = sum(s.duration_seconds for s in sessions) / 60
        avg_confidence = sum(s.confidence_score for s in sessions) / total_sessions
        
        # 维度统计
        dimensions_count = {}
        for s in sessions:
            dim = s.dimension
            dimensions_count[dim] = dimensions_count.get(dim, 0) + 1
        
        # 提取洞察
        all_insights = []
        for s in sessions:
            for insight in s.insights:
                all_insights.append({
                    'dimension': s.dimension,
                    'topic': s.topic,
                    'insight': insight,
                    'confidence': s.confidence_score
                })
        
        top_insights = sorted(all_insights, key=lambda x: x['confidence'], reverse=True)[:20]
        
        # 提取行动项
        action_items = []
        for s in sessions:
            action_items.extend(s.action_items)
        action_items_summary = list(set(action_items))[:15]
        
        # 知识增长评估
        knowledge_growth = {dim: count / total_sessions for dim, count in dimensions_count.items()}
        
        # 生成推荐
        recommendations = self._generate_recommendations(dimensions_count)
        next_day_plan = self._generate_next_day_plan(dimensions_count)
        
        return DailyReport(
            date=datetime.now().strftime('%Y-%m-%d'),
            total_sessions=total_sessions,
            total_duration_minutes=total_duration,
            average_confidence=avg_confidence,
            dimensions_covered=list(dimensions_count.keys()),
            dimensions_count=dimensions_count,
            top_insights=top_insights,
            action_items_summary=action_items_summary,
            knowledge_growth=knowledge_growth,
            recommendations=recommendations,
            next_day_plan=next_day_plan
        )
    
    def save_report(self, report: DailyReport, filepath: Path):
        """保存HTML报告"""
        sessions_data = [
            {
                'timestamp': datetime.now().isoformat(),
                'dimension': insight['dimension'],
                'topic': insight['topic'],
                'insights': [insight['insight']],
                'action_items': [],
                'confidence_score': insight['confidence'],
                'duration_seconds': 1.0
            }
            for insight in report.top_insights
        ]
        
        html_content = self._generate_report_content(sessions_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)


if __name__ == "__main__":
    generator = LearningReportGenerator()
    
    # 测试生成空报告
    generator.save_report(
        DailyReport(
            date=datetime.now().strftime('%Y-%m-%d'),
            total_sessions=0,
            total_duration_minutes=0,
            average_confidence=0,
            dimensions_covered=[],
            dimensions_count={},
            top_insights=[],
            action_items_summary=[],
            knowledge_growth={},
            recommendations=[],
            next_day_plan=[]
        ),
        generator.output_dir / "test_report.html"
    )
    
    print(f"测试报告已生成: {generator.output_dir / 'test_report.html'}")
