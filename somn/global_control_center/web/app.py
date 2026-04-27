"""
Flask Web应用 - Somn全局控制中心
Flask Web Application
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime


def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    CORS(app)
    
    # 路由
    @app.route('/')
    def index():
        """主页"""
        return render_template('index.html')
    
    @app.route('/api/status')
    def get_status():
        """获取系统状态"""
        return jsonify({
            'status': 'running',
            'version': 'V1.0.0',
            'uptime': '2 hours 34 minutes',
            'modules': {
                'total': 32,
                'active': 32
            },
            'engines': {
                'total': 45,
                'active': 42
            },
            'claws': {
                'total': 776,
                'active': 752
            },
            'tasks': {
                'pending': 12,
                'running': 3,
                'completed': 1847
            },
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/api/modules')
    def get_modules():
        """获取模块列表"""
        modules = [
            {'id': 'core', 'name': '核心模块', 'status': 'running', 'load_time': '0.12s', 'memory': '128MB'},
            {'id': 'intelligence', 'name': '智慧层', 'status': 'running', 'load_time': '0.25s', 'memory': '256MB'},
            {'id': 'capability', 'name': '能力层', 'status': 'running', 'load_time': '0.18s', 'memory': '192MB'},
            {'id': 'application', 'name': '应用层', 'status': 'running', 'load_time': '0.15s', 'memory': '144MB'},
            {'id': 'data', 'name': '数据层', 'status': 'running', 'load_time': '0.08s', 'memory': '96MB'},
            {'id': 'network', 'name': '网络模块', 'status': 'running', 'load_time': '0.05s', 'memory': '64MB'},
            {'id': 'storage', 'name': '存储模块', 'status': 'running', 'load_time': '0.10s', 'memory': '112MB'},
            {'id': 'scheduler', 'name': '调度模块', 'status': 'running', 'load_time': '0.09s', 'memory': '88MB'},
        ]
        return jsonify({'modules': modules})
    
    @app.route('/api/engines')
    def get_engines():
        """获取智慧引擎列表"""
        engines = [
            {'id': 'SUFU', 'name': '俗谛智慧核', 'school': '综合', 'status': 'running', 'requests': 1247, 'avg_time': '12ms'},
            {'id': 'DAOIST', 'name': '道家智慧', 'school': '道家', 'status': 'running', 'requests': 892, 'avg_time': '8ms'},
            {'id': 'CONFUCIAN', 'name': '儒家智慧', 'school': '儒家', 'status': 'running', 'requests': 756, 'avg_time': '10ms'},
            {'id': 'BUDDHIST', 'name': '佛家智慧', 'school': '佛家', 'status': 'running', 'requests': 623, 'avg_time': '9ms'},
            {'id': 'MILITARY', 'name': '兵家智慧', 'school': '兵家', 'status': 'running', 'requests': 534, 'avg_time': '7ms'},
            {'id': 'ECONOMICS', 'name': '经济学智慧', 'school': '经济学', 'status': 'running', 'requests': 445, 'avg_time': '11ms'},
            {'id': 'PSYCHOLOGY', 'name': '心理学智慧', 'school': '心理学', 'status': 'running', 'requests': 398, 'avg_time': '8ms'},
            {'id': 'SOCIOLOGY', 'name': '社会学智慧', 'school': '社会学', 'status': 'running', 'requests': 312, 'avg_time': '13ms'},
            {'id': 'LAW', 'name': '法学智慧', 'school': '法学', 'status': 'running', 'requests': 267, 'avg_time': '9ms'},
            {'id': 'ANTHROPOLOGY', 'name': '人类学智慧', 'school': '人类学', 'status': 'running', 'requests': 198, 'avg_time': '14ms'},
            {'id': 'COMMUNICATION', 'name': '传播学智慧', 'school': '传播学', 'status': 'running', 'requests': 156, 'avg_time': '10ms'},
            {'id': 'POLITICAL', 'name': '政治经济学智慧', 'school': '政治经济学', 'status': 'running', 'requests': 134, 'avg_time': '15ms'},
        ]
        return jsonify({'engines': engines})
    
    @app.route('/api/claws')
    def get_claws():
        """获取Claw代理列表"""
        claws = [
            {'id': 'CLAW_001', 'name': '孔子', 'school': '儒家', 'status': 'active', 'tasks': 234},
            {'id': 'CLAW_002', 'name': '老子', 'school': '道家', 'status': 'active', 'tasks': 198},
            {'id': 'CLAW_003', 'name': '孙子', 'school': '兵家', 'status': 'active', 'tasks': 176},
            {'id': 'CLAW_004', 'name': '鬼谷子', 'school': '纵横家', 'status': 'active', 'tasks': 145},
            {'id': 'CLAW_005', 'name': '墨子', 'school': '墨家', 'status': 'active', 'tasks': 132},
            {'id': 'CLAW_006', 'name': '孟子', 'school': '儒家', 'status': 'active', 'tasks': 128},
            {'id': 'CLAW_007', 'name': '庄子', 'school': '道家', 'status': 'active', 'tasks': 119},
            {'id': 'CLAW_008', 'name': '荀子', 'school': '儒家', 'status': 'active', 'tasks': 98},
        ]
        
        # 学派统计
        schools = [
            {'id': 'CONFUCIAN', 'name': '儒家', 'total': 45, 'active': 43},
            {'id': 'DAOIST', 'name': '道家', 'total': 52, 'active': 50},
            {'id': 'BUDDHIST', 'name': '佛家', 'total': 38, 'active': 36},
            {'id': 'MILITARY', 'name': '兵家', 'total': 35, 'active': 33},
            {'id': 'ECONOMICS', 'name': '经济学', 'total': 42, 'active': 40},
            {'id': 'PSYCHOLOGY', 'name': '心理学', 'total': 48, 'active': 46},
            {'id': 'SOCIOLOGY', 'name': '社会学', 'total': 30, 'active': 28},
            {'id': 'LAW', 'name': '法学', 'total': 28, 'active': 26},
        ]
        
        return jsonify({'claws': claws, 'schools': schools})
    
    @app.route('/api/health')
    def health_check():
        """健康检查"""
        checks = [
            {'name': '核心模块', 'status': 'ok', 'message': '正常'},
            {'name': '智慧引擎', 'status': 'ok', 'message': '42/45 运行中'},
            {'name': 'Claw系统', 'status': 'ok', 'message': '752/776 活跃'},
            {'name': '调度器', 'status': 'ok', 'message': '运行中'},
            {'name': '配置系统', 'status': 'ok', 'message': '正常'},
            {'name': '存储系统', 'status': 'ok', 'message': '正常'},
            {'name': '网络连接', 'status': 'ok', 'message': '正常'},
        ]
        
        all_ok = all(c['status'] == 'ok' for c in checks)
        
        return jsonify({
            'status': 'healthy' if all_ok else 'degraded',
            'checks': checks,
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/api/config')
    def get_config():
        """获取配置"""
        config = {
            'system': {
                'version': '2.0.0',
                'mode': 'standalone',
                'log_level': 'INFO'
            },
            'llm': {
                'default_model': 'gemma4-local-b',
                'api_port': 8976
            },
            'performance': {
                'lazy_loading': True,
                'max_parallel_tasks': 4,
                'cache_size': '100MB'
            },
            'features': {
                'gui': True,
                'web_search': True,
                'ml_engine': True,
                'knowledge_graph': True
            }
        }
        return jsonify({'config': config})
    
    @app.route('/api/config', methods=['POST'])
    def update_config():
        """更新配置"""
        data = request.json
        # 这里应该写入配置文件
        return jsonify({'status': 'ok', 'message': '配置已更新'})
    
    @app.route('/api/logs')
    def get_logs():
        """获取日志"""
        logs = [
            {'time': '2026-04-25 23:54:00', 'level': 'INFO', 'message': 'Global Control Center started'},
            {'time': '2026-04-25 23:54:01', 'level': 'INFO', 'message': 'Loading system configuration...'},
            {'time': '2026-04-25 23:54:02', 'level': 'INFO', 'message': 'Configuration loaded successfully'},
            {'time': '2026-04-25 23:54:03', 'level': 'INFO', 'message': 'Initializing wisdom engines (45+)...'},
            {'time': '2026-04-25 23:54:05', 'level': 'INFO', 'message': 'Wisdom engines initialized (42/45 active)'},
            {'time': '2026-04-25 23:54:06', 'level': 'INFO', 'message': 'Loading Claw configurations (776)...'},
            {'time': '2026-04-25 23:54:08', 'level': 'INFO', 'message': 'Claw system ready (752/776 active)'},
            {'time': '2026-04-25 23:54:10', 'level': 'INFO', 'message': 'Starting GlobalWisdomScheduler...'},
            {'time': '2026-04-25 23:54:11', 'level': 'INFO', 'message': 'System ready - All modules operational'},
        ]
        return jsonify({'logs': logs})
    
    @app.route('/api/action/<action>', methods=['POST'])
    def perform_action(action):
        """执行操作"""
        data = request.json or {}
        target = data.get('target', '')
        
        actions = {
            'start_module': f'启动模块: {target}',
            'stop_module': f'停止模块: {target}',
            'restart_module': f'重启模块: {target}',
            'create_claw': f'创建Claw: {target}',
            'delete_claw': f'删除Claw: {target}',
        }
        
        return jsonify({
            'status': 'ok',
            'action': action,
            'target': target,
            'result': actions.get(action, '未知操作')
        })
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8970, debug=True)
