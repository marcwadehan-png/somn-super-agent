"""
__all__ = [
    'diagnose_needs_level',
    'get_growth_path',
    'segment_by_needs',
    'track_needs_dynamics',
]

心理学先驱深化引擎 - 马斯洛需求动态系统
Pioneer Maslow - Dynamic Needs System
=====================================
版本: v8.2.0
创建时间: 2026-04-03

马斯洛核心思想:
1. 需求层次理论 - 5层金字塔
2. 自我实现 - 人的最高追求
3. 超越需求 - 超越自我的灵性追求
4. 需求动态 - 需求不是静态的
5. 高峰体验 - 自我实现的瞬间
6. 优善理论 - 防御和成长的辩证

核心功能:
1. 需求层次诊断
2. 需求动态追踪
3. 消费升级预测
4. 用户价值分层
5. 成长路径规划
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

class 需求层次(Enum):
    """马斯洛需求层次"""
    生理需求 = "生理需求"           # 食物,水,睡眠
    安全需求 = "安全需求"           # 安全,稳定,庇护
    社交需求 = "社交需求"           # 归属,友爱,被接纳
    尊重需求 = "尊重需求"           # 成就,尊重,被认可
    认知需求 = "认知需求"           # 知识,理解,好奇心
    审美需求 = "审美需求"           # 对称,美,和谐
    自我实现 = "自我实现"           # 潜能实现,成长
    超越需求 = "超越需求"           # 灵性,意义,宇宙共鸣

class 需求状态(Enum):
    """需求满足状态"""
    极度匮乏 = "极度匮乏"
    轻度匮乏 = "轻度匮乏"
    基本满足 = "基本满足"
    充分满足 = "充分满足"
    过度满足 = "过度满足"

class 马斯洛需求引擎:
    """
    马斯洛需求动态系统
    
    核心功能:
    1. 需求层次诊断 - recognize用户当前主导需求
    2. 需求动态分析 - 追踪需求变化趋势
    3. 消费升级预测 - 预测消费升级路径
    4. 用户价值分层 - 基于需求层次的用户分层
    5. 成长路径规划 - 规划用户成长路径
    """
    
    def __init__(self):
        self.name = "马斯洛需求动态引擎"
        self.version = "8.2.0"
        
        # 需求层次定义
        self.需求层次定义 = {
            需求层次.生理需求: {
                "描述": "维持生存的基本需求",
                "包括": ["食物", "水", "睡眠", "呼吸", "性"],
                "驱动": "生存本能",
                "产品类型": ["食品", "饮料", "住房", "医疗"]
            },
            需求层次.安全需求: {
                "描述": "对稳定,安全,秩序的需求",
                "包括": ["人身安全", "健康", "财产安全", "就业保障"],
                "驱动": "安全感需求",
                "产品类型": ["保险", "安防", "储蓄", "保健"]
            },
            需求层次.社交需求: {
                "描述": "对归属,友谊,爱情的需求",
                "包括": ["友谊", "爱情", "归属感", "社交关系"],
                "驱动": "社交本能",
                "产品类型": ["社交应用", "旅游", "聚会", "礼品"]
            },
            需求层次.尊重需求: {
                "描述": "对成就,地位,被尊重的需求",
                "包括": ["成就", "认可", "尊重", "地位"],
                "驱动": "自我提升需求",
                "产品类型": ["高端品牌", "教育", "奢侈品", "会员"]
            },
            需求层次.认知需求: {
                "描述": "对知识和理解的需求",
                "包括": ["学习", "探索", "好奇心", "理解"],
                "驱动": "认知本能",
                "产品类型": ["教育", "书籍", "课程", "咨询"]
            },
            需求层次.审美需求: {
                "描述": "对美,和谐,秩序的需求",
                "包括": ["美感", "对称", "和谐", "优雅"],
                "驱动": "审美本能",
                "产品类型": ["设计", "艺术", "旅游", "音乐"]
            },
            需求层次.自我实现: {
                "描述": "实现个人潜能的需求",
                "包括": ["成长", "成就", "创造力", "问题解决"],
                "驱动": "自我超越需求",
                "产品类型": ["自我提升", "创作工具", "挑战项目"]
            },
            需求层次.超越需求: {
                "描述": "超越自我,与宇宙连接的需求",
                "包括": ["灵性", "意义", "使命", "宇宙观"],
                "驱动": "灵性需求",
                "产品类型": ["冥想", "心灵成长", "公益", "哲学"]
            }
        }
        
        # 需求characteristics信号
        self.需求信号 = {
            需求层次.生理需求: ["打折", "免费", "量大", "便宜"],
            需求层次.安全需求: ["保障", "安全", "保险", "稳定"],
            需求层次.社交需求: ["分享", "推荐", "一起", "朋友"],
            需求层次.尊重需求: ["限量", "高端", "专属", "VIP"],
            需求层次.认知需求: ["学习", "知道", "了解", "懂得"],
            需求层次.审美需求: ["好看", "设计", "艺术", "美"],
            需求层次.自我实现: ["成长", "突破", "实现", "潜能"],
            需求层次.超越需求: ["意义", "使命", "价值", "贡献"]
        }
    
    def diagnose_needs_level(self, user_data: Dict) -> Dict:
        """
        需求层次诊断
        
        Args:
            user_data: 用户数据
            
        Returns:
            需求诊断结果
        """
        behaviors = user_data.get("behaviors", [])
        purchases = user_data.get("purchases", [])
        interests = user_data.get("interests", [])
        
        # 统计各层次需求信号
        需求得分 = {层次: 0 for 层次 in 需求层次}
        
        all_text = " ".join(behaviors + purchases + interests)
        
        for 层次, signals in self.需求信号.items():
            for signal in signals:
                if signal in all_text:
                    需求得分[层次] += 1
        
        # 确定主导需求
        sorted_needs = sorted(需求得分.items(), key=lambda x: x[1], reverse=True)
        
        主导需求 = sorted_needs[0][0]
        次级需求 = sorted_needs[1][0]
        
        # generate需求画像
        需求画像 = self._generate_needs_profile(sorted_needs)
        
        return {
            "主导需求层次": 主导需求.value,
            "次级需求层次": 次级需求.value,
            "需求层次详情": 需求画像,
            "需求满足状态": self._evaluate_needs_satisfaction(需求画像),
            "消费characteristics": self._generate_consumption_pattern(主导需求, 次级需求),
            "升级预测": self._predict_upgrade_path(主导需求)
        }
    
    def _generate_needs_profile(self, sorted_needs: List) -> Dict:
        """generate需求画像"""
        profile = {}
        for 层次, 得分 in sorted_needs[:5]:
            profile[层次.value] = {
                "得分": 得分,
                "状态": self._estimate_needs_state(得分),
                "characteristics": self.需求层次定义.get(层次, {}).get("描述", ""),
                "驱动力": self.需求层次定义.get(层次, {}).get("驱动", "")
            }
        return profile
    
    def _estimate_needs_state(self, score: int) -> str:
        """评估需求状态"""
        if score == 0:
            return 需求状态.极度匮乏.value
        elif score == 1:
            return 需求状态.轻度匮乏.value
        elif score <= 3:
            return 需求状态.基本满足.value
        elif score <= 5:
            return 需求状态.充分满足.value
        else:
            return 需求状态.过度满足.value
    
    def _evaluate_needs_satisfaction(self, profile: Dict) -> str:
        """评估需求满足状态"""
        满足程度 = []
        for 层次, info in profile.items():
            满足程度.append((层次, info["状态"]))
        
        # 简化judge
        high_satisfaction = sum(1 for _, s in 满足程度 if 需求状态.充分满足.value in s)
        
        if high_satisfaction >= 4:
            return "需求整体满足度高,可能追求更高层次"
        elif high_satisfaction >= 2:
            return "需求满足中等,有提升空间"
        else:
            return "基础需求满足不足,优先关注基础需求"
    
    def _generate_consumption_pattern(self, primary, secondary) -> Dict:
        """generate消费characteristics"""
        return {
            "核心诉求": self.需求层次定义.get(primary, {}).get("驱动", "满足需求"),
            "偏好产品": self.需求层次定义.get(primary, {}).get("产品类型", []),
            "次级诉求": self.需求层次定义.get(secondary, {}).get("驱动", ""),
            "消费升级方向": self._predict_upgrade_direction(primary, secondary)
        }
    
    def _predict_upgrade_direction(self, primary, secondary) -> str:
        """预测升级方向"""
        层次列表 = list(需求层次)
        try:
            primary_idx = 层次列表.index(primary)
            return f"从{primary.value}向{层次列表[min(primary_idx+1, len(层次列表)-1)].value}升级"
        except ValueError:
            return "需求升级路径待确定"
    
    def _predict_upgrade_path(self, current_level: 需求层次) -> List[Dict]:
        """预测消费升级路径"""
        层次列表 = list(需求层次)
        try:
            current_idx = 层次列表.index(current_level)
        except ValueError:
            current_idx = 0
        
        upgrade_path = []
        for i in range(current_idx + 1, len(层次列表)):
            next_level = 层次列表[i]
            upgrade_path.append({
                "下一层次": next_level.value,
                "触发条件": self._get_upgrade_trigger(next_level),
                "机会产品": self.需求层次定义.get(next_level, {}).get("产品类型", []),
                "营销strategy": self._get_marketing_strategy(next_level)
            })
        
        return upgrade_path
    
    def _get_upgrade_trigger(self, level: 需求层次) -> str:
        """get升级触发条件"""
        triggers = {
            需求层次.生理需求: "基础生活保障",
            需求层次.安全需求: "收入稳定,有储蓄",
            需求层次.社交需求: "社交圈扩大",
            需求层次.尊重需求: "社会地位提升",
            需求层次.认知需求: "教育水平提高",
            需求层次.审美需求: "生活品质追求",
            需求层次.自我实现: "自我认知深化",
            需求层次.超越需求: "人生阅历丰富"
        }
        return triggers.get(level, "需求自然升级")
    
    def _get_marketing_strategy(self, level: 需求层次) -> str:
        """get营销strategy"""
        strategies = {
            需求层次.生理需求: "强调性价比,实用性",
            需求层次.安全需求: "强调保障,安全性",
            需求层次.社交需求: "强调社交属性,社群",
            需求层次.尊重需求: "强调稀缺性,独特性",
            需求层次.认知需求: "强调知识价值,学习效果",
            需求层次.审美需求: "强调设计感,艺术性",
            需求层次.自我实现: "强调成长性,成就感",
            需求层次.超越需求: "强调意义,使命感"
        }
        return strategies.get(level, "满足用户需求")
    
    def track_needs_dynamics(self, historical_data: List[Dict]) -> Dict:
        """
        需求动态追踪
        
        Args:
            historical_data: 历史需求数据
            
        Returns:
            需求动态分析
        """
        if not historical_data:
            return {"状态": "数据不足,无法分析"}
        
        # 分析需求变化趋势
        变化趋势 = []
        for i in range(1, len(historical_data)):
            prev = historical_data[i-1]
            curr = historical_data[i]
            
            changes = {}
            for 层次 in 需求层次:
                prev_score = prev.get(层次.value, 0)
                curr_score = curr.get(层次.value, 0)
                change = curr_score - prev_score
                if change != 0:
                    changes[层次.value] = {
                        "变化": change,
                        "方向": "上升" if change > 0 else "下降"
                    }
            
            变化趋势.append({
                "时期": curr.get("period", f"T{i}"),
                "变化": changes
            })
        
        # generate趋势洞察
        洞察 = self._generate_dynamics_insights(变化趋势)
        
        return {
            "需求变化趋势": 变化趋势,
            "主导变化": 洞察,
            "预测": self._predict_future_needs(变化趋势)
        }
    
    def _generate_dynamics_insights(self, trends: List) -> List[str]:
        """generate动态洞察"""
        insights = []
        
        # 简化分析
        for trend in trends:
            changes = trend.get("变化", {})
            for 层次, info in changes.items():
                if info["方向"] == "上升":
                    insights.append(f"{层次}需求正在上升")
                elif info["变化"] < -2:
                    insights.append(f"{层次}需求正在下降")
        
        return insights if insights else ["需求保持稳定"]
    
    def _predict_future_needs(self, trends: List) -> Dict:
        """预测未来需求"""
        if not trends:
            return {"预测": "数据不足"}
        
        # 取最近的趋势
        latest = trends[-1] if trends else {}
        changes = latest.get("变化", {})
        
        rising_needs = []
        for 层次, info in changes.items():
            if info["方向"] == "上升":
                rising_needs.append(层次)
        
        return {
            "预测需求": rising_needs,
            "建议": "提前布局上升需求相关产品"
        }
    
    def segment_by_needs(self, users: List[Dict]) -> Dict:
        """
        基于需求的用户分层
        
        Args:
            users: 用户列表
            
        Returns:
            用户分层结果
        """
        segments = {层次.value: [] for 层次 in 需求层次}
        
        for user in users:
            diagnosis = self.diagnose_needs_level(user)
            primary_level = diagnosis["主导需求层次"]
            
            for 层次 in 需求层次:
                if 层次.value == primary_level:
                    segments[层次.value].append({
                        "user_id": user.get("id", "unknown"),
                        "secondary": diagnosis.get("次级需求层次", ""),
                        "characteristics": diagnosis.get("消费characteristics", {})
                    })
        
        # generate分层报告
        segment_report = []
        for 层次, users_in_segment in segments.items():
            if users_in_segment:
                segment_report.append({
                    "层次": 层次,
                    "用户数": len(users_in_segment),
                    "核心诉求": self.需求层次定义.get(层次, {}).get("描述", ""),
                    "推荐strategy": self._get_marketing_strategy(层次)
                })
        
        return {
            "分层结果": segment_report,
            "分层洞察": self._generate_segment_insights(segment_report)
        }
    
    def _generate_segment_insights(self, segments: List) -> str:
        """generate分层洞察"""
        if not segments:
            return "用户分层完成"
        
        largest_segment = max(segments, key=lambda x: x["用户数"])
        return f"最大用户群体集中在{largest_segment['层次']},建议重点关注"
    
    def get_growth_path(self, user_data: Dict) -> Dict:
        """
        get用户成长路径
        
        Args:
            user_data: 用户数据
            
        Returns:
            成长路径规划
        """
        diagnosis = self.diagnose_needs_level(user_data)
        current_level = diagnosis["主导需求层次"]
        
        # 找到当前层次
        层次列表 = list(需求层次)
        current_level_enum = None
        for 层次 in 层次列表:
            if 层次.value == current_level:
                current_level_enum = 层次
                break
        
        if not current_level_enum:
            return {"错误": "无法确定当前需求层次"}
        
        current_idx = 层次列表.index(current_level_enum)
        
        # 规划成长路径
        growth_path = []
        for i in range(current_idx + 1, len(层次列表)):
            next_level = 层次列表[i]
            growth_path.append({
                "目标层次": next_level.value,
                "层次描述": self.需求层次定义.get(next_level, {}).get("描述", ""),
                "成长标志": self._get_growth_milestone(next_level),
                "成长strategy": self._get_growth_strategy(next_level)
            })
        
        return {
            "当前层次": current_level,
            "成长路径": growth_path,
            "终极目标": "自我实现与超越",
            "成长建议": "循序渐进,逐层满足"
        }
    
    def _get_growth_milestone(self, level: 需求层次) -> str:
        """get成长里程碑"""
        milestones = {
            需求层次.安全需求: "建立稳定的收入和储蓄",
            需求层次.社交需求: "建立稳定的人际关系",
            需求层次.尊重需求: "获得社会认可和成就",
            需求层次.认知需求: "系统学习某一领域",
            需求层次.审美需求: "培养审美品味",
            需求层次.自我实现: "完成个人重要目标",
            需求层次.超越需求: "找到人生使命"
        }
        return milestones.get(level, "需求层次提升")
    
    def _get_growth_strategy(self, level: 需求层次) -> str:
        """get成长strategy"""
        strategies = {
            需求层次.安全需求: "理财规划,风险保障",
            需求层次.社交需求: "主动社交,社群参与",
            需求层次.尊重需求: "技能提升,社会贡献",
            需求层次.认知需求: "持续学习,深度阅读",
            需求层次.审美需求: "艺术修养,生活美学",
            需求层次.自我实现: "挑战自我,突破极限",
            需求层次.超越需求: "心灵修炼,使命探索"
        }
        return strategies.get(level, "满足该层次需求")

# 全局实例
maslow_engine = 马斯洛需求引擎()
