# -*- coding: utf-8 -*-
"""
Somn 版本号管理 v6.2 [v6.2.0 / 开源发布]

## 版本号规范 (SemVer变体)

### 格式规则
- 统一使用小写 `v` 前缀: `vX.Y.Z`
- X = 主版本(架构级变更) / Y = 次版本(功能变更) / Z = 补丁版本(bug修复)
- 示例: v6.2.0, v6.2.1, v7.0.0

### 当前系统版本
"""
Somn_VERSION = "v6.2.0"
Somn_VERSION_INFO = (6, 2, 0)  # 用于程序化比较

### 各子系统版本索引（v6.2.0 发布版本）
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

# v6.2.0 开源发布: 统一版本号为 v6.2.0
