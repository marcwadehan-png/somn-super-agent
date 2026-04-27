"""
__all__ = [
    'getrepresentative_works',
]

刘禹锡深化引擎 - 诗豪豪迈与辩证智慧的铁骨智能系统
v8.2.0

核心理念:刘禹锡(772-842),字梦得,号poet豪杰
诗歌style:豪迈沉雄,含蓄隽永,清新明快
哲学基础:儒家济世 + 朴素唯物 + 辩证思维
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 刘禹锡style类型(Enum):
    """刘禹锡诗歌style分类"""
    诗豪豪迈 = "豪迈奔放,诗豪本色"
    怀古伤今 = "借古讽今,气象阔大"
    辩证思维 = "沉舟侧畔千帆过,病树前头万木春"
    清新华丽 = "竹枝词清新明快,民歌风韵"
    政治讽刺 = "玄都观桃花,讽刺权贵"
    陋室安贫 = "斯是陋室,惟吾德馨"

class 刘禹锡意象类型(Enum):
    """刘禹锡常见imagery"""
    沉舟病树 = "沉舟病树:逆境中的达观"
    千帆万木 = "千帆万木:新旧更替的希望"
    陋室 = "陋室:安贫乐道的象征"
    玄都观 = "玄都观桃花:讽刺朝中新贵"
    竹枝词 = "竹枝词:清新民歌style"
    前度刘郎 = "前度刘郎:坚韧不屈的精神"

@dataclass
class 刘禹锡诗歌characteristics:
    """刘禹锡诗歌核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 刘禹锡深化引擎:
    """刘禹锡诗歌深化分析引擎 v8.2.0"""

    VERSION = "v8.2.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 刘禹锡诗歌characteristics:
        return 刘禹锡诗歌characteristics(
            style=[
                "豪迈奔放:被称为诗豪,气势磅礴",
                "怀古伤今:借历史题材抒发现实感慨",
                "清新明快:竹枝ci_study习民歌style",
                "含蓄隽永:讽刺尖锐但不直露"
            ],
            imagery=[
                "沉舟病树:辩证看待逆境与新生",
                "陋室imagery:安贫乐道的精神追求",
                "玄都观桃花:讽刺权贵更迭",
                "竹枝词imagery:清新自然的民歌风韵"
            ],
           修辞=[
                "借古讽今:借历史人物讽刺现实权贵",
                "辩证思维:沉舟与千帆的对比",
                "谐音双关:道是无晴却有晴",
                "以物喻人:借山水喻社会人生"
            ],
            情感=[
                "济世抱负:渴望建功立业",
                "面对挫折:达观进取,不屈不挠",
                "民歌情怀:学习民间文学的清新追求",
                "文化传承:继往开来的历史责任感"
            ],
            语言="豪迈清新并重,含蓄隽永,寓理于景"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "陋室铭": {
                "原文": "山不在高,有仙则名.水不在深,有龙则灵.斯是陋室,惟吾德馨.",
                "类型": "铭文",
                "style": "陋室安贫",
                "imagery": "陋室,德馨",
                "情感": "安贫乐道",
                "赏析": "托物言志典范,何陋之有"
            },
            "酬乐天扬州初逢席上见赠": {
                "原文": "沉舟侧畔千帆过,病树前头万木春.",
                "类型": "诗",
                "style": "辩证思维",
                "imagery": "沉舟,病树,千帆",
                "情感": "达观进取",
                "赏析": "千古名句,辩证看待逆境与新生"
            },
            "竹枝词": {
                "原文": "东边日出西边雨,道是无晴却有晴.",
                "类型": "词",
                "style": "清新华丽",
                "imagery": "竹枝,东雨",
                "情感": "初恋之情",
                "赏析": "谐音双关,民歌风韵"
            },
            "玄都观桃花": {
                "原文": "紫陌红尘拂面来,无人不道看花回.玄都观里桃千树,尽是刘郎去后栽.",
                "类型": "诗",
                "style": "政治讽刺",
                "imagery": "桃花,玄都观",
                "情感": "讽刺权贵",
                "赏析": "讽刺朝中新贵,因此再贬"
            },
            "西塞山怀古": {
                "原文": "人世几回伤往事,山形依旧枕寒流.",
                "类型": "诗",
                "style": "怀古伤今",
                "imagery": "西塞山,金陵",
                "情感": "历史兴亡",
                "赏析": "被誉为金陵怀古之祖"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "逆境达观": "沉舟侧畔千帆过,病树前头万木春",
            "安贫乐道": "斯是陋室,惟吾德馨",
            "历史辩证": "人世几回伤往事,山形依旧枕寒流",
            "坚韧不屈": "前度刘郎今又来",
            "创新精神": "请君莫奏前朝曲,听唱新翻杨柳枝",
            "民歌情怀": "东边日出西边雨,道是无晴却有晴"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "逆境智慧": "在逆境中看到希望,新事物必然取代旧事物",
            "精神独立": "安贫乐道,以德为馨,不以外物为意",
            "历史意识": "以历史兴亡为镜鉴,反思现实",
            "创新精神": "不因循守旧,不断推陈出新",
            "民歌传统": "向民间文学学习,追求清新自然的语言"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的刘禹锡style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["沉舟", "病树", "千帆", "万木春"]):
            score += 4
            matched_styles.append("辩证思维")
            matched_images.append("沉舟病树")
        if any(word in text for word in ["陋室", "德馨", "何陋之有"]):
            score += 3
            matched_styles.append("陋室安贫")
        if any(word in text for word in ["桃花", "玄都观", "刘郎", "去后栽"]):
            score += 3
            matched_styles.append("政治讽刺")
        if any(word in text for word in ["竹枝", "东边日出", "无晴", "有晴"]):
            score += 3
            matched_styles.append("清新华丽")
        if any(word in text for word in ["怀古", "往事", "兴亡", "金陵"]):
            score += 2
            matched_images.append("怀古imagery")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "刘禹锡style浓郁" if score >= 5 else "略有刘禹锡style" if score >= 3 else "不具刘禹锡style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get刘禹锡representative_works"""
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
        """get刘禹锡核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get刘禹锡的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get刘禹锡诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get刘禹锡生平摘要"""
        return {
            "字": "梦得",
            "号": "poet豪杰,诗豪",
            "生卒": "772年-842年",
            "籍贯": "洛阳(今河南洛阳)",
            "身份": "poet,文学家,政治家",
            "并称": "与白居易并称'刘白',与柳宗元并称'刘柳'",
            "地位": "诗豪,怀古诗大家"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
