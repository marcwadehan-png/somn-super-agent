# ADR-002: A/B Dual-Model Scheduling Strategy

## Status
Accepted

## Context

The system uses two local LLMs:
- Model A: Llama 3.2 1B GGUF (primary, fast)
- Model B: Gemma4 multimodal (secondary, capable)

Challenges:
- Single model may be unavailable during high load
- Different models excel at different tasks
- Need failover mechanism for reliability
- Want to optimize cost/performance tradeoff

## Decision

Implemented A/B dual-model scheduling with:

1. **Primary/Secondary Mode**
   - A: Fast responses for simple queries
   - B: Complex reasoning tasks

2. **Fallback Chain**
   - Try A → If timeout/error → Try B → If timeout → Default response

3. **Load Balancing**
   - Distribute requests based on model capacity
   - Monitor latency and adjust routing

4. **Circuit Breaker**
   - Detect persistent failures
   - Temporarily disable failing model
   - Auto-recover after cooldown

Configuration:
```python
dual_model_service = DualModelService(
    model_a=ModelConfig(name="llama-3.2-1b", ...),
    model_b=ModelConfig(name="gemma4-multimodal", ...),
    fallback_enabled=True,
    timeout_ms=30000,
    circuit_breaker_threshold=5
)
```

## Consequences

### Positive
- Improved reliability (no single point of failure)
- Better utilization of available models
- Graceful degradation under load

### Negative
- More complex routing logic
- Increased latency for fallback scenarios
- Added configuration complexity

## Implementation
`src/tool_layer/dual_model_service.py`