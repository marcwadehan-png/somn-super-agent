"""
__all__ = [
    'getrepresentative_works',
]

杜甫深化引擎 - 诗圣现实主义智能系统
v8.2.0

核心理念:杜甫(712-770),字子美,号少陵野老,老杜,诗圣
诗歌style:沉郁顿挫,忧国忧民,诗史特质
哲学基础:儒家济世 + 民本思想 + 君子人格
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 杜甫style类型(Enum):
    """杜甫诗歌style分类"""
    沉郁顿挫 = "情感深厚,节奏多变"
    忧国忧民 = "心系苍生,批判现实"
    律法谨严 = "对仗精工,格律严谨"
    诗史特质 = "以诗写史,记录时代"
    日常温情 = "平凡生活,人间烟火"

class 杜甫意象类型(Enum):
    """杜甫常用imagery"""
    百姓 = "黎元,苍生,寒士"
    战乱 = "烽火,兵革,征战"
    秋 = "秋,落木,萧萧"
    登高 = "登高,凭栏,远望"
    茅屋 = "茅屋,破屋,寒士"
    故乡 = "故乡,月夜,兄弟"

@dataclass
class 杜甫诗歌characteristics:
    """杜甫诗歌核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 杜甫深化引擎:
    """杜甫诗歌深化分析引擎 v8.2.0"""
    
    VERSION = "v8.2.0"
    
    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()
    
    def _init_characteristics(self) -> 杜甫诗歌characteristics:
        return 杜甫诗歌characteristics(
            style=[
                "沉郁顿挫:情感的深厚浓郁与节奏的停顿转折",
                "忧国忧民:心系苍生,批判现实黑暗",
                "以小见大:个人悲欢与时代洪流交织",
                "律法谨严:对仗精工,意脉贯通"
            ],
            imagery=[
                "百姓imagery:黎元,苍生,冻死骨",
                "战乱imagery:烽火,兵革,乱离",
                "秋imagery:落木,秋风,悲秋",
                "登高imagery:登台,凭栏,远望"
            ],
            修辞=[
                "对比手法:朱门酒肉臭vs路有冻死骨",
                "移情于物:感时花溅泪,恨别鸟惊心",
                "细节描写:白头搔更短,浑欲不胜簪",
                "以乐景写哀:城春草木深"
            ],
            情感=[
                "忧国忧民:穷年忧黎元,叹息肠内热",
                "家国情怀:国破山河在,城春草木深",
                "济世抱负:安得广厦千万间,大庇天下寒士",
                "身世之感:万里悲秋常作客,百年多病独登台"
            ],
            语言="精工锤炼,语不惊人死不休"
        )
    
    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "春望": {
                "原文": "国破山河在,城春草木深.感时花溅泪,恨别鸟惊心.",
                "style": "沉郁顿挫",
                "imagery": "国破,春望,花鸟",
                "情感": "亡国之痛",
                "赏析": "首联以乐景写哀,颔联移情于物"
            },
            "茅屋为秋风所破歌": {
                "原文": "八月秋高风怒号,卷我屋上三重茅...",
                "style": "忧国忧民",
                "imagery": "秋风,茅屋,广厦",
                "情感": "推己及人的博大情怀",
                "名句": "安得广厦千万间,大庇天下寒士俱欢颜"
            },
            "登高": {
                "原文": "风急天高猿啸哀,渚清沙白鸟飞回...",
                "style": "沉郁顿挫",
                "imagery": "风,天,落木,长风",
                "情感": "身世之悲,家国之恨",
                "评价": "古今七律第一"
            },
            "自京赴奉先县咏怀五百字": {
                "原文": "杜陵有布衣,老大意转拙.许身一何愚,窃比稷与契.",
                "style": "忧国忧民",
                "imagery": "黎元,朱门,冻死骨",
                "情感": "忧国忧民的代表性作品",
                "名句": "朱门酒肉臭,路有冻死骨"
            },
            "望岳": {
                "原文": "岱宗夫如何?齐鲁青未了.造化钟神秀,阴阳割昏晓.",
                "style": "豪迈奔放",
                "imagery": "岱宗,齐鲁,神秀",
                "情感": "少年壮志",
                "名句": "会当凌绝顶,一览众山小"
            },
            "蜀相": {
                "原文": "丞相祠堂何处寻,锦官城外柏森森.",
                "style": "沉郁顿挫",
                "imagery": "祠堂,柏森森,出师",
                "情感": "敬仰,惋惜",
                "名句": "出师未捷身先死,长使英雄泪满襟"
            }
        }
    
    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "忧国忧民": "穷年忧黎元,叹息肠内热",
            "民本思想": "朱门酒肉臭,路有冻死骨",
            "济世抱负": "安得广厦千万间,大庇天下寒士俱欢颜",
            "家国情怀": "国破山河在,城春草木深",
            "壮志豪情": "会当凌绝顶,一览众山小",
            "批判现实": "不废江河万古流"
        }
    
    def _init_revelations(self) -> Dict[str, str]:
        return {
            "忧患意识": "生于忧患,死于安乐的东方智慧",
            "民本思想": "以人民为中心的价值取向",
            "人格力量": "逆境中的坚守与担当",
            "家国情怀": "个人命运与国家命运的紧密相连",
            "批判精神": "直面社会问题,不回避黑暗"
        }
    
    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """
        分析给定文本是否具有杜甫style
        
        Args:
            text: 待分析文本
            
        Returns:
            杜甫style分析结果
        """
        score = 0
        matched_styles = []
        matched_images = []
        
        # 沉郁顿挫
        if any(word in text for word in ["秋", "悲", "病", "愁", "苦"]):
            score += 2
            matched_styles.append(杜甫style类型.沉郁顿挫.value)
        
        # 忧国忧民
        if any(word in text for word in ["国", "民", "黎元", "苍生", "寒士"]):
            score += 3
            matched_styles.append(杜甫style类型.忧国忧民.value)
            matched_images.append("百姓imagery")
        
        # 战乱imagery
        if any(word in text for word in ["烽火", "兵", "战", "乱", "破"]):
            score += 2
            matched_images.append("战乱imagery")
        
        # 登高imagery
        if any(word in text for word in ["登", "高", "台", "望", "凭"]):
            score += 1
            matched_styles.append(杜甫style类型.登高.value)
        
        # 批判现实
        if any(word in text for word in ["朱门", "冻死", "酒肉"]):
            score += 3
            matched_styles.append(杜甫style类型.忧国忧民.value)
        
        # 济世抱负
        if any(word in text for word in ["广厦", "大庇", "俱欢颜"]):
            score += 3
            matched_images.append("济世抱负")
        
        style_ratio = min(score / 10, 1.0)
        
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "is_du_fu_style": score >= 5,
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "杜甫style浓郁" if score >= 5 else "略有杜甫style" if score >= 3 else "不具杜甫style"
        }
    
    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get杜甫representative_works"""
        if style:
            return [
                {**poem, "title": title}
                for title, poem in self.经典famous_poems.items()
                if poem["style"] == style
            ]
        return [
            {**poem, "title": title}
            for title, poem in self.经典famous_poems.items()
        ]
    
    def get核心spiritual_insight(self) -> Dict[str, str]:
        """get杜甫核心spiritual_insight"""
        return self.核心spiritual_insight
    
    def get现代revelations(self) -> Dict[str, str]:
        """get杜甫的现代revelations"""
        return self.现代revelations
    
    def get诗歌characteristics(self) -> Dict:
        """get杜甫诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }
    
    def get生平摘要(self) -> Dict:
        """get杜甫生平摘要"""
        return {
            "字": "子美",
            "号": "少陵野老,老杜,诗圣",
            "生卒": "712年-770年",
            "籍贯": "河南巩县(今河南省巩义市)",
            "身份": "poet,官员",
            "并称": "与李白并称'李杜'",
            "地位": "诗圣,诗史,中国现实主义诗歌最高峰"
        }
    
    def get李杜对比(self) -> Dict:
        """get李白与杜甫对比"""
        return {
            "诗歌style": {"李白": "豪放飘逸", "杜甫": "沉郁顿挫"},
            "创作方法": {"李白": "浪漫主义", "杜甫": "现实主义"},
            "关注焦点": {"李白": "个人超脱", "杜甫": "社会现实"},
            "诗歌语言": {"李白": "自然天成", "杜甫": "精工锤炼"},
            "人生态度": {"李白": "追求自由", "杜甫": "积极入世"},
            "诗歌史地位": {"李白": "诗仙", "杜甫": "诗圣"},
            "representative_works": {"李白": "<将进酒><蜀道难>", "杜甫": "<兵车行><春望>"}
        }
    
    def 创作指导(self, theme: str, emotion: str) -> Dict:
        """
        提供杜甫style的创作指导
        
        Args:
            theme: 主题(如"忧国","登高")
            emotion: 情感(如"沉郁","悲愤")
            
        Returns:
            创作指导
        """
        guidance = {
            "主题": theme,
            "情感": emotion,
            "推荐imagery": [],
            "修辞手法": [],
            "语言style": "精工锤炼,格律严谨",
            "参考作品": []
        }
        
        # 根据主题推荐imagery
        if theme in ["忧国", "战乱", "批判"]:
            guidance["推荐imagery"] = ["烽火", "黎元", "冻死骨", "朱门"]
            guidance["修辞手法"] = ["对比", "移情于物"]
            guidance["参考作品"] = ["<兵车行>", "<自京赴奉先县咏怀五百字>"]
        elif theme in ["登高", "秋思", "身世"]:
            guidance["推荐imagery"] = ["落木", "长江", "秋", "病"]
            guidance["语言style"] = "沉郁顿挫,对仗工整"
            guidance["参考作品"] = ["<登高>", "<秋兴八首>"]
        elif theme in ["济世", "理想", "仁政"]:
            guidance["推荐imagery"] = ["广厦", "寒士", "广厦千万间"]
            guidance["情感基调"] = "推己及人的博大情怀"
            guidance["参考作品"] = ["<茅屋为秋风所破歌>"]
        elif theme in ["家国", "思乡"]:
            guidance["推荐imagery"] = ["国破", "月夜", "烽火"]
            guidance["参考作品"] = ["<春望>", "<月夜忆舍弟>"]
        
        return guidance

# 测试函数
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
