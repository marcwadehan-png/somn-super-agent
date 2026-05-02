# -*- coding: utf-8 -*-
"""
Somn 版本号管理

## 版本体系说明

Somn 使用双版本体系：
1. **构建版本**: v6.2.0 (项目整体版本，SemVer 格式)
2. **S 系列版本**: S1.0 / S1.1 (功能系列版本，动态扫描加载)

## 版本号规范

### 构建版本格式
- 统一使用小写 v 前缀: vX.Y.Z
- X = 主版本(架构级变更) / Y = 次版本(功能变更) / Z = 补丁版本(bug修复)
- 示例: v6.2.0, v6.2.1, v7.0.0

### S 系列版本格式
- S + 系列号 + . + 子版本号
- 示例: S1.0, S1.1, S2.0
- 以已加载 S 系列的最高版本为主
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════
# 项目构建版本 (SemVer)
# ═══════════════════════════════════════════════════════════════════════════

# Somn 项目构建版本
Somn_VERSION = "v6.2.0"
Somn_VERSION_INFO = (6, 2, 0)  # 用于程序化比较

# 各子系统版本索引（v6.2.0 发布版本）
SUBSYSTEM_VERSIONS = {
    # 核心层
    "SomnCore":           "v6.2.0",
    "TimeoutGuard":       "v6.2.0",
    "SomnEnsure":         "v6.2.0",
    "LocalLLMEngine":     "v6.2.0",
    "CommonExceptions":   "v6.2.0",
    # 智能体层
    "ClawArchitect":      "v6.2.0",
    "GlobalClawScheduler":"v6.2.0",
    "NeuralMemoryV3":     "v6.2.0",
    "ROICalculation":     "v6.2.0",
    # 调度层
    "WisdomDispatcher":   "v6.2.0",
    "ImperialLibrary":    "v6.2.0",
    # 学习层
    "ThreeTierLearning":  "v6.2.0",
    "ResearchPhaseManager":"v6.2.0",
    "ResearchStrategyEngine": "v6.2.0",
}


# ═══════════════════════════════════════════════════════════════════════════
# S 系列版本动态加载
# ═══════════════════════════════════════════════════════════════════════════

def _scan_s_series_version(module_path: Path) -> Optional[str]:
    """
    扫描模块目录获取 S 系列版本号

    Args:
        module_path: 模块路径

    Returns:
        S 系列版本号 (如 "S1.1") 或 None
    """
    init_file = module_path / "__init__.py"
    if not init_file.exists():
        return None

    try:
        content = init_file.read_text(encoding="utf-8")
        # 匹配 __version__ = "S1.x" 或 __version__ = 'S1.x'
        match = re.search(r'__version__\s*=\s*["\'](S\d+\.\d+)["\']', content)
        if match:
            return match.group(1)
    except Exception:
        pass

    return None


def _parse_s_series(version: str) -> Tuple[str, int]:
    """
    解析 S 系列版本号

    Args:
        version: 版本号 (如 "S1.1")

    Returns:
        (系列名, 子版本号) 如 ("S1", 1)
    """
    match = re.match(r'(S\d+)\.(\d+)', version)
    if match:
        return match.group(1), int(match.group(2))
    return version, 0


def get_loaded_s_series_version() -> str:
    """
    获取当前已加载的 S 系列版本

    动态扫描 knowledge_cells 等模块的 __version__，
    找到所有 S 系列版本，返回最新版本

    Returns:
        S 系列版本号 (如 "S1.1") 或 "unknown"
    """
    # 已知的 S 系列模块路径
    module_paths = [
        Path(__file__).parent.parent.parent.parent / "knowledge_cells",
        Path(__file__).parent.parent.parent / "neural_memory",
        Path(__file__).parent.parent.parent / "smart_office_assistant" / "src",
    ]

    s_versions: List[Tuple[str, int]] = []

    for base_path in module_paths:
        if base_path.exists():
            # 扫描所有子模块
            for item in base_path.iterdir():
                if item.is_dir() and (item / "__init__.py").exists():
                    version = _scan_s_series_version(item)
                    if version and version.startswith("S"):
                        series, sub = _parse_s_series(version)
                        s_versions.append((version, sub))

                # 也检查父级目录（有些模块直接在 base_path 下）
                version = _scan_s_series_version(base_path)
                if version and version.startswith("S"):
                    series, sub = _parse_s_series(version)
                    if (version, sub) not in s_versions:
                        s_versions.append((version, sub))

    if not s_versions:
        return "S1.0"  # 默认版本

    # 返回最新版本（按子版本号排序）
    s_versions.sort(key=lambda x: x[1], reverse=True)
    return s_versions[0][0]


def get_s_series_info() -> Dict[str, str]:
    """
    获取 S 系列版本详细信息

    Returns:
        S 系列版本信息字典
    """
    version = get_loaded_s_series_version()
    series, sub = _parse_s_series(version)

    return {
        "series": series,
        "version": version,
        "sub_version": sub,
        "build_version": Somn_VERSION,
    }


# ═══════════════════════════════════════════════════════════════════════════
# 初始化时自动加载 S 系列版本
# ═══════════════════════════════════════════════════════════════════════════

# 动态获取当前加载的 S 系列版本
_LOADED_S_VERSION = get_loaded_s_series_version()

# 导出便捷访问
S_SERIES_VERSION = _LOADED_S_VERSION  # 当前加载的 S 系列版本 (如 "S1.1")
S_SERIES_NAME = "S1"  # S 系列名

# 兼容旧代码
def get_version() -> str:
    """获取当前运行的版本（优先返回 S 系列版本）"""
    if S_SERIES_VERSION != "unknown":
        return S_SERIES_VERSION
    return Somn_VERSION
