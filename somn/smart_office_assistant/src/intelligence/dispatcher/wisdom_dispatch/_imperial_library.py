# -*- coding: utf-8 -*-
"""
皇家藏书阁 v1.0.0
_imperial_library.py

Somn全局记忆中心 —— 藏书阁从神之架构记忆中心升级为全系统记忆汇聚枢纽

V1.0.0 核心升级（V1.0 方向三）:
  - 格子化存储：分馆→书架→格位 三级结构
  - 8个分馆：贤者/架构/执行/学习/研究/情绪/外部/用户
  - 记忆来源扩展：6种→20种
  - 记忆分类扩展：7种→16种
  - CellRecord替代MemoryRecord，增加语义向量/跨域引用/访问统计
  - 分区持久化：按分馆+书架目录结构落盘
  - 分级权限模型：READ_ONLY/SUBMIT/WRITE/DELETE/ADMIN
  - 多维检索：按分馆/书架/贤者/岗位/Claw/时间/标签
  - 跨系统桥接接口：submit_bridge_memory / register_bridge
  - V2→V3兼容层：旧API自动适配

核心原则:
  - 不受任何团队管理（包括七人代表大会）
  - 王爵独裁制（藏书阁内部事务完全自主）
  - 自主筛选保留策略
  - 格子为本：所有记忆以格子为基本单位
  - 桥接互通：所有子系统的记忆汇聚点和分发枢纽
  - 渐进兼容：V2.0.0的所有接口在V3.0中保持向后兼容

v1.0.0 变更（YAML持久化）:
  - 新增 YAML 持久化：甲级/乙级记忆自动落盘到 data/imperial_library/
  - 新增从持久化文件恢复记忆（启动时加载）

v1.0.0新增:
  - 权限控制：所有系统各级成员可查阅藏书阁（只读）
  - 写入/删除仅限藏书阁内部人员（大学士/侍郎/编修/校理/领班）
"""

import json
import logging
import os
import time
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import asdict, dataclass, field

logger = logging.getLogger(__name__)

# v1.0.0: 从共享工具模块导入（消除重复）
from ._dispatch_utils import find_project_root as _find_project_root, find_court_config as _find_court_config


# ═══════════════════════════════════════════════════════════════
#  V1.0 类型定义
# ═══════════════════════════════════════════════════════════════

class MemoryGrade(Enum):
    """记忆分级"""
    JIA = "甲级"      # 永恒记忆 - 永不删除
    YI = "乙级"       # 长期记忆 - 1年审查
    BING = "丙级"     # 短期记忆 - 30天审查
    DING = "丁级"     # 待定记忆 - 7天自动清理


class LibraryWing(Enum):
    """V1.0 分馆（一级分类）"""
    SAGE = "贤者分馆"         # 贤者能力画像/智慧编码/Claw记忆
    ARCH = "架构分馆"         # 神之架构决策/调度记录/岗位变动
    EXEC = "执行分馆"         # 任务执行记录/结果/ROI数据
    LEARN = "学习分馆"        # 三层学习模型/策略/经验沉淀
    RESEARCH = "研究分馆"     # 研究发现/策略/颗粒度评估
    EMOTION = "情绪分馆"      # 消费情绪/感性决策研究
    EXTERNAL = "外部分馆"     # OpenClaw抓取的外部知识
    USER = "用户分馆"         # 用户画像/偏好/历史

    @property
    def code(self) -> str:
        """分馆编码"""
        return self.name  # e.g. "SAGE", "ARCH"


class MemorySource(Enum):
    """V1.0 扩展记忆来源（6→20种）"""
    # V2.0 原有6种
    DEPARTMENT_RESULT = "部门工作结果"
    TALENT_EVALUATION = "人才能力评估"
    HISTORICAL_DECISION = "历史决策存档"
    HANLIN_REVIEW = "翰林院审核记录"
    CONGRESS_VOTE = "代表大会投票记录"
    SYSTEM_EVENT = "系统事件"
    # V1.0 新增16种
    CLAW_EXECUTION = "Claw执行记录"
    CLAW_MEMORY = "Claw运行记忆"
    SAGE_ENCODING = "贤者智慧编码"
    SAGE_DISTILLATION = "贤者蒸馏文档"
    NEURAL_MEMORY = "神经记忆系统"
    SUPER_MEMORY = "超级神经记忆"
    LEARNING_STRATEGY = "学习策略"
    RESEARCH_FINDING = "研究发现"
    EMOTION_RESEARCH = "情绪研究"
    OPENCLAW_FETCH = "OpenClaw抓取"
    ROI_TRACKING = "ROI追踪"
    USER_INTERACTION = "用户交互"
    SYSTEM_PERFORMANCE = "系统性能"
    BRIDGE_REPORT = "桥接汇报"


class MemoryCategory(Enum):
    """V1.0 扩展记忆分类（7→16种）"""
    # V2.0 原有7种
    ARCHITECTURE = "架构决策"
    WORK_RESULT = "工作成果"
    TALENT_PROFILE = "人才画像"
    METHODOLOGY = "方法论"
    REVIEW_RECORD = "审核记录"
    EXECUTION_LOG = "执行日志"
    OTHER = "其他"
    # V1.0 新增9种
    SAGE_WISDOM = "贤者智慧"
    CLAW_OUTPUT = "Claw产出"
    LEARNING_INSIGHT = "学习洞察"
    RESEARCH_INSIGHT = "研究洞察"
    EMOTION_PATTERN = "情绪模式"
    EXTERNAL_KNOWLEDGE = "外部知识"
    USER_PREFERENCE = "用户偏好"
    SYSTEM_METRICS = "系统指标"
    CROSS_DOMAIN = "跨域关联"


class LibraryPermission(Enum):
    """V1.0 权限等级"""
    READ_ONLY = "read_only"      # 只读（全系统默认）
    SUBMIT = "submit"             # 提交记忆（子系统自动汇报）
    WRITE = "write"               # 写入/修改（格子管理员）
    DELETE = "delete"             # 删除（大学士级）
    ADMIN = "admin"               # 管理配置（大学士独享）


# ═══════════════════════════════════════════════════════════════
#  V1.0 书架预设（分馆→书架映射）
# ═══════════════════════════════════════════════════════════════

