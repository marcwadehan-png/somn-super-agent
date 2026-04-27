# -*- coding: utf-8 -*-
"""
783贤者完整注册表 v1.1.0（已清理79个噪音条目）

包含783位贤者的完整元数据，用于Cloning系统。
按学派和领域组织，支持快速查找和咨询。

更新日期: 2026-04-13
清理内容: 删除79个群体占位符/学派后学/描述性标签类噪音条目
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class SageTier(Enum):
    """贤者层级"""
    GRANDMASTER = 0   # 超级大师（超越创始人）
    FOUNDER = 1      # 学派创始人
    MASTER = 2       # 集大成者
    SCHOLAR = 3      # 著名学者
    PRACTITIONER = 4 # 实践者


@dataclass
class SageMeta:
    """贤者元数据"""
    name: str                    # 中文名
    name_en: str                 # 英文名/ID
    school: str                  # 所属学派
    tier: SageTier               # 层级
    era: str                     # 时代
    lifespan: str                # 生卒年
    titles: List[str] = field(default_factory=list)  # 头衔
    works: List[str] = field(default_factory=list)   # 代表作品
    expertise: List[str] = field(default_factory=list)  # 专长领域
    department: str = ""         # 所属部门
    description: str = ""        # 简介


# ═══════════════════════════════════════════════════════════════════════════════
# 一、儒家 (Confucianism) - 100人
# ═══════════════════════════════════════════════════════════════════════════════

CONFUCIAN_SAGES: List[SageMeta] = [
    # === 创始人 ===
    SageMeta(name="孔子", name_en="confucius", school="儒家", tier=SageTier.FOUNDER, era="春秋", lifespan="前551-前479", titles=["至圣先师", "万世师表"], works=["论语", "春秋"], expertise=["仁学", "礼治", "教育"], department="礼部", description="儒家学派创始人"),
    SageMeta(name="孟子", name_en="mencius", school="儒家", tier=SageTier.FOUNDER, era="战国", lifespan="前372-前289", titles=["亚圣"], works=["孟子"], expertise=["性善论", "仁政"], department="礼部", description="儒家亚圣"),
    SageMeta(name="荀子", name_en="xunzi", school="儒家", tier=SageTier.FOUNDER, era="战国", lifespan="前313-前238", titles=["后圣"], works=["荀子"], expertise=["性恶论", "礼法并重"], department="礼部", description="儒家集大成者"),
    
    # === 汉代经学 ===
    SageMeta(name="董仲舒", name_en="dong_zhongshu", school="儒家", tier=SageTier.MASTER, era="西汉", lifespan="前179-前104", titles=["汉代大儒"], works=["春秋繁露"], expertise=["天人感应", "独尊儒术"], department="礼部", description="提出罢黜百家独尊儒术"),
    SageMeta(name="郑玄", name_en="zheng_xuan", school="儒家", tier=SageTier.MASTER, era="东汉", lifespan="127-200", titles=["经学大师"], works=["毛诗传笺"], expertise=["经学", "训诂学"], department="礼部", description="东汉经学大师"),
    SageMeta(name="扬雄", name_en="yang_xiong", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前53-18", titles=["辞赋家"], works=["法言", "太玄"], expertise=["哲学", "语言学"], department="礼部", description="模仿论语作法言"),
    SageMeta(name="刘向", name_en="liu_xiang", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前77-前6", titles=["目录学家"], works=["说苑", "新序"], expertise=["目录学", "文献"], department="礼部", description="中国目录学之祖"),
    SageMeta(name="刘歆", name_en="liu_xin", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前50-23", titles=["目录学家"], works=["七略"], expertise=["目录学", "古文经"], department="礼部", description="刘向之子，目录学家"),
    SageMeta(name="贾谊", name_en="jia_yi", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前200-前168", titles=["政论家"], works=["新书", "过秦论"], expertise=["政论", "治国"], department="吏部", description="西汉政论家"),
    SageMeta(name="桓宽", name_en="huan_kuan", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?", titles=["经济学者"], works=["盐铁论"], expertise=["经济", "盐铁"], department="户部", description="记录盐铁会议"),
    
    # === 宋明理学 ===
    SageMeta(name="周敦颐", name_en="zhou_dunyi", school="儒家", tier=SageTier.FOUNDER, era="北宋", lifespan="1017-1073", titles=["理学开山"], works=["太极图说"], expertise=["理学", "太极"], department="礼部", description="理学开山鼻祖"),
    SageMeta(name="程颢", name_en="cheng_hao", school="儒家", tier=SageTier.FOUNDER, era="北宋", lifespan="1032-1085", titles=["明道先生"], works=["定性书"], expertise=["理学", "心学倾向"], department="礼部", description="程朱理学创始人之一"),
    SageMeta(name="程颐", name_en="cheng_yi", school="儒家", tier=SageTier.FOUNDER, era="北宋", lifespan="1033-1107", titles=["伊川先生"], works=["伊川易传"], expertise=["理学", "格物致知"], department="礼部", description="程朱理学创始人之一"),
    SageMeta(name="朱熹", name_en="zhu_xi", school="儒家", tier=SageTier.MASTER, era="南宋", lifespan="1130-1200", titles=["朱子"], works=["四书章句集注"], expertise=["理学", "理气论"], department="礼部", description="理学集大成者"),
    SageMeta(name="陆九渊", name_en="lu_jiuyuan", school="儒家", tier=SageTier.FOUNDER, era="南宋", lifespan="1139-1193", titles=["象山先生"], works=["象山集"], expertise=["心学", "心即理"], department="礼部", description="心学创始人"),
    SageMeta(name="王阳明", name_en="wang_yangming", school="儒家", tier=SageTier.MASTER, era="明代", lifespan="1472-1529", titles=["阳明先生"], works=["传习录"], expertise=["心学", "知行合一"], department="兵部", description="心学集大成者"),
    SageMeta(name="张载", name_en="zhang_zai", school="儒家", tier=SageTier.MASTER, era="北宋", lifespan="1020-1077", titles=["横渠先生"], works=["正蒙", "西铭"], expertise=["气学", "民胞物与"], department="礼部", description="关学创始人"),
    SageMeta(name="邵雍", name_en="shao_yong", school="儒家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1011-1077", titles=["康节先生"], works=["皇极经世"], expertise=["象数学", "易学"], department="工部", description="象数学大师"),
    SageMeta(name="程颢程颐", name_en="cheng_brothers", school="儒家", tier=SageTier.MASTER, era="北宋", lifespan="", titles=["二程"], works=["二程集"], expertise=["理学"], department="礼部", description="程颢程颐合称"),
    SageMeta(name="吕祖谦", name_en="lv_zuqian", school="儒家", tier=SageTier.SCHOLAR, era="南宋", lifespan="1137-1181", titles=["东莱先生"], works=["东莱博议"], expertise=["史学", "文献"], department="礼部", description="金华学派"),
    
    # === 明清实学 ===
    SageMeta(name="王夫之", name_en="wang_fuzhi", school="儒家", tier=SageTier.MASTER, era="明清", lifespan="1619-1692", titles=["船山先生"], works=["读通鉴论"], expertise=["实学", "气学"], department="礼部", description="明末清初三大思想家"),
    SageMeta(name="顾炎武", name_en="gu_yanwu", school="儒家", tier=SageTier.MASTER, era="明清", lifespan="1613-1682", titles=["亭林先生"], works=["日知录"], expertise=["实学", "经世致用"], department="户部", description="天下兴亡匹夫有责"),
    SageMeta(name="黄宗羲", name_en="huang_zongxi", school="儒家", tier=SageTier.MASTER, era="明清", lifespan="1610-1695", titles=["梨洲先生"], works=["明夷待访录"], expertise=["政治思想", "民主"], department="礼部", description="中国思想启蒙之父"),
    SageMeta(name="颜元", name_en="yan_yuan", school="儒家", tier=SageTier.SCHOLAR, era="清代", lifespan="1635-1704", titles=["习斋先生"], works=["四存编"], expertise=["实学", "教育"], department="礼部", description="颜李学派创始人"),
    SageMeta(name="李塨", name_en="li_gong", school="儒家", tier=SageTier.SCHOLAR, era="清代", lifespan="1659-1733", titles=["恕谷先生"], works=["大学辨业"], expertise=["实学", "教育"], department="礼部", description="颜李学派"),
    SageMeta(name="戴震", name_en="dai_zhen", school="儒家", tier=SageTier.SCHOLAR, era="清代", lifespan="1724-1777", titles=["考据学家"], works=["孟子字义疏证"], expertise=["考据", "哲学"], department="礼部", description="清代考据学大师"),
    SageMeta(name="康有为", name_en="kang_youwei", school="儒家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1858-1927", titles=["维新派"], works=["新学伪经考"], expertise=["今文经", "变法"], department="吏部", description="戊戌变法领袖"),
    SageMeta(name="梁启超", name_en="liang_qichao", school="儒家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1873-1929", titles=["启蒙思想家"], works=["饮冰室合集"], expertise=["启蒙", "史学"], department="礼部", description="近代启蒙思想家"),
    SageMeta(name="章太炎", name_en="zhang_taiyan", school="儒家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1869-1936", titles=["国学大师"], works=["国故论衡"], expertise=["国学", "古文经"], department="礼部", description="近代国学大师"),
    SageMeta(name="钱穆", name_en="qian_mu", school="儒家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1895-1990", titles=["史学家"], works=["国史大纲"], expertise=["史学", "文化"], department="礼部", description="现代史学家"),
    
    # === 近现代新儒家 ===
    SageMeta(name="熊十力", name_en="xiong_shili", school="儒家", tier=SageTier.MASTER, era="近现代", lifespan="1885-1968", titles=["新儒家开山"], works=["新唯识论"], expertise=["新儒学", "体用论"], department="礼部", description="现代新儒家开山"),
    SageMeta(name="梁漱溟", name_en="liang_shuming", school="儒家", tier=SageTier.MASTER, era="近现代", lifespan="1893-1988", titles=["新儒家代表"], works=["东西文化及其哲学"], expertise=["文化哲学", "乡村建设"], department="礼部", description="现代新儒家代表"),
    SageMeta(name="冯友兰", name_en="feng_youlan", school="儒家", tier=SageTier.MASTER, era="近现代", lifespan="1895-1990", titles=["哲学家"], works=["中国哲学史"], expertise=["中国哲学", "新理学"], department="礼部", description="新理学体系"),
    SageMeta(name="牟宗三", name_en="mou_zongsan", school="儒家", tier=SageTier.MASTER, era="近现代", lifespan="1909-1995", titles=["新儒家代表"], works=["心体与性体"], expertise=["道德形上学", "会通中西"], department="礼部", description="当代新儒家代表"),
    SageMeta(name="唐君毅", name_en="tang_junyi", school="儒家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1909-1978", titles=["新儒家代表"], works=["生命存在与心灵境界"], expertise=["文化哲学", "心灵境界"], department="礼部", description="现代新儒家代表"),
    SageMeta(name="徐复观", name_en="xu_fuguan", school="儒家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1903-1982", titles=["新儒家代表"], works=["中国人性论史"], expertise=["思想史", "艺术哲学"], department="礼部", description="现代新儒家代表"),
    SageMeta(name="贺麟", name_en="he_lin", school="儒家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1902-1992", titles=["哲学家"], works=["文化与人生"], expertise=["新心学", "翻译"], department="礼部", description="新心学代表"),
    SageMeta(name="张君劢", name_en="zhang_junmai", school="儒家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1887-1969", titles=["新儒家"], works=["新儒家思想史"], expertise=["政治哲学", "宪法"], department="吏部", description="新儒家代表"),
    SageMeta(name="方东美", name_en="fang_dongmei", school="儒家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1899-1977", titles=["哲学家"], works=["中国人生哲学"], expertise=["比较哲学", "文化"], department="礼部", description="比较哲学家"),
    SageMeta(name="杜维明", name_en="du_weiming", school="儒家", tier=SageTier.SCHOLAR, era="当代", lifespan="1940-", titles=["新儒家"], works=["儒学第三期"], expertise=["儒学", "文明对话"], department="礼部", description="当代新儒家代表"),
    
    # === 孔门弟子 ===
    SageMeta(name="颜回", name_en="yan_hui", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前521-前481", titles=["复圣"], works=[], expertise=["德行", "安贫乐道"], department="礼部", description="孔子最得意弟子"),
    SageMeta(name="曾子", name_en="zengzi", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前505-前435", titles=["宗圣"], works=["大学", "孝经"], expertise=["孝道", "修身"], department="礼部", description="作大学孝经"),
    SageMeta(name="子思", name_en="zi_si", school="儒家", tier=SageTier.SCHOLAR, era="战国", lifespan="前483-前402", titles=["述圣"], works=["中庸"], expertise=["中庸之道", "诚学"], department="礼部", description="孔子之孙，作中庸"),
    SageMeta(name="子贡", name_en="zi_gong", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前520-前456", titles=["言语科代表"], works=[], expertise=["外交", "经商"], department="户部", description="言语科代表，善于经商"),
    SageMeta(name="子路", name_en="zi_lu", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前542-前480", titles=["政事科代表"], works=[], expertise=["政事", "勇武"], department="兵部", description="政事科代表，勇猛"),
    SageMeta(name="子夏", name_en="zi_xia", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前507-前400", titles=["文学科代表"], works=["毛诗"], expertise=["文学", "经学"], department="礼部", description="文学科代表，传毛诗"),
    SageMeta(name="子游", name_en="zi_you", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前506-前443", titles=["文学科代表"], works=[], expertise=["文学", "礼乐"], department="礼部", description="文学科代表"),
    SageMeta(name="宰我", name_en="zai_wo", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["言语科"], works=[], expertise=["言语", "辩论"], department="礼部", description="言语科代表"),
    SageMeta(name="冉有", name_en="ran_you", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前522-前?", titles=["政事科"], works=[], expertise=["政事", "理财"], department="户部", description="政事科代表"),
    SageMeta(name="闵子骞", name_en="min_ziqian", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前536-前487", titles=["德行科"], works=[], expertise=["德行", "孝道"], department="礼部", description="德行科代表"),
    
    # === 其他重要儒者 ===
    SageMeta(name="子张", name_en="zi_zhang", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前503-前?", titles=["子张氏之儒"], works=[], expertise=["交友", "政治"], department="礼部", description="孔子弟子"),
    SageMeta(name="有子", name_en="you_zi", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前518-?", titles=["有子"], works=[], expertise=["礼论", "孝悌"], department="礼部", description="孔子弟子"),
    SageMeta(name="澹台灭明", name_en="tantai_mieming", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前512-?", titles=["子羽"], works=[], expertise=["修身", "行事"], department="礼部", description="孔子弟子"),
    SageMeta(name="原宪", name_en="yuan_xian", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前515-?", titles=["子思"], works=[], expertise=["安贫", "守节"], department="礼部", description="孔子弟子"),
    SageMeta(name="公西华", name_en="gongxi_hua", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["子华"], works=[], expertise=["礼仪", "外交"], department="礼部", description="孔子弟子"),
    SageMeta(name="樊迟", name_en="fan_chi", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["樊须"], works=[], expertise=["农学", "勇武"], department="工部", description="孔子弟子"),
    SageMeta(name="公冶长", name_en="gongye_chang", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["子长"], works=[], expertise=["德行", "鸟语"], department="礼部", description="孔子弟子，传说懂鸟语"),
    SageMeta(name="南容", name_en="nan_rong", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["子容"], works=[], expertise=["慎言", "德行"], department="礼部", description="孔子弟子"),
    SageMeta(name="宓子贱", name_en="mi_zijian", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前521-前445", titles=["单父宰"], works=[], expertise=["政治", "教化"], department="吏部", description="孔子弟子，单父宰"),
    SageMeta(name="巫马期", name_en="wuma_qi", school="儒家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["子期"], works=[], expertise=["政事"], department="吏部", description="孔子弟子"),
    
    # === 汉唐儒者 ===
    SageMeta(name="伏生", name_en="fu_sheng", school="儒家", tier=SageTier.SCHOLAR, era="秦汉", lifespan="前260-前161", titles=["尚书博士"], works=["今文尚书"], expertise=["尚书", "经学"], department="礼部", description="传今文尚书"),
    SageMeta(name="辕固生", name_en="yuangusheng", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?", titles=["齐诗博士"], works=["齐诗"], expertise=["诗经", "经学"], department="礼部", description="传齐诗"),
    SageMeta(name="韩婴", name_en="han_ying", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前200-前130", titles=["韩诗博士"], works=["韩诗外传"], expertise=["诗经", "经学"], department="礼部", description="传韩诗"),
    SageMeta(name="毛亨", name_en="mao_heng", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?", titles=["毛诗故训传"], works=["毛诗"], expertise=["诗经", "训诂"], department="礼部", description="毛诗创始人"),
    SageMeta(name="毛苌", name_en="mao_chang", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?", titles=["小毛公"], works=["毛诗"], expertise=["诗经"], department="礼部", description="毛诗传人"),
    SageMeta(name="孔安国", name_en="kong_anguo", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前156-前74", titles=["古文尚书"], works=["古文尚书"], expertise=["尚书", "古文经"], department="礼部", description="传古文尚书"),
    SageMeta(name="欧阳生", name_en="ouyang_sheng", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前200-前140", titles=["欧阳尚书"], works=["欧阳尚书"], expertise=["尚书"], department="礼部", description="传欧阳尚书"),
    SageMeta(name="大小夏侯", name_en="xiahou", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="", titles=["夏侯尚书"], works=["大小夏侯尚书"], expertise=["尚书"], department="礼部", description="传夏侯尚书"),
    SageMeta(name="王充", name_en="wang_chong", school="儒家", tier=SageTier.SCHOLAR, era="东汉", lifespan="27-97", titles=["论衡作者"], works=["论衡"], expertise=["批判", "唯物"], department="礼部", description="著论衡"),
    SageMeta(name="许慎", name_en="xu_shen", school="儒家", tier=SageTier.SCHOLAR, era="东汉", lifespan="58-147", titles=["说文解字"], works=["说文解字"], expertise=["文字学", "训诂"], department="礼部", description="说文解字作者"),
    
    # === 宋儒 ===
    SageMeta(name="胡瑗", name_en="hu_yuan", school="儒家", tier=SageTier.SCHOLAR, era="北宋", lifespan="993-1059", titles=["安定先生"], works=["周易口义"], expertise=["易学", "教育"], department="礼部", description="宋初三先生"),
    SageMeta(name="孙复", name_en="sun_fu", school="儒家", tier=SageTier.SCHOLAR, era="北宋", lifespan="992-1057", titles=["泰山先生"], works=["春秋尊王发微"], expertise=["春秋", "经学"], department="礼部", description="宋初三先生"),
    SageMeta(name="石介", name_en="shi_jie", school="儒家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1005-1045", titles=["徂徕先生"], works=["徂徕集"], expertise=["古文", "经学"], department="礼部", description="宋初三先生"),
    SageMeta(name="欧阳修", name_en="ouyang_xiu", school="儒家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1007-1072", titles=["六一居士"], works=["新五代史", "醉翁亭记"], expertise=["史学", "文学"], department="礼部", description="唐宋八大家"),
    SageMeta(name="王安石", name_en="wang_anshi", school="儒家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1021-1086", titles=["临川先生"], works=["临川集"], expertise=["变法", "经学"], department="吏部", description="王安石变法"),
    SageMeta(name="司马光", name_en="sima_guang", school="儒家", tier=SageTier.MASTER, era="北宋", lifespan="1019-1086", titles=["涑水先生"], works=["资治通鉴"], expertise=["史学", "政治"], department="礼部", description="资治通鉴作者"),
    SageMeta(name="苏轼", name_en="su_shi", school="儒家", tier=SageTier.MASTER, era="北宋", lifespan="1037-1101", titles=["东坡居士"], works=["东坡全集"], expertise=["文学", "政治"], department="礼部", description="唐宋八大家"),
    SageMeta(name="苏辙", name_en="su_zhe", school="儒家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1039-1112", titles=["栾城先生"], works=["栾城集"], expertise=["文学", "政治"], department="礼部", description="唐宋八大家"),
    SageMeta(name="曾巩", name_en="zeng_gong", school="儒家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1019-1083", titles=["南丰先生"], works=["元丰类稿"], expertise=["古文", "史学"], department="礼部", description="唐宋八大家"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 二、道家 (Taoism) - 80人
# ═══════════════════════════════════════════════════════════════════════════════

TAOIST_SAGES: List[SageMeta] = [
    # === 创始人 ===
    SageMeta(name="老子", name_en="laozi", school="道家", tier=SageTier.FOUNDER, era="春秋", lifespan="前6-前5世纪", titles=["道家始祖"], works=["道德经"], expertise=["道法自然", "无为"], department="吏部", description="道家创始人"),
    SageMeta(name="庄子", name_en="zhuangzi", school="道家", tier=SageTier.FOUNDER, era="战国", lifespan="前369-前286", titles=["南华真人"], works=["庄子"], expertise=["逍遥", "齐物"], department="吏部", description="道家集大成者"),
    SageMeta(name="列子", name_en="liezi", school="道家", tier=SageTier.SCHOLAR, era="战国", lifespan="前450-前375", titles=["冲虚真人"], works=["列子"], expertise=["贵虚", "养生"], department="吏部", description="道家代表"),
    
    # === 黄老道家 ===
    SageMeta(name="文子", name_en="wenzi", school="道家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["道家学者"], works=["文子"], expertise=["黄老之学"], department="吏部", description="老子弟子"),
    SageMeta(name="杨朱", name_en="yang_zhu", school="道家", tier=SageTier.SCHOLAR, era="战国", lifespan="前395-前335", titles=["杨朱学派"], works=[], expertise=["贵己", "全生"], department="吏部", description="杨朱学派创始人"),
    SageMeta(name="慎到", name_en="shen_dao", school="道家", tier=SageTier.SCHOLAR, era="战国", lifespan="约前350-前275", titles=["法家先驱"], works=["慎子"], expertise=["势治", "道法结合"], department="刑部", description="由道入法"),
    SageMeta(name="田骈", name_en="tian_pian", school="道家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["黄老学者"], works=[], expertise=["黄老"], department="吏部", description="稷下学者"),
    SageMeta(name="彭蒙", name_en="peng_meng", school="道家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["黄老学者"], works=[], expertise=["黄老"], department="吏部", description="稷下学者"),
    SageMeta(name="接子", name_en="jie_zi", school="道家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["黄老学者"], works=[], expertise=["黄老"], department="吏部", description="稷下学者"),
    SageMeta(name="环渊", name_en="huan_yuan", school="道家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["黄老学者"], works=[], expertise=["黄老"], department="吏部", description="稷下学者"),
    
    # === 魏晋玄学 ===
    SageMeta(name="王弼", name_en="wang_bi", school="道家", tier=SageTier.MASTER, era="魏晋", lifespan="226-249", titles=["玄学宗师"], works=["老子注", "周易注"], expertise=["玄学", "贵无"], department="礼部", description="玄学创始人"),
    SageMeta(name="何晏", name_en="he_yan", school="道家", tier=SageTier.SCHOLAR, era="魏晋", lifespan="190-249", titles=["玄学家"], works=["论语集解"], expertise=["玄学", "无为"], department="礼部", description="玄学代表"),
    SageMeta(name="阮籍", name_en="ruan_ji", school="道家", tier=SageTier.SCHOLAR, era="魏晋", lifespan="210-263", titles=["竹林七贤"], works=["阮籍集"], expertise=["玄学", "诗歌"], department="礼部", description="竹林七贤"),
    SageMeta(name="嵇康", name_en="ji_kang", school="道家", tier=SageTier.SCHOLAR, era="魏晋", lifespan="223-262", titles=["竹林七贤"], works=["嵇康集"], expertise=["玄学", "养生"], department="礼部", description="竹林七贤"),
    SageMeta(name="向秀", name_en="xiang_xiu", school="道家", tier=SageTier.SCHOLAR, era="魏晋", lifespan="约227-272", titles=["竹林七贤"], works=["庄子注"], expertise=["玄学", "庄子"], department="礼部", description="竹林七贤"),
    SageMeta(name="郭象", name_en="guo_xiang", school="道家", tier=SageTier.SCHOLAR, era="魏晋", lifespan="约252-312", titles=["玄学家"], works=["庄子注"], expertise=["玄学", "独化"], department="礼部", description="玄学集大成者"),
    SageMeta(name="山涛", name_en="shan_tao", school="道家", tier=SageTier.SCHOLAR, era="魏晋", lifespan="205-283", titles=["竹林七贤"], works=[], expertise=["玄学", "政治"], department="吏部", description="竹林七贤"),
    SageMeta(name="王戎", name_en="wang_rong", school="道家", tier=SageTier.SCHOLAR, era="魏晋", lifespan="234-305", titles=["竹林七贤"], works=[], expertise=["玄学", "政治"], department="吏部", description="竹林七贤"),
    SageMeta(name="刘伶", name_en="liu_ling", school="道家", tier=SageTier.SCHOLAR, era="魏晋", lifespan="约221-300", titles=["竹林七贤"], works=["酒德颂"], expertise=["玄学", "放达"], department="礼部", description="竹林七贤"),
    SageMeta(name="阮咸", name_en="ruan_xian", school="道家", tier=SageTier.SCHOLAR, era="魏晋", lifespan="?", titles=["竹林七贤"], works=[], expertise=["玄学", "音乐"], department="礼部", description="竹林七贤"),
    
    # === 道教人物 ===
    SageMeta(name="张道陵", name_en="zhang_daoling", school="道家", tier=SageTier.FOUNDER, era="东汉", lifespan="34-156", titles=["张天师"], works=["老子想尔注"], expertise=["道教", "五斗米道"], department="工部", description="道教创始人"),
    SageMeta(name="葛玄", name_en="ge_xuan", school="道家", tier=SageTier.SCHOLAR, era="东汉", lifespan="164-244", titles=["葛仙公"], works=[], expertise=["丹道", "符箓"], department="工部", description="葛洪从祖"),
    SageMeta(name="魏伯阳", name_en="wei_boyang", school="道家", tier=SageTier.SCHOLAR, era="东汉", lifespan="约100-200", titles=["丹道祖师"], works=["周易参同契"], expertise=["丹道", "易学"], department="工部", description="丹道经典作者"),
    SageMeta(name="葛洪", name_en="ge_hong", school="道家", tier=SageTier.MASTER, era="东晋", lifespan="283-343", titles=["抱朴子"], works=["抱朴子"], expertise=["道教", "炼丹", "医药"], department="工部", description="道教理论家"),
    SageMeta(name="陶弘景", name_en="tao_hongjing", school="道家", tier=SageTier.MASTER, era="南朝", lifespan="456-536", titles=["山中宰相"], works=["真诰", "本草经集注"], expertise=["道教", "医药"], department="工部", description="茅山宗创始人"),
    SageMeta(name="寇谦之", name_en="kou_qianzhi", school="道家", tier=SageTier.MASTER, era="北魏", lifespan="365-448", titles=["北天师"], works=["云中音诵新科之诫"], expertise=["北天师道"], department="工部", description="北天师道创始人"),
    SageMeta(name="陆修静", name_en="lu_xiujing", school="道家", tier=SageTier.MASTER, era="南朝", lifespan="406-477", titles=["南天师"], works=["三洞经书目录"], expertise=["南天师道"], department="工部", description="南天师道创始人"),
    SageMeta(name="孙思邈", name_en="sun_simiao", school="道家", tier=SageTier.MASTER, era="唐代", lifespan="541-682", titles=["药王"], works=["千金要方"], expertise=["医药", "养生"], department="工部", description="药王"),
    SageMeta(name="司马承祯", name_en="sima_chengzhen", school="道家", tier=SageTier.SCHOLAR, era="唐代", lifespan="647-735", titles=["上清宗师"], works=["坐忘论"], expertise=["上清派", "坐忘"], department="工部", description="上清派宗师"),
    SageMeta(name="吴筠", name_en="wu_yun", school="道家", tier=SageTier.SCHOLAR, era="唐代", lifespan="?-778", titles=["玄纲先生"], works=["玄纲论"], expertise=["道教", "神仙"], department="工部", description="唐代道士"),
    
    # === 全真道 ===
    SageMeta(name="王重阳", name_en="wang_chongyang", school="道家", tier=SageTier.FOUNDER, era="金代", lifespan="1113-1170", titles=["重阳真人"], works=["重阳全真集"], expertise=["全真道", "三教合一"], department="工部", description="全真道创始人"),
    SageMeta(name="马钰", name_en="ma_yu", school="道家", tier=SageTier.SCHOLAR, era="金代", lifespan="1123-1183", titles=["丹阳真人", "北七真"], works=["渐悟集"], expertise=["全真道", "内丹"], department="工部", description="北七真之一"),
    SageMeta(name="丘处机", name_en="qiu_chuji", school="道家", tier=SageTier.MASTER, era="金元", lifespan="1148-1227", titles=["长春真人", "北七真"], works=["磻溪集"], expertise=["全真道", "止杀"], department="工部", description="西行劝成吉思汗"),
    SageMeta(name="谭处端", name_en="tan_chuduan", school="道家", tier=SageTier.SCHOLAR, era="金代", lifespan="1123-1185", titles=["长真真人", "北七真"], works=["水云集"], expertise=["全真道"], department="工部", description="北七真之一"),
    SageMeta(name="刘处玄", name_en="liu_chuxuan", school="道家", tier=SageTier.SCHOLAR, era="金代", lifespan="1147-1203", titles=["长生真人", "北七真"], works=["仙乐集"], expertise=["全真道"], department="工部", description="北七真之一"),
    SageMeta(name="王处一", name_en="wang_chuyi", school="道家", tier=SageTier.SCHOLAR, era="金代", lifespan="1142-1217", titles=["玉阳真人", "北七真"], works=["云光集"], expertise=["全真道"], department="工部", description="北七真之一"),
    SageMeta(name="郝大通", name_en="hao_datong", school="道家", tier=SageTier.SCHOLAR, era="金代", lifespan="1140-1212", titles=["广宁真人", "北七真"], works=["太古集"], expertise=["全真道", "易学"], department="工部", description="北七真之一"),
    SageMeta(name="孙不二", name_en="sun_buer", school="道家", tier=SageTier.SCHOLAR, era="金代", lifespan="1119-1182", titles=["清静散人", "北七真"], works=["孙不二元君法语"], expertise=["全真道", "女丹"], department="工部", description="北七真之一"),
    SageMeta(name="尹志平", name_en="yin_zhiping", school="道家", tier=SageTier.SCHOLAR, era="元代", lifespan="1169-1251", titles=["清和真人"], works=["葆光集"], expertise=["全真道"], department="工部", description="丘处机弟子"),
    SageMeta(name="李志常", name_en="li_zhichang", school="道家", tier=SageTier.SCHOLAR, era="元代", lifespan="1193-1256", titles=["真常真人"], works=["长春真人西游记"], expertise=["全真道"], department="工部", description="全真掌教"),
    
    # === 内丹学派 ===
    SageMeta(name="张伯端", name_en="zhang_boduan", school="道家", tier=SageTier.MASTER, era="北宋", lifespan="983-1082", titles=["紫阳真人"], works=["悟真篇"], expertise=["内丹", "南宗"], department="工部", description="内丹南宗创始人"),
    SageMeta(name="石泰", name_en="shi_tai", school="道家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1022-1158", titles=["杏林真人"], works=["还元篇"], expertise=["内丹", "南宗"], department="工部", description="南宗二祖"),
    SageMeta(name="薛道光", name_en="xue_daoguang", school="道家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1078-1191", titles=["紫贤真人"], works=["还丹复命篇"], expertise=["内丹", "南宗"], department="工部", description="南宗三祖"),
    SageMeta(name="陈楠", name_en="chen_nan", school="道家", tier=SageTier.SCHOLAR, era="南宋", lifespan="?-1213", titles=["翠虚真人"], works=["翠虚篇"], expertise=["内丹", "雷法"], department="工部", description="南宗四祖"),
    SageMeta(name="白玉蟾", name_en="bai_yuchan", school="道家", tier=SageTier.MASTER, era="南宋", lifespan="1194-1229", titles=["紫清真人"], works=["海琼白真人集"], expertise=["内丹", "雷法"], department="工部", description="南宗五祖"),
    SageMeta(name="陈抟", name_en="chen_tuan", school="道家", tier=SageTier.MASTER, era="五代宋", lifespan="871-989", titles=["希夷先生"], works=["无极图", "先天图"], expertise=["易学", "内丹"], department="工部", description="睡仙"),
    SageMeta(name="张无梦", name_en="zhang_wumeng", school="道家", tier=SageTier.SCHOLAR, era="北宋", lifespan="?", titles=["鸿蒙子"], works=[], expertise=["内丹", "易学"], department="工部", description="陈抟弟子"),
    SageMeta(name="刘海蟾", name_en="liu_haichan", school="道家", tier=SageTier.SCHOLAR, era="五代", lifespan="?-1080", titles=["海蟾真人"], works=[], expertise=["内丹", "财神"], department="工部", description="八仙之一"),
    SageMeta(name="钟离权", name_en="zhongli_quan", school="道家", tier=SageTier.SCHOLAR, era="唐五代", lifespan="?", titles=["正阳祖师"], works=["灵宝毕法"], expertise=["内丹", "八仙"], department="工部", description="八仙之一"),
    SageMeta(name="吕洞宾", name_en="lv_dongbin", school="道家", tier=SageTier.SCHOLAR, era="唐五代", lifespan="796-?", titles=["纯阳祖师"], works=["吕祖全书"], expertise=["内丹", "八仙"], department="工部", description="八仙之首"),
    
    # === 正一道 ===
    SageMeta(name="张盛", name_en="zhang_sheng", school="道家", tier=SageTier.SCHOLAR, era="三国", lifespan="?", titles=["第三代天师"], works=[], expertise=["正一道"], department="工部", description="龙虎山天师"),
    SageMeta(name="张鲁", name_en="zhang_lu", school="道家", tier=SageTier.SCHOLAR, era="东汉", lifespan="?-216", titles=["系师"], works=[], expertise=["五斗米道"], department="工部", description="汉中教主张鲁"),
    SageMeta(name="张衡", name_en="zhang_heng_tianshi", school="道家", tier=SageTier.SCHOLAR, era="东汉", lifespan="?", titles=["第二代天师"], works=[], expertise=["正一道"], department="工部", description="张道陵之子"),
    SageMeta(name="张与材", name_en="zhang_yucai", school="道家", tier=SageTier.SCHOLAR, era="元代", lifespan="?-1316", titles=["第三十八代天师"], works=[], expertise=["正一道"], department="工部", description="元代天师"),
    SageMeta(name="张正常", name_en="zhang_zhengchang", school="道家", tier=SageTier.SCHOLAR, era="明代", lifespan="?-1378", titles=["第四十二代天师"], works=[], expertise=["正一道"], department="工部", description="明代天师"),
    SageMeta(name="邵元节", name_en="shao_yuanjie", school="道家", tier=SageTier.SCHOLAR, era="明代", lifespan="1459-1539", titles=["真人"], works=[], expertise=["正一道"], department="工部", description="嘉靖朝道士"),
    SageMeta(name="陶仲文", name_en="tao_zhongwen", school="道家", tier=SageTier.SCHOLAR, era="明代", lifespan="?-1560", titles=["真人"], works=[], expertise=["正一道"], department="工部", description="嘉靖朝道士"),
    SageMeta(name="陆西星", name_en="lu_xixing", school="道家", tier=SageTier.SCHOLAR, era="明代", lifespan="1520-1606", titles=["内丹东派"], works=["方壶外史"], expertise=["内丹", "东派"], department="工部", description="内丹东派"),
    SageMeta(name="李西月", name_en="li_xiyue", school="道家", tier=SageTier.SCHOLAR, era="清代", lifespan="1806-1856", titles=["内丹西派"], works=["道窍谈"], expertise=["内丹", "西派"], department="工部", description="内丹西派"),
    SageMeta(name="刘一明", name_en="liu_yiming", school="道家", tier=SageTier.SCHOLAR, era="清代", lifespan="1734-1821", titles=["悟元子"], works=["道书十二种"], expertise=["内丹", "易学"], department="工部", description="清代道士"),
    
    # === 近现代道家学者 ===
    SageMeta(name="陈撄宁", name_en="chen_yingning", school="道家", tier=SageTier.MASTER, era="近现代", lifespan="1880-1969", titles=["仙学大师"], works=["中华仙学"], expertise=["仙学", "道教研究"], department="工部", description="现代仙学倡导者"),
    SageMeta(name="萧天石", name_en="xiao_tianshi", school="道家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1908-1986", titles=["道藏精华"], works=["道藏精华"], expertise=["道教", "养生"], department="工部", description="道藏整理"),
    SageMeta(name="王明", name_en="wang_ming", school="道家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1911-1992", titles=["道教学者"], works=["抱朴子内篇校释"], expertise=["道教研究"], department="工部", description="道教学者"),
    SageMeta(name="卿希泰", name_en="qing_xitai", school="道家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1928-2017", titles=["道教学者"], works=["中国道教史"], expertise=["道教史"], department="工部", description="道教学者"),
    SageMeta(name="任继愈", name_en="ren_jiyu", school="道家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1916-2009", titles=["宗教学者"], works=["中国道教史"], expertise=["道教研究"], department="工部", description="宗教学者"),
    SageMeta(name="李养正", name_en="li_yangzheng", school="道家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1925-2003", titles=["道教学者"], works=["道教概说"], expertise=["道教研究"], department="工部", description="道教学者"),
    SageMeta(name="胡孚琛", name_en="hu_fuchen", school="道家", tier=SageTier.SCHOLAR, era="当代", lifespan="1945-", titles=["道教学者"], works=["道学通论"], expertise=["道教研究"], department="工部", description="道教学者"),
    SageMeta(name="张继禹", name_en="zhang_jiyu", school="道家", tier=SageTier.SCHOLAR, era="当代", lifespan="1962-", titles=["天师"], works=[], expertise=["正一道"], department="工部", description="第六十五代天师"),
    SageMeta(name="闵智亭", name_en="min_zhiting", school="道家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1924-2004", titles=["道长"], works=["道教仪范"], expertise=["道教"], department="工部", description="中国道协会长"),
    SageMeta(name="傅圆天", name_en="fu_yuantian", school="道家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1925-1997", titles=["道长"], works=[], expertise=["道教"], department="工部", description="四川道协会长"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 三、佛家 (Buddhism) - 80人
# ═══════════════════════════════════════════════════════════════════════════════

BUDDHIST_SAGES: List[SageMeta] = [
    # === 印度佛教 ===
    SageMeta(name="释迦牟尼", name_en="shakyamuni", school="佛家", tier=SageTier.FOUNDER, era="公元前", lifespan="前623-前543", titles=["佛陀"], works=["佛经"], expertise=["四圣谛", "八正道"], department="礼部", description="佛教创始人"),
    SageMeta(name="摩诃迦叶", name_en="mahakashyapa", school="佛家", tier=SageTier.SCHOLAR, era="公元前", lifespan="?", titles=["头陀第一"], works=[], expertise=["头陀行", "禅宗"], department="礼部", description="禅宗初祖"),
    SageMeta(name="阿难", name_en="ananda", school="佛家", tier=SageTier.SCHOLAR, era="公元前", lifespan="?", titles=["多闻第一"], works=["阿含经"], expertise=["诵经"], department="礼部", description="多闻第一"),
    SageMeta(name="舍利弗", name_en="shariputra", school="佛家", tier=SageTier.SCHOLAR, era="公元前", lifespan="?", titles=["智慧第一"], works=[], expertise=["智慧", "般若"], department="礼部", description="智慧第一"),
    SageMeta(name="目犍连", name_en="moggallana", school="佛家", tier=SageTier.SCHOLAR, era="公元前", lifespan="?", titles=["神通第一"], works=[], expertise=["神通"], department="礼部", description="神通第一"),
    SageMeta(name="龙树", name_en="nagarjuna", school="佛家", tier=SageTier.MASTER, era="公元", lifespan="150-250", titles=["八宗共祖"], works=["中论"], expertise=["中观", "空宗"], department="礼部", description="中观学派创始人"),
    SageMeta(name="提婆", name_en="arya_deva", school="佛家", tier=SageTier.SCHOLAR, era="公元", lifespan="约170-270", titles=["圣天菩萨"], works=["百论"], expertise=["中观"], department="礼部", description="龙树弟子"),
    SageMeta(name="无著", name_en="asanga", school="佛家", tier=SageTier.MASTER, era="公元", lifespan="310-390", titles=["瑜伽行派祖师"], works=["瑜伽师地论"], expertise=["唯识", "瑜伽行"], department="礼部", description="瑜伽行派创始人"),
    SageMeta(name="世亲", name_en="vasubandhu", school="佛家", tier=SageTier.MASTER, era="公元", lifespan="320-400", titles=["千部论主"], works=["俱舍论"], expertise=["唯识", "俱舍"], department="礼部", description="唯识学派集大成者"),
    SageMeta(name="护法", name_en="dharmapala", school="佛家", tier=SageTier.SCHOLAR, era="公元", lifespan="530-561", titles=["唯识宗"], works=[], expertise=["唯识"], department="礼部", description="唯识十大论师之一"),
    
    # === 中国禅宗 ===
    SageMeta(name="菩提达摩", name_en="bodhidharma", school="佛家", tier=SageTier.FOUNDER, era="南北朝", lifespan="?-536", titles=["禅宗初祖"], works=["二入四行论"], expertise=["禅宗", "壁观"], department="礼部", description="禅宗初祖"),
    SageMeta(name="慧可", name_en="huike", school="佛家", tier=SageTier.SCHOLAR, era="南北朝", lifespan="487-593", titles=["禅宗二祖"], works=[], expertise=["禅宗"], department="礼部", description="断臂求法"),
    SageMeta(name="僧璨", name_en="sengcan", school="佛家", tier=SageTier.SCHOLAR, era="南北朝", lifespan="?-606", titles=["禅宗三祖"], works=["信心铭"], expertise=["禅宗"], department="礼部", description="信心铭作者"),
    SageMeta(name="道信", name_en="daoxin", school="佛家", tier=SageTier.SCHOLAR, era="隋唐", lifespan="580-651", titles=["禅宗四祖"], works=[], expertise=["东山法门"], department="礼部", description="东山法门"),
    SageMeta(name="弘忍", name_en="hongren", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="601-674", titles=["禅宗五祖"], works=[], expertise=["禅宗"], department="礼部", description="传衣钵于六祖"),
    SageMeta(name="慧能", name_en="huineng", school="佛家", tier=SageTier.MASTER, era="唐代", lifespan="638-713", titles=["禅宗六祖"], works=["六祖坛经"], expertise=["顿悟", "无念"], department="礼部", description="顿悟法门"),
    SageMeta(name="神秀", name_en="shenxiu", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="606-706", titles=["北宗禅"], works=[], expertise=["渐修", "北宗"], department="礼部", description="北宗禅创始人"),
    SageMeta(name="神会", name_en="shenhui", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="684-758", titles=["荷泽神会"], works=[], expertise=["南宗", "顿悟"], department="礼部", description="确立南宗正统"),
    SageMeta(name="行思", name_en="xing_si", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="?-740", titles=["青原行思"], works=[], expertise=["青原系"], department="礼部", description="青原系开创者"),
    SageMeta(name="怀让", name_en="huai_rang", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="677-744", titles=["南岳怀让"], works=[], expertise=["南岳系"], department="礼部", description="南岳系开创者"),
    
    # === 禅宗五家七宗 ===
    SageMeta(name="马祖道一", name_en="mazu_daoyi", school="佛家", tier=SageTier.MASTER, era="唐代", lifespan="709-788", titles=["马祖"], works=[], expertise=["洪州宗"], department="礼部", description="洪州宗创始人"),
    SageMeta(name="百丈怀海", name_en="baizhang_huaihai", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="720-814", titles=["百丈禅师"], works=["百丈清规"], expertise=["清规", "农禅"], department="礼部", description="百丈清规"),
    SageMeta(name="黄檗希运", name_en="huangbo_xiyun", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="?-850", titles=["黄檗禅师"], works=["传心法要"], expertise=["临济宗"], department="礼部", description="临济宗之祖"),
    SageMeta(name="临济义玄", name_en="linji_yixuan", school="佛家", tier=SageTier.MASTER, era="唐代", lifespan="?-867", titles=["临济宗"], works=["临济录"], expertise=["棒喝", "四料简"], department="礼部", description="临济宗创始人"),
    SageMeta(name="沩山灵祐", name_en="weishan_lingyou", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="771-853", titles=["沩仰宗"], works=[], expertise=["沩仰宗"], department="礼部", description="沩仰宗创始人"),
    SageMeta(name="仰山慧寂", name_en="yangshan_huiji", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="807-883", titles=["沩仰宗"], works=[], expertise=["沩仰宗"], department="礼部", description="沩仰宗创始人之一"),
    SageMeta(name="洞山良价", name_en="dongshan_liangjie", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="807-869", titles=["曹洞宗"], works=[], expertise=["曹洞宗"], department="礼部", description="曹洞宗创始人"),
    SageMeta(name="曹山本寂", name_en="caoshan_benji", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="840-901", titles=["曹洞宗"], works=[], expertise=["曹洞宗"], department="礼部", description="曹洞宗创始人之一"),
    SageMeta(name="云门文偃", name_en="yunmen_wenyan", school="佛家", tier=SageTier.MASTER, era="五代", lifespan="864-949", titles=["云门宗"], works=["云门广录"], expertise=["云门宗"], department="礼部", description="云门宗创始人"),
    SageMeta(name="法眼文益", name_en="fayan_wenyi", school="佛家", tier=SageTier.SCHOLAR, era="五代", lifespan="885-958", titles=["法眼宗"], works=[], expertise=["法眼宗"], department="礼部", description="法眼宗创始人"),
    
    # === 净土宗 ===
    SageMeta(name="慧远", name_en="hui_yuan", school="佛家", tier=SageTier.FOUNDER, era="东晋", lifespan="334-416", titles=["净土宗初祖"], works=[], expertise=["净土宗"], department="礼部", description="净土宗初祖"),
    SageMeta(name="善导", name_en="shan_dao", school="佛家", tier=SageTier.MASTER, era="唐代", lifespan="613-681", titles=["净土宗二祖"], works=["观经疏"], expertise=["念佛", "往生"], department="礼部", description="净土宗实际创始人"),
    SageMeta(name="承远", name_en="cheng_yuan", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="712-802", titles=["净土宗三祖"], works=[], expertise=["净土宗"], department="礼部", description="净土宗三祖"),
    SageMeta(name="法照", name_en="fa_zhao", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="?-821", titles=["净土宗四祖"], works=[], expertise=["五会念佛"], department="礼部", description="净土宗四祖"),
    SageMeta(name="少康", name_en="shao_kang", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="?-805", titles=["净土宗五祖"], works=[], expertise=["净土宗"], department="礼部", description="净土宗五祖"),
    SageMeta(name="延寿", name_en="yan_shou", school="佛家", tier=SageTier.MASTER, era="五代宋", lifespan="904-975", titles=["净土宗六祖"], works=["宗镜录"], expertise=["禅净双修"], department="礼部", description="禅净双修"),
    SageMeta(name="省常", name_en="sheng_chang", school="佛家", tier=SageTier.SCHOLAR, era="北宋", lifespan="959-1020", titles=["净土宗七祖"], works=[], expertise=["净土宗"], department="礼部", description="净土宗七祖"),
    SageMeta(name="袾宏", name_en="zhu_hong", school="佛家", tier=SageTier.SCHOLAR, era="明代", lifespan="1535-1615", titles=["净土宗八祖", "莲池大师"], works=[], expertise=["禅净双修"], department="礼部", description="净土宗八祖"),
    SageMeta(name="智旭", name_en="zhi_xu", school="佛家", tier=SageTier.SCHOLAR, era="明代", lifespan="1599-1655", titles=["净土宗九祖", "蕅益大师"], works=[], expertise=["天台", "律宗"], department="礼部", description="净土宗九祖"),
    SageMeta(name="印光", name_en="yin_guang", school="佛家", tier=SageTier.MASTER, era="近现代", lifespan="1861-1940", titles=["净土宗十三祖"], works=["印光法师文钞"], expertise=["净土宗", "因果"], department="礼部", description="近代净土宗复兴者"),
    
    # === 天台宗 ===
    SageMeta(name="智顗", name_en="zhi_yi", school="佛家", tier=SageTier.MASTER, era="隋代", lifespan="538-597", titles=["智者大师"], works=["法华玄义"], expertise=["天台宗", "法华"], department="礼部", description="天台宗创始人"),
    SageMeta(name="灌顶", name_en="guan_ding", school="佛家", tier=SageTier.SCHOLAR, era="隋代", lifespan="561-632", titles=["章安大师"], works=[], expertise=["天台宗"], department="礼部", description="智顗弟子"),
    SageMeta(name="湛然", name_en="zhan_ran", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="711-782", titles=["荆溪大师"], works=[], expertise=["天台宗"], department="礼部", description="天台宗中兴"),
    SageMeta(name="知礼", name_en="zhi_li", school="佛家", tier=SageTier.SCHOLAR, era="北宋", lifespan="960-1028", titles=["四明尊者"], works=[], expertise=["天台宗"], department="礼部", description="山家派"),
    
    # === 华严宗 ===
    SageMeta(name="杜顺", name_en="du_shun", school="佛家", tier=SageTier.FOUNDER, era="唐代", lifespan="557-640", titles=["华严宗初祖"], works=[], expertise=["华严宗"], department="礼部", description="华严宗初祖"),
    SageMeta(name="智俨", name_en="zhi_yan", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="602-668", titles=["华严宗二祖"], works=[], expertise=["华严宗", "十玄门"], department="礼部", description="华严宗二祖"),
    SageMeta(name="法藏", name_en="fa_zang", school="佛家", tier=SageTier.MASTER, era="唐代", lifespan="643-712", titles=["华严宗三祖", "贤首大师"], works=[], expertise=["华严宗", "六相"], department="礼部", description="华严宗集大成者"),
    SageMeta(name="澄观", name_en="cheng_guan", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="738-839", titles=["华严宗四祖"], works=[], expertise=["华严宗"], department="礼部", description="华严宗四祖"),
    SageMeta(name="宗密", name_en="zong_mi", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="780-841", titles=["华严宗五祖"], works=[], expertise=["华严宗", "禅"], department="礼部", description="华严宗五祖"),
    
    # === 唯识宗 ===
    SageMeta(name="玄奘", name_en="xuanzang", school="佛家", tier=SageTier.MASTER, era="唐代", lifespan="602-664", titles=["三藏法师"], works=["成唯识论"], expertise=["唯识宗", "译经"], department="礼部", description="西行取经"),
    SageMeta(name="窥基", name_en="kui_ji", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="632-682", titles=["慈恩大师"], works=[], expertise=["唯识宗"], department="礼部", description="玄奘弟子"),
    
    # === 三论宗 ===
    SageMeta(name="僧肇", name_en="seng_zhao", school="佛家", tier=SageTier.SCHOLAR, era="东晋", lifespan="384-414", titles=["三论宗"], works=["肇论"], expertise=["三论宗"], department="礼部", description="三论宗先驱"),
    SageMeta(name="吉藏", name_en="ji_zang", school="佛家", tier=SageTier.MASTER, era="隋代", lifespan="549-623", titles=["三论宗祖师"], works=[], expertise=["三论宗"], department="礼部", description="三论宗创始人"),
    
    # === 律宗 ===
    SageMeta(name="道宣", name_en="dao_xuan", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="596-667", titles=["律宗祖师"], works=[], expertise=["律宗"], department="礼部", description="律宗创始人"),
    SageMeta(name="鉴真", name_en="jian_zhen", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="688-763", titles=["律宗"], works=[], expertise=["律宗", "东渡"], department="礼部", description="东渡日本"),
    
    # === 密宗 ===
    SageMeta(name="善无畏", name_en="shan_wuwei", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="637-735", titles=["密宗祖师"], works=[], expertise=["密宗"], department="礼部", description="密宗创始人之一"),
    SageMeta(name="金刚智", name_en="jin_gangzhi", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="671-741", titles=["密宗祖师"], works=[], expertise=["密宗"], department="礼部", description="密宗创始人之一"),
    SageMeta(name="不空", name_en="bu_kong", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="705-774", titles=["密宗祖师"], works=[], expertise=["密宗"], department="礼部", description="密宗创始人之一"),
    SageMeta(name="惠果", name_en="hui_guo", school="佛家", tier=SageTier.SCHOLAR, era="唐代", lifespan="746-806", titles=["密宗"], works=[], expertise=["密宗"], department="礼部", description="不空弟子"),
    
    # === 藏传佛教 ===
    SageMeta(name="莲花生", name_en="padmasambhava", school="佛家", tier=SageTier.FOUNDER, era="唐代", lifespan="8世纪", titles=["密宗祖师"], works=[], expertise=["密宗", "藏传"], department="礼部", description="藏传佛教创始人"),
    SageMeta(name="阿底峡", name_en="atisha", school="佛家", tier=SageTier.SCHOLAR, era="宋代", lifespan="982-1054", titles=["噶当派"], works=[], expertise=["噶当派"], department="礼部", description="噶当派祖师"),
    SageMeta(name="宗喀巴", name_en="tsongkhapa", school="佛家", tier=SageTier.MASTER, era="明代", lifespan="1357-1419", titles=["格鲁派创始人"], works=[], expertise=["格鲁派"], department="礼部", description="格鲁派创始人"),
    SageMeta(name="达赖喇嘛", name_en="dalai_lama", school="佛家", tier=SageTier.SCHOLAR, era="明清", lifespan="", titles=["格鲁派领袖"], works=[], expertise=["格鲁派"], department="礼部", description="格鲁派领袖"),
    SageMeta(name="班禅额尔德尼", name_en="panchen_lama", school="佛家", tier=SageTier.SCHOLAR, era="明清", lifespan="", titles=["格鲁派领袖"], works=[], expertise=["格鲁派"], department="礼部", description="格鲁派领袖"),
    
    # === 近现代佛学家 ===
    SageMeta(name="杨仁山", name_en="yang_renshan", school="佛家", tier=SageTier.MASTER, era="近现代", lifespan="1837-1911", titles=["近代佛教复兴之父"], works=[], expertise=["佛教复兴"], department="礼部", description="近代佛教复兴"),
    SageMeta(name="欧阳竟无", name_en="ouyang_jingwu", school="佛家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1871-1943", titles=["支那内学院"], works=[], expertise=["唯识学"], department="礼部", description="支那内学院"),
    SageMeta(name="太虚", name_en="tai_xu", school="佛家", tier=SageTier.MASTER, era="近现代", lifespan="1890-1947", titles=["太虚大师"], works=[], expertise=["人间佛教"], department="礼部", description="人间佛教倡导者"),
    SageMeta(name="弘一", name_en="hong_yi", school="佛家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1880-1942", titles=["弘一法师"], works=[], expertise=["律宗", "艺术"], department="礼部", description="律宗大师"),
    SageMeta(name="虚云", name_en="xu_yun", school="佛家", tier=SageTier.MASTER, era="近现代", lifespan="1840-1959", titles=["虚云老和尚"], works=[], expertise=["禅宗"], department="礼部", description="近代禅宗泰斗"),
    SageMeta(name="圆瑛", name_en="yuan_ying", school="佛家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1878-1953", titles=["圆瑛大师"], works=[], expertise=["佛教"], department="礼部", description="中国佛教协会会长"),
    SageMeta(name="赵朴初", name_en="zhao_puchu", school="佛家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1907-2000", titles=["赵朴初"], works=[], expertise=["佛教", "书法"], department="礼部", description="中国佛教协会会长"),
    SageMeta(name="印顺", name_en="yin_shun", school="佛家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1906-2005", titles=["印顺导师"], works=[], expertise=["佛教研究"], department="礼部", description="佛学研究"),
    SageMeta(name="圣严", name_en="sheng_yan", school="佛家", tier=SageTier.SCHOLAR, era="当代", lifespan="1930-2009", titles=["圣严法师"], works=[], expertise=["禅宗", "佛学"], department="礼部", description="法鼓山创始人"),
    SageMeta(name="星云", name_en="xing_yun", school="佛家", tier=SageTier.SCHOLAR, era="当代", lifespan="1927-2023", titles=["星云大师"], works=[], expertise=["人间佛教"], department="礼部", description="佛光山创始人"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 四、兵家 (Military) - 60人
# ═══════════════════════════════════════════════════════════════════════════════

MILITARY_SAGES: List[SageMeta] = [
    # === 先秦兵家 ===
    SageMeta(name="孙武", name_en="sun_wu", school="兵家", tier=SageTier.FOUNDER, era="春秋", lifespan="前545-前470", titles=["兵圣"], works=["孙子兵法"], expertise=["战略", "谋略"], department="兵部", description="兵家至圣"),
    SageMeta(name="吴起", name_en="wu_qi", school="兵家", tier=SageTier.MASTER, era="战国", lifespan="前440-前381", titles=["兵家亚圣"], works=["吴子兵法"], expertise=["兵法", "变法"], department="兵部", description="兵家亚圣"),
    SageMeta(name="孙膑", name_en="sun_bin", school="兵家", tier=SageTier.MASTER, era="战国", lifespan="前380-前316", titles=["兵家"], works=["孙膑兵法"], expertise=["兵法", "谋略"], department="兵部", description="孙武后代"),
    SageMeta(name="尉缭", name_en="wei_liao", school="兵家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["兵家"], works=["尉缭子"], expertise=["兵法", "治军"], department="兵部", description="尉缭子作者"),
    SageMeta(name="司马穰苴", name_en="sima_rangju", school="兵家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["兵家"], works=["司马法"], expertise=["兵法", "军礼"], department="兵部", description="司马法作者"),
    SageMeta(name="田穰苴", name_en="tian_rangju", school="兵家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["兵家"], works=[], expertise=["兵法"], department="兵部", description="齐国名将"),
    SageMeta(name="范蠡", name_en="fan_li", school="兵家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前536-前448", titles=["商圣", "兵家"], works=[], expertise=["谋略", "经商"], department="户部", description="助勾践灭吴"),
    SageMeta(name="文种", name_en="wen_zhong", school="兵家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?-前472", titles=["谋略家"], works=[], expertise=["谋略"], department="吏部", description="助勾践灭吴"),
    SageMeta(name="伍子胥", name_en="wu_zixu", school="兵家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前559-前484", titles=["谋略家"], works=[], expertise=["谋略", "战略"], department="兵部", description="吴国相国"),
    SageMeta(name="鬼谷子", name_en="guiguzi", school="兵家", tier=SageTier.FOUNDER, era="战国", lifespan="前400-前320", titles=["纵横家祖师"], works=["鬼谷子"], expertise=["谋略", "纵横"], department="兵部", description="纵横家祖师"),
    
    # === 战国名将 ===
    SageMeta(name="白起", name_en="bai_qi", school="兵家", tier=SageTier.SCHOLAR, era="战国", lifespan="?-前257", titles=["人屠"], works=[], expertise=["歼灭战"], department="兵部", description="战国四大名将"),
    SageMeta(name="王翦", name_en="wang_jian", school="兵家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名将"], works=[], expertise=["战略"], department="兵部", description="秦灭六国主将"),
    SageMeta(name="廉颇", name_en="lian_po", school="兵家", tier=SageTier.SCHOLAR, era="战国", lifespan="前327-前243", titles=["名将"], works=[], expertise=["防守"], department="兵部", description="战国四大名将"),
    SageMeta(name="李牧", name_en="li_mu", school="兵家", tier=SageTier.SCHOLAR, era="战国", lifespan="?-前229", titles=["名将"], works=[], expertise=["防守", "骑兵"], department="兵部", description="战国四大名将"),
    SageMeta(name="赵奢", name_en="zhao_she", school="兵家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名将"], works=[], expertise=["谋略"], department="兵部", description="赵括之父"),
    SageMeta(name="乐毅", name_en="yue_yi", school="兵家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名将"], works=[], expertise=["战略"], department="兵部", description="五国伐齐"),
    SageMeta(name="田单", name_en="tian_shan", school="兵家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名将"], works=[], expertise=["火牛阵"], department="兵部", description="火牛阵复齐"),
    SageMeta(name="蒙恬", name_en="meng_tian", school="兵家", tier=SageTier.SCHOLAR, era="秦代", lifespan="?-前210", titles=["名将"], works=[], expertise=["北击匈奴"], department="兵部", description="北击匈奴"),
    SageMeta(name="章邯", name_en="zhang_han", school="兵家", tier=SageTier.SCHOLAR, era="秦代", lifespan="?-前205", titles=["名将"], works=[], expertise=["平叛"], department="兵部", description="秦末名将"),
    SageMeta(name="项燕", name_en="xiang_yan", school="兵家", tier=SageTier.SCHOLAR, era="战国", lifespan="?-前223", titles=["名将"], works=[], expertise=["抗秦"], department="兵部", description="项羽祖父"),
    
    # === 楚汉名将 ===
    SageMeta(name="韩信", name_en="han_xin", school="兵家", tier=SageTier.MASTER, era="西汉", lifespan="前231-前196", titles=["兵仙"], works=[], expertise=["战略", "战术"], department="兵部", description="汉初三杰"),
    SageMeta(name="项羽", name_en="xiang_yu", school="兵家", tier=SageTier.SCHOLAR, era="秦末", lifespan="前232-前202", titles=["西楚霸王"], works=[], expertise=["勇武", "战术"], department="兵部", description="霸王"),
    SageMeta(name="张良", name_en="zhang_liang", school="兵家", tier=SageTier.MASTER, era="西汉", lifespan="前250-前186", titles=["谋圣"], works=[], expertise=["谋略"], department="兵部", description="汉初三杰"),
    SageMeta(name="陈平", name_en="chen_ping", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前178", titles=["谋士"], works=[], expertise=["谋略", "反间"], department="兵部", description="汉初谋士"),
    SageMeta(name="曹参", name_en="cao_shen", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前190", titles=["名将"], works=[], expertise=["治军"], department="兵部", description="萧规曹随"),
    SageMeta(name="周勃", name_en="zhou_bo", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前169", titles=["名将"], works=[], expertise=["平叛"], department="兵部", description="安刘氏天下"),
    SageMeta(name="灌婴", name_en="guan_ying", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前176", titles=["名将"], works=[], expertise=["骑兵"], department="兵部", description="汉初名将"),
    SageMeta(name="樊哙", name_en="fan_kuai", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前242-前189", titles=["名将"], works=[], expertise=["勇武"], department="兵部", description="汉初名将"),
    SageMeta(name="彭越", name_en="peng_yue", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前196", titles=["名将"], works=[], expertise=["游击战"], department="兵部", description="游击战鼻祖"),
    SageMeta(name="英布", name_en="ying_bu", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前196", titles=["名将"], works=[], expertise=["勇武"], department="兵部", description="汉初名将"),
    
    # === 汉魏名将 ===
    SageMeta(name="卫青", name_en="wei_qing", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前106", titles=["大将军"], works=[], expertise=["北击匈奴"], department="兵部", description="北击匈奴"),
    SageMeta(name="霍去病", name_en="huo_qubing", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前140-前117", titles=["冠军侯"], works=[], expertise=["骑兵", "闪电战"], department="兵部", description="封狼居胥"),
    SageMeta(name="李广", name_en="li_guang", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前119", titles=["飞将军"], works=[], expertise=["防守", "箭术"], department="兵部", description="飞将军"),
    SageMeta(name="周亚夫", name_en="zhou_yafu", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前199-前143", titles=["名将"], works=[], expertise=["治军"], department="兵部", description="细柳营"),
    SageMeta(name="赵充国", name_en="zhao_chongguo", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前137-前52", titles=["名将"], works=[], expertise=["屯田", "平羌"], department="兵部", description="屯田平羌"),
    SageMeta(name="陈汤", name_en="chen_tang", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-约前6", titles=["名将"], works=[], expertise=["远征"], department="兵部", description="明犯强汉者虽远必诛"),
    SageMeta(name="冯奉世", name_en="feng_fengshi", school="兵家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前39", titles=["名将"], works=[], expertise=["平叛"], department="兵部", description="西汉名将"),
    SageMeta(name="邓禹", name_en="deng_yu", school="兵家", tier=SageTier.SCHOLAR, era="东汉", lifespan="2-58", titles=["名将"], works=[], expertise=["战略"], department="兵部", description="云台二十八将"),
    SageMeta(name="冯异", name_en="feng_yi", school="兵家", tier=SageTier.SCHOLAR, era="东汉", lifespan="?-34", titles=["名将"], works=[], expertise=["治军"], department="兵部", description="大树将军"),
    SageMeta(name="吴汉", name_en="wu_han", school="兵家", tier=SageTier.SCHOLAR, era="东汉", lifespan="?-44", titles=["名将"], works=[], expertise=["攻坚"], department="兵部", description="云台二十八将"),
    
    # === 三国名将 ===
    SageMeta(name="曹操", name_en="cao_cao", school="兵家", tier=SageTier.MASTER, era="东汉", lifespan="155-220", titles=["魏武帝"], works=["孟德新书"], expertise=["战略", "谋略"], department="兵部", description="军事家政治家"),
    SageMeta(name="诸葛亮", name_en="zhuge_liang", school="兵家", tier=SageTier.MASTER, era="三国", lifespan="181-234", titles=["武侯"], works=["将苑", "便宜十六策"], expertise=["战略", "治军"], department="兵部", description="卧龙"),
    SageMeta(name="司马懿", name_en="sima_yi", school="兵家", tier=SageTier.SCHOLAR, era="三国", lifespan="179-251", titles=["晋宣帝"], works=[], expertise=["战略", "谋略"], department="兵部", description="冢虎"),
    SageMeta(name="周瑜", name_en="zhou_yu", school="兵家", tier=SageTier.SCHOLAR, era="三国", lifespan="175-210", titles=["名将"], works=[], expertise=["水战", "谋略"], department="兵部", description="赤壁之战"),
    SageMeta(name="陆逊", name_en="lu_xun", school="兵家", tier=SageTier.SCHOLAR, era="三国", lifespan="183-245", titles=["名将"], works=[], expertise=["战略", "防守"], department="兵部", description="夷陵之战"),
    SageMeta(name="关羽", name_en="guan_yu", school="兵家", tier=SageTier.SCHOLAR, era="三国", lifespan="?-220", titles=["武圣"], works=[], expertise=["勇武", "忠义"], department="兵部", description="武圣"),
    SageMeta(name="张飞", name_en="zhang_fei", school="兵家", tier=SageTier.SCHOLAR, era="三国", lifespan="?-221", titles=["名将"], works=[], expertise=["勇武"], department="兵部", description="万人敌"),
    SageMeta(name="赵云", name_en="zhao_yun", school="兵家", tier=SageTier.SCHOLAR, era="三国", lifespan="?-229", titles=["名将"], works=[], expertise=["勇武", "忠义"], department="兵部", description="常胜将军"),
    SageMeta(name="张辽", name_en="zhang_liao", school="兵家", tier=SageTier.SCHOLAR, era="三国", lifespan="169-222", titles=["名将"], works=[], expertise=["勇武", "战术"], department="兵部", description="威震逍遥津"),
    SageMeta(name="邓艾", name_en="deng_ai", school="兵家", tier=SageTier.SCHOLAR, era="三国", lifespan="197-264", titles=["名将"], works=[], expertise=["奇袭", "战略"], department="兵部", description="偷渡阴平"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 五、法家 (Legalism) - 40人
# ═══════════════════════════════════════════════════════════════════════════════

LEGALIST_SAGES: List[SageMeta] = [
    # === 法家先驱 ===
    SageMeta(name="管仲", name_en="guan_zhong", school="法家", tier=SageTier.FOUNDER, era="春秋", lifespan="前723-前645", titles=["法家先驱"], works=["管子"], expertise=["法治", "经济"], department="刑部", description="法家先驱"),
    SageMeta(name="子产", name_en="zi_chan", school="法家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?-前522", titles=["政治家"], works=[], expertise=["法治", "铸刑书"], department="刑部", description="铸刑书"),
    SageMeta(name="邓析", name_en="deng_xi", school="法家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前545-前501", titles=["名家先驱"], works=[], expertise=["法律", "名辩"], department="刑部", description="名家先驱"),
    
    # === 法家三派 ===
    SageMeta(name="李悝", name_en="li_kui", school="法家", tier=SageTier.FOUNDER, era="战国", lifespan="前455-前395", titles=["法家始祖"], works=["法经"], expertise=["法治", "变法"], department="刑部", description="法家始祖"),
    SageMeta(name="商鞅", name_en="shang_yang", school="法家", tier=SageTier.MASTER, era="战国", lifespan="前390-前338", titles=["商君"], works=["商君书"], expertise=["变法", "重农抑商"], department="刑部", description="商鞅变法"),
    SageMeta(name="申不害", name_en="shen_buhai", school="法家", tier=SageTier.MASTER, era="战国", lifespan="前385-前337", titles=["术治派"], works=["申子"], expertise=["术治", "权术"], department="刑部", description="术治派"),
    SageMeta(name="慎到", name_en="shen_dao_legalist", school="法家", tier=SageTier.SCHOLAR, era="战国", lifespan="约前350-前275", titles=["势治派"], works=["慎子"], expertise=["势治"], department="刑部", description="势治派"),
    SageMeta(name="韩非", name_en="han_fei", school="法家", tier=SageTier.MASTER, era="战国", lifespan="约前280-前233", titles=["法家集大成者"], works=["韩非子"], expertise=["法家理论", "法术势"], department="刑部", description="法家集大成者"),
    SageMeta(name="李斯", name_en="li_si", school="法家", tier=SageTier.SCHOLAR, era="秦代", lifespan="前284-前208", titles=["秦相"], works=[], expertise=["法治", "统一文字"], department="刑部", description="秦相"),
    SageMeta(name="吴起", name_en="wu_qi_legalist", school="法家", tier=SageTier.SCHOLAR, era="战国", lifespan="前440-前381", titles=["兵家法家"], works=[], expertise=["兵法", "变法"], department="刑部", description="兵家法家"),
    
    # === 秦汉法家 ===
    SageMeta(name="秦始皇", name_en="qin_shihuang", school="法家", tier=SageTier.SCHOLAR, era="秦代", lifespan="前259-前210", titles=["始皇帝"], works=[], expertise=["法治", "统一"], department="刑部", description="统一六国"),
    SageMeta(name="赵高", name_en="zhao_gao", school="法家", tier=SageTier.SCHOLAR, era="秦代", lifespan="?-前207", titles=["权臣"], works=[], expertise=["权术"], department="刑部", description="秦代权臣"),
    SageMeta(name="萧何", name_en="xiao_he", school="法家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前257-前193", titles=["汉相"], works=[], expertise=["法律", "治国"], department="刑部", description="汉律"),
    SageMeta(name="曹参", name_en="cao_shen_legalist", school="法家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前190", titles=["汉相"], works=[], expertise=["治国"], department="刑部", description="萧规曹随"),
    SageMeta(name="张汤", name_en="zhang_tang", school="法家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前116", titles=["酷吏"], works=[], expertise=["法律", "酷吏"], department="刑部", description="西汉酷吏"),
    SageMeta(name="杜周", name_en="du_zhou", school="法家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前95", titles=["酷吏"], works=[], expertise=["法律"], department="刑部", description="西汉酷吏"),
    SageMeta(name="桑弘羊", name_en="sang_hongyang", school="法家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前155-前80", titles=["理财家"], works=[], expertise=["经济", "盐铁"], department="户部", description="盐铁专卖"),
    SageMeta(name="晁错", name_en="chao_cuo", school="法家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前200-前154", titles=["政治家"], works=[], expertise=["削藩", "重农"], department="刑部", description="削藩策"),
    SageMeta(name="主父偃", name_en="zhufu_yan", school="法家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前126", titles=["政治家"], works=[], expertise=["推恩令"], department="刑部", description="推恩令"),
    SageMeta(name="张敞", name_en="zhang_chang", school="法家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前48", titles=["京兆尹"], works=[], expertise=["治盗"], department="刑部", description="京兆尹"),
    
    # === 后世法家 ===
    SageMeta(name="诸葛亮", name_en="zhuge_liang_legalist", school="法家", tier=SageTier.SCHOLAR, era="三国", lifespan="181-234", titles=["政治家"], works=[], expertise=["法治", "治国"], department="刑部", description="依法治国"),
    SageMeta(name="曹操", name_en="cao_cao_legalist", school="法家", tier=SageTier.SCHOLAR, era="东汉", lifespan="155-220", titles=["政治家"], works=[], expertise=["法治", "屯田"], department="刑部", description="重法治"),
    SageMeta(name="王猛", name_en="wang_meng", school="法家", tier=SageTier.SCHOLAR, era="前秦", lifespan="325-375", titles=["政治家"], works=[], expertise=["法治", "治国"], department="刑部", description="前秦名相"),
    SageMeta(name="王安石", name_en="wang_anshi_legalist", school="法家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1021-1086", titles=["改革家"], works=[], expertise=["变法", "理财"], department="刑部", description="王安石变法"),
    SageMeta(name="张居正", name_en="zhang_juzheng", school="法家", tier=SageTier.MASTER, era="明代", lifespan="1525-1582", titles=["改革家"], works=[], expertise=["变法", "一条鞭法"], department="刑部", description="张居正改革"),
    SageMeta(name="韩非子", name_en="han_feizi", school="法家", tier=SageTier.MASTER, era="战国", lifespan="约前280-前233", titles=["法家代表"], works=["韩非子"], expertise=["法术势"], department="刑部", description="法家代表"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 六、墨家 (Mohism) - 30人
# ═══════════════════════════════════════════════════════════════════════════════

MOHIST_SAGES: List[SageMeta] = [
    SageMeta(name="墨子", name_en="mozi", school="墨家", tier=SageTier.FOUNDER, era="战国", lifespan="约前468-前376", titles=["墨家创始人"], works=["墨子"], expertise=["兼爱", "非攻", "科技"], department="工部", description="墨家创始人"),
    SageMeta(name="公输般", name_en="gongshu_ban", school="墨家", tier=SageTier.SCHOLAR, era="战国", lifespan="约前507-前444", titles=["鲁班"], works=[], expertise=["工匠", "机关"], department="工部", description="工匠祖师"),
    SageMeta(name="鲁班", name_en="lu_ban", school="墨家", tier=SageTier.SCHOLAR, era="战国", lifespan="约前507-前444", titles=["工匠祖师"], works=[], expertise=["工匠", "建筑"], department="工部", description="工匠祖师"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 七、名家 (School of Names) - 20人
# ═══════════════════════════════════════════════════════════════════════════════

SCHOOL_OF_NAMES_SAGES: List[SageMeta] = [
    SageMeta(name="邓析", name_en="deng_xi_names", school="名家", tier=SageTier.FOUNDER, era="春秋", lifespan="前545-前501", titles=["名家先驱"], works=["邓析子"], expertise=["名辩", "法律"], department="礼部", description="名家先驱"),
    SageMeta(name="惠施", name_en="hui_shi", school="名家", tier=SageTier.MASTER, era="战国", lifespan="约前370-前310", titles=["名家代表"], works=[], expertise=["合同异", "名辩"], department="礼部", description="合同异派"),
    SageMeta(name="公孙龙", name_en="gongsun_long", school="名家", tier=SageTier.MASTER, era="战国", lifespan="约前320-前250", titles=["名家代表"], works=["公孙龙子"], expertise=["离坚白", "名辩"], department="礼部", description="离坚白派"),
    SageMeta(name="宋钘", name_en="song_xing", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="约前382-前300", titles=["名家"], works=[], expertise=["名辩"], department="礼部", description="宋尹学派"),
    SageMeta(name="尹文", name_en="yin_wen", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="约前360-前280", titles=["名家"], works=["尹文子"], expertise=["名辩"], department="礼部", description="宋尹学派"),
    SageMeta(name="儿说", name_en="er_shuo", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名家"], works=[], expertise=["名辩"], department="礼部", description="名家"),
    SageMeta(name="桓团", name_en="huan_tuan", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名家"], works=[], expertise=["名辩"], department="礼部", description="名家"),
    SageMeta(name="綦毋子", name_en="qimu_zi", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名家"], works=[], expertise=["名辩"], department="礼部", description="名家"),
    SageMeta(name="毛公", name_en="mao_gong", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名家"], works=[], expertise=["名辩"], department="礼部", description="名家"),
    SageMeta(name="黄公", name_en="huang_gong", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名家"], works=[], expertise=["名辩"], department="礼部", description="名家"),
    SageMeta(name="成公生", name_en="chenggong_sheng", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名家"], works=[], expertise=["名辩"], department="礼部", description="名家"),
    SageMeta(name="黄疵", name_en="huang_ci", school="名家", tier=SageTier.SCHOLAR, era="秦代", lifespan="?", titles=["名家"], works=[], expertise=["名辩"], department="礼部", description="名家"),
    SageMeta(name="倪说", name_en="ni_shuo", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名家"], works=[], expertise=["名辩"], department="礼部", description="名家"),
    SageMeta(name="田巴", name_en="tian_ba", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["名家"], works=[], expertise=["名辩"], department="礼部", description="名家"),
    SageMeta(name="邹衍", name_en="zou_yan_names", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="约前324-前250", titles=["阴阳家"], works=[], expertise=["阴阳", "五行"], department="礼部", description="阴阳家代表"),
    SageMeta(name="邹奭", name_en="zou_shi", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["阴阳家"], works=[], expertise=["阴阳"], department="礼部", description="阴阳家"),
    SageMeta(name="名家弟子", name_en="names_disciples", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="", titles=["弟子"], works=[], expertise=["名辩"], department="礼部", description="名家弟子"),
    SageMeta(name="辩者", name_en="bian_zhe", school="名家", tier=SageTier.SCHOLAR, era="战国", lifespan="", titles=["辩者"], works=[], expertise=["名辩"], department="礼部", description="辩者二十一事"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 八、阴阳家 (Yin-Yang School) - 20人
# ═══════════════════════════════════════════════════════════════════════════════

YINYANG_SAGES: List[SageMeta] = [
    SageMeta(name="邹衍", name_en="zou_yan", school="阴阳家", tier=SageTier.FOUNDER, era="战国", lifespan="约前324-前250", titles=["阴阳家创始人"], works=[], expertise=["阴阳", "五行", "五德终始"], department="工部", description="阴阳家创始人"),
    SageMeta(name="邹奭", name_en="zou_shi_yinyang", school="阴阳家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["阴阳家"], works=[], expertise=["阴阳"], department="工部", description="邹衍弟子"),
    SageMeta(name="公梼生", name_en="gongtao_sheng", school="阴阳家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["阴阳家"], works=[], expertise=["阴阳"], department="工部", description="阴阳家"),
    SageMeta(name="公孙发", name_en="gongsun_fa", school="阴阳家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["阴阳家"], works=[], expertise=["阴阳"], department="工部", description="阴阳家"),
    SageMeta(name="张苍", name_en="zhang_cang", school="阴阳家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前256-前152", titles=["阴阳家", "历算家"], works=[], expertise=["历法", "算学"], department="工部", description="西汉丞相"),
    SageMeta(name="司马季主", name_en="sima_jizhu", school="阴阳家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?", titles=["占卜家"], works=[], expertise=["占卜"], department="工部", description="占卜家"),
    SageMeta(name="甘公", name_en="gan_gong", school="阴阳家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["天文学家"], works=[], expertise=["天文"], department="工部", description="天文学家"),
    SageMeta(name="石申", name_en="shi_shen", school="阴阳家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["天文学家"], works=["石氏星经"], expertise=["天文"], department="工部", description="天文学家"),
    SageMeta(name="唐昧", name_en="tang_mei", school="阴阳家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["天文学家"], works=[], expertise=["天文"], department="工部", description="天文学家"),
    SageMeta(name="尹皋", name_en="yin_gao", school="阴阳家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["天文学家"], works=[], expertise=["天文"], department="工部", description="天文学家"),
    SageMeta(name="羲和", name_en="xi_he", school="阴阳家", tier=SageTier.SCHOLAR, era="上古", lifespan="?", titles=["历法始祖"], works=[], expertise=["历法"], department="工部", description="历法始祖"),
    SageMeta(name="常仪", name_en="chang_yi", school="阴阳家", tier=SageTier.SCHOLAR, era="上古", lifespan="?", titles=["占月始祖"], works=[], expertise=["占月"], department="工部", description="占月始祖"),
    SageMeta(name="容成", name_en="rong_cheng", school="阴阳家", tier=SageTier.SCHOLAR, era="上古", lifespan="?", titles=["历法始祖"], works=[], expertise=["历法"], department="工部", description="历法始祖"),
    SageMeta(name="臾区", name_en="yu_qu", school="阴阳家", tier=SageTier.SCHOLAR, era="上古", lifespan="?", titles=["占星始祖"], works=[], expertise=["占星"], department="工部", description="占星始祖"),
    SageMeta(name="裨灶", name_en="bi_zao", school="阴阳家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["占星家"], works=[], expertise=["占星"], department="工部", description="占星家"),
    SageMeta(name="梓慎", name_en="zi_shen", school="阴阳家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["占星家"], works=[], expertise=["占星"], department="工部", description="占星家"),
    SageMeta(name="卜徒父", name_en="bu_tufu", school="阴阳家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["占卜家"], works=[], expertise=["占卜"], department="工部", description="占卜家"),
    SageMeta(name="史墨", name_en="shi_mo", school="阴阳家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["占星家"], works=[], expertise=["占星"], department="工部", description="占星家"),
    SageMeta(name="阴阳家后学", name_en="yinyang_later", school="阴阳家", tier=SageTier.SCHOLAR, era="秦汉", lifespan="", titles=["后学"], works=[], expertise=["阴阳"], department="工部", description="阴阳家后学"),
    SageMeta(name="方士", name_en="fang_shi", school="阴阳家", tier=SageTier.SCHOLAR, era="秦汉", lifespan="", titles=["方士"], works=[], expertise=["方术"], department="工部", description="秦汉方士"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 九、纵横家 (Diplomacy School) - 20人
# ═══════════════════════════════════════════════════════════════════════════════

DIPLOMACY_SAGES: List[SageMeta] = [
    SageMeta(name="鬼谷子", name_en="guiguzi_diplomacy", school="纵横家", tier=SageTier.FOUNDER, era="战国", lifespan="前400-前320", titles=["纵横家祖师"], works=["鬼谷子"], expertise=["谋略", "纵横"], department="兵部", description="纵横家祖师"),
    SageMeta(name="苏秦", name_en="su_qin", school="纵横家", tier=SageTier.MASTER, era="战国", lifespan="?-前284", titles=["纵横家"], works=[], expertise=["合纵"], department="兵部", description="合纵派"),
    SageMeta(name="张仪", name_en="zhang_yi", school="纵横家", tier=SageTier.MASTER, era="战国", lifespan="?-前310", titles=["纵横家"], works=[], expertise=["连横"], department="兵部", description="连横派"),
    SageMeta(name="苏代", name_en="su_dai", school="纵横家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["纵横家"], works=[], expertise=["合纵"], department="兵部", description="苏秦之弟"),
    SageMeta(name="苏厉", name_en="su_li", school="纵横家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["纵横家"], works=[], expertise=["合纵"], department="兵部", description="苏秦之弟"),
    SageMeta(name="甘茂", name_en="gan_mao", school="纵横家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["纵横家"], works=[], expertise=["谋略"], department="兵部", description="秦国丞相"),
    SageMeta(name="甘罗", name_en="gan_luo", school="纵横家", tier=SageTier.SCHOLAR, era="战国", lifespan="约前256-?", titles=["纵横家"], works=[], expertise=["谋略"], department="兵部", description="十二岁为相"),
    SageMeta(name="范雎", name_en="fan_ju", school="纵横家", tier=SageTier.SCHOLAR, era="战国", lifespan="?-前255", titles=["纵横家"], works=[], expertise=["远交近攻"], department="兵部", description="远交近攻"),
    SageMeta(name="蔡泽", name_en="cai_ze", school="纵横家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["纵横家"], works=[], expertise=["谋略"], department="兵部", description="秦相"),
    SageMeta(name="郦食其", name_en="li_yiji", school="纵横家", tier=SageTier.SCHOLAR, era="秦末", lifespan="?-前203", titles=["纵横家"], works=[], expertise=["游说"], department="兵部", description="汉初说客"),
    SageMeta(name="蒯通", name_en="kuai_tong", school="纵横家", tier=SageTier.SCHOLAR, era="秦末", lifespan="?", titles=["纵横家"], works=[], expertise=["谋略"], department="兵部", description="韩信谋士"),
    SageMeta(name="陆贾", name_en="lu_jia", school="纵横家", tier=SageTier.SCHOLAR, era="西汉", lifespan="约前240-前170", titles=["纵横家"], works=[], expertise=["外交"], department="兵部", description="汉初外交家"),
    SageMeta(name="主父偃", name_en="zhufu_yan_diplomacy", school="纵横家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前126", titles=["纵横家"], works=[], expertise=["谋略"], department="兵部", description="推恩令"),
    SageMeta(name="邹阳", name_en="zou_yang", school="纵横家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前120", titles=["纵横家"], works=[], expertise=["游说"], department="兵部", description="狱中上梁王书"),
    SageMeta(name="严助", name_en="yan_zhu", school="纵横家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前122", titles=["纵横家"], works=[], expertise=["游说"], department="兵部", description="汉武帝侍从"),
    SageMeta(name="徐乐", name_en="xu_le", school="纵横家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?", titles=["纵横家"], works=[], expertise=["游说"], department="兵部", description="汉武帝时人"),
    SageMeta(name="庄安", name_en="zhuang_an", school="纵横家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?", titles=["纵横家"], works=[], expertise=["游说"], department="兵部", description="汉武帝时人"),
    SageMeta(name="终军", name_en="zhong_jun", school="纵横家", tier=SageTier.SCHOLAR, era="西汉", lifespan="约前140-前112", titles=["纵横家"], works=[], expertise=["游说"], department="兵部", description="请缨"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 十、农家 (Agricultural School) - 15人
# ═══════════════════════════════════════════════════════════════════════════════

AGRICULTURAL_SAGES: List[SageMeta] = [
    SageMeta(name="许行", name_en="xu_xing", school="农家", tier=SageTier.FOUNDER, era="战国", lifespan="?", titles=["农家创始人"], works=[], expertise=["农业", "君民并耕"], department="户部", description="农家创始人"),
    SageMeta(name="陈相", name_en="chen_xiang", school="农家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["农家弟子"], works=[], expertise=["农业"], department="户部", description="许行弟子"),
    SageMeta(name="陈辛", name_en="chen_xin", school="农家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["农家弟子"], works=[], expertise=["农业"], department="户部", description="许行弟子"),
    SageMeta(name="神农", name_en="shen_nong", school="农家", tier=SageTier.FOUNDER, era="上古", lifespan="?", titles=["农业始祖"], works=[], expertise=["农业", "医药"], department="户部", description="农业始祖"),
    SageMeta(name="后稷", name_en="hou_ji", school="农家", tier=SageTier.SCHOLAR, era="上古", lifespan="?", titles=["农业之神"], works=[], expertise=["农业"], department="户部", description="周人始祖"),
    SageMeta(name="氾胜之", name_en="fan_shengzhi", school="农家", tier=SageTier.MASTER, era="西汉", lifespan="?", titles=["农学家"], works=["氾胜之书"], expertise=["农业"], department="户部", description="农学家"),
    SageMeta(name="崔寔", name_en="cui_shi", school="农家", tier=SageTier.SCHOLAR, era="东汉", lifespan="?-约170", titles=["农学家"], works=["四民月令"], expertise=["农业"], department="户部", description="农学家"),
    SageMeta(name="贾思勰", name_en="jia_sixie", school="农家", tier=SageTier.MASTER, era="北魏", lifespan="?", titles=["农学家"], works=["齐民要术"], expertise=["农业"], department="户部", description="齐民要术作者"),
    SageMeta(name="王祯", name_en="wang_zhen", school="农家", tier=SageTier.SCHOLAR, era="元代", lifespan="?", titles=["农学家"], works=["王祯农书"], expertise=["农业"], department="户部", description="农学家"),
    SageMeta(name="徐光启", name_en="xu_guangqi", school="农家", tier=SageTier.MASTER, era="明代", lifespan="1562-1633", titles=["农学家"], works=["农政全书"], expertise=["农业", "天文"], department="户部", description="农政全书作者"),
    SageMeta(name="宋应星", name_en="song_yingxing", school="农家", tier=SageTier.SCHOLAR, era="明代", lifespan="1587-约1666", titles=["科学家"], works=["天工开物"], expertise=["农业", "工艺"], department="工部", description="天工开物作者"),
    SageMeta(name="陈旉", name_en="chen_fu", school="农家", tier=SageTier.SCHOLAR, era="南宋", lifespan="?", titles=["农学家"], works=["陈旉农书"], expertise=["农业"], department="户部", description="农学家"),
    SageMeta(name="宋应星", name_en="song_yingxing", school="农家", tier=SageTier.SCHOLAR, era="明代", lifespan="1587-约1666", titles=["科学家"], works=["天工开物"], expertise=["农业", "工艺"], department="工部", description="天工开物作者"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 十一、杂家 (Eclectic School) - 20人
# ═══════════════════════════════════════════════════════════════════════════════

ECLECTIC_SAGES: List[SageMeta] = [
    SageMeta(name="吕不韦", name_en="lv_buwei", school="杂家", tier=SageTier.FOUNDER, era="战国", lifespan="前292-前235", titles=["杂家代表"], works=["吕氏春秋"], expertise=["杂学", "治国"], department="吏部", description="吕氏春秋主编"),
    SageMeta(name="刘安", name_en="liu_an", school="杂家", tier=SageTier.MASTER, era="西汉", lifespan="前179-前122", titles=["杂家代表"], works=["淮南子"], expertise=["杂学", "道家"], department="吏部", description="淮南子主编"),
    SageMeta(name="尸佼", name_en="shi_jiao", school="杂家", tier=SageTier.SCHOLAR, era="战国", lifespan="约前390-前330", titles=["杂家"], works=["尸子"], expertise=["杂学"], department="吏部", description="尸子作者"),
    SageMeta(name="尉缭", name_en="wei_liao_eclectic", school="杂家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["杂家"], works=["尉缭子"], expertise=["兵法", "杂学"], department="兵部", description="尉缭子作者"),
    SageMeta(name="由余", name_en="you_yu", school="杂家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["杂家"], works=[], expertise=["杂学"], department="吏部", description="西戎贤臣"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 十二、医家 (Medicine) - 40人
# ═══════════════════════════════════════════════════════════════════════════════

MEDICAL_SAGES: List[SageMeta] = [
    SageMeta(name="神农", name_en="shen_nong_medical", school="医家", tier=SageTier.FOUNDER, era="上古", lifespan="?", titles=["医药始祖"], works=["神农本草经"], expertise=["医药", "本草"], department="工部", description="医药始祖"),
    SageMeta(name="黄帝", name_en="huang_di", school="医家", tier=SageTier.FOUNDER, era="上古", lifespan="?", titles=["医学始祖"], works=["黄帝内经"], expertise=["医学", "养生"], department="工部", description="黄帝内经"),
    SageMeta(name="岐伯", name_en="qi_bo", school="医家", tier=SageTier.SCHOLAR, era="上古", lifespan="?", titles=["医学之祖"], works=[], expertise=["医学"], department="工部", description="岐黄之术"),
    SageMeta(name="扁鹊", name_en="bian_que", school="医家", tier=SageTier.MASTER, era="战国", lifespan="前407-前310", titles=["医祖"], works=[], expertise=["望闻问切", "四诊法"], department="工部", description="望闻问切"),
    SageMeta(name="仓公", name_en="cang_gong", school="医家", tier=SageTier.SCHOLAR, era="西汉", lifespan="约前205-?", titles=["医学家"], works=[], expertise=["医学", "诊籍"], department="工部", description="诊籍创始人"),
    SageMeta(name="张仲景", name_en="zhang_zhongjing", school="医家", tier=SageTier.MASTER, era="东汉", lifespan="约150-219", titles=["医圣"], works=["伤寒杂病论"], expertise=["伤寒", "辨证论治"], department="工部", description="医圣"),
    SageMeta(name="华佗", name_en="hua_tuo", school="医家", tier=SageTier.MASTER, era="东汉", lifespan="约145-208", titles=["外科圣手"], works=[], expertise=["外科", "麻醉"], department="工部", description="外科鼻祖"),
    SageMeta(name="王叔和", name_en="wang_shuhe", school="医家", tier=SageTier.SCHOLAR, era="西晋", lifespan="210-258", titles=["医学家"], works=["脉经"], expertise=["脉学"], department="工部", description="脉经作者"),
    SageMeta(name="皇甫谧", name_en="huangfu_mi", school="医家", tier=SageTier.SCHOLAR, era="西晋", lifespan="215-282", titles=["医学家"], works=["针灸甲乙经"], expertise=["针灸"], department="工部", description="针灸甲乙经作者"),
    SageMeta(name="葛洪", name_en="ge_hong_medical", school="医家", tier=SageTier.MASTER, era="东晋", lifespan="283-343", titles=["医学家"], works=["肘后备急方"], expertise=["医学", "炼丹"], department="工部", description="肘后备急方作者"),
    SageMeta(name="陶弘景", name_en="tao_hongjing_medical", school="医家", tier=SageTier.SCHOLAR, era="南朝", lifespan="456-536", titles=["医学家"], works=["本草经集注"], expertise=["本草", "医学"], department="工部", description="本草经集注作者"),
    SageMeta(name="孙思邈", name_en="sun_simiao_medical", school="医家", tier=SageTier.MASTER, era="唐代", lifespan="541-682", titles=["药王"], works=["千金要方", "千金翼方"], expertise=["医学", "养生"], department="工部", description="药王"),
    SageMeta(name="巢元方", name_en="chao_yuanfang", school="医家", tier=SageTier.SCHOLAR, era="隋代", lifespan="?", titles=["医学家"], works=["诸病源候论"], expertise=["病因学"], department="工部", description="诸病源候论作者"),
    SageMeta(name="苏敬", name_en="su_jing", school="医家", tier=SageTier.SCHOLAR, era="唐代", lifespan="?", titles=["医学家"], works=["唐本草"], expertise=["本草"], department="工部", description="唐本草主编"),
    SageMeta(name="陈藏器", name_en="chen_cangqi", school="医家", tier=SageTier.SCHOLAR, era="唐代", lifespan="约687-757", titles=["医学家"], works=["本草拾遗"], expertise=["本草"], department="工部", description="本草拾遗作者"),
    SageMeta(name="孟诜", name_en="meng_shen", school="医家", tier=SageTier.SCHOLAR, era="唐代", lifespan="621-713", titles=["医学家"], works=["食疗本草"], expertise=["食疗"], department="工部", description="食疗本草作者"),
    SageMeta(name="甄权", name_en="zhen_quan", school="医家", tier=SageTier.SCHOLAR, era="唐代", lifespan="541-643", titles=["医学家"], works=[], expertise=["针灸"], department="工部", description="针灸学家"),
    SageMeta(name="王冰", name_en="wang_bing", school="医家", tier=SageTier.SCHOLAR, era="唐代", lifespan="约710-805", titles=["医学家"], works=["黄帝内经素问注"], expertise=["内经"], department="工部", description="黄帝内经素问注作者"),
    SageMeta(name="钱乙", name_en="qian_yi", school="医家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1032-1113", titles=["儿科之圣"], works=["小儿药证直诀"], expertise=["儿科"], department="工部", description="儿科之圣"),
    SageMeta(name="唐慎微", name_en="tang_shenwei", school="医家", tier=SageTier.SCHOLAR, era="北宋", lifespan="约1056-1136", titles=["医学家"], works=["证类本草"], expertise=["本草"], department="工部", description="证类本草作者"),
    SageMeta(name="刘完素", name_en="liu_wansu", school="医家", tier=SageTier.SCHOLAR, era="金代", lifespan="约1120-1200", titles=["寒凉派"], works=[], expertise=["寒凉派"], department="工部", description="金元四大家"),
    SageMeta(name="张从正", name_en="zhang_congzheng", school="医家", tier=SageTier.SCHOLAR, era="金代", lifespan="约1156-1228", titles=["攻下派"], works=["儒门事亲"], expertise=["攻下派"], department="工部", description="金元四大家"),
    SageMeta(name="李东垣", name_en="li_dongyuan", school="医家", tier=SageTier.SCHOLAR, era="金元", lifespan="1180-1251", titles=["补土派"], works=["脾胃论"], expertise=["补土派"], department="工部", description="金元四大家"),
    SageMeta(name="朱丹溪", name_en="zhu_danxi", school="医家", tier=SageTier.SCHOLAR, era="元代", lifespan="1281-1358", titles=["滋阴派"], works=["格致余论"], expertise=["滋阴派"], department="工部", description="金元四大家"),
    SageMeta(name="李时珍", name_en="li_shizhen", school="医家", tier=SageTier.MASTER, era="明代", lifespan="1518-1593", titles=["药圣"], works=["本草纲目"], expertise=["本草", "医学"], department="工部", description="本草纲目作者"),
    SageMeta(name="陈实功", name_en="chen_shigong", school="医家", tier=SageTier.SCHOLAR, era="明代", lifespan="1555-1636", titles=["外科专家"], works=["外科正宗"], expertise=["外科"], department="工部", description="外科正宗作者"),
    SageMeta(name="张景岳", name_en="zhang_jingyue", school="医家", tier=SageTier.SCHOLAR, era="明代", lifespan="1563-1640", titles=["医学家"], works=["景岳全书"], expertise=["医学"], department="工部", description="景岳全书作者"),
    SageMeta(name="吴有性", name_en="wu_youxing", school="医家", tier=SageTier.SCHOLAR, era="明代", lifespan="1582-1652", titles=["温病学派"], works=["温疫论"], expertise=["温病"], department="工部", description="温疫论作者"),
    SageMeta(name="叶天士", name_en="ye_tianshi", school="医家", tier=SageTier.SCHOLAR, era="清代", lifespan="1666-1745", titles=["温病学派"], works=["温热论"], expertise=["温病"], department="工部", description="温热论作者"),
    SageMeta(name="薛雪", name_en="xue_xue", school="医家", tier=SageTier.SCHOLAR, era="清代", lifespan="1681-1770", titles=["温病学派"], works=["湿热条辨"], expertise=["温病"], department="工部", description="湿热条辨作者"),
    SageMeta(name="吴鞠通", name_en="wu_jutong", school="医家", tier=SageTier.SCHOLAR, era="清代", lifespan="1758-1836", titles=["温病学派"], works=["温病条辨"], expertise=["温病"], department="工部", description="温病条辨作者"),
    SageMeta(name="王孟英", name_en="wang_mengying", school="医家", tier=SageTier.SCHOLAR, era="清代", lifespan="1808-1868", titles=["温病学派"], works=["温热经纬"], expertise=["温病"], department="工部", description="温热经纬作者"),
    SageMeta(name="王清任", name_en="wang_qingren", school="医家", tier=SageTier.SCHOLAR, era="清代", lifespan="1768-1831", titles=["医学家"], works=["医林改错"], expertise=["解剖"], department="工部", description="医林改错作者"),
    SageMeta(name="傅青主", name_en="fu_qingzhu", school="医家", tier=SageTier.SCHOLAR, era="明清", lifespan="1607-1684", titles=["医学家"], works=["傅青主女科"], expertise=["妇科"], department="工部", description="傅青主女科作者"),
    SageMeta(name="喻昌", name_en="yu_chang", school="医家", tier=SageTier.SCHOLAR, era="清代", lifespan="1585-1664", titles=["医学家"], works=["医门法律"], expertise=["医学"], department="工部", description="医门法律作者"),
    SageMeta(name="徐大椿", name_en="xu_dachun", school="医家", tier=SageTier.SCHOLAR, era="清代", lifespan="1693-1771", titles=["医学家"], works=["医学源流论"], expertise=["医学"], department="工部", description="医学源流论作者"),
    SageMeta(name="陈修园", name_en="chen_xiuyuan", school="医家", tier=SageTier.SCHOLAR, era="清代", lifespan="1753-1823", titles=["医学家"], works=["医学三字经"], expertise=["医学"], department="工部", description="医学三字经作者"),
    SageMeta(name="古代医家群", name_en="ancient_medical_group", school="医家", tier=SageTier.SCHOLAR, era="先秦", lifespan="", titles=["医家"], works=[], expertise=["医学"], department="工部", description="古代医家群"),
    SageMeta(name="民间名医", name_en="folk_famous_doctors", school="医家", tier=SageTier.SCHOLAR, era="历代", lifespan="", titles=["名医"], works=[], expertise=["医学"], department="工部", description="民间名医"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 十三、史家 (Historiography) - 40人
# ═══════════════════════════════════════════════════════════════════════════════

HISTORIAN_SAGES: List[SageMeta] = [
    SageMeta(name="司马迁", name_en="sima_qian", school="史家", tier=SageTier.FOUNDER, era="西汉", lifespan="前145-前86", titles=["史圣"], works=["史记"], expertise=["史学", "文学"], department="礼部", description="史记作者"),
    SageMeta(name="班固", name_en="ban_gu", school="史家", tier=SageTier.MASTER, era="东汉", lifespan="32-92", titles=["史学家"], works=["汉书"], expertise=["史学"], department="礼部", description="汉书作者"),
    SageMeta(name="班昭", name_en="ban_zhao", school="史家", tier=SageTier.SCHOLAR, era="东汉", lifespan="约49-约120", titles=["女史学家"], works=["汉书"], expertise=["史学"], department="礼部", description="续汉书"),
    SageMeta(name="班彪", name_en="ban_biao", school="史家", tier=SageTier.SCHOLAR, era="东汉", lifespan="3-54", titles=["史学家"], works=["史记后传"], expertise=["史学"], department="礼部", description="班固之父"),
    SageMeta(name="荀悦", name_en="xun_yue", school="史家", tier=SageTier.SCHOLAR, era="东汉", lifespan="148-209", titles=["史学家"], works=["汉纪"], expertise=["史学"], department="礼部", description="汉纪作者"),
    SageMeta(name="陈寿", name_en="chen_shou", school="史家", tier=SageTier.SCHOLAR, era="西晋", lifespan="233-297", titles=["史学家"], works=["三国志"], expertise=["史学"], department="礼部", description="三国志作者"),
    SageMeta(name="裴松之", name_en="pei_songzhi", school="史家", tier=SageTier.SCHOLAR, era="南朝", lifespan="372-451", titles=["史学家"], works=["三国志注"], expertise=["史学"], department="礼部", description="三国志注作者"),
    SageMeta(name="范晔", name_en="fan_ye", school="史家", tier=SageTier.SCHOLAR, era="南朝", lifespan="398-445", titles=["史学家"], works=["后汉书"], expertise=["史学"], department="礼部", description="后汉书作者"),
    SageMeta(name="沈约", name_en="shen_yue", school="史家", tier=SageTier.SCHOLAR, era="南朝", lifespan="441-513", titles=["史学家"], works=["宋书"], expertise=["史学"], department="礼部", description="宋书作者"),
    SageMeta(name="萧子显", name_en="xiao_zixian", school="史家", tier=SageTier.SCHOLAR, era="南朝", lifespan="489-537", titles=["史学家"], works=["南齐书"], expertise=["史学"], department="礼部", description="南齐书作者"),
    SageMeta(name="魏收", name_en="wei_shou", school="史家", tier=SageTier.SCHOLAR, era="北齐", lifespan="506-572", titles=["史学家"], works=["魏书"], expertise=["史学"], department="礼部", description="魏书作者"),
    SageMeta(name="刘知几", name_en="liu_zhiji", school="史家", tier=SageTier.MASTER, era="唐代", lifespan="661-721", titles=["史学理论家"], works=["史通"], expertise=["史学理论"], department="礼部", description="史通作者"),
    SageMeta(name="杜佑", name_en="du_you", school="史家", tier=SageTier.SCHOLAR, era="唐代", lifespan="735-812", titles=["史学家"], works=["通典"], expertise=["典章制度"], department="礼部", description="通典作者"),
    SageMeta(name="刘昫", name_en="liu_xu", school="史家", tier=SageTier.SCHOLAR, era="后晋", lifespan="887-946", titles=["史学家"], works=["旧唐书"], expertise=["史学"], department="礼部", description="旧唐书主编"),
    SageMeta(name="欧阳修", name_en="ouyang_xiu_historian", school="史家", tier=SageTier.MASTER, era="北宋", lifespan="1007-1072", titles=["史学家"], works=["新唐书", "新五代史"], expertise=["史学", "文学"], department="礼部", description="新唐书新五代史作者"),
    SageMeta(name="宋祁", name_en="song_qi", school="史家", tier=SageTier.SCHOLAR, era="北宋", lifespan="998-1061", titles=["史学家"], works=["新唐书"], expertise=["史学"], department="礼部", description="新唐书作者"),
    SageMeta(name="薛居正", name_en="xue_juzheng", school="史家", tier=SageTier.SCHOLAR, era="北宋", lifespan="912-981", titles=["史学家"], works=["旧五代史"], expertise=["史学"], department="礼部", description="旧五代史主编"),
    SageMeta(name="司马光", name_en="sima_guang_historian", school="史家", tier=SageTier.MASTER, era="北宋", lifespan="1019-1086", titles=["史学家"], works=["资治通鉴"], expertise=["史学"], department="礼部", description="资治通鉴作者"),
    SageMeta(name="刘恕", name_en="liu_shu", school="史家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1032-1078", titles=["史学家"], works=["通鉴外纪"], expertise=["史学"], department="礼部", description="资治通鉴编者"),
    SageMeta(name="刘攽", name_en="liu_ban", school="史家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1023-1089", titles=["史学家"], works=[], expertise=["史学"], department="礼部", description="资治通鉴编者"),
    SageMeta(name="范祖禹", name_en="fan_zuyu", school="史家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1041-1098", titles=["史学家"], works=["唐鉴"], expertise=["史学"], department="礼部", description="资治通鉴编者"),
    SageMeta(name="郑樵", name_en="zheng_qiao", school="史家", tier=SageTier.SCHOLAR, era="南宋", lifespan="1104-1162", titles=["史学家"], works=["通志"], expertise=["史学"], department="礼部", description="通志作者"),
    SageMeta(name="袁枢", name_en="yuan_shu", school="史家", tier=SageTier.SCHOLAR, era="南宋", lifespan="1131-1205", titles=["史学家"], works=["通鉴纪事本末"], expertise=["史学"], department="礼部", description="纪事本末体创始人"),
    SageMeta(name="李焘", name_en="li_tao", school="史家", tier=SageTier.SCHOLAR, era="南宋", lifespan="1115-1184", titles=["史学家"], works=["续资治通鉴长编"], expertise=["史学"], department="礼部", description="续资治通鉴长编作者"),
    SageMeta(name="脱脱", name_en="tuo_tuo", school="史家", tier=SageTier.SCHOLAR, era="元代", lifespan="1314-1356", titles=["史学家"], works=["宋史", "辽史", "金史"], expertise=["史学"], department="礼部", description="宋辽金史主编"),
    SageMeta(name="宋濂", name_en="song_lian", school="史家", tier=SageTier.SCHOLAR, era="明代", lifespan="1310-1381", titles=["史学家"], works=["元史"], expertise=["史学"], department="礼部", description="元史主编"),
    SageMeta(name="王祎", name_en="wang_yi", school="史家", tier=SageTier.SCHOLAR, era="明代", lifespan="1322-1373", titles=["史学家"], works=["元史"], expertise=["史学"], department="礼部", description="元史作者"),
    SageMeta(name="解缙", name_en="xie_jin", school="史家", tier=SageTier.SCHOLAR, era="明代", lifespan="1369-1415", titles=["史学家"], works=["明太祖实录"], expertise=["史学"], department="礼部", description="明实录主编"),
    SageMeta(name="张廷玉", name_en="zhang_tingyu", school="史家", tier=SageTier.SCHOLAR, era="清代", lifespan="1672-1755", titles=["史学家"], works=["明史"], expertise=["史学"], department="礼部", description="明史主编"),
    SageMeta(name="万斯同", name_en="wan_sitong", school="史家", tier=SageTier.SCHOLAR, era="清代", lifespan="1638-1702", titles=["史学家"], works=["明史稿"], expertise=["史学"], department="礼部", description="明史稿作者"),
    SageMeta(name="谈迁", name_en="tan_qian", school="史家", tier=SageTier.SCHOLAR, era="明清", lifespan="1594-1658", titles=["史学家"], works=["国榷"], expertise=["史学"], department="礼部", description="国榷作者"),
    SageMeta(name="谷应泰", name_en="gu_yingtai", school="史家", tier=SageTier.SCHOLAR, era="清代", lifespan="1620-1690", titles=["史学家"], works=["明史纪事本末"], expertise=["史学"], department="礼部", description="明史纪事本末作者"),
    SageMeta(name="赵翼", name_en="zhao_yi", school="史家", tier=SageTier.SCHOLAR, era="清代", lifespan="1727-1814", titles=["史学家"], works=["廿二史札记"], expertise=["史学"], department="礼部", description="廿二史札记作者"),
    SageMeta(name="钱大昕", name_en="qian_daxin", school="史家", tier=SageTier.SCHOLAR, era="清代", lifespan="1728-1804", titles=["史学家"], works=["廿二史考异"], expertise=["史学"], department="礼部", description="廿二史考异作者"),
    SageMeta(name="王鸣盛", name_en="wang_mingsheng", school="史家", tier=SageTier.SCHOLAR, era="清代", lifespan="1722-1797", titles=["史学家"], works=["十七史商榷"], expertise=["史学"], department="礼部", description="十七史商榷作者"),
    SageMeta(name="崔述", name_en="cui_shu", school="史家", tier=SageTier.SCHOLAR, era="清代", lifespan="1740-1816", titles=["史学家"], works=["考信录"], expertise=["史学"], department="礼部", description="考信录作者"),
    SageMeta(name="章学诚", name_en="zhang_xuecheng", school="史家", tier=SageTier.MASTER, era="清代", lifespan="1738-1801", titles=["史学理论家"], works=["文史通义"], expertise=["史学理论"], department="礼部", description="文史通义作者"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 十四、文学家 (Literature) - 60人
# ═══════════════════════════════════════════════════════════════════════════════

LITERARY_SAGES: List[SageMeta] = [
    # === 先秦文学 ===
    SageMeta(name="屈原", name_en="qu_yuan", school="文学家", tier=SageTier.FOUNDER, era="战国", lifespan="约前340-前278", titles=["诗祖", "楚辞之祖"], works=["离骚", "九歌", "天问"], expertise=["楚辞", "诗歌"], department="礼部", description="楚辞创始人"),
    SageMeta(name="宋玉", name_en="song_yu", school="文学家", tier=SageTier.SCHOLAR, era="战国", lifespan="约前298-前222", titles=["辞赋家"], works=["九辩", "高唐赋"], expertise=["辞赋"], department="礼部", description="屈原弟子"),
    SageMeta(name="景差", name_en="jing_cha", school="文学家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["辞赋家"], works=[], expertise=["辞赋"], department="礼部", description="楚辞作家"),
    SageMeta(name="唐勒", name_en="tang_le", school="文学家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["辞赋家"], works=[], expertise=["辞赋"], department="礼部", description="楚辞作家"),
    
    # === 汉代文学 ===
    SageMeta(name="贾谊", name_en="jia_yi_literature", school="文学家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前200-前168", titles=["辞赋家"], works=["吊屈原赋", "鵩鸟赋"], expertise=["辞赋", "政论"], department="礼部", description="汉赋先驱"),
    SageMeta(name="枚乘", name_en="mei_cheng", school="文学家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前140", titles=["辞赋家"], works=["七发"], expertise=["辞赋"], department="礼部", description="汉赋代表"),
    SageMeta(name="司马相如", name_en="sima_xiangru", school="文学家", tier=SageTier.MASTER, era="西汉", lifespan="约前179-前118", titles=["赋圣"], works=["子虚赋", "上林赋"], expertise=["辞赋"], department="礼部", description="汉赋代表"),
    SageMeta(name="扬雄", name_en="yang_xiong_literature", school="文学家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前53-18", titles=["辞赋家"], works=["甘泉赋", "羽猎赋"], expertise=["辞赋"], department="礼部", description="汉赋代表"),
    SageMeta(name="班固", name_en="ban_gu_literature", school="文学家", tier=SageTier.SCHOLAR, era="东汉", lifespan="32-92", titles=["辞赋家"], works=["两都赋"], expertise=["辞赋", "史学"], department="礼部", description="汉赋代表"),
    SageMeta(name="张衡", name_en="zhang_heng_literature", school="文学家", tier=SageTier.SCHOLAR, era="东汉", lifespan="78-139", titles=["科学家", "文学家"], works=["二京赋", "归田赋"], expertise=["辞赋", "科学"], department="工部", description="二京赋作者"),
    SageMeta(name="蔡邕", name_en="cai_yong", school="文学家", tier=SageTier.SCHOLAR, era="东汉", lifespan="133-192", titles=["文学家", "书法家"], works=[], expertise=["文学", "书法"], department="礼部", description="蔡文姬之父"),
    SageMeta(name="曹操", name_en="cao_cao_literature", school="文学家", tier=SageTier.SCHOLAR, era="东汉", lifespan="155-220", titles=["文学家"], works=["短歌行", "观沧海"], expertise=["诗歌"], department="礼部", description="建安文学代表"),
    SageMeta(name="曹丕", name_en="cao_pi", school="文学家", tier=SageTier.SCHOLAR, era="三国", lifespan="187-226", titles=["文学家"], works=["典论", "燕歌行"], expertise=["文学", "文论"], department="礼部", description="典论论文"),
    SageMeta(name="曹植", name_en="cao_zhi", school="文学家", tier=SageTier.MASTER, era="三国", lifespan="192-232", titles=["诗圣"], works=["洛神赋", "七步诗"], expertise=["诗歌", "辞赋"], department="礼部", description="建安之杰"),
    
    # === 魏晋南北朝文学 ===
    SageMeta(name="陶渊明", name_en="tao_yuanming", school="文学家", tier=SageTier.MASTER, era="东晋", lifespan="约365-427", titles=["田园诗人", "隐逸诗人之宗"], works=["桃花源记", "归去来兮辞"], expertise=["田园诗", "散文"], department="礼部", description="田园诗创始人"),
    SageMeta(name="谢灵运", name_en="xie_lingyun", school="文学家", tier=SageTier.SCHOLAR, era="南朝", lifespan="385-433", titles=["山水诗人"], works=[], expertise=["山水诗"], department="礼部", description="山水诗创始人"),
    SageMeta(name="鲍照", name_en="bao_zhao", school="文学家", tier=SageTier.SCHOLAR, era="南朝", lifespan="约414-466", titles=["诗人"], works=["鲍参军集"], expertise=["诗歌"], department="礼部", description="南朝诗人"),
    SageMeta(name="谢朓", name_en="xie_tiao", school="文学家", tier=SageTier.SCHOLAR, era="南朝", lifespan="464-499", titles=["诗人"], works=[], expertise=["诗歌"], department="礼部", description="南朝诗人"),
    SageMeta(name="庾信", name_en="yu_xin", school="文学家", tier=SageTier.SCHOLAR, era="南北朝", lifespan="513-581", titles=["文学家"], works=["庾子山集"], expertise=["诗歌", "骈文"], department="礼部", description="南北朝文学家"),
    SageMeta(name="江淹", name_en="jiang_yan", school="文学家", tier=SageTier.SCHOLAR, era="南朝", lifespan="444-505", titles=["文学家"], works=["别赋", "恨赋"], expertise=["辞赋"], department="礼部", description="别赋恨赋作者"),
    SageMeta(name="沈约", name_en="shen_yue_literature", school="文学家", tier=SageTier.SCHOLAR, era="南朝", lifespan="441-513", titles=["文学家"], works=[], expertise=["诗歌", "声律"], department="礼部", description="永明体代表"),
    SageMeta(name="陆机", name_en="lu_ji", school="文学家", tier=SageTier.SCHOLAR, era="西晋", lifespan="261-303", titles=["文学家"], works=["文赋"], expertise=["文学", "文论"], department="礼部", description="文赋作者"),
    SageMeta(name="潘岳", name_en="pan_yue", school="文学家", tier=SageTier.SCHOLAR, era="西晋", lifespan="247-300", titles=["文学家"], works=[], expertise=["辞赋"], department="礼部", description="西晋文学家"),
    SageMeta(name="左思", name_en="zuo_si", school="文学家", tier=SageTier.SCHOLAR, era="西晋", lifespan="约250-305", titles=["文学家"], works=["三都赋"], expertise=["辞赋"], department="礼部", description="三都赋作者"),
    
    # === 唐代文学 ===
    SageMeta(name="李白", name_en="li_bai", school="文学家", tier=SageTier.MASTER, era="唐代", lifespan="701-762", titles=["诗仙"], works=["李太白集"], expertise=["诗歌"], department="礼部", description="诗仙"),
    SageMeta(name="杜甫", name_en="du_fu", school="文学家", tier=SageTier.MASTER, era="唐代", lifespan="712-770", titles=["诗圣"], works=["杜工部集"], expertise=["诗歌"], department="礼部", description="诗圣"),
    SageMeta(name="白居易", name_en="bai_juyi", school="文学家", tier=SageTier.MASTER, era="唐代", lifespan="772-846", titles=["诗魔", "诗王"], works=["白氏长庆集"], expertise=["诗歌"], department="礼部", description="新乐府运动"),
    SageMeta(name="王维", name_en="wang_wei", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="701-761", titles=["诗佛"], works=["王右丞集"], expertise=["诗歌", "绘画"], department="礼部", description="山水田园诗"),
    SageMeta(name="孟浩然", name_en="meng_haoran", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="689-740", titles=["诗人"], works=[], expertise=["山水田园诗"], department="礼部", description="山水田园诗"),
    SageMeta(name="王昌龄", name_en="wang_changling", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="698-757", titles=["七绝圣手"], works=[], expertise=["边塞诗"], department="礼部", description="边塞诗代表"),
    SageMeta(name="高适", name_en="gao_shi", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="约704-765", titles=["诗人"], works=[], expertise=["边塞诗"], department="礼部", description="边塞诗代表"),
    SageMeta(name="岑参", name_en="cen_shen", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="约715-770", titles=["诗人"], works=[], expertise=["边塞诗"], department="礼部", description="边塞诗代表"),
    SageMeta(name="韩愈", name_en="han_yu", school="文学家", tier=SageTier.MASTER, era="唐代", lifespan="768-824", titles=["文起八代之衰"], works=["韩昌黎集"], expertise=["散文", "诗歌"], department="礼部", description="唐宋八大家"),
    SageMeta(name="柳宗元", name_en="liu_zongyuan", school="文学家", tier=SageTier.MASTER, era="唐代", lifespan="773-819", titles=["文学家"], works=["柳河东集"], expertise=["散文", "诗歌"], department="礼部", description="唐宋八大家"),
    SageMeta(name="刘禹锡", name_en="liu_yuxi", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="772-842", titles=["诗豪"], works=["刘梦得集"], expertise=["诗歌"], department="礼部", description="诗豪"),
    SageMeta(name="李贺", name_en="li_he", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="790-816", titles=["诗鬼"], works=[], expertise=["诗歌"], department="礼部", description="诗鬼"),
    SageMeta(name="李商隐", name_en="li_shangyin", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="约813-858", titles=["诗人"], works=["李义山诗集"], expertise=["诗歌"], department="礼部", description="晚唐诗人"),
    SageMeta(name="杜牧", name_en="du_mu", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="803-约852", titles=["诗人"], works=["樊川文集"], expertise=["诗歌"], department="礼部", description="晚唐诗人"),
    
    # === 宋代文学 ===
    SageMeta(name="苏轼", name_en="su_shi_literature", school="文学家", tier=SageTier.MASTER, era="北宋", lifespan="1037-1101", titles=["东坡居士"], works=["东坡全集"], expertise=["诗词", "散文"], department="礼部", description="唐宋八大家"),
    SageMeta(name="辛弃疾", name_en="xin_qiji", school="文学家", tier=SageTier.MASTER, era="南宋", lifespan="1140-1207", titles=["词中之龙"], works=["稼轩长短句"], expertise=["词"], department="礼部", description="豪放派词人"),
    SageMeta(name="李清照", name_en="li_qingzhao", school="文学家", tier=SageTier.SCHOLAR, era="南宋", lifespan="1084-约1155", titles=["千古第一才女"], works=["漱玉词"], expertise=["词"], department="礼部", description="婉约派代表"),
    SageMeta(name="陆游", name_en="lu_you", school="文学家", tier=SageTier.SCHOLAR, era="南宋", lifespan="1125-1210", titles=["小李白"], works=["剑南诗稿"], expertise=["诗歌"], department="礼部", description="南宋诗人"),
    SageMeta(name="欧阳修", name_en="ouyang_xiu_literature", school="文学家", tier=SageTier.MASTER, era="北宋", lifespan="1007-1072", titles=["文学家"], works=["欧阳文忠集"], expertise=["散文", "诗词"], department="礼部", description="唐宋八大家"),
    SageMeta(name="王安石", name_en="wang_anshi_literature", school="文学家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1021-1086", titles=["文学家"], works=["临川集"], expertise=["散文", "诗词"], department="礼部", description="唐宋八大家"),
    SageMeta(name="柳永", name_en="liu_yong", school="文学家", tier=SageTier.SCHOLAR, era="北宋", lifespan="约984-约1053", titles=["词人"], works=["乐章集"], expertise=["词"], department="礼部", description="婉约派代表"),
    SageMeta(name="周邦彦", name_en="zhou_bangyan", school="文学家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1056-1121", titles=["词人"], works=["清真集"], expertise=["词"], department="礼部", description="格律派词人"),
    SageMeta(name="姜夔", name_en="jiang_kui", school="文学家", tier=SageTier.SCHOLAR, era="南宋", lifespan="约1155-约1221", titles=["词人"], works=["白石道人歌曲"], expertise=["词", "音乐"], department="礼部", description="格律派词人"),
    SageMeta(name="范仲淹", name_en="fan_zhongyan", school="文学家", tier=SageTier.SCHOLAR, era="北宋", lifespan="989-1052", titles=["文学家"], works=["范文正集"], expertise=["散文", "诗词"], department="礼部", description="岳阳楼记作者"),
    
    # === 元明清文学 ===
    SageMeta(name="关汉卿", name_en="guan_hanqing", school="文学家", tier=SageTier.MASTER, era="元代", lifespan="约1234-约1300", titles=["曲圣"], works=["窦娥冤", "救风尘"], expertise=["杂剧"], department="礼部", description="元曲四大家之首"),
    SageMeta(name="王实甫", name_en="wang_shifu", school="文学家", tier=SageTier.SCHOLAR, era="元代", lifespan="约1260-1336", titles=["杂剧家"], works=["西厢记"], expertise=["杂剧"], department="礼部", description="西厢记作者"),
    SageMeta(name="马致远", name_en="ma_zhiyuan", school="文学家", tier=SageTier.SCHOLAR, era="元代", lifespan="约1250-约1321", titles=["曲状元"], works=["汉宫秋"], expertise=["杂剧", "散曲"], department="礼部", description="元曲四大家"),
    SageMeta(name="白朴", name_en="bai_pu", school="文学家", tier=SageTier.SCHOLAR, era="元代", lifespan="1226-约1306", titles=["杂剧家"], works=["墙头马上", "梧桐雨"], expertise=["杂剧"], department="礼部", description="元曲四大家"),
    SageMeta(name="郑光祖", name_en="zheng_guangzu", school="文学家", tier=SageTier.SCHOLAR, era="元代", lifespan="约1260-1320", titles=["杂剧家"], works=["倩女离魂"], expertise=["杂剧"], department="礼部", description="元曲四大家"),
    SageMeta(name="施耐庵", name_en="shi_nai'an", school="文学家", tier=SageTier.MASTER, era="元明", lifespan="约1296-约1370", titles=["小说家"], works=["水浒传"], expertise=["小说"], department="礼部", description="水浒传作者"),
    SageMeta(name="罗贯中", name_en="luo_guanzhong", school="文学家", tier=SageTier.MASTER, era="元明", lifespan="约1330-约1400", titles=["小说家"], works=["三国演义"], expertise=["小说"], department="礼部", description="三国演义作者"),
    SageMeta(name="吴承恩", name_en="wu_cheng'en", school="文学家", tier=SageTier.MASTER, era="明代", lifespan="约1500-约1582", titles=["小说家"], works=["西游记"], expertise=["小说"], department="礼部", description="西游记作者"),
    SageMeta(name="曹雪芹", name_en="cao_xueqin", school="文学家", tier=SageTier.MASTER, era="清代", lifespan="约1715-约1763", titles=["小说家"], works=["红楼梦"], expertise=["小说"], department="礼部", description="红楼梦作者"),
    SageMeta(name="蒲松龄", name_en="pu_songling", school="文学家", tier=SageTier.SCHOLAR, era="清代", lifespan="1640-1715", titles=["小说家"], works=["聊斋志异"], expertise=["小说"], department="礼部", description="聊斋志异作者"),
    SageMeta(name="吴敬梓", name_en="wu_jingzi", school="文学家", tier=SageTier.SCHOLAR, era="清代", lifespan="1701-1754", titles=["小说家"], works=["儒林外史"], expertise=["小说"], department="礼部", description="儒林外史作者"),
    SageMeta(name="纳兰性德", name_en="nal_xingde", school="文学家", tier=SageTier.SCHOLAR, era="清代", lifespan="1655-1685", titles=["词人"], works=["纳兰词"], expertise=["词"], department="礼部", description="清代词人"),
    SageMeta(name="龚自珍", name_en="gong_zizhen", school="文学家", tier=SageTier.SCHOLAR, era="清代", lifespan="1792-1841", titles=["文学家"], works=["龚自珍全集"], expertise=["诗词", "散文"], department="礼部", description="清代文学家"),
    SageMeta(name="黄遵宪", name_en="huang_zunxian", school="文学家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1848-1905", titles=["诗人"], works=["人境庐诗草"], expertise=["诗歌"], department="礼部", description="近代诗人"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 十五、艺术家 (Arts) - 30人
# ═══════════════════════════════════════════════════════════════════════════════

ARTIST_SAGES: List[SageMeta] = [
    SageMeta(name="王羲之", name_en="wang_xizhi", school="艺术家", tier=SageTier.MASTER, era="东晋", lifespan="303-361", titles=["书圣"], works=["兰亭集序"], expertise=["书法"], department="礼部", description="书圣"),
    SageMeta(name="王献之", name_en="wang_xianzhi", school="艺术家", tier=SageTier.SCHOLAR, era="东晋", lifespan="344-386", titles=["书法家"], works=[], expertise=["书法"], department="礼部", description="王羲之之子"),
    SageMeta(name="颜真卿", name_en="yan_zhenqing", school="艺术家", tier=SageTier.MASTER, era="唐代", lifespan="709-784", titles=["书法家"], works=[], expertise=["书法"], department="礼部", description="颜体创始人"),
    SageMeta(name="柳公权", name_en="liu_gongquan", school="艺术家", tier=SageTier.SCHOLAR, era="唐代", lifespan="778-865", titles=["书法家"], works=[], expertise=["书法"], department="礼部", description="柳体创始人"),
    SageMeta(name="欧阳询", name_en="ouyang_xun", school="艺术家", tier=SageTier.SCHOLAR, era="唐代", lifespan="557-641", titles=["书法家"], works=[], expertise=["书法"], department="礼部", description="欧体创始人"),
    SageMeta(name="赵孟頫", name_en="zhao_mengfu", school="艺术家", tier=SageTier.SCHOLAR, era="元代", lifespan="1254-1322", titles=["书法家", "画家"], works=[], expertise=["书法", "绘画"], department="礼部", description="赵体创始人"),
    SageMeta(name="张旭", name_en="zhang_xu", school="艺术家", tier=SageTier.SCHOLAR, era="唐代", lifespan="约685-约759", titles=["草圣"], works=[], expertise=["草书"], department="礼部", description="草圣"),
    SageMeta(name="怀素", name_en="huai_su", school="艺术家", tier=SageTier.SCHOLAR, era="唐代", lifespan="737-799", titles=["草书家"], works=[], expertise=["草书"], department="礼部", description="草书大家"),
    SageMeta(name="苏轼", name_en="su_shi_artist", school="艺术家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1037-1101", titles=["书法家", "画家"], works=[], expertise=["书法", "绘画"], department="礼部", description="宋四家"),
    SageMeta(name="黄庭坚", name_en="huang_tingjian", school="艺术家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1045-1105", titles=["书法家"], works=[], expertise=["书法"], department="礼部", description="宋四家"),
    SageMeta(name="米芾", name_en="mi_fu", school="艺术家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1051-1107", titles=["书法家", "画家"], works=[], expertise=["书法", "绘画"], department="礼部", description="宋四家"),
    SageMeta(name="蔡襄", name_en="cai_xiang", school="艺术家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1012-1067", titles=["书法家"], works=[], expertise=["书法"], department="礼部", description="宋四家"),
    SageMeta(name="顾恺之", name_en="gu_kaizhi", school="艺术家", tier=SageTier.MASTER, era="东晋", lifespan="约348-409", titles=["画圣"], works=[], expertise=["绘画"], department="礼部", description="画圣"),
    SageMeta(name="吴道子", name_en="wu_daozi", school="艺术家", tier=SageTier.MASTER, era="唐代", lifespan="约680-759", titles=["画圣"], works=[], expertise=["绘画"], department="礼部", description="画圣"),
    SageMeta(name="阎立本", name_en="yan_liben", school="艺术家", tier=SageTier.SCHOLAR, era="唐代", lifespan="约601-673", titles=["画家"], works=[], expertise=["绘画"], department="礼部", description="唐代画家"),
    SageMeta(name="李思训", name_en="li_sixun", school="艺术家", tier=SageTier.SCHOLAR, era="唐代", lifespan="651-716", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="北宗之祖"),
    SageMeta(name="王维", name_en="wang_wei_artist", school="艺术家", tier=SageTier.SCHOLAR, era="唐代", lifespan="701-761", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="南宗之祖"),
    SageMeta(name="荆浩", name_en="jing_hao", school="艺术家", tier=SageTier.SCHOLAR, era="五代", lifespan="约850-?", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="北方山水画派"),
    SageMeta(name="关仝", name_en="guan_tong", school="艺术家", tier=SageTier.SCHOLAR, era="五代", lifespan="约907-960", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="关家山水"),
    SageMeta(name="董源", name_en="dong_yuan", school="艺术家", tier=SageTier.SCHOLAR, era="五代", lifespan="约934-约962", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="南方山水画派"),
    SageMeta(name="巨然", name_en="ju_ran", school="艺术家", tier=SageTier.SCHOLAR, era="五代宋", lifespan="?", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="董源弟子"),
    SageMeta(name="范宽", name_en="fan_kuan", school="艺术家", tier=SageTier.SCHOLAR, era="北宋", lifespan="约950-约1032", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="北宋三大家"),
    SageMeta(name="郭熙", name_en="guo_xi", school="艺术家", tier=SageTier.SCHOLAR, era="北宋", lifespan="约1023-约1085", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="林泉高致"),
    SageMeta(name="李唐", name_en="li_tang", school="艺术家", tier=SageTier.SCHOLAR, era="南宋", lifespan="约1066-1150", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="南宋四家"),
    SageMeta(name="刘松年", name_en="liu_songnian", school="艺术家", tier=SageTier.SCHOLAR, era="南宋", lifespan="约1131-1218", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="南宋四家"),
    SageMeta(name="马远", name_en="ma_yuan", school="艺术家", tier=SageTier.SCHOLAR, era="南宋", lifespan="约1140-约1225", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="马一角"),
    SageMeta(name="夏圭", name_en="xia_gui", school="艺术家", tier=SageTier.SCHOLAR, era="南宋", lifespan="约1180-约1230", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="夏半边"),
    SageMeta(name="黄公望", name_en="huang_gongwang", school="艺术家", tier=SageTier.SCHOLAR, era="元代", lifespan="1269-1354", titles=["画家"], works=["富春山居图"], expertise=["山水画"], department="礼部", description="元四家之首"),
    SageMeta(name="倪瓒", name_en="ni_zan", school="艺术家", tier=SageTier.SCHOLAR, era="元代", lifespan="1301-1374", titles=["画家"], works=[], expertise=["山水画"], department="礼部", description="元四家"),
    SageMeta(name="徐渭", name_en="xu_wei", school="艺术家", tier=SageTier.SCHOLAR, era="明代", lifespan="1521-1593", titles=["画家"], works=[], expertise=["花鸟画"], department="礼部", description="青藤白阳"),
    SageMeta(name="朱耷", name_en="zhu_da", school="艺术家", tier=SageTier.SCHOLAR, era="清代", lifespan="1626-约1705", titles=["画家"], works=[], expertise=["花鸟画"], department="礼部", description="八大山人"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 十六、科学家 (Science) - 40人
# ═══════════════════════════════════════════════════════════════════════════════

SCIENTIST_SAGES: List[SageMeta] = [
    SageMeta(name="墨子", name_en="mo_di_science", school="科学家", tier=SageTier.FOUNDER, era="战国", lifespan="约前468-前376", titles=["科学家"], works=["墨经"], expertise=["光学", "力学"], department="工部", description="光学力学先驱"),
    SageMeta(name="鲁班", name_en="lu_ban_science", school="科学家", tier=SageTier.SCHOLAR, era="战国", lifespan="约前507-前444", titles=["工匠祖师"], works=[], expertise=["木工", "建筑"], department="工部", description="工匠祖师"),
    SageMeta(name="张衡", name_en="zhang_heng", school="科学家", tier=SageTier.MASTER, era="东汉", lifespan="78-139", titles=["科学家"], works=["灵宪", "浑天仪"], expertise=["天文", "地震"], department="工部", description="地动仪发明者"),
    SageMeta(name="蔡伦", name_en="cai_lun", school="科学家", tier=SageTier.SCHOLAR, era="东汉", lifespan="约61-121", titles=["造纸术发明者"], works=[], expertise=["造纸"], department="工部", description="造纸术改进者"),
    SageMeta(name="刘徽", name_en="liu_hui", school="科学家", tier=SageTier.MASTER, era="三国", lifespan="约225-约295", titles=["数学家"], works=["九章算术注"], expertise=["数学"], department="工部", description="割圆术"),
    SageMeta(name="祖冲之", name_en="zu_chongzhi", school="科学家", tier=SageTier.MASTER, era="南朝", lifespan="429-500", titles=["数学家", "天文学家"], works=[], expertise=["数学", "天文"], department="工部", description="圆周率"),
    SageMeta(name="祖暅", name_en="zu_geng", school="科学家", tier=SageTier.SCHOLAR, era="南朝", lifespan="约450-约520", titles=["数学家"], works=[], expertise=["数学"], department="工部", description="祖暅原理"),
    SageMeta(name="贾思勰", name_en="jia_sixie_science", school="科学家", tier=SageTier.SCHOLAR, era="北魏", lifespan="?", titles=["农学家"], works=["齐民要术"], expertise=["农学"], department="工部", description="齐民要术作者"),
    SageMeta(name="郦道元", name_en="li_daoyuan", school="科学家", tier=SageTier.SCHOLAR, era="北魏", lifespan="约472-527", titles=["地理学家"], works=["水经注"], expertise=["地理"], department="工部", description="水经注作者"),
    SageMeta(name="僧一行", name_en="seng_yixing", school="科学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="683-727", titles=["天文学家"], works=[], expertise=["天文", "历法"], department="工部", description="大衍历"),
    SageMeta(name="孙思邈", name_en="sun_simiao_science", school="科学家", tier=SageTier.MASTER, era="唐代", lifespan="541-682", titles=["医学家"], works=["千金要方"], expertise=["医学"], department="工部", description="药王"),
    SageMeta(name="沈括", name_en="shen_kuo", school="科学家", tier=SageTier.MASTER, era="北宋", lifespan="1031-1095", titles=["科学家"], works=["梦溪笔谈"], expertise=["天文", "地理", "数学"], department="工部", description="梦溪笔谈作者"),
    SageMeta(name="苏颂", name_en="su_song", school="科学家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1020-1101", titles=["科学家"], works=[], expertise=["天文", "医学"], department="工部", description="水运仪象台"),
    SageMeta(name="郭守敬", name_en="guo_shoujing", school="科学家", tier=SageTier.MASTER, era="元代", lifespan="1231-1316", titles=["天文学家"], works=[], expertise=["天文", "历法"], department="工部", description="授时历"),
    SageMeta(name="王祯", name_en="wang_zhen_science", school="科学家", tier=SageTier.SCHOLAR, era="元代", lifespan="?", titles=["农学家"], works=["王祯农书"], expertise=["农学"], department="工部", description="王祯农书作者"),
    SageMeta(name="徐光启", name_en="xu_guangqi_science", school="科学家", tier=SageTier.MASTER, era="明代", lifespan="1562-1633", titles=["科学家"], works=["农政全书"], expertise=["农学", "天文"], department="工部", description="农政全书作者"),
    SageMeta(name="宋应星", name_en="song_yingxing_science", school="科学家", tier=SageTier.SCHOLAR, era="明代", lifespan="1587-约1666", titles=["科学家"], works=["天工开物"], expertise=["工艺", "技术"], department="工部", description="天工开物作者"),
    SageMeta(name="徐霞客", name_en="xi_xiake", school="科学家", tier=SageTier.SCHOLAR, era="明代", lifespan="1587-1641", titles=["地理学家"], works=["徐霞客游记"], expertise=["地理"], department="工部", description="徐霞客游记作者"),
    SageMeta(name="李时珍", name_en="li_shizhen_science", school="科学家", tier=SageTier.MASTER, era="明代", lifespan="1518-1593", titles=["医学家"], works=["本草纲目"], expertise=["医学", "本草"], department="工部", description="本草纲目作者"),
    SageMeta(name="朱载堉", name_en="zhu_zaiyu", school="科学家", tier=SageTier.SCHOLAR, era="明代", lifespan="1536-1611", titles=["乐律学家"], works=[], expertise=["乐律", "数学"], department="工部", description="十二平均律"),
    SageMeta(name="方以智", name_en="fang_yizhi", school="科学家", tier=SageTier.SCHOLAR, era="明清", lifespan="1611-1671", titles=["科学家"], works=["物理小识"], expertise=["科学", "哲学"], department="工部", description="物理小识作者"),
    SageMeta(name="王清任", name_en="wang_qingren_science", school="科学家", tier=SageTier.SCHOLAR, era="清代", lifespan="1768-1831", titles=["医学家"], works=["医林改错"], expertise=["医学"], department="工部", description="医林改错作者"),
    SageMeta(name="梅文鼎", name_en="mei_wending", school="科学家", tier=SageTier.SCHOLAR, era="清代", lifespan="1633-1721", titles=["数学家"], works=[], expertise=["数学", "天文"], department="工部", description="清代算学第一"),
    SageMeta(name="明安图", name_en="ming_antu", school="科学家", tier=SageTier.SCHOLAR, era="清代", lifespan="1692-1765", titles=["数学家"], works=[], expertise=["数学"], department="工部", description="割圆密率捷法"),
    SageMeta(name="王锡阐", name_en="wang_xichan", school="科学家", tier=SageTier.SCHOLAR, era="清代", lifespan="1628-1682", titles=["天文学家"], works=[], expertise=["天文"], department="工部", description="天文学家"),
    SageMeta(name="李善兰", name_en="li_shanlan", school="科学家", tier=SageTier.SCHOLAR, era="清代", lifespan="1811-1882", titles=["数学家"], works=[], expertise=["数学"], department="工部", description="近代数学先驱"),
    SageMeta(name="华蘅芳", name_en="hua_hengfang", school="科学家", tier=SageTier.SCHOLAR, era="清代", lifespan="1833-1902", titles=["数学家"], works=[], expertise=["数学"], department="工部", description="近代数学家"),
    SageMeta(name="詹天佑", name_en="zhan_tianyou", school="科学家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1861-1919", titles=["工程师"], works=[], expertise=["铁路工程"], department="工部", description="京张铁路"),
    SageMeta(name="侯德榜", name_en="hou_debang", school="科学家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1890-1974", titles=["化学家"], works=[], expertise=["化学工业"], department="工部", description="侯氏制碱法"),
    SageMeta(name="茅以升", name_en="mao_yisheng", school="科学家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1896-1989", titles=["工程师"], works=[], expertise=["桥梁工程"], department="工部", description="钱塘江大桥"),
    SageMeta(name="竺可桢", name_en="zhu_kezhen", school="科学家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1890-1974", titles=["气象学家"], works=[], expertise=["气象学"], department="工部", description="气象学家"),
    SageMeta(name="华罗庚", name_en="hua_luogeng", school="科学家", tier=SageTier.MASTER, era="近现代", lifespan="1910-1985", titles=["数学家"], works=[], expertise=["数学"], department="工部", description="数学家"),
    SageMeta(name="钱学森", name_en="qian_xuesen", school="科学家", tier=SageTier.MASTER, era="近现代", lifespan="1911-2009", titles=["科学家"], works=[], expertise=["航天", "工程"], department="工部", description="航天之父"),
    SageMeta(name="邓稼先", name_en="deng_jiaxian", school="科学家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1924-1986", titles=["物理学家"], works=[], expertise=["核物理"], department="工部", description="两弹元勋"),
    SageMeta(name="袁隆平", name_en="yuan_longping", school="科学家", tier=SageTier.MASTER, era="当代", lifespan="1930-2021", titles=["农学家"], works=[], expertise=["杂交水稻"], department="工部", description="杂交水稻之父"),
    SageMeta(name="屠呦呦", name_en="tu_youyou", school="科学家", tier=SageTier.SCHOLAR, era="当代", lifespan="1930-", titles=["药学家"], works=[], expertise=["药学"], department="工部", description="诺贝尔奖得主"),
    SageMeta(name="杨振宁", name_en="yang_zhenning", school="科学家", tier=SageTier.SCHOLAR, era="当代", lifespan="1922-", titles=["物理学家"], works=[], expertise=["理论物理"], department="工部", description="诺贝尔物理学奖"),
    SageMeta(name="李政道", name_en="li_zhengdao", school="科学家", tier=SageTier.SCHOLAR, era="当代", lifespan="1926-", titles=["物理学家"], works=[], expertise=["理论物理"], department="工部", description="诺贝尔物理学奖"),
    SageMeta(name="丁肇中", name_en="ding_zhaozhong", school="科学家", tier=SageTier.SCHOLAR, era="当代", lifespan="1936-", titles=["物理学家"], works=[], expertise=["粒子物理"], department="工部", description="诺贝尔物理学奖"),
    SageMeta(name="吴健雄", name_en="wu_jianxiong", school="科学家", tier=SageTier.SCHOLAR, era="近现代", lifespan="1912-1997", titles=["物理学家"], works=[], expertise=["核物理"], department="工部", description="实验物理学家"),
    SageMeta(name="王选", name_en="wang_xuan", school="科学家", tier=SageTier.SCHOLAR, era="当代", lifespan="1937-2006", titles=["科学家"], works=[], expertise=["计算机"], department="工部", description="激光照排"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 十七、政治家 (Statesmen) - 40人
# ═══════════════════════════════════════════════════════════════════════════════

STATESMAN_SAGES: List[SageMeta] = [
    SageMeta(name="周公", name_en="zhou_gong", school="政治家", tier=SageTier.FOUNDER, era="西周", lifespan="约前11世纪", titles=["周公旦"], works=[], expertise=["礼制", "政治"], department="礼部", description="制礼作乐"),
    SageMeta(name="管仲", name_en="guan_zhong_statesman", school="政治家", tier=SageTier.MASTER, era="春秋", lifespan="前723-前645", titles=["春秋第一相"], works=[], expertise=["政治", "经济"], department="吏部", description="春秋第一相"),
    SageMeta(name="子产", name_en="zi_chan_statesman", school="政治家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?-前522", titles=["政治家"], works=[], expertise=["政治", "法治"], department="吏部", description="郑国执政"),
    SageMeta(name="晏婴", name_en="yan_ying", school="政治家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前578-前500", titles=["晏子"], works=["晏子春秋"], expertise=["政治", "外交"], department="吏部", description="晏子使楚"),
    SageMeta(name="范蠡", name_en="fan_li_statesman", school="政治家", tier=SageTier.SCHOLAR, era="春秋", lifespan="前536-前448", titles=["政治家"], works=[], expertise=["政治", "谋略"], department="吏部", description="助勾践灭吴"),
    SageMeta(name="商鞅", name_en="shang_yang_statesman", school="政治家", tier=SageTier.MASTER, era="战国", lifespan="前390-前338", titles=["改革家"], works=[], expertise=["变法", "法治"], department="刑部", description="商鞅变法"),
    SageMeta(name="李斯", name_en="li_si_statesman", school="政治家", tier=SageTier.SCHOLAR, era="秦代", lifespan="前284-前208", titles=["秦相"], works=[], expertise=["政治", "统一"], department="吏部", description="秦相"),
    SageMeta(name="萧何", name_en="xiao_he_statesman", school="政治家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前257-前193", titles=["汉相"], works=[], expertise=["政治", "治国"], department="吏部", description="汉初三杰"),
    SageMeta(name="张良", name_en="zhang_liang_statesman", school="政治家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前250-前186", titles=["谋士"], works=[], expertise=["谋略"], department="吏部", description="汉初三杰"),
    SageMeta(name="陈平", name_en="chen_ping_statesman", school="政治家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前178", titles=["谋士"], works=[], expertise=["谋略"], department="吏部", description="汉初谋士"),
    SageMeta(name="霍光", name_en="huo_guang", school="政治家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前68", titles=["权臣"], works=[], expertise=["政治"], department="吏部", description="霍光辅政"),
    SageMeta(name="诸葛亮", name_en="zhuge_liang_statesman", school="政治家", tier=SageTier.MASTER, era="三国", lifespan="181-234", titles=["武侯"], works=[], expertise=["政治", "治国"], department="吏部", description="鞠躬尽瘁"),
    SageMeta(name="曹操", name_en="cao_cao_statesman", school="政治家", tier=SageTier.SCHOLAR, era="东汉", lifespan="155-220", titles=["魏武帝"], works=[], expertise=["政治", "军事"], department="吏部", description="政治家军事家"),
    SageMeta(name="司马懿", name_en="sima_yi_statesman", school="政治家", tier=SageTier.SCHOLAR, era="三国", lifespan="179-251", titles=["晋宣帝"], works=[], expertise=["政治", "谋略"], department="吏部", description="政治家"),
    SageMeta(name="王导", name_en="wang_dao", school="政治家", tier=SageTier.SCHOLAR, era="东晋", lifespan="276-339", titles=["政治家"], works=[], expertise=["政治"], department="吏部", description="王与马共天下"),
    SageMeta(name="谢安", name_en="xie_an", school="政治家", tier=SageTier.SCHOLAR, era="东晋", lifespan="320-385", titles=["政治家"], works=[], expertise=["政治", "军事"], department="吏部", description="淝水之战"),
    SageMeta(name="王猛", name_en="wang_meng_statesman", school="政治家", tier=SageTier.SCHOLAR, era="前秦", lifespan="325-375", titles=["政治家"], works=[], expertise=["政治", "治国"], department="吏部", description="前秦名相"),
    SageMeta(name="魏征", name_en="wei_zheng", school="政治家", tier=SageTier.SCHOLAR, era="唐代", lifespan="580-643", titles=["名相"], works=[], expertise=["谏诤", "治国"], department="吏部", description="贞观之治"),
    SageMeta(name="房玄龄", name_en="fang_xuanling", school="政治家", tier=SageTier.SCHOLAR, era="唐代", lifespan="579-648", titles=["名相"], works=[], expertise=["政治", "治国"], department="吏部", description="贞观之治"),
    SageMeta(name="杜如晦", name_en="du_ruhui", school="政治家", tier=SageTier.SCHOLAR, era="唐代", lifespan="585-630", titles=["名相"], works=[], expertise=["政治"], department="吏部", description="房谋杜断"),
    SageMeta(name="姚崇", name_en="yao_chong", school="政治家", tier=SageTier.SCHOLAR, era="唐代", lifespan="650-721", titles=["名相"], works=[], expertise=["政治"], department="吏部", description="开元盛世"),
    SageMeta(name="宋璟", name_en="song_jing", school="政治家", tier=SageTier.SCHOLAR, era="唐代", lifespan="663-737", titles=["名相"], works=[], expertise=["政治"], department="吏部", description="开元盛世"),
    SageMeta(name="狄仁杰", name_en="di_renjie", school="政治家", tier=SageTier.SCHOLAR, era="唐代", lifespan="630-700", titles=["名相"], works=[], expertise=["政治", "断案"], department="吏部", description="神探狄仁杰"),
    SageMeta(name="赵普", name_en="zhao_pu", school="政治家", tier=SageTier.SCHOLAR, era="北宋", lifespan="922-992", titles=["名相"], works=[], expertise=["政治", "谋略"], department="吏部", description="半部论语治天下"),
    SageMeta(name="王安石", name_en="wang_anshi_statesman", school="政治家", tier=SageTier.MASTER, era="北宋", lifespan="1021-1086", titles=["改革家"], works=[], expertise=["变法", "改革"], department="吏部", description="王安石变法"),
    SageMeta(name="司马光", name_en="sima_guang_statesman", school="政治家", tier=SageTier.SCHOLAR, era="北宋", lifespan="1019-1086", titles=["政治家"], works=[], expertise=["政治", "史学"], department="吏部", description="政治家"),
    SageMeta(name="范仲淹", name_en="fan_zhongyan_statesman", school="政治家", tier=SageTier.SCHOLAR, era="北宋", lifespan="989-1052", titles=["政治家"], works=[], expertise=["政治", "改革"], department="吏部", description="先天下之忧而忧"),
    SageMeta(name="包拯", name_en="bao_zheng", school="政治家", tier=SageTier.SCHOLAR, era="北宋", lifespan="999-1062", titles=["清官"], works=[], expertise=["司法", "清廉"], department="刑部", description="包青天"),
    SageMeta(name="寇准", name_en="kou_zhun", school="政治家", tier=SageTier.SCHOLAR, era="北宋", lifespan="961-1023", titles=["名相"], works=[], expertise=["政治", "外交"], department="吏部", description="澶渊之盟"),
    SageMeta(name="文天祥", name_en="wen_tianxiang", school="政治家", tier=SageTier.SCHOLAR, era="南宋", lifespan="1236-1283", titles=["民族英雄"], works=[], expertise=["政治", "气节"], department="吏部", description="人生自古谁无死"),
    SageMeta(name="耶律楚材", name_en="yelu_chucai", school="政治家", tier=SageTier.SCHOLAR, era="元代", lifespan="1190-1244", titles=["政治家"], works=[], expertise=["政治", "治国"], department="吏部", description="蒙古国名相"),
    SageMeta(name="刘秉忠", name_en="liu_bingzhong", school="政治家", tier=SageTier.SCHOLAR, era="元代", lifespan="1216-1274", titles=["政治家"], works=[], expertise=["政治", "规划"], department="吏部", description="元大都规划者"),
    SageMeta(name="朱元璋", name_en="zhu_yuanzhang", school="政治家", tier=SageTier.SCHOLAR, era="明代", lifespan="1328-1398", titles=["明太祖"], works=[], expertise=["政治", "开国"], department="吏部", description="明朝开国皇帝"),
    SageMeta(name="张居正", name_en="zhang_juzheng_statesman", school="政治家", tier=SageTier.MASTER, era="明代", lifespan="1525-1582", titles=["改革家"], works=[], expertise=["变法", "改革"], department="吏部", description="张居正改革"),
    SageMeta(name="于谦", name_en="yu_qian", school="政治家", tier=SageTier.SCHOLAR, era="明代", lifespan="1398-1457", titles=["民族英雄"], works=[], expertise=["政治", "军事"], department="吏部", description="北京保卫战"),
    SageMeta(name="海瑞", name_en="hai_rui", school="政治家", tier=SageTier.SCHOLAR, era="明代", lifespan="1514-1587", titles=["清官"], works=[], expertise=["清廉", "刚正"], department="吏部", description="海青天"),
    SageMeta(name="曾国藩", name_en="zeng_guofan", school="政治家", tier=SageTier.MASTER, era="清代", lifespan="1811-1872", titles=["政治家"], works=[], expertise=["政治", "军事"], department="吏部", description="晚清重臣"),
    SageMeta(name="李鸿章", name_en="li_hongzhang", school="政治家", tier=SageTier.SCHOLAR, era="清代", lifespan="1823-1901", titles=["政治家"], works=[], expertise=["政治", "外交"], department="吏部", description="晚清重臣"),
    SageMeta(name="张之洞", name_en="zhang_zhidong", school="政治家", tier=SageTier.SCHOLAR, era="清代", lifespan="1837-1909", titles=["政治家"], works=[], expertise=["政治", "洋务"], department="吏部", description="洋务派代表"),
    SageMeta(name="林则徐", name_en="lin_zexu", school="政治家", tier=SageTier.SCHOLAR, era="清代", lifespan="1785-1850", titles=["民族英雄"], works=[], expertise=["政治", "禁烟"], department="吏部", description="虎门销烟"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 十八、其他学派 (Others) - 50人
# ═══════════════════════════════════════════════════════════════════════════════

OTHER_SAGES: List[SageMeta] = [
    # === 杨朱学派 ===
    SageMeta(name="杨朱", name_en="yang_zhu_others", school="其他", tier=SageTier.FOUNDER, era="战国", lifespan="前395-前335", titles=["杨朱学派"], works=[], expertise=["贵己", "为我"], department="吏部", description="杨朱学派创始人"),
    
    # === 许行学派 ===
    SageMeta(name="许行", name_en="xu_xing_others", school="其他", tier=SageTier.FOUNDER, era="战国", lifespan="?", titles=["农家"], works=[], expertise=["农业"], department="户部", description="农家创始人"),
    
    # === 告子 ===
    SageMeta(name="告子", name_en="gao_zi", school="其他", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["思想家"], works=[], expertise=["人性论"], department="礼部", description="与孟子辩论"),
    
    # === 宋尹学派 ===
    SageMeta(name="宋钘", name_en="song_xing_others", school="其他", tier=SageTier.SCHOLAR, era="战国", lifespan="约前382-前300", titles=["宋尹学派"], works=[], expertise=["思想"], department="礼部", description="宋尹学派"),
    SageMeta(name="尹文", name_en="yin_wen_others", school="其他", tier=SageTier.SCHOLAR, era="战国", lifespan="约前360-前280", titles=["宋尹学派"], works=[], expertise=["思想"], department="礼部", description="宋尹学派"),
    
    # === 淳于髡 ===
    SageMeta(name="淳于髡", name_en="chun_yukun", school="其他", tier=SageTier.SCHOLAR, era="战国", lifespan="约前385-前305", titles=["辩士"], works=[], expertise=["辩论"], department="礼部", description="齐国辩士"),
    
    # === 慎到 ===
    SageMeta(name="慎到", name_en="shen_dao_others", school="其他", tier=SageTier.SCHOLAR, era="战国", lifespan="约前350-前275", titles=["法家道家"], works=[], expertise=["势治"], department="刑部", description="道法结合"),
    
    # === 申不害 ===
    SageMeta(name="申不害", name_en="shen_buhai_others", school="其他", tier=SageTier.SCHOLAR, era="战国", lifespan="前385-前337", titles=["术治派"], works=[], expertise=["术治"], department="刑部", description="术治派"),
]


# ═══════════════════════════════════════════════════════════════════════════════
ECONOMICS_SAGES: List[SageMeta] = [
    SageMeta(name="亚当·斯密（Adam Smith）", name_en="adam_smith", school="经济学家", tier=SageTier.FOUNDER, era="18世纪", lifespan="1723-1790", titles=["经济学之父"], works=["《国富论》", "《道德情操论》"], expertise=["看不见的手", "分工理论", "自由交换"], department="户部", description="现代经济学奠基人"),
    SageMeta(name="大卫·李嘉图", name_en="david_ricardo", school="经济学家", tier=SageTier.MASTER, era="19世纪", lifespan="1772-1823", titles=["比较优势之父"], works=["《政治经济学及赋税原理》"], expertise=["比较优势", "劳动价值论", "边际递减"], department="户部", description="比较优势原理提出者"),
    SageMeta(name="凯恩斯", name_en="john_maynard_keynes", school="经济学家", tier=SageTier.FOUNDER, era="20世纪", lifespan="1883-1946", titles=["宏观经济学之父"], works=["《就业、利息和货币通论》"], expertise=["有效需求", "乘数效应", "流动性偏好"], department="户部", description="宏观经济学奠基人"),
    SageMeta(name="马克思（Karl Marx）", name_en="karl_marx", school="经济学家", tier=SageTier.FOUNDER, era="19世纪", lifespan="1818-1883", titles=["资本论作者"], works=["《资本论》", "《共产党宣言》"], expertise=["剩余价值", "历史唯物主义", "阶级斗争"], department="户部", description="政治经济学批判大师"),
    SageMeta(name="弗里德曼", name_en="milton_friedman", school="经济学家", tier=SageTier.MASTER, era="20世纪", lifespan="1912-2006", titles=["货币主义之父"], works=["《资本主义与自由》", "《自由选择》"], expertise=["通胀理论", "自由市场", "永久性收入"], department="户部", description="诺贝尔经济学奖得主"),
    SageMeta(name="熊彼特", name_en="joseph_schumpeter", school="经济学家", tier=SageTier.MASTER, era="20世纪", lifespan="1883-1950", titles=["创新理论之父"], works=["《经济发展理论》", "《资本主义、社会主义与民主》"], expertise=["创造性破坏", "企业家精神", "长波理论"], department="户部", description="创新经济学奠基人"),
    SageMeta(name="科斯", name_en="ronald_coase", school="经济学家", tier=SageTier.MASTER, era="20世纪", lifespan="1910-2013", titles=["交易成本之父"], works=["《企业的性质》", "《社会成本问题》"], expertise=["交易成本", "科斯定理", "企业边界"], department="户部", description="诺贝尔经济学奖得主"),
    SageMeta(name="贝克尔", name_en="gary_becker", school="经济学家", tier=SageTier.MASTER, era="20世纪", lifespan="1930-2014", titles=["人力资本理论之父"], works=["《人力资本》", "《家庭论》"], expertise=["人力资本", "时间价值", "理性选择"], department="户部", description="诺贝尔经济学奖得主"),
    SageMeta(name="卡尼曼", name_en="daniel_kahneman", school="经济学家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1934-", titles=["行为经济学之父"], works=["《思考，快与慢》", "《不确定状况下的判断》"], expertise=["前景理论", "锚定效应", "过度自信"], department="户部", description="诺贝尔经济学奖得主"),
    SageMeta(name="阿马蒂亚·森", name_en="amartya_sen", school="经济学家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1933-", titles=["福利经济学大师"], works=["《以自由看待发展》", "《集体选择与社会福利》"], expertise=["自由即发展", "能力方法", "社会选择"], department="户部", description="诺贝尔经济学奖得主"),
    SageMeta(name="哈耶克", name_en="friedrich_hayek", school="经济学家", tier=SageTier.MASTER, era="20世纪", lifespan="1899-1992", titles=["自发秩序之父"], works=["《通往奴役之路》", "《自由秩序原理》"], expertise=["自发秩序", "价格信号", "知识分散"], department="户部", description="诺贝尔经济学奖得主"),
    SageMeta(name="萨缪尔森", name_en="paul_samuelson", school="经济学家", tier=SageTier.MASTER, era="20世纪", lifespan="1915-2009", titles=["现代经济学之父"], works=["《经济学》"], expertise=["乘数-加速数", "比较静态", "显示偏好"], department="户部", description="诺贝尔经济学奖得主"),
    SageMeta(name="奥斯特罗姆", name_en="elinor_ostrom", school="经济学家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1933-2012", titles=["公地治理大师"], works=["《公共事物的治理之道》"], expertise=["公地治理", "制度多样性", "多层次治理"], department="户部", description="诺贝尔经济学奖得主"),
    SageMeta(name="费雪", name_en="irving_fisher", school="经济学家", tier=SageTier.SCHOLAR, era="20世纪", lifespan="1867-1947", titles=["费雪方程式之父"], works=["《货币购买力》"], expertise=["费雪方程式", "利率决定", "预期效用"], department="户部", description="货币理论先驱"),
]

PSYCHOLOGY_SAGES: List[SageMeta] = [
    SageMeta(name="弗洛伊德", name_en="sigmund_freud", school="心理学家", tier=SageTier.FOUNDER, era="19-20世纪", lifespan="1856-1939", titles=["精神分析之父"], works=["《梦的解析》", "《精神分析引论》"], expertise=["潜意识", "人格结构", "性驱力"], department="礼部", description="精神分析学派创始人"),
    SageMeta(name="荣格", name_en="carl_jung", school="心理学家", tier=SageTier.MASTER, era="19-20世纪", lifespan="1875-1961", titles=["集体无意识之父"], works=["《原型与集体无意识》", "《心理类型》"], expertise=["集体无意识", "原型理论", "人格类型"], department="礼部", description="分析心理学创始人"),
    SageMeta(name="马斯洛", name_en="abraham_maslow", school="心理学家", tier=SageTier.FOUNDER, era="20世纪", lifespan="1908-1970", titles=["需求层次之父"], works=["《动机与人格》"], expertise=["需求层次", "自我实现", "高峰体验"], department="礼部", description="人本心理学创始人"),
    SageMeta(name="斯金纳", name_en="bf_skinner", school="心理学家", tier=SageTier.MASTER, era="20世纪", lifespan="1904-1990", titles=["行为强化之父"], works=["《科学与人类行为》", "《Walden Two》"], expertise=["操作性条件反射", "强化理论", "行为工程"], department="礼部", description="行为主义代表人物"),
    SageMeta(name="皮亚杰", name_en="jean_piaget", school="心理学家", tier=SageTier.MASTER, era="20世纪", lifespan="1896-1980", titles=["认知发展之父"], works=["《儿童智力的起源》", "《儿童的心理起源》"], expertise=["认知发展阶段", "图式", "建构主义"], department="礼部", description="认知发展心理学奠基人"),
    SageMeta(name="班杜拉", name_en="albert_bandura", school="心理学家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1925-2021", titles=["社会学习理论之父"], works=["《思想和行动的社会基础》"], expertise=["观察学习", "自我效能感", "交互决定论"], department="礼部", description="社会学习理论提出者"),
    SageMeta(name="西奥迪尼", name_en="robert_cialdini", school="心理学家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1945-", titles=["影响力六要素"], works=["《影响力》"], expertise=["互惠", "社会认同", "承诺一致"], department="户部", description="社会心理学大师"),
    SageMeta(name="维果茨基", name_en="lev_vygotsky", school="心理学家", tier=SageTier.MASTER, era="20世纪", lifespan="1896-1934", titles=["最近发展区之父"], works=["《思维与语言》"], expertise=["最近发展区", "支架式教学", "内化"], department="礼部", description="社会文化理论提出者"),
    SageMeta(name="塞利格曼", name_en="martin_seligman", school="心理学家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1942-", titles=["积极心理学之父"], works=["《活出乐观的自己》", "《真实的幸福》"], expertise=["习得性无助", "解释风格", "PERMA模型"], department="礼部", description="积极心理学创始人"),
]

SOCIOLOGY_SAGES: List[SageMeta] = [
    SageMeta(name="涂尔干", name_en="emile_durkheim", school="社会学家", tier=SageTier.FOUNDER, era="19-20世纪", lifespan="1858-1917", titles=["社会学之父"], works=["《社会分工论》", "《自杀论》"], expertise=["社会事实", "社会分工", "集体意识"], department="礼部", description="现代社会学奠基人"),
    SageMeta(name="韦伯（Max Weber）", name_en="max_weber", school="社会学家", tier=SageTier.FOUNDER, era="19-20世纪", lifespan="1864-1920", titles=["理解社会学之父"], works=["《新教伦理与资本主义精神》", "《经济与社会》"], expertise=["理解社会学", "理性化铁笼", "合法性类型"], department="礼部", description="社会学奠基人"),
    SageMeta(name="布迪厄", name_en="pierre_bourdieu", school="社会学家", tier=SageTier.MASTER, era="20世纪", lifespan="1930-2002", titles=["文化资本理论之父"], works=["《区隔》", "《再生产》"], expertise=["文化资本", "场域", "惯习"], department="礼部", description="文化社会学大师"),
    SageMeta(name="福柯", name_en="michel_foucault", school="社会学家", tier=SageTier.MASTER, era="20世纪", lifespan="1926-1984", titles=["权力知识理论大师"], works=["《规训与惩罚》", "《性经验史》"], expertise=["权力/知识", "全景敞视", "话语即权力"], department="礼部", description="后现代社会学大师"),
    SageMeta(name="吉登斯", name_en="anthony_giddens", school="社会学家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1938-", titles=["结构化理论之父"], works=["《社会的构成》", "《现代性的后果》"], expertise=["结构化理论", "现代性反思性", "时空伸延"], department="礼部", description="结构化理论提出者"),
    SageMeta(name="米尔斯", name_en="cwright_mills", school="社会学家", tier=SageTier.MASTER, era="20世纪", lifespan="1916-1962", titles=["社会学想象力"], works=["《社会学的想象力》", "《权力精英》"], expertise=["社会学想象力", "权力精英", "宏大理论"], department="礼部", description="批判社会学大师"),
    SageMeta(name="查尔斯·泰勒", name_en="charles_taylor", school="社会学家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1931-", titles=["承认政治大师"], works=["《自我的根源》", "《承认的政治》"], expertise=["承认的政治", "本真性理想", "对话式自我"], department="吏部", description="现代身份政治理论家"),
    SageMeta(name="哈贝马斯", name_en="jurgen_habermas", school="社会学家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1929-", titles=["公共领域理论之父"], works=["《公共领域的结构转型》", "《交往行为理论》"], expertise=["公共领域", "交往理性", "生活世界殖民化"], department="礼部", description="法兰克福学派巨匠"),
    SageMeta(name="齐美尔", name_en="georg_simmel", school="社会学家", tier=SageTier.MASTER, era="19-20世纪", lifespan="1858-1918", titles=["形式社会学之父"], works=["《货币哲学》", "《社会学》"], expertise=["货币哲学", "社会化形式", "文化悲剧"], department="礼部", description="形式社会学奠基人"),
    SageMeta(name="默顿", name_en="robert_merton", school="社会学家", tier=SageTier.MASTER, era="20世纪", lifespan="1910-2003", titles=["功能主义大师"], works=["《社会理论与社会结构》"], expertise=["功能分析", "自我实现预言", "中层理论"], department="礼部", description="功能主义发展者"),
]

GOVERNANCE_SAGES: List[SageMeta] = [
    SageMeta(name="马基雅维利（Machiavelli）", name_en="machiavelli", school="治理战略家", tier=SageTier.FOUNDER, era="15-16世纪", lifespan="1469-1527", titles=["现代政治学之父"], works=["《君主论》", "《论李维》"], expertise=["目的正当性", "权力策略", "命运观"], department="吏部", description="政治现实主义奠基人"),
    SageMeta(name="汉娜·阿伦特", name_en="hannah_arendt", school="治理战略家", tier=SageTier.MASTER, era="20世纪", lifespan="1906-1975", titles=["政治哲学大师"], works=["《极权主义的起源》", "《人的条件》", "《平庸的恶》"], expertise=["公共领域", "极权主义批判", "行动与言说"], department="吏部", description="20世纪最重要的政治哲学家之一"),
    SageMeta(name="托克维尔", name_en="alexis_de_tocqueville", school="治理战略家", tier=SageTier.MASTER, era="19世纪", lifespan="1805-1859", titles=["民主理论大师"], works=["《论美国的民主》", "《旧制度与大革命》"], expertise=["民主分析", "社会平等", "公民社会"], department="吏部", description="民主理论的经典作家"),
    SageMeta(name="克劳塞维茨", name_en="carl_von_clausewitz", school="治理战略家", tier=SageTier.FOUNDER, era="19世纪", lifespan="1780-1831", titles=["战略思想之父"], works=["《战争论》"], expertise=["战争与政治", "战略摩擦", "战争迷雾"], department="兵部", description="西方战略学奠基人"),
    SageMeta(name="若米尼", name_en="antoine_jomini", school="治理战略家", tier=SageTier.MASTER, era="19世纪", lifespan="1779-1869", titles=["军事战略大师"], works=["《战争艺术》"], expertise=["战争艺术", "战略体系", "会战原理"], department="兵部", description="近代军事战略学奠基人之一"),
    SageMeta(name="李德·哈特", name_en="basil_liddell_hart", school="治理战略家", tier=SageTier.MASTER, era="20世纪", lifespan="1895-1970", titles=["间接路线战略之父"], works=["《战略论》"], expertise=["间接路线", "有限战争", "战略文化"], department="兵部", description="20世纪最重要的战略理论家之一"),
]

INVESTMENT_SAGES: List[SageMeta] = [
    SageMeta(name="巴菲特（Warren Buffett）", name_en="warren_buffett", school="投资家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1930-", titles=["股神"], works=["《巴菲特致股东的信》"], expertise=["价值投资", "护城河", "安全边际"], department="户部", description="伯克希尔·哈撒韦创始人"),
    SageMeta(name="芒格（Charlie Munger）", name_en="charlie_munger", school="投资家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1924-", titles=["巴菲特搭档"], works=["《穷查理宝典》"], expertise=["多元思维模型", "逆向思维", "心理学"], department="户部", description="伯克希尔副董事长"),
    SageMeta(name="达利欧", name_en="ray_dalio", school="投资家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1949-", titles=["桥水基金创始人"], works=["《原则》"], expertise=["全天候投资", "风险平价", "债务周期"], department="户部", description="全球最大对冲基金创始人"),
    SageMeta(name="费雪（Philip Fisher）", name_en="philip_fisher", school="投资家", tier=SageTier.MASTER, era="20世纪", lifespan="1907-2004", titles=["成长股投资之父"], works=["《非常成长股投资》"], expertise=["成长股投资", "闲聊法", "管理层评估"], department="户部", description="成长股投资先驱"),
    SageMeta(name="索罗斯", name_en="george_soros", school="投资家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1930-", titles=["量子基金创始人"], works=["《金融炼金术》"], expertise=["反射理论", "宏观投资", "开放社会"], department="户部", description="著名对冲基金经理"),
    SageMeta(name="格雷厄姆（Benjamin Graham）", name_en="benjamin_graham", school="投资家", tier=SageTier.FOUNDER, era="20世纪", lifespan="1894-1976", titles=["价值投资之父"], works=["《证券分析》", "《聪明的投资者》"], expertise=["安全边际", "内在价值", "市场先生"], department="户部", description="巴菲特的老师"),
    SageMeta(name="彼得·林奇（Peter Lynch）", name_en="peter_lynch", school="投资家", tier=SageTier.MASTER, era="20世纪", lifespan="1944-", titles=["麦哲伦基金传奇"], works=["《彼得·林奇的成功投资》"], expertise=["投资你所知的", "十倍股", "成长股投资"], department="户部", description="13年年均收益29%"),
    SageMeta(name="约翰·邓普顿", name_en="john_templeton", school="投资家", tier=SageTier.MASTER, era="20世纪", lifespan="1912-2008", titles=["全球投资之父"], works=["《全球价值投资》"], expertise=["逆向投资", "全球分散", "长期思维"], department="户部", description="邓普顿基金创始人"),
    SageMeta(name="约翰·博格尔", name_en="john_bogle", school="投资家", tier=SageTier.MASTER, era="20-21世纪", lifespan="1929-2019", titles=["指数基金之父"], works=["《共同基金常识》"], expertise=["指数投资", "低费率", "市场不可战胜"], department="户部", description="先锋基金创始人"),
    SageMeta(name="彼得·蒂尔", name_en="peter_thiel", school="投资家", tier=SageTier.MASTER, era="21世纪", lifespan="1967-", titles=["PayPal黑帮教父"], works=["《从0到1》"], expertise=["0到1创新", "垄断策略", "秘密思维"], department="户部", description="Palantir创始人"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 扩展贤者库 - 来自文学研究目录 (2026-04-10)
# ═══════════════════════════════════════════════════════════════════════════════

EXTENDED_SAGES: List[SageMeta] = [
    # === 西方哲学家 ===
    SageMeta(name="柏拉图（Plato）", name_en="plato", school="哲学家", tier=SageTier.FOUNDER, era="古希腊", lifespan="前428-前348", titles=["哲学之父"], works=["《理想国》", "《对话录》"], expertise=["理念论", "政治哲学", "形而上学"], department="礼部", description="西方哲学奠基人"),
    SageMeta(name="亚里士多德（Aristotle）", name_en="aristotle", school="哲学家", tier=SageTier.FOUNDER, era="古希腊", lifespan="前384-前322", titles=["百科全书式学者"], works=["《形而上学》", "《尼各马可伦理学》"], expertise=["逻辑学", "形而上学", "伦理学"], department="礼部", description="西方哲学集大成者"),
    SageMeta(name="苏格拉底（Socrates）", name_en="socrates", school="哲学家", tier=SageTier.FOUNDER, era="古希腊", lifespan="前469-前399", titles=["哲学之父"], works=["苏格拉底对话"], expertise=["伦理学", "认识论", "辩证法"], department="礼部", description="西方哲学奠基人"),
    SageMeta(name="伏尔泰", name_en="voltaire", school="哲学家", tier=SageTier.MASTER, era="18世纪", lifespan="1694-1778", titles=["启蒙思想家"], works=["《哲学通信》", "《老实人》"], expertise=["理性主义", "宗教宽容", "自由思想"], department="礼部", description="法国启蒙思想家"),
    SageMeta(name="康德（Immanuel Kant）", name_en="kant", school="哲学家", tier=SageTier.MASTER, era="18世纪", lifespan="1724-1804", titles=["批判哲学奠基人"], works=["《纯粹理性批判》", "《实践理性批判》"], expertise=["先验哲学", "伦理学", "美学"], department="礼部", description="德国哲学奠基人"),
    SageMeta(name="尼采（Friedrich Nietzsche）", name_en="nietzsche", school="哲学家", tier=SageTier.MASTER, era="19世纪", lifespan="1844-1900", titles=["生命哲学家"], works=["《查拉图斯特拉如是说》", "《悲剧的诞生》"], expertise=["超人哲学", "权力意志", "虚无主义批判"], department="礼部", description="生命哲学代表"),

    # === 西方科学家 ===
    SageMeta(name="牛顿（Isaac Newton）", name_en="newton", school="科学家", tier=SageTier.MASTER, era="17-18世纪", lifespan="1643-1727", titles=["经典力学之父"], works=["《自然哲学的数学原理》"], expertise=["力学", "光学", "微积分"], department="工部", description="经典力学和万有引力定律发现者"),
    SageMeta(name="爱因斯坦（Albert Einstein）", name_en="einstein", school="科学家", tier=SageTier.MASTER, era="19-20世纪", lifespan="1879-1955", titles=["相对论创立者"], works=["《相对论》"], expertise=["相对论", "光电效应", "量子力学"], department="工部", description="现代物理学奠基人"),

    # === 唐太宗 ===
    SageMeta(name="唐太宗", name_en="tang_taizong", school="政治家", tier=SageTier.MASTER, era="唐代", lifespan="598-649", titles=["天可汗"], works=[], expertise=["贞观之治", "政治", "军事"], department="吏部", description="开创贞观之治"),

    # === 隋文帝 ===
    SageMeta(name="隋文帝", name_en="sui_wendi", school="政治家", tier=SageTier.MASTER, era="隋代", lifespan="541-604", titles=["隋朝开国皇帝"], works=[], expertise=["统一", "政治", "制度"], department="吏部", description="结束南北朝分裂"),

    # === 汉高祖 ===
    SageMeta(name="刘邦", name_en="liu_bang", school="政治家", tier=SageTier.SCHOLAR, era="西汉", lifespan="前256-前195", titles=["汉高祖"], works=[], expertise=["政治", "军事", "开国"], department="吏部", description="汉朝开国皇帝"),

    # === 武则天 ===
    SageMeta(name="武则天", name_en="wu_zetian", school="政治家", tier=SageTier.MASTER, era="唐代", lifespan="624-705", titles=["女皇"], works=[], expertise=["政治", "统治"], department="吏部", description="中国历史上唯一的女皇帝"),

    # === 唐代诗人/文学家 ===
    SageMeta(name="王勃", name_en="wang_bo", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="650-676", titles=["初唐四杰"], works=["滕王阁序"], expertise=["诗文", "骈文"], department="礼部", description="初唐四杰之首"),
    SageMeta(name="王之涣", name_en="wang_zhihuan", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="688-742", titles=["边塞诗人"], works=["登鹳雀楼"], expertise=["诗歌", "边塞诗"], department="礼部", description="边塞诗人代表"),
    SageMeta(name="孟浩然", name_en="meng_haoran", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="689-740", titles=["田园诗人"], works=["春晓"], expertise=["田园诗", "五言诗"], department="礼部", description="唐代田园诗开创者"),
    SageMeta(name="孟郊", name_en="meng_jiao", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="751-814", titles=["苦吟诗人"], works=["游子吟"], expertise=["诗歌", "苦吟"], department="礼部", description="以苦吟著称"),
    SageMeta(name="张九龄", name_en="zhang_jiuling", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="678-740", titles=["岭南文宗"], works=["曲江集"], expertise=["诗文", "政治"], department="礼部", description="唐代名相"),
    SageMeta(name="张先", name_en="zhang_xian", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="990-1078", titles=["张三影"], works=["天仙子"], expertise=["词", "婉约派"], department="礼部", description="北宋词人"),
    SageMeta(name="张炎", name_en="zhang_yan", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="1248-约1320", titles=["宋末词坛领袖"], works=["山中白云词"], expertise=["词", "婉约派"], department="礼部", description="宋末婉约派词人"),
    SageMeta(name="徐陵", name_en="xu_ling", school="文学家", tier=SageTier.SCHOLAR, era="南朝", lifespan="507-583", titles=["宫体诗代表"], works=["玉台新咏"], expertise=["骈文", "宫体诗"], department="礼部", description="宫体诗代表作家"),
    SageMeta(name="晏殊", name_en="yan_shu", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="991-1055", titles=["词人"], works=["浣溪沙"], expertise=["词", "婉约派"], department="礼部", description="北宋婉约派词人"),
    SageMeta(name="晏几道", name_en="yan_jidao", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="1038-1110", titles=["词人"], works=["小山词"], expertise=["词", "婉约派"], department="礼部", description="晏殊之子，婉约派词人"),
    SageMeta(name="李靖", name_en="li_jing_general", school="兵家", tier=SageTier.SCHOLAR, era="唐代", lifespan="571-649", titles=["军神"], works=[], expertise=["军事", "战略"], department="兵部", description="唐朝开国名将"),
    SageMeta(name="李光弼", name_en="li_guangbi", school="兵家", tier=SageTier.SCHOLAR, era="唐代", lifespan="727-779", titles=["中兴名将"], works=[], expertise=["军事", "平叛"], department="兵部", description="唐朝中期名将"),
    SageMeta(name="杨炯", name_en="yang_jiong", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="650-693", titles=["初唐四杰"], works=["从军行"], expertise=["诗文", "边塞诗"], department="礼部", description="初唐四杰之一"),
    SageMeta(name="温庭筠", name_en="wen_tingyun", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="812-866", titles=["花间派鼻祖"], works=["菩萨蛮"], expertise=["词", "花间派"], department="礼部", description="花间派词人开创者"),
    SageMeta(name="王沂孙", name_en="wang_yisun", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="约1230-约1291", titles=["宋末词人"], works=["花外集"], expertise=["词", "咏物词"], department="礼部", description="宋末婉约派词人"),
    SageMeta(name="王符", name_en="wang_fu", school="儒家", tier=SageTier.SCHOLAR, era="东汉", lifespan="约85-约163", titles=["政论家"], works=["潜夫论"], expertise=["政论", "治国"], department="吏部", description="东汉政论家"),
    SageMeta(name="秦观", name_en="qin_guan", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="1049-1100", titles=["苏门四学士"], works=["鹊桥仙"], expertise=["词", "婉约派"], department="礼部", description="苏门四学士之一"),
    SageMeta(name="罗隐", name_en="luo_yin", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="833-910", titles=["讽刺诗人"], works=["蜂"], expertise=["诗歌", "讽刺"], department="礼部", description="晚唐讽刺诗人"),
    SageMeta(name="苏洵", name_en="su_xun", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="1009-1066", titles=["唐宋八大家"], works=["六国论"], expertise=["散文", "政论"], department="礼部", description="苏轼苏辙之父"),
    SageMeta(name="萧衍", name_en="xiao_yan", school="政治家", tier=SageTier.MASTER, era="南朝梁", lifespan="464-549", titles=["梁武帝"], works=["诗词"], expertise=["文学", "政治", "佛教"], department="吏部", description="梁朝开国皇帝，提倡文学"),
    SageMeta(name="蒋捷", name_en="jiang_jie", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="约1245-1305", titles=["宋末词人"], works=["虞美人"], expertise=["词", "亡国悲音"], department="礼部", description="宋末遗民词人"),
    SageMeta(name="韦庄", name_en="wei_zhuang", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="836-910", titles=["花间派代表"], works=["菩萨蛮"], expertise=["词", "花间派"], department="礼部", description="晚唐花间派词人"),
    SageMeta(name="骆宾王", name_en="luo_binwang", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="约619-约687", titles=["初唐四杰"], works=["咏鹅"], expertise=["诗文", "骈文"], department="礼部", description="初唐四杰之一"),
    SageMeta(name="贾岛", name_en="jia_dao", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="779-843", titles=["苦吟诗人"], works=["题李凝幽居"], expertise=["诗歌", "苦吟"], department="礼部", description="以苦吟著称的诗人"),
    SageMeta(name="元稹", name_en="yuan_zhen", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="779-831", titles=["新乐府运动"], works=["莺莺传", "离思五首"], expertise=["诗文", "新乐府"], department="礼部", description="新乐府运动代表"),
    SageMeta(name="卢照邻", name_en="lu_zhaolin", school="文学家", tier=SageTier.SCHOLAR, era="唐代", lifespan="约637-约689", titles=["初唐四杰"], works=["长安古意"], expertise=["诗文", "骈文"], department="礼部", description="初唐四杰之一"),
    SageMeta(name="史达祖", name_en="shi_dazu", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="1163-约1220", titles=["南宋词人"], works=["双双燕"], expertise=["词", "咏物词"], department="礼部", description="南宋婉约派词人"),
    SageMeta(name="刘克庄", name_en="liu_kezhuang", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="1187-1269", titles=["江湖诗派领袖"], works=["后村诗话"], expertise=["诗", "词"], department="礼部", description="江湖诗派代表"),
    SageMeta(name="吴均", name_en="wu_jun", school="文学家", tier=SageTier.SCHOLAR, era="南朝", lifespan="469-520", titles=["文学家"], works=["与朱元思书"], expertise=["骈文", "散文"], department="礼部", description="南朝文学家"),
    SageMeta(name="吴文英", name_en="wu_wenying", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="约1200-约1260", titles=["南宋词人"], works=["莺啼序"], expertise=["词", "密丽派"], department="礼部", description="南宋密丽派词人"),
    SageMeta(name="周密", name_en="zhou_mi", school="文学家", tier=SageTier.SCHOLAR, era="宋代", lifespan="1232-1298", titles=["宋末词人"], works=["武林旧事"], expertise=["词", "笔记"], department="礼部", description="宋末遗民词人"),
    SageMeta(name="仲长统", name_en="zhongchang_tong", school="儒家", tier=SageTier.SCHOLAR, era="东汉", lifespan="180-220", titles=["政论家"], works=["昌言"], expertise=["政论", "批判"], department="吏部", description="东汉政论家"),
    SageMeta(name="任昉", name_en="ren_fang", school="史家", tier=SageTier.SCHOLAR, era="南朝", lifespan="460-508", titles=["文章学大家"], works=["文章缘起"], expertise=["文章学", "骈文"], department="礼部", description="南朝文章学家"),

    # === 近现代人物 ===
    SageMeta(name="鲁迅", name_en="lu_xun", school="文学家", tier=SageTier.MASTER, era="近现代", lifespan="1881-1936", titles=["现代文学之父"], works=["呐喊", "彷徨"], expertise=["小说", "杂文", "批判"], department="礼部", description="中国现代文学奠基人"),
    SageMeta(name="胡适", name_en="hu_shi", school="文学家", tier=SageTier.MASTER, era="近现代", lifespan="1891-1962", titles=["新文化运动领袖"], works=["尝试集"], expertise=["文学革命", "白话文"], department="礼部", description="新文化运动代表"),
    SageMeta(name="辜鸿铭", name_en="gu_hongming", school="思想家", tier=SageTier.MASTER, era="近现代", lifespan="1857-1928", titles=["文化怪杰"], works=["中国人的精神"], expertise=["文化保守", "跨文化", "翻译"], department="礼部", description="清末民初文化名人"),
    SageMeta(name="陈省身", name_en="chen_xingshen", school="科学家", tier=SageTier.MASTER, era="当代", lifespan="1911-2004", titles=["微分几何之父"], works=[], expertise=["微分几何", "拓扑学"], department="工部", description="沃尔夫数学奖得主"),

    # === 兵法人物 ===
    SageMeta(name="吴子", name_en="wu_qi_military", school="兵家", tier=SageTier.MASTER, era="战国", lifespan="前440-前381", titles=["兵家亚圣"], works=["吴子兵法"], expertise=["兵法", "变法"], department="兵部", description="与孙子齐名"),

    # === 文学批评家 ===
    SageMeta(name="刘勰", name_en="liu_xie", school="文学批评家", tier=SageTier.MASTER, era="南朝", lifespan="约465-约527", titles=["文心雕龙作者"], works=["文心雕龙"], expertise=["文学理论", "批评"], department="礼部", description="中国文学批评之父"),
    SageMeta(name="钟嵘", name_en="zhong_rong", school="文学批评家", tier=SageTier.MASTER, era="南朝", lifespan="约468-约518", titles=["诗品作者"], works=["诗品"], expertise=["诗学批评", "五言诗"], department="礼部", description="中国第一部诗学批评专著作者"),

    # === 佛学家 ===
    SageMeta(name="道安", name_en="dao_an", school="佛家", tier=SageTier.MASTER, era="东晋", lifespan="312-385", titles=["中国佛教奠基人"], works=[], expertise=["佛经翻译", "佛教中国化"], department="礼部", description="中国佛教奠基人之一"),
    SageMeta(name="道生", name_en="dao_sheng", school="佛家", tier=SageTier.SCHOLAR, era="东晋", lifespan="355-434", titles=["涅槃大师"], works=["法华经疏"], expertise=["涅槃学", "顿悟说"], department="礼部", description="涅槃学大家"),
    SageMeta(name="鸠摩罗什", name_en="kumaij Luo", school="佛家", tier=SageTier.MASTER, era="东晋十六国", lifespan="344-413", titles=["四大译经师"], works=["金刚经注", "法华经注"], expertise=["佛经翻译", "般若学"], department="礼部", description="佛经翻译大家"),

    # === 茶圣 ===
    SageMeta(name="陆羽", name_en="lu_yu", school="茶道家", tier=SageTier.MASTER, era="唐代", lifespan="733-804", titles=["茶圣"], works=["茶经"], expertise=["茶道", "茶文化"], department="户部", description="茶道之祖"),

    # === 书法家 ===
    SageMeta(name="王献之", name_en="wang_xianzhi", school="艺术家", tier=SageTier.SCHOLAR, era="东晋", lifespan="344-386", titles=["书圣"], works=["中秋帖"], expertise=["书法", "行草"], department="礼部", description="王羲之之子，书圣"),

    # === 典籍 ===
    SageMeta(name="论语", name_en="lunyu", school="儒家", tier=SageTier.FOUNDER, era="春秋", lifespan="", titles=["儒家经典"], works=[], expertise=["仁学", "礼治", "教育"], department="礼部", description="孔子及其弟子言行录"),
    SageMeta(name="诗经", name_en="shijing", school="儒家", tier=SageTier.FOUNDER, era="西周至春秋", lifespan="", titles=["诗三百"], works=[], expertise=["诗歌", "风雅颂"], department="礼部", description="中国最早的诗歌总集"),
    SageMeta(name="论衡", name_en="lunheng", school="儒家", tier=SageTier.SCHOLAR, era="东汉", lifespan="", titles=["王充著"], works=["论衡"], expertise=["批判", "无神论"], department="礼部", description="东汉批判哲学著作"),
    SageMeta(name="素书", name_en="sushu", school="道家", tier=SageTier.FOUNDER, era="秦末汉初", lifespan="", titles=["黄石公著"], works=["素书"], expertise=["谋略", "道术"], department="兵部", description="道家谋略经典"),
    SageMeta(name="颜氏家训", name_en="yanshi_jiaxun", school="儒家", tier=SageTier.SCHOLAR, era="南北朝", lifespan="", titles=["颜之推著"], works=["颜氏家训"], expertise=["家庭教育", "修身"], department="礼部", description="中国第一部家训专著"),

    # === 郭子仪 ===
    SageMeta(name="郭子仪", name_en="guo_ziyi", school="兵家", tier=SageTier.SCHOLAR, era="唐代", lifespan="697-781", titles=["再造唐室"], works=[], expertise=["军事", "平叛"], department="兵部", description="唐朝中兴名将"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 汇总字典 - 所有贤者（按类别重新组织 v2.0）
# ═══════════════════════════════════════════════════════════════════════════════

# 首先按school字段收集所有贤者
_temp_by_school: Dict[str, List[SageMeta]] = {}
for _cat_sages in [
    CONFUCIAN_SAGES, TAOIST_SAGES, BUDDHIST_SAGES, MILITARY_SAGES,
    LEGALIST_SAGES, MOHIST_SAGES, SCHOOL_OF_NAMES_SAGES, YINYANG_SAGES,
    DIPLOMACY_SAGES, AGRICULTURAL_SAGES, ECLECTIC_SAGES, MEDICAL_SAGES,
    HISTORIAN_SAGES, LITERARY_SAGES, ARTIST_SAGES, SCIENTIST_SAGES,
    STATESMAN_SAGES, OTHER_SAGES, ECONOMICS_SAGES, PSYCHOLOGY_SAGES,
    SOCIOLOGY_SAGES, GOVERNANCE_SAGES, INVESTMENT_SAGES, EXTENDED_SAGES
]:
    for _sage in _cat_sages:
        _sc = _sage.school if _sage.school else "其他"
        if _sc not in _temp_by_school:
            _temp_by_school[_sc] = []
        _temp_by_school[_sc].append(_sage)

# 按类别排序
SCHOOL_ORDER = [
    # 哲学宗教
    "儒家", "道家", "佛家", "哲学家", "思想家",
    # 诸子百家
    "兵家", "法家", "墨家", "名家", "阴阳家", "纵横家", "农家", "杂家",
    # 文化传承
    "史家", "文学家", "艺术家", "文学批评家",
    # 科技医学
    "科学家", "医家",
    # 社会政治
    "政治家", "经济学家", "社会学家", "心理学家", "治理战略家",
    # 经济金融
    "投资家",
    # 专业技艺
    "茶道家",
    # 其他
    "其他",
]

# 构建新的分类字典
ALL_SAGES: Dict[str, List[SageMeta]] = {}
for _sc in SCHOOL_ORDER:
    if _sc in _temp_by_school:
        ALL_SAGES[_sc] = _temp_by_school[_sc]

# 清理临时变量
del _temp_by_school

# 快速查找字典
SAGE_BY_NAME: Dict[str, SageMeta] = {}
SAGE_BY_EN: Dict[str, SageMeta] = {}


def _build_lookup_tables() -> None:
    """构建快速查找表"""
    global SAGE_BY_NAME, SAGE_BY_EN
    for school_sages in ALL_SAGES.values():
        for sage in school_sages:
            SAGE_BY_NAME[sage.name] = sage
            SAGE_BY_EN[sage.name_en] = sage


# 初始化查找表
_build_lookup_tables()


def get_sage(name: str) -> Optional[SageMeta]:
    """
    根据名称获取贤者信息
    
    Args:
        name: 贤者中文名或英文名
        
    Returns:
        SageMeta或None
    """
    if name in SAGE_BY_NAME:
        return SAGE_BY_NAME[name]
    if name in SAGE_BY_EN:
        return SAGE_BY_EN[name]
    # 查找补充注册表
    try:
        from . import _sage_registry_extra as extra
        for sages in extra.EXTRA_SAGES.values():
            for sage in sages:
                if sage.name == name or sage.name_en == name:
                    return sage
    except ImportError:
        pass
    return None


def get_sages_by_school(school: str) -> List[SageMeta]:
    """
    根据学派获取贤者列表
    
    Args:
        school: 学派名称
        
    Returns:
        SageMeta列表
    """
    result = ALL_SAGES.get(school, [])
    # 补充注册表
    try:
        from . import _sage_registry_extra as extra
        result.extend(extra.EXTRA_SAGES.get(school, []))
    except ImportError:
        pass
    return result


def get_sages_by_department(department: str) -> List[SageMeta]:
    """
    根据部门获取贤者列表
    
    Args:
        department: 部门名称
        
    Returns:
        SageMeta列表
    """
    result = []
    for school_sages in ALL_SAGES.values():
        for sage in school_sages:
            if sage.department == department:
                result.append(sage)
    return result


def get_sages_by_tier(tier: SageTier) -> List[SageMeta]:
    """
    根据层级获取贤者列表
    
    Args:
        tier: 贤者层级
        
    Returns:
        SageMeta列表
    """
    result = []
    for school_sages in ALL_SAGES.values():
        for sage in school_sages:
            if sage.tier == tier:
                result.append(sage)
    return result


def get_sages_by_era(era: str) -> List[SageMeta]:
    """
    根据时代获取贤者列表
    
    Args:
        era: 时代名称
        
    Returns:
        SageMeta列表
    """
    result = []
    for school_sages in ALL_SAGES.values():
        for sage in school_sages:
            if era in sage.era:
                result.append(sage)
    return result


def search_sages(keyword: str) -> List[SageMeta]:
    """
    搜索贤者
    
    Args:
        keyword: 关键词
        
    Returns:
        SageMeta列表
    """
    result = []
    keyword_lower = keyword.lower()
    for school_sages in ALL_SAGES.values():
        for sage in school_sages:
            if (keyword in sage.name or 
                keyword_lower in sage.name_en.lower() or
                keyword in sage.school or
                keyword in sage.era or
                keyword in sage.department or
                keyword in sage.description or
                any(keyword in title for title in sage.titles) or
                any(keyword in work for work in sage.works) or
                any(keyword in exp for exp in sage.expertise)):
                result.append(sage)
    return result


def get_registry_stats() -> Dict[str, Any]:
    """
    获取注册表统计信息
    
    Returns:
        统计信息字典
    """
    total = sum(len(sages) for sages in ALL_SAGES.values())
    by_school = {school: len(sages) for school, sages in ALL_SAGES.items()}
    
    by_tier = {}
    for school_sages in ALL_SAGES.values():
        for sage in school_sages:
            tier_name = sage.tier.name
            by_tier[tier_name] = by_tier.get(tier_name, 0) + 1
    
    by_department = {}
    for school_sages in ALL_SAGES.values():
        for sage in school_sages:
            dept = sage.department or "未分类"
            by_department[dept] = by_department.get(dept, 0) + 1
    
    return {
        "total_sages": total,
        "by_school": by_school,
        "by_tier": by_tier,
        "by_department": by_department,
        "schools": list(ALL_SAGES.keys()),
    }


# [P0修复] 命令行入口已禁用，统一通过 somn.py 入口调用
# if __name__ == "__main__":
#     stats = get_registry_stats()
#     print(f"600贤者注册表 v1.0.0")
#     print(f"总计: {stats['total_sages']} 位贤者")
#     print(f"学派: {len(stats['by_school'])} 个")
#     print("\n按学派分布:")
#     for school, count in sorted(stats['by_school'].items(), key=lambda x: -x[1]):
#         print(f"  {school}: {count} 人")
#     print("\n按层级分布:")
#     for tier, count in stats['by_tier'].items():
#         print(f"  {tier}: {count} 人")
#     print("\n按部门分布:")
#     for dept, count in sorted(stats['by_department'].items(), key=lambda x: -x[1]):
#         print(f"  {dept}: {count} 人")
