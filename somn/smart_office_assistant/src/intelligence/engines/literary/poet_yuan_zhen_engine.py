"""
__all__ = [
    'getrepresentative_works',
]

元稹深化引擎 - 深情悼亡与新乐府的缠绵智能系统
v1.0.0

核心理念:元稹(779-831),字微之
诗歌style:情深意切,艳情缠绵,通俗易懂
哲学基础:新乐府运动 + 儒家济世 + 悼亡真情
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 元稹style类型(Enum):
    """元稹诗歌style分类"""
    悼亡深情 = "悼念亡妻,情真意切"
    艳情缠绵 = "曾经沧海难为水,除却巫山不是云"
    新乐府 = "文章合为时而著,歌诗合为事而作"
    排律精工 = "连昌宫词,长篇排律"
    通俗易懂 = "语言通俗,老妪能解"

class 元稹意象类型(Enum):
    """元稹常见imagery"""
    沧海巫山 = "沧海巫山:至深爱情的象征"
    莺莺传 = "莺莺传:唐传奇famous_poems"
    离思 = "离思五首:悼亡诗巅峰"
    菊花 = "菊花:清高品格的追求"
    连昌宫 = "连昌宫:历史兴亡之叹"

@dataclass
class 元稹诗歌characteristics:
    """元稹诗歌核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 元稹深化引擎:
    """元稹诗歌深化分析引擎 v1.0.0"""

    VERSION = "v1.0.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 元稹诗歌characteristics:
        return 元稹诗歌characteristics(
            style=[
                "悼亡深情:<遣悲怀>情真意切",
                "艳情缠绵:<离思>五首缠绵悱恻",
                "新乐府运动:与白居易共同倡导",
                "排律精工:长篇叙事结构严谨"
            ],
            imagery=[
                "沧海imagery:最深爱情的象征",
                "巫山imagery:其他一切都不算什么",
                "菊花imagery:清高品格的象征",
                "连昌宫imagery:历史兴亡的感叹"
            ],
            修辞=[
                "比喻绝唱:曾经沧海难为水",
                "对比手法:富贵与贫贱的对比",
                "细节描写:顾我无衣搜荩箧",
                "借物喻理:以菊花喻品格"
            ],
            情感=[
                "悼亡真情:对亡妻韦丛的深情",
                "爱情专一:取次花丛懒回顾",
                "济世情怀:新乐府运动的主张",
                "历史感慨:连昌宫的历史兴亡"
            ],
            语言="通俗易懂,情深意切,缠绵悱恻"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "离思五首(其四)": {
                "原文": "曾经沧海难为水,除却巫山不是云.取次花丛懒回顾,半缘修道半缘君.",
                "类型": "诗",
                "style": "艳情缠绵",
                "imagery": "沧海,巫山",
                "情感": "悼念亡妻",
                "赏析": "千古第一情诗"
            },
            "遣悲怀三首": {
                "原文": "顾我无衣搜荩箧,泥他沽酒拔金钗.",
                "类型": "诗",
                "style": "悼亡深情",
                "imagery": "荩箧,金钗",
                "情感": "悼念亡妻",
                "赏析": "回忆与妻子共患难的往事,情真意切"
            },
            "菊花": {
                "原文": "不是花中偏爱菊,此花开尽更无花.",
                "类型": "诗",
                "style": "通俗易懂",
                "imagery": "菊花",
                "情感": "品格追求",
                "赏析": "以菊花喻坚贞品格"
            },
            "连昌宫词": {
                "原文": "连昌宫中满宫竹,岁久无人森似束.",
                "类型": "排律",
                "style": "排律精工",
                "imagery": "连昌宫",
                "情感": "历史兴亡",
                "赏析": "与白居易<长恨歌>媲美"
            },
            "莺莺传": {
                "原文": "待月西厢下,迎风户半开.",
                "类型": "传奇",
                "style": "艳情缠绵",
                "imagery": "西厢",
                "情感": "爱情故事",
                "赏析": "唐传奇famous_poems,影响<西厢记>"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "至爱深情": "曾经沧海难为水,除却巫山不是云",
            "悼亡真情": "诚知此恨人人有,贫贱夫妻百事哀",
            "新乐府主张": "文章合为时而著,歌诗合为事而作",
            "品格追求": "不是花中偏爱菊,此花开尽更无花",
            "深情专一": "取次花丛懒回顾,半缘修道半缘君"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "爱情专一": "真正的爱情具有排他性,见过最好的一切便再难将就",
            "珍惜当下": "贫贱夫妻的患难真情最珍贵",
            "新乐府精神": "文学应当回应现实,关注民生疾苦",
            "品格追求": "像菊花一样,在百花凋谢后独自开放"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的元稹style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["沧海", "巫山", "难为水"]):
            score += 4
            matched_styles.append("艳情缠绵")
            matched_images.append("沧海巫山")
        if any(word in text for word in ["悼亡", "贫贱", "百事哀", "遣悲怀"]):
            score += 3
            matched_styles.append("悼亡深情")
        if any(word in text for word in ["菊花", "偏爱", "更无花"]):
            score += 3
            matched_images.append("菊花imagery")
        if any(word in text for word in ["懒回顾", "修道", "半缘君"]):
            score += 2
            matched_styles.append("深情专一")
        if any(word in text for word in ["连昌宫", "宫词", "长篇"]):
            score += 2
            matched_images.append("历史imagery")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "元稹style浓郁" if score >= 5 else "略有元稹style" if score >= 3 else "不具元稹style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get元稹representative_works"""
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
        """get元稹核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get元稹的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get元稹诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get元稹生平摘要"""
        return {
            "字": "微之",
            "号": "威明",
            "生卒": "779年-831年",
            "籍贯": "河南洛阳",
            "身份": "poet,文学家,政治家",
            "并称": "与白居易并称'元白'",
            "地位": "新乐府运动倡导者,悼亡诗巅峰"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
