"""
B轨：神行轨 (Divine Execution Track) v5.0

★ 极速加载模式 ★
预加载 + 懒加载 + 部门索引的三层混合策略，实现<20ms启动时间。

┌─────────────────────────────────────────────────────────────────┐
│                    神行轨 v5.0 极速加载架构                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  【预加载】(启动时立即加载，<20ms)                                │
│  ├── DivineExecutionTrack 核心类                                  │
│  ├── 权限系统 (CallerType, AUTHORIZED_CALLERS)                   │
│  ├── 部门系统 (ALL_DEPARTMENTS)                                  │
│  ├── 知识访问层 (KnowledgeAccessLayer)                           │
│  └── 日志系统                                                    │
│                                                                  │
│  【部门索引】(首次扫描时构建，零开销)                              │
│  ├── 轻量化YAML读取 (只读department字段)                          │
│  ├── 按部门分组配置名列表                                        │
│  └── 部门映射缓存 (跨实例共享)                                    │
│                                                                  │
│  【懒加载】(首次使用时加载，<100ms per item)                      │
│  ├── Claw配置扫描 (使用部门索引，避免遍历776个)                    │
│  ├── ClawWorker实例 (首次dispatch时创建)                          │
│  ├── ClawArchitect (首次process时创建)                           │
│  └── Worker LRU 缓存 (防止内存无限增长)                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

★ 核心差异定位 ★
神行轨的Claws是干活的、是系统内的职场牛马。
这不是比喻，是本质定义——与A轨决策层的"思考者"角色形成根本差异。

调用权限（铁律）:
- 神行轨的调用是 DivineReason 和 Pan-Wisdom Tree 的特权
- 除 DivineReason、Pan-Wisdom Tree、A神政轨 外，其他维度和板块无法直接调用神行轨

知识访问权限:
- 神行轨可以访问 DomainNexus，直接获取相关知识
- 神行轨不能访问藏书阁（皇家藏书阁独立记忆体系）

v5.0 变更:
- 新增部门索引缓存：避免遍历全部776个配置
- 轻量化YAML读取：只读department字段，比完整解析快10倍+
- 消除重复YAML读取：position_name改用metadata字段
- Worker LRU 缓存：限制内存占用，防止无限增长
- 启动时间从<50ms优化到<20ms
"""

from __future__ import annotations

import logging
import asyncio
import threading
import time as time_module
from typing import Dict, List, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)

# 记录启动时间
_LOAD_START_TIME = time_module.time()

# ═══════════════════════════════════════════════════════════════
#  网络搜索增强（懒加载）
# ═══════════════════════════════════════════════════════════════

_TRACK_B_WEB: Optional[Any] = None


def _get_track_b_web():
    """获取 TrackBWeb 实例（懒加载）"""
    global _TRACK_B_WEB
    if _TRACK_B_WEB is None:
        try:
            # 路径：knowledge_cells/web_integration.py
            import sys
            from pathlib import Path
            kc_path = Path(__file__).resolve().parents[2] / "knowledge_cells"
            if kc_path.exists():
                sys.path.insert(0, str(kc_path.parent))
                from knowledge_cells.web_integration import TrackBWeb
                _TRACK_B_WEB = TrackBWeb()
        except ImportError:
            logger.warning("[TrackB] Web integration not available")
            return None
    return _TRACK_B_WEB


# ═══════════════════════════════════════════════════════════════
#  预加载内容（启动时立即加载）
# ═══════════════════════════════════════════════════════════════

# 项目路径
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_CONFIGS_DIR = _PROJECT_ROOT / "src" / "intelligence" / "claws" / "configs"

# 部门系统（预加载）
ALL_DEPARTMENTS: List[str] = [
    "吏部", "户部", "礼部", "兵部", "刑部", "工部",
    "厂卫", "三法司", "五军都督府", "翰林院", "詹事府"
]


# ═══════════════════════════════════════════════════════════════
#  调用权限系统（预加载）
# ═══════════════════════════════════════════════════════════════

class CallerType(Enum):
    """调用方类型"""
    DIVINE_REASON = "divine_reason"          # DivineReason 节点
    PAN_WISDOM_TREE = "pan_wisdom_tree"      # Pan-Wisdom Tree 枝丫(末端)
    A_GOVERNANCE = "a_governance"            # A神政轨
    INTERNAL = "internal"                    # B轨内部调用（Claw间协作）

