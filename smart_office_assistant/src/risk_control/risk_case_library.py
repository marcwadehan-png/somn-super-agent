"""
__all__ = [
    'add_case',
    'analyze_content_risk',
    'export_case_report',
    'get_case',
    'get_cases_by_level',
    'get_cases_by_type',
    'get_prevention_guide',
    'get_statistics',
    'search_cases',
]

风险案例库模块 - 情绪营销风险案例管理
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class RiskType(Enum):
    """风险类型"""
    ANXIETY_AMPLIFICATION = "anxiety_amplification"      # 焦虑放大
    EMOTIONAL_MANIPULATION = "emotional_manipulation"    # 情绪操控
    PRIVACY_BREACH = "privacy_breach"                    # 隐私泄露
    DISCRIMINATION = "discrimination"                    # 歧视内容
    HOMOGENIZATION = "homogenization"                    # 同质化
    DELIVERY_GAP = "delivery_gap"                        # 交付不一致
    LEGAL_VIOLATION = "legal_violation"                  # 法律违规
    CULTURAL_OFFENSE = "cultural_offense"                # 文化冒犯

class RiskLevel(Enum):
    """风险等级"""
    CRITICAL = "critical"    # 严重
    HIGH = "high"           # 高
    MEDIUM = "medium"       # 中
    LOW = "low"             # 低

@dataclass
class RiskCase:
    """风险案例"""
    case_id: str
    title: str
    risk_type: RiskType
    risk_level: RiskLevel
    description: str
    trigger_content: str  # 触发风险的原始内容
    consequences: List[str]  # 造成的后果
    lessons_learned: List[str]  # 经验教训
    prevention_measures: List[str]  # 预防措施
    related_regulations: List[str]  # 相关法规
    case_date: datetime
    source: str = ""  # 案例来源
    industry: str = ""  # 所属行业

class RiskCaseLibrary:
    """
    风险案例库
    
    管理和查询情绪营销风险案例,包括:
    - 典型案例收录
    - 风险模式recognize
    - 预防措施建议
    """
    
    def __init__(self):
        self.cases: List[RiskCase] = []
        self._initialize_default_cases()
        
    def _initialize_default_cases(self):
        """init默认案例"""
        
        # === 焦虑放大类案例 ===
        self.add_case(RiskCase(
            case_id="AA-001",
            title="教育培训机构焦虑营销翻车事件",
            risk_type=RiskType.ANXIETY_AMPLIFICATION,
            risk_level=RiskLevel.HIGH,
            description="某教育培训机构在广告中大量使用'您的孩子已经输在起跑线','不报名就晚了'等极端焦虑话术,引发家长强烈反感",
            trigger_content="'别的孩子都在学,您的孩子还在玩?','错过3-6岁黄金期,孩子一辈子落后'",
            consequences=[
                "社交媒体大量负面评论",
                "家长集体投诉至监管部门",
                "品牌口碑严重受损",
                "被市场监管部门约谈"
            ],
            lessons_learned=[
                "焦虑营销需要适度,过度会引发反感",
                "应该强调解决方案而非放大问题",
                "需要平衡情绪引导的正面和负面"
            ],
            prevention_measures=[
                "焦虑指数控制在0.3以下",
                "解决方案内容占比超过50%",
                "增加积极正向的情绪引导"
            ],
            related_regulations=["<广告法>第9条", "<消费者权益保护法>"],
            case_date=datetime(2023, 6, 15),
            source="公开报道",
            industry="教育培训"
        ))
        
        self.add_case(RiskCase(
            case_id="AA-002",
            title="医美机构'容貌焦虑'营销被处罚",
            risk_type=RiskType.ANXIETY_AMPLIFICATION,
            risk_level=RiskLevel.CRITICAL,
            description="某医美机构通过制造'容貌焦虑'进行营销,使用'丑女逆袭','颜值即正义'等不当表述",
            trigger_content="'长得不好看连工作都找不到','你的脸值多少钱?'",
            consequences=[
                "被市场监管部门罚款50万元",
                "广告被强制下架",
                "引发社会舆论批评",
                "多家媒体跟进报道"
            ],
            lessons_learned=[
                "不能利用消费者的身体焦虑进行营销",
                "尊重消费者的人格尊严",
                "营销内容需要符合社会公序良俗"
            ],
            prevention_measures=[
                "避免使用身体羞辱性语言",
                "强调健康美而非外貌焦虑",
                "建立内容伦理审查机制"
            ],
            related_regulations=["<广告法>第9条", "<反不正当竞争法>"],
            case_date=datetime(2023, 9, 20),
            source="行政处罚公示",
            industry="医疗美容"
        ))
        
        # === 隐私泄露类案例 ===
        self.add_case(RiskCase(
            case_id="PB-001",
            title="品牌泄露用户聊天记录引发危机",
            risk_type=RiskType.PRIVACY_BREACH,
            risk_level=RiskLevel.CRITICAL,
            description="某品牌在宣传中使用了与用户的完整聊天记录截图,包含用户真实姓名,手机号,地址等敏感信息",
            trigger_content="公开的聊天记录截图中包含:用户手机号138****8888,收货地址北京市朝阳区***小区**号楼**单元",
            consequences=[
                "用户隐私被公开泄露",
                "面临法律诉讼风险",
                "品牌信任度崩塌",
                "被监管部门调查"
            ],
            lessons_learned=[
                "用户数据使用必须获得明确授权",
                "公开内容必须进行隐私脱敏处理",
                "建立严格的数据使用审批流程"
            ],
            prevention_measures=[
                "所有用户数据使用需书面授权",
                "发布前进行隐私信息扫描",
                "敏感信息必须脱敏或打码",
                "建立数据使用审计机制"
            ],
            related_regulations=["<个人信息保护法>第28条", "<民法典>第1034条"],
            case_date=datetime(2023, 11, 8),
            source="用户投诉",
            industry="电商零售"
        ))
        
        self.add_case(RiskCase(
            case_id="PB-002",
            title="营销案例泄露客户商业机密",
            risk_type=RiskType.PRIVACY_BREACH,
            risk_level=RiskLevel.HIGH,
            description="某营销公司在案例分享中,泄露了B端客户的内部数据,strategy细节和未公开的产品信息",
            trigger_content="案例中提到:'某客户(实际点名)的Q3销售额为5000万,毛利率35%,主要成本在...'",
            consequences=[
                "客户商业机密泄露",
                "客户终止合作并索赔",
                "行业声誉严重受损",
                "面临商业机密侵权诉讼"
            ],
            lessons_learned=[
                "B端客户案例需要更严格的保密审查",
                "商业数据不能作为营销素材公开",
                "建立客户数据分级保护机制"
            ],
            prevention_measures=[
                "案例发布前需客户书面确认",
                "敏感商业数据必须脱敏",
                "建立客户数据访问权限控制"
            ],
            related_regulations=["<反不正当竞争法>第9条", "<民法典>第501条"],
            case_date=datetime(2023, 8, 12),
            source="行业报道",
            industry="营销服务"
        ))
        
        # === 歧视类案例 ===
        self.add_case(RiskCase(
            case_id="DI-001",
            title="招聘广告性别歧视被处罚",
            risk_type=RiskType.DISCRIMINATION,
            risk_level=RiskLevel.CRITICAL,
            description="某公司在招聘广告中明确标注'限男性','女性需已婚已育'等歧视性要求",
            trigger_content="'本岗位限男性,女性请勿投递','要求已婚已育,能全身心投入工作'",
            consequences=[
                "被劳动监察部门处罚",
                "招聘广告被强制下架",
                "引发性别平等议题讨论",
                "企业形象严重受损"
            ],
            lessons_learned=[
                "招聘内容不能有性别,年龄,婚育等歧视",
                "就业平等是法律红线",
                "歧视性内容会引发社会舆论危机"
            ],
            prevention_measures=[
                "建立招聘内容合规审查",
                "培训HR团队法律意识",
                "使用包容性语言"
            ],
            related_regulations=["<劳动法>第12条", "<就业促进法>第27条", "<妇女权益保障法>"],
            case_date=datetime(2023, 5, 22),
            source="行政处罚公示",
            industry="人力资源"
        ))
        
        self.add_case(RiskCase(
            case_id="DI-002",
            title="广告内容地域歧视引发争议",
            risk_type=RiskType.DISCRIMINATION,
            risk_level=RiskLevel.HIGH,
            description="某品牌在广告中使用了带有地域偏见的内容,暗示某些地区的人群素质较低",
            trigger_content="'不像某些地方的人,我们的用户都是高素质人群'",
            consequences=[
                "引发地域歧视争议",
                "社交媒体舆论发酵",
                "多地消费者抵制",
                "被迫公开道歉"
            ],
            lessons_learned=[
                "营销内容不能有任何形式的歧视",
                "地域,民族,文化都需要尊重",
                "歧视性内容会迅速引发舆论危机"
            ],
            prevention_measures=[
                "内容发布前进行歧视性检测",
                "避免使用对比性贬低语言",
                "建立多元化内容审核团队"
            ],
            related_regulations=["<广告法>第9条", "<消费者权益保护法>"],
            case_date=datetime(2023, 10, 5),
            source="社交媒体",
            industry="快消品"
        ))
        
        # === 同质化类案例 ===
        self.add_case(RiskCase(
            case_id="HO-001",
            title="'内卷'营销话术全行业泛滥",
            risk_type=RiskType.HOMOGENIZATION,
            risk_level=RiskLevel.MEDIUM,
            description="某段时间内,几乎所有品牌都在使用'内卷','躺平','emo'等网络热词进行营销,导致消费者审美疲劳",
            trigger_content="多个品牌广告:'拒绝内卷,选择我们','不再emo,从这里开始'",
            consequences=[
                "消费者产生审美疲劳",
                "品牌差异化度降低",
                "营销效果大幅下降",
                "被消费者吐槽'跟风'"
            ],
            lessons_learned=[
                "跟风热点会导致同质化",
                "需要挖掘品牌独特的情绪价值",
                "创新比追热点更重要"
            ],
            prevention_measures=[
                "建立差异化评估机制",
                "挖掘细分场景独特痛点",
                "避免使用全行业通用话术"
            ],
            related_regulations=["<反不正当竞争法>"],
            case_date=datetime(2022, 12, 10),
            source="行业观察",
            industry="多行业"
        ))
        
        # === 交付不一致类案例 ===
        self.add_case(RiskCase(
            case_id="DG-001",
            title="承诺'治愈'却无法兑现引发维权",
            risk_type=RiskType.DELIVERY_GAP,
            risk_level=RiskLevel.HIGH,
            description="某心理健康App在营销中承诺'30天治愈焦虑',但实际服务效果远低于承诺,引发用户集体维权",
            trigger_content="'30天告别焦虑','100%治愈保证','无效全额退款'",
            consequences=[
                "大量用户要求退款",
                "消费者协会介入",
                "应用商店评分暴跌",
                "面临虚假宣传诉讼"
            ],
            lessons_learned=[
                "营销承诺必须可兑现",
                "不能夸大产品效果",
                "心理健康服务不能承诺'治愈'"
            ],
            prevention_measures=[
                "建立承诺-能力匹配审查",
                "避免绝对化效果承诺",
                "确保退款承诺可执行"
            ],
            related_regulations=["<广告法>第4条", "<消费者权益保护法>第20条"],
            case_date=datetime(2023, 7, 18),
            source="消费者投诉",
            industry="心理健康"
        ))
        
        self.add_case(RiskCase(
            case_id="DG-002",
            title="奢侈品营销承诺服务无法兑现",
            risk_type=RiskType.DELIVERY_GAP,
            risk_level=RiskLevel.MEDIUM,
            description="某奢侈品牌承诺VIP客户'24小时专属客服','专属定制服务',实际服务体验与承诺严重不符",
            trigger_content="'24小时专属管家服务','一对一私人定制','尊享VIP特权'",
            consequences=[
                "VIP客户大量流失",
                "负面口碑传播",
                "品牌高端形象受损",
                "客户投诉率上升"
            ],
            lessons_learned=[
                "高端营销承诺需要匹配服务能力",
                "过度承诺会损害品牌信誉",
                "服务一致性是品牌信任的基础"
            ],
            prevention_measures=[
                "营销承诺需经服务部门确认",
                "建立服务交付监控机制",
                "定期评估承诺兑现率"
            ],
            related_regulations=["<消费者权益保护法>", "<反不正当竞争法>"],
            case_date=datetime(2023, 4, 25),
            source="客户反馈",
            industry="奢侈品"
        ))
        
        # === 法律违规类案例 ===
        self.add_case(RiskCase(
            case_id="LV-001",
            title="使用绝对化用语被处罚",
            risk_type=RiskType.LEGAL_VIOLATION,
            risk_level=RiskLevel.HIGH,
            description="某品牌在广告中使用了'最佳','第一','顶级'等绝对化用语,违反<广告法>",
            trigger_content="'行业第一品牌','最佳效果','顶级品质','绝无仅有'",
            consequences=[
                "被罚款20万元",
                "广告被强制下架",
                "需重新制作营销素材",
                "合规成本增加"
            ],
            lessons_learned=[
                "广告法禁用绝对化用语",
                "需要使用相对性,可证明的表述",
                "建立广告法合规词库"
            ],
            prevention_measures=[
                "建立禁用词库和审查机制",
                "使用可验证的相对性表述",
                "定期进行广告法培训"
            ],
            related_regulations=["<广告法>第9条"],
            case_date=datetime(2023, 3, 12),
            source="行政处罚公示",
            industry="多行业"
        ))
        
        # === 文化冒犯类案例 ===
        self.add_case(RiskCase(
            case_id="CO-001",
            title="广告内容冒犯特定宗教群体",
            risk_type=RiskType.CULTURAL_OFFENSE,
            risk_level=RiskLevel.CRITICAL,
            description="某国际品牌广告中使用了不当的宗教元素,冒犯了特定宗教信仰群体",
            trigger_content="广告中使用了宗教符号进行商业宣传",
            consequences=[
                "引发宗教群体抗议",
                "多国发起抵制运动",
                "被迫全球下架广告",
                "品牌形象严重受损"
            ],
            lessons_learned=[
                "宗教文化需要特别尊重",
                "跨文化营销需要本地化审查",
                "宗教元素不能用于商业宣传"
            ],
            prevention_measures=[
                "建立宗教文化敏感性审查",
                "跨文化内容进行本地化测试",
                "咨询宗教文化专家"
            ],
            related_regulations=["<广告法>第9条", "<宗教事务条例>"],
            case_date=datetime(2023, 2, 8),
            source="国际新闻",
            industry="快消品"
        ))
    
    def add_case(self, case: RiskCase):
        """添加案例"""
        self.cases.append(case)
    
    def get_case(self, case_id: str) -> Optional[RiskCase]:
        """get指定案例"""
        for case in self.cases:
            if case.case_id == case_id:
                return case
        return None
    
    def search_cases(self, risk_type: Optional[RiskType] = None,
                    risk_level: Optional[RiskLevel] = None,
                    industry: Optional[str] = None,
                    keyword: Optional[str] = None) -> List[RiskCase]:
        """
        搜索案例
        
        Args:
            risk_type: 风险类型
            risk_level: 风险等级
            industry: 行业
            keyword: 关键词
            
        Returns:
            案例列表
        """
        results = self.cases
        
        if risk_type:
            results = [c for c in results if c.risk_type == risk_type]
        
        if risk_level:
            results = [c for c in results if c.risk_level == risk_level]
        
        if industry:
            results = [c for c in results if c.industry == industry]
        
        if keyword:
            keyword = keyword.lower()
            results = [
                c for c in results
                if (keyword in c.title.lower() or
                    keyword in c.description.lower() or
                    any(keyword in lesson.lower() for lesson in c.lessons_learned))
            ]
        
        return results
    
    def get_cases_by_type(self, risk_type: RiskType) -> List[RiskCase]:
        """按类型get案例"""
        return [c for c in self.cases if c.risk_type == risk_type]
    
    def get_cases_by_level(self, risk_level: RiskLevel) -> List[RiskCase]:
        """按等级get案例"""
        return [c for c in self.cases if c.risk_level == risk_level]
    
    def get_prevention_guide(self, risk_type: RiskType) -> Dict:
        """
        get预防指南
        
        Args:
            risk_type: 风险类型
            
        Returns:
            预防指南
        """
        cases = self.get_cases_by_type(risk_type)
        
        if not cases:
            return {"message": "暂无该类型的案例"}
        
        all_measures = []
        all_regulations = []
        
        for case in cases:
            all_measures.extend(case.prevention_measures)
            all_regulations.extend(case.related_regulations)
        
        return {
            "risk_type": risk_type.value,
            "case_count": len(cases),
            "prevention_measures": list(set(all_measures)),
            "related_regulations": list(set(all_regulations)),
            "typical_cases": [
                {
                    "case_id": c.case_id,
                    "title": c.title,
                    "risk_level": c.risk_level.value
                }
                for c in cases[:3]  # 最多3个典型案例
            ]
        }
    
    def analyze_content_risk(self, content: str) -> List[Dict]:
        """
        分析内容风险(基于案例库)
        
        Args:
            content: 待分析内容
            
        Returns:
            风险分析结果
        """
        risks = []
        content_lower = content.lower()
        
        for case in self.cases:
            # 检查是否包含触发内容的关键词
            if case.trigger_content.lower() in content_lower:
                risks.append({
                    "matched_case": case.case_id,
                    "title": case.title,
                    "risk_type": case.risk_type.value,
                    "risk_level": case.risk_level.value,
                    "similarity": "高",
                    "suggestion": f"参考案例{case.case_id},建议:{case.prevention_measures[0]}"
                })
        
        return risks
    
    def export_case_report(self, risk_type: Optional[RiskType] = None) -> Dict:
        """
        导出案例报告
        
        Args:
            risk_type: 指定风险类型,None则导出全部
            
        Returns:
            案例报告
        """
        cases = self.cases if risk_type is None else self.get_cases_by_type(risk_type)
        
        # 统计
        type_distribution = {}
        level_distribution = {}
        industry_distribution = {}
        
        for case in cases:
            type_distribution[case.risk_type.value] = type_distribution.get(case.risk_type.value, 0) + 1
            level_distribution[case.risk_level.value] = level_distribution.get(case.risk_level.value, 0) + 1
            industry_distribution[case.industry] = industry_distribution.get(case.industry, 0) + 1
        
        return {
            "total_cases": len(cases),
            "type_distribution": type_distribution,
            "level_distribution": level_distribution,
            "industry_distribution": industry_distribution,
            "cases": [
                {
                    "case_id": c.case_id,
                    "title": c.title,
                    "risk_type": c.risk_type.value,
                    "risk_level": c.risk_level.value,
                    "industry": c.industry,
                    "case_date": c.case_date.isoformat()
                }
                for c in cases
            ]
        }
    
    def get_statistics(self) -> Dict:
        """get案例统计"""
        return {
            "total_cases": len(self.cases),
            "by_type": {
                risk_type.value: len(self.get_cases_by_type(risk_type))
                for risk_type in RiskType
            },
            "by_level": {
                risk_level.value: len(self.get_cases_by_level(risk_level))
                for risk_level in RiskLevel
            },
            "industries": list(set(c.industry for c in self.cases if c.industry))
        }
