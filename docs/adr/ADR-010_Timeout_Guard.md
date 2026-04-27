# ADR-010: Timeout and Resource Guard System

## Status
Accepted

## Context

Need controlled execution boundaries:
- Prevent infinite loops
- Limit resource consumption
- Provide graceful degradation
- Enable progress tracking

## Decision

**Tiered Timeout System**:

| Tier | Timeout | Use Case |
|------|---------|----------|
| Tier 0 | 30 seconds | Instant response |
| Tier 1 | 60 seconds | Quick analysis |
| Tier 2 | 120 seconds | Standard processing |
| Tier 3 | 180 seconds | Deep reasoning |

**TimeoutGuard Implementation**:
```python
class TimeoutGuard:
    """Context manager for timeout control."""

    def __init__(self, tier: int):
        self.timeout = TIMEOUT_BY_TIER[tier]
        self.elapsed = 0

    def check(self) -> bool:
        """Check if time remains."""
        return self.elapsed < self.timeout

    def remaining(self) -> float:
        """Get remaining time."""
        return max(0, self.timeout - self.elapsed)
```

**Fallback Strategy**:
1. Cancel current operation
2. Return partial result if available
3. Log timeout event
4. Trigger alternative path if defined

## Consequences

### Positive
- Predictable resource usage
- Prevents system hangs
- Clear user feedback
- Enables graceful degradation

### Negative
- May timeout long-but-valid operations
- Complexity in setting appropriate tiers
- Partial results may be confusing

## Implementation
`src/core/timeout_guard.py`