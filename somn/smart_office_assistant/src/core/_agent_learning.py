"""AgentCore 学习系统模块

__all__ = [
    'agent_get_learning_status',
    'agent_get_learning_summary',
    'agent_learn_from_interaction',
    'agent_run_daily_learning',
    'agent_trigger_learning',
]

已从 agent_core.py 提取，负责学习状态管理和从交互中学习。
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from loguru import logger

logger = logging.getLogger(__name__)
def agent_run_daily_learning(agent_core) -> Dict[str, Any]:
    """执行每日学习任务."""
    try:
        if not agent_core.daily_learning:
            return {'success': False, 'message': '学习系统未初始化'}
        
        result = agent_core.daily_learning.run()
        
        # 记录学习历史
        _persist_learning_history(agent_core, 'daily', result)
        
        return {
            'success': True,
            'message': '每日学习完成',
            'result': result
        }
    except Exception as e:
        logger.error(f"[每日学习] 异常: {e}")
        return {'success': False, 'error': '每日学习执行失败'}

def agent_get_learning_summary(agent_core) -> Dict[str, Any]:
    """获取学习摘要."""
    try:
        if not agent_core.learning_system:
            return {
                'success': True,
                'message': '学习系统未初始化',
                'data': {}
            }
        
        # 从学习系统获取摘要
        summary = agent_core.learning_system.get_summary()
        
        return {
            'success': True,
            'message': '获取学习摘要成功',
            'data': summary
        }
    except Exception as e:
        logger.error(f"[学习摘要] 异常: {e}")
        return {'success': False, 'error': '获取学习摘要失败'}

def agent_trigger_learning(agent_core, topic: Optional[str] = None) -> Dict[str, Any]:
    """触发学习."""
    try:
        topic = topic or 'general'
        
        if not agent_core.learning_system:
            return {'success': False, 'message': '学习系统未初始化'}
        
        result = agent_core.learning_system.learn(topic)
        
        return {
            'success': True,
            'message': f'学习主题 {topic} 完成',
            'result': result
        }
    except Exception as e:
        logger.error(f"[触发学习] 异常: {e}")
        return {'success': False, 'error': '触发学习失败'}

def agent_get_learning_status(agent_core) -> Dict[str, Any]:
    """获取学习状态."""
    try:
        status = {
            'learning_enabled': agent_core.learning_enabled,
            'initialized': agent_core._learning_initialized if hasattr(agent_core, '_learning_initialized') else False,
            'daily_learning': agent_core.daily_learning is not None,
            'learning_system': agent_core.learning_system is not None,
        }
        
        if agent_core.learning_system:
            try:
                status['metrics'] = agent_core.learning_system.get_metrics()
            except Exception as e:
                logger.debug(f"加载学习数据失败: {e}")
        
        return {
            'success': True,
            'message': '获取学习状态成功',
            'data': status
        }
    except Exception as e:
        logger.error(f"[学习状态] 异常: {e}")
        return {'success': False, 'error': '获取学习状态失败'}

def agent_learn_from_interaction(agent_core, user_input: str, intent: Dict[str, Any], response: Any) -> None:
    """从交互中学习."""
    try:
        if not agent_core.learning_enabled:
            return
        
        # 构建学习记录
        learning_record = {
            'timestamp': datetime.now().isoformat(),
            'input': user_input,
            'intent': intent.get('type', 'unknown'),
            'confidence': intent.get('confidence', 0.0),
            'success': response.success if hasattr(response, 'success') else True
        }
        
        # 存储到记忆系统
        if agent_core.memory:
            agent_core.memory.add(
                content=json.dumps(learning_record, ensure_ascii=False),
                category='learning_interaction'
            )
        
        logger.debug(f"[学习] 记录交互: {intent.get('type')}")
        
    except Exception as e:
        logger.warning(f"[从交互学习] 异常: {e}")

def _persist_learning_history(agent_core, learning_type: str, result: Any) -> None:
    """持久化学学习历史."""
    try:
        history_file = agent_core.config.get('learning_history_file', 'data/learning_history.json')
        
        # 读取现有历史
        history = []
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except FileNotFoundError:
            pass
        
        # 添加新记录
        history.append({
            'type': learning_type,
            'timestamp': datetime.now().isoformat(),
            'result': result if isinstance(result, dict) else {'message': str(result)}
        })
        
        # 保留最近100条
        history = history[-100:]
        
        # 写入
        import os
        os.makedirs(os.path.dirname(history_file) if os.path.dirname(history_file) else '.', exist_ok=True)
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        logger.warning(f"[持久化学学习历史] 异常: {e}")
