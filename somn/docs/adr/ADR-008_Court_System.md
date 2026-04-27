# ADR-008: Court System Design (Positions & Ranks)

## Status
Accepted

## Context

Need organizational structure for 776+ sage claws:
- Clear hierarchy for coordination
- Role definitions for accountability
- Career progression for motivation
- Authority delegation mechanism

## Decision

**V1.0.0 Court System**:

```
┌─────────────────────────────────────────┐
│           Emperor (最高决策)              │
│         Seven Congress (七人代表)        │
│            4-vote approval              │
└─────────────────────────────────────────┘
         │
    ┌────┴────┐
    │  11 Departments  │
    └─────────────┘
         │
    ┌────┴────┐
    │ 35 Schools │
    └───────────┘
         │
    ┌────┴────┐
    │ 422 Positions │
    └───────────┘
```

**Position Structure**:
- 377 base positions
- 25 noble ranks (爵位)
- 7 Congress members
- 6 Foremen leaders

**Governance**:
- Seven Congress with 4-vote approval system
- Department heads report to Congress
- Position appointments via meritocracy

## Consequences

### Positive
- Clear organizational structure
- Scalable governance
- Fair advancement system
- Wisdom diversity representation

### Negative
- Bureaucratic overhead
- Complex position mapping
- Potential political dynamics

## Related ADRs
- ADR-006: Wisdom Schools
- ADR-009: Claw Assignment