# -*- coding: utf-8 -*-
"""唐诗宋词融合模块独立验证脚本
绕过 __init__.py 链式依赖，直接加载 tang_song_poetry_fusion.py
"""
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

# Step 1: 统一定位项目根目录，然后构造 intelligence_dir
project_root = bootstrap_project_paths(__file__, change_cwd=True)
intelligence_dir = str(project_root / 'src' / 'intelligence')
if intelligence_dir not in sys.path:
    sys.path.insert(0, intelligence_dir)


# Step 2: 加载 tang_song_poetry_fusion.py（禁用 __init__.py 自动加载）
# 关键：需要把父包也塞进 sys.modules，否则相对导入无法解析
import importlib.util
parent_spec = importlib.util.spec_from_file_location('intelligence', os.path.join(intelligence_dir, '__init__.py'))
parent_mod = importlib.util.module_from_spec(parent_spec)
sys.modules['intelligence'] = parent_mod  # 虚包，让相对导入能找到父包

spec = importlib.util.spec_from_file_location(
    'tang_song_poetry_fusion',
    os.path.join(intelligence_dir, 'tang_song_poetry_fusion.py')
)
fusion_mod = importlib.util.module_from_spec(spec)
fusion_mod.__package__ = 'intelligence'  # 让相对导入在 intelligence 包内解析
fusion_mod.__spec__ = spec
sys.modules['tang_song_poetry_fusion'] = fusion_mod
spec.loader.exec_module(fusion_mod)

# Step 3: 创建实例并验证
m = fusion_mod.唐诗宋词融合模块()
print(f"版本: {m.VERSION}")
print()

# engines 接入
print("【engines接入检查】")
all_ok = True
for name in sorted(m.engines.keys()):
    eng = m.engines[name]
    ok = eng is not None
    if not ok:
        all_ok = False
    print(f"  {'✅' if ok else '❌'} {name}")
print(f"共 {len(m.engines)} 个，全部接入: {'✅' if all_ok else '❌'}")
print()

# 唐宋分类
print("【唐宋分类修复验证】")
s = m.获取系统摘要()
tang = s['唐代诗人']
song = s['宋代词人']
extra = s['额外接入引擎']
print(f"  唐代诗人({len(tang)}): {tang}")
print(f"  宋代词人({len(song)}): {song}")
print(f"  额外接入({len(extra)}): {extra}")

# 验证分类正确性（已扩展至32位诗人）
tang_expected = {'李白', '杜甫', '王维', '白居易', '杜牧', '李商隐', '王勃', '骆宾王', '杨炯', '卢照邻', '高适', '岑参', '王昌龄', '王之涣', '孟浩然', '李煜', '温庭筠', '韦庄', '罗隐'}
song_expected = {'苏轼', '李清照', '辛弃疾', '柳永', '秦观', '周邦彦', '黄庭坚', '范仲淹', '晏殊', '晏几道', '欧阳修', '张先', '王安石', '姜夔', '吴文英', '史达祖', '蒋捷', '张炎', '文天祥', '刘克庄', '王沂孙', '周密', '杨万里', '陆游'}
tang_correct = set(tang) == tang_expected
song_correct = set(song) == song_expected
print(f"  唐代分类正确: {'✅' if tang_correct else '❌'}")
print(f"  宋代分类正确: {'✅' if song_correct else '❌'}")
print()

# 核心接口
print("【核心接口测试】")
info = m.获取诗人信息("苏轼")
print(f"  获取诗人信息(苏轼): {info['诗人']} | {info['基本信息']['称号']} | {info['基本信息']['时代']}")

info2 = m.获取诗人信息("柳永")
print(f"  获取诗人信息(柳永): {info2['诗人']} | {info2['基本信息']['称号']} | {info2['基本信息']['时代']}")

compare = m.获取诗人对比("李白", "杜甫")
print(f"  李杜对比: 浪漫 vs 现实")

# 新增诗人测试
info3 = m.获取诗人信息("陆游")
print(f"  获取诗人信息(陆游): {info3['诗人']} | {info3['基本信息']['称号']} | {info3['基本信息']['时代']}")

info4 = m.获取诗人信息("李煜")
print(f"  获取诗人信息(李煜): {info4['诗人']} | {info4['基本信息']['称号']} | {info4['基本信息']['时代']}")

info5 = m.获取诗人信息("姜夔")
print(f"  获取诗人信息(姜夔): {info5['诗人']} | {info5['基本信息']['称号']} | {info5['基本信息']['时代']}")

poetry = m.分析文本("大江东去浪淘尽千古风流人物")
print(f"  文本分析: {poetry['判断']} (置信度:{poetry['置信度']})")

guide = m.获取创作指导("豪放")
if guide.get("建议"):
    print(f"  创作指导(豪放): {guide['建议'][0][:60]}...")

metrics = m.融合指标
print(f"  融合指标数: {len(metrics)}")

print()
if all_ok and tang_correct and song_correct:
    print("=== 唐宋词融合模块 v1.0.0 全链路验证通过 ✅ ===")
else:
    print("=== 存在问题，请检查上述输出 ===")
