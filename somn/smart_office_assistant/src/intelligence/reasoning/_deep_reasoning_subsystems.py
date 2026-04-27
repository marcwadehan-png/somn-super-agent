"""
__all__ = [
    'init_all_subsystems',
    'init_consulting_validator',
    'init_dewey_system',
    'init_logic_system',
    'init_neurodynamics',
    'init_top_thinking_system',
    'init_xinmind_system',
]

深度推理引擎子系统初始化模块
Deep Reasoning Engine Subsystem Initializers

包含6个子系统的懒加载初始化:
- 逻辑学系统 (谬误检测)
- 增长咨询验证引擎
- 神经动力学系统
- 王阳明心学系统
- 杜威反省思维系统
- 顶级思维法系统
"""

import logging
from loguru import logger

_log = logging.getLogger(__name__)

def init_logic_system(engine):
    """
    初始化逻辑学系统(谬误检测)
    
    Args:
        engine: DeepReasoningEngine 实例
        
    Sets:
        engine.fallacy_detector: FallacyDetector 或 None
    """
    try:
        from src.logic.fallacy_detector import FallacyDetector
        engine.fallacy_detector = FallacyDetector()
        logger.info("  ✓ 逻辑学系统加载完成(含战略咨询专用谬误检测)")
    except Exception as e:
        engine.fallacy_detector = None
        logger.warning(f"  ✗ 逻辑学系统加载失败: {e}")

def init_consulting_validator(engine):
    """
    初始化增长咨询验证引擎
    
    Args:
        engine: DeepReasoningEngine 实例
        
    Sets:
        engine.consulting_validator: ConsultingValidator 或 None
    """
    try:
        from ..engines.consulting_validator import ConsultingValidator
        engine.consulting_validator = ConsultingValidator()
        logger.info("  ✓ 增长咨询验证引擎加载完成")
    except Exception as e:
        engine.consulting_validator = None
        logger.warning(f"  ✗ 增长咨询验证引擎加载失败: {e}")

def init_neurodynamics(engine):
    """
    初始化神经动力学系统 [v1.0.0]
    
    Args:
        engine: DeepReasoningEngine 实例
        
    Sets:
        engine.neurodynamics: NeurodynamicsCore 或 None
        engine.synaptic_engine: SynapticPlasticityEngine 或 None
        engine.phase_coordinator: PhaseSynchronizationCoordinator 或 None
    """
    try:
        from ..engines.neurodynamics_core import NeurodynamicsCore
        from ..engines.synaptic_plasticity_engine import SynapticPlasticityEngine
        from .phase_synchronization_coordinator import PhaseSynchronizationCoordinator
        engine.neurodynamics = NeurodynamicsCore()
        engine.synaptic_engine = SynapticPlasticityEngine()
        engine.phase_coordinator = PhaseSynchronizationCoordinator()
        logger.info("  ✓ 神经动力学系统加载完成 (H-H模型+分岔分析+簇放电+E-I平衡+随机共振+STDP+Kuramoto)")
    except Exception as e:
        engine.neurodynamics = None
        engine.synaptic_engine = None
        engine.phase_coordinator = None
        logger.warning(f"  ✗ 神经动力学系统加载失败: {e}")

def init_xinmind_system(engine):
    """
    初始化王阳明心学系统 [v1.0.0]
    
    Args:
        engine: DeepReasoningEngine 实例
        
    Sets:
        engine.yangming_engine: YangmingXinxueEngine 或 None
    """
    try:
        from ..engines.philosophy.yangming_xinxue_engine import YangmingXinxueEngine
        engine.yangming_engine = YangmingXinxueEngine()
        logger.info("  ✓ 王阳明xinxue引擎加载完成 (知行合一+致良知+事上磨练)")
    except Exception as e:
        engine.yangming_engine = None
        logger.warning(f"  ✗ 王阳明xinxue引擎加载失败: {e}")

def init_dewey_system(engine):
    """
    初始化杜威反省思维系统 [v1.0.0]
    
    Args:
        engine: DeepReasoningEngine 实例
        
    Sets:
        engine.dewey_engine: DeweyThinkingEngine 或 None
    """
    try:
        from ..engines.dewey_thinking_engine import DeweyThinkingEngine
        engine.dewey_engine = DeweyThinkingEngine()
        logger.info("  ✓ 杜威反省思维引擎加载完成 (五步法+反省思维)")
    except Exception as e:
        engine.dewey_engine = None
        logger.warning(f"  ✗ 杜威反省思维引擎加载失败: {e}")

def init_top_thinking_system(engine):
    """
    初始化顶级思维法系统 [v1.0.0]
    
    Args:
        engine: DeepReasoningEngine 实例
        
    Sets:
        engine.top_thinking_engine: TopThinkingEngine 或 None
    """
    try:
        from ..engines.top_thinking_engine import TopThinkingEngine
        engine.top_thinking_engine = TopThinkingEngine()
        logger.info("  ✓ 顶级思维法引擎加载完成 (六大顶级思维)")
    except Exception as e:
        engine.top_thinking_engine = None
        logger.warning(f"  ✗ 顶级思维法引擎加载失败: {e}")

def init_all_subsystems(engine):
    """
    初始化所有子系统（便捷函数）
    
    Args:
        engine: DeepReasoningEngine 实例
    """
    init_logic_system(engine)
    init_consulting_validator(engine)
    init_neurodynamics(engine)
    init_xinmind_system(engine)
    init_dewey_system(engine)
    init_top_thinking_system(engine)
