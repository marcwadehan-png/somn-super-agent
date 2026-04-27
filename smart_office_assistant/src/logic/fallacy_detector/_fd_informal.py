"""
__all__ = [
    'calculate_fallacy_confidence',
    'detect_informal',
    'init_detection_patterns',
    'init_informal_fallacies',
]

非形式谬误库与检测
"""

from typing import Dict, List
from ._fd_types import FallacyCategory, FallacyDetection
from datetime import datetime
import re

def init_informal_fallacies() -> Dict[str, Dict]:
    """初始化非形式谬误库"""
    return {
        # 歧义谬误
        'equivocation': {
            'name': '偷换概念',
            'category': FallacyCategory.AMBIGUITY,
            'description': '在同一论证中多次使用一个词的不同含义',
            'example': '人必须吃饭.我是人,所以我必须吃饭.',
            'correction': '保持术语的一致性定义'
        },
        'amphiboly': {
            'name': '句法歧义',
            'category': FallacyCategory.AMBIGUITY,
            'description': '由于句子结构不清晰导致的歧义',
            'example': '我看到他带着望远镜',
            'correction': '明确句子结构,消除歧义'
        },
        'accent': {
            'name': '强调谬误',
            'category': FallacyCategory.AMBIGUITY,
            'description': '通过改变强调来扭曲原意',
            'example': '他说"我不会撒谎"',
            'correction': '避免断章取义'
        },
        'composition': {
            'name': '合成谬误',
            'category': FallacyCategory.AMBIGUITY,
            'description': '从部分具有的属性推断整体也具有',
            'example': '每个机器人都很轻,所以整个机器人军团很轻',
            'correction': '区分部分属性和整体属性'
        },
        'division': {
            'name': '分解谬误',
            'category': FallacyCategory.AMBIGUITY,
            'description': '从整体具有的属性推断部分也具有',
            'example': '这个团队很强大,所以每个成员都很强大',
            'correction': '整体属性不能自动转移到部分'
        },
        
        # 相关性谬误
        'ad_hominem': {
            'name': '人身攻击',
            'category': FallacyCategory.RELEVANCE,
            'description': '攻击人而不是论证',
            'example': '他的说法不可信,因为他以前撒过谎',
            'correction': '关注论证本身,而非论证者'
        },
        'straw_man': {
            'name': '稻草人谬误',
            'category': FallacyCategory.RELEVANCE,
            'description': '歪曲对方观点然后攻击这个歪曲的观点',
            'example': '他说要减少开支,所以他想让大家都失业',
            'correction': '准确理解对方的实际观点'
        },
        'red_herring': {
            'name': '红鲱鱼谬误',
            'category': FallacyCategory.RELEVANCE,
            'description': '引入无关话题分散注意力',
            'example': '我们不需要讨论这个,更重要的是...[无关话题]',
            'correction': '保持话题的相关性'
        },
        'appeal_to_authority': {
            'name': '诉诸权威',
            'category': FallacyCategory.RELEVANCE,
            'description': '仅仅因为某人是权威就接受其观点',
            'example': '专家说这样是对的,所以它是对的',
            'correction': '权威观点需要证据支持,而非盲从'
        },
        'appeal_to_popularity': {
            'name': '诉诸大众',
            'category': FallacyCategory.RELEVANCE,
            'description': '因为很多人相信所以认为正确',
            'example': '大家都这么想,所以这是对的',
            'correction': '真理不由人数决定'
        },
        'appeal_to_emotion': {
            'name': '诉诸情感',
            'category': FallacyCategory.RELEVANCE,
            'description': '利用情感而非逻辑来说服',
            'example': '想想那些可怜的孩子吧',
            'correction': '用逻辑和证据而非情感来论证'
        },
        'appeal_to_force': {
            'name': '诉诸武力',
            'category': FallacyCategory.RELEVANCE,
            'description': '用威胁而非论证来说服',
            'example': '如果你不接受我的观点,后果自负',
            'correction': '避免威胁,理性讨论'
        },
        'guilt_by_association': {
            'name': '有罪推定',
            'category': FallacyCategory.RELEVANCE,
            'description': '因为与某人有关联就认为有同样的问题',
            'example': '他和坏人在一起,所以他也是坏人',
            'correction': '个人行为不由他人决定'
        },
        'circumstantial_ad_hominem': {
            'name': '情境人身攻击',
            'category': FallacyCategory.RELEVANCE,
            'description': '因为对方的利益或立场而质疑其论证',
            'example': '你当然这么说,你是这个行业的',
            'correction': '论证的有效性不取决于论证者的立场'
        },
        
        # 预设谬误
        'begging_the_question': {
            'name': '循环论证/乞题',
            'category': FallacyCategory.PRESUMPTION,
            'description': '用结论作为前提来证明结论',
            'example': '上帝存在,因为圣经这么说,而圣经是上帝写的',
            'correction': '避免循环依赖,寻找独立证据'
        },
        'complex_question': {
            'name': '复合问题',
            'category': FallacyCategory.PRESUMPTION,
            'description': '问题中预设了未证明的前提',
            'example': '你停止打你妻子了吗?',
            'correction': '将复合问题分解为独立问题'
        },
        'false_dilemma': {
            'name': '虚假二分法',
            'category': FallacyCategory.PRESUMPTION,
            'description': '只给出两个极端选项而忽略其他可能',
            'example': '你要么支持我们,要么就是敌人',
            'correction': '考虑所有可能的选项'
        },
        'appeal_to_ignorance': {
            'name': '诉诸无知',
            'category': FallacyCategory.PRESUMPTION,
            'description': '因为没有证据证明X错就认为X对',
            'example': '没人证明鬼不存在,所以鬼存在',
            'correction': '缺乏证据不等于支持或反对'
        },
        'false_cause': {
            'name': '虚假因果',
            'category': FallacyCategory.CAUSATION,
            'description': '错误地认为A导致B',
            'example': '公鸡打鸣后太阳升起,所以公鸡导致日出',
            'correction': '因果关系需要严格验证'
        },
        'post_hoc': {
            'name': '后此谬误',
            'category': FallacyCategory.CAUSATION,
            'description': '仅仅因为A发生在B之前就认为A导致B',
            'example': '自从新政策出台,犯罪率下降,所以政策有效',
            'correction': '相关性不等于因果性'
        },
        'slippery_slope': {
            'name': '滑坡谬误',
            'category': FallacyCategory.CAUSATION,
            'description': '认为某事会导致一连串不可控的后果',
            'example': '如果我们允许A,那么B,然后C,最后...灾难',
            'correction': '每一步都需要独立论证'
        },
        'hasty_generalization': {
            'name': '草率概括',
            'category': FallacyCategory.PRESUMPTION,
            'description': '从样本不足的案例中得出普遍结论',
            'example': '我遇到的两个法国人都很粗鲁,所以法国人都很粗鲁',
            'correction': '需要足够大且具代表性的样本'
        },
        'biased_sample': {
            'name': '有偏样本',
            'category': FallacyCategory.PRESUMPTION,
            'description': '样本不能代表整体',
            'example': '在我这个富人区,大家都支持减税',
            'correction': '确保样本的代表性'
        },
        'accident': {
            'name': '意外概括',
            'category': FallacyCategory.PRESUMPTION,
            'description': '将一般规则应用在不适合的特定情况',
            'example': '应该自由说话,所以你可以威胁他人',
            'correction': '注意规则的适用范围和例外'
        }
    }

