# -*- coding: utf-8 -*-
"""
文档智能分析器 [v22.2 Phase 4]
Document Intelligence Analyzer

功能:
- 智能内容分析 - 提取关键信息
- 结构化数据提取 - 从表格中提取结构化数据
- 文档摘要生成 - 自动生成摘要
- 内容理解 - 理解文档语义结构
- 实体识别 - 识别人名/地名/组织等

版本: v22.2.0
日期: 2026-04-25
"""

from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EntityType(Enum):
    """实体类型"""
    PERSON = auto()      # 人名
    ORGANIZATION = auto() # 组织/公司
    LOCATION = auto()    # 地名
    DATE = auto()        # 日期
    TIME = auto()        # 时间
    MONEY = auto()       # 金额
    PERCENT = auto()     # 百分比
    EMAIL = auto()       # 邮箱
    PHONE = auto()       # 电话
    URL = auto()         # 网址
    PRODUCT = auto()     # 产品名
    PROJECT = auto()     # 项目名


@dataclass
class DocumentEntity:
    """文档实体"""
    text: str
    entity_type: EntityType
    confidence: float = 1.0
    start_pos: int = 0
    end_pos: int = 0


@dataclass
class DocumentSection:
    """文档章节"""
    title: str
    level: int  # 1=一级, 2=二级...
    content: str
    start_line: int = 0
    keywords: List[str] = field(default_factory=list)


@dataclass
class TableData:
    """表格数据"""
    headers: List[str]
    rows: List[List[str]]
    caption: str = ""
    row_count: int = 0
    col_count: int = 0


@dataclass
class DocumentSummary:
    """文档摘要"""
    title: str
    overview: str
    key_points: List[str]
    entities: List[DocumentEntity]
    sections: List[DocumentSection]
    tables: List[TableData]
    statistics: Dict[str, Any]
    word_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AnalysisResult:
    """分析结果"""
    success: bool
    summary: Optional[DocumentSummary] = None
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)


class EntityRecognizer:
    """
    实体识别器
    
    使用规则和模式匹配识别文本中的实体。
    
    示例:
    ```python
    recognizer = EntityRecognizer()
    entities = recognizer.recognize("张三和李四在2024年1月1日去了北京公司。")
    # -> [Entity("张三", PERSON), Entity("李四", PERSON), 
    #      Entity("2024年1月1日", DATE), Entity("北京", LOCATION)]
    ```
    """

    # 实体模式定义
    PATTERNS: Dict[EntityType, str] = {
        EntityType.DATE: r'(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?|\d{1,2}[-/月]\d{1,2}[日]?)',
        EntityType.TIME: r'(\d{1,2}[时:]\d{2}(分)?|\d{1,2}:\d{2})',
        EntityType.MONEY: r'([¥$€£]?\d+(?:,\d{3})*(?:\.\d{1,2})?(?:元|万|亿)?)',
        EntityType.PERCENT: r'(\d+(?:\.\d+)?%)',
        EntityType.EMAIL: r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        EntityType.PHONE: r'(\d{3,4}[-]?\d{7,8}|\d{11})',
        EntityType.URL: r'(https?://[^\s]+)',
    }

    # 中文姓名常见姓氏
    CHINESE_SURNAMES = set(
        '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻'
        '柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤'
        '滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵堪汪祁毛禹狄'
        '米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭'
        '梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓'
        '郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊於惠甄麴加封芮羿储靳汲邴糜松'
        '井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘'
        '景詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴郁胥能苍'
        '双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍舄璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄'
        '晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙'
        '东殴殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰巢关'
        '蒯相查后荆红游竺权逯盖益桓公万俟司马上官欧阳夏侯诸葛闻人东方赫连皇浦'
    )

    def __init__(self):
        self.compiled_patterns: Dict[EntityType, re.Pattern] = {
            etype: re.compile(pattern) 
            for etype, pattern in self.PATTERNS.items()
        }

    def recognize(self, text: str) -> List[DocumentEntity]:
        """识别文本中的实体"""
        entities = []
        
        # 模式匹配
        for etype, pattern in self.compiled_patterns.items():
            for match in pattern.finditer(text):
                entities.append(DocumentEntity(
                    text=match.group(),
                    entity_type=etype,
                    start_pos=match.start(),
                    end_pos=match.end()
                ))
        
        # 识别人名 (简单规则)
        entities.extend(self._recognize_persons(text))
        
        return sorted(entities, key=lambda e: e.start_pos)

    def _recognize_persons(self, text: str) -> List[DocumentEntity]:
        """识别人名"""
        persons = []
        # 匹配 2-4 个字的中文姓名
        pattern = re.compile(r'[ %s][\u4e00-\u9fa5]{1,3}(?=\s|$|[，,。.])' % ''.join(self.CHINESE_SURNAMES))
        
        for match in pattern.finditer(text):
            name = match.group().strip()
            if len(name) >= 2 and len(name) <= 4:
                persons.append(DocumentEntity(
                    text=name,
                    entity_type=EntityType.PERSON,
                    confidence=0.7,
                    start_pos=match.start(),
                    end_pos=match.end()
                ))
        
        return persons


class DocumentStructureAnalyzer:
    """
    文档结构分析器
    
    分析文档的语义结构，提取章节、标题、段落等。
    
    示例:
    ```python
    analyzer = DocumentStructureAnalyzer()
    sections = analyzer.analyze("# 主标题\\n\\n## 二级标题\\n\\n内容...")
    ```
    """

    # Markdown标题模式
    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    
    # Word标题样式关键词
    HEADING_KEYWORDS = [
        '章节', '第', '章', '节', '一、', '二、', '三、',
        '（一）', '（二）', '（三）',
        '1.', '1.1', '2.', '2.1', '3.'
    ]

    def __init__(self):
        self.entity_recognizer = EntityRecognizer()

    def analyze(self, content: str, format: str = 'markdown') -> List[DocumentSection]:
        """分析文档结构"""
        sections = []
        
        if format == 'markdown':
            sections = self._analyze_markdown(content)
        elif format == 'plain':
            sections = self._analyze_plain_text(content)
        else:
            sections = self._analyze_plain_text(content)
        
        # 为每个章节提取关键词
        for section in sections:
            section.keywords = self._extract_keywords(section.content)
        
        return sections

    def _analyze_markdown(self, content: str) -> List[DocumentSection]:
        """分析Markdown文档"""
        sections = []
        lines = content.split('\n')
        
        current_section = None
        current_content = []
        current_line = 0
        
        for i, line in enumerate(lines):
            match = self.HEADING_PATTERN.match(line)
            if match:
                # 保存之前的章节
                if current_section:
                    current_section.content = '\n'.join(current_content).strip()
                    sections.append(current_section)
                
                # 开始新章节
                level = len(match.group(1))
                title = match.group(2).strip()
                current_section = DocumentSection(
                    title=title,
                    level=level,
                    content='',
                    start_line=i
                )
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # 保存最后一个章节
        if current_section:
            current_section.content = '\n'.join(current_content).strip()
            sections.append(current_section)
        
        return sections

    def _analyze_plain_text(self, content: str) -> List[DocumentSection]:
        """分析纯文本文档"""
        sections = []
        lines = content.split('\n')
        
        current_title = "开头"
        current_level = 1
        current_content = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # 检查是否是标题
            is_heading = False
            for keyword in self.HEADING_KEYWORDS:
                if line.startswith(keyword) and len(line) < 50:
                    is_heading = True
                    break
            
            # 检查Markdown标题
            if line.startswith('#'):
                is_heading = True
            
            if is_heading and line:
                # 保存之前的章节
                if current_content:
                    sections.append(DocumentSection(
                        title=current_title,
                        level=current_level,
                        content='\n'.join(current_content).strip(),
                        start_line=i - len(current_content)
                    ))
                    current_content = []
                
                current_title = line
                current_level = self._estimate_level(line)
            else:
                current_content.append(line)
        
        # 保存最后一个章节
        if current_content:
            sections.append(DocumentSection(
                title=current_title,
                level=current_level,
                content='\n'.join(current_content).strip(),
                start_line=len(lines) - len(current_content)
            ))
        
        return sections

    def _estimate_level(self, title: str) -> int:
        """估算标题级别"""
        if title.startswith('######'):
            return 6
        elif title.startswith('#####'):
            return 5
        elif title.startswith('####'):
            return 4
        elif title.startswith('###'):
            return 3
        elif title.startswith('##'):
            return 2
        elif title.startswith('#'):
            return 1
        
        # 中文标题
        if title.startswith('第') and '章' in title:
            return 1
        elif any(title.startswith(k) for k in ['一、', '二、', '三、']):
            return 2
        elif title.startswith('（') and '）' in title:
            return 3
        
        return 1

    def _extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """提取关键词（简单实现）"""
        # 移除标点和停用词
        stop_words = {'的', '是', '在', '和', '了', '有', '我', '你', '他', '她', '它',
                     '这', '那', '个', '与', '对', '等', '到', '为', '以', '上', '下'}
        
        # 分词（简单按标点和空格分割）
        words = re.findall(r'[\u4e00-\u9fa5]+', text)
        
        # 统计词频
        word_freq = {}
        for word in words:
            if len(word) >= 2 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 返回top_n
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in sorted_words[:top_n]]


