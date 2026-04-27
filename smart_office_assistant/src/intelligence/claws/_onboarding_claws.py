# -*- coding: utf-8 -*-
"""
贤者入职神之架构 - Claw岗位入职脚本
=====================================

功能：
1. 读取贤者注册表，获取每个贤者的部门信息
2. 从神之架构岗位体系获取对应的岗位ID
3. 更新776个Claw YAML配置，填充court_position和department字段

执行方式：
    python _onboarding_claws.py

版本: v1.0.0
创建: 2026-04-22
"""

import sys
import json
import yaml
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple, List, Any
from dataclasses import asdict

# 设置项目路径 - 基于脚本位置动态定位
PROJECT_ROOT = Path(__file__).resolve().parents[4]
SRC_ROOT = PROJECT_ROOT / "smart_office_assistant" / "src" / "intelligence"

# 添加路径以便导入模块 - 添加到smart_office_assistant层级
sys.path.insert(0, str(PROJECT_ROOT / "smart_office_assistant" / "src"))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# 一、路径配置
# ═══════════════════════════════════════════════════════════════════════════════

CLAW_CONFIGS_DIR = SRC_ROOT / "claws" / "configs"
COURT_POSITIONS_MODULE = SRC_ROOT / "engines" / "cloning" / "_court_positions.py"
SAGE_REGISTRY_MODULE = SRC_ROOT / "engines" / "cloning" / "_sage_registry_full.py"

# 输出报告
OUTPUT_REPORT = PROJECT_ROOT / "_onboarding_claws_report.json"


# ═══════════════════════════════════════════════════════════════════════════════
# 二、加载数据
# ═══════════════════════════════════════════════════════════════════════════════

def load_sage_registry() -> Dict[str, Any]:
    """加载贤者注册表"""
    logger.info("加载贤者注册表...")
    
    # 动态导入 - 使用正确的包名 intelligence.engines.cloning
    from intelligence.engines.cloning._sage_registry_full import ALL_SAGES, SAGE_BY_NAME
    from intelligence.engines.cloning._sage_registry_extra import EXTRA_SAGES
    
    # 构建名称到信息的映射
    sage_info = {}
    
    # 主注册表
    for school, sages in ALL_SAGES.items():
        for sage in sages:
            sage_info[sage.name] = {
                "name": sage.name,
                "name_en": sage.name_en,
                "school": sage.school,
                "tier": sage.tier.value,
                "era": sage.era,
                "department": sage.department,
                "expertise": sage.expertise,
            }
    
    # 补充注册表
    for school, sages in EXTRA_SAGES.items():
        for sage in sages:
            if sage.name not in sage_info:
                sage_info[sage.name] = {
                    "name": sage.name,
                    "name_en": sage.name_en,
                    "school": sage.school,
                    "tier": sage.tier.value,
                    "era": sage.era,
                    "department": sage.department,
                    "expertise": sage.expertise,
                }
    
    logger.info(f"  加载了 {len(sage_info)} 位贤者")
    return sage_info


def load_court_positions() -> Dict[str, Any]:
    """加载神之架构岗位体系"""
    logger.info("加载神之架构岗位体系...")
    
    # 动态导入
    from intelligence.engines.cloning._court_positions import CourtPositionRegistry, get_sage_court_position
    
    # 创建注册表实例
    registry = CourtPositionRegistry()
    
    # 获取所有岗位
    all_positions = {}
    for pos_id, pos in registry._positions.items():
        all_positions[pos_id] = {
            "id": pos.id,
            "name": pos.name,
            "department": pos.department,
            "pin": pos.pin.value,
            "pin_name": pos.display_rank,
            "nobility": pos.nobility.value if pos.nobility else 99,
            "domain": pos.domain,
            "si_name": pos.si_name,
        }
    
    logger.info(f"  加载了 {len(all_positions)} 个岗位")
    return {"registry": registry, "positions": all_positions}


