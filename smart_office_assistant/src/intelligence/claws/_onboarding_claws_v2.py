# -*- coding: utf-8 -*-
"""
贤者入职神之架构 - Claw岗位入职脚本
=====================================

功能：
1. 直接读取贤者注册表JSON/文本数据
2. 读取神之架构岗位体系
3. 更新776个Claw YAML配置

执行方式：
    python _onboarding_claws_v2.py

版本: v2.0.0 (简化版，直接读取数据)
创建: 2026-04-22
"""

import os
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
# 一、提取贤者注册表数据（通过解析源代码）
# ═══════════════════════════════════════════════════════════════════════════════

def parse_sage_registry() -> Dict[str, Any]:
    """从sage_registry_full.py解析贤者数据"""
    logger.info("解析贤者注册表...")
    
    sage_file = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "engines" / "cloning" / "_sage_registry_full.py"
    extra_file = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "engines" / "cloning" / "_sage_registry_extra.py"
    
    sage_info = {}
    
    # 解析主注册表
    with open(sage_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则提取 SageMeta 数据
    # 匹配模式：SageMeta(name="...", name_en="...", school="...", ...)
    pattern = r'SageMeta\s*\(\s*name\s*=\s*"([^"]+)"\s*,\s*name_en\s*=\s*"([^"]+)"\s*,\s*school\s*=\s*"([^"]+)"\s*,\s*tier\s*=\s*SageTier\.(\w+)\s*,\s*era\s*=\s*"([^"]*)"\s*,\s*[^)]*department\s*=\s*"([^"]*)"'
    
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
# 二、提取神之架构岗位数据
# ═══════════════════════════════════════════════════════════════════════════════

def parse_court_positions() -> Dict[str, Any]:
    """从_court_positions.py解析岗位数据"""
    logger.info("解析神之架构岗位体系...")
    
    court_file = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence" / "engines" / "cloning" / "_court_positions.py"
    
    positions = {}
    
    with open(court_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 _sage_position_map 的定义
    # 格式: "贤者名": "岗位ID",
    map_pattern = r'"([^"]+)"\s*:\s*"([A-Z_]+_\d+)"'
    map_matches = re.findall(map_pattern, content)
    
    # 查找岗位ID对应的岗位名称
    # 格式: id="XXX", name="岗位名", department="部门", ...
    pos_pattern = r'id\s*=\s*"([^"]+)"\s*,\s*name\s*=\s*"([^"]+)"\s*,\s*department\s*=\s*"([^"]+)"'
    pos_matches = re.findall(pos_pattern, content)
    
    pos_map = {}
    for pos_id, name, dept in pos_matches:
        pos_map[pos_id] = {"name": name, "department": dept}
    
    # 构建贤者到岗位的映射
    for sage_name, pos_id in map_matches:
        if pos_id in pos_map:
            positions[sage_name] = {
                "position_id": pos_id,
                "position_name": pos_map[pos_id]["name"],
                "department": pos_map[pos_id]["department"],
            }
    
    logger.info(f"  解析了 {len(positions)} 个贤者-岗位映射")
    return positions


# ═══════════════════════════════════════════════════════════════════════════════
# 三、构建合并映射
# ═══════════════════════════════════════════════════════════════════════════════

def build_sage_position_mapping(sage_info: Dict, court_positions: Dict) -> Dict[str, Dict]:
    """构建完整的贤者-岗位映射"""
    logger.info("构建贤者-岗位映射...")
    
    mapping = {}
    matched = 0
    unmatched = 0
    
    for sage_name, info in sage_info.items():
        # 优先从court_positions获取
        if sage_name in court_positions:
            mapping[sage_name] = {
                **info,
                **court_positions[sage_name]
            }
            matched += 1
        else:
            # 使用默认部门
            mapping[sage_name] = {
                **info,
                "position_id": "",
                "position_name": "",
                "department": info.get("department", ""),
            }
            unmatched += 1
    
    logger.info(f"  匹配成功: {matched}, 未匹配: {unmatched}")
    return mapping


# ═══════════════════════════════════════════════════════════════════════════════
# 四、更新Claw配置
# ═══════════════════════════════════════════════════════════════════════════════

def load_claw_yaml(file_path: Path) -> Optional[Dict]:
    """加载单个Claw YAML配置"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.warning(f"  加载失败 {file_path.name}: {e}")
        return None


def update_claw_config(
    file_path: Path,
    position_info: Dict,
    sage_info: Dict
) -> bool:
    """更新单个Claw配置"""
    data = load_claw_yaml(file_path)
    if not data:
        return False
    
    # 更新岗位信息
    data["court_position"] = position_info.get("position_id", "")
    data["department"] = position_info.get("department", sage_info.get("department", ""))
    
    # 添加额外信息
    data["position_name"] = position_info.get("position_name", "")
    data["si_name"] = position_info.get("si_name", "")
    
    # 添加岗位级别
    tier_map = {
        "GRANDMASTER": "超级大师",
        "FOUNDER": "创始人",
        "MASTER": "集大成者",
        "SCHOLAR": "学者",
        "PRACTITIONER": "实践者",
    }
    data["tier_name"] = tier_map.get(sage_info.get("tier", ""), "")
    
    # 写入回文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False)
        return True
    except Exception as e:
        logger.error(f"  写入失败 {file_path.name}: {e}")
        return False


def onboard_all_claws(
    claw_dir: Path,
    sage_position_mapping: Dict,
    sage_info: Dict
) -> Dict[str, Any]:
    """执行所有Claw入职"""
    logger.info(f"开始Claw入职流程: {claw_dir}")
    
    # 获取所有YAML文件
    yaml_files = list(claw_dir.glob("*.yaml"))
    logger.info(f"  找到 {len(yaml_files)} 个Claw配置")
    
    success_count = 0
    fail_count = 0
    not_found = []
    
    for yaml_file in yaml_files:
        # 获取文件名（不含.yaml后缀）作为贤者名
        claw_name = yaml_file.stem
        
        # 尝试精确匹配
        position_info = sage_position_mapping.get(claw_name)
        info = sage_info.get(claw_name)
        
        if not position_info or not info:
            # 尝试模糊匹配
            for sage_name, pos_info in sage_position_mapping.items():
                if claw_name == sage_name or claw_name in sage_name or sage_name in claw_name:
                    position_info = pos_info
                    info = sage_info.get(sage_name)
                    break
        
        if position_info and info:
            if update_claw_config(yaml_file, position_info, info):
                success_count += 1
            else:
                fail_count += 1
        else:
            not_found.append(claw_name)
            fail_count += 1
    
    logger.info(f"  入职完成: 成功 {success_count}, 失败 {fail_count}")
    
    return {
        "total": len(yaml_files),
        "success": success_count,
        "failed": fail_count,
        "not_found": not_found,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 五、生成统计报告
# ═══════════════════════════════════════════════════════════════════════════════

def generate_report(
    sage_info: Dict,
    sage_position_mapping: Dict,
    onboarding_result: Dict
) -> Dict:
    """生成入职报告"""
    
    # 统计各部门人数
    dept_stats = {}
    for sage_name, info in sage_position_mapping.items():
        dept = info.get("department", "未知")
        dept_stats[dept] = dept_stats.get(dept, 0) + 1
    
    # 统计岗位等级
    tier_stats = {}
    for sage_name, info in sage_position_mapping.items():
        tier = info.get("tier", "未知")
        tier_stats[tier] = tier_stats.get(tier, 0) + 1
    
    # 统计有岗位的贤者
    positioned_count = sum(1 for info in sage_position_mapping.values() if info.get("position_id"))
    
    report = {
        "timestamp": "2026-04-22",
        "version": "v2.0.0",
        "summary": {
            "total_sages": len(sage_info),
            "total_claws": onboarding_result["total"],
            "onboarded_success": onboarding_result["success"],
            "onboarded_failed": onboarding_result["failed"],
            "positioned_sages": positioned_count,
        },
        "department_stats": dept_stats,
        "tier_stats": tier_stats,
        "not_found_claws": onboarding_result["not_found"][:20],
    }
    
    return report


# ═══════════════════════════════════════════════════════════════════════════════
# 六、主执行流程
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("贤者入职神之架构 - Claw岗位入职脚本 v2.0")
    logger.info("=" * 60)
    
    # 1. 解析贤者注册表
    sage_info = parse_sage_registry()
    
    # 2. 解析神之架构岗位体系
    court_positions = parse_court_positions()
    
    # 3. 构建贤者-岗位映射
    sage_position_mapping = build_sage_position_mapping(sage_info, court_positions)
    
    # 4. 执行Claw入职
    onboarding_result = onboard_all_claws(
        CLAW_CONFIGS_DIR,
        sage_position_mapping,
        sage_info
    )
    
    # 5. 生成报告
    report = generate_report(sage_info, sage_position_mapping, onboarding_result)
    
    # 保存报告
    OUTPUT_REPORT = PROJECT_ROOT / "_onboarding_claws_report.json"
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info("=" * 60)
    logger.info("入职完成！")
    logger.info(f"  总贤者: {report['summary']['total_sages']}")
    logger.info(f"  已有岗位: {report['summary']['positioned_sages']}")
    logger.info(f"  入职成功: {report['summary']['onboarded_success']}")
    logger.info(f"  入职失败: {report['summary']['onboarded_failed']}")
    logger.info(f"  报告已保存: {OUTPUT_REPORT}")
    logger.info("=" * 60)
    
    # 输出部门统计
    logger.info("\n各部门入职人数:")
    for dept, count in sorted(report["department_stats"].items(), key=lambda x: -x[1])[:10]:
        logger.info(f"  {dept}: {count}")
    
    return report


if __name__ == "__main__":
    main()