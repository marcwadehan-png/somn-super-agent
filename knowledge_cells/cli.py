#!/usr/bin/env python3
"""
知识格子系统 CLI
================
交互式命令行界面
"""

import sys
import os
import cmd
from typing import Optional

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge_cells import get_knowledge_system


class KnowledgeShell(cmd.Cmd):
    """知识格子交互Shell"""
    
    intro = """
╔══════════════════════════════════════════════════════════╗
║         知识格子系统 v1.1 - 交互Shell                     ║
╠══════════════════════════════════════════════════════════╣
║  命令:                                                    ║
║    ask <问题>      - 提问并获取知识融合回答                ║
║    check <内容>    - 检查内容是否符合方法论                ║
║    search <关键词> - 搜索相关格子                         ║
║    cell <ID>       - 查看指定格子详情                     ║
║    related <ID>    - 查看格子关联                         ║
║    hot             - 查看最热格子                         ║
║    graph           - 查看知识图谱摘要                      ║
║    list            - 列出所有格子                         ║
║    status          - 系统状态                             ║
║    help            - 显示帮助                            ║
║    quit/exit       - 退出                                ║
╚══════════════════════════════════════════════════════════╝
"""
    prompt = "(知识) > "
    
    def __init__(self):
        super().__init__()
        self.system = get_knowledge_system()
    
    def do_ask(self, arg):
        """ask <问题> - 提问并获取知识融合回答"""
        if not arg.strip():
            print("请输入问题，例如: ask 如何提升用户增长")
            return
        
        result = self.system.query(arg)
        
        print("\n┌─────────────────────────────────────────┐")
        print("│ 回答")
        print("└─────────────────────────────────────────┘")
        print(result['answer'])
        
        print(f"\n📊 质量分数: {result['quality_score']}/100")
        print(f"🔗 使用格子: {', '.join(result['cells_used'])}")
        print(f"📐 推荐框架: {', '.join(result['frameworks']) if result['frameworks'] else '无'}")
        print(f"💡 举一反三: {result['analogies'][0] if result['analogies'] else '无'}")
    
    def do_check(self, arg):
        """check <内容> - 检查内容是否符合方法论"""
        if not arg.strip():
            print("请输入要检查的内容")
            return
        
        result = self.system.check_methodology(arg)
        
        print("\n┌─────────────────────────────────────────┐")
        print("│ 方法论检查结果")
        print("└─────────────────────────────────────────┘")
        
        level_names = {
            "S": "S级 - 卓越",
            "A": "A级 - 优秀",
            "B": "B级 - 良好",
            "C": "C级 - 一般",
            "D": "D级 - 待改进"
        }
        
        print(f"\n🎯 整体评分: {result['overall_score']}/100")
        print(f"📈 评估等级: {result['level']} - {level_names.get(result['level'], '')}")
        
        print("\n各维度得分:")
        dims = result['dimensions']
        for name, info in dims.items():
            bar = "█" * (info['score'] // 10) + "░" * (10 - info['score'] // 10)
            print(f"  {name:8}: [{bar}] {info['score']}/100")
            if info['issues']:
                print(f"           问题: {', '.join(info['issues'][:2])}")
        
        if result['suggestions']:
            print("\n💡 改进建议:")
            for s in result['suggestions'][:3]:
                print(f"  • {s}")
    
    def do_search(self, arg):
        """search <关键词> - 搜索相关格子"""
        if not arg.strip():
            print("请输入搜索关键词")
            return
        
        results = self.system.search_cells(arg)
        
        if not results:
            print(f"未找到与'{arg}'相关的格子")
            return
        
        print(f"\n🔍 搜索'{arg}'，找到 {len(results)} 个格子:")
        for r in results[:10]:
            print(f"  [{r['cell_id']}] {r['name']}")
    
    def do_cell(self, arg):
        """cell <ID> - 查看指定格子详情"""
        if not arg.strip():
            print("请输入格子ID，例如: A1, B1")
            return
        
        cell_id = arg.strip().upper()
        cell = self.system.get_cell_content(cell_id)
        
        if not cell:
            print(f"未找到格子: {cell_id}")
            return
        
        print(f"\n┌─────────────────────────────────────────┐")
        print(f"│ 格子: [{cell_id}] {cell['name']}")
        print(f"└─────────────────────────────────────────┘")
        
        print(f"\n🏷️ 标签: {', '.join(cell['tags']) if cell['tags'] else '无'}")
        print(f"📈 激活次数: {cell['activation_count']}")
        print(f"🕐 上次激活: {cell['last_activation'] or '从未'}")
        
        if cell['content']:
            print("\n📝 内容摘要:")
            if 'what' in cell['content']:
                print(f"  这是什么: {cell['content']['what'][:100]}...")
    
    def do_related(self, arg):
        """related <ID> - 查看格子关联"""
        if not arg.strip():
            print("请输入格子ID")
            return
        
        cell_id = arg.strip().upper()
        related = self.system.get_related_cells(cell_id)
        
        if not related:
            print(f"格子 {cell_id} 没有关联")
            return
        
        print(f"\n🔗 格子 {cell_id} 的关联:")
        for r in related:
            bar = "█" * int(r['weight'] * 10) + "░" * (10 - int(r['weight'] * 10))
            print(f"  [{r['cell_id']}] {r['name']} {bar} {r['weight']:.1f}")
    
    def do_hot(self, arg):
        """hot - 查看最热格子"""
        hot = self.system.get_hot_cells(10)
        
        print("\n🔥 最热格子 TOP10:")
        for i, c in enumerate(hot, 1):
            bar = "█" * min(c['activations'], 10) + "░" * max(0, 10 - c['activations'])
            print(f"  {i:2}. [{c['cell_id']}] {c['name']:10} {bar} ({c['activations']}次)")
    
    def do_graph(self, arg):
        """graph - 查看知识图谱摘要"""
        graph = self.system.get_knowledge_graph()
        
        print("\n🕸️ 知识图谱:")
        print(f"  • 节点数: {len(graph['nodes'])}")
        print(f"  • 边数: {len(graph['links'])}")
        
        # 按分类统计
        core = [n for n in graph['nodes'] if n['category'] == 'core']
        domain = [n for n in graph['nodes'] if n['category'] == 'domain']
        
        print(f"\n  智慧核心: {len(core)} 个")
        for n in core:
            print(f"    • {n['id']} {n['name']}")
        
        print(f"\n  知识域: {len(domain)} 个")
        for n in domain[:8]:
            print(f"    • {n['id']} {n['name']}")
        if len(domain) > 8:
            print(f"    ... 还有 {len(domain) - 8} 个")
    
    def do_list(self, arg):
        """list - 列出所有格子"""
        cells = self.system.list_all_cells()
        
        print("\n📋 所有格子:")
        
        # 按分类显示
        core = [c for c in cells if c['cell_id'].startswith('A')]
        domain = [c for c in cells if c['cell_id'].startswith(('B', 'C'))]
        
        print(f"\n  智慧核心 ({len(core)}):")
        for c in core:
            print(f"    [{c['cell_id']}] {c['name']}")
        
        print(f"\n  知识域 ({len(domain)}):")
        for c in domain:
            print(f"    [{c['cell_id']}] {c['name']}")
    
    def do_status(self, arg):
        """status - 系统状态"""
        status = self.system.get_status()
        
        print("\n📊 系统状态:")
        print(f"  • 总格子数: {status['total_cells']}")
        print(f"  • 知识图谱节点: {status['knowledge_graph_nodes']}")
        
        print("\n  🔥 Top5 最热格子:")
        for c in status['hot_cells'][:5]:
            print(f"    [{c['cell_id']}] {c['name']}: {c['activations']}次")
    
    def do_help(self, arg):
        """显示帮助"""
        print(self.intro)
    
    def do_quit(self, arg):
        """退出"""
        print("\n👋 再见!")
        return True
    
    def do_exit(self, arg):
        """退出"""
        return self.do_quit(arg)


def main():
    """主函数"""
    shell = KnowledgeShell()
    shell.cmdloop()


if __name__ == "__main__":
    main()
