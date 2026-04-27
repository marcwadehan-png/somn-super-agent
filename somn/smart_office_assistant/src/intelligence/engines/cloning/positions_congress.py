# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 七人代表大会岗位
从 _court_positions.py 提取，V1.0.0
"""
from typing import List
from .court_helpers import _p


def build_congress_positions() -> List:
    """七人代表大会岗位（最高决策机构）"""
    positions = []

    # 七人代表大会常务委员（正值从二品，7个席位）
    pin_zheng = 5  # 二品正
    pin_cong = 6   # 二品从

    names = ["儒家委员", "道家委员", "法家委员", "墨家委员", "兵家委员", "史家委员", "科学家委员"]
    for i, name in enumerate(names):
        # 正值
        positions.append(_p(
            id=f"QY_{i+1:02d}_Z",
            name=f"七人代表大会常务委员（{name}·正）",
            department="七人代表大会",
            pin=pin_zheng,
            position_type_str="management",
            capacity=1,
            is_zheng=True,
            system_type_str="congress",
            domain=f"七人代表大会决策（{name}）",
            dispatch_path=f"皇帝→七人代表大会→常务委员（{name}）",
            suitable_schools=[name.replace("委员", "")],
            description=f"七人代表大会常务委员，{name}，正值",
            sage_type_str="theorist",
        ))

        # 从值
        positions.append(_p(
            id=f"QY_{i+1:02d}_C",
            name=f"七人代表大会常务委员（{name}·从）",
            department="七人代表大会",
            pin=pin_cong,
            position_type_str="management",
            capacity=1,
            is_zheng=False,
            system_type_str="congress",
            domain=f"七人代表大会决策（{name}）",
            dispatch_path=f"皇帝→七人代表大会→常务委员（{name}）",
            suitable_schools=[name.replace("委员", "")],
            description=f"七人代表大会常务委员，{name}，从值",
            sage_type_str="theorist",
        ))

    # 七人代表大会秘书长（正值从三品）
    positions += [_p(
        id="QY_SEC_Z",
        name="七人代表大会秘书长（正）",
        department="七人代表大会",
        pin=9,  # 三品正
        position_type_str="management",
        capacity=1,
        is_zheng=True,
        system_type_str="congress",
        domain="七人代表大会秘书与协调",
        dispatch_path="皇帝→七人代表大会→秘书长",
        suitable_schools=["儒家", "法家"],
        description="七人代表大会秘书长，正值",
        sage_type_str="dual_type",
    ), _p(
        id="QY_SEC_C",
        name="七人代表大会秘书长（从）",
        department="七人代表大会",
        pin=10,  # 三品从
        position_type_str="management",
        capacity=1,
        is_zheng=False,
        system_type_str="congress",
        domain="七人代表大会秘书与协调",
        dispatch_path="皇帝→七人代表大会→秘书长",
        suitable_schools=["儒家", "法家"],
        description="七人代表大会秘书长，从值",
        sage_type_str="dual_type",
    )]

    return positions
