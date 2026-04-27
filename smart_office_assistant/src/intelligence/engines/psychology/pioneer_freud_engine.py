"""
__all__ = [
    'analyze_iceberg',
    'analyze_subconscious_drive',
    'get_marketing_application',
    'identify_defense_mechanism',
    'interpret_dream',
]

心理学先驱深化引擎 - 弗洛伊德潜意识decision引擎
Pioneer Freud - Subconscious Decision Engine
============================================
版本: v8.2.0
创建时间: 2026-04-03

弗洛伊德核心思想:
1. 冰山理论 - 意识/前意识/潜意识三层结构
2. 本我/自我/超我 - 三重人格结构
3. 防御机制 - 压抑/投射/合理化/升华等
4. 梦的解析 - 潜意识愿望的伪装满足
5. 精神分析 - 自由联想/移情/阻抗

核心功能:
1. 潜意识需求挖掘
2. 本能驱动力分析
3. 防御机制recognize
4. 心理阻抗诊断
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

class 潜意识层次(Enum):
    """潜意识层次"""
    意识 = "意识层"           # 可以觉察的
    前意识 = "前意识层"       # 可以召回的
    潜意识 = "潜意识层"       # 无法直接觉察的深层

class 人格结构(Enum):
    """弗洛伊德人格结构"""
    本我 = "本我 (Id)"       # 快乐原则,原始欲望
    自我 = "自我 (Ego)"      # 现实原则,调和者
    超我 = "超我 (Superego)" # 完美原则,道德良心

class 防御机制(Enum):
    """主要防御机制"""
    压抑 = "压抑"           # 把痛苦排除在意识之外
    投射 = "投影"           # 把自己的情感归于他人
    合理化 = "合理化"        # 为自己的行为找借口
    升华 = "升华"            # 把冲动转化为社会认可的活动
    退行 = "退行"           # 退回到早期发展阶段
    否认 = "否认"            # 拒绝承认现实
    转移 = "转移"            # 把情感转移到另一对象
    反向形成 = "反向形成"      # 把无意识冲动转化为相反形式

class 弗洛伊德潜意识引擎:
    """
    弗洛伊德潜意识decision引擎
    
    核心功能:
    1. 冰山分析 - recognize意识/前意识/潜意识层次
    2. 人格诊断 - 分析本我/自我/超我平衡
    3. 防御recognize - recognize常见的心理防御
    4. 需求挖掘 - 挖掘深层的潜意识需求
    5. decision影响 - 分析潜意识如何影响decision
    """
    
    def __init__(self):
        self.name = "弗洛伊德潜意识引擎"
        self.version = "8.2.0"
        
        # 潜意识需求分类
        self.潜意识需求表 = {
            "生存需求": {
                "描述": "最基本的本能驱动力",
                "表现形式": ["食欲", "性欲", "攻击性"],
                "营销应用": "生存本能是最强的购买驱动力"
            },
            "归属需求": {
                "描述": "对群体接纳的渴望",
                "表现形式": ["归属感", "被接纳", "被认可"],
                "营销应用": "社群营销,品牌认同感"
            },
            "权力需求": {
                "描述": "对控制和支配的渴望",
                "表现形式": ["控制感", "优越感", "影响力"],
                "营销应用": "高端品牌,VIP体系"
            },
            "自我实现需求": {
                "描述": "对个人成长和潜能实现",
                "表现形式": ["成长", "成就", "自我超越"],
                "营销应用": "教育培训,个人发展产品"
            },
            "安全需求": {
                "描述": "对稳定和安全感的渴望",
                "表现形式": ["安全感", "稳定性", "保障"],
                "营销应用": "保险,安防产品"
            }
        }
        
        # 防御机制recognize表
        self.防御recognize表 = {
            "压抑": {
                "触发词": ["忘记", "不重要", "算了", "不想说"],
                "表现": "刻意回避某些话题或情感",
                "应对": "不强制追问,建立信任后逐步引导"
            },
            "合理化": {
                "触发词": ["因为", "所以", "当然", "合理"],
                "表现": "为行为找到合乎逻辑的解释",
                "应对": "recognize表面理由下的真实动机"
            },
            "投射": {
                "触发词": ["他们觉得", "别人都", "我觉得你也"],
                "表现": "把自己的情感归于他人或外部",
                "应对": "帮助区分自我感受与他人感受"
            },
            "否认": {
                "触发词": ["不是", "没有", "不可能"],
                "表现": "拒绝承认现实或情感",
                "应对": "提供安全感,允许慢慢接受"
            },
            "退行": {
                "触发词": ["我不管", "就要", "以前不是这样"],
                "表现": "在压力下表现出不成熟的行为",
                "应对": "理解背后的焦虑,提供支持"
            }
        }
        
        # 梦的象征符号
        self.梦的象征 = {
            "水": {"象征": "情感/潜意识", "解释": "水象征情感状态,溺水表示情感被淹没"},
            "坠落": {"象征": "失控/焦虑", "解释": "坠落象征失去控制或安全感的丧失"},
            "追逐": {"象征": "逃避/压力", "解释": "追逐象征逃避某些责任或压力"},
            "死亡": {"象征": "转变/结束", "解释": "死亡象征某种阶段或关系的结束"},
            "性象征": {"象征": "亲密/欲望", "解释": "许多日常物品都可能象征性能量"},
            "动物": {"象征": "本能", "解释": "动物象征未被驯服的本能驱动力"}
        }
    
    def analyze_iceberg(self, statement: str, context: Optional[Dict] = None) -> Dict:
        """
        冰山分析 - recognize显性表达背后的潜意识
        
        Args:
            statement: 用户的表达
            context: 上下文信息
            
        Returns:
            冰山分析结果
        """
        # 提取关键词
        words = list(statement)
        
        # 分析意识层次
        conscious_keywords = ["我想要", "我认为", "我知道", "我决定", "我觉得"]
        preconscious_keywords = ["记得", "想起", "好像", "隐约", "感觉"]
        unconscious_keywords = ["不知道为什么", "控制不住", "总是", "其实"]
        
        意识层次 = 潜意识层次.意识
        for kw in unconscious_keywords:
            if kw in statement:
                意识层次 = 潜意识层次.潜意识
                break
        for kw in preconscious_keywords:
            if kw in statement:
                意识层次 = 潜意识层次.前意识
                break
        
        # 分析人格结构倾向
        本我关键词 = ["想要", "渴望", "欲望", "想", "要", "快乐", "满足"]
        超我关键词 = ["应该", "必须", "不该", "道德", "责任", "义务", "正确"]
        自我关键词 = ["考虑", "权衡", "平衡", "现实", "实际", "合理"]
        
        结构得分 = {"本我": 0, "自我": 0, "超我": 0}
        for kw in 本我关键词:
            if kw in statement:
                结构得分["本我"] += 1
        for kw in 超我关键词:
            if kw in statement:
                结构得分["超我"] += 1
        for kw in 自我关键词:
            if kw in statement:
                结构得分["自我"] += 1
        
        主导结构 = max(结构得分, key=结构得分.get) if max(结构得分.values()) > 0 else "自我"
        
        # 挖掘潜意识需求
        潜在需求 = []
        需求关键词mapping = {
            "归属": ["归属", "接纳", "融入", "群体", "大家"],
            "权力": ["控制", "支配", "影响", "权力", "地位"],
            "安全": ["安全", "保障", "稳定", "放心", "保护"],
            "成就": ["成就", "成功", "实现", "达成", "完成"]
        }
        
        for 需求, keywords in 需求关键词mapping.items():
            for kw in keywords:
                if kw in statement:
                    潜在需求.append(self.潜意识需求表.get(需求, {}).get("描述", 需求))
                    break
        
        return {
            "意识层次": 意识层次.value,
            "主导人格结构": 主导结构,
            "人格结构得分": 结构得分,
            "潜在需求": list(set(潜在需求)),
            "冰山解读": self._generate_iceberg_interpretation(意识层次, 主导结构, 潜在需求),
            "营销洞察": self._generate_marketing_insight(潜在需求)
        }
    
    def _generate_iceberg_interpretation(self, 层次, 结构, 需求) -> str:
        """generate冰山解读"""
        解读 = f"表达处于{层次},"
        if 结构 == "本我":
            解读 += "主要由原始欲望驱动,"
        elif 结构 == "超我":
            解读 += "主要由道德规范约束,"
        else:
            解读 += "在现实和欲望间寻求平衡,"
        
        if 需求:
            解读 += f"潜在的潜意识需求包括:{', '.join(需求)}"
        else:
            解读 += "潜意识需求尚需进一步挖掘"
        
        return 解读
    
    def _generate_marketing_insight(self, 需求: List[str]) -> List[Dict]:
        """generate营销洞察"""
        insights = []
        for 需求 in 需求:
            if 需求 in self.潜意识需求表:
                insights.append({
                    "需求": 需求,
                    "营销应用": self.潜意识需求表[需求]["营销应用"]
                })
        return insights if insights else [{"默认": "理解消费者的深层动机,为其提供超越功能价值的情感价值"}]
    
    def identify_defense_mechanism(self, statement: str) -> Dict:
        """
        recognize防御机制
        
        Args:
            statement: 用户的表达
            
        Returns:
            防御机制recognize结果
        """
        recognize结果 = []
        
        for 机制, info in self.防御recognize表.items():
            for keyword in info["触发词"]:
                if keyword in statement:
                    recognize结果.append({
                        "机制": 机制,
                        "触发词": keyword,
                        "表现": info["表现"],
                        "应对建议": info["应对"]
                    })
                    break
        
        if not recognize结果:
            return {
                "recognize结果": "未发现明显防御机制",
                "解读": "表达较为直接,或需要更多语境进行judge"
            }
        
        return {
            "recognize结果": recognize结果,
            "总体评估": self._evaluate_defense_level(recognize结果),
            "沟通建议": self._generate_communication_suggestion(recognize结果)
        }
    
    def _evaluate_defense_level(self, 结果: List[Dict]) -> str:
        """评估防御水平"""
        if len(结果) >= 2:
            return "高度防御 - 可能存在较强的心理阻抗"
        elif len(结果) == 1:
            return "轻度防御 - 有一定的心理保护倾向"
        else:
            return "开放表达 - 防御较低"
    
    def _generate_communication_suggestion(self, 结果: List[Dict]) -> str:
        """generate沟通建议"""
        if not 结果:
            return "可以直接沟通,注意倾听"
        
        建议 = []
        for r in 结果:
            建议.append(r["应对建议"])
        
        return "; ".join(set(建议))
    
    def analyze_subconscious_drive(self, user_profile: Dict) -> Dict:
        """
        分析潜意识驱动力
        
        Args:
            user_profile: 用户画像
            
        Returns:
            潜意识驱动力分析
        """
        # 简化分析逻辑
        drives = []
        
        # 基于人口统计推断
        age = user_profile.get("age", 30)
        if age < 25:
            drives.append({"驱动力": "探索与新奇", "强度": "高", "建议": "新奇产品,限量版"})
        elif age < 40:
            drives.append({"驱动力": "成就与社会认可", "强度": "高", "建议": "彰显成功的产品"})
        else:
            drives.append({"驱动力": "安全与稳定", "强度": "高", "建议": "可靠品质,长期价值"})
        
        # 基于行为数据
        behavior = user_profile.get("behavior", {})
        if behavior.get("high_spending"):
            drives.append({"驱动力": "炫耀与地位", "强度": "中", "建议": "高端品牌,奢侈品"})
        if behavior.get("social_active"):
            drives.append({"驱动力": "归属与认同", "强度": "中", "建议": "社群营销,口碑传播"})
        
        return {
            "主导驱动力": drives[0] if drives else {"驱动力": "待探索", "强度": "未知"},
            "次级驱动力": drives[1:] if len(drives) > 1 else [],
            "潜意识营销建议": [d["建议"] for d in drives]
        }
    
    def interpret_dream(self, dream_description: str) -> Dict:
        """
        解析梦境
        
        Args:
            dream_description: 梦境描述
            
        Returns:
            梦境解析结果
        """
        symbols_found = []
        
        for symbol, info in self.梦的象征.items():
            if symbol in dream_description:
                symbols_found.append({
                    "符号": symbol,
                    "象征意义": info["象征"],
                    "解释": info["解释"]
                })
        
        if not symbols_found:
            return {
                "梦境类型": "需更多信息",
                "建议": "提供更多细节以便解析"
            }
        
        return {
            "recognize符号": symbols_found,
            "整体解读": self._generate_dream_interpretation(symbols_found),
            "潜意识信息": self._extract_subconscious_message(symbols_found)
        }
    
    def _generate_dream_interpretation(self, symbols: List[Dict]) -> str:
        """generate梦境解读"""
        解读 = "梦境中的符号可能反映以下潜意识信息:"
        for s in symbols:
            解读 += f"\n- {s['符号']}象征{s['象征意义']}:{s['解释']}"
        return 解读
    
    def _extract_subconscious_message(self, symbols: List[Dict]) -> str:
        """提取潜意识信息"""
        meanings = [s["象征意义"] for s in symbols]
        if "情感/潜意识" in meanings:
            return "可能涉及深层的情感需求或未处理的情感问题"
        elif "失控/焦虑" in meanings:
            return "可能反映对失控或压力的焦虑"
        elif "转变/结束" in meanings:
            return "可能标志某种人生阶段的转变"
        else:
            return "需要结合个人情境进一步分析"
    
    def get_marketing_application(self, analysis_result: Dict) -> Dict:
        """
        get营销应用建议
        
        Args:
            analysis_result: 分析结果
            
        Returns:
            营销应用建议
        """
        应用建议 = []
        
        # 基于潜意识需求
        if "潜在需求" in analysis_result:
            for 需求 in analysis_result["潜在需求"]:
                if 需求 in self.潜意识需求表:
                    应用建议.append(self.潜意识需求表[需求]["营销应用"])
        
        # 基于人格结构
        if "主导人格结构" in analysis_result:
            结构 = analysis_result["主导人格结构"]
            if 结构 == "本我":
                应用建议.append("强调感官体验和即时满足")
            elif 结构 == "超我":
                应用建议.append("强调道德价值和社会责任")
            else:
                应用建议.append("提供理性和感性兼具的价值主张")
        
        return {
            "营销建议": 应用建议 if 应用建议 else ["深入理解消费者,提供情感价值"],
            "创意方向": self._suggest_creative_direction(analysis_result),
            "沟通strategy": self._suggest_communication_strategy(analysis_result)
        }
    
    def _suggest_creative_direction(self, analysis: Dict) -> str:
        """建议创意方向"""
        结构 = analysis.get("主导人格结构", "自我")
        层次 = analysis.get("意识层次", "意识层")
        
        if 层次 == "潜意识层":
            return "使用象征,隐喻和情感诉求,触动深层需求"
        elif 结构 == "本我":
            return "强调感官享受和即时满足"
        else:
            return "平衡理性诉求和情感诉求"
    
    def _suggest_communication_strategy(self, analysis: Dict) -> str:
        """建议沟通strategy"""
        if "recognize结果" in analysis and "未发现" not in analysis["recognize结果"]:
            return "采用间接方式,避免直接触及敏感点"
        return "开放直接的沟通方式"

# 全局实例
freud_engine = 弗洛伊德潜意识引擎()
