# ADR-015: OpenClaw External Data Architecture

## Status
Accepted

## Context

Need integration with external data:
- Web fetching
- File parsing
- API calls
- RSS feeds
- Web scraping

Challenge: Diverse data sources, different formats.

## Decision

**OpenClaw Architecture**:

```
Data Sources (13 files)
├── Web          # WebFetcher
├── File         # FileReader
├── API          # APIClient
├── RSS          # RSSParser
└── ...

Processors (5 core)
├── DocParser    # Document parsing
├── Cleaner      # Content cleaning
├── Extractor    # Data extraction
└── ...

Learning (2 components)
├── Feedback     # Result feedback
└── PatternLearner  # Pattern learning
```

**Tool Registry**:
```python
OpenClawTools = {
    "web_fetch": WebFetcher(),
    "file_read": FileReader(),
    "api_call": APIClient(),
    "rss_parse": RSSParser(),
    # ... 10+ tools
}
```

**Processing Flow**:
1. Select appropriate tool
2. Execute with retry logic
3. Parse/clean results
4. Learn from patterns
5. Store for future use

## Consequences

### Positive
- Extensible data sources
- Unified access interface
- Learning from usage patterns
- Comprehensive coverage

### Negative
- External dependencies
- Rate limiting challenges
- Data quality variance

## Implementation
`openclaw/`