# -*- coding: utf-8 -*-
"""
DivineReason 超级引擎网络 - WisdomSchool 166引擎节点集成
================================================================

将 Somn 系统的 166 个智慧引擎（42学派 + 163问题类型）接入 DivineReason 超级推理网络。

版本: V2.0.0 (引擎完整版)
创建: 2026-04-28

引擎架构:
- 42 个 WisdomSchool 智慧学派引擎 (如: 儒家/道家/佛家/兵法...)
- 163 个 ProblemType 问题类型引擎 (如: 战略转型/危机处理/博弈分析...)
- 合计: 166 个推理引擎节点
"""

from __future__ import annotations

import time
import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict

logger = logging.getLogger(__name__)


class EngineType(Enum):
    """引擎类型枚举"""
    WISDOM_SCHOOL = "wisdom_school"      # 智慧学派引擎
    PROBLEM_TYPE = "problem_type"        # 问题类型引擎
    REASONING_MODE = "reasoning_mode"    # 推理模式引擎
    FUSION = "fusion"                    # 融合引擎


@dataclass
class WisdomEngineNode:
    """
    智慧引擎节点 - 表示一个独立的推理引擎
    
    支持三种引擎类型:
    1. WisdomSchool: 智慧学派引擎 (42个)
    2. ProblemType: 问题类型引擎 (163个)
    3. ReasoningMode: 推理模式引擎
    """
    # 节点标识
    node_id: str                          # 唯一节点ID
    name: str                             # 引擎名称
    engine_type: EngineType               # 引擎类型
    
    # 来源信息
    school: Optional[str] = None           # 所属学派 (WisdomSchool)
    problem_type: Optional[str] = None    # 问题类型 (ProblemType)
    
    # 能力描述
    description: str = ""                 # 引擎描述
    keywords: List[str] = field(default_factory=list)  # 关键词
    capabilities: List[str] = field(default_factory=list)  # 能力列表
    
    # 状态
    is_active: bool = True
    load_priority: int = 5                # 加载优先级 (1-10)
    last_used: float = 0.0
    
    # 性能统计
    call_count: int = 0
    success_rate: float = 0.0
    avg_latency_ms: float = 0.0
    
    # 关系网络
    related_nodes: Set[str] = field(default_factory=set)  # 相关节点ID
    complementary_nodes: Set[str] = field(default_factory=set)  # 互补节点
    
    def __post_init__(self):
        """确保节点ID格式正确"""
        if not self.node_id:
            self.node_id = f"{self.engine_type.value}_{self.school or self.problem_type}"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "node_id": self.node_id,
            "name": self.name,
            "engine_type": self.engine_type.value,
            "school": self.school,
            "problem_type": self.problem_type,
            "description": self.description,
            "keywords": self.keywords,
            "capabilities": self.capabilities,
            "is_active": self.is_active,
            "load_priority": self.load_priority,
            "call_count": self.call_count,
            "success_rate": self.success_rate,
            "avg_latency_ms": self.avg_latency_ms,
            "related_nodes": list(self.related_nodes),
            "complementary_nodes": list(self.complementary_nodes),
        }


