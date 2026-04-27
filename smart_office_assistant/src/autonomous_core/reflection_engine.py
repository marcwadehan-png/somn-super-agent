"""
__all__ = [
    'add_reflection',
    'complete',
    'complete_execution',
    'extract_patterns',
    'fail_execution',
    'from_dict',
    'generate_report',
    'generate_strategy_suggestions',
    'get_failed_records',
    'get_recent_records',
    'get_record',
    'get_relevant_patterns',
    'get_statistics',
    'start_execution',
    'to_dict',
]

执行-观察-反思闭环 - Execution-Reflection Loop

实现智能体的自我改进能力:
- action执行记录
- 结果观察与评估
- 反思与总结
- strategy调整建议
- 经验积累
"""

import json
import uuid
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

class ActionType(Enum):
    """action类型"""
    ANALYSIS = "analysis"           # 分析
    GENERATION = "generation"       # generate
    LEARNING = "learning"           # 学习
    DECISION = "decision"           # decision
    COMMUNICATION = "communication" # 沟通
    TOOL_USE = "tool_use"           # 工具使用
    PLANNING = "planning"           # 规划
    REFLECTION = "reflection"       # 反思

class OutcomeStatus(Enum):
    """结果状态"""
    SUCCESS = "success"             # 成功
    PARTIAL = "partial"             # 部分成功
    FAILURE = "failure"             # 失败
    UNKNOWN = "unknown"             # 未知

@dataclass
class ExecutionRecord:
    """执行记录"""
    # 基本信息
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    action_type: ActionType = ActionType.ANALYSIS
    
    # action描述
    action_name: str = ""
    action_description: str = ""
    action_params: Dict[str, Any] = field(default_factory=dict)
    
    # 执行上下文
    context_before: Dict[str, Any] = field(default_factory=dict)
    goal_id: Optional[str] = None
    task_id: Optional[str] = None
    
    # 执行结果
    outcome_status: OutcomeStatus = OutcomeStatus.UNKNOWN
    outcome_description: str = ""
    outcome_data: Dict[str, Any] = field(default_factory=dict)
    
    # 时间记录
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    duration_seconds: float = 0.0
    
    # 评估
    expected_outcome: str = ""
    actual_outcome: str = ""
    deviation: str = ""  # 偏差分析
    
    # 反思
    reflection: str = ""
    lessons_learned: List[str] = field(default_factory=list)
    improvement_suggestions: List[str] = field(default_factory=list)
    
    # 元数据
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'action_type': self.action_type.value,
            'action_name': self.action_name,
            'action_description': self.action_description,
            'action_params': self.action_params,
            'context_before': self.context_before,
            'goal_id': self.goal_id,
            'task_id': self.task_id,
            'outcome_status': self.outcome_status.value,
            'outcome_description': self.outcome_description,
            'outcome_data': self.outcome_data,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'duration_seconds': self.duration_seconds,
            'expected_outcome': self.expected_outcome,
            'actual_outcome': self.actual_outcome,
            'deviation': self.deviation,
            'reflection': self.reflection,
            'lessons_learned': self.lessons_learned,
            'improvement_suggestions': self.improvement_suggestions,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ExecutionRecord':
        """从字典创建"""
        return cls(
            id=data.get('id', str(uuid.uuid4())[:8]),
            action_type=ActionType(data.get('action_type', 'analysis')),
            action_name=data.get('action_name', ''),
            action_description=data.get('action_description', ''),
            action_params=data.get('action_params', {}),
            context_before=data.get('context_before', {}),
            goal_id=data.get('goal_id'),
            task_id=data.get('task_id'),
            outcome_status=OutcomeStatus(data.get('outcome_status', 'unknown')),
            outcome_description=data.get('outcome_description', ''),
            outcome_data=data.get('outcome_data', {}),
            started_at=data.get('started_at', datetime.now().isoformat()),
            completed_at=data.get('completed_at'),
            duration_seconds=data.get('duration_seconds', 0.0),
            expected_outcome=data.get('expected_outcome', ''),
            actual_outcome=data.get('actual_outcome', ''),
            deviation=data.get('deviation', ''),
            reflection=data.get('reflection', ''),
            lessons_learned=data.get('lessons_learned', []),
            improvement_suggestions=data.get('improvement_suggestions', []),
            tags=data.get('tags', [])
        )
    
    def complete(self, outcome_status: OutcomeStatus, outcome_description: str = ""):
        """完成记录"""
        self.outcome_status = outcome_status
        self.outcome_description = outcome_description
        self.completed_at = datetime.now().isoformat()
        
        # 计算持续时间
        try:
            started = datetime.fromisoformat(self.started_at)
            completed = datetime.fromisoformat(self.completed_at)
            self.duration_seconds = (completed - started).total_seconds()
        except Exception:
            pass  # self.duration_seconds = (completed - started).total_seconds(失败时静默忽略

