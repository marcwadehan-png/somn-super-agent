"""
__all__ = [
    'analyze_shadow',
    'design_brand_archetype',
    'diagnose_archetype',
    'get_narrative_archetype',
]

心理学先驱深化引擎 - 荣格原型系统引擎
Pioneer Jung - Archetype System Engine
======================================
版本: v8.2.0
创建时间: 2026-04-03

荣格核心思想:
1. 集体无意识 - 人类共同的心理遗产
2. 原型理论 - 12大原型/人神imagery
3. 性格类型学 - 外向/内向 + 四种功能
4. 个体化进程 - 自性实现之旅
5. 阴影理论 - 被压抑的黑暗面
6. 阿尼玛/阿尼姆斯 - 男性中的女性/女性中的男性

核心功能:
1. 原型诊断 - recognize用户的主导原型
2. 阴影分析 - recognize被压抑的特质
3. 品牌原型设计 - 构建品牌人格
4. 叙事原型应用 - 故事驱动的品牌传播
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

class 原型类型(Enum):
    """荣格12大原型"""
    # 身份原型
    纯真者 = "纯真者 (Innocent)"
    凡人 = "凡人 (Everyman)"
    探险家 = "探险家 (Explorer)"
    
    # 社会原型
    英雄 = "英雄 (Hero)"
    亡命之徒 = "亡命之徒 (Outlaw)"
    魔法师 = "魔法师 (Magician)"
    
    # 组织原型
    照顾者 = "照顾者 (Caregiver)"
    发明家 = "发明家 (Creator)"
    
    # 秩序原型
    统治者 = "统治者 (Ruler)"
    娱乐者 = "娱乐者 (Jester)"
    智者 = "智者 (Sage)"
    情人 = "情人 (Lover)"
    
    # 超越原型
    梦想家 = "梦想家 (Dreamer)"
    反抗者 = "反抗者 (Rebel)"

class 原型characteristics:
    """原型characteristics描述"""
    def __init__(self, 渴望, 目标, 恐惧, strategy, 才能, 阴影):
        self.渴望 = 渴望
        self.目标 = 目标
        self.恐惧 = 恐惧
        self.strategy = strategy
        self.才能 = 才能
        self.阴影 = 阴影

class 荣格原型引擎:
    """
    荣格原型系统引擎
    
    核心功能:
    1. 原型诊断 - recognize用户的主导原型
    2. 原型组合 - 分析原型间的互动
    3. 阴影分析 - recognize被压抑的阴影特质
    4. 品牌原型设计 - 构建品牌人格
    5. 叙事原型应用 - 故事驱动的品牌传播
    """
    
    def __init__(self):
        self.name = "荣格原型引擎"
        self.version="6.2.0"
        
        # 原型数据库
        self.原型库 = {
            原型类型.纯真者: 原型characteristics(
                渴望="永远保持纯真,避免犯错",
                目标="幸福快乐,保持安全",
                恐惧="被惩罚,被认为有罪",
                strategy="做正确的事,做一个好公民",
                才能="信任,乐观,道德",
                阴影="愚蠢,天真,自欺"
            ),
            原型类型.凡人: 原型characteristics(
                渴望="与他人联系,被需要",
                目标="属于,融入,连接",
                恐惧="与众不同,被边缘化",
                strategy="发展社交技能,让自己有用",
                才能="务实,脚踏实地",
                阴影="没有骨气,失去自我"
            ),
            原型类型.探险家: 原型characteristics(
                渴望="自由探索,找到自我",
                目标="通过体验定义自我",
                恐惧="被困,空虚,无意义",
                strategy="探索,寻找新的体验",
                才能="独立,自主,发现",
                阴影="漫无目的,逃避责任"
            ),
            原型类型.英雄: 原型characteristics(
                渴望="证明自己的价值",
                目标="通过action战胜困难",
                恐惧="软弱,被认为不够好",
                strategy="变得强大,有能力",
                才能="勇气,决心,能力",
                阴影="傲慢,虐待,胜利即失败"
            ),
            原型类型.亡命之徒: 原型characteristics(
                渴望="复仇或颠覆导致不公的事物",
                目标="改变现状",
                恐惧="被发现,无法对抗",
                strategy="破坏,挑战权威",
                才能="勇敢,独立",
                阴影="邪恶,恶意"
            ),
            原型类型.魔法师: 原型characteristics(
                渴望="理解宇宙法则,实现愿景",
                目标="让梦想成真",
                恐惧="意外结果,副作用",
                strategy="学习,掌握力量",
                才能="愿景,转化",
                阴影="操纵,欺骗"
            ),
            原型类型.照顾者: 原型characteristics(
                渴望="保护他人,表达爱",
                目标="帮助他人",
                恐惧="被需要的人拒绝",
                strategy="给予,照顾",
                才能="慷慨,同情",
                阴影="牺牲,自我剥夺"
            ),
            原型类型.发明家: 原型characteristics(
                渴望="创造有意义的价值",
                目标="创造永恒的作品",
                恐惧="缺乏独创性",
                strategy="发明,创新",
                才能="创造力,想象力",
                阴影="完美主义,破坏"
            ),
            原型类型.统治者: 原型characteristics(
                渴望="掌控,创造成功",
                目标="建立繁荣的家庭或企业",
                恐惧="混乱,被推翻",
                strategy="控制,领导",
                才能="领导,责任",
                阴影="专制,滥用权力"
            ),
            原型类型.娱乐者: 原型characteristics(
                渴望="快乐,尽情享受",
                目标="让生活充满乐趣",
                恐惧="无聊,被讨厌",
                strategy="让一切变得有趣",
                才能="幽默,即兴",
                阴影="轻浮,浪费时间"
            ),
            原型类型.智者: 原型characteristics(
                渴望="找到真理和智慧",
                目标="理解世界",
                恐惧="被欺骗,不知道",
                strategy="寻求真理",
                才能="智慧,知识",
                阴影="自以为是,过度分析"
            ),
            原型类型.情人: 原型characteristics(
                渴望="亲密关系,美好体验",
                目标="在爱与美中生活",
                恐惧="孤独,错过",
                strategy="变得更美,更感性",
                才能="激情,欣赏",
                阴影="放纵,失去自我"
            )
        }
        
        # 用户类型到原型的mapping
        self.类型mapping = {
            "理性型": [原型类型.智者, 原型类型.发明家],
            "感性型": [原型类型.情人, 原型类型.照顾者],
            "action型": [原型类型.英雄, 原型类型.探险家],
            "社交型": [原型类型.娱乐者, 原型类型.凡人],
            "控制型": [原型类型.统治者, 原型类型.魔法师]
        }
        
        # 品牌原型组合
        self.品牌原型组合 = {
            "Apple": {"主": 原型类型.发明家, "次": 原型类型.反抗者},
            "Nike": {"主": 原型类型.英雄, "次": 原型类型.娱乐者},
            "Google": {"主": 原型类型.智者, "次": 原型类型.发明家},
            "Disney": {"主": 原型类型.魔法师, "次": 原型类型.纯真者},
            "Starbucks": {"主": 原型类型.情人, "次": 原型类型.照顾者}
        }
    
    def diagnose_archetype(self, user_data: Dict) -> Dict:
        """
        原型诊断
        
        Args:
            user_data: 用户数据
            
        Returns:
            原型诊断结果
        """
        # 简化分析逻辑 - 基于关键词
        behaviors = user_data.get("behaviors", [])
        interests = user_data.get("interests", [])
        values = user_data.get("values", [])
        
        # 统计原型匹配
        原型得分 = {p: 0 for p in 原型类型}
        
        # 关键词mapping
        关键词mapping = {
            原型类型.纯真者: ["善良", "简单", "信任", "乐观"],
            原型类型.凡人: ["接地气", "实用", "普通", "平凡"],
            原型类型.探险家: ["探索", "自由", "旅行", "冒险"],
            原型类型.英雄: ["勇敢", "坚强", "成就", "克服"],
            原型类型.亡命之徒: ["反叛", "颠覆", "挑战", "自由"],
            原型类型.魔法师: ["愿景", "转化", "梦想", "智慧"],
            原型类型.照顾者: ["关怀", "帮助", "付出", "温暖"],
            原型类型.发明家: ["创造", "创新", "独特", "想象"],
            原型类型.统治者: ["领导", "控制", "责任", "成功"],
            原型类型.娱乐者: ["快乐", "幽默", "有趣", "享受"],
            原型类型.智者: ["知识", "学习", "理解", "真理"],
            原型类型.情人: ["爱情", "美", "亲密", "感性"]
        }
        
        all_text = " ".join(behaviors + interests + values)
        for 原型, keywords in 关键词mapping.items():
            for kw in keywords:
                if kw in all_text:
                    原型得分[原型] += 1
        
        # 排序并返回前3
        sorted_archetypes = sorted(原型得分.items(), key=lambda x: x[1], reverse=True)
        
        主原型, 主得分 = sorted_archetypes[0]
        次原型, 次得分 = sorted_archetypes[1]
        
        return {
            "主原型": {
                "类型": 主原型.value,
                "得分": 主得分,
                "characteristics": self._get_archetype_features(主原型)
            },
            "次原型": {
                "类型": 次原型.value,
                "得分": 次得分,
                "characteristics": self._get_archetype_features(次原型)
            },
            "完整排名": [{"原型": p.value, "得分": s} for p, s in sorted_archetypes[:5]],
            "原型解读": self._generate_archetype_interpretation(主原型, 次原型),
            "营销建议": self._generate_marketing_suggestion(主原型, 次原型)
        }
    
    def _get_archetype_features(self, archetype: 原型类型) -> Dict:
        """get原型characteristics"""
        features = self.原型库.get(archetype)
        if not features:
            return {}
        return {
            "渴望": features.渴望,
            "目标": features.目标,
            "恐惧": features.恐惧,
            "strategy": features.strategy,
            "才能": features.才能,
            "阴影": features.阴影
        }
    
    def _generate_archetype_interpretation(self, primary, secondary) -> str:
        """generate原型解读"""
        return f"用户主导原型为{primary.value},次级原型为{secondary.value}." \
               f"这意味着用户在追求{self.原型库[primary].目标}的同时,也关注{self.原型库[secondary].渴望}."
    
    def _generate_marketing_suggestion(self, primary, secondary) -> Dict:
        """generate营销建议"""
        return {
            "品牌定位": f"应体现{primary.value}的核心价值",
            "沟通style": f"采用能引发{primary.value}共鸣的叙事方式",
            "产品设计": f"满足用户对{primary.value}所代表的品质的追求",
            "情感诉求": f"触动用户{self.原型库[primary].渴望}的深层需求"
        }
    
    def design_brand_archetype(self, brand_data: Dict) -> Dict:
        """
        品牌原型设计
        
        Args:
            brand_data: 品牌数据
            
        Returns:
            品牌原型设计方案
        """
        industry = brand_data.get("industry", "")
        target = brand_data.get("target", "")
        value = brand_data.get("core_value", "")
        
        # 根据行业和价值推荐原型
        推荐原型 = self._recommend_archetype(industry, target, value)
        
        # generate品牌原型卡
        primary_archetype = 推荐原型[0]
        secondary_archetype = 推荐原型[1] if len(推荐原型) > 1 else None
        
        brand_archetype_card = {
            "品牌名称": brand_data.get("name", "待命名品牌"),
            "主原型": primary_archetype.value,
            "主原型characteristics": self._get_archetype_features(primary_archetype),
            "次原型": secondary_archetype.value if secondary_archetype else None,
            "次原型characteristics": self._get_archetype_features(secondary_archetype) if secondary_archetype else None
        }
        
        # generate品牌故事框架
        brand_story = self._generate_brand_story(primary_archetype, brand_data)
        
        # generate视觉语言建议
        visual_suggestions = self._generate_visual_suggestion(primary_archetype)
        
        return {
            "品牌原型卡": brand_archetype_card,
            "品牌故事框架": brand_story,
            "视觉语言建议": visual_suggestions,
            "营销strategy建议": self._generate_marketing_strategy(primary_archetype, secondary_archetype)
        }
    
    def _recommend_archetype(self, industry: str, target: str, value: str) -> List[原型类型]:
        """推荐原型"""
        # 基于行业的推荐
        行业mapping = {
            "科技": [原型类型.发明家, 原型类型.智者],
            "时尚": [原型类型.情人, 原型类型.娱乐者],
            "运动": [原型类型.英雄, 原型类型.探险家],
            "金融": [原型类型.统治者, 原型类型.智者],
            "教育": [原型类型.智者, 原型类型.照顾者],
            "餐饮": [原型类型.情人, 原型类型.照顾者],
            "汽车": [原型类型.英雄, 原型类型.统治者]
        }
        
        for 行业关键词, 原型列表 in 行业mapping.items():
            if 行业关键词 in industry:
                return 原型列表
        
        return [原型类型.发明家, 原型类型.智者]
    
    def _generate_brand_story(self, archetype: 原型类型, brand_data: Dict) -> Dict:
        """generate品牌故事框架"""
        features = self.原型库[archetype]
        
        return {
            "故事起点": f"从前有一个{archetype.value}...",
            "核心主题": features.目标,
            "英雄之旅框架": {
                "平凡世界": "用户当前的困境或需求",
                "冒险召唤": "为什么用户需要这个品牌",
                "跨越门槛": "品牌如何帮助用户",
                "考验与盟友": "品牌与用户的关系发展",
                "最大危机": "品牌解决的问题有多深刻",
                "蜕变": "用户使用品牌后的改变",
                "回归": "用户获得的新生活"
            },
            "核心信息": f"让你成为{features.渴望}的自己"
        }
    
    def _generate_visual_suggestion(self, archetype: 原型类型) -> Dict:
        """generate视觉语言建议"""
        视觉mapping = {
            原型类型.纯真者: {"色调": "柔和,温暖", "imagery": "阳光,花朵", "字体": "圆润,友好"},
            原型类型.英雄: {"色调": "强烈,对比", "imagery": "山峰,火焰", "字体": "粗犷,有力"},
            原型类型.智者: {"色调": "深沉,智慧", "imagery": "书本,星空", "字体": "简洁,经典"},
            原型类型.情人: {"色调": "浪漫,柔美", "imagery": "玫瑰,月光", "字体": "优雅,流畅"}
        }
        
        return 视觉mapping.get(archetype, {
            "色调": "专业,信任",
            "imagery": "现代,简洁",
            "字体": "清晰,易读"
        })
    
    def _generate_marketing_strategy(self, primary, secondary) -> Dict:
        """generate营销strategy"""
        features = self.原型库[primary]
        
        return {
            "品牌定位": f"{primary.value}品牌 - {features.目标}",
            "核心诉求": features.渴望,
            "差异化": f"帮助用户克服{features.恐惧}的恐惧",
            "传播主题": self._generate_communication_theme(primary),
            "KPI": ["品牌认知度", "情感连接度", "用户忠诚度"]
        }
    
    def _generate_communication_theme(self, archetype: 原型类型) -> str:
        """generate传播主题"""
        主题mapping = {
            原型类型.英雄: "Just Do It - 战胜困难,证明自己",
            原型类型.发明家: "Think Different - 创新改变世界",
            原型类型.智者: "Don't Be Evil - 追求真理",
            原型类型.情人: "Because You're Worth It - 你值得拥有",
            原型类型.探险家: "Adventure Awaits - 探索未知"
        }
        return 主题mapping.get(archetype, f"成为更好的自己 - {archetype.value}")
    
    def analyze_shadow(self, user_data: Dict) -> Dict:
        """
        阴影分析 - recognize被压抑的特质
        
        Args:
            user_data: 用户数据
            
        Returns:
            阴影分析结果
        """
        behaviors = user_data.get("behaviors", [])
        正面特质 = user_data.get("positive_traits", [])
        
        # 简化分析:recognize正面特质对应的阴影
        阴影mapping = {
            "善良": "冷漠,自私",
            "勤奋": "过度工作,完美主义",
            "谦虚": "自我否定,缺乏自信",
            "宽容": "软弱,没有原则",
            "乐观": "盲目,不切实际"
        }
        
        阴影特质 = []
        for 特质 in 正面特质:
            if 特质 in 阴影mapping:
                阴影特质.append({
                    "正面特质": 特质,
                    "对应阴影": 阴影mapping[特质],
                    "整合建议": f"接受{阴影mapping[特质]}的部分特质,在适当场景下展现"
                })
        
        return {
            "recognize阴影": 阴影特质,
            "整合建议": self._generate_shadow_integration(阴影特质),
            "成长方向": "在保持优势的同时,适度接纳阴影特质"
        }
    
    def _generate_shadow_integration(self, 阴影特质: List[Dict]) -> str:
        """generate阴影整合建议"""
        if not 阴影特质:
            return "阴影特质不明显,继续保持自我"
        
        建议 = "整合阴影的步骤:\n"
        建议 += "1. 觉察:注意到自己压抑的特质\n"
        建议 += "2. 接纳:承认这是人性的一部分\n"
        建议 += "3. 转化:在适当场景下有意识地运用\n"
        建议 += "4. 平衡:找到正面特质和阴影的平衡点"
        
        return 建议
    
    def get_narrative_archetype(self, story_type: str) -> Dict:
        """
        get叙事原型
        
        Args:
            story_type: 故事类型
            
        Returns:
            叙事原型建议
        """
        叙事mapping = {
            "励志": {"原型": 原型类型.英雄, "核心": "克服障碍,实现成长"},
            "爱情": {"原型": 原型类型.情人, "核心": "追求真爱,克服距离"},
            "冒险": {"原型": 原型类型.探险家, "核心": "探索未知,发现自我"},
            "幽默": {"原型": 原型类型.娱乐者, "核心": "轻松愉快,讽刺现实"},
            "悬疑": {"原型": 原型类型.智者, "核心": "揭开真相,理解世界"}
        }
        
        叙事原型 = 叙事mapping.get(story_type, {"原型": 原型类型.英雄, "核心": "成长之旅"})
        
        return {
            "推荐原型": 叙事原型["原型"].value,
            "核心主题": 叙事原型["核心"],
            "故事结构建议": self._generate_story_structure(叙事原型["原型"]),
            "角色原型建议": self._suggest_characters(叙事原型["原型"])
        }
    
    def _generate_story_structure(self, archetype: 原型类型) -> List[str]:
        """generate故事结构"""
        return [
            "1. 设定:介绍主人公和其现状",
            "2. 触发:面临挑战或机遇",
            "3. 变化:主人公开始转变",
            "4. 高潮:面临最大考验",
            "5. 解决:成功或失败,新平衡建立"
        ]
    
    def _suggest_characters(self, archetype: 原型类型) -> List[str]:
        """建议角色"""
        return [
            f"英雄主角:体现{archetype.value}的特质",
            "导师:提供智慧和指引",
            "阴影对手:代表需要克服的障碍",
            "盟友:提供支持和帮助"
        ]

# 全局实例
jung_archetype_engine = 荣格原型引擎()
