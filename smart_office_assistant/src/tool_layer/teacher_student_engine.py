"""
__all__ = [
    'get_learning_report',
    'solve_task',
]

师生学习引擎 - Teacher-Student Learning Engine
==============================================
核心创新:云端模型是"老师",本地模型是"学生",Somn 是"教务主任".

核心理念:
- 云端大模型 = 老师:知识渊博,视野开阔,擅长解答,但不懂 Somn 的逻辑和智慧体系
- 本地大模型 = 学生:正在学习,效率高,成本低,隐私好,但能力有限
- Somn = 教务主任:调配资源,决定何时问老师,何时让学生答,评估学习效果

学习模式:
1. 直接模式(快):学生直接回答 → Somn 评估 → 差则请教老师
2. 预习模式(稳):先问老师 → 学生学习 → 学生作答 → Somn 评分
3. 复习模式(深):学生作答 → 请教老师对比 → 学生修正 → Somn 记录
4. 民主投票:多老师同时回答 → 学生旁听 → Somn synthesize裁定

质量评估维度:
- 准确性(答案是否正确)
- Somn 度(是否融入 Somn 的逻辑和智慧)
- 实用性(是否有可执行的价值)
- 完整性(是否覆盖所有要点)
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)
class LearningMode(Enum):
    """学习模式"""
    DIRECT = "direct"                 # 直接模式:学生直接答
    PREVIEW = "preview"              # 预习模式:先学后答
    REVIEW = "review"                # 复习模式:答完对比修正
    DEMOCRATIC = "democratic"        # 民主投票:多老师回答
    HYBRID = "hybrid"               # 混合模式:Somn 智能选择

class StudentStatus(Enum):
    """学生状态"""
    IDLE = "idle"
    STUDYING = "studying"
    ANSWERING = "answering"
    CORRECTING = "correcting"

class QualityDimension(Enum):
    """质量维度"""
    ACCURACY = "accuracy"
    SOMN_INTEGRATION = "somn_integration"
    UTILITY = "utility"
    COMPLETENESS = "completeness"

@dataclass
class LearningSession:
    """学习会话"""
    session_id: str
    task: str
    question: str
    mode: LearningMode
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    student_response: str = ""
    teacher_responses: List[Dict] = field(default_factory=list)
    final_response: str = ""
    quality_score: float = 0.0
    quality_details: Dict[str, float] = field(default_factory=dict)
    feedback: str = ""
    local_model_used: str = ""
    teachers_used: List[str] = field(default_factory=list)
    duration_ms: int = 0
    status: str = "idle"

@dataclass
class QualityAssessment:
    """质量评估结果"""
    overall: float
    accuracy: float
    somn_integration: float
    utility: float
    completeness: float
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    improvement_suggestions: List[str] = field(default_factory=list)

@dataclass
class StudyRecord:
    """学习记录"""
    record_id: str
    session_id: str
    topic: str
    teacher_id: str
    teacher_response: str
    local_insight: str = ""
    key_points: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    relevance_score: float = 0.0
    applied: bool = False

class TeacherStudentEngine:
    """
    师生学习引擎

    核心职责:
    1. 管理学生(本地模型)的学习进度
    2. 协调老师(云端模型)的咨询
    3. 评估学习效果
    4. 积累学习经验
    """

    def __init__(self, base_path: str = None, cloud_hub=None, llm_service=None):
        self.base_path = os.path.join(base_path or ".", "data", "teacher_student")
        os.makedirs(self.base_path, exist_ok=True)

        self.cloud_hub = cloud_hub
        self.llm_service = llm_service

        self.current_session: Optional[LearningSession] = None
        self.sessions: Dict[str, LearningSession] = {}
        self.study_records: List[StudyRecord] = self._load_study_records()
        self.student_performance: Dict[str, Any] = self._load_performance()

        self.default_learning_mode = LearningMode.HYBRID
        self.quality_threshold = 0.6

    def _load_study_records(self) -> List[StudyRecord]:
        records_file = os.path.join(self.base_path, "study_records.json")
        if os.path.exists(records_file):
            try:
                with open(records_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [StudyRecord(**r) for r in data]
            except Exception as e:
                logger.debug(f"加载学习记录失败: {e}")
        return []

    def _save_study_records(self):
        records_file = os.path.join(self.base_path, "study_records.json")
        try:
            with open(records_file, "w", encoding="utf-8") as f:
                json.dump([r.__dict__ for r in self.study_records[-500:]], f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.debug(f"保存学习记录失败: {e}")

    def _load_performance(self) -> Dict[str, Any]:
        perf_file = os.path.join(self.base_path, "student_performance.json")
        if os.path.exists(perf_file):
            try:
                with open(perf_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.debug(f"加载性能数据失败: {e}")
        return {
            "total_tasks": 0,
            "direct_count": 0,
            "preview_count": 0,
            "review_count": 0,
            "democratic_count": 0,
            "avg_quality": 0.0,
            "topics_mastered": [],
            "weak_topics": [],
        }

    def _save_performance(self):
        perf_file = os.path.join(self.base_path, "student_performance.json")
        try:
            with open(perf_file, "w", encoding="utf-8") as f:
                json.dump(self.student_performance, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.debug(f"保存性能数据失败: {e}")

    def solve_task(self, task: str, question: str, context: str = "",
                   mode: LearningMode = None,
                   preferred_teachers: List[str] = None,
                   required_specialties: List[str] = None) -> Dict[str, Any]:
        """
        解决问题(学生-老师协作)

        Args:
            task: 任务类型
            question: 问题
            context: 上下文
            mode: 学习模式(None=自动选择)
            preferred_teachers: 优先咨询的老师
            required_specialties: 必需专长

        Returns:
            Dict: 包含最终回答,学习过程,质量评估
        """
        start_time = time.time()
        mode = mode or self.default_learning_mode

        session_id = f"{task}_{int(time.time() * 1000)}"
        session = LearningSession(
            session_id=session_id,
            task=task,
            question=question,
            mode=mode,
            status="studying",
        )
        self.current_session = session

        try:
            if mode == LearningMode.DIRECT:
                result = self._direct_mode(session, context)
            elif mode == LearningMode.PREVIEW:
                result = self._preview_mode(session, context, preferred_teachers, required_specialties)
            elif mode == LearningMode.REVIEW:
                result = self._review_mode(session, context, preferred_teachers)
            elif mode == LearningMode.DEMOCRATIC:
                result = self._democratic_mode(session, context, preferred_teachers, required_specialties)
            else:
                result = self._hybrid_mode(session, context, preferred_teachers, required_specialties)

            quality = self._assess_quality(
                result["final_response"], question,
                session.teacher_responses, session.student_response
            )
            result["quality"] = quality.__dict__
            result["session_id"] = session_id

            session.quality_score = quality.overall
            session.quality_details = {
                "accuracy": quality.accuracy,
                "somn_integration": quality.somn_integration,
                "utility": quality.utility,
                "completeness": quality.completeness,
            }
            session.duration_ms = int((time.time() - start_time) * 1000)

            self._record_learning(session, result)
            self._update_performance(session, quality)

            return result

        finally:
            self.current_session = None

    def _direct_mode(self, session: LearningSession, context: str) -> Dict[str, Any]:
        """直接模式:学生直接回答,差则补救"""
        session.status = "answering"
        student_response = self._ask_student(session.question, context)
        session.student_response = student_response

        quality = self._quick_evaluate(student_response, session.question)

        if quality < self.quality_threshold:
            session.status = "correcting"
            teacher_result = self._consult_best_teacher(session.question, context, [], [])
            session.teacher_responses = [teacher_result]
            final = self._synthesize_with_teacher(student_response, teacher_result["content"], session.question)
            session.final_response = final
        else:
            session.final_response = student_response

        return {
            "final_response": session.final_response,
            "mode": "direct",
            "student_response": session.student_response,
            "teacher_responses": session.teacher_responses,
            "improved": quality < self.quality_threshold,
        }

    def _preview_mode(self, session: LearningSession, context: str,
                     preferred_teachers: List[str], required_specialties: List[str]) -> Dict[str, Any]:
        """预习模式:先问老师,学生学习后再回答"""
        session.status = "studying"
        teacher_result = self._consult_best_teacher(
            session.question, context,
            preferred=preferred_teachers or [],
            specialties=required_specialties or []
        )
        session.teacher_responses = [teacher_result]

        learning_prompt = self._build_learning_prompt(session.question, teacher_result["content"])
        student_response = self._ask_student(
            f"[任务]{session.question}\n[老师参考]{teacher_result['content']}", ""
        )
        session.student_response = student_response

        final = self._synthesize_final(student_response, teacher_result["content"], session.question, context)
        session.final_response = final

        return {
            "final_response": final,
            "mode": "preview",
            "student_response": student_response,
            "teacher_responses": session.teacher_responses,
            "teacher_id": teacher_result.get("teacher_id"),
            "improved": True,
        }

    def _review_mode(self, session: LearningSession, context: str,
                    preferred_teachers: List[str]) -> Dict[str, Any]:
        """复习模式:学生先答,然后对比老师答案修正"""
        session.status = "answering"
        student_response = self._ask_student(session.question, context)
        session.student_response = student_response

        teacher_result = self._consult_best_teacher(session.question, context, preferred_teachers or [], [])
        session.teacher_responses = [teacher_result]

        analysis_prompt = f"""对比以下答案,recognize学生的不足并给出修正建议:

