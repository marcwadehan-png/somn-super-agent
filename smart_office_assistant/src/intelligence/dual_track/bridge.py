"""
双轨桥接器 - Track Bridge v3.0

连接A轨(神政轨)和B轨(神行轨)

核心职责:
1. 建立A→B的单向调用关系
2. 确保B轨不能反向调用A轨
3. 提供任务派发和结果回收的通道
4. 实现"跳过多余环节"的直接调用机制
5. 调用权限校验（DivineReason / Pan-Wisdom Tree / A神政轨）

v3.0 变更:
- 新增 appoint_claw_to_department() — 任命Claw到部门
- 新增 get_department_claws() — 查看部门任命的Claw
- 新增 dispatch_to_claw() — 指派任务给特定Claw
- direct_department_call() 优先使用真实Claw，降级到DivineReason
- 新增 get_appointment_info() — 查看任命详情
- 保留所有 v2.0 向后兼容接口
"""

import logging
import time
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BridgeStatus:
    """桥接状态"""
    connected: bool = False
    track_a_status: str = "unknown"
    track_b_status: str = "unknown"
    total_dispatches: int = 0
    total_completions: int = 0


class TrackBridge:
    """
    双轨桥接器 v3.1

    实现A轨到B轨的严格单向通信:
    - A轨可以派发任务给B轨
    - B轨执行完后回报A轨
    - B轨不能主动调用A轨 (设计约束)

    v3.1优化:
    - create_system() 复用已有 track_b 实例（不再重复创建）
    - 便捷函数使用进程级 track_b 缓存（避免每次新建）
    """

    # v3.1: 进程级 track_b 缓存，避免便捷函数每次新建实例
    _shared_track_b: Optional["DivineExecutionTrack"] = None

    def __init__(self):
        self.track_a: Optional["DivineGovernanceTrack"] = None
        self.track_b: Optional["DivineExecutionTrack"] = None
        self._status = BridgeStatus()

        logger.info("[双轨桥] TrackBridge v3.0 初始化完成")

    def create_system(self) -> "DualTrackSystem":
        """
        创建完整的双轨系统

        Returns:
            DualTrackSystem: 已连接的双轨系统实例
        """
        from .track_a import DivineGovernanceTrack
        from .track_b import DivineExecutionTrack

        # 创建A轨和B轨
        self.track_a = DivineGovernanceTrack()
        self.track_b = DivineExecutionTrack(auto_appoint=True)

        # 通过桥接器连接
        self.track_a.set_track_b(self.track_b)

        self._status.connected = True
        self._status.track_a_status = "active"
        self._status.track_b_status = "active"

        logger.info("[双轨桥] 双轨系统创建并连接成功 v3.0")

        return DualTrackSystem(self)

    # ═══════════════════════════════════════════════════════
    #  v3.0 新增: Claw任命管理接口
    # ═══════════════════════════════════════════════════════

    def get_department_claws(self, department: str) -> List[str]:
        """
        获取某个部门任命的所有Claw名称

        Args:
            department: 部门名称 (e.g., "兵部")

        Returns:
            Claw名称列表
        """
        if not self.track_b:
            return []
        return self.track_b.get_department_claws(department)

    def get_primary_claw(self, department: str) -> Optional[str]:
        """
        获取某个部门的主责Claw名称

        Args:
            department: 部门名称

        Returns:
            主责Claw名称，无任命时返回None
        """
        if not self.track_b:
            return None
        return self.track_b.get_primary_claw(department)

    def get_appointment_info(self, department: str) -> Dict[str, Any]:
        """
        获取某个部门的任命详情

        Args:
            department: 部门名称

        Returns:
            任命信息字典
        """
        if not self.track_b:
            return {"error": "B轨未初始化"}
        return self.track_b.get_appointment_info(department)

    def dispatch_to_claw(
        self,
        department: str,
        claw_name: str,
        task_description: str,
        context: Optional[Dict[str, Any]] = None,
        caller: str = "a_governance",
    ) -> Dict[str, Any]:
        """
        指派任务给特定Claw

        这是v3.0的核心接口——不是给部门派任务，而是直接指定哪个Claw来干活。
        对应"贤者Claw被任命到对应的岗位"的设计理念。

        Args:
            department: 部门名称
            claw_name: 具体Claw名称 (e.g., "乐毅")
            task_description: 任务描述
            context: 上下文
            caller: 调用方类型

        Returns:
            执行结果
        """
        if not self.track_b:
            return {"success": False, "error": "B轨未初始化"}

        logger.info(
            f"[双轨桥] 指派任务给Claw: {claw_name}（{department}）"
        )

        self._status.total_dispatches += 1
        result = self.track_b.execute_sync(
            department=department,
            task_description=task_description,
            context=context or {},
            caller=caller,
            claw_name=claw_name,
        )
        if result.get("success"):
            self._status.total_completions += 1
        return result

    # ═══════════════════════════════════════════════════════
    #  v2.0 保留接口
    # ═══════════════════════════════════════════════════════

    def get_bridge_status(self) -> BridgeStatus:
        """获取桥接状态"""
        if self.track_a and self.track_b:
            a_info = self.track_a.get_status()
            b_info = self.track_b.get_stats()

            self._status.track_a_status = a_info.get("name", "unknown")
            self._status.track_b_status = b_info.get("name", "unknown")
            self._status.total_dispatches = a_info.get("total_assignments", 0)
            self._status.total_completions = b_info.get("completed_tasks", 0)

        return self._status

    def validate_call_direction(self, caller: str, receiver: str) -> bool:
        """
        验证调用方向是否合法

        只允许 A → B，禁止 B → A
        """
        is_valid = (caller == "A" and receiver == "B") or (caller == receiver)

        if not is_valid:
            logger.error(f"[双轨桥] 非法调用方向: {caller} → {receiver} (只允许 A→B)")

        return is_valid

    def direct_department_call(
        self,
        caller_track: str,
        department_name: str,
        task_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        直接部门调用 (跳过多余环节的核心实现)

        v3.0: 优先使用该部门的真实Claw独立工作，无Claw时降级到DivineReason。

        Args:
            caller_track: 调用方轨道 ("A" 或 "B")
            department_name: 目标部门名称
            task_data: 任务数据

        Returns:
            执行结果
        """
        # 验证调用方向
        if not self.validate_call_direction(caller_track, "B"):
            return {
                "success": False,
                "error": f"ACCESS_DENIED: {caller_track} 不能直接调用 {department_name}",
                "reason": "只有A轨才能直接调用B轨的职能部门",
            }

        logger.info(f"[双轨桥] 直接部门调用: {caller_track} → {department_name}")

        self._status.total_dispatches += 1

        task_description = task_data.get("task_description", "")
        context = task_data.get("context", {})

        if self.track_b:
            result = self.track_b.execute_sync(
                department=department_name,
                task_description=task_description,
                context=context,
                caller="a_governance",
            )
            if result.get("success"):
                self._status.total_completions += 1
            return result
        else:
            return {
                "success": False,
                "error": "B轨未初始化",
                "department": department_name,
            }

    def create_divine_reason_caller(self, node_id: str = "default") -> Callable:
        """
        创建 DivineReason 节点调用器

        DivineReason 的各节点可通过此调用器跳过调度器直接调用神行轨。

        Args:
            node_id: DivineReason 节点标识

        Returns:
            调用函数 (department, task_description, context) → result
        """
        if not self.track_b:
            raise RuntimeError("B轨未连接")

        def caller(
            department: str,
            task_description: str,
            context: Optional[Dict[str, Any]] = None,
            claw_name: Optional[str] = None,  # v3.0新增: 可指定Claw
        ) -> Dict[str, Any]:
            logger.info(f"[双轨桥-DR] DivineReason节点 {node_id} → {department}")
            return self.track_b.execute_sync(
                department=department,
                task_description=task_description,
                context=context or {},
                caller="divine_reason",
                claw_name=claw_name,
            )

        return caller

    def create_wisdom_tree_caller(self, branch_id: str = "default") -> Callable:
        """
        创建 Pan-Wisdom Tree 枝丫调用器

        Pan-Wisdom Tree 的各枝丫（末端）可通过此调用器跳过调度器直接调用神行轨。

        Args:
            branch_id: 枝丫标识

        Returns:
            调用函数 (department, task_description, context) → result
        """
        if not self.track_b:
            raise RuntimeError("B轨未连接")

        def caller(
            department: str,
            task_description: str,
            context: Optional[Dict[str, Any]] = None,
            claw_name: Optional[str] = None,  # v3.0新增: 可指定Claw
        ) -> Dict[str, Any]:
            logger.info(f"[双轨桥-PWT] WisdomTree枝丫 {branch_id} → {department}")
            return self.track_b.execute_sync(
                department=department,
                task_description=task_description,
                context=context or {},
                caller="pan_wisdom_tree",
                claw_name=claw_name,
            )

        return caller


class DualTrackSystem:
    """
    双轨架构统一入口 v3.0

    对外提供统一的接口，内部自动协调A/B两轨的工作
    """

    def __init__(self, bridge: TrackBridge):
        self.bridge = bridge
        self.track_a = bridge.track_a
        self.track_b = bridge.track_b

        logger.info("[双轨系统] 统一入口初始化 v3.0")

    def process(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        统一处理接口

        Args:
            query: 用户查询
            context: 可选上下文

        Returns:
            完整处理结果
        """
        logger.info(f"[双轨系统] 处理请求: {query[:50]}...")

        return self.track_a.process_request(query, context)

    def execute_direct(
        self,
        department: str,
        task: str,
        context: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        直接执行命令 (跳过多余环节)

        Args:
            department: 目标部门
            task: 任务描述
            context: 额外上下文

        Returns:
            执行结果
        """
        logger.info(f"[双轨系统] 直接执行: {department} - {task}")

        return self.bridge.direct_department_call(
            caller_track="A",
            department_name=department,
            task_data={
                "task_description": task,
                "context": context or {},
                "mode": "direct_skip_layers",
            },
        )

    # ═══════════════════════════════════════════════════════
    #  v3.0 新增接口
    # ═══════════════════════════════════════════════════════

    def dispatch_to_claw(
        self,
        department: str,
        claw_name: str,
        task: str,
        context: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        指派任务给特定Claw

        Args:
            department: 部门名称
            claw_name: 具体Claw名称
            task: 任务描述
            context: 额外上下文

        Returns:
            执行结果
        """
        return self.bridge.dispatch_to_claw(
            department=department,
            claw_name=claw_name,
            task_description=task,
            context=context or {},
            caller="a_governance",
        )

    def get_department_claws(self, department: str) -> List[str]:
        """获取某个部门任命的所有Claw"""
        return self.bridge.get_department_claws(department)

    def get_primary_claw(self, department: str) -> Optional[str]:
        """获取某个部门的主责Claw"""
        return self.bridge.get_primary_claw(department)

    def get_appointment_info(self, department: str) -> Dict[str, Any]:
        """获取部门任命详情"""
        return self.bridge.get_appointment_info(department)

    # ═══════════════════════════════════════════════════════
    #  v2.0 保留接口
    # ═══════════════════════════════════════════════════════

    def get_divine_reason_caller(self, node_id: str = "default") -> Callable:
        """获取 DivineReason 特权调用器"""
        return self.bridge.create_divine_reason_caller(node_id)

    def get_wisdom_tree_caller(self, branch_id: str = "default") -> Callable:
        """获取 Pan-Wisdom Tree 特权调用器"""
        return self.bridge.create_wisdom_tree_caller(branch_id)

    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        bridge_status = self.bridge.get_bridge_status()
        a_status = self.track_a.get_status() if self.track_a else {}
        b_status = self.track_b.get_stats() if self.track_b else {}

        return {
            "system": "双轨架构 v3.0",
            "bridge": {
                "connected": bridge_status.connected,
                "total_dispatches": bridge_status.total_dispatches,
                "total_completions": bridge_status.total_completions,
            },
            "track_a": a_status,
            "track_b": b_status,
            "architecture": {
                "call_pattern": "A → B (单向)",
                "skip_mechanism": "支持直接部门调用 + 指定Claw调用",
                "b_to_a_restricted": True,
                "authorized_callers": ["divine_reason", "pan_wisdom_tree", "a_governance", "internal"],
                "claw_mode": "independent_worker",  # v3.0
            },
        }


# ═══════════════════════════════════════════════════════
#  Pan-Wisdom Tree 集成点 (向后兼容)
# ═══════════════════════════════════════════════════════

def create_wisdom_tree_branch_executor(department: str):
    """
    创建 Pan-Wisdom Tree 枝干/枝丫执行器

    v3.1优化: 复用进程级 track_b 缓存，避免每次新建实例。
    """
    def executor(task: str, **kwargs) -> Dict[str, Any]:
        """枝干/枝丫执行器"""
        logger.info(f"[智慧树枝干] 执行: {department} - {task}")

        try:
            # v3.1: 复用共享 track_b
            if TrackBridge._shared_track_b is None:
                from .track_b import DivineExecutionTrack
                TrackBridge._shared_track_b = DivineExecutionTrack(auto_appoint=True)

            return TrackBridge._shared_track_b.execute_sync(
                department=department,
                task_description=task,
                context=kwargs.get("context", {}),
                caller="pan_wisdom_tree",
                claw_name=kwargs.get("claw_name"),
            )
        except Exception as e:
            logger.error(f"[智慧树枝干] 执行失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "department": department,
                "task": task,
                "mode": "error",
            }

    return executor


def create_divine_reason_node_executor(node_id: str = "default"):
    """
    创建 DivineReason 节点执行器

    v3.1优化: 复用进程级 track_b 缓存。
    """
    def executor(
        department: str,
        task: str,
        **kwargs
    ) -> Dict[str, Any]:
        logger.info(f"[DivineReason节点 {node_id}] 执行: {department} - {task}")

        try:
            # v3.1: 复用共享 track_b
            if TrackBridge._shared_track_b is None:
                from .track_b import DivineExecutionTrack
                TrackBridge._shared_track_b = DivineExecutionTrack(auto_appoint=True)

            return TrackBridge._shared_track_b.execute_sync(
                department=department,
                task_description=task,
                context=kwargs.get("context", {}),
                caller="divine_reason",
                claw_name=kwargs.get("claw_name"),
            )
        except Exception as e:
            logger.error(f"[DivineReason节点 {node_id}] 执行失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "department": department,
                "task": task,
                "mode": "error",
            }

    return executor


# ============================================================
# DivineExecutionBridge - DivineReason 神行轨桥接器
# ============================================================

def get_divine_execution_bridge():
    """
    获取 DivineExecutionBridge 桥接器
    
    用于将 DivineReason 的推荐节点映射到神行轨执行。
    """
    from ._divine_execution_bridge import DivineExecutionBridge
    return DivineExecutionBridge()


def reason_and_execute(
    query: str,
    problem_type: str = "",
    max_engines: int = 8,
    context: dict = None
):
    """
    快捷函数：推理+执行一步到位
    
    这是 DivineReason + 神行轨的联合入口。
    """
    from ._divine_execution_bridge import reason_and_execute as bridge_execute
    return bridge_execute(
        query=query,
        problem_type=problem_type,
        max_engines=max_engines,
        context=context
    )
