# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 文治系统岗位
从 _court_positions.py 提取，V4.2.0
"""
from typing import List
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch


def build_wenzhi_positions() -> List:
    """文治系统岗位（儒家主导）"""
    positions = []

    # 一品
    positions += _zheng_cong_pair(
        "WZ_1_01", "文渊阁大学士", "文治系统", pin_level=1,
        system_type_str="wenzhi",
        domain="文治最高决策与学术总管",
        dispatch_path_prefix="皇帝→文渊阁大学士",
        suitable_schools=["儒家", "史家", "文学家"],
        description_prefix="文治最高决策",
        sage_type_str="theorist",
    )

    # 二品
    positions += _zheng_cong_pair(
        "WZ_2_01", "东阁大学士", "文治系统", pin_level=2,
        system_type_str="wenzhi",
        domain="东阁学术与文书",
        dispatch_path_prefix="文渊阁大学士→东阁大学士",
        suitable_schools=["儒家", "文学家"],
        description_prefix="东阁学术管理",
    )

    positions += _zheng_cong_pair(
        "WZ_2_02", "国子监祭酒", "文治系统", pin_level=2,
        system_type_str="wenzhi",
        domain="国家教育与人才培养",
        dispatch_path_prefix="文渊阁大学士→国子监祭酒",
        suitable_schools=["儒家", "教育家"],
        description_prefix="国家教育管理",
    )

    # 三品
    positions += _zheng_cong_pair(
        "WZ_3_01", "翰林院学士", "文治系统", pin_level=3,
        system_type_str="wenzhi",
        domain="翰林院学术与文书",
        dispatch_path_prefix="东阁大学士→翰林院学士",
        suitable_schools=["儒家", "文学家", "史家"],
        description_prefix="翰林院学术",
    )

    positions += _zheng_cong_pair(
        "WZ_3_02", "太学博士", "文治系统", pin_level=3,
        system_type_str="wenzhi",
        domain="太学教学与经学",
        dispatch_path_prefix="国子监祭酒→太学博士",
        suitable_schools=["儒家", "教育家"],
        description_prefix="太学教学",
    )

    # 四品
    positions += _zheng_cong_pair(
        "WZ_4_01", "秘书监", "文治系统", pin_level=4,
        system_type_str="wenzhi",
        domain="宫廷秘籍与档案",
        dispatch_path_prefix="翰林院学士→秘书监",
        suitable_schools=["儒家", "史家"],
        description_prefix="秘籍档案管理",
    )

    # 五品
    positions += _zheng_cong_pair(
        "WZ_5_01", "国史馆修撰", "文治系统", pin_level=5,
        system_type_str="wenzhi",
        domain="国史编撰与修订",
        dispatch_path_prefix="翰林院学士→国史馆修撰",
        suitable_schools=["史家", "儒家"],
        description_prefix="国史编撰",
    )

    # 六品
    positions += _zheng_cong_pair(
        "WZ_6_01", "钦天监博士", "文治系统", pin_level=6,
        system_type_str="wenzhi",
        domain="天文历法与天象记录",
        dispatch_path_prefix="秘书监→钦天监博士",
        suitable_schools=["科学家", "儒家"],
        description_prefix="天文历法",
    )

    # 专员（七品）
    positions += _specialist_batch("WZ_P7", "文治系统", pin_level=7, items=[
        ("经学专员", "经义注疏、典籍校勘", ["儒家"]),
        ("史学专员", "史书编撰、史料整理", ["史家"]),
        ("文学专员", "诏令起草、文书撰写", ["文学家", "儒家"]),
        ("教育专员", "地方教育、生员考核", ["儒家", "教育家"]),
    ])

    return positions
