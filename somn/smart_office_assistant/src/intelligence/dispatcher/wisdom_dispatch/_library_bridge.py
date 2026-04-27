# -*- coding: utf-8 -*-
"""
藏书阁V1.0 跨系统桥接模块
_library_bridge.py

为Somn各子系统提供藏书阁桥接能力：
1. ROI追踪系统 → 执行分馆
2. 学习系统 → 学习分馆
3. 神经记忆系统 → 贤者分馆/架构分馆
4. 研究系统 → 研究分馆
5. 情绪研究系统 → 情绪分馆

使用方式：
    from src.intelligence.dispatcher.wisdom_dispatch._library_bridge import (
        get_library_bridge,
        ROIBridge,
        LearningBridge,
        NeuralMemoryBridge,
    )

    # 获取桥接实例
    bridge = get_library_bridge()

    # ROI汇报
    bridge.report_roi(
        task_id="task_001",
        claw_name="孔子",
        efficiency=0.85,
        quality=0.9,
    )

    # 学习汇报
    bridge.report_learning(
        strategy_type="THREE_TIER",
        insight="新模式发现",
        sage="孔子",
    )
"""

import logging
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ._imperial_library import ImperialLibrary, LibraryWing, MemorySource, MemoryCategory, MemoryGrade, CellRecord

logger = logging.getLogger(__name__)

# 全局桥接实例
_library_bridge_instance: Optional["LibraryBridge"] = None


# ═══════════════════════════════════════════════════════════════
#  桥接配置常量
# ═══════════════════════════════════════════════════════════════

class BridgeConfig:
    """桥接配置常量"""

    # ROI追踪系统配置
    ROI_CONFIG = {
        "subsystem_name": "ROITracker",
        "wing": "EXEC",  # 执行分馆
        "default_shelf": "execution_logs",
        "source": "ROI追踪",  # MemorySource枚举值
        "auto_submit": True,
    }

    # 学习系统配置
    LEARNING_CONFIG = {
        "subsystem_name": "LearningCoordinator",
        "wing": "LEARN",  # 学习分馆
        "default_shelf": "learning_insights",
        "source": "学习策略",  # MemorySource枚举值
        "auto_submit": True,
    }

    # 神经记忆系统配置
    NEURAL_MEMORY_CONFIG = {
        "subsystem_name": "NeuralMemory",
        "wing": "SAGE",  # 贤者分馆
        "default_shelf": "sage_memories",
        "source": "神经记忆系统",  # MemorySource枚举值
        "auto_submit": False,
    }

    # 研究策略引擎配置
    RESEARCH_CONFIG = {
        "subsystem_name": "ResearchStrategyEngine",
        "wing": "RESEARCH",  # 研究分馆
        "default_shelf": "research_findings",
        "source": "研究发现",  # MemorySource枚举值
        "auto_submit": True,
    }

    # 情绪研究系统配置
    EMOTION_CONFIG = {
        "subsystem_name": "EmotionResearchCore",
        "wing": "EMOTION",  # 情绪分馆
        "default_shelf": "emotion_patterns",
        "source": "情绪研究",  # MemorySource枚举值
        "auto_submit": True,
    }

    # Claw子系统配置
    CLAW_CONFIG = {
        "subsystem_name": "GlobalClawScheduler",
        "wing": "SAGE",  # 贤者分馆
        "default_shelf": "claw_memories",
        "source": "Claw执行记录",  # MemorySource枚举值
        "auto_submit": True,
    }


# ═══════════════════════════════════════════════════════════════
#  LibraryBridge 统一桥接类
# ═══════════════════════════════════════════════════════════════

class LibraryBridge:
    """
    藏书阁V1.0 统一桥接接口

    为Somn各子系统提供简化的藏书阁访问能力。
    自动管理桥接注册，隐藏底层细节。
    """

    def __init__(self, library: "ImperialLibrary" = None):
        """
        初始化桥接

        Args:
            library: 藏书阁实例，如果为None则延迟获取
        """
        self._library = library
        self._bridges_registered: Dict[str, bool] = {}

    @property
    def library(self) -> "ImperialLibrary":
        """延迟获取藏书阁实例"""
        if self._library is None:
            from ._imperial_library import ImperialLibrary
            self._library = ImperialLibrary()
        return self._library

    def _ensure_bridge_registered(self, config: Dict[str, Any]) -> bool:
        """确保子系统桥接已注册"""
        subsystem = config["subsystem_name"]
        if subsystem in self._bridges_registered:
            return True

        # 获取枚举
        from ._imperial_library import LibraryWing, MemorySource

        wing_enum = LibraryWing[config["wing"]]
        # source 是枚举值字符串，需要从枚举名称获取
        source_name = config["source"]
        # 查找对应的枚举成员
        source_enum = None
        for member in MemorySource:
            if member.value == source_name:
                source_enum = member
                break
        if source_enum is None:
            source_enum = MemorySource.SYSTEM_EVENT  # 默认回退

        # 注册桥接
        self.library.register_bridge(subsystem, {
            "wing": wing_enum,
            "default_shelf": config["default_shelf"],
            "source": source_enum,
            "auto_submit": config.get("auto_submit", False),
        })

        self._bridges_registered[subsystem] = True
        logger.info(f"桥接已注册: {subsystem} → {config['wing']}/{config['default_shelf']}")
        return True

    # ──────────────────────────────────────────────────────────
    #  ROI追踪系统桥接
    # ──────────────────────────────────────────────────────────

    def report_roi(
        self,
        task_id: str,
        claw_name: str,
        efficiency: float,
        quality: float,
        satisfaction: float = 0.5,
        roi_score: float = 0.0,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> Optional["CellRecord"]:
        """
        汇报ROI数据到藏书阁执行分馆

        Args:
            task_id: 任务ID
            claw_name: Claw名称
            efficiency: 效率评分 (0-1)
            quality: 质量评分 (0-1)
            satisfaction: 满意度 (0-1)
            roi_score: ROI综合评分
            tags: 标签
            metadata: 元数据

        Returns:
            CellRecord 或 None
        """
        from ._imperial_library import MemoryCategory

        self._ensure_bridge_registered(BridgeConfig.ROI_CONFIG)

        title = f"ROI汇报 - {task_id}"
        content = (
            f"任务ID: {task_id}\n"
            f"Claw: {claw_name}\n"
            f"效率: {efficiency:.2%}\n"
            f"质量: {quality:.2%}\n"
            f"满意度: {satisfaction:.2%}\n"
            f"ROI评分: {roi_score:.4f}"
        )

        return self.library.submit_bridge_memory(
            subsystem_name=BridgeConfig.ROI_CONFIG["subsystem_name"],
            title=title,
            content=content,
            category=MemoryCategory.EXECUTION_LOG,
            tags=tags or ["ROI", "效率", "质量"],
            metadata=metadata or {
                "task_id": task_id,
                "claw_name": claw_name,
                "efficiency": efficiency,
                "quality": quality,
                "satisfaction": satisfaction,
                "roi_score": roi_score,
            },
            associated_claw=claw_name,
        )

    def query_roi_by_claw(self, claw_name: str, limit: int = 10) -> List["CellRecord"]:
        """查询某Claw的ROI历史"""
        return self.library.query_cells(
            associated_claw=claw_name,
            limit=limit,
            sort_by="created_at",
        )

    # ──────────────────────────────────────────────────────────
    #  学习系统桥接
    # ──────────────────────────────────────────────────────────

    def report_learning(
        self,
        strategy_type: str,
        insight: str,
        sage: str = "",
        claw_name: str = "",
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> Optional["CellRecord"]:
        """
        汇报学习洞察到藏书阁学习分馆

        Args:
            strategy_type: 学习策略类型 (THREE_TIER/DAILY/ENHANCED等)
            insight: 学习洞察内容
            sage: 关联贤者
            claw_name: 关联Claw
            tags: 标签
            metadata: 元数据

        Returns:
            CellRecord 或 None
        """
        from ._imperial_library import MemoryCategory

        self._ensure_bridge_registered(BridgeConfig.LEARNING_CONFIG)

        title = f"学习洞察 - {strategy_type}"
        content = (
            f"策略: {strategy_type}\n"
            f"洞察: {insight}"
        )

        return self.library.submit_bridge_memory(
            subsystem_name=BridgeConfig.LEARNING_CONFIG["subsystem_name"],
            title=title,
            content=content,
            category=MemoryCategory.LEARNING_INSIGHT,
            tags=tags or ["学习", "洞察", strategy_type],
            metadata=metadata or {
                "strategy_type": strategy_type,
                "insight": insight,
            },
            associated_sage=sage,
            associated_claw=claw_name,
        )

    def query_learning_by_strategy(self, strategy_type: str, limit: int = 10) -> List["CellRecord"]:
        """查询某学习策略的洞察"""
        return self.library.query_cells(
            keyword=strategy_type,
            limit=limit,
            sort_by="value_score",
        )

    # ──────────────────────────────────────────────────────────
    #  神经记忆系统桥接
    # ──────────────────────────────────────────────────────────

    def report_memory(
        self,
        memory_type: str,
        content: str,
        sage: str = "",
        claw_name: str = "",
        wing: str = "SAGE",
        shelf: str = "sage_memories",
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> Optional["CellRecord"]:
        """
        汇报神经记忆到藏书阁

        Args:
            memory_type: 记忆类型
            content: 记忆内容
            sage: 关联贤者
            claw_name: 关联Claw
            wing: 分馆 (SAGE/ARCH/EXEC等)
            shelf: 书架
            tags: 标签
            metadata: 元数据

        Returns:
            CellRecord 或 None
        """
        from ._imperial_library import LibraryWing, MemoryCategory, MemorySource

        self._ensure_bridge_registered(BridgeConfig.NEURAL_MEMORY_CONFIG)

        title = f"神经记忆 - {memory_type}"

        # 特殊处理：根据wing切换来源
        source_map = {
            "SAGE": MemorySource.NEURAL_MEMORY,
            "ARCH": MemorySource.SYSTEM_EVENT,
            "EXEC": MemorySource.CLAW_EXECUTION,
        }

        return self.library.submit_bridge_memory(
            subsystem_name=BridgeConfig.NEURAL_MEMORY_CONFIG["subsystem_name"],
            title=title,
            content=content,
            category=MemoryCategory.METHODOLOGY,
            tags=tags or ["神经记忆", memory_type],
            metadata=metadata or {
                "memory_type": memory_type,
                "wing": wing,
                "shelf": shelf,
            },
            associated_sage=sage,
            associated_claw=claw_name,
        )

    # ──────────────────────────────────────────────────────────
    #  研究策略引擎桥接
    # ──────────────────────────────────────────────────────────

    def report_research(
        self,
        research_type: str,
        finding: str,
        depth: str = "",
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> Optional["CellRecord"]:
        """
        汇报研究发现到藏书阁研究分馆

        Args:
            research_type: 研究类型
            finding: 研究发现
            depth: 研究深度
            tags: 标签
            metadata: 元数据

        Returns:
            CellRecord 或 None
        """
        from ._imperial_library import MemoryCategory

        self._ensure_bridge_registered(BridgeConfig.RESEARCH_CONFIG)

        title = f"研究发现 - {research_type}"
        content = (
            f"类型: {research_type}\n"
            f"深度: {depth}\n"
            f"发现: {finding}"
        )

        return self.library.submit_bridge_memory(
            subsystem_name=BridgeConfig.RESEARCH_CONFIG["subsystem_name"],
            title=title,
            content=content,
            category=MemoryCategory.RESEARCH_INSIGHT,
            tags=tags or ["研究", "发现", research_type],
            metadata=metadata or {
                "research_type": research_type,
                "depth": depth,
            },
        )

    # ──────────────────────────────────────────────────────────
    #  情绪研究系统桥接
    # ──────────────────────────────────────────────────────────

    def report_emotion(
        self,
        emotion_type: str,
        pattern: str,
        intensity: float = 0.5,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> Optional["CellRecord"]:
        """
        汇报情绪研究到藏书阁情绪分馆

        Args:
            emotion_type: 情绪类型
            pattern: 情绪模式
            intensity: 情绪强度
            tags: 标签
            metadata: 元数据

        Returns:
            CellRecord 或 None
        """
        from ._imperial_library import MemoryCategory

        self._ensure_bridge_registered(BridgeConfig.EMOTION_CONFIG)

        title = f"情绪模式 - {emotion_type}"
        content = (
            f"情绪类型: {emotion_type}\n"
            f"强度: {intensity:.2%}\n"
            f"模式: {pattern}"
        )

        return self.library.submit_bridge_memory(
            subsystem_name=BridgeConfig.EMOTION_CONFIG["subsystem_name"],
            title=title,
            content=content,
            category=MemoryCategory.EMOTION_PATTERN,
            tags=tags or ["情绪", "模式", emotion_type],
            metadata=metadata or {
                "emotion_type": emotion_type,
                "intensity": intensity,
                "pattern": pattern,
            },
        )

    # ──────────────────────────────────────────────────────────
    #  Claw子系统桥接
    # ──────────────────────────────────────────────────────────

    def report_claw_execution(
        self,
        claw_name: str,
        task: str,
        result: str,
        success: bool = True,
        duration: float = 0.0,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
    ) -> Optional["CellRecord"]:
        """
        汇报Claw执行记录到藏书阁贤者分馆

        Args:
            claw_name: Claw名称
            task: 任务描述
            result: 执行结果
            success: 是否成功
            duration: 执行时长(秒)
            tags: 标签
            metadata: 元数据

        Returns:
            CellRecord 或 None
        """
        from ._imperial_library import MemoryCategory

        self._ensure_bridge_registered(BridgeConfig.CLAW_CONFIG)

        title = f"Claw执行 - {claw_name}"
        content = (
            f"Claw: {claw_name}\n"
            f"任务: {task}\n"
            f"结果: {result}\n"
            f"状态: {'成功' if success else '失败'}\n"
            f"时长: {duration:.2f}秒"
        )

        return self.library.submit_bridge_memory(
            subsystem_name=BridgeConfig.CLAW_CONFIG["subsystem_name"],
            title=title,
            content=content,
            category=MemoryCategory.CLAW_OUTPUT,
            tags=tags or ["Claw", "执行", claw_name],
            metadata=metadata or {
                "claw_name": claw_name,
                "task": task,
                "result": result,
                "success": success,
                "duration": duration,
            },
            associated_claw=claw_name,
        )

    # ──────────────────────────────────────────────────────────
    #  统计接口
    # ──────────────────────────────────────────────────────────

    def get_bridge_stats(self) -> Dict[str, Any]:
        """获取所有桥接统计"""
        return {
            "registered_bridges": self.library.get_bridges(),
            "library_stats": self.library.get_stats(),
        }


# ═══════════════════════════════════════════════════════════════
#  全局访问函数
# ═══════════════════════════════════════════════════════════════

def get_library_bridge(library: "ImperialLibrary" = None) -> LibraryBridge:
    """
    获取藏书阁桥接全局实例

    Args:
        library: 可选的藏书阁实例

    Returns:
        LibraryBridge实例
    """
    global _library_bridge_instance
    if _library_bridge_instance is None:
        _library_bridge_instance = LibraryBridge(library)
    return _library_bridge_instance


def reset_library_bridge() -> None:
    """重置全局桥接实例（用于测试）"""
    global _library_bridge_instance
    _library_bridge_instance = None
