# -*- coding: utf-8 -*-
"""
Sage代理工厂模块
用于创建和管理Sage(贤者)代理实例
贤者工程第三层: Cloning (克隆实现)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class SageProxyConfig:
    """Sage代理配置"""
    sage_code: str
    wisdom_school: str
    problem_types: List[str]
    enabled: bool = True


class SageProxyFactory:
    """Sage代理工厂类"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._proxies: Dict[str, Any] = {}
        self._factories: Dict[str, Any] = {}
    
    def register_sage(self, config: SageProxyConfig) -> bool:
        """注册贤者代理"""
        if not config.enabled:
            return False
        self._proxies[config.sage_code] = config
        return True
    
    def get_sage(self, sage_code: str) -> Optional[SageProxyConfig]:
        """获取贤者代理"""
        return self._proxies.get(sage_code)
    
    def list_sages(self, wisdom_school: Optional[str] = None) -> List[SageProxyConfig]:
        """列出贤者"""
        if wisdom_school:
            return [s for s in self._proxies.values() 
                    if s.wisdom_school == wisdom_school]
        return list(self._proxies.values())
    
    def create_proxy(self, sage_code: str) -> Optional[Any]:
        """创建贤者代理实例"""
        config = self.get_sage(sage_code)
        if not config:
            return None
        return {
            "sage_code": config.sage_code,
            "wisdom_school": config.wisdom_school,
            "problem_types": config.problem_types
        }


def get_sage_proxy_factory() -> SageProxyFactory:
    """获取Sage代理工厂单例"""
    return SageProxyFactory()


__all__ = ["SageProxyFactory", "SageProxyConfig", "get_sage_proxy_factory"]
