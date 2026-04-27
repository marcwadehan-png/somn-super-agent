# -*- coding: utf-8 -*-
"""
智慧记忆数据模块 v1.0.0
懒加载数据模块，包含经典语录和智慧图谱

来源: wisdom_memory_enhancer.py
- 语录数据库: 12个分类，约60条语录
- 智慧图谱: 7个节点
"""

from typing import Dict, List

# 缓存
_quotes_cache: Dict = None
_graph_cache: Dict = None

def _dict_to_quote(data: Dict) -> 'WisdomQuote':
    """将字典转换为WisdomQuote"""
    from .wisdom_memory_enhancer import WisdomQuote, WisdomCategory
    cat = data["category"]
    if isinstance(cat, str):
        cat = WisdomCategory[cat]
    return WisdomQuote(
        text=data["text"],
        source=data["source"],
        category=cat,
        meaning=data["meaning"],
        application=data.get("application", ""),
        keywords=data.get("keywords", [])
    )

def get_quotes_data() -> Dict:
    """获取语录数据（懒加载）"""
    global _quotes_cache
    if _quotes_cache is not None:
        return _quotes_cache
    
    _quotes_cache = {
        "论语": [
            {"text": "仁者爱人,己所不欲勿施于人", "source": "论语·颜渊", "category": "REN", "meaning": "仁爱的人爱护他人,自己不想要的不要强加给别人", "application": "处理人际关系时的黄金法则", "keywords": ["仁爱", "同理心", "人际"]},
            {"text": "君子喻于义,小人喻于利", "source": "论语·里仁", "category": "YI", "meaning": "君子懂得道义,小人只顾私利", "application": "价值观抉择时的judge标准", "keywords": ["义利", "君子", "价值观"]},
            {"text": "礼之用,和为贵", "source": "论语·学而", "category": "LI", "meaning": "礼的作用,以和谐为贵", "application": "团队协作与社会交往", "keywords": ["和谐", "礼", "秩序"]},
            {"text": "知之为知之,不知为不知", "source": "论语·为政", "category": "ZHI", "meaning": "知道就是知道,不知道就是不知道", "application": "求知态度与诚信", "keywords": ["求知", "诚实", "智慧"]},
            {"text": "人无信不立", "source": "论语·颜渊", "category": "XIN", "meaning": "一个人没有信用就无法立足", "application": "商业诚信与人际信任", "keywords": ["信用", "信任", "立身"]},
            {"text": "学而时习之,不亦说乎", "source": "论语·学而", "category": "GROWTH", "meaning": "学习并时常温习,不也是很快乐吗", "application": "终身学习与知识巩固", "keywords": ["学习", "温习", "成长"]},
            {"text": "三人行必有我师", "source": "论语·述而", "category": "ZHI", "meaning": "三人同行,其中必有我的老师", "application": "虚xinxue习与人才发现", "keywords": ["学习", "谦逊", "人才"]},
            {"text": "己欲立而立人,己欲达而达人", "source": "论语·雍也", "category": "REN", "meaning": "自己想立足也帮助别人立足,自己想发达也帮助别人发达", "application": "利他领导力", "keywords": ["利他", "领导", "仁爱"]},
            {"text": "君子求诸己,小人求诸人", "source": "论语·卫灵公", "category": "DE", "meaning": "君子严于律己,小人苛求他人", "application": "自我反省与责任担当", "keywords": ["自律", "反省", "责任"]},
            {"text": "君子和而不同,小人同而不和", "source": "论语·子路", "category": "LI", "meaning": "君子和谐但不盲从,小人盲从但不和谐", "application": "团队建设与意见整合", "keywords": ["和谐", "独立", "团队"]},
        ],
        "孟子": [
            {"text": "民为贵,社稷次之,君为轻", "source": "孟子·尽心下", "category": "REN", "meaning": "人民最重要,国家其次,君主最轻", "application": "以用户/客户为中心的经营哲学", "keywords": ["民本", "用户中心", "价值观"]},
            {"text": "舍生取义", "source": "孟子·告子上", "category": "YI", "meaning": "舍弃生命也要追求道义", "application": "重大抉择时的价值judge", "keywords": ["义", "牺牲", "原则"]},
            {"text": "生于忧患,死于安乐", "source": "孟子·告天下", "category": "GROWTH", "meaning": "在忧患中成长,在安乐中灭亡", "application": "危机意识与持续奋斗", "keywords": ["忧患", "危机", "成长"]},
            {"text": "天将降大任于斯人也", "source": "孟子·告天下", "category": "DE", "meaning": "上天要把重大任务交给这个人", "application": "面对困难时的积极心态", "keywords": ["使命", "担当", "成长"]},
            {"text": "恻隐之心,人皆有之", "source": "孟子·告子上", "category": "REN", "meaning": "同情之心人人都有", "application": "团队同理心建设", "keywords": ["同理心", "仁爱", "领导"]},
        ],
        "大学": [
            {"text": "大学之道,在明明德", "source": "大学·经一章", "category": "DE", "meaning": "大学的宗旨在于弘扬光明正大的品德", "application": "企业使命与价值观建设", "keywords": ["明德", "使命", "价值观"]},
            {"text": "苟日新,日日新,又日新", "source": "大学·盘铭", "category": "GROWTH", "meaning": "如果能够一天新,就应保持天天新", "application": "持续创新与自我迭代", "keywords": ["创新", "迭代", "进步"]},
            {"text": "格物致知", "source": "大学·经一章", "category": "ZHI", "meaning": "穷究事物之理,获得知识", "application": "深度学习与洞察分析", "keywords": ["学习", "洞察", "智慧"]},
            {"text": "修身齐家治国平天下", "source": "大学·经一章", "category": "LI", "meaning": "修养自身,管理家庭,治理国家,平定天下", "application": "组织发展的阶段目标", "keywords": ["修身", "治理", "格局"]},
        ],
        "中庸": [
            {"text": "不偏之谓中,不易之谓庸", "source": "中庸·第一章", "category": "LI", "meaning": "不偏不倚叫做中,永恒不变叫做庸", "application": "平衡decision与稳健经营", "keywords": ["平衡", "中庸", "稳健"]},
            {"text": "致中和,天地位焉", "source": "中庸·第一章", "category": "LI", "meaning": "达到中和的境界,天地各就其位", "application": "组织和谐与生态平衡", "keywords": ["和谐", "平衡", "生态"]},
            {"text": "诚者,天之道也", "source": "中庸·第二十章", "category": "XIN", "meaning": "真诚是上天的法则", "application": "真诚经营与品牌诚信", "keywords": ["真诚", "诚信", "天道"]},
        ],
        "尚书": [
            {"text": "德惟善政,政在养民", "source": "尚书·大禹谟", "category": "DE", "meaning": "德行体现为好的政治,政治在于养育人民", "application": "德治管理与用户价值", "keywords": ["德治", "管理", "价值"]},
            {"text": "任贤勿贰", "source": "尚书·大禹谟", "category": "ZHI", "meaning": "任用贤才不要三心二意", "application": "人才战略与管理", "keywords": ["人才", "任贤", "管理"]},
            {"text": "人心惟危,道心惟微", "source": "尚书·大禹谟", "category": "ZHI", "meaning": "人心是危险的,道心是微妙的", "application": "洞察人心与把握规律", "keywords": ["洞察", "规律", "人心"]},
        ],
        "诗经": [
            {"text": "他山之石,可以攻玉", "source": "诗经·小雅·鹤鸣", "category": "ZHI", "meaning": "别的山上的石头,可以用来雕琢玉器", "application": "借鉴他人提升自己", "keywords": ["借鉴", "学习", "成长"]},
            {"text": "靡不有初,鲜克有终", "source": "诗经·大雅·荡", "category": "LOOP", "meaning": "事情都有开始,但很少能善终", "application": "闭环执行与持续坚持", "keywords": ["坚持", "闭环", "执行"]},
        ],
        "易经": [
            {"text": "天行健,君子以自强不息", "source": "易经·乾卦", "category": "GROWTH", "meaning": "天道刚健,君子应效法天永不停息", "application": "持续奋斗与自我提升", "keywords": ["自强", "奋斗", "成长"]},
            {"text": "地势坤,君子以厚德载物", "source": "易经·坤卦", "category": "DE", "meaning": "地势柔顺,君子应增厚美德承载万物", "application": "德行修养与包容领导", "keywords": ["厚德", "包容", "领导"]},
            {"text": "穷则变,变则通", "source": "易经·系辞", "category": "ZHI", "meaning": "穷尽时就会变化,变化了就能通达", "application": "转型变革与创新突破", "keywords": ["变革", "创新", "突破"]},
            {"text": "物极必反", "source": "易经·易传", "category": "ZHI", "meaning": "事物发展到极点必然反向发展", "application": "周期预判与风险防范", "keywords": ["周期", "风险", "预判"]},
            {"text": "亢龙有悔", "source": "易经·乾卦", "category": "YI", "meaning": "龙飞得太高会有悔恨", "application": "成功时的谦逊与审慎", "keywords": ["谦逊", "审慎", "风险"]},
        ],
        "道德经": [
            {"text": "道可道,非常道", "source": "道德经·第一章", "category": "DAO", "meaning": "道如果可以言说,就不是永恒的道", "application": "对规律的认识与敬畏", "keywords": ["道", "规律", "智慧"]},
            {"text": "上善若水", "source": "道德经·第八章", "category": "REN", "meaning": "最高的善就像水一样", "application": "柔性领导力", "keywords": ["善", "柔性", "领导"]},
            {"text": "无为而无不为", "source": "道德经·第三章", "category": "WUWEI", "meaning": "不妄为就没有做不成的事", "application": "战略定力与有所为有所不为", "keywords": ["无为", "战略", "定力"]},
            {"text": "柔弱胜刚强", "source": "道德经·第三十六章", "category": "ZHI", "meaning": "柔弱能够战胜刚强", "application": "以柔克刚的竞争strategy", "keywords": ["柔弱", "竞争", "strategy"]},
            {"text": "知足者富", "source": "道德经·第三十三章", "category": "DAO", "meaning": "知道满足的人是富有的", "application": "欲望管理与价值创造", "keywords": ["知足", "价值", "富足"]},
            {"text": "为而不争", "source": "道德经·第八十一章", "category": "YI", "meaning": "有所作为但不与人争", "application": "利他商业与社会价值", "keywords": ["不争", "利他", "价值"]},
            {"text": "致虚极,守静笃", "source": "道德经·第十六章", "category": "DAO", "meaning": "达到虚无的极点,坚守清静的极致", "application": "decision前的静心与深思", "keywords": ["静心", "深思", "decision"]},
        ],
        "素书": [
            {"text": "道者,人之所蹈", "source": "素书·原始章", "category": "DAO", "meaning": "道,是人们应当遵循的", "application": "战略规划与规律遵循", "keywords": ["道", "规律", "战略"]},
            {"text": "德者,人之所失", "source": "素书·原始章", "category": "DE", "meaning": "德,是人们应当培养的", "application": "品德修养与领导魅力", "keywords": ["德", "修养", "领导"]},
            {"text": "仁者,人之所亲", "source": "素书·原始章", "category": "REN_SUFU", "meaning": "仁爱,是人们应当亲近的", "application": "仁爱管理与团队凝聚", "keywords": ["仁", "团队", "凝聚"]},
            {"text": "义者,人之所宜", "source": "素书·原始章", "category": "YI_SUFU", "meaning": "适宜,是人们应当做的", "application": "合理decision与恰当action", "keywords": ["义", "decision", "action"]},
            {"text": "礼者,人之所履", "source": "素书·原始章", "category": "LI_SUFU", "meaning": "礼法,是人们应当履行的", "application": "制度建设与流程规范", "keywords": ["礼", "制度", "规范"]},
            {"text": "俊者,人之所羡", "source": "素书·正道章", "category": "ZHI", "meaning": "俊杰,是人们所羡慕的", "application": "人才recognize与培养", "keywords": ["人才", "俊杰", "培养"]},
            {"text": "豪者,人之所畏", "source": "素书·正道章", "category": "ZHI", "meaning": "豪杰,是人们所敬畏的", "application": "领导力与影响力", "keywords": ["领导", "影响", "敬畏"]},
            {"text": "吉莫吉于知足", "source": "素书·安礼章", "category": "DAO", "meaning": "最大的吉利就是知道满足", "application": "欲望管理与幸福指数", "keywords": ["知足", "幸福", "管理"]},
        ],
        "孙子兵法": [
            {"text": "知己知彼,百战不殆", "source": "孙子兵法·谋攻篇", "category": "ZHI", "meaning": "了解自己也了解敌人,百战都不会有危险", "application": "竞争分析与战略制定", "keywords": ["知己知彼", "竞争", "战略"]},
            {"text": "不战而屈人之兵", "source": "孙子兵法·谋攻篇", "category": "ZHENG", "meaning": "不用战争就能使敌人屈服", "application": "非对抗性竞争与合作博弈", "keywords": ["不战", "合作", "博弈"]},
            {"text": "上兵伐谋", "source": "孙子兵法·谋攻篇", "category": "QI", "meaning": "最高级的战争是挫败敌人的谋略", "application": "战略智慧与顶层设计", "keywords": ["伐谋", "战略", "顶层"]},
            {"text": "兵者,诡道也", "source": "孙子兵法·始计篇", "category": "QI", "meaning": "用兵是诡诈之道", "application": "灵活strategy与出奇制胜", "keywords": ["诡道", "灵活", "奇正"]},
            {"text": "致人而不致于人", "source": "孙子兵法·虚实篇", "category": "ZHENG", "meaning": "调动敌人而不被敌人调动", "application": "主动权掌控与市场主导", "keywords": ["主动权", "主导", "掌控"]},
            {"text": "兵贵胜,不贵久", "source": "孙子兵法·作战篇", "category": "ZHI", "meaning": "用兵贵在速胜,不在持久", "application": "快速迭代与敏捷响应", "keywords": ["速胜", "敏捷", "迭代"]},
        ],
        "吕氏春秋": [
            {"text": "贵公去私", "source": "吕氏春秋·贵公", "category": "DE", "meaning": "贵在公正,去除私心", "application": "公正管理与团队信任", "keywords": ["公正", "无私", "管理"]},
            {"text": "公则天下平", "source": "吕氏春秋·贵公", "category": "LI", "meaning": "公正就能使天下太平", "application": "公平制度与透明运营", "keywords": ["公平", "透明", "制度"]},
            {"text": "阴阳调和", "source": "吕氏春秋·任理", "category": "DAO", "meaning": "阴阳相互调和", "application": "平衡管理与生态和谐", "keywords": ["阴阳", "平衡", "和谐"]},
        ],
        "成长思维": [
            {"text": "能力可以培养", "source": "卡罗尔·德韦克<终身成长>", "category": "GROWTH", "meaning": "智力和能力不是固定的,而是可以发展的", "application": "人才培养与自我突破", "keywords": ["能力", "培养", "突破"]},
            {"text": "失败是成长的机会", "source": "卡罗尔·德韦克<终身成长>", "category": "GROWTH", "meaning": "失败不是终点,而是学习的机会", "application": "错误管理与持续改进", "keywords": ["失败", "学习", "改进"]},
            {"text": "拥抱挑战", "source": "卡罗尔·德韦克<终身成长>", "category": "GROWTH", "meaning": "挑战是发展的契机", "application": "勇于尝试与突破舒适区", "keywords": ["挑战", "舒适区", "突破"]},
            {"text": "过程比结果重要", "source": "卡罗尔·德韦克<终身成长>", "category": "LOOP", "meaning": "关注学习过程而非仅仅是成绩", "application": "过程管理与持续迭代", "keywords": ["过程", "迭代", "管理"]},
        ],
    }
    return _quotes_cache

