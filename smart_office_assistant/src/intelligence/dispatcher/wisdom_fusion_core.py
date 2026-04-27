"""wisdom_fusion_core backward compat layer v1.2

修复: 只导入已存在于wisdom_fusion包中的符号
"""
from .wisdom_fusion import (
    WisdomFusionCore, WisdomPriority, FusionMethod,
    WisdomContribution, FusionConfig, FusionResult,
)

# 注意: fuse_wisdom 和 get_fusion_insights 是 WisdomFusionCore 的方法，不是模块函数
