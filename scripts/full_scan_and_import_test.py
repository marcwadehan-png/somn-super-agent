"""
Somn 全链路扫描与导入测试脚本
1. 扫描所有代码，建立完整模块注册清单
2. 逐层导入测试：从somn.py启动，检查所有子模块能否正常加载
3. 输出导入断裂清单
"""
import sys
import os
import importlib
import traceback
from pathlib import Path
from collections import defaultdict

# === 路径引导 ===
_SCRIPT_DIR = Path(__file__).resolve().parent if "__file__" in dir() else Path(r"d:\AI\somn\scripts")
_PROJECT_ROOT = _SCRIPT_DIR.parent
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_PROJECT_ROOT / "smart_office_assistant"))
sys.path.insert(0, str(_PROJECT_ROOT / "smart_office_assistant" / "src"))

results = {
    "modules": [],          # 所有可导入模块
    "failed": [],           # 导入失败
    "packages": [],         # 所有包
    "classes": {},          # 模块 -> 类名列表
    "functions": {},        # 模块 -> 顶层函数列表
    "total_files": 0,
    "total_lines": 0,
    "import_errors": defaultdict(list),  # 错误类型 -> 模块列表
}

# ============================================================
# Phase 1: 扫描所有 .py 文件，建立完整模块清单
# ============================================================
print("=" * 80)
print("Phase 1: 扫描所有代码，建立完整模块注册清单")
print("=" * 80)

base_pkg = _PROJECT_ROOT / "smart_office_assistant"
all_py_files = []

for py_file in sorted(base_pkg.rglob("*.py")):
    rel = py_file.relative_to(base_pkg)
    all_py_files.append(rel)
    results["total_files"] += 1

    # 统计代码行数
    try:
        lines = py_file.read_text(encoding="utf-8", errors="ignore")
        non_empty = sum(1 for l in lines.splitlines() if l.strip() and not l.strip().startswith("#"))
        results["total_lines"] += non_empty
    except Exception:
        pass

print(f"\n扫描完成: {results['total_files']} 个 .py 文件, {results['total_lines']} 行有效代码")

# 识别所有包 (__init__.py 所在目录)
for py_file in all_py_files:
    if py_file.name == "__init__.py":
        parts = list(py_file.parts[:-1])
        pkg_name = ".".join(parts)
        results["packages"].append(pkg_name)

print(f"包 (含子包): {len(results['packages'])} 个")

# 识别所有模块（.py 文件，排除 __init__.py 和测试）
all_modules = []
for py_file in all_py_files:
    if "tests" in py_file.parts:
        continue
    parts = list(py_file.parts[:-1])
    if py_file.name == "__init__.py":
        mod_name = ".".join(parts) if parts else "smart_office_assistant"
    else:
        stem = py_file.stem
        mod_name = ".".join(parts + [stem]) if parts else stem
    all_modules.append(mod_name)

all_modules = sorted(set(all_modules))
print(f"可导入模块（排除测试）: {len(all_modules)} 个")

# ============================================================
# Phase 2: 逐层导入测试
# ============================================================
print("\n" + "=" * 80)
print("Phase 2: 逐层导入测试")
print("=" * 80)

# 按层级分组显示
max_depth = 0
module_depths = defaultdict(list)
for mod in all_modules:
    depth = mod.count(".")
    module_depths[depth].append(mod)
    if depth > max_depth:
        max_depth = depth

print(f"最大导入深度: {max_depth} 层\n")

failed_modules = []
success_count = 0

