"""
DivineReason - 至高推理引擎 (S1.0)
==========================================

完整版导入桥梁 — 从 smart_office_assistant 导入真正的 DivineReason

完整实现：
- GoT (Graph of Thoughts) 图结构
- LongCoT (Long Chain of Thought) 长链推理
- ToT (Tree of Thoughts) 树状分支
- ReAct (Reasoning and Acting) 工具调用

网络搜索增强 (v1.1)：
- 联网时自动搜索最新信息增强推理
- 网络洞察注入推理 context，影响推理过程
- 结果融合提升推理质量

路径: smart_office_assistant/src/intelligence/reasoning/_unified_reasoning_engine.py
"""

import sys
import os
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

logger = logging.getLogger("Somn.DivineReason")

# 安全地添加 smart_office_assistant/src 到 Python 路径
# 使用 site-packages 风格的方式：只追加不插入到开头，避免覆盖标准库
_smart_office_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "smart_office_assistant",
    "src"
)
_path_added = False
if os.path.exists(_smart_office_path):
    if _smart_office_path not in sys.path:
        sys.path.append(_smart_office_path)  # append 而非 insert(0)，避免覆盖标准库
        _path_added = True
    # v7.1: 清理重复路径（避免 sys.path 膨胀）
    seen = set()
    sys.path = [p for p in sys.path if not (p in seen or seen.add(p))]

# 导入完整版 DivineReason 及相关类
from intelligence.reasoning._unified_reasoning_engine import (
    DivineReason,
    UnifiedConfig,
    ReasoningMode,
    NodeType,
    EdgeType,
    ReasoningResult,
    SuperGraph,
    UnifiedEvaluator,
    UnifiedGenerator,
    UnifiedNode,
    UnifiedEdge,
    ReasoningMetadata,
    GraphStatistics,
    InsightType,
    NodeStatus,
    TaskComplexity,
    ThoughtPath,
    UnifiedReasoningEngine,
)

# ==================== 网络搜索增强层 (v1.0) ====================

@dataclass
class WebSearchContext:
    """网络搜索上下文"""
    enabled: bool = True
    auto_search: bool = True  # 自动搜索增强
    search_depth: str = "normal"  # quick / normal / deep
    context_window: int = 3  # 搜索时考虑的上下文节点数
    web_insights: List[Dict[str, Any]] = field(default_factory=list)
    search_count: int = 0
    last_search_time_ms: float = 0.0


