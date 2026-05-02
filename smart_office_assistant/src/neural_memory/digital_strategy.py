# -*- coding: utf-8 -*-
"""
NeuralMemory v7.0 - 数字大脑策略层
=====================================

[品牌定位]
DigitalStrategy 是 NeuralMemory 的策略决策核心，
负责问题识别、智慧调度、LLM增强、进化触发等策略判断。
执行全部委托给 NeuralExecutor。

[架构角色]
  用户请求
      │
      ▼
  NeuralMemory (统一入口)
      │
      ├──► DigitalStrategy (策略层) ← 本文件
      │         │
      │         ├──► 问题类型识别
      │         ├──► 智慧学派调度
      │         ├──► LLM增强策略
      │         └──► 进化触发决策
      │
      └──► NeuralExecutor (执行层)
                │
                ├──► 记忆检索/存储
                ├──► 生命周期管理
                ├──► 藏书阁同步
                └──► 学习强化

版本: v7.0.0
更新: 2026-04-30
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .neural_executor import NeuralExecutor

logger = logging.getLogger("NeuralMemory.DigitalStrategy")


# ═══════════════════════════════════════════════════════════════
#  记忆层级 (统一版 - 合并DigitalBrain+NeuralMemory)
# ═══════════════════════════════════════════════════════════════

class MemoryLevel(Enum):
    """统一记忆层级 (v7.0)
    
    合并来源:
    - DigitalBrain: SENSORY/WORKING/SHORT_TERM/LONG_TERM/ETERNAL
    - NeuralMemory: TIER_1_WORKING/TIER_2_SHORT/ETERNAL
    """
    # 感官记忆 (毫秒级)
    SENSORY = "sensory"
    # 工作记忆 (秒级)
    WORKING = "working"
    # 短期记忆 (分钟级)
    SHORT_TERM = "short_term"
    # 长期记忆 (持久)
    LONG_TERM = "long_term"
    # 永恒记忆 (永不遗忘)
    ETERNAL = "eternal"

    @property
    def priority(self) -> int:
        """优先级 (数字越小越重要)"""
        priorities = {
            MemoryLevel.SENSORY: 0,
            MemoryLevel.WORKING: 1,
            MemoryLevel.SHORT_TERM: 2,
            MemoryLevel.LONG_TERM: 3,
            MemoryLevel.ETERNAL: 4,
        }
        return priorities.get(self, 2)


class BrainState(Enum):
    """大脑状态"""
    INITIALIZING = "initializing"
    READY = "ready"
    PROCESSING = "processing"
    EVOLVING = "evolving"
    SLEEPING = "sleeping"
    ERROR = "error"


# ═══════════════════════════════════════════════════════════════
#  思维记录
# ═══════════════════════════════════════════════════════════════

@dataclass
class StrategyThought:
    """策略层思维记录"""
    thought_id: str
    content: str
    source: str  # "memory", "wisdom", "llm", "strategy"
    timestamp: float = field(default_factory=time.time)
    confidence: float = 0.5
    processing_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # v7.0 新增：执行轨迹
    executor_calls: List[Dict] = field(default_factory=list)  # 执行层调用记录


@dataclass
class StrategyEvolution:
    """策略进化记录"""
    evolution_id: str
    evolution_type: str  # "memory_consolidation", "strategy_update", "architecture_adjust"
    trigger_reason: str
    changes: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    success: bool = True
    improvements: List[str] = field(default_factory=list)


@dataclass
class StrategyHealth:
    """策略层健康状态"""
    overall_score: float  # 0-100
    strategy_health: float  # 策略健康
    executor_health: float  # 执行层健康
    evolution_health: float  # 进化健康
    llm_health: float  # LLM健康
    
    active_thoughts: int = 0
    pending_evolutions: int = 0
    last_evolution_time: Optional[float] = None
    uptime_seconds: float = 0.0
    
    anomalies: List[Dict] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
#  策略配置
# ═══════════════════════════════════════════════════════════════

@dataclass
class StrategyConfig:
    """数字大脑策略配置 (v7.0)"""
    # 策略开关
    enable_wisdom_dispatch: bool = True
    enable_llm_enhancement: bool = True
    enable_autonomous_evolution: bool = True
    
    # 调度配置
    dispatch_timeout: float = 10.0
    dispatch_wuwei_enabled: bool = True
    
    # LLM配置
    llm_timeout: float = 30.0
    llm_fallback_to_template: bool = True
    prefer_local_llm: bool = True
    
    # 进化配置
    evolution_interval_minutes: int = 60
    evolution_auto_optimize: bool = True
    evolution_risk_threshold: str = "medium"
    min_thoughts_before_evolve: int = 10
    
    # 执行层配置
    executor_max_workers: int = 4
    executor_encoding_dim: int = 384


# ═══════════════════════════════════════════════════════════════
#  策略层核心
# ═══════════════════════════════════════════════════════════════

class DigitalStrategy:
    """
    数字大脑策略层 (v7.0)
    
    职责:
    1. 问题类型识别
    2. 智慧学派调度
    3. LLM增强决策
    4. 进化触发判断
    
    执行全部委托给 NeuralExecutor。
    """

    _instance: Optional['DigitalStrategy'] = None

    def __init__(
        self,
        config: Optional[StrategyConfig] = None,
        executor: Optional['NeuralExecutor'] = None
    ):
        self.config = config or StrategyConfig()
        self.executor = executor  # 由NeuralMemory统一注入
        
        self.state = BrainState.INITIALIZING
        self._start_time = time.time()
        
        # 思维历史
        self._thought_history: List[StrategyThought] = []
        self._thought_lock = asyncio.Lock()
        
        # 进化历史
        self._evolution_history: List[StrategyEvolution] = []
        self._evolution_lock = asyncio.Lock()
        
        # 进化任务
        self._evolution_task: Optional[asyncio.Task] = None
        
        logger.info("[DigitalStrategy] 策略层初始化中...")
        
        # 延迟初始化（仅在有运行中事件循环时才创建任务）
        # 否则由首次 think() 调用时触发惰性初始化
        self._init_deferred = True
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._initialize())
        except RuntimeError:
            # 无运行中事件循环，标记为待惰性初始化
            self._init_deferred = True

    async def _initialize(self):
        """初始化策略层（幂等）"""
        if getattr(self, '_initialized', False):
            return
        self._initialized = True
        try:
            # 启动进化循环
            if self.config.enable_autonomous_evolution:
                self._evolution_task = asyncio.create_task(self._evolution_loop())
            
            self.state = BrainState.READY
            logger.info("[DigitalStrategy] 策略层初始化完成!")
            
        except Exception as e:
            self.state = BrainState.ERROR
            logger.error(f"[DigitalStrategy] 初始化失败: {e}")

    # ═══════════════════════════════════════════════════════════════
    #  主入口
    # ═══════════════════════════════════════════════════════════════

    async def think(self, query: str, context: Optional[Dict] = None) -> StrategyThought:
        """
        核心思维方法 - 策略决策 + 执行委托
        
        流程:
        1. 问题类型识别
        2. 从执行层检索相关记忆
        3. 智慧学派调度
        4. LLM增强 (可选)
        5. 委托执行层存储记忆
        6. 触发进化检查
        
        Args:
            query: 输入问题
            context: 上下文
            
        Returns:
            StrategyThought: 策略思维结果
        """
        start_time = time.time()
        self.state = BrainState.PROCESSING
        
        # 惰性初始化（如果 __init__ 时无事件循环，由 think() 触发）
        if getattr(self, '_init_deferred', False):
            self._init_deferred = False
            self.state = BrainState.INITIALIZING
            try:
                await self._initialize()
            except Exception:
                self.state = BrainState.ERROR
        
        thought = StrategyThought(
            thought_id=f"thought_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            content="",
            source="",
            metadata=context or {},
            executor_calls=[]
        )
        
        try:
            # 1. 问题类型识别 (策略)
            problem_type = self._identify_problem_type(query)
            thought.metadata["problem_type"] = problem_type
            
            # 2. 记忆检索 (委托执行层)
            executor_record = await self.executor.record_operation("retrieve")
            memories = await self._retrieve_memories(query)
            thought.executor_calls.append(executor_record)
            
            # 3. 智慧调度 (策略)
            wisdom_result = await self._dispatch_wisdom(query, memories)
            thought.metadata["wisdom"] = wisdom_result
            
            # 4. LLM增强 (策略，可选)
            llm_result = None
            if self.config.enable_llm_enhancement:
                llm_result = await self._enhance_with_llm(query, memories, wisdom_result)
                thought.metadata["llm"] = llm_result
            
            # 5. 整合结果
            thought.content = (
                llm_result.get("answer") if llm_result 
                else wisdom_result.get("answer", "")
            )
            thought.source = (
                llm_result.get("source") if llm_result 
                else wisdom_result.get("source", "wisdom")
            )
            thought.confidence = max(
                llm_result.get("confidence", 0.5) if llm_result else 0.5,
                wisdom_result.get("confidence", 0.5)
            )
            
            # 6. 委托执行层存储记忆
            if thought.content:
                await self._consolidate_memory(query, thought)
            
            # 7. 触发进化检查
            await self._check_evolution_trigger(query, thought)
            
        except Exception as e:
            logger.error(f"[DigitalStrategy] 思考过程错误: {e}")
            thought.content = f"处理错误: {e}"
            thought.confidence = 0.0
        
        thought.processing_time_ms = (time.time() - start_time) * 1000
        self.state = BrainState.READY
        
        # 记录思维
        async with self._thought_lock:
            self._thought_history.append(thought)
            if len(self._thought_history) > 1000:
                self._thought_history = self._thought_history[-500:]
        
        return thought

    # ═══════════════════════════════════════════════════════════════
    #  问题识别
    # ═══════════════════════════════════════════════════════════════

    def _identify_problem_type(self, query: str):
        """识别问题类型 — 委托给 WisdomDispatcher（返回 ProblemType 枚举）"""
        try:
            try:
                from ..intelligence.dispatcher.wisdom_dispatcher import WisdomDispatcher
            except ImportError:
                from intelligence.dispatcher.wisdom_dispatcher import WisdomDispatcher
            dispatcher = WisdomDispatcher()
            return dispatcher.identify_problem_type(query)
        except Exception as e:
            logger.warning(f"[DigitalStrategy] 问题识别失败: {e}，使用默认类型")
            # 回退：使用关键词匹配
            try:
                from ..intelligence.dispatcher.wisdom_dispatch._dispatch_enums import ProblemType
            except ImportError:
                from intelligence.dispatcher.wisdom_dispatch._dispatch_enums import ProblemType
            query_lower = query.lower()
            if any(k in query_lower for k in ["分析", "对比", "compare"]):
                return ProblemType.MARKET_ANALYSIS
            elif any(k in query_lower for k in ["战略", "策略", "规划"]):
                return ProblemType.STRATEGY
            elif any(k in query_lower for k in ["增长", "成长", "突破"]):
                return ProblemType.GROWTH_MINDSET
            elif any(k in query_lower for k in ["创新", "变革", "改变"]):
                return ProblemType.CHANGE
            elif any(k in query_lower for k in ["决策", "判断", "decide"]):
                return ProblemType.LEADERSHIP
            elif any(k in query_lower for k in ["预测", "forecast"]):
                return ProblemType.TIMING
            elif any(k in query_lower for k in ["优化", "改进"]):
                return ProblemType.OPTIMIZATION
            else:
                return ProblemType.SYSTEM_THINKING

    # ═══════════════════════════════════════════════════════════════
    #  记忆检索 (委托执行层)
    # ═══════════════════════════════════════════════════════════════

    async def _retrieve_memories(self, query: str) -> List[Dict]:
        """从执行层检索相关记忆"""
        if not self.executor:
            return []
        
        try:
            # 委托给执行层
            results = await self.executor.retrieve(
                query=query,
                top_k=10
            )
            return results
        except Exception as e:
            logger.warning(f"[DigitalStrategy] 记忆检索失败: {e}")
            return []

    # ═══════════════════════════════════════════════════════════════
    #  智慧调度
    # ═══════════════════════════════════════════════════════════════

    async def _dispatch_wisdom(self, query: str, memories: List[Dict]) -> Dict:
        """智慧学派调度 — 真正调用 WisdomDispatcher 获取推理内容"""
        if not self.config.enable_wisdom_dispatch:
            return {"answer": "", "confidence": 0.0, "source": "wisdom"}

        try:
            try:
                from ..intelligence.dispatcher.wisdom_dispatcher import WisdomDispatcher
            except ImportError:
                from intelligence.dispatcher.wisdom_dispatcher import WisdomDispatcher
            dispatcher = WisdomDispatcher()

            # 问题类型识别（返回 ProblemType 枚举）
            problem_type = self._identify_problem_type(query)
            problem_type_name = problem_type.name if hasattr(problem_type, 'name') else str(problem_type)

            # 调用智慧推荐引擎获取真实推理内容
            recommendations = dispatcher.get_wisdom_recommendation(query, problem_type)

            if recommendations:
                # 取最优学派推荐
                top_rec = max(recommendations, key=lambda r: r.confidence)
                answer = (
                    f"【{top_rec.school.value}学派】\n"
                    f"方法: {top_rec.primary_method}\n"
                    f"推理: {top_rec.reasoning}\n"
                    f"建议: {top_rec.advice}\n"
                    f"古籍来源: {top_rec.ancient_source}\n"
                    f"现代应用: {top_rec.modern_application}"
                )
                return {
                    "answer": answer,
                    "confidence": top_rec.confidence,
                    "source": "wisdom",
                    "problem_type": problem_type_name,
                    "school": top_rec.school.value,
                    "recommendations": [
                        {"school": r.school.value, "confidence": r.confidence, "method": r.primary_method}
                        for r in recommendations[:3]
                    ]
                }

            # 回退：从 problem_school_mapping 获取学派信息
            school_mapping = getattr(dispatcher, 'problem_school_mapping', {})
            for key, schools in school_mapping.items():
                if key == problem_type and schools:
                    top_school, weight = schools[0]
                    return {
                        "answer": f"[智慧调度] 问题类型: {problem_type_name}, 学派: {top_school.value}",
                        "confidence": weight,
                        "source": "wisdom",
                        "problem_type": problem_type_name,
                        "school": top_school.value
                    }

            return {
                "answer": f"[智慧调度] 问题类型: {problem_type_name}，未匹配到专项学派",
                "confidence": 0.4,
                "source": "wisdom",
                "problem_type": problem_type_name
            }

        except Exception as e:
            logger.warning(f"[DigitalStrategy] 智慧调度失败: {e}")
            return {"answer": "", "confidence": 0.0, "source": "wisdom"}

    # ═══════════════════════════════════════════════════════════════
    #  LLM增强
    # ═══════════════════════════════════════════════════════════════

    async def _enhance_with_llm(
        self,
        query: str,
        memories: List[Dict],
        wisdom_result: Dict
    ) -> Optional[Dict]:
        """
        LLM增强推理 (策略决策)
        
        透明级联:
        1. 优先本地LLM
        2. 本地失败 → DualModelService
        3. 全部失败 → 返回wisdom结果
        """
        enhanced_prompt = self._build_enhanced_prompt(query, memories, wisdom_result)
        
        # 策略1: 尝试本地LLM
        try:
            result = await self._try_local_llm(enhanced_prompt)
            if result:
                return result
        except Exception as e:
            logger.warning(f"[DigitalStrategy] 本地LLM失败: {e}")
        
        # 策略2: 尝试DualModelService
        try:
            result = await self._try_dual_model(enhanced_prompt)
            if result:
                return result
        except Exception as e:
            logger.warning(f"[DigitalStrategy] DualModel失败: {e}")
        
        # 策略3: 降级到wisdom结果
        return None

    def _build_enhanced_prompt(
        self,
        query: str,
        memories: List[Dict],
        wisdom_result: Dict
    ) -> str:
        """构建增强提示"""
        context_text = ""
        if memories:
            context_text = "\n相关记忆:\n" + "\n".join([
                f"- {m.get('content', m.get('title', ''))[:100]}"
                for m in memories[:3]
            ])
        
        wisdom_context = ""
        if wisdom_result.get("school"):
            wisdom_context = f"\n智慧学派: {wisdom_result['school']}"
        
        return f"""基于以下上下文回答问题:

