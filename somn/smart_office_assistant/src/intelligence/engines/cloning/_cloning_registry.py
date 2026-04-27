# -*- coding: utf-8 -*-
"""
Cloning注册表 v1.0.0

双模式注册表：
1. 简化模式：直接用name/SageProfile存储（tier1/cluster模块使用）
2. 完整模式：CloningRegistry类（未来扩展使用）

当前以简化模式为主，提供全局便捷函数。
"""

import logging
import threading
from typing import Dict, List, Optional, Any
from datetime import datetime

__all__ = [
    "register_cloning", "get_cloning", "list_clonings",
    "list_clusters", "consult_sage", "get_registry_info",
    "CloningRegistry", "get_registry",
]

from ._cloning_types import (
    ClusterResult, ConsultationMethod,
)
from ._cloning_base import SageCloning

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
#  全局注册表（简化模式 - 线程安全）
# ═══════════════════════════════════════════════════════════════

_clonings: Dict[str, SageCloning] = {}           # name -> SageCloning
_clusters: Dict[str, 'SchoolCluster'] = {}        # cluster_name -> SchoolCluster
_cloning_to_cluster: Dict[str, str] = {}          # name -> cluster_name
_lock = threading.Lock()
_initialized = False


def _ensure_initialized() -> None:
    """懒加载：首次调用时加载所有Cloning"""
    global _initialized
    if _initialized:
        return
    with _lock:
        if _initialized:
            return
        _initialized = True
        logger.info("Cloning系统开始懒加载...")
        _load_tier1_clonings()
        _load_tier2_clusters()
        _load_sage_proxies()  # 加载所有750贤者代理
        logger.info(f"Cloning系统初始化完成: {len(_clonings)}人 / {len(_clusters)}集群")


def _load_tier1_clonings() -> None:
    """加载Tier 1 核心Cloning"""
    try:
        from .tier1 import load_all
        count = load_all(register_cloning)
        logger.debug(f"Tier1加载完成: {count}人")
    except ImportError as e:
        logger.debug(f"Tier1 Cloning加载跳过: {e}")
    except Exception as e:
        logger.warning(f"Tier1 Cloning加载异常: {e}")


def _load_tier2_clusters() -> None:
    """加载Tier 2 学派集群"""
    try:
        from .clusters import load_all
        count = load_all(_register_cluster_internal, register_cloning)
        logger.debug(f"Tier2集群加载完成: {count}个")
    except ImportError as e:
        logger.debug(f"Tier2 集群加载跳过: {e}")
    except Exception as e:
        logger.warning(f"Tier2 集群加载异常: {e}")


def _load_sage_proxies() -> None:
    """加载所有贤者的智能代理（从文学研究目录读取）"""
    try:
        from ._sage_proxy_factory import build_sage_proxies_from_literature
        proxies = build_sage_proxies_from_literature()
        for name, cloning in proxies.items():
            with _lock:
                if name not in _clonings:
                    _clonings[name] = cloning
        logger.debug(f"贤者代理加载完成: {len(proxies)}个")
    except ImportError as e:
        logger.debug(f"贤者代理模块不存在: {e}")
    except Exception as e:
        logger.warning(f"贤者代理加载异常: {e}")


# ═══════════════════════════════════════════════════════════════
#  公开API
# ═══════════════════════════════════════════════════════════════

def register_cloning(cloning: SageCloning) -> None:
    """注册一个Cloning实例"""
    name = getattr(cloning, 'name', None) or getattr(cloning, 'identity', None)
    if name is None:
        logger.warning(f"Cloning没有name属性，跳过注册: {type(cloning).__name__}")
        return
    key = name if isinstance(name, str) else name.name
    with _lock:
        if key not in _clonings:
            _clonings[key] = cloning


def _register_cluster_internal(cluster) -> None:
    """内部：注册集群（不重复注册成员）"""
    name = getattr(cluster, 'name', '') or getattr(cluster, 'cluster_name', '')
    if name:
        with _lock:
            _clusters[name] = cluster
        # 将集群成员注册到全局索引
        members = getattr(cluster, '_members', {}) or getattr(cluster, 'members', {})
        for m_name, m_cloning in members.items():
            with _lock:
                if m_name not in _clonings:
                    _clonings[m_name] = m_cloning
                    _cloning_to_cluster[m_name] = name


def get_cloning(name: str) -> Optional[SageCloning]:
    """按名称获取Cloning"""
    _ensure_initialized()
    return _clonings.get(name)


def list_clonings() -> List[str]:
    """列出所有已注册Cloning的名称"""
    _ensure_initialized()
    return list(_clonings.keys())


def list_clusters() -> List[str]:
    """列出所有已注册集群的名称"""
    _ensure_initialized()
    return list(_clusters.keys())


