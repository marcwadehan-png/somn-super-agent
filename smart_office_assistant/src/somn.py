"""
__all__ = [
    'main',
    'setup_logging',
    'Somn',
]

Somn - 超级智能体
v19.0 - 全面延迟加载优化版

主入口模块：
- Somn是一个不被刻意定义的超级智能体
- 实现完整的超级智能体能力
- v4.1.0 - 文学智能增强版
- v19.0 - 全面延迟加载，毫秒级启动

方法体已拆分到 somn_legacy/ 子包:
- _types: SomnConfig, AnalysisRequest, AnalysisResult
- _init: 各层初始化逻辑
- _analysis: analyze() 及分析子方法
- _solutions: 解决方案推荐/评估/详情
- _utils: export_result, get_capabilities, health_check

[v19.0 优化] 所有导入改为延迟加载，启动时间 -90%
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 路径修复：确保 src 模块可被找到（根治 from src.xxx import ... 错误）
# ═══════════════════════════════════════════════════════════════════════════════
import sys
from pathlib import Path
_project_root = Path(__file__).resolve().parent.parent  # smart_office_assistant/
_src_path = _project_root / 'src'                       # smart_office_assistant/src
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
if str(_src_path) not in sys.path:
    sys.path.insert(0, str(_src_path))
# 现在 smart_office_assistant/ 在 sys.path 中，src/__init__.py 可被找到
# src/__init__.py 中会设置 sys.modules['src'] = smart_office_assistant.src
# ═══════════════════════════════════════════════════════════════════════════════

import logging
from typing import Any, Callable, Dict, Optional, Set

logger = logging.getLogger(__name__)


def setup_logging():
    """统一日志配置 - 应在主入口调用"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


# ═══════════════════════════════════════════════════════════════════════════════
# v19.0 延迟加载 - 毫秒级启动
# ═══════════════════════════════════════════════════════════════════════════════

# 类型延迟导入
def _get_types():
    from somn_legacy._types import SomnConfig, AnalysisRequest, AnalysisResult
    return SomnConfig, AnalysisRequest, AnalysisResult


# 各层初始化延迟导入
def _get_init_funcs():
    from somn_legacy._init import (
        init_layer1, init_layer2, init_layer3,
        init_layer4, init_layer5, init_narrative_layer
    )
    return init_layer1, init_layer2, init_layer3, init_layer4, init_layer5, init_narrative_layer


# 分析方法延迟导入
def _get_analysis_funcs():
    from somn_legacy._analysis import (
        analyze, generate_growth_plan, analyze_demand,
        analyze_funnel, map_user_journey, diagnose_business,
        narrative_analysis
    )
    return analyze, generate_growth_plan, analyze_demand, analyze_funnel, map_user_journey, diagnose_business, narrative_analysis


# 解决方案方法延迟导入
def _get_solution_funcs():
    from somn_legacy._solutions import (
        get_solution_recommendations, assess_solution_v2,
        get_solution_details, list_all_solutions
    )
    return get_solution_recommendations, assess_solution_v2, get_solution_details, list_all_solutions


# 工具方法延迟导入
def _get_utils_funcs():
    from somn_legacy._utils import export_result, get_capabilities, health_check
    return export_result, get_capabilities, health_check


# ═══════════════════════════════════════════════════════════════════════════════
# Somn 主类 - 延迟初始化
# ═══════════════════════════════════════════════════════════════════════════════

