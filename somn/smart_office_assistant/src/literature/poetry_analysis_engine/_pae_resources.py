# -*- coding: utf-8 -*-
"""诗词分析引擎 - 资源加载模块"""
from typing import Dict, Any, List

__all__ = [
    'load_all',
]

class PoetryResourceLoader:
    """诗词资源加载器"""

    def __init__(self):
        self.rhyme_rules = None
        self.imagery_library = None
        self.theme_library = None
        self.author_style_library = None

    def load_all(self) -> Dict[str, Any]:
        """加载所有诗词资源"""
        return {
            "rhyme_rules": self._load_rhyme_rules(),
            "imagery_library": self._load_imagery_library(),
            "theme_library": self._load_theme_library(),
            "author_style_library": self._load_author_style_library()
        }

    def _load_rhyme_rules(self) -> Dict[str, List[str]]:
        """加载韵律规则"""
        return {
            "平水韵": ["一东", "二冬", "三江", "四支", "五微", "六鱼", "七虞", "八齐", "九佳", "十灰"],
            "词林正韵": ["第一部", "第二部", "第三部", "第四部", "第五部", "第六部", "第七部", "第八部", "第九部", "第十部"],
            "现代诗韵": ["a韵", "i韵", "u韵", "e韵", "o韵", "ai韵", "ei韵", "ao韵", "ou韵"]
        }

    def _load_imagery_library(self) -> Dict[str, Dict[str, Any]]:
        """加载imagery_database"""
        return {
            "自然imagery": {
                "月亮": {"情感": ["思乡", "怀人", "孤独"], "频率": 0.85},
                "青山": {"情感": ["隐逸", "旷达", "永恒"], "频率": 0.72},
                "流水": {"情感": ["时光流逝", "离别", "愁绪"], "频率": 0.68},
                "春花": {"情感": ["美好", "短暂", "珍惜"], "频率": 0.61},
                "秋叶": {"情感": ["萧瑟", "离别", "衰老"], "频率": 0.57}
            },
            "人文imagery": {
                "酒": {"情感": ["豪放", "忧愁", "友情"], "频率": 0.79},
                "剑": {"情感": ["壮志", "豪情", "侠义"], "频率": 0.65},
                "舟": {"情感": ["漂泊", "归隐", "旅途"], "频率": 0.58},
                "琴": {"情感": ["雅致", "知音", "孤独"], "频率": 0.53}
            }
        }

    def _load_theme_library(self) -> Dict[str, List[str]]:
        """加载主题分类库"""
        return {
            "爱国": ["报国", "忧国", "抗敌", "壮志"],
            "山水": ["田园", "隐逸", "自然", "风景"],
            "离别": ["送别", "思念", "怀人", "友情"],
            "爱情": ["相思", "闺怨", "缠绵", "忠贞"],
            "咏史": ["怀古", "感慨", "兴亡", "沧桑"],
            "哲理": ["人生", "感悟", "智慧", "禅意"]
        }

    def _load_author_style_library(self) -> Dict[str, Dict[str, Any]]:
        """加载作者style库"""
        return {
            "李白": {
                "style": "豪放",
                "features": ["豪放", "浪漫", "想象丰富", "语言夸张"],
                "rhyme_preference": "自由奔放",
                "imagery_preference": ["月亮", "酒", "剑", "仙山"]
            },
            "杜甫": {
                "style": "雄浑",
                "features": ["雄浑", "沉郁", "写实", "社会关怀"],
                "rhyme_preference": "严谨工整",
                "imagery_preference": ["战乱", "民生", "历史", "沧桑"]
            },
            "王维": {
                "style": "清新",
                "features": ["清新", "淡雅", "禅意", "诗画一体"],
                "rhyme_preference": "自然流畅",
                "imagery_preference": ["山水", "竹林", "禅寺", "明月"]
            },
            "李清照": {
                "style": "婉约",
                "features": ["婉约", "细腻", "深情", "女性视角"],
                "rhyme_preference": "精巧婉转",
                "imagery_preference": ["黄花", "梧桐", "细雨", "帘幕"]
            }
        }
