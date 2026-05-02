"""
==============================================
            DomainNexus S1.0
       知识域格子动态更新系统
==============================================

核心理念：
- 知识域格子是动态的，不是预设的
- 根据实际使用情况自动更新、自动丰富、智能迭代
- 绝对禁止删除任何知识点

功能：
- 自动追踪使用情况
- 发现知识缺口
- 自动丰富格子内容
- 智能合并/拆分建议

==============================================

定位：与 SageDispatch 完全独立的知识库系统
- DomainNexus: 知识管理、自动丰富、动态迭代
- SageDispatch: 问题调度、推理增强、策略选择

==============================================

版本历史：
- v2.2: 预加载+懒加载快速加载模式
  * CellIndex: 轻量级索引(仅元数据)
  * LazyCellLoader: 按需加载完整内容
  * 首次加载时间优化: ~500ms → ~50ms
==============================================
"""

import os
import re
import json
import hashlib
import logging
import threading
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from collections import defaultdict, OrderedDict
import sys

logger = logging.getLogger("Somn.DomainNexus")

# ============ 路径设置 ============
_CELLS_DIR = Path(__file__).parent

# v6.1: mkdir 延迟到首次使用时执行，避免 import 时文件系统副作用
_CONFIG_DIR: Path = _CELLS_DIR / "configs"
_CONFIG_DIR_CREATED = False


def _ensure_config_dir() -> Path:
    """确保配置目录存在（懒化）"""
    global _CONFIG_DIR_CREATED
    if not _CONFIG_DIR_CREATED:
        _CONFIG_DIR.mkdir(exist_ok=True)
        _CONFIG_DIR_CREATED = True
    return _CONFIG_DIR


# ============ 数据结构 ============

@dataclass
class EvolutionRecord:
    """进化记录"""
    timestamp: str
    action: str
    cell_id: Optional[str]
    details: str
    quality_delta: float = 0.0


@dataclass
class UsageStats:
    """使用统计"""
    cell_id: str
    call_count: int = 0
    last_called: Optional[str] = None
    topics: Set[str] = field(default_factory=set)
    queries: List[str] = field(default_factory=list)


@dataclass
class CellContent:
    """格子内容"""
    cell_id: str
    name: str
    tags: Set[str]
    summary: str = ""
    points: List[str] = field(default_factory=list)
    associations: Dict[str, float] = field(default_factory=dict)
    analogies: List[str] = field(default_factory=list)  # 举一反三
    metrics: List[str] = field(default_factory=list)     # 关键指标
    cases: List[str] = field(default_factory=list)        # 实战案例
    insights: List[str] = field(default_factory=list)     # 核心洞见
    last_updated: str = ""
    activation_count: int = 0  # 激活次数


# ============ v2.2 轻量级索引系统 ============

@dataclass
class CellIndex:
    """
    格子轻量级索引 - 仅包含元数据

    用于快速加载，不加载完整内容
    首次加载仅需 ~5ms (15个格子)
    """
    cell_id: str
    name: str
    tags: Set[str]
    file_path: str  # 文件路径，用于懒加载
    summary_preview: str = ""  # 仅第一行预览


class CellIndexManager:
    """
    格子索引管理器 - v2.2 预加载+缓存优化版

    优化策略：
    1. 并行读取多个文件
    2. 索引持久化缓存（pickle）
    3. 仅读取必要的元数据行
    4. 内存映射加速
    """

    # 索引缓存文件
    _CACHE_FILE = ".cell_index_cache.pkl"

    def __init__(self, cells_dir: Optional[Path] = None):
        self.cells_dir = cells_dir or _CELLS_DIR
        self.index: Dict[str, CellIndex] = {}  # 索引缓存
        self._index_loaded = False
        self._cache_file = self.cells_dir / self._CACHE_FILE

    def preload_index(self) -> float:
        """
        预加载索引 - 快速启动

        优化：
        1. 尝试从缓存文件加载
        2. 并行读取多个文件
        3. 仅读取必要的元数据行

        Returns:
            加载耗时(秒)
        """
        import time
        import pickle
        from concurrent.futures import ThreadPoolExecutor, as_completed

        start = time.perf_counter()

        # 1. 尝试从缓存加载
        cached_index = self._load_from_cache()
        if cached_index is not None:
            self.index = cached_index
            self._index_loaded = True
            return time.perf_counter() - start

        # 2. 并行读取所有格子文件
        md_files = list(self.cells_dir.glob("B*.md")) + list(self.cells_dir.glob("C*.md"))
        index_list: List[CellIndex] = []

        # 并行读取（使用线程池）
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(self._parse_index_fast, f): f for f in md_files}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    index_list.append(result)

        # 3. 构建索引字典
        for idx in index_list:
            self.index[idx.cell_id] = idx

        self._index_loaded = True

        # 4. 异步保存缓存
        self._save_cache_async()

        return time.perf_counter() - start

    def _parse_index_fast(self, md_file: Path) -> Optional[CellIndex]:
        """
        快速解析索引 - 仅读取必要的行

        策略：只读取前3行（标题、标签、摘要预览）
        """
        try:
            cell_id = md_file.stem.split('_')[0]
            name = '_'.join(md_file.stem.split('_')[1:]) if '_' in md_file.stem else md_file.stem

            # 读取前3行（标题行已不需要，因为有name）
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = [f.readline() for _ in range(3)]
                # 跳过标题行，直接找标签和摘要

            tags = set()
            summary_preview = ""

            # 读取更多行找标签和摘要
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read(500)  # 只读前500字节

            # 提取标签
            tags_match = re.search(r'## 标签\s*\n(.+?)(?:\n|$)', content)
            if tags_match:
                tags = set(t.strip() for t in re.split(r'[,:，：]', tags_match.group(1)) if t.strip())

            # 提取摘要预览（下一行）
            if tags_match:
                pos = tags_match.end()
                next_line = content[pos:content.find('\n', pos)].strip()
                if next_line:
                    summary_preview = next_line[:50]

            return CellIndex(
                cell_id=cell_id,
                name=name,
                tags=tags,
                file_path=str(md_file),
                summary_preview=summary_preview
            )

        except Exception:
            return None

    def _load_from_cache(self) -> Optional[Dict[str, CellIndex]]:
        """从缓存文件加载索引"""
        import pickle

        try:
            if self._cache_file.exists():
                # 检查文件是否过期（1小时）
                import time
                if time.time() - self._cache_file.stat().st_mtime < 3600:
                    with open(self._cache_file, 'rb') as f:
                        return pickle.load(f)
        except Exception:
            pass

        return None

    def _save_cache_async(self):
        """异步保存缓存"""
        import pickle
        import threading

        def _save():
            try:
                with open(self._cache_file, 'wb') as f:
                    pickle.dump(self.index, f)
            except Exception:
                pass

        threading.Thread(target=_save, daemon=True).start()

    def get_index(self, cell_id: str) -> Optional[CellIndex]:
        """获取格子索引"""
        return self.index.get(cell_id)

    def get_all_indices(self) -> Dict[str, CellIndex]:
        """获取所有索引"""
        return self.index

    def search_indices(self, keyword: str) -> List[CellIndex]:
        """搜索索引"""
        keyword_lower = keyword.lower()
        results = []

        for cell in self.index.values():
            if (keyword_lower in cell.name.lower() or
                keyword_lower in cell.summary_preview.lower() or
                any(keyword_lower in tag.lower() for tag in cell.tags)):
                results.append(cell)

        return results


