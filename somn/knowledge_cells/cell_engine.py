"""
知识格子引擎 v1.0
================
动态加载和使用21个知识格子的系统

功能：
- 动态加载Markdown格子文件
- 格子关联检索
- 激活计数和更新
- 跨格子知识整合

来源：基于legacy格子系统设计迁移优化
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime


class KnowledgeCell:
    """知识格子"""
    
    def __init__(self, cell_id: str, file_path: Path):
        self.cell_id = cell_id
        self.file_path = file_path
        self.name = ""
        self.tags: Set[str] = set()
        self.associations: Dict[str, float] = {}  # 关联格子及权重
        self.activation_count = 0
        self.last_activation = None
        self.content: Dict[str, str] = {}  # 各区块内容
        self._load()
    
    def _load(self):
        """加载格子内容"""
        if not self.file_path.exists():
            return
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析元信息（包含元信息和标签）
        meta_match = re.search(r'## 元信息\s*\n(.*?)(?=\n## 核心摘要|\n## 举一反三|\n## 关联|\Z)', content, re.DOTALL)
        if meta_match:
            self._parse_meta(meta_match.group(1))
        
        # 解析标签（单独处理）
        tags_match = re.search(r'## 标签\s*\n(.+?)(?=\n## |\Z)', content, re.DOTALL)
        if tags_match:
            self.tags = set(t.strip() for t in re.split(r'[,，]', tags_match.group(1)) if t.strip())
        
        # 解析核心摘要
        summary_match = re.search(r'## 核心摘要\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if summary_match:
            self._parse_summary(summary_match.group(1))
        
        # 解析举一反三
        analogy_match = re.search(r'## 举一反三\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if analogy_match:
            self.content['analogy'] = analogy_match.group(1).strip()
        
        # 解析关联领域
        assoc_match = re.search(r'## 关联领域\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if assoc_match:
            self._parse_associations(assoc_match.group(1))
    
    def _parse_meta(self, meta_text: str):
        """解析元信息区块"""
        # 从文件内容获取名称
        with open(self.file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        match = re.match(r'#\s*([A-Z]\d)_(.+)', first_line)
        if match:
            self.name = match.group(2).strip()
        
        # 激活次数
        act_match = re.search(r'激活次数[：:]\s*(\d+)', meta_text)
        if act_match:
            self.activation_count = int(act_match.group(1))
        
        # 上次激活
        last_match = re.search(r'上次激活[：:]\s*(.+)', meta_text)
        if last_match:
            self.last_activation = last_match.group(1).strip()
    
    def _parse_summary(self, summary_text: str):
        """解析核心摘要"""
        # 这是什么
        what_match = re.search(r'### 这是什么\s*\n(.+?)(?=\n### |\Z)', summary_text, re.DOTALL)
        if what_match:
            self.content['what'] = what_match.group(1).strip()
        
        # 核心要点
        points_match = re.search(r'### 核心要点\s*\n(.+?)(?=\n### |\Z)', summary_text, re.DOTALL)
        if points_match:
            self.content['points'] = points_match.group(1).strip()
    
    def _parse_associations(self, assoc_text: str):
        """解析关联领域"""
        for line in assoc_text.strip().split('\n'):
            match = re.match(r'- (.+?)（关联度：([\d.]+)）', line)
            if match:
                cell_name = match.group(1).strip()
                weight = float(match.group(2))
                self.associations[cell_name] = weight
    
    def activate(self):
        """激活格子"""
        self.activation_count += 1
        self.last_activation = datetime.now().strftime('%Y-%m-%d')
        self._save_meta()
    
    def _save_meta(self):
        """保存元信息更新"""
        if not self.file_path.exists():
            return
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新激活次数
        content = re.sub(
            r'激活次数：\d+',
            f'激活次数：{self.activation_count}',
            content
        )
        
        # 更新上次激活
        content = re.sub(
            r'## 上次激活\s*\n.*',
            f'## 上次激活\n{self.last_activation}',
            content
        )
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def get_related_cells(self, threshold: float = 0.6) -> List[tuple]:
        """获取高关联格子"""
        return [(name, weight) for name, weight in self.associations.items() 
                if weight >= threshold]
    
    def __repr__(self):
        return f"KnowledgeCell({self.cell_id}: {self.name}, activations={self.activation_count})"


class KnowledgeCellEngine:
    """知识格子引擎"""
    
    def __init__(self, cells_dir: Optional[str] = None):
        if cells_dir is None:
            self.cells_dir = Path(__file__).parent
        else:
            self.cells_dir = Path(cells_dir)
        
        self.cells: Dict[str, KnowledgeCell] = {}
        self._load_all_cells()
    
    def _load_all_cells(self):
        """加载所有格子"""
        if not self.cells_dir.exists():
            return
        
        for md_file in self.cells_dir.glob("*.md"):
            if md_file.stem == "INDEX":
                continue
            
            # 解析格子ID
            match = re.match(r'([A-Z]\d)_(.+)', md_file.stem)
            if match:
                cell_id = match.group(1)
                self.cells[cell_id] = KnowledgeCell(cell_id, md_file)
    
    def get_cell(self, cell_id: str) -> Optional[KnowledgeCell]:
        """获取指定格子"""
        return self.cells.get(cell_id)
    
    def activate_cell(self, cell_id: str) -> bool:
        """激活格子"""
        cell = self.cells.get(cell_id)
        if cell:
            cell.activate()
            return True
        return False
    
    def find_related(self, cell_id: str, threshold: float = 0.6) -> List[KnowledgeCell]:
        """查找关联格子"""
        cell = self.cells.get(cell_id)
        if not cell:
            return []
        
        related = []
        for related_name, weight in cell.associations.items():
            if weight >= threshold:
                # 找到关联格子
                for cid, c in self.cells.items():
                    if c.name == related_name:
                        related.append((c, weight))
                        break
        
        return related
    
    def search_by_tags(self, tags: Set[str]) -> List[KnowledgeCell]:
        """按标签搜索"""
        results = []
        for cell in self.cells.values():
            if cell.tags & tags:
                results.append(cell)
        return results
    
    def search_by_content(self, keyword: str) -> List[KnowledgeCell]:
        """按内容搜索"""
        results = []
        keyword_lower = keyword.lower()
        for cell in self.cells.values():
            if keyword_lower in cell.content.get('what', '').lower():
                results.append(cell)
                continue
            if keyword_lower in cell.content.get('points', '').lower():
                results.append(cell)
                continue
        return results
    
    def get_hot_cells(self, top_n: int = 5) -> List[KnowledgeCell]:
        """获取最热格子"""
        sorted_cells = sorted(
            self.cells.values(),
            key=lambda c: c.activation_count,
            reverse=True
        )
        return sorted_cells[:top_n]
    
    def get_analogy(self, cell_id: str) -> Optional[str]:
        """获取举一反三内容"""
        cell = self.cells.get(cell_id)
        if cell:
            return cell.content.get('analogy')
        return None
    
    def get_knowledge_graph(self) -> Dict:
        """获取知识图谱"""
        nodes = []
        links = []
        
        for cell in self.cells.values():
            nodes.append({
                'id': cell.cell_id,
                'name': cell.name,
                'activations': cell.activation_count,
                'category': 'core' if cell.cell_id.startswith('A') else 'domain'
            })
            
            for related_name, weight in cell.associations.items():
                # 找到关联格子ID
                for cid, c in self.cells.items():
                    if c.name == related_name:
                        links.append({
                            'source': cell.cell_id,
                            'target': cid,
                            'weight': weight
                        })
                        break
        
        return {'nodes': nodes, 'links': links}
    
    def summarize(self) -> str:
        """获取格子系统摘要"""
        total_activations = sum(c.activation_count for c in self.cells.values())
        hot_cells = self.get_hot_cells(3)
        
        lines = [
            "📊 知识格子系统状态",
            "=" * 40,
            f"总格子数：{len(self.cells)}",
            f"总激活次数：{total_activations}",
            "",
            "🔥 最热格子："
        ]
        
        for cell in hot_cells:
            lines.append(f"  {cell.cell_id} {cell.name}: {cell.activation_count}次")
        
        return "\n".join(lines)


# 全局实例
_engine: Optional[KnowledgeCellEngine] = None

def get_knowledge_engine(cells_dir: Optional[str] = None) -> KnowledgeCellEngine:
    """获取知识格子引擎单例"""
    global _engine
    if _engine is None:
        _engine = KnowledgeCellEngine(cells_dir)
    return _engine


if __name__ == "__main__":
    # 测试
    engine = get_knowledge_engine()
    print(engine.summarize())
    
    # 测试激活
    print("\n--- 测试激活 ---")
    engine.activate_cell("A1")
    cell = engine.get_cell("A1")
    if cell:
        print(f"已激活: {cell.name}")
        print(f"关联格子: {cell.associations}")
    
    # 测试检索
    print("\n--- 测试内容检索 ---")
    results = engine.search_by_content("裂变")
    for c in results:
        print(f"  找到: {c.cell_id} {c.name}")
