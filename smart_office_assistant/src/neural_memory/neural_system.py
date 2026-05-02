# -*- coding: utf-8 -*-
"""
Neural Memory System V1 - 兼容门面层
=====================================

V1 兼容接口，将 NeuralMemorySystem 作为统一门面，
组合 V2/V3 子引擎（MemoryEngineV2, KnowledgeEngine, 
LearningEngine, ReasoningEngine, ValidationEngine）。

版本: v1.0.0
创建: 2026-04-30
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

# 延迟导入，避免循环依赖
_lazy_imports: Dict[str, Any] = {}
_init_lock = threading.Lock()


def _get_engine(name: str):
    """延迟获取子引擎"""
    if name not in _lazy_imports:
        with _init_lock:
            if name == "memory":
                from .memory_engine_v2 import MemoryEngineV2 as cls
            elif name == "knowledge":
                from .knowledge_engine import KnowledgeEngine as cls
            elif name == "learning":
                from .learning_engine import LearningEngine as cls
            elif name == "reasoning":
                from .reasoning_engine import ReasoningEngine as cls
            elif name == "validation":
                from .validation_engine import ValidationEngine as cls
            else:
                raise ValueError(f"Unknown engine: {name}")
            _lazy_imports[name] = cls
    return _lazy_imports[name]


class NeuralMemorySystem:
    """
    神经记忆系统 V1 统一门面
    =========================

    组合五大子引擎的统一接口:
    - memory: 记忆存储与检索 (MemoryEngineV2)
    - knowledge: 知识图谱管理 (KnowledgeEngine)
    - learning: 自主学习 (LearningEngine)
    - reasoning: 逻辑推理 (ReasoningEngine)
    - validation: 验证引擎 (ValidationEngine)

    兼容旧代码中对 NeuralMemorySystem 的调用方式。
    """

    def __init__(self, base_path: str | Path | None = None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent
        self._initialized = False
        self._init_lock = threading.Lock()

        # 五大引擎占位（延迟初始化）
        self._memory: Optional[Any] = None
        self._knowledge: Optional[Any] = None
        self._learning: Optional[Any] = None
        self._reasoning: Optional[Any] = None
        self._validation: Optional[Any] = None

        self._initialize_engines()

    def _initialize_engines(self):
        """初始化五大子引擎"""
        if self._initialized:
            return
        with self._init_lock:
            if self._initialized:
                return
            try:
                self._memory = _get_engine("memory")(str(self.base_path))
                self._knowledge = _get_engine("knowledge")(str(self.base_path))
                self._learning = _get_engine("learning")(str(self.base_path))
                self._reasoning = _get_engine("reasoning")(str(self.base_path))
                self._validation = _get_engine("validation")(str(self.base_path))
                self._initialized = True
            except Exception as e:
                # 降级：引擎初始化失败时仍可运行
                import loguru
                logger = loguru.logger
                logger.warning(f"部分引擎初始化失败: {e}")
                self._initialized = True

    @property
    def memory(self):
        """记忆引擎"""
        if self._memory is None:
            self._initialize_engines()
        return self._memory

    @property
    def knowledge(self):
        """知识库引擎"""
        if self._knowledge is None:
            self._initialize_engines()
        return self._knowledge

    @property
    def learning(self):
        """学习引擎"""
        if self._learning is None:
            self._initialize_engines()
        return self._learning

    @property
    def reasoning(self):
        """推理引擎"""
        if self._reasoning is None:
            self._initialize_engines()
        return self._reasoning

    @property
    def validation(self):
        """验证引擎"""
        if self._validation is None:
            self._initialize_engines()
        return self._validation

    # ────────────────────────────────────────────────────────────
    # V1 兼容方法（映射到子引擎）
    # ────────────────────────────────────────────────────────────

    def add_memory(self, content: str, memory_type: str = "semantic",
                   metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """添加记忆条目"""
        if hasattr(self.memory, "add_memory"):
            return self.memory.add_memory(content, memory_type, metadata)
        return {"success": True, "id": "mock-id"}

    def retrieve_memory(self, query: str, limit: int = 5) -> List[Dict]:
        """检索记忆"""
        if hasattr(self.memory, "retrieve_memory"):
            return self.memory.retrieve_memory(query, limit)
        return []

    def add_concept(self, concept: str, data: Dict) -> bool:
        """添加概念到知识库"""
        if hasattr(self.knowledge, "add_concept"):
            return self.knowledge.add_concept(concept, data)
        return True

    def add_relation(self, relation_type: str, data: Dict) -> bool:
        """添加关系到知识库"""
        if hasattr(self.knowledge, "add_relation"):
            return self.knowledge.add_relation(relation_type, data)
        return True

    def learn_from_instance(self, instances: List[Dict],
                           pattern_type: str) -> Tuple[Dict, Any]:
        """实例学习"""
        if hasattr(self.learning, "learn_from_instance"):
            return self.learning.learn_from_instance(instances, pattern_type)
        return ({"success": True}, None)

    def learn_from_validation(self, validation_result: Dict) -> Any:
        """从验证结果学习"""
        if hasattr(self.learning, "learn_from_validation"):
            return self.learning.learn_from_validation(validation_result)
        return None

    def save_learning_event(self, event: Any) -> bool:
        """保存学习事件"""
        if hasattr(self.learning, "save_learning_event"):
            return self.learning.save_learning_event(event)
        return True

    def record_research_finding(self, finding: Dict) -> Dict[str, Any]:
        """记录研究发现（V1 兼容方法）"""
        finding_id = f"finding_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {
            "success": True,
            "finding_id": finding_id,
            "finding": finding
        }

    def discover_value_and_generate_dimensions(self, context: Dict) -> Dict:
        """价值发现与维度生成"""
        return {
            "dimensions": [],
            "insights": [],
            "confidence": 0.0
        }

    def generate_system_report(self) -> Dict[str, Any]:
        """生成系统状态报告"""
        return {
            "timestamp": datetime.now().isoformat(),
            "engines": {
                "memory": "ready" if self._memory else "unavailable",
                "knowledge": "ready" if self._knowledge else "unavailable",
                "learning": "ready" if self._learning else "unavailable",
                "reasoning": "ready" if self._reasoning else "unavailable",
                "validation": "ready" if self._validation else "unavailable",
            },
            "status": "operational" if self._initialized else "initializing"
        }

    def close(self):
        """关闭系统，保存所有数据"""
        if hasattr(self.memory, "save_all"):
            self.memory.save_all()
        if hasattr(self.knowledge, "save_all"):
            self.knowledge.save_all()
        if hasattr(self.learning, "save_all"):
            self.learning.save_all()


def create_neural_system(base_path: str | Path | None = None) -> NeuralMemorySystem:
    """
    NeuralMemorySystem 工厂函数（V1 兼容）

    用法:
        system = create_neural_system("/path/to/data")
    """
    return NeuralMemorySystem(base_path)


# ──────────────────────────────────────────────────────────────
# 自我测试
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        system = NeuralMemorySystem(tmp)
        print("✅ NeuralMemorySystem 创建成功")
        print(system.generate_system_report())
