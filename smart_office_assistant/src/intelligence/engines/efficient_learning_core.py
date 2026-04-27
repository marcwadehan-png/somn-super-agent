# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_learning_efficiency',
    'assess_learning_style',
    'create_efficient_learning_core',
    'create_study_plan',
    'get_focus_training',
    'get_memory_technique',
    'recommend_techniques',
    'select_reading_method',
    'to_dict',
]

高效学习核心系统 v1.0.0
Efficient Learning Core System

基于<超级记忆力训练法><高效阅读><思维的本质>核心思想构建

核心思想:
- 学习是神经连接的重塑过程
- 记忆是存储和提取的艺术
- 专注力是学习的核心竞争力
- 深度学习优于浅层学习

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import re

class LearningStyle(Enum):
    """学习style"""
    VISUAL = "视觉型"  # 喜欢看图,图表
    AUDITORY = "听觉型"  # 喜欢听,讨论
    KINESTHETIC = "动觉型"  # 喜欢动手实践
    READING = "阅读型"  # 喜欢阅读文字
    MIXED = "混合型"  # 多种方式结合

class MemoryTechnique(Enum):
    """记忆技巧"""
    MEMORY_PALACE = "记忆宫殿"  # 位置记忆法
    ASSOCIATION = "联想记忆"  # 关联联想
    VISUALIZATION = "形象化"  # 将抽象转为形象
    CHUNKING = "组块化"  # 分块记忆
    SPACED_REPETITION = "间隔重复"  # 科学复习
    ACTIVE_RECALL = "主动回忆"  # 测试式学习
    MIND_MAP = "思维导图"  # 图形化组织

class ReadingMethod(Enum):
    """阅读方法"""
    SKIMMING = "略读"  # 快速浏览get大意
    SCANNING = "扫读"  # 有目标地寻找信息
    INTENSIVE = "精读"  # 深入理解
    CRITICAL = "批判性阅读"  # 分析评价
    ACTIVE = "主动阅读"  # 边读边思考

@dataclass
class LearningStyleProfile:
    """学习style画像"""
    visual_score: float = 0.0
    auditory_score: float = 0.0
    kinesthetic_score: float = 0.0
    reading_score: float = 0.0
    
    dominant_style: LearningStyle = LearningStyle.MIXED
    suggestions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "visual": round(self.visual_score, 1),
            "auditory": round(self.auditory_score, 1),
            "kinesthetic": round(self.kinesthetic_score, 1),
            "reading": round(self.reading_score, 1),
            "dominant_style": self.dominant_style.value,
            "suggestions": self.suggestions
        }

@dataclass
class MemoryTechniqueGuide:
    """记忆技巧指南"""
    technique: MemoryTechnique
    description: str
    use_scenario: str  # 适用场景
    steps: List[str]
    example: str
    effectiveness: float  # 有效性 0-10

