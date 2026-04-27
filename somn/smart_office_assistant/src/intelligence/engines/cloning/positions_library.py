# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 皇家藏书阁岗位
从 _court_positions.py 提取，V1.0.0
"""
from typing import List
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch


def build_library_positions() -> List:
    """皇家藏书阁岗位（学术收藏）"""
    positions = []

    # 藏书阁最高负责人（正值从三品）
    positions += _zheng_cong_pair(
        "TS_3_01", "翰林院掌院学士", "皇家藏书阁", pin_level=3,
        system_type_str="library",
        domain="藏书管理与学术收藏",
        dispatch_path_prefix="皇帝→翰林院掌院学士",
        suitable_schools=["儒家", "史家", "文学家"],
        description_prefix="藏书阁管理",
        sage_type_str="theorist",
    )

    # 四品
    positions += _zheng_cong_pair(
        "TS_4_01", "秘书监", "皇家藏书阁", pin_level=4,
        system_type_str="library",
        domain="秘籍与档案管理",
        dispatch_path_prefix="翰林院掌院学士→秘书监",
        suitable_schools=["儒家", "史家"],
        description_prefix="秘籍档案管理",
    )

    # 五品
    positions += _zheng_cong_pair(
        "TS_5_01", "校书郎", "皇家藏书阁", pin_level=5,
        system_type_str="library",
        domain="书籍校勘与编目",
        dispatch_path_prefix="秘书监→校书郎",
        suitable_schools=["儒家", "史家", "文学家"],
        description_prefix="书籍校勘",
    )

    # 六品
    positions += _zheng_cong_pair(
        "TS_6_01", "太史令", "皇家藏书阁", pin_level=6,
        system_type_str="library",
        domain="史书编撰与记录",
        dispatch_path_prefix="秘书监→太史令",
        suitable_schools=["史家", "儒家"],
        description_prefix="史书编撰",
    )

    # 专员（七品）
    positions += _specialist_batch("TS_P7", "皇家藏书阁", pin_level=7, items=[
        ("典籍保管专员", "典籍保管、藏书整理", ["儒家", "史家"]),
        ("文书抄写专员", "经典抄写、文书誊录", ["儒家", "文学家"]),
        ("目录编撰专员", "藏书目录、索引编制", ["儒家", "史家"]),
        ("版本校勘专员", "版本比对、错漏校正", ["儒家", "科学家"]),
    ])

    return positions
