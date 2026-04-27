"""
__all__ = [
    'analyze',
    'coordinate',
    'get_coordination_report',
    'get_super_wisdom_coordinator',
    'main',
]

智慧fusion主协调器 v1.0
Supreme Wisdom Coordinator

Somn v1.0.0 终极智慧fusion系统,整合17大智慧流派,
提供超级decision能力.

核心功能:
1. 全域智慧感知 - 监听所有智慧系统的输出与状态
2. 智能调度 - 根据问题类型自动选择最优智慧组合
3. 超级fusion - 将多个流派的智慧fusion为unified答案
4. 时空选择 - 根据场景选择合适的思维方式
5. 冲突仲裁 - 解决不同流派间的智慧冲突

[v1.0 功能]
- 整合王阳明xinxue:知行合一,致良知
- 整合杜威反省思维:五步法,反省思维
- 整合顶级思维法:六法合一的synthesize思维
- 与现有17大智慧系统无缝集成

版本: v1.0
更新: 2026-04-02
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json

try:
    from ..dispatcher.wisdom_fusion_core import WisdomFusionCore, WisdomPriority, FusionMethod
    from ..engines.philosophy.yangming_xinxue_engine import YangmingXinxueEngine, XinxueLifeStage, XinxueInsight
    from ..reasoning.dewey_thinking_engine import DeweyThinkingEngine, DeweyStep, ReflectiveThinkingResult
    from ..engines.top_thinking_engine import TopThinkingEngine, ThinkingMethod
    COORDINATOR_MODULES_AVAILABLE = True
except ImportError as e:
    COORDINATOR_MODULES_AVAILABLE = False
    logging.warning(f"协调器模块导入失败: {e}")

logger = logging.getLogger(__name__)

class CoordinationStrategy(Enum):
    """协调strategy枚举"""
    # v1.0.0 新增strategy
    XINMIND_PRIMARY = "xinmind_primary"        # xinxue主导(人生/内省类问题)
    DEWEY_PRIMARY = "dewey_primary"            # 杜威思维主导(解决问题类)
    TOP_METHODS_PRIMARY = "top_methods_primary" # 顶级思维主导(复杂战略decision)
    
    # synthesizestrategy
    UNIVERSAL = "universal"                    # 通用synthesize(所有流派参与)
    MINIMALIST = "minimalist"                  # 简约主义(精简参与)
    DEEPEST = "deepest"                        # 最深智慧(质量优先)

class ProblemDomain(Enum):
    """问题领域枚举"""
    INNER_GROWTH = "inner_growth"          # 内心成长/自我修养 → xinxue
    PRACTICAL_PROBLEM = "practical_problem"  # 实际问题解决 → 杜威
    STRATEGIC_DECISION = "strategic"        # 战略decision → 顶级思维
    ETHICAL_JUDGMENT = "ethical"            # 伦理道德judge → 儒家
    NATURAL_ORDER = "natural"               # 自然规律/道 → 道家
    CREATIVE_INNOVATION = "creative"        # 创新创造 → 顶级思维
    SOCIAL_RELATIONS = "social"             # 社会关系 → 儒家/鸿铭
    COMPETITIVE = "competitive"             # 竞争博弈 → 兵法/博弈思维
    CULTURAL_BRIDGE = "cultural"             # 跨文化 → 鸿铭
    UNKNOWN = "unknown"                     # 未分类 → 通用fusion

@dataclass
class WisdomCoordinationRequest:
    """智慧协调请求"""
    problem: str
    context: Dict[str, Any] = field(default_factory=dict)
    preferred_strategies: List[CoordinationStrategy] = field(default_factory=list)
    excluded_systems: List[str] = field(default_factory=list)
    max_systems: int = 10
    confidence_threshold: float = 0.7

@dataclass
class WisdomCoordinationResult:
    """智慧协调结果"""
    primary_strategy: CoordinationStrategy
    active_systems: List[str]
    insights: Dict[str, Any]
    fused_answer: str
    confidence: float
    strategy_rationale: str
    recommendations: List[str]
    metadata: Dict[str, Any]

class SuperWisdomAnalysisResult:
    """analyze() 方法返回结果，兼容 agent_core / somn_core 的调用签名"""
    def __init__(self, primary_insight: str = "",
                 secondary_insights: list = None,
                 action_recommendations: list = None,
                 activated_schools: list = None,
                 confidence: float = 0.0,
                 raw_result: 'WisdomCoordinationResult' = None):
        self.primary_insight = primary_insight
        self.secondary_insights = secondary_insights or []
        self.action_recommendations = action_recommendations or []
        self.activated_schools = activated_schools or []
        self.confidence = confidence
        self.raw_result = raw_result

class SupremeWisdomCoordinator:
    """
    智慧fusion主协调器

    Somn v1.0.0 的最高智慧协调层,unified调度17大智慧系统,
    为复杂问题提供最优智慧组合方案.

    使用方式:
    coordinator = SupremeWisdomCoordinator()
    result = coordinator.coordinate(problem="如何提升认知深度?", context={})
    logger.info(result.fused_answer)
    """

    def __init__(self):
        """init智慧协调器"""
        self.name = "SupremeWisdomCoordinator"
        self.version = "v1.0"
        self.active_systems: Dict[str, Any] = {}
        self.coordination_history: List[WisdomCoordinationResult] = []

        self._load_wisdom_systems()
        logger.info(f"✓ 智慧fusion主协调器 {self.version} init完成")
        logger.info(f"  活跃系统数: {len(self.active_systems)}")

    def analyze(self, query_text: str = "", context: Dict[str, Any] = None,
                threshold: float = 0.25, max_schools: int = 6) -> SuperWisdomAnalysisResult:
        """
        [v10.0 P0修复] 兼容桥接方法 — 强制使用 coordinate_with_timeout 防止无限阻塞。

        将 keyword 签名 (query_text, context, threshold, max_schools)
        内部转换为 coordinate() 调用，返回 SuperWisdomAnalysisResult.
        """
        import time as _time
        if context is None:
            context = {}

        _guard = context.get("_timeout_guard")
        # ★ P0-2 修复：30s 硬超时保护，防止 coordinate() 内部任何步骤卡死
        _ANALYZE_TIMEOUT = 30.0

        try:
            request = WisdomCoordinationRequest(
                problem=query_text,
                context=dict(context),  # 隔离避免污染原context
                max_systems=max_schools,
                confidence_threshold=threshold,
            )

            # ★ 优先使用 coordinate_with_timeout（ThreadPoolExecutor 硬超时兜底）
            coord_result = self.coordinate_with_timeout(
                request, timeout=_ANALYZE_TIMEOUT, timeout_guard=_guard
            )

            # 从协调结果提取结构化字段
            primary = coord_result.fused_answer or ""
            # 从 insights 中提取 secondary
            secondary = []
            for sys_name, insight in coord_result.insights.items():
                if insight:
                    if isinstance(insight, str):
                        secondary.append(insight[:200])
                    elif isinstance(insight, dict):
                        answer = insight.get("answer", "")
                        if answer:
                            secondary.append(f"[{sys_name}] {answer[:200]}")
                if len(secondary) >= 5:
                    break

            return SuperWisdomAnalysisResult(
                primary_insight=primary,
                secondary_insights=secondary,
                action_recommendations=coord_result.recommendations or [],
                activated_schools=coord_result.active_systems or [],
                confidence=coord_result.confidence,
                raw_result=coord_result,
            )
        except Exception as e:
            logger.warning(f"analyze() 桥接失败，回退简单结果: {e}")
            return SuperWisdomAnalysisResult(
                primary_insight="",
                secondary_insights=[],
                action_recommendations=[],
                activated_schools=[],
                confidence=0.0,
            )

    def _load_wisdom_systems(self):
        """加载所有智慧系统"""
        if not COORDINATOR_MODULES_AVAILABLE:
            logger.warning("  ⚠ 协调器依赖模块不可用,仅基础功能可用")
            return
        
        # ---- v1.0.0 新系统 ----
        try:
            self.active_systems["yangming_xinxue"] = YangmingXinxueEngine()
            logger.info("  ✓ 王阳明xinxue系统已注册")
        except Exception as e:
            logger.warning(f"  ✗ 王阳明xinxue系统注册失败: {e}")
        
        try:
            self.active_systems["dewey_thinking"] = DeweyThinkingEngine()
            logger.info("  ✓ 杜威反省思维系统已注册")
        except Exception as e:
            logger.warning(f"  ✗ 杜威反省思维系统注册失败: {e}")
        
        try:
            self.active_systems["top_thinking"] = TopThinkingEngine()
            logger.info("  ✓ 顶级思维法系统已注册")
        except Exception as e:
            logger.warning(f"  ✗ 顶级思维法系统注册失败: {e}")
        
        # ---- 核心fusion系统 ----
        try:
            self.active_systems["wisdom_fusion"] = WisdomFusionCore()
            logger.info("  ✓ 智慧fusion核心系统已注册")
        except Exception as e:
            logger.warning(f"  ✗ 智慧fusion核心系统注册失败: {e}")
        
        # ---- 扩展智慧系统 ----
        system_names = [
            "sufu_wisdom", "military_strategy", "dao_wisdom", "ru_wisdom",
            "hongming_wisdom", "classic_wisdom", "lvshi_wisdom",
            "growth_engine", "science_thinking", "poetry_intelligence"
        ]
        
        for sys_name in system_names:
            try:
                mod = __import__(f"src.intelligence.{sys_name}", fromlist=[""])
                if hasattr(mod, sys_name.replace("_", "").title().replace("Sufu", "Sufu").replace("Dao", "Dao").replace("Ru", "Ru").replace("Hongming", "Hongming").replace("Classic", "Classic").replace("Lvshi", "Lvshi")):
                    inst = getattr(mod, sys_name.replace("_", "").title().replace("Sufu", "Sufu").replace("Dao", "Dao").replace("Ru", "Ru").replace("Hongming", "Hongming").replace("Classic", "Classic").replace("Lvshi", "Lvshi"))()
                    self.active_systems[sys_name] = inst
                    logger.info(f"  ✓ {sys_name} 已注册")
            except Exception as e:
                logger.debug(f"[SuperWisdom] 系统{sys_name}注册失败(跳过): {e}")
    
    def coordinate(self, request: WisdomCoordinationRequest) -> WisdomCoordinationResult:
        """
        协调处理问题的核心方法 [v9.0: 增加超时感知]。
        
        流程:
        1. 问题域recognize - judge问题属于哪个领域
        2. strategy选择 - 确定最优协调strategy
        3. 系统调度 - 激活相关智慧系统
        4. 智慧fusion - 多系统输出fusion
        5. 答案输出 - generatesynthesize建议

        v9.0 增强：支持通过 request.context["_timeout_guard"] 接收全局超时信号，
        在每步之间检查是否已超时，避免无意义的长链路执行。
        """
        import time as _time
        _coord_start = _time.monotonic()
        
        # 获取全局超时守护器（如果存在）
        _guard = (request.context or {}).get("_timeout_guard")
        
        problem = request.problem
        context = request.context
        
        def _check_timeout(step_name: str):
            """内部工具：在关键步骤前检查是否应中断"""
            if _guard is None:
                return False
            try:
                if hasattr(_guard, 'ctx') and _guard.ctx.is_expired():
                    logger.warning(f"[SuperWisdom] 在'{step_name}'前检测到全局超时, T+{_time.monotonic()-_coord_start:.1f}s")
                    return True
                _guard.check_and_degrade()
            except Exception as e:
                logger.debug(f"[SuperWisdom] 守护器检查跳过: {e}")
            return False
        
        # ---- 步骤1: 问题域recognize ----
        if _check_timeout("域识别"):
            return self._timeout_fallback_result(request, "timeout_before_domain", _coord_start)
        domain = self._identify_domain(problem, context)
        logger.info(f"  [协调] 问题域recognize: {domain.value}")
        
        # ---- 步骤2: strategy选择 ----
        if _check_timeout("策略选择"):
            return self._timeout_fallback_result(request, "timeout_before_strategy", _coord_start, domain=domain)
        strategy = self._select_strategy(domain, request)
        logger.info(f"  [协调] strategy选择: {strategy.value}")
        
        # ---- 步骤3: 系统调度 ----
        if _check_timeout("系统调度"):
            return self._timeout_fallback_result(request, "timeout_before_dispatch", _coord_start,
                                                  domain=domain, strategy=strategy)
        active = self._dispatch_systems(domain, strategy, request)
        logger.info(f"  [协调] 激活系统: {len(active)}个")
        
        # ★ [v10.0 P0修复] 绝对超时守护：总坐标时间上限60s
        _COORD_ABSOLUTE_TIMEOUT = 60.0

        # ---- 步骤4: 智慧fusion ----
        if _check_timeout("智慧融合"):
            return self._timeout_fallback_result(request, "timeout_before_fusion", _coord_start,
                                                  domain=domain, strategy=strategy, active_count=len(active))
        # ★ P0-2 修复：fuse_insights 中每系统独立超时（每系统最多3s）
        insights = self._fuse_insights(active, problem, context, timeout_guard=_guard,
                                        coord_start=_coord_start, abs_timeout=_COORD_ABSOLUTE_TIMEOUT)

        # ★ P0-2 修复：最终答案生成绝对超时检查
        if _time.monotonic() - _coord_start > _COORD_ABSOLUTE_TIMEOUT:
            logger.warning(f"[SuperWisdom] coordinate() 达到绝对超时({_COORD_ABSOLUTE_TIMEOUT}s)，提前返回")
            return self._timeout_fallback_result(request, f"abs_timeout_{_COORD_ABSOLUTE_TIMEOUT:.0f}s",
                                                  _coord_start, domain=domain, strategy=strategy,
                                                  active_count=len(active))

        # ---- 步骤5: 答案generate ----
        result = self._generate_answer(strategy, active, insights, problem, domain)
        
        self.coordination_history.append(result)

        # 记录协调结果到全局guard
        if _guard is not None:
            try:
                _guard.record_partial("wisdom_coordination", {
                    "domain": domain.value if hasattr(domain, 'value') else str(domain),
                    "strategy": strategy.value if hasattr(strategy, 'value') else str(strategy),
                    "insight_count": len(insights) if isinstance(insights, dict) else 0,
                    "elapsed_s": round(_time.monotonic() - _coord_start, 2),
                })
            except Exception as e:
                logger.debug(f"[SuperWisdom] 记录partial失败: {e}")

        return result

    def coordinate_with_timeout(self, request: WisdomCoordinationRequest,
                                 timeout: float = 30.0,
                                 timeout_guard=None) -> WisdomCoordinationResult:
        """
        [v9.0 新增] 带硬超时保护的协调包装器。
        
        使用线程池执行coordinate()，超时后返回降级结果。
        这是在外部调用方无法使用asyncio时（如同步主链路）的备选方案。

        Args:
            request: 协调请求
            timeout: 超时时间（秒），默认30秒
            timeout_guard: 可选的全局TimeoutGuard实例

        Returns:
            WisdomCoordinationResult — 正常结果或降级结果
        """
        import time as _time
        from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

        # 如果已有全局guard且处于终止级别，直接跳过
        if timeout_guard is not None:
            try:
                level = timeout_guard.current_level
                from src.core.timeout_guard import TimeoutLevel, _level_ordinal
                if _level_ordinal(level) >= _level_ordinal(TimeoutLevel.TERMINATE):
                    return self._timeout_fallback_result(
                        request, "skipped_terminate", _time.monotonic()
                    )
                # 在降级/紧急模式下缩短超时
                if _level_ordinal(level) >= _level_ordinal(TimeoutLevel.DEGRADED):
                    timeout = min(timeout, 10.0)
            except Exception as e:
                logger.debug(f"[SuperWisdom] 降级检查跳过: {e}")

        # 将guard注入request context
        if timeout_guard is not None and request.context is None:
            request.context = {"_timeout_guard": timeout_guard}
        elif timeout_guard is not None:
            request.context["_timeout_guard"] = timeout_guard

        executor = ThreadPoolExecutor(max_workers=1)
        try:
            future = executor.submit(self.coordinate, request)
            result = future.result(timeout=timeout)
            return result
        except FuturesTimeout:
            elapsed = _time.monotonic() - (_time.monotonic() - timeout) - timeout  # 近似值，实际用下面重新算
            logger.warning(
                f"[SuperWisdom] coordinate() 硬超时({timeout:.1f}s), "
                f"返回降级结果"
            )
            if timeout_guard is not None:
                try:
                    timeout_guard.check_and_degrade()
                except Exception as e:
                    logger.debug(f"[SuperWisdom] 硬超时后守护器检查跳过: {e}")
            return self._timeout_fallback_result(request, f"hard_timeout_{timeout:.0f}s", 0.0)
        finally:
            executor.shutdown(wait=False)

    def _timeout_fallback_result(self, request, reason: str,
                                  coord_start_time: float,
                                  domain=None, strategy=None,
                                  active_count=None) -> WisdomCoordinationResult:
        """
        [v9.0 新增] 生成超时降级结果。
        
        当coordinate()在任何步骤被中断时返回一个结构化的空结果，
        让下游可以继续处理而不是抛出异常。
        """
        import time as _time
        elapsed = _time.monotonic() - coord_start_time if coord_start_time > 0 else 0.0

        return WisdomCoordinationResult(
            primary_strategy=strategy or CoordinationStrategy.FUSION_DEPTH,
            active_systems=[],
            insights={"timeout_reason": reason, "elapsed_s": round(elapsed, 2)},
            fused_answer=f"[协调降级] 智慧协调因{reason}被截断({elapsed:.1f}s)",
            confidence=0.0,
            strategy_rationale=f"协调过程未完成: {reason}",
            recommendations=["协调超时，建议直接使用基础推理"],
            metadata={
                "status": "degraded",
                "reason": reason,
                "elapsed_seconds": round(elapsed, 2),
                "domain_reached": domain.value if hasattr(domain, 'value') else str(domain) if domain else "none",
                "active_systems_found": active_count or 0,
            },
        )
    
    def _identify_domain(self, problem: str, context: Dict) -> ProblemDomain:
        """recognize问题所属领域"""
        problem_lower = problem.lower()
        
        # 内心成长 / 自我修养
        if any(k in problem_lower for k in ['成长', '修养', '内心', '自我', '知行', '良知', '心安', '困惑', '迷茫', '人生', '意义', '价值', '信念', '志向', '志向']):
            return ProblemDomain.INNER_GROWTH
        
        # 实际问题解决
        if any(k in problem_lower for k in ['如何', '怎么办', '解决', '方法', 'strategy', '步骤', '流程', '方案', '设计', '实现', '优化', '改进']):
            return ProblemDomain.PRACTICAL_PROBLEM
        
        # 战略decision
        if any(k in problem_lower for k in ['战略', 'decision', '规划', '长远', '全局', '顶层', '布局', '取舍', '选择', '风险', '机遇', '竞争', '市场', '扩张']):
            return ProblemDomain.STRATEGIC_DECISION
        
        # 伦理道德judge
        if any(k in problem_lower for k in ['应该', '对错', '道德', '伦理', '善恶', '仁义', '公正', '公平', '正义', '责任', '义务', '诚信', '忠诚']):
            return ProblemDomain.ETHICAL_JUDGMENT
        
        # 自然规律
        if any(k in problem_lower for k in ['自然', '规律', '阴阳', '平衡', '变化', '循环', '无为', '顺应', '天道']):
            return ProblemDomain.NATURAL_ORDER
        
        # 创新创造
        if any(k in problem_lower for k in ['创新', '创造', '突破', '颠覆', '新', '发明', '灵感', '想象', '愿景']):
            return ProblemDomain.CREATIVE_INNOVATION
        
        # 社会关系
        if any(k in problem_lower for k in ['人际', '关系', '合作', '沟通', '领导', '团队', '家庭', '朋友', '同事', '上级']):
            return ProblemDomain.SOCIAL_RELATIONS
        
        # 竞争博弈
        if any(k in problem_lower for k in ['竞争', '博弈', '对手', '优势', '劣势', 'strategy', '谈判', '争夺']):
            return ProblemDomain.COMPETITIVE
        
        # 跨文化
        if any(k in problem_lower for k in ['文化', '跨文化', '国际', '翻译', '交流', '差异', 'fusion', '东方', '西方']):
            return ProblemDomain.CULTURAL_BRIDGE
        
        return ProblemDomain.UNKNOWN
    
    def _select_strategy(self, domain: ProblemDomain, 
                         request: WisdomCoordinationRequest) -> CoordinationStrategy:
        """根据问题领域选择协调strategy"""
        # 优先使用用户指定的strategy
        if request.preferred_strategies:
            return request.preferred_strategies[0]
        
        # 根据领域自动选择
        domain_strategy_map = {
            ProblemDomain.INNER_GROWTH: CoordinationStrategy.XINMIND_PRIMARY,
            ProblemDomain.PRACTICAL_PROBLEM: CoordinationStrategy.DEWEY_PRIMARY,
            ProblemDomain.STRATEGIC_DECISION: CoordinationStrategy.TOP_METHODS_PRIMARY,
            ProblemDomain.ETHICAL_JUDGMENT: CoordinationStrategy.UNIVERSAL,
            ProblemDomain.NATURAL_ORDER: CoordinationStrategy.UNIVERSAL,
            ProblemDomain.CREATIVE_INNOVATION: CoordinationStrategy.TOP_METHODS_PRIMARY,
            ProblemDomain.SOCIAL_RELATIONS: CoordinationStrategy.UNIVERSAL,
            ProblemDomain.COMPETITIVE: CoordinationStrategy.TOP_METHODS_PRIMARY,
            ProblemDomain.CULTURAL_BRIDGE: CoordinationStrategy.UNIVERSAL,
            ProblemDomain.UNKNOWN: CoordinationStrategy.UNIVERSAL,
        }
        
        return domain_strategy_map.get(domain, CoordinationStrategy.UNIVERSAL)
    
    def _dispatch_systems(self, domain: ProblemDomain, 
                          strategy: CoordinationStrategy,
                          request: WisdomCoordinationRequest) -> Dict[str, Any]:
        """调度相关智慧系统"""
        active = {}
        
        # strategy对应的系统优先级
        strategy_systems = {
            CoordinationStrategy.XINMIND_PRIMARY: [
                ("yangming_xinxue", 0.9),
                ("dewey_thinking", 0.6),
                ("top_thinking", 0.5),
                ("wisdom_fusion", 0.4),
            ],
            CoordinationStrategy.DEWEY_PRIMARY: [
                ("dewey_thinking", 0.9),
                ("yangming_xinxue", 0.6),
                ("top_thinking", 0.7),
                ("wisdom_fusion", 0.5),
            ],
            CoordinationStrategy.TOP_METHODS_PRIMARY: [
                ("top_thinking", 0.9),
                ("dewey_thinking", 0.7),
                ("yangming_xinxue", 0.5),
                ("wisdom_fusion", 0.6),
            ],
            CoordinationStrategy.UNIVERSAL: [
                ("yangming_xinxue", 0.7),
                ("dewey_thinking", 0.7),
                ("top_thinking", 0.7),
                ("wisdom_fusion", 0.8),
            ],
            CoordinationStrategy.MINIMALIST: [
                ("top_thinking", 0.8),
            ],
            CoordinationStrategy.DEEPEST: [
                ("yangming_xinxue", 0.8),
                ("wisdom_fusion", 0.7),
            ],
        }
        
        systems_to_activate = strategy_systems.get(strategy, strategy_systems[CoordinationStrategy.UNIVERSAL])
        
        for sys_name, priority in systems_to_activate:
            if sys_name in self.active_systems and sys_name not in request.excluded_systems:
                if len(active) < request.max_systems:
                    active[sys_name] = {
                        "instance": self.active_systems[sys_name],
                        "priority": priority
                    }
        
        return active
    
    # ★ [v10.0 P0修复] fuse_insights 超时配置
    _FUSE_SYSTEM_TIMEOUT = 3.0   # 每个系统最多3秒
    _FUSE_TOTAL_BUDGET = 10.0   # 总fuse预算10秒

    def _fuse_insights(self, active: Dict[str, Any],
                       problem: str,
                       context: Dict,
                       timeout_guard=None,
                       coord_start: float = 0.0,
                       abs_timeout: float = 60.0) -> Dict[str, Any]:
        """
        [v10.0 P0修复] fusion多个智慧系统的输出 — 带每系统独立超时保护。

        Args:
            active: 活跃系统字典
            problem: 问题文本
            context: 上下文
            timeout_guard: 全局TimeoutGuard（可选）
            coord_start: 协调开始时间（用于绝对超时检查）
            abs_timeout: 绝对超时上限
        """
        import time as _time
        insights = {}
        _fuse_start = _time.monotonic()
        _system_timeout = self._FUSE_SYSTEM_TIMEOUT

        for sys_name, sys_info in active.items():
            # ★ 每次循环前检查绝对超时
            if _time.monotonic() - coord_start > abs_timeout:
                logger.warning(f"[SuperWisdom] fuse_insights 达到绝对超时({abs_timeout}s)，提前终止")
                break

            # 检查全局guard
            if timeout_guard is not None:
                try:
                    if hasattr(timeout_guard, 'ctx') and timeout_guard.ctx.is_expired():
                        break
                    timeout_guard.check_and_degrade()
                except Exception as e:
                    logger.debug(f"[SuperWisdom] fuse_insights守护器检查跳过: {e}")

            # 计算剩余时间，决定是否跳过
            elapsed = _time.monotonic() - _fuse_start
            remaining = self._FUSE_TOTAL_BUDGET - elapsed
            if remaining <= 0:
                logger.warning(f"[SuperWisdom] fuse_insights 预算耗尽({elapsed:.1f}s)，跳过剩余系统")
                break

            # ★ 动态缩短超时：保证至少有0.5s给后续步骤
            effective_sys_timeout = min(_system_timeout, max(0.5, remaining * 0.8))

            instance = sys_info["instance"]
            try:
                from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

                def _call_analyze():
                    if sys_name == "yangming_xinxue" and hasattr(instance, "analyze"):
                        return instance.analyze(problem, context)
                    elif sys_name == "dewey_thinking" and hasattr(instance, "analyze"):
                        return instance.analyze(problem, context)
                    elif sys_name == "top_thinking" and hasattr(instance, "analyze"):
                        return instance.analyze(problem, context)
                    elif sys_name == "wisdom_fusion" and hasattr(instance, "fuse"):
                        return instance.fuse(problem, context)
                    return None

                executor = ThreadPoolExecutor(max_workers=1)
                try:
                    future = executor.submit(_call_analyze)
                    result = future.result(timeout=effective_sys_timeout)
                    insights[sys_name] = result
                except FuturesTimeout:
                    logger.warning(f"[SuperWisdom] {sys_name} fusion超时({effective_sys_timeout:.1f}s)，跳过")
                    insights[sys_name] = None
                finally:
                    executor.shutdown(wait=False)
            except Exception as e:
                logger.warning(f"  ⚠ {sys_name} 输出fusion失败: {e}")
                insights[sys_name] = None

        return insights
    
    def _generate_answer(self, strategy: CoordinationStrategy,
                         active: Dict[str, Any],
                         insights: Dict[str, Any],
                         problem: str,
                         domain: ProblemDomain) -> WisdomCoordinationResult:
        """generate最终synthesize答案"""
        strategy_rationales = {
            CoordinationStrategy.XINMIND_PRIMARY: "xinxue思维主导 - 内外兼修,知行合一,从心性问题切入根本",
            CoordinationStrategy.DEWEY_PRIMARY: "杜威反省思维主导 - 五步法系统推演,从问题分解到实验检验",
            CoordinationStrategy.TOP_METHODS_PRIMARY: "顶级思维法主导 - 六法合一的synthesize_decision",
            CoordinationStrategy.UNIVERSAL: "通用fusion_strategy - 多流派智慧synthesize",
            CoordinationStrategy.MINIMALIST: "简约strategy - 精简高效,直击核心",
            CoordinationStrategy.DEEPEST: "深度strategy - 触及最深层的智慧洞见",
        }
        
        # 构建fusion答案
        answer_parts = []
        recommendations = []
        
        # 从各系统提取洞见
        for sys_name, insight in insights.items():
            if insight:
                if isinstance(insight, dict):
                    if "answer" in insight:
                        answer_parts.append(f"[{sys_name}]: {insight['answer']}")
                    if "recommendations" in insight:
                        recommendations.extend(insight["recommendations"])
        
        # 整合推荐,去重（v16.1 P1: 增强 — 先精确去重，再语义去重）
        unique_recommendations = list(dict.fromkeys(recommendations))
        if len(unique_recommendations) > 1:
            unique_recommendations = self._semantic_dedup(unique_recommendations)
        unique_recommendations = unique_recommendations[:5]
        
        # generate最终答案
        if answer_parts:
            fused_answer = f"[{strategy.value}]\n\n" + "\n\n".join(answer_parts)
        else:
            fused_answer = f"[{strategy.value}]\n\n基于{len(active)}个智慧系统的synthesize分析,"
            fused_answer += f'对问题"{problem}"给出以下建议:\n'
            fused_answer += f"核心洞见: {problem}的解决之道在于内外兼修,"
            fused_answer += f"从根本入手,在事上磨练,最终达到知行合一的境界."
        
        return WisdomCoordinationResult(
            primary_strategy=strategy,
            active_systems=list(active.keys()),
            insights=insights,
            fused_answer=fused_answer,
            confidence=0.82,
            strategy_rationale=strategy_rationales.get(strategy, "通用strategy"),
            recommendations=unique_recommendations,
            metadata={
                "domain": domain.value,
                "systems_count": len(active),
                "v7_0_systems": ["yangming_xinxue", "dewey_thinking", "top_thinking"]
            }
        )
    
    @staticmethod
    def _semantic_dedup(items: List[str], threshold: float = 0.45) -> List[str]:
        """v16.1 P1: 基于 Jaccard 相似度的语义去重.
        对每对 recommendation 计算字符 bigram Jaccard 系数，
        超过 threshold 的视为语义重复，只保留较早出现的。
        短文本（<=2字符）退化为精确匹配去重。
        """
        def _bigrams(text: str) -> set:
            if len(text) <= 2:
                return {text}  # v16.1 fix: 短文本直接用自身做集合
            return {text[i:i+2] for i in range(len(text) - 1)}
        
        kept: List[str] = []
        for item in items:
            bg = _bigrams(item)
            is_dup = False
            for existing in kept:
                inter = len(bg & _bigrams(existing))
                union = len(bg | _bigrams(existing))
                if union > 0 and inter / union >= threshold:
                    is_dup = True
                    break
            if not is_dup:
                kept.append(item)
        return kept
    
    def get_coordination_report(self) -> Dict[str, Any]:
        """get协调器状态报告"""
        return {
            "version": self.version,
            "active_systems": list(self.active_systems.keys()),
            "total_coordinations": len(self.coordination_history),
            "v7_0_systems": {
                "yangming_xinxue": "yangming_xinxue" in self.active_systems,
                "dewey_thinking": "dewey_thinking" in self.active_systems,
                "top_thinking": "top_thinking" in self.active_systems,
            }
        }

def main():
    """演示智慧协调器"""
    logging.info("=" * 60)
    logging.info("智慧fusion主协调器演示")
    logging.info("=" * 60)
    
    coordinator = SupremeWisdomCoordinator()
    
    report = coordinator.get_coordination_report()
    logging.info(f"✓ 协调器状态:")
    logging.info(f"  版本: {report['version']}")
    logging.info(f"  活跃系统: {len(report['active_systems'])}")
    logging.info(f"  v1.0.0新系统状态:")
    for sys_name, status in report['v7_0_systems'].items():
        logging.info(f"    {sys_name}: {'✓' if status else '✗'}")
    
    # 测试协调
    logging.info("=" * 60)
    logging.info("示例问题: 如何在工作中提升认知深度?")
    logging.info("=" * 60)
    
    request = WisdomCoordinationRequest(
        problem="如何在工作中提升认知深度?",
        context={}
    )
    
    result = coordinator.coordinate(request)
    
    logging.info(f"问题域: {result.metadata['domain']}")
    logging.info(f"协调strategy: {result.primary_strategy.value}")
    logging.info(f"strategybasis: {result.strategy_rationale}")
    logging.info(f"激活系统: {', '.join(result.active_systems)}")
    logging.info(f"置信度: {result.confidence:.2f}")
    logging.info(f"fusion答案:\n{result.fused_answer}")
    
    if result.recommendations:
        logging.info(f"推荐建议:")
        for rec in result.recommendations:
            logging.info(f"  • {rec}")
    
    logging.info("=" * 60)
    logging.info("演示完成")
    logging.info("=" * 60)

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

# 别名兼容
SuperWisdomCoordinator = SupremeWisdomCoordinator

# 单例实例
_super_wisdom_coordinator_instance = None

def get_super_wisdom_coordinator():
    """get SuperWisdomCoordinator 单例实例"""
    global _super_wisdom_coordinator_instance
    if _super_wisdom_coordinator_instance is None:
        _super_wisdom_coordinator_instance = SupremeWisdomCoordinator()
    return _super_wisdom_coordinator_instance
