"""
__all__ = [
    'detect',
    'get_trending_topics',
    'is_oversaturated',
    'update_topic_frequency',
]

同质化检测器 - Homogenization Detector

检测内容的同质化程度,recognize行业套路和审美疲劳风险
"""

import re
from typing import Dict, List, Set
from dataclasses import dataclass
from collections import Counter

@dataclass
class HomogenizationResult:
    """同质化检测结果"""
    score: float                    # 同质化评分 0-100
    risk_level: str                 # 风险等级
    topic_hotness: float            # 话题热度 0-100
    expression_similarity: float    # 表达相似度 0-100
    pattern_score: float            # 套路recognize度 0-100
    similar_topics: List[str]       # 相似话题
    differentiation_suggestions: List[str]  # 差异化建议

class HomogenizationDetector:
    """同质化检测器"""
    
    # 行业同质化热点话题库
    HOMOGENIZED_TOPICS = {
        "教育": [
            "不要让孩子输在起跑线", "起跑线", "鸡娃", "内卷",
            "补习班", "学区房", "升学压力", "别人家的孩子"
        ],
        "职场": [
            "35岁危机", "中年危机", "职场内卷", "996", "007",
            "躺平", "摸鱼", "打工人", "社畜", "福报"
        ],
        "健康": [
            "熬夜致癌", "朋克养生", "保温杯里泡枸杞",
            "脱发", "秃头", "亚健康", "过劳肥"
        ],
        "理财": [
            "穷人思维", "富人思维", "睡后收入", "财务自由",
            "月光族", "精致穷", "隐形贫困人口"
        ],
        "情感": [
            "PUA", "舔狗", "备胎", "渣男", "渣女",
            "恋爱脑", "emo", "社死", "单身焦虑"
        ],
        "消费": [
            "种草", "拔草", "剁手", "吃土", "真香",
            "智商税", "割韭菜", "智商税", "平替"
        ],
        "生活方式": [
            "仪式感", "小确幸", "佛系", "丧", "毒鸡汤",
            "人间清醒", "摆烂", "卷不动"
        ]
    }
    
    # 套路化表达模板
    PATTERN_TEMPLATES = [
        r".*震惊.*",           # 震惊体
        r".*绝了.*",           # 绝了体
        r".*YYDS.*",           # YYDS
        r".*天花板.*",         # 天花板
        r".*卷王.*",           # 卷王
        r".*破防.*",           # 破防
        r".*emo.*",           # emo
        r".*栓Q.*",           # 栓Q
        r".*芭比Q.*",         # 芭比Q
        r".*爷青回.*",         # 爷青回
        r".*爷青结.*",         # 爷青结
    ]
    
    # 高频套路句式
    ROUTINE_SENTENCES = [
        "不会还有人不知道吧",
        "我不允许你还不知道",
        "建议收藏",
        "全网最",
        "保姆级",
        "手把手",
        "亲测有效",
        "后悔没早点",
        "看完我悟了",
        "原来这才是",
        "这才是真正的",
        "终于知道为什么",
    ]
    
    def __init__(self):
        self._compile_patterns()
        self.topic_frequency = Counter()  # 话题频次统计
    
    def _compile_patterns(self):
        """编译正则表达式"""
        self.patterns = [re.compile(p, re.IGNORECASE) for p in self.PATTERN_TEMPLATES]
    
    def detect(self, content: str, category: str = None) -> HomogenizationResult:
        """
        检测内容的同质化程度
        
        Args:
            content: 待检测内容
            category: 内容类别(可选)
            
        Returns:
            HomogenizationResult: 检测结果
        """
        # 话题热度检查
        topic_hotness = self._check_topic_hotness(content)
        
        # 表达方式相似度
        expression_similarity = self._check_expression_similarity(content)
        
        # 套路recognize
        pattern_score = self._detect_patterns(content)
        
        # recognize相似话题
        similar_topics = self._identify_similar_topics(content)
        
        # 计算synthesize同质化评分
        score = self._calculate_score(
            topic_hotness, expression_similarity, pattern_score
        )
        
        # 确定风险等级
        risk_level = self._determine_risk_level(score)
        
        # generate差异化建议
        suggestions = self._generate_suggestions(
            score, similar_topics, pattern_score
        )
        
        return HomogenizationResult(
            score=score,
            risk_level=risk_level,
            topic_hotness=topic_hotness,
            expression_similarity=expression_similarity,
            pattern_score=pattern_score,
            similar_topics=similar_topics,
            differentiation_suggestions=suggestions
        )
    
    def _check_topic_hotness(self, content: str) -> float:
        """检查话题热度"""
        all_topics = []
        for category_topics in self.HOMOGENIZED_TOPICS.values():
            all_topics.extend(category_topics)
        
        matches = 0
        for topic in all_topics:
            if topic in content:
                matches += 1
        
        # 热度评分
        score = min(100, matches * 15)
        return score
    
    def _check_expression_similarity(self, content: str) -> float:
        """检查表达方式相似度"""
        # 检测套路句式
        routine_matches = sum(1 for rs in self.ROUTINE_SENTENCES if rs in content)
        
        # 检测网络流行语密度
        buzzword_patterns = [
            r"(绝绝子|yyds|栓Q|芭比Q|emo|破防|内卷|躺平|佛系)",
        ]
        buzzword_count = sum(
            len(re.findall(p, content, re.IGNORECASE)) 
            for p in buzzword_patterns
        )
        
        score = min(100, routine_matches * 12 + buzzword_count * 8)
        return score
    
    def _detect_patterns(self, content: str) -> float:
        """检测套路化程度"""
        pattern_matches = sum(
            1 for p in self.patterns if p.search(content)
        )
        
        score = min(100, pattern_matches * 20)
        return score
    
    def _identify_similar_topics(self, content: str) -> List[str]:
        """recognize相似话题"""
        similar = []
        
        for category, topics in self.HOMOGENIZED_TOPICS.items():
            for topic in topics:
                if topic in content:
                    similar.append(f"{category}: {topic}")
                    break
        
        return similar
    
    def _calculate_score(self, topic: float, expression: float, 
                         pattern: float) -> float:
        """计算synthesize同质化评分"""
        score = (
            topic * 0.35 +
            expression * 0.30 +
            pattern * 0.35
        )
        return score
    
    def _determine_risk_level(self, score: float) -> str:
        """确定风险等级"""
        if score >= 70:
            return "P2"
        elif score >= 50:
            return "P3"
        else:
            return "PASS"
    
    def _generate_suggestions(self, score: float, similar_topics: List[str],
                              pattern_score: float) -> List[str]:
        """generate差异化建议"""
        suggestions = []
        
        if score >= 70:
            suggestions.append("内容同质化程度较高,建议重新策划角度")
        
        if similar_topics:
            topics_str = ",".join([t.split(": ")[1] for t in similar_topics[:3]])
            suggestions.append(f"检测到同质化话题({topics_str}),建议挖掘细分痛点")
        
        if pattern_score >= 40:
            suggestions.append("表达方式套路化明显,建议创新表达形式")
        
        if not suggestions:
            suggestions.append("差异化程度良好,保持创新style")
        else:
            suggestions.append("建议:寻找独特的用户视角,挖掘未被充分讨论的细分场景")
        
        return suggestions
    
    def update_topic_frequency(self, topic: str):
        """更新话题频次统计"""
        self.topic_frequency[topic] += 1
    
    def get_trending_topics(self, top_n: int = 10) -> List[tuple]:
        """get热门话题排行"""
        return self.topic_frequency.most_common(top_n)
    
    def is_oversaturated(self, topic: str, threshold: int = 100) -> bool:
        """judge话题是否过度饱和"""
        return self.topic_frequency.get(topic, 0) >= threshold
