# -*- coding: utf-8 -*-
"""测试 somn_components 所有模块"""
import sys
sys.path.insert(0, 'core')

from somn_components import (
    SemanticAnalyzer, SemanticMemoryManager, RouterDispatcher,
    ROITracker, FeedbackPipeline, ReinforcementLearner,
    MemoryRetriever, SearchCache, GoalManager, ReflectionEngine,
    TaskOrchestrator, QLearner, ActionResolver,
    LLMParser, SystemMonitor,
)

print('=== Somn Components 完整导入测试 ===')
print()

# 实例化所有组件
components = {
    'SemanticAnalyzer': SemanticAnalyzer(),
    'RouterDispatcher': RouterDispatcher(),
    'ROITracker': ROITracker(),
    'FeedbackPipeline': FeedbackPipeline(),
    'MemoryRetriever': MemoryRetriever(),
    'SearchCache': SearchCache(),
    'GoalManager': GoalManager(),
    'ReflectionEngine': ReflectionEngine(),
    'TaskOrchestrator': TaskOrchestrator(),
    'QLearner': QLearner(),
    'ActionResolver': ActionResolver(),
    'LLMParser': LLMParser(),
    'SystemMonitor': SystemMonitor(),
}

for name, obj in components.items():
    print(f'OK: {name}')

print()
print('=== 功能验证 ===')
tc = TaskOrchestrator()
cache_key = tc.compute_cache_key("测试用户输入")
print(f'TaskOrchestrator cache_key: {cache_key}')

qlearner = QLearner()
state = qlearner.encode_state({'industry': 'test', 'intent_type': 'chat', 'user_id': 'u1'})
print(f'QLearner state: {state}')
print(f'QLearner Q值: {qlearner.get_q_value(state, "default")}')

ar = ActionResolver()
print(f'ActionResolver clamp: {ar.clamp_score(1.5)}')

goal_id = GoalManager().make_goal_id("完成销售增长")
print(f'GoalManager goal_id: {goal_id}')

print()
print('所有模块导入和实例化成功!')
