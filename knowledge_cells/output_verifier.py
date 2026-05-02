"""
输出验证器 v1.0
====================
LLM 输出事实核查与自动修正闭环

核心流程：
  LLM输出
    ↓
  [自动触发] 提取可验证陈述（数字/日期/事实断言）
    ↓
  [网络搜索] 对每条陈述搜索验证
    ↓
  [一致性比对] LLM输出 vs 搜索结果
    ↓
     ├─ 一致 → 通过，标注来源
     ├─ 冲突 → 自动修正 + 重新输出
     └─ 无法验证 → 标注"需人工核实"

设计原则：
  1. 不验证所有输出，只验证含客观事实的陈述
  2. 验证失败不直接驳回，而是标注可信度
  3. 验证结果作为新证据存回记忆系统
"""

from __future__ import annotations

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

# ==================== 枚举定义 ====================


class VerificationStatus(Enum):
    """验证状态"""
    CONSISTENT = "consistent"        # 与搜索结果一致
    CONFLICT = "conflict"            # 与搜索结果冲突
    UNVERIFIABLE = "unverifiable"  # 无法验证（无搜索结果）
    NEEDS_HUMAN = "needs_human"     # 需要人工核实


class StatementType(Enum):
    """可验证陈述类型"""
    NUMERIC = "numeric"          # 数字（价格/数量/百分比）
    DATE = "date"                # 日期/时间
    FACT = "fact"                # 事实断言
    QUOTE = "quote"              # 引述
    DEFINITION = "definition"    # 定义/概念


# ==================== 数据结构 ====================


@dataclass
class VerifiableStatement:
    """可验证陈述"""
    text: str                          # 陈述原文
    stmt_type: StatementType           # 陈述类型
    confidence: float = 0.5           # 原始置信度
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIABLE
    evidence: List[Dict[str, str]] = field(default_factory=list)  # 支持/反驳证据
    corrected_text: str = ""          # 修正后的陈述（如有）
    source_urls: List[str] = field(default_factory=list)


@dataclass
class VerificationResult:
    """验证结果"""
    original_output: str                         # 原始输出
    verified_output: str                        # 验证后输出（可能已修正）
    statements: List[VerifiableStatement]       # 所有可验证陈述
    overall_confidence: float                   # 整体置信度
    needs_human_review: bool                   # 是否需要人工复核
    verification_summary: str                   # 验证摘要


# ==================== 陈述提取器 ====================


