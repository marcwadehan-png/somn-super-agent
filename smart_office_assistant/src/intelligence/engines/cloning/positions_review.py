# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 审核系统岗位
从 _court_positions.py 提取，V4.2.0
"""
from typing import List
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch


def build_review_positions() -> List:
    """审核系统岗位（独立监察）"""
    positions = []

    # 一品
    positions += _zheng_cong_pair(
        "SH_1_01", "太子太师", "审核系统", pin_level=1,
        system_type_str="review",
        domain="最高审核与监察",
        dispatch_path_prefix="皇帝→太子太师",
        suitable_schools=["儒家", "法家"],
        description_prefix="最高审核决策",
        sage_type_str="dual_type",
    )

    # 二品
    positions += _zheng_cong_pair(
        "SH_2_01", "谏议大夫", "审核系统", pin_level=2,
        system_type_str="review",
        domain="谏言与规劝",
        dispatch_path_prefix="太子太师→谏议大夫",
        suitable_schools=["儒家", "思想家"],
        description_prefix="谏言规劝",
    )

    # 三品
    positions += _zheng_cong_pair(
        "SH_3_01", "给事中", "审核系统", pin_level=3,
        system_type_str="review",
        domain="封驳与审核",
        dispatch_path_prefix="太子太师→给事中",
        suitable_schools=["儒家", "法家"],
        description_prefix="封驳审核",
    )

    # 四品
    positions += _zheng_cong_pair(
        "SH_4_01", "拾遗", "审核系统", pin_level=4,
        system_type_str="review",
        domain="拾遗补缺、进谏",
        dispatch_path_prefix="谏议大夫→拾遗",
        suitable_schools=["儒家", "史家"],
        description_prefix="拾遗进谏",
    )

    # 专员（七品）
    positions += _specialist_batch("SH_P7", "审核系统", pin_level=7, items=[
        ("审核专员", "文书审核、合规检查", ["法家", "儒家"]),
        ("监察专员", "行为监察、违规调查", ["法家"]),
        ("谏言专员", "意见收集、谏言整理", ["儒家", "思想家"]),
    ])

    return positions
