# -*- coding: utf-8 -*-
"""
神之架构完整整合 - Claw岗位入职脚本 v3.0
=========================================

功能：
1. 从sage_registry解析贤者信息（部门、层级等）
2. 从court_positions解析岗位定义
3. 生成完整的贤者-岗位映射
4. 更新776个Claw YAML配置，填充完整岗位信息

执行方式：
    python _onboarding_claws_v3.py

版本: v1.0.0
创建: 2026-04-22
"""

import sys
import json
import yaml
import logging
import re
from pathlib import Path
from typing import Dict, Optional, Tuple, List, Any

# 设置项目路径
PROJECT_ROOT = Path(__file__).resolve().parents[4]
CLAW_CONFIGS_DIR = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "claws" / "configs"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 一、提取贤者注册表数据
# ═══════════════════════════════════════════════════════════════════════════════

def parse_sage_registry() -> Dict[str, Any]:
    """从sage_registry解析贤者数据"""
    logger.info("解析贤者注册表...")
    
    sage_file = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "engines" / "cloning" / "_sage_registry_full.py"
    extra_file = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "engines" / "cloning" / "_sage_registry_extra.py"
    
    sage_info = {}
    
    # 解析主注册表
    with open(sage_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则提取 SageMeta 数据
    pattern = r'SageMeta\s*\(\s*name\s*=\s*"([^"]+)"\s*,\s*name_en\s*=\s*"([^"]+)"\s*,\s*school\s*=\s*"([^"]+)"\s*,\s*tier\s*=\s*SageTier\.(\w+)\s*,\s*era\s*=\s*"([^"]*)"[^)]*department\s*=\s*"([^"]*)"'
    
    matches = re.findall(pattern, content)
    for match in matches:
        name, name_en, school, tier, era, department = match
        sage_info[name] = {
            "name": name,
            "name_en": name_en,
            "school": school,
            "tier": tier,
            "era": era,
            "department": department,
        }
    
    # 解析补充注册表
    if extra_file.exists():
        with open(extra_file, 'r', encoding='utf-8') as f:
            extra_content = f.read()
        
        extra_matches = re.findall(pattern, extra_content)
        for match in extra_matches:
            name, name_en, school, tier, era, department = match
            if name not in sage_info:
                sage_info[name] = {
                    "name": name,
                    "name_en": name_en,
                    "school": school,
                    "tier": tier,
                    "era": era,
                    "department": department,
                }
    
    logger.info(f"  解析了 {len(sage_info)} 位贤者")
    return sage_info


# ═══════════════════════════════════════════════════════════════════════════════
# 二、提取神之架构岗位数据（带完整信息）
# ═══════════════════════════════════════════════════════════════════════════════

def parse_court_positions_v2() -> Tuple[Dict[str, Dict], Dict[str, Dict]]:
    """从court_positions解析岗位数据（改进版）"""
    logger.info("解析神之架构岗位体系...")
    
    court_file = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "engines" / "cloning" / "_court_positions.py"
    
    with open(court_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 提取完整岗位定义（包含pin、domain等）
    # id, name, department, pin, domain, si_name
    pos_pattern = r'id\s*=\s*"([^"]+)"\s*,\s*name\s*=\s*"([^"]+)"\s*,\s*department\s*=\s*"([^"]+)"'
    pos_matches = re.findall(pos_pattern, content)
    
    positions = {}
    for pos_id, name, dept in pos_matches:
        positions[pos_id] = {
            "name": name,
            "department": dept,
            "pin": "",
            "domain": "",
            "si_name": "",
            "nobility": "",
        }
    
    # 2. 提取pin信息
    pin_pattern = r'id\s*=\s*"([^"]+)"\s*,\s*pin\s*=\s*PinRank\.(\w+)'
    pin_matches = re.findall(pin_pattern, content)
    for pos_id, pin in pin_matches:
        if pos_id in positions:
            positions[pos_id]["pin"] = pin
    
    # 3. 提取domain信息
    domain_pattern = r'id\s*=\s*"([^"]+)"\s*,\s*domain\s*=\s*"([^"]*)"'
    domain_matches = re.findall(domain_pattern, content)
    for pos_id, domain in domain_matches:
        if pos_id in positions:
            positions[pos_id]["domain"] = domain
    
    # 4. 提取si_name信息
    si_pattern = r'id\s*=\s*"([^"]+)"\s*,\s*si_name\s*=\s*"([^"]*)"'
    si_matches = re.findall(si_pattern, content)
    for pos_id, si_name in si_matches:
        if pos_id in positions:
            positions[pos_id]["si_name"] = si_name
    
    # 5. 提取nobility信息
    noble_pattern = r'id\s*=\s*"([^"]+)"\s*,\s*nobility\s*=\s*NobilityRank\.(\w+)'
    noble_matches = re.findall(noble_pattern, content)
    for pos_id, noble in noble_matches:
        if pos_id in positions:
            positions[pos_id]["nobility"] = noble
    
    # 6. 提取贤者任命（从_builtin_assignments）
    # 格式: "孔子": "HJ_WJ_01",
    assign_pattern = r'"([^"]+)"\s*:\s*"([A-Z_]+\d+)"'
    assign_matches = re.findall(assign_pattern, content)
    
    assignments = {}
    for name, pos_id in assign_matches:
        if pos_id in positions:
            assignments[name] = pos_id
    
    logger.info(f"  解析了 {len(positions)} 个岗位")
    logger.info(f"  解析了 {len(assignments)} 个贤者任命")
    
    return positions, assignments


# ═══════════════════════════════════════════════════════════════════════════════
# 三、构建映射并更新Claw配置
# ═══════════════════════════════════════════════════════════════════════════════

def load_claw_yaml(file_path: Path) -> Optional[Dict]:
    """加载单个Claw YAML配置"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.warning(f"  加载失败 {file_path.name}: {e}")
        return None


def update_claw_with_full_info(
    file_path: Path,
    sage_info: Dict,
    positions: Dict,
    assignments: Dict,
) -> bool:
    """更新Claw配置，包含完整岗位信息"""
    data = load_claw_yaml(file_path)
    if not data:
        return False
    
    claw_name = file_path.stem
    
    # 1. 获取贤者基本信息
    info = sage_info.get(claw_name)
    if not info:
        # 尝试模糊匹配
        for name, sinfo in sage_info.items():
            if claw_name == name or claw_name in name or name in claw_name:
                info = sinfo
                break
    
    if info:
        data["department"] = info.get("department", "")
        data["school"] = info.get("school", "")
        data["era"] = info.get("era", "")
        
        # 层级名称映射
        tier_map = {
            "GRANDMASTER": "超级大师",
            "FOUNDER": "创始人",
            "MASTER": "集大成者",
            "SCHOLAR": "学者",
            "PRACTITIONER": "实践者",
        }
        data["tier_name"] = tier_map.get(info.get("tier", ""), "")
    
    # 2. 获取岗位信息
    pos_id = assignments.get(claw_name, "")
    if pos_id and pos_id in positions:
        pos = positions[pos_id]
        data["court_position"] = pos_id
        data["position_name"] = pos.get("name", "")
        data["position_department"] = pos.get("department", "")
        data["position_pin"] = pos.get("pin", "")
        data["position_domain"] = pos.get("domain", "")
        data["position_si_name"] = pos.get("si_name", "")
        
        # 爵位映射
        noble_map = {
            "WANGJUE": "王爵",
            "GONGJUE": "公爵",
            "HOUJUE": "侯爵",
            "BOJUE": "伯爵",
        }
        data["nobility"] = noble_map.get(pos.get("nobility", ""), "")
    else:
        # 没有岗位任命，使用默认值
        data["court_position"] = ""
        data["position_name"] = ""
        data["position_department"] = info.get("department", "") if info else ""
        data["position_pin"] = ""
        data["position_domain"] = ""
        data["position_si_name"] = ""
        data["nobility"] = ""
    
    # 写入回文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False)
        return True
    except Exception as e:
        logger.error(f"  写入失败 {file_path.name}: {e}")
        return False


def onboard_all_claws_v3(
    claw_dir: Path,
    sage_info: Dict,
    positions: Dict,
    assignments: Dict,
) -> Dict[str, Any]:
    """执行所有Claw入职"""
    logger.info(f"开始Claw入职流程: {claw_dir}")
    
    # 获取所有YAML文件
    yaml_files = list(claw_dir.glob("*.yaml"))
    logger.info(f"  找到 {len(yaml_files)} 个Claw配置")
    
    success_count = 0
    fail_count = 0
    positioned_count = 0
    
    for yaml_file in yaml_files:
        claw_name = yaml_file.stem
        
        # 检查是否有岗位任命
        if claw_name in assignments:
            positioned_count += 1
        
        if update_claw_with_full_info(yaml_file, sage_info, positions, assignments):
            success_count += 1
        else:
            fail_count += 1
    
    logger.info(f"  入职完成: 成功 {success_count}, 失败 {fail_count}")
    logger.info(f"  已有岗位任命: {positioned_count}")
    
    return {
        "total": len(yaml_files),
        "success": success_count,
        "failed": fail_count,
        "positioned": positioned_count,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 四、生成统计报告
# ═══════════════════════════════════════════════════════════════════════════════

def generate_report_v3(
    sage_info: Dict,
    positions: Dict,
    assignments: Dict,
    onboarding_result: Dict,
) -> Dict:
    """生成入职报告"""
    
    # 统计各部门
    dept_stats = {}
    for info in sage_info.values():
        dept = info.get("department", "未知")
        dept_stats[dept] = dept_stats.get(dept, 0) + 1
    
    # 统计岗位
    pos_dept_stats = {}
    for pos in positions.values():
        dept = pos.get("department", "未知")
        pos_dept_stats[dept] = pos_dept_stats.get(dept, 0) + 1
    
    # 统计任命
    assigned_dept_stats = {}
    for name, pos_id in assignments.items():
        if pos_id in positions:
            dept = positions[pos_id].get("department", "未知")
            assigned_dept_stats[dept] = assigned_dept_stats.get(dept, 0) + 1
    
    report = {
        "timestamp": "2026-04-22",
        "version": "v1.0.0",
        "summary": {
            "total_sages": len(sage_info),
            "total_positions": len(positions),
            "total_assignments": len(assignments),
            "total_claws": onboarding_result["total"],
            "onboarded_success": onboarding_result["success"],
            "onboarded_failed": onboarding_result["failed"],
            "positioned_claws": onboarding_result["positioned"],
        },
        "sage_department_stats": dept_stats,
        "position_department_stats": pos_dept_stats,
        "assignment_department_stats": assigned_dept_stats,
    }
    
    return report


# ═══════════════════════════════════════════════════════════════════════════════
# 五、主执行流程
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("神之架构完整整合 - Claw岗位入职脚本 v3.0")
    logger.info("=" * 60)
    
    # 1. 解析贤者注册表
    sage_info = parse_sage_registry()
    
    # 2. 解析神之架构岗位体系
    positions, assignments = parse_court_positions_v2()
    
    # 3. 执行Claw入职
    onboarding_result = onboard_all_claws_v3(
        CLAW_CONFIGS_DIR,
        sage_info,
        positions,
        assignments
    )
    
    # 4. 生成报告
    report = generate_report_v3(sage_info, positions, assignments, onboarding_result)
    
    # 保存报告
    OUTPUT_REPORT = PROJECT_ROOT / "_onboarding_claws_report.json"
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info("=" * 60)
    logger.info("入职完成！")
    logger.info(f"  总贤者: {report['summary']['total_sages']}")
    logger.info(f"  总岗位: {report['summary']['total_positions']}")
    logger.info(f"  已有任命: {report['summary']['total_assignments']}")
    logger.info(f"  入职Claw: {report['summary']['total_claws']}")
    logger.info(f"  有岗位Claw: {report['summary']['positioned_claws']}")
    logger.info(f"  报告已保存: {OUTPUT_REPORT}")
    logger.info("=" * 60)
    
    # 输出部门统计
    logger.info("\n贤者部门分布:")
    for dept, count in sorted(report["sage_department_stats"].items(), key=lambda x: -x[1])[:8]:
        logger.info(f"  {dept}: {count}")
    
    logger.info("\n岗位部门分布:")
    for dept, count in sorted(report["position_department_stats"].items(), key=lambda x: -x[1])[:8]:
        logger.info(f"  {dept}: {count}")
    
    return report


if __name__ == "__main__":
    main()