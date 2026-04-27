"""
__all__ = [
    'plan_learning_data_selection',
    'run_learning_scheduler_v2',
    'save_schedule',
    'scan_data_sources',
    'set_local_threshold',
    'set_network_supplement_ratio',
    'set_strategy',
]

学习调度器 - Learning Scheduler
实现本地优先,网络补充的智能学习strategy

核心逻辑:
1. 本地优先:优先扫描和学习本地数据
2. 阈值检查:如果本地数据不足,自动启用网络学习
3. 混合学习:可选地同时使用本地和网络数据以优化学习质量
4. 灵活配置:支持自定义阈值和学习strategy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  兼容层说明（v2.0 统一重构后）
本文件保留原始实现以确保现有调用链 100% 兼容。
新代码请使用：
    from .unified_learning_orchestrator import UnifiedLearningOrchestrator
    orchestrator = UnifiedLearningOrchestrator()
    status = orchestrator.scan_data_sources()
    selection = orchestrator.plan_learning_data_selection()
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import logging
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# ── 枚举统一: 复用 unified_learning_orchestrator 的 SchedulerStrategyMode ──
# 为保持向后兼容, 保留 LearningStrategy 别名
try:
    from .unified_learning_orchestrator import SchedulerStrategyMode as LearningStrategy
except ImportError:
    # 回退: 如果统一编排器不可用, 使用本地定义
    class LearningStrategy(Enum):
        """学习策略"""
        LOCAL_ONLY = "本地只读"
        LOCAL_FIRST = "本地优先"
        LOCAL_NETWORK_HYBRID = "混合学习"
        NETWORK_ONLY = "网络只读"

logger = logging.getLogger(__name__)

class DataSource(Enum):
    """数据源类型"""
    LOCAL_FINDINGS = "本地发现"             # findings目录中的YAML文件
    LOCAL_VALIDATION = "本地验证"           # validation目录中的验证结果
    LOCAL_LEARNING = "本地学习事件"         # learning目录中已保存的学习事件
    NETWORK_RESEARCH = "网络研究"           # 网络搜索get的研究数据
    USER_INPUT = "用户输入"                 # 用户手动输入的数据

@dataclass
class DataSourceInfo:
    """数据源信息"""
    source_type: DataSource
    count: int                  # 数据条数
    quality_score: float        # 质量评分 (0-1)
    recency: int                # 最近数据距今(天)
    priority: int               # 优先级 (1=最高)

@dataclass
class LearningSchedule:
    """学习调度信息"""
    strategy: LearningStrategy
    local_threshold: int        # 本地数据不足的阈值
    network_supplement_ratio: float  # 网络数据补充比例
    max_local_data: int         # 单次使用的最大本地数据量
    max_network_data: int       # 单次使用的最大网络数据量
    quality_threshold: float    # 最低质量要求
    recency_threshold: int      # 最大允许的数据年龄(天)

class LearningScheduler:
    """学习调度器 - 管理本地优先,网络补充的学习strategy"""
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            from src.core.paths import PROJECT_ROOT
            base_path = str(PROJECT_ROOT)
        self.base_path = Path(base_path)
        self.config_path = self.base_path / "learning_schedule.yaml"
        
        # 默认学习调度
        self.default_schedule = LearningSchedule(
            strategy=LearningStrategy.LOCAL_FIRST,
            local_threshold=5,              # 本地数据少于5条时启用网络
            network_supplement_ratio=0.3,   # 网络数据不超过30%
            max_local_data=50,              # 单次最多用50条本地数据
            max_network_data=15,            # 单次最多补充15条网络数据
            quality_threshold=0.6,          # 质量评分不低于0.6
            recency_threshold=30            # 数据不超过30天
        )
        
        self.schedule = self._load_schedule()
        self.data_sources_info: Dict[DataSource, DataSourceInfo] = {}
    
    def _load_schedule(self) -> LearningSchedule:
        """加载学习调度配置"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if config:
                        return LearningSchedule(
                            strategy=LearningStrategy[config.get('strategy', 'LOCAL_FIRST')],
                            local_threshold=config.get('local_threshold', 5),
                            network_supplement_ratio=config.get('network_supplement_ratio', 0.3),
                            max_local_data=config.get('max_local_data', 50),
                            max_network_data=config.get('max_network_data', 15),
                            quality_threshold=config.get('quality_threshold', 0.6),
                            recency_threshold=config.get('recency_threshold', 30)
                        )
            except Exception as e:
                logger.warning(f"加载学习调度配置失败: {e},使用默认配置")
        
        return self.default_schedule
    
    def save_schedule(self, schedule: LearningSchedule = None):
        """保存学习调度配置"""
        if schedule is None:
            schedule = self.schedule
        
        config = {
            'strategy': schedule.strategy.name,
            'local_threshold': schedule.local_threshold,
            'network_supplement_ratio': schedule.network_supplement_ratio,
            'max_local_data': schedule.max_local_data,
            'max_network_data': schedule.max_network_data,
            'quality_threshold': schedule.quality_threshold,
            'recency_threshold': schedule.recency_threshold,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        self.schedule = schedule
        logger.info(f"学习调度已保存: {self.config_path}")
    
    def scan_data_sources(self) -> Dict[DataSource, DataSourceInfo]:
        """扫描所有可用的数据源"""
        sources_info = {}
        
        # 1. 扫描本地发现
        local_findings_count = self._count_local_findings()
        sources_info[DataSource.LOCAL_FINDINGS] = DataSourceInfo(
            source_type=DataSource.LOCAL_FINDINGS,
            count=local_findings_count,
            quality_score=0.85,         # 本地数据质量高
            recency=self._get_recency_days('findings'),
            priority=1                  # 最高优先级
        )
        
        # 2. 扫描本地验证结果
        local_validation_count = self._count_local_validation()
        sources_info[DataSource.LOCAL_VALIDATION] = DataSourceInfo(
            source_type=DataSource.LOCAL_VALIDATION,
            count=local_validation_count,
            quality_score=0.9,          # 验证结果质量最高
            recency=self._get_recency_days('validation'),
            priority=1                  # 最高优先级
        )
        
        # 3. 扫描本地学习事件
        local_learning_count = self._count_local_learning_events()
        sources_info[DataSource.LOCAL_LEARNING] = DataSourceInfo(
            source_type=DataSource.LOCAL_LEARNING,
            count=local_learning_count,
            quality_score=0.8,
            recency=self._get_recency_days('learning'),
            priority=2                  # 次优先级
        )
        
        # 4. 网络研究数据(如果存在)
        network_data_count = self._count_network_research()
        sources_info[DataSource.NETWORK_RESEARCH] = DataSourceInfo(
            source_type=DataSource.NETWORK_RESEARCH,
            count=network_data_count,
            quality_score=0.7,          # 网络数据质量相对较低
            recency=self._get_recency_days('findings', prefix='NET_'),
            priority=3                  # 较低优先级
        )
        
        self.data_sources_info = sources_info
        return sources_info
    
    def plan_learning_data_selection(self) -> Dict:
        """
        根据学习strategy规划数据选择
        
        Returns:
            {
                'strategy': 学习strategy,
                'local_data': 本地数据列表,
                'network_data': 网络数据列表,
                'total_data': 总数据条数,
                'data_source_breakdown': 数据源分布,
                'recommendations': 学习建议
            }
        """
        # 扫描数据源
        self.scan_data_sources()
        
        local_data = []
        network_data = []
        recommendations = []
        
        # 收集本地数据
        local_findings = self._load_local_findings()
        local_validations = self._load_local_validation()
        local_learning = self._load_local_learning_events()
        
        local_data = local_findings + local_validations + local_learning
        local_data = local_data[:self.schedule.max_local_data]
        
        # 根据strategy决定是否使用网络数据
        if self.schedule.strategy == LearningStrategy.LOCAL_ONLY:
            # 仅使用本地数据
            pass
        
        elif self.schedule.strategy == LearningStrategy.LOCAL_FIRST:
            # 本地优先:如果本地数据不足,补充网络数据
            if len(local_data) < self.schedule.local_threshold:
                network_data = self._load_network_research()
                supplement_count = int(len(local_data) * self.schedule.network_supplement_ratio)
                network_data = network_data[:supplement_count]
                recommendations.append(
                    f"🌐 本地数据({len(local_data)})不足({self.schedule.local_threshold}),"
                    f"已补充{len(network_data)}条网络数据"
                )
            else:
                recommendations.append(
                    f"✅ 本地数据充足({len(local_data)}),无需网络补充"
                )
        
        elif self.schedule.strategy == LearningStrategy.LOCAL_NETWORK_HYBRID:
            # 混合学习:同时使用本地和网络数据优化学习
            network_data = self._load_network_research()
            supplement_count = max(
                int(len(local_data) * self.schedule.network_supplement_ratio),
                min(5, self.schedule.max_network_data)
            )
            network_data = network_data[:supplement_count]
            recommendations.append(
                f"🔄 混合学习: 本地{len(local_data)}条 + 网络{len(network_data)}条"
            )
        
        elif self.schedule.strategy == LearningStrategy.NETWORK_ONLY:
            # 仅使用网络数据
            local_data = []
            network_data = self._load_network_research()[:self.schedule.max_network_data]
            recommendations.append("🌐 仅使用网络数据进行学习")
        
        # generate数据源分布统计
        total_count = len(local_data) + len(network_data)
        data_source_breakdown = {
            "本地数据": len(local_data),
            "网络数据": len(network_data),
            "总计": total_count,
            "本地占比": f"{len(local_data)/max(total_count,1)*100:.1f}%" if total_count > 0 else "0%"
        }
        
        return {
            'strategy': self.schedule.strategy.value,
            'local_data': local_data,
            'network_data': network_data,
            'total_data': len(local_data) + len(network_data),
            'data_source_breakdown': data_source_breakdown,
            'data_sources_info': self._format_sources_info(),
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    def _count_local_findings(self) -> int:
        """统计本地发现数量"""
        findings_path = self.base_path / "findings"
        if not findings_path.exists():
            return 0
        return len([f for f in findings_path.glob("*.yaml") 
                   if not f.name.startswith("NET_")])
    
    def _count_local_validation(self) -> int:
        """统计本地验证结果数量"""
        validation_path = self.base_path / "validation"
        if not validation_path.exists():
            return 0
        return len(list(validation_path.glob("*.yaml")))
    
    def _count_local_learning_events(self) -> int:
        """统计本地学习事件数量"""
        learning_path = self.base_path / "learning"
        if not learning_path.exists():
            return 0
        return len(list(learning_path.glob("LE_*.yaml")))
    
    def _count_network_research(self) -> int:
        """统计网络研究数据数量"""
        findings_path = self.base_path / "findings"
        if not findings_path.exists():
            return 0
        return len([f for f in findings_path.glob("NET_*.yaml")])
    
    def _get_recency_days(self, dir_name: str, prefix: str = "") -> int:
        """get最近数据距离今天的天数"""
        target_path = self.base_path / dir_name
        if not target_path.exists():
            return 999
        
        try:
            files = list(target_path.glob(f"{prefix}*.yaml"))
            if not files:
                return 999
            
            # 按修改时间排序,get最新文件
            latest_file = max(files, key=lambda f: f.stat().st_mtime)
            mtime = datetime.fromtimestamp(latest_file.stat().st_mtime)
            days_diff = (datetime.now() - mtime).days
            return max(0, days_diff)
        except (OSError, IOError, PermissionError):
            return 999
    
    def _load_local_findings(self) -> List[Dict]:
        """加载本地发现数据"""
        findings_path = self.base_path / "findings"
        findings = []
        
        if findings_path.exists():
            for file_path in findings_path.glob("*.yaml"):
                if not file_path.name.startswith("NET_"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = yaml.safe_load(f)
                            if data:
                                data['_source'] = 'local_finding'
                                findings.append(data)
                    except Exception as e:
                        logger.warning(f"读取本地发现失败 {file_path}: {e}")
        
        return findings
    
    def _load_local_validation(self) -> List[Dict]:
        """加载本地验证结果"""
        validation_path = self.base_path / "validation"
        validations = []
        
        if validation_path.exists():
            for file_path in validation_path.glob("*.yaml"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data:
                            data['_source'] = 'local_validation'
                            validations.append(data)
                except Exception as e:
                    logger.warning(f"读取本地验证失败 {file_path}: {e}")
        
        return validations
    
    def _load_local_learning_events(self) -> List[Dict]:
        """加载本地学习事件"""
        learning_path = self.base_path / "learning"
        events = []
        
        if learning_path.exists():
            for file_path in learning_path.glob("LE_*.yaml"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data:
                            data['_source'] = 'local_learning'
                            events.append(data)
                except Exception as e:
                    logger.warning(f"读取学习事件失败 {file_path}: {e}")
        
        return events
    
    def _load_network_research(self) -> List[Dict]:
        """加载网络研究数据"""
        findings_path = self.base_path / "findings"
        research = []
        
        if findings_path.exists():
            for file_path in findings_path.glob("NET_*.yaml"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data:
                            data['_source'] = 'network_research'
                            research.append(data)
                except Exception as e:
                    logger.warning(f"读取网络研究失败 {file_path}: {e}")
        
        return research
    
    def _format_sources_info(self) -> List[Dict]:
        """格式化数据源信息用于输出"""
        result = []
        for source_type in [DataSource.LOCAL_FINDINGS, DataSource.LOCAL_VALIDATION, 
                          DataSource.LOCAL_LEARNING, DataSource.NETWORK_RESEARCH]:
            info = self.data_sources_info.get(source_type)
            if info:
                result.append({
                    '数据源': info.source_type.value,
                    '数据条数': info.count,
                    '质量评分': f"{info.quality_score:.1%}",
                    '最近数据': f"{info.recency}天前",
                    '优先级': f"P{info.priority}"
                })
        return result
    
    def set_strategy(self, strategy: LearningStrategy):
        """设置学习strategy"""
        self.schedule.strategy = strategy
        self.save_schedule()
        logger.info(f"学习strategy已设置为: {strategy.value}")
    
    def set_local_threshold(self, threshold: int):
        """设置本地数据不足的阈值"""
        self.schedule.local_threshold = threshold
        self.save_schedule()
        logger.info(f"本地数据阈值已设置为: {threshold}")
    
    def set_network_supplement_ratio(self, ratio: float):
        """设置网络数据补充比例"""
        if 0 <= ratio <= 1:
            self.schedule.network_supplement_ratio = ratio
            self.save_schedule()
            logger.info(f"网络补充比例已设置为: {ratio:.1%}")
        else:
            logger.error("比例必须在0-1之间")

# ─── v2.0 兼容路由 ───────────────────────────────────────────────────
def run_learning_scheduler_v2(base_path: str = None):
    """
    新路由入口（推荐）：通过 UnifiedLearningOrchestrator 使用调度功能。
    保留 LearningScheduler 类原有接口不变。
    """
    try:
        from .unified_learning_orchestrator import UnifiedLearningOrchestrator
        orchestrator = UnifiedLearningOrchestrator(base_path)
        sources = orchestrator.scan_data_sources()
        selection = orchestrator.plan_learning_data_selection()
        return {"data_sources": sources, "learning_plan": selection}
    except Exception as e:
        logger.warning(f"v2路由失败，回退到原始调度器: {e}")
        scheduler = LearningScheduler(base_path)
        scheduler.scan_data_sources()
        return scheduler.plan_learning_data_selection()
