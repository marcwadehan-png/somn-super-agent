# -*- coding: utf-8 -*-
"""
蒋捷深化引擎 - 宋末四大家之一
v8.2.0

蒋捷(1245-1305),字胜欲
文学地位:宋末四大家之一
作品风格:悲壮苍凉,时代悲歌
代表名句:少年听雨歌楼上,红烛昏罗帐.壮年听雨客舟中.而今听雨僧庐下
"""

from typing import Dict, List, Optional, Any
from enum import Enum

class 蒋捷style类型(Enum):
    """蒋捷作品风格分类"""
    悲壮苍凉 = "悲壮苍凉"
    时代悲歌 = "时代悲歌"
    听雨意境 = "听雨意境"
    故国之思 = "故国之思"

class 蒋捷意象类型(Enum):
    """蒋捷常用意象"""
    听雨 = "听雨"
    少年 = "少年"
    壮年 = "壮年"
    僧庐 = "僧庐"
    雨声 = "雨声"

class 蒋捷代表作品(Enum):
    """蒋捷代表作品"""
    虞美人·听雨 = "虞美人·听雨"
    一剪梅·舟过吴江 = "一剪梅·舟过吴江"
    贺新郎·梦遇 = "贺新郎·梦遇"

class 蒋捷深化引擎:
    """蒋捷诗词深化分析引擎 v8.2.0"""

    VERSION = "6.2.0"

    def __init__(self):
        self.诗歌characteristics = self._init_characteristics()
        self.经典famous_poems = self._init_famous_poems()
        self.核心spiritual_insight = self._init_spiritual_insight()
        self.现代revelations = self._init_revelations()

    def _init_characteristics(self) -> Dict:
        return {
            "style": [
        "悲壮苍凉",
        "时代悲歌",
        "听雨意境",
        "故国之思"
            ],
            "imagery": [
        "听雨",
        "少年",
        "壮年",
        "僧庐",
        "雨声"
            ],
            "手法": [
                "意象独特:听雨",
                "情景交融:借景抒情",
                "语言优美:清新自然",
                "意境深远:耐人寻味"
            ],
            "情感": [
                "悲壮苍凉",
                "时代悲歌",
                "听雨意境",
                "故国之思"
            ],
            "语言": "悲壮苍凉、时代悲歌"
        }
    def _init_famous_poems(self) -> Dict[str, Dict]:
        return {
            "虞美人·听雨": {
                "原文": "少年听雨歌楼上,红烛昏罗帐.壮年听雨客舟中.而今听雨僧庐下",
                "类型": "词",
                "style": "悲壮苍凉",
                "imagery": "听雨,少年,壮年",
                "情感": "时代悲歌",
                "赏析": "宋末四大家之一"
            },
            "一剪梅·舟过吴江": {
                "原文": "少年听雨歌楼上,红烛昏罗帐.壮年听雨客舟中.而今听雨僧庐下",
                "类型": "词",
                "style": "听雨意境",
                "imagery": "壮年,僧庐,雨声",
                "情感": "悲壮苍凉",
                "赏析": "代表作"
            }
        }

    def _init_spiritual_insight(self) -> List[str]:
        return [
            "[悲壮苍凉]少年听雨歌楼上,红烛昏罗帐.壮年听雨客舟中.而今听雨僧庐下",
            "[时代悲歌]宋末四大家之一",
            "[听雨]宋末四大家之一",
            "[听雨意境]虞美人·听雨",
            "[少年]悲壮苍凉,时代悲歌"
        ]

    def _init_revelations(self) -> Dict[str, List[str]]:
        return {

        "南宋末": [
            "代表作品:虞美人·听雨",
            "艺术特点:悲壮苍凉",
            "核心意象:听雨"
        ],
        "艺术成就": [
            "文学地位:宋末四大家之一",
            "代表风格:悲壮苍凉",
            "名句:少年听雨歌楼上,红烛昏罗帐.壮年听雨客舟"
        ],
        "人生智慧": [
            "宋末四大家之一",
            "蒋捷(1245-1305),字胜欲"
        ]
        }

    def 分析wenben(self, text: str) -> Dict[str, Any]:
        """分析给定文本的蒋捷作品风格"""
        score = 0
        matched_styles = []
        matched_images = []

        style_keywords = [
            "悲壮苍凉",
            "时代悲歌",
            "听雨意境"
        ]
        for kw in style_keywords:
            if kw in text:
                score += 3
                if kw not in matched_styles:
                    matched_styles.append(kw)

        image_keywords = [
            "听雨",
            "少年",
            "壮年",
            "僧庐",
            "雨声"
        ]
        for img in image_keywords:
            if img in text:
                if img not in matched_images:
                    matched_images.append(img)

        return {
            "score": score,
            "matched_styles": matched_styles,
            "matched_images": matched_images,
            "judge": "具有明显的蒋捷风格特征" if score >= 5 else "具有一定的蒋捷风格痕迹" if score >= 3 else "较少蒋捷风格特征",
            "作者": "蒋捷",
            "称号": "胜欲",
            "时代": "南宋末"
        }

# 全局实例
蒋捷引擎 = 蒋捷深化引擎()
__all__ = ['蒋捷style类型', '蒋捷意象类型', '蒋捷代表作品']