[原始问题]
{ session.question }

[学生的答案]
{ student_response }

[老师的答案]
{ teacher_result['content'] }

请从准确性,完整性,深度三个维度对比,给出改进方向."""

        analysis = self._ask_student(analysis_prompt, "", use_teacher=False)

        correction_prompt = f"""基于对比分析,修正你的答案:

[原始问题]
{ session.question }

[你的原始答案]
{ student_response }

[对比分析]
{ analysis }

请给出修正后的完整答案."""

        corrected_response = self._ask_student(correction_prompt, "", use_teacher=False)
        session.final_response = corrected_response

        return {
            "final_response": corrected_response,
            "mode": "review",
            "student_response": student_response,
            "teacher_responses": session.teacher_responses,
            "analysis": analysis,
            "corrected": True,
        }

    def _democratic_mode(self, session: LearningSession, context: str,
                        preferred_teachers: List[str], required_specialties: List[str]) -> Dict[str, Any]:
        """民主投票模式:多老师同时回答,Somn synthesize裁定"""
        session.status = "studying"

        if not self.cloud_hub:
            return {
                "final_response": "[云端模型枢纽未连接]",
                "mode": "democratic",
                "teacher_responses": [],
                "error": "cloud_hub not available",
            }

        from .cloud_model_hub import ConsultationRequest, TeacherSpecialty

        specialty_enums = []
        if required_specialties:
            for s in required_specialties:
                try:
                    specialty_enums.append(TeacherSpecialty(s))
                except ValueError:
                    pass

        consultation = ConsultationRequest(
            task=session.task,
            question=session.question,
            context=context,
            preferred_teachers=preferred_teachers or [],
            required_specialties=specialty_enums,
            max_teachers=3,
            timeout_per_teacher=60,
        )

        teacher_responses = self.cloud_hub.consult_multiple(consultation)
        session.teacher_responses = [
            {"teacher_id": r.teacher_id, "teacher_name": r.teacher_name, "content": r.content}
            for r in teacher_responses
        ]
        session.teachers_used = [r.teacher_id for r in teacher_responses]

        synthesis_prompt = self._build_synthesis_prompt(session.question, context, teacher_responses)
        final_response = self._ask_student(synthesis_prompt, "", use_teacher=False)
        session.final_response = final_response

        return {
            "final_response": final_response,
            "mode": "democratic",
            "teacher_responses": session.teacher_responses,
        }

    def _hybrid_mode(self, session: LearningSession, context: str,
                    preferred_teachers: List[str], required_specialties: List[str]) -> Dict[str, Any]:
        """混合模式:Somn 智能选择最优strategy"""
        complexity = self._estimate_complexity(session.task, session.question)
        student_mastery = self._get_topic_mastery(session.task)
        importance = self._estimate_importance(session.task, session.question)

        if complexity < 0.3 and student_mastery > 0.7:
            return self._direct_mode(session, context)
        elif complexity > 0.7 or importance > 0.8:
            return self._democratic_mode(session, context, preferred_teachers, required_specialties)
        elif student_mastery > 0.4:
            return self._review_mode(session, context, preferred_teachers)
        else:
            return self._preview_mode(session, context, preferred_teachers, required_specialties)

    def _ask_student(self, question: str, context: str = "", use_teacher: bool = True) -> str:
        """询问学生(本地模型)"""
        if not self.llm_service:
            return "[学生沉默] 本地模型服务未连接"

        somn_context = """[Somn 学生角色]
