#!/usr/bin/env python3
"""
Somn — 汇千古之智，向未知而生
主入口文件（Web 模式，FastAPI 后端 + 浏览器前端）
"""

import sys
import os
from pathlib import Path

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

import uvicorn


def main():
    """主函数 — 启动 FastAPI Web 服务"""
    from api.server import create_app

    app = create_app()

    print("=" * 50)
    print("  Somn — 汇千古之智，向未知而生")
    print("  Web 服务启动中...")
    print("  访问 http://localhost:8000")
    print("=" * 50)

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
