"""
SageDispatch - 贤者调度系统
后台调度引擎，不是描述文档

Usage:
    from knowledge_cells import dispatch, chain, smart_dispatch

    # 快捷调度
    result = dispatch("分析这个战略问题...")

    # 智能调度（自动选择最优级别）
    result = smart_dispatch("复杂问题")

    # 链式调度
    results = chain("问题", ["SD-F1", "SD-D3", "SD-C2"])

    # 神行轨调用
    from knowledge_cells import execute_with_track_b
    result = execute_with_track_b("SD-F1", "融合分析", "礼部")

加载架构 (v6.1.1 快速加载):
  L0 立即加载 (~5ms): core.py 枚举/数据类 + 版本信息
  L1 懒导入 (首次~50ms): dispatchers / track_b_adapter / pan_wisdom / pipeline
  L2 懒实例化 (首次~80ms): DomainNexus / RefuteCore
"""

# ==================== L0: 立即加载 — 仅核心枚举+数据类 ====================
from .core import (
    Level,
    DispatcherState,
    DispatchRequest,
    DispatchResponse,
    BaseDispatcher,
    LevelAssessor,
    DispatchEngine,
    get_engine,
    dispatch,
    chain,
    smart_dispatch,
)

# ==================== L1/L2: 延迟加载 — __getattr__ 拦截 ====================
# 以下 6 个重量级模块不再在 import 时加载，
# 而是在首次访问属性时才触发对应模块的 import。
# 效果: import knowledge_cells 从 ~100ms 降至 ~5ms

import sys
import importlib

