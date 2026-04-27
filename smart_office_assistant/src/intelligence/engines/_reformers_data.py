# -*- coding: utf-8 -*-
"""
政治改革策略数据 v1.0
7种改革策略的懒加载数据模块
"""

from typing import Dict, List

# 懒加载缓存
_strategy_cache: Dict = None

def get_strategy_data() -> Dict:
    """获取策略数据（懒加载）"""
    global _strategy_cache
    if _strategy_cache is not None:
        return _strategy_cache
    
    # 策略数据 - 格式与原 _init_strategy_map 返回值一致
    _strategy_cache = {
        "渐进改革": {
            "strategy_name": "萧规曹随·渐进改革",
            "source_sages": ["曹参", "萧何"],
            "reasoning": "恢复期宜稳定优先，避免激进变革，以时间换取空间",
            "action_plan": [
                "1. 评估现有制度的有效性",
                "2. 识别可以微调的领域",
                "3. 逐步推行试点改革",
                "4. 观察效果后扩大范围"
            ],
            "risk_factors": ["改革过于缓慢可能错失时机", "既得利益集团阻力"],
            "expected_outcome": "社会稳定与改革的平衡",
            "historical_cases": ["曹参继萧何为相，继续执行原有政策"]
        },
        "激进改革": {
            "strategy_name": "天变不足畏·激进改革",
            "source_sages": ["王安石", "商鞅", "晁错"],
            "reasoning": "危机时刻需要大胆改革，打破旧有利益格局",
            "action_plan": [
                "1. 明确改革目标和愿景",
                "2. 争取最高决策者支持",
                "3. 组建改革核心团队",
                "4. 同步推进多项改革",
                "5. 准备应对强烈反弹"
            ],
            "risk_factors": ["改革者下场往往不佳", "可能引发政治动荡"],
            "expected_outcome": "根本性制度变革",
            "historical_cases": ["王安石熙宁变法", "商鞅变法", "晁错削藩"]
        },
        "人才治国": {
            "strategy_name": "任贤使能·人才战略",
            "source_sages": ["管仲", "百里奚", "房玄龄", "狄仁杰"],
            "reasoning": "治国之本在于得人，人才是改革成败的关键",
            "action_plan": [
                "1. 建立人才识别机制",
                "2. 设计人才晋升通道",
                "3. 形成人才梯队",
                "4. 合理配置人才组合"
            ],
            "risk_factors": ["任人唯亲的风险", "人才流失"],
            "expected_outcome": "人尽其才，才尽其用",
            "historical_cases": ["房玄龄善于用人", "狄仁杰举贤任能"]
        },
        "财政改革": {
            "strategy_name": "理财为国·财政改革",
            "source_sages": ["刘晏", "杨炎", "张居正", "管仲"],
            "reasoning": "财政是国家的血脉，理财能力决定国力",
            "action_plan": [
                "1. 摸清财政家底",
                "2. 设计新税收制度",
                "3. 建立监管机制",
                "4. 平衡中央与地方财政"
            ],
            "risk_factors": ["触动既得利益", "执行变形"],
            "expected_outcome": "财政可持续，国力增强",
            "historical_cases": ["刘晏理财改革", "杨炎两税法", "张居正一条鞭法"]
        },
        "危机应对": {
            "strategy_name": "力挽狂澜·危机应对",
            "source_sages": ["谢安", "于谦", "林则徐", "诸葛亮", "寇准"],
            "reasoning": "危机时刻最能考验领导力，需冷静、果敢、坚定",
            "action_plan": [
                "1. 迅速评估危机程度",
                "2. 调动核心资源应对",
                "3. 稳定军心民心",
                "4. 寻找转机",
                "5. 化危为机"
            ],
            "risk_factors": ["判断失误可能加重危机", "时间压力"],
            "expected_outcome": "成功化解危机，转危为安",
            "historical_cases": ["谢安淝水之战", "于谦北京保卫战", "林则徐禁烟"]
        },
        "法治建设": {
            "strategy_name": "以法治国·制度建设",
            "source_sages": ["管仲", "子产", "诸葛亮", "王安石"],
            "reasoning": "法治是长治久安的基础，制度比人治更可靠",
            "action_plan": [
                "1. 制定清晰法律",
                "2. 确保执法公正",
                "3. 建立监督机制",
                "4. 培育法治文化"
            ],
            "risk_factors": ["执法不公", "法律僵化"],
            "expected_outcome": "法治社会，长治久安",
            "historical_cases": ["子产铸刑书", "诸葛亮依法治蜀"]
        },
        "外交博弈": {
            "strategy_name": "合纵连横·外交智慧",
            "source_sages": ["张良", "范蠡", "寇准"],
            "reasoning": "外交是内政的延伸，联盟与博弈需审时度势",
            "action_plan": [
                "1. 分析各方利益",
                "2. 寻找共同利益点",
                "3. 设计互惠方案",
                "4. 保持战略定力"
            ],
            "risk_factors": ["盟友背叛", "过度依赖"],
            "expected_outcome": "国家利益最大化",
            "historical_cases": ["寇准澶渊之盟", "张良辅佐刘邦"]
        },
    }
    return _strategy_cache
