"""
Pan-Wisdom Tree 懒加载模块 V2.0.0
万法智慧树 - 预加载+懒加载快速模式

三层加载架构：
- L1: 预加载正则模式 (<1ms)
- L2: LRU缓存学派/问题类型 (<5ms)
- L3: 按需加载完整数据 (首次访问)

使用方式:
    from knowledge_cells.pan_wisdom_lazy_loader import (
        PanWisdomPreloader,
        PanWisdomLRUCache,
        PanWisdomOnDemandLoader,
        preload_pan_wisdom,
        is_pan_wisdom_ready,
    )
"""

import re
import time
import threading
from typing import Dict, List, Optional, Set, Any, Tuple
from functools import lru_cache
from collections import OrderedDict
import os

# 版本信息
VERSION = "2.0.0"

# 预加载状态
_PRELOADED: bool = False
_PRELOAD_TIME: float = 0.0
_lock = threading.Lock()


class PanWisdomPreloader:
    """
    Pan-Wisdom预加载器 - L1层 (<1ms)

    类级别属性（与 pan_wisdom_core.py 兼容）：
    - KEYWORD_SET_INDEX: 问题类型名称 -> 关键词集合
    - KEYWORD_TO_PROBLEM: 关键词 -> 问题类型名称
    - COMPILED_PATTERNS: 关键词 -> 编译的正则表达式
    """

    VERSION = "2.0.0"
    _initialized: bool = False

    # 类级别属性（与 pan_wisdom_core.py 兼容）
    KEYWORD_SET_INDEX: Dict[str, Set[str]] = {}
    KEYWORD_TO_PROBLEM: Dict[str, str] = {}
    COMPILED_PATTERNS: Dict[str, re.Pattern] = {}

    @classmethod
    def is_preloaded(cls) -> bool:
        """检查是否已预加载"""
        return cls._initialized and _PRELOADED

    @classmethod
    def preload(cls) -> None:
        """预加载所有模式和数据"""
        global _PRELOADED, _PRELOAD_TIME

        if cls._initialized:
            return

        start_time = time.perf_counter()

        with _lock:
            if cls._initialized:
                return

            # 初始化编译模式
            cls._init_compiled_patterns()

            # 初始化关键词索引
            cls._init_keyword_index()

            _PRELOADED = True
            cls._initialized = True
            _PRELOAD_TIME = time.perf_counter() - start_time

    @classmethod
    def _init_compiled_patterns(cls) -> None:
        """初始化编译的正则表达式模式"""
        # 中文关键词模式
        patterns = [
            "增长", "运营", "策略", "分析", "优化", "创新", "设计", "规划",
            "营销", "用户", "产品", "市场", "竞争", "数据", "品牌", "流量",
            "转化", "留存", "复购", "gmv", "收入", "成本", "利润", "投资",
            "融资", "团队", "管理", "组织", "文化", "战略", "商业", "模式",
            "盈利", "私域", "公域", "社群", "直播", "短视频", "内容", "电商",
            "供应链", "库存", "物流", "定价", "推广", "获客", "裂变", "会员",
            "积分", "活动", "节日", "大促", "爆款", "种草", "拔草", "评测",
            "攻略", "教程", "干货", "分享", "ugc", "pgc", "kol", "koc",
            "转化率", "点击率", "曝光量", "互动率", "完播率", "跳出率", "复购率",
            "流失率", "道德", "治理", "人才", "选用", "传承", "转型", "危机",
            "变革", "平衡", "阴阳", "时机", "布局", "格局", "结构", "心态",
            "和谐", "协调", "长期", "领导", "决策", "风险", "福祸", "识别",
            "竞争", "攻击", "防御", "谈判", "博弈", "战争", "国家", "制度",
            "反省", "思维", "阳明", "心学", "科学", "自然", "心理", "系统",
            "纵横", "墨家", "法家", "经济", "复杂", "社会学", "行为", "传播",
            "人类", "政治", "组织", "社会",
        ]

        for pattern in patterns:
            try:
                cls.COMPILED_PATTERNS[pattern] = re.compile(pattern, re.IGNORECASE)
            except re.error:
                pass

    @classmethod
    def _init_keyword_index(cls) -> None:
        """初始化关键词索引（问题类型名称 -> 关键词集合）"""
        # 问题类型名称到关键词集合的映射
        # key 必须与 ProblemType 枚举的名称完全匹配（共165个）
        cls.KEYWORD_SET_INDEX = {
            # ===== 儒家 (5) =====
            "ETHICAL": {"道德", "伦理", "诚信", "品德", "品行"},
            "GOVERNANCE": {"治理", "管理", "制度", "规范", "组织"},
            "TALENT": {"人才", "选用", "识人", "知人", "善任"},
            "CULTURE": {"文化", "传承", "精神", "价值", "育人"},
            "CONFUCIAN_SUB_SCHOOL": {"儒家", "孔孟", "仁义", "中庸", "修身"},
            # ===== 道家 (8) =====
            "STRATEGY": {"战略", "策略", "规划", "长远", "全局"},
            "CRISIS": {"危机", "风险", "紧急", "突发", "险境"},
            "CHANGE": {"变革", "变化", "转型", "改革", "革新"},
            "BALANCE": {"平衡", "阴阳", "调和", "均衡", "适度"},
            "TIMING": {"时机", "节点", "窗口", "火候", "节奏"},
            "ENVIRONMENT": {"环境", "形势", "态势", "布局", "顺势"},
            "PATTERN": {"格局", "结构", "模式", "态势", "大局"},
            "DAOIST_SUB_SCHOOL": {"道家", "老子", "庄子", "无为", "自然"},
            # ===== 佛家 (4) =====
            "MINDSET": {"心态", "心境", "态度", "心理", "心性"},
            "HARMONY": {"和谐", "协调", "融洽", "和睦", "共处"},
            "INTEREST": {"利益", "协调", "分配", "平衡", "取舍"},
            "LONGTERM": {"长期", "长远", "持久", "持续", "永续"},
            "BUDDHIST_SUB_SCHOOL": {"佛家", "佛教", "禅", "缘起", "放下"},
            # ===== 素书 (4) =====
            "LEADERSHIP": {"领导", "决策", "统帅", "统领", "指引"},
            "RISK": {"风险", "隐患", "危险", "险", "防患"},
            "FORTUNE": {"福祸", "吉凶", "利弊", "得失", "祸福"},
            "PERSONNEL": {"人才", "人事", "人力", "团队", "选用"},
            # ===== 兵法 (8) =====
            "COMPETITION": {"竞争", "博弈", "较量", "对决", "争锋"},
            "ATTACK": {"攻击", "进攻", "出击", "抢占", "侵袭"},
            "DEFENSE": {"防御", "防守", "保守", "固守", "抵御"},
            "NEGOTIATION": {"谈判", "协商", "洽谈", "议价", "交涉"},
            "WAR_ECONOMY_NEXUS": {"战争", "军事", "经济", "经战", "联动"},
            "STATE_CAPACITY": {"国家", "政府", "制度", "能力", "国力"},
            "INSTITUTIONAL_SEDIMENTATION": {"制度", "沉淀", "积累", "演进", "固化"},
            "MILITARY_SUB_SCHOOL": {"兵法", "孙子", "战术", "战", "兵家"},
            # ===== 顶级思维/成长 (10) =====
            "GROWTH_MINDSET": {"增长", "提升", "突破", "成长", "进步", "扩张", "突破", "进化"},
            "REVERSE": {"逆向", "反向", "倒推", "颠覆", "反思"},
            "CLOSED_LOOP": {"闭环", "循环", "迭代", "反馈", "回路"},
            "ADAPTIVE_EVOLUTION": {"适应", "演化", "进化", "迭代", "变革"},
            "INNOVATION_ECOLOGY": {"创新", "生态", "体系", "系统", "机制"},
            "RESILIENCE": {"韧性", "抗逆", "弹性", "恢复", "适应"},
            "PARADIGM_SHIFT": {"范式", "转型", "跃迁", "革命", "颠覆"},
            "META_PERSPECTIVE": {"元", "超越", "升维", "高维", "俯视"},
            "DIMENSION": {"维度", "多维", "跨界", "立体", "多元"},
            "SURVIVAL": {"生存", "存活", "竞争", "淘汰", "进化"},
            # ===== 科学/系统 (5) =====
            "SCIENTIFIC_METHOD": {"科学", "实验", "验证", "假设", "求证"},
            "SYSTEM_THINKING": {"系统", "整体", "要素", "反馈", "结构"},
            "EVIDENCE": {"证据", "数据", "事实", "实证", "依据"},
            "COMPLEX_SYSTEM": {"复杂", "系统", "混沌", "涌现", "非线性"},
            "FEEDBACK_LOOP": {"反馈", "回路", "循环", "迭代", "调节"},
            # ===== 心理学/行为 (12) =====
            "HABIT": {"习惯", "惯性", "养成", "行为", "定式"},
            "WILLPOWER": {"意志", "自控", "自制", "毅力", "坚持"},
            "NUDGE": {"助推", "引导", "轻推", "暗示", "启发"},
            "MOTIVATION_ANALYSIS": {"动机", "激励", "欲望", "驱动力", "诱因"},
            "COGNITIVE_BIAS": {"偏差", "认知", "偏见", "误判", "思维陷阱"},
            "PSYCHOLOGICAL_INSIGHT": {"心理", "洞察", "人心", "需求", "动机"},
            "TRAUMA_HEALING": {"创伤", "修复", "治愈", "心理", "疗愈"},
            "SELF_ACTUALIZATION": {"自我", "实现", "成长", "成就", "价值"},
            "INTERPERSONAL_RELATIONSHIP": {"人际", "关系", "社交", "相处", "联络"},
            "PERSONALITY_ANALYSIS": {"人格", "性格", "个性", "特质", "分析"},
            "GROUP_DYNAMICS": {"群体", "动态", "从众", "影响", "羊群"},
            "DECISION_MAKING_BEHAVIOR": {"决策", "选择", "判断", "抉择", "决定"},
            # ===== 管理/组织 (8) =====
            "STRATEGIC_PLANNING": {"战略", "规划", "计划", "蓝图", "谋划"},
            "ORGANIZATIONAL_DESIGN": {"组织", "架构", "结构", "设计", "体系"},
            "PERFORMANCE_MANAGEMENT": {"绩效", "考核", "评估", "衡量", "管理"},
            "KNOWLEDGE_MANAGEMENT": {"知识", "管理", "沉淀", "积累", "传承"},
            "CHANGE_MANAGEMENT": {"变革", "管理", "推进", "转型", "实施"},
            "INNOVATION_MANAGEMENT": {"创新", "管理", "推动", "激励", "孵化"},
            "LEADERSHIP_STYLE_ANALYSIS": {"领导", "风格", "管理", "带队", "领袖"},
            "ORGANIZATIONAL_CULTURE": {"文化", "组织", "氛围", "价值观", "精神"},
            # ===== 纵横/外交 (3) =====
            "DIPLOMATIC_NEGOTIATION": {"外交", "谈判", "邦交", "国际", "斡旋"},
            "ALLIANCE_BUILDING": {"联盟", "结盟", "合作", "联合", "协同"},
            "POWER_BALANCE": {"权力", "平衡", "博弈", "制衡", "势力"},
            # ===== 墨家/法家 (3) =====
            "ENGINEERING_INNOVATION": {"工程", "技术", "创新", "建造", "实施"},
            "COST_OPTIMIZATION": {"成本", "优化", "效率", "节约", "精简"},
            "UNIVERSAL_BENEFIT": {"普惠", "公利", "天下", "兼爱", "公平"},
            "DEFENSE_FORTIFICATION": {"防御", "筑防", "巩固", "坚守", "工事"},
            "LOGICAL_DEDUCTION": {"逻辑", "推理", "演绎", "论证", "推论"},
            "INSTITUTIONAL_DESIGN": {"制度", "设计", "体系", "机制", "法治"},
            "LAW_ENFORCEMENT": {"执法", "法治", "执行", "司法", "刑罚"},
            "POWER_STRUCTURING": {"权力", "架构", "配置", "分配", "权势"},
            "REWARD_PUNISHMENT": {"赏罚", "激励", "奖惩", "考核", "管控"},
            "HUMAN_NATURE_ANALYSIS": {"人性", "利害", "善恶", "本性", "人心"},
            "STATE_CONSOLIDATION": {"集权", "巩固", "统一", "中央", "政权"},
            # ===== 名家/辩证 (4) =====
            "LOGICAL_PARADOX": {"悖论", "矛盾", "诡辩", "逻辑", "悖"},
            "CLASSIFICATION_REFINEMENT": {"名实", "分类", "辨析", "概念", "名"},
            "DIALECTICAL_REASONING": {"辩证", "矛盾", "对立", "统一", "转化"},
            # ===== 阴阳/五行 (5) =====
            "WUXING_ANALYSIS": {"五行", "生克", "制化", "旺衰", "流转"},
            "YINYANG_DIALECTICS": {"阴阳", "辩证", "对立", "转化", "动态"},
            "YINYANG": {"阴阳", "调和", "平衡", "两面", "互补"},
            "SEASONAL_RHYTHM": {"时节", "季节", "节律", "周期", "四时"},
            "COSMIC_HARMONY": {"天人", "合一", "和谐", "宇宙", "自然"},
            # ===== 文明/历史 (5) =====
            "CIVILIZATION_ANALYSIS": {"文明", "演进", "发展", "历程", "脉络"},
            "HISTORICAL_ANALYSIS": {"历史", "经验", "教训", "传统", "规律"},
            "THOUGHT_EVOLUTION": {"思想", "演进", "变迁", "流派", "脉络"},
            "ECONOMIC_EVOLUTION": {"经济", "演进", "变迁", "发展", "周期"},
            "TECH_HISTORY": {"科技", "历史", "演进", "进步", "技术"},
            # ===== 社会科学 V6.2 (16) =====
            "MARKETING": {"营销", "推广", "宣传", "获客", "推广"},
            "MARKET_ANALYSIS": {"市场", "分析", "调研", "赛道", "行业"},
            "SOCIAL_DEVELOPMENT": {"社会", "发展", "变迁", "趋势", "演进"},
            "MARKET_BEHAVIOR": {"市场", "行为", "消费", "购买", "决策"},
            "MARKET_EFFICIENCY": {"市场", "效率", "配置", "资源", "最优"},
            "MARKET_REGULATION_ANALYSIS": {"市场", "监管", "政策", "法规", "规范"},
            "CONSUMER_MARKETING": {"消费", "营销", "C端", "用户", "购买"},
            "BRAND_STRATEGY": {"品牌", "战略", "定位", "形象", "心智"},
            "BRAND_CULTURE": {"品牌", "文化", "内涵", "故事", "价值"},
            "CROSS_CULTURE": {"跨文化", "国际", "全球", "本土", "文化"},
            "CROSS_CULTURAL_ADAPTATION": {"跨文化", "适应", "融合", "本地化", "国际化"},
            "CULTURAL_CHANGE": {"文化", "变迁", "演变", "趋势", "革新"},
            "RITUAL": {"仪式", "典礼", "规范", "传统", "惯例"},
            "SOCIAL_STRATIFICATION": {"阶层", "分级", "固化", "流动", "平等"},
            "PUBLIC_CHOICE": {"公共", "选择", "集体", "投票", "决策"},
            "SOCIAL_INFLUENCE_MECHANISM": {"影响", "传播", "扩散", "口碑", "效应"},
            # ===== 经济学/资源配置 (6) =====
            "RESOURCE_ALLOCATION": {"资源", "配置", "分配", "优化", "调度"},
            "SUPPLY_DEMAND_BALANCE": {"供需", "平衡", "定价", "市场", "调节"},
            "ECONOMIC_INCENTIVE": {"激励", "经济", "奖励", "动机", "机制"},
            "INVESTMENT_DECISION": {"投资", "决策", "回报", "收益", "风险"},
            "INCENTIVE_DESIGN": {"激励", "设计", "机制", "奖励", "惩罚"},
            "PUBLIC_INTEREST": {"公共", "利益", "公益", "公私", "取舍"},
            # ===== 复杂性/涌现 (5) =====
            "EMERGENT_BEHAVIOR": {"涌现", "突发", "自发", "宏观", "微观"},
            "EMERGENT_ORDER": {"涌现", "秩序", "自发", "生成", "自组织"},
            "ADAPTIVE_SYSTEM": {"自适应", "系统", "调节", "反馈", "响应"},
            "SYSTEM_EQUILIBRIUM": {"均衡", "平衡", "稳态", "系统", "和谐"},
            "SCALE_CROSSING": {"跨尺度", "宏观", "微观", "跨界", "穿透"},
            # ===== 宇宙/系统 (6) =====
            "COSMOS_EXPLORATION": {"宇宙", "探索", "太空", "星辰", "未知"},
            "EARTH_SYSTEM": {"地球", "系统", "生态", "环境", "星球"},
            "LIFE_SCIENCE": {"生命", "科学", "生物", "演化", "生态"},
            "PHYSICS_ANALYSIS": {"物理", "分析", "规律", "力学", "原理"},
            "SCALE_TRANSFORMATION": {"尺度", "转换", "跃迁", "降维", "升维"},
            "WORLDVIEW_SHIFT": {"世界观", "认知", "范式", "转换", "颠覆"},
            # ===== 叙事/神话 (4) =====
            "NARRATIVE": {"叙事", "故事", "讲述", "情节", "剧本"},
            "CREATION_MYTH": {"创世", "神话", "起源", "传说", "开天"},
            "APOCALYPSE": {"灭世", "危机", "末日", "崩塌", "终结"},
            "CYCLICAL": {"循环", "周期", "轮回", "轮回", "反复"},
            # ===== 韧性/复杂 (4) =====
            "RESOURCE_ECOLOGY": {"资源", "生态", "循环", "可持续", "再生"},
            "CYCLICAL_TRANSFORMATION": {"循环", "转化", "变迁", "转型", "演进"},
            "CROSS_DIMENSION": {"跨维", "跨界", "综合", "融合", "多元"},
            "NETWORK_DYNAMICS": {"网络", "动态", "连接", "节点", "传播"},
            # ===== 传播/舆论 (5) =====
            "INFORMATION_CASCADE": {"信息", "传播", "级联", "扩散", "蔓延"},
            "PUBLIC_OPINION_FORMATION": {"舆论", "形成", "发酵", "引导", "民意的形成"},
            "MEDIA_EFFECT": {"媒体", "效果", "影响", "传播", "效应"},
            "DISCOURSE_ANALYSIS": {"话语", "分析", "叙事", "框架", "建构"},
            "SOCIAL_STRUCTURE_ANALYSIS": {"社会", "结构", "分析", "阶层", "网络"},
            # ===== 行为塑造 (4) =====
            "CONFORMITY_BEHAVIOR": {"从众", "随大流", "群体", "压力", "社会"},
            "GROUP_THINK_ANALYSIS": {"群体", "思维", "盲从", "一致", "极化"},
            "COLLECTIVE_ACTION": {"集体", "行动", "协作", "合作", "组织"},
            "CLASS_MOBILITY": {"阶级", "流动", "跃迁", "晋升", "固化"},
            # ===== 政治/制度 (5) =====
            "INSTITUTIONAL_POLITICAL_ANALYSIS": {"制度", "政治", "分析", "权力", "治理"},
            "INSTITUTIONAL_SOCIOLOGY": {"制度", "社会学", "规范", "结构", "组织"},
            "POLICY_GAME_THEORY": {"政策", "博弈", "策略", "互动", "均衡"},
            "AUTHORITY_OBEDIENCE": {"权威", "服从", "追随", "效忠", "等级"},
            "SOCIAL_STABILITY": {"社会稳定", "秩序", "安定", "和谐", "治理"},
            # ===== 哲学/智慧 (5) =====
            "WISDOM_EVOLUTION": {"智慧", "演化", "演进", "迭代", "升级"},
            "TECH_EVOLUTION": {"技术", "进化", "演进", "迭代", "变革"},
            "COSMIC_COGNITION": {"宇宙", "认知", "哲学", "世界观", "存在"},
            "PHILOSOPHY_OF_MIND": {"心灵", "哲学", "意识", "精神", "存在"},
            "CULTURAL_PATTERN_RECOGNITION": {"文化", "模式", "识别", "规律", "范式"},
            # ===== 营销/增长 (4) =====
            "MARKET_EFFICIENCY": {"市场", "效率", "最优", "配置", "资源"},
            "NUDGE_POLICY": {"助推", "政策", "引导", "设计", "行为"},
            "ADAPTIVE_EVOLUTION": {"适应", "演化", "进化", "变革", "迭代"},
            "INTERPERSONAL_COMMUNICATION": {"人际", "沟通", "交流", "表达", "倾听"},
        }

        # 生成反向索引：关键词 -> 问题类型名称
        cls.KEYWORD_TO_PROBLEM = {}
        for problem_type_name, keywords in cls.KEYWORD_SET_INDEX.items():
            for keyword in keywords:
                cls.KEYWORD_TO_PROBLEM[keyword.lower()] = problem_type_name

    @classmethod
    def get_pattern(cls, keyword: str) -> Optional[re.Pattern]:
        """获取编译的正则表达式模式"""
        if not cls._initialized:
            cls.preload()
        return cls.COMPILED_PATTERNS.get(keyword)

    @classmethod
    def get_keyword_to_problem(cls, keyword: str) -> Optional[str]:
        """获取关键词对应的问题类型名称"""
        if not cls._initialized:
            cls.preload()
        return cls.KEYWORD_TO_PROBLEM.get(keyword.lower())

    @classmethod
    def reset(cls) -> None:
        """重置预加载状态"""
        global _PRELOADED, _PRELOAD_TIME
        with _lock:
            _PRELOADED = False
            _PRELOAD_TIME = 0.0
            cls.KEYWORD_SET_INDEX = {}
            cls.KEYWORD_TO_PROBLEM = {}
            cls.COMPILED_PATTERNS = {}
            cls._initialized = False


