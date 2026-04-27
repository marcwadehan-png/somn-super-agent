"""
配置管理器
Config Manager
"""

import os
import sys
from typing import Dict, Any, Optional

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)


class ConfigManager:
    """配置管理器"""
    
    DEFAULT_CONFIG = {
        'system': {
            'version': '2.0.0',
            'mode': 'standalone',
            'log_level': 'INFO',
            'debug': False,
        },
        'llm': {
            'default_model': 'gemma4-local-b',
            'api_host': 'localhost',
            'api_port': 8976,
            'timeout': 30,
            'max_retries': 3,
        },
        'performance': {
            'lazy_loading': True,
            'max_parallel_tasks': 4,
            'cache_size': '100MB',
            'thread_pool_size': 8,
        },
        'features': {
            'gui': True,
            'web_search': True,
            'ml_engine': True,
            'knowledge_graph': True,
            'wisdom_fusion': True,
        },
        'intelligence': {
            'wisdom_engine_count': 45,
            'claw_count': 776,
            'problem_types': 135,
            'execution_phases': 'A-G',
        },
    }
    
    def __init__(self):
        self.config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        self.modified = False
        
    def get(self, key: str = None) -> Any:
        """获取配置"""
        if key is None:
            return self.config
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return None
        return value
    
    def set(self, key: str, value: Any) -> Dict[str, Any]:
        """设置配置"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.modified = True
        return {'status': 'ok', 'key': key, 'value': value}
    
    def save(self, filepath: str = None) -> Dict[str, Any]:
        """保存配置"""
        import json
        if filepath is None:
            filepath = os.path.join(project_root, 'config', 'local_config.yaml')
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self.modified = False
            return {'status': 'ok', 'path': filepath}
        except Exception as e:
            print(f"[配置管理] 保存失败: {e}")
            return {'status': 'error', 'message': '保存配置失败'}
    
    def load(self, filepath: str = None) -> Dict[str, Any]:
        """加载配置"""
        import json
        if filepath is None:
            filepath = os.path.join(project_root, 'config', 'local_config.yaml')
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return {'status': 'ok', 'config': self.config}
        except Exception as e:
            print(f"[配置管理] 加载失败: {e}")
            return {'status': 'error', 'message': '加载配置失败'}
    
    def reset(self) -> Dict[str, Any]:
        """重置为默认配置"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.modified = False
        return {'status': 'ok', 'message': 'Config reset to default'}
    
    def get_summary(self) -> Dict[str, Any]:
        """获取配置摘要"""
        return {
            'modified': self.modified,
            'config': self.config,
        }


_config_manager = None


def get_config_manager() -> ConfigManager:
    """获取配置管理器单例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
