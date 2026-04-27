# -*- coding: utf-8 -*-
"""
七人决策代表大会 v4.0.0
_decision_congress.py

[v4.0.0 道家升级] 新增道家否决权（DaoVeto）机制——
体现"过犹不及"的中道智慧和"上善若水"的平衡哲学。

核心变更：
  - 新增 MemberRole.DAO_VETO：道家否决角色
  - 新增 CongressMember.is_dao_veto_member：否决权标记
  - 新增 DaoVetoConfig：否决权配置（触发条件、重审流程）
  - 修改 submit_command：投票后增加否决检查
  - 新增 dao_veto_check：否决权行使分析
  - 新增 trigger_yinyang_review：阴阳辩证重审

核心理念："过犹不及"——票数过于集中在某一极端方向，
反而说明决策缺乏阴阳平衡，需要重新审视。
"""

import logging
import os
import re
import time
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# 从共享工具模块导入（v3.3.6 提取，消除重复）
from ._dispatch_utils import find_project_root, load_yaml, deep_merge

# 向后兼容别名
_find_project_root = find_project_root
_load_yaml = load_yaml
_deep_merge = deep_merge


# 项目根目录
_PROJECT_ROOT = _find_project_root()

# 配置文件路径
_COURT_CONFIG_PATH = _PROJECT_ROOT / "config" / "court_config.yaml"
_RUNTIME_OVERRIDE_PATH = _PROJECT_ROOT / "data" / "imperial_library" / "congress_runtime.yaml"

# 缓存已加载的配置（模块级，只加载一次）
_LOADED_CONFIG: Optional[Dict[str, Any]] = None


def load_court_config() -> Dict[str, Any]:
    """
    加载神之架构配置（合并基准 + 运行时覆盖）。

    加载顺序:
    1. config/court_config.yaml — 基准配置（人工可编辑）
    2. data/imperial_library/congress_runtime.yaml — 运行时覆盖（系统自主迭代）
    """
    global _LOADED_CONFIG
    if _LOADED_CONFIG is not None:
        return _LOADED_CONFIG

    # 基准配置
    baseline = _load_yaml(_COURT_CONFIG_PATH) if _COURT_CONFIG_PATH.exists() else {}
    if not baseline:
        logger.warning("基准配置 court_config.yaml 不存在或为空，使用内置默认值")

    # 运行时覆盖
    runtime = _load_yaml(_RUNTIME_OVERRIDE_PATH) if _RUNTIME_OVERRIDE_PATH.exists() else {}

    # 合并
    _LOADED_CONFIG = _deep_merge(baseline, runtime)

    logger.info(
        f"架构配置已加载: 基准={'有' if baseline else '无'}, "
        f"运行时覆盖={'有' if runtime else '无'}"
    )

    return _LOADED_CONFIG


def reload_court_config() -> Dict[str, Any]:
    """强制重新加载配置（热更新）"""
    global _LOADED_CONFIG
    _LOADED_CONFIG = None
    return load_court_config()


def get_runtime_override_path() -> Path:
    """获取运行时覆盖文件路径"""
    return _RUNTIME_OVERRIDE_PATH