# ============================================================
# L2: LRU缓存 (<5ms)
# ============================================================

class PanWisdomLRUCache:
    """Pan-Wisdom LRU缓存 - L2层"""

    VERSION = "2.0.0"

    def __init__(self, max_size: int = 128):
        self._cache: OrderedDict = OrderedDict()
        self._max_size = max_size
        self._hits: int = 0
        self._misses: int = 0

    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        if key in self._cache:
            self._hits += 1
            self._cache.move_to_end(key)
            return self._cache[key]
        self._misses += 1
        return None

    def put(self, key: str, value: Any) -> None:
        """设置缓存值"""
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)
            self._cache[key] = value

    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total = self._hits + self._misses
        hit_rate = self._hits / total if total > 0 else 0.0
        return {
            "size": len(self._cache),
            "max_size": self._max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{hit_rate:.2%}",
        }

    # SchoolRecommender 所需的方法
    def get_school_info(self, key: str) -> Optional[Any]:
        """获取学派信息（兼容 SchoolRecommender）"""
        return self.get(key)

    def cache_school_info(self, key: str, info: Any) -> None:
        """缓存学派信息（兼容 SchoolRecommender）"""
        self.put(key, info)

    def get_recommendation(self, key: str) -> Optional[Any]:
        """获取推荐（兼容 SchoolRecommender）"""
        return self.get(key)

    def cache_recommendation(self, key: str, rec: Any) -> None:
        """缓存推荐（兼容 SchoolRecommender）"""
        self.put(key, rec)


