"""AgentCore 动作执行模块

__all__ = [
    'agent_execute_action',
    'agent_extract_task_response',
]

已从 agent_core.py 提取，负责具体操作的执行。
"""

import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

def agent_execute_action(agent_core, action_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行具体操作
    
    Args:
        action_type: 操作类型
        parameters: 操作参数
        
    Returns:
        操作结果
    """
    action_map = {
        'scan_directory': _agent_action_scan_directory,
        'analyze_cleanup': _agent_action_analyze_cleanup,
        'trigger_learning': _agent_action_trigger_learning,
    }
    
    handler = action_map.get(action_type)
    if handler:
        return handler(agent_core, parameters)
    
    return {
        'success': False,
        'error': f'Unknown action type: {action_type}'
    }

def _agent_action_scan_directory(agent_core, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """扫描目录操作."""
    try:
        directory = parameters.get('directory', '.')
        max_depth = parameters.get('max_depth', 3)
        
        # 使用文件扫描器
        if agent_core.file_scanner:
            result = agent_core.file_scanner.scan(
                path=directory,
                max_depth=max_depth
            )
            return {
                'success': True,
                'action': 'scan_directory',
                'result': result
            }
        
        return {
            'success': True,
            'action': 'scan_directory',
            'result': {'message': '文件扫描器未初始化'}
        }
    except Exception as e:
        logger.error(f"[扫描目录] 异常: {e}")
        return {'success': False, 'error': '目录扫描失败'}

def _agent_action_analyze_cleanup(agent_core, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """分析清理操作."""
    try:
        target_path = parameters.get('path', '.')
        file_types = parameters.get('file_types', ['temp', 'cache', 'log'])
        
        # 使用文件清理器
        if agent_core.file_cleaner:
            analysis = agent_core.file_cleaner.analyze(target_path, file_types)
            return {
                'success': True,
                'action': 'analyze_cleanup',
                'result': analysis
            }
        
        return {
            'success': True,
            'action': 'analyze_cleanup',
            'result': {'message': '文件清理器未初始化'}
        }
    except Exception as e:
        logger.error(f"[分析清理] 异常: {e}")
        return {'success': False, 'error': '分析清理失败'}

def _agent_action_trigger_learning(agent_core, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """触发学习操作."""
    try:
        topic = parameters.get('topic', 'general')
        
        # 使用学习系统
        if agent_core.learning_system:
            result = agent_core.learning_system.trigger_learning(topic)
            return {
                'success': True,
                'action': 'trigger_learning',
                'result': result
            }
        
        return {
            'success': True,
            'action': 'trigger_learning',
            'result': {'message': '学习系统未初始化'}
        }
    except Exception as e:
        logger.error(f"[触发学习] 异常: {e}")
        return {'success': False, 'error': '触发学习失败'}

def agent_extract_task_response(agent_core, action_result: Dict[str, Any], intent: Dict[str, Any]) -> Dict[str, Any]:
    """
    从动作结果提取任务响应
    
    Args:
        action_result: 动作执行结果
        intent: 意图信息
        
    Returns:
        结构化的任务响应
    """
    action = intent.get('type', 'unknown')
    success = action_result.get('success', False)
    
    if not success:
        return {
            'strategy': 'error_handling',
            'action': None,
            'evaluation': {
                'success': False,
                'quality': 0.0,
                'message': action_result.get('error', 'Unknown error')
            },
            'next_steps': ['retry', 'fallback']
        }
    
    # 根据动作类型构建响应
    response_templates = {
        'scan_files': _build_scan_response,
        'clean_files': _build_clean_response,
        'generate_report': _build_report_response,
        'create_strategy': _build_strategy_response,
        'ml_prediction': _build_prediction_response,
    }
    
    builder = response_templates.get(action, _build_default_response)
    return builder(action_result, intent)

def _build_scan_response(result: Dict, intent: Dict) -> Dict:
    """构建扫描响应."""
    return {
        'strategy': 'direct_output',
        'action': 'scan_completed',
        'evaluation': {
            'success': True,
            'quality': 0.9,
            'message': '扫描完成'
        },
        'next_steps': ['view_results', 'analyze']
    }

def _build_clean_response(result: Dict, intent: Dict) -> Dict:
    """构建清理响应."""
    return {
        'strategy': 'direct_output',
        'action': 'cleanup_ready',
        'evaluation': {
            'success': True,
            'quality': 0.85,
            'message': '清理分析完成'
        },
        'next_steps': ['confirm_cleanup', 'cancel']
    }

def _build_report_response(result: Dict, intent: Dict) -> Dict:
    """构建报告响应."""
    return {
        'strategy': 'direct_output',
        'action': 'report_generated',
        'evaluation': {
            'success': True,
            'quality': 0.9,
            'message': '报告已生成'
        },
        'next_steps': ['download', 'view', 'share']
    }

def _build_strategy_response(result: Dict, intent: Dict) -> Dict:
    """构建策略响应."""
    return {
        'strategy': 'direct_output',
        'action': 'strategy_created',
        'evaluation': {
            'success': True,
            'quality': 0.85,
            'message': '策略方案已制定'
        },
        'next_steps': ['review', 'execute', 'modify']
    }

def _build_prediction_response(result: Dict, intent: Dict) -> Dict:
    """构建预测响应."""
    return {
        'strategy': 'direct_output',
        'action': 'prediction_complete',
        'evaluation': {
            'success': True,
            'quality': 0.8,
            'message': '预测分析完成'
        },
        'next_steps': ['view_details', 'export']
    }

def _build_default_response(result: Dict, intent: Dict) -> Dict:
    """构建默认响应."""
    return {
        'strategy': 'direct_output',
        'action': intent.get('type', 'completed'),
        'evaluation': {
            'success': True,
            'quality': 0.8,
            'message': '处理完成'
        },
        'next_steps': []
    }
