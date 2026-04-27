"""
Somn - 增长解决方案专家系统
Smart Office Assistant & Knowledge Management Platform

@version: 6.2.0
@license: AGPL-3.0-or-later
@author: Somn Project Team
"""

__version__ = "6.2.0"
__author__ = "Somn Project Team"
__license__ = "AGPL-3.0-or-later"

# 导出主要模块
from somn import smart_office_assistant
from somn import api
from somn import knowledge_cells
from somn import global_control_center

__all__ = [
    "smart_office_assistant",
    "api",
    "knowledge_cells",
    "global_control_center",
]