# 模块映射: name -> (module_name, symbols_or_None)
# symbols_or_None 表示加载整个模块后自动查找
_LAZY_MODULES = {
    # dispatchers.py — 91KB, 11个调度器
    "FourLevelDispatchController": ".dispatchers",
    "ProblemDispatcher": ".dispatchers",
    "FallacyChecker": ".dispatchers",
    "SchoolFusion": ".dispatchers",
    "SuperReasoning": ".dispatchers",
    "YinYangDecision": ".dispatchers",
    "DivineArchitecture": ".dispatchers",
    "ChainExecutor": ".dispatchers",
    "ResultTracker": ".dispatchers",
    # RefuteCore — 驳心引擎桥接 (S1.0)
    "RefuteCore": ".refute_core",
    "RefuteDimension": ".refute_core",
    "ArgumentDimension": ".refute_core",
    "RefuteCoreEngine": ".refute_core",
    "RefuteCoreResult": ".refute_core",
    "Refutation": ".refute_core",
    "MultiDimensionRefutation": ".refute_core",
    "ArgumentParser": ".refute_core",
    "DebateArena": ".refute_core",
    "ArgumentRepair": ".refute_core",
    "get_refute_core": ".refute_core",
    "quick_refute": ".refute_core",
    "batch_refute": ".refute_core",
    # ContentEnricher — 在 domain_nexus.py 中
    "ContentEnricher": ".domain_nexus",
    "DivineReason": ".divine_reason",
    "UnifiedConfig": ".divine_reason",
    "ReasoningMode": ".divine_reason",
    "NodeType": ".divine_reason",
    "EdgeType": ".divine_reason",
    "ReasoningResult": ".divine_reason",
    "SuperGraph": ".divine_reason",
    "UnifiedEvaluator": ".divine_reason",
    "UnifiedGenerator": ".divine_reason",
    "UnifiedNode": ".divine_reason",
    "UnifiedEdge": ".divine_reason",
    "ReasoningMetadata": ".divine_reason",
    "GraphStatistics": ".divine_reason",
    "InsightType": ".divine_reason",
    "NodeStatus": ".divine_reason",
    "TaskComplexity": ".divine_reason",
    "ThoughtPath": ".divine_reason",
    "UnifiedReasoningEngine": ".divine_reason",
    # track_b_adapter.py — 13KB, 神行轨
    "TrackBExecutor": ".track_b_adapter",
    "get_track_b_executor": ".track_b_adapter",
    "execute_with_track_b": ".track_b_adapter",
    "wisdom_tree_call": ".track_b_adapter",
    "sd_f1_call": ".track_b_adapter",
    "sd_d_call": ".track_b_adapter",
    "sd_c1_call": ".track_b_adapter",
    "sd_c2_call": ".track_b_adapter",
    "sd_e1_call": ".track_b_adapter",
    "sd_l1_call": ".track_b_adapter",
    "sd_r2_call": ".track_b_adapter",
    # domain_nexus.py — 77KB, 知识库 (L2 重量级)
    "DomainNexus": ".domain_nexus",
    "DomainCellManager": ".domain_nexus",
    "CellContent": ".domain_nexus",
    "CellIndex": ".domain_nexus",
    "CellIndexManager": ".domain_nexus",
    "LazyCellLoader": ".domain_nexus",
    "get_nexus": ".domain_nexus",
    "get_domain_nexus": ".domain_nexus",  # 别名
    "get_domain_system": ".domain_nexus",
    "query": ".domain_nexus",
    "evolve": ".domain_nexus",
    "get_status": ".domain_nexus",
    "execute_task": ".domain_nexus",
    "query_and_execute": ".domain_nexus",
    "quick_query": ".domain_nexus",
    "get_loading_stats": ".domain_nexus",
    "benchmark_loading": ".domain_nexus",
    # lazy_loader.py — 28KB, 加载工具
    "Preloader": ".lazy_loader",
    "LazyLoader": ".lazy_loader",
    "OnDemandLoader": ".lazy_loader",
    "LoadContext": ".lazy_loader",
    "preload": ".lazy_loader",
    "is_ready": ".lazy_loader",
    "quick_dispatch": ".lazy_loader",
    "get_load_info": ".lazy_loader",
    "benchmark_load_speeds": ".lazy_loader",
    # pan_wisdom_core.py — 76KB, 智慧树
    "WisdomSchool": ".pan_wisdom_core",
    "ProblemType": ".pan_wisdom_core",
    "PanWisdomTree": ".pan_wisdom_core",
    "ProblemIdentifier": ".pan_wisdom_core",
    "SchoolRecommender": ".pan_wisdom_core",
    "WisdomRecommendation": ".pan_wisdom_core",
    "PanWisdomResult": ".pan_wisdom_core",
    "preload_pan_wisdom": ".pan_wisdom_core",
    "is_pan_wisdom_ready": ".pan_wisdom_core",
    "get_pan_wisdom_cache": ".pan_wisdom_core",
    "get_pan_wisdom_on_demand": ".pan_wisdom_core",
    "get_pan_wisdom_load_info": ".pan_wisdom_core",
    "clear_pan_wisdom_cache": ".pan_wisdom_core",
    "benchmark_pan_wisdom_load": ".pan_wisdom_core",

    # growth_industry_bridge.py — v1.0, Growth+Industry → Pan-Wisdom (v7.0)
    "get_growth_recommendation": ".growth_industry_bridge",
    "get_industry_profile": ".growth_industry_bridge",
    "search_industry_profiles": ".growth_industry_bridge",
    "get_bagua_analysis": ".growth_industry_bridge",
    "get_growth_formula": ".growth_industry_bridge",
    "list_growth_templates": ".growth_industry_bridge",
    "list_industry_profiles": ".growth_industry_bridge",
    # eight_layer_pipeline.py — 119KB, 八层管道
    "EightLayerPipeline": ".eight_layer_pipeline",
    "ProcessingGrade": ".eight_layer_pipeline",
    "DomainCategory": ".eight_layer_pipeline",
    "PipelineStage": ".eight_layer_pipeline",
    "LayerResult": ".eight_layer_pipeline",
    "PipelineResult": ".eight_layer_pipeline",
    "InputLayer": ".eight_layer_pipeline",
    "NLAnalysisLayer": ".eight_layer_pipeline",
    "ClassificationDB": ".eight_layer_pipeline",
    "RoutingLayer": ".eight_layer_pipeline",
    "ReasoningLayer": ".eight_layer_pipeline",
    "ArgumentationLayer": ".eight_layer_pipeline",
    "OutputLayer": ".eight_layer_pipeline",
    "OptimizationLayer": ".eight_layer_pipeline",
    "quick_process": ".eight_layer_pipeline",
    "deep_process": ".eight_layer_pipeline",
    "super_process": ".eight_layer_pipeline",

    # output_engine.py — 多模态输出引擎 (v6.2)
    "OutputEngine": ".output_engine",
    "OutputFormat": ".output_engine",
    "OutputArtifact": ".output_engine",
    "OutputStrategy": ".output_engine",
    "OutputFormatDetector": ".output_engine",
    "RenderContext": ".output_engine",
    "TextOutputStrategy": ".output_engine",
    "MarkdownOutputStrategy": ".output_engine",
    "HtmlOutputStrategy": ".output_engine",
    "ImageOutputStrategy": ".output_engine",
    "PdfOutputStrategy": ".output_engine",
    "PptxOutputStrategy": ".output_engine",
    "DocxOutputStrategy": ".output_engine",

    # divine_oversight.py — 神政轨监督框架
    "DivineTrackOversight": ".divine_oversight",
    "OversightCategory": ".divine_oversight",
    "ComplianceLevel": ".divine_oversight",
    "OversightRecord": ".divine_oversight",
    "OversightReport": ".divine_oversight",
    "get_oversight": ".divine_oversight",
    "record_oversight": ".divine_oversight",
    "oversee_module": ".divine_oversight",
    "oversee_memory_io": ".divine_oversight",

    # web_integration.py — 网络搜索集成 (v1.0)
    "WebSearchMixin": ".web_integration",
    "NeuralMemoryWeb": ".web_integration",
    "RefuteCoreWeb": ".web_integration",
    "TianShuWeb": ".web_integration",
    "TrackAWeb": ".web_integration",
    "TrackBWeb": ".web_integration",
    "is_online": ".web_integration",
    "search_with_fallback": ".web_integration",
    "should_trigger_web_search": ".web_integration",

    # output_verifier.py — 输出验证器 (v1.0)
    "OutputVerifier": ".output_verifier",
    "VerificationStatus": ".output_verifier",
    "StatementType": ".output_verifier",
    "VerifiableStatement": ".output_verifier",
    "VerificationResult": ".output_verifier",
    "verify_llm_output": ".output_verifier",
    "verify_and_correct": ".output_verifier",
    "get_output_verifier": ".output_verifier",

    # reasoning_web_bridge.py — 推理-网络桥接 (v1.0)
    "ReasoningWebBridge": ".reasoning_web_bridge",
    "SearchIntent": ".reasoning_web_bridge",
    "WebSearchRequest": ".reasoning_web_bridge",
    "WebSearchResult": ".reasoning_web_bridge",
    "ReasoningWebContext": ".reasoning_web_bridge",
    "IntentClassifier": ".reasoning_web_bridge",
    "get_reasoning_bridge": ".reasoning_web_bridge",
    "needs_search": ".reasoning_web_bridge",
    "search_for_reasoning": ".reasoning_web_bridge",
    "enhance_with_web": ".reasoning_web_bridge",
    "auto_search_in_reasoning": ".reasoning_web_bridge",

    # llm_rule_layer.py — LLM统一规则层 (v7.0)
    "llm_chat": ".llm_rule_layer",
    "llm_analyze": ".llm_rule_layer",
    "llm_with_web_search": ".llm_rule_layer",
    "call_module_llm": ".llm_rule_layer",
    "get_llm_status": ".llm_rule_layer",
    "get_call_stats": ".llm_rule_layer",
    "LLMResponse": ".llm_rule_layer",
    "LLMSource": ".llm_rule_layer",
    "LLMCallStats": ".llm_rule_layer",

    # logic_bridge.py — v1.0, Logic → DivineReason 集成
    "FallacyCategory": ".logic_bridge",
    "FallacyDetection": ".logic_bridge",
    "detect_reasoning_fallacies": ".logic_bridge",
    "analyze_reasoning_quality": ".logic_bridge",
    "suggest_reasoning_improvements": ".logic_bridge",
    "enhance_reasoning_result": ".logic_bridge",
    "DivineReasonWithFallacyCheck": ".logic_bridge",
    # risk_security_bridge.py — v1.0, Risk+Security → RefuteCore 集成 (v3.0.2)
    "RefuteCoreWithRiskCheck": ".risk_security_bridge",
    "assess_argument_risk": ".risk_security_bridge",
    "enhance_refute_result": ".risk_security_bridge",
    "check_argument_compliance": ".risk_security_bridge",
    "analyze_emotion_health": ".risk_security_bridge",
    # literature_bridge.py — v1.0, Literature → DomainNexus 集成
    "LiteratureKnowledge": ".literature_bridge",
    "PoetryNodeType": ".literature_bridge",
    "PoetryEdgeType": ".literature_bridge",
    "PoetryKnowledgeNode": ".literature_bridge",
    "search_literature": ".literature_bridge",
    "analyze_poetry": ".literature_bridge",
    "get_author_network": ".literature_bridge",
    "build_literature_knowledge_graph": ".literature_bridge",
    "integrate_literature_to_domain_nexus": ".literature_bridge",
    # tianshu_output.py — v1.0, 第10个子系统（天枢输出层）
    "TianShuOutput": ".tianshu_output",
    "OutputFormat": ".tianshu_output",
    "ReportType": ".tianshu_output",
    "ChartType": ".tianshu_output",
    "ReportSection": ".tianshu_output",
    "ReportSpec": ".tianshu_output",
    "SlideSpec": ".tianshu_output",
    "ChartSpec": ".tianshu_output",
    "OutputResult": ".tianshu_output",
    "get_tianshu_output": ".tianshu_output",
    "generate_report": ".tianshu_output",
    "generate_slides": ".tianshu_output",
    "generate_chart": ".tianshu_output",
    # tianshu_input.py — v1.0, 天枢输入层
    "TianShuInput": ".tianshu_input",
    "FileMetadata": ".tianshu_input",
    "InputResult": ".tianshu_input",
    "get_tianshu_input": ".tianshu_input",
    "scan_file": ".tianshu_input",
    "scan_directory": ".tianshu_input",
    "analyze_attachment": ".tianshu_input",
    # closed_loop_solver.py — v1.0, 真正能解决问题的闭环工作流
    "ClosedLoopSolver": ".closed_loop_solver",
    "SolutionGenerator": ".closed_loop_solver",
    "SolutionVerifier": ".closed_loop_solver",
    "FeedbackManager": ".closed_loop_solver",
    "LearningEngine": ".closed_loop_solver",
    "SolutionPlan": ".closed_loop_solver",
    "ActionableStep": ".closed_loop_solver",
    "VerificationResult": ".closed_loop_solver",
    "UserFeedback": ".closed_loop_solver",
    "ClosedLoopResult": ".closed_loop_solver",
    "solve_problem": ".closed_loop_solver",
    "collect_feedback": ".closed_loop_solver",
    # solution_executor.py — v1.0, 方案执行器（真正解决问题）
    "SolutionExecutor": ".solution_executor",
    "ExecutionResult": ".solution_executor",
    "PlanExecutionResult": ".solution_executor",
    "execute_solution": ".solution_executor",

    # neural_memory_v7.py — 代理模块（实际实现在 smart_office_assistant.src.neural_memory）
    "get_neural_memory": ".neural_memory_v7",
    "NeuralMemory": ".neural_memory_v7",
    "DigitalStrategy": ".neural_memory_v7",
    "NeuralExecutor": ".neural_memory_v7",

    # pan_wisdom_core — 补充 get_pan_wisdom 映射
    "get_pan_wisdom": ".pan_wisdom_core",
}

