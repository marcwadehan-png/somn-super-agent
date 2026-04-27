# -*- coding: utf-8 -*-
"""
中文代码修复核心逻辑
Chinese Code Fixer - Core Logic
"""
import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass

from ._gcf_mappings import CHINESE_PUNCT_TO_ASCII


@dataclass
class FixResult:
    """修复结果"""
    file_path: str
    fixes_count: int
    chinese_chars_found: List[str]
    errors: List[str]


class ChineseCodeFixer:
    """中文代码修复器"""

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.results: List[FixResult] = []
        self.total_fixes = 0

    def scan_file(self, file_path: Path) -> Tuple[int, List[str]]:
        """扫描文件中的中文内容"""
        chinese_chars = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                found = re.findall(r'[\u4e00-\u9fa5]', content)
                chinese_chars = list(set(found))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        return len(chinese_chars), chinese_chars

    def fix_file(self, file_path: Path, dry_run: bool = True) -> FixResult:
        """修复文件中的中文内容"""
        result = FixResult(
            file_path=str(file_path),
            fixes_count=0,
            chinese_chars_found=[],
            errors=[]
        )

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 1. 替换中文标点符号
            for cn_punct, ascii_punct in CHINESE_PUNCT_TO_ASCII.items():
                content = content.replace(cn_punct, ascii_punct)

            # 2. 替换中文引号
            content = content.replace('"', '"').replace('"', '"')
            content = content.replace(''', "'").replace(''', "'")

            # 计算修复数量
            fixes = len(re.findall(
                r'[\u4e00-\u9fa5「」『』【】（）《》〈〉！？。，；：、～·…—–""''‖｜＋－＝×÷％￥•]',
                original_content
            ))
            result.fixes_count = fixes

            if not dry_run and content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed: {file_path} ({fixes} replacements)")

        except Exception as e:
            result.errors.append(str(e))

        return result

    def scan_all(self, pattern: str = "*.py") -> Dict:
        """扫描所有文件"""
        files_with_chinese = {}

        for file_path in self.root_path.rglob(pattern):
            if '__pycache__' in str(file_path) or 'node_modules' in str(file_path):
                continue

            count, chars = self.scan_file(file_path)
            if count > 0:
                files_with_chinese[str(file_path)] = {
                    'count': count,
                    'sample_chars': chars[:20]
                }

        return files_with_chinese

    def fix_all(self, pattern: str = "*.py", dry_run: bool = True) -> List[FixResult]:
        """修复所有文件"""
        self.results = []
        self.total_fixes = 0

        for file_path in self.root_path.rglob(pattern):
            if '__pycache__' in str(file_path) or 'node_modules' in str(file_path):
                continue

            result = self.fix_file(file_path, dry_run=dry_run)
            self.results.append(result)
            self.total_fixes += result.fixes_count

        return self.results

    def generate_report(self) -> str:
        """生成修复报告"""
        report = []
        report.append("# 中文代码修复报告")
        report.append("")
        report.append(f"扫描路径: {self.root_path}")
        report.append(f"总修复数: {self.total_fixes}")
        report.append(f"处理文件数: {len(self.results)}")
        report.append("")

        sorted_results = sorted(
            [r for r in self.results if r.fixes_count > 0],
            key=lambda x: x.fixes_count,
            reverse=True
        )

        if sorted_results:
            report.append("## Top 30 需要修复的文件")
            report.append("")
            report.append("| 排名 | 文件 | 修复数 |")
            report.append("|------|------|--------|")

            for i, result in enumerate(sorted_results[:30], 1):
                report.append(f"| {i} | `{result.file_path}` | {result.fixes_count} |")

        return "\n".join(report)
