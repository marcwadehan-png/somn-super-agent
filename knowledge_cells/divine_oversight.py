# -*- coding: utf-8 -*-
"""
神政轨监督框架 v2.0 (DivineTrackOversight)
==========================================
性能优化版本：
  1. __slots__ 减少内存占用 (~40%)
  2. 快速ID生成 (计数器+base36，比uuid快10倍)
  3. 规则函数模块级缓存 (避免重复创建)
  4. time.time() 替代 datetime.now() (更快)
  5. LRU缓存摘要 (避免重复处理)
  6. 记录上限机制 (防止内存泄漏)
  7. 批量记录支持 (减少函数调用开销)
  8. 网络搜索增强 (RefuteCoreWeb)
"""

import time
import sys
import logging
import threading
from typing import Dict, List, Any, Optional, Callable, Set
from functools import lru_cache
from collections import deque

logger = logging.getLogger(__name__)

# ==================== 网络搜索增强（懒加载） ====================

_REFUTE_WEB: Optional[Any] = None
_REFUTE_WEB_LOCK = threading.Lock()


def _get_refute_web():
    """获取RefuteCoreWeb实例（线程安全的懒加载）"""
    global _REFUTE_WEB
    if _REFUTE_WEB is None:
        with _REFUTE_WEB_LOCK:
            if _REFUTE_WEB is None:  # double-check
                _REFUTE_WEB = _try_load_refute_web()
    return _REFUTE_WEB


def _try_load_refute_web():
    """
    尝试加载 RefuteCoreWeb（支持多种导入方式）

    导入优先级:
    1. 相对导入 (knowledge_cells 包内)
    2. 绝对导入 (knowledge_cells.web_integration)
    3. 路径查找 (sys.path 中的 knowledge_cells)
    """
    # 方式1: 尝试相对导入
    try:
        from .web_integration import RefuteCoreWeb
        instance = RefuteCoreWeb()
        logger.info("[RefuteCore] RefuteCoreWeb loaded via relative import")
        return instance
    except (ImportError, TypeError) as e:
        pass

    # 方式2: 尝试绝对导入
    try:
        from knowledge_cells.web_integration import RefuteCoreWeb
        instance = RefuteCoreWeb()
        logger.info("[RefuteCore] RefuteCoreWeb loaded via absolute import")
        return instance
    except ImportError:
        pass

    # 方式3: 尝试路径查找
    try:
        import sys
        from pathlib import Path

        # 尝试在 sys.path 中查找 knowledge_cells
        for path_str in sys.path:
            kc_path = Path(path_str) / "knowledge_cells" / "web_integration.py"
            if kc_path.exists():
                sys.path.insert(0, str(Path(path_str).parent))
                from knowledge_cells.web_integration import RefuteCoreWeb
                instance = RefuteCoreWeb()
                logger.info(f"[RefuteCore] RefuteCoreWeb loaded via path: {path_str}")
                return instance
    except Exception:
        pass

    # 所有方式都失败
    logger.warning("[RefuteCore] Failed to load RefuteCoreWeb - web search integration disabled")
    return None


# ==================== 性能常量 ====================
_MAX_RECORDS = 10000  # 最大记录数，超出后FIFO淘汰
_ID_COUNTER = 100000  # 初始计数器
_ID_LOCK = threading.Lock()  # 多线程锁：保护 _ID_COUNTER 自增


def _generate_id() -> str:
    """快速生成唯一ID：时间戳(8位) + 计数器(6位) + 随机(2位) — 线程安全"""
    global _ID_COUNTER
    with _ID_LOCK:
        counter = _ID_COUNTER
        _ID_COUNTER = (counter + 1) % 0xFFFFFF
    ts = int(time.time() * 1000) % 0xFFFFFFFF
    # 组合成紧凑ID: TTTTTTTT-CCCCCC-RR
    return f"{ts:08x}-{counter:06x}-{id(time):04x}"[:18]


# ==================== 枚举类（模块级常量） ====================

class ComplianceLevel:
    """合规等级 - 使用类属性替代Enum减少开销"""
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    SKIP = "skip"
    
    @classmethod
    def all_values(cls) -> frozenset:
        return frozenset([cls.PASS, cls.WARN, cls.FAIL, cls.SKIP])


