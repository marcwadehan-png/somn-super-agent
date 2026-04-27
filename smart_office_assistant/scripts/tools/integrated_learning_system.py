#!/usr/bin/env python3
"""
集成学习系统 - 整合超级学习系统与E盘学习系统
提供统一的学习界面和协调机制
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import asyncio

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

from super_learning_system import SuperLearningSystem, LearningDimension

from e_drive_learning_system import EDriveLearningSystem, LearningSession

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/learning/integrated_learning.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class IntegratedLearningSystem:
    """集成学习系统 - 整合所有学习维度和来源"""
    
    def __init__(self):
        # 初始化两个学习系统
        self.super_learning = SuperLearningSystem()
        self.e_drive_learning = EDriveLearningSystem()
        
        # 集成数据目录
        self.data_dir = Path("data/learning/integrated")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.report_file = self.data_dir / "integrated_report.json"
        self.coordination_file = self.data_dir / "coordination.json"
        
        # 学习策略
        self.strategy = self._load_strategy()
        
    def _load_strategy(self) -> Dict[str, Any]:
        """加载学习策略"""
        default_strategy = {
            'e_drive_weight': 0.4,  # E盘学习权重
            'network_weight': 0.6,  # 网络学习权重
            'dimensions': {
                LearningDimension.PROVIDER_INTELLIGENCE.value: {'priority': 'HIGH', 'target': 10},
                LearningDimension.SOLUTION_TEMPLATE.value: {'priority': 'HIGH', 'target': 10},
                LearningDimension.BUSINESS_STRATEGY.value: {'priority': 'MEDIUM', 'target': 5},
                LearningDimension.AI_TECHNOLOGY.value: {'priority': 'MEDIUM', 'target': 5},
                LearningDimension.NEURAL_MEMORY.value: {'priority': 'MEDIUM', 'target': 5},
                LearningDimension.CHART_DESIGN.value: {'priority': 'LOW', 'target': 3},
                LearningDimension.PPT_STYLE.value: {'priority': 'LOW', 'target': 3},
                LearningDimension.DATA_VISUALIZATION.value: {'priority': 'LOW', 'target': 3},
            },
            'learning_gaps': []
        }
        
        if self.coordination_file.exists():
            try:
                with open(self.coordination_file, 'r', encoding='utf-8') as f:
                    strategy = json.load(f)
                    return strategy
            except Exception as e:
                logger.error(f"加载策略失败: {e}")
        
        return default_strategy
    
    def _save_strategy(self):
        """保存学习策略"""
        try:
            with open(self.coordination_file, 'w', encoding='utf-8') as f:
                json.dump(self.strategy, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存策略失败: {e}")
    
    def analyze_learning_status(self) -> Dict[str, Any]:
        """分析学习状态"""
        # E盘学习统计
        e_drive_stats = self._analyze_e_drive_learning()
        
        # 网络学习统计
        network_stats = self._analyze_network_learning()
        
        # 维度覆盖分析
        dimension_analysis = self._analyze_dimensions()
        
        # 学习不足识别
        gaps = self._identify_gaps(e_drive_stats, network_stats, dimension_analysis)
        
        # 更新策略
        self.strategy['learning_gaps'] = gaps
        self._save_strategy()
        
        # 生成报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'e_drive_stats': e_drive_stats,
            'network_stats': network_stats,
            'dimension_analysis': dimension_analysis,
            'gaps': gaps,
            'recommendations': self._generate_recommendations(gaps)
        }
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def _analyze_e_drive_learning(self) -> Dict[str, Any]:
        """分析E盘学习状态"""
        sessions = self.e_drive_learning.sessions
        
        if not sessions:
            return {
                'total_files': 0,
                'categories': {},
                'dimensions': {},
                'confidence_avg': 0.0
            }
        
        # 类别统计
        categories = {}
        for session in sessions:
            cat = session.e_drive_category
            categories[cat] = categories.get(cat, 0) + 1
        
        # 维度统计
        dimensions = {}
        total_confidence = 0
        for session in sessions:
            dim = session.dimension
            dimensions[dim] = dimensions.get(dim, 0) + 1
            total_confidence += session.confidence_score
        
        return {
            'total_files': len(sessions),
            'categories': categories,
            'dimensions': dimensions,
            'confidence_avg': total_confidence / len(sessions)
        }
    
    def _analyze_network_learning(self) -> Dict[str, Any]:
        """分析网络学习状态"""
        sessions = self.super_learning.sessions
        
        if not sessions:
            return {
                'total_sessions': 0,
                'dimensions': {},
                'confidence_avg': 0.0
            }
        
        # 维度统计
        dimensions = {}
        total_confidence = 0
        for session in sessions:
            dim = session.dimension
            dimensions[dim] = dimensions.get(dim, 0) + 1
            total_confidence += session.confidence_score
        
        return {
            'total_sessions': len(sessions),
            'dimensions': dimensions,
            'confidence_avg': total_confidence / len(sessions)
        }
    
    def _analyze_dimensions(self) -> Dict[str, Any]:
        """分析维度覆盖情况"""
        # 合并两个系统的维度学习情况
        all_dimensions = {}
        
        # E盘维度
        for session in self.e_drive_learning.sessions:
            dim = session.dimension
            all_dimensions[dim] = all_dimensions.get(dim, 0) + 1
        
        # 网络学习维度
        for session in self.super_learning.sessions:
            dim = session.dimension
            all_dimensions[dim] = all_dimensions.get(dim, 0) + 1
        
        # 分析每个维度的状态
        dimension_status = {}
        for dim in LearningDimension:
            dim_name = dim.value
            learned_count = all_dimensions.get(dim_name, 0)
            target = self.strategy['dimensions'].get(dim_name, {}).get('target', 5)
            priority = self.strategy['dimensions'].get(dim_name, {}).get('priority', 'MEDIUM')
            
            status = 'OK'
            if learned_count == 0:
                status = 'NOT_STARTED'
            elif learned_count < target * 0.5:
                status = 'LOW'
            elif learned_count < target:
                status = 'MEDIUM'
            
            dimension_status[dim_name] = {
                'learned_count': learned_count,
                'target': target,
                'priority': priority,
                'status': status,
                'progress': min(100, (learned_count / target) * 100) if target > 0 else 100
            }
        
        return dimension_status
    
    def _identify_gaps(self, e_drive_stats: Dict, network_stats: Dict, 
                       dimension_analysis: Dict) -> list:
        """识别学习不足"""
        gaps = []
        
        # 维度学习不足
        for dim_name, status in dimension_analysis.items():
            if status['status'] == 'NOT_STARTED':
                gaps.append({
                    'type': 'DIMENSION_NOT_STARTED',
                    'dimension': dim_name,
                    'priority': 'HIGH',
                    'description': f"{dim_name}维度尚未开始学习",
                    'recommendation': f"立即启动{dim_name}维度学习"
                })
            elif status['status'] == 'LOW':
                gaps.append({
                    'type': 'DIMENSION_LOW',
                    'dimension': dim_name,
                    'priority': 'MEDIUM',
                    'description': f"{dim_name}维度学习进度较低 ({status['learned_count']}/{status['target']})",
                    'recommendation': f"增加{dim_name}维度的学习频次"
                })
        
        # E盘类别缺失
        e_drive_categories = set(e_drive_stats.get('categories', {}).keys())
        expected_categories = {'PMP项目管理', '保险知识', '简历与职业', 'Abyss AI知识库'}
        missing_categories = expected_categories - e_drive_categories
        
        for cat in missing_categories:
            gaps.append({
                'type': 'CATEGORY_MISSING',
                'category': cat,
                'priority': 'HIGH',
                'description': f"{cat}类别尚未开始学习",
                'recommendation': f"检查E盘{cat}目录并启动学习"
            })
        
        # 网络学习不足
        network_count = network_stats.get('total_sessions', 0)
        if network_count < 50:
            gaps.append({
                'type': 'NETWORK_LEARNING_LOW',
                'priority': 'MEDIUM',
                'description': f"网络学习会话数较少 ({network_count})",
                'recommendation': "增加网络学习频次，获取最新行业知识"
            })
        
        return gaps
    
    def _generate_recommendations(self, gaps: list) -> list:
        """生成优化建议"""
        recommendations = []
        
        # 按优先级排序
        high_priority = [g for g in gaps if g['priority'] == 'HIGH']
        medium_priority = [g for g in gaps if g['priority'] == 'MEDIUM']
        
        # 高优先级建议
        for gap in high_priority:
            if gap['type'] == 'DIMENSION_NOT_STARTED':
                recommendations.append({
                    'priority': 'HIGH',
                    'area': '维度学习',
                    'issue': gap['description'],
                    'action': gap['recommendation'],
                    'expected_impact': '完善知识体系覆盖'
                })
            elif gap['type'] == 'CATEGORY_MISSING':
                recommendations.append({
                    'priority': 'HIGH',
                    'area': 'E盘学习',
                    'issue': gap['description'],
                    'action': gap['recommendation'],
                    'expected_impact': '确保E盘所有资料被充分学习'
                })
        
        # 中优先级建议
        for gap in medium_priority:
            if gap['type'] == 'DIMENSION_LOW':
                recommendations.append({
                    'priority': 'MEDIUM',
                    'area': '维度学习',
                    'issue': gap['description'],
                    'action': gap['recommendation'],
                    'expected_impact': '提升特定维度的知识深度'
                })
            elif gap['type'] == 'NETWORK_LEARNING_LOW':
                recommendations.append({
                    'priority': 'MEDIUM',
                    'area': '网络学习',
                    'issue': gap['description'],
                    'action': "增加网络学习频次至每日至少10次",
                    'expected_impact': '获取最新行业趋势和技术动态'
                })
        
        # 系统级建议
        e_drive_stats = self._analyze_e_drive_learning()
        network_stats = self._analyze_network_learning()
        
        if e_drive_stats.get('confidence_avg', 0) < 0.7:
            recommendations.append({
                'priority': 'HIGH',
                'area': '学习质量',
                'issue': f"E盘学习平均置信度较低: {e_drive_stats.get('confidence_avg', 0):.2f}",
                'action': "优化知识提取算法，提高学习准确性",
                'expected_impact': '提升学习质量和可靠性'
            })
        
        if network_stats.get('confidence_avg', 0) < 0.7:
            recommendations.append({
                'priority': 'HIGH',
                'area': '学习质量',
                'issue': f"网络学习平均置信度较低: {network_stats.get('confidence_avg', 0):.2f}",
                'action': "引入更先进的RAG技术，提高网络知识提取质量",
                'expected_impact': '确保学习到的知识准确可靠'
            })
        
        return recommendations
    
    def start_coordinated_learning(self, max_files: Optional[int] = None):
        """启动协调学习"""
        logger.info("=" * 60)
        logger.info("集成学习系统启动 - 协调E盘与网络学习")
        logger.info("=" * 60)
        
        # 1. 先完成E盘学习
        logger.info("\n[步骤 1] 启动E盘深度学习...")
        self.e_drive_learning.start_learning(max_files=max_files, interval_seconds=2)
        
        # 2. 生成分析报告
        logger.info("\n[步骤 2] 分析学习状态...")
        report = self.analyze_learning_status()
        
        # 3. 打印报告摘要
        self._print_report_summary(report)
        
        # 4. 启动网络学习（补充维度）
        logger.info("\n[步骤 3] 启动网络学习，补充维度覆盖...")
        self.super_learning.start_learning(interval_seconds=2)
        
        logger.info("\n" + "=" * 60)
        logger.info("协调学习完成")
        logger.info("=" * 60)
    
    def _print_report_summary(self, report: Dict[str, Any]):
        """打印报告摘要"""
        logger.info("\n" + "=" * 60)
        logger.info("学习分析报告")
        logger.info("=" * 60)
        
        # E盘统计
        e_stats = report['e_drive_stats']
        logger.info(f"\n【E盘学习统计】")
        logger.info(f"  总学习文件数: {e_stats['total_files']}")
        logger.info(f"  平均置信度: {e_stats['confidence_avg']:.2f}")
        logger.info(f"  类别覆盖:")
        for cat, count in e_stats.get('categories', {}).items():
            logger.info(f"    - {cat}: {count}")
        
        # 网络学习统计
        n_stats = report['network_stats']
        logger.info(f"\n【网络学习统计】")
        logger.info(f"  总学习会话数: {n_stats['total_sessions']}")
        logger.info(f"  平均置信度: {n_stats['confidence_avg']:.2f}")
        
        # 维度分析
        logger.info(f"\n【维度覆盖分析】")
        dim_analysis = report['dimension_analysis']
        for dim_name, status in sorted(dim_analysis.items()):
            if status['status'] != 'OK':
                logger.info(f"  [{status['priority']}] {dim_name}: {status['learned_count']}/{status['target']} ({status['progress']:.0f}%)")
        
        # 学习不足
        logger.info(f"\n【学习不足】")
        gaps = report['gaps']
        logger.info(f"  发现 {len(gaps)} 个学习不足")
        for gap in gaps[:5]:  # 只显示前5个
            logger.info(f"  [{gap['priority']}] {gap['description']}")
        
        # 优化建议
        logger.info(f"\n【优化建议】")
        recommendations = report['recommendations']
        logger.info(f"  提出 {len(recommendations)} 条建议")
        for rec in recommendations[:5]:  # 只显示前5个
            logger.info(f"  [{rec['priority']}] {rec['action']}")
        
        logger.info("=" * 60)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='集成学习系统')
    parser.add_argument('--analyze-only', action='store_true',
                       help='仅分析学习状态，不执行学习')
    parser.add_argument('--max-files', type=int, default=None,
                       help='最大E盘学习文件数')
    
    args = parser.parse_args()
    
    # 创建集成系统
    system = IntegratedLearningSystem()
    
    if args.analyze_only:
        # 仅分析
        report = system.analyze_learning_status()
        system._print_report_summary(report)
    else:
        # 启动协调学习
        system.start_coordinated_learning(max_files=args.max_files)


if __name__ == '__main__':
    main()
