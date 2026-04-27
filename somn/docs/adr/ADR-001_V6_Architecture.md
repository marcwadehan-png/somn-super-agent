# ADR-001: V6 Overall Architecture Design

## Status
Accepted

## Context

Somn v6.0 represents a major architectural upgrade from v5.x. The system needed to support:
- 776+ sage claws across 35 schools
- 422 positions in the court system
- Self-evolution capabilities
- Multi-reasoning engine support (LongCoT, ToT, GoT, ReAct)

Previous architecture had limitations:
- Rigid single-model dispatch
- Poor scalability for wisdom system
- Limited learning feedback loops
- Monolithic components

## Decision

Adopted a layered architecture with clear separation:

```
Layer 1: Presentation (AgentCore)
Layer 2: Intelligence (Wisdom Coordinator, Scheduler)
Layer 3: Execution (WisdomDispatcher, Claws)
Layer 4: Learning (UnifiedLearningOrchestrator)
Layer 5: Memory (NeuralMemorySystem)
```

Key architectural decisions:

1. **Wisdom Layer Separation**: Isolated wisdom processing from core logic
2. **Claw Subsystem**: Created modular claw execution system
3. **Multi-Engine Reasoning**: Unified interface for LongCoT/ToT/GoT/ReAct
4. **Tier-based Processing**: Tier0 (instant) → Tier3 (deep reasoning)
5. **Feedback Loop**: Learning system integrated at all layers

## Consequences

### Positive
- Clear separation enables independent scaling
- Modular design supports incremental upgrades
- Multi-engine flexibility improves problem-solving
- Self-evolution capability built-in

### Negative
- Increased complexity in coordination
- More communication overhead between layers
- Steeper learning curve for new developers

## Related ADRs
- ADR-002: Multi-Model Strategy
- ADR-003: Claw Subsystem Design
- ADR-004: Learning System Architecture