# 已加载模块缓存（避免重复 importlib.import_module）
_LOADED_SUBMODULES: dict = {}


def __getattr__(name: str):
    """
    延迟加载属性 — 首次访问时才 import 对应模块

    Example:
        from knowledge_cells import DomainNexus  # 此时仅执行 L0 (~5ms)
        nexus = DomainNexus()  # ← 此时才真正 import domain_nexus.py (~80ms)
    """
    module_name = _LAZY_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    # 延迟导入模块
    if module_name not in _LOADED_SUBMODULES:
        _LOADED_SUBMODULES[module_name] = importlib.import_module(module_name, __name__)

    mod = _LOADED_SUBMODULES[module_name]
    # 将属性注入到当前模块，后续访问直接命中不再经过 __getattr__
    globals()[name] = getattr(mod, name)
    return globals()[name]

# 版本信息
__version__ = "S1.1"
__system_name__ = "SageDispatch"
__display_name__ = "贤者调度系统 S1.1 — 天枢 TianShu 生产运行版"
__domain_nexus_version__ = "S1.1"
__divine_reason_version__ = "S1.1"
__pan_wisdom_version__ = "7.0.0"
__lazy_load_version__ = "S1.1"
__eight_layer_version__ = "S1.1"
__oversight_version__ = "S1.1"
__output_engine_version__ = "S1.1"
__web_integration_version__ = "S1.1"
__output_verifier_version__ = "S1.1"
__reasoning_web_bridge_version__ = "S1.1"
__llm_rule_layer_version__ = "S1.1"

