# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 标准系统岗位
从 _court_positions.py 提取，V1.0.0
"""
from typing import List
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch


def build_standard_positions() -> List:
    """标准系统岗位（法家主导）"""
    positions = []

    # 一品
    positions += _zheng_cong_pair(
        "BZ_1_01", "大理寺卿", "标准系统", pin_level=1,
        system_type_str="standard",
        domain="国家法律与司法最高",
        dispatch_path_prefix="皇帝→大理寺卿",
        suitable_schools=["法家", "儒家"],
        description_prefix="国家司法最高决策",
        sage_type_str="theorist",
    )

    # 二品
    positions += _zheng_cong_pair(
        "BZ_2_01", "刑部尚书", "标准系统", pin_level=2,
        system_type_str="standard",
        domain="刑法与治安",
        dispatch_path_prefix="大理寺卿→刑部尚书",
        suitable_schools=["法家"],
        description_prefix="刑法与治安",
    )

    positions += _zheng_cong_pair(
        "BZ_2_02", "御史大夫", "标准系统", pin_level=2,
        system_type_str="standard",
        domain="监察与弹劾",
        dispatch_path_prefix="大理寺卿→御史大夫",
        suitable_schools=["法家", "儒家"],
        description_prefix="监察百官",
    )

    # 三品
    positions += _zheng_cong_pair(
        "BZ_3_01", "廷尉", "标准系统", pin_level=3,
        system_type_str="standard",
        domain="司法审判",
        dispatch_path_prefix="大理寺卿→廷尉",
        suitable_schools=["法家"],
        description_prefix="司法审判",
    )

    # 四品
    positions += _zheng_cong_pair(
        "BZ_4_01", "监察御史", "标准系统", pin_level=4,
        system_type_str="standard",
        domain="地方监察",
        dispatch_path_prefix="御史大夫→监察御史",
        suitable_schools=["法家", "儒家"],
        description_prefix="地方监察",
    )

    # 专员（七品）
    positions += _specialist_batch("BZ_P7", "标准系统", pin_level=7, items=[
        ("法典编纂专员", "法律编纂、法典修订", ["法家"]),
        ("判例研究员", "判例收集、司法研究", ["法家", "儒家"]),
        ("监察专员", "地方监察、百官考评", ["法家"]),
        ("律法教员", "法律教学、人才培养", ["法家", "教育家"]),
    ])

    return positions
