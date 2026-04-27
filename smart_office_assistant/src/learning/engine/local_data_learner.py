"""
本地资料学习引擎
Local Data Learner

功能:
1. 扫描E盘所有文件
2. 智能分类文件类型
3. 提取关键信息
4. 建立索引
5. 调用对应学习引擎处理
"""

import os
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import logging
import re
import threading
from collections import defaultdict
import time

logger = logging.getLogger(__name__)

class FileType(Enum):
    """文件类型分类"""
    TEXT = "text"                    # 纯文本
    DOCUMENT = "document"            # 文档 (pdf, docx)
    CODE = "code"                    # 代码文件
    CONFIG = "config"                # 配置文件
    DATA = "data"                    # 数据文件 (csv, xlsx)
    KNOWLEDGE = "knowledge"          # 知识文件 (md, mindmap)
    ARCHIVE = "archive"              # 压缩包
    BINARY = "binary"                # 二进制文件
    UNKNOWN = "unknown"              # 未知类型

class FileCategory(Enum):
    """文件内容分类"""
    CODEBASE = "codebase"            # 代码库
    DOCUMENTATION = "documentation"  # 文档
    KNOWLEDGE = "knowledge"          # 知识库
    CONFIG = "config"                # 配置
    DATA = "data"                    # 数据
    ASSETS = "assets"                # 资源
    LOGS = "logs"                    # 日志
    TEMP = "temp"                    # 临时文件
    SYSTEM = "system"                # 系统文件

@dataclass
class FileInfo:
    """文件信息"""
    path: str
    size: int
    modified_time: str
    file_type: FileType
    file_category: FileCategory

    # 内容信息
    content_hash: Optional[str] = None
    preview: Optional[str] = None
    key_features: List[str] = field(default_factory=list)

    # 学习信息
    learned: bool = False
    learned_at: Optional[str] = None
    learning_score: float = 0.0

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LearningResult:
    """学习结果"""
    file_path: str
    success: bool
    insights: List[str] = field(default_factory=list)
    knowledge: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    processing_time: float = 0.0

