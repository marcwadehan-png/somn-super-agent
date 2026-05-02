"""
神政轨 - 监管引擎系统
=====================

包含:
1. 锦督促引擎 (JinDuCuJinEngine) - 进度监督、节点催促
2. 行政之鞭引擎 (AdministrativeWhipEngine) - 惩罚机制、问责追踪

版本: v1.1.0
更新: 2026-04-28（v2.4.0 快速加载：共享Factory，消除冗余实例化）

快速加载优化:
- 工厂实例注入: 工程不自己创建 SupervisionClawFactory，由外部注入共享实例
- 消除冗余: 从3个独立Factory(18个WiseoneClaw) → 1个共享Factory(6个WiseoneClaw)
- _archive_punishment: 使用注入的factory而非每次新建
"""

import logging
import uuid
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from ._supervision_claws import (
    SupervisionLevel,
    SupervisionType,
    PunishmentType,
    SupervisionRecord,
    SupervisionClawFactory,
    SupervisionClaw,
)

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════════════
# 锦督促引擎
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class DeadlineNode:
    """截止节点"""
    id: str
    task_id: str
    target_claw: str
    description: str
    deadline: datetime
    urgency_level: int  # 1-5, 越高越紧急
    status: str = "pending"  # pending/running/completed/delayed
    reminder_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)


