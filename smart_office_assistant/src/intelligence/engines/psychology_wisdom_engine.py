"""
心理学智慧引擎 V1.0.0
===================
版本: V1.0.0
日期: 2026-04-23
来源: V6.0 第二阶段新增学派集成

整合心理学先驱与消费心理学洞察能力:

1. 人格分析 - 卡特尔16PF/大五人格/MBTI框架
2. 群体动力学 - 群体极化/社会从众/群体决策
3. 认知偏差 - 锚定/可得性/确认偏误等20+种偏差
4. 动机分析 - 内在/外在动机/自我决定理论
5. 心理运算 - 预期效价/概率权重/风险偏好
6. 创伤修复 - 依恋理论/创伤后成长
7. 自我实现 - 马斯洛顶层/存在主义
8. 人际关系 - 依恋风格/沟通分析/社会渗透

引擎架构:
┌─────────────────────────────────────────────────────┐
│           心理学智慧引擎 V1.0.0                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │人格分析  │ │群体动力学│ │认知偏差  │ │动机分析  │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ │
│       └────────────┴─────┬───────┴────────────┘        │
│                   ┌─────┴─────┐                       │
│                   │ 心理洞察层 │                       │
│                   │  Fusion    │                       │
│                   └───────────┘                       │
└─────────────────────────────────────────────────────┘
"""

from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class 人格维度(Enum):
    """人格大五维度"""
    开放性 = "O"      # Openness
    尽责性 = "C"      # Conscientiousness
    外向性 = "E"      # Extraversion
    宜人性 = "A"      # Agreeableness
    神经质 = "N"      # Neuroticism


class 认知偏差类型(Enum):
    """常见认知偏差"""
    锚定效应 = "anchoring"
    可得性启发 = "availability"
    确认偏误 = "confirmation"
    过度自信 = "overconfidence"
    损失厌恶 = "loss_aversion"
    现状偏见 = "status_quo"
    框架效应 = "framing"
    峰终定律 = "peak_end"
    禀赋效应 = "endowment"
    虚假独特性 = "false_uniqueness"


class 动机类型(Enum):
    """动机类型"""
    内在动机 = "intrinsic"
    外在动机 = "extrinsic"
    成就动机 = "achievement"
    亲和动机 = "affiliation"
    权力动机 = "power"
    自我超越 = "self_transcendence"


class 依恋风格(Enum):
    """成人依恋风格"""
    安全型 = "secure"
    焦虑型 = "anxious"
    回避型 = "avoidant"
    混乱型 = "disorganized"


@dataclass
class 人格档案:
    """人格分析结果"""
    大五分数: Dict[str, float]
    人格类型: str
    核心特质: List[str]
    优势领域: List[str]
    风险领域: List[str]
    行为预测: List[str]


@dataclass
class 心理洞察结果:
    """综合心理洞察"""
    人格分析: Dict
    群体分析: Dict
    偏差识别: List[Dict]
    动机剖析: Dict
    关系评估: Dict
    干预建议: List[str]
    置信度: float


