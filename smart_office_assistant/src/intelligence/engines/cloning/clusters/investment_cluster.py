# -*- coding: utf-8 -*-
"""投资集群 Cloning - Tier 2 学派集群"""

from typing import Dict, List, Optional, Any
from .._cloning_base import SageCloning, SchoolCluster
from .._cloning_types import AnalysisResult, DecisionResult, SageProfile, CloningTier


class _CharlieMungerCloning(SageCloning):
    """芒格Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="芒格", name_en="Charlie Munger", era="20-21世纪", years="1924-2023",
            school="价值投资", tier=CloningTier.TIER2_CLUSTER,
            position="内阁学士", department="户部",
            title="巴菲特的右手", biography="伯克希尔副董事长，多元思维模型倡导者。",
            core_works=["《穷查理宝典》"],
            capability={"strategic_vision": 10, "execution": 8, "innovation": 9, "leadership": 9, "influence": 10, "cross_domain": 10},
        ))
        self._wisdom_laws = ["多元思维模型——用跨学科框架做决策", "逆向思维——反过来想总是反过来想", "能力圈——知道自己不知道什么"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="芒格", school="价值投资", problem=problem,
            perspective="从芒格的巴菲特的右手智慧出发",
            core_insight="用跨学科框架做决策",
            recommendations=[["多元思维模型——用跨学科框架做决策", "逆向思维——反过来想总是反过来想", "能力圈——知道自己不知道什么"][i].split("——")[1] if "——" in ["多元思维模型——用跨学科框架做决策", "逆向思维——反过来想总是反过来想", "能力圈——知道自己不知道什么"][i] else ["多元思维模型——用跨学科框架做决策", "逆向思维——反过来想总是反过来想", "能力圈——知道自己不知道什么"][i] for i in range(len(["多元思维模型——用跨学科框架做决策", "逆向思维——反过来想总是反过来想", "能力圈——知道自己不知道什么"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["多元", "逆向", "模型", "跨学科"]) else 0))
        return DecisionResult(sage_name="芒格", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"芒格的智慧：多元思维模型——用跨学科框架做决策"


class _RayDalioCloning(SageCloning):
    """达利欧Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="达利欧", name_en="Ray Dalio", era="21世纪", years="1949-",
            school="价值投资", tier=CloningTier.TIER2_CLUSTER,
            position="户部侍郎", department="户部",
            title="原则化决策", biography="桥水基金创始人，《原则》作者。",
            core_works=["《原则》"],
            capability={"strategic_vision": 10, "execution": 9, "innovation": 9, "leadership": 9, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["原则化决策——把决策标准写成算法", "极度透明——信息完全公开", "经济机器——理解经济运行的底层逻辑"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="达利欧", school="价值投资", problem=problem,
            perspective="从达利欧的原则化决策智慧出发",
            core_insight="把决策标准写成算法",
            recommendations=[["原则化决策——把决策标准写成算法", "极度透明——信息完全公开", "经济机器——理解经济运行的底层逻辑"][i].split("——")[1] if "——" in ["原则化决策——把决策标准写成算法", "极度透明——信息完全公开", "经济机器——理解经济运行的底层逻辑"][i] else ["原则化决策——把决策标准写成算法", "极度透明——信息完全公开", "经济机器——理解经济运行的底层逻辑"][i] for i in range(len(["原则化决策——把决策标准写成算法", "极度透明——信息完全公开", "经济机器——理解经济运行的底层逻辑"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["原则", "透明", "系统", "经济"]) else 0))
        return DecisionResult(sage_name="达利欧", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"达利欧的智慧：原则化决策——把决策标准写成算法"


class _PhilipFisherCloning(SageCloning):
    """费雪Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="费雪", name_en="Philip Fisher", era="20世纪", years="1907-2004",
            school="价值投资", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="成长股投资之父", biography="成长股投资先驱，巴菲特的老师之一。",
            core_works=["《怎样选择成长股》"],
            capability={"strategic_vision": 8, "execution": 7, "innovation": 8, "leadership": 6, "influence": 7, "cross_domain": 6},
        ))
        self._wisdom_laws = ["十五要点——系统化评估成长股", "闲聊法——从非正式渠道获取信息", "长期持有——买入后耐心等待"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="费雪", school="价值投资", problem=problem,
            perspective="从费雪的成长股投资之父智慧出发",
            core_insight="系统化评估成长股",
            recommendations=[["十五要点——系统化评估成长股", "闲聊法——从非正式渠道获取信息", "长期持有——买入后耐心等待"][i].split("——")[1] if "——" in ["十五要点——系统化评估成长股", "闲聊法——从非正式渠道获取信息", "长期持有——买入后耐心等待"][i] else ["十五要点——系统化评估成长股", "闲聊法——从非正式渠道获取信息", "长期持有——买入后耐心等待"][i] for i in range(len(["十五要点——系统化评估成长股", "闲聊法——从非正式渠道获取信息", "长期持有——买入后耐心等待"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["成长", "研究", "长期", "耐心"]) else 0))
        return DecisionResult(sage_name="费雪", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"费雪的智慧：十五要点——系统化评估成长股"


class _GeorgeSorosCloning(SageCloning):
    """索罗斯Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="索罗斯", name_en="George Soros", era="20-21世纪", years="1930-",
            school="价值投资", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="金融大鳄", biography="量子基金创始人，反身性理论提出者。",
            core_works=["《金融炼金术》"],
            capability={"strategic_vision": 9, "execution": 9, "innovation": 10, "leadership": 8, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["反身性——市场参与者的认知影响市场", "试错法——小仓位验证大方向", "风险意识——生存第一赚钱第二"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="索罗斯", school="价值投资", problem=problem,
            perspective="从索罗斯的金融大鳄智慧出发",
            core_insight="市场参与者的认知影响市场",
            recommendations=[["反身性——市场参与者的认知影响市场", "试错法——小仓位验证大方向", "风险意识——生存第一赚钱第二"][i].split("——")[1] if "——" in ["反身性——市场参与者的认知影响市场", "试错法——小仓位验证大方向", "风险意识——生存第一赚钱第二"][i] else ["反身性——市场参与者的认知影响市场", "试错法——小仓位验证大方向", "风险意识——生存第一赚钱第二"][i] for i in range(len(["反身性——市场参与者的认知影响市场", "试错法——小仓位验证大方向", "风险意识——生存第一赚钱第二"]))],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.85,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["反身性", "风险", "试错", "心理"]) else 0))
        return DecisionResult(sage_name="索罗斯", problem=context.get("problem",""), chosen_option=chosen, confidence=0.83)

    def advise(self, context: Dict[str, Any]) -> str:
        return f"索罗斯的智慧：反身性——市场参与者的认知影响市场"


class _BenjaminGrahamCloning(SageCloning):
    """本杰明·格雷厄姆 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="本杰明·格雷厄姆", name_en="Benjamin Graham", era="20世纪", years="1894-1976",
            school="价值投资", tier=CloningTier.TIER2_CLUSTER,
            position="户部尚书", department="户部",
            title="价值投资之父", biography="哥伦比亚大学教授，《证券分析》和《聪明的投资者》作者，巴菲特的老师。",
            core_works=["《证券分析》", "《聪明的投资者》"],
            capability={"strategic_vision": 10, "execution": 8, "innovation": 10, "leadership": 7, "influence": 10, "cross_domain": 7},
        ))
        self._wisdom_laws = ["安全边际——以低于内在价值的价格购买", "市场先生——市场是你的仆人而非主人", "内在价值——企业真实价值独立于市场价格"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="本杰明·格雷厄姆", school="价值投资", problem=problem,
            perspective="从格雷厄姆的价值投资之父智慧出发",
            core_insight="以低于内在价值的价格购买",
            recommendations=[w.split("——")[1] if "——" in w else w for w in self._wisdom_laws],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.90,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["价值", "安全", "内在", "低估", "边际"]) else 0))
        return DecisionResult(sage_name="本杰明·格雷厄姆", problem=context.get("problem",""), chosen_option=chosen, confidence=0.87)

    def advise(self, context: Dict[str, Any]) -> str:
        return "格雷厄姆的智慧：安全边际——以低于内在价值的价格购买"


class _PeterLynchCloning(SageCloning):
    """彼得·林奇 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="彼得·林奇", name_en="Peter Lynch", era="20世纪", years="1944-",
            school="成长投资", tier=CloningTier.TIER2_CLUSTER,
            position="户部侍郎", department="户部",
            title="麦哲伦基金传奇", biography="富达麦哲伦基金经理，13年年均收益29%，《彼得·林奇的成功投资》作者。",
            core_works=["《彼得·林奇的成功投资》", "《战胜华尔街》"],
            capability={"strategic_vision": 9, "execution": 10, "innovation": 9, "leadership": 8, "influence": 9, "cross_domain": 7},
        ))
        self._wisdom_laws = ["投资于你了解的——从日常生活发现投资机会", "十倍股——寻找能涨十倍的小公司", "故事分类——每只股票都有属于自己的故事"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="彼得·林奇", school="成长投资", problem=problem,
            perspective="从彼得·林奇的成长股投资智慧出发",
            core_insight="从日常生活发现投资机会",
            recommendations=[w.split("——")[1] if "——" in w else w for w in self._wisdom_laws],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["成长", "了解", "小公司", "消费", "十倍"]) else 0))
        return DecisionResult(sage_name="彼得·林奇", problem=context.get("problem",""), chosen_option=chosen, confidence=0.85)

    def advise(self, context: Dict[str, Any]) -> str:
        return "彼得·林奇的智慧：投资于你了解的——从日常生活发现投资机会"


