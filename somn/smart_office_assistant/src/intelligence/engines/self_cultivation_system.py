# -*- coding: utf-8 -*-
"""
__all__ = [
    'apply_to_decision',
    'assess_cultivation',
    'get_cultivation_system',
    'get_guidance',
    'track_progress',
]

修身齐家系统 v1.0.0
=====================

基于<大学>与<论语>的君子修身系统

核心思想:
- <大学>:格物→致知→正心→诚意→修身→齐家→治国→平天下
- <论语>君子标准:仁,智,勇三达德
- 修身次第:从内圣到外王

版本:v1.0.0
更新:2026-04-02
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

class CultivationLevel(Enum):
    """修养层级"""
    WEIMIN = "愚昧"           # 格物致知阶段
    XUEZHE = "学者"           # 开始学习
    JUREN = "居仁"            # 心中有仁
    YIZHE = "义士"            # 行为合义
    WENZHE = "文哲"           # 学识渊博
    JUNZI = "君子"            # 君子境界
    XIANREN = "贤人"          # 贤者
    RUSHENG = "儒圣"          # 儒学圣人

class CultivationStep(Enum):
    """大学八条目"""
    GEWU = "格物"     # 穷究事物之理
    ZHIZHI = "致知"    # 获得知识
    CHENGYI = "诚意"   # 意念真诚
    ZHENGXIN = "正心"  # 心地端正
    XIUSHEN = "修身"   # 修养身心
    QIUJIA = "齐家"   # 治理家庭
    ZHIGUO = "治国"   # 治理国家
    PINGTIANXIA = "平天下"  # 天下太平

@dataclass
class CultivationProgress:
    """修养进度"""
    current_step: CultivationStep
    current_level: CultivationLevel
    gewo_score: float = 0.5    # 格物
    zhizhi_score: float = 0.5   # 致知
    chengyi_score: float = 0.5  # 诚意
    zhengxin_score: float = 0.5 # 正心
    xiushen_score: float = 0.5 # 修身
    qiujia_score: float = 0.5  # 齐家
    zhiguo_score: float = 0.5   # 治国
    pingtianxia_score: float = 0.5  # 平天下

    # 君子三德
    ren_score: float = 0.5  # 仁
    zhi_score: float = 0.5  # 智
    yong_score: float = 0.5  # 勇

    # 修身进度
    progress_percentage: float = 0.0
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

class SelfCultivationSystem:
    """
    修身齐家系统

    基于<大学>的八条目修养次第:
    ┌─────────────────────────────────────────┐
    │         大学八条目修养次第                │
    ├─────────────────────────────────────────┤
    │  格物 → 致知 → 诚意 → 正心               │
    │    ↓                           ↑        │
    │  平天下 ← 治国 ← 齐家 ←── 修身 ──┘       │
    └─────────────────────────────────────────┘

    核心功能:
    - assess_cultivation() - 评估当前修养水平
    - get_guidance() - get修身指导
    - track_progress() - 追踪进步
    - apply_to_decision() - 修身应用于decision
    """

    def __init__(self):
        """init修身系统"""
        self.name = "SelfCultivationSystem"
        self.version = "v1.0.0"

        # 大学原文
        self.daxue_text = {
            "开篇": "大学之道,在明明德,在亲民,在止于至善.",
            "格物致知": "致知在格物,物格而后知至,知至而后意诚.",
            "诚意正心": "欲正其心者,先诚其意;欲诚其意者,先致其知.",
            "修身": "欲修其身者,先正其心;欲正其心者,先诚其意.",
            "齐家": "欲齐其家者,先修其身;欲修其身者,先正其心.",
            "治国": "欲治其国者,先齐其家;欲齐其家者,先修其身.",
            "平天下": "欲平天下者,先治其国;欲治其国者,先齐其家.",
            "本末": "物有本末,事有终始,知所先后,则近道矣."
        }

        # 论语君子标准
        self.junzi_standards = {
            "仁": [
                "仁者不忧",
                "仁者爱人",
                "克己复礼为仁",
                "己所不欲,勿施于人",
                "为政以德"
            ],
            "智": [
                "知者不惑",
                "知之为知之,不知为不知",
                "学而不思则罔,思而不学则殆",
                "温故而知新",
                "多闻阙疑,慎言其余"
            ],
            "勇": [
                "勇者不惧",
                "见义不为,无勇也",
                "当仁不让于师",
                "杀身成仁",
                "三军可夺帅也,匹夫不可夺志也"
            ]
        }

        # 君子九思
        self.jiusi = {
            "视思明": "看要看得清楚分明,不被表象迷惑",
            "听思聪": "听要听得明白清楚,不被谗言误导",
            "色思温": "脸色要温和,不喜怒无常",
            "貌思恭": "容貌要恭敬,不傲慢无礼",
            "言思忠": "说话要忠诚,不口是心非",
            "事思敬": "做事要谨慎,不敷衍了事",
            "疑思问": "有疑问要请教,不自以为是",
            "忿思难": "愤怒时要想到后果,不冲动行事",
            "见得思义": "见到利益要想到是否合义,不取不义之财"
        }

        # 君子三戒
        self.sanjie = {
            "少之时戒之在色": "年少时戒除色欲,保护精气神",
            "壮之时戒之在斗": "壮年时戒除争斗,避免惹祸上身",
            "老之时戒之在得": "年老时戒除贪得,防止晚节不保"
        }

        # 当前进度(简化存储)
        self.progress = CultivationProgress(
            current_step=CultivationStep.GEWU,
            current_level=CultivationLevel.XUEZHE,
            progress_percentage=0.0
        )

    def assess_cultivation(self, person_data: Dict) -> CultivationProgress:
        """
        评估个人修养水平

        Args:
            person_data: 个人数据,包含:
                - knowledge_level: 学识水平
                - moral_actions: 道德行为
                - social_relations: 社会关系
                - self_reflection: 自我反省

        Returns:
            CultivationProgress: 修养评估结果
        """
        # 评估各维度
        self.progress.gewo_score = self._assess_gewo(person_data)
        self.progress.zhizhi_score = self._assess_zhizhi(person_data)
        self.progress.chengyi_score = self._assess_chengyi(person_data)
        self.progress.zhengxin_score = self._assess_zhengxin(person_data)
        self.progress.xiushen_score = self._assess_xiushen(person_data)

        # 君子三德评估
        self.progress.ren_score = person_data.get("仁", 0.5)
        self.progress.zhi_score = person_data.get("智", 0.5)
        self.progress.yong_score = person_data.get("勇", 0.5)

        # 确定当前层级
        avg_score = (
            self.progress.ren_score +
            self.progress.zhi_score +
            self.progress.yong_score +
            self.progress.xiushen_score
        ) / 4

        if avg_score >= 0.95:
            self.progress.current_level = CultivationLevel.RUSHENG
        elif avg_score >= 0.85:
            self.progress.current_level = CultivationLevel.XIANREN
        elif avg_score >= 0.75:
            self.progress.current_level = CultivationLevel.JUNZI
        elif avg_score >= 0.65:
            self.progress.current_level = CultivationLevel.WENZHE
        elif avg_score >= 0.55:
            self.progress.current_level = CultivationLevel.YIZHE
        elif avg_score >= 0.45:
            self.progress.current_level = CultivationLevel.JUREN
        elif avg_score >= 0.3:
            self.progress.current_level = CultivationLevel.XUEZHE
        else:
            self.progress.current_level = CultivationLevel.WEIMIN

        # 确定当前步骤
        if self.progress.gewo_score < 0.6:
            self.progress.current_step = CultivationStep.GEWU
        elif self.progress.zhizhi_score < 0.6:
            self.progress.current_step = CultivationStep.ZHIZHI
        elif self.progress.chengyi_score < 0.6:
            self.progress.current_step = CultivationStep.CHENGYI
        elif self.progress.zhengxin_score < 0.6:
            self.progress.current_step = CultivationStep.ZHENGXIN
        elif self.progress.xiushen_score < 0.6:
            self.progress.current_step = CultivationStep.XIUSHEN
        elif self.progress.qiujia_score < 0.6:
            self.progress.current_step = CultivationStep.QIUJIA
        elif self.progress.zhiguo_score < 0.6:
            self.progress.current_step = CultivationStep.ZHIGUO
        else:
            self.progress.current_step = CultivationStep.PINGTIANXIA

        # 计算进度百分比
        self._calculate_progress()

        # 找出优劣势
        self._analyze_strengths_weaknesses()

        # generate建议
        self._generate_suggestions()

        return self.progress

    def _assess_gewo(self, data: Dict) -> float:
        """评估格物(观察学习)"""
        base_score = 0.5

        # 学习态度
        if data.get("好学", False):
            base_score += 0.1
        if data.get("多闻", False):
            base_score += 0.1
        if data.get("博学", False):
            base_score += 0.1

        # 实践经验
        if data.get("实践", False):
            base_score += 0.1

        return min(1.0, base_score)

    def _assess_zhizhi(self, data: Dict) -> float:
        """评估致知(知识get)"""
        base_score = 0.5

        # 知识广度
        if data.get("学识渊博", False):
            base_score += 0.15
        if data.get("专业能力强", False):
            base_score += 0.1

        # 理解深度
        if data.get("理解深刻", False):
            base_score += 0.1

        # 学习方法
        if data.get("学思结合", False):
            base_score += 0.1

        return min(1.0, base_score)

    def _assess_chengyi(self, data: Dict) -> float:
        """评估诚意(意念真诚)"""
        base_score = 0.5

        # 真诚度
        if data.get("真诚待人", False):
            base_score += 0.15
        if data.get("不自欺", False):
            base_score += 0.1

        # 诚实度
        if data.get("诚实守信", False):
            base_score += 0.1

        # 动机纯正
        if data.get("动机纯正", False):
            base_score += 0.1

        return min(1.0, base_score)

    def _assess_zhengxin(self, data: Dict) -> float:
        """评估正心(心地端正)"""
        base_score = 0.5

        # 情绪稳定
        if data.get("情绪稳定", False):
            base_score += 0.1
        if data.get("不喜怒无常", False):
            base_score += 0.1

        # 心态平和
        if data.get("心态平和", False):
            base_score += 0.1

        # 无私心
        if data.get("公正无私", False):
            base_score += 0.15

        return min(1.0, base_score)

    def _assess_xiushen(self, data: Dict) -> float:
        """评估修身(修养身心)"""
        base_score = 0.5

        # 道德行为
        if data.get("仁", False):
            base_score += 0.1
        if data.get("义", False):
            base_score += 0.1
        if data.get("礼", False):
            base_score += 0.1

        # 自律
        if data.get("自律", False):
            base_score += 0.1

        # 反省
        if data.get("吾日三省", False):
            base_score += 0.1

        return min(1.0, base_score)

    def _calculate_progress(self):
        """计算整体进度"""
        total = (
            self.progress.gewo_score * 0.1 +
            self.progress.zhizhi_score * 0.15 +
            self.progress.chengyi_score * 0.15 +
            self.progress.zhengxin_score * 0.15 +
            self.progress.xiushen_score * 0.2 +
            self.progress.qiujia_score * 0.1 +
            self.progress.zhiguo_score * 0.1 +
            self.progress.pingtianxia_score * 0.05
        )

        # 君子三德权重
        junzi_score = (
            self.progress.ren_score * 0.4 +
            self.progress.zhi_score * 0.3 +
            self.progress.yong_score * 0.3
        )

        self.progress.progress_percentage = (total + junzi_score) / 2 * 100

    def _analyze_strengths_weaknesses(self):
        """分析优劣势"""
        scores = {
            "格物": self.progress.gewo_score,
            "致知": self.progress.zhizhi_score,
            "诚意": self.progress.chengyi_score,
            "正心": self.progress.zhengxin_score,
            "修身": self.progress.xiushen_score,
            "仁": self.progress.ren_score,
            "智": self.progress.zhi_score,
            "勇": self.progress.yong_score
        }

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # 取前3为优势
        self.progress.strengths = [item[0] for item in sorted_scores[:3]]

        # 取后3为劣势
        self.progress.weaknesses = [item[0] for item in sorted_scores[-3:]]

    def _generate_suggestions(self):
        """generate修身建议"""
        self.progress.suggestions = []

        # 根据当前步骤建议
        step_suggestions = {
            CultivationStep.GEWU: "宜博学多闻,格物致知,多向他人学习",
            CultivationStep.ZHIZHI: "宜温故知新,学思结合,深化理解",
            CultivationStep.CHENGYI: "宜真诚待人,不自欺欺人意念真诚",
            CultivationStep.ZHENGXIN: "宜心态平和,去除私欲心地端正",
            CultivationStep.XIUSHEN: "宜以身作则,克己复礼修养身心",
            CultivationStep.QIUJIA: "宜孝悌传家,以身示范治理家庭",
            CultivationStep.ZHIGUO: "宜以德治国,任贤使能治理国家",
            CultivationStep.PINGTIANXIA: "宜明明德于天下,平天下在明明德"
        }

        self.progress.suggestions.append(step_suggestions.get(
            self.progress.current_step, "继续努力"
        ))

        # 根据劣势建议
        if "仁" in self.progress.weaknesses:
            self.progress.suggestions.append("宜加强仁爱之心,己所不欲勿施于人")

        if "智" in self.progress.weaknesses:
            self.progress.suggestions.append("宜多学多思,温故知新增长智慧")

        if "勇" in self.progress.weaknesses:
            self.progress.suggestions.append("宜见义勇为,当仁不让培养勇气")

        if "诚意" in self.progress.weaknesses:
            self.progress.suggestions.append("宜真诚不自欺,意念诚实表里如一")

    def get_guidance(self, focus_area: Optional[str] = None) -> Dict[str, Any]:
        """
        get修身指导

        Args:
            focus_area: 重点领域 (nine_thinks/three_cautions/junzi_qualities)

        Returns:
            修身指导
        """
        guidance = {}

        if focus_area is None or focus_area == "nine_thinks":
            guidance["君子九思"] = {
                desc: self.jiusi[desc]
                for desc in self.jiusi
            }

        if focus_area is None or focus_area == "three_cautions":
            guidance["君子三戒"] = self.sanjie

        if focus_area is None or focus_area == "junzi_qualities":
            guidance["君子三德"] = {
                "仁": "仁者不忧,爱人如己",
                "智": "知者不惑,明辨是非",
                "勇": "勇者不惧,见义敢为"
            }

        guidance["当前进度"] = {
            "step": self.progress.current_step.value,
            "level": self.progress.current_level.value,
            "progress": f"{self.progress.progress_percentage:.1f}%"
        }

        guidance["经典引述"] = {
            "大学": self.daxue_text["开篇"],
            "论语": "君子务本,本立而道生"
        }

        return guidance

    def apply_to_decision(self, decision: Dict) -> Dict[str, Any]:
        """
        将修身应用于decision

        Args:
            decision: 待评估的decision

        Returns:
            修身视角的decision评估
        """
        decision_text = str(decision)

        # 评估decision是否符合修身要求
        assessment = {
            "符合君子之道": False,
            "符合中庸之道": False,
            "符合德治思想": False,
            "修身建议": []
        }

        # 检查仁义礼智信
        if any(kw in decision_text for kw in ["爱", "仁", "关怀"]):
            assessment["符合君子之道"] = True

        if any(kw in decision_text for kw in ["义", "正当", "公正"]):
            assessment["符合君子之道"] = True

        if any(kw in decision_text for kw in ["和", "和为贵", "中"]):
            assessment["符合中庸之道"] = True

        if any(kw in decision_text for kw in ["德", "任贤", "以德"]):
            assessment["符合德治思想"] = True

        # 根据当前进度给出建议
        if self.progress.current_step.value in ["格物", "致知"]:
            assessment["修身建议"].append("宜先充实学识,再做重大decision")

        if self.progress.current_step.value in ["诚意", "正心"]:
            assessment["修身建议"].append("宜先审视动机是否纯正")

        if self.progress.xiushen_score < 0.6:
            assessment["修身建议"].append("修身不足,宜先修养自身")

        return assessment

    def track_progress(self, new_data: Dict) -> Dict[str, Any]:
        """
        追踪进步

        Args:
            new_data: 新的修养数据

        Returns:
            进步报告
        """
        old_progress = CultivationProgress(
            current_step=self.progress.current_step,
            current_level=self.progress.current_level,
            gewo_score=self.progress.gewo_score,
            zhizhi_score=self.progress.zhizhi_score,
            chengyi_score=self.progress.chengyi_score,
            zhengxin_score=self.progress.zhengxin_score,
            xiushen_score=self.progress.xiushen_score,
            ren_score=self.progress.ren_score,
            zhi_score=self.progress.zhi_score,
            yong_score=self.progress.yong_score
        )

        # 重新评估
        self.assess_cultivation(new_data)

        # 计算变化
        changes = {
            "格物": self.progress.gewo_score - old_progress.gewo_score,
            "致知": self.progress.zhizhi_score - old_progress.zhizhi_score,
            "诚意": self.progress.chengyi_score - old_progress.chengyi_score,
            "正心": self.progress.zhengxin_score - old_progress.zhengxin_score,
            "修身": self.progress.xiushen_score - old_progress.xiushen_score,
            "仁": self.progress.ren_score - old_progress.ren_score,
            "智": self.progress.zhi_score - old_progress.zhi_score,
            "勇": self.progress.yong_score - old_progress.yong_score
        }

        positive_changes = [k for k, v in changes.items() if v > 0]
        negative_changes = [k for k, v in changes.items() if v < 0]

        return {
            "old_level": old_progress.current_level.value,
            "new_level": self.progress.current_level.value,
            "level_up": self.progress.current_level.value != old_progress.current_level.value,
            "progress_increase": self.progress.progress_percentage - (
                old_progress.gewo_score * 0.1 +
                old_progress.zhizhi_score * 0.15 +
                old_progress.chengyi_score * 0.15 +
                old_progress.zhengxin_score * 0.15 +
                old_progress.xiushen_score * 0.2 +
                old_progress.ren_score * 0.1 +
                old_progress.zhi_score * 0.08 +
                old_progress.yong_score * 0.07
            ) * 100,
            "positive_changes": positive_changes,
            "negative_changes": negative_changes,
            "overall": "进步" if sum(changes.values()) > 0 else "需加强修炼"
        }

# 全局实例
_cultivation_system: Optional[SelfCultivationSystem] = None

def get_cultivation_system() -> SelfCultivationSystem:
    """get修身system_instance"""
    global _cultivation_system
    if _cultivation_system is None:
        _cultivation_system = SelfCultivationSystem()
    return _cultivation_system