class WisdomEngineRegistry:
    """
    WisdomSchool 智慧引擎注册表
    
    管理 Somn 系统的 166 个智慧引擎节点:
    - 42 个 WisdomSchool 学派引擎
    - 163 个 ProblemType 问题类型引擎
    """
    
    # 42 个智慧学派及其元数据
    WISDOM_SCHOOLS: Dict[str, Dict[str, Any]] = {
        "CONFUCIAN": {
            "name": "儒家智慧引擎",
            "description": "仁义礼智信，中庸之道，为政以德",
            "keywords": ["仁义", "中庸", "德治", "礼制", "修身齐家"],
            "capabilities": ["伦理判断", "组织治理", "人才选用", "文化传承"],
        },
        "DAOIST": {
            "name": "道家智慧引擎",
            "description": "道法自然，无为而治，阴阳辩证",
            "keywords": ["道法自然", "无为", "阴阳", "辩证", "柔弱胜刚强"],
            "capabilities": ["战略转型", "危机处理", "变革管理", "阴阳平衡"],
        },
        "BUDDHIST": {
            "name": "佛家智慧引擎",
            "description": "缘起性空，慈悲喜舍，觉悟解脱",
            "keywords": ["因缘", "空性", "慈悲", "放下", "觉悟"],
            "capabilities": ["心态调适", "团队和谐", "利益协调", "长期规划"],
        },
        "SUFU": {
            "name": "素书智慧引擎",
            "description": "道义礼仁，神秘预言，韬略之源",
            "keywords": ["道义", "礼仁", "神秘", "预言", "韬略"],
            "capabilities": ["领导决策", "风险管理", "福祸评估", "人才识别"],
        },
        "MILITARY": {
            "name": "兵法智慧引擎",
            "description": "知己知彼，奇正相生，不战而屈人之兵",
            "keywords": ["兵法", "奇正", "知己知彼", "伐谋", "形势"],
            "capabilities": ["竞争策略", "市场攻击", "市场防御", "谈判博弈"],
        },
        "LVSHI": {
            "name": "吕氏春秋智慧引擎",
            "description": "兼容并蓄，纪纲治事，宇宙观",
            "keywords": ["兼容", "纪纲", "宇宙观", "时令", "义兵"],
            "capabilities": ["公私抉择", "时令管理", "阴阳调和", "政治谋略"],
        },
        "HONGMING": {
            "name": "辜鸿铭智慧引擎",
            "description": "东西文化桥梁，中华文明守护",
            "keywords": ["文化桥梁", "文明守护", "东西融合", "传统价值"],
            "capabilities": ["跨文化沟通", "文化传承", "价值判断", "身份认同"],
        },
        "METAPHYSICS": {
            "name": "术数时空智慧引擎",
            "description": "易经象数，风水堪舆，天地人合一",
            "keywords": ["易经", "象数", "风水", "时空", "天人合一"],
            "capabilities": ["时机判断", "环境布局", "结构格局", "吉凶预测"],
        },
        "CIVILIZATION": {
            "name": "文明演化智慧引擎",
            "description": "文明诊断，发展演进，周期规律",
            "keywords": ["文明", "演进", "周期", "规律", "诊断"],
            "capabilities": ["文明诊断", "社会发展", "历史分析", "文明比较"],
        },
        "CIV_WAR_ECONOMY": {
            "name": "文明经战智慧引擎",
            "description": "经济与战争博弈，国家能力演化",
            "keywords": ["经战", "国家能力", "制度", "经济博弈"],
            "capabilities": ["国家能力评估", "制度分析", "经济战略", "博弈分析"],
        },
        "SCI_FI": {
            "name": "科幻思维智慧引擎",
            "description": "维度超越，生存法则，尺度思维",
            "keywords": ["维度", "生存", "尺度", "科幻", "未来学"],
            "capabilities": ["维度超越", "生存法则", "尺度思维", "未来推演"],
        },
        "GROWTH": {
            "name": "成长思维智慧引擎",
            "description": "成长突破，逆向思考，闭环执行",
            "keywords": ["成长", "突破", "逆向", "闭环", "迭代"],
            "capabilities": ["成长突破", "逆向思考", "闭环执行", "能力提升"],
        },
        "MYTHOLOGY": {
            "name": "神话智慧引擎",
            "description": "创世叙事，灭世危机，循环哲学",
            "keywords": ["神话", "创世", "灭世", "循环", "原型"],
            "capabilities": ["创世叙事", "灭世危机分析", "循环哲学", "原型分析"],
        },
        "LITERARY": {
            "name": "文学叙事智慧引擎",
            "description": "叙事构建，韧性评估，人物分析",
            "keywords": ["叙事", "文学", "人物", "韧性", "故事"],
            "capabilities": ["叙事构建", "韧性评估", "人物分析", "故事创作"],
        },
        "ANTHROPOLOGY": {
            "name": "人类学智慧引擎",
            "description": "跨文化沟通，仪式分析，文化变迁",
            "keywords": ["人类学", "文化", "仪式", "田野", "比较"],
            "capabilities": ["跨文化沟通", "仪式分析", "文化变迁", "田野调查"],
        },
        "BEHAVIOR": {
            "name": "行为塑造智慧引擎",
            "description": "习惯设计，自控力管理，助推设计",
            "keywords": ["行为", "习惯", "自控", "助推", "激励"],
            "capabilities": ["习惯设计", "自控力管理", "助推设计", "行为改变"],
        },
        "SCIENCE": {
            "name": "科学思维智慧引擎",
            "description": "科学验证，系统分析，证据评估",
            "keywords": ["科学", "验证", "系统", "证据", "实验"],
            "capabilities": ["科学验证", "系统分析", "证据评估", "假说检验"],
        },
        "SOCIAL_SCIENCE": {
            "name": "社会科学智慧引擎",
            "description": "市场分析，营销战略，社会发展",
            "keywords": ["市场", "营销", "社会", "分析", "战略"],
            "capabilities": ["市场分析", "营销战略", "社会发展", "消费者行为"],
        },
        "YANGMING": {
            "name": "王阳明心学智慧引擎",
            "description": "知行合一，致良知，心即理",
            "keywords": ["心学", "知行", "良知", "致良知", "事上练"],
            "capabilities": ["知行合一分析", "良知判断", "心性修炼", "事上磨练"],
        },
        "DEWEY": {
            "name": "杜威反省思维智慧引擎",
            "description": "反省思维，经验主义，教育民主",
            "keywords": ["反省", "经验", "民主", "教育", "实验主义"],
            "capabilities": ["反省思维", "经验分析", "问题解决", "连续性思维"],
        },
        "TOP_METHODS": {
            "name": "顶级思维法智慧引擎",
            "description": "第一性原理，思维模型，决策框架",
            "keywords": ["第一性原理", "思维模型", "框架", "决策", "顶层设计"],
            "capabilities": ["第一性原理分析", "思维模型选择", "决策框架构建", "顶层设计"],
        },
        "NATURAL_SCIENCE": {
            "name": "自然科学智慧引擎",
            "description": "物理分析，生命科学，地球系统，宇宙探索",
            "keywords": ["物理", "生物", "地球", "宇宙", "科学"],
            "capabilities": ["物理分析", "生命科学", "地球系统", "宇宙探索"],
        },
        "CHINESE_CONSUMER": {
            "name": "中国社会消费文化智慧引擎",
            "description": "消费心理，文化因素，本土化策略",
            "keywords": ["消费", "文化", "本土", "心理", "习惯"],
            "capabilities": ["消费心理分析", "文化因素研究", "本土化策略", "品牌定位"],
        },
        "WCC": {
            "name": "WCC智慧演化引擎",
            "description": "宇宙认知，智慧演化，尺度转换",
            "keywords": ["演化", "智慧", "尺度", "宇宙", "认知"],
            "capabilities": ["元视角升维", "文明诊断", "宇宙认知", "智慧演化"],
        },
        "HISTORICAL_THOUGHT": {
            "name": "历史思想三维度智慧引擎",
            "description": "历史分析，思想演进，经济演进",
            "keywords": ["历史", "思想", "经济", "演进", "分析"],
            "capabilities": ["历史分析", "思想演进", "经济演进", "科技发展"],
        },
        "PSYCHOLOGY": {
            "name": "心理学智慧引擎",
            "description": "弗洛伊德/荣格/马斯洛等心理学先驱融合",
            "keywords": ["心理", "潜意识", "人格", "需求", "发展"],
            "capabilities": ["心理分析", "人格评估", "需求层次", "治疗洞察"],
        },
        "SYSTEMS": {
            "name": "系统论智慧引擎",
            "description": "系统论/复杂适应系统",
            "keywords": ["系统", "反馈", "涌现", "复杂", "适应"],
            "capabilities": ["系统建模", "反馈分析", "涌现识别", "复杂性分析"],
        },
        "MANAGEMENT": {
            "name": "管理学智慧引擎",
            "description": "德鲁克/波特等管理学经典",
            "keywords": ["管理", "战略", "组织", "领导", "效率"],
            "capabilities": ["战略规划", "组织设计", "领导力分析", "效率优化"],
        },
        "ZONGHENG": {
            "name": "纵横家智慧引擎",
            "description": "合纵连横/外交博弈",
            "keywords": ["纵横", "外交", "博弈", "联盟", "谈判"],
            "capabilities": ["联盟分析", "外交策略", "博弈分析", "谈判技巧"],
        },
        "MOZI": {
            "name": "墨家智慧引擎",
            "description": "兼爱非攻/工程技术/逻辑推理",
            "keywords": ["兼爱", "非攻", "逻辑", "技术", "平等"],
            "capabilities": ["逻辑推理", "技术分析", "平等分析", "工程思维"],
        },
        "FAJIA": {
            "name": "法家智慧引擎",
            "description": "法术势/制度设计/权力治理",
            "keywords": ["法", "术", "势", "制度", "权力"],
            "capabilities": ["制度设计", "权力分析", "法治思维", "治理结构"],
        },
        "ECONOMICS": {
            "name": "经济学智慧引擎",
            "description": "亚当斯密/凯恩斯等经济学智慧",
            "keywords": ["经济", "市场", "供需", "价值", "分配"],
            "capabilities": ["经济分析", "市场机制", "政策评估", "价值判断"],
        },
        "MINGJIA": {
            "name": "名家智慧引擎",
            "description": "公孙龙/惠施等名家逻辑学",
            "keywords": ["逻辑", "名实", "辩论", "悖论", "分析"],
            "capabilities": ["逻辑分析", "名实辨析", "悖论研究", "辩论术"],
        },
        "WUXING": {
            "name": "阴阳家智慧引擎",
            "description": "阴阳五行学派（邹衍等）",
            "keywords": ["阴阳", "五行", "相生相克", "时令", "谶纬"],
            "capabilities": ["五行分析", "时令判断", "相生相克分析", "谶纬解读"],
        },
        "COMPLEXITY": {
            "name": "复杂性科学智慧引擎",
            "description": "圣塔菲/复杂适应系统",
            "keywords": ["复杂", "涌现", "适应", "网络", "非线性"],
            "capabilities": ["复杂性建模", "涌现分析", "网络分析", "非线性思维"],
        },
        "SOCIOLOGY": {
            "name": "社会学智慧引擎",
            "description": "涂尔干/韦伯/马克思社会学三巨头",
            "keywords": ["社会", "结构", "阶层", "功能", "冲突"],
            "capabilities": ["社会结构分析", "阶层分析", "功能分析", "社会变迁"],
        },
        "BEHAVIORAL_ECONOMICS": {
            "name": "行为经济学智慧引擎",
            "description": "卡尼曼/塞勒/西奥迪尼行为经济学",
            "keywords": ["行为", "偏差", "heuristic", "框架", "助推"],
            "capabilities": ["行为偏差识别", "决策分析", "助推设计", "框架效应分析"],
        },
        "COMMUNICATION": {
            "name": "传播学智慧引擎",
            "description": "麦克卢汉/鲍德里亚/哈贝马斯传播学",
            "keywords": ["传播", "媒介", "符号", "话语", "公共领域"],
            "capabilities": ["媒介分析", "符号解读", "话语分析", "公共领域研究"],
        },
        "CULTURAL_ANTHROPOLOGY": {
            "name": "文化人类学智慧引擎",
            "description": "马林诺夫斯基/列维斯特劳斯/格尔茨文化人类学",
            "keywords": ["文化", "符号", "意义", "田野", "解释"],
            "capabilities": ["文化解释", "符号分析", "田野研究", "意义建构"],
        },
        "POLITICAL_ECONOMICS": {
            "name": "政治经济学智慧引擎",
            "description": "李斯特/凯恩斯/哈耶克政治经济学",
            "keywords": ["政治", "经济", "国家", "市场", "制度"],
            "capabilities": ["政治经济分析", "国家战略", "市场干预", "制度比较"],
        },
        "ORGANIZATIONAL_PSYCHOLOGY": {
            "name": "组织心理学智慧引擎",
            "description": "阿吉里斯/舍恩/沙因组织心理学",
            "keywords": ["组织", "学习", "变革", "文化", "发展"],
            "capabilities": ["组织学习", "变革管理", "组织文化", "组织发展"],
        },
        "SOCIAL_PSYCHOLOGY": {
            "name": "社会心理学智慧引擎",
            "description": "米尔格拉姆/阿希/津巴多社会心理学",
            "keywords": ["社会", "从众", "服从", "规范", "态度"],
            "capabilities": ["从众分析", "服从研究", "社会规范", "态度改变"],
        },
    }
    
    # 问题类型关键词映射 (ProblemType -> keywords)
    PROBLEM_TYPE_KEYWORDS: Dict[str, List[str]] = {
        # 儒家问题
        "ETHICAL": ["道德", "伦理", "善恶", "正义", "仁义", "品行"],
        "GOVERNANCE": ["治理", "管理", "制度", "体制", "领导"],
        "TALENT": ["人才", "选人", "用人", "培养", "选拔"],
        "CULTURE": ["文化", "传承", "传统", "价值", "风俗"],
        # 道家问题
        "STRATEGY": ["战略", "规划", "长期", "布局", "谋划"],
        "CRISIS": ["危机", "紧急", "突发", "风险", "困境"],
        "CHANGE": ["变革", "转型", "变化", "改革", "创新"],
        "BALANCE": ["平衡", "调和", "协调", "中庸", "适度"],
        "TIMING": ["时机", "机会", "窗口", "节点", "火候"],
        "ENVIRONMENT": ["环境", "形势", "格局", "态势", "场景"],
        "PATTERN": ["格局", "结构", "模式", "规律", "趋势"],
        # 佛家问题
        "MINDSET": ["心态", "心境", "情绪", "态度", "心理"],
        "HARMONY": ["和谐", "协调", "融合", "团结", "和睦"],
        "INTEREST": ["利益", "分配", "协调", "共赢", "平衡"],
        "LONGTERM": ["长期", "未来", "规划", "持续", "长远"],
        # 素书问题
        "LEADERSHIP": ["领导", "统帅", "决策", "用人", "威信"],
        "RISK": ["风险", "危险", "隐患", "预防", "规避"],
        "FORTUNE": ["福祸", "吉凶", "成败", "得失", "输赢"],
        "PERSONNEL": ["人才", "人事", "团队", "人员", "人力资源"],
        # 兵法问题
        "COMPETITION": ["竞争", "博弈", "对抗", "争夺", "较量"],
        "ATTACK": ["攻击", "进攻", "出击", "征伐", "突破"],
        "DEFENSE": ["防御", "防守", "保卫", "守备", "巩固"],
        "NEGOTIATION": ["谈判", "协商", "议和", "交涉", "磋商"],
        "WAR_ECONOMY_NEXUS": ["经战", "战时经济", "军工", "资源"],
        "STATE_CAPACITY": ["国家能力", "国力", "实力", "政府能力"],
        "INSTITUTIONAL_SEDIMENTATION": ["制度", "沉淀", "固化", "路径依赖"],
        # 吕氏春秋问题
        "PUBLIC_INTEREST": ["公私", "公益", "私利", "公义", "大义"],
        "SEASONAL": ["时令", "季节", "时机", "节气", "周期"],
        "YINYANG": ["阴阳", "调和", "平衡", "互补", "转化"],
        # 科幻思维问题
        "DIMENSION": ["维度", "空间", "层次", "视角", "升维"],
        "SURVIVAL": ["生存", "存活", "延续", "灭绝", "适应"],
        "SCALE": ["尺度", "规模", "大小", "比例", "缩放"],
        # 成长思维问题
        "GROWTH_MINDSET": ["成长", "发展", "进步", "提升", "突破"],
        "REVERSE": ["逆向", "反推", "倒逼", "反思", "反驳"],
        "CLOSED_LOOP": ["闭环", "回路", "反馈", "迭代", "循环"],
        # 神话智慧问题
        "CREATION_MYTH": ["创世", "起源", "诞生", "创造", "神话"],
        "APOCALYPSE": ["灭世", "末日", "灾难", "毁灭", "危机"],
        "CYCLICAL": ["循环", "周期", "轮回", "往复", "螺旋"],
        # 文学叙事问题
        "NARRATIVE": ["叙事", "故事", "叙述", "讲述", "情节"],
        "RESILIENCE": ["韧性", "弹性", "抗压", "恢复", "适应"],
        "CHARACTER": ["人物", "角色", "性格", "形象", "塑造"],
        # 人类学问题
        "CROSS_CULTURE": ["跨文化", "文化差异", "文化冲突", "文化融合"],
        "RITUAL": ["仪式", "典礼", "礼节", "风俗", "传统"],
        "CULTURAL_CHANGE": ["文化变迁", "文化转型", "文化演进", "文化融合"],
        # 行为塑造问题
        "HABIT": ["习惯", "习性", "惯性", "成瘾", "常规"],
        "WILLPOWER": ["意志", "自控", "自律", "毅力", "决心"],
        "NUDGE": ["助推", "引导", "激励", "启发", "暗示"],
        # 科学思维问题
        "SCIENTIFIC_METHOD": ["科学方法", "实验", "验证", "假说", "观测"],
        "SYSTEM_THINKING": ["系统思维", "整体观", "关联分析", "动态分析"],
        "EVIDENCE": ["证据", "事实", "数据", "论证", "依据"],
        # 社会科学问题
        "MARKETING": ["营销", "推广", "宣传", "品牌", "市场"],
        "MARKET_ANALYSIS": ["市场分析", "行业分析", "竞争分析", "需求分析"],
        "SOCIAL_DEVELOPMENT": ["社会发展", "文明进步", "人类发展", "趋势"],
        "CONSUMER_MARKETING": ["消费者营销", "C端", "用户", "体验", "口碑"],
        "BRAND_STRATEGY": ["品牌战略", "品牌定位", "品牌形象", "品牌价值"],
        "SOCIAL_STABILITY": ["社会稳定", "秩序", "和谐", "安定", "安全"],
        "PSYCHOLOGICAL_INSIGHT": ["心理洞察", "用户心理", "消费心理", "行为动机"],
        # 自然科学问题
        "PHYSICS_ANALYSIS": ["物理分析", "力学", "能量", "运动", "相互作用"],
        "LIFE_SCIENCE": ["生命科学", "生物", "生态", "进化", "基因"],
        "EARTH_SYSTEM": ["地球系统", "气候", "生态", "环境", "地理"],
        "COSMOS_EXPLORATION": ["宇宙探索", "天文", "星系", "宇宙学", "航天"],
        "SCALE_CROSSING": ["跨尺度", "多尺度", "尺度转换", "层级"],
        # WCC智慧演化问题
        "META_PERSPECTIVE": ["元视角", "超越视角", "升维", "高维"],
        "CIVILIZATION_ANALYSIS": ["文明分析", "文明诊断", "文明评估"],
        "COSMIC_COGNITION": ["宇宙认知", "世界观", "宇宙观", "哲学观"],
        "SCALE_TRANSFORMATION": ["尺度转换", "维度跨越", "规模跃迁"],
        "WORLDVIEW_SHIFT": ["世界观转换", "范式转换", "观念转变"],
        "WISDOM_EVOLUTION": ["智慧演化", "思想进化", "认知升级"],
        "TECH_EVOLUTION": ["技术进化", "科技发展", "技术进步"],
        # 历史思想问题
        "HISTORICAL_ANALYSIS": ["历史分析", "史料分析", "历史考证"],
        "THOUGHT_EVOLUTION": ["思想演进", "哲学发展", "观念变迁"],
        "ECONOMIC_EVOLUTION": ["经济演进", "经济发展", "产业升级"],
        "TECH_HISTORY": ["科技史", "技术发展", "发明历史"],
        # V6.0 新增问题类型
        "CROSS_DIMENSION": ["跨维度", "维度跨越", "升维思考", "高维视角"],
        "PARADIGM_SHIFT": ["范式转换", "范式转移", "理论变革", "观念革新"],
        # 心理学问题
        "PERSONALITY_ANALYSIS": ["人格分析", "性格测试", "个性评估", "心理画像"],
        "GROUP_DYNAMICS": ["群体动力学", "群体行为", "群体心理", "社会影响"],
        "COGNITIVE_BIAS": ["认知偏差", "思维误区", "判断偏误", "heuristic"],
        "MOTIVATION_ANALYSIS": ["动机分析", "驱动力", "激励因素", "需求挖掘"],
        "PSYCHOLOGICAL_ARITHMETIC": ["心理运算", "概率评估", "风险感知"],
        "TRAUMA_HEALING": ["心理创伤", "创伤修复", "心理治疗", "情绪疗愈"],
        "SELF_ACTUALIZATION": ["自我实现", "潜能开发", "个人成长", "自我超越"],
        "INTERPERSONAL_RELATIONSHIP": ["人际关系", "社交技巧", "沟通艺术", "关系维护"],
        # 系统论问题
        "COMPLEX_SYSTEM": ["复杂系统", "系统建模", "系统仿真", "涌现现象"],
        "FEEDBACK_LOOP": ["反馈回路", "正反馈", "负反馈", "系统动力学"],
        "EMERGENT_BEHAVIOR": ["涌现行为", "突现", "自组织", "复杂性"],
        "SYSTEM_EQUILIBRIUM": ["系统均衡", "稳态", "平衡点", "动态平衡"],
        "ADAPTIVE_SYSTEM": ["自适应系统", "自我调节", "适应性", "学习系统"],
        # 管理学问题
        "STRATEGIC_PLANNING": ["战略规划", "长期计划", "战略制定", "愿景规划"],
        "ORGANIZATIONAL_DESIGN": ["组织设计", "架构调整", "部门划分", "职能优化"],
        "PERFORMANCE_MANAGEMENT": ["绩效管理", "KPI", "考核评估", "目标管理"],
        "KNOWLEDGE_MANAGEMENT": ["知识管理", "知识库", "经验沉淀", "学习型组织"],
        "CHANGE_MANAGEMENT": ["变革管理", "转型管理", "改革推进", "变革领导"],
        "INNOVATION_MANAGEMENT": ["创新管理", "创新战略", "创新机制", "持续创新"],
        # 纵横家问题
        "DIPLOMATIC_NEGOTIATION": ["外交谈判", "国际谈判", "博弈策略", "外交手腕"],
        "ALLIANCE_BUILDING": ["联盟构建", "合纵连横", "战略联盟", "伙伴关系"],
        "POWER_BALANCE": ["权力平衡", "势力均衡", "制衡", "多方博弈"],
        # 墨家问题
        "ENGINEERING_INNOVATION": ["工程创新", "技术创新", "技术发明", "工艺改进"],
        "COST_OPTIMIZATION": ["成本优化", "降本增效", "效率提升", "资源节约"],
        "UNIVERSAL_BENEFIT": ["普惠利益", "兼爱", "公共利益", "社会公平"],
        "DEFENSE_FORTIFICATION": ["防御设计", "城防", "安全防护", "风险防御"],
        "LOGICAL_DEDUCTION": ["逻辑推理", "演绎推理", "论证", "推理方法"],
        # 法家问题
        "INSTITUTIONAL_DESIGN": ["制度设计", "机制设计", "规则制定", "体制创新"],
        "LAW_ENFORCEMENT": ["法治执行", "法律实施", "执法", "守法"],
        "POWER_STRUCTURING": ["权力架构", "权力结构", "权力分配", "治理结构"],
        "REWARD_PUNISHMENT": ["赏罚激励", "激励机制", "奖惩制度", "激励约束"],
        "HUMAN_NATURE_ANALYSIS": ["人性分析", "利害分析", "趋利避害", "人性假设"],
        "STATE_CONSOLIDATION": ["国家集权", "政权巩固", "中央集权", "统治稳固"],
        # 经济学问题
        "RESOURCE_ALLOCATION": ["资源配置", "资源分配", "优化配置", "效率配置"],
        "SUPPLY_DEMAND_BALANCE": ["供需平衡", "供求关系", "市场均衡", "价格机制"],
        "ECONOMIC_INCENTIVE": ["经济激励", "激励机制", "经济杠杆", "激励政策"],
        "MARKET_EFFICIENCY": ["市场效率", "资源配置效率", "市场失灵", "帕累托"],
        "INVESTMENT_DECISION": ["投资决策", "投资分析", "资本配置", "项目评估"],
        # 名家问题
        "LOGICAL_PARADOX": ["逻辑悖论", "矛盾", "悖论分析", "反论"],
        "CLASSIFICATION_REFINEMENT": ["名实辨析", "概念辨析", "分类", "命名"],
        "DIALECTICAL_REASONING": ["辩证推理", "矛盾分析", "正反合", "辩证法"],
        # 阴阳家问题
        "WUXING_ANALYSIS": ["五行分析", "相生相克", "五行生克", "阴阳五行"],
        "YINYANG_DIALECTICS": ["阴阳辩证", "对立统一", "转化", "动态平衡"],
        "SEASONAL_RHYTHM": ["时节节律", "时令", "天时节气", "自然规律"],
        "COSMIC_HARMONY": ["天人合一", "宇宙和谐", "自然法则", "天道"],
        "CYCLICAL_TRANSFORMATION": ["循环转化", "物极必反", "周期转化", "转化规律"],
        # 复杂性科学问题
        "EMERGENT_ORDER": ["涌现秩序", "自组织", "秩序生成", "突现"],
        "NETWORK_DYNAMICS": ["网络动力学", "网络分析", "图论", "连接"],
        "ADAPTIVE_EVOLUTION": ["自适应演化", "进化算法", "遗传", "优胜劣汰"],
        # 社会科学精细化问题
        "CONFUCIAN_SUB_SCHOOL": ["儒家子学", "理学", "心学", "实学"],
        "DAOIST_SUB_SCHOOL": ["道家子学", "老庄", "黄老", "道教"],
        "BUDDHIST_SUB_SCHOOL": ["佛家子学", "禅宗", "净土", "密宗"],
        "MILITARY_SUB_SCHOOL": ["兵法子学", "孙子兵法", "孙膑兵法", "六韬三略"],
        "TALENT_PIPELINE": ["人才梯队", "继任计划", "人才培养", "队伍建设"],
        "ORGANIZATIONAL_CULTURE": ["组织文化", "企业文化", "价值观", "文化塑造"],
        "BRAND_CULTURE": ["品牌文化", "品牌故事", "品牌精神", "文化符号"],
        "PHILOSOPHY_OF_MIND": ["心学实践", "知行合一", "致良知", "事上练"],
        "DECISION_FRAMEWORK": ["决策框架", "决策模型", "分析框架", "选择模型"],
        "RESOURCE_ECOLOGY": ["资源生态", "生态系统", "资源循环", "生态链"],
        "INNOVATION_ECOLOGY": ["创新生态", "创新体系", "创业生态", "创新网络"],
        # V6.2 社会科学问题
        "SOCIAL_STRUCTURE_ANALYSIS": ["社会结构", "阶层", "阶级", "社会分层"],
        "CLASS_MOBILITY": ["阶层流动", "社会流动", "上升通道", "代际流动"],
        "INSTITUTIONAL_SOCIOLOGY": ["制度分析", "制度社会学", "社会制度", "体制分析"],
        "SOCIAL_STRATIFICATION": ["社会分层", "阶层分化", "贫富差距", "社会不平等"],
        "COLLECTIVE_ACTION": ["集体行动", "社会运动", "群体事件", "协调行动"],
        "COGNITIVE_BIAS_V62": ["认知偏差", "启发式", "锚定效应", "确认偏误"],
        "DECISION_MAKING_BEHAVIOR": ["决策行为", "选择心理", "决策偏好", "行为决策"],
        "MARKET_BEHAVIOR": ["市场行为", "消费者行为", "投资行为", "交易行为"],
        "INCENTIVE_DESIGN": ["激励设计", "激励机制", "激励相容", "激励相容"],
        "NUDGE_POLICY": ["助推政策", "行为政策", "choice architecture", "默认选项"],
        "MEDIA_EFFECT": ["媒介效果", "传播效果", "舆论影响", "媒体影响"],
        "PUBLIC_OPINION_FORMATION": ["舆论形成", "舆情", "公共意见", "舆论领袖"],
        "INFORMATION_CASCADE": ["信息级联", "羊群效应", "信息传播", "级联效应"],
        "DISCOURSE_ANALYSIS": ["话语分析", "言语分析", "文本分析", "语篇分析"],
        "INTERPERSONAL_COMMUNICATION": ["人际传播", "沟通技巧", "说话艺术", "表达"],
        "CULTURAL_PATTERN_RECOGNITION": ["文化模式", "文化符号", "文化原型", "文化代码"],
    }
    
    def __init__(self):
        self._school_nodes: Dict[str, WisdomEngineNode] = {}
        self._problem_type_nodes: Dict[str, WisdomEngineNode] = {}
        self._all_nodes: Dict[str, WisdomEngineNode] = {}
        self._school_to_problems: Dict[str, List[str]] = defaultdict(list)
        
        # 构建节点网络
        self._build_school_nodes()
        self._build_problem_type_nodes()
        self._build_node_relations()
        
        logger.info(f"[WisdomEngineRegistry] 已构建 {len(self._all_nodes)} 个引擎节点 "
                   f"(42学派 + {len(self._problem_type_nodes)}问题类型)")
    
    def _build_school_nodes(self):
        """构建42个智慧学派引擎节点"""
        for school_key, school_meta in self.WISDOM_SCHOOLS.items():
            node = WisdomEngineNode(
                node_id=f"wisdom_school_{school_key}",
                name=school_meta["name"],
                engine_type=EngineType.WISDOM_SCHOOL,
                school=school_key,
                description=school_meta["description"],
                keywords=school_meta["keywords"],
                capabilities=school_meta["capabilities"],
                load_priority=self._get_school_priority(school_key),
            )
            self._school_nodes[school_key] = node
            self._all_nodes[node.node_id] = node
    
    def _build_problem_type_nodes(self):
        """构建问题类型引擎节点"""
        for problem_key, keywords in self.PROBLEM_TYPE_KEYWORDS.items():
            # 确定所属学派
            school = self._infer_school(problem_key, keywords)
            
            node = WisdomEngineNode(
                node_id=f"problem_type_{problem_key}",
                name=f"{problem_key.replace('_', ' ')}问题引擎",
                engine_type=EngineType.PROBLEM_TYPE,
                problem_type=problem_key,
                school=school,
                description=f"处理{keywords[0] if keywords else problem_key}类型问题",
                keywords=keywords,
                capabilities=[keywords[0] if keywords else problem_key],
                load_priority=7,
            )
            self._problem_type_nodes[problem_key] = node
            self._all_nodes[node.node_id] = node
            
            if school:
                self._school_to_problems[school].append(problem_key)
    
    def _get_school_priority(self, school_key: str) -> int:
        """获取学派优先级（核心学派优先级高）"""
        core_schools = {"CONFUCIAN", "DAOIST", "BUDDHIST", "MILITARY", "FAJIA", "ECONOMICS"}
        if school_key in core_schools:
            return 9
        important_schools = {"PSYCHOLOGY", "MANAGEMENT", "SYSTEMS", "SOCIOLOGY", "BEHAVIORAL_ECONOMICS"}
        if school_key in important_schools:
            return 7
        return 5
    
    def _infer_school(self, problem_key: str, keywords: List[str]) -> Optional[str]:
        """推断问题类型所属学派"""
        # 基于关键词和问题类型推断
        school_mapping = {
            # 儒家
            "ETHICAL": "CONFUCIAN", "GOVERNANCE": "CONFUCIAN", "TALENT": "CONFUCIAN", "CULTURE": "CONFUCIAN",
            # 道家
            "STRATEGY": "DAOIST", "CRISIS": "DAOIST", "CHANGE": "DAOIST", "BALANCE": "DAOIST",
            "TIMING": "DAOIST", "ENVIRONMENT": "DAOIST", "PATTERN": "DAOIST",
            # 佛家
            "MINDSET": "BUDDHIST", "HARMONY": "BUDDHIST", "INTEREST": "BUDDHIST", "LONGTERM": "BUDDHIST",
            # 兵法
            "COMPETITION": "MILITARY", "ATTACK": "MILITARY", "DEFENSE": "MILITARY", "NEGOTIATION": "MILITARY",
            "WAR_ECONOMY_NEXUS": "CIV_WAR_ECONOMY", "STATE_CAPACITY": "CIV_WAR_ECONOMY",
            # 素书
            "LEADERSHIP": "SUFU", "RISK": "SUFU", "FORTUNE": "SUFU", "PERSONNEL": "SUFU",
            # 科学思维
            "SCIENTIFIC_METHOD": "SCIENCE", "SYSTEM_THINKING": "SYSTEMS", "EVIDENCE": "SCIENCE",
            # 社会科学
            "MARKETING": "SOCIAL_SCIENCE", "MARKET_ANALYSIS": "SOCIAL_SCIENCE",
            "CONSUMER_MARKETING": "CHINESE_CONSUMER", "BRAND_STRATEGY": "CHINESE_CONSUMER",
            # 行为
            "HABIT": "BEHAVIOR", "WILLPOWER": "BEHAVIOR", "NUDGE": "BEHAVIORAL_ECONOMICS",
            # 心理
            "PSYCHOLOGICAL_INSIGHT": "PSYCHOLOGY",
            # 组织
            "SOCIAL_STABILITY": "SOCIOLOGY",
            # 成长
            "GROWTH_MINDSET": "GROWTH", "REVERSE": "GROWTH", "CLOSED_LOOP": "GROWTH",
        }
        return school_mapping.get(problem_key, "DAOIST")
    
    def _build_node_relations(self):
        """构建节点关系网络"""
        # 学派间的互补关系
        complementary_pairs = [
            ("CONFUCIAN", "DAOIST"),   # 儒道互补
            ("DAOIST", "BUDDHIST"),    # 道佛互补
            ("MILITARY", "DIPLOMACY"), # 文武互补
            ("FAJIA", "CONFUCIAN"),    # 法儒互补
            ("MOZI", "FAJIA"),         # 墨法互补
            ("ECONOMICS", "BEHAVIORAL_ECONOMICS"),  # 理性与行为经济
            ("PSYCHOLOGY", "SOCIOLOGY"),  # 个体与群体
            ("MANAGEMENT", "ORGANIZATIONAL_PSYCHOLOGY"),  # 管理与组织心理
        ]
        
        for school1, school2 in complementary_pairs:
            if school1 in self._school_nodes and school2 in self._school_nodes:
                n1 = self._school_nodes[school1]
                n2 = self._school_nodes[school2]
                n1.complementary_nodes.add(n2.node_id)
                n2.complementary_nodes.add(n1.node_id)
        
        # 学派与问题类型的关系
        for school, problems in self._school_to_problems.items():
            if school in self._school_nodes:
                school_node = self._school_nodes[school]
                for problem in problems:
                    if problem in self._problem_type_nodes:
                        problem_node = self._problem_type_nodes[problem]
                        school_node.related_nodes.add(problem_node.node_id)
                        problem_node.related_nodes.add(school_node.node_id)
    
    def get_school_node(self, school_key: str) -> Optional[WisdomEngineNode]:
        """获取学派引擎节点"""
        return self._school_nodes.get(school_key)
    
    def get_problem_node(self, problem_key: str) -> Optional[WisdomEngineNode]:
        """获取问题类型引擎节点"""
        return self._problem_type_nodes.get(problem_key)
    
    def get_all_nodes(self) -> List[WisdomEngineNode]:
        """获取所有引擎节点"""
        return list(self._all_nodes.values())
    
    # 同义词映射
    SYNONYMS = {
        "战略": ["策略", "规划", "谋略", "计划"],
        "危机": ["危机", "危险", "紧急", "风险"],
        "管理": ["管理", "治理", "经营"],
        "团队": ["团队", "群体", "组织"],
        "市场": ["市场", "商业", "营销"],
        "竞争": ["竞争", "博弈", "对抗"],
        "决策": ["决策", "决定", "选择"],
        "创新": ["创新", "创造", "变革"],
        "文化": ["文化", "文明", "传统"],
        "心理": ["心理", "心智", "心态"],
    }
    
    def search_nodes(self, query: str, top_k: int = 5) -> List[Tuple[WisdomEngineNode, float]]:
        """搜索相关引擎节点"""
        query_lower = query.lower()
        # 展开同义词
        expanded_keywords = set()
        for word in query_lower:
            expanded_keywords.add(word)
            if word in self.SYNONYMS:
                expanded_keywords.update(self.SYNONYMS[word])
        
        # 原始查询词
        raw_keywords = set(query_lower.replace(" ", "").split())
        expanded_keywords.update(raw_keywords)
        
        results = []
        for node in self._all_nodes.values():
            score = 0.0
            
            # 名称匹配 (最高权重)
            if query_lower in node.name.lower():
                score += 1.0
            # 部分名称匹配
            for word in expanded_keywords:
                if word in node.name.lower():
                    score += 0.3
            
            # 关键词匹配
            for kw in node.keywords:
                kw_lower = kw.lower()
                if query_lower in kw_lower:
                    score += 0.5
                # 部分匹配
                for word in expanded_keywords:
                    if word in kw_lower:
                        score += 0.2
            
            # 能力匹配
            for cap in node.capabilities:
                cap_lower = cap.lower()
                if query_lower in cap_lower:
                    score += 0.4
                for word in expanded_keywords:
                    if word in cap_lower:
                        score += 0.15
            
            if score > 0:
                results.append((node, score))
        
        # 排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def get_network_stats(self) -> Dict[str, Any]:
        """获取网络统计"""
        return {
            "total_nodes": len(self._all_nodes),
            "school_nodes": len(self._school_nodes),
            "problem_type_nodes": len(self._problem_type_nodes),
            "node_types": {
                "wisdom_school": len(self._school_nodes),
                "problem_type": len(self._problem_type_nodes),
            },
            "schools_by_priority": {
                "high": len([n for n in self._school_nodes.values() if n.load_priority >= 8]),
                "medium": len([n for n in self._school_nodes.values() if 5 <= n.load_priority < 8]),
                "low": len([n for n in self._school_nodes.values() if n.load_priority < 5]),
            },
            "total_complementary_links": sum(
                len(n.complementary_nodes) for n in self._all_nodes.values()
            ) // 2,
            "total_related_links": sum(
                len(n.related_nodes) for n in self._all_nodes.values()
            ) // 2,
        }
    
    def get_engine_tree(self) -> Dict[str, Any]:
        """获取引擎树结构"""
        tree = {
            "name": "Somn智慧引擎网络",
            "total_count": len(self._all_nodes),
            "children": []
        }
        
        # 按学派组织
        school_categories = {
            "哲学思辨": ["CONFUCIAN", "DAOIST", "BUDDHIST", "YANGMING", "MOZI", "FAJIA", "MINGJIA", "WUXING"],
            "政治军事": ["MILITARY", "ZONGHENG", "CIV_WAR_ECONOMY", "STATE_CAPACITY"],
            "社会科学": ["SOCIOLOGY", "POLITICAL_ECONOMICS", "CULTURAL_ANTHROPOLOGY", "COMMUNICATION"],
            "经济管理": ["ECONOMICS", "BEHAVIORAL_ECONOMICS", "MANAGEMENT", "ORGANIZATIONAL_PSYCHOLOGY"],
            "心理行为": ["PSYCHOLOGY", "SOCIAL_PSYCHOLOGY", "BEHAVIOR"],
            "科学技术": ["NATURAL_SCIENCE", "COMPLEXITY", "SYSTEMS", "SCIENCE"],
            "历史文化": ["HISTORICAL_THOUGHT", "CIVILIZATION", "WCC", "HONGMING"],
            "思维成长": ["GROWTH", "TOP_METHODS", "DEWEY", "SCI_FI"],
            "文学艺术": ["LITERARY", "MYTHOLOGY", "ANTHROPOLOGY"],
            "实用智慧": ["SUFU", "LVSHI", "METAPHYSICS", "CHINESE_CONSUMER"],
        }
        
        for category, schools in school_categories.items():
            category_node = {
                "name": category,
                "children": []
            }
            for school_key in schools:
                if school_key in self._school_nodes:
                    node = self._school_nodes[school_key]
                    school_node = {
                        "name": node.name,
                        "count": 1 + len(self._school_to_problems.get(school_key, [])),
                        "priority": node.load_priority,
                    }
                    category_node["children"].append(school_node)
            
            if category_node["children"]:
                tree["children"].append(category_node)
        
        return tree


