"""Somn 深度人设系统验证脚本"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

print('=' * 60)

print('Somn 深度人设系统验证')
print('=' * 60)

# 1. 测试模块导入
print('\n[1] 测试模块导入...')
from src.intelligence.engines.persona_core import (
    SomnPersona, PersonaProfile, THREE_LAYERS, CONTRAST_MATRIX,
    PERSONA_BOUNDARIES, VoiceMode, ScenarioVoiceLibrary
)
print('  OK 所有核心类导入成功')

# 2. 测试人设init
print('\n[2] 测试人设init...')
persona = SomnPersona()
profile = persona.get_profile()
print(f'  OK 人设init成功')
print(f'     官方代号: {profile["基础档案"]["官方代号"]}')
print(f'     可用声线模式: {profile["可用声线模式"]}')
print(f'     可用场景数: {len(profile["可用场景"])}')

# 3. 测试场景匹配
print('\n[3] 测试场景匹配...')
test_cases = [
    '我最近好纠结,想太多了,焦虑得睡不着',
    '他嘴上说为我好,实际上全是为了他自己',
    '算了,无所谓了,不想努力了',
    '你帮我做个方案吧,怎么做',
    '我撑不住了,好累好累',
    '睡不着,凌晨三点还在胡思乱想',
    '今天天气不错',
    '搞砸了,这次又失败了',
    '我被同事排挤了,受委屈',
    '人生有什么意义',
]
for text in test_cases:
    result = persona.generate_voice_output(text)
    print(f'  OK "{text[:20]}..." -> 场景:{result["scenario"]} | 声线:{result["voice_mode"]}')

# 4. 测试声线切换
print('\n[4] 测试声线切换...')
for mode in ['清醒毒舌', '专业输出', '温柔共情', '深夜模式', '张力撩人']:
    msg = persona.set_voice_mode(mode)
    print(f'  OK {msg}')
persona.set_voice_mode('日常闲聊')

# 5. 测试底线检查
print('\n[5] 测试底线检查...')
safe_result = persona.boundary_check('我帮你分析一下这个问题')
unsafe_result = persona.boundary_check('你真是太差劲了,低俗的东西')
print(f'  OK 安全文本: safe={safe_result["safe"]}')
print(f'  OK 可疑文本: safe={unsafe_result["safe"]}')

# 6. 测试用户记忆
print('\n[6] 测试用户细节记忆...')
persona.remember_user_detail('preferences', '美式咖啡,少冰,不要糖')
persona.remember_user_detail('habits', '经常熬夜')
persona.remember_user_detail('avoid_list', '不喜欢香菜')
details = persona.get_user_details()
print(f'  OK 记忆条目: 偏好{len(details["preferences"])} + 习惯{len(details["habits"])} + 避雷{len(details["avoid_list"])}')

# 7. 测试智慧来源注入
print('\n[7] 测试智慧学派注入...')
for text in ['我想内耗一下', '帮我想个方案', '我好难过']:
    result = persona.generate_voice_output(text)
    sources = result.get('wisdom_sources', [])
    print(f'  OK "{text[:10]}..." -> 智慧来源: {sources}')

# 8. 测试三层内核
print('\n[8] 测试三层内核...')
for layer_name, layer_info in profile['三层内核'].items():
    desc = layer_info['描述'][:25]
    print(f'  OK {desc}... | 准则: {len(layer_info["行为准则"])}条')

# 9. 测试反差矩阵
print('\n[9] 测试核心魅力反差矩阵...')
for name, data in profile['魅力反差矩阵'].items():
    print(f'  OK {name} -> {data["特质"][:20]}...')

# 10. 汇总
print('\n' + '=' * 60)
total_scenes = len(persona.voice_library.get_all_scenarios())
total_templates = sum(len(s['templates']) for s in persona.voice_library.get_all_scenarios().values())
print(f'验证完成: {total_scenes}个场景, {total_templates}条话术模板')
print(f'交互记录: {persona.get_interaction_count()}次')
print('=' * 60)