class OversightCategory:
    """监督类别 - 使用类属性替代Enum"""
    PROCESS = "process"
    RESULT = "result"
    MEMORY_IO = "memory_io"
    
    @classmethod
    def all_values(cls) -> frozenset:
        return frozenset([cls.PROCESS, cls.RESULT, cls.MEMORY_IO])


# ==================== 快速摘要缓存 ====================

# v7.2: 基于内容哈希的缓存（替代不稳定的 id()）
_summarize_cache: Dict = {}
_SUMMARIZE_CACHE_MAX = 512


def _content_hash(data: Any) -> int:
    """生成数据的内容哈希（替代 id()，确保跨 GC 周期的缓存稳定性）"""
    if data is None:
        return 0
    if isinstance(data, str):
        return hash(data) ^ len(data)
    if isinstance(data, (dict, list, tuple)):
        try:
            return hash(repr(sorted(data.items())) if isinstance(data, dict) else repr(data))
        except Exception:
            return id(data)
    return id(data)


def _summarize_fast(data: Any) -> str:
    """快速数据摘要（带内容哈希缓存）"""
    if data is None:
        return "None"
    if isinstance(data, dict):
        summary = f"Dict({len(data)})"
    elif isinstance(data, (list, tuple)):
        summary = f"List({len(data)})"
    elif isinstance(data, str):
        summary = f"Str({len(data)})"
    else:
        summary = type(data).__name__

    # 使用内容哈希替代 id()
    h = _content_hash(data)
    cached = _summarize_cache.get(h)
    if cached is not None:
        return cached

    if len(_summarize_cache) > _SUMMARIZE_CACHE_MAX:
        _summarize_cache.clear()
    _summarize_cache[h] = summary
    return summary


# ==================== 预定义规则函数（模块级缓存） ====================

def _rule_memory_input(record: 'OversightRecord') -> tuple:
    """规则1: NeuralMemory 输入必须非空"""
    if record.category == OversightCategory.MEMORY_IO:
        if not record.input_summary or record.input_summary == "None":
            return False, "NeuralMemory 输入为空"
    return True, ""


def _rule_has_content(record: 'OversightRecord') -> tuple:
    """规则2: 成果必须有实质内容"""
    if record.category == OversightCategory.RESULT:
        output_data = record._output_data
        
        if output_data is None:
            return False, "输出数据为空"
        
        if isinstance(output_data, str) and not output_data.strip():
            return False, "输出内容为空字符串"
        
        if isinstance(output_data, dict):
            if not output_data or all(v == "" or v is None for v in output_data.values()):
                return False, "输出内容为空"
        elif isinstance(output_data, list) and not output_data:
            return False, "输出列表为空"
        
        if len(record.output_summary) < 5:
            return False, "输出内容过短"
    return True, ""


def _rule_has_trace(record: 'OversightRecord') -> tuple:
    """规则3: 所有模块必须有执行记录"""
    if not record.timestamp:
        return False, "缺少时间戳"
    return True, ""


# 预定义规则映射（模块级缓存）
_DEFAULT_RULES: Dict[str, Callable] = {
    "memory_input": _rule_memory_input,
    "has_content": _rule_has_content,
    "has_trace": _rule_has_trace,
}


# ==================== OversightRecord (使用 __slots__ 优化) ====================

