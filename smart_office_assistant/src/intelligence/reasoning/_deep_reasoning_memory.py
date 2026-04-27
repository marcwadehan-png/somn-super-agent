"""
__all__ = [
    'load_reasoning_memory',
    'save_reasoning_memory',
]

记忆管理与字典转换模块
负责推理记忆的加载/保存，以及字典到 ReasoningResult 的转换
"""
import json
import logging
from pathlib import Path
from typing import Dict, Union

from ..reasoning._deep_reasoning_types import ReasoningMode, ThoughtNode, ReasoningResult

logger = logging.getLogger(__name__)

def load_reasoning_memory(
    reasoning_memory_path: Union[str, Path], max_memory: int = 100
) -> Dict[str, ReasoningResult]:
    """
    加载推理记忆

    Args:
        reasoning_memory_path: 记忆文件路径
        max_memory: 最大记忆条数

    Returns:
        推理记忆字典 {result_id: ReasoningResult}
    """
    if not reasoning_memory_path:
        return {}

    path = Path(reasoning_memory_path)
    if not path.exists():
        return {}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        memory = {}
        for result_id, data in raw.items():
            memory[result_id] = _dict_to_result(data)
        # 保留最新 max_memory 条（如果 max_memory <= 0，跳过裁剪）
        if max_memory > 0 and len(memory) > max_memory:
            sorted_items = sorted(
                memory.items(),
                key=lambda x: x[1].metadata.get('timestamp', 0),
                reverse=True
            )
            memory = dict(sorted_items[:max_memory])
        return memory
    except Exception as e:
        logger.warning(f"加载推理记忆失败 {path}: {e}")
        return {}

def save_reasoning_memory(
    reasoning_memory_path: Union[str, Path],
    reasoning_memory: Dict[str, ReasoningResult]
):
    """
    保存推理记忆

    Args:
        reasoning_memory_path: 记忆文件路径
        reasoning_memory: 推理记忆字典
    """
    if not reasoning_memory_path:
        return
    try:
        path = Path(reasoning_memory_path)
        data = {
            result_id: result.to_dict()
            for result_id, result in reasoning_memory.items()
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"保存推理记忆失败 {reasoning_memory_path}: {e}")

def _dict_to_result(data: Dict) -> ReasoningResult:
    """
    将字典转换为推理结果

    Args:
        data: 记忆字典

    Returns:
        ReasoningResult
    """
    trace = [
        ThoughtNode(
            **{
                **node_data,
                'reasoning_mode': ReasoningMode(node_data['reasoning_mode'])
                if isinstance(node_data.get('reasoning_mode'), str)
                else node_data.get('reasoning_mode', ReasoningMode.CHAIN_OF_THOUGHT)
            }
        )
        for node_data in data.get('reasoning_trace', [])
    ]

    return ReasoningResult(
        result_id=data['result_id'],
        problem=data['problem'],
        reasoning_mode=ReasoningMode(data['reasoning_mode']),
        success=data['success'],
        reasoning_trace=trace,
        final_answer=data['final_answer'],
        confidence=data.get('confidence', 0.0),
        steps_count=data.get('steps_count', 0),
        execution_time=data.get('execution_time', 0.0),
        suggestions=data.get('suggestions', []),
        metadata=data.get('metadata', {})
    )

