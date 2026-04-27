# -*- coding: utf-8 -*-
"""
补充注册表 - 来自噪音文件清理的真实人物
创建时间: 2026-04-21
用途: 补充75位未被主注册表收录的真实历史人物
"""
from typing import List
from ._sage_registry_full import SageMeta, SageTier

# ═══════════════════════════════════════════════════════════════════════════════
# 兵家 (5人)
# ═══════════════════════════════════════════════════════════════════════════════
MILITARY_SAGES_EXTRA: List[SageMeta] = [
    SageMeta(name="孙子", name_en="sunzi_bing", school="兵家", tier=SageTier.SCHOLAR, era="春秋", lifespan="?", titles=["兵圣"], works=["孙子兵法"], expertise=["战略", "军事"], department="兵部", description="春秋兵家，著孙子兵法"),
    SageMeta(name="庞涓", name_en="pangjuan", school="兵家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["魏将"], works=[], expertise=["军事"], department="兵部", description="战国魏将，与孙膑同门"),
    SageMeta(name="尉迟恭", name_en="yuchigong", school="兵家", tier=SageTier.SCHOLAR, era="唐代", lifespan="585-658", titles=["门神"], works=[], expertise=["武功", "忠勇"], department="兵部", description="唐初名将"),
    SageMeta(name="秦琼", name_en="qinqiong", school="兵家", tier=SageTier.SCHOLAR, era="唐代", lifespan="?-638", titles=["门神"], works=[], expertise=["武功", "忠勇"], department="兵部", description="唐初名将"),
    SageMeta(name="禽滑釐", name_en="qingua_li", school="兵家", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["墨家弟子"], works=[], expertise=["军事", "墨家"], department="兵部", description="墨家弟子，擅长守城"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 文学 (7人)
# ═══════════════════════════════════════════════════════════════════════════════
LITERARY_SAGES_EXTRA: List[SageMeta] = [
    SageMeta(name="元好问", name_en="yuan_haowen", school="文学", tier=SageTier.SCHOLAR, era="金元", lifespan="1190-1257", titles=["金元之际大诗人"], works=["论诗三十首"], expertise=["诗词", "文学批评"], department="礼部", description="金元之际大诗人"),
    SageMeta(name="归有光", name_en="gui_youguang", school="文学", tier=SageTier.SCHOLAR, era="明代", lifespan="1506-1571", titles=["震川先生"], works=["震川文集"], expertise=["古文", "叙事"], department="礼部", description="明代古文家"),
    SageMeta(name="李煜", name_en="li_yu", school="文学", tier=SageTier.SCHOLAR, era="五代南唐", lifespan="937-978", titles=["南唐后主", "千古词帝"], works=["词集"], expertise=["词", "亡国之痛"], department="礼部", description="千古词帝"),
    SageMeta(name="萧统", name_en="xiao_tong", school="文学", tier=SageTier.SCHOLAR, era="南北朝", lifespan="501-531", titles=["昭明太子"], works=["文选"], expertise=["文学", "编辑"], department="礼部", description="主编文选"),
    SageMeta(name="陈子昂", name_en="chen_ziang", school="文学", tier=SageTier.SCHOLAR, era="唐代", lifespan="659-700", titles=["诗骨"], works=["陈伯玉集"], expertise=["诗歌", "复古"], department="礼部", description="初唐诗歌革新先驱"),
    SageMeta(name="虞世南", name_en="yu_shinan", school="文学", tier=SageTier.SCHOLAR, era="唐代", lifespan="558-638", titles=["初唐四大家"], works=["虞世南集"], expertise=["书法", "诗文"], department="礼部", description="初唐书法家"),
    SageMeta(name="李德裕", name_en="li_deyu", school="文学", tier=SageTier.MASTER, era="唐代", lifespan="787-850", titles=["李卫公"], works=["会昌一品集"], expertise=["政治", "文学"], department="吏部", description="唐代名相"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 史学 (6人)
# ═══════════════════════════════════════════════════════════════════════════════
HISTORIAN_SAGES_EXTRA: List[SageMeta] = [
    SageMeta(name="冯梦龙", name_en="feng_menglong", school="史学", tier=SageTier.SCHOLAR, era="明代", lifespan="1574-1646", titles=["通俗文学家"], works=["三言"], expertise=["小说", "民间文学"], department="礼部", description="三言主编"),
    SageMeta(name="凌濛初", name_en="ling_mengchu", school="史学", tier=SageTier.SCHOLAR, era="明代", lifespan="1580-1644", titles=["小说家"], works=["二拍"], expertise=["小说"], department="礼部", description="二拍作者"),
    SageMeta(name="刘义庆", name_en="liu_yiqing", school="史学", tier=SageTier.SCHOLAR, era="南北朝", lifespan="403-444", titles=["宋宗室"], works=["世说新语"], expertise=["文学", "笔记"], department="礼部", description="世说新语作者"),
    SageMeta(name="金圣叹", name_en="jin_shentan", school="史学", tier=SageTier.SCHOLAR, era="清代", lifespan="1608-1661", titles=["文学评点家"], works=["金批西厢"], expertise=["文学批评", "评点"], department="礼部", description="文学评点大师"),
    SageMeta(name="郑樵", name_en="zheng_qiao", school="史学", tier=SageTier.SCHOLAR, era="宋代", lifespan="1108-1162", titles=["夹漈先生"], works=["通志"], expertise=["史学", "会通"], department="礼部", description="通志作者"),
    SageMeta(name="杨衒之", name_en="yang_xuanzhi", school="史学", tier=SageTier.SCHOLAR, era="北魏", lifespan="?", titles=["洛阳伽蓝记"], works=["洛阳伽蓝记"], expertise=["史学", "佛教"], department="礼部", description="洛阳伽蓝记作者"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 科学 (13人)
# ═══════════════════════════════════════════════════════════════════════════════
SCIENTIST_SAGES_EXTRA: List[SageMeta] = [
    SageMeta(name="伽利略", name_en="galileo", school="科学", tier=SageTier.MASTER, era="近代", lifespan="1564-1642", titles=["科学之父"], works=["两大体系对话"], expertise=["天文", "物理"], department="工部", description="近代科学先驱"),
    SageMeta(name="达尔文", name_en="darwin", school="科学", tier=SageTier.MASTER, era="近代", lifespan="1809-1882", titles=["进化论奠基"], works=["物种起源"], expertise=["生物学", "进化论"], department="工部", description="进化论奠基人"),
    SageMeta(name="牛顿", name_en="newton", school="科学", tier=SageTier.MASTER, era="近代", lifespan="1643-1727", titles=["经典力学之父"], works=["自然哲学数学原理"], expertise=["物理", "数学"], department="工部", description="经典力学奠基人"),
    SageMeta(name="法拉第", name_en="faraday", school="科学", tier=SageTier.MASTER, era="近代", lifespan="1791-1867", titles=["电学之父"], works=["电学实验研究"], expertise=["电磁学", "化学"], department="工部", description="电磁学奠基人"),
    SageMeta(name="拉瓦锡", name_en="lavoisier", school="科学", tier=SageTier.MASTER, era="近代", lifespan="1743-1794", titles=["化学之父"], works=["化学纲要"], expertise=["化学", "质量守恒"], department="工部", description="近代化学奠基人"),
    SageMeta(name="哈维", name_en="harvey", school="科学", tier=SageTier.MASTER, era="近代", lifespan="1578-1657", titles=["血液循环发现者"], works=["心血运动论"], expertise=["医学", "生理学"], department="太医院", description="发现血液循环"),
    SageMeta(name="巴斯德", name_en="pasteur", school="科学", tier=SageTier.MASTER, era="近代", lifespan="1822-1895", titles=["微生物学之父"], works=["发酵研究"], expertise=["微生物", "免疫学"], department="太医院", description="微生物学奠基人"),
    SageMeta(name="林奈", name_en="linnaeus", school="科学", tier=SageTier.MASTER, era="近代", lifespan="1707-1778", titles=["分类学之父"], works=["自然系统"], expertise=["植物学", "分类学"], department="工部", description="生物分类学奠基人"),
    SageMeta(name="门捷列夫", name_en="mendeleev", school="科学", tier=SageTier.MASTER, era="近代", lifespan="1834-1907", titles=["元素周期表之父"], works=["化学原理"], expertise=["化学", "周期律"], department="工部", description="发现元素周期律"),
    SageMeta(name="麦克斯韦", name_en="maxwell", school="科学", tier=SageTier.MASTER, era="近代", lifespan="1831-1879", titles=["电磁理论奠基"], works=["电磁通论"], expertise=["电磁学", "统计物理"], department="工部", description="经典电磁理论奠基人"),
    SageMeta(name="居里夫人", name_en="curie", school="科学", tier=SageTier.MASTER, era="近代", lifespan="1867-1934", titles=["两次诺贝尔奖"], works=["放射性研究"], expertise=["物理", "化学"], department="工部", description="放射性研究先驱"),
    SageMeta(name="李冰", name_en="li_bing", school="科学", tier=SageTier.SCHOLAR, era="战国", lifespan="?", titles=["都江堰创建者"], works=[], expertise=["水利", "工程"], department="工部", description="都江堰创建者"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 西方哲学 (6人)
# ═══════════════════════════════════════════════════════════════════════════════
WESTERN_PHILOSOPHY_SAGES: List[SageMeta] = [
    SageMeta(name="休谟", name_en="hume", school="西方哲学", tier=SageTier.MASTER, era="近代", lifespan="1711-1776", titles=["经验主义", "怀疑论"], works=["人性论"], expertise=["认识论", "伦理学"], department="礼部", description="英国经验主义哲学家"),
    SageMeta(name="笛卡尔", name_en="descartes", school="西方哲学", tier=SageTier.MASTER, era="近代", lifespan="1596-1650", titles=["现代哲学之父"], works=["第一哲学沉思集"], expertise=["认识论", "形而上学"], department="礼部", description="我思故我在"),
    SageMeta(name="黑格尔", name_en="hegel", school="西方哲学", tier=SageTier.MASTER, era="近代", lifespan="1770-1831", titles=["辩证法大师"], works=["精神现象学"], expertise=["辩证法", "绝对精神"], department="礼部", description="德国古典哲学大师"),
    SageMeta(name="叔本华", name_en="schopenhauer", school="西方哲学", tier=SageTier.MASTER, era="近代", lifespan="1788-1860", titles=["悲观主义哲学"], works=["意志与表象"], expertise=["意志哲学", "人生观"], department="礼部", description="悲观主义哲学"),
    SageMeta(name="加缪", name_en="camus", school="西方哲学", tier=SageTier.MASTER, era="近代", lifespan="1913-1960", titles=["荒诞哲学"], works=["局外人"], expertise=["荒诞哲学", "存在主义"], department="礼部", description="荒诞哲学代表"),
    SageMeta(name="萨特", name_en="sartre", school="西方哲学", tier=SageTier.MASTER, era="近代", lifespan="1905-1980", titles=["存在主义"], works=["存在与虚无"], expertise=["存在主义", "自由"], department="礼部", description="存在主义哲学家"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 管理学 (3人)
# ═══════════════════════════════════════════════════════════════════════════════
MANAGEMENT_SAGES: List[SageMeta] = [
    SageMeta(name="德鲁克", name_en="drucker", school="管理学", tier=SageTier.MASTER, era="近现代", lifespan="1909-2005", titles=["现代管理学之父"], works=["管理的实践"], expertise=["管理学", "战略"], department="户部", description="现代管理学奠基人"),
    SageMeta(name="波特", name_en="porter", school="管理学", tier=SageTier.MASTER, era="近现代", lifespan="1947-", titles=["竞争战略之父"], works=["竞争战略"], expertise=["战略管理", "竞争优势"], department="户部", description="竞争战略理论"),
    SageMeta(name="亚当斯密", name_en="adam_smith", school="管理学", tier=SageTier.MASTER, era="近代", lifespan="1723-1790", titles=["经济学之父"], works=["国富论"], expertise=["经济学", "古典自由主义"], department="户部", description="经济学之父"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 医学 (1人)
# ═══════════════════════════════════════════════════════════════════════════════
MEDICAL_SAGES_EXTRA: List[SageMeta] = [
    SageMeta(name="朱震亨", name_en="zhu_zhenheng", school="医学", tier=SageTier.MASTER, era="元代", lifespan="1281-1358", titles=["滋阴派创始人"], works=["丹溪心法"], expertise=["滋阴", "清热"], department="太医院", description="金元四大家之一，滋阴派"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 政治/军事 (10人)
# ═══════════════════════════════════════════════════════════════════════════════
POLITICAL_SAGES_EXTRA: List[SageMeta] = [
    SageMeta(name="张三丰", name_en="zhang_sanfeng", school="道教/武术", tier=SageTier.MASTER, era="明代", lifespan="?", titles=["太极拳创始人"], works=[], expertise=["道教", "武术"], department="兵部", description="太极拳创始人"),
    SageMeta(name="张骞", name_en="zhang_qian", school="政治", tier=SageTier.SCHOLAR, era="西汉", lifespan="?-前114", titles=["丝路开拓者"], works=[], expertise=["外交", "丝路"], department="礼部", description="丝绸之路开拓者"),
    SageMeta(name="郑和", name_en="zheng_he", school="政治", tier=SageTier.SCHOLAR, era="明代", lifespan="1371-1433", titles=["三宝太监"], works=[], expertise=["航海", "外交"], department="礼部", description="郑和下西洋"),
    SageMeta(name="郑成功", name_en="zheng_chenggong", school="政治", tier=SageTier.SCHOLAR, era="明代", lifespan="1624-1662", titles=["延平王"], works=[], expertise=["军事", "复明"], department="兵部", description="收复台湾"),
    SageMeta(name="岳飞", name_en="yue_fei", school="政治", tier=SageTier.SCHOLAR, era="宋代", lifespan="1103-1142", titles=["民族英雄"], works=["满江红"], expertise=["军事", "忠义"], department="兵部", description="精忠报国"),
    SageMeta(name="戚继光", name_en="qi_jiguang", school="政治", tier=SageTier.SCHOLAR, era="明代", lifespan="1528-1588", titles=["抗倭名将"], works=["纪效新书"], expertise=["军事", "阵法"], department="兵部", description="戚家军创建者"),
    SageMeta(name="刘伯温", name_en="liu_bowen", school="政治", tier=SageTier.MASTER, era="明代", lifespan="1311-1375", titles=["诚意伯"], works=["诚意伯文集"], expertise=["谋略", "政治"], department="吏部", description="辅佐朱元璋"),
    SageMeta(name="魏徵", name_en="wei_zheng_statesman", school="政治", tier=SageTier.SCHOLAR, era="唐代", lifespan="580-643", titles=["名相"], works=[], expertise=["谏诤", "治国"], department="吏部", description="贞观名臣"),
    SageMeta(name="魏源", name_en="wei_yuan", school="政治", tier=SageTier.SCHOLAR, era="清代", lifespan="1794-1857", titles=["睁眼看世界"], works=["海国图志"], expertise=["经世致用", "睁眼看世界"], department="礼部", description="海国图志作者"),
    SageMeta(name="王应麟", name_en="wang_yinglin", school="政治", tier=SageTier.SCHOLAR, era="宋代", lifespan="1223-1287", titles=["学者"], works=["三字经"], expertise=["经学", "史学"], department="礼部", description="三字经作者"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 儒家/经学 (21人)
# ═══════════════════════════════════════════════════════════════════════════════
RU_SAGES_EXTRA: List[SageMeta] = [
    SageMeta(name="刘宗周", name_en="liu_zongzhou", school="儒家", tier=SageTier.MASTER, era="明代", lifespan="1578-1645", titles=["蕺山先生"], works=["刘子全书"], expertise=["理学", "慎独"], department="礼部", description="蕺山学派创始人"),
    SageMeta(name="刘峻", name_en="liu_jun", school="儒家", tier=SageTier.SCHOLAR, era="南北朝", lifespan="462-521", titles=["学者"], works=["广绝交论"], expertise=["儒学"], department="礼部", description="南朝儒学家"),
    SageMeta(name="王珪", name_en="wang_gui", school="儒家", tier=SageTier.SCHOLAR, era="唐代", lifespan="571-639", titles=["名相"], works=[], expertise=["政治"], department="吏部", description="唐代名相"),
    SageMeta(name="裴度", name_en="pei_du", school="儒家", tier=SageTier.SCHOLAR, era="唐代", lifespan="765-839", titles=["名相"], works=[], expertise=["政治"], department="吏部", description="唐代名相"),
    SageMeta(name="裴秀", name_en="pei_xiu", school="儒家", tier=SageTier.SCHOLAR, era="魏晋", lifespan="223-271", titles=["地图学家"], works=["禹贡地域图"], expertise=["地理", "绘图"], department="工部", description="中国地图学之父"),
    SageMeta(name="裴頠", name_en="pei_wei", school="儒家", tier=SageTier.SCHOLAR, era="魏晋", lifespan="267-300", titles=["哲学家"], works=["崇有论"], expertise=["哲学"], department="礼部", description="崇有论作者"),
    SageMeta(name="裴骃", name_en="pei_yin", school="儒家", tier=SageTier.SCHOLAR, era="南朝", lifespan="?", titles=["史学家"], works=["史记集解"], expertise=["史学"], department="礼部", description="史记注家"),
    SageMeta(name="褚遂良", name_en="chu_suiliang", school="儒家", tier=SageTier.SCHOLAR, era="唐代", lifespan="596-658", titles=["书法家"], works=[], expertise=["书法", "政治"], department="礼部", description="初唐书法家"),
    SageMeta(name="申培", name_en="shen_pei", school="儒家", tier=SageTier.SCHOLAR, era="西汉", lifespan="?", titles=["诗经学家"], works=["鲁诗"], expertise=["诗经"], department="礼部", description="鲁诗学派"),
    SageMeta(name="真德秀", name_en="zhen_dexiu", school="儒家", tier=SageTier.MASTER, era="宋代", lifespan="1178-1235", titles=["西山先生"], works=["大学衍义"], expertise=["理学", "心学"], department="礼部", description="理学名臣"),
    SageMeta(name="公羊高", name_en="gongyang_gao", school="儒家", tier=SageTier.FOUNDER, era="战国", lifespan="?", titles=["公羊传"], works=["公羊传"], expertise=["春秋学"], department="礼部", description="公羊学创始人"),
    SageMeta(name="谷梁赤", name_en="guliang_chi", school="儒家", tier=SageTier.FOUNDER, era="战国", lifespan="?", titles=["谷梁传"], works=["谷梁传"], expertise=["春秋学"], department="礼部", description="谷梁学创始人"),
    SageMeta(name="孔颖达", name_en="kong_yingda", school="儒家", tier=SageTier.SCHOLAR, era="唐代", lifespan="574-648", titles=["经学家"], works=["五经正义"], expertise=["经学", "注疏"], department="礼部", description="五经正义主编"),
    SageMeta(name="颜之推", name_en="yan_zhitui", school="儒家", tier=SageTier.SCHOLAR, era="南北朝", lifespan="531-591", titles=["颜氏家训"], works=["颜氏家训"], expertise=["儒学", "家庭教育"], department="礼部", description="颜氏家训作者"),
    SageMeta(name="颜师古", name_en="yan_shigu", school="儒家", tier=SageTier.SCHOLAR, era="唐代", lifespan="581-645", titles=["经学家"], works=["汉书注"], expertise=["经学", "注疏"], department="礼部", description="汉书注家"),
    SageMeta(name="黄震", name_en="huang_zhen", school="儒家", tier=SageTier.SCHOLAR, era="宋代", lifespan="1213-1280", titles=["学者"], works=["黄氏日抄"], expertise=["理学"], department="礼部", description="宋代学者"),
    SageMeta(name="陈亮", name_en="chen_liang", school="儒家", tier=SageTier.MASTER, era="宋代", lifespan="1143-1194", titles=["永康学派"], works=["龙川文集"], expertise=["事功学"], department="礼部", description="永康学派创始人"),
    SageMeta(name="叶适", name_en="ye_shi", school="儒家", tier=SageTier.MASTER, era="宋代", lifespan="1150-1223", titles=["永嘉学派"], works=["水心文集"], expertise=["事功学"], department="礼部", description="永嘉学派创始人"),
    SageMeta(name="桓温", name_en="huan_wen", school="政治", tier=SageTier.SCHOLAR, era="东晋", lifespan="312-373", titles=["权臣"], works=[], expertise=["政治", "军事"], department="兵部", description="东晋权臣"),
    SageMeta(name="谢玄", name_en="xie_xuan", school="政治", tier=SageTier.SCHOLAR, era="东晋", lifespan="343-388", titles=["将才"], works=[], expertise=["军事"], department="兵部", description="淝水之战主将"),
    SageMeta(name="崔浩", name_en="cui_hao", school="政治", tier=SageTier.SCHOLAR, era="北魏", lifespan="?-450", titles=["谋士"], works=[], expertise=["政治"], department="吏部", description="北魏谋士"),
    SageMeta(name="范缜", name_en="fan_zhen", school="儒家", tier=SageTier.SCHOLAR, era="南北朝", lifespan="约450-约510", titles=["无神论者"], works=["神灭论"], expertise=["无神论"], department="礼部", description="神灭论作者"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 英国哲学 (1人)
# ═══════════════════════════════════════════════════════════════════════════════
PHILOSOPHY_SAGES_EXTRA: List[SageMeta] = [
    SageMeta(name="培根", name_en="bacon", school="英国哲学", tier=SageTier.MASTER, era="近代", lifespan="1561-1626", titles=["经验主义之父"], works=["新工具"], expertise=["经验主义", "归纳法"], department="礼部", description="英国经验主义哲学之父"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 虚拟/集合人物 - 2026-04-22 新增 (11人)
# ═══════════════════════════════════════════════════════════════════════════════
VIRTUAL_SAGES: List[SageMeta] = [
    SageMeta(name="明1-心理", name_en="ming1_xinli", school="心理学", tier=SageTier.SCHOLAR, era="当代", lifespan="虚拟", titles=["心理学集合"], works=[], expertise=["心理分析", "行为观察", "认知行为"], department="礼部", description="心理学知识集合虚拟人物"),
    SageMeta(name="明2-宇宙", name_en="ming2_yuzhou", school="科学", tier=SageTier.SCHOLAR, era="当代", lifespan="虚拟", titles=["宇宙科学集合"], works=[], expertise=["宇宙观测", "理论建模", "量子探索"], department="皇家科学院", description="宇宙科学知识集合虚拟人物"),
    SageMeta(name="明3-诗词", name_en="ming3_shici", school="文学", tier=SageTier.SCHOLAR, era="古代", lifespan="虚拟", titles=["诗词集合"], works=[], expertise=["意象分析", "情感解读", "韵律研究"], department="礼部", description="诗词文学知识集合虚拟人物"),
    SageMeta(name="明4-科哲", name_en="ming4_kezhe", school="科学", tier=SageTier.SCHOLAR, era="当代", lifespan="虚拟", titles=["科学哲学集合"], works=[], expertise=["数学建模", "逻辑分析", "假设验证"], department="皇家科学院", description="科学哲学知识集合虚拟人物"),
    SageMeta(name="明5-现当代", name_en="ming5_xiandangdai", school="文学", tier=SageTier.SCHOLAR, era="当代", lifespan="虚拟", titles=["现当代文学集合"], works=[], expertise=["魔幻现实主义", "乡土叙事", "历史书写"], department="礼部", description="现当代文学知识集合虚拟人物"),
    SageMeta(name="明6-乡土", name_en="ming6_xiangtu", school="文学", tier=SageTier.SCHOLAR, era="当代", lifespan="虚拟", titles=["乡土文学集合"], works=[], expertise=["现实主义", "苦难叙事", "奋斗精神"], department="礼部", description="乡土文学知识集合虚拟人物"),
    SageMeta(name="明7-医家", name_en="ming7_yijia", school="医学", tier=SageTier.SCHOLAR, era="古代", lifespan="虚拟", titles=["中医集合"], works=[], expertise=["阴阳五行", "辨证论治", "整体观念"], department="工部", description="中医传统知识集合虚拟人物"),
    SageMeta(name="明8-诗经", name_en="ming8_shijing", school="文学", tier=SageTier.SCHOLAR, era="春秋", lifespan="虚拟", titles=["诗经集合"], works=["诗经"], expertise=["赋比兴", "风雅颂", "诗教传统"], department="礼部", description="诗经知识集合虚拟人物"),
    SageMeta(name="明9-论衡", name_en="ming9_lunheng", school="哲学", tier=SageTier.SCHOLAR, era="东汉", lifespan="虚拟", titles=["论衡集合"], works=["论衡"], expertise=["唯物主义", "批判精神", "实证方法"], department="礼部", description="论衡思想集合虚拟人物"),
    SageMeta(name="明10-论语", name_en="ming10_lunyu", school="哲学", tier=SageTier.SCHOLAR, era="春秋", lifespan="虚拟", titles=["论语集合"], works=["论语"], expertise=["仁学", "礼治", "教育"], department="礼部", description="论语思想集合虚拟人物"),
    SageMeta(name="明11-家训", name_en="ming11_jiaxun", school="哲学", tier=SageTier.SCHOLAR, era="南北朝", lifespan="虚拟", titles=["家训集合"], works=["颜氏家训"], expertise=["家庭教育", "读书明理", "修身养性"], department="礼部", description="家训文化集合虚拟人物"),
    # ---- 2026-04-22 补充真实人物 ----
    SageMeta(name="李嘉图", name_en="li_jiatu", school="经济", tier=SageTier.MASTER, era="18世纪", lifespan="1772-1823", titles=["古典经济学大师"], works=["政治经济学及赋税原理"], expertise=["比较优势", "地租理论", "自由贸易"], department="户部", description="古典经济学重要代表人物"),
    SageMeta(name="李贽", name_en="li_zhi", school="儒家", tier=SageTier.MASTER, era="明代", lifespan="1527-1602", titles=["异端之尤", "思想解放先驱"], works=["焚书", "藏书"], expertise=["童心说", "独立思考", "人性解放"], department="礼部", description="明代思想解放先驱，以童心说著称"),
    SageMeta(name="马克斯·韦伯", name_en="max_weber", school="管理", tier=SageTier.GRANDMASTER, era="现代", lifespan="1864-1920", titles=["社会学之父"], works=["新教伦理与资本主义精神", "经济与社会"], expertise=["科层制", "理性化", "合法性权威"], department="工部", description="现代社会学与管理学奠基人"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# 合并所有补充人物
# ═══════════════════════════════════════════════════════════════════════════════
EXTRA_SAGES = {
    "兵家": MILITARY_SAGES_EXTRA,
    "文学": LITERARY_SAGES_EXTRA,
    "史学": HISTORIAN_SAGES_EXTRA,
    "科学": SCIENTIST_SAGES_EXTRA,
    "西方哲学": WESTERN_PHILOSOPHY_SAGES,
    "管理学": MANAGEMENT_SAGES,
    "医学": MEDICAL_SAGES_EXTRA,
    "政治": POLITICAL_SAGES_EXTRA,
    "儒家": RU_SAGES_EXTRA,
    "英国哲学": PHILOSOPHY_SAGES_EXTRA,
    "虚拟人物": VIRTUAL_SAGES,
}

def get_all_extra_sages() -> List[SageMeta]:
    """获取所有补充人物"""
    result = []
    for sages in EXTRA_SAGES.values():
        result.extend(sages)
    return result

def get_extra_sages_by_school(school: str) -> List[SageMeta]:
    """根据学派获取补充人物"""
    return EXTRA_SAGES.get(school, [])
