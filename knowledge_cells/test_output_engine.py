"""
测试 OutputEngine v1.0 — 多模态输出引擎
覆盖: 7种格式渲染 + 格式检测 + 引擎集成 + PipelineResult 新字段
"""

import os
import sys
import tempfile
import shutil

# 确保可以导入
sys.path.insert(0, r"d:\AI\somn")

from knowledge_cells.output_engine import (
    OutputEngine,
    OutputFormat,
    OutputArtifact,
    OutputFormatDetector,
    RenderContext,
    TextOutputStrategy,
    MarkdownOutputStrategy,
    HtmlOutputStrategy,
    ImageOutputStrategy,
    PdfOutputStrategy,
    PptxOutputStrategy,
    DocxOutputStrategy,
)


def make_ctx(**overrides) -> RenderContext:
    """构建测试用渲染上下文"""
    defaults = {
        "final_answer": "核心结论：基于多维度分析，建议采取渐进式策略。",
        "metadata": {"demand_type": "分析研究"},
        "confidence": 0.85,
        "grade": "deep",
        "domain": "general",
        "demand_type": "分析研究",
        "decision_method": "太极阴阳决策",
        "reasoning_chain": [
            {"step": "问题识别", "description": "识别核心问题"},
            {"step": "模式匹配", "description": "匹配历史解决方案"},
            {"step": "结论生成", "description": "生成最终建议"},
        ],
        "routing_path": ["SD-P1", "SD-F2", "SD-C1", "SD-D2", "SD-E1"],
        "argumentation_passed": True,
        "argumentation_data": {
            "all_passed": True,
            "r2_argumentation": {"grade": "A", "recommendation": "通过"},
        },
        "optimization_suggestions": ["可增加案例支撑", "建议补充量化数据"],
        "request_id": "TEST001",
        "total_duration_ms": 42.5,
    }
    defaults.update(overrides)
    return RenderContext(**defaults)


def test_output_format_enum():
    """1. OutputFormat 枚举完整性"""
    formats = list(OutputFormat)
    assert len(formats) == 7, f"期望7种格式，实际{len(formats)}种"
    names = {f.value for f in formats}
    expected = {"text", "markdown", "html", "image", "pdf", "pptx", "docx"}
    assert names == expected, f"格式名不匹配: {names - expected}"
    print("  1. OutputFormat 枚举 ✓ (7种格式)")


def test_output_artifact():
    """2. OutputArtifact 数据类"""
    artifact = OutputArtifact(format=OutputFormat.PDF, content=b"%PDF-1.4")
    assert artifact.extension == ".pdf"
    assert artifact.mime_type.startswith("application/pdf")
    assert artifact.size_bytes == 8
    print("  2. OutputArtifact 数据类 ✓")


def test_format_detector():
    """3. OutputFormatDetector 格式检测"""
    # 基础等级映射
    assert OutputFormatDetector.detect("信息查询") == OutputFormat.TEXT
    assert OutputFormatDetector.detect("分析研究") == OutputFormat.MARKDOWN
    assert OutputFormatDetector.detect("战略规划") == OutputFormat.DOCX
    assert OutputFormatDetector.detect("决策选择") == OutputFormat.HTML
    assert OutputFormatDetector.detect("执行落地") == OutputFormat.MARKDOWN
    assert OutputFormatDetector.detect("创新突破") == OutputFormat.PPTX
    assert OutputFormatDetector.detect("论证反驳") == OutputFormat.TEXT
    assert OutputFormatDetector.detect("综合需求") == OutputFormat.MARKDOWN

    # 等级升级
    assert OutputFormatDetector.detect("分析研究", grade="deep") == OutputFormat.HTML
    assert OutputFormatDetector.detect("分析研究", grade="super") == OutputFormat.PDF
    assert OutputFormatDetector.detect("战略规划", grade="deep") == OutputFormat.PDF
    assert OutputFormatDetector.detect("创新突破", grade="super") == OutputFormat.PDF

    # 显式指定覆盖
    assert OutputFormatDetector.detect("分析研究", explicit_format=OutputFormat.PDF) == OutputFormat.PDF
    print("  3. OutputFormatDetector ✓ (基础映射+等级升级+显式覆盖)")


def test_text_strategy():
    """4. TextOutputStrategy"""
    ctx = make_ctx()
    strategy = TextOutputStrategy()
    content = strategy.render(ctx)
    assert isinstance(content, bytes)
    text = content.decode("utf-8")
    assert "SageDispatch" in text
    assert "核心结论" in text
    assert "推理链路" in text
    assert "论证结果" in text
    assert "优化建议" in text
    print("  4. TextOutputStrategy ✓")


