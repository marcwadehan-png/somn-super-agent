"""
大秦指标考核引擎 v1.0.0
_daqin_metrics.py

神之架构v3.3 全局目标管理引擎。
覆盖决策层以下全部层级：高级管理层（侯爵/伯爵/正一至三品）、
中级管理层（正四品至从七品）、执行层（正八品至从九品/专员）。

核心流程：
  1. 目标制定与对齐（季度初）
  2. 过程跟踪与调整（季度中）
  3. 期末评估与反馈（季度末）

大秦指标 = 原 OKR 考核体系，经神之架构秦制化改造。
"""

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════
#  枚举与类型
# ═══════════════════════════════════════════════════════════════

class MetricsLevel(Enum):
    """大秦指标层级"""
    ORGANIZATION = "帝国级"      # 七人代表大会制定
    SYSTEM = "系统级"            # 高级管理层（侯爵/伯爵/正一至三品）
    DEPARTMENT = "部门级"        # 中级管理层（正四品至从七品）
    INDIVIDUAL = "个人级"        # 执行层（正八品至从九品/专员）


class KRStatus(Enum):
    """KR状态（红黄绿灯）"""
    GREEN = "绿灯"      # >= 0.7
    YELLOW = "黄灯"     # 0.4 ~ 0.7
    RED = "红灯"        # < 0.4


class QuarterPeriod(Enum):
    """季度"""
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"


class EvaluationDimension(Enum):
    """评估维度"""
    SELF = "自评"           # 40%
    MANAGER = "主管评"      # 40%
    PEER = "互评"           # 20%


@dataclass
class KeyResult:
    """关键结果（KR）"""
    kr_id: str
    description: str          # KR描述
    target_value: float       # 目标值
    current_value: float = 0  # 当前值
    score: float = 0          # 评分 0~1
    weight: float = 1.0       # 权重（默认1.0）
    updated_at: float = 0     # 最后更新时间
    notes: str = ""           # 备注

    def update_progress(self, current_value: float, notes: str = "") -> Dict[str, Any]:
        """更新KR进展"""
        self.current_value = current_value
        self.updated_at = time.time()
        self.notes = notes
        if self.target_value > 0:
            self.score = min(1.0, current_value / self.target_value)
        return {
            "kr_id": self.kr_id,
            "score": round(self.score, 3),
            "status": self.get_status().value,
            "progress": f"{current_value}/{self.target_value}",
        }

    def get_status(self) -> KRStatus:
        """获取红黄绿灯状态"""
        if self.score >= 0.7:
            return KRStatus.GREEN
        elif self.score >= 0.4:
            return KRStatus.YELLOW
        return KRStatus.RED


@dataclass
class Objective:
    """目标（O）"""
    o_id: str
    description: str           # O描述
    level: MetricsLevel
    owner: str                 # 负责人
    parent_o_id: str = ""     # 承接的上游O编号（对齐用）
    system_name: str = ""     # 所属系统
    department: str = ""      # 所属部门
    krs: List[KeyResult] = field(default_factory=list)
    quarter: str = ""         # 季度（如"2026-Q2"）

    def add_kr(self, description: str, target_value: float, weight: float = 1.0) -> KeyResult:
        """添加KR（每O不超过3个）"""
        if len(self.krs) >= 3:
            raise ValueError(f"目标{self.o_id}已有{len(self.krs)}个KR，不允许超过3个")
        kr = KeyResult(
            kr_id=f"KR-{uuid.uuid4().hex[:8]}",
            description=description,
            target_value=target_value,
            weight=weight,
        )
        self.krs.append(kr)
        return kr

    def get_overall_score(self) -> float:
        """计算O的综合得分（KR加权平均）"""
        if not self.krs:
            return 0
        total_weight = sum(kr.weight for kr in self.krs)
        if total_weight == 0:
            return 0
        return sum(kr.score * kr.weight for kr in self.krs) / total_weight

    def get_status_summary(self) -> Dict[str, Any]:
        """获取O的状态摘要"""
        kr_statuses = [kr.get_status() for kr in self.krs]
        return {
            "o_id": self.o_id,
            "description": self.description,
            "level": self.level.value,
            "owner": self.owner,
            "overall_score": round(self.get_overall_score(), 3),
            "kr_count": len(self.krs),
            "green_count": kr_statuses.count(KRStatus.GREEN),
            "yellow_count": kr_statuses.count(KRStatus.YELLOW),
            "red_count": kr_statuses.count(KRStatus.RED),
            "status": KRStatus.GREEN.value if self.get_overall_score() >= 0.7
                      else KRStatus.YELLOW.value if self.get_overall_score() >= 0.4
                      else KRStatus.RED.value,
        }


