"""
neural_memory_v7.py — knowledge_cells 代理模块
提供 get_neural_memory() 函数，适配 closed_loop_solver 的学习引擎调用。

实际实现委托给 smart_office_assistant.src.neural_memory.neural_memory_v7，
如果导入失败，则返回轻量级内存备份实现（不依赖外部存储）。
"""

import sys
import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

# ─────────────────────────────────────────────
# 轻量级内存实现（降级方案）
# ─────────────────────────────────────────────

_memory_store: List[Dict[str, Any]] = []


@dataclass
class MemoryRecord:
    """记忆记录"""
    content: str
    category: str
    tags: List[str]
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
        }


class NeuralMemoryLight:
    """轻量级 NeuralMemory 实现（内存 + 本地JSON文件备份）"""

    def __init__(self, storage_dir: str = "data/neural_memory_fallback"):
        self.storage_dir = storage_dir
        self.records: List[MemoryRecord] = []
        os.makedirs(storage_dir, exist_ok=True)

    def store(self, content: str, category: str = "default",
              tags: Optional[List[str]] = None, confidence: float = 0.5) -> str:
        """存储一条记忆，返回记忆ID"""
        record = MemoryRecord(
            content=content,
            category=category,
            tags=tags or [],
            confidence=confidence,
        )
        self.records.append(record)
        _memory_store.append(record.to_dict())

        # 持久化到本地文件
        try:
            import json
            fname = f"memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            fpath = os.path.join(self.storage_dir, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(record.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # 持久化失败不影响主流程

        return f"mem_{len(self.records)}"

    def query(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """简单关键词查询（降级版）"""
        results = []
        for rec in self.records:
            if query.lower() in rec.content.lower():
                results.append(rec.to_dict())
                if len(results) >= top_k:
                    break
        return results

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_records": len(self.records),
            "categories": list(set(r.category for r in self.records)),
            "storage_dir": self.storage_dir,
        }


# ─────────────────────────────────────────────
# 尝试导入真实实现，失败则使用轻量级实现
# ─────────────────────────────────────────────

_neural_memory_instance: Optional[NeuralMemoryLight] = None
_use_fallback = False


def get_neural_memory(**kwargs):
    """
    获取 NeuralMemory 实例。
    优先尝试导入 smart_office_assistant 中的真实实现，
    失败则返回轻量级内存实现。
    """
    global _neural_memory_instance, _use_fallback

    if _neural_memory_instance is not None:
        return _neural_memory_instance

    # 尝试导入真实实现
    try:
        # 把 smart_office_assistant 的 src 目录加入路径
        sa_src = os.path.join(os.path.dirname(__file__), "..", "smart_office_assistant", "src")
        sa_src = os.path.abspath(sa_src)
        if sa_src not in sys.path:
            sys.path.insert(0, sa_src)

        from neural_memory.neural_memory_v7 import get_neural_memory as _real_get
        _neural_memory_instance = _real_get(**kwargs)
        return _neural_memory_instance
    except Exception as e:
        # 导入失败，使用轻量级降级实现
        if not _use_fallback:
            print(f"[neural_memory_v7] 真实实现导入失败，使用轻量级降级: {e}")
            _use_fallback = True

        _neural_memory_instance = NeuralMemoryLight()
        return _neural_memory_instance
