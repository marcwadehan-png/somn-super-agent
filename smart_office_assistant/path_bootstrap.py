"""项目路径引导工具。

让脚本在任意工作目录下启动时都能自动定位项目根目录、补齐导入路径，
并在需要时把当前工作目录切回项目根目录，避免手动 cd 依赖。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable


def _prepend_unique(paths: Iterable[Path]) -> None:
    """按给定顺序前置路径，跳过重复项。"""
    ordered = [str(path) for path in paths]
    for path_str in reversed(ordered):
        if path_str not in sys.path:
            sys.path.insert(0, path_str)


def resolve_project_root(anchor_file: str | Path) -> Path:
    """从当前文件位置向上查找项目根目录。"""
    current = Path(anchor_file).resolve()
    candidates = [current.parent, *current.parents]

    for candidate in candidates:
        if (candidate / "setup.py").exists() and (candidate / "src").is_dir():
            return candidate

    raise RuntimeError(
        f"无法从 {current} 自动定位项目根目录：未找到同时包含 setup.py 与 src/ 的目录"
    )


def bootstrap_project_paths(
    anchor_file: str | Path,
    *,
    include_project_root: bool = True,
    include_src: bool = True,
    change_cwd: bool = False,
) -> Path:
    """补齐项目运行所需路径，并可选切回项目根目录。"""
    project_root = resolve_project_root(anchor_file)

    paths = []
    if include_project_root:
        paths.append(project_root)
    if include_src:
        paths.append(project_root / "src")

    _prepend_unique(paths)

    if change_cwd:
        os.chdir(project_root)

    return project_root


__all__ = ["bootstrap_project_paths", "resolve_project_root"]