class TableExtractor:
    """
    表格数据提取器
    
    从文档中提取表格数据并转换为结构化格式。
    
    示例:
    ```python
    extractor = TableExtractor()
    tables = extractor.extract_from_markdown(content)
    for table in tables:
        print(f"表头: {table.headers}")
        print(f"行数: {table.row_count}")
    ```
    """

    # Markdown表格模式
    TABLE_PATTERN = re.compile(
        r'\|(.+?)\|[\r\n]+\|[-:\s|]+\|[\r\n]+(?:\|(.+?)\|[\r\n]+)+',
        re.MULTILINE
    )

    def extract_from_markdown(self, content: str) -> List[TableData]:
        """从Markdown提取表格"""
        tables = []
        
        for match in self.TABLE_PATTERN.finditer(content):
            table = self._parse_markdown_table(match.group())
            if table:
                tables.append(table)
        
        return tables

    def _parse_markdown_table(self, text: str) -> Optional[TableData]:
        """解析Markdown表格"""
        lines = text.strip().split('\n')
        
        if len(lines) < 3:
            return None
        
        # 解析表头
        headers = [h.strip() for h in lines[0].split('|') if h.strip()]
        
        # 跳过分隔行
        data_lines = lines[2:] if len(lines) > 2 else []
        
        # 解析数据行
        rows = []
        for line in data_lines:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if cells:
                rows.append(cells)
        
        if not headers:
            return None
        
        return TableData(
            headers=headers,
            rows=rows,
            row_count=len(rows),
            col_count=len(headers)
        )


class DocumentSummarizer:
    """
    文档摘要生成器
    
    为文档生成摘要和关键信息提取。
    
    示例:
    ```python
    summarizer = DocumentSummarizer()
    summary = summarizer.summarize(document_content)
    print(summary.overview)
    print(summary.key_points)
    ```
    """

    def __init__(self):
        self.entity_recognizer = EntityRecognizer()
        self.structure_analyzer = DocumentStructureAnalyzer()
        self.table_extractor = TableExtractor()

    def summarize(self, content: str, format: str = 'markdown') -> DocumentSummary:
        """生成文档摘要"""
        # 提取实体
        entities = self.entity_recognizer.recognize(content)
        
        # 分析结构
        sections = self.structure_analyzer.analyze(content, format)
        
        # 提取表格
        tables = self.table_extractor.extract_from_markdown(content)
        
        # 统计信息
        statistics = self._compute_statistics(content, sections, tables)
        
        # 生成概述
        overview = self._generate_overview(sections, statistics)
        
        # 提取关键点
        key_points = self._extract_key_points(sections, entities)
        
        # 生成标题
        title = self._generate_title(sections, content)
        
        return DocumentSummary(
            title=title,
            overview=overview,
            key_points=key_points,
            entities=entities,
            sections=sections,
            tables=tables,
            statistics=statistics,
            word_count=len(content)
        )

    def _compute_statistics(
        self, 
        content: str, 
        sections: List[DocumentSection],
        tables: List[TableData]
    ) -> Dict[str, Any]:
        """计算统计信息"""
        # 字符统计
        char_count = len(content)
        line_count = content.count('\n') + 1
        
        # 词频统计
        chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', content))
        english_words = len(re.findall(r'[a-zA-Z]+', content))
        numbers = len(re.findall(r'\d+', content))
        
        # 标点统计
        punct_count = len(re.findall(r'[，。、！？；：""''（）【】《》]', content))
        
        return {
            'char_count': char_count,
            'line_count': line_count,
            'chinese_chars': chinese_chars,
            'english_words': english_words,
            'numbers': numbers,
            'punct_count': punct_count,
            'section_count': len(sections),
            'table_count': len(tables),
            'entity_count': {
                'person': 0,
                'organization': 0,
                'location': 0,
                'date': 0,
                'money': 0,
                'other': 0
            }
        }

    def _generate_overview(self, sections: List[DocumentSection], stats: Dict) -> str:
        """生成文档概述"""
        if not sections:
            return f"文档包含 {stats['char_count']} 个字符，{stats['line_count']} 行。"
        
        # 使用第一个章节的内容生成概述
        first_section = sections[0]
        preview = first_section.content[:200]
        if len(first_section.content) > 200:
            preview += "..."
        
        return preview

    def _extract_key_points(
        self, 
        sections: List[DocumentSection],
        entities: List[DocumentEntity]
    ) -> List[str]:
        """提取关键点"""
        key_points = []
        
        # 从章节标题提取关键点
        for section in sections[:5]:  # 最多5个
            if section.level <= 2 and len(section.content) > 20:
                key_points.append(f"**{section.title}**: {section.content[:100]}...")
        
        # 从实体提取关键点
        person_entities = [e for e in entities if e.entity_type == EntityType.PERSON][:3]
        if person_entities:
            names = '、'.join(e.text for e in person_entities)
            key_points.append(f"涉及人物: {names}")
        
        return key_points[:7]  # 最多7个关键点

    def _generate_title(self, sections: List[DocumentSection], content: str) -> str:
        """生成文档标题"""
        if sections:
            for section in sections:
                if section.level == 1 and len(section.title) < 30:
                    return section.title
        
        # 使用第一行作为标题
        first_line = content.split('\n')[0].strip()
        if first_line:
            return first_line[:50]
        
        return "无标题文档"


class DocumentIntelligenceService:
    """
    文档智能分析服务
    
    整合所有智能分析功能，提供统一的文档理解接口。
    
    示例:
    ```python
    service = DocumentIntelligenceService()
    
    # 分析文档
    result = service.analyze("document.md")
    print(result.summary.title)
    print(result.summary.key_points)
    
    # 提取结构化数据
    tables = service.extract_tables("report.md")
    for table in tables:
        print(table.headers)
        print(table.rows)
    ```
    """

    def __init__(self):
        self.entity_recognizer = EntityRecognizer()
        self.structure_analyzer = DocumentStructureAnalyzer()
        self.table_extractor = TableExtractor()
        self.summarizer = DocumentSummarizer()

    def analyze(self, content: str, format: str = 'markdown') -> AnalysisResult:
        """
        全面分析文档
        
        Args:
            content: 文档内容
            format: 文档格式 (markdown, plain)
        
        Returns:
            AnalysisResult: 分析结果
        """
        try:
            summary = self.summarizer.summarize(content, format)
            return AnalysisResult(success=True, summary=summary)
        except Exception as e:
            logger.exception(f"文档分析失败")
            return AnalysisResult(success=False, error="文档分析失败")

    def analyze_file(self, file_path: Union[str, Path]) -> AnalysisResult:
        """
        分析文档文件
        
        Args:
            file_path: 文件路径
        
        Returns:
            AnalysisResult: 分析结果
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return AnalysisResult(success=False, error=f"文件不存在: {file_path}")
        
        try:
            content = file_path.read_text(encoding='utf-8')
            suffix = file_path.suffix.lower()
            
            if suffix == '.md':
                return self.analyze(content, 'markdown')
            else:
                return self.analyze(content, 'plain')
        except Exception as e:
            return AnalysisResult(success=False, error=f"读取失败: {e}")

    def extract_entities(self, text: str) -> List[DocumentEntity]:
        """提取实体"""
        return self.entity_recognizer.recognize(text)

    def extract_structure(self, content: str, format: str = 'markdown') -> List[DocumentSection]:
        """提取文档结构"""
        return self.structure_analyzer.analyze(content, format)

    def extract_tables(self, content: str) -> List[TableData]:
        """提取表格"""
        return self.table_extractor.extract_from_markdown(content)

    def generate_summary(self, content: str, format: str = 'markdown') -> DocumentSummary:
        """生成摘要"""
        return self.summarizer.summarize(content, format)


# 便捷函数
def analyze_document(content: str) -> AnalysisResult:
    """快速分析文档"""
    service = DocumentIntelligenceService()
    return service.analyze(content)


def extract_entities(text: str) -> List[DocumentEntity]:
    """快速提取实体"""
    recognizer = EntityRecognizer()
    return recognizer.recognize(text)


def extract_tables(content: str) -> List[TableData]:
    """快速提取表格"""
    extractor = TableExtractor()
    return extractor.extract_from_markdown(content)


def summarize_document(content: str) -> DocumentSummary:
    """快速生成摘要"""
    summarizer = DocumentSummarizer()
    return summarizer.summarize(content)
