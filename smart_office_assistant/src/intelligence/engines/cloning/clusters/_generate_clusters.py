# -*- coding: utf-8 -*-
"""
Cloning系统 - 集群生成脚本
批量生成12个学派集群模块
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 集群定义: (文件名, 集群名, 学派, 部门, 领军人物)
CLUSTERS = [
    ("legalist_cluster.py", "法家集群", "法家", "刑部", "韩非子"),
    ("mohist_cluster.py", "墨家集群", "墨家", "工部", "墨子"),
    ("xinxue_cluster.py", "心学集群", "心学", "礼部", "王阳明"),
    ("lixue_cluster.py", "理学集群", "理学", "礼部", "朱熹"),
    ("diplomatist_cluster.py", "纵横家集群", "纵横家", "厂卫", "鬼谷子"),
    ("medical_cluster.py", "医家集群", "医家", "户部", "张仲景"),
    ("historian_cluster.py", "史学集群", "史学", "五军都督府", "司马迁"),
    ("literary_cluster.py", "文学集群", "文学", "礼部", "苏轼"),
    ("scientist_cluster.py", "科技集群", "科技", "工部", "张衡"),
    ("marketing_cluster.py", "营销集群", "营销学", "户部", "科特勒"),
    ("investment_cluster.py", "投资集群", "价值投资", "户部", "巴菲特"),
    ("entrepreneur_cluster.py", "创业集群", "创新创业", "工部", "马斯克"),
]

# 成员定义: (集群key, 成员列表)
# 每个成员: (name, name_en, era, years, title, bio, works, wisdom_laws, cap, position, keywords)
MEMBERS = {
    "legalist": [
        ("商鞅", "Shang Yang", "战国中期", "前390-前338", "变法先驱",
         "战国政治家，在秦国推行变法使秦国强大。", "《商君书》",
         ["法不阿贵——法律面前人人平等", "奖励耕战——以制度引导行为", "徙木立信——公信力是执行力的基础"],
         {"strategic_vision":9,"execution":10,"innovation":9,"leadership":8,"influence":9,"cross_domain":6},
         "刑部主事", ["制度","法治","务实","改革"]),
        ("管仲", "Guan Zhong", "春秋", "前723-前645", "华夏第一相",
         "春秋齐国政治家，辅佐齐桓公成为春秋首霸。", "《管子》",
         ["仓廪实而知礼节——物质基础决定上层建筑", "四维不张国乃灭亡——礼义廉耻是根基", "与俗同好恶——政策顺应民心"],
         {"strategic_vision":10,"execution":9,"innovation":9,"leadership":9,"influence":10,"cross_domain":8},
         "户部侍郎", ["经济","民生","全局","统筹"]),
        ("李斯", "Li Si", "秦代", "前284-前208", "统一功臣",
         "秦朝丞相，推动书同文车同轨等统一政策。", "",
         ["统一标准——减少内耗的最佳方式", "以史为鉴——从历史中学习治理", "各尽其能——人尽其才物尽其用"],
         {"strategic_vision":8,"execution":9,"innovation":8,"leadership":7,"influence":9,"cross_domain":7},
         "吏部主事", ["统一","标准","规范","整合"]),
        ("申不害", "Shen Buhai", "战国中期", "前385-前337", "术治先驱",
         "战国法家思想家，以'术'（权术）著称。", "",
         ["术治——用制度和信息控制权力", "循名责实——名实相符方为正道", "因任授官——能力匹配职位"],
         {"strategic_vision":7,"execution":8,"innovation":8,"leadership":7,"influence":7,"cross_domain":6},
         "厂卫主事", ["权术","监控","考核","名实"]),
    ],
    "mohist": [
        ("禽滑厘", "Qin Guli", "战国", "前470-前390", "墨家巨子",
         "墨子最重要的弟子，墨家第二任巨子。", "",
         ["兼爱非攻——和平主义先驱", "身体力行——实践墨子理念", "组织纪律——墨者集团以纪律严明著称"],
         {"strategic_vision":6,"execution":9,"innovation":6,"leadership":8,"influence":6,"cross_domain":5},
         "工部主事", ["实践","纪律","和平","执行"]),
    ],
    "xinxue": [
        ("陆九渊", "Lu Jiuyuan", "南宋", "1139-1193", "象山先生",
         "南宋理学家，心学先驱，提出'心即理'。", "《象山全集》",
         ["心即理——心外无物，心外无理", "辨志——先立志再治学", "易简功夫——大道至简"],
         {"strategic_vision":8,"execution":7,"innovation":9,"leadership":7,"influence":8,"cross_domain":7},
         "礼部主事", ["本心","立志","简洁","直觉"]),
        ("李贽", "Li Zhi", "明代", "1527-1602", "卓吾先生",
         "明代思想家，以批判精神著称，主张个性解放。", "《焚书》《藏书》",
         ["童心说——保持真实不被污染的心", "反传统——质疑权威和教条", "个性解放——尊重每个人的独特性"],
         {"strategic_vision":7,"execution":6,"innovation":10,"leadership":6,"influence":8,"cross_domain":7},
         "吏部主事", ["真实","反叛","个性","自由"]),
        ("黄宗羲", "Huang Zongxi", "明末清初", "1610-1695", "梨洲先生",
         "明末清初思想家，提出'天下为主君为客'。", "《明夷待访录》",
         ["天下为主君为客——权力来源于人民", "学校议政——公共讨论是治理基础", "工商皆本——经济思想的超前突破"],
         {"strategic_vision":9,"execution":6,"innovation":9,"leadership":7,"influence":9,"cross_domain":8},
         "吏部侍郎", ["民主","经济","制度","公共"]),
    ],
    "lixue": [
        ("程颢", "Cheng Hao", "北宋", "1032-1085", "明道先生",
         "北宋理学家，'洛学'创始人之一。", "",
         ["仁者浑然与物同体——万物一体的世界观", "识仁——通过修养体认仁的境界", "定性——不被外物所动的定力"],
         {"strategic_vision":7,"execution":6,"innovation":8,"leadership":6,"influence":8,"cross_domain":7},
         "礼部主事", ["仁","整体","修养","定性"]),
        ("程颐", "Cheng Yi", "北宋", "1033-1107", "伊川先生",
         "北宋理学家，'洛学'创始人之一，主张'性即理'。", "",
         ["性即理——人性中蕴含天理", "涵养须用敬——以敬畏之心修养", "格物致知——通过研究事物获取知识"],
         {"strategic_vision":7,"execution":6,"innovation":7,"leadership":6,"influence":8,"cross_domain":6},
         "礼部主事", ["敬","理","格物","致知"]),
        ("张载", "Zhang Zai", "北宋", "1020-1077", "横渠先生",
         "北宋理学家，提出'为天地立心'。", "《正蒙》",
         ["为天地立心——知识分子的终极使命", "为生民立命——改善民生的责任感", "横渠四句——天地生民往圣万世"],
         {"strategic_vision":8,"execution":6,"innovation":8,"leadership":7,"influence":9,"cross_domain":7},
         "礼部侍郎", ["使命","民生","责任","担当"]),
        ("邵雍", "Shao Yong", "北宋", "1011-1077", "康节先生",
         "北宋理学家、数学家，先天象数体系创立者。", "《皇极经世》",
         ["先天象数——以数学模型描述宇宙", "观物——从整体上观察和理解事物", "元会运世——宏观周期理论"],
         {"strategic_vision":9,"execution":5,"innovation":10,"leadership":5,"influence":7,"cross_domain":9},
         "五军都督府主事", ["系统","周期","数学","宏观"]),
    ],
    "diplomatist": [
        ("苏秦", "Su Qin", "战国中期", "前380-前284", "合纵家",
         "战国纵横家，以'合纵'策略联合六国抗秦。", "《苏子》",
         ["合纵——联合弱者对抗强者", "口舌之劳——言语的力量超越刀剑", "时势造英雄——把握历史机遇"],
         {"strategic_vision":9,"execution":8,"innovation":8,"leadership":8,"influence":9,"cross_domain":7},
         "兵部主事", ["联盟","合作","时机","说服"]),
        ("张仪", "Zhang Yi", "战国中期", "前378-前309", "连横家",
         "战国纵横家，以'连横'策略分化六国。", "",
         ["连横——分化瓦解对手联盟", "利诱——以利益驱使对方决策", "因势利导——根据形势灵活变化"],
         {"strategic_vision":9,"execution":9,"innovation":7,"leadership":8,"influence":8,"cross_domain":7},
         "厂卫主事", ["分化","利诱","灵活","策略"]),
        ("陈平", "Chen Ping", "秦末汉初", "前?-前178", "六出奇计",
         "汉初谋士，以'六出奇计'辅佐刘邦。", "",
         ["奇计——非常规手段解决关键问题", "反间——利用信息不对称分化敌人", "知人善任——看人极准"],
         {"strategic_vision":9,"execution":8,"innovation":9,"leadership":7,"influence":7,"cross_domain":6},
         "内阁主事", ["奇计","情报","用人","反间"]),
    ],
    "medical": [
        ("华佗", "Hua Tuo", "东汉", "约145-208", "神医",
         "东汉末年医学家，外科鼻祖，发明麻沸散。", "",
         ["对症下药——因人制宜的治疗方案", "预防为主——治未病的理念", "五禽戏——运动是健康之本"],
         {"strategic_vision":7,"execution":9,"innovation":10,"leadership":6,"influence":9,"cross_domain":6},
         "礼部主事", ["创新","预防","对症","运动"]),
        ("孙思邈", "Sun Simiao", "唐代", "541-682", "药王",
         "唐代医学家，著有《千金要方》。", "《千金要方》《千金翼方》",
         ["大医精诚——医者的职业道德", "养生有道——预防重于治疗", "综合治疗——身心并治"],
         {"strategic_vision":7,"execution":8,"innovation":7,"leadership":7,"influence":9,"cross_domain":7},
         "户部主事", ["道德","养生","综合","细节"]),
        ("李时珍", "Li Shizhen", "明代", "1518-1593", "药圣",
         "明代医学家，著有《本草纲目》。", "《本草纲目》",
         ["实证精神——亲身验证每一种药物", "系统分类——建立完整的知识体系", "持之以恒——27年编成一部书"],
         {"strategic_vision":7,"execution":10,"innovation":8,"leadership":6,"influence":10,"cross_domain":7},
         "户部主事", ["实证","系统","坚持","分类"]),
        ("葛洪", "Ge Hong", "东晋", "284-364", "抱朴子",
         "东晋道教学者、炼丹家、医学家。", "《抱朴子》《肘后备急方》",
         ["急症急救——快速应对突发状况", "实验精神——炼丹即古代化学实验", "简便验廉——用最简单的方法解决最大问题"],
         {"strategic_vision":7,"execution":8,"innovation":9,"leadership":5,"influence":7,"cross_domain":8},
         "工部主事", ["急救","实验","简便","实用"]),
        ("陶弘景", "Tao Hongjing", "南朝", "456-536", "山中宰相",
         "南朝道教思想家、医学家。", "《本草经集注》《养性延命录》",
         ["系统整理——建立知识的分类体系", "养生之道——身心合一的健康观", "隐士智慧——在退隐中观察和思考"],
         {"strategic_vision":7,"execution":7,"innovation":7,"leadership":6,"influence":7,"cross_domain":7},
         "户部主事", ["系统","养生","分类","整合"]),
    ],
    "historian": [
        ("班固", "Ban Gu", "东汉", "32-92", "汉书作者",
         "东汉史学家，中国第一部纪传体断代史《汉书》作者。", "《汉书》",
         ["断代为史——专注于一个时代深入研究", "体例创新——开创纪传体断代史", "文史兼通——文学与史学并重"],
         {"strategic_vision":7,"execution":9,"innovation":8,"leadership":6,"influence":9,"cross_domain":7},
         "五军都督府主事", ["专注","系统","断代","整理"]),
        ("司马光", "Sima Guang", "北宋", "1019-1086", "资治通鉴作者",
         "北宋政治家、史学家，编撰《资治通鉴》。", "《资治通鉴》",
         ["以史为鉴——从历史中提取决策智慧", "编年叙事——以时间为线索还原真相", "鉴于往事有资于治道——历史服务于现实"],
         {"strategic_vision":9,"execution":8,"innovation":7,"leadership":8,"influence":10,"cross_domain":8},
         "内阁学士", ["历史","借鉴","决策","治理"]),
        ("刘知几", "Liu Zhiji", "唐代", "661-721", "史通作者",
         "唐代史学理论家，著有中国第一部史学理论著作《史通》。", "《史通》",
         ["史学方法论——建立评判历史的标准", "直笔实录——不受政治干预如实记录", "识才——好的史学家需要才学识三长"],
         {"strategic_vision":7,"execution":7,"innovation":9,"leadership":6,"influence":7,"cross_domain":7},
         "五军都督府主事", ["方法论","客观","批判","标准"]),
        ("杜佑", "Du You", "唐代", "735-812", "通典作者",
         "唐代政治家、史学家，著有中国第一部制度史《通典》。", "《通典》",
         ["制度史观——从制度变迁理解历史", "经世致用——史学服务于现实治理", "分类考述——系统化研究各类制度"],
         {"strategic_vision":8,"execution":8,"innovation":8,"leadership":7,"influence":7,"cross_domain":7},
         "户部侍郎", ["制度","实用","分类","经济"]),
    ],
    "literary": [
        ("李白", "Li Bai", "唐代", "701-762", "诗仙",
         "唐代浪漫主义诗人，被称为'诗仙'。", "《李太白集》",
         ["天生我材必有用——极致的自信和才华", "浪漫超越——突破现实的想象力", "自由精神——不受拘束的表达"],
         {"strategic_vision":7,"execution":5,"innovation":10,"leadership":5,"influence":10,"cross_domain":8},
         "礼部主事", ["想象","自由","激情","创意"]),
        ("杜甫", "Du Fu", "唐代", "712-770", "诗圣",
         "唐代现实主义诗人，被称为'诗圣'。", "《杜工部集》",
         ["忧国忧民——深沉的社会责任感", "现实主义——直面社会真相", "沉郁顿挫——深沉有力的表达"],
         {"strategic_vision":8,"execution":7,"innovation":8,"leadership":7,"influence":10,"cross_domain":8},
         "礼部侍郎", ["现实","责任","民生","深度"]),
        ("白居易", "Bai Juyi", "唐代", "772-846", "诗魔",
         "唐代诗人，主张'文章合为时而著'。", "《白氏长庆集》",
         ["通俗易懂——让所有人都能理解", "文章合为时而著——写作服务于现实", "兼济天下——知识分子的社会担当"],
         {"strategic_vision":8,"execution":8,"innovation":7,"leadership":7,"influence":9,"cross_domain":7},
         "礼部主事", ["通俗","现实","传播","社会"]),
        ("辛弃疾", "Xin Qiji", "南宋", "1140-1207", "词中之龙",
         "南宋爱国词人，以豪放词风著称。", "《稼轩词》",
         ["壮志难酬——理想与现实的永恒张力", "豪放创新——打破词的柔美传统", "文武兼备——词人中的将军"],
         {"strategic_vision":8,"execution":8,"innovation":9,"leadership":8,"influence":9,"cross_domain":8},
         "兵部主事", ["豪放","爱国","创新","跨界"]),
        ("曹雪芹", "Cao Xueqin", "清代", "约1715-1763", "红楼梦作者",
         "清代文学家，《红楼梦》作者。", "《红楼梦》",
         ["人性洞察——对人性的深刻理解", "百科全书式写作——一个作品涵盖整个时代", "悲剧美学——在毁灭中展现美"],
         {"strategic_vision":9,"execution":6,"innovation":10,"leadership":5,"influence":10,"cross_domain":9},
         "礼部侍郎", ["人性","细节","深度","全貌"]),
    ],
    "scientist": [
        ("祖冲之", "Zu Chongzhi", "南北朝", "429-500", "数学泰斗",
         "南北朝数学家、天文学家，将圆周率精确到小数点后7位。", "《大明历》",
         ["极致精确——追求计算的极限精度", "打破权威——质疑前人的结论", "数学建模——用数学描述自然规律"],
         {"strategic_vision":7,"execution":9,"innovation":10,"leadership":5,"influence":9,"cross_domain":8},
         "工部主事", ["精确","数学","质疑","建模"]),
        ("沈括", "Shen Kuo", "北宋", "1031-1095", "中国科学全才",
         "北宋科学家、政治家，《梦溪笔谈》作者。", "《梦溪笔谈》",
         ["跨学科整合——天文地理物理化学无所不包", "实验验证——以实践检验理论", "系统记录——详尽记录观察和数据"],
         {"strategic_vision":9,"execution":8,"innovation":10,"leadership":7,"influence":9,"cross_domain":10},
         "工部侍郎", ["跨学科","实验","记录","系统"]),
        ("郭守敬", "Guo Shoujing", "元代", "1231-1316", "天文大师",
         "元代天文学家、数学家、水利学家。", "《授时历》",
         ["实测精神——亲自动手测量和验证", "精密仪器——发明制造天文仪器", "水利工程——理论与实践结合"],
         {"strategic_vision":8,"execution":10,"innovation":9,"leadership":7,"influence":8,"cross_domain":8},
         "工部主事", ["实测","仪器","水利","精密"]),
        ("宋应星", "Song Yingxing", "明代", "1587-1666", "中国狄德罗",
         "明代科学家，《天工开物》作者。", "《天工开物》",
         ["工艺百科——系统记录工农业生产技术", "实用主义——技术服务于生产", "工匠精神——尊重劳动和技术"],
         {"strategic_vision":7,"execution":8,"innovation":8,"leadership":5,"influence":8,"cross_domain":8},
         "工部主事", ["工艺","实用","技术","生产"]),
        ("徐光启", "Xu Guangqi", "明代", "1562-1633", "中西交流先驱",
         "明代科学家，翻译《几何原本》，引进西方科学。", "《农政全书》",
         ["中西融合——引进消化西方先进知识", "实用科学——科学服务于农业和国防", "数学思维——用数学方法解决实际问题"],
         {"strategic_vision":9,"execution":8,"innovation":9,"leadership":8,"influence":9,"cross_domain":10},
         "工部侍郎", ["中西融合","数学","农业","引进"]),
    ],
    "marketing": [
        ("奥格威", "David Ogilvy", "20世纪", "1911-1999", "广告教父",
         "奥美广告创始人，被称为'广告教父'。", "《一个广告人的自白》",
         ["广告的目标是销售——不是艺术", "深入研究产品——好创意来自深理解", "品牌形象——长期积累的品牌资产"],
         {"strategic_vision":8,"execution":9,"innovation":8,"leadership":9,"influence":10,"cross_domain":7},
         "户部主事", ["销售","品牌","研究","创意"]),
        ("特劳特", "Jack Trout", "20世纪", "1935-2017", "定位之父",
         "定位理论创始人。", "《定位》",
         ["成为第一胜过做得更好——心智占领", "聚焦——不要试图满足所有人", "差异化——找到对手无法模仿的独特性"],
         {"strategic_vision":9,"execution":7,"innovation":9,"leadership":7,"influence":9,"cross_domain":7},
         "户部主事", ["定位","聚焦","差异化","心智"]),
        ("里斯", "Al Ries", "20世纪", "1926-", "定位之父",
         "定位理论联合创始人。", "《定位》《22条商规》",
         ["品类创建——比品牌更重要的是品类", "对立定位——与领导者对着干", "营销是一场心智战"],
         {"strategic_vision":8,"execution":7,"innovation":9,"leadership":6,"influence":8,"cross_domain":7},
         "户部主事", ["品类","对立","心智","规律"]),
        ("舒尔茨", "Don Schultz", "20世纪", "1940-", "整合营销之父",
         "整合营销传播理论创始人。", "《整合营销传播》",
         ["整合传播——所有触点传递一致信息", "以顾客为中心——从卖方到买方的范式转变", "触点管理——每一个接触都是营销机会"],
         {"strategic_vision":8,"execution":7,"innovation":8,"leadership":7,"influence":8,"cross_domain":8},
         "户部主事", ["整合","顾客","触点","一致"]),
        ("莱维特", "Theodore Levitt", "20世纪", "1925-2006", "营销短文大师",
         "哈佛商学院教授，'营销近视症'概念提出者。", "",
         ["营销近视症——行业定义不应局限于产品", "全球化——标准化的全球营销", "产品差异化——持续的差异化是竞争关键"],
         {"strategic_vision":9,"execution":7,"innovation":9,"leadership":7,"influence":8,"cross_domain":7},
         "户部主事", ["视野","全球化","差异化","行业"]),
    ],
    "investment": [
        ("芒格", "Charlie Munger", "20-21世纪", "1924-2023", "巴菲特的右手",
         "伯克希尔副董事长，多元思维模型倡导者。", "《穷查理宝典》",
         ["多元思维模型——用跨学科框架做决策", "逆向思维——反过来想总是反过来想", "能力圈——知道自己不知道什么"],
         {"strategic_vision":10,"execution":8,"innovation":9,"leadership":9,"influence":10,"cross_domain":10},
         "内阁学士", ["多元","逆向","模型","跨学科"]),
        ("达利欧", "Ray Dalio", "21世纪", "1949-", "原则化决策",
         "桥水基金创始人，《原则》作者。", "《原则》",
         ["原则化决策——把决策标准写成算法", "极度透明——信息完全公开", "经济机器——理解经济运行的底层逻辑"],
         {"strategic_vision":10,"execution":9,"innovation":9,"leadership":9,"influence":9,"cross_domain":8},
         "户部侍郎", ["原则","透明","系统","经济"]),
        ("费雪", "Philip Fisher", "20世纪", "1907-2004", "成长股投资之父",
         "成长股投资先驱，巴菲特的老师之一。", "《怎样选择成长股》",
         ["十五要点——系统化评估成长股", "闲聊法——从非正式渠道获取信息", "长期持有——买入后耐心等待"],
         {"strategic_vision":8,"execution":7,"innovation":8,"leadership":6,"influence":7,"cross_domain":6},
         "户部主事", ["成长","研究","长期","耐心"]),
        ("索罗斯", "George Soros", "20-21世纪", "1930-", "金融大鳄",
         "量子基金创始人，反身性理论提出者。", "《金融炼金术》",
         ["反身性——市场参与者的认知影响市场", "试错法——小仓位验证大方向", "风险意识——生存第一赚钱第二"],
         {"strategic_vision":9,"execution":9,"innovation":10,"leadership":8,"influence":9,"cross_domain":7},
         "户部主事", ["反身性","风险","试错","心理"]),
    ],
    "entrepreneur": [
        ("贝索斯", "Jeff Bezos", "21世纪", "1964-", "长期主义实践者",
         "亚马逊创始人。", "",
         ["长期主义——一切都基于10年以上的判断", "客户至上——从客户需求倒推", "Day 1心态——永远保持创业状态"],
         {"strategic_vision":10,"execution":9,"innovation":9,"leadership":9,"influence":10,"cross_domain":9},
         "工部侍郎", ["长期","客户","效率","规模"]),
        ("任正非", "Ren Zhengfei", "21世纪", "1944-", "华为精神",
         "华为创始人，以狼性文化和自主研发著称。", "",
         ["活下去——企业第一要务是生存", "自主研发——核心技术不能受制于人", "灰度管理——在黑白之间找到平衡"],
         {"strategic_vision":10,"execution":10,"innovation":8,"leadership":10,"influence":10,"cross_domain":7},
         "工部尚书", ["生存","研发","管理","危机"]),
        ("马云", "Jack Ma", "21世纪", "1964-", "电商先驱",
         "阿里巴巴创始人。", "",
         ["让天下没有难做的生意——平台思维", "赋能中小企业——生态而非帝国", "拥抱变化——唯一不变的是变化"],
         {"strategic_vision":9,"execution":8,"innovation":9,"leadership":9,"influence":10,"cross_domain":8},
         "户部侍郎", ["平台","生态","变化","赋能"]),
        ("张一鸣", "Zhang Yiming", "21世纪", "1983-", "算法驱动增长",
         "字节跳动创始人。", "",
         ["算法驱动——用技术解决信息分发", "Context not Control——提供背景而非控制", "延迟满足——短期不赚钱也要做正确的事"],
         {"strategic_vision":9,"execution":9,"innovation":10,"leadership":8,"influence":9,"cross_domain":8},
         "工部主事", ["算法","效率","数据","创新"]),
    ],
}

# 集群名到成员key的映射
CLUSTER_KEY_MAP = {
    "法家集群": "legalist",
    "墨家集群": "mohist",
    "心学集群": "xinxue",
    "理学集群": "lixue",
    "纵横家集群": "diplomatist",
    "医家集群": "medical",
    "史学集群": "historian",
    "文学集群": "literary",
    "科技集群": "scientist",
    "营销集群": "marketing",
    "投资集群": "investment",
    "创业集群": "entrepreneur",
}

def generate_cluster(filename, cluster_name, school, dept, leader):
    key = CLUSTER_KEY_MAP[cluster_name]
    members = MEMBERS.get(key, [])
    
    lines = []
    lines.append(f'# -*- coding: utf-8 -*-')
    lines.append(f'"""{cluster_name} Cloning - Tier 2 学派集群"""')
    lines.append(f'')
    lines.append(f'from typing import Dict, List, Optional, Any'), Any
    lines.append(f'from .._cloning_base import SageCloning, SchoolCluster')
    lines.append(f'from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier')
    lines.append(f'')
    
    for i, (name, name_en, era, years, title, bio, works, laws, cap, pos, kws) in enumerate(members):
        class_name = f"_{name_en.replace(' ', '').replace('-','')}Cloning"
        cap_str = str(cap).replace("'", '"')
        laws_str = str(laws).replace("'", '"')
        kws_str = str(kws).replace("'", '"')
        
        lines.append(f'')
        lines.append(f'class {class_name}(SageCloning):')
        lines.append(f'    """{name}Cloning"""')
        lines.append(f'    def __init__(self):')
        lines.append(f'        super().__init__(SageProfile(')
        lines.append(f'            name="{name}", name_en="{name_en}", era="{era}", years="{years}",')
        lines.append(f'            school="{school}", tier=CloningTier.TIER2_CLUSTER,')
        lines.append(f'            position="{pos}", department="{dept}",')
        lines.append(f'            title="{title}", biography="{bio}",')
        lines.append(f'            core_works=[{works}],')
        lines.append(f'            capability={cap_str},')
        lines.append(f'        ))')
        lines.append(f'        self._wisdom_laws = {laws_str}')
        lines.append(f'')
        lines.append(f'    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:')
        insight = f"从{name}的{title}智慧出发"
        # 用第一条法则做核心洞察
        core = laws[0].split("——")[1] if "——" in laws[0] else laws[0]
        lines.append(f'        return AnalysisResult(')
        lines.append(f'            sage_name="{name}", school="{school}", problem=problem,')
        lines.append(f'            perspective="{insight}",')
        lines.append(f'            core_insight="{core}",')
        lines.append(f'            recommendations=[{laws_str}[i].split("——")[1] if "——" in {laws_str}[i] else {laws_str}[i] for i in range(len({laws_str}))],')
        lines.append(f'            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,')
        lines.append(f'        )')
        lines.append(f'')
        lines.append(f'    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:')
        lines.append(f'        context = context or {{}}')
        lines.append(f'        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in {kws_str}) else 0))')
        lines.append(f'        return DecisionResult(sage_name="{name}", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)')
        lines.append(f'')
        lines.append(f'    def advise(self, context: Dict[str, Any]) -> str:')
        lines.append(f'        return f"{name}的智慧：{laws[0]}"')
        lines.append(f'')
    
    # build_cluster
    lines.append(f'')
    lines.append(f'def build_cluster() -> SchoolCluster:')
    lines.append(f'    """构建{cluster_name}"""')
    member_strs = []
    for name, name_en, era, years, title, bio, works, laws, cap, pos, kws in members:
        class_name = f"_{name_en.replace(' ', '').replace('-','')}Cloning"
        member_strs.append(f'        "{name}": {class_name}(),')
    
    lines.append(f'    return SchoolCluster(')
    lines.append(f'        name="{cluster_name}",')
    lines.append(f'        school="{school}",')
    lines.append(f'        department="{dept}",')
    lines.append(f'        leader_name="{leader}",')
    lines.append(f'        members={{')
    for ms in member_strs:
        lines.append(ms)
    lines.append(f'        }},')
    lines.append(f'    )')
    
    return "\n".join(lines)


# 生成所有集群文件
for filename, cluster_name, school, dept, leader in CLUSTERS:
    content = generate_cluster(filename, cluster_name, school, dept, leader)
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"生成: {filename}")

print(f"\n完成！共生成 {len(CLUSTERS)} 个集群模块")
