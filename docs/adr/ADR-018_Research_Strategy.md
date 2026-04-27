# ADR-018: Research Strategy Engine

## Status
Accepted

## Context

Need intelligent research planning:
- Multiple research approaches
- Strategy selection based on context
- Depth/cost tradeoffs
- Time constraints handling

## Decision

**Research Strategy Engine (~1320 lines)**:

**7 Strategy Enumerations**:
```python
class ResearchStrategy(Enum):
    PARALLEL = auto()      # Multiple simultaneous
    SEQUENTIAL = auto()    # One after another
    ADAPTIVE = auto()      # Adjust based on results
    DEPTH_FIRST = auto()   # Thorough exploration
    BREADTH_FIRST = auto() # Broad coverage
    BEST_EFFORT = auto()   # Time-constrained
    CONFIDENCE = auto()    # High-confidence first
```

**5 Data Classes**:
```python
@dataclass
class ResearchConfig:
    strategy: ResearchStrategy
    max_depth: int
    timeout_seconds: int
    min_confidence: float

@dataclass
class ResearchResult:
    findings: List[Finding]
    confidence: float
    time_spent: float
    strategy_used: ResearchStrategy
```

**Selection Logic**:
```python
def select_strategy(context: ResearchContext) -> ResearchStrategy:
    if context.time_constraint:
        return ResearchStrategy.BEST_EFFORT
    elif context.requires_depth:
        return ResearchStrategy.DEPTH_FIRST
    elif context.multiple_hypotheses:
        return ResearchStrategy.PARALLEL
    else:
        return ResearchStrategy.ADAPTIVE
```

## Consequences

### Positive
- Optimized research approach per task
- Time-aware planning
- Quality/cost tradeoff handling
- Extensible for new strategies

### Negative
- Strategy selection complexity
- May choose suboptimal strategy
- Increased cognitive overhead

## Implementation
`_research_strategy_engine.py`