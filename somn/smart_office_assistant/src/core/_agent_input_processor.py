"""AgentCore 输入处理与意图识别模块

__all__ = [
    'agent_process_input',
]

已从 agent_core.py 提取，负责理解用户输入、分类意图、调用各处理函数。
"""

from __future__ import annotations
import logging
import re
import json
from typing import Dict, List, Any, Optional
from loguru import logger

logger = logging.getLogger(__name__)
def agent_process_input(agent_core, user_input: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
    """
    处理用户输入的主入口
    
    Args:
        user_input: 用户输入文本
        context: 可选的上下文信息
        
    Returns:
        AgentResponse: 处理结果
    """
    from ._agent_types import AgentResponse
    
    try:
        # 更新会话上下文
        agent_core.session_context['interaction_count'] += 1
        
        # 理解意图
        intent = _agent_understand_intent(agent_core, user_input, context or {})
        
        # 收集上下文
        full_context = _agent_gather_context(agent_core, user_input, context or {}, intent)
        
        # 生成响应
        response = _agent_generate_response(agent_core, user_input, full_context, intent)
        
        # 学习从交互中
        if agent_core.learning_enabled:
            _agent_learn_from_interaction(agent_core, user_input, intent, response)
        
        return response
        
    except Exception as e:
        logger.error(f"[AgentCore] 处理输入异常: {e}")
        return AgentResponse(
            success=False,
            message="处理输入时发生错误",
            data={}
        )

def _agent_understand_intent(agent_core, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """理解用户意图."""
    try:
        intent_type = _agent_classify_input_intent(agent_core, user_input, context)
        
        return {
            'type': intent_type,
            'raw_input': user_input,
            'confidence': 0.9,
            'entities': _extract_entities(user_input),
            'sentiment': _analyze_sentiment(user_input)
        }
    except Exception as e:
        logger.warning(f"[意图理解] 异常: {e}")
        return {'type': 'unknown', 'confidence': 0.0}

def _agent_classify_input_intent(agent_core, user_input: str, context: Dict[str, Any]) -> str:
    """分类输入意图."""
    user_input_lower = user_input.lower().strip()
    
    # 文件操作
    if any(kw in user_input_lower for kw in ['扫描', 'scan', '查找大文件', '清理', 'clean']):
        return 'scan_files'
    if any(kw in user_input_lower for kw in ['生成报告', 'report', '总结']):
        return 'generate_report'
    
    # 文档创建
    if any(kw in user_input_lower for kw in ['创建word', 'create_word', '生成word', '写文档']):
        return 'create_word'
    if any(kw in user_input_lower for kw in ['创建ppt', 'create_ppt', '生成ppt', '幻灯片']):
        return 'create_ppt'
    if any(kw in user_input_lower for kw in ['创建pdf', 'create_pdf', '生成pdf']):
        return 'create_pdf'
    if any(kw in user_input_lower for kw in ['创建excel', 'create_excel', '生成表格', 'spreadsheet']):
        return 'create_excel'
    
    # 知识管理
    if any(kw in user_input_lower for kw in ['搜索知识', 'search_knowledge', '查询知识库']):
        return 'search_knowledge'
    if any(kw in user_input_lower for kw in ['添加知识', 'add_knowledge', '录入知识']):
        return 'add_knowledge'
    
    # 分析类
    if any(kw in user_input_lower for kw in ['分析', 'analyze']):
        return 'analyze'
    if any(kw in user_input_lower for kw in ['总结', 'summarize', '摘要']):
        return 'summarize'
    
    # 策略类
    if any(kw in user_input_lower for kw in ['策略', 'strategy', '增长', 'growth']):
        return 'create_strategy'
    
    # ML预测
    if any(kw in user_input_lower for kw in ['预测', 'predict', '趋势']):
        return 'ml_prediction'
    
    # 学习系统
    if any(kw in user_input_lower for kw in ['学习总结', 'learning_summary', '学习状态']):
        return 'learning_summary'
    if any(kw in user_input_lower for kw in ['触发学习', 'trigger_learning', '开始学习']):
        return 'trigger_learning'
    if any(kw in user_input_lower for kw in ['搜索学习', 'learning_search']):
        return 'search_learning'
    
    # 问候/感谢
    greeting_keywords = ['你好', 'hi', 'hello', '嗨', '您好', 'hey', 'greetings']
    if any(kw in user_input_lower for kw in greeting_keywords):
        return 'greeting'
    
    thanks_keywords = ['谢谢', 'thanks', '感谢', 'thank']
    if any(kw in user_input_lower for kw in thanks_keywords):
        return 'thanks'
    
    # 默认：通用对话
    return 'general_chat'

def _extract_entities(text: str) -> Dict[str, Any]:
    """提取命名实体（简化版）."""
    entities = {'numbers': [], 'files': [], 'urls': []}
    
    # 提取数字
    numbers = re.findall(r'\d+(?:\.\d+)?', text)
    entities['numbers'] = [float(n) if '.' in n else int(n) for n in numbers]
    
    # 提取文件路径
    file_pattern = r'[a-zA-Z]:\\[^\s]+|\/[^\s]+\.\w+'
    entities['files'] = re.findall(file_pattern, text)
    
    # 提取URL
    url_pattern = r'https?://[^\s]+'
    entities['urls'] = re.findall(url_pattern, text)
    
    return entities

def _analyze_sentiment(text: str) -> str:
    """简单情感分析."""
    positive_words = ['好', '棒', '优秀', '喜欢', '谢谢', '感谢', '太好了', '赞']
    negative_words = ['差', '烂', '糟', '不喜欢', '讨厌', '麻烦', '问题']
    
    pos_count = sum(1 for w in positive_words if w in text)
    neg_count = sum(1 for w in negative_words if w in text)
    
    if pos_count > neg_count:
        return 'positive'
    elif neg_count > pos_count:
        return 'negative'
    return 'neutral'

def _agent_gather_context(agent_core, user_input: str, context: Dict[str, Any], intent: Dict[str, Any]) -> Dict[str, Any]:
    """收集完整上下文."""
    full_context = {
        **context,
        'session': agent_core.session_context,
        'intent': intent,
        'timestamp': context.get('timestamp')
    }
    
    # 从记忆中获取相关上下文
    topic = _agent_extract_topic(agent_core, user_input)
    if topic:
        full_context['topic'] = topic
        agent_core.session_context['current_topic'] = topic
    
    return full_context

def _agent_extract_topic(agent_core, text: str) -> Optional[str]:
    """提取主题关键词."""
    try:
        # 简单关键词提取
        keywords = re.findall(r'[\u4e00-\u9fff]{2,}', text)
        if keywords:
            return keywords[0]
    except Exception as e:
        logger.debug(f"执行输入处理失败: {e}")
    return None

def _agent_generate_response(agent_core, user_input: str, context: Dict[str, Any], intent: Dict[str, Any]) -> AgentResponse:
    """根据意图生成响应."""
    from ._agent_types import AgentResponse
    
    intent_type = intent.get('type', 'unknown')
    
    # 根据意图类型调用对应处理函数
    handlers = {
        'create_word': _agent_handle_create_word,
        'create_ppt': _agent_handle_create_ppt,
        'create_pdf': _agent_handle_create_pdf,
        'create_excel': _agent_handle_create_excel,
        'search_knowledge': _agent_handle_search_knowledge,
        'add_knowledge': _agent_handle_add_knowledge,
        'summarize': _agent_handle_summarize,
        'analyze': _agent_handle_analyze,
        'greeting': _agent_handle_greeting,
        'thanks': _agent_handle_thanks,
        'llm_direct': _agent_handle_llm_direct,
        'general_chat': _agent_handle_general_chat,
        'conversational': _agent_handle_conversational,
        'scan_files': _agent_handle_scan_files,
        'clean_files': _agent_handle_clean_files,
        'generate_report': _agent_handle_generate_report,
        'create_strategy': _agent_handle_create_strategy,
        'ml_prediction': _agent_handle_ml_prediction,
        'learning_summary': _agent_handle_learning_summary,
        'trigger_learning': _agent_handle_trigger_learning,
        'search_learning': _agent_handle_search_learning,
    }
    
    handler = handlers.get(intent_type, _agent_handle_general_chat)
    
    try:
        return handler(agent_core, user_input, context)
    except Exception as e:
        logger.error(f"[响应生成] {intent_type} 处理异常: {e}")
        return AgentResponse(
            success=False,
            message="处理请求时发生错误",
            data={}
        )

def _agent_handle_create_word(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理创建 Word 文档请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="Word 文档创建功能已准备就绪",
        data={'action': 'create_word', 'input': user_input}
    )

def _agent_handle_create_ppt(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理创建 PPT 请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="PPT 创建功能已准备就绪",
        data={'action': 'create_ppt', 'input': user_input}
    )

def _agent_handle_create_pdf(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理创建 PDF 请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="PDF 创建功能已准备就绪",
        data={'action': 'create_pdf', 'input': user_input}
    )

def _agent_handle_create_excel(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理创建 Excel 请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="Excel 创建功能已准备就绪",
        data={'action': 'create_excel', 'input': user_input}
    )

def _agent_handle_search_knowledge(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理知识搜索请求."""
    from ._agent_types import AgentResponse
    query = user_input.replace('搜索', '').replace('知识', '').strip()
    return AgentResponse(
        success=True,
        message=f"正在搜索知识库: {query}",
        data={'action': 'search_knowledge', 'query': query}
    )

def _agent_handle_add_knowledge(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理添加知识请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="知识添加功能已准备就绪",
        data={'action': 'add_knowledge', 'input': user_input}
    )

def _agent_handle_summarize(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理总结请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="正在生成总结...",
        data={'action': 'summarize', 'input': user_input}
    )

def _agent_handle_analyze(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理分析请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="正在进行深度分析...",
        data={'action': 'analyze', 'input': user_input}
    )

def _agent_handle_greeting(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理问候."""
    from ._agent_types import AgentResponse
    greetings = ['你好！有什么我可以帮助你的吗？', '嗨！今天想做什么？', '你好，有什么需要？']
    import random
    return AgentResponse(
        success=True,
        message=random.choice(greetings),
        data={'action': 'greeting'}
    )

def _agent_handle_thanks(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理感谢."""
    from ._agent_types import AgentResponse
    responses = ['不客气！', '随时为你服务！', '有问题随时找我！']
    import random
    return AgentResponse(
        success=True,
        message=random.choice(responses),
        data={'action': 'thanks'}
    )

def _agent_handle_llm_direct(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """直接调用 LLM 处理."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="正在思考...",
        data={'action': 'llm_direct', 'input': user_input}
    )

def _agent_handle_general_chat(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """通用对话处理."""
    from ._agent_types import AgentResponse
    
    # 尝试使用 Somn Core 处理
    if agent_core.somn_core:
        try:
            result = agent_core.somn_core.run_agent_task(user_input, context)
            return AgentResponse(
                success=True,
                message=result.get('response', '处理完成'),
                data=result
            )
        except Exception as e:
            logger.warning(f"[通用对话] Somn 调用失败: {e}")
    
    return AgentResponse(
        success=True,
        message="我收到了你的消息。有什么我可以帮助的？",
        data={'action': 'general_chat', 'input': user_input}
    )

def _agent_handle_conversational(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """对话式交互处理."""
    return _agent_handle_general_chat(agent_core, user_input, context)

def _agent_handle_scan_files(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理文件扫描请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="正在扫描目录...",
        data={'action': 'scan_files', 'input': user_input}
    )

def _agent_handle_clean_files(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理文件清理请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="正在分析清理方案...",
        data={'action': 'clean_files', 'input': user_input}
    )

def _agent_handle_generate_report(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理报告生成请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="正在生成报告...",
        data={'action': 'generate_report', 'input': user_input}
    )

def _agent_handle_create_strategy(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理策略创建请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="正在制定增长策略...",
        data={'action': 'create_strategy', 'input': user_input}
    )

def _agent_handle_ml_prediction(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理 ML 预测请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="正在进行预测分析...",
        data={'action': 'ml_prediction', 'input': user_input}
    )

def _agent_handle_learning_summary(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理学习总结请求."""
    return agent_core.get_learning_summary()

def _agent_handle_trigger_learning(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理触发学习请求."""
    return agent_core.trigger_learning()

def _agent_handle_search_learning(agent_core, user_input: str, context: Dict) -> 'AgentResponse':
    """处理学习内容搜索请求."""
    from ._agent_types import AgentResponse
    return AgentResponse(
        success=True,
        message="正在搜索学习内容...",
        data={'action': 'search_learning', 'input': user_input}
    )
