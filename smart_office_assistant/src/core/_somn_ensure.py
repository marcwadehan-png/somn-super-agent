"""
__all__ = [
    'background_warmup',
    'ensure_autonomous_agent',
    'ensure_cloud_learning',
    'ensure_dual_model',  # [v1.0.0] A/B双模型左右大脑调度
    'ensure_dual_track',  # [v1.1.0] 双轨系统(神政轨+神行轨)
    'ensure_divine_reason',  # [v1.1.0] DivineReason统一推理引擎
    'ensure_domain_nexus',  # [v1.1.0] DomainNexus知识库引擎
    'ensure_ecosystem',  # [v1.2.0] 生态引擎系统
    'ensure_eight_layer_pipeline',  # [v1.1.0] 天枢八层管道
    'ensure_neural_layout',  # [v1.3.0] 神经网络布局集成
    'ensure_emotion_research',  # [v1.0.0] 情绪研究体系
    'ensure_global_claw_scheduler',  # [v1.0.0] 全局Claw调度器
    'ensure_layers',
    'ensure_learning_coordinator',
    'ensure_llm',
    'ensure_main_chain',
    'ensure_openclaw',
    'ensure_research_phase_manager',  # [v1.0.0] 研究阶段管理系统
    'ensure_runtime',
    'ensure_sage_dispatch',  # [v1.1.0] SageDispatch贤者调度系统
    'ensure_semantic_memory',
    'ensure_wisdom_layers',
    'init_semantic_memory',
    'summarize_understanding',
]

SomnCore 初始化/懒加载方法委托 [v20.0 整合优化版 + v1.0.0 A/B双模型]

[v20.0 优化] 整合减少冗余：
- 统一的 _wait_for_warmup() 消除重复等待逻辑
- 消除重复的 _ensure_llm() 调用
- 优化 Group A/B 依赖链，减少串行等待

[v10.1 P1-3优化] 25学派引擎预热：
- Group B 增加 WisdomDispatcher.prewarm_all_engines()
- 5个worker并行加载25个引擎，每引擎独立5s超时
- 消除首次访问学派时的懒加载冷启动（200ms~2s/次×3=最多6s）
"""

import logging
import os
import time
import threading

logger = logging.getLogger(__name__)

# [v21.0 优化] 首调等待超时（秒）
_FIRST_CALL_TIMEOUT = 3.0

# [v21.0] 预热完成事件（用于Event.wait替代轮询）
_warmup_complete_event: threading.Event = None

def _get_warmup_event() -> threading.Event:
    """[v21.0] 获取或创建预热完成事件"""
    global _warmup_complete_event
    if _warmup_complete_event is None:
        _warmup_complete_event = threading.Event()
    return _warmup_complete_event

# [v20.0 优化] 统一的预热等待辅助函数
def _wait_for_warmup(self) -> bool:
    """
    [v21.0 优化] 统一的预热等待辅助函数

    改进：使用 threading.Event.wait(timeout) 替代 time.sleep 轮询
    减少CPU开销和上下文切换。
    """
    bg_thread = getattr(self, '_bg_warmup_thread', None)
    if bg_thread is None or not bg_thread.is_alive():
        return True  # 无后台预热或已结束，需要同步初始化

    # [v21.0] 使用Event.wait替代轮询
    warmup_event = _get_warmup_event()
    result = warmup_event.wait(timeout=_FIRST_CALL_TIMEOUT)

    if result:
        # Event被set，预热已完成
        return False
    else:
        # 超时
        logger.debug(f"[预热等待] 超时({_FIRST_CALL_TIMEOUT}s)，切换到同步初始化")
        return True


