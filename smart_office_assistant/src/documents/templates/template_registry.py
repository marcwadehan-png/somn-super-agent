# -*- coding: utf-8 -*-
"""
文档模板注册表 [v22.4]
Template Registry

功能:
- 内置模板注册表
- 模板元数据管理
- 模板分类检索

版本: v22.4.0
日期: 2026-04-25
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json


class TemplateCategory(Enum):
    """模板分类"""
    REPORT = "报告"
    MEETING = "会议"
    BUSINESS = "商务"
    FINANCIAL = "财务"
    PRESENTATION = "演示"
    DATA = "数据"
    CUSTOM = "自定义"


@dataclass
class TemplateMetadata:
    """模板元数据"""
    name: str                      # 模板名称
    category: TemplateCategory      # 分类
    description: str               # 描述
    file_path: Path                # 文件路径
    variables: List[str] = field(default_factory=list)  # 变量列表
    tags: List[str] = field(default_factory=list)      # 标签
    author: str = ""               # 作者
    version: str = "6.2.0"          # 版本
    created: str = ""             # 创建日期


class TemplateRegistry:
    """
    模板注册表
    
    管理所有可用模板，提供检索和加载功能。
    """
    
    # 内置模板目录
    TEMPLATES_DIR = Path(__file__).parent / "templates"
    
    # 模板注册表
    _registry: Dict[str, TemplateMetadata] = {}
    
    # 初始化注册表
    @classmethod
    def initialize(cls):
        """初始化模板注册表"""
        cls._register_builtin_templates()
    
    @classmethod
    def _register_builtin_templates(cls):
        """注册内置模板"""
        templates = [
            # Word模板
            TemplateMetadata(
                name="通用报告模板",
                category=TemplateCategory.REPORT,
                description="标准的项目报告/工作总结模板",
                file_path=cls.TEMPLATES_DIR / "report_template.docx",
                variables=["title", "author", "date", "department", "summary", "content"],
                tags=["报告", "总结", "通用"]
            ),
            TemplateMetadata(
                name="会议纪要模板",
                category=TemplateCategory.MEETING,
                description="标准的会议记录和决策跟踪模板",
                file_path=cls.TEMPLATES_DIR / "meeting_template.docx",
                variables=["meeting_title", "date", "attendees", "chairman", "recorder"],
                tags=["会议", "纪要", "决策"]
            ),
            
            # Excel模板
            TemplateMetadata(
                name="数据表格模板",
                category=TemplateCategory.DATA,
                description="通用的数据记录和分析表格",
                file_path=cls.TEMPLATES_DIR / "data_table.xlsx",
                variables=["title", "date", "analyst"],
                tags=["数据", "表格", "分析"]
            ),
            TemplateMetadata(
                name="预算表模板",
                category=TemplateCategory.FINANCIAL,
                description="项目预算和费用跟踪表",
                file_path=cls.TEMPLATES_DIR / "budget.xlsx",
                variables=["project_name", "start_date", "end_date", "manager"],
                tags=["预算", "财务", "费用"]
            ),
            
            # PPT模板
            TemplateMetadata(
                name="演示文稿模板",
                category=TemplateCategory.PRESENTATION,
                description="标准的商务演示文稿模板",
                file_path=cls.TEMPLATES_DIR / "presentation.pptx",
                variables=["title", "subtitle", "author", "date"],
                tags=["演示", "PPT", "商务"]
            ),
        ]
        
        for template in templates:
            cls._registry[template.name] = template
    
    @classmethod
    def get(cls, name: str) -> Optional[TemplateMetadata]:
        """获取模板元数据"""
        return cls._registry.get(name)
    
    @classmethod
    def get_all(cls) -> List[TemplateMetadata]:
        """获取所有模板"""
        return list(cls._registry.values())
    
    @classmethod
    def search(cls, keyword: str) -> List[TemplateMetadata]:
        """搜索模板"""
        keyword_lower = keyword.lower()
        results = []
        
        for template in cls._registry.values():
            # 搜索名称、描述、标签
            if (keyword_lower in template.name.lower() or
                keyword_lower in template.description.lower() or
                any(keyword_lower in tag.lower() for tag in template.tags)):
                results.append(template)
        
        return results
    
    @classmethod
    def filter_by_category(cls, category: TemplateCategory) -> List[TemplateMetadata]:
        """按分类筛选模板"""
        return [t for t in cls._registry.values() if t.category == category]
    
    @classmethod
    def get_template_path(cls, name: str) -> Optional[Path]:
        """获取模板文件路径"""
        template = cls._registry.get(name)
        return template.file_path if template else None
    
    @classmethod
    def export_catalog(cls) -> Dict[str, Any]:
        """导出模板目录"""
        return {
            template.name: {
                "category": template.category.value,
                "description": template.description,
                "variables": template.variables,
                "tags": template.tags,
                "file_path": str(template.file_path),
                "exists": template.file_path.exists()
            }
            for template in cls._registry.values()
        }


# 便捷函数
def get_template(name: str) -> Optional[TemplateMetadata]:
    """获取模板元数据"""
    return TemplateRegistry.get(name)


def list_templates(category: Optional[TemplateCategory] = None) -> List[TemplateMetadata]:
    """列出模板"""
    if category:
        return TemplateRegistry.filter_by_category(category)
    return TemplateRegistry.get_all()


def search_templates(keyword: str) -> List[TemplateMetadata]:
    """搜索模板"""
    return TemplateRegistry.search(keyword)


# 初始化注册表
TemplateRegistry.initialize()
