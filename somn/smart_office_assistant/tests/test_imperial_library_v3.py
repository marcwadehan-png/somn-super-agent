# -*- coding: utf-8 -*-
"""
藏书阁V1.0 全链路测试
test_imperial_library_v3.py

测试藏书阁V1.0的所有核心功能：
1. 格子化存储（分馆→书架→格位）
2. 多维查询（分馆/书架/分级/来源/分类/关键词/标签/贤者/岗位/Claw）
3. 跨系统桥接（register_bridge/submit_bridge_memory）
4. 跨域引用（add_cross_reference/get_cross_references）
5. 持久化（YAML分馆分区落盘）
6. V2兼容层（query_memories/get_memory）
7. 统计接口（get_wing_stats/get_full_stats）
8. 权限模型（LibraryPermission）

运行: python -m pytest tests/test_imperial_library_v3.py -v
"""

import pytest
import tempfile
import shutil
import os
import time
from pathlib import Path
from typing import List, Dict, Any

# 路径引导
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.intelligence.dispatcher.wisdom_dispatch._imperial_library import (
    ImperialLibrary,
    LibraryWing,
    LibraryPermission,
    MemoryGrade,
    MemorySource,
    MemoryCategory,
    CellRecord,
    MemoryRecord,
)


# ═══════════════════════════════════════════════════════════════
#  Fixtures
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def temp_storage():
    """创建临时存储目录"""
    temp_dir = tempfile.mkdtemp(prefix="test_imperial_library_v3_")
    yield temp_dir
    # 清理
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def library(temp_storage):
    """创建藏书阁实例（使用临时存储）"""
    lib = ImperialLibrary()

    # 手动设置存储路径（绕过配置文件）
    lib._storage_path = Path(temp_storage) / "imperial_library"
    lib._storage_path.mkdir(parents=True, exist_ok=True)
    lib._auto_save_interval = 60

    # 清空内部状态
    lib._cells.clear()
    lib._wing_shelf_index.clear()
    lib._cell_counters.clear()
    lib._cell_counters["SAGE_sage_profiles"] = 1
    lib._cell_counters["EXEC_execution_logs"] = 1
    lib._cell_counters["LEARN_learning_insights"] = 1
    lib._bridges.clear()

    return lib


@pytest.fixture
def sample_cell_data() -> Dict[str, Any]:
    """样例格位数据"""
    return {
        "title": "测试记忆",
        "content": "这是一条测试记忆内容，用于验证藏书阁V1.0功能",
        "wing": LibraryWing.SAGE,
        "shelf": "sage_profiles",
        "source": MemorySource.SAGE_ENCODING,
        "category": MemoryCategory.SAGE_WISDOM,
        "grade": MemoryGrade.BING,
        "reporting_system": "TestSystem",
        "tags": ["测试", "单元测试", "V1.0"],
        "metadata": {"test_id": "test_001", "version": "v3.0"},
        "associated_sage": "孔子",
        "associated_position": "礼部尚书",
        "associated_claw": "孔子",
    }


# ═══════════════════════════════════════════════════════════════
#  G.1 格子化存储测试
# ═══════════════════════════════════════════════════════════════

class TestGridStorage:
    """测试格子化存储（分馆→书架→格位三级结构）"""

    def test_submit_cell_generates_correct_id(self, library, sample_cell_data):
        """测试submit_cell生成正确的格位ID"""
        record = library.submit_cell(**sample_cell_data)

        assert record is not None
        assert record.id.startswith("SAGE_sage_profiles_")
        assert record.wing == LibraryWing.SAGE
        assert record.shelf == "sage_profiles"
        assert record.cell_index == 1

    def test_cell_counter_increments(self, library, sample_cell_data):
        """测试格位计数器递增"""
        record1 = library.submit_cell(**sample_cell_data)
        record2 = library.submit_cell(**sample_cell_data)

        assert record1.cell_index == 1
        assert record2.cell_index == 2
        assert record1.id != record2.id

    def test_get_cell_retrieves_record(self, library, sample_cell_data):
        """测试get_cell能正确获取记录"""
        submitted = library.submit_cell(**sample_cell_data)
        retrieved = library.get_cell(submitted.id)

        assert retrieved is not None
        assert retrieved.id == submitted.id
        assert retrieved.title == sample_cell_data["title"]
        assert retrieved.content == sample_cell_data["content"]

    def test_cell_record_has_v3_fields(self, library, sample_cell_data):
        """测试CellRecord包含V3.0新增字段"""
        record = library.submit_cell(**sample_cell_data)

        # V1.0新增字段
        assert hasattr(record, 'semantic_embedding')
        assert hasattr(record, 'cross_references')
        assert hasattr(record, 'access_count')
        assert hasattr(record, 'last_accessed')

        assert record.semantic_embedding is None
        assert record.cross_references == []
        assert record.access_count == 0

    def test_touch_updates_access_stats(self, library, sample_cell_data):
        """测试touch()更新访问统计"""
        record = library.submit_cell(**sample_cell_data)
        initial_access = record.access_count

        library.get_cell(record.id)  # 会触发touch
        updated = library.get_cell(record.id)

        assert updated.access_count > initial_access
        assert updated.last_accessed > 0


