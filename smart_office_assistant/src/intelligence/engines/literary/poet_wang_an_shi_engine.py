"""
__all__ = [
    'getrepresentative_works',
]

王安石深化引擎 - 峭拔劲健与政治改革的智能系统
v8.2.0

核心理念:王安石(1021-1086),字介甫,号半山
诗歌style:峭拔劲健,说理精辟,豪放与婉约兼具
哲学基础:变法改革 + 荆公新学 + 经世致用
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 王安石style类型(Enum):
    """王安石诗词style分类"""
    峭拔劲健 = "语言精炼,骨力劲健"
    说理精辟 = "以诗说理,独具一格"
    咏史怀古 = "借古讽今,感慨深沉"
    借景喻理 = "以景喻理,情景交融"
    豪放婉约 = "豪放与婉约兼具"

class 王安石意象类型(Enum):
    """王安石常见imagery"""
    春风江南 = "春风又绿江南岸"
    浮云 = "浮云:遮蔽真相的障碍"
    明月 = "明月:照我还的归思"
    澄江 = "澄江似练:金陵秋景"
    寒烟芳草 = "寒烟芳草:历史变迁"
    梅花 = "梅花:凌寒独自开"

@dataclass
class 王安石诗歌characteristics:
    """王安石诗文核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 王安石深化引擎:
    """王安石诗文深化分析引擎 v8.2.0"""

    VERSION = "6.2.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 王安石诗歌characteristics:
        return 王安石诗歌characteristics(
            style=[
                "峭拔劲健:语言精炼,骨力劲健",
                "说理精辟:以诗说理,独具一格",
                "咏史怀古:借古讽今,感慨深沉",
                "借景喻理:情景交融,富含哲理"
            ],
            imagery=[
                "春风江南:春风又绿江南岸的明丽",
                "浮云imagery:不畏浮云遮望眼",
                "澄江翠峰:金陵秋景的壮美",
                "寒烟芳草:历史变迁的见证"
            ],
            修辞=[
                "以景喻理:将哲理融入景物描写",
                "借古讽今:借历史故事讽刺当世",
                "炼字精妙:春风又绿江南岸的绿字",
                "对比手法:今昔对比,感慨深沉"
            ],
            情感=[
                "政治抱负:天变不足畏的改革精神",
                "思归之情:春风又绿江南岸,明月何时照我还",
                "历史感慨:对六朝兴亡的深沉思考",
                "高远志向:不畏浮云遮望眼,自缘身在最高层"
            ],
            语言="峭拔劲健,精炼准确,情景交融"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "泊船瓜洲": {
                "原文": "京口瓜洲一水间,钟山只隔数重山.春风又绿江南岸,明月何时照我还.",
                "类型": "诗",
                "style": "借景喻理",
                "imagery": "春风,江南岸,明月",
                "情感": "思归之情",
                "赏析": "春风又绿江南岸--炼字的典范"
            },
            "登飞来峰": {
                "原文": "飞来峰上千寻塔,闻说鸡鸣见日升.不畏浮云遮望眼,自缘身在最高层.",
                "类型": "诗",
                "style": "说理精辟",
                "imagery": "浮云,最高层",
                "情感": "高远志向",
                "赏析": "不畏浮云遮望眼,自缘身在最高层--改革者的气魄"
            },
            "桂枝香·金陵怀古": {
                "原文": "登临送目,正故国晚秋,天气初肃.千里澄江似练,翠峰如簇.征帆去棹残阳里,背西风,酒旗斜矗.彩舟云淡,星河鹭起,画图难足.",
                "类型": "词",
                "style": "咏史怀古",
                "imagery": "澄江,翠峰,斜阳",
                "情感": "历史感慨",
                "赏析": "宋词三大怀古famous_poems之一,与苏轼<念奴娇>并称"
            },
            "梅花": {
                "原文": "墙角数枝梅,凌寒独自开.遥知不是雪,为有暗香来.",
                "类型": "诗",
                "style": "峭拔劲健",
                "imagery": "梅花,暗香",
                "情感": "高洁品格",
                "赏析": "以梅花喻高洁品格,晚年心境的写照"
            },
            "明妃曲": {
                "原文": "明妃初出汉宫时,泪湿春风鬓脚垂.低回顾影无颜色,尚得君王不自持.",
                "类型": "诗",
                "style": "咏史怀古",
                "imagery": "明妃,春风",
                "情感": "历史感慨",
                "赏析": "为王昭君翻案,翻案文章的典范"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "改革精神": "天变不足畏,祖宗不足法,人言不足恤",
            "高远志向": "不畏浮云遮望眼,自缘身在最高层",
            "炼字典范": "春风又绿江南岸--绿字点睛",
            "金陵怀古": "千里澄江似练,翠峰如簇",
            "经世致用": "明道致用,学以致用"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "改革勇气": "面对积弊,勇于提出并实施改革方案",
            "高远视野": "不畏浮云遮望眼,自缘身在最高层--站得高看得远",
            "炼字精神": "春风又绿江南岸--精益求精的创作态度",
            "经世致用": "学问要为现实服务,注重实践效果",
            "历史智慧": "以史为鉴,可以知兴替"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的王安石style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["春风又绿", "江南岸"]):
            score += 5
            matched_styles.append("借景喻理")
            matched_images.append("春风imagery")
        if any(word in text for word in ["不畏浮云", "最高层", "遮望眼"]):
            score += 4
            matched_styles.append("说理精辟")
            matched_images.append("浮云imagery")
        if any(word in text for word in ["澄江", "翠峰", "金陵", "怀古"]):
            score += 4
            matched_styles.append("咏史怀古")
        if any(word in text for word in ["天变", "祖宗", "不足畏", "改革"]):
            score += 3
            matched_styles.append("峭拔劲健")
        if any(word in text for word in ["梅花", "凌寒", "暗香"]):
            score += 3
            matched_styles.append("峭拔劲健")
            matched_images.append("梅花imagery")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "王安石style浓郁" if score >= 5 else "略有王安石style" if score >= 3 else "不具王安石style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get王安石representative_works"""
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
        """get王安石核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get王安石的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get王安石诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get王安石生平摘要"""
        return {
            "字": "介甫,号半山",
            "谥号": "文",
            "生卒": "1021年-1086年",
            "籍贯": "临川(今江西抚州)",
            "身份": "政治家,思想家,文学家",
            "并称": "与韩愈,柳宗元,欧阳修,苏洵,苏轼,苏辙,曾巩并称'唐宋八大家'",
            "地位": "唐宋八大家之一,北宋著名改革家"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
