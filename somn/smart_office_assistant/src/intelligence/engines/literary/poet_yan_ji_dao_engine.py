"""
__all__ = [
    'getrepresentative_works',
]

晏几道深化引擎 - 深婉哀怨与梦魂追寻的智能系统
v1.0.0

核心理念:晏几道(1038-1110),字叔原,号小山
诗歌style:深婉哀怨,梦魂追寻,清新俊逸,情真意深
哲学基础:北宋婉约词 + 纯真情感 + 小山词独特魅力
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 晏几道style类型(Enum):
    """晏几道词style分类"""
    深婉哀怨 = "凄婉动人,情感深沉"
    梦魂追寻 = "以梦写情,跨越时空"
    清新俊逸 = "语言清新,意境优美"
    情真意深 = "情感真挚,意浓情深"
    离别相思 = "离别之苦,相思之痛"

class 晏几道意象类型(Enum):
    """晏几道常见imagery"""
    梦 = "梦:追忆与思念的载体"
    杨柳楼心月 = "杨柳楼心月:歌舞之夜的美好"
    桃花扇底风 = "桃花扇底风:尽情欢乐"
    银缸 = "银缸:重逢时的端详"
    兰舟 = "兰舟:离别的imagery"
    江南烟水 = "江南烟水:思念中的江南"

@dataclass
class 晏几道诗歌characteristics:
    """晏几道词核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 晏几道深化引擎:
    """晏几道词深化分析引擎 v1.0.0"""

    VERSION = "v1.0.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 晏几道诗歌characteristics:
        return 晏几道诗歌characteristics(
            style=[
                "深婉哀怨:凄婉动人,情感深沉",
                "梦魂追寻:以梦写情,跨越时空",
                "清新俊逸:语言清新,意境优美",
                "情真意深:情感真挚,不作虚饰"
            ],
            imagery=[
                "梦imagery:梦中相见的深情",
                "杨柳楼心月:昔日欢乐的追忆",
                "银缸imagery:重逢时的端详",
                "江南烟水:思念中的imagery"
            ],
            修辞=[
                "今昔交织:今昔对比,往事如梦",
                "以梦写情:梦中相见,超越时空",
                "翻进一层:疑真疑幻,跌宕有致",
                "以景结情:以景写情,余韵悠长"
            ],
            情感=[
                "离别之痛:与心上人分离的痛苦",
                "梦中相思:几回魂梦与君同的深情",
                "重逢之喜:犹恐相逢是梦中的复杂心情",
                "家道中落:从相府公子到晚年潦倒"
            ],
            语言="清新俊逸,意浓情深,凄婉动人"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "鹧鸪天": {
                "原文": "彩袖殷勤捧玉钟,当年拚却醉颜红.舞低杨柳楼心月,歌尽桃花扇底风.从别后,忆相逢,几回魂梦与君同.今宵剩把银缸照,犹恐相逢是梦中.",
                "类型": "词",
                "style": "深婉哀怨",
                "imagery": "银缸,杨柳楼心月,桃花扇底风",
                "情感": "重逢深情",
                "赏析": "千古famous_poems,今宵剩把银缸照,犹恐相逢是梦中"
            },
            "鹧鸪天": {
                "原文": "醉拍春衫惜旧香,天将离恨恼疏狂.年年陌上生秋草,日日楼中到夕阳.云渺渺,水茫茫,征人归路许多长.相思本是无凭语,莫向花笺费泪行.",
                "类型": "词",
                "style": "清新俊逸",
                "imagery": "云渺渺,水茫茫,夕阳",
                "情感": "离别相思",
                "赏析": "清新俊逸,相思无凭语的惆怅"
            },
            "清平乐": {
                "原文": "留人不住,醉解兰舟去.一棹碧涛春水路,过尽晓莺啼处.渡头杨柳青青,枝枝叶叶离情.此后锦书休寄,画楼云雨无凭.",
                "类型": "词",
                "style": "情真意深",
                "imagery": "兰舟,杨柳,锦书",
                "情感": "离别之痛",
                "赏析": "留人不住的深情与无奈"
            },
            "阮郎归": {
                "原文": "天边金掌露成霜,云随雁字长.绿杯红袖趁重阳,人情似故乡.兰佩紫,菊簪黄,殷勤理旧狂.欲将沉醉换悲凉,清歌莫断肠.",
                "类型": "词",
                "style": "深婉哀怨",
                "imagery": "金掌,雁字,菊黄",
                "情感": "重阳怀人",
                "赏析": "欲将沉醉换悲凉,以酒浇愁"
            },
            "蝶恋花": {
                "原文": "梦入江南烟水路,行尽江南,不与离人遇.睡里消得无春晚,何处寻芳寻此去.旅食悲欢异,空留此,向谁倚醉醒时风雨.",
                "类型": "词",
                "style": "梦魂追寻",
                "imagery": "江南烟水,离人",
                "情感": "梦中寻觅",
                "赏析": "梦入江南烟水路,不与离人遇的深情"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "重逢深情": "今宵剩把银缸照,犹恐相逢是梦中",
            "梦中相思": "几回魂梦与君同",
            "歌舞之美": "舞低杨柳楼心月,歌尽桃花扇底风",
            "小山词魂": "情真,意深,语清,境美",
            "离别之痛": "留人不住,醉解兰舟去"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "纯真情感": "小山词情真意深,不作虚饰",
            "梦魂imagery": "以梦写情,跨越时空,深化词的抒情功能",
            "以情动人": "小山词以情胜,不以辞胜",
            "傲骨铮铮": "晚年不趋炎附势,宁可清贫自守",
            "艺术升华": "将人生悲欢化为艺术的永恒"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的晏几道style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["银缸", "相逢是梦", "梦中"]):
            score += 4
            matched_styles.append("深婉哀怨")
            matched_images.append("重逢imagery")
        if any(word in text for word in ["魂梦", "梦中", "梦入"]):
            score += 4
            matched_styles.append("梦魂追寻")
            matched_images.append("梦imagery")
        if any(word in text for word in ["杨柳楼心月", "桃花扇底风", "彩袖"]):
            score += 4
            matched_styles.append("清新俊逸")
            matched_images.append("昔日imagery")
        if any(word in text for word in ["兰舟", "留人不住", "离情"]):
            score += 3
            matched_styles.append("离别相思")
        if any(word in text for word in ["云渺渺", "水茫茫", "相思"]):
            score += 2
            matched_styles.append("情真意深")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "晏几道style浓郁" if score >= 5 else "略有晏几道style" if score >= 3 else "不具晏几道style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get晏几道representative_works"""
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
        """get晏几道核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get晏几道的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get晏几道词完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get晏几道生平摘要"""
        return {
            "字": "叔原,号小山",
            "生卒": "1038年-1110年",
            "籍贯": "临川(今江西抚州)",
            "身份": "poet,婉约派代表人物",
            "并称": "与父亲晏殊并称'大小晏'",
            "地位": "北宋婉约词大家,深婉哀怨词的代表"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
