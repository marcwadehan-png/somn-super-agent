"""全局A/B测试运行器 - 运行dual_track下所有测试文件"""
import subprocess
import sys
import os

os.chdir(r"d:\AI\somn\smart_office_assistant")
python = r"C:\Users\18000\.workbuddy\binaries\python\versions\3.13.12\python.exe"

test_dir = r"src\intelligence\dual_track"
test_files = sorted([f for f in os.listdir(test_dir) if f.startswith("test_") and f.endswith(".py")])

print(f"发现 {len(test_files)} 个测试文件:\n")

total_passed = 0
total_failed = 0
total_errors = 0
all_failures = {}

for tf in test_files:
    test_path = os.path.join(test_dir, tf)
    print(f"{'='*60}")
    print(f"测试文件: {tf}")
    print(f"{'='*60}")
    
    result = subprocess.run(
        [python, "-m", "pytest", test_path, "-v", "--tb=short", "--no-header"],
        capture_output=True, text=True, timeout=120
    )
    
    # 解析输出
    output = result.stdout + result.stderr
    print(output)
    
    # 统计
    for line in output.split('\n'):
        if ' passed' in line and ('failed' in line or line.strip().startswith('passed')):
            # 提取 passed 和 failed 数量
            import re
            m = re.search(r'(\d+) passed', line)
            if m:
                total_passed += int(m.group(1))
            m2 = re.search(r'(\d+) failed', line)
            if m2:
                total_failed += int(m2.group(1))
            m3 = re.search(r'(\d+) error', line)
            if m3:
                total_errors += int(m3.group(1))
    
    # 收集失败
    for line in output.split('\n'):
        if line.strip().startswith('FAILED'):
            test_name = line.strip()
            # 找到对应的错误信息
            all_failures[tf] = all_failures.get(tf, [])
    
    # 如果有 FAILURES 段
    if 'FAILED' in output:
        in_failure = False
        failure_info = []
        for line in output.split('\n'):
            if '==== FAILURES ====' in line:
                in_failure = True
                continue
            if in_failure:
                if line.startswith('===='):
                    in_failure = False
                elif line.strip().startswith('FAILED') or line.strip().startswith('_'):
                    failure_info.append(line.strip())
                elif 'AssertionError' in line or 'Error' in line or 'KeyError' in line or 'AttributeError' in line:
                    failure_info.append(line.strip())
        if failure_info:
            all_failures[tf] = failure_info

print(f"\n{'#'*60}")
print(f"全局测试汇总")
print(f"{'#'*60}")
print(f"总通过: {total_passed}")
print(f"总失败: {total_failed}")
print(f"总错误: {total_errors}")
print(f"测试文件: {len(test_files)}")

if all_failures:
    print(f"\n失败的测试文件:")
    for tf, failures in all_failures.items():
        print(f"\n  [{tf}]")
        for f in failures[:5]:
            print(f"    - {f}")
else:
    print(f"\n✅ 全部测试通过!")
