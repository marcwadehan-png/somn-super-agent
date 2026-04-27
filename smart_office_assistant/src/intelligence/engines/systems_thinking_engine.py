"""
系统论智慧引擎 V1.0.0
====================
版本: V1.0.0
日期: 2026-04-23
来源: V6.0 第二阶段新增学派集成

整合系统论与复杂适应系统理论:

1. 复杂系统建模 - 系统边界/要素/关系/环境
2. 反馈回路设计 - 正反馈/负反馈/延迟效应
3. 涌现行为预测 - 微观到宏观的涌现规律
4. 系统均衡分析 - 稳态/动态平衡/相变点
5. 自适应系统优化 - 鲁棒性/脆弱性/适应性

核心理论来源:
- 贝塔朗菲: 一般系统论
- 维纳: 控制论
- 普里戈金: 耗散结构理论
- 霍兰: 复杂适应系统理论
- 钱学森: 开放复杂巨系统理论
"""

from typing import Dict, List, Optional, Any, Tuple, Set
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime


class 系统类型(Enum):
    """系统类型"""
    简单系统 = "simple"
    复合系统 = "complex"
    复杂系统 = "chaotic"
    适应性系统 = "adaptive"
    开放复杂巨系统 = "mega_open"


class 反馈类型(Enum):
    """反馈类型"""
    正反馈 = "positive"
    负反馈 = "negative"
    延迟反馈 = "delayed"


class 均衡状态(Enum):
    """均衡状态"""
    稳态 = "stable"
    动态平衡 = "dynamic"
    临界态 = "critical"
    相变中 = "transitioning"


@dataclass
class 系统模型:
    """系统模型"""
    系统类型: str
    边界: str
    核心要素: List[str]
    关键关系: List[Dict]
    环境因素: List[str]
    涌现性质: List[str]


@dataclass
class 反馈回路:
    """反馈回路"""
    名称: str
    类型: str
    回路要素: List[str]
    增益: float
    延迟周期: int
    稳定性: str


@dataclass
class 系统诊断:
    """系统诊断结果"""
    系统模型: Dict
    反馈结构: List[Dict]
    均衡分析: Dict
    涌现预测: List[Dict]
    优化建议: List[str]
    风险预警: List[str]
    置信度: float