# 全局LRU缓存实例
_global_lru_cache = PanWisdomLRUCache()


def get_pan_wisdom_cache() -> PanWisdomLRUCache:
    """获取全局LRU缓存实例"""
    return _global_lru_cache


# ============================================================
# L3: 按需加载 (首次访问)
# ============================================================

class PanWisdomOnDemandLoader:
    """Pan-Wisdom 按需加载器 - L3层"""

    VERSION = "2.0.0"
    _loaded: bool = False
    _load_time: float = 0.0

    @classmethod
    def is_loaded(cls) -> bool:
        """检查是否已加载"""
        return cls._loaded

    @classmethod
    def load(cls) -> None:
        """按需加载完整数据"""
        if cls._loaded:
            return

        start_time = time.perf_counter()

        # 确保L1和L2已加载
        PanWisdomPreloader.preload()

        # L3: 加载完整数据
        cls._load_full_data()

        cls._loaded = True
        cls._load_time = time.perf_counter() - start_time

    @classmethod
    def _load_full_data(cls) -> None:
        """加载完整数据（扩展数据）"""
        # 实际应用中，这里会从文件、数据库或API加载完整数据
        pass

    @classmethod
    def reset(cls) -> None:
        """重置加载状态"""
        cls._loaded = False
        cls._load_time = 0.0


