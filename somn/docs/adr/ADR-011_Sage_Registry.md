# ADR-011: Sage Registry Design (Phase 2 Codification)

## Status
Accepted

## Context

Phase 2 of the Sage Engineering project requires:
- 779 encoded wisdom codes
- 746 full sages + 87 extra
- Machine-readable format
- Efficient lookup

## Decision

**Registry Structure**:

```
SageRegistry
├── Full Sages (746)
│   ├── Name/ID
│   ├── School affiliation
│   ├── Expertise areas
│   ├── Wisdom code
│   └── Position mapping
└── Extra Sages (87)
    └── Additional specialists
```

**Code Format**:
```python
@dataclass
class SageCode:
    code: str          # e.g., "CONFUCIUS_ANALYSIS_001"
    school: WisdomSchool
    domain: ProblemType
    description: str
    keywords: List[str]
```

**Lookup Efficiency**:
- School → Sage codes index
- Domain → Sage codes index
- Keyword → Sage codes index
- Name → Sage details

## Consequences

### Positive
- Standardized wisdom representation
- Fast retrieval by multiple dimensions
- Machine-processable
- Version controllable

### Negative
- Manual maintenance overhead
- Code explosion potential
- Mapping complexity

## Implementation
`wisdom_encoding_registry.py`