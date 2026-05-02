"""
SageDispatch Core - 核心调度引擎
贤者调度系统 - 后台调度中枢
"""

import time
import uuid
import re
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import json


class Level(Enum):
    """调度级别枚举"""
    L1_INSTINCT = "L1"
    L2_LOGIC = "L2"
    L3_WISDOM = "L3"
    L4_INTUITION = "L4"


class DispatcherState(Enum):
    """调度器状态"""
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATING = "escalating"


@dataclass
class DispatchRequest:
    """调度请求"""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    problem: Dict[str, Any] = field(default_factory=dict)
    level: Optional[Level] = None
    forced_level: Optional[Level] = None
    allow_escalation: bool = True
    max_time: float = 30.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    trace_enabled: bool = True
    parent_output: Optional[Dict] = None  # 链式调度传递的父输出


@dataclass
class DispatchResponse:
    """调度响应"""
    request_id: str
    dispatcher_id: str = "SD-ROOT"
    level: Level = Level.L2_LOGIC
    time_spent: float = 0.0
    dispatched_to: List[str] = field(default_factory=list)
    confidence: float = 0.8
    output: Dict[str, Any] = field(default_factory=dict)
    state: DispatcherState = DispatcherState.READY
    escalated: bool = False
    escalation_target: Optional[str] = None
    trace: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class BaseDispatcher:
    """调度器基类"""

    dispatcher_id: str = "BASE"
    dispatcher_name: str = "基础调度器"

    def __init__(self):
        self.state = DispatcherState.READY
        self._metrics = {
            "total_calls": 0,
            "failed_calls": 0,
            "avg_time": 0.0,
            "total_time": 0.0
        }

    def dispatch(self, request: DispatchRequest) -> DispatchResponse:
        """统一调度入口"""
        self.state = DispatcherState.RUNNING
        self._metrics["total_calls"] += 1
        start_time = time.time()

        try:
            output = self._execute(request)
            self.state = DispatcherState.COMPLETED
            elapsed = time.time() - start_time
            self._update_metrics(elapsed)
            return self._build_response(request, output, elapsed)
        except Exception as e:
            self.state = DispatcherState.FAILED
            self._metrics["failed_calls"] += 1
            return self._build_error_response(request, str(e))

    def _execute(self, request: DispatchRequest) -> Dict[str, Any]:
        """子类实现具体调度逻辑"""
        raise NotImplementedError

    def _build_response(self, request: DispatchRequest,
                       output: Dict, elapsed: float) -> DispatchResponse:
        """构建响应"""
        # 修复：直接从output中获取confidence，避免嵌套问题
        confidence = output.get("confidence", 0.8)
        # 如果output中有嵌套的output，取内层confidence
        inner_output = output.get("output", {})
        if isinstance(inner_output, dict):
            confidence = inner_output.get("confidence", confidence)
        
        return DispatchResponse(
            request_id=request.request_id,
            dispatcher_id=self.dispatcher_id,
            level=request.level or Level.L2_LOGIC,
            time_spent=elapsed,
            dispatched_to=output.get("dispatched_to", [self.dispatcher_id]),
            confidence=confidence,
            output=output,
            state=self.state,
            trace=output.get("trace", {})
        )

    def _build_error_response(self, request: DispatchRequest,
                             error: str) -> DispatchResponse:
        """构建错误响应"""
        return DispatchResponse(
            request_id=request.request_id,
            dispatcher_id=self.dispatcher_id,
            level=request.level or Level.L2_LOGIC,
            time_spent=0.0,
            dispatched_to=[],
            confidence=0.0,
            output={},
            state=DispatcherState.FAILED,
            error=error
        )

    def _update_metrics(self, elapsed: float):
        """更新指标"""
        self._metrics["total_time"] += elapsed
        self._metrics["avg_time"] = (
            self._metrics["total_time"] / self._metrics["total_calls"]
        )

    def get_state(self) -> DispatcherState:
        return self.state

    def get_metrics(self) -> Dict:
        return self._metrics.copy()

    def reset_metrics(self):
        """重置指标"""
        self._metrics = {
            "total_calls": 0,
            "failed_calls": 0,
            "avg_time": 0.0,
            "total_time": 0.0
        }


