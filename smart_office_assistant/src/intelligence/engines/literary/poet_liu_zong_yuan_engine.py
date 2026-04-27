"""
__all__ = [
    'getrepresentative_works',
]

柳宗元深化引擎 - 山水游记与唯物思想的清峭智能系统
v8.2.0

核心理念:柳宗元(773-819),字子厚
诗歌style:简古幽峭,情景交融,冷峻深情
哲学基础:唯物主义 + 天人不相预 + 民本思想
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 柳宗元style类型(Enum):
    """柳宗元诗文style分类"""
    冷峭幽峭 = "意境清冷,幽峭孤独"
    情景交融 = "借景抒情,意在言外"
    寓言文学 = "借物喻理,短小精悍"
    唯物思想 = "天人不相预,否定天命"
    民本精神 = "关心民瘼,批判苛政"
    贬谪孤独 = "永州十年,孤独坚守"

class 柳宗元意象类型(Enum):
    """柳宗元常见imagery"""
    寒江 = "寒江:孤独坚守的象征"
    孤舟 = "孤舟:贬谪生涯的写照"
    蓑笠翁 = "蓑笠翁:傲世独立的imagery"
    永州 = "永州:十年贬谪之地"
    封建论 = "封建论:郡县制的主张"
    小石潭 = "小石潭:游记文学的典范"

@dataclass
class 柳宗元诗歌characteristics:
    """柳宗元诗文核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 柳宗元深化引擎:
    """柳宗元诗文深化分析引擎 v8.2.0"""

    VERSION = "v8.2.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 柳宗元诗歌characteristics:
        return 柳宗元诗歌characteristics(
            style=[
                "冷峭幽峭:诗歌意境清冷幽寂",
                "情景交融:借山水抒发抑郁之情",
                "简古清朗:语言简洁,意境清远",
                "寓言文学:借动物故事讽刺现实"
            ],
            imagery=[
                "寒江imagery:孤独坚守的精神象征",
                "孤舟imagery:贬谪生涯的写照",
                "蓑笠翁imagery:傲世独立的人格",
                "小石潭imagery:游记文学的典范"
            ],
            修辞=[
                "寓言手法:借动物喻社会现实",
                "情景交融:借山水抒发内心抑郁",
                "以小见大:从小事物见大道理",
                "冷峭imagery:清冷幽寂的意境营造"
            ],
            情感=[
                "贬谪之痛:十年永州的孤独与压抑",
                "傲世独立:世人皆浊我独清的精神",
                "民本关怀:批判苛政,同情百姓",
                "哲学思考:天人不相预的唯物思想"
            ],
            语言="简古清朗,不事雕琢,意境清远"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "江雪": {
                "原文": "千山鸟飞绝,万径人踪灭.孤舟蓑笠翁,独钓寒江雪.",
                "类型": "诗",
                "style": "冷峭幽峭",
                "imagery": "寒江,孤舟,蓑笠翁",
                "情感": "孤独傲世",
                "赏析": "唐人五绝压卷之作,'独钓寒江雪'意境极高"
            },
            "捕蛇者说": {
                "原文": "永州之野产异蛇...孔子曰:'苛政猛于虎也.'",
                "类型": "散文",
                "style": "民本精神",
                "imagery": "毒蛇,苛政",
                "情感": "批判苛政",
                "赏析": "揭露苛政害民的本质"
            },
            "小石潭记": {
                "原文": "潭中鱼可百许头,皆若空游无所依.",
                "类型": "游记",
                "style": "情景交融",
                "imagery": "小石潭,游鱼",
                "情感": "贬谪之痛",
                "赏析": "永州八记代表,情景交融famous_poems"
            },
            "封建论": {
                "原文": "失在于政,不在于制.",
                "类型": "论说文",
                "style": "唯物思想",
                "imagery": "郡县,分封",
                "情感": "政治主张",
                "赏析": "肯定郡县制,批判分封制"
            },
            "黔之驴": {
                "原文": "黔无驴,有好事者船载以入.",
                "类型": "寓言",
                "style": "寓言文学",
                "imagery": "驴,虎",
                "情感": "讽刺批判",
                "赏析": "三戒之一,篇幅短小,寓意深刻"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "傲世独立": "千山鸟飞绝,万径人踪灭",
            "贬谪坚守": "孤舟蓑笠翁,独钓寒江雪",
            "批判苛政": "苛政猛于虎也",
            "唯物思想": "天人不相预,自然与人事无关",
            "以小见大": "借寓言故事说明大道理",
            "情景交融": "心凝形释,与万化冥合"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "独立精神": "在困境中保持独立人格,不随波逐流",
            "民本思想": "批判社会不公,关注底层疾苦",
            "唯物哲学": "用现实原因解释社会现象,不信天命",
            "以小见大": "从具体事物入手说明抽象道理",
            "游记创作": "在自然山水中寻求精神寄托与心灵超脱"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的柳宗元style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["千山", "鸟飞绝", "万径", "孤舟", "寒江", "蓑笠"]):
            score += 4
            matched_styles.append("冷峭幽峭")
            matched_images.append("寒江imagery")
        if any(word in text for word in ["苛政", "猛于虎", "捕蛇"]):
            score += 3
            matched_styles.append("民本精神")
        if any(word in text for word in ["小石潭", "潭中鱼", "永州"]):
            score += 2
            matched_images.append("山水imagery")
        if any(word in text for word in ["寓言", "驴", "虎"]):
            score += 2
            matched_styles.append("寓言文学")
        if any(word in text for word in ["封建", "郡县", "天命"]):
            score += 2
            matched_images.append("唯物思想")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "柳宗元style浓郁" if score >= 5 else "略有柳宗元style" if score >= 3 else "不具柳宗元style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get柳宗元representative_works"""
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
        """get柳宗元核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get柳宗元的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get柳宗元诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get柳宗元生平摘要"""
        return {
            "字": "子厚",
            "号": "柳河东",
            "生卒": "773年-819年",
            "籍贯": "河东解县(今山西运城)",
            "身份": "文学家,思想家,唐宋八大家之一",
            "并称": "与韩愈并称'韩柳'",
            "地位": "山水游记奠基人,寓言文学开创者"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