def init_detection_patterns() -> Dict[str, List[str]]:
    """初始化检测模式"""
    return {
        'affirming_consequent': [
            r'如果.*那么.*\.?因为.*所以',
            r'.*\.?所以.*因为.*',
            r'既然.*那么'
        ],
        'ad_hominem': [
            r'他.*所以',
            r'你是.*所以',
            r'这种人说的话'
        ],
        'straw_man': [
            r'所以你想.*',
            r'你是说',
            r'你以为',
            r'你根本不懂'
        ],
        'false_dilemma': [
            r'要么.*要么',
            r'只有.*才能',
            r'不是.*就是'
        ],
        'appeal_to_popularity': [
            r'大家都',
            r'多数人',
            r'很多人认为',
            r'普遍认为'
        ],
        'appeal_to_authority': [
            r'专家说',
            r'权威认为',
            r'教授指出'
        ],
        'hasty_generalization': [
            r'所有.*都',
            r'每个.*都是',
            r'凡是.*都',
            r'根本.*',
            r'绝对.*'
        ]
    }

def calculate_fallacy_confidence(
    informal_fallacies: Dict[str, Dict],
    patterns: Dict[str, List[str]],
    argument: str,
    fallacy_id: str
) -> float:
    """
    计算谬误的置信度
    """
    confidence = 0.0
    
    if fallacy_id in patterns:
        pattern_list = patterns[fallacy_id]
        matches = 0
        for pattern in pattern_list:
            if re.search(pattern, argument, re.IGNORECASE):
                matches += 1
        if len(pattern_list) > 0:
            confidence += (matches / len(pattern_list)) * 0.5
    
    # 基于结构characteristics
    if fallacy_id == 'false_dilemma':
        if '要么' in argument or '只有' in argument:
            confidence += 0.3
    elif fallacy_id == 'hasty_generalization':
        if any(word in argument for word in ['所有', '每个', '凡是', '根本', '绝对']):
            confidence += 0.4
    elif fallacy_id == 'ad_hominem':
        if '你' in argument or '他' in argument:
            confidence += 0.3
    
    return min(confidence, 1.0)

def detect_informal(
    informal_fallacies: Dict[str, Dict],
    patterns: Dict[str, List[str]],
    argument: str
) -> List[FallacyDetection]:
    """
    检测非形式谬误
    """
    detections = []

    for fallacy_id, fallacy_info in informal_fallacies.items():
        confidence = calculate_fallacy_confidence(
            informal_fallacies, patterns, argument, fallacy_id
        )

        if confidence > 0.3:  # 置信度阈值
            detection = FallacyDetection(
                fallacy_name=fallacy_info['name'],
                category=fallacy_info['category'],
                description=fallacy_info['description'],
                severity=fallacy_info.get('severity', 'minor'),
                confidence=confidence,
                suggestion=fallacy_info['correction'],
                detected_at=datetime.now()
            )
            detections.append(detection)

    # 按置信度排序
    detections.sort(key=lambda x: x.confidence, reverse=True)
    return detections