# 每个分馆的默认书架配置
WING_SHELVES: Dict[LibraryWing, List[str]] = {
    LibraryWing.SAGE: [
        "sage_profiles",      # 贤者能力画像
        "sage_codes",         # 智慧编码
        "claw_memories",      # Claw运行时记忆
        "distillation",       # 蒸馏文档索引
        "sage_evaluation",    # 贤者能力评估
    ],
    LibraryWing.ARCH: [
        "court_decisions",    # 朝廷决策
        "scheduling",         # 调度记录
        "position_changes",   # 岗位变动
        "upgrade_history",    # 升级历史
        "architecture_docs",  # 架构文档
    ],
    LibraryWing.EXEC: [
        "task_results",       # 任务执行结果
        "roi_data",           # ROI数据
        "performance",        # 执行效能
        "workflow_logs",      # 工作流日志
    ],
    LibraryWing.LEARN: [
        "learning_strategies",  # 学习策略
        "experience",          # 经验沉淀
        "skill_acquisition",   # 技能习得
        "adaptive_records",    # 适应性记录
    ],
    LibraryWing.RESEARCH: [
        "research_findings",   # 研究发现
        "strategy_insights",   # 策略洞察
        "depth_assessments",   # 深度评估
        "phase_records",       # 阶段记录
    ],
    LibraryWing.EMOTION: [
        "emotion_patterns",    # 情绪模式
        "consumer_behavior",   # 消费行为
        "sentiment_analysis",  # 情绪分析
        "decision_factors",    # 决策因子
    ],
    LibraryWing.EXTERNAL: [
        "web_knowledge",       # 网络知识
        "api_data",            # API数据
        "file_imports",        # 文件导入
        "rss_feeds",           # RSS订阅
    ],
    LibraryWing.USER: [
        "user_profiles",       # 用户画像
        "preferences",         # 偏好设置
        "interaction_history", # 交互历史
        "feedback",            # 用户反馈
    ],
}


# ═══════════════════════════════════════════════════════════════
#  V1.0 数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class CellRecord:
    """V1.0 格子化记忆条目"""
    id: str                                        # 格位唯一标识：{WING}_{SHELF}_{SEQ:06d}
    wing: LibraryWing                              # 分馆
    shelf: str                                     # 书架
    cell_index: int                                # 格位编号
    title: str                                     # 记忆标题
    content: str                                   # 记忆内容
    grade: MemoryGrade                             # 分级（甲乙丙丁）
    source: MemorySource                           # 来源（22种）
    category: MemoryCategory                       # 分类（16种）
    reporting_system: str                          # 汇报子系统
    created_at: float = field(default_factory=time.time)
    last_reviewed: float = 0.0
    review_count: int = 0
    value_score: float = 0.5
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    # V1.0 新增字段
    associated_sage: str = ""                      # 关联贤者
    associated_position: str = ""                  # 关联岗位
    associated_claw: str = ""                      # 关联Claw
    semantic_embedding: Optional[List[float]] = None  # 语义向量
    cross_references: List[str] = field(default_factory=list)  # 跨格子引用ID列表
    access_count: int = 0                          # 访问次数
    last_accessed: float = 0.0                     # 最后访问时间

    @property
    def age_days(self) -> float:
        return (time.time() - self.created_at) / 86400

    def touch(self) -> None:
        """记录访问（更新访问计数和时间）"""
        self.access_count += 1
        self.last_accessed = time.time()

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        d = {
            "id": self.id,
            "wing": self.wing.value,
            "wing_code": self.wing.code,
            "shelf": self.shelf,
            "cell_index": self.cell_index,
            "title": self.title,
            "content": self.content,
            "grade": self.grade.value,
            "source": self.source.value,
            "category": self.category.value,
            "reporting_system": self.reporting_system,
            "created_at": self.created_at,
            "last_reviewed": self.last_reviewed,
            "review_count": self.review_count,
            "value_score": self.value_score,
            "tags": self.tags,
            "metadata": self.metadata,
            "associated_sage": self.associated_sage,
            "associated_position": self.associated_position,
            "associated_claw": self.associated_claw,
            "cross_references": self.cross_references,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed,
        }
        # 语义向量较大，仅在非空时序列化
        if self.semantic_embedding:
            d["semantic_embedding"] = self.semantic_embedding
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CellRecord":
        """从字典反序列化"""
        wing_code = data.get("wing_code", data.get("wing", "ARCH"))
        # 兼容V3.0 wing_code格式（name如"SAGE"）和中文格式（value如"贤者分馆"）
        try:
            # 先尝试name匹配（用枚举成员访问语法）
            wing = LibraryWing[wing_code]
        except (KeyError, ValueError):
            # 再尝试value匹配
            try:
                wing = next(w for w in LibraryWing if w.value == wing_code)
            except StopIteration:
                wing = LibraryWing.ARCH

        # 兼容旧source/category格式
        source_value = data.get("source", "SYSTEM_EVENT")
        try:
            source = MemorySource(source_value)
        except ValueError:
            source = MemorySource.SYSTEM_EVENT

        category_value = data.get("category", "OTHER")
        try:
            category = MemoryCategory(category_value)
        except ValueError:
            category = MemoryCategory.OTHER

        grade_value = data.get("grade", "DING")
        try:
            grade = MemoryGrade(grade_value)
        except ValueError:
            grade = MemoryGrade.DING

        return cls(
            id=data.get("id", ""),
            wing=wing,
            shelf=data.get("shelf", "default"),
            cell_index=data.get("cell_index", 0),
            title=data.get("title", ""),
            content=data.get("content", ""),
            grade=grade,
            source=source,
            category=category,
            reporting_system=data.get("reporting_system", data.get("reporting_department", "")),
            created_at=data.get("created_at", time.time()),
            last_reviewed=data.get("last_reviewed", 0.0),
            review_count=data.get("review_count", 0),
            value_score=data.get("value_score", 0.5),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
            associated_sage=data.get("associated_sage", ""),
            associated_position=data.get("associated_position", ""),
            associated_claw=data.get("associated_claw", ""),
            semantic_embedding=data.get("semantic_embedding"),
            cross_references=data.get("cross_references", []),
            access_count=data.get("access_count", 0),
            last_accessed=data.get("last_accessed", 0.0),
        )


# ═══════════════════════════════════════════════════════════════
#  V2→V3 兼容：保留旧 MemoryRecord 供旧代码使用
# ═══════════════════════════════════════════════════════════════

@dataclass
class MemoryRecord:
    """V2.0 兼容层 - 旧记忆条目格式

    V1.0中保留此类，旧代码继续使用。内部自动转换到CellRecord。
    """
    id: str
    title: str
    content: str
    source: MemorySource
    category: MemoryCategory
    grade: MemoryGrade
    reporting_department: str
    created_at: float = field(default_factory=time.time)
    last_reviewed: float = 0.0
    review_count: int = 0
    value_score: float = 0.5
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def age_days(self) -> float:
        return (time.time() - self.created_at) / 86400


# ═══════════════════════════════════════════════════════════════
#  V1.0 分馆权限配置
# ═══════════════════════════════════════════════════════════════

