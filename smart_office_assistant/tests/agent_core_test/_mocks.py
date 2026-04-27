# -*- coding: utf-8 -*-
"""
agent_core 测试 Mock 组件
Agent Core Test Mocks
"""
from unittest.mock import Mock


class MockMemorySystem:
    """Mock 记忆系统"""

    def __init__(self):
        self.memories = []
        self._stats = {'total': 0, 'short_term': 0, 'long_term': 0}

    def add_memory(self, content, memory_type='short_term', importance=0.5, context=None, tags=None):
        entry = Mock()
        entry.id = f'mem_{len(self.memories)}'
        entry.content = content
        entry.memory_type = memory_type
        entry.importance = importance
        entry.context = context or {}
        entry.tags = tags or []
        self.memories.append(entry)
        self._stats['total'] += 1
        self._stats[memory_type] = self._stats.get(memory_type, 0) + 1
        return entry

    def get_recent_context(self, n=5):
        return [m.content for m in self.memories[-n:]]

    def get_stats(self):
        return self._stats.copy()

    def search_memories(self, query, limit=5):
        return [m for m in self.memories if query.lower() in m.content.lower()][:limit]

    def get_memory(self, memory_id):
        for m in self.memories:
            if m.id == memory_id:
                return m
        return None


class MockKnowledgeBase:
    """Mock 知识库"""

    def __init__(self):
        self.entries = []
        self._stats = {'total': 0, 'categories': {}}

    def add_knowledge(self, title, content, category='general', source='', metadata=None, tags=None):
        entry = Mock()
        entry.id = f'kb_{len(self.entries)}'
        entry.title = title
        entry.content = content
        entry.category = category
        entry.source = source
        entry.metadata = metadata or {}
        entry.tags = tags or []
        self.entries.append(entry)
        self._stats['total'] += 1
        self._stats['categories'][category] = self._stats['categories'].get(category, 0) + 1
        return entry

    def search_knowledge(self, query, limit=5):
        results = [e for e in self.entries
                   if query.lower() in e.title.lower() or query.lower() in e.content.lower()]
        return results[:limit]

    def get_stats(self):
        return self._stats.copy()