@dataclass
class ReflectionPattern:
    """反思模式 - 从经验中提取的模式"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    # 模式描述
    pattern_name: str = ""
    description: str = ""
    
    # 触发条件
    trigger_conditions: List[str] = field(default_factory=list)
    action_type: Optional[ActionType] = None
    
    # 模式内容
    what_worked: List[str] = field(default_factory=list)      # 什么有效
    what_failed: List[str] = field(default_factory=list)      # 什么无效
    what_uncertain: List[str] = field(default_factory=list)   # 什么不确定
    
    # 证据
    supporting_records: List[str] = field(default_factory=list)  # 支持该模式的记录ID
    confidence: float = 0.5  # 置信度 0-1
    
    # 时间
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    occurrence_count: int = 0  # 出现次数
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'pattern_name': self.pattern_name,
            'description': self.description,
            'trigger_conditions': self.trigger_conditions,
            'action_type': self.action_type.value if self.action_type else None,
            'what_worked': self.what_worked,
            'what_failed': self.what_failed,
            'what_uncertain': self.what_uncertain,
            'supporting_records': self.supporting_records,
            'confidence': self.confidence,
            'created_at': self.created_at,
            'last_updated': self.last_updated,
            'occurrence_count': self.occurrence_count
        }

class ReflectionEngine:
    """
    反思引擎 - 实现执行-观察-反思闭环
    
    核心功能:
    1. 执行记录追踪
    2. 结果评估
    3. 反思generate
    4. 模式提取
    5. strategy调整建议
    """
    
    def __init__(self, storage_path: str = "data/reflection"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # 执行记录存储
        self._records: Dict[str, ExecutionRecord] = {}
        self._patterns: Dict[str, ReflectionPattern] = {}
        
        # 当前活跃记录
        self._active_records: Dict[str, ExecutionRecord] = {}
        
        # 加载已有数据
        self._load_data()
        
        logger.info(f"反思引擎init完成,已加载 {len(self._records)} 条记录,{len(self._patterns)} 个模式")
    
    def _load_data(self):
        """加载数据（空文件/损坏时优雅降级）"""
        # 加载执行记录
        records_file = self.storage_path / "execution_records.json"
        if records_file.exists():
            try:
                with open(records_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if not content:
                    logger.info("execution_records.json 为空，初始化为空记录列表")
                else:
                    data = json.loads(content)
                    for record_data in data.get('records', []):
                        record = ExecutionRecord.from_dict(record_data)
                        self._records[record.id] = record
            except json.JSONDecodeError as e:
                logger.warning(f"execution_records.json 格式损坏 ({e})，初始化为空记录列表")
            except Exception as e:
                logger.warning(f"加载执行记录失败 ({e})，初始化为空记录列表")

        # 加载反思模式
        patterns_file = self.storage_path / "reflection_patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if not content:
                    logger.info("reflection_patterns.json 为空，初始化为空模式列表")
                else:
                    data = json.loads(content)
                    for pattern_data in data.get('patterns', []):
                        pattern = ReflectionPattern(
                            id=pattern_data['id'],
                            pattern_name=pattern_data['pattern_name'],
                            description=pattern_data.get('description', ''),
                            trigger_conditions=pattern_data.get('trigger_conditions', []),
                            action_type=ActionType(pattern_data['action_type']) if pattern_data.get('action_type') else None,
                            what_worked=pattern_data.get('what_worked', []),
                            what_failed=pattern_data.get('what_failed', []),
                            what_uncertain=pattern_data.get('what_uncertain', []),
                            supporting_records=pattern_data.get('supporting_records', []),
                            confidence=pattern_data.get('confidence', 0.5),
                            created_at=pattern_data.get('created_at'),
                            last_updated=pattern_data.get('last_updated'),
                            occurrence_count=pattern_data.get('occurrence_count', 0)
                        )
                        self._patterns[pattern.id] = pattern
            except json.JSONDecodeError as e:
                logger.warning(f"reflection_patterns.json 格式损坏 ({e})，初始化为空模式列表")
            except Exception as e:
                logger.warning(f"加载反思模式失败 ({e})，初始化为空模式列表")
    
    def _save_data(self):
        """保存数据"""
        # 保存执行记录
        records_file = self.storage_path / "execution_records.json"
        try:
            data = {
                'updated_at': datetime.now().isoformat(),
                'records': [record.to_dict() for record in self._records.values()]
            }
            with open(records_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存执行记录失败: {e}")
        
        # 保存反思模式
        patterns_file = self.storage_path / "reflection_patterns.json"
        try:
            data = {
                'updated_at': datetime.now().isoformat(),
                'patterns': [pattern.to_dict() for pattern in self._patterns.values()]
            }
            with open(patterns_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存反思模式失败: {e}")
    
    # ========== 执行记录 ==========
    
    def start_execution(
        self,
        action_type: ActionType,
        action_name: str,
        action_description: str = "",
        action_params: Optional[Dict] = None,
        context: Optional[Dict] = None,
        goal_id: Optional[str] = None,
        task_id: Optional[str] = None,
        expected_outcome: str = ""
    ) -> ExecutionRecord:
        """
        开始记录一次执行
        
        Returns:
            执行记录对象,用于后续完成
        """
        record = ExecutionRecord(
            action_type=action_type,
            action_name=action_name,
            action_description=action_description,
            action_params=action_params or {},
            context_before=context or {},
            goal_id=goal_id,
            task_id=task_id,
            expected_outcome=expected_outcome
        )
        
        self._active_records[record.id] = record
        
        logger.debug(f"开始执行记录: [{record.id}] {action_name}")
        return record
    
    def complete_execution(
        self,
        record_id: str,
        outcome_status: OutcomeStatus,
        outcome_description: str = "",
        outcome_data: Optional[Dict] = None,
        actual_outcome: str = ""
    ) -> Optional[ExecutionRecord]:
        """完成执行记录"""
        record = self._active_records.get(record_id)
        if not record:
            logger.warning(f"未找到活跃记录: {record_id}")
            return None
        
        # 完成记录
        record.complete(outcome_status, outcome_description)
        record.outcome_data = outcome_data or {}
        record.actual_outcome = actual_outcome
        
        # 计算偏差
        if record.expected_outcome and record.actual_outcome:
            if record.expected_outcome == record.actual_outcome:
                record.deviation = "符合预期"
            else:
                record.deviation = f"预期: {record.expected_outcome}, 实际: {record.actual_outcome}"
        
        # 保存到历史记录
        self._records[record.id] = record
        del self._active_records[record_id]
        
        self._save_data()
        
        logger.info(f"完成执行记录: [{record_id}] {record.action_name} -> {outcome_status.value}")
        
        # 自动触发反思
        self._auto_reflect(record)
        
        return record
    
    def fail_execution(
        self,
        record_id: str,
        error_message: str,
        outcome_data: Optional[Dict] = None
    ) -> Optional[ExecutionRecord]:
        """标记执行失败"""
        return self.complete_execution(
            record_id=record_id,
            outcome_status=OutcomeStatus.FAILURE,
            outcome_description=error_message,
            outcome_data=outcome_data
        )
    
    # ========== 反思generate ==========
    
    def _auto_reflect(self, record: ExecutionRecord):
        """自动反思 - 基于执行结果generate反思"""
        # 只有完成或失败的记录才需要反思
        if record.outcome_status not in [OutcomeStatus.SUCCESS, OutcomeStatus.FAILURE, OutcomeStatus.PARTIAL]:
            return
        
        # generate反思内容
        reflection_parts = []
        lessons = []
        suggestions = []
        
        if record.outcome_status == OutcomeStatus.SUCCESS:
            reflection_parts.append(f"成功完成了 {record.action_name}")
            lessons.append(f"{record.action_name} 的方法在当前情境下有效")
            suggestions.append(f"可以在类似情境下复用 {record.action_name} 的方法")
        
        elif record.outcome_status == OutcomeStatus.FAILURE:
            reflection_parts.append(f"{record.action_name} 未能成功执行")
            if record.outcome_description:
                reflection_parts.append(f"失败原因: {record.outcome_description}")
            lessons.append(f"{record.action_name} 在当前情境下存在问题")
            suggestions.append(f"需要改进 {record.action_name} 的方法或前置条件")
        
        elif record.outcome_status == OutcomeStatus.PARTIAL:
            reflection_parts.append(f"{record.action_name} 部分成功")
            lessons.append(f"{record.action_name} 的方法需要调整")
            suggestions.append(f"优化 {record.action_name} 以提高成功率")
        
        # 如果有偏差分析
        if record.deviation:
            reflection_parts.append(f"偏差分析: {record.deviation}")
        
        # 更新记录
        record.reflection = "\n".join(reflection_parts)
        record.lessons_learned = lessons
        record.improvement_suggestions = suggestions
        
        self._save_data()
        
        logger.debug(f"自动generate反思: [{record.id}]")
    
    def add_reflection(
        self,
        record_id: str,
        reflection: str,
        lessons: Optional[List[str]] = None,
        suggestions: Optional[List[str]] = None
    ) -> bool:
        """手动添加反思"""
        record = self._records.get(record_id)
        if not record:
            return False
        
        record.reflection = reflection
        if lessons:
            record.lessons_learned.extend(lessons)
        if suggestions:
            record.improvement_suggestions.extend(suggestions)
        
        self._save_data()
        return True
    
    # ========== 模式提取 ==========
    
    def extract_patterns(self, min_occurrences: int = 3) -> List[ReflectionPattern]:
        """
        从执行记录中提取反思模式
        
        Args:
            min_occurrences: 最小出现次数才形成模式
        
        Returns:
            提取的模式列表
        """
        patterns = []
        
        # 按action类型分组分析
        by_action_type: Dict[ActionType, List[ExecutionRecord]] = {}
        for record in self._records.values():
            if record.action_type not in by_action_type:
                by_action_type[record.action_type] = []
            by_action_type[record.action_type].append(record)
        
        for action_type, records in by_action_type.items():
            if len(records) < min_occurrences:
                continue
            
            # 分析成功/失败模式
            success_records = [r for r in records if r.outcome_status == OutcomeStatus.SUCCESS]
            failure_records = [r for r in records if r.outcome_status == OutcomeStatus.FAILURE]
            
            success_rate = len(success_records) / len(records)
            
            # 创建模式
            pattern = ReflectionPattern(
                pattern_name=f"{action_type.value}_模式",
                description=f"基于 {len(records)} 次 {action_type.value} action的分析",
                action_type=action_type,
                what_worked=[r.action_name for r in success_records[:5]],
                what_failed=[r.action_name for r in failure_records[:5]],
                supporting_records=[r.id for r in records],
                confidence=success_rate,
                occurrence_count=len(records)
            )
            
            patterns.append(pattern)
            self._patterns[pattern.id] = pattern
        
        self._save_data()
        
        logger.info(f"提取了 {len(patterns)} 个反思模式")
        return patterns
    
    def get_relevant_patterns(
        self,
        action_type: Optional[ActionType] = None,
        context: Optional[Dict] = None
    ) -> List[ReflectionPattern]:
        """get相关的反思模式"""
        patterns = list(self._patterns.values())
        
        # 按action类型过滤
        if action_type:
            patterns = [p for p in patterns if p.action_type == action_type]
        
        # [修复] 根据context过滤和排序
        if context:
            context_keywords = context.get("keywords", [])
            context_industry = context.get("industry", "")
            context_intent = context.get("intent", "")
            
            # 计算每个模式的上下文匹配度
            scored_patterns = []
            for p in patterns:
                score = 0
                # 检查触发条件匹配
                if context_keywords:
                    for kw in context_keywords:
                        if any(kw.lower() in tc.lower() for tc in p.trigger_conditions):
                            score += 2
                # 检查行业匹配
                if context_industry and context_industry in p.description:
                    score += 1
                # 检查意图匹配
                if context_intent and context_intent in p.pattern_name:
                    score += 3
                
                scored_patterns.append((p, score))
            
            # 按匹配度和置信度排序
            scored_patterns.sort(key=lambda x: (x[1], x[0].confidence), reverse=True)
            patterns = [p for p, _ in scored_patterns]
        else:
            # 按置信度排序
            patterns.sort(key=lambda p: p.confidence, reverse=True)
        
        return patterns
    
    def get_relevant_reflections(
        self,
        context: Optional[Dict] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        [新增] 获取与当前上下文相关的历史反思记录
        用于将历史反思结果应用到新学习任务
        
        Args:
            context: 当前上下文，包含keywords、industry、intent等
            limit: 返回数量限制
        
        Returns:
            相关反思记录列表
        """
        context = context or {}
        context_keywords = context.get("keywords", [])
        context_industry = context.get("industry", "")
        
        relevant_records = []
        
        for record in self._records.values():
            # 计算上下文匹配度
            score = 0
            
            # 检查action类型匹配
            action_type = context.get("action_type")
            if action_type and record.action_type.value == action_type:
                score += 2
            
            # 检查标签匹配
            if context_keywords:
                for kw in context_keywords:
                    if any(kw.lower() in tag.lower() for tag in record.tags):
                        score += 1
                    if kw.lower() in record.action_description.lower():
                        score += 1
            
            # 检查行业匹配 (如果记录中有相关上下文)
            if context_industry and context_industry in record.action_description:
                score += 1
            
            # 检查成功/失败状态
            if record.outcome_status == OutcomeStatus.SUCCESS:
                score += 1
            elif record.outcome_status == OutcomeStatus.FAILURE:
                score -= 1  # 失败记录降低优先级
            
            if score > 0:
                relevant_records.append({
                    "record_id": record.id,
                    "action_name": record.action_name,
                    "action_type": record.action_type.value,
                    "outcome": record.outcome_status.value,
                    "reflection": record.reflection,
                    "lessons_learned": record.lessons_learned,
                    "improvement_suggestions": record.improvement_suggestions,
                    "relevance_score": score,
                    "context_before": record.context_before
                })
        
        # 按相关度排序
        relevant_records.sort(key=lambda x: x["relevance_score"], reverse=True)
        return relevant_records[:limit]
    
    # ========== strategy建议 ==========
    
    def generate_strategy_suggestions(
        self,
        action_type: ActionType,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        基于历史经验generatestrategy建议
        
        Returns:
            strategy建议字典
        """
        # get相关记录
        relevant_records = [
            r for r in self._records.values()
            if r.action_type == action_type
        ]
        
        if not relevant_records:
            return {
                'has_history': False,
                'suggestion': "没有相关历史记录,建议谨慎尝试"
            }
        
        # 统计分析
        total = len(relevant_records)
        success = len([r for r in relevant_records if r.outcome_status == OutcomeStatus.SUCCESS])
        failure = len([r for r in relevant_records if r.outcome_status == OutcomeStatus.FAILURE])
        partial = len([r for r in relevant_records if r.outcome_status == OutcomeStatus.PARTIAL])
        
        success_rate = success / total if total > 0 else 0
        
        # 收集建议
        all_suggestions = []
        for r in relevant_records:
            all_suggestions.extend(r.improvement_suggestions)
        
        # 统计最常见的建议
        suggestion_counts = {}
        for s in all_suggestions:
            suggestion_counts[s] = suggestion_counts.get(s, 0) + 1
        
        top_suggestions = sorted(
            suggestion_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            'has_history': True,
            'total_attempts': total,
            'success_rate': success_rate,
            'success_count': success,
            'failure_count': failure,
            'partial_count': partial,
            'confidence': success_rate,
            'top_suggestions': [s[0] for s in top_suggestions],
            'recommendation': self._generate_recommendation(success_rate, total)
        }
    
    def _generate_recommendation(self, success_rate: float, total: int) -> str:
        """generate建议文本"""
        if total < 3:
            return "历史数据不足,建议小规模试验"
        
        if success_rate >= 0.8:
            return "历史成功率很高,可以 confidently 执行"
        elif success_rate >= 0.5:
            return "历史成功率一般,建议准备备选方案"
        else:
            return "历史成功率较低,建议重新评估方法或寻求改进"
    
    # ========== 查询接口 ==========
    
    def get_record(self, record_id: str) -> Optional[ExecutionRecord]:
        """get执行记录"""
        return self._records.get(record_id)
    
    def get_recent_records(
        self,
        action_type: Optional[ActionType] = None,
        limit: int = 10
    ) -> List[ExecutionRecord]:
        """get最近的执行记录"""
        records = list(self._records.values())
        
        if action_type:
            records = [r for r in records if r.action_type == action_type]
        
        # 按时间排序
        records.sort(key=lambda r: r.started_at, reverse=True)
        
        return records[:limit]
    
    def get_failed_records(self, limit: int = 10) -> List[ExecutionRecord]:
        """get失败的记录"""
        records = [
            r for r in self._records.values()
            if r.outcome_status == OutcomeStatus.FAILURE
        ]
        records.sort(key=lambda r: r.started_at, reverse=True)
        return records[:limit]
    
    # ========== 统计与报告 ==========
    
    def get_statistics(self) -> Dict[str, Any]:
        """get反思引擎统计"""
        total_records = len(self._records)
        total_patterns = len(self._patterns)
        
        by_status = {status.value: 0 for status in OutcomeStatus}
        for record in self._records.values():
            by_status[record.outcome_status.value] += 1
        
        by_action = {action.value: 0 for action in ActionType}
        for record in self._records.values():
            by_action[record.action_type.value] += 1
        
        # 计算平均执行时间
        durations = [
            r.duration_seconds for r in self._records.values()
            if r.duration_seconds > 0
        ]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            'total_records': total_records,
            'total_patterns': total_patterns,
            'active_records': len(self._active_records),
            'by_status': by_status,
            'by_action': by_action,
            'avg_duration': avg_duration,
            'success_rate': by_status.get('success', 0) / total_records if total_records > 0 else 0
        }
    
    def generate_report(self) -> str:
        """generate反思引擎报告"""
        stats = self.get_statistics()
        
        report = f"""
# 执行-反思闭环报告

## 统计概览
- 总执行记录: {stats['total_records']}
- 活跃记录: {stats['active_records']}
- 反思模式: {stats['total_patterns']}
- 成功率: {stats['success_rate']:.1%}
- 平均执行时间: {stats['avg_duration']:.1f}秒

## 结果分布
- 成功: {stats['by_status'].get('success', 0)}
- 部分成功: {stats['by_status'].get('partial', 0)}
- 失败: {stats['by_status'].get('failure', 0)}
- 未知: {stats['by_status'].get('unknown', 0)}

## action类型分布
"""
        for action_type, count in sorted(stats['by_action'].items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                report += f"- {action_type}: {count}\n"
        
        report += "\n## 最近失败的执行\n"
        for record in self.get_failed_records(5):
            report += f"- [{record.id}] {record.action_name}: {record.outcome_description[:50]}...\n"
        
        report += "\n## 已提取的模式\n"
        for pattern in list(self._patterns.values())[:5]:
            report += f"- [{pattern.id}] {pattern.pattern_name} (置信度: {pattern.confidence:.1%})\n"
        
        return report
