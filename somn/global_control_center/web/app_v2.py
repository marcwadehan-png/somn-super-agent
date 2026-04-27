"""
Flask Web应用 - Somn全局控制中心
集成真实后端API
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime
import requests
from functools import wraps
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 后端API配置
BACKEND_URL = "http://127.0.0.1:8964"
API_TIMEOUT = 5


def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    CORS(app)

    def get_backend_json(endpoint: str, default=None):
        """从后端获取JSON数据"""
        try:
            resp = requests.get(f"{BACKEND_URL}{endpoint}", timeout=API_TIMEOUT)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logger.debug(f"Backend API error for {endpoint}: {e}")
        return default

    def get_backend_status() -> str:
        """获取后端状态"""
        try:
            sock = __import__('socket')
            s = sock.socket()
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', 8964))
            s.close()
            return "online" if result == 0 else "offline"
        except (ConnectionRefusedError, OSError, TimeoutError):
            return "offline"

    # ============================================================
    # 路由
    # ============================================================

    @app.route('/')
    def index():
        """主页"""
        return render_template('index.html')

    @app.route('/api/status')
    def get_status():
        """获取系统状态 - 集成真实API"""
        backend_status = get_backend_status()

        if backend_status == "online":
            # 尝试获取真实数据
            data = get_backend_json("/api/v1/status")
            health = get_backend_json("/api/v1/health")

            if data and data.get('success'):
                info = data['data']
                uptime = info.get('uptime_seconds', 0)
                hours = uptime // 3600
                minutes = (uptime % 3600) // 60

                return jsonify({
                    'status': 'healthy' if backend_status == "online" else 'degraded',
                    'backend': backend_status,
                    'version': info.get('version', 'unknown'),
                    'uptime': f"{hours}h {minutes}m",
                    'uptime_seconds': uptime,
                    'environment': info.get('environment', 'unknown'),
                    'modules': {
                        'total': info.get('loaded_modules_count', 0),
                        'loaded': len(info.get('loaded_modules', []))
                    },
                    'engines': {
                        'total': info.get('engine_count', 0),
                        'wisdom_schools': info.get('wisdom_schools_count', 0)
                    },
                    'claws': {
                        'total': info.get('claw_count', 0)
                    },
                    'memory': {
                        'mb': info.get('memory_usage_mb', 0)
                    },
                    'health': health.get('data', {}) if health else {},
                    'timestamp': datetime.now().isoformat()
                })

        # 后端离线时的降级响应
        return jsonify({
            'status': 'offline',
            'backend': 'offline',
            'version': 'v1.0',
            'uptime': '0h 0m',
            'uptime_seconds': 0,
            'environment': 'unknown',
            'modules': {'total': 0, 'loaded': 0},
            'engines': {'total': 0, 'wisdom_schools': 0},
            'claws': {'total': 0},
            'memory': {'mb': 0},
            'timestamp': datetime.now().isoformat()
        })

    @app.route('/api/modules')
    def get_modules():
        """获取模块列表"""
        data = get_backend_json("/api/v1/config")

        if data and data.get('success'):
            modules = data['data'].get('modules', [])
            return jsonify({
                'success': True,
                'modules': modules,
                'count': len(modules)
            })

        return jsonify({'success': False, 'modules': [], 'count': 0})

    @app.route('/api/logs')
    def get_logs():
        """获取最近日志"""
        return jsonify({
            'success': True,
            'logs': [
                {'time': datetime.now().isoformat(), 'level': 'INFO', 'msg': 'Web Dashboard connected'},
                {'time': datetime.now().isoformat(), 'level': 'INFO', 'msg': f'Backend: {get_backend_status()}'}
            ]
        })

    @app.route('/api/health')
    def get_health():
        """健康检查"""
        return jsonify({
            'status': 'healthy',
            'backend': get_backend_status(),
            'timestamp': datetime.now().isoformat()
        })

    return app


if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("Somn V1.0 全局控制中心 - Web Dashboard")
    print("=" * 60)
    print(f"Backend API: {BACKEND_URL}")
    print(f"Web Server:  http://127.0.0.1:8970")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8970, debug=False)
