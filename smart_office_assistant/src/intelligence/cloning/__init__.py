# -*- coding: utf-8 -*-
"""
贤者工程第三层: Cloning (克隆实现)

提供Sage代理工厂和Somn克隆引擎

模块:
- _sage_proxy_factory: Sage代理工厂
- _somn_clone_engine: Somn克隆引擎
- claws: Claw智能体实现
"""

from ._sage_proxy_factory import (
    SageProxyFactory,
    SageProxyConfig,
    get_sage_proxy_factory
)
from ._somn_clone_engine import (
    SomnCloneEngine,
    CloneConfig,
    get_clone_engine
)

__all__ = [
    "SageProxyFactory",
    "SageProxyConfig",
    "get_sage_proxy_factory",
    "SomnCloneEngine",
    "CloneConfig",
    "get_clone_engine",
]

__version__ = "6.2.0"