for depth in range(max_depth + 1):
    mods_at_depth = module_depths[depth]
    print(f"--- 深度 {depth} ({len(mods_at_depth)} 个模块) ---")
    
    depth_ok = 0
    depth_fail = 0
    
    for mod_name in mods_at_depth:
        try:
            mod = importlib.import_module(mod_name)
            results["modules"].append(mod_name)
            
            # 提取类和函数
            cls_list = []
            func_list = []
            for attr_name in dir(mod):
                if attr_name.startswith("_"):
                    continue
                attr = getattr(mod, attr_name, None)
                if attr is None:
                    continue
                if isinstance(attr, type):
                    cls_list.append(attr_name)
                elif callable(attr) and hasattr(attr, '__module__') and attr.__module__ == mod_name:
                    func_list.append(attr_name)
            
            if cls_list:
                results["classes"][mod_name] = cls_list
            if func_list:
                results["functions"][mod_name] = func_list
            
            depth_ok += 1
            success_count += 1
            
            # 只在有类/函数时显示
            parts = cls_list + func_list
            if parts:
                short = mod_name.split(".")[-1] if "." in mod_name else mod_name
                indicator = f"  [{len(cls_list)}C/{len(func_list)}F]"
                print(f"  OK {mod_name}{indicator}")
            else:
                print(f"  OK {mod_name}")
                
        except Exception as e:
            depth_fail += 1
            failed_modules.append((mod_name, str(e)))
            results["failed"].append((mod_name, str(e)))
            err_type = type(e).__name__
            results["import_errors"][err_type].append(mod_name)
            print(f"  FAIL {mod_name}: {err_type}: {e}")
    
    if depth_fail > 0:
        print(f"  >> 深度 {depth}: {depth_ok} OK, {depth_fail} FAIL")
    else:
        print(f"  >> 深度 {depth}: 全部通过")

# ============================================================
# Phase 3: 汇总报告
# ============================================================
print("\n" + "=" * 80)
print("Phase 3: 导入测试汇总报告")
print("=" * 80)

total = len(all_modules)
fail_count = len(failed_modules)
ok_count = total - fail_count
rate = (ok_count / total * 100) if total > 0 else 0

print(f"\n总模块数: {total}")
print(f"成功导入: {ok_count} ({rate:.1f}%)")
print(f"导入失败: {fail_count}")

# 统计类和函数
total_classes = sum(len(v) for v in results["classes"].values())
total_functions = sum(len(v) for v in results["functions"].values())
print(f"注册类:   {total_classes}")
print(f"注册函数: {total_functions}")

if failed_modules:
    print(f"\n{'=' * 60}")
    print(f"导入断裂清单 ({fail_count} 个)")
    print(f"{'=' * 60}")
    
    # 按错误类型分组
    for err_type, mods in sorted(results["import_errors"].items()):
        print(f"\n[{err_type}] ({len(mods)} 个)")
        for mod_name, err_msg in failed_modules:
            if any(m == mod_name for m in mods):
                # 提取关键错误信息
                short_err = err_msg.split("\n")[0][:120]
                print(f"  - {mod_name}: {short_err}")
else:
    print("\n所有模块导入成功，完整代码链可同时启动!")

# ============================================================
# 模块注册清单（按包分组输出）
# ============================================================
print(f"\n{'=' * 80}")
print("完整模块注册清单")
print(f"{'=' * 80}")

pkg_modules = defaultdict(list)
for mod_name in results["modules"]:
    parts = mod_name.rsplit(".", 1)
    if len(parts) == 2:
        pkg_modules[parts[0]].append((parts[1], mod_name))
    else:
        pkg_modules["(root)"].append((mod_name, mod_name))

for pkg_name in sorted(pkg_modules.keys()):
    mods = sorted(pkg_modules[pkg_name], key=lambda x: x[0])
    cls_count = sum(len(results["classes"].get(m[1], [])) for m in mods)
    func_count = sum(len(results["functions"].get(m[1], [])) for m in mods)
    print(f"\n[{pkg_name}] ({len(mods)} 模块, {cls_count} 类, {func_count} 函数)")
    for short_name, full_name in mods:
        cls = results["classes"].get(full_name, [])
        func = results["functions"].get(full_name, [])
        if cls or func:
            items = []
            if cls:
                items.append(f"C:{','.join(cls[:3])}")
                if len(cls) > 3:
                    items.append(f"+{len(cls)-3}")
            if func:
                items.append(f"F:{','.join(func[:3])}")
                if len(func) > 3:
                    items.append(f"+{len(func)-3}")
            print(f"  {short_name}  # {', '.join(items)}")
        else:
            print(f"  {short_name}")

print(f"\n{'=' * 80}")
print("扫描完成")
print(f"{'=' * 80}")