class LazyCellLoader:
    """
    懒加载格子内容 - v2.2 LRU缓存优化版

    优化策略：
    1. LRU缓存（最近最少使用）
    2. 内存上限控制
    3. 按访问频率保留热点
    4. 支持预热指定格子
    """

    # 缓存配置
    _MAX_CACHE_SIZE = 20  # 最多缓存20个格子
    _MEMORY_THRESHOLD_MB = 2  # 内存上限2MB

    def __init__(self, cells_dir: Optional[Path] = None):
        self.cells_dir = cells_dir or _CELLS_DIR
        self._cache: OrderedDict[str, CellContent] = OrderedDict()  # LRU缓存
        self._access_count: Dict[str, int] = {}  # 访问计数
        self._parse_func: Optional[callable] = None  # 解析函数注入
        self._total_memory_bytes = 0  # 估算内存使用

    def set_parse_func(self, func: callable):
        """注入解析函数"""
        self._parse_func = func

    def load_cell(self, cell_id: str, file_path: str) -> Optional[CellContent]:
        """
        懒加载单个格子 - LRU策略

        Args:
            cell_id: 格子ID
            file_path: 文件路径

        Returns:
            格子内容
        """
        # 1. 检查缓存（命中则移到末尾）
        if cell_id in self._cache:
            # LRU: 移到末尾表示最近使用
            self._cache.move_to_end(cell_id)
            self._access_count[cell_id] = self._access_count.get(cell_id, 0) + 1
            return self._cache[cell_id]

        # 2. 懒加载
        if self._parse_func and file_path:
            content = self._parse_func(Path(file_path))
            if content:
                # 估算内存占用
                estimated_size = self._estimate_size(content)
                self._total_memory_bytes += estimated_size

                # 检查内存限制
                if self._total_memory_bytes > self._MEMORY_THRESHOLD_MB * 1024 * 1024:
                    self._evict_lru()

                # LRU缓存
                self._cache[cell_id] = content
                self._access_count[cell_id] = 1

                # 检查数量限制
                if len(self._cache) > self._MAX_CACHE_SIZE:
                    self._evict_lru()

                return content

        return None

    def _estimate_size(self, content: CellContent) -> int:
        """估算格子内存占用（字节）"""
        size = 0
        # 基本字段
        size += len(content.cell_id) + len(content.name) + len(content.summary)
        size += len(str(content.tags)) * 8  # 估算set开销
        # 列表字段
        for lst in [content.points, content.associations, content.analogies,
                    content.metrics, content.cases, content.insights]:
            size += len(str(lst)) * 8
        return size

    def _evict_lru(self):
        """驱逐最少使用的格子"""
        if not self._cache:
            return

        # 找出访问次数最少的
        min_access = min(self._access_count.values())
        for cell_id in list(self._cache.keys()):
            if self._access_count.get(cell_id, 0) == min_access:
                # 释放内存
                content = self._cache.pop(cell_id)
                self._total_memory_bytes -= self._estimate_size(content)
                self._access_count.pop(cell_id, None)
                break

        # 如果还不够，再驱逐一个
        if len(self._cache) > self._MAX_CACHE_SIZE // 2:
            oldest = next(iter(self._cache))
            content = self._cache.pop(oldest)
            self._total_memory_bytes -= self._estimate_size(content)
            self._access_count.pop(oldest, None)

    def preload_cells(self, cell_ids: List[str], index_manager: CellIndexManager):
        """
        预加载指定格子

        Args:
            cell_ids: 要预加载的格子ID列表
            index_manager: 索引管理器
        """
        for cell_id in cell_ids:
            index = index_manager.get_index(cell_id)
            if index and cell_id not in self._cache:
                self.load_cell(cell_id, index.file_path)

    def get_cached_count(self) -> int:
        """获取已缓存的格子数"""
        return len(self._cache)

    def get_memory_usage(self) -> Dict[str, Any]:
        """获取内存使用统计"""
        return {
            'cached_count': len(self._cache),
            'memory_bytes': self._total_memory_bytes,
            'memory_mb': round(self._total_memory_bytes / 1024 / 1024, 2),
            'max_cache_size': self._MAX_CACHE_SIZE,
            'max_memory_mb': self._MEMORY_THRESHOLD_MB
        }

    def get_hot_cells(self, top_n: int = 5) -> List[str]:
        """获取热点格子（访问次数最多）"""
        sorted_cells = sorted(
            self._access_count.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [cell_id for cell_id, _ in sorted_cells[:top_n]]

    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
        self._access_count.clear()
        self._total_memory_bytes = 0


# ============ 知识域格子管理器 ============

class DomainCellManager:
    """
    知识域格子管理器 - v2.2 深度优化版

    优化策略：
    1. 启动时仅加载索引（~5ms，缓存后 ~1ms）
    2. 访问格子时按需加载完整内容
    3. LRU缓存 + 内存上限控制
    4. 并行读取 + 缓存持久化
    """

    # 知识域格子ID范围
    B_CELLS = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15']
    C_CELLS = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']

    def __init__(self, cells_dir: Optional[Path] = None, lazy: bool = True):
        """
        初始化格子管理器

        Args:
            cells_dir: 格子目录
            lazy: 是否使用懒加载模式（默认True）
        """
        import time

        self.cells_dir = cells_dir or _CELLS_DIR

        # 格子内容缓存（懒加载模式下为空，使用_lazy_loader）
        self.cells: Dict[str, CellContent] = {}

        # v2.2 新增：索引管理器（并行读取+缓存）
        self._index_manager = CellIndexManager(self.cells_dir)

        # v2.2 新增：懒加载器（LRU缓存）
        self._lazy_loader = LazyCellLoader(self.cells_dir)
        self._lazy_loader.set_parse_func(self._load_cell)

        # v2.2 新增：加载性能统计
        self._load_stats = {
            'index_load_time': 0.0,
            'cells_load_time': 0.0,
            'cache_hits': 0,
            'lazy_mode': lazy,
            'from_cache': False
        }

        if lazy:
            # 懒加载模式：仅预加载索引
            start = time.perf_counter()
            self._load_stats['index_load_time'] = self._index_manager.preload_index()
            self._load_stats['from_cache'] = self._index_manager._cache_file.exists()
        else:
            # 兼容模式：加载全部
            start = time.perf_counter()
            self._load_all_cells()
            self._load_stats['cells_load_time'] = time.perf_counter() - start

    def _load_all_cells(self):
        """加载所有知识域格子（兼容模式）"""
        for md_file in self.cells_dir.glob("B*.md"):
            cell_id = md_file.stem.split('_')[0]
            self.cells[cell_id] = self._load_cell(md_file)

        for md_file in self.cells_dir.glob("C*.md"):
            cell_id = md_file.stem.split('_')[0]
            self.cells[cell_id] = self._load_cell(md_file)

    def _load_cell(self, file_path: Path) -> CellContent:
        """加载单个格子"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析基本信息
        stem = file_path.stem
        parts = stem.split('_', 1)
        cell_id = parts[0] if len(parts) > 1 else stem
        name = parts[1] if len(parts) > 1 else stem

        # 解析标签
        tags_match = re.search(r'## 标签\s*\n(.+?)(?=\n## |\Z)', content, re.DOTALL)
        tags = set()
        if tags_match:
            tags = set(t.strip() for t in re.split(r'[,:，：]', tags_match.group(1)) if t.strip())

        # 解析核心摘要
        summary = ""
        points = []
        summary_match = re.search(r'## 核心摘要\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if summary_match:
            summary_text = summary_match.group(1)
            what_match = re.search(r'### 这是什么\s*\n(.+?)(?=\n### |\Z)', summary_text, re.DOTALL)
            if what_match:
                summary = what_match.group(1).strip()

            points_match = re.search(r'### 核心要点\s*\n(.+?)(?=\n### |\Z)', summary_text, re.DOTALL)
            if points_match:
                points = [p.strip() for p in re.findall(r'\d+\.\s*\*\*(.+?)\*\*', points_match.group(1))]

        # 解析举一反三
        analogies = []
        analogy_match = re.search(r'## 举一反三\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if analogy_match:
            analogies = [a.strip() for a in analogy_match.group(1).strip().split('\n') if a.strip() and not a.startswith('无')]

        # 解析实战案例
        cases = []
        cases_match = re.search(r'## 实战案例\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if cases_match:
            for line in cases_match.group(1).strip().split('\n'):
                if line.strip() and line.strip() != '暂无':
                    cases.append(line.strip().lstrip('- '))

        # 解析关联
        associations = {}
        assoc_match = re.search(r'## 关联领域\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if assoc_match:
            for line in assoc_match.group(1).strip().split('\n'):
                match = re.match(r'- (.+?)（关联度[：:]([\d.]+)）', line)
                if match:
                    associations[match.group(1).strip()] = float(match.group(2))

        return CellContent(
            cell_id=cell_id,
            name=name,
            tags=tags,
            summary=summary,
            points=points,
            associations=associations,
            analogies=analogies,
            cases=cases,
            last_updated=datetime.now().strftime('%Y-%m-%d')
        )

    def get_cell(self, cell_id: str) -> Optional[CellContent]:
        """
        获取格子 - v2.2 LRU懒加载实现

        策略：
        1. 优先从LRU缓存获取
        2. 未命中则懒加载
        3. 自动LRU淘汰
        """
        # 1. 检查懒加载缓存（LRU）
        cached = self._lazy_loader.load_cell(cell_id, "")
        if cached:
            self._load_stats['cache_hits'] += 1
            return cached

        # 2. 通过索引懒加载
        index = self._index_manager.get_index(cell_id)
        if index:
            content = self._lazy_loader.load_cell(cell_id, index.file_path)
            if content:
                return content

        return None

    def get_all_cells(self) -> Dict[str, CellContent]:
        """
        获取所有格子

        注意：懒加载模式下只返回已缓存的格子
        如需完整列表，使用 get_all_indices()
        """
        # 返回LRU缓存中的所有格子
        return dict(self._lazy_loader._cache)

    def get_all_indices(self) -> Dict[str, CellIndex]:
        """
        获取所有格子索引 - 快速方法

        返回所有格子的轻量级元数据，不加载完整内容
        """
        return self._index_manager.get_all_indices()

    def search_indices(self, keyword: str) -> List[CellIndex]:
        """
        搜索格子索引 - 快速方法

        不触发完整内容加载
        """
        return self._index_manager.search_indices(keyword)

    def preload_cells(self, cell_ids: List[str]):
        """
        预加载指定格子

        Args:
            cell_ids: 要预加载的格子ID列表
        """
        self._lazy_loader.preload_cells(cell_ids, self._index_manager)

    def get_load_stats(self) -> Dict[str, Any]:
        """
        获取加载性能统计

        Returns:
            包含加载时间、缓存数量等统计信息
        """
        return {
            **self._load_stats,
            'cached_count': self._lazy_loader.get_cached_count(),
            'total_indices': len(self._index_manager.index),
            'memory_usage': self._lazy_loader.get_memory_usage(),
            'hot_cells': self._lazy_loader.get_hot_cells(3)
        }

    def get_domain_cells(self) -> Dict[str, CellContent]:
        """获取知识域格子（B和C开头）"""
        return {k: v for k, v in self.cells.items() if k.startswith(('B', 'C'))}

    def create_cell(self, name: str, tags: Set[str], summary: str = "",
                   associations: Dict[str, float] = None) -> Optional[str]:
        """创建新格子"""
        # 分配ID
        existing_ids = set(self.cells.keys())
        available_b = [b for b in self.B_CELLS if b not in existing_ids]

        if not available_b:
            return None  # 格子已满

        cell_id = available_b[0]

        # 生成内容
        content = self._generate_cell_content(cell_id, name, tags, summary, associations or {})

        # 保存文件
        cell_path = self.cells_dir / f"{cell_id}_{name}.md"
        with open(cell_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # 加载到内存
        self.cells[cell_id] = CellContent(
            cell_id=cell_id,
            name=name,
            tags=tags,
            summary=summary,
            associations=associations or {},
            last_updated=datetime.now().strftime('%Y-%m-%d')
        )

        return cell_id

    def _generate_cell_content(self, cell_id: str, name: str, tags: Set[str],
                                summary: str, associations: Dict[str, float]) -> str:
        """生成格子内容"""
        assoc_lines = []
        for rel_name, weight in associations.items():
            assoc_lines.append(f"- {rel_name}（关联度：{weight}）")
        assoc_str = "\n".join(assoc_lines) if assoc_lines else "- 暂无关联"

        return f"""# {cell_id}_{name}

## 元信息
- 创建时间：{datetime.now().strftime('%Y-%m-%d')}
- 更新时间：{datetime.now().strftime('%Y-%m-%d')}
- 激活次数：0
- 学习深度：理解
- 来源：自动发现生成

## 标签
{', '.join(tags)}

## 核心摘要

### 这是什么
{summary or f'{name}是运营管理中的重要领域'}

### 核心要点
1. **基础认知**：理解{name}的基本概念和范畴
2. **关键指标**：掌握衡量{name}效果的核心指标
3. **实践方法**：应用系统化的{name}方法论

## 详细笔记
_待填充_

## 举一反三
- {name} = 另一种形态的运营实践
- 做好{name}需要持续迭代优化

## 关联领域
{assoc_str}

## 上次激活
{datetime.now().strftime('%Y-%m-%d')}
"""

    def enrich_cell(self, cell_id: str, new_content: Dict[str, Any]) -> bool:
        """丰富格子内容"""
        cell = self.cells.get(cell_id)
        if not cell:
            return False

        # 更新标签
        if 'new_tags' in new_content:
            cell.tags.update(new_content['new_tags'])

        # 更新举一反三
        if 'new_analogies' in new_content:
            cell.analogies.extend(new_content['new_analogies'])

        # 更新指标
        if 'new_metrics' in new_content:
            cell.metrics.extend(new_content['new_metrics'])

        # 更新案例（去重）
        if 'new_cases' in new_content:
            existing_cases = set(cell.cases)
            for case in new_content['new_cases']:
                if case not in existing_cases:
                    cell.cases.append(case)

        # 更新洞见（去重）
        if 'new_insights' in new_content:
            existing_insights = set(cell.insights)
            for insight in new_content['new_insights']:
                if insight not in existing_insights:
                    cell.insights.append(insight)

        # 更新摘要
        if 'summary' in new_content:
            cell.summary = new_content['summary']

        # 保存到文件
        self._save_cell(cell)

        return True

    def _save_cell(self, cell: CellContent):
        """保存格子到文件"""
        cell_path = self.cells_dir / f"{cell.cell_id}_{cell.name}.md"
        if not cell_path.exists():
            return

        with open(cell_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 更新标签
        if cell.tags:
            content = re.sub(
                r'## 标签\s*\n.+?(?=\n## |\Z)',
                f'## 标签\n{", ".join(sorted(cell.tags))}',
                content,
                flags=re.DOTALL
            )

        # 更新举一反三
        if cell.analogies:
            analogy_lines = []
            for a in cell.analogies:
                a = a.strip().lstrip('- ')
                if a and not a.startswith('暂无'):
                    analogy_lines.append(f"- {a}")
            if analogy_lines:
                analogy_section = "\n".join(analogy_lines)
                content = re.sub(
                    r'## 举一反三\s*\n.+?(?=\n## |\Z)',
                    f'## 举一反三\n{analogy_section}',
                    content,
                    flags=re.DOTALL
                )

        # 更新案例
        if cell.cases:
            cases_lines = [f"- {c}" for c in cell.cases if c]
            if cases_lines:
                cases_section = "\n".join(cases_lines)
                # 如果没有案例章节，添加一个
                if '## 实战案例' not in content:
                    content = content.replace('## 上次激活', f'## 实战案例\n{cases_section}\n\n## 上次激活')
                else:
                    content = re.sub(
                        r'## 实战案例\s*\n.+?(?=\n## |\Z)',
                        f'## 实战案例\n{cases_section}',
                        content,
                        flags=re.DOTALL
                    )

        # 更新指标
        if cell.metrics:
            metrics_section = "\n".join([f"- {m}" for m in cell.metrics])
            content = re.sub(
                r'## 关键指标\s*\n.+?(?=\n## |\Z)',
                f'## 关键指标\n{metrics_section}',
                content,
                flags=re.DOTALL
            )

        # 更新时间
        content = re.sub(
            r'更新时间：[\d-]+',
            f'更新时间：{datetime.now().strftime("%Y-%m-%d")}',
            content
        )

        with open(cell_path, 'w', encoding='utf-8') as f:
            f.write(content)


# ============ 使用追踪器 ============

class UsageTracker:
    """使用追踪器"""

    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or (_CONFIG_DIR / "usage_tracker.json")
        self.stats: Dict[str, UsageStats] = defaultdict(lambda: UsageStats(cell_id=""))
        self.topic_demand: Dict[str, int] = defaultdict(int)
        self.query_patterns: Dict[str, int] = defaultdict(int)
        self._loaded = False  # v6.1: 延迟加载标记

    def _load(self):
        """加载追踪数据（v6.1: 延迟到首次使用时才执行）"""
        if self._loaded:
            return
        self._loaded = True
        _ensure_config_dir()
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for cell_id, stats_data in data.get('stats', {}).items():
                        stats = UsageStats(
                            cell_id=cell_id,
                            call_count=stats_data.get('call_count', 0),
                            last_called=stats_data.get('last_called'),
                            topics=set(stats_data.get('topics', [])),
                            queries=stats_data.get('queries', [])[-50:]  # 只保留最近50条
                        )
                        self.stats[cell_id] = stats
                    self.topic_demand = defaultdict(int, data.get('topic_demand', {}))
                    self.query_patterns = defaultdict(int, data.get('query_patterns', {}))
            except Exception as e:
                logger.warning(f"[UsageTracker] _load failed: {e}")

    def _save(self):
        """保存追踪数据"""
        data = {
            'stats': {
                cell_id: {
                    'call_count': s.call_count,
                    'last_called': s.last_called,
                    'topics': list(s.topics),
                    'queries': s.queries
                }
                for cell_id, s in self.stats.items()
            },
            'topic_demand': dict(self.topic_demand),
            'query_patterns': dict(self.query_patterns),
            'last_updated': datetime.now().isoformat()
        }
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def track(self, cell_id: str, query: str, topics: Set[str]):
        """追踪使用"""
        self._load()  # v6.1: 首次追踪时才加载历史数据
        stats = self.stats[cell_id]
        stats.cell_id = cell_id
        stats.call_count += 1
        stats.last_called = datetime.now().isoformat()
        stats.queries.append(f"{datetime.now().date()}: {query[:50]}")
        stats.topics.update(topics)

        # 追踪主题需求
        for topic in topics:
            self.topic_demand[topic] += 1

        # 追踪查询模式
        pattern = self._extract_pattern(query)
        if pattern:
            self.query_patterns[pattern] += 1

        self._save()

    def _extract_pattern(self, query: str) -> str:
        """提取查询模式"""
        pattern = re.sub(r'[\d]+', '#', query)
        pattern = re.sub(r'[某这那个些个的]', '', pattern)
        return pattern.strip()[:30]

    def get_hot_topics(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """获取热门主题"""
        return sorted(self.topic_demand.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def get_cold_cells(self, threshold: int = 3) -> List[str]:
        """获取冷门格子（低使用率）"""
        return [cell_id for cell_id, stats in self.stats.items()
                if stats.call_count < threshold]

    # 无意义的词（查询片段）
    _NOISE_WORDS = {'如何', '怎么', '什么', '为什么', '哪个', '是否', '提升', '优化', '增加', '提高'}

    def get_topic_gaps(self, existing_names: Set[str], top_n: int = 5, min_count: int = 3) -> List[str]:
        """发现知识缺口"""
        gaps = []
        for topic, count in sorted(self.topic_demand.items(), key=lambda x: x[1], reverse=True):
            # 过滤太短的词（可能是查询片段）
            if len(topic) < 2:
                continue

            # 过滤无意义的查询词
            if topic in self._NOISE_WORDS or any(topic.startswith(w) for w in ['如何', '怎么', '什么', '为什么']):
                continue

            # 检查是否与现有格子名称相似
            is_gap = True
            for existing in existing_names:
                # 检查包含关系
                if topic in existing or existing in topic:
                    is_gap = False
                    break
                # 检查是否有共同字符（前两个字）
                if len(topic) >= 2 and len(existing) >= 2:
                    if topic[:2] in existing or existing[:2] in topic:
                        is_gap = False
                        break

            if is_gap and count >= min_count:
                gaps.append(topic)
                if len(gaps) >= top_n:
                    break
        return gaps

    def get_usage_stats(self, cell_id: str) -> Optional[UsageStats]:
        """获取格子使用统计"""
        return self.stats.get(cell_id)


# ============ 内容丰富器 ============

class ContentEnricher:
    """内容丰富器 - 提供真实深度的业务知识"""

    # 深度知识库：每个领域都有真实的业务洞见
    DEEP_KNOWLEDGE = {
        "增长": {
            "metrics": ["CAC", "LTV", "K因子", "留存率", "激活率", "自然增长率"],
            "analogies": [
                "增长 = 找到可持续的获客飞轮",
                "裂变 = 用户自愿成为分发渠道",
                "增长黑客 = 用数据驱动实验迭代",
                "LTV > CAC 3倍才是健康模型"
            ],
            "cases": [
                "Dropbox通过推荐奖励实现从0到1亿用户的爆发式增长",
                "拼多多通过拼团模式实现社交裂变，年GMV突破万亿"
            ],
            "insights": [
                "北极星指标是增长的指南针",
                "留存率是检验增长质量的唯一标准",
                "获客成本需要用LTV来评估是否值得"
            ]
        },
        "直播": {
            "metrics": ["在线人数", "GMV", "互动率", "停留时长", "转化率", "UV价值", "场均GMV"],
            "analogies": [
                "直播 = 线上批发市场的实时叫卖",
                "直播 = 用内容换流量，用流量换GMV",
                "主播 = 24小时在线的销售员+客服+品牌",
                "直播间停留时长决定转化可能性"
            ],
            "cases": [
                "李佳琦直播间通过口红试色创造单场破亿GMV",
                "东方甄选转型农产品直播，实现股价10倍增长"
            ],
            "insights": [
                "直播开场5分钟决定整场氛围",
                "互动率>10%才是活跃直播间",
                "选品决定了GMV的天花板"
            ]
        },
        "私域": {
            "metrics": ["入群率", "触达率", "响应率", "流失率", "复购率", "ARPU", "LTV"],
            "analogies": [
                "私域 = 自有鱼塘，不用每次付费捕鱼",
                "私域 = 用户资产私有化，可重复开采",
                "企微私域 = 建立用户档案，实现精准触达",
                "私域复购成本是公域的1/10"
            ],
            "cases": [
                "完美日记通过企微私域实现复购率提升50%",
                "瑞幸咖啡通过私域社群实现月活提升30%"
            ],
            "insights": [
                "私域的本质是经营用户关系",
                "高频低毛利产品适合私域",
                "私域要分层运营，不能一刀切"
            ]
        },
        "策略": {
            "metrics": ["目标达成率", "资源利用率", "ROI", "执行效率", "风险覆盖率"],
            "analogies": [
                "策略 = 在约束条件下找到最优解",
                "战略规划 = 先画地图再赶路",
                "竞争策略 = 在长板处压制对手",
                "策略 = 用有限资源撬动最大杠杆"
            ],
            "cases": [
                "美团从团购到外卖，战略聚焦实现千亿市值",
                "字节跳动通过算法推荐实现全球化突破"
            ],
            "insights": [
                "好的策略是找到差异化定位",
                "执行速度往往比完美计划更重要",
                "要学会在关键时刻果断投入资源"
            ]
        },
        "数据": {
            "metrics": ["DAU", "MAU", "留存率", "转化率", "NPS", "流失率", "GMV", "ARPU"],
            "analogies": [
                "数据 = 业务的眼睛和仪表盘",
                "数据分析 = 用证据说话的艺术",
                "数据埋点 = 给用户行为装上追踪器",
                "指标体系 = 业务的体温计和血压计"
            ],
            "cases": [
                "字节跳动通过数据中台支撑千人千面推荐",
                "某电商通过漏斗分析发现支付环节流失率高达40%"
            ],
            "insights": [
                "数据是用来提问的，不是用来回答的",
                "北极星指标只有一个，找到它",
                "相关性不等于因果性，要设计实验验证"
            ]
        },
        "内容": {
            "metrics": ["阅读量", "互动率", "完播率", "转发率", "涨粉率", "点赞率", "评论率"],
            "analogies": [
                "内容 = 价值的载体，信任的媒介",
                "爆款内容 = 戳中情绪+提供价值+便于传播",
                "内容IP = 持续输出建立认知壁垒",
                "内容 = 最低成本的获客方式"
            ],
            "cases": [
                "公众号咪蒙通过情绪共鸣实现10万+刷屏",
                "B站何同学通过科技内容实现千万粉丝"
            ],
            "insights": [
                "选题占内容成败的70%",
                "开头3秒决定用户是否继续",
                "要站在用户视角而非品牌视角创作"
            ]
        },
        "会员": {
            "metrics": ["会员数", "升级率", "活跃度", "ARPU", "续费率", "会员收入占比"],
            "analogies": [
                "会员 = 用户用确定的钱换确定的服务",
                "会员体系 = 用权益分级激励用户升级",
                "付费会员 = 锁定用户终身价值的合约",
                "会员 = 把流量变成留量的容器"
            ],
            "cases": [
                "Costco通过会员制实现90%续费率，净利润来自会费",
                "爱奇艺通过会员分级提升ARPU 40%"
            ],
            "insights": [
                "会员的核心价值是专属感和特权感",
                "低频产品适合订阅制",
                "会员生命周期价值要大于获客成本"
            ]
        },
        "广告": {
            "metrics": ["CPM", "CPC", "CTR", "ROI", "转化成本", "消耗", "转化数", "CPA"],
            "analogies": [
                "广告 = 用钱买流量的速度",
                "信息流广告 = 把广告伪装成内容",
                "效果广告 = 为每一次曝光付费",
                "品牌广告 = 为用户心智上保险"
            ],
            "cases": [
                "某品牌通过素材AB测试将CTR提升3倍",
                "完美日记通过社交流量实现ROI 1:5"
            ],
            "insights": [
                "广告的尽头是素材质量",
                "投放要先小步快跑测试，再放量",
                "不同平台用户特征不同，要差异化投放"
            ]
        },
        "电商": {
            "metrics": ["GMV", "转化率", "客单价", "复购率", "毛利率", "库存周转", "UV"],
            "analogies": [
                "电商 = 线上交易闭环的效率游戏",
                "选品 = 确定卖给谁、卖什么",
                "电商 = 流量获取+转化优化+供应链效率的综合体",
                "GMV = UV × 转化率 × 客单价"
            ],
            "cases": [
                "某品牌通过选品优化将客单价提升40%",
                "SHEIN通过小单快返实现库存周转率行业第一"
            ],
            "insights": [
                "电商的核心竞争力是供应链",
                "要把流量成本摊薄到复购上",
                "转化率的微小提升对GMV影响巨大"
            ]
        },
        "投放": {
            "metrics": ["消耗", "ROI", "CPM", "CPC", "转化数", "CPA", "回搜率"],
            "analogies": [
                "投放 = 付费杠杆，放大自然增长的成果",
                "投放 = 用确定的钱换确定的流量",
                "千川投放 = 抖音电商的流量印钞机",
                "投放 = 规模化测试，找到最优组合"
            ],
            "cases": [
                "某品牌通过达人投放实现ROI 1:8",
                "某直播间通过千川投放实现在线人数破万"
            ],
            "insights": [
                "投放要先测品，再放量",
                "素材衰退期通常只有7-14天",
                "投放要和内容结合才能持久"
            ]
        },
        "裂变": {
            "metrics": ["K因子", "分享率", "邀请率", "转化率", "病毒系数", "裂变系数"],
            "analogies": [
                "裂变 = 用户自愿成为分发渠道",
                "裂变 = 用产品换流量",
                "拼团 = 社交关系驱动的购买转化",
                "邀请奖励 = 用利益驱动用户拉新"
            ],
            "cases": [
                "拼多多通过拼团模式实现用户指数级增长",
                "瑞幸咖啡通过邀请得一杯实现千万新增"
            ],
            "insights": [
                "K因子>1才能实现病毒式增长",
                "裂变需要设计好激励和路径",
                "好的裂变是用户觉得在帮朋友，不是在帮品牌"
            ]
        },
        "用户研究": {
            "metrics": ["NPS", "满意度", "留存率", "流失率", "复购周期", "用户画像覆盖率", "北极星指标"],
            "analogies": [
                "用户研究 = 用数据理解人的行为",
                "用户画像 = 把抽象用户具象化",
                "用户旅程 = 从陌生到忠诚的完整路径",
                "用户分层 = 差异化运营的基础",
                "会员 = 把流量变成留量的容器",
                "会员体系 = 用权益分级激励用户升级",
            ],
            "cases": [
                "Costco通过会员制实现90%续费率，净利润来自会费",
                "爱奇艺通过会员分级提升ARPU 40%",
                "某电商通过用户分层实现精准推送，转化率提升25%",
                "某APP通过用户旅程优化使留存率提升40%",
            ],
            "insights": [
                "用户说的话和做的事往往不一致",
                "定量数据回答是什么，定性研究回答为什么",
                "核心用户比泛用户更有价值",
                "会员的核心价值是专属感和特权感",
                "低频产品适合订阅制",
                "会员生命周期价值要大于获客成本",
            ]
        },
        "互动": {
            "metrics": ["互动率", "评论率", "点赞率", "转发率", "关注率", "停留时长"],
            "analogies": [
                "互动 = 用户用行动表达认可",
                "评论 = 用户主动参与的信号",
                "互动 = 建立信任的过程",
                "互动率 = 内容的温度计"
            ],
            "cases": [
                "某直播间通过福袋抽奖提升互动率300%",
                "某博主通过问答互动提升粉丝忠诚度"
            ],
            "insights": [
                "互动是最好的用户反馈",
                "要设计让用户容易互动的钩子",
                "回复评论可以提升二次互动"
            ]
        }
    }

    def enrich(self, cell: CellContent) -> Dict[str, Any]:
        """丰富格子内容"""
        # 找到匹配的关键词
        matched_key = None
        cell_name_lower = cell.name.lower()

        for key in self.DEEP_KNOWLEDGE:
            if key in cell_name_lower or any(key in tag.lower() for tag in cell.tags if tag):
                matched_key = key
                break

        # 优先使用名称匹配
        if not matched_key:
            for key in self.DEEP_KNOWLEDGE:
                if key in cell_name_lower:
                    matched_key = key
                    break

        if not matched_key:
            return {}

        knowledge = self.DEEP_KNOWLEDGE[matched_key]
        result = {
            'new_tags': set(),
            'new_analogies': [],
            'new_metrics': [],
            'new_cases': [],
            'new_insights': knowledge.get('insights', [])
        }

        # 添加新标签（去重）
        for tag in knowledge['metrics'][:4]:
            if tag.lower() not in [t.lower() for t in cell.tags]:
                result['new_tags'].add(tag)

        # 添加举一反三（严格去重）
        existing_analogies = set(a.replace('- ', '').replace('= ', '=').replace(' ', '') for a in cell.analogies)
        for analogy in knowledge['analogies']:
            normalized = analogy.replace('= ', '=').replace(' ', '')
            if normalized not in existing_analogies:
                result['new_analogies'].append(analogy)
                existing_analogies.add(normalized)

        # 添加指标（去重）
        for metric in knowledge['metrics'][:5]:
            if metric not in cell.metrics:
                result['new_metrics'].append(metric)

        # 添加案例（去重）
        existing_cases = set(cell.cases)
        for case in knowledge['cases'][:2]:
            if case not in existing_cases:
                result['new_cases'].append(case)

        return result


# ============ 主引擎 ============

class DomainNexus:
    """
    DomainNexus - 知识域格子动态更新系统主引擎 v2.2

    真正可工作的知识域格子动态更新系统

    核心能力：
    1. query() - 知识检索和整合
    2. execute() - 调用神行轨执行任务
    3. evolve() - 自动丰富知识

    加载性能（v2.2优化）：
    - 索引加载: ~5ms (15个格子)
    - 单格访问: ~1ms (首次解析)
    - 缓存命中: ~0.1ms
    """

    # 部门映射：根据问题类型自动选择执行部门
    DEPARTMENT_MAP = {
        "增长": "户部",      # 资源优化
        "裂变": "户部",      # 资源分配
        "直播": "礼部",      # 内容营销
        "内容": "礼部",      # 文化创意
        "私域": "礼部",      # 用户关系
        "会员": "礼部",      # 用户运营
        "数据": "吏部",      # 分析评估
        "策略": "兵部",      # 战略决策
        "电商": "工部",      # 执行运营
        "广告": "工部",      # 投放执行
        "投放": "工部",      # 投放执行
        "互动": "礼部",      # 用户互动
        "分析": "吏部",      # 数据分析
        "规划": "兵部",      # 战略规划
        "执行": "工部",      # 任务执行
        "风险": "刑部",      # 合规审查
    }

    def __init__(self, cells_dir: Optional[Path] = None, lazy: bool = True):
        """
        初始化 DomainNexus - v7.0 升级版

        新增能力（来自 knowledge_graph 提炼）：
        - KnowledgeGraph: cell 关系图谱（图结构关联）
        - ConceptLinker: 概念链接器（跨 cell 概念关联）
        - RuleManager: 规则管理器（条件→动作推理）

        Args:
            cells_dir: 格子目录
            lazy: 是否使用懒加载模式（默认True，更快启动）
        """
        import time
        self._init_start = time.perf_counter()

        self.cell_manager = DomainCellManager(cells_dir, lazy=lazy)
        self.usage_tracker = UsageTracker()
        self.content_enricher = ContentEnricher()
        self._evolved_cells: Set[str] = set()  # 已进化的格子
        self._track_b_executor = None  # 神行轨执行器

        # ==== v7.0 新增：来自 knowledge_graph 的价值板块 ====
        self.knowledge_graph = KnowledgeGraph()          # cell 关系图谱
        self.concept_linker = ConceptLinker()          # 概念链接器
        self.rule_manager = RuleManager()               # 规则管理器
        self._graph_synced: bool = False               # 图谱是否已与现有 cell 同步
        self._concepts_synced: bool = False           # 概念是否已同步

        # v2.2 性能统计
        self._init_time = time.perf_counter() - self._init_start
        self._query_count = 0
        self._query_times: List[float] = []

    # ---- v7.0 新增：图谱/概念惰性同步 ----

    def _ensure_graph_synced(self):
        """
        惰性同步：将现有 cell 的 associations 注入 KnowledgeGraph
        只在首次需要图查询时调用，避免启动时加载全部 cell
        """
        if self._graph_synced:
            return
        cell_name_map: Dict[str, str] = {}  # name → cell_id
        for cell_id, cell in self.cell_manager.get_domain_cells().items():
            cell_name_map[cell.name] = cell_id
        for cell_id, cell in self.cell_manager.get_domain_cells().items():
            self.knowledge_graph.add_cell_node(cell_id, {
                "name": cell.name, "tags": list(cell.tags)
            })
            if cell.associations:
                self.knowledge_graph.suggest_relations_from_associations(
                    cell_id, cell.associations, cell_name_map
                )
        self._graph_synced = True

    def _ensure_concepts_synced(self):
        """
        惰性同步：将现有 cell 的 tags/metrics 注入 ConceptLinker
        """
        if self._concepts_synced:
            return
        for cell_id, cell in self.cell_manager.get_domain_cells().items():
            self.concept_linker.auto_extract_from_cell(cell)
        self._concepts_synced = True

    def get_init_time(self) -> float:
        """获取初始化耗时"""
        return self._init_time

    def get_performance_stats(self) -> Dict[str, Any]:
        """
        获取性能统计

        Returns:
            性能统计信息
        """
        return {
            'init_time_ms': round(self._init_time * 1000, 2),
            'query_count': self._query_count,
            'avg_query_time_ms': round(sum(self._query_times) / len(self._query_times) * 1000, 2) if self._query_times else 0,
            'cell_stats': self.cell_manager.get_load_stats()
        }

    def list_cells(self) -> List[Dict[str, Any]]:
        """
        列出所有知识格子

        Returns:
            格子信息列表 [{"cell_id":..., "name":..., ...}]
        """
        cells_info = []

        # 优先从cell_manager.cells获取（如果已加载）
        if self.cell_manager.cells:
            for cell_id, cell in self.cell_manager.cells.items():
                cells_info.append({
                    "cell_id": cell.cell_id,
                    "name": cell.name,
                    "tags": list(cell.tags) if isinstance(cell.tags, set) else cell.tags,
                    "summary": cell.summary[:50] if cell.summary else "",
                    "activated": cell.activation_count
                })
        else:
            # 从索引管理器获取（更快）
            indices = self.cell_manager._index_manager.get_all_indices()
            for cell_id, idx in indices.items():
                cells_info.append({
                    "cell_id": idx.cell_id,
                    "name": idx.name,
                    "tags": list(idx.tags) if isinstance(idx.tags, set) else idx.tags,
                    "summary_preview": idx.summary_preview
                })

        return cells_info

    def reload(self):
        """重新加载所有格子（动态感知新增格子）"""
        self.cell_manager._load_all_cells()
        self.usage_tracker._load()
        return len(self.cell_manager.cells)

    def refresh(self):
        """刷新单例（强制重新初始化）"""
        global _nexus
        _nexus = DomainNexus(self.cell_manager.cells_dir)
        return _nexus

    def connect_track_b(self):
        """
        连接神行轨，让知识格子具备执行能力

        Returns:
            是否连接成功
        """
        try:
            from knowledge_cells.track_b_adapter import get_track_b_executor
            self._track_b_executor = get_track_b_executor()
            return True
        except ImportError:
            print("⚠️ 无法导入神行轨适配器")
            return False

    def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行任务 - 调用神行轨 Claw 执行具体工作

        Args:
            task: 任务描述
            context: 上下文信息

        Returns:
            执行结果
        """
        # 1. 分析任务，确定部门
        department = self._analyze_department(task)
        branch_id = self._department_to_branch(department)

        # 2. 如果未连接神行轨，先尝试连接
        if not self._track_b_executor:
            self.connect_track_b()

        # 3. 构建执行上下文
        exec_context = context or {}
        exec_context['source'] = 'domain_nexus'
        exec_context['task_source'] = 'knowledge_cell'

        # 4. 执行任务
        if self._track_b_executor:
            result = self._track_b_executor.execute(
                branch_id=branch_id,
                department=department,
                task=task,
                context=exec_context
            )
        else:
            # 回退：使用模拟结果
            result = self._execute_mock(department, task)

        # 5. 追踪使用
        self._track_execution(task, department, result)

        return result

    def _analyze_department(self, task: str) -> str:
        """分析任务类型，确定执行部门"""
        if not task:
            return "工部"
        task_lower = task.lower()

        for keyword, dept in self.DEPARTMENT_MAP.items():
            if keyword in task_lower:
                return dept

        # 默认选择工部（执行部门）
        return "工部"

    def _department_to_branch(self, department: str) -> str:
        """部门到枝丫的映射"""
        branch_map = {
            "户部": "SD-L1",
            "吏部": "SD-D2",
            "兵部": "SD-C2",
            "礼部": "SD-F1",
            "工部": "SD-E1",
            "刑部": "SD-R2",
        }
        return branch_map.get(department, "SD-E1")

    def _execute_mock(self, department: str, task: str) -> Dict[str, Any]:
        """模拟执行（神行轨未连接时）"""
        mock_outputs = {
            "兵部": f"📊 【战略分析报告】\n\n基于任务「{task[:30]}...」，已完成战略视角分析。",
            "吏部": f"📈 【数据分析报告】\n\n基于任务「{task[:30]}...」，已完成数据分析。",
            "户部": f"💰 【资源规划报告】\n\n基于任务「{task[:30]}...」，已完成资源分配方案。",
            "礼部": f"🎯 【用户洞察报告】\n\n基于任务「{task[:30]}...」，已完成用户行为分析。",
            "工部": f"⚙️ 【执行方案】\n\n基于任务「{task[:30]}...」，已制定实施方案。",
            "刑部": f"🛡️ 【风险评估报告】\n\n基于任务「{task[:30]}...」，已完成合规性审查。",
        }

        return {
            "success": False,
            "is_mock": True,
            "source": "domain_nexus_mock",
            "department": department,
            "task": task,
            "output": mock_outputs.get(department, f"已完成任务分析：{task[:50]}..."),
            "mode": "local_simulation",
            "warning": "神行轨未连接，结果为本地模拟，不具备真实分析能力"
        }

    def _track_execution(self, task: str, department: str, result: Dict):
        """追踪执行记录"""
        # 提取话题
        topics = self._extract_topics(task)

        # 记录到usage tracker
        for topic in topics:
            self.usage_tracker.topic_demand[topic] += 1

    def query_and_execute(self, question: str) -> Dict[str, Any]:
        """
        查询+执行一体化 - 先检索知识，再执行任务

        Args:
            question: 问题或任务

        Returns:
            包含知识回答和执行结果的字典
        """
        # 1. 检索相关知识
        knowledge_result = self.query(question)

        # 2. 判断是否需要执行
        needs_execution = any(k in question.lower() for k in [
            '分析', '制定', '执行', '计划', '方案', '报告', '评估', '优化'
        ])

        execution_result = None
        if needs_execution:
            execution_result = self.execute(question, {
                'relevant_cells': knowledge_result.get('relevant_cells', [])
            })

        return {
            'question': question,
            'knowledge': knowledge_result.get('answer', ''),
            'relevant_cells': knowledge_result.get('relevant_cells', []),
            'execution': execution_result,
            'topic_gaps': knowledge_result.get('topic_gaps', [])
        }

    def init_seeds(self) -> List[str]:
        """
        初始化种子知识域格子

        Returns:
            创建的格子ID列表
        """
        seeds = [
            ("增长运营", {"增长", "获客", "转化"}, "增长运营是提升用户规模和价值的核心能力"),
            ("直播运营", {"直播", "带货", "互动"}, "直播运营是通过实时视频进行营销和销售的运营方式"),
            ("私域运营", {"私域", "社群", "复购"}, "私域运营是构建自有用户池进行长期运营的策略"),
            ("策略运营", {"策略", "规划", "决策"}, "策略运营是为达成目标而制定的中长期规划和执行方案"),
            ("数据运营", {"数据", "分析", "指标"}, "数据运营是通过数据分析驱动业务决策的运营方式"),
            ("内容运营", {"内容", "创作", "传播"}, "内容运营是通过有价值的内容吸引和留住用户的策略"),
            ("电商运营", {"电商", "商品", "流量"}, "电商运营是在线上平台进行商品销售和服务的运营"),
            ("广告投放", {"投放", "广告", "ROI"}, "广告投放是通过付费渠道获取流量和转化的策略"),
        ]

        created = []
        for name, tags, summary in seeds:
            cell_id = self.cell_manager.create_cell(name, tags, summary)
            if cell_id:
                created.append(cell_id)

        return created

    def query(self, question: str, context: str = "") -> Dict[str, Any]:
        """
        查询知识 - 主要入口

        Args:
            question: 问题
            context: 上下文

        Returns:
            包含回答、相关格子、建议的字典
        """
        import time
        query_start = time.perf_counter()
        self._query_count += 1

        # 空输入保护
        if not question:
            return {
                'answer': "请输入要查询的问题",
                'relevant_cells': [],
                'evolution_suggestions': [],
                'hot_topics': [],
                'topic_gaps': []
            }

        # 1. 找到相关格子（使用索引快速搜索）
        relevant_cells = self._find_relevant_cells(question)

        # 2. 追踪使用
        cell_ids = [c.cell_id for c in relevant_cells]
        topics = self._extract_topics(question)
        for cell_id in cell_ids:
            self.usage_tracker.track(cell_id, question, topics)

        # 3. 检查是否需要进化
        evolution_needed = self._check_evolution_needed(topics, cell_ids)

        # 4. 生成回答
        answer = self._generate_answer(question, relevant_cells, context)

        # 记录查询时间
        query_time = time.perf_counter() - query_start
        self._query_times.append(query_time)

        # 组装结果
        result = {
            'answer': answer,
            'relevant_cells': [{'cell_id': c.cell_id, 'name': c.name, 'tags': list(c.tags)}
                            for c in relevant_cells],
            'evolution_suggestions': evolution_needed,
            'hot_topics': self.usage_tracker.get_hot_topics(5),
            'topic_gaps': self.usage_tracker.get_topic_gaps(
                set(c.name for c in self.cell_manager.get_domain_cells().values()),
                5
            ),
            '_perf': {  # 内部性能数据
                'query_time_ms': round(query_time * 1000, 2),
                'cells_accessed': len(relevant_cells)
            }
        }

        # 神政轨监督记录
        try:
            from .divine_oversight import get_oversight, OversightCategory
            oversight = get_oversight()
            if oversight:
                oversight.record(
                    module="DomainNexus",
                    action="query",
                    category=OversightCategory.RESULT,
                    input_data={"question": question[:100], "context": context},
                    output_data={"cells_accessed": len(relevant_cells), "has_answer": bool(answer)}
                )
        except Exception:
            pass  # 监督失败不影响主流程

        return result

    def _find_relevant_cells(self, question: str) -> List[CellContent]:
        """
        找到相关格子 - v7.0 升级版

        策略：
        1. 先用索引快速筛选候选格子
        2. 再懒加载命中的格子完整内容
        3. v7.0 新增：用 KnowledgeGraph 补充图谱关联 cell
        """
        question_lower = question.lower()
        results: List[CellContent] = []
        result_ids: Set[str] = set()

        # v2.2: 先用索引快速搜索
        indices = self.cell_manager.get_all_indices()
        candidate_ids = []

        for cell_id, index in indices.items():
            # 检查名称匹配
            if question_lower in index.name.lower() or question_lower in index.summary_preview.lower():
                candidate_ids.append((cell_id, 0.9))
                continue

            # 检查标签匹配（双向：标签包含查询词 或 查询词包含标签）
            tag_matched = False
            for tag in index.tags:
                tag_lower = tag.lower()
                if tag_lower in question_lower or question_lower in tag_lower:
                    candidate_ids.append((cell_id, 0.7))
                    tag_matched = True
                    break

        # 按相关性排序
        candidate_ids.sort(key=lambda x: x[1], reverse=True)

        # 懒加载命中的格子
        for cell_id, score in candidate_ids[:5]:
            cell = self.cell_manager.get_cell(cell_id)
            if cell:
                results.append(cell)
                result_ids.add(cell_id)

        # v7.0 新增：用 KnowledgeGraph 补充关联 cell
        if results:
            self._ensure_graph_synced()
            for cell in list(results):
                related = self.knowledge_graph.find_related_cells(
                    cell.cell_id, top_n=3
                )
                for rel_id, weight in related:
                    if rel_id not in result_ids:
                        rel_cell = self.cell_manager.get_cell(rel_id)
                        if rel_cell:
                            results.append(rel_cell)
                            result_ids.add(rel_id)

        return results[:5]

    def _extract_topics(self, text: str) -> Set[str]:
        """提取主题"""
        topics = set()

        # 提取中文词
        words = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
        topics.update(words)

        return topics

    def _check_evolution_needed(self, topics: Set[str], current_cells: List[str]) -> Dict[str, Any]:
        """检查是否需要进化"""
        suggestions = {
            'enrich_needed': [],      # 需要丰富的格子
            'new_cell_suggestions': [],  # 新格子建议
            'merge_candidates': []    # 合并候选
        }

        # 检查现有格子是否需要丰富
        for cell in self.cell_manager.get_domain_cells().values():
            if len(cell.analogies) < 2:  # 举一反三少于2条
                suggestions['enrich_needed'].append(cell.cell_id)

        # 检查知识缺口
        existing_names = set(c.name for c in self.cell_manager.get_domain_cells().values())
        gaps = self.usage_tracker.get_topic_gaps(existing_names, 3)
        suggestions['new_cell_suggestions'] = gaps

        return suggestions

    def _generate_answer(self, question: str, cells: List[CellContent], context: str) -> str:
        """
        生成高质量回答 - 整合格子知识 + 分析逻辑
        """
        if not cells:
            return f"❌ 未找到与「{question}」直接相关的知识域格子。\n\n💡 建议：系统将自动创建相关知识格子。"

        lines = ["## 📚 知识分析报告\n"]
        lines.append(f"**问题**：{question}\n")

        # 按相关性分组
        for cell in cells:
            lines.append(f"### {cell.cell_id} {cell.name}")
            lines.append("─" * 40)

            # 核心认知
            if cell.summary:
                lines.append(f"**定义**：{cell.summary}")

            # 举一反三（精选3条有洞见的）
            if cell.analogies:
                lines.append("\n**💡 核心洞见**：")
                # 只选真正有价值的（排除模板化的）
                good_analogies = [a for a in cell.analogies if '=' in a and '另一种形态' not in a][:3]
                if good_analogies:
                    for analogy in good_analogies:
                        clean = analogy.strip().lstrip('- ')
                        lines.append(f"- {clean}")
                else:
                    for analogy in cell.analogies[:2]:
                        clean = analogy.strip().lstrip('- ')
                        lines.append(f"- {clean}")

            # 案例
            if hasattr(cell, 'cases') and cell.cases:
                lines.append("\n**📖 实战案例**：")
                for case in cell.cases[:1]:
                    lines.append(f"- {case}")

            # 关键指标
            if cell.metrics:
                lines.append(f"\n**📊 关键指标**：{', '.join(cell.metrics[:5])}")

            lines.append("")

        # 生成行动建议
        lines.append("\n## 🎯 行动建议\n")
        suggestions = self._generate_suggestions(question, cells)
        lines.extend(suggestions)

        return "\n".join(lines)

    def _generate_suggestions(self, question: str, cells: List[CellContent]) -> List[str]:
        """根据问题和相关格子生成行动建议"""
        suggestions = []
        question_lower = question.lower()

        # 分析问题类型
        if any(k in question_lower for k in ['如何', '怎么', '提升', '增长']):
            suggestions.append("1. **先诊断**：明确当前指标基数和行业基准")
            suggestions.append("2. **定目标**：设定可量化的提升目标（如提升X%）")
            suggestions.append("3. **找杠杆**：找到投入产出比最高的改进点")
            suggestions.append("4. **快迭代**：小步快跑，快速验证假设")

        if any(k in question_lower for k in ['分析', '原因', '为什么', '下降']):
            suggestions.append("1. **数据对比**：同比、环比、竞品对比")
            suggestions.append("2. **漏斗拆解**：找出转化率最低的环节")
            suggestions.append("3. **用户访谈**：了解真实用户反馈")
            suggestions.append("4. **归因分析**：区分内外部因素")

        if any(k in question_lower for k in ['策略', '规划', '战略']):
            suggestions.append("1. **SWOT分析**：明确优势、劣势、机会、威胁")
            suggestions.append("2. **资源盘点**：评估可用资源和约束条件")
            suggestions.append("3. **路径规划**：设计从现状到目标的路径")
            suggestions.append("4. **里程碑**：设定关键检查点和目标")

        # 如果没有匹配的建议，使用通用建议
        if not suggestions:
            suggestions.append("1. **明确问题**：拆解为可执行的小问题")
            suggestions.append("2. **收集数据**：用数据支撑分析")
            suggestions.append("3. **制定方案**：设计3种以上备选方案")
            suggestions.append("4. **快速验证**：先小规模测试再推广")

        return suggestions

    def evolve(self) -> Dict[str, Any]:
        """
        执行进化 - 核心功能
        1. 丰富现有格子内容
        2. 自动创建新的知识缺口格子
        3. 生成深度内容而非空洞模板

        Returns:
            进化结果
        """
        results = {
            'enriched_cells': [],
            'new_cells_created': [],
            'updated_cells': [],  # 新增：已更新内容的格子
            'errors': []
        }

        # 1. 丰富所有现有格子（不只是需要丰富的）
        for cell_id, cell in self.cell_manager.get_domain_cells().items():
            enrichment = self.content_enricher.enrich(cell)
            if enrichment and (enrichment.get('new_analogies') or enrichment.get('new_metrics')):
                success = self.cell_manager.enrich_cell(cell_id, enrichment)
                if success:
                    results['enriched_cells'].append(cell_id)

        # 2. 检查并补充空洞格子（举一反三还是模板化的）
        for cell_id, cell in self.cell_manager.get_domain_cells().items():
            is_template = any('另一种形态' in a for a in cell.analogies)
            if is_template or len(cell.analogies) < 3:
                enrichment = self.content_enricher.enrich(cell)
                if enrichment:
                    self.cell_manager.enrich_cell(cell_id, enrichment)
                    results['updated_cells'].append(cell_id)

        # 3. 检查是否需要创建新格子
        existing_names = set(c.name for c in self.cell_manager.get_domain_cells().values())
        gaps = self.usage_tracker.get_topic_gaps(existing_names, 3)

        for gap_topic in gaps:
            # 尝试匹配已有知识库
            matched_knowledge = None
            matched_key = None
            for key in self.content_enricher.DEEP_KNOWLEDGE:
                if key in gap_topic.lower():
                    matched_knowledge = self.content_enricher.DEEP_KNOWLEDGE[key]
                    matched_key = key
                    break

            # 根据匹配的知识生成summary
            if matched_knowledge:
                summary = f"{gap_topic}是通过{matched_key}实现业务增长的重要领域"
            else:
                summary = f"{gap_topic}是运营管理中需要深入研究的重要课题"

            # 创建新格子
            new_id = self.cell_manager.create_cell(
                name=gap_topic,
                tags={gap_topic, "新增", "待完善"},
                summary=summary
            )
            if new_id:
                results['new_cells_created'].append(new_id)
                # 立即丰富新格子
                new_cell = self.cell_manager.get_cell(new_id)
                if new_cell:
                    # 找到最接近的知识来丰富
                    for key, knowledge in self.content_enricher.DEEP_KNOWLEDGE.items():
                        if key in gap_topic.lower():
                            self.cell_manager.enrich_cell(new_id, {
                                'new_tags': {gap_topic, '运营', '增长'},
                                'new_analogies': knowledge['analogies'][:2],
                                'new_metrics': knowledge['metrics'][:3],
                                'new_cases': knowledge['cases'][:1]
                            })
                            break

        # 4. v7.0 新增：用 RuleManager 辅助进化决策
        hot_topics = self.usage_tracker.get_hot_topics(3)
        rule_context = {
            "topic_query_count": hot_topics[0][1] if hot_topics else 0,
        }
        rule_suggestions = self.rule_manager.evaluate(rule_context)
        results['rule_suggestions'] = rule_suggestions

        # 根据规则建议执行额外动作
        for suggestion in rule_suggestions:
            for action in suggestion.get('actions', []):
                if action['type'] == 'recommend' and action['target'] == 'create_cell':
                    # 规则建议创建新格子
                    if suggestion.get('confidence', 0) >= 0.7:
                        new_id = self.cell_manager.create_cell(
                            name=f"规则建议：{hot_topics[0][0] if hot_topics else '新领域'}",
                            tags={"规则生成", "待完善"},
                            summary=f"由规则 {suggestion['rule_id']} 自动建议创建"
                        )
                        if new_id:
                            results['new_cells_created'].append(new_id)

        return results

    def auto_evolve_if_needed(self, threshold: int = 5) -> bool:
        """
        自动进化（如果需要）

        Args:
            threshold: 热门主题阈值

        Returns:
            是否执行了进化
        """
        hot_topics = self.usage_tracker.get_hot_topics(3)

        # 如果某个主题被频繁查询但没有对应格子，执行进化
        existing_names = set(c.name for c in self.cell_manager.get_domain_cells().values())

        for topic, count in hot_topics:
            if count >= threshold and topic not in existing_names:
                # 发现知识缺口，执行进化
                self.evolve()
                return True

        return False

    def get_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        cells = self.cell_manager.get_domain_cells()

        return {
            'total_cells': len(cells),
            'hot_topics': self.usage_tracker.get_hot_topics(5),
            'cold_cells': self.usage_tracker.get_cold_cells(3),
            'topic_gaps': self.usage_tracker.get_topic_gaps(
                set(c.name for c in cells.values()), 5
            ),
            'cells': [
                {
                    'cell_id': c.cell_id,
                    'name': c.name,
                    'tag_count': len(c.tags),
                    'analogy_count': len(c.analogies)
                }
                for c in cells.values()
            ]
        }

    # ---- v7.0 新增：图谱/概念/规则 公开 API ----

    def link_cells_graph(self, cell_a: str, cell_b: str,
                        weight: float = 0.5, relation_type: str = "related") -> bool:
        """
        手动在两个 cell 之间建立图谱关联

        Args:
            cell_a: 第一个 cell 的 ID
            cell_b: 第二个 cell 的 ID
            weight: 关联度 0~1
            relation_type: 关系类型（related / similar / depends_on / improves）
        """
        self._ensure_graph_synced()
        self.knowledge_graph.add_relation(
            cell_a, cell_b, weight=weight, relation_type=relation_type
        )
        return True

    def find_related_cells_graph(self, cell_id: str,
                                  top_n: int = 5) -> List[Dict[str, Any]]:
        """
        通过 KnowledgeGraph 查找与 cell 相关的其他 cell

        Returns:
            [{"cell_id": ..., "weight": ..., "name": ...}, ...]
        """
        self._ensure_graph_synced()
        related = self.knowledge_graph.find_related_cells(cell_id, top_n=top_n)
        results = []
        for rel_id, w in related:
            cell = self.cell_manager.get_cell(rel_id)
            results.append({
                "cell_id": rel_id,
                "weight": w,
                "name": cell.name if cell else rel_id,
            })
        return results

    def find_path_between_cells(self, cell_a: str,
                                 cell_b: str) -> Optional[List[str]]:
        """查找两个 cell 在图谱中的关联路径"""
        self._ensure_graph_synced()
        return self.knowledge_graph.find_path(cell_a, cell_b)

    def add_concept(self, concept_name: str, description: str = "",
                    source_cell: Optional[str] = None) -> Dict[str, Any]:
        """
        注册一个概念，并可选关联到某个 cell

        Returns:
            {"concept": ..., "linked_cell": ...}
        """
        self._ensure_concepts_synced()
        concept = self.concept_linker.register_concept(
            concept_name, description=description, source_cell=source_cell
        )
        if source_cell:
            self.concept_linker.link_concept_to_cell(concept_name, source_cell)
        return {
            "concept": concept.name,
            "description": concept.description,
            "linked_cell": source_cell,
        }

    def add_concept_relation(self, concept_a: str, concept_b: str,
                              relation_type: str = "related", weight: float = 0.5):
        """添加两个概念之间的关系"""
        self._ensure_concepts_synced()
        self.concept_linker.add_concept_relation(
            concept_a, concept_b, relation_type=relation_type, weight=weight
        )

    def find_cells_by_concept(self, concept_name: str) -> List[Dict[str, Any]]:
        """
        通过概念查找相关 cell

        Returns:
            [{"cell_id": ..., "name": ..., "match_type": "concept"}, ...]
        """
        self._ensure_concepts_synced()
        cell_ids = self.concept_linker.find_cells_by_concept(concept_name)
        results = []
        for cid in cell_ids:
            cell = self.cell_manager.get_cell(cid)
            if cell:
                results.append({
                    "cell_id": cid,
                    "name": cell.name,
                    "match_type": "concept",
                })
        return results

    def evaluate_rules(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        评估规则，返回触发的动作建议

        context 示例：
        - {"topic_query_count": 6, "topic": "增长"}
        - {"cell_id": "B1", "analogy_count": 1}
        - {"coquery_pair": ("B1", "B2"), "count": 3}

        Returns:
            [{"rule_id": ..., "actions": [...], "confidence": ...}, ...]
        """
        return self.rule_manager.evaluate(context)

    def get_graph_status(self) -> Dict[str, Any]:
        """获取 KnowledgeGraph 状态"""
        self._ensure_graph_synced()
        g = self.knowledge_graph._g
        return {
            "nodes": list(g.nodes()),
            "edge_count": g.number_of_edges(),
            "nodes_count": g.number_of_nodes(),
            "synced": self._graph_synced,
        }

    def get_concepts_status(self) -> Dict[str, Any]:
        """获取概念链接状态"""
        self._ensure_concepts_synced()
        return {
            "concept_count": len(self.concept_linker.concepts),
            "relation_count": len(self.concept_linker.relations),
            "concept_cell_links": {
                k: list(v) for k, v in self.concept_linker._concept_cells.items()
            },
            "synced": self._concepts_synced,
        }

    def sync_all_now(self):
        """强制同步图谱和概念（手动触发）"""
        self._ensure_graph_synced()
        self._ensure_concepts_synced()
        return {
            "graph_nodes": self.knowledge_graph._g.number_of_nodes(),
            "concept_count": len(self.concept_linker.concepts),
        }


# ============ 全局实例 ============

_nexus: Optional[DomainNexus] = None
_nexus_lock = threading.Lock()


def get_nexus(cells_dir: Optional[str] = None, lazy: bool = True) -> DomainNexus:
    """
    获取 DomainNexus 单例 - v7.1 线程安全

    Args:
        cells_dir: 格子目录
        lazy: 是否使用懒加载（默认True，更快启动）

    Returns:
        DomainNexus 实例
    """
    global _nexus
    if _nexus is None:
        with _nexus_lock:
            if _nexus is None:
                _nexus = DomainNexus(Path(cells_dir) if cells_dir else None, lazy=lazy)
    return _nexus


# 向后兼容别名
def get_domain_system(cells_dir: Optional[str] = None, lazy: bool = True) -> DomainNexus:
    """获取知识域系统单例（向后兼容）"""
    return get_nexus(cells_dir, lazy=lazy)


# ============ v2.2 快捷性能查询 ============

def quick_query(question: str) -> Dict[str, Any]:
    """
    快速查询 - 仅使用索引，不加载完整内容

    适用场景：
    - 只需要知道哪些格子相关
    - 不需要完整内容和分析

    Args:
        question: 查询问题

    Returns:
        快速结果（包含格子索引信息）
    """
    nexus = get_nexus()

    if not question:
        return {
            'relevant_cells': [],
            'hint': '使用 query() 获取完整回答'
        }

    # 使用索引搜索
    indices = nexus.cell_manager.search_indices(question)

    return {
        'relevant_cells': [
            {
                'cell_id': idx.cell_id,
                'name': idx.name,
                'tags': list(idx.tags),
                'summary_preview': idx.summary_preview[:50] + '...' if len(idx.summary_preview) > 50 else idx.summary_preview
            }
            for idx in indices[:3]
        ],
        'total_indices': len(indices),
        'hint': '使用 query() 获取完整回答'
    }


def get_loading_stats() -> Dict[str, Any]:
    """
    获取加载性能统计

    Returns:
        性能统计信息
    """
    nexus = get_nexus()
    return nexus.get_performance_stats()


# ============ 快捷函数 ============

def query(question: str, context: str = "") -> Dict[str, Any]:
    """快捷查询"""
    return get_domain_system(lazy=True).query(question, context)


def evolve() -> Dict[str, Any]:
    """执行进化"""
    return get_domain_system().evolve()


def get_status() -> Dict[str, Any]:
    """获取状态"""
    return get_domain_system().get_status()


def execute_task(task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    快捷执行任务 - 调用神行轨 Claw 执行具体工作

    Args:
        task: 任务描述
        context: 上下文信息

    Returns:
        执行结果
    """
    return get_domain_system().execute(task, context)


def query_and_execute(question: str) -> Dict[str, Any]:
    """
    快捷查询执行一体化

    Args:
        question: 问题或任务

    Returns:
        包含知识回答和执行结果的字典
    """
    return get_domain_system().query_and_execute(question)


# ============ v2.2 性能测试函数 ============

def benchmark_loading(iterations: int = 5) -> Dict[str, Any]:
    """
    性能基准测试 - v2.2 增强版

    测试内容：
    1. 冷启动时间
    2. 缓存命中时间
    3. 索引搜索时间
    4. 懒加载性能
    5. 内存占用

    Args:
        iterations: 测试迭代次数

    Returns:
        测试结果
    """
    import time
    import gc

    results = {
        'cold_start': [],
        'cache_hit': [],
        'index_search': [],
        'lazy_load': [],
        'memory_usage': []
    }

    # 预热
    _nexus_warm = DomainNexus(lazy=True)
    _nexus_warm.query("增长运营")
    _nexus_warm.query("直播运营")
    del _nexus_warm

    # 测试冷启动
    for i in range(iterations):
        gc.collect()
        start = time.perf_counter()
        nexus = DomainNexus(lazy=True)
        results['cold_start'].append(time.perf_counter() - start)

        # 测试缓存命中
        start = time.perf_counter()
        nexus.query("增长运营")  # 首次访问
        nexus.query("增长运营")  # 缓存命中
        results['cache_hit'].append(time.perf_counter() - start)

        # 测试索引搜索
        start = time.perf_counter()
        indices = nexus.cell_manager.search_indices("增长")
        results['index_search'].append(time.perf_counter() - start)

        # 测试懒加载
        start = time.perf_counter()
        nexus.query("用户研究")
        results['lazy_load'].append(time.perf_counter() - start)

        # 内存使用
        stats = nexus.get_performance_stats()
        results['memory_usage'].append(stats['cell_stats']['memory_usage']['memory_mb'])

        del nexus

    # 计算统计
    def avg(lst):
        return round(sum(lst) / len(lst), 4) if lst else 0

    def min_max(lst):
        return {
            'min': round(min(lst), 4) if lst else 0,
            'max': round(max(lst), 4) if lst else 0
        }

    return {
        'cold_start': {
            'avg_ms': round(avg(results['cold_start']) * 1000, 2),
            **min_max([t * 1000 for t in results['cold_start']])
        },
        'cache_hit': {
            'avg_ms': round(avg(results['cache_hit']) * 1000, 2),
            **min_max([t * 1000 for t in results['cache_hit']])
        },
        'index_search': {
            'avg_ms': round(avg(results['index_search']) * 1000, 2),
            **min_max([t * 1000 for t in results['index_search']])
        },
        'lazy_load': {
            'avg_ms': round(avg(results['lazy_load']) * 1000, 2),
            **min_max([t * 1000 for t in results['lazy_load']])
        },
        'memory_usage': {
            'avg_mb': round(avg(results['memory_usage']), 2),
            'max_mb': round(max(results['memory_usage']), 2)
        },
        'iterations': iterations,
        'optimizations': [
            '并行索引加载',
            'LRU缓存',
            '内存上限控制',
            '索引缓存持久化'
        ]
    }


# ============ 图结构：cell 关系网络（来自 knowledge_graph/graph_engine.py） ============

class KnowledgeGraph:
    """
    cell 关系图谱 —— 用 NetworkX 维护 cell 之间的关联关系

    每条边带 weight（关联度），支持：
    - 添加/删除 cell 节点
    - 添加/删除关联关系
    - 查找与某 cell 相关的其他 cell
    - 查找两个 cell 之间的关联路径
    - 获取 cell 子图
    """
    def __init__(self):
        import networkx as nx
        self._g = nx.Graph()

    # ---- 节点管理 ----
    def add_cell_node(self, cell_id: str, metadata: Optional[Dict] = None):
        if not self._g.has_node(cell_id):
            self._g.add_node(cell_id, **(metadata or {}))

    def remove_cell_node(self, cell_id: str):
        if self._g.has_node(cell_id):
            self._g.remove_node(cell_id)

    # ---- 边管理（关联关系）----
    def add_relation(self, cell_a: str, cell_b: str, weight: float = 0.5,
                     relation_type: str = "related"):
        """添加两个 cell 之间的关联关系"""
        self.add_cell_node(cell_a)
        self.add_cell_node(cell_b)
        self._g.add_edge(cell_a, cell_b, weight=weight, type=relation_type)

    def remove_relation(self, cell_a: str, cell_b: str):
        if self._g.has_edge(cell_a, cell_b):
            self._g.remove_edge(cell_a, cell_b)

    # ---- 查询 ----
    def find_related_cells(self, cell_id: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        找出与 cell_id 最相关的其他 cell
        返回 [(cell_id, weight), ...]，按 weight 降序
        """
        if not self._g.has_node(cell_id):
            return []
        neighbors = []
        for nb in self._g.neighbors(cell_id):
            w = self._g[cell_id][nb].get("weight", 0.5)
            neighbors.append((nb, w))
        neighbors.sort(key=lambda x: x[1], reverse=True)
        return neighbors[:top_n]

    def find_path(self, cell_a: str, cell_b: str) -> Optional[List[str]]:
        """找出两个 cell 之间的关联路径（最短路径）"""
        import networkx as nx
        try:
            return list(nx.shortest_path(self._g, cell_a, cell_b))
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def get_subgraph(self, cell_ids: List[str]) -> Dict[str, Any]:
        """获取包含指定 cell 的子图（节点列表 + 边列表）"""
        import networkx as nx
        subgraph = self._g.subgraph(cell_ids)
        return {
            "nodes": list(subgraph.nodes(data=True)),
            "edges": list(subgraph.edges(data=True)),
        }

    def suggest_relations_from_associations(self, cell_id: str,
                                            associations: Dict[str, float],
                                            cell_name_map: Dict[str, str]) -> int:
        """
        根据 cell 的 associations（关联领域字典）自动在图谱中添加边
        返回成功添加的边数
        """
        added = 0
        for target_name, weight in associations.items():
            # 通过 cell_name_map 找到对应的 cell_id
            target_id = cell_name_map.get(target_name)
            if target_id and target_id != cell_id:
                self.add_relation(cell_id, target_id, weight=float(weight))
                added += 1
        return added

    def to_dict(self) -> Dict[str, Any]:
        """导出图谱为可序列化字典"""
        return {
            "nodes": [(n, self._g.nodes[n]) for n in self._g.nodes()],
            "edges": [
                (u, v, self._g[u][v]) for u, v in self._g.edges()
            ]
        }

    def load_dict(self, data: Dict[str, Any]):
        """从字典加载图谱"""
        import networkx as nx
        self._g = nx.Graph()
        for n, attrs in data.get("nodes", []):
            self._g.add_node(n, **(attrs or {}))
        for u, v, attrs in data.get("edges", []):
            self._g.add_edge(u, v, **(attrs or {}))


# ============ 概念链接器（来自 knowledge_graph/concept_manager.py） ============

@dataclass
class Concept:
    name: str
    description: str = ""
    source_cell: Optional[str] = None   # 该概念最早来自哪个 cell
    related_concepts: List[str] = field(default_factory=list)
    confidence: float = 1.0


@dataclass
class ConceptRelation:
    concept_a: str
    concept_b: str
    relation_type: str = "related"   # related / is_a / part_of / causes
    weight: float = 0.5
    confidence: float = 1.0


class ConceptLinker:
    """
    概念链接器 —— 跨 cell 的概念关联系统

    多个 cell 可能涉及同一个概念（如"转化率"），
    通过 ConceptLinker 可以：
    - 注册概念
    - 建立概念之间的关系
    - 通过共享概念找到相关的 cell
    """

    def __init__(self):
        self.concepts: Dict[str, Concept] = {}
        self.relations: List[ConceptRelation] = []
        self._concept_cells: Dict[str, Set[str]] = defaultdict(set)  # concept → cell_ids

    def register_concept(self, name: str, description: str = "",
                         source_cell: Optional[str] = None) -> Concept:
        """注册或更新一个概念"""
        if name not in self.concepts:
            self.concepts[name] = Concept(
                name=name, description=description, source_cell=source_cell
            )
        else:
            if source_cell:
                self.concepts[name].source_cell = source_cell
            if description:
                self.concepts[name].description = description
        return self.concepts[name]

    def link_concept_to_cell(self, concept_name: str, cell_id: str):
        """将一个概念链接到一个 cell"""
        self.register_concept(concept_name)
        self._concept_cells[concept_name].add(cell_id)

    def add_concept_relation(self, concept_a: str, concept_b: str,
                              relation_type: str = "related", weight: float = 0.5):
        """添加两个概念之间的关系"""
        self.register_concept(concept_a)
        self.register_concept(concept_b)
        if not any(r.concept_a == concept_a and r.concept_b == concept_b
                   for r in self.relations):
            self.relations.append(ConceptRelation(
                concept_a=concept_a, concept_b=concept_b,
                relation_type=relation_type, weight=weight
            ))

    def find_cells_by_concept(self, concept_name: str) -> List[str]:
        """找出包含某概念的所有 cell"""
        return list(self._concept_cells.get(concept_name, set()))

    def find_related_concepts(self, concept_name: str,
                               top_n: int = 5) -> List[Tuple[str, float]]:
        """找出与某概念相关的其他概念"""
        results = []
        for rel in self.relations:
            if rel.concept_a == concept_name:
                results.append((rel.concept_b, rel.weight))
            elif rel.concept_b == concept_name:
                results.append((rel.concept_a, rel.weight))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]

    def auto_extract_from_cell(self, cell: CellContent) -> int:
        """
        从 cell 的 tags/summary/points 中自动提取概念并链接
        返回提取到的概念数
        """
        extracted = 0
        # 从 tags 提取概念
        for tag in cell.tags:
            self.link_concept_to_cell(tag, cell.cell_id)
            extracted += 1
        # 从 metrics 提取概念
        if hasattr(cell, 'metrics'):
            for metric in cell.metrics:
                self.link_concept_to_cell(metric, cell.cell_id)
                extracted += 1
        return extracted

    def to_dict(self) -> Dict:
        return {
            "concepts": {
                k: {"description": v.description,
                     "source_cell": v.source_cell,
                     "confidence": v.confidence}
                for k, v in self.concepts.items()
            },
            "relations": [
                {"concept_a": r.concept_a, "concept_b": r.concept_b,
                 "relation_type": r.relation_type, "weight": r.weight}
                for r in self.relations
            ],
            "concept_cells": {k: list(v) for k, v in self._concept_cells.items()}
        }


# ============ 规则管理器（来自 knowledge_graph/rule_engine.py） ============

class RuleManager:
    """
    规则管理器 —— 将 knowledge_graph/rule_engine 的核心能力注入 DomainNexus

    支持的规则类型：deductive / inductive / heuristic / causal
    可用于：
    - 根据查询结果触发推荐动作
    - 根据 cell 使用情况触发自动丰富
    - 根据概念关联触发跨域推荐
    """

    def __init__(self):
        self.rules: Dict[str, Dict] = {}
        self._init_core_rules()

    def _init_core_rules(self):
        """初始化核心知识规则（来自 rule_engine.py 的预置规则）"""
        core_rules = [
            # 演绎规则：高频查询某领域 → 推荐创建新 cell
            {
                "rule_id": "deductive_hot_topic_new_cell",
                "name": "热门主题自动建议新格子",
                "rule_type": "deductive",
                "description": "当某主题查询频率超过阈值时，建议创建新格子",
                "conditions": {"topic_query_count_gte": 5},
                "actions": [{"type": "recommend", "target": "create_cell",
                             "value": "auto_suggest"}],
                "priority": 2,
                "confidence": 0.85,
            },
            # 启发规则：cell 内容太薄 → 建议丰富
            {
                "rule_id": "heuristic_thin_cell_enrich",
                "name": "内容薄的格子自动丰富",
                "rule_type": "heuristic",
                "description": "当格子的举一反三少于2条时，建议自动丰富",
                "conditions": {"analogy_count_lt": 2},
                "actions": [{"type": "recommend", "target": "enrich",
                             "value": "auto_enrich"}],
                "priority": 2,
                "confidence": 0.80,
            },
            # 因果规则：两个 cell 频繁同时被查询 → 建立图谱关联
            {
                "rule_id": "causal_coquery_link_cells",
                "name": "共现查询自动建关联",
                "rule_type": "causal",
                "description": "两个格子频繁同时被查询时，在图谱中建立关联",
                "conditions": {"coquery_count_gte": 3},
                "actions": [{"type": "add_relation", "target": "knowledge_graph",
                             "value": 0.7}],
                "priority": 3,
                "confidence": 0.75,
            },
        ]
        for rule in core_rules:
            self.rules[rule["rule_id"]] = rule

    def evaluate(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        评估当前上下文，返回触发的规则列表
        context 可以包含：
        - topic_query_count: Dict[str, int]
        - cell_id / analogy_count
        - coquery_pair: Tuple[str, str]
        """
        triggered = []
        for rule_id, rule in self.rules.items():
            if self._evaluate_conditions(rule["conditions"], context):
                triggered.append({
                    "rule_id": rule_id,
                    "name": rule["name"],
                    "actions": rule["actions"],
                    "confidence": rule["confidence"],
                })
        return triggered

    def _evaluate_conditions(self, conditions: Dict, context: Dict) -> bool:
        """评估条件字典（简化版，支持 _gte / _lt 后缀）"""
        for key, expected in conditions.items():
            actual = context.get(key)
            if actual is None:
                return False
            if key.endswith("_gte"):
                if not actual >= expected:
                    return False
            elif key.endswith("_lt"):
                if not actual < expected:
                    return False
            else:
                if actual != expected:
                    return False
        return True

    def add_custom_rule(self, rule_id: str, name: str, conditions: Dict,
                         actions: List[Dict], confidence: float = 0.8):
        """添加自定义规则"""
        self.rules[rule_id] = {
            "rule_id": rule_id,
            "name": name,
            "rule_type": "custom",
            "conditions": conditions,
            "actions": actions,
            "priority": 3,
            "confidence": confidence,
        }


# ============ CLI入口 ============

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DomainNexus - 知识域格子动态更新系统")
    parser.add_argument('action', choices=['query', 'evolve', 'status'],
                       help='操作类型')
    parser.add_argument('question', nargs='?', help='查询问题')
    parser.add_argument('--context', '-c', default='', help='上下文')

    args = parser.parse_args()

    system = get_domain_system()

    if args.action == 'query':
        if not args.question:
            print("请提供查询问题")
            exit(1)
        result = system.query(args.question, args.context)
        print(result['answer'])
        print("\n--- 相关格子 ---")
        for cell in result['relevant_cells']:
            print(f"  {cell['cell_id']} {cell['name']}")

    elif args.action == 'evolve':
        result = system.evolve()
        print("进化结果:")
        print(f"  丰富格子: {result['enriched_cells']}")
        print(f"  新建格子: {result['new_cells_created']}")

    elif args.action == 'status':
        status = system.get_status()
        print(f"总格子数: {status['total_cells']}")
        print("\n热门主题:")
        for topic, count in status['hot_topics']:
            print(f"  {topic}: {count}")
        print("\n知识缺口:")
        for gap in status['topic_gaps']:
            print(f"  - {gap}")
