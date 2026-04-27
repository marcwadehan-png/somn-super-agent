# -*- coding: utf-8 -*-
"""
神之架构Claw路由扩展
====================

V2.0: 为WisdomDispatcher添加Claw路由能力

功能：
1. 按部门路由Claw
2. 按岗位等级路由Claw  
3. 按触发词匹配Claw
4. 多Claw协作调度

使用方式：
    from src.intelligence.dispatcher.wisdom_dispatch._dispatch_claw import ClawRouter
    
    router = ClawRouter()
    result = router.route_by_department("礼部", "什么是仁？")
    print(result)
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# 路径配置
PROJECT_ROOT = Path(__file__).resolve().parents[5]
CLAW_CONFIGS_DIR = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "claws" / "configs"


# ═══════════════════════════════════════════════════════════════════════════════
# 数据结构
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ClawInfo:
    """Claw信息"""
    name: str
    department: str           # 部门
    school: str               # 学派
    era: str                  # 时代
    tier_name: str            # 层级名称
    court_position: str       # 岗位ID
    position_name: str        # 岗位名称
    position_pin: str         # 品秩
    nobility: str             # 爵位
    triggers: List[str]       # 触发词
    wisdom_school: str        # 智慧学派
    can_lead: bool            # 可作为主Claw
    can_support: bool         # 可作为协作Claw
    preferred_role: str       # 偏好角色
    
    @property
    def priority_score(self) -> float:
        """计算优先级分数"""
        score = 0.0
        
        # 爵位加分
        if self.nobility == "王爵":
            score += 100
        elif self.nobility == "公爵":
            score += 80
        elif self.nobility == "侯爵":
            score += 60
        elif self.nobility == "伯爵":
            score += 40
        
        # 品秩加分
        pin_scores = {
            "ZHENG_1PIN": 90, "CONG_1PIN": 85,
            "ZHENG_2PIN": 70, "CONG_2PIN": 65,
            "ZHENG_3PIN": 50, "CONG_3PIN": 45,
            "ZHENG_4PIN": 30, "CONG_4PIN": 25,
        }
        score += pin_scores.get(self.position_pin, 0)
        
        # 层级加分
        tier_scores = {"创始人": 50, "超级大师": 45, "集大成者": 30, "学者": 15, "实践者": 10}
        score += tier_scores.get(self.tier_name, 0)
        
        return score


@dataclass
class ClawRouteResult:
    """路由结果"""
    primary_claw: str                      # 主Claw
    collaborator_claws: List[str]          # 协作Claw列表
    department: str                         # 目标部门
    routing_reason: str                     # 路由原因
    confidence: float                       # 置信度


# ═══════════════════════════════════════════════════════════════════════════════
# Claw路由核心
# ═══════════════════════════════════════════════════════════════════════════════

class ClawRouter:
    """
    Claw路由器 V2.0
    
    根据问题内容、部门、岗位等信息路由到合适的Claw
    """
    
    def __init__(self):
        self._claws: Dict[str, ClawInfo] = {}
        self._department_claws: Dict[str, List[str]] = {}
        self._school_claws: Dict[str, List[str]] = {}
        self._trigger_index: Dict[str, List[str]] = {}  # trigger -> claw names
        self._initialized = False
    
    def initialize(self) -> None:
        """初始化：加载所有Claw配置"""
        if self._initialized:
            return
        
        logger.info("[ClawRouter] 初始化Claw路由器...")
        
        yaml_files = list(CLAW_CONFIGS_DIR.glob("*.yaml"))
        logger.info(f"[ClawRouter] 找到 {len(yaml_files)} 个Claw配置")
        
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                if not config:
                    continue
                
                claw = ClawInfo(
                    name=config.get("name", yaml_file.stem),
                    department=config.get("department", ""),
                    school=config.get("school", ""),
                    era=config.get("era", ""),
                    tier_name=config.get("tier_name", ""),
                    court_position=config.get("court_position", ""),
                    position_name=config.get("position_name", ""),
                    position_pin=config.get("position_pin", ""),
                    nobility=config.get("nobility", ""),
                    triggers=config.get("triggers", []),
                    wisdom_school=config.get("wisdom_school", ""),
                    can_lead=config.get("collaboration", {}).get("can_lead", True),
                    can_support=config.get("collaboration", {}).get("can_support", True),
                    preferred_role=config.get("collaboration", {}).get("preferred_role", "analyst"),
                )
                
                self._claws[claw.name] = claw
                
                # 建立索引
                dept = claw.department
                if dept:
                    if dept not in self._department_claws:
                        self._department_claws[dept] = []
                    self._department_claws[dept].append(claw.name)
                
                school = claw.school
                if school:
                    if school not in self._school_claws:
                        self._school_claws[school] = []
                    self._school_claws[school].append(claw.name)
                
                # 触发词索引
                for trigger in claw.triggers:
                    trigger_lower = trigger.lower()
                    if trigger_lower not in self._trigger_index:
                        self._trigger_index[trigger_lower] = []
                    self._trigger_index[trigger_lower].append(claw.name)
                    
            except Exception as e:
                logger.warning(f"[ClawRouter] 加载失败 {yaml_file.name}: {e}")
        
        self._initialized = True
        logger.info(f"[ClawRouter] 初始化完成: {len(self._claws)} 个Claw")
    
    def _match_triggers(self, query: str) -> List[Tuple[str, float]]:
        """匹配触发词，返回匹配的Claw及其匹配度"""
        query_lower = query.lower()
        matches = []
        
        for trigger, claw_names in self._trigger_index.items():
            if trigger in query_lower:
                # 计算匹配度：完全匹配 > 包含匹配
                if trigger == query_lower:
                    score = 1.0
                else:
                    score = len(trigger) / len(query_lower)
                
                for claw_name in claw_names:
                    matches.append((claw_name, score))
        
        # 去重并排序
        seen = set()
        unique_matches = []
        for claw_name, score in sorted(matches, key=lambda x: -x[1]):
            if claw_name not in seen:
                seen.add(claw_name)
                unique_matches.append((claw_name, score))
        
        return unique_matches
    
    # ── 路由方法 ─────────────────────────────────────────────────────────────
    
    def route_by_department(
        self,
        department: str,
        query: str,
        include_collaborators: bool = True,
    ) -> ClawRouteResult:
        """
        按部门路由Claw
        
        Args:
            department: 目标部门（如"礼部"、"兵部"）
            query: 用户问题
            include_collaborators: 是否包含协作Claw
            
        Returns:
            ClawRouteResult
        """
        self.initialize()
        
        # 1. 获取部门内所有Claw
        dept_claws = self._department_claws.get(department, [])
        
        if not dept_claws:
            # 尝试模糊匹配
            for dept, claws in self._department_claws.items():
                if department in dept or dept in department:
                    dept_claws = claws
                    department = dept
                    break
        
        if not dept_claws:
            # 回退到全量搜索
            dept_claws = list(self._claws.keys())
            department = "全局"
        
        # 2. 匹配触发词
        trigger_matches = self._match_triggers(query)
        matched_claws = [m[0] for m in trigger_matches if m[0] in dept_claws]
        
        # 3. 选择主Claw
        if matched_claws:
            # 优先选择匹配触发词的Claw，按优先级排序
            primary = max(
                matched_claws,
                key=lambda x: self._claws[x].priority_score
            )
        else:
            # 没有匹配，选择优先级最高的
            primary = max(
                dept_claws,
                key=lambda x: self._claws[x].priority_score
            )
        
        # 4. 选择协作Claw
        collaborators = []
        if include_collaborators and primary in self._claws:
            primary_claw = self._claws[primary]
            
            # 同一学派
            school = primary_claw.school
            school_claws = self._school_claws.get(school, [])
            collaborators.extend([c for c in school_claws if c != primary][:2])
            
            # 同一部门其他Claw
            dept_others = [c for c in dept_claws if c != primary and c not in collaborators]
            collaborators.extend(dept_others[:2])
            
            # 限制数量
            collaborators = collaborators[:3]
        
        return ClawRouteResult(
            primary_claw=primary,
            collaborator_claws=collaborators,
            department=department,
            routing_reason=f"基于部门路由: {department}",
            confidence=0.8 if matched_claws else 0.5,
        )
    
    def route_by_problem_type(
        self,
        problem_type: str,
        query: str,
        department_mapping: Dict[str, str] = None,
    ) -> ClawRouteResult:
        """
        按问题类型路由Claw
        
        根据ProblemType确定部门，再路由到Claw
        """
        self.initialize()
        
        # 默认部门映射
        if department_mapping is None:
            department_mapping = {
                "COMPETITION": "兵部",
                "CRISIS": "兵部",
                "ATTACK": "兵部",
                "DEFENSE": "兵部",
                "NEGOTIATION": "兵部",
                "MARKET_ANALYSIS": "户部",
                "MARKETING": "户部",
                "CONSUMER_MARKETING": "户部",
                "BRAND_STRATEGY": "户部",
                "GROWTH_STRATEGY": "工部",
                "INNOVATION": "工部",
                "TEAM_BUILDING": "吏部",
                "ORGANIZATION": "吏部",
                "LEADERSHIP": "吏部",
                "VALUES": "礼部",
                "EDUCATION": "礼部",
                "CULTURE": "礼部",
                "LEGAL": "刑部",
                "COMPLIANCE": "刑部",
                "RISK": "刑部",
            }
        
        department = department_mapping.get(problem_type, "吏部")
        return self.route_by_department(department, query)
    
    def route_by_query(
        self,
        query: str,
        preferred_department: str = None,
    ) -> ClawRouteResult:
        """
        智能路由：根据问题内容自动选择部门和Claw
        
        这是主要的入口方法，兼容现有WisdomDispatcher
        """
        self.initialize()
        
        # 1. 触发词匹配
        trigger_matches = self._match_triggers(query)
        
        if trigger_matches:
            # 有触发词匹配，选择优先级最高的
            claw_name = max(
                [m[0] for m in trigger_matches],
                key=lambda x: self._claws[x].priority_score
            )
            claw = self._claws[claw_name]
            
            # 找协作Claw
            collaborators = []
            school_claws = self._school_claws.get(claw.school, [])
            collaborators.extend([c for c in school_claws if c != claw_name][:2])
            
            return ClawRouteResult(
                primary_claw=claw_name,
                collaborator_claws=collaborators,
                department=claw.department,
                routing_reason=f"触发词匹配: {[m[0] for m in trigger_matches[:3]]}",
                confidence=0.9,
            )
        
        # 2. 没有触发词匹配，使用指定部门或默认
        if preferred_department:
            return self.route_by_department(preferred_department, query)
        
        # 3. 智能推断部门（基于关键词）
        query_lower = query.lower()
        
        # 军事/竞争相关
        if any(kw in query_lower for kw in ["竞争", "战略", "战争", "攻击", "防守", "谈判"]):
            return self.route_by_department("兵部", query)
        
        # 经济/市场相关
        if any(kw in query_lower for kw in ["市场", "营销", "增长", "用户", "品牌", "销售"]):
            return self.route_by_department("户部", query)
        
        # 思想/文化相关
        if any(kw in query_lower for kw in ["仁", "义", "礼", "智", "信", "道德", "教育", "文化"]):
            return self.route_by_department("礼部", query)
        
        # 组织/管理相关
        if any(kw in query_lower for kw in ["管理", "组织", "领导", "团队", "人才", "制度"]):
            return self.route_by_department("吏部", query)
        
        # 创新/技术相关
        if any(kw in query_lower for kw in ["创新", "技术", "开发", "产品", "设计"]):
            return self.route_by_department("工部", query)
        
        # 默认到礼部（儒家经典问题最多）
        return self.route_by_department("礼部", query)
    
    # ── 统计方法 ─────────────────────────────────────────────────────────────
    
    def get_department_stats(self) -> Dict[str, int]:
        """获取各部门Claw数量"""
        self.initialize()
        return {dept: len(claws) for dept, claws in self._department_claws.items()}
    
    def list_claws_by_department(self, department: str) -> List[Dict[str, Any]]:
        """列出部门内的Claw"""
        self.initialize()
        
        claws = self._department_claws.get(department, [])
        return [
            {
                "name": c.name,
                "tier": c.tier_name,
                "position": c.position_name,
                "priority": c.priority_score,
            }
            for c in sorted(
                [self._claws[name] for name in claws],
                key=lambda x: -x.priority_score
            )
        ]


# ═══════════════════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════════════════

# 全局路由器实例
_claw_router: Optional[ClawRouter] = None

def get_claw_router() -> ClawRouter:
    """获取全局ClawRouter实例"""
    global _claw_router
    if _claw_router is None:
        _claw_router = ClawRouter()
    return _claw_router


def route_claw(
    query: str,
    department: str = None,
    problem_type: str = None,
) -> ClawRouteResult:
    """
    路由Claw的便捷函数
    
    Args:
        query: 用户问题
        department: 指定的部门（可选）
        problem_type: 问题类型（可选）
        
    Returns:
        ClawRouteResult
    """
    router = get_claw_router()
    
    if department:
        return router.route_by_department(department, query)
    elif problem_type:
        return router.route_by_problem_type(problem_type, query)
    else:
        return router.route_by_query(query)


__all__ = [
    "ClawRouter",
    "ClawInfo",
    "ClawRouteResult",
    "get_claw_router",
    "route_claw",
]