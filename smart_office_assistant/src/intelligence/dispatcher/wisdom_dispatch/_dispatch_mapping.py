"""
智慧引擎unified调度器 - 初始化与问题-学派映射矩阵

[v2.2.0 道家升级] 新增无为调度模式（WuWeiDispatchMode），
体现"道法自然"的系统行为原则：让各模块自然响应，而非强制激活竞争。
"""

from typing import Dict, List, Tuple, Any, Optional, Set
from enum import Enum
from dataclasses import dataclass, field
import time
import threading
import logging

from ._dispatch_enums import WisdomSchool, ProblemType, SubSchool, SUBSCHOOL_PARENT

logger = logging.getLogger(__name__)


# ── v2.2.0: 道家无为调度模式 ──────────────────────────────────────────────

class WuWeiDispatchMode(Enum):
    """
    无为调度模式 - 体现"道法自然"的道家哲学原则。

    - TASK_MATCHING: 传统匹配模式，立即激活最优模块
    - WUWEI_OBSERVE: 无为观察模式，观察-等待-顺势
    - HYBRID_FLOW: 混合流模式，智能选择前两者
    """
    TASK_MATCHING = "task_matching"      # 传统立即匹配
    WUWEI_OBSERVE = "wuwei_observe"       # 无为观察模式
    HYBRID_FLOW = "hybrid_flow"           # 智能混合


@dataclass
class WuWeiConfig:
    """
    无为调度配置 - "上善若水"的系统参数。

    核心理念：让系统如水般柔韧自然地响应，而非强制干预。
    """
    # 观察窗口期（毫秒）：无为模式下等待自然响应的最长时间
    observe_window_ms: int = 500
    # 自然响应阈值：窗口期内至少需要多少被动响应才进入最终分发
    passive_response_threshold: int = 1
    # 是否在无为模式下记录观察日志
    log_observation: bool = True
    # 无为模式触发的任务模糊度阈值（0-1，越高越模糊）
    ambiguity_threshold: float = 0.6
    # 允许参与无为观察的学派白名单（None表示全部）
    allowed_schools: Optional[Set[WisdomSchool]] = None
    # 水属性学派（无为观察模式优先）：这些学派的响应被视为"更自然"
    water_nature_schools: Set[WisdomSchool] = field(
        default_factory=lambda: {WisdomSchool.DAOIST, WisdomSchool.BUDDHIST}
    )

    def __post_init__(self):
        # 自动识别具有"水属性"的学派（无为、佛家等柔性学派）
        self.water_nature_schools = self.water_nature_schools


@dataclass
class WuWeiObservationResult:
    """无为观察结果 - 记录自然响应的分析"""
    mode_used: WuWeiDispatchMode
    observed_responses: List[Tuple[WisdomSchool, float, str]]  # (school, confidence, response_type)
    final_dispatch: Optional[List[Tuple[WisdomSchool, float]]]  # 最终分发结果
    observation_duration_ms: float
    natural_response_count: int
    # 道家分析
    dao_analysis: str = ""  # 自然和谐度分析
    water_nature_score: float = 0.0  # 上善若水评分
    balance_assessment: str = ""     # 阴阳平衡评估

