# ADR-003: Claw Subsystem Architecture

## Status
Accepted

## Context

The system requires execution of wisdom through "claws" - specialized execution units.
Requirements:
- 776+ claws need efficient management
- Claws must be extensible
- Need both independent and collaborative execution modes
- Performance critical (hot path)

## Decision

**Core Design**: Three-tier claw architecture

```
GlobalClawScheduler (orchestration)
    ↓
ClawArchitect (template/registry)
    ↓
Individual Claws (execution)
```

**Key Components**:

1. **GlobalClawScheduler**
   - 9 dispatch interfaces
   - Independent/collaborative modes
   - Result synthesis

2. **_ClawArchitect**
   - Claw template definitions
   - Lifecycle management
   - Configuration registry

3. **Individual Claws**
   - Task-specific execution
   - Wisdom source integration
   - Feedback reporting

**Execution Modes**:

1. **Independent Mode**
   - Single claw execution
   - Fast, focused response
   - Use for simple tasks

2. **Collaborative Mode**
   - Multiple claws coordinated
   - Complex problem-solving
   - Synthesized results

**Scheduling Strategy**:
- ProblemType → Department → WisdomSchool → Claw
- Weighted by expertise and availability

## Consequences

### Positive
- Scalable to 1000+ claws
- Clear separation enables testing
- Flexible execution modes
- Extensible claw definitions

### Negative
- Coordination overhead for collaborative mode
- Registry management complexity
- Performance overhead for small tasks

## Related ADRs
- ADR-001: V6 Architecture
- ADR-006: Wisdom School Classification