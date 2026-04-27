"""编码类型定义 - 单元测试 (encoding_types.py)"""

import pytest
from datetime import datetime


class TestEncodingGranularity:
    """EncodingGranularity 枚举测试"""

    def test_all_values_exist(self):
        """验证所有 8 个颗粒度级别存在"""
        from src.neural_memory.encoding_types import EncodingGranularity
        expected = {"character", "word", "phrase", "sentence", "paragraph",
                     "section", "document", "multi"}
        actual = {g.value for g in EncodingGranularity}
        assert actual == expected

    def test_value_uniqueness(self):
        """验证枚举值无重复"""
        from src.neural_memory.encoding_types import EncodingGranularity
        values = [g.value for g in EncodingGranularity]
        assert len(values) == len(set(values))


class TestEncodingModality:
    """EncodingModality 枚举测试"""

    def test_basic_modalities(self):
        from src.neural_memory.encoding_types import EncodingModality
        assert EncodingModality.TEXT.value == "text"
        assert EncodingModality.IMAGE.value == "image"
        assert EncodingModality.AUDIO.value == "audio"
        assert EncodingModality.VIDEO.value == "video"
        assert EncodingModality.MULTI.value == "multi"


class TestEncodingType:
    """EncodingType 枚举测试"""

    def test_core_types(self):
        from src.neural_memory.encoding_types import EncodingType
        core = {"semantic", "syntactic", "context", "emotion", "temporal",
                "knowledge", "hybrid"}
        actual = {t.value for t in EncodingType}
        for c in core:
            assert c in actual

    def test_v31_types(self):
        from src.neural_memory.encoding_types import EncodingType
        v31 = {"contrastive", "attention", "causal", "abstraction",
               "cross_modal", "metacognitive", "semantic_field", "dynamic"}
        actual = {t.value for t in EncodingType}
        for v in v31:
            assert v in actual

    def test_v32_consulting_types(self):
        from src.neural_memory.encoding_types import EncodingType
        v32 = {"consulting_experience", "strategic_pattern",
               "anti_pattern", "methodology"}
        actual = {t.value for t in EncodingType}
        for v in v32:
            assert v in actual

    def test_total_type_count(self):
        from src.neural_memory.encoding_types import EncodingType
        assert len(list(EncodingType)) == 19


class TestEncodingContext:
    """EncodingContext dataclass 测试"""

    def test_minimal_creation(self):
        from src.neural_memory.encoding_types import EncodingContext
        ctx = EncodingContext(user_id="u1", session_id="s1")
        assert ctx.user_id == "u1"
        assert ctx.session_id == "s1"
        assert ctx.scenario == "general"
        assert ctx.priority == 5
        assert ctx.emotion == "neutral"
        assert ctx.attention_focus == []
        assert ctx.metadata == {}

    def test_full_creation(self, sample_encoding_context):
        ctx = sample_encoding_context
        assert ctx.user_id == "test_user"
        assert ctx.domain == "growth_consulting"
        assert isinstance(ctx.timestamp, str)

    def test_default_timestamp_is_valid_iso(self):
        from src.neural_memory.encoding_types import EncodingContext
        ctx = EncodingContext(user_id="u1", session_id="s1")
        datetime.fromisoformat(ctx.timestamp)  # 不抛异常即通过

    def test_v32_consulting_fields(self):
        from src.neural_memory.encoding_types import EncodingContext
        ctx = EncodingContext(
            user_id="u1", session_id="s1",
            consulting_phase="research",
            consulting_domain="growth",
            verified=True,
            lesson_source="案例A",
        )
        assert ctx.consulting_phase == "research"
        assert ctx.consulting_domain == "growth"
        assert ctx.verified is True
        assert ctx.lesson_source == "案例A"


class TestMemoryEncoding:
    """MemoryEncoding dataclass 测试"""

    def test_minimal_creation(self, sample_encoding_context):
        from src.neural_memory.encoding_types import (
            MemoryEncoding, EncodingGranularity, EncodingModality, EncodingType
        )
        enc = MemoryEncoding(
            id="enc_001",
            original_content="测试内容",
            encoded_vectors={"semantic": [0.1, 0.2]},
            granularity=EncodingGranularity.SENTENCE,
            modality=EncodingModality.TEXT,
            encoding_types=[EncodingType.SEMANTIC],
            context=sample_encoding_context,
        )
        assert enc.id == "enc_001"
        assert enc.quality_score == 0.8
        assert enc.confidence == 0.8
        assert enc.access_count == 0

    def test_to_dict(self, sample_encoding_context):
        from src.neural_memory.encoding_types import (
            MemoryEncoding, EncodingGranularity, EncodingModality, EncodingType
        )
        enc = MemoryEncoding(
            id="enc_002",
            original_content="内容",
            encoded_vectors={"semantic": [0.5]},
            granularity=EncodingGranularity.WORD,
            modality=EncodingModality.TEXT,
            encoding_types=[EncodingType.SEMANTIC, EncodingType.ATTENTION],
            context=sample_encoding_context,
        )
        d = enc.to_dict()
        assert d["id"] == "enc_002"
        assert d["granularity"] == "word"
        assert len(d["encoding_types"]) == 2
        assert "context" in d
        assert d["context"]["user_id"] == "test_user"

    def test_to_dict_timestamps_valid(self, sample_encoding_context):
        from src.neural_memory.encoding_types import (
            MemoryEncoding, EncodingGranularity, EncodingModality, EncodingType
        )
        enc = MemoryEncoding(
            id="e1", original_content="c",
            encoded_vectors={},
            granularity=EncodingGranularity.DOCUMENT,
            modality=EncodingModality.TEXT,
            encoding_types=[],
            context=sample_encoding_context,
        )
        d = enc.to_dict()
        datetime.fromisoformat(d["last_accessed"])
        datetime.fromisoformat(d["created_at"])
