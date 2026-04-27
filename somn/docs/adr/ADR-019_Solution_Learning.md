# ADR-019: Solution Learning Architecture

## Status
Accepted

## Context

Need to learn from successful solutions:
- Track problem-solution pairs
- Pattern extraction
- Solution reuse
- Improvement tracking

## Decision

**Solution Learning Architecture**:

```
SolutionLearningSystem
├── SessionManager
│   ├── Record solutions
│   ├── Track success rates
│   └── Extract patterns
├── PatternExtractor
│   ├── Problem patterns
│   ├── Solution patterns
│   └── Context patterns
└── ReuseEngine
    ├── Similarity matching
    ├── Adaptation rules
    └── Success prediction
```

**Session Data Structure**:
```yaml
sessions/
├── session_id.yaml
│   ├── problem: "..."
│   ├── problem_type: "..."
│   ├── solution: "..."
│   ├── wisdom_used: [...]
│   ├── success: true/false
│   ├── feedback: "..."
│   └── metrics:
│       - time_taken
│       - quality_score
│       - satisfaction
```

**Learning Pipeline**:
1. Record: Store solution session
2. Extract: Find patterns
3. Index: Build searchable knowledge
4. Match: Find similar problems
5. Adapt: Apply solution to new context
6. Validate: Test adapted solution
7. Refine: Update based on results

## Consequences

### Positive
- Cumulative learning
- Faster problem resolution
- Quality improvement over time
- Wisdom reuse efficiency

### Negative
- Pattern overfitting risk
- Solution may not transfer
- Maintenance of solution library

## Implementation
`data/solution_learning/`