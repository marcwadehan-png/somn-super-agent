# -*- coding: utf-8 -*-
"""诗词分析引擎 - 核心类模块"""
import json
import re
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime

from ._pae_types import PoetryAnalysisLevel, PoetryStyle, PoetryAnalysisResult
from ._pae_resources import PoetryResourceLoader
from ._pae_basic import BasicAnalyzer
from ._pae_intermediate import IntermediateAnalyzer
from ._pae_advanced import AdvancedAnalyzer
from ._pae_scoring import PoetryScorer
from ._pae_comparison import PoetryComparator

__all__ = [
    'analyze_emotion',
    'analyze_imagery',
    'analyze_influence',
    'analyze_innovation',
    'analyze_language',
    'analyze_poem',
    'analyze_rhyme',
    'analyze_structure',
    'analyze_style',
    'analyze_theme',
    'batch_analysis',
    'compare_poems',
]

class PoetryAnalysisEngine:
    """诗词智能分析引擎核心类"""

    def __init__(self, analysis_level: PoetryAnalysisLevel = PoetryAnalysisLevel.ADVANCED):
        """
        init诗词分析引擎

        Args:
            analysis_level: 分析层级,默认为高级分析
        """
        self.analysis_level = analysis_level

        # 初始化组件
        self.resource_loader = PoetryResourceLoader()
        resources = self.resource_loader.load_all()

        # 初始化各层分析器
        self.basic_analyzer = BasicAnalyzer(resources["rhyme_rules"])
        self.intermediate_analyzer = IntermediateAnalyzer(
            resources["imagery_library"],
            resources["theme_library"]
        )
        self.advanced_analyzer = AdvancedAnalyzer(
            resources["author_style_library"],
            resources["imagery_library"]
        )
        self.scorer = PoetryScorer()
        self.comparator = PoetryComparator()

        # 存储资源引用（用于兼容）
        self.rhyme_rules = resources["rhyme_rules"]
        self.imagery_library = resources["imagery_library"]
        self.theme_library = resources["theme_library"]
        self.author_style_library = resources["author_style_library"]

        # 初始化分析器映射
        self.analyzers = {
            "basic": {
                "rhyme": self.basic_analyzer.analyze_rhyme,
                "structure": self.basic_analyzer.analyze_structure,
                "language": self.basic_analyzer.analyze_language
            },
            "intermediate": {
                "imagery": self.intermediate_analyzer.analyze_imagery,
                "emotion": self.intermediate_analyzer.analyze_emotion,
                "theme": self.intermediate_analyzer.analyze_theme
            },
            "advanced": {
                "style": self.advanced_analyzer.analyze_style,
                "influence": self.advanced_analyzer.analyze_influence,
                "innovation": self.advanced_analyzer.analyze_innovation
            }
        }

        # 尝试导入记忆编码器
        try:
            from src.neural_memory.memory_encoder import MemoryEncoder
            self.memory_encoder = MemoryEncoder()
        except ImportError:
            self.memory_encoder = None

        print(f"诗词智能分析引擎init完成,分析层级:{analysis_level.value}")

    def analyze_poem(self, poem_text: str, author: str = "", title: str = "") -> PoetryAnalysisResult:
        """
        分析单首诗词

        Args:
            poem_text: 诗词文本
            author: 作者姓名
            title: 诗词标题

        Returns:
            PoetryAnalysisResult: 分析结果
        """
        print(f"开始分析诗词:{title if title else '未命名作品'}")

        result = PoetryAnalysisResult(
            poem_id=self._generate_poem_id(poem_text, author),
            poem_title=title or "未命名作品",
            author=author or "未知作者",
            dynasty=self._infer_dynasty(author),
            original_text=poem_text,
            analysis_timestamp=self._get_current_timestamp()
        )

        # 执行基础分析
        result.basic_analysis = self._perform_basic_analysis(poem_text)

        # 根据分析层级执行不同深度的分析
        if self.analysis_level in [PoetryAnalysisLevel.INTERMEDIATE,
                                   PoetryAnalysisLevel.ADVANCED,
                                   PoetryAnalysisLevel.EXPERT]:
            result.intermediate_analysis = self._perform_intermediate_analysis(poem_text, author)

        if self.analysis_level in [PoetryAnalysisLevel.ADVANCED,
                                   PoetryAnalysisLevel.EXPERT]:
            result.advanced_analysis = self._perform_advanced_analysis(poem_text, author)

        # 计算synthesize评分
        result.comprehensive_score = self.scorer.calculate_comprehensive_score(result)

        # 存储到记忆系统
        self._store_analysis_to_memory(result)

        print(f"诗词分析完成:{title}")
        return result

    def _generate_poem_id(self, poem_text: str, author: str) -> str:
        """generate诗词唯一ID"""
        content = f"{author}_{poem_text[:50]}" if author else poem_text[:100]
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]

    def _infer_dynasty(self, author: str) -> str:
        """推断朝代"""
        tang_authors = ["李白", "杜甫", "王维", "孟浩然", "白居易", "李商隐", "杜牧", "王昌龄"]
        song_authors = ["苏轼", "辛弃疾", "李清照", "陆游", "柳永", "晏殊", "欧阳修"]

        if author in tang_authors:
            return "唐代"
        elif author in song_authors:
            return "宋代"
        else:
            return "未知朝代"

    def _get_current_timestamp(self) -> str:
        """get当前时间戳"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _perform_basic_analysis(self, poem_text: str) -> Dict[str, Any]:
        """执行基础分析"""
        return {
            "rhyme": self.basic_analyzer.analyze_rhyme(poem_text),
            "structure": self.basic_analyzer.analyze_structure(poem_text),
            "language": self.basic_analyzer.analyze_language(poem_text)
        }

    def _perform_intermediate_analysis(self, poem_text: str, author: str) -> Dict[str, Any]:
        """执行中级分析"""
        return {
            "imagery": self.intermediate_analyzer.analyze_imagery(poem_text),
            "emotion": self.intermediate_analyzer.analyze_emotion(poem_text),
            "theme": self.intermediate_analyzer.analyze_theme(poem_text)
        }

    def _perform_advanced_analysis(self, poem_text: str, author: str) -> Dict[str, Any]:
        """执行高级分析"""
        return {
            "style": self.advanced_analyzer.analyze_style(poem_text, author),
            "influence": self.advanced_analyzer.analyze_influence(poem_text, author),
            "innovation": self.advanced_analyzer.analyze_innovation(poem_text, author)
        }

    def _store_analysis_to_memory(self, result: PoetryAnalysisResult):
        """将分析结果存储到记忆系统"""
        if self.memory_encoder is None:
            return

        memory_data = {
            "type": "poetry_analysis",
            "content": result.to_dict(),
            "tags": ["诗词", "分析", result.author, result.dynasty],
            "timestamp": result.analysis_timestamp
        }

        try:
            self.memory_encoder.encode(memory_data)
            print(f"分析结果已存储到记忆系统:{result.poem_title}")
        except Exception as e:
            print(f"存储到记忆系统失败:{e}")

    def batch_analysis(self, poems_data: List[Dict[str, str]]) -> List[PoetryAnalysisResult]:
        """
        批量分析诗词

        Args:
            poems_data: 诗词数据列表,每个元素包含text,author,title

        Returns:
            List[PoetryAnalysisResult]: 分析结果列表
        """
        results = []

        print(f"开始批量分析诗词,共{len(poems_data)}首")

        for i, poem_data in enumerate(poems_data, 1):
            poem_text = poem_data.get("text", "")
            author = poem_data.get("author", "")
            title = poem_data.get("title", f"作品{i}")

            print(f"分析进度:{i}/{len(poems_data)} - {title}")

            try:
                result = self.analyze_poem(poem_text, author, title)
                results.append(result)
            except Exception as e:
                print(f"分析失败:{title} - {e}")

        print(f"批量分析完成,成功分析{len(results)}首诗词")
        return results

    def compare_poems(self, poem1: PoetryAnalysisResult, poem2: PoetryAnalysisResult) -> Dict[str, Any]:
        """
        比较两首诗词

        Args:
            poem1: 第一首诗词分析结果
            poem2: 第二首诗词分析结果

        Returns:
            Dict[str, Any]: 比较结果
        """
        return self.comparator.compare_poems(poem1, poem2)

    # ----- 兼容方法 -----

    def analyze_rhyme(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词韵律"""
        return self.basic_analyzer.analyze_rhyme(poem_text)

    def analyze_structure(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词结构"""
        return self.basic_analyzer.analyze_structure(poem_text)

    def analyze_language(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词语言characteristics"""
        return self.basic_analyzer.analyze_language(poem_text)

    def analyze_imagery(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词imagery"""
        return self.intermediate_analyzer.analyze_imagery(poem_text)

    def analyze_emotion(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词情感"""
        return self.intermediate_analyzer.analyze_emotion(poem_text)

    def analyze_theme(self, poem_text: str) -> Dict[str, Any]:
        """分析诗词主题"""
        return self.intermediate_analyzer.analyze_theme(poem_text)

    def analyze_style(self, poem_text: str, author: str) -> Dict[str, Any]:
        """分析诗词style"""
        return self.advanced_analyzer.analyze_style(poem_text, author)

    def analyze_influence(self, poem_text: str, author: str) -> Dict[str, Any]:
        """分析诗词影响"""
        return self.advanced_analyzer.analyze_influence(poem_text, author)

    def analyze_innovation(self, poem_text: str, author: str) -> Dict[str, Any]:
        """分析诗词创新性"""
        return self.advanced_analyzer.analyze_innovation(poem_text, author)
