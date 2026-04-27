"""
彩色输出工具
Color Printer Utility
"""

import sys


class ColorPrinter:
    """终端彩色输出工具"""
    
    # ANSI颜色代码
    COLORS = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'gray': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
    }
    
    # 样式代码
    STYLES = {
        'bold': '\033[1m',
        'dim': '\033[2m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        'blink': '\033[5m',
        'reverse': '\033[7m',
        'hidden': '\033[8m',
    }
    
    # 重置代码
    RESET = '\033[0m'
    
    @classmethod
    def _colorize(cls, text: str, color: str = None, style: str = None) -> str:
        """将文本着色"""
        result = ""
        
        if color and color in cls.COLORS:
            result += cls.COLORS[color]
            
        if style and style in cls.STYLES:
            result += cls.STYLES[style]
            
        result += text + cls.RESET
        
        return result
    
    @classmethod
    def black(cls, text: str, style: str = None) -> str:
        return cls._colorize(text, 'black', style)
    
    @classmethod
    def red(cls, text: str, style: str = None) -> str:
        return cls._colorize(text, 'red', style)
    
    @classmethod
    def green(cls, text: str, style: str = None) -> str:
        return cls._colorize(text, 'green', style)
    
    @classmethod
    def yellow(cls, text: str, style: str = None) -> str:
        return cls._colorize(text, 'yellow', style)
    
    @classmethod
    def blue(cls, text: str, style: str = None) -> str:
        return cls._colorize(text, 'blue', style)
    
    @classmethod
    def magenta(cls, text: str, style: str = None) -> str:
        return cls._colorize(text, 'magenta', style)
    
    @classmethod
    def cyan(cls, text: str, style: str = None) -> str:
        return cls._colorize(text, 'cyan', style)
    
    @classmethod
    def white(cls, text: str, style: str = None) -> str:
        return cls._colorize(text, 'white', style)
    
    # 快捷打印方法
    @staticmethod
    def print_header(text: str):
        """打印标题"""
        print(f"\n{'='*60}\n{text}\n{'='*60}")
    
    @staticmethod
    def print_success(text: str):
        """打印成功信息"""
        print(f"{ColorPrinter.green('[✓]')} {text}")
    
    @staticmethod
    def print_error(text: str):
        """打印错误信息"""
        print(f"{ColorPrinter.red('[✗]')} {text}")
    
    @staticmethod
    def print_warning(text: str):
        """打印警告信息"""
        print(f"{ColorPrinter.yellow('[!]')} {text}")
    
    @staticmethod
    def print_info(text: str):
        """打印提示信息"""
        print(f"{ColorPrinter.blue('[i]')} {text}")
    
    @staticmethod
    def print_bullet(text: str, color: str = 'white'):
        """打印项目符号"""
        colored_dot = ColorPrinter._colorize('●', color)
        print(f"  {colored_dot} {text}")
    
    @staticmethod
    def print_section(title: str):
        """打印分节标题"""
        print(f"\n{ColorPrinter.cyan(title, 'bold')}")
        print(ColorPrinter.gray('─' * 50))
    
    @staticmethod
    def print_table_row(columns: list, widths: list = None, colors: list = None):
        """打印表格行"""
        if widths is None:
            widths = [20] * len(columns)
        if colors is None:
            colors = ['white'] * len(columns)
            
        cells = []
        for col, width, color in zip(columns, widths, colors):
            cell = str(col).ljust(width)
            cells.append(ColorPrinter._colorize(cell, color))
            
        print('│ ' + ' │ '.join(cells) + ' │')
    
    @staticmethod
    def print_divider(char: str = '─', length: int = 50, color: str = 'gray'):
        """打印分隔线"""
        line = ColorPrinter._colorize(char * length, color)
        print(line)


# 测试
if __name__ == '__main__':
    ColorPrinter.print_header("Color Printer Test")
    
    ColorPrinter.print_success("Success message")
    ColorPrinter.print_error("Error message")
    ColorPrinter.print_warning("Warning message")
    ColorPrinter.print_info("Info message")
    
    ColorPrinter.print_section("Section Title")
    
    # 彩色文本
    print(f"\n{ColorPrinter.red('Red')} | {ColorPrinter.green('Green')} | {ColorPrinter.blue('Blue')}")
    print(f"{ColorPrinter.bold('Bold')} | {ColorPrinter.underline('Underline')}")
    
    # 表格
    ColorPrinter.print_divider()
    ColorPrinter.print_table_row(["Name", "Status", "Score"], [15, 15, 10], ['cyan', 'green', 'yellow'])
    ColorPrinter.print_table_row(["Module A", "Running", "95"], [15, 15, 10], ['white', 'white', 'white'])
    ColorPrinter.print_divider()