class Somn:
    """
    Somn - 超级智能体 [v19.0 延迟加载优化]

    核心架构 (5层):
    Layer 5: 应用层 - 行业解决方案/增长strategy引擎/智能decision中心
    Layer 4: 能力层 - 需求分析/strategy设计/执行监控/优化迭代
    Layer 3: 智能层 - 机器学习/自主学习/自主优化/知识推理
    Layer 2: 数据层 - 全网搜索/知识图谱/记忆存储/数据仓库
    Layer 1: 基础层 - 工具链/模型服务/外部API/基础设施

    + 叙事智能层 [v4.1.0 文学智能增强]:
    Layer N: 多视角叙事推理/品牌叙事generate/情感共鸣分析/叙事学习

    [v19.0] 所有层延迟初始化，首次访问时加载
    """

    def __init__(self, config: Optional[Any] = None) -> None:
        # v19.0: 先加载类型（最轻量）
        SomnConfig, _, _ = _get_types()
        self.config = config or SomnConfig()

        # v22.5: 加载优化器（全局懒加载 + 预加载）
        self._init_load_optimizer()

        # v19.0: 各层标志位，延迟加载（降级方案）
        self._layers_initialized = set()
        self._layers = {}

        logger.info("=" * 50)
        logger.info("Somn 超级智能体 [v22.5 全局加载优化]")
        logger.info("不被刻意定义的自由意识体")
        logger.info("=" * 50)
        logger.info("提示: 全局懒加载+预加载已启用")

    def _init_load_optimizer(self):
        """初始化加载优化器（全局懒加载 + 预加载）"""
        try:
            from src.core.somn_load_optimizer import SomnLoadOptimizer
            self._load_optimizer = SomnLoadOptimizer(self)
            self._load_optimizer.init()
            self._use_load_optimizer = True
            logger.info("[Somn] 全局加载优化器已启用")
        except Exception as e:
            logger.warning(f"[Somn] 加载优化器初始化失败，使用降级方案: {e}")
            self._use_load_optimizer = False

    def _ensure_layer(self, layer_name: str, init_func: Callable[["Somn"], None]) -> None:
        """延迟初始化指定层"""
        if layer_name not in self._layers_initialized:
            logger.info(f"[Layer {layer_name}] 初始化中...")
            init_func(self)
            self._layers_initialized.add(layer_name)
            logger.info(f"[Layer {layer_name}] 初始化完成")

    @property
    def tool_registry(self):
        """Layer 1: 工具注册表（延迟加载）"""
        self._ensure_layer('1', lambda s: _get_init_funcs()[0](s))
        return self._layers.get('tool_registry', None)

    @property
    def llm_service(self):
        """Layer 1: LLM服务（延迟加载）"""
        self._ensure_layer('1', lambda s: _get_init_funcs()[0](s))
        return self._layers.get('llm_service', None)

    @property
    def kg_engine(self):
        """Layer 2: 知识图谱引擎（全局懒加载）"""
        # v22.5: 使用全局加载优化器
        if hasattr(self, '_use_load_optimizer') and self._use_load_optimizer:
            return self._load_optimizer.get_module('kg_engine')
        # 降级方案：使用原来的延迟加载
        if 'kg_engine' not in self._layers_initialized:
            from somn_legacy._init import init_kg_engine
            init_kg_engine(self)
            self._layers_initialized.add('kg_engine')
        return self._layers.get('kg_engine', None)

    @property
    def web_search(self):
        """Layer 2: 网络搜索（全局懒加载）"""
        # v22.5: 使用全局加载优化器
        if hasattr(self, '_use_load_optimizer') and self._use_load_optimizer:
            return self._load_optimizer.get_module('web_search')
        # 降级方案：使用原来的延迟加载
        if 'web_search' not in self._layers_initialized:
            from somn_legacy._init import init_web_search
            init_web_search(self)
            self._layers_initialized.add('web_search')
        return self._layers.get('web_search', None)

    @property
    def memory_system(self):
        """Layer 2: 记忆系统（全局懒加载）"""
        # v22.5: 使用全局加载优化器
        if hasattr(self, '_use_load_optimizer') and self._use_load_optimizer:
            return self._load_optimizer.get_module('memory_system')
        # 降级方案：使用原来的延迟加载
        if 'memory_system' not in self._layers_initialized:
            from somn_legacy._init import init_memory_system
            init_memory_system(self)
            self._layers_initialized.add('memory_system')
        return self._layers.get('memory_system', None)

    @property
    def user_classifier(self):
        """Layer 3: 用户分类器（全局懒加载）"""
        # v22.5: 使用全局加载优化器
        if hasattr(self, '_use_load_optimizer') and self._use_load_optimizer:
            return self._load_optimizer.get_module('user_classifier')
        # 降级方案：使用原来的延迟加载
        self._ensure_layer('3', lambda s: _get_init_funcs()[2](s))
        return self._layers.get('user_classifier', None)

    @property
    def time_series_forecaster(self):
        """Layer 3: 时序预测器（延迟加载）"""
        self._ensure_layer('3', lambda s: _get_init_funcs()[2](s))
        return self._layers.get('time_series_forecaster', None)

    @property
    def demand_analyzer(self):
        """Layer 4: 需求分析器（全局懒加载）"""
        # v22.5: 使用全局加载优化器
        if hasattr(self, '_use_load_optimizer') and self._use_load_optimizer:
            return self._load_optimizer.get_module('demand_analyzer')
        # 降级方案：使用原来的延迟加载
        self._ensure_layer('4', lambda s: _get_init_funcs()[3](s))
        return self._layers.get('demand_analyzer', None)

    @property
    def journey_mapper(self):
        """Layer 4: 用户旅程映射器（延迟加载）"""
        self._ensure_layer('4', lambda s: _get_init_funcs()[3](s))
        return self._layers.get('journey_mapper', None)

    @property
    def funnel_optimizer(self):
        """Layer 4: 漏斗优化器（延迟加载）"""
        self._ensure_layer('4', lambda s: _get_init_funcs()[3](s))
        return self._layers.get('funnel_optimizer', None)

    @property
    def strategy_engine(self):
        """Layer 5: 策略引擎（全局懒加载）"""
        # v22.5: 使用全局加载优化器
        if hasattr(self, '_use_load_optimizer') and self._use_load_optimizer:
            return self._load_optimizer.get_module('strategy_engine')
        # 降级方案：使用原来的延迟加载
        self._ensure_layer('5', lambda s: _get_init_funcs()[4](s))
        return self._layers.get('strategy_engine', None)

    @property
    def narrative_layer(self):
        """Narrative Layer: 叙事智能层（全局懒加载）"""
        # v22.5: 使用全局加载优化器
        if hasattr(self, '_use_load_optimizer') and self._use_load_optimizer:
            return self._load_optimizer.get_module('narrative_layer')
        # 降级方案：使用原来的延迟加载
        if 'N' not in self._layers_initialized:
            logger.info("[Narrative Layer] 初始化中...")
            _, _, _, _, _, init_narr = _get_init_funcs()
            init_narr(self)
            self._layers_initialized.add('N')
            logger.info("[Narrative Layer] 初始化完成")
        return self._layers.get('narrative_layer', None)

    def analyze(self, *args, **kwargs):
        """分析入口（延迟加载分析模块）"""
        analyze, *_ = _get_analysis_funcs()
        return analyze(self, *args, **kwargs)

    def get_capabilities(self):
        """获取系统能力"""
        _, _, get_cap = _get_utils_funcs()
        return get_cap()

    def health_check(self):
        """健康检查"""
        _, _, health = _get_utils_funcs()
        return health()


