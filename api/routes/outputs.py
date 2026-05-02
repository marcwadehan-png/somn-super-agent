"""
Somn API Server - 作品库路由
浏览/管理 outputs 目录下生成的作品文件
"""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import Query
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)

# 输出目录根路径
OUTPUTS_DIR = Path(__file__).resolve().parent.parent.parent / "outputs"

# 文件类型图标映射
FILE_ICONS = {
    ".pdf": "📄", ".docx": "📝", ".doc": "📝",
    ".pptx": "📊", ".ppt": "📊", ".xlsx": "📈", ".xls": "📈",
    ".csv": "📋", ".txt": "📃", ".md": "📑",
    ".html": "🌐", ".json": "🔧", ".yaml": "⚙️", ".yml": "⚙️",
    ".png": "🖼️", ".jpg": "🖼️", ".jpeg": "🖼️", ".gif": "🖼️", ".svg": "🖼️",
    ".mp4": "🎬", ".mp3": "🎵", ".zip": "📦",
}

# 文件类型颜色映射
FILE_COLORS = {
    ".pdf": "#FF3B30", ".docx": "#2B579A", ".doc": "#2B579A",
    ".pptx": "#D04423", ".ppt": "#D04423", ".xlsx": "#217346", ".xls": "#217346",
    ".csv": "#34C759", ".txt": "#8A8A8A", ".md": "#4A90D9",
    ".html": "#FF9500", ".json": "#6B6B6B",
    ".png": "#AF52DE", ".jpg": "#AF52DE",
}


def register_outputs_routes(app, app_state):
    """注册作品库相关路由"""

    @app.get("/api/v1/outputs", tags=["作品库"])
    async def list_outputs(
        path: Optional[str] = Query(default=None, description="子目录路径"),
    ):
        """获取作品库文件列表"""
        try:
            target_dir = OUTPUTS_DIR
            if path:
                target_dir = OUTPUTS_DIR / path
                # 安全检查：防止路径穿越
                target_dir = target_dir.resolve()
                if not str(target_dir).startswith(str(OUTPUTS_DIR.resolve())):
                    return _error("非法路径")

            if not target_dir.exists():
                return _ok("目录不存在", data={"items": [], "total": 0, "current_path": path or "", "base_path": ""})

            items = []
            dirs = []
            for entry in sorted(target_dir.iterdir()):
                # 跳过隐藏文件和 __pycache__
                if entry.name.startswith('.') or entry.name == '__pycache__':
                    continue

                stat = entry.stat()
                ext = entry.suffix.lower()
                rel_path = str(entry.relative_to(OUTPUTS_DIR))

                if entry.is_dir():
                    # 统计子目录文件数
                    try:
                        file_count = sum(1 for _ in entry.rglob('*') if _.is_file())
                    except Exception:
                        file_count = 0
                    dirs.append({
                        "name": entry.name,
                        "type": "directory",
                        "path": rel_path,
                        "size": 0,
                        "file_count": file_count,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "icon": "📁",
                    })
                else:
                    items.append({
                        "name": entry.name,
                        "type": "file",
                        "path": rel_path,
                        "ext": ext,
                        "size": stat.st_size,
                        "size_display": _format_size(stat.st_size),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "icon": FILE_ICONS.get(ext, "📎"),
                        "color": FILE_COLORS.get(ext, "var(--silver)"),
                    })

            # 目录排在前面
            all_items = dirs + items
            current_path = path or ""
            base_path = ""

            # 面包屑导航
            breadcrumbs = []
            if path:
                parts = path.replace('\\', '/').split('/')
                for i, part in enumerate(parts):
                    breadcrumbs.append({
                        "name": part,
                        "path": '/'.join(parts[:i + 1]),
                    })

            return _ok("作品列表", data={
                "items": all_items,
                "total": len(all_items),
                "directories": len(dirs),
                "files": len(items),
                "current_path": current_path,
                "breadcrumbs": breadcrumbs,
            })
        except Exception as e:
            logger.error(f"获取作品列表失败: {e}", exc_info=True)
            return _error("获取作品列表失败")

    @app.get("/api/v1/outputs/stats", tags=["作品库"])
    async def outputs_stats():
        """获取作品库统计信息"""
        try:
            total_files = 0
            total_size = 0
            type_counts = {}
            directory_count = 0

            if OUTPUTS_DIR.exists():
                for entry in OUTPUTS_DIR.rglob('*'):
                    if entry.is_file() and not entry.name.startswith('.'):
                        total_files += 1
                        total_size += entry.stat().st_size
                        ext = entry.suffix.lower() or '.other'
                        type_counts[ext] = type_counts.get(ext, 0) + 1
                    elif entry.is_dir() and not entry.name.startswith('.'):
                        directory_count += 1

            # 按数量排序
            sorted_types = sorted(type_counts.items(), key=lambda x: -x[1])

            return _ok("作品统计", data={
                "total_files": total_files,
                "total_size": total_size,
                "total_size_display": _format_size(total_size),
                "directory_count": directory_count,
                "type_distribution": [
                    {"type": ext, "count": count, "icon": FILE_ICONS.get(ext, "📎")}
                    for ext, count in sorted_types[:10]
                ],
            })
        except Exception as e:
            logger.error(f"获取作品统计失败: {e}", exc_info=True)
            return _error("获取作品统计失败")

    @app.get("/api/v1/outputs/download/{file_path:path}", tags=["作品库"])
    async def download_output(file_path: str):
        """下载作品文件"""
        try:
            target = OUTPUTS_DIR / file_path
            target = target.resolve()
            # 安全检查
            if not str(target).startswith(str(OUTPUTS_DIR.resolve())):
                return _error("非法路径")
            if not target.exists() or not target.is_file():
                return _error("文件不存在")

            return FileResponse(
                path=str(target),
                filename=target.name,
                media_type="application/octet-stream",
            )
        except Exception as e:
            logger.error(f"下载文件失败: {e}", exc_info=True)
            return _error("下载文件失败")

    @app.delete("/api/v1/outputs/{file_path:path}", tags=["作品库"])
    async def delete_output(file_path: str):
        """删除作品文件"""
        try:
            target = OUTPUTS_DIR / file_path
            target = target.resolve()
            # 安全检查
            if not str(target).startswith(str(OUTPUTS_DIR.resolve())):
                return _error("非法路径")
            if not target.exists():
                return _error("文件不存在")

            if target.is_dir():
                import shutil
                shutil.rmtree(target)
            else:
                target.unlink()

            return _ok("删除成功", data={"deleted": file_path})
        except Exception as e:
            logger.error(f"删除文件失败: {e}", exc_info=True)
            return _error("删除文件失败")


def _format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def _ok(message: str, data=None) -> dict:
    return {
        "success": True,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "data": data,
    }


def _error(error: str, code: str = "ERROR") -> dict:
    return {
        "success": False,
        "message": error,
        "error_code": code,
        "timestamp": datetime.now().isoformat(),
        "data": None,
    }