class StatementExtractor:
    """
    从LLM输出中提取可验证陈述

    触发规则：
    - 含数字 + 单位（元/吨/个/%/美元等）
    - 含日期（2024年/昨日/本月等）
    - 含"是"/"为"/"达到"等判断词 + 专有名词
    - 含引号内的引述
    """

    # 数字模式：匹配数字+单位
    _NUMERIC_PATTERN = re.compile(
        r'(\d+\.?\d*)\s*'
        r'(元|美元|欧元|吨|公斤|克|个|件|套|台|'
        r'%|百分|亿美元|万元|亿元|千元|'
        r'人|用户|客户|订单|)',
        re.IGNORECASE
    )

    # 日期模式
    _DATE_PATTERN = re.compile(
        r'(\d{4}年\d{1,2}月\d{1,2}日|'
        r'\d{1,2}月\d{1,2}日|'
        r'昨日|前日|今天|本月|上年度|202\d年)',
        re.IGNORECASE
    )

    # 事实判断模式
    _FACT_PATTERN = re.compile(
        r'([是|为|达到|增至|降至|超过|突破|降至]'
        r'[^。，；\n]{2,50}'
        r'(市场|公司|产品|技术|政策|法规|数据))',
        re.IGNORECASE
    )

    # 引述模式
    _QUOTE_PATTERN = re.compile(r'[""]([^"""]{5,200})[""]')

    @classmethod
    def extract(cls, text: str) -> List[VerifiableStatement]:
        """
        从文本中提取可验证陈述

        Args:
            text: LLM输出文本

        Returns:
            可验证陈述列表
        """
        statements = []
        seen_texts = set()

        # 1. 提取数字陈述
        for match in cls._NUMERIC_PATTERN.finditer(text):
            stmt_text = cls._extract_sentence_containing(text, match.start())
            if stmt_text and stmt_text not in seen_texts:
                seen_texts.add(stmt_text)
                statements.append(VerifiableStatement(
                    text=stmt_text,
                    stmt_type=StatementType.NUMERIC,
                    confidence=0.6  # 数字陈述默认中等置信度
                ))

        # 2. 提取日期陈述
        for match in cls._DATE_PATTERN.finditer(text):
            stmt_text = cls._extract_sentence_containing(text, match.start())
            if stmt_text and stmt_text not in seen_texts:
                seen_texts.add(stmt_text)
                statements.append(VerifiableStatement(
                    text=stmt_text,
                    stmt_type=StatementType.DATE,
                    confidence=0.5
                ))

        # 3. 提取事实断言
        for match in cls._FACT_PATTERN.finditer(text):
            stmt_text = match.group(0).strip()
            if stmt_text and stmt_text not in seen_texts:
                seen_texts.add(stmt_text)
                statements.append(VerifiableStatement(
                    text=stmt_text,
                    stmt_type=StatementType.FACT,
                    confidence=0.4  # 事实断言置信度较低，需要验证
                ))

        # 4. 提取引述
        for match in cls._QUOTE_PATTERN.finditer(text):
            quote_text = match.group(1).strip()
            if quote_text and quote_text not in seen_texts:
                seen_texts.add(quote_text)
                # 扩取到完整句子
                full_stmt = cls._extract_sentence_containing(text, match.start())
                statements.append(VerifiableStatement(
                    text=full_stmt or f'"{quote_text}"',
                    stmt_type=StatementType.QUOTE,
                    confidence=0.3  # 引述置信度最低
                ))

        return statements

    @staticmethod
    def _extract_keywords(text: str) -> str:
        """从文本中提取关键词（简化版）"""
        # 去除常见停用词，保留名词性短语
        stop_words = {
            "的", "了", "是", "在", "和", "与", "或", "以及", "对于", "关于",
            "一个", "这种", "那种", "可以", "已经", "正在", "将要",
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
        }
        import re
        words = re.findall(r'[\w\u4e00-\u9fff]{2,}', text)
        keywords = [w for w in words if w not in stop_words]
        return " ".join(keywords[:5])

    @staticmethod
    def _extract_sentence_containing(text: str, pos: int) -> str:
        """提取包含指定位置的完整句子"""
        # 向前找到句子开头
        sentence_start = 0
        for i in range(pos, max(0, pos - 200), -1):
            if i < len(text) and text[i] in '。！？\n':
                sentence_start = i + 1
                break

        # 向后找到句子结尾
        sentence_end = len(text)
        for i in range(pos, min(len(text), pos + 300)):
            if text[i] in '。！？\n':
                sentence_end = i + 1
                break

        sentence = text[sentence_start:sentence_end].strip()
        # 清理多余空白
        sentence = re.sub(r'\s+', ' ', sentence)
        return sentence if len(sentence) >= 5 else ""


# ==================== 证据搜寻器 ====================


class EvidenceSearcher:
    """
    对陈述进行网络搜索，收集支持/反驳证据
    """

    def __init__(self, max_results_per_stmt: int = 3):
        self.max_results = max_results_per_stmt

    def search_evidence(self, statement: VerifiableStatement) -> VerifiableStatement:
        """
        为陈述搜索证据，并返回更新后的陈述

        Args:
            statement: 待验证陈述

        Returns:
            更新了验证状态和证据的陈述
        """
        try:
            from knowledge_cells.web_integration import search_with_fallback
            from knowledge_cells.web_integration import is_online
        except ImportError:
            logger.warning("web_integration not available, skipping evidence search")
            statement.verification_status = VerificationStatus.UNVERIFIABLE
            return statement

        if not is_online():
            statement.verification_status = VerificationStatus.UNVERIFIABLE
            return statement

        # 构建搜索查询
        query = self._build_search_query(statement)
        if not query:
            statement.verification_status = VerificationStatus.UNVERIFIABLE
            return statement

        # 执行搜索
        try:
            response = search_with_fallback(query, max_results=self.max_results)
        except Exception as e:
            logger.warning(f"Evidence search failed for '{statement.text[:50]}...': {e}")
            statement.verification_status = VerificationStatus.UNVERIFIABLE
            return statement

        if not response.get("success") or not response.get("results"):
            statement.verification_status = VerificationStatus.UNVERIFIABLE
            return statement

        # 解析搜索结果作为证据
        evidence_list = []
        for r in response["results"]:
            evidence_list.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("snippet", ""),
                "source": r.get("source", ""),
            })
            if r.get("url"):
                statement.source_urls.append(r["url"])

        statement.evidence = evidence_list

        # 初步判断：有证据 = 可验证（具体一致性比对由 StatementVerifier 完成）
        statement.verification_status = VerificationStatus.CONSISTENT

        return statement

    @staticmethod
    def _build_search_query(statement: VerifiableStatement) -> str:
        """根据陈述类型构建搜索查询"""
        text = statement.text

        if statement.stmt_type == StatementType.NUMERIC:
            # 提取数字和上下文关键词
            num_match = re.search(r'\d+\.?\d*', text)
            if num_match:
                number = num_match.group(0)
                # 提取数字附近的关键词（去停用词）
                keywords = StatementExtractor._extract_keywords(text)
                return f"{number} {keywords}"
            return text[:50]

        elif statement.stmt_type == StatementType.DATE:
            keywords = StatementExtractor._extract_keywords(text)
            return f"{text[:20]} {keywords}"

        elif statement.stmt_type == StatementType.QUOTE:
            # 引述搜索用关键词
            return StatementExtractor._extract_keywords(text)

        else:  # FACT
            return StatementExtractor._extract_keywords(text) or text[:50]