class LevelAssessor:
    """问题级别评估器"""

    # 关键词权重配置
    KEYWORD_PATTERNS = {
        "L1": [
            "是什么", "如何", "怎么", "告诉我", "查询",
            "时间", "天气", "紧急", "马上", "立刻", "现在",
            "多少", "几点", "谁", "哪里"
        ],
        "L2": [
            "分析", "推理", "判断", "论证", "评估", "比较",
            "数据", "统计", "检验", "验证", "逻辑", "证明",
            "为什么", "原因", "依据"
        ],
        "L3": [
            "战略", "规划", "转型", "策划", "方案", "系统",
            "全面", "深度", "复杂", "综合", "融合", "整合",
            "优化", "改进", "设计", "架构"
        ],
        "L4": [
            "创新", "突破", "颠覆", "创造", "根本", "本质",
            "核心", "理论", "哲学", "智慧", "直觉", "极致",
            "革命", "范式", "重新定义", "前所未有的"
        ]
    }

    @classmethod
    def assess(cls, problem: Dict[str, Any]) -> tuple:
        """
        评估问题级别

        Returns:
            (level, confidence) 元组
        """
        description = problem.get("description", "")
        context = problem.get("context", "")
        text = (description + " " + context).lower()

        # 统计各级别关键词命中
        scores = {"L1": 0, "L2": 0, "L3": 0, "L4": 0}

        for level, keywords in cls.KEYWORD_PATTERNS.items():
            for kw in keywords:
                if kw in text:
                    scores[level] += 1

        # 问题长度加成
        if len(description) > 200:
            scores["L3"] += 1
            scores["L4"] += 1
        elif len(description) > 500:
            scores["L4"] += 2

        # 决定级别
        if sum(scores.values()) == 0:
            return Level.L2_LOGIC, 0.7

        max_level = max(scores, key=scores.get)
        max_score = scores[max_level]

        # 计算置信度
        total = sum(scores.values())
        confidence = min(0.95, max_score / (total + 1) * 3 + 0.5)

        level_map = {
            "L1": Level.L1_INSTINCT,
            "L2": Level.L2_LOGIC,
            "L3": Level.L3_WISDOM,
            "L4": Level.L4_INTUITION
        }

        return level_map.get(max_level, Level.L2_LOGIC), confidence