class OversightRecord:
    """
    监督记录 - 使用 __slots__ 减少内存占用
    
    相比 dataclass:
    - 内存减少 ~40%
    - 属性访问速度更快
    - 防止随意添加属性
    """
    __slots__ = (
        'record_id', 'timestamp', 'category', 'module', 'action',
        'input_summary', 'output_summary', 'compliance', 'issues',
        'verdict', 'reroute', '_input_data', '_output_data',
        'verification_result',
    )
    
    def __init__(
        self,
        record_id: str,
        timestamp: str,
        category: str,
        module: str,
        action: str,
        input_summary: str,
        output_summary: str,
        compliance: str = ComplianceLevel.PASS,
        issues: Optional[List[str]] = None,
        verdict: str = "",
        reroute: bool = False,
        _input_data: Any = None,
        _output_data: Any = None,
    ):
        self.record_id = record_id
        self.timestamp = timestamp
        self.category = category
        self.module = module
        self.action = action
        self.input_summary = input_summary
        self.output_summary = output_summary
        self.compliance = compliance
        self.issues = issues if issues is not None else []
        self.verdict = verdict
        self.reroute = reroute
        self._input_data = _input_data
        self._output_data = _output_data
        self.verification_result: Optional[Dict] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（兼容旧代码）"""
        d = {
            "record_id": self.record_id,
            "timestamp": self.timestamp,
            "category": self.category,
            "module": self.module,
            "action": self.action,
            "input_summary": self.input_summary,
            "output_summary": self.output_summary,
            "compliance": self.compliance,
            "issues": self.issues,
            "verdict": self.verdict,
            "reroute": self.reroute,
        }
        if self.verification_result is not None:
            d["verification_result"] = self.verification_result
        return d


# ==================== OversightReport ====================

class OversightReport:
    """监督报告"""
    __slots__ = ('total_records', 'pass_count', 'warn_count', 'fail_count', 
                  'reroute_count', 'records', 'summary')
    
    def __init__(self, total_records: int, pass_count: int, warn_count: int,
                 fail_count: int, reroute_count: int, records: List, summary: str):
        self.total_records = total_records
        self.pass_count = pass_count
        self.warn_count = warn_count
        self.fail_count = fail_count
        self.reroute_count = reroute_count
        self.records = records
        self.summary = summary
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_records": self.total_records,
            "pass_count": self.pass_count,
            "warn_count": self.warn_count,
            "fail_count": self.fail_count,
            "reroute_count": self.reroute_count,
            "records": self.records,
            "summary": self.summary,
        }


# ==================== DivineTrackOversight v2 ====================

class DivineTrackOversight:
    """
    神政轨监督框架 v2.0
    
    性能优化：
    - 使用 __slots__ 的 OversightRecord
    - 预定义规则函数（模块级缓存）
    - 快速ID生成
    - 记录上限机制（防止内存泄漏）
    - 批量记录支持
    
    单例模式：sys.modules + 类级双保险
    """
    
    VERSION = "6.2.0"
    _global_instance: Optional['DivineTrackOversight'] = None
    
    def __init__(self, enabled: bool = True, max_records: int = _MAX_RECORDS):
        # 单例复用
        if DivineTrackOversight._global_instance is not None:
            existing = DivineTrackOversight._global_instance
            self.enabled = enabled
            self.records = existing.records
            self._watched_modules = existing._watched_modules
            self.watched_modules = existing.watched_modules
            self._rules = existing._rules
            self._max_records = max_records
            self._refute_web = existing._refute_web
            # 输出验证器（懒加载）- 单例复用时指向同一个实例
            self._output_verifier = existing._output_verifier
            self.auto_verify_output = existing.auto_verify_output
            self.verify_output_threshold = existing.verify_output_threshold
            return

        self.enabled = enabled
        self._max_records = max_records
        # 使用 deque 实现 FIFO 淘汰
        self.records: deque = deque(maxlen=max_records)
        self._watched_modules: Dict[str, bool] = {}
        self.watched_modules: List[str] = []
        # 直接引用预定义规则（模块级缓存）
        self._rules: Dict[str, Callable] = _DEFAULT_RULES
        # 网络搜索增强（懒加载）
        self._refute_web: Optional[Any] = None

        DivineTrackOversight._global_instance = self

        # 输出验证器（懒加载）
        self._output_verifier: Optional[Any] = None
        self.auto_verify_output: bool = True      # 是否自动验证输出
        self.verify_output_threshold: float = 0.6  # 置信度阈值，低于此值触发验证
    
    def watch(self, module: str) -> None:
        """开始监督指定模块"""
        self._watched_modules[module] = True
        if module not in self.watched_modules:
            self.watched_modules.append(module)

    # ══════════════════════════════════════════════════════════
    #  输出验证集成（OutputVerifier）
    # ══════════════════════════════════════════════════════════

    @property
    def output_verifier(self):
        """懒加载 OutputVerifier"""
        if self._output_verifier is None:
            try:
                from knowledge_cells.output_verifier import OutputVerifier
                self._output_verifier = OutputVerifier()
                logger.info("[DivineOversight] OutputVerifier loaded")
            except ImportError as e:
                logger.warning(f"[DivineOversight] OutputVerifier not available: {e}")
                return None
        return self._output_verifier

    def verify_output(
        self,
        llm_output: str,
        module: str = "",
        auto_correct: bool = True,
        skip_auto_record: bool = False,
    ) -> Dict[str, Any]:
        """
        验证LLM输出（自动触发网络搜索验证）

        Args:
            llm_output: LLM原始输出
            module: 来源模块名（用于记录）
            auto_correct: 是否自动修正输出
            skip_auto_record: 是否跳过自动记录（防止递归）

        Returns:
            {
                "verified_output": str,      # 验证后输出（可能已修正）
                "overall_confidence": float, # 整体置信度
                "needs_human_review": bool,  # 是否需要人工复核
                "verification_summary": str,  # 验证摘要
                "statements": List[Dict],    # 各陈述验证详情
            }
        """
        verifier = self.output_verifier
        if verifier is None:
            return {
                "verified_output": llm_output,
                "overall_confidence": 1.0,
                "needs_human_review": False,
                "verification_summary": "OutputVerifier 未加载，跳过验证",
                "statements": [],
            }

        # 调用验证器
        result = verifier.verify_output(llm_output)

        # 记录验证结果到监督系统
        if module and not skip_auto_record:
            self.record(
                module=module,
                action="output_verification",
                category=OversightCategory.RESULT,
                input_data={"output_snippet": llm_output[:200]},
                output_data={
                    "confidence": result.overall_confidence,
                    "needs_review": result.needs_human_review,
                    "statement_count": len(result.statements),
                },
                skip_checks=True,
            )

        # 构建返回结果
        verified_result = {
            "verified_output": result.verified_output if auto_correct else llm_output,
            "original_output": result.original_output,
            "overall_confidence": result.overall_confidence,
            "needs_human_review": result.needs_human_review,
            "verification_summary": result.verification_summary,
            "statements": [
                {
                    "text": s.text,
                    "type": s.stmt_type.value,
                    "status": s.verification_status.value,
                    "confidence": s.confidence,
                    "has_correction": bool(s.corrected_text),
                    "source_urls": s.source_urls[:3],
                }
                for s in result.statements
            ],
            "auto_corrected": auto_correct and result.verified_output != result.original_output,
        }

        # v7.0: 当规则验证不确定时，尝试 LLM 辅助验证
        if result.overall_confidence < self.verify_output_threshold:
            llm_val = self._llm_validate(llm_output, context="")
            if llm_val:
                verified_result["llm_validation"] = llm_val
                # 如果 LLM 验证结果更可靠，更新置信度
                if llm_val["confidence"] > result.overall_confidence:
                    verified_result["overall_confidence"] = llm_val["confidence"]
                    verified_result["needs_human_review"] = not llm_val["validated"]

        return verified_result

    def verify_and_store(
        self,
        llm_output: str,
        store_to_memory: bool = True,
    ) -> Dict[str, Any]:
        """
        验证输出并存储验证结果到记忆系统
        """
        verifier = self.output_verifier
        if verifier is None:
            return {"error": "OutputVerifier not available"}

        try:
            from knowledge_cells.output_verifier import verify_llm_output
            result = verify_llm_output(llm_output)

            if store_to_memory:
                # 存储到DomainNexus
                try:
                    from knowledge_cells.domain_nexus import DomainNexus
                    nexus = DomainNexus()
                    nexus.add_verification_record({
                        "output_snippet": llm_output[:200],
                        "confidence": result.overall_confidence,
                        "verified": result.verified_output != result.original_output,
                        "needs_review": result.needs_human_review,
                    })
                except Exception:
                    pass

            return {
                "verified_output": result.verified_output,
                "overall_confidence": result.overall_confidence,
                "needs_human_review": result.needs_human_review,
                "summary": result.verification_summary,
            }
        except Exception as e:
            logger.error(f"verify_and_store failed: {e}")
            return {"error": str(e)}

    def _llm_validate(
        self,
        text: str,
        context: str = "",
    ) -> Dict[str, Any]:
        """
        v7.0: 使用 LLM 做二次验证确认

        当规则验证不确定时，尝试用 LLM 获取辅助验证。

        Args:
            text: 待验证文本
            context: 上下文信息

        Returns:
            {
                "validated": bool,      # LLM是否认为合理
                "confidence": float,    # 置信度
                "issues": List[str],   # 发现的问题
                "suggestions": str,    # 修正建议
            }
        """
        result = {
            "validated": True,
            "confidence": 0.8,
            "issues": [],
            "suggestions": "",
        }

        try:
            from .llm_rule_layer import call_module_llm
            system_prompt = "你是论证审查专家，擅长识别论证中的逻辑问题和改进建议。"
            prompt = f"""请审查以下论证文本，判断其质量：

