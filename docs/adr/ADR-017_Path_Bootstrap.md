# ADR-017: Path Bootstrap and Project Layout

## Status
Accepted

## Context

Project location may vary:
- Different drives (D:, E:, etc.)
- Different base paths
- Multiple Python environments
- Shared team configurations

Challenge: Absolute paths break portability.

## Decision

**Path Bootstrap Strategy**:

```python
# path_bootstrap.py
def find_project_root() -> Path:
    """Auto-discover project root."""
    current = Path(__file__).parent

    # Search upward for marker
    markers = ['smart_office_assistant', 'pyproject.toml', '.git']
    for parent in current.parents:
        if any((parent / m).exists() for m in markers):
            return parent

    # Fallback to current
    return current
```

**Three-Layer Path Resolution**:

```python
# Layer 1: Project root
PROJECT_ROOT = find_project_root()

# Layer 2: Module paths
MODULE_ROOT = PROJECT_ROOT / 'smart_office_assistant' / 'src'
DATA_ROOT = PROJECT_ROOT / 'data'

# Layer 3: Relative paths in code
CONFIG_PATH = Path('config') / 'settings.yaml'  # relative!
```

**Import Strategy**:
```python
# Always use relative imports within module
from ..core import AgentCore  # Good

# External access via somn package
from smart_office_assistant import Somn  # Good
```

## Consequences

### Positive
- Project runs from any location
- Team sharing made easy
- No hardcoded paths
- CI/CD friendly

### Negative
- Slight startup overhead
- Debugging path issues harder
- Some IDE features may not work

## Implementation
`path_bootstrap.py`, `tests/conftest.py`