class DispatchEngine:
    """
    SageDispatch 核心调度引擎 - 懒加载版
    
    优化策略：
    1. 预注册：只注册调度器ID和工厂函数，不创建实例
    2. 懒实例化：首次使用时才创建调度器实例
    3. LRU缓存：已创建的调度器实例被缓存复用
    """

    # 类级别调度器注册表（延迟导入）
    _DISPATCHER_REGISTRY: Dict[str, Dict] = {}

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self._dispatchers: Dict[str, BaseDispatcher] = {}  # 实例缓存
        self._factories: Dict[str, Callable] = {}           # 工厂函数
        self._dispatcher_defs: Dict[str, Dict] = {}         # 调度器定义信息
        self._load_stats: Dict[str, float] = {}             # 加载统计
        self._lazy_mode = True  # 默认开启懒加载
        self._load_times: Dict[str, float] = {}             # 各调度器加载时间
        
        # 预注册所有调度器（不创建实例）
        self._register_default_dispatchers()

    def _register_default_dispatchers(self):
        """预注册默认调度器（仅注册ID和工厂函数，不创建实例）"""
        # 定义调度器注册信息
        dispatcher_defs = {
            "SD-F2": {
                "name": "四级调度总控",
                "factory_module": "dispatchers",
                "factory_class": "FourLevelDispatchController",
                "priority": 0,
            },
            "SD-P1": {
                "name": "问题调度器",
                "factory_module": "dispatchers",
                "factory_class": "ProblemDispatcher",
                "priority": 1,
            },
            "SD-R1": {
                "name": "三层推理监管",
                "factory_module": "dispatchers",
                "factory_class": "ThreeLayerReasoning",
                "priority": 2,
            },
            "SD-R2": {
                "name": "谬误检测",
                "factory_module": "dispatchers",
                "factory_class": "FallacyChecker",
                "priority": 3,
            },
            "SD-F1": {
                "name": "学派融合",
                "factory_module": "dispatchers",
                "factory_class": "SchoolFusion",
                "priority": 4,
            },
            "SD-D1": {
                "name": "轻量深度推理",
                "factory_module": "dispatchers",
                "factory_class": "SuperReasoning",
                "factory_args": ("light",),
                "priority": 5,
            },
            "SD-D2": {
                "name": "标准深度推理",
                "factory_module": "dispatchers",
                "factory_class": "SuperReasoning",
                "factory_args": ("standard",),
                "priority": 6,
            },
            "SD-D3": {
                "name": "极致深度推理",
                "factory_module": "dispatchers",
                "factory_class": "SuperReasoning",
                "factory_args": ("deep",),
                "priority": 7,
            },
            "SD-C1": {
                "name": "太极阴阳决策",
                "factory_module": "dispatchers",
                "factory_class": "YinYangDecision",
                "priority": 8,
            },
            "SD-C2": {
                "name": "神之架构决策",
                "factory_module": "dispatchers",
                "factory_class": "DivineArchitecture",
                "priority": 9,
            },
            "SD-E1": {
                "name": "五步主链执行",
                "factory_module": "dispatchers",
                "factory_class": "ChainExecutor",
                "priority": 10,
            },
            "SD-L1": {
                "name": "学习进化",
                "factory_module": "dispatchers",
                "factory_class": "ResultTracker",
                "priority": 11,
            },
        }
        
        for dispatcher_id, def_info in dispatcher_defs.items():
            # 保存定义信息用于延迟导入
            self._dispatcher_defs[dispatcher_id] = def_info
            
            # 创建延迟工厂函数
            self._factories[dispatcher_id] = self._make_lazy_factory(def_info)

    def _make_lazy_factory(self, def_info: Dict) -> Callable:
        """创建懒加载工厂函数"""
        module_name = def_info["factory_module"]
        class_name = def_info["factory_class"]
        factory_args = def_info.get("factory_args", ())
        
        def factory():
            # 延迟导入
            try:
                from dispatchers import (
                    FourLevelDispatchController,
                    ProblemDispatcher,
                    ThreeLayerReasoning,
                    FallacyChecker,
                    SchoolFusion,
                    SuperReasoning,
                    YinYangDecision,
                    DivineArchitecture,
                    ChainExecutor,
                    ResultTracker,
                )
            except ImportError:
                from knowledge_cells.dispatchers import (
                    FourLevelDispatchController,
                    ProblemDispatcher,
                    ThreeLayerReasoning,
                    FallacyChecker,
                    SchoolFusion,
                    SuperReasoning,
                    YinYangDecision,
                    DivineArchitecture,
                    ChainExecutor,
                    ResultTracker,
                )
            
            class_map = {
                "FourLevelDispatchController": FourLevelDispatchController,
                "ProblemDispatcher": ProblemDispatcher,
                "ThreeLayerReasoning": ThreeLayerReasoning,
                "FallacyChecker": FallacyChecker,
                "SchoolFusion": SchoolFusion,
                "SuperReasoning": SuperReasoning,
                "YinYangDecision": YinYangDecision,
                "DivineArchitecture": DivineArchitecture,
                "ChainExecutor": ChainExecutor,
                "ResultTracker": ResultTracker,
            }
            
            cls = class_map.get(class_name)
            if cls is None:
                raise ValueError(f"Unknown dispatcher class: {class_name}")
            
            return cls(*factory_args)
        
        return factory

    def register(self, dispatcher_id: str, factory: Callable):
        """注册调度器工厂函数"""
        self._factories[dispatcher_id] = factory

    def register_lazy(self, dispatcher_id: str, def_info: Dict):
        """懒注册调度器（保存定义信息）"""
        self._dispatcher_defs[dispatcher_id] = def_info
        self._factories[dispatcher_id] = self._make_lazy_factory(def_info)

    def get_dispatcher(self, dispatcher_id: str) -> BaseDispatcher:
        """获取调度器实例（懒加载）"""
        import time
        
        if dispatcher_id not in self._dispatchers:
            if dispatcher_id in self._factories:
                start = time.perf_counter()
                self._dispatchers[dispatcher_id] = self._factories[dispatcher_id]()
                elapsed = (time.perf_counter() - start) * 1000
                self._load_times[dispatcher_id] = elapsed
            else:
                raise ValueError(f"Unknown dispatcher: {dispatcher_id}")
        return self._dispatchers[dispatcher_id]

    def dispatch(self, problem: Any,
                level: Optional[Level] = None,
                dispatcher_id: str = "SD-F2",
                **kwargs) -> DispatchResponse:
        """快捷调度入口"""
        if isinstance(problem, str):
            problem_dict = {
                "description": problem,
                "keywords": self._extract_keywords(problem),
                "context": "",
                "scenario": "general"
            }
        else:
            problem_dict = problem

        request = DispatchRequest(
            problem=problem_dict,
            forced_level=level,
            **kwargs
        )

        dispatcher = self.get_dispatcher(dispatcher_id)
        return dispatcher.dispatch(request)

    def chain(self, problem: Any, path: List[str], **kwargs) -> List[DispatchResponse]:
        """链式调度"""
        results = []
        current_output = None

        for dispatcher_id in path:
            if current_output:
                kwargs["parent_output"] = current_output
            response = self.dispatch(problem, dispatcher_id=dispatcher_id, **kwargs)
            results.append(response)
            current_output = response.output

        return results

    def smart_dispatch(self, problem: Any, **kwargs) -> DispatchResponse:
        """智能调度"""
        return self.dispatch(problem, dispatcher_id="SD-F2", **kwargs)

    def get_metrics(self) -> Dict:
        """获取所有调度器指标"""
        metrics = {}
        for dispatcher_id, dispatcher in self._dispatchers.items():
            metrics[dispatcher_id] = dispatcher.get_metrics()
        return metrics

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        important_words = [
            "分析", "战略", "规划", "创新", "紧急", "决策",
            "判断", "推理", "评估", "预测", "优化", "创新"
        ]
        for word in important_words:
            if word in text:
                keywords.append(word)
        return keywords[:5]


