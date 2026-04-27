"""
__all__ = [
    'getrepresentative_works',
]

王维深化引擎 - 诗佛禅意派智能系统
v8.2.0

核心理念:王维(701-761),字摩诘,号摩诘居士
诗歌style:诗中有画,画中有诗,禅意盎然
哲学基础:佛教禅宗 + 儒家底色 + 自然主义
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

class 王维style类型(Enum):
    """王维诗歌style分类"""
    诗中有画 = "视觉imagery丰富,色彩鲜明"
    禅意盎然 = "意境空灵,超然象外"
    动静相宜 = "静中有动,动中有静"
    山水田园 = "隐逸情怀,自然和谐"
    送别之情 = "深情厚谊,感人至深"

class 王维意象类型(Enum):
    """王维常用imagery"""
    空山 = "空山新雨,一切皆空"
    明月 = "明月松间,静谧清幽"
    清泉 = "清泉石上,纯净无染"
    竹林 = "竹里馆中,独坐幽篁"
    白云 = "行到水穷,坐看云起"

@dataclass
class 王维诗歌characteristics:
    """王维诗歌核心characteristics"""
    style: List[str]
    imagery: List[str]
    修辞: List[str]
    情感: List[str]
    语言: str

class 王维深化引擎:
    """王维诗歌深化分析引擎 v8.2.0"""
    
    VERSION = "v8.2.0"
    
    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()
        self.wangchuan二十景 = self._init_wangchuan()
    
    def _init_characteristics(self) -> 王维诗歌characteristics:
        return 王维诗歌characteristics(
            style=[
                "诗中有画:视觉imagery丰富,色彩鲜明",
                "画中有诗:画面感强,构图精美",
                "动静相宜:静中有动,以动写静",
                "禅意盎然:意境空灵,超然象外"
            ],
            imagery=[
                "空山imagery:空山新雨,空林,人不知",
                "明月imagery:明月松间,明月来相照",
                "清泉imagery:清泉石上流,流水不腐",
                "竹林imagery:竹喧,幽篁,竹里馆"
            ],
            修辞=[
                "以声写寂:但闻人语响",
                "以动写静:月出惊山鸟,时鸣春涧中",
                "色彩渲染:大漠孤烟直,长河落日圆",
                "反用典故:随意春芳歇,王孙自可留"
            ],
            情感=[
                "隐逸情怀:随意春芳歇,王孙自可留",
                "禅意超脱:行到水穷处,坐看云起时",
                "自然和谐:明月松间照,清泉石上流",
                "送别深情:劝君更尽一杯酒,西出阳关无故人"
            ],
            语言="纯净洗练,浑然天成,意境圆融"
        )
    
    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "山居秋暝": {
                "原文": "空山新雨后,天气晚来秋.明月松间照,清泉石上流.",
                "style": "诗中有画",
                "imagery": "空山,秋雨,明月,清泉",
                "情感": "隐逸秋居的宁静美好",
                "名句": "明月松间照,清泉石上流",
                "评价": "千古传诵的意境典范"
            },
            "使至塞上": {
                "原文": "单车欲问边,属国过居延.征蓬出汉塞,归雁入胡天.",
                "style": "雄浑壮阔",
                "imagery": "大漠,孤烟,长河,落日",
                "情感": "边塞苍茫与孤独",
                "名句": "大漠孤烟直,长河落日圆",
                "评价": "王国维评为'千古壮观'"
            },
            "送元二使安西": {
                "原文": "渭城朝雨浥轻尘,客舍青青柳色新.劝君更尽一杯酒,西出阳关无故人.",
                "style": "送别深情",
                "imagery": "朝雨,客舍,柳色,酒",
                "情感": "深情厚谊与离别悲凉",
                "评价": "古今送别诗之冠"
            },
            "鹿柴": {
                "原文": "空山不见人,但闻人语响.返景入深林,复照青苔上.",
                "style": "禅意盎然",
                "imagery": "空山,人语,深林,青苔",
                "情感": "寂静空灵禅意",
                "特色": "以声写寂,以静写幽"
            },
            "竹里馆": {
                "原文": "独坐幽篁里,弹琴复长啸.深林人不知,明月来相照.",
                "style": "禅意盎然",
                "imagery": "幽篁,弹琴,长啸,明月",
                "情感": "超然物外的隐士情怀",
                "特色": "物我两忘的极致境界"
            },
            "相思": {
                "原文": "红豆生南国,春来发几枝.愿君多采撷,此物最相思.",
                "style": "深情款款",
                "imagery": "红豆,南国,春",
                "情感": "含蓄深沉的相思之情",
                "特色": "以红豆起兴,语言浅近,情意深长"
            },
            "鸟鸣涧": {
                "原文": "人闲桂花落,夜静春山空.月出惊山鸟,时鸣春涧中.",
                "style": "动静相宜",
                "imagery": "桂花落,春山空,月出,鸟鸣",
                "情感": "寂静中的生命律动",
                "名句": "月出惊山鸟,时鸣春涧中",
                "特色": "以动写静的极致"
            },
            "终南别业": {
                "原文": "中岁颇好道,晚家南山陲.兴来每独往,胜事空自知.",
                "style": "禅意盎然",
                "imagery": "南山,独往,流水,行止",
                "情感": "随缘任运的人生哲学",
                "名句": "行到水穷处,坐看云起时",
                "评价": "禅意人生的最高境界"
            }
        }
    
    def _init_spiritual_insight(self) -> Dict[str, str]:
        return {
            "禅意核心": "行到水穷处,坐看云起时",
            "意境典范": "明月松间照,清泉石上流",
            "壮美画卷": "大漠孤烟直,长河落日圆",
            "送别深情": "劝君更尽一杯酒,西出阳关无故人",
            "相思之名": "愿君多采撷,此物最相思",
            "隐逸超脱": "独坐幽篁里,弹琴复长啸"
        }
    
    def _init_revelations(self) -> Dict[str, str]:
        return {
            "宁静致远": "在浮躁时代保持内心宁静",
            "诗意栖居": "在日常生活中发现诗意,诗意地栖居",
            "和谐共生": "人与自然的和谐,物质与精神的平衡",
            "随缘任运": "顺应自然,不强求,不执着",
            "物我两忘": "在审美中超越主客二分"
        }
    
    def _init_wangchuan(self) -> List[str]:
        """wangchuan别业二十景"""
        return [
            "孟城坳", "华子岗", "文杏馆", "斤竹岭", "鹿柴",
            "木兰柴", "茱萸泮", "宫槐陌", "临湖亭", "南垞",
            "欹湖", "柳浪", "栾家濑", "金屑泉", "白石滩",
            "北垞", "竹里馆", "辛夷坞", "漆园", "椒园"
        ]
    
    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """
        分析给定文本是否具有王维style
        
        Args:
            text: 待分析文本
            
        Returns:
            王维style分析结果
        """
        score = 0
        matched_styles = []
        matched_images = []
        
        # 禅意空灵
        if any(word in text for word in ["空", "静", "寂", "幽"]):
            score += 2
            matched_styles.append(王维style类型.禅意盎然.value)
        
        # 山水imagery
        if any(word in text for word in ["山", "水", "月", "松", "泉"]):
            score += 2
            matched_images.append("山水imagery")
        
        # 明月imagery
        if "明月" in text:
            score += 2
            matched_images.append("明月松间")
        
        # 清泉白石
        if any(word in text for word in ["清泉", "石", "流"]):
            score += 2
            matched_styles.append("清泉白石的纯净意境")
        
        # 竹林幽篁
        if any(word in text for word in ["竹", "篁", "深林"]):
            score += 2
            matched_images.append("竹林幽篁")
        
        # 送别深情
        if any(word in text for word in ["酒", "阳关", "故人", "相思"]):
            score += 2
            matched_styles.append(王维style类型.送别之情.value)
        
        # 诗中有画
        if any(word in text for word in ["大漠", "孤烟", "落日"]):
            score += 3
            matched_styles.append(王维style类型.诗中有画.value)
        
        style_ratio = min(score / 10, 1.0)
        
        return {
            "score": score,
            "style_ratio": round(style_ratio, 2),
            "is_wang_wei_style": score >= 5,
            "matched_styles": matched_styles[:3],
            "matched_images": matched_images[:3],
            "judge": "王维style浓郁" if score >= 5 else "略有王维style" if score >= 3 else "不具王维style"
        }
    
    def getrepresentative_works(self, style: Optional[str] = None) -> List[Dict]:
        """get王维representative_works"""
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
        """get王维核心spiritual_insight"""
        return self.核心spiritual_insight
    
    def get现代revelations(self) -> Dict[str, str]:
        """get王维的现代revelations"""
        return self.现代revelations
    
    def get诗歌characteristics(self) -> Dict:
        """get王维诗歌完整characteristics"""
        return {
            "style": self.诗歌characteristics.style,
            "imagery": self.诗歌characteristics.imagery,
            "修辞": self.诗歌characteristics.修辞,
            "情感": self.诗歌characteristics.情感,
            "语言": self.诗歌characteristics.语言
        }
    
    def get生平摘要(self) -> Dict:
        """get王维生平摘要"""
        return {
            "字": "摩诘",
            "号": "摩诘居士,诗佛",
            "生卒": "701年(或699年)- 761年",
            "籍贯": "河东蒲州(今山西永济),后家于蓝田wangchuan",
            "身份": "poet,画家,音乐家,书法家",
            "并称": "与孟浩然并称'王孟'",
            "地位": "诗佛,山水田园诗派之宗,文人画开创者"
        }
    
    def getwangchuan别业(self) -> List[str]:
        """getwangchuan别业二十景"""
        return self.wangchuan二十景
    
    def get李杜王对比(self) -> Dict:
        """get李白,杜甫,王维三人的对比"""
        return {
            "并称": {"李白": "诗仙", "杜甫": "诗圣", "王维": "诗佛"},
            "诗歌style": {
                "李白": "豪放飘逸,浪漫主义",
                "杜甫": "沉郁顿挫,现实主义",
                "王维": "诗中有画,禅意盎然"
            },
            "关注焦点": {
                "李白": "个人超脱与自由",
                "杜甫": "社会现实与民生",
                "王维": "内心宁静与和谐"
            },
            "哲学基础": {
                "李白": "道家逍遥",
                "杜甫": "儒家济世",
                "王维": "佛教禅宗"
            },
            "代表imagery": {
                "李白": "酒,月,剑,鹏",
                "杜甫": "黎元,秋,登高",
                "王维": "空山,明月,清泉"
            }
        }
    
    def 创作指导(self, theme: str, emotion: str) -> Dict:
        """
        提供王维style的创作指导
        
        Args:
            theme: 主题(如"山水","禅意","送别")
            emotion: 情感(如"宁静","超脱")
            
        Returns:
            创作指导
        """
        guidance = {
            "主题": theme,
            "情感": emotion,
            "推荐imagery": [],
            "修辞手法": [],
            "语言style": "纯净洗练,浑然天成",
            "参考作品": []
        }
        
        # 根据主题推荐imagery
        if theme in ["山水", "自然", "隐居"]:
            guidance["推荐imagery"] = ["空山", "明月", "清泉", "松间"]
            guidance["修辞手法"] = ["以动写静", "色彩渲染"]
            guidance["参考作品"] = ["<山居秋暝>", "<鸟鸣涧>"]
        elif theme in ["禅意", "悟道", "超脱"]:
            guidance["推荐imagery"] = ["云", "水", "深林", "青苔"]
            guidance["语言style"] = "空灵寂静,意在言外"
            guidance["参考作品"] = ["<鹿柴>", "<终南别业>"]
        elif theme in ["送别", "相思", "友情"]:
            guidance["推荐imagery"] = ["酒", "阳关", "故人", "柳色"]
            guidance["情感基调"] = "含蓄深情,意在言外"
            guidance["参考作品"] = ["<送元二使安西>", "<相思>"]
        elif theme in ["边塞", "壮美"]:
            guidance["推荐imagery"] = ["大漠", "孤烟", "长河", "落日"]
            guidance["修辞手法"] = ["白描", "对仗"]
            guidance["参考作品"] = ["<使至塞上>"]
        
        return guidance

# 测试函数
# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
