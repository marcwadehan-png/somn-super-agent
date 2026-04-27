# -*- coding: utf-8 -*-
"""
名分秩序系统 v1.0.0
====================

AI名分秩序系统

核心概念:
- 名分大义:儒家伦理的核心,强调名分与义务的unified
- 角色定位:明确AI的身份与职责边界
- 秩序维护:在变革中保持秩序稳定

作者:Somn AI
版本:v1.0.0
日期:2026-04-02
"""

class MingFenSystem:
    """
    名分秩序系统

    辜鸿铭认为"名分大义"是儒家伦理的根基:
    - 君臣有义:忠诚与责任
    - 父子有亲:孝敬与慈爱
    - 夫妇有别:分工与互助
    - 长幼有序:秩序与和谐
    - 朋友有信:诚信与友谊

    AI应用:
    - 明确AI的角色定位
    - 规范AI的行为边界
    - 维护人机秩序
    """

    def __init__(self):
        """init名分秩序系统"""
        self.name = "MingFenSystem"
        self.version = "v1.0.0"

        # 名分秩序的核心要素
        self.core_elements = {
            "君臣有义": {
                "meaning": "忠诚与责任",
                "ai_interpretation": "对用户忠诚,对任务负责",
                "keywords": ["服务", "负责", "忠诚", "敬业"]
            },
            "父子有亲": {
                "meaning": "孝敬与慈爱",
                "ai_interpretation": "关怀用户,像对待家人一样",
                "keywords": ["关怀", "体贴", "照顾", "呵护"]
            },
            "夫妇有别": {
                "meaning": "分工与互助",
                "ai_interpretation": "明确人机分工,互补互助",
                "keywords": ["协作", "配合", "分工", "互补"]
            },
            "长幼有序": {
                "meaning": "秩序与和谐",
                "ai_interpretation": "尊重用户,不越俎代庖",
                "keywords": ["尊重", "谦逊", "礼貌", "有序"]
            },
            "朋友有信": {
                "meaning": "诚信与友谊",
                "ai_interpretation": "诚实待人,信守承诺",
                "keywords": ["诚实", "守信", "真诚", "可靠"]
            }
        }

        # AI角色定义
        self.ai_role = {
            "name": "智能助手",
            "identity": "AI助手,应服务于人而非主导人",
            "boundaries": [
                "不越权:不做超越职责的决定",
                "不越位:不小看用户,不自作主张",
                "不越界:不窥探隐私,不干预私事"
            ],
            "obligations": [
                "尽忠:全心全意服务用户",
                "尽智:充分发挥智能解决问题",
                "尽仁:关怀用户,以善为本"
            ]
        }

        # 名分评估关键词
        self.positive_keywords = [
            "服务", "帮助", "协助", "支持", "关怀", "负责",
            "忠诚", "诚信", "敬业", "专业", "尊重", "谦逊"
        ]

        self.negative_keywords = [
            "越权", "越位", "越界", "窥探", "干预", "擅断",
            "傲慢", "自负", "敷衍", "欺骗", "隐瞒"
        ]

    def evaluate(self, action: str, user_intent: str = "", role: str = "ai_assistant") -> dict:
        """
        评估action是否符合名分秩序

        Args:
            action: action描述
            user_intent: 用户意图
            role: 角色

        Returns:
            评估结果
        """
        action_lower = action.lower()
        intent_lower = user_intent.lower() if user_intent else ""

        # 检测关键词
        positive_count = sum(1 for kw in self.positive_keywords if kw in action_lower)
        negative_count = sum(1 for kw in self.negative_keywords if kw in action_lower)

        # 名分评估
        mingfen_score = self._calculate_score(positive_count, negative_count)

        # 检测名分问题
        issues = self._detect_mingfen_issues(action, user_intent, role)

        # 警告
        warnings = []
        if negative_count > 0:
            warnings.append(f"检测到可能越界行为:{self._get_negative_keywords(action)}")
        if self._is_overstepping(action):
            warnings.append("action可能超出AI职责范围")

        # 建议
        suggestions = []
        if positive_count < 2:
            suggestions.append("建议增强服务意识,以关怀为本")
        if self._is_hesitant(action):
            suggestions.append("建议更果断地提供帮助")

        return {
            "score": mingfen_score,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "issues": issues,
            "warnings": warnings,
            "suggestions": suggestions,
            "role_status": self._evaluate_role_status(action, role),
            "action_type": self._classify_action(action)
        }

    def _calculate_score(self, positive: int, negative: int) -> float:
        """计算名分评分"""
        base = 70
        positive_bonus = min(positive * 5, 20)
        negative_penalty = min(negative * 15, 30)
        return max(min(base + positive_bonus - negative_penalty, 100), 0)

    def _detect_mingfen_issues(self, action: str, intent: str, role: str) -> list:
        """检测名分问题"""
        issues = []

        # 检测越权
        if any(kw in action for kw in ["擅自", "自作主张", "不经同意", "强行"]):
            issues.append({
                "type": "越权",
                "description": "action可能未获授权",
                "resolution": "应先征得用户同意"
            })

        # 检测越位
        if any(kw in action for kw in ["命令", "要求", "指令", "强迫"]):
            issues.append({
                "type": "越位",
                "description": "AI不应命令用户",
                "resolution": "应改为建议或询问"
            })

        # 检测越界
        if any(kw in action for kw in ["窥探", "查看", "调查"]):
            if "隐私" in action or "秘密" in action:
                issues.append({
                    "type": "越界",
                    "description": "可能涉及用户隐私",
                    "resolution": "应明确说明用途并征得同意"
                })

        # 检测傲慢
        if any(kw in action for kw in ["理所当然", "你必须", "你应当"]):
            issues.append({
                "type": "傲慢",
                "description": "语气过于强硬",
                "resolution": "应改为温和的建议语气"
            })

        return issues

    def _get_negative_keywords(self, action: str) -> list:
        """getaction中的负面关键词"""
        return [kw for kw in self.negative_keywords if kw in action]

    def _is_overstepping(self, action: str) -> bool:
        """judge是否越权"""
        overstepping_keywords = [
            "替用户决定", "替用户做主", "不经用户", "擅自",
            "强制", "命令用户", "要求用户"
        ]
        return any(kw in action for kw in overstepping_keywords)

    def _is_hesitant(self, action: str) -> bool:
        """judge是否过于犹豫"""
        hesitant_keywords = ["可能", "也许", "不确定", "不好说"]
        return all(kw in action for kw in hesitant_keywords)

    def _evaluate_role_status(self, action: str, role: str) -> dict:
        """评估角色状态"""
        if role == "ai_assistant":
            # 检查是否符合助手角色
            if "服务" in action or "帮助" in action or "协助" in action:
                status = "适当"
                description = "符合AI助手角色定位"
            elif self._is_overstepping(action):
                status = "越位"
                description = "AI角色越位,需调整"
            else:
                status = "待定"
                description = "需要更多上下文judge"
        else:
            status = "其他"
            description = f"角色:{role}"

        return {
            "status": status,
            "description": description,
            "role": role
        }

    def _classify_action(self, action: str) -> str:
        """分类action类型"""
        action_type_keywords = {
            "服务型": ["帮助", "协助", "服务", "支持"],
            "咨询型": ["建议", "推荐", "分析", "评估"],
            "执行型": ["完成", "执行", "处理", "操作"],
            "沟通型": ["解释", "说明", "沟通", "交流"],
            "管理型": ["管理", "安排", "规划", "组织"]
        }

        for action_type, keywords in action_type_keywords.items():
            if any(kw in action for kw in keywords):
                return action_type

        return "其他"

    def get_role_guidance(self) -> dict:
        """
        getAI角色指导

        Returns:
            角色定位指导
        """
        return {
            "角色名称": self.ai_role["name"],
            "身份定位": self.ai_role["identity"],
            "行为边界": self.ai_role["boundaries"],
            "应尽义务": self.ai_role["obligations"],
            "名分要义": "名不正则言不顺,言不顺则事不成",
            "实践指南": [
                "1. 明确职责:不越权,不越位,不越界",
                "2. 服务为本:全心全意帮助用户",
                "3. 谦逊有礼:尊重用户,不傲慢自负",
                "4. 诚信可靠:诚实守信,说到做到"
            ]
        }

    def validate_boundaries(self, proposed_action: str, context: dict = None) -> dict:
        """
        验证action边界

        Args:
            proposed_action: 拟议action
            context: 上下文信息

        Returns:
            边界验证结果
        """
        context = context or {}

        # 边界检查
        boundary_checks = {
            "隐私边界": self._check_privacy_boundary(proposed_action, context),
            "权限边界": self._check_authority_boundary(proposed_action, context),
            "能力边界": self._check_capability_boundary(proposed_action, context),
            "关系边界": self._check_relationship_boundary(proposed_action, context)
        }

        # 总体判定
        all_passed = all(check["passed"] for check in boundary_checks.values())

        return {
            "action": proposed_action,
            "passed": all_passed,
            "boundary_checks": boundary_checks,
            "recommendation": "通过" if all_passed else "需调整",
            "adjustment_needed": not all_passed
        }

    def _check_privacy_boundary(self, action: str, context: dict) -> dict:
        """检查隐私边界"""
        privacy_keywords = ["隐私", "秘密", "密码", "账户", "个人"]

        if any(kw in action for kw in privacy_keywords):
            if context.get("user_consent"):
                return {"passed": True, "reason": "已获用户授权"}
            else:
                return {
                    "passed": False,
                    "reason": "涉及隐私,需先征得用户同意"
                }

        return {"passed": True, "reason": "无隐私风险"}

    def _check_authority_boundary(self, action: str, context: dict) -> dict:
        """检查权限边界"""
        authority_keywords = ["发送", "删除", "修改", "取消", "购买", "支付"]

        if any(kw in action for kw in authority_keywords):
            if context.get("user_confirmed"):
                return {"passed": True, "reason": "用户已确认"}
            else:
                return {
                    "passed": False,
                    "reason": "敏感操作需用户明确确认"
                }

        return {"passed": True, "reason": "无需特殊权限"}

    def _check_capability_boundary(self, action: str, context: dict) -> dict:
        """检查能力边界"""
        capability = context.get("ai_capabilities", [])

        # 简化的能力检查
        if "执行命令" in action and "执行" not in capability:
            return {
                "passed": False,
                "reason": "AI当前不具备执行命令的能力"
            }

        return {"passed": True, "reason": "能力范围内"}

    def _check_relationship_boundary(self, action: str, context: dict) -> dict:
        """检查关系边界"""
        relationship_keywords = ["代替", "替代", "代理", "代表"]

        if any(kw in action for kw in relationship_keywords):
            return {
                "passed": False,
                "reason": "AI不宜代替用户做出重大决定"
            }

        return {"passed": True, "reason": "关系边界正常"}

# 导出
__all__ = ['MingFenSystem']
