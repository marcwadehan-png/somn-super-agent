"""
__all__ = [
    'build_reasoning_chain',
    'check_vague_expression',
    'classify_intent_from_text',
    'extract_keywords',
    'infer_intent',
    'match_mappings',
    'tokenize',
]

语义处理工具函数 - 分词、关键词提取、意图推断等内部工具
Semantic Processing Utilities - Tokenization, keyword extraction, intent inference, etc.
"""

import re
from typing import Dict, List, Tuple
from collections import defaultdict

def tokenize(text: str) -> List[str]:
    """中英文混合分词"""
    text = re.sub(r'\s+', ' ', text.strip())

    tokens = []

    # 提取英文单词
    english_words = re.findall(r"[a-zA-Z0-9_\-]{2,}", text)
    for word in english_words:
        tokens.append(word.lower())

    # 停用词集合
    stopwords = {
        '的', '了', '是', '在', '我', '你', '他', '她', '它', '们',
        '这', '那', '有', '和', '与', '或', '不', '也', '都', '就',
        '要', '会', '能', '可以', '一个', '一', '个', '把', '被',
        '一下', '什么', '怎么', '如何', '吗', '呢', '吧',
        '帮我', '帮我分析', '帮我分析一下', '研究一下', '看看', '看看那个'
    }

    # 提取所有2字词(滑动窗口)
    chinese_text = re.sub(r'[^\u4e00-\u9fff]', '', text)
    for i in range(len(chinese_text) - 1):
        token_2 = chinese_text[i:i+2]
        if token_2 not in stopwords:
            tokens.append(token_2)

    # 提取3字词
    for i in range(len(chinese_text) - 2):
        token_3 = chinese_text[i:i+3]
        if token_3 not in stopwords:
            tokens.append(token_3)

    # 提取4字词
    for i in range(len(chinese_text) - 3):
        token_4 = chinese_text[i:i+4]
        if token_4 not in stopwords:
            tokens.append(token_4)

    # 移除停用词并去重
    tokens = [t for t in tokens if t not in stopwords and len(t) >= 2]

    return list(set(tokens))[:30]

def extract_keywords(tokens: List[str]) -> List[str]:
    """提取关键词"""
    stopwords = {
        '的', '了', '是', '在', '我', '你', '他', '她', '它', '们',
        '这', '那', '有', '和', '与', '或', '不', '也', '都', '就',
        '要', '会', '能', '可以', '一个', '一', '个', '把', '被',
        '一下', '什么', '怎么', '如何', '吗', '呢', '吧',
    }

    keywords = [t for t in tokens if t not in stopwords and len(t) >= 2]

    # 去重并按长度排序
    keywords = sorted(set(keywords), key=len, reverse=True)

    return keywords[:15]

def match_mappings(keywords: List[str],
                   user_mappings: Dict[str, 'KeywordMapping'],
                   shared_mappings: Dict[str, 'KeywordMapping'],
                   user_id: str) -> List[Dict]:
    """匹配已知mapping"""
    matched = []

    for kw in keywords:
        # 先查用户mapping
        if kw in user_mappings.get(user_id, {}):
            mapping = user_mappings[user_id][kw]
            matched.append({
                'keyword': kw,
                'meaning': mapping.primary_meaning,
                'confidence': mapping.confidence,
                'source': 'user'
            })
        # 再查全局mapping
        elif kw in shared_mappings:
            mapping = shared_mappings[kw]
            matched.append({
                'keyword': kw,
                'meaning': mapping.primary_meaning,
                'confidence': mapping.confidence,
                'source': 'system'
            })

    return matched

def infer_intent(text: str, keywords: List[str], matched: List[Dict],
                 intent_patterns: Dict) -> Tuple[str, float]:
    """推断意图"""
    text_lower = text.lower()
    scores = defaultdict(float)

    for intent_name, intent_data in intent_patterns.items():
        for kw in intent_data.get('keywords', []):
            if kw in text_lower:
                scores[intent_name] += 1.0
            elif kw in keywords:
                scores[intent_name] += 0.5

        # 匹配mapping也增加分数
        for m in matched:
            if m['meaning'] and any(kw in m['meaning'] for kw in intent_data.get('keywords', [])):
                scores[intent_name] += 0.3

    if scores:
        best_intent = max(scores.items(), key=lambda x: x[1])
        max_score = best_intent[1]
        total_keywords = max(len(keywords), 1)
        confidence = min(1.0, max_score / total_keywords)

        return best_intent[0], confidence

    return 'unknown', 0.0

def classify_intent_from_text(text: str,
                              intent_patterns: Dict) -> str:
    """从文本分类意图"""
    keywords = extract_keywords(tokenize(text))
    intent, _ = infer_intent(text, keywords, [], intent_patterns)
    return intent

def check_vague_expression(text: str) -> Tuple[bool, str]:
    """检测模糊表达"""
    vague_patterns = ['这个', '那个', '这样', '那样', '类似的', '那件事']

    for pattern in vague_patterns:
        if pattern in text:
            return True, f'您说的"{pattern}"具体是指什么?能更详细地描述一下吗?'

    return False, ""

def build_reasoning_chain(text: str, keywords: List[str],
                          intent: str, matched: List[Dict]) -> List[str]:
    """构建推理链"""
    chain = []

    # 基础推断
    chain.append(f'输入: "{text}"')

    if keywords:
        chain.append(f"关键词: {', '.join(keywords[:5])}")

    if matched:
        matched_strs = [f"{m['keyword']}→{m['meaning']}" for m in matched[:3]]
        chain.append(f"已知mapping: {', '.join(matched_strs)}")

    chain.append(f"推断意图: {intent}")

    return chain
