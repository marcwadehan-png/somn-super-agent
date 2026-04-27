# ADR-005: Neural Memory System Design

## Status
Accepted

## Context

Memory system needs to support:
- Short-term context (session)
- Medium-term patterns (semantic)
- Long-term experiences (episodic)
- Wisdom accumulation (knowledge)

Previous approach: Separate systems for different memory types.
Problem: Poor integration, inconsistent behavior.

## Decision

**Unified Memory Architecture**:

```
NeuralMemorySystem v1.0
    ├── UnifiedMemoryInterface (unified access)
    ├── MemoryTier hierarchy (7 tiers)
    └── UnifiedMemoryTier bridge (v4 compatibility)
```

**Memory Tiers**:

| Tier | Type | Capacity | Persistence |
|------|------|----------|-------------|
| TIER_WORKING | Session | ~100 items | Session only |
| TIER_SHORT_TERM | Context | ~1K items | Hours |
| TIER_MEDIUM_TERM | Semantic | ~10K items | Days |
| TIER_LONG_TERM | Episodic | ~100K items | Permanent |
| TIER_CENTRAL | Wisdom | ~1M items | Permanent |
| TIER_SEMANTIC | Abstract | Variable | Permanent |
| TIER_EPISODIC | Events | Variable | Permanent |

**Unified Interface**:
```python
interface UnifiedMemoryInterface:
    async store(type, key, value, metadata)
    async retrieve(type, key) -> value
    async search(query, filters) -> results
    async forget(type, key)
```

## Consequences

### Positive
- Consistent access pattern for all memory types
- Clear tier responsibilities
- Efficient memory usage
- Easy to extend new tiers

### Negative
- More complex implementation
- Potential performance overhead
- Migration complexity from v4

## Related ADRs
- ADR-004: Learning System
- ADR-010: Memory Persistence Strategy