def background_warmup(self):
    """
    [v20.0 优化版] daemon 线程：分组并行预热所有组件
    
    [v20.0 优化] 改动：
    - Group A/B 内部依赖优化：减少不必要的串行等待
    - 统一使用 _wait_for_warmup 状态检查
    - Group A 只负责 LLM + 自治存储（运行时由首调触发）
    
    分为3组并行执行:
      Group A (基础): LLM + 自治存储（不阻塞运行时）
      Group B (智能): 神经层 → 智慧层 + 引擎预热
      Group C (扩展): 云端学习 (独立)
    """
    import traceback

    def _group_a_basic():
        """[v20.0 优化] Group A: 基础组件（LLM + 双模型 + 自治存储），运行时由首调触发"""
        try:
            self._ensure_llm()
            # [v1.0.0] A/B双模型左右大脑 - LLM就绪后立即初始化
            try:
                ensure_dual_model(self)
                logger.info("[预热-GroupA] A/B双模型左右大脑就绪")
            except Exception as de:
                logger.warning(f"[预热-GroupA] 双模型初始化失败（不影响主流程）: {de}")
            # 直接调用 delegate 函数，避免经 __getattr__ 双重注入 self
            try:
                from ._somn_delegation import delegate_ensure_autonomy_stores
                delegate_ensure_autonomy_stores(self)
            except Exception as ae:
                logger.warning(f"[预热-GroupA] 自治存储初始化失败（不影响主流程）: {ae}")
        except Exception as e:
            logger.error(f"[预热-GroupA] 基础组件失败: {e}")

    def _group_b_intelligence():
        """Group B: 智能层（神经层 + 智慧层 + 25学派引擎预热）"""
        try:
            self._ensure_layers()
            self._ensure_wisdom_layers()
            # [v10.1 P1-3] 预热25学派引擎，消除首次调用时的懒加载延迟
            try:
                from src.intelligence.dispatcher.wisdom_dispatch import WisdomDispatcher
                dispatcher = WisdomDispatcher()
                dispatcher.prewarm_all_engines(timeout=30.0)
                logger.info("[预热-GroupB] 25学派引擎预热完成")
            except Exception as e:
                logger.warning(f"[预热-GroupB] 学派引擎预热失败（不影响主流程）: {e}")

            # [v10.2 Phase3] 预热776个Claw YAML配置，构建内存索引
            try:
                import threading
                def _prewarm_yaml():
                    try:
                        from src.intelligence.claws._claw_architect import _yaml_cache
                        result = _yaml_cache.preload_all(max_workers=4, timeout_per_file=2.0)
                        logger.info(f"[预热-GroupB] Claw YAML索引预热: {result['loaded']}/{result['total']} 加载")
                    except Exception as exc:
                        logger.warning(f"[预热-GroupB] Claw YAML预热失败: {exc}")
                t = threading.Thread(target=_prewarm_yaml, name="warmup-yaml", daemon=True)
                t.start()
            except Exception as e:
                logger.warning(f"[预热-GroupB] Claw YAML预热初始化失败: {e}")

            # [v1.0.1] 初始化 OpenClaw 开放抓取 + ClawSystemBridge
            try:
                ensure_openclaw(self)
                logger.info("[预热-GroupB] OpenClaw + ClawBridge 初始化完成")
            except Exception as e:
                logger.warning(f"[预热-GroupB] OpenClaw初始化失败（不影响主流程）: {e}")

            # [v1.0.0] 初始化情绪研究体系核心
            try:
                ensure_emotion_research(self)
                logger.info("[预热-GroupB] 情绪研究体系核心初始化完成")
            except Exception as e:
                logger.warning(f"[预热-GroupB] 情绪研究体系初始化失败（不影响主流程）: {e}")

            # [v1.1.0] SageDispatch 贤者调度系统（12调度器）
            try:
                _init_sage_dispatch(self)
                logger.info("[预热-GroupB] SageDispatch 贤者调度系统就绪")
            except Exception as e:
                logger.warning(f"[预热-GroupB] SageDispatch初始化失败: {e}")

            # [v1.1.0] DivineReason 统一推理引擎
            try:
                _init_divine_reason(self)
                logger.info("[预热-GroupB] DivineReason 统一推理引擎就绪")
            except Exception as e:
                logger.warning(f"[预热-GroupB] DivineReason初始化失败: {e}")

            # [v1.1.0] 天枢八层管道
            try:
                _init_eight_layer_pipeline(self)
                logger.info("[预热-GroupB] 天枢八层管道就绪")
            except Exception as e:
                logger.warning(f"[预热-GroupB] 八层管道初始化失败: {e}")

            # [v1.1.0] 双轨系统（神政轨+神行轨）
            try:
                _init_dual_track(self)
                logger.info("[预热-GroupB] 双轨系统TrackBridge就绪")
            except Exception as e:
                logger.warning(f"[预热-GroupB] 双轨系统初始化失败: {e}")

            # [v1.1.0] DomainNexus 知识库引擎
            try:
                _init_domain_nexus(self)
                logger.info("[预热-GroupB] DomainNexus 知识库引擎就绪")
            except Exception as e:
                logger.warning(f"[预热-GroupB] DomainNexus初始化失败: {e}")

            # [v1.3.0] 神经网络布局集成（6桥接绑定真实模块）
            try:
                _init_neural_layout(self)
                logger.info("[预热-GroupB] NeuralLayout 神经网络布局集成就绪")
            except Exception as e:
                logger.warning(f"[预热-GroupB] NeuralLayout初始化失败: {e}")
        except Exception as e:
            logger.error(f"[预热-GroupB] 智能层失败: {e}")

    def _group_c_extension():
        """Group C: 扩展组件（云端学习等，可延迟加载）"""
        try:
            self._ensure_cloud_learning()
        except Exception as e:
            logger.error(f"[预热-GroupC] 扩展组件失败: {e}")

    def _group_d_local_llm():
        """Group D: 本地LLM引擎 (A大模型 + B大模型) - 自动启动"""
        # 如果设置了跳过本地模型（无本地模型环境），直接跳过 Group D
        if os.getenv("SOMN_SKIP_LOCAL_MODEL", "").strip() in ("1", "true", "yes"):
            logger.info("[预热-GroupD] 跳过本地模型初始化 (SOMN_SKIP_LOCAL_MODEL=1)")
            return

        # A大模型 (Ollama/GGUF)
        try:
            from src.core.local_llm_manager import get_manager
            manager = get_manager(auto_start=True)
            logger.info(f"[预热-GroupD] A大模型管理器就绪: {manager.state.value}")
        except Exception as e:
            logger.warning(f"[预热-GroupD] A大模型初始化失败（不影响主流程）: {e}")

        # B大模型 (Gemma4 safetensors) - 后台异步加载，不阻塞
        def _start_model_b():
            try:
                from src.core.local_llm_engine import get_engine_b
                engine_b = get_engine_b()
                success = engine_b.start(timeout=300)
                if success:
                    logger.info(f"[预热-GroupD] B大模型就绪: mode={engine_b.load_mode}")
                else:
                    logger.warning(f"[预热-GroupD] B大模型启动失败: state={engine_b.state.value}")
            except Exception as ex:
                logger.warning(f"[预热-GroupD] B大模型初始化失败（不影响主流程）: {ex}")

        t_b = threading.Thread(target=_start_model_b, name="warmup-model-b", daemon=True)
        t_b.start()

    try:
        logger.info("  ⏳ [后台预热 v20.0 并行] 开始...")

        # 启动4个组并行执行
        threads = [
            threading.Thread(target=_group_a_basic, name="warmup-basic", daemon=True),
            threading.Thread(target=_group_b_intelligence, name="warmup-intel", daemon=True),
            threading.Thread(target=_group_c_extension, name="warmup-ext", daemon=True),
            threading.Thread(target=_group_d_local_llm, name="warmup-local-llm", daemon=True),
        ]
        for t in threads:
            t.start()

        # 等待所有组完成（每个组有独立的超时保护）
        _GROUP_TIMEOUT = 45.0  # 整体预热超时
        _start = time.time()
        for t in threads:
            remaining = max(1.0, _GROUP_TIMEOUT - (time.time() - _start))
            t.join(timeout=remaining)
            if t.is_alive():
                logger.warning(f"[预热] 线程 {t.name} 在{remaining:.0f}s内未完成，允许继续后台运行")

        logger.info("  ✅ [后台预热 v20.0] 全部组件就绪")
        # [v22.1 修复] 预热完成后通知等待者
        _get_warmup_event().set()
    except Exception as e:
        logger.error(f"[后台预热] 失败: {e}\n{traceback.format_exc()}")
        # 即使失败也要通知，避免等待者永远阻塞
        _get_warmup_event().set()

