# ADR-012: ROI Tracking System Design

## Status
Accepted

## Context

Need to measure system effectiveness:
- Task-level ROI (time, quality, satisfaction)
- Workflow-level ROI (efficiency gains)
- Strategy-level ROI (overall improvement)
- Data-driven optimization

## Decision

**Three-Level ROI System**:

```
Level 1: Task ROI
├── Time efficiency: expected vs actual
├── Quality score: user rating
└── Satisfaction: feedback sentiment

Level 2: Workflow ROI
├── Task completion rate
├── Average time per task type
└── Resource utilization

Level 3: Strategy ROI
├── Long-term improvement trends
├── Strategy success rates
└── System evolution metrics
```

**Persistence**:
- Cross-process YAML storage
- Automatic aggregation
- Time-weighted calculations
- Historical comparison

**ROI Formula**:
```
ROI = (Benefits - Costs) / Costs × 100%

Where:
- Benefits = Quality × Satisfaction × Efficiency
- Costs = Time × Resource × Complexity
```

## Consequences

### Positive
- Data-driven optimization
- Identifies underperforming areas
- Tracks improvement over time
- Enables A/B testing

### Negative
- Complex metrics collection
- Delayed feedback (quality takes time)
- Potential gaming of metrics

## Implementation
`data/ml/roi_*.yaml`