# ==================== 陈述验证器 ====================


class StatementVerifier:
    """
    比对陈述与证据，判断一致性

    核心逻辑：
    1. 数字陈述：比对数字是否一致（允许±5%误差）
    2. 日期陈述：比对日期是否一致
    3. 事实陈述：检查证据是否支持该事实
    4. 引述陈述：检查证据中是否出现相同或相似表述
    """

    @classmethod
    def verify(cls, statement: VerifiableStatement) -> VerifiableStatement:
        """
        验证陈述与证据的一致性

        Args:
            statement: 含证据的陈述

        Returns:
            更新了验证状态的陈述
        """
        if not statement.evidence:
            statement.verification_status = VerificationStatus.UNVERIFIABLE
            return statement

        if statement.stmt_type == StatementType.NUMERIC:
            return cls._verify_numeric(statement)
        elif statement.stmt_type == StatementType.DATE:
            return cls._verify_date(statement)
        elif statement.stmt_type == StatementType.FACT:
            return cls._verify_fact(statement)
        elif statement.stmt_type == StatementType.QUOTE:
            return cls._verify_quote(statement)
        else:
            return statement

    @classmethod
    def _verify_numeric(cls, stmt: VerifiableStatement) -> VerifiableStatement:
        """验证数字陈述"""
        # 从陈述中提取数字
        stmt_numbers = re.findall(r'\d+\.?\d*', stmt.text)

        # 从证据中搜索相同/相近数字
        found_match = False
        best_match = None
        min_diff_ratio = float('inf')

        for ev in stmt.evidence:
            search_text = ev["title"] + " " + ev["snippet"]
            ev_numbers = re.findall(r'\d+\.?\d*', search_text)

            for sn in stmt_numbers:
                for en in ev_numbers:
                    try:
                        s_val = float(sn)
                        e_val = float(en)
                        if e_val == 0:
                            continue
                        diff_ratio = abs(s_val - e_val) / e_val
                        if diff_ratio < min_diff_ratio:
                            min_diff_ratio = diff_ratio
                            best_match = (s_val, e_val, ev)
                    except ValueError:
                        continue

        # 判断：差异小于5%认为一致；差异大于20%认为冲突
        if best_match and min_diff_ratio <= 0.05:
            stmt.verification_status = VerificationStatus.CONSISTENT
            stmt.confidence = min(0.95, stmt.confidence + 0.3)
        elif best_match and min_diff_ratio >= 0.20:
            stmt.verification_status = VerificationStatus.CONFLICT
            stmt.confidence = max(0.1, stmt.confidence - 0.4)
            # 生成修正建议
            s_val, e_val, ev = best_match
            stmt.corrected_text = cls._correct_numeric_statement(
                stmt.text, s_val, e_val, ev
            )
        else:
            stmt.verification_status = VerificationStatus.UNVERIFIABLE

        return stmt

    @classmethod
    def _verify_date(cls, stmt: VerifiableStatement) -> VerifiableStatement:
        """验证日期陈述"""
        # 简化版：检查证据中是否出现相同日期表达
        stmt_dates = re.findall(
            r'(\d{4}年\d{1,2}月\d{1,2}日|\d{1,2}月\d{1,2}日|昨日|前日|今天|本月|202\d年)',
            stmt.text
        )

        if not stmt_dates:
            stmt.verification_status = VerificationStatus.UNVERIFIABLE
            return stmt

        found_in_evidence = False
        for ev in stmt.evidence:
            search_text = ev["title"] + " " + ev["snippet"]
            for dt in stmt_dates:
                if dt in search_text:
                    found_in_evidence = True
                    break
            if found_in_evidence:
                break

        if found_in_evidence:
            stmt.verification_status = VerificationStatus.CONSISTENT
            stmt.confidence = min(0.9, stmt.confidence + 0.2)
        else:
            stmt.verification_status = VerificationStatus.UNVERIFIABLE

        return stmt

    @classmethod
    def _verify_fact(cls, stmt: VerifiableStatement) -> VerifiableStatement:
        """验证事实陈述"""
        # 简化版：检查证据中是否支持该事实
        # 策略：将陈述关键词与证据做重叠度计算
        stmt_keywords = set(EvidenceSearcher._extract_keywords(stmt.text).split())

        support_count = 0
        contradict_count = 0

        for ev in stmt.evidence:
            ev_text = (ev["title"] + " " + ev["snippet"]).lower()
            ev_keywords = set(EvidenceSearcher._extract_keywords(ev_text).split())

            overlap = stmt_keywords & ev_keywords
            if len(overlap) >= 2:
                # 检查是否有否定词
                neg_words = {"不", "否", "非", "未", "无", "没", "相反", "not", "no", "never"}
                if any(nw in ev_text for nw in neg_words):
                    contradict_count += 1
                else:
                    support_count += 1

        if support_count > contradict_count and support_count >= 1:
            stmt.verification_status = VerificationStatus.CONSISTENT
            stmt.confidence = min(0.85, stmt.confidence + 0.3)
        elif contradict_count > support_count and contradict_count >= 1:
            stmt.verification_status = VerificationStatus.CONFLICT
            stmt.confidence = max(0.15, stmt.confidence - 0.3)
        else:
            stmt.verification_status = VerificationStatus.UNVERIFIABLE

        return stmt

    @classmethod
    def _verify_quote(cls, stmt: VerifiableStatement) -> VerifiableStatement:
        """验证引述陈述"""
        # 提取引述内容
        quote_match = re.search(r'[""]([^"""]{5,200})[""]', stmt.text)
        if not quote_match:
            stmt.verification_status = VerificationStatus.UNVERIFIABLE
            return stmt

        quote_text = quote_match.group(1)

        # 检查证据中是否出现相同或相似表述
        for ev in stmt.evidence:
            ev_text = ev["title"] + " " + ev["snippet"]
            if quote_text in ev_text:
                stmt.verification_status = VerificationStatus.CONSISTENT
                stmt.confidence = min(0.9, stmt.confidence + 0.4)
                return stmt

        stmt.verification_status = VerificationStatus.UNVERIFIABLE
        return stmt

    @staticmethod
    def _correct_numeric_statement(
        original: str,
        stmt_value: float,
        evidence_value: float,
        evidence: Dict[str, str]
    ) -> str:
        """生成修正后的数字陈述"""
        # 用证据中的数字替换陈述中的数字
        corrected = re.sub(
            r'\d+\.?\d*',
            str(evidence_value),
            original,
            count=1
        )
        source_hint = f"（据{evidence.get('source', '网络来源')}修正）"
        return corrected + source_hint


