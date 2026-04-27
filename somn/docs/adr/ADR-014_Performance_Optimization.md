# ADR-014: Performance Optimization Strategy

## Status
Accepted

## Context

System optimization needs (v19-v21):
- Startup time too slow (~500ms target → ~5ms)
- Lazy loading not fully implemented
- I/O operations inefficient
- Memory usage high

## Decision

**Optimization Layers**:

**1. Lazy Loading (v19)**
```python
# Before: Import all sages at startup
from smart_office_assistant import ALL_SAGES  # 858 loaded

# After: Load on demand
@lazy_import
def get_sages(school):
    return _load_sages_for_school(school)
```

**2. Dead Code Cleanup (v20)**
- Empty stub files
- Unused utility functions
- Obsolete compatibility layers
- Result: ~2000+ lines removed

**3. I/O Optimization (v21)**
- Dirty flag for learning writes
- Feedback report caching
- Registry副本消除

**4. Loop Optimization**
```python
# Before: Multiple passes
for grade in grades:
    for source in sources:
        count += 1

# After: Single pass
stats = {}
for item in items:
    stats[get_grade(item)] += 1
    stats[get_source(item)] += 1
```

## Consequences

### Positive
- 99% startup time reduction
- Lower memory footprint
- Faster response times
- Cleaner codebase

### Negative
- First-access latency
- Debug complexity for lazy loading
- Testing harder without full imports

## Implementation
- `cloning/__init__.py` (lazy loading)
- Various dead code cleanup
- `_imperial_library.py` (loop optimization)