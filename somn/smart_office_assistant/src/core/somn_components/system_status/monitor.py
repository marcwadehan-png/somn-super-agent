"""
__all__ = [
    'get_component_health',
    'get_status',
    'is_component_healthy',
]

系统监控器 - 提供系统状态监控能力
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SystemMonitor:
    """系统监控器封装类"""

    def __init__(self, somn_core=None):
        """
        Args:
            somn_core: SomnCore实例引用
        """
        self._core = somn_core

    def get_status(self) -> Dict[str, Any]:
        """
        获取系统状态

        Returns:
            系统状态字典
        """
        if not self._core:
            return {"status": "unavailable", "reason": "no_core_reference"}

        try:
            # 获取各组件状态
            components = {}

            # 神经记忆
            if hasattr(self._core, 'neural_system') and self._core.neural_system:
                try:
                    components["neural_memory"] = self._core.neural_system.generate_system_report()
                except Exception:
                    components["neural_memory"] = {"status": "error"}

            # 知识图谱
            if hasattr(self._core, 'knowledge_graph') and self._core.knowledge_graph:
                try:
                    components["knowledge_graph"] = self._core.knowledge_graph.get_statistics()
                except Exception:
                    components["knowledge_graph"] = {"status": "error"}

            # 工具注册表
            if hasattr(self._core, 'tool_registry') and self._core.tool_registry:
                try:
                    tools = self._core.tool_registry.list_tools()
                    components["tool_registry"] = {
                        "total_tools": len(tools),
                        "tools": [tool.tool_id for tool in tools[:10]],
                        "status": "ok"
                    }
                except Exception:
                    components["tool_registry"] = {"status": "error"}

            # 语义记忆
            if hasattr(self._core, 'semantic_memory') and self._core.semantic_memory:
                try:
                    stats = self._core.semantic_memory.get_stats()
                    components["semantic_memory"] = {
                        "status": "ok",
                        "stats": stats
                    }
                except Exception:
                    components["semantic_memory"] = {"status": "error"}

            # ROI追踪器
            if hasattr(self._core, '_get_roi_tracker'):
                try:
                    roi_tracker = self._core._get_roi_tracker()
                    components["roi_tracker"] = {
                        "available": roi_tracker is not None,
                        "status": "ok" if roi_tracker else "unavailable"
                    }
                except Exception:
                    components["roi_tracker"] = {"status": "error"}

            return {
                "status": "ok",
                "components": components
            }

        except Exception as e:
            logger.warning(f"获取系统状态失败: {e}")
            return {"status": "error", "reason": "获取系统状态失败"}

    def get_component_health(self, component_name: str) -> Dict[str, Any]:
        """
        获取指定组件健康状态

        Args:
            component_name: 组件名

        Returns:
            组件状态
        """
        status = self.get_status()
        components = status.get("components", {})
        return components.get(component_name, {"status": "not_found"})

    def is_component_healthy(self, component_name: str) -> bool:
        """
        检查组件是否健康

        Args:
            component_name: 组件名

        Returns:
            是否健康
        """
        health = self.get_component_health(component_name)
        return health.get("status") == "ok"
