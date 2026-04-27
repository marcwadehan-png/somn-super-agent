#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Somn项目 - 代码质量自动化检查脚本
用法: python code_quality_check.py [--target src/] [--threshold 15]

依赖:
    pip install pylint flake8 radon bandit
"""

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class QualityConfig:
    """代码质量检查配置"""
    max_complexity: int = 15
    max_line_length: int = 120
    max_args: int = 8
    max_locals: int = 20
    max_attributes: int = 12
    max_statements: int = 60
    exclude_dirs: tuple = (
        "data", "tests", "__pycache__", ".git",
        "node_modules", ".venv", ".pytest_cache"
    )


class QualityChecker:
    """代码质量检查器"""

    def __init__(self, config: QualityConfig):
        self.config = config
        self.results = []
        self.errors = []

    def check_pylint(self, target: str) -> bool:
        """运行pylint检查"""
        print(f"\n{'='*60}")
        print("Pylint 代码质量检查 (复杂度阈值={})".format(self.config.max_complexity))
        print('='*60)

        cmd = [
            sys.executable, "-m", "pylint",
            target,
            f"--max-complexity={self.config.max_complexity}",
            "--jobs=4",
            "--persistent=yes",
            "--output-format=text",
            "--disable=missing-function-docstring,missing-class-docstring,missing-module-docstring,"
                     "raw-checker-failed,bad-inline-option,locally-disabled,file-ignored,"
                     "suppressed-message,useless-suppression,deprecated-pragma",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout + result.stderr

            # 解析复杂度违规
            complexity_issues = [line for line in output.split('\n')
                                 if 'R0914' in line or 'too-many-' in line.lower()
                                 or 'C901' in line]  # too-complex

            if complexity_issues:
                print(f"\n发现 {len(complexity_issues)} 个复杂度问题:")
                for issue in complexity_issues[:20]:  # 只显示前20个
                    print(f"  {issue.strip()}")

            # 统计信息
            if 'Your code has been rated at' in output:
                for line in output.split('\n'):
                    if 'Your code has been rated at' in line:
                        print(f"\n{line.strip()}")
                        self.results.append(line.strip())

            return result.returncode == 0

        except FileNotFoundError:
            print("pylint 未安装. 运行: pip install pylint")
            return False
        except Exception as e:
            print(f"Pylint 检查失败: {e}")
            return False

    def check_flake8(self, target: str) -> bool:
        """运行flake8检查"""
        print(f"\n{'='*60}")
        print("Flake8 风格检查 (行长度={})".format(self.config.max_line_length))
        print('='*60)

        cmd = [
            "flake8", target,
            f"--max-line-length={self.config.max_line_length}",
            "--exclude=" + ",".join(self.config.exclude_dirs),
            "--count", "--statistics", "--show-source"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout + result.stderr

            if output.strip():
                print(output)
                self.results.append(f"Flake8: {len(output.splitlines())} issues")
            else:
                print("✓ Flake8 检查通过")

            return result.returncode == 0

        except FileNotFoundError:
            print("flake8 未安装. 运行: pip install flake8")
            return False
        except Exception as e:
            print(f"Flake8 检查失败: {e}")
            return False

    def check_complexity(self, target: str) -> bool:
        """运行radon复杂度分析"""
        print(f"\n{'='*60}")
        print("复杂度分析 (McCabe CC 阈值={})".format(self.config.max_complexity))
        print('='*60)

        # CC分析
        cmd_cc = ["radon", "cc", "-a", "-n", str(self.config.max_complexity), target]

        try:
            result = subprocess.run(cmd_cc, capture_output=True, text=True)
            output = result.stdout

            if output.strip():
                lines = output.strip().split('\n')
                print(f"\n发现 {len(lines)} 个超过阈值的函数/方法:\n")
                for line in lines[:30]:  # 只显示前30个
                    print(f"  {line}")

                high_cc = [l for l in lines if '-' in l]
                self.results.append(f"高复杂度函数: {len(high_cc)} 个")

                return False
            else:
                print("✓ 所有函数复杂度都在阈值内")
                return True

        except FileNotFoundError:
            print("radon 未安装. 运行: pip install radon")
            return False
        except Exception as e:
            print(f"复杂度分析失败: {e}")
            return False

    def check_security(self, target: str) -> bool:
        """运行bandit安全检查"""
        print(f"\n{'='*60}")
        print("安全检查 (Bandit)")
        print('='*60)

        cmd = ["bandit", "-r", target, "-f", "screen", "-ll"]  # -ll 低级别也显示

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout + result.stderr

            if "No issues identified" in output:
                print("✓ 安全检查通过，未发现漏洞")
                return True
            elif output.strip():
                print(output)
                self.results.append("安全检查: 发现问题")
                return False
            else:
                print("✓ 安全检查通过")
                return True

        except FileNotFoundError:
            print("bandit 未安装. 运行: pip install bandit")
            return False
        except Exception as e:
            print(f"安全检查失败: {e}")
            return False

    def generate_report(self, target: str) -> str:
        """生成检查报告"""
        report = f"""
{'='*60}
Somn 代码质量检查报告
{'='*60}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
目标: {target}

配置:
  - 最大圈复杂度: {self.config.max_complexity}
  - 最大行长度: {self.config.max_line_length}
  - 最大参数数: {self.config.max_args}
  - 最大局部变量: {self.config.max_locals}
  - 最大属性数: {self.config.max_attributes}

检查结果摘要:
"""

        for result in self.results:
            report += f"  • {result}\n"

        report += f"""
{'='*60}
报告生成: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Somn项目 - 智能代码质量检查系统
{'='*60}
"""
        return report

    def run_all(self, target: str) -> bool:
        """运行所有检查"""
        print("\n" + "="*60)
        print("Somn 代码质量自动化检查")
        print(f"目标目录: {target}")
        print(f"复杂度阈值: {self.config.max_complexity}")
        print("="*60)

        # 预处理目标路径
        if not os.path.exists(target):
            print(f"错误: 目标目录不存在: {target}")
            return False

        results = {
            'pylint': self.check_pylint(target),
            'flake8': self.check_flake8(target),
            'complexity': self.check_complexity(target),
            'security': self.check_security(target),
        }

        # 生成报告
        report = self.generate_report(target)
        print(report)

        # 保存报告
        report_path = Path(target).parent / "code_quality_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n报告已保存: {report_path}")

        # 返回结果
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        print(f"\n通过: {passed}/{total}")

        return all(results.values())


def main():
    parser = argparse.ArgumentParser(
        description="Somn代码质量自动化检查",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python code_quality_check.py                                    # 检查src目录
  python code_quality_check.py --target src/core                # 检查特定目录
  python code_quality_check.py --threshold 10                    # 设置更低阈值
  python code_quality_check.py --config complexity.json         # 从配置文件加载
        """
    )
    parser.add_argument(
        '--target', '-t',
        default='smart_office_assistant/src',
        help='检查目标目录 (默认: smart_office_assistant/src)'
    )
    parser.add_argument(
        '--threshold', '-th',
        type=int,
        default=15,
        help='McCabe圈复杂度阈值 (默认: 15)'
    )
    parser.add_argument(
        '--line-length', '-l',
        type=int,
        default=120,
        help='最大行长度 (默认: 120)'
    )

    args = parser.parse_args()

    config = QualityConfig(
        max_complexity=args.threshold,
        max_line_length=args.line_length,
    )

    checker = QualityChecker(config)
    success = checker.run_all(args.target)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
