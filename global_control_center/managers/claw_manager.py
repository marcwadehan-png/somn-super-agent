"""
Claw代理管理器
Claw Manager
"""

import os
import sys
from typing import List, Dict, Any, Optional

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)


class ClawInfo:
    """Claw代理信息"""
    
    def __init__(self, claw_id: str, name: str, school: str, archetype: str = None):
        self.id = claw_id
        self.name = name
        self.school = school
        self.archetype = archetype or school
        self.status = 'inactive'
        self.tasks = 0
        self.created_at = None
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'school': self.school,
            'archetype': self.archetype,
            'status': self.status,
            'tasks': self.tasks,
            'created_at': self.created_at,
        }


class ClawManager:
    """Claw代理管理器"""
    
    WISDOM_SCHOOLS = [
        ('CONFUCIAN', '儒家', 45),
        ('DAOIST', '道家', 52),
        ('BUDDHIST', '佛家', 38),
        ('MILITARY', '兵家', 35),
        ('LEGALIST', '法家', 28),
        ('MOHIST', '墨家', 25),
        ('NOMIST', '名家', 18),
        ('YINYANG', '阴阳家', 22),
        ('ECONOMICS', '经济学', 42),
        ('PSYCHOLOGY', '心理学', 48),
        ('SOCIOLOGY', '社会学', 30),
        ('LAW', '法学', 28),
        ('ANTHROPOLOGY', '人类学', 24),
        ('COMMUNICATION', '传播学', 26),
        ('POLITICAL', '政治经济学', 20),
        ('ORGANIZATION', '组织心理学', 22),
    ]
    
    def __init__(self):
        self.claws: Dict[str, ClawInfo] = {}
        self.schools: Dict[str, Dict[str, Any]] = {}
        self._init_schools()
        self._init_claws()
        
    def _init_schools(self):
        """初始化学派"""
        for school_id, name, count in self.WISDOM_SCHOOLS:
            self.schools[school_id] = {
                'id': school_id,
                'name': name,
                'total': count,
                'active': count,  # 假设全部活跃
            }
            
    def _init_claws(self):
        """初始化Claws"""
        claw_id = 1
        archetypes = {
            'CONFUCIAN': ['孔子', '孟子', '荀子', '朱熹', '王阳明'],
            'DAOIST': ['老子', '庄子', '列子', '杨朱'],
            'BUDDHIST': ['释迦牟尼', '慧能', '玄奘', '道宣'],
            'MILITARY': ['孙子', '吴子', '孙膑', '尉缭子'],
            'ECONOMICS': ['亚当斯密', '凯恩斯', '马克思', '哈耶克'],
            'PSYCHOLOGY': ['弗洛伊德', '荣格', '马斯洛', '华生'],
            'SOCIOLOGY': ['孔德', '韦伯', '涂尔干', '费孝通'],
        }
        
        for school_id, name, count in self.WISDOM_SCHOOLS:
            school_claws = archetypes.get(school_id, [name])
            for i in range(min(count, len(school_claws))):
                claw = ClawInfo(
                    f'CLAW_{claw_id:04d}',
                    school_claws[i],
                    name
                )
                claw.status = 'active'
                claw.tasks = (hash(claw.id) % 300) + 50
                self.claws[claw.id] = claw
                claw_id += 1
                
    def get_all_claws(self) -> List[ClawInfo]:
        """获取所有Claws"""
        return list(self.claws.values())
    
    def get_claw(self, claw_id: str) -> Optional[ClawInfo]:
        """获取指定Claw"""
        return self.claws.get(claw_id)
    
    def get_claws_by_school(self, school: str) -> List[ClawInfo]:
        """按学派获取Claws"""
        return [c for c in self.claws.values() if c.school == school]
    
    def create_claw(self, name: str, school: str, archetype: str = None) -> Dict[str, Any]:
        """创建Claw"""
        claw_id = f'CLAW_{len(self.claws) + 1:04d}'
        claw = ClawInfo(claw_id, name, school, archetype)
        claw.status = 'active'
        self.claws[claw_id] = claw
        
        if school in self.schools:
            self.schools[school]['total'] += 1
            self.schools[school]['active'] += 1
            
        return {'status': 'ok', 'claw': claw.to_dict()}
    
    def delete_claw(self, claw_id: str) -> Dict[str, Any]:
        """删除Claw"""
        claw = self.claws.get(claw_id)
        if claw:
            del self.claws[claw_id]
            if claw.school in self.schools:
                self.schools[claw.school]['total'] -= 1
                self.schools[claw.school]['active'] -= 1
            return {'status': 'ok', 'message': f'Claw {claw_id} deleted'}
        return {'status': 'error', 'message': f'Claw {claw_id} not found'}
    
    def get_summary(self) -> Dict[str, Any]:
        """获取Claw摘要"""
        total = len(self.claws)
        active = sum(1 for c in self.claws.values() if c.status == 'active')
        total_tasks = sum(c.tasks for c in self.claws.values())
        
        return {
            'total': total,
            'active': active,
            'inactive': total - active,
            'total_tasks': total_tasks,
            'schools': list(self.schools.values()),
            'claws': [c.to_dict() for c in self.claws.values()],
        }


_claw_manager = None


def get_claw_manager() -> ClawManager:
    """获取Claw管理器单例"""
    global _claw_manager
    if _claw_manager is None:
        _claw_manager = ClawManager()
    return _claw_manager
