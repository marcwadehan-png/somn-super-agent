"""
__all__ = [
    'export_learning_plan',
    'get_learning_plan_summary',
    'get_learning_roadmap',
    'get_learning_statistics',
    'get_next_learning_batch',
    'get_progress',
    'mark_learning_completed',
    'start_learning_session',
]

持续学习计划
Continuous Learning Plan - 15大赛道头部服务商智能学习路线图

这是一个智能的,敏捷的,持续的学习计划:
- 智能: 自动recognize高价值信息,逻辑judge择优
- 敏捷: 快速迭代,小步快跑
- 持续: 长期跟踪,动态更新
- 择优: 只学习最优实践

15大赛道 x 20家头部 = 300家服务商
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

class LearningPriority(Enum):
    """学习优先级"""
    P0_CRITICAL = "P0-核心赛道"      # 必须优先学习
    P1_IMPORTANT = "P1-重要赛道"     # 重要,尽快学习
    P2_NORMAL = "P2-常规赛道"        # 按计划学习
    P3_NICE = "P3-补充赛道"          # 有余力时学习

class LearningStatus(Enum):
    """学习状态"""
    PENDING = "待学习"
    IN_PROGRESS = "学习中"
    COMPLETED = "已完成"
    NEEDS_UPDATE = "需更新"

@dataclass
class LearningTask:
    """学习任务"""
    provider_name: str
    category: str
    priority: LearningPriority
    status: LearningStatus = LearningStatus.PENDING
    
    # 学习计划
    estimated_hours: float = 2.0  # 预计学习时间
    learning_objectives: List[str] = field(default_factory=list)
    
    # 执行记录
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    learned_capabilities: List[str] = field(default_factory=list)
    confidence_score: float = 0.0
    
    # 质量评估
    data_quality: str = "unknown"  # high/medium/low
    learning_depth: str = "surface"  # surface/deep/comprehensive

@dataclass
class CategoryLearningPlan:
    """赛道学习计划"""
    category: str
    priority: LearningPriority
    providers: List[str]  # 头部服务商列表
    
    # 学习重点
    key_focus_areas: List[str] = field(default_factory=list)
    capability_targets: List[str] = field(default_factory=list)
    
    # 进度跟踪
    tasks: Dict[str, LearningTask] = field(default_factory=dict)
    completed_count: int = 0
    total_count: int = 0
    
    def get_progress(self) -> float:
        """get学习进度"""
        if not self.tasks:
            return 0.0
        completed = sum(1 for t in self.tasks.values() if t.status == LearningStatus.COMPLETED)
        return completed / len(self.tasks)

class ContinuousLearningPlan:
    """
    持续学习主控器
    
    管理15大赛道的300家服务商学习计划
    """
    
    # 15大赛道头部服务商数据
    PROVIDER_CATALOG = {
        "会员体系": {
            "priority": LearningPriority.P0_CRITICAL,
            "providers": [
                "科传智能会员系统", "有赞新零售 CRM", "微盟", "销售易 CRM", "纷享销客 CRM",
                "客如云", "美洽", "企业微信 + WeCom", "悟空 CRM", "Salesforce",
                "南讯客道 CRM", "品氪 SCRM", "拓维云科", "二维火", "逸创云",
                "乔拓云商城", "商派", "银豹", "码云数智", "联蔚数科"
            ],
            "focus_areas": ["会员生命周期管理", "积分体系设计", "分层运营strategy", "私域沉淀"],
            "capability_targets": ["全渠道打通能力", "AI智能推荐", "自动化营销"]
        },
        "数字化运营": {
            "priority": LearningPriority.P0_CRITICAL,
            "providers": [
                "深德科", "用友", "金蝶", "明源云", "帆软",
                "联蔚数科", "宝尊电商", "壹网壹创", "若羽臣", "青木科技",
                "丽人丽妆", "碧橙数字", "火奴数据", "百秋尚美", "凯诘电商",
                "杭州网创", "品融电商", "瑞金麟", "网营科技", "四九八科技"
            ],
            "focus_areas": ["数据中台建设", "运营流程自动化", "decision智能化", "全链路数字化"],
            "capability_targets": ["数据整合能力", "流程引擎", "BI分析"]
        },
        "数字化转型": {
            "priority": LearningPriority.P0_CRITICAL,
            "providers": [
                "华为技术", "阿里巴巴集团", "字节跳动", "腾讯控股", "浪潮数字企业",
                "中国电信", "中国移动", "中国联通", "京东集团", "中兴通讯",
                "百度", "金山办公", "用友网络", "东软集团", "紫光股份",
                "小米集团", "神州数码", "启明星辰", "太极计算机", "三六零"
            ],
            "focus_areas": ["企业级架构", "云原生转型", "智能化升级", "生态协同"],
            "capability_targets": ["架构咨询", "实施交付", "生态整合"]
        },
        "整合营销": {
            "priority": LearningPriority.P1_IMPORTANT,
            "providers": [
                "北京海唐新媒集团", "上海胜加广告", "华与华营销咨询", "杭州有氧文化", "赞意互动",
                "时趣互动", "环时互动", "剧星传媒", "欧赛斯", "群邑中国",
                "阳狮媒体", "李奥贝纳", "蓝色光标", "省广集团", "华扬联众",
                "君智咨询", "新意互动", "因赛集团", "多想互动", "璞康"
            ],
            "focus_areas": ["全链路营销", "品牌strategy", "创意内容", "媒介整合"],
            "capability_targets": ["strategy规划", "创意产出", "资源整合"]
        },
        "小红书运营": {
            "priority": LearningPriority.P1_IMPORTANT,
            "providers": [
                "众引传播", "侵尘文化", "微思敦", "蓝色光标", "微盟",
                "省广集团", "华扬联众", "易点天下", "珍岛集团", "天下秀",
                "博雅公关", "布马", "小花猫", "融趣传媒", "玖叁鹿数字",
                "天擎天拓", "遥望网络", "新榜", "品氪", "联蔚数科"
            ],
            "focus_areas": ["种草内容strategy", "KOL矩阵", "搜索优化", "社区运营"],
            "capability_targets": ["内容创作", "达人资源", "数据分析"]
        },
        "抖音运营": {
            "priority": LearningPriority.P1_IMPORTANT,
            "providers": [
                "杭州亿馨网络", "宝尊电商", "壹网壹创", "丽人丽妆", "若羽臣",
                "青木科技", "碧橙数字", "悠可集团", "融趣传媒", "智麦电商",
                "交个朋友", "遥望科技", "无忧传媒", "祈飞网络", "聚星电商",
                "创科传媒", "优途电商", "星脉数字", "启梦传媒", "盛景电商"
            ],
            "focus_areas": ["直播运营", "短视频内容", "投流strategy", "达人合作"],
            "capability_targets": ["直播能力", "内容制作", "流量运营"]
        },
        "AI增长": {
            "priority": LearningPriority.P0_CRITICAL,
            "providers": [
                "百分点科技", "虎博科技", "智推时代", "森辰 GEO", "大树科技",
                "百度智能云", "新榜智汇", "探小星 GEO", "科大讯飞", "商汤科技",
                "智谱华章", "面壁智能", "极光", "洞见科技", "滴普科技",
                "阶跃星辰", "博特智能", "百川智能", "蚂蚁数科", "启迪问智"
            ],
            "focus_areas": ["AI营销", "智能推荐", "预测分析", "自动化decision"],
            "capability_targets": ["算法能力", "模型训练", "场景落地"]
        },
        "O2O运营": {
            "priority": LearningPriority.P1_IMPORTANT,
            "providers": [
                "美团", "饿了么", "大众点评", "携程商旅", "娟娟科技",
                "小达科技", "携旅集团", "直订网", "携住科技", "鹊问健康",
                "艾特互动", "九盈科技", "优兔互联", "杏墨科技", "哗啦啦",
                "客如云", "掌贝", "零一数科", "食亨", "餐道"
            ],
            "focus_areas": ["线上线下fusion", "本地生活", "到店引流", "即时配送"],
            "capability_targets": ["LBS能力", "履约系统", "商户运营"]
        },
        "新零售": {
            "priority": LearningPriority.P1_IMPORTANT,
            "providers": [
                "阿里巴巴", "有赞", "微盟", "多点 Dmall", "哗啦啦",
                "客如云", "用友 YonBIP", "金蝶云星辰", "美咖", "掌贝",
                "吉客云", "科脉", "思迅软件", "鼎捷数智", "云从科技",
                "小鹅通", "明略科技", "第四范式", "汇纳科技", "极易科技"
            ],
            "focus_areas": ["人货场重构", "全渠道fusion", "智能门店", "供应链优化"],
            "capability_targets": ["门店数字化", "库存打通", "会员通"]
        },
        "跨境电商": {
            "priority": LearningPriority.P1_IMPORTANT,
            "providers": [
                "卓志集团", "珊瑚跨境", "世贸通", "泛鼎国际", "价之链",
                "易芽", "来赞宝", "海比电商", "纵腾集团", "西邮物流",
                "燕文物流", "递四方", "菜鸟国际", "至美通", "泛远国际",
                "乐舱物流", "安骏物流", "飞盒跨境", "海管家", "易达云科技"
            ],
            "focus_areas": ["海外仓配", "跨境支付", "合规服务", "本地化运营"],
            "capability_targets": ["物流网络", "清关能力", "海外资源"]
        },
        "直播电商": {
            "priority": LearningPriority.P1_IMPORTANT,
            "providers": [
                "索象", "遥望科技", "无忧传媒", "交个朋友", "谦寻",
                "美腕", "如涵控股", "壹网壹创", "青木股份", "嘉乐东立",
                "蝉妈妈电商服务", "宝尊电商", "丽人丽妆", "若羽臣", "碧橙数字",
                "悠可集团", "融趣传媒", "智麦电商", "聚星电商", "创科传媒"
            ],
            "focus_areas": ["主播孵化", "直播运营", "供应链整合", "流量投放"],
            "capability_targets": ["主播资源", "运营SOP", "选品能力"]
        },
        "KOL营销": {
            "priority": LearningPriority.P2_NORMAL,
            "providers": [
                "因赛集团", "微播易", "众引传播", "热点营销 Hotlist", "映马传媒 InsMark",
                "Genflow", "Viral Nation", "IMF", "华彩汽车传播", "大鱼出海",
                "蓝色光标", "省广集团", "华扬联众", "天下秀", "新榜",
                "微思敦", "侵尘文化", "玖叁鹿数字", "天擎天拓", "联蔚数科"
            ],
            "focus_areas": ["达人筛选", "内容共创", "效果监测", "长期合作"],
            "capability_targets": ["达人库", "匹配算法", "效果追踪"]
        },
        "品牌建设": {
            "priority": LearningPriority.P1_IMPORTANT,
            "providers": [
                "Interbrand", "Prophet 铂慧", "朗标集团", "MetaThink 根元咨询", "君智战略咨询",
                "华与华", "里斯咨询", "和君咨询", "奇正沐古", "奥纬咨询",
                "艾瑞咨询", "北大纵横", "华夏咨询", "思美股份", "爱德曼",
                "宣亚国际", "嘉利公关", "灵思云途", "同心动力", "罗兰贝格"
            ],
            "focus_areas": ["品牌定位", "视觉recognize", "品牌故事", "声誉管理"],
            "capability_targets": ["strategy咨询", "创意设计", "公关传播"]
        },
        "数据驱动营销": {
            "priority": LearningPriority.P0_CRITICAL,
            "providers": [
                "百分点科技", "秒针系统", "神策数据", "GrowingIO", "致趣百川",
                "火眼云", "MarketUP", "ConvertLab", "HubSpot", "Salesforce",
                "爱点击", "华扬联众", "智驰创科", "森辰 GEO", "大树科技",
                "百度智能云", "新榜智汇", "探小星 GEO", "明略科技", "第四范式"
            ],
            "focus_areas": ["数据采集", "用户画像", "归因分析", "预测模型"],
            "capability_targets": ["CDP", "MA", "BI分析"]
        },
        "软件系统/解决方案": {
            "priority": LearningPriority.P0_CRITICAL,
            "providers": [
                "Salesforce", "HubSpot", "Microsoft Dynamics 365", "SAP CX", "Oracle CX",
                "Zoho CRM", "销售易", "纷享销客", "悟空 CRM", "MarketUP",
                "鲸奇 SCRM", "致趣百川", "有赞", "微盟", "用友",
                "金蝶", "明源云", "帆软", "联蔚数科", "品氪 SCRM"
            ],
            "focus_areas": ["CRM/SCRM", "营销自动化", "数据分析", "客户旅程"],
            "capability_targets": ["产品成熟度", "集成能力", "定制开发"]
        }
    }
    
    def __init__(self):
        self.plans: Dict[str, CategoryLearningPlan] = {}
        self._init_plans()
    
    def _init_plans(self):
        """init学习计划"""
        for category, config in self.PROVIDER_CATALOG.items():
            plan = CategoryLearningPlan(
                category=category,
                priority=config["priority"],
                providers=config["providers"],
                key_focus_areas=config["focus_areas"],
                capability_targets=config["capability_targets"],
                total_count=len(config["providers"])
            )
            
            # 为每个服务商创建学习任务
            for provider in config["providers"]:
                task = LearningTask(
                    provider_name=provider,
                    category=category,
                    priority=config["priority"],
                    learning_objectives=config["focus_areas"][:3]
                )
                plan.tasks[provider] = task
            
            self.plans[category] = plan
    
    def get_learning_roadmap(self) -> Dict[str, Any]:
        """get学习路线图"""
        roadmap = {
            "generated_at": datetime.now().isoformat(),
            "total_providers": sum(p.total_count for p in self.plans.values()),
            "total_categories": len(self.plans),
            "phases": []
        }
        
        # 按优先级分组
        for priority in [LearningPriority.P0_CRITICAL, LearningPriority.P1_IMPORTANT, 
                        LearningPriority.P2_NORMAL, LearningPriority.P3_NICE]:
            phase_providers = []
            for plan in self.plans.values():
                if plan.priority == priority:
                    phase_providers.extend([
                        {"name": t.provider_name, "category": t.category, "status": t.status.value}
                        for t in plan.tasks.values()
                    ])
            
            if phase_providers:
                roadmap["phases"].append({
                    "priority": priority.value,
                    "provider_count": len(phase_providers),
                    "providers": phase_providers[:10]  # 只显示前10个
                })
        
        return roadmap
    
    def get_next_learning_batch(self, batch_size: int = 5) -> List[LearningTask]:
        """get下一批学习任务"""
        pending_tasks = []
        
        # 按优先级收集待学习的服务商
        for priority in [LearningPriority.P0_CRITICAL, LearningPriority.P1_IMPORTANT,
                        LearningPriority.P2_NORMAL, LearningPriority.P3_NICE]:
            for plan in self.plans.values():
                if plan.priority == priority:
                    for task in plan.tasks.values():
                        if task.status == LearningStatus.PENDING:
                            pending_tasks.append(task)
        
        return pending_tasks[:batch_size]
    
    def mark_learning_completed(self, category: str, provider: str, 
                                learned_data: Dict[str, Any]):
        """标记学习完成"""
        if category in self.plans and provider in self.plans[category].tasks:
            task = self.plans[category].tasks[provider]
            task.status = LearningStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()
            task.learned_capabilities = learned_data.get("capabilities", [])
            task.confidence_score = learned_data.get("confidence", 0.0)
            task.data_quality = learned_data.get("data_quality", "medium")
            task.learning_depth = learned_data.get("depth", "surface")
            
            # 更新完成计数
            self.plans[category].completed_count += 1
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """get学习统计"""
        stats = {
            "total_providers": 0,
            "completed": 0,
            "in_progress": 0,
            "pending": 0,
            "by_priority": {},
            "by_category": {}
        }
        
        for plan in self.plans.values():
            cat_stats = {"total": plan.total_count, "completed": 0, "progress": 0.0}
            
            for task in plan.tasks.values():
                stats["total_providers"] += 1
                
                if task.status == LearningStatus.COMPLETED:
                    stats["completed"] += 1
                    cat_stats["completed"] += 1
                elif task.status == LearningStatus.IN_PROGRESS:
                    stats["in_progress"] += 1
                else:
                    stats["pending"] += 1
            
            cat_stats["progress"] = plan.get_progress()
            stats["by_category"][plan.category] = cat_stats
            
            # 按优先级统计
            priority_key = plan.priority.value
            if priority_key not in stats["by_priority"]:
                stats["by_priority"][priority_key] = {"total": 0, "completed": 0}
            stats["by_priority"][priority_key]["total"] += plan.total_count
            stats["by_priority"][priority_key]["completed"] += cat_stats["completed"]
        
        stats["completion_rate"] = stats["completed"] / max(stats["total_providers"], 1)
        
        return stats
    
    def export_learning_plan(self, output_path: str):
        """导出学习计划"""
        plan_data = {
            "created_at": datetime.now().isoformat(),
            "categories": {}
        }
        
        for category, plan in self.plans.items():
            plan_data["categories"][category] = {
                "priority": plan.priority.value,
                "total_providers": plan.total_count,
                "completed": plan.completed_count,
                "progress": plan.get_progress(),
                "focus_areas": plan.key_focus_areas,
                "providers": [
                    {
                        "name": t.provider_name,
                        "status": t.status.value,
                        "confidence": t.confidence_score,
                        "completed_at": t.completed_at
                    }
                    for t in plan.tasks.values()
                ]
            }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(plan_data, f, ensure_ascii=False, indent=2)
        
        return plan_data

# ==================== 便捷使用接口 ====================

def get_learning_plan_summary() -> Dict[str, Any]:
    """get学习计划摘要"""
    plan = ContinuousLearningPlan()
    stats = plan.get_learning_statistics()
    roadmap = plan.get_learning_roadmap()
    
    return {
        "overview": {
            "total_providers": stats["total_providers"],
            "completion_rate": f"{stats['completion_rate']:.1%}",
            "completed": stats["completed"],
            "pending": stats["pending"]
        },
        "by_priority": stats["by_priority"],
        "roadmap_phases": len(roadmap["phases"]),
        "next_batch": [
            {"name": t.provider_name, "category": t.category}
            for t in plan.get_next_learning_batch(5)
        ]
    }

def start_learning_session(batch_size: int = 3) -> Dict[str, Any]:
    """启动学习会话"""
    plan = ContinuousLearningPlan()
    batch = plan.get_next_learning_batch(batch_size)
    
    return {
        "session_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "batch_size": len(batch),
        "tasks": [
            {
                "provider": t.provider_name,
                "category": t.category,
                "priority": t.priority.value,
                "objectives": t.learning_objectives,
                "estimated_hours": t.estimated_hours
            }
            for t in batch
        ],
        "instructions": [
            "1. 访问服务商官网,了解核心产品/服务",
            "2. 查找客户案例,提取成功要素",
            "3. 分析技术架构,recognize差异化优势",
            "4. 整理PPT/提案能力特点",
            "5. 总结可学习借鉴的最佳实践"
        ]
    }

# ==================== 测试示例 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
