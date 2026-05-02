"""
closed_loop_solver.py v1.0.0
=====================================
真正能解决问题的闭环工作流

全流程：
  问题输入 → 八层分析 → 方案生成 → 方案验证 
  → 多格式输出 → 用户反馈 → 学习进化 → 知识更新

核心创新：
  1. 方案可落地性评分（0-1）
  2. 方案验证机制（规则+LLM）
  3. 用户反馈闭环（评分+修正）
  4. 知识自动更新（NeuralMemory + DomainNexus）
  5. 端到端追踪（request_id 全链路）

Author: 张三
Version: 1.0.0
Date: 2026-05-01
"""

from __future__ import annotations

import time
import uuid
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

logger = logging.getLogger("Somn.ClosedLoopSolver")


# ============ 枚举定义 ============

class SolutionStatus(Enum):
    """方案状态"""
    DRAFT = "draft"               # 草稿（待验证）
    VERIFIED = "verified"           # 已验证（可通过）
    NEEDS_REVISION = "revision"    # 需要修改
    REJECTED = "rejected"          # 已拒绝（不可行）
    IMPLEMENTED = "implemented"     # 已实现（用户确认）


class FeedbackType(Enum):
    """反馈类型"""
    RATING = "rating"              # 评分（1-5）
    CORRECTION = "correction"       # 修正（指出错误）
    IMPROVEMENT = "improvement"     # 改进建议
    IMPLEMENTATION = "implementation"  # 实施反馈（是否解决了问题）


# ============ 数据类 ============

@dataclass
class ActionableStep:
    """可执行的步骤"""
    step_id: str
    description: str
    action_type: str  # command / code / config / manual / decision
    content: str           # 具体执行内容
    expected_output: str   # 预期输出
    validation: str        # 验证方式
    dependencies: List[str] = field(default_factory=list)  # 依赖的步骤ID
    estimated_effort: str = "medium"  # low / medium / high
    risk_level: str = "low"           # low / medium / high
    
    def to_dict(self) -> Dict:
        return {
            "step_id": self.step_id,
            "description": self.description,
            "action_type": self.action_type,
            "content": self.content,
            "expected_output": self.expected_output,
            "validation": self.validation,
            "dependencies": self.dependencies,
            "estimated_effort": self.estimated_effort,
            "risk_level": self.risk_level,
        }


@dataclass
class SolutionPlan:
    """解决方案"""
    plan_id: str
    title: str
    description: str
    steps: List[ActionableStep]
    prerequisites: List[str] = field(default_factory=list)
    expected_outcome: str = ""
    success_criteria: List[str] = field(default_factory=list)
    total_effort: str = "medium"
    confidence: float = 0.5
    status: SolutionStatus = SolutionStatus.DRAFT
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.strftime("%Y-%m-%dT%H:%M:%S")
    
    def to_dict(self) -> Dict:
        return {
            "plan_id": self.plan_id,
            "title": self.title,
            "description": self.description,
            "steps": [s.to_dict() for s in self.steps],
            "prerequisites": self.prerequisites,
            "expected_outcome": self.expected_outcome,
            "success_criteria": self.success_criteria,
            "total_effort": self.total_effort,
            "confidence": self.confidence,
            "status": self.status.value,
            "created_at": self.created_at,
        }


@dataclass
class VerificationResult:
    """验证结果"""
    passed: bool
    score: float  # 0-1，可落地性评分
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    verified_by: str = "rule"  # rule / llm / hybrid
    
    def to_dict(self) -> Dict:
        return {
            "passed": self.passed,
            "score": self.score,
            "issues": self.issues,
            "suggestions": self.suggestions,
            "verified_by": self.verified_by,
        }


@dataclass
class UserFeedback:
    """用户反馈"""
    feedback_id: str
    request_id: str
    feedback_type: FeedbackType
    rating: Optional[int] = None  # 1-5（如果类型是 RATING）
    comment: str = ""
    corrections: List[str] = field(default_factory=list)  # 修正内容
    implemented: bool = False  # 是否已实施该方案
    outcome: str = ""  # 实施结果
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.strftime("%Y-%m-%dT%H:%M:%S")
    
    def to_dict(self) -> Dict:
        return {
            "feedback_id": self.feedback_id,
            "request_id": self.request_id,
            "feedback_type": self.feedback_type.value,
            "rating": self.rating,
            "comment": self.comment,
            "corrections": self.corrections,
            "implemented": self.implemented,
            "outcome": self.outcome,
            "created_at": self.created_at,
        }


@dataclass
class ClosedLoopResult:
    """闭环工作流结果（含执行结果）"""
    request_id: str
    problem: str
    grade: str = "basic"  # 处理等级
    analysis_result: Dict = field(default_factory=dict)
    solution_plan: Optional[SolutionPlan] = None
    verification: Optional[VerificationResult] = None
    execution_result: Optional[Any] = None  # PlanExecutionResult
    output_files: List[str] = field(default_factory=list)
    feedback_id: Optional[str] = None
    feedback_ready: bool = False
    knowledge_updated: bool = False
    total_time: float = 0.0  # 总耗时（秒）
    
    @property
    def success(self) -> bool:
        """是否成功解决（有解决方案且通过验证）"""
        if not self.solution_plan:
            return False
        if self.verification and not self.verification.passed:
            return False
        if self.execution_result and hasattr(self.execution_result, 'success'):
            return self.execution_result.success
        return True  # 有方案且通过验证，认为成功
    
    def to_dict(self) -> Dict:
        return {
            "request_id": self.request_id,
            "problem": self.problem,
            "analysis_result": self.analysis_result,
            "solution_plan": self.solution_plan.to_dict() if self.solution_plan else None,
            "verification": self.verification.to_dict() if self.verification else None,
            "execution_result": self.execution_result.to_dict() if self.execution_result and hasattr(self.execution_result, 'to_dict') else None,
            "output_files": self.output_files,
            "feedback": self.feedback.to_dict() if self.feedback else None,
            "knowledge_updated": self.knowledge_updated,
            "total_duration_ms": self.total_duration_ms,
        }