# 调度器注册表
DISPATCHERS = {
    "SD-P1": "问题调度（树干核心）",
    "SD-F1": "25学派融合",
    "SD-F2": "四级调度总控",
    "SD-R1": "三层推理监管",
    "SD-R2": "谬误检测",
    "SD-D1": "轻量深度推理",
    "SD-D2": "标准深度推理",
    "SD-D3": "极致深度推理",
    "SD-C1": "太极阴阳决策",
    "SD-C2": "神之架构决策",
    "SD-E1": "五步主链执行",
    "SD-L1": "学习进化",
}


def list_dispatchers() -> dict:
    """列出所有调度器"""
    return DISPATCHERS.copy()


def get_dispatcher_info(dispatcher_id: str) -> dict:
    """获取调度器信息"""
    return {
        "id": dispatcher_id,
        "name": DISPATCHERS.get(dispatcher_id, "未知"),
        "available": True,
    }


def info():
    """打印系统信息"""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║         天枢 TianShu — 贤者调度系统 S1.0                      ║
║           SageDispatch 生产运行版 + 八层智慧处理管道           ║
║           + 多模态输出引擎 (TEXT/MD/HTML/IMG/PDF/PPT/DOC)   ║
╠══════════════════════════════════════════════════════════════╣
║  12个专业调度器 + RefuteCore T2 + 八层管道 + 神行轨集成     ║
║                                                              ║
║  【快速加载架构 S1.0 FastBoot】                               ║
║  L0 立即加载 (~5ms): core.py 枚举/数据类 + 版本信息          ║
║  L1 懒导入 (~50ms): dispatchers / track_b / pan_wisdom       ║
║  L2 懒实例化 (~80ms): DomainNexus / RefuteCore               ║
║  S1.0: Pipeline 全局单例 + NLP结果缓存 + OutputEngine复用    ║
║  效果: import knowledge_cells 从 ~100ms 降至 ~5ms            ║
║                                                              ║
║  【八层管道 + 多模态输出 (S1.0)】                              ║
║  L1 输入层 → L2 NLP分析 → L3 需求分类 → L4 分流           ║
║  L5 推理层 → L6 论证层 → L7 多模态输出 → L8 优化层         ║
║  输出格式: TEXT / MARKDOWN / HTML / IMAGE / PDF / PPTX / DOCX║
║                                                              ║
║  【三个处理等级】                                            ║
║  基础(Basic): 快速响应，不进入神之架构                       ║
║  深度(Deep): 神之架构并行论证 + 翰林院审核                   ║
║  超级(Super): 全链路Claw讨论 + T2 RefuteCore 驳心引擎论证      ║
║                                                              ║
║  【调度器矩阵】                                              ║
║  树干: SD-P1 问题调度（核心）                               ║
║  融合层: SD-F1 学派融合 | SD-F2 四级总控                    ║
║  检测层: SD-R2 谬误检测                                     ║
║  推理层: SD-D1/D2/D3 深度推理                               ║
║  决策层: SD-C1 阴阳决策 | SD-C2 神之架构                    ║
║  执行层: SD-E1 五步主链                                     ║
║  进化层: SD-L1 学习进化                                      ║
║                                                              ║
║  【T2 论证引擎】RefuteCore 驳心引擎 v3.2                      ║
║    8维度反驳: 逻辑/证据/假设/反面/类比/权威/因果/价值           ║
║    强度评估: S/A/B/C/D/F 六级量化                             ║
║    风险判定: 红/橙/黄/绿 四级                                 ║
║                                                              ║
║  【神政轨监督框架 v1.0】                                      ║
║    过程记录: 各模块执行轨迹完整记录                           ║
║    成果验证: 输出合规性检查                                   ║
║    驳回机制: 不合规成果标记返回，不阻断工作流                  ║
║    NeuralMemory I/O: 输入输出监督                            ║
║                                                              ║
║  【神行轨集成】枝丫特权: 各调度器可调用神行轨完成执行        ║
║    SD-F1 → 礼部(文化)    SD-D系列 → 吏部(人才)              ║
║    SD-C2 → 兵部(战略)   SD-E1 → 工部(执行)                 ║
║    SD-L1 → 户部(资源)   SD-R2 → 刑部(合规)                 ║
║                                                              ║
║  【输出验证器 v1.0】                                          ║
║    自动核查LLM输出的客观事实陈述                              ║
║    数字/日期/定义 → 网络搜索验证 → 一致/冲突/无法验证        ║
║    冲突自动修正 → 置信度评分 → 人工复核标记                  ║
║                                                              ║
║  【推理-网络桥接 v1.0】                                       ║
║    LLM推理过程中主动触发网络搜索                             ║
║    搜索意图识别: 事实/数据/知识/新闻/趋势                    ║
║    结果注入推理上下文                                        ║
╚══════════════════════════════════════════════════════════════╝
    """)


__all__ = [
    # 核心
    "Level",
    "DispatcherState",
    "DispatchRequest",
    "DispatchResponse",
    "BaseDispatcher",
    "LevelAssessor",
    "DispatchEngine",

    # 快捷函数
    "dispatch",
    "chain",
    "smart_dispatch",
    "get_engine",

    # 调度器
    "FourLevelDispatchController",
    "ProblemDispatcher",
    "FallacyChecker",
    "SchoolFusion",
    "SuperReasoning",
    "YinYangDecision",
    "DivineArchitecture",
    "ChainExecutor",
    "ResultTracker",
    "WebSearchDispatcher",

    # DivineReason - v3.1.0 超级推理图引擎 (GoT + LongCoT + ToT + ReAct)
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

    # 神行轨适配器
    "TrackBExecutor",
    "get_track_b_executor",
    "execute_with_track_b",
    "wisdom_tree_call",
    "sd_f1_call",
    "sd_d_call",
    "sd_c1_call",
    "sd_c2_call",
    "sd_e1_call",
    "sd_l1_call",
    "sd_r2_call",

    # 工具
    "list_dispatchers",
    "get_dispatcher_info",
    "info",

    # 版本
    "__version__",
    "__system_name__",
    "__display_name__",
    "__pan_wisdom_version__",
    "DISPATCHERS",

    # DomainNexus - v2.2
    "DomainNexus",
    "DomainCellManager",
    "CellContent",
    "CellIndex",
    "CellIndexManager",
    "LazyCellLoader",
    "get_nexus",
    "get_domain_system",
    "query",
    "evolve",
    "get_status",
    "execute_task",
    "query_and_execute",
    "quick_query",
    "get_loading_stats",
    "benchmark_loading",

    # LazyLoader - v4.2 快速加载
    "Preloader",
    "LazyLoader",
    "OnDemandLoader",
    "LoadContext",
    "preload",
    "is_ready",
    "quick_dispatch",
    "get_load_info",
    "benchmark_load_speeds",

    # 八层智能处理管道 v5.0
    "EightLayerPipeline",
    "ProcessingGrade",
    "DomainCategory",
    "PipelineStage",
    "LayerResult",
    "PipelineResult",
    "InputLayer",
    "NLAnalysisLayer",
    "ClassificationDB",
    "RoutingLayer",
    "ReasoningLayer",
    "ArgumentationLayer",
    "OutputLayer",
    "OptimizationLayer",
    "quick_process",
    "deep_process",
    "super_process",

    # 多模态输出引擎 v1.0
    "OutputEngine",
    "OutputFormat",
    "OutputArtifact",
    "OutputStrategy",
    "OutputFormatDetector",
    "RenderContext",
    "TextOutputStrategy",
    "MarkdownOutputStrategy",
    "HtmlOutputStrategy",
    "ImageOutputStrategy",
    "PdfOutputStrategy",
    "PptxOutputStrategy",
    "DocxOutputStrategy",

    # Pan-Wisdom Tree - v2.0.0 预加载+懒加载版
    "WisdomSchool",
    "ProblemType",
    "PanWisdomTree",
    "ProblemIdentifier",
    "SchoolRecommender",
    "WisdomRecommendation",
    "PanWisdomResult",
    "preload_pan_wisdom",
    "is_pan_wisdom_ready",
    "get_pan_wisdom_cache",
    "get_pan_wisdom_on_demand",
    "get_pan_wisdom_load_info",
    "clear_pan_wisdom_cache",
    "benchmark_pan_wisdom_load",

    # web_search_engine.py — 网络搜索引擎 (v1.0)
    "WebSearchEngine",
    "SearchResult",
    "SearchResponse",
    "SearchMode",
    "SourceType",
    "is_online",
    "get_network_status",
    "search_web",
    "search_with_context",
    "batch_search",
    "quick_search",
    "deep_search",
    "get_search_stats",
    "clear_search_cache",
    "get_web_engine",

    # 神政轨监督框架 v1.0 - 过程记录、成果验证、驳回机制
    "DivineTrackOversight",
    "OversightCategory",
    "ComplianceLevel",
    "OversightRecord",
    "OversightReport",
    "get_oversight",
    "record_oversight",
    "oversee_module",
    "oversight_memory_io",
    "benchmark_oversight",

    # 输出验证器 v1.0
    "OutputVerifier",
    "VerificationStatus",
    "StatementType",
    "VerifiableStatement",
    "VerificationResult",
    "verify_llm_output",
    "verify_and_correct",
    "get_output_verifier",

    # 推理-网络桥接 v1.0
    "ReasoningWebBridge",
    "SearchIntent",
    "WebSearchRequest",
    "WebSearchResult",
    "ReasoningWebContext",
    "IntentClassifier",
    "get_reasoning_bridge",
    "needs_search",
    "search_for_reasoning",
    "enhance_with_web",
    "auto_search_in_reasoning",
]
