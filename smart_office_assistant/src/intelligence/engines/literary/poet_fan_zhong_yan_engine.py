"""
__all__ = [
    'getrepresentative_works',
]

范仲淹深化引擎 - 先忧后乐与苍凉悲壮的智能系统
v8.2.0

核心理念:范仲淹(989-1052),字希文
诗歌style:苍凉悲壮,刚柔并济,境界开阔
哲学基础:儒家济世精神 + 以诗为词 + 庆历新政
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 范仲淹style类型(Enum):
    """范仲淹诗词style分类"""
    苍凉悲壮 = "边塞词的苍凉悲壮"
    刚柔并济 = "既有豪放之作,也有婉约之词"
    以诗为词 = "词中有诗的意境"
    怀人思乡 = "思念故乡和亲人"
    济世情怀 = "先天下之忧而忧的儒家精神"

class 范仲淹意象类型(Enum):
    """范仲淹常见imagery"""
    塞下秋色 = "塞下秋色:边塞苍凉"
    衡阳雁 = "衡阳雁:边塞imagery"
    长烟落日 = "长烟落日:边塞黄昏"
    碧云黄叶 = "碧云黄叶:秋日思念"
    芳草斜阳 = "芳草斜阳:怀人imagery"
    羌管霜地 = "羌管霜地:边塞艰苦"

@dataclass
class 范仲淹诗歌characteristics:
    """范仲淹诗文核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 范仲淹深化引擎:
    """范仲淹诗文深化分析引擎 v8.2.0"""

    VERSION = "v8.2.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 范仲淹诗歌characteristics:
        return 范仲淹诗歌characteristics(
            style=[
                "苍凉悲壮:边塞词的典型style",
                "刚柔并济:豪放与婉约兼具",
                "以诗为词:打破词为艳科的传统",
                "境界开阔:忧国忧民的济世情怀"
            ],
            imagery=[
                "塞下秋色:边塞的苍凉",
                "衡阳雁:边塞与思乡的imagery",
                "碧云黄叶:秋日思念的意境",
                "长烟落日:边塞黄昏的壮美"
            ],
            修辞=[
                "情景交融:借边塞景物抒发感慨",
                "以景结情:以边塞景色收束全词",
                "对比手法:将军白发与征夫泪的对比",
                "白描手法:语言质朴,意境深远"
            ],
            情感=[
                "边塞之苦:戍边将士的艰辛",
                "思乡之情:远离故乡的愁思",
                "壮志未酬:报国无门的感慨",
                "济世理想:先天下之忧而忧的抱负"
            ],
            语言="沉雄苍凉,悲壮深沉,意境开阔"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "渔家傲": {
                "原文": "塞下秋来风景异,衡阳雁去无留意.四面边声连角起,千嶂里,长烟落日孤城闭.",
                "类型": "词",
                "style": "苍凉悲壮",
                "imagery": "塞下秋色,衡阳雁,长烟落日",
                "情感": "边塞之苦",
                "赏析": "边塞词的代表作,打破词为艳科传统"
            },
            "苏幕遮": {
                "原文": "碧云天,黄叶地,秋色连波,波上寒烟翠.山映斜阳天接水,芳草无情,更在斜阳外.",
                "类型": "词",
                "style": "刚柔并济",
                "imagery": "碧云,黄叶,芳草",
                "情感": "怀人思乡",
                "赏析": "写秋景名句,意境开阔"
            },
            "岳阳楼记": {
                "原文": "先天下之忧而忧,后天下之乐而乐.",
                "类型": "文",
                "style": "济世情怀",
                "imagery": "天下,忧乐",
                "情感": "政治理想",
                "赏析": "千古名句,北宋散文巅峰"
            },
            "御街行": {
                "原文": "纷纷坠叶飘香砌,夜寂静,寒声碎.真珠帘卷玉楼空,天淡银河垂地.",
                "类型": "词",
                "style": "刚柔并济",
                "imagery": "坠叶,寒声,玉楼",
                "情感": "秋夜怀人",
                "赏析": "婉约词的精品"
            },
            "剔银灯": {
                "原文": "昨夜因看蜀志,笑曹操孙权刘备.用尽机关,徒劳心力,只得三分天地.",
                "类型": "词",
                "style": "苍凉悲壮",
                "imagery": "蜀志,曹操,孙权",
                "情感": "历史感慨",
                "赏析": "以诗为词的代表"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "政治理想": "先天下之忧而忧,后天下之乐而乐",
            "边塞悲壮": "浊酒一杯家万里,燕然未勒归无计",
            "秋景名句": "碧云天,黄叶地,秋色连波",
            "以诗为词": "打破词为艳科的传统",
            "四起四落": "屡遭贬谪,始终不改其志"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "济世精神": "先天下之忧而忧,体现儒家士大夫的担当",
            "边塞词风": "范仲淹的边塞词打破了词为艳科的传统",
            "刚柔并济": "兼具豪放与婉约,展现多元style",
            "政治勇气": "主持庆历新政,不怕得罪权贵",
            "百折不挠": "四起四落,始终不改其志"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的范仲淹style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["先天下", "忧而忧", "后天下", "乐而乐"]):
            score += 5
            matched_styles.append("济世情怀")
            matched_images.append("政治理想")
        if any(word in text for word in ["塞下", "秋来", "衡阳雁", "燕然", "征夫"]):
            score += 4
            matched_styles.append("苍凉悲壮")
            matched_images.append("边塞imagery")
        if any(word in text for word in ["碧云", "黄叶", "秋色", "芳草"]):
            score += 3
            matched_styles.append("刚柔并济")
            matched_images.append("秋景imagery")
        if any(word in text for word in ["长烟", "落日", "孤城", "浊酒"]):
            score += 3
            matched_styles.append("苍凉悲壮")
        if any(word in text for word in ["将军白发", "征夫泪"]):
            score += 2
            matched_styles.append("苍凉悲壮")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "范仲淹style浓郁" if score >= 5 else "略有范仲淹style" if score >= 3 else "不具范仲淹style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get范仲淹representative_works"""
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
        """get范仲淹核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get范仲淹的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get范仲淹诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get范仲淹生平摘要"""
        return {
            "字": "希文",
            "生卒": "989年-1052年",
            "籍贯": "苏州吴县(今江苏苏州)",
            "身份": "政治家,文学家",
            "并称": "与欧阳修等并称北宋文坛巨匠",
            "地位": "先天下之忧而忧的政治家与文学家"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