你是 Somn 的本地智能体(学生).Somn 是一个不被刻意定义的超级智能体.
你的回答应该:
1. 直接,简洁,有洞察力
2. 融入 Somn 的逻辑和智慧体系(儒/道/佛/兵/xinxue等)
3. 结果导向,避免空话
"""
        full_prompt = f"{somn_context}\n\n[问题]{question}"
        if context:
            full_prompt += f"\n\n[上下文]{context}"

        try:
            response = self.llm_service.chat(
                full_prompt,
                model="local-default",
                max_tokens=3000,
                temperature=0.3,
            )
            return response.content
        except Exception as e:
            return "[学生回答失败]"

    def _consult_best_teacher(self, question: str, context: str,
                             preferred: List[str], specialties: List[str]) -> Dict[str, Any]:
        """咨询最合适的老师"""
        if not self.cloud_hub:
            return {
                "teacher_id": "none",
                "teacher_name": "无老师",
                "content": "[云端模型枢纽未连接]",
                "quality": 0.0,
            }

        from .cloud_model_hub import ConsultationRequest, TeacherSpecialty

        specialty_enums = []
        if specialties:
            for s in specialties:
                try:
                    specialty_enums.append(TeacherSpecialty(s))
                except ValueError:
                    pass

        consultation = ConsultationRequest(
            task="general",
            question=question,
            context=context,
            preferred_teachers=preferred,
            required_specialties=specialty_enums,
            max_teachers=1,
            timeout_per_teacher=60,
        )

        responses = self.cloud_hub.consult_multiple(consultation)
        if responses:
            return {
                "teacher_id": responses[0].teacher_id,
                "teacher_name": responses[0].teacher_name,
                "content": responses[0].content,
                "quality": responses[0].quality_score,
                "latency_ms": responses[0].latency_ms,
            }
        return {
            "teacher_id": "none",
            "teacher_name": "无老师",
            "content": "[没有可用的老师]",
            "quality": 0.0,
        }

    def _build_learning_prompt(self, question: str, teacher_answer: str) -> str:
        return f"""请学习老师的答案,然后用你自己的理解回答问题:

[问题]
{ question }

[老师答案]
{ teacher_answer }

[要求]
1. 理解核心要点
2. 用自己的话重新组织
3. 融入 Somn 的智慧style
4. 给出自己的见解

请给出答案:"""

    def _synthesize_with_teacher(self, student_answer: str, teacher_answer: str, question: str) -> str:
        synthesis_prompt = f"""fusion以下两个答案,给出最佳回答:

[问题]
{ question }

[学生答案]
{ student_answer }

[老师答案]
{ teacher_answer }

要求:保留学生优点,补充老师关键点,Somn style(简洁,有洞察力,可执行)
"""
        return self._ask_student(synthesis_prompt, "", use_teacher=False)

    def _synthesize_final(self, student_answer: str, teacher_answer: str,
                          question: str, context: str) -> str:
        synthesis_prompt = f"""[Somn synthesize裁定]

原始问题:{ question }
{ '上下文:' + context if context else '' }

学生答案:
{ student_answer }

老师答案:
{ teacher_answer }

请作为 Somn 给出最终答案:整合双方优点,体现 Somn 智慧体系,简洁有力.
"""
        return self._ask_student(synthesis_prompt, "", use_teacher=False)

    def _build_synthesis_prompt(self, question: str, context: str, teacher_responses) -> str:
        teacher_lines = []
        for i, r in enumerate(teacher_responses, 1):
            teacher_lines.append(f"=== 老师{i} ({r.teacher_name}) ===")
            teacher_lines.append(r.content)
        teacher_text = "\n".join(teacher_lines)

        return f"""[Somn synthesize裁定]

