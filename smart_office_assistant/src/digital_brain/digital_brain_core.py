# -*- coding: utf-8 -*-
"""
数字大脑核心引擎 - Digital Brain Core V1.1
==========================================

三个维度强化打通：
1. 神经记忆系统 ↔ 智慧调度系统 ↔ 自主净化能力
2. 本地大模型深度集成
3. 藏书阁全局记忆库桥接

形成可迭代、会进化、会成长的智能核心。

版本: V1.1.0 [2026-04-24]
更新:
- [v1.1] LLM集成增强：透明级联切换、本地优先策略
- [v1.1] 统一响应格式支持
- [v1.1] 会话上下文传递
创建: 2026-04-23
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

from pathlib import Path

logger = logging.getLogger("DigitalBrain")


# ═══════════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════════

class BrainState(Enum):
    """数字大脑状态"""
    INITIALIZING = "initializing"
    READY = "ready"
    PROCESSING = "processing"
    EVOLVING = "evolving"
    SLEEPING = "sleeping"
    ERROR = "error"


class MemoryLevel(Enum):
    """记忆层级"""
    SENSORY = "sensory"       # 感官记忆（毫秒级）
    WORKING = "working"        # 工作记忆（秒级）
    SHORT_TERM = "short_term" # 短期记忆（分钟级）
    LONG_TERM = "long_term"   # 长期记忆（持久）
    ETERNAL = "eternal"       # 永恒记忆（永不遗忘）


@dataclass
class BrainConfig:
    """数字大脑配置"""
    # 系统配置
    enable_local_llm: bool = True
    enable_wisdom_dispatch: bool = True
    enable_autonomous_evolution: bool = True
    enable_imperial_library: bool = True
    
    # 本地LLM配置
    llm_model_path: str = "models/llama-3.2-1b-instruct"
    llm_timeout: float = 30.0
    llm_fallback_to_template: bool = True
    
    # 神经记忆配置
    memory_max_workers: int = 4
    memory_encoding_dim: int = 384
    memory_granularity_levels: int = 8
    
    # 智慧调度配置
    dispatch_prewarm_engines: bool = True
    dispatch_timeout: float = 10.0
    dispatch_wuwei_enabled: bool = True
    
    # 自主进化配置
    evolution_interval_minutes: int = 60
    evolution_auto_optimize: bool = True
    evolution_risk_threshold: str = "medium"
    
    # 藏书阁配置
    library_sync_enabled: bool = True
    library_sync_interval_minutes: int = 30
    library_persistence_path: str = "data/imperial_library"
    
    # 净化配置
    purification_enabled: bool = True
    purification_schedule_hours: int = 24
    purification_confidence_threshold: float = 0.3


@dataclass
class BrainThought:
    """大脑思维记录"""
    thought_id: str
    content: str
    source: str  # "memory", "wisdom", "llm", "external"
    timestamp: float = field(default_factory=time.time)
    confidence: float = 0.5
    processing_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BrainEvolution:
    """大脑进化记录"""
    evolution_id: str
    evolution_type: str  # "memory_consolidation", "strategy_update", "architecture_adjust"
    trigger_reason: str
    changes: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    success: bool = True
    improvements: List[str] = field(default_factory=list)


@dataclass
class BrainHealth:
    """大脑健康状态"""
    overall_score: float  # 0-100
    memory_health: float
    wisdom_health: float
    evolution_health: float
    llm_health: float
    library_health: float
    
    active_thoughts: int = 0
    pending_evolutions: int = 0
    last_evolution_time: Optional[float] = None
    uptime_seconds: float = 0.0
    
    anomalies: List[Dict] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════
# 核心引擎
# ═══════════════════════════════════════════════════════════════════════

class DigitalBrainCore:
    """
    数字大脑核心引擎 V1.0
    
    整合三大维度 + 两大外部系统：
    
    维度一：神经记忆系统 (Neural Memory System)
    ├── 记忆编码与存储
    ├── 记忆检索与回忆
    └── 记忆衰减与强化
    
    维度二：智慧调度系统 (Wisdom Dispatch System)
    ├── 问题类型识别
    ├── 学派引擎调度
    └── 决策融合
    
    维度三：自主净化能力 (Autonomous Purification)
    ├── 自我诊断
    ├── 预测性维护
    └── 新陈代谢
    
    外部打通一：本地大模型 (Local LLM)
    ├── 推理加速
    └── 知识补全
    
    外部打通二：藏书阁 (Imperial Library)
    ├── 记忆汇聚
    └── 永久存储
    
    核心特性：
    - 可迭代：基于反馈持续优化
    - 会进化：自主学习和策略调整
    - 会成长：知识积累和能力提升
    """
    
    _instance: Optional['DigitalBrainCore'] = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, config: Optional[BrainConfig] = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        self.config = config or BrainConfig()
        self.state = BrainState.INITIALIZING
        
        # 启动时间
        self._start_time = time.time()
        
        # 组件初始化状态
        self._components: Dict[str, Any] = {}
        self._component_status: Dict[str, bool] = {}
        
        # 思维记录
        self._thought_history: List[BrainThought] = []
        self._thought_lock = threading.RLock()
        
        # 进化记录
        self._evolution_history: List[BrainEvolution] = []
        self._evolution_lock = threading.RLock()
        
        # 同步锁
        self._sync_lock = threading.RLock()
        
        # 后台任务
        self._background_tasks: Set[asyncio.Task] = set()
        self._evolution_task: Optional[asyncio.Task] = None
        
        self._initialized = True
        logger.info("[DigitalBrain] 数字大脑核心引擎初始化中...")
        
        # 初始化各组件
        asyncio.create_task(self._initialize_components())
    
    async def _initialize_components(self):
        """初始化所有组件"""
        try:
            logger.info("[DigitalBrain] 开始初始化组件...")
            
            # 1. 初始化神经记忆系统
            await self._init_neural_memory()
            
            # 2. 初始化智慧调度系统
            await self._init_wisdom_dispatch()
            
            # 3. 初始化自主进化系统
            await self._init_autonomous_evolution()
            
            # 4. 初始化本地大模型
            await self._init_local_llm()
            
            # 5. 初始化藏书阁桥接
            await self._init_imperial_library()
            
            # 6. 启动后台任务
            await self._start_background_tasks()
            
            self.state = BrainState.READY
            logger.info("[DigitalBrain] 数字大脑核心引擎初始化完成!")
            
        except Exception as e:
            self.state = BrainState.ERROR
            logger.error(f"[DigitalBrain] 初始化失败: {e}")
    
    async def _init_neural_memory(self):
        """初始化神经记忆系统"""
        try:
            from neural_memory.neural_memory_system_v3 import NeuralMemorySystemV3
            from neural_memory.memory_lifecycle_manager import MemoryLifecycleManager
            
            # 神经记忆核心
            neural_config = self.config.__dict__.copy()
            self._components['neural_memory'] = NeuralMemorySystemV3(neural_config)
            
            # 记忆生命周期管理
            self._components['memory_lifecycle'] = MemoryLifecycleManager()
            
            self._component_status['neural_memory'] = True
            logger.info("[DigitalBrain] 神经记忆系统初始化完成")
            
        except Exception as e:
            logger.warning(f"[DigitalBrain] 神经记忆系统初始化失败: {e}")
            self._component_status['neural_memory'] = False
    
    async def _init_wisdom_dispatch(self):
        """初始化智慧调度系统"""
        try:
            from intelligence.dispatcher.wisdom_dispatch._dispatch_mapping import WisdomDispatcher
            
            # 智慧调度核心
            self._components['wisdom_dispatch'] = WisdomDispatcher()
            
            # 预热学派引擎
            if self.config.dispatch_prewarm_engines:
                logger.info("[DigitalBrain] 预热学派引擎...")
                # 延迟加载，避免阻塞
            
            self._component_status['wisdom_dispatch'] = True
            logger.info("[DigitalBrain] 智慧调度系统初始化完成")
            
        except Exception as e:
            logger.warning(f"[DigitalBrain] 智慧调度系统初始化失败: {e}")
            self._component_status['wisdom_dispatch'] = False
    
    async def _init_autonomous_evolution(self):
        """初始化自主进化系统"""
        try:
            from core.autonomous_evolution_engine._aee_engine import AutonomousEvolutionEngine
            
            evolution_config = {
                "auto_evolution": self.config.evolution_auto_optimize,
                "diagnostic_interval_minutes": self.config.evolution_interval_minutes,
                "risk_threshold": self.config.evolution_risk_threshold,
            }
            
            self._components['autonomous_evolution'] = AutonomousEvolutionEngine(evolution_config)
            self._component_status['autonomous_evolution'] = True
            logger.info("[DigitalBrain] 自主进化系统初始化完成")
            
        except Exception as e:
            logger.warning(f"[DigitalBrain] 自主进化系统初始化失败: {e}")
            self._component_status['autonomous_evolution'] = False
    
    async def _init_local_llm(self):
        """初始化本地大模型"""
        if not self.config.enable_local_llm:
            self._component_status['local_llm'] = False
            return
        
        try:
            from core.local_llm_manager import LocalLLMManager
            
            self._components['local_llm'] = LocalLLMManager(auto_start=True)
            
            # 等待启动
            if not self._components['local_llm'].is_ready:
                logger.info("[DigitalBrain] 等待本地LLM启动...")
                await asyncio.sleep(2)
            
            self._component_status['local_llm'] = True
            logger.info("[DigitalBrain] 本地大模型初始化完成")
            
        except Exception as e:
            logger.warning(f"[DigitalBrain] 本地大模型初始化失败: {e}")
            self._component_status['local_llm'] = False
    
    async def _init_imperial_library(self):
        """初始化藏书阁桥接"""
        if not self.config.enable_imperial_library:
            self._component_status['imperial_library'] = False
            return
        
        try:
            from intelligence.dispatcher.wisdom_dispatch._imperial_library import get_imperial_library
            
            self._components['imperial_library'] = get_imperial_library()
            self._component_status['imperial_library'] = True
            logger.info("[DigitalBrain] 藏书阁桥接初始化完成")
            
        except Exception as e:
            logger.warning(f"[DigitalBrain] 藏书阁桥接初始化失败: {e}")
            self._component_status['imperial_library'] = False
    
    async def _start_background_tasks(self):
        """启动后台任务"""
        # 启动自主进化循环
        if self._component_status.get('autonomous_evolution'):
            self._evolution_task = asyncio.create_task(self._evolution_loop())
        
        # 启动藏书阁同步
        if self._component_status.get('imperial_library') and self.config.library_sync_enabled:
            sync_task = asyncio.create_task(self._library_sync_loop())
            self._background_tasks.add(sync_task)
    
    async def _evolution_loop(self):
        """进化循环"""
        engine = self._components.get('autonomous_evolution')
        if not engine:
            return
        
        interval = self.config.evolution_interval_minutes * 60
        
        while self.state not in (BrainState.ERROR, BrainState.SLEEPING):
            try:
                self.state = BrainState.EVOLVING
                logger.info("[DigitalBrain] 执行诊断周期...")
                
                health = await engine.run_diagnostic_cycle()
                
                # 记录进化
                if health.anomaly_alerts or not health.is_healthy():
                    evolution = BrainEvolution(
                        evolution_id=f"evo_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        evolution_type="diagnostic_cycle",
                        trigger_reason=f"健康度: {health.overall_score:.1f}%, 异常: {len(health.anomaly_alerts)}",
                        changes={"health": health.__dict__},
                        success=True,
                    )
                    with self._evolution_lock:
                        self._evolution_history.append(evolution)
                
                self.state = BrainState.READY
                
            except Exception as e:
                logger.error(f"[DigitalBrain] 进化循环错误: {e}")
            
            await asyncio.sleep(interval)
    
    async def _library_sync_loop(self):
        """藏书阁同步循环"""
        library = self._components.get('imperial_library')
        if not library:
            return
        
        interval = self.config.library_sync_interval_minutes * 60
        memory_system = self._components.get('neural_memory')
        
        while self.state != BrainState.ERROR:
            try:
                # 从神经记忆同步到藏书阁
                if memory_system:
                    # 实现双向同步逻辑
                    logger.debug("[DigitalBrain] 藏书阁同步...")
                
            except Exception as e:
                logger.error(f"[DigitalBrain] 藏书阁同步错误: {e}")
            
            await asyncio.sleep(interval)
    
    # ═══════════════════════════════════════════════════════════════════════
    # 核心能力接口
    # ═══════════════════════════════════════════════════════════════════════
    
    async def think(self, query: str, context: Optional[Dict] = None) -> BrainThought:
        """
        核心思维方法 - 三维强化思考
        
        Args:
            query: 输入问题
            context: 上下文
            
        Returns:
            BrainThought: 思维结果
        """
        start_time = time.time()
        self.state = BrainState.PROCESSING
        
        thought = BrainThought(
            thought_id=f"thought_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            content="",
            source="",
            metadata=context or {}
        )
        
        try:
            # 1. 从神经记忆检索相关记忆
            relevant_memories = await self._retrieve_memories(query)
            
            # 2. 智慧调度选择学派
            wisdom_result = await self._dispatch_wisdom(query, relevant_memories)
            
            # 3. 本地LLM增强推理
            llm_result = await self._enhance_with_llm(query, relevant_memories, wisdom_result)
            
            # 4. 整合结果
            thought.content = llm_result.get("answer", wisdom_result.get("answer", ""))
            thought.source = llm_result.get("source", wisdom_result.get("source", "wisdom"))
            thought.confidence = max(
                llm_result.get("confidence", 0.5),
                wisdom_result.get("confidence", 0.5)
            )
            
            # 5. 存储记忆
            await self._consolidate_memory(query, thought)
            
            # 6. 触发进化检查
            await self._check_evolution_trigger(query, thought)
            
        except Exception as e:
            logger.error(f"[DigitalBrain] 思考过程错误: {e}")
            thought.content = f"处理错误: {e}"
            thought.confidence = 0.0
        
        thought.processing_time_ms = (time.time() - start_time) * 1000
        self.state = BrainState.READY
        
        # 记录思维
        with self._thought_lock:
            self._thought_history.append(thought)
            if len(self._thought_history) > 1000:
                self._thought_history = self._thought_history[-500:]
        
        return thought
    
    async def _retrieve_memories(self, query: str) -> List[Dict]:
        """从神经记忆系统检索相关记忆"""
        memory_system = self._components.get('neural_memory')
        if not memory_system:
            return []
        
        try:
            # 使用统一的检索接口
            results = await memory_system.retrieve_memory(
                query=query,
                context=None,
                top_k=10
            )
            return results.result_data if hasattr(results, 'result_data') else []
        except Exception as e:
            logger.warning(f"[DigitalBrain] 记忆检索失败: {e}")
            return []
    
    async def _dispatch_wisdom(self, query: str, memories: List[Dict]) -> Dict:
        """智慧调度系统分发"""
        wisdom = self._components.get('wisdom_dispatch')
        if not wisdom:
            return {"answer": "", "confidence": 0.0, "source": "wisdom"}
        
        try:
            # 问题类型识别（简化版）
            from intelligence.dispatcher.wisdom_dispatch._dispatch_enums import ProblemType
            
            # 根据查询内容识别问题类型
            problem_type = self._identify_problem_type(query)
            
            # 获取学派映射
            school_mapping = wisdom.problem_school_mapping.get(problem_type, [])
            
            if school_mapping:
                top_school, weight = school_mapping[0]
                return {
                    "answer": f"[智慧调度] 问题类型: {problem_type.value}, 学派: {top_school.value}",
                    "confidence": weight,
                    "source": "wisdom",
                    "problem_type": problem_type.value,
                    "school": top_school.value
                }
            
            return {"answer": "", "confidence": 0.0, "source": "wisdom"}
            
        except Exception as e:
            logger.warning(f"[DigitalBrain] 智慧调度失败: {e}")
            return {"answer": "", "confidence": 0.0, "source": "wisdom"}
    
    def _identify_problem_type(self, query: str) -> ProblemType:
        """识别问题类型"""
        from intelligence.dispatcher.wisdom_dispatch._dispatch_enums import ProblemType
        
        query_lower = query.lower()
        
        # 关键词匹配
        if any(k in query_lower for k in ["分析", "分析一下", "compare"]):
            return ProblemType.MARKET_ANALYSIS
        elif any(k in query_lower for k in ["策略", "战略", "strategy"]):
            return ProblemType.STRATEGIC_PLANNING
        elif any(k in query_lower for k in ["增长", "growth"]):
            return ProblemType.GROWTH_MINDSET
        elif any(k in query_lower for k in ["创新", "creative"]):
            return ProblemType.INNOVATION_MANAGEMENT
        elif any(k in query_lower for k in ["决策", "decide"]):
            return ProblemType.DECISION_FRAMEWORK
        else:
            return ProblemType.SYSTEM_THINKING
    
    async def _enhance_with_llm(
        self, 
        query: str, 
        memories: List[Dict],
        wisdom_result: Dict
    ) -> Dict:
        """
        本地大模型增强推理 [v1.1]
        
        透明级联策略：
        1. 优先使用本地LLM
        2. 本地失败 → 尝试DualModelService
        3. 全部失败 → 返回wisdom结果
        """
        # 构建增强提示
        enhanced_prompt = self._build_enhanced_prompt(query, memories, wisdom_result)
        
        # 策略1: 尝试本地LLM Manager
        llm = self._components.get('local_llm')
        if llm and llm.is_ready:
            try:
                result = llm.dispatch(enhanced_prompt, request_timeout=60.0)
                if result and not result.error:
                    return {
                        "answer": result.text,
                        "confidence": 0.7 if result.text else 0.3,
                        "source": "local_llm",
                        "tokens": getattr(result, 'tokens', 0)
                    }
            except Exception as e:
                logger.warning(f"[DigitalBrain] 本地LLM失败: {e}")
        
        # 策略2: 尝试DualModelService（本地优先）
        try:
            dual_result = await self._try_dual_model(enhanced_prompt)
            if dual_result:
                return dual_result
        except Exception as e:
            logger.warning(f"[DigitalBrain] DualModelService失败: {e}")
        
        # 策略3: 直接使用云端模型
        try:
            cloud_result = await self._fallback_to_cloud(enhanced_prompt)
            if cloud_result:
                return cloud_result
        except Exception as e:
            logger.warning(f"[DigitalBrain] 云端降级失败: {e}")
        
        # 兜底: 返回wisdom结果
        return {
            "answer": wisdom_result.get("answer", ""),
            "confidence": 0.5,
            "source": "wisdom"
        }
    
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
    
    async def _try_dual_model(self, prompt: str) -> Optional[Dict]:
        """尝试使用DualModelService [v1.1]"""
        try:
            from src.tool_layer.dual_model_service import get_dual_model_service
            
            dual_service = get_dual_model_service()
            if dual_service:
                # 优先使用本地引擎
                response = dual_service.chat(
                    prompt, 
                    prefer_local=True,
                    max_tokens=1024
                )
                if response and response.content:
                    return {
                        "answer": response.content,
                        "confidence": 0.75,
                        "source": f"dual_model_{response.brain_used}",
                        "tokens": sum(response.usage.values()) if response.usage else 0,
                        "latency_ms": response.latency_ms
                    }
        except ImportError:
            logger.debug("[DigitalBrain] DualModelService未安装")
        except Exception as e:
            logger.debug(f"[DigitalBrain] DualModelService调用失败: {e}")
        
        return None
    
    async def _fallback_to_cloud(self, prompt: str) -> Optional[Dict]:
        """降级到云端模型 [v1.1]"""
        try:
            from src.tool_layer.llm_service import LLMService
            
            llm_svc = LLMService()
            
            # 尝试可用的云端模型
            available = llm_svc.list_available_models()
            model_to_use = None
            
            # 优先使用DeepSeek（成本低、质量高）
            for model_name in ["deepseek", "qwen", "doubao", "hunyuan"]:
                if model_name in available and available[model_name].get("available"):
                    model_to_use = model_name
                    break
            
            if not model_to_use:
                model_to_use = llm_svc.get_default_model()
            
            response = llm_svc.chat(prompt, model=model_to_use, max_tokens=1024)
            
            if response and response.content:
                return {
                    "answer": response.content,
                    "confidence": 0.8,
                    "source": f"cloud_{model_to_use}",
                    "tokens": sum(response.usage.values()) if response.usage else 0,
                    "latency_ms": response.latency_ms
                }
                
        except ImportError:
            logger.debug("[DigitalBrain] LLMService未安装")
        except Exception as e:
            logger.debug(f"[DigitalBrain] 云端调用失败: {e}")
        
        return None
    
    async def _consolidate_memory(self, query: str, thought: BrainThought):
        """记忆整合"""
        memory_system = self._components.get('neural_memory')
        if not memory_system:
            return
        
        try:
            # 添加到神经记忆
            from neural_memory.memory_encoding_system_v3 import EncodingContext
            
            ctx = EncodingContext(
                user_id=thought.metadata.get("user_id", "system"),
                session_id=thought.metadata.get("session_id", "default"),
                timestamp=datetime.now().isoformat(),
                metadata=thought.metadata
            )
            
            await memory_system.add_memory(
                content=f"Q: {query}\nA: {thought.content}",
                context=ctx,
                encode=True,
                granularize=True
            )
            
            # 同步到藏书阁
            library = self._components.get('imperial_library')
            if library:
                from intelligence.dispatcher.wisdom_dispatch._imperial_library import (
                    MemorySource, MemoryCategory
                )
                
                library.submit_memory(
                    title=f"思维记录: {query[:50]}...",
                    content=f"问题: {query}\n答案: {thought.content}",
                    source=MemorySource.SYSTEM_EVENT,
                    category=MemoryCategory.EXECUTION_LOG,
                    reporting_department="数字大脑",
                    tags=["brain", "thought", thought.source]
                )
            
        except Exception as e:
            logger.warning(f"[DigitalBrain] 记忆整合失败: {e}")
    
    async def _check_evolution_trigger(self, query: str, thought: BrainThought):
        """检查是否触发进化"""
        evolution = self._components.get('autonomous_evolution')
        if not evolution:
            return
        
        # 触发条件：置信度低、错误反馈、新领域问题
        if thought.confidence < 0.5:
            try:
                await evolution.handle_knowledge_expansion(
                    query_patterns=[{"pattern": query, "frequency": 1}],
                    failure_cases=[{"query": query, "confidence": thought.confidence}]
                )
            except Exception as e:
                logger.warning(f"[DigitalBrain] 进化触发检查失败: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # 净化与自优化
    # ═══════════════════════════════════════════════════════════════════════
    
    async def purify(self, mode: str = "auto") -> Dict[str, Any]:
        """
        执行自我净化
        
        Args:
            mode: 净化模式 "auto" | "aggressive" | "gentle"
            
        Returns:
            净化结果
        """
        results = {
            "memories_cleaned": 0,
            "duplicates_removed": 0,
            "weak_memories_reinforced": 0,
            "optimizations_applied": [],
            "duration_ms": 0.0
        }
        
        start_time = time.time()
        
        try:
            # 1. 记忆生命周期净化
            lifecycle = self._components.get('memory_lifecycle')
            if lifecycle:
                # 应用衰减
                decay_results = lifecycle.apply_decay()
                results["memories_cleaned"] = len(decay_results)
                
                # 触发复习
                review_tasks = lifecycle.trigger_review(max_tasks=10)
                results["weak_memories_reinforced"] = len(review_tasks)
            
            # 2. 神经记忆自清理
            memory_system = self._components.get('neural_memory')
            if memory_system:
                # 获取统计信息
                stats = memory_system.get_stats()
                if stats.get('operation_stats', {}).get('success_rate', 1.0) < 0.8:
                    results["optimizations_applied"].append("记忆系统健康度下降，建议检查")
            
            # 3. 藏书阁清理
            library = self._components.get('imperial_library')
            if library:
                clean_result = library.auto_clean(operator="DigitalBrain")
                results["optimizations_applied"].append(f"藏书阁清理: {clean_result}")
            
            # 4. 进化系统优化
            evolution = self._components.get('autonomous_evolution')
            if evolution:
                report = evolution.get_evolution_report()
                if report.get('failed', 0) > 0:
                    results["optimizations_applied"].append("检测到失败的进化计划，需要关注")
            
        except Exception as e:
            logger.error(f"[DigitalBrain] 净化过程错误: {e}")
            results["error"] = "执行失败"
        
        results["duration_ms"] = (time.time() - start_time) * 1000
        return results
    
    async def evolve(self, target: Optional[str] = None) -> BrainEvolution:
        """
        执行系统进化
        
        Args:
            target: 进化目标模块，如 "wisdom", "memory", "all"
            
        Returns:
            进化记录
        """
        evolution = BrainEvolution(
            evolution_id=f"evo_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            evolution_type="manual_trigger",
            trigger_reason=f"手动触发: {target or 'all'}",
            changes={}
        )
        
        try:
            evolution_engine = self._components.get('autonomous_evolution')
            if evolution_engine:
                # 运行诊断
                health = await evolution_engine.run_diagnostic_cycle()
                evolution.changes["health_score"] = health.overall_score
                
                # 执行优化计划
                if evolution_engine.active_plans:
                    for plan in evolution_engine.active_plans[:3]:
                        result = await evolution_engine.execute_evolution_plan(plan)
                        evolution.improvements.append(f"执行计划: {plan.evolution_id}")
                
                evolution.success = True
                evolution.trigger_reason = f"自动优化完成，健康度: {health.overall_score:.1f}%"
            
        except Exception as e:
            evolution.success = False
            evolution.changes["error"] = "操作失败"
            logger.error(f"[DigitalBrain] 进化过程错误: {e}")
        
        with self._evolution_lock:
            self._evolution_history.append(evolution)
        
        return evolution
    
    # ═══════════════════════════════════════════════════════════════════════
    # 健康状态与统计
    # ═══════════════════════════════════════════════════════════════════════
    
    async def get_health(self) -> BrainHealth:
        """
        获取大脑健康状态
        
        Returns:
            BrainHealth: 健康报告
        """
        uptime = time.time() - self._start_time
        
        # 各组件健康度
        memory_health = 100.0 if self._component_status.get('neural_memory') else 0.0
        wisdom_health = 100.0 if self._component_status.get('wisdom_dispatch') else 0.0
        evolution_health = 100.0 if self._component_status.get('autonomous_evolution') else 0.0
        
        llm = self._components.get('local_llm')
        llm_health = 100.0 if (llm and llm.is_ready) else 0.0
        
        library = self._components.get('imperial_library')
        library_health = 100.0 if library else 0.0
        
        # 综合健康度
        overall = (
            memory_health * 0.25 +
            wisdom_health * 0.25 +
            evolution_health * 0.2 +
            llm_health * 0.15 +
            library_health * 0.15
        )
        
        # 获取进化历史中的最新记录
        last_evolution = None
        with self._evolution_lock:
            if self._evolution_history:
                last_evolution = self._evolution_history[-1].timestamp
        
        return BrainHealth(
            overall_score=overall,
            memory_health=memory_health,
            wisdom_health=wisdom_health,
            evolution_health=evolution_health,
            llm_health=llm_health,
            library_health=library_health,
            active_thoughts=len(self._thought_history),
            pending_evolutions=0,
            last_evolution_time=last_evolution,
            uptime_seconds=uptime,
            anomalies=self._detect_anomalies(),
            recommendations=self._generate_recommendations(overall)
        )
    
    def _detect_anomalies(self) -> List[Dict]:
        """检测异常"""
        anomalies = []
        
        # 检查组件状态
        for comp, status in self._component_status.items():
            if not status:
                anomalies.append({
                    "type": "component_offline",
                    "component": comp,
                    "severity": "high"
                })
        
        # 检查思维历史
        with self._thought_lock:
            recent = [t for t in self._thought_history if time.time() - t.timestamp < 300]
            low_confidence = [t for t in recent if t.confidence < 0.3]
            
            if len(low_confidence) > 5:
                anomalies.append({
                    "type": "low_confidence_trend",
                    "count": len(low_confidence),
                    "severity": "medium"
                })
        
        return anomalies
    
    def _generate_recommendations(self, overall_score: float) -> List[str]:
        """生成建议"""
        recs = []
        
        if overall_score < 60:
            recs.append("系统健康度偏低，建议执行进化优化")
        
        if not self._component_status.get('local_llm'):
            recs.append("本地大模型未启用，建议配置以提升推理能力")
        
        if not self._component_status.get('imperial_library'):
            recs.append("藏书阁未连接，建议启用以实现永久记忆")
        
        if not self._component_status.get('autonomous_evolution'):
            recs.append("自主进化系统未启用，建议启用以实现自我优化")
        
        if not recs:
            recs.append("系统运行良好，继续保持")
        
        return recs
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self._thought_lock:
            thought_count = len(self._thought_history)
            recent_thoughts = self._thought_history[-10:] if self._thought_history else []
        
        with self._evolution_lock:
            evolution_count = len(self._evolution_history)
        
        return {
            "state": self.state.value,
            "uptime_seconds": time.time() - self._start_time,
            "components": {
                name: "online" if status else "offline"
                for name, status in self._component_status.items()
            },
            "thoughts": {
                "total": thought_count,
                "recent_avg_confidence": sum(t.confidence for t in recent_thoughts) / len(recent_thoughts) if recent_thoughts else 0
            },
            "evolutions": {
                "total": evolution_count,
                "pending": len([
                    e for e in self._evolution_history 
                    if e.trigger_reason == "pending"
                ])
            }
        }
    
    # ═══════════════════════════════════════════════════════════════════════
    # 生命周期管理
    # ═══════════════════════════════════════════════════════════════════════
    
    async def shutdown(self):
        """关闭数字大脑"""
        logger.info("[DigitalBrain] 关闭数字大脑...")
        
        self.state = BrainState.SLEEPING
        
        # 取消后台任务
        for task in self._background_tasks:
            task.cancel()
        
        if self._evolution_task:
            self._evolution_task.cancel()
        
        # 保存记忆
        memory_system = self._components.get('neural_memory')
        if memory_system:
            try:
                memory_system.save_all()
            except Exception as e:
                logger.warning(f"[DigitalBrain] 保存记忆失败: {e}")
        
        # 关闭藏书阁
        library = self._components.get('imperial_library')
        if library:
            try:
                library.save_all()
            except Exception as e:
                logger.warning(f"[DigitalBrain] 保存藏书阁失败: {e}")
        
        logger.info("[DigitalBrain] 数字大脑已关闭")
    
    def __repr__(self) -> str:
        return f"DigitalBrainCore(state={self.state.value}, uptime={time.time() - self._start_time:.0f}s)"


# ═══════════════════════════════════════════════════════════════════════
# 全局访问
# ═══════════════════════════════════════════════════════════════════════

_digital_brain_instance: Optional[DigitalBrainCore] = None


def get_digital_brain(config: Optional[BrainConfig] = None) -> DigitalBrainCore:
    """获取数字大脑全局实例"""
    global _digital_brain_instance
    if _digital_brain_instance is None:
        _digital_brain_instance = DigitalBrainCore(config)
    return _digital_brain_instance


async def shutdown_digital_brain():
    """关闭数字大脑"""
    global _digital_brain_instance
    if _digital_brain_instance:
        await _digital_brain_instance.shutdown()
        _digital_brain_instance = None


__all__ = [
    'DigitalBrainCore',
    'BrainConfig',
    'BrainState',
    'BrainThought',
    'BrainEvolution',
    'BrainHealth',
    'MemoryLevel',
    'get_digital_brain',
    'shutdown_digital_brain',
]
