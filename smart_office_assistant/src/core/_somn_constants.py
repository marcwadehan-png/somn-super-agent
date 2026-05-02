"""
SomnCore 静态常量定义
所有类级常量、配置值、默认值集中管理。
"""

from typing import Dict, Any

# ══════════════════════════════════════════════════════
# 并行化线程池配置
# ══════════════════════════════════════════════════════
ANALYSIS_EXECUTOR_MAX_WORKERS: int = 3
ANALYSIS_EXECUTOR_PREFIX: str = "somn_analysis"

# ══════════════════════════════════════════════════════
# 网络搜索熔断器配置
# ══════════════════════════════════════════════════════
SEARCH_CIRCUIT_BREAKER_CONFIG: Dict[str, Any] = {
    "state": "closed",               # closed | open | half_open
    "consecutive_failures": 0,       # 连续失败次数
    "failure_threshold": 3,          # 连续失败 N 次后进入 OPEN
    "recovery_timeout": 30.0,        # OPEN 状态持续 30s 后允许 HALF_OPEN 探测
    "last_failure_time": None,       # 上次失败时间
}

# ══════════════════════════════════════════════════════
# 搜索结果缓存配置
# ══════════════════════════════════════════════════════
SEARCH_CACHE_TTL: float = 300.0          # 缓存有效期 5 分钟
SEARCH_CACHE_MAX_ENTRIES: int = 50       # 最大缓存条目数
SEARCH_SIMILARITY_THRESHOLD: float = 0.5 # Jaccard 相似度阈值

# ══════════════════════════════════════════════════════
# LLM 结果缓存配置 (v16.0)
# ══════════════════════════════════════════════════════
LLM_CACHE_TTL: float = 600.0             # LLM 缓存有效期 10 分钟
LLM_CACHE_MAX_ENTRIES: int = 200         # 最大缓存条目数
LLM_CACHE_PROMPT_PREFIX: int = 256      # 取 prompt 前 N 字符做哈希

# ══════════════════════════════════════════════════════
# 分析阶段超时配置
# ══════════════════════════════════════════════════════
ANALYSIS_SEARCH_TIMEOUT: float = 4.0      # 搜索外层超时
ANALYSIS_LLM_TIMEOUT: float = 15.0       # LLM 最迟 15s
ANALYSIS_MEMORY_TIMEOUT: float = 5.0      # 记忆查询最迟 5s
ANALYSIS_PHASE2_TIMEOUT: float = 12.0    # 单路最大等待
ANALYSIS_STRATEGY_TIMEOUT: float = 20.0  # 策略生成超时

# ══════════════════════════════════════════════════════
# 经验库保留条数
# ══════════════════════════════════════════════════════
EXPERIENCE_STORE_MAX: int = 100          # 经验库最多保留条数
EXPERIENCE_REFLECTION_MAX: int = 50      # 复盘最多保留条数

# ══════════════════════════════════════════════════════
# TF-IDF 索引配置
# ══════════════════════════════════════════════════════
TFIDF_MIN_DF: int = 1
TFIDF_MAX_DF_RATIO: float = 0.95

# ══════════════════════════════════════════════════════
# 自治目标默认值
# ══════════════════════════════════════════════════════
DEFAULT_GOAL_SUCCESS_DEF: str = "形成稳定可复用结果"
DEFAULT_GOAL_PRIORITY: str = "medium"
DEFAULT_GOAL_TASK_TYPE: str = "general_analysis"

# ══════════════════════════════════════════════════════
# 任务状态评分映射
# ══════════════════════════════════════════════════════
TASK_STATUS_BASE_SCORE: Dict[str, float] = {
    "completed": 0.86,
    "failed": 0.22,
    "blocked": 0.35,
}

# ══════════════════════════════════════════════════════
# ROI 追踪默认值
# ══════════════════════════════════════════════════════
ROI_DEFAULT_ESTIMATED_MINUTES: float = 5.0
ROI_BASELINE: Dict[str, float] = {
    "avg_efficiency": 0.5,
    "avg_quality": 0.5,
    "adopt_rate": 0.5,
    "avg_roi_ratio": 0.0,
    "roi_return_score": 0.5,
    "confidence": 0.0,
}

# ══════════════════════════════════════════════════════
# 路由复杂度阈值
# ══════════════════════════════════════════════════════
ROUTING_COMPLEXITY_SIMPLE: float = 0.35   # < 0.35 → orchestrator (fast)
ROUTING_COMPLEXITY_MEDIUM: float = 0.55  # < 0.55 → orchestrator (home)
# >= 0.55 → full_workflow (feast)

# ══════════════════════════════════════════════════════
# 路由模式映射
# ══════════════════════════════════════════════════════
ROUTING_MODE_MAP: Dict[str, tuple] = {
    "fast":      ("orchestrator", "fast", "simple", "用户指定FAST模式"),
    "home":      ("orchestrator", "home", "medium", "用户指定HOME模式"),
    "feast":     ("full_workflow", "feast", "complex", "用户指定FEAST模式"),
    "direct":    ("orchestrator", "fast", "simple", "用户指定直接模式"),
    "preview":   ("orchestrator", "home", "medium", "用户指定预习模式"),
    "review":    ("orchestrator", "home", "medium", "用户指定复习模式"),
    "democratic":("full_workflow", "feast", "complex", "用户指定民主模式"),
}

# ══════════════════════════════════════════════════════
# 主链自评权重
# ══════════════════════════════════════════════════════
CHAIN_EVAL_WEIGHTS: Dict[str, float] = {
    "understanding": 0.15,
    "strategy": 0.20,
    "execution": 0.30,
    "quality": 0.20,
    "learning": 0.10,
    "completeness": 0.05,
}