def get_wisdom_graph_data() -> Dict:
    """获取智慧图谱数据（懒加载）"""
    global _graph_cache
    if _graph_cache is not None:
        return _graph_cache
    
    from .wisdom_memory_enhancer import WisdomCategory
    
    _graph_cache = {
        WisdomCategory.REN: [
            WisdomCategory.REN_SUFU, WisdomCategory.KONG, WisdomCategory.ZIRAN
        ],
        WisdomCategory.YI: [
            WisdomCategory.YI_SUFU, WisdomCategory.QI, WisdomCategory.ZHENG
        ],
        WisdomCategory.LI: [
            WisdomCategory.LI_SUFU, WisdomCategory.DAO, WisdomCategory.LOOP
        ],
        WisdomCategory.ZHI: [
            WisdomCategory.HUI, WisdomCategory.DAO, WisdomCategory.GROWTH
        ],
        WisdomCategory.XIN: [
            WisdomCategory.DE, WisdomCategory.ZIRAN
        ],
        WisdomCategory.GROWTH: [
            WisdomCategory.GROWTH, WisdomCategory.LOOP, WisdomCategory.ZHI
        ],
        WisdomCategory.LOOP: [
            WisdomCategory.LI, WisdomCategory.LI_SUFU, WisdomCategory.GROWTH
        ],
    }
    return _graph_cache
