"""V2 基准学习引擎"""

import re
import yaml
import statistics
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.core.paths import SOLUTION_LEARNING_DIR
from ._sl_v2_enums import LearningSourceType
from ._sl_v2_dataclasses import BenchmarkDataPoint, IndustryBenchmarkUpdate
from ._sl_utils import safe_yaml_load, safe_yaml_dump, _enum_to_str

__all__ = [
    'aggregate_benchmarks',
    'apply_benchmark_update',
    'detect_anomalies',
    'extract_outcomes_from_case',
    'get_benchmark_statistics',
    'learn_from_provider_cases',
    'propose_benchmark_update',
]

class BenchmarkLearningEngine:
    """
    基准数据学习引擎
    
    核心功能:
    1. 从服务商案例中提取效果数据
    2. 聚类分析generate行业基准
    3. 检测基准数据异常
    4. 持续更新行业基准库
    """
    
    def __init__(self, base_path: str = None):
        resolved_base_path = Path(base_path) if base_path else SOLUTION_LEARNING_DIR
        self.base_path = resolved_base_path
        self.benchmarks_path = self.base_path / "benchmarks"
        self.updates_path = self.base_path / "benchmark_updates"

        
        # 创建目录
        self.benchmarks_path.mkdir(parents=True, exist_ok=True)
        self.updates_path.mkdir(parents=True, exist_ok=True)
        
        # 效果数据提取模式
        self.outcome_patterns = self._init_outcome_patterns()
    
    def _init_outcome_patterns(self) -> Dict:
        """init效果数据提取模式"""
        return {
            "percentage_increase": [
                r"提升(\d+(?:\.\d+)?)%",
                r"增长(\d+(?:\.\d+)?)%",
                r"增加(\d+(?:\.\d+)?)%",
                r"(\d+(?:\.\d+)?)%提升",
                r"(\d+(?:\.\d+)?)%增长",
            ],
            "multiple_increase": [
                r"(\d+(?:\.\d+)?)倍",
                r"提升(\d+(?:\.\d+)?)倍",
                r"增长(\d+(?:\.\d+)?)倍",
            ],
            "absolute_value": [
                r"(\d+(?:\.\d+)?)万",
                r"(\d+(?:\.\d+)?)亿",
                r"(\d{3,})元",
            ],
            "ratio": [
                r"ROI[\s::]*(\d+(?:\.\d+)?)",
                r"转化率[\s::]*(\d+(?:\.\d+)?)%",
                r"留存率[\s::]*(\d+(?:\.\d+)?)%",
            ],
        }
    
    def extract_outcomes_from_case(self, case_content: str, 
                                   provider_name: str,
                                   industry: str,
                                   solution_type: str) -> List[BenchmarkDataPoint]:
        """
        从案例内容中提取效果数据
        
        Args:
            case_content: 案例文本内容
            provider_name: 服务商名称
            industry: 行业
            solution_type: 解决方案类型
            
        Returns:
            提取的基准数据点列表
        """
        data_points = []
        
        # 1. 提取百分比增长数据
        for pattern in self.outcome_patterns["percentage_increase"]:
            matches = re.finditer(pattern, case_content)
            for match in matches:
                value = float(match.group(1))
                # get上下文
                start = max(0, match.start() - 50)
                end = min(len(case_content), match.end() + 50)
                context = case_content[start:end]
                
                # recognizemetrics类型
                metric_name = self._identify_metric_type(context, "percentage")
                
                if metric_name:
                    data_point = BenchmarkDataPoint(
                        metric_name=metric_name,
                        industry=industry,
                        value_low=value * 0.7,      # 估算低值
                        value_typical=value,         # 典型值
                        value_high=value * 1.3,      # 估算高值
                        source_provider=provider_name,
                        source_type=LearningSourceType.CASE_STUDY,
                        confidence=0.6,
                        context={"extracted_text": context}
                    )
                    data_points.append(data_point)
        
        # 2. 提取倍数增长数据
        for pattern in self.outcome_patterns["multiple_increase"]:
            matches = re.finditer(pattern, case_content)
            for match in matches:
                value = float(match.group(1))
                start = max(0, match.start() - 50)
                end = min(len(case_content), match.end() + 50)
                context = case_content[start:end]
                
                metric_name = self._identify_metric_type(context, "multiple")
                
                if metric_name:
                    data_point = BenchmarkDataPoint(
                        metric_name=metric_name,
                        industry=industry,
                        value_low=value * 0.8,
                        value_typical=value,
                        value_high=value * 1.2,
                        source_provider=provider_name,
                        source_type=LearningSourceType.CASE_STUDY,
                        confidence=0.65,
                        context={"extracted_text": context}
                    )
                    data_points.append(data_point)
        
        # 3. 提取ROI等比率数据
        for pattern in self.outcome_patterns["ratio"]:
            matches = re.finditer(pattern, case_content)
            for match in matches:
                value = float(match.group(1))
                start = max(0, match.start() - 50)
                end = min(len(case_content), match.end() + 50)
                context = case_content[start:end]
                
                metric_name = self._identify_metric_type(context, "ratio")
                
                if metric_name:
                    data_point = BenchmarkDataPoint(
                        metric_name=metric_name,
                        industry=industry,
                        value_low=value * 0.7,
                        value_typical=value,
                        value_high=value * 1.3,
                        source_provider=provider_name,
                        source_type=LearningSourceType.CASE_STUDY,
                        confidence=0.7,
                        context={"extracted_text": context}
                    )
                    data_points.append(data_point)
        
        return data_points
    
    def _identify_metric_type(self, context: str, value_type: str) -> Optional[str]:
        """recognizemetrics类型"""
        metric_keywords = {
            "cac_reduction": ["获客成本", "CAC", "获客", "成本降低"],
            "ltv_lift": ["LTV", "用户价值", "生命周期", "价值提升"],
            "conversion_rate": ["转化率", "转化", "成交率"],
            "retention_rate": ["留存率", "留存", "复购率"],
            "roi": ["ROI", "投资回报", "投入产出"],
            "gmv_growth": ["GMV", "销售额", "营收增长"],
            "efficiency_lift": ["效率", "人效", "效率提升"],
            "user_growth": ["用户增长", "粉丝增长", "增长"],
            "penetration_rate": ["渗透率", "会员占比"],
            "arpu_lift": ["ARPU", "客单价", "用户消费"],
        }
        
        for metric_name, keywords in metric_keywords.items():
            for keyword in keywords:
                if keyword in context:
                    return metric_name
        
        return None
    
    def aggregate_benchmarks(self, data_points: List[BenchmarkDataPoint],
                            solution_type: str,
                            industry: str) -> Dict:
        """
        聚类分析generate行业基准
        
        Args:
            data_points: 数据点列表
            solution_type: 解决方案类型
            industry: 行业
            
        Returns:
            聚合后的基准数据
        """
        # 按metrics分组
        by_metric = {}
        for dp in data_points:
            if dp.metric_name not in by_metric:
                by_metric[dp.metric_name] = []
            by_metric[dp.metric_name].append(dp)
        
        aggregated = {}
        
        for metric_name, points in by_metric.items():
            if len(points) < 2:
                # 数据点太少,直接使用
                if points:
                    aggregated[metric_name] = {
                        "low": points[0].value_low,
                        "typical": points[0].value_typical,
                        "high": points[0].value_high,
                        "sample_size": 1,
                        "confidence": points[0].confidence
                    }
                continue
            
            # 计算统计值
            typical_values = [p.value_typical for p in points]
            
            aggregated[metric_name] = {
                "low": round(min(p.value_low for p in points), 1),
                "typical": round(statistics.median(typical_values), 1),
                "high": round(max(p.value_high for p in points), 1),
                "sample_size": len(points),
                "confidence": round(sum(p.confidence for p in points) / len(points), 2),
                "std_dev": round(statistics.stdev(typical_values), 2) if len(points) > 1 else 0
            }
        
        return aggregated
    
    def detect_anomalies(self, new_benchmarks: Dict, 
                        existing_benchmarks: Dict) -> List[Dict]:
        """
        检测基准数据异常
        
        规则:
        - 新值与旧值差异超过50%视为异常
        - 需要人工验证
        """
        anomalies = []
        
        for metric_name, new_data in new_benchmarks.items():
            if metric_name not in existing_benchmarks:
                continue
            
            old_data = existing_benchmarks[metric_name]
            old_typical = old_data.get("typical", 0)
            new_typical = new_data.get("typical", 0)
            
            if old_typical > 0:
                change_ratio = abs(new_typical - old_typical) / old_typical
                
                if change_ratio > 0.5:  # 变化超过50%
                    anomalies.append({
                        "metric_name": metric_name,
                        "old_value": old_typical,
                        "new_value": new_typical,
                        "change_ratio": round(change_ratio, 2),
                        "severity": "high" if change_ratio > 1.0 else "medium"
                    })
        
        return anomalies
    
    def propose_benchmark_update(self, solution_type: str,
                                 industry: str,
                                 new_data_points: List[BenchmarkDataPoint]) -> Optional[IndustryBenchmarkUpdate]:
        """
        提出基准更新建议
        
        Args:
            solution_type: 解决方案类型
            industry: 行业
            new_data_points: 新的数据点
            
        Returns:
            更新建议或None
        """
        # 1. 聚合新数据
        new_benchmarks = self.aggregate_benchmarks(new_data_points, solution_type, industry)
        
        # 2. 加载现有基准
        existing_benchmarks = self._load_existing_benchmark(solution_type, industry)
        
        # 3. 检测异常
        anomalies = self.detect_anomalies(new_benchmarks, existing_benchmarks)
        
        # 4. 如果有显著变化,generate更新建议
        if anomalies or self._has_significant_change(new_benchmarks, existing_benchmarks):
            update_id = f"UPD_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{solution_type[:4]}"
            
            update = IndustryBenchmarkUpdate(
                update_id=update_id,
                solution_type=solution_type,
                industry=industry,
                metric_name="multiple",  # 可能涉及多个metrics
                old_baseline=existing_benchmarks,
                new_baseline=new_benchmarks,
                change_reason=self._generate_change_reason(new_data_points, anomalies),
                data_points=new_data_points,
                validation_status="pending" if anomalies else "auto_approved"
            )
            
            # 保存更新记录
            self._save_update(update)
            
            return update
        
        return None
    
    def _load_existing_benchmark(self, solution_type: str, industry: str) -> Dict:
        """加载现有基准"""
        benchmark_file = self.benchmarks_path / f"{solution_type}_{industry}.yaml"
        
        if benchmark_file.exists():
            with open(benchmark_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        
        return {}
    
    def _has_significant_change(self, new_benchmarks: Dict, 
                                existing_benchmarks: Dict,
                                threshold: float = 0.2) -> bool:
        """检查是否有显著变化"""
        for metric_name, new_data in new_benchmarks.items():
            if metric_name not in existing_benchmarks:
                return True
            
            old_typical = existing_benchmarks[metric_name].get("typical", 0)
            new_typical = new_data.get("typical", 0)
            
            if old_typical > 0:
                change_ratio = abs(new_typical - old_typical) / old_typical
                if change_ratio > threshold:
                    return True
        
        return False
    
    def _generate_change_reason(self, data_points: List[BenchmarkDataPoint],
                               anomalies: List[Dict]) -> str:
        """generate变更原因说明"""
        reasons = []
        
        # 数据来源说明
        providers = set(dp.source_provider for dp in data_points)
        reasons.append(f"基于{len(data_points)}个数据点,来自{len(providers)}个服务商")
        
        # 异常说明
        if anomalies:
            reasons.append(f"检测到{len(anomalies)}个metrics存在显著变化")
        
        return "; ".join(reasons)
    
    def _save_update(self, update: IndustryBenchmarkUpdate):
        """保存更新记录"""
        update_file = self.updates_path / f"{update.update_id}.yaml"
        with open(update_file, 'w', encoding='utf-8') as f:
            yaml.dump(_enum_to_str(update.__dict__), f, allow_unicode=True, default_flow_style=False)
    
    def apply_benchmark_update(self, update_id: str) -> bool:
        """
        应用基准更新
        
        Args:
            update_id: 更新ID
            
        Returns:
            是否成功
        """
        update_file = self.updates_path / f"{update_id}.yaml"
        
        if not update_file.exists():
            return False
        
        with open(update_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            update = IndustryBenchmarkUpdate(**data)
        
        # 保存新的基准
        benchmark_file = self.benchmarks_path / f"{update.solution_type}_{update.industry}.yaml"
        with open(benchmark_file, 'w', encoding='utf-8') as f:
            yaml.dump(update.new_baseline, f, allow_unicode=True, default_flow_style=False)
        
        # 更新状态
        update.validation_status = "verified"
        self._save_update(update)
        
        return True
    
    def learn_from_provider_cases(self, provider_name: str,
                                  cases: List[Dict]) -> List[IndustryBenchmarkUpdate]:
        """
        从服务商案例批量学习
        
        Args:
            provider_name: 服务商名称
            cases: 案例列表
            
        Returns:
            generate的更新建议列表
        """
        updates = []
        
        for case in cases:
            case_content = case.get("content", "")
            industry = case.get("industry", "未知")
            solution_type = case.get("solution_type", "unknown")
            
            # 提取数据点
            data_points = self.extract_outcomes_from_case(
                case_content, provider_name, industry, solution_type
            )
            
            if data_points:
                # 提出更新建议
                update = self.propose_benchmark_update(
                    solution_type, industry, data_points
                )
                
                if update:
                    updates.append(update)
        
        return updates
    
    def get_benchmark_statistics(self) -> Dict:
        """get基准数据统计"""
        stats = {
            "total_benchmarks": 0,
            "by_solution_type": {},
            "by_industry": {},
            "pending_updates": 0,
            "recent_updates": []
        }
        
        # 统计基准文件
        for benchmark_file in self.benchmarks_path.glob("*.yaml"):
            stats["total_benchmarks"] += 1
            
            # 解析文件名
            parts = benchmark_file.stem.split("_")
            if len(parts) >= 2:
                solution_type = parts[0]
                industry = "_".join(parts[1:])
                
                stats["by_solution_type"][solution_type] = stats["by_solution_type"].get(solution_type, 0) + 1
                stats["by_industry"][industry] = stats["by_industry"].get(industry, 0) + 1
        
        # 统计更新记录
        for update_file in self.updates_path.glob("*.yaml"):
            with open(update_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data.get("validation_status") == "pending":
                    stats["pending_updates"] += 1
        
        return stats
