# ADR-006: Wisdom School Classification System

## Status
Accepted

## Context

The system integrates wisdom from 35 ancient Chinese philosophical schools.
Need to:
- Classify problems to appropriate schools
- Combine multiple schools when beneficial
- Balance tradition with modern applicability

## Decision

**35 Schools across 11 Departments**:

| Department | Schools | Focus |
|------------|---------|-------|
| 政治 | 儒、法、墨、道、阴阳 | Governance, Ethics |
| 军事 | 兵、墨(侠) | Strategy, Defense |
| 经济 | 农、商、轻重 | Economy, Trade |
| 文化 | 儒、墨、道、法 | Education, Arts |
| 科技 | 名、墨(工)、阴阳 | Science, Logic |
| 社会 | 儒、墨、道、杂 | Society, Community |
| 外交 | 纵、衡、儒 | Diplomacy |
| 法律 | 法、儒、杂 | Law, Justice |
| 思想 | 道、玄、佛 | Philosophy |
| 自然 | 阴阳、五行、农 | Nature, Cosmos |
| 管理 | 儒、法、道、兵 | Management |

**School Selection Algorithm**:
1. Analyze problem type
2. Identify relevant departments
3. Score schools by expertise match
4. Select top N schools (typically 1-3)
5. Weight by problem complexity

## Consequences

### Positive
- Rich wisdom source diversity
- Clear classification system
- Scalable to new schools
- Cross-school synthesis

### Negative
- Complex selection logic
- Potential school conflicts
- Overlapping expertise areas

## Implementation
`intelligence/dispatcher/wisdom_dispatch/_dispatch_mapping.py`