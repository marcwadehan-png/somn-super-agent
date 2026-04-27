"""
somn_legacy - Somn 早期入口模块拆分子包

从 src/somn.py 拆分出的子模块:
- _types: SomnConfig, AnalysisRequest, AnalysisResult
- _init: 各层初始化逻辑
- _analysis: 分析方法（analyze, growth_plan, demand_analysis 等）
- _solutions: 解决方案方法（recommendations, assess_v2, details）
- _utils: 工具方法（export, capabilities, health_check）
"""
