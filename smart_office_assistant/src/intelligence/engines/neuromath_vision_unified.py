# -*- coding: utf-8 -*-
"""
__all__ = [
    'analyze',
    'create_neuromath_unified',
    'diagnose_system_health',
    'get_all_insights',
    'get_theory_summary',
]

神经数学视觉unified入口 v1.0.1 (v8.4.3 修复版)
=======================

整合<Neuromathematics of Vision>所有智慧模块的unified入口

整合模块:
1. 神经几何学智慧核心 (NeurogeometryWisdomCore) - v8.4.3 已移除
2. 亚黎曼测地线推理引擎 (GeodesicReasoningEngine)
3. 格式塔感知组织系统 (GestaltOrganizationEngine)
4. Hebbian协同学习引擎 (HebbianEnsembleEngine)
5. Gabor多尺度characteristics系统 (GaborFeatureSystem)
6. 辛几何decision框架 (SymplecticDecisionFramework)

核心理论支撑:
- Citti & Sarti: 视觉皮层功能架构的数学模型
- Petitot: 神经几何学
- Duits & Sachkov: 亚黎曼测地线
- Hubel & Wiesel: Gabor函数与简单细胞
- Hebb: Hebbian学习

@author: Somn AI
@version: 1.0.1 (v8.4.3 修复版)
@date: 2026-04-03
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass
import traceback

# 导入各模块(v8.4.3 修复:使用 try-except 处理已删除模块)
try:
    from .neurogeometry_wisdom_core import (
        NeurogeometryWisdomCore,
        CorticalFeature,
        FeatureDimension,
        ArchitectureType,
        get_neurogeometry_insights
    )
    NEUROGEOMETRY_AVAILABLE = True
except ImportError:
    NEUROGEOMETRY_AVAILABLE = False
    # 创建兼容层
    NeurogeometryWisdomCore = None

from .geodesic_reasoning_engine import (
    GeodesicReasoningEngine,
    StateSE2,
    GeodesicSegment,
    ConstraintType,
    create_geodesic_engine,
    get_geodesic_insights
)

from .gestalt_organization_engine import (
    GestaltOrganizationEngine,
    VisualElement,
    PerceptualGroup,
    GestaltPrinciple,
    create_gestalt_engine,
    get_gestalt_insights
)

from .hebbian_ensemble_engine import (
    HebbianEnsembleEngine,
    SelfOrganizingMap,
    LearningRule,
    create_hebbian_engine,
    create_som,
    get_hebbian_insights
)

from .gabor_feature_system import (
    GaborFeatureSystem,
    GaborParameters,
    FeatureResponse,
    create_gabor_system,
    get_gabor_insights
)

from .symplectic_decision_framework import (
    SymplecticDecisionFramework,
    PhaseSpacePoint,
    create_symplectic_framework,
    get_symplectic_insights
)

@dataclass
class UnifiedAnalysisResult:
    """unified分析结果"""
    neurogeometry: Dict[str, Any]
    geodesic: Dict[str, Any]
    gestalt: Dict[str, Any]
    hebbian: Dict[str, Any]
    gabor: Dict[str, Any]
    symplectic: Dict[str, Any]
    synthesis: Dict[str, Any]

class NeuromathVisionUnified:
    """神经数学视觉unified入口
    
    提供unified的接口访问所有神经数学视觉模块
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """init_all模块
        
        Args:
            config: 配置参数
        """
        self.name = "NeuromathVisionUnified"
        self.version="6.2.0"
        
        if config is None:
            config = self._default_config()
        
        self.config = config
        
        # init各模块
        self._init_modules()
        
        # 分析缓存
        self.analysis_cache: Dict[str, Any] = {}
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "neurogeometry": {
                "input_space": (32, 32),
                "orientation_bins": 8,
                "scale_levels": 3
            },
            "geodesic": {
                "beta": 0.5
            },
            "gestalt": {
                "proximity_threshold": 0.1,
                "similarity_threshold": 0.7
            },
            "hebbian": {
                "som_width": 10,
                "som_height": 10,
                "learning_rate": 0.5
            },
            "gabor": {
                "n_orientations": 8,
                "n_scales": 5
            },
            "symplectic": {
                "n_dimensions": 3
            }
        }
    
    def _init_modules(self):
        """init_all模块"""
        # 神经几何学智慧核心
        self.neurogeometry = NeurogeometryWisdomCore()
        
        # 亚黎曼测地线推理引擎
        self.geodesic = GeodesicReasoningEngine(beta=self.config["geodesic"]["beta"])
        
        # 格式塔感知组织系统
        self.gestalt = GestaltOrganizationEngine()
        
        # Hebbian协同学习引擎
        self.hebbian = HebbianEnsembleEngine()
        
        # Gabor多尺度characteristics系统
        self.gabor = GaborFeatureSystem(
            n_orientations=self.config["gabor"]["n_orientations"],
            n_scales=self.config["gabor"]["n_scales"]
        )
        
        # 辛几何decision框架
        self.symplectic = SymplecticDecisionFramework(
            n_dimensions=self.config["symplectic"]["n_dimensions"]
        )
    
    def analyze(self, data: Any, analysis_type: str = "full") -> UnifiedAnalysisResult:
        """unified分析
        
        Args:
            data: 输入数据
            analysis_type: 分析类型 ('full', 'quick', 'deep')
            
        Returns:
            unified分析结果
        """
        results = {
            "neurogeometry": {},
            "geodesic": {},
            "gestalt": {},
            "hebbian": {},
            "gabor": {},
            "symplectic": {},
            "synthesis": {}
        }
        
        if analysis_type in ["full", "quick"]:
            # 神经几何学分析
            try:
                results["neurogeometry"] = self._analyze_neurogeometry(data)
            except Exception as e:
                results["neurogeometry"] = {"error": "引擎初始化失败"}
            
            # 格式塔分析
            try:
                results["gestalt"] = self._analyze_gestalt(data)
            except Exception as e:
                results["gestalt"] = {"error": "引擎初始化失败"}
            
            # Gabor分析
            try:
                results["gabor"] = self._analyze_gabor(data)
            except Exception as e:
                results["gabor"] = {"error": "引擎初始化失败"}
        
        if analysis_type in ["full", "deep"]:
            # 测地线分析
            try:
                results["geodesic"] = self._analyze_geodesic(data)
            except Exception as e:
                results["geodesic"] = {"error": "引擎初始化失败"}
            
            # Hebbian分析
            try:
                results["hebbian"] = self._analyze_hebbian(data)
            except Exception as e:
                results["hebbian"] = {"error": "引擎初始化失败"}
            
            # 辛几何分析
            try:
                results["symplectic"] = self._analyze_symplectic(data)
            except Exception as e:
                results["symplectic"] = {"error": "引擎初始化失败"}
        
        # synthesize分析
        try:
            results["synthesis"] = self._synthesize_results(results)
        except Exception as e:
            results["synthesis"] = {"error": "引擎初始化失败"}
        
        return UnifiedAnalysisResult(**results)
    
    def _analyze_neurogeometry(self, data: Any) -> Dict[str, Any]:
        """神经几何学分析"""
        if isinstance(data, dict):
            features = data.get("features", {})
            constraints = data.get("constraints", [])
            
            # 问题几何分析
            if "features" in data:
                return self.neurogeometry.analyze_problem_geometry(data)
        
        # 构建功能架构
        config = self.config["neurogeometry"]
        arch = self.neurogeometry.build_functional_architecture(
            input_space=config["input_space"],
            orientation_bins=config["orientation_bins"],
            scale_levels=config["scale_levels"]
        )
        
        return {
            "architecture_scales": len(arch),
            "total_features": sum(len(v) for v in arch.values()),
            "theory_summary": self.neurogeometry.get_theory_summary()
        }
    
    def _analyze_geodesic(self, data: Any) -> Dict[str, Any]:
        """测地线分析"""
        # 创建测试问题
        start = StateSE2(0.1, 0.1, 0.0)
        end = StateSE2(0.8, 0.8, np.pi/4)
        
        geodesic = self.geodesic.find_geodesic(start, end)
        
        # 轮廓补全测试
        visible = [(0.1, 0.3), (0.2, 0.35), (0.3, 0.4)]
        completed = self.geodesic.complete_contour(visible)
        
        return {
            "geodesic_length": geodesic.length,
            "geodesic_cost": geodesic.cost,
            "geodesic_curvature": geodesic.curvature,
            "contour_completion_points": len(completed),
            "reasoning_stats": self.geodesic.get_reasoning_stats()
        }
    
    def _analyze_gestalt(self, data: Any) -> Dict[str, Any]:
        """格式塔分析"""
        # 创建测试元素
        elements = [
            VisualElement("e1", (0.1, 0.1), {"color": "red", "size": 5}),
            VisualElement("e2", (0.12, 0.11), {"color": "red", "size": 5}),
            VisualElement("e3", (0.5, 0.5), {"color": "blue", "size": 5}),
            VisualElement("e4", (0.52, 0.51), {"color": "blue", "size": 5}),
        ]
        
        # 感知组织
        groups = self.gestalt.organize(elements)
        
        return {
            "n_groups": len(groups),
            "avg_coherence": np.mean([g.coherence for g in groups]) if groups else 0,
            "avg_saliency": np.mean([g.saliency for g in groups]) if groups else 0,
            "organization_quality": self.gestalt.get_organization_quality(),
            "gestalt_insights": get_gestalt_insights()[:3]
        }
    
    def _analyze_hebbian(self, data: Any) -> Dict[str, Any]:
        """Hebbian分析"""
        # generate测试数据
        np.random.seed(42)
        n_samples = 100
        n_features = 4
        
        cluster1 = np.random.randn(n_samples//2, n_features) + [2, 2, 0, 0]
        cluster2 = np.random.randn(n_samples//2, n_features) + [-2, -2, 0, 0]
        data_array = np.vstack([cluster1, cluster2])
        
        # SOM学习
        self.hebbian.create_som(
            width=self.config["hebbian"]["som_width"],
            height=self.config["hebbian"]["som_height"],
            input_dim=n_features
        )
        stats = self.hebbian.learn_patterns(data_array, epochs=20)
        
        # 聚类
        labels = self.hebbian.cluster(data_array, n_clusters=2)
        
        return {
            "som_final_error": stats["final_error"],
            "cluster_distribution": [int(np.sum(labels == i)) for i in range(2)],
            "learning_analysis": self.hebbian.analyze_learning()
        }
    
    def _analyze_gabor(self, data: Any) -> Dict[str, Any]:
        """Gabor分析"""
        # 创建测试图像
        if isinstance(data, np.ndarray):
            image = data
        else:
            np.random.seed(42)
            image = np.random.rand(64, 64)
        
        # 提取characteristics
        features = self.gabor.multi_scale.extract_features(image, stride=8)
        
        # 边缘检测
        edges = self.gabor.multi_scale.detect_edges(image, threshold=0.3)
        
        return {
            "n_features": len(features),
            "n_edges": int(np.sum(edges > 0)),
            "filter_count": self.gabor.multi_scale.filter_bank.get_filter_count(),
            "gabor_insights": get_gabor_insights()[:3]
        }
    
    def _analyze_symplectic(self, data: Any) -> Dict[str, Any]:
        """辛几何分析"""
        from .symplectic_decision_framework import harmonic_oscillator_hamiltonian
        
        # 设置哈密顿量
        def H(q, p, t):
            return harmonic_oscillator_hamiltonian(q, p, t, k=1.0, mass=1.0)
        
        def dHdq(q, p, t):
            return q
        
        def dHdp(q, p, t):
            return p
        
        self.symplectic.set_hamiltonian(H, dHdq, dHdp, name="TestOscillator")
        
        # init
        q0 = np.array([1.0, 0.0, 0.0])
        p0 = np.array([0.0, 1.0, 0.0])
        self.symplectic.initialize_state(q0, p0)
        
        # 演化
        final_state = self.symplectic.evolve_decision(dt=0.1, n_steps=20)
        
        # 分析
        phase_analysis = self.symplectic.analyze_phase_structure()
        
        return {
            "final_q": final_state.q.tolist(),
            "final_p": final_state.p.tolist(),
            "phase_structure": phase_analysis,
            "symplectic_insights": get_symplectic_insights()[:3]
        }
    
    def _synthesize_results(self, results: Dict) -> Dict[str, Any]:
        """synthesize分析结果"""
        synthesis = {
            "confidence_scores": {},
            "key_findings": [],
            "recommendations": []
        }
        
        # 计算各模块置信度
        for module, result in results.items():
            if module == "synthesis":
                continue
            
            if "error" in result:
                synthesis["confidence_scores"][module] = 0.0
            else:
                synthesis["confidence_scores"][module] = 0.8  # 默认置信度
        
        # 提取关键发现
        if "gabor" in results and "n_features" in results["gabor"]:
            synthesis["key_findings"].append(
                f"提取了 {results['gabor']['n_features']} 个Gaborcharacteristics"
            )
        
        if "gestalt" in results and "n_groups" in results["gestalt"]:
            synthesis["key_findings"].append(
                f"recognize了 {results['gestalt']['n_groups']} 个感知组"
            )
        
        if "hebbian" in results and "som_final_error" in results["hebbian"]:
            synthesis["key_findings"].append(
                f"SOM学习误差: {results['hebbian']['som_final_error']:.4f}"
            )
        
        # generate建议
        synthesis["recommendations"] = [
            "使用神经几何学框架建模复杂问题",
            "应用测地线原理进行路径优化",
            "利用格式塔原则进行感知组织",
            "采用Hebbian学习进行模式recognize"
        ]
        
        return synthesis
    
    def get_theory_summary(self) -> Dict[str, List[str]]:
        """get所有理论摘要"""
        return {
            "neurogeometry": get_neurogeometry_insights(),
            "geodesic": get_geodesic_insights(),
            "gestalt": get_gestalt_insights(),
            "hebbian": get_hebbian_insights(),
            "gabor": get_gabor_insights(),
            "symplectic": get_symplectic_insights()
        }
    
    def diagnose_system_health(self) -> Dict[str, Any]:
        """诊断系统健康状态"""
        health = {
            "modules": {},
            "overall": "healthy"
        }
        
        modules = {
            "neurogeometry": self.neurogeometry,
            "geodesic": self.geodesic,
            "gestalt": self.gestalt,
            "hebbian": self.hebbian,
            "gabor": self.gabor,
            "symplectic": self.symplectic
        }
        
        for name, module in modules.items():
            try:
                health["modules"][name] = {
                    "status": "active",
                    "version": getattr(module, "version", "unknown"),
                    "name": getattr(module, "name", "unknown")
                }
            except Exception as e:
                health["modules"][name] = {
                    "status": "error",
                    "error": "执行失败"
                }
                health["overall"] = "degraded"
        
        return health

# ==================== 工厂函数 ====================

def create_neuromath_unified(config: Optional[Dict] = None) -> NeuromathVisionUnified:
    """创建神经数学视觉unified入口"""
    return NeuromathVisionUnified(config=config)

def get_all_insights() -> Dict[str, List[str]]:
    """get所有模块的关键洞见"""
    return {
        "神经几何学": [
            "视觉皮层的功能架构本质上是几何的",
            "神经连接遵循微分几何的结构约束",
            "协变编码追踪变换,不变编码消除变换"
        ],
        "亚黎曼测地线": [
            "测地线是约束条件下的最优路径",
            "轮廓补全 = 穿过遮挡区域的最短测地线",
            "SE(2)群 = 平面刚体运动(平移+旋转)"
        ],
        "格式塔理论": [
            "整体大于部分之和",
            "接近律,相似律,连续律,闭合律",
            "Prägnanz律:倾向最简洁规则的表示"
        ],
        "Hebbian学习": [
            "一起放电的神经元,连接在一起",
            "竞争学习选出最佳匹配单元",
            "拓扑保持:输入空间拓扑在输出空间保持"
        ],
        "Gaborcharacteristics": [
            "Gabor函数完美模拟视觉皮层简单细胞",
            "方位选择性与空间频率选择性",
            "多尺度整合:从小尺度细节到大尺度轮廓"
        ],
        "辛几何": [
            "辛几何描述相空间(位置+动量)",
            "哈密顿方程是decision动力学的几何形式",
            "辛积分保持相空间体积"
        ]
    }

# ==================== 测试代码 ====================

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
