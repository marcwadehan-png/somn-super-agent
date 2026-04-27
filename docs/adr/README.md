# Architecture Decision Records (ADR)

This directory contains architectural decision records for the Somn project.

## Purpose

ADRs document significant architectural decisions, including:
- The context that led to the decision
- The options considered
- The decision made
- The consequences (positive and negative)

## Format

Each ADR follows this template:

```markdown
# ADR-XXX: Title

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
Describe the problem or situation that requires a decision.

## Decision
Describe the decision that was made.

## Consequences
### Positive
- ...

### Negative
- ...

## Related ADRs
- ADR-001: ...
```

## Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| ADR-001 | V6 Architecture Decision | Accepted | 2026-01 |
| ADR-002 | Multi-Model Strategy | Accepted | 2026-02 |
| ADR-003 | Claw Subsystem Design | Accepted | 2026-02 |
| ADR-004 | Learning System Architecture | Accepted | 2026-02 |
| ADR-005 | Memory System Design | Accepted | 2026-02 |
| ... | ... | ... | ... |

## Creating New ADRs

1. Copy the template
2. Assign the next sequential number
3. Set status to "Proposed"
4. Fill in the details
5. Submit for review

## Review Process

1. Create ADR with "Proposed" status
2. Team reviews during weekly sync
3. Update status to "Accepted" or "Rejected"
4. Link related ADRs