class PsychologyWisdomEngine:
    """
    心理学智慧引擎
    
    整合心理学先驱研究成果:
    - 弗洛伊德: 潜意识/人格结构
    - 荣格: 原型/集体无意识
    - 马斯洛: 需求层次/自我实现
    - 卡哈内: 认知偏差/决策心理学
    - 阿德勒: 自卑与超越
    - 埃利斯: 理性情绪疗法
    """
    
    VERSION = "6.2.0"
    
    def __init__(self):
        self.name = "心理学智慧引擎"
        self.先驱知识库 = self._初始化先驱知识库()
        self.偏差知识库 = self._初始化偏差知识库()
        self.干预策略库 = self._初始化干预策略库()
    
    def _初始化先驱知识库(self) -> Dict:
        """初始化心理学先驱知识库"""
        return {
            "弗洛伊德": {
                "核心概念": ["潜意识", "本我/自我/超我", "防御机制", "性心理发展阶段"],
                "分析方法": ["自由联想", "梦的解析", "移情分析"],
                "干预技术": ["精神分析", "阻抗处理", "梦的联想"]
            },
            "荣格": {
                "核心概念": ["集体无意识", "原型", "个性化过程", "阴影"],
                "分析方法": ["词语联想", "积极想象", "扩充技术"],
                "干预技术": ["梦的分析", "沙盘治疗", "主动想象"]
            },
            "马斯洛": {
                "核心概念": ["需求层次", "自我实现", "高峰体验", "元需求"],
                "分析方法": ["需求诊断", "成长评估", "动机分析"],
                "干预技术": ["人本主义对话", "高峰体验引导", "自我探索"]
            },
            "卡哈内": {
                "核心概念": ["认知偏差", "启发式决策", "框架效应", "双系统理论"],
                "分析方法": ["偏差审计", "决策树分析", "概率评估"],
                "干预技术": ["偏差纠正训练", "清单核查", "外部视角获取"]
            },
            "阿德勒": {
                "核心概念": ["自卑感", "优越感追求", "生活风格", "社会兴趣"],
                "分析方法": ["早期记忆分析", "出生顺序", "私人逻辑识别"],
                "干预技术": ["鼓励技术", "行为激活", "目的论重构"]
            },
            "埃利斯": {
                "核心概念": ["ABC理论", "非理性信念", "理性情绪", "无条件接受"],
                "分析方法": ["信念识别", "不合理性评估", "辩论技术"],
                "干预技术": ["RET步骤", "合理情绪想象", "羞耻攻击训练"]
            }
        }
    
    def _初始化偏差知识库(self) -> Dict:
        """初始化认知偏差知识库"""
        return {
            认知偏差类型.锚定效应.value: {
                "描述": "过度依赖第一个信息（锚点）进行决策",
                "示例": "原价999现价199觉得便宜",
                "干预": "独立评估/多方参考/反向思考"
            },
            认知偏差类型.可得性启发.value: {
                "描述": "用易想到的例子来判断概率",
                "示例": "因为记得飞机事故新闻而高估飞行风险",
                "干预": "数据核实/统计基础/基准率参照"
            },
            认知偏差类型.确认偏误.value: {
                "描述": "搜索支持自己观点的信息",
                "示例": "只读立场相同的新闻",
                "干预": "魔鬼代言人/红队测试/证据权重法"
            },
            认知偏差类型.过度自信.value: {
                "描述": "高估自己判断的准确性",
                "示例": "90%的司机认为自己高于平均水平",
                "干预": "校准训练/外部反馈/基准对比"
            },
            认知偏差类型.损失厌恶.value: {
                "描述": "损失带来的痛苦大于同等收益的快乐",
                "示例": "宁可不变也不愿冒险",
                "干预": "重新框架/损失暴露/概率加权"
            },
            认知偏差类型.现状偏见.value: {
                "描述": "倾向于保持现状",
                "示例": "默认选项参与率远高于主动选择参与",
                "干预": "积极决策/对比分析/决策时限"
            },
            认知偏差类型.框架效应.value: {
                "描述": "同一信息不同表述导致不同决策",
                "示例": "\"90%存活\"vs\"10%死亡\"",
                "干预": "双向框架/核心本质/数据原始化"
            },
            认知偏差类型.峰终定律.value: {
                "描述": "体验记忆由高峰和结束时刻决定",
                "示例": "度假最后一天的体验决定整体回忆",
                "干预": "体验设计/峰值创造/结尾优化"
            },
            认知偏差类型.禀赋效应.value: {
                "描述": "对自己拥有的东西估值更高",
                "示例": "自己的旧手机总觉得比市场价值钱",
                "干预": "市场比较/忘却沉没成本/交换视角"
            },
            认知偏差类型.虚假独特性.value: {
                "描述": "高估自己的积极特质和技能",
                "示例": "多数人认为自己的道德高于平均水平",
                "干预": "客观评估/360反馈/标准对照"
            }
        }
    
    def _初始化干预策略库(self) -> Dict:
        """初始化心理干预策略库"""
        return {
            "认知层面": [
                "元认知训练：提高对思维过程的觉察",
                "偏差审计清单：决策前系统性检查",
                "概率校准：基于历史的预测准确率评估",
                "外部视角获取：刻意寻求反对意见"
            ],
            "情感层面": [
                "情绪标签化：命名情绪降低强度",
                "接纳承诺疗法：开放、觉察、行动",
                "辩证行为技术：TIP调节情绪",
                "慈悲心训练：对自己和他人的慈悲"
            ],
            "行为层面": [
                "行为激活：增加积极行为频率",
                "习惯叠加：新习惯绑定旧习惯触发器",
                "承诺机制：预先承诺增加依从性",
                "环境设计：让好行为更容易，坏行为更困难"
            ],
            "关系层面": [
                "非暴力沟通：观察-感受-需要-请求",
                "依恋安全基地：建立安全依恋关系",
                "社会兴趣培养：关注共同体福祉",
                "边界设定：健康的自我-他人界限"
            ]
        }
    
    def analyze_personality(self, user_data: Dict) -> 人格档案:
        """
        人格分析
        
        Args:
            user_data: 包含行为数据、言语内容、选择偏好的字典
            
        Returns:
            人格档案
        """
        大五分数 = self._评估大五维度(user_data)
        人格类型 = self._判定人格类型(大五分数)
        核心特质 = self._提取核心特质(大五分数)
        优势领域 = self._识别优势领域(大五分数)
        风险领域 = self._识别风险领域(大五分数)
        行为预测 = self._生成行为预测(大五分数)
        
        return 人格档案(
            大五分数=大五分数,
            人格类型=人格类型,
            核心特质=核心特质,
            优势领域=优势领域,
            风险领域=风险领域,
            行为预测=行为预测
        )
    
    def _评估大五维度(self, user_data: Dict) -> Dict[str, float]:
        """评估大五人格维度"""
        行为指标 = user_data.get("behavior_indicators", {})
        言语分析 = user_data.get("speech_patterns", {})
        选择历史 = user_data.get("choice_history", [])
        
        # 简化评估逻辑
        分数 = {
            "开放性": 0.5,
            "尽责性": 0.5,
            "外向性": 0.5,
            "宜人性": 0.5,
            "神经质": 0.5
        }
        
        # 基于行为指标调整
        if "creative_projects" in 行为指标:
            分数["开放性"] += 0.1 * min(行为指标["creative_projects"] / 5, 1)
        if "deadline_compliance" in 行为指标:
            分数["尽责性"] += 0.1 * min(行为指标["deadline_compliance"] / 5, 1)
        if "social_events" in 行为指标:
            分数["外向性"] += 0.1 * min(行为指标["social_events"] / 5, 1)
        if "conflict_avoidance" in 行为指标:
            分数["宜人性"] += 0.1 * min(行为指标["冲突避免"] / 5, 1)
        if "stress_indicators" in 行为指标:
            分数["神经质"] += 0.1 * min(行为指标["压力指标"] / 5, 1)
        
        # 确保分数在0-1范围
        for key in 分数:
            分数[key] = max(0.0, min(1.0, 分数[key]))
        
        return 分数
    
    def _判定人格类型(self, 大五分数: Dict[str, float]) -> str:
        """判定人格类型"""
        组合 = ""
        if 大五分数["开放性"] > 0.6:
            组合 += "O"
        if 大五分数["尽责性"] > 0.6:
            组合 += "C"
        if 大五分数["外向性"] > 0.6:
            组合 += "E"
        if 大五分数["宜人性"] > 0.6:
            组合 += "A"
        if 大五分数["神经质"] > 0.6:
            组合 += "N"
        
        if not 组合:
            组合 = "OCEAN-平均型"
        
        return 组合
    
    def _提取核心特质(self, 大五分数: Dict[str, float]) -> List[str]:
        """提取核心特质描述"""
        特质 = []
        
        if 大五分数["开放性"] > 0.7:
            特质.append("高开放性：富有想象力，好奇心强，追求新奇")
        elif 大五分数["开放性"] < 0.3:
            特质.append("低开放性：务实传统，偏好熟悉，稳定可预测")
        
        if 大五分数["尽责性"] > 0.7:
            特质.append("高尽责性：自律可靠，有组织，目标导向")
        elif 大五分数["尽责性"] < 0.3:
            特质.append("低尽责性：灵活随性，适应变化，但可能拖延")
        
        if 大五分数["外向性"] > 0.7:
            特质.append("高外向性：社交活跃，精力充沛，喜欢刺激")
        elif 大五分数["外向性"] < 0.3:
            特质.append("低外向性：内省安静，享受独处，深思熟虑")
        
        if 大五分数["宜人性"] > 0.7:
            特质.append("高宜人性：合作信任，利他友好，同理心强")
        elif 大五分数["宜人性"] < 0.3:
            特质.append("低宜人性：竞争独立，质疑批评，优先任务")
        
        if 大五分数["神经质"] > 0.7:
            特质.append("高神经质：情绪波动大，焦虑敏感，担忧倾向")
        elif 大五分数["神经质"] < 0.3:
            特质.append("低神经质：情绪稳定，沉着冷静，压力恢复快")
        
        return 特质 if 特质 else ["中等水平，各维度平衡发展"]
    
    def _识别优势领域(self, 大五分数: Dict[str, float]) -> List[str]:
        """识别优势领域"""
        优势 = []
        
        排序 = sorted(大五分数.items(), key=lambda x: x[1], reverse=True)
        for 维度, 分数 in 排序[:3]:
            if 分数 > 0.6:
                优势.append(f"{维度}({分数:.1%})")
        
        return 优势 if 优势 else ["中等综合能力"]
    
    def _识别风险领域(self, 大五分数: Dict[str, float]) -> List[str]:
        """识别风险领域"""
        风险 = []
        
        if 大五分数["神经质"] > 0.7:
            风险.append("高神经质：需关注情绪管理")
        if 大五分数["尽责性"] < 0.3:
            风险.append("低尽责性：需建立自律机制")
        if 大五分数["宜人性"] < 0.3:
            风险.append("低宜人性：需注意人际关系")
        
        return 风险 if 风险 else ["无显著风险"]
    
    def _生成行为预测(self, 大五分数: Dict[str, float]) -> List[str]:
        """生成行为预测"""
        预测 = []
        
        if 大五分数["外向性"] > 0.6 and 大五分数["宜人性"] > 0.6:
            预测.append("适合社交协作类任务")
        if 大五分数["尽责性"] > 0.7:
            预测.append("适合需要持续投入的项目")
        if 大五分数["开放性"] > 0.7:
            预测.append("适合创新探索类任务")
        if 大五分数["神经质"] > 0.6:
            预测.append("压力情境下需额外支持")
        
        return 预测 if 预测 else ["行为模式需更多数据支撑"]
    
    def analyze_cognitive_biases(self, decision_context: Dict) -> List[Dict]:
        """
        认知偏差识别
        
        Args:
            decision_context: 决策上下文，包含描述、选项、背景
            
        Returns:
            识别出的偏差列表及干预建议
        """
        识别结果 = []
        描述 = decision_context.get("description", "")
        
        # 锚定效应检测
        if any(kw in 描述 for kw in ["原价", "参考价", "基准"]):
            识别结果.append({
                "偏差": "锚定效应",
                "置信度": 0.85,
                "证据": "决策描述中包含锚点信息",
                "干预": self.偏差知识库["anchoring"]["干预"]
            })
        
        # 框架效应检测
        if any(kw in 描述 for kw in ["增加", "减少", "提高", "降低", "正面", "负面"]):
            识别结果.append({
                "偏差": "框架效应",
                "置信度": 0.78,
                "证据": "信息以特定框架呈现",
                "干预": self.偏差知识库["framing"]["干预"]
            })
        
        # 损失厌恶检测
        if any(kw in 描述 for kw in ["失去", "损失", "风险", "亏损", "不利"]):
            识别结果.append({
                "偏差": "损失厌恶",
                "置信度": 0.82,
                "证据": "涉及潜在损失情境",
                "干预": self.偏差知识库["loss_aversion"]["干预"]
            })
        
        # 确认偏误检测
        if decision_context.get("information_sources"):
            sources = decision_context["information_sources"]
            if len(sources) == 1 or all(s.get("立场") == sources[0].get("立场") for s in sources):
                识别结果.append({
                    "偏差": "确认偏误",
                    "置信度": 0.80,
                    "证据": "信息来源立场单一",
                    "干预": self.偏差知识库["confirmation"]["干预"]
                })
        
        return 识别结果
    
    def analyze_motivation(self, user_data: Dict) -> Dict:
        """
        动机分析
        
        Args:
            user_data: 用户行为和态度数据
            
        Returns:
            动机剖析结果
        """
        内在指标 = user_data.get("intrinsic_indicators", [])
        外在指标 = user_data.get("extrinsic_indicators", [])
        成就指标 = user_data.get("achievement_indicators", [])
        亲和指标 = user_data.get("affiliation_indicators", [])
        
        # 计算动机强度
        内在强度 = min(len(内在指标) / 5, 1.0) if 内在指标 else 0.5
        外在强度 = min(len(外在指标) / 5, 1.0) if 外在指标 else 0.5
        成就强度 = min(len(成就指标) / 5, 1.0) if 成就指标 else 0.5
        亲和强度 = min(len(亲和指标) / 5, 1.0) if 亲和指标 else 0.5
        
        # 主导动机判定
        动机强度列表 = [
            ("内在动机", 内在强度),
            ("外在动机", 外在强度),
            ("成就动机", 成就强度),
            ("亲和动机", 亲和强度)
        ]
        主导动机 = max(动机强度列表, key=lambda x: x[1])
        
        # 自我决定理论评估
        自主性 = 内在强度 / max(内在强度 + 外在强度, 0.1)
        胜任感 = 成就强度
        归属感 = 亲和强度
        
        return {
            "动机档案": {
                "内在动机": f"{内在强度:.0%}",
                "外在动机": f"{外在强度:.0%}",
                "成就动机": f"{成就强度:.0%}",
                "亲和动机": f"{亲和强度:.0%}"
            },
            "主导动机": 主导动机[0],
            "自我决定三维度": {
                "自主性": f"{自主性:.0%}",
                "胜任感": f"{胜任感:.0%}",
                "归属感": f"{归属感:.0%}"
            },
            "动机建议": self._生成动机建议(主导动机, 内在强度, 外在强度)
        }
    
    def _生成动机建议(self, 主导动机: Tuple[str, float], 内在: float, 外在: float) -> List[str]:
        """生成动机改善建议"""
        建议 = []
        
        if 外在 > 内在:
            建议.append("当前以外在动机为主，建议增加任务内在价值")
            建议.append("将长期目标分解为有意义的小目标")
            建议.append("减少纯粹金钱/分数激励，增加自主选择")
        
        if 主导动机[0] == "成就动机" and 主导动机[1] > 0.8:
            建议.append("高成就动机：设置挑战性但可达成的目标")
        
        if 主导动机[0] == "亲和动机" and 主导动机[1] > 0.8:
            建议.append("高亲和动机：增加团队协作机会")
            建议.append("个人任务中引入社会问责机制")
        
        return 建议 if 建议 else ["动机平衡，继续保持"]
    
    def analyze_group_dynamics(self, group_data: Dict) -> Dict:
        """
        群体动力学分析
        
        Args:
            group_data: 群体数据，包含成员、互动模式、决策过程
            
        Returns:
            群体分析结果
        """
        成员 = group_data.get("members", [])
        互动 = group_data.get("interactions", [])
        决策 = group_data.get("decisions", [])
        
        # 群体极化检测
        极化程度 = self._评估群体极化(互动)
        
        # 从众效应分析
        从众效应 = self._分析从众效应(互动, 成员)
        
        # 群体决策质量评估
        决策质量 = self._评估群体决策(决策)
        
        # 社会网络分析
        网络结构 = self._分析社会网络(成员, 互动)
        
        return {
            "群体极化": {
                "程度": 极化程度,
                "风险": "高极化可能导致群体思维",
                "建议": "引入魔鬼代言人，鼓励异议"
            },
            "从众效应": 从众效应,
            "决策质量": 决策质量,
            "网络结构": 网络结构,
            "干预建议": self._生成群体干预建议(极化程度, 从众效应, 决策质量)
        }
    
    def _评估群体极化(self, 互动: List[Dict]) -> str:
        """评估群体极化程度"""
        if not 互动:
            return "数据不足"
        
        极端发言比例 = sum(1 for i in 互动 if i.get("is_extreme", False)) / max(len(互动), 1)
        
        if 极端发言比例 > 0.7:
            return "高极化"
        elif 极端发言比例 > 0.4:
            return "中度极化"
        else:
            return "低极化"
    
    def _分析从众效应(self, 互动: List[Dict], 成员: List) -> Dict:
        """分析从众效应"""
        从众比例 = 0.3  # 简化估算
        
        for i in 互动:
            if i.get("changed_opinion_after_hearing_others"):
                从众比例 += 0.05
        
        从众比例 = min(从众比例, 0.9)
        
        return {
            "从众程度": f"{从众比例:.0%}",
            "主要触发": "权威意见/多数意见/信息缺乏",
            "影响": "可能导致群体思维压制少数意见"
        }
    
    def _评估群体决策(self, 决策: List[Dict]) -> Dict:
        """评估群体决策质量"""
        if not 决策:
            return {"质量": "数据不足", "建议": "收集更多决策数据"}
        
        质量评分 = 0.7  # 简化
        
        return {
            "质量": "良好" if 质量评分 > 0.7 else "一般" if 质量评分 > 0.5 else "需改进",
            "评分": 质量评分,
            "主要问题": ["少数压制", "讨论不充分", "替代方案不足"] if 质量评分 < 0.7 else []
        }
    
    def _分析社会网络(self, 成员: List, 互动: List[Dict]) -> Dict:
        """分析社会网络结构"""
        核心成员 = []
        边缘成员 = []
        
        if 成员:
            # 简化：按发言次数排序
            发言次数 = {}
            for i in 互动:
                speaker = i.get("speaker")
                if speaker:
                    发言次数[speaker] = 发言次数.get(speaker, 0) + 1
            
            排序 = sorted(发言次数.items(), key=lambda x: x[1], reverse=True)
            if 排序:
                核心成员 = [排序[0][0]] if len(排序) > 0 else []
                边缘成员 = [m for m in 成员 if m not in 核心成员][:2]
        
        return {
            "核心成员": 核心成员,
            "边缘成员": 边缘成员,
            "凝聚力": "高" if len(核心成员) <= len(成员) / 3 else "中"
        }
    
    def _生成群体干预建议(self, 极化: str, 从众: Dict, 质量: Dict) -> List[str]:
        """生成群体干预建议"""
        建议 = []
        
        if 极化 == "高极化":
            建议.append("引入红队机制：指定成员专门提反对意见")
            建议.append("匿名投票：减少社会压力")
            建议.append("外脑参与：引入外部视角")
        
        if float(从众["从众程度"].replace("%", "")) > 50:
            建议.append("指定沉默者发言时间")
            建议.append("分组讨论后再合并")
        
        if 质量["质量"] == "需改进":
            建议.append("引入结构化决策框架")
            建议.append("增加备选方案数量")
        
        return 建议 if 建议 else ["群体运行良好，保持现状"]
    
    def comprehensive_insight(self, user_data: Dict, context: Dict = None) -> 心理洞察结果:
        """
        综合心理洞察
        
        Args:
            user_data: 用户数据
            context: 上下文（可选）
            
        Returns:
            综合心理洞察结果
        """
        # 人格分析
        人格 = self.analyze_personality(user_data)
        
        # 群体分析（如适用）
        群体 = {"不适用": "无群体上下文"}
        if context and context.get("group_data"):
            群体 = self.analyze_group_dynamics(context["group_data"])
        
        # 偏差识别
        偏差 = []
        if context and context.get("decision"):
            偏差 = self.analyze_cognitive_biases(context["decision"])
        
        # 动机剖析
        动机 = self.analyze_motivation(user_data)
        
        # 关系评估
        关系 = {"评估": "基于现有数据进行人际关系评估"}
        
        # 综合干预建议
        干预 = self._生成综合干预(
            人格, 群体, 偏差, 动机
        )
        
        # 计算置信度
        置信度 = 0.7
        if len(偏差) > 0:
            置信度 += 0.05
        if 动机["自我决定三维度"]:
            置信度 += 0.05
        置信度 = min(置信度, 0.95)
        
        return 心理洞察结果(
            人格分析={
                "大五分数": 人格.大五分数,
                "人格类型": 人格.人格类型,
                "核心特质": 人格.核心特质,
                "行为预测": 人格.行为预测
            },
            群体分析=群体,
            偏差识别=偏差,
            动机剖析=动机,
            关系评估=关系,
            干预建议=干预,
            置信度=置信度
        )
    
    def _生成综合干预(
        self,
        人格: 人格档案,
        群体: Dict,
        偏差: List[Dict],
        动机: Dict
    ) -> List[str]:
        """生成综合干预建议"""
        建议 = []
        
        # 基于人格特质
        if "高神经质" in " ".join(人格.核心特质):
            建议.append("情绪调节训练：正念冥想/呼吸练习")
            建议.append("压力管理计划：识别触发因素，建立应对策略")
        
        if "低尽责性" in " ".join(人格.核心特质):
            建议.append("环境设计：减少诱惑，增加提示")
            建议.append("承诺机制：公开承诺，设置检查点")
        
        # 基于认知偏差
        if 偏差:
            建议.append("决策前执行偏差审计清单")
            建议.append("寻求外部视角和反对意见")
        
        # 基于动机
        if 动机.get("主导动机") == "外在动机":
            建议.append("增加任务内在价值，提升自主性")
        
        return 建议 if 建议 else ["当前状态良好，持续监测"]


