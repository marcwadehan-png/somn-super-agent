"""
Web模块 - 基于Flask的Web控制台
Web Module for Browser Access
"""

import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def run_web_app(port: int = 8970):
    """运行Web应用"""
    try:
        from flask import Flask, render_template, jsonify, request
        from flask_cors import CORS
    except ImportError:
        print("[错误] Flask 未安装，请安装: pip install flask flask-cors")
        print("[提示] 或使用 CLI 模式: python main_console.py --mode cli")
        return
        
    from .app import create_app
    app = create_app()
    
    print(f"[Web控制台] 启动中...")
    print(f"[Web控制台] 访问地址: http://localhost:{port}")
    print(f"[Web控制台] 按 Ctrl+C 停止服务器")
    
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    run_web_app()
