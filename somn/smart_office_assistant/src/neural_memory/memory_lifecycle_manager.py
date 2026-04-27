"""
__all__ = [
    'apply_decay',
    'evolve_knowledge',
    'get_health_report',
    'get_knowledge_registry',
    'trigger_review',
]

记忆生命周期管理器 - Memory Lifecycle Manager v1.0.0
管理知识的完整生命周期：创建 → 强化 → 衰减 → 复习 → 进化

核心功能:
1. 知识注册 - 统一管理所有知识条目
2. 记忆衰减 - 基于遗忘曲线的置信度衰减
3. 复习触发 - 判断何时需要复习特定知识
4. 知识进化 - 基于新证据更新知识
5. 健康度评估 - 评估知识库整体健康状态
"""

from __future__ import annotations

import logging
import json
import yaml
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

from src.core.paths import LEARNING_DIR

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════

class KnowledgeStatus(Enum):
    """知识状态"""
    ACTIVE = "active"              # 活跃
    STALE = "stale"                # 陈旧
    WEAK = "weak"                  # 弱记忆
    REVIEWING = "reviewing"        # 复习中
    EVOLVING = "evolving"          # 进化中
    ARCHIVED = "archived"          # 归档
    DELETED = "deleted"            # 已删除

class DecayModel(Enum):
    """衰减模型"""
    EXPONENTIAL = "exponential"     # 指数衰减
    LINEAR = "linear"              # 线性衰减
    STEP = "step"                  # 阶梯衰减
    CUSTOM = "custom"              # 自定义

@dataclass
class KnowledgeEntry:
    """知识条目"""
    knowledge_id: str
    concept: str                   # 核心概念
    content: str                   # 内容摘要
    category: str                  # 分类
    confidence: float              # 置信度 0-1
    importance: float              # 重要性 0-1
    
    # 生命周期
    created_at: str
    last_accessed: str
    last_modified: str
    access_count: int = 0
    review_count: int = 0
    
    # 状态
    status: KnowledgeStatus = KnowledgeStatus.ACTIVE
    decay_model: DecayModel = DecayModel.EXPONENTIAL
    
    # 关联
    related_knowledge: List[str] = field(default_factory=list)
    evidence: List[Dict] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    # 元数据
    source: str = ""               # 来源
    author: str = ""               # 创建者
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "knowledge_id": self.knowledge_id,
            "concept": self.concept,
            "content": self.content,
            "category": self.category,
            "confidence": self.confidence,
            "importance": self.importance,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "last_modified": self.last_modified,
            "access_count": self.access_count,
            "review_count": self.review_count,
            "status": self.status.value,
            "decay_model": self.decay_model.value,
            "related_knowledge": self.related_knowledge,
            "evidence": self.evidence,
            "tags": self.tags,
            "source": self.source,
            "author": self.author,
            "metadata": self.metadata
        }

@dataclass
class HealthReport:
    """健康度报告"""
    total_knowledge: int
    active_count: int
    stale_count: int
    weak_count: int
    reviewing_count: int
    
    avg_confidence: float
    avg_importance: float
    avg_age_days: float
    
    health_score: float           # 0-100
    health_status: str            # excellent / good / fair / poor
    
    recommendations: List[str]
    weak_knowledge: List[Dict]    # 需要关注的知识

@dataclass
class ReviewTask:
    """复习任务"""
    knowledge_id: str
    concept: str
    current_confidence: float
    decay_confidence: float
    days_since_access: int
    priority: float               # 优先级
    reason: str                  # 触发原因

# ═══════════════════════════════════════════════════════════════════
# 记忆生命周期管理器
# ═══════════════════════════════════════════════════════════════════