class SystemsThinkingEngine:
    """
    系统论智慧引擎
    
    整合系统论、控制论、复杂适应系统理论，
    提供复杂问题的系统性分析和解决方案。
    """
    
    VERSION = "V1.0.0"
    
    def __init__(self):
        self.name = "系统论智慧引擎"
        self.理论框架 = self._初始化理论框架()
        self.系统模式库 = self._初始化系统模式库()
        self.干预策略库 = self._初始化干预策略库()
    
    def _初始化理论框架(self) -> Dict:
        """初始化系统论理论框架"""
        return {
            "贝塔朗菲一般系统论": {
                "核心": "系统整体性、层次性、动态性",
                "方程": "整体大于部分之和",
                "应用": "生态系统、组织管理"
            },
            "维纳控制论": {
                "核心": "反馈机制、信息与控制",
                "方程": "输入→系统→输出→反馈→输入",
                "应用": "自动控制、管理调节"
            },
            "普里戈金耗散结构": {
                "核心": "开放系统、远离平衡、自组织",
                "方程": "熵减→有序结构形成",
                "应用": "生命系统、社会系统"
            },
            "霍兰复杂适应系统": {
                "核心": "适应性主体、涌现、混沌边缘",
                "机制": "学习、反馈、竞争、合作",
                "应用": "经济系统、生态系统"
            },
            "钱学森开放复杂巨系统": {
                "核心": "开放、复杂、层次、整体",
                "方法": "定性定量结合、人机结合",
                "应用": "社会系统、智慧系统"
            }
        }
    
    def _初始化系统模式库(self) -> Dict:
        """初始化常见系统模式库"""
        return {
            "增长极限": {
                "结构": "增长→资源受限→减速→平衡/崩溃",
                "杠杆点": "限制因素管理",
                "案例": "人口增长、环境承载"
            },
            "转移负担": {
                "结构": "问题症状→短期解→依赖→根本问题恶化",
                "杠杆点": "恢复根本解能力",
                "案例": "成瘾行为、组织依赖"
            },
            "公地悲剧": {
                "结构": "公共资源→个体理性→过度使用→资源枯竭",
                "杠杆点": "建立规则或私有化",
                "案例": "环境污染、过度捕捞"
            },
            "竞争升级": {
                "结构": "A增强→B感受到威胁→B增强→A更强",
                "杠杆点": "一方主动退出或引入调解",
                "案例": "价格战、军备竞赛"
            },
            "目标侵蚀": {
                "结构": "绩效差距→短期让步→目标下调→差距消失",
                "杠杆点": "保持高标准、公开目标",
                "案例": "组织目标偏移"
            },
            "饮鸩止渴": {
                "结构": "问题→短期缓解→长期恶化→更多使用",
                "杠杆点": "寻找根本解决方案",
                "案例": "债务、药物依赖"
            }
        }
    
    def _初始化干预策略库(self) -> Dict:
        """初始化系统干预策略库"""
        return {
            "杠杆点层次": [
                "12. 参数调整", "11. 物质存量", "10. 结构",
                "9. 信息流", "8. 系统规则", "7. 自组织",
                "6. 目标", "5. 社会典范", "4. 价值观",
                "3. 思维模式", "2. 超越范式", "1. 范式/目标/系统本身"
            ],
            "干预时机": {
                "预防性": "在系统积累成问题之前介入",
                "及时性": "在转折点附近介入",
                "补救性": "在问题严重后干预"
            },
            "干预范围": {
                "局部": "针对特定反馈回路",
                "结构": "改变系统结构",
                "目标": "改变系统目标",
                "范式": "改变根本假设"
            }
        }
    
    def model_system(
        self,
        description: str,
        elements: List[str] = None,
        relationships: List[Dict] = None
    ) -> 系统模型:
        """系统建模"""
        if elements is None:
            elements = self._提取系统要素(description)
        
        if relationships is None:
            relationships = self._识别系统关系(elements, description)
        
        系统类型 = self._判定系统类型(elements, relationships)
        边界 = self._确定系统边界(description, elements)
        环境因素 = self._识别环境因素(description, elements)
        涌现性质 = self._识别涌现性质(elements, relationships)
        
        return 系统模型(
            系统类型=系统类型,
            边界=边界,
            核心要素=elements,
            关键关系=relationships,
            环境因素=环境因素,
            涌现性质=涌现性质
        )
    
    def _提取系统要素(self, description: str) -> List[str]:
        """提取系统核心要素"""
        keywords = ["用户", "产品", "服务", "市场", "竞争", "技术", "团队", "资源", "政策"]
        found = [kw for kw in keywords if kw in description]
        if not found:
            found = [f"要素{i+1}" for i in range(5)]
        return found
    
    def _识别系统关系(self, elements: List[str], description: str) -> List[Dict]:
        """识别系统关系"""
        关系 = []
        for i in range(len(elements) - 1):
            关系.append({
                "from": elements[i],
                "to": elements[i + 1],
                "type": "因果",
                "strength": 0.5 + (i % 3) * 0.15,
                "delay": i % 3
            })
        return 关系
    
    def _判定系统类型(self, elements: List[str], relationships: List[Dict]) -> str:
        """判定系统类型"""
        复杂度 = len(elements) * len(relationships)
        if 复杂度 < 10:
            return 系统类型.简单系统.value
        elif 复杂度 < 30:
            return 系统类型.复合系统.value
        elif 复杂度 < 60:
            return 系统类型.复杂系统.value
        else:
            return 系统类型.适应性系统.value
    
    def _确定系统边界(self, description: str, elements: List[str]) -> str:
        """确定系统边界"""
        return "根据目标和研究问题动态确定"
    
    def _识别环境因素(self, description: str, elements: List[str]) -> List[str]:
        """识别环境因素"""
        return ["政策环境", "经济环境", "技术环境", "社会文化"]
    
    def _识别涌现性质(self, elements: List[str], relationships: List[Dict]) -> List[str]:
        """识别涌现性质"""
        涌现 = []
        if len(elements) > 5:
            涌现.append("整体协同效应")
        if len(relationships) > 3:
            涌现.append("涌现行为可能出现")
        if any(r.get("type") == "正反馈" for r in relationships):
            涌现.append("可能存在增长或衰减")
        return 涌现 if 涌现 else ["基础涌现性质"]
    
    def analyze_feedback_loops(
        self,
        system_model: 系统模型,
        known_loops: List[Dict] = None
    ) -> List[反馈回路]:
        """分析反馈回路"""
        回路 = []
        
        if known_loops:
            for loop in known_loops:
                回路.append(反馈回路(
                    名称=loop.get("name", "未命名回路"),
                    类型=loop.get("type", "unknown"),
                    回路要素=loop.get("elements", []),
                    增益=loop.get("gain", 1.0),
                    延迟周期=loop.get("delay", 0),
                    稳定性="稳定" if loop.get("type") == "负反馈" else "不稳定"
                ))
        else:
            for i in range(min(3, len(system_model.核心要素))):
                回路.append(反馈回路(
                    名称=f"回路{i+1}",
                    类型=反馈类型.负反馈.value if i % 2 == 0 else 反馈类型.正反馈.value,
                    回路要素=system_model.核心要素[:3],
                    增益=1.0 + (i * 0.2),
                    延迟周期=i,
                    稳定性="稳定" if i % 2 == 0 else "需监控"
                ))
        
        return 回路
    
    def predict_emergence(
        self,
        system_model: 系统模型,
        conditions: Dict = None
    ) -> List[Dict]:
        """涌现行为预测"""
        预测 = []
        
        if system_model.系统类型 == 系统类型.适应性系统.value:
            预测.append({
                "涌现类型": "自适应行为",
                "描述": "系统主体将学习和适应环境变化",
                "概率": "高",
                "影响": "系统整体性能提升"
            })
        
        密度 = len(system_model.关键关系) / max(len(system_model.核心要素), 1)
        if 密度 > 0.5:
            预测.append({
                "涌现类型": "同步行为",
                "描述": "要素之间可能产生同步或协调行为",
                "概率": "中",
                "影响": "可能形成有序结构或群体行为"
            })
        
        正反馈数 = sum(1 for r in system_model.关键关系 if r.get("type") == "正反馈")
        if 正反馈数 > 0:
            预测.append({
                "涌现类型": "增长或衰减",
                "描述": "正反馈回路可能导致快速增长或崩溃",
                "概率": "中",
                "影响": "需监控和调节"
            })
        
        return 预测 if 预测 else [{"涌现类型": "基础行为", "描述": "系统运行正常", "概率": "高", "影响": "无显著变化"}]
    
    def analyze_equilibrium(
        self,
        system_model: 系统模型,
        feedback_loops: List[反馈回路]
    ) -> Dict:
        """系统均衡分析"""
        总增益 = sum(f.增益 for f in feedback_loops)
        延迟效应 = any(f.延迟周期 > 2 for f in feedback_loops)
        
        if 总增益 < 1.0 and not 延迟效应:
            均衡 = 均衡状态.稳态
        elif 0.8 < 总增益 < 1.2:
            均衡 = 均衡状态.动态平衡
        elif 延迟效应 and 0.9 < 总增益 < 1.1:
            均衡 = 均衡状态.临界态
        else:
            均衡 = 均衡状态.相变中
        
        return {
            "均衡状态": 均衡.value,
            "总增益": f"{总增益:.2f}",
            "延迟效应": "存在" if 延迟效应 else "无",
            "稳定性评估": self._评估稳定性(总增益, 延迟效应),
            "相变信号": self._识别相变信号(system_model, feedback_loops),
            "管理建议": self._生成均衡管理建议(均衡, 总增益, 延迟效应)
        }
    
    def _评估稳定性(self, 增益: float, 延迟: bool) -> str:
        """评估稳定性"""
        if 增益 < 0.8:
            return "衰减趋势"
        elif 增益 < 1.1:
            return "相对稳定"
        elif 增益 < 1.5:
            return "增长趋势"
        else:
            return "快速增长/潜在失控"
    
    def _识别相变信号(self, model, loops) -> List[str]:
        """识别相变信号"""
        信号 = []
        if len(loops) > 5:
            信号.append("回路复杂度增加")
        if any(l.类型 == "正反馈" for l in loops):
            信号.append("正反馈增强")
        return 信号 if 信号 else ["无明显相变信号"]
    
    def _生成均衡管理建议(self, 均衡, 增益, 延迟) -> List[str]:
        """生成均衡管理建议"""
        建议 = []
        if 均衡 == 均衡状态.稳态:
            建议.append("系统稳定，保持现状")
        elif 均衡 == 均衡状态.动态平衡:
            建议.append("动态平衡中，监控关键参数")
        elif 均衡 == 均衡状态.临界态:
            建议.append("接近相变点，准备干预预案")
            建议.append("增加监控频率")
        else:
            建议.append("系统正在转变中")
            建议.append("评估正反馈来源")
        return 建议
    
    def optimize_adaptive_system(
        self,
        system_model: 系统模型,
        goal: str
    ) -> Dict:
        """自适应系统优化"""
        当前状态 = {
            "系统类型": system_model.系统类型,
            "要素数量": len(system_model.核心要素),
            "关系数量": len(system_model.关键关系),
            "涌现性质": system_model.涌现性质
        }
        
        干预策略 = self._设计干预策略(system_model, goal)
        
        鲁棒性分析 = {
            "当前鲁棒性": "中等",
            "脆弱点": ["部分关系强度不足"],
            "建议": "增强关键关系"
        }
        
        适应性建议 = ["建立反馈机制持续监测", "保持适度冗余", "促进信息流通"]
        
        return {
            "当前状态": 当前状态,
            "优化目标": goal,
            "干预策略": 干预策略,
            "鲁棒性分析": 鲁棒性分析,
            "适应性建议": 适应性建议,
            "实施路径": self._设计实施路径(goal)
        }
    
    def _设计干预策略(self, model: 系统模型, goal: str) -> List[Dict]:
        """设计干预策略"""
        策略 = []
        if "效率" in goal:
            策略.append({"层次": "参数调整", "策略": "优化流速/存量", "可行性": "高"})
        if "稳定" in goal:
            策略.append({"层次": "反馈调节", "策略": "增强负反馈", "可行性": "中"})
        if "创新" in goal:
            策略.append({"层次": "自组织", "策略": "允许涌现", "可行性": "中"})
        return 策略 if 策略 else [{"层次": "参数调整", "策略": "微调关键参数", "可行性": "高"}]
    
    def _设计实施路径(self, goal: str) -> List[str]:
        """设计实施路径"""
        return [
            "第一步：建立系统模型基线",
            "第二步：识别关键杠杆点",
            "第三步：小规模试点干预",
            "第四步：监测反馈并调整",
            "第五步：扩大实施范围"
        ]
    
    def comprehensive_diagnosis(
        self,
        system_description: str,
        context: Dict = None
    ) -> 系统诊断:
        """综合系统诊断"""
        系统模型 = self.model_system(system_description)
        
        反馈结构 = []
        loops = self.analyze_feedback_loops(系统模型)
        for loop in loops:
            反馈结构.append({
                "名称": loop.名称,
                "类型": loop.类型,
                "增益": loop.增益,
                "稳定性": loop.稳定性
            })
        
        均衡分析 = self.analyze_equilibrium(系统模型, loops)
        涌现预测 = self.predict_emergence(系统模型)
        优化建议 = self._生成综合优化建议(系统模型, 均衡分析)
        风险预警 = self._识别系统风险(系统模型, loops)
        
        置信度 = 0.7 + (0.05 * min(len(系统模型.核心要素), 5))
        置信度 = min(置信度, 0.9)
        
        return 系统诊断(
            系统模型={
                "类型": 系统模型.系统类型,
                "要素": 系统模型.核心要素,
                "关系": 系统模型.关键关系,
                "边界": 系统模型.边界,
                "涌现": 系统模型.涌现性质
            },
            反馈结构=反馈结构,
            均衡分析=均衡分析,
            涌现预测=涌现预测,
            优化建议=优化建议,
            风险预警=风险预警,
            置信度=置信度
        )
    
    def _生成综合优化建议(self, model, 均衡分析) -> List[str]:
        """生成综合优化建议"""
        建议 = []
        if model.系统类型 in [系统类型.复杂系统.value, 系统类型.适应性系统.value]:
            建议.append("建立多层次反馈机制")
        if 均衡分析.get("延迟效应") == "存在":
            建议.append("设计延迟补偿机制")
        建议.append("持续监测关键指标")
        建议.append("保持系统适度弹性")
        return 建议
    
    def _识别系统风险(self, model, loops) -> List[str]:
        """识别系统风险"""
        风险 = []
        正反馈数 = sum(1 for l in loops if l.类型 == "正反馈" and l.增益 > 1.2)
        if 正反馈数 > 0:
            风险.append(f"存在{正反馈数}个高增益正反馈，可能导致失控")
        延迟回路数 = sum(1 for l in loops if l.延迟周期 > 2)
        if 延迟回路数 > 0:
            风险.append(f"存在{延迟回路数}个长延迟回路，可能导致振荡")
        if len(model.核心要素) > 10:
            风险.append("系统复杂度较高，管理难度增加")
        return 风险 if 风险 else ["无显著风险"]


