"""
__all__ = [
    'analyze',
    'enhance_reasoning',
    'fuse_with_humanities',
    'get_frontier_problems',
    'get_scale_ladder',
    'get_scale_perspective',
    'get_statistics',
    'get_system_info',
    'get_unified_principles',
    'query',
]

自然科学unified入口模块 v1.0.1 (v8.4.3 修复版)
Natural Science Unified Entry Module

整合三大自然科学智慧模块 + 跨尺度unified思维引擎,
提供unified的自然科知识查询,分析和decision支持接口.

模块:
- NaturalScienceWisdomCore: 物理,化学(v8.4.3 已移除,由 natural_science_unified 独立实现)
- LifeScienceWisdomCore: 生物学(v8.4.3 已移除)
- EarthCosmosWisdomEngine: 地球与宇宙(v8.4.3 已移除)
- CrossScaleThinkingEngine: 跨尺度unified(cross_scale_thinking_engine.py)

知识来源:<自然科学全景深度研究报告>v2.0 博士生级
涵盖:从普朗克长度到可观测宇宙,62个数量级的完整科学图景

版本:v1.0.1 (v8.4.3 修复版)
日期:2026-04-03
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

logger = logging.getLogger(__name__)

class ScienceDomain(Enum):
    """自然科学领域枚举"""
    PHYSICS = "physics"              # 物理学
    CHEMISTRY = "chemistry"          # 化学
    QUANTUM = "quantum"              # 量子物理
    THERMODYNAMICS = "thermodynamics"  # 热力学与统计物理
    RELATIVITY = "relativity"        # 相对论
    PARTICLE = "particle"            # 粒子物理
    MOLECULAR_BIO = "molecular_bio"  # 分子生物学
    EVOLUTION = "evolution"          # 演化生物学
    ECOLOGY = "ecology"              # 生态学
    GENOMICS = "genomics"            # 基因组学
    NEUROSCIENCE = "neuroscience"    # 神经科学
    GEOLOGY = "geology"              # 地质学
    ATMOSPHERE = "atmosphere"        # 大气科学
    OCEANOGRAPHY = "oceanography"    # 海洋学
    COSMOLOGY = "cosmology"          # 宇宙学
    ASTROPHYSICS = "astrophysics"    # 天体物理
    CROSS_SCALE = "cross_scale"      # 跨尺度unified
    COMPLEX_SYSTEM = "complex_system"  # 复杂系统
    INFORMATION = "information"      # 信息论

class NaturalScienceUnified:
    """自然科学智慧unified入口 v1.0.1 (v8.4.3 修复版)"""

    VERSION = "6.2.0"
    DESCRIPTION = "自然科学智慧unified系统 - 从量子到宇宙的全谱系知识引擎"

    def __init__(self):
        """init:加载核心模块(v8.4.3 使用 try-except 处理已删除模块)"""
        # v8.4.3 修复:使用 importlib 进action态导入
        import importlib
        
        self.physics_core = None
        self.life_core = None
        self.earth_cosmos_core = None
        self.cross_scale_engine = None
        package_name = __package__ or 'src.intelligence'
        
        try:
            natural_science_module = importlib.import_module('.natural_science_wisdom_core', package=package_name)
            NaturalScienceWisdomCore = getattr(natural_science_module, 'NaturalScienceWisdomCore')
            self.physics_core = NaturalScienceWisdomCore()
            logger.info("[自然科学] 物理与化学核心模块加载成功")
        except (ImportError, AttributeError) as e:
            logger.warning(f"[自然科学] 物理与化学核心模块加载失败(已移除): {e}")

        try:
            life_science_module = importlib.import_module('.life_science_wisdom_core', package=package_name)
            LifeScienceWisdomCore = getattr(life_science_module, 'LifeScienceWisdomCore')
            self.life_core = LifeScienceWisdomCore()
            logger.info("[自然科学] 生命科学核心模块加载成功")
        except (ImportError, AttributeError) as e:
            logger.warning(f"[自然科学] 生命科学核心模块加载失败(已移除): {e}")

        try:
            earth_cosmos_module = importlib.import_module('.earth_cosmos_wisdom_core', package=package_name)
            EarthCosmosWisdomEngine = getattr(earth_cosmos_module, 'EarthCosmosWisdomEngine')
            self.earth_cosmos_core = EarthCosmosWisdomEngine()
            logger.info("[自然科学] 地球与宇宙核心模块加载成功")
        except (ImportError, AttributeError) as e:
            logger.warning(f"[自然科学] 地球与宇宙核心模块加载失败(已移除): {e}")

        try:
            from .cross_scale_thinking_engine import CrossScaleThinkingEngine
            self.cross_scale_engine = CrossScaleThinkingEngine()
            logger.info("[自然科学] 跨尺度unified思维引擎加载成功")
        except (ImportError, AttributeError) as e:
            logger.warning(f"[自然科学] 跨尺度unified思维引擎加载失败: {e}")

        self._domain_router = self._build_domain_router()

    def _build_domain_router(self) -> Dict[str, Any]:
        """构建领域路由表"""
        router = {}
        if self.physics_core:
            router.update({
                ScienceDomain.PHYSICS: self.physics_core,
                ScienceDomain.CHEMISTRY: self.physics_core,
                ScienceDomain.QUANTUM: self.physics_core,
                ScienceDomain.THERMODYNAMICS: self.physics_core,
                ScienceDomain.RELATIVITY: self.physics_core,
                ScienceDomain.PARTICLE: self.physics_core,
            })
        if self.life_core:
            router.update({
                ScienceDomain.MOLECULAR_BIO: self.life_core,
                ScienceDomain.EVOLUTION: self.life_core,
                ScienceDomain.ECOLOGY: self.life_core,
                ScienceDomain.GENOMICS: self.life_core,
                ScienceDomain.NEUROSCIENCE: self.life_core,
            })
        if self.earth_cosmos_core:
            router.update({
                ScienceDomain.GEOLOGY: self.earth_cosmos_core,
                ScienceDomain.ATMOSPHERE: self.earth_cosmos_core,
                ScienceDomain.OCEANOGRAPHY: self.earth_cosmos_core,
                ScienceDomain.COSMOLOGY: self.earth_cosmos_core,
                ScienceDomain.ASTROPHYSICS: self.earth_cosmos_core,
            })
        if self.cross_scale_engine:
            router.update({
                ScienceDomain.CROSS_SCALE: self.cross_scale_engine,
                ScienceDomain.COMPLEX_SYSTEM: self.cross_scale_engine,
                ScienceDomain.INFORMATION: self.cross_scale_engine,
            })
        return router

    # ==================== 核心unified接口 ====================

    def query(self, question: str, domains: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        unified知识查询接口

        Args:
            question: 自然语言问题
            domains: 指定领域列表(可选),不指定则自动路由

        Returns:
            {
                "answer": str,          # 回答内容
                "domain": str,          # 路由到的领域
                "confidence": float,    # 置信度
                "sources": list,        # 知识来源
                "related_concepts": list  # 相关概念
            }
        """
        if not domains:
            domains = self._auto_route(question)

        all_results = []
        for domain_str in domains:
            try:
                domain = ScienceDomain(domain_str)
                handler = self._domain_router.get(domain)
                if handler:
                    # Adapt to different module interfaces
                    if hasattr(handler, 'query'):
                        result = handler.query(question, domain_str)
                    elif hasattr(handler, 'analyze'):
                        raw = handler.analyze(question)
                        # Normalize return format
                        if isinstance(raw, dict):
                            if 'answer' not in raw:
                                raw['answer'] = str(raw.get('analysis', raw.get('summary', str(raw)[:300])))
                            if 'domain' not in raw:
                                raw['domain'] = domain_str
                            if 'confidence' not in raw:
                                raw['confidence'] = 0.6
                            if 'sources' not in raw:
                                raw['sources'] = []
                            if 'related_concepts' not in raw:
                                raw['related_concepts'] = []
                            result = raw
                        else:
                            result = {
                                "answer": str(raw)[:300],
                                "domain": domain_str,
                                "confidence": 0.4,
                                "sources": [],
                                "related_concepts": []
                            }
                    else:
                        result = {
                            "answer": str(handler)[:200],
                            "domain": domain_str,
                            "confidence": 0.3,
                            "sources": [],
                            "related_concepts": []
                        }
                    all_results.append(result)
            except (ValueError, AttributeError) as e:
                logger.warning(f"[自然科学] 领域查询失败: {domain_str}: {e}")

        if not all_results:
            return {
                "answer": f"暂未覆盖该自然科学领域的问题:{question}",
                "domain": "unknown",
                "confidence": 0.0,
                "sources": [],
                "related_concepts": []
            }

        # 合并多个结果
        best = max(all_results, key=lambda x: x.get("confidence", 0))
        if len(all_results) > 1:
            best["answer"] = self._merge_answers(all_results)
            best["cross_domain"] = True

        return best

    def analyze(self, topic: str, depth: str = "standard") -> Dict[str, Any]:
        """
        深度分析接口

        Args:
            topic: 分析主题
            depth: 分析深度 ("basic" / "standard" / "deep")

        Returns:
            完整分析报告
        """
        domains = self._auto_route(topic)
        results = {}

        for domain_str in domains:
            try:
                domain = ScienceDomain(domain_str)
                handler = self._domain_router.get(domain)
                if handler and hasattr(handler, 'analyze'):
                    results[domain_str] = handler.analyze(topic, depth)
            except (ValueError, AttributeError):
                pass

        # 跨尺度整合分析
        cross_result = None
        if self.cross_scale_engine and len(results) > 1:
            if hasattr(self.cross_scale_engine, 'integrate_across_scales'):
                cross_result = self.cross_scale_engine.integrate_across_scales(topic, results)
            else:
                cross_result = {
                    "type": "cross_scale_integration",
                    "topic": topic,
                    "summary": f"从{len(results)}个领域对'{topic}'进行跨尺度分析",
                }

        return {
            "topic": topic,
            "depth": depth,
            "domain_analyses": results,
            "cross_scale_integration": cross_result,
            "total_domains_analyzed": len(results),
            "version": self.VERSION
        }

    def get_scale_perspective(self, scale_m: float) -> Dict[str, Any]:
        """
        尺度透视:给定一个物理尺度,返回该尺度下的主导物理学
        """
        if self.cross_scale_engine:
            if hasattr(self.cross_scale_engine, 'analyze_scale'):
                return self.cross_scale_engine.analyze_scale(scale_m)
            elif hasattr(self.cross_scale_engine, 'get_perspective_on_scale'):
                return self.cross_scale_engine.get_perspective_on_scale(str(scale_m))
        return {"error": "跨尺度引擎未加载", "scale": scale_m}

    def get_unified_principles(self) -> Dict[str, Any]:
        """get自然科学unified原理"""
        if self.cross_scale_engine and hasattr(self.cross_scale_engine, 'get_unified_principles'):
            return self.cross_scale_engine.get_unified_principles()
        # Fallback: return built-in principles
        return {
            "principles": [
                "还原论与涌现性的辩证unified",
                "信息作为跨尺度通用货币",
                "对称性破缺与有序结构generate",
                "能量最低原理与稳定性",
                "临界现象与普适性",
            ],
            "source": "自然科学unified系统内置"
        }

    def get_scale_ladder(self) -> List[Dict[str, Any]]:
        """get完整的物质尺度阶梯"""
        if self.cross_scale_engine and hasattr(self.cross_scale_engine, 'get_scale_ladder'):
            return self.cross_scale_engine.get_scale_ladder()
        # Fallback: return built-in scale data
        return [
            {"name": "普朗克长度", "scale_m": 1.6e-35, "domain": "量子引力"},
            {"name": "原子核", "scale_m": 1e-15, "domain": "核物理"},
            {"name": "原子", "scale_m": 1e-10, "domain": "原子物理"},
            {"name": "分子/DNA", "scale_m": 1e-9, "domain": "化学/分子生物学"},
            {"name": "病毒", "scale_m": 1e-7, "domain": "微生物学"},
            {"name": "细胞", "scale_m": 1e-5, "domain": "细胞生物学"},
            {"name": "人类", "scale_m": 1.7, "domain": "宏观生物"},
            {"name": "地球", "scale_m": 1.27e7, "domain": "地球科学"},
            {"name": "太阳系", "scale_m": 9e12, "domain": "行星科学"},
            {"name": "太阳", "scale_m": 1.4e9, "domain": "恒星物理"},
            {"name": "银河系", "scale_m": 9.5e20, "domain": "天体物理"},
            {"name": "可观测宇宙", "scale_m": 8.8e26, "domain": "宇宙学"},
        ]

    def get_frontier_problems(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """get前沿未解问题"""
        problems = {}

        physics_domains = ["physics", "chemistry", "quantum", "thermodynamics", "relativity", "particle"]
        life_domains = ["molecular_bio", "evolution", "ecology", "genomics", "neuroscience"]
        earth_domains = ["geology", "atmosphere", "oceanography", "cosmology", "astrophysics"]
        cross_domains = ["cross_scale", "complex_system", "information"]

        if self.physics_core and (domain is None or domain in physics_domains):
            if hasattr(self.physics_core, 'get_frontier_problems'):
                problems["physics"] = self.physics_core.get_frontier_problems()
            else:
                problems["physics"] = ["量子引力", "暗物质本质", "物质-反物质不对称", "中微子质量起源"]

        if self.life_core and (domain is None or domain in life_domains):
            if hasattr(self.life_core, 'get_frontier_problems'):
                problems["life_science"] = self.life_core.get_frontier_problems()
            else:
                problems["life_science"] = ["生命起源", "意识困难问题", "蛋白质折叠问题", "人类加速演化之谜"]

        if self.earth_cosmos_core and (domain is None or domain in earth_domains):
            if hasattr(self.earth_cosmos_core, 'get_frontier_problems'):
                problems["earth_cosmos"] = self.earth_cosmos_core.get_frontier_problems()
            else:
                problems["earth_cosmos"] = ["哈勃常数张力", "暗能量本质", "太阳中微子问题", "板块构造启动机制"]

        if self.cross_scale_engine and (domain is None or domain in cross_domains):
            if hasattr(self.cross_scale_engine, 'get_frontier_problems'):
                problems["cross_scale"] = self.cross_scale_engine.get_frontier_problems()
            else:
                problems["cross_scale"] = ["涌现的严格定义", "复杂系统的普适定律", "生命的信息论本质"]

        return problems

    # ==================== 智慧fusion接口 ====================

    def fuse_with_humanities(self, science_concept: str,
                             humanities_wisdom: Dict[str, Any]) -> Dict[str, Any]:
        """
        自然科学与人文智慧fusion

        Args:
            science_concept: 自然科学概念
            humanities_wisdom: 人文智慧(来自儒释道等模块)

        Returns:
            fusion后的智慧洞察
        """
        science_perspective = self.query(science_concept)

        insights = []

        # 尺度思维注入
        if self.cross_scale_engine:
            if hasattr(self.cross_scale_engine, 'get_scale_perspective_for_concept'):
                scale_insight = self.cross_scale_engine.get_scale_perspective_for_concept(
                    science_concept
                )
            else:
                scale_insight = f"跨尺度视角:{science_concept} 涉及从微观到宏观的多层次相互作用"
            if scale_insight:
                insights.append({
                    "type": "scale_thinking",
                    "content": scale_insight
                })

        # unified原理注入
        principles = self.get_unified_principles()
        if principles:
            insights.append({
                "type": "unified_principles",
                "content": principles
            })

        return {
            "science_concept": science_concept,
            "science_perspective": science_perspective,
            "humanities_wisdom": humanities_wisdom,
            "fusion_insights": insights,
            "fusion_quality": self._evaluate_fusion_quality(science_perspective, humanities_wisdom)
        }

    def enhance_reasoning(self, reasoning_chain: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        用自然科学知识增强推理链

        Args:
            reasoning_chain: 推理链(步骤列表)

        Returns:
            增强后的推理链
        """
        enhanced = []

        for step in reasoning_chain:
            content = step.get("content", "") if isinstance(step, dict) else str(step)

            # 为每个推理步骤寻找科学支撑
            science_support = None
            domains = self._auto_route(content)
            for domain_str in domains:
                try:
                    domain = ScienceDomain(domain_str)
                    handler = self._domain_router.get(domain)
                    if handler and hasattr(handler, 'get_evidence_for_claim'):
                        evidence = handler.get_evidence_for_claim(content)
                        if evidence and evidence.get("confidence", 0) > 0.5:
                            science_support = evidence
                            break
                    elif handler and hasattr(handler, 'analyze'):
                        analysis = handler.analyze(content)
                        if analysis:
                            science_support = {
                                "domain": domain_str,
                                "confidence": 0.5,
                                "analysis": analysis
                            }
                            break
                except (ValueError, AttributeError):
                    pass

            enhanced_step = dict(step) if isinstance(step, dict) else {"content": step}
            if science_support:
                enhanced_step["science_support"] = science_support
            enhanced.append(enhanced_step)

        return enhanced

    # ==================== 辅助方法 ====================

    def _auto_route(self, question: str) -> List[str]:
        """
        自动路由:根据问题关键词judge应查询的领域

        Returns:
            领域列表(按相关性排序)
        """
        q = question.lower()
        scores = {}

        # 物理关键词
        physics_kw = ["量子", "相对论", "引力", "电磁", "粒子", "原子", "分子",
                      "热力学", "熵", "力", "能量", "动量", "波", "场", "希格斯",
                      "标准模型", "夸克", "轻子", "规范", "对称性", "暗物质", "暗能量",
                      "普朗克", "薛定谔", "海森堡", "不确定性", "纠缠", "叠加",
                      "physics", "quantum", "relativity", "gravity", "particle",
                      "thermodynamics", "entropy", "entanglement"]
        for kw in physics_kw:
            if kw in q:
                scores[ScienceDomain.PHYSICS.value] = scores.get(ScienceDomain.PHYSICS.value, 0) + 1

        # 化学关键词
        chemistry_kw = ["化学键", "元素", "周期表", "有机", "无机", "催化", "反应",
                        "分子式", "电子云", "轨道", "共价", "离子", "金属",
                        "chemistry", "molecule", "element", "bond", "catalysis"]
        for kw in chemistry_kw:
            if kw in q:
                scores[ScienceDomain.CHEMISTRY.value] = scores.get(ScienceDomain.CHEMISTRY.value, 0) + 1

        # 生命科学关键词
        life_kw = ["细胞", "DNA", "RNA", "蛋白质", "基因", "遗传", "进化", "演化",
                    "生态", "物种", "突变", "自然选择", "基因组", "转录", "翻译",
                    "神经元", "突触", "意识", "大脑", "免疫", "病毒", "细菌",
                    "cell", "dna", "rna", "protein", "gene", "evolution", "ecology",
                    "neuron", "consciousness", "genome", "mutation"]
        for kw in life_kw:
            if kw in q:
                scores[ScienceDomain.MOLECULAR_BIO.value] = scores.get(ScienceDomain.MOLECULAR_BIO.value, 0) + 1

        # 地球科学关键词
        earth_kw = ["地球", "板块", "地震", "火山", "大气", "海洋", "气候",
                     "地质", "岩浆", "地幔", "地核", "潮汐", "洋流", "降水",
                     "温室效应", "冰河", "ocean", "atmosphere", "climate",
                     "earth", "geology", "plate", "earthquake", "volcano"]
        for kw in earth_kw:
            if kw in q:
                scores[ScienceDomain.GEOLOGY.value] = scores.get(ScienceDomain.GEOLOGY.value, 0) + 1

        # 宇宙学关键词
        cosmos_kw = ["宇宙", "星系", "恒星", "黑洞", "大爆炸", "暗物质", "暗能量",
                      "膨胀", "红移", "类星体", "脉冲星", "中子星", "超新星",
                      "太阳系", "行星", "卫星", "宇宙微波", "哈勃",
                      "universe", "galaxy", "star", "black hole", "big bang",
                      "dark matter", "dark energy", "cosmology", "supernova"]
        for kw in cosmos_kw:
            if kw in q:
                scores[ScienceDomain.COSMOLOGY.value] = scores.get(ScienceDomain.COSMOLOGY.value, 0) + 1

        # 跨尺度关键词
        cross_kw = ["涌现", "复杂性", "自组织", "混沌", "分形", "网络",
                     "信息熵", "unified", "尺度", "层级", "还原", "整体",
                     "相变", "临界", "人择", "精调",
                     "emergence", "complexity", "self-organization", "chaos",
                     "fractal", "scale", "information"]
        for kw in cross_kw:
            if kw in q:
                scores[ScienceDomain.CROSS_SCALE.value] = scores.get(ScienceDomain.CROSS_SCALE.value, 0) + 1

        # 排序返回
        sorted_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [d[0] for d in sorted_domains] if sorted_domains else ["physics"]

    def _merge_answers(self, results: List[Dict[str, Any]]) -> str:
        """合并多个领域的回答"""
        answers = []
        domains = []
        for r in results:
            domain = r.get("domain", "未知")
            answer = r.get("answer", "")
            if answer:
                domains.append(domain)
                answers.append(f"[{domain}视角]{answer}")

        merged = "\n\n".join(answers)
        if self.cross_scale_engine:
            if hasattr(self.cross_scale_engine, 'synthesize_multi_domain'):
                insight = self.cross_scale_engine.synthesize_multi_domain(merged)
            else:
                domain_text = ",".join(dict.fromkeys(domains)) or "多个领域"
                insight = f"跨尺度整合:以上分析共同说明该问题需要同时从{domain_text}等尺度与机制层面理解."
            if insight:
                merged += f"\n\n[跨尺度整合]{insight}"
        return merged

    def _evaluate_fusion_quality(self, science: Dict, humanities: Dict) -> float:
        """评估fusion质量"""
        score = 0.5  # 基础分
        if science.get("confidence", 0) > 0.7:
            score += 0.2
        if humanities.get("confidence", 0) > 0.7:
            score += 0.2
        if science.get("cross_domain"):
            score += 0.1
        return min(score, 1.0)

    def get_system_info(self) -> Dict[str, Any]:
        """get系统信息"""
        total = sum(1 for v in [
            self.physics_core, self.life_core,
            self.earth_cosmos_core, self.cross_scale_engine
        ] if v is not None)
        return {
            "name": "自然科学智慧unified系统",
            "version": self.VERSION,
            "description": self.DESCRIPTION,
            "modules": {
                "physics_core": self.physics_core is not None,
                "life_core": self.life_core is not None,
                "earth_cosmos_core": self.earth_cosmos_core is not None,
                "cross_scale_engine": self.cross_scale_engine is not None,
            },
            "domains_supported": [d.value for d in self._domain_router.keys()],
            "knowledge_source": "自然科学全景深度研究报告 v2.0 博士生级",
            "scale_range": "10^-35 m (普朗克长度) ~ 10^27 m (可观测宇宙)",
            "total_orders_of_magnitude": 62,
            "total_modules": total,
        }

    def get_statistics(self) -> Dict[str, Any]:
        """get系统统计"""
        stats = {
            "total_modules": sum(1 for v in [
                self.physics_core, self.life_core,
                self.earth_cosmos_core, self.cross_scale_engine
            ] if v is not None),
            "total_domains": len(self._domain_router),
            "domain_list": [d.value for d in self._domain_router.keys()],
        }

        if self.physics_core:
            stats["physics_concepts"] = len(getattr(self.physics_core, '_knowledge_base', {}))
        if self.life_core:
            stats["life_concepts"] = len(getattr(self.life_core, '_knowledge_base', {}))
        if self.earth_cosmos_core:
            stats["earth_cosmos_concepts"] = len(getattr(self.earth_cosmos_core, '_knowledge_base', {}))

        return stats