class JinDuCuJinEngine:
    """
    锦督促引擎 - 进度监督核心
    
    职责:
    1. 管理任务截止节点
    2. 自动检测进度延误
    3. 分级催促机制
    4. 存档催促记录
    
    催促等级:
    - L1: 温和提醒 (提前1小时)
    - L2: 正常催促 (提前30分钟)
    - L3: 严厉质问 (提前10分钟)
    - L4: 极限施压 (到期前5分钟)
    - L5: 执行问责 (已超时)
    """
    
    def __init__(self, factory: Optional[SupervisionClawFactory] = None):
        self.nodes: Dict[str, DeadlineNode] = {}
        self.records: List[SupervisionRecord] = []
        # v1.1: 共享Factory（避免冗余实例化）
        self.factory = factory if factory is not None else SupervisionClawFactory()
        
        logger.info("[锦督促引擎] 初始化完成")
    
    def register_deadline(
        self,
        task_id: str,
        target_claw: str,
        description: str,
        deadline: datetime,
        urgency_level: int = 3,
    ) -> str:
        """
        注册截止节点
        
        Args:
            task_id: 任务ID
            target_claw: 目标Claw
            description: 节点描述
            deadline: 截止时间
            urgency_level: 紧急程度(1-5)
            
        Returns:
            节点ID
        """
        node_id = str(uuid.uuid4())[:8]
        
        node = DeadlineNode(
            id=node_id,
            task_id=task_id,
            target_claw=target_claw,
            description=description,
            deadline=deadline,
            urgency_level=urgency_level,
        )
        
        self.nodes[node_id] = node
        logger.info(f"[锦督促] 注册节点: {description} | 截止: {deadline} | 目标: {target_claw}")
        
        return node_id
    
    def check_deadlines(self, current_time: Optional[datetime] = None) -> List[SupervisionRecord]:
        """
        检查所有截止节点，生成催促记录
        
        Args:
            current_time: 当前时间，默认now
            
        Returns:
            生成的监管记录列表
        """
        current_time = current_time or datetime.now()
        records = []
        
        for node_id, node in self.nodes.items():
            if node.status == "completed":
                continue
            
            time_diff = (node.deadline - current_time).total_seconds()
            
            # 确定催促等级
            level = self._determine_urgency_level(time_diff, node.urgency_level)
            
            if level and level != SupervisionLevel.MILD:
                # 生成催促
                message = self._generate_reminder_message(node, time_diff, level)
                
                record = SupervisionRecord(
                    timestamp=datetime.now().isoformat(),
                    claw_name="锦督促引擎",
                    position="progress",
                    target=node.target_claw,
                    action="urge",
                    level=level.value,
                    thinking_chain=[],
                    result={"message": message},
                )
                
                records.append(record)
                self.records.append(record)
                node.reminder_count += 1
                
                logger.warning(f"[锦督促] {node.target_claw}: {message}")
            
            # 检查是否超时
            if time_diff < 0 and node.status != "completed":
                node.status = "delayed"
        
        return records
    
    def _determine_urgency_level(self, time_diff_seconds: float, urgency: int) -> Optional[SupervisionLevel]:
        """根据时间差确定催促等级"""
        minutes = time_diff_seconds / 60
        
        if minutes > 60:  # 超过1小时
            return None  # 不催促
        elif minutes > 30:
            return SupervisionLevel.MILD
        elif minutes > 10:
            return SupervisionLevel.NORMAL
        elif minutes > 5:
            return SupervisionLevel.HARSH
        elif minutes > 0:
            return SupervisionLevel.EXTREME
        else:
            return SupervisionLevel.EXECUTION
    
    def _generate_reminder_message(self, node: DeadlineNode, time_diff: float, 
                                   level: SupervisionLevel) -> str:
        """生成催促消息"""
        minutes = abs(time_diff) / 60
        
        base = f"【锦督促】{node.target_claw}！任务「{node.description}」"
        
        if time_diff < 0:
            return f"{base}已超时 {minutes:.0f} 分钟！立即处理！"
        
        if level == SupervisionLevel.MILD:
            return f"{base}还有 {minutes:.0f} 分钟，注意把握时间"
        elif level == SupervisionLevel.NORMAL:
            return f"{base}仅剩 {minutes:.0f} 分钟，加快进度！"
        elif level == SupervisionLevel.HARSH:
            return f"{base}只剩 {minutes:.0f} 分钟！还不快点？！"
        elif level == SupervisionLevel.EXTREME:
            return f"{base}最后 {minutes:.0f} 分钟！再磨蹭问责！"
        else:
            return f"{base}已超时 {minutes:.0f} 分钟！问责处理！"
    
    def mark_completed(self, node_id: str) -> bool:
        """标记节点完成"""
        if node_id in self.nodes:
            self.nodes[node_id].status = "completed"
            logger.info(f"[锦督促] 节点 {node_id} 已完成")
            return True
        return False
    
    def get_pending_nodes(self) -> List[DeadlineNode]:
        """获取待处理节点"""
        return [n for n in self.nodes.values() if n.status == "pending"]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = len(self.nodes)
        completed = len([n for n in self.nodes.values() if n.status == "completed"])
        delayed = len([n for n in self.nodes.values() if n.status == "delayed"])
        pending = len([n for n in self.nodes.values() if n.status == "pending"])
        
        return {
            "total_nodes": total,
            "completed": completed,
            "delayed": delayed,
            "pending": pending,
            "total_reminders": sum(n.reminder_count for n in self.nodes.values()),
        }


# ══════════════════════════════════════════════════════════════════════════════
# 行政之鞭引擎
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PunishmentRecord:
    """惩罚记录"""
    id: str
    target_claw: str
    target_task: str
    punishment_type: PunishmentType
    reason: str
    severity: int  # 1-5
    created_at: datetime = field(default_factory=datetime.now)
    executed: bool = False
    executed_at: Optional[datetime] = None


