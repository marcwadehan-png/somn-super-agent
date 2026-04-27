# -*- coding: utf-8 -*-
"""
__all__ = [
    'classify_intent',
    'gather_context',
    'understand_intent',
]

意图理解模块 - IntentHandler
负责用户意图分类、意图理解、上下文收集
"""
import time
import hashlib
import re
from typing import Any, Dict, List, Optional, Tuple

class IntentClassifier:
    """
    意图分类器

    职责：
    1. 意图类型分类（对话型/论证型/任务型）
    2. 关键词提取
    3. 意图置信度评估
    """

    # 意图类型常量
    INTENT_CHAT = 'chat'           # 对话型
    INTENT_ARGUMENT = 'argument'    # 论证型
    INTENT_TASK = 'task'           # 任务型
    INTENT_LEARNING = 'learning'    # 学习型
    INTENT_GENERAL = 'general'      # 一般型

    def __init__(self):
        # 意图关键词映射
        self._intent_keywords = {
            self.INTENT_TASK: [
                '创建', '生成', '分析', '查找', '搜索', '扫描', '清理',
                '帮我', '我要', '请', '给我', '生成一个', '写一个'
            ],
            self.INTENT_LEARNING: [
                '学习', '总结', '回顾', '记录', '教会', '教我'
            ],
            self.INTENT_ARGUMENT: [
                '为什么', '怎么看', '觉得', '认为', '讨论', '探讨',
                '分析一下', '对比'
            ],
        }

        # 动作关键词映射
        self._action_keywords = {
            'create_word': ['word', '文档', 'docx', '报告', '文章', '写'],
            'create_ppt': ['ppt', '幻灯片', '演示', '讲稿', 'presentation'],
            'create_pdf': ['pdf'],
            'create_excel': ['excel', '表格', 'xlsx', '数据表'],
            'search_knowledge': ['搜索知识', '查找知识', '知识库'],
            'add_knowledge': ['添加知识', '加入知识', '录入知识'],
            'summarize': ['总结', '概括', '摘要'],
            'analyze': ['分析'],
            'scan_files': ['扫描', '查看文件', '列出'],
            'clean_files': ['清理', '删除', '清除'],
            'generate_report': ['生成报告'],
            'create_strategy': ['策略', '增长方案', 'strategy'],
            'ml_prediction': ['预测', '预估'],
        }

    def classify_intent(self, user_input: str, context: Dict = None) -> Dict[str, Any]:
        """
        意图分类

        Args:
            user_input: 用户输入
            context: 上下文信息

        Returns:
            {
                'intent_type': str,
                'confidence': float,
                'keywords': list,
                'action': str or None
            }
        """
        user_input_lower = user_input.lower()
        keywords = self._extract_keywords(user_input)

        # 判断意图类型
        intent_type, confidence = self._determine_intent_type(user_input_lower, keywords)

        # 判断具体动作
        action = self._detect_action(user_input_lower, keywords)

        return {
            'intent_type': intent_type,
            'confidence': confidence,
            'keywords': keywords,
            'action': action,
            'original_input': user_input,
        }

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单分词
        words = re.findall(r'[\w]+', text.lower())
        # 过滤停用词
        stopwords = {'的', '了', '是', '在', '和', '我', '你', '他', '她', '它', '这', '那', '有', '个'}
        return [w for w in words if w not in stopwords and len(w) > 1]

    def _determine_intent_type(self, text: str, keywords: List[str]) -> Tuple[str, float]:
        """判断意图类型"""
        # 论证型特征
        argument_score = sum(1 for kw in keywords if kw in [
            '为什么', '怎么看', '认为', '觉得', '讨论', '分析', '对比'
        ])
        if argument_score >= 1:
            return self.INTENT_ARGUMENT, 0.8

        # 任务型特征
        task_score = sum(1 for kw in keywords if kw in [
            '创建', '生成', '分析', '查找', '搜索', '扫描', '清理', '帮我'
        ])
        if task_score >= 1:
            return self.INTENT_TASK, 0.9

        # 学习型特征
        learning_score = sum(1 for kw in keywords if kw in [
            '学习', '总结', '记录', '教会'
        ])
        if learning_score >= 1:
            return self.INTENT_LEARNING, 0.85

        # 对话型（闲聊、寒暄）
        chat_patterns = [
            '你好', 'hello', 'hi', '嗨', '早上好', '下午好', '晚上好',
            '谢谢', '感谢', '再见', 'bye'
        ]
        if any(p in text for p in chat_patterns):
            return self.INTENT_CHAT, 0.95

        # 默认为一般对话
        return self.INTENT_GENERAL, 0.5

    def _detect_action(self, text: str, keywords: List[str]) -> Optional[str]:
        """检测具体动作"""
        for action, action_kws in self._action_keywords.items():
            if any(kw in text for kw in action_kws):
                return action
        return None

    def understand_intent(self, user_input: str, context: Dict = None) -> Dict[str, Any]:
        """
        理解用户意图 - 综合意图分析

        Args:
            user_input: 用户输入
            context: 上下文

        Returns:
            意图理解结果
        """
        result = self.classify_intent(user_input, context)

        # 补充语义理解
        result['semantic_understanding'] = self._semantic_understand(user_input)

        return result

    def _semantic_understand(self, text: str) -> Dict[str, Any]:
        """语义理解"""
        keywords = self._extract_keywords(text)

        return {
            'keywords': keywords,
            'topic': self._extract_topic(text),
            'sentiment': 'neutral',  # 简化版
            'urgency': self._assess_urgency(text),
        }

    def _extract_topic(self, text: str) -> str:
        """提取主题"""
        # 简单实现：取最长/最重要的词
        words = re.findall(r'[\w]+', text)
        if not words:
            return 'unknown'
        # 返回最长词
        return max(words, key=len)

    def _assess_urgency(self, text: str) -> str:
        """评估紧急程度"""
        urgent_kws = ['紧急', '马上', '立刻', '尽快', '今天', '尽快']
        if any(kw in text for kw in urgent_kws):
            return 'high'
        return 'normal'

    def gather_context(self, user_input: str, context: Dict = None) -> Dict[str, Any]:
        """
        收集相关上下文

        Args:
            user_input: 用户输入
            context: 已有上下文

        Returns:
            扩充后的上下文
        """
        gathered = context.copy() if context else {}

        # 提取关键词
        gathered['keywords'] = self._extract_keywords(user_input)

        # 添加时间戳
        gathered['timestamp'] = time.time()

        # 计算输入hash（用于缓存）
        gathered['input_hash'] = hashlib.md5(user_input.encode()).hexdigest()

        return gathered