问题: {query}
{context_text}
{wisdom_context}

请给出简洁、准确的回答。"""

    async def _try_local_llm(self, prompt: str) -> Optional[Dict]:
        """尝试本地LLM"""
        try:
            from core.local_llm_manager import LocalLLMManager
            
            llm = LocalLLMManager(auto_start=True)
            if llm.is_ready:
                result = llm.dispatch(prompt, request_timeout=self.config.llm_timeout)
                if result and not result.error:
                    return {
                        "answer": result.text,
                        "confidence": 0.7 if result.text else 0.3,
                        "source": "local_llm",
                        "tokens": getattr(result, 'tokens', 0)
                    }
        except Exception:
            pass
        return None

    async def _try_dual_model(self, prompt: str) -> Optional[Dict]:
        """尝试DualModelService"""
        try:
            from src.tool_layer.dual_model_service import get_dual_model_service
            
            dual_service = get_dual_model_service()
            if dual_service:
                response = dual_service.chat(
                    prompt,
                    prefer_local=self.config.prefer_local_llm
                )
                if response:
                    return {
                        "answer": response.get("text", ""),
                        "confidence": 0.6,
                        "source": "dual_model"
                    }
        except Exception:
            pass
        return None

    # ═══════════════════════════════════════════════════════════════
    #  记忆整合 (委托执行层)
    # ═══════════════════════════════════════════════════════════════

    async def _consolidate_memory(self, query: str, thought: StrategyThought):
        """委托执行层存储记忆 — 闭环核心"""
        if not self.executor:
            return
        
        try:
            executor_record = await self.executor.record_operation("add")
            
            # 序列化 problem_type（枚举 → 字符串）
            problem_type = thought.metadata.get("problem_type", "")
            if hasattr(problem_type, 'name'):
                problem_type = problem_type.name
            
            wisdom_meta = thought.metadata.get("wisdom", {})
            school = wisdom_meta.get("school", "")
            recommendations = wisdom_meta.get("recommendations", [])
            
            # 委托给执行层存储
            await self.executor.add(
                content=thought.content,
                query=query,
                metadata={
                    "source": thought.source,
                    "confidence": thought.confidence,
                    "problem_type": problem_type,
                    "school": school,
                    "recommendations": recommendations,
                    "query": query,
                    "thought_id": thought.thought_id,
                }
            )
            
            thought.executor_calls.append(executor_record)
            logger.info(f"[DigitalStrategy] 记忆整合完成: {thought.thought_id}")
            
        except Exception as e:
            logger.warning(f"[DigitalStrategy] 记忆整合失败: {e}")

    # ═══════════════════════════════════════════════════════════════
    #  进化机制
    # ═══════════════════════════════════════════════════════════════

    async def _check_evolution_trigger(self, query: str, thought: StrategyThought):
        """检查是否触发进化 — 闭环机制"""
        if not self.config.enable_autonomous_evolution:
            return
        
        async with self._thought_lock:
            thought_count = len(self._thought_history)
            # 分析历史中的问题类型分布
            problem_types = [t.metadata.get("problem_type", "") for t in self._thought_history[-10:]]
            if problem_types and hasattr(problem_types[0], 'name'):
                problem_types = [pt.name for pt in problem_types if pt]
        
        # 达到进化阈值
        if thought_count >= self.config.min_thoughts_before_evolve:
            # 触发条件1: 低置信度
            if thought.confidence < 0.4:
                await self._trigger_evolution("low_confidence", query, thought)
                return
            
            # 触发条件2: 同一问题类型频繁出现（>3次）
            current_pt = thought.metadata.get("problem_type", "")
            if hasattr(current_pt, 'name'):
                current_pt = current_pt.name
            if current_pt and problem_types.count(current_pt) >= 3:
                await self._trigger_evolution(
                    f"pattern_detected:{current_pt}", query, thought
                )
                return
            
            # 触发条件3: 连续3次以上置信度下降
            recent = self._thought_history[-3:]
            if len(recent) >= 3:
                confidences = [getattr(t, 'confidence', 0) for t in recent]
                if all(c2 < c1 for c1, c2 in zip(confidences, confidences[1:])):
                    await self._trigger_evolution("declining_confidence", query, thought)

    async def _trigger_evolution(
        self,
        trigger_type: str,
        query: str,
        thought: StrategyThought
    ):
        """触发进化"""
        evolution = StrategyEvolution(
            evolution_id=f"evo_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            evolution_type="diagnostic_cycle",
            trigger_reason=f"触发类型: {trigger_type}, 问题: {query[:50]}",
            changes={
                "confidence": thought.confidence,
                "problem_type": getattr(thought.metadata.get("problem_type", ""), 'name', str(thought.metadata.get("problem_type", ""))),
            }
        )
        
        async with self._evolution_lock:
            self._evolution_history.append(evolution)
        
        logger.info(f"[DigitalStrategy] 触发进化: {evolution.evolution_id}")

    async def _evolution_loop(self):
        """进化循环"""
        interval = self.config.evolution_interval_minutes * 60
        
        while self.state not in (BrainState.ERROR, BrainState.SLEEPING):
            try:
                self.state = BrainState.EVOLVING
                logger.info("[DigitalStrategy] 执行诊断周期...")
                
                # 检查执行层健康
                if self.executor:
                    health = await self.executor.get_health()
                    if health:
                        logger.info(f"[DigitalStrategy] 执行层健康度: {health.get('score', 0):.1f}")
                
                self.state = BrainState.READY
                
            except Exception as e:
                logger.error(f"[DigitalStrategy] 进化循环错误: {e}")
            
            await asyncio.sleep(interval)

    # ═══════════════════════════════════════════════════════════════
    #  健康检查
    # ═══════════════════════════════════════════════════════════════

    async def get_health(self) -> StrategyHealth:
        """获取策略层健康状态"""
        executor_health = 0.0
        if self.executor:
            h = await self.executor.get_health()
            executor_health = h.get("score", 0) if h else 0.0
        
        return StrategyHealth(
            overall_score=(executor_health + 90) / 2,  # 简化计算
            strategy_health=95.0,
            executor_health=executor_health,
            evolution_health=90.0 if self._evolution_task else 0.0,
            llm_health=85.0,
            active_thoughts=len(self._thought_history),
            pending_evolutions=0,
            last_evolution_time=self._evolution_history[-1].timestamp if self._evolution_history else None,
            uptime_seconds=time.time() - self._start_time
        )

    # ═══════════════════════════════════════════════════════════════
    #  工具方法
    # ═══════════════════════════════════════════════════════════════

    def get_thought_history(self, limit: int = 10) -> List[StrategyThought]:
        """获取思维历史"""
        return self._thought_history[-limit:]

    def get_evolution_history(self, limit: int = 10) -> List[StrategyEvolution]:
        """获取进化历史"""
        return self._evolution_history[-limit:]

    async def shutdown(self):
        """关闭策略层"""
        if self._evolution_task:
            self._evolution_task.cancel()
        self.state = BrainState.SLEEPING
        logger.info("[DigitalStrategy] 策略层已关闭")

    # ════════════════════════════════════════════════════════════════
    #  兼容 DigitalBrainCore 的额外方法 (v7.0 新增)
    # ════════════════════════════════════════════════════════════════

    async def initialize(self):
        """兼容 DigitalBrainCore.initialize()"""
        await self._initialize()

    async def purify(self, mode: str = "auto") -> Dict[str, Any]:
        """
        兼容 DigitalBrainCore.purify()
        执行自我净化（委托给 NeuralExecutor 的生命周期管理）
        """
        results = {
            "memories_cleaned": 0,
            "duplicates_removed": 0,
            "weak_memories_reinforced": 0,
            "optimizations_applied": [],
            "duration_ms": 0.0,
        }
        start_time = time.time()
        try:
            if self.executor:
                # 触发执行层的生命周期管理
                if hasattr(self.executor, 'apply_decay'):
                    decay_results = self.executor.apply_decay()
                    results["memories_cleaned"] = len(decay_results) if decay_results else 0
            results["duration_ms"] = (time.time() - start_time) * 1000
        except Exception as e:
            logger.warning(f"[DigitalStrategy] purify 失败: {e}")
            results["error"] = str(e)
        return results

    async def evolve(self, target: Optional[str] = None) -> StrategyEvolution:
        """
        兼容 DigitalBrainCore.evolve()
        执行系统进化（触发一次诊断周期）
        """
        evolution = StrategyEvolution(
            evolution_id=f"evo_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            evolution_type="manual_trigger",
            trigger_reason=f"手动触发: {target or 'all'}",
            changes={},
        )
        try:
            await self._evolution_loop()
            evolution.success = True
        except Exception as e:
            evolution.success = False
            evolution.changes["error"] = str(e)
        async with self._evolution_lock:
            self._evolution_history.append(evolution)
        return evolution

    def get_stats(self) -> Dict[str, Any]:
        """兼容 DigitalBrainCore.get_stats()"""
        uptime = time.time() - self._start_time
        with self._thought_lock:
            thought_count = len(self._thought_history)
            recent = self._thought_history[-10:]
        return {
            "state": self.state.value,
            "uptime_seconds": uptime,
            "thoughts": {
                "total": thought_count,
                "recent_avg_confidence": (
                    sum(t.confidence for t in recent) / len(recent) if recent else 0
                ),
            },
            "evolutions": {"total": len(self._evolution_history)},
        }


# ════════════════════════════════════════════════════════════════
#  兼容别名导出 (让 digital_brain/__init__.py 的 __getattr__ 继续工作)
# ════════════════════════════════════════════════════════════════

BrainThought = StrategyThought
BrainEvolution = StrategyEvolution
BrainHealth = StrategyHealth


class BrainConfig:
    """
    兼容 DigitalBrainCore.BrainConfig
    v7.0: 薄包装层，内部转换为 StrategyConfig
    """
    def __init__(
        self,
        enable_neural_memory: bool = True,
        enable_wisdom_dispatch: bool = True,
        enable_autonomous_evolution: bool = True,
        enable_local_llm: bool = False,
        enable_imperial_library: bool = False,
        llm_model_path: str = "models/llm/7b",
        llm_device: str = "cpu",
        dispatch_prewarm_engines: bool = False,
        evolution_auto_optimize: bool = True,
        evolution_interval_minutes: int = 60,
        evolution_risk_threshold: str = "medium",
        library_sync_enabled: bool = False,
        library_sync_interval_minutes: int = 30,
    ):
        self.enable_neural_memory = enable_neural_memory
        self.enable_wisdom_dispatch = enable_wisdom_dispatch
        self.enable_autonomous_evolution = enable_autonomous_evolution
        self.enable_local_llm = enable_local_llm
        self.enable_imperial_library = enable_imperial_library
        self.llm_model_path = llm_model_path
        self.llm_device = llm_device
        self.dispatch_prewarm_engines = dispatch_prewarm_engines
        self.evolution_auto_optimize = evolution_auto_optimize
        self.evolution_interval_minutes = evolution_interval_minutes
        self.evolution_risk_threshold = evolution_risk_threshold
        self.library_sync_enabled = library_sync_enabled
        self.library_sync_interval_minutes = library_sync_interval_minutes

    def to_strategy_config(self) -> StrategyConfig:
        """转换为 v7.0 StrategyConfig"""
        return StrategyConfig(
            enable_wisdom_dispatch=self.enable_wisdom_dispatch,
            enable_llm_enhancement=self.enable_local_llm,
            enable_autonomous_evolution=self.enable_autonomous_evolution,
            evolution_interval_minutes=self.evolution_interval_minutes,
            evolution_auto_optimize=self.evolution_auto_optimize,
            evolution_risk_threshold=self.evolution_risk_threshold,
        )


class DigitalBrainCore(DigitalStrategy):
    """
    兼容 DigitalBrainCore（旧类名）

    v7.0: DigitalBrainCore 现在是 DigitalStrategy 的子类，
    所有实际逻辑在 DigitalStrategy / NeuralExecutor 中。
    旧代码 from digital_brain import DigitalBrainCore 继续有效。
    """
    def __init__(self, config: Optional[Any] = None, executor: Optional[Any] = None):
        if config and isinstance(config, BrainConfig):
            strategy_config = config.to_strategy_config()
        else:
            strategy_config = config
        super().__init__(strategy_config, executor)
        self._brain_config = config

    async def think(self, query: str, context: Optional[Dict] = None):
        """兼容旧接口（返回 BrainThought 而非 StrategyThought）"""
        result = await super().think(query, context)
        # 如果返回的是 StrategyThought，它已经兼容 BrainThought 的字段
        return result


# ════════════════════════════════════════════════════════════════
#  全局单例兼容函数
# ════════════════════════════════════════════════════════════════

_digital_brain_instance: Optional[DigitalBrainCore] = None


def get_digital_brain(config: Optional[Any] = None) -> DigitalBrainCore:
    """兼容 get_digital_brain()"""
    global _digital_brain_instance
    if _digital_brain_instance is None:
        _digital_brain_instance = DigitalBrainCore(config)
    return _digital_brain_instance


async def shutdown_digital_brain():
    """兼容 shutdown_digital_brain()"""
    global _digital_brain_instance
    if _digital_brain_instance:
        await _digital_brain_instance.shutdown()
        _digital_brain_instance = None
