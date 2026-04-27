#!/usr/bin/env python3
"""运行所有测试并生成报告"""
import subprocess
import sys
from pathlib import Path

def run_pytest(test_file=None):
    """运行 pytest 并捕获输出"""
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/", "-v", "--tb=short",
        "--color=yes"
    ]
    if test_file:
        cmd[2] = test_file
    
    result = subprocess.run(
        cmd,
        cwd=Path(__file__).parent,
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr

if __name__ == "__main__":
    print("=" * 80)
    print("Somn 完整测试报告")
    print("=" * 80)
    print()
    
    output = run_pytest()
    print(output)
    
    # 统计
    if "passed" in output:
        lines = output.split('\n')
        for line in lines:
            if "passed" in line or "failed" in line:
                if "===" not in line or "warnings" not in line:
                    print("\n" + line)
