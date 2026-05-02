# -*- coding: utf-8 -*-
"""
贤者协作规则 — Sage Collaboration Rules S1.0
================================================

从已废弃的 src/collaboration/ 模块中提炼有价值的能力，
整合为神之架构内贤者协作的统一规则引擎。

核心能力:
1. 品秩仲裁 — 基于 NobilityRank / PinRank 的运行时决策仲裁
2. 协作角色约束 — 主Claw资格验证、参与者权限检查
3. 冲突升级流程 — 声明→品秩仲裁→裁决→执行
4. 冲突解决策略 — 最后写入胜出 / 最先写入胜出 / 品秩仲裁 / 共识融合

设计原则:
- 不持有状态，纯规则判断（与 CourtPositionRegistry 查询分离）
- A轨调用品秩仲裁审核B轨协作结果
- B轨在协作执行前调用角色约束检查
- 所有方法返回结构化结果，不抛异常
"""

import logging
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger(__name__)

__all__ = [
    "SageCollaborationRules",
    "ArbitrationResult",
    "CollaborationCheckResult",
    "ConflictEscalation",
    "ConflictResolution",
    "ConflictStrategy",
    "get_sage_collaboration_rules",
    "register_sage_authority",
    "batch_register_authority",
    "_CORE_SAGE_AUTHORITY",
]

# ═══════════════════════════════════════════════════════════════════════════════
# 一、数据结构
# ═══════════════════════════════════════════════════════════════════════════════


class ConflictStrategy(str, Enum):
    """冲突解决策略（提炼自旧 collaboration_engine.py）"""
    LAST_WRITES_WINS = "last_writes_wins"       # 最后写入胜出
    FIRST_WRITES_WINS = "first_writes_wins"     # 最先写入胜出
    NOBILITY_ARBITRATION = "nobility_arbitration" # 品秩仲裁（新增）
    CONSENSUS_FUSION = "consensus_fusion"        # 共识融合（新增）


@dataclass
class ArbitrationResult:
    """品秩仲裁结果"""
    winner: str = ""                    # 胜出者名称
    winner_authority: int = 99          # 胜出者权威值
    loser: str = ""                     # 败方名称
    loser_authority: int = 99           # 败方权威值
    reason: str = ""                    # 裁决理由
    is_decisive: bool = True            # 是否压倒性裁决（权威差 >= 10）

    @property
    def as_dict(self) -> Dict[str, Any]:
        return {
            "winner": self.winner,
            "winner_authority": self.winner_authority,
            "loser": self.loser,
            "loser_authority": self.loser_authority,
            "reason": self.reason,
            "is_decisive": self.is_decisive,
        }


@dataclass
class CollaborationCheckResult:
    """协作权限检查结果"""
    passed: bool = False
    primary_claw: str = ""
    issue: str = ""                     # 未通过原因
    warnings: List[str] = field(default_factory=list)

    @property
    def as_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "primary_claw": self.primary_claw,
            "issue": self.issue,
            "warnings": self.warnings,
        }


@dataclass
class ConflictEscalation:
    """冲突升级记录"""
    escalation_id: str = ""
    declared_at: float = 0.0
    parties: List[str] = field(default_factory=list)
    topic: str = ""
    strategy: ConflictStrategy = ConflictStrategy.NOBILITY_ARBITRATION
    arbitration: Optional[ArbitrationResult] = None
    resolution: Optional[str] = None    # 冲突解决文本
    resolved: bool = False
    resolved_at: float = 0.0


# 冲突解决结果
ConflictResolution = Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]
# (采纳的结论列表, 丢弃的结论列表)


# ═══════════════════════════════════════════════════════════════════════════════
# 二、核心贤者品秩降级表
# ═══════════════════════════════════════════════════════════════════════════════
# 当 CourtPositionRegistry 不可用时（如开发环境/轻量部署），
# 使用此内置表进行品秩仲裁，确保仲裁能力始终可用。
#
# 权威值规则（越小权威越高）:
#   王爵=0, 公爵=1, 侯爵=2, 伯爵=5
#   正一品=10, 从一品=11, ... 正九品=90, 从九品=91
#   无记录=99