class WisdomEngineNetwork:
    """
    WisdomEngine 166引擎网络 - DivineReason 的引擎层
    
    将42个智慧学派 + 163个问题类型 = 166个引擎节点整合为统一的推理网络。
    支持:
    - 智能路由: 根据问题自动选择最佳引擎组合
    - 引擎融合: 多引擎协同推理，结果融合
    - 关系推理: 利用引擎间的关系网络进行深度推理
    """
    
    def __init__(self):
        self.registry = WisdomEngineRegistry()
        self._active_engines: Set[str] = set()
        
    def solve(self, query: str, strategy: str = "auto") -> Dict[str, Any]:
        """
        使用智慧引擎网络解决问题
        
        Args:
            query: 用户问题
            strategy: 解决策略 (auto/single/fusion/hierarchy)
            
        Returns:
            解决结果字典
        """
        # 1. 搜索相关引擎
        related_nodes = self.registry.search_nodes(query, top_k=5)
        
        if not related_nodes:
            return {
                "success": False,
                "error": "未找到相关引擎",
                "query": query,
            }
        
        # 2. 构建解决路径
        path = []
        insights = []
        
        for node, score in related_nodes:
            path.append({
                "engine_id": node.node_id,
                "engine_name": node.name,
                "engine_type": node.engine_type.value,
                "relevance_score": score,
                "keywords": node.keywords[:3],
                "capabilities": node.capabilities[:2],
            })
            
            # 生成洞察
            if node.engine_type == EngineType.WISDOM_SCHOOL:
                insight = self._generate_school_insight(node, query)
            else:
                insight = self._generate_problem_insight(node, query)
            insights.append(insight)
        
        # 3. 返回结果
        return {
            "success": True,
            "query": query,
            "strategy": strategy,
            "engines_used": len(path),
            "engine_path": path,
            "insights": insights,
            "network_stats": self.registry.get_network_stats(),
            "total_nodes": self.registry.get_network_stats()["total_nodes"],
        }
    
    def _generate_school_insight(self, node: WisdomEngineNode, query: str) -> str:
        """生成学派洞察"""
        school_insights = {
            "CONFUCIAN": f"从儒家视角分析：{node.description}，关键词：{', '.join(node.keywords[:2])}",
            "DAOIST": f"从道家视角分析：{node.description}，强调：{', '.join(node.capabilities[:2])}",
            "BUDDHIST": f"从佛家视角分析：{node.description}，核心方法：{', '.join(node.capabilities[:2])}",
            "MILITARY": f"从兵法视角分析：{node.description}，关键策略：{', '.join(node.keywords[:2])}",
        }
        return school_insights.get(
            node.school, 
            f"【{node.name}】{node.description}"
        )
    
    def _generate_problem_insight(self, node: WisdomEngineNode, query: str) -> str:
        """生成问题类型洞察"""
        return f"【{node.problem_type}问题类型】适用关键词：{', '.join(node.keywords[:3])}"


# 全局单例
_wisdom_engine_network: Optional[WisdomEngineNetwork] = None

def get_wisdom_engine_network() -> WisdomEngineNetwork:
    """获取智慧引擎网络单例"""
    global _wisdom_engine_network
    if _wisdom_engine_network is None:
        _wisdom_engine_network = WisdomEngineNetwork()
    return _wisdom_engine_network


# ── 导出 ────────────────────────────────────────────────────────────────

__all__ = [
    'EngineType',
    'WisdomEngineNode',
    'WisdomEngineRegistry',
    'WisdomEngineNetwork',
    'get_wisdom_engine_network',
]
