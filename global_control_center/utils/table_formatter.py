"""
表格格式化工具
Table Formatter Utility
"""

from typing import List, Tuple, Optional


class TableFormatter:
    """终端表格格式化工具"""
    
    @staticmethod
    def format_table(
        headers: List[str],
        rows: List[Tuple],
        title: str = None,
        col_widths: List[int] = None,
        style: str = 'single'
    ) -> str:
        """
        格式化表格
        
        Args:
            headers: 表头列表
            rows: 数据行列表
            title: 表格标题
            col_widths: 列宽列表
            style: 边框样式 ('single', 'double', 'minimal')
        
        Returns:
            格式化的表格字符串
        """
        # 计算列宽
        if col_widths is None:
            col_widths = [max(len(str(row[i])) for row in [headers] + rows) + 2 
                         for i in range(len(headers))]
        else:
            # 确保列宽至少与表头匹配
            col_widths = [max(col_widths[i], len(headers[i]) + 2) for i in range(len(headers))]
        
        # 边框字符
        borders = {
            'single': ('┌', '┐', '└', '┘', '├', '┤', '┬', '┴', '┼', '─', '│'),
            'double': ('╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬', '═', '║'),
            'minimal': ('', '', '', '', '', '', '', '', '', '-', '|'),
        }
        
        chars = borders.get(style, borders['single'])
        top_left, top_right, bottom_left, bottom_right = chars[0:4]
        left_t, right_t, top_cross, bottom_cross, center = chars[4:9]
        h_line, v_line = chars[9], chars[10]
        
        # 构建表格
        lines = []
        
        # 标题
        if title:
            total_width = sum(col_widths) + len(col_widths) + 1
            padding = (total_width - len(title)) // 2
            lines.append(f"╔{'═' * total_width}╗")
            lines.append(f"║{' ' * padding}{title}{' ' * (total_width - padding - len(title))}║")
        
        # 顶部边框
        top_border = top_left + ''.join(h_line * w for w in col_widths).replace(
            h_line * col_widths[0], 
            h_line * col_widths[0]
        )
        for i in range(1, len(col_widths)):
            top_border += top_cross + h_line * col_widths[i]
        top_border += top_right
        
        if title:
            lines.append(top_border.replace(top_left, top_t := left_t, 1).replace(top_right, right_t := right_t, 1))
        else:
            lines.append(top_border)
        
        # 表头
        header_line = v_line + ' ' + f' {v_line} '.join(
            headers[i].center(col_widths[i]) for i in range(len(headers))
        ) + ' ' + v_line
        lines.append(header_line)
        
        # 表头与数据分隔
        sep_line = left_t + ''.join(h_line * (col_widths[i] + 2) for i in range(len(col_widths)))
        for i in range(1, len(col_widths)):
            sep_line = sep_line[:len(left_t) + sum(col_widths[:i]) + i + 2 * i] + center + sep_line[len(left_t) + sum(col_widths[:i]) + i + 2 * i + 1:]
        sep_line = sep_line[:-1] + right_t
        lines.append(sep_line)
        
        # 数据行
        for row in rows:
            row_line = v_line + ' ' + f' {v_line} '.join(
                str(row[i]).center(col_widths[i]) for i in range(len(row))
            ) + ' ' + v_line
            lines.append(row_line)
        
        # 底部边框
        bottom_border = bottom_left + ''.join(h_line * (col_widths[i] + 2) for i in range(len(col_widths)))
        for i in range(1, len(col_widths)):
            bottom_border = bottom_border[:len(bottom_left) + sum(col_widths[:i]) + 2 * i] + bottom_cross + bottom_border[len(bottom_left) + sum(col_widths[:i]) + 2 * i + 1:]
        bottom_border = bottom_border[:-1] + bottom_right
        lines.append(bottom_border)
        
        return '\n'.join(lines)
    
    @staticmethod
    def print_table(headers: List[str], rows: List[Tuple], **kwargs):
        """直接打印表格"""
        print(TableFormatter.format_table(headers, rows, **kwargs))
    
    @staticmethod
    def format_tree(items: List[Tuple[str, str]], indent: int = 2) -> str:
        """
        格式化树形结构
        
        Args:
            items: [(标题, 值), ...]
            indent: 缩进空格数
        
        Returns:
            格式化的树形字符串
        """
        lines = []
        prefix = ' ' * indent
        
        for key, value in items:
            lines.append(f"{prefix}├─ {key}: {value}")
            
        return '\n'.join(lines)
    
    @staticmethod
    def format_key_value(
        data: dict,
        key_color: str = 'cyan',
        value_color: str = 'white',
        indent: int = 0,
        separator: str = ':'
    ) -> str:
        """
        格式化键值对
        
        Args:
            data: 字典数据
            key_color: 键的颜色
            value_color: 值的颜色
            indent: 缩进空格数
            separator: 分隔符
        
        Returns:
            格式化的键值对字符串
        """
        from .color_printer import ColorPrinter
        
        lines = []
        prefix = ' ' * indent
        
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{ColorPrinter._colorize(key, key_color)}:")
                lines.append(TableFormatter.format_key_value(value, key_color, value_color, indent + 2, separator))
            else:
                lines.append(f"{prefix}{ColorPrinter._colorize(key, key_color)} {separator} {ColorPrinter._colorize(str(value), value_color)}")
                
        return '\n'.join(lines)
    
    @staticmethod
    def format_list(items: List[str], bullet: str = '●', color: str = 'white') -> str:
        """
        格式化列表
        
        Args:
            items: 列表项
            bullet: 项目符号
            color: 颜色
        
        Returns:
            格式化的列表字符串
        """
        from .color_printer import ColorPrinter
        
        colored_bullet = ColorPrinter._colorize(bullet, color)
        return '\n'.join(f"  {colored_bullet} {item}" for item in items)


# 测试
if __name__ == '__main__':
    # 测试表格
    headers = ['模块ID', '模块名称', '状态', '加载时间']
    rows = [
        ('core', '核心模块', '● 运行中', '0.12s'),
        ('intelligence', '智慧层', '● 运行中', '0.25s'),
        ('capability', '能力层', '● 运行中', '0.18s'),
        ('data', '数据层', '● 运行中', '0.08s'),
    ]
    
    print(TableFormatter.format_table(headers, rows, title='模块总览'))
    
    print()
    
    # 测试键值对
    data = {
        'system': 'standalone',
        'version': '2.0.0',
        'performance': {
            'lazy_loading': True,
            'max_tasks': 4
        }
    }
    
    print(TableFormatter.format_key_value(data))