class WisdomDispatcher:
    """智慧引擎unified调度器（初始化+映射矩阵）"""

    # [v22.5 调度优化] pickle缓存版本号，修改后自动失效旧缓存
    PICKLE_CACHE_VERSION = "SomnV6.2"

    def __init__(self):
        self._engine_registry: Dict[WisdomSchool, Tuple[str, str]] = {}
        self._engines: Dict[WisdomSchool, Any] = {}
        self._engine_lock = __import__('threading').Lock()
        self._failed_engines: set = set()
        # [v10.1] 失败时间追踪：school → 首次失败时间戳（用于冷却后重试）
        self._failed_timestamps: Dict[WisdomSchool, float] = {}
        # [v10.1] 失败重试冷却时间（秒），冷却后可重新尝试加载
        self._failure_cooldown: float = 300.0  # 5分钟冷却
        # [v10.2 Phase3] pickle预编译缓存路径
        self._pickle_cache_path = None  # 延迟初始化

        # [v2.2.0 道家升级] 无为调度模式配置
        self.wuwei_mode: WuWeiDispatchMode = WuWeiDispatchMode.TASK_MATCHING
        self.wuwei_config: WuWeiConfig = WuWeiConfig()
        self._wuwei_responses: List[Tuple[WisdomSchool, float, str]] = []  # 被动响应收集
        self._wuwei_lock = threading.Lock()
        self._wuwei_observation_active = False
        self._wuwei_observation_start: Optional[float] = None

        self._register_engine_table()
        self.problem_school_mapping = self._build_mapping_matrix()
        self.subschool_mapping = self._build_subschool_mapping()
        # [v22.5 映射索引优化] 构建反向索引：School → ProblemType（加速查询）
        self._school_to_problem_types: Dict[WisdomSchool, List[Tuple[ProblemType, float]]] = {}
        for problem_type, schools in self.problem_school_mapping.items():
            for school, weight in schools:
                if school not in self._school_to_problem_types:
                    self._school_to_problem_types[school] = []
                self._school_to_problem_types[school].append((problem_type, weight))
        logger.info(f"[映射索引优化] 反向索引已构建: {len(self._school_to_problem_types)} 个学派")

        # [v10.2] 尝试从pickle缓存恢复引擎实例
        # [v22.5 优化] 重新启用，已添加版本控制，支持V6.2+新问题类型
        self._try_restore_from_pickle()
        # ── v2.1.0: 神之架构 - 部门路由 ──
        from ._dispatch_court import resolve_departments, DEPARTMENT_SCHOOL_MATRIX
        self._department_matrix = DEPARTMENT_SCHOOL_MATRIX
        self._resolve_departments = resolve_departments
        self.school_weights = {
            WisdomSchool.CONFUCIAN: 0.10,
            WisdomSchool.DAOIST: 0.08,
            WisdomSchool.BUDDHIST: 0.06,
            WisdomSchool.SUFU: 0.05,
            WisdomSchool.MILITARY: 0.05,
            WisdomSchool.LVSHI: 0.03,
            WisdomSchool.HONGMING: 0.03,
            WisdomSchool.METAPHYSICS: 0.03,
            WisdomSchool.CIVILIZATION: 0.02,
            WisdomSchool.CIV_WAR_ECONOMY: 0.02,
            WisdomSchool.SCI_FI: 0.02,
            WisdomSchool.GROWTH: 0.02,
            WisdomSchool.MYTHOLOGY: 0.02,
            WisdomSchool.LITERARY: 0.02,
            WisdomSchool.ANTHROPOLOGY: 0.01,
            WisdomSchool.BEHAVIOR: 0.01,
            WisdomSchool.SCIENCE: 0.02,
            WisdomSchool.SOCIAL_SCIENCE: 0.03,
            WisdomSchool.YANGMING: 0.04,
            WisdomSchool.DEWEY: 0.03,
            WisdomSchool.TOP_METHODS: 0.05,
            WisdomSchool.NATURAL_SCIENCE: 0.03,
            WisdomSchool.CHINESE_CONSUMER: 0.03,
            WisdomSchool.WCC: 0.03,
            WisdomSchool.HISTORICAL_THOUGHT: 0.03,
            # V6.0 第二阶段新增学派
            WisdomSchool.PSYCHOLOGY: 0.02,
            WisdomSchool.SYSTEMS: 0.01,
            WisdomSchool.MANAGEMENT: 0.02,
            WisdomSchool.ZONGHENG: 0.02,
            # V6.0 第三阶段新增: 墨家/法家核心学派
            WisdomSchool.MOZI: 0.03,
            WisdomSchool.FAJIA: 0.04,
            # V6.0 第三阶段新增: 经济学/名家/阴阳家/复杂性科学
            WisdomSchool.ECONOMICS: 0.04,
            WisdomSchool.MINGJIA: 0.03,
            WisdomSchool.WUXING: 0.04,
            WisdomSchool.COMPLEXITY: 0.04,
            # V6.2 社会科学智慧版新增权重
            WisdomSchool.SOCIOLOGY: 0.04,
            WisdomSchool.BEHAVIORAL_ECONOMICS: 0.04,
            WisdomSchool.COMMUNICATION: 0.03,
            WisdomSchool.CULTURAL_ANTHROPOLOGY: 0.02,
            WisdomSchool.POLITICAL_ECONOMICS: 0.04,
            WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY: 0.03,
            WisdomSchool.SOCIAL_PSYCHOLOGY: 0.03,
        }

    _ENGINE_TABLE: List[Tuple["WisdomSchool", str, str]] = [
        (None, "engines.ru_wisdom_unified", "UnifiedConfucianWisdom"),
        (None, "engines.dao_wisdom_core", "DaoWisdomCore"),
        (None, "engines.confucian_buddhist_dao_fusion_engine", "ConfucianBuddhistDaoFusion"),
        (None, "engines.sufu_wisdom_core", "SufuWisdomCore"),
        (None, "engines.military_strategy_engine", "MilitaryStrategyEngine"),
        (None, "engines.lvshi_wisdom_engine", "LvShiWisdomEngine"),
        (None, "engines.hongming_wisdom_core", "HongMingWisdomCore"),
        (None, "engines.metaphysics_wisdom_unified", "MetaphysicsWisdomUnified"),
        (None, "engines.civilization_wisdom_core", "CivilizationWisdomCore"),
        (None, "engines.civilization_war_economy_core", "CivilizationWarEconomyCore"),
        (None, "engines.marvel_wisdom_unified", "MarvelWisdomUnified"),
        (None, "engines.thinking_growth_unified", "ThinkingGrowthUnifiedSystem"),
        (None, "engines.mythology_wisdom_engine", "MythologyWisdomEngine"),
        (None, "engines.literary_narrative_engine", "LiteraryNarrativeEngine"),
        (None, "engines.anthropology_wisdom_engine", "AnthropologyWisdomEngine"),
        (None, "engines.behavior_shaping_engine", "BehaviorShapingEngine"),
        (None, "engines.science_thinking_engine", "ScienceThinkingEngine"),
        (None, "engines.social_science_engine", "SocialScienceWisdomEngine"),
        (None, "engines.philosophy.yangming_xinxue_engine", "YangmingXinxueEngine"),
        (None, "reasoning.dewey_thinking_engine", "DeweyThinkingEngine"),
        (None, "engines.top_thinking_engine", "TopThinkingEngine"),
        (None, "engines.natural_science_unified", "NaturalScienceUnified"),
        (None, "engines.chinese_consumer_culture_engine", "ChineseConsumerCultureEngine"),
        (None, "engines.wcc_evolutionary_core", "WCCEvolutionaryCore"),
        (None, "engines.historical_thought_trinity_engine", "HistoricalThoughtTrinityEngine"),
        # V6.0 第二阶段新增学派
        (WisdomSchool.PSYCHOLOGY, "engines.psychology_wisdom_engine", "PsychologyWisdomEngine"),
        (WisdomSchool.SYSTEMS, "engines.systems_thinking_engine", "SystemsThinkingEngine"),
        (WisdomSchool.MANAGEMENT, "engines.management_wisdom_engine", "ManagementWisdomEngine"),
        (WisdomSchool.ZONGHENG, "engines.zongheng_wisdom_engine", "ZonghengWisdomEngine"),
        # V6.0 第三阶段新增: 墨家/法家核心学派
        (WisdomSchool.MOZI, "engines.cloning.tier1.mozi", "MoZiCloning"),
        (WisdomSchool.FAJIA, "engines.cloning.tier1.hanfeizi", "HanFeiZiCloning"),
        # V6.0 第三阶段新增: 经济学/名家/阴阳家/复杂性科学
        (WisdomSchool.ECONOMICS, "engines.economics_wisdom_engine", "EconomicsWisdomEngine"),
        (WisdomSchool.MINGJIA, "engines.mingjia_wisdom_engine", "MingjiaWisdomEngine"),
        (WisdomSchool.WUXING, "engines.wuxing_wisdom_engine", "WuxingWisdomEngine"),
        (WisdomSchool.COMPLEXITY, "engines.complexity_wisdom_engine", "ComplexityWisdomEngine"),
        # V6.2 社会科学智慧版新增引擎
        (WisdomSchool.SOCIOLOGY, "engines.sociology_wisdom", "SociologyWisdomCore"),
        (WisdomSchool.BEHAVIORAL_ECONOMICS, "engines.behavioral_economics_wisdom", "BehavioralEconomicsWisdomCore"),
        (WisdomSchool.COMMUNICATION, "engines.communication_wisdom", "CommunicationWisdomCore"),
        (WisdomSchool.CULTURAL_ANTHROPOLOGY, "engines.anthropology_wisdom", "AnthropologyWisdomCore"),
        (WisdomSchool.POLITICAL_ECONOMICS, "engines.political_economics_wisdom", "PoliticalEconomicsWisdomCore"),
        (WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, "engines.organizational_psychology_wisdom", "OrganizationalPsychologyWisdomCore"),
        (WisdomSchool.SOCIAL_PSYCHOLOGY, "engines.social_psychology_wisdom", "SocialPsychologyWisdomCore"),
    ]

    def _register_engine_table(self):
        """将枚举顺序与注册表绑定"""
        _schools = list(WisdomSchool)
        for i, (school, mod_name, cls_name) in enumerate(self._ENGINE_TABLE):
            if school is None and i < len(_schools):
                school = _schools[i]
            if school is not None:
                self._engine_registry[school] = (mod_name, cls_name)

    def prewarm_all_engines(self, timeout: float = 30.0) -> Dict[str, Any]:
        """
        [v10.1 P1-3修复] 预热全部25个学派引擎，消除首次调用时的懒加载延迟。

        使用 ThreadPoolExecutor 并行加载所有学派引擎，每个引擎有独立超时保护。
        总耗时从串行的最多 25×2s=50s 降至并行时的 ~2-5s。

        Args:
            timeout: 总预热超时（秒），默认30s

        Returns:
            包含成功/失败/跳过数量的统计字典
        """
        import time as _time
        import logging as _logging
        from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeout
        _logger = _logging.getLogger(__name__)

        _start = _time.monotonic()
        _ENGINES = list(WisdomSchool)
        results = {"total": len(_ENGINES), "loaded": 0, "failed": 0, "skipped": 0}

        def _load_one(school: WisdomSchool) -> str:
            """在子线程中加载单个引擎（强制重试失败引擎）"""
            try:
                engine = self._get_engine(school, force_retry=True)
                return f"OK:{school.value}" if engine else f"NULL:{school.value}"
            except Exception as e:
                return f"ERR:{school.value}:{e}"

        # 使用5个worker并行加载25个引擎
        _MAX_WORKERS = 5
        _PER_ENGINE_TIMEOUT = 5.0  # 每个引擎最多5秒
        with ThreadPoolExecutor(max_workers=_MAX_WORKERS) as executor:
            futures = {executor.submit(_load_one, s): s for s in _ENGINES}
            for future in as_completed(futures):
                # 检查总预热超时
                if (_time.monotonic() - _start) > timeout:
                    _logger.warning(f"[预热] 总预热超时({timeout}s)，停止等待剩余引擎")
                    for f in futures:
                        f.cancel()
                    break
                try:
                    res = future.result(timeout=_PER_ENGINE_TIMEOUT)
                    if res.startswith("OK:"):
                        results["loaded"] += 1
                    elif res.startswith("NULL:"):
                        results["skipped"] += 1
                    else:
                        results["failed"] += 1
                except FuturesTimeout:
                    results["failed"] += 1
                    _logger.warning(f"[预热] 引擎 {futures[future].value} 加载超时({_PER_ENGINE_TIMEOUT}s)")
                except Exception as e:
                    results["failed"] += 1
                    _logger.warning(f"[预热] 引擎 {futures[future].value} 加载异常: {e}")

        _elapsed = _time.monotonic() - _start
        _logger.info(f"[预热] 25学派引擎预热完成({_elapsed:.1f}s): "
                      f"已加载{results['loaded']}/{results['total']}, "
                      f"失败{results['failed']}, 跳过{results['skipped']}")

        # [v10.2 Phase3] 预热完成后尝试保存pickle缓存
        if results["loaded"] >= results["total"] * 0.8:
            self._save_to_pickle()
        return results

    # ── v10.2 Phase3: pickle预编译缓存 ──────────────────────────

    def _get_pickle_cache_path(self) -> "Path | None":
        """获取pickle缓存文件路径（延迟初始化）"""
        if self._pickle_cache_path is not None:
            return self._pickle_cache_path
        try:
            from pathlib import Path
            cache_dir = Path(__import__("os").getcwd()) / "data" / "engine_cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
            self._pickle_cache_path = cache_dir / "wisdom_engines.pkl"
            return self._pickle_cache_path
        except Exception:
            return None

    def _try_restore_from_pickle(self) -> bool:
        """
        [v10.2 Phase3] 尝试从pickle缓存恢复引擎实例。

        如果pickle文件存在且可读，则直接反序列化到 _engines，
        跳过全部25个引擎的 import_module + 实例化过程。

        [v22.5 优化] 添加版本控制，支持V6.2+新问题类型。
        版本不匹配时自动失效缓存，重新创建引擎实例。

        Returns:
            True if restored from cache, False otherwise
        """
        try:
            cache_path = self._get_pickle_cache_path()
            if not cache_path or not cache_path.exists():
                return False
            import pickle
            import os
            mtime_cache = cache_path.stat().st_mtime
            # 检查缓存是否过期（超过24小时重新生成）
            if (time.time() - mtime_cache) > 86400:
                return False
            with open(cache_path, "rb") as f:
                # SECURITY: pickle仅用于内部缓存，数据由本模块生成
                data = pickle.load(f)

            # [v22.5 版本控制] 检查缓存版本
            if isinstance(data, dict) and "version" in data and "engines" in data:
                # 新格式：包含版本信息
                if data["version"] != self.PICKLE_CACHE_VERSION:
                    __import__("logging").getLogger(__name__).info(
                        f"[_dispatch] pickle缓存版本不匹配: {data['version']} != {self.PICKLE_CACHE_VERSION}，重新生成"
                    )
                    return False
                engines = data["engines"]
            elif isinstance(data, dict):
                # 旧格式：直接是引擎字典，视为版本不匹配
                return False
            else:
                return False

            with self._engine_lock:
                self._engines = engines
            __import__("logging").getLogger(__name__).info(
                f"[_dispatch] pickle缓存恢复: {len(self._engines)} 个引擎 (版本 {data.get('version', 'unknown')})"
            )
            return True
        except Exception as e:
            __import__("logging").getLogger(__name__).warning(
                f"[_dispatch] pickle缓存恢复失败: {e}"
            )
            return False

    def _save_to_pickle(self) -> bool:
        """
        [v10.2 Phase3] 将当前已加载的引擎字典序列化到pickle文件。

        [v22.5 优化] 保存版本信息，支持版本控制。

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            cache_path = self._get_pickle_cache_path()
            if not cache_path:
                return False
            import pickle
            with self._engine_lock:
                engines = {k: v for k, v in self._engines.items() if v is not None}
                data = {
                    "version": self.PICKLE_CACHE_VERSION,
                    "engines": engines
                }
            with open(cache_path, "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            __import__("logging").getLogger(__name__).info(
                f"[_dispatch] pickle缓存已保存: {len(engines)} 个引擎 → {cache_path} (版本 {self.PICKLE_CACHE_VERSION})"
            )
            return True
        except Exception as e:
            __import__("logging").getLogger(__name__).warning(
                f"[_dispatch] pickle缓存保存失败: {e}"
            )
            return False

    def _get_engine(self, school: WisdomSchool, force_retry: bool = False):
        """
        获取学派引擎实例（懒加载）[v10.1 重试优化]

        支持冷却重试：引擎加载失败后，经过 _failure_cooldown 秒后可重新尝试加载。
        配合 prewarm_all_engines() 预热机制，在系统空闲时重试失败的引擎。

        Args:
            school: 智慧学派
            force_retry: 强制重试（忽略冷却期，用于预热时重试失败引擎）
        """
        if school in self._engines:
            return self._engines[school]

        # [v10.1] 冷却检查：冷却期内不重试，避免对故障服务持续打隔
        if school in self._failed_engines and not force_retry:
            failed_at = self._failed_timestamps.get(school, 0)
            if (time.time() - failed_at) < self._failure_cooldown:
                return None
            # 冷却期已过，清除失败标记，允许重试
            self._failed_engines.discard(school)
            self._failed_timestamps.pop(school, None)

        reg = self._engine_registry.get(school)
        if not reg:
            return None
        with self._engine_lock:
            if school in self._engines:
                return self._engines[school]
            if school in self._failed_engines and not force_retry:
                return None
            try:
                from importlib import import_module
                # 统一从 src.intelligence 加载: reg[0] 格式为 "engines.xxx" 或 "reasoning.xxx"
                module = import_module(f"src.intelligence.{reg[0]}")
                engine_cls = getattr(module, reg[1])
                self._engines[school] = engine_cls()
                # 加载成功后清除失败记录
                self._failed_engines.discard(school)
                self._failed_timestamps.pop(school, None)
                return self._engines[school]
            except Exception:
                self._failed_engines.add(school)
                self._failed_timestamps[school] = time.time()
                return None

    def _build_mapping_matrix(self) -> Dict[ProblemType, List[Tuple[WisdomSchool, float]]]:
        """构建问题类型到智慧学派的mapping矩阵"""
        return {
            # 儒家
            ProblemType.ETHICAL: [(WisdomSchool.CONFUCIAN, 0.9), (WisdomSchool.SUFU, 0.5), (WisdomSchool.BUDDHIST, 0.3)],
            ProblemType.GOVERNANCE: [(WisdomSchool.CONFUCIAN, 0.85), (WisdomSchool.SUFU, 0.45), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.TALENT: [(WisdomSchool.SUFU, 0.9), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.BUDDHIST, 0.3)],
            ProblemType.CULTURE: [(WisdomSchool.CONFUCIAN, 0.9), (WisdomSchool.DAOIST, 0.4), (WisdomSchool.BUDDHIST, 0.3)],
            # 道家
            ProblemType.STRATEGY: [(WisdomSchool.DAOIST, 0.85), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.MILITARY, 0.4)],
            ProblemType.CRISIS: [(WisdomSchool.DAOIST, 0.9), (WisdomSchool.MILITARY, 0.5), (WisdomSchool.BUDDHIST, 0.4)],
            ProblemType.CHANGE: [(WisdomSchool.DAOIST, 0.85), (WisdomSchool.CONFUCIAN, 0.4), (WisdomSchool.SUFU, 0.3)],
            ProblemType.BALANCE: [(WisdomSchool.DAOIST, 0.95), (WisdomSchool.METAPHYSICS, 0.7), (WisdomSchool.CONFUCIAN, 0.4)],
            ProblemType.TIMING: [(WisdomSchool.METAPHYSICS, 0.92), (WisdomSchool.DAOIST, 0.65), (WisdomSchool.LVSHI, 0.45)],
            ProblemType.ENVIRONMENT: [(WisdomSchool.METAPHYSICS, 0.95), (WisdomSchool.DAOIST, 0.55), (WisdomSchool.CONFUCIAN, 0.25)],
            ProblemType.PATTERN: [(WisdomSchool.METAPHYSICS, 0.9), (WisdomSchool.DAOIST, 0.55), (WisdomSchool.GROWTH, 0.3)],
            # 佛家
            ProblemType.MINDSET: [(WisdomSchool.BUDDHIST, 0.9), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.CONFUCIAN, 0.3)],
            ProblemType.HARMONY: [(WisdomSchool.BUDDHIST, 0.85), (WisdomSchool.CONFUCIAN, 0.6), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.INTEREST: [(WisdomSchool.BUDDHIST, 0.8), (WisdomSchool.CONFUCIAN, 0.6), (WisdomSchool.MILITARY, 0.4)],
            ProblemType.LONGTERM: [(WisdomSchool.BUDDHIST, 0.85), (WisdomSchool.CONFUCIAN, 0.4), (WisdomSchool.DAOIST, 0.45)],
            # 素书
            ProblemType.LEADERSHIP: [(WisdomSchool.SUFU, 0.9), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.RISK: [(WisdomSchool.SUFU, 0.9), (WisdomSchool.MILITARY, 0.5), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.FORTUNE: [(WisdomSchool.SUFU, 0.9), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.BUDDHIST, 0.3)],
            ProblemType.PERSONNEL: [(WisdomSchool.SUFU, 0.9), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.BUDDHIST, 0.3)],
            # 兵法
            ProblemType.COMPETITION: [(WisdomSchool.MILITARY, 0.9), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.SUFU, 0.4)],
            ProblemType.ATTACK: [(WisdomSchool.MILITARY, 0.9), (WisdomSchool.DAOIST, 0.4), (WisdomSchool.CONFUCIAN, 0.3)],
            ProblemType.DEFENSE: [(WisdomSchool.MILITARY, 0.85), (WisdomSchool.DAOIST, 0.6), (WisdomSchool.SUFU, 0.4)],
            ProblemType.NEGOTIATION: [(WisdomSchool.MILITARY, 0.7), (WisdomSchool.ZONGHENG, 0.8), (WisdomSchool.DAOIST, 0.5)],
            ProblemType.WAR_ECONOMY_NEXUS: [(WisdomSchool.MILITARY, 0.88), (WisdomSchool.CONFUCIAN, 0.55), (WisdomSchool.LVSHI, 0.4)],
            ProblemType.STATE_CAPACITY: [(WisdomSchool.CONFUCIAN, 0.86), (WisdomSchool.SUFU, 0.52), (WisdomSchool.LVSHI, 0.45)],
            ProblemType.INSTITUTIONAL_SEDIMENTATION: [(WisdomSchool.CONFUCIAN, 0.82), (WisdomSchool.LVSHI, 0.56), (WisdomSchool.DAOIST, 0.36)],
            # 吕氏春秋
            ProblemType.PUBLIC_INTEREST: [(WisdomSchool.LVSHI, 0.9), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.SUFU, 0.4)],
            ProblemType.SEASONAL: [(WisdomSchool.LVSHI, 0.85), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.CONFUCIAN, 0.3)],
            ProblemType.YINYANG: [(WisdomSchool.LVSHI, 0.9), (WisdomSchool.DAOIST, 0.8), (WisdomSchool.CONFUCIAN, 0.4)],
            # 科幻思维
            ProblemType.DIMENSION: [(WisdomSchool.SCI_FI, 0.9), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.MILITARY, 0.4)],
            ProblemType.SURVIVAL: [(WisdomSchool.SCI_FI, 0.85), (WisdomSchool.MILITARY, 0.5), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.SCALE: [(WisdomSchool.SCI_FI, 0.9), (WisdomSchool.CONFUCIAN, 0.4), (WisdomSchool.LVSHI, 0.3)],
            # 成长思维
            ProblemType.GROWTH_MINDSET: [(WisdomSchool.GROWTH, 0.9), (WisdomSchool.CONFUCIAN, 0.4), (WisdomSchool.SUFU, 0.3)],
            ProblemType.REVERSE: [(WisdomSchool.GROWTH, 0.9), (WisdomSchool.MILITARY, 0.5), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.CLOSED_LOOP: [(WisdomSchool.GROWTH, 0.9), (WisdomSchool.SUFU, 0.5), (WisdomSchool.CONFUCIAN, 0.3)],
            # 神话智慧
            ProblemType.CREATION_MYTH: [(WisdomSchool.MYTHOLOGY, 0.9), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.BUDDHIST, 0.3)],
            ProblemType.APOCALYPSE: [(WisdomSchool.MYTHOLOGY, 0.9), (WisdomSchool.MILITARY, 0.5), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.CYCLICAL: [(WisdomSchool.MYTHOLOGY, 0.9), (WisdomSchool.DAOIST, 0.7), (WisdomSchool.METAPHYSICS, 0.5)],
            # 文学叙事
            ProblemType.NARRATIVE: [(WisdomSchool.LITERARY, 0.9), (WisdomSchool.CONFUCIAN, 0.4), (WisdomSchool.DAOIST, 0.3)],
            ProblemType.RESILIENCE: [(WisdomSchool.LITERARY, 0.9), (WisdomSchool.BUDDHIST, 0.5), (WisdomSchool.CONFUCIAN, 0.4)],
            ProblemType.CHARACTER: [(WisdomSchool.LITERARY, 0.9), (WisdomSchool.CONFUCIAN, 0.4), (WisdomSchool.BUDDHIST, 0.3)],
            # 人类学
            ProblemType.CROSS_CULTURE: [(WisdomSchool.ANTHROPOLOGY, 0.9), (WisdomSchool.HONGMING, 0.5), (WisdomSchool.CONFUCIAN, 0.4)],
            ProblemType.RITUAL: [(WisdomSchool.ANTHROPOLOGY, 0.9), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.DAOIST, 0.3)],
            ProblemType.CULTURAL_CHANGE: [(WisdomSchool.ANTHROPOLOGY, 0.9), (WisdomSchool.CIVILIZATION, 0.6), (WisdomSchool.MYTHOLOGY, 0.4)],
            # 行为塑造
            ProblemType.HABIT: [(WisdomSchool.BEHAVIOR, 0.9), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.DAOIST, 0.3)],
            ProblemType.WILLPOWER: [(WisdomSchool.BEHAVIOR, 0.9), (WisdomSchool.BUDDHIST, 0.5), (WisdomSchool.CONFUCIAN, 0.3)],
            ProblemType.NUDGE: [(WisdomSchool.BEHAVIOR, 0.9), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.MILITARY, 0.3)],
            # 科学思维
            ProblemType.SCIENTIFIC_METHOD: [(WisdomSchool.SCIENCE, 0.9), (WisdomSchool.MILITARY, 0.4), (WisdomSchool.CONFUCIAN, 0.3)],
            ProblemType.SYSTEM_THINKING: [(WisdomSchool.SCIENCE, 0.9), (WisdomSchool.DAOIST, 0.6), (WisdomSchool.METAPHYSICS, 0.4)],
            ProblemType.EVIDENCE: [(WisdomSchool.SCIENCE, 0.9), (WisdomSchool.CONFUCIAN, 0.4), (WisdomSchool.MILITARY, 0.3)],
            # 社会科学
            ProblemType.MARKETING: [(WisdomSchool.SOCIAL_SCIENCE, 0.9), (WisdomSchool.BEHAVIOR, 0.5), (WisdomSchool.LITERARY, 0.3)],
            ProblemType.MARKET_ANALYSIS: [(WisdomSchool.SOCIAL_SCIENCE, 0.9), (WisdomSchool.SCIENCE, 0.4), (WisdomSchool.MILITARY, 0.3)],
            ProblemType.SOCIAL_DEVELOPMENT: [(WisdomSchool.SOCIAL_SCIENCE, 0.9), (WisdomSchool.ANTHROPOLOGY, 0.5), (WisdomSchool.CIVILIZATION, 0.35)],
            # v3.2 营销战略首位
            ProblemType.CONSUMER_MARKETING: [(WisdomSchool.CHINESE_CONSUMER, 0.95), (WisdomSchool.BEHAVIOR, 0.9), (WisdomSchool.SOCIAL_SCIENCE, 0.7)],
            ProblemType.BRAND_STRATEGY: [(WisdomSchool.CHINESE_CONSUMER, 0.9), (WisdomSchool.LITERARY, 0.8), (WisdomSchool.BEHAVIOR, 0.7)],
            ProblemType.SOCIAL_STABILITY: [(WisdomSchool.SOCIAL_SCIENCE, 0.9), (WisdomSchool.CONFUCIAN, 0.7), (WisdomSchool.DAOIST, 0.5)],
            ProblemType.PSYCHOLOGICAL_INSIGHT: [(WisdomSchool.BEHAVIOR, 0.95), (WisdomSchool.CHINESE_CONSUMER, 0.8), (WisdomSchool.SOCIAL_SCIENCE, 0.6)],
            # 自然科学
            ProblemType.PHYSICS_ANALYSIS: [(WisdomSchool.NATURAL_SCIENCE, 0.95), (WisdomSchool.SCIENCE, 0.6), (WisdomSchool.SCI_FI, 0.4)],
            ProblemType.LIFE_SCIENCE: [(WisdomSchool.NATURAL_SCIENCE, 0.95), (WisdomSchool.SCIENCE, 0.6), (WisdomSchool.DAOIST, 0.3)],
            ProblemType.EARTH_SYSTEM: [(WisdomSchool.NATURAL_SCIENCE, 0.95), (WisdomSchool.METAPHYSICS, 0.5), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.COSMOS_EXPLORATION: [(WisdomSchool.NATURAL_SCIENCE, 0.95), (WisdomSchool.SCI_FI, 0.7), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.SCALE_CROSSING: [(WisdomSchool.NATURAL_SCIENCE, 0.9), (WisdomSchool.SCI_FI, 0.6), (WisdomSchool.DAOIST, 0.5)],
            # WCC智慧演化
            ProblemType.META_PERSPECTIVE: [(WisdomSchool.WCC, 0.9), (WisdomSchool.NATURAL_SCIENCE, 0.6), (WisdomSchool.SCI_FI, 0.4)],
            ProblemType.CIVILIZATION_ANALYSIS: [(WisdomSchool.WCC, 0.9), (WisdomSchool.CIVILIZATION, 0.8), (WisdomSchool.CIV_WAR_ECONOMY, 0.5)],
            ProblemType.COSMIC_COGNITION: [(WisdomSchool.WCC, 0.9), (WisdomSchool.NATURAL_SCIENCE, 0.8), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.SCALE_TRANSFORMATION: [(WisdomSchool.WCC, 0.9), (WisdomSchool.NATURAL_SCIENCE, 0.7), (WisdomSchool.SCI_FI, 0.5)],
            ProblemType.WORLDVIEW_SHIFT: [(WisdomSchool.WCC, 0.9), (WisdomSchool.NATURAL_SCIENCE, 0.6), (WisdomSchool.DEWEY, 0.4)],
            ProblemType.WISDOM_EVOLUTION: [(WisdomSchool.WCC, 0.9), (WisdomSchool.CIVILIZATION, 0.7), (WisdomSchool.NATURAL_SCIENCE, 0.6)],
            ProblemType.TECH_EVOLUTION: [(WisdomSchool.WCC, 0.9), (WisdomSchool.CIVILIZATION, 0.7), (WisdomSchool.NATURAL_SCIENCE, 0.5)],
            # 历史思想三维度
            ProblemType.HISTORICAL_ANALYSIS: [(WisdomSchool.HISTORICAL_THOUGHT, 0.95), (WisdomSchool.CIVILIZATION, 0.7), (WisdomSchool.WCC, 0.6)],
            ProblemType.THOUGHT_EVOLUTION: [(WisdomSchool.HISTORICAL_THOUGHT, 0.95), (WisdomSchool.CIVILIZATION, 0.6), (WisdomSchool.SCIENCE, 0.5)],
            ProblemType.ECONOMIC_EVOLUTION: [(WisdomSchool.HISTORICAL_THOUGHT, 0.95), (WisdomSchool.CIV_WAR_ECONOMY, 0.7), (WisdomSchool.CIVILIZATION, 0.5)],
            ProblemType.TECH_HISTORY: [(WisdomSchool.HISTORICAL_THOUGHT, 0.95), (WisdomSchool.WCC, 0.6), (WisdomSchool.NATURAL_SCIENCE, 0.5)],
            ProblemType.CROSS_DIMENSION: [(WisdomSchool.HISTORICAL_THOUGHT, 0.95), (WisdomSchool.WCC, 0.6), (WisdomSchool.NATURAL_SCIENCE, 0.5)],
            ProblemType.PARADIGM_SHIFT: [(WisdomSchool.HISTORICAL_THOUGHT, 0.95), (WisdomSchool.WCC, 0.7), (WisdomSchool.SCIENCE, 0.6)],
            # ── V6.0 第二阶段: 心理学ProblemType ──
            ProblemType.PERSONALITY_ANALYSIS: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.YANGMING, 0.5), (WisdomSchool.BEHAVIOR, 0.5)],
            ProblemType.GROUP_DYNAMICS: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.COGNITIVE_BIAS: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.BEHAVIOR, 0.5), (WisdomSchool.SCIENCE, 0.4)],
            ProblemType.MOTIVATION_ANALYSIS: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.BEHAVIOR, 0.6), (WisdomSchool.DAOIST, 0.3)],
            ProblemType.PSYCHOLOGICAL_ARITHMETIC: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.NATURAL_SCIENCE, 0.5), (WisdomSchool.SCIENCE, 0.4)],
            ProblemType.TRAUMA_HEALING: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.BUDDHIST, 0.6), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.SELF_ACTUALIZATION: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.BUDDHIST, 0.5), (WisdomSchool.GROWTH, 0.4)],
            ProblemType.INTERPERSONAL_RELATIONSHIP: [(WisdomSchool.PSYCHOLOGY, 0.9), (WisdomSchool.CONFUCIAN, 0.6), (WisdomSchool.BUDDHIST, 0.3)],
            # ── V6.0 第二阶段: 系统论ProblemType ──
            ProblemType.COMPLEX_SYSTEM: [(WisdomSchool.SYSTEMS, 0.9), (WisdomSchool.COMPLEXITY, 0.7), (WisdomSchool.DAOIST, 0.5)],
            ProblemType.FEEDBACK_LOOP: [(WisdomSchool.SYSTEMS, 0.9), (WisdomSchool.SCIENCE, 0.5), (WisdomSchool.GROWTH, 0.4)],
            ProblemType.EMERGENT_BEHAVIOR: [(WisdomSchool.SYSTEMS, 0.9), (WisdomSchool.DAOIST, 0.6), (WisdomSchool.SCI_FI, 0.3)],
            ProblemType.SYSTEM_EQUILIBRIUM: [(WisdomSchool.SYSTEMS, 0.9), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.METAPHYSICS, 0.4)],
            ProblemType.ADAPTIVE_SYSTEM: [(WisdomSchool.SYSTEMS, 0.9), (WisdomSchool.GROWTH, 0.5), (WisdomSchool.SCIENCE, 0.3)],
            # ── V6.0 第二阶段: 管理学ProblemType ──
            ProblemType.STRATEGIC_PLANNING: [(WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.MILITARY, 0.4)],
            ProblemType.ORGANIZATIONAL_DESIGN: [(WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.FAJIA, 0.5), (WisdomSchool.CONFUCIAN, 0.3)],
            ProblemType.PERFORMANCE_MANAGEMENT: [(WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.FAJIA, 0.4), (WisdomSchool.SUFU, 0.3)],
            ProblemType.KNOWLEDGE_MANAGEMENT: [(WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.GROWTH, 0.5), (WisdomSchool.CONFUCIAN, 0.3)],
            ProblemType.CHANGE_MANAGEMENT: [(WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.CONFUCIAN, 0.3)],
            ProblemType.INNOVATION_MANAGEMENT: [(WisdomSchool.MANAGEMENT, 0.9), (WisdomSchool.SCI_FI, 0.4), (WisdomSchool.GROWTH, 0.4)],
            # ── V6.0 第二阶段: 纵横家ProblemType ──
            ProblemType.DIPLOMATIC_NEGOTIATION: [(WisdomSchool.ZONGHENG, 0.9), (WisdomSchool.MILITARY, 0.6), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.ALLIANCE_BUILDING: [(WisdomSchool.ZONGHENG, 0.9), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.POWER_BALANCE: [(WisdomSchool.ZONGHENG, 0.9), (WisdomSchool.FAJIA, 0.5), (WisdomSchool.DAOIST, 0.4)],
            # ── V6.0 第三阶段: 墨家ProblemType ──
            ProblemType.ENGINEERING_INNOVATION: [
                (WisdomSchool.MOZI, 0.9), (WisdomSchool.SCIENCE, 0.6), (WisdomSchool.NATURAL_SCIENCE, 0.4)],
            ProblemType.COST_OPTIMIZATION: [
                (WisdomSchool.MOZI, 0.9), (WisdomSchool.SUFU, 0.5), (WisdomSchool.MANAGEMENT, 0.4)],
            ProblemType.UNIVERSAL_BENEFIT: [
                (WisdomSchool.MOZI, 0.9), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.BUDDHIST, 0.4)],
            ProblemType.DEFENSE_FORTIFICATION: [
                (WisdomSchool.MOZI, 0.9), (WisdomSchool.MILITARY, 0.6), (WisdomSchool.SCIENCE, 0.4)],
            ProblemType.LOGICAL_DEDUCTION: [
                (WisdomSchool.MOZI, 0.9), (WisdomSchool.SCIENCE, 0.6), (WisdomSchool.TOP_METHODS, 0.4)],
            # ── V6.0 第三阶段: 法家ProblemType ──
            ProblemType.INSTITUTIONAL_DESIGN: [
                (WisdomSchool.FAJIA, 0.9), (WisdomSchool.CONFUCIAN, 0.5), (WisdomSchool.MANAGEMENT, 0.4)],
            ProblemType.LAW_ENFORCEMENT: [
                (WisdomSchool.FAJIA, 0.9), (WisdomSchool.SUFU, 0.5), (WisdomSchool.MILITARY, 0.3)],
            ProblemType.POWER_STRUCTURING: [
                (WisdomSchool.FAJIA, 0.9), (WisdomSchool.ZONGHENG, 0.5), (WisdomSchool.CONFUCIAN, 0.3)],
            ProblemType.REWARD_PUNISHMENT: [
                (WisdomSchool.FAJIA, 0.9), (WisdomSchool.SUFU, 0.6), (WisdomSchool.CONFUCIAN, 0.3)],
            ProblemType.HUMAN_NATURE_ANALYSIS: [
                (WisdomSchool.FAJIA, 0.9), (WisdomSchool.PSYCHOLOGY, 0.5), (WisdomSchool.BEHAVIOR, 0.4)],
            ProblemType.STATE_CONSOLIDATION: [
                (WisdomSchool.FAJIA, 0.9), (WisdomSchool.MILITARY, 0.5), (WisdomSchool.CONFUCIAN, 0.4)],
            # ── V6.0 第三阶段: 经济学ProblemType ──
            ProblemType.RESOURCE_ALLOCATION: [(WisdomSchool.ECONOMICS, 0.9), (WisdomSchool.SOCIAL_SCIENCE, 0.6), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.SUPPLY_DEMAND_BALANCE: [(WisdomSchool.ECONOMICS, 0.95), (WisdomSchool.SOCIAL_SCIENCE, 0.7), (WisdomSchool.MILITARY, 0.5)],
            ProblemType.ECONOMIC_INCENTIVE: [(WisdomSchool.ECONOMICS, 0.95), (WisdomSchool.BEHAVIOR, 0.7), (WisdomSchool.SOCIAL_SCIENCE, 0.6)],
            ProblemType.MARKET_EFFICIENCY: [(WisdomSchool.ECONOMICS, 0.95), (WisdomSchool.SOCIAL_SCIENCE, 0.7), (WisdomSchool.SCIENCE, 0.5)],
            ProblemType.INVESTMENT_DECISION: [(WisdomSchool.ECONOMICS, 0.95), (WisdomSchool.SUFU, 0.7), (WisdomSchool.MILITARY, 0.5)],
            # ── V6.0 第三阶段: 名家ProblemType ──
            ProblemType.LOGICAL_PARADOX: [(WisdomSchool.MINGJIA, 0.95), (WisdomSchool.DAOIST, 0.6), (WisdomSchool.SCIENCE, 0.4)],
            ProblemType.CLASSIFICATION_REFINEMENT: [(WisdomSchool.MINGJIA, 0.95), (WisdomSchool.CONFUCIAN, 0.6), (WisdomSchool.SCIENCE, 0.4)],
            ProblemType.DIALECTICAL_REASONING: [(WisdomSchool.MINGJIA, 0.95), (WisdomSchool.DAOIST, 0.7), (WisdomSchool.MILITARY, 0.5)],
            # ── V6.0 第三阶段: 阴阳家ProblemType ──
            ProblemType.WUXING_ANALYSIS: [(WisdomSchool.WUXING, 0.9), (WisdomSchool.METAPHYSICS, 0.7), (WisdomSchool.DAOIST, 0.5)],
            ProblemType.YINYANG_DIALECTICS: [(WisdomSchool.WUXING, 0.95), (WisdomSchool.DAOIST, 0.8), (WisdomSchool.METAPHYSICS, 0.6)],
            ProblemType.SEASONAL_RHYTHM: [(WisdomSchool.WUXING, 0.95), (WisdomSchool.LVSHI, 0.7), (WisdomSchool.METAPHYSICS, 0.6)],
            ProblemType.COSMIC_HARMONY: [(WisdomSchool.WUXING, 0.95), (WisdomSchool.DAOIST, 0.8), (WisdomSchool.METAPHYSICS, 0.6)],
            ProblemType.CYCLICAL_TRANSFORMATION: [(WisdomSchool.WUXING, 0.95), (WisdomSchool.METAPHYSICS, 0.8), (WisdomSchool.DAOIST, 0.7)],
            # ── V6.0 第三阶段: 复杂性科学ProblemType ──
            ProblemType.EMERGENT_ORDER: [(WisdomSchool.COMPLEXITY, 0.9), (WisdomSchool.SYSTEMS, 0.6), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.NETWORK_DYNAMICS: [(WisdomSchool.COMPLEXITY, 0.95), (WisdomSchool.SOCIAL_SCIENCE, 0.7), (WisdomSchool.SCIENCE, 0.6)],
            # ── V6.0 精细优化: 学派子领域细分ProblemType ──
            ProblemType.CONFUCIAN_SUB_SCHOOL: [(WisdomSchool.CONFUCIAN, 0.95), (WisdomSchool.YANGMING, 0.7), (WisdomSchool.DAOIST, 0.3)],
            ProblemType.DAOIST_SUB_SCHOOL: [(WisdomSchool.DAOIST, 0.95), (WisdomSchool.METAPHYSICS, 0.6), (WisdomSchool.BUDDHIST, 0.4)],
            ProblemType.BUDDHIST_SUB_SCHOOL: [(WisdomSchool.BUDDHIST, 0.95), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.CONFUCIAN, 0.3)],
            ProblemType.MILITARY_SUB_SCHOOL: [(WisdomSchool.MILITARY, 0.95), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.FAJIA, 0.4)],
            ProblemType.TALENT_PIPELINE: [(WisdomSchool.CONFUCIAN, 0.85), (WisdomSchool.SUFU, 0.7), (WisdomSchool.YANGMING, 0.5)],
            ProblemType.ORGANIZATIONAL_CULTURE: [(WisdomSchool.CONFUCIAN, 0.8), (WisdomSchool.DAOIST, 0.5), (WisdomSchool.PSYCHOLOGY, 0.4)],
            ProblemType.BRAND_CULTURE: [(WisdomSchool.CHINESE_CONSUMER, 0.9), (WisdomSchool.LITERARY, 0.7), (WisdomSchool.CONFUCIAN, 0.5)],
            ProblemType.PHILOSOPHY_OF_MIND: [(WisdomSchool.YANGMING, 0.95), (WisdomSchool.CONFUCIAN, 0.7), (WisdomSchool.BUDDHIST, 0.5)],
            ProblemType.DECISION_FRAMEWORK: [(WisdomSchool.TOP_METHODS, 0.85), (WisdomSchool.SCIENCE, 0.6), (WisdomSchool.CONFUCIAN, 0.5)],
            ProblemType.RESOURCE_ECOLOGY: [(WisdomSchool.ECONOMICS, 0.85), (WisdomSchool.DAOIST, 0.6), (WisdomSchool.SYSTEMS, 0.5)],
            ProblemType.INNOVATION_ECOLOGY: [(WisdomSchool.MANAGEMENT, 0.85), (WisdomSchool.SCI_FI, 0.6), (WisdomSchool.MOZI, 0.5)],
            ProblemType.ADAPTIVE_EVOLUTION: [(WisdomSchool.COMPLEXITY, 0.9), (WisdomSchool.SYSTEMS, 0.6), (WisdomSchool.DAOIST, 0.4)],
            # ── V6.2 社会科学智慧版: 社会学ProblemType ──
            ProblemType.SOCIAL_STRUCTURE_ANALYSIS: [(WisdomSchool.SOCIOLOGY, 0.95), (WisdomSchool.POLITICAL_ECONOMICS, 0.6), (WisdomSchool.CONFUCIAN, 0.4)],
            ProblemType.CLASS_MOBILITY: [(WisdomSchool.SOCIOLOGY, 0.9), (WisdomSchool.POLITICAL_ECONOMICS, 0.7), (WisdomSchool.ECONOMICS, 0.5)],
            ProblemType.INSTITUTIONAL_SOCIOLOGY: [(WisdomSchool.SOCIOLOGY, 0.9), (WisdomSchool.POLITICAL_ECONOMICS, 0.7), (WisdomSchool.FAJIA, 0.5)],
            ProblemType.SOCIAL_STRATIFICATION: [(WisdomSchool.SOCIOLOGY, 0.95), (WisdomSchool.POLITICAL_ECONOMICS, 0.6), (WisdomSchool.ECONOMICS, 0.5)],
            ProblemType.COLLECTIVE_ACTION: [(WisdomSchool.SOCIOLOGY, 0.9), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.7), (WisdomSchool.PSYCHOLOGY, 0.5)],
            # ── V6.2 社会科学智慧版: 行为经济学ProblemType ──
            ProblemType.COGNITIVE_BIAS_V62: [(WisdomSchool.BEHAVIORAL_ECONOMICS, 0.95), (WisdomSchool.PSYCHOLOGY, 0.7), (WisdomSchool.BEHAVIOR, 0.5)],
            ProblemType.DECISION_MAKING_BEHAVIOR: [(WisdomSchool.BEHAVIORAL_ECONOMICS, 0.9), (WisdomSchool.PSYCHOLOGY, 0.6), (WisdomSchool.MILITARY, 0.4)],
            ProblemType.MARKET_BEHAVIOR: [(WisdomSchool.BEHAVIORAL_ECONOMICS, 0.9), (WisdomSchool.ECONOMICS, 0.7), (WisdomSchool.SOCIAL_SCIENCE, 0.5)],
            ProblemType.INCENTIVE_DESIGN: [(WisdomSchool.BEHAVIORAL_ECONOMICS, 0.9), (WisdomSchool.ECONOMICS, 0.7), (WisdomSchool.FAJIA, 0.5)],
            ProblemType.NUDGE_POLICY: [(WisdomSchool.BEHAVIORAL_ECONOMICS, 0.95), (WisdomSchool.BEHAVIOR, 0.7), (WisdomSchool.POLITICAL_ECONOMICS, 0.5)],
            # ── V6.2 社会科学智慧版: 传播学ProblemType ──
            ProblemType.MEDIA_EFFECT: [(WisdomSchool.COMMUNICATION, 0.95), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.6), (WisdomSchool.SOCIOLOGY, 0.5)],
            ProblemType.PUBLIC_OPINION_FORMATION: [(WisdomSchool.COMMUNICATION, 0.9), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.7), (WisdomSchool.SOCIOLOGY, 0.5)],
            ProblemType.INFORMATION_CASCADE: [(WisdomSchool.COMMUNICATION, 0.9), (WisdomSchool.BEHAVIORAL_ECONOMICS, 0.6), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.5)],
            ProblemType.DISCOURSE_ANALYSIS: [(WisdomSchool.COMMUNICATION, 0.9), (WisdomSchool.SOCIOLOGY, 0.6), (WisdomSchool.POLITICAL_ECONOMICS, 0.4)],
            ProblemType.INTERPERSONAL_COMMUNICATION: [(WisdomSchool.COMMUNICATION, 0.9), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.7), (WisdomSchool.PSYCHOLOGY, 0.5)],
            # ── V6.2 社会科学智慧版: 文化人类学ProblemType ──
            ProblemType.CULTURAL_PATTERN_RECOGNITION: [(WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.95), (WisdomSchool.ANTHROPOLOGY, 0.7), (WisdomSchool.SOCIOLOGY, 0.5)],
            ProblemType.SYMBOL_SYSTEM_ANALYSIS: [(WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.9), (WisdomSchool.COMMUNICATION, 0.6), (WisdomSchool.SOCIAL_SCIENCE, 0.5)],
            ProblemType.RITUAL_CONTEXT_ANALYSIS: [(WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.9), (WisdomSchool.ANTHROPOLOGY, 0.7), (WisdomSchool.SOCIOLOGY, 0.5)],
            ProblemType.CROSS_CULTURAL_ADAPTATION: [(WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.95), (WisdomSchool.ANTHROPOLOGY, 0.7), (WisdomSchool.SOCIOLOGY, 0.6)],
            # ── V6.2 社会科学智慧版: 政治经济学ProblemType ──
            ProblemType.INSTITUTIONAL_POLITICAL_ANALYSIS: [(WisdomSchool.POLITICAL_ECONOMICS, 0.95), (WisdomSchool.SOCIOLOGY, 0.6), (WisdomSchool.FAJIA, 0.5)],
            ProblemType.POLICY_GAME_THEORY: [(WisdomSchool.POLITICAL_ECONOMICS, 0.9), (WisdomSchool.MILITARY, 0.7), (WisdomSchool.ECONOMICS, 0.5)],
            ProblemType.MARKET_REGULATION_ANALYSIS: [(WisdomSchool.POLITICAL_ECONOMICS, 0.9), (WisdomSchool.ECONOMICS, 0.7), (WisdomSchool.FAJIA, 0.5)],
            ProblemType.PUBLIC_CHOICE: [(WisdomSchool.POLITICAL_ECONOMICS, 0.9), (WisdomSchool.ECONOMICS, 0.7), (WisdomSchool.SOCIOLOGY, 0.5)],
            # ── V6.2 社会科学智慧版: 组织心理学ProblemType ──
            ProblemType.ORGANIZATIONAL_CHANGE_V62: [(WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.95), (WisdomSchool.MANAGEMENT, 0.6), (WisdomSchool.DAOIST, 0.4)],
            ProblemType.LEADERSHIP_STYLE_ANALYSIS: [(WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.9), (WisdomSchool.MANAGEMENT, 0.7), (WisdomSchool.SUFU, 0.5)],
            ProblemType.TEAM_COHESION_ANALYSIS: [(WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.9), (WisdomSchool.SOCIAL_PSYCHOLOGY, 0.7), (WisdomSchool.PSYCHOLOGY, 0.5)],
            ProblemType.ORGANIZATIONAL_CULTURE_V62: [(WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.9), (WisdomSchool.CULTURAL_ANTHROPOLOGY, 0.6), (WisdomSchool.MANAGEMENT, 0.5)],
            # ── V6.2 社会科学智慧版: 社会心理学ProblemType ──
            ProblemType.CONFORMITY_BEHAVIOR: [(WisdomSchool.SOCIAL_PSYCHOLOGY, 0.95), (WisdomSchool.SOCIOLOGY, 0.6), (WisdomSchool.PSYCHOLOGY, 0.5)],
            ProblemType.AUTHORITY_OBEDIENCE: [(WisdomSchool.SOCIAL_PSYCHOLOGY, 0.95), (WisdomSchool.PSYCHOLOGY, 0.6), (WisdomSchool.SOCIOLOGY, 0.5)],
            ProblemType.SOCIAL_INFLUENCE_MECHANISM: [(WisdomSchool.SOCIAL_PSYCHOLOGY, 0.9), (WisdomSchool.COMMUNICATION, 0.6), (WisdomSchool.SOCIOLOGY, 0.5)],
            ProblemType.GROUP_THINK_ANALYSIS: [(WisdomSchool.SOCIAL_PSYCHOLOGY, 0.9), (WisdomSchool.ORGANIZATIONAL_PSYCHOLOGY, 0.7), (WisdomSchool.MANAGEMENT, 0.5)],
        }

    def _build_subschool_mapping(self) -> Dict[ProblemType, List[Tuple[SubSchool, float]]]:
        """构建问题类型到子学派的精细映射矩阵 V6.0.1"""
        return {
            # 儒家子学派映射
            ProblemType.CONFUCIAN_SUB_SCHOOL: [
                (SubSchool.MENCIUS, 0.9), (SubSchool.XUNZI, 0.8),
                (SubSchool.NEO_CONFUCIAN, 0.7), (SubSchool.CLASSICAL, 0.6)],
            ProblemType.ETHICAL: [
                (SubSchool.MENCIUS, 0.9), (SubSchool.CLASSICAL, 0.8), (SubSchool.NEO_CONFUCIAN, 0.6)],
            ProblemType.GOVERNANCE: [
                (SubSchool.XUNZI, 0.9), (SubSchool.CLASSICAL, 0.8), (SubSchool.NEO_CONFUCIAN, 0.5)],
            ProblemType.TALENT: [
                (SubSchool.MENCIUS, 0.7), (SubSchool.XUNZI, 0.8), (SubSchool.CLASSICAL, 0.6)],
            ProblemType.CULTURE: [
                (SubSchool.CLASSICAL, 0.9), (SubSchool.NEO_CONFUCIAN, 0.7), (SubSchool.MENCIUS, 0.5)],
            ProblemType.ORGANIZATIONAL_CULTURE: [
                (SubSchool.NEO_CONFUCIAN, 0.7), (SubSchool.XUNZI, 0.6), (SubSchool.MENCIUS, 0.5)],
            # 道家子学派映射
            ProblemType.DAOIST_SUB_SCHOOL: [
                (SubSchool.LAOZI, 0.95), (SubSchool.ZHUANGZI, 0.9), (SubSchool.LIEZI, 0.7)],
            ProblemType.STRATEGY: [
                (SubSchool.LAOZI, 0.9), (SubSchool.ZHUANGZI, 0.7), (SubSchool.LIEZI, 0.5)],
            ProblemType.CRISIS: [
                (SubSchool.LAOZI, 0.9), (SubSchool.ZHUANGZI, 0.8), (SubSchool.LIEZI, 0.6)],
            ProblemType.BALANCE: [
                (SubSchool.LAOZI, 0.95), (SubSchool.ZHUANGZI, 0.8), (SubSchool.LIEZI, 0.5)],
            ProblemType.CHANGE: [
                (SubSchool.ZHUANGZI, 0.9), (SubSchool.LAOZI, 0.85), (SubSchool.LIEZI, 0.6)],
            # 佛家子学派映射
            ProblemType.BUDDHIST_SUB_SCHOOL: [
                (SubSchool.CHAN, 0.9), (SubSchool.HUAYAN, 0.7),
                (SubSchool.TIANTAI, 0.6), (SubSchool.PURELAND, 0.5)],
            ProblemType.MINDSET: [
                (SubSchool.CHAN, 0.9), (SubSchool.PURELAND, 0.7), (SubSchool.HUAYAN, 0.5)],
            ProblemType.HARMONY: [
                (SubSchool.CHAN, 0.8), (SubSchool.HUAYAN, 0.7), (SubSchool.TIANTAI, 0.6)],
            ProblemType.LONGTERM: [
                (SubSchool.PURELAND, 0.8), (SubSchool.TIANTAI, 0.7), (SubSchool.HUAYAN, 0.6)],
            # 兵法子学派映射
            ProblemType.MILITARY_SUB_SCHOOL: [
                (SubSchool.SUNZI, 0.95), (SubSchool.WUZI, 0.8), (SubSchool.LIUTAO, 0.7)],
            ProblemType.COMPETITION: [
                (SubSchool.SUNZI, 0.95), (SubSchool.WUZI, 0.6), (SubSchool.LIUTAO, 0.5)],
            ProblemType.ATTACK: [
                (SubSchool.SUNZI, 0.95), (SubSchool.LIUTAO, 0.7), (SubSchool.WUZI, 0.5)],
            ProblemType.DEFENSE: [
                (SubSchool.SUNZI, 0.8), (SubSchool.LIUTAO, 0.9), (SubSchool.WUZI, 0.6)],
            ProblemType.NEGOTIATION: [
                (SubSchool.WUZI, 0.8), (SubSchool.SUNZI, 0.7), (SubSchool.LIUTAO, 0.6)],
        }

    def get_subschool_for_problem(self, problem_type: ProblemType) -> List[Tuple[SubSchool, float]]:
        """获取问题类型对应的子学派及其权重 V6.0.1

        Args:
            problem_type: 问题类型枚举值

        Returns:
            子学派及其权重的列表，按权重降序排列；若无匹配则返回空列表
        """
        return self.subschool_mapping.get(problem_type, [])

    def get_all_subschools_for_school(self, wisdom_school: WisdomSchool) -> List[SubSchool]:
        """获取某学派下的所有子学派 V6.0.1

        Args:
            wisdom_school: 父学派枚举值

        Returns:
            该学派下的所有子学派列表
        """
        return [ss for ss, ws in SUBSCHOOL_PARENT.items() if ws == wisdom_school]

    def resolve_departments(self, problem_type):
        """根据问题类型确定调度部门及其能力组合"""
        return self._resolve_departments(problem_type, self.problem_school_mapping)

    def get_department_routing(self, problem_type):
        """
        获取问题类型的部门路由信息。
        Returns: {
            "primary_department": str,
            "all_departments": [str],
            "routing_detail": str,
            "school_combinations": {dept: [(school, weight)]}
        }
        """
        dispatches = self._resolve_departments(problem_type, self.problem_school_mapping)
        if not dispatches:
            return {
                "primary_department": "吏部",
                "all_departments": ["吏部"],
                "routing_detail": f"默认吏部调度: {problem_type.value}",
                "school_combinations": {},
            }
        result = {
            "primary_department": dispatches[0][0].value,
            "all_departments": [d[0].value for d in dispatches],
            "routing_detail": f"主调度{dispatches[0][0].value}",
            "school_combinations": {},
        }
        for dept, role, schools in dispatches:
            result["school_combinations"][dept.value] = [
                (s.value, w) for s, w in schools
            ]
        if len(dispatches) > 1:
            result["routing_detail"] += f", 联合调度{', '.join(d[0].value for d in dispatches[1:])}"
        return result

    # ── v2.2.0: 道家无为调度方法 ──────────────────────────────────────────

    def set_dispatch_mode(self, mode: WuWeiDispatchMode, config: Optional[WuWeiConfig] = None):
        """
        设置调度模式。

        [道家解读] "无为而治"——选择何种干预程度，本身就是一种道。
        - TASK_MATCHING: 主动匹配，积极干预
        - WUWEI_OBSERVE: 无为观察，最小干预
        - HYBRID_FLOW: 顺势而为，因地制宜
        """
        self.wuwei_mode = mode
        if config is not None:
            self.wuwei_config = config

    def register_passive_response(self, school: WisdomSchool, confidence: float, response_type: str = "natural"):
        """
        [无为模式] 注册被动响应——"水善利万物而不争"。

        当系统处于WUWEI_OBSERVE模式时，各学派模块可调用此方法
        注册其自然产生的响应，而非等待强制激活。

        此方法线程安全，可在多线程环境下调用。

        [道家解读] 响应是"自然流出"而非"被挤压出"——如泉水涌出，
        不争而自至。
        """
        if self.wuwei_mode != WuWeiDispatchMode.WUWEI_OBSERVE:
            return
        if not self._wuwei_observation_active:
            return
        with self._wuwei_lock:
            # 水属性学派响应获得额外权重（水善利万物）
            water_weight = 1.2 if school in self.wuwei_config.water_nature_schools else 1.0
            self._wuwei_responses.append((school, confidence * water_weight, response_type))

    def wuwei_observe(
        self,
        problem_type: ProblemType,
        task_context: Optional[Dict[str, Any]] = None,
        window_ms: Optional[int] = None,
    ) -> WuWeiObservationResult:
        """
        [无为调度核心方法] 观察-等待-顺势分发。

        体现"道法自然"：让系统在窗口期内收集各模块的自然响应，
        基于自然竞争结果进行最终分发，而非立即强制激活多个模块竞争。

        算法流程：
        1. 进入观察期，激活被动响应收集
        2. 等待预设窗口（让各模块自然响应）
        3. 分析收集到的被动响应
        4. 如响应充足，基于自然响应分发
        5. 如响应不足，回退到传统匹配模式

        [道家解读] "致虚极，守静笃，万物并作，吾以观复"——
        在静默中观察，等待自然浮现。

        Args:
            problem_type: 问题类型
            task_context: 任务上下文
            window_ms: 观察窗口（毫秒），覆盖config默认值

        Returns:
            WuWeiObservationResult: 包含观察分析和最终分发结果
        """
        start_time = time.time() * 1000
        window = window_ms or self.wuwei_config.observe_window_ms

        # 步骤1：进入观察期
        with self._wuwei_lock:
            self._wuwei_responses = []
            self._wuwei_observation_active = True
            self._wuwei_observation_start = start_time

        if self.wuwei_config.log_observation:
            _log_wuwei(f"[无为观察] 启动: problem_type={problem_type.value}, window={window}ms")

        # 步骤2：等待窗口期（观察自然响应）
        # 注意：这是轻量级等待，实际应用中可结合异步事件机制
        _sleep_ms = min(window, 200)  # 最多等待200ms以避免阻塞过久
        time.sleep(_sleep_ms / 1000.0)

        # 步骤3：收集响应并退出观察期
        with self._wuwei_lock:
            responses = list(self._wuwei_responses)
            self._wuwei_observation_active = False

        elapsed_ms = time.time() * 1000 - start_time

        # 步骤4：分析响应
        natural_count = len(responses)
        if natural_count > 0:
            # 计算上善若水评分：水属性学派响应的质量加成
            water_responses = [r for r in responses if r[0] in self.wuwei_config.water_nature_schools]
            water_score = len(water_responses) / natural_count if natural_count > 0 else 0.0

            # 阴阳平衡评估：学派多样性
            unique_schools = set(r[0] for r in responses)
            balance_score = min(len(unique_schools) / 3.0, 1.0)  # 3个学派以上视为平衡

            # 自然和谐度
            avg_confidence = sum(r[1] for r in responses) / natural_count
            dao_analysis = (
                f"自然响应{natural_count}个，"
                f"水属性学派占比{water_score:.1%}（上善若水），"
                f"学派多样性{balance_score:.1%}（阴阳平衡），"
                f"平均置信度{avg_confidence:.2f}。"
            )
            if water_score > 0.5:
                dao_analysis += "【大吉】水属性学派主导，自然和谐度高。"
            elif balance_score > 0.6:
                dao_analysis += "【中吉】学派均衡，阴阳调和。"
            else:
                dao_analysis += "【平】响应偏少，顺其自然。"

            balance_assessment = (
                "阴（被动等待）充足" if natural_count >= self.wuwei_config.passive_response_threshold
                else "阴不足，需阳（主动）补充"
            )

            # 步骤5：基于自然响应生成最终分发
            # 按置信度排序，选取前N个学派
            sorted_responses = sorted(responses, key=lambda r: r[1], reverse=True)
            top_schools = sorted_responses[:3]  # 取前3

            # 归一化为分发权重
            total_conf = sum(r[1] for r in top_schools)
            final_dispatch = [
                (school, conf / total_conf) for school, conf, _ in top_schools
            ] if total_conf > 0 else None

            if self.wuwei_config.log_observation:
                _log_wuwei(f"[无为观察] 完成: 响应数={natural_count}, dao_analysis={dao_analysis}")

            return WuWeiObservationResult(
                mode_used=WuWeiDispatchMode.WUWEI_OBSERVE,
                observed_responses=responses,
                final_dispatch=final_dispatch,
                observation_duration_ms=elapsed_ms,
                natural_response_count=natural_count,
                dao_analysis=dao_analysis,
                water_nature_score=water_score,
                balance_assessment=balance_assessment,
            )
        else:
            # 无自然响应，回退到传统匹配模式
            if self.wuwei_config.log_observation:
                _log_wuwei(f"[无为观察] 无响应，回退传统匹配")

            return WuWeiObservationResult(
                mode_used=WuWeiDispatchMode.TASK_MATCHING,
                observed_responses=[],
                final_dispatch=None,  # None表示使用传统分发
                observation_duration_ms=elapsed_ms,
                natural_response_count=0,
                dao_analysis="【无为→有为】无自然响应，道法自然未能启动，回退到传统匹配模式。",
                water_nature_score=0.0,
                balance_assessment="阴（被动）为空，阳（主动）接管",
            )

    def get_dao_wisdom_hint(self, problem_type: ProblemType) -> Dict[str, Any]:
        """
        获取道家智慧提示——"不争，天下莫能与之争"。

        根据问题类型，返回适合的道家学派建议，
        帮助在无为观察模式中选择合适的学派响应。
        """
        # 道家学派主导的问题类型
        dao_dominant_types = {
            ProblemType.DIALECTICAL_REASONING,
            ProblemType.YINYANG_DIALECTICS,
            ProblemType.CYCLICAL_TRANSFORMATION,
            ProblemType.EMERGENT_ORDER,
            ProblemType.ADAPTIVE_EVOLUTION,
            ProblemType.COSMIC_HARMONY,
        }

        hint = {
            "recommended_mode": WuWeiDispatchMode.HYBRID_FLOW.value,
            "dao_schools": [WisdomSchool.DAOIST.value, WisdomSchool.BUDDHIST.value],
            "water_nature_emphasis": problem_type in dao_dominant_types,
            "dao_proverb": "上善若水，水善利万物而不争，处众人之所恶，故几于道。",
            "system_guidance": (
                "【道家提示】此类问题适合无为观察模式。"
                "让老子、庄子的智慧自然浮现，而非强制激活竞争。"
            ),
        }

        if problem_type in dao_dominant_types:
            hint["recommended_mode"] = WuWeiDispatchMode.WUWEI_OBSERVE.value
            hint["system_guidance"] = (
                "【道家强烈推荐】此为阴阳辩证类问题，"
                "强烈建议使用无为观察模式，让自然和谐的处理方案浮现。"
            )

        return hint


def _log_wuwei(msg: str):
    """无为调度日志——写入专门的日志通道"""
    try:
        from loguru import logger
        logger.info(f"[WuWei道家] {msg}")
    except ImportError:
        print(f"[WuWei道家] {msg}")
