"""
心理学先驱fusion模块 - Psychology Pioneer Fusion Engine
=======================================================
版本: v8.2.0
创建时间: 2026-04-03

整合5位心理学先驱深化引擎,构建完整的用户心理洞察能力:

1. 弗洛伊德潜意识引擎 - 潜意识需求挖掘,冰山分析
2. 荣格原型系统引擎 - 集体无意识,原型诊断
3. 马斯洛需求动态引擎 - 需求层次,成长路径
4. 奥格威品牌叙事引擎 - 品牌形象,Big Idea
5. 特劳特定位引擎 - 竞争定位,差异化

fusion架构:
┌─────────────────────────────────────────────────────────┐
│              心理学先驱fusion引擎 v8.2.0                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ 弗洛伊德  │ │   荣格   │ │  马斯洛  │ │  奥格威  │ │
│  │潜意识引擎 │ │原型引擎  │ │需求引擎  │ │叙事引擎  │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ │
│       │            │            │            │        │
│       └────────────┴─────┬───────┴────────────┘        │
│                          │                             │
│                  ┌───────┴───────┐                     │
│                  │  用户心理洞察  │                     │
│                  │    fusion层      │                     │
│                  └───────────────┘                     │
└─────────────────────────────────────────────────────────┘
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

# 导入各先驱引擎
from .psychology.pioneer_freud_engine import 弗洛伊德潜意识引擎, 潜意识层次, 人格结构
from .psychology.pioneer_jung_archetype import 荣格原型引擎, 原型类型
from .psychology.pioneer_maslow_dynamic import 马斯洛需求引擎, 需求层次
from .psychology.pioneer_ogilvy_narrative import 奥格威品牌叙事引擎, 品牌类型, 创意方向
from .psychology.pioneer_positioning_engine import 特劳特定位引擎, 定位类型

class PsychologyPioneerFusionEngine:
    """
    心理学先驱fusion引擎

    整合14位心理学与营销学先驱的核心思想,提供完整的用户心理洞察能力.
    """

    # 别名(中文名用于兼容)
    __name__zh__ = "心理学先驱fusion引擎"
    
    def __init__(self):
        self.name = "心理学先驱fusion引擎"
        self.version = "8.2.0"
        
        # init各先驱引擎
        self.弗洛伊德 = 弗洛伊德潜意识引擎()
        self.荣格 = 荣格原型引擎()
        self.马斯洛 = 马斯洛需求引擎()
        self.奥格威 = 奥格威品牌叙事引擎()
        self.特劳特 = 特劳特定位引擎()
        
        # fusion分析配置
        self.分析深度 = "完整"
    
    def comprehensive_user_analysis(self, user_data: Dict) -> Dict:
        """
        synthesize用户分析
        
        Args:
            user_data: 用户数据
            
        Returns:
            synthesize分析结果
        """
        # 1. 潜意识分析
        潜意识分析 = self.弗洛伊德.analyze_iceberg(
            user_data.get("statement", ""),
            user_data.get("context")
        )
        
        # 2. 原型诊断
        原型诊断 = self.荣格.diagnose_archetype(user_data)
        
        # 3. 需求层次诊断
        需求诊断 = self.马斯洛.diagnose_needs_level(user_data)
        
        # 4. 潜意识驱动力
        驱动力 = self.弗洛伊德.analyze_subconscious_drive(user_data)
        
        # 5. 成长路径
        成长路径 = self.马斯洛.get_growth_path(user_data)
        
        # synthesize洞察
        synthesize洞察 = self._generate_comprehensive_insights(
            潜意识分析, 原型诊断, 需求诊断, 驱动力
        )
        
        return {
            "version": self.version,
            "分析时间": datetime.now().isoformat(),
            "用户ID": user_data.get("id", "unknown"),
            "潜意识分析": 潜意识分析,
            "原型诊断": 原型诊断,
            "需求诊断": 需求诊断,
            "潜意识驱动力": 驱动力,
            "成长路径": 成长路径,
            "synthesize洞察": synthesize洞察,
            "营销建议": self._generate_marketing_recommendations(
                潜意识分析, 原型诊断, 需求诊断
            )
        }
    
    def _generate_comprehensive_insights(
        self,
        潜意识: Dict,
        原型: Dict,
        需求: Dict,
        驱动力: Dict
    ) -> Dict:
        """generatesynthesize洞察"""
        return {
            "用户画像": {
                "主导需求": 需求.get("主导需求层次", ""),
                "主导原型": 原型.get("主原型", {}).get("类型", ""),
                "意识层次": 潜意识.get("意识层次", ""),
                "核心驱动力": 驱动力.get("主导驱动力", {})
            },
            "心理characteristics": [
                f"潜意识需求:{', '.join(潜意识.get('潜在需求', []))}",
                f"人格结构:{潜意识.get('主导人格结构', '')}",
                f"次级原型:{原型.get('次原型', {}).get('类型', '')}"
            ],
            "用户总结": self._summarize_user(潜意识, 原型, 需求)
        }
    
    def _summarize_user(
        self,
        潜意识: Dict,
        原型: Dict,
        需求: Dict
    ) -> str:
        """总结用户"""
        总结 = []
        
        # 需求层面
        主导需求 = 需求.get("主导需求层次", "")
        if 主导需求:
            总结.append(f"处于{主导需求}阶段")
        
        # 原型层面
        主原型 = 原型.get("主原型", {}).get("类型", "")
        if 主原型:
            总结.append(f"心理原型偏向{主原型}")
        
        # 潜意识层面
        意识层次 = 潜意识.get("意识层次", "")
        if 意识层次:
            总结.append(f"表达处于{意识层次}")
        
        return ";".join(总结) if 总结 else "用户characteristics待进一步分析"
    
    def _generate_marketing_recommendations(
        self,
        潜意识: Dict,
        原型: Dict,
        需求: Dict
    ) -> Dict:
        """generate营销建议"""
        return {
            "产品strategy": self._get_product_strategy(原型, 需求),
            "定价strategy": self._get_pricing_strategy(需求),
            "传播strategy": self._get_communication_strategy(原型, 潜意识),
            "渠道strategy": self._get_channel_strategy(原型)
        }
    
    def _get_product_strategy(self, 原型: Dict, 需求: Dict) -> str:
        """get产品strategy"""
        主原型 = 原型.get("主原型", {}).get("类型", "")
        主导需求 = 需求.get("主导需求层次", "")
        
        return f"产品应满足{主导需求},体现{主原型}的品牌形象"
    
    def _get_pricing_strategy(self, 需求: Dict) -> str:
        """get定价strategy"""
        主导需求 = 需求.get("主导需求层次", "")
        
        if "生理" in 主导需求 or "安全" in 主导需求:
            return "性价比优先"
        elif "尊重" in 主导需求:
            return "高端定价"
        else:
            return "价值定价"
    
    def _get_communication_strategy(self, 原型: Dict, 潜意识: Dict) -> str:
        """get传播strategy"""
        主原型 = 原型.get("主原型", {}).get("类型", "")
        意识层次 = 潜意识.get("意识层次", "")
        
        if 意识层次 == "潜意识层":
            return "采用隐喻,情感诉求"
        else:
            return f"体现{主原型}的价值观"
    
    def _get_channel_strategy(self, 原型: Dict) -> str:
        """get渠道strategy"""
        主原型 = 原型.get("主原型", {}).get("类型", "")
        
        if "英雄" in 主原型 or "探险家" in 主原型:
            return "线上渠道为主"
        elif "照顾者" in 主原型 or "情人" in 主原型:
            return "线下体验为主"
        else:
            return "全渠道布局"
    
    def brand_analysis(self, brand_data: Dict, market_data: Dict) -> Dict:
        """
        品牌分析
        
        Args:
            brand_data: 品牌数据
            market_data: 市场数据
            
        Returns:
            品牌分析结果
        """
        # 1. 品牌形象设计
        品牌形象 = self.奥格威.design_brand_image(brand_data)
        
        # 2. Big Ideagenerate
        Big_Idea = self.奥格威.generate_big_idea(brand_data, market_data)
        
        # 3. 品牌故事
        品牌故事 = self.奥格威.build_brand_story(brand_data)
        
        # 4. 竞争定位
        竞争分析 = self.特劳特.analyze_competition(brand_data, market_data.get("competitors", []))
        
        # 5. 定位strategy
        定位类型 = self.特劳特.determine_positioning_type(market_data, brand_data)
        
        # 6. 差异化设计
        差异化 = self.特劳特.design_differentiation(brand_data, market_data)
        
        # 7. 定位陈述
        定位陈述 = self.特劳特.create_positioning_statement(brand_data)
        
        return {
            "version": self.version,
            "分析时间": datetime.now().isoformat(),
            "品牌形象": 品牌形象,
            "Big_Idea": Big_Idea,
            "品牌故事": 品牌故事,
            "竞争分析": 竞争分析,
            "定位strategy": 定位类型,
            "差异化": 差异化,
            "定位陈述": 定位陈述,
            "执行建议": self._generate_brand_execution_advice(
                品牌形象, Big_Idea, 差异化
            )
        }
    
    def _generate_brand_execution_advice(
        self,
        品牌形象: Dict,
        Big_Idea: Dict,
        差异化: Dict
    ) -> List[str]:
        """generate品牌执行建议"""
        return [
            f"1. 品牌形象:unified{品牌形象.get('品牌形象', {}).get('类型', '')}形象",
            f"2. Big Idea:{Big_Idea.get('Big_Idea', '')}",
            f"3. 差异化:聚焦{差异化.get('推荐差异化', {}).get('概念', '')}",
            "4. 持续传播:重复核心信息"
        ]
    
    def creative_strategy(self, brief: Dict) -> Dict:
        """
        创意strategy制定
        
        Args:
            brief: 创意简报
            
        Returns:
            创意strategy方案
        """
        # 奥格威创意strategy
        奥格威strategy = self.奥格威.get_creative_strategy(brief)
        
        # 标题创作
        标题 = self.奥格威.create_headline(
            brief.get("content", {}),
            brief.get("direction", "理性诉求")
        )
        
        # 叙事strategy
        叙事原型 = self.荣格.get_narrative_archetype(
            brief.get("story_type", "励志")
        )
        
        return {
            "奥格威strategy": 奥格威strategy,
            "标题方案": 标题[:5],
            "叙事原型": 叙事原型,
            "执行要点": self._extract_creative_execution_points(奥格威strategy, 叙事原型)
        }
    
    def _extract_creative_execution_points(
        self,
        strategy: Dict,
        叙事: Dict
    ) -> List[str]:
        """提取创意执行要点"""
        return [
            f"创意方向:{strategy.get('创意方向', '')}",
            f"核心信息:{strategy.get('strategy框架', {}).get('核心信息', '')}",
            f"叙事原型:{叙事.get('推荐原型', '')}"
        ]
    
    def get_user_insights(self, user_data: Dict) -> Dict:
        """
        get用户洞察(简化版)
        
        Args:
            user_data: 用户数据
            
        Returns:
            用户洞察
        """
        # 原型诊断
        原型 = self.荣格.diagnose_archetype(user_data)
        
        # 需求诊断
        需求 = self.马斯洛.diagnose_needs_level(user_data)
        
        # 潜意识分析
        潜意识 = self.弗洛伊德.analyze_iceberg(
            user_data.get("statement", "")
        )
        
        return {
            "心理原型": 原型.get("主原型", {}).get("类型", ""),
            "需求层次": 需求.get("主导需求层次", ""),
            "潜意识需求": 潜意识.get("潜在需求", []),
            "核心洞察": f"用户追求{原型.get('主原型', {}).get('characteristics', {}).get('渴望', '')}," \
                       f"处于{需求.get('主导需求层次', '')}阶段"
        }

# ───────────────────────────────────────────────────────────────
# 全局单例惰性加载（修复全局代码规范）
# ───────────────────────────────────────────────────────────────

from functools import lru_cache

@lru_cache(maxsize=1)
def get_psychology_pioneer_fusion() -> PsychologyPioneerFusionEngine:
    """获取心理学先驱融合引擎单例 - 惰性初始化"""
    return PsychologyPioneerFusionEngine()

# 便捷函数（使用惰性加载）
def 用户synthesize分析(user_data: Dict) -> Dict:
    """用户synthesize分析"""
    return get_psychology_pioneer_fusion().comprehensive_user_analysis(user_data)

def 品牌分析(brand_data: Dict, market_data: Dict) -> Dict:
    """品牌分析"""
    return get_psychology_pioneer_fusion().brand_analysis(brand_data, market_data)

def 创意strategy(brief: Dict) -> Dict:
    """创意strategy"""
    return get_psychology_pioneer_fusion().creative_strategy(brief)

def 用户洞察(user_data: Dict) -> Dict:
    """用户洞察"""
    return get_psychology_pioneer_fusion().get_user_insights(user_data)

# 向后兼容别名
心理学先驱融合引擎 = PsychologyPioneerFusionEngine

# ───────────────────────────────────────────────────────────────
# 模块导出
# ───────────────────────────────────────────────────────────────
__all__ = [
    'PsychologyPioneerFusionEngine',
    'get_psychology_pioneer_fusion',
    '用户synthesize分析',
    '品牌分析',
    '创意strategy',
    '用户洞察',
    '心理学先驱融合引擎',
]
