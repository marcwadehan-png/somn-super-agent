"""与V2模板库集成"""

import yaml
from pathlib import Path

from ._sl_v2_engine import BenchmarkLearningEngine

__all__ = [
    'integrate_with_template_library',
]

def integrate_with_template_library(template_library_v2):
    """
    将学习引擎与V2模板库集成
    
    实现动态基准更新
    """
    learning_engine = BenchmarkLearningEngine()
    
    # 加载学习到的基准数据到模板库
    for solution_type in template_library_v2.templates.keys():
        template = template_library_v2.templates[solution_type]
        
        for metric in template.dynamic_metrics:
            industry_baselines = {}
            
            # 尝试加载学习到的基准
            for industry in metric.industry_baselines.keys():
                benchmark_file = learning_engine.benchmarks_path / f"{solution_type.value}_{industry}.yaml"
                
                if benchmark_file.exists():
                    with open(benchmark_file, 'r', encoding='utf-8') as f:
                        learned_baseline = yaml.safe_load(f)
                        if learned_baseline and metric.metric_id in learned_baseline:
                            industry_baselines[industry] = learned_baseline[metric.metric_id]
            
            # 如果有学习到的数据,更新metrics定义
            if industry_baselines:
                metric.industry_baselines.update(industry_baselines)
    
    return learning_engine
