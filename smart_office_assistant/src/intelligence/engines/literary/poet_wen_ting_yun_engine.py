"""
__all__ = [
    'getrepresentative_works',
]

温庭筠深化引擎 - 花间词鼻祖与绮丽婉约的智能系统
v8.2.0

核心理念:温庭筠(812-866),本名岐,字飞卿
诗歌style:词浓艳华美,诗清峭疏朗
哲学基础:花间词派开创者 + 音律精通
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 温庭筠style类型(Enum):
    """温庭筠诗词style分类"""
    浓艳香软 = "imagery浓艳,色彩华丽"
    闺情闺怨 = "描写闺阁,离别相思"
    绮丽婉约 = "语言华美,意境绮丽"
    清峭疏朗 = "诗风清峭,不同于词"
    音律精审 = "精通音律,词律娴熟"
    女子容饰 = "描写女子容貌服饰"

class 温庭筠意象类型(Enum):
    """温庭筠常见imagery"""
    闺阁 = "闺阁:绮丽生活"
    金鹧鸪 = "金鹧鸪:华美imagery"
    鬓云 = "鬓云:女子鬓发之美"
    香腮雪 = "香腮雪:容颜之美"
    小山眉 = "小山眉:眉妆之美"
    茅店月 = "茅店月:羁旅清景"
    板桥霜 = "板桥霜:早行imagery"

@dataclass
class 温庭筠诗歌characteristics:
    """温庭筠诗文核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 温庭筠深化引擎:
    """温庭筠诗文深化分析引擎 v8.2.0"""

    VERSION = "v8.2.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 温庭筠诗歌characteristics:
        return 温庭筠诗歌characteristics(
            style=[
                "浓艳华美:imagery浓艳,色彩华丽",
                "花间词祖:开创花间词派",
                "词律精审:精通音律,词律娴熟",
                "诗清峭疏朗:诗风与词风不同"
            ],
            imagery=[
                "闺阁imagery:绮丽华美的闺房",
                "金鹧鸪imagery:华美装饰",
                "鬓云imagery:女子鬓发之美",
                "茅店月imagery:羁旅清景"
            ],
            修辞=[
                "imagery叠加:不用动词,纯以imagery叠加",
                "色彩描写:运用华丽色彩",
                "细节描写:女子容貌服饰的细腻描写",
                "通感手法:视听嗅触联觉"
            ],
            情感=[
                "闺情闺怨:离别相思之情",
                "华美绮丽:宫廷贵族生活",
                "羁旅之苦:早行诗的清峭",
                "音律之美:对音乐性的追求"
            ],
            语言="浓艳华美,精雕细琢,绮丽婉约"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "菩萨蛮": {
                "原文": "小山重叠金明灭,鬓云欲度香腮雪.懒起画蛾眉,弄妆梳洗迟.",
                "类型": "词",
                "style": "浓艳香软",
                "imagery": "小山眉,鬓云,香腮雪",
                "情感": "闺情",
                "赏析": "花间词的代表作,描写女子梳妆"
            },
            "商山早行": {
                "原文": "晨起动征铎,客行悲故乡.鸡声茅店月,人迹板桥霜.",
                "类型": "诗",
                "style": "清峭疏朗",
                "imagery": "茅店月,板桥霜",
                "情感": "羁旅思乡",
                "赏析": "千古名句,imagery叠加,不用动词"
            },
            "更漏子": {
                "原文": "玉炉香,红蜡泪,偏照画堂秋思.眉翠薄,鬓云残,夜长衾枕寒.",
                "类型": "词",
                "style": "绮丽婉约",
                "imagery": "玉炉,红蜡,画堂,鬓云",
                "情感": "秋思闺怨",
                "赏析": "以景写情,意境绮丽"
            },
            "望江南": {
                "原文": "梳洗罢,独倚望江楼.过尽千帆皆不是,斜晖脉脉水悠悠.肠断白苹洲.",
                "类型": "词",
                "style": "清峭疏朗",
                "imagery": "千帆,斜晖,白苹洲",
                "情感": "思妇望归",
                "赏析": "以景结情,肠断白苹洲"
            },
            "梦江南": {
                "原文": "千万恨,恨极在天涯.山月不知心里事,水风空落眼前花.摇曳碧云斜.",
                "类型": "词",
                "style": "清峭疏朗",
                "imagery": "山月,水风,碧云",
                "情感": "闺怨",
                "赏析": "以景写情,意境清远"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "花间词祖": "词为艳科,温庭筠开一代词风",
            "imagery叠加": "鸡声茅店月,人迹板桥霜--不用动词",
            "闺情描写": "小山重叠金明灭,鬓云欲度香腮雪",
            "诗清峭峭": "商山早行与词风迥异,清峭疏朗",
            "音律精审": "精通音律,为花间词派奠基"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "ci_study开创": "温庭筠是花间词派的开创者,对词的发展影响深远",
            "imagery创新": "以imagery叠加代替叙述,创造独特意境",
            "style多样": "词与诗style迥异,展现艺术的多样性",
            "音律追求": "精通音律,对词的规范化有重要贡献",
            "闺情描写": "细腻描写女性内心世界,丰富词的表现内容"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的温庭筠style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["小山", "金明灭", "鬓云", "香腮", "蛾眉", "画眉"]):
            score += 4
            matched_styles.append("浓艳香软")
            matched_images.append("闺阁imagery")
        if any(word in text for word in ["鸡声", "茅店月", "人迹", "板桥霜"]):
            score += 4
            matched_styles.append("清峭疏朗")
            matched_images.append("羁旅imagery")
        if any(word in text for word in ["闺阁", "金鹧鸪", "红蜡", "玉炉"]):
            score += 3
            matched_styles.append("绮丽婉约")
        if any(word in text for word in ["千帆", "斜晖", "肠断"]):
            score += 2
            matched_styles.append("闺情闺怨")
        if any(word in text for word in ["更漏", "夜长", "枕寒"]):
            score += 2
            matched_images.append("秋思闺怨")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "温庭筠style浓郁" if score >= 5 else "略有温庭筠style" if score >= 3 else "不具温庭筠style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get温庭筠representative_works"""
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
        """get温庭筠核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get温庭筠的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get温庭筠诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get温庭筠生平摘要"""
        return {
            "字": "本名岐,字飞卿",
            "生卒": "812年-866年",
            "籍贯": "太原祁县(今山西祁县)",
            "身份": "poet,poet,花间词鼻祖",
            "并称": "与韦庄并称'温韦'",
            "地位": "花间词派的开创者和代表人物"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
