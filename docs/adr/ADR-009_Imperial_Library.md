# ADR-009: Imperial Library System V3.0

## Status
Accepted

## Context

Need centralized knowledge storage:
- 830+ sage wisdom documents
- Multiple knowledge sources
- Diverse classification needs
- Access control requirements

## Decision

**8-Pavilion Structure**:

| Pavilion | Content | Source Types | Classification |
|----------|---------|--------------|----------------|
| 智慧阁 | Wisdom codes | 20 types | 16 categories |
| 经验馆 | Experience records | 8 types | Learning |
| 方案馆 | Solutions | Problem-type | Indexed |
| 反馈馆 | Feedback | Task/workflow | Priority |
| 模式馆 | Patterns | Abstract | Similarity |
| 指标馆 | Metrics | ROI, quality | Time-series |
| 档案馆 | Archives | Historical | Date-indexed |
| 法规馆 | Rules | System | Authority |

**Features**:
- 5-level permission system
- 20 source types
- 16 classification dimensions
- Unified statistics interface

## Consequences

### Positive
- Centralized knowledge management
- Clear organization
- Scalable architecture
- Easy to extend

### Negative
- Single point of failure (mitigated by backup)
- Complexity in classification
- Performance for large queries

## Implementation
`_imperial_library.py`