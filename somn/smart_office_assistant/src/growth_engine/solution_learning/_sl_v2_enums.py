"""V2 枚举定义"""

from enum import Enum

class LearningSourceType(Enum):
    """学习来源类型"""
    SERVICE_PROVIDER = "服务商"      # 行业服务商官网/文档
    CASE_STUDY = "案例研究"          # 客户案例
    INDUSTRY_REPORT = "行业报告"     # 第三方研究报告
    USER_FEEDBACK = "用户反馈"       # 实际使用反馈
    COMPETITOR_ANALYSIS = "竞品分析" # 竞争对手方案
    EXPERT_INTERVIEW = "专家访谈"    # 行业专家访谈

    # V1 兼容值
    V1_SERVICE_PROVIDER = "service_provider"
    V1_CASE_STUDY = "case_study"
    V1_USER_FEEDBACK = "user_feedback"
    V1_MARKET_RESEARCH = "market_research"
