# -*- coding: utf-8 -*-
"""
朝廷岗位体系 - 皇家系统岗位
从 _court_positions.py 提取，V4.2.0
"""
from typing import List
from .court_helpers import _p, _zheng_cong_pair, _specialist_batch


def build_royal_positions() -> List:
    """皇家系统岗位（最高决策层）"""
    positions = []

    # 王爵（全局最高，1人）
    positions.append(_p(
        id="HJ_WJ_01", name="太师·王爵", department="皇家",
        pin=None, nobility_val=0,  # WANGJUE = 0
        position_type_str="supreme_single", capacity=1,
        system_type_str="royal",
        si_name="孔子",
        domain="全局最高决策与最终裁决",
        dispatch_path="皇帝→太师·王爵→孔子",
        suitable_schools=["儒家", "道家", "思想家", "哲学家"],
        description="全局最高决策人，王爵独裁，拥有最终裁决权，由孔子担任",
        sage_type_str="theorist",
    ))

    # 公爵（副最高，1人）
    positions.append(_p(
        id="HJ_GJ_01", name="太傅·公爵", department="皇家",
        pin=None, nobility_val=1,  # GONGJUE = 1
        position_type_str="supreme_single", capacity=1,
        system_type_str="royal",
        domain="全局战略与次高决策",
        dispatch_path="皇帝→太傅·公爵",
        suitable_schools=["儒家", "道家", "兵家", "法家"],
        description="公爵，全局战略决策，决策权大于一品，由孟子担任",
        sage_type_str="theorist",
    ))

    # 侯爵
    positions.append(_p(
        id="HJ_HJ_01", name="太保·侯爵", department="皇家",
        pin=None, nobility_val=2,  # HOUJUE = 2
        position_type_str="execution", capacity=1,
        system_type_str="royal",
        domain="战略顾问与皇家事务",
        dispatch_path="皇帝→太保·侯爵",
        suitable_schools=["儒家", "道家", "佛家", "思想家"],
        description="侯爵，品秩等同一品，决策权介于正一品和正二品之间，由荀子担任",
        sage_type_str="dual_type",
    ))

    # 伯爵
    positions.append(_p(
        id="HJ_BJ_01", name="伯爵·皇家侍读", department="皇家",
        pin=None, nobility_val=3,  # BOJUE = 3
        position_type_str="execution", capacity=1,
        system_type_str="royal",
        domain="皇家文书与侍读顾问",
        dispatch_path="皇帝→伯爵·皇家侍读",
        suitable_schools=["儒家", "文学家", "思想家"],
        description="伯爵，品秩等同三品，决策权介于正三品和正二品之间，由郑玄担任",
        sage_type_str="theorist",
    ))

    # 中枢管理层（正从各品，一正一副）
    positions += _zheng_cong_pair(
        "HJ_2_01", "枢密使", "皇家", pin_level=2,
        system_type_str="royal",
        domain="中枢机密与信息总管",
        dispatch_path_prefix="皇帝→枢密使",
        suitable_schools=["兵家", "纵横家", "法家"],
        description_prefix="中枢机密管理",
    )

    positions += _zheng_cong_pair(
        "HJ_3_01", "翰林院掌院", "皇家", pin_level=3,
        system_type_str="royal",
        domain="翰林院学术总管",
        dispatch_path_prefix="皇帝→翰林院掌院",
        suitable_schools=["儒家", "文学家", "史家", "哲学家"],
        description_prefix="翰林院学术管理",
    )

    positions += _zheng_cong_pair(
        "HJ_4_01", "通政使司", "皇家", pin_level=4,
        system_type_str="royal",
        domain="内外奏章与信息通传",
        dispatch_path_prefix="皇帝→通政使司",
        suitable_schools=["儒家", "法家", "兵家"],
        description_prefix="奏章通传管理",
    )

    positions += _zheng_cong_pair(
        "HJ_5_01", "詹事府", "皇家", pin_level=5,
        system_type_str="royal",
        domain="皇家教育与辅导",
        dispatch_path_prefix="皇帝→詹事府",
        suitable_schools=["儒家", "教育家", "道家"],
        description_prefix="皇家教育管理",
    )

    positions += _zheng_cong_pair(
        "HJ_6_01", "太仆寺", "皇家", pin_level=6,
        system_type_str="royal",
        domain="皇家仪仗与车马",
        dispatch_path_prefix="皇帝→太仆寺",
        suitable_schools=["儒家", "法家"],
        description_prefix="皇家仪仗管理",
    )

    # 专员
    positions += _specialist_batch("HJ_P7", "皇家", pin_level=7, items=[
        ("皇家文书专员", "经典抄写、文献校对、诏令起草", ["儒家", "文学家"]),
        ("经学研究员", "经典注疏、训诂研究、经义考辨", ["儒家", "思想家"]),
        ("礼仪典制专员", "朝廷礼仪、祭祀典制、文书格式", ["儒家", "思想家"]),
        ("史籍校勘专员", "史书校勘、文献考证、版本比对", ["史家", "儒家"]),
        ("文字训诂专员", "文字学研究、音韵考据、方言记录", ["儒家", "科学家"]),
        ("皇家教育专员", "皇子教育、学术传承、礼仪教学", ["儒家", "教育家", "道家"]),
        ("侍卫专员", "皇家安全、军事护卫、战时征调", ["兵家", "法家"]),
        ("天文历法专员", "天文观测、历法推算、星象记录", ["科学家", "数学"]),
    ])

    return positions