@dataclass
class MetricsSet:
    """一个季度的一组大秦指标"""
    set_id: str
    owner: str
    level: MetricsLevel
    quarter: str               # "2026-Q2"
    objectives: List[Objective] = field(default_factory=list)

    def add_objective(self, description: str, parent_o_id: str = "",
                      system_name: str = "", department: str = "") -> Objective:
        """添加O（每季度不超过3个）"""
        if len(self.objectives) >= 3:
            raise ValueError(f"{self.owner}已有{len(self.objectives)}个O，不允许超过3个")
        o = Objective(
            o_id=f"O-{uuid.uuid4().hex[:8]}",
            description=description,
            level=self.level,
            owner=self.owner,
            parent_o_id=parent_o_id,
            system_name=system_name,
            department=department,
            quarter=self.quarter,
        )
        self.objectives.append(o)
        return o

    def get_overall_score(self) -> float:
        """季度总评分（所有O等权平均）"""
        if not self.objectives:
            return 0
        return sum(o.get_overall_score() for o in self.objectives) / len(self.objectives)


@dataclass
class Evaluation:
    """季度评估结果"""
    eval_id: str
    owner: str
    quarter: str
    self_score: float = 0           # 自评 40%
    manager_score: float = 0        # 主管评 40%
    peer_score: float = 0           # 互评 20%
    final_score: float = 0          # 综合分
    manager_feedback: str = ""      # 主管书面反馈
    improvement_plan: str = ""      # 改进计划
    evaluated_at: float = 0

    def calculate_final(self) -> float:
        """计算综合评分"""
        self.final_score = (
            self.self_score * 0.4
            + self.manager_score * 0.4
            + self.peer_score * 0.2
        )
        self.evaluated_at = time.time()
        return round(self.final_score, 3)

    def get_evaluation_result(self) -> Dict[str, Any]:
        """获取评估结果"""
        if self.final_score >= 0.7:
            result = "超预期"
            action = "公开表彰，案例报送藏书阁"
        elif self.final_score >= 0.4:
            result = "部分达成"
            action = "分析短板，制定改进计划"
        else:
            result = "未达成"
            action = "根因分析，调整下季度目标难度，非追责"
        return {
            "owner": self.owner,
            "quarter": self.quarter,
            "self_score": round(self.self_score, 3),
            "manager_score": round(self.manager_score, 3),
            "peer_score": round(self.peer_score, 3),
            "final_score": round(self.final_score, 3),
            "result": result,
            "action": action,
            "feedback": self.manager_feedback,
        }


# ═══════════════════════════════════════════════════════════════
#  大秦指标引擎核心
# ═══════════════════════════════════════════════════════════════

