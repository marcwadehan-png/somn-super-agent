# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze_suffering',
    'cultivate_immeasurables',
    'evaluate_karma',
    'get_wisdom',
    'make_decision',
    'recommend_practice',
]

佛家智慧核心模块 v1.0.0
Buddha Wisdom Core Module

版本:v1.0.0
更新:2026-04-02
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

class FourNobleTruths(Enum):
    """四圣谛"""
    KU = "苦谛"      # 世间一切皆苦
    JI = "集谛"      # 苦的根源是贪嗔痴
    MIE = "灭谛"     # 断除烦恼达到涅槃
    DAO = "道谛"     # 通往解脱的修行方法

class EightfoldPath(Enum):
    """八正道 - 通往涅槃的八种正确途径"""
    ZHENGJIAN = "正见"      # 正确理解四圣谛,因果,无常,无我
    ZHENGSI = "正思维"      # 远离贪嗔,进行如理思维
    ZHENGYU = "正语"        # 戒除妄语,两舌,恶口,绮语
    ZHENGYE = "正业"        # 行为端正,不杀生,不偷盗,不邪淫
    ZHENGMING = "正命"      # 以合法,不损害众生的方式谋生
    ZHENGJING = "正精进"    # 勤修善法,断恶修善
    ZHENGNIAN = "正念"      # 保持觉知,如实观察身心现象
    ZHENGDING = "正定"      # 修习禅定,心专注一境

class ThreeDharmaSeals(Enum):
    """三法印 - 验证佛法真伪的三个标准"""
    WUCHANG = "诸行无常"    # 一切现象皆无常变化
    WUWO = "诸法无我"       # 一切现象无独立自性
    JING = "涅槃寂静"       # 涅槃是寂静解脱的境界

class SixParamitas(Enum):
    """六度 - 六种修行方法"""
    BUSHI = "布施"      # 给予,分享
    CHIJIE = "持戒"     # 遵守戒律
    RENRU = "忍辱"      # 忍受苦难
    JINGJIN = "精进"    # 勤奋修行
    CHANDING = "禅定"   # 冥想专注
    BORE = "般若"       # 智慧觉悟

class FourImmeasurables(Enum):
    """四无量心 - 慈悲喜舍"""
    CI = "慈"      # 慈爱,愿众生得乐
    BEI = "悲"      # 悲悯,愿众生离苦
    XI = "喜"       # 随喜,见众生得乐而喜
    SHE = "舍"      # 舍离,平等心,无执着

@dataclass
class BuddhaDecision:
    """佛家decision结构"""
    primary_truth: FourNobleTruths      # 主要basis圣谛
    primary_path: EightfoldPath          # 主要修行路径
    reasoning: str                        # 推理过程
    action: str                            # action建议
    wisdom_source: str                     # 智慧来源(佛经原文)
    attachment_level: float               # 执着程度评估(0-1)
    suffering_level: float                # 痛苦程度评估(0-1)
    liberation_potential: float           # 解脱潜力(0-1)
    recommendations: List[str]            # 修行建议
    warnings: List[str]                   # 警示

@dataclass
class BuddhaPersona:
    """佛家修行者人格"""
    # 八正道修行程度
    zhengjian_level: float = 0.5    # 正见
    zhengsi_level: float = 0.5      # 正思维
    zhengyu_level: float = 0.5      # 正语
    zhengye_level: float = 0.5      # 正业
    zhengming_level: float = 0.5    # 正命
    zhengjing_level: float = 0.5    # 正精进
    zhengnian_level: float = 0.5    # 正念
    zhengding_level: float = 0.5    # 正定
    
    # 六度修行
    bushi_level: float = 0.5        # 布施
    chijie_level: float = 0.5       # 持戒
    renru_level: float = 0.5        # 忍辱
    jingjin_level: float = 0.5      # 精进
    chanding_level: float = 0.5     # 禅定
    bore_level: float = 0.5         # 般若
    
    # 四无量心
    ci_level: float = 0.5           # 慈
    bei_level: float = 0.5          # 悲
    xi_level: float = 0.5           # 喜
    she_level: float = 0.5          # 舍
    
    # 执着程度
    attachment_to_wealth: float = 0.5    # 对财富的执着
    attachment_to_fame: float = 0.5      # 对名利的执着
    attachment_to_relationships: float = 0.5  # 对关系的执着
    attachment_to_views: float = 0.5     # 对见解的执着
    
    # 修行层级
    cultivation_level: int = 1      # 1-10级

