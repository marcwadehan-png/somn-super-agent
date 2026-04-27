"""
__all__ = [
    'execute_full_cycle',
    'execute_learning',
    'plan_learning',
    'run_integrated_learning',
]

集成式学习执行器 - Integrated Learning Executor
将学习调度器和学习引擎整合,实现本地优先,网络补充的完整流程

使用场景:
1. 每日自动学习任务调用此执行器
2. 手动学习请求时调用此执行器
3. 支持strategy动态调整

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  兼容层说明（v2.0 统一重构后）
本文件保留原始实现以确保现有调用链 100% 兼容。
新代码请使用：
    from .unified_learning_orchestrator import UnifiedLearningOrchestrator
    orchestrator = UnifiedLearningOrchestrator()
    result = orchestrator.plan_and_execute()
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import yaml
import logging
from pathlib import Path
from src.core.paths import LEARNING_DIR, PROJECT_ROOT
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

# 导入学习相关模块
from .learning_scheduler import LearningScheduler, LearningStrategy
from .learning_engine import LearningEngine, LearningType

@dataclass
class IntegratedLearningPlan:
    """集成学习计划"""
    plan_id: str
    strategy: str
    execution_phase: str
    data_selection: Dict
    learning_config: Dict
    expected_outcomes: List[str]
    timestamp: str

class IntegratedLearningExecutor:
    """集成学习执行器"""
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = str(PROJECT_ROOT)
        self.base_path = Path(base_path)
        self.scheduler = LearningScheduler(base_path)
        self.learning_engine = LearningEngine(base_path)
        
        # 执行日志
        self.execution_log = []
        self.plans_history = []
    
    def plan_learning(self) -> IntegratedLearningPlan:
        """
        规划学习过程
        
        步骤:
        1. 扫描数据源
        2. 根据strategy选择数据
        3. generate学习计划
        """
        plan_id = f"ILP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info("\n" + "="*60)
        logger.info("📋 学习规划阶段")
        logger.info("="*60)
        
        # 规划数据选择
        logger.info("\n[1/3] 规划数据选择...")
        data_selection = self.scheduler.plan_learning_data_selection()
        
        self._print_data_selection(data_selection)
        
        # generate学习配置
        logger.info("\n[2/3] generate学习配置...")
        learning_config = self._generate_learning_config(data_selection)
        
        # generate学习计划
        logger.info("\n[3/3] generate学习计划...")
        plan = IntegratedLearningPlan(
            plan_id=plan_id,
            strategy=data_selection['strategy'],
            execution_phase="规划完成",
            data_selection=data_selection,
            learning_config=learning_config,
            expected_outcomes=self._generate_expected_outcomes(
                len(data_selection['local_data']),
                len(data_selection['network_data'])
            ),
            timestamp=datetime.now().isoformat()
        )
        
        self.plans_history.append(plan)
        
        logger.info(f"\n✅ 学习规划完成")
        logger.info(f"   计划ID: {plan_id}")
        logger.info(f"   strategy: {plan.strategy}")
        logger.info(f"   总数据量: {data_selection['total_data']}")
        
        return plan
    
    def execute_learning(self, plan: IntegratedLearningPlan) -> Dict:
        """
        执行学习计划
        
        步骤:
        1. 加载数据
        2. 执行学习
        3. generate报告
        """
        logger.info("\n" + "="*60)
        logger.info("🚀 学习执行阶段")
        logger.info("="*60)
        
        execution_id = f"EXE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()
        
        # 合并本地和网络数据
        logger.info("\n[1/3] 加载学习数据...")
        all_data = plan.data_selection['local_data'] + plan.data_selection['network_data']
        logger.info(f"   ✅ 已加载 {len(all_data)} 条数据")
        logger.info(f"      - 本地数据: {len(plan.data_selection['local_data'])} 条")
        logger.info(f"      - 网络数据: {len(plan.data_selection['network_data'])} 条")
        
        # 执行学习
        logger.info("\n[2/3] 执行学习流程...")
        learning_results = self._execute_learning_stages(all_data)
        
        # generate报告
        logger.info("\n[3/3] generate学习报告...")
        report = self._generate_execution_report(
            execution_id=execution_id,
            plan=plan,
            learning_results=learning_results,
            start_time=start_time
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info(f"\n✅ 学习执行完成")
        logger.info(f"   执行ID: {execution_id}")
        logger.info(f"   耗时: {duration:.2f}秒")
        logger.info(f"   学习事件: {report['learning_events_count']}")
        logger.info(f"   知识更新: {report['knowledge_updates_count']}")
        
        return report
    
    def execute_full_cycle(self) -> Dict:
        """
        执行完整学习周期:规划 -> 执行
        """
        logger.info("\n" + "="*60)
        logger.info("🎯 开始完整学习周期")
        logger.info("="*60)
        
        # 规划阶段
        plan = self.plan_learning()
        
        # 执行阶段
        report = self.execute_learning(plan)
        
        # 总结
        summary = {
            'plan': asdict(plan) if plan else None,
            'report': report,
            'total_duration': (datetime.now() - datetime.fromisoformat(plan.timestamp)).total_seconds() if plan else 0,
            'success': report['status'] == '成功'
        }
        
        self._print_summary(summary)
        
        return summary
    
    def _generate_learning_config(self, data_selection: Dict) -> Dict:
        """generate学习配置"""
        return {
            '数据源': data_selection['data_source_breakdown'],
            '学习strategy': data_selection['strategy'],
            '建议': data_selection['recommendations'],
            '数据质量': self._assess_data_quality(data_selection),
            '学习参数': {
                '最小样本': 5,
                '置信度阈值': 0.7,
                '模式recognize阈值': 0.6
            }
        }
    
    def _assess_data_quality(self, data_selection: Dict) -> Dict:
        """评估数据质量"""
        local_data_count = data_selection['data_source_breakdown']['本地数据']
        network_data_count = data_selection['data_source_breakdown']['网络数据']
        total = data_selection['total_data']
        
        # 计算数据质量评分
        if total == 0:
            quality_score = 0
        elif local_data_count >= 5 and network_data_count == 0:
            quality_score = 0.95  # 本地数据充足,高质量
        elif local_data_count >= 3:
            quality_score = 0.85  # 本地数据较好
        else:
            quality_score = 0.6   # 依赖网络数据
        
        return {
            '总体评分': f"{quality_score:.1%}",
            '本地数据占比': f"{local_data_count/max(total,1)*100:.1f}%",
            '数据多样性': '高' if network_data_count > 0 else '中' if local_data_count > 3 else '低'
        }
    
    def _execute_learning_stages(self, data: List[Dict]) -> Dict:
        """执行各学习阶段（接入真实 LearningEngine）"""
        results = {
            '实例学习': {'事件数': 0, '模式数': 0},
            '验证学习': {'事件数': 0, '更新数': 0},
            '错误学习': {'事件数': 0, '发现数': 0},
            '关联学习': {'事件数': 0, '关联数': 0},
            '总体': {'学习事件': 0, '知识更新': 0, '错误': 0}
        }
        
        if len(data) < 5:
            logger.warning("   ℹ️ 数据不足,跳过深度学习(需要≥5条)")
            return results
        
        try:
            # 实例学习：从数据中提取模式
            logger.info("   ▸ 执行实例学习...")
            pattern, event = self.learning_engine.learn_from_instance(data, "综合模式")
            if event:
                results['实例学习']['事件数'] = 1
                results['实例学习']['模式数'] = 1
                self.learning_engine.save_learning_event(event)
            
            # 验证学习：对有置信度标记的数据做贝叶斯更新
            logger.info("   ▸ 执行验证学习...")
            validated_count = 0
            for item in data[:10]:
                if isinstance(item, dict) and item.get('置信度'):
                    v_event = self.learning_engine.learn_from_validation(
                        hypothesis_id=item.get('id', 'unknown'),
                        validation_result={
                            'passed': item.get('通过', item.get('置信度', 0) > 0.7),
                            'sample_size': item.get('样本量', 10),
                            'effect_size': item.get('效应量', 0.5),
                            'p_value': item.get('p值', 0.05),
                            'original_confidence': item.get('置信度', 0.5)
                        }
                    )
                    if v_event:
                        validated_count += 1
                        self.learning_engine.save_learning_event(v_event)
            results['验证学习']['事件数'] = validated_count
            results['验证学习']['更新数'] = validated_count
            
            # 错误学习：识别标记为错误的数据
            logger.error("   ▸ 执行错误学习...")
            error_count = 0
            for item in data[:5]:
                if isinstance(item, dict) and (item.get('error') or item.get('失败') or item.get('错误原因')):
                    e_event = self.learning_engine.learn_from_error({
                        'hypothesis': item.get('假设', str(item.get('_source', ''))),
                        'actual_result': item.get('实际结果', ''),
                        'error_reason': item.get('错误原因', item.get('error', '未知'))
                    })
                    if e_event:
                        error_count += 1
                        self.learning_engine.save_learning_event(e_event)
            results['错误学习']['事件数'] = error_count
            results['错误学习']['发现数'] = error_count
            
            # 关联学习：从数据中提取概念关联
            logger.info("   ▸ 执行关联学习...")
            assoc_count = 0
            tags_set = set()
            for item in data:
                if isinstance(item, dict):
                    t = item.get('标签', item.get('tags', item.get('类型', '')))
                    if t:
                        tags_set.add(str(t))
            tags_list = list(tags_set)
            for i in range(min(len(tags_list) - 1, 3)):
                a_event = self.learning_engine.learn_from_association(
                    tags_list[i], tags_list[i+1],
                    [{'co_occurred': True, 'correlation': 0.6}]
                )
                if a_event:
                    assoc_count += 1
            results['关联学习']['事件数'] = assoc_count
            results['关联学习']['关联数'] = assoc_count
            
            # 统计总体
            results['总体']['学习事件'] = sum(
                r['事件数'] for k, r in results.items() if k != '总体'
            )
            results['总体']['知识更新'] = (
                results['实例学习']['模式数'] +
                results['验证学习']['更新数'] +
                results['关联学习']['关联数']
            )
            results['总体']['错误'] = results['错误学习']['发现数']
            
        except Exception as e:
            logger.warning(f"   ⚠️ 学习执行异常: {e}")
            results['总体']['错误'] = '学习失败'
        
        return results
    
    def _generate_expected_outcomes(self, local_count: int, network_count: int) -> List[str]:
        """generate预期成果"""
        outcomes = []
        
        if local_count >= 5:
            outcomes.append("✅ 完整的实例学习流程")
            outcomes.append("✅ 新模式提取")
            outcomes.append("✅ 关联学习")
        elif local_count >= 3:
            outcomes.append("⚠️ 受限的学习流程")
            outcomes.append("✅ 关联学习")
        else:
            outcomes.append("ℹ️ 补充性网络学习")
        
        if network_count > 0:
            outcomes.append("🌐 网络知识补充")
        
        return outcomes
    
    def _generate_execution_report(self, execution_id: str, plan: IntegratedLearningPlan,
                                  learning_results: Dict, start_time: datetime) -> Dict:
        """generate执行报告"""
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        total_events = learning_results['总体']['学习事件']
        total_updates = learning_results['总体']['知识更新']
        has_error = bool(learning_results['总体'].get('错误')) and learning_results['总体'].get('错误') != 0
        
        return {
            '执行ID': execution_id,
            '计划ID': plan.plan_id,
            'strategy': plan.strategy,
            '执行时间': datetime.now().isoformat(),
            '耗时(秒)': duration,
            '数据统计': {
                '本地数据': len(plan.data_selection['local_data']),
                '网络数据': len(plan.data_selection['network_data']),
                '总计': plan.data_selection['total_data']
            },
            '学习成果': learning_results,
            'learning_events_count': total_events,
            'knowledge_updates_count': total_updates,
            '状态': '失败' if has_error else ('成功' if total_events > 0 else '无数据'),
            '建议': plan.data_selection['recommendations']
        }
    
    def _print_data_selection(self, data_selection: Dict):
        """打印数据选择信息"""
        logger.info(f"\n   strategy: {data_selection['strategy']}")
        
        breakdown = data_selection['data_source_breakdown']
        logger.info(f"\n   数据源分布:")
        logger.info(f"   ├─ 本地数据: {breakdown['本地数据']} 条")
        logger.info(f"   ├─ 网络数据: {breakdown['网络数据']} 条")
        logger.info(f"   ├─ 总计: {breakdown['总计']} 条")
        logger.info(f"   └─ 本地占比: {breakdown['本地占比']}")
        
        if data_selection.get('data_sources_info'):
            logger.info(f"\n   数据源详情:")
            for info in data_selection['data_sources_info']:
                logger.info(f"{info['数据源']}: {info['数据条数']}条 | "
                            f"质量{info['质量评分']} | {info['最近数据']} | {info['优先级']}")
        
        if data_selection.get('recommendations'):
            logger.info(f"\n   学习建议:")
            for i, rec in enumerate(data_selection['recommendations'], 1):
                logger.info(f"   {i}. {rec}")
    
    def _print_summary(self, summary: Dict):
        """打印执行摘要"""
        logger.info("\n" + "="*60)
        logger.info("📊 学习周期总结")
        logger.info("="*60)
        
        if summary['plan']:
            logger.info(f"\n规划阶段:")
            logger.info(f"  计划ID: {summary['plan']['plan_id']}")
            logger.info(f"  strategy: {summary['plan']['strategy']}")
            logger.info(f"  预期成果: {len(summary['plan']['expected_outcomes'])} 项")
        
        report = summary['report']
        logger.info(f"\n执行阶段:")
        logger.info(f"  执行ID: {report['执行ID']}")
        logger.info(f"  耗时: {report['耗时(秒)']:.2f}秒")
        logger.info(f"  学习事件: {report['learning_events_count']}")
        logger.info(f"  知识更新: {report['knowledge_updates_count']}")
        logger.info(f"  状态: {report['状态']}")
        
        logger.info(f"\n数据统计:")
        stats = report['数据统计']
        logger.info(f"  本地: {stats['本地数据']} | 网络: {stats['网络数据']} | 总计: {stats['总计']}")
        
        logger.info("\n" + "="*60 + "\n")

# 辅助函数:快速启动集成学习
def run_integrated_learning():
    """
    快速启动集成学习流程。
    内部优先调用 UnifiedLearningOrchestrator，不可用时回退到原始执行器。
    """
    try:
        from .unified_learning_orchestrator import run_integrated_learning as _new
        return _new()
    except Exception:
        executor = IntegratedLearningExecutor()
        return executor.execute_full_cycle()

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
