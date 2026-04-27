# -*- coding: utf-8 -*-
"""
Tier 2 学派集群 Cloning 加载器 v8.0.0
懒加载所有学派集群（包含V6.2社会科学7学派）

V6.2新增社会科学集群:
- 行为经济学集群
- 传播学集群
- 人类学集群
- 政治经济学集群
- 组织心理学集群
- 社会心理学集群
"""

import logging
from typing import Callable

logger = logging.getLogger(__name__)

# 集群定义表: (name, module_path)
_CLUSTER_DEFS = [
    # 传统学派集群
    ("儒家集群", "intelligence.engines.cloning.clusters.confucian_cluster"),
    ("道家集群", "intelligence.engines.cloning.clusters.daoist_cluster"),
    ("兵家集群", "intelligence.engines.cloning.clusters.military_cluster"),
    ("法家集群", "intelligence.engines.cloning.clusters.legalist_cluster"),
    ("墨家集群", "intelligence.engines.cloning.clusters.mohist_cluster"),
    ("心学集群", "intelligence.engines.cloning.clusters.xinxue_cluster"),
    ("理学集群", "intelligence.engines.cloning.clusters.lixue_cluster"),
    ("纵横家集群", "intelligence.engines.cloning.clusters.diplomatist_cluster"),
    ("医家集群", "intelligence.engines.cloning.clusters.medical_cluster"),
    ("史学集群", "intelligence.engines.cloning.clusters.historian_cluster"),
    ("文学集群", "intelligence.engines.cloning.clusters.literary_cluster"),
    ("科技集群", "intelligence.engines.cloning.clusters.scientist_cluster"),
    ("营销集群", "intelligence.engines.cloning.clusters.marketing_cluster"),
    ("投资集群", "intelligence.engines.cloning.clusters.investment_cluster"),
    ("创业集群", "intelligence.engines.cloning.clusters.entrepreneur_cluster"),
    ("经济学集群", "intelligence.engines.cloning.clusters.economics_cluster"),
    ("心理学集群", "intelligence.engines.cloning.clusters.psychology_cluster"),
    ("社会学集群", "intelligence.engines.cloning.clusters.sociology_cluster"),
    ("治理战略集群", "intelligence.engines.cloning.clusters.governance_cluster"),
    # V6.2社会科学集群
    ("行为经济学集群", "intelligence.engines.cloning.clusters.behavioral_economics_cluster"),
    ("传播学集群", "intelligence.engines.cloning.clusters.communication_cluster"),
    ("人类学集群", "intelligence.engines.cloning.clusters.anthropology_cluster"),
    ("政治经济学集群", "intelligence.engines.cloning.clusters.political_economy_cluster"),
    ("组织心理学集群", "intelligence.engines.cloning.clusters.organizational_psychology_cluster"),
    ("社会心理学集群", "intelligence.engines.cloning.clusters.social_psychology_cluster"),
]


def load_all(cluster_register_fn, cloning_register_fn) -> int:
    """
    加载所有Tier 2集群，并注册集群中的所有成员到全局cloning表

    Args:
        cluster_register_fn: 集群注册函数
        cloning_register_fn: cloning注册函数

    Returns:
        成功加载的集群数量
    """
    import importlib

    loaded = 0
    for name, mod_path in _CLUSTER_DEFS:
        try:
            mod = importlib.import_module(mod_path)
            build_fn = getattr(mod, 'build_cluster', None)
            if build_fn:
                cluster = build_fn()
                cluster_register_fn(cluster)
                # Register all members in the cluster to global clonings
                for member_name, member_cloning in cluster.members.items():
                    cloning_register_fn(member_cloning)
                loaded += 1
                logger.debug(f"Cluster loaded: {name} ({len(cluster.members)} members)")
            else:
                logger.warning(f"Cluster {name}: no build_cluster() function")
        except ImportError as e:
            logger.debug(f"Cluster module not found: {mod_path} ({e})")
        except Exception as e:
            logger.warning(f"Cluster load failed {name}: {e}")

    logger.info(f"Tier2 Clusters loaded: {loaded}/{len(_CLUSTER_DEFS)}")
    return loaded


__all__ = ['load_all']
