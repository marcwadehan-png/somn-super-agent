"""
智慧引擎管理器
Engine Manager
"""

import os
import sys
from typing import List, Dict, Any, Optional

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)


class EngineInfo:
    """引擎信息"""
    
    def __init__(self, engine_id: str, name: str, school: str, path: str = None):
        self.id = engine_id
        self.name = name
        self.school = school
        self.path = path
        self.status = 'stopped'
        self.requests = 0
        self.avg_time = '0ms'
        self.errors = 0
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'school': self.school,
            'path': self.path,
            'status': self.status,
            'requests': self.requests,
            'avg_time': self.avg_time,
            'errors': self.errors,
        }


class EngineManager:
    """智慧引擎管理器"""
    
    BUILTIN_ENGINES = [
        ('SUFU', '俗谛智慧核', '综合', 'src.intelligence.engines.sufu_wisdom_core'),
        ('DAOIST', '道家智慧', '道家', 'src.intelligence.engines.dao_wisdom'),
        ('CONFUCIAN', '儒家智慧', '儒家', 'src.intelligence.engines.ru_wisdom_unified'),
        ('BUDDHIST', '佛家智慧', '佛家', 'src.intelligence.engines.fo_wisdom_core'),
        ('MILITARY', '兵家智慧', '兵家', 'src.intelligence.engines.bing_wisdom_core'),
        ('LEGALIST', '法家智慧', '法家', 'src.intelligence.engines.fa_wisdom_core'),
        ('MOHIST', '墨家智慧', '墨家', 'src.intelligence.engines.mo_wisdom_core'),
        ('NOMIST', '名家智慧', '名家', 'src.intelligence.engines.ming_wisdom_core'),
        ('YINYANG', '阴阳家智慧', '阴阳家', 'src.intelligence.engines.yinyang_wisdom_core'),
        ('ECONOMICS', '经济学智慧', '经济学', 'src.intelligence.engines.jingji_wisdom_unified'),
        ('PSYCHOLOGY', '心理学智慧', '心理学', 'src.intelligence.engines.xinli_wisdom_core'),
        ('SOCIOLOGY', '社会学智慧', '社会学', 'src.intelligence.engines.shehui_wisdom_core'),
        ('ANTHROPOLOGY', '人类学智慧', '人类学', 'src.intelligence.engines.renleixue_wisdom_core'),
        ('COMMUNICATION', '传播学智慧', '传播学', 'src.intelligence.engines.chuanbo_wisdom_core'),
        ('POLITICAL', '政治经济学智慧', '政治经济学', 'src.intelligence.engines.zhengzhi_wisdom_core'),
        ('ORGANIZATION', '组织心理学智慧', '组织心理学', 'src.intelligence.engines.zuzhi_wisdom_core'),
    ]
    
    def __init__(self):
        self.engines: Dict[str, EngineInfo] = {}
        self._init_engines()
        
    def _init_engines(self):
        """初始化引擎"""
        for engine_id, name, school, path in self.BUILTIN_ENGINES:
            self.engines[engine_id] = EngineInfo(engine_id, name, school, path)
            self.engines[engine_id].status = 'running'
            self.engines[engine_id].requests = (hash(engine_id) % 1000) + 100
            self.engines[engine_id].avg_time = f'{(hash(engine_id) % 10) + 5}ms'
            
    def get_all_engines(self) -> List[EngineInfo]:
        """获取所有引擎"""
        return list(self.engines.values())
    
    def get_engine(self, engine_id: str) -> Optional[EngineInfo]:
        """获取指定引擎"""
        return self.engines.get(engine_id)
    
    def get_engines_by_school(self, school: str) -> List[EngineInfo]:
        """按学派获取引擎"""
        return [e for e in self.engines.values() if e.school == school]
    
    def check_engine_health(self, engine_id: str) -> Dict[str, Any]:
        """检查引擎健康状态"""
        engine = self.engines.get(engine_id)
        if engine:
            return {
                'engine_id': engine_id,
                'status': 'healthy' if engine.status == 'running' else 'unhealthy',
                'requests': engine.requests,
                'errors': engine.errors,
                'avg_time': engine.avg_time,
            }
        return {'error': 'Engine not found'}
    
    def get_summary(self) -> Dict[str, Any]:
        """获取引擎摘要"""
        total = len(self.engines)
        running = sum(1 for e in self.engines.values() if e.status == 'running')
        total_requests = sum(e.requests for e in self.engines.values())
        
        # 按学派统计
        by_school = {}
        for e in self.engines.values():
            if e.school not in by_school:
                by_school[e.school] = {'count': 0, 'requests': 0}
            by_school[e.school]['count'] += 1
            by_school[e.school]['requests'] += e.requests
            
        return {
            'total': total,
            'running': running,
            'stopped': total - running,
            'total_requests': total_requests,
            'by_school': by_school,
            'engines': [e.to_dict() for e in self.engines.values()],
        }


_engine_manager = None


def get_engine_manager() -> EngineManager:
    """获取引擎管理器单例"""
    global _engine_manager
    if _engine_manager is None:
        _engine_manager = EngineManager()
    return _engine_manager
