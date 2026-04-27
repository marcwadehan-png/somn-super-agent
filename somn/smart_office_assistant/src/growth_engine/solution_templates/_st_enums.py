"""枚举定义模块"""

from enum import Enum

class SolutionType(Enum):
    """解决方案类型"""
    # 业务增长类
    PRIVATE_DOMAIN = "private_domain"       # 私域运营
    MEMBERSHIP = "membership"               # 会员体系
    DIGITAL_OPERATION = "digital_operation" # 数字化运营
    DIGITAL_TRANSFORMATION = "digital_transformation"  # 数字化转型
    INTEGRATED_MARKETING = "integrated_marketing"      # 整合营销
    XIAOHONGSHU = "xiaohongshu"             # 小红书运营
    DOUYIN = "douyin"                       # 抖音运营
    AI_GROWTH = "ai_growth"                 # AI增长
    O2O = "o2o"                             # O2O运营
    NEW_RETAIL = "new_retail"               # 新零售
    CROSS_BORDER = "cross_border"           # 跨境电商
    LIVE_COMMERCE = "live_commerce"         # 直播电商
    KOL_MARKETING = "kol_marketing"         # KOL营销
    BRAND_BUILDING = "brand_building"       # 品牌建设
    DATA_DRIVEN = "data_driven"             # 数据驱动增长
    
    # 软件系统类
    CRM = "crm"                             # 客户关系管理
    SCRM = "scrm"                           # 社交化客户关系管理
    MA = "ma"                               # 营销自动化
    
    # 人文智能类 [v1.0.0 文学智能增强]
    HUMANISTIC_BRAND = "humanistic_brand"   # 人文品牌叙事

class SolutionCategory(Enum):
    """解决方案分类"""
    ACQUISITION = "acquisition"         # 获客类
    RETENTION = "retention"             # 留存类
    MONETIZATION = "monetization"       # 变现类
    EFFICIENCY = "efficiency"           # 效率类
    TRANSFORMATION = "transformation"   # 转型类
    PLATFORM = "platform"               # 平台类
