"""
__all__ = [
    'init_content_gaming',
    'init_month3_profiles',
]

Month 3 新增行业画像 (1个行业)
"""

from typing import Dict
from ._ip_types import IndustryType, IndustryProfile, BusinessModel

def init_content_gaming() -> IndustryProfile:
    """内容媒体/游戏行业 (v2.1新增)"""
    return IndustryProfile(
        industry_type=IndustryType.CONTENT_GAMING,
        name="内容媒体/游戏",
        name_en="Content Media & Gaming",
        description="内容创作,媒体平台,游戏开发与运营",
        sub_types=["短视频", "直播", "游戏", "资讯", "社区"],
        business_models=[BusinessModel.ADVERTISING, BusinessModel.FREEMIUM, BusinessModel.SUBSCRIPTION],
        key_characteristics=[
            "注意力经济",
            "内容为王",
            "用户时长",
            "社交传播",
            "IP价值"
        ],
        growth_drivers=[
            "内容创新",
            "算法推荐",
            "社交裂变",
            "IP运营",
            "跨平台分发"
        ],
        key_metrics=[
            "DAU/MAU",
            "用户时长",
            "内容消费",
            "广告收入",
            "付费率"
        ],
        benchmarks={
            "dau_mau_ratio": "> 30%",
            "avg_session_duration": "> 15分钟",
            "content_consumption": "> 10条/日",
            "ad_fill_rate": "> 85%",
            "paying_rate": "> 5%"
        },
        typical_challenges=[
            "内容审核",
            "用户留存",
            "变现效率",
            "监管合规",
            "版权保护"
        ],
        best_practices=[
            "算法优化",
            "创作者生态",
            "社区治理",
            "多元变现"
        ],
        tags=["内容", "媒体", "游戏", "注意力", "IP"],
        special_attributes={
            "attention_economy": True,
            "content_driven": True,
            "viral_potential": True
        }
    )

def init_month3_profiles() -> Dict[IndustryType, IndustryProfile]:
    """初始化Month 3行业画像"""
    return {
        IndustryType.CONTENT_GAMING: init_content_gaming(),
    }
