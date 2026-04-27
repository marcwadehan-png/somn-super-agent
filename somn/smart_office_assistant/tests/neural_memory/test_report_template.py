# -*- coding: utf-8 -*-
"""
Tests for report_template.py
从 if __name__ == "__main__" 迁移的 pytest 测试用例。
"""

from pathlib import Path
from unittest.mock import patch
import pytest


# ──────────────────────────────────────────────────────────────
# LearningMetrics 数据类
# ──────────────────────────────────────────────────────────────

class TestLearningMetrics:
    """测试学习指标数据类"""

    def test_metrics_creation(self):
        from src.neural_memory.report_template import LearningMetrics
        metrics = LearningMetrics(
            total_events=10,
            instance_count=3,
            validation_count=2,
            error_count=1,
            association_count=4,
            knowledge_updates=5,
            confidence_changes=[],
        )
        assert metrics.total_events == 10
        assert metrics.instance_count == 3
        assert metrics.knowledge_updates == 5


# ──────────────────────────────────────────────────────────────
# LearningReportTemplate
# ──────────────────────────────────────────────────────────────

class TestLearningReportTemplate:
    """测试学习报告模板生成器"""

    def test_template_creation(self, tmp_path):
        """模板能创建"""
        from src.neural_memory.report_template import LearningReportTemplate
        template = LearningReportTemplate(base_path=str(tmp_path))
        assert template is not None

    def test_generate_html_report(self, tmp_path):
        """生成 HTML 报告"""
        from src.neural_memory.report_template import LearningReportTemplate
        template = LearningReportTemplate(base_path=str(tmp_path))

        sample_data = {
            "report_date": "2026-04-06",
            "learning_summary": {"total": 10, "success": 8},
            "learning_events": [
                {"type": "instance", "content": "test event"}
            ],
            "validation_events": [
                {"hypothesis": "test", "old_confidence": 0.5, "new_confidence": 0.8}
            ],
            "error_events": [],
            "system_status": {
                "health_score": 0.85,
                "knowledge_base_size": "100条",
                "memory_density": "0.72",
            },
            "new_findings": 3,
            "patterns_extracted": 2,
            "recommendations": ["keep learning"],
        }

        output_path = template.generate_html_report(sample_data)
        assert output_path is not None
        assert Path(output_path).exists()
        content = Path(output_path).read_text(encoding="utf-8")
        assert "<html" in content.lower() or "<!doctype" in content.lower()

    def test_generate_with_custom_filename(self, tmp_path):
        """自定义文件名生成"""
        from src.neural_memory.report_template import LearningReportTemplate
        template = LearningReportTemplate(base_path=str(tmp_path))

        sample_data = {
            "report_date": "2026-04-06",
            "learning_summary": {},
            "learning_events": [],
            "validation_events": [],
            "error_events": [],
            "system_status": {},
            "new_findings": 0,
            "patterns_extracted": 0,
            "recommendations": ["继续监控数据流"],
        }

        output_path = template.generate_html_report(sample_data, output_filename="custom_report.html")
        assert "custom_report" in str(output_path)
