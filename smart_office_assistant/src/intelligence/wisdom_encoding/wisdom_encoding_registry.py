# -*- coding: utf-8 -*-
"""
730贤者智慧编码注册表 v2.2
===========================

v2.2变更: 完全懒加载模式。
       - WisdomEncodingRegistry初始化不含数据，启动时间<1ms
       - 数据在首次访问时才加载
       - 新增lazy参数控制加载时机

v2.1变更: 数据外置到JSON（data/sage_codes.json），支持懒加载。
       原文件9320行(663KB) → 本文件约280行(12KB)。
       数据量: 779条SageCode, 21个学派。

v2.0升级要点:
  - core_methods: 真实智慧法则
  - cognitive_dimensions: 蒸馏文档认知维度评分
  - wisdom_functions: 从法则名语义化生成
  - triggers: 蒸馏文档触发关键词
  - 学派名统一

版本: v2.2
日期: 2026-04-24
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path


# ============================================================================
# 枚举与数据类定义
# ============================================================================


class CognitiveDimension(Enum):
    """六大认知维度"""
    COG_DEPTH = "cog_depth"
    DECISION_QUALITY = "decision_quality"
    VALUE_JUDGE = "value_judge"
    GOV_DECISION = "gov_decision"
    STRATEGY = "strategy"
    SELF_MGMT = "self_mgmt"


class ProblemCategory(Enum):
    """问题类别枚举"""
    SOCIAL_GOVERNANCE = "social_governance"
    PERSONAL_GROWTH = "personal_growth"
    BUSINESS_STRATEGY = "business_strategy"
    ETHICAL_JUDGMENT = "ethical_judgment"
    CRISIS_RESPONSE = "crisis_response"
    LONG_TERM_PLANNING = "long_term_planning"
    RELATIONSHIP = "relationship"
    KNOWLEDGE_INQUIRY = "knowledge_inquiry"


@dataclass
class SageCode:
    """贤者编码数据结构"""
    sage_id: str
    name: str
    era: str
    school: str
    core_methods: List[str]
    cognitive_dimensions: Dict[str, float]
    system_mapping: Dict[str, Any]
    wisdom_functions: List[str]
    integration_layer: str
    triggers: List[str] = field(default_factory=list)

    def get_dimension_score(self, dimension: CognitiveDimension) -> float:
        return self.cognitive_dimensions.get(dimension.value, 5.0)

    def matches_problem(self, problem_text: str) -> float:
        match_count = sum(1 for trigger in self.triggers if trigger in problem_text)
        return min(match_count / max(len(self.triggers), 1), 1.0)

    @classmethod
    def from_dict(cls, data: dict) -> 'SageCode':
        """从字典创建实例（用于JSON加载）"""
        return cls(
            sage_id=data['sage_id'],
            name=data['name'],
            era=data['era'],
            school=data['school'],
            core_methods=data['core_methods'],
            cognitive_dimensions=data['cognitive_dimensions'],
            system_mapping=data['system_mapping'],
            wisdom_functions=data['wisdom_functions'],
            integration_layer=data['integration_layer'],
            triggers=data.get('triggers', []),
        )


@dataclass
class WisdomLaw:
    """通用智慧法则"""
    law_id: str
    name: str
    description: str
    source_sages: List[str]
    implementation_pattern: str
    dimension_weights: Dict[str, float]


@dataclass
class CognitiveBlend:
    """认知维度混合结果"""
    problem_category: ProblemCategory
    dimension_weights: Dict[CognitiveDimension, float]
    primary_sages: List[Tuple[Any, float]]
    wisdom_laws: List[WisdomLaw]


# ============================================================================
# 10大通用智慧法则（保留硬编码——仅10条，量小且逻辑紧密）
# ============================================================================

UNIVERSAL_WISDOM_LAWS: Dict[str, WisdomLaw] = {
    "WL_001": WisdomLaw(law_id="WL_001", name="实践优先", description="行可兼知，事上磨练", source_sages=["王阳明", "颜元"], implementation_pattern="知行合一处理器", dimension_weights={"cog_depth": 0.20, "decision_quality": 0.30, "value_judge": 0.10, "gov_decision": 0.15, "strategy": 0.15, "self_mgmt": 0.10}),
    "WL_002": WisdomLaw(law_id="WL_002", name="中道平衡", description="过犹不及，执两用中", source_sages=["孔子", "亚里士多德"], implementation_pattern="中庸处理器", dimension_weights={"cog_depth": 0.15, "decision_quality": 0.25, "value_judge": 0.25, "gov_decision": 0.20, "strategy": 0.10, "self_mgmt": 0.05}),
    "WL_003": WisdomLaw(law_id="WL_003", name="因势利导", description="顺天应人，乘势而为", source_sages=["老子", "管仲"], implementation_pattern="顺势处理器", dimension_weights={"cog_depth": 0.10, "decision_quality": 0.20, "value_judge": 0.10, "gov_decision": 0.20, "strategy": 0.30, "self_mgmt": 0.10}),
    "WL_004": WisdomLaw(law_id="WL_004", name="系统思维", description="整体观照，辩证统一", source_sages=["王夫之", "张载"], implementation_pattern="系统处理器", dimension_weights={"cog_depth": 0.30, "decision_quality": 0.15, "value_judge": 0.15, "gov_decision": 0.15, "strategy": 0.15, "self_mgmt": 0.10}),
    "WL_005": WisdomLaw(law_id="WL_005", name="知止知足", description="知足不辱，知止不殆", source_sages=["老子", "范蠡"], implementation_pattern="止损处理器", dimension_weights={"cog_depth": 0.20, "decision_quality": 0.20, "value_judge": 0.25, "gov_decision": 0.10, "strategy": 0.10, "self_mgmt": 0.15}),
    "WL_006": WisdomLaw(law_id="WL_006", name="以柔克刚", description="柔弱胜刚强", source_sages=["老子", "孙武"], implementation_pattern="柔韧处理器", dimension_weights={"cog_depth": 0.15, "decision_quality": 0.20, "value_judge": 0.10, "gov_decision": 0.15, "strategy": 0.30, "self_mgmt": 0.10}),
    "WL_007": WisdomLaw(law_id="WL_007", name="居安思危", description="安而不忘危", source_sages=["孟子", "诸葛亮"], implementation_pattern="预警处理器", dimension_weights={"cog_depth": 0.15, "decision_quality": 0.25, "value_judge": 0.10, "gov_decision": 0.20, "strategy": 0.20, "self_mgmt": 0.10}),
    "WL_008": WisdomLaw(law_id="WL_008", name="务实创新", description="守正出奇", source_sages=["王安石", "张衡"], implementation_pattern="创新处理器", dimension_weights={"cog_depth": 0.20, "decision_quality": 0.15, "value_judge": 0.10, "gov_decision": 0.15, "strategy": 0.25, "self_mgmt": 0.15}),
    "WL_009": WisdomLaw(law_id="WL_009", name="教化育人", description="有教无类，因材施教", source_sages=["孔子", "朱熹"], implementation_pattern="教育处理器", dimension_weights={"cog_depth": 0.25, "decision_quality": 0.10, "value_judge": 0.20, "gov_decision": 0.10, "strategy": 0.10, "self_mgmt": 0.25}),
    "WL_010": WisdomLaw(law_id="WL_010", name="天人合一", description="人与自然和谐共生", source_sages=["董仲舒", "张载"], implementation_pattern="生态处理器", dimension_weights={"cog_depth": 0.25, "decision_quality": 0.10, "value_judge": 0.25, "gov_decision": 0.15, "strategy": 0.10, "self_mgmt": 0.15}),
}


# ============================================================================
# 数据加载器（从外部JSON加载贤者数据）
# ============================================================================

_DATA_FILE_PATH = Path(__file__).parent / 'data' / 'sage_codes.json'
_cached_sage_codes: Optional[List[SageCode]] = None


def _get_data_file_path() -> Path:
    """获取数据文件路径"""
    global _DATA_FILE_PATH
    if not _DATA_FILE_PATH.exists():
        # 兼容：如果data目录在上级目录
        _DATA_FILE_PATH = Path(__file__).parent.parent / 'wisdom_encoding' / 'data' / 'sage_codes.json'
    return _DATA_FILE_PATH


def _load_sage_codes_from_json() -> List[SageCode]:
    """从外部JSON文件加载全部贤者编码数据"""
    data_path = _get_data_file_path()
    if not data_path.exists():
        import warnings
        warnings.warn(
            f"SageCodes JSON data file not found: {data_path}. "
            f"Registry will be empty.",
            UserWarning,
            stacklevel=2,
        )
        return []

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    raw_sages = data.get('sages', [])
    return [SageCode.from_dict(s) for s in raw_sages]


def _get_all_sage_codes() -> List[SageCode]:
    """获取全部贤者编码（进程级缓存，返回引用——调用方不应修改）"""
    global _cached_sage_codes
    if _cached_sage_codes is None:
        _cached_sage_codes = _load_sage_codes_from_json()
    return _cached_sage_codes  # [P6] 直接返回引用，省去 O(n) 浅拷贝（779元素）


def invalidate_sage_cache() -> None:
    """清除缓存（用于测试或热更新场景）"""
    global _cached_sage_codes
    _cached_sage_codes = None


# ============================================================================
# Registry核心类
# ============================================================================


class WisdomEncodingRegistry:
    """
    智慧编码注册表 v2.2 — 779贤者蒸馏编码
    
    数据源：外部JSON文件（data/sage_codes.json）
    加载方式：[v2.2] 完全懒加载 - 只在首次访问时才加载数据
    
    启动时间: < 1ms (初始化不含数据)
    """

    def __init__(self, lazy: bool = True):
        """
        初始化注册表
        
        Args:
            lazy: 是否懒加载数据。True时启动最快，但首次访问有延迟
        """
        self._sage_codes: Dict[str, SageCode] = {}
        self._school_encodings: Dict[str, List[str]] = {}
        self._wisdom_laws: Dict[str, WisdomLaw] = {}
        self._dimension_config: Dict[str, Dict[CognitiveDimension, float]] = {}
        self._trigger_index: Dict[str, Set[str]] = {}
        
        # v2.2: 懒加载标志
        self._data_loaded: bool = False
        self._lazy: bool = lazy
        
        self._initialize_dimension_config()
        self._register_universal_wisdom_laws()
        
        # v2.2: 延迟加载数据
        if not lazy:
            self._ensure_data_loaded()

    def _ensure_data_loaded(self) -> None:
        """确保数据已加载（懒加载触发点）"""
        if self._data_loaded:
            return
        
        all_sages = _get_all_sage_codes()
        self.register_sages_batch(all_sages)
        self._build_trigger_index()
        self._data_loaded = True

    def _ensure_data_loaded_lazy(self) -> None:
        """懒加载数据（用于首次访问时自动触发）"""
        if not self._data_loaded:
            self._ensure_data_loaded()

    def _initialize_dimension_config(self) -> None:
        self._dimension_config = {
            "social_governance": {CognitiveDimension.COG_DEPTH: 0.15, CognitiveDimension.DECISION_QUALITY: 0.25, CognitiveDimension.VALUE_JUDGE: 0.20, CognitiveDimension.GOV_DECISION: 0.25, CognitiveDimension.STRATEGY: 0.10, CognitiveDimension.SELF_MGMT: 0.05},
            "business_strategy": {CognitiveDimension.COG_DEPTH: 0.15, CognitiveDimension.DECISION_QUALITY: 0.20, CognitiveDimension.VALUE_JUDGE: 0.15, CognitiveDimension.GOV_DECISION: 0.10, CognitiveDimension.STRATEGY: 0.30, CognitiveDimension.SELF_MGMT: 0.10},
            "personal_growth": {CognitiveDimension.COG_DEPTH: 0.20, CognitiveDimension.DECISION_QUALITY: 0.10, CognitiveDimension.VALUE_JUDGE: 0.15, CognitiveDimension.GOV_DECISION: 0.05, CognitiveDimension.STRATEGY: 0.10, CognitiveDimension.SELF_MGMT: 0.40},
            "ethical_judgment": {CognitiveDimension.COG_DEPTH: 0.15, CognitiveDimension.DECISION_QUALITY: 0.20, CognitiveDimension.VALUE_JUDGE: 0.35, CognitiveDimension.GOV_DECISION: 0.15, CognitiveDimension.STRATEGY: 0.05, CognitiveDimension.SELF_MGMT: 0.10},
            "crisis_response": {CognitiveDimension.COG_DEPTH: 0.10, CognitiveDimension.DECISION_QUALITY: 0.30, CognitiveDimension.VALUE_JUDGE: 0.15, CognitiveDimension.GOV_DECISION: 0.15, CognitiveDimension.STRATEGY: 0.25, CognitiveDimension.SELF_MGMT: 0.05},
            "long_term_planning": {CognitiveDimension.COG_DEPTH: 0.20, CognitiveDimension.DECISION_QUALITY: 0.15, CognitiveDimension.VALUE_JUDGE: 0.15, CognitiveDimension.GOV_DECISION: 0.10, CognitiveDimension.STRATEGY: 0.35, CognitiveDimension.SELF_MGMT: 0.05},
        }

    def _register_universal_wisdom_laws(self) -> None:
        self._wisdom_laws = dict(UNIVERSAL_WISDOM_LAWS)

    def register_sage(self, sage_code: SageCode) -> None:
        self._sage_codes[sage_code.sage_id] = sage_code
        school = sage_code.school
        if school not in self._school_encodings:
            self._school_encodings[school] = []
        self._school_encodings[school].append(sage_code.sage_id)

    def register_sages_batch(self, sages: List[SageCode]) -> None:
        for sage in sages:
            self.register_sage(sage)

    def _build_trigger_index(self) -> None:
        """
        [v10.1 P1-7] 构建触发词倒排索引。
        将所有贤者的 trigger 词语展开，建立 trigger → {sage_id} 的映射表。
        后续 get_cognitive_blend() 先用 problem_text 的所有子串匹配 trigger，
        再仅对命中的 sage_id 计算分数，将复杂度从 O(n*m) 降至 O(k + n')。
        """
        self._trigger_index.clear()
        for sage_id, sage in self._sage_codes.items():
            for trigger in sage.triggers:
                if trigger not in self._trigger_index:
                    self._trigger_index[trigger] = set()
                self._trigger_index[trigger].add(sage_id)

    def _find_matching_sages(self, problem_text: str) -> Dict[str, int]:
        """
        [v10.1 P1-7] 用触发词索引快速找到匹配的sage及命中数量。
        Returns:
            Dict[sage_id, hit_count] — 命中的sages及其命中触发词数量
        """
        hit_counts: Dict[str, int] = {}
        for trigger, sage_ids in self._trigger_index.items():
            if trigger in problem_text:
                for sid in sage_ids:
                    hit_counts[sid] = hit_counts.get(sid, 0) + 1
        return hit_counts

    def get_statistics(self) -> Dict:
        """[v6.2.1] 获取注册表统计信息"""
        self._ensure_data_loaded_lazy()
        return {
            "total_sages": len(self._sage_codes),
            "total_schools": len(self._school_encodings),
            "total_wisdom_laws": len(self._wisdom_laws),
            "schools": {school: len(sages) for school, sages in self._school_encodings.items()},
        }

    def get_sage(self, sage_id: str) -> Optional[SageCode]:
        self._ensure_data_loaded_lazy()
        return self._sage_codes.get(sage_id)

    def get_sages_by_school(self, school: str) -> List[SageCode]:
        self._ensure_data_loaded_lazy()
        ids = self._school_encodings.get(school, [])
        return [self._sage_codes[sid] for sid in ids if sid in self._sage_codes]

    def query_by_problem(self, problem_text: str, top_k: int = 5) -> List[Tuple[SageCode, float]]:
        """[v6.2.1] 按问题文本查询匹配的贤者"""
        self._ensure_data_loaded_lazy()
        hit_counts = self._find_matching_sages(problem_text)
        scores: List[Tuple[SageCode, float]] = []
        for sage_id, hit in hit_counts.items():
            sage = self._sage_codes.get(sage_id)
            if not sage:
                continue
            score = min(hit / max(len(sage.triggers), 1), 1.0)
            scores.append((sage, score))
        # 若索引未命中，fallback到全量扫描
        if not scores:
            scores = [(sage, sage.matches_problem(problem_text))
                      for sage in self._sage_codes.values()]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def get_cognitive_blend(self, problem_text_or_category) -> CognitiveBlend:
        """获取认知混合。接受字符串或ProblemCategory枚举。"""
        self._ensure_data_loaded_lazy()
        # [v6.2.1] 支持 ProblemCategory 枚举或字符串
        if isinstance(problem_text_or_category, ProblemCategory):
            problem_text = problem_text_or_category.value
            category = problem_text_or_category
        else:
            problem_text = str(problem_text_or_category)
            category = ProblemCategory.KNOWLEDGE_INQUIRY
        # [v10.1 P1-7] 使用触发词索引：先命中候选集，再评分
        hit_counts = self._find_matching_sages(problem_text)
        scores: List[Tuple[SageCode, float]] = []
        for sage_id, hit in hit_counts.items():
            sage = self._sage_codes.get(sage_id)
            if not sage:
                continue
            score = min(hit / max(len(sage.triggers), 1), 1.0)
            scores.append((sage, score))
        # 若索引未命中任何sages（文本中无触发词），fallback到全量扫描
        if not scores:
            scores = [(sage, sage.matches_problem(problem_text))
                      for sage in self._sage_codes.values()]
        scores.sort(key=lambda x: x[1], reverse=True)
        primary = scores[:5]
        # 获取维度配置
        dim_key = problem_text if problem_text in self._dimension_config else "social_governance"
        dim_weights = self._dimension_config.get(dim_key, self._dimension_config.get("social_governance", {}))
        return CognitiveBlend(
            problem_category=category,
            dimension_weights=dim_weights,
            primary_sages=primary,
            wisdom_laws=list(self._wisdom_laws.values())[:3]
        )

    def dispatch_wisdom(self, blend: CognitiveBlend, query: str = "") -> Dict[str, Any]:
        """[v6.2.1] 支持可选的 query 参数"""
        result: Dict[str, Any] = {
            "problem_category": blend.problem_category.value if hasattr(blend.problem_category, 'value') else str(blend.problem_category),
            "query": query,
            "recommended_sages": [],
            "wisdom_laws": []
        }
        for sage, score in blend.primary_sages:
            result["recommended_sages"].append({"name": sage.name, "score": score, "methods": sage.core_methods})
        for law in blend.wisdom_laws:
            result["wisdom_laws"].append({"id": law.law_id, "name": law.name})
        return result

    def export_data(self) -> Dict[str, Any]:
        self._ensure_data_loaded_lazy()
        return {"total_sages": len(self._sage_codes), "schools": {k: len(v) for k, v in self._school_encodings.items()}, "wisdom_laws": len(self._wisdom_laws)}


# ============================================================================
# 全局单例
# ============================================================================

_global_registry: Optional[WisdomEncodingRegistry] = None


def get_wisdom_registry(lazy: bool = True) -> WisdomEncodingRegistry:
    """
    获取全局智慧注册表单例
    
    Args:
        lazy: 是否懒加载数据。True时启动最快（<1ms）
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = WisdomEncodingRegistry(lazy=lazy)
    return _global_registry


def create_wisdom_encoding_system() -> WisdomEncodingRegistry:
    return get_wisdom_registry()