def ensure_llm(self):
    """
    确保 LLM 服务已初始化 [v20.0 优化]
    
    优化：使用统一的 _wait_for_warmup() 检查，减少重复代码
    """
    if self._llm_initialized:
        return

    # [v20.0 优化] 使用统一等待函数
    if not _wait_for_warmup(self):
        if self._llm_initialized:
            return

    with self._init_lock:
        if self._llm_initialized:
            return
        try:
            from src.tool_layer.llm_service import LLMService
            self.llm_service = LLMService(str(self.base_path / "data/llm"))
            self._llm_initialized = True
        except Exception as e:
            logger.error(f"LLM 服务加载失败: {e}")
            # [v22.1 修复] 不再标记为True，允许后续重试


def ensure_dual_model(self):
    """
    [v1.0.0 新增] 确保 A/B 双模型左右大脑调度服务已初始化

    DualModelService 是全局模式下 A/B 模型平行调用的核心：
    - A模型（左脑/主脑）优先调用
    - A模型响应速度不够时自动切换B模型（右脑/副脑）
    - 在全局任何需求指令下，大模型都会被自动激活
    - A/B模型作为系统的左右大脑来完成任务
    """
    if getattr(self, '_dual_model_initialized', False):
        return

    # 等待后台预热
    if not _wait_for_warmup(self):
        if getattr(self, '_dual_model_initialized', False):
            return

    with self._init_lock:
        if getattr(self, '_dual_model_initialized', False):
            return
        try:
            # 确保 LLM 服务先就绪
            if not getattr(self, '_llm_initialized', False):
                from src.tool_layer.llm_service import LLMService
                self.llm_service = LLMService(str(self.base_path / "data/llm"))
                self._llm_initialized = True

            from src.tool_layer.dual_model_service import DualModelService, DualModelConfig
            config = DualModelConfig(
                primary_model=os.getenv("SOMN_DUAL_PRIMARY_MODEL", os.getenv("SOMN_DEFAULT_MODEL", "local-default")),
                fallback_model=os.getenv("SOMN_DUAL_FALLBACK_MODEL", "deepseek" if os.getenv("SOMN_DEFAULT_MODEL") == "minimax" else "minimax"),
            )
            self.dual_model_service = DualModelService(self.llm_service, config)
            self._dual_model_initialized = True
            logger.info(
                f"[DualModel] A/B左右大脑就绪: "
                f"左脑(A)={config.primary_model}, 右脑(B)={config.fallback_model}"
            )
        except Exception as e:
            logger.error(f"A/B双模型服务初始化失败: {e}")
            # [v22.1 修复] 不再标记为True，允许后续重试

