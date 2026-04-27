"""
Cloning基类 v1.0
贤者Cloning的抽象基类

每个Cloning是一个轻量级智慧引擎，具备:
- analyze() - 用该人物的思想分析问题
- decide() - 用该人物的决策框架做选择
- advise() - 在特定情境下给出建议
- assess() - 用其价值标准进行评估

基于600贤者Distillation研究成果
"""

from abc import ABC, abstractmethod
from datetime import datetime

__all__ = [
    "SageCloning", "Tier1CoreCloning", "Tier2ClusterCloning",
    "Tier4MicroCloning", "SchoolCluster",
]
from typing import List, Dict, Optional, Any

from ._cloning_types import (
    CloningTier,
    CloningIdentity,
    CloningProfile,
    CapabilityVector,
    WisdomLaw,
    AnalysisResult,
    DecisionResult,
    DecisionOption,
    AdviceResult,
    AdviceContext,
    AssessmentResult,
    AssessmentCriteria,
)


class SageCloning(ABC):
    """
    贤者Cloning基类
    
    所有Cloning都应继承此类并实现核心接口。
    支持两种初始化方式：
    1. 完整版：设置 self.identity = CloningIdentity(...)
    2. 简化版：传入 SageProfile(...) 到 __init__
    """
    
    # ── 身份信息 (子类必须定义) ──────────────────────────────
    identity: Optional['CloningIdentity'] = None
    tier: Optional['CloningTier'] = None
    capability_vector: Optional['CapabilityVector'] = None
    wisdom_laws: Optional[List['WisdomLaw']] = None
    
    # ── 简化版属性（兼容SageProfile初始化） ─────────────────
    _sage_name: str = ""
    _sage_school: str = ""
    _sage_department: str = ""
    _sage_position: str = ""

    def __init__(self, profile=None):
        """
        初始化Cloning
        
        Args:
            profile: SageProfile实例（可选，简化版API使用）
        """
        if profile is not None:
            self._sage_name = getattr(profile, 'name', '') or ''
            self._sage_school = getattr(profile, 'school', '') or ''
            self._sage_department = getattr(profile, 'department', '') or ''
            self._sage_position = getattr(profile, 'position', '') or ''
            self._sage_tier = getattr(profile, 'tier', None)

    @property
    def name(self) -> str:
        """便捷属性：返回名称"""
        if hasattr(self, 'identity') and self.identity:
            return self.identity.name
        return self._sage_name

    @property
    def school(self) -> str:
        """便捷属性：返回学派"""
        if hasattr(self, 'identity') and self.identity:
            return self.identity.school
        return self._sage_school

    @property
    def department(self) -> str:
        """便捷属性：返回部门"""
        if hasattr(self, 'identity') and self.identity:
            return self.identity.department
        return self._sage_department

    @property
    def position(self) -> str:
        """便捷属性：返回岗位"""
        if hasattr(self, 'identity') and self.identity:
            return self.identity.position
        return self._sage_position
    
    # ── 核心接口 (子类必须实现) ─────────────────────────────
    
    @abstractmethod
    def analyze(
        self, 
        problem: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> AnalysisResult:
        """
        用该人物的思想分析问题
        
        Args:
            problem: 要分析的问题描述
            context: 额外的上下文信息
            
        Returns:
            AnalysisResult: 分析结果
        """
        pass
    
    @abstractmethod
    def decide(
        self, 
        options: List[DecisionOption]
    ) -> DecisionResult:
        """
        用该人物的决策框架做选择
        
        Args:
            options: 决策选项列表
            
        Returns:
            DecisionResult: 决策结果
        """
        pass
    
    @abstractmethod
    def advise(
        self, 
        context: AdviceContext
    ) -> AdviceResult:
        """
        在特定情境下给出建议
        
        Args:
            context: 建议上下文
            
        Returns:
            AdviceResult: 建议结果
        """
        pass
    
    def assess(
        self, 
        subject: str,
        criteria: Optional[AssessmentCriteria] = None
    ) -> AssessmentResult:
        """
        用其价值标准进行评估（默认实现，子类可覆盖）
        """
        return AssessmentResult(
            cloning_name=self.name,
            timestamp=datetime.now(),
            subject=subject,
            overall_score=75.0,
            dimension_scores={},
            strengths=[],
            weaknesses=[],
            recommendations=[],
            value_framework=f"{self.school}评价体系",
        )
    
    # ── 辅助方法 (子类可覆盖) ──────────────────────────────
    
    def get_identity(self) -> CloningIdentity:
        """获取Cloning身份信息"""
        return self.identity
    
    def get_capability_vector(self) -> CapabilityVector:
        """获取能力向量"""
        return self.capability_vector
    
    def get_wisdom_laws(self) -> List[WisdomLaw]:
        """获取智慧法则列表"""
        return self.wisdom_laws
    
    def get_tier(self) -> CloningTier:
        """获取Cloning层级"""
        return self.tier
    
    def get_profile(self) -> CloningProfile:
        """获取完整Cloning画像"""
        return CloningProfile(
            identity=self.identity,
            tier=self.tier,
            capability_vector=self.capability_vector,
            wisdom_laws=self.wisdom_laws,
        )
    
    def cosine_similarity(self, other: 'SageCloning') -> float:
        """计算与另一个Cloning的能力相似度"""
        return self.capability_vector.cosine_similarity(other.capability_vector)
    
    # ── 通用推理辅助方法 ───────────────────────────────────
    
    def _build_reasoning_chain(
        self, 
        steps: List[str]
    ) -> List[str]:
        """构建推理链"""
        chain = []
        for i, step in enumerate(steps, 1):
            chain.append(f"[推理{i}] {step}")
        return chain
    
    def _apply_wisdom_framework(
        self, 
        problem: str,
        framework_name: str
    ) -> str:
        """应用智慧框架分析问题"""
        return f"基于【{framework_name}】分析: {problem}"
    
    def _evaluate_ethics(
        self, 
        action: str
    ) -> tuple[bool, str]:
        """评估行动的伦理正当性"""
        return True, "符合基本伦理规范"
    
    def _check_precedent(
        self, 
        historical_cases: List[Dict[str, str]],
        current_situation: str
    ) -> Optional[str]:
        """检查历史先例"""
        if historical_cases:
            return historical_cases[0].get('insight')
        return None


class Tier1CoreCloning(SageCloning):
    """
    Tier 1: 核心独立Cloning
    内阁级/六部尚书级核心人物
    """
    pass


class Tier2ClusterCloning(SageCloning):
    """
    Tier 2: 学派集群Cloning
    按学派/领域分组的Cloning集合
    """
    
    def __init__(self):
        self._members: Dict[str, SageCloning] = {}
        self._leader: Optional[str] = None
    
    def add_member(self, cloning: SageCloning, is_leader: bool = False) -> None:
        """添加集群成员"""
        name = cloning.identity.name
        self._members[name] = cloning
        if is_leader:
            self._leader = name
    
    def get_member(self, name: str) -> Optional[SageCloning]:
        """获取指定成员"""
        return self._members.get(name)
    
    def get_leader(self) -> Optional[SageCloning]:
        """获取领军人物"""
        if self._leader:
            return self._members.get(self._leader)
        return None
    
    def get_all_members(self) -> Dict[str, SageCloning]:
        """获取所有成员"""
        return self._members.copy()
    
    def get_member_count(self) -> int:
        """获取成员数量"""
        return len(self._members)


class Tier4MicroCloning(SageCloning):
    """
    Tier 4: 里甲制微Cloning
    基层执行角色的微Cloning
    """
    
    def __init__(self):
        self._target_function: Optional[str] = None
        self._specific_capability: str = ""
    
    def set_function_mapping(self, function_name: str) -> None:
        """设置函数映射"""
        self._target_function = function_name
    
    def set_specific_capability(self, capability: str) -> None:
        """设置特定能力"""
        self._specific_capability = capability
    
    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            cloning_name=self.identity.name,
            timestamp=datetime.now(),
            problem=problem,
            perspective=self._specific_capability,
            analysis_content=f"基于{self.identity.name}的{self._specific_capability}视角分析",
        )
    
    def decide(self, options: List[DecisionOption]) -> DecisionResult:
        return DecisionResult(
            cloning_name=self.identity.name,
            timestamp=datetime.now(),
            decision="微Cloning不支持复杂决策",
            chosen_option="",
            reasoning="功能限制"
        )
    
    def advise(self, context: AdviceContext) -> AdviceResult:
        return AdviceResult(
            cloning_name=self.identity.name,
            timestamp=datetime.now(),
            advice=f"基于{self.identity.name}的{self._specific_capability}提供建议",
            reasoning="微Cloning特定能力"
        )
    
    def assess(self, subject: str, criteria: Optional[AssessmentCriteria] = None) -> AssessmentResult:
        return AssessmentResult(
            cloning_name=self.identity.name,
            timestamp=datetime.now(),
            subject=subject,
            overall_score=75.0,
            dimension_scores={self._specific_capability: 85.0},
            value_framework=f"{self.identity.name}评价体系"
        )