class AdministrativeWhipEngine:
    """
    行政之鞭引擎 - 惩罚问责核心
    
    职责:
    1. 记录违规行为
    2. 执行惩罚措施
    3. 追踪问责链条
    4. 存档惩罚记录
    
    惩罚机制:
    - WARNING: 口头警告，记录在案
    - CRITICISM: 书面批评，纳入绩效
    - LOGGING: 行为日志，重点监控
    - PUBLIC_SHAME: 公开问责，全员通报
    - ESCALATION: 升级处理，上级介入
    - SUSPENSION: 暂停权限，直至整改
    
    累积惩罚:
    - 3次 WARNING → 升级为 CRITICISM
    - 3次 CRITICISM → 升级为 LOGGING
    - 3次 LOGGING → 升级为 PUBLIC_SHAME
    - PUBLIC_SHAME → ESCALATION
    - ESCALATION后再次违规 → SUSPENSION
    """
    
    def __init__(self, factory: Optional[SupervisionClawFactory] = None):
        self.punishments: Dict[str, List[PunishmentRecord]] = {}  # claw_id -> records
        self.escalation_chain: Dict[str, int] = {}  # claw_id -> escalation_count
        # v1.1: 共享Factory（避免冗余实例化）
        self.factory = factory if factory is not None else SupervisionClawFactory()
        
        # 惩罚计数器
        self.warning_count: Dict[str, int] = {}
        self.criticism_count: Dict[str, int] = {}
        self.logging_count: Dict[str, int] = {}
        
        logger.info("[行政之鞭引擎] 初始化完成")
    
    def punish(
        self,
        target_claw: str,
        target_task: str,
        reason: str,
        punishment: PunishmentType = PunishmentType.WARNING,
        severity: int = 1,
    ) -> PunishmentRecord:
        """
        执行惩罚
        
        Args:
            target_claw: 目标Claw
            target_task: 关联任务
            reason: 惩罚原因
            punishment: 惩罚类型
            severity: 严重程度(1-5)
            
        Returns:
            惩罚记录
        """
        record = PunishmentRecord(
            id=str(uuid.uuid4()),
            target_claw=target_claw,
            target_task=target_task,
            punishment_type=punishment,
            reason=reason,
            severity=severity,
        )
        
        # 记录惩罚
        if target_claw not in self.punishments:
            self.punishments[target_claw] = []
        self.punishments[target_claw].append(record)
        
        # 更新计数器
        self._update_counters(target_claw, punishment)
        
        # 检查是否需要升级
        upgraded = self._check_escalation(target_claw)
        if upgraded:
            record.punishment_type = upgraded
            record.reason = f"[升级] {reason}"
        
        # 执行惩罚
        self._execute_punishment(record)
        
        logger.warning(f"[行政之鞭] {target_claw}: {punishment.value} | {reason}")
        
        return record
    
    def _update_counters(self, claw_id: str, punishment: PunishmentType):
        """更新惩罚计数器"""
        if punishment == PunishmentType.WARNING:
            self.warning_count[claw_id] = self.warning_count.get(claw_id, 0) + 1
        elif punishment == PunishmentType.CRITICISM:
            self.criticism_count[claw_id] = self.criticism_count.get(claw_id, 0) + 1
        elif punishment == PunishmentType.LOGGING:
            self.logging_count[claw_id] = self.logging_count.get(claw_id, 0) + 1
    
    def _check_escalation(self, claw_id: str) -> Optional[PunishmentType]:
        """检查是否需要升级惩罚"""
        # WARNING累积
        if self.warning_count.get(claw_id, 0) >= 3:
            self.warning_count[claw_id] = 0
            return PunishmentType.CRITICISM
        
        # CRITICISM累积
        if self.criticism_count.get(claw_id, 0) >= 3:
            self.criticism_count[claw_id] = 0
            return PunishmentType.LOGGING
        
        # LOGGING累积
        if self.logging_count.get(claw_id, 0) >= 3:
            self.logging_count[claw_id] = 0
            return PunishmentType.PUBLIC_SHAME
        
        return None
    
    def _execute_punishment(self, record: PunishmentRecord):
        """执行惩罚"""
        record.executed = True
        record.executed_at = datetime.now()
        
        message = self._generate_punishment_message(record)
        
        # 存档
        self._archive_punishment(record, message)
    
    def _generate_punishment_message(self, record: PunishmentRecord) -> str:
        """生成惩罚消息"""
        target = record.target_claw
        punishment = record.punishment_type.value
        reason = record.reason
        severity = "★" * record.severity
        
        messages = {
            PunishmentType.WARNING: f"【警告】{target}：{reason} {severity}",
            PunishmentType.CRITICISM: f"【批评】{target}：{reason} {severity}，纳入绩效档案",
            PunishmentType.LOGGING: f"【记录】{target}：{reason} {severity}，重点监控中",
            PunishmentType.PUBLIC_SHAME: f"【通报】{target}：{reason} {severity}！全员知悉！",
            PunishmentType.ESCALATION: f"【升级】{target}：{reason}，上报处理！",
            PunishmentType.SUSPENSION: f"【停权】{target}：{reason}，权限已暂停！",
        }
        
        return messages.get(record.punishment_type, f"【惩罚】{target}：{reason}")
    
    def _archive_punishment(self, record: PunishmentRecord, message: str):
        """存档惩罚记录"""
        # v1.1: 使用已注入的共享factory，而非每次新建
        try:
            claw = self.factory.get_claw("performance")
            if claw:
                # 记录到思考链（替代store_to_memory）
                claw.thinking_chain.append(f"[存档] {message}")
                logger.info(f"[行政之鞭] 存档: {message}")
        except Exception as e:
            logger.warning(f"[行政之鞭] 存档失败: {e}")
    
    def get_punishment_history(self, claw_id: str) -> List[PunishmentRecord]:
        """获取Claw惩罚历史"""
        return self.punishments.get(claw_id, [])
    
    def get_active_punishments(self, claw_id: str) -> List[PunishmentRecord]:
        """获取有效惩罚(未过期的)"""
        history = self.get_punishment_history(claw_id)
        # 简单策略：返回最近10条
        return history[-10:]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total_punishments = sum(len(records) for records in self.punishments.values())
        by_type = {}
        for records in self.punishments.values():
            for record in records:
                ptype = record.punishment_type.value
                by_type[ptype] = by_type.get(ptype, 0) + 1
        
        return {
            "total_punishments": total_punishments,
            "affected_claws": len(self.punishments),
            "punishments_by_type": by_type,
            "escalation_count": len(self.escalation_chain),
        }


