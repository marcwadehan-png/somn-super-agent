# -*- coding: utf-8 -*-
"""
内容清洗引擎 - 标准化与降噪处理

功能:
- HTML标签/实体清洗
- 特殊字符与空白标准化
- 噪声过滤（广告/导航/页脚/水印等）
- 语言检测与分离
- 重复段落检测与合并
- 文本摘要化（超长文本截取核心内容）
- 敏感信息脱敏
- 知识条目标准化（统一输出格式）

版本: v1.0.0
创建: 2026-04-23
"""

from __future__ import annotations
import hashlib
import re
import logging
from typing import Dict, List, Optional, Any, Tuple, Set, Pattern
from dataclasses import dataclass, field
from datetime import datetime
from collections import OrderedDict

logger = logging.getLogger(__name__)


@dataclass
class CleanConfig:
    """清洗配置"""
    # 基础清洗
    strip_html: bool = True             # 移除HTML标签
    decode_entities: bool = True        # 解码HTML实体
    normalize_whitespace: bool = True   # 标准化空白字符
    remove_urls: bool = False           # 移除URL
    remove_emails: bool = False         # 移除邮箱
    normalize_punctuation: bool = True  # 统一中英文标点
    # 噪声过滤
    remove_ads: bool = True             # 移除广告文案
    remove_navigation: bool = True      # 移除导航文本
    remove_copyright: bool = True       # 移除版权声明
    min_paragraph_length: int = 10      # 最小段落长度（低于此值丢弃）
    max_paragraph_length: int = 10000   # 最大段落长度（超出截断）
    # 去重
    dedup_paragraphs: bool = True       # 段落去重
    similarity_threshold: float = 0.85  # 段落相似度阈值
    # 语言
    target_language: str = ""           # 目标语言（空=不过滤）
    min_chinese_ratio: float = 0.3      # 最小中文比例（仅中文内容源有效）
    # 脱敏
    mask_phone: bool = False            # 脱敏手机号
    mask_id_card: bool = False          # 脱敏身份证号
    mask_bank_card: bool = False        # 脱敏银行卡号
    # 长度限制
    max_content_length: int = 50000     # 最大内容长度
    # 摘要化
    summarize_long: bool = True         # 超长内容自动摘要
    summarize_threshold: int = 3000     # 触发摘要的长度阈值


@dataclass
class CleanResult:
    """清洗结果"""
    content: str = ""
    original_length: int = 0
    cleaned_length: int = 0
    reduction_ratio: float = 0.0
    paragraphs_removed: int = 0
    ads_removed: int = 0
    duplicates_removed: int = 0
    masked_count: int = 0
    language_detected: str = ""
    operations: List[str] = field(default_factory=list)


# ─────────────────────────────────────────
# 噪声模式（预编译正则）
# ─────────────────────────────────────────

# 广告文案模式
_AD_PATTERNS: List[Pattern] = [
    re.compile(r"(广告|推广|sponsored|advertisement|点击查看|立即下载|免费领取|优惠活动)", re.I),
    re.compile(r"(扫码关注|关注公众号|关注我们|扫码|二维码|follow\s+us)", re.I),
    re.compile(r"(分享到|转发|点赞|收藏|评论|更多精彩)", re.I),
    re.compile(r"(点击此处|click\s+here|了解更多|learn\s+more)", re.I),
]

# 导航文本模式
_NAV_PATTERNS: List[Pattern] = [
    re.compile(r"^(首页|上一页|下一页|尾页|返回|返回顶部|back\s+to\s+top)", re.I),
    re.compile(r"^(登录|注册|登录/注册|sign\s+in|sign\s+up|login|register)", re.I),
    re.compile(r"^(搜索|search|查找|find|菜单|menu|导航|navigation)", re.I),
    re.compile(r"^\d+\s*/\s*\d+\s*$"),  # 分页: "1 / 10"
]

# 版权声明模式
_COPYRIGHT_PATTERNS: List[Pattern] = [
    re.compile(r"(版权所有|all\s+rights?\s+reserved|copyright\s*[©@]?\s*\d{4})", re.I),
    re.compile(r"(本站|本文|本页面)\s*(不承担|不保证|不对|免责)", re.I),
    re.compile(r"(转载请注明|转载需|未经授权|unauthorized)", re.I),
    re.compile(r"(icp备|京公网|粤icp|备案号)\s*[\w\d\-]+", re.I),
]


class ContentCleaner:
    """内容清洗引擎

    对抓取到的原始内容进行多级清洗，输出高质量的标准文本。

    示例:
        cleaner = ContentCleaner()
        result = cleaner.clean(raw_html_content)
        logger.info(result.content)
    """

    def __init__(self, config: Optional[CleanConfig] = None):
        self.config = config or CleanConfig()

    def clean(self, content: str) -> CleanResult:
        """执行完整清洗流程

        流程: HTML解码 → 噪声过滤 → 去重 → 标准化 → 脱敏 → 摘要化
        """
        if not content:
            return CleanResult()

        result = CleanResult()
        result.original_length = len(content)
        text = content

        # Step 1: HTML解码
        if self.config.strip_html:
            text = self._strip_html(text)
            result.operations.append("strip_html")

        if self.config.decode_entities:
            text = self._decode_entities(text)
            result.operations.append("decode_entities")

        # Step 2: 段落分割与噪声过滤
        paragraphs = self._split_paragraphs(text)
        original_count = len(paragraphs)

        paragraphs = self._filter_noise(paragraphs, result)
        paragraphs = self._filter_length(paragraphs, result)

        # Step 3: 去重
        if self.config.dedup_paragraphs:
            paragraphs, dups = self._dedup_paragraphs(paragraphs)
            result.duplicates_removed = dups
            result.operations.append(f"dedup({dups} removed)")

        result.paragraphs_removed = original_count - len(paragraphs)

        # Step 4: 重新组装
        text = "\n\n".join(paragraphs)

        # Step 5: 标准化
        if self.config.normalize_whitespace:
            text = self._normalize_whitespace(text)
            result.operations.append("normalize_whitespace")

        if self.config.normalize_punctuation:
            text = self._normalize_punctuation(text)
            result.operations.append("normalize_punctuation")

        # Step 6: 移除URL/邮箱
        if self.config.remove_urls:
            text = self._remove_urls(text)
            result.operations.append("remove_urls")

        if self.config.remove_emails:
            text = self._remove_emails(text)
            result.operations.append("remove_emails")

        # Step 7: 脱敏
        if any([self.config.mask_phone, self.config.mask_id_card, self.config.mask_bank_card]):
            text, masked = self._mask_sensitive(text)
            result.masked_count = masked
            if masked > 0:
                result.operations.append(f"mask_sensitive({masked})")

        # Step 8: 语言检测与过滤
        if self.config.target_language or self.config.min_chinese_ratio > 0:
            text = self._filter_language(text, result)

        # Step 9: 长度截断
        if len(text) > self.config.max_content_length:
            text = text[:self.config.max_content_length]
            result.operations.append("truncate")

        # Step 10: 摘要化
        if self.config.summarize_long and len(text) > self.config.summarize_threshold:
            text = self._summarize(text)
            result.operations.append("summarize")

        result.content = text.strip()
        result.cleaned_length = len(result.content)
        result.reduction_ratio = (
            1 - result.cleaned_length / max(result.original_length, 1)
        )

        return result

    def clean_knowledge_item(self, content: str, source: str = "") -> str:
        """清洗单个知识条目，返回标准化文本"""
        result = self.clean(content)
        return result.content

    # ─────────────────────────────────────────
    # HTML 处理
    # ─────────────────────────────────────────

    @staticmethod
    def _strip_html(text: str) -> str:
        """移除HTML标签"""
        # 替换<br>为换行
        text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
        # 替换块级元素为换行
        text = re.sub(r"</(p|div|h[1-6]|li|tr|blockquote)>", "\n", text, flags=re.I)
        # 移除所有标签
        text = re.sub(r"<[^>]+>", "", text)
        return text

    @staticmethod
    def _decode_entities(text: str) -> str:
        """解码HTML实体"""
        # 常见实体
        entities = {
            "&nbsp;": " ", "&lt;": "<", "&gt;": ">", "&amp;": "&",
            "&quot;": '"', "&apos;": "'", "&mdash;": "—", "&ndash;": "–",
            "&hellip;": "...", "&copy;": "©", "&reg;": "®",
            r"&#(\d+);": lambda m: chr(int(m.group(1))),
            r"&#x([0-9a-fA-F]+);": lambda m: chr(int(m.group(1), 16)),
        }
        for pattern, replacement in entities.items():
            if callable(replacement):
                text = re.sub(pattern, replacement, text)
            else:
                text = text.replace(pattern, replacement)
        return text

    # ─────────────────────────────────────────
    # 段落处理
    # ─────────────────────────────────────────

    @staticmethod
    def _split_paragraphs(text: str) -> List[str]:
        """分割段落"""
        # 按多种分隔符分割
        paragraphs = re.split(r"\n\s*\n|\n{2,}", text)
        return [p.strip() for p in paragraphs if p.strip()]

    def _filter_noise(self, paragraphs: List[str], result: CleanResult) -> List[str]:
        """过滤噪声段落"""
        clean = []
        for para in paragraphs:
            is_noise = False

            # 广告检测
            if self.config.remove_ads:
                for pat in _AD_PATTERNS:
                    if pat.search(para):
                        result.ads_removed += 1
                        is_noise = True
                        break

            # 导航检测
            if not is_noise and self.config.remove_navigation:
                for pat in _NAV_PATTERNS:
                    if pat.match(para.strip()):
                        is_noise = True
                        break

            # 版权检测
            if not is_noise and self.config.remove_copyright:
                for pat in _COPYRIGHT_PATTERNS:
                    if pat.search(para):
                        is_noise = True
                        break

            # 纯数字/纯符号行
            if not is_noise and re.match(r"^[\d\s\-\.\,\+\*]+$", para.strip()):
                is_noise = True

            # 过短的段落（可能是碎片）
            if not is_noise and len(para.strip()) < self.config.min_paragraph_length:
                # 保留可能有意义的短标题
                if not re.match(r"^#+\s*.+", para.strip()):
                    is_noise = True

            if not is_noise:
                clean.append(para)

        return clean

    def _filter_length(self, paragraphs: List[str], result: CleanResult) -> List[str]:
        """过滤过长段落"""
        clean = []
        for para in paragraphs:
            if len(para) > self.config.max_paragraph_length:
                clean.append(para[:self.config.max_paragraph_length] + "...")
            else:
                clean.append(para)
        return clean

    def _dedup_paragraphs(self, paragraphs: List[str]) -> Tuple[List[str], int]:
        """段落去重（基于内容哈希和相似度）"""
        seen_hashes: Set[str] = set()
        unique = []
        removed = 0

        for para in paragraphs:
            # 精确哈希去重
            h = hashlib.md5(para.encode()).hexdigest()
            if h in seen_hashes:
                removed += 1
                continue

            # 相似度去重
            is_similar = False
            for existing in unique[-5:]:  # 只与最近5段比较
                sim = self._text_similarity(para, existing)
                if sim >= self.config.similarity_threshold:
                    removed += 1
                    is_similar = True
                    break

            if not is_similar:
                seen_hashes.add(h)
                unique.append(para)

        return unique, removed

    @staticmethod
    def _text_similarity(a: str, b: str) -> float:
        """简单文本相似度（基于n-gram重叠）"""
        if not a or not b:
            return 0.0
        # 3-gram
        def ngrams(s: str, n: int = 3) -> Set[str]:
            return {s[i:i+n] for i in range(len(s) - n + 1)}

        set_a = ngrams(a)
        set_b = ngrams(b)
        if not set_a or not set_b:
            return 0.0

        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        # ★ v1.2 修复: 防止 union 为 0 时 ZeroDivisionError（理论上 ngrams 已过滤空集，但双重保险）
        return intersection / union if union > 0 else 0.0

    # ─────────────────────────────────────────
    # 标准化
    # ─────────────────────────────────────────

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        """标准化空白字符"""
        # 多个空格变单空格
        text = re.sub(r"[ \t]+", " ", text)
        # 多个换行变双换行
        text = re.sub(r"\n{3,}", "\n\n", text)
        # 行首行尾空白
        text = "\n".join(line.strip() for line in text.split("\n"))
        return text.strip()

    @staticmethod
    def _normalize_punctuation(text: str) -> str:
        """统一标点符号"""
        # 全角转半角（保留中文标点）
        punct_map = {
            "：": "：",  # 中文冒号保留
            "，": "，",  # 中文逗号保留
            "。": "。",
            "！": "！",
            "？": "？",
            "；": "；",
            "（": "(",
            "）": ")",
            "【": "[",
            "】": "]",
            '"': '"',
            '"': '"',
            "'": "'",
            "'": "'",
        }
        # 英文环境中全角→半角
        # 但我们主要处理中文内容，保留中文标点
        # 只处理明显的不一致
        text = re.sub(r"\r\n", "\n", text)
        # 移除零宽字符
        text = re.sub(r"[\u200b\u200c\u200d\ufeff\u00ad]", "", text)
        return text

    @staticmethod
    def _remove_urls(text: str) -> str:
        """移除URL"""
        return re.sub(r"https?://[^\s<>\"')\]]+", "", text)

    @staticmethod
    def _remove_emails(text: str) -> str:
        """移除邮箱"""
        return re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "", text)

    # ─────────────────────────────────────────
    # 脱敏
    # ─────────────────────────────────────────

    def _mask_sensitive(self, text: str) -> Tuple[str, int]:
        """脱敏处理"""
        masked = 0

        if self.config.mask_phone:
            text, count = self._mask_pattern(
                text,
                r"1[3-9]\d{9}",
                lambda m: m.group()[:3] + "****" + m.group()[-4:],
            )
            masked += count

        if self.config.mask_id_card:
            text, count = self._mask_pattern(
                text,
                r"\b\d{17}[\dXx]\b",
                lambda m: m.group()[:6] + "********" + m.group()[-4:],
            )
            masked += count

        if self.config.mask_bank_card:
            text, count = self._mask_pattern(
                text,
                r"\b\d{16,19}\b",
                lambda m: m.group()[:4] + " **** **** " + m.group()[-4:],
            )
            masked += count

        return text, masked

    @staticmethod
    def _mask_pattern(text: str, pattern: str, replacer) -> Tuple[str, int]:
        """通用模式替换脱敏"""
        count = 0

        def _replace(m):
            nonlocal count
            count += 1
            return replacer(m)

        text = re.sub(pattern, _replace, text)
        return text, count

    # ─────────────────────────────────────────
    # 语言过滤
    # ─────────────────────────────────────────

    def _filter_language(self, text: str, result: CleanResult) -> str:
        """语言检测与过滤"""
        chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
        total_chars = len(re.findall(r"\w", text))

        if total_chars == 0:
            return text

        chinese_ratio = chinese_chars / total_chars
        result.language_detected = "zh-CN" if chinese_ratio > 0.3 else "en"

        if self.config.min_chinese_ratio > 0 and chinese_ratio < self.config.min_chinese_ratio:
            # 过滤掉非中文段落
            paragraphs = self._split_paragraphs(text)
            filtered = [p for p in paragraphs if len(re.findall(r"[\u4e00-\u9fff]", p)) / max(len(re.findall(r"\w", p)), 1) >= self.config.min_chinese_ratio]
            text = "\n\n".join(filtered)
            result.operations.append(f"language_filter(zh_ratio={chinese_ratio:.2f})")

        return text

    # ─────────────────────────────────────────
    # 摘要化
    # ─────────────────────────────────────────

    def _summarize(self, text: str) -> str:
        """基于位置和长度的启发式摘要

        策略: 保留开头和结尾段落（通常包含核心信息），中间部分抽样保留。
        """
        paragraphs = self._split_paragraphs(text)
        if len(paragraphs) <= 10:
            return text

        target_count = max(10, int(len(paragraphs) * 0.5))

        # 开头3段
        head = paragraphs[:3]
        # 结尾3段
        tail = paragraphs[-3:]
        # 中间均匀抽样
        middle_pool = paragraphs[3:-3]
        middle_count = target_count - len(head) - len(tail)
        if middle_count > 0 and middle_pool:
            step = max(1, len(middle_pool) // middle_count)
            middle = middle_pool[::step][:middle_count]
        else:
            middle = []

        return "\n\n".join(head + middle + tail)


__all__ = [
    'ContentCleaner',
    'CleanConfig',
    'CleanResult',
]
