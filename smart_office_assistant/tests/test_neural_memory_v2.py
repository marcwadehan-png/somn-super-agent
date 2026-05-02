# -*- coding: utf-8 -*-
"""
NeuralMemory v2.0 集成测试
============================
验证 G-1~G-8 所有模块的代码级协作能力：

  G-1: 统一记忆分级体系 (memory_types.py + _imperial_library.py)
  G-3: Claw贤者动态注册 (_library_staff_registry.py)
  G-5: 语义向量编码器 (_semantic_encoder.py)
  G-7: 定时审查调度器 (_library_review_scheduler.py)

运行方式:
    cd d:\AI\somn\smart_office_assistant\src && python ../tests/test_neural_memory_v2.py
"""

from __future__ import annotations

import os
import sys
import time

# ── 路径设置：src/ 作为包根 ──
_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR = os.path.join(_TEST_DIR, "..", "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, os.path.abspath(_SRC_DIR))


# ═══════════════════════════════════════════════════════════════
#  测试工具
# ═══════════════════════════════════════════════════════════════

_passed = 0
_failed = 0
_errors = []


def _check(condition, name):
    global _passed, _failed
    if condition:
        _passed += 1
        print(f"  ✅ {name}")
    else:
        _failed += 1
        _errors.append(name)
        print(f"  ❌ {name}")


def _section(title):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


# ═══════════════════════════════════════════════════════════════
#  G-1: 统一记忆分级体系
# ═══════════════════════════════════════════════════════════════

def test_g1_memory_grades():
    """G-1: MemoryGrade + CellRecord.tier 字段 (v2.0)"""
    _section("G-1: 统一记忆分级体系")

    try:
        from intelligence.dispatcher.wisdom_dispatch._imperial_library import (
            MemoryGrade,
            LibraryWing,
            CellRecord,
            MemorySource,
            MemoryCategory,
        )

        # 验证枚举存在
        grades = list(MemoryGrade)
        wings = list(LibraryWing)
        sources = list(MemorySource)
        categories = list(MemoryCategory)
        _check(len(grades) == 4, f"MemoryGrade: {len(grades)} 级 (甲乙丙丁)")
        _check(len(wings) == 8, f"LibraryWing: {len(wings)} 个分馆")
        _check(len(sources) >= 20, f"MemorySource: {len(sources)} 种来源")
        _check(len(categories) >= 10, f"MemoryCategory: {len(categories)} 种分类")

        # CellRecord 包含 tier 字段 (v2.0 G-1)
        sample = CellRecord(
            id="test_g1_001",
            wing="SAGE", shelf="CAPABILITY",
            cell_index=1, title="测试记忆", content="这是一段测试内容",
            grade=MemoryGrade.JIA,
            source=MemorySource.NEURAL_MEMORY,
            category=MemoryCategory.METHODOLOGY,
            reporting_system="test",
        )
        _check(hasattr(sample, 'tier'), "CellRecord 含 tier 字段 [v2.0 G-1]")
        _check(sample.grade == MemoryGrade.JIA, "MemoryGrade.JIA 赋值正确")
        _check(str(sample.id) == "test_g1_001", "ID 正确")

    except Exception as e:
        _check(False, f"G-1 异常: {e}")


# ═══════════════════════════════════════════════════════════════
#  G-3: Claw贤者动态注册表
# ═══════════════════════════════════════════════════════════════

def test_g3_staff_registry():
    """G-3: StaffRegistry 动态注册/查询/注销"""
    _section("G-3: Claw贤者动态注册表")

    try:
        from intelligence.dispatcher.wisdom_dispatch._library_staff_registry import (
            LibraryStaffRegistry,
            LibraryStaffRecord,
            get_staff_registry,
            StaffRole,
            StaffType,
        )

        registry = get_staff_registry()
        _check(isinstance(registry, LibraryStaffRegistry), "获取全局单例")

        # 默认注册表有人员（ensure_initialized 触发懒加载）
        registry.ensure_initialized()
        all_names_with_write = registry.list_all_names_with_write()
        _check(isinstance(all_names_with_write, set),
               f"list_all_names_with_write() 返回 set ({len(all_names_with_write)} 人)")

        # 查询 SHILANG 角色（侍郎 = WRITE 权限，默认有注册）
        staff_shilang = registry.get_staff_by_role(StaffRole.SHILANG)
        _check(len(staff_shilang) > 0, f"SHILANG(侍郎) 角色: {len(staff_shilang)} 人")

        # 动态注册新人员（测试用）
        result = registry.register(
            name="__test_claw__",
            claw_id="TestClaw",
            role=StaffRole.XIUXIU,
            staff_type=StaffType.AGENT,
        )
        _check(result is not None and isinstance(result, LibraryStaffRecord), f"register() 返回 LibraryStaffRecord: {result.name}")

        # 注销测试用户
        try:
            registry.remove("__test_claw__")
        except AttributeError:
            registry._staff.pop("__test_claw__", None)
        after = registry.get_staff("__test_claw__")
        _check(after is None, "注销后查询返回 None")

    except Exception as e:
        _check(False, f"G-3 异常: {e}")


# ═══════════════════════════════════════════════════════════════
#  G-5: 语义向量编码器
# ═══════════════════════════════════════════════════════════════

def test_g5_semantic_encoder():
    """G-5: SemanticEncoder 编码 + 批量编码 + 相似度"""
    _section("G-5: 语义向量编码器 (TF-IDF + Hashing)")

    try:
        from intelligence.dispatcher.wisdom_dispatch._semantic_encoder import (
            SemanticEncoder,
            EncoderConfig,
            EncodingResult,
            get_semantic_encoder,
            encode_text,
            batch_encode_texts,
        )

        # 单例模式
        enc = get_semantic_encoder()
        _check(isinstance(enc, SemanticEncoder), "get_semantic_encoder() 返回实例")

        # 编码文本
        result = encode_text("这是一段关于营销策略的记忆内容")
        _check(isinstance(result, list), "编码结果为 list")
        _check(len(result) > 0, f"编码维度 = {len(result)}")
        _check(all(isinstance(v, float) for v in result), "所有值为 float")

        # 相似度计算方法存在且返回有效范围
        r1 = encode_text("直播运营增长策略方案")
        r2 = encode_text("短视频带货执行计划")
        sim = enc.similarity(r1, r2)
        _check(isinstance(sim, float) and 0 <= sim <= 1,
               f"similarity() 返回 [{sim:.4f}] ∈ [0, 1]")

        # 完全相同的文本应该 similarity = 1.0
        same_sim = enc.similarity(r1, r1)
        _check(abs(same_sim - 1.0) < 1e-6,
               f"相同向量 similarity ≈ 1.0 (实际={same_sim:.6f})")

        # 批量编码
        batch_result = batch_encode_texts(["测试一", "测试二", "测试三"])
        _check(len(batch_result) == 3, f"批量编码: {len(batch_result)} 条")
        _check(all(isinstance(v, list) and len(v) > 0 for v in batch_result),
               "所有批处理结果均为非空列表")

    except Exception as e:
        _check(False, f"G-5 异常: {e}")


# ═══════════════════════════════════════════════════════════════
#  G-7: 定时审查调度器
# ═══════════════════════════════════════════════════════════════

def test_g7_review_scheduler():
    """G-7: ReviewScheduler 初始化与接口验证"""
    _section("G-7: 定时审查调度器")

    try:
        from intelligence.dispatcher.wisdom_dispatch._library_review_scheduler import (
            LibraryReviewScheduler,
            get_review_scheduler,
            run_once as run_review_once,
            ReviewAction,
            ReviewTask,
            ReviewResult,
        )

        scheduler = get_review_scheduler()
        _check(isinstance(scheduler, LibraryReviewScheduler), "获取全局单例")

        # v2.0 新增方法验证
        _check(hasattr(scheduler, 'bind_library'), "bind_library() 方法存在 [v2.0 新增]")
        _check(hasattr(scheduler, 'start_background'), "start_background() 方法存在")
        _check(hasattr(scheduler, 'run_review'), "run_review() 方法存在")

        # 枚举验证 — 使用 dir/属性而非直接迭代（兼容 Enum 子类）
        action_names = [m.name for m in ReviewAction]
        task_fields = [f.name for f in __import__('dataclasses').fields(ReviewTask)]
        _check(len(action_names) >= 4,
               f"ReviewAction: {action_names} ({len(action_names)} 种)")
        _check('cell_id' in task_fields and 'action' in task_fields,
               f"ReviewTask 字段: {task_fields}")

        # TTL 配置验证
        ttl_config = scheduler.GRADE_TTL_DAYS
        _check("甲级" in ttl_config, f"TTL配置含 甲级: {list(ttl_config.keys())}")
        _check(ttl_config["丁级"]["ttl"] == 7,
               f"丁级 TTL = {ttl_config['丁级']['ttl']} 天")

    except Exception as e:
        _check(False, f"G-7 异常: {e}")


# ═══════════════════════════════════════════════════════════════
#  G-1+G-3+G-5+G-7 联合集成：藏书阁完整生命周期
# ═══════════════════════════════════════════════════════════════

def test_full_lifecycle():
    """联合集成：ImperialLibrary → 自动编码(G-5) → 权限(G-3) → 审查(G-7)"""
    _section("联合集成：藏书阁完整生命周期 (G-1+G-3+G-5+G-7)")

    try:
        from intelligence.dispatcher.wisdom_dispatch._imperial_library import (
            ImperialLibrary,
            MemoryGrade,
            MemorySource,
            MemoryCategory,
            LibraryWing,
        )
        from intelligence.dispatcher.wisdom_dispatch._library_staff_registry import (
            StaffRole,
        )
        from intelligence.dispatcher.wisdom_dispatch._semantic_encoder import (
            get_semantic_encoder,
        )
        from intelligence.dispatcher.wisdom_dispatch._library_review_scheduler import (
            get_review_scheduler,
        )

        # ① 创建藏书阁（自动启动 G-7 调度器）
        library = ImperialLibrary()
        _check(library is not None, "① ImperialLibrary 实例化成功")

        # ② G-7 调度器是否已自动绑定（v2.0 __init__ 中自动启动）
        has_scheduler = getattr(library, '_review_scheduler', None) is not None
        _check(has_scheduler, "② G-7 定时审查调度器已自动绑定")

        # ③ 提交一条记忆（触发 G-5 自动语义编码）
        cell_id = library.submit_cell(
            title="NeuralMemory v2.0 集成测试",
            content="神经记忆系统v2.0集成测试：验证G-5自动语义编码和G-1记忆分级。",
            wing=LibraryWing.SAGE,
            shelf="CAPABILITY",
            source=MemorySource.NEURAL_MEMORY,
            category=MemoryCategory.METHODOLOGY,
            reporting_system="test",
            suggested_grade=MemoryGrade.BING,
            tags=["neural-memory-v2", "integration-test"],
        )
        _check(cell_id is not None, f"③ submit_cell 成功")

        # ④ 验证入库后的记录
        # submit_cell 返回 CellRecord 对象，用 .id 查询
        cell_record_id = cell_id.id if hasattr(cell_id, 'id') else cell_id
        record = library.get_cell(str(cell_record_id))
        _check(record is not None, f"④ get_cell('{cell_record_id}') 返回记录")
        _check(record.title == "NeuralMemory v2.0 集成测试", "标题匹配")
        # value_score 由藏书阁内部评估决定，非传入值
        _check(record.value_score > 0, f"value_score = {record.value_score}（内部评估）")

        # ⑤ 验证 G-5 语义编码结果（入库时自动编码）
        embedding = getattr(record, 'semantic_embedding', None)
        if embedding is not None:
            _check(isinstance(embedding, list) and len(embedding) > 0,
                   f"⑤ G-5 语义编码成功, 维度={len(embedding)}")
        else:
            _check(False, "⑤ G-5 语义向量为空（可能编码失败）")

        # ⑥ G-3 权限检查（通过动态注册表）
        registry = library._get_registry()
        staff_shilang = registry.get_staff_by_role(StaffRole.SHILANG)
        _check(len(staff_shilang) > 0, f"⑥ G-3 注册表查询 SHILANG(侍郎): {len(staff_shilang)}人")

        # ⑦ 语义搜索（使用藏书阁 query_cells 接口）
        try:
            results = library.query_cells(keyword="神经记忆集成测试", limit=5)
            _check(isinstance(results, list),
                   f"⑦ query_cells 返回 {type(results).__name__}, {len(results)} 条")
        except Exception as e:
            _check(False, f"⑦ 搜索接口调用: {e}")

        # ⑧ 清理测试数据（submit_cell 返回 CellRecord，需取 .id）
        cell_record_id = cell_id.id if hasattr(cell_id, 'id') else str(cell_id)
        deleted = library.delete_cell(cell_record_id)
        _check(deleted, f"⑧ delete_cell 清理成功 (id={cell_record_id})")

    except Exception as e:
        import traceback
        _check(False, f"联合集成异常: {e}\n{traceback.format_exc()}")


# ═══════════════════════════════════════════════════════════════
#  __init__.py 导出验证
# ═══════════════════════════════════════════════════════════════

def test_package_exports():
    """验证 wisdom_dispatch/__init__.py 的 v2.0 导出符号完整"""
    _section("__init__.py v2.0 导出验证")

    try:
        import intelligence.dispatcher.wisdom_dispatch as pkg
        import importlib
        importlib.reload(pkg)

        # G-3 符号
        _check(hasattr(pkg, 'LibraryStaffRegistry'), "导出: LibraryStaffRegistry (G-3)")
        _check(hasattr(pkg, 'get_staff_registry'), "导出: get_staff_registry (G-3)")
        _check(hasattr(pkg, 'StaffRole'), "导出: StaffRole (G-3)")
        _check(hasattr(pkg, 'StaffType'), "导出: StaffType (G-3)")
        _check(hasattr(pkg, 'role_names_cn'), "导出: role_names_cn (G-3)")
        _check(hasattr(pkg, 'register_claw_as_staff'), "导出: register_claw_as_staff (G-3)")

        # G-5 符号
        _check(hasattr(pkg, 'SemanticEncoder'), "导出: SemanticEncoder (G-5)")
        _check(hasattr(pkg, 'get_semantic_encoder'), "导出: get_semantic_encoder (G-5)")
        _check(hasattr(pkg, 'encode_text'), "导出: encode_text (G-5)")
        _check(hasattr(pkg, 'batch_encode_texts'), "导出: batch_encode_texts (G-5)")
        _check(hasattr(pkg, 'EncoderConfig'), "导出: EncoderConfig (G-5)")
        _check(hasattr(pkg, 'EncodingResult'), "导出: EncodingResult (G-5)")

        # G-7 符号
        _check(hasattr(pkg, 'LibraryReviewScheduler'), "导出: LibraryReviewScheduler (G-7)")
        _check(hasattr(pkg, 'get_review_scheduler'), "导出: get_review_scheduler (G-7)")
        _check(hasattr(pkg, 'run_review_once'), "导出: run_review_once (G-7)")
        _check(hasattr(pkg, 'ReviewAction'), "导出: ReviewAction (G-7)")
        _check(hasattr(pkg, 'ReviewTask'), "导出: ReviewTask (G-7)")
        _check(hasattr(pkg, 'ReviewResult'), "导出: ReviewResult (G-7)")

    except ImportError as e:
        _check(False, f"导入失败: {e}")
    except Exception as e:
        _check(False, f"导出验证异常: {e}")


# ═══════════════════════════════════════════════════════════════
#  主入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  NeuralMemory v2.0 — 神经记忆系统集成测试")
    print("  G-1 / G-3 / G-5 / G-7 全模块验证")
    print("=" * 60)

    t0 = time.time()

    test_g1_memory_grades()
    test_g3_staff_registry()
    test_g5_semantic_encoder()
    test_g7_review_scheduler()
    test_full_lifecycle()
    test_package_exports()

    elapsed = time.time() - t0

    total = _passed + _failed
    print("\n" + "=" * 60)
    print(f"  结果: {_passed}/{total} 通过, {_failed} 失败 ({elapsed:.1f}s)")
    if _errors:
        print(f"\n  失败项:")
        for err in _errors:
            print(f"    ❌ {err}")
    else:
        print(f"\n  🎉 全部通过！NeuralMemory v2.0 集成正常")
    print("=" * 60)

    sys.exit(0 if _failed == 0 else 1)
