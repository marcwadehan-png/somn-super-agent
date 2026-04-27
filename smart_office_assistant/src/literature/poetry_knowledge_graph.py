"""
__all__ = [
    'add_author',
    'add_edge',
    'add_node',
    'add_poem',
    'analyze_author_network',
    'create_sample_knowledge_graph',
    'export_graph',
    'find_nodes_by_name',
    'find_nodes_by_type',
    'find_similar_poems',
    'generate_statistics',
    'get_author_poems',
    'get_poem_authors',
    'get_related_nodes',
    'load_from_file',
    'save_to_file',
    'to_dict',
    'visualize_graph',
]

诗词知识图谱系统
基于唐诗宋词50大家深度学习研究项目成果构建
Version: 1.0.0
Created: 2026-04-02
"""

import json
import os
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import networkx as nx
from enum import Enum

class NodeType(Enum):
    """知识图谱节点类型"""
    AUTHOR = "author"          # 作者节点
    POEM = "poem"              # 诗词作品节点
    DYNASTY = "dynasty"        # 朝代节点
    STYLE = "style"            # style流派节点
    THEME = "theme"            # 主题节点
    TECHNIQUE = "technique"    # 艺术手法节点
    LOCATION = "location"      # 地点节点
    HISTORICAL_EVENT = "event" # 历史事件节点

class EdgeType(Enum):
    """知识图谱边类型"""
    CREATED_BY = "created_by"          # 创作关系
    BELONGS_TO_DYNASTY = "belongs_to"  # 属于朝代
    HAS_STYLE = "has_style"            # 具有style
    HAS_THEME = "has_theme"            # 具有主题
    USES_TECHNIQUE = "uses_technique"  # 使用手法
    MENTIONS_LOCATION = "mentions"     # 提及地点
    INSPIRED_BY = "inspired_by"        # 受启发于
    INFLUENCES = "influences"          # 影响
    FRIENDS_WITH = "friends_with"      # 朋友关系
    TEACHER_STUDENT = "teacher_student" # 师生关系
    RELATES_TO_EVENT = "relates_to"    # 关联事件
    SIMILAR_TO = "similar_to"          # 相似作品

@dataclass
class KnowledgeNode:
    """知识图谱节点"""
    node_id: str
    node_type: NodeType
    name: str
    attributes: Dict
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "id": self.node_id,
            "type": self.node_type.value,
            "name": self.name,
            "attributes": self.attributes,
            "created_at": self.created_at
        }

@dataclass
class KnowledgeEdge:
    """知识图谱边"""
    edge_id: str
    source_id: str
    target_id: str
    edge_type: EdgeType
    attributes: Dict
    weight: float = 1.0
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "id": self.edge_id,
            "source": self.source_id,
            "target": self.target_id,
            "type": self.edge_type.value,
            "attributes": self.attributes,
            "weight": self.weight,
            "created_at": self.created_at
        }