class DivineReasonWithWebSearch:
    """
    DivineReason 网络搜索增强包装器

    功能：
    - 联网时自动搜索最新信息增强推理
    - 将网络知识注入推理节点
    - 多角度融合提升推理质量
    """

    def __init__(self, divine_reason: DivineReason):
        """
        初始化增强包装器

        Args:
            divine_reason: 原始 DivineReason 实例
        """
        self._engine = divine_reason
        self._web_context = WebSearchContext()

    def reason(
        self,
        problem: str,
        context: Dict[str, Any] = None,
        mode: ReasoningMode = ReasoningMode.DIVINE,
    ) -> ReasoningResult:
        """
        增强推理

        Args:
            problem: 问题描述
            context: 上下文
            mode: 推理模式

        Returns:
            ReasoningResult: 推理结果
        """
        # 确保context是可修改的字典
        if context is None:
            context = {}

        # 1. 检查是否需要网络搜索
        need_search = self._should_search(problem, context)

        if need_search and self._web_context.auto_search:
            # 2. 执行网络搜索增强
            self._enhance_with_web_search(problem, context)

        # 3. 将网络洞察注入推理 context，影响推理过程（核心修复）
        if self._web_context.web_insights:
            context = self._inject_web_insights_to_context(context)

        # 4. 执行原始推理（此时 context 已包含网络知识）
        result = self._engine.reason(problem, context, mode)

        # 5. 融合网络知识到结果元数据
        if self._web_context.web_insights:
            result = self._fuse_web_insights(result)

        return result

    def _should_search(self, problem: str, context: Optional[Dict]) -> bool:
        """判断是否需要网络搜索"""
        if not self._web_context.enabled:
            return False

        # 检查网络状态
        if not self._check_online():
            return False

        # 触发关键词
        trigger_keywords = [
            "最新", "最近", "2024", "2025", "2026",
            "趋势", "动态", "行情", "新闻",
            "数据", "统计", "报告", "研究",
            "今天", "昨日", "本周", "本月",
        ]

        if any(kw in problem for kw in trigger_keywords):
            return True

        # 检查上下文中的实时需求
        if context:
            if context.get("requires_realtime", False):
                return True
            if context.get("search_hint"):
                return True

        return False

    def _check_online(self) -> bool:
        """检查网络状态"""
        try:
            from .web_search_engine import is_online
        except ImportError:
            try:
                from web_search_engine import is_online
            except ImportError:
                return False
        return is_online()

    def _enhance_with_web_search(self, problem: str, context: Optional[Dict]):
        """使用网络搜索增强推理"""
        try:
            from .web_search_engine import search_web
        except ImportError:
            try:
                from web_search_engine import search_web
            except ImportError:
                return

        try:
            # 构建搜索查询
            query = self._build_search_query(problem, context)

            # 执行搜索
            max_results = 5
            if self._web_context.search_depth == "quick":
                max_results = 3
            elif self._web_context.search_depth == "deep":
                max_results = 10

            response = search_web(query, max_results=max_results)

            if response.success:
                # 提取关键洞察
                insights = []
                for r in response.results[:5]:
                    insights.append({
                        "title": r.title,
                        "snippet": r.snippet,
                        "url": r.url,
                        "source": r.source,
                        "relevance": r.relevance_score,
                    })

                self._web_context.web_insights = insights
                self._web_context.search_count += 1
                self._web_context.last_search_time_ms = response.search_time_ms

        except Exception as e:
            logger.debug(f"[DivineReason] Web search enhancement failed: {e}")

    def _build_search_query(self, problem: str, context: Optional[Dict]) -> str:
        """构建搜索查询"""
        query = problem[:100]  # 限制长度

        if context:
            # 添加上下文中的关键信息
            if "domain" in context:
                query = f"{context['domain']} {query}"
            if "keywords" in context:
                keywords = context["keywords"][:3]
                query = f"{' '.join(keywords)} {query}"

        return query

    def _fuse_web_insights(self, result: ReasoningResult) -> ReasoningResult:
        """
        将网络洞察融入推理结果元数据

        在 result 中添加 web_insights 字段，保留完整搜索信息供后续分析
        """
        # 为result添加web_insights属性
        result.web_insights = self._web_context.web_insights
        result.web_search_count = self._web_context.search_count
        result.web_search_time_ms = self._web_context.last_search_time_ms

        return result

    def _inject_web_insights_to_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        将网络洞察注入推理 context，使推理引擎在推理过程中可参考最新知识

        这是 v1.1 的核心改进：不再仅在推理后挂载 web_insights，
        而是将洞察内容实际注入 context，影响推理过程本身。

        注入策略：
        1. 将所有洞察摘要合并为 _web_knowledge 字段
        2. 保留原始洞察列表为 _web_insights_raw
        3. 设置 _web_enhanced=True 标记
        """
        # 避免修改原始 context
        enhanced_context = dict(context)

        # 合并洞察为知识摘要
        knowledge_parts = []
        for insight in self._web_context.web_insights:
            title = insight.get("title", "")
            snippet = insight.get("snippet", "")
            source = insight.get("source", "")
            if snippet:
                knowledge_parts.append(f"- [{source}] {title}: {snippet}")

        if knowledge_parts:
            enhanced_context["_web_knowledge"] = "\n".join(knowledge_parts)
            enhanced_context["_web_insights_raw"] = self._web_context.web_insights
            enhanced_context["_web_enhanced"] = True
            enhanced_context["requires_realtime"] = False  # 已获取实时数据，避免重复搜索

        return enhanced_context

    def set_web_search_enabled(self, enabled: bool):
        """设置是否启用网络搜索"""
        self._web_context.enabled = enabled

    def set_auto_search(self, auto: bool):
        """设置是否自动搜索"""
        self._web_context.auto_search = auto

    def set_search_depth(self, depth: str):
        """设置搜索深度: quick / normal / deep"""
        self._web_context.search_depth = depth

    def get_web_context(self) -> Dict[str, Any]:
        """获取网络搜索上下文"""
        return {
            "enabled": self._web_context.enabled,
            "auto_search": self._web_context.auto_search,
            "search_depth": self._web_context.search_depth,
            "search_count": self._web_context.search_count,
            "last_search_time_ms": self._web_context.last_search_time_ms,
            "insights_count": len(self._web_context.web_insights),
        }

__all__ = [
    # 原始 DivineReason 类
    "DivineReason",
    "UnifiedConfig",
    "ReasoningMode",
    "NodeType",
    "EdgeType",
    "ReasoningResult",
    "SuperGraph",
    "UnifiedEvaluator",
    "UnifiedGenerator",
    "UnifiedNode",
    "UnifiedEdge",
    "ReasoningMetadata",
    "GraphStatistics",
    "InsightType",
    "NodeStatus",
    "TaskComplexity",
    "ThoughtPath",
    "UnifiedReasoningEngine",
    # 网络搜索增强 (v1.0)
    "DivineReasonWithWebSearch",
    "WebSearchContext",
    # 谬误检测增强 (v1.1 — Logic 模块集成)
    "DivineReasonWithFallacyCheck",
    "detect_reasoning_fallacies",
    "analyze_reasoning_quality",
    "suggest_reasoning_improvements",
    "enhance_reasoning_result",
]


# ==================== 谬误检测增强层 (v1.1 — Logic 模块集成) ====================
try:
    from .logic_bridge import (
        DivineReasonWithFallacyCheck,
        detect_reasoning_fallacies,
        analyze_reasoning_quality,
        suggest_reasoning_improvements,
        enhance_reasoning_result,
    )
except Exception as e:
    import logging
    logging.getLogger("Somn.DivineReason").warning(f"Logic bridge import failed: {e}")
    # 提供空实现，避免导入失败导致整个模块不可用
    class DivineReasonWithFallacyCheck:
        def __init__(self, engine):
            self._engine = engine
        def reason_with_fallacy_check(self, problem, **kwargs):
            return self._engine.reason(problem, **kwargs)
    def detect_reasoning_fallacies(*args, **kwargs): return []
    def analyze_reasoning_quality(*args, **kwargs): return {"quality_score": 0.5}
    def suggest_reasoning_improvements(*args, **kwargs): return []
    def enhance_reasoning_result(result): return result

# =================== DivineReason 升级版 (v2.0 —— 整合 AutonomousCore 价值板块) ===================

@dataclass
class EnhancedReasoningResult:
    """增强推理结果（在 DivineReason ReasoningResult 基础上新增字段）"""
    engine: str = ""
    version: str = ""
    problem: str = ""
    mode: str = ""
    success: bool = False

    solution: str = ""
    graph: Optional[Any] = None
    path: Optional[Any] = None
    statistics: Optional[Any] = None
    quality_score: float = 0.0

    insights: List[Dict] = field(default_factory=list)
    corrections: List[Dict] = field(default_factory=list)
    reflections: List[Dict] = field(default_factory=list)
    verifications: List[Dict] = field(default_factory=list)
    critiques: List[Dict] = field(default_factory=list)
    tool_calls: List[Dict] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    # 新增增强字段
    reasoning_time: float = 0.0
    value_score: float = 0.5
    value_reasoning: str = ""
    reflection: Optional[Dict] = None
    has_goals: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "engine": self.engine,
            "version": self.version,
            "problem": self.problem,
            "mode": self.mode,
            "success": self.success,
            "solution": self.solution,
            "quality_score": round(self.quality_score, 4),
            "reasoning_time": round(self.reasoning_time, 4),
            "value_score": round(self.value_score, 4),
            "value_reasoning": self.value_reasoning,
            "reflection": self.reflection,
            "has_goals": self.has_goals,
            "insights_count": len(self.insights),
            "errors": self.errors,
            "warnings": self.warnings,
        }


class DivineReasonEnhanced:
    """
    DivineReason 升级版 —— 整合 AutonomousCore 价值板块

    新增三大能力（均可独立开关）：
    1. 推理后反思 (ReflectionEngine)  —— 从推理中总结模式、持续改进
    2. 价值评估 (ValueSystem)      —— 对推理结果做价值对齐评分
    3. 目标驱动推理 (GoalSystem)    —— 将活跃目标注入推理上下文

    使用方式：
        base = DivineReasonWithWebSearch(DivineReason(...))
        enhanced = DivineReasonEnhanced(base)
        result = enhanced.reason(problem, context)

    也可直接调用 reason_pro() 强制开启全部增强。
    """

    def __init__(
        self,
        divine_reason: DivineReason,
        enable_reflection: bool = True,
        enable_values: bool = True,
        enable_goals: bool = True,
    ):
        self._engine: DivineReason = divine_reason
        self.enable_reflection = enable_reflection
        self.enable_values = enable_values
        self.enable_goals = enable_goals

        # 延迟加载增强组件（避免无谓依赖）
        self._reflection_engine = None   # type: ignore
        self._value_system = None          # type: ignore
        self._goal_system = None           # type: ignore

        logger.info(
            f"[DivineReasonEnhanced] v2.0 初始化完成: "
            f"reflection={enable_reflection}, values={enable_values}, goals={enable_goals}"
        )

    # ── 延迟加载各增强组件 ──────────────────────────────────────────────────

    def _ensure_reflection(self):
        if self._reflection_engine is not None or not self.enable_reflection:
            return
        try:
            from src.autonomous_core.reflection_engine import ReflectionEngine
            self._reflection_engine = ReflectionEngine()
            logger.info("[DivineReasonEnhanced] ReflectionEngine 已加载")
        except Exception as e:
            logger.warning(f"[DivineReasonEnhanced] ReflectionEngine 加载失败: {e}")
            self.enable_reflection = False

    def _ensure_values(self):
        if self._value_system is not None or not self.enable_values:
            return
        try:
            from src.autonomous_core.value_system import ValueSystem
            self._value_system = ValueSystem()
            logger.info("[DivineReasonEnhanced] ValueSystem 已加载")
        except Exception as e:
            logger.warning(f"[DivineReasonEnhanced] ValueSystem 加载失败: {e}")
            self.enable_values = False

    def _ensure_goals(self):
        if self._goal_system is not None or not self.enable_goals:
            return
        try:
            from src.autonomous_core.goal_system import GoalSystem
            self._goal_system = GoalSystem()
            logger.info("[DivineReasonEnhanced] GoalSystem 已加载")
        except Exception as e:
            logger.warning(f"[DivineReasonEnhanced] GoalSystem 加载失败: {e}")
            self.enable_goals = False

    # ── 核心推理入口 ──────────────────────────────────────────────────────

    def reason(
        self,
        problem: str,
        context: Optional[Dict] = None,
        mode: ReasoningMode = ReasoningMode.DIVINE,
    ) -> EnhancedReasoningResult:
        """
        增强推理：推理 →（反思）→（价值评估）→（目标驱动）
        """
        import time
        ctx = dict(context) if context else {}

        # ① 注入活跃目标到推理上下文
        if self.enable_goals:
            self._ensure_goals()
            if self._goal_system:
                active_goals = self._goal_system.get_active_goals()
                if active_goals:
                    ctx["_active_goals"] = [g.to_dict() for g in active_goals[:3]]
                    logger.info(f"[DivineReasonEnhanced] 注入 {len(active_goals)} 个活跃目标到推理上下文")

        # ② 执行原始推理
        start = time.time()
        raw = self._engine.reason(problem, ctx, mode)
        reasoning_time = time.time() - start

        # 将原始 ReasoningResult 字段复制到增强结果
        result = EnhancedReasoningResult(
            engine=getattr(raw, 'engine', 'DivineReason'),
            version=getattr(raw, 'version', 'unknown'),
            problem=problem,
            mode=mode.value,
            success=getattr(raw, 'success', False),
            solution=getattr(raw, 'solution', ''),
            graph=getattr(raw, 'graph', None),
            path=getattr(raw, 'path', None),
            statistics=getattr(raw, 'statistics', None),
            quality_score=getattr(raw, 'quality_score', 0.0),
            insights=getattr(raw, 'insights', []),
            corrections=getattr(raw, 'corrections', []),
            reflections=getattr(raw, 'reflections', []),
            verifications=getattr(raw, 'verifications', []),
            critiques=getattr(raw, 'critiques', []),
            tool_calls=getattr(raw, 'tool_calls', []),
            errors=getattr(raw, 'errors', []),
            warnings=getattr(raw, 'warnings', []),
            metadata=getattr(raw, 'metadata', {}),
            reasoning_time=reasoning_time,
        )

        # ③ 推理后反思
        if self.enable_reflection and result.success:
            self._ensure_reflection()
            if self._reflection_engine:
                try:
                    record = self._reflection_engine.start_execution(
                        action_type="reasoning",
                        action_name=f"DivineReason.{mode.value}",
                        goal_id=ctx.get("_active_goal_id"),
                    )
                    self._reflection_engine.complete_execution(
                        record_id=record.id,
                        status="success",
                        result={"solution": result.solution[:200], "quality_score": result.quality_score},
                    )
                    result.reflection = {
                        "record_id": record.id,
                        "lessons_count": len(self._reflection_engine.get_recent_records(limit=5)),
                    }
                    logger.info(f"[DivineReasonEnhanced] 反思已记录: {record.id}")
                except Exception as e:
                    logger.warning(f"[DivineReasonEnhanced] 反思执行失败: {e}")

        # ④ 价值评估
        if self.enable_values and result.success and result.solution:
            self._ensure_values()
            if self._value_system:
                try:
                    eval_result = self._value_system.evaluate_options([
                        {"name": "reasoning_result", "content": result.solution}
                    ])
                    if eval_result:
                        result.value_score = eval_result[0][1]
                        result.value_reasoning = eval_result[0][2]
                    logger.info(f"[DivineReasonEnhanced] 价值评估得分: {result.value_score:.2f}")
                except Exception as e:
                    logger.warning(f"[DivineReasonEnhanced] 价值评估失败: {e}")

        result.has_goals = self._goal_system is not None
        return result

    def reason_pro(
        self,
        problem: str,
        context: Optional[Dict] = None,
        mode: ReasoningMode = ReasoningMode.DIVINE,
    ) -> EnhancedReasoningResult:
        """专业模式：强制开启全部增强（临时覆盖开关设置）"""
        old_r = self.enable_reflection
        old_v = self.enable_values
        old_g = self.enable_goals
        self.enable_reflection = True
        self.enable_values = True
        self.enable_goals = True
        try:
            return self.reason(problem, context, mode)
        finally:
            self.enable_reflection = old_r
            self.enable_values = old_v
            self.enable_goals = old_g

    # ── 目标管理接口（便捷方法）────────────────────────────────────

    def add_goal(self, title: str, description: str = "", priority: int = 3) -> Optional[str]:
        """添加推理目标（指导后续推理）"""
        if not self.enable_goals:
            logger.warning("[DivineReasonEnhanced] 目标系统未启用")
            return None
        self._ensure_goals()
        if self._goal_system:
            goal = self._goal_system.create_goal(title, description, priority)
            logger.info(f"[DivineReasonEnhanced] 添加目标: {goal.id} - {title}")
            return goal.id
        return None

    def get_enhancement_status(self) -> Dict[str, Any]:
        """获取各增强组件的加载/启用状态"""
        return {
            "reflection": {
                "enabled": self.enable_reflection,
                "loaded": self._reflection_engine is not None,
            },
            "values": {
                "enabled": self.enable_values,
                "loaded": self._value_system is not None,
            },
            "goals": {
                "enabled": self.enable_goals,
                "loaded": self._goal_system is not None,
                "active_goals": len(self._goal_system.get_active_goals()) if self._goal_system else 0,
            },
        }


# =================== 导出别名 (v2.0) ===================
# 让 from knowledge_cells import DivineReason 自动拿到增强版
DivineReason = DivineReasonEnhanced  # type: ignore

__all__ = [
    # 原始 DivineReason 类
    "DivineReason",
    "UnifiedConfig",
    "ReasoningMode",
    "NodeType",
    "EdgeType",
    "ReasoningResult",
    "SuperGraph",
    "UnifiedEvaluator",
    "UnifiedGenerator",
    "UnifiedNode",
    "UnifiedEdge",
    "ReasoningMetadata",
    "GraphStatistics",
    "InsightType",
    "NodeStatus",
    "TaskComplexity",
    "ThoughtPath",
    "UnifiedReasoningEngine",
    # 网络搜索增强 (v1.0)
    "DivineReasonWithWebSearch",
    "WebSearchContext",
    # 谬误检测增强 (v1.1)
    "DivineReasonWithFallacyCheck",
    "detect_reasoning_fallacies",
    "analyze_reasoning_quality",
    "suggest_reasoning_improvements",
    "enhance_reasoning_result",
    # 升级版 (v2.0)
    "DivineReasonEnhanced",
    "EnhancedReasoningResult",
]


