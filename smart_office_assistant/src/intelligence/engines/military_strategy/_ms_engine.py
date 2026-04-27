"""
__all__ = [
    'analyze_situation',
    'get_all_strategies',
    'get_strategy_advice',
]

兵法策略引擎主类
"""

from typing import Dict, List, Optional
from ._ms_enums import StrategyCategory
from ._ms_dataclasses import StrategyApplication
from ._ms_database import StrategyDatabase
from ._ms_selector import StrategySelector
from ._ms_situation import SituationAnalyzer

class MilitaryStrategyEngine:
    """三十六计兵法strategy引擎主类"""
    
    def __init__(self):
        self.database = StrategyDatabase()
        self.selector = StrategySelector()
        self.analyzer = SituationAnalyzer()
    
    def analyze_situation(self, self_state: Dict, 
                         enemy_state: Dict, 
                         context: Dict) -> Dict:
        """分析形势"""
        category, advantage = self.analyzer.analyze(
            self_state, enemy_state, context
        )
        
        return {
            'category': category.value,
            'advantage_ratio': advantage,
            'recommendation': self._get_category_recommendation(category)
        }
    
    def _get_category_recommendation(self, category: StrategyCategory) -> str:
        """get类别建议"""
        recommendations = {
            StrategyCategory.VICTORY: "处于优势,建议使用胜战计,稳扎稳打扩大优势",
            StrategyCategory.CONFRONTATION: "势均力敌,建议使用敌战计,灵活应对",
            StrategyCategory.ATTACK: "略处下风,建议使用攻战计,主动出击",
            StrategyCategory.CHAOS: "局势混乱,建议使用混战计,浑水摸鱼",
            StrategyCategory.MERGE: "需要兼并,建议使用并战计,整合资源",
            StrategyCategory.RETREAT: "处于劣势,建议使用败战计,保存实力"
        }
        return recommendations.get(category, "请根据具体情况选择strategy")
    
    def get_strategy_advice(self, situation: Dict) -> StrategyApplication:
        """getstrategy建议"""
        self_state = situation.get('self_state', {})
        enemy_state = situation.get('enemy_state', {})
        context = situation.get('context', {})
        
        return self.selector.select_strategy(
            situation, self_state, enemy_state, context
        )
    
    def get_all_strategies(self, category: Optional[StrategyCategory] = None) -> List[Dict]:
        """get所有strategy"""
        if category:
            strategies = self.database.get_by_category(category)
        else:
            strategies = list(self.database.strategies.values())
        
        return [
            {
                'name': s.name,
                'category': s.category.value,
                'original_text': s.original_text,
                'explanation': s.explanation,
                'principles': s.principles,
                'applications': s.applications,
                'historical_cases': s.historical_cases
            }
            for s in strategies
        ]