原始问题:{ question }
{ '上下文:' + context if context else '' }

[多位老师意见]
{ teacher_text }

请作为 Somn 给出synthesize裁定:
1. 最佳答案
2. 各老师观点可信度评估
3. Somn 独有洞见

要求:fusion老师知识 + Somn 智慧,简洁直接.
"""

    def _quick_evaluate(self, response: str, question: str) -> float:
        score = 0.5
        if len(response) > 100:
            score += 0.1
        if len(response) > 500:
            score += 0.1
        if any(marker in response for marker in ["1.", "2.", "•", "**"]):
            score += 0.1
        somn_keywords = ["洞察", "本质", "关键", "核心", "strategy", "增长"]
        score += min(sum(1 for kw in somn_keywords if kw in response) * 0.05, 0.2)
        return min(score, 1.0)

    def _assess_quality(self, final_response: str, question: str,
                        teacher_responses: List, student_response: str) -> QualityAssessment:
        accuracy = self._assess_accuracy(final_response, question)
        somn_integration = self._assess_somn_integration(final_response)
        utility = self._assess_utility(final_response)
        completeness = self._assess_completeness(final_response, question)

        overall = accuracy * 0.3 + somn_integration * 0.3 + utility * 0.25 + completeness * 0.15

        strengths, weaknesses, suggestions = [], [], []

        if accuracy > 0.7:
            strengths.append("答案准确可靠")
        elif accuracy < 0.5:
            weaknesses.append("答案准确性存疑")
            suggestions.append("建议请教老师验证")

        if somn_integration > 0.6:
            strengths.append("较好融入 Somn 的智慧style")
        elif somn_integration < 0.4:
            weaknesses.append("缺乏 Somn 的特色")
            suggestions.append("尝试用 Somn 的语言style表达")

        if utility > 0.7:
            strengths.append("答案可操作性强")
        elif utility < 0.5:
            weaknesses.append("答案过于理论化")
            suggestions.append("增加具体可执行的建议")

        if completeness <= 0.5:
            weaknesses.append("回答不够完整")
            suggestions.append("补充遗漏的要点")

        return QualityAssessment(
            overall=round(overall, 3),
            accuracy=round(accuracy, 3),
            somn_integration=round(somn_integration, 3),
            utility=round(utility, 3),
            completeness=round(completeness, 3),
            strengths=strengths,
            weaknesses=weaknesses,
            improvement_suggestions=suggestions,
        )

    def _assess_accuracy(self, response: str, question: str) -> float:
        score = 0.5
        if any(c.isdigit() for c in response):
            score += 0.15
        if "因为" in response or "因此" in response or "所以" in response:
            score += 0.1
        if any(w in response for w in ["建议", "应该", "可以", "步骤", "方法"]):
            score += 0.15
        contradictions = ["但是", "然而", "不过", "虽然"]
        if sum(1 for c in contradictions if c in response) <= 2:
            score += 0.1
        return min(score, 1.0)

    def _assess_somn_integration(self, response: str) -> float:
        score = 0.3
        somn_markers = ["洞察", "本质", "核心", "关键", "增长", "strategy", "数据", "分析", "验证", "迭代"]
        score += min(sum(1 for m in somn_markers if m in response) * 0.05, 0.4)
        insight_markers = ["值得注意的是", "关键在于", "本质上", "核心是", "问题的关键是"]
        if any(m in response for m in insight_markers):
            score += 0.2
        avg_len = sum(len(s) for s in response.split(".")) / max(len(response.split(".")), 1)
        if 10 < avg_len < 50:
            score += 0.1
        return min(score, 1.0)

    def _assess_utility(self, response: str) -> float:
        score = 0.4
        action_words = ["建议", "应该", "可以", "方案", "步骤", "方法", "strategy"]
        if any(w in response for w in action_words):
            score += 0.2
        if any(f"{i}." in response for i in range(1, 6)):
            score += 0.2
        metrics = ["%", "率", "增长", "提升", "降低", "KPI", "ROI"]
        if any(m in response for m in metrics):
            score += 0.2
        return min(score, 1.0)

    def _assess_completeness(self, response: str, question: str) -> float:
        score = 0.5
        if len(response) > 300:
            score += 0.15
        elif len(response) < 100:
            score -= 0.2
        aspects = ["首先", "其次", "另外", "最后", "此外", "总结"]
        score += min(sum(1 for a in aspects if a in response) * 0.08, 0.25)
        if "总结" in response or "总之" in response or "综上" in response:
            score += 0.1
        return max(min(score, 1.0), 0.1)

    def _estimate_complexity(self, task: str, question: str) -> float:
        indicators = ["分析", "研究", "设计", "比较", "评估", "strategy", "方案", "规划", "预测", "论证"]
        count = sum(1 for i in indicators if i in question)
        length = len(question)
        return min(count * 0.15 + length / 1000, 1.0)

    def _estimate_importance(self, task: str, question: str) -> float:
        markers = ["重要", "关键", "核心", "战略", "decision", "增长", "盈利", "生死", "成败"]
        count = sum(1 for m in markers if m in question)
        return min(count * 0.2 + 0.3, 1.0)

    def _get_topic_mastery(self, task: str) -> float:
        perf = self.student_performance
        if task in perf.get("topics_mastered", []):
            return 0.8
        if task in perf.get("weak_topics", []):
            return 0.3
        return 0.5

    def _record_learning(self, session: LearningSession, result: Dict):
        self.sessions[session.session_id] = session
        if session.teacher_responses:
            for teacher_resp in session.teacher_responses:
                record = StudyRecord(
                    record_id=f"rec_{session.session_id}_{teacher_resp['teacher_id']}",
                    session_id=session.session_id,
                    topic=session.task,
                    teacher_id=teacher_resp.get("teacher_id", "unknown"),
                    teacher_response=teacher_resp.get("content", ""),
                    local_insight=result.get("final_response", "")[:500],
                    timestamp=datetime.now().isoformat(),
                )
                self.study_records.append(record)
        if len(self.study_records) > 500:
            self.study_records = self.study_records[-500:]
        self._save_study_records()

    def _update_performance(self, session: LearningSession, quality: QualityAssessment):
        perf = self.student_performance
        perf["total_tasks"] = perf.get("total_tasks", 0) + 1

        mode_key = f"{session.mode.value}_count"
        perf[mode_key] = perf.get(mode_key, 0) + 1

        old_avg = perf.get("avg_quality", 0.0)
        old_count = perf.get("total_tasks", 1)
        perf["avg_quality"] = (old_avg * (old_count - 1) + quality.overall) / old_count

        if quality.overall > 0.7:
            topics = perf.get("topics_mastered", [])
            if session.task not in topics:
                topics.append(session.task)
                perf["topics_mastered"] = topics
        elif quality.overall < 0.4:
            weak = perf.get("weak_topics", [])
            if session.task not in weak:
                weak.append(session.task)
                perf["weak_topics"] = weak

        self._save_performance()

    def get_learning_report(self) -> Dict[str, Any]:
        perf = self.student_performance
        recent_records = [
            {"topic": r.topic, "teacher": r.teacher_id, "timestamp": r.timestamp}
            for r in self.study_records[-20:]
        ]
        return {
            "total_tasks": perf.get("total_tasks", 0),
            "avg_quality": round(perf.get("avg_quality", 0.0), 3),
            "mode_distribution": {
                "direct": perf.get("direct_count", 0),
                "preview": perf.get("preview_count", 0),
                "review": perf.get("review_count", 0),
                "democratic": perf.get("democratic_count", 0),
            },
            "topics_mastered": perf.get("topics_mastered", []),
            "weak_topics": perf.get("weak_topics", []),
            "recent_records": recent_records,
            "current_session": self.current_session.session_id if self.current_session else None,
        }