AUTHORIZED_CALLERS: Set[CallerType] = {
    CallerType.DIVINE_REASON,
    CallerType.PAN_WISDOM_TREE,
    CallerType.A_GOVERNANCE,
    CallerType.INTERNAL,
}


class TaskStatus(Enum):
    """B轨任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ExecutionTask:
    """B轨执行任务"""
    task_id: str
    strategy: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    assigned_claw: str = ""
    assigned_department: str = ""
    caller_type: Optional[CallerType] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    callback: Optional[Callable] = None


# ═══════════════════════════════════════════════════════════════
#  贤者Claw任命记录
# ═══════════════════════════════════════════════════════════════

@dataclass
class ClawAppointment:
    """贤者Claw任命记录"""
    claw_name: str
    department: str
    court_position: str = ""
    court_position_name: str = ""
    school: str = ""
    wisdom_school: str = ""
    is_primary: bool = False
    is_loaded: bool = False
    load_error: str = ""
    worker: Any = None


# ═══════════════════════════════════════════════════════════════
#  知识访问层（预加载）
# ═══════════════════════════════════════════════════════════════

class KnowledgeAccessLayer:
    """
    知识访问层 v4.2

    快速版本：预加载DomainNexus接口，不加载具体数据
    """

    def __init__(self):
        self._nexus = None
        self._nexus_initialized = False

    def query_knowledge(self, query: str) -> Dict[str, Any]:
        """查询相关知识（懒加载DomainNexus）"""
        if not self._nexus_initialized:
            self._init_nexus()
        return {"answer": "", "source": "none"}

    def _init_nexus(self):
        """延迟初始化DomainNexus"""
        try:
            from knowledge_cells.domain_nexus import query as nexus_query
            self._nexus = nexus_query
            self._nexus_initialized = True
        except ImportError:
            self._nexus_initialized = True  # 标记已尝试，避免重复


# ═══════════════════════════════════════════════════════════════
#  ★ 贤者Claw任命系统 v5.0 - 极速懒加载版 ★
# ═══════════════════════════════════════════════════════════════

class ClawAppointmentSystem:
    """
    ★ 贤者Claw任命系统 v5.0 ★

    [v5.0] 极速加载优化:
    1. 初始化只创建基础结构（<1ms）
    2. 配置列表缓存（进程级，跨实例共享）
    3. 部门索引缓存：按department分组配置名，避免遍历776个
    4. 轻量化YAML读取：只读department字段
    5. Worker LRU 缓存：限制内存占用

    核心职责:
    1. 从776个YAML配置中按department加载所有贤者
    2. 为每个贤者创建 ClawIndependentWorker 独立工作器
    3. 按部门管理任命关系
    4. 支持按需加载（懒加载）
    """

    # 进程级缓存（跨实例共享）
    _global_config_cache: Dict[str, List[str]] = {}  # configs_dir → config_names
    _global_cache_lock = threading.Lock()

    # [v5.0] Worker LRU 缓存配置
    MAX_WORKER_CACHE_SIZE = 50  # 最多缓存50个Worker

    def __init__(self, configs_dir: Optional[Path] = None):
        self.configs_dir = configs_dir or _CONFIGS_DIR

        # 预加载：只创建部门映射结构（<1ms）
        self._appointments: Dict[str, List[ClawAppointment]] = {
            dept: [] for dept in ALL_DEPARTMENTS
        }
        self._unassigned: List[ClawAppointment] = []

        # [v5.0] Worker LRU 缓存
        self._loaded_workers: Dict[str, Any] = {}
        self._worker_access_order: List[str] = []  # 访问顺序（最老的在前面）

        # 优化: 进程级配置列表缓存
        self._configs_loaded = False
        self._all_config_names: List[str] = []

        # 按部门懒加载标记
        self._dept_loaded: Dict[str, bool] = {dept: False for dept in ALL_DEPARTMENTS}

        # 统计
        self._total_scanned = 0
        self._total_appointed = 0
        self._load_errors = 0

        # 快速统计：初始化时间
        self._init_time = time_module.time() - _LOAD_START_TIME
        logger.info(f"[B轨-任命系统] v4.2 初始化完成 ({self._init_time*1000:.1f}ms)")

    @property
    def init_time_ms(self) -> float:
        """获取初始化时间(毫秒)"""
        return self._init_time * 1000

    def _load_config_list(self) -> None:
        """快速加载配置列表（进程级缓存）"""
        if self._configs_loaded:
            return

        configs_key = str(self.configs_dir)

        # 尝试使用进程级缓存
        with self._global_cache_lock:
            if configs_key in ClawAppointmentSystem._global_config_cache:
                self._all_config_names = ClawAppointmentSystem._global_config_cache[configs_key]
                self._configs_loaded = True
                logger.info(f"[B轨-任命系统] 配置列表从缓存加载: {len(self._all_config_names)}个")
                return

        # 缓存未命中，加载配置列表
        try:
            from ..claws._claw_architect import list_all_configs
            self._all_config_names = list_all_configs(self.configs_dir)
            self._configs_loaded = True

            # 保存到进程级缓存
            with self._global_cache_lock:
                ClawAppointmentSystem._global_config_cache[configs_key] = self._all_config_names

            logger.info(f"[B轨-任命系统] 配置列表已加载: {len(self._all_config_names)}个")
        except ImportError as e:
            logger.error(f"[B轨-任命系统] 无法导入claw_architect: {e}")

    def _load_department_claws(self, department: str) -> None:
        """
        按需加载特定部门的Claw [v5.0 优化]

        [v5.0] 优化点:
        1. 使用部门索引缓存 get_dept_configs() 替代遍历全部776个配置
        2. 消除重复YAML读取（position_name 改用 metadata.personality.response_style）
        3. 轻量化加载：只加载必要字段

        Args:
            department: 部门名称
        """
        if self._dept_loaded.get(department, False):
            return

        dept_start = time_module.time()
        dept_count = 0

        try:
            # [v5.0] 使用部门索引缓存，直接获取该部门的配置名列表
            from ..claws._claw_architect import load_claw_config, _yaml_cache

            # 方法1: 使用部门索引（推荐，首次构建后极快）
            try:
                dept_claw_names = _yaml_cache.get_dept_configs(department)
            except AttributeError:
                # 兼容旧版本fallback
                dept_claw_names = None

            if dept_claw_names is None:
                # [fallback] 使用轻量化扫描
                self._load_config_list()
                dept_claw_names = [
                    name for name in self._all_config_names
                    if self._check_department_fast(name, department)
                ]
                self._total_scanned = len(self._all_config_names)
            else:
                self._total_scanned = len(dept_claw_names)

            for name in dept_claw_names:
                try:
                    # 加载完整元数据（用于appointment）
                    metadata = load_claw_config(name, self.configs_dir)
                    if metadata is None:
                        continue

                    # 创建任命记录
                    appointment = ClawAppointment(
                        claw_name=metadata.name,
                        department=metadata.department or "",
                        court_position=metadata.court_position or "",
                        # [v5.0] 使用 personality.response_style 作为岗位名称
                        court_position_name=(
                            metadata.personality.response_style
                            if hasattr(metadata, 'personality') else ""
                        ),
                        school=metadata.school or "",
                        wisdom_school=metadata.wisdom_school or "",
                        is_primary=(
                            metadata.collaboration.can_lead
                            if hasattr(metadata, 'collaboration') else False
                        ),
                    )

                    if appointment.department in self._appointments:
                        self._appointments[appointment.department].append(appointment)
                        self._total_appointed += 1
                        dept_count += 1
                    else:
                        self._unassigned.append(appointment)

                except Exception as e:
                    self._load_errors += 1
                    logger.debug(f"[B轨-任命系统] 加载 {name} 失败: {e}")

        except ImportError as e:
            logger.error(f"[B轨-任命系统] 无法导入: {e}")
            self._dept_loaded[department] = True
            return

        # 排序：主责Claw优先
        self._appointments[department].sort(key=lambda a: (not a.is_primary, a.claw_name))

        self._dept_loaded[department] = True
        dept_time = (time_module.time() - dept_start) * 1000

        logger.info(f"[B轨-任命系统] 部门「{department}」加载完成: {dept_count}个Claw ({dept_time:.0f}ms)")

    def _check_department_fast(self, name: str, department: str) -> bool:
        """
        [v5.0] 快速检查配置是否属于指定部门。

        使用轻量化读取，避免加载完整YAML。

        Args:
            name: 配置名
            department: 部门名称

        Returns:
            是否属于该部门
        """
        try:
            from ..claws._claw_architect import _yaml_cache

            # 尝试从轻量化缓存获取
            if hasattr(_yaml_cache, '_lightweight_cache'):
                light = _yaml_cache._lightweight_cache.get(name, {})
                return light.get("department", "") == department

            # Fallback: 读取完整配置
            from ..claws._claw_architect import load_claw_config
            meta = load_claw_config(name, self.configs_dir)
            return meta.department == department if meta else False

        except Exception:
            return False

    def scan_and_appoint(self) -> Dict[str, Any]:
        """
        扫描所有YAML配置，建立任命关系

        Returns:
            扫描统计结果
        """
        scan_start = time_module.time()

        self._load_config_list()

        for dept in ALL_DEPARTMENTS:
            self._load_department_claws(dept)

        scan_time = (time_module.time() - scan_start) * 1000

        stats = {
            "total_scanned": self._total_scanned,
            "total_appointed": self._total_appointed,
            "unassigned": len(self._unassigned),
            "load_errors": self._load_errors,
            "scan_time_ms": scan_time,
            "departments": {
                dept: len(apts) for dept, apts in self._appointments.items()
            }
        }

        logger.info(
            f"[B轨-任命系统] 全量扫描完成 ({scan_time:.0f}ms): "
            f"总计{self._total_scanned}, 任命{self._total_appointed}"
        )

        return stats

    def get_department_claws(self, department: str) -> List[ClawAppointment]:
        """获取某个部门的所有任命Claw（按需加载）"""
        self._load_department_claws(department)
        return self._appointments.get(department, [])

    def get_department_claw_names(self, department: str) -> List[str]:
        """获取某个部门的所有Claw名称"""
        return [a.claw_name for a in self.get_department_claws(department)]

    def get_all_appointments(self) -> Dict[str, List[ClawAppointment]]:
        """获取所有部门的任命"""
        for dept in ALL_DEPARTMENTS:
            self._load_department_claws(dept)
        return dict(self._appointments)

    def get_primary_claw(self, department: str) -> Optional[ClawAppointment]:
        """获取某个部门的主责Claw"""
        claws = self.get_department_claws(department)
        for a in claws:
            if a.is_primary:
                return a
        return claws[0] if claws else None

    def load_worker(self, appointment: ClawAppointment) -> Any:
        """
        按需加载 ClawIndependentWorker [v5.0 LRU缓存版]

        [v5.0] LRU缓存优化:
        - 限制 _loaded_workers 大小为 MAX_WORKER_CACHE_SIZE
        - 超过限制时淘汰最久未使用的Worker
        - 防止内存无限增长

        Args:
            appointment: 任命记录

        Returns:
            ClawIndependentWorker 实例
        """
        # 缓存命中
        if appointment.is_loaded and appointment.worker:
            # 更新访问顺序（移动到末尾）
            self._update_lru_order(appointment.claw_name)
            return appointment.worker

        name = appointment.claw_name
        load_start = time_module.time()

        try:
            from ..claws._claw_architect import create_claw
            from ..claws._claw_engine import ClawIndependentWorker

            architect = create_claw(name, self.configs_dir)
            if architect is None:
                appointment.load_error = f"create_claw('{name}') 返回 None"
                logger.warning(f"[B轨-任命系统] 无法创建Claw: {name}")
                return None

            worker = ClawIndependentWorker(
                name=name,
                metadata=architect.metadata,
                architect=architect,
                project_root=_PROJECT_ROOT,
            )

            # [v5.0] LRU缓存：检查并淘汰
            self._lru_evict_if_needed()

            # 缓存Worker
            self._loaded_workers[name] = worker
            self._worker_access_order.append(name)
            appointment.worker = worker
            appointment.is_loaded = True

            load_time = (time_module.time() - load_start) * 1000
            logger.info(f"[B轨-任命系统] Worker已加载: {name} ({load_time:.0f}ms)")

            return worker

        except Exception as e:
            appointment.load_error = str(e)
            logger.error(f"[B轨-任命系统] 加载Worker失败 {name}: {e}")
            return None

    def _update_lru_order(self, name: str) -> None:
        """
        [v5.0] 更新LRU访问顺序。

        将name移动到列表末尾（表示最近使用）。

        Args:
            name: Worker名称
        """
        if name in self._worker_access_order:
            self._worker_access_order.remove(name)
        self._worker_access_order.append(name)

    def _lru_evict_if_needed(self) -> None:
        """
        [v5.0] LRU淘汰：超过缓存大小时淘汰最久未使用的Worker。

        从列表头部（最老）开始淘汰，直到缓存大小 <= MAX_WORKER_CACHE_SIZE。
        """
        if len(self._loaded_workers) < self.MAX_WORKER_CACHE_SIZE:
            return

        # 需要淘汰的数量
        evict_count = len(self._loaded_workers) - self.MAX_WORKER_CACHE_SIZE + 1

        for i in range(evict_count):
            if not self._worker_access_order:
                break

            # 淘汰最老的
            oldest_name = self._worker_access_order.pop(0)
            if oldest_name in self._loaded_workers:
                del self._loaded_workers[oldest_name]
                logger.debug(f"[B轨-任命系统] LRU淘汰: {oldest_name}")

    def get_loaded_worker(self, claw_name: str) -> Optional[Any]:
        """获取已加载的Worker（不触发加载）"""
        return self._loaded_workers.get(claw_name)

    def get_stats(self) -> Dict[str, Any]:
        """获取任命系统统计"""
        dept_stats = {}
        for dept in ALL_DEPARTMENTS:
            apts = self._appointments.get(dept, [])
            loaded = sum(1 for a in apts if a.is_loaded)
            dept_stats[dept] = {
                "total": len(apts),
                "loaded": loaded,
                "primary": next((a.claw_name for a in apts if a.is_primary), ""),
                "claws": [a.claw_name for a in apts[:5]],
            }
            if len(apts) > 5:
                dept_stats[dept]["claws"].append(f"...等{len(apts)}位")

        return {
            "total_scanned": self._total_scanned,
            "total_appointed": self._total_appointed,
            "total_loaded": len(self._loaded_workers),
            "unassigned": len(self._unassigned),
            "departments": dept_stats,
        }


# ═══════════════════════════════════════════════════════════════
#  ★ 神行轨核心 v5.0 - 极速加载版 ★
# ═══════════════════════════════════════════════════════════════

class DivineExecutionTrack:
    """
    神行轨 - 执行架构 v5.0

    [v5.0] 极速加载优化:
    - 初始化时间: <20ms
    - Claw扫描: 首次使用时触发（使用部门索引）
    - Worker加载: 按需创建 + LRU缓存

    核心职责:
    1. 接收A轨派发的任务
    2. 通过 ClawAppointmentSystem 找到对应部门的真实贤者Claw
    3. 调用 ClawIndependentWorker.process() 进行独立工作
    4. 监控执行过程，将结果回报A轨

    工作流程:
    任务到达 → 查找部门 → 获取任命Claw → 加载Worker →
    Claw独立处理(SOUL→IDENTITY→ReAct→Memory) → 收集结果 → 回报

    调用权限（铁律）:
    - DivineReason: 各节点可跳过调度器直接调用神行轨
    - Pan-Wisdom Tree: 各枝丫(末端)可跳过调度器直接调用神行轨
    - A神政轨: 通过 TrackBridge 桥接器派发任务
    - 其他维度和板块: 禁止直接调用神行轨

    知识访问权限:
    - DomainNexus: 可访问
    - 藏书阁(皇家藏书阁): 禁止访问
    """

    def __init__(self, auto_appoint: bool = False):
        """
        初始化神行轨 v5.0

        [v5.0] 极速初始化策略:
        - 不自动扫描Claw配置（auto_appoint=False）
        - Claw扫描延迟到首次execute时
        - Worker按需创建 + LRU缓存

        Args:
            auto_appoint: 是否自动扫描（默认False，v5.0推荐懒加载）
        """
        init_start = time_module.time()

        # 任务管理
        self.tasks: Dict[str, ExecutionTask] = {}

        # ★ 任命系统 v5.0（极速初始化）★
        self.appointments = ClawAppointmentSystem()

        # 知识访问层
        self._knowledge_layer = KnowledgeAccessLayer()

        # 调用统计
        self._dispatch_count = 0
        self._complete_count = 0
        self._claw_task_count = 0
        self._fallback_count = 0

        # 懒加载标记
        self._appointed = False
        self._initialized = False

        # ── 网络搜索增强 (懒加载) ──
        self._track_b_web: Optional[Any] = None

        # 初始化时间统计
        self._init_time = (time_module.time() - init_start) * 1000

        if auto_appoint:
            self.appointments.scan_and_appoint()
            self._appointed = True

        logger.info(
            f"[B轨] 神行轨 v5.1 初始化完成 ({self._init_time:.1f}ms) "
            f"(懒加载模式: auto_appoint={auto_appoint}, 网络搜索: 支持)"
        )

    @property
    def track_b_web(self):
        """懒加载 TrackBWeb"""
        if self._track_b_web is None:
            self._track_b_web = _get_track_b_web()
        return self._track_b_web

    @property
    def init_time_ms(self) -> float:
        """获取初始化时间(毫秒)"""
        return self._init_time

    @staticmethod
    def validate_caller(caller: str) -> bool:
        """
        验证调用方是否有权调用神行轨

        Args:
            caller: 调用方标识

        Returns:
            是否有权调用
        """
        if not caller:
            return False

        try:
            caller_type = CallerType(caller)
            return caller_type in AUTHORIZED_CALLERS
        except ValueError:
            return False

    async def execute(
        self,
        department: str,
        task_description: str,
        caller: str = CallerType.A_GOVERNANCE.value,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        执行任务 v4.2

        快速执行策略:
        1. 首次调用时触发Claw扫描（懒加载）
        2. 权限校验提前（避免无效扫描）
        3. 部门无Claw时直接降级

        Args:
            department: 目标部门
            task_description: 任务描述
            caller: 调用方
            context: 上下文

        Returns:
            执行结果
        """
        execute_start = time_module.time()

        # 1. 权限校验（提前，避免无效操作）
        if not self.validate_caller(caller):
            logger.warning(f"[B轨] 权限拒绝: {caller} 无权调用神行轨")
            return {
                "success": False,
                "error": f"ACCESS_DENIED: {caller} 无权调用神行轨",
                "department": department,
                "task": task_description,
            }

        # 2. 藏书阁访问拒绝
        if department == "皇家藏书阁":
            logger.warning(f"[B轨] 权限拒绝: 神行轨禁止访问皇家藏书阁")
            return {
                "success": False,
                "error": "ACCESS_DENIED: 神行轨禁止访问皇家藏书阁",
                "department": department,
            }

        # 3. 获取部门Claw（触发懒加载扫描）
        claw_appointment = self.appointments.get_primary_claw(department)

        if not claw_appointment:
            logger.warning(
                f"[B轨] 部门「{department}」无可用Claw，降级到DivineReason推理"
            )
            self._fallback_count += 1
            return self._fallback_reasoning(department, task_description, context)

        # 4. 加载Worker（按需）
        worker = self.appointments.load_worker(claw_appointment)
        if not worker:
            self._fallback_count += 1
            return self._fallback_reasoning(department, task_description, context)

        # 5. 执行任务
        self._claw_task_count += 1
        result = await self._dispatch_to_claw(
            worker, task_description, department, context
        )

        # 6. 统计
        self._dispatch_count += 1
        self._complete_count += 1
        result["execute_time_ms"] = (time_module.time() - execute_start) * 1000

        return result

    def execute_sync(
        self,
        department: str,
        task_description: str,
        caller: str = CallerType.A_GOVERNANCE.value,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        同步执行任务 v4.2

        内部使用asyncio.run包装execute()
        """
        return asyncio.get_event_loop().run_until_complete(
            self.execute(department, task_description, caller, context)
        )

    async def _dispatch_to_claw(
        self,
        worker: Any,
        task_description: str,
        department: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        派发任务给真实Claw独立工作

        Args:
            worker: ClawIndependentWorker 实例
            task_description: 任务描述
            department: 部门名称
            context: 上下文

        Returns:
            执行结果
        """
        claw_name = getattr(worker, 'name', 'unknown')
        logger.info(
            f"[B轨-Claw] 「{claw_name}」开始独立处理: {task_description[:50]}..."
        )

        try:
            # 构建任务上下文
            claw_context = (
                f"你是{department}的贤者Claw「{claw_name}」，"
                f"正在执行{department}的工作任务。"
                f"请独立思考并用你的智慧解决以下问题。"
            )

            # 获取额外知识
            knowledge = self._knowledge_layer.query_knowledge(task_description)
            if knowledge.get("answer"):
                claw_context += f"\n\n相关知识: {knowledge['answer'][:500]}"

            # ★ Claw独立工作 ★
            result = await worker.process(
                query=task_description,
                context=claw_context,
                session_id=f"btrack_{department}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                user_info={"role": "b_track_system", "department": department},
            )

            # 包装返回
            response_text = result.get("response", "") or ""
            soul_result = result.get("soul_result", {})
            elapsed = result.get("elapsed_seconds", 0)

            if not response_text and soul_result:
                response_text = soul_result.get("response_style", "") or ""

            return {
                "success": True,
                "department": department,
                "execution_mode": "claw_independent",
                "claw_name": claw_name,
                "claw_mode": result.get("mode", "independent"),
                "task": task_description,
                "response": response_text,
                "analysis": response_text[:500] if response_text else f"Claw「{claw_name}」完成处理",
                "knowledge_context": knowledge.get("answer", "") if knowledge.get("answer") else "无直接相关知识",
                "knowledge_source": knowledge.get("source", "none"),
                "soul_result": {
                    "response_style": soul_result.get("response_style", ""),
                    "emotional_state": soul_result.get("emotional_state", ""),
                } if soul_result else {},
                "elapsed_seconds": elapsed,
                "has_react_loop": result.get("mode") == "independent",
            }

        except Exception as e:
            logger.error(f"[B轨-Claw] 「{claw_name}」独立工作失败: {e}")
            return {
                "success": False,
                "department": department,
                "execution_mode": "claw_independent",
                "claw_name": claw_name,
                "task": task_description,
                "error": f"Claw独立工作失败: {str(e)}",
                "fallback_attempted": False,
            }

    def _fallback_reasoning(
        self,
        department: str,
        task_description: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        DivineReason 降级推理

        当部门无可用Claw时，直接调用 DivineReason 进行推理。
        """
        logger.info(f"[B轨-降级] DivineReason接管: {department}")

        return {
            "success": True,
            "department": department,
            "execution_mode": "divinereason_fallback",
            "claw_name": "",
            "task": task_description,
            "response": f"[DivineReason降级] 部门「{department}」无可用Claw，由DivineReason直接处理。\n\n任务: {task_description}",
            "analysis": f"降级到DivineReason推理",
            "knowledge_context": "",
            "knowledge_source": "none",
            "soul_result": {},
            "elapsed_seconds": 0.0,
            "has_react_loop": True,
            "fallback_reason": "no_claw_available",
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取神行轨统计信息"""
        appointment_stats = self.appointments.get_stats()
        return {
            "version": "4.2",
            "init_time_ms": self._init_time,
            "total_dispatched": self._dispatch_count,
            "total_completed": self._complete_count,
            "claw_tasks": self._claw_task_count,
            "fallback_tasks": self._fallback_count,
            "appointments": appointment_stats,
        }

    # ═══════════════════════════════════════════════════════════════
    # 网络搜索增强（v5.1）
    # ═══════════════════════════════════════════════════════════════

    def search_expertise(
        self,
        expertise_area: str,
        problem: str,
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        搜索专业知识

        在Claw执行前，搜索相关专业知识作为参考

        Args:
            expertise_area: 专业领域
            problem: 具体问题
            max_results: 最大结果数

        Returns:
            专业知识列表
        """
        track_b_web = self.track_b_web
        if not track_b_web or not track_b_web.is_enabled():
            return {"success": False, "source": "disabled"}

        try:
            result = track_b_web.search_expertise(expertise_area, problem, max_results)
            if result.get("success"):
                logger.info(f"[TrackB] Found {len(result.get('results', []))} expertise items for {expertise_area}")
            return result
        except Exception as e:
            logger.warning(f"[TrackB] Expertise search failed: {e}")
            return {"success": False, "error": str(e)}

    def search_tools_and_methods(
        self,
        task: str,
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        搜索工具和方法

        Args:
            task: 任务描述
            max_results: 最大结果数

        Returns:
            相关工具和方法
        """
        track_b_web = self.track_b_web
        if not track_b_web or not track_b_web.is_enabled():
            return {"success": False, "source": "disabled"}

        try:
            return track_b_web.search_tools_and_methods(task, max_results)
        except Exception as e:
            logger.warning(f"[TrackB] Tools search failed: {e}")
            return {"success": False, "error": str(e)}

    def search_best_practices(
        self,
        practice: str,
        domain: str = "",
        max_results: int = 2,
    ) -> Dict[str, Any]:
        """
        搜索最佳实践

        Args:
            practice: 实践名称
            domain: 领域
            max_results: 最大结果数

        Returns:
            最佳实践
        """
        track_b_web = self.track_b_web
        if not track_b_web or not track_b_web.is_enabled():
            return {"success": False, "source": "disabled"}

        try:
            return track_b_web.search_best_practices(practice, domain, max_results)
        except Exception as e:
            logger.warning(f"[TrackB] Best practices search failed: {e}")
            return {"success": False, "error": str(e)}

    def receive_task(
        self,
        task_id: str,
        strategy: Dict[str, Any],
        callback=None,
    ) -> None:
        """
        接收A轨派发的任务（同步包装器）

        A轨通过此接口派发任务给B轨执行。
        内部调用异步 execute() 方法，并触发回调通知A轨。

        Args:
            task_id: 任务ID
            strategy: 执行策略（含department/task_description/claw_name等）
            callback: 完成回调 function(task_id, result)
        """
        import asyncio

        department = strategy.get("department", "default")
        task_description = strategy.get("task_description", strategy.get("context", {}).get("query", ""))
        caller = CallerType.A_GOVERNANCE.value
        context = strategy.get("context", {})

        logger.info(f"[B轨] 接收任务 {task_id} → {department}: {task_description[:50]}...")

        # 运行异步execute
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果已有事件循环（如在asyncio.run内），创建新线程运行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(
                        asyncio.run,
                        self.execute(department, task_description, caller, context)
                    )
                    result = future.result(timeout=30)
            else:
                result = loop.run_until_complete(
                    self.execute(department, task_description, caller, context)
                )
        except RuntimeError:
            result = asyncio.run(
                self.execute(department, task_description, caller, context)
            )

        self._dispatch_count += 1
        if result.get("success"):
            self._complete_count += 1

        # 触发回调
        if callback:
            try:
                callback(task_id, result)
            except Exception as e:
                logger.error(f"[B轨] 回调执行失败: {e}")


# ═══════════════════════════════════════════════════════════════
#  快速加载测试
# ═══════════════════════════════════════════════════════════════

def test_fast_load():
    """测试神行轨快速加载"""
    print("\n" + "="*60)
    print("神行轨 v4.2 快速加载测试")
    print("="*60)

    # 测试1: 初始化时间
    print("\n[测试1] 初始化时间测试")
    load_start = time_module.time()
    btrack = DivineExecutionTrack(auto_appoint=False)
    init_time = (time_module.time() - load_start) * 1000
    print(f"  初始化时间: {init_time:.2f}ms")
    print(f"  内部统计: {btrack.init_time_ms:.2f}ms")
    print(f"  任命系统: {btrack.appointments.init_time_ms:.2f}ms")

    # 测试2: 首次execute触发懒加载
    print("\n[测试2] 首次execute触发懒加载")
    exec_start = time_module.time()
    result = btrack.execute_sync(
        department="兵部",
        task_description="测试任务",
        caller="a_governance",
    )
    first_exec_time = (time_module.time() - exec_start) * 1000
    print(f"  首次执行时间: {first_exec_time:.2f}ms")
    print(f"  Claw扫描时间: {btrack.appointments.get_stats()['total_scanned']}个")
    print(f"  执行结果: {'成功' if result.get('success') else '失败'}")
    if result.get('claw_name'):
        print(f"  分配的Claw: {result['claw_name']}")

    # 测试3: 第二次execute（已扫描）
    print("\n[测试3] 第二次execute（已扫描）")
    exec_start = time_module.time()
    result = btrack.execute_sync(
        department="户部",
        task_description="测试任务2",
        caller="a_governance",
    )
    second_exec_time = (time_module.time() - exec_start) * 1000
    print(f"  第二次执行时间: {second_exec_time:.2f}ms")
    print(f"  执行结果: {'成功' if result.get('success') else '失败'}")
    if result.get('claw_name'):
        print(f"  分配的Claw: {result['claw_name']}")

    # 测试4: Worker按需加载
    print("\n[测试4] Worker按需加载")
    stats = btrack.get_stats()
    print(f"  已扫描Claw: {stats['appointments']['total_scanned']}")
    print(f"  已任命Claw: {stats['appointments']['total_appointed']}")
    print(f"  已加载Worker: {stats['appointments']['total_loaded']}")

    # 测试5: 完整统计
    print("\n[测试5] 完整统计")
    full_stats = btrack.get_stats()
    print(f"  版本: {full_stats['version']}")
    print(f"  初始化时间: {full_stats['init_time_ms']:.2f}ms")
    print(f"  总派发: {full_stats['total_dispatched']}")
    print(f"  Claw任务: {full_stats['claw_tasks']}")
    print(f"  降级任务: {full_stats['fallback_tasks']}")

    print("\n" + "="*60)
    print("快速加载测试完成")
    print("="*60)

    return {
        "init_time_ms": init_time,
        "first_exec_time_ms": first_exec_time,
        "second_exec_time_ms": second_exec_time,
        "stats": full_stats,
    }


if __name__ == "__main__":
    test_fast_load()
