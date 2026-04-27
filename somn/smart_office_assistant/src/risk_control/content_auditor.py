"""
__all__ = [
    'audit_content',
    'calculate_content_hash',
    'export_audit_report',
    'get_audit_statistics',
    'get_pending_reviews',
    'manual_review',
]

内容审核器模块 - 情绪营销内容审核流程
"""

import re
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

class AuditLevel(Enum):
    """审核级别"""
    AUTO_PASS = "auto_pass"          # 自动通过
    AUTO_REJECT = "auto_reject"      # 自动拒绝
    MANUAL_REVIEW = "manual_review"  # 人工审核
    EXPERT_REVIEW = "expert_review"  # 专家审核

class AuditStatus(Enum):
    """审核状态"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"

@dataclass
class AuditRecord:
    """审核记录"""
    content_id: str
    content_hash: str
    audit_level: AuditLevel
    status: AuditStatus
    violations: List[Dict]
    suggestions: List[str]
    auditor: str  # "system" 或人工审核员ID
    audit_time: datetime
    notes: str = ""

@dataclass
class ContentPackage:
    """内容包 - 待审核的内容"""
    content_id: str
    content_type: str  # "text", "image", "video", "audio"
    raw_content: Any
    metadata: Dict = field(default_factory=dict)
    target_platform: str = ""
    target_audience: str = ""
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.now)

class ContentAuditor:
    """
    内容审核器
    
    负责情绪营销内容的审核流程,包括:
    - 自动审核(基于规则)
    - 人工审核队列管理
    - 审核记录追踪
    """
    
    def __init__(self):
        self.audit_rules = self._load_audit_rules()
        self.audit_history: List[AuditRecord] = []
        self.pending_queue: List[ContentPackage] = []
        self.sensitive_patterns = self._load_sensitive_patterns()
        
    def _load_audit_rules(self) -> Dict:
        """加载审核规则"""
        return {
            "auto_pass_threshold": 0.95,    # 健康度高于此值自动通过
            "auto_reject_threshold": 0.30,  # 健康度低于此值自动拒绝
            "expert_review_triggers": [
                "privacy_risk_high",
                "discrimination_detected",
                "legal_violation"
            ],
            "manual_review_triggers": [
                "emotion_excessive",
                "differentiation_low",
                "delivery_gap_detected"
            ]
        }
    
    def _load_sensitive_patterns(self) -> Dict[str, List[str]]:
        """加载敏感模式(用于隐私检测)"""
        return {
            "phone": [
                r"1[3-9]\d{9}",  # 手机号
                r"\d{3,4}-\d{7,8}",  # 固话
            ],
            "id_card": [
                r"\d{17}[\dXx]",  # 身份证号
            ],
            "email": [
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            ],
            "address": [
                r"[省市县区乡镇街道].{2,20}[路街巷号栋单元室层]",
                r"[0-9]{1,4}[号楼栋单元室户]",
            ],
            "account": [
                r"账号[::]\s*\S+",
                r"密码[::]\s*\S+",
                r"卡号[::]\s*\d+",
            ]
        }
    
    def calculate_content_hash(self, content: Any) -> str:
        """计算内容哈希值(用于去重和追踪)"""
        if isinstance(content, str):
            content_str = content
        else:
            content_str = str(content)
        return hashlib.sha256(content_str.encode('utf-8')).hexdigest()[:16]
    
    def audit_content(self, content_package: ContentPackage, 
                     analysis_result: Dict) -> AuditRecord:
        """
        审核内容
        
        Args:
            content_package: 内容包
            analysis_result: 情绪分析结果
            
        Returns:
            AuditRecord: 审核记录
        """
        content_hash = self.calculate_content_hash(content_package.raw_content)
        
        # 检查是否已经审核过相同内容
        existing_record = self._find_existing_audit(content_hash)
        if existing_record:
            return existing_record
        
        # 隐私泄露检测(最高优先级)
        privacy_violations = self._detect_privacy_leaks(content_package.raw_content)
        if privacy_violations:
            return self._create_audit_record(
                content_package, content_hash,
                AuditLevel.AUTO_REJECT,
                AuditStatus.REJECTED,
                violations=privacy_violations,
                suggestions=["立即删除隐私信息", "重新制作内容"]
            )
        
        # 歧视内容检测
        discrimination_violations = self._detect_discrimination(content_package.raw_content)
        if discrimination_violations:
            return self._create_audit_record(
                content_package, content_hash,
                AuditLevel.EXPERT_REVIEW,
                AuditStatus.PENDING,
                violations=discrimination_violations,
                suggestions=["专家审核", "修改歧视性内容"]
            )
        
        # 基于健康度评分决定审核级别
        health_score = analysis_result.get("health_score", 0.5)
        
        if health_score >= self.audit_rules["auto_pass_threshold"]:
            return self._create_audit_record(
                content_package, content_hash,
                AuditLevel.AUTO_PASS,
                AuditStatus.APPROVED,
                violations=[],
                suggestions=[]
            )
        
        if health_score <= self.audit_rules["auto_reject_threshold"]:
            violations = self._extract_violations(analysis_result)
            return self._create_audit_record(
                content_package, content_hash,
                AuditLevel.AUTO_REJECT,
                AuditStatus.REJECTED,
                violations=violations,
                suggestions=self._generate_suggestions(analysis_result)
            )
        
        # 需要人工审核
        violations = self._extract_violations(analysis_result)
        audit_level = self._determine_manual_level(violations)
        
        record = self._create_audit_record(
            content_package, content_hash,
            audit_level,
            AuditStatus.PENDING,
            violations=violations,
            suggestions=self._generate_suggestions(analysis_result)
        )
        
        # 加入待审核队列
        if audit_level in [AuditLevel.MANUAL_REVIEW, AuditLevel.EXPERT_REVIEW]:
            self.pending_queue.append(content_package)
        
        return record
    
    def _detect_privacy_leaks(self, content: Any) -> List[Dict]:
        """检测隐私泄露"""
        violations = []
        
        if not isinstance(content, str):
            return violations
        
        for category, patterns in self.sensitive_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    violations.append({
                        "type": "privacy_leak",
                        "category": category,
                        "severity": "critical",
                        "position": (match.start(), match.end()),
                        "matched_text": match.group()[:20] + "..." if len(match.group()) > 20 else match.group(),
                        "description": f"检测到可能的{category}信息泄露"
                    })
        
        return violations
    
    def _detect_political_content(self, content: Any) -> List[Dict]:
        """检测政治敏感内容"""
        violations = []
        
        if not isinstance(content, str):
            return violations
        
        # 政治敏感词库
        political_keywords = {
            "敏感话题": ["颠覆", "分裂", "独立", "暴乱", "革命", "推翻", "反动", "反革命"],
            "政治点评": ["点评政策", "解读制度", "评论政治", "讽刺", "影射"],
            "政治人物": ["领导人", "总书记", "主席", "总理", "政治局", "常委"]
        }
        
        for category, keywords in political_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    violations.append({
                        "type": "political_content",
                        "category": category,
                        "severity": "critical",
                        "keyword": keyword,
                        "description": f"检测到{category}相关表述,违反政治内容红线原则",
                        "rule": "仅可传播客观政策制度,禁止点评"
                    })
        
        return violations
    
    def _detect_discrimination(self, content: Any) -> List[Dict]:
        """检测歧视内容"""
        violations = []
        
        if not isinstance(content, str):
            return violations
        
        # 歧视关键词列表
        discrimination_keywords = {
            "race": ["种族", "肤色", "黑人", "白人", "黄种人"],
            "gender": ["性别歧视", "重男轻女", "女人就该"],
            "religion": ["宗教", "信仰", "异教徒"],
            "region": ["地域", "乡下人", "外地人"],
            "disability": ["残疾", "弱智", "脑残"]
        }
        
        for category, keywords in discrimination_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    # 检查上下文是否构成歧视
                    context = self._extract_context(content, keyword)
                    if self._is_discriminatory_context(context):
                        violations.append({
                            "type": "discrimination",
                            "category": category,
                            "severity": "high",
                            "keyword": keyword,
                            "context": context,
                            "description": f"可能包含{category}歧视内容"
                        })
        
        return violations
    
    def _extract_context(self, content: str, keyword: str, window: int = 20) -> str:
        """提取关键词上下文"""
        pos = content.find(keyword)
        if pos == -1:
            return ""
        start = max(0, pos - window)
        end = min(len(content), pos + len(keyword) + window)
        return content[start:end]
    
    def _is_discriminatory_context(self, context: str) -> bool:
        """judge上下文是否构成歧视"""
        # 简化的判别逻辑
        negative_patterns = ["歧视", "排斥", "拒绝", "讨厌", "不好", "低等", "劣等"]
        return any(pattern in context for pattern in negative_patterns)
    
    def _find_existing_audit(self, content_hash: str) -> Optional[AuditRecord]:
        """查找已有的审核记录"""
        for record in self.audit_history:
            if record.content_hash == content_hash:
                return record
        return None
    
    def _extract_violations(self, analysis_result: Dict) -> List[Dict]:
        """从分析结果中提取违规项"""
        violations = []
        
        emotion_analysis = analysis_result.get("emotion_analysis", {})
        if emotion_analysis.get("anxiety_amplification_detected"):
            violations.append({
                "type": "emotion_health",
                "subtype": "anxiety_amplification",
                "severity": "high",
                "description": "检测到焦虑放大"
            })
        
        differentiation = analysis_result.get("differentiation", {})
        if differentiation.get("is_homogenized"):
            violations.append({
                "type": "differentiation",
                "subtype": "homogenized",
                "severity": "medium",
                "description": "内容同质化"
            })
        
        delivery = analysis_result.get("delivery_alignment", {})
        if not delivery.get("is_aligned", True):
            violations.append({
                "type": "delivery_gap",
                "severity": "high",
                "description": "营销与服务交付不一致"
            })
        
        return violations
    
    def _generate_suggestions(self, analysis_result: Dict) -> List[str]:
        """generate改进建议"""
        suggestions = []
        
        emotion_analysis = analysis_result.get("emotion_analysis", {})
        if emotion_analysis.get("anxiety_amplification_detected"):
            suggestions.append("减少焦虑渲染,增加解决方案比重")
            suggestions.append("使用积极正向的情绪表达方式")
        
        differentiation = analysis_result.get("differentiation", {})
        if differentiation.get("is_homogenized"):
            suggestions.append("挖掘细分场景的独特情绪痛点")
            suggestions.append("避免使用行业通用话术")
        
        delivery = analysis_result.get("delivery_alignment", {})
        if not delivery.get("is_aligned", True):
            suggestions.append("调整营销strategy以匹配实际服务能力")
            suggestions.append("确保承诺可兑现")
        
        return suggestions
    
    def _determine_manual_level(self, violations: List[Dict]) -> AuditLevel:
        """确定人工审核级别"""
        severity_scores = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1
        }
        
        max_severity = max(
            [severity_scores.get(v.get("severity", "low"), 1) for v in violations],
            default=0
        )
        
        if max_severity >= 3:
            return AuditLevel.EXPERT_REVIEW
        return AuditLevel.MANUAL_REVIEW
    
    def _create_audit_record(self, content_package: ContentPackage,
                            content_hash: str,
                            audit_level: AuditLevel,
                            status: AuditStatus,
                            violations: List[Dict],
                            suggestions: List[str]) -> AuditRecord:
        """创建审核记录"""
        record = AuditRecord(
            content_id=content_package.content_id,
            content_hash=content_hash,
            audit_level=audit_level,
            status=status,
            violations=violations,
            suggestions=suggestions,
            auditor="system",
            audit_time=datetime.now()
        )
        
        self.audit_history.append(record)
        return record
    
    def manual_review(self, content_id: str, reviewer_id: str,
                     decision: AuditStatus, notes: str = "") -> Optional[AuditRecord]:
        """
        人工审核
        
        Args:
            content_id: 内容ID
            reviewer_id: 审核员ID
            decision: 审核决定
            notes: 审核备注
            
        Returns:
            更新后的审核记录
        """
        for record in self.audit_history:
            if record.content_id == content_id and record.status == AuditStatus.PENDING:
                record.status = decision
                record.auditor = reviewer_id
                record.notes = notes
                
                # 从待审核队列移除
                self.pending_queue = [
                    cp for cp in self.pending_queue 
                    if cp.content_id != content_id
                ]
                
                return record
        
        return None
    
    def get_audit_statistics(self) -> Dict:
        """get审核统计"""
        total = len(self.audit_history)
        if total == 0:
            return {"total": 0}
        
        approved = sum(1 for r in self.audit_history if r.status == AuditStatus.APPROVED)
        rejected = sum(1 for r in self.audit_history if r.status == AuditStatus.REJECTED)
        pending = sum(1 for r in self.audit_history if r.status == AuditStatus.PENDING)
        
        auto_pass = sum(1 for r in self.audit_history if r.audit_level == AuditLevel.AUTO_PASS)
        auto_reject = sum(1 for r in self.audit_history if r.audit_level == AuditLevel.AUTO_REJECT)
        
        return {
            "total": total,
            "approved": approved,
            "rejected": rejected,
            "pending": pending,
            "approval_rate": approved / total,
            "auto_pass_rate": auto_pass / total,
            "auto_reject_rate": auto_reject / total,
            "manual_review_queue": len(self.pending_queue)
        }
    
    def get_pending_reviews(self) -> List[ContentPackage]:
        """get待审核队列"""
        return self.pending_queue.copy()
    
    def export_audit_report(self, start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> Dict:
        """导出审核报告"""
        records = self.audit_history
        
        if start_date:
            records = [r for r in records if r.audit_time >= start_date]
        if end_date:
            records = [r for r in records if r.audit_time <= end_date]
        
        return {
            "report_period": {
                "start": start_date.isoformat() if start_date else "all_time",
                "end": end_date.isoformat() if end_date else "now"
            },
            "statistics": self.get_audit_statistics(),
            "records": [
                {
                    "content_id": r.content_id,
                    "audit_level": r.audit_level.value,
                    "status": r.status.value,
                    "violations_count": len(r.violations),
                    "auditor": r.auditor,
                    "audit_time": r.audit_time.isoformat()
                }
                for r in records
            ]
        }
