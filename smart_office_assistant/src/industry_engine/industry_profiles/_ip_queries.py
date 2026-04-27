"""
__all__ = [
    'compare_industries',
    'export_summary',
    'get_all_profiles',
    'get_industries_by_attribute',
    'get_industries_by_tag',
    'get_profile',
    'get_profile_by_name',
    'search_industries',
]

行业画像查询方法
"""

from typing import Dict, List, Optional, Any
from ._ip_types import IndustryType, IndustryProfile

class IndustryProfileLibrary:
    """行业画像库"""
    
    def __init__(self):
        self.profiles: Dict[IndustryType, IndustryProfile] = {}
    
    def get_profile(self, industry: IndustryType) -> Optional[IndustryProfile]:
        """获取行业画像"""
        return self.profiles.get(industry)
    
    def get_profile_by_name(self, name: str) -> Optional[IndustryProfile]:
        """通过名称获取行业画像"""
        name_lower = name.lower()
        for profile in self.profiles.values():
            if (profile.name == name or 
                profile.name_en.lower() == name_lower or
                profile.industry_type.value == name_lower):
                return profile
        return None
    
    def get_all_profiles(self) -> Dict[IndustryType, IndustryProfile]:
        """获取所有行业画像"""
        return self.profiles.copy()
    
    def get_industries_by_tag(self, tag: str) -> List[IndustryProfile]:
        """通过标签获取行业"""
        return [p for p in self.profiles.values() if tag in p.tags]
    
    def get_industries_by_attribute(self, attribute: str, value: Any = True) -> List[IndustryProfile]:
        """通过特殊属性获取行业"""
        return [
            p for p in self.profiles.values() 
            if p.special_attributes.get(attribute) == value
        ]
    
    def search_industries(self, keyword: str) -> List[IndustryProfile]:
        """搜索行业"""
        keyword_lower = keyword.lower()
        results = []
        for profile in self.profiles.values():
            if (keyword_lower in profile.name.lower() or
                keyword_lower in profile.description.lower() or
                keyword_lower in profile.name_en.lower() or
                any(keyword_lower in st.lower() for st in profile.sub_types) or
                any(keyword_lower in tag.lower() for tag in profile.tags)):
                results.append(profile)
        return results
    
    def compare_industries(self, industries: List[IndustryType]) -> Dict:
        """对比多个行业"""
        profiles = [self.get_profile(i) for i in industries]
        profiles = [p for p in profiles if p]
        
        return {
            "industries": [
                {
                    "type": p.industry_type.value,
                    "name": p.name,
                    "key_metrics": p.key_metrics[:3],
                    "growth_drivers": p.growth_drivers[:2],
                    "tags": p.tags
                }
                for p in profiles
            ],
            "total_count": len(profiles)
        }
    
    def export_summary(self) -> Dict:
        """导出行业摘要"""
        return {
            "total_industries": len(self.profiles),
            "industries": [
                {
                    "type": p.industry_type.value,
                    "name": p.name,
                    "sub_types_count": len(p.sub_types),
                    "key_metrics_count": len(p.key_metrics),
                    "tags": p.tags
                }
                for p in self.profiles.values()
            ]
        }
