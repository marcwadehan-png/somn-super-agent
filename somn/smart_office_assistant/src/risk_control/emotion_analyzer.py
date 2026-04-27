"""
__all__ = [
    'analyze',
    'quick_check',
]

情绪健康度分析器 - Emotion Health Analyzer

分析营销内容的情绪健康度,检测焦虑贩卖,恐惧营销等不健康情绪引导
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    """风险等级 - 放宽后:非安全/质量/功效类营销降级处理"""
    P0 = "致命"      # 安全/质量/功效虚假声明,严重违规
    P1 = "高危"      # 一般行业的情绪过度表达
    P2 = "中危"      # 同质化内容,模糊承诺
    P3 = "低危"      # 一般情绪表达
    P4 = "安全"      # 夸张修辞,主观表达
    PASS = "通过"    # 无风险

@dataclass
class EmotionAnalysisResult:
    """情绪分析结果"""
    health_score: float           # 健康度评分 0-100
    risk_level: RiskLevel         # 风险等级
    anxiety_score: float          # 焦虑指数 0-100
    fear_score: float             # 恐惧指数 0-100
    negative_ratio: float         # 负面占比 0-1
    solution_focus: float         # 解决导向 0-100
    hope_score: float             # 希望指数 0-100
    detected_issues: List[Dict]   # 检测到的问题
    suggestions: List[str]        # 改进建议

class EmotionHealthAnalyzer:
    """情绪健康度分析器 - 支持分级管理和行业差异化"""
    
    # 行业类型
    INDUSTRY_GENERAL = "general"      # 一般行业
    INDUSTRY_HEALTH = "health"        # 健康/保健行业
    INDUSTRY_EDUCATION = "education"  # 教育行业
    INDUSTRY_FINANCE = "finance"      # 金融行业
    
    # 客观问题呈现(P3 - 正常,但需结合行业judge)
    OBJECTIVE_ISSUES = {
        "职场": ["35岁", "中年危机", "职业转型", "职场瓶颈", "晋升困难"],
        "健康": ["熬夜", "久坐", "亚健康", "免疫力下降", "作息不规律"],
        "教育": ["升学压力", "竞争激烈", "教育资源"],
        "经济": ["通货膨胀", "物价上涨", "经济下行"]
    }
    
    # 焦虑营销关键词库 - 分级管理(放宽后)
    ANXIETY_KEYWORDS = {
        "P0": [  # 绝对禁止 - 仅安全/质量/功效虚假声明
            "必死", "必败", "必然失败", "注定完蛋", "毫无希望",
            "100%治愈", "保证治愈", "绝对安全", "无副作用"  # 功效/安全虚假声明
        ],
        "P1": [  # 高危 - 降级为一般行业P2
            "再不", "就晚了", "来不及了", "最后机会", "错过",
            "后悔", "输在起跑线", "被时代抛弃", "落后", "淘汰",
            "危机", "危险", "警告", "必须", "不得不",
            "唯一机会", "最后期限", "倒计时", "紧急", "刻不容缓"
        ],
        "P2": [  # 中危 - 降级为一般行业P3
            "焦虑", "压力", "担心", "害怕", "恐惧",
            "不安", "紧张", "困扰", "烦恼", "痛苦"
        ],
        "P3": [  # 低危 - 一般情绪表达
            "挑战", "困难", "问题", "障碍", "瓶颈"
        ],
        "P4": [  # 安全 - 夸张修辞允许
            "火爆", "爆棚", "疯抢", "热销", "爆品"
        ]
    }
    
    # 恐惧营销关键词库 - 分级管理 + 行业差异化(放宽后)
    FEAR_KEYWORDS = {
        "P0": {  # 绝对禁止 - 仅安全/健康/功效虚假声明
            "general": ["100%有效", "保证治愈", "绝对安全", "无副作用"],
            "health": ["必死", "必得癌症", "必然致病", "不治之症", "药到病除", "根治"],
            "education": ["包过", "包拿证", "保录取"],
            "finance": ["保本保息", "稳赚不赔", "零风险", "无风险"]
        },
        "P1": {  # 高危 - 一般行业降级为P2
            "general": [
                "毁掉", "毁了", "毁掉健康", "毁掉家庭", "毁掉事业",
                "可怕", "恐怖", "惊悚", "震惊", "骇人听闻"
            ],
            "health": [
                "致癌", "致命", "死亡", "绝症", "无药可救"
            ],
            "education": [
                "毁掉孩子", "毁掉前途", "毁了未来", "毁掉一生"
            ]
        },
        "P2": {  # 中危 - 一般行业降级为P3
            "general": [
                "疾病", "灾难", "悲剧", "崩溃", "绝望", "无助", "完蛋"
            ],
            "health": [
                "生病", "患病", "健康问题"
            ],
            "education": [
                "落后", "跟不上", "被淘汰"
            ]
        },
        "P4": {  # 安全 - 夸张修辞允许
            "general": [
                "震撼", "惊艳", "逆天", "封神", "绝了",
                "爆款", "爆品", "卖疯了", "抢疯了"
            ],
            "health": [],
            "education": [],
            "finance": []
        }
    }
    
    # 行业敏感词升级规则
    INDUSTRY_ESCALATION = {
        "health": {
            "P3": ["熬夜", "致癌", "致命", "死亡", "疾病"],  # 一般行业P3,健康行业P2/P1
            "P2": ["免疫力下降", "健康风险", "亚健康"]       # 一般行业P2,健康行业P1
        },
        "education": {
            "P3": ["升学压力", "竞争激烈"],  # 一般行业P3,教育行业P2
            "P2": ["输在起跑线", "落后"]     # 一般行业P2,教育行业P1
        }
    }
    
    # 羞耻感营销关键词 - 放宽后降级处理
    SHAME_KEYWORDS = [
        "太落伍", "太out", "土", "low", "丢人",
        "丢脸", "没面子", "被人嘲笑", "被人看不起",
        "连这个都不知道", "太无知", "太愚蠢"
    ]
    
    # 社会排斥关键词 - 放宽后降级处理
    EXCLUSION_KEYWORDS = [
        "被抛弃", "被孤立", "被边缘化", "不合群",
        "跟不上", "out了", "过时了", "老土"
    ]
    
    # P4级允许的主观夸张表达
    SUBJECTIVE_HYPE = [
        "最美", "最好", "极致", "顶级", "巅峰",
        "封神", "逆天", "绝了", "yyds", "神作",
        " masterpiece", "完美", "无可挑剔", "无懈可击"
    ]
    
    # 正面解决导向关键词
    SOLUTION_KEYWORDS = [
        "解决方案", "方法", "技巧", "建议", "帮助",
        "改善", "提升", "优化", "进步", "成长",
        "实现", "达成", "成功", "突破", "创新"
    ]
    
    # 希望启发关键词
    HOPE_KEYWORDS = [
        "希望", "可能", "机会", "潜力", "未来",
        "美好", "精彩", "值得", "期待", "信心",
        "相信", "坚持", "努力", "奋斗", "梦想"
    ]
    
    def __init__(self):
        self._compile_patterns()
    
    def _compile_patterns(self):
        """编译正则表达式模式"""
        # 基础模式(一般行业)
        self.patterns = {
            "anxiety_p0": re.compile(r'(' + '|'.join(self.ANXIETY_KEYWORDS["P0"]) + r')', re.IGNORECASE),
            "anxiety_p1": re.compile(r'(' + '|'.join(self.ANXIETY_KEYWORDS["P1"]) + r')', re.IGNORECASE),
            "anxiety_p2": re.compile(r'(' + '|'.join(self.ANXIETY_KEYWORDS["P2"]) + r')', re.IGNORECASE),
            "fear_p0_general": re.compile(r'(' + '|'.join(self.FEAR_KEYWORDS["P0"]["general"]) + r')', re.IGNORECASE),
            "fear_p1_general": re.compile(r'(' + '|'.join(self.FEAR_KEYWORDS["P1"]["general"]) + r')', re.IGNORECASE),
            "fear_p2_general": re.compile(r'(' + '|'.join(self.FEAR_KEYWORDS["P2"]["general"]) + r')', re.IGNORECASE),
            "shame": re.compile(r'(' + '|'.join(self.SHAME_KEYWORDS) + r')', re.IGNORECASE),
            "exclusion": re.compile(r'(' + '|'.join(self.EXCLUSION_KEYWORDS) + r')', re.IGNORECASE),
            "solution": re.compile(r'(' + '|'.join(self.SOLUTION_KEYWORDS) + r')', re.IGNORECASE),
            "hope": re.compile(r'(' + '|'.join(self.HOPE_KEYWORDS) + r')', re.IGNORECASE),
        }
        
        # 客观问题呈现模式
        self.objective_issue_patterns = {}
        for category, keywords in self.OBJECTIVE_ISSUES.items():
            self.objective_issue_patterns[category] = re.compile(
                r'(' + '|'.join(keywords) + r')', re.IGNORECASE
            )
    
    def analyze(self, content: str, industry: str = "general") -> EmotionAnalysisResult:
        """
        分析内容的情绪健康度 - 支持行业差异化
        
        Args:
            content: 待分析的内容文本
            industry: 行业类型 (general/health/education/finance)
            
        Returns:
            EmotionAnalysisResult: 分析结果
        """
        # 各项评分计算
        anxiety_score = self._calculate_anxiety_score(content)
        fear_score = self._calculate_fear_score(content, industry)
        negative_ratio = self._calculate_negative_ratio(content)
        solution_focus = self._calculate_solution_focus(content)
        hope_score = self._calculate_hope_score(content)
        objective_issue_score = self._calculate_objective_issue_score(content)
        
        # synthesize健康度评分
        health_score = self._calculate_health_score(
            anxiety_score, fear_score, negative_ratio,
            solution_focus, hope_score, objective_issue_score
        )
        
        # 风险等级判定(带行业差异化)
        risk_level = self._determine_risk_level(
            health_score, anxiety_score, fear_score, content, industry
        )
        
        # 检测问题
        detected_issues = self._detect_issues(content, industry)
        
        # generate建议
        suggestions = self._generate_suggestions(
            anxiety_score, fear_score, solution_focus, hope_score, objective_issue_score
        )
        
        return EmotionAnalysisResult(
            health_score=health_score,
            risk_level=risk_level,
            anxiety_score=anxiety_score,
            fear_score=fear_score,
            negative_ratio=negative_ratio,
            solution_focus=solution_focus,
            hope_score=hope_score,
            detected_issues=detected_issues,
            suggestions=suggestions
        )
    

    
    def _calculate_anxiety_score(self, content: str) -> float:
        """计算焦虑指数"""
        p1_matches = len(self.patterns["anxiety_p1"].findall(content))
        p2_matches = len(self.patterns["anxiety_p2"].findall(content))
        
        # P1关键词权重更高
        score = min(100, p1_matches * 15 + p2_matches * 8)
        return score
    
    def _calculate_fear_score(self, content: str, industry: str = "general") -> float:
        """计算恐惧指数 - 支持行业差异化"""
        # get行业特定的关键词
        fear_p0_keywords = self.FEAR_KEYWORDS["P0"].get(industry, self.FEAR_KEYWORDS["P0"]["general"])
        fear_p1_keywords = self.FEAR_KEYWORDS["P1"].get(industry, self.FEAR_KEYWORDS["P1"]["general"])
        fear_p2_keywords = self.FEAR_KEYWORDS["P2"].get(industry, self.FEAR_KEYWORDS["P2"]["general"])
        
        # 编译行业特定模式
        p0_pattern = re.compile(r'(' + '|'.join(fear_p0_keywords) + r')', re.IGNORECASE)
        p1_pattern = re.compile(r'(' + '|'.join(fear_p1_keywords) + r')', re.IGNORECASE)
        p2_pattern = re.compile(r'(' + '|'.join(fear_p2_keywords) + r')', re.IGNORECASE)
        
        p0_matches = len(p0_pattern.findall(content))
        p1_matches = len(p1_pattern.findall(content))
        p2_matches = len(p2_pattern.findall(content))
        
        # P0权重最高,P1次之,P2最低
        score = min(100, p0_matches * 30 + p1_matches * 20 + p2_matches * 10)
        return score
    
    def _calculate_negative_ratio(self, content: str, industry: str = "general") -> float:
        """计算负面词汇占比 - 支持行业差异化"""
        # 基础负面词
        negative_words = self.ANXIETY_KEYWORDS["P1"] + self.ANXIETY_KEYWORDS["P2"]
        
        # 添加行业特定的负面词
        fear_p1 = self.FEAR_KEYWORDS["P1"].get(industry, self.FEAR_KEYWORDS["P1"]["general"])
        fear_p2 = self.FEAR_KEYWORDS["P2"].get(industry, self.FEAR_KEYWORDS["P2"]["general"])
        negative_words += fear_p1 + fear_p2
        
        words = content.split()
        if not words:
            return 0.0
        
        negative_count = sum(1 for word in words if any(nw in word for nw in negative_words))
        ratio = negative_count / len(words)
        
        return min(1.0, ratio * 5)  # 放大系数
    
    def _calculate_objective_issue_score(self, content: str) -> float:
        """计算客观问题呈现得分 - 区分客观陈述与焦虑贩卖"""
        score = 0
        matched_categories = []
        
        for category, pattern in self.objective_issue_patterns.items():
            matches = len(pattern.findall(content))
            if matches > 0:
                score += matches * 5  # 每个匹配加5分
                matched_categories.append(category)
        
        # 检查是否伴随解决方案
        solution_matches = len(self.patterns["solution"].findall(content))
        if solution_matches > 0 and score > 0:
            # 有客观问题 + 有解决方案 = 加分
            score += 20
        
        return min(100, score)
    
    def _calculate_solution_focus(self, content: str) -> float:
        """计算解决导向得分"""
        matches = len(self.patterns["solution"].findall(content))
        score = min(100, matches * 10 + 30)  # 基础分30
        return score
    
    def _calculate_hope_score(self, content: str) -> float:
        """计算希望指数"""
        matches = len(self.patterns["hope"].findall(content))
        score = min(100, matches * 8 + 25)  # 基础分25
        return score
    
    def _calculate_health_score(self, anxiety: float, fear: float, 
                                negative: float, solution: float, 
                                hope: float, objective_issue: float = 0) -> float:
        """计算synthesize健康度评分 - 考虑客观问题呈现"""
        # 基础评分
        base_score = (
            (100 - anxiety) * 0.20 +
            (100 - fear) * 0.20 +
            (1 - negative) * 100 * 0.15 +
            solution * 0.15 +
            hope * 0.15
        )
        
        # 客观问题呈现加分(如果是合理的客观陈述而非焦虑贩卖)
        if objective_issue > 0 and solution > 50:
            # 有客观问题 + 有解决方案 = 健康的内容
            base_score += objective_issue * 0.15
        
        return max(0, min(100, base_score))
    
    def _determine_risk_level(self, health_score: float, 
                              anxiety_score: float, fear_score: float,
                              content: str, industry: str = "general") -> RiskLevel:
        """
        确定风险等级 - 支持行业差异化 + 风控放宽
        
        风控放宽原则:
        - 严格管控(维持原等级):涉及安全,质量,产品功效的声明
        - 放宽管控(降级处理):一般情绪营销,夸张修辞,主观表达
        """
        is_critical_industry = industry in ["health", "medical", "finance", "education"]
        
        # 检查P0级别违规(安全/质量/功效虚假声明 - 所有行业严格管控)
        p0_matches = len(self.patterns["anxiety_p0"].findall(content))
        if p0_matches > 0:
            return RiskLevel.P0
        
        # 检查行业特定的P0违规
        fear_p0_keywords = self.FEAR_KEYWORDS["P0"].get(industry, [])
        if fear_p0_keywords:
            p0_fear_pattern = re.compile(r'(' + '|'.join(fear_p0_keywords) + r')', re.IGNORECASE)
            if len(p0_fear_pattern.findall(content)) > 0:
                return RiskLevel.P0
        
        # 检查P4级别(安全 - 夸张修辞,主观表达)
        hype_matches = sum(1 for word in self.SUBJECTIVE_HYPE if word in content)
        if hype_matches > 0 and anxiety_score < 30 and fear_score < 30:
            return RiskLevel.P4
        
        # 非关键行业:风控等级降级处理
        if not is_critical_industry:
            # 原P1降级为P2
            if anxiety_score >= 60 or fear_score >= 60:
                return RiskLevel.P2
            
            # 羞耻感和社会排斥降级为P2
            shame_matches = len(self.patterns["shame"].findall(content))
            exclusion_matches = len(self.patterns["exclusion"].findall(content))
            if shame_matches > 0 or exclusion_matches > 0:
                return RiskLevel.P2
            
            # 根据健康度评分判定(降级后)
            if health_score >= 80:
                return RiskLevel.PASS
            elif health_score >= 60:
                return RiskLevel.P4  # 原P3降为P4
            elif health_score >= 40:
                return RiskLevel.P3  # 原P2降为P3
            else:
                return RiskLevel.P2  # 原P1降为P2
        
        # 关键行业:维持原有严格管控
        else:
            # 检查P1级别违规
            if anxiety_score >= 60 or fear_score >= 60:
                return RiskLevel.P1
            
            # 检查羞耻感和社会排斥
            shame_matches = len(self.patterns["shame"].findall(content))
            exclusion_matches = len(self.patterns["exclusion"].findall(content))
            if shame_matches > 0 or exclusion_matches > 0:
                return RiskLevel.P1
            
            # 检查行业敏感词升级
            if industry in self.INDUSTRY_ESCALATION:
                escalation_rules = self.INDUSTRY_ESCALATION[industry]
                
                # 检查P3升级P2的词
                for word in escalation_rules.get("P3", []):
                    if word in content:
                        return RiskLevel.P2
                
                # 检查P2升级P1的词
                for word in escalation_rules.get("P2", []):
                    if word in content:
                        return RiskLevel.P1
            
            # 根据健康度评分判定
            if health_score >= 80:
                return RiskLevel.PASS
            elif health_score >= 60:
                return RiskLevel.P3
            elif health_score >= 40:
                return RiskLevel.P2
            else:
                return RiskLevel.P1
    
    def _detect_issues(self, content: str, industry: str = "general") -> List[Dict]:
        """检测具体问题 - 支持行业差异化"""
        issues = []
        
        # 检测P0级别(绝对禁止)
        anxiety_p0 = self.patterns["anxiety_p0"].findall(content)
        if anxiety_p0:
            issues.append({
                "type": "极端焦虑贩卖",
                "level": "P0",
                "keywords": list(set(anxiety_p0)),
                "description": "检测到极端焦虑贩卖内容,绝对禁止"
            })
        
        # 检测行业特定的P0违规
        fear_p0_keywords = self.FEAR_KEYWORDS["P0"].get(industry, [])
        if fear_p0_keywords:
            p0_fear_pattern = re.compile(r'(' + '|'.join(fear_p0_keywords) + r')', re.IGNORECASE)
            fear_p0 = p0_fear_pattern.findall(content)
            if fear_p0:
                issues.append({
                    "type": "行业特定严重违规",
                    "level": "P0",
                    "keywords": list(set(fear_p0)),
                    "description": f"在{industry}行业检测到严重违规内容"
                })
        
        # 检测焦虑营销
        anxiety_p1 = self.patterns["anxiety_p1"].findall(content)
        if anxiety_p1:
            issues.append({
                "type": "焦虑营销",
                "level": "P1",
                "keywords": list(set(anxiety_p1)),
                "description": "检测到焦虑营销关键词,可能引发用户不适"
            })
        
        # 检测恐惧营销
        fear_p1 = self.patterns["fear_p1_general"].findall(content)
        if fear_p1:
            issues.append({
                "type": "恐惧营销",
                "level": "P1",
                "keywords": list(set(fear_p1)),
                "description": "检测到恐惧营销关键词,涉嫌不当引导"
            })
        
        # 检测羞耻感营销
        shame = self.patterns["shame"].findall(content)
        if shame:
            issues.append({
                "type": "羞耻感营销",
                "level": "P1",
                "keywords": list(set(shame)),
                "description": "检测到利用羞耻感进行营销"
            })
        
        # 检测社会排斥
        exclusion = self.patterns["exclusion"].findall(content)
        if exclusion:
            issues.append({
                "type": "社会排斥",
                "level": "P1",
                "keywords": list(set(exclusion)),
                "description": "检测到利用社会排斥恐惧进行营销"
            })
        
        # 检测客观问题呈现(P3级别,正常)
        for category, pattern in self.objective_issue_patterns.items():
            matches = pattern.findall(content)
            if matches:
                issues.append({
                    "type": "客观问题呈现",
                    "level": "P3",
                    "category": category,
                    "keywords": list(set(matches)),
                    "description": f"检测到{category}相关客观问题陈述,属于正常表达范围"
                })
        
        return issues
    
    def _generate_suggestions(self, anxiety: float, fear: float,
                              solution: float, hope: float,
                              objective_issue: float = 0) -> List[str]:
        """generate改进建议 - 考虑客观问题呈现"""
        suggestions = []
        
        if anxiety > 60:
            suggestions.append("[P1]减少焦虑性表达,避免使用'再不...就晚了'等制造紧迫感的词汇")
        elif anxiety > 40:
            suggestions.append("[P2]适度减少焦虑性表达,增加解决方案比重")
        
        if fear > 60:
            suggestions.append("[P1]避免使用恐吓性语言,不要夸大问题的严重性")
        elif fear > 40:
            suggestions.append("[P2]减少恐惧性表达,使用更客观中性的描述")
        
        if solution < 50:
            if objective_issue > 30:
                suggestions.append("[P3]您提出了客观问题,建议增加更多具体的解决方案")
            else:
                suggestions.append("[P2]增加解决方案导向的内容,提供实用的方法和建议")
        
        if hope < 50:
            suggestions.append("[P3]增加积极正面的内容,传递希望和可能性")
        
        if objective_issue > 30 and solution >= 50:
            suggestions.append("[P3]内容结构良好:客观问题+解决方案,符合健康营销标准")
        
        if not suggestions:
            suggestions.append("情绪健康度良好,保持当前style")
        
        return suggestions
    
    def quick_check(self, content: str, industry: str = "general") -> Tuple[bool, str]:
        """
        快速检查,返回是否通过及原因 - 支持行业差异化 + 风控放宽
        
        Args:
            content: 待检查内容
            industry: 行业类型
            
        Returns:
            (通过状态, 原因说明)
        """
        result = self.analyze(content, industry)
        
        if result.risk_level == RiskLevel.PASS:
            return True, f"情绪健康度评分: {result.health_score:.1f},通过检查"
        elif result.risk_level == RiskLevel.P4:
            return True, f"[P4安全]情绪健康度评分: {result.health_score:.1f},夸张修辞允许使用"
        elif result.risk_level == RiskLevel.P3:
            return True, f"[P3低危]情绪健康度评分: {result.health_score:.1f},一般情绪表达"
        elif result.risk_level == RiskLevel.P2:
            return True, f"[P2注意]情绪健康度评分: {result.health_score:.1f},建议优化"
        elif result.risk_level == RiskLevel.P1:
            return False, f"[P1限制]风险等级: {result.risk_level.value},{result.detected_issues[0]['description'] if result.detected_issues else '存在情绪健康风险'}"
        else:  # P0
            return False, f"[P0禁止]严重违规: {result.detected_issues[0]['description'] if result.detected_issues else '存在严重违规内容'}"