class MemoryLifecycleManager:
    """
    记忆生命周期管理器 v1.0.0
    
    功能:
    1. 知识注册表 - 统一管理所有知识
    2. 衰减管理 - 多种衰减模型
    3. 复习触发 - 智能判断复习时机
    4. 知识进化 - 基于证据的知识更新
    5. 健康度评估 - 知识库健康状态
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else LEARNING_DIR
        self.registry_path = self.base_path / "knowledge_registry"
        self.registry_path.mkdir(parents=True, exist_ok=True)

        # [v1.0 增量加载优化] 轻量索引 + 按需加载条目
        self._index = {}  # 轻量索引：{knowledge_id: {concept, category, confidence, status, ...}}
        self.knowledge: Dict[str, KnowledgeEntry] = {}  # 全量条目（按需加载）
        self._load_index()  # 只加载索引，不加载全量数据

        # 迁移旧格式（如果存在）
        self._migrate_old_format()

        # 衰减参数
        
        # 衰减参数
        self.decay_config = {
            "exponential": {"base_rate": 0.01, "half_life_days": 30},
            "linear": {"rate": 0.001, "min_confidence": 0.1},
            "step": {"interval_days": 7, "decay_step": 0.05}
        }
        
        # 复习参数
        self.review_config = {
            "threshold_confidence": 0.3,      # 置信度阈值
            "threshold_days": 7,              # 时间阈值
            "priority_weights": {
                "confidence": 0.4,
                "importance": 0.3,
                "days_since_access": 0.3
            }
        }
        
        logger.info("记忆生命周期管理器初始化完成")
        logger.info(f"  知识条目: {len(self.knowledge)}")
    
    # ─────────────────────────────────────────────────────────────────
    # 核心API
    # ─────────────────────────────────────────────────────────────────
    
    def register_knowledge(self,
                         concept: str,
                         content: str,
                         category: str = "general",
                         importance: float = 0.5,
                         source: str = "",
                         tags: List[str] = None,
                         metadata: Dict = None) -> KnowledgeEntry:
        """
        注册新知识
        
        Args:
            concept: 核心概念
            content: 内容摘要
            category: 分类
            importance: 重要性 0-1
            source: 来源
            tags: 标签
            metadata: 元数据
        
        Returns:
            KnowledgeEntry: 新创建的知识条目
        """
        now = datetime.now().isoformat()
        
        # 生成ID
        knowledge_id = f"KN_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        
        # 检查重复
        for existing in self.knowledge.values():
            if existing.concept == concept and existing.status != KnowledgeStatus.DELETED:
                logger.warning(f"知识已存在: {concept}")
                return existing
        
        entry = KnowledgeEntry(
            knowledge_id=knowledge_id,
            concept=concept,
            content=content,
            category=category,
            confidence=0.8,  # 新知识初始置信度
            importance=importance,
            created_at=now,
            last_accessed=now,
            last_modified=now,
            status=KnowledgeStatus.ACTIVE,
            source=source,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        self.knowledge[knowledge_id] = entry

        # [v1.0 增量加载] 保存到独立文件 + 更新索引
        self._update_index(entry)
        self._save_entry(knowledge_id)
        self._save_index()

        logger.info(f"注册知识: {concept}, ID: {knowledge_id}")
        
        return entry
    
    def apply_decay(self,
                   knowledge_ids: List[str] = None,
                   force: bool = False) -> Dict[str, float]:
        """
        [增量加载优化] 应用记忆衰减

        未指定 knowledge_ids 时，从索引获取全部 ID，逐条懒加载。

        Args:
            knowledge_ids: 要衰减的知识ID列表，None表示全部
            force: 是否强制衰减（不考虑访问）

        Returns:
            Dict[str, float]: {knowledge_id: decay_amount}
        """
        decay_results = {}

        # [v1.0 增量加载] 如果未指定 ID，从索引获取全部
        if knowledge_ids is None:
            knowledge_ids = list(self._index.keys())

        for kid in knowledge_ids:
            entry = self._load_entry(kid)
            if not entry:
                continue

            # 跳过非活跃和复习中的知识
            if entry.status not in [KnowledgeStatus.ACTIVE, KnowledgeStatus.STALE]:
                continue

            # 计算衰减
            decay = self._calculate_decay(entry, force)

            if decay > 0:
                old_conf = entry.confidence
                entry.confidence = max(0.1, entry.confidence - decay)
                entry.last_modified = datetime.now().isoformat()
                decay_results[kid] = old_conf - entry.confidence

                # 更新状态
                self._update_status(entry)

                # [v1.0 增量加载] 保存独立文件和索引
                self._update_index(entry)
                self._save_entry(kid)

        if decay_results:
            self._save_index()

        return decay_results
    
    def trigger_review(self,
                      max_tasks: int = 10,
                      category: str = None) -> List[ReviewTask]:
        """
        [增量加载优化] 触发复习任务

        从索引获取候选，按需加载完整条目。

        Args:
            max_tasks: 最大任务数
            category: 指定分类
        
        Returns:
            List[ReviewTask]: 复习任务列表
        """
        tasks = []
        now = datetime.now()
        
        # [v1.0 增量加载] 从索引获取候选，按需加载
        for kid in self._index.keys():
            meta = self._index.get(kid, {})
            if meta.get("status") == KnowledgeStatus.DELETED.value:
                continue
            
            if category and meta.get("category") != category:
                continue
            
            entry = self._load_entry(kid)
            if not entry:
                continue
            
            # 检查是否需要复习
            days_since = (now - datetime.fromisoformat(entry.last_accessed)).days
            
            # 置信度过低
            if entry.confidence < self.review_config["threshold_confidence"]:
                priority = self._calculate_priority(entry, days_since)
                tasks.append(ReviewTask(
                    knowledge_id=entry.knowledge_id,
                    concept=entry.concept,
                    current_confidence=entry.confidence,
                    decay_confidence=entry.confidence,
                    days_since_access=days_since,
                    priority=priority,
                    reason="低置信度"
                ))
                continue
            
            # 长时间未访问
            if days_since > self.review_config["threshold_days"]:
                priority = self._calculate_priority(entry, days_since)
                tasks.append(ReviewTask(
                    knowledge_id=entry.knowledge_id,
                    concept=entry.concept,
                    current_confidence=entry.confidence,
                    decay_confidence=entry.confidence,
                    days_since_access=days_since,
                    priority=priority,
                    reason="长时间未复习"
                ))
        
        # 按优先级排序
        tasks.sort(key=lambda x: x.priority, reverse=True)
        
        return tasks[:max_tasks]
    
    def evolve_knowledge(self,
                        knowledge_id: str,
                        new_evidence: Dict,
                        confidence_boost: float = 0.0) -> Optional[KnowledgeEntry]:
        """
        [增量加载优化] 知识进化 - 基于新证据更新知识

        Args:
            knowledge_id: 知识ID
            new_evidence: 新证据 {type, content, weight}
            confidence_boost: 置信度提升
        
        Returns:
            更新后的知识条目
        """
        entry = self._load_entry(knowledge_id)
        if not entry:
            return None
        
        entry.last_accessed = datetime.now().isoformat()
        entry.last_modified = datetime.now().isoformat()
        entry.access_count += 1
        
        # 添加新证据
        evidence_item = {
            "type": new_evidence.get("type", "inference"),
            "content": new_evidence.get("content", ""),
            "weight": new_evidence.get("weight", 0.5),
            "timestamp": datetime.now().isoformat()
        }
        entry.evidence.append(evidence_item)
        
        # 计算新的置信度
        if confidence_boost > 0:
            # 基于证据权重计算提升
            evidence_weights = [e["weight"] for e in entry.evidence]
            avg_weight = sum(evidence_weights) / len(evidence_weights)
            boost = confidence_boost * avg_weight
            
            entry.confidence = min(1.0, entry.confidence + boost)
        else:
            # 基于贝叶斯更新
            entry.confidence = self._bayesian_update(entry, new_evidence)
        
        # 更新状态
        entry.status = KnowledgeStatus.ACTIVE

        # [v1.0 增量加载] 保存独立文件和索引
        self._update_index(entry)
        self._save_entry(knowledge_id)
        self._save_index()
        
        logger.info(f"知识进化: {entry.concept}, 新置信度: {entry.confidence:.3f}")
        
        return entry
    
    def reinforce_knowledge(self, knowledge_id: str, boost: float = 0.1) -> Optional[KnowledgeEntry]:
        """
        [增量加载优化] 强化知识 - 复习后提升置信度

        Args:
            knowledge_id: 知识ID
            boost: 提升量
        
        Returns:
            更新后的知识条目
        """
        entry = self._load_entry(knowledge_id)
        if not entry:
            return None
        
        entry.confidence = min(1.0, entry.confidence + boost)
        entry.review_count += 1
        entry.last_accessed = datetime.now().isoformat()
        entry.status = KnowledgeStatus.ACTIVE
        
        # [v1.0 增量加载] 保存独立文件和索引
        self._update_index(entry)
        self._save_entry(knowledge_id)
        self._save_index()
        
        return entry
    
    def get_health_report(self) -> HealthReport:
        """
        [增量加载优化] 获取知识库健康度报告

        使用索引计算大部分指标，只对弱知识按需懒加载，避免全量读入。

        Returns:
            HealthReport: 健康度报告
        """
        now = datetime.now()
        active_count = 0
        stale_count = 0
        weak_count = 0
        reviewing_count = 0

        total_confidence = 0.0
        total_importance = 0.0
        total_age = 0.0

        # [v1.0 增量加载] 使用索引计算，无需加载全量条目
        count = 0
        weak_ids = []  # 收集弱知识的 ID，后续按需加载

        for kid, meta in self._index.items():
            if meta.get("status") == KnowledgeStatus.DELETED.value:
                continue

            count += 1
            confidence = meta.get("confidence", 0)
            importance = meta.get("importance", 0)

            total_confidence += confidence
            total_importance += importance

            created = datetime.fromisoformat(meta.get("created_at", now.isoformat()))
            age_days = (now - created).days
            total_age += age_days

            status = meta.get("status", "active")
            if status == KnowledgeStatus.ACTIVE.value:
                active_count += 1
            elif status == KnowledgeStatus.STALE.value:
                stale_count += 1
            elif status == KnowledgeStatus.WEAK.value:
                weak_count += 1
                weak_ids.append(kid)
            elif status == KnowledgeStatus.REVIEWING.value:
                reviewing_count += 1

            # 置信度低于阈值视为弱
            if confidence < 0.3:
                if kid not in weak_ids:
                    weak_count += 1
                    weak_ids.append(kid)

        if count == 0:
            return HealthReport(
                total_knowledge=0,
                active_count=0, stale_count=0, weak_count=0, reviewing_count=0,
                avg_confidence=0, avg_importance=0, avg_age_days=0,
                health_score=0, health_status="empty",
                recommendations=["知识库为空，建议添加新知识"],
                weak_knowledge=[]
            )

        avg_confidence = total_confidence / count
        avg_importance = total_importance / count
        avg_age = total_age / count

        # 计算健康分 (0-100)
        health_score = (
            (active_count / count) * 40 +
            avg_confidence * 30 +
            (1 - weak_count / max(count, 1)) * 30
        )

        # 判断健康状态
        if health_score >= 80:
            health_status = "excellent"
        elif health_score >= 60:
            health_status = "good"
        elif health_score >= 40:
            health_status = "fair"
        else:
            health_status = "poor"

        # 生成建议
        recommendations = []
        if weak_count > count * 0.3:
            recommendations.append(f"弱知识过多 ({weak_count}), 建议加强复习")
        if avg_age > 60:
            recommendations.append("知识库老化, 建议更新陈旧知识")
        if stale_count > count * 0.2:
            recommendations.append(f"陈旧知识较多 ({stale_count}), 建议定期清理")
        if health_score >= 60:
            recommendations.append("知识库运行良好, 继续保持")

        # [v1.0 增量加载] 按需加载弱知识（最多5条）
        weak_knowledge = []
        for kid in weak_ids[:5]:
            entry = self._load_entry(kid)
            if entry:
                weak_knowledge.append({
                    "knowledge_id": entry.knowledge_id,
                    "concept": entry.concept,
                    "confidence": entry.confidence,
                    "status": entry.status.value
                })

        return HealthReport(
            total_knowledge=count,
            active_count=active_count,
            stale_count=stale_count,
            weak_count=weak_count,
            reviewing_count=reviewing_count,
            avg_confidence=avg_confidence,
            avg_importance=avg_importance,
            avg_age_days=avg_age,
            health_score=health_score,
            health_status=health_status,
            recommendations=recommendations,
            weak_knowledge=weak_knowledge
        )
    
    def get_knowledge_registry(self,
                              category: str = None,
                              status: KnowledgeStatus = None,
                              min_confidence: float = 0.0) -> List[KnowledgeEntry]:
        """
        [增量加载优化] 获取知识注册表
        
        使用索引快速过滤，按需加载完整条目，避免一次性全量读入。
        
        Args:
            category: 分类筛选
            status: 状态筛选
            min_confidence: 最低置信度
        
        Returns:
            List[KnowledgeEntry]: 知识列表
        """
        results = []
        
        # [v1.0 增量加载] 使用索引快速过滤（只比较元数据，不加载全量数据）
        candidate_ids = []
        for kid, meta in self._index.items():
            # 跳过已删除的条目
            if meta.get("status") == KnowledgeStatus.DELETED.value:
                continue

            # 状态筛选
            if status:
                target_status = status.value if isinstance(status, KnowledgeStatus) else status
                if meta.get("status") != target_status:
                    continue

            # 分类筛选
            if category and meta.get("category") != category:
                continue

            # 置信度筛选
            if meta.get("confidence", 0) < min_confidence:
                continue

            candidate_ids.append(kid)
        
        # 按需加载完整条目
        for kid in candidate_ids:
            entry = self._load_entry(kid)
            if entry:
                results.append(entry)
        
        # 按置信度和重要性排序
        results.sort(key=lambda x: (x.confidence * 0.6 + x.importance * 0.4), reverse=True)
        
        logger.debug(f"[增量加载] 查询到 {len(results)} 条知识（索引过滤: {len(candidate_ids)} 条）")
        return results
    
    def relate_knowledge(self, 
                        knowledge_id_a: str,
                        knowledge_id_b: str,
                        relation_type: str = "related") -> bool:
        """
        建立知识关联
        
        Args:
            knowledge_id_a: 知识A ID
            knowledge_id_b: 知识B ID
            relation_type: 关联类型
        
        Returns:
            bool: 是否成功
        """
        if knowledge_id_a not in self.knowledge or knowledge_id_b not in self.knowledge:
            return False
        
        entry_a = self.knowledge[knowledge_id_a]
        entry_b = self.knowledge[knowledge_id_b]
        
        if knowledge_id_b not in entry_a.related_knowledge:
            entry_a.related_knowledge.append(knowledge_id_b)
        
        if knowledge_id_a not in entry_b.related_knowledge:
            entry_b.related_knowledge.append(knowledge_id_a)
        
        entry_a.last_modified = datetime.now().isoformat()
        entry_b.last_modified = datetime.now().isoformat()
        
        # [v1.0 增量加载] 保存独立文件 + 更新索引
        self._update_index(entry_a)
        self._update_index(entry_b)
        self._save_entry(knowledge_id_a)
        self._save_entry(knowledge_id_b)
        self._save_index()
        
        return True
    
    # ─────────────────────────────────────────────────────────────────
    # 内部方法
    # ─────────────────────────────────────────────────────────────────
    
    def _calculate_decay(self, entry: KnowledgeEntry, force: bool) -> float:
        """计算衰减量"""
        days_since = (datetime.now() - datetime.fromisoformat(entry.last_accessed)).days
        
        # 如果最近访问过，减少衰减
        if not force and days_since < 1:
            return 0.0
        
        model = entry.decay_model
        
        if model == DecayModel.EXPONENTIAL:
            config = self.decay_config["exponential"]
            half_life = config["half_life_days"]
            # 指数衰减: C(t) = C0 * (0.5)^(t/half_life)
            decay = 1 - pow(0.5, days_since / half_life)
            return entry.confidence * decay * 0.1  # 减缓衰减速度
        
        elif model == DecayModel.LINEAR:
            config = self.decay_config["linear"]
            return config["rate"] * days_since
        
        elif model == DecayModel.STEP:
            config = self.decay_config["step"]
            steps = days_since // config["interval_days"]
            return steps * config["decay_step"]
        
        return 0.0
    
    def _update_status(self, entry: KnowledgeEntry):
        """更新知识状态"""
        if entry.confidence < 0.2:
            entry.status = KnowledgeStatus.WEAK
        elif entry.confidence < 0.4:
            days_since = (datetime.now() - datetime.fromisoformat(entry.last_accessed)).days
            if days_since > 14:
                entry.status = KnowledgeStatus.STALE
    
    def _calculate_priority(self, entry: KnowledgeEntry, days_since: int) -> float:
        """计算复习优先级"""
        weights = self.review_config["priority_weights"]
        
        # 置信度得分 (越低优先级越高)
        conf_score = 1 - entry.confidence
        
        # 重要性得分
        imp_score = entry.importance
        
        # 时间得分 (越久优先级越高)
        time_score = min(1.0, days_since / 30)
        
        priority = (
            conf_score * weights["confidence"] +
            imp_score * weights["importance"] +
            time_score * weights["days_since_access"]
        )
        
        return priority

    # ── [v1.0 增量加载优化] 新增方法 ───────────────────────────────────

    def _load_index(self):
        """[增量加载优化] 只加载轻量索引，不加载全量数据"""
        index_file = self.registry_path / "index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    self._index = json.load(f)
            except Exception as e:
                logger.warning(f"加载索引失败: {e}")
                self._index = {}
        else:
            self._index = {}

    def _save_index(self):
        """保存轻量索引"""
        try:
            index_file = self.registry_path / "index.json"
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(self._index, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"保存索引失败: {e}")

    def _update_index(self, entry: KnowledgeEntry):
        """更新索引中的条目元数据"""
        self._index[entry.knowledge_id] = {
            "concept": entry.concept,
            "category": entry.category,
            "confidence": entry.confidence,
            "importance": entry.importance,
            "status": entry.status.value,
            "last_accessed": entry.last_accessed,
            "created_at": entry.created_at,
        }

    def _load_entry(self, knowledge_id: str) -> Optional[KnowledgeEntry]:
        """[增量加载优化] 按需加载单个条目"""
        # 已加载
        if knowledge_id in self.knowledge:
            return self.knowledge[knowledge_id]

        # 从独立文件加载
        entries_dir = self.registry_path / "entries"
        entry_file = entries_dir / f"{knowledge_id}.json"
        if entry_file.exists():
            try:
                with open(entry_file, 'r', encoding='utf-8') as f:
                    kdata = json.load(f)
                kdata["status"] = KnowledgeStatus(kdata.get("status", "active"))
                kdata["decay_model"] = DecayModel(kdata.get("decay_model", "exponential"))
                entry = KnowledgeEntry(**kdata)
                self.knowledge[knowledge_id] = entry
                return entry
            except Exception as e:
                logger.warning(f"加载条目 {knowledge_id} 失败: {e}")
                return None

        return None

    def _save_entry(self, knowledge_id: str):
        """保存单个条目到独立文件"""
        if knowledge_id not in self.knowledge:
            return

        entries_dir = self.registry_path / "entries"
        entries_dir.mkdir(parents=True, exist_ok=True)

        entry_file = entries_dir / f"{knowledge_id}.json"
        entry = self.knowledge[knowledge_id]
        try:
            with open(entry_file, 'w', encoding='utf-8') as f:
                json.dump(entry.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"保存条目 {knowledge_id} 失败: {e}")

    def _migrate_old_format(self):
        """从旧格式迁移到新格式（增量加载）"""
        old_file = self.registry_path / "knowledge_registry.json"
        if not old_file.exists():
            return

        # 如果新格式已存在，跳过迁移
        index_file = self.registry_path / "index.json"
        if index_file.exists():
            return

        logger.info("[迁移] 检测到旧格式 knowledge_registry.json，开始迁移到增量加载格式...")

        try:
            with open(old_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for kid, kdata in data.items():
                kdata["status"] = KnowledgeStatus(kdata.get("status", "active"))
                kdata["decay_model"] = DecayModel(kdata.get("decay_model", "exponential"))
                entry = KnowledgeEntry(**kdata)
                self.knowledge[kid] = entry

                # 更新索引
                self._update_index(entry)

                # 保存到独立文件
                self._save_entry(kid)

            # 保存索引
            self._save_index()

            # 备份旧文件
            backup_file = self.registry_path / "knowledge_registry.json.bak"
            shutil.move(str(old_file), str(backup_file))

            logger.info(f"[迁移] 完成: {len(self._index)} 条知识已迁移到增量加载格式")
            logger.info(f"[迁移] 旧文件已备份到: {backup_file}")

        except Exception as e:
            logger.warning(f"[迁移] 失败: {e}")

    # ── 原有方法（修改版）────────────────────────────────────────────────────

    def _bayesian_update(self, entry: KnowledgeEntry, new_evidence: Dict) -> float:
        """贝叶斯更新置信度"""
        weight = new_evidence.get("weight", 0.5)
        
        # 简化的贝叶斯更新
        # P(H|E) = P(E|H) * P(H) / P(E)
        prior = entry.confidence
        likelihood = 0.5 + weight * 0.5  # 0.5-1.0
        
        posterior = (likelihood * prior) / (likelihood * prior + (1 - likelihood) * (1 - prior))
        
        # 平滑过渡
        alpha = 0.3
        return alpha * posterior + (1 - alpha) * entry.confidence
    
    def _load_registry(self):
        """加载知识注册表"""
        registry_file = self.registry_path / "knowledge_registry.json"
        if registry_file.exists():
            try:
                with open(registry_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for kid, kdata in data.items():
                        kdata["status"] = KnowledgeStatus(kdata.get("status", "active"))
                        kdata["decay_model"] = DecayModel(kdata.get("decay_model", "exponential"))
                        self.knowledge[kid] = KnowledgeEntry(**kdata)
                logger.debug(f"加载知识注册表: {len(self.knowledge)} 条")
            except Exception as e:
                logger.warning(f"加载知识注册表失败: {e}")
    
    def _save_registry(self):
        """[v1.0 增量加载] 保存索引 + 所有独立条目文件（全量备份）"""
        try:
            # 保存轻量索引
            self._save_index()

            # 保存所有已加载的条目到独立文件
            for kid in list(self.knowledge.keys()):
                self._save_entry(kid)

            # 同时保存一份全量 JSON 作为备份（兼容旧接口）
            registry_file = self.registry_path / "knowledge_registry.json.bak"
            data = {kid: entry.to_dict() for kid, entry in self.knowledge.items()}
            with open(registry_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.debug(f"[增量加载] 已保存 {len(self.knowledge)} 条知识（索引 + 独立文件）")
        except Exception as e:
            logger.warning(f"保存知识注册表失败: {e}")


# ═══════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════

_manager_instance = None

def get_knowledge_registry() -> MemoryLifecycleManager:
    """获取管理器单例"""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = MemoryLifecycleManager()
    return _manager_instance

def apply_decay(knowledge_ids: List[str] = None, force: bool = False) -> Dict[str, float]:
    """便捷函数：应用衰减"""
    return get_knowledge_registry().apply_decay(knowledge_ids, force)

def trigger_review(max_tasks: int = 10, category: str = None) -> List[ReviewTask]:
    """便捷函数：触发复习"""
    return get_knowledge_registry().trigger_review(max_tasks, category)

def evolve_knowledge(knowledge_id: str, new_evidence: Dict, boost: float = 0.0) -> Optional[KnowledgeEntry]:
    """便捷函数：知识进化"""
    return get_knowledge_registry().evolve_knowledge(knowledge_id, new_evidence, boost)

def get_health_report() -> HealthReport:
    """便捷函数：获取健康报告"""
    return get_knowledge_registry().get_health_report()
