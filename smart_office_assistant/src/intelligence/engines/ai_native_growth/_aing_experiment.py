# -*- coding: utf-8 -*-
"""增长实验框架 - GrowthExperimentFramework类

__all__ = [
    'analyze_experiment',
    'complete_experiment',
    'create_experiment',
    'get_experiment_summary',
    'record_experiment_data',
    'start_experiment',
]

提供增长实验的创建、运行和分析功能
"""

import logging
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

from ._aing_enums import GrowthExperiment, GrowthStrategy
from ._aing_stats import StatisticalEngine

logger = logging.getLogger(__name__)

class GrowthExperimentFramework:
    """增长实验框架"""
    
    def __init__(self):
        self.experiments: Dict[str, GrowthExperiment] = {}
        self.experiment_history: List[Dict] = []
        self.statistical_engine = StatisticalEngine()
    
    def create_experiment(
        self,
        name: str,
        hypothesis: str,
        control: GrowthStrategy,
        treatments: List[GrowthStrategy],
        success_criteria: Dict,
        duration_days: int = 14,
        sample_size: int = 1000
    ) -> GrowthExperiment:
        """创建增长实验"""
        exp_id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        
        experiment = GrowthExperiment(
            id=exp_id,
            name=name,
            hypothesis=hypothesis,
            control_variant=control,
            treatment_variants=treatments,
            success_criteria=success_criteria,
            duration_days=duration_days,
            sample_size=sample_size
        )
        
        self.experiments[exp_id] = experiment
        logger.info(f"🧪 创建增长实验: {name} (ID: {exp_id})")
        
        return experiment
    
    def start_experiment(self, exp_id: str) -> bool:
        """启动实验"""
        if exp_id not in self.experiments:
            logger.error(f"实验不存在: {exp_id}")
            return False
        
        experiment = self.experiments[exp_id]
        experiment.status = "running"
        experiment.start_date = datetime.now()
        
        logger.info(f"▶️ 启动实验: {experiment.name}")
        return True
    
    def record_experiment_data(
        self,
        exp_id: str,
        variant_id: str,
        metrics: Dict[str, float]
    ):
        """记录实验数据"""
        if exp_id not in self.experiments:
            return
        
        experiment = self.experiments[exp_id]
        
        if "daily_data" not in experiment.results:
            experiment.results["daily_data"] = []
        
        experiment.results["daily_data"].append({
            "timestamp": datetime.now().isoformat(),
            "variant_id": variant_id,
            "metrics": metrics
        })
    
    def analyze_experiment(self, exp_id: str) -> Dict:
        """分析实验结果"""
        if exp_id not in self.experiments:
            return {"error": "实验不存在"}
        
        experiment = self.experiments[exp_id]
        
        if "daily_data" not in experiment.results or not experiment.results["daily_data"]:
            return {"error": "无实验数据"}
        
        # 按变体分组数据
        variant_data: Dict[str, List[Dict]] = {}
        
        for record in experiment.results["daily_data"]:
            vid = record["variant_id"]
            if vid not in variant_data:
                variant_data[vid] = []
            variant_data[vid].append(record["metrics"])
        
        # 计算统计显著性
        significance = self.statistical_engine.calculate_significance(variant_data)
        
        # 计算各变体的平均表现
        variant_performance = {}
        for vid, data in variant_data.items():
            metrics_summary = {}
            for metric_key in ["conversion_rate", "revenue", "engagement"]:
                values = [d.get(metric_key, 0) for d in data]
                if values:
                    metrics_summary[metric_key] = {
                        "mean": sum(values) / len(values),
                        "count": len(values)
                    }
            variant_performance[vid] = metrics_summary
        
        findings = {
            "experiment_id": exp_id,
            "experiment_name": experiment.name,
            "significance": significance,
            "variant_performance": variant_performance,
            "control_variant": experiment.control_variant.id,
            "recommendation": self._generate_recommendation(significance, variant_performance, experiment.success_criteria)
        }
        
        return findings
    
    def _generate_recommendation(
        self,
        significance: Dict,
        variant_performance: Dict,
        success_criteria: Dict
    ) -> str:
        """生成实验建议"""
        if not significance.get("is_significant"):
            return "实验结果不显著,建议继续观察或调整实验设计"
        
        # 找到最佳变体
        control_key = list(variant_performance.keys())[0] if variant_performance else None
        
        if control_key:
            return f"变体{control_key}表现显著优于对照组,建议推广应用"
        
        return "实验结果显著,但需要进一步分析确定最优变体"
    
    def complete_experiment(self, exp_id: str) -> bool:
        """完成实验"""
        if exp_id not in self.experiments:
            return False
        
        experiment = self.experiments[exp_id]
        experiment.status = "completed"
        experiment.end_date = datetime.now()
        
        # 保存到历史
        self.experiment_history.append({
            "experiment_id": exp_id,
            "name": experiment.name,
            "completed_at": experiment.end_date.isoformat(),
            "results": experiment.results
        })
        
        logger.info(f"✅ 实验完成: {experiment.name}")
        return True
    
    def get_experiment_summary(self) -> Dict:
        """获取实验摘要"""
        return {
            "total_experiments": len(self.experiments),
            "running": sum(1 for e in self.experiments.values() if e.status == "running"),
            "completed": sum(1 for e in self.experiments.values() if e.status == "completed"),
            "pending": sum(1 for e in self.experiments.values() if e.status == "pending"),
            "history_count": len(self.experiment_history)
        }