class PoetryKnowledgeGraph:
    """诗词知识图谱系统"""
    
    def __init__(self, data_dir: str = None):
        """
        init知识图谱系统
        
        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir or os.path.join("data", "knowledge_graph")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # init图结构
        self.graph = nx.MultiDiGraph()
        
        # 节点和边存储
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: Dict[str, KnowledgeEdge] = {}
        
        # 索引
        self.name_to_id: Dict[str, str] = {}
        self.type_to_ids: Dict[NodeType, Set[str]] = {}
        
        # 基于唐诗宋词研究项目的预定义数据
        self._init_predefined_data()
    
    def _init_predefined_data(self):
        """基于唐诗宋词50大家研究项目init预定义数据"""
        
        # 预定义朝代
        self.add_node(
            node_id="dynasty_tang",
            node_type=NodeType.DYNASTY,
            name="唐代",
            attributes={
                "time_period": "618-907年",
                "capital": "长安",
                "characteristics": "诗歌黄金时代,开放包容",
                "literary_achievements": "唐诗达到顶峰"
            }
        )
        
        self.add_node(
            node_id="dynasty_song",
            node_type=NodeType.DYNASTY,
            name="宋代",
            attributes={
                "time_period": "960-1279年",
                "capital": "开封/临安",
                "characteristics": "词体文学繁荣,理学兴起",
                "literary_achievements": "宋词成为主流"
            }
        )
        
        # 预定义style流派
        styles = [
            ("style_heroic", "豪放派", {"characteristics": "气势磅礴,情感奔放", "representatives": "李白,苏轼,辛弃疾"}),
            ("style_graceful", "婉约派", {"characteristics": "语言婉约,情感细腻", "representatives": "李清照,秦观,柳永"}),
            ("style_nature", "山水田园派", {"characteristics": "描写自然,意境清新", "representatives": "王维,孟浩然"}),
            ("style_frontier", "边塞诗派", {"characteristics": "描写边塞,豪迈悲壮", "representatives": "高适,岑参,王昌龄"}),
            ("style_metaphysical", "玄言诗派", {"characteristics": "玄理思辨,语言玄妙", "representatives": "陶渊明,谢灵运"}),
            ("style_neo_yuefu", "新乐府运动", {"characteristics": "关注现实,语言通俗", "representatives": "白居易,元稹"}),
        ]
        
        for style_id, style_name, attrs in styles:
            self.add_node(
                node_id=style_id,
                node_type=NodeType.STYLE,
                name=style_name,
                attributes=attrs
            )
        
        # 预定义主题
        themes = [
            ("theme_love", "爱情", {"description": "表达男女之爱,相思之情"}),
            ("theme_nature", "山水自然", {"description": "描写自然风光,山水田园"}),
            ("theme_friendship", "友情", {"description": "表达朋友之情,离别之思"}),
            ("theme_patriotism", "爱国", {"description": "表达爱国之情,报国之志"}),
            ("theme_philosophy", "哲理", {"description": "蕴含人生哲理,宇宙思考"}),
            ("theme_history", "咏史怀古", {"description": "追忆历史,抒发感慨"}),
            ("theme_season", "季节", {"description": "描写四季变化,时令景物"}),
            ("theme_travel", "行旅", {"description": "描写旅途见闻,游子情怀"}),
        ]
        
        for theme_id, theme_name, attrs in themes:
            self.add_node(
                node_id=theme_id,
                node_type=NodeType.THEME,
                name=theme_name,
                attributes=attrs
            )
    
    def add_node(self, node_id: str, node_type: NodeType, name: str, attributes: Dict) -> KnowledgeNode:
        """添加节点到知识图谱"""
        
        # 创建节点
        node = KnowledgeNode(
            node_id=node_id,
            node_type=node_type,
            name=name,
            attributes=attributes
        )
        
        # 存储节点
        self.nodes[node_id] = node
        
        # 添加到networkx图
        self.graph.add_node(node_id, **node.to_dict())
        
        # 更新索引
        self.name_to_id[name] = node_id
        
        if node_type not in self.type_to_ids:
            self.type_to_ids[node_type] = set()
        self.type_to_ids[node_type].add(node_id)
        
        return node
    
    def add_edge(self, source_id: str, target_id: str, edge_type: EdgeType, 
                 attributes: Dict = None, weight: float = 1.0) -> KnowledgeEdge:
        """添加边到知识图谱"""
        
        # 检查节点是否存在
        if source_id not in self.nodes:
            raise ValueError(f"源节点 {source_id} 不存在")
        if target_id not in self.nodes:
            raise ValueError(f"目标节点 {target_id} 不存在")
        
        # generate边ID
        edge_id = f"edge_{source_id}_{target_id}_{edge_type.value}"
        
        # 创建边
        edge = KnowledgeEdge(
            edge_id=edge_id,
            source_id=source_id,
            target_id=target_id,
            edge_type=edge_type,
            attributes=attributes or {},
            weight=weight
        )
        
        # 存储边
        self.edges[edge_id] = edge
        
        # 添加到networkx图
        self.graph.add_edge(source_id, target_id, key=edge_id, **edge.to_dict())
        
        return edge
    
    def add_author(self, author_id: str, name: str, attributes: Dict) -> KnowledgeNode:
        """添加作者节点"""
        return self.add_node(
            node_id=f"author_{author_id}",
            node_type=NodeType.AUTHOR,
            name=name,
            attributes=attributes
        )
    
    def add_poem(self, poem_id: str, title: str, attributes: Dict) -> KnowledgeNode:
        """添加诗词作品节点"""
        return self.add_node(
            node_id=f"poem_{poem_id}",
            node_type=NodeType.POEM,
            name=title,
            attributes=attributes
        )
    
    def find_nodes_by_name(self, name: str) -> List[KnowledgeNode]:
        """根据名称查找节点"""
        if name in self.name_to_id:
            node_id = self.name_to_id[name]
            return [self.nodes[node_id]]
        return []
    
    def find_nodes_by_type(self, node_type: NodeType) -> List[KnowledgeNode]:
        """根据类型查找节点"""
        if node_type in self.type_to_ids:
            return [self.nodes[node_id] for node_id in self.type_to_ids[node_type]]
        return []
    
    def get_author_poems(self, author_id: str) -> List[KnowledgeNode]:
        """get作者的所有作品"""
        author_node_id = f"author_{author_id}"
        poems = []
        
        for edge in self.edges.values():
            if edge.source_id == author_node_id and edge.edge_type == EdgeType.CREATED_BY:
                if edge.target_id in self.nodes:
                    poems.append(self.nodes[edge.target_id])
        
        return poems
    
    def get_poem_authors(self, poem_id: str) -> List[KnowledgeNode]:
        """get作品的作者"""
        poem_node_id = f"poem_{poem_id}"
        authors = []
        
        for edge in self.edges.values():
            if edge.target_id == poem_node_id and edge.edge_type == EdgeType.CREATED_BY:
                if edge.source_id in self.nodes:
                    authors.append(self.nodes[edge.source_id])
        
        return authors
    
    def get_related_nodes(self, node_id: str, max_depth: int = 2) -> Dict[str, List]:
        """get关联节点(BFS搜索)"""
        if node_id not in self.graph:
            return {}
        
        visited = set()
        queue = [(node_id, 0)]
        related = {"direct": [], "indirect": []}
        
        while queue:
            current_id, depth = queue.pop(0)
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            # get邻居节点
            neighbors = list(self.graph.neighbors(current_id))
            
            for neighbor_id in neighbors:
                if neighbor_id not in visited:
                    # get边信息
                    edge_data = self.graph.get_edge_data(current_id, neighbor_id)
                    if edge_data:
                        for edge_key, edge_attrs in edge_data.items():
                            edge_info = {
                                "node": self.nodes[neighbor_id].to_dict() if neighbor_id in self.nodes else {},
                                "edge": edge_attrs,
                                "depth": depth + 1
                            }
                            
                            if depth == 0:
                                related["direct"].append(edge_info)
                            else:
                                related["indirect"].append(edge_info)
                    
                    if depth + 1 < max_depth:
                        queue.append((neighbor_id, depth + 1))
        
        return related
    
    def analyze_author_network(self, author_id: str) -> Dict:
        """分析作者社交网络"""
        author_node_id = f"author_{author_id}"
        
        if author_node_id not in self.graph:
            return {}
        
        # get朋友关系
        friends = []
        for edge in self.edges.values():
            if edge.edge_type == EdgeType.FRIENDS_WITH:
                if edge.source_id == author_node_id:
                    friends.append(self.nodes[edge.target_id].name)
                elif edge.target_id == author_node_id:
                    friends.append(self.nodes[edge.source_id].name)
        
        # get师生关系
        teachers = []
        students = []
        for edge in self.edges.values():
            if edge.edge_type == EdgeType.TEACHER_STUDENT:
                if edge.target_id == author_node_id:  # 作者是学生
                    teachers.append(self.nodes[edge.source_id].name)
                elif edge.source_id == author_node_id:  # 作者是老师
                    students.append(self.nodes[edge.target_id].name)
        
        # get影响关系
        influenced_by = []
        influences = []
        for edge in self.edges.values():
            if edge.edge_type == EdgeType.INFLUENCES:
                if edge.target_id == author_node_id:  # 被谁影响
                    influenced_by.append(self.nodes[edge.source_id].name)
                elif edge.source_id == author_node_id:  # 影响了谁
                    influences.append(self.nodes[edge.target_id].name)
        
        return {
            "author": author_id,
            "friends": friends,
            "teachers": teachers,
            "students": students,
            "influenced_by": influenced_by,
            "influences": influences,
            "social_score": len(friends) + len(teachers) + len(students) + len(influences)
        }
    
    def find_similar_poems(self, poem_id: str, similarity_threshold: float = 0.7) -> List[Dict]:
        """查找相似作品"""
        poem_node_id = f"poem_{poem_id}"
        similar_poems = []
        
        for edge in self.edges.values():
            if edge.edge_type == EdgeType.SIMILAR_TO and edge.weight >= similarity_threshold:
                if edge.source_id == poem_node_id:
                    target_node = self.nodes[edge.target_id]
                    similar_poems.append({
                        "poem": target_node.to_dict(),
                        "similarity": edge.weight,
                        "reasons": edge.attributes.get("reasons", [])
                    })
                elif edge.target_id == poem_node_id:
                    source_node = self.nodes[edge.source_id]
                    similar_poems.append({
                        "poem": source_node.to_dict(),
                        "similarity": edge.weight,
                        "reasons": edge.attributes.get("reasons", [])
                    })
        
        # 按相似度排序
        similar_poems.sort(key=lambda x: x["similarity"], reverse=True)
        return similar_poems
    
    def export_graph(self, format: str = "json") -> Dict:
        """导出知识图谱"""
        nodes_data = [node.to_dict() for node in self.nodes.values()]
        edges_data = [edge.to_dict() for edge in self.edges.values()]
        
        return {
            "metadata": {
                "name": "唐诗宋词知识图谱",
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "node_count": len(nodes_data),
                "edge_count": len(edges_data),
                "data_source": "唐诗宋词50大家深度学习研究项目"
            },
            "nodes": nodes_data,
            "edges": edges_data
        }
    
    def save_to_file(self, filename: str = None):
        """保存知识图谱到文件"""
        if filename is None:
            filename = f"poetry_knowledge_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        graph_data = self.export_graph()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def load_from_file(self, filepath: str):
        """从文件加载知识图谱"""
        with open(filepath, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        
        # 清空当前图
        self.graph = nx.MultiDiGraph()
        self.nodes.clear()
        self.edges.clear()
        self.name_to_id.clear()
        self.type_to_ids.clear()
        
        # 加载节点
        for node_data in graph_data["nodes"]:
            node = KnowledgeNode(
                node_id=node_data["id"],
                node_type=NodeType(node_data["type"]),
                name=node_data["name"],
                attributes=node_data["attributes"],
                created_at=node_data["created_at"]
            )
            self.nodes[node.node_id] = node
            self.graph.add_node(node.node_id, **node.to_dict())
            
            # 更新索引
            self.name_to_id[node.name] = node.node_id
            if node.node_type not in self.type_to_ids:
                self.type_to_ids[node.node_type] = set()
            self.type_to_ids[node.node_type].add(node.node_id)
        
        # 加载边
        for edge_data in graph_data["edges"]:
            edge = KnowledgeEdge(
                edge_id=edge_data["id"],
                source_id=edge_data["source"],
                target_id=edge_data["target"],
                edge_type=EdgeType(edge_data["type"]),
                attributes=edge_data["attributes"],
                weight=edge_data["weight"],
                created_at=edge_data["created_at"]
            )
            self.edges[edge.edge_id] = edge
            self.graph.add_edge(
                edge.source_id, 
                edge.target_id, 
                key=edge.edge_id, 
                **edge.to_dict()
            )
    
    def visualize_graph(self, output_path: str = None):
        """可视化知识图谱(需要matplotlib)"""
        try:
            import matplotlib.pyplot as plt
            
            # 创建布局
            pos = nx.spring_layout(self.graph, seed=42)
            
            # 根据节点类型设置颜色
            node_colors = []
            color_map = {
                NodeType.AUTHOR: "red",
                NodeType.POEM: "blue",
                NodeType.DYNASTY: "green",
                NodeType.STYLE: "orange",
                NodeType.THEME: "purple",
                NodeType.TECHNIQUE: "brown",
                NodeType.LOCATION: "pink",
                NodeType.HISTORICAL_EVENT: "gray"
            }
            
            for node_id in self.graph.nodes():
                node = self.nodes[node_id]
                node_colors.append(color_map.get(node.node_type, "black"))
            
            # 绘制图
            plt.figure(figsize=(20, 15))
            nx.draw(
                self.graph, 
                pos, 
                with_labels=True,
                node_color=node_colors,
                node_size=500,
                font_size=8,
                edge_color="gray",
                alpha=0.7
            )
            
            # 添加图例
            legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                        markerfacecolor=color, markersize=10, 
                                        label=node_type.value)
                            for node_type, color in color_map.items()]
            plt.legend(handles=legend_elements, loc='upper right')
            
            plt.title("唐诗宋词知识图谱", fontsize=16)
            
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
            
            plt.show()
            
        except ImportError:
            print("需要安装matplotlib进行可视化: pip install matplotlib")
    
    def generate_statistics(self) -> Dict:
        """generate知识图谱统计信息"""
        stats = {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": {},
            "edge_types": {},
            "density": nx.density(self.graph),
            "connected_components": nx.number_connected_components(self.graph.to_undirected()),
            "average_degree": sum(dict(self.graph.degree()).values()) / len(self.nodes) if self.nodes else 0
        }
        
        # 统计节点类型
        for node_type in NodeType:
            type_count = len(self.type_to_ids.get(node_type, set()))
            stats["node_types"][node_type.value] = type_count
        
        # 统计边类型
        edge_type_count = {}
        for edge in self.edges.values():
            edge_type = edge.edge_type.value
            edge_type_count[edge_type] = edge_type_count.get(edge_type, 0) + 1
        stats["edge_types"] = edge_type_count
        
        return stats

# 示例使用
def create_sample_knowledge_graph():
    """创建示例知识图谱"""
    kg = PoetryKnowledgeGraph()
    
    # 添加唐代poet(基于唐诗宋词50大家研究项目)
    tang_poets = [
        ("libai", "李白", {
            "birth_year": 701,
            "death_year": 762,
            "courtesy_name": "太白",
            "art_name": "青莲居士",
            "hometown": "陇西成纪",
            "style": "豪放派",
            "achievements": "诗仙,唐代浪漫主义诗歌代表"
        }),
        ("dufu", "杜甫", {
            "birth_year": 712,
            "death_year": 770,
            "courtesy_name": "子美",
            "art_name": "少陵野老",
            "hometown": "河南巩县",
            "style": "现实主义",
            "achievements": "诗圣,唐代现实主义诗歌代表"
        }),
        ("wangwei", "王维", {
            "birth_year": 701,
            "death_year": 761,
            "courtesy_name": "摩诘",
            "art_name": "诗佛",
            "hometown": "河东蒲州",
            "style": "山水田园派",
            "achievements": "诗中有画,画中有诗"
        })
    ]
    
    for poet_id, name, attrs in tang_poets:
        kg.add_author(poet_id, name, attrs)
        # 关联到唐代
        kg.add_edge(f"author_{poet_id}", "dynasty_tang", EdgeType.BELONGS_TO_DYNASTY)
        # 关联到style
        if attrs["style"] == "豪放派":
            kg.add_edge(f"author_{poet_id}", "style_heroic", EdgeType.HAS_STYLE)
        elif attrs["style"] == "山水田园派":
            kg.add_edge(f"author_{poet_id}", "style_nature", EdgeType.HAS_STYLE)
    
    # 添加宋代poet
    song_poets = [
        ("sushi", "苏轼", {
            "birth_year": 1037,
            "death_year": 1101,
            "courtesy_name": "子瞻",
            "art_name": "东坡居士",
            "hometown": "眉州眉山",
            "style": "豪放派",
            "achievements": "豪放词开创者,唐宋八大家之一"
        }),
        ("xinqiji", "辛弃疾", {
            "birth_year": 1140,
            "death_year": 1207,
            "courtesy_name": "幼安",
            "art_name": "稼轩",
            "hometown": "历城",
            "style": "豪放派",
            "achievements": "与苏轼并称苏辛"
        }),
        ("liqingzhao", "李清照", {
            "birth_year": 1084,
            "death_year": 1155,
            "art_name": "易安居士",
            "hometown": "济南",
            "style": "婉约派",
            "achievements": "千古第一才女,婉约词代表"
        })
    ]
    
    for poet_id, name, attrs in song_poets:
        kg.add_author(poet_id, name, attrs)
        # 关联到宋代
        kg.add_edge(f"author_{poet_id}", "dynasty_song", EdgeType.BELONGS_TO_DYNASTY)
        # 关联到style
        if attrs["style"] == "豪放派":
            kg.add_edge(f"author_{poet_id}", "style_heroic", EdgeType.HAS_STYLE)
        elif attrs["style"] == "婉约派":
            kg.add_edge(f"author_{poet_id}", "style_graceful", EdgeType.HAS_STYLE)
    
    # 添加作品
    poems = [
        ("jiangjinjiu", "将进酒", "libai", {
            "content_preview": "君不见黄河之水天上来...",
            "form": "乐府诗",
            "theme": ["豪情", "饮酒", "人生"],
            "techniques": ["夸张", "比喻", "对偶"]
        }),
        ("yueyexiangsi", "月夜忆舍弟", "dufu", {
            "content_preview": "戍鼓断人行,边秋一雁声...",
            "form": "五言律诗",
            "theme": ["思乡", "兄弟", "战争"],
            "techniques": ["对仗", "借景抒情"]
        }),
        ("shandaonan", "蜀道难", "libai", {
            "content_preview": "噫吁嚱,危乎高哉...",
            "form": "乐府诗",
            "theme": ["山水", "艰险", "人生"],
            "techniques": ["夸张", "排比", "反复"]
        })
    ]
    
    for poem_id, title, author_id, attrs in poems:
        kg.add_poem(poem_id, title, attrs)
        # 关联作者
        kg.add_edge(f"author_{author_id}", f"poem_{poem_id}", EdgeType.CREATED_BY)
        # 关联主题
        for theme in attrs.get("theme", []):
            if theme == "豪情":
                kg.add_edge(f"poem_{poem_id}", "theme_patriotism", EdgeType.HAS_THEME, weight=0.8)
            elif theme == "思乡":
                kg.add_edge(f"poem_{poem_id}", "theme_travel", EdgeType.HAS_THEME, weight=0.9)
            elif theme == "山水":
                kg.add_edge(f"poem_{poem_id}", "theme_nature", EdgeType.HAS_THEME, weight=1.0)
    
    # 添加社交关系
    kg.add_edge("author_libai", "author_dufu", EdgeType.FRIENDS_WITH, {"relationship": "诗友"})
    kg.add_edge("author_sushi", "author_xinqiji", EdgeType.INFLUENCES, {"influence_area": "豪放词风"})
    
    # 添加相似作品关系
    kg.add_edge(
        "poem_jiangjinjiu", 
        "poem_shandaonan", 
        EdgeType.SIMILAR_TO, 
        {"reasons": ["同作者", "豪放style", "乐府形式"]},
        weight=0.85
    )
    
    return kg

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
