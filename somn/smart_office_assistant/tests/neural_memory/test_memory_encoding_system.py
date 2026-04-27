"""记忆编码系统主入口 - 单元测试 (memory_encoding_system_v3.py)

迁移自 memory_encoding_system_v3.py 第428行的 if __name__ == "__main__" 自测块
"""

import pytest
import numpy as np


class TestMemoryEncodingSystemV31Construction:
    """系统构造测试"""

    def test_default_construction(self):
        from src.neural_memory.memory_encoding_system_v3 import MemoryEncodingSystemV31
        system = MemoryEncodingSystemV31()
        assert system.model_name == "all-MiniLM-L6-v2"
        assert system.embedding_dim == 384
        assert system.contrastive_encoder is not None
        assert system.attention_encoder is not None
        assert system.causal_encoder is not None
        assert system.abstraction_encoder is not None
        assert system.cross_modal_encoder is not None
        assert system.metacognitive_encoder is not None
        assert system.semantic_field_encoder is not None
        assert system.dynamic_encoder is not None

    def test_custom_dimension(self):
        from src.neural_memory.memory_encoding_system_v3 import MemoryEncodingSystemV31
        system = MemoryEncodingSystemV31(embedding_dim=256)
        assert system.embedding_dim == 256

    def test_stats_initialized(self):
        from src.neural_memory.memory_encoding_system_v3 import MemoryEncodingSystemV31
        system = MemoryEncodingSystemV31()
        stats = system.get_stats()
        assert stats["total_encodings"] == 0


class TestMemoryEncodingSystemV31Encode:
    """编码功能测试（迁移自原自测块）"""

    def test_encode_returns_encoding_object(self, sample_encoding_context):
        from src.neural_memory.memory_encoding_system_v3 import MemoryEncodingSystemV31
        from src.neural_memory.encoding_types import EncodingType, EncodingGranularity
        system = MemoryEncodingSystemV31()
        content = "私域运营是现代企业增长的关键strategy"
        encoding = system.encode(
            content=content,
            context=sample_encoding_context,
            granularity=EncodingGranularity.MULTI,
            encoding_types=[
                EncodingType.SEMANTIC,
                EncodingType.ATTENTION,
                EncodingType.CAUSAL,
                EncodingType.ABSTRACTION,
                EncodingType.DYNAMIC,
            ],
        )
        assert encoding is not None
        assert encoding.id  # 编码ID非空
        assert 0.0 <= encoding.quality_score <= 1.0
        assert 0.0 <= encoding.confidence <= 1.0
        assert len(encoding.encoding_types) >= 1

    def test_encode_generates_id(self, sample_encoding_context):
        from src.neural_memory.memory_encoding_system_v3 import MemoryEncodingSystemV31
        from src.neural_memory.encoding_types import EncodingType, EncodingGranularity
        system = MemoryEncodingSystemV31()
        encoding = system.encode(
            content="测试", context=sample_encoding_context,
            granularity=EncodingGranularity.SENTENCE,
            encoding_types=[EncodingType.SEMANTIC],
        )
        assert encoding.id  # ID 不为空即可（实际前缀取决于 session_id）

    def test_encode_updates_stats(self, sample_encoding_context):
        from src.neural_memory.memory_encoding_system_v3 import MemoryEncodingSystemV31
        from src.neural_memory.encoding_types import EncodingType, EncodingGranularity
        system = MemoryEncodingSystemV31()
        system.encode(
            content="更新统计测试", context=sample_encoding_context,
            granularity=EncodingGranularity.WORD,
            encoding_types=[EncodingType.SEMANTIC],
        )
        stats = system.get_stats()
        assert stats["total_encodings"] >= 1
