# -*- coding: utf-8 -*-
"""
DivineReason 引擎自动发现与注册系统
====================================

自动扫描项目中所有引擎并注册到引擎网络。

功能：
- 自动发现引擎
- 智能分类
- 批量注册
- 元数据提取

版本: V1.0.0
创建: 2026-04-28
"""

import logging
import os
import re
from typing import Dict, List, Optional, Any, Tuple, Callable
from pathlib import Path
import importlib
import inspect

from ._engine_network import (
    EngineNetwork,
    EngineCategory,
    EngineMetadata,
    EngineNode,
    NetworkConfig,
    create_engine_network,
    EngineStatus
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 引擎扫描器
# ═══════════════════════════════════════════════════════════════════════════════

class EngineScanner:
    """
    引擎扫描器 - 自动发现项目中的引擎
    
    扫描规则：
    1. 文件名模式：*_engine.py, *_wisdom.py, *_core.py
    2. 类名模式：*Engine, *Wisdom, *Core, *Intelligence
    3. 目录扫描：engines/, reasoning/, wisdom_*/
    """
    
    # 引擎类型到分类的映射
    CATEGORY_MAPPING = {
        'philosophy': EngineCategory.PHILOSOPHY,
        'military': EngineCategory.MILITARY,
        'psychology': EngineCategory.PSYCHOLOGY,
        'management': EngineCategory.MANAGEMENT,
        'economics': EngineCategory.ECONOMICS,
        'literature': EngineCategory.LITERATURE,
        'science': EngineCategory.SCIENCE,
        'history': EngineCategory.HISTORY,
        'politics': EngineCategory.POLITICS,
        'religion': EngineCategory.RELIGION,
        'math': EngineCategory.MATH,
        'neuro': EngineCategory.NEURO,
        'culture': EngineCategory.CULTURE,
        'cross_culture': EngineCategory.CROSS_CULTURE,
        'reasoning': EngineCategory.REASONING,
        'learning': EngineCategory.LEARNING,
        'memory': EngineCategory.MEMORY,
        'cloning': EngineCategory.CLONING,
        'composite': EngineCategory.COMPOSITE,
        'fusion': EngineCategory.FUSION,
    }
    
    # 引擎文件模式
    ENGINE_PATTERNS = [
        r'^(.+)_engine\.py$',
        r'^(.+)_wisdom(_.*)?\.py$',
        r'^(.+)_core\.py$',
        r'^(.+)_intelligence\.py$',
        r'^(.+)_system\.py$',
    ]
    
    # 引擎类名模式
    CLASS_PATTERNS = [
        r'(.+Engine)',
        r'(.+Wisdom)',
        r'(.+Core)',
        r'(.+Intelligence)',
        r'(.+System)',
    ]
    
    # 能力关键词
    CAPABILITY_KEYWORDS = {
        'analysis': ['分析', '研究', 'analyze', 'research'],
        'strategy': ['战略', '策略', 'strategy', 'tactic'],
        'emotion': ['情绪', '情感', 'emotion', 'feeling'],
        'creativity': ['创意', '创造', 'creative', 'innovation'],
        'learning': ['学习', 'learn', 'growth'],
        'memory': ['记忆', 'memory', 'recall'],
        'decision': ['决策', 'decision', 'choice'],
        'communication': ['沟通', '交流', 'communication', 'dialogue'],
        'planning': ['规划', '计划', 'planning', 'plan'],
        'evaluation': ['评估', '评价', 'evaluate', 'assess'],
    }
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.discovered_engines: List[Dict[str, Any]] = []
    
    def scan(self, 
             directories: Optional[List[str]] = None,
             recursive: bool = True) -> List[Dict[str, Any]]:
        """
        扫描引擎
        
        Args:
            directories: 要扫描的目录列表
            recursive: 是否递归扫描
        
        Returns:
            发现的引擎列表
        """
        if directories is None:
            directories = ['engines', 'reasoning', 'wisdom_encoding']
        
        self.discovered_engines = []
        
        for dir_name in directories:
            dir_path = self.base_path / dir_name
            if not dir_path.exists():
                logger.warning(f"Directory not found: {dir_path}")
                continue
            
            if recursive:
                self._scan_recursive(dir_path, dir_name)
            else:
                self._scan_directory(dir_path, dir_name)
        
        logger.info(f"Discovered {len(self.discovered_engines)} engines")
        return self.discovered_engines
    
    def _scan_directory(self, path: Path, relative_path: str):
        """扫描单个目录"""
        for file_path in path.glob('*.py'):
            if file_path.name.startswith('_'):
                continue
            
            engine_info = self._analyze_file(file_path, relative_path)
            if engine_info:
                self.discovered_engines.append(engine_info)
    
    def _scan_recursive(self, path: Path, relative_path: str):
        """递归扫描"""
        for item in path.iterdir():
            if item.is_dir():
                sub_relative = f"{relative_path}/{item.name}"
                if item.name not in ['__pycache__', 'data', 'claws', 'tests']:
                    self._scan_recursive(item, sub_relative)
            elif item.suffix == '.py' and not item.name.startswith('_'):
                engine_info = self._analyze_file(item, relative_path)
                if engine_info:
                    self.discovered_engines.append(engine_info)
    
    def _analyze_file(self, file_path: Path, relative_path: str) -> Optional[Dict[str, Any]]:
        """分析引擎文件"""
        filename = file_path.stem  # 不带扩展名的文件名
        
        # 检查是否匹配引擎模式
        engine_match = None
        for pattern in self.ENGINE_PATTERNS:
            match = re.match(pattern, filename, re.IGNORECASE)
            if match:
                engine_match = match.group(1)
                break
        
        if not engine_match:
            return None
        
        # 确定分类
        category = self._infer_category(filename, relative_path)
        
        # 提取引擎信息
        engine_id = self._generate_engine_id(filename)
        name = self._format_name(engine_match)
        description = self._extract_description(file_path)
        capabilities = self._extract_capabilities(filename, description)
        triggers = self._extract_triggers(filename, description)
        
        return {
            'engine_id': engine_id,
            'name': name,
            'filename': filename,
            'file_path': str(file_path),
            'relative_path': relative_path,
            'category': category,
            'description': description,
            'capabilities': capabilities,
            'triggers': triggers,
            'quality_score': 0.5,  # 默认质量
            'reliability': 0.8,    # 默认可靠性
        }
    
    def _infer_category(self, filename: str, relative_path: str) -> EngineCategory:
        """推断引擎分类"""
        # 先检查路径
        path_lower = relative_path.lower()
        for key, category in self.CATEGORY_MAPPING.items():
            if key in path_lower:
                return category
        
        # 再检查文件名
        filename_lower = filename.lower()
        for key, category in self.CATEGORY_MAPPING.items():
            if key in filename_lower:
                return category
        
        # 默认分类
        return EngineCategory.COMPOSITE
    
    def _generate_engine_id(self, filename: str) -> str:
        """生成引擎ID"""
        # 移除后缀
        engine_id = re.sub(r'(_engine|_wisdom|_core|_intelligence|_system)$', '', 
                          filename, flags=re.IGNORECASE)
        # 转为小写，用下划线分隔
        engine_id = re.sub(r'([A-Z])', r'_\1', engine_id).lower().strip('_')
        return engine_id
    
    def _format_name(self, name: str) -> str:
        """格式化引擎名称"""
        # 转为Title Case
        return ' '.join(word.capitalize() for word in re.split(r'[_\s]+', name))
    
    def _extract_description(self, file_path: Path) -> str:
        """提取引擎描述"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 查找文档字符串
            doc_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            if doc_match:
                doc = doc_match.group(1).strip()
                # 取第一段或前200字符
                first_para = doc.split('\n\n')[0]
                return first_para[:200].strip()
            
            # 查找注释
            comment_match = re.search(r'#.*?$', content, re.MULTILINE)
            if comment_match:
                return comment_match.group(0).lstrip('#').strip()[:200]
        
        except Exception as e:
            logger.debug(f"Failed to extract description from {file_path}: {e}")
        
        return file_path.stem
    
    def _extract_capabilities(self, filename: str, description: str) -> List[str]:
        """提取能力列表"""
        capabilities = []
        text = f"{filename} {description}".lower()
        
        for cap, keywords in self.CAPABILITY_KEYWORDS.items():
            if any(kw.lower() in text for kw in keywords):
                capabilities.append(cap)
        
        return capabilities if capabilities else ['general']
    
    def _extract_triggers(self, filename: str, description: str) -> List[str]:
        """提取触发关键词"""
        triggers = []
        
        # 从文件名提取
        words = re.split(r'[_\-]', filename)
        triggers.extend([w.lower() for w in words if len(w) > 2])
        
        # 从描述提取
        if description:
            # 提取中文词
            chinese_words = re.findall(r'[\u4e00-\u9fff]+', description)
            triggers.extend([w.lower() for w in chinese_words if len(w) > 1])
        
        # 去重并限制数量
        triggers = list(set(triggers))[:20]
        return triggers


# ═══════════════════════════════════════════════════════════════════════════════
# 引擎注册器
# ═══════════════════════════════════════════════════════════════════════════════

class EngineRegistrar:
    """
    引擎注册器 - 将发现的引擎注册到网络
    """
    
    def __init__(self, network: EngineNetwork):
        self.network = network
        self.registered_count = 0
        self.failed_count = 0
        self.errors: List[Dict[str, Any]] = []
    
    def register_discovered(self, 
                           discovered_engines: List[Dict[str, Any]],
                           create_executor: Optional[Callable] = None) -> Tuple[int, int]:
        """
        注册发现的引擎
        
        Args:
            discovered_engines: 扫描发现的引擎列表
            create_executor: 创建执行器的函数(engine_info) -> callable
        
        Returns:
            (成功数量, 失败数量)
        """
        self.registered_count = 0
        self.failed_count = 0
        self.errors = []
        
        for engine_info in discovered_engines:
            try:
                self._register_single(engine_info, create_executor)
                self.registered_count += 1
            except Exception as e:
                self.failed_count += 1
                self.errors.append({
                    'engine': engine_info.get('name', 'unknown'),
                    'error': str(e)
                })
                logger.error(f"Failed to register {engine_info.get('name')}: {e}")
        
        return self.registered_count, self.failed_count
    
    def _register_single(self, 
                         engine_info: Dict[str, Any],
                         create_executor: Optional[Callable] = None):
        """注册单个引擎"""
        # 创建执行器（如果提供）
        executor = None
        if create_executor:
            executor = create_executor(engine_info)
        
        # 注册到网络
        self.network.register_engine(
            engine_id=engine_info['engine_id'],
            name=engine_info['name'],
            description=engine_info['description'],
            category=engine_info['category'],
            capabilities=engine_info.get('capabilities', []),
            triggers=engine_info.get('triggers', []),
            executor=executor,
            file_path=engine_info.get('file_path', ''),
            quality_score=engine_info.get('quality_score', 0.5),
            reliability=engine_info.get('reliability', 0.8)
        )


# ═══════════════════════════════════════════════════════════════════════════════
# 引擎网络构建器
# ═══════════════════════════════════════════════════════════════════════════════

class EngineNetworkBuilder:
    """
    引擎网络构建器 - 完整构建流程
    
    用法:
        builder = EngineNetworkBuilder(base_path)
        network = builder.build()
        stats = builder.get_statistics()
    """
    
    def __init__(self, base_path: str, config: Optional[NetworkConfig] = None):
        self.base_path = base_path
        self.config = config or NetworkConfig()
        
        self.network = create_engine_network(self.config)
        self.scanner = EngineScanner(base_path)
        self.registrar = EngineRegistrar(self.network)
        
        self._statistics: Dict[str, Any] = {}
    
    def scan(self, 
             directories: Optional[List[str]] = None,
             recursive: bool = True) -> 'EngineNetworkBuilder':
        """扫描引擎"""
        self.discovered_engines = self.scanner.scan(directories, recursive)
        return self
    
    def register(self,
                create_executor: Optional[Callable] = None) -> 'EngineNetworkBuilder':
        """注册引擎"""
        if not hasattr(self, 'discovered_engines'):
            self.scan()
        
        self.registrar.register_discovered(self.discovered_engines, create_executor)
        return self
    
    def build(self) -> EngineNetwork:
        """构建并返回网络"""
        # 如果还没有注册，先执行
        if self.registrar.registered_count == 0 and self.registrar.failed_count == 0:
            self.register()
        
        # 生成统计
        self._statistics = self._generate_statistics()
        
        logger.info(f"EngineNetwork built: {self.registrar.registered_count} engines registered")
        return self.network
    
    def _generate_statistics(self) -> Dict[str, Any]:
        """生成统计信息"""
        discovered = len(self.discovered_engines)
        registered = self.registrar.registered_count
        failed = self.registrar.failed_count
        
        # 按分类统计
        by_category: Dict[str, int] = {}
        for engine in self.discovered_engines:
            cat = engine['category'].value
            by_category[cat] = by_category.get(cat, 0) + 1
        
        return {
            'discovered': discovered,
            'registered': registered,
            'failed': failed,
            'success_rate': registered / max(discovered, 1),
            'by_category': by_category,
            'errors': self.registrar.errors[:10]  # 最多10个错误
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self._statistics:
            self._generate_statistics()
        return self._statistics
    
    def get_report(self) -> str:
        """生成报告"""
        stats = self.get_statistics()
        
        lines = [
            "=" * 60,
            "Engine Network Build Report",
            "=" * 60,
            f"Discovered: {stats['discovered']} engines",
            f"Registered: {stats['registered']} engines",
            f"Failed: {stats['failed']} engines",
            f"Success Rate: {stats['success_rate']:.1%}",
            "",
            "By Category:",
        ]
        
        for cat, count in sorted(stats['by_category'].items(), key=lambda x: -x[1]):
            lines.append(f"  {cat}: {count}")
        
        if stats['errors']:
            lines.append("")
            lines.append("Errors:")
            for err in stats['errors'][:5]:
                lines.append(f"  - {err['engine']}: {err['error']}")
        
        lines.append("=" * 60)
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════════════════

def build_engine_network(base_path: str,
                        directories: Optional[List[str]] = None,
                        config: Optional[NetworkConfig] = None) -> EngineNetwork:
    """
    构建引擎网络 - 一站式函数
    
    Args:
        base_path: 项目根目录
        directories: 要扫描的目录列表
        config: 网络配置
    
    Returns:
        构建好的引擎网络
    """
    builder = EngineNetworkBuilder(base_path, config)
    return builder.scan(directories).register().build()


def discover_and_register_engines(network: EngineNetwork,
                                   directories: List[str],
                                   base_path: str) -> Tuple[int, int]:
    """
    发现并注册引擎到现有网络
    
    Args:
        network: 已有引擎网络
        directories: 要扫描的目录
        base_path: 项目根目录
    
    Returns:
        (成功数量, 失败数量)
    """
    scanner = EngineScanner(base_path)
    discovered = scanner.scan(directories)
    
    registrar = EngineRegistrar(network)
    return registrar.register_discovered(discovered)
