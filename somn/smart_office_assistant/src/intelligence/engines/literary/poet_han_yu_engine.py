"""
__all__ = [
    'getrepresentative_works',
]

韩愈深化引擎 - 古文运动与儒学复兴的雄奇智能系统
v1.0.0

核心理念:韩愈(768-824),字退之,号昌黎先生
诗歌style:奇崛险怪,以文为诗,雄奇奔放
哲学基础:儒家道统 + 反佛尊儒 + 古文运动
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 韩愈style类型(Enum):
    """韩愈诗文style分类"""
    雄奇怪异 = "以奇为美,突破常规"
    散文化 = "以文为诗,议论入诗"
    道统精神 = "儒家道统,传承圣人之道"
    刚直不屈 = "刚直不屈,不畏权贵"
    古文运动 = "古文运动,提倡散体"
    不平则鸣 = "不平则鸣,愤而为文"

class 韩愈意象类型(Enum):
    """韩愈常见imagery"""
    师道 = "师道:传道授业解惑"
    古文 = "古文:先秦两汉散文"
    仁义 = "仁义:儒家核心价值"
    佛骨 = "佛骨:反佛尊儒的标志事件"
    贬谪 = "贬谪:潮州岁月的磨砺"
    春雨 = "春雨:天街小雨润如酥"

@dataclass
class 韩愈诗歌characteristics:
    """韩愈诗文核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 韩愈深化引擎:
    """韩愈诗文深化分析引擎 v1.0.0"""

    VERSION = "v1.0.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 韩愈诗歌characteristics:
        return 韩愈诗歌characteristics(
            style=[
                "奇崛险怪:imagery奇特,style险怪",
                "以文为诗:散文笔法入诗,打破常规",
                "气势磅礴:韩潮苏海,如潮汹涌",
                "刚直不屈:三次被贬,始终不改其志"
            ],
            imagery=[
                "师道imagery:传道授业解惑",
                "仁义imagery:儒家核心精神",
                "古文imagery:先秦两汉散文传统",
                "不平imagery:贬谪不屈的抗争精神"
            ],
            修辞=[
                "奇崛imagery:追求险怪imagery",
                "以文为诗:散文议论入诗",
                "对比手法:古与今,正与邪的对比",
                "险怪用词:打破常规的词汇选择"
            ],
            情感=[
                "道统传承:传承儒家道统为己任",
                "反佛尊儒:坚决反对佛教",
                "提携后进:柳宗元,李翱皆出其门下",
                "不平则鸣:愤而为文,笔锋犀利"
            ],
            语言="奇崛险怪,精雕细琢,戛戛乎其难哉"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "师说": {
                "原文": "古之学者必有师.师者,所以传道受业解惑也.",
                "类型": "古文",
                "style": "散文化",
                "imagery": "师道,传道",
                "情感": "教育理想",
                "赏析": "师道famous_poems,提出教师职责与学习之道"
            },
            "进学解": {
                "原文": "业精于勤荒于嬉,行成于思毁于随.",
                "类型": "古文",
                "style": "散文化",
                "imagery": "勤学,修身",
                "情感": "自我勉励",
                "赏析": "借学生之口自嘲,构思巧妙"
            },
            "祭十二郎文": {
                "原文": "呜呼!吾少孤,及长,不省所怙,惟兄嫂是依.",
                "类型": "祭文",
                "style": "雄奇怪异",
                "imagery": "兄弟,生死",
                "情感": "悼亡真情",
                "赏析": "祭文中千年绝调,情真意切"
            },
            "左迁至蓝关示侄孙湘": {
                "原文": "一封朝奏九重天,夕贬潮州路八千.",
                "类型": "诗",
                "style": "刚直不屈",
                "imagery": "佛骨,潮州",
                "情感": "忠而被贬",
                "赏析": "忠而被贬,仍不改其志"
            },
            "早春呈水部张十八员外": {
                "原文": "天街小雨润如酥,草色遥看近却无.",
                "类型": "诗",
                "style": "奇崛险怪",
                "imagery": "春雨,草色",
                "情感": "早春欣喜",
                "赏析": "写早春名句,草色遥看近却无"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "教育理想": "师者,所以传道受业解惑也",
            "学习态度": "业精于勤荒于嬉,行成于思毁于随",
            "道统传承": "文以明道,传承圣人之道",
            "刚直精神": "欲为圣明除弊事,肯将衰朽惜残年",
            "不平则鸣": "不平则鸣,愤而为文",
            "勇于创新": "唯陈言之务去,戛戛乎其难哉"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "教育思想": "教师职责是传道授业解惑,打破门第观念",
            "学习态度": "学业的精进在于勤奋,品行的成就在于思考",
            "刚直品格": "面对错误敢直言,即使被贬也不改其志",
            "道统意识": "文化传承需要使命感与责任感",
            "提携后进": "发现和培养人才是文化延续的关键"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的韩愈style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["师", "道", "传道", "受业", "解惑"]):
            score += 3
            matched_styles.append("师道精神")
        if any(word in text for word in ["古文", "散文", "文以明道"]):
            score += 2
            matched_styles.append("古文运动")
        if any(word in text for word in ["佛", "反佛", "佛骨", "儒"]):
            score += 2
            matched_images.append("反佛尊儒")
        if any(word in text for word in ["勤", "思", "毁于随"]):
            score += 2
            matched_styles.append("学习态度")
        if any(word in text for word in ["贬", "谪", "潮州", "蓝关"]):
            score += 2
            matched_images.append("贬谪imagery")
        if any(word in text for word in ["不平", "则鸣", "愤"]):
            score += 2
            matched_styles.append("不平则鸣")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "韩愈style浓郁" if score >= 5 else "略有韩愈style" if score >= 3 else "不具韩愈style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get韩愈representative_works"""
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
        """get韩愈核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get韩愈的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get韩愈诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get韩愈生平摘要"""
        return {
            "字": "退之",
            "号": "昌黎先生",
            "生卒": "768年-824年",
            "籍贯": "河南河阳(今河南孟州)",
            "身份": "文学家,思想家,政治家,唐宋八大家之首",
            "并称": "与柳宗元并称'韩柳'",
            "地位": "唐宋八大家之首,古文运动领袖"
        }

# 测试函数
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")

    print("=" * 50)
    print("韩愈深化引擎 v1.0.0 测试")
    print("=" * 50)

    test_texts = [
        "师者,所以传道受业解惑也",
        "业精于勤荒于嬉,行成于思毁于随",
        "天街小雨润如酥,草色遥看近却无",
        "一封朝奏九重天,夕贬潮州路八千"
    ]

    print("\n[文本style分析测试]")
    for text in test_texts:
        result = engine.分析文本(text)
        print(f"文本: {text}")
        print(f"  得分: {result['score']}, judge: {result['judge']}")
        print()

    print("\n[生平摘要]")
    bio = engine.get生平摘要()
    for k, v in bio.items():
        print(f"  {k}: {v}")
