"""
__all__ = [
    'get_saint_king_wisdom',
    'query_saint_king_by_problem',
    'get_technology_guidance',
    'get_agriculture_guidance',
    'get_engineering_guidance',
    'get_scientific_method',
]

科技圣王智慧核心模块 v2.0
Science and Technology Sage Wisdom Core Module

覆盖领域：
- 天文历法数学（22人）
- 工程技术（9人）
- 农学水利（11人）
- 发明创造（5人）
- 地理探险（3人）
- 上古圣王（22人）
- 晚近启蒙（9人）

总计：81位古今中外科技与民生贤者

v2.0: 数据外置到 saint_king_sages_data.json，消除2202行硬编码
v1.0: 初始版本 (2026-04-10)
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

# 数据文件路径（与本模块同目录）
_DATA_PATH = Path(__file__).parent / "saint_king_sages_data.json"


class SaintKingDomain(Enum):
    """科技圣王应用领域"""
    ASTRONOMY_MATH = "天文历法数学"     # 天文观测、历法编制、数学研究
    ENGINEERING = "工程技术"             # 建筑、机械、制造
    AGRICULTURE = "农学水利"             # 农业技术、水利工程
    INVENTION = "发明创造"               # 技术发明、工艺改进
    GEOGRAPHY = "地理探险"               # 地理考察、地图绘制
    SAGE_KING = "上古圣王"               # 上古圣王治理智慧
    MODERN = "晚近启蒙"                  # 近代启蒙思想


class AbilityDimension(Enum):
    """能力维度"""
    TECH_INNOVATION = "技术创新"        # 技术创新能力
    SYSTEM_THINKING = "系统思维"        # 系统思维能力
    EXPERIMENT_SPIRIT = "实验精神"      # 实验探索精神
    ENGINEERING_PRACTICE = "工程实践"    # 工程实践能力
    CROSS_DISCIPLINE = "跨学科整合"      # 跨学科整合能力
    THEORY_BREAKTHROUGH = "理论突破"     # 理论突破能力


@dataclass
class SaintKingProfile:
    """科技圣王贤者画像"""
    sage_id: str                          # 贤者编码
    name: str                             # 姓名
    era: str                              # 时代
    years: str                            # 生卒年/活动年代
    domain: SaintKingDomain               # 所属领域
    core_achievements: List[str]          # 核心成就
    methodology: List[str]                # 方法论
    wisdom_laws: List[str]                # 智慧法则
    abilities: Dict[AbilityDimension, int] # 能力评分 (1-10)
    historical_impact: int                # 历史影响力 (1-10)


@dataclass
class SaintKingWisdomResult:
    """科技圣王智慧查询结果"""
    sage_name: str                        # 推荐贤者
    domain: SaintKingDomain               # 应用领域
    problem: str                          # 输入问题
    core_insight: str                     # 核心洞察
    methodology: List[str]                # 推荐方法论
    wisdom_laws: List[str]                # 智慧法则
    recommendations: List[str]            # 具体建议
    confidence: float                     # 置信度


# --------------------------------------------------------------------------- #
#  反向映射表：JSON中文key → 枚举值                                          #
# --------------------------------------------------------------------------- #

_DOMAIN_REVERSE = {v.value: v for v in SaintKingDomain}
_ABILITY_REVERSE = {v.value: v for v in AbilityDimension}


def _load_sages_from_json(filepath: Path = _DATA_PATH) -> List[Dict[str, Any]]:
    """从 JSON 数据文件加载贤者原始数据，返回可迭代的 dict 列表。"""
    if not filepath.exists():
        raise FileNotFoundError(
            f"圣贤数据文件不存在: {filepath}\n"
            "请确认 saint_king_sages_data.json 与 saint_king_wisdom.py 在同一目录下。"
        )
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    sages = data.get("sages", [])
    logger.debug("从 %s 加载 %d 位贤者数据", filepath, len(sages))
    return sages


def _parse_sage(raw: Dict[str, Any]) -> SaintKingProfile:
    """将 JSON 中的单条贤者 dict 转换为 SaintKingProfile dataclass。"""
    domain = _DOMAIN_REVERSE.get(raw["domain"], SaintKingDomain.ASTRONOMY_MATH)
    abilities = {}
    for k, v in raw.get("abilities", {}).items():
        dim = _ABILITY_REVERSE.get(k)
        if dim is not None:
            abilities[dim] = int(v)
    return SaintKingProfile(
        sage_id=raw["sage_id"],
        name=raw["name"],
        era=raw["era"],
        years=raw["years"],
        domain=domain,
        core_achievements=raw.get("core_achievements", []),
        methodology=raw.get("methodology", []),
        wisdom_laws=raw.get("wisdom_laws", []),
        abilities=abilities,
        historical_impact=int(raw.get("historical_impact", 5)),
    )


class SaintKingWisdomCore:
    """
    科技圣王智慧核心

    提供古代科学家、工程师、圣王的智慧查询
    涵盖天文历法、工程技术、农学水利、发明创造、地理探险等领域
    """

    def __init__(self):
        self._sages: Dict[str, SaintKingProfile] = {}
        self._domain_sages: Dict[SaintKingDomain, List[str]] = {}
        self._initialize_sages()

    def _initialize_sages(self) -> None:
        """从 JSON 数据文件加载全部贤者数据。"""
        raw_list = _load_sages_from_json()
        for raw in raw_list:
            profile = _parse_sage(raw)
            self._add_sage(profile)
        logger.info("圣贤数据初始化完成，共 %d 位贤者", len(self._sages))

    def _add_sage(self, sage: SaintKingProfile) -> None:
        """添加贤者到索引"""
        self._sages[sage.name] = sage
        if sage.domain not in self._domain_sages:
            self._domain_sages[sage.domain] = []
        self._domain_sages[sage.domain].append(sage.name)

    def get_saint_king_wisdom(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None
    ) -> SaintKingWisdomResult:
        """
        获取科技圣王智慧

        Args:
            problem: 待解决的问题
            context: 上下文（可选）

        Returns:
            科技圣王智慧分析结果
        """
        context = context or {}

        # 分析问题领域
        domain = self._classify_problem_domain(problem, context)

        # 选择最合适的贤者
        sage_name = self._select_best_sage(domain, problem)

        if sage_name not in self._sages:
            return SaintKingWisdomResult(
                sage_name="未知",
                domain=domain,
                problem=problem,
                core_insight="暂无匹配的科技圣王",
                methodology=[],
                wisdom_laws=[],
                recommendations=["请尝试更具体的问题描述"],
                confidence=0.0
            )

        sage = self._sages[sage_name]

        return SaintKingWisdomResult(
            sage_name=sage_name,
            domain=domain,
            problem=problem,
            core_insight=self._get_core_insight(sage, domain),
            methodology=sage.methodology,
            wisdom_laws=sage.wisdom_laws[:3],
            recommendations=self._generate_recommendations(problem, sage, domain),
            confidence=0.85
        )

    def query_saint_king_by_problem(self, problem: str) -> List[Dict[str, Any]]:
        """根据问题查询科技圣王智慧"""
        result = self.get_saint_king_wisdom(problem)
        return [{
            "sage": result.sage_name,
            "domain": result.domain.value,
            "insight": result.core_insight,
            "methodology": result.methodology,
            "wisdom_laws": result.wisdom_laws,
            "recommendations": result.recommendations,
            "confidence": result.confidence
        }]

    def get_technology_guidance(
        self,
        problem: str,
        domain: Optional[SaintKingDomain] = None
    ) -> Dict[str, Any]:
        """获取技术领域指导"""
        domain = domain or SaintKingDomain.ASTRONOMY_MATH
        return self._get_domain_guidance(domain, problem)

    def get_agriculture_guidance(self, problem: str) -> Dict[str, Any]:
        """获取农业水利指导"""
        return self._get_domain_guidance(SaintKingDomain.AGRICULTURE, problem)

    def get_engineering_guidance(self, problem: str) -> Dict[str, Any]:
        """获取工程技术指导"""
        return self._get_domain_guidance(SaintKingDomain.ENGINEERING, problem)

    def get_scientific_method(self, problem: str) -> Dict[str, Any]:
        """获取科学方法论指导"""
        result = self.get_saint_king_wisdom(problem)
        sage = self._sages.get(result.sage_name)

        if not sage:
            return {
                "methodology": [],
                "abilities": {},
                "recommendation": "暂无匹配的科学方法"
            }

        return {
            "methodology": sage.methodology,
            "abilities": {k.value: v for k, v in sage.abilities.items()},
            "recommendation": self._generate_recommendations(problem, sage, result.domain)
        }

    def get_sage_by_domain(self, domain: SaintKingDomain) -> List[str]:
        """获取指定领域的所有贤者"""
        return self._domain_sages.get(domain, [])

    def get_all_sages(self) -> Dict[str, SaintKingProfile]:
        """获取所有贤者"""
        return self._sages.copy()

    def get_domain_statistics(self) -> Dict[str, int]:
        """获取各领域统计"""
        return {domain.value: len(sages) for domain, sages in self._domain_sages.items()}

    def _classify_problem_domain(
        self,
        problem: str,
        context: Optional[Dict[str, Any]]
    ) -> SaintKingDomain:
        """分类问题领域"""
        problem_lower = problem.lower()

        # 技术创新/数学/天文
        if any(k in problem_lower for k in ["数学", "天文", "历法", "计算", "算法", "观测", "仪器"]):
            return SaintKingDomain.ASTRONOMY_MATH
        # 工程技术/建筑/机械
        elif any(k in problem_lower for k in ["建筑", "机械", "工程", "设计", "制造", "工具"]):
            return SaintKingDomain.ENGINEERING
        # 农业/水利
        elif any(k in problem_lower for k in ["农业", "水利", "灌溉", "农耕", "土壤", "作物"]):
            return SaintKingDomain.AGRICULTURE
        # 发明/创造/改进
        elif any(k in problem_lower for k in ["发明", "创造", "改进", "创新", "技术"]):
            return SaintKingDomain.INVENTION
        # 地理/探险/地图
        elif any(k in problem_lower for k in ["地理", "探险", "地图", "考察", "山川"]):
            return SaintKingDomain.GEOGRAPHY
        # 上古/圣王/治理
        elif any(k in problem_lower for k in ["治理", "领导", "制度", "治国", "圣王", "上古"]):
            return SaintKingDomain.SAGE_KING
        # 启蒙/近代/改革
        elif any(k in problem_lower for k in ["启蒙", "改革", "近代", "西学", "变革"]):
            return SaintKingDomain.MODERN

        # 默认根据上下文或返回综合领域
        return SaintKingDomain.ASTRONOMY_MATH

    def _select_best_sage(
        self,
        domain: SaintKingDomain,
        problem: str
    ) -> str:
        """选择最合适的贤者"""
        sages = self._domain_sages.get(domain, [])

        if not sages:
            # 尝试从所有贤者中选择
            sages = list(self._sages.keys())

        if not sages:
            return "未知"

        # 根据问题关键词匹配合适的贤者
        problem_lower = problem.lower()

        for sage_name in sages:
            sage = self._sages[sage_name]
            # 检查核心成就是否包含问题关键词
            for achievement in sage.core_achievements:
                if any(k in achievement for k in problem_lower if len(k) > 2):
                    return sage_name

        # 返回该领域影响力最高的贤者
        best_sage = max(sages, key=lambda s: self._sages[s].historical_impact)
        return best_sage

    def _get_core_insight(
        self,
        sage: SaintKingProfile,
        domain: SaintKingDomain
    ) -> str:
        """获取核心洞察"""
        if sage.wisdom_laws:
            return sage.wisdom_laws[0]
        return f"{sage.name}的智慧：技术创新与系统思维并重"

    def _generate_recommendations(
        self,
        problem: str,
        sage: SaintKingProfile,
        domain: SaintKingDomain
    ) -> List[str]:
        """生成建议"""
        recommendations = []

        # 添加方法论建议
        for method in sage.methodology[:2]:
            recommendations.append(f"方法：{method}")

        # 添加智慧法则
        for law in sage.wisdom_laws[:2]:
            if "——" in law:
                parts = law.split("——")
                if len(parts) >= 2:
                    recommendations.append(f"原则：{parts[1].strip()}")
            else:
                recommendations.append(f"智慧：{law}")

        return recommendations

    def _get_domain_guidance(
        self,
        domain: SaintKingDomain,
        problem: str
    ) -> Dict[str, Any]:
        """获取领域指导"""
        sages = self._domain_sages.get(domain, [])

        if not sages:
            return {
                "domain": domain.value,
                "sages": [],
                "guidance": "该领域暂无数据"
            }

        # 获取该领域最杰出的贤者
        top_sages = sorted(
            [self._sages[s] for s in sages],
            key=lambda x: x.historical_impact,
            reverse=True
        )[:3]

        return {
            "domain": domain.value,
            "top_sages": [
                {
                    "name": s.name,
                    "era": s.era,
                    "core_achievements": s.core_achievements,
                    "methodology": s.methodology,
                    "wisdom": s.wisdom_laws[:3]
                }
                for s in top_sages
            ],
            "guidance": f"推荐参考{top_sages[0].name if top_sages else '该领域'}的智慧"
        }


# 全局单例
_ENGINE: Optional[SaintKingWisdomCore] = None


def get_saint_king_wisdom(
    problem: str,
    context: Optional[Dict[str, Any]] = None
) -> SaintKingWisdomResult:
    """获取科技圣王智慧（全局入口）"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SaintKingWisdomCore()
    return _ENGINE.get_saint_king_wisdom(problem, context)


def query_saint_king_by_problem(problem: str) -> List[Dict[str, Any]]:
    """根据问题查询科技圣王智慧"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SaintKingWisdomCore()
    return _ENGINE.query_saint_king_by_problem(problem)


def get_technology_guidance(
    problem: str,
    domain: Optional[SaintKingDomain] = None
) -> Dict[str, Any]:
    """获取技术领域指导"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SaintKingWisdomCore()
    return _ENGINE.get_technology_guidance(problem, domain)


def get_agriculture_guidance(problem: str) -> Dict[str, Any]:
    """获取农业水利指导"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SaintKingWisdomCore()
    return _ENGINE.get_agriculture_guidance(problem)


def get_engineering_guidance(problem: str) -> Dict[str, Any]:
    """获取工程技术指导"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SaintKingWisdomCore()
    return _ENGINE.get_engineering_guidance(problem)


def get_scientific_method(problem: str) -> Dict[str, Any]:
    """获取科学方法论指导"""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = SaintKingWisdomCore()
    return _ENGINE.get_scientific_method(problem)