def get_sage_position_mapping(sage_info: Dict, court_data: Dict) -> Dict[str, Dict]:
    """构建贤者到岗位的映射"""
    logger.info("构建贤者-岗位映射...")
    
    registry = court_data["registry"]
    positions = court_data["positions"]
    
    mapping = {}
    matched = 0
    unmatched = 0
    
    for sage_name, info in sage_info.items():
        # 尝试获取岗位
        result = registry.get_sage_position(sage_name)
        
        if result:
            pos_id, pos = result
            mapping[sage_name] = {
                "sage_name": sage_name,
                "position_id": pos_id,
                "position_name": pos.name,
                "department": pos.department,
                "pin_name": pos.display_rank,
                "nobility": pos.nobility.value if pos.nobility else None,
                "domain": pos.domain,
                "si_name": pos.si_name,
            }
            matched += 1
        else:
            # 使用默认部门（从sage_info中的department）
            mapping[sage_name] = {
                "sage_name": sage_name,
                "position_id": "",
                "position_name": "",
                "department": info.get("department", ""),
                "pin_name": "",
                "nobility": None,
                "domain": "",
                "si_name": "",
            }
            unmatched += 1
    
    logger.info(f"  匹配成功: {matched}, 未匹配: {unmatched}")
    return mapping


# ═══════════════════════════════════════════════════════════════════════════════
# 三、更新Claw配置
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
    sage_name: str,
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
    data["pin_name"] = position_info.get("pin_name", "")
    data["si_name"] = position_info.get("si_name", "")
    
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
            # 尝试模糊匹配（处理名称变体）
            for sage_name, pos_info in sage_position_mapping.items():
                if claw_name in sage_name or sage_name in claw_name:
                    position_info = pos_info
                    info = sage_info.get(sage_name)
                    break
        
        if position_info and info:
            if update_claw_config(yaml_file, claw_name, position_info, info):
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
# 四、生成统计报告
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
    pin_stats = {}
    for sage_name, info in sage_position_mapping.items():
        pin = info.get("pin_name", "未任命")
        pin_stats[pin] = pin_stats.get(pin, 0) + 1
    
    # 统计爵位
    nobility_stats = {}
    for sage_name, info in sage_position_mapping.items():
        noble = info.get("nobility")
        if noble is None:
            key = "无爵位"
        elif noble == 0:
            key = "王爵"
        elif noble == 1:
            key = "公爵"
        elif noble == 2:
            key = "侯爵"
        elif noble == 3:
            key = "伯爵"
        else:
            key = "无"
        nobility_stats[key] = nobility_stats.get(key, 0) + 1
    
    report = {
        "timestamp": "2026-04-22",
        "version": "v1.0.0",
        "summary": {
            "total_sages": len(sage_info),
            "total_claws": onboarding_result["total"],
            "onboarded_success": onboarding_result["success"],
            "onboarded_failed": onboarding_result["failed"],
        },
        "department_stats": dept_stats,
        "pin_stats": pin_stats,
        "nobility_stats": nobility_stats,
        "not_found_claws": onboarding_result["not_found"][:20],  # 只保留前20个
    }
    
    return report


# ═══════════════════════════════════════════════════════════════════════════════
# 五、主执行流程
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("贤者入职神之架构 - Claw岗位入职脚本")
    logger.info("=" * 60)
    
    # 1. 加载贤者注册表
    sage_info = load_sage_registry()
    
    # 2. 加载神之架构岗位体系
    court_data = load_court_positions()
    
    # 3. 构建贤者-岗位映射
    sage_position_mapping = get_sage_position_mapping(sage_info, court_data)
    
    # 4. 执行Claw入职
    onboarding_result = onboard_all_claws(
        CLAW_CONFIGS_DIR,
        sage_position_mapping,
        sage_info
    )
    
    # 5. 生成报告
    report = generate_report(sage_info, sage_position_mapping, onboarding_result)
    
    # 保存报告
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    logger.info("=" * 60)
    logger.info("入职完成！")
    logger.info(f"  总贤者: {report['summary']['total_sages']}")
    logger.info(f"  入职成功: {report['summary']['onboarded_success']}")
    logger.info(f"  入职失败: {report['summary']['onboarded_failed']}")
    logger.info(f"  报告已保存: {OUTPUT_REPORT}")
    logger.info("=" * 60)
    
    return report


if __name__ == "__main__":
    main()