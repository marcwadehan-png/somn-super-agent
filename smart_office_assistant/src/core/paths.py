"""
Somn 项目路径配置
unified管理所有模块的数据存储路径,消除硬编码

使用方式:
    from src.core.paths import PROJECT_ROOT, DATA_DIR, LEARNING_DIR, ...

    # get项目根目录
    path = PROJECT_ROOT / "data" / "memory.json"

    # 初始化目录（在主入口调用）
    from src.core.paths import ensure_directories
    ensure_directories()
"""

from pathlib import Path
from functools import lru_cache

# ───────────────────────────────────────────────────────────────
# 路径常量定义（仅定义，不创建目录）
# ───────────────────────────────────────────────────────────────

# 项目根目录(自动检测)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"

# 各子模块数据目录
LEARNING_DIR = DATA_DIR / "learning"
MEMORY_DIR = DATA_DIR / "memory"
# 神经记忆系统实际数据路径(与每日学习系统共享)
NEURAL_MEMORY_DIR = LEARNING_DIR / "memory"
NEURAL_KNOWLEDGE_DIR = MEMORY_DIR / "research_framework"
MEMORY_V2_DIR = DATA_DIR / "memory_v2"
MEMORY_ENCODINGS_DIR = DATA_DIR / "memory_encodings"
MEMORY_GRANULARITY_DIR = DATA_DIR / "memory_granularity"
MEMORY_RICHNESS_DIR = DATA_DIR / "memory_richness"
SOLUTION_LEARNING_DIR = DATA_DIR / "solution_learning"
# 每日学习记忆日志目录（v2.0 独立运行版，原.workbuddy/memory）
DAILY_MEMORY_DIR = DATA_DIR / "daily_memory"
KNOWLEDGE_DIR = DATA_DIR / "knowledge"
KNOWLEDGE_GRAPH_DIR = DATA_DIR / "knowledge_graph"
ML_DIR = DATA_DIR / "ml"
ML_CLASSIFIER_DIR = ML_DIR / "classifier"
SEARCH_CACHE_DIR = DATA_DIR / "search_cache"
COLLECTED_DIR = DATA_DIR / "collected"
REASONING_DIR = DATA_DIR / "reasoning"
NARRATIVE_DIR = DATA_DIR / "narrative"
TOOLS_DIR = DATA_DIR / "tools"

# 系统字体路径(Windows)
FONT_MS_YAHEI = Path("C:/Windows/Fonts/msyh.ttc")
FONT_SIMHEI = Path("C:/Windows/Fonts/simhei.ttf")
FONT_SIMSUN = Path("C:/Windows/Fonts/simsun.ttc")

# ───────────────────────────────────────────────────────────────
# 目录惰性初始化函数（修复全局代码规范）
# ───────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def get_all_paths() -> dict:
    """获取所有路径的字典 - 惰性初始化"""
    return {
        'PROJECT_ROOT': PROJECT_ROOT,
        'DATA_DIR': DATA_DIR,
        'LEARNING_DIR': LEARNING_DIR,
        'MEMORY_DIR': MEMORY_DIR,
        'MEMORY_V2_DIR': MEMORY_V2_DIR,
        'MEMORY_ENCODINGS_DIR': MEMORY_ENCODINGS_DIR,
        'MEMORY_GRANULARITY_DIR': MEMORY_GRANULARITY_DIR,
        'MEMORY_RICHNESS_DIR': MEMORY_RICHNESS_DIR,
        'SOLUTION_LEARNING_DIR': SOLUTION_LEARNING_DIR,
        'DAILY_MEMORY_DIR': DAILY_MEMORY_DIR,  # v2.0 独立运行版
        'KNOWLEDGE_DIR': KNOWLEDGE_DIR,
        'KNOWLEDGE_GRAPH_DIR': KNOWLEDGE_GRAPH_DIR,
        'ML_DIR': ML_DIR,
        'ML_CLASSIFIER_DIR': ML_CLASSIFIER_DIR,
        'SEARCH_CACHE_DIR': SEARCH_CACHE_DIR,
        'COLLECTED_DIR': COLLECTED_DIR,
        'REASONING_DIR': REASONING_DIR,
        'NARRATIVE_DIR': NARRATIVE_DIR,
        'TOOLS_DIR': TOOLS_DIR,
    }

def ensure_directories() -> None:
    """确保所有必要目录存在 - 应在主入口调用"""
    _dirs = [
        DATA_DIR, LEARNING_DIR, MEMORY_DIR, MEMORY_V2_DIR,
        MEMORY_ENCODINGS_DIR, MEMORY_GRANULARITY_DIR, MEMORY_RICHNESS_DIR,
        SOLUTION_LEARNING_DIR, KNOWLEDGE_DIR, KNOWLEDGE_GRAPH_DIR,
        ML_DIR, ML_CLASSIFIER_DIR, SEARCH_CACHE_DIR, COLLECTED_DIR,
        REASONING_DIR, NARRATIVE_DIR, TOOLS_DIR,
        DAILY_MEMORY_DIR,  # v2.0 独立运行版记忆目录
    ]
    for _dir in _dirs:
        _dir.mkdir(parents=True, exist_ok=True)

# ───────────────────────────────────────────────────────────────
# 模块导出
# ───────────────────────────────────────────────────────────────
__all__ = [
    'PROJECT_ROOT',
    'DATA_DIR',
    'LEARNING_DIR',
    'MEMORY_DIR',
    'MEMORY_V2_DIR',
    'MEMORY_ENCODINGS_DIR',
    'MEMORY_GRANULARITY_DIR',
    'MEMORY_RICHNESS_DIR',
    'SOLUTION_LEARNING_DIR',
    'DAILY_MEMORY_DIR',  # v2.0 独立运行版
    'KNOWLEDGE_DIR',
    'KNOWLEDGE_GRAPH_DIR',
    'ML_DIR',
    'ML_CLASSIFIER_DIR',
    'SEARCH_CACHE_DIR',
    'COLLECTED_DIR',
    'REASONING_DIR',
    'NARRATIVE_DIR',
    'TOOLS_DIR',
    'FONT_MS_YAHEI',
    'FONT_SIMHEI',
    'FONT_SIMSUN',
    'get_all_paths',
    'ensure_directories',
]