WING_PERMISSIONS: Dict[str, Dict[str, Any]] = {
    "SAGE": {
        "managers": ["扬雄", "左丘明", "班固"],
        "writers": ["司马迁", "司马光", "藏书阁专员团队"],
        "description": "贤者能力画像与智慧编码",
    },
    "ARCH": {
        "managers": ["扬雄", "左丘明"],
        "writers": ["司马迁", "班固", "司马光"],
        "description": "神之架构决策与调度记录",
    },
    "EXEC": {
        "managers": ["司马光"],
        "writers": ["司马迁", "班固"],
        "description": "任务执行与ROI数据",
    },
    "LEARN": {
        "managers": ["班固"],
        "writers": ["司马迁", "司马光"],
        "description": "三层学习模型与经验沉淀",
    },
    "RESEARCH": {
        "managers": ["左丘明", "班固"],
        "writers": ["司马迁", "扬雄"],
        "description": "研究发现与策略洞察",
    },
    "EMOTION": {
        "managers": ["班固"],
        "writers": ["司马迁"],
        "description": "情绪研究与感性决策",
    },
    "EXTERNAL": {
        "managers": ["扬雄"],
        "writers": ["司马迁", "藏书阁专员团队"],
        "description": "OpenClaw外部知识",
    },
    "USER": {
        "managers": ["司马迁"],
        "writers": ["司马光", "藏书阁专员团队"],
        "description": "用户画像与偏好",
    },
}


# ═══════════════════════════════════════════════════════════════
#  V1.0 藏书阁核心引擎
# ═══════════════════════════════════════════════════════════════

