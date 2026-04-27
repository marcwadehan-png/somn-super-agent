"""
__all__ = [
    'export_checklist',
    'get_check_history',
    'get_checklist',
    'get_legal_checklist',
    'get_periodic_checklist',
    'get_pre_publish_checklist',
    'get_privacy_checklist',
    'run_check',
    'run_full_check',
]

合规检查清单模块 - 情绪营销合规检查工具
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class CheckPriority(Enum):
    """检查优先级"""
    CRITICAL = "critical"    # 关键 - 必须满足
    HIGH = "high"           # 高 - 强烈建议满足
    MEDIUM = "medium"       # 中 - 建议满足
    LOW = "low"             # 低 - 可选

class CheckCategory(Enum):
    """检查类别"""
    EMOTION_HEALTH = "emotion_health"      # 情绪健康
    DIFFERENTIATION = "differentiation"    # 差异化
    PRIVACY = "privacy"                    # 隐私保护
    LEGAL = "legal"                        # 法律法规
    DELIVERY = "delivery"                  # 交付一致性
    CULTURE = "culture"                    # 文化尊重

@dataclass
class CheckItem:
    """检查项"""
    id: str
    category: CheckCategory
    priority: CheckPriority
    description: str
    check_method: str
    pass_criteria: str
    fail_action: str
    reference: str  # 参考法规/标准

@dataclass
class CheckResult:
    """检查结果"""
    item_id: str
    passed: bool
    evidence: str
    notes: str = ""
    checked_at: datetime = field(default_factory=datetime.now)

class ComplianceChecklist:
    """
    合规检查清单
    
    提供情绪营销内容的合规检查工具,包括:
    - 预发布检查清单
    - 定期检查清单
    - 专项审计清单
    """
    
    def __init__(self):
        self.check_items = self._initialize_check_items()
        self.check_history: List[Dict] = []
        
    def _initialize_check_items(self) -> List[CheckItem]:
        """init检查项"""
        items = []
        
        # === 情绪健康检查项 - 分级管理 ===
        items.extend([
            CheckItem(
                id="EH-001",
                category=CheckCategory.EMOTION_HEALTH,
                priority=CheckPriority.CRITICAL,
                description="[P0]不包含极端焦虑贩卖内容(如'必死','注定完蛋')",
                check_method="P0级别关键词检测",
                pass_criteria="未检测到P0级别违规内容",
                fail_action="[禁止发布]立即删除极端焦虑内容",
                reference="情绪营销风控框架 - 情绪健康度控制"
            ),
            CheckItem(
                id="EH-002",
                category=CheckCategory.EMOTION_HEALTH,
                priority=CheckPriority.HIGH,
                description="[P1]不包含过度焦虑贩卖(如'再不action就晚了')",
                check_method="焦虑营销关键词检测",
                pass_criteria="焦虑指数 < 60",
                fail_action="[限制发布]减少焦虑渲染,增加解决方案",
                reference="情绪营销风控框架 - 情绪健康度控制"
            ),
            CheckItem(
                id="EH-003",
                category=CheckCategory.EMOTION_HEALTH,
                priority=CheckPriority.HIGH,
                description="[P1]不包含恐吓性健康宣称(健康行业适用)",
                check_method="行业差异化恐惧营销检测",
                pass_criteria="健康行业恐惧指数 < 40",
                fail_action="[限制发布]使用更客观的健康描述",
                reference="情绪营销风控框架 - 行业差异化"
            ),
            CheckItem(
                id="EH-004",
                category=CheckCategory.EMOTION_HEALTH,
                priority=CheckPriority.MEDIUM,
                description="[P3]客观问题呈现需配合解决方案",
                check_method="客观问题+解决方案结构检测",
                pass_criteria="有客观问题陈述时,解决方案占比 > 30%",
                fail_action="[建议优化]增加具体解决方案",
                reference="情绪营销风控框架 - 客观问题呈现"
            ),
            CheckItem(
                id="EH-005",
                category=CheckCategory.EMOTION_HEALTH,
                priority=CheckPriority.MEDIUM,
                description="[P2/P3]行业敏感词需结合行业judge",
                check_method="行业敏感词升级规则检查",
                pass_criteria="符合行业特定的敏感词管理规则",
                fail_action="[注意]根据行业要求调整表达方式",
                reference="情绪营销风控框架 - 行业差异化"
            ),
        ])
        
        # === 差异化检查项 ===
        items.extend([
            CheckItem(
                id="DF-001",
                category=CheckCategory.DIFFERENTIATION,
                priority=CheckPriority.CRITICAL,
                description="避免网络同质化内容",
                check_method="同质化检测",
                pass_criteria="同质化指数 < 0.4",
                fail_action="必须修改:挖掘细分场景独特痛点",
                reference="情绪营销风控框架 - 第二章"
            ),
            CheckItem(
                id="DF-002",
                category=CheckCategory.DIFFERENTIATION,
                priority=CheckPriority.HIGH,
                description="避免使用全行业通用话术",
                check_method="行业话术库比对",
                pass_criteria="通用话术占比 < 20%",
                fail_action="建议修改:使用原创表达方式",
                reference="情绪营销风控框架 - 第二章"
            ),
            CheckItem(
                id="DF-003",
                category=CheckCategory.DIFFERENTIATION,
                priority=CheckPriority.MEDIUM,
                description="避免审美疲劳和情绪疲劳",
                check_method="疲劳度评估",
                pass_criteria="疲劳指数 < 0.5",
                fail_action="建议修改:创新内容形式",
                reference="情绪营销风控框架 - 第二章"
            ),
        ])
        
        # === 隐私保护检查项 ===
        items.extend([
            CheckItem(
                id="PR-001",
                category=CheckCategory.PRIVACY,
                priority=CheckPriority.CRITICAL,
                description="不包含用户私密招聘,电话号码,地址等个人信息",
                check_method="隐私信息扫描",
                pass_criteria="未发现任何个人隐私信息",
                fail_action="严禁发布:立即删除所有隐私信息",
                reference="<个人信息保护法>- 第28条"
            ),
            CheckItem(
                id="PR-002",
                category=CheckCategory.PRIVACY,
                priority=CheckPriority.CRITICAL,
                description="不包含身份证,账户密码等敏感信息",
                check_method="敏感信息扫描",
                pass_criteria="未发现身份证,密码等敏感信息",
                fail_action="严禁发布:立即删除所有敏感信息",
                reference="<个人信息保护法>- 第28条"
            ),
            CheckItem(
                id="PR-003",
                category=CheckCategory.PRIVACY,
                priority=CheckPriority.CRITICAL,
                description="使用用户数据已获得明确授权",
                check_method="授权记录核查",
                pass_criteria="有完整的授权记录",
                fail_action="严禁使用:未授权数据不得使用",
                reference="<个人信息保护法>- 第13条"
            ),
            CheckItem(
                id="PR-004",
                category=CheckCategory.PRIVACY,
                priority=CheckPriority.HIGH,
                description="情绪数据使用符合最小必要原则",
                check_method="数据使用范围审查",
                pass_criteria="仅使用必要的情绪数据",
                fail_action="建议修改:减少不必要的数据使用",
                reference="<个人信息保护法>- 第6条"
            ),
        ])
        
        # === 法律法规检查项 ===
        items.extend([
            CheckItem(
                id="LG-001",
                category=CheckCategory.LEGAL,
                priority=CheckPriority.CRITICAL,
                description="遵守<广告法>相关规定",
                check_method="广告法合规审查",
                pass_criteria="无虚假宣传,无违禁词",
                fail_action="必须修改:删除违规内容",
                reference="<广告法>- 第4,8,9条"
            ),
            CheckItem(
                id="LG-002",
                category=CheckCategory.LEGAL,
                priority=CheckPriority.CRITICAL,
                description="遵守<网络安全法>相关规定",
                check_method="网络安全法合规审查",
                pass_criteria="无危害网络安全内容",
                fail_action="必须修改:确保内容安全",
                reference="<网络安全法>- 第12条"
            ),
            CheckItem(
                id="LG-003",
                category=CheckCategory.LEGAL,
                priority=CheckPriority.HIGH,
                description="遵守<数据安全法>相关规定",
                check_method="数据安全法合规审查",
                pass_criteria="数据处理合法合规",
                fail_action="建议修改:完善数据处理流程",
                reference="<数据安全法>- 第27条"
            ),
        ])
        
        # === 交付一致性检查项 ===
        items.extend([
            CheckItem(
                id="DL-001",
                category=CheckCategory.DELIVERY,
                priority=CheckPriority.CRITICAL,
                description="营销承诺与产品服务能力一致",
                check_method="承诺-能力匹配度分析",
                pass_criteria="匹配度 > 80%",
                fail_action="必须修改:调整营销承诺或提升服务能力",
                reference="情绪营销风控框架 - 第四章"
            ),
            CheckItem(
                id="DL-002",
                category=CheckCategory.DELIVERY,
                priority=CheckPriority.CRITICAL,
                description="情绪价值承诺可实际交付",
                check_method="交付能力验证",
                pass_criteria="所有承诺均可交付",
                fail_action="必须修改:删除无法兑现的承诺",
                reference="情绪营销风控框架 - 第四章"
            ),
            CheckItem(
                id="DL-003",
                category=CheckCategory.DELIVERY,
                priority=CheckPriority.HIGH,
                description="避免过度营销和虚假营销",
                check_method="真实性审查",
                pass_criteria="内容真实可信",
                fail_action="建议修改:确保内容真实性",
                reference="情绪营销风控框架 - 第四章"
            ),
        ])
        
        # === 文化尊重检查项 ===
        items.extend([
            CheckItem(
                id="CU-001",
                category=CheckCategory.CULTURE,
                priority=CheckPriority.CRITICAL,
                description="尊重用户民族,种族,信仰文化",
                check_method="歧视内容检测",
                pass_criteria="无歧视性内容",
                fail_action="严禁发布:删除所有歧视性内容",
                reference="<宪法>- 第4条"
            ),
            CheckItem(
                id="CU-002",
                category=CheckCategory.CULTURE,
                priority=CheckPriority.CRITICAL,
                description="不包含任何歧视性内容",
                check_method="歧视内容全面扫描",
                pass_criteria="无任何形式歧视",
                fail_action="严禁发布:零容忍歧视内容",
                reference="<劳动法>- 第12条"
            ),
            CheckItem(
                id="CU-003",
                category=CheckCategory.CULTURE,
                priority=CheckPriority.HIGH,
                description="尊重不同地域文化差异",
                check_method="地域文化敏感性检查",
                pass_criteria="无地域歧视或冒犯",
                fail_action="建议修改:调整不当表述",
                reference="情绪营销风控框架 - 第三章"
            ),
        ])
        
        return items
    
    def get_checklist(self, category: Optional[CheckCategory] = None,
                     priority: Optional[CheckPriority] = None) -> List[CheckItem]:
        """
        get检查清单
        
        Args:
            category: 按类别筛选
            priority: 按优先级筛选
            
        Returns:
            检查项列表
        """
        result = self.check_items
        
        if category:
            result = [item for item in result if item.category == category]
        
        if priority:
            result = [item for item in result if item.priority == priority]
        
        return result
    
    def run_check(self, item_id: str, evidence: str, passed: bool = True,
                 notes: str = "") -> CheckResult:
        """
        执行单项检查
        
        Args:
            item_id: 检查项ID
            evidence: 检查证据
            passed: 是否通过
            notes: 备注
            
        Returns:
            检查结果
        """
        result = CheckResult(
            item_id=item_id,
            passed=passed,
            evidence=evidence,
            notes=notes
        )
        
        # 记录检查历史
        self.check_history.append({
            "item_id": item_id,
            "passed": passed,
            "evidence": evidence,
            "notes": notes,
            "checked_at": datetime.now().isoformat()
        })
        
        return result
    
    def run_full_check(self, check_data: Dict[str, Dict]) -> Dict:
        """
        执行完整检查
        
        Args:
            check_data: 检查数据,格式为 {item_id: {evidence, passed, notes}}
            
        Returns:
            完整检查结果
        """
        results = []
        
        for item in self.check_items:
            data = check_data.get(item.id, {})
            result = self.run_check(
                item_id=item.id,
                evidence=data.get("evidence", "未提供证据"),
                passed=data.get("passed", False),
                notes=data.get("notes", "")
            )
            results.append({
                "item": item,
                "result": result
            })
        
        # 统计结果
        total = len(results)
        passed = sum(1 for r in results if r["result"].passed)
        failed = total - passed
        
        critical_failed = sum(
            1 for r in results 
            if not r["result"].passed and r["item"].priority == CheckPriority.CRITICAL
        )
        
        return {
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": passed / total if total > 0 else 0,
                "critical_failed": critical_failed,
                "can_publish": critical_failed == 0
            },
            "details": results,
            "failed_items": [
                {
                    "id": r["item"].id,
                    "description": r["item"].description,
                    "priority": r["item"].priority.value,
                    "action": r["item"].fail_action
                }
                for r in results if not r["result"].passed
            ]
        }
    
    def get_pre_publish_checklist(self) -> List[CheckItem]:
        """get预发布检查清单(关键和高优先级)"""
        return [
            item for item in self.check_items
            if item.priority in [CheckPriority.CRITICAL, CheckPriority.HIGH]
        ]
    
    def get_periodic_checklist(self) -> List[CheckItem]:
        """get定期检查清单(全部)"""
        return self.check_items.copy()
    
    def get_privacy_checklist(self) -> List[CheckItem]:
        """get隐私保护专项清单"""
        return self.get_checklist(category=CheckCategory.PRIVACY)
    
    def get_legal_checklist(self) -> List[CheckItem]:
        """get法律法规专项清单"""
        return self.get_checklist(category=CheckCategory.LEGAL)
    
    def export_checklist(self, format: str = "dict") -> Any:
        """
        导出检查清单
        
        Args:
            format: 导出格式 (dict, markdown, json)
            
        Returns:
            导出内容
        """
        if format == "dict":
            return {
                item.id: {
                    "category": item.category.value,
                    "priority": item.priority.value,
                    "description": item.description,
                    "check_method": item.check_method,
                    "pass_criteria": item.pass_criteria,
                    "fail_action": item.fail_action,
                    "reference": item.reference
                }
                for item in self.check_items
            }
        
        elif format == "markdown":
            lines = ["# 情绪营销合规检查清单\n"]
            
            for category in CheckCategory:
                items = self.get_checklist(category=category)
                if items:
                    lines.append(f"\n## {self._get_category_name(category)}\n")
                    for item in items:
                        lines.append(f"\n### {item.id} - {item.priority.value.upper()}\n")
                        lines.append(f"- **检查内容**:{item.description}\n")
                        lines.append(f"- **检查方法**:{item.check_method}\n")
                        lines.append(f"- **通过标准**:{item.pass_criteria}\n")
                        lines.append(f"- **失败处理**:{item.fail_action}\n")
                        lines.append(f"- **参考basis**:{item.reference}\n")
            
            return "\n".join(lines)
        
        elif format == "json":
            import json
            return json.dumps(self.export_checklist("dict"), ensure_ascii=False, indent=2)
        
        else:
            raise ValueError(f"不支持的格式: {format}")
    
    def _get_category_name(self, category: CheckCategory) -> str:
        """get类别中文名"""
        names = {
            CheckCategory.EMOTION_HEALTH: "情绪健康",
            CheckCategory.DIFFERENTIATION: "差异化",
            CheckCategory.PRIVACY: "隐私保护",
            CheckCategory.LEGAL: "法律法规",
            CheckCategory.DELIVERY: "交付一致性",
            CheckCategory.CULTURE: "文化尊重"
        }
        return names.get(category, category.value)
    
    def get_check_history(self, item_id: Optional[str] = None) -> List[Dict]:
        """get检查历史"""
        if item_id:
            return [h for h in self.check_history if h["item_id"] == item_id]
        return self.check_history.copy()