def test_markdown_strategy():
    """5. MarkdownOutputStrategy"""
    ctx = make_ctx()
    strategy = MarkdownOutputStrategy()
    content = strategy.render(ctx)
    text = content.decode("utf-8")
    assert "# SageDispatch" in text
    assert "## 核心结论" in text
    assert "## 推理链路" in text
    assert "## 论证结果" in text
    assert "|" in text  # 表格
    assert "**" in text  # 粗体
    print("  5. MarkdownOutputStrategy ✓")


def test_html_strategy():
    """6. HtmlOutputStrategy"""
    ctx = make_ctx()
    strategy = HtmlOutputStrategy()
    content = strategy.render(ctx)
    text = content.decode("utf-8")
    assert "<!DOCTYPE html>" in text
    assert "</html>" in text
    assert "SageDispatch" in text
    assert "conf-fill" in text  # 置信度条
    assert "推理链路" in text
    assert "85.0%" in text  # 置信度
    print("  6. HtmlOutputStrategy ✓")


def test_image_strategy():
    """7. ImageOutputStrategy"""
    ctx = make_ctx()
    strategy = ImageOutputStrategy()
    content = strategy.render(ctx)
    assert isinstance(content, bytes)
    assert content[:8] == b"\x89PNG\r\n\x1a\n"  # PNG 文件头
    assert len(content) > 1000  # 合理大小的图表
    print(f"  7. ImageOutputStrategy ✓ ({len(content)} bytes PNG)")


def test_pdf_strategy():
    """8. PdfOutputStrategy"""
    ctx = make_ctx()
    strategy = PdfOutputStrategy()
    content = strategy.render(ctx)
    assert isinstance(content, bytes)
    assert content[:5] == b"%PDF-"  # PDF 文件头
    assert len(content) > 500
    print(f"  8. PdfOutputStrategy ✓ ({len(content)} bytes PDF)")


def test_pptx_strategy():
    """9. PptxOutputStrategy"""
    ctx = make_ctx()
    strategy = PptxOutputStrategy()
    content = strategy.render(ctx)
    assert isinstance(content, bytes)
    # PPTX 是 ZIP 格式 (PK header)
    assert content[:2] == b"PK"
    assert len(content) > 2000
    print(f"  9. PptxOutputStrategy ✓ ({len(content)} bytes PPTX)")


def test_docx_strategy():
    """10. DocxOutputStrategy"""
    ctx = make_ctx()
    strategy = DocxOutputStrategy()
    content = strategy.render(ctx)
    assert isinstance(content, bytes)
    assert content[:2] == b"PK"  # DOCX 也是 ZIP
    assert len(content) > 2000
    print(f"  10. DocxOutputStrategy ✓ ({len(content)} bytes DOCX)")


def test_engine_render_all_formats():
    """11. OutputEngine 渲染所有格式"""
    engine = OutputEngine()
    ctx = make_ctx()

    for fmt in OutputFormat:
        artifact = engine.render(fmt, ctx)
        assert artifact.format == fmt
        assert artifact.size_bytes > 0
        assert artifact.duration_ms >= 0

    stats = engine.get_stats()
    assert stats["total_renders"] == 7
    print(f"  11. OutputEngine 全格式渲染 ✓ (7/7, stats={stats['by_format']})")


def test_engine_auto_render():
    """12. OutputEngine 自动格式检测+渲染"""
    engine = OutputEngine()
    ctx = make_ctx(demand_type="战略规划", grade="super")
    artifact = engine.auto_render(ctx)
    assert artifact.format == OutputFormat.PPTX  # 战略规划+super → PPTX
    print(f"  12. 自动渲染 ✓ (战略规划+super → {artifact.format.value})")

    ctx2 = make_ctx(demand_type="信息查询", grade="basic")
    artifact2 = engine.auto_render(ctx2)
    assert artifact2.format == OutputFormat.TEXT
    print(f"      自动渲染 ✓ (信息查询+basic → {artifact2.format.value})")