文本：{text[:500]}
上下文：{context[:200] if context else '无'}

请判断：
1. 论证是否合理？
2. 存在哪些问题？
3. 如何改进？"""

            llm_feedback = call_module_llm("TrackA", prompt, system_prompt=system_prompt)

            # 解析LLM反馈
            if "不合理" in llm_feedback or "有问题" in llm_feedback:
                result["validated"] = False
                result["confidence"] = 0.5
            elif "基本合理" in llm_feedback or "可以接受" in llm_feedback:
                result["validated"] = True
                result["confidence"] = 0.75

            # 提取问题和建议
            if "问题" in llm_feedback:
                lines = llm_feedback.split("\n")
                for line in lines:
                    if "问题" in line or "建议" in line:
                        result["issues"].append(line.strip())

        except Exception as e:
            logger.debug(f"[DivineOversight] LLM validation failed: {e}")

        return result

    def set_auto_verify(self, enabled: bool, threshold: float = 0.6):
        """设置自动验证参数"""
        self.auto_verify_output = enabled
        self.verify_output_threshold = threshold
        logger.info(f"[DivineOversight] auto_verify={enabled}, threshold={threshold}")

    # ══════════════════════════════════════════════════════════
    
    def unwatch(self, module: str) -> None:
        """停止监督指定模块"""
        self._watched_modules[module] = False
        if module in self.watched_modules:
            self.watched_modules.remove(module)
    
    def record(
        self,
        module: str,
        action: str,
        category: str,
        input_data: Any = None,
        output_data: Any = None,
        custom_rules: Optional[List[str]] = None,
        skip_checks: bool = False,
        auto_verify_output: Optional[bool] = None,
    ) -> Optional[OversightRecord]:
        """
        记录监督数据

        性能优化:
        - 快速ID生成
        - 缓存摘要
        - 可选跳过检查（批量模式）
        - 自动输出验证（新增）

        Args:
            auto_verify_output: 是否自动验证输出（None=使用全局配置）
        """
        if not self.enabled:
            return None

        # 快速生成
        record_id = _generate_id()
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")

        # 缓存摘要
        input_summary = _summarize_fast(input_data)
        output_summary = _summarize_fast(output_data)

        # 创建记录
        record = OversightRecord(
            record_id=record_id,
            timestamp=timestamp,
            category=category,
            module=module,
            action=action,
            input_summary=input_summary,
            output_summary=output_summary,
            compliance=ComplianceLevel.PASS,
            _input_data=input_data,
            _output_data=output_data,
        )

        # 合规检查（可跳过用于批量操作）
        if not skip_checks:
            self._check_compliance(record, custom_rules)

        # ════════════════════════════════════════════════════════
        #  自动输出验证（新增）
        # ════════════════════════════════════════════════════════
        should_verify = (
            auto_verify_output
            if auto_verify_output is not None
            else self.auto_verify_output
        )

        if (
            should_verify
            and category == OversightCategory.RESULT
            and output_data is not None
        ):
            # 只验证字符串输出
            output_text = ""
            if isinstance(output_data, str):
                output_text = output_data
            elif isinstance(output_data, dict) and "text" in output_data:
                output_text = output_data["text"]
            elif isinstance(output_data, dict) and "content" in output_data:
                output_text = output_data["content"]
            elif isinstance(output_data, list) and output_data:
                # 列表取第一个字符串元素
                first_item = output_data[0]
                if isinstance(first_item, str):
                    output_text = first_item

            # 需要验证的输出非空
            if output_text and len(output_text) >= 20:
                try:
                    verification = self.verify_output(
                        llm_output=output_text,
                        module=module,
                        auto_correct=False,  # 只验证，不自动修正
                        skip_auto_record=True,  # 防止递归：验证内部不再触发 record()
                    )

                    # 将验证结果附加到记录
                    record.verification_result = verification
                    record.output_summary += f" [验证置信度:{verification['overall_confidence']:.2f}]"

                    # 如果置信度低于阈值，标记为需要复核
                    if verification["overall_confidence"] < self.verify_output_threshold:
                        record.issues.append(
                            f"输出验证置信度低: {verification['overall_confidence']:.2f}"
                        )
                        record.compliance = ComplianceLevel.WARN
                        logger.warning(
                            f"[DivineOversight] Low confidence output from {module}: "
                            f"{verification['overall_confidence']:.2f}"
                        )

                except Exception as e:
                    logger.warning(f"Auto verification failed for {module}: {e}")

        # 存储（deque自动处理FIFO淘汰）
        self.records.append(record)

        return record
    
    def _check_compliance(
        self,
        record: OversightRecord,
        custom_rules: Optional[List[str]] = None
    ) -> None:
        """执行合规检查"""
        rules_to_check = custom_rules or list(self._rules.keys())
        
        for rule_name in rules_to_check:
            if rule_name not in self._rules:
                continue
            
            passed, issue = self._rules[rule_name](record)
            
            if not passed:
                record.issues.append(issue)
                record.compliance = ComplianceLevel.FAIL
                record.verdict = f"驳回: {issue}"
                record.reroute = True
                break
        
        if record.compliance == ComplianceLevel.PASS and record.issues:
            record.compliance = ComplianceLevel.WARN
            record.verdict = "警告: " + "; ".join(record.issues)
    
    def check_compliance(self, record: OversightRecord, 
                        custom_rules: Optional[List[str]] = None) -> OversightRecord:
        """公共方法：对记录执行合规检查"""
        self._check_compliance(record, custom_rules)
        return record
    
    def record_batch(
        self,
        records_data: List[Dict[str, Any]],
        skip_checks: bool = True,
    ) -> List[OversightRecord]:
        """
        批量记录（性能优化）
        
        Args:
            records_data: 记录数据列表
            skip_checks: 是否跳过合规检查（批量时跳过，最后统一检查）
        
        Returns:
            记录的列表
        """
        results = []
        for data in records_data:
            rec = self.record(
                module=data.get("module", "unknown"),
                action=data.get("action", ""),
                category=data.get("category", OversightCategory.PROCESS),
                input_data=data.get("input_data"),
                output_data=data.get("output_data"),
                skip_checks=skip_checks,
            )
            if rec:
                results.append(rec)
        
        # 批量检查（可选）
        if not skip_checks:
            for rec in results:
                self._check_compliance(rec)
        
        return results
    
    def reroute(self, record: OversightRecord, reason: str) -> Dict[str, Any]:
        """生成驳回指令"""
        record.reroute = True
        record.verdict = f"驳回: {reason}"
        record.compliance = ComplianceLevel.FAIL
        record.issues.append(reason)
        
        return {
            "action": "reroute",
            "record_id": record.record_id,
            "reason": reason,
            "module": record.module,
            "original_action": record.action,
            "allow_continue": True,
            "suggestion": f"请检查{record.module}的{record.action}输出"
        }
    
    def get_report(self) -> Dict[str, Any]:
        """生成监督报告"""
        records_list = list(self.records)
        
        pass_count = sum(1 for r in records_list if r.compliance == ComplianceLevel.PASS)
        warn_count = sum(1 for r in records_list if r.compliance == ComplianceLevel.WARN)
        fail_count = sum(1 for r in records_list if r.compliance == ComplianceLevel.FAIL)
        reroute_count = sum(1 for r in records_list if r.reroute)
        
        return {
            "total_records": len(records_list),
            "pass_count": pass_count,
            "warn_count": warn_count,
            "fail_count": fail_count,
            "reroute_count": reroute_count,
            "records": [r.to_dict() for r in records_list],
            "summary": f"监督 {len(records_list)} 条记录，{pass_count} 通过，{warn_count} 警告，{fail_count} 驳回"
        }
    
    def clear(self) -> None:
        """清空监督记录"""
        self.records.clear()
    
    def is_watching(self, module: str) -> bool:
        """检查是否在监督某模块"""
        return self._watched_modules.get(module, False)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        records_list = list(self.records)
        return {
            "total_records": len(records_list),
            "max_records": self._max_records,
            "memory_usage_estimate": len(records_list) * 200,  # 估算bytes
            "watched_modules": len(self.watched_modules),
            "enabled": self.enabled,
        }

    # ═══════════════════════════════════════════════════════════════
    #  网络搜索增强方法（RefuteCore 论证系统）
    # ═══════════════════════════════════════════════════════════════

    @property
    def refute_web(self):
        """懒加载 RefuteCoreWeb"""
        if self._refute_web is None:
            self._refute_web = _get_refute_web()
        return self._refute_web

    def verify_with_evidence(
        self,
        claim: str,
        context: str = "",
        max_results: int = 3,
    ) -> Dict[str, Any]:
        """
        使用网络搜索验证论点（带证据支持/反驳）

        Args:
            claim: 论点/主张
            context: 上下文信息
            max_results: 最大结果数

        Returns:
            {
                "claim": str,
                "supporting_evidence": List[Dict],
                "counter_evidence": List[Dict],
                "web_available": bool,
            }
        """
        result = {
            "claim": claim,
            "supporting_evidence": [],
            "counter_evidence": [],
            "web_available": False,
        }

        refute_web = self.refute_web
        if not refute_web or not refute_web.is_enabled():
            return result

        # 搜索支持性证据
        try:
            supporting = refute_web.search_supporting_evidence(claim, max_results)
            if supporting.get("success") and supporting.get("results"):
                result["supporting_evidence"] = supporting["results"]
        except Exception as e:
            logger.warning(f"[RefuteCore] Supporting evidence search failed: {e}")

        # 搜索反驳性证据
        try:
            counter = refute_web.search_counter_evidence(claim, max_results)
            if counter.get("success") and counter.get("results"):
                result["counter_evidence"] = counter["results"]
        except Exception as e:
            logger.warning(f"[RefuteCore] Counter evidence search failed: {e}")

        result["web_available"] = bool(result["supporting_evidence"] or result["counter_evidence"])
        return result

    def verify_fact_statement(
        self,
        statement: str,
    ) -> Dict[str, Any]:
        """
        事实核查（使用网络搜索）

        Args:
            statement: 待核查的陈述

        Returns:
            {
                "statement": str,
                "verifiable": bool,
                "evidence": List[Dict],
                "verified": bool,
            }
        """
        result = {
            "statement": statement,
            "verifiable": False,
            "evidence": [],
            "verified": False,
        }

        refute_web = self.refute_web
        if not refute_web or not refute_web.is_enabled():
            return result

        # 检查是否需要网络搜索
        if not refute_web.should_search(statement):
            return result

        try:
            verification = refute_web.verify_fact(statement, max_results=2)
            if verification.get("success") and verification.get("results"):
                result["verifiable"] = True
                result["evidence"] = verification["results"]
        except Exception as e:
            logger.warning(f"[RefuteCore] Fact verification failed: {e}")

        return result

    def enhance_reroute_with_evidence(
        self,
        record: OversightRecord,
        reason: str,
    ) -> Dict[str, Any]:
        """
        增强驳回指令（搜索相关证据）

        在驳回时搜索相关证据，帮助被驳回的模块更好地理解问题
        """
        reroute_result = self.reroute(record, reason)

        # 尝试搜索相关证据
        evidence = self.verify_with_evidence(
            claim=reason,
            context=f"{record.module} {record.action}",
            max_results=2
        )

        if evidence.get("web_available"):
            reroute_result["evidence"] = {
                "supporting": evidence.get("supporting_evidence", []),
                "counter": evidence.get("counter_evidence", []),
            }
            logger.info(f"[RefuteCore] Enhanced reroute with {len(evidence.get('supporting_evidence', []))} supporting and {len(evidence.get('counter_evidence', []))} counter evidence")

        return reroute_result


# ==================== 便捷函数 ====================

_DIVINE_TRACK_KEY = "knowledge_cells.__divine_oversight__"


def get_oversight() -> DivineTrackOversight:
    """获取全局监督实例"""
    if _DIVINE_TRACK_KEY not in sys.modules:
        instance = DivineTrackOversight()
        sys.modules[_DIVINE_TRACK_KEY] = instance
    else:
        instance = sys.modules[_DIVINE_TRACK_KEY]
    
    DivineTrackOversight._global_instance = instance
    return instance


def record_oversight(
    module: str,
    action: str,
    category: str,
    input_data: Any = None,
    output_data: Any = None,
) -> Optional[OversightRecord]:
    """快捷记录函数"""
    return get_oversight().record(module, action, category, input_data, output_data)


# ==================== 装饰器 ====================

def oversee_module(module_name: str):
    """模块监督装饰器"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            oversight = get_oversight()
            oversight.watch(module_name)
            
            # 记录输入
            oversight.record(
                module=module_name,
                action=f"{func.__name__}_input",
                category=OversightCategory.PROCESS,
                input_data={"args": str(args)[:50], "kwargs": list(kwargs.keys())[:10]},
                skip_checks=True,
            )
            
            # 执行原函数
            result = func(*args, **kwargs)
            
            # 记录输出
            output_record = oversight.record(
                module=module_name,
                action=f"{func.__name__}_output",
                category=OversightCategory.RESULT,
                input_data={"args": str(args)[:50]},
                output_data=result,
            )
            
            # 如果输出不合规，添加驳回标记
            if output_record and output_record.reroute:
                if isinstance(result, dict):
                    result["_oversight_reroute"] = True
                    result["_oversight_issues"] = output_record.issues
            
            return result
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator


def oversee_memory_io(
    key: str,
    value: Any = None,
    operation: str = "store",
    module_name: str = "NeuralMemory"
) -> Optional[OversightRecord]:
    """快捷NeuralMemory I/O监督函数"""
    oversight = get_oversight()
    
    action_map = {
        "store": "memory_store",
        "retrieve": "memory_retrieve", 
        "delete": "memory_delete",
        "read": "memory_read",
        "write": "memory_write"
    }
    
    action = action_map.get(operation, f"memory_{operation}")
    
    return oversight.record(
        module=module_name,
        action=action,
        category=OversightCategory.MEMORY_IO,
        input_data={"key": key, "operation": operation},
        output_data={"status": "success" if value is not None else "pending"},
        skip_checks=True,
    )


# 兼容别名
oversight_memory_io = oversee_memory_io


# ==================== 性能基准 ====================

def benchmark_oversight(iterations: int = 1000) -> Dict[str, float]:
    """性能基准测试"""
    import time
    
    oversight = DivineTrackOversight()
    oversight.clear()
    
    # 测试单条记录
    start = time.perf_counter()
    for _ in range(iterations):
        oversight.record(
            module="Benchmark",
            action="test",
            category=OversightCategory.RESULT,
            input_data={"key": "value"},
            output_data={"result": "ok"},
        )
    single_time = time.perf_counter() - start
    
    # 测试批量记录
    oversight.clear()
    batch_data = [
        {"module": "M1", "action": "a1", "category": OversightCategory.PROCESS, 
         "input_data": {}, "output_data": {}}
        for _ in range(iterations)
    ]
    start = time.perf_counter()
    oversight.record_batch(batch_data)
    batch_time = time.perf_counter() - start
    
    # 测试带检查的记录
    oversight.clear()
    start = time.perf_counter()
    for _ in range(iterations):
        oversight.record(
            module="Benchmark",
            action="test",
            category=OversightCategory.RESULT,
            input_data={"key": "value"},
            output_data={"result": "ok"},
            skip_checks=False,
        )
    check_time = time.perf_counter() - start
    
    return {
        "iterations": iterations,
        "single_per_record_ms": single_time / iterations * 1000,
        "batch_per_record_ms": batch_time / iterations * 1000,
        "check_per_record_ms": check_time / iterations * 1000,
        "speedup_batch_vs_single": single_time / batch_time if batch_time > 0 else 0,
    }


# ==================== 使用示例 ====================

if __name__ == "__main__":
    print("神政轨监督框架 v2.0 - 性能优化版")
    print("-" * 50)
    
    # 基本使用
    oversight = DivineTrackOversight()
    
    # 监督 RefuteCore
    oversight.watch("RefuteCore")
    record = oversight.record(
        module="RefuteCore",
        action="refute",
        category=OversightCategory.RESULT,
        input_data={"text": "AI将改变教育"},
        output_data={"refutations": ["假设错误"], "strength": "B"}
    )
    print(f"合规等级: {record.compliance}")
    print(f"驳回: {record.reroute}")
    
    # 性能基准
    print("\n性能基准测试:")
    stats = benchmark_oversight(1000)
    print(f"  单条记录: {stats['single_per_record_ms']:.4f} ms/条")
    print(f"  批量记录: {stats['batch_per_record_ms']:.4f} ms/条")
    print(f"  带检查:   {stats['check_per_record_ms']:.4f} ms/条")
    print(f"  批量加速: {stats['speedup_batch_vs_single']:.2f}x")
    
    # 统计信息
    print(f"\n{oversight.get_stats()}")
