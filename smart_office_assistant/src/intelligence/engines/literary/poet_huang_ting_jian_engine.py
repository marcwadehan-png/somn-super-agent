"""
__all__ = [
    'getrepresentative_works',
]

黄庭坚深化引擎 - 江西诗派与瘦硬通神的智能系统
v8.2.0

核心理念:黄庭坚(1045-1105),字鲁直,号山谷道人
诗歌style:瘦硬通神,点铁成金,骨力劲健,豪放婉约兼擅
哲学基础:江西诗派 + 宗杜学韩 + 诗词双绝
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 黄庭坚style类型(Enum):
    """黄庭坚诗词style分类"""
    瘦硬通神 = "骨力劲健,imagery奇崛"
    点铁成金 = "化用前人,翻出新意"
    豪放词风 = "豪放词风的代表"
    婉约词风 = "清平乐等婉约精品"
    用典精切 = "用典精当,不露痕迹"

class 黄庭坚意象类型(Enum):
    """黄庭坚常见imagery"""
    落木澄江 = "落木千山天远大,澄江一道月分明"
    白鸥 = "白鸥:归隐的象征"
    黄鹂 = "黄鹂:春的使者"
    长笛 = "长笛:归船之思"
    蔷薇 = "蔷薇:春归之处"

@dataclass
class 黄庭坚诗歌characteristics:
    """黄庭坚诗文核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 黄庭坚深化引擎:
    """黄庭坚诗文深化分析引擎 v8.2.0"""

    VERSION = "6.2.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> 黄庭坚诗歌characteristics:
        return 黄庭坚诗歌characteristics(
            style=[
                "瘦硬通神:骨力劲健,imagery奇崛",
                "点铁成金:化用前人,翻出新意",
                "夺胎换骨:师承诗意,创新表达",
                "诗词双绝:诗与词皆为大家"
            ],
            imagery=[
                "落木澄江:秋景的壮阔与清朗",
                "白鸥imagery:归隐江湖的追求",
                "长笛imagery:归船吹笛的意境",
                "黄鹂蔷薇:春归夏来的流转"
            ],
            修辞=[
                "点铁成金:化用前人诗句,如灵丹一粒",
                "夺胎换骨:窥入诗意,形容创新",
                "以典入诗:用典精当,不露痕迹",
                "句法变化:打破常规句式,追求新奇"
            ],
            情感=[
                "归隐之思:万里归船弄长笛,此心吾与白鸥盟",
                "朋友思念:桃李春风一杯酒,江湖夜雨十年灯",
                "贬谪之痛:投荒万死鬓毛斑的坚韧",
                "哲学思辨:春归何处的对人生意义的追问"
            ],
            语言="瘦硬通神,用典精切,意境清远"
        )

    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "登快阁": {
                "原文": "痴儿了却公家事,快阁东西倚晚晴.落木千山天远大,澄江一道月分明.朱弦已为佳人绝,青眼聊因美酒横.万里归船弄长笛,此心吾与白鸥盟.",
                "类型": "诗",
                "style": "瘦硬通神",
                "imagery": "落木,澄江,白鸥",
                "情感": "归隐之思",
                "赏析": "落木千山天远大,澄江一道月分明--千古名句"
            },
            "寄黄几复": {
                "原文": "我居北海君南海,寄雁传书谢不能.桃李春风一杯酒,江湖夜雨十年灯.持家但有四立壁,治病不蕲三折肱.想见读书头已白,隔溪猿哭瘴溪藤.",
                "类型": "诗",
                "style": "点铁成金",
                "imagery": "桃李春风,江湖夜雨",
                "情感": "朋友思念",
                "赏析": "桃李春风一杯酒,江湖夜雨十年灯--对仗名句"
            },
            "清平乐": {
                "原文": "春归何处?寂寞无行路.若有人知春去处,唤取归来同住.春无踪迹谁知?除非问取黄鹂.百啭无人能解,因风飞过蔷薇.",
                "类型": "词",
                "style": "婉约词风",
                "imagery": "黄鹂,蔷薇",
                "情感": "惜春之情",
                "赏析": "以问句贯穿,跌宕有致,余韵悠长"
            },
            "念奴娇": {
                "原文": "断虹霁雨,净秋空,山染修眉新绿.桂影扶疏,谁便道,今夕清辉不足?万里青天,姮娥何处,驾此一轮玉?老子平生,江南江北,最爱临风笛.",
                "类型": "词",
                "style": "豪放词风",
                "imagery": "断虹,桂影,万里青天",
                "情感": "豪放洒脱",
                "赏析": "老子平生,江南江北,最爱临风笛--豪放词风"
            },
            "雨中登岳阳楼望君山": {
                "原文": "投荒万死鬓毛斑,生出瞿塘滟滪关.未到江南先一笑,岳阳楼上对君山.",
                "类型": "诗",
                "style": "瘦硬通神",
                "imagery": "瞿塘,君山",
                "情感": "贬谪坚韧",
                "赏析": "投荒万死鬓毛斑--贬谪中依然豁达"
            }
        }

    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "点铁成金": "古之能为文章者,真能陶冶万物,虽取古人之陈言入于翰墨,如灵丹一粒,点铁成金也",
            "归隐之思": "万里归船弄长笛,此心吾与白鸥盟",
            "朋友之情": "桃李春风一杯酒,江湖夜雨十年灯",
            "瘦硬通神": "江西诗派的核心追求,骨力劲健",
            "诗词双绝": "与苏轼并称苏黄,诗与词皆为大家"
        }

    def _init_revelations(self) -> Dict[str, str]:
        return {
            "继承创新": "在继承中求创新,点铁成金的智慧",
            "以典入诗": "用典精切,不露痕迹,显示学养",
            "友情珍重": "桃李春风一杯酒,江湖夜雨十年灯--友情的珍贵",
            "归隐智慧": "此心吾与白鸥盟--在纷扰中保持本心",
            "人生感悟": "春归何处--对时光流逝的哲思"
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的黄庭坚style"""
        score = 0
        matched_styles = []
        matched_images = []

        if any(word in text for word in ["落木", "澄江", "月分明"]):
            score += 5
            matched_styles.append("瘦硬通神")
            matched_images.append("落木澄江")
        if any(word in text for word in ["桃李春风", "一杯酒", "江湖夜雨", "十年灯"]):
            score += 4
            matched_styles.append("点铁成金")
            matched_images.append("桃李春风")
        if any(word in text for word in ["白鸥", "归船", "长笛盟"]):
            score += 4
            matched_styles.append("瘦硬通神")
        if any(word in text for word in ["春归何处", "黄鹂", "蔷薇"]):
            score += 4
            matched_styles.append("婉约词风")
        if any(word in text for word in ["老子平生", "临风笛", "江南江北"]):
            score += 3
            matched_styles.append("豪放词风")

        style_ratio = min(score / 10, 1.0)
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "黄庭坚style浓郁" if score >= 5 else "略有黄庭坚style" if score >= 3 else "不具黄庭坚style"
        }

    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get黄庭坚representative_works"""
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
        """get黄庭坚核心spiritual_insight"""
        return self.核心spiritual_insight

    def get现代revelations(self) -> Dict[str, str]:
        """get黄庭坚的现代revelations"""
        return self.现代revelations

    def get诗歌characteristics(self) -> Dict:
        """get黄庭坚诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }

    def get生平摘要(self) -> Dict:
        """get黄庭坚生平摘要"""
        return {
            "字": "鲁直,号山谷道人",
            "生卒": "1045年-1105年",
            "籍贯": "洪州分宁(今江西九江)",
            "身份": "poet,poet,书法家",
            "并称": "与苏轼并称'苏黄',与蔡京,米芾并称宋代书法四大家",
            "地位": "江西诗派开创者,唐宋八大家之一"
        }

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