def test_engine_file_output():
    """13. OutputEngine 文件输出"""
    tmp_dir = tempfile.mkdtemp(prefix="tianshu_test_")
    try:
        engine = OutputEngine(output_dir=tmp_dir)
        ctx = make_ctx()
        artifact = engine.render(OutputFormat.HTML, ctx)
        assert artifact.file_path != "", "应该生成文件路径"
        assert os.path.exists(artifact.file_path), f"文件不存在: {artifact.file_path}"
        assert artifact.file_path.endswith(".html")
        print(f"  13. 文件输出 ✓ ({artifact.file_path})")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_render_to_file():
    """14. 策略 render_to_file 方法"""
    tmp_dir = tempfile.mkdtemp(prefix="tianshu_test_")
    try:
        ctx = make_ctx(output_dir=tmp_dir)
        strategy = MarkdownOutputStrategy()
        artifact = strategy.render_to_file(ctx)
        assert artifact.format == OutputFormat.MARKDOWN
        assert os.path.exists(artifact.file_path)
        assert artifact.file_path.endswith(".md")
        print(f"  14. render_to_file ✓ ({artifact.file_path})")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_render_context_from_pipeline():
    """15. RenderContext.from_pipeline_result"""
    from knowledge_cells.eight_layer_pipeline import PipelineResult, ProcessingGrade, DomainCategory

    result = PipelineResult(
        request_id="CTX001",
        grade=ProcessingGrade.DEEP,
        domain=DomainCategory.GENERAL,
        final_answer="测试结论",
        final_confidence=0.9,
        total_duration_ms=100.0,
        reasoning_chain=[{"step": "test", "description": "desc"}],
        routing_path=["SD-P1"],
        metadata={"demand_type": "分析研究"},
    )

    ctx = RenderContext.from_pipeline_result(result, output_dir="/tmp/test")
    assert ctx.final_answer == "测试结论"
    assert ctx.confidence == 0.9
    assert ctx.grade == "deep"
    assert ctx.demand_type == "分析研究"
    assert len(ctx.reasoning_chain) == 1
    assert ctx.output_dir == "/tmp/test"
    print("  15. RenderContext.from_pipeline_result ✓")


def test_pipeline_result_new_fields():
    """16. PipelineResult 新增字段"""
    from knowledge_cells.eight_layer_pipeline import PipelineResult, ProcessingGrade, DomainCategory

    result = PipelineResult(
        request_id="NEW001",
        grade=ProcessingGrade.BASIC,
        domain=DomainCategory.GENERAL,
        final_answer="test",
    )
    assert result.output_format is None  # 默认 None
    assert result.output_artifact is None
    result.output_format = "pdf"
    result.output_artifact = {"test": True}
    assert result.output_format == "pdf"
    assert result.output_artifact == {"test": True}
    print("  16. PipelineResult 新字段 ✓ (output_format + output_artifact)")


def test_empty_context():
    """17. 空上下文渲染（边界情况）"""
    ctx = RenderContext()  # 全部默认值
    engine = OutputEngine()
    # TEXT 格式应该能处理空上下文
    artifact = engine.render(OutputFormat.TEXT, ctx)
    assert artifact.size_bytes > 0
    # MARKDOWN 同样
    artifact2 = engine.render(OutputFormat.MARKDOWN, ctx)
    assert artifact2.size_bytes > 0
    # HTML
    artifact3 = engine.render(OutputFormat.HTML, ctx)
    assert artifact3.size_bytes > 0
    print("  17. 空上下文边界测试 ✓")


def test_supported_formats():
    """18. supported_formats"""
    engine = OutputEngine()
    formats = engine.supported_formats()
    assert len(formats) == 7
    assert "text" in formats
    assert "html" in formats
    assert "pdf" in formats
    print(f"  18. supported_formats ✓ ({formats})")


# ==================== 运行 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("  OutputEngine v1.0 测试")
    print("=" * 60)
    print()

    tests = [
        test_output_format_enum,
        test_output_artifact,
        test_format_detector,
        test_text_strategy,
        test_markdown_strategy,
        test_html_strategy,
        test_image_strategy,
        test_pdf_strategy,
        test_pptx_strategy,
        test_docx_strategy,
        test_engine_render_all_formats,
        test_engine_auto_render,
        test_engine_file_output,
        test_render_to_file,
        test_render_context_from_pipeline,
        test_pipeline_result_new_fields,
        test_empty_context,
        test_supported_formats,
    ]

    passed = 0
    failed = 0
    errors = []

    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            failed += 1
            errors.append((t.__name__, str(e)))
            print(f"  {t.__name__} ✗ {e}")

    print()
    print("=" * 60)
    print(f"  结果: {passed}/{passed + failed} 通过", end="")
    if errors:
        print(f" | {failed} 失败:")
        for name, err in errors:
            print(f"    - {name}: {err[:100]}")
    else:
        print()
    print("=" * 60)