def ensure_runtime(self):
    """
    确保运行时基础组件已初始化（含 LLM）[v20.0 优化]
    
    [v20.0 优化]：
    - 使用统一的 _wait_for_warmup() 检查
    - 不再主动调用 _ensure_llm()，因为后续代码会使用 llm_service 时自动触发
    """
    if self._runtime_initialized:
        return

    # [v20.0 优化] 使用统一等待函数
    if not _wait_for_warmup(self):
        if self._runtime_initialized:
            return

    with self._init_lock:
        if self._runtime_initialized:
            return
        try:
            logger.info("  📦 [Tier2] 运行时基础组件...")
            from src.tool_layer.tool_registry import ToolRegistry
            from src.data_layer.web_search import WebSearchEngine
            from src.data_layer.data_collector import DataCollector

            # [v20.0 优化] llm_service 可能已在后台预热中初始化
            if not getattr(self, '_llm_initialized', False):
                from src.tool_layer.llm_service import LLMService
                self.llm_service = LLMService(str(self.base_path / "data/llm"))
                self._llm_initialized = True

            self.tool_registry = ToolRegistry(str(self.base_path / "data/tools"))
            if hasattr(self, 'llm_service') and self.llm_service:
                self.tool_registry.attach_llm_service(self.llm_service)
            self.web_search = WebSearchEngine(str(self.base_path / "data/search_cache"))
            self.data_collector = DataCollector(str(self.base_path / "data/collected"))
            logger.info("    ✅ tool_registry + web_search + data_collector 就绪")
        except Exception as e:
            logger.error(f"运行时基础组件加载失败: {e}")
        finally:
            self._runtime_initialized = True

def ensure_layers(self):
    """
    确保智能层(神经/知识图谱/语义记忆)已初始化 [v20.0 优化]
    
    优化：使用统一的 _wait_for_warmup() 检查
    """
    if self._layers_initialized:
        return

    # [v20.0 优化] 使用统一等待函数
    if not _wait_for_warmup(self):
        if self._layers_initialized:
            return

    with self._layers_lock:
        if self._layers_initialized:
            return
        try:
            logger.info("  📦 [Tier2] 初始化神经/知识/语义记忆层...")
            from src.neural_memory.neural_system import create_neural_system
            from src.knowledge_graph import create_knowledge_graph, IndustryKnowledgeBase, RuleEngine

            self.neural_system = create_neural_system(str(self.base_path / "data/learning"))
            self.knowledge_graph = create_knowledge_graph(str(self.base_path / "data/knowledge_graph"))
            self.industry_kb = IndustryKnowledgeBase(self.knowledge_graph)
            self.rule_engine = RuleEngine(self.knowledge_graph)
            self.neural_system.knowledge = self.knowledge_graph

            try:
                from src.neural_memory.semantic_memory_engine import SemanticMemoryEngine, SomnSemanticIntegration
                self.semantic_memory = SemanticMemoryEngine()
                self.semantic_integration = SomnSemanticIntegration(self.semantic_memory)
                logger.info("    ✅ SemanticMemoryEngine 加载成功")
            except Exception as e:
                logger.warning(f"    ⚠️ SemanticMemoryEngine 加载失败: {e}")
                self.semantic_memory = None

            self._layers_initialized = True
            logger.info("神经/知识/语义记忆层 Tier2 加载完成")
        except Exception as e:
            logger.error(f"神经/知识/语义记忆层 Tier2 加载失败: {e}")
            # [v22.1 修复] 不再标记为True，允许后续重试

