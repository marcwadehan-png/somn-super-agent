# -*- coding: utf-8 -*-
"""
Tier 1 Cloning 加载器 v1.0.0
懒加载所有核心独立Cloning
"""

import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)

# Tier 1 Cloning模块映射表
# 格式: (模块路径, 类名)
_TIER1_MODULES = [
    ("intelligence.engines.cloning.tier1.confucius", "ConfuciusCloning"),
    ("intelligence.engines.cloning.tier1.laotzu", "LaoTzuCloning"),
    ("intelligence.engines.cloning.tier1.sunwu", "SunWuCloning"),
    ("intelligence.engines.cloning.tier1.hanfeizi", "HanFeiZiCloning"),
    ("intelligence.engines.cloning.tier1.guiguzi", "GuiGuZiCloning"),
    ("intelligence.engines.cloning.tier1.mozi", "MoZiCloning"),
    ("intelligence.engines.cloning.tier1.wangyangming", "WangYangMingCloning"),
    ("intelligence.engines.cloning.tier1.zhuxi", "ZhuXiCloning"),
    ("intelligence.engines.cloning.tier1.zhugege", "ZhugeLiangCloning"),
    ("intelligence.engines.cloning.tier1.kotler", "KotlerCloning"),
    ("intelligence.engines.cloning.tier1.drucker", "DruckerCloning"),
    ("intelligence.engines.cloning.tier1.buffett", "BuffettCloning"),
    ("intelligence.engines.cloning.tier1.musk", "MuskCloning"),
    ("intelligence.engines.cloning.tier1.jobs", "JobsCloning"),
]


def load_all(register_fn: Callable) -> int:
    """
    加载所有Tier 1 Cloning

    Args:
        register_fn: 注册函数 (SageCloning) -> None

    Returns:
        成功加载的数量
    """
    import importlib

    loaded = 0
    for mod_path, class_name in _TIER1_MODULES:
        try:
            mod = importlib.import_module(mod_path)
            cls = getattr(mod, class_name)
            instance = cls()
            register_fn(instance)
            loaded += 1
            logger.debug(f"Tier1 loaded: {class_name}")
        except ImportError:
            logger.debug(f"Tier1 module not found: {mod_path}")
        except Exception as e:
            logger.warning(f"Tier1 load failed {mod_path}.{class_name}: {e}")

    logger.info(f"Tier1 Cloning loaded: {loaded}/{len(_TIER1_MODULES)}")
    return loaded


__all__ = ['load_all']