# 全局单例与便捷函数
_engine_instance = None

def get_systems_engine() -> SystemsThinkingEngine:
    """获取系统论引擎单例"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = SystemsThinkingEngine()
    return _engine_instance


def quick_system_modeling(description: str) -> Dict:
    """快速系统建模"""
    return get_systems_engine().model_system(description).__dict__


def quick_feedback_analysis(system_description: str) -> List[Dict]:
    """快速反馈分析"""
    model = get_systems_engine().model_system(system_description)
    loops = get_systems_engine().analyze_feedback_loops(model)
    return [{"名称": l.名称, "类型": l.类型, "增益": l.增益} for l in loops]


def quick_emergence_prediction(system_description: str) -> List[Dict]:
    """快速涌现预测"""
    model = get_systems_engine().model_system(system_description)
    return get_systems_engine().predict_emergence(model)


def quick_equilibrium_analysis(system_description: str) -> Dict:
    """快速均衡分析"""
    engine = get_systems_engine()
    model = engine.model_system(system_description)
    loops = engine.analyze_feedback_loops(model)
    return engine.analyze_equilibrium(model, loops)


def systems_diagnosis(system_description: str, context: Dict = None) -> Dict:
    """综合系统诊断"""
    result = get_systems_engine().comprehensive_diagnosis(system_description, context)
    return {
        "系统模型": result.系统模型,
        "反馈结构": result.反馈结构,
        "均衡分析": result.均衡分析,
        "涌现预测": result.涌现预测,
        "优化建议": result.优化建议,
        "风险预警": result.风险预警,
        "置信度": result.置信度
    }


__all__ = [
    'SystemsThinkingEngine',
    'get_systems_engine',
    'quick_system_modeling',
    'quick_feedback_analysis',
    'quick_emergence_prediction',
    'quick_equilibrium_analysis',
    'systems_diagnosis',
    '系统类型',
    '反馈类型',
    '均衡状态',
]
