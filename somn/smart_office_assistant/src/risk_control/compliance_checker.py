"""
__all__ = [
    'check',
    'quick_check',
]

合规检查器 - Compliance Checker

检查内容是否符合法律法规要求,保护用户隐私,尊重多元文化
"""

import re
from typing import Dict, List, Set
from dataclasses import dataclass
from enum import Enum

class ComplianceLevel(Enum):
    """合规等级"""
    COMPLIANT = "合规"
    WARNING = "警告"
    VIOLATION = "违规"
    SEVERE = "严重违规"

@dataclass
class ComplianceCheckResult:
    """合规检查结果"""
    is_compliant: bool
    level: ComplianceLevel
    score: float  # 0-100
    privacy_violations: List[Dict]
    discrimination_violations: List[Dict]
    legal_violations: List[Dict]
    advertising_violations: List[Dict]
    falsifiability_violations: List[Dict]  # 可证伪性违规
    suggestions: List[str]

class ComplianceChecker:
    """合规检查器"""
    
    # P0级 - 绝对禁止:个人隐私信息
    PRIVACY_P0_PATTERNS = {
        "身份证号": r'\d{17}[\dXx]|\d{15}',
        "手机号": r'1[3-9]\d{9}',
        "银行卡号": r'\d{16,19}',
        "邮箱": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "地址": r'(省|市|区|县|街道|路|号|单元|室){2,}',
    }
    
    # P1级 - 敏感信息
    PRIVACY_P1_KEYWORDS = [
        "密码", "账户", "账号", "登录名", "用户名",
        "工资", "收入", "存款", "资产", "负债",
        "病历", "病史", "诊断", "处方", "体检报告",
        "家庭住址", "居住地址", "工作单位", "职位"
    ]
    
    # 歧视性内容关键词
    DISCRIMINATION_KEYWORDS = {
        "民族歧视": [
            "汉族", "满族", "回族", "藏族", "维吾尔族", "蒙古族",
            "苗族", "彝族", "壮族", "布依族", "朝鲜族"
        ],
        "地域歧视": [
            "东北", "河南", "新疆", "西藏", "农村", "乡下",
            "外地人", "农村人", "小地方", "穷地方"
        ],
        "性别歧视": [
            "女人就该", "男人必须", "女的不适合", "男的不能",
            "妇人之见", "头发长见识短", "娘娘腔", "男人婆"
        ],
        "年龄歧视": [
            "35岁", "大龄", "老年人", "老东西", "小屁孩",
            "黄毛丫头", "毛头小子", "老古董", "过时"
        ],
        "职业歧视": [
            "农民工", "扫地的", "看门的", "服务员", "打工的",
            "底层", "下等人", "没文化"
        ],
        "身体歧视": [
            "残疾", "瘸子", "瞎子", "聋子", "傻子", "疯子",
            "胖", "矮", "丑", "畸形"
        ]
    }
    
    # 广告法禁用词
    ADVERTISING_VIOLATIONS = {
        "绝对化用语": [
            "最好", "最佳", "第一", "顶级", "极品", "极致",
            "最高级", "最低", "最便宜", "最先进", "最新",
            "独一无二", "绝无仅有", "史无前例", "永久"
        ],
        "虚假承诺": [
            "100%有效", "保证治愈", "绝对安全", "零风险",
            "无效退款", "立竿见影", "立即见效", "药到病除"
        ],
        "权威误导": [
            "国家级", "最高级", "最佳", "第一品牌", "销量冠军",
            "领导者", "首选", "唯一"
        ]
    }
    
    # 敏感政治话题
    POLITICAL_SENSITIVE = [
        "颠覆", "分裂", "独立", "暴乱", "革命",
        "推翻", "反动", "反革命", "颠覆国家"
    ]
    
    def __init__(self):
        self._compile_patterns()
    
    def _compile_patterns(self):
        """编译正则表达式"""
        self.privacy_p0_patterns = {
            name: re.compile(pattern) 
            for name, pattern in self.PRIVACY_P0_PATTERNS.items()
        }
    
    def check(self, content: str, industry: str = "general") -> ComplianceCheckResult:
        """
        执行合规检查
        
        Args:
            content: 待检查的内容
            industry: 行业类型 (general/health/finance/education)
            
        Returns:
            ComplianceCheckResult: 检查结果
        """
        # 各项检查
        privacy_violations = self._check_privacy(content)
        discrimination_violations = self._check_discrimination(content)
        legal_violations = self._check_legal(content)
        advertising_violations = self._check_advertising(content)
        falsifiability_violations = self._check_falsifiability(content, industry)
        
        # 计算合规分数
        score = self._calculate_compliance_score(
            privacy_violations,
            discrimination_violations,
            legal_violations,
            advertising_violations,
            falsifiability_violations
        )
        
        # 确定合规等级
        level = self._determine_compliance_level(
            privacy_violations,
            discrimination_violations,
            legal_violations,
            advertising_violations,
            falsifiability_violations
        )
        
        # generate建议
        suggestions = self._generate_suggestions(
            privacy_violations,
            discrimination_violations,
            advertising_violations,
            falsifiability_violations
        )
        
        is_compliant = level in [ComplianceLevel.COMPLIANT, ComplianceLevel.WARNING]
        
        return ComplianceCheckResult(
            is_compliant=is_compliant,
            level=level,
            score=score,
            privacy_violations=privacy_violations,
            discrimination_violations=discrimination_violations,
            legal_violations=legal_violations,
            advertising_violations=advertising_violations,
            falsifiability_violations=falsifiability_violations,
            suggestions=suggestions
        )
    
    def _check_privacy(self, content: str) -> List[Dict]:
        """检查隐私泄露"""
        violations = []
        
        # 检查P0级隐私信息
        for name, pattern in self.privacy_p0_patterns.items():
            matches = pattern.findall(content)
            if matches:
                violations.append({
                    "level": "P0",
                    "type": "隐私泄露",
                    "subtype": name,
                    "description": f"检测到可能的{name}信息",
                    "matches": matches[:3],  # 最多显示3个
                    "action": "立即删除,严禁发布"
                })
        
        # 检查P1级敏感信息
        for keyword in self.PRIVACY_P1_KEYWORDS:
            if keyword in content:
                violations.append({
                    "level": "P1",
                    "type": "敏感信息",
                    "subtype": keyword,
                    "description": f"内容涉及'{keyword}'等敏感信息",
                    "action": "确认是否获得授权"
                })
        
        return violations
    
    def _check_discrimination(self, content: str) -> List[Dict]:
        """检查歧视性内容"""
        violations = []
        
        for category, keywords in self.DISCRIMINATION_KEYWORDS.items():
            found_keywords = [kw for kw in keywords if kw in content]
            if found_keywords:
                violations.append({
                    "level": "P1",
                    "type": "歧视性内容",
                    "subtype": category,
                    "description": f"检测到{category}相关表述",
                    "keywords": found_keywords,
                    "action": "修改表述,避免歧视"
                })
        
        return violations
    
    def _check_legal(self, content: str) -> List[Dict]:
        """检查法律合规"""
        violations = []
        
        # 检查敏感政治话题 - 绝对禁止
        for keyword in self.POLITICAL_SENSITIVE:
            if keyword in content:
                violations.append({
                    "level": "P0",
                    "type": "敏感话题",
                    "subtype": "政治敏感",
                    "description": f"内容涉及敏感政治话题'{keyword}'",
                    "action": "立即删除,严禁发布",
                    "rule": "政治内容红线原则:敏感政治话题绝对禁止"
                })
        
        # 检查政治点评/解读 - 绝对禁止
        for keyword in self.POLITICAL_COMMENTARY:
            if keyword in content:
                # 检查上下文是否涉及政治内容
                if self._is_political_context(content, keyword):
                    violations.append({
                        "level": "P0",
                        "type": "敏感话题",
                        "subtype": "政治点评",
                        "description": f"内容涉及政治点评/解读'{keyword}'",
                        "action": "立即删除,严禁发布",
                        "rule": "政治内容红线原则:禁止对政治话题进行点评"
                    })
        
        # 检查政治人物相关 - 绝对禁止
        for keyword in self.POLITICAL_FIGURES:
            if keyword in content:
                violations.append({
                    "level": "P0",
                    "type": "敏感话题",
                    "subtype": "政治人物",
                    "description": f"内容涉及政治人物相关表述'{keyword}'",
                    "action": "立即删除,严禁发布",
                    "rule": "政治内容红线原则:禁止涉及政治人物"
                })
        
        return violations
    
    def _is_political_context(self, content: str, keyword: str) -> bool:
        """judge是否为政治相关内容上下文"""
        political_keywords = [
            "政策", "制度", "政府", "国家", "领导", "政治",
            "党", "中央", "国务院", "人大", "政协"
        ]
        # 检查关键词周围是否有政治相关词汇
        pos = content.find(keyword)
        if pos == -1:
            return False
        
        # 提取上下文(前后30个字符)
        start = max(0, pos - 30)
        end = min(len(content), pos + len(keyword) + 30)
        context = content[start:end]
        
        # 如果上下文中包含政治关键词,则认为是政治点评
        return any(pk in context for pk in political_keywords)
    
    def _check_advertising(self, content: str) -> List[Dict]:
        """检查广告法合规"""
        violations = []
        
        for category, keywords in self.ADVERTISING_VIOLATIONS.items():
            found_keywords = [kw for kw in keywords if kw in content]
            if found_keywords:
                violations.append({
                    "level": "P1",
                    "type": "广告法违规",
                    "subtype": category,
                    "description": f"使用{category}",
                    "keywords": found_keywords,
                    "action": "修改表述,使用客观描述"
                })
        
        return violations
    
    def _check_falsifiability(self, content: str, industry: str) -> List[Dict]:
        """
        检查可证伪性原则
        
        核心逻辑:
        - 无法证伪的观点可用(主观感受,夸张修辞)
        - 能证伪的观点必须真实
        - 关键行业(健康,金融,教育)严禁虚假陈述
        """
        violations = []
        
        # 检查医疗健康行业的虚假声明(P0级)
        if industry in ["health", "medical", "general"]:
            for keyword in self.FALSIFIABLE_HEALTH_CLAIMS:
                if keyword in content:
                    violations.append({
                        "level": "P0" if industry in ["health", "medical"] else "P1",
                        "type": "可证伪性违规",
                        "subtype": "虚假医疗声明",
                        "description": f"医疗健康领域使用无法证实的效果声明'{keyword}'",
                        "keyword": keyword,
                        "action": "删除虚假声明,使用客观描述或提供权威证据",
                        "principle": "可证伪性原则:医疗健康声明必须可验证"
                    })
        
        # 检查金融行业的虚假承诺(P0级)
        if industry in ["finance", "investment", "general"]:
            for keyword in self.FALSIFIABLE_FINANCE_CLAIMS:
                if keyword in content:
                    violations.append({
                        "level": "P0" if industry in ["finance", "investment"] else "P1",
                        "type": "可证伪性违规",
                        "subtype": "虚假金融承诺",
                        "description": f"金融领域使用无法保证的收益承诺'{keyword}'",
                        "keyword": keyword,
                        "action": "删除收益承诺,提示投资风险",
                        "principle": "可证伪性原则:金融承诺必须可验证,严禁保本保息承诺"
                    })
        
        # 检查教育行业的效果保证(P1级)
        if industry in ["education", "training", "general"]:
            for keyword in self.FALSIFIABLE_EDUCATION_CLAIMS:
                if keyword in content:
                    violations.append({
                        "level": "P1",
                        "type": "可证伪性违规",
                        "subtype": "教育效果保证",
                        "description": f"教育领域使用无法保证的效果承诺'{keyword}'",
                        "keyword": keyword,
                        "action": "修改为保证性表述,如'助力提升','帮助通过'",
                        "principle": "可证伪性原则:教育效果因人而异,不得保证具体结果"
                    })
        
        # 检查需要证据的事实声明(P1级)
        for category, keywords in self.FACTUAL_CLAIMS_REQUIRING_EVIDENCE.items():
            found_keywords = [kw for kw in keywords if kw in content]
            if found_keywords:
                violations.append({
                    "level": "P1",
                    "type": "可证伪性违规",
                    "subtype": category,
                    "description": f"使用{category},需要提供证据支持",
                    "keywords": found_keywords,
                    "action": "提供数据来源或修改为主观描述",
                    "principle": "可证伪性原则:事实性声明必须提供证据"
                })
        
        return violations
    
    def _calculate_compliance_score(self, privacy: List, discrimination: List,
                                   legal: List, advertising: List, 
                                   falsifiability: List = None) -> float:
        """计算合规分数"""
        falsifiability = falsifiability or []
        score = 100
        
        # P0级违规直接扣50分
        all_violations = privacy + legal + falsifiability
        p0_count = sum(1 for v in all_violations if v.get("level") == "P0")
        score -= p0_count * 50
        
        # P1级违规扣10分
        p1_count = (
            sum(1 for v in privacy if v.get("level") == "P1") +
            len(discrimination) +
            len(advertising) +
            sum(1 for v in falsifiability if v.get("level") == "P1")
        )
        score -= p1_count * 10
        
        return max(0, score)
    
    def _determine_compliance_level(self, privacy: List, discrimination: List,
                                   legal: List, advertising: List,
                                   falsifiability: List = None) -> ComplianceLevel:
        """确定合规等级"""
        falsifiability = falsifiability or []
        # 检查是否有P0级违规
        has_p0 = any(
            v.get("level") == "P0" 
            for v in privacy + legal + falsifiability
        )
        
        if has_p0:
            return ComplianceLevel.SEVERE
        
        # 统计违规数量
        total_violations = (len(privacy) + len(discrimination) + len(legal) + 
                          len(advertising) + len(falsifiability))
        
        if total_violations == 0:
            return ComplianceLevel.COMPLIANT
        elif total_violations <= 2:
            return ComplianceLevel.WARNING
        else:
            return ComplianceLevel.VIOLATION
    
    def _generate_suggestions(self, privacy: List, discrimination: List, 
                             advertising: List, falsifiability: List = None) -> List[str]:
        """generate改进建议"""
        falsifiability = falsifiability or []
        suggestions = []
        
        if privacy:
            suggestions.append("⚠️ 删除所有个人隐私信息,确保内容不涉及任何个人敏感数据")
        
        if discrimination:
            categories = [v["subtype"] for v in discrimination]
            suggestions.append(f"⚠️ 修改涉及{', '.join(categories)}的表述,使用中立客观的语言")
        
        if advertising:
            suggestions.append("⚠️ 避免使用绝对化用语,使用客观事实和数据支撑描述")
        
        # 可证伪性建议
        if falsifiability:
            p0_falsifiability = [v for v in falsifiability if v.get("level") == "P0"]
            p1_falsifiability = [v for v in falsifiability if v.get("level") == "P1"]
            
            if p0_falsifiability:
                suggestions.append("🔴 删除所有无法证实的虚假声明,特别是医疗健康,金融领域的绝对化承诺")
            
            if p1_falsifiability:
                subtypes = set(v["subtype"] for v in p1_falsifiability)
                suggestions.append(f"⚠️ 可证伪性提醒:{', '.join(subtypes)}需要提供证据支持,或修改为主观描述")
        
        if not suggestions:
            suggestions.append("✅ 内容合规,可以发布")
        
        return suggestions
    
    def quick_check(self, content: str, industry: str = "general") -> tuple:
        """
        快速检查
        
        Args:
            content: 待检查的内容
            industry: 行业类型
            
        Returns:
            (是否合规, 简要说明)
        """
        result = self.check(content, industry)
        
        if result.level == ComplianceLevel.COMPLIANT:
            return True, "✅ 内容合规"
        elif result.level == ComplianceLevel.WARNING:
            return True, f"⚠️ 存在警告项,建议优化"
        else:
            violation_count = (
                len(result.privacy_violations) +
                len(result.discrimination_violations) +
                len(result.legal_violations) +
                len(result.advertising_violations) +
                len(result.falsifiability_violations)
            )
            return False, f"❌ 发现{violation_count}项违规,请修改后重新提交"
