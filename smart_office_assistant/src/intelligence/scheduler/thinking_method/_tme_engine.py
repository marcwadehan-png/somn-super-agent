"""
__all__ = [
    'analyze',
    'analyze_thinking_method',
    'select_method',
]

思维方法引擎核心类
"""

import re
from typing import Dict, List, Optional, Any, Callable
from ._tme_enums import ThinkingMethod, ThinkingDepth
from ._tme_dataclasses import (
    ThinkingAnalysis,
    ThinkingPath,
    MethodSuggestion,
    ThinkingMethodResult,
)

class ThinkingMethodEngine:
    """思维方法引擎 - 基于中国哲学智慧的思维方法分析器"""

    def __init__(self):
        """初始化思维方法引擎"""
        self.query = ""
        self.context = {}
        self.method_descriptions = self._init_method_descriptions()

    def _init_method_descriptions(self) -> Dict[str, Dict[str, Any]]:
        """初始化思维方法描述库"""
        return {
            "yangming_xinxue": {
                "title": "王阳明心学思维",
                "description": "知行合一、致良知的思维方法",
                "keywords": ["知行合一", "致良知", "心即理", "事上磨练"],
                "process": ["知之真切笃实处即是行", "行之明觉精察处即是知"],
                "applications": ["战略决策", "自我修养", "企业管理"],
            },
            "zengzi_self_examination": {
                "title": "曾子吾日三省思维",
                "description": "每日反思的思维方法",
                "keywords": ["为人谋而不忠乎", "与朋友交而不信乎", "传不习乎"],
                "process": ["为人谋", "与朋友交", "传不习"],
                "applications": ["自我提升", "人际关系", "学习进步"],
            },
            "mozijianai": {
                "title": "墨子兼爱思维",
                "description": "无差别的关爱思维",
                "keywords": ["兼相爱", "交相利", "非攻", "节用"],
                "process": ["兼爱", "非攻", "节用", "尚贤"],
                "applications": ["社会公益", "资源配置", "人际合作"],
            },
            "sunwu_strategic": {
                "title": "孙武战略思维",
                "description": "知己知彼的战略分析",
                "keywords": ["知己知彼", "兵者诡道", "上兵伐谋", "不战而屈人之兵"],
                "process": ["知彼知己", "庙算", "奇正", "因敌制胜"],
                "applications": ["商业竞争", "谈判策略", "危机处理"],
            },
            "mozijieyong": {
                "title": "墨子节用思维",
                "description": "实用主义的思维方法",
                "keywords": ["节用", "非攻", "节葬", "非乐"],
                "process": ["考察需求", "评估成本", "优化方案"],
                "applications": ["资源管理", "成本控制", "效率提升"],
            },
            "huanzi_practical": {
                "title": "换位思考思维",
                "description": "站在对方角度思考问题",
                "keywords": ["换位", "理解", "共情", "沟通"],
                "process": ["理解对方立场", "分析对方需求", "寻找共同点"],
                "applications": ["沟通协调", "矛盾调解", "客户服务"],
            },
            "daode_ziran": {
                "title": "道德自然思维",
                "description": "顺应自然规律的思维",
                "keywords": ["道法自然", "无为而治", "顺势而为"],
                "process": ["观察规律", "顺应趋势", "自然行动"],
                "applications": ["战略规划", "风险管理", "个人发展"],
            },
            "daode_wuwei": {
                "title": "道德无为思维",
                "description": "不妄为的智慧思维",
                "keywords": ["无为", "不争", "柔弱胜刚强"],
                "process": ["认识边界", "避免妄为", "顺势而成"],
                "applications": ["领导艺术", "团队管理", "个人修养"],
            },
            "daode_qiu": {
                "title": "道德求索思维",
                "description": "不断探索的思维方法",
                "keywords": ["上善若水", "柔弱处上", "为而不争"],
                "process": ["深入分析", "持续探索", "创新突破"],
                "applications": ["学术研究", "产品创新", "个人成长"],
            },
            "zhuangzi_qiwu": {
                "title": "庄子齐物思维",
                "description": "万物齐一的辩证思维",
                "keywords": ["齐物", "相对", "逍遥", "齐是非"],
                "process": ["超越偏见", "多角度思考", "寻求平衡"],
                "applications": ["认知提升", "心态调整", "视野拓展"],
            },
            "zhuangzi_xiaoyao": {
                "title": "庄子逍遥思维",
                "description": "自由超脱的思维境界",
                "keywords": ["逍遥", "自由", "无待", "无用"],
                "process": ["放下执念", "超越限制", "达到自由"],
                "applications": ["心态调整", "压力缓解", "创造力激发"],
            },
            "xinzi_correct": {
                "title": "荀子劝学思维",
                "description": "学以致用的思维方法",
                "keywords": ["学不可以已", "青出于蓝", "锲而不舍"],
                "process": ["学习积累", "实践应用", "不断精进"],
                "applications": ["学习成长", "技能提升", "职业发展"],
            },
            "xinzi_biran": {
                "title": "荀子自然思维",
                "description": "人性本恶的治理思维",
                "keywords": ["性恶", "礼法", "教化", "规范"],
                "process": ["认识人性", "建立规范", "引导向善"],
                "applications": ["制度建设", "团队管理", "教育引导"],
            },
            "xinfa_benti": {
                "title": "心法本体思维",
                "description": "回归本质的思维方法",
                "keywords": ["本体", "核心", "本质", "回归"],
                "process": ["剥离表象", "抓住本质", "直击核心"],
                "applications": ["问题分析", "决策制定", "创新突破"],
            },
            "zonghe_zh": {
                "title": "综合思维",
                "description": "多维度综合分析思维",
                "keywords": ["综合", "系统", "整体", "全局"],
                "process": ["多角度分析", "系统整合", "全局优化"],
                "applications": ["战略规划", "复杂问题处理", "创新设计"],
            },
            "zonghe_xt": {
                "title": "综合系统思维",
                "description": "系统性综合思考",
                "keywords": ["系统", "要素", "关系", "整体"],
                "process": ["要素识别", "关系分析", "系统优化"],
                "applications": ["系统设计", "流程优化", "组织变革"],
            },
            "zonghe_tigao": {
                "title": "综合提高思维",
                "description": "持续改进的思维方法",
                "keywords": ["提高", "改进", "优化", "创新"],
                "process": ["现状分析", "目标设定", "持续改进"],
                "applications": ["绩效提升", "质量管理", "个人成长"],
            },
            "liyun_sendu": {
                "title": "理一分殊思维",
                "description": "普遍与特殊的关系思维",
                "keywords": ["理一", "分殊", "普遍性", "特殊性"],
                "process": ["认识普遍", "区分特殊", "灵活应用"],
                "applications": ["理论应用", "文化适应", "战略调整"],
            },
            "liyun_principled": {
                "title": "理一原则思维",
                "description": "坚持原则的思维方法",
                "keywords": ["原则", "底线", "坚持", "灵活"],
                "process": ["明确原则", "坚持底线", "灵活变通"],
                "applications": ["道德决策", "商业伦理", "个人品格"],
            },
            "liyun_integration": {
                "title": "殊途同归思维",
                "description": "多种路径达到目标",
                "keywords": ["殊途", "同归", "变通", "目标"],
                "process": ["明确目标", "探索路径", "殊途同归"],
                "applications": ["问题解决", "创新方法", "路径规划"],
            },
            "mencius_xin": {
                "title": "孟子心性思维",
                "description": "心性修养的思维方法",
                "keywords": ["性善", "四端", "养心", "寡欲"],
                "process": ["认识本心", "培养四端", "养心寡欲"],
                "applications": ["道德修养", "情绪管理", "人格完善"],
            },
            "mingjia_synthesis": {
                "title": "名家综合思维",
                "description": "综合分析的思维方法",
                "keywords": ["综合", "分析", "归纳", "演绎"],
                "process": ["收集信息", "综合分析", "得出结论"],
                "applications": ["研究分析", "决策支持", "方案评估"],
            },
            "guanliu_ziran": {
                "title": "观流自然思维",
                "description": "观察趋势的思维方法",
                "keywords": ["观察", "趋势", "规律", "预判"],
                "process": ["观察现象", "分析趋势", "预判未来"],
                "applications": ["市场分析", "趋势预测", "战略规划"],
            },
            "yijing_guaxiang": {
                "title": "易经卦象思维",
                "description": "象数思维的智慧",
                "keywords": ["卦象", "象数理", "变化", "规律"],
                "process": ["观察现象", "分析卦象", "理解变化"],
                "applications": ["决策分析", "风险管理", "人生规划"],
            },
            "yijing_bianhua": {
                "title": "易经变化思维",
                "description": "变化发展的辩证思维",
                "keywords": ["变化", "发展", "辩证", "动态"],
                "process": ["认识变化", "把握规律", "顺势而为"],
                "applications": ["战略调整", "危机应对", "创新突破"],
            },
            "wuxing_tuidao": {
                "title": "五行推道思维",
                "description": "五行相生相克的分析思维",
                "keywords": ["五行", "相生", "相克", "平衡"],
                "process": ["分析要素", "把握关系", "寻求平衡"],
                "applications": ["关系分析", "资源配置", "系统平衡"],
            },
            "taiji_shunei": {
                "title": "太极顺势思维",
                "description": "阴阳变化的顺势思维",
                "keywords": ["阴阳", "变化", "顺势", "平衡"],
                "process": ["认识阴阳", "把握变化", "顺势而为"],
                "applications": ["战略规划", "危机处理", "人生智慧"],
            },
            "taiji_yangsheng": {
                "title": "太极养生思维",
                "description": "身心和谐的养生思维",
                "keywords": ["阴阳平衡", "动静结合", "和谐"],
                "process": ["调和阴阳", "动静结合", "身心和谐"],
                "applications": ["健康管理", "压力调节", "生活方式"],
            },
            "xinfaxitong": {
                "title": "心法百变思维",
                "description": "灵活运用的思维方法",
                "keywords": ["灵活", "变通", "创新", "适应"],
                "process": ["理解原理", "灵活应用", "创新变通"],
                "applications": ["问题解决", "创新突破", "适应变化"],
            },
            "baojia_mingtian": {
                "title": "百家明天思维",
                "description": "百家争鸣的开放思维",
                "keywords": ["开放", "包容", "创新", "多元"],
                "process": ["开放心态", "包容观点", "创新思考"],
                "applications": ["学术研究", "团队讨论", "创新思考"],
            },
        }

    def analyze(self, query: str, context: Optional[Dict[str, Any]] = None) -> ThinkingMethodResult:
        """分析查询并提供思维方法建议"""
        self.query = query
        self.context = context or {}

        # 选择最佳方法
        selected_methods = self._select_methods(query, context)

        # 构建思维路径
        thinking_paths = self._build_thinking_paths(query, selected_methods)

        # 综合分析
        comprehensive = self._comprehensive_analysis(query, selected_methods, thinking_paths)

        # 深度评估
        depth_assessment = self._assess_depth(query, comprehensive)

        # 生成建议
        recommendations = self._generate_recommendations(query, comprehensive, depth_assessment)

        return ThinkingMethodResult(
            original_query=query,
            selected_methods=selected_methods,
            thinking_paths=thinking_paths,
            comprehensive_analysis=comprehensive,
            depth_assessment=depth_assessment,
            recommendations=recommendations,
            summary=self._generate_summary(query, comprehensive),
        )

    def _select_methods(self, query: str, context: Dict[str, Any]) -> List[MethodSuggestion]:
        """选择最适合的思维方法"""
        suggestions = []
        query_lower = query.lower()

        # 关键词匹配
        method_scores = {}
        for method_key, desc in self.method_descriptions.items():
            score = 0
            keywords = desc.get("keywords", [])
            for keyword in keywords:
                if keyword in query:
                    score += 2
            if score > 0:
                method_scores[method_key] = score

        # 按分数排序，取前5个
        sorted_methods = sorted(method_scores.items(), key=lambda x: x[1], reverse=True)
        if sorted_methods:
            top_methods = sorted_methods[:5]
        else:
            # 如果没有匹配，默认选择前5个方法
            top_methods = [(k, 1) for k in list(self.method_descriptions.keys())[:5]]

        for method_key, score in top_methods:
            desc = self.method_descriptions[method_key]
            suggestions.append(MethodSuggestion(
                method=method_key,
                title=desc["title"],
                description=desc["description"],
                suitability=f"匹配度: {min(score * 20, 100)}%",
                expected_outcome="深入分析，全面思考",
            ))

        return suggestions

    def _build_thinking_paths(self, query: str, methods: List[MethodSuggestion]) -> List[ThinkingPath]:
        """构建思维路径"""
        paths = []
        for i, method in enumerate(methods[:3], 1):
            desc = self.method_descriptions.get(method.method, {})
            paths.append(ThinkingPath(
                step=i,
                method=method.method,
                description=f"运用{method.title}分析",
                thinking=f"通过{desc.get('description', '该方法')}进行思考",
                outcome="形成系统化认知",
            ))
        return paths

    def _comprehensive_analysis(
        self,
        query: str,
        methods: List[MethodSuggestion],
        paths: List[ThinkingPath]
    ) -> ThinkingAnalysis:
        """综合分析"""
        method_names = [m.title for m in methods]
        all_keywords = []
        all_process = []
        all_applications = []

        for method in methods:
            desc = self.method_descriptions.get(method.method, {})
            all_keywords.extend(desc.get("keywords", []))
            all_process.extend(desc.get("process", []))
            all_applications.extend(desc.get("applications", []))

        return ThinkingAnalysis(
            method=",".join([m.method for m in methods]),
            title=f"基于{'/'.join(method_names)}的综合分析",
            description=f"从{len(methods)}个思维维度对问题进行全面分析",
            keywords=list(set(all_keywords))[:10],
            process=list(set(all_process))[:8],
            applications=list(set(all_applications))[:6],
            depth="deep",
            insight="通过多维度的思维方法整合，形成系统性的认知框架",
            warnings=["避免过度思考", "保持行动的勇气"],
        )

    def _assess_depth(self, query: str, analysis: ThinkingAnalysis) -> Dict[str, Any]:
        """评估思维深度"""
        query_depth_score = min(len(query) / 20, 1.0)
        keyword_depth_score = len(analysis.keywords) / 10

        return {
            "surface_score": max(0, 1 - query_depth_score),
            "middle_score": min(0.5 + query_depth_score * 0.3, 1.0),
            "deep_score": min(0.3 + keyword_depth_score * 0.4, 1.0),
            "ultimate_score": min(keyword_depth_score * 0.3, 0.8),
            "recommended_depth": "deep",
        }

    def _generate_recommendations(
        self,
        query: str,
        analysis: ThinkingAnalysis,
        depth: Dict[str, Any]
    ) -> List[str]:
        """生成建议"""
        recommendations = [
            f"建议采用{analysis.depth}层思维方法进行深入分析",
            "结合实际情境，灵活运用多种思维方法",
            "保持开放心态，接纳不同视角的观点",
        ]

        if depth.get("deep_score", 0) > 0.5:
            recommendations.append("深入思考问题的本质和根源")

        if depth.get("ultimate_score", 0) > 0.3:
            recommendations.append("探索更高层次的智慧和洞见")

        return recommendations

    def _generate_summary(self, query: str, analysis: ThinkingAnalysis) -> str:
        """生成总结"""
        return f"通过对'{query}'的多维度分析，建议运用{analysis.depth}层思维方法，结合{', '.join(analysis.applications[:3])}等方式，形成系统性的认知和行动方案。"

def analyze_thinking_method(query: str, context: Optional[Dict[str, Any]] = None) -> ThinkingMethodResult:
    """便捷函数：分析思维方法"""
    engine = ThinkingMethodEngine()
    return engine.analyze(query, context)

class ThinkingMethodFusionEngine:
    """
    思维方法融合引擎 - 兼容占位类
    
    注: 原始 ThinkingMethodFusionEngine 类需要从 thinking_method_engine 子包中导入。
    当前版本提供基础思维方法分析功能。
    """

    def __init__(self):
        self.engine = ThinkingMethodEngine()

    def analyze(self, query: str, context: Optional[Dict[str, Any]] = None) -> ThinkingMethodResult:
        """分析查询并提供思维方法建议"""
        return self.engine.analyze(query, context)

    def select_method(self, query: str, context: Optional[Dict[str, Any]] = None) -> MethodSuggestion:
        """选择最佳思维方法"""
        result = self.engine.analyze(query, context)
        if result.selected_methods:
            return result.selected_methods[0]
        return MethodSuggestion(
            method="yangming_xinxue",
            title="王阳明心学思维",
            description="知行合一的思维方法",
            suitability="默认选择",
            expected_outcome="形成系统认知",
        )