# ═══════════════════════════════════════════════════════════════
#  G.2 多维查询测试
# ═══════════════════════════════════════════════════════════════

class TestMultiDimensionalQuery:
    """测试多维查询功能"""

    @pytest.fixture(autouse=True)
    def setup_test_data(self, library):
        """设置测试数据"""
        # 提交多条不同维度的记录
        library.submit_cell(
            title="孔子智慧",
            content="仁者爱人",
            wing=LibraryWing.SAGE,
            shelf="sage_profiles",
            source=MemorySource.SAGE_ENCODING,
            category=MemoryCategory.SAGE_WISDOM,
            grade=MemoryGrade.JIA,
            tags=["儒家", "孔子"],
            associated_sage="孔子",
        )
        library.submit_cell(
            title="ROI优化报告",
            content="效率提升30%",
            wing=LibraryWing.EXEC,
            shelf="execution_logs",
            source=MemorySource.ROI_TRACKING,
            category=MemoryCategory.EXECUTION_LOG,
            grade=MemoryGrade.BING,
            tags=["ROI", "优化"],
            reporting_system="ROITracker",
        )
        library.submit_cell(
            title="学习洞察",
            content="新策略学习完成",
            wing=LibraryWing.LEARN,
            shelf="learning_insights",
            source=MemorySource.LEARNING_STRATEGY,
            category=MemoryCategory.LEARNING_INSIGHT,
            grade=MemoryGrade.YI,
            tags=["学习", "策略"],
            reporting_system="LearningCoordinator",
            associated_claw="孔子",
        )

    def test_query_by_wing(self, library):
        """测试按分馆查询"""
        results = library.query_cells(wing=LibraryWing.SAGE)
        assert len(results) == 1
        assert results[0].associated_sage == "孔子"

    def test_query_by_grade(self, library):
        """测试按分级查询"""
        results = library.query_cells(grade=MemoryGrade.JIA)
        assert len(results) == 1
        assert results[0].title == "孔子智慧"

    def test_query_by_source(self, library):
        """测试按来源查询"""
        results = library.query_cells(source=MemorySource.ROI_TRACKING)
        assert len(results) == 1
        assert results[0].title == "ROI优化报告"

    def test_query_by_keyword(self, library):
        """测试按关键词查询"""
        results = library.query_cells(keyword="孔子")
        assert len(results) >= 1
        assert any(r.title == "孔子智慧" for r in results)

    def test_query_by_tags(self, library):
        """测试按标签查询"""
        results = library.query_cells(tags=["儒家"])
        assert len(results) == 1
        assert results[0].associated_sage == "孔子"

    def test_query_by_associated_sage(self, library):
        """测试按关联贤者查询"""
        results = library.query_cells(associated_sage="孔子")
        assert len(results) >= 1
        assert all(r.associated_sage == "孔子" for r in results)

    def test_query_by_associated_claw(self, library):
        """测试按关联Claw查询"""
        results = library.query_cells(associated_claw="孔子")
        assert len(results) == 1
        assert results[0].title == "学习洞察"

    def test_query_by_reporting_system(self, library):
        """测试按汇报子系统查询"""
        results = library.query_cells(reporting_system="ROITracker")
        assert len(results) == 1
        assert results[0].source == MemorySource.ROI_TRACKING

    def test_query_limit_and_sort(self, library):
        """测试查询结果限制和排序"""
        results = library.query_cells(limit=2, sort_by="created_at")
        assert len(results) <= 2

    def test_query_min_value_score(self, library):
        """测试价值评分筛选"""
        results = library.query_cells(min_value_score=0.9)
        # 默认value_score=0.5，应该过滤掉
        assert all(r.value_score >= 0.9 for r in results)


# ═══════════════════════════════════════════════════════════════
#  G.3 跨系统桥接测试
# ═══════════════════════════════════════════════════════════════

class TestBridgeInterface:
    """测试跨系统桥接接口"""

    def test_register_bridge(self, library):
        """测试注册桥接"""
        config = {
            "wing": LibraryWing.EXEC,
            "default_shelf": "execution_logs",
            "source": MemorySource.ROI_TRACKING,
            "auto_submit": True,
        }
        result = library.register_bridge("ROITracker", config)
        assert result is True
        assert "ROITracker" in library.get_bridges()

    def test_submit_bridge_memory(self, library):
        """测试通过桥接提交记忆"""
        # 先注册
        library.register_bridge("ROITracker", {
            "wing": LibraryWing.EXEC,
            "default_shelf": "execution_logs",
            "source": MemorySource.ROI_TRACKING,
        })

        # 通过桥接提交
        record = library.submit_bridge_memory(
            subsystem_name="ROITracker",
            title="ROI优化记录",
            content="任务完成，效率提升20%",
            category=MemoryCategory.EXECUTION_LOG,
            tags=["ROI", "测试"],
        )

        assert record is not None
        assert record.associated_sage is None
        assert record.reporting_system == "ROITracker"

    def test_submit_bridge_memory_unregistered_fails(self, library):
        """测试未注册子系统返回None"""
        record = library.submit_bridge_memory(
            subsystem_name="UnknownSystem",
            title="测试",
            content="测试内容",
        )
        assert record is None

    def test_get_bridges(self, library):
        """测试获取已注册桥接"""
        library.register_bridge("ROI", {"wing": LibraryWing.EXEC})
        library.register_bridge("Learning", {"wing": LibraryWing.LEARN})

        bridges = library.get_bridges()
        assert "ROI" in bridges
        assert "Learning" in bridges


# ═══════════════════════════════════════════════════════════════
#  G.4 跨域引用测试
# ═══════════════════════════════════════════════════════════════

class TestCrossReference:
    """测试跨域引用功能"""

    def test_add_cross_reference(self, library, sample_cell_data):
        """测试添加跨域引用"""
        record1 = library.submit_cell(**sample_cell_data)
        sample_cell_data["title"] = "第二条记录"
        sample_cell_data["associated_sage"] = "老子"
        record2 = library.submit_cell(**sample_cell_data)

        result = library.add_cross_reference(record1.id, record2.id)
        assert result is True

        refs = library.get_cross_references(record1.id)
        assert len(refs) == 1
        assert refs[0].id == record2.id

    def test_add_cross_reference_invalid_ids(self, library):
        """测试无效ID添加失败"""
        result = library.add_cross_reference("invalid_id_1", "invalid_id_2")
        assert result is False

    def test_cross_reference_stats(self, library, sample_cell_data):
        """测试跨引用统计"""
        record1 = library.submit_cell(**sample_cell_data)
        sample_cell_data["title"] = "第二条"
        record2 = library.submit_cell(**sample_cell_data)

        library.add_cross_reference(record1.id, record2.id)
        stats = library.get_full_stats()

        assert stats["stats"]["cross_references_created"] == 1


# ═══════════════════════════════════════════════════════════════
#  G.5 持久化测试
# ═══════════════════════════════════════════════════════════════

class TestPersistence:
    """测试持久化功能"""

    def test_persistence_directory_structure(self, library, sample_cell_data, temp_storage):
        """测试持久化目录结构"""
        # 提交记录
        library.submit_cell(**sample_cell_data)
        library.force_save()

        # 检查目录结构
        wings_dir = library._storage_path / "wings"
        assert wings_dir.exists()

        sage_dir = wings_dir / "SAGE" / "sage_profiles"
        assert sage_dir.exists()

    def test_persistence_yaml_file(self, library, sample_cell_data, temp_storage):
        """测试YAML文件持久化"""
        record = library.submit_cell(**sample_cell_data)
        library.force_save()

        # 查找持久化的YAML文件
        sage_dir = library._storage_path / "wings" / "SAGE" / "sage_profiles"
        yaml_files = list(sage_dir.glob("CELL_*.yaml"))
        assert len(yaml_files) >= 1

        # 验证文件内容
        import yaml
        with open(yaml_files[0], "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert data["title"] == sample_cell_data["title"]
        assert data["id"] == record.id

    def test_load_from_disk(self, library, sample_cell_data, temp_storage):
        """测试从磁盘恢复"""
        # 提交并保存
        record = library.submit_cell(**sample_cell_data)
        library.force_save()

        # 创建新实例并加载
        new_lib = ImperialLibrary()
        new_lib._storage_path = library._storage_path
        new_lib._cells.clear()
        new_lib._wing_shelf_index.clear()
        new_lib._cell_counters.clear()
        new_lib._bridges.clear()

        loaded_count = new_lib._load_from_disk_v3()

        # 验证恢复成功
        assert loaded_count >= 1
        restored = new_lib.get_cell(record.id)
        assert restored is not None
        assert restored.title == sample_cell_data["title"]


# ═══════════════════════════════════════════════════════════════
#  G.6 V2兼容层测试
# ═══════════════════════════════════════════════════════════════

class TestV2Compatibility:
    """测试V2兼容层"""

    def test_query_memories_v2_interface(self, library):
        """测试V2的query_memories接口"""
        library.submit_cell(
            title="V2兼容测试",
            content="测试V2兼容层",
            wing=LibraryWing.ARCH,
            shelf="court_decisions",
            source=MemorySource.HISTORICAL_DECISION,
            category=MemoryCategory.ARCHITECTURE,
            reporting_system="TestDept",
        )

        # 使用V2接口查询
        memories = library.query_memories(
            source=MemorySource.HISTORICAL_DECISION,
            department="TestDept",
        )

        assert len(memories) == 1
        assert isinstance(memories[0], MemoryRecord)
        assert memories[0].title == "V2兼容测试"

    def test_get_memory_v2_interface(self, library, sample_cell_data):
        """测试V2的get_memory接口"""
        record = library.submit_cell(**sample_cell_data)

        # 使用V2接口获取
        memory = library.get_memory(record.id)

        assert memory is not None
        assert isinstance(memory, MemoryRecord)
        assert memory.title == sample_cell_data["title"]


# ═══════════════════════════════════════════════════════════════
#  G.7 统计接口测试
# ═══════════════════════════════════════════════════════════════

class TestStatistics:
    """测试统计接口"""

    def test_get_wing_stats(self, library):
        """测试分馆统计"""
        library.submit_cell(
            title="测试1",
            content="内容1",
            wing=LibraryWing.SAGE,
            shelf="sage_profiles",
            grade=MemoryGrade.JIA,
        )
        library.submit_cell(
            title="测试2",
            content="内容2",
            wing=LibraryWing.SAGE,
            shelf="sage_profiles",
            grade=MemoryGrade.YI,
        )

        stats = library.get_wing_stats(LibraryWing.SAGE)

        assert stats["total_cells"] == 2
        assert "shelves" in stats
        assert "sage_profiles" in stats["shelves"]
        assert stats["shelves"]["sage_profiles"]["count"] == 2

    def test_get_full_stats(self, library):
        """测试完整统计"""
        library.submit_cell(
            title="测试",
            content="内容",
            wing=LibraryWing.EXEC,
            shelf="execution_logs",
        )

        stats = library.get_full_stats()

        assert "total_cells" in stats
        assert stats["total_cells"] == 1
        assert "registered_bridges" in stats
        assert "stats" in stats


# ═══════════════════════════════════════════════════════════════
#  G.8 分馆管理测试
# ═══════════════════════════════════════════════════════════════

class TestWingManagement:
    """测试分馆管理"""

    def test_get_wings(self, library):
        """测试获取所有分馆"""
        wings = library.get_wings()
        assert len(wings) == 8  # V1.0 8个分馆
        assert LibraryWing.SAGE in wings
        assert LibraryWing.ARCH in wings
        assert LibraryWing.EXEC in wings

    def test_get_shelves_by_wing(self, library):
        """测试获取分馆的书架列表"""
        shelves = library.get_shelves_by_wing(LibraryWing.SAGE)
        assert "sage_profiles" in shelves
        assert "sage_codes" in shelves

    def test_get_wings_with_counts(self, library):
        """测试获取分馆统计"""
        library.submit_cell(
            title="测试",
            content="内容",
            wing=LibraryWing.LEARN,
            shelf="learning_insights",
        )

        wings_with_counts = library.get_wings_with_counts()
        sage_wing = next(w for w in wings_with_counts if w["wing"] == LibraryWing.LEARN.value)
        assert sage_wing["cell_count"] == 1


# ═══════════════════════════════════════════════════════════════
#  运行入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