# 全局实例
_engine: Optional[DispatchEngine] = None
_engine_lock = __import__('threading').Lock()


def get_engine() -> DispatchEngine:
    """获取全局调度引擎（线程安全）"""
    global _engine
    if _engine is None:
        with _engine_lock:
            if _engine is None:
                _engine = DispatchEngine()
    return _engine


def dispatch(problem: Any, level: Optional[Level] = None,
            dispatcher_id: str = "SD-F2", **kwargs) -> DispatchResponse:
    """快捷调度函数"""
    return get_engine().dispatch(problem, level, dispatcher_id, **kwargs)


def chain(problem: Any, path: List[str], **kwargs) -> List[DispatchResponse]:
    """快捷链式调度函数"""
    return get_engine().chain(problem, path, **kwargs)


def smart_dispatch(problem: Any, **kwargs) -> DispatchResponse:
    """快捷智能调度函数"""
    return get_engine().smart_dispatch(problem, **kwargs)


# ==================== 神政轨监督集成 ====================

def _get_oversight():
    """获取监督实例（延迟导入避免循环依赖）"""
    try:
        from .divine_oversight import get_oversight, OversightCategory
        return get_oversight()
    except ImportError:
        return None


def _record_dispatch_oversight(problem: Any, response: DispatchResponse,
                                dispatcher_id: str = "SD-F2") -> None:
    """记录调度监督数据"""
    oversight = _get_oversight()
    if oversight is None:
        return

    try:
        from .divine_oversight import OversightCategory

        # 记录过程
        oversight.record(
            module="SageDispatch",
            action=f"dispatch_{dispatcher_id}",
            category=OversightCategory.PROCESS,
            input_data={"problem": str(problem)[:100], "level": str(response.level)},
            output_data={"dispatched_to": response.dispatched_to, "state": response.state.value}
        )

        # 记录成果
        if response.output:
            oversight.record(
                module="SageDispatch",
                action=f"result_{dispatcher_id}",
                category=OversightCategory.RESULT,
                input_data={"problem": str(problem)[:100]},
                output_data={"has_output": bool(response.output), "confidence": response.confidence}
            )

    except Exception:
        pass  # 监督失败不影响主流程


# 为 dispatch 添加监督
_original_dispatch = dispatch
_original_chain = chain
_original_smart_dispatch = smart_dispatch


def dispatch(problem: Any, level: Optional[Level] = None,
            dispatcher_id: str = "SD-F2", **kwargs) -> DispatchResponse:
    """快捷调度函数（带监督）"""
    response = _original_dispatch(problem, level, dispatcher_id, **kwargs)
    _record_dispatch_oversight(problem, response, dispatcher_id)
    return response


def chain(problem: Any, path: List[str], **kwargs) -> List[DispatchResponse]:
    """快捷链式调度函数（带监督）"""
    results = _original_chain(problem, path, **kwargs)
    oversight = _get_oversight()
    if oversight:
        try:
            from .divine_oversight import OversightCategory
            oversight.record(
                module="SageDispatch",
                action="chain_execution",
                category=OversightCategory.PROCESS,
                input_data={"problem": str(problem)[:100], "path": path},
                output_data={"chain_length": len(results)}
            )
        except Exception:
            pass
    return results
