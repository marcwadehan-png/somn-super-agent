"""
__all__ = [
    'complete_module',
    'demo_education_app',
    'evaluate_test',
    'export_learning_data',
    'generate_practice_test',
    'get_current_module',
    'get_exercises_for_module',
    'get_recommendations',
    'get_recommended_path',
    'get_user_progress_report',
    'register_user',
    'to_dict',
]

诗词教育应用模块
基于唐诗宋词50大家深度学习研究项目成果开发
Version: 1.0.0
Created: 2026-04-02
"""

import os
import json
import random
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

class LearningMode(Enum):
    """学习模式"""
    BEGINNER = "beginner"      # 初学者
    INTERMEDIATE = "intermediate"  # 中级
    ADVANCED = "advanced"      # 高级
    EXPERT = "expert"          # 专家

class ExerciseType(Enum):
    """练习类型"""
    MULTIPLE_CHOICE = "multiple_choice"    # 选择题
    FILL_IN_BLANK = "fill_in_blank"        # 填空题
    MATCHING = "matching"                  # 匹配题
    ANALYSIS = "analysis"                  # 分析题
    COMPOSITION = "composition"            # 创作题

@dataclass
class LearningPath:
    """学习路径"""
    path_id: str
    name: str
    description: str
    target_level: LearningMode
    estimated_hours: int
    modules: List[str]
    prerequisites: List[str] = None
    
    def to_dict(self):
        return {
            "id": self.path_id,
            "name": self.name,
            "description": self.description,
            "target_level": self.target_level.value,
            "estimated_hours": self.estimated_hours,
            "modules": self.modules,
            "prerequisites": self.prerequisites or []
        }

@dataclass
class LearningModule:
    """学习模块"""
    module_id: str
    title: str
    description: str
    difficulty: LearningMode
    content: Dict
    exercises: List[Dict]
    estimated_time: int  # 分钟
    
    def to_dict(self):
        return {
            "id": self.module_id,
            "title": self.title,
            "description": self.description,
            "difficulty": self.difficulty.value,
            "content": self.content,
            "exercises": self.exercises,
            "estimated_time": self.estimated_time
        }

@dataclass
class UserProgress:
    """用户学习进度"""
    user_id: str
    completed_modules: List[str]
    current_module: str
    learning_path: str
    start_date: str
    last_active: str
    scores: Dict[str, float]  # 模块ID: 分数
    achievements: List[str]
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "completed_modules": self.completed_modules,
            "current_module": self.current_module,
            "learning_path": self.learning_path,
            "start_date": self.start_date,
            "last_active": self.last_active,
            "scores": self.scores,
            "achievements": self.achievements
        }

@dataclass
class Exercise:
    """练习题"""
    exercise_id: str
    exercise_type: ExerciseType
    question: str
    options: List[str] = None
    correct_answer: str = None
    explanation: str = None
    difficulty: LearningMode = LearningMode.BEGINNER
    points: int = 10
    
    def to_dict(self):
        return {
            "id": self.exercise_id,
            "type": self.exercise_type.value,
            "question": self.question,
            "options": self.options or [],
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "difficulty": self.difficulty.value,
            "points": self.points
        }