class LocalDataLearner:
    """
    本地资料学习引擎

    核心功能:
    1. 文件扫描 - 遍历目标目录所有文件
    2. 智能分类 - 基于扩展名,路径,内容分类
    3. 内容提取 - 支持多种文件格式
    4. 索引建立 - 全文索引和语义索引
    5. 知识提取 - 从文件中提取知识
    """

    # 支持的文件扩展名
    SUPPORTED_EXTENSIONS = {
        FileType.TEXT: ['.txt', '.log', '.md'],
        FileType.DOCUMENT: ['.pdf', '.docx', '.doc'],
        FileType.CODE: ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.go', '.rs'],
        FileType.CONFIG: ['.yaml', '.yml', '.json', '.xml', '.toml', '.ini', '.cfg'],
        FileType.DATA: ['.csv', '.xlsx', '.xls', '.jsonl'],
        FileType.KNOWLEDGE: ['.md', '.mindmap', '.mermaid', '.drawio'],
        FileType.ARCHIVE: ['.zip', '.rar', '.7z', '.tar', '.gz'],
    }

    # 忽略的目录
    IGNORED_DIRS = {
        '.git', '.vscode', '.idea', 'node_modules', '__pycache__',
        'venv', 'env', '.venv', 'dist', 'build', 'target'
    }

    # 忽略的文件模式
    IGNORED_PATTERNS = [
        r'\.pyc$', r'\.pyo$', r'\.DS_Store$', r'\.gitignore$',
        r'\.gitmodules$', r'\.gitattributes$', r'\.bat$', r'\.sh$',
        r'\.spec$', r'\.egg-info$', r'\.pytest_cache$'
    ]

    def __init__(self, target_drive: str = "E:", base_path: Optional[str] = None):
        """
        init本地资料学习引擎

        Args:
            target_drive: 目标盘符 (如 "E:")
            base_path: 基础路径 (用于相对路径)
        """
        self.target_drive = target_drive
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent.parent.parent

        # 数据目录
        self.data_dir = self.base_path / "data" / "learning" / "local"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 索引文件
        self.index_file = self.data_dir / "index.json"
        self.knowledge_file = self.data_dir / "knowledge.json"
        self.progress_file = self.data_dir / "progress.json"

        # 文件索引
        self.file_index: Dict[str, FileInfo] = {}

        # 知识库
        self.knowledge_base: Dict[str, List[Dict]] = defaultdict(list)

        # 学习统计
        self.stats = {
            "total_files": 0,
            "learned_files": 0,
            "failed_files": 0,
            "total_size": 0,
            "total_time": 0.0,
            "by_type": defaultdict(int),
            "by_category": defaultdict(int)
        }

        # 线程锁
        self.index_lock = threading.Lock()

        # 加载索引
        self._load_index()

        logger.info(f"本地资料学习引擎init完成,目标: {target_drive}")

    def scan_directory(self, max_files: Optional[int] = None,
                       file_types: Optional[Set[FileType]] = None) -> List[FileInfo]:
        """
        扫描目标目录所有文件

        Args:
            max_files: 最大扫描文件数
            file_types: 文件类型过滤

        Returns:
            文件信息列表
        """
        logger.info(f"开始扫描目录: {self.target_drive}")

        files = []
        scanned_count = 0

        try:
            target_path = Path(self.target_drive)
            if not target_path.exists():
                logger.error(f"目标路径不存在: {self.target_drive}")
                return files

            for root, dirs, filenames in os.walk(self.target_drive):
                # 过滤忽略的目录
                dirs[:] = [d for d in dirs if d not in self.IGNORED_DIRS]

                for filename in filenames:
                    # 检查最大文件数
                    if max_files and scanned_count >= max_files:
                        logger.info(f"已达到最大文件数限制: {max_files}")
                        return files

                    file_path = Path(root) / filename

                    # 检查是否应该忽略
                    if self._should_ignore(filename):
                        continue

                    # get文件信息
                    file_info = self._get_file_info(file_path)

                    # 文件类型过滤
                    if file_types and file_info.file_type not in file_types:
                        continue

                    files.append(file_info)
                    scanned_count += 1

                    # 更新索引
                    with self.index_lock:
                        self.file_index[str(file_path)] = file_info

                    if scanned_count % 100 == 0:
                        logger.info(f"已扫描 {scanned_count} 个文件...")

        except Exception as e:
            logger.error(f"扫描目录失败: {e}")

        # 更新统计
        self.stats["total_files"] = len(self.file_index)
        self.stats["total_size"] = sum(f.size for f in self.file_index.values())

        # 保存索引
        self._save_index()

        logger.info(f"扫描完成,共找到 {len(files)} 个文件")
        return files

    def _should_ignore(self, filename: str) -> bool:
        """检查文件是否应该被忽略"""
        for pattern in self.IGNORED_PATTERNS:
            if re.search(pattern, filename, re.IGNORECASE):
                return True
        return False

    def _get_file_info(self, file_path: Path) -> FileInfo:
        """get文件信息"""
        try:
            stat = file_path.stat()
            size = stat.st_size
            modified_time = datetime.fromtimestamp(stat.st_mtime).isoformat()

            # judge文件类型
            file_type = self._classify_file_type(file_path)

            # judge文件类别
            file_category = self._classify_file_category(file_path, file_type)

            # 计算内容哈希(对于小文件)
            content_hash = None
            if size < 1024 * 100:  # 小于100KB
                content_hash = self._calculate_hash(file_path)

            # 预览内容
            preview = None
            if size < 1024 * 50 and file_type in [FileType.TEXT, FileType.CODE, FileType.KNOWLEDGE]:
                preview = self._extract_preview(file_path, max_chars=200)

            return FileInfo(
                path=str(file_path),
                size=size,
                modified_time=modified_time,
                file_type=file_type,
                file_category=file_category,
                content_hash=content_hash,
                preview=preview
            )

        except Exception as e:
            logger.error(f"get文件信息失败 {file_path}: {e}")
            return FileInfo(
                path=str(file_path),
                size=0,
                modified_time=datetime.now().isoformat(),
                file_type=FileType.UNKNOWN,
                file_category=FileCategory.UNKNOWN
            )

    def _classify_file_type(self, file_path: Path) -> FileType:
        """分类文件类型"""
        ext = file_path.suffix.lower()

        for file_type, extensions in self.SUPPORTED_EXTENSIONS.items():
            if ext in extensions:
                return file_type

        return FileType.UNKNOWN

    def _classify_file_category(self, file_path: Path, file_type: FileType) -> FileCategory:
        """分类文件类别"""
        path_str = str(file_path).lower()

        # 基于路径judge
        if 'doc' in path_str or 'readme' in path_str or 'guide' in path_str:
            return FileCategory.DOCUMENTATION
        elif 'data' in path_str or 'dataset' in path_str:
            return FileCategory.DATA
        elif 'config' in path_str or file_type == FileType.CONFIG:
            return FileCategory.CONFIG
        elif 'knowledge' in path_str or file_type == FileType.KNOWLEDGE:
            return FileCategory.KNOWLEDGE
        elif 'log' in path_str or file_type == FileType.TEXT:
            return FileCategory.LOGS
        elif 'temp' in path_str or 'tmp' in path_str:
            return FileCategory.TEMP
        elif file_type == FileType.CODE:
            return FileCategory.CODEBASE
        elif file_type == FileType.DATA:
            return FileCategory.DATA

        return FileCategory.UNKNOWN

    def _calculate_hash(self, file_path: Path) -> str:
        """计算文件哈希"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except (OSError, IOError, PermissionError):
            return None

    def _extract_preview(self, file_path: Path, max_chars: int = 200) -> str:
        """提取文件预览"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(max_chars)
                return content.replace('\n', ' ').strip()
        except (OSError, IOError, PermissionError):
            return None

    def learn_from_files(self, file_paths: List[str] = None,
                         max_files: int = None,
                         file_types: Set[FileType] = None) -> List[LearningResult]:
        """
        从文件学习

        Args:
            file_paths: 指定文件路径列表,None表示扫描所有
            max_files: 最大学习文件数
            file_types: 文件类型过滤

        Returns:
            学习结果列表
        """
        logger.info("开始从文件学习")

        # 如果未指定文件,则扫描目录
        if not file_paths:
            file_infos = self.scan_directory(max_files=max_files, file_types=file_types)
            file_paths = [f.path for f in file_infos]

        results = []
        learned_count = 0

        for file_path in file_paths:
            # 检查是否已学习
            if file_path in self.file_index and self.file_index[file_path].learned:
                continue

            # 学习文件
            result = self._learn_file(file_path)
            results.append(result)

            if result.success:
                learned_count += 1

            # 检查最大文件数
            if max_files and learned_count >= max_files:
                break

            # 更新统计
            self.stats["learned_files"] = learned_count

        # 保存进度
        self._save_progress()

        logger.info(f"学习完成,共学习 {learned_count} 个文件")
        return results

    def _learn_file(self, file_path: str) -> LearningResult:
        """学习单个文件"""
        start_time = time.time()
        result = LearningResult(file_path=file_path)

        try:
            file_info = self.file_index.get(file_path)
            if not file_info:
                # get文件信息
                file_path_obj = Path(file_path)
                if file_path_obj.exists():
                    file_info = self._get_file_info(file_path_obj)
                    self.file_index[file_path] = file_info
                else:
                    result.error = f"文件不存在: {file_path}"
                    return result

            # 根据文件类型提取知识
            if file_info.file_type == FileType.CODE:
                knowledge = self._extract_code_knowledge(file_path, file_info)
            elif file_info.file_type == FileType.KNOWLEDGE:
                knowledge = self._extract_knowledge_knowledge(file_path, file_info)
            elif file_info.file_type == FileType.CONFIG:
                knowledge = self._extract_config_knowledge(file_path, file_info)
            elif file_info.file_type == FileType.DOCUMENT:
                knowledge = self._extract_document_knowledge(file_path, file_info)
            else:
                knowledge = self._extract_general_knowledge(file_path, file_info)

            # generate洞察
            insights = self._generate_insights(knowledge)

            # 保存知识
            self._save_knowledge(file_path, knowledge)

            # 更新文件信息
            file_info.learned = True
            file_info.learned_at = datetime.now().isoformat()
            file_info.learning_score = self._calculate_learning_score(knowledge)

            # 更新统计
            self.stats["by_type"][file_info.file_type.value] += 1
            self.stats["by_category"][file_info.file_category.value] += 1

            result.success = True
            result.insights = insights
            result.knowledge = knowledge

        except Exception as e:
            result.error = f"学习失败"
            self.stats["failed_files"] += 1
            logger.error(f"学习文件失败 {file_path}: {e}")

        result.processing_time = time.time() - start_time
        return result

    def _extract_code_knowledge(self, file_path: str, file_info: FileInfo) -> Dict[str, Any]:
        """提取代码知识"""
        knowledge = {
            "type": "code",
            "language": self._detect_language(file_path),
            "functions": [],
            "classes": [],
            "imports": [],
            "patterns": [],
            "key_lines": []
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # 提取函数定义
                functions = re.findall(r'def\s+(\w+)\s*\(', content)
                knowledge["functions"] = functions[:20]  # 限制数量

                # 提取类定义
                classes = re.findall(r'class\s+(\w+)', content)
                knowledge["classes"] = classes[:20]

                # 提取导入
                imports = re.findall(r'import\s+(\w+)|from\s+(\w+)', content)
                knowledge["imports"] = [i[0] or i[1] for i in imports][:20]

                # 提取关键行(注释,TODO等)
                key_lines = re.findall(r'.*(TODO|FIXME|NOTE|HACK|XXX).*', content, re.IGNORECASE)
                knowledge["key_lines"] = key_lines[:10]

        except Exception as e:
            logger.error(f"提取代码知识失败 {file_path}: {e}")

        return knowledge

    def _extract_knowledge_knowledge(self, file_path: str, file_info: FileInfo) -> Dict[str, Any]:
        """提取知识文件知识"""
        knowledge = {
            "type": "knowledge",
            "structure": [],
            "key_concepts": [],
            "summaries": []
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # 提取标题(Markdown)
                headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
                knowledge["structure"] = headers[:20]

                # 提取关键概念(加粗或引用)
                concepts = re.findall(r'\*\*(.+?)\*\*|`(.+?)`', content)
                knowledge["key_concepts"] = [c[0] or c[1] for c in concepts][:20]

                # 提取段落摘要
                paragraphs = re.split(r'\n\n+', content)
                knowledge["summaries"] = [p.strip()[:100] for p in paragraphs[:5] if p.strip()]

        except Exception as e:
            logger.error(f"提取知识文件知识失败 {file_path}: {e}")

        return knowledge

    def _extract_config_knowledge(self, file_path: str, file_info: FileInfo) -> Dict[str, Any]:
        """提取配置文件知识"""
        knowledge = {
            "type": "config",
            "format": file_path.split('.')[-1],
            "keys": [],
            "sections": []
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                if file_path.endswith('.json'):
                    # JSON配置
                    data = json.loads(content)
                    knowledge["keys"] = list(data.keys())[:20]
                elif file_path.endswith(('.yaml', '.yml')):
                    # YAML配置
                    keys = re.findall(r'^\s*(\w+)\s*:', content, re.MULTILINE)
                    knowledge["keys"] = keys[:20]
                    sections = re.findall(r'^\s*#.*$', content, re.MULTILINE)
                    knowledge["sections"] = [s.strip('#').strip() for s in sections if s.strip()][:10]

        except Exception as e:
            logger.error(f"提取配置文件知识失败 {file_path}: {e}")

        return knowledge

    def _extract_document_knowledge(self, file_path: str, file_info: FileInfo) -> Dict[str, Any]:
        """提取文档知识(简化版,实际需要PDF/Word解析库)"""
        knowledge = {
            "type": "document",
            "format": file_path.split('.')[-1],
            "metadata": {}
        }

        # 简化处理,只记录文件信息
        knowledge["metadata"] = {
            "size": file_info.size,
            "modified": file_info.modified_time
        }

        return knowledge

    def _extract_general_knowledge(self, file_path: str, file_info: FileInfo) -> Dict[str, Any]:
        """提取通用知识"""
        knowledge = {
            "type": "general",
            "format": file_path.split('.')[-1],
            "preview": file_info.preview,
            "metadata": {
                "size": file_info.size,
                "modified": file_info.modified_time
            }
        }

        return knowledge

    def _generate_insights(self, knowledge: Dict[str, Any]) -> List[str]:
        """generate洞察"""
        insights = []

        knowledge_type = knowledge.get("type")

        if knowledge_type == "code":
            functions = knowledge.get("functions", [])
            classes = knowledge.get("classes", [])
            if functions:
                insights.append(f"定义了 {len(functions)} 个函数")
            if classes:
                insights.append(f"定义了 {len(classes)} 个类")
            if knowledge.get("key_lines"):
                insights.append(f"包含 {len(knowledge['key_lines'])} 个标记行(TODO/FIXME等)")

        elif knowledge_type == "knowledge":
            structure = knowledge.get("structure", [])
            if structure:
                insights.append(f"文档结构: {' -> '.join(structure[:5])}")
            concepts = knowledge.get("key_concepts", [])
            if concepts:
                insights.append(f"关键概念: {', '.join(concepts[:5])}")

        elif knowledge_type == "config":
            keys = knowledge.get("keys", [])
            if keys:
                insights.append(f"配置项: {len(keys)} 个")
                insights.append(f"主要配置: {', '.join(keys[:5])}")

        return insights[:3]  # 限制洞察数量

    def _calculate_learning_score(self, knowledge: Dict[str, Any]) -> float:
        """计算学习得分"""
        score = 0.0

        # 基于知识丰富度
        knowledge_type = knowledge.get("type")
        if knowledge_type == "code":
            functions = len(knowledge.get("functions", []))
            classes = len(knowledge.get("classes", []))
            score = (functions * 0.01 + classes * 0.02)  # 0-1之间
        elif knowledge_type == "knowledge":
            structure = len(knowledge.get("structure", []))
            concepts = len(knowledge.get("key_concepts", []))
            score = (structure * 0.05 + concepts * 0.03)
        elif knowledge_type == "config":
            keys = len(knowledge.get("keys", []))
            score = keys * 0.02

        return min(score, 1.0)

    def _save_knowledge(self, file_path: str, knowledge: Dict[str, Any]):
        """保存知识"""
        with self.index_lock:
            self.knowledge_base[file_path].append({
                "knowledge": knowledge,
                "timestamp": datetime.now().isoformat()
            })

    def _load_index(self):
        """加载索引"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for path, info_dict in data.items():
                        info = FileInfo(**info_dict)
                        self.file_index[path] = info
                logger.info(f"加载索引: {len(self.file_index)} 个文件")
            except Exception as e:
                logger.warning(f"加载索引失败: {e}")

    def _save_index(self):
        """保存索引"""
        try:
            data = {path: info.__dict__ for path, info in self.file_index.items()}
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存索引失败: {e}")

    def _save_progress(self):
        """保存进度"""
        try:
            data = {
                "stats": {
                    **self.stats,
                    "by_type": dict(self.stats["by_type"]),
                    "by_category": dict(self.stats["by_category"])
                },
                "timestamp": datetime.now().isoformat()
            }
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存进度失败: {e}")

    def get_statistics(self) -> Dict[str, Any]:
        """get学习统计"""
        return {
            "total_files": len(self.file_index),
            "learned_files": self.stats["learned_files"],
            "failed_files": self.stats["failed_files"],
            "total_size": self.stats["total_size"],
            "by_type": dict(self.stats["by_type"]),
            "by_category": dict(self.stats["by_category"]),
            "timestamp": datetime.now().isoformat()
        }

# 便捷函数
def create_local_learner(target_drive: str = "E:") -> LocalDataLearner:
    """创建本地资料学习引擎"""
    return LocalDataLearner(target_drive=target_drive)

__all__ = [
    'FileType', 'FileCategory', 'FileInfo', 'LearningResult',
    'LocalDataLearner', 'create_local_learner',
]
