"""
__all__ = [
    'create_capability_engine_map',
    'init_engines',
]

超级学习引擎 - 引擎初始化模块
"""

from typing import Dict, Any
from pathlib import Path
import logging

from src.core.paths import LEARNING_DIR
from src.learning.unified_learning_system import UnifiedLearningSystem, UnifiedLearningConfig
from src.neural_memory.learning_engine import LearningEngine as NeuralLearningEngine, LearningType as NeuralLearningType
from src.learning.engine.smart_learning_engine import SmartLearningEngine
from src.core.learning_engine import LearningEngine as CoreLearningEngine

logger = logging.getLogger(__name__)

def init_engines(config: Dict) -> Dict[str, Any]:
    """
    初始化所有学习引擎
    
    Args:
        config: 配置字典
        
    Returns:
        引擎字典
    """
    engines = {}
    base_path = config.get("base_path") or config.get("storage_path") or str(LEARNING_DIR)
    
    try:
        # unified学习系统
        unified_config = UnifiedLearningConfig(
            target_drive=config.get("target_drive", "E:"),
            max_concurrent_tasks=config.get("max_concurrent_tasks", 4)
        )
        engines["unified"] = UnifiedLearningSystem(unified_config)
        logger.info("  ✓ unified学习系统已加载")
    except Exception as e:
        logger.warning(f"  ✗ unified学习系统加载失败: {e}")
    
    try:
        # 神经记忆学习引擎
        engines["neural"] = NeuralLearningEngine(base_path)
        logger.info("  ✓ 神经记忆学习引擎已加载")
    except Exception as e:
        logger.warning(f"  ✗ 神经记忆学习引擎加载失败: {e}")
    
    try:
        # 智能学习引擎
        engines["smart"] = SmartLearningEngine()
        logger.info("  ✓ 智能学习引擎已加载")
    except Exception as e:
        logger.warning(f"  ✗ 智能学习引擎加载失败: {e}")
    
    try:
        # 核心学习引擎
        engines["core"] = CoreLearningEngine()
        logger.info("  ✓ 核心学习引擎已加载")
    except Exception as e:
        logger.warning(f"  ✗ 核心学习引擎加载失败: {e}")
    
    return engines

def create_capability_engine_map() -> Dict:
    """创建学习能力到引擎的映射"""
    return {
        "INSTANCE_LEARNING": ["neural", "smart"],
        "VALIDATION_LEARNING": ["neural", "unified"],
        "ERROR_LEARNING": ["neural", "smart"],
        "ASSOCIATION_LEARNING": ["neural", "smart"],
        "TRANSFER_LEARNING": ["unified", "smart"],
        "REINFORCEMENT_LEARNING": ["smart", "neural"],
        "LOCAL_DATA_LEARNING": ["unified"],
        "NEURAL_LEARNING": ["neural"],
        "SMART_LEARNING": ["smart"],
        "CONTINUOUS_LEARNING": ["unified", "neural"],
        "META_LEARNING": ["super"],  # 由超级引擎自己处理
        "NARRATIVE_LEARNING": ["narrative"],  # 叙事学习引擎 [v4.1.0]
    }
