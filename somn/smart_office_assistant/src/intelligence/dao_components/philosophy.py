# -*- coding: utf-8 -*-
"""
__all__ = [
    'get_wisdom',
    'match_theme',
]

道家哲学模块 - DaoPhilosophy
负责道德经、庄子等经典哲学智慧的提取和应用
"""
from typing import Any, Dict, List, Optional

class DeJingPhilosophy:
    """
    道德经哲学

    职责：
    1. 道德经主题匹配
    2. 核心智慧提取
    3. 情境应用
    """

    # 道德经主题关键词映射
    THEMES = {
        '自然无为': {
            'keywords': ['自然', '无为', '道法自然', '顺其自然', '不强求', '自然规律'],
            'quotes': [
                '人法地，地法天，天法道，道法自然。',
                '为学日益，为道日损，损之又损，以至于无为，无为而无不为。',
            ],
            'insights': [
                '尊重事物发展的自然规律，不过度干预',
                '真正的智慧在于知道何时该行动，何时该静观',
            ]
        },
        '柔弱胜刚强': {
            'keywords': ['柔弱', '刚强', '水', '柔能克刚', '以柔克刚'],
            'quotes': [
                '天下莫柔弱于水，而攻坚强者莫之能胜。',
                '柔弱胜刚强。',
                '强大处下，柔弱处上。',
            ],
            'insights': [
                '柔弱不是软弱，而是一种韧性和适应性',
                '真正的力量在于包容和顺应，而非对抗',
            ]
        },
        '知足不争': {
            'keywords': ['知足', '不争', '欲望', '贪', '寡欲', '少私'],
            'quotes': [
                '知足者富，强行者有志。',
                '罪莫大于可欲，祸莫大于不知足，咎莫大于欲得。',
                '为而不争，夫唯不争，天下莫能与之争。',
            ],
            'insights': [
                '知足是内在富足的源泉',
                '不争不是放弃，而是以退为进的策略',
            ]
        },
        '清静治国': {
            'keywords': ['清静', '治国', '无为而治', '清净', '安定'],
            'quotes': [
                '致虚极，守静笃。万物并作，吾以观复。',
                '清静为天下正。',
                '我无为而民自化，我好静而民自正。',
            ],
            'insights': [
                '领导者的心态决定团队的状态',
                '少即是多，给空间比给命令更有效',
            ]
        },
        '上善若水': {
            'keywords': ['善', '水', '利他', '谦下', '不争'],
            'quotes': [
                '上善若水，水善利万物而不争。',
                '夫唯不争，故无尤。',
                '居善地，心善渊，与善仁，言善信，政善治，事善能，动善时。',
            ],
            'insights': [
                '最高的善像水一样，滋养万物而不求回报',
                '选择合适的位置，保持内心的深沉',
            ]
        },
        '返璞归真': {
            'keywords': ['返璞', '归真', '纯朴', '天真', '质朴', '素'],
            'quotes': [
                '见素抱朴，少私寡欲。',
                '含德之厚，比于赤子。',
                '复归于婴儿，复归于朴。',
            ],
            'insights': [
                '保持纯真本性是最高智慧',
                '复杂是混乱的根源，简化是管理的精髓',
            ]
        },
    }

    def __init__(self):
        self._themes = self.THEMES

    def match_theme(self, query: str) -> List[str]:
        """
        根据问题匹配道德经主题

        Args:
            query: 用户查询

        Returns:
            匹配的主题列表
        """
        query_lower = query.lower()
        matched = []

        for theme, data in self._themes.items():
            for keyword in data['keywords']:
                if keyword in query_lower:
                    matched.append(theme)
                    break

        return matched if matched else ['自然无为']  # 默认主题

    def get_wisdom(self, theme: str, max_quotes: int = 2) -> Dict[str, Any]:
        """
        获取道德经智慧

        Args:
            theme: 主题
            max_quotes: 最大引用数

        Returns:
            包含引言和洞见的字典
        """
        theme_data = self._themes.get(theme, self._themes['自然无为'])

        return {
            'theme': theme,
            'quotes': theme_data['quotes'][:max_quotes],
            'insights': theme_data['insights'],
            'application': self._generate_application(theme),
        }

    def _generate_application(self, theme: str) -> str:
        """生成应用建议"""
        applications = {
            '自然无为': '在制定计划时，考虑事物发展的自然规律，给足够的时间和空间。',
            '柔弱胜刚强': '面对竞争时，考虑以柔克刚的策略，而非直接对抗。',
            '知足不争': '评估目标时，回顾是否与核心价值一致，避免盲目扩张。',
            '清静治国': '领导团队时，保持内心的稳定，不过度干预，给团队自主空间。',
            '上善若水': '处理关系时，以滋养和支持为导向，而非索取和竞争。',
            '返璞归真': '优化流程时，回归本质需求，去除不必要的复杂性。',
        }
        return applications.get(theme, '将道德经智慧应用于当前情境。')

class ZhuangziPhilosophy:
    """
    庄子哲学

    职责：
    1. 庄子主题匹配
    2. 逍遥智慧提取
    3. 情境应用
    """

    THEMES = {
        '自由逍遥': {
            'keywords': ['自由', '逍遥', '解放', '束缚', '限制'],
            'quotes': [
                '若夫乘天地之正，而御六气之辩，以游无穷者，彼且恶乎待哉！',
                '鹏之徙于南冥也，水击三千里，抟扶摇而上者九万里。',
            ],
            'insights': ['真正的自由是超越条件的限制', '格局决定视野，视野决定选择']
        },
        '处世智慧': {
            'keywords': ['处世', '与人', '交往', '处下', '谦逊'],
            'quotes': [
                '直木先伐，甘井先竭。',
                '而不自失也。',
            ],
            'insights': ['过于显露往往招致灾祸', '保持低调是一种保护']
        },
        '生命哲学': {
            'keywords': ['生命', '生死', '寿', '短命', '意义'],
            'quotes': [
                '天地与我并生，而万物与我为一。',
                '生也死之徒，死也生之始。',
            ],
            'insights': ['生命是一个整体的一部分', '接受无常是智慧的开始']
        },
        '无用之用': {
            'keywords': ['有用', '无用', '价值', '材', '不材'],
            'quotes': [
                '人皆知有用之用，而莫知无用之用也。',
                '桂可食，故伐之；漆可用，故割之。',
            ],
            'insights': ['看似无用的事物可能有隐藏的价值', '过度有用反而招致灾祸']
        },
    }

    def match_theme(self, query: str) -> List[str]:
        """根据问题匹配庄子主题"""
        query_lower = query.lower()
        matched = []

        for theme, data in self.THEMES.items():
            for keyword in data['keywords']:
                if keyword in query_lower:
                    matched.append(theme)
                    break

        return matched if matched else ['自由逍遥']

    def get_wisdom(self, theme: str) -> Dict[str, Any]:
        """获取庄子智慧"""
        theme_data = self.THEMES.get(theme, self.THEMES['自由逍遥'])

        return {
            'theme': theme,
            'quotes': theme_data['quotes'],
            'insights': theme_data['insights'],
        }
