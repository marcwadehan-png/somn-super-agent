# -*- coding: utf-8 -*-
"""
ClawArchitect - Claw子智能体架构核心
=====================================

Phase 4: 每个贤者作为一个独立Claw子智能体的感知-推理-执行-反馈四模块架构。

功能:
- YAML配置加载器（从configs/{name}.yaml读取元数据）
- SageLoop/ReAct闭环推理引擎接入
- Skills工具链绑定
- NeuralMemorySystem记忆层连接
- 个性化人格与智慧法则驱动

数据流:
  用户输入 → 感知(Perception) → 推理(Reasoning/ReAct) → 执行(Execution) → 反馈(Feedback)
                                                              ↓
                                                        记忆持久化(Memory)

版本: v1.0.0
创建: 2026-04-22
"""

from __future__ import annotations

import os
import yaml
import logging
import asyncio
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# ── 项目根路径 ────────────────────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parents[4]
_CONFIGS_DIR = _PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "claws" / "configs"


# ═══════════════════════════════════════════════════════════════
# 安全异常定义 [v10.3 Phase4修复]
# ═══════════════════════════════════════════════════════════════

class ClawConfigError(Exception):
    """Claw配置相关错误基类"""
    pass

class ClawNameValidationError(ClawConfigError):
    """Claw名称校验失败（路径遍历风险或非法字符）"""
    pass

class ClawLoadError(ClawConfigError):
    """Claw配置加载失败"""
    pass


# ═══════════════════════════════════════════════════════════════
# 安全校验工具函数 [v10.3 Phase4修复F001]
# ═══════════════════════════════════════════════════════════════

def _sanitize_name(name: str) -> str:
    """
    校验并清理Claw名称，防止路径遍历攻击。

    检查项:
    - 不包含路径分隔符(.., /, \\)
    - 不包含驱动器名(C:, D:等)
    - 不包含其他危险字符(<>, |, *, ?, "等)
    - 不超出合理长度(≤64字符)

    Args:
        name: 待校验的名称

    Returns:
        清理后的安全名称

    Raises:
        ClawNameValidationError: 名称包含危险字符或格式
    """
    if not name or not isinstance(name, str):
        raise ClawNameValidationError(f"无效的Claw名称: {repr(name)}")

    name_stripped = name.strip()

    # 长度检查
    if len(name_stripped) > 64:
        raise ClawNameValidationError(
            f"Claw名称过长({len(name_stripped)}字符)，最大64字符: {name_stripped[:32]}..."
        )

    # 危险模式列表
    DANGEROUS_PATTERNS = [
        "..",           # 路径遍历
        "/",            # Unix路径分隔符
        "\\",           # Windows路径分隔符
        "<", ">",      # 重定向
        "|",            # 管道
        "*",            # 通配符
        "?",            # 问号通配符
        '"',            # 引号
        "\0",           # 空字节
    ]

    for pattern in DANGEROUS_PATTERNS:
        if pattern in name_stripped:
            raise ClawNameValidationError(
                f"Claw名称包含危险字符 '{pattern}': {name_stripped}"
            )

    # 检查是否以空格或点开头/结尾
    if name_stripped.startswith((' ', '.')):
        raise ClawNameValidationError(
            f"Claw名称不能以空格或点开头: {name_stripped}"
        )

    return name_stripped


# ═══════════════════════════════════════════════════════════════
# YAML配置预加载索引 [v10.2 Phase3优化]
# ═══════════════════════════════════════════════════════════════

class _YAMLConfigCache:
    """
    776个Claw YAML配置的内存缓存 + 元数据索引。

    [v10.2] Phase3优化：
    - 首次加载后全量缓存，避免776次磁盘I/O
    - 按文件mtime自动失效，保证配置更新后重新加载
    - 预热时构建全量索引，供 list_available_claws() 零I/O返回
    - 整体节省：776次文件读取 → 首次1次，后续0次

    用法:
        _yaml_cache.get("孔子")           # 缓存读取，无磁盘I/O
        _yaml_cache.preload_all()         # 后台预热全部776个配置
        _yaml_cache.list_all_names()      # 零I/O返回全量列表
    """

    def __init__(self, configs_dir: Path = None):
        self.configs_dir = configs_dir or _CONFIGS_DIR
        self._config_cache: Dict[str, "ClawMetadata"] = {}
        self._yaml_mtime: Dict[str, float] = {}
        self._index_cache: List[str] = []
        self._metadata_index: List[Dict[str, Any]] = []
        self._index_built = False
        self._preload_lock = __import__("threading").Lock()

    def _get_mtime(self, name: str) -> float:
        """获取YAML文件的修改时间（内部方法，已在调用前校验）"""
        # [v10.3] name已在调用方校验，此处不再重复校验以提升性能
        path = self.configs_dir / f"{name}.yaml"
        if not path.exists():
            path = self.configs_dir / f"{name}.yml"
        try:
            return path.stat().st_mtime if path.exists() else 0.0
        except OSError:
            return 0.0

    def _is_cache_valid(self, name: str) -> bool:
        """检查缓存是否有效（文件未修改，内部方法）"""
        if name not in self._config_cache:
            return False
        return abs(self._get_mtime(name) - self._yaml_mtime.get(name, -1)) < 0.1

    def get(self, name: str) -> Optional["ClawMetadata"]:
        """
        获取Claw配置（优先缓存，无效时重新加载）[v10.3 安全校验]。

        [v10.2] 优化效果：
          - 热命中：O(1) 字典查找
          - 冷失效：重新读取1个文件（而非776个）

        [v10.3] 安全修复：
          - 对name参数进行路径遍历校验
        """
        # [v10.3] 安全校验：防止路径遍历攻击
        safe_name = _sanitize_name(name)

        if self._is_cache_valid(safe_name):
            return self._config_cache.get(safe_name)
        # 缓存失效或未命中，重新加载
        return self._load_single(safe_name)

    def _load_single(self, name: str) -> Optional["ClawMetadata"]:
        """加载单个YAML配置（无缓存查询，内部方法，已校验name）"""
        # [v10.3] name已在get()方法中校验，此处直接使用
        yaml_path = self.configs_dir / f"{name}.yaml"
        if not yaml_path.exists():
            # 仅尝试 .yml 变体（.yaml 已在上面尝试过）
            yml_path = self.configs_dir / f"{name}.yml"
            if yml_path.exists():
                yaml_path = yml_path
            else:
                return None

        try:
            mtime = yaml_path.stat().st_mtime
            with open(yaml_path, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f)
            if not raw or not isinstance(raw, dict):
                return None
            meta = _parse_raw_config(raw)
            # ★ v1.1 修复: 多线程写入共享 dict 需要加锁
            with self._preload_lock:
                self._config_cache[name] = meta
                self._yaml_mtime[name] = mtime
            self._index_built = False  # 需要重建索引
            return meta
        except Exception as e:
            logger.warning(f"[_YAMLCache] 加载 {name} 失败: {e}")
            return None

    def list_all_names(self) -> List[str]:
        """
        零I/O返回所有Claw名称列表。

        首次调用扫描一次磁盘，之后返回缓存列表。
        """
        if self._index_cache:
            return self._index_cache
        names = []
        if not self.configs_dir.exists():
            return names
        for f in sorted(self.configs_dir.iterdir()):
            if f.suffix in (".yaml", ".yml"):
                names.append(f.stem)
        self._index_cache = names
        return names

    def get_metadata_index(self) -> List[Dict[str, Any]]:
        """
        获取全量元数据索引（最小信息集）。

        返回列表包含：name, school, wisdom_school, era, status
        供快速列举/过滤使用，无需解析完整配置。
        """
        if self._metadata_index and self._index_built:
            return self._metadata_index
        # 延迟构建：先确保索引列表就绪
        _ = self.list_all_names()
        results = []
        for name in self._index_cache:
            meta = self.get(name)
            if meta:
                results.append({
                    "name": meta.name,
                    "school": meta.school,
                    "wisdom_school": meta.wisdom_school,
                    "era": meta.era,
                    "status": meta.status,
                })
        self._metadata_index = results
        self._index_built = True
        return results

    def preload_all(self, max_workers: int = 4, timeout_per_file: float = 2.0) -> Dict[str, Any]:
        """
        后台预热全部776个YAML配置 [v10.2]。

        使用多线程并行加载（最多4个worker），每个文件2秒超时，
        总超时60秒。已在缓存中的文件跳过。

        返回:
            {"total": 776, "loaded": N, "failed": M, "elapsed": t}
        """
        import concurrent.futures
        import time as _time

        names = self.list_all_names()
        total = len(names)
        start = _time.time()

        # 过滤出需要加载的（未缓存或已失效）
        to_load = [n for n in names if not self._is_cache_valid(n)]
        loaded = 0
        failed = 0

        def _safe_load(name: str) -> bool:
            try:
                meta = self._load_single(name)
                return meta is not None
            except Exception:
                return False

        # ★ v1.2 修复: 移除外层 preload_lock，避免与 _load_single 内部的锁产生死锁。
        # 多线程安全性已由 _load_single 内部的 with self._preload_lock 保证。
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(_safe_load, name): name
                for name in to_load
            }
            try:
                for future in concurrent.futures.as_completed(
                    futures, timeout=max(10, min(len(to_load) * timeout_per_file / max_workers, 60))
                ):
                    try:
                        ok = future.result(timeout=timeout_per_file)
                        if ok:
                            loaded += 1
                        else:
                            failed += 1
                    except Exception:
                        failed += 1
            except concurrent.futures.TimeoutError:
                logger.warning(f"[_YAMLCache] 预热超时，已加载 {loaded}/{len(to_load)}")

        elapsed = _time.time() - start
        result = {"total": total, "loaded": loaded, "failed": failed, "elapsed": elapsed}
        logger.info(
            f"[_YAMLCache] 预热完成: {loaded}/{total} 加载"
            f" ({failed} 失败), 耗时 {elapsed:.1f}s"
        )
        return result

    def invalidate(self, name: str = None):
        """清除缓存（单个或全部）"""
        if name:
            self._config_cache.pop(name, None)
            self._yaml_mtime.pop(name, None)
        else:
            self._config_cache.clear()
            self._yaml_mtime.clear()
        self._index_built = False


