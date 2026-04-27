"""
三十六计枚举定义
"""

from enum import Enum

class StrategyCategory(Enum):
    """策略类别"""
    VICTORY = "胜战计"      # 优势时策略
    CONFRONTATION = "敌战计"  # 对峙时策略
    ATTACK = "攻战计"       # 进攻时策略
    CHAOS = "混战计"       # 混乱时策略
    MERGE = "并战计"       # 兼并时策略
    RETREAT = "败战计"      # 劣势时策略

class StrategyType(Enum):
    """具体计谋"""
    # 胜战计
    MAN_TIAN_GUO_HAI = "瞒天过海"
    WEI_WE_JIU_ZHAO = "围魏救赵"
    JIE_DAO_SHA_REN = "借刀杀人"
    YI_YI_DAI_LAO = "以逸待劳"
    CHEN_HUO_DA_JIE = "趁火打劫"
    SHENG_DONG_JI_XI = "声东击西"
    
    # 敌战计
    WU_ZHONG_SHENG_YOU = "无中生有"
    AN_DU_CHEN_CANG = "暗渡陈仓"
    GE_AN_GUAN_HUO = "隔岸观火"
    XIAO_LI_CANG_DAO = "笑里藏刀"
    LI_DAI_TAO_JIANG = "李代桃僵"
    SHUN_SHOU_QIAN_YANG = "顺手牵羊"
    
    # 攻战计
    DA_CAO_JING_SHE = "打草惊蛇"
    JIE_SHI_HUAN_HUN = "借尸还魂"
    DIAO_HU_LI_SHAN = "调虎离山"
    YU_QIN_GU_ZONG = "欲擒故纵"
    PAO_ZHUAN_YIN_YU = "抛砖引玉"
    QIN_ZEI_QIN_WANG = "擒贼擒王"
    
    # 混战计
    FU_DI_CHOU_XIN = "釜底抽薪"
    HUN_SHUI_MO_YU = "浑水摸鱼"
    JIN_CHAN_TUO_QIAO = "金蝉脱壳"
    GUAN_MEN_ZHUO_ZEI = "关门捉贼"
    YUAN_JIAO_JIN_GONG = "远交近攻"
    JIA_TU_DAI_GUO = "假途待虢"
    
    # 并战计
    TOU_LIANG_HUAN_ZHU = "偷梁换柱"
    ZHI_SANG_MA_HUAI = "指桑骂槐"
    JIA_CHI_BU_DIAN = "假痴不癫"
    SHANG_WU_CHOU_TI = "上屋抽梯"
    SHU_SHANG_KAI_HUA = "树上开花"
    FAN_KE_WEI_ZHU = "反客为主"
    
    # 败战计
    MEI_REN_JI = "美人计"
    KONG_CHENG_JI = "空城计"
    FAN_JIAN_JI = "反间计"
    KU_ROU_JI = "苦肉计"
    LIAN_HUAN_JI = "连环计"
    ZOU_WEI_SHANG_JI = "走为上计"
