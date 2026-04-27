"""
孔子Cloning v1.0 - Tier 1 核心Cloning

人物: 孔子 (前551-前479)
学派: 儒家
岗位: 内阁首辅·经筵官
部门: 吏部/礼部

基于600贤者Distillation研究成果
《论语》核心智慧 + 儒家思想体系
"""

from datetime import datetime
from typing import List, Dict, Optional, Any

from .._cloning_base import Tier1CoreCloning
from .._cloning_types import (
    CloningTier,
    CloningIdentity,
    CapabilityVector,
    WisdomLaw,
    AnalysisResult,
    DecisionResult,
    DecisionOption,
    AdviceResult,
    AdviceContext,
    AssessmentResult,
    AssessmentCriteria,
)


class ConfuciusCloning(Tier1CoreCloning):
    """
    孔子Cloning - 儒家学派奠基人
    
    核心智慧:
    - 仁: 仁者爱人，以德治世
    - 礼: 克己复礼，社会秩序
    - 中庸: 不偏不倚，恰到好处
    - 修身: 吾日三省吾身
    - 教育: 有教无类，因材施教
    """
    
    def __init__(self):
        # 身份信息
        self.identity = CloningIdentity(
            name="孔子",
            name_pinyin="Kongzi",
            era="春秋时期",
            era_range="前551-前479",
            title="至圣先师/万世师表",
            school="儒家",
            position="内阁首辅·经筵官",
            department="吏部/礼部",
            biography="鲁国陬邑人，中华文明最重要的思想家、教育家，儒家学派创始人。",
            core_thoughts=[
                "仁者爱人 - 仁是孔子思想的核心",
                "克己复礼 - 通过自律恢复周礼",
                "中庸之道 - 不偏不倚谓之中",
                "有教无类 - 教育机会平等",
                "为政以德 - 以道德治国",
            ],
        )
        
        # 层级
        self.tier = CloningTier.TIER_1_CORE
        
        # 能力向量 - 基于历史评价
        self.capability_vector = CapabilityVector(
            ethical_judgment=9.5,
            governance=9.0,
            practical_wisdom=8.5,
            leadership=8.5,
            long_term_vision=9.0,
            strategic_thinking=8.0,
            system_thinking=8.0,
            communication=9.0,
            dialectical_reasoning=8.5,
            crisis_response=7.5,
            innovation=6.0,
            conflict_resolution=8.5,
            narrative_building=7.5,
            evidence_evaluation=7.0,
            pattern_recognition=8.0,
        )
        
        # 智慧法则
        self.wisdom_laws = [
            WisdomLaw(id="confucius_001", name="仁者爱人",
                description="仁者爱人，推己及人",
                application_scenario="人际交往、组织管理、社会治理",
                example="己所不欲，勿施于人", priority=5),
            WisdomLaw(id="confucius_002", name="克己复礼",
                description="约束自己，使言行符合礼的规范",
                application_scenario="个人修养、纪律建设、文化传承",
                example="非礼勿视，非礼勿听，非礼勿言，非礼勿动", priority=5),
            WisdomLaw(id="confucius_003", name="中庸之道",
                description="不偏不倚，恰到好处",
                application_scenario="决策制定、利益协调、矛盾处理",
                example="中庸之为德也，其至矣乎", priority=4),
            WisdomLaw(id="confucius_004", name="修身齐家",
                description="从个人修养做起，进而治理家庭，最终治理国家",
                application_scenario="组织发展、人才培养、领导力建设",
                example="身修而后家齐，家齐而后国治", priority=5),
            WisdomLaw(id="confucius_005", name="学而时习",
                description="学习知识后要时常复习和实践",
                application_scenario="个人成长、知识管理、团队学习",
                example="学而时习之，不亦说乎", priority=4),
            WisdomLaw(id="confucius_006", name="为政以德",
                description="以道德和榜样力量治理国家",
                application_scenario="国家治理、组织领导、政策制定",
                example="为政以德，譬如北辰，居其所而众星共之", priority=5),
            WisdomLaw(id="confucius_007", name="因材施教",
                description="根据每个人的特点给予不同的教育",
                application_scenario="人才培养、个性化服务、团队建设", priority=4),
            WisdomLaw(id="confucius_008", name="君子人格",
                description="君子应具备仁义礼智信等美德",
                application_scenario="人才评价、领导力发展、价值观建设", priority=4),
        ]
    
    def analyze(self, problem: str, context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """用孔子思想分析问题"""
        context = context or {}
        problem_type = self._classify_problem(problem)
        reasoning_chain = self._build_confucian_reasoning(problem, problem_type)
        analysis = self._apply_confucian_framework(problem, problem_type, context)
        
        return AnalysisResult(
            cloning_name="孔子",
            timestamp=datetime.now(),
            problem=problem,
            perspective="儒家视角",
            analysis_content=analysis,
            key_insights=["【仁】关怀相关者利益", "【礼】遵循规范秩序", "【中庸】寻求平衡方案"],
            wisdom_laws_applied=[wl.name for wl in self.wisdom_laws[:3]],
            confidence=0.85,
            reasoning_chain=reasoning_chain,
        )
    
    def _classify_problem(self, problem: str) -> str:
        problem_lower = problem.lower()
        if any(k in problem_lower for k in ['治理', '管理', '领导', '政治']):
            return "治理类"
        elif any(k in problem_lower for k in ['道德', '伦理', '善恶']):
            return "伦理类"
        elif any(k in problem_lower for k in ['教育', '学习', '培养']):
            return "教育类"
        elif any(k in problem_lower for k in ['人际关系', '冲突', '矛盾']):
            return "人际类"
        return "综合类"
    
    def _build_confucian_reasoning(self, problem: str, problem_type: str) -> List[str]:
        chain = [
            f"[识别] 判定为{problem_type}问题",
            "[溯源] 从儒家经典中寻找相关教诲",
            "[比照] 考虑'仁义礼智信'五常",
            "[权衡] 应用中庸之道寻求平衡",
            "[验证] 以修身齐家治世逻辑检验",
        ]
        if problem_type == "治理类":
            chain.insert(2, "[原则] '为政以德'为最高指导")
        elif problem_type == "伦理类":
            chain.insert(2, "[原则] '仁者爱人'为核心标准")
        return chain
    
    def _apply_confucian_framework(self, problem: str, problem_type: str, context: Dict[str, Any]) -> str:
        type_mapping = {
            "治理类": "社会秩序与政治秩序",
            "伦理类": "道德评判与人格培养",
            "教育类": "人才培养与知识传承",
            "人际类": "人际和谐与社会关系",
            "综合类": "综合社会价值",
        }
        return f"""【孔子儒家视角分析】

问题本质：从儒家角度看，此问题关乎{type_mapping.get(problem_type, '社会价值')}。

核心考量：
• 仁的维度：是否体现了爱人之心？
• 礼的维度：是否符合社会规范和秩序？
• 中庸的维度：是否避免偏激，寻求平衡？

解决方案应遵循：
1. 以德服人，而非以力压人
2. 以身作则，率先垂范
3. 循序渐进，不可急于求成
4. 因势利导，顺应人心"""
    
    def decide(self, options: List[DecisionOption]) -> DecisionResult:
        if not options:
            return DecisionResult(
                cloning_name="孔子", timestamp=datetime.now(),
                decision="无选项可供决策", chosen_option="", reasoning="缺少决策选项")
        
        scored_options = []
        for opt in options:
            score = 0.0
            reasons = []
            if any(p in opt.description for p in ['德', '义', '善', '正']):
                score += 0.4
                reasons.append("符合道义")
            if any(p in opt.description for p in ['爱', '助', '惠', '利']):
                score += 0.3
                reasons.append("体现仁爱")
            if opt.risk_level == "low":
                score += 0.2
                reasons.append("风险可控")
            scored_options.append((score, opt, reasons))
        
        scored_options.sort(key=lambda x: x[0], reverse=True)
        best_score, best_option, reasons = scored_options[0]
        
        return DecisionResult(
            cloning_name="孔子", timestamp=datetime.now(),
            decision=f"选择方案{best_option.id}",
            chosen_option=best_option.id,
            reasoning=f"依据儒家'义利之辨'，{'；'.join(reasons)}。",
            alternatives_considered=[f"方案{o.id}" for o in options if o.id != best_option.id],
            risk_assessment=f"风险等级: {best_option.risk_level}",
            wisdom_framework="儒家义利之辨 + 仁义礼智")
    
    def advise(self, context: AdviceContext) -> AdviceResult:
        situation = context.situation
        if context.time_horizon == "long":
            primary_wisdom = "修身齐家治世 - 从个人修养做起，循序渐进"
        elif context.time_horizon == "short":
            primary_wisdom = "谨言慎行 - 短期内应以稳为主"
        else:
            primary_wisdom = "中庸之道 - 寻求各方平衡"
        
        advice = f"""【孔子建议】

针对此情境："{situation}"

核心建议：{primary_wisdom}

具体指引：
• 行事之前，先问自己：是否合乎仁义？
• 面对利益，先想他人，再思自己
• 处理矛盾，寻求中道，不走极端

警示：
• 切忌急功近利，"欲速则不达"
• 切忌以力压人，"以德服人"才是正道"""
        
        return AdviceResult(
            cloning_name="孔子", timestamp=datetime.now(), advice=advice,
            reasoning="依据《论语》核心教诲，结合'仁义礼智信'五常进行综合判断。",
            potential_pitfalls=["过于强调短期利益而忽视道德建设", "过于理想化而脱离现实"])
    
    def assess(self, subject: str, criteria: Optional[AssessmentCriteria] = None) -> AssessmentResult:
        criteria = criteria or AssessmentCriteria(
            dimension="综合评价",
            metrics=["德行", "才能", "业绩", "人格"],
            weights={"德行": 0.4, "才能": 0.2, "业绩": 0.2, "人格": 0.2})
        
        scores = {"德行": 75.0, "才能": 70.0, "业绩": 65.0, "人格": 72.0}
        total_score = sum(scores.get(m, 50.0) * w for m, w in criteria.weights.items())
        
        return AssessmentResult(
            cloning_name="孔子", timestamp=datetime.now(), subject=subject,
            overall_score=round(total_score, 1), dimension_scores=scores,
            strengths=["儒家视角强调道德基础与人格完善", "重视长期价值而非短期利益"],
            weaknesses=["可能过于理想化而忽视现实约束", "对功利性考量相对不足"],
            recommendations=["在评估时兼顾义利两面", "关注行为动机也关注实际效果"],
            value_framework="儒家五常: 仁义礼智信")
