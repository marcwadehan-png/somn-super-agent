"""
__all__ = [
    'generate_detailed_report',
    'run_daily_learning',
    'run_daily_learning_v2',
    'update_neural_memory',
]

解决方案每日学习 - 自动化脚本
与神经记忆系统集成,实现持续学习积累

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  兼容层说明（v2.0 统一重构后）
本文件保留原始实现以确保现有调用链 100% 兼容。
新代码请使用：
    from .unified_learning_orchestrator import UnifiedLearningOrchestrator
    from .learning_strategies import LearningStrategyType
    orchestrator = UnifiedLearningOrchestrator()
    report = orchestrator.execute_daily(strategy_types=[LearningStrategyType.SOLUTION])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
import logging
from pathlib import Path

import yaml
from datetime import datetime

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from path_bootstrap import bootstrap_project_paths

PROJECT_ROOT = bootstrap_project_paths(__file__, change_cwd=True)

from src.core.paths import SOLUTION_LEARNING_DIR, DAILY_MEMORY_DIR, DATA_DIR
from growth_engine import solution_learning_engine, daily_learning_executor

def run_daily_learning():
    """执行每日学习"""
    logger.info("Somn 解决方案智能学习系统")
    logger.info("=" * 60)
    logger.info(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    try:
        # 执行每日学习
        report = daily_learning_executor.execute_daily_learning()

        # generate详细报告
        generate_detailed_report(report)

        # 更新神经记忆
        update_neural_memory(report)

        logger.info("每日学习完成!")
        return 0

    except Exception as e:
        logger.error(f"学习过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

def generate_detailed_report(report: dict):
    """generate详细学习报告"""
    
    # 创建报告目录
    report_dir = Path(SOLUTION_LEARNING_DIR / 'reports')
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # generate文件名
    date_str = datetime.now().strftime('%Y%m%d')
    report_file = report_dir / f"daily_report_{date_str}.yaml"
    
    # 添加报告元数据
    report['report_metadata'] = {
        'generated_at': datetime.now().isoformat(),
        'report_type': 'daily_learning',
        'system_version': 'v2.2.0',
        'engine': 'SolutionLearningEngine'
    }
    
    # 保存报告
    with open(report_file, 'w', encoding='utf-8') as f:
        yaml.dump(report, f, allow_unicode=True, default_flow_style=False)
    
    logger.info(f"详细报告已保存: {report_file}")

def update_neural_memory(report: dict):
    """更新神经记忆系统"""
    
    # 准备记忆数据
    memory_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': 'solution_learning',
        'summary': {
            'categories': report.get('categories_processed', []),
            'sessions': report.get('sessions_created', 0) if isinstance(report.get('sessions_created'), int) else len(report.get('sessions_created', [])),
            'insights': report.get('insights_generated', 0) if isinstance(report.get('insights_generated'), int) else len(report.get('insights_generated', [])),
            'templates': report.get('templates_updated', 0) if isinstance(report.get('templates_updated'), int) else len(report.get('templates_updated', []))
        },
        'learning_summary': report.get('learning_summary', {})
    }
    
    # 追加到每日记忆日志
    # [v2.0 独立运行版] 使用项目内部 data/daily_memory/ 替代 .workbuddy/memory/
    memory_dir = DAILY_MEMORY_DIR
    memory_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    memory_file = memory_dir / f"{date_str}.md"
    
    # 读取现有内容
    existing_content = ""
    if memory_file.exists():
        with open(memory_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # 添加新的学习记录
    learning_log = f"""

## 解决方案智能学习 ({datetime.now().strftime('%H:%M')})

**学习范围**: {', '.join(report.get('categories_processed', []))}
**学习成果**:
- 学习会话: {report.get('sessions_created', 0) if isinstance(report.get('sessions_created'), int) else len(report.get('sessions_created', []))} 个
- generate洞察: {report.get('insights_generated', 0) if isinstance(report.get('insights_generated'), int) else len(report.get('insights_generated', []))} 个
- 更新模板: {report.get('templates_updated', 0) if isinstance(report.get('templates_updated'), int) else len(report.get('templates_updated', []))} 个

**学习摘要**:
{yaml.dump(report.get('learning_summary', {}), allow_unicode=True, default_flow_style=False)}

"""
    
    # 写入文件
    with open(memory_file, 'a', encoding='utf-8') as f:
        f.write(learning_log)
    
    logger.info(f"神经记忆已更新: {memory_file}")

def run_daily_learning_v2():
    """
    新路由入口（推荐）：通过 UnifiedLearningOrchestrator 执行解决方案每日学习。
    保留 run_daily_learning() 原有接口不变。
    """
    try:
        from .unified_learning_orchestrator import UnifiedLearningOrchestrator
        from .learning_strategies import LearningStrategyType
        orchestrator = UnifiedLearningOrchestrator()
        report = orchestrator.execute_daily(strategy_types=[LearningStrategyType.SOLUTION])
        return 0 if report else 1
    except Exception as e:
        logger.warning(f"v2路由失败，回退到原始执行器: {e}")
        return run_daily_learning()

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