_CORE_SAGE_AUTHORITY: Dict[str, int] = {
    # ── 王爵级（最高决策权）──
    "孔子": 0,        # 万世师表，至圣先师

    # ── 公爵级（等同/高于一品）──
    "老子": 1,        # 道家创始人
    "庄子": 1,        # 道家集大成
    "墨子": 2,        # 墨家创始人，侯爵级

    # ── 侯爵级（等同一品）──
    "韩非子": 2,      # 法家集大成
    "孟子": 3,        # 儒家亚圣
    "荀子": 3,        # 儒家大师
    "管仲": 3,        # 法家先驱，名相
    "鬼谷子": 3,      # 纵横家创始人
    "孙子": 3,        # 兵家至圣

    # ── 伯爵级（等同三品）──
    "商鞅": 5,        # 法家改革家
    "苏秦": 5,        # 纵横家
    "张仪": 5,        # 纵横家
    "吕不韦": 5,      # 杂家
    "朱熹": 5,        # 理学集大成
    "王阳明": 5,      # 心学创始人
    "诸葛亮": 5,      # 蜀汉丞相

    # ── 正三品到正五品 ──
    "贾谊": 10,       # 汉代政论家
    "董仲舒": 10,     # 儒学制度化
    "王安石": 10,     # 改革家
    "司马迁": 10,     # 史学家
    "司马光": 10,     # 资治通鉴
    "张仲景": 10,     # 医圣

    # ── 正五品到从五品 ──
    "白居易": 20,     # 诗人
    "杜甫": 20,       # 诗圣
    "李白": 20,       # 诗仙
    "苏轼": 20,       # 文豪
    "韩愈": 20,       # 唐宋八大家

    # ── 正六品以下 ──
    "鲁班": 30,       # 工匠祖师
    "蔡伦": 30,       # 造纸术
    "贾思勰": 30,     # 农学
    "沈括": 30,       # 博学家
}


def register_sage_authority(name: str, authority: int) -> None:
    """
    动态注册贤者权威值到内置降级表。

    优先级: CourtPositionRegistry > 内置表 > 99

    Args:
        name: 贤者名称
        authority: 权威值（越小越高）
    """
    _CORE_SAGE_AUTHORITY[name] = authority


def batch_register_authority(authority_map: Dict[str, int]) -> int:
    """批量注册，返回注册数量"""
    count = 0
    for name, auth in authority_map.items():
        if name not in _CORE_SAGE_AUTHORITY:
            _CORE_SAGE_AUTHORITY[name] = auth
            count += 1
    return count


# ═══════════════════════════════════════════════════════════════════════════════
# 二、核心规则引擎
# ═══════════════════════════════════════════════════════════════════════════════