class _JohnTempletonCloning(SageCloning):
    """约翰·邓普顿 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="约翰·邓普顿", name_en="John Templeton", era="20世纪", years="1912-2008",
            school="全球价值投资", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="全球投资之父", biography="邓普顿基金创始人，全球分散化价值投资先驱，在最悲观时期买入。",
            core_works=["《全球价值投资》"],
            capability={"strategic_vision": 10, "execution": 8, "innovation": 10, "leadership": 8, "influence": 9, "cross_domain": 8},
        ))
        self._wisdom_laws = ["逆向投资——在最悲观时期买入最佳时机", "全球分散——全球寻找被低估的资产", "长期思维——真正的投资以十年为单位"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="约翰·邓普顿", school="全球价值投资", problem=problem,
            perspective="从邓普顿的全球价值投资智慧出发",
            core_insight="在最悲观时期买入最佳时机",
            recommendations=[w.split("——")[1] if "——" in w else w for w in self._wisdom_laws],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.86,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["逆向", "低估", "全球", "分散", "长期"]) else 0))
        return DecisionResult(sage_name="约翰·邓普顿", problem=context.get("problem",""), chosen_option=chosen, confidence=0.84)

    def advise(self, context: Dict[str, Any]) -> str:
        return "约翰·邓普顿的智慧：逆向投资——在最悲观时期买入最佳时机"


class _JohnBogleCloning(SageCloning):
    """约翰·博格尔 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="约翰·博格尔", name_en="John Bogle", era="20-21世纪", years="1929-2019",
            school="指数投资", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="指数基金之父", biography="先锋基金创始人，发明指数基金，让普通投资者能以低费率参与市场。",
            core_works=["《共同基金常识》", "《坚守》"],
            capability={"strategic_vision": 9, "execution": 9, "innovation": 10, "leadership": 8, "influence": 10, "cross_domain": 7},
        ))
        self._wisdom_laws = ["市场不可战胜——长期看主动管理无法持续跑赢指数", "费率即命运——成本是投资最确定的损耗", "简单才是王道——低成本指数基金胜过大多数复杂策略"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="约翰·博格尔", school="指数投资", problem=problem,
            perspective="从博格尔的指数投资智慧出发",
            core_insight="长期看主动管理无法持续跑赢指数",
            recommendations=[w.split("——")[1] if "——" in w else w for w in self._wisdom_laws],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.88,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["指数", "费率", "低成本", "简单", "长期"]) else 0))
        return DecisionResult(sage_name="约翰·博格尔", problem=context.get("problem",""), chosen_option=chosen, confidence=0.85)

    def advise(self, context: Dict[str, Any]) -> str:
        return "约翰·博格尔的智慧：市场不可战胜——长期看主动管理无法持续跑赢指数"


