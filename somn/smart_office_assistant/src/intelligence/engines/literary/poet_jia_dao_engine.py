"""
__all__ = [
    'getrepresentative_works',
]

贾岛深化引擎 - 苦吟poet与推敲精神的瘦硬智能系统
v1.0.0

核心理念:贾岛(779-843),字阆仙,号诗奴
诗歌style:瘦硬幽峭,苦吟精神,清寂冷峭
哲学基础:隐逸情怀 + 孤独心境 + 推敲精神
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 贾岛style类型(Enum):
    """贾岛诗歌style分类"""
    瘦硬幽峭 = "郊寒岛瘦,诗歌幽冷苦涩"
    苦吟精神 = "两句三年得,一吟双泪流"
    推敲精神 = "僧敲月下门,一字三年炼"
    隐逸情怀 = "只在此山中,云深不知处"
    清寂冷峭 = "鸟宿池边树,僧敲月下门"

class 贾岛意象类型(Enum):
    """贾岛常见imagery"""
    推敲 = "推敲:炼字精神的象征"
    寒水瘦月 = "寒水:清寂imagery"
    僧敲月 = "僧敲月:夜晚寂静的意境"
    寻隐者 = "只在此山中:隐逸情怀"
    瘦驴 = "瘦驴:苦吟poet的写照"
    枯枝 = "枯枝:瘦硬imagery的延伸"

@dataclass
class 贾岛诗歌characteristics:
    """贾岛诗歌核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 贾岛深化引擎:
    """贾岛诗歌深化分析引擎 v1.0.0"""

    VERSION = "v1.0.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 贾岛诗歌characteristics:
        return 贾岛诗歌characteristics(
            style=[
                "瘦硬幽峭:诗歌imagery瘦硬,意境幽寂",
                "苦吟精神:两句三年得,一吟双泪流",
                "清寂冷峭:诗歌氛围清冷寂静",
                "隐逸情怀:早年出家,向往隐居"
            ],
            imagery=[
                "推敲imagery:精益求精的创作态度",
                "僧敲月imagery:夜晚寂静的意境之美",
                "隐者imagery:只在此山中,云深不知处",
                "枯寂imagery:营造清冷幽寂的诗歌境界"
            ],
            修辞=[
                "苦吟手法:反复推敲,精益求精",
                "以动衬静:鸟鸣,月敲更显寂静",
                "imagery叠加:不用动词只用名词imagery并置",
                "清冷意境:营造清寂幽冷的氛围"
            ],
            情感=[
                "科举不第:十年蹭蹬的孤独与苦涩",
                "隐逸向往:只在此山中,云深不知处",
                "精益求精:两句三年得的苦吟精神",
                "知音难觅:知音如不赏,归卧故山秋"
            ],
            语言="瘦硬幽峭,精雕细琢,每字必反复推敲"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "题李凝幽居": {
                "原文": "鸟宿池边树,僧敲月下门.",
                "类型": "诗",
                "style": "推敲精神",
                "imagery": "鸟,僧,月,门",
                "情感": "隐逸情趣",
                "赏析": "推敲典故的来源,'鸟宿池边树,僧敲月下门'"
            },
            "寻隐者不遇": {
                "原文": "只在此山中,云深不知处.",
                "类型": "诗",
                "style": "隐逸情怀",
                "imagery": "云,山,隐者",
                "情感": "隐逸向往",
                "赏析": "五绝famous_poems,以问答体写寻隐不遇"
            },
            "题诗后": {
                "原文": "两句三年得,一吟双泪流.知音如不赏,归卧故山秋.",
                "类型": "诗",
                "style": "苦吟精神",
                "imagery": "三年,双泪",
                "情感": "苦吟心声",
                "赏析": "表达苦吟精神的名作"
            },
            "剑客": {
                "原文": "十年磨一剑,霜刃未曾试.今日把示君,谁有不平事?",
                "类型": "诗",
                "style": "清寂冷峭",
                "imagery": "剑,霜刃",
                "情感": "怀才不遇",
                "赏析": "十年磨一剑成为名言"
            },
            "暮过山村": {
                "原文": "数里闻寒水,山家少四邻.怪禽啼旷野,落日恐行人.",
                "类型": "诗",
                "style": "清寂冷峭",
                "imagery": "寒水,怪禽",
                "情感": "旅途孤独",
                "赏析": "imagery叠加营造冷峭意境"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "苦吟精神": "两句三年得,一吟双泪流",
            "精益求精": "鸟宿池边树,僧敲月下门",
            "隐逸向往": "只在此山中,云深不知处",
            "怀才不遇": "十年磨一剑,霜刃未曾试",
            "知音难觅": "知音如不赏,归卧故山秋",
            "推敲典故": "推敲一词源于贾岛冲撞韩愈仪仗"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "精益求精": "创作需要反复打磨,一字千金",
            "苦吟精神": "真正的好作品需要时间和精力的投入",
            "隐逸智慧": "在喧嚣中保持内心的宁静与独立",
            "知音难得": "真正理解自己作品的人很少,不要因此放弃",
            "以动衬静": "用动态来反衬静态,会产生更强烈的效果"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的贾岛style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["敲", "推", "月下门", "鸟宿"]):
            score += 4
            matched_styles.append("推敲精神")
            matched_images.append("推敲imagery")
        if any(word in text for word in ["三年", "两句", "一吟", "双泪"]):
            score += 3
            matched_styles.append("苦吟精神")
        if any(word in text for word in ["云深", "隐者", "山中", "不知处"]):
            score += 3
            matched_styles.append("隐逸情怀")
        if any(word in text for word in ["十年", "磨一剑", "霜刃", "不平事"]):
            score += 2
            matched_images.append("剑imagery")
        if any(word in text for word in ["寒", "冷", "瘦", "枯", "孤"]):
            score += 1
            matched_styles.append("清寂冷峭")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "贾岛style浓郁" if score >= 5 else "略有贾岛style" if score >= 3 else "不具贾岛style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get贾岛representative_works"""
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
        """get贾岛核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get贾岛的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get贾岛诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get贾岛生平摘要"""
        return {
            "字": "阆仙",
            "号": "诗奴,苦吟poet",
            "生卒": "779年-843年",
            "籍贯": "范阳幽州(今河北涿州)",
            "身份": "poet,苦吟poet",
            "并称": "与孟郊并称'郊寒岛瘦'",
            "地位": "唐代苦吟poet代表,推敲典故来源"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