class SageCollaborationRules:
    """
    贤者协作规则引擎 S1.0

    集成点:
    - A轨: _supervise_execution / _review_result 调用品秩仲裁
    - B轨: 协作执行前调用 check_collaboration_eligibility
    - 协作协议: _dispatch_collaboration.CollaborationProtocol 可选用 resolve_conflict
    """

    VERSION = "S1.0"

    def __init__(self):
        # 品秩权威缓存 {claw_name: authority_value}
        self._authority_cache: Dict[str, int] = {}
        self._cache_lock = threading.Lock()

    # ─────────────────────────────────────────────────────────────
    # 2.1 品秩仲裁
    # ─────────────────────────────────────────────────────────────

    def get_authority_value(self, claw_name: str) -> int:
        """
        获取贤者的运行时权威值。

        权威值决定仲裁优先级，越低越优先：
        - 王爵=0, 公爵=1, 侯爵=2, 伯爵=5, 无爵位=99
        - 无爵位时回退到品秩值（正一品=10, 从九品=91）

        Args:
            claw_name: 贤者名称（如 "孔子", "韩非子"）

        Returns:
            权威值（越小权威越高）
        """
        with self._cache_lock:
            if claw_name in self._authority_cache:
                return self._authority_cache[claw_name]

        authority = self._query_authority(claw_name)

        with self._cache_lock:
            self._authority_cache[claw_name] = authority
        return authority

    def _query_authority(self, claw_name: str) -> int:
        """从 CourtPositionRegistry 查询权威值，不可用时回退到内置降级表"""
        # 优先从 CourtPositionRegistry 查询
        try:
            from ...engines.cloning._court_positions import (
                get_sage_court_position, NobilityRank,
            )
            info = get_sage_court_position(claw_name)
            if info is not None:
                nobility = info.get("nobility")
                if nobility is not None and nobility != NobilityRank.NOBLE_NONE.value:
                    try:
                        from ...engines.cloning.court_enums import (
                            _NOBILITY_AUTHORITY, NobilityRank as NR,
                        )
                        return _NOBILITY_AUTHORITY[NR(nobility)]
                    except (KeyError, ValueError):
                        pass
                pin = info.get("pin")
                if pin is not None:
                    return int(pin)
        except ImportError:
            pass
        except Exception as e:
            logger.debug(f"[协作规则] CourtPositionRegistry 查询 {claw_name} 失败: {e}")

        # 回退: 内置核心贤者品秩降级表
        builtin = _CORE_SAGE_AUTHORITY.get(claw_name)
        if builtin is not None:
            logger.debug(f"[协作规则] {claw_name} 使用内置品秩: {builtin}")
            return builtin

        # 最终回退
        return 99

    def arbitrate_by_nobility(
        self,
        party_a: str,
        party_b: str,
        topic: str = "",
    ) -> ArbitrationResult:
        """
        品秩仲裁：比较两位贤者的权威值决定胜出方。

        Args:
            party_a: 甲方贤者名称
            party_b: 乙方贤者名称
            topic: 争议主题（用于日志）

        Returns:
            ArbitrationResult 仲裁结果
        """
        auth_a = self.get_authority_value(party_a)
        auth_b = self.get_authority_value(party_b)

        if auth_a < auth_b:
            winner, loser = party_a, party_b
            w_auth, l_auth = auth_a, auth_b
        elif auth_b < auth_a:
            winner, loser = party_b, party_a
            w_auth, l_auth = auth_b, auth_a
        else:
            # 权威值相同，品秩仲裁无法裁决
            return ArbitrationResult(
                winner="", loser="",
                winner_authority=auth_a, loser_authority=auth_b,
                reason=f"{party_a} 与 {party_b} 权威值相同（{auth_a}），品秩仲裁无法裁决",
                is_decisive=False,
            )

        decisive = abs(auth_a - auth_b) >= 10
        reason = (
            f"{winner}（权威值 {w_auth}）优于 {loser}（权威值 {l_auth}），"
            f"{'压倒性' if decisive else '轻微'}胜出"
        )

        logger.info(f"[协作规则-仲裁] {topic or '争议'}: {reason}")

        return ArbitrationResult(
            winner=winner, loser=loser,
            winner_authority=w_auth, loser_authority=l_auth,
            reason=reason, is_decisive=decisive,
        )

    def arbitrate_multi(
        self,
        parties: List[str],
        topic: str = "",
    ) -> ArbitrationResult:
        """
        多方品秩仲裁：从多个贤者中选出权威最高者。

        Args:
            parties: 参与仲裁的贤者名称列表
            topic: 争议主题

        Returns:
            ArbitrationResult（winner为最高权威者）
        """
        if not parties:
            return ArbitrationResult(reason="无参与方")
        if len(parties) == 1:
            auth = self.get_authority_value(parties[0])
            return ArbitrationResult(
                winner=parties[0], winner_authority=auth,
                reason=f"仅 {parties[0]} 一方参与，直接胜出",
                is_decisive=True,
            )

        # 按权威值排序
        auth_pairs = [(name, self.get_authority_value(name)) for name in parties]
        auth_pairs.sort(key=lambda x: x[1])

        winner_name, winner_auth = auth_pairs[0]
        runner_name, runner_auth = auth_pairs[1]

        decisive = (runner_auth - winner_auth) >= 10
        reason = (
            f"{winner_name}（权威值 {winner_auth}）在 {len(parties)} 方中权威最高，"
            f"领先 {runner_name}（{runner_auth}），"
            f"{'压倒性' if decisive else '轻微'}胜出"
        )

        logger.info(f"[协作规则-多方仲裁] {topic or '争议'}: {reason}")

        return ArbitrationResult(
            winner=winner_name, winner_authority=winner_auth,
            loser=runner_name, loser_authority=runner_auth,
            reason=reason, is_decisive=decisive,
        )

    # ─────────────────────────────────────────────────────────────
    # 2.2 协作角色约束
    # ─────────────────────────────────────────────────────────────

    def check_collaboration_eligibility(
        self,
        primary_claw: str,
        collaborators: List[str],
        task_description: str = "",
    ) -> CollaborationCheckResult:
        """
        检查协作组是否满足角色约束。

        规则:
        1. primary_claw 必须具有 is_primary 资格（B轨 YAML can_lead）
        2. primary_claw 品秩应 >= 所有协作者的最低品秩（主Claw不能是品秩最低者）
        3. 至少1个协作者

        Args:
            primary_claw: 主Claw名称
            collaborators: 协作者名称列表
            task_description: 任务描述

        Returns:
            CollaborationCheckResult
        """
        warnings = []

        # 规则1: 至少1个协作者
        if not collaborators:
            return CollaborationCheckResult(
                passed=False,
                primary_claw=primary_claw,
                issue="至少需要1个协作者",
            )

        # 规则2: 主Claw资格检查
        primary_auth = self.get_authority_value(primary_claw)
        if primary_auth >= 99:
            # 99表示无岗位信息，发出警告但不阻断
            warnings.append(f"主Claw {primary_claw} 无岗位信息，品秩仲裁不可用")

        # 规则3: 主Claw品秩应不低于最弱协作者
        collab_authorities = {
            name: self.get_authority_value(name) for name in collaborators
        }

        min_collab_auth = min(collab_authorities.values())
        min_collab_name = min(collab_authorities, key=collab_authorities.get)

        # 权威值越大越弱，所以 primary_auth 应 <= min_collab_auth
        if primary_auth > min_collab_auth and primary_auth < 99:
            # 主Claw品秩低于（权威值高于）最弱协作者
            warnings.append(
                f"主Claw {primary_claw}（权威值 {primary_auth}）"
                f"低于协作者 {min_collab_name}（权威值 {min_collab_auth}），"
                f"建议调换主Claw"
            )

        passed = True
        issue = ""
        if not warnings:
            issue = ""
        else:
            # 警告不阻断，只记录
            logger.info(
                f"[协作规则] {primary_claw} 主导协作检查: "
                f"{len(collaborators)} 位协作者, {len(warnings)} 条警告"
            )

        return CollaborationCheckResult(
            passed=passed,
            primary_claw=primary_claw,
            issue=issue,
            warnings=warnings,
        )

    def suggest_primary(
        self,
        participants: List[str],
        task_description: str = "",
    ) -> Tuple[str, int]:
        """
        从参与者中推荐最适合担任主Claw的贤者。

        策略: 权威值最低（品秩最高）的贤者担任主Claw。

        Returns:
            (推荐贤者名称, 权威值)
        """
        if not participants:
            return ("", 99)

        auth_pairs = [(name, self.get_authority_value(name)) for name in participants]
        auth_pairs.sort(key=lambda x: x[1])

        return auth_pairs[0]

    # ─────────────────────────────────────────────────────────────
    # 2.3 冲突升级流程
    # ─────────────────────────────────────────────────────────────

    def declare_conflict(
        self,
        party_a: str,
        party_b: str,
        topic: str,
        strategy: ConflictStrategy = ConflictStrategy.NOBILITY_ARBITRATION,
    ) -> ConflictEscalation:
        """
        声明冲突并进入升级流程。

        流程: 声明 → 仲裁 → 裁决 → 执行

        Args:
            party_a: 冲突方A
            party_b: 冲突方B
            topic: 冲突主题
            strategy: 解决策略

        Returns:
            ConflictEscalation 升级记录
        """
        import uuid
        escalation = ConflictEscalation(
            escalation_id=str(uuid.uuid4())[:8],
            declared_at=time.time(),
            parties=[party_a, party_b],
            topic=topic,
            strategy=strategy,
        )

        logger.info(
            f"[协作规则-冲突] 冲突 #{escalation.escalation_id} 声明: "
            f"{party_a} vs {party_b} — {topic}"
        )

        # 自动仲裁
        if strategy == ConflictStrategy.NOBILITY_ARBITRATION:
            arbitration = self.arbitrate_by_nobility(party_a, party_b, topic)
            escalation.arbitration = arbitration
            if arbitration.is_decisive:
                escalation.resolved = True
                escalation.resolved_at = time.time()
                escalation.resolution = arbitration.reason
                logger.info(
                    f"[协作规则-冲突] #{escalation.escalation_id} 自动裁决: "
                    f"{arbitration.winner} 胜出"
                )
            else:
                escalation.resolution = "品秩相同，需人工裁决"
                logger.info(
                    f"[协作规则-冲突] #{escalation.escalation_id} 仲裁无果，等待人工裁决"
                )

        return escalation

    def resolve_conflict(
        self,
        conclusions: List[Dict[str, Any]],
        strategy: ConflictStrategy = ConflictStrategy.LAST_WRITES_WINS,
    ) -> ConflictResolution:
        """
        解决结论冲突。

        提炼自旧 collaboration_engine.ConflictResolver，扩展为4种策略。

        Args:
            conclusions: 结论列表，每个结论需包含 'author' 和 'timestamp' 字段
            strategy: 解决策略

        Returns:
            (采纳的结论列表, 丢弃的结论列表)
        """
        if not conclusions:
            return ([], [])

        if len(conclusions) == 1:
            return (conclusions, [])

        if strategy == ConflictStrategy.LAST_WRITES_WINS:
            # 最后写入胜出
            sorted_conclusions = sorted(
                conclusions,
                key=lambda c: c.get("timestamp", 0) or 0,
            )
            return ([sorted_conclusions[-1]], sorted_conclusions[:-1])

        elif strategy == ConflictStrategy.FIRST_WRITES_WINS:
            # 最先写入胜出
            sorted_conclusions = sorted(
                conclusions,
                key=lambda c: c.get("timestamp", 0) or 0,
            )
            return ([sorted_conclusions[0]], sorted_conclusions[1:])

        elif strategy == ConflictStrategy.NOBILITY_ARBITRATION:
            # 品秩仲裁: 权威最高的结论胜出
            authors = [c.get("author", "") for c in conclusions]
            if len(set(authors)) <= 1:
                # 同一作者，回退到最后写入
                return self.resolve_conflict(
                    conclusions, ConflictStrategy.LAST_WRITES_WINS
                )

            arbitration = self.arbitrate_multi(authors)
            if arbitration.winner:
                accepted = [
                    c for c in conclusions
                    if c.get("author") == arbitration.winner
                ]
                rejected = [
                    c for c in conclusions
                    if c.get("author") != arbitration.winner
                ]
                return (accepted, rejected)
            else:
                # 无法裁决，回退到最后写入
                return self.resolve_conflict(
                    conclusions, ConflictStrategy.LAST_WRITES_WINS
                )

        elif strategy == ConflictStrategy.CONSENSUS_FUSION:
            # 共识融合: 全部采纳（不做丢弃）
            # 调用方负责做合成
            return (conclusions, [])

        return ([conclusions[-1]], conclusions[:-1])

    def review_collaboration_result(
        self,
        result: Dict[str, Any],
        collaborators: List[str],
    ) -> Dict[str, Any]:
        """
        A轨专用的协作结果审核。

        在 A轨 _review_result() 中调用，审核B轨多Claw协作的结果。

        检查项:
        1. 各贡献者是否在协作名单内
        2. 主Claw是否是品秩最高者
        3. 是否存在未解决的冲突

        Args:
            result: B轨协作执行结果
            collaborators: 参与协作的Claw名称列表

        Returns:
            审核结果字典，附加到原有result中
        """
        review = {
            "collaboration_review": True,
            "review_passed": True,
            "review_issues": [],
            "review_warnings": [],
        }

        if not result:
            review["review_passed"] = False
            review["review_issues"].append("执行结果为空")
            return review

        # 检查贡献者
        contributions = result.get("contributions", [])
        if contributions:
            actual_contributors = set()
            for contrib in contributions:
                author = contrib.get("claw_name", contrib.get("author", ""))
                if author:
                    actual_contributors.add(author)

            # 检查是否有未授权参与者
            expected_set = set(collaborators)
            unexpected = actual_contributors - expected_set
            if unexpected:
                review["review_warnings"].append(
                    f"未授权参与者: {', '.join(unexpected)}"
                )

            # 检查主Claw品秩
            primary = result.get("primary_claw", "")
            if primary and len(actual_contributors) > 1:
                suggested, _ = self.suggest_primary(list(actual_contributors))
                if suggested and suggested != primary:
                    review["review_warnings"].append(
                        f"主Claw {primary} 品秩非最高，建议 {suggested} 主导"
                    )

        # 检查冲突标记
        conflicts = result.get("conflicts", [])
        if conflicts:
            review["review_warnings"].append(
                f"存在 {len(conflicts)} 处未解决冲突"
            )

        return review

    # ─────────────────────────────────────────────────────────────
    # 2.4 缓存管理
    # ─────────────────────────────────────────────────────────────

    def invalidate_cache(self, claw_name: Optional[str] = None) -> None:
        """清除权威值缓存"""
        with self._cache_lock:
            if claw_name:
                self._authority_cache.pop(claw_name, None)
            else:
                self._authority_cache.clear()

    def get_stats(self) -> Dict[str, Any]:
        """获取规则引擎统计"""
        return {
            "version": self.VERSION,
            "cached_authorities": len(self._authority_cache),
            "authority_snapshot": dict(self._authority_cache),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# 三、单例管理
# ═══════════════════════════════════════════════════════════════════════════════

_rules_instance: Optional[SageCollaborationRules] = None
_rules_lock = threading.Lock()


def get_sage_collaboration_rules() -> SageCollaborationRules:
    """获取 SageCollaborationRules 单例"""
    global _rules_instance
    if _rules_instance is None:
        with _rules_lock:
            if _rules_instance is None:
                _rules_instance = SageCollaborationRules()
    return _rules_instance