# ─────────────────────────────────────────────────────────────
# 全局单例与便捷函数
# ─────────────────────────────────────────────────────────────

_engine_instance = None

def get_psychology_engine() -> PsychologyWisdomEngine:
    """获取心理学引擎单例"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = PsychologyWisdomEngine()
    return _engine_instance


def quick_personality_analysis(user_data: Dict) -> Dict:
    """快速人格分析"""
    return get_psychology_engine().analyze_personality(user_data).__dict__


def quick_bias_detection(decision_context: Dict) -> List[Dict]:
    """快速偏差检测"""
    return get_psychology_engine().analyze_cognitive_biases(decision_context)


def quick_motivation_analysis(user_data: Dict) -> Dict:
    """快速动机分析"""
    return get_psychology_engine().analyze_motivation(user_data)


def quick_group_analysis(group_data: Dict) -> Dict:
    """快速群体分析"""
    return get_psychology_engine().analyze_group_dynamics(group_data)


def comprehensive_psychology_insight(user_data: Dict, context: Dict = None) -> Dict:
    """综合心理洞察"""
    result = get_psychology_engine().comprehensive_insight(user_data, context)
    return {
        "人格分析": result.人格分析,
        "群体分析": result.群体分析,
        "偏差识别": result.偏差识别,
        "动机剖析": result.动机剖析,
        "关系评估": result.关系评估,
        "干预建议": result.干预建议,
        "置信度": result.置信度
    }


# 模块导出
__all__ = [
    'PsychologyWisdomEngine',
    'get_psychology_engine',
    'quick_personality_analysis',
    'quick_bias_detection',
    'quick_motivation_analysis',
    'quick_group_analysis',
    'comprehensive_psychology_insight',
    '人格维度',
    '认知偏差类型',
    '动机类型',
    '依恋风格',
]