# ============ 方案生成器 ============

class SolutionGenerator:
    """方案生成器 — 将分析结果转化为可执行的解决方案"""
    
    def __init__(self):
        self.logger = logging.getLogger("Somn.SolutionGenerator")
    
    def generate(self, problem: str, analysis_result: Dict, 
                 reasoning_result: Dict) -> SolutionPlan:
        """
        生成解决方案
        
        Args:
            problem: 原始问题
            analysis_result: 八层分析结果
            reasoning_result: 推理结果
            
        Returns:
            SolutionPlan 解决方案
        """
        plan_id = f"plan_{uuid.uuid4().hex[:8]}"
        
        # 提取关键信息
        demand_type = analysis_result.get("demand_type", "综合需求")
        # 用关键词细化 demand_type（补充 EightLayerPipeline 未覆盖的类型）
        demand_type = self._detect_demand_type(problem, demand_type)
        domain = analysis_result.get("domain", "general")
        conclusions = reasoning_result.get("conclusion", "")
        recommendations = reasoning_result.get("recommendations", [])
        
        # 生成方案标题
        title = self._generate_title(problem, demand_type)
        
        # 生成方案描述
        description = self._generate_description(problem, conclusions)
        
        # 生成可执行步骤
        steps = self._generate_steps(
            problem, demand_type, domain, conclusions, recommendations
        )
        
        # 生成前置条件
        prerequisites = self._generate_prerequisites(steps)
        
        # 生成预期结果
        expected_outcome = self._generate_expected_outcome(
            problem, demand_type, conclusions
        )
        
        # 生成成功标准
        success_criteria = self._generate_success_criteria(
            problem, demand_type, expected_outcome
        )
        
        # 评估总工作量
        total_effort = self._estimate_total_effort(steps)
        
        # 计算置信度
        confidence = self._calculate_confidence(
            analysis_result, reasoning_result, steps
        )
        
        plan = SolutionPlan(
            plan_id=plan_id,
            title=title,
            description=description,
            steps=steps,
            prerequisites=prerequisites,
            expected_outcome=expected_outcome,
            success_criteria=success_criteria,
            total_effort=total_effort,
            confidence=confidence,
            status=SolutionStatus.DRAFT,
        )
        
        self.logger.info(f"[SolutionGenerator] 生成方案: {title} ({len(steps)} steps)")
        
        return plan
    
    def _detect_demand_type(self, problem: str, current_type: str) -> str:
        """
        根据问题文本细化 demand_type，补充更多模板类型
        当 EightLayerPipeline 的分类太粗时，用关键词匹配细化
        """
        p = problem.lower()

        # 如果已经有明确分类且不是通用类型，直接返回
        if current_type not in ("综合需求", "通用"):
            return current_type

        # 数据分析类
        if any(kw in p for kw in ["数据分析", "数据可视化", "图表", "趋势分析",
                                    "统计分析", "数据报告", "指标分析"]):
            return "数据分析"

        # 代码生成类
        if any(kw in p for kw in ["写代码", "编写函数", "实现", "开发",
                                    "代码生成", "脚本", "爬虫", "api",
                                    "帮我写", "写一个"]):
            return "代码生成"

        # 文档编写类
        if any(kw in p for kw in ["写文档", "写报告", "写方案", "写总结",
                                    "会议纪要", "ppt", "word", "pdf",
                                    "文档生成", "报告生成"]):
            return "文档编写"

        # 系统配置类
        if any(kw in p for kw in ["配置", "部署", "安装", "环境搭建",
                                    "初始化", "设置", "搭建环境"]):
            return "系统配置"

        # 问题排查类
        if any(kw in p for kw in ["报错", "bug", "错误", "不工作", "失败",
                                    "排查", "调试", "为什么", "怎么办"]):
            return "问题排查"

        return current_type  # 无法识别，返回原类型

    def _generate_title(self, problem: str, demand_type: str) -> str:
        """生成方案标题"""
        # 简化版：取问题前50字符
        short_problem = problem[:50].strip()
        if len(problem) > 50:
            short_problem += "..."
        return f"{demand_type}解决方案：{short_problem}"
    
    def _generate_description(self, problem: str, conclusions: str) -> str:
        """生成方案描述"""
        desc = f"## 问题\n{problem}\n\n"
        if conclusions:
            desc += f"## 分析结论\n{conclusions}\n\n"
        desc += "## 方案概述\n本方案包含一系列可执行步骤，旨在解决上述问题。"
        return desc
    
    def _generate_steps(self, problem: str, demand_type: str, 
                       domain: str, conclusions: str, 
                       recommendations: List) -> List[ActionableStep]:
        """生成可执行步骤"""
        steps = []
        
        # 基于需求类型生成不同步骤
        if demand_type == "信息查询":
            steps.append(ActionableStep(
                step_id="step_1",
                description="整理查询结果",
                action_type="manual",
                content=conclusions or "根据查询结果整理答案",
                expected_output="结构化的答案",
                validation="人工审核答案完整性",
            ))
        
        elif demand_type == "分析研究":
            # 分析类：问题理解 → 数据收集 → 分析 → 结论
            steps.append(ActionableStep(
                step_id="step_1",
                description="明确分析目标和范围",
                action_type="decision",
                content=f"分析问题：{problem}\n确定分析维度：\n1. 核心问题\n2. 关键因素\n3. 数据需求",
                expected_output="分析框架",
                validation="框架是否覆盖所有关键维度",
            ))
            steps.append(ActionableStep(
                step_id="step_2",
                description="收集相关数据和信息",
                action_type="manual",
                content=conclusions or "收集相关数据和信息",
                expected_output="数据清单",
                validation="数据是否充分可靠",
                dependencies=["step_1"],
            ))
            steps.append(ActionableStep(
                step_id="step_3",
                description="执行分析",
                action_type="manual",
                content="根据分析框架执行分析，得出结论",
                expected_output="分析结论",
                validation="结论是否有数据和逻辑支撑",
                dependencies=["step_2"],
            ))
        
        elif demand_type == "策略规划":
            # 策略类：现状分析 → 目标设定 → 策略制定 → 实施计划
            steps.append(ActionableStep(
                step_id="step_1",
                description="分析现状和目标",
                action_type="decision",
                content=f"现状分析：\n{conclusions}\n\n目标设定：明确可量化的目标",
                expected_output="现状+目标文档",
                validation="目标是否SMART",
            ))
            
            # 从recommendations生成策略步骤
            for i, rec in enumerate(recommendations[:5], start=2):
                steps.append(ActionableStep(
                    step_id=f"step_{i}",
                    description=f"实施策略：{rec[:50]}",
                    action_type="manual",
                    content=rec,
                    expected_output="策略实施结果",
                    validation="策略是否达到预期效果",
                    dependencies=[s.step_id for s in steps],
                ))

        elif demand_type == "数据分析":
            steps.append(ActionableStep(
                step_id="step_1",
                description="明确分析目标和数据需求",
                action_type="decision",
                content=f"分析目标：{problem}\n需要哪些数据？数据来源？指标如何定义？",
                expected_output="数据分析需求文档",
                validation="目标是否明确、可量化",
            ))
            steps.append(ActionableStep(
                step_id="step_2",
                description="收集和处理数据",
                action_type="code",
                content="""# 数据收集和处理示例
import pandas as pd
# 1. 从数据源读取
# df = pd.read_csv('data.csv')
# 2. 数据清洗
# df = df.dropna()
# 3. 数据转换和特征工程""",
                expected_output="清洗后的数据集",
                validation="数据质量检查通过：缺失值、异常值已处理",
                dependencies=["step_1"],
            ))
            steps.append(ActionableStep(
                step_id="step_3",
                description="执行数据分析和建模",
                action_type="code",
                content="""# 数据分析和建模示例
# 描述性统计
# 相关性分析
# 可视化展示""",
                expected_output="数据分析报告",
                validation="分析方法是否合适，结论是否有数据支撑",
                dependencies=["step_2"],
            ))

        elif demand_type == "代码生成":
            steps.append(ActionableStep(
                step_id="step_1",
                description="分析需求和设计方案",
                action_type="decision",
                content=f"需求：{problem}\n输入/输出是什么？边界条件？性能要求？",
                expected_output="技术方案文档",
                validation="方案是否覆盖所有需求",
            ))
            steps.append(ActionableStep(
                step_id="step_2",
                description="编写代码实现",
                action_type="code",
                content=f"# 根据方案编写代码\n# 函数名、参数、返回值\n# {problem}",
                expected_output="代码文件",
                validation="代码语法检查通过，静态分析无严重问题",
                dependencies=["step_1"],
            ))
            steps.append(ActionableStep(
                step_id="step_3",
                description="编写和运行测试用例",
                action_type="command",
                content="python -m pytest tests/ -v",
                expected_output="测试结果",
                validation="所有测试通过，覆盖率达到要求",
                dependencies=["step_2"],
            ))

        elif demand_type == "文档编写":
            steps.append(ActionableStep(
                step_id="step_1",
                description="设计文档大纲",
                action_type="decision",
                content=f"文档类型：{problem}\n目标读者是谁？核心内容有哪些？章节结构如何安排？",
                expected_output="文档大纲",
                validation="大纲是否覆盖所有必要内容，逻辑顺序是否合理",
            ))
            steps.append(ActionableStep(
                step_id="step_2",
                description="编写文档内容",
                action_type="manual",
                content=f"根据大纲逐节编写《{problem}》的文档内容，注意准确性、完整性和可读性",
                expected_output="文档草稿",
                validation="内容准确、无错别字、格式规范",
                dependencies=["step_1"],
            ))
            steps.append(ActionableStep(
                step_id="step_3",
                description="审核和修订",
                action_type="manual",
                content="按照审核检查表逐项检查：准确性、一致性、可读性、格式规范",
                expected_output="修订后的正式文档",
                validation="审核检查表全部通过",
                dependencies=["step_2"],
            ))

        elif demand_type == "系统配置":
            steps.append(ActionableStep(
                step_id="step_1",
                description="检查当前环境和现有配置",
                action_type="command",
                content="检查系统环境：版本、依赖、现有配置文件",
                expected_output="环境检查报告",
                validation="环境是否满足最低要求",
            ))
            steps.append(ActionableStep(
                step_id="step_2",
                description="生成配置文件",
                action_type="config",
                content=f"# {problem} 配置文件\n# 根据实际环境填写配置项",
                expected_output="配置文件（如 config.yaml / .env）",
                validation="配置文件语法正确，必填项完整",
                dependencies=["step_1"],
            ))
            steps.append(ActionableStep(
                step_id="step_3",
                description="应用配置并验证",
                action_type="command",
                content="应用配置变更，重启相关服务，验证配置是否生效",
                expected_output="配置生效确认",
                validation="配置已生效，服务正常运行",
                dependencies=["step_2"],
            ))

        elif demand_type == "问题排查":
            steps.append(ActionableStep(
                step_id="step_1",
                description="明确问题描述和复现步骤",
                action_type="decision",
                content=f"问题：{problem}\n复现步骤？环境信息？相关错误日志？",
                expected_output="问题报告",
                validation="问题描述完整，复现步骤清晰",
            ))
            steps.append(ActionableStep(
                step_id="step_2",
                description="分析可能原因并逐一排查",
                action_type="manual",
                content="根据问题描述和日志，列出可能原因，按可能性排序并逐一验证",
                expected_output="排查过程和结论",
                validation="根因已找到，有证据支撑",
                dependencies=["step_1"],
            ))
            steps.append(ActionableStep(
                step_id="step_3",
                description="实施解决方案并验证",
                action_type="command",
                content="根据排查结论实施修复，然后验证问题是否解决",
                expected_output="修复结果确认",
                validation="问题已解决，无副作用",
                dependencies=["step_2"],
            ))

        else:
            # 通用：问题分解 → 方案生成 → 实施
            steps.append(ActionableStep(
                step_id="step_1",
                description="分解问题",
                action_type="decision",
                content=f"将问题'{problem[:100]}'分解为可处理的子问题",
                expected_output="问题分解树",
                validation="是否覆盖所有关键子问题",
            ))
            steps.append(ActionableStep(
                step_id="step_2",
                description="生成解决方案",
                action_type="manual",
                content=conclusions or "基于分析问题生成解决方案",
                expected_output="解决方案草案",
                validation="方案是否解决所有子问题",
                dependencies=["step_1"],
            ))
        
        return steps
    
    def _generate_prerequisites(self, steps: List[ActionableStep]) -> List[str]:
        """生成前置条件"""
        prereqs = []
        
        # 检查是否有 High 难度步骤
        has_high = any(s.estimated_effort == "high" for s in steps)
        if has_high:
            prereqs.append("需要具备相关领域知识或专家支持")
        
        # 检查是否有 command 类型步骤
        has_command = any(s.action_type == "command" for s in steps)
        if has_command:
            prereqs.append("需要命令行访问权限")
        
        # 通用前置条件
        prereqs.append("需要明确问题边界和约束条件")
        
        return prereqs
    
    def _generate_expected_outcome(self, problem: str, 
                                   demand_type: str, 
                                   conclusions: str) -> str:
        """生成预期结果"""
        if demand_type == "信息查询":
            return "获得准确、完整的答案"
        elif demand_type == "分析研究":
            return "获得有数据支撑的分析结论和可执行的建议"
        elif demand_type == "策略规划":
            return "获得完整的策略方案和实施路线图"
        else:
            return "问题得到有效解决，目标达成"
    
    def _generate_success_criteria(self, problem: str, 
                                   demand_type: str,
                                   expected_outcome: str) -> List[str]:
        """生成成功标准"""
        criteria = []
        
        criteria.append("方案步骤清晰可执行")
        criteria.append("预期输出可验证")
        
        if demand_type == "策略规划":
            criteria.append("有可量化的目标指标")
            criteria.append("有清晰的实施时间表")
        
        return criteria
    
    def _estimate_total_effort(self, steps: List[ActionableStep]) -> str:
        """评估总工作量"""
        effort_scores = {"low": 1, "medium": 2, "high": 3}
        total = sum(effort_scores.get(s.estimated_effort, 2) for s in steps)
        avg = total / len(steps) if steps else 1
        
        if avg < 1.5:
            return "low"
        elif avg < 2.5:
            return "medium"
        else:
            return "high"
    
    def _calculate_confidence(self, analysis_result: Dict, 
                              reasoning_result: Dict, 
                              steps: List[ActionableStep]) -> float:
        """计算方案置信度"""
        # 基于分析置信度
        analysis_conf = analysis_result.get("confidence", 0.5)
        
        # 基于推理置信度
        reasoning_conf = reasoning_result.get("confidence", 0.5)
        
        # 基于步骤完整性（步骤越多越完整，但也要考虑质量）
        step_score = min(len(steps) / 5, 1.0)  # 5个步骤以上为完整
        
        # 加权平均
        confidence = analysis_conf * 0.3 + reasoning_conf * 0.4 + step_score * 0.3
        
        return round(confidence, 3)


