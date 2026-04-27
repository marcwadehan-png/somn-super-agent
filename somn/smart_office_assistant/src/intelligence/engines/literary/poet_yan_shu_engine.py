"""
__all__ = [
    'getrepresentative_works',
]

晏殊深化引擎 - 珠圆玉润与富贵闲适的智能系统
v1.0.0

核心理念:晏殊(991-1055),字同叔
诗歌style:富贵闲适,典雅蕴藉,珠圆玉润,淡淡感伤
哲学基础:北宋婉约词 + 富贵气象 + 圆融平静
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 晏殊style类型(Enum):
    """晏殊词style分类"""
    富贵闲适 = "词中多富贵气象,雍容华贵"
    典雅蕴藉 = "语言华美,imagery精美,意在言外"
    珠圆玉润 = "语言华美,珠圆玉润"
    感伤惆怅 = "人生短暂的感慨,淡淡忧伤"
    意在言外 = "含蓄蕴藉,意在言外"
    理性色彩 = "富贵气象中的理性观察"

class 晏殊意象类型(Enum):
    """晏殊常见imagery"""
    落花 = "落花:时光流逝的象征"
    归燕 = "归燕:新生事物不可阻挡"
    西风 = "西风:秋天的象征"
    碧树 = "碧树:相思的imagery"
    明月 = "明月:思乡怀人"
    独徘徊 = "独徘徊:孤独的imagery"

@dataclass
class 晏殊诗歌characteristics:
    """晏殊词核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 晏殊深化引擎:
    """晏殊词深化分析引擎 v1.0.0"""

    VERSION = "v1.0.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 晏殊诗歌characteristics:
        return 晏殊诗歌characteristics(
            style=[
                "富贵闲适:词中多富贵气象",
                "典雅蕴藉:语言华美,意在言外",
                "珠圆玉润:语言精美,音韵和谐",
                "感伤惆怅:淡淡的忧伤,时光流逝的感慨"
            ],
            imagery=[
                "落花imagery:无可奈何花落去的感叹",
                "归燕imagery:似曾相识燕归来的新生",
                "西风碧树imagery:离别相思的意境",
                "明月imagery:思乡怀人"
            ],
            修辞=[
                "以景衬情:借自然景物抒发感慨",
                "今昔对比:去年与今日的对照",
                "哲理升华:从个别到一般的升华",
                "含蓄蕴藉:意在言外,不直说情"
            ],
            情感=[
                "感伤惆怅:时光流逝的淡淡忧伤",
                "富贵闲适:太平宰相的雍容",
                "离别相思:对亲友的思念",
                "理性观察:对人生的冷静观察"
            ],
            语言="珠圆玉润,典雅蕴藉,闲雅而有情思"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "浣溪沙": {
                "原文": "一曲新词酒一杯,去年天气旧亭台.夕阳西下几时回?无可奈何花落去,似曾相识燕归来.小园香径独徘徊.",
                "类型": "词",
                "style": "感伤惆怅",
                "imagery": "落花,归燕,独徘徊",
                "情感": "时光流逝",
                "赏析": "无可奈何花落去,似曾相识燕归来--千古名句"
            },
            "蝶恋花": {
                "原文": "槛菊愁烟兰泣露,罗幕轻寒,燕子双飞去.明月不谙离恨苦,斜光到晓穿朱户.昨夜西风凋碧树,独上高楼,望尽天涯路.",
                "类型": "词",
                "style": "典雅蕴藉",
                "imagery": "西风,碧树,明月",
                "情感": "离别相思",
                "赏析": "昨夜西风凋碧树,独上高楼,望尽天涯路--王国维第一境界"
            },
            "清平乐": {
                "原文": "红笺小字,说尽平生意.鸿雁在云鱼在水,惆怅此情难寄.斜阳独倚西楼,遥山恰对帘钩.人面不知何处,绿波依旧东流.",
                "类型": "词",
                "style": "珠圆玉润",
                "imagery": "鸿雁,绿波,斜阳",
                "情感": "相思难寄",
                "赏析": "鸿雁在云鱼在水,情意难寄的惆怅"
            },
            "踏莎行": {
                "原文": "小径红稀,芳郊绿遍,高台树色阴阴见.春风不解禁杨花,蒙蒙乱扑行人面.翠叶藏莺,朱帘隔燕,炉香静逐游丝转.一场愁梦酒醒时,斜阳却照深深院.",
                "类型": "词",
                "style": "富贵闲适",
                "imagery": "春风,杨花,斜阳",
                "情感": "闲适感伤",
                "赏析": "富贵闲适中的淡淡感伤"
            },
            "破阵子": {
                "原文": "燕子来时新社,梨花落后清明.池上碧苔三四点,叶底黄鹂一两声,日长飞絮轻.巧笑东邻女伴,采桑径里逢迎.疑怪昨宵春梦好,元是今朝斗草赢,笑从双脸生.",
                "类型": "词",
                "style": "富贵闲适",
                "imagery": "燕子,梨花,碧苔",
                "情感": "春日闲适",
                "赏析": "富贵气象中的清新自然"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "时光流逝": "无可奈何花落去,似曾相识燕归来",
            "相思之情": "昨夜西风凋碧树,独上高楼,望尽天涯路",
            "富贵气象": "无可救药的太平宰相,富贵闲适",
            "王国维三境": "望尽天涯路为古今成大事业第一境",
            "珠圆玉润": "闲雅而有情思,语言华美精美"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "时光观念": "无可奈何花落去,时光不可逆转",
            "新生希望": "似曾相识燕归来,新生事物不可阻挡",
            "境界追求": "独上高楼,望尽天涯路--追求的境界",
            "含蓄之美": "晏殊词意在言外,含蓄蕴藉",
            "富贵与超脱": "太平宰相的富贵中亦含时光流逝的感慨"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的晏殊style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["无可奈何", "花落去", "似曾相识", "燕归来"]):
            score += 5
            matched_styles.append("感伤惆怅")
            matched_images.append("落花归燕")
        if any(word in text for word in ["西风凋碧树", "望尽天涯路", "独上高楼"]):
            score += 4
            matched_styles.append("典雅蕴藉")
            matched_images.append("西风碧树")
        if any(word in text for word in ["一曲新词", "去年天气", "旧亭台"]):
            score += 3
            matched_styles.append("富贵闲适")
        if any(word in text for word in ["鸿雁", "鱼在水", "惆怅"]):
            score += 3
            matched_styles.append("珠圆玉润")
        if any(word in text for word in ["燕子", "梨花", "清明"]):
            score += 2
            matched_styles.append("富贵闲适")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "晏殊style浓郁" if score >= 5 else "略有晏殊style" if score >= 3 else "不具晏殊style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get晏殊representative_works"""
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
        """get晏殊核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get晏殊的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get晏殊词完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get晏殊生平摘要"""
        return {
            "字": "同叔",
            "生卒": "991年-1055年",
            "籍贯": "抚州临川(今江西抚州)",
            "身份": "poet,政治家",
            "并称": "与晏几道并称'大小晏'",
            "地位": "北宋婉约词的重要开创者,富贵poet"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