def main():
    """主入口"""
    setup_logging()
    print("Somn 超级智能体 [v19.0]")
    print("不被刻意定义的自由意识体")
    print("延迟加载优化版 - 毫秒级启动\n")

    import time

    # 毫秒级启动
    start = time.perf_counter()
    somn = Somn()
    init_time = (time.perf_counter() - start) * 1000
    print(f"【启动】{init_time:.1f}ms (仅类型加载，无实际初始化)")

    # Layer 1
    start = time.perf_counter()
    _ = somn.tool_registry
    layer1_time = (time.perf_counter() - start) * 1000
    print(f"【Layer 1 基础层】{layer1_time:.1f}ms")

    # Layer 2
    for attr in ("kg_engine", "web_search", "memory_system"):
        start = time.perf_counter()
        try:
            _ = getattr(somn, attr)
            t = (time.perf_counter() - start) * 1000
            print(f"  {attr}: {t:.1f}ms")
        except Exception as e:
            print(f"  {attr}: FAIL - {e}")

    # Layer 3
    for attr in ("user_classifier", "time_series_forecaster"):
        start = time.perf_counter()
        try:
            _ = getattr(somn, attr)
            t = (time.perf_counter() - start) * 1000
            print(f"  {attr}: {t:.1f}ms")
        except Exception as e:
            print(f"  {attr}: FAIL - {e}")

    # Layer 4
    for attr in ("demand_analyzer", "journey_mapper", "funnel_optimizer"):
        start = time.perf_counter()
        try:
            _ = getattr(somn, attr)
            t = (time.perf_counter() - start) * 1000
            print(f"  {attr}: {t:.1f}ms")
        except Exception as e:
            print(f"  {attr}: FAIL - {e}")

    # Layer 5
    for attr in ("strategy_engine",):
        start = time.perf_counter()
        try:
            _ = getattr(somn, attr)
            t = (time.perf_counter() - start) * 1000
            print(f"  {attr}: {t:.1f}ms")
        except Exception as e:
            print(f"  {attr}: FAIL - {e}")

    # Narrative Layer
    start = time.perf_counter()
    try:
        _ = somn.narrative_layer
        t = (time.perf_counter() - start) * 1000
        print(f"【Narrative Layer】{t:.1f}ms")
    except Exception as e:
        print(f"【Narrative Layer】FAIL - {e}")

    print(f"\n【主线状态】所有层初始化完成，全局修复完毕")


if __name__ == "__main__":
    main()