class DaqinMetricsEngine:
    """
    大秦指标考核引擎。

    管理全系统的目标制定、跟踪、评估流程。
    所有指标数据可供藏书阁存储和查询。
    与行政之鞭引擎联动，评分直接影响鞭策强度。
    """

    def __init__(self):
        self._metrics_sets: Dict[str, MetricsSet] = {}      # owner -> MetricsSet
        self._evaluations: Dict[str, Evaluation] = {}        # owner -> Evaluation
        self._history: List[Dict[str, Any]] = []

    # ── 指标创建 ──

    def create_metrics_set(
        self,
        owner: str,
        level: MetricsLevel,
        quarter: str,
    ) -> MetricsSet:
        """为某成员创建一个季度的指标集"""
        metrics_set = MetricsSet(
            set_id=f"DQ-{uuid.uuid4().hex[:8]}",
            owner=owner,
            level=level,
            quarter=quarter,
        )
        self._metrics_sets[f"{owner}_{quarter}"] = metrics_set
        self._history.append({
            "action": "create_metrics_set",
            "owner": owner,
            "level": level.value,
            "quarter": quarter,
            "timestamp": time.time(),
        })
        return metrics_set

    # ── 进度跟踪 ──

    def update_kr(
        self,
        owner: str,
        quarter: str,
        o_id: str,
        kr_id: str,
        current_value: float,
        notes: str = "",
    ) -> Optional[Dict[str, Any]]:
        """更新某个KR的进展"""
        key = f"{owner}_{quarter}"
        metrics_set = self._metrics_sets.get(key)
        if not metrics_set:
            return {"error": f"未找到{owner}在{quarter}的大秦指标"}

        for obj in metrics_set.objectives:
            if obj.o_id == o_id:
                for kr in obj.krs:
                    if kr.kr_id == kr_id:
                        result = kr.update_progress(current_value, notes)
                        self._history.append({
                            "action": "update_kr",
                            "owner": owner,
                            "o_id": o_id,
                            "kr_id": kr_id,
                            "score": result["score"],
                            "timestamp": time.time(),
                        })
                        return result
        return {"error": f"未找到O={o_id}/KR={kr_id}"}

    # ── 状态查询 ──

    def get_owner_status(self, owner: str, quarter: str) -> Optional[Dict[str, Any]]:
        """获取某成员的指标状态"""
        key = f"{owner}_{quarter}"
        metrics_set = self._metrics_sets.get(key)
        if not metrics_set:
            return {"error": f"未找到{owner}在{quarter}的大秦指标"}

        return {
            "owner": owner,
            "level": metrics_set.level.value,
            "quarter": quarter,
            "overall_score": round(metrics_set.get_overall_score(), 3),
            "objectives": [o.get_status_summary() for o in metrics_set.objectives],
        }

    def get_dashboard(self, quarter: str) -> Dict[str, Any]:
        """
        生成季度大秦指标看板。

        返回各层级整体数据。
        """
        sets = [s for s in self._metrics_sets.values() if s.quarter == quarter]
        if not sets:
            return {"error": f"未找到{quarter}的大秦指标数据"}

        dashboard = {
            "quarter": quarter,
            "total_members": len(sets),
            "by_level": {},
            "alerts": [],  # 逾期未更新等
        }

        for level in MetricsLevel:
            level_sets = [s for s in sets if s.level == level]
            if not level_sets:
                continue
            scores = [s.get_overall_score() for s in level_sets]
            dashboard["by_level"][level.value] = {
                "count": len(level_sets),
                "avg_score": round(sum(scores) / len(scores), 3),
                "green": sum(1 for s in scores if s >= 0.7),
                "yellow": sum(1 for s in scores if 0.4 <= s < 0.7),
                "red": sum(1 for s in scores if s < 0.4),
            }

        # 逾期预警
        now = time.time()
        for metrics_set in sets:
            for obj in metrics_set.objectives:
                for kr in obj.krs:
                    if kr.updated_at > 0 and (now - kr.updated_at) > 14 * 86400:
                        dashboard["alerts"].append({
                            "owner": metrics_set.owner,
                            "o_id": obj.o_id,
                            "kr_id": kr.kr_id,
                            "days_since_update": int((now - kr.updated_at) / 86400),
                        })

        return dashboard

    # ── 评估 ──

    def submit_evaluation(
        self,
        owner: str,
        quarter: str,
        self_score: float = 0,
        manager_score: float = 0,
        peer_score: float = 0,
        manager_feedback: str = "",
        improvement_plan: str = "",
    ) -> Evaluation:
        """提交季度评估"""
        evaluation = Evaluation(
            eval_id=f"EVAL-{uuid.uuid4().hex[:8]}",
            owner=owner,
            quarter=quarter,
            self_score=self_score,
            manager_score=manager_score,
            peer_score=peer_score,
            manager_feedback=manager_feedback,
            improvement_plan=improvement_plan,
        )
        evaluation.calculate_final()
        self._evaluations[f"{owner}_{quarter}"] = evaluation
        self._history.append({
            "action": "submit_evaluation",
            "owner": owner,
            "quarter": quarter,
            "final_score": evaluation.final_score,
            "timestamp": time.time(),
        })
        return evaluation

    # ── 数据导出（供藏书阁收录） ──

    def export_quarter_data(self, quarter: str) -> Dict[str, Any]:
        """导出季度全量数据（供藏书阁收录）"""
        sets = [s for s in self._metrics_sets.values() if s.quarter == quarter]
        evals = [
            e for e in self._evaluations.values() if e.quarter == quarter
        ]

        return {
            "quarter": quarter,
            "exported_at": time.time(),
            "metrics_sets": [
                {
                    "owner": s.owner,
                    "level": s.level.value,
                    "overall_score": round(s.get_overall_score(), 3),
                    "objectives": [
                        {
                            "o_id": o.o_id,
                            "description": o.description,
                            "parent_o_id": o.parent_o_id,
                            "score": round(o.get_overall_score(), 3),
                            "krs": [
                                {
                                    "kr_id": kr.kr_id,
                                    "description": kr.description,
                                    "target": kr.target_value,
                                    "current": kr.current_value,
                                    "score": round(kr.score, 3),
                                    "status": kr.get_status().value,
                                }
                                for kr in o.krs
                            ],
                        }
                        for o in s.objectives
                    ],
                }
                for s in sets
            ],
            "evaluations": [
                e.get_evaluation_result() for e in evals
            ],
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计"""
        return {
            "total_metrics_sets": len(self._metrics_sets),
            "total_evaluations": len(self._evaluations),
            "total_operations": len(self._history),
            "quarters": sorted(set(s.quarter for s in self._metrics_sets.values())),
        }

    # ── 向后兼容别名 ──

    # OKRSet -> MetricsSet 别名
    @property
    def _okr_sets(self) -> Dict[str, MetricsSet]:
        return self._metrics_sets


# ═══════════════════════════════════════════════════════════════
#  向后兼容别名（保持旧代码可用）
# ═══════════════════════════════════════════════════════════════

OKRLevel = MetricsLevel
OKRSet = MetricsSet
OKREngine = DaqinMetricsEngine