class EfficientLearningCore:
    """
    高效学习核心系统
    
    基于<超级记忆力训练法><高效阅读><思维的本质>构建,
    提供科学的学习方法指导.
    
    主要功能:
    1. 学习style评估
    2. 记忆技巧指导
    3. 阅读方法选择
    4. 学习计划制定
    5. 专注力训练
    """
    
    # 学习style关键词
    STYLE_KEYWORDS = {
        LearningStyle.VISUAL: ["看", "图片", "图表", "颜色", "视觉", "观察", "演示"],
        LearningStyle.AUDITORY: ["听", "讨论", "说话", "听觉", "音频", "讲解", "对话"],
        LearningStyle.KINESTHETIC: ["做", "动手", "实践", "触摸", "移动", "尝试", "体验"],
        LearningStyle.READING: ["读", "文字", "书写", "阅读", "笔记", "看书", "文章"]
    }
    
    # 记忆技巧详情
    MEMORY_TECHNIQUES = {
        MemoryTechnique.MEMORY_PALACE: {
            "description": "将信息与熟悉的空间位置关联",
            "适用场景": "记忆列表,顺序,大量信息",
            "steps": [
                "选择熟悉的地方(如家里)",
                "规划一条路线",
                "将信息与每个位置关联",
                "在脑中沿着路线回忆"
            ],
            "example": "记忆购物清单:苹果→门口,牛奶→鞋柜,面包→餐桌..."
        },
        MemoryTechnique.ASSOCIATION: {
            "description": "将新信息与已知信息关联",
            "适用场景": "记忆概念,定义,抽象信息",
            "steps": [
                "recognize新信息的核心",
                "找到与之关联的已知信息",
                "创造生动有趣的联想",
                "重复强化关联"
            ],
            "example": "记忆'量子纠缠':想象两个纠缠的舞蹈演员,一个动另一个就动"
        },
        MemoryTechnique.VISUALIZATION: {
            "description": "将抽象信息形象化",
            "适用场景": "记忆抽象概念,理论",
            "steps": [
                "理解抽象概念的本质",
                "创造具体的形象或场景",
                "添加夸张,荒诞的元素加深印象",
                "定期复习形象"
            ],
            "example": "记忆'通货膨胀':想象一叠钱变成纸飞机的过程"
        },
        MemoryTechnique.CHUNKING: {
            "description": "将信息分成有意义的小块",
            "适用场景": "记忆数字,代码,长文本",
            "steps": [
                "recognize信息的规律",
                "按照规律分组",
                "给每组一个标签或意义",
                "组块之间建立联系"
            ],
            "example": "记忆手机号:138-1234-5678(3-4-4分组)"
        },
        MemoryTechnique.SPACED_REPETITION: {
            "description": "在遗忘点前复习",
            "适用场景": "记忆需要长期保持的信息",
            "steps": [
                "首次学习新信息",
                "1天后复习",
                "3天后复习",
                "7天后复习",
                "14天后复习",
                "30天后复习"
            ],
            "example": "背单词app的复习间隔就是这个原理"
        },
        MemoryTechnique.ACTIVE_RECALL: {
            "description": "主动回忆而非被动重读",
            "适用场景": "任何需要记忆的学习",
            "steps": [
                "学习后合上书",
                "尝试回忆关键内容",
                "检查回忆的准确度",
                "重点复习回忆错误的部分"
            ],
            "example": "读完一页后,闭眼回忆这页讲了什么"
        },
        MemoryTechnique.MIND_MAP: {
            "description": "用图形组织信息",
            "适用场景": "整理知识结构,头脑风暴",
            "steps": [
                "中心主题放在中央",
                "分支写主要类别",
                "每个类别展开细节",
                "使用颜色和图像"
            ],
            "example": "以'健康'为中心,分出饮食,运动,睡眠等分支"
        }
    }
    
    # 阅读方法详情
    READING_METHODS = {
        ReadingMethod.SKIMMING: {
            "适用场景": "快速了解大意,筛选内容",
            "目标": "get文章大意和结构",
            "技巧": ["看标题和小标题", "读首段和末段", "扫读每段首句"]
        },
        ReadingMethod.SCANNING: {
            "适用场景": "寻找特定信息",
            "目标": "快速定位目标内容",
            "技巧": ["明确要找什么", "眼睛快速扫动", "遇到相关词减速"]
        },
        ReadingMethod.INTENSIVE: {
            "适用场景": "深入学习重要内容",
            "目标": "完全理解内容",
            "技巧": ["逐句阅读", "做笔记", "划重点", "思考含义"]
        },
        ReadingMethod.CRITICAL: {
            "适用场景": "评估信息质量",
            "目标": "形成自己的judge",
            "技巧": ["质疑作者观点", "寻找证据", "比较不同观点", "形成评价"]
        },
        ReadingMethod.ACTIVE: {
            "适用场景": "深度学习和吸收",
            "目标": "将知识内化",
            "技巧": ["边读边提问", "与已有知识关联", "做总结", "应用实践"]
        }
    }
    
    def __init__(self):
        self.learning_history: List[Dict] = []
        self.technique_usage: Dict[str, int] = defaultdict(int)
    
    def assess_learning_style(self, text: str = "") -> LearningStyleProfile:
        """
        评估学习style
        
        Args:
            text: 关于学习偏好的描述
            
        Returns:
            LearningStyleProfile: 学习style画像
        """
        text_lower = text.lower()
        
        scores = {LearningStyle.VISUAL: 0, LearningStyle.AUDITORY: 0,
                 LearningStyle.KINESTHETIC: 0, LearningStyle.READING: 0}
        
        for style, keywords in self.STYLE_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    scores[style] += 10
        
        # 确定主导style
        max_score = max(scores.values())
        if max_score < 30:
            dominant = LearningStyle.MIXED
        else:
            for style, score in scores.items():
                if score == max_score:
                    dominant = style
                    break
        
        # generate建议
        suggestions = self._generate_style_suggestions(dominant)
        
        return LearningStyleProfile(
            visual_score=scores[LearningStyle.VISUAL],
            auditory_score=scores[LearningStyle.AUDITORY],
            kinesthetic_score=scores[LearningStyle.KINESTHETIC],
            reading_score=scores[LearningStyle.READING],
            dominant_style=dominant,
            suggestions=suggestions
        )
    
    def _generate_style_suggestions(self, style: LearningStyle) -> List[str]:
        """generatestyle建议"""
        suggestions = {
            LearningStyle.VISUAL: [
                "多用图表,颜色,图像来学习",
                "制作思维导图整理信息",
                "观看视频教程",
                "用荧光笔标注重点"
            ],
            LearningStyle.AUDITORY: [
                "多听讲座,播客,有声书",
                "加入讨论小组,边讨论边学习",
                "把自己学的内容讲给别人听",
                "学习时大声朗读"
            ],
            LearningStyle.KINESTHETIC: [
                "边做笔记边学习",
                "通过实践来学习新知识",
                "模拟真实场景练习",
                "使用实物模型帮助理解"
            ],
            LearningStyle.READING: [
                "多阅读相关书籍和文章",
                "做好笔记和总结",
                "写读后感和学习心得",
                "对比不同来源的文字信息"
            ],
            LearningStyle.MIXED: [
                "结合多种方式进行学习",
                "根据不同内容选择最适合的方式",
                "发挥各种style的优势"
            ]
        }
        return suggestions.get(style, suggestions[LearningStyle.MIXED])
    
    def get_memory_technique(self, technique: MemoryTechnique) -> MemoryTechniqueGuide:
        """get记忆技巧详情"""
        info = self.MEMORY_TECHNIQUES.get(technique, {})
        
        return MemoryTechniqueGuide(
            technique=technique,
            description=info.get("description", ""),
            适用场景=info.get("适用场景", ""),
            steps=info.get("steps", []),
            example=info.get("example", ""),
            effectiveness=8.5
        )
    
    def recommend_techniques(self, content_type: str) -> List[MemoryTechniqueGuide]:
        """
        推荐适合的记忆技巧
        
        Args:
            content_type: 内容类型(单词,概念,数字,列表等)
            
        Returns:
            List[MemoryTechniqueGuide]: 推荐的技巧列表
        """
        recommendations = []
        
        if "单词" in content_type or "词汇" in content_type:
            recommendations.append(self.get_memory_technique(MemoryTechnique.ASSOCIATION))
            recommendations.append(self.get_memory_technique(MemoryTechnique.VISUALIZATION))
            recommendations.append(self.get_memory_technique(MemoryTechnique.SPACED_REPETITION))
        
        elif "列表" in content_type or "顺序" in content_type:
            recommendations.append(self.get_memory_technique(MemoryTechnique.MEMORY_PALACE))
            recommendations.append(self.get_memory_technique(MemoryTechnique.CHUNKING))
        
        elif "概念" in content_type or "定义" in content_type:
            recommendations.append(self.get_memory_technique(MemoryTechnique.ASSOCIATION))
            recommendations.append(self.get_memory_technique(MemoryTechnique.ACTIVE_RECALL))
            recommendations.append(self.get_memory_technique(MemoryTechnique.MIND_MAP))
        
        elif "数字" in content_type or "日期" in content_type:
            recommendations.append(self.get_memory_technique(MemoryTechnique.CHUNKING))
            recommendations.append(self.get_memory_technique(MemoryTechnique.MEMORY_PALACE))
        
        else:
            # 默认推荐
            recommendations.append(self.get_memory_technique(MemoryTechnique.ACTIVE_RECALL))
            recommendations.append(self.get_memory_technique(MemoryTechnique.SPACED_REPETITION))
            recommendations.append(self.get_memory_technique(MemoryTechnique.MIND_MAP))
        
        return recommendations
    
    def select_reading_method(self, goal: str, time_available: str = "") -> Dict:
        """
        选择适合的阅读方法
        
        Args:
            goal: 阅读目的
            time_available: 可用时间
            
        Returns:
            Dict: 阅读方法建议
        """
        # 根据目的选择方法
        if "了解" in goal or "概览" in goal:
            method = ReadingMethod.SKIMMING
        elif "寻找" in goal or "查找" in goal:
            method = ReadingMethod.SCANNING
        elif "深入" in goal or "学习" in goal:
            method = ReadingMethod.INTENSIVE
        elif "评价" in goal or "分析" in goal:
            method = ReadingMethod.CRITICAL
        elif "吸收" in goal or "内化" in goal:
            method = ReadingMethod.ACTIVE
        else:
            method = ReadingMethod.INTENSIVE
        
        info = self.READING_METHODS.get(method, {})
        
        return {
            "recommended_method": method.value,
            "适用场景": info.get("适用场景", ""),
            "目标": info.get("目标", ""),
            "技巧": info.get("技巧", []),
            "time_tip": self._get_time_tip(time_available, method)
        }
    
    def _get_time_tip(self, time_available: str, method: ReadingMethod) -> str:
        """get时间建议"""
        if "充足" in time_available:
            return "时间充足,可以深入阅读和思考"
        elif "有限" in time_available or "短" in time_available:
            return "时间有限,建议使用略读或扫读方法"
        else:
            return f"使用{method.value}方法,根据内容难度调整速度"
    
    def create_study_plan(self, topic: str, current_level: str = "初学者",
                          target_level: str = "掌握",
                          weeks: int = 4) -> Dict:
        """
        创建学习计划
        
        Args:
            topic: 学习主题
            current_level: 当前水平
            target_level: 目标水平
            weeks: 计划周期(周)
            
        Returns:
            Dict: 学习计划
        """
        plan = {
            "topic": topic,
            "current_level": current_level,
            "target_level": target_level,
            "duration_weeks": weeks,
            "phases": [],
            "daily_routine": [],
            "key_milestones": [],
            "recommended_resources": []
        }
        
        # 分阶段
        phase_names = ["基础入门", "进阶学习", "深度理解", "实践应用"]
        for i, phase in enumerate(phase_names[:weeks]):
            week_start = i + 1
            week_end = i + 1
            
            plan["phases"].append({
                "week": f"第{week_start}周",
                "name": phase,
                "goals": self._get_phase_goals(phase, topic),
                "activities": self._get_phase_activities(phase)
            })
            
            plan["key_milestones"].append({
                "week": f"第{week_start}周完成时",
                "milestone": f"能够{self._get_phase_milestone(phase)}"
            })
        
        # 每日Routine
        plan["daily_routine"] = [
            "早晨(30分钟):复习前一天学的内容",
            "上午(60分钟):学习新知识,使用主动回忆",
            "下午(45分钟):做练习或实践",
            "晚上(20分钟):整理笔记,预习明天内容"
        ]
        
        # 推荐资源
        plan["recommended_resources"] = [
            f"{topic}入门书籍2-3本",
            f"{topic}相关视频课程",
            f"{topic}实践社区或论坛",
            f"{topic}领域专家的社交媒体"
        ]
        
        return plan
    
    def _get_phase_goals(self, phase: str, topic: str) -> List[str]:
        """get阶段目标"""
        goals = {
            "基础入门": [f"了解{topic}的基本概念", f"掌握{topic}的核心术语", "建立整体框架"],
            "进阶学习": [f"深入理解{topic}的原理", "开始实践基本操作", "解决常见问题"],
            "深度理解": [f"全面掌握{topic}", "能够解释为什么", "开始有自己的见解"],
            "实践应用": [f"能够独立应用{topic}", "解决复杂问题", "教授他人"]
        }
        return goals.get(phase, [f"学习{topic}"])
    
    def _get_phase_activities(self, phase: str) -> List[str]:
        """get阶段活动"""
        activities = {
            "基础入门": ["阅读入门资料", "观看基础视频", "做笔记整理", "记忆核心概念"],
            "进阶学习": ["阅读进阶书籍", "做更多练习", "加入讨论", "使用间隔重复复习"],
            "深度理解": ["阅读原版资料", "深度思考原理", "写学习心得", "与专家讨论"],
            "实践应用": ["做项目实践", "解决实际问题", "分享给他人", "总结经验教训"]
        }
        return activities.get(phase, ["学习"])
    
    def _get_phase_milestone(self, phase: str) -> str:
        """get阶段里程碑"""
        milestones = {
            "基础入门": "用自己的话解释核心概念",
            "进阶学习": "能够解决中等难度的问题",
            "深度理解": "能够教授他人",
            "实践应用": "能够独立处理真实案例"
        }
        return milestones.get(phase, "完成该阶段学习")
    
    def get_focus_training(self) -> Dict:
        """get专注力训练指导"""
        return {
            "基础训练": [
                "番茄工作法:25分钟专注,5分钟休息",
                "冥想训练:每天10分钟,专注呼吸",
                "单任务专注:一次只做一件事"
            ],
            "进阶训练": [
                "深度工作:90分钟无干扰专注",
                "环境管理:创造无干扰的学习环境",
                "习惯绑定:将专注与特定环境关联"
            ],
            "日常实践": [
                "学习前冥想3分钟清空杂念",
                "用计时器记录专注时间",
                "每天反思专注状态"
            ]
        }
    
    def analyze_learning_efficiency(self, study_time: float, 
                                   content_learned: float,
                                   retention_rate: float = 0.7) -> Dict:
        """
        分析学习效率
        
        Args:
            study_time: 学习时长(小时)
            content_learned: 学会的内容量(百分比)
            retention_rate: 记忆保持率(0-1)
            
        Returns:
            Dict: 效率分析
        """
        # 计算效率分数
        base_efficiency = (content_learned / max(study_time, 0.1)) * retention_rate * 100
        
        # 效率等级
        if base_efficiency > 80:
            level = "高效学习者"
            advice = "继续保持,可以挑战更高难度"
        elif base_efficiency > 50:
            level = "良好学习者"
            advice = "效率不错,可以优化学习方法"
        elif base_efficiency > 30:
            level = "有待提升"
            advice = "建议检查学习方法和专注度"
        else:
            level = "效率较低"
            advice = "需要大幅改进学习strategy"
        
        return {
            "study_time_hours": study_time,
            "content_mastered_percent": content_learned,
            "retention_rate": retention_rate * 100,
            "efficiency_score": round(base_efficiency, 1),
            "level": level,
            "advice": advice,
            "suggestions": self._get_efficiency_suggestions(base_efficiency)
        }
    
    def _get_efficiency_suggestions(self, efficiency: float) -> List[str]:
        """get效率提升建议"""
        if efficiency < 50:
            return [
                "使用主动回忆而非被动重读",
                "采用间隔重复法复习",
                "减少干扰,创造专注环境",
                "一次学习时间不要太长"
            ]
        else:
            return [
                "继续使用有效的学习方法",
                "定期评估和调整strategy",
                "尝试教授他人来巩固"
            ]

def create_efficient_learning_core() -> EfficientLearningCore:
    """工厂函数"""
    return EfficientLearningCore()
