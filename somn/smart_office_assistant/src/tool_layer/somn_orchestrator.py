"""
__all__ = [
    'comprehensive_report',
    'get_kitchen_status',
    'quick_answer',
    'serve',
    'thoughtful_answer',
]

Somn 编排器 - Somn Orchestrator
===============================
核心:Somn = 磨坊 + 厨师
- 大模型+搜索 = 小麦(原材料)
- Somn = 磨坊+厨师(加工能力)
三种模式:快手菜(FAST)/家常菜(HOME)/大餐(FEAST)
"""

import json
import os
import time
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class CuisineMode(Enum):
    FAST = "fast"     # 快手菜:本地直答
    HOME = "home"     # 家常菜:本地+云端辅助
    FEAST = "feast"   # 大餐:多云端民主投票

class DishType(Enum):
    SOUP = "soup"
    NOODLES = "noodles"
    DUMPLINGS = "dumplings"
    BREAD = "bread"
    GOURMET = "gourmet"

@dataclass
class MenuRequest:
    dish_name: str
    hunger_level: str = "normal"
    dietary_preference: str = ""
    ingredients_available: str = ""
    allergies: List[str] = field(default_factory=list)
    dining_mode: str = "home"

@dataclass
class SomnResponse:
    dish_type: str
    content: str
    cuisine_mode: str
    ingredients_used: List[str] = field(default_factory=list)
    teachers_consulted: List[str] = field(default_factory=list)
    student_involved: bool = False
    cooking_time_ms: int = 0
    quality_stars: float = 0.0
    chef_notes: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class SomnOrchestrator:
    """Somn 编排器 - 磨坊 + 厨师"""

    def __init__(self, cloud_hub=None, teacher_student_engine=None, llm_service=None):
        self.cloud_hub = cloud_hub
        self.teacher_student_engine = teacher_student_engine
        self.llm_service = llm_service
        self.base_path = ".data/somn_orchestrator"
        os.makedirs(self.base_path, exist_ok=True)

    def serve(self, request: MenuRequest) -> SomnResponse:
        start_time = time.time()
        mode = self._decide_mode(request)
        dish = self._decide_dish(request)

        if mode == CuisineMode.FAST:
            result = self._cook_fast(request)
        elif mode == CuisineMode.FEAST:
            result = self._cook_feast(request)
        else:
            result = self._cook_home(request)

        q_overall = result.get("quality", {}).get("overall", 0.0)

        return SomnResponse(
            dish_type=dish.value,
            content=result.get("final_response", ""),
            cuisine_mode=mode.value,
            ingredients_used=result.get("ingredients_used", []),
            teachers_consulted=result.get("teachers_used", []),
            student_involved=result.get("student_involved", True),
            cooking_time_ms=int((time.time() - start_time) * 1000),
            quality_stars=q_overall * 5,
            chef_notes=self._generate_notes(result),
        )

    def _decide_mode(self, req: MenuRequest) -> CuisineMode:
        # User's explicit preference wins (only if not "home" - the default)
        mode_map = {"fast": CuisineMode.FAST, "feast": CuisineMode.FEAST}
        if req.dining_mode == "fast" or req.dining_mode == "feast":
            return mode_map[req.dining_mode]
        # "home" is the default - fall through to auto-detection

        # Auto-detect from keywords (no .lower() needed for Chinese)
        name = req.dish_name

        # 深度复杂任务 → FEAST(关键词更宽松,覆盖"深度分析"/"generate一份"/"研究报告"等)
        feast_keywords = [
            "研究", "分析报告", "深度", "论证", "全面", "系统",
            "generate一份", "generate一份详细", "详细的研究报告", "深度分析",
            "generate报告", "generate研究", "报告", "大餐", "完整", "完整分析", "系统性",
        ]
        for kw in feast_keywords:
            if kw in name:
                return CuisineMode.FEAST

        # 极短输入或纯问候 → FAST(默认)
        # 包括:问候,简单问答,闲聊(len ≤ 15 且无明确任务词)
        simple_keywords = [
            "你好", "您好", "hello", "hi", "hey", "天气", "查一下", "多少钱",
            "一句话", "简单", "快速", "怎么", "怎样", "如何", "是不是", "吗?",
            "?", "介绍一下", "是什么", "你是谁", "啥", "干哈",
        ]
        if len(name) <= 15 and any(kw in name for kw in simple_keywords):
            return CuisineMode.FAST

        # 中等复杂度 → HOME(任务驱动型)
        # 包含"帮我/给我/制定"等动作词 → 家常菜(本地+云端)
        home_keywords = ["帮我", "给我", "制定", "增长", "strategy", "方案", "评估", "建议", "分析"]
        for kw in home_keywords:
            if kw in name:
                return CuisineMode.HOME

        # Fallback to hunger-based
        hunger_map = {"light": CuisineMode.FAST, "normal": CuisineMode.HOME, "hungry": CuisineMode.FEAST}
        return hunger_map.get(req.hunger_level, CuisineMode.HOME)

    def _decide_dish(self, req: MenuRequest) -> DishType:
        name = req.dish_name.lower()
        if any(kw in name for kw in ["报告", "方案", "研究", "论证", "深度"]):
            return DishType.DUMPLINGS
        if any(kw in name for kw in ["分析", "对比", "strategy"]):
            return DishType.NOODLES
        if any(kw in name for kw in ["模板", "总结", "摘要"]):
            return DishType.BREAD
        return DishType.NOODLES

    def _cook_fast(self, req: MenuRequest) -> Dict[str, Any]:
        if not self.teacher_student_engine:
            return self._cook_llm_direct(req)
        from .teacher_student_engine import LearningMode
        result = self.teacher_student_engine.solve_task(
            task="fast", question=req.dish_name,
            context=req.ingredients_available,
            mode=LearningMode.DIRECT)
        result["ingredients_used"] = ["local_model"]
        result["teachers_used"] = []
        return result

    def _cook_home(self, req: MenuRequest) -> Dict[str, Any]:
        if not self.teacher_student_engine:
            return self._cook_llm_direct(req)
        from .teacher_student_engine import LearningMode
        mode = LearningMode.REVIEW if len(req.dish_name) < 100 else LearningMode.PREVIEW
        result = self.teacher_student_engine.solve_task(
            task="general", question=req.dish_name,
            context=req.ingredients_available, mode=mode)
        result["ingredients_used"] = ["local_model", "cloud_teacher"]
        return result

    def _cook_feast(self, req: MenuRequest) -> Dict[str, Any]:
        if not self.teacher_student_engine:
            return self._cook_llm_direct(req)
        from .teacher_student_engine import LearningMode
        result = self.teacher_student_engine.solve_task(
            task="deep", question=req.dish_name,
            context=req.ingredients_available,
            mode=LearningMode.DEMOCRATIC,
            required_specialties=["reasoning", "academic"])
        result["ingredients_used"] = ["local_model", "multiple_cloud_teachers"]
        return result

    def _cook_llm_direct(self, req: MenuRequest) -> Dict[str, Any]:
        if not self.llm_service:
            return {
                "final_response": "[Somn 厨房未营业] 本地模型和云端老师都不可用",
                "quality": {"overall": 0.1},
                "ingredients_used": [],
                "teachers_used": [],
                "student_involved": False,
            }
        try:
            response = self.llm_service.chat(
                req.dish_name,
                model="local-default",
                system_prompt=self._get_system_prompt(req),
                max_tokens=3000,
                temperature=0.3,
            )
            return {
                "final_response": response.content,
                "quality": {"overall": 0.6},
                "ingredients_used": ["local_model"],
                "teachers_used": [],
                "student_involved": True,
            }
        except Exception as e:
            return {
                "final_response": "[Somn 烹饪失败]",
                "quality": {"overall": 0.0},
                "ingredients_used": [],
                "teachers_used": [],
                "student_involved": False,
            }

    def _get_system_prompt(self, req: MenuRequest) -> str:
        pref = ("\n用户偏好:" + req.dietary_preference) if req.dietary_preference else ""
        ctx = ("\n上下文:" + req.ingredients_available) if req.ingredients_available else ""
        return (
            "你是 Somn,一个不被刻意定义的超级智能体.\n"
            "核心原则:直接简洁有洞察力,结果导向,融入 Somn 智慧(儒/道/佛/兵/xinxue),数据驱动.\n"
            "style:不说废话,开门见山,有洞见有深度." + pref + ctx
        )

    def _generate_notes(self, result: Dict) -> str:
        q = result.get("quality", {})
        overall = q.get("overall", 0.0)
        mode = result.get("mode", "unknown")
        teachers = result.get("teachers_used", [])
        if overall >= 0.8:
            qstr = "精品"
        elif overall >= 0.6:
            qstr = "品质"
        elif overall >= 0.4:
            qstr = "待改进"
        else:
            qstr = "返工"
        mstr = {"direct": "快手", "preview": "预习", "review": "复习", "democratic": "民主"}.get(mode, mode)
        if teachers:
            tstr = "请教了" + str(len(teachers)) + "位老师"
        else:
            tstr = "独立完成"
        return qstr + " | " + mstr + "模式 | " + tstr

    def quick_answer(self, question: str) -> str:
        req = MenuRequest(dish_name=question, hunger_level="light", dining_mode="fast")
        return self.serve(req).content

    def thoughtful_answer(self, question: str, context: str = "") -> str:
        req = MenuRequest(dish_name=question, hunger_level="normal", dining_mode="home",
                         ingredients_available=context)
        return self.serve(req).content

    def comprehensive_report(self, topic: str, context: str = "") -> str:
        req = MenuRequest(dish_name=topic, hunger_level="hungry", dining_mode="feast",
                         ingredients_available=context)
        return self.serve(req).content

    def get_kitchen_status(self) -> Dict[str, Any]:
        status = {
            "modes": {"fast": "快手菜(本地直答)", "home": "家常菜(本地+云端)", "feast": "大餐(多云端民主)"},
            "dishes": [d.value for d in DishType],
        }
        if self.teacher_student_engine:
            r = self.teacher_student_engine.get_learning_report()
            status["learning"] = {
                "total_tasks": r.get("total_tasks", 0),
                "avg_quality": r.get("avg_quality", 0.0),
                "mastered_topics": len(r.get("topics_mastered", [])),
            }
        if self.cloud_hub:
            teachers = self.cloud_hub.list_teachers(available_only=True)
            status["teachers_available"] = len(teachers)
            status["teacher_list"] = [{"id": t["teacher_id"], "name": t["name"]} for t in teachers[:5]]
        return status
