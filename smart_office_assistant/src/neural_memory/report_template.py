# -*- coding: utf-8 -*-
"""
__all__ = [
    'generate_html_report',
    'generate_sample_report',
]

学习报告模板generate器
generate可视化的每日学习报告(HTML格式)
"""

from pathlib import Path
from src.core.paths import LEARNING_DIR
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class LearningMetrics:
    """学习metrics数据"""
    total_events: int
    instance_count: int
    validation_count: int
    error_count: int
    association_count: int
    knowledge_updates: int
    confidence_changes: List[Dict[str, Any]]
    

class LearningReportTemplate:
    """
    学习报告模板generate器
    
    generate美观的HTML格式学习报告,包含:
    - 学习概览卡片
    - 学习类型分布图表
    - 知识更新详情
    - 置信度变化趋势
    - 系统健康度metrics
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path)
        self.reports_path = self.base_path / "daily_reports"
        self.reports_path.mkdir(parents=True, exist_ok=True)
        
    def generate_html_report(
        self,
        report_data: Dict[str, Any],
        output_filename: str = None
    ) -> Path:
        """
        generateHTML格式的学习报告
        
        Args:
            report_data: 报告数据字典
            output_filename: 输出文件名(可选)
            
        Returns:
            generate的HTML文件路径
        """
        if output_filename is None:
            date_str = datetime.now().strftime("%Y%m%d")
            output_filename = f"learning_report_{date_str}.html"
            
        output_path = self.reports_path / output_filename
        
        html_content = self._build_html(report_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        # 同时更新 latest.html
        latest_path = self.reports_path / "latest.html"
        with open(latest_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return output_path
    
    def _build_html(self, data: Dict[str, Any]) -> str:
        """构建HTML报告内容"""
        
        date_str = data.get('date', datetime.now().strftime("%Y-%m-%d"))
        summary = data.get('summary', {})
        metrics = self._extract_metrics(data)
        
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日学习报告 - {date_str}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --primary-color: #4F46E5;
            --secondary-color: #10B981;
            --warning-color: #F59E0B;
            --danger-color: #EF4444;
            --bg-color: #F3F4F6;
            --card-bg: #FFFFFF;
            --text-primary: #1F2937;
            --text-secondary: #6B7280;
            --border-color: #E5E7EB;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, var(--primary-color), #7C3AED);
            color: white;
            padding: 40px;
            border-radius: 16px;
            margin-bottom: 30px;
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            opacity: 0.9;
            font-size: 1.1rem;
        }}
        
        /* Metrics Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: var(--card-bg);
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }}
        
        .metric-card .icon {{
            font-size: 2rem;
            margin-bottom: 12px;
        }}
        
        .metric-card .value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: var(--primary-color);
            margin-bottom: 4px;
        }}
        
        .metric-card .label {{
            color: var(--text-secondary);
            font-size: 0.95rem;
        }}
        
        .metric-card.success .value {{ color: var(--secondary-color); }}
        .metric-card.warning .value {{ color: var(--warning-color); }}
        .metric-card.danger .value {{ color: var(--danger-color); }}
        
        /* Charts Section */
        .charts-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 24px;
            margin-bottom: 30px;
        }}
        
        .chart-card {{
            background: var(--card-bg);
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .chart-card h3 {{
            margin-bottom: 20px;
            color: var(--text-primary);
            font-size: 1.2rem;
        }}
        
        .chart-container {{
            position: relative;
            height: 300px;
        }}
        
        /* Details Section */
        .details-section {{
            background: var(--card-bg);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }}
        
        .details-section h2 {{
            margin-bottom: 20px;
            color: var(--text-primary);
            font-size: 1.5rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 10px;
        }}
        
        .detail-item {{
            padding: 16px;
            background: var(--bg-color);
            border-radius: 8px;
            margin-bottom: 12px;
            border-left: 4px solid var(--primary-color);
        }}
        
        .detail-item.success {{ border-left-color: var(--secondary-color); }}
        .detail-item.warning {{ border-left-color: var(--warning-color); }}
        .detail-item.danger {{ border-left-color: var(--danger-color); }}
        
        .detail-item h4 {{
            margin-bottom: 8px;
            color: var(--text-primary);
        }}
        
        .detail-item p {{
            color: var(--text-secondary);
            font-size: 0.95rem;
        }}
        
        .detail-item .meta {{
            margin-top: 8px;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}
        
        /* Status Badge */
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .status-badge.success {{
            background: #D1FAE5;
            color: #065F46;
        }}
        
        .status-badge.warning {{
            background: #FEF3C7;
            color: #92400E;
        }}
        
        .status-badge.danger {{
            background: #FEE2E2;
            color: #991B1B;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 20px;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}
            
            .charts-section {{
                grid-template-columns: 1fr;
            }}
            
            .metric-card .value {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🧠 每日学习报告</h1>
            <div class="subtitle">
                {date_str} | 神经记忆系统自动generate
            </div>
        </div>
        
        <!-- Metrics Overview -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="icon">📊</div>
                <div class="value">{metrics.total_events}</div>
                <div class="label">总学习事件</div>
            </div>
            <div class="metric-card success">
                <div class="icon">💡</div>
                <div class="value">{metrics.instance_count}</div>
                <div class="label">实例学习</div>
            </div>
            <div class="metric-card">
                <div class="icon">✅</div>
                <div class="value">{metrics.validation_count}</div>
                <div class="label">验证学习</div>
            </div>
            <div class="metric-card warning">
                <div class="icon">🔧</div>
                <div class="value">{metrics.error_count}</div>
                <div class="label">错误学习</div>
            </div>
            <div class="metric-card">
                <div class="icon">🔗</div>
                <div class="value">{metrics.association_count}</div>
                <div class="label">关联学习</div>
            </div>
            <div class="metric-card success">
                <div class="icon">📚</div>
                <div class="value">{metrics.knowledge_updates}</div>
                <div class="label">知识更新</div>
            </div>
        </div>
        
        <!-- Charts -->
        <div class="charts-section">
            <div class="chart-card">
                <h3>学习类型分布</h3>
                <div class="chart-container">
                    <canvas id="learningTypeChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h3>知识增长趋势</h3>
                <div class="chart-container">
                    <canvas id="knowledgeTrendChart"></canvas>
                </div>
            </div>
        </div>
        
        <!-- Learning Details -->
        <div class="details-section">
            <h2>📋 学习详情</h2>
            {self._build_detail_items(data)}
        </div>
        
        <!-- System Status -->
        <div class="details-section">
            <h2>🔍 系统状态</h2>
            {self._build_system_status(data)}
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>🌙 Somn 神经记忆系统 | 报告generate时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </div>
    
    <script>
        // 学习类型分布图表
        const learningTypeCtx = document.getElementById('learningTypeChart').getContext('2d');
        new Chart(learningTypeCtx, {{
            type: 'doughnut',
            data: {{
                labels: ['实例学习', '验证学习', '错误学习', '关联学习'],
                datasets: [{{
                    data: [{metrics.instance_count}, {metrics.validation_count}, {metrics.error_count}, {metrics.association_count}],
                    backgroundColor: [
                        '#10B981',
                        '#4F46E5',
                        '#F59E0B',
                        '#8B5CF6'
                    ],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 15,
                            font: {{
                                size: 12
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // 知识增长趋势图表
        const knowledgeTrendCtx = document.getElementById('knowledgeTrendChart').getContext('2d');
        new Chart(knowledgeTrendCtx, {{
            type: 'line',
            data: {{
                labels: ['概念', '规则', '关系', '模式'],
                datasets: [{{
                    label: '知识增长',
                    data: [
                        {summary.get('concept_growth', 0)},
                        {summary.get('rule_growth', 0)},
                        {summary.get('relation_growth', 0)},
                        {summary.get('pattern_growth', 0)}
                    ],
                    borderColor: '#4F46E5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{
                            color: 'rgba(0,0,0,0.05)'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    def _extract_metrics(self, data: Dict[str, Any]) -> LearningMetrics:
        """从报告数据中提取metrics"""
        summary = data.get('summary', {})
        
        return LearningMetrics(
            total_events=summary.get('total_events', 0),
            instance_count=summary.get('instance_learning', 0),
            validation_count=summary.get('validation_learning', 0),
            error_count=summary.get('error_learning', 0),
            association_count=summary.get('association_learning', 0),
            knowledge_updates=summary.get('knowledge_updates', 0),
            confidence_changes=data.get('confidence_changes', [])
        )
    
    def _build_detail_items(self, data: Dict[str, Any]) -> str:
        """构建详情项目HTML"""
        items = []
        
        # 实例学习详情
        instance_events = data.get('instance_events', [])
        for event in instance_events[:3]:  # 最多显示3个
            items.append(f"""
            <div class="detail-item success">
                <h4>💡 实例学习: {event.get('pattern_name', '新模式')}</h4>
                <p>{event.get('description', '从具体案例中提取模式')}</p>
                <div class="meta">
                    置信度: <span class="status-badge success">{event.get('confidence', '中')}</span>
                    场景: {event.get('scenario', '通用')}
                </div>
            </div>
            """)
        
        # 验证学习详情
        validation_events = data.get('validation_events', [])
        for event in validation_events[:2]:
            items.append(f"""
            <div class="detail-item">
                <h4>✅ 验证学习: {event.get('hypothesis', '假设验证')}</h4>
                <p>置信度更新: {event.get('old_confidence', 0.5):.2f} → {event.get('new_confidence', 0.6):.2f}</p>
                <div class="meta">
                    验证方法: {event.get('method', '观察验证')}
                </div>
            </div>
            """)
        
        # 错误学习详情
        error_events = data.get('error_events', [])
        for event in error_events[:2]:
            items.append(f"""
            <div class="detail-item warning">
                <h4>🔧 错误学习: {event.get('error_pattern', '错误模式recognize')}</h4>
                <p>{event.get('lesson', '从失败中提取教训')}</p>
                <div class="meta">
                    影响范围: {event.get('scope', '局部')}
                </div>
            </div>
            """)
        
        if not items:
            items.append("""
            <div class="detail-item">
                <h4>📝 今日暂无新的学习事件</h4>
                <p>系统持续监控中,将在发现新数据时自动触发学习.</p>
            </div>
            """)
        
        return '\n'.join(items)
    
    def _build_system_status(self, data: Dict[str, Any]) -> str:
        """构建系统状态HTML"""
        system_status = data.get('system_status', {})
        health_score = system_status.get('health_score', 0.8)
        
        health_class = 'success' if health_score >= 0.8 else 'warning' if health_score >= 0.6 else 'danger'
        health_label = '健康' if health_score >= 0.8 else '需关注' if health_score >= 0.6 else '异常'
        
        return f"""
        <div class="detail-item {health_class}">
            <h4>🏥 系统健康度</h4>
            <p>当前评分: <strong>{health_score:.0%}</strong> <span class="status-badge {health_class}">{health_label}</span></p>
            <div class="meta">
                知识库规模: {system_status.get('knowledge_base_size', 'N/A')} | 
                记忆网络密度: {system_status.get('memory_density', 'N/A')} | 
                最近更新: {system_status.get('last_update', '刚刚')}
            </div>
        </div>
        
        <div class="detail-item">
            <h4>📈 学习效能</h4>
            <p>今日学习效率良好,共处理 {data.get('summary', {}).get('total_events', 0)} 个学习事件.</p>
            <div class="meta">
                数据扫描范围: 过去24小时 | 
                新发现: {data.get('new_findings', 0)} 个 | 
                模式提取: {data.get('patterns_extracted', 0)} 个
            </div>
        </div>
        
        <div class="detail-item success">
            <h4>🎯 建议与展望</h4>
            <p>{data.get('recommendations', ['继续监控数据流,保持学习节奏'])[0]}</p>
            <div class="meta">
                下次自动学习: 明日 09:00
            </div>
        </div>
        """

def generate_sample_report():
    """generate示例报告(用于测试)"""
    template = LearningReportTemplate()
    
    sample_data = {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'summary': {
            'total_events': 12,
            'instance_learning': 5,
            'validation_learning': 3,
            'error_learning': 2,
            'association_learning': 2,
            'knowledge_updates': 8,
            'concept_growth': 3,
            'rule_growth': 2,
            'relation_growth': 4,
            'pattern_growth': 1
        },
        'instance_events': [
            {
                'pattern_name': '用户偏好模式A',
                'description': '发现用户在上午9-11点活跃度最高',
                'confidence': '高',
                'scenario': '用户行为分析'
            },
            {
                'pattern_name': '文档处理模式B',
                'description': '周报generate任务通常在周五下午触发',
                'confidence': '中',
                'scenario': '任务调度'
            }
        ],
        'validation_events': [
            {
                'hypothesis': '用户喜欢简洁界面',
                'old_confidence': 0.6,
                'new_confidence': 0.75,
                'method': 'A/B测试'
            }
        ],
        'error_events': [
            {
                'error_pattern': '大文件处理超时',
                'lesson': '需要增加文件大小检测和分块处理机制',
                'scope': '文件处理模块'
            }
        ],
        'system_status': {
            'health_score': 0.85,
            'knowledge_base_size': '1,247条',
            'memory_density': '0.72',
            'last_update': '10分钟前'
        },
        'new_findings': 5,
        'patterns_extracted': 3,
        'recommendations': [
            '建议增加对周末用户行为的监控',
            '考虑优化大文件处理流程'
        ]
    }
    
    output_path = template.generate_html_report(sample_data)
    logger.info(f"示例报告已生成: {output_path}")
    return output_path

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
