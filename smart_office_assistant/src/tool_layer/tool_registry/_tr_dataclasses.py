"""数据类定义模块"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime

from ._tr_enums import ToolCategory, ToolStatus

__all__ = [
    'to_dict',
]

@dataclass
class ToolParameter:
    """工具参数定义"""
    name: str
    param_type: str
    description: str = ""
    required: bool = True
    default: Any = None
    enum_values: List[Any] = field(default_factory=list)

@dataclass
class Tool:
    """工具定义"""
    tool_id: str
    name: str
    category: ToolCategory
    description: str = ""
    parameters: List[ToolParameter] = field(default_factory=list)
    return_type: str = "dict"
    handler: Optional[Callable] = None
    status: ToolStatus = ToolStatus.ACTIVE
    config: Dict[str, Any] = field(default_factory=dict)
    rate_limit: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    call_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "parameters": [
                {
                    "name": p.name,
                    "type": p.param_type,
                    "description": p.description,
                    "required": p.required,
                    "default": p.default,
                    "enum": p.enum_values
                }
                for p in self.parameters
            ],
            "return_type": self.return_type,
            "status": self.status.value,
            "config": self.config,
            "rate_limit": self.rate_limit,
            "created_at": self.created_at,
            "call_count": self.call_count
        }
