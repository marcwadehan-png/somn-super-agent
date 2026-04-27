# ADR-007: Multi-Reasoning Engine Strategy

## Status
Accepted

## Context

Complex problems require different reasoning approaches:
- Simple queries → fast direct response
- Complex analysis → chain-of-thought
- Multi-perspective → tree exploration
- Interdependent → graph reasoning
- Practical problems → tool-augmented

## Decision

**Unified Reasoning Interface with Four Engines**:

1. **LongCoT (Long Chain of Thought)**
   - Sequential step-by-step reasoning
   - Best for: Complex calculations, multi-step logic
   - Max depth: 15 steps

2. **ToT (Tree of Thoughts)**
   - Parallel branch exploration
   - Best for: Strategic planning, option analysis
   - Beam width: 3 branches

3. **GoT (Graph of Thoughts)**
   - Graph network with dependencies
   - Best for: Complex systems, relationships
   - Max nodes: 100

4. **ReAct (Reasoning + Acting)**
   - Tool-augmented reasoning
   - Best for: Practical problem-solving
   - 10+ extended tools

**Selection Logic**:
```python
def select_engine(problem, context):
    if context.complexity < COMPLEXITY_THRESHOLD:
        return Engine.LONG_COT  # Fast path
    elif problem.has_dependencies:
        return Engine.GOT  # Graph reasoning
    elif problem.exploration_needed:
        return Engine.TOT  # Tree exploration
    else:
        return Engine.REACT  # Tool usage
```

## Consequences

### Positive
- Optimal reasoning approach per problem
- Extensible for new engines
- Clear performance tradeoffs

### Negative
- Engine selection complexity
- Increased execution time for complex problems
- Testing all combinations difficult

## Implementation
`intelligence/reasoning/`