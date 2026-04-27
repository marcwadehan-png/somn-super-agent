# -*- coding: utf-8 -*-
"""
Claw岗位任职映射脚本 V1.0
===========================
直接import CourtPositionRegistry，实现三级映射。
V1.0: 补全SCHOOL_TO_DEPT映射（从43项→57项），覆盖全部70个未映射Claw。

版本: v1.0.0 | 2026-04-23
"""

import sys, json, yaml, logging, re
from pathlib import Path
from typing import Dict, List, Tuple, Any
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parents[4]
CLAW_CONFIGS_DIR = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "claws" / "configs"
SAGE_FILE = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "engines" / "cloning" / "_sage_registry_full.py"
SAGE_EXTRA_FILE = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "engines" / "cloning" / "_sage_registry_extra.py"

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

# 添加项目路径
sys.path.insert(0, str(PROJECT_ROOT / "smart_office_assistant" / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

# ═══════════════════════════════════════════════════════════════════════════════
# 一、Import获取完整岗位体系
# ═══════════════════════════════════════════════════════════════════════════════

from smart_office_assistant.src.intelligence.engines.cloning._court_positions import (
    CourtPositionRegistry, PinRank, NobilityRank, PositionType
)


def _to_pinrank(pin_val, is_zheng=True):
    """Safely convert pin value to PinRank enum."""
    if pin_val is None:
        return PinRank.CONG_7_PIN
    valid = [10,11,20,21,30,31,40,41,50,51,60,61,70,71,80,81,90,91]
    if pin_val in valid:
        return PinRank(pin_val)
    if not isinstance(pin_val, (int, float)):
        return PinRank.CONG_7_PIN
    zheng = True if is_zheng is None else is_zheng
    val = int(pin_val) * 10 + (0 if zheng else 1)
    return PinRank(val)


def _to_nobility(nob_val):
    """Safely convert nobility value to NobilityRank enum."""
    if isinstance(nob_val, int):
        try:
            return NobilityRank(nob_val)
        except ValueError:
            return NobilityRank.NOBLE_NONE
    return nob_val


logger.info("加载神之架构岗位体系...")
registry = CourtPositionRegistry()
all_positions = list(registry._positions.values())

PIN_NAMES = {
    PinRank.ZHENG_1_PIN: '正一品', PinRank.CONG_1_PIN: '从一品',
    PinRank.ZHENG_2_PIN: '正二品', PinRank.CONG_2_PIN: '从二品',
    PinRank.ZHENG_3_PIN: '正三品', PinRank.CONG_3_PIN: '从三品',
    PinRank.ZHENG_4_PIN: '正四品', PinRank.CONG_4_PIN: '从四品',
    PinRank.ZHENG_5_PIN: '正五品', PinRank.CONG_5_PIN: '从五品',
    PinRank.ZHENG_6_PIN: '正六品', PinRank.CONG_6_PIN: '从六品',
    PinRank.ZHENG_7_PIN: '正七品', PinRank.CONG_7_PIN: '从七品',
    PinRank.ZHENG_8_PIN: '正八品', PinRank.CONG_8_PIN: '从八品',
    PinRank.ZHENG_9_PIN: '正九品', PinRank.CONG_9_PIN: '从九品',
}
NOBLE_NAMES = {
    NobilityRank.WANGJUE: '王爵', NobilityRank.GONGJUE: '公爵',
    NobilityRank.HOUJUE: '侯爵', NobilityRank.BOJUE: '伯爵', NobilityRank.NOBLE_NONE: '',
}
PT_NAMES = {
    PositionType.SUPREME_SINGLE: 'supreme_single', PositionType.SUPREME_TRIPLE: 'supreme_triple',
    PositionType.SUPREME_DUAL: 'supreme_dual', PositionType.MANAGEMENT: 'management',
    PositionType.EXECUTION: 'execution', PositionType.SPECIALIST: 'specialist',
    PositionType.AUDIT: 'audit', PositionType.TEAM_LEADER: 'team_leader',
}

# 转为dict
positions = {}
for pos in all_positions:
    pin_enum = _to_pinrank(pos.pin, pos.is_zheng)
    nob_enum = _to_nobility(pos.nobility)
    positions[pos.id] = {
        'id': pos.id, 'name': pos.name, 'department': pos.department,
        'pin': pin_enum.name,
        'pin_name': PIN_NAMES.get(pin_enum, ''),
        'nobility': nob_enum.name,
        'nobility_name': NOBLE_NAMES.get(nob_enum, ''),
        'position_type': PT_NAMES.get(pos.position_type, 'execution'),
        'capacity': pos.capacity, 'domain': pos.domain, 'si_name': pos.si_name,
        'system_type': pos.system_type.value, 'is_zheng': pos.is_zheng,
        'suitable_schools': list(pos.suitable_schools) if pos.suitable_schools else [],
        'description': pos.description,
    }

logger.info(f"  岗位总量: {len(positions)}")

# ═══════════════════════════════════════════════════════════════════════════════
# 二、加载Claw和贤者数据
# ═══════════════════════════════════════════════════════════════════════════════

# 加载Claw
logger.info("加载Claw配置...")
claws = {}
for f in CLAW_CONFIGS_DIR.glob("*.yaml"):
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            data = yaml.safe_load(fh)
        if data and isinstance(data, dict):
            claws[f.stem] = data
    except Exception as e:
        logger.debug(f"claws[f.stem] = data失败: {e}")
logger.info(f"  加载了 {len(claws)} 个Claw")

# 解析贤者注册表
logger.info("解析贤者注册表...")
sage_info = {}
pattern = r'SageMeta\s*\(\s*name\s*=\s*"([^"]+)"\s*,\s*name_en\s*=\s*"([^"]+)"\s*,\s*school\s*=\s*"([^"]+)"\s*,\s*tier\s*=\s*SageTier\.(\w+)\s*,\s*era\s*=\s*"([^"]*)"[^)]*department\s*=\s*"([^"]*)"'
for sf in [SAGE_FILE, SAGE_EXTRA_FILE]:
    if sf.exists():
        with open(sf, 'r', encoding='utf-8') as f:
            for m in re.findall(pattern, f.read()):
                name, name_en, school, tier, era, dept = m
                sage_info[name] = {'name': name, 'school': school, 'tier': tier, 'era': era, 'department': dept}
logger.info(f"  解析了 {len(sage_info)} 位贤者")

# ═══════════════════════════════════════════════════════════════════════════════
# 三、预设任命提取
# ═══════════════════════════════════════════════════════════════════════════════

logger.info("提取预设任命...")
preset = {}  # sage_name -> pos_id
for pos_id, pos in positions.items():
    si = pos['si_name']
    if si and '团队' not in si and '专才' not in si:
        clean = re.sub(r'[（(][^)）]*[)）]', '', si).strip()
        if clean:
            preset[clean] = pos_id
    # 从description补充
    desc = pos['description']
    dm = re.search(r'由(\S+)担任', desc)
    if dm and dm.group(1) not in preset:
        preset[dm.group(1)] = pos_id

logger.info(f"  提取了 {len(preset)} 个预设任命")

# ═══════════════════════════════════════════════════════════════════════════════
# 四、部门→专员岗映射
# ═══════════════════════════════════════════════════════════════════════════════

dept_specialists = defaultdict(list)
for pos_id, pos in positions.items():
    if pos['position_type'] in ('specialist', 'team_leader'):
        dept_specialists[pos['department']].append(pos_id)
logger.info(f"  专员岗分布: {dict((k, len(v)) for k, v in dept_specialists.items())}")

# YAML六部 → 岗位体系专员岗部门路由（V1.0: 解决六部专员岗不足导致溢出到皇家的问题）
# V1.0更新: 六部已补充专员岗，优先路由到本部门
DEPT_FALLBACK_ROUTE = {
    '礼部': ['礼部', '文治系统', '标准系统', '翰林院', '皇家藏书阁'],
    '兵部': ['兵部', '军政系统', '五军都督府', '厂卫'],
    '工部': ['工部', '标准系统', '创新系统', '厂卫'],
    '户部': ['户部', '标准系统'],
    '刑部': ['刑部', '三法司', '厂卫'],
    '吏部': ['吏部', '内阁', '厂卫'],
    '皇家': ['皇家'],
    '皇家科学院': ['工部', '创新系统', '标准系统'],
    '太医院': ['工部', '标准系统'],
}

# 学派→部门映射（V1.0 — 补全所有Claw中出现的学派标签）
SCHOOL_TO_DEPT = {
    # ── 诸子百家 ──
    '儒家': '礼部', '道家': '礼部', '佛家': '礼部', '法家': '刑部', '兵家': '兵部',
    '墨家': '工部', '纵横家': '兵部', '阴阳家': '礼部', '名家': '礼部', '农家': '户部',
    '医家': '工部', '杂家': '礼部', '小说家': '礼部', '史家': '礼部',
    # ── 文艺类 ──
    '文学家': '礼部', '诗人': '礼部', '艺术家': '礼部', '音乐家': '礼部',
    '文学': '礼部', '文学批评家': '礼部', '翻译家': '礼部',
    # ── 思想哲学类 ──
    '思想家': '礼部', '哲学家': '礼部', '西方哲学': '礼部', '哲学': '礼部',
    '英国哲学': '礼部', '王阳明': '礼部', '杜威': '礼部', '顶级思维法': '礼部',
    '素书': '兵部', 'TOP_MIND': '礼部',
    # ── 科学技术类 ──
    '科学家': '工部', '科学': '工部', '科学思维': '工部',
    '数学': '工部', '天文学家': '工部', '地理学家': '工部', '发明家': '工部',
    '医学': '工部', '心理学': '工部', '心理学家': '工部',
    # ── 政治军事类 ──
    '政治家': '兵部', '军事家': '兵部', '政治': '兵部', '治理战略家': '兵部',
    # ── 经济管理类 ──
    '企业家': '户部', '经济学家': '户部', '投资家': '户部', '金融家': '户部',
    '经济': '户部', '管理': '户部', '管理学': '户部',
    # ── 社会人文类 ──
    '社会学家': '礼部', '史家': '礼部', '史学': '礼部', '教育家': '礼部',
    # ── 其他 ──
    '其他': '礼部', '道教/武术': '礼部', '茶道家': '户部',
}

# ═══════════════════════════════════════════════════════════════════════════════
# 五、三级映射算法
# ═══════════════════════════════════════════════════════════════════════════════

PIN_ORDER = {
    'ZHENG_1_PIN': 10, 'CONG_1_PIN': 11, 'ZHENG_2_PIN': 20, 'CONG_2_PIN': 21,
    'ZHENG_3_PIN': 30, 'CONG_3_PIN': 31, 'ZHENG_4_PIN': 40, 'CONG_4_PIN': 41,
    'ZHENG_5_PIN': 50, 'CONG_5_PIN': 51, 'ZHENG_6_PIN': 60, 'CONG_6_PIN': 61,
    'ZHENG_7_PIN': 70, 'CONG_7_PIN': 71, 'ZHENG_8_PIN': 80, 'CONG_8_PIN': 81,
    'ZHENG_9_PIN': 90, 'CONG_9_PIN': 91,
}

def match_claw(claw_name, claw_data, fill_count):
    """三级映射"""
    
    # P1: 预设任命
    if claw_name in preset:
        pid = preset[claw_name]
        if pid in positions:
            return pid, 'appointed', 1.0
    
    # 确定目标部门：YAML已有department优先，否则SCHOOL_TO_DEPT查找，最后默认礼部
    school = claw_data.get('school', '')
    claw_dept = claw_data.get('department', '').strip()
    target_dept = claw_dept or SCHOOL_TO_DEPT.get(school, '礼部')
    
    # P2: 认知维度匹配（V1.0: 多部门路由）
    fallback_depts_p2 = DEPT_FALLBACK_ROUTE.get(target_dept, [target_dept])
    mgmt = [pid for pid, p in positions.items()
            if p['department'] in fallback_depts_p2 and p['position_type'] not in ('specialist', 'team_leader')]
    mgmt.sort(key=lambda pid: PIN_ORDER.get(positions[pid]['pin'], 99))
    
    best_pid, best_score = None, 0.0
    cog = claw_data.get('cognitive_dimensions', {})
    cog_sum = sum(cog.values()) / max(len(cog), 1) if cog else 0
    strategy_val = cog.get('strategy', 0) + cog.get('decision_quality', 0) + cog.get('gov_decision', 0)
    
    for pid in mgmt:
        p = positions[pid]
        if fill_count.get(pid, 0) >= p['capacity'] and p['capacity'] < 999:
            continue
        
        score = 0.0
        # 学派匹配 (0.4)
        if school in p['suitable_schools']:
            score += 0.4
        elif any(school in s or s in school for s in p['suitable_schools'] if s):
            score += 0.2
        # domain匹配 (0.3)
        if p['domain'] and any(kw in str(cog) for kw in p['domain'][:20].split('/')):
            score += 0.3
        # 能力匹配 (0.3)
        score += min(strategy_val / 25.0, 1.0) * 0.3
        
        # 品秩与贤者层级匹配
        tier = sage_info.get(claw_name, {}).get('tier', '')
        pin_val = PIN_ORDER.get(p['pin'], 99)
        if pin_val <= 11 and tier in ('GRANDMASTER', 'FOUNDER', 'MASTER'):
            score += 0.15
        
        if score > best_score:
            best_score = score
            best_pid = pid
    
    if best_score >= 0.3 and best_pid:
        return best_pid, 'cognitive_match', round(best_score, 2)
    
    # P3: 专员兜底（V1.0: 精确学派匹配 + 负载均衡 + 多部门路由）
    fallback_depts = DEPT_FALLBACK_ROUTE.get(target_dept, [target_dept])
    
    # 收集所有候选专员岗，按匹配度分组
    exact_matches = []   # 学派精确匹配
    fuzzy_matches = []   # 学派模糊匹配
    default_matches = [] # 默认兜底
    
    for fb_dept in fallback_depts:
        specs = dept_specialists.get(fb_dept, [])
        for sp in specs:
            ss = positions[sp]['suitable_schools']
            load = fill_count.get(sp, 0)
            cap = positions[sp]['capacity']
            
            # 精确学派匹配
            if school and school in ss:
                # 负载均衡：优先选填充最少的岗
                exact_matches.append((sp, load))
            # 模糊匹配
            elif school and any(school in s or s in school for s in ss if s):
                fuzzy_matches.append((sp, load))
            # 默认候选
            elif not exact_matches and not fuzzy_matches:
                default_matches.append((sp, load))
    
    # 按负载排序（优先选填充最少的岗）
    exact_matches.sort(key=lambda x: x[1])
    fuzzy_matches.sort(key=lambda x: x[1])
    default_matches.sort(key=lambda x: x[1])
    
    if exact_matches:
        return exact_matches[0][0], 'specialist_fallback', 0.3
    if fuzzy_matches:
        return fuzzy_matches[0][0], 'specialist_fallback', 0.3
    if default_matches:
        return default_matches[0][0], 'specialist_fallback', 0.3
    
    # 终极兜底
    for pid, p in positions.items():
        if p['position_type'] == 'specialist':
            return pid, 'specialist_fallback', 0.1
    
    return '', 'unassigned', 0.0

# ═══════════════════════════════════════════════════════════════════════════════
# 六、执行映射
# ═══════════════════════════════════════════════════════════════════════════════

logger.info("开始三级映射...")
fill_count = defaultdict(int)
results = []

for claw_name, claw_data in claws.items():
    pos_id, method, conf = match_claw(claw_name, claw_data, fill_count)
    
    result = {'claw_name': claw_name, 'pos_id': pos_id, 'method': method, 'confidence': conf}
    if pos_id and pos_id in positions:
        p = positions[pos_id]
        result.update({
            'position_name': p['name'], 'department': p['department'],
            'pin': p['pin_name'], 'nobility': p['nobility_name'],
            'domain': p['domain'], 'si_name': p['si_name'],
        })
    else:
        result.update({'position_name': '', 'department': '', 'pin': '', 'nobility': '', 'domain': '', 'si_name': ''})
    
    results.append(result)
    fill_count[pos_id] += 1

appointed_count = sum(1 for r in results if r['method'] == 'appointed')
cognitive_count = sum(1 for r in results if r['method'] == 'cognitive_match')
specialist_count = sum(1 for r in results if r['method'] == 'specialist_fallback')
unassigned_count = sum(1 for r in results if r['method'] == 'unassigned')

logger.info(f"  预设任命: {appointed_count}, 认知匹配: {cognitive_count}, 专员兜底: {specialist_count}, 未分配: {unassigned_count}")

# ═══════════════════════════════════════════════════════════════════════════════
# 七、批量更新YAML
# ═══════════════════════════════════════════════════════════════════════════════

logger.info("批量更新Claw YAML...")
success, fail = 0, 0

for claw_name, claw_data in claws.items():
    r = next((x for x in results if x['claw_name'] == claw_name), None)
    if not r or not r['pos_id']:
        fail += 1
        continue
    
    fp = CLAW_CONFIGS_DIR / f"{claw_name}.yaml"
    if not fp.exists():
        fail += 1
        continue
    
    claw_data['court_position'] = r['pos_id']
    claw_data['position_name'] = r['position_name']
    claw_data['position_department'] = r['department']
    claw_data['position_pin'] = r['pin']
    claw_data['position_domain'] = r['domain']
    claw_data['position_si_name'] = r['si_name']
    claw_data['nobility'] = r['nobility']
    claw_data['claw_role'] = 'primary' if r['method'] == 'appointed' else 'secondary'
    claw_data['mapping_confidence'] = r['confidence']
    claw_data['mapping_method'] = r['method']
    
    try:
        with open(fp, 'w', encoding='utf-8') as f:
            yaml.safe_dump(claw_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        success += 1
    except Exception as e:
        logger.warning(f"  写入失败 {claw_name}: {e}")
        fail += 1

logger.info(f"  更新: 成功={success}, 失败={fail}")

# ═══════════════════════════════════════════════════════════════════════════════
# 八、生成报告
# ═══════════════════════════════════════════════════════════════════════════════

logger.info("生成任职报告...")

method_stats = defaultdict(int)
dept_stats = defaultdict(int)
noble_stats = defaultdict(int)
pos_fill = defaultdict(list)

for r in results:
    method_stats[r['method']] += 1
    if r['department']:
        dept_stats[r['department']] += 1
    if r['nobility']:
        noble_stats[r['nobility']] += 1
    if r['pos_id']:
        pos_fill[r['pos_id']].append(r['claw_name'])

lines = []
lines.append("# 贤者Claw任职报告 V1.0")
lines.append("")
lines.append(f"> **日期**: 2026-04-23 | **方案**: 神之架构V6.0三级映射 | **覆盖率**: {((len(results)-unassigned_count)/len(results)*100):.1f}%")
lines.append(f"> **总Claw**: {len(results)} | **总岗位**: {len(positions)} | **更新成功**: {success}")
lines.append("")

# 一、总览
lines.append("## 一、任职总览")
lines.append("")
lines.append("| 指标 | 数值 |")
lines.append("|------|------|")
lines.append(f"| 预设任命(appointed) | {appointed_count} |")
lines.append(f"| 认知匹配(cognitive_match) | {cognitive_count} |")
lines.append(f"| 专员兜底(specialist_fallback) | {specialist_count} |")
lines.append(f"| 未分配(unassigned) | {unassigned_count} |")
lines.append(f"| **覆盖率** | **{((len(results)-unassigned_count)/len(results)*100):.1f}%** |")
lines.append("")

# 二、预设任命明细
lines.append("## 二、预设任命明细")
lines.append("")
lines.append("| 贤者 | 岗位ID | 岗位名称 | 品秩 | 爵位 | 部门 |")
lines.append("|------|--------|---------|------|------|------|")
for r in sorted((x for x in results if x['method'] == 'appointed'), key=lambda x: (
    {'王爵': 0, '公爵': 1, '侯爵': 2, '伯爵': 3, '': 9}.get(x['nobility'], 9), x['pin']
)):
    lines.append(f"| {r['claw_name']} | {r['pos_id']} | {r['position_name']} | {r['pin']} | {r['nobility'] or '-'} | {r['department']} |")
lines.append("")

# 三、各部门分布
lines.append("## 三、各部门任职分布")
lines.append("")
lines.append("| 部门 | 任职数 | 占比 |")
lines.append("|------|--------|------|")
for dept, cnt in sorted(dept_stats.items(), key=lambda x: -x[1]):
    lines.append(f"| {dept} | {cnt} | {cnt/len(results)*100:.1f}% |")
lines.append("")

# 四、管理层岗位填充
lines.append("## 四、管理层岗位填充详情")
lines.append("")
lines.append("| 岗位ID | 岗位名称 | 部门 | 品秩 | 爵位 | 填充Claw |")
lines.append("|--------|---------|------|------|------|---------|")
for pid in sorted(positions.keys()):
    p = positions[pid]
    if p['position_type'] in ('specialist', 'team_leader'):
        continue
    filled = pos_fill.get(pid, [])
    filled_str = ', '.join(filled[:5]) + (f" (+{len(filled)-5})" if len(filled) > 5 else '') if filled else '(空)'
    lines.append(f"| {pid} | {p['name']} | {p['department']} | {p['pin_name']} | {p['nobility_name'] or '-'} | {filled_str} |")
lines.append("")

# 五、未分配
if unassigned_count > 0:
    lines.append("## 五、未分配Claw")
    lines.append("")
    for r in results:
        if r['method'] == 'unassigned':
            lines.append(f"- {r['claw_name']}")
    lines.append("")

report_text = '\n'.join(lines)
report_path = PROJECT_ROOT / "file" / "系统文件" / "Claw任职报告_V1.0.md"
report_path.parent.mkdir(parents=True, exist_ok=True)
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_text)

json_path = PROJECT_ROOT / "file" / "系统文件" / "claw_appointment_results.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

logger.info("=" * 60)
logger.info(f"任职完成! 覆盖率={((len(results)-unassigned_count)/len(results)*100):.1f}%")
logger.info(f"报告: {report_path}")
logger.info("=" * 60)