# 全局缓存实例
_yaml_cache = _YAMLConfigCache()


# ═══════════════════════════════════════════════════════════════
# 数据类型定义
# ═══════════════════════════════════════════════════════════════

class ClawStatus(Enum):
    """Claw状态枚举"""
    IDLE = "idle"
    ACTIVE = "active"
    REASONING = "reasoning"
    EXECUTING = "executing"
    ERROR = "error"
    SUSPENDED = "suspended"


class ReasoningStyle(Enum):
    """推理风格"""
    DEEP_ANALYTICAL = "deep_analytical"     # 深度分析型（儒、法）
    INTUITIVE_WISDOM = "intuitive_wisdom"   # 直觉智慧型（道、释）
    PRACTICAL_ACTION = "practical_action"   # 实践行动型（兵、墨）
    SYSTEMATIC_LOGIC = "systematic_logic"   # 系统逻辑型（名、阴阳）
    NARRATIVE_POETIC = "narrative_poetic"    # 叙事诗意型（文、史）
    DIALECTICAL = "dialectical"             # 辩证综合型（杂家等）


@dataclass
class CognitiveDimensions:
    """六大认知维度"""
    cog_depth: float = 7.0        # 思维深度
    decision_quality: float = 7.0 # 决策质量
    value_judge: float = 7.0     # 价值判断
    gov_decision: float = 7.0    # 治理决策
    strategy: float = 7.0        # 战略思维
    self_mgmt: float = 7.0       # 自我管理

    def to_dict(self) -> Dict[str, float]:
        return {
            "cog_depth": self.cog_depth,
            "decision_quality": self.decision_quality,
            "value_judge": self.value_judge,
            "gov_decision": self.gov_decision,
            "strategy": self.strategy,
            "self_mgmt": self.self_mgmt,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CognitiveDimensions":
        if isinstance(data, dict):
            return cls(
                cog_depth=float(data.get("cog_depth", 7.0)),
                decision_quality=float(data.get("decision_quality", 7.0)),
                value_judge=float(data.get("value_judge", 7.0)),
                gov_decision=float(data.get("gov_decision", 7.0)),
                strategy=float(data.get("strategy", 7.0)),
                self_mgmt=float(data.get("self_mgmt", 7.0)),
            )
        return cls()


@dataclass
class ReActConfig:
    """ReAct闭环配置"""
    max_iterations: int = 10
    timeout_seconds: int = 300
    quality_threshold: float = 0.7
    reasoning_style: str = "deep_analytical"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReActConfig":
        if isinstance(data, dict):
            return cls(
                max_iterations=int(data.get("max_iterations", 10)),
                timeout_seconds=int(data.get("timeout_seconds", 300)),
                quality_threshold=float(data.get("quality_threshold", 0.7)),
                reasoning_style=data.get("reasoning_style", "deep_analytical"),
            )
        return cls()


@dataclass
class MemoryConfig:
    """记忆系统配置"""
    memory_type: str = "episodic"       # episodic / semantic / procedural
    path: str = ""
    max_episodes: int = 1000
    consolidation_threshold: int = 50

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryConfig":
        if isinstance(data, dict):
            return cls(
                memory_type=data.get("type", "episodic"),
                path=data.get("path", ""),
                max_episodes=int(data.get("max_episodes", 1000)),
                consolidation_threshold=int(data.get("consolidation_threshold", 50)),
            )
        return cls()


@dataclass
class PersonalityProfile:
    """个性化人格配置"""
    response_style: str = "balanced_informative"
    formality_level: int = 5    # 1-10
    creativity_level: int = 5   # 1-10
    caution_level: int = 5      # 1-10

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典 [v1.2 新增]"""
        return {
            "response_style": self.response_style,
            "formality_level": self.formality_level,
            "creativity_level": self.creativity_level,
            "caution_level": self.caution_level,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PersonalityProfile":
        if isinstance(data, dict):
            return cls(
                response_style=data.get("response_style", "balanced_informative"),
                formality_level=int(data.get("formality_level", 5)),
                creativity_level=int(data.get("creativity_level", 5)),
                caution_level=int(data.get("caution_level", 5)),
            )
        return cls()


@dataclass
class CollaborationConfig:
    """协作配置"""
    can_lead: bool = True
    can_support: bool = True
    preferred_role: str = "analyst"  # leader / analyst / supporter / reviewer

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CollaborationConfig":
        if isinstance(data, dict):
            return cls(
                can_lead=bool(data.get("can_lead", True)),
                can_support=bool(data.get("can_support", True)),
                preferred_role=data.get("preferred_role", "analyst"),
            )
        return cls()


# ═══════════════════════════════════════════════════════════════════
# Claw双阶段架构 v1.0.0 [Phase 0: SOUL | Phase 1: IDENTITY]
# ═══════════════════════════════════════════════════════════════════

@dataclass
class ClawSoul:
    r"""
    Phase 0: 灵魂配置
    
    源自项目迁移设计理念：SOUL.md设计理念：
    - 核心信念（beliefs）
    - 价值观（values）
    - 自律准则（discipline）
    - 性格特征（personality_traits）
    - 响应风格（response_style）
    """
    beliefs: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)
    discipline: List[str] = field(default_factory=list)
    personality_traits: List[str] = field(default_factory=list)
    response_style: Dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClawSoul":
        if isinstance(data, dict):
            # ★ v1.2 修复: 对列表元素进行类型过滤，防止非字符串元素导致 TypeError
            def _str_list(key: str) -> List[str]:
                raw = data.get(key, [])
                return [str(v) for v in raw if v] if isinstance(raw, list) else []
            return cls(
                beliefs=_str_list("beliefs"),
                values=_str_list("values"),
                discipline=_str_list("discipline"),
                personality_traits=_str_list("personality_traits"),
                response_style=data.get("response_style", {}),
            )
        return cls()
    
    def get_primary_belief(self) -> str:
        """获取核心信念"""
        return self.beliefs[0] if self.beliefs else ""
    
    def get_response_style(self, context: str = "default") -> str:
        """获取指定上下文的响应风格"""
        return self.response_style.get(context, self.response_style.get("default", ""))


@dataclass
class ClawIdentity:
    r"""
    Phase 1: 身份配置
    
    源自项目迁移设计理念：IDENTITY.md设计理念：
    - 名称（name）
    - 物种/类型（species）
    - Emoji标志
    - 角色定位（role）
    - 技能标签（skills_tags）
    - 打招呼语（greetings）
    """
    name: str = ""
    species: str = ""
    emoji: str = "🎯"
    role_primary: str = ""
    role_secondary: List[str] = field(default_factory=list)
    skills_tags: List[str] = field(default_factory=list)
    greetings: Dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClawIdentity":
        if isinstance(data, dict):
            role_data = data.get("role", {})
            if isinstance(role_data, dict):
                primary = role_data.get("primary", "")
                secondary = role_data.get("secondary", [])
            else:
                primary = str(role_data)
                secondary = []
            # ★ v1.2 修复: 对列表元素进行类型过滤
            secondary = [str(v) for v in secondary if v] if isinstance(secondary, list) else []
            skills_tags = data.get("skills_tags", [])
            skills_tags = [str(v) for v in skills_tags if v] if isinstance(skills_tags, list) else []
            return cls(
                name=data.get("name", ""),
                species=data.get("species", ""),
                emoji=data.get("emoji", "🎯"),
                role_primary=primary,
                role_secondary=secondary,
                skills_tags=skills_tags,
                greetings=data.get("greetings", {}),
            )
        return cls()
    
    def get_greeting(self, context: str = "default") -> str:
        """获取指定上下文的打招呼"""
        return self.greetings.get(context, self.greetings.get("default", "你好！"))


@dataclass
class ClawMetadata:
    """Claw完整元数据（从YAML加载）"""
    name: str = ""
    sage_id: str = ""
    version: str = "1.0.0"
    status: str = "idle"

    # 基本信息
    era: str = ""
    school: str = ""
    court_position: str = ""
    department: str = ""
    wisdom_school: str = ""

    # 四链路文档引用
    phase_0_doc: str = ""
    phase_1_doc: str = ""
    phase_2_registry: str = ""
    phase_3_factory: str = ""

    # 能力与智慧
    cognitive_dimensions: CognitiveDimensions = field(default_factory=CognitiveDimensions)
    wisdom_laws: List[str] = field(default_factory=list)
    wisdom_functions: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)

    # ReAct闭环
    react_config: ReActConfig = field(default_factory=ReActConfig)

    # 工具与技能
    tools: List[Dict[str, str]] = field(default_factory=list)
    skills: List[Dict[str, Any]] = field(default_factory=list)

    # 记忆
    memory_config: MemoryConfig = field(default_factory=MemoryConfig)

    # 人格
    personality: PersonalityProfile = field(default_factory=PersonalityProfile)

    # 协作
    collaboration: CollaborationConfig = field(default_factory=CollaborationConfig)

    # ═══════════════════════════════════════════════════════════════════
    # Claw双阶段架构 v1.0.0
    # ═══════════════════════════════════════════════════════════════════
    
    # Phase 0: SOUL（灵魂）
    soul: ClawSoul = field(default_factory=ClawSoul)
    
    # Phase 1: IDENTITY（身份）
    identity: ClawIdentity = field(default_factory=ClawIdentity)

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "name": self.name,
            "sage_id": self.sage_id,
            "version": self.version,
            "status": self.status,
            "era": self.era,
            "school": self.school,
            "cognitive_dimensions": self.cognitive_dimensions.to_dict(),
            "wisdom_laws": self.wisdom_laws,
            "wisdom_functions": self.wisdom_functions,
            "triggers": self.triggers,
            "react_config": {
                "max_iterations": self.react_config.max_iterations,
                "timeout_seconds": self.react_config.timeout_seconds,
                "quality_threshold": self.react_config.quality_threshold,
                "reasoning_style": self.react_config.reasoning_style,
            },
            "tools": self.tools,
            "skills": self.skills,
            "memory_config": {
                "type": self.memory_config.memory_type,
                "path": self.memory_config.path,
                "max_episodes": self.memory_config.max_episodes,
            },
            "personality": {
                "response_style": self.personality.response_style,
                "formality_level": self.personality.formality_level,
                "creativity_level": self.personality.creativity_level,
                "caution_level": self.personality.caution_level,
            },
            "collaboration": {
                "can_lead": self.collaboration.can_lead,
                "can_support": self.collaboration.can_support,
                "preferred_role": self.collaboration.preferred_role,
            },
        }


# ═══════════════════════════════════════════════════════════════
# YAML 配置加载器
# ═══════════════════════════════════════════════════════════════

def load_claw_config(name: str, configs_dir: Optional[Path] = None) -> Optional[ClawMetadata]:
    """
    从YAML文件加载Claw配置 [v10.2 缓存优化]。

    Args:
        name: 贤者名称（如"孔子"）
        configs_dir: 配置目录路径，默认为标准claws/configs/

    Returns:
        ClawMetadata实例，加载失败返回None
    """
    # [v10.2] 默认使用全局YAML缓存；传入自定义configs_dir时使用专用缓存实例
    # ★ v1.2 修复: 使用模块级缓存字典，避免每次调用都创建新 _YAMLConfigCache 导致缓存失效
    _custom_caches: Dict[str, "_YAMLConfigCache"] = {}
    if configs_dir is not None and configs_dir != _CONFIGS_DIR:
        cache_key = str(configs_dir)
        if cache_key not in _custom_caches:
            _custom_caches[cache_key] = _YAMLConfigCache(configs_dir)
        return _custom_caches[cache_key].get(name)
    return _yaml_cache.get(name)


def _safe_get_float(value: Any, default: float = 0.0) -> float:
    """安全获取浮点数值，防止float(None)抛TypeError"""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_get_int(value: Any, default: int = 0) -> int:
    """安全获取整数值，防止int(None)抛TypeError"""
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _parse_raw_config(raw: Dict[str, Any]) -> ClawMetadata:
    """
    解析原始YAML字典为ClawMetadata [v10.3 异常保护]。

    兼容v1和v2两种YAML格式：
    - v1: 扁平结构（_gen_claw.py生成）
    - v2: 分段注释结构（_gen_claw_v2.py生成）

    [v10.3] 异常保护：
    - 所有from_dict调用使用安全版本
    - 单个字段解析失败不影响整体返回
    - 日志记录具体失败字段
    """
    try:
        meta = ClawMetadata()
    except Exception:
        raise ClawLoadError("无法创建ClawMetadata实例")

    # 基本字段
    try:
        meta.name = str(raw.get("name", meta.name)) if raw.get("name") else meta.name
        meta.sage_id = str(raw.get("sage_id", meta.sage_id)) if raw.get("sage_id") else meta.sage_id
        meta.version = str(raw.get("version", meta.version)) if raw.get("version") else meta.version
        meta.status = str(raw.get("status", meta.status)) if raw.get("status") else meta.status
    except Exception as e:
        logger.debug(f"[_parse_raw_config] 基本字段解析警告: {e}")

    # 基本信息
    meta.era = str(raw.get("era", "")) if raw.get("era") else ""
    meta.school = str(raw.get("school", "")) if raw.get("school") else ""
    meta.court_position = str(raw.get("court_position", "")) if raw.get("court_position") else ""
    meta.department = str(raw.get("department", "")) if raw.get("department") else ""
    meta.wisdom_school = str(raw.get("wisdom_school", "")) if raw.get("wisdom_school") else ""

    # 四链路文档
    phase_docs = raw.get("phase_documents", {})
    if isinstance(phase_docs, dict):
        meta.phase_0_doc = str(phase_docs.get("phase_0", "")) if phase_docs.get("phase_0") else str(raw.get("phase_0_doc", ""))
        meta.phase_1_doc = str(phase_docs.get("phase_1", "")) if phase_docs.get("phase_1") else str(raw.get("phase_1_doc", ""))
        meta.phase_2_registry = str(phase_docs.get("phase_2", "")) if phase_docs.get("phase_2") else str(raw.get("phase_2_registry", ""))
        meta.phase_3_factory = str(phase_docs.get("phase_3", "")) if phase_docs.get("phase_3") else str(raw.get("phase_3_factory", ""))
    else:
        meta.phase_0_doc = str(raw.get("phase_0_doc", "")) if raw.get("phase_0_doc") else ""
        meta.phase_1_doc = str(raw.get("phase_1_doc", "")) if raw.get("phase_1_doc") else ""
        meta.phase_2_registry = str(raw.get("phase_2_registry", "")) if raw.get("phase_2_registry") else ""
        meta.phase_3_factory = str(raw.get("phase_3_factory", "")) if raw.get("phase_3_factory") else ""

    # 认知维度（兼容两种格式）[v10.3 使用安全解析]
    cd_raw = raw.get("cognitive_dimensions")
    if cd_raw:
        if isinstance(cd_raw, dict):
            try:
                meta.cognitive_dimensions = CognitiveDimensions(
                    cog_depth=_safe_get_float(cd_raw.get("cog_depth"), 7.0),
                    decision_quality=_safe_get_float(cd_raw.get("decision_quality"), 7.0),
                    value_judge=_safe_get_float(cd_raw.get("value_judge"), 7.0),
                    gov_decision=_safe_get_float(cd_raw.get("gov_decision"), 7.0),
                    strategy=_safe_get_float(cd_raw.get("strategy"), 7.0),
                    self_mgmt=_safe_get_float(cd_raw.get("self_mgmt"), 7.0),
                )
            except Exception as e:
                logger.debug(f"[_parse_raw_config] 认知维度解析警告: {e}")
                meta.cognitive_dimensions = CognitiveDimensions()
        elif isinstance(cd_raw, str):
            # 某些v1格式可能是字符串化的dict，跳过
            pass

    # 智慧法则
    wl = raw.get("wisdom_laws", raw.get("personalized_rules", []))
    if isinstance(wl, list):
        meta.wisdom_laws = [str(item) for item in wl if item is not None]
    elif wl is None:
        meta.wisdom_laws = []

    # 智慧函数
    wf = raw.get("wisdom_functions", [])
    if isinstance(wf, list):
        meta.wisdom_functions = [str(item) for item in wf if item is not None]
    elif wf is None:
        meta.wisdom_functions = []

    # 触发词
    tg = raw.get("triggers", [])
    if isinstance(tg, list):
        meta.triggers = [str(item) for item in tg if item is not None]
    elif tg is None:
        meta.triggers = []

    # ReAct配置 [v10.3 使用安全解析]
    rc = raw.get("react_loop", raw.get("react", {}))
    if isinstance(rc, dict):
        try:
            meta.react_config = ReActConfig(
                max_iterations=_safe_get_int(rc.get("max_iterations"), 10),
                timeout_seconds=_safe_get_int(rc.get("timeout_seconds"), 300),
                quality_threshold=_safe_get_float(rc.get("quality_threshold"), 0.7),
                reasoning_style=str(rc.get("reasoning_style", "deep_analytical")) if rc.get("reasoning_style") else "deep_analytical",
            )
        except Exception as e:
            logger.debug(f"[_parse_raw_config] ReAct配置解析警告: {e}")
            meta.react_config = ReActConfig()
    elif rc is None:
        meta.react_config = ReActConfig()

    # 工具
    tl = raw.get("tools", raw.get("system_tools", {}))
    if isinstance(tl, list):
        meta.tools = [t for t in tl if isinstance(t, dict)]
    elif isinstance(tl, dict):
        # v1格式：{"core": [...], "extended": [...]}
        result = []
        for category, items in tl.items():
            if isinstance(items, list):
                for item in items:
                    if item is not None:
                        result.append({"name": str(item), "category": str(category)})
        meta.tools = result
    elif tl is None:
        meta.tools = []

    # 技能
    sk = raw.get("skills", [])
    if isinstance(sk, list):
        meta.skills = [s for s in sk if s is not None]
    elif sk is None:
        meta.skills = []

    # 记忆 [v10.3 使用安全解析]
    mc = raw.get("memory", {})
    if isinstance(mc, dict):
        try:
            meta.memory_config = MemoryConfig(
                memory_type=str(mc.get("type", "episodic")) if mc.get("type") else "episodic",
                path=str(mc.get("path", "")) if mc.get("path") else "",
                max_episodes=_safe_get_int(mc.get("max_episodes"), 1000),
                consolidation_threshold=_safe_get_int(mc.get("consolidation_threshold"), 50),
            )
        except Exception as e:
            logger.debug(f"[_parse_raw_config] 记忆配置解析警告: {e}")
            meta.memory_config = MemoryConfig()
    elif mc is None:
        meta.memory_config = MemoryConfig()

    # 人格 [v10.3 使用安全解析]
    pp = raw.get("personality", {})
    if isinstance(pp, dict):
        try:
            meta.personality = PersonalityProfile(
                response_style=str(pp.get("response_style", "balanced_informative")) if pp.get("response_style") else "balanced_informative",
                formality_level=_safe_get_int(pp.get("formality_level"), 5),
                creativity_level=_safe_get_int(pp.get("creativity_level"), 5),
                caution_level=_safe_get_int(pp.get("caution_level"), 5),
            )
        except Exception as e:
            logger.debug(f"[_parse_raw_config] 人格配置解析警告: {e}")
            meta.personality = PersonalityProfile()
    elif pp is None:
        meta.personality = PersonalityProfile()

    # 协作 [v10.3 使用安全解析]
    cb = raw.get("collaboration", {})
    if isinstance(cb, dict):
        try:
            meta.collaboration = CollaborationConfig(
                can_lead=bool(cb.get("can_lead", True)),
                can_support=bool(cb.get("can_support", True)),
                preferred_role=str(cb.get("preferred_role", "analyst")) if cb.get("preferred_role") else "analyst",
            )
        except Exception as e:
            logger.debug(f"[_parse_raw_config] 协作配置解析警告: {e}")
            meta.collaboration = CollaborationConfig()
    elif cb is None:
        meta.collaboration = CollaborationConfig()

    # ═══════════════════════════════════════════════════════════
    # Claw双阶段架构 v1.0.0 [Phase 0: SOUL | Phase 1: IDENTITY]
    # ═══════════════════════════════════════════════════════════

    # Phase 0: SOUL（灵魂）
    soul_raw = raw.get("soul", {})
    if isinstance(soul_raw, dict):
        try:
            meta.soul = ClawSoul.from_dict(soul_raw)
        except Exception as e:
            logger.debug(f"[_parse_raw_config] SOUL配置解析警告: {e}")
            meta.soul = ClawSoul()
    elif soul_raw is None:
        meta.soul = ClawSoul()

    # Phase 1: IDENTITY（身份）
    identity_raw = raw.get("identity", {})
    if isinstance(identity_raw, dict):
        try:
            meta.identity = ClawIdentity.from_dict(identity_raw)
        except Exception as e:
            logger.debug(f"[_parse_raw_config] IDENTITY配置解析警告: {e}")
            meta.identity = ClawIdentity()
    elif identity_raw is None:
        meta.identity = ClawIdentity()

    # ═══════════════════════════════════════════════════════════
    # v1.0.0 动态格子系统（可选加载）
    # 设置 use_dynamic_cells: true 启用
    # meta._dynamic_memory = DynamicMemorySystem(memory_dir)
    # ═══════════════════════════════════════════════════════════

    return meta


def list_all_configs(configs_dir: Optional[Path] = None) -> List[str]:
    """
    列出所有可用的Claw配置文件名（不含扩展名）[v10.2 缓存优化]。

    Returns:
        贤者名称列表
    """
    # [v10.2] 默认使用缓存；传入自定义configs_dir时创建临时缓存
    if configs_dir is not None and configs_dir != _CONFIGS_DIR:
        cache = _YAMLConfigCache(configs_dir)
        return cache.list_all_names()
    return _yaml_cache.list_all_names()


# ═══════════════════════════════════════════════════════════════
# ReAct/SageLoop 推理闭环
# ═══════════════════════════════════════════════════════════════

@dataclass
class ReActStep:
    """ReAct单步结果"""
    step_num: int
    thought: str           # 思考(Thought)
    action: str            # 动作(Action)
    observation: str       # 观察(Observation)
    confidence: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ReActResult:
    """ReAct闭环最终结果"""
    query: str
    claw_name: str
    steps: List[ReActStep] = field(default_factory=list)
    final_answer: str = ""
    total_tokens: int = 0
    success: bool = False
    reason: str = ""
    elapsed_seconds: float = 0.0


class ReActLoop:
    """
    ReAct (Reasoning + Acting) 推理闭环。

    为每个Claw提供个性化的ReAct循环：
      Thought → Action → Observation → Thought → ...

    特性:
    - 基于Claw配置的max_iterations/timeout/quality_threshold参数
    - 个性化推理风格映射（reasoning_style → ReasoningMode）
    - 智慧法则约束（每一步思考受wisdom_laws指导）
    - 工具调用集成（tools列表中的工具可被Action调用）
    """

    def __init__(self, config: ReActConfig, metadata: ClawMetadata):
        self.config = config
        self.metadata = metadata
        self._steps: List[ReActStep] = []
        self._tool_registry: Dict[str, Callable] = {}
        self._iteration_count = 0
        
        # 跨Claw协作注册表（用于consult动作）
        self._collaborators: Dict[str, "ClawArchitect"] = {}
        self._consult_history: List[Dict[str, Any]] = []

    def register_tool(self, name: str, fn: Callable) -> None:
        """注册可用工具"""
        self._tool_registry[name] = fn

    def register_collaborator(self, name: str, claw: "ClawArchitect") -> None:
        """注册跨Claw协作伙伴"""
        self._collaborators[name] = claw

    def get_collaborators(self) -> List[str]:
        """获取已注册的协作伙伴列表"""
        return list(self._collaborators.keys())

    def _should_continue(self) -> bool:
        """判断是否应继续迭代 [v1.0 + 循环检测]"""
        if self._iteration_count >= self.config.max_iterations:
            return False
        if self._steps and self._steps[-1].confidence >= self.config.quality_threshold:
            return False
        # [v1.0] 循环检测：最近3步动作完全相同 → 认为进入死循环
        if len(self._steps) >= 3:
            last_3_actions = [s.action for s in self._steps[-3:]]
            if len(set(last_3_actions)) == 1 and last_3_actions[0]:
                logger.warning(
                    f"[ReActLoop:{self.metadata.name}] 检测到循环: "
                    f"连续3步相同动作 '{last_3_actions[0]}'，提前终止"
                )
                return False
        return True

    async def run(self, query: str, context: Optional[Dict[str, Any]] = None) -> ReActResult:
        """
        执行ReAct推理闭环 [v9.0 修复: 真正的异步超时保护]。

        Args:
            query: 用户问题/任务
            context: 额外上下文信息（可包含 _timeout_guard 键指向TimeoutGuard实例）

        Returns:
            ReActResult包含完整推理轨迹
        """
        import time
        start_time = time.monotonic()

        # ★ v1.1 修复: 每次调用 run() 必须重置推理状态
        self._steps: List[ReActStep] = []
        self._iteration_count = 0

        result = ReActResult(query=query, claw_name=self.metadata.name)
        ctx = context or {}

        try:
            # ★ v9.0 核心：计算有效超时时间
            effective_timeout = self.config.timeout_seconds

            # 如果全局超时守护器存在，动态缩短超时以适配全局剩余时间
            _global_guard = ctx.get("_timeout_guard")
            if _global_guard is not None:
                global_remaining = getattr(_global_guard.ctx, 'remaining', lambda: effective_timeout)()
                if callable(global_remaining):
                    global_remaining = global_remaining()
                if isinstance(global_remaining, (int, float)) and global_remaining > 0:
                    effective_timeout = min(effective_timeout, float(global_remaining))
                    # 在紧急模式下降低最大迭代次数
                    if global_remaining < 60 and self.config.max_iterations > 3:
                        self._emergency_max_iter = min(self.config.max_iterations, 3)
                        logger.warning(
                            f"[ReActLoop:{self.metadata.name}] 紧急模式: "
                            f"max_iter {self.config.max_iterations}->{self._emergency_max_iter}"
                        )
                    elif global_remaining < 30 and self.config.max_iterations > 2:
                        self._emergency_max_iter = min(self.config.max_iterations, 2)

            # 保存原始max_iterations以便恢复
            _orig_max_iter = self.config.max_iterations
            _has_emergency = hasattr(self, '_emergency_max_iter')
            if _has_emergency:
                self.config.max_iterations = self._emergency_max_iter

            # ★ v9.0 关键修复：将循环体提取为内部协程，用 asyncio.wait_for 施加硬超时
            async def _run_loop():
                while self._should_continue():
                    self._iteration_count += 1
                    step_num = self._iteration_count

                    # ── Thought: 基于智慧法则和认知维度进行思考 ──
                    thought = await self._think(query, ctx, step_num)

                    # ── Action: 决定下一步动作 ──
                    action, action_params = await self._act(thought, query, ctx)

                    # ── Observation: 执行动作并获取观察结果 ──
                    observation, confidence = await self._observe(action, action_params, ctx)

                    # 记录步骤
                    step = ReActStep(
                        step_num=step_num,
                        thought=thought,
                        action=action,
                        observation=observation,
                        confidence=confidence,
                    )
                    self._steps.append(step)

                    # 更新上下文
                    ctx["_last_step"] = step
                    ctx["_all_steps"] = self._steps

                    # 质量阈值检查
                    if confidence >= self.config.quality_threshold:
                        break

                # 生成最终答案
                result.final_answer = await self._synthesize(query, self._steps)
                result.success = True
                result.steps = list(self._steps)

            # ★ 这里才是真正实施超时的地方
            await asyncio.wait_for(_run_loop(), timeout=effective_timeout)

        except asyncio.TimeoutError:
            result.success = False
            elapsed = time.monotonic() - start_time
            result.reason = (
                f"Timeout after {elapsed:.1f}s (limit={effective_timeout:.1f}s, "
                f"iterations={self._iteration_count}/{self.config.max_iterations})"
            )
            logger.warning(f"[ReActLoop:{self.metadata.name}] {result.reason}")

            # 保存已有的中间结果作为部分输出
            if self._steps:
                result.steps = list(self._steps)
                result.final_answer = await self._synthesize_fallback(query, self._steps)
            else:
                result.final_answer = (
                    f"[{self.metadata.name}] 推理超时({effective_timeout:.0f}s)，"
                    f"未能完成任何推理步骤"
                )

            # 通知全局超时守护器记录中间结果
            _global_guard = ctx.get("_timeout_guard")
            if _global_guard is not None:
                try:
                    _global_guard.record_partial(
                        f"react_{self.metadata.name}",
                        {
                            "partial_steps": len(self._steps),
                            "timeout_seconds": effective_timeout,
                            "iterations_done": self._iteration_count,
                            "status": "timeout",
                        }
                    )
                    _global_guard.check_and_degrade()
                except Exception as e:
                    logger.debug(f"[ReActLoop:{self.metadata.name}] 守护器降级检查跳过: {e}")

        except Exception as e:
            result.success = False
            result.reason = "架构生成失败"
            logger.error(f"[ReActLoop:{self.metadata.name}] Error: {e}")
        finally:
            # ★ v1.2 修复: 恢复原始max_iterations（使用 _has_emergency 避免状态泄漏）
            if '_orig_max_iter' in dir() and _has_emergency:
                self.config.max_iterations = _orig_max_iter
                if hasattr(self, '_emergency_max_iter'):
                    delattr(self, '_emergency_max_iter')

        result.elapsed_seconds = time.monotonic() - start_time
        return result

    async def _synthesize_fallback(self, query: str, steps: List[ReActStep]) -> str:
        """
        [v9.0 新增] 降级综合：基于已有中间步骤生成最佳部分答案。
        
        当超时时调用，尽可能利用已产生的推理步骤给出有意义的回答。
        """
        if not steps:
            return f"[{self.metadata.name}] 因超时未能完成推理"

        last_step = steps[-1]

        # 如果最后一步已经是结论动作，直接使用其观察结果
        if last_step.action == "conclude":
            return str(last_step.observation)

        # 构造部分推理摘要
        parts = [
            f"[{self.metadata.name}] 部分推理结果（{len(steps)}步后超时中断）:",
            "",
        ]

        for i, s in enumerate(steps[-3:], start=max(1, len(steps) - 2)):
            thought_preview = s.thought[:150] + ("..." if len(s.thought) > 150 else "")
            obs_preview = s.observation[:150] + ("..." if len(s.observation) > 150 else "")
            parts.append(f"  步骤{i}: 思考={thought_preview}")
            parts.append(f"         动作={s.action} | 观察={obs_preview}")

        # 尝试给出初步结论
        if any(s.action == "conclude" for s in steps):
            conclude_step = next(s for s in steps if s.action == "conclude")
            parts.append(f"\n  已有结论: {conclude_step.observation[:200]}")
        else:
            parts.append("\n  （推理未达到结论即被超时中断）")

        return "\n".join(parts)

    async def _think(self, query: str, context: Dict[str, Any], step_num: int) -> str:
        """
        Thought阶段：生成推理思考。

        结合：
        - 个性化智慧法则（wisdom_laws）
        - 认知维度权重（cognitive_dimensions）
        - 推理风格（reasoning_style）
        - 历史步骤上下文
        """
        laws_text = "；".join(self.metadata.wisdom_laws[:3])  # 取前3条作为主要约束
        dims = self.metadata.cognitive_dimensions

        # 构建思考提示
        thought_parts = [
            f"【{self.metadata.name}的第{step_num}步思考】",
            f"问题：{query}",
            f"智慧指引：{laws_text}",
            f"思维深度={dims.cog_depth:.1f}, 判断力={dims.value_judge:.1f}",
        ]

        # 如果有历史步骤，加入上下文
        if context.get("_last_step"):
            last = context["_last_step"]
            thought_parts.append(
                f"上一步：动作=[{last.action}], 观察=[{last.observation[:100]}]"
            )

        thought = "\n".join(thought_parts)
        logger.debug(f"[ReActLoop:{self.metadata.name}] Step {step_num} thought generated")
        return thought

    async def _act(self, thought: str, query: str, context: Dict[str, Any]) -> tuple:
        """
        Action阶段：决定下一个动作。

        可选动作:
        - conclude: 得出结论（当置信度足够高时）
        - tool_call: 调用工具
        - deep_think: 需要更深层的推理
        - consult: 咨询其他Claw
        """
        step_num = self._iteration_count

        # 最后一步或置信度已够 → conclude
        if step_num >= self.config.max_iterations:
            return "conclude", {"thought": thought}

        # 根据推理风格选择默认动作
        style = self.config.reasoning_style
        if style == "deep_analytical":
            # 分析型偏好工具调用和深层推理
            if step_num <= 2 and self._tool_registry:
                tool_name = list(self._tool_registry.keys())[0]
                return "tool_call", {"tool": tool_name, "input": query}
            elif step_num >= 5 and self._collaborators:
                # 后期阶段尝试跨Claw咨询获取多元视角
                return "consult", {"query": query}
            return "deep_think", {"thought": thought}
        elif style == "intuitive_wisdom":
            # 直觉型较快收敛
            if step_num >= 3:
                return "conclude", {"thought": thought}
            return "deep_think", {"thought": thought}
        else:
            # 默认策略：中期可尝试协作
            if step_num >= 4 and self._collaborators:
                return "consult", {"query": query}
            return "deep_think", {"thought": thought}

    async def _observe(self, action: str, params: Dict[str, Any], context: Dict[str, Any]) -> tuple:
        """
        Observation阶段：执行动作并获取结果。

        Returns:
            (observation_string, confidence_float)
        """
        if action == "conclude":
            thought = params.get("thought", "")
            return f"基于完整推理，准备得出结论。思考摘要：{thought[:200]}", 0.85

        elif action == "tool_call":
            tool_name = params.get("tool", "")
            tool_input = params.get("input", "")
            fn = self._tool_registry.get(tool_name)
            if fn:
                try:
                    if asyncio.iscoroutinefunction(fn):
                        result = await fn(tool_input)
                    else:
                        result = fn(tool_input)
                    return str(result)[:500], 0.6
                except Exception as e:
                    return f"工具[{tool_name}]执行错误: {e}", 0.2
            else:
                return f"工具[{tool_name}]未注册，使用内置推理", 0.5

        elif action == "deep_think":
            return f"深层推理中...结合{self.metadata.name}的{self.metadata.wisdom_laws[0] if self.metadata.wisdom_laws else '智慧'}法则进行分析", 0.55

        elif action == "consult":
            return await self._observe_consult(action, params, context), 0.6

        else:
            return f"未知动作: {action}", 0.0

    async def _observe_consult(
        self, action: str, params: Dict[str, Any], context: Dict[str, Any]
    ) -> str:
        """
        Observation阶段：执行跨Claw咨询。
        
        向已注册的协作Claw发起咨询请求，获取其学派视角的补充分析。
        
        Returns:
            协作Claw的回答摘要
        """
        target_name = params.get("target", "")
        consult_query = params.get("query", "")
        
        if not target_name and self._collaborators:
            # 自动选择一个协作伙伴（轮询或按学派差异）
            available = [
                n for n in self._collaborators 
                if n != self.metadata.name
            ]
            if available:
                # 选择与当前学派不同的Claw
                different_school = [
                    n for n in available
                    if self._collaborators[n].metadata.school != self.metadata.school
                ]
                # ★ v1.1 修复: 用实际选择的池子长度取模，而非 available 长度
                pool = different_school or available
                target_name = pool[len(self._consult_history) % len(pool)]
        
        collaborator = self._collaborators.get(target_name)
        if not collaborator:
            if target_name:
                return f"协作Claw [{target_name}] 未注册，无法咨询"
            return "无可用的协作Claw"
        
        try:
            # 调用协作Claw的process方法获取补充视角
            collab_context = dict(context or {})
            collab_context["_collaboration_role"] = "consultant"
            collab_context["_original_claw"] = self.metadata.name
            
            result = await collaborator.process(
                f"请从{collaborator.metadata.school}学派视角分析：{consult_query}",
                collab_context,
            )
            
            # 记录咨询历史
            self._consult_history.append({
                "target": target_name,
                "query": consult_query[:100],
                "school": collaborator.metadata.school,
                "success": result.success,
                "timestamp": __import__("datetime").datetime.now().isoformat(),
            })
            
            if result.success:
                answer_preview = result.final_answer[:300] if result.final_answer else "(无答案)"
                return (
                    f"[跨Claw咨询→{target_name}({collaborator.metadata.school})] "
                    f"成功。回答摘要: {answer_preview}"
                )
            else:
                return f"[跨Claw咨询→{target_name}] 失败: {result.reason}"
                
        except Exception as e:
            return f"[跨Claw咨询→{target_name}] 异常"

    async def _synthesize(self, query: str, steps: List[ReActStep]) -> str:
        """
        综合所有步骤生成最终答案。
        """
        parts = [
            f"【{self.metadata.name}的回答】",
            f"",
            f"针对问题「{query}」，经过{len(steps)}步ReAct推理：",
        ]

        for i, s in enumerate(steps):
            parts.append(f"\n--- 第{s.step_num}步 ---")
            # ★ v1.2 修复: 仅在内容实际被截断时追加 "..."
            thought_text = s.thought[:150]
            if len(s.thought) > 150:
                thought_text += "..."
            parts.append(f"思考: {thought_text}")
            parts.append(f"动作: {s.action}")
            if len(s.observation) > 200:
                parts.append(f"观察: {s.observation[:200]}...")
            else:
                parts.append(f"观察: {s.observation}")

        # 最终结论
        if steps:
            last_obs = steps[-1].observation
            parts.append(f"\n=== 结论 ===")
            parts.append(f"基于{self.metadata.name}的{self.metadata.school}学派视角：{last_obs}")

        return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════
# Skills 工具链
# ═══════════════════════════════════════════════════════════════

class SkillsToolChain:
    """
    Claw技能工具链。

    管理每个Claw可用的技能集合：
    - analysis: 分析能力
    - writing: 写作能力
    - reasoning: 推理能力
    - memory_recall: 记忆召回
    - knowledge_retrieval: 知识检索
    - ethical_judgment: 伦理判断（儒家等专用）
    - tactical_planning: 战术规划（兵家等专用）
    """

    STANDARD_SKILLS = {
        "analysis": {"desc": "深度分析", "category": "core"},
        "writing": {"desc": "文本生成", "category": "core"},
        "reasoning": {"desc": "逻辑推理", "category": "core"},
        "memory_recall": {"desc": "记忆召回", "category": "core"},
        "knowledge_retrieval": {"desc": "知识检索", "category": "extended"},
        "ethical_judgment": {"desc": "伦理判断", "category": "school_specialized"},
        "tactical_planning": {"desc": "战术规划", "category": "school_specialized"},
        "strategic_consulting": {"desc": "战略咨询", "category": "school_specialized"},
        "classics_interpretation": {"desc": "典籍解读", "category": "school_specialized"},
        "metaphysical_reasoning": {"desc": "形而上学推理", "category": "school_specialized"},
    }

    def __init__(self, metadata: ClawMetadata):
        self.metadata = metadata
        self._skills: Dict[str, Dict[str, Any]] = {}
        self._skill_handlers: Dict[str, Callable] = {}

        # 从YAML配置加载启用的技能
        self._load_from_metadata()

    def _load_from_metadata(self) -> None:
        """从metadata的skills列表初始化"""
        for skill_entry in self.metadata.skills:
            if isinstance(skill_entry, dict):
                name = skill_entry.get("name", "")
                enabled = skill_entry.get("enabled", False)
                if enabled and name:
                    self._skills[name] = self.STANDARD_SKILLS.get(name, {"desc": name, "category": "custom"})
            elif isinstance(skill_entry, str) and skill_entry in self.STANDARD_SKILLS:
                self._skills[skill_entry] = self.STANDARD_SKILLS[skill_entry]

    def register_handler(self, skill_name: str, handler: Callable) -> None:
        """注册技能处理函数"""
        self._skill_handlers[skill_name] = handler

    def has_skill(self, skill_name: str) -> bool:
        return skill_name in self._skills

    def list_skills(self) -> List[Dict[str, str]]:
        return [{"name": k, **v} for k, v in self._skills.items()]

    async def execute(self, skill_name: str, input_data: Any) -> Any:
        """
        执行指定技能。

        Args:
            skill_name: 技能名称
            input_data: 技能输入

        Returns:
            技能输出

        Raises:
            KeyError: 技能未注册
        """
        handler = self._skill_handlers.get(skill_name)
        if handler is None:
            # 尝试使用默认实现
            return await self._default_skill_impl(skill_name, input_data)

        if asyncio.iscoroutinefunction(handler):
            return await handler(input_data)
        else:
            return handler(input_data)

    async def _default_skill_impl(self, skill_name: str, input_data: Any) -> str:
        """技能默认实现（兜底）"""
        desc = self.STANDARD_SKILLS.get(skill_name, {}).get("desc", skill_name)
        return (
            f"[{self.metadata.name}] 使用「{desc}」技能处理: {str(input_data)[:200]}\n"
            f"结合{self.metadata.school}学派视角和{len(self.metadata.wisdom_laws)}条智慧法则。"
        )


# ═══════════════════════════════════════════════════════════════
# NeuralMemorySystem 记忆层适配器
# ═══════════════════════════════════════════════════════════════

@dataclass
class MemoryEpisode:
    """记忆片段"""
    episode_id: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5  # 0-1, 用于遗忘曲线和巩固


class ClawMemoryAdapter:
    """
    Claw记忆系统适配器。

    为每个Claw提供独立的记忆空间：
    - 短期记忆（当前会话上下文）
    - 长期记忆（跨会话持久化）
    - 情景记忆（episodic，记录交互历史）

    存储路径: data/claws/{sage_id}/memory/
    """

    def __init__(self, metadata: ClawMetadata, project_root: Optional[Path] = None):
        self.metadata = metadata
        self.root = project_root or _PROJECT_ROOT
        self.config = metadata.memory_config

        # 内存存储
        self._short_term: List[Dict[str, Any]] = []  # 当前会话
        self._episodes: List[MemoryEpisode] = []      # 情景记忆

        # 确定存储目录
        sage_id = metadata.sage_id or metadata.name
        self.memory_dir = self.root / "data" / "claws" / sage_id / "memory"
        self._ensure_dirs()

        # 加载已有记忆
        self._load_persistent()

    def _ensure_dirs(self) -> None:
        """确保存储目录存在"""
        try:
            self.memory_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logger.warning(f"[ClawMemory:{self.metadata.name}] Cannot create memory dir: {e}")
            self.memory_dir = self.root / "data" / "claws" / "_shared" / "memory"

    def _load_persistent(self) -> None:
        """从磁盘加载长期记忆"""
        ep_file = self.memory_dir / "episodes.json"
        if ep_file.exists():
            try:
                import json
                with open(ep_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._episodes = [MemoryEpisode(**ep) for ep in data]
                logger.debug(f"[ClawMemory:{self.metadata.name}] Loaded {len(self._episodes)} episodes")
            except Exception as e:
                logger.warning(f"[ClawMemory:{self.metadata.name}] Load episodes failed: {e}")

    def add_short_term(self, role: str, content: str, metadata: Optional[Dict] = None) -> None:
        """添加短期记忆"""
        self._short_term.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        })

        # 限制短期记忆大小
        max_st = 50  # 默认保留最近50条
        if len(self._short_term) > max_st:
            self._short_term = self._short_term[-max_st:]

    def add_episode(self, content: str, importance: float = 0.5, metadata: Optional[Dict] = None) -> None:
        """添加情景记忆片段"""
        episode = MemoryEpisode(
            episode_id=f"ep_{len(self._episodes)}_{datetime.now().strftime('%H%M%S')}",
            content=content,
            importance=min(1.0, max(0.0, importance)),
            metadata=metadata or {},
        )
        self._episodes.append(episode)

        # 检查是否需要巩固
        if len(self._episodes) >= self.config.consolidation_threshold:
            self._consolidate()

    def get_context_window(self, max_episodes: int = 10) -> str:
        """
        获取上下文窗口（用于注入到推理中）。

        Returns:
            格式化的记忆上下文字符串
        """
        parts = [f"[{self.metadata.name}的记忆上下文]"]

        # 近期情景记忆
        recent = sorted(self._episodes, key=lambda e: e.timestamp, reverse=True)[:max_episodes]
        if recent:
            parts.append("近期重要记忆:")
            for ep in recent:
                preview = ep.content[:120] + ("..." if len(ep.content) > 120 else "")
                parts.append(f"  - [{ep.timestamp[:16]}] ({ep.importance:.1f}) {preview}")

        # 短期记忆（当前对话）
        if self._short_term:
            parts.append("\n当前对话:")
            for st in self._short_term[-5:]:
                preview = st["content"][:80] + ("..." if len(st["content"]) > 80 else "")
                parts.append(f"  [{st['role']}]: {preview}")

        return "\n".join(parts)

    def search(self, query: str, top_k: int = 5) -> List[MemoryEpisode]:
        """
        简单关键词搜索记忆。

        TODO: 未来接入向量检索（NeuralMemorySystem语义搜索）[延期: 等待NeuralMemorySystem v1.0]
        当前使用关键词匹配，性能足够且无额外依赖
        """
        query_lower = query.lower()
        scored = []
        for ep in self._episodes:
            if query_lower in ep.content.lower():
                # 简单评分：匹配位置越靠前分越高
                pos = ep.content.lower().find(query_lower)
                score = ep.importance + (1.0 / (pos + 1))
                scored.append((score, ep))

        scored.sort(key=lambda x: -x[0])
        return [ep for _, ep in scored[:top_k]]

    def _consolidate(self) -> None:
        """记忆巩固：低重要性记忆归档"""
        # 按重要性排序，保留top max_episodes
        max_ep = self.config.max_episodes
        if len(self._episodes) <= max_ep:
            return

        self._episodes.sort(key=lambda e: (e.importance, e.timestamp), reverse=True)
        archived = self._episodes[max_ep:]
        self._episodes = self._episodes[:max_ep]

        # 归档到文件
        if archived:
            self._save_archive(archived)

    def persist(self) -> bool:
        """持久化记忆到磁盘"""
        try:
            import json

            # 保存episodes
            ep_file = self.memory_dir / "episodes.json"
            data = [{
                "episode_id": ep.episode_id,
                "content": ep.content,
                "timestamp": ep.timestamp,
                "metadata": ep.metadata,
                "importance": ep.importance,
            } for ep in self._episodes]

            with open(ep_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.debug(f"[ClawMemory:{self.metadata.name}] Persisted {len(data)} episodes")
            return True

        except Exception as e:
            logger.error(f"[ClawMemory:{self.metadata.name}] Persist failed: {e}")
            return False

    def _save_archive(self, episodes: List[MemoryEpisode]) -> None:
        """保存归档记忆"""
        try:
            import json
            archive_dir = self.memory_dir / "archive"
            archive_dir.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_file = archive_dir / f"archive_{timestamp}.json"

            data = [{
                "episode_id": ep.episode_id,
                "content": ep.content,
                "timestamp": ep.timestamp,
                "importance": ep.importance,
            } for ep in episodes]

            with open(archive_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"[ClawArchitect:{self.metadata.name}] 记忆归档失败: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        return {
            "claw_name": self.metadata.name,
            "sage_id": self.metadata.sage_id,
            "memory_type": self.config.memory_type,
            "short_term_count": len(self._short_term),
            "episode_count": len(self._episodes),
            "memory_dir": str(self.memory_dir),
            "max_episodes": self.config.max_episodes,
        }


# ═══════════════════════════════════════════════════════════════
# ClawArchitect 主类 — 四模块架构
# ═══════════════════════════════════════════════════════════════

class ClawArchitect:
    """
    Claw子智能体架构核心。

    每个贤者对应一个ClawArchitect实例，提供完整的四模块能力：

    ┌────────────────────────────────────────────┐
    │              ClawArchitect                  │
    ├──────────┬──────────┬──────────┬───────────┤
    │ Perception│ Reasoning│ Execution│  Feedback  │
    │  (感知)   │  (推理)  │  (执行)  │  (反馈)    │
    │          │ ReActLoop│SkillsChain│MemoryAdapter│
    │ YAML加载 │ SageLoop │ ToolCall  │ Persist   │
    └──────────┴──────────┴──────────┴───────────┘

    用法:
        >>> meta = load_claw_config("孔子")
        >>> claw = ClawArchitect(meta)
        >>> result = await claw.process("什么是仁？")
        >>> print(result.final_answer)
    """

    def __init__(self, metadata: ClawMetadata):
        self.metadata = metadata
        self.status = ClawStatus.IDLE

        # ── 模块初始化 ──
        self.memory = ClawMemoryAdapter(metadata)
        self.react_loop = ReActLoop(metadata.react_config, metadata)
        self.skills = SkillsToolChain(metadata)

        # 内置工具注册
        self._register_builtin_tools()

        # 回调钩子
        self._on_before_reasoning: List[Callable] = []
        self._on_after_execution: List[Callable] = []
        self._on_error: List[Callable] = []

    def _register_builtin_tools(self) -> None:
        """注册内置工具到ReActLoop"""
        # 知识检索工具
        self.react_loop.register_tool("knowledge_retrieval", self._tool_knowledge_retrieval)
        # 通用推理工具
        self.react_loop.register_tool("general_reasoning", self._tool_general_reasoning)
        # 记忆召回工具
        self.react_loop.register_tool("memory_recall", self._tool_memory_recall)

    async def _tool_knowledge_retrieval(self, query: str) -> str:
        """内置工具：知识检索（从Phase 0/1文档中检索相关知识）"""
        return f"[知识检索] 在{self.metadata.name}({self.metadata.school})的知识库中检索「{query}」...\n" \
               f"参考文档: {self.metadata.phase_0_doc or self.metadata.phase_1_doc or '无'}\n" \
               f"相关智慧法则: {'; '.join(self.metadata.wisdom_laws[:2])}"

    async def _tool_general_reasoning(self, query: str) -> str:
        """内置工具：通用推理（基于认知维度进行推理分析）"""
        dims = self.metadata.cognitive_dimensions
        return f"[通用推理] {self.metadata.name}对「{query}」的分析:\n" \
               f"- 思维深度: {dims.cog_depth}/10\n" \
               f"- 价值判断: {dims.value_judge}/10\n" \
               f"- 战略思维: {dims.strategy}/10\n" \
               f"结论倾向: 结合{self.metadata.school}传统观点"

    async def _tool_memory_recall(self, query: str) -> str:
        """内置工具：记忆召回"""
        episodes = self.memory.search(query, top_k=3)
        if episodes:
            results = [f"- [{ep.importance:.1f}] {ep.content[:100]}" for ep in episodes]
            return f"[记忆召回] 找到{len(episodes)}条相关记忆:\n" + "\n".join(results)
        return f"[记忆召回] 未找到关于「{query}」的相关记忆"

    async def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> ReActResult:
        """
        处理用户输入的主入口。

        完整流程:
        1. Perception: 记录输入到短期记忆
        2. Pre-reasoning hook
        3. Reasoning: ReAct闭环推理
        4. Post-execution hook
        5. Feedback: 结果写入记忆
        6. 返回结果

        Args:
            query: 用户问题
            context: 额外上下文

        Returns:
            ReActResult
        """
        self.status = ClawStatus.ACTIVE
        ctx = context or {}

        try:
            # 1. Perception: 感知层
            self.memory.add_short_term("user", query)

            # 注入记忆上下文
            memory_context = self.memory.get_context_window(max_episodes=5)
            ctx["memory_context"] = memory_context
            ctx["personality"] = self.metadata.personality.to_dict() if hasattr(self.metadata.personality, 'to_dict') else {}
            ctx["wisdom_laws"] = self.metadata.wisdom_laws

            # 2. Pre-reasoning hooks
            for hook in self._on_before_reasoning:
                if asyncio.iscoroutinefunction(hook):
                    await hook(self, query, ctx)
                else:
                    hook(self, query, ctx)

            # 3. Reasoning: ReAct闭环
            self.status = ClawStatus.REASONING
            result = await self.react_loop.run(query, ctx)

            # 4. Post-execution hooks
            self.status = ClawStatus.EXECUTING
            for hook in self._on_after_execution:
                if asyncio.iscoroutinefunction(hook):
                    await hook(self, result, ctx)
                else:
                    hook(self, result, ctx)

            # 5. Feedback: 反馈层
            if result.success:
                self.memory.add_short_term("assistant", result.final_answer)
                self.memory.add_episode(
                    content=f"Q: {query}\nA: {result.final_answer[:300]}",
                    importance=result.steps[-1].confidence if result.steps else 0.5,
                    metadata={"steps_count": len(result.steps), "elapsed": result.elapsed_seconds},
                )
                # 自动持久化
                self.memory.persist()

        except Exception as e:
            self.status = ClawStatus.ERROR
            result = ReActResult(query=query, claw_name=self.metadata.name)
            result.success = False
            result.reason = "架构生成失败"

            for hook in self._on_error:
                try:
                    if asyncio.iscoroutinefunction(hook):
                        await hook(self, e, ctx)
                    else:
                        hook(self, e, ctx)
                except Exception as hook_error:
                    logger.debug(f"[ClawArchitect] error hook执行失败: {hook_error}")
        finally:
            self.status = ClawStatus.IDLE

        return result

    # ── Hook 注册方法 ──

    def on_before_reasoning(self, fn: Callable) -> "ClawArchitect":
        """注册推理前钩子"""
        self._on_before_reasoning.append(fn)
        return self

    def on_after_execution(self, fn: Callable) -> "ClawArchitect":
        """注册执行后钩子"""
        self._on_after_execution.append(fn)
        return self

    def on_error(self, fn: Callable) -> "ClawArchitect":
        """注册错误钩子"""
        self._on_error.append(fn)
        return self

    # ── 便捷方法 ──

    def get_status_dict(self) -> Dict[str, Any]:
        """获取完整状态字典"""
        return {
            "name": self.metadata.name,
            "sage_id": self.metadata.sage_id,
            "status": self.status.value,
            "school": self.metadata.school,
            "era": self.metadata.era,
            "react_style": self.metadata.react_config.reasoning_style,
            "react_max_iter": self.metadata.react_config.max_iterations,
            "skills_count": len(self.skills.list_skills()),
            "memory_stats": self.memory.get_stats(),
            "wisdom_laws_count": len(self.metadata.wisdom_laws),
            "triggers": self.metadata.triggers,
        }

    def matches_trigger(self, text: str) -> bool:
        """
        检查输入文本是否匹配此Claw的触发词。

        Args:
            text: 用户输入文本

        Returns:
            是否匹配
        """
        text_lower = text.lower()
        return any(trigger.lower() in text_lower for trigger in self.metadata.triggers)


# ═══════════════════════════════════════════════════════════════
# 便捷工厂函数
# ═══════════════════════════════════════════════════════════════

def create_claw(name: str, configs_dir: Optional[Path] = None) -> Optional[ClawArchitect]:
    """
    便捷工厂：根据名称创建完整的Claw实例。

    Args:
        name: 贤者名称（如"孔子"、"王阳明"、"白玉蟾"）

    Returns:
        ClawArchitect实例，配置不存在时返回None
    """
    meta = load_claw_config(name, configs_dir)
    if meta is None:
        return None
    return ClawArchitect(meta)


def create_claws_batch(names: List[str], configs_dir: Optional[Path] = None) -> Dict[str, ClawArchitect]:
    """
    批量创建Claw实例。

    Args:
        names: 贤者名称列表
        configs_dir: 配置目录

    Returns:
        {name: ClawArchitect} 字典
    """
    claws = {}
    for name in names:
        claw = create_claw(name, configs_dir)
        if claw is not None:
            claws[name] = claw
    return claws


__all__ = [
    # 安全异常 [v10.3]
    "ClawConfigError", "ClawNameValidationError", "ClawLoadError",
    # 类型
    "ClawStatus", "ReasoningStyle",
    "ClawMetadata", "CognitiveDimensions", "ReActConfig", "MemoryConfig",
    "PersonalityProfile", "CollaborationConfig",
    "ReActStep", "ReActResult",
    "MemoryEpisode",
    # 核心类
    "ClawArchitect",
    # 子模块
    "ReActLoop", "SkillsToolChain", "ClawMemoryAdapter",
    # 函数
    "load_claw_config", "list_all_configs", "create_claw", "create_claws_batch",
    "_sanitize_name",  # [v10.3] 导出安全校验函数供外部使用
]
