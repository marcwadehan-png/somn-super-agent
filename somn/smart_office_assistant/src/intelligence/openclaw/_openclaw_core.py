# -*- coding: utf-8 -*-
"""
OpenClaw 开放抓取核心引擎
========================

Phase 4: 外部世界主动抓取并更新系统

功能:
- 外部数据源接入
- 实时知识更新
- 用户反馈闭环
- 主动学习机制

版本: v1.0.0
创建: 2026-04-22
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import asyncio


class UpdateMode(Enum):
    """更新模式"""
    FULL = "full"           # 全量更新
    INCREMENTAL = "incremental"  # 增量更新
    EVENT_DRIVEN = "event_driven"  # 事件驱动
    ACTIVE = "active"       # 主动学习


class DataSourceType(Enum):
    """数据源类型"""
    WEB = "web"             # 网页
    FILE = "file"           # 文件系统
    API = "api"             # 外部API
    RSS = "rss"             # RSS订阅
    DATABASE = "database"   # 数据库


@dataclass
class KnowledgeItem:
    """知识条目"""
    id: str
    content: str
    source: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0  # 置信度 0-1
    
    
@dataclass
class Feedback:
    """用户反馈"""
    user_id: str
    content: str
    rating: int  # 1-5
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)
    
    
@dataclass
class UpdateResult:
    """更新结果"""
    added: int = 0
    updated: int = 0
    removed: int = 0
    conflicts: int = 0
    errors: List[str] = field(default_factory=list)


class DataSourceConnector:
    """数据源连接器基类"""
    
    def __init__(self, source_type: DataSourceType, config: Dict[str, Any]):
        self.source_type = source_type
        self.config = config
        self.connected = False
        
    async def connect(self) -> bool:
        """连接数据源"""
        raise NotImplementedError
    
    async def disconnect(self) -> bool:
        """断开连接"""
        raise NotImplementedError
        
    async def fetch(self, query: str) -> List[KnowledgeItem]:
        """抓取数据"""
        raise NotImplementedError


class OpenClawCore:
    """OpenClaw核心引擎
    
    职责:
    1. 管理外部数据源（Web/File/API/RSS）
    2. 抓取外部知识并注入Claw记忆
    3. 学习用户反馈并优化路由策略
    4. 知识版本控制与增量更新
    
    与Claw子系统的对接点:
    - ClawMemoryAdapter: 注入新知识到指定Claw的记忆
    - GatewayRouter: 根据反馈调整路由权重
    - ClawsCoordinator: 注册为全局知识更新器
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.sources: Dict[str, DataSourceConnector] = {}
        self.update_mode = UpdateMode.INCREMENTAL
        self.last_update: Optional[datetime] = None
        
        # 反馈学习子系统
        from ._feedback import FeedbackCollector, ActiveLearner, SageAdaptor
        self.feedback_collector = FeedbackCollector()
        self.active_learner = ActiveLearner()
        self.sage_adaptor = SageAdaptor()
        
        # 深层学习子系统（Phase 4.5 v1.0.0）
        from ._pattern_learner import PatternLearner
        from ._recommender import SageRecommender
        self.pattern_learner = PatternLearner()
        self.recommender = SageRecommender(self.pattern_learner)
        # 将深层学习器绑定到ActiveLearner（兼容层桥接）
        self.active_learner.set_deep_learner(self.pattern_learner)
        
        # 内容处理子系统（Phase 4.5 v1.0.0）
        from ._cleaner import ContentCleaner
        from ._doc_parser import DocParser
        self.cleaner = ContentCleaner()
        self.doc_parser = DocParser()
        
        # 知识更新子系统
        from ._updater import DiffEngine, Merger, VersionControl
        self.diff_engine = DiffEngine()
        self.merger = Merger()
        self.version_ctrl: Optional[VersionControl] = None
        
        # ★ v1.2 修复: 知识快照从类变量改为实例变量，避免多实例数据污染
        self._knowledge_snapshot: Dict[str, Dict[str, Any]] = {}  # key → {content, confidence}
        
        # 统计
        self._stats = {
            "fetches_total": 0,
            "knowledge_added": 0,
            "feedbacks_received": 0,
            "updates_performed": 0,
            "errors": 0,
            "recommendations_made": 0,
        }
        
        # 回调
        self._callbacks: Dict[str, List[Callable]] = {
            'on_fetch': [],
            'on_update': [],
            'on_feedback': [],
            'on_recommend': [],
        }
        
    def register_source(self, name: str, connector: DataSourceConnector) -> bool:
        """注册数据源"""
        self.sources[name] = connector
        return True
        
    def unregister_source(self, name: str) -> bool:
        """注销数据源"""
        if name in self.sources:
            del self.sources[name]
            return True
        return False
        
    async def connect_source(self, name: str) -> bool:
        """连接指定数据源"""
        source = self.sources.get(name)
        if source:
            source.connected = await source.connect()
            return source.connected
        return False
        
    async def fetch_knowledge(self, query: str, source_names: Optional[List[str]] = None) -> List[KnowledgeItem]:
        """从指定数据源抓取知识"""
        results = []
        sources_to_use = source_names or list(self.sources.keys())
        
        for name in sources_to_use:
            source = self.sources.get(name)
            if source and source.connected:
                items = await source.fetch(query)
                results.extend(items)
                
        # 触发回调
        for cb in self._callbacks['on_fetch']:
            await cb(results)
            
        return results
        
    async def update_knowledge(self, items: List[KnowledgeItem]) -> UpdateResult:
        """更新知识库（完整实现）
        
        流程:
        1. 计算差异 (DiffEngine)
        2. 合并知识 (Merger)
        3. 版本控制 (VersionControl)
        4. 注入到对应Claw的记忆
        """
        result = UpdateResult()
        
        if not items:
            return result
        
        # 初始化版本控制
        if self.version_ctrl is None:
            storage = self.config.get("version_storage", "data/openclaw/versions")
            from ._updater import VersionControl
            self.version_ctrl = VersionControl(storage)
        
        for item in items:
            try:
                key = item.id or item.source
                new_data = {
                    "content": item.content,
                    "source": item.source,
                    "confidence": item.confidence,
                    "metadata": item.metadata,
                }
                
                # 步骤1: 计算差异
                old_data = self._knowledge_snapshot.get(key)
                if old_data is not None:
                    diffs = self.diff_engine.compute(old_data, new_data)
                    # ★ v1.2 修复: UNCHANGED 不计入统计，MODIFIED 统一计数不双重计算
                    for d in diffs:
                        if d.diff_type.value == "added":
                            result.added += 1
                        elif d.diff_type.value == "deleted":
                            result.removed += 1
                        # UNCHANGED 跳过
                    # 步骤2: 合并知识
                    merged = self.merger.merge(old_data, diffs)
                    # 统计冲突（MODIFIED条目视为冲突，统一在diffs中计数一次）
                    conflicts = sum(1 for d in diffs if d.diff_type.value == "modified")
                    result.conflicts += conflicts
                    result.updated = conflicts  # updated = modified 数量
                    self._knowledge_snapshot[key] = merged
                else:
                    result.added += 1
                    self._knowledge_snapshot[key] = new_data
                
                # 步骤3: 保存版本
                ver_id = self.version_ctrl.save_version(key, new_data)
                
                # 触发回调
                for cb in self._callbacks['on_update']:
                    await cb({"item": item, "version_id": ver_id})
                    
            except Exception as e:
                result.errors.append(f"Update error for {item.id}: {e}")
                self._stats["errors"] += 1
        
        self.last_update = datetime.now()
        self._stats["knowledge_added"] += result.added
        self._stats["updates_performed"] += 1
        
        # 触发完成回调
        for cb in self._callbacks['on_update']:
            await cb(result)
            
        return result
    
    async def learn_feedback(self, feedback) -> Dict[str, Any]:
        """学习用户反馈（完整实现）
        
        流程:
        1. 收集反馈到FeedbackCollector
        2. ActiveLearner提取模式
        3. SageAdaptor调整参数
        """
        from ._feedback import FeedbackItem
        
        # 统一反馈格式
        if isinstance(feedback, dict):
            fb = FeedbackItem(
                user_id=feedback.get("user_id", "anonymous"),
                sage_name=feedback.get("sage_name", ""),
                rating=int(feedback.get("rating", 3)),
                comment=feedback.get("comment", ""),
                context=feedback.get("context", {}),
            )
        elif isinstance(feedback, FeedbackItem):
            fb = feedback
        else:
            return {"error": "Invalid feedback format"}
        
        # 收集
        self.feedback_collector.add(fb)
        
        # 学习模式
        self.active_learner.learn(fb)
        
        # 调整参数
        self.sage_adaptor.adjust(fb.sage_name, fb)
        
        self._stats["feedbacks_received"] += 1
        
        learned = {
            'user_id': fb.user_id,
            'sage_name': fb.sage_name,
            'rating': fb.rating,
            'pattern': self.active_learner.recommend("")[:5] if fb.comment else [],
            'adjustments': self.sage_adaptor.get_params(fb.sage_name),
            'preferred_sages': self.feedback_collector.get_preferred_sages(fb.user_id),
        }
        
        # 触发回调
        for cb in self._callbacks['on_feedback']:
            await cb(learned)
            
        return learned
    
    async def inject_to_claw(self, claw_memory, knowledge_items: List[KnowledgeItem]) -> int:
        """将抓取的知识注入到指定Claw的记忆中。
        
        这是OpenClaw与Claw子系统的关键对接点。
        
        Args:
            claw_memory: ClawMemoryAdapter实例
            knowledge_items: 知识条目列表
            
        Returns:
            成功注入的数量
        """
        injected = 0
        for item in knowledge_items:
            try:
                claw_memory.add_episode(
                    content=f"[外部知识] {item.content[:500]}",
                    importance=item.confidence * 0.7,
                    metadata={"source": item.source, "type": "external", "id": item.id},
                )
                injected += 1
            except Exception:
                self._stats["errors"] += 1
        
        # 持久化
        try:
            claw_memory.persist()
        except Exception:
            pass  # claw_memory.persist()失败时静默忽略
            
        return injected
        
    def register_callback(self, event: str, callback: Callable) -> bool:
        """注册事件回调"""
        if event in self._callbacks:
            self._callbacks[event].append(callback)
            return True
        return False
        
    def get_status(self) -> Dict[str, Any]:
        """获取引擎状态（含反馈学习+推荐统计）"""
        return {
            'sources': list(self.sources.keys()),
            'update_mode': self.update_mode.value,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'registered_callbacks': {k: len(v) for k, v in self._callbacks.items()},
            # 反馈学习状态
            'feedback_stats': self.feedback_collector.get_stats(),
            'active_learner_patterns': len(self.active_learner.patterns),
            # 深层学习状态（Phase 4.5）
            'pattern_learner_stats': self.pattern_learner.get_stats(),
            'recommender_stats': self.recommender.get_recommendation_stats(),
            # 运行时统计
            **self._stats,
        }

    def recommend_sage(self, query: str, user_id: str = "", top_k: int = 5) -> List[Dict[str, Any]]:
        """推荐最合适的贤者

        Args:
            query: 用户查询
            user_id: 用户ID
            top_k: 推荐数量

        Returns:
            [{"sage_name": str, "score": float, "reasons": [str]}, ...]
        """
        result = self.recommender.recommend(query, user_id=user_id, top_k=top_k)
        self._stats["recommendations_made"] += 1

        # 触发回调
        for cb in self._callbacks.get('on_recommend', []):
            try:
                cb({"query": query, "user_id": user_id, "result": result})
            except Exception:
                pass  # cb({'query': query, 'user_id': user_id, 'result': result})失败时静默忽略

        return [
            {
                "sage_name": rec.sage_name,
                "score": round(rec.score, 3),
                "reasons": rec.reasons,
                "is_cold_start": rec.is_cold_start,
            }
            for rec in result.recommendations
        ]

    def clean_content(self, content: str) -> str:
        """清洗内容（使用ContentCleaner）

        Args:
            content: 原始内容

        Returns:
            清洗后的内容
        """
        result = self.cleaner.clean(content)
        return result.content


__all__ = [
    'OpenClawCore',
    'DataSourceConnector',
    'KnowledgeItem',
    'Feedback',
    'UpdateResult',
    'UpdateMode',
    'DataSourceType',
]