# 全局按需加载器实例
_global_on_demand_loader = PanWisdomOnDemandLoader()


def get_pan_wisdom_on_demand() -> PanWisdomOnDemandLoader:
    """获取全局按需加载器实例"""
    return _global_on_demand_loader


# ============================================================
# 便捷函数
# ============================================================

def preload_pan_wisdom() -> None:
    """预加载Pan-Wisdom Tree（推荐在应用启动时调用一次）"""
    PanWisdomPreloader.preload()


def is_pan_wisdom_ready() -> bool:
    """检查Pan-Wisdom是否就绪"""
    return PanWisdomPreloader.is_preloaded()


def get_pan_wisdom_load_info() -> Dict[str, Any]:
    """获取加载信息"""
    return {
        "preloaded": _PRELOADED,
        "preload_time_ms": f"{_PRELOAD_TIME * 1000:.2f}ms",
        "version": VERSION,
        "patterns_count": len(PanWisdomPreloader.COMPILED_PATTERNS),
        "keywords_count": len(PanWisdomPreloader.KEYWORD_TO_PROBLEM),
        "problem_types_count": len(PanWisdomPreloader.KEYWORD_SET_INDEX),
    }


def clear_pan_wisdom_cache() -> None:
    """清空所有缓存"""
    _global_lru_cache.clear()
    PanWisdomOnDemandLoader.reset()


def benchmark_pan_wisdom_load() -> Dict[str, Any]:
    """基准测试加载性能"""
    PanWisdomPreloader.reset()
    clear_pan_wisdom_cache()

    # 测试L1预加载
    start = time.perf_counter()
    PanWisdomPreloader.preload()
    l1_time = time.perf_counter() - start

    # 测试缓存
    cache = get_pan_wisdom_cache()
    for i in range(100):
        cache.put(f"test_key_{i}", f"test_value_{i}")
    for i in range(100):
        cache.get(f"test_key_{i}")

    return {
        "L1_preload_ms": f"{l1_time * 1000:.2f}ms",
        "cache_stats": cache.stats(),
        "recommendation": "L1 < 1ms OK" if l1_time < 0.001 else f"L1 {l1_time * 1000:.2f}ms",
    }