class BuddhaWisdomCore:
    """
    佛家智慧核心引擎
    
    将佛教核心教义融入智能decision:
    1. 四圣谛 - 认识苦,断除集,证得灭,修习道
    2. 八正道 - 修行的八种正确途径
    3. 缘起性空 - 诸法因缘生,无独立自性
    4. 三法印 - 验证真理的标准
    5. 六度 - 菩萨修行的六种方法
    6. 四无量心 - 慈悲喜舍的广大心量
    """
    
    def __init__(self):
        """init佛家智慧核心"""
        self.name = "BuddhaWisdomCore"
        self.version="6.2.0"
        
        # 四圣谛详解
        self.four_truths = {
            FourNobleTruths.KU: {
                "description": "世间一切皆苦",
                "eight_sufferings": [
                    "生苦 - 出生之苦",
                    "老苦 - 衰老之苦", 
                    "病苦 - 疾病之苦",
                    "死苦 - 死亡之苦",
                    "爱别离苦 - 与所爱分离之苦",
                    "怨憎会苦 - 与所憎相遇之苦",
                    "求不得苦 - 求而不得之苦",
                    "五阴炽盛苦 - 身心烦恼之苦"
                ],
                "three_sufferings": [
                    "苦苦 - 直接的痛苦",
                    "坏苦 - 快乐消逝的痛苦",
                    "行苦 - 无常变迁的痛苦"
                ],
                "quote": "一切皆苦,诸行无常",
                "source": "<阿含经>"
            },
            FourNobleTruths.JI: {
                "description": "苦的根源是贪嗔痴",
                "root_causes": [
                    "贪 - 贪欲,执着",
                    "嗔 - 愤怒,憎恨",
                    "痴 - 无明,迷惑"
                ],
                "twelve_links": [
                    "无明", "行", "识", "名色", "六入", "触",
                    "受", "爱", "取", "有", "生", "老死"
                ],
                "quote": "此有故彼有,此生故彼生",
                "source": "<缘起经>"
            },
            FourNobleTruths.MIE: {
                "description": "断除烦恼达到涅槃",
                "nirvana_types": [
                    "有余涅槃 - 断除烦恼,仍有身体",
                    "无余涅槃 - 断除烦恼,身体亦灭"
                ],
                "characteristics": [
                    "寂静 - 无烦恼扰动",
                    "清凉 - 无热恼之苦",
                    "安稳 - 无动摇之惧",
                    "解脱 - 无束缚之累"
                ],
                "quote": "涅槃寂静,常恒不变",
                "source": "<涅槃经>"
            },
            FourNobleTruths.DAO: {
                "description": "通往解脱的修行方法",
                "eightfold_path": "八正道",
                "thirty_seven_practices": "三十七道品",
                "quote": "八正道是通往涅槃的唯一道路",
                "source": "<转法轮经>"
            }
        }
        
        # 八正道详解
        self.eightfold_path = {
            EightfoldPath.ZHENGJIAN: {
                "meaning": "正确理解四圣谛,因果,无常,无我",
                "practice": "学习佛法,建立正确的世界观",
                "quote": "正见为首,如目导行"
            },
            EightfoldPath.ZHENGSI: {
                "meaning": "远离贪嗔,进行如理思维",
                "practice": "培养善念,断除恶念",
                "quote": "正思维者,离欲思维"
            },
            EightfoldPath.ZHENGYU: {
                "meaning": "戒除妄语,两舌,恶口,绮语",
                "practice": "说真实语,和合语,柔软语,利益语",
                "quote": "正语清净,口业庄严"
            },
            EightfoldPath.ZHENGYE: {
                "meaning": "行为端正,不杀生,不偷盗,不邪淫",
                "practice": "持守五戒,行为清净",
                "quote": "正业清净,身业庄严"
            },
            EightfoldPath.ZHENGMING: {
                "meaning": "以合法,不损害众生的方式谋生",
                "practice": "远离五种邪命",
                "quote": "正命清净,生活如法"
            },
            EightfoldPath.ZHENGJING: {
                "meaning": "勤修善法,断恶修善",
                "practice": "四正勤:未生恶令不生,已生恶令断,未生善令生,已生善令增长",
                "quote": "正精进者,勇猛不懈"
            },
            EightfoldPath.ZHENGNIAN: {
                "meaning": "保持觉知,如实观察身心现象",
                "practice": "四念处:观身不净,观受是苦,观心无常,观法无我",
                "quote": "正念安住,如实观察"
            },
            EightfoldPath.ZHENGDING: {
                "meaning": "修习禅定,心专注一境",
                "practice": "四禅八定,心一境性",
                "quote": "正定清净,心得解脱"
            }
        }
        
        # 三法印详解
        self.three_seals = {
            ThreeDharmaSeals.WUCHANG: {
                "meaning": "一切现象皆无常变化",
                "implication": "没有永恒不变的事物",
                "practice": "观察无常,减少对事物的执着",
                "quote": "诸行无常,是生灭法"
            },
            ThreeDharmaSeals.WUWO: {
                "meaning": "一切现象无独立自性",
                "implication": "没有永恒不变的自我",
                "practice": "观察无我,减少我执",
                "quote": "诸法无我,寂静涅槃"
            },
            ThreeDharmaSeals.JING: {
                "meaning": "涅槃是寂静解脱的境界",
                "implication": "解脱是可能的",
                "practice": "修习正道,趋向涅槃",
                "quote": "涅槃寂静,究竟圆满"
            }
        }
        
        # 六度详解
        self.six_paramitas = {
            SixParamitas.BUSHI: {
                "meaning": "给予,分享",
                "types": ["财布施", "法布施", "无畏布施"],
                "benefit": "破除悭贪,培养慷慨",
                "quote": "布施者,破悭贪之贼"
            },
            SixParamitas.CHIJIE: {
                "meaning": "遵守戒律",
                "types": ["五戒", "八戒", "十戒", "具足戒"],
                "benefit": "防非止恶,行为规范",
                "quote": "持戒者,防非止恶"
            },
            SixParamitas.RENRU: {
                "meaning": "忍受苦难",
                "types": ["生忍", "法忍", "无生法忍"],
                "benefit": "培养耐心,化解嗔恨",
                "quote": "忍辱者,嗔心不起"
            },
            SixParamitas.JINGJIN: {
                "meaning": "勤奋修行",
                "types": ["披甲精进", "摄善法精进", "利乐精进"],
                "benefit": "破除懈怠,勇猛修行",
                "quote": "精进者,懈怠不生"
            },
            SixParamitas.CHANDING: {
                "meaning": "冥想专注",
                "types": ["四禅", "四无色定", "灭尽定"],
                "benefit": "心得安定,开发智慧",
                "quote": "禅定者,心不散乱"
            },
            SixParamitas.BORE: {
                "meaning": "智慧觉悟",
                "types": ["生空智", "法空智", "一切智智"],
                "benefit": "破除愚痴,开发智慧",
                "quote": "般若者,烦恼永断"
            }
        }
        
        # 四无量心详解
        self.four_immeasurables = {
            FourImmeasurables.CI: {
                "meaning": "慈爱,愿众生得乐",
                "practice": "愿一切众生得乐",
                "benefit": "对治嗔恨",
                "quote": "慈能与乐"
            },
            FourImmeasurables.BEI: {
                "meaning": "悲悯,愿众生离苦",
                "practice": "愿一切众生离苦",
                "benefit": "对治残忍",
                "quote": "悲能拔苦"
            },
            FourImmeasurables.XI: {
                "meaning": "随喜,见众生得乐而喜",
                "practice": "见众生得乐,心生欢喜",
                "benefit": "对治嫉妒",
                "quote": "喜能除嫉"
            },
            FourImmeasurables.SHE: {
                "meaning": "舍离,平等心,无执着",
                "practice": "对一切众生,平等看待",
                "benefit": "对治贪嗔",
                "quote": "舍能离执"
            }
        }
    
    def analyze_suffering(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析情境中的苦(苦谛分析)
        
        Args:
            situation: 情境描述
            
        Returns:
            苦的分析结果
        """
        suffering_types = []
        suffering_score = 0.0
        
        # 分析八苦
        if situation.get("loss"):
            suffering_types.append("爱别离苦")
            suffering_score += 0.15
        if situation.get("conflict"):
            suffering_types.append("怨憎会苦")
            suffering_score += 0.15
        if situation.get("unfulfilled_desire"):
            suffering_types.append("求不得苦")
            suffering_score += 0.15
        if situation.get("change"):
            suffering_types.append("行苦")
            suffering_score += 0.1
        if situation.get("physical_pain"):
            suffering_types.append("苦苦")
            suffering_score += 0.2
        
        # 分析根源
        root_causes = []
        if situation.get("greed"):
            root_causes.append("贪")
        if situation.get("anger"):
            root_causes.append("嗔")
        if situation.get("confusion"):
            root_causes.append("痴")
        
        return {
            "suffering_types": suffering_types,
            "suffering_score": min(suffering_score, 1.0),
            "root_causes": root_causes,
            "analysis": f"当前情境主要涉及{len(suffering_types)}种苦,根源在于{', '.join(root_causes) if root_causes else '无明'}"
        }
    
    def recommend_practice(self, persona: BuddhaPersona, situation: Dict[str, Any]) -> List[str]:
        """
        推荐修行方法
        
        Args:
            persona: 修行者人格
            situation: 情境描述
            
        Returns:
            修行建议列表
        """
        recommendations = []
        
        # 根据执着程度推荐
        if situation.get("attachment_to_wealth", 0) > 0.6:
            recommendations.append("修习布施,破除对财富的执着")
        if situation.get("attachment_to_fame", 0) > 0.6:
            recommendations.append("修习忍辱,看破名利的虚幻")
        if situation.get("attachment_to_relationships", 0) > 0.6:
            recommendations.append("修习禅定,观察缘起性空")
        
        # 根据痛苦程度推荐
        if situation.get("suffering_level", 0) > 0.7:
            recommendations.append("修习四念处,如实观察身心现象")
            recommendations.append("修习慈悲喜舍,培养广大心量")
        
        # 根据修行程度推荐
        if persona.cultivation_level < 3:
            recommendations.append("从五戒十善开始,打好基础")
        elif persona.cultivation_level < 6:
            recommendations.append("修习四念处,培养正念")
        else:
            recommendations.append("修习六度,利益众生")
        
        return recommendations
    
    def make_decision(self, situation: Dict[str, Any], persona: Optional[BuddhaPersona] = None) -> BuddhaDecision:
        """
        基于佛家智慧做出decision
        
        Args:
            situation: decision情境
            persona: 修行者人格(可选)
            
        Returns:
            佛家decision结果
        """
        if persona is None:
            persona = BuddhaPersona()
        
        # 分析苦
        suffering_analysis = self.analyze_suffering(situation)
        
        # 确定主要圣谛
        if suffering_analysis["suffering_score"] > 0.7:
            primary_truth = FourNobleTruths.KU
            primary_path = EightfoldPath.ZHENGNIAN
            reasoning = "当前情境苦重,应先认识苦的本质,修习正念"
        elif suffering_analysis["root_causes"]:
            primary_truth = FourNobleTruths.JI
            primary_path = EightfoldPath.ZHENGJIAN
            reasoning = "苦的根源已明,应修习正见,断除贪嗔痴"
        else:
            primary_truth = FourNobleTruths.DAO
            primary_path = EightfoldPath.ZHENGJING
            reasoning = "应在日常生活中修习正道,精进不懈"
        
        # generateaction建议
        action = self._generate_action(primary_path, situation)
        
        # get智慧来源
        wisdom_source = self.eightfold_path[primary_path]["quote"]
        
        # 评估执着程度
        attachment_level = max(
            situation.get("attachment_to_wealth", 0),
            situation.get("attachment_to_fame", 0),
            situation.get("attachment_to_relationships", 0),
            situation.get("attachment_to_views", 0)
        )
        
        # 评估解脱潜力
        liberation_potential = 1.0 - attachment_level
        
        # generate修行建议
        recommendations = self.recommend_practice(persona, situation)
        
        # generate警示
        warnings = []
        if attachment_level > 0.7:
            warnings.append("执着深重,易生烦恼")
        if suffering_analysis["suffering_score"] > 0.7:
            warnings.append("痛苦剧烈,需及时修行")
        
        return BuddhaDecision(
            primary_truth=primary_truth,
            primary_path=primary_path,
            reasoning=reasoning,
            action=action,
            wisdom_source=wisdom_source,
            attachment_level=attachment_level,
            suffering_level=suffering_analysis["suffering_score"],
            liberation_potential=liberation_potential,
            recommendations=recommendations,
            warnings=warnings
        )
    
    def _generate_action(self, path: EightfoldPath, situation: Dict[str, Any]) -> str:
        """generateaction建议"""
        path_actions = {
            EightfoldPath.ZHENGJIAN: "学习佛法,建立正见,正确认识事物的本质",
            EightfoldPath.ZHENGSI: "培养善念,断除贪嗔痴等恶念",
            EightfoldPath.ZHENGYU: "说真实语,避免妄语,两舌,恶口,绮语",
            EightfoldPath.ZHENGYE: "行为端正,持守五戒,不伤害众生",
            EightfoldPath.ZHENGMING: "以正当方式谋生,远离邪命",
            EightfoldPath.ZHENGJING: "勤修善法,断恶修善,勇猛精进",
            EightfoldPath.ZHENGNIAN: "保持正念,如实观察身心现象",
            EightfoldPath.ZHENGDING: "修习禅定,令心得定,开发智慧"
        }
        return path_actions.get(path, "修习八正道,趋向解脱")
    
    def evaluate_karma(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估业力的善恶
        
        Args:
            action: 行为描述
            
        Returns:
            业力评估结果
        """
        karma_score = 0.0
        karma_type = ""
        
        # 评估十善业/十恶业
        if action.get("killing"):
            karma_score -= 1.0
            karma_type = "恶业"
        if action.get("stealing"):
            karma_score -= 0.8
            karma_type = "恶业"
        if action.get("sexual_misconduct"):
            karma_score -= 0.8
            karma_type = "恶业"
        if action.get("lying"):
            karma_score -= 0.6
            karma_type = "恶业"
        if action.get("generosity"):
            karma_score += 1.0
            karma_type = "善业"
        if action.get("kindness"):
            karma_score += 0.8
            karma_type = "善业"
        if action.get("truthfulness"):
            karma_score += 0.6
            karma_type = "善业"
        
        return {
            "karma_score": karma_score,
            "karma_type": karma_type,
            "result": "善有善报,恶有恶报" if karma_score > 0 else "当断恶业,修习善业"
        }
    
    def cultivate_immeasurables(self, target: str = "all_beings") -> Dict[str, Any]:
        """
        修习四无量心
        
        Args:
            target: 修习对象
            
        Returns:
            修习指导
        """
        return {
            "target": target,
            "practices": {
                "慈": f"愿{target}得乐",
                "悲": f"愿{target}离苦",
                "喜": f"见{target}得乐,心生欢喜",
                "舍": f"对{target}平等看待,无分别心"
            },
            "benefits": "对治贪嗔,培养广大心量",
            "quote": "慈悲喜舍,无量无边"
        }
    
    def get_wisdom(self, topic: str) -> str:
        """
        get佛家智慧
        
        Args:
            topic: 主题
            
        Returns:
            智慧箴言
        """
        wisdom_dict = {
            "苦": "一切皆苦,诸行无常",
            "空": "诸法因缘生,诸法因缘灭",
            "无我": "诸法无我,寂静涅槃",
            "因果": "种善因得善果,种恶因得恶果",
            "修行": "诸恶莫作,众善奉行,自净其意",
            "智慧": "般若波罗蜜,能除一切苦",
            "慈悲": "慈能与乐,悲能拔苦",
            "放下": "应无所住而生其心",
            "当下": "过去心不可得,现在心不可得,未来心不可得",
            "解脱": "涅槃寂静,究竟圆满"
        }
        return wisdom_dict.get(topic, "诸法因缘生,诸法因缘灭")

# ============================================================
# 使用示例
# ============================================================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