def save_runtime_override(data: Dict[str, Any]) -> bool:
    """
    保存运行时覆盖到藏书阁（持久化）。

    Args:
        data: 要保存的配置字典（会深度合并到已有文件）

    Returns:
        是否保存成功
    """
    try:
        import yaml

        # 确保目录存在
        _RUNTIME_OVERRIDE_PATH.parent.mkdir(parents=True, exist_ok=True)

        # 读取已有内容并深度合并
        existing = {}
        if _RUNTIME_OVERRIDE_PATH.exists():
            existing = _load_yaml(_RUNTIME_OVERRIDE_PATH)

        merged = _deep_merge(existing, data)

        with open(_RUNTIME_OVERRIDE_PATH, "w", encoding="utf-8") as f:
            yaml.dump(merged, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        # 清除缓存，下次访问时重新加载
        global _LOADED_CONFIG
        _LOADED_CONFIG = None

        logger.info(f"运行时覆盖已保存到藏书阁: {_RUNTIME_OVERRIDE_PATH}")
        return True
    except Exception as e:
        logger.error(f"运行时覆盖保存失败: {e}")
        return False


# ═══════════════════════════════════════════════════════════════
#  类型定义
# ═══════════════════════════════════════════════════════════════

class VoteResult(Enum):
    """投票结果"""
    APPROVED = "通过"
    REJECTED = "驳回"
    TIE = "平票（视为驳回）"
    IMPERIAL_EDICT = "圣旨直下"


class CommandStatus(Enum):
    """命令执行状态"""
    PENDING = "待投票"
    APPROVED = "已下发"
    IN_EXECUTION = "执行中"
    COMPLETED = "已完成"
    REPORTED = "已汇报皇帝"
    REJECTED = "被驳回"
    IMPERIAL_EDICT = "圣旨·绕过代表大会"
    URGENT_DISPATCHED = "紧急下发（待补审）"
    PENDING_RETROACTIVE = "待补审"


class MemberRole(Enum):
    """代表大会成员身份"""
    CHIEF = "首席代表"
    ECONOMY = "经济代表"
    SOCIOLOGY = "社会学代表"
    MANAGEMENT = "系统管理代表"
    DEBATE = "辩论质疑代表"
    SPECIALIST_A = "创新专员"
    WHITE_CLOTH = "白衣代表"
    # [v4.0.0 道家升级] 道家否决角色：可基于"过犹不及"原则行使否决权
    DAO_VETO = "道家否决代表"


# [v4.0.0 道家升级] 道家否决权配置
from dataclasses import dataclass, field


@dataclass
class DaoVetoConfig:
    """
    道家否决权配置——"过犹不及"的中道智慧。

    核心理念：当投票结果过于极端（全部赞成激进或全部赞成保守），
    说明决策缺乏阴阳平衡，道家代表有权行使否决并触发重审。

   否决触发条件（满足任一即触发）：
    1. 票数基尼系数 > threshold：赞成票/反对票严重不均
    2. 全票通过/全票反对：缺乏辩证声音
    3. 战略极端化标记：命令内容含"激进"/"保守"/"全力"/"收缩"等极端词
    """
    # 否决权启用标志
    enabled: bool = True

    # 触发条件
    gini_threshold: float = 0.7      # 票数分布基尼系数阈值（>0.7表示严重不均）
    unanimous_trigger: bool = True    # 全票通过/反对是否触发否决
    extreme_words_trigger: bool = True  # 包含极端化词语是否触发

    # 全票权重（触发否决时的重审票数）
    full_review_threshold: int = 7  # 7票全赞或全反对

    # 可行使否决权的学派成员
    # 道家代表（老子/庄子/范蠡/列子）自动具有否决权
    dao_veto_members: Tuple[str, ...] = ("老子", "庄子", "范蠡", "列子")

    # 极端化词语列表（触发否决检查）
    extreme_positive_words: Tuple[str, ...] = ("全力", "激进", "极致", "最大化", "全面扩张", "毕其功于一役")
    extreme_negative_words: Tuple[str, ...] = ("全力收缩", "保守", "完全放弃", "一刀切", "极端保守")

    # 阴阳重审策略
    yinyang_review_required: bool = True  # 否决后是否强制阴阳辩证重审

    # 道家谚语
    dao_proverb: str = "过犹不及，物极必反，阴阳平衡，方为正道。"


@dataclass
class VetoAssessment:
    """否决评估结果"""
    veto_triggered: bool
    trigger_reason: str
    gini_coefficient: float
    vote_distribution: Dict[str, int]  # {"approve": N, "reject": N}
    extreme_word_found: Optional[str] = None
    dao_veto_member: Optional[str] = None
    yinyang_review_triggered: bool = False
    yinyang_analysis: str = ""
    dao_guidance: str = ""
    final_recommendation: str = ""


@dataclass
class CongressMember:
    """代表大会成员"""
    name: str
    role: MemberRole
    other_position: str        # 其他部门任职描述
    is_white_cloth: bool       # 是否白衣（无任何任职）
    is_western: bool = False   # 是否西方贤者
    expert_tags: List[str] = field(default_factory=list)  # 能力标签
    vote_weight: int = 1       # 投票权重
    # [v4.0.0 道家升级] 道家否决权成员标记
    is_dao_veto_member: bool = field(default=False)  # 是否具有道家否决权


@dataclass
class Vote:
    """单次投票"""
    voter_name: str
    approved: bool              # True=赞成, False=反对
    reason: str = ""


# ═══════════════════════════════════════════════════════════════
#  代表大会核心引擎
# ═══════════════════════════════════════════════════════════════

class DecisionCongress:
    """
    七人决策代表大会 —— 最高权力执行层

    驾临所有系统之上（包括皇家藏书阁）。
    职责: 执行皇帝命令的下发、审核、完成、汇报。
    决策: 4票及以上通过（可配置）。

    v3.0.0: 成员和约束从动态配置加载，不再硬编码。
    """

    def __init__(self):
        self._command_history: List[Dict[str, Any]] = []
        self._next_cmd_id = 1
        self._cloning_cache: Dict[str, Any] = {}  # 成员Cloning缓存

        # ── 从动态配置加载 ──
        self._config = load_court_config()
        self.MEMBERS: List[CongressMember] = self._load_members()
        self.PASS_THRESHOLD: int = self._config.get("decision_congress", {}).get("pass_threshold", 4)
        self.MAJOR_THRESHOLD: int = self._config.get("decision_congress", {}).get("major_threshold", 5)

        # [v4.0.0 道家升级] 道家否决权配置
        self.dao_veto_config: DaoVetoConfig = DaoVetoConfig()

    def _load_members(self) -> List[CongressMember]:
        """从配置文件加载成员列表"""
        members_config = self._config.get("decision_congress", {}).get("members", [])

        if not members_config:
            logger.warning("配置文件中无成员数据，使用内置默认七人名单")
            return self._default_members()

        members = []
        for m in members_config:
            # 跳过 inactive 成员
            if not m.get("active", True):
                continue

            try:
                role = MemberRole[m.get("role", "WHITE_CLOTH")]
            except (ValueError, KeyError):
                logger.warning(f"未知角色 '{m.get('role')}' for member '{m.get('name')}'，跳过")
                continue

            # [v4.0.0 道家升级] 自动识别道家否决权成员
            is_dao_veto = m.get("name", "") in self.dao_veto_config.dao_veto_members
            members.append(CongressMember(
                name=m.get("name", ""),
                role=role,
                other_position=m.get("other_position", ""),
                is_white_cloth=m.get("is_white_cloth", False),
                is_western=m.get("is_western", False),
                expert_tags=m.get("expert_tags", []),
                vote_weight=m.get("vote_weight", 1),
                is_dao_veto_member=is_dao_veto,
            ))

        if len(members) == 0:
            logger.warning("加载后无有效成员，回退到默认名单")
            return self._default_members()

        logger.info(f"动态加载 {len(members)} 名代表大会成员（来自配置文件）")
        return members

    @staticmethod
    def _default_members() -> List[CongressMember]:
        """内置默认七人名单（仅当配置文件不可用时使用）"""
        return [
            CongressMember(name="孔子", role=MemberRole.CHIEF,
                           other_position="王爵·太师·皇家系统",
                           is_white_cloth=False, is_western=False,
                           expert_tags=["儒家", "教育", "伦理"]),
            CongressMember(name="管仲", role=MemberRole.ECONOMY,
                           other_position="伯爵·户部尚书",
                           is_white_cloth=False, is_western=False,
                           expert_tags=["经济学家", "宏观经济", "国家治理"]),
            CongressMember(name="韦伯（Max Weber）", role=MemberRole.SOCIOLOGY,
                           other_position="专员·礼部专员团队",
                           is_white_cloth=False, is_western=True,
                           expert_tags=["社会学家", "系统管理", "官僚制理论", "组织管理"]),
            CongressMember(name="德鲁克（Peter Drucker）", role=MemberRole.MANAGEMENT,
                           other_position="伯爵·工部",
                           is_white_cloth=False, is_western=True,
                           expert_tags=["系统管理", "现代管理学之父", "组织效能"]),
            CongressMember(name="孟子", role=MemberRole.DEBATE,
                           other_position="公爵·太傅·皇家系统",
                           is_white_cloth=False, is_western=False,
                           expert_tags=["辩论质疑", "性善论", "仁政", "辟杨墨"]),
            CongressMember(name="张衡", role=MemberRole.SPECIALIST_A,
                           other_position="专员·皇家科学院团队",
                           is_white_cloth=False, is_western=False,
                           expert_tags=["科技创新", "天文", "科学"]),
            # [v4.0.0 道家升级] 范蠡具有道家否决权
            CongressMember(name="范蠡", role=MemberRole.WHITE_CLOTH,
                           other_position="无任何任职",
                           is_white_cloth=True, is_western=False,
                           expert_tags=["商业智慧", "经济周期", "韬略"],
                           is_dao_veto_member=True),  # 范蠡：道家否决权
        ]

    # ── 动态配置 API ──

    def reload_config(self) -> None:
        """热重载配置（从 YAML + 藏书阁覆盖重新加载）"""
        self._config = reload_court_config()
        self.MEMBERS = self._load_members()
        self.PASS_THRESHOLD = self._config.get("decision_congress", {}).get("pass_threshold", 4)
        self.MAJOR_THRESHOLD = self._config.get("decision_congress", {}).get("major_threshold", 5)
        # 清除 Cloning 缓存（成员可能已变更）
        self._cloning_cache.clear()
        logger.info("代表大会配置已热重载")

    def update_member(self, name: str, **kwargs) -> Dict[str, Any]:
        """
        更新成员信息并持久化到藏书阁。

        Args:
            name: 成员名称
            **kwargs: 要更新的字段（role, other_position, is_white_cloth, is_western,
                      expert_tags, vote_weight, active）

        Returns:
            更新结果
        """
        member = None
        for m in self.MEMBERS:
            if m.name == name:
                member = m
                break

        if member is None:
            return {"error": f"成员 '{name}' 不在当前代表大会中"}

        # 更新内存中的对象
        if "role" in kwargs:
            try:
                member.role = MemberRole[kwargs["role"]]
            except (ValueError, KeyError):
                return {"error": f"未知角色 '{kwargs['role']}'"}
        if "other_position" in kwargs:
            member.other_position = kwargs["other_position"]
        if "is_white_cloth" in kwargs:
            member.is_white_cloth = kwargs["is_white_cloth"]
        if "is_western" in kwargs:
            member.is_western = kwargs["is_western"]
        if "expert_tags" in kwargs:
            member.expert_tags = kwargs["expert_tags"]
        if "vote_weight" in kwargs:
            member.vote_weight = kwargs["vote_weight"]
        if "active" in kwargs:
            member.active = kwargs.get("active", True)

        # 序列化当前成员列表并持久化到藏书阁
        members_data = []
        for m in self._default_members():
            # 以默认列表为基底
            member_dict = {
                "name": m.name,
                "role": m.role.value,
                "other_position": m.other_position,
                "is_white_cloth": m.is_white_cloth,
                "is_western": m.is_western,
                "expert_tags": m.expert_tags,
                "vote_weight": m.vote_weight,
                "active": True,
            }
            # 覆盖为当前内存中的值
            for cur in self.MEMBERS:
                if cur.name == m.name:
                    member_dict = {
                        "name": cur.name,
                        "role": cur.role.value,
                        "other_position": cur.other_position,
                        "is_white_cloth": cur.is_white_cloth,
                        "is_western": cur.is_western,
                        "expert_tags": cur.expert_tags,
                        "vote_weight": cur.vote_weight,
                        "active": True,
                    }
                    break
            members_data.append(member_dict)

        # 写入运行时覆盖文件
        saved = save_runtime_override({
            "decision_congress": {"members": members_data}
        })

        logger.info(f"成员 '{name}' 已更新并{'持久化' if saved else '尝试持久化'}到藏书阁")

        return {
            "success": True,
            "member_name": name,
            "updated_fields": list(kwargs.keys()),
            "persisted": saved,
        }

    def add_member(self, name: str, role: str, other_position: str,
                   is_white_cloth: bool = False, is_western: bool = False,
                   expert_tags: List[str] = None, vote_weight: int = 1) -> Dict[str, Any]:
        """
        新增成员并持久化到藏书阁。

        Args:
            name: 成员名称
            role: 角色枚举值
            other_position: 其他部门任职
            is_white_cloth: 是否白衣
            is_western: 是否西方贤者
            expert_tags: 能力标签
            vote_weight: 投票权重

        Returns:
            添加结果
        """
        try:
            member_role = MemberRole[role]
        except (ValueError, KeyError):
            return {"error": f"未知角色 '{role}'"}

        # 检查重名
        for m in self.MEMBERS:
            if m.name == name:
                return {"error": f"成员 '{name}' 已存在"}

        new_member = CongressMember(
            name=name,
            role=member_role,
            other_position=other_position,
            is_white_cloth=is_white_cloth,
            is_western=is_western,
            expert_tags=expert_tags or [],
            vote_weight=vote_weight,
        )

        self.MEMBERS.append(new_member)

        # 持久化
        members_data = [{
            "name": m.name,
            "role": m.role.value,
            "other_position": m.other_position,
            "is_white_cloth": m.is_white_cloth,
            "is_western": m.is_western,
            "expert_tags": m.expert_tags,
            "vote_weight": m.vote_weight,
            "active": True,
        } for m in self.MEMBERS]

        saved = save_runtime_override({
            "decision_congress": {"members": members_data}
        })

        logger.info(f"新成员 '{name}' 已加入代表大会（共{len(self.MEMBERS)}人），持久化={'成功' if saved else '失败'}")

        return {
            "success": True,
            "member_name": name,
            "total_members": len(self.MEMBERS),
            "persisted": saved,
        }

    def remove_member(self, name: str) -> Dict[str, Any]:
        """
        移除成员并持久化到藏书阁。

        Args:
            name: 成员名称

        Returns:
            移除结果
        """
        original_len = len(self.MEMBERS)
        self.MEMBERS = [m for m in self.MEMBERS if m.name != name]

        if len(self.MEMBERS) == original_len:
            return {"error": f"成员 '{name}' 不在当前代表大会中"}

        # 清除该成员的 Cloning 缓存
        self._cloning_cache.pop(name, None)

        # 持久化
        members_data = [{
            "name": m.name,
            "role": m.role.value,
            "other_position": m.other_position,
            "is_white_cloth": m.is_white_cloth,
            "is_western": m.is_western,
            "expert_tags": m.expert_tags,
            "vote_weight": m.vote_weight,
            "active": True,
        } for m in self.MEMBERS]

        saved = save_runtime_override({
            "decision_congress": {"members": members_data}
        })

        logger.info(f"成员 '{name}' 已移出代表大会（剩余{len(self.MEMBERS)}人），持久化={'成功' if saved else '失败'}")

        return {
            "success": True,
            "member_name": name,
            "remaining_members": len(self.MEMBERS),
            "persisted": saved,
        }

    # ── 命令下发与投票 ──

    def submit_imperial_command(
        self,
        command: str,
        target_department: str = "",
        command_type: str = "regular",
        context: str = "",
    ) -> Dict[str, Any]:
        """
        接收皇帝（用户）命令，发起代表大会投票。

        Args:
            command: 皇帝命令内容
            target_department: 目标执行部门
            command_type: "regular"(常规) / "major"(重大) / "urgent"(紧急) / "imperial_edict"(圣旨)
            context: 命令上下文

        Returns:
            投票结果字典
        """
        cmd_id = f"CMD_{self._next_cmd_id:04d}"
        self._next_cmd_id += 1

        # ── 圣旨绕过 ──
        if command_type == "imperial_edict":
            record = {
                "cmd_id": cmd_id,
                "command": command,
                "target_department": target_department,
                "command_type": "imperial_edict",
                "status": CommandStatus.IMPERIAL_EDICT.value,
                "result": VoteResult.IMPERIAL_EDICT.value,
                "votes": [],
                "approve_count": 0,
                "reject_count": 0,
                "threshold": 0,
                "submitted_at": time.time(),
                "imperial_edict": True,
            }
            self._command_history.append(record)
            logger.info(f"[圣旨·绕过代表大会] {cmd_id}: {command[:50]}...")
            return record

        # ── 紧急决策：先执行后补审 ──
        if command_type == "urgent":
            record = {
                "cmd_id": cmd_id,
                "command": command,
                "target_department": target_department,
                "command_type": "urgent",
                "status": CommandStatus.URGENT_DISPATCHED.value,
                "result": "紧急下发（待补审）",
                "votes": [],
                "approve_count": 0,
                "reject_count": 0,
                "threshold": self.PASS_THRESHOLD,
                "submitted_at": time.time(),
                "urgent": True,
                "pending_retroactive": True,
            }
            self._command_history.append(record)
            logger.info(f"[紧急下发·待补审] {cmd_id}: {command[:50]}...")
            return record

        threshold = self.MAJOR_THRESHOLD if command_type == "major" else self.PASS_THRESHOLD

        # 自动投票（基于成员角色和命令内容）
        votes = self._auto_vote(command, target_department, command_type, context)

        approve_count = sum(1 for v in votes if v.approved)
        reject_count = sum(1 for v in votes if not v.approved)

        if approve_count >= threshold:
            result = VoteResult.APPROVED
        else:
            result = VoteResult.REJECTED

        # [v4.0.0 道家升级] 否决权检查——"过犹不及"
        veto_assessment: Optional[VetoAssessment] = None
        if self.dao_veto_config.enabled:
            veto_assessment = self._dao_veto_check(
                votes, command, approve_count, reject_count, threshold, result
            )
            if veto_assessment.veto_triggered:
                logger.info(
                    f"[道家否决] {veto_assessment.trigger_reason} | "
                    f"基尼={veto_assessment.gini_coefficient:.2f} | "
                    f"{veto_assessment.dao_guidance}"
                )
                # 将否决信息写入记录
                result = VoteResult.REJECTED
                veto_assessment.final_recommendation = (
                    "【道家否决】票数过于极端，触发阴阳辩证重审。"
                    f"{veto_assessment.yinyang_analysis}"
                )

        record = {
            "cmd_id": cmd_id,
            "command": command,
            "target_department": target_department,
            "command_type": command_type,
            "status": CommandStatus.APPROVED.value if result == VoteResult.APPROVED else CommandStatus.REJECTED.value,
            "result": result.value,
            "votes": [{"voter": v.voter_name, "approved": v.approved, "reason": v.reason} for v in votes],
            "approve_count": approve_count,
            "reject_count": reject_count,
            "threshold": threshold,
            "submitted_at": time.time(),
            "hanlin_exempt": True,  # v2.0: 代表大会决策不受翰林院审核
            # [v4.0.0 道家升级] 否决权信息
            "dao_veto": {
                "enabled": self.dao_veto_config.enabled,
                "triggered": veto_assessment.veto_triggered if veto_assessment else False,
                "reason": veto_assessment.trigger_reason if veto_assessment else "",
                "dao_guidance": veto_assessment.dao_guidance if veto_assessment else "",
            } if self.dao_veto_config.enabled else {},
        }

        self._command_history.append(record)

        logger.info(
            f"代表大会[{cmd_id}]: {result.value} ({approve_count}/{len(self.MEMBERS)}票) "
            f"命令: {command[:50]}..."
        )

        # ── 驳回自动汇报皇帝 ──
        if result == VoteResult.REJECTED:
            rejection_report = self._generate_rejection_report(record)
            record["rejection_report"] = rejection_report
            record["auto_reported_to_emperor"] = True
            logger.info(f"代表大会[{cmd_id}]: 驳回，反对理由已自动汇报皇帝")

        return record

    def _get_cloning_for_member(self, member_name: str) -> Optional[Any]:
        """
        获取成员的Cloning实例（懒加载）。

        通过贤者代理工厂获取，失败则返回None。
        """
        if member_name in self._cloning_cache:
            return self._cloning_cache[member_name]

        try:
            from src.intelligence.engines.cloning._sage_proxy_factory import get_sage_cloning
            cloning = get_sage_cloning(member_name)
            if cloning is not None:
                self._cloning_cache[member_name] = cloning
            return cloning
        except Exception as e:
            logger.debug(f"Cloning获取失败 [{member_name}]: {e}")
            return None

    def _cloning_vote(
        self, member: CongressMember, command: str, target: str, context: str
    ) -> Tuple[bool, str]:
        """
        调用成员的Cloning能力进行独立投票评估。

        Args:
            member: 代表大会成员
            command: 命令内容
            target: 目标部门
            context: 上下文

        Returns:
            (approved, reason) 投票结果和理由
        """
        cloning = self._get_cloning_for_member(member.name)
        if cloning is None:
            return None, ""  # Cloning不可用，回退到规则引擎

        try:
            # 构建评估提示
            prompt = (
                f"你是{member.name}（{member.role.value}），正在七人决策代表大会上投票。\n"
                f"皇帝命令: {command}\n"
                f"目标部门: {target}\n"
                f"上下文: {context}\n\n"
                f"请以{member.name}的智慧视角评估此命令，给出你的投票决定（赞成/反对）和理由。\n"
                f"只输出JSON格式: {{\"approved\": true/false, \"reason\": \"理由\"}}"
            )

            # 调用Cloning的consult或evaluate方法
            if hasattr(cloning, 'consult'):
                response = cloning.consult(prompt, max_tokens=200)
            elif hasattr(cloning, 'evaluate'):
                response = cloning.evaluate(command, context=context)
            elif hasattr(cloning, 'query'):
                response = cloning.query(prompt)
            else:
                return None, ""

            # 解析响应
            if isinstance(response, dict):
                approved = response.get("approved", True)
                reason = response.get("reason", "")
            elif isinstance(response, str):
                # 尝试从文本中提取
                approved = "反对" not in response and "驳回" not in response
                reason = response[:200] if response else "基于Cloning评估"
            else:
                return None, ""

            return bool(approved), str(reason)[:200]
        except Exception as e:
            logger.debug(f"Cloning投票失败 [{member.name}]: {e}")
            return None, ""

    def _auto_vote(
        self,
        command: str,
        target_department: str,
        command_type: str,
        context: str,
    ) -> List[Vote]:
        """
        自动投票（基于成员Cloning能力 + 规则引擎回退）。

        优先使用各成员的Cloning能力进行独立评估；
        若Cloning不可用，回退到基于规则的概率引擎。
        """
        votes = []

        for member in self.MEMBERS:
            # 尝试Cloning投票
            cloning_approved, cloning_reason = self._cloning_vote(
                member, command, target_department, context
            )

            if cloning_approved is not None:
                # Cloning成功
                votes.append(Vote(
                    voter_name=member.name,
                    approved=cloning_approved,
                    reason=cloning_reason or f"基于{member.name}智慧独立评估",
                ))
                continue

            # ── 规则引擎回退 ──
            base_approval = 0.85 if command_type == "regular" else 0.7

            negative_keywords = ["删除", "清空", "销毁", "覆盖全部", "重置"]
            positive_keywords = ["优化", "升级", "新增", "修复", "验证", "改进"]

            negative_score = sum(0.15 for kw in negative_keywords if kw in command)
            positive_score = sum(0.05 for kw in positive_keywords if kw in command)

            approval_prob = max(0.3, min(1.0, base_approval - negative_score + positive_score))

            if member.is_white_cloth:
                prob = approval_prob - 0.1
            elif member.role == MemberRole.CHIEF:
                prob = approval_prob + 0.05
            else:
                prob = approval_prob

            if target_department and target_department in member.other_position:
                prob += 0.1

            approved = prob >= 0.5
            reason = self._generate_vote_reason(member, approved, command, target_department)

            votes.append(Vote(
                voter_name=member.name,
                approved=approved,
                reason=reason,
            ))

        return votes

    def _generate_vote_reason(
        self, member: CongressMember, approved: bool, command: str, target: str
    ) -> str:
        """生成投票理由"""
        if approved:
            reasons = [
                f"命令方向正确，有利于系统发展",
                f"执行路径清晰，建议下发{target}",
                f"符合当前战略优先级",
                f"风险可控，支持执行",
            ]
        else:
            reasons = [
                "命令可能带来不可逆影响，建议进一步论证",
                "当前时机不成熟，建议暂缓",
                "执行成本过高，性价比不足",
                "缺乏充分论证，建议补充方案细节",
            ]
        return reasons[hash(member.name) % len(reasons)]

    # ── v4.0.0: 道家否决权 ──────────────────────────────────────────────

    def _dao_veto_check(
        self,
        votes: List[Vote],
        command: str,
        approve_count: int,
        reject_count: int,
        threshold: int,
        current_result: VoteResult,
    ) -> VetoAssessment:
        """
        [道家否决核心] 检查是否应行使否决权——"过犹不及"。

        否决触发条件（满足任一即触发）：
        1. 票数基尼系数 > 0.7：赞成票/反对票严重不均
        2. 全票通过/全票反对：缺乏辩证声音
        3. 命令包含极端化词语

        [道家解读] "过犹不及"——票数太集中反而是危险的信号。
        真正好的决策应该既有赞成也有反对，体现阴阳平衡。
        """
        total = len(votes)
        if total == 0:
            return VetoAssessment(
                veto_triggered=False,
                trigger_reason="无投票数据",
                gini_coefficient=0.0,
                vote_distribution={"approve": 0, "reject": 0},
                dao_guidance="无投票，无法评估。",
            )

        approve_n = approve_count
        reject_n = reject_count
        vote_distribution = {"approve": approve_n, "reject": reject_n}

        # 条件1：计算基尼系数
        sorted_votes = sorted([approve_n, reject_n])
        n = 2
        mean = sum(sorted_votes) / n
        if mean == 0:
            gini = 0.0
        else:
            gini = (2 * sum((i + 1) * v for i, v in enumerate(sorted_votes))) / (n * sum(sorted_votes)) - (n + 1) / n
        gini = max(0.0, min(1.0, gini))

        # 条件2：全票检查
        is_unanimous = (approve_n == total) or (reject_n == total)

        # 条件3：极端化词语检查
        extreme_word: Optional[str] = None
        for word in self.dao_veto_config.extreme_positive_words + self.dao_veto_config.extreme_negative_words:
            if word in command:
                extreme_word = word
                break

        # 判断是否触发否决
        trigger_reasons: List[str] = []
        if gini > self.dao_veto_config.gini_threshold:
            direction = "激进" if approve_n > reject_n else "保守"
            trigger_reasons.append(f"基尼系数{gini:.2f}>{self.dao_veto_config.gini_threshold}（票数严重{direction}）")
        if self.dao_veto_config.unanimous_trigger and is_unanimous:
            direction = "全票赞成（阳盛）" if approve_n == total else "全票反对（阴盛）"
            trigger_reasons.append(f"{direction}（缺乏辩证声音）")
        if self.dao_veto_config.extreme_words_trigger and extreme_word:
            trigger_reasons.append(f"命令含极端化词语：'{extreme_word}'")

        veto_triggered = len(trigger_reasons) > 0

        if not veto_triggered:
            return VetoAssessment(
                veto_triggered=False,
                trigger_reason="投票分布正常，无需否决",
                gini_coefficient=gini,
                vote_distribution=vote_distribution,
                dao_guidance="阴阳平衡，决策正常推进。",
            )

        # 生成阴阳分析
        yinyang_analysis = self._generate_yinyang_analysis(
            approve_n, reject_n, total, is_unanimous, extreme_word
        )

        # 生成道家指引
        dao_guidance = self._generate_dao_guidance(approve_n, reject_n, total, trigger_reasons)

        return VetoAssessment(
            veto_triggered=True,
            trigger_reason="; ".join(trigger_reasons),
            gini_coefficient=gini,
            vote_distribution=vote_distribution,
            extreme_word_found=extreme_word,
            yinyang_review_triggered=True,
            yinyang_analysis=yinyang_analysis,
            dao_guidance=dao_guidance,
            final_recommendation=(
                f"【道家否决】{'; '.join(trigger_reasons)}。"
                f"建议重新审视决策，从对立方向重新思考。"
            ),
        )

    def _generate_yinyang_analysis(
        self, approve_n: int, reject_n: int, total: int,
        is_unanimous: bool, extreme_word: Optional[str]
    ) -> str:
        """生成阴阳辩证分析"""
        approve_ratio = approve_n / total if total > 0 else 0.0
        reject_ratio = reject_n / total if total > 0 else 0.0

        # 阴阳强度评估
        yang_score = approve_ratio
        yin_score = reject_ratio

        analysis_parts = []
        analysis_parts.append(f"投票阴阳分析：阳（赞成）={yang_score:.0%}，阴（反对）={yin_score:.0%}。")

        if yang_score > 0.8:
            analysis_parts.append("【阳亢】阳气过盛，决策偏向激进行动主义。")
        elif yin_score > 0.8:
            analysis_parts.append("【阴盛】阴气过盛，决策偏向消极保守主义。")
        elif 0.3 <= yang_score <= 0.7:
            analysis_parts.append("【阴阳平衡】决策较为中道，既有推动力又有制动力量。")

        if is_unanimous:
            analysis_parts.append("【一阴一阳之谓道】全票通过/反对，缺乏内部张力，需要外部质疑力量。")

        if extreme_word:
            analysis_parts.append(f"【过犹不及】命令中含'{extreme_word}'，提示决策者关注极端化倾向。")

        return " ".join(analysis_parts)

    def _generate_dao_guidance(
        self, approve_n: int, reject_n: int, total: int, trigger_reasons: List[str]
    ) -> str:
        """生成道家智慧指引"""
        approve_ratio = approve_n / total if total > 0 else 0.0

        if approve_ratio > 0.8:
            return (
                "【上善若水·谦下】票数过于集中于行动方。"
                "建议：增加反对声音的权重，引入更多辩证视角，"
                "如水往低处流，决策也应包容不同意见。"
            )
        elif approve_ratio < 0.2:
            return (
                "【致虚极守静笃】票数过于集中于反对方。"
                "建议：重新审视反对理由，是否存在过度保守倾向。"
                "无为不是不作为，而是在适当的时机采取适当的行动。"
            )
        else:
            return (
                "【阴阳平衡】决策虽未全票通过，但分布存在偏重。"
                "建议：深入分析分歧原因，确保最终决策考虑了多方视角。"
            )

    def get_dao_veto_status(self) -> Dict[str, Any]:
        """
        获取道家否决权状态报告。

        [道家解读] 定期审视否决权系统的运作状态，
        不是为了改变什么，而是清楚自己正在哪里。
        """
        dao_members = [m for m in self.MEMBERS if m.is_dao_veto_member]
        veto_enabled = self.dao_veto_config.enabled

        return {
            "veto_enabled": veto_enabled,
            "dao_veto_members": [m.name for m in dao_members],
            "config": {
                "gini_threshold": self.dao_veto_config.gini_threshold,
                "unanimous_trigger": self.dao_veto_config.unanimous_trigger,
                "extreme_words_trigger": self.dao_veto_config.extreme_words_trigger,
                "yinyang_review_required": self.dao_veto_config.yinyang_review_required,
            },
            "dao_proverb": self.dao_veto_config.dao_proverb,
            "status": "已启用" if veto_enabled else "已停用",
        }

    # ── 驳回自动汇报 ──

    def _generate_rejection_report(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成驳回报告（自动汇报皇帝）。

        汇总所有反对理由，生成皇帝可读的摘要。
        """
        reject_votes = [v for v in record["votes"] if not v["approved"]]
        approve_votes = [v for v in record["votes"] if v["approved"]]

        reasons_summary = "\n".join(
            f"  - {v['voter']}: {v['reason']}"
            for v in reject_votes
        )

        report = {
            "cmd_id": record["cmd_id"],
            "command": record["command"],
            "verdict": "驳回",
            "vote_summary": f"{record['approve_count']}赞成/{record['reject_count']}反对",
            "reject_reasons": reasons_summary,
            "reject_voters": [v["voter"] for v in reject_votes],
            "approve_voters": [v["voter"] for v in approve_votes],
            "generated_at": time.time(),
        }
        return report

    # ── 紧急决策补审 ──

    def retroactive_review(
        self, cmd_id: str, execution_result: str = "", success: bool = True
    ) -> Dict[str, Any]:
        """
        紧急决策执行后的追溯性投票审核。

        紧急命令先执行后补审：执行完毕后回溯进行代表大会投票。
        补审结果不影响已执行的操作，但记录为历史参考。

        Args:
            cmd_id: 紧急命令ID
            execution_result: 执行结果摘要
            success: 执行是否成功

        Returns:
            补审结果字典
        """
        for record in self._command_history:
            if record["cmd_id"] == cmd_id and record.get("urgent"):
                # 发起追溯性投票
                votes = self._auto_vote(
                    record["command"], record["target_department"],
                    "regular", f"[补审] 执行结果: {execution_result}"
                )
                approve_count = sum(1 for v in votes if v.approved)
                reject_count = sum(1 for v in votes if not v.approved)

                retroactive_result = "补审通过" if approve_count >= self.PASS_THRESHOLD else "补审未通过"

                record["retroactive_review"] = {
                    "votes": [{"voter": v.voter_name, "approved": v.approved, "reason": v.reason} for v in votes],
                    "approve_count": approve_count,
                    "reject_count": reject_count,
                    "result": retroactive_result,
                    "execution_success": success,
                    "execution_result": execution_result,
                    "reviewed_at": time.time(),
                }
                record["status"] = CommandStatus.COMPLETED.value if success else CommandStatus.REJECTED.value
                record["pending_retroactive"] = False

                logger.info(f"紧急补审[{cmd_id}]: {retroactive_result} ({approve_count}/{len(votes)}票)")
                return record["retroactive_review"]

        return {"error": f"命令 {cmd_id} 不存在或不是紧急决策"}

    # ── 全局执行情况聚合报告 ──

    def generate_global_report(self) -> Dict[str, Any]:
        """
        生成全局执行情况聚合报告（月度/按需汇报皇帝）。

        统计所有命令的状态分布、通过率、各部门执行情况等。

        Returns:
            全局报告字典
        """
        total = len(self._command_history)
        if total == 0:
            return {
                "report_title": "七人决策代表大会·全局执行报告",
                "total_commands": 0,
                "summary": "暂无命令记录",
            }

        # 按状态统计
        status_counts: Dict[str, int] = {}
        for record in self._command_history:
            status = record.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        # 按类型统计
        type_counts: Dict[str, int] = {}
        for record in self._command_history:
            ct = record.get("command_type", "regular")
            type_counts[ct] = type_counts.get(ct, 0) + 1

        # 通过率
        approved = sum(1 for r in self._command_history if r["result"] == VoteResult.APPROVED.value)
        rejected = sum(1 for r in self._command_history if r["result"] == VoteResult.REJECTED.value)
        imperial_edicts = sum(1 for r in self._command_history if r.get("imperial_edict"))
        urgents = sum(1 for r in self._command_history if r.get("urgent"))

        # 待处理项
        pending = sum(1 for r in self._command_history if r.get("status") in (
            CommandStatus.PENDING.value, CommandStatus.IN_EXECUTION.value,
            CommandStatus.URGENT_DISPATCHED.value, CommandStatus.PENDING_RETROACTIVE.value,
        ))

        # 待补审项
        pending_retroactive = sum(1 for r in self._command_history if r.get("pending_retroactive"))

        # 驳回报告（最近5条）
        rejection_reports = [
            r.get("rejection_report", {})
            for r in self._command_history
            if r["result"] == VoteResult.REJECTED.value and r.get("rejection_report")
        ][-5:]

        # 各部门命令分布
        dept_counts: Dict[str, int] = {}
        for record in self._command_history:
            dept = record.get("target_department", "未指定")
            dept_counts[dept] = dept_counts.get(dept, 0) + 1

        report = {
            "report_title": "七人决策代表大会·全局执行报告",
            "generated_at": time.time(),
            "summary": (
                f"共 {total} 条命令：通过 {approved}，驳回 {rejected}，"
                f"圣旨 {imperial_edicts}，紧急 {urgents}，待处理 {pending}"
            ),
            "total_commands": total,
            "statistics": {
                "approved": approved,
                "rejected": rejected,
                "imperial_edicts": imperial_edicts,
                "urgent": urgents,
                "pending": pending,
                "pending_retroactive": pending_retroactive,
                "approval_rate": approved / (approved + rejected) if (approved + rejected) > 0 else 0,
            },
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "department_distribution": dept_counts,
            "recent_rejections": rejection_reports,
            "member_count": len(self.MEMBERS),
            "pass_threshold": self.PASS_THRESHOLD,
        }

        logger.info(f"全局执行报告: {report['summary']}")
        return report

    # ── 执行确认与汇报 ──

    def confirm_execution(
        self, cmd_id: str, execution_result: str, success: bool = True
    ) -> Dict[str, Any]:
        """确认命令执行完成"""
        for record in self._command_history:
            if record["cmd_id"] == cmd_id:
                record["status"] = CommandStatus.COMPLETED.value if success else CommandStatus.REJECTED.value
                record["execution_result"] = execution_result
                record["completed_at"] = time.time()
                return record
        return {"error": f"命令 {cmd_id} 不存在"}

    def report_to_emperor(self, cmd_id: str) -> Dict[str, Any]:
        """向皇帝汇报执行结果"""
        for record in self._command_history:
            if record["cmd_id"] == cmd_id:
                record["status"] = CommandStatus.REPORTED.value
                record["reported_at"] = time.time()
                return {
                    "cmd_id": cmd_id,
                    "command": record["command"],
                    "status": "已汇报皇帝",
                    "result": record["result"],
                    "execution_result": record.get("execution_result", ""),
                    "votes_summary": f"{record['approve_count']}赞成/{record['reject_count']}反对",
                }
        return {"error": f"命令 {cmd_id} 不存在"}

    # ── 查询 ──

    def get_members(self) -> List[Dict[str, Any]]:
        """获取代表大会成员信息"""
        return [
            {
                "name": m.name,
                "role": m.role.value,
                "other_position": m.other_position,
                "is_white_cloth": m.is_white_cloth,
                "is_western": m.is_western,
                "expert_tags": m.expert_tags,
            }
            for m in self.MEMBERS
        ]

    def validate_constraints(self) -> Dict[str, Any]:
        """
        验证成员组合是否满足全部约束条件。

        约束规则从 court_config.yaml 的 decision_congress.constraints 读取，
        不再硬编码。支持动态增减约束。

        Returns:
            验证结果字典
        """
        members = self.MEMBERS
        constraints_config = self._config.get("decision_congress", {}).get("constraints", {})

        # ── 内置约束检查逻辑（基于 check 描述匹配） ──
        # 如果 YAML 中有 constraints 配置，使用它；否则用内置默认检查
        checks: Dict[str, bool] = {}
        details: Dict[str, List[str]] = {}

        if constraints_config:
            # 从配置文件读取约束规则
            for key, rule in constraints_config.items():
                label = rule.get("label", key)
                min_count = rule.get("min", 0)
                max_count = rule.get("max")  # 可选上限
                check = rule.get("check", "")

                matched = self._evaluate_constraint_check(members, check)
                count = len(matched)

                passed = count >= min_count
                if max_count is not None:
                    passed = passed and count <= max_count

                checks[label] = passed
                details[label] = [m.name for m in matched]
        else:
            # 回退：内置默认约束检查（向后兼容）
            checks, details = self._default_constraint_checks(members)

        all_pass = all(checks.values())

        return {
            "all_constraints_satisfied": all_pass,
            "checks": checks,
            "details": details,
        }

    @staticmethod
    def _evaluate_constraint_check(members: List[CongressMember], check: str) -> List[CongressMember]:
        """
        根据约束规则描述评估成员匹配。

        支持的 check 模式:
        - "not is_white_cloth" → 非白衣成员
        - "is_white_cloth" → 白衣成员
        - "is_western" → 西方贤者
        - "contains 其他职位 '专员'" → other_position 包含 '专员'
        - "expert_tags contains '社会学家'" → expert_tags 包含指定值
        - "expert_tags contains '系统管理' or '组织管理'" → expert_tags 包含任一值
        - "other_position contains '王爵'" → other_position 包含指定值
        """
        if "not is_white_cloth" in check:
            return [m for m in members if not m.is_white_cloth]
        elif "is_white_cloth" in check:
            return [m for m in members if m.is_white_cloth]
        elif "is_western" in check:
            return [m for m in members if m.is_western]
        elif "expert_tags contains" in check:
            # 支持 or 语法
            if " or " in check:
                # 提取引号内的标签名（支持子串匹配）
                tags = re.findall(r"'([^']+)'", check)
                return [m for m in members if any(any(t in et for et in m.expert_tags) for t in tags)]
            else:
                match = re.search(r"'([^']+)'", check)
                if match:
                    tag = match.group(1)
                    return [m for m in members if any(tag in et for et in m.expert_tags)]
        elif "other_position contains" in check:
            match = re.search(r"'([^']+)'", check)
            if match:
                keyword = match.group(1)
                return [m for m in members if keyword in m.other_position]
        elif "其他职位" in check and "专员" in check:
            return [m for m in members if "专员" in m.other_position]

        return []

    @staticmethod
    def _default_constraint_checks(members: List[CongressMember]) -> Tuple[Dict[str, bool], Dict[str, List[str]]]:
        """内置默认约束检查（向后兼容，仅当 YAML 无 constraints 时使用）"""
        department_holders = [m for m in members if not m.is_white_cloth]
        specialists = [m for m in members if "专员" in m.other_position]
        white_cloths = [m for m in members if m.is_white_cloth]
        westerners = [m for m in members if m.is_western]
        sociologists = [m for m in members if "社会学家" in m.expert_tags]
        economists = [m for m in members if "经济学家" in m.expert_tags]
        system_managers = [m for m in members if "系统管理" in m.expert_tags or "组织管理" in m.expert_tags]
        debaters = [m for m in members if any("辩论" in tag or "质疑" in tag for tag in m.expert_tags)]
        wangjue = [m for m in members if "王爵" in m.other_position]
        gongjue = [m for m in members if "公爵" in m.other_position]
        bojue = [m for m in members if "伯爵" in m.other_position]

        checks = {
            "部门任职≥4": len(department_holders) >= 4,
            "专员≥2": len(specialists) >= 2,
            "白衣=1": len(white_cloths) == 1,
            "西方≥1": len(westerners) >= 1,
            "社会学家≥1": len(sociologists) >= 1,
            "经济学家≥1": len(economists) >= 1,
            "系统管理≥1": len(system_managers) >= 1,
            "辩论质疑≥1": len(debaters) >= 1,
            "王爵≥1": len(wangjue) >= 1,
            "公爵≥1": len(gongjue) >= 1,
            "伯爵≥1": len(bojue) >= 1,
        }
        details = {
            "部门任职": [m.name for m in department_holders],
            "专员": [m.name for m in specialists],
            "白衣": [m.name for m in white_cloths],
            "西方": [m.name for m in westerners],
            "社会学家": [m.name for m in sociologists],
            "经济学家": [m.name for m in economists],
            "系统管理": [m.name for m in system_managers],
            "辩论质疑": [m.name for m in debaters],
            "王爵": [m.name for m in wangjue],
            "公爵": [m.name for m in gongjue],
            "伯爵": [m.name for m in bojue],
        }
        return checks, details

    def get_command_history(
        self, limit: int = 20, status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """获取命令历史"""
        results = self._command_history
        if status:
            results = [r for r in results if r.get("status") == status]
        return list(reversed(results[-limit:]))

    def get_stats(self) -> Dict[str, Any]:
        """获取代表大会统计"""
        total = len(self._command_history)
        approved = sum(1 for r in self._command_history if r["result"] == VoteResult.APPROVED.value)
        rejected = total - approved

        return {
            "total_commands": total,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": approved / total if total > 0 else 0,
            "pass_threshold": self.PASS_THRESHOLD,
            "member_count": len(self.MEMBERS),
            "white_cloth_member": next(
                (m.name for m in self.MEMBERS if m.is_white_cloth), None
            ),
        }

    # ── 任免权系统 ──

    @staticmethod
    def determine_appointment_authority(
        target_pin: int,
        target_has_nobility: bool,
    ) -> str:
        """
        判断任免权归属。

        任免规则:
        - 七人决策代表大会: 任免正三品及以上品级、持有爵位者
        - 上级对下级: 任免正三品以下品级且无爵位者

        Args:
            target_pin: 目标品级（数值越小品级越高）
            target_has_nobility: 目标是否持有爵位

        Returns:
            "congress" (代表大会任免) / "superior" (上级任免) / "both" (均可行)
        """
        # 正三品及以上（pin <= 3）→ 代表大会任免
        if target_pin <= 3:
            return "congress"
        # 持有爵位 → 代表大会任免
        if target_has_nobility:
            return "congress"
        # 正三品以下且无爵位 → 上级对下级任免
        return "superior"

    def congress_appoint(
        self,
        target_name: str,
        target_position: str,
        target_pin: int,
        target_has_nobility: bool,
        action: str = "appoint",  # "appoint" 任命 / "dismiss" 免职
        reason: str = "",
    ) -> Dict[str, Any]:
        """
        七人决策代表大会行使任免权。

        仅适用于正三品及以上品级、或持有爵位者。
        需通过投票决策（4票通过）。

        Args:
            target_name: 目标贤者名称
            target_position: 目标岗位名称
            target_pin: 目标品级
            target_has_nobility: 目标是否持有爵位
            action: "appoint"(任命) / "dismiss"(免职)
            reason: 任免理由

        Returns:
            投票+任免结果
        """
        authority = self.determine_appointment_authority(target_pin, target_has_nobility)

        if authority != "congress":
            return {
                "error": f"此岗位不属于代表大会任免范围（{target_position}，品级={target_pin}，爵位={target_has_nobility}）",
                "suggestion": "正三品以下且无爵位的岗位由上级对下级任免",
                "authority": authority,
            }

        # 发起任免投票
        action_text = "任命" if action == "appoint" else "免职"
        command = f"代表大会{action_text}：{target_name} - {target_position}"

        vote_result = self.submit_imperial_command(
            command=command,
            target_department="全局",
            command_type="major",  # 任免属重大决策，需5票通过
            context=f"{action_text}理由: {reason}" if reason else "",
        )

        vote_result["appointment"] = {
            "target_name": target_name,
            "target_position": target_position,
            "action": action_text,
            "authority": "七人决策代表大会",
            "pin": target_pin,
            "has_nobility": target_has_nobility,
        }

        return vote_result

    def superior_appoint(
        self,
        superior_name: str,
        superior_position: str,
        target_name: str,
        target_position: str,
        target_pin: int,
        target_has_nobility: bool,
        action: str = "appoint",
        reason: str = "",
    ) -> Dict[str, Any]:
        """
        上级对下级行使任免权。

        仅适用于正三品以下品级且无爵位者。
        无需投票，由上级直接决定。

        Args:
            superior_name: 上级名称
            superior_position: 上级岗位
            target_name: 目标名称
            target_position: 目标岗位
            target_pin: 目标品级
            target_has_nobility: 目标是否持有爵位
            action: "appoint" / "dismiss"
            reason: 理由

        Returns:
            任免结果
        """
        authority = self.determine_appointment_authority(target_pin, target_has_nobility)

        if authority == "congress":
            return {
                "error": f"此岗位需经代表大会任免（{target_position}，品级={target_pin}，或持有爵位）",
                "suggestion": "请使用 congress_appoint() 发起代表大会投票",
                "authority": authority,
            }

        action_text = "任命" if action == "appoint" else "免职"
        result = {
            "success": True,
            "appointment": {
                "target_name": target_name,
                "target_position": target_position,
                "action": action_text,
                "authority": f"上级({superior_name}·{superior_position})",
                "pin": target_pin,
                "has_nobility": target_has_nobility,
                "reason": reason,
                "decided_at": time.time(),
            },
        }

        logger.info(
            f"上级任免: {superior_name}({superior_position}) "
            f"{action_text} {target_name}({target_position})"
        )

        return result

    def get_appointment_rules(self) -> Dict[str, Any]:
        """获取任免权规则说明"""
        return {
            "congress_authority": {
                "scope": "正三品及以上品级 + 持有爵位者",
                "method": "投票决策（重大决策5票通过）",
                "members": self.get_members(),
            },
            "superior_authority": {
                "scope": "正三品以下品级且无爵位者",
                "method": "上级直接决定",
            },
            "rule_summary": (
                "七人决策代表大会对各板块高层有任免权（正三品及以上品级和爵位），"
                "上级对下级有任免权（正三品以下品级和没有爵位的）"
            ),
        }


# ═══════════════════════════════════════════════════════════════
#  全局单例
# ═══════════════════════════════════════════════════════════════

_congress_instance: Optional[DecisionCongress] = None


def get_decision_congress() -> DecisionCongress:
    """获取七人决策代表大会全局单例"""
    global _congress_instance
    if _congress_instance is None:
        _congress_instance = DecisionCongress()
    return _congress_instance
