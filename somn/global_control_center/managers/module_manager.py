"""
模块管理器
Module Manager
"""

import os
import sys
from typing import List, Dict, Any, Optional
from datetime import datetime

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)


class ModuleInfo:
    """模块信息"""
    
    def __init__(self, module_id: str, name: str, path: str = None):
        self.id = module_id
        self.name = name
        self.path = path or f"src.{module_id}"
        self.status = 'stopped'
        self.load_time = None
        self.memory = '0MB'
        self.started_at = None
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path,
            'status': self.status,
            'load_time': self.load_time,
            'memory': self.memory,
            'started_at': self.started_at.isoformat() if self.started_at else None,
        }


class ModuleManager:
    """模块管理器 - 管理 Somn 项目所有模块"""
    
    BUILTIN_MODULES = [
        ('core', '核心模块', 'src'),
        ('intelligence', '智慧层', 'src.intelligence'),
        ('capability', '能力层', 'src.capability'),
        ('application', '应用层', 'src.application'),
        ('data', '数据层', 'src.data'),
        ('network', '网络模块', 'src.network'),
        ('storage', '存储模块', 'src.storage'),
        ('scheduler', '调度模块', 'src.intelligence.scheduler'),
        ('claws', 'Claw系统', 'src.intelligence.claws'),
        ('wisdom', '智慧引擎', 'src.intelligence.engines'),
        ('dispatcher', '分发器', 'src.intelligence.dispatcher'),
        ('config', '配置系统', 'config'),
    ]
    
    def __init__(self):
        self.modules: Dict[str, ModuleInfo] = {}
        self._init_modules()
        
    def _init_modules(self):
        """初始化模块"""
        for module_id, name, path in self.BUILTIN_MODULES:
            self.modules[module_id] = ModuleInfo(module_id, name, path)
            self.modules[module_id].status = 'running'
            self.modules[module_id].load_time = f'{len(self.modules) * 0.03:.2f}s'
            self.modules[module_id].memory = f'{64 + len(self.modules) * 16}MB'
            
    def get_all_modules(self) -> List[ModuleInfo]:
        """获取所有模块"""
        return list(self.modules.values())
    
    def get_module(self, module_id: str) -> Optional[ModuleInfo]:
        """获取指定模块"""
        return self.modules.get(module_id)
    
    def start_module(self, module_id: str) -> Dict[str, Any]:
        """启动模块"""
        module = self.modules.get(module_id)
        if module:
            if module.status == 'running':
                return {'status': 'error', 'message': f'Module {module_id} is already running'}
            module.status = 'running'
            module.started_at = datetime.now()
            return {'status': 'ok', 'message': f'Module {module_id} started', 'module': module.to_dict()}
        return {'status': 'error', 'message': f'Module {module_id} not found'}
    
    def stop_module(self, module_id: str) -> Dict[str, Any]:
        """停止模块"""
        module = self.modules.get(module_id)
        if module:
            if module.status == 'stopped':
                return {'status': 'error', 'message': f'Module {module_id} is already stopped'}
            module.status = 'stopped'
            module.started_at = None
            return {'status': 'ok', 'message': f'Module {module_id} stopped'}
        return {'status': 'error', 'message': f'Module {module_id} not found'}
    
    def restart_module(self, module_id: str) -> Dict[str, Any]:
        """重启模块"""
        result = self.stop_module(module_id)
        if result['status'] == 'ok':
            return self.start_module(module_id)
        return result
    
    def get_summary(self) -> Dict[str, Any]:
        """获取模块摘要"""
        total = len(self.modules)
        running = sum(1 for m in self.modules.values() if m.status == 'running')
        return {
            'total': total,
            'running': running,
            'stopped': total - running,
            'modules': [m.to_dict() for m in self.modules.values()]
        }


_module_manager = None


def get_module_manager() -> ModuleManager:
    """获取模块管理器单例"""
    global _module_manager
    if _module_manager is None:
        _module_manager = ModuleManager()
    return _module_manager