class SchoolCluster:
    """
    学派集群 - Tier 2
    
    包含同一学派/领域多个贤者Cloning，
    支持leader/consensus/debate/synthesis四种咨询方法。
    """

    def __init__(
        self,
        name: str,
        school: str,
        department: str = "",
        leader_name: str = "",
        members: Optional[Dict[str, 'SageCloning']] = None,
    ):
        self.name = name
        self.school = school
        self.department = department
        self.leader_name = leader_name
        self._members: Dict[str, SageCloning] = members or {}

    @property
    def members(self) -> Dict[str, 'SageCloning']:
        """集群成员字典"""
        return self._members
        self._leader: Optional[SageCloning] = self._members.get(leader_name) if leader_name else None

    @property
    def leader(self) -> Optional['SageCloning']:
        return self._leader

    @property
    def member_count(self) -> int:
        return len(self._members)

    @property
    def member_names(self) -> List[str]:
        return list(self._members.keys())

    def get_member(self, name: str) -> Optional['SageCloning']:
        return self._members.get(name)

    def consult(
        self,
        problem: str,
        method: str = "leader",
        context: Optional[Dict[str, Any]] = None,
    ) -> 'ClusterResult':
        """
        咨询学派集群

        Args:
            problem: 要咨询的问题
            method: leader/consensus/debate/synthesis
            context: 额外上下文

        Returns:
            ClusterResult
        """
        from ._cloning_types import ClusterResult

        analyses = []
        participants = []

        if method == "leader" and self._leader:
            try:
                r = self._leader.analyze(problem, context)
                analyses.append(r)
                participants.append(self._leader.identity.name if hasattr(self._leader, 'identity') else self.leader_name)
            except Exception:
                pass  # participants.append(self._leader.identity.name if hasattr(se失败时静默忽略
        else:
            for m_name, m_cloning in self._members.items():
                try:
                    r = m_cloning.analyze(problem, context)
                    analyses.append(r)
                    participants.append(m_name)
                except Exception:
                    pass  # participants.append(m_name)失败时静默忽略

        if not analyses:
            return ClusterResult(
                cluster_name=self.name,
                method=method,
                synthesis="",
                participant_count=0,
                leader_analysis=None,
            )

        # 构建综合结果
        primary = analyses[0]
        synthesis_parts = []
        for a in analyses:
            content = getattr(a, 'analysis_content', '') or getattr(a, 'core_insight', '')
            if content:
                synthesis_parts.append(content[:100])

        if method == "debate":
            synthesis = "【辩论】" + "; ".join(synthesis_parts[:5])
        elif method == "synthesis":
            synthesis = " | ".join(synthesis_parts[:5])
        elif method == "consensus":
            synthesis = synthesis_parts[0] if synthesis_parts else ""
        else:
            synthesis = synthesis_parts[0] if synthesis_parts else ""

        leader_analysis = primary if (method == "leader" and self._leader) else None

        return ClusterResult(
            cluster_name=self.name,
            method=method,
            synthesis=synthesis,
            participant_count=len(participants),
            leader_analysis=leader_analysis,
        )
