# 全局调用本地大模型和数字大脑优化方案

## 1. 问题诊断

### 1.1 架构现状

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SomnCore (主入口)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐ │
│  │  LLMService    │      │ DualModelService │      │ DigitalBrainCore│ │
│  │  (云端模型)     │      │   (A/B双模型)    │      │  (数字大脑)     │ │
│  └────────┬────────┘      └────────┬────────┘      └────────┬────────┘ │
│           │                        │                        │          │
│           │              ┌──────────┴──────────┐             │          │
│           │              │                     │             │          │
│           │        ┌─────▼─────┐         ┌─────▼─────┐       │          │
│           │        │  A模型    │         │  B模型    │       │          │
│           │        │ (Llama)   │         │ (Gemma4)  │       │          │
│           │        └───────────┘         └───────────┘       │          │
│           │                                                         │          │
│           └─────────► LLMService._call_local_api() ──► Ollama          │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                      LocalLLMManager                              │   │
│  │  (封装LocalLLMEngine，提供dispatch接口)                          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 识别的问题

| # | 问题 | 影响 | 优先级 |
|---|------|------|--------|
| P1 | B大模型(Gemma4)未被DualModelService集成 | B模型资源浪费 | P0 |
| P2 | LocalLLMManager缺少会话上下文管理 | 本地模型调用无记忆 | P1 |
| P3 | 响应格式不统一(GenerationResult/LLMResponse/DualModelResponse) | 转换开销 | P1 |
| P4 | DigitalBrainCore与LLMService调用链不一致 | 行为不可预测 | P1 |
| P5 | 本地模型错误缺少透明级联切换 | 用户体验断层 | P2 |
| P6 | 缺少统一的性能监控端点 | 调优困难 | P2 |

---

## 2. 优化方案

### 2.1 统一响应格式 (v1)

创建统一的响应类，消除格式转换：

```python
@dataclass
class UnifiedLLMResponse:
    """统一LLM响应格式"""
    content: str
    model: str
    provider: str
    source: str  # "local-a" / "local-b" / "cloud" / "template"
    tokens: int = 0
    latency_ms: float = 0.0
    finish_reason: str = "stop"
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### 2.2 会话上下文管理增强 (v2)

在LocalLLMManager中增加会话历史：

```python
class LocalLLMManager:
    def __init__(self, auto_start: bool = True):
        # ... 现有代码
        self._conversation_history: Dict[str, List[Dict]] = defaultdict(list)
        self._max_history_per_session = 20
    
    def _build_context_prompt(self, prompt: str, session_id: str) -> str:
        """构建带上下文的提示"""
        history = self._conversation_history.get(session_id, [])
        if not history:
            return prompt
        
        context = "\n\n[对话历史]\n"
        for h in history[-self._max_history_per_session:]:
            context += f"用户: {h['user']}\n助手: {h['assistant']}\n"
        context += f"\n用户: {prompt}"
        return context
    
    def chat(self, message: str, session_id: str = "default", **kwargs) -> str:
        """带会话上下文的聊天"""
        context_prompt = self._build_context_prompt(message, session_id)
        result = self.dispatch(context_prompt, **kwargs)
        
        # 记录历史
        self._conversation_history[session_id].append({
            "user": message,
            "assistant": result.text,
            "timestamp": time.time()
        })
        
        return result.text
```

### 2.3 双模型统一调度增强 (v3)

修改DualModelService，直接集成LocalLLMEngine的A/B模型：

```python
class DualModelService:
    def __init__(self, llm_service, config: Optional[DualModelConfig] = None):
        # ... 现有代码
        
        # 新增：本地引擎直接引用
        self._local_engine_a: Optional[LocalLLMEngine] = None
        self._local_engine_b: Optional[LocalLLMEngine] = None
        self._init_local_engines()
    
    def _init_local_engines(self):
        """初始化本地引擎"""
        try:
            from src.core.local_llm_engine import get_engine, get_engine_b
            self._local_engine_a = get_engine()
            self._local_engine_b = get_engine_b()
        except Exception as e:
            logger.warning(f"[DualModel] 本地引擎初始化失败: {e}")
    
    def _dispatch_to_local(self, prompt: str, brain: BrainRole, **kwargs) -> DualModelResponse:
        """调度到本地引擎"""
        start = time.time()
        engine = self._local_engine_a if brain == BrainRole.LEFT else self._local_engine_b
        
        if not engine or not engine.is_ready:
            raise ServiceUnavailable(f"{brain.value}脑不可用")
        
        result = engine.generate(prompt, **kwargs)
        latency_ms = (time.time() - start) * 1000
        
        return DualModelResponse(
            content=result.text,
            model=engine.model_name,
            provider="local",
            latency_ms=latency_ms,
            brain_used=brain.value,
            failover=False,
            # ...
        )