# ==================== 输出修正器 ====================


class OutputCorrector:
    """
    根据验证结果修正LLM输出
    """

    @classmethod
    def correct(
        cls,
        original_output: str,
        statements: List[VerifiableStatement],
    ) -> Tuple[str, List[str]]:
        """
        修正输出中的冲突陈述

        Args:
            original_output: 原始输出
            statements: 验证后的陈述列表

        Returns:
            (修正后输出, 修正说明列表)
        """
        corrected_output = original_output
        corrections = []

        for stmt in statements:
            if stmt.verification_status == VerificationStatus.CONFLICT and stmt.corrected_text:
                # 用修正后的陈述替换原文
                old_text = stmt.text
                new_text = stmt.corrected_text
                if old_text in corrected_output:
                    corrected_output = corrected_output.replace(old_text, new_text, 1)
                    corrections.append(f"修正事实：{old_text[:50]}... → {new_text[:50]}...")

            elif stmt.verification_status == VerificationStatus.CONSISTENT and stmt.source_urls:
                # 一致陈述：标注来源（可选）
                pass

        return corrected_output, corrections


# ==================== 主验证器 ====================


class OutputVerifier:
    """
    输出验证器主类

    用法：
        verifier = OutputVerifier()
        result = verifier.verify_output(llm_output)
        print(result.verified_output)
    """

    def __init__(
        self,
        enable_verification: bool = True,
        max_statements: int = 10,
        max_results_per_stmt: int = 3,
    ):
        self.enable_verification = enable_verification
        self.max_statements = max_statements
        self._extractor = StatementExtractor()
        self._searcher = EvidenceSearcher(max_results_per_stmt)
        self._verifier = StatementVerifier()
        self._corrector = OutputCorrector()

    def verify_output(self, llm_output: str) -> VerificationResult:
        """
        验证LLM输出

        Args:
            llm_output: LLM的原始输出文本

        Returns:
            VerificationResult 验证结果
        """
        if not self.enable_verification:
            return VerificationResult(
                original_output=llm_output,
                verified_output=llm_output,
                statements=[],
                overall_confidence=1.0,
                needs_human_review=False,
                verification_summary="验证已禁用",
            )

        if not llm_output or not llm_output.strip():
            return VerificationResult(
                original_output=llm_output,
                verified_output=llm_output,
                statements=[],
                overall_confidence=1.0,
                needs_human_review=False,
                verification_summary="空输出，跳过验证",
            )

        # Step 1: 提取可验证陈述
        statements = self._extractor.extract(llm_output)
        if not statements:
            return VerificationResult(
                original_output=llm_output,
                verified_output=llm_output,
                statements=[],
                overall_confidence=0.8,  # 无客观事实陈述，中等置信度
                needs_human_review=False,
                verification_summary="未检测到可验证的客观事实陈述",
            )

        # 限制陈述数量
        statements = statements[:self.max_statements]

        # Step 2: 为每个陈述搜索证据
        for stmt in statements:
            self._searcher.search_evidence(stmt)

        # Step 3: 验证每个陈述
        for stmt in statements:
            self._verifier.verify(stmt)

        # Step 4: 修正输出
        corrected_output, corrections = self._corrector.correct(llm_output, statements)

        # Step 5: 计算整体置信度
        overall_confidence = self._calculate_overall_confidence(statements)

        # Step 6: 判断是否需要人工复核
        needs_human = self._needs_human_review(statements)

        # Step 7: 生成验证摘要
        summary = self._generate_summary(statements, corrections)

        return VerificationResult(
            original_output=llm_output,
            verified_output=corrected_output,
            statements=statements,
            overall_confidence=overall_confidence,
            needs_human_review=needs_human,
            verification_summary=summary,
        )

    @staticmethod
    def _calculate_overall_confidence(statements: List[VerifiableStatement]) -> float:
        """计算整体置信度"""
        if not statements:
            return 0.8

        consistent = sum(
            1 for s in statements
            if s.verification_status == VerificationStatus.CONSISTENT
        )
        conflict = sum(
            1 for s in statements
            if s.verification_status == VerificationStatus.CONFLICT
        )
        unverifiable = sum(
            1 for s in statements
            if s.verification_status == VerificationStatus.UNVERIFIABLE
        )

        # 加权平均
        total = len(statements)
        score = (consistent * 1.0 + unverifiable * 0.5) / total
        score -= conflict * 0.3 / total  # 冲突陈述扣分
        return max(0.1, min(0.95, score))

    @staticmethod
    def _needs_human_review(statements: List[VerifiableStatement]) -> bool:
        """判断是否需要人工复核"""
        # 规则1: 有冲突且无法自动修正
        for s in statements:
            if s.verification_status == VerificationStatus.CONFLICT and not s.corrected_text:
                return True

        # 规则2: 超过一半陈述无法验证
        unverifiable = sum(
            1 for s in statements
            if s.verification_status == VerificationStatus.UNVERIFIABLE
        )
        if unverifiable > len(statements) / 2:
            return True

        return False

    @staticmethod
    def _generate_summary(
        statements: List[VerifiableStatement],
        corrections: List[str],
    ) -> str:
        """生成验证摘要"""
        consistent = sum(
            1 for s in statements
            if s.verification_status == VerificationStatus.CONSISTENT
        )
        conflict = sum(
            1 for s in statements
            if s.verification_status == VerificationStatus.CONFLICT
        )
        unverifiable = sum(
            1 for s in statements
            if s.verification_status == VerificationStatus.UNVERIFIABLE
        )

        lines = [
            f"验证陈述总数: {len(statements)}",
            f"  ✓ 一致: {consistent}",
            f"  ✗ 冲突: {conflict}",
            f"  ? 无法验证: {unverifiable}",
        ]
        if corrections:
            lines.append(f"  修正项数: {len(corrections)}")
            for c in corrections:
                lines.append(f"    - {c}")

        return "\n".join(lines)

    def verify_and_store(
        self,
        llm_output: str,
        store_to_memory: bool = True,
    ) -> VerificationResult:
        """
        验证输出并存储验证结果到记忆系统

        Args:
            llm_output: LLM输出
            store_to_memory: 是否存储到记忆系统

        Returns:
            VerificationResult
        """
        result = self.verify_output(llm_output)

        if store_to_memory and result.statements:
            try:
                self._store_verification_result(result)
            except Exception as e:
                logger.warning(f"Failed to store verification result: {e}")

        return result

    @staticmethod
    def _store_verification_result(result: VerificationResult):
        """将验证结果存储到记忆系统"""
        try:
            from knowledge_cells.domain_nexus import DomainNexus
            nexus = DomainNexus()

            # 构建验证记录
            verification_record = {
                "type": "output_verification",
                "original_output_snippet": result.original_output[:200],
                "verified_output_snippet": result.verified_output[:200],
                "overall_confidence": result.overall_confidence,
                "needs_human_review": result.needs_human_review,
                "statement_count": len(result.statements),
                "consistent_count": sum(
                    1 for s in result.statements
                    if s.verification_status == VerificationStatus.CONSISTENT
                ),
                "conflict_count": sum(
                    1 for s in result.statements
                    if s.verification_status == VerificationStatus.CONFLICT
                ),
                "source_urls": [
                    url for s in result.statements for url in s.source_urls
                ][:5],
            }

            # 存储到知识库（作为验证记录）
            nexus.add_verification_record(verification_record)
            logger.info("Verification result stored to DomainNexus")

        except ImportError:
            logger.debug("DomainNexus not available, skipping memory storage")
        except Exception as e:
            logger.warning(f"Failed to store verification to memory: {e}")


# ==================== 全局快捷函数 ====================


_default_verifier: Optional[OutputVerifier] = None


def get_output_verifier() -> OutputVerifier:
    """获取全局OutputVerifier实例"""
    global _default_verifier
    if _default_verifier is None:
        _default_verifier = OutputVerifier()
    return _default_verifier


def verify_llm_output(llm_output: str) -> VerificationResult:
    """
    快捷函数：验证LLM输出

    Usage:
        result = verify_llm_output(llm_response_text)
        print(result.verified_output)  # 验证后的输出
        print(result.overall_confidence)  # 整体置信度
    """
    return get_output_verifier().verify_output(llm_output)


def verify_and_correct(llm_output: str) -> Tuple[str, float, bool]:
    """
    快捷函数：验证并修正LLM输出，返回修正后文本

    Returns:
        (修正后输出, 置信度, 是否需要人工复核)
    """
    result = verify_llm_output(llm_output)
    return (
        result.verified_output,
        result.overall_confidence,
        result.needs_human_review,
    )


# ==================== 测试用例 ====================


def _test_output_verifier():
    """内部测试"""
    verifier = OutputVerifier()

    # 测试含数字陈述的输出
    test_output_1 = """
    根据2024年数据，该公司营收达到15.8亿元，同比增长23.5%。
    市场规模为1200亿美元，主要竞争对手是A公司和B公司。
    """

    result1 = verifier.verify_output(test_output_1)
    print("=== 测试1: 含数字陈述 ===")
    print(f"陈述数: {len(result1.statements)}")
    for s in result1.statements:
        print(f"  [{s.stmt_type.value}] {s.verification_status.value}: {s.text[:50]}...")
    print(f"整体置信度: {result1.overall_confidence:.2f}")
    print(f"验证摘要:\n{result1.verification_summary}")

    # 测试含日期陈述的输出
    test_output_2 = """
    2024年3月15日，该公司发布了最新产品。
    昨日，股价上涨了5.2%。
    """

    result2 = verifier.verify_output(test_output_2)
    print("\n=== 测试2: 含日期陈述 ===")
    print(f"陈述数: {len(result2.statements)}")
    print(f"验证摘要:\n{result2.verification_summary}")


if __name__ == "__main__":
    _test_output_verifier()