def consult_sage(
    cluster_name: str,
    problem: str,
    method: str = "leader",
    context: Optional[Dict[str, Any]] = None
) -> Optional[ClusterResult]:
    """
    咨询学派集群

    Args:
        cluster_name: 集群名称（如"儒家集群"）
        problem: 要咨询的问题
        method: 咨询方法 (leader/consensus/debate/synthesis)
        context: 额外上下文

    Returns:
        ClusterResult 或 None
    """
    _ensure_initialized()
    cluster = _clusters.get(cluster_name)
    if not cluster:
        logger.warning(f"集群 '{cluster_name}' 不存在")
        return None

    try:
        # 尝试调用集群的consult方法（如果有的话）
        if hasattr(cluster, 'consult'):
            return cluster.consult(problem, method=method, context=context)
    except Exception as e:
        logger.warning(f"集群咨询失败: {e}")

    # 回退：手动构建咨询结果
    members = getattr(cluster, '_members', {}) or getattr(cluster, 'members', {})
    leader_name = getattr(cluster, 'leader_name', '')
    leader = members.get(leader_name)

    analyses = []
    participant_count = 0
    if method == "leader" and leader:
        try:
            r = leader.analyze(problem, context)
            analyses.append(r)
            participant_count = 1
        except Exception as e:
            logger.debug(f"participant_count = 1失败: {e}")
    else:
        for m_name, m_cloning in members.items():
            try:
                r = m_cloning.analyze(problem, context)
                analyses.append(r)
                participant_count += 1
            except Exception as e:
                logger.debug(f"participant_count += 1失败: {e}")

    if not analyses:
        return None

    # 构建结果
    primary = analyses[0]
    synthesis = ""
    if method == "synthesis" and len(analyses) > 1:
        parts = []
        for a in analyses:
            content = getattr(a, 'core_insight', '') or getattr(a, 'analysis_content', '')
            if content:
                parts.append(content[:80])
        synthesis = " | ".join(parts[:5])
    elif method == "debate" and len(analyses) > 1:
        parts = []
        for a in analyses:
            sname = getattr(a, 'sage_name', '') or getattr(a, 'cloning_name', '')
            content = getattr(a, 'core_insight', '') or getattr(a, 'perspective', '')
            parts.append(f"{sname}: {content[:60]}")
        synthesis = "【辩论】" + "; ".join(parts[:5])
    elif method == "consensus" and len(analyses) > 1:
        # 简单共识：取最高置信度
        best = max(analyses, key=lambda a: getattr(a, 'confidence', 0.5))
        synthesis = getattr(best, 'core_insight', '') or getattr(best, 'analysis_content', '')
    else:
        synthesis = getattr(primary, 'core_insight', '') or getattr(primary, 'analysis_content', '')

    return ClusterResult(
        cluster_name=cluster_name,
        method=method,
        synthesis=synthesis,
        participant_count=participant_count,
        leader_analysis=primary if (method == "leader" and leader) else None,
    )


def get_registry_info() -> Dict[str, Any]:
    """获取注册表摘要信息"""
    _ensure_initialized()
    by_school: Dict[str, int] = {}
    by_tier: Dict[str, int] = {}
    by_dept: Dict[str, int] = {}

    for name, c in _clonings.items():
        school = getattr(c, 'school', '') or (getattr(c, 'identity', None) and c.identity.school) or ''
        tier = getattr(c, 'tier', None)
        dept = getattr(c, 'department', '') or (getattr(c, 'identity', None) and c.identity.department) or ''

        if school:
            by_school[school] = by_school.get(school, 0) + 1
        tier_key = str(tier) if tier else "unknown"
        by_tier[tier_key] = by_tier.get(tier_key, 0) + 1
        if dept:
            by_dept[dept] = by_dept.get(dept, 0) + 1

    return {
        "total_clonings": len(_clonings),
        "total_clusters": len(_clusters),
        "by_school": by_school,
        "by_tier": by_tier,
        "by_department": by_dept,
        "cloning_names": sorted(_clonings.keys()),
        "cluster_names": sorted(_clusters.keys()),
    }


# ═══════════════════════════════════════════════════════════════
#  完整模式（CloningRegistry类）- 保留供未来使用
# ═══════════════════════════════════════════════════════════════

class CloningRegistry:
    """完整版Cloning注册表（单例）"""
    _instance: Optional['CloningRegistry'] = None
    _lock = threading.Lock()

    def __new__(cls) -> 'CloningRegistry':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._clonings: Dict[str, SageCloning] = {}
        self._clusters: Dict[str, Any] = {}
        self._by_school: Dict[str, List[str]] = {}
        self._by_tier: Dict[str, List[str]] = {}
        self._by_department: Dict[str, List[str]] = {}
        self._registry_lock = threading.Lock()

    def register(self, cloning: SageCloning) -> None:
        """注册Cloning"""
        with self._registry_lock:
            name = getattr(cloning, 'name', '') or (hasattr(cloning, 'identity') and cloning.identity.name) or ''
            if not name:
                return
            self._clonings[name] = cloning

    def get(self, name: str) -> Optional[SageCloning]:
        return self._clonings.get(name)

    def get_summary(self) -> Dict[str, Any]:
        return {
            'total_clonings': len(self._clonings),
            'total_clusters': len(self._clusters),
            'by_school': {k: len(v) for k, v in self._by_school.items()},
            'by_tier': {k: len(v) for k, v in self._by_tier.items()},
        }


def get_registry() -> CloningRegistry:
    """获取完整版注册表实例"""
    return CloningRegistry()
