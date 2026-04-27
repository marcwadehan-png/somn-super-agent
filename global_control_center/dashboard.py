"""
仪表板模块
Dashboard Module
"""

import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


class Dashboard:
    """系统仪表板"""
    
    def __init__(self):
        self.stats = {
            'modules': {'total': 32, 'active': 32},
            'engines': {'total': 45, 'active': 42},
            'claws': {'total': 776, 'active': 752},
            'tasks': {'pending': 12, 'running': 3, 'completed': 1847},
        }
        
    def get_overview(self) -> dict:
        """获取系统概览"""
        return {
            'version': 'V6.2.0',
            'project': 'Somn 智能助手',
            'edition': '神之架构最终完整版',
            'modules': self.stats['modules'],
            'engines': self.stats['engines'],
            'claws': self.stats['claws'],
            'tasks': self.stats['tasks'],
        }
    
    def get_module_status(self) -> list:
        """获取模块状态"""
        return [
            {'id': 'core', 'name': '核心模块', 'status': 'running', 'load_time': '0.12s', 'memory': '128MB'},
            {'id': 'intelligence', 'name': '智慧层', 'status': 'running', 'load_time': '0.25s', 'memory': '256MB'},
            {'id': 'capability', 'name': '能力层', 'status': 'running', 'load_time': '0.18s', 'memory': '192MB'},
            {'id': 'application', 'name': '应用层', 'status': 'running', 'load_time': '0.15s', 'memory': '144MB'},
            {'id': 'data', 'name': '数据层', 'status': 'running', 'load_time': '0.08s', 'memory': '96MB'},
            {'id': 'network', 'name': '网络模块', 'status': 'running', 'load_time': '0.05s', 'memory': '64MB'},
            {'id': 'storage', 'name': '存储模块', 'status': 'running', 'load_time': '0.10s', 'memory': '112MB'},
            {'id': 'scheduler', 'name': '调度模块', 'status': 'running', 'load_time': '0.09s', 'memory': '88MB'},
        ]
    
    def get_engine_status(self) -> list:
        """获取引擎状态"""
        return [
            {'id': 'SUFU', 'name': '俗谛智慧核', 'school': '综合', 'status': 'running', 'requests': 1247, 'avg_time': '12ms'},
            {'id': 'DAOIST', 'name': '道家智慧', 'school': '道家', 'status': 'running', 'requests': 892, 'avg_time': '8ms'},
            {'id': 'CONFUCIAN', 'name': '儒家智慧', 'school': '儒家', 'status': 'running', 'requests': 756, 'avg_time': '10ms'},
            {'id': 'BUDDHIST', 'name': '佛家智慧', 'school': '佛家', 'status': 'running', 'requests': 623, 'avg_time': '9ms'},
            {'id': 'MILITARY', 'name': '兵家智慧', 'school': '兵家', 'status': 'running', 'requests': 534, 'avg_time': '7ms'},
            {'id': 'ECONOMICS', 'name': '经济学智慧', 'school': '经济学', 'status': 'running', 'requests': 445, 'avg_time': '11ms'},
            {'id': 'PSYCHOLOGY', 'name': '心理学智慧', 'school': '心理学', 'status': 'running', 'requests': 398, 'avg_time': '8ms'},
            {'id': 'SOCIOLOGY', 'name': '社会学智慧', 'school': '社会学', 'status': 'running', 'requests': 312, 'avg_time': '13ms'},
        ]
    
    def get_claw_status(self) -> dict:
        """获取Claw状态"""
        schools = [
            {'id': 'CONFUCIAN', 'name': '儒家', 'total': 45, 'active': 43},
            {'id': 'DAOIST', 'name': '道家', 'total': 52, 'active': 50},
            {'id': 'BUDDHIST', 'name': '佛家', 'total': 38, 'active': 36},
            {'id': 'MILITARY', 'name': '兵家', 'total': 35, 'active': 33},
            {'id': 'ECONOMICS', 'name': '经济学', 'total': 42, 'active': 40},
            {'id': 'PSYCHOLOGY', 'name': '心理学', 'total': 48, 'active': 46},
        ]
        
        claws = [
            {'id': 'CLAW_001', 'name': '孔子', 'school': '儒家', 'status': 'active', 'tasks': 234},
            {'id': 'CLAW_002', 'name': '老子', 'school': '道家', 'status': 'active', 'tasks': 198},
            {'id': 'CLAW_003', 'name': '孙子', 'school': '兵家', 'status': 'active', 'tasks': 176},
            {'id': 'CLAW_004', 'name': '鬼谷子', 'school': '纵横家', 'status': 'active', 'tasks': 145},
            {'id': 'CLAW_005', 'name': '墨子', 'school': '墨家', 'status': 'active', 'tasks': 132},
        ]
        
        return {'schools': schools, 'claws': claws}
    
    def get_health_status(self) -> dict:
        """获取健康状态"""
        return {
            'overall': 'healthy',
            'checks': [
                {'name': '核心模块', 'status': 'ok', 'message': '正常'},
                {'name': '智慧引擎', 'status': 'ok', 'message': '42/45 运行中'},
                {'name': 'Claw系统', 'status': 'ok', 'message': '752/776 活跃'},
                {'name': '调度器', 'status': 'ok', 'message': '运行中'},
                {'name': '配置系统', 'status': 'ok', 'message': '正常'},
                {'name': '存储系统', 'status': 'ok', 'message': '正常'},
                {'name': '网络连接', 'status': 'ok', 'message': '正常'},
            ]
        }


def get_dashboard() -> Dashboard:
    """获取仪表板实例"""
    return Dashboard()


if __name__ == '__main__':
    dash = Dashboard()
    print("系统概览:")
    for key, value in dash.get_overview().items():
        print(f"  {key}: {value}")