def ensure_wisdom_layers(self):
    """
    确保智慧/逻辑协调层已初始化 [v20.0 优化]
    
    [v20.0 优化]：
    - 使用统一的 _wait_for_warmup() 检查
    - 增加首调等待时间（5s→更激进）
    """
    if self._wisdom_layers_initialized:
        return

    # [v22.0 修复] 统一使用Event.wait替代轮询（消除最后一个sleep(0.05)残留）
    if not _wait_for_warmup(self):
        if self._wisdom_layers_initialized:
            return

    with self._wisdom_layers_lock:
        if self._wisdom_layers_initialized:
            return
        try:
            logger.info("  📦 [懒加载] 初始化智慧/逻辑协调层...")
            try:
                from src.intelligence.engines.super_wisdom_coordinator import SuperWisdomCoordinator
                self.super_wisdom = SuperWisdomCoordinator()
                logger.info("    ✅ SuperWisdomCoordinator 加载成功")
            except Exception as e:
                logger.warning(f"    ⚠️ SuperWisdomCoordinator 加载失败: {e}")
            try:
                from src.intelligence.engines.unified_intelligence_coordinator import UnifiedIntelligenceCoordinator
                self.unified_coordinator = UnifiedIntelligenceCoordinator()
                logger.info("    ✅ UnifiedIntelligenceCoordinator 加载成功")
            except Exception as e:
                logger.warning(f"    ⚠️ UnifiedIntelligenceCoordinator 加载失败: {e}")
            try:
                from src.intelligence.scheduler.global_wisdom_scheduler import get_scheduler
                self.global_wisdom = get_scheduler()
                logger.info("    ✅ GlobalWisdomScheduler 加载成功")
            except Exception as e:
                logger.warning(f"    ⚠️ GlobalWisdomScheduler 加载失败: {e}")
            try:
                from src.intelligence.scheduler.thinking_method_engine import ThinkingMethodFusionEngine
                self.thinking_engine = ThinkingMethodFusionEngine()
                logger.info("    ✅ ThinkingMethodFusionEngine 加载成功")
            except Exception as e:
                logger.warning(f"    ⚠️ ThinkingMethodEngine 加载失败: {e}")
            try:
                from src.intelligence.engines.persona_core import SomnPersona
                self.persona = SomnPersona()
                logger.info("    ✅ SomnPersona 深度人设系统加载成功")
            except Exception as e:
                logger.warning(f"    ⚠️ SomnPersona 加载失败: {e}")
            self._wisdom_layers_initialized = True
            logger.info("  📦 智慧/逻辑协调层懒加载完成")
        except Exception as e:
            logger.error(f"智慧层懒加载失败: {e}")
            # [v22.1 修复] 不再标记为True，允许后续重试

def ensure_semantic_memory(self):
    """确保语义记忆引擎已初始化 -- 合并到 _ensure_layers 统一管理"""
    if self._layers_initialized:
        return
    self._ensure_layers()

def ensure_cloud_learning(self):
    """确保云端学习系统已初始化 [v20.0 优化]"""
    if self._cloud_learning_initialized:
        return
    with self._init_lock:
        if self._cloud_learning_initialized:
            return
        try:
            self._init_cloud_learning_system()
        except Exception as e:
            logger.error(f"云端学习系统 Tier2 加载失败: {e}")
        finally:
            self._cloud_learning_initialized = True

def ensure_learning_coordinator(self):
    """确保学习协调器已初始化 [v20.0 优化]"""
    if self._learning_coordinator_initialized:
        return
    with self._init_lock:
        if self._learning_coordinator_initialized:
            return
        try:
            self._init_learning_coordinator()
        finally:
            self._learning_coordinator_initialized = True

def ensure_autonomous_agent(self):
    """确保自主智能体已初始化 [v20.0 优化]"""
    if self._autonomous_agent_initialized:
        return
    with self._init_lock:
        if self._autonomous_agent_initialized:
            return
        try:
            self._init_autonomous_agent()
        finally:
            self._autonomous_agent_initialized = True

def ensure_main_chain(self):
    """确保主线集成器已初始化 [v20.0 优化]"""
    if self._main_chain_initialized:
        return
    with self._init_lock:
        if self._main_chain_initialized:
            return
        try:
            self._init_main_chain_integration()
        finally:
            self._main_chain_initialized = True

def init_semantic_memory(self):
    """init语义记忆引擎"""
    self.semantic_memory = None
    try:
        from src.neural_memory.semantic_memory_engine import SemanticMemoryEngine, SomnSemanticIntegration
        self.semantic_memory = SemanticMemoryEngine()
        self.semantic_integration = SomnSemanticIntegration(self.semantic_memory)
        logger.info("    ✅ SemanticMemoryEngine 加载成功(关键词-语义mapping+自主理解)")
    except Exception as e:
        logger.warning(f"    ⚠️ SemanticMemoryEngine 加载失败: {e}")

def summarize_understanding(self, semantic_context) -> str:
    """生成语义理解摘要（兼容语义上下文对象）."""
    inferred = getattr(semantic_context, "inferred_intent", "unknown")
    keywords = getattr(semantic_context, "keywords_extracted", []) or []
    mappings = getattr(semantic_context, "matched_mappings", []) or []
    parts = []
    if inferred != "unknown":
        parts.append(f"用户想[{inferred}]")
    if keywords:
        parts.append(f"关键词:{','.join(keywords[:5])}")
    if mappings:
        parts.append(f"已匹配语义mapping:{len(mappings)} 条")
    return ";".join(parts) if parts else "未recognize到明确意图"


