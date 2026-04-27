"""
__all__ = [
    'detect',
    'detect_industry',
    'detect_industry_single',
    'detect_single',
    'get_recommendations',
    'get_similar_industries',
]

自动行业recognize器
Auto Industry Detector

基于业务描述,关键词,metrics等自动recognize行业类型

版本: v1.0
日期: 2026-04-03
"""

import re
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
import logging

from .industry_profiles import (
    IndustryType, IndustryProfile, 
    industry_library, get_industry_profile
)

logger = logging.getLogger(__name__)

@dataclass
class DetectionResult:
    """检测结果"""
    industry_type: IndustryType
    confidence: float
    matched_keywords: List[str]
    reason: str

class IndustryKeywordDatabase:
    """行业关键词数据库"""
    
    # 行业关键词mapping
    KEYWORDS = {
        IndustryType.SAAS_B2B: {
            "strong": ["saas", "b2b", "企业服务", "crm", "erp", "企业软件", "订阅", "arr", "mrr"],
            "medium": ["销售周期", "客户成功", "plg", "企业客户", "b端"],
            "weak": ["软件", "云", "数字化"]
        },
        IndustryType.SAAS_B2C: {
            "strong": ["app", "工具", "效率", "免费增值", "freemium", "病毒传播"],
            "medium": ["c端", "消费者", "留存", "dau", "mau"],
            "weak": ["移动", "应用"]
        },
        IndustryType.ECOMMERCE: {
            "strong": ["电商", "gmv", "购物车", "转化率", "复购", "sku", "库存"],
            "medium": ["零售", "交易", "平台", "roas", "aov"],
            "weak": ["卖货", "网店"]
        },
        IndustryType.FINTECH: {
            "strong": ["金融", "支付", "借贷", "理财", "风控", "kyc", "合规", "aum"],
            "medium": ["银行", "保险", "证券", "监管", "反欺诈"],
            "weak": ["钱", "投资"]
        },
        IndustryType.HEALTHCARE: {
            "strong": ["医疗", "医院", "医生", "患者", "处方", "复诊", "互联网医疗", "医药"],
            "medium": ["健康", "体检", "诊所", "医保", "问诊"],
            "weak": ["养生", "保健"]
        },
        IndustryType.EDUCATION: {
            "strong": ["教育", "培训", "课程", "学习", "老师", "学生", "完课率", "续费"],
            "medium": ["k12", "职业", "考试", "学校", "教学"],
            "weak": ["知识", "读书"]
        },
        IndustryType.REAL_ESTATE: {
            "strong": ["房产", "房地产", "买房", "租房", "经纪人", "带看", "楼盘"],
            "medium": ["中介", "二手房", "新房", "商业地产", "物业"],
            "weak": ["房子", "住"]
        },
        IndustryType.TRAVEL: {
            "strong": ["旅游", "酒店", "机票", "景区", "ota", "预订", "度假"],
            "medium": ["出行", "旅行社", "民宿", "门票", "攻略"],
            "weak": ["玩", "旅行"]
        },
        IndustryType.FOOD_BEVERAGE: {
            "strong": ["餐饮", "餐厅", "外卖", "翻台率", "门店", "菜品", "茶饮"],
            "medium": ["美食", "饭店", "咖啡", "烘焙", "连锁"],
            "weak": ["吃", "喝"]
        },
        IndustryType.AI_TECH: {
            "strong": ["ai", "人工智能", "大模型", "llm", "算法", "api调用", "机器学习"],
            "medium": ["智能", "模型", "训练", "推理", "generate式ai"],
            "weak": ["科技", "创新"]
        },
        IndustryType.NEW_ENERGY: {
            "strong": ["新能源", "电动车", "充电桩", "试驾", "交付", "续航", "整车"],
            "medium": ["汽车", "电池", "充电", "新能源", "造车"],
            "weak": ["车", "出行"]
        },
        IndustryType.LUXURY: {
            "strong": ["奢侈品", "高端", "vip", "限量", "品牌溢价", "腕表", "珠宝"],
            "medium": ["名牌", "高端消费", "精品", "尊享"],
            "weak": ["贵", "豪华"]
        },
        IndustryType.SPORTS_FITNESS: {
            "strong": ["健身", "运动", "健身房", "课程", "教练", "训练", "打卡"],
            "medium": ["瑜伽", "跑步", "体育", "健康", "锻炼"],
            "weak": ["瘦", "减肥"]
        },
        IndustryType.PET: {
            "strong": ["宠物", "猫", "狗", "宠物食品", "宠物医疗", "铲屎官", "萌宠"],
            "medium": ["猫粮", "狗粮", "宠物店", "宠物用品"],
            "weak": ["动物", "养"]
        },
        IndustryType.CONTENT_GAMING: {
            "strong": ["内容", "短视频", "直播", "游戏", "资讯", "创作者", "IP", "DAU", "时长"],
            "medium": ["媒体", "平台", "广告", "付费", "推荐算法"],
            "weak": ["娱乐", "视频"]
        },
    }
    
    # metrics到行业的mapping
    METRICS_TO_INDUSTRY = {
        "mrr": IndustryType.SAAS_B2B,
        "arr": IndustryType.SAAS_B2B,
        "nrr": IndustryType.SAAS_B2B,
        "logo_churn": IndustryType.SAAS_B2B,
        "dau": IndustryType.SAAS_B2C,
        "mau": IndustryType.SAAS_B2C,
        "病毒系数": IndustryType.SAAS_B2C,
        "gmv": IndustryType.ECOMMERCE,
        "转化率": [IndustryType.ECOMMERCE, IndustryType.FOOD_BEVERAGE],
        "roas": IndustryType.ECOMMERCE,
        "复购率": [IndustryType.ECOMMERCE, IndustryType.FOOD_BEVERAGE, IndustryType.PET],
        "aum": IndustryType.FINTECH,
        "kyc": IndustryType.FINTECH,
        "风控": IndustryType.FINTECH,
        "患者": IndustryType.HEALTHCARE,
        "复诊率": IndustryType.HEALTHCARE,
        "处方": IndustryType.HEALTHCARE,
        "完课率": IndustryType.EDUCATION,
        "续费率": IndustryType.EDUCATION,
        "转介绍": IndustryType.EDUCATION,
        "带看": IndustryType.REAL_ESTATE,
        "成交周期": IndustryType.REAL_ESTATE,
        "经纪人": IndustryType.REAL_ESTATE,
        "预订": IndustryType.TRAVEL,
        "nps": [IndustryType.TRAVEL, IndustryType.SAAS_B2B],
        "翻台率": IndustryType.FOOD_BEVERAGE,
        "api调用": IndustryType.AI_TECH,
        "模型": IndustryType.AI_TECH,
        "试驾": IndustryType.NEW_ENERGY,
        "交付": IndustryType.NEW_ENERGY,
        "vip": IndustryType.LUXURY,
        "打卡": IndustryType.SPORTS_FITNESS,
        "铲屎官": IndustryType.PET,
        "dau": [IndustryType.SAAS_B2C, IndustryType.CONTENT_GAMING],
        "mau": [IndustryType.SAAS_B2C, IndustryType.CONTENT_GAMING],
        "时长": IndustryType.CONTENT_GAMING,
        "付费率": IndustryType.CONTENT_GAMING,
        "广告": IndustryType.CONTENT_GAMING,
    }

class AutoIndustryDetector:
    """自动行业recognize器"""
    
    def __init__(self):
        self.keyword_db = IndustryKeywordDatabase()
        self.industry_library = industry_library
    
    def detect(
        self,
        description: str = "",
        keywords: List[str] = None,
        metrics: List[str] = None,
        top_k: int = 3
    ) -> List[DetectionResult]:
        """
        自动recognize行业
        
        Args:
            description: 业务描述文本
            keywords: 关键词列表
            metrics: metrics列表
            top_k: 返回前K个结果
        
        Returns:
            检测结果列表
        """
        scores = defaultdict(lambda: {"score": 0.0, "keywords": [], "reasons": []})
        
        # 1. 基于描述文本分析
        if description:
            desc_scores = self._analyze_description(description)
            for industry, data in desc_scores.items():
                scores[industry]["score"] += data["score"] * 0.4  # 权重40%
                scores[industry]["keywords"].extend(data["keywords"])
                scores[industry]["reasons"].append(f"文本匹配: {', '.join(data['keywords'][:3])}")
        
        # 2. 基于关键词分析
        if keywords:
            kw_scores = self._analyze_keywords(keywords)
            for industry, data in kw_scores.items():
                scores[industry]["score"] += data["score"] * 0.35  # 权重35%
                scores[industry]["keywords"].extend(data["keywords"])
                scores[industry]["reasons"].append(f"关键词匹配: {', '.join(data['keywords'][:3])}")
        
        # 3. 基于metrics分析
        if metrics:
            metric_scores = self._analyze_metrics(metrics)
            for industry, data in metric_scores.items():
                scores[industry]["score"] += data["score"] * 0.25  # 权重25%
                scores[industry]["keywords"].extend(data["metrics"])
                scores[industry]["reasons"].append(f"metrics匹配: {', '.join(data['metrics'][:3])}")
        
        # 转换为结果列表
        results = []
        for industry, data in scores.items():
            if data["score"] > 0:
                confidence = min(data["score"] / 100, 1.0)  # 归一化到0-1
                results.append(DetectionResult(
                    industry_type=industry,
                    confidence=confidence,
                    matched_keywords=list(set(data["keywords"])),
                    reason="; ".join(data["reasons"])
                ))
        
        # 按置信度排序
        results.sort(key=lambda x: x.confidence, reverse=True)
        
        return results[:top_k]
    
    def _analyze_description(self, description: str) -> Dict:
        """分析描述文本"""
        desc_lower = description.lower()
        scores = defaultdict(lambda: {"score": 0, "keywords": []})
        
        for industry, keywords in self.keyword_db.KEYWORDS.items():
            # 强关键词匹配
            for kw in keywords["strong"]:
                if kw in desc_lower:
                    scores[industry]["score"] += 20
                    scores[industry]["keywords"].append(kw)
            
            # 中等关键词匹配
            for kw in keywords["medium"]:
                if kw in desc_lower:
                    scores[industry]["score"] += 10
                    scores[industry]["keywords"].append(kw)
            
            # 弱关键词匹配
            for kw in keywords["weak"]:
                if kw in desc_lower:
                    scores[industry]["score"] += 5
                    scores[industry]["keywords"].append(kw)
        
        return dict(scores)
    
    def _analyze_keywords(self, keywords: List[str]) -> Dict:
        """分析关键词"""
        scores = defaultdict(lambda: {"score": 0, "keywords": []})
        
        for keyword in keywords:
            kw_lower = keyword.lower()
            
            for industry, kw_groups in self.keyword_db.KEYWORDS.items():
                for strength, kw_list in kw_groups.items():
                    weight = {"strong": 15, "medium": 8, "weak": 3}[strength]
                    for kw in kw_list:
                        if kw in kw_lower or kw_lower in kw:
                            scores[industry]["score"] += weight
                            scores[industry]["keywords"].append(keyword)
        
        return dict(scores)
    
    def _analyze_metrics(self, metrics: List[str]) -> Dict:
        """分析metrics"""
        scores = defaultdict(lambda: {"score": 0, "metrics": []})
        
        for metric in metrics:
            metric_lower = metric.lower()
            
            for kw, industry in self.keyword_db.METRICS_TO_INDUSTRY.items():
                if kw in metric_lower:
                    if isinstance(industry, list):
                        for ind in industry:
                            scores[ind]["score"] += 25
                            scores[ind]["metrics"].append(metric)
                    else:
                        scores[industry]["score"] += 25
                        scores[industry]["metrics"].append(metric)
        
        return dict(scores)
    
    def detect_single(
        self,
        description: str = "",
        keywords: List[str] = None,
        metrics: List[str] = None,
        confidence_threshold: float = 0.5
    ) -> Optional[IndustryType]:
        """
        recognize单一行业(最高置信度)
        
        Args:
            description: 业务描述
            keywords: 关键词
            metrics: metrics
            confidence_threshold: 置信度阈值
        
        Returns:
            行业类型或None
        """
        results = self.detect(description, keywords, metrics, top_k=1)
        
        if results and results[0].confidence >= confidence_threshold:
            return results[0].industry_type
        
        return None
    
    def get_recommendations(
        self,
        current_industry: IndustryType,
        top_k: int = 3
    ) -> List[Dict]:
        """
        get相似行业推荐
        
        基于标签和属性相似度推荐相关行业
        """
        current_profile = self.industry_library.get_profile(current_industry)
        if not current_profile:
            return []
        
        similarities = []
        
        for industry_type, profile in self.industry_library.get_all_profiles().items():
            if industry_type == current_industry:
                continue
            
            # 计算相似度
            similarity = self._calculate_similarity(current_profile, profile)
            
            if similarity > 0.3:  # 阈值
                similarities.append({
                    "industry": industry_type,
                    "name": profile.name,
                    "similarity": similarity,
                    "shared_tags": list(set(current_profile.tags) & set(profile.tags)),
                    "shared_attributes": self._get_shared_attributes(
                        current_profile.special_attributes,
                        profile.special_attributes
                    )
                })
        
        # 按相似度排序
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        return similarities[:top_k]
    
    def _calculate_similarity(
        self,
        profile1: IndustryProfile,
        profile2: IndustryProfile
    ) -> float:
        """计算两个行业画像的相似度"""
        score = 0.0
        
        # 标签相似度 (权重40%)
        tags1 = set(profile1.tags)
        tags2 = set(profile2.tags)
        if tags1 and tags2:
            tag_sim = len(tags1 & tags2) / len(tags1 | tags2)
            score += tag_sim * 0.4
        
        # 商业模式相似度 (权重30%)
        models1 = set(profile1.business_models)
        models2 = set(profile2.business_models)
        if models1 and models2:
            model_sim = len(models1 & models2) / len(models1 | models2)
            score += model_sim * 0.3
        
        # 属性相似度 (权重30%)
        attrs1 = set(profile1.special_attributes.keys())
        attrs2 = set(profile2.special_attributes.keys())
        if attrs1 and attrs2:
            attr_sim = len(attrs1 & attrs2) / len(attrs1 | attrs2)
            score += attr_sim * 0.3
        
        return score
    
    def _get_shared_attributes(self, attrs1: Dict, attrs2: Dict) -> List[str]:
        """get共享属性"""
        shared = []
        for key in set(attrs1.keys()) & set(attrs2.keys()):
            if attrs1[key] == attrs2[key]:
                shared.append(key)
        return shared

# 全局实例
detector = AutoIndustryDetector()

# 便捷函数
def detect_industry(
    description: str = "",
    keywords: List[str] = None,
    metrics: List[str] = None,
    top_k: int = 3
) -> List[DetectionResult]:
    """检测行业便捷函数"""
    return detector.detect(description, keywords, metrics, top_k)

def detect_industry_single(
    description: str = "",
    keywords: List[str] = None,
    metrics: List[str] = None,
    confidence_threshold: float = 0.5
) -> Optional[IndustryType]:
    """检测单一行业便捷函数"""
    return detector.detect_single(description, keywords, metrics, confidence_threshold)

def get_similar_industries(
    industry: str,
    top_k: int = 3
) -> List[Dict]:
    """get相似行业便捷函数"""
    try:
        industry_type = IndustryType(industry.lower())
        return detector.get_recommendations(industry_type, top_k)
    except ValueError:
        return []
