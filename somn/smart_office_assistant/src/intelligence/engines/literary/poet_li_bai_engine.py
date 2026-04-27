"""
__all__ = [
    'getrepresentative_works',
]

李白深化引擎 - 诗仙浪漫主义智能系统
v1.0.0

核心理念:李白(701-762),字太白,号青莲居士,谪仙人
诗歌style:豪放飘逸,想象奇特,情感激越
哲学基础:道家逍遥 + 儒家济世 + 游侠精神
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 李白style类型(Enum):
    """李白诗歌style分类"""
    豪放飘逸 = "豪放飘逸,气象万千"
    浪漫想象 = "想象奇特,突破常规"
    自然天成 = "语言通俗,意境深远"
    傲骨风骨 = "傲岸不屈,人格独立"
    思乡怀人 = "月下相思,游子情怀"
    济世抱负 = "功名渴望,济世情怀"

class 李白意象类型(Enum):
    """李白常用imagery"""
    酒 = "酒:旷达,洒脱,超越"
    月 = "月:思乡,孤独,永恒"
    剑 = "剑:侠客,自由,力量"
    鹏 = "鹏:大鹏展翅,志向高远"
    瀑布 = "瀑布:气势磅礴,壮美"
    黄河 = "黄河:奔放,不羁"
    扁舟 = "扁舟:归隐,逍遥"
    仙人 = "仙人:超脱,长生"

@dataclass
class 李白诗歌characteristics:
    """李白诗歌核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 李白深化引擎:
    """李白诗歌深化分析引擎 v1.0.0"""
    
    VERSION = "v1.0.0"
    
    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()
    
    def _init_characteristics(self) -> 李白诗歌characteristics:
        return 李白诗歌characteristics(
            style=[
                "豪放飘逸,不受拘束",
                "想象奇特,大胆夸张",
                "气势磅礴,震人心魄",
                "情感激越,爱恨分明"
            ],
            imagery=[
                "酒,月,剑,鹏",
                "黄河,长江,瀑布",
                "青山,白云,扁舟",
                "仙人,瑶台,天宫"
            ],
            修辞=[
                "大胆夸张:白发三千丈",
                "奇特想象:银河落九天",
                "对比强烈:黄河之水与人生短暂",
                "拟人手法:月会'邀'人饮酒"
            ],
            情感=[
                "旷达超脱:人生得意须尽欢",
                "傲骨不屈:安能摧眉折腰事权贵",
                "思乡怀人:举头望明月,低头思故乡",
                "济世抱负:大鹏一日同风起"
            ],
            语言="语言通俗,明白如话,看似随意实则精雕细琢"
        )
    
    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "静夜思": {
                "原文": "床前明月光,疑是地上霜.举头望明月,低头思故乡.",
                "style": "自然天成",
                "imagery": "月,霜",
                "情感": "思乡",
                "赏析": "语言极简却意境深远,以霜喻月光,渲染清冷氛围"
            },
            "将进酒": {
                "原文": "君不见黄河之水天上来,奔流到海不复回...",
                "style": "豪放飘逸",
                "imagery": "黄河,酒,月",
                "情感": "旷达,超越",
                "名句": "天生我材必有用,千金散尽还复来"
            },
            "蜀道难": {
                "原文": "噫吁嚱,危乎高哉!蜀道之难,难于上青天!",
                "style": "浪漫想象",
                "imagery": "蜀道,鸟道,六龙",
                "情感": "震撼,感叹",
                "特色": "融入神话传说,想象奇特"
            },
            "早发白帝城": {
                "原文": "朝辞白帝彩云间,千里江陵一日还.",
                "style": "轻快明丽",
                "imagery": "彩云,轻舟,万重山",
                "情感": "重获自由的喜悦",
                "特色": "以轻快笔调写轻松心情"
            },
            "行路难": {
                "原文": "金樽清酒斗十千,玉盘珍羞直万钱...",
                "style": "豪放与悲愤交织",
                "imagery": "冰塞川,雪满山,行路难",
                "情感": "困境中的自信",
                "名句": "长风破浪会有时,直挂云帆济沧海"
            },
            "望庐山瀑布": {
                "原文": "日照香炉生紫烟,遥看瀑布挂前川.",
                "style": "浪漫想象",
                "imagery": "香炉,紫烟,瀑布",
                "情感": "壮美,惊叹",
                "名句": "飞流直下三千尺,疑是银河落九天"
            }
        }
    
    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "人生态度": "天生我材必有用,千金散尽还复来",
            "自由精神": "安能摧眉折腰事权贵,使我不得开心颜",
            "进取精神": "长风破浪会有时,直挂云帆济沧海",
            "超脱智慧": "人生在世不称意,明朝散发弄扁舟",
            "珍惜时光": "君不见黄河之水天上来,奔流到海不复回",
            "自信傲骨": "仰天大笑出门去,我辈岂是蓬蒿人"
        }
    
    def _init_revelations(self) -> Dict[str, str]:
        return {
            "自由精神": "追求人格独立与精神自由,不为权贵折腰",
            "自信进取": "天生我材必有用的自信,积极进取的人生态度",
            "浪漫情怀": "对理想的不懈追求,对美好事物的热爱",
            "超越困境": "在困境中保持旷达,用诗意化解苦难",
            "活在当下": "珍惜时光,及时行乐,但不虚度光阴"
        }
    
    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """
        分析给定文本是否具有李白style
        
        Args:
            text: 待分析文本
            
        Returns:
            李白style分析结果
        """
        text_lower = text.lower()
        score = 0
        matched_styles = []
        matched_images = []
        
        # 豪放飘逸
        if any(word in text for word in ["豪", "放", "天", "地", "大", "九"]):
            score += 2
            matched_styles.append(李白style类型.豪放飘逸.value)
        
        # 酒月imagery
        if any(word in text for word in ["酒", "月", "杯", "樽"]):
            score += 3
            matched_images.append("酒/月imagery")
        
        # 黄河长江
        if any(word in text for word in ["黄河", "长江", "江", "海"]):
            score += 2
            matched_images.append("水系imagery")
        
        # 鹏鸟imagery
        if any(word in text for word in ["鹏", "飞", "翔", "云"]):
            score += 2
            matched_images.append("飞鸟imagery")
        
        # 思乡情感
        if any(word in text for word in ["故乡", "思乡", "归", "故"]):
            score += 2
            matched_styles.append(李白style类型.思乡怀人.value)
        
        # 自信超越
        if any(word in text for word in ["必", "有用", "千金", "复来"]):
            score += 3
            matched_styles.append(李白style类型.济世抱负.value)
        
        # 计算style占比
        style_ratio = min(score / 10, 1.0)
        
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "is_li_bai_style": score >= 5,
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "李白style浓郁" if score >= 5 else "略有李白style" if score >= 3 else "不具李白style"
        }
    
    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get李白representative_works"""
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
        """get李白核心spiritual_insight"""
        return self.核心spiritual_insight
    
    def get现代revelations(self) -> Dict[str, str]:
        """get李白的现代revelations"""
        return self.现代revelations
    
    def get诗歌characteristics(self) -> Dict:
        """get李白诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }
    
    def get生平摘要(self) -> Dict:
        """get李白生平摘要"""
        return {
            "字": "太白",
            "号": "青莲居士,谪仙人",
            "生卒": "701年-762年",
            "籍贯": "碎叶城(今吉尔吉斯斯坦),出生于四川江油",
            "身份": "poet,道士,剑客",
            "并称": "与杜甫并称'李杜'",
            "地位": "诗仙,中国浪漫主义诗歌最高峰"
        }
    
    def 创作指导(self, theme: str, emotion: str) -> Dict:
        """
        提供李白style的创作指导
        
        Args:
            theme: 主题(如"思乡","壮志")
            emotion: 情感(如"旷达","悲愤")
            
        Returns:
            创作指导
        """
        guidance = {
            "主题": theme,
            "情感": emotion,
            "推荐imagery": [],
            "修辞手法": [],
            "语言style": "通俗流畅,意到笔随",
            "参考作品": []
        }
        
        # 根据主题推荐imagery
        if theme in ["思乡", "离别"]:
            guidance["推荐imagery"] = ["月", "酒", "归雁", "故乡"]
            guidance["参考作品"] = ["<静夜思>", "<黄鹤楼送孟浩然之广陵>"]
        elif theme in ["壮志", "进取", "自信"]:
            guidance["推荐imagery"] = ["大鹏", "长风", "云帆", "沧海"]
            guidance["修辞手法"] = ["大胆夸张", "奇特想象"]
            guidance["参考作品"] = ["<行路难>", "<上李邕>"]
        elif theme in ["自然", "山水", "超脱"]:
            guidance["推荐imagery"] = ["瀑布", "黄河", "青山", "扁舟"]
            guidance["语言style"] = "清新自然,浑然天成"
            guidance["参考作品"] = ["<望庐山瀑布>", "<早发白帝城>"]
        
        # 根据情感调整
        if emotion in ["旷达", "洒脱", "喜悦"]:
            guidance["语气"] = "高昂向上,超越世俗"
            guidance["名句参考"] = "人生得意须尽欢,莫使金樽空对月"
        elif emotion in ["悲愤", "郁结", "困境"]:
            guidance["语气"] = "悲中有豪,绝处逢生"
            guidance["名句参考"] = "长风破浪会有时,直挂云帆济沧海"
        
        return guidance

# 测试函数
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
