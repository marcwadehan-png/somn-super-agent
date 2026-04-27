"""
__all__ = [
    'getrepresentative_works',
]

韦庄深化引擎 - 花间清丽与怀古伤今的智能系统
v8.2.0

核心理念:韦庄(836-910),字端己
诗歌style:清丽疏朗,怀古伤今,乱世叙事
哲学基础:花间词 + 现实主义 + 江南imagery
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 韦庄style类型(Enum):
    """韦庄诗词style分类"""
    清丽疏朗 = "清丽自然,不同于温词的浓艳"
    怀古伤今 = "怀古伤今,六朝如梦"
    乱世叙事 = "描写战乱,长篇叙事"
    江南词风 = "描写江南,风光清丽"
    婉约细腻 = "情感细腻,含蓄蕴藉"

class 韦庄意象类型(Enum):
    """韦庄常见imagery"""
    江南 = "江南:最美的故乡"
    春水 = "春水:碧于天的江南"
    画船 = "画船:江南生活"
    台城柳 = "台城柳:六朝旧梦"
    月色美人 = "月色:江南月夜"
    六朝 = "六朝:历史的感慨"

@dataclass
class 韦庄诗歌characteristics:
    """韦庄诗文核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 韦庄深化引擎:
    """韦庄诗文深化分析引擎 v8.2.0"""

    VERSION = "v8.2.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 韦庄诗歌characteristics:
        return 韦庄诗歌characteristics(
            style=[
                "清丽疏朗:不同于温词的浓艳",
                "怀古伤今:以古讽今,六朝如梦",
                "乱世叙事:描写黄巢起义的长篇",
                "江南词风:描写江南风光,清丽自然",
                "情感细腻:离别相思,含蓄蕴藉"
            ],
            imagery=[
                "江南imagery:最美的故乡",
                "春水画船:江南生活图景",
                "台城柳:历史变迁的见证",
                "月色美人:江南月夜的美好"
            ],
            修辞=[
                "以景衬情:借江南美景衬故国之思",
                "怀古讽今:借六朝旧事讽当世",
                "今昔对比:今昔对照,感慨深沉",
                "白描手法:语言质朴,意境清远"
            ],
            情感=[
                "怀古之情:对六朝兴亡的感慨",
                "故国之思:对唐朝衰落的忧虑",
                "江南之美:对江南风光的赞美",
                "离别相思:游子思归之情"
            ],
            语言="清丽疏朗,自然流畅,情景交融"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "菩萨蛮": {
                "原文": "人人尽说江南好,游人只合江南老.春水碧于天,画船听雨眠.",
                "类型": "词",
                "style": "江南词风",
                "imagery": "春水,画船,江南",
                "情感": "江南赞美",
                "赏析": "描写江南风光的经典之作"
            },
            "台城": {
                "原文": "江雨霏霏江草齐,六朝如梦鸟空啼.无情最是台城柳,依旧烟笼十里堤.",
                "类型": "诗",
                "style": "怀古伤今",
                "imagery": "江雨,江草,台城柳",
                "情感": "怀古伤今",
                "赏析": "怀古诗的绝唱,无情最是台城柳"
            },
            "秦妇吟": {
                "原文": "中和癸卯春三月,洛阳城外花如雪.",
                "类型": "诗",
                "style": "乱世叙事",
                "imagery": "洛阳,花,战乱",
                "情感": "乱世悲鸣",
                "赏析": "长篇叙事诗,与<长恨歌><琵琶行>并称"
            },
            "思帝乡": {
                "原文": "春日游,杏花吹满头.陌上谁家年少足风流.",
                "类型": "词",
                "style": "清丽疏朗",
                "imagery": "杏花,春风,少年",
                "情感": "少女怀春",
                "赏析": "清新自然,情感真挚"
            },
            "女冠子": {
                "原文": "四月十七,正是去年今日.别君时.忍泪佯低面,含羞半敛眉.",
                "类型": "词",
                "style": "婉约细腻",
                "imagery": "含羞,敛眉,忍泪",
                "情感": "离别相思",
                "赏析": "描写离别,含蓄细腻"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "怀古绝唱": "无情最是台城柳,依旧烟笼十里堤",
            "江南最美": "春水碧于天,画船听雨眠",
            "乱世悲歌": "秦妇吟秀才,记述黄巢起义",
            "清丽自然": "韦词清丽,不同于温词的浓艳",
            "以古讽今": "六朝如梦鸟空啼,感慨深沉"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "怀古智慧": "借古讽今,以历史映照现实",
            "清丽词风": "韦词清丽疏朗,开创不同于温词的新风",
            "现实关怀": "长篇叙事诗记录乱世,文学的现实主义精神",
            "江南之美": "韦庄对江南的描写,展现了理想家园的美好",
            "情感细腻": "离别相思的描写,含蓄而动人"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的韦庄style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["江南", "春水", "画船", "听雨"]):
            score += 4
            matched_styles.append("江南词风")
            matched_images.append("江南imagery")
        if any(word in text for word in ["台城", "六朝", "如梦", "无情"]):
            score += 4
            matched_styles.append("怀古伤今")
            matched_images.append("历史imagery")
        if any(word in text for word in ["秦妇", "洛阳", "花如雪"]):
            score += 3
            matched_styles.append("乱世叙事")
        if any(word in text for word in ["忍泪", "含羞", "半敛眉"]):
            score += 3
            matched_styles.append("婉约细腻")
        if any(word in text for word in ["春日游", "杏花"]):
            score += 2
            matched_styles.append("清丽疏朗")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "韦庄style浓郁" if score >= 5 else "略有韦庄style" if score >= 3 else "不具韦庄style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get韦庄representative_works"""
        if style:
            return [
                {**poem, "title": title}
                for title, poem in self.经典famous_poems.items()
                if poem.get("style") == style
            ]
        return [
            {**poem, "title": title}
            for title, poem in self.经典famous_poems.items()
        ]

    def get核心spiritual_insight(self) -> Dict[str, str]:
        """get韦庄核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get韦庄的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get韦庄诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get韦庄生平摘要"""
        return {
            "字": "端己",
            "生卒": "836年-910年",
            "籍贯": "京兆杜陵(今陕西西安)",
            "身份": "poet,poet,前蜀宰相",
            "并称": "与温庭筠并称'温韦'",
            "地位": "花间词派重要代表,<秦妇吟>与<长恨歌><琵琶行>并称"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