def _init_openclaw(self):
    """
    [v1.0.1 新增] 初始化 OpenClaw 核心引擎 + ClawSystemBridge

    OpenClaw 是 Phase 4 的开放抓取子系统，负责：
    1. 从外部数据源（Web/文件）主动抓取知识
    2. 将知识注入到 Claw 子智能体的记忆中
    3. 从用户反馈中学习并优化贤者参数

    集成方式：
    - OpenClawCore: 独立引擎，管理数据源和知识更新
    - ClawSystemBridge: 桥接层，将 OpenClaw 与 Claw 子系统连接
    """
    try:
        from src.intelligence.claws._claw_bridge import (
            ClawSystemBridge, IntegrationConfig, IntegrationLevel
        )
        # 以 FULL 级别集成，启用 OpenClaw
        config = IntegrationConfig(
            level=IntegrationLevel.FULL,
            enable_openclaw=True,
            default_fallback_claw="孔子",
        )
        bridge = ClawSystemBridge(config)
        # 初始化桥接器（内部会初始化 ClawSystem 和 OpenClaw）
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 在已有事件循环中，创建新线程运行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, bridge.initialize())
                    init_result = future.result(timeout=30)
            else:
                init_result = asyncio.run(bridge.initialize())
        except RuntimeError:
            # 没有事件循环，直接 run
            init_result = asyncio.run(bridge.initialize())

        self.claw_bridge = bridge
        self.openclaw_core = bridge._openclaw_core
        self._openclaw_initialized = True

        loaded_claws = init_result.get("loaded_claws", 0)
        logger.info(f"[OpenClaw] 初始化完成: {loaded_claws} 个Claw已加载, bridge_level={init_result.get('bridge_level', 'unknown')}")
    except Exception as e:
        logger.warning(f"[OpenClaw] 初始化异常: {e}")
        # [v22.1 修复] 不再标记为True，允许后续重试


def ensure_openclaw(self):
    """
    [v1.0.1 新增] 确保 OpenClaw 开放抓取已初始化

    如果后台预热已完成则直接返回；
    如果后台预热仍在运行则等待；
    如果后台预热未覆盖则同步初始化。
    """
    if self._openclaw_initialized:
        return

    # 等待后台预热
    if not _wait_for_warmup(self):
        if self._openclaw_initialized:
            return

    with self._init_lock:
        if self._openclaw_initialized:
            return
        try:
            _init_openclaw(self)
        except Exception as e:
            logger.error(f"OpenClaw 初始化失败: {e}")
        finally:
            self._openclaw_initialized = True


def _init_emotion_research(self):
    """
    [v1.0.0 新增] 初始化情绪研究体系核心
    """
    try:
        from ._somn_emotion_research import integrate_with_somn_core
        integrate_with_somn_core(self)
    except Exception as e:
        logger.error(f"情绪研究体系整合失败: {e}")


def ensure_emotion_research(self):
    """
    [v1.0.0 新增] 确保情绪研究体系已初始化

    作为项目核心能力、底层生产框架、自主学习升级中枢
    """
    if getattr(self, '_emotion_research_initialized', False):
        return

    # 等待后台预热
    if not _wait_for_warmup(self):
        if getattr(self, '_emotion_research_initialized', False):
            return

    with self._init_lock:
        if getattr(self, '_emotion_research_initialized', False):
            return
        try:
            _init_emotion_research(self)
            self._emotion_research_initialized = True
            logger.info("✅ 情绪研究体系核心已就绪")
        except Exception as e:
            logger.error(f"情绪研究体系初始化失败: {e}")
            # [v22.1 修复] 不再标记为True，允许后续重试


def ensure_research_phase_manager(self):
    """
    [v1.0.0 新增] 确保研究阶段管理系统已初始化

    四阶段研究管理: 基础研究→深度研究→应用研究→体系构建
    """
    if getattr(self, '_research_phase_manager_initialized', False):
        return

    # 等待情绪研究体系就绪(研究阶段管理依赖它)
    if not _wait_for_warmup(self):
        if getattr(self, '_research_phase_manager_initialized', False):
            return

    with self._init_lock:
        if getattr(self, '_research_phase_manager_initialized', False):
            return
        try:
            from .intelligence.engines.research_phase_manager import ResearchPhaseManager
            # 使用已有的 emotion_research_core
            self._research_phase_manager = ResearchPhaseManager(
                emotion_research_core=getattr(self, 'emotion_research_core', None),
                data_dir=str(self.base_path / "data" / "research_phases"),
            )
            self._research_phase_manager_initialized = True
            logger.info("✅ 研究阶段管理系统 v1.0.0 已就绪")
        except Exception as e:
            logger.error(f"研究阶段管理系统初始化失败: {e}")
            self._research_phase_manager_initialized = True


def _init_global_claw_scheduler(self):
    """
    [v1.0.0 新增] 初始化全局Claw调度器
    
    GlobalClawScheduler统一调度763个贤者Claw，提供：
    - 全局调动（ProblemType/Department/School/Name路由）
    - 分布式工作（任务队列+工作池+并发控制）
    - 独立工作（单Claw ReAct闭环）
    - 协作工作（多Claw角色分工+结果聚合）
    """
    try:
        from src.intelligence.claws._global_claw_scheduler import (
            GlobalClawScheduler,
        )
        scheduler = GlobalClawScheduler()
        
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, scheduler.initialize())
                    init_result = future.result(timeout=30)
            else:
                init_result = asyncio.run(scheduler.initialize())
        except RuntimeError:
            init_result = asyncio.run(scheduler.initialize())
        
        self._global_claw_scheduler = scheduler
        self._global_claw_scheduler_initialized = True
        
        logger.info(f"[GlobalClawScheduler] 全局Claw调度器初始化完成: {init_result}")
    except Exception as e:
        logger.warning(f"[GlobalClawScheduler] 初始化异常: {e}")
        self._global_claw_scheduler_initialized = True


