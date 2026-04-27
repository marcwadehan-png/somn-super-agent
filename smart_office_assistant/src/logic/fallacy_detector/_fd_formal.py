"""
__all__ = [
    'check_affirming_consequent',
    'check_denying_antecedent',
    'check_propositional_fallacies',
    'check_syllogism_fallacies',
    'detect_formal',
    'extract_terms',
    'has_undistributed_middle',
    'init_formal_fallacies',
]

形式谬误库与检测
"""

from typing import Dict, List
from ._fd_types import FallacyCategory, FallacyDetection
from datetime import datetime
import re

def init_formal_fallacies() -> Dict[str, Dict]:
    """初始化形式谬误库"""
    return {
        'affirming_the_consequent': {
            'name': '肯定后件谬误',
            'category': FallacyCategory.FORMAL,
            'pattern': r'如果.*那么.*\.?因为.*所以.*',  # 简化模式
            'description': '从条件命题的后件推断前件: P→Q, Q ⊢ P',
            'example': '如果是下雨,地就会湿.地湿了,所以下雨了.',
            'counterexample': '如果不下雨,地也可能因为洒水而湿',
            'severity': 'major',
            'correction': '不能从结果推断原因,需要额外证据支持'
        },
        'denying_the_antecedent': {
            'name': '否定前件谬误',
            'category': FallacyCategory.FORMAL,
            'description': '否定条件命题的前件来否定后件: P→Q, ~P ⊢ ~Q',
            'example': '如果是下雨,地就会湿.没下雨,所以地不会湿.',
            'counterexample': '没下雨,地也可能因为洒水而湿',
            'severity': 'major',
            'correction': '否定条件不能推出否定结果'
        },
        'undistributed_middle': {
            'name': '中项不周延',
            'category': FallacyCategory.FORMAL,
            'description': '三段论中中项至少有一次不周延',
            'example': '所有A都是B,所有C都是B,所以所有A都是C',
            'correction': '中项必须至少有一次周延'
        },
        'illicit_major': {
            'name': '大项非法周延',
            'category': FallacyCategory.FORMAL,
            'description': '大项在结论中周延但在前提中不周延',
            'example': '所有A都是B,所有C都不是A,所以所有C都不是B',
            'correction': '大项在结论中周延必须在前提中也周延'
        },
        'illicit_minor': {
            'name': '小项非法周延',
            'category': FallacyCategory.FORMAL,
            'description': '小项在结论中周延但在前提中不周延',
            'example': '所有A都是B,所有B都是C,所以所有C都是A',
            'correction': '小项在结论中周延必须在前提中也周延'
        },
        'four_terms': {
            'name': '四项谬误',
            'category': FallacyCategory.FORMAL,
            'description': '三段论中出现四个不同的项',
            'example': '所有A都是B,所有C都是D,所以所有A都是D',
            'correction': '有效的三段论只能包含三个项'
        },
        'exclusive_premises': {
            'name': '双否定前提',
            'category': FallacyCategory.FORMAL,
            'description': '三段论的两个前提都是否定的',
            'example': '没有A是B,没有C是B,所以没有A是C',
            'correction': '三段论不能有两个否定前提'
        },
        'affirmative_from_negative': {
            'name': '否定前提肯定结论',
            'category': FallacyCategory.FORMAL,
            'description': '三段论有否定前提但结论是肯定的',
            'example': '没有A是B,所有C都是A,所以所有C都是B',
            'correction': '有否定前提时结论必须是否定的'
        },
        'existential_fallacy': {
            'name': '存在谬误',
            'category': FallacyCategory.FORMAL,
            'description': '从全称命题推出特称结论',
            'example': '所有独角兽都是动物,所以有些动物是独角兽',
            'correction': '全称命题不承诺存在性'
        }
    }