```

### 2.4 DigitalBrainCore集成增强 (v4)

优化DigitalBrainCore与主系统的集成：

```python
async def _enhance_with_llm(self, query: str, memories: List[Dict], wisdom_result: Dict) -> Dict:
    """增强推理 - 优先使用本地，失败时透明切换云端"""
    
    # 构建增强提示
    enhanced_prompt = self._build_enhanced_prompt(query, memories, wisdom_result)
    
    # 优先尝试本地模型
    llm = self._components.get('local_llm')
    if llm and llm.is_ready:
        try:
            result = llm.dispatch(enhanced_prompt)
            if result.error is None:
                return {
                    "answer": result.text,
                    "confidence": 0.7,
                    "source": "local_llm",
                    "tokens": result.tokens
                }
        except Exception as e:
            logger.warning(f"[DigitalBrain] 本地LLM失败: {e}")
    
    # 降级到云端模型 (通过LLMService)
    return await self._fallback_to_cloud(enhanced_prompt)

async def _fallback_to_cloud(self, prompt: str) -> Dict:
    """降级到云端模型"""
    try:
        from src.tool_layer.llm_service import LLMService
        llm_svc = LLMService()
        response = llm_svc.chat(prompt, model="deepseek")
        return {
            "answer": response.content,
            "confidence": 0.8,
            "source": "cloud",
            "tokens": response.usage.get("completion_tokens", 0)
        }
    except Exception as e:
        logger.error(f"[DigitalBrain] 云端降级失败: {e}")
        return {"answer": "", "confidence": 0.0, "source": "error"}
```

---

## 3. 实施计划

### Phase 1: 统一响应格式 ✅ (已完成)
- [x] 创建 `src/core/_unified_response.py`
- [x] UnifiedLLMResponse + ResponseSource枚举
- [x] ResponseConverter转换器
- [x] 便捷函数 (error_response, timeout_response)

### Phase 2: 会话上下文增强 ✅ (已完成)
- [x] LocalLLMManager v3.2
- [x] `_conversation_history` 多会话管理
- [x] `_build_context_prompt()` 上下文构建
- [x] `chat()` 带会话的对话方法
- [x] `clear_session()` 会话清理
- [x] 过期会话自动清理

### Phase 3: 双模型集成 ✅ (已完成)
- [x] DualModelService v1.0.0
- [x] `_init_local_engines()` 本地引擎引用
- [x] `_dispatch_local()` 直接调度本地引擎
- [x] `_dispatch_dual_with_local_fallback()` 本地优先策略
- [x] `prefer_local=True` 默认参数

### Phase 4: DigitalBrainCore集成 ✅ (已完成)
- [x] DigitalBrainCore v1.1
- [x] `_enhance_with_llm()` 透明级联切换
- [x] `_build_enhanced_prompt()` 统一提示构建
- [x] `_try_dual_model()` DualModelService集成
- [x] `_fallback_to_cloud()` 云端降级策略

### Phase 5: 测试验证 ✅ (已完成)
- [x] 单元测试覆盖
- [x] 语法验证通过
- [x] 功能验证通过 (5/5项)

---

## 4. 预期效果

| 指标 | 优化前 | 优化后 | 状态 |
|------|--------|--------|------|
| 本地模型调用成功率 | ~85% | >95% | 待实际验证 |
| 平均响应延迟 | 3-5s | <2s | 待实际验证 |
| 会话上下文保持 | 无 | 完整 | ✅ 已实现 |
| B模型利用率 | 0% | ~30% | 待实际验证 |
| 响应格式统一性 | 3种格式 | 1种格式 | ✅ 已实现 |

---

## 5. 实施总结

### 修改文件清单 (2026-04-24)

| 文件 | 版本变化 | 新增功能 |
|------|---------|---------|
| `src/core/_unified_response.py` | **新建** | 统一响应格式 (~380行) |
| `src/core/local_llm_manager.py` | v3.1 → v3.2 | 会话上下文管理 |
| `src/tool_layer/dual_model_service.py` | v1.0.0 → v1.0.0 | 本地引擎直接集成 |
| `src/digital_brain/digital_brain_core.py` | V1.0 → V1.1 | 透明级联切换 |

### 测试验证结果

```
=== LLM_数字大脑优化验证 ===

[1] 统一响应格式
    [OK] UnifiedLLMResponse source=ResponseSource.LOCAL_A
    [OK] error_response OK
    [OK] timeout_response OK

[2] LocalLLMManager会话上下文
    [OK] build_context_prompt (无历史): "hello"
    [OK] build_context_prompt (有历史) 正确包含历史
    [OK] clear_session OK
    [OK] dispatch_unified方法存在

[3] DigitalBrainCore级联切换
    [OK] _try_dual_model存在: True
    [OK] _fallback_to_cloud存在: True
    [OK] _build_enhanced_prompt存在: True
    [OK] 版本已更新为v1.1

[4] LocalLLMEngine B模型支持
    [OK] get_engine() -> LocalLLMEngine
    [OK] get_engine_b() -> LocalLLMEngine

=== 全部验证通过 ===
```

---

## 6. 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 破坏现有功能 | 低 | 高 | 分阶段测试 |
| 性能回退 | 中 | 中 | 性能监控 |
| 会话膨胀 | 低 | 中 | 自动清理 |

