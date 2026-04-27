# -*- coding: utf-8 -*-
"""
儒释道fusiondecision引擎 v1.0.0
Confucian-Buddhist-Dao Fusion Decision Engine

基于<儒释道三家文化深度研究报告>(2026-04-02) 的智慧fusion系统

核心思想:
- 以儒治世:以孔子为代表的儒家思想,专注于社会秩序,人伦关系,经世致用
- 以道治身:以老子为代表的道家思想,专注于个人修养,自然无为,身心平衡
- 以佛治心:以释迦牟尼为代表的佛家思想,专注于心灵解脱,慈悲智慧,超越执念

三家fusion:
- 功能互补:入世/避世/超越
- 思想fusion:三教合一
- 共同构成中华文明精神支柱

版本: v1.0.0
更新: 2026-04-02
作者: Somn
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

class WisdomSchool(Enum):
    """智慧流派"""
    RU = "儒"           # 儒家 - 入世治世
    DAO = "道"          # 道家 - 治身养生
    BUDDHISM = "佛"      # 佛家 - 治心解脱

class DecisionDomain(Enum):
    """decision领域"""
    CAREER = "事业"          # 职业,创业,战略
    RELATIONSHIP = "人际关系"   # 家庭,社交,团队
    PERSONAL = "个人成长"      # 修身,学习,心态
    CRISIS = "危机应对"       # 困境,抉择,转型
    CULTURE = "文化使命"      # 品牌,文化,传承 (文化品牌专项)

class LifeLevel(Enum):
    """人生层次"""
    PHYSICAL = "物质层"    # 生存,利益,竞争
    SOCIAL = "社会层"      # 名誉,地位,人际
    SPIRITUAL = "精神层"   # 价值,意义,使命
    TRANSCENDENT = "超越层" # 解脱,自在,无为

@dataclass
class ThreeTeachingsBalance:
    """三教平衡结构"""
    ru_score: float      # 儒家得分 (0-1)
    dao_score: float     # 道家得分 (0-1)
    buddhism_score: float # 佛家得分 (0-1)
    
    # synthesize评估
    dominant_school: WisdomSchool
    secondary_school: Optional[WisdomSchool]
    balance_degree: float  # 平衡度 (0-1)
    
    # 建议
    primary_recommendation: str
    harmony_guidance: str

@dataclass
class FusionDecision:
    """fusiondecision结构"""
    decision_id: str
    
    # decision基本信息
    situation: str
    domain: DecisionDomain
    life_level: LifeLevel
    
    # 三教分析
    ru_analysis: Dict[str, Any]      # 儒家视角分析
    dao_analysis: Dict[str, Any]      # 道家视角分析
    buddhism_analysis: Dict[str, Any] # 佛家视角分析
    
    # fusiondecision
    three_teachings_balance: ThreeTeachingsBalance
    integrated_advice: List[str]      # fusion建议
    wisdom_source: str                 # 智慧来源
    expected_outcome: str              # 预期结果
    
    # 执行指引
    immediate_action: str              # 立即action
    medium_term_action: str            # 中期规划
    long_term_direction: str          # 长期方向
    
    # 警示
    ru_warnings: List[str]            # 儒家警示
    dao_warnings: List[str]            # 道家警示
    buddhism_warnings: List[str]       # 佛家警示

class ConfucianBuddhistDaoFusion:
    """
    儒释道fusiondecision引擎
    
    ┌────────────────────────────────────────────────────────────────┐
    │                    儒释道三家fusion智慧体系                          │
    ├────────────────────────────────────────────────────────────────┤
    │                                                                │
    │    ┌──────────┐     ┌──────────┐     ┌──────────┐            │
    │    │   儒     │ ──▶ │   道     │ ──▶ │   佛     │            │
    │    │  入世治世 │     │  治身养生 │     │  治心解脱 │            │
    │    └──────────┘     └──────────┘     └──────────┘            │
    │         │                │                │                    │
    │         ▼                ▼                ▼                    │
    │    ┌──────────────────────────────────────────┐               │
    │    │           三家和而不同                      │               │
    │    │    以儒治世,以道治身,以佛治心              │               │
    │    └──────────────────────────────────────────┘               │
    │                          │                                   │
    │                          ▼                                   │
    │              ┌─────────────────────┐                          │
    │              │   中华文明精神支柱    │                          │
    │              └─────────────────────┘                          │
    └────────────────────────────────────────────────────────────────┘
    
    核心方法:
    - make_fusion_decision() - 三家fusiondecision
    - analyze_three_teachings() - 三教平衡分析
    - get_domain_guidance() - 分领域指导
    - integrate_with_reasoning() - 推理链集成
    """
    
    def __init__(self):
        """init儒释道fusion引擎"""
        self.name = "ConfucianBuddhistDaoFusion"
        self.version = "v1.0.0"
        
        # ═══════════════════════════════════════════════════════
        # 儒家核心智慧
        # ═══════════════════════════════════════════════════════
        self.ru_wisdom = {
            "core": {
                "name": "儒家",
                "origin": "以孔子为代表的儒家思想",
                "focus": "社会秩序,人伦关系,经世致用",
                "method": "修身齐家治国平天下",
                "virtue": "仁,义,礼,智,信"
            },
            "key_teachings": {
                "ren": {
                    "term": "仁",
                    "meaning": "仁者爱人,己所不欲勿施于人",
                    "application": "人际交往,企业文化,客户关系"
                },
                "li": {
                    "term": "礼",
                    "meaning": "礼之用,和为贵;非礼勿视,非礼勿听",
                    "application": "制度设计,流程规范,品牌形象"
                },
                "yi": {
                    "term": "义",
                    "meaning": "义者宜也,见利思义,君子喻于义",
                    "application": "商业道德,合作伙伴,社会责任"
                },
                "zhi": {
                    "term": "智",
                    "meaning": "智者知也,知之为知之,不知为不知",
                    "application": "战略decision,风险recognize,创新管理"
                },
                "xin": {
                    "term": "信",
                    "meaning": "信者诚也,民无信不立",
                    "application": "品牌信誉,客户信任,团队凝聚"
                }
            },
            "decision_principles": {
                "strategy": "为政以德,譬如北辰,居其所而众星共之",
                "talent": "君子之德风,小人之德草,草上之风必偃",
                "crisis": "君子求诸己,小人求诸人",
                "relationship": "己欲立而立人,己欲达而达人"
            },
            "adaptation_rules": {
                "CAREER": "以义为先,利而后义",
                "RELATIONSHIP": "以仁为本,和而不同",
                "PERSONAL": "以智为用,学而不厌",
                "CRISIS": "以礼为守,危而不乱",
                "CULTURE": "以德为根,传承创新"
            }
        }
        
        # ═══════════════════════════════════════════════════════
        # 道家核心智慧
        # ═══════════════════════════════════════════════════════
        self.dao_wisdom = {
            "core": {
                "name": "道家",
                "origin": "以老子为代表的道家思想",
                "focus": "个人修养,自然无为,身心平衡",
                "method": "道法自然,无为而治",
                "virtue": "柔弱,谦下,不争"
            },
            "key_teachings": {
                "ziran": {
                    "term": "自然",
                    "meaning": "人法地,地法天,天法道,道法自然",
                    "application": "顺势而为,不强求,顺其自然"
                },
                "wuwei": {
                    "term": "无为",
                    "meaning": "为学日益,为道日损,无为而无不为",
                    "application": "减少干预,相信团队,顺势引导"
                },
                "ruoxiu": {
                    "term": "柔弱",
                    "meaning": "天下至柔,驰骋天下之至坚,水滴石穿",
                    "application": "以柔克刚,以退为进,柔能克刚"
                },
                "buzheng": {
                    "term": "不争",
                    "meaning": "夫唯不争,天下莫能与之争,为而不争",
                    "application": "专注本分,不参与无谓竞争"
                },
                "zhiman": {
                    "term": "知足",
                    "meaning": "祸莫大于不知足,咎莫大于欲得,知足者富",
                    "application": "合理预期,控制欲望,适可而止"
                }
            },
            "decision_principles": {
                "strategy": "以正治国,以奇用兵",
                "talent": "上善若水,水善利万物而不争",
                "crisis": "祸兮福之所倚,福兮祸之所伏,否极泰来",
                "relationship": "和大怨,必有余怨,和光同尘"
            },
            "adaptation_rules": {
                "CAREER": "顺势而为,不强求",
                "RELATIONSHIP": "和光同尘,不露锋芒",
                "PERSONAL": "致虚极,守静笃",
                "CRISIS": "静观其变,以静制动",
                "CULTURE": "返璞归真,自然天成"
            }
        }
        
        # ═══════════════════════════════════════════════════════
        # 佛家核心智慧
        # ═══════════════════════════════════════════════════════
        self.buddhism_wisdom = {
            "core": {
                "name": "佛家",
                "origin": "以释迦牟尼为代表的佛家思想",
                "focus": "心灵解脱,慈悲智慧,超越执念",
                "method": "四圣谛八正道",
                "virtue": "戒,定,慧;慈悲,智慧,放下"
            },
            "key_teachings": {
                "four_truths": {
                    "term": "四圣谛",
                    "meaning": "苦(认识苦),集(找出因),灭(消除因),道(八正道)",
                    "application": "问题分析,原因追溯,解决方案,持续修行"
                },
                "eightfold": {
                    "term": "八正道",
                    "meaning": "正见,正思惟,正语,正业,正命,正精进,正念,正定",
                    "application": "正确的认知,思维,言行,谋生,努力,专注"
                },
                "emptiness": {
                    "term": "空",
                    "meaning": "诸行无常,诸法无我,缘起性空",
                    "application": "放下执念,看透本质,不执着于成败"
                },
                "compassion": {
                    "term": "慈悲",
                    "meaning": "慈能予乐,悲能拔苦,无缘大慈,同体大悲",
                    "application": "客户关怀,员工关怀,社会责任"
                },
                "let_go": {
                    "term": "放下",
                    "meaning": "放下执念,方得自在;过去心不可得,现在心不可得",
                    "application": "放下得失心,放下虚荣,放下不必要的负担"
                }
            },
            "decision_principles": {
                "strategy": "因上努力,果上随缘",
                "talent": "一切众生皆具如来智慧相因",
                "crisis": "一切有为法,如梦幻泡影,如露亦如电",
                "relationship": "无缘大慈,同体大悲"
            },
            "adaptation_rules": {
                "CAREER": "因上努力,果上随缘",
                "RELATIONSHIP": "慈悲喜舍,四无量心",
                "PERSONAL": "戒定慧三学,止观双运",
                "CRISIS": "看透放下,自在随缘",
                "CULTURE": "法喜充满,传承智慧"
            }
        }
        
        # ═══════════════════════════════════════════════════════
        # 三家fusion规则
        # ═══════════════════════════════════════════════════════
        self.fusion_rules = {
            # 人生层次 → 三教权重
            "PHYSICAL": {
                "ru": 0.3, "dao": 0.4, "buddhism": 0.3,
                "guidance": "物质层面:道家顺势,儒家规范,佛家放下"
            },
            "SOCIAL": {
                "ru": 0.5, "dao": 0.3, "buddhism": 0.2,
                "guidance": "社会层面:儒家为主,道家为辅,佛家超脱"
            },
            "SPIRITUAL": {
                "ru": 0.3, "dao": 0.4, "buddhism": 0.3,
                "guidance": "精神层面:三家平衡,归于中道"
            },
            "TRANSCENDENT": {
                "ru": 0.2, "dao": 0.3, "buddhism": 0.5,
                "guidance": "超越层面:佛家为主,道家为辅,儒家补位"
            }
        }
        
        # decision历史
        self.decision_history: List[FusionDecision] = []
    
    # ═══════════════════════════════════════════════════════════════
    # 核心decision方法
    # ═══════════════════════════════════════════════════════════════
    
    def make_fusion_decision(self, situation: Dict) -> FusionDecision:
        """
        儒释道fusiondecision
        
        Args:
            situation: decision情境,包含:
                - description: 情境描述
                - domain: decision领域 (CAREER/RELATIONSHIP/PERSONAL/CRISIS/CULTURE)
                - life_level: 人生层次 (PHYSICAL/SOCIAL/SPIRITUAL/TRANSCENDENT)
                - challenge: 主要挑战
                - options: 可选方案
        
        Returns:
            FusionDecision: fusiondecision结果
        """
        decision_id = f"fusion_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        description = situation.get("description", "")
        domain = situation.get("domain", DecisionDomain.PERSONAL)
        life_level = situation.get("life_level", LifeLevel.SOCIAL)
        challenge = situation.get("challenge", "")
        
        # 1. 儒家视角分析
        ru_analysis = self._analyze_from_ru(situation)
        
        # 2. 道家视角分析
        dao_analysis = self._analyze_from_dao(situation)
        
        # 3. 佛家视角分析
        buddhism_analysis = self._analyze_from_buddhism(situation)
        
        # 4. 三教平衡分析
        balance = self._analyze_three_teachings(ru_analysis, dao_analysis, buddhism_analysis, life_level)
        
        # 5. fusion建议
        integrated_advice = self._generate_integrated_advice(domain, life_level, balance)
        
        # 6. generatedecision
        return FusionDecision(
            decision_id=decision_id,
            situation=description,
            domain=domain,
            life_level=life_level,
            ru_analysis=ru_analysis,
            dao_analysis=dao_analysis,
            buddhism_analysis=buddhism_analysis,
            three_teachings_balance=balance,
            integrated_advice=integrated_advice,
            wisdom_source=self._get_wisdom_source(domain),
            expected_outcome=self._get_expected_outcome(domain, balance),
            immediate_action=self._get_immediate_action(domain, balance),
            medium_term_action=self._get_medium_term_action(domain, balance),
            long_term_direction=self._get_long_term_direction(domain, balance),
            ru_warnings=self._get_ru_warnings(situation),
            dao_warnings=self._get_dao_warnings(situation),
            buddhism_warnings=self._get_buddhism_warnings(situation)
        )
    
    def _analyze_from_ru(self, situation: Dict) -> Dict[str, Any]:
        """儒家视角分析"""
        description = situation.get("description", "")
        domain = situation.get("domain", DecisionDomain.PERSONAL)
        
        # 确定儒家核心原则
        if domain == DecisionDomain.CAREER:
            core_virtue = "义"
            principle = self.ru_wisdom["key_teachings"]["yi"]
            quote = "君子喻于义,小人喻于利"
        elif domain == DecisionDomain.RELATIONSHIP:
            core_virtue = "仁"
            principle = self.ru_wisdom["key_teachings"]["ren"]
            quote = "己所不欲,勿施于人"
        elif domain == DecisionDomain.CRISIS:
            core_virtue = "礼"
            principle = self.ru_wisdom["key_teachings"]["li"]
            quote = "君子求诸己,小人求诸人"
        else:
            core_virtue = "智"
            principle = self.ru_wisdom["key_teachings"]["zhi"]
            quote = "知之为知之,不知为不知"
        
        # 儒家建议
        suggestions = []
        if "竞争" in description or "利益" in description:
            suggestions.append("先义后利,见利思义")
        if "团队" in description or "员工" in description:
            suggestions.append("以德服人,以身作则")
        if "客户" in description or "用户" in description:
            suggestions.append("仁者爱人,客户至上")
        if "品牌" in description or "形象" in description:
            suggestions.append("礼之用,和为贵,品牌调性一致")
        
        return {
            "school": WisdomSchool.RU,
            "core_virtue": core_virtue,
            "principle": principle,
            "quote": quote,
            "suggestions": suggestions if suggestions else ["以儒治世,恪守正道"],
            "focus": "社会秩序,人伦关系,经世致用"
        }
    
    def _analyze_from_dao(self, situation: Dict) -> Dict[str, Any]:
        """道家视角分析"""
        description = situation.get("description", "")
        domain = situation.get("domain", DecisionDomain.PERSONAL)
        
        # 确定道家核心原则
        if "困境" in description or "危机" in description:
            core_teaching = "祸福"
            principle = self.dao_wisdom["key_teachings"]["zhiman"]
            quote = "祸兮福之所倚,福兮祸之所伏"
        elif "竞争" in description or "压力" in description:
            core_teaching = "不争"
            principle = self.dao_wisdom["key_teachings"]["buzheng"]
            quote = "夫唯不争,天下莫能与之争"
        elif "变革" in description or "创新" in description:
            core_teaching = "自然"
            principle = self.dao_wisdom["key_teachings"]["ziran"]
            quote = "道法自然,顺势而为"
        else:
            core_teaching = "无为"
            principle = self.dao_wisdom["key_teachings"]["wuwei"]
            quote = "为学日益,为道日损"
        
        # 道家建议
        suggestions = []
        if "焦虑" in description or "急躁" in description:
            suggestions.append("致虚极,守静笃")
        if "过度" in description or "贪心" in description:
            suggestions.append("知足不争,适可而止")
        if "僵化" in description or "固执" in description:
            suggestions.append("上善若水,随物赋形")
        if "高端" in description or "奢侈品" in description:
            suggestions.append("返璞归真,大巧若拙")
        
        return {
            "school": WisdomSchool.DAO,
            "core_teaching": core_teaching,
            "principle": principle,
            "quote": quote,
            "suggestions": suggestions if suggestions else ["以道治身,顺其自然"],
            "focus": "个人修养,自然无为,身心平衡"
        }
    
    def _analyze_from_buddhism(self, situation: Dict) -> Dict[str, Any]:
        """佛家视角分析"""
        description = situation.get("description", "")
        domain = situation.get("domain", DecisionDomain.PERSONAL)
        
        # 确定佛家核心原则
        if "得失" in description or "成败" in description:
            core_teaching = "放下"
            principle = self.buddhism_wisdom["key_teachings"]["let_go"]
            quote = "过去心不可得,现在心不可得,未来心不可得"
        elif "苦难" in description or "困境" in description:
            core_teaching = "四圣谛"
            principle = self.buddhism_wisdom["key_teachings"]["four_truths"]
            quote = "知苦,断集,慕灭,修道"
        elif "人际关系" in description or "矛盾" in description:
            core_teaching = "慈悲"
            principle = self.buddhism_wisdom["key_teachings"]["compassion"]
            quote = "无缘大慈,同体大悲"
        else:
            core_teaching = "空"
            principle = self.buddhism_wisdom["key_teachings"]["emptiness"]
            quote = "诸行无常,诸法无我"
        
        # 佛家建议
        suggestions = []
        if "执念" in description or "纠结" in description:
            suggestions.append("看透放下,自在随缘")
        if "焦虑" in description or "恐惧" in description:
            suggestions.append("因上努力,果上随缘")
        if "伤害" in description or "怨恨" in description:
            suggestions.append("慈悲喜舍,放下怨恨")
        if "传承" in description or "使命" in description:
            suggestions.append("法喜充满,智慧传承")
        
        return {
            "school": WisdomSchool.BUDDHISM,
            "core_teaching": core_teaching,
            "principle": principle,
            "quote": quote,
            "suggestions": suggestions if suggestions else ["以佛治心,心无挂碍"],
            "focus": "心灵解脱,慈悲智慧,超越执念"
        }
    
    def _analyze_three_teachings(
        self, 
        ru: Dict, 
        dao: Dict, 
        buddhism: Dict,
        life_level: LifeLevel
    ) -> ThreeTeachingsBalance:
        """三教平衡分析"""
        # get权重
        weights = self.fusion_rules.get(life_level.value, self.fusion_rules["SOCIAL"])
        
        # 计算得分
        ru_score = 0.5 + len(ru.get("suggestions", [])) * 0.1
        dao_score = 0.5 + len(dao.get("suggestions", [])) * 0.1
        buddhism_score = 0.5 + len(buddhism.get("suggestions", [])) * 0.1
        
        # 归一化
        total = ru_score + dao_score + buddhism_score
        ru_score = ru_score / total * (ru_score / weights["ru"])
        dao_score = dao_score / total * (dao_score / weights["dao"])
        buddhism_score = buddhism_score / total * (buddhism_score / weights["buddhism"])
        
        # 重新归一化到0-1
        total = ru_score + dao_score + buddhism_score
        if total > 0:
            ru_score = ru_score / total
            dao_score = dao_score / total
            buddhism_score = buddhism_score / total
        
        # 确定主导和辅助
        scores = {
            WisdomSchool.RU: ru_score,
            WisdomSchool.DAO: dao_score,
            WisdomSchool.BUDDHISM: buddhism_score
        }
        sorted_schools = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        dominant = sorted_schools[0][0]
        secondary = sorted_schools[1][0] if sorted_schools[1][1] > 0.2 else None
        
        # 计算平衡度
        balance_degree = 1 - abs(ru_score - dao_score) - abs(dao_score - buddhism_score) - abs(buddhism_score - ru_score)
        balance_degree = max(0, min(1, balance_degree))
        
        # generate建议
        harmony_guidance = self.fusion_rules.get(life_level.value, {}).get("guidance", "三家和而不同")
        
        primary_recommendation = f"以{dominant.value}为主,{secondary.value if secondary else '道'}为辅,{harmony_guidance}"
        
        return ThreeTeachingsBalance(
            ru_score=round(ru_score, 3),
            dao_score=round(dao_score, 3),
            buddhism_score=round(buddhism_score, 3),
            dominant_school=dominant,
            secondary_school=secondary,
            balance_degree=round(balance_degree, 3),
            primary_recommendation=primary_recommendation,
            harmony_guidance=harmony_guidance
        )
    
    def _generate_integrated_advice(
        self, 
        domain: DecisionDomain, 
        life_level: LifeLevel,
        balance: ThreeTeachingsBalance
    ) -> List[str]:
        """generatefusion建议"""
        advice = []
        
        # 基于领域
        if domain == DecisionDomain.CAREER:
            advice.append(f"儒家视角:{self.ru_wisdom['adaptation_rules']['CAREER']}")
            advice.append(f"道家视角:{self.dao_wisdom['adaptation_rules']['CAREER']}")
            advice.append(f"佛家视角:{self.buddhism_wisdom['adaptation_rules']['CAREER']}")
        elif domain == DecisionDomain.CULTURE:
            # 文化品牌专项:文化奢侈品
            advice.append("[文化品牌]以儒治世:传承传统文化,以德化人")
            advice.append("[文化品牌]以道治身:天人合一,自然之道")
            advice.append("[文化品牌]以佛治心:心境合一,温润如玉")
        else:
            advice.append(f"儒家视角:{self.ru_wisdom['adaptation_rules'][domain.value]}")
            advice.append(f"道家视角:{self.dao_wisdom['adaptation_rules'][domain.value]}")
            advice.append(f"佛家视角:{self.buddhism_wisdom['adaptation_rules'][domain.value]}")
        
        # 基于平衡
        if balance.dominant_school == WisdomSchool.RU:
            advice.append(f"主导智慧:儒家 - {balance.primary_recommendation}")
        elif balance.dominant_school == WisdomSchool.DAO:
            advice.append(f"主导智慧:道家 - {balance.primary_recommendation}")
        else:
            advice.append(f"主导智慧:佛家 - {balance.primary_recommendation}")
        
        return advice
    
    def _get_wisdom_source(self, domain: DecisionDomain) -> str:
        """get智慧来源"""
        if domain == DecisionDomain.CULTURE:
            return "儒释道三家fusion + 文化品牌传承"
        return "儒释道三家fusion智慧"
    
    def _get_expected_outcome(self, domain: DecisionDomain, balance: ThreeTeachingsBalance) -> str:
        """get预期结果"""
        if domain == DecisionDomain.CULTURE:
            return "文化传承与商业成功并重,德艺双馨,基业长青"
        
        base_outcomes = {
            DecisionDomain.CAREER: "事业有成,德才兼备",
            DecisionDomain.RELATIONSHIP: "人际和谐,各得其所",
            DecisionDomain.PERSONAL: "身心合一,自在圆满",
            DecisionDomain.CRISIS: "转危为机,否极泰来"
        }
        return base_outcomes.get(domain, "诸事顺遂")
    
    def _get_immediate_action(self, domain: DecisionDomain, balance: ThreeTeachingsBalance) -> str:
        """get立即action"""
        if balance.dominant_school == WisdomSchool.RU:
            return "以儒家原则为立即action指南:克己复礼,正心诚意"
        elif balance.dominant_school == WisdomSchool.DAO:
            return "以道家智慧为立即action指南:致虚守静,顺势而为"
        else:
            return "以佛家心态为立即action指南:放下执念,因上努力"
    
    def _get_medium_term_action(self, domain: DecisionDomain, balance: ThreeTeachingsBalance) -> str:
        """get中期规划"""
        if balance.dominant_school == WisdomSchool.RU:
            return "修身齐家:完善制度,培养团队,稳固根基"
        elif balance.dominant_school == WisdomSchool.DAO:
            return "道法自然:循序渐进,不急不躁,水到渠成"
        else:
            return "戒定慧三学:持续修行,智慧增长,慈悲喜舍"
    
    def _get_long_term_direction(self, domain: DecisionDomain, balance: ThreeTeachingsBalance) -> str:
        """get长期方向"""
        if domain == DecisionDomain.CULTURE:
            return "传承与创新并重,以文化立品牌,以匠心铸未来"
        return "三家和而不同,终归于中道,止于至善"
    
    def _get_ru_warnings(self, situation: Dict) -> List[str]:
        """儒家警示"""
        warnings = []
        description = situation.get("description", "")
        
        if "唯利" in description:
            warnings.append("⚠️ 儒家警示:见利忘义,有违君子之道")
        if "傲慢" in description:
            warnings.append("⚠️ 儒家警示:骄傲自大,有失礼数")
        if "不仁" in description:
            warnings.append("⚠️ 儒家警示:仁者爱人,不可不仁")
        
        return warnings if warnings else ["✅ 儒家视角暂无明显警示"]
    
    def _get_dao_warnings(self, situation: Dict) -> List[str]:
        """道家警示"""
        warnings = []
        description = situation.get("description", "")
        
        if "妄为" in description or "强求" in description:
            warnings.append("⚠️ 道家警示:强取妄为,有违自然之道")
        if "贪欲" in description or "过度" in description:
            warnings.append("⚠️ 道家警示:贪得无厌,不知止足")
        if "争强" in description:
            warnings.append("⚠️ 道家警示:争强好胜,天下莫能与之争")
        
        return warnings if warnings else ["✅ 道家视角暂无明显警示"]
    
    def _get_buddhism_warnings(self, situation: Dict) -> List[str]:
        """佛家警示"""
        warnings = []
        description = situation.get("description", "")
        
        if "执念" in description or "执着" in description:
            warnings.append("⚠️ 佛家警示:执着不放,烦恼自生")
        if "嗔恨" in description or "怨恨" in description:
            warnings.append("⚠️ 佛家警示:嗔恨炽盛,心火燃烧")
        if "愚痴" in description or "盲目" in description:
            warnings.append("⚠️ 佛家警示:无明愚痴,不见实相")
        
        return warnings if warnings else ["✅ 佛家视角暂无明显警示"]
    
    # ═══════════════════════════════════════════════════════════════
    # 分领域指导
    # ═══════════════════════════════════════════════════════════════
    
    def get_domain_guidance(self, domain: DecisionDomain) -> Dict[str, Any]:
        """get分领域指导"""
        guidance_map = {
            DecisionDomain.CAREER: {
                "title": "事业领域三教智慧",
                "ru": self.ru_wisdom["decision_principles"]["strategy"],
                "dao": self.dao_wisdom["decision_principles"]["strategy"],
                "buddhism": self.buddhism_wisdom["decision_principles"]["strategy"],
                "integration": "义利并重,顺势而为,因上努力"
            },
            DecisionDomain.CULTURE: {
                "title": "文化使命领域三教智慧[文化品牌专项]",
                "ru": "以德化人,传承有序,礼乐文明",
                "dao": "道法自然,天人合一,返璞归真",
                "buddhism": "法喜充满,慈悲喜舍,智慧传承",
                "integration": "以儒立德,以道修身,以佛养心,三家fusion,文化传世"
            }
        }
        return guidance_map.get(domain, guidance_map[DecisionDomain.CAREER])
    
    # ═══════════════════════════════════════════════════════════════
    # 系统集成
    # ═══════════════════════════════════════════════════════════════
    
    def integrate_with_reasoning(self, reasoning_chain: List[Dict]) -> Dict[str, Any]:
        """将儒释道fusion智慧融入推理链"""
        enhanced_chain = []
        
        for step in reasoning_chain:
            situation = {
                "description": step.get("content", ""),
                "domain": DecisionDomain.PERSONAL,
                "life_level": LifeLevel.SOCIAL
            }
            
            decision = self.make_fusion_decision(situation)
            
            enhanced_step = {
                **step,
                "three_teachings_wisdom": {
                    "dominant": decision.three_teachings_balance.dominant_school.value,
                    "secondary": decision.three_teachings_balance.secondary_school.value if decision.three_teachings_balance.secondary_school else None,
                    "balance": decision.three_teachings_balance.balance_degree,
                    "integrated_advice": decision.integrated_advice[:2]
                }
            }
            
            enhanced_chain.append(enhanced_step)
        
        return {
            "original_chain": reasoning_chain,
            "enhanced_chain": enhanced_chain,
            "overall_balance": sum(
                s["three_teachings_wisdom"]["balance"]
                for s in enhanced_chain
            ) / len(enhanced_chain) if enhanced_chain else 0
        }
    
    def get_wisdom_summary(self) -> Dict[str, Any]:
        """get三教fusion智慧概要"""
        return {
            "title": "儒释道三家fusion智慧体系",
            "subtitle": "以儒治世,以道治身,以佛治心",
            "three_schools": {
                "ru": {
                    "name": "儒家",
                    "focus": "社会秩序,人伦关系,经世致用",
                    "core": "仁,义,礼,智,信"
                },
                "dao": {
                    "name": "道家",
                    "focus": "个人修养,自然无为,身心平衡",
                    "core": "道法自然,无为而治,柔弱不争"
                },
                "buddhism": {
                    "name": "佛家",
                    "focus": "心灵解脱,慈悲智慧,超越执念",
                    "core": "四圣谛,八正道,慈悲喜舍"
                }
            },
            "fusion_principle": "三家和而不同,共同构成中华文明精神支柱",
            "adaptation": {
                "PHYSICAL": "物质层面:道家顺势,儒家规范,佛家放下",
                "SOCIAL": "社会层面:儒家为主,道家为辅,佛家超脱",
                "SPIRITUAL": "精神层面:三家平衡,归于中道",
                "TRANSCENDENT": "超越层面:佛家为主,道家为辅,儒家补位"
            }
        }

# 全局实例
_fusion_engine: Optional[ConfucianBuddhistDaoFusion] = None

def get_fusion_engine() -> ConfucianBuddhistDaoFusion:
    """get儒释道fusion引擎实例"""
    global _fusion_engine
    if _fusion_engine is None:
        _fusion_engine = ConfucianBuddhistDaoFusion()
    return _fusion_engine

__all__ = [
    'ConfucianBuddhistDaoFusion',
    'FusionDecision',
    'ThreeTeachingsBalance',
    'WisdomSchool',
    'DecisionDomain',
    'LifeLevel',
    'get_fusion_engine'
]