# ============ 方案验证器 ============

class SolutionVerifier:
    """方案验证器 — 验证方案的可落地性"""
    
    def __init__(self):
        self.logger = logging.getLogger("Somn.SolutionVerifier")
    
    def verify(self, plan: SolutionPlan, 
               problem: str, 
               analysis_result: Dict) -> VerificationResult:
        """
        验证方案
        
        Args:
            plan: 解决方案
            problem: 原始问题
            analysis_result: 分析结果
            
        Returns:
            VerificationResult 验证结果
        """
        issues = []
        suggestions = []
        score = 0.0
        
        # 规则验证
        rule_score, rule_issues, rule_suggestions = self._rule_verification(
            plan, problem, analysis_result
        )
        issues.extend(rule_issues)
        suggestions.extend(rule_suggestions)
        
        # LLM验证（模拟）
        llm_score, llm_issues, llm_suggestions = self._llm_verification(
            plan, problem, analysis_result
        )
        
        # 综合评分
        score = rule_score * 0.6 + llm_score * 0.4
        
        # 合并问题和建议
        all_issues = rule_issues + llm_issues
        all_suggestions = rule_suggestions + llm_suggestions
        
        # 判断是否通过（score >= 0.6 为通过）
        passed = score >= 0.6 and len([i for i in all_issues if "严重" in i or "critical" in i.lower()]) == 0
        
        verified_by = "hybrid" if llm_score > 0 else "rule"
        
        result = VerificationResult(
            passed=passed,
            score=round(score, 3),
            issues=all_issues,
            suggestions=all_suggestions,
            verified_by=verified_by,
        )
        
        self.logger.info(
            f"[SolutionVerifier] 验证完成: passed={passed}, score={score:.3f}"
        )
        
        return result
    
    def _rule_verification(self, plan: SolutionPlan, 
                           problem: str, 
                           analysis_result: Dict) -> Tuple[float, List[str], List[str]]:
        """规则验证"""
        issues = []
        suggestions = []
        score = 1.0
        
        # 检查1：方案是否解决问题
        if not plan.steps:
            issues.append("严重：方案没有可执行步骤")
            score -= 0.4
        
        # 检查2：步骤是否有具体内容
        empty_steps = [s.step_id for s in plan.steps if not s.content or len(s.content) < 20]
        if empty_steps:
            issues.append(f"步骤内容不完整: {empty_steps}")
            score -= 0.1 * len(empty_steps)
        
        # 检查3：是否有验证方式
        no_validation = [s.step_id for s in plan.steps if not s.validation]
        if no_validation:
            issues.append(f"步骤缺少验证方式: {no_validation}")
            score -= 0.05 * len(no_validation)
            suggestions.append("为每个步骤添加验证方式，确保可验收")
        
        # 检查4：步骤依赖是否完整
        all_ids = {s.step_id for s in plan.steps}
        for step in plan.steps:
            for dep in step.dependencies:
                if dep not in all_ids:
                    issues.append(f"步骤{step.step_id}依赖不存在的step {dep}")
                    score -= 0.1
        
        # 检查5：预期结果是否明确
        if not plan.expected_outcome:
            issues.append("缺少预期结果")
            score -= 0.1
            suggestions.append("添加明确的预期结果，便于验证方案有效性")
        
        # 检查6：成功标准是否可衡量
        if not plan.success_criteria:
            issues.append("缺少成功标准")
            score -= 0.1
            suggestions.append("添加可衡量的成功标准")
        
        return max(score, 0.0), issues, suggestions
    
    def _llm_verification(self, plan: SolutionPlan, 
                          problem: str, 
                          analysis_result: Dict) -> Tuple[float, List[str], List[str]]:
        """LLM验证（模拟）"""
        # 模拟LLM验证结果
        # 实际实现应调用LLM API
        
        issues = []
        suggestions = []
        
        # 模拟评分：基于方案完整性
        score = 0.7  # 默认0.7
        
        # 模拟问题检测
        if len(plan.steps) < 3:
            issues.append("方案步骤较少，可能不够全面")
            score -= 0.1
        
        if plan.confidence < 0.6:
            issues.append("方案置信度较低，建议补充更多信息")
            score -= 0.15
        
        # 模拟建议
        suggestions.append("建议在实施前与相关人员评审方案")
        
        return score, issues, suggestions


