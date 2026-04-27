"""
__all__ = [
    'analyze_character',
    'analyze_luyao_spirit',
    'analyze_moyan_style',
    'analyze_narrative',
    'analyze_text_narrative',
    'apply_magical_realism',
    'assess_resilience',
    'assess_situation_resilience',
    'create_multivoice_narrative',
    'generate_land_narrative',
    'get_comprehensive_analysis',
    'optimize_narrative_structure',
]

文学叙事智能增强引擎 v1.0
基于莫言,路遥深度学习研究(5篇文档)

核心能力:
1. 多声部叙事分析 - 莫言式多重视角编织
2. 苦难意识与韧性模型 - 路遥式生命韧性
3. 土地叙事与地域性 - 根植土地的叙事智慧
4. 魔幻现实fusion - 莫言式现实与幻想交织
5. 人物原型深度分析 - 经典人物性格模型
6. 叙事结构优化 - 叙事节奏与张力控制

版本:v1.0.0
更新:2026-04-02
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field

class NarrativeStyle(Enum):
    """叙事style类型"""
    MULTIVOICE = "多声部叙事"       # 莫言式多重视角
    REALIST = "现实主义"           # 路遥式现实主义
    MAGICAL_REALISM = "魔幻现实主义"  # 莫言式魔幻fusion
    LAND_ROOTED = "土地叙事"       # 根植土地的叙事
    STREAM_OF_CONSCIOUSNESS = "意识流"  # 内心独白

class HeroArchetype(Enum):
    """英雄/人物原型"""
    EARTH_BEARER = "土地承载者"     # 孙少平/孙少安式:默默承受,坚韧不拔
    REBELLIOUS_SOUL = "叛逆之魂"   # 余占鳌式:不羁野性,突破常规
    TRAGIC_SCHOLAR = "悲剧知识分子" # 方言之父式:知识分子的困境
    SUFFERING_WOMAN = "苦难女性"   # 巩俐/九儿式:在苦难中觉醒
    VILLAGE_SAGE = "乡村智者"     # 乡村中的智者原型

@dataclass
class NarrativeElement:
    """叙事元素"""
    perspective: str           # 叙事视角
    voice: str                # 叙事声音
    time_structure: str       # 时间结构(线性/倒叙/插叙/环形)
    space_setting: str        # 空间设定
    tone: str                 # 基调
    key_symbols: List[str]    # 核心imagery
    tension_points: List[str] # 张力节点

@dataclass
class CharacterProfile:
    """人物性格档案"""
    name: str
    archetype: HeroArchetype
    core_trait: str          # 核心性格characteristics
    motivation: str          # 内在动机
    conflict_type: str       # 核心冲突类型
    growth_arc: str          # 成长弧线
    earth_connection: float  # 与土地/根脉的连接度 (0-1)
    resilience_score: float  # 韧性评分 (0-1)

class LiteraryNarrativeEngine:
    """
    文学叙事智能增强引擎
    
    fusion莫言与路遥两大文学传统:
    - 莫言:多声部叙事,魔幻现实主义,感官盛宴,历史与现实的交织
    - 路遥:苦难美学,生命韧性,奋斗叙事,城乡二元对立
    
    核心价值:让系统具备深度叙事分析能力和人文洞察力
    """

    VERSION = "v1.0.0"
    
    def __init__(self):
        # === 莫言叙事系统 ===
        self.moyan_voices = {
            "第一人称回忆者": {
                "desc": "以第一人称回顾往事,带有强烈的情感色彩和主观judge",
                "technique": "时间跳跃,记忆碎片,情感评论穿插",
                "example": "我奶奶那年的高粱地,红得像血",
                "applicable": ["个人经历叙述", "家族历史", "情感回忆"]
            },
            "全知旁观者": {
                "desc": "以全知视角俯瞰故事,但刻意保留模糊和矛盾",
                "technique": "多人物内心独白切换,视角游移,信息不对称",
                "example": "没有人知道那天夜里究竟发生了什么",
                "applicable": ["复杂事件分析", "多角度解读", "群体叙事"]
            },
            "魔幻叙述者": {
                "desc": "在写实中植入超自然元素,模糊现实与幻想的边界",
                "technique": "通感描写,夸张变形,神话imagery融入日常",
                "example": "月亮像一块烧红的烙铁,烫伤了整个天空",
                "applicable": ["创意表达", "隐喻叙事", "文化寓言"]
            },
            "感官叙述者": {
                "desc": "通过五感的极致调动来构建叙事空间",
                "technique": "嗅觉/味觉/触觉/听觉/视觉的密集轰炸",
                "example": "空气里弥漫着高粱酒,泥土和血腥的混合味道",
                "applicable": ["场景描写", "氛围构建", "沉浸式叙事"]
            }
        }
        
        # === 路遥韧性模型 ===
        self.luyao_resilience_dimensions = {
            "苦难承受力": {
                "desc": "面对极度贫困和困境时的承受与转化能力",
                "levels": {
                    "崩溃": "被苦难完全击倒",
                    "忍受": "被动承受,不倒下但也不成长",
                    "转化": "将苦难转化为内在力量",
                    "超越": "在苦难中发现意义,成为精神财富"
                },
                "key_works": "<平凡的世界>孙少平煤矿记",
                "insight": "路遥的核心洞见:苦难本身没有价值,有价值的面对苦难的态度"
            },
            "奋斗驱动力": {
                "desc": "在资源极度匮乏的环境中保持向上攀登的内在动力",
                "levels": {
                    "无为": "接受命运安排,不思改变",
                    "挣扎": "试图改变但缺乏方向和毅力",
                    "坚持": "明确目标,持续努力",
                    "燃烧": "以生命为燃料的极致奋斗"
                },
                "key_works": "<平凡的世界>孙少安开砖窑",
                "insight": "路遥式奋斗:不是个人英雄主义,而是对命运的不屈服"
            },
            "情感深度": {
                "desc": "在苦难环境中保持的真挚情感和人性温度",
                "levels": {
                    "麻木": "苦难磨灭了情感",
                "保留": "在苦难中维持基本人情",
                "升华": "苦难反而加深了情感的深度",
                "悲悯": "从自身苦难出发,理解所有人类的苦难"
                },
                "key_works": "<人生>高加林与巧珍",
                "insight": "路遥的情感哲学:最深沉的爱往往诞生在最艰苦的环境中"
            },
            "精神信仰": {
                "desc": "在物质极度匮乏时支撑人的精神支柱",
                "levels": {
                    "空虚": "没有精神支柱,随波逐流",
                    "功利": "以物质为唯一追求",
                    "理想": "有超越物质的精神追求",
                    "信仰": "将精神追求作为生命的最高价值"
                },
                "key_works": "<平凡的世界>孙少平读书与思考",
                "insight": "路遥的信仰:通过读书和思考,人可以在精神上超越物质的束缚"
            }
        }
        
        # === 土地叙事模型 ===
        self.land_narrative_elements = {
            "高粱地": {
                "symbolism": ["生命力", "野性", "血与火的洗礼", "民族精神"],
                "author": "莫言",
                "usage": "表达原始的生命力量和不屈的反抗精神"
            },
            "黄土地": {
                "symbolism": ["苦难", "坚韧", "根脉", "母亲"],
                "author": "路遥",
                "usage": "表达与土地绑定的生存哲学和苦难美学"
            },
            "河流": {
                "symbolism": ["时间", "命运", "洗刷", "连接"],
                "dual_author": True,
                "usage": "表达时间的流逝和命运的不可抗逆"
            },
            "窑洞": {
                "symbolism": ["庇护", "贫穷", "温暖", "局限"],
                "author": "路遥",
                "usage": "表达物质贫乏中的精神温暖"
            },
            "集市": {
                "symbolism": ["权力", "欲望", "混乱", "生命力"],
                "author": "莫言",
                "usage": "表达社会生态的复杂和人性的多面"
            }
        }
        
        # === 叙事结构模式库 ===
        self.narrative_structures = {
            "环形结构": {
                "desc": "故事结尾回到开头,但在认知层面完成升华",
                "technique": "首尾呼应,时间闭环,视角反转",
                "examples": ["<红高粱家族>"],
                "effect": "制造宿命感和历史的循环感"
            },
            "双线并进": {
                "desc": "两条叙事线平行推进,最终交汇",
                "technique": "章节交替,人物命运对比,主题对话",
                "examples": ["<平凡的世界>兄弟线"],
                "effect": "通过对比深化主题"
            },
            "编年史式": {
                "desc": "按时间顺序推进,在宏大历史中嵌入个人命运",
                "technique": "时间跨度大,历史事件穿插,代际更替",
                "examples": ["<丰乳肥臀>"],
                "effect": "展现个人命运与历史洪流的关系"
            },
            "倒叙揭秘": {
                "desc": "从结果出发,逐步揭示过程和原因",
                "technique": "悬念设置,信息碎片化拼贴,多版本叙事",
                "examples": ["<檀香刑>"],
                "effect": "制造悬疑感和叙事张力"
            }
        }

    def analyze_narrative(self, text: str, style: NarrativeStyle = NarrativeStyle.REALIST) -> Dict:
        """
        分析给定文本的叙事characteristics
        
        Args:
            text: 待分析文本
            style: 叙事style参考
            
        Returns:
            包含叙事元素分析,优化建议,style匹配度的字典
        """
        analysis = {
            "style_reference": style.value,
            "detected_elements": self._detect_narrative_elements(text),
            "perspective_analysis": self._analyze_perspective(text),
            "rhythm_assessment": self._assess_rhythm(text),
            "suggestion": None,
            "confidence": 0.0
        }
        
        analysis["suggestion"] = self._generate_narrative_suggestions(
            analysis["detected_elements"], style
        )
        analysis["confidence"] = self._calculate_confidence(analysis)
        
        return analysis

    def create_multivoice_narrative(self, event: str, perspectives: List[str]) -> Dict:
        """
        创建多声部叙事(莫言模式)
        
        Args:
            event: 核心事件
            perspectives: 多个视角(人物/立场描述)
            
        Returns:
            多声部叙事结构
        """
        narrative = {
            "core_event": event,
            "voices": [],
            "tensions": [],
            "convergent_theme": self._find_convergent_theme(event, perspectives)
        }
        
        for i, perspective in enumerate(perspectives):
            voice = {
                "voice_id": i + 1,
                "perspective": perspective,
                "narrative_strategy": self._assign_voice_strategy(i, len(perspectives)),
                "key_details": self._extract_voice_details(event, perspective),
                "emotional_tone": self._determine_emotional_tone(perspective)
            }
            narrative["voices"].append(voice)
        
        # recognize视角间的张力
        for i in range(len(perspectives)):
            for j in range(i + 1, len(perspectives)):
                tension = self._identify_voice_tension(
                    perspectives[i], perspectives[j]
                )
                if tension:
                    narrative["tensions"].append({
                        "between": f"视角{i+1} vs 视角{j+1}",
                        "conflict_type": tension["type"],
                        "narrative_value": tension["value"]
                    })
        
        return narrative

    def assess_resilience(self, situation: str, context: Dict = None) -> Dict:
        """
        评估韧性(路遥模式)
        
        Args:
            situation: 当前困境描述
            context: 上下文信息
            
        Returns:
            韧性评估和成长建议
        """
        assessment = {
            "situation": situation,
            "dimensions": {},
            "overall_resilience": 0.0,
            "growth_strategy": [],
            "literary_parallel": None
        }
        
        total_score = 0.0
        dimension_count = len(self.luyao_resilience_dimensions)
        
        for dim_name, dim_info in self.luyao_resilience_dimensions.items():
            score = self._evaluate_dimension(situation, dim_name, context)
            assessment["dimensions"][dim_name] = {
                "score": score,
                "level": self._score_to_level(score, dim_info["levels"]),
                "insight": dim_info["insight"]
            }
            total_score += score
        
        assessment["overall_resilience"] = total_score / dimension_count
        assessment["growth_strategy"] = self._generate_resilience_strategies(
            assessment["dimensions"]
        )
        assessment["literary_parallel"] = self._find_literary_parallel(
            assessment["overall_resilience"], situation
        )
        
        return assessment

    def generate_land_narrative(self, theme: str, element: str = None) -> Dict:
        """
        generate土地叙事方案
        
        Args:
            theme: 核心主题
            element: 土地元素(可选,自动匹配最佳)
            
        Returns:
            土地叙事方案
        """
        if not element:
            element = self._match_land_element(theme)
        
        element_info = self.land_narrative_elements.get(element)
        if not element_info:
            return {"error": f"未知土地元素: {element}"}
        
        return {
            "theme": theme,
            "land_element": element,
            "symbolism": element_info["symbolism"],
            "narrative_approach": element_info["usage"],
            "key_scenes": self._generate_land_scenes(theme, element),
            "symbolic_layers": self._build_symbolic_layers(element_info["symbolism"], theme),
            "emotional_arc": self._design_emotional_arc(theme, element_info["symbolism"])
        }

    def analyze_character(self, character_desc: str) -> CharacterProfile:
        """
        深度分析人物原型
        
        Args:
            character_desc: 人物描述
            
        Returns:
            人物性格档案
        """
        archetype = self._identify_archetype(character_desc)
        
        return CharacterProfile(
            name=self._extract_name(character_desc),
            archetype=archetype,
            core_trait=self._extract_core_trait(character_desc, archetype),
            motivation=self._infer_motivation(character_desc, archetype),
            conflict_type=self._identify_conflict(character_desc),
            growth_arc=self._predict_growth_arc(character_desc, archetype),
            earth_connection=self._assess_earth_connection(character_desc),
            resilience_score=self._assess_character_resilience(character_desc)
        )

    def apply_magical_realism(self, text: str, intensity: str = "moderate") -> Dict:
        """
        对现实文本施加魔幻现实主义改造
        
        Args:
            text: 原始文本
            intensity: 强度 (subtle/moderate/intense)
            
        Returns:
            魔幻现实主义改造方案
        """
        techniques = {
            "subtle": {
                "desc": "轻度魔幻:在日常中嵌入一两个超自然细节",
                "methods": ["感官异常", "时间错位", "微妙预言"]
            },
            "moderate": {
                "desc": "中度魔幻:超自然元素与现实并存,边界模糊",
                "methods": ["通感描写", "变形imagery", "神话人物介入", "梦境侵入现实"]
            },
            "intense": {
                "desc": "重度魔幻:现实与超现实完全交融",
                "methods": ["鬼神叙事", "时间循环", "身份裂变", "生死界限消融"]
            }
        }
        
        config = techniques.get(intensity, techniques["moderate"])
        
        return {
            "original_text": text,
            "intensity": intensity,
            "technique_desc": config["desc"],
            "suggested_methods": config["methods"],
            "modifications": self._generate_magical_modifications(text, config["methods"]),
            "moyan_reference": self._find_moyan_reference(config["methods"])
        }

    def optimize_narrative_structure(self, story_outline: str) -> Dict:
        """
        优化叙事结构
        
        Args:
            story_outline: 故事大纲
            
        Returns:
            结构优化方案
        """
        current_structure = self._analyze_current_structure(story_outline)
        
        # 基于路遥和莫言的最佳实践提供建议
        recommendations = {
            "structure_type": current_structure,
            "strengths": self._identify_structure_strengths(current_structure),
            "weaknesses": self._identify_structure_weaknesses(current_structure),
            "optimization_options": self._suggest_structure_improvements(current_structure),
            "reference_works": self._match_reference_works(current_structure),
            "pacing_guide": self._generate_pacing_guide(story_outline)
        }
        
        return recommendations

    # === 莫言专题分析 ===
    
    def analyze_moyan_style(self, text: str) -> Dict:
        """
        分析文本中的莫言style_features
        
        Returns:
            莫言style各维度的匹配度分析
        """
        moyan_features = {
            "感官密度": self._analyze_sensory_density(text),
            "多声部程度": self._analyze_multivoice_degree(text),
            "魔幻元素浓度": self._analyze_magical_elements(text),
            "历史意识": self._analyze_historical_consciousness(text),
            "语言野性": self._analyze_wild_language(text),
            "民间文化嵌入": self._analyze_folk_culture(text)
        }
        
        return {
            "moyan_style_score": sum(moyan_features.values()) / len(moyan_features),
            "feature_details": moyan_features,
            "style_summary": self._summarize_moyan_style(moyan_features)
        }

    # === 路遥专题分析 ===
    
    def analyze_luyao_spirit(self, text: str) -> Dict:
        """
        分析文本中的路遥精神characteristics
        
        Returns:
            路遥精神各维度的分析
        """
        luyao_features = {
            "苦难意识": self._analyze_suffering_awareness(text),
            "奋斗精神": self._analyze_striving_spirit(text),
            "城乡矛盾": self._analyze_urban_rural_contradiction(text),
            "情感纯度": self._analyze_emotional_purity(text),
            "理想主义": self._analyze_idealism(text),
            "平民立场": self._analyze_civilian_stance(text)
        }
        
        return {
            "luyao_spirit_score": sum(luyao_features.values()) / len(luyao_features),
            "feature_details": luyao_features,
            "spirit_summary": self._summarize_luyao_spirit(luyao_features)
        }

    # === 内部方法 ===
    
    def _detect_narrative_elements(self, text: str) -> Dict:
        """检测叙事元素"""
        elements = {
            "has_dialogue": '"""' in text or "''" in text or '"' in text,
            "has_inner_thought": any(kw in text for kw in ["想", "觉得", "心中", "内心"]),
            "has_environment": any(kw in text for kw in ["天", "地", "风", "雨", "夜", "日"]),
            "has_action": any(kw in text for kw in ["走", "跑", "看", "说", "做", "打"]),
            "has_symbol": any(kw in text for kw in ["像", "仿佛", "如同", "好似"]),
            "has_time_shift": any(kw in text for kw in ["后来", "此前", "那时", "如今", "回忆"])
        }
        return elements
    
    def _analyze_perspective(self, text: str) -> Dict:
        """分析叙事视角"""
        first_person = text.count("我")
        third_person = text.count("他") + text.count("她")
        
        if first_person > third_person:
            return {"type": "第一人称", "depth": "深入"}
        elif third_person > first_person:
            return {"type": "第三人称", "depth": "全知/有限"}
        else:
            return {"type": "混合视角", "depth": "多声部倾向"}
    
    def _assess_rhythm(self, text: str) -> Dict:
        """评估叙事节奏"""
        length = len(text)
        sentences = text.count(".") + text.count("!") + text.count("?")
        avg_length = length / max(sentences, 1)
        
        if avg_length < 20:
            rhythm = "短促有力"
        elif avg_length < 40:
            rhythm = "中速流畅"
        else:
            rhythm = "悠长舒缓"
            
        return {"avg_sentence_length": avg_length, "rhythm": rhythm}
    
    def _generate_narrative_suggestions(self, elements: Dict, style: NarrativeStyle) -> str:
        """generate叙事优化建议"""
        suggestions = []
        
        if not elements.get("has_dialogue"):
            suggestions.append("建议增加对话,增强叙事生动性")
        if not elements.get("has_inner_thought"):
            suggestions.append("建议加入内心独白,深化人物心理")
        if not elements.get("has_symbol"):
            suggestions.append("建议使用象征imagery,提升文本层次")
            
        if style == NarrativeStyle.MULTIVOICE and elements.get("has_time_shift"):
            suggestions.append("多声部叙事配合时间跳跃效果更佳")
        elif style == NarrativeStyle.MAGICAL_REALISM and elements.get("has_environment"):
            suggestions.append("在环境描写中嵌入魔幻元素")
            
        return ";".join(suggestions) if suggestions else "叙事元素完整"
    
    def _calculate_confidence(self, analysis: Dict) -> float:
        """计算分析置信度"""
        elements = analysis.get("detected_elements", {})
        detected = sum(1 for v in elements.values() if v)
        return min(detected / max(len(elements), 1), 1.0)
    
    def _find_convergent_theme(self, event: str, perspectives: List[str]) -> str:
        """寻找多视角汇聚的主题"""
        return f"关于'{event}'的多维度审视"
    
    def _assign_voice_strategy(self, index: int, total: int) -> str:
        """分配叙事strategy"""
        strategies = ["回忆性叙述", "现场式描写", "评论性反思", "侧面暗示"]
        return strategies[index % len(strategies)]
    
    def _extract_voice_details(self, event: str, perspective: str) -> List[str]:
        """提取各视角的独特细节"""
        return [f"从'{perspective}'角度观察{event}的独特发现"]
    
    def _determine_emotional_tone(self, perspective: str) -> str:
        """确定情感基调"""
        positive_words = ["希望", "光明", "温暖", "爱", "善"]
        negative_words = ["痛苦", "愤怒", "悲伤", "恐惧", "恨"]
        
        pos = sum(1 for w in positive_words if w in perspective)
        neg = sum(1 for w in negative_words if w in perspective)
        
        if pos > neg:
            return "温暖/希望"
        elif neg > pos:
            return "沉重/痛苦"
        return "复杂/矛盾"
    
    def _identify_voice_tension(self, p1: str, p2: str) -> Optional[Dict]:
        """recognize视角间的张力"""
        return {"type": "认知冲突", "value": f"'{p1}'与'{p2}'构成对照视角"}
    
    def _evaluate_dimension(self, situation: str, dim_name: str, context: Dict = None) -> float:
        """评估韧性维度"""
        # 基于文本characteristics的简单评估
        positive_indicators = ["坚持", "努力", "不放弃", "克服", "突破", "成长"]
        negative_indicators = ["绝望", "放弃", "崩溃", "无法", "不可能"]
        
        pos = sum(1 for w in positive_indicators if w in situation)
        neg = sum(1 for w in negative_indicators if w in situation)
        
        base = 0.5 + (pos - neg) * 0.1
        return max(0.0, min(1.0, base))
    
    def _score_to_level(self, score: float, levels: Dict) -> str:
        """分数转等级"""
        level_keys = list(levels.keys())
        idx = min(int(score * len(level_keys)), len(level_keys) - 1)
        return level_keys[idx]
    
    def _generate_resilience_strategies(self, dimensions: Dict) -> List[str]:
        """generate韧性成长strategy"""
        strategies = []
        for dim_name, dim_data in dimensions.items():
            if dim_data["score"] < 0.6:
                strategies.append(f"[{dim_name}]需要重点强化:{dim_data['insight']}")
        return strategies if strategies else ["各项韧性metrics良好,保持当前状态"]
    
    def _find_literary_parallel(self, score: float, situation: str) -> Dict:
        """寻找文学对照"""
        parallels = {
            "孙少平": "从煤矿工人到精神贵族的蜕变--路遥<平凡的世界>",
            "孙少安": "从贫困农民到企业家的奋斗--路遥<平凡的世界>",
            "高加林": "在理想与现实的夹缝中挣扎--路遥<人生>",
            "余占鳌": "野性生命力的极致表达--莫言<红高粱家族>",
            "上官鲁氏": "苦难中孕育生命与希望的伟大母亲--莫言<丰乳肥臀>"
        }
        
        if score < 0.3:
            return {"character": "孙少平(早期)", "reference": parallels["孙少平"], "lesson": "在最黑暗的时刻,坚持读书和思考"}
        elif score < 0.6:
            return {"character": "高加林", "reference": parallels["高加林"], "lesson": "理想是必要的,但脚踏实地的选择同样重要"}
        else:
            return {"character": "孙少平(后期)", "reference": parallels["孙少平"], "lesson": "苦难终将成为人生最宝贵的财富"}
    
    def _match_land_element(self, theme: str) -> str:
        """匹配最佳土地元素"""
        theme_element_map = {
            "生命": "高粱地", "死亡": "河流", "苦难": "黄土地",
            "希望": "高粱地", "爱": "河流", "贫困": "窑洞",
            "欲望": "集市", "权力": "集市", "根脉": "黄土地"
        }
        for keyword, element in theme_element_map.items():
            if keyword in theme:
                return element
        return "黄土地"
    
    def _generate_land_scenes(self, theme: str, element: str) -> List[str]:
        """generate土地场景"""
        return [
            f"{element}的清晨:{theme}在晨光中萌芽",
            f"{element}的黄昏:{theme}在暮色中沉淀",
            f"{element}的风暴:{theme}经受最严酷的考验",
            f"{element}的重生:{theme}在废墟中新生"
        ]
    
    def _build_symbolic_layers(self, symbolism: List[str], theme: str) -> List[Dict]:
        """构建象征层次"""
        return [{"layer": i+1, "symbol": s, "connection_to_theme": f"{s}mapping{theme}的{['表层','深层','核心'][i%3]}含义"} 
                for i, s in enumerate(symbolism)]
    
    def _design_emotional_arc(self, theme: str, symbolism: List[str]) -> Dict:
        """设计情感弧线"""
        return {
            "opening": "沉稳/压抑",
            "development": "逐渐升温",
            "climax": "激烈/爆发",
            "resolution": "沉淀/升华",
            "closing_note": f"以{symbolism[0] if symbolism else '自然'}的imagery收束"
        }
    
    def _identify_archetype(self, desc: str) -> HeroArchetype:
        """recognize人物原型"""
        archetypes_map = {
            HeroArchetype.EARTH_BEARER: ["坚持", "承受", "努力", "踏实", "农民", "底层"],
            HeroArchetype.REBELLIOUS_SOUL: ["叛逆", "不羁", "反抗", "野性", "冲动"],
            HeroArchetype.TRAGIC_SCHOLAR: ["知识", "思想", "困境", "矛盾", "挣扎"],
            HeroArchetype.SUFFERING_WOMAN: ["女性", "苦难", "觉醒", "坚强", "母亲"],
            HeroArchetype.VILLAGE_SAGE: ["智慧", "乡村", "老人", "传统", "经验"]
        }
        
        for archetype, keywords in archetypes_map.items():
            if any(kw in desc for kw in keywords):
                return archetype
        return HeroArchetype.EARTH_BEARER
    
    def _extract_name(self, desc: str) -> str:
        """提取人物名称"""
        return desc[:min(len(desc), 20)]
    
    def _extract_core_trait(self, desc: str, archetype: HeroArchetype) -> str:
        """提取核心characteristics"""
        trait_map = {
            HeroArchetype.EARTH_BEARER: "坚韧不拔",
            HeroArchetype.REBELLIOUS_SOUL: "不羁野性",
            HeroArchetype.TRAGIC_SCHOLAR: "思想挣扎",
            HeroArchetype.SUFFERING_WOMAN: "苦难中觉醒",
            HeroArchetype.VILLAGE_SAGE: "民间智慧"
        }
        return trait_map.get(archetype, "待分析")
    
    def _infer_motivation(self, desc: str, archetype: HeroArchetype) -> str:
        """推断内在动机"""
        motivation_map = {
            HeroArchetype.EARTH_BEARER: "改变命运,守护家庭",
            HeroArchetype.REBELLIOUS_SOUL: "追求自由,反抗压迫",
            HeroArchetype.TRAGIC_SCHOLAR: "寻求真理,安放灵魂",
            HeroArchetype.SUFFERING_WOMAN: "保护后代,赢得尊严",
            HeroArchetype.VILLAGE_SAGE: "传承智慧,维系社群"
        }
        return motivation_map.get(archetype, "未知")
    
    def _identify_conflict(self, desc: str) -> str:
        """recognize核心冲突"""
        conflicts = ["人与命运的冲突", "人与社会的冲突", "人与自我的冲突", 
                     "人与自然的冲突", "传统与现代的冲突"]
        return conflicts[hash(desc) % len(conflicts)]
    
    def _predict_growth_arc(self, desc: str, archetype: HeroArchetype) -> str:
        """预测成长弧线"""
        arc_map = {
            HeroArchetype.EARTH_BEARER: "从默默承受到主动改变",
            HeroArchetype.REBELLIOUS_SOUL: "从盲目反抗到有方向地战斗",
            HeroArchetype.TRAGIC_SCHOLAR: "从迷茫挣扎到精神超越",
            HeroArchetype.SUFFERING_WOMAN: "从被动受苦到主动觉醒",
            HeroArchetype.VILLAGE_SAGE: "从经验积累到智慧传承"
        }
        return arc_map.get(archetype, "待分析")
    
    def _assess_earth_connection(self, desc: str) -> float:
        """评估与土地的连接度"""
        earth_keywords = ["土地", "农村", "乡村", "家乡", "故乡", "农田", "庄稼"]
        count = sum(1 for kw in earth_keywords if kw in desc)
        return min(count * 0.2, 1.0)
    
    def _assess_character_resilience(self, desc: str) -> float:
        """评估人物韧性"""
        resilience_keywords = ["坚持", "不屈", "忍耐", "坚强", "勇敢"]
        count = sum(1 for kw in resilience_keywords if kw in desc)
        return min(0.3 + count * 0.15, 1.0)
    
    def _generate_magical_modifications(self, text: str, methods: List[str]) -> List[Dict]:
        """generate魔幻改造建议"""
        return [{"method": m, "suggestion": f"在叙述中嵌入'{m}'元素"} for m in methods]
    
    def _find_moyan_reference(self, methods: List[str]) -> str:
        """寻找莫言作品参考"""
        if "鬼神叙事" in methods:
            return "参考<生死疲劳>中的六道轮回叙事"
        elif "变形imagery" in methods:
            return "参考<透明的红萝卜>中的感官变形"
        return "参考<红高粱家族>中的历史魔幻叙事"
    
    def _analyze_current_structure(self, outline: str) -> str:
        """分析当前叙事结构"""
        if "章" in outline or "节" in outline:
            return "编年史式"
        elif "回忆" in outline or "回到" in outline:
            return "环形结构"
        elif "同时" in outline or "另一边" in outline:
            return "双线并进"
        return "线性叙事"
    
    def _identify_structure_strengths(self, structure: str) -> List[str]:
        """recognize结构优势"""
        strengths_map = {
            "编年史式": ["历史纵深感强", "人物成长轨迹清晰"],
            "环形结构": ["首尾呼应有张力", "命运感强烈"],
            "双线并进": ["对比效果突出", "主题多维度展开"],
            "线性叙事": ["节奏清晰", "读者容易跟随"]
        }
        return strengths_map.get(structure, [])
    
    def _identify_structure_weaknesses(self, structure: str) -> List[str]:
        """recognize结构弱点"""
        weaknesses_map = {
            "编年史式": ["可能冗长", "重点不够突出"],
            "环形结构": ["需要精心设计", "首尾衔接要求高"],
            "双线并进": ["切换可能生硬", "需要平衡两条线"],
            "线性叙事": ["可能平淡", "缺少叙事张力"]
        }
        return weaknesses_map.get(structure, [])
    
    def _suggest_structure_improvements(self, structure: str) -> List[str]:
        """建议结构改进"""
        improvements_map = {
            "编年史式": ["在关键节点设置高潮", "穿插回忆或预叙增加层次"],
            "环形结构": ["确保结尾的认知升华", "设置视角反转"],
            "双线并进": ["找到最佳交汇点", "在交汇处制造冲突"],
            "线性叙事": ["设置悬念和反转", "增加倒叙或插叙"]
        }
        return improvements_map.get(structure, [])
    
    def _match_reference_works(self, structure: str) -> List[str]:
        """匹配参考作品"""
        works_map = {
            "编年史式": ["<丰乳肥臀>- 莫言", "<平凡的世界>- 路遥"],
            "环形结构": ["<红高粱家族>- 莫言"],
            "双线并进": ["<平凡的世界>- 路遥"],
            "线性叙事": ["<人生>- 路遥"]
        }
        return works_map.get(structure, [])
    
    def _generate_pacing_guide(self, outline: str) -> Dict:
        """generate节奏指南"""
        return {
            "opening": "慢节奏建立背景和人物",
            "rising": "逐步加速,插入冲突",
            "climax": "最高速,最大张力",
            "falling": "减速,情感沉淀",
            "resolution": "从容收束,留有余韵"
        }
    
    # 莫言style分析
    
    def _analyze_sensory_density(self, text: str) -> float:
        """分析感官密度"""
        sensory_words = ["红", "黑", "白", "香", "臭", "冷", "热", "苦", "甜", "酸", 
                         "声音", "光线", "触", "味", "嗅", "响", "亮"]
        count = sum(1 for w in sensory_words if w in text)
        return min(count * 0.08, 1.0)
    
    def _analyze_multivoice_degree(self, text: str) -> float:
        """分析多声部程度"""
        voices = text.count("我") + text.count("他") + text.count("她")
        return min(voices * 0.05, 1.0)
    
    def _analyze_magical_elements(self, text: str) -> float:
        """分析魔幻元素浓度"""
        magical_words = ["鬼", "神", "妖", "魔", "仙", "灵", "梦", "幻", "魂"]
        count = sum(1 for w in magical_words if w in text)
        return min(count * 0.1, 1.0)
    
    def _analyze_historical_consciousness(self, text: str) -> float:
        """分析历史意识"""
        historical_words = ["历史", "年代", "战争", "革命", "朝代", "时代"]
        count = sum(1 for w in historical_words if w in text)
        return min(count * 0.15, 1.0)
    
    def _analyze_wild_language(self, text: str) -> float:
        """分析语言野性"""
        wild_words = ["血", "肉", "骨头", "怒吼", "嚎叫", "疯狂", "撕咬"]
        count = sum(1 for w in wild_words if w in text)
        return min(count * 0.12, 1.0)
    
    def _analyze_folk_culture(self, text: str) -> float:
        """分析民间文化嵌入"""
        folk_words = ["庙", "祭", "巫", "咒", "年", "节", "俗", "乡"]
        count = sum(1 for w in folk_words if w in text)
        return min(count * 0.12, 1.0)
    
    def _summarize_moyan_style(self, features: Dict) -> str:
        """总结莫言style"""
        dominant = max(features, key=features.get)
        summaries = {
            "感官密度": "感官描写丰富,典型的莫言式体验叙事",
            "多声部程度": "多重视角交织,具有莫言式叙事复杂性",
            "魔幻元素浓度": "魔幻与现实交融,接近莫言式魔幻现实主义",
            "历史意识": "强烈的历史关怀,具有莫言式宏大叙事",
            "语言野性": "语言具有原始野性力量,莫言式生命呐喊",
            "民间文化嵌入": "民间文化根植深厚,莫言式乡土叙事"
        }
        return summaries.get(dominant, "synthesize莫言style_features")
    
    # 路遥精神分析
    
    def _analyze_suffering_awareness(self, text: str) -> float:
        """分析苦难意识"""
        words = ["苦", "难", "穷", "贫", "挣扎", "煎熬", "受罪"]
        count = sum(1 for w in words if w in text)
        return min(count * 0.12, 1.0)
    
    def _analyze_striving_spirit(self, text: str) -> float:
        """分析奋斗精神"""
        words = ["奋斗", "努力", "拼搏", "奋斗", "不屈", "坚持"]
        count = sum(1 for w in words if w in text)
        return min(count * 0.15, 1.0)
    
    def _analyze_urban_rural_contradiction(self, text: str) -> float:
        """分析城乡矛盾"""
        words = ["城", "乡", "农村", "城市", "回乡", "进城"]
        count = sum(1 for w in words if w in text)
        return min(count * 0.15, 1.0)
    
    def _analyze_emotional_purity(self, text: str) -> float:
        """analyze_emotion纯度"""
        words = ["纯真", "真挚", "善良", "温暖", "爱", "情"]
        count = sum(1 for w in words if w in text)
        return min(count * 0.1, 1.0)
    
    def _analyze_idealism(self, text: str) -> float:
        """分析理想主义"""
        words = ["理想", "梦想", "希望", "信念", "追求", "未来"]
        count = sum(1 for w in words if w in text)
        return min(count * 0.12, 1.0)
    
    def _analyze_civilian_stance(self, text: str) -> float:
        """分析平民立场"""
        words = ["农民", "工人", "普通人", "平民", "底层", "百姓"]
        count = sum(1 for w in words if w in text)
        return min(count * 0.15, 1.0)
    
    def _summarize_luyao_spirit(self, features: Dict) -> str:
        """总结路遥精神"""
        dominant = max(features, key=features.get)
        summaries = {
            "苦难意识": "强烈的苦难意识,路遥式苦难美学",
            "奋斗精神": "不屈的奋斗精神,路遥式生命力量",
            "城乡矛盾": "深刻的城乡矛盾书写,路遥式社会关怀",
            "情感纯度": "纯真深厚的情感表达,路遥式人情温度",
            "理想主义": "执着的理想主义追求,路遥式精神高度",
            "平民立场": "坚定的平民立场,路遥式人民性"
        }
        return summaries.get(dominant, "synthesize路遥精神characteristics")

    def get_comprehensive_analysis(self, text: str) -> Dict:
        """
        synthesize分析:同时运用莫言和路遥两大维度
        
        Returns:
            完整的双维度文学分析报告
        """
        return {
            "moyan_dimension": self.analyze_moyan_style(text),
            "luyao_dimension": self.analyze_luyao_spirit(text),
            "narrative_analysis": self.analyze_narrative(text),
            "synthesis": self._synthesize_analysis(text),
            "recommendation": self._generate_reading_recommendation(text)
        }
    
    def _synthesize_analysis(self, text: str) -> str:
        """synthesize分析结论"""
        moyan_score = self._analyze_sensory_density(text)
        luyao_score = self._analyze_suffering_awareness(text)
        
        if moyan_score > luyao_score:
            return "文本偏向莫言style:强调感官体验和叙事复杂性"
        elif luyao_score > moyan_score:
            return "文本偏向路遥style:强调苦难意识和生命韧性"
        return "文本fusion了莫言的感官力量和路遥的精神深度"
    
    def _generate_reading_recommendation(self, text: str) -> str:
        """generate延伸阅读建议"""
        return "建议延伸阅读:莫言<红高粱家族>+ 路遥<平凡的世界>,理解中国文学的两大地标性叙事传统"

# 便捷函数
def analyze_text_narrative(text: str, style: str = "realist") -> Dict:
    """便捷函数:快速叙事分析"""
    engine = LiteraryNarrativeEngine()
    style_map = {
        "realist": NarrativeStyle.REALIST,
        "multivoice": NarrativeStyle.MULTIVOICE,
        "magical_realism": NarrativeStyle.MAGICAL_REALISM,
        "land_rooted": NarrativeStyle.LAND_ROOTED
    }
    return engine.analyze_narrative(text, style_map.get(style, NarrativeStyle.REALIST))

def assess_situation_resilience(situation: str) -> Dict:
    """便捷函数:快速韧性评估"""
    engine = LiteraryNarrativeEngine()
    return engine.assess_resilience(situation)