class PoetryEducationApp:
    """诗词教育应用"""
    
    def __init__(self, data_dir: str = None):
        """
        init教育应用
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir or os.path.join("data", "poetry_education")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 学习路径
        self.learning_paths: Dict[str, LearningPath] = {}
        
        # 学习模块
        self.modules: Dict[str, LearningModule] = {}
        
        # 用户进度
        self.user_progress: Dict[str, UserProgress] = {}
        
        # 练习题库
        self.exercises: Dict[str, Exercise] = {}
        
        # 基于唐诗宋词研究项目init
        self._init_learning_paths()
        self._init_modules()
        self._init_exercises()
    
    def _init_learning_paths(self):
        """init学习路径(基于50大家研究项目)"""
        
        paths = [
            LearningPath(
                path_id="path_tang_intro",
                name="唐代诗歌入门",
                description="学习唐代诗歌基础,了解主要poet和representative_works",
                target_level=LearningMode.BEGINNER,
                estimated_hours=20,
                modules=["mod_tang_overview", "mod_libai_intro", "mod_dufu_intro"],
                prerequisites=[]
            ),
            LearningPath(
                path_id="path_tang_advanced",
                name="唐代诗歌进阶",
                description="深入学习唐代各流派诗歌,掌握艺术特色和创作背景",
                target_level=LearningMode.INTERMEDIATE,
                estimated_hours=40,
                modules=["mod_tang_styles", "mod_wangwei", "mod_bai_juyi"],
                prerequisites=["path_tang_intro"]
            ),
            LearningPath(
                path_id="path_song_intro",
                name="宋代词作入门",
                description="学习宋代词作基础,了解主要poet和ci_pattern",
                target_level=LearningMode.BEGINNER,
                estimated_hours=25,
                modules=["mod_song_overview", "mod_sushi_intro", "mod_liqingzhao_intro"],
                prerequisites=[]
            ),
            LearningPath(
                path_id="path_song_advanced",
                name="宋代词作进阶",
                description="深入学习宋代各流派词作,掌握格律和艺术手法",
                target_level=LearningMode.INTERMEDIATE,
                estimated_hours=45,
                modules=["mod_song_styles", "mod_xinqiji", "mod_liuyong"],
                prerequisites=["path_song_intro"]
            ),
            LearningPath(
                path_id="path_comprehensive",
                name="唐诗宋词synthesize研究",
                description="系统研究唐诗宋词,掌握比较分析和synthesize研究能力",
                target_level=LearningMode.ADVANCED,
                estimated_hours=60,
                modules=["mod_comparative_analysis", "mod_literary_criticism", "mod_research_methods"],
                prerequisites=["path_tang_advanced", "path_song_advanced"]
            ),
            LearningPath(
                path_id="path_expert",
                name="诗词研究专家",
                description="深入专题研究,掌握学术研究和创作能力",
                target_level=LearningMode.EXPERT,
                estimated_hours=80,
                modules=["mod_special_topics", "mod_creative_writing", "mod_academic_research"],
                prerequisites=["path_comprehensive"]
            )
        ]
        
        for path in paths:
            self.learning_paths[path.path_id] = path
    
    def _init_modules(self):
        """init学习模块(基于50大家研究项目)"""
        
        # 唐代诗歌概述模块
        tang_overview = LearningModule(
            module_id="mod_tang_overview",
            title="唐代诗歌概览",
            description="了解唐代诗歌发展历程,主要流派和代表poet",
            difficulty=LearningMode.BEGINNER,
            content={
                "sections": [
                    {
                        "title": "唐代诗歌发展历程",
                        "content": "初唐(618-712)→ 盛唐(713-765)→ 中唐(766-835)→ 晚唐(836-907)",
                        "key_points": ["四唐分期", "时代背景", "演变characteristics"]
                    },
                    {
                        "title": "主要诗歌流派",
                        "content": "山水田园派,边塞诗派,浪漫主义,现实主义,新乐府运动",
                        "key_points": ["代表poet", "艺术特色", "representative_works"]
                    },
                    {
                        "title": "唐代诗歌成就",
                        "content": "唐诗是中国古典诗歌的巅峰,现存约5万首,poet约2300位",
                        "key_points": ["数量规模", "艺术成就", "国际影响"]
                    }
                ],
                "resources": [
                    {"type": "video", "title": "唐代诗歌发展简史", "duration": "15分钟"},
                    {"type": "reading", "title": "<唐诗三百首>导读", "pages": "10页"},
                    {"type": "interactive", "title": "唐代poet时间轴", "activity": "时间排序"}
                ]
            },
            exercises=["ex_tang_overview_1", "ex_tang_overview_2", "ex_tang_overview_3"],
            estimated_time=120
        )
        
        # 李白介绍模块
        libai_intro = LearningModule(
            module_id="mod_libai_intro",
            title="诗仙李白",
            description="学习李白的生平,创作特点和representative_works",
            difficulty=LearningMode.BEGINNER,
            content={
                "sections": [
                    {
                        "title": "李白的生平",
                        "content": "李白(701-762),字太白,号青莲居士,唐代浪漫主义poet代表",
                        "key_points": ["生卒年份", "字号别称", "主要经历"]
                    },
                    {
                        "title": "创作特点",
                        "content": "豪放飘逸,想象丰富,语言夸张,情感奔放",
                        "key_points": ["艺术style", "语言特色", "情感表达"]
                    },
                    {
                        "title": "representative_works",
                        "content": "<将进酒>,<蜀道难>,<静夜思>,<早发白帝城>",
                        "key_points": ["作品主题", "艺术成就", "历史地位"]
                    },
                    {
                        "title": "诗歌赏析",
                        "content": """
                        <静夜思>赏析:
                        床前明月光,疑是地上霜.
                        举头望明月,低头思故乡.
                        
                        赏析要点:
                        1. 语言简练,意境深远
                        2. 乡愁主题,情感真挚
                        3. 对仗工整,音韵和谐
                        """,
                        "key_points": ["语言分析", "意境解读", "情感体验"]
                    }
                ],
                "resources": [
                    {"type": "video", "title": "李白生平纪录片", "duration": "25分钟"},
                    {"type": "audio", "title": "李白诗歌朗诵", "duration": "30分钟"},
                    {"type": "interactive", "title": "李白诗歌创作地图", "activity": "地理定位"}
                ]
            },
            exercises=["ex_libai_1", "ex_libai_2", "ex_libai_3"],
            estimated_time=150
        )
        
        # 更多模块...
        # 实际项目中会有50个模块,对应50位大家
        
        modules = [tang_overview, libai_intro]
        
        for module in modules:
            self.modules[module.module_id] = module
    
    def _init_exercises(self):
        """init练习题库"""
        
        exercises = [
            # 唐代诗歌概述练习题
            Exercise(
                exercise_id="ex_tang_overview_1",
                exercise_type=ExerciseType.MULTIPLE_CHOICE,
                question="唐代诗歌发展的四个时期是什么顺序?",
                options=[
                    "初唐→盛唐→中唐→晚唐",
                    "盛唐→初唐→中唐→晚唐", 
                    "初唐→中唐→盛唐→晚唐",
                    "晚唐→中唐→盛唐→初唐"
                ],
                correct_answer="初唐→盛唐→中唐→晚唐",
                explanation="唐代诗歌发展分为四个时期:初唐(618-712),盛唐(713-765),中唐(766-835),晚唐(836-907).",
                difficulty=LearningMode.BEGINNER,
                points=10
            ),
            Exercise(
                exercise_id="ex_tang_overview_2",
                exercise_type=ExerciseType.FILL_IN_BLANK,
                question="唐代现存诗歌约______首,poet约______wei.",
                correct_answer="5万,2300",
                explanation="根据<全唐诗>统计,唐代现存诗歌约5万首,poet约2300位.",
                difficulty=LearningMode.BEGINNER,
                points=15
            ),
            Exercise(
                exercise_id="ex_tang_overview_3",
                exercise_type=ExerciseType.MATCHING,
                question="请将下列poet与其流派进行匹配:",
                options=[
                    "王维", "高适", "李白", "白居易", "杜甫",
                    "山水田园派", "边塞诗派", "浪漫主义", "新乐府运动", "现实主义"
                ],
                correct_answer="王维:山水田园派,高适:边塞诗派,李白:浪漫主义,白居易:新乐府运动,杜甫:现实主义",
                explanation="王维是山水田园派代表,高适是边塞诗派代表,李白是浪漫主义代表,白居易是新乐府运动领袖,杜甫是现实主义代表.",
                difficulty=LearningMode.BEGINNER,
                points=20
            ),
            
            # 李白练习题
            Exercise(
                exercise_id="ex_libai_1",
                exercise_type=ExerciseType.MULTIPLE_CHOICE,
                question="李白的字号是什么?",
                options=[
                    "字太白,号青莲居士",
                    "字子美,号少陵野老",
                    "字摩诘,号诗佛",
                    "字乐天,号香山居士"
                ],
                correct_answer="字太白,号青莲居士",
                explanation="李白,字太白,号青莲居士,又号\"谪仙人\".",
                difficulty=LearningMode.BEGINNER,
                points=10
            ),
            Exercise(
                exercise_id="ex_libai_2",
                exercise_type=ExerciseType.FILL_IN_BLANK,
                question="李白<静夜思>的前两句是:床前______,疑是______.",
                correct_answer="明月光,地上霜",
                explanation="<静夜思>全诗:床前明月光,疑是地上霜.举头望明月,低头思故乡.",
                difficulty=LearningMode.BEGINNER,
                points=15
            ),
            Exercise(
                exercise_id="ex_libai_3",
                exercise_type=ExerciseType.ANALYSIS,
                question="请分析李白<将进酒>中\"天生我材必有用\"一句的深刻含义.",
                correct_answer="这句话表达了李白对个人价值的自信,体现了唐代士人的积极进取精神,同时也反映了李白豪放不羁的性格特点.",
                explanation="\"天生我材必有用\"体现了:1. 对个人才能的自信 2. 积极的人生态度 3. 唐代开放包容的时代精神 4. 李白特有的浪漫主义情怀.",
                difficulty=LearningMode.INTERMEDIATE,
                points=25
            )
        ]
        
        for exercise in exercises:
            self.exercises[exercise.exercise_id] = exercise
    
    def register_user(self, user_id: str, learning_path_id: str) -> UserProgress:
        """注册新用户"""
        if learning_path_id not in self.learning_paths:
            raise ValueError(f"学习路径 {learning_path_id} 不存在")
        
        progress = UserProgress(
            user_id=user_id,
            completed_modules=[],
            current_module=self.learning_paths[learning_path_id].modules[0] if self.learning_paths[learning_path_id].modules else "",
            learning_path=learning_path_id,
            start_date=datetime.now().isoformat(),
            last_active=datetime.now().isoformat(),
            scores={},
            achievements=[]
        )
        
        self.user_progress[user_id] = progress
        self._save_user_progress(user_id)
        
        return progress
    
    def get_recommended_path(self, user_level: LearningMode = None) -> LearningPath:
        """get推荐学习路径"""
        if user_level is None:
            user_level = LearningMode.BEGINNER
        
        # 根据用户水平推荐路径
        level_to_path = {
            LearningMode.BEGINNER: "path_tang_intro",
            LearningMode.INTERMEDIATE: "path_comprehensive",
            LearningMode.ADVANCED: "path_expert",
            LearningMode.EXPERT: "path_expert"
        }
        
        path_id = level_to_path.get(user_level, "path_tang_intro")
        return self.learning_paths[path_id]
    
    def get_current_module(self, user_id: str) -> Optional[LearningModule]:
        """get用户当前学习模块"""
        if user_id not in self.user_progress:
            return None
        
        current_module_id = self.user_progress[user_id].current_module
        if current_module_id in self.modules:
            return self.modules[current_module_id]
        
        return None
    
    def complete_module(self, user_id: str, module_id: str, score: float) -> bool:
        """完成学习模块"""
        if user_id not in self.user_progress:
            return False
        
        if module_id not in self.modules:
            return False
        
        progress = self.user_progress[user_id]
        
        # 记录完成
        if module_id not in progress.completed_modules:
            progress.completed_modules.append(module_id)
        
        # 记录分数
        progress.scores[module_id] = score
        
        # 更新当前模块
        learning_path = self.learning_paths[progress.learning_path]
        current_index = learning_path.modules.index(module_id) if module_id in learning_path.modules else -1
        
        if current_index >= 0 and current_index + 1 < len(learning_path.modules):
            progress.current_module = learning_path.modules[current_index + 1]
        else:
            progress.current_module = ""
        
        # 更新最后活跃时间
        progress.last_active = datetime.now().isoformat()
        
        # 检查成就
        self._check_achievements(user_id)
        
        # 保存进度
        self._save_user_progress(user_id)
        
        return True
    
    def _check_achievements(self, user_id: str):
        """检查并授予成就"""
        if user_id not in self.user_progress:
            return
        
        progress = self.user_progress[user_id]
        new_achievements = []
        
        # 完成第一个模块
        if len(progress.completed_modules) >= 1 and "first_module" not in progress.achievements:
            new_achievements.append("first_module")
        
        # 完成所有基础模块
        if len(progress.completed_modules) >= 3 and "basic_completed" not in progress.achievements:
            new_achievements.append("basic_completed")
        
        # 高分成就
        high_scores = [score for score in progress.scores.values() if score >= 90]
        if len(high_scores) >= 5 and "high_achiever" not in progress.achievements:
            new_achievements.append("high_achiever")
        
        # 添加新成就
        for achievement in new_achievements:
            if achievement not in progress.achievements:
                progress.achievements.append(achievement)
    
    def get_exercises_for_module(self, module_id: str, count: int = 5) -> List[Exercise]:
        """get模块相关练习题"""
        if module_id not in self.modules:
            return []
        
        module = self.modules[module_id]
        module_exercises = []
        
        for exercise_id in module.exercises:
            if exercise_id in self.exercises:
                module_exercises.append(self.exercises[exercise_id])
        
        # 如果数量不够,补充随机练习题
        if len(module_exercises) < count:
            available_exercises = list(self.exercises.values())
            random.shuffle(available_exercises)
            
            for exercise in available_exercises:
                if exercise not in module_exercises:
                    module_exercises.append(exercise)
                
                if len(module_exercises) >= count:
                    break
        
        return module_exercises[:count]
    
    def generate_practice_test(self, user_id: str, difficulty: LearningMode = None) -> Dict:
        """generate练习测试"""
        if user_id not in self.user_progress:
            return {}
        
        progress = self.user_progress[user_id]
        
        if difficulty is None:
            # 根据用户进度确定难度
            completed_count = len(progress.completed_modules)
            if completed_count < 3:
                difficulty = LearningMode.BEGINNER
            elif completed_count < 6:
                difficulty = LearningMode.INTERMEDIATE
            elif completed_count < 10:
                difficulty = LearningMode.ADVANCED
            else:
                difficulty = LearningMode.EXPERT
        
        # 筛选对应难度的练习题
        filtered_exercises = []
        for exercise in self.exercises.values():
            if exercise.difficulty == difficulty:
                filtered_exercises.append(exercise)
        
        # 随机选择题目
        test_size = min(10, len(filtered_exercises))
        selected_exercises = random.sample(filtered_exercises, test_size) if filtered_exercises else []
        
        # 计算总分
        total_points = sum(exercise.points for exercise in selected_exercises)
        
        return {
            "test_id": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "difficulty": difficulty.value,
            "exercises": [exercise.to_dict() for exercise in selected_exercises],
            "total_points": total_points,
            "estimated_time": test_size * 3,  # 每题3分钟
            "created_at": datetime.now().isoformat()
        }
    
    def evaluate_test(self, test_id: str, answers: Dict[str, str]) -> Dict:
        """评估测试结果"""
        # 在实际应用中,这里会根据test_idget原始测试题目
        # 这里简化处理,只返回示例结果
        
        correct_count = 0
        total_count = len(answers)
        score_details = []
        
        for exercise_id, user_answer in answers.items():
            if exercise_id in self.exercises:
                exercise = self.exercises[exercise_id]
                is_correct = (user_answer == exercise.correct_answer)
                
                if is_correct:
                    correct_count += 1
                
                score_details.append({
                    "exercise_id": exercise_id,
                    "question": exercise.question,
                    "user_answer": user_answer,
                    "correct_answer": exercise.correct_answer,
                    "is_correct": is_correct,
                    "points": exercise.points if is_correct else 0,
                    "explanation": exercise.explanation
                })
        
        total_score = (correct_count / total_count * 100) if total_count > 0 else 0
        
        # 评估学习水平
        if total_score >= 90:
            level = LearningMode.EXPERT
        elif total_score >= 75:
            level = LearningMode.ADVANCED
        elif total_score >= 60:
            level = LearningMode.INTERMEDIATE
        else:
            level = LearningMode.BEGINNER
        
        return {
            "test_id": test_id,
            "total_score": total_score,
            "correct_count": correct_count,
            "total_count": total_count,
            "learning_level": level.value,
            "score_details": score_details,
            "evaluated_at": datetime.now().isoformat()
        }
    
    def get_user_progress_report(self, user_id: str) -> Dict:
        """get用户进度报告"""
        if user_id not in self.user_progress:
            return {}
        
        progress = self.user_progress[user_id]
        learning_path = self.learning_paths.get(progress.learning_path)
        
        # 计算总体进度
        total_modules = len(learning_path.modules) if learning_path else 0
        completed_count = len(progress.completed_modules)
        overall_progress = (completed_count / total_modules * 100) if total_modules > 0 else 0
        
        # 计算平均分
        average_score = sum(progress.scores.values()) / len(progress.scores) if progress.scores else 0
        
        # 学习时间统计
        start_date = datetime.fromisoformat(progress.start_date)
        current_date = datetime.now()
        learning_days = (current_date - start_date).days
        
        return {
            "user_id": user_id,
            "learning_path": learning_path.to_dict() if learning_path else {},
            "overall_progress": overall_progress,
            "completed_modules": completed_count,
            "total_modules": total_modules,
            "current_module": progress.current_module,
            "average_score": average_score,
            "achievements": progress.achievements,
            "learning_days": learning_days,
            "last_active": progress.last_active,
            "module_details": [
                {
                    "module_id": module_id,
                    "module_name": self.modules[module_id].title if module_id in self.modules else "未知",
                    "score": progress.scores.get(module_id, 0),
                    "completed_date": "2026-04-02"  # 实际应用中应该记录完成日期
                }
                for module_id in progress.completed_modules
            ]
        }
    
    def get_recommendations(self, user_id: str) -> List[Dict]:
        """get学习推荐"""
        if user_id not in self.user_progress:
            return []
        
        progress = self.user_progress[user_id]
        recommendations = []
        
        # 基于进度推荐
        if len(progress.completed_modules) == 0:
            recommendations.append({
                "type": "start",
                "title": "开始学习之旅",
                "description": "建议从唐代诗歌入门开始学习",
                "priority": "high",
                "action": "开始学习"
            })
        
        # 基于分数推荐
        low_score_modules = []
        for module_id, score in progress.scores.items():
            if score < 60:
                low_score_modules.append(module_id)
        
        if low_score_modules:
            for module_id in low_score_modules[:2]:  # 最多推荐2个
                module = self.modules.get(module_id)
                if module:
                    recommendations.append({
                        "type": "review",
                        "title": f"复习 {module.title}",
                        "description": f"该模块得分较低,建议复习巩固",
                        "priority": "medium",
                        "action": "重新学习"
                    })
        
        # 基于成就推荐
        if "basic_completed" in progress.achievements and "advanced_started" not in progress.achievements:
            recommendations.append({
                "type": "advance",
                "title": "进入进阶学习",
                "description": "基础模块已完成,可以开始进阶学习了",
                "priority": "high",
                "action": "查看进阶路径"
            })
        
        return recommendations
    
    def _save_user_progress(self, user_id: str):
        """保存用户进度到文件"""
        if user_id not in self.user_progress:
            return
        
        filepath = os.path.join(self.data_dir, f"user_{user_id}_progress.json")
        progress_data = self.user_progress[user_id].to_dict()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=2)
    
    def _load_user_progress(self, user_id: str):
        """从文件加载用户进度"""
        filepath = os.path.join(self.data_dir, f"user_{user_id}_progress.json")
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
            
            progress = UserProgress(
                user_id=progress_data["user_id"],
                completed_modules=progress_data["completed_modules"],
                current_module=progress_data["current_module"],
                learning_path=progress_data["learning_path"],
                start_date=progress_data["start_date"],
                last_active=progress_data["last_active"],
                scores=progress_data["scores"],
                achievements=progress_data["achievements"]
            )
            
            self.user_progress[user_id] = progress
    
    def export_learning_data(self, user_id: str = None) -> Dict:
        """导出学习数据"""
        if user_id:
            # 导出单个用户数据
            if user_id in self.user_progress:
                return {
                    "user_data": self.user_progress[user_id].to_dict(),
                    "metadata": {
                        "exported_at": datetime.now().isoformat(),
                        "data_type": "user_learning_data"
                    }
                }
            return {}
        else:
            # 导出系统数据
            return {
                "learning_paths": [path.to_dict() for path in self.learning_paths.values()],
                "modules": [module.to_dict() for module in self.modules.values()],
                "exercises": [exercise.to_dict() for exercise in self.exercises.values()],
                "metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "data_type": "system_learning_data",
                    "data_source": "唐诗宋词50大家深度学习研究项目"
                }
            }

# 示例使用
def demo_education_app():
    """演示教育应用功能"""
    print("init诗词教育应用...")
    app = PoetryEducationApp()
    
    # 注册新用户
    print("\n1. 注册新用户...")
    user_id = "user_001"
    progress = app.register_user(user_id, "path_tang_intro")
    print(f"用户 {user_id} 注册成功")
    print(f"学习路径: {progress.learning_path}")
    print(f"当前模块: {progress.current_module}")
    
    # get当前学习模块
    print("\n2. get当前学习模块...")
    current_module = app.get_current_module(user_id)
    if current_module:
        print(f"模块标题: {current_module.title}")
        print(f"模块描述: {current_module.description}")
        print(f"预计学习时间: {current_module.estimated_time}分钟")
    
    # get练习题
    print("\n3. get练习题...")
    exercises = app.get_exercises_for_module("mod_tang_overview", count=3)
    print(f"get到 {len(exercises)} 道练习题")
    for i, exercise in enumerate(exercises, 1):
        print(f"\n练习 {i}: {exercise.question}")
        if exercise.exercise_type == ExerciseType.MULTIPLE_CHOICE:
            print(f"选项: {exercise.options}")
        print(f"正确答案: {exercise.correct_answer}")
    
    # 完成模块
    print("\n4. 完成模块...")
    app.complete_module(user_id, "mod_tang_overview", 85.0)
    
    # get进度报告
    print("\n5. get进度报告...")
    progress_report = app.get_user_progress_report(user_id)
    print(f"总体进度: {progress_report['overall_progress']:.1f}%")
    print(f"已完成模块: {progress_report['completed_modules']}/{progress_report['total_modules']}")
    print(f"平均分: {progress_report['average_score']:.1f}")
    
    # get学习推荐
    print("\n6. get学习推荐...")
    recommendations = app.get_recommendations(user_id)
    print(f"获得 {len(recommendations)} 条推荐")
    for rec in recommendations:
        print(f"  - [{rec['priority'].upper()}] {rec['title']}: {rec['description']}")
    
    # generate练习测试
    print("\n7. generate练习测试...")
    practice_test = app.generate_practice_test(user_id, LearningMode.BEGINNER)
    print(f"测试ID: {practice_test['test_id']}")
    print(f"难度: {practice_test['difficulty']}")
    print(f"题目数量: {len(practice_test['exercises'])}")
    print(f"总分: {practice_test['total_points']}")
    
    # 导出学习数据
    print("\n8. 导出学习数据...")
    learning_data = app.export_learning_data(user_id)
    print(f"数据导出完成,包含 {len(learning_data.get('user_data', {}).get('completed_modules', []))} 个已完成模块")
    
    print("\n诗词教育应用演示完成!")

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