# ══════════════════════════════════════════════════════════════════════════════
# 全局实例
# ══════════════════════════════════════════════════════════════════════════════

_jindu_engine: Optional[JinDuCuJinEngine] = None
_whiplash_engine: Optional[AdministrativeWhipEngine] = None
_shared_factory: Optional[SupervisionClawFactory] = None


def _get_shared_factory() -> SupervisionClawFactory:
    """获取共享的SupervisionClawFactory单例"""
    global _shared_factory
    if _shared_factory is None:
        _shared_factory = SupervisionClawFactory()
    return _shared_factory


def get_jindu_engine(factory: Optional[SupervisionClawFactory] = None) -> JinDuCuJinEngine:
    """获取锦督促引擎（共享Factory）"""
    global _jindu_engine
    if _jindu_engine is None:
        _jindu_engine = JinDuCuJinEngine(factory=factory or _get_shared_factory())
    elif factory is not None and _jindu_engine.factory is not factory:
        # v1.1.1: 传入新factory时替换旧实例
        _jindu_engine = JinDuCuJinEngine(factory=factory)
    return _jindu_engine


def get_whiplash_engine(factory: Optional[SupervisionClawFactory] = None) -> AdministrativeWhipEngine:
    """获取行政之鞭引擎（共享Factory）"""
    global _whiplash_engine
    if _whiplash_engine is None:
        _whiplash_engine = AdministrativeWhipEngine(factory=factory or _get_shared_factory())
    elif factory is not None and _whiplash_engine.factory is not factory:
        # v1.1.1: 传入新factory时替换旧实例
        _whiplash_engine = AdministrativeWhipEngine(factory=factory)
    return _whiplash_engine


__all__ = [
    'JinDuCuJinEngine',
    'DeadlineNode',
    'AdministrativeWhipEngine',
    'PunishmentRecord',
    'get_jindu_engine',
    'get_whiplash_engine',
]