def check_affirming_consequent(text: str) -> bool:
    """检查是否为肯定后件谬误"""
    patterns = [
        r'如果.*那么.*\.?因为.*所以',
        r'.*所以.*因为.*'
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def check_denying_antecedent(text: str) -> bool:
    """检查是否为否定前件谬误"""
    patterns = [
        r'如果.*那么.*\.?不是.*所以不是',
        r'.*不是.*所以不是.*'
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def has_undistributed_middle(premises: List[str]) -> bool:
    """
    检查中项是否不周延
    简化实现 - 实际需要完整的直言命题分析
    """
    return False  # 暂时返回False

def extract_terms(statements: List[str]) -> set:
    """
    提取三段论中的项
    简化实现 - 提取名词和代词
    """
    terms = set()
    for statement in statements:
        words = re.findall(r'[所有|没有|有些]\s*([^\s]+)\s*[是|不是]', statement)
        terms.update(words)
    return terms

def check_syllogism_fallacies(
    formal_fallacies: Dict[str, Dict],
    premises: List[str],
    conclusion: str
) -> List[FallacyDetection]:
    """检查三段论谬误"""
    detections = []
    
    # 检查中项不周延
    if has_undistributed_middle(premises):
        fallacy_info = formal_fallacies['undistributed_middle']
        detections.append(FallacyDetection(
            fallacy_name=fallacy_info['name'],
            category=fallacy_info['category'],
            description=fallacy_info['description'],
            severity=fallacy_info['severity'],
            confidence=0.8,
            suggestion=fallacy_info['correction'],
            detected_at=datetime.now()
        ))
    
    # 检查四项谬误
    terms = extract_terms(premises + [conclusion])
    if len(terms) > 3:
        fallacy_info = formal_fallacies['four_terms']
        detections.append(FallacyDetection(
            fallacy_name=fallacy_info['name'],
            category=fallacy_info['category'],
            description=fallacy_info['description'],
            severity=fallacy_info['severity'],
            confidence=0.9,
            suggestion=fallacy_info['correction'],
            detected_at=datetime.now()
        ))
    
    return detections

def check_propositional_fallacies(
    formal_fallacies: Dict[str, Dict],
    premises: List[str],
    conclusion: str
) -> List[FallacyDetection]:
    """检查命题逻辑谬误"""
    detections = []
    combined_text = ' '.join(premises) + ' ' + conclusion
    
    # 检查肯定后件谬误
    if check_affirming_consequent(combined_text):
        fallacy_info = formal_fallacies['affirming_the_consequent']
        detections.append(FallacyDetection(
            fallacy_name=fallacy_info['name'],
            category=fallacy_info['category'],
            description=fallacy_info['description'],
            severity=fallacy_info['severity'],
            confidence=0.7,
            suggestion=fallacy_info['correction'],
            detected_at=datetime.now()
        ))
    
    # 检查否定前件谬误
    if check_denying_antecedent(combined_text):
        fallacy_info = formal_fallacies['denying_the_antecedent']
        detections.append(FallacyDetection(
            fallacy_name=fallacy_info['name'],
            category=fallacy_info['category'],
            description=fallacy_info['description'],
            severity=fallacy_info['severity'],
            confidence=0.7,
            suggestion=fallacy_info['correction'],
            detected_at=datetime.now()
        ))
    
    return detections

def detect_formal(
    formal_fallacies: Dict[str, Dict],
    premises: List[str],
    conclusion: str
) -> List[FallacyDetection]:
    """
    检测形式谬误
    
    Args:
        formal_fallacies: 形式谬误库
        premises: 前提列表
        conclusion: 结论
        
    Returns:
        检测到的谬误列表
    """
    detections = []
    
    # 检查三段论形式谬误
    if len(premises) == 2:
        syllogism_fallacies = check_syllogism_fallacies(
            formal_fallacies, premises, conclusion
        )
        detections.extend(syllogism_fallacies)
    
    # 检查命题逻辑形式谬误
    prop_fallacies = check_propositional_fallacies(
        formal_fallacies, premises, conclusion
    )
    detections.extend(prop_fallacies)
    
    return detections
