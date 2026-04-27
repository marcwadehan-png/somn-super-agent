"""
__all__ = [
    'attributes',
    'bagua_ref',
    'body_relation',
    'color',
    'definition',
    'direction',
    'examples',
    'function',
    'get_number',
    'get_position_meaning',
    'interpretation',
    'meaning',
    'name',
    'nature',
    'note',
    'numbers',
    'organ',
    'principle',
    'quote',
    'season',
    'time',
    'title',
    'verify_magic_sum',
    'virtue',
    'wisdom',
    'yy_name',
    'yyp_name',
]

道家枚举与数据结构模块
从 dao_wisdom_core.py 提取的枚举定义和dataclass
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

# ============================================================
# 道德经核心章节精选
# ============================================================

class DaoDeJingCore(Enum):
    """道德经核心章节"""
    # 第一层次:宇宙本体论
    CHAPTER_1 = ("第一章", "道可道,非常道;名可名,非常名",
                 "宇宙本源不可言说,无名天地之始,有名万物之母")
    CHAPTER_4 = ("第四章", "道冲而用之或不盈",
                 "道空虚而无形,但作用无穷")
    CHAPTER_6 = ("第六章", "谷神不死,是谓玄牝",
                 "道如虚空永生,是万物的根源")
    CHAPTER_14 = ("第十四章", "视之不见名曰夷,听之不闻名曰希",
                   "道超越感官,无法感知")
    CHAPTER_21 = ("第二十一章", "孔德之容,惟道是从",
                   "大德的形态,完全跟随道")
    CHAPTER_25 = ("第二十五章", "人法地,地法天,天法道,道法自然",
                   "道以自然为法则")

    # 第二层次:治国理政
    CHAPTER_3 = ("第三章", "不尚贤,使民不争",
                 "不崇尚贤才,使人民不争夺")
    CHAPTER_5 = ("第五章", "天地不仁,以万物为刍狗",
                 "天地无所偏爱,一视同仁")
    CHAPTER_17 = ("第十七章", "太上,下知有之",
                   "最高明的统治,人民只知道他的存在")
    CHAPTER_57 = ("第五十七章", "以正治国,以奇用兵",
                   "以正道治国,以奇计用兵")
    CHAPTER_60 = ("第六十章", "治大国若烹小鲜",
                   "治理大国如同煎小鱼,不可折腾")

    # 第三层次:修身智慧
    CHAPTER_8 = ("第八章", "上善若水",
                 "最高的善如同水一般")
    CHAPTER_12 = ("第十二章", "五色令人目盲",
                   "五色使人眼瞎,倡导返璞归真")
    CHAPTER_16 = ("第十六章", "致虚极,守静笃",
                   "达到虚空的极致,保持内心的宁静")
    CHAPTER_19 = ("第十九章", "绝圣弃智,民利百倍",
                   "抛弃聪明才智,人民得利百倍")
    CHAPTER_22 = ("第二十二章", "曲则全,枉则直",
                   "委曲反而能保全,弯曲反而能伸直")
    CHAPTER_28 = ("第二十八章", "知其雄,守其雌",
                   "知道雄强,却守住雌柔")

    # 第四层次:军事外交
    CHAPTER_30 = ("第三十章", "以道佐人主,不以兵强天下",
                   "用道辅佐君主,不靠武力逞强天下")
    CHAPTER_31 = ("第三十一章", "夫佳兵者,不祥之器",
                   "兵器是不吉祥的器物")
    CHAPTER_69 = ("第六十九章", "用兵有言:吾不敢为主而为客",
                   "用兵者说:我不敢主动进攻而宁愿防守")

    # 第五层次:处世哲学
    CHAPTER_2 = ("第二章", "天下皆知美之为美,斯恶已",
                 "天下都知道美之所以为美,丑的观念就产生了")
    CHAPTER_9 = ("第九章", "功遂身退,天之道",
                 "功成身退,是天的法则")
    CHAPTER_13 = ("第十三章", "宠辱若惊,贵大患若身",
                   "得宠和受辱都令人惊慌,把大患看得如同生命一样重要")
    CHAPTER_36 = ("第三十六章", "鱼不可脱于渊,国之利器不可以示人",
                   "鱼不能离开深渊,国家的利器不能展示给人")
    CHAPTER_38 = ("第三十八章", "上德不德,是以有德;下德不失德,是以无德",
                   "上德之人不刻意追求德,因此真正有德;下德之人刻意保持德,因此反而无德")
    CHAPTER_39 = ("第三十九章", "昔之得一者,天得一以清,地得一以宁",
                   "自古得到道的:天得到道而清明,地得到道而安宁")
    CHAPTER_41 = ("第四十一章", "大器晚成,大音希声,大象无形",
                   "大器是慢慢做成的,大音是听不到声音的,大像是没有形状的")
    CHAPTER_44 = ("第四十四章", "名与身孰亲?身与货孰多?",
                   "名声和身体哪个更亲近?身体和财货哪个更重要?")
    CHAPTER_45 = ("第四十五章", "大成若缺,其用不弊;大盈若冲,其用不穷",
                   "最完满的东西好像有欠缺,但它的作用不会衰竭")
    CHAPTER_46 = ("第四十六章", "祸莫大于不知足,咎莫大于欲得",
                   "祸患没有大于不知足的,罪过没有大于贪得无厌的")
    CHAPTER_47 = ("第四十七章", "不出户,知天下;不窥牖,见天道",
                   "不出门就能知道天下事,不望窗外就能看见天道规律")
    CHAPTER_48 = ("第四十八章", "为学日益,为道日损",
                   "求学一天比一天增加,求道一天比一天减少")
    CHAPTER_49 = ("第四十九章", "圣人无常心,以百姓心为心",
                   "圣人没有固定的心意,以百姓的心意为心意")
    CHAPTER_58 = ("第五十八章", "祸兮,福之所倚;福兮,祸之所伏",
                   "灾祸啊,幸福倚靠在它旁边;幸福啊,灾祸藏在它里面")
    CHAPTER_67 = ("第六十七章", "我有三宝,持而保之:一曰慈,二曰俭,三曰不敢为天下先",
                   "我有三件宝贝,保持而珍视:第一是慈爱,第二是节俭,第三是不敢走在天下人的前面")
    CHAPTER_63 = ("第六十三章", "为无为,事无事,味无味",
                   "以无为的态度去作为,以无事的方式去做事,以无味作为滋味")
    CHAPTER_64 = ("第六十四章", "其安易持,其未兆易谋,其脆易泮,其微易散",
                   "局面安稳时容易持守,事变没有迹象时容易图谋")
    CHAPTER_68 = ("第六十八章", "善为士者不武,善战者不怒,善胜敌者不与",
                   "善于做士的不逞勇武,善于作战的不轻易发怒,善于战胜敌人的不与敌正面交锋")

    # 第六层次:最高智慧
    CHAPTER_40 = ("第四十章", "反者道之动,弱者道之用",
                   "道的运动是循环往复的,道的作用是柔弱的")
    CHAPTER_43 = ("第四十三章", "天下之至柔,驰骋天下之至坚",
                   "天下最柔弱的东西,能在天下最坚硬的东西中穿行")
    CHAPTER_76 = ("第七十六章", "人之生也柔弱,其死也坚强",
                   "人活着时身体柔弱,死了就变得坚硬")
    CHAPTER_78 = ("第七十八章", "天下莫柔弱于水,而攻坚强者莫之能胜",
                   "天下没有比水更柔弱的东西,但攻坚克强没有能胜过它的")

    # 结论
    CHAPTER_81 = ("第八十一章", "圣人不积,既以为人己愈有,既以与人己愈多",
                   "圣人不积累,尽量帮助别人自己反而更充足,尽量给予别人自己反而更丰富")

    def __init__(self, chapter: str, quote: str, interpretation: str):
        self.chapter = chapter
        self.quote = quote
        self.interpretation = interpretation

# ============================================================
# 八卦体系
# ============================================================

class BaGua(Enum):
    """八卦枚举"""
    QIAN = ("乾", "☰", "天", "健", "父", "首", "西北", "秋冬", "金",
            "纯阳至刚,代表创造,主导,领导力")
    DUI = ("兑", "☱", "泽", "悦", "少女", "口", "东", "秋", "金",
            "上缺阴柔,代表喜悦,柔和,口才")
    LI = ("离", "☲", "火", "丽", "中女", "目", "南", "夏", "火",
            "中虚阴柔,代表光明,美丽,文化")
    ZHEN = ("震", "☳", "雷", "动", "长男", "足", "东", "春", "木",
            "一阳在下,代表action,震动,进取")
    XUN = ("巽", "☴", "风", "入", "长女", "股", "东南", "春夏", "木",
            "一阴在上,代表顺从,进入,渗透")
    KAN = ("坎", "☵", "水", "陷", "中男", "耳", "北", "冬", "水",
            "中满阳陷,代表危险,陷阱,智慧")
    GEN = ("艮", "☶", "山", "止", "少男", "手", "东北", "冬春", "土",
            "一阳在上,代表停止,稳重,坚守")
    KUN = ("坤", "☷", "地", "顺", "母", "腹", "西南", "夏秋", "土",
            "纯阴至柔,代表承载,包容,柔顺")

    def __init__(self, bagua_name: str, symbol: str, element: str, virtue: str,
                 family: str, body: str, direction: str, season: str,
                 wuxing: str, meaning: str):
        self.bagua_name = bagua_name
        self.symbol = symbol
        self.element = element
        self.virtue = virtue
        self.family = family
        self.body = body
        self.direction = direction
        self.season = season
        self.wuxing = wuxing
        self.meaning = meaning

class BaGuaRelation(Enum):
    """八卦关系"""
    # 相生
    MU_SHENG_HUO = ("木生火", BaGua.ZHEN, BaGua.LI)
    HUO_SHENG_TU = ("火生土", BaGua.LI, BaGua.GEN)
    TU_SHENG_JIN = ("土生金", BaGua.GEN, BaGua.QIAN)
    JIN_SHENG_SHUI = ("金生水", BaGua.QIAN, BaGua.KAN)
    SHUI_SHENG_MU = ("水生木", BaGua.KAN, BaGua.ZHEN)
    # 相克
    MU_KE_TU = ("木克土", BaGua.XUN, BaGua.GEN)
    TU_KE_SHUI = ("土克水", BaGua.GEN, BaGua.KAN)
    SHUI_KE_HUO = ("水克火", BaGua.KAN, BaGua.LI)
    HUO_KE_JIN = ("火克金", BaGua.LI, BaGua.QIAN)
    JIN_KE_MU = ("金克木", BaGua.QIAN, BaGua.XUN)
    # 相合
    QIAN_KUN = ("乾坤合", BaGua.QIAN, BaGua.KUN, "天地交泰,阴阳和合")
    ZHEN_XUN = ("震巽合", BaGua.ZHEN, BaGua.XUN, "雷风相与,action一致")
    KAN_LI = ("坎离合", BaGua.KAN, BaGua.LI, "水火既济,互补平衡")
    GEN_DUI = ("艮兑合", BaGua.GEN, BaGua.DUI, "山泽通气,刚柔并济")
    # 先天转后天
    TIAN_HOU = ("先天转后天", "乾南→乾西北", "乾", "乾")

    def __init__(self, relation: str, *args):
        self.relation = relation
        if len(args) == 2:
            self.bagua1 = args[0]
            self.bagua2 = args[1]
            self.description = ""
        elif len(args) == 3:
            self.bagua1 = args[0]
            self.bagua2 = args[1]
            self.description = args[2]

# ============================================================
# 庄子哲学核心 v2.0新增
# ============================================================

class ZhuangziCore(Enum):
    """庄子哲学核心篇章"""
    # 逍遥哲学
    XIAO_YAO_YOU = "逍遥游"
    QI_WU_LUN = "齐物论"
    YANG_SHENG_ZHU = "养生主"
    DE_CHONG_FU = "德充符"
    REN_JIAN_SHI = "人间世"
    # 辩证哲学
    DA_ZONG_SHI = "大宗师"
    YING_DI_WANG = "应帝王"
    # 认识论
    QI_SHUI_LUN = "秋水"

    @property
    def title(self):
        titles = {
            "XIAO_YAO_YOU": "逍遥游",
            "QI_WU_LUN": "齐物论",
            "YANG_SHENG_ZHU": "养生主",
            "DE_CHONG_FU": "德充符",
            "REN_JIAN_SHI": "人间世",
            "DA_ZONG_SHI": "大宗师",
            "YING_DI_WANG": "应帝王",
            "QI_SHUI_LUN": "秋水"
        }
        return titles.get(self.name, self.value)

    @property
    def quote(self):
        quotes = {
            "XIAO_YAO_YOU": "北冥有鱼,其名为鲲...化而为鸟,其名为鹏",
            "QI_WU_LUN": "天地与我并生,而万物与我为一",
            "YANG_SHENG_ZHU": "吾生也有涯,而知也无涯.以有涯随无涯,殆已",
            "DE_CHONG_FU": "人莫鉴于流水,而鉴于止水",
            "REN_JIAN_SHI": "心斋:若一志,无听之以耳而听之以心",
            "DA_ZONG_SHI": "杀生者不死,生生者不生.其为物,无不将也,无不迎也",
            "YING_DI_WANG": "顺物自然而无容私焉,而天下治矣",
            "QI_SHUI_LUN": "井蛙不可以语于海者,拘于虚也;夏虫不可以语于冰者,笃于时也"
        }
        return quotes.get(self.name, "")

    @property
    def interpretation(self):
        interpretations = {
            "XIAO_YAO_YOU": "绝对自由--超越有限,追求无待的逍遥境界",
            "QI_WU_LUN": "万物齐一--打破是非对错的二元对立",
            "YANG_SHENG_ZHU": "养生之道--顺应自然,保全天性,无为而终",
            "DE_CHONG_FU": "德行充实--内在的德性远比外在形貌重要",
            "REN_JIAN_SHI": "处世智慧--心斋坐忘,虚己以游世",
            "DA_ZONG_SHI": "道为万物宗师--超越生死,安时处顺",
            "YING_DI_WANG": "无为治国--不扰民,顺自然,天下自治",
            "QI_SHUI_LUN": "认知局限--不可被时空经验所束缚"
        }
        return interpretations.get(self.name, "")

# ============================================================
# 德经五层递降体系 v2.0新增
# ============================================================

class DeJingHierarchy(Enum):
    """道德经德经五层递降(第38章)"""
    SHANG_DE = ("上德", "上德不德,是以有德", "不自以为有德,才是真正有德")
    XIA_DE = ("下德", "下德不失德,是以无德", "刻意追求形式之德,反而无德")
    SHANG_REN = ("上仁", "上仁为之而无以为", "仁爱出于自然,无目的性")
    SHANG_YI = ("上义", "上义为之而有以为", "道义出于有意的judge")
    SHANG_LI = ("上礼", "上礼为之而莫之应,则攘臂而扔之", "礼仪是道德沦丧的最后手段")

    def __init__(self, level: str, quote: str, meaning: str):
        self.level = level
        self.quote = quote
        self.meaning = meaning

# ============================================================
# 道的三重境界 v2.0新增
# ============================================================

class DaoThreeRealms(Enum):
    """道的认知三重境界"""
    REALM_1 = "可道之道"
    REALM_2 = "常道之道"
    REALM_3 = "道法自然"

    @property
    def name(self):
        return self.value

    @property
    def definition(self):
        definitions = {
            "REALM_1": "语言可表达的道",
            "REALM_2": "永恒不变的道",
            "REALM_3": "道以自然为法则"
        }
        return definitions.get(self.name, "")

    @property
    def wisdom(self):
        wisdoms = {
            "REALM_1": "相对真理,道的表现形式",
            "REALM_2": "绝对真理,道的本体",
            "REALM_3": "最高智慧,道与万物合一"
        }
        return wisdoms.get(self.name, "")

# ============================================================
# 阴阳五行互推体系 v2.0新增
# ============================================================

class WuXing(Enum):
    """五行体系"""
    MU = "木"
    HUO = "火"
    TU = "土"
    JIN = "金"
    SHUI = "水"

    @property
    def name(self):
        return self.value

    @property
    def direction(self):
        directions = {"MU": "东", "HUO": "南", "TU": "中", "JIN": "西", "SHUI": "北"}
        return directions.get(self.name, "")

    @property
    def season(self):
        seasons = {"MU": "春", "HUO": "夏", "TU": "长夏", "JIN": "秋", "SHUI": "冬"}
        return seasons.get(self.name, "")

    @property
    def function(self):
        functions = {"MU": "生", "HUO": "长", "TU": "化", "JIN": "收", "SHUI": "藏"}
        return functions.get(self.name, "")

    @property
    def organ(self):
        organs = {"MU": "肝", "HUO": "心", "TU": "脾", "JIN": "肺", "SHUI": "肾"}
        return organs.get(self.name, "")

    @property
    def virtue(self):
        virtues = {"MU": "仁", "HUO": "礼", "TU": "信", "JIN": "义", "SHUI": "智"}
        return virtues.get(self.name, "")

    @property
    def color(self):
        colors = {"MU": "青", "HUO": "赤", "TU": "黄", "JIN": "白", "SHUI": "黑"}
        return colors.get(self.name, "")

    @property
    def note(self):
        notes = {"MU": "角", "HUO": "徵", "TU": "宫", "JIN": "商", "SHUI": "羽"}
        return notes.get(self.name, "")

    @property
    def numbers(self):
        nums = {"MU": [1, 2], "HUO": [3, 4], "TU": [5, 6], "JIN": [7, 8], "SHUI": [9, 10]}
        return nums.get(self.name, [])

class WuXingCycle(Enum):
    """五行生克循环"""
    # 相生
    MU_SHENG_HUO = "木生火"
    HUO_SHENG_TU = "火生土"
    TU_SHENG_JIN = "土生金"
    JIN_SHENG_SHUI = "金生水"
    SHUI_SHENG_MU = "水生木"
    # 相克
    MU_KE_TU = "木克土"
    TU_KE_SHUI = "土克水"
    SHUI_KE_HUO = "水克火"
    HUO_KE_JIN = "火克金"
    JIN_KE_MU = "金克木"

    @property
    def name(self):
        return self.value

    @property
    def body_relation(self):
        relations = {
            "MU_SHENG_HUO": "肝(木)养心(火)",
            "HUO_SHENG_TU": "心(火)暖脾(土)",
            "TU_SHENG_JIN": "脾(土)化肺(金)",
            "JIN_SHENG_SHUI": "肺(金)滋肾(水)",
            "SHUI_SHENG_MU": "肾(水)养肝(木)",
            "MU_KE_TU": "肝(木)制脾(土)",
            "TU_KE_SHUI": "脾(土)控肾(水)",
            "SHUI_KE_HUO": "肾(水)制心(火)",
            "HUO_KE_JIN": "心(火)制肺(金)",
            "JIN_KE_MU": "肺(金)制肝(木)"
        }
        return relations.get(self.name, "")

    @property
    def principle(self):
        principles = {
            "MU_SHENG_HUO": "木燃烧生火,生发助长",
            "HUO_SHENG_TU": "火燃烧成灰化土",
            "TU_SHENG_JIN": "土中蕴藏金属矿物",
            "JIN_SHENG_SHUI": "金属熔化成液体",
            "SHUI_SHENG_MU": "水滋润树木生长",
            "MU_KE_TU": "树木根系扎入土壤",
            "TU_KE_SHUI": "堤坝阻挡水流",
            "SHUI_KE_HUO": "水灭火",
            "HUO_KE_JIN": "火熔化金属",
            "JIN_KE_MU": "刀斧砍伐树木"
        }
        return principles.get(self.name, "")

# ============================================================
# 四象体系 v2.0新增
# ============================================================

class SiXiang(Enum):
    """四象体系(阴阳的四种组合态)"""
    TAI_YANG = "太阳"
    SHAO_YIN = "少阴"
    SHAO_YANG = "少阳"
    TAI_YIN = "太阴"

    @property
    def name(self):
        return self.value

    @property
    def nature(self):
        natures = {
            "TAI_YANG": "阳中之阳",
            "SHAO_YIN": "阳中之阴",
            "SHAO_YANG": "阴中之阳",
            "TAI_YIN": "阴中之阴"
        }
        return natures.get(self.name, "")

    @property
    def bagua_ref(self):
        refs = {
            "TAI_YANG": "乾(☰☰)",
            "SHAO_YIN": "兑(☱☱)",
            "SHAO_YANG": "震(☳☳)",
            "TAI_YIN": "坤(☷☷)"
        }
        return refs.get(self.name, "")

    @property
    def time(self):
        times = {
            "TAI_YANG": "春分→夏至",
            "SHAO_YIN": "夏至→秋分",
            "SHAO_YANG": "冬至→春分",
            "TAI_YIN": "秋分→冬至"
        }
        return times.get(self.name, "")

    @property
    def meaning(self):
        meanings = {
            "TAI_YANG": "刚健,纯阳,创造",
            "SHAO_YIN": "收敛,温和,成熟",
            "SHAO_YANG": "萌发,进取,希望",
            "TAI_YIN": "收藏,沉静,孕育"
        }
        return meanings.get(self.name, "")

# ============================================================
# 道家管理哲学 v2.0新增
# ============================================================

class DaoManagement(Enum):
    """道家管理哲学"""
    WU_WEI = "无为而治"
    WU_SHI = "无事取天下"
    SHANG_SHAN_RUO_SHUI = "上善若水式领导"
    ZHI_DA_GUO = "治大国若烹小鲜"
    CI_JIAN_BU_GAN = "三宝管理法"
    TUO_QI_RUI = "挫其锐解其纷"
    BU_XING_ER_ZHI = "不行而知"
    WEI_YU_WEI_SHI = "为于未有事"

    @property
    def name(self):
        return self.value

    @property
    def quote(self):
        quotes = {
            "WU_WEI": "太上,下知有之;其次,亲而誉之",
            "WU_SHI": "以无事取天下,及其有事,不足以取天下",
            "SHANG_SHAN_RUO_SHUI": "水善利万物而不争",
            "ZHI_DA_GUO": "治大国若烹小鲜",
            "CI_JIAN_BU_GAN": "慈,俭,不敢为天下先",
            "TUO_QI_RUI": "挫其锐,解其纷,和其光,同其尘",
            "BU_XING_ER_ZHI": "不出户,知天下",
            "WEI_YU_WEI_SHI": "为之于未有,治之于未乱"
        }
        return quotes.get(self.name, "")

    @property
    def interpretation(self):
        interpretations = {
            "WU_WEI": "最高管理者不干预,让团队自主运作;其次的领导者让人亲近称赞",
            "WU_SHI": "不折腾就是最好的管理,过度管理反而导致混乱",
            "SHANG_SHAN_RUO_SHUI": "领导如水:服务团队,处低不争,顺势而为",
            "ZHI_DA_GUO": "管理复杂组织如同煎小鱼,不能反复翻动",
            "CI_JIAN_BU_GAN": "慈爱员工,俭朴经营,谦虚不争领导style",
            "TUO_QI_RUI": "管理中要钝化锋芒,化解矛盾,和谐共处,融入团队",
            "BU_XING_ER_ZHI": "优秀管理者不需要事必躬亲,通过系统即可洞察全局",
            "WEI_YU_WEI_SHI": "管理重在预防,在问题出现前就提前布局"
        }
        return interpretations.get(self.name, "")

# ============================================================
# 道家养生智慧 v2.0新增
# ============================================================

class DaoHealth(Enum):
    """道家养生智慧"""
    ZHI_XU_SHOU_JING = "致虚守静"
    SI_XING_BING_LUN = "四季养生"
    SHAN_YANG_XIN = "善养心"
    WEI_FU_BU_WEI_MU = "为腹不为目"
    GU_GEN_FU_MING = "归根复命"
    CHI_JIAN_YANG_SHEN = "啬俭养神"
    BAO_QUAN_GUI_ZHEN = "保全归真"
    WEI_XUE_RI_YI_WEI_DAO_RI_SUN = "为道日损"

    @property
    def name(self):
        return self.value

    @property
    def quote(self):
        quotes = {
            "ZHI_XU_SHOU_JING": "致虚极,守静笃",
            "SI_XING_BING_LUN": "春夏养阳,秋冬养阴",
            "SHAN_YANG_XIN": "心善渊",
            "WEI_FU_BU_WEI_MU": "为腹不为目,故去彼取此",
            "GU_GEN_FU_MING": "归根曰静,是谓复命",
            "CHI_JIAN_YANG_SHEN": "治人事天莫若啬",
            "BAO_QUAN_GUI_ZHEN": "见素抱朴,少私寡欲",
            "WEI_XUE_RI_YI_WEI_DAO_RI_SUN": "为学日益,为道日损"
        }
        return quotes.get(self.name, "")

    @property
    def interpretation(self):
        interpretations = {
            "ZHI_XU_SHOU_JING": "虚静是养生的根本功夫",
            "SI_XING_BING_LUN": "顺应四时阴阳变化调养",
            "SHAN_YANG_XIN": "心胸深沉如渊,情绪稳定平和",
            "WEI_FU_BU_WEI_MU": "注重内在充实,不追求外在刺激",
            "GU_GEN_FU_MING": "回归生命本源,恢复自然状态",
            "CHI_JIAN_YANG_SHEN": "节约精气神,不妄耗,不妄为",
            "BAO_QUAN_GUI_ZHEN": "保持朴素本性,减少私心欲望",
            "WEI_XUE_RI_YI_WEI_DAO_RI_SUN": "减少不必要的知识负担,回归简单纯粹"
        }
        return interpretations.get(self.name, "")

# ============================================================
# 阴阳学说
# ============================================================

class YinYang(Enum):
    """阴阳基本属性"""
    YANG = "阳"
    YIN = "阴"

    @property
    def yy_name(self):
        return self.value

    @property
    def attributes(self):
        if self.name == "YANG":
            return ["天", "日", "昼", "热", "动", "升", "刚", "强", "进", "开", "奇"]
        return ["地", "月", "夜", "寒", "静", "降", "柔", "弱", "退", "闭", "偶"]

class YinYangPrinciple(Enum):
    """阴阳基本原则"""
    DUAN_ZHI = "对立制约"
    HU_GEN = "互根互用"
    XIAO_CHANG = "消长平衡"
    ZHUAN_HUA = "相互转化"
    HU_CANG = "互藏交感"

    @property
    def yyp_name(self):
        return self.value

    @property
    def definition(self):
        definitions = {
            "DUAN_ZHI": "阴阳双方相互对立,相互制约",
            "HU_GEN": "阴阳相互依存,互为根本",
            "XIAO_CHANG": "阴阳双方彼消此长,维持动态平衡",
            "ZHUAN_HUA": "阴阳在一定条件下相互转化",
            "HU_CANG": "阴中有阳,阳中有阴,相藏相系"
        }
        return definitions.get(self.name, "")

    @property
    def examples(self):
        examples_map = {
            "DUAN_ZHI": ["骄兵必败", "刚柔相济", "动静结合", "寒热调和"],
            "HU_GEN": ["孤阴不生,独阳不长", "阳根于阴,阴根于阳", "阴阳相互依存"],
            "XIAO_CHANG": ["春夏养阳,秋冬养阴", "阳盛则阴衰", "阴盛则阳衰"],
            "ZHUAN_HUA": ["物极必反", "否极泰来", "阴阳交替", "祸福相依"],
            "HU_CANG": ["阳中有阴,阴中有阳", "阴阳交合,相互感应"]
        }
        return examples_map.get(self.name, [])

# ============================================================
# 九宫洛书
# ============================================================

class LuoShu:
    """洛书(幻方)"""
    GRID = [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6]
    ]

    CENTER = 5
    HEAD_NUMBER = 9
    FOOT_NUMBER = 1
    LEFT_NUMBER = 3
    RIGHT_NUMBER = 7

    @classmethod
    def get_number(cls, row: int, col: int) -> int:
        """get指定位置的数字"""
        return cls.GRID[row][col]

    @classmethod
    def verify_magic_sum(cls) -> bool:
        """验证幻和方法(每行,每列,对角线之和均为15)"""
        target = 15
        # 行
        for row in cls.GRID:
            if sum(row) != target:
                return False
        # 列
        for col in range(3):
            if sum(cls.GRID[row][col] for row in range(3)) != target:
                return False
        # 对角线
        if cls.GRID[0][0] + cls.GRID[1][1] + cls.GRID[2][2] != target:
            return False
        if cls.GRID[0][2] + cls.GRID[1][1] + cls.GRID[2][0] != target:
            return False
        return True

    @classmethod
    def get_position_meaning(cls, row: int, col: int) -> Dict[str, Any]:
        """get位置含义"""
        meanings = {
            (0, 0): {"number": 4, "bagua": BaGua.XUN, "meaning": "东南-风", "virtue": "进入"},
            (0, 1): {"number": 9, "bagua": BaGua.LI, "meaning": "南-火", "virtue": "光明"},
            (0, 2): {"number": 2, "bagua": BaGua.KUN, "meaning": "西南-地", "virtue": "柔顺"},
            (1, 0): {"number": 3, "bagua": BaGua.ZHEN, "meaning": "东-雷", "virtue": "震动"},
            (1, 1): {"number": 5, "bagua": "中宫", "meaning": "中-土", "virtue": "调和"},
            (1, 2): {"number": 7, "bagua": BaGua.GEN, "meaning": "东北-山", "virtue": "静止"},
            (2, 0): {"number": 8, "bagua": BaGua.GEN, "meaning": "东北-山", "virtue": "静止"},
            (2, 1): {"number": 1, "bagua": BaGua.KAN, "meaning": "北-水", "virtue": "危险"},
            (2, 2): {"number": 6, "bagua": BaGua.QIAN, "meaning": "西北-天", "virtue": "刚健"},
        }
        return meanings.get((row, col), {})

# ============================================================
# 核心数据结构
# ============================================================

@dataclass
class DaoWisdom:
    """道家智慧结构"""
    principle: str                    # 核心原则
    source_chapter: str               # 道德经章节
    interpretation: str               # 解读
    application: str                  # 应用建议
    yin_yang_nature: str              # 阴阳属性
    bagua_correlation: str            # 八卦关联

@dataclass
class DaoDecision:
    """道家decision结构"""
    decision_id: str
    situation: str                    # 情境
    yin_yang_analysis: Dict[str, Any] # 阴阳分析
    bagua_analysis: Dict[str, Any]   # 八卦分析
    dao_advice: List[str]             # 道德经建议
    recommended_action: str            # 推荐的action
    wisdom_source: str                # 智慧来源
    balance_score: float              # 阴阳平衡分数(0-1)
    transformation_potential: str     # 转化潜力

@dataclass
class TaoistPersona:
    """道家人格特质"""
    # 阴阳属性
    yin_yang_balance: float = 0.5     # 阴阳平衡度(0=纯阴, 1=纯阳)
    yang_attributes: List[str] = field(default_factory=list)  # 阳性特质
    yin_attributes: List[str] = field(default_factory=list)   # 阴性特质

    # 八卦属性
    dominant_bagua: Optional[BaGua] = None  # 主卦
    supporting_bagua: List[BaGua] = field(default_factory=list)  # 辅卦

    # 道德经修为
    daodejing_level: int = 5          # 道德经理解层级(1-10)
    natural_flow: float = 0.8         # 自然流动程度(0-1)
    non_action_practice: float = 0.6 # 无为实践程度(0-1)
    softness_wisdom: float = 0.7      # 柔弱智慧(0-1)

    # decisionstyle
    decision_style: str = "balanced"  # balanced/yang/dynamic
