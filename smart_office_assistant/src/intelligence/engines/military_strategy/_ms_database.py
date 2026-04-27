"""
__all__ = [
    'get_by_category',
    'get_by_name',
]

计谋数据库 - 包含36计的所有策略定义
"""

from typing import Dict, List, Optional
from ._ms_enums import StrategyCategory, StrategyType
from ._ms_dataclasses import StrategyInfo

class StrategyDatabase:
    """计谋数据库"""
    
    def __init__(self):
        self.strategies: Dict[str, StrategyInfo] = {}
        self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        # 胜战计
        self._add_victory_strategies()
        # 敌战计
        self._add_confrontation_strategies()
        # 攻战计
        self._add_attack_strategies()
        # 混战计
        self._add_chaos_strategies()
        # 并战计
        self._add_merge_strategies()
        # 败战计
        self._add_retreat_strategies()
    
    def _add_victory_strategies(self):
        """添加胜战计"""
        self.strategies['瞒天过海'] = StrategyInfo(
            name='瞒天过海',
            category=StrategyCategory.VICTORY,
            original_text='备周则意怠，常见则不疑。阴在阳之内，不在阳之对。太阳，太阴。',
            explanation='在敌人防备周密时，其注意力会松懈；常见的事物不会引起怀疑。秘密往往隐藏在公开的事物中，而不是与公开事物对立。',
            principles=['示假隐真', '出其不意', '利用惯性思维'],
            applications=['商业竞争', '谈判策略', '危机处理'],
            historical_cases=['薛仁贵征辽']
        )
        
        self.strategies['围魏救赵'] = StrategyInfo(
            name='围魏救赵',
            category=StrategyCategory.VICTORY,
            original_text='共敌不如分敌，敌阳不如敌阴。',
            explanation='与其攻击集中的敌人，不如分散其力量；与其正面攻击，不如从侧面或后方攻击。',
            principles=['攻其所必救', '分散敌人', '间接路线'],
            applications=['商业竞争', '资源调配', '战略转移'],
            historical_cases=['孙膑救赵']
        )
        
        self.strategies['借刀杀人'] = StrategyInfo(
            name='借刀杀人',
            category=StrategyCategory.VICTORY,
            original_text='敌已明，友未定，引友杀敌，不自出力。',
            explanation='敌人已经明确，但盟友尚未确定，这时应引导盟友去消灭敌人，自己不必出力。',
            principles=['借力打力', '保存实力', '转移矛盾'],
            applications=['商业联盟', '资源整合', '竞争策略'],
            historical_cases=['曹操借刀杀吕布']
        )
        
        self.strategies['以逸待劳'] = StrategyInfo(
            name='以逸待劳',
            category=StrategyCategory.VICTORY,
            original_text='困敌之势，不以战；损刚益柔。',
            explanation='使敌人陷入困境，不一定要直接交战；以柔克刚，消耗敌人锐气。',
            principles=['以静制动', '消耗敌人', '掌握主动'],
            applications=['持久战', '防守策略', '资源管理'],
            historical_cases=['陆逊破刘备']
        )
        
        self.strategies['趁火打劫'] = StrategyInfo(
            name='趁火打劫',
            category=StrategyCategory.VICTORY,
            original_text='敌之害大，就势取利，刚决柔也。',
            explanation='敌人遭遇大灾难时，乘机取利，以刚克柔。',
            principles=['把握时机', '乘人之危', '快速行动'],
            applications=['危机收购', '市场机会', '竞争策略'],
            historical_cases=['勾践灭吴']
        )
        
        self.strategies['声东击西'] = StrategyInfo(
            name='声东击西',
            category=StrategyCategory.VICTORY,
            original_text='敌志乱萃，不虞，坤下兑上之象，利其不自主而取之。',
            explanation='敌人意志混乱，出乎意料，利用其不能自主的机会采取行动。',
            principles=['虚实结合', '迷惑敌人', '出其不意'],
            applications=['市场策略', '谈判技巧', '军事行动'],
            historical_cases=['韩信破魏']
        )
    
    def _add_confrontation_strategies(self):
        """添加敌战计"""
        self.strategies['无中生有'] = StrategyInfo(
            name='无中生有',
            category=StrategyCategory.CONFRONTATION,
            original_text='诳也，非诳也，实其所诳也。',
            explanation='用假象欺骗敌人，但不是完全的虚假，而是使虚假变成真实。',
            principles=['虚实转换', '制造假象', '化虚为实'],
            applications=['品牌建设', '市场造势', '谈判策略'],
            historical_cases=['张仪欺楚']
        )
        
        self.strategies['暗度陈仓'] = StrategyInfo(
            name='暗度陈仓',
            category=StrategyCategory.CONFRONTATION,
            original_text='示之以动，利其静而有主，益动而巽。',
            explanation='表面上显示行动，利用敌人的静止，暗中采取真正的行动。',
            principles=['明修栈道', '暗度陈仓', '出其不意'],
            applications=['商业布局', '战略转移', '秘密行动'],
            historical_cases=['韩信出川']
        )
        
        self.strategies['隔岸观火'] = StrategyInfo(
            name='隔岸观火',
            category=StrategyCategory.CONFRONTATION,
            original_text='阳乖序乱，阴以待逆。暴戾恣睢，其势自毙。',
            explanation='敌人内部混乱时，静观其变，等待其自灭。',
            principles=['坐山观虎斗', '等待时机', '渔翁得利'],
            applications=['竞争策略', '危机处理', '投资决策'],
            historical_cases=['苏代救周']
        )
        
        self.strategies['笑里藏刀'] = StrategyInfo(
            name='笑里藏刀',
            category=StrategyCategory.CONFRONTATION,
            original_text='信而安之，阴以图之；备而后动，勿使有变。',
            explanation='使敌人相信并安心，暗中图谋；准备充分后再行动，不要使情况发生变化。',
            principles=['外柔内刚', '麻痹敌人', '伺机而动'],
            applications=['商业谈判', '竞争策略', '危机处理'],
            historical_cases=['曹操煮酒论英雄']
        )
        
        self.strategies['李代桃僵'] = StrategyInfo(
            name='李代桃僵',
            category=StrategyCategory.CONFRONTATION,
            original_text='势必有损，损阴以益阳。',
            explanation='当形势必然有损失时，牺牲局部以保全整体。',
            principles=['丢卒保车', '舍小保大', '战略牺牲'],
            applications=['危机处理', '资源调配', '战略调整'],
            historical_cases=['赵氏孤儿']
        )
        
        self.strategies['顺手牵羊'] = StrategyInfo(
            name='顺手牵羊',
            category=StrategyCategory.CONFRONTATION,
            original_text='微隙在所必乘，微利在所必得。',
            explanation='敌人微小的漏洞必须利用，微小的利益必须获取。',
            principles=['抓住机会', '积小胜为大胜', '灵活机动'],
            applications=['商业机会', '市场拓展', '资源整合'],
            historical_cases=['谢石破秦']
        )
    
    def _add_attack_strategies(self):
        """添加攻战计"""
        self.strategies['打草惊蛇'] = StrategyInfo(
            name='打草惊蛇',
            category=StrategyCategory.ATTACK,
            original_text='疑以叩实，察而后动；复者，阴之媒也。',
            explanation='用试探来查明真相，观察后再行动；反复试探是发现隐藏敌人的媒介。',
            principles=['试探虚实', '侦察敌情', '谨慎行动'],
            applications=['市场调研', '竞争情报', '风险评估'],
            historical_cases=['王鲁丢印']
        )
        
        self.strategies['借尸还魂'] = StrategyInfo(
            name='借尸还魂',
            category=StrategyCategory.ATTACK,
            original_text='有用者，不可借；不能用者，求借。',
            explanation='有用的东西不可借用，不能用的东西才要求借，借来后使其为我所用。',
            principles=['废物利用', '借壳上市', '资源整合'],
            applications=['品牌重塑', '资产重组', '战略转型'],
            historical_cases=['刘备借荆州']
        )
        
        self.strategies['调虎离山'] = StrategyInfo(
            name='调虎离山',
            category=StrategyCategory.ATTACK,
            original_text='待天以困之，用人以诱之，往蹇来连。',
            explanation='等待天时使敌人陷入困境，用人为的诱饵引诱敌人，使其离开有利地形。',
            principles=['诱敌深入', '分散敌人', '攻其不备'],
            applications=['商业竞争', '谈判策略', '市场争夺'],
            historical_cases=['虞诩破羌']
        )
        
        self.strategies['欲擒故纵'] = StrategyInfo(
            name='欲擒故纵',
            category=StrategyCategory.ATTACK,
            original_text='逼则反兵，走则减势。紧随勿迫，累其气力，消其斗志，散而后擒，兵不血刃。',
            explanation='逼迫太紧敌人会拼死反抗，让其逃跑会削弱其气势。跟随但不逼迫，消耗其体力，瓦解其斗志，然后擒获。',
            principles=['欲擒故纵', '消耗敌人', '瓦解斗志'],
            applications=['谈判策略', '客户管理', '竞争策略'],
            historical_cases=['诸葛亮七擒孟获']
        )
        
        self.strategies['抛砖引玉'] = StrategyInfo(
            name='抛砖引玉',
            category=StrategyCategory.ATTACK,
            original_text='类以诱之，击蒙也。',
            explanation='用类似的东西引诱敌人，打击被蒙蔽的敌人。',
            principles=['以小引大', '诱饵策略', '信息获取'],
            applications=['市场营销', '产品推广', '谈判策略'],
            historical_cases=['契丹攻唐']
        )
        
        self.strategies['擒贼擒王'] = StrategyInfo(
            name='擒贼擒王',
            category=StrategyCategory.ATTACK,
            original_text='摧其坚，夺其魁，以解其体。',
            explanation='摧毁敌人的坚固防线，擒获其首领，以瓦解其整体。',
            principles=['擒贼擒王', '斩首行动', '攻其要害'],
            applications=['竞争策略', '危机处理', '战略打击'],
            historical_cases=['张巡守睢阳']
        )
    
    def _add_chaos_strategies(self):
        """添加混战计"""
        self.strategies['釜底抽薪'] = StrategyInfo(
            name='釜底抽薪',
            category=StrategyCategory.CHAOS,
            original_text='不敌其力，而消其势，兑下乾上之象。',
            explanation='不直接对抗敌人的力量，而是削弱其气势，从根本上解决问题。',
            principles=['从根本上解决', '削弱气势', '间接路线'],
            applications=['危机处理', '竞争策略', '资源调配'],
            historical_cases=['曹操烧乌巢']
        )
        
        self.strategies['浑水摸鱼'] = StrategyInfo(
            name='浑水摸鱼',
            category=StrategyCategory.CHAOS,
            original_text='乘其阴乱，利其弱而无主。随，以向晦入宴息。',
            explanation='乘敌人内部混乱，利用其虚弱且无主见，像随卦那样向黑暗处行动。',
            principles=['浑水摸鱼', '趁乱取利', '把握时机'],
            applications=['危机收购', '市场机会', '竞争策略'],
            historical_cases=['刘备取荆州']
        )
        
        self.strategies['金蝉脱壳'] = StrategyInfo(
            name='金蝉脱壳',
            category=StrategyCategory.CHAOS,
            original_text='存其形，完其势；友不疑，敌不动。巽而止蛊。',
            explanation='保持原有形态和气势，使盟友不疑，敌人不动，暗中转移。',
            principles=['金蝉脱壳', '暗度陈仓', '保存实力'],
            applications=['战略转移', '危机处理', '撤退策略'],
            historical_cases=['孙坚换帻']
        )
        
        self.strategies['关门捉贼'] = StrategyInfo(
            name='关门捉贼',
            category=StrategyCategory.CHAOS,
            original_text='小敌困之。剥，不利有攸往。',
            explanation='对小股敌人要包围歼灭，如果让其逃跑，日后必成大患。',
            principles=['关门捉贼', '斩草除根', '不留后患'],
            applications=['危机处理', '竞争策略', '问题解决'],
            historical_cases=['白起坑赵卒']
        )
        
        self.strategies['远交近攻'] = StrategyInfo(
            name='远交近攻',
            category=StrategyCategory.CHAOS,
            original_text='形禁势格，利从近取，害以远隔。上火下泽。',
            explanation='受到形势限制时，先攻取近处的敌人，结交远处的敌人，各个击破。',
            principles=['远交近攻', '各个击破', '分化瓦解'],
            applications=['商业联盟', '竞争策略', '外交策略'],
            historical_cases=['范雎献计']
        )
        
        self.strategies['假道伐虢'] = StrategyInfo(
            name='假道伐虢',
            category=StrategyCategory.CHAOS,
            original_text='两大之间，敌胁以从，我假以势。困，有言不信。',
            explanation='处于两个大国之间，敌人胁迫其服从时，我借其地势以成事。',
            principles=['假道伐虢', '借力打力', '一石二鸟'],
            applications=['商业合作', '竞争策略', '战略联盟'],
            historical_cases=['晋献公灭虢']
        )
    
    def _add_merge_strategies(self):
        """添加并战计"""
        self.strategies['偷梁换柱'] = StrategyInfo(
            name='偷梁换柱',
            category=StrategyCategory.MERGE,
            original_text='频更其阵，抽其劲旅，待其自败，而后乘之。',
            explanation='频繁更换敌人的阵势，抽掉其主力，等待其自败后再乘机取之。',
            principles=['偷梁换柱', '暗中替换', '瓦解敌人'],
            applications=['组织变革', '战略调整', '竞争策略'],
            historical_cases=['赵高矫诏']
        )
        
        self.strategies['指桑骂槐'] = StrategyInfo(
            name='指桑骂槐',
            category=StrategyCategory.MERGE,
            original_text='大凌小者，警以诱之。刚中而应，行险而顺。',
            explanation='以强凌弱时，用警告来诱导，内刚外柔，行险而顺。',
            principles=['指桑骂槐', '杀鸡儆猴', '警示作用'],
            applications=['管理策略', '谈判技巧', '危机处理'],
            historical_cases=['孙武斩美']
        )
        
        self.strategies['假痴不癫'] = StrategyInfo(
            name='假痴不癫',
            category=StrategyCategory.MERGE,
            original_text='宁伪作不知不为，不伪作假知妄为。',
            explanation='宁可假装不知道而不行动，不可假装知道而妄动。',
            principles=['韬光养晦', '隐藏实力', '等待时机'],
            applications=['商业策略', '竞争策略', '危机处理'],
            historical_cases=['司马懿装病']
        )
        
        self.strategies['上屋抽梯'] = StrategyInfo(
            name='上屋抽梯',
            category=StrategyCategory.MERGE,
            original_text='假之以便，唆之使前，断其援应，陷之死地。',
            explanation='给敌人提供便利，诱使其前进，然后断绝其援应，使其陷入死地。',
            principles=['诱敌深入', '断其后路', '置之死地'],
            applications=['竞争策略', '谈判技巧', '危机处理'],
            historical_cases=['刘琦求计']
        )
        
        self.strategies['树上开花'] = StrategyInfo(
            name='树上开花',
            category=StrategyCategory.MERGE,
            original_text='借局布势，力小势大。鸿渐于陆，其羽可用为仪也。',
            explanation='借助局面布置气势，使弱小的力量显得强大。',
            principles=['虚张声势', '借势造势', '以弱示强'],
            applications=['品牌建设', '市场策略', '谈判技巧'],
            historical_cases=['张飞断桥']
        )
        
        self.strategies['反客为主'] = StrategyInfo(
            name='反客为主',
            category=StrategyCategory.MERGE,
            original_text='乘隙插足，扼其主机，渐之进也。',
            explanation='乘机插足，掌握敌人的关键，逐渐推进，反客为主。',
            principles=['反客为主', '掌握主动', '逐步渗透'],
            applications=['商业竞争', '谈判策略', '组织变革'],
            historical_cases=['郭子仪单骑']
        )
    
    def _add_retreat_strategies(self):
        """添加败战计"""
        self.strategies['美人计'] = StrategyInfo(
            name='美人计',
            category=StrategyCategory.RETREAT,
            original_text='兵强者，攻其将；将智者，伐其情。',
            explanation='对兵力强大的敌人，攻击其将领；对足智多谋的将领，腐蚀其意志。',
            principles=['攻心为上', '腐蚀意志', '软化敌人'],
            applications=['谈判策略', '客户关系', '竞争策略'],
            historical_cases=['西施亡吴']
        )
        
        self.strategies['空城计'] = StrategyInfo(
            name='空城计',
            category=StrategyCategory.RETREAT,
            original_text='虚者虚之，疑中生疑；刚柔之际，奇而复奇。',
            explanation='空虚的显示空虚，使敌人疑上加疑，在刚柔转换之际，出奇制胜。',
            principles=['虚者虚之', '疑兵之计', '心理战术'],
            applications=['危机处理', '谈判策略', '竞争策略'],
            historical_cases=['诸葛亮空城']
        )
        
        self.strategies['反间计'] = StrategyInfo(
            name='反间计',
            category=StrategyCategory.RETREAT,
            original_text='疑中之疑，比之自内，不自失也。',
            explanation='在敌人的疑阵中再布疑阵，利用敌人内部的人，自己不会受到损失。',
            principles=['反间计', '利用内奸', '分化瓦解'],
            applications=['情报战', '竞争策略', '危机处理'],
            historical_cases=['陈平离间']
        )
        
        self.strategies['苦肉计'] = StrategyInfo(
            name='苦肉计',
            category=StrategyCategory.RETREAT,
            original_text='人不自害，受害必真；假真真假，间以得行。',
            explanation='人不会自己伤害自己，受害必然是真的；真真假假，间谍才能成功。',
            principles=['苦肉计', '骗取信任', '卧底渗透'],
            applications=['危机处理', '谈判策略', '竞争策略'],
            historical_cases=['周瑜打黄盖']
        )
        
        self.strategies['连环计'] = StrategyInfo(
            name='连环计',
            category=StrategyCategory.RETREAT,
            original_text='将多兵众，不可以敌，使其自累，以杀其势。',
            explanation='敌人将多兵众，不可硬敌，使其自我牵制，以削弱其势力。',
            principles=['连环计', '使其自累', '削弱敌人'],
            applications=['竞争策略', '危机处理', '战略设计'],
            historical_cases=['庞统献连环']
        )
        
        self.strategies['走为上计'] = StrategyInfo(
            name='走为上计',
            category=StrategyCategory.RETREAT,
            original_text='全师避敌，左次无咎，未失常也。',
            explanation='全军退避敌人，左次无咎，没有违背常规。',
            principles=['走为上', '保存实力', '战略转移'],
            applications=['危机处理', '战略撤退', '资源保全'],
            historical_cases=['晋文公退避三舍']
        )
    
    def get_by_category(self, category: StrategyCategory) -> List[StrategyInfo]:
        """按类别获取策略"""
        return [s for s in self.strategies.values() if s.category == category]
    
    def get_by_name(self, name: str) -> Optional[StrategyInfo]:
        """按名称获取策略"""
        return self.strategies.get(name)