class ImperialLibrary:
    """
    皇家藏书阁 V1.0 —— Somn全局记忆中心

    王爵: 司马迁
    职责: 记录一切有价值的工作成果、人才能力、历史决策
    范围: 从神之架构记忆中心扩展到Somn全系统记忆汇聚枢纽
    原则: 不受任何团队管理，自主决策记忆保留
    """

    # 王爵信息
    CHANCELLOR = "司马迁"
    CHANCELLOR_TITLE = "藏书阁大学士·王爵"
    CHANCELLOR_NICKNAME = "太史公"

    # 藏书阁内部人员（拥有写入/删除权限）
    _LIBRARY_STAFF = {"司马迁", "左丘明", "班固", "司马光", "扬雄", "藏书阁专员团队"}

    # 价值评估关键词（提升评分）
    _VALUE_KEYWORDS = {
        "架构升级": 0.3, "重大突破": 0.3, "核心方法论": 0.25,
        "实战成果": 0.2, "创新": 0.2, "跨部门协作": 0.15,
        "用户反馈": 0.2, "验证通过": 0.15, "全链路": 0.15,
        "全量通过": 0.2, "100%": 0.15, "V1.0": 0.15,
        "全局打通": 0.2, "子系统": 0.1, "跨域引用": 0.15,
    }

    def __init__(self):
        # ── V1.0 格子化存储 ──
        self._cells: Dict[str, CellRecord] = {}            # id → CellRecord
        self._wing_shelf_index: Dict[str, Dict[str, List[str]]] = {}  # wing → shelf → [cell_ids]
        self._tag_index: Dict[str, Set[str]] = {}           # tag → {cell_ids}
        self._sage_index: Dict[str, Set[str]] = {}          # sage → {cell_ids}
        self._position_index: Dict[str, Set[str]] = {}      # position → {cell_ids}
        self._claw_index: Dict[str, Set[str]] = {}          # claw → {cell_ids}
        self._system_index: Dict[str, Set[str]] = {}        # reporting_system → {cell_ids}
        self._cell_counters: Dict[str, int] = {}            # "{wing}_{shelf}" → next_cell_index
        self._next_legacy_id = 1                            # V2兼容：旧LIB_xxxxx格式ID

        # ── V1.0 跨系统桥接注册 ──
        self._bridges: Dict[str, Any] = {}                  # subsystem_name → bridge_config

        # ── 统计 ──
        self._stats = {
            "total_records": 0,
            "total_submissions": 0,
            "auto_cleaned": 0,
            "manual_retained": 0,
            "bridge_submissions": 0,
            "cross_references_created": 0,
        }

        # ── V2.0 持久化（保留）──
        self._storage_path: Optional[Path] = None
        self._auto_save_interval: int = 300
        self._last_save_time: float = 0.0
        self._dirty: bool = False

        # 初始化
        self._init_persistence()
        self._init_wing_shelf_index()
        self._load_from_disk_v3()

    # ──────────────────────────────────────────────────────────
    #  初始化
    # ──────────────────────────────────────────────────────────

    def _init_wing_shelf_index(self) -> None:
        """初始化分馆→书架索引结构"""
        for wing, shelves in WING_SHELVES.items():
            wing_key = wing.code
            self._wing_shelf_index[wing_key] = {}
            for shelf in shelves:
                self._wing_shelf_index[wing_key][shelf] = []
                counter_key = f"{wing_key}_{shelf}"
                if counter_key not in self._cell_counters:
                    self._cell_counters[counter_key] = 1

    def _init_persistence(self) -> None:
        """从配置文件初始化持久化设置"""
        try:
            config_path = self._find_court_config()
            if config_path and config_path.exists():
                import yaml
                with open(config_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f) or {}

                lib_config = config.get("imperial_library", {})
                persistence = lib_config.get("persistence", {})

                if persistence.get("enabled", True):
                    storage_dir = persistence.get("storage_path", "data/imperial_library")
                    self._storage_path = self._find_project_root() / storage_dir
                    self._storage_path.mkdir(parents=True, exist_ok=True)
                    self._auto_save_interval = persistence.get("auto_save_interval", 300)

                    logger.info(
                        f"藏书阁V1.0持久化已启用: {self._storage_path}, "
                        f"自动保存间隔={self._auto_save_interval}s"
                    )
        except Exception as e:
            logger.debug(f"藏书阁V1.0持久化初始化失败（将使用纯内存模式）: {e}")

    def _load_from_disk_v3(self) -> int:
        """V1.0 从磁盘恢复记忆（分区持久化格式）"""
        if not self._storage_path:
            return self._load_from_disk_v2_legacy()

        total_loaded = 0

        # V1.0: 从 wings/ 目录加载
        wings_dir = self._storage_path / "wings"
        if wings_dir.exists():
            for wing_dir in wings_dir.iterdir():
                if not wing_dir.is_dir():
                    continue
                wing_code = wing_dir.name  # e.g. "SAGE"
                for shelf_dir in wing_dir.iterdir():
                    if not shelf_dir.is_dir():
                        continue
                    shelf_name = shelf_dir.name  # e.g. "sage_profiles"
                    for cell_file in shelf_dir.glob("CELL_*.yaml"):
                        try:
                            import yaml
                            with open(cell_file, "r", encoding="utf-8") as f:
                                data = yaml.safe_load(f)
                            if not data or not isinstance(data, dict):
                                continue

                            record = CellRecord.from_dict(data)
                            self._cells[record.id] = record
                            self._add_to_indexes(record)
                            total_loaded += 1

                            # 更新计数器
                            counter_key = f"{wing_code}_{shelf_name}"
                            if record.cell_index >= self._cell_counters.get(counter_key, 0):
                                self._cell_counters[counter_key] = record.cell_index + 1

                        except Exception as e:
                            logger.debug(f"V1.0记忆文件加载失败 [{cell_file}]: {e}")

        # V2.0 兼容：从旧格式 LIB_*.yaml 加载
        total_loaded += self._load_from_disk_v2_legacy()

        if total_loaded > 0:
            self._stats["total_records"] = len(self._cells)
            logger.info(f"藏书阁V1.0从磁盘恢复 {total_loaded} 条记忆")

        return total_loaded

    def _load_from_disk_v2_legacy(self) -> int:
        """V2.0 兼容：从旧格式文件迁移记忆"""
        if not self._storage_path:
            return 0

        loaded = 0
        try:
            for file_path in self._storage_path.glob("LIB_*.yaml"):
                try:
                    import yaml
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    if not data or not isinstance(data, dict):
                        continue

                    # 将V2格式转换为CellRecord
                    source_value = data.get("source", "SYSTEM_EVENT")
                    try:
                        source = MemorySource(source_value)
                    except ValueError:
                        source = MemorySource.SYSTEM_EVENT

                    category_value = data.get("category", "OTHER")
                    try:
                        category = MemoryCategory(category_value)
                    except ValueError:
                        category = MemoryCategory.OTHER

                    grade_value = data.get("grade", "DING")
                    try:
                        grade = MemoryGrade(grade_value)
                    except ValueError:
                        grade = MemoryGrade.DING

                    # 自动归类到ARCH分馆（旧数据默认归入架构分馆）
                    wing = LibraryWing.ARCH
                    shelf = "court_decisions"

                    counter_key = f"{wing.code}_{shelf}"
                    cell_index = self._cell_counters.get(counter_key, 1)

                    cell_id = f"{wing.code}_{shelf}_{cell_index:06d}"
                    self._cell_counters[counter_key] = cell_index + 1

                    # 更新旧ID计数器
                    try:
                        num = int(data.get("id", "LIB_00001").replace("LIB_", ""))
                        if num >= self._next_legacy_id:
                            self._next_legacy_id = num + 1
                    except ValueError:
                        pass

                    record = CellRecord(
                        id=cell_id,
                        wing=wing,
                        shelf=shelf,
                        cell_index=cell_index,
                        title=data.get("title", ""),
                        content=data.get("content", ""),
                        grade=grade,
                        source=source,
                        category=category,
                        reporting_system=data.get("reporting_department", ""),
                        created_at=data.get("created_at", time.time()),
                        last_reviewed=data.get("last_reviewed", 0.0),
                        review_count=data.get("review_count", 0),
                        value_score=data.get("value_score", 0.5),
                        tags=data.get("tags", []),
                        metadata=data.get("metadata", {}),
                        # 保留旧ID到metadata中
                        metadata_legacy_id=data.get("id", ""),
                    )
                    # 把旧ID写入metadata
                    record.metadata["v2_legacy_id"] = data.get("id", "")

                    self._cells[cell_id] = record
                    self._add_to_indexes(record)
                    loaded += 1

                except Exception as e:
                    logger.debug(f"V2.0兼容加载失败 [{file_path}]: {e}")

            if loaded > 0:
                logger.info(f"藏书阁V1.0从V2.0格式迁移 {loaded} 条记忆")
                # 将旧格式文件移到v2_archive目录
                self._archive_v2_files()

        except Exception as e:
            logger.warning(f"V2.0兼容迁移异常: {e}")

        return loaded

    def _archive_v2_files(self) -> None:
        """将V2格式的旧文件归档"""
        if not self._storage_path:
            return
        archive_dir = self._storage_path / "v2_archive"
        try:
            archive_dir.mkdir(parents=True, exist_ok=True)
            for file_path in list(self._storage_path.glob("LIB_*.yaml")):
                target = archive_dir / file_path.name
                if not target.exists():
                    file_path.rename(target)
        except Exception as e:
            logger.debug(f"V2文件归档失败: {e}")

    # ──────────────────────────────────────────────────────────
    #  索引管理
    # ──────────────────────────────────────────────────────────

    def _add_to_indexes(self, record: CellRecord) -> None:
        """将记录添加到所有索引"""
        rid = record.id
        wing_key = record.wing.code
        shelf_name = record.shelf

        # 分馆→书架索引
        if wing_key not in self._wing_shelf_index:
            self._wing_shelf_index[wing_key] = {}
        if shelf_name not in self._wing_shelf_index[wing_key]:
            self._wing_shelf_index[wing_key][shelf_name] = []
        if rid not in self._wing_shelf_index[wing_key][shelf_name]:
            self._wing_shelf_index[wing_key][shelf_name].append(rid)

        # 标签索引
        for tag in record.tags:
            if tag not in self._tag_index:
                self._tag_index[tag] = set()
            self._tag_index[tag].add(rid)

        # 贤者索引
        if record.associated_sage:
            if record.associated_sage not in self._sage_index:
                self._sage_index[record.associated_sage] = set()
            self._sage_index[record.associated_sage].add(rid)

        # 岗位索引
        if record.associated_position:
            if record.associated_position not in self._position_index:
                self._position_index[record.associated_position] = set()
            self._position_index[record.associated_position].add(rid)

        # Claw索引
        if record.associated_claw:
            if record.associated_claw not in self._claw_index:
                self._claw_index[record.associated_claw] = set()
            self._claw_index[record.associated_claw].add(rid)

        # 系统索引
        if record.reporting_system:
            if record.reporting_system not in self._system_index:
                self._system_index[record.reporting_system] = set()
            self._system_index[record.reporting_system].add(rid)

    def _remove_from_indexes(self, record: CellRecord) -> None:
        """将记录从所有索引移除"""
        rid = record.id
        wing_key = record.wing.code
        shelf_name = record.shelf

        if wing_key in self._wing_shelf_index and shelf_name in self._wing_shelf_index[wing_key]:
            if rid in self._wing_shelf_index[wing_key][shelf_name]:
                self._wing_shelf_index[wing_key][shelf_name].remove(rid)

        for tag in record.tags:
            if tag in self._tag_index:
                self._tag_index[tag].discard(rid)

        if record.associated_sage and record.associated_sage in self._sage_index:
            self._sage_index[record.associated_sage].discard(rid)

        if record.associated_position and record.associated_position in self._position_index:
            self._position_index[record.associated_position].discard(rid)

        if record.associated_claw and record.associated_claw in self._claw_index:
            self._claw_index[record.associated_claw].discard(rid)

        if record.reporting_system and record.reporting_system in self._system_index:
            self._system_index[record.reporting_system].discard(rid)

    # ──────────────────────────────────────────────────────────
    #  权限检查（V1.0 分级）
    # ──────────────────────────────────────────────────────────

    def _check_permission(
        self, operator: str = "", required: LibraryPermission = LibraryPermission.READ_ONLY
    ) -> bool:
        """
        V1.0 分级权限检查

        READ_ONLY: 全系统可访问
        SUBMIT: 任何子系统可提交记忆（汇报是义务）
        WRITE: 仅藏书阁内部人员 + 分馆管理员
        DELETE: 仅藏书阁内部人员
        ADMIN: 仅大学士（司马迁）
        """
        if not operator:
            return True  # 系统内部调用

        # ADMIN: 只有大学士
        if required == LibraryPermission.ADMIN:
            return operator == self.CHANCELLOR

        # DELETE/WRITE: 藏书阁内部人员
        if required in (LibraryPermission.DELETE, LibraryPermission.WRITE):
            return operator in self._LIBRARY_STAFF

        # SUBMIT: 任何人均可提交
        return True

    def _check_wing_write_permission(self, operator: str, wing: LibraryWing) -> bool:
        """检查对特定分馆的写入权限"""
        if not operator or operator in self._LIBRARY_STAFF:
            return True
        wing_config = WING_PERMISSIONS.get(wing.code, {})
        return operator in wing_config.get("writers", [])

    @staticmethod
    def is_read_only_for(operator: str) -> bool:
        """判断某人对藏书阁是否只有只读权限"""
        return operator not in ImperialLibrary._LIBRARY_STAFF

    # ──────────────────────────────────────────────────────────
    #  V1.0 核心记忆收录
    # ──────────────────────────────────────────────────────────

    def submit_cell(
        self,
        title: str,
        content: str,
        wing: LibraryWing,
        shelf: str,
        source: MemorySource,
        category: MemoryCategory,
        reporting_system: str = "",
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
        suggested_grade: Optional[MemoryGrade] = None,
        associated_sage: str = "",
        associated_position: str = "",
        associated_claw: str = "",
        operator: str = "",
    ) -> CellRecord:
        """
        V1.0 格子化记忆收录接口

        按分馆+书架定位格位，自动分配格位编号。

        Args:
            title: 记忆标题
            content: 记忆内容
            wing: 分馆
            shelf: 书架名称
            source: 记忆来源
            category: 记忆分类
            reporting_system: 汇报子系统
            tags: 标签列表
            metadata: 元数据
            suggested_grade: 建议分级
            associated_sage: 关联贤者
            associated_position: 关联岗位
            associated_claw: 关联Claw
            operator: 操作者

        Returns:
            CellRecord
        """
        self._stats["total_submissions"] += 1

        # 自动分配格位
        counter_key = f"{wing.code}_{shelf}"
        cell_index = self._cell_counters.get(counter_key, 1)
        self._cell_counters[counter_key] = cell_index + 1

        cell_id = f"{wing.code}_{shelf}_{cell_index:06d}"

        # 价值评估
        value_score = self._evaluate_value(title, content, tags or [])

        # 自主决定保留等级
        grade = suggested_grade or self._decide_grade(value_score, category)

        record = CellRecord(
            id=cell_id,
            wing=wing,
            shelf=shelf,
            cell_index=cell_index,
            title=title,
            content=content,
            grade=grade,
            source=source,
            category=category,
            reporting_system=reporting_system,
            value_score=value_score,
            tags=tags or [],
            metadata=metadata or {},
            associated_sage=associated_sage,
            associated_position=associated_position,
            associated_claw=associated_claw,
        )

        self._cells[cell_id] = record
        self._add_to_indexes(record)
        self._stats["total_records"] += 1
        self._dirty = True

        logger.info(
            f"藏书阁V1.0收录: [{cell_id}] {title} "
            f"(分馆={wing.value}, 书架={shelf}, 等级={grade.value}, 价值={value_score:.2f})"
        )

        self._try_auto_save()
        return record

    # ── V2.0 兼容接口 ──

    def submit_memory(
        self,
        title: str,
        content: str,
        source: MemorySource,
        category: MemoryCategory,
        reporting_department: str,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
        suggested_grade: Optional[MemoryGrade] = None,
        operator: str = "",
    ) -> MemoryRecord:
        """
        V2.0 兼容接口 - 旧代码继续使用

        内部自动转换为CellRecord存储，返回MemoryRecord供旧代码使用。
        """
        self._stats["total_submissions"] += 1

        # 价值评估
        value_score = self._evaluate_value(title, content, tags or [])
        grade = suggested_grade or self._decide_grade(value_score, category)

        # 归入ARCH分馆
        wing = LibraryWing.ARCH
        shelf = "court_decisions"
        counter_key = f"{wing.code}_{shelf}"
        cell_index = self._cell_counters.get(counter_key, 1)
        self._cell_counters[counter_key] = cell_index + 1
        cell_id = f"{wing.code}_{shelf}_{cell_index:06d}"

        # 构建CellRecord
        cell = CellRecord(
            id=cell_id,
            wing=wing,
            shelf=shelf,
            cell_index=cell_index,
            title=title,
            content=content,
            grade=grade,
            source=source,
            category=category,
            reporting_system=reporting_department,
            value_score=value_score,
            tags=tags or [],
            metadata=metadata or {},
        )

        self._cells[cell_id] = cell
        self._add_to_indexes(cell)
        self._stats["total_records"] += 1
        self._dirty = True

        # 返回V2格式的MemoryRecord（兼容旧代码）
        legacy_record = MemoryRecord(
            id=cell_id,
            title=title,
            content=content,
            source=source,
            category=category,
            grade=grade,
            reporting_department=reporting_department,
            value_score=value_score,
            tags=tags or [],
            metadata=metadata or {},
        )

        logger.info(
            f"藏书阁V1.0收录(V2兼容): [{cell_id}] {title} "
            f"(等级={grade.value}, 价值={value_score:.2f}, 来源={reporting_department})"
        )

        self._try_auto_save()
        return legacy_record

    # ──────────────────────────────────────────────────────────
    #  V1.0 跨系统桥接
    # ──────────────────────────────────────────────────────────

    def register_bridge(self, subsystem_name: str, config: Dict[str, Any]) -> bool:
        """
        注册子系统桥接

        Args:
            subsystem_name: 子系统名称
            config: 桥接配置 {
                "wing": LibraryWing,
                "default_shelf": str,
                "source": MemorySource,
                "auto_submit": bool,
            }

        Returns:
            注册成功
        """
        self._bridges[subsystem_name] = config
        logger.info(f"藏书阁V1.0桥接注册: {subsystem_name} → {config.get('wing')}")
        return True

    def submit_bridge_memory(
        self,
        subsystem_name: str,
        title: str,
        content: str,
        category: MemoryCategory = MemoryCategory.OTHER,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
        associated_sage: str = "",
        associated_position: str = "",
        associated_claw: str = "",
    ) -> Optional[CellRecord]:
        """
        子系统通过桥接接口提交记忆

        自动使用注册时配置的分馆/书架/来源。

        Args:
            subsystem_name: 子系统名称（需已注册）
            title: 记忆标题
            content: 记忆内容
            category: 记忆分类
            tags: 标签
            metadata: 元数据
            associated_sage: 关联贤者
            associated_position: 关联岗位
            associated_claw: 关联Claw

        Returns:
            CellRecord 或 None（如果子系统未注册）
        """
        bridge = self._bridges.get(subsystem_name)
        if not bridge:
            logger.warning(f"桥接提交失败: 子系统 '{subsystem_name}' 未注册")
            return None

        self._stats["bridge_submissions"] += 1

        return self.submit_cell(
            title=title,
            content=content,
            wing=bridge["wing"],
            shelf=bridge.get("default_shelf", "default"),
            source=bridge.get("source", MemorySource.BRIDGE_REPORT),
            category=category,
            reporting_system=subsystem_name,
            tags=tags,
            metadata=metadata,
            associated_sage=associated_sage,
            associated_position=associated_position,
            associated_claw=associated_claw,
        )

    # ──────────────────────────────────────────────────────────
    #  V1.0 多维查询
    # ──────────────────────────────────────────────────────────

    def query_cells(
        self,
        wing: Optional[LibraryWing] = None,
        shelf: Optional[str] = None,
        grade: Optional[MemoryGrade] = None,
        source: Optional[MemorySource] = None,
        category: Optional[MemoryCategory] = None,
        reporting_system: Optional[str] = None,
        keyword: Optional[str] = None,
        tags: Optional[List[str]] = None,
        associated_sage: Optional[str] = None,
        associated_position: Optional[str] = None,
        associated_claw: Optional[str] = None,
        min_value_score: float = 0.0,
        limit: int = 50,
        sort_by: str = "value_score",  # value_score | created_at | access_count
    ) -> List[CellRecord]:
        """
        V1.0 多维查询接口

        支持按分馆/书架/分级/来源/分类/子系统/关键词/标签/贤者/岗位/Claw/价值评分等多维筛选。
        """
        results = list(self._cells.values())

        # 分馆筛选
        if wing:
            wing_key = wing.code
            if wing_key in self._wing_shelf_index:
                wing_ids = set()
                for shelf_ids in self._wing_shelf_index[wing_key].values():
                    wing_ids.update(shelf_ids)
                results = [r for r in results if r.id in wing_ids]

        # 书架筛选
        if shelf and wing:
            wing_key = wing.code
            if wing_key in self._wing_shelf_index and shelf in self._wing_shelf_index[wing_key]:
                shelf_ids = set(self._wing_shelf_index[wing_key][shelf])
                results = [r for r in results if r.id in shelf_ids]

        # 分级筛选
        if grade:
            results = [r for r in results if r.grade == grade]

        # 来源筛选
        if source:
            results = [r for r in results if r.source == source]

        # 分类筛选
        if category:
            results = [r for r in results if r.category == category]

        # 子系统筛选
        if reporting_system:
            results = [r for r in results if r.reporting_system == reporting_system]

        # 关键词筛选
        if keyword:
            kw_lower = keyword.lower()
            results = [
                r for r in results
                if keyword in r.title or keyword in r.content
                or any(keyword in t for t in r.tags)
                or kw_lower in r.title.lower() or kw_lower in r.content.lower()
            ]

        # 标签筛选
        if tags:
            tag_set = set(tags)
            results = [r for r in results if tag_set.intersection(set(r.tags))]

        # 贤者筛选
        if associated_sage:
            sage_ids = self._sage_index.get(associated_sage, set())
            results = [r for r in results if r.id in sage_ids]

        # 岗位筛选
        if associated_position:
            pos_ids = self._position_index.get(associated_position, set())
            results = [r for r in results if r.id in pos_ids]

        # Claw筛选
        if associated_claw:
            claw_ids = self._claw_index.get(associated_claw, set())
            results = [r for r in results if r.id in claw_ids]

        # 价值评分筛选
        if min_value_score > 0:
            results = [r for r in results if r.value_score >= min_value_score]

        # 排序
        if sort_by == "created_at":
            results.sort(key=lambda r: r.created_at, reverse=True)
        elif sort_by == "access_count":
            results.sort(key=lambda r: r.access_count, reverse=True)
        else:  # value_score
            results.sort(key=lambda r: r.value_score, reverse=True)

        # 访问记录
        for r in results[:min(limit, 20)]:  # 最多记录前20条的访问
            r.touch()

        return results[:limit]

    def get_cell(self, cell_id: str) -> Optional[CellRecord]:
        """获取单个格位记录"""
        record = self._cells.get(cell_id)
        if record:
            record.touch()
        return record

    # V2兼容查询接口
    def query_memories(
        self,
        grade: Optional[MemoryGrade] = None,
        category: Optional[MemoryCategory] = None,
        source: Optional[MemorySource] = None,
        department: Optional[str] = None,
        keyword: Optional[str] = None,
        limit: int = 50,
    ) -> List[MemoryRecord]:
        """V2.0 兼容查询接口"""
        cells = self.query_cells(
            wing=LibraryWing.ARCH,  # 旧数据默认在ARCH
            grade=grade,
            source=source,
            category=category,
            reporting_system=department,
            keyword=keyword,
            limit=limit,
        )
        # 转换为V2格式
        return [
            MemoryRecord(
                id=c.id,
                title=c.title,
                content=c.content,
                source=c.source,
                category=c.category,
                grade=c.grade,
                reporting_department=c.reporting_system,
                created_at=c.created_at,
                last_reviewed=c.last_reviewed,
                review_count=c.review_count,
                value_score=c.value_score,
                tags=c.tags,
                metadata=c.metadata,
            )
            for c in cells
        ]

    def get_memory(self, record_id: str) -> Optional[MemoryRecord]:
        """V2.0 兼容单条查询"""
        cell = self.get_cell(record_id)
        if not cell:
            return None
        return MemoryRecord(
            id=cell.id,
            title=cell.title,
            content=cell.content,
            source=cell.source,
            category=cell.category,
            grade=cell.grade,
            reporting_department=cell.reporting_system,
            created_at=cell.created_at,
            value_score=cell.value_score,
            tags=cell.tags,
            metadata=cell.metadata,
        )

    # ──────────────────────────────────────────────────────────
    #  V1.0 跨域引用
    # ──────────────────────────────────────────────────────────

    def add_cross_reference(self, from_id: str, to_id: str) -> bool:
        """添加跨域引用"""
        if from_id not in self._cells or to_id not in self._cells:
            return False
        if to_id not in self._cells[from_id].cross_references:
            self._cells[from_id].cross_references.append(to_id)
            self._stats["cross_references_created"] += 1
            self._dirty = True
        return True

    def get_cross_references(self, cell_id: str) -> List[CellRecord]:
        """获取某格位的所有跨域引用记录"""
        cell = self._cells.get(cell_id)
        if not cell:
            return []
        return [self._cells[ref_id] for ref_id in cell.cross_references if ref_id in self._cells]

    # ──────────────────────────────────────────────────────────
    #  V1.0 分馆/书架管理
    # ──────────────────────────────────────────────────────────

    def get_wing_stats(self, wing: Optional[LibraryWing] = None) -> Dict[str, Any]:
        """获取分馆统计"""
        if wing:
            wing_key = wing.code
            stats = {"wing": wing.value, "total_cells": 0, "shelves": {}}
            if wing_key in self._wing_shelf_index:
                for shelf_name, cell_ids in self._wing_shelf_index[wing_key].items():
                    shelf_cells = [self._cells[cid] for cid in cell_ids if cid in self._cells]
                    grade_dist = {}
                    for g in MemoryGrade:
                        grade_dist[g.value] = sum(1 for c in shelf_cells if c.grade == g)
                    stats["shelves"][shelf_name] = {
                        "count": len(shelf_cells),
                        "grade_distribution": grade_dist,
                    }
                    stats["total_cells"] += len(shelf_cells)
            return stats

        # 全部分馆统计
        all_stats = {}
        for w in LibraryWing:
            all_stats[w.value] = self.get_wing_stats(w)
        all_stats["total"] = sum(
            s.get("total_cells", 0) for s in all_stats.values()
        )
        return all_stats

    def get_available_shelves(self, wing: LibraryWing) -> List[str]:
        """获取分馆的可用书架列表"""
        return WING_SHELVES.get(wing, [])

    def get_bridges(self) -> Dict[str, Any]:
        """获取已注册的桥接子系统"""
        return dict(self._bridges)

    # ──────────────────────────────────────────────────────────
    #  价值评估（保留V2逻辑 + V3增强）
    # ──────────────────────────────────────────────────────────

    def _evaluate_value(self, title: str, content: str, tags: List[str]) -> float:
        """自主评估记忆价值 (0-1)"""
        base_score = 0.3

        text = f"{title} {content} {' '.join(tags)}"
        for keyword, bonus in self._VALUE_KEYWORDS.items():
            if keyword in text:
                base_score += bonus

        # 内容长度加分
        if len(content) > 500:
            base_score += 0.1
        if len(content) > 2000:
            base_score += 0.1

        # V1.0: 标签密度加分
        if len(tags) >= 3:
            base_score += 0.05
        if len(tags) >= 5:
            base_score += 0.05

        return min(1.0, max(0.0, base_score))

    def _decide_grade(self, value_score: float, category: MemoryCategory) -> MemoryGrade:
        """根据价值评分自主决定保留等级"""
        if value_score >= 0.8:
            return MemoryGrade.JIA
        elif value_score >= 0.6:
            return MemoryGrade.YI
        elif value_score >= 0.4:
            return MemoryGrade.BING
        else:
            return MemoryGrade.DING

    # ──────────────────────────────────────────────────────────
    #  自动清理
    # ──────────────────────────────────────────────────────────

    def auto_clean(self, operator: str = "") -> Dict[str, Any]:
        """
        自动清理过期记忆（仅藏书阁内部人员可执行）

        - 甲级：永不删除
        - 乙级：365天未审查标记
        - 丙级：30天未审查标记
        - 丁级：7天自动清理
        """
        if not self._check_permission(operator, LibraryPermission.DELETE):
            return {
                "error": "权限不足：清理操作仅限藏书阁内部人员",
                "authorized_staff": list(self._LIBRARY_STAFF),
            }

        now = time.time()
        cleaned = {"jia_kept": 0, "yi_reviewed": 0, "bing_reviewed": 0, "ding_cleaned": 0}

        to_remove = []
        for record in self._cells.values():
            age = now - record.created_at

            if record.grade == MemoryGrade.DING and age > 7 * 86400:
                to_remove.append(record.id)
                cleaned["ding_cleaned"] += 1
            elif record.grade == MemoryGrade.BING and age > 30 * 86400:
                record.last_reviewed = now
                record.review_count += 1
                cleaned["bing_reviewed"] += 1
            elif record.grade == MemoryGrade.YI and age > 365 * 86400:
                record.last_reviewed = now
                record.review_count += 1
                cleaned["yi_reviewed"] += 1
            else:
                cleaned["jia_kept"] += 1

        for rid in to_remove:
            record = self._cells.get(rid)
            if record:
                self._remove_from_indexes(record)
            del self._cells[rid]
            self._stats["auto_cleaned"] += 1
            # 清理持久化文件
            self._delete_cell_file(record)

        self._dirty = len(to_remove) > 0
        self._try_auto_save()

        return cleaned

    def delete_cell(self, cell_id: str, operator: str = "") -> bool:
        """删除单个格位记录"""
        if not self._check_permission(operator, LibraryPermission.DELETE):
            return False

        record = self._cells.get(cell_id)
        if not record:
            return False

        self._remove_from_indexes(record)
        del self._cells[cell_id]
        self._stats["auto_cleaned"] += 1
        self._dirty = True
        self._delete_cell_file(record)
        self._try_auto_save()
        return True

    # ──────────────────────────────────────────────────────────
    #  V1.0 分区持久化
    # ──────────────────────────────────────────────────────────

    def _delete_cell_file(self, record: CellRecord) -> None:
        """删除格位的持久化文件"""
        if not self._storage_path:
            return
        file_path = self._get_cell_file_path(record)
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                logger.debug(f"file_path.unlink()失败: {e}")

    def _get_cell_file_path(self, record: CellRecord) -> Optional[Path]:
        """获取格位文件的存储路径"""
        if not self._storage_path:
            return None
        return (
            self._storage_path
            / "wings"
            / record.wing.code
            / record.shelf
            / f"{record.id}.yaml"
        )

    def save_all(self) -> Dict[str, Any]:
        """
        手动保存所有值得持久化的记忆到磁盘。

        V1.0: 按分馆+书架分区存储，仅甲级/乙级持久化。
        """
        if not self._storage_path:
            return {"error": "持久化未启用", "persisted": False}

        saved = 0
        skipped = 0
        failed = 0

        for record in self._cells.values():
            if record.grade in (MemoryGrade.JIA, MemoryGrade.YI):
                if self._save_cell(record):
                    saved += 1
                else:
                    failed += 1
            else:
                skipped += 1

        self._dirty = False
        self._last_save_time = time.time()

        # 保存索引
        self._save_indexes()

        result = {
            "persisted": True,
            "saved": saved,
            "skipped": skipped,
            "failed": failed,
            "storage_path": str(self._storage_path),
            "version": "V1.0",
        }
        logger.info(f"藏书阁V1.0保存: 保存={saved}, 跳过={skipped}, 失败={failed}")
        return result

    def _save_cell(self, record: CellRecord) -> bool:
        """保存单个格位到分区文件"""
        if not self._storage_path:
            return False
        if record.grade == MemoryGrade.DING:
            return False

        try:
            import yaml
            file_path = self._get_cell_file_path(record)
            if not file_path:
                return False

            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.dump(record.to_dict(), f, allow_unicode=True, default_flow_style=False)
            return True
        except Exception as e:
            logger.debug(f"格位保存失败 [{record.id}]: {e}")
            return False

    def _save_indexes(self) -> None:
        """保存索引文件"""
        if not self._storage_path:
            return
        index_dir = self._storage_path / "index"
        try:
            index_dir.mkdir(parents=True, exist_ok=True)
            import yaml

            # 贤者索引
            sage_index_data = {k: list(v) for k, v in self._sage_index.items()}
            with open(index_dir / "sage_index.json", "w", encoding="utf-8") as f:
                json.dump(sage_index_data, f, ensure_ascii=False, indent=2)

            # 岗位索引
            pos_index_data = {k: list(v) for k, v in self._position_index.items()}
            with open(index_dir / "position_index.json", "w", encoding="utf-8") as f:
                json.dump(pos_index_data, f, ensure_ascii=False, indent=2)

            # Claw索引
            claw_index_data = {k: list(v) for k, v in self._claw_index.items()}
            with open(index_dir / "claw_index.json", "w", encoding="utf-8") as f:
                json.dump(claw_index_data, f, ensure_ascii=False, indent=2)

            # 标签索引
            tag_index_data = {k: list(v) for k, v in self._tag_index.items()}
            with open(index_dir / "tag_index.json", "w", encoding="utf-8") as f:
                json.dump(tag_index_data, f, ensure_ascii=False, indent=2)

            # 分馆统计
            with open(index_dir / "wing_stats.json", "w", encoding="utf-8") as f:
                json.dump(self.get_wing_stats(), f, ensure_ascii=False, indent=2)

            logger.debug("藏书阁V1.0索引已保存")

        except Exception as e:
            logger.debug(f"索引保存失败: {e}")

    def _try_auto_save(self) -> None:
        """尝试自动保存"""
        if self._should_auto_save():
            self.save_all()

    def _should_auto_save(self) -> bool:
        """检查是否需要自动保存"""
        if not self._storage_path or not self._dirty:
            return False
        if self._auto_save_interval <= 0:
            return False
        return (time.time() - self._last_save_time) >= self._auto_save_interval

    def _clean_orphaned_files(self) -> int:
        """清理磁盘上已不存在的格位文件"""
        if not self._storage_path:
            return 0

        cleaned = 0
        wings_dir = self._storage_path / "wings"
        if wings_dir.exists():
            for wing_dir in wings_dir.iterdir():
                if not wing_dir.is_dir():
                    continue
                for shelf_dir in wing_dir.iterdir():
                    if not shelf_dir.is_dir():
                        continue
                    for cell_file in shelf_dir.glob("CELL_*.yaml"):
                        cell_id = cell_file.stem
                        if cell_id not in self._cells:
                            try:
                                cell_file.unlink()
                                cleaned += 1
                            except Exception as e:
                                logger.debug(f"cleaned += 1失败: {e}")

        # 也清理根目录的V2旧文件（迁移后应该已被归档）
        for file_path in self._storage_path.glob("LIB_*.yaml"):
            try:
                file_path.unlink()
                cleaned += 1
            except Exception as e:
                logger.debug(f"cleaned += 1失败: {e}")

        return cleaned

    # ──────────────────────────────────────────────────────────
    #  统计信息
    # ──────────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        """获取藏书阁统计信息（P6: 单次遍历多维度统计）"""
        # [P6] 优化：原实现分别对 _cells.values() 做了 (1+N_grade+N_source) 次遍历
        # 改为单次遍历同时计算 grade_distribution 和 source_distribution
        grade_counts: Dict[str, int] = {g.value: 0 for g in MemoryGrade}
        source_counts: Dict[str, int] = {}
        
        for record in self._cells.values():
            # grade 统计
            g_key = record.grade.value if hasattr(record.grade, 'value') else str(record.grade)
            if g_key in grade_counts:
                grade_counts[g_key] = grade_counts.get(g_key, 0) + 1
            else:
                grade_counts[g_key] = grade_counts.get(g_key, 0) + 1
            # source 统计
            s_key = record.source.value if hasattr(record.source, 'value') else str(record.source)
            source_counts[s_key] = source_counts.get(s_key, 0) + 1

        return {
            "version": "V1.0.0",
            "chancellor": self.CHANCELLOR,
            "chancellor_title": self.CHANCELLOR_TITLE,
            "independence": "不受任何团队管理",
            "total_records": len(self._cells),
            "grade_distribution": grade_counts,
            "source_distribution": source_counts,
            "wing_stats": self.get_wing_stats(),
            "registered_bridges": list(self._bridges.keys()),
            "stats": self._stats,
        }

    def get_persistence_stats(self) -> Dict[str, Any]:
        """获取持久化统计信息"""
        disk_count = 0
        if self._storage_path and self._storage_path.exists():
            wings_dir = self._storage_path / "wings"
            if wings_dir.exists():
                for wing_dir in wings_dir.iterdir():
                    if wing_dir.is_dir():
                        for shelf_dir in wing_dir.iterdir():
                            if shelf_dir.is_dir():
                                disk_count += len(list(shelf_dir.glob("CELL_*.yaml")))

        return {
            "version": "V1.0.0",
            "persistence_enabled": self._storage_path is not None,
            "storage_path": str(self._storage_path) if self._storage_path else None,
            "auto_save_interval": self._auto_save_interval,
            "dirty": self._dirty,
            "last_save_time": self._last_save_time,
            "memory_count": len(self._cells),
            "disk_file_count": disk_count,
            "index_count": {
                "sage": len(self._sage_index),
                "position": len(self._position_index),
                "claw": len(self._claw_index),
                "tag": len(self._tag_index),
            },
        }

    def get_chancellor_info(self) -> Dict[str, str]:
        """获取藏书阁大学士信息"""
        return {
            "name": self.CHANCELLOR,
            "title": self.CHANCELLOR_TITLE,
            "nickname": self.CHANCELLOR_NICKNAME,
            "nobility": "王爵",
            "system": "皇家藏书阁（Somn全局记忆中心）",
            "version": "V1.0.0",
            "role": "独立记忆体系最高长官",
            "principle": "记录一切有价值之记忆，不受任何团队管理",
        }

    def version(self) -> str:
        """返回藏书阁版本"""
        return "V1.0.0"


# ═══════════════════════════════════════════════════════════════
#  全局单例
# ═══════════════════════════════════════════════════════════════

_library_instance: Optional[ImperialLibrary] = None


def get_imperial_library() -> ImperialLibrary:
    """获取皇家藏书阁全局单例"""
    global _library_instance
    if _library_instance is None:
        _library_instance = ImperialLibrary()
    return _library_instance
