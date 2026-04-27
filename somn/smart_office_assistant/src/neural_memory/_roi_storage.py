# -*- coding: utf-8 -*-
"""ROI追踪器 - 存储方法

__all__ = [
    'deserialize_record_impl',
    'load_records_impl',
    'save_record_impl',
    'serialize_record_impl',
]

_serialize_record / _deserialize_record / _save_record / _load_records
"""

from dataclasses import asdict
from typing import Dict, Any, List

import yaml

from .roi_types import MetricCategory, FeedbackSource, ROIRecord

def serialize_record_impl(core, record: ROIRecord) -> Dict[str, Any]:
    """把 ROIRecord 转成可安全跨进程落盘的纯字典"""
    data = asdict(record)
    data["category"] = record.category.value if isinstance(record.category, MetricCategory) else str(record.category)
    data["source"] = record.source.value if isinstance(record.source, FeedbackSource) else str(record.source)
    return data

def deserialize_record_impl(core, data: Dict[str, Any]) -> ROIRecord:
    """兼容字符串/枚举两种格式,恢复 ROIRecord"""
    category = data.get("category", MetricCategory.TASK_COMPLETION.value)
    source = data.get("source", FeedbackSource.USER_IMPLICIT.value)
    if not isinstance(category, MetricCategory):
        category = MetricCategory(str(category))
    if not isinstance(source, FeedbackSource):
        source = FeedbackSource(str(source))

    payload = dict(data)
    payload["category"] = category
    payload["source"] = source
    payload["workflow_id"] = str(payload.get("workflow_id", "") or "")
    payload["scope"] = str(payload.get("scope", "task") or "task")
    payload["strategy_combo_id"] = str(payload.get("strategy_combo_id", "") or "")
    payload["strategy_combo"] = core._normalize_strategy_combo(payload.get("strategy_combo", []))
    return ROIRecord(**payload)

def save_record_impl(core, record: ROIRecord):
    """保存单条记录"""
    path = core.records_path / f"{record.record_id}.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(core._serialize_record(record), f, allow_unicode=True, default_flow_style=False)

def load_records_impl(core):
    """加载历史记录,兼容旧版带 Python 标签的 YAML"""
    for path in sorted(core.records_path.glob("*.yaml")):
        data = None
        try:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception:
            try:
                with open(path, encoding="utf-8") as f:
                    data = yaml.load(f, Loader=yaml.UnsafeLoader)
            except Exception:
                data = None

        if not isinstance(data, dict):
            continue

        try:
            record = core._deserialize_record(data)
            core._records.append(record)
        except Exception:
            continue