def ensure_global_claw_scheduler(self):
    """
    [v1.0.0 新增] 确保全局Claw调度器已初始化
    """
    if getattr(self, '_global_claw_scheduler_initialized', False):
        return

    # 等待后台预热
    if not _wait_for_warmup(self):
        if getattr(self, '_global_claw_scheduler_initialized', False):
            return

    with self._init_lock:
        if getattr(self, '_global_claw_scheduler_initialized', False):
            return
        try:
            _init_global_claw_scheduler(self)
        except Exception as e:
            logger.error(f"全局Claw调度器初始化失败: {e}")
        finally:
            self._global_claw_scheduler_initialized = True


# ═══════════════════════════════════════════════════════════════════
# [v1.1.0] SageDispatch / DivineReason / 八层管道 / 双轨 / DomainNexus
# ═══════════════════════════════════════════════════════════════════

def _init_sage_dispatch(self):
    """
    [v1.1.0 新增] 初始化 SageDispatch 贤者调度系统

    SageDispatch = 12调度器 + 核心引擎
    入口: DispatchEngine.dispatch(problem, level, dispatcher_id)
    单例: get_engine() -> DispatchEngine
    """
    try:
        from knowledge_cells.core import get_engine as get_dispatch_engine
        engine = get_dispatch_engine()
        self._sage_dispatch_engine = engine
        self._sage_dispatch_initialized = True
        logger.info(f"[SageDispatch] 贤者调度系统就绪 (12调度器)")
    except Exception as e:
        logger.warning(f"[SageDispatch] 初始化失败（不影响主流程）: {e}")


def ensure_sage_dispatch(self):
    """[v1.1.0] 确保SageDispatch贤者调度系统已初始化"""
    if getattr(self, '_sage_dispatch_initialized', False):
        return

    if not _wait_for_warmup(self):
        if getattr(self, '_sage_dispatch_initialized', False):
            return

    with self._init_lock:
        if getattr(self, '_sage_dispatch_initialized', False):
            return
        try:
            _init_sage_dispatch(self)
        except Exception as e:
            logger.error(f"SageDispatch 初始化失败: {e}")


def _init_divine_reason(self):
    """
    [v1.1.0 新增] 初始化 DivineReason 统一推理引擎

    DivineReason = 4合1推理 (GoT + LongCoT + ToT + ReAct)
    入口: DivineReason.solve(problem, mode, context)
    模式: LINEAR / DIVINE / SUPER / BRANCHING / REACTIVE / GRAPH
    """
    try:
        from src.intelligence.reasoning._unified_reasoning_engine import DivineReason
        self._divine_reason = DivineReason()
        self._divine_reason_initialized = True
        logger.info(f"[DivineReason] 统一推理引擎就绪 (GoT+LongCoT+ToT+ReAct)")
    except Exception as e:
        logger.warning(f"[DivineReason] 初始化失败（不影响主流程）: {e}")


def ensure_divine_reason(self):
    """[v1.1.0] 确保DivineReason统一推理引擎已初始化"""
    if getattr(self, '_divine_reason_initialized', False):
        return

    if not _wait_for_warmup(self):
        if getattr(self, '_divine_reason_initialized', False):
            return

    with self._init_lock:
        if getattr(self, '_divine_reason_initialized', False):
            return
        try:
            _init_divine_reason(self)
        except Exception as e:
            logger.error(f"DivineReason 初始化失败: {e}")


def _init_eight_layer_pipeline(self):
    """
    [v1.1.0 新增] 初始化天枢八层管道 (TianShu)

    EightLayerPipeline = L1输入→L2 NLP→L3 分类→L4 分流→L5 推理→L6 论证→L7 输出→L8 优化
    入口: EightLayerPipeline.get_pipeline().process(input_text, grade)
    等级: BASIC(快速) / DEEP(智慧+Claw) / SUPER(全Claw+T2)
    """
    try:
        from knowledge_cells.eight_layer_pipeline import EightLayerPipeline
        pipeline = EightLayerPipeline.get_pipeline(output_dir="")
        self._eight_layer_pipeline = pipeline
        self._eight_layer_pipeline_initialized = True
        logger.info(f"[天枢] 八层管道就绪 (L1→L8)")
    except Exception as e:
        logger.warning(f"[天枢] 八层管道初始化失败（不影响主流程）: {e}")


def ensure_eight_layer_pipeline(self):
    """[v1.1.0] 确保天枢八层管道已初始化"""
    if getattr(self, '_eight_layer_pipeline_initialized', False):
        return

    if not _wait_for_warmup(self):
        if getattr(self, '_eight_layer_pipeline_initialized', False):
            return

    with self._init_lock:
        if getattr(self, '_eight_layer_pipeline_initialized', False):
            return
        try:
            _init_eight_layer_pipeline(self)
        except Exception as e:
            logger.error(f"八层管道初始化失败: {e}")