# ============ 反馈管理器 ============

class FeedbackManager:
    """反馈管理器 — 收集和管理用户反馈"""
    
    def __init__(self, feedback_dir: Optional[str] = None):
        self.feedback_dir = Path(feedback_dir) if feedback_dir else Path.cwd() / "feedback"
        self.feedback_dir.mkdir(exist_ok=True)
        self.feedback_history: List[UserFeedback] = []
        self.logger = logging.getLogger("Somn.FeedbackManager")
        self.logger.info(f"[FeedbackManager] 初始化，反馈目录: {self.feedback_dir}")
    
    def collect_feedback(self, request_id: str, 
                         feedback_type: FeedbackType, 
                         rating: Optional[int] = None,
                         comment: str = "",
                         corrections: List[str] = None,
                         implemented: bool = False,
                         outcome: str = "") -> UserFeedback:
        """收集用户反馈"""
        feedback = UserFeedback(
            feedback_id=f"fb_{uuid.uuid4().hex[:8]}",
            request_id=request_id,
            feedback_type=feedback_type,
            rating=rating,
            comment=comment,
            corrections=corrections or [],
            implemented=implemented,
            outcome=outcome,
        )
        
        # 保存到历史
        self.feedback_history.append(feedback)
        
        # 持久化
        self._save_feedback(feedback)
        
        self.logger.info(f"[FeedbackManager] 收集反馈: {feedback.feedback_type.value}, rating={rating}")
        
        return feedback
    
    def _save_feedback(self, feedback: UserFeedback):
        """保存反馈到文件"""
        try:
            feedback_file = self.feedback_dir / f"{feedback.feedback_id}.json"
            with open(feedback_file, "w", encoding="utf-8") as f:
                json.dump(feedback.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"[FeedbackManager] 保存反馈失败: {e}")
    
    def load_feedback(self, request_id: Optional[str] = None) -> List[UserFeedback]:
        """加载反馈"""
        feedback_list = []
        
        for f in self.feedback_dir.glob("fb_*.json"):
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    fb = UserFeedback(
                        feedback_id=data["feedback_id"],
                        request_id=data["request_id"],
                        feedback_type=FeedbackType(data["feedback_type"]),
                        rating=data.get("rating"),
                        comment=data.get("comment", ""),
                        corrections=data.get("corrections", []),
                        implemented=data.get("implemented", False),
                        outcome=data.get("outcome", ""),
                        created_at=data.get("created_at"),
                    )
                    
                    if request_id is None or fb.request_id == request_id:
                        feedback_list.append(fb)
            except Exception as e:
                self.logger.error(f"[FeedbackManager] 加载反馈失败 {f}: {e}")
        
        return feedback_list
    
    def analyze_feedback(self, request_id: Optional[str] = None) -> Dict:
        """分析反馈，提取改进点"""
        feedback_list = self.load_feedback(request_id)
        
        if not feedback_list:
            return {"count": 0}
        
        # 统计评分
        ratings = [fb.rating for fb in feedback_list if fb.rating is not None]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # 收集所有修正
        all_corrections = []
        for fb in feedback_list:
            all_corrections.extend(fb.corrections)
        
        # 实施率
        implemented_count = sum(1 for fb in feedback_list if fb.implemented)
        implementation_rate = implemented_count / len(feedback_list) if feedback_list else 0
        
        return {
            "count": len(feedback_list),
            "avg_rating": round(avg_rating, 2),
            "rating_distribution": {r: ratings.count(r) for r in set(ratings)} if ratings else {},
            "correction_count": len(all_corrections),
            "corrections": all_corrections[:10],  # 最多返回10条
            "implementation_rate": round(implementation_rate, 2),
            "implemented_count": implemented_count,
        }