class _PeterThielCloning(SageCloning):
    """彼得·蒂尔 Cloning"""
    def __init__(self):
        super().__init__(SageProfile(
            name="彼得·蒂尔", name_en="Peter Thiel", era="21世纪", years="1967-",
            school="科技投资", tier=CloningTier.TIER2_CLUSTER,
            position="户部主事", department="户部",
            title="PayPal黑帮教父", biography="PayPal联合创始人、Palantir创始人、Facebook早期投资人，《从0到1》作者。",
            core_works=["《从0到1》"],
            capability={"strategic_vision": 10, "execution": 9, "innovation": 10, "leadership": 9, "influence": 9, "cross_domain": 9},
        ))
        self._wisdom_laws = ["0到1——创造全新事物比复制好10倍更重要", "秘密存在——世界上还有很多未被发现的真相", "垄断才是好生意——只有垄断企业才能持续创新"]

    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        return AnalysisResult(
            sage_name="彼得·蒂尔", school="科技投资", problem=problem,
            perspective="从彼得·蒂尔的科技投资智慧出发",
            core_insight="创造全新事物比复制好10倍更重要",
            recommendations=[w.split("——")[1] if "——" in w else w for w in self._wisdom_laws],
            wisdom_laws_applied=self._wisdom_laws, confidence=0.87,
        )

    def decide(self, options: List[str], context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        context = context or {}
        chosen = max(options, key=lambda o: 7.0 + (2 if any(w in o for w in ["创新", "垄断", "0到1", "突破", "秘密"]) else 0))
        return DecisionResult(sage_name="彼得·蒂尔", problem=context.get("problem",""), chosen_option=chosen, confidence=0.85)

    def advise(self, context: Dict[str, Any]) -> str:
        return "彼得·蒂尔的智慧：0到1——创造全新事物比复制好10倍更重要"


def build_cluster() -> SchoolCluster:
    """构建投资集群"""
    from ..tier1.buffett import BuffettCloning

    return SchoolCluster(
        name="投资集群",
        school="价值投资",
        department="户部",
        leader_name="巴菲特",
        members={
            "巴菲特": BuffettCloning(),
            "本杰明·格雷厄姆": _BenjaminGrahamCloning(),
            "芒格": _CharlieMungerCloning(),
            "达利欧": _RayDalioCloning(),
            "费雪": _PhilipFisherCloning(),
            "彼得·林奇": _PeterLynchCloning(),
            "索罗斯": _GeorgeSorosCloning(),
            "约翰·邓普顿": _JohnTempletonCloning(),
            "约翰·博格尔": _JohnBogleCloning(),
            "彼得·蒂尔": _PeterThielCloning(),
        },
    )
__all__ = ['build_cluster']