def _init_ecosystem(self):
    """
    [v1.2.0 新增] 初始化生态引擎系统

    Note: src/ecology/ 目录已移除，生态能力已整合至
    knowledge_cells/ecology_ml_bridge.py + neural_memory_v7.py
    此函数保留为占位，始终不执行任何操作。
    """
    logger.info("[生态引擎] src/ecology/ 已移除，跳过初始化")
    return


def ensure_ecosystem(self):
    """[v1.2.0] 确保生态引擎已初始化"""
    if getattr(self, '_ecosystem_initialized', False):
        return

    if not _wait_for_warmup(self):
        if getattr(self, '_ecosystem_initialized', False):
            return

    with self._init_lock:
        if getattr(self, '_ecosystem_initialized', False):
            return
        try:
            _init_ecosystem(self)
        except Exception as e:
            logger.error(f"生态引擎初始化失败: {e}")


def _init_dual_track(self):
    """
    [v1.1.0 新增] 初始化双轨系统 (神政轨 TrackA + 神行轨 TrackB)

    TrackBridge 连接双轨:
    - create_system() → 构建双轨系统 (初始化 TrackA + TrackB 并连接)
    - direct_department_call() → 跨轨部门调用
    - dispatch_to_claw() → Claw调度
    """
    try:
        from src.intelligence.dual_track.bridge import TrackBridge
        bridge = TrackBridge()
        # create_system() 会初始化 TrackA + TrackB 并连接，使 dispatch_to_claw 可用
        bridge.create_system()
        self._track_bridge = bridge
        self._dual_track_initialized = True
        logger.info(f"[双轨系统] TrackBridge就绪 (神政轨+神行轨已连接)")
    except Exception as e:
        logger.warning(f"[双轨系统] 初始化失败（不影响主流程）: {e}")


def ensure_dual_track(self):
    """[v1.1.0] 确保双轨系统已初始化"""
    if getattr(self, '_dual_track_initialized', False):
        return

    if not _wait_for_warmup(self):
        if getattr(self, '_dual_track_initialized', False):
            return

    with self._init_lock:
        if getattr(self, '_dual_track_initialized', False):
            return
        try:
            _init_dual_track(self)
        except Exception as e:
            logger.error(f"双轨系统初始化失败: {e}")


def _init_domain_nexus(self):
    """
    [v1.1.0 新增] 初始化 DomainNexus 知识库引擎

    DomainNexus = 31知识格子 + 双向标签匹配 + LRU懒加载
    入口: get_nexus() → DomainNexus单例
    """
    try:
        from knowledge_cells.domain_nexus import get_nexus
        nexus = get_nexus()
        self._domain_nexus = nexus
        self._domain_nexus_initialized = True
        logger.info(f"[DomainNexus] 知识库引擎就绪")
    except Exception as e:
        logger.warning(f"[DomainNexus] 初始化失败（不影响主流程）: {e}")


def ensure_domain_nexus(self):
    """[v1.1.0] 确保DomainNexus知识库引擎已初始化"""
    if getattr(self, '_domain_nexus_initialized', False):
        return

    if not _wait_for_warmup(self):
        if getattr(self, '_domain_nexus_initialized', False):
            return

    with self._init_lock:
        if getattr(self, '_domain_nexus_initialized', False):
            return
        try:
            _init_domain_nexus(self)
        except Exception as e:
            logger.error(f"DomainNexus 初始化失败: {e}")


def _init_neural_layout(self):
    """
    [v1.3.0 新增] 初始化神经网络布局集成

    将 SomnCore 绑定到 GlobalNeuralBridge 的 6 个桥接处理器：
    AgentCore / SomnCore / WisdomDispatcher / MemorySystem / LearningSystem / AutonomySystem
    入口: neural_layout.integration.initialize_neural_layout()
    """
    try:
        from src.neural_layout.integration import initialize_neural_layout
        integration = initialize_neural_layout(somn_core=self)
        self._neural_layout = integration
        self._neural_layout_initialized = True
        bridge_count = len(getattr(integration, '_bridge', {})._bridge_handlers) if hasattr(integration, '_bridge') and integration._bridge else 0
        logger.info(f"[NeuralLayout] 布局集成就绪, {bridge_count} 个桥接处理器已绑定")
    except Exception as e:
        logger.warning(f"[NeuralLayout] 初始化失败（不影响主流程）: {e}")


def ensure_neural_layout(self):
    """[v1.3.0] 确保神经网络布局已初始化"""
    if getattr(self, '_neural_layout_initialized', False):
        return

    if not _wait_for_warmup(self):
        if getattr(self, '_neural_layout_initialized', False):
            return

    with self._init_lock:
        if getattr(self, '_neural_layout_initialized', False):
            return
        try:
            _init_neural_layout(self)
        except Exception as e:
            logger.error(f"NeuralLayout 初始化失败: {e}")
