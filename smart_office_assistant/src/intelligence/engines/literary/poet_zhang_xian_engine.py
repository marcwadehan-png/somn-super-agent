"""
__all__ = [
    'getrepresentative_works',
]

张先深化引擎 - 善写影与婉约清隽的智能系统
v8.2.0

核心理念:张先(990-1078),字子野
诗歌style:婉约清隽,善写影,情景交融,含蓄蕴藉
哲学基础:慢词发展 + 雅俗fusion + 词的文人化
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 张先style类型(Enum):
    """张先词style分类"""
    工于写影 = "以影为审美对象,意境优美"
    情景交融 = "借景抒情,意境幽深"
    含蓄蕴藉 = "意在言外,含蓄婉转"
    慢词推进 = "创制慢词,推进词体发展"
    雅俗fusion = "将俗曲提升到文人词的高度"

class 张先意象类型(Enum):
    """张先常见imagery"""
    月 = "月:云破月来花弄影"
    花影 = "花影:花影摇曳之美"
    秋千影 = "秋千影:以影写人"
    双丝网 = "双丝网:情网之喻"
    斜月 = "斜月:帘栊之景"
    并禽 = "并禽:双宿双飞"

@dataclass
class 张先诗歌characteristics:
    """张先词核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 张先深化引擎:
    """张先词深化分析引擎 v8.2.0"""

    VERSION = "6.2.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 张先诗歌characteristics:
        return 张先诗歌characteristics(
            style=[
                "工于写影:以影为审美对象,意境优美",
                "情景交融:借景抒情,意境幽深",
                "含蓄蕴藉:意在言外,不直说情",
                "慢词推进:创制慢词,推进词体发展"
            ],
            imagery=[
                "花影imagery:云破月来花弄影的优美",
                "秋千影:以影写人,含蓄婉转",
                "双丝网:情网之喻,情深意切",
                "斜月帘栊:闺阁的清幽"
            ],
            修辞=[
                "以影写人:以影的朦胧写人的情感",
                "情景交融:借景物抒发内心",
                "以物喻情:以双丝网喻情网",
                "以小见大:从细微处见深情"
            ],
            情感=[
                "离别相思:与心上人分离的痛苦",
                "伤春惜时:对春光流逝的感叹",
                "含蓄婉约:欲说还休的深情",
                "时光流逝:对年华老去的感慨"
            ],
            语言="婉约清隽,含蓄蕴藉,以影传情"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "天仙子": {
                "原文": "水调数声持酒听,午醉醒来愁未醒.送春春去几时回?临晚镜,伤流景,往事悠悠空记省.沙上并禽池上暝,云破月来花弄影.重重帘幕密遮灯,风不定,人初静,明日落红应满径.",
                "类型": "词",
                "style": "工于写影",
                "imagery": "云破月来花弄影",
                "情感": "伤春惜时",
                "赏析": "云破月来花弄影--千古名句,张三影之首"
            },
            "青门引": {
                "原文": "乍暖还轻冷,风雨晚来方定.庭轩寂寞近清明,残花中酒,又是去年病.楼头画角风吹醒,入夜重门静.那堪更被明月,隔墙送过秋千影.",
                "类型": "词",
                "style": "含蓄蕴藉",
                "imagery": "秋千影,明月",
                "情感": "伤春离别",
                "赏析": "隔墙送过秋千影--张三影之一"
            },
            "一丛花": {
                "原文": "伤高怀远几时穷?无物似情浓.离愁正引千丝乱,更南陌,飞絮蒙蒙.嘶骑渐遥,征尘不断,何处认郎踪?双鸳池沼水溶溶,南北小桡通.梯横画阁黄昏后,又还是,斜月帘栊.沉恨细思,不如桃杏,犹解嫁东风.",
                "类型": "词",
                "style": "情景交融",
                "imagery": "双鸳,斜月,飞絮",
                "情感": "离别相思",
                "赏析": "不如桃杏,犹解嫁东风--以物衬人,情深意切"
            },
            "千秋岁": {
                "原文": "数声鹈鴂,又报芳菲歇.惜春更把残红折,雨轻风色暴,梅子青时节.永丰柳,无人尽日花飞雪.莫把幺弦拨,怨极弦能说.天不老,情难绝,心似双丝网,中有千千结.夜过也,东窗未白孤灯灭.",
                "类型": "词",
                "style": "雅俗fusion",
                "imagery": "双丝网,幺弦",
                "情感": "情深意切",
                "赏析": "心似双丝网,中有千千结--情词名句"
            },
            "醉垂鞭": {
                "原文": "双蝶绣罗裙,东池宴,初相见.朱粉不深匀,闲花淡淡春.细看诸处好,人人道,柳腰身.昨日乱山昏,来时衣上云.",
                "类型": "词",
                "style": "含蓄蕴藉",
                "imagery": "双蝶,罗裙,柳腰",
                "情感": "美人描写",
                "赏析": "闲花淡淡春,以淡写浓,别有风致"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "张三影": "云破月来花弄影--词中名句",
            "三影典故": "帘压卷花影,堕絮轻无影--张三影",
            "情网之喻": "心似双丝网,中有千千结",
            "以影写人": "隔墙送过秋千影--张三影之一",
            "以物衬人": "不如桃杏,犹解嫁东风"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "以影写情": "张先善于以影的朦胧写情感的缱绻",
            "imagery创新": "以影为审美对象,开拓词的imagery领域",
            "含蓄之美": "含蓄蕴藉,意在言外是中国诗歌的传统",
            "慢词贡献": "张先推进慢词发展,为苏轼,周邦彦奠基",
            "情深意切": "心似双丝网,中有千千结--用比喻深化情感"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的张先style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["云破月来", "花弄影", "弄影"]):
            score += 5
            matched_styles.append("工于写影")
            matched_images.append("花影imagery")
        if any(word in text for word in ["双丝网", "千千结", "情难绝"]):
            score += 4
            matched_styles.append("情景交融")
            matched_images.append("情网imagery")
        if any(word in text for word in ["秋千影", "帘压卷", "花影"]):
            score += 4
            matched_styles.append("含蓄蕴藉")
        if any(word in text for word in ["送春", "伤流景", "落红"]):
            score += 3
            matched_styles.append("伤春惜时")
        if any(word in text for word in ["桃杏", "嫁东风"]):
            score += 2
            matched_styles.append("情景交融")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "张先style浓郁" if score >= 5 else "略有张先style" if score >= 3 else "不具张先style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get张先representative_works"""
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
        """get张先核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get张先的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get张先词完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get张先生平摘要"""
        return {
            "字": "子野",
            "生卒": "990年-1078年",
            "籍贯": "乌程(今浙江湖州)",
            "身份": "poet,婉约派代表人物",
            "并称": "与晏殊,柳永,苏轼等各代poet交往",
            "地位": "慢词发展的重要推动者,'张三影'--词中好影者"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
