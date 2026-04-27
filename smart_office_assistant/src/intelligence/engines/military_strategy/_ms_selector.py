"""
__all__ = [
    'select_strategy',
]

策略选择器 - 根据形势选择最佳策略
"""

from typing import Dict, List
from ._ms_enums import StrategyCategory, StrategyType
from ._ms_dataclasses import StrategyInfo, StrategyApplication
from ._ms_database import StrategyDatabase
from ._ms_situation import SituationAnalyzer

class StrategySelector:
    """strategy选择器"""
    
    def __init__(self):
        self.database = StrategyDatabase()
        self.analyzer = SituationAnalyzer()
    
    def select_strategy(self, 
                       situation: Dict,
                       self_state: Dict,
                       enemy_state: Dict,
                       context: Dict) -> StrategyApplication:
        """选择最佳strategy"""
        # 分析形势
        category, advantage = self.analyzer.analyze(self_state, enemy_state, context)
        
        # get该类别的strategy
        strategies = self.database.get_by_category(category)
        
        # 根据具体情境选择最佳strategy
        best_strategy = self._evaluate_strategies(
            strategies, situation, advantage
        )
        
        # 构建应用建议
        return self._build_application(best_strategy, advantage)
    
    def _evaluate_strategies(self, 
                            strategies: List[StrategyInfo],
                            situation: Dict,
                            advantage: float) -> StrategyInfo:
        """评估strategy适合度"""
        best = None
        best_score = -1
        
        for strategy in strategies:
            score = self._calculate_fit(strategy, situation, advantage)
            if score > best_score:
                best_score = score
                best = strategy
        
        return best
    
    def _calculate_fit(self, 
                      strategy: StrategyInfo,
                      situation: Dict,
                      advantage: float) -> float:
        """计算strategy适合度"""
        score = 0.0
        
        # 情境匹配度
        context_match = situation.get('type', 'general')
        if context_match in strategy.applications:
            score += 0.5
        
        # 优势程度匹配
        if strategy.category == StrategyCategory.VICTORY and advantage > 1.5:
            score += 0.3
        elif strategy.category == StrategyCategory.RETREAT and advantage < 0.5:
            score += 0.3
        
        # 原则匹配度
        score += 0.2 * len([
            p for p in strategy.principles 
            if any(k in situation.get('keywords', []) for k in p)
        ])
        
        return score
    
    def _build_application(self, 
                           strategy: StrategyInfo,
                           advantage: float) -> StrategyApplication:
        """构建strategy应用"""
        return StrategyApplication(
            strategy=self._get_strategy_type(strategy.name),
            confidence=min(0.95, max(0.5, advantage / 2)),
            reasoning=f"根据当前形势分析,选择'{strategy.name}'作为最佳strategy",
            steps=self._generate_steps(strategy),
            risks=self._analyze_risks(strategy),
            benefits=self._analyze_benefits(strategy)
        )
    
    def _get_strategy_type(self, name: str) -> StrategyType:
        """getstrategy类型"""
        for st in StrategyType:
            if st.value == name:
                return st
        return StrategyType.ZOU_WEI_SHANG_JI
    
    def _generate_steps(self, strategy: StrategyInfo) -> List[str]:
        """generate执行步骤"""
        steps = [
            f"第一步:理解{strategy.name}的核心原理",
            f"第二步:分析当前情境与strategy的匹配度",
            f"第三步:制定具体实施方案",
            f"第四步:准备应急预案",
            f"第五步:执行并监控效果"
        ]
        return steps
    
    def _analyze_risks(self, strategy: StrategyInfo) -> List[str]:
        """分析风险"""
        return [
            "执行过程中可能出现意外变化",
            "敌方可能有反制措施",
            "需要准确把握时机"
        ]
    
    def _analyze_benefits(self, strategy: StrategyInfo) -> List[str]:
        """分析收益"""
        return [
            f"运用{strategy.name}智慧化解当前困境",
            "符合传统智慧,具有文化认同感",
            "多维度思考问题,提升decision质量"
        ]
