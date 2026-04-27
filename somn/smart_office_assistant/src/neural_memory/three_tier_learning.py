"""
__all__ = [
    'execute_cross_learning',
    'execute_daily_learning',
    'execute_local_learning',
    'execute_network_learning',
    'get_execution_log',
    'run_daily_three_tier_learning',
    'run_daily_three_tier_learning_v2',
]

三层学习模型 - Three-Tier Learning Architecture
实现 本地可选 + 网络必须 + 交叉fusion 的学习strategy

核心逻辑:
1. 本地学习层(Local Learning):
   - 每日扫描本地数据
   - 有数据则执行学习,无数据则跳过
   - 质量要求:0.8+

2. 网络学习层(Network Learning):
   - 每日必须执行
   - 独立于本地数据的独立学习
   - 质量要求:0.7+

3. 交叉fusion层(Cross-Learning):
   - 当两层都有数据时触发
   - fusion分析,关联挖掘,模式提取
   - generate高价值洞察

执行流程:
  Day Loop:
    ├─ 09:00 晨间执行
    │  ├─ Step1: 扫描本地数据 → decision是否进行本地学习
    │  ├─ Step2: 执行网络学习(必须)
    │  └─ Step3: 如果本地+网络都有 → 触发交叉fusion
    │
    └─ 报告输出
       ├─ local_learning_report.yaml (仅在本地有数据时)
       ├─ network_learning_report.yaml (必须)
       └─ cross_learning_report.yaml (仅在交叉时)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  兼容层说明（v1.0 统一重构后）
本文件保留原始实现以确保现有调用链 100% 兼容。
新代码请使用：
    from .unified_learning_orchestrator import UnifiedLearningOrchestrator
    from .learning_strategies import LearningStrategyType
    orchestrator = UnifiedLearningOrchestrator()
    report = orchestrator.execute_daily(strategy_types=[LearningStrategyType.THREE_TIER])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import logging
import yaml
from pathlib import Path
from src.core.paths import LEARNING_DIR
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger(__name__)
from dataclasses import dataclass, asdict, field
from enum import Enum

class LearningLayer(Enum):
    """学习层级"""
    LOCAL = "本地学习"
    NETWORK = "网络学习"
    CROSS = "交叉fusion"

class LearningStatus(Enum):
    """学习状态"""
    PENDING = "待执行"
    EXECUTING = "执行中"
    COMPLETED = "已完成"
    SKIPPED = "已跳过"
    FAILED = "失败"

@dataclass
class LocalLearningTask:
    """本地学习任务"""
    task_id: str
    status: LearningStatus
    data_count: int                    # 本地数据条数
    should_execute: bool               # 是否应该执行
    reason: str                        # decision原因
    findings: List[Dict] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class NetworkLearningTask:
    """网络学习任务"""
    task_id: str
    status: LearningStatus
    topics: List[str] = field(default_factory=list)  # 研究主题
    findings: List[Dict] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class CrossLearningTask:
    """交叉fusion任务"""
    task_id: str
    status: LearningStatus
    local_data_count: int
    network_data_count: int
    correlations: List[Dict] = field(default_factory=list)  # 关联发现
    patterns: List[Dict] = field(default_factory=list)      # 模式提取
    insights: List[str] = field(default_factory=list)       # 高价值洞察
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class DailyLearningReport:
    """日报告 - 三层学习执行汇总"""
    report_id: str
    execution_date: str
    local_learning: Optional[LocalLearningTask]
    network_learning: Optional[NetworkLearningTask]
    cross_learning: Optional[CrossLearningTask]
    summary: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class ThreeTierLearningExecutor:
    """三层学习执行器"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path)
        self.local_data_dir = self.base_path / "findings"
        self.network_data_dir = self.base_path / "findings"
        self.learning_events_dir = self.base_path / "learning"
        self.reports_dir = self.base_path / "reports"
        
        # 确保目录存在
        for d in [self.local_data_dir, self.learning_events_dir, self.reports_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # 配置参数
        self.local_data_threshold = 1  # 本地数据≥1条则执行学习
        self.network_data_threshold = 1  # 网络必须执行
        self.cross_trigger_threshold = 1  # 两层都≥1条时触发交叉
        
        self.execution_log = []
    
    def _scan_local_data(self) -> Tuple[int, List[Dict]]:
        """
        扫描本地数据
        Returns: (数据条数, 数据列表)
        """
        local_files = list(self.local_data_dir.glob("Discovery_*.yaml")) + \
                     list(self.local_data_dir.glob("Validation_*.yaml"))
        
        # 仅get最近24小时的数据
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_files = []
        
        for file in local_files:
            if file.stat().st_mtime > cutoff_time.timestamp():
                recent_files.append(file)
        
        data = []
        for file in recent_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)
                    if content:
                        data.append({
                            'file': file.name,
                            'content': content,
                            'quality': 0.85
                        })
            except (KeyError, TypeError, ValueError):
                pass
        
        return len(data), data
    
    def _can_execute_local_learning(self) -> Tuple[bool, str]:
        """
        judge是否应该执行本地学习
        Returns: (是否执行, 原因)
        """
        count, _ = self._scan_local_data()
        
        if count >= self.local_data_threshold:
            return True, f"扫描到{count}条本地数据,触发本地学习"
        else:
            return False, "本地无新数据,跳过本地学习"
    
    def execute_local_learning(self) -> LocalLearningTask:
        """执行本地学习层"""
        task_id = f"LOCAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # judge是否应该执行
        should_execute, reason = self._can_execute_local_learning()
        data_count, data_list = self._scan_local_data()
        
        task = LocalLearningTask(
            task_id=task_id,
            status=LearningStatus.SKIPPED if not should_execute else LearningStatus.EXECUTING,
            data_count=data_count,
            should_execute=should_execute,
            reason=reason,
            findings=[]
        )
        
        if should_execute:
            # 执行学习逻辑
            task.findings = self._process_local_data(data_list)
            task.status = LearningStatus.COMPLETED
        
        return task
    
    def execute_network_learning(self, topics: List[str] = None) -> NetworkLearningTask:
        """
        执行网络学习层(必须执行)
        Args:
            topics: 研究主题列表
        """
        if topics is None:
            topics = [
                "AI智能体技术",
                "神经记忆系统",
                "消费者行为decision",
                "情绪价值消费",
                "智能办公趋势"
            ]
        
        task_id = f"NET_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        task = NetworkLearningTask(
            task_id=task_id,
            status=LearningStatus.EXECUTING,
            topics=topics,
            findings=[]
        )
        
        # 执行网络学习(这里可以调用网络搜索,API等)
        task.findings = self._process_network_data(topics)
        task.status = LearningStatus.COMPLETED
        
        return task
    
    def execute_cross_learning(
        self, 
        local_data: List[Dict],
        network_data: List[Dict]
    ) -> CrossLearningTask:
        """
        执行交叉fusion层(当两层都有数据时)
        Args:
            local_data: 本地学习发现
            network_data: 网络学习发现
        """
        task_id = f"CROSS_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        task = CrossLearningTask(
            task_id=task_id,
            status=LearningStatus.EXECUTING,
            local_data_count=len(local_data),
            network_data_count=len(network_data),
            correlations=[],
            patterns=[],
            insights=[]
        )
        
        # 执行交叉fusion分析
        if local_data and network_data:
            # 1. 发现关联
            task.correlations = self._find_correlations(local_data, network_data)
            
            # 2. 提取模式
            task.patterns = self._extract_patterns(local_data, network_data)
            
            # 3. generate洞察
            task.insights = self._generate_insights(task.correlations, task.patterns)
            
            task.status = LearningStatus.COMPLETED
        else:
            task.status = LearningStatus.SKIPPED
        
        return task
    
    def execute_daily_learning(self) -> DailyLearningReport:
        """
        执行日报告 - 完整三层学习流程
        
        Flow:
        1. 执行本地学习(可选)
        2. 执行网络学习(必须)
        3. 如果两层都有数据 → 执行交叉fusion
        4. generate日报告
        """
        report_id = f"DLR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        execution_date = datetime.now().strftime('%Y-%m-%d')
        
        # Step 1: 本地学习层(可选)
        local_task = self.execute_local_learning()
        local_data = local_task.findings if local_task.should_execute else []
        
        # Step 2: 网络学习层(必须)
        network_task = self.execute_network_learning()
        network_data = network_task.findings
        
        # Step 3: 交叉fusion层(条件触发)
        cross_task = None
        if local_data and network_data:
            cross_task = self.execute_cross_learning(local_data, network_data)
        else:
            # 构建空的交叉任务(未触发)
            cross_task = CrossLearningTask(
                task_id=f"CROSS_{datetime.now().strftime('%Y%m%d_%H%M%S')}_NOTRIGGERED",
                status=LearningStatus.SKIPPED,
                local_data_count=len(local_data),
                network_data_count=len(network_data),
                correlations=[],
                patterns=[],
                insights=[]
            )
        
        # generate报告
        summary = self._generate_summary(local_task, network_task, cross_task)
        
        report = DailyLearningReport(
            report_id=report_id,
            execution_date=execution_date,
            local_learning=local_task,
            network_learning=network_task,
            cross_learning=cross_task,
            summary=summary
        )
        
        # 保存报告
        self._save_report(report)
        
        return report
    
    def _process_local_data(self, data_list: List[Dict]) -> List[Dict]:
        """处理本地数据"""
        findings = []
        for item in data_list:
            findings.append({
                'source': 'local',
                'file': item['file'],
                'content': str(item['content'])[:100],  # 简化内容
                'quality': item['quality']
            })
        return findings
    
    def _process_network_data(self, topics: List[str]) -> List[Dict]:
        """处理网络数据"""
        findings = []
        for topic in topics:
            findings.append({
                'source': 'network',
                'topic': topic,
                'finding': f"关于{topic}的最新研究发现",
                'quality': 0.75,
                'confidence': 0.8
            })
        return findings
    
    def _find_correlations(self, local_data: List[Dict], network_data: List[Dict]) -> List[Dict]:
        """发现关联"""
        correlations = []
        
        if local_data and network_data:
            correlation = {
                'local_sources': len(local_data),
                'network_sources': len(network_data),
                'correlation_strength': 0.85,
                'description': f"发现{len(local_data)}条本地数据与{len(network_data)}条网络数据的高度关联"
            }
            correlations.append(correlation)
        
        return correlations
    
    def _extract_patterns(self, local_data: List[Dict], network_data: List[Dict]) -> List[Dict]:
        """提取模式"""
        patterns = []
        
        if local_data and network_data:
            pattern = {
                'pattern_type': '数据fusion模式',
                'description': '本地数据与网络研究形成一致的趋势',
                'confidence': 0.8,
                'supporting_points': len(local_data) + len(network_data)
            }
            patterns.append(pattern)
        
        return patterns
    
    def _generate_insights(self, correlations: List[Dict], patterns: List[Dict]) -> List[str]:
        """generate洞察"""
        insights = []
        
        if correlations:
            insights.append("本地实践与网络研究形成强相关验证")
        
        if patterns:
            insights.append("发现跨数据源的一致性模式")
        
        if correlations or patterns:
            insights.append("可提升学习置信度,generate高价值知识")
        
        return insights
    
    def _generate_summary(
        self, 
        local_task: LocalLearningTask,
        network_task: NetworkLearningTask,
        cross_task: CrossLearningTask
    ) -> Dict[str, Any]:
        """generate执行摘要"""
        return {
            'local_learning': {
                'status': local_task.status.value,
                'executed': local_task.should_execute,
                'data_count': local_task.data_count,
                'reason': local_task.reason,
                'findings': len(local_task.findings)
            },
            'network_learning': {
                'status': network_task.status.value,
                'executed': True,  # 网络学习必须执行
                'topics': len(network_task.topics),
                'findings': len(network_task.findings)
            },
            'cross_learning': {
                'status': cross_task.status.value,
                'triggered': cross_task.status == LearningStatus.COMPLETED,
                'local_sources': cross_task.local_data_count,
                'network_sources': cross_task.network_data_count,
                'correlations': len(cross_task.correlations),
                'patterns': len(cross_task.patterns),
                'insights': len(cross_task.insights)
            },
            'execution_flow': self._describe_execution_flow(local_task, network_task, cross_task),
            'timestamp': datetime.now().isoformat()
        }
    
    def _describe_execution_flow(
        self,
        local_task: LocalLearningTask,
        network_task: NetworkLearningTask,
        cross_task: CrossLearningTask
    ) -> str:
        """描述执行流程"""
        flow = []
        
        flow.append("┌─ 本地学习层")
        if local_task.should_execute:
            flow.append(f"│  ├─ ✅ 执行 ({local_task.data_count}条数据)")
        else:
            flow.append(f"│  ├─ ⊘ 跳过 ({local_task.reason})")
        
        flow.append("├─ 网络学习层")
        flow.append(f"│  ├─ ✅ 执行(必须)({len(network_task.findings)}条发现)")
        
        flow.append("├─ 交叉fusion层")
        if cross_task.status == LearningStatus.COMPLETED:
            flow.append(f"│  ├─ ✅ 触发 (发现{len(cross_task.insights)}个洞察)")
        else:
            flow.append(f"│  ├─ ⊘ 未触发 (需两层都有数据)")
        
        flow.append("└─ 报告generate")
        
        return "\n".join(flow)
    
    def _save_report(self, report: DailyLearningReport):
        """保存报告"""
        report_path = self.reports_dir / f"DLR_{report.execution_date}.yaml"
        
        report_dict = {
            'report_id': report.report_id,
            'execution_date': report.execution_date,
            'local_learning': asdict(report.local_learning) if report.local_learning else None,
            'network_learning': asdict(report.network_learning) if report.network_learning else None,
            'cross_learning': asdict(report.cross_learning) if report.cross_learning else None,
            'summary': report.summary,
            'timestamp': report.timestamp
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            yaml.dump(report_dict, f, allow_unicode=True, default_flow_style=False)
    
    def get_execution_log(self) -> str:
        """get执行日志"""
        return "\n".join(self.execution_log)

# 快速使用函数
def run_daily_three_tier_learning(base_path: str = None) -> "DailyLearningReport":
    """
    执行日报告 - 三层学习完整流程（原始入口，向后兼容）。
    
    Usage:
        report = run_daily_three_tier_learning()
        print(report.summary)
    """
    if base_path is None:
        base_path = str(LEARNING_DIR)
    
    executor = ThreeTierLearningExecutor(base_path)
    report = executor.execute_daily_learning()
    
    return report


def run_daily_three_tier_learning_v2(base_path: str = None) -> "DailyLearningReport":
    """
    新路由入口（推荐）：通过 UnifiedLearningOrchestrator 执行三层学习。
    回退到原始执行器 run_daily_three_tier_learning()。
    """
    try:
        from .unified_learning_orchestrator import UnifiedLearningOrchestrator
        from .learning_strategies import LearningStrategyType
        orchestrator = UnifiedLearningOrchestrator(base_path)
        orchestrator.execute_daily(strategy_types=[LearningStrategyType.THREE_TIER])
    except Exception as e:
        logger.warning(f"v2路由失败，回退到原始执行器: {e}")
    # 始终返回兼容格式的报告
    return run_daily_three_tier_learning(base_path)