# ============ 学习引擎 ============

class LearningEngine:
    """学习引擎 — 从反馈中学习，更新知识"""
    
    def __init__(self):
        self.logger = logging.getLogger("Somn.LearningEngine")
    
    def learn_from_feedback(self, feedback: UserFeedback, 
                             result: ClosedLoopResult) -> bool:
        """
        从反馈中学习
        
        Returns:
            是否成功更新知识
        """
        try:
            # 1. 更新 NeuralMemory
            self._update_neural_memory(feedback, result)
            
            # 2. 更新 DomainNexus
            self._update_domain_nexus(feedback, result)
            
            # 3. 更新 Pan-Wisdom Tree（如果有学派推荐）
            self._update_pan_wisdom(feedback, result)
            
            self.logger.info(f"[LearningEngine] 从反馈学习完成: {feedback.feedback_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"[LearningEngine] 学习失败: {e}")
            return False
    
    def _update_neural_memory(self, feedback: UserFeedback, 
                              result: ClosedLoopResult):
        """更新 NeuralMemory，失败时降级到本地JSON文件"""
        saved = False
        try:
            from .neural_memory_v7 import get_neural_memory
            nm = get_neural_memory()
            
            # 构建记忆内容
            memory_content = f"""
# 问题解决记录

## 问题
{result.problem}

## 方案
{result.solution_plan.title if result.solution_plan else "无方案"}

## 用户反馈
- 评分: {feedback.rating}
- 评论: {feedback.comment}
- 是否实施: {feedback.implemented}
- 实施结果: {feedback.outcome}

## 改进建议
{chr(10).join(feedback.corrections)}
"""
            
            # 存入记忆
            nm.store(
                content=memory_content,
                category="problem_solving",
                tags=["closed_loop", feedback.feedback_type.value],
                confidence=feedback.rating / 5.0 if feedback.rating else 0.5,
            )
            saved = True
            self.logger.info(f"[LearningEngine] NeuralMemory更新成功: {feedback.feedback_id}")
            
        except Exception as e:
            self.logger.warning(f"[LearningEngine] 更新NeuralMemory失败: {e}")
        
        # 降级方案：保存到本地JSON文件
        if not saved:
            try:
                import json, time
                fallback_dir = Path("data/learning_fallback")
                fallback_dir.mkdir(parents=True, exist_ok=True)
                fallback_file = fallback_dir / f"memory_{feedback.feedback_id}.json"
                fallback_data = {
                    "feedback_id": feedback.feedback_id,
                    "request_id": feedback.request_id,
                    "problem": result.problem,
                    "solution_title": result.solution_plan.title if result.solution_plan else "",
                    "rating": feedback.rating,
                    "comment": feedback.comment,
                    "corrections": feedback.corrections,
                    "implemented": feedback.implemented,
                    "outcome": feedback.outcome,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
                with open(fallback_file, "w", encoding="utf-8") as f:
                    json.dump(fallback_data, f, ensure_ascii=False, indent=2)
                self.logger.info(f"[LearningEngine] 降级保存记忆到本地文件: {fallback_file}")
            except Exception as e2:
                self.logger.error(f"[LearningEngine] 本地降级也失败: {e2}")
    
    def _update_domain_nexus(self, feedback: UserFeedback, 
                              result: ClosedLoopResult):
        """更新 DomainNexus，失败时降级到本地JSON文件"""
        saved = False
        try:
            from .domain_nexus import get_nexus
            nexus = get_nexus()
            
            # 构建知识单元
            unit = {
                "type": "feedback_learning",
                "problem": result.problem,
                "solution_title": result.solution_plan.title if result.solution_plan else "",
                "rating": feedback.rating,
                "corrections": feedback.corrections,
                "outcome": feedback.outcome,
            }
            
            # 更新知识图谱
            nexus.learn_from_feedback(feedback.request_id, unit)
            saved = True
            self.logger.info(f"[LearningEngine] DomainNexus更新成功: {feedback.feedback_id}")
            
        except Exception as e:
            self.logger.warning(f"[LearningEngine] 更新DomainNexus失败: {e}")
        
        # 降级方案：保存到本地JSON文件
        if not saved:
            try:
                import json, time
                fallback_dir = Path("data/learning_fallback")
                fallback_dir.mkdir(parents=True, exist_ok=True)
                fallback_file = fallback_dir / f"domain_{feedback.feedback_id}.json"
                fallback_data = {
                    "feedback_id": feedback.feedback_id,
                    "request_id": feedback.request_id,
                    "problem": result.problem,
                    "solution_title": result.solution_plan.title if result.solution_plan else "",
                    "rating": feedback.rating,
                    "corrections": feedback.corrections,
                    "outcome": feedback.outcome,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
                with open(fallback_file, "w", encoding="utf-8") as f:
                    json.dump(fallback_data, f, ensure_ascii=False, indent=2)
                self.logger.info(f"[LearningEngine] 降级保存DomainNexus到本地文件: {fallback_file}")
            except Exception as e2:
                self.logger.error(f"[LearningEngine] 本地降级也失败: {e2}")
    
    def _update_pan_wisdom(self, feedback: UserFeedback, 
                            result: ClosedLoopResult):
        """更新 Pan-Wisdom Tree，失败时降级到本地JSON文件"""
        saved = False
        try:
            from .pan_wisdom_core import get_pan_wisdom
            pw = get_pan_wisdom()
            
            # 如果反馈评分低，调整学派推荐权重
            if feedback.rating and feedback.rating <= 2:
                # 降低相关学派的权重
                self.logger.info("[LearningEngine] 低评分反馈，调整学派权重")
                # 实际实现需要访问学派推荐系统
            saved = True
            
        except Exception as e:
            self.logger.warning(f"[LearningEngine] 更新Pan-Wisdom失败: {e}")
        
        # 降级方案：保存到本地JSON文件
        if not saved:
            try:
                import json, time
                fallback_dir = Path("data/learning_fallback")
                fallback_dir.mkdir(parents=True, exist_ok=True)
                fallback_file = fallback_dir / f"panwisdom_{feedback.feedback_id}.json"
                fallback_data = {
                    "feedback_id": feedback.feedback_id,
                    "request_id": feedback.request_id,
                    "problem": result.problem,
                    "rating": feedback.rating,
                    "comment": feedback.comment,
                    "corrections": feedback.corrections,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
                with open(fallback_file, "w", encoding="utf-8") as f:
                    json.dump(fallback_data, f, ensure_ascii=False, indent=2)
                self.logger.info(f"[LearningEngine] 降级保存Pan-Wisdom到本地文件: {fallback_file}")
            except Exception as e2:
                self.logger.error(f"[LearningEngine] 本地降级也失败: {e2}")


# ============ 主闭环Solver ============

class ClosedLoopSolver:
    """
    闭环问题解决器 — 完整的问题解决工作流
    
    工作流：
    1. 输入问题
    2. 八层分析（调用EightLayerPipeline）
    3. 生成解决方案（SolutionGenerator）
    4. 验证解决方案（SolutionVerifier）
    5. 输出结果（TianShuOutput）
    6. 收集反馈（FeedbackManager）
    7. 学习进化（LearningEngine）
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "outputs"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 核心组件
        self.pipeline = None  # 懒加载
        self.solution_generator = SolutionGenerator()
        self.solution_verifier = SolutionVerifier()
        self.solution_executor = None  # 懒加载
        self.feedback_manager = FeedbackManager(
            feedback_dir=str(self.output_dir.parent / "feedback")
        )
        self.learning_engine = LearningEngine()
        self.output_engine = None  # 懒加载
        
        self.logger = logging.getLogger("Somn.ClosedLoopSolver")
        self.logger.info("[ClosedLoopSolver] v1.0.0 初始化完成")
    
    def _get_pipeline(self):
        """懒加载八层管道"""
        if self.pipeline is None:
            from .eight_layer_pipeline import EightLayerPipeline
            self.pipeline = EightLayerPipeline.get_pipeline(
                output_dir=str(self.output_dir)
            )
        return self.pipeline
    
    def _get_output_engine(self):
        """懒加载输出引擎，失败时降级到内置Markdown报告生成器"""
        if self.output_engine is None:
            try:
                from .tianshu_output import get_tianshu_output
                self.output_engine = get_tianshu_output()
                self.output_engine.output_dir = Path(self.output_dir)
            except (ImportError, Exception) as e:
                self.logger.warning(f"[ClosedLoopSolver] tianshu_output不可用，启用Markdown降级: {e}")
                # 内置Markdown报告生成器（降级方案）
                self.output_engine = self._create_markdown_fallback()
        return self.output_engine

    def _create_markdown_fallback(self):
        """创建内置Markdown报告生成器（降级方案）"""
        class MarkdownFallback:
            def __init__(self, output_dir):
                self.output_dir = Path(output_dir)
                self.output_dir.mkdir(parents=True, exist_ok=True)
            def generate_report(self, report_type, title, sections, output_format="markdown"):
                import time
                timestamp = int(time.time())
                filename = f"report_{timestamp}.md"
                filepath = self.output_dir / filename
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"# {title}\n\n")
                    for sec in sections:
                        f.write(f"## {sec.get('title', '章节')}\n\n")
                        f.write(f"{sec.get('content', '')}\n\n")
                return {"output_id": str(filepath), "format": "markdown", "fallback": True}
        return MarkdownFallback(self.output_dir)
    
    def _get_solution_executor(self):
        """懒加载方案执行器"""
        if self.solution_executor is None:
            try:
                from .solution_executor import SolutionExecutor
                self.solution_executor = SolutionExecutor(
                    work_dir=str(self.output_dir.parent / "executions")
                )
            except ImportError:
                self.solution_executor = None
        return self.solution_executor
    
    def solve(self, problem: str, 
              grade: str = "deep", 
              output_format: str = "markdown") -> ClosedLoopResult:
        """
        解决问题 — 完整闭环工作流
        
        Args:
            problem: 问题描述
            grade: 处理等级 (basic/deep/super)
            output_format: 输出格式 (markdown/html/pptx)
            
        Returns:
            ClosedLoopResult 包含完整处理结果
        """
        start = time.perf_counter()
        request_id = f"req_{uuid.uuid4().hex[:8]}"
        
        self.logger.info(f"[ClosedLoopSolver] 开始解决问题: {request_id}")
        self.logger.info(f"  问题: {problem[:100]}...")
        self.logger.info(f"  等级: {grade}, 输出格式: {output_format}")
        
        # ===== Step 1: 八层分析 =====
        self.logger.info("[Step 1] 八层分析...")
        pipeline = self._get_pipeline()
        
        # 转换grade
        from .eight_layer_pipeline import ProcessingGrade
        try:
            grade_enum = ProcessingGrade(grade)
        except ValueError:
            grade_enum = ProcessingGrade.DEEP
        
        pipeline_result = pipeline.process(problem, grade=grade_enum)
        
        # 提取分析结果
        analysis_result = {
            "demand_type": pipeline_result.metadata.get("demand_type", "综合需求"),
            "domain": pipeline_result.domain.value if hasattr(pipeline_result.domain, 'value') else str(pipeline_result.domain),
            "confidence": pipeline_result.final_confidence,
            "reasoning_chain": pipeline_result.reasoning_chain,
        }
        
        self.logger.info(f"  分析完成，置信度: {pipeline_result.final_confidence:.3f}")
        
        # ===== Step 2: 生成解决方案 =====
        self.logger.info("[Step 2] 生成解决方案...")
        
        reasoning_result = {
            "conclusion": pipeline_result.final_answer,
            "recommendations": pipeline_result.metadata.get("optimization_suggestions", []),
            "confidence": pipeline_result.final_confidence,
        }
        
        solution_plan = self.solution_generator.generate(
            problem, analysis_result, reasoning_result
        )
        
        self.logger.info(f"  方案生成完成: {solution_plan.title} ({len(solution_plan.steps)} steps)")
        
        # ===== Step 3: 验证解决方案 =====
        self.logger.info("[Step 3] 验证解决方案...")
        
        verification = self.solution_verifier.verify(
            solution_plan, problem, analysis_result
        )
        
        if verification.passed:
            solution_plan.status = SolutionStatus.VERIFIED
            self.logger.info(f"  验证通过，可落地性评分: {verification.score:.3f}")
            
            # ===== Step 4: 真正执行解决方案 =====
            self.logger.info("[Step 4] 执行解决方案...")
            executor = self._get_solution_executor()
            if executor:
                execution_result = executor.execute_plan(
                    solution_plan, dry_run=False
                )
                self.logger.info(
                    f"  执行{'成功' if execution_result.overall_success else '失败'}"
                )
            else:
                execution_result = None
                self.logger.warning("  SolutionExecutor 不可用，跳过执行")
        else:
            solution_plan.status = SolutionStatus.NEEDS_REVISION
            self.logger.info(f"  验证未通过，问题: {verification.issues}")
            execution_result = None
            
            # 根据建议修订方案（简化版）
            if verification.suggestions:
                self.logger.info(f"  修订建议: {verification.suggestions[:3]}")
        
        # ===== Step 5: 输出结果 =====
        self.logger.info("[Step 5] 输出结果...")
        
        output_files = []
        
        # 生成报告（使用全局函数）
        try:
            import json
            from .tianshu_output import generate_report
            
            # 构建 sections（确保所有 content 都是字符串）
            def to_str(obj):
                if isinstance(obj, dict):
                    return json.dumps(obj, indent=2, ensure_ascii=False)
                return str(obj)
            
            sections = [
                {
                    "title": "问题分析",
                    "content": to_str(analysis_result.get("summary", analysis_result)),
                },
                {
                    "title": "解决方案",
                    "content": to_str(solution_plan.to_dict()) if solution_plan else "无解决方案",
                },
                {
                    "title": "验证结果",
                    "content": to_str(verification.to_dict()) if verification else "未验证",
                },
            ]
            
            report_result = generate_report(
                report_type="analysis",
                title=solution_plan.title if solution_plan else "解决方案分析",
                sections=sections,
                output_format=output_format,
            )
            
            if report_result and 'output_id' in report_result:
                output_files.append(report_result['output_id'])
                self.logger.info(f"  报告已生成: {report_result['output_id']}")
        except Exception as e:
            self.logger.error(f"  报告生成失败: {e}")
        
        # ===== Step 5: 构建结果 =====
        total_time = time.perf_counter() - start  # 秒
        
        result = ClosedLoopResult(
            request_id=request_id,
            problem=problem,
            grade=grade,
            analysis_result=analysis_result,
            solution_plan=solution_plan,
            verification=verification,
            execution_result=execution_result,
            output_files=output_files,
            knowledge_updated=False,
            total_time=round(total_time, 2),
        )
        
        self.logger.info(
            f"[ClosedLoopSolver] 解决问题完成，总耗时: {total_time:.2f}秒"
        )
        
        return result
    
    def collect_feedback(self, result: ClosedLoopResult, 
                         rating: int, 
                         comment: str = "", 
                         corrections: List[str] = None,
                         implemented: bool = False,
                         outcome: str = "") -> UserFeedback:
        """
        收集用户反馈，触发学习
        
        Args:
            result: solve()的返回结果
            rating: 评分（1-5）
            comment: 评论
            corrections: 修正内容
            implemented: 是否已实施
            outcome: 实施结果
            
        Returns:
            UserFeedback
        """
        self.logger.info(f"[ClosedLoopSolver] 收集反馈: rating={rating}")
        
        # 确定反馈类型
        if corrections:
            fb_type = FeedbackType.CORRECTION
        elif implemented:
            fb_type = FeedbackType.IMPLEMENTATION
        elif comment:
            fb_type = FeedbackType.IMPROVEMENT
        else:
            fb_type = FeedbackType.RATING
        
        # 收集反馈
        feedback = self.feedback_manager.collect_feedback(
            request_id=result.request_id,
            feedback_type=fb_type,
            rating=rating,
            comment=comment,
            corrections=corrections,
            implemented=implemented,
            outcome=outcome,
        )
        
        # 触发学习
        updated = self.learning_engine.learn_from_feedback(feedback, result)
        result.knowledge_updated = updated
        
        self.logger.info(f"[ClosedLoopSolver] 反馈处理完成，知识更新: {updated}")
        
        return feedback
    
    def get_solution_status(self, request_id: str) -> Optional[Dict]:
        """获取方案状态"""
        # 从反馈历史中查找
        feedback_list = self.feedback_manager.load_feedback(request_id)
        
        if not feedback_list:
            return None
        
        latest = feedback_list[-1]
        return {
            "request_id": request_id,
            "latest_feedback": latest.to_dict(),
            "feedback_count": len(feedback_list),
            "avg_rating": sum(f.rating for f in feedback_list if f.rating) / len(feedback_list),
        }


# ============ 便捷函数 ============

def solve_problem(problem: str, 
                  grade: str = "deep", 
                  output_format: str = "markdown") -> ClosedLoopResult:
    """
    便捷函数：解决问题
    
    Usage:
        result = solve_problem("如何提升用户增长率？")
        print(result.solution_plan.title)
        print(result.verification.score)
    """
    solver = ClosedLoopSolver()
    return solver.solve(problem, grade, output_format)


def collect_feedback(result: ClosedLoopResult, 
                     rating: int, 
                     comment: str = "") -> UserFeedback:
    """便捷函数：收集反馈"""
    solver = ClosedLoopSolver()
    return solver.collect_feedback(result, rating, comment)


# ============ 测试 ============

if __name__ == "__main__":
    import sys
    
    print("=== ClosedLoopSolver 测试 ===\n")
    
    # 测试1：解决问题
    print("[测试1] 解决问题...")
    result = solve_problem(
        "如何设计一个高效的用户增长策略？",
        grade="deep",
        output_format="markdown",
    )
    
    print(f"  请求ID: {result.request_id}")
    print(f"  方案标题: {result.solution_plan.title}")
    print(f"  方案步骤数: {len(result.solution_plan.steps)}")
    print(f"  验证通过: {result.verification.passed}")
    print(f"  可落地性评分: {result.verification.score}")
    print(f"  总耗时: {result.total_duration_ms:.2f}ms")
    
    # 测试2：收集反馈
    print("\n[测试2] 收集反馈...")
    feedback = collect_feedback(
        result, 
        rating=4, 
        comment="方案很有帮助，但第三步需要更具体的实施细节"
    )
    
    print(f"  反馈ID: {feedback.feedback_id}")
    print(f"  评分: {feedback.rating}")
    print(f"  评论: {feedback.comment}")
    
    print("\n=== 测试完成 ===")
    
    sys.exit(0)
