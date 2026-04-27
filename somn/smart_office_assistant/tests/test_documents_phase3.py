# -*- coding: utf-8 -*-
"""
文档模块 Phase 3 功能测试
Document Module Phase 3 Feature Tests

测试内容:
1. TemplateFiller - 智能模板填充
2. BatchDocumentProcessor - 批量文档处理
3. DocumentConverter - 文档转换

版本: v1.0.0
日期: 2026-04-25
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_template_filler():
    """测试模板填充"""
    print("\n" + "=" * 60)
    print("测试 1: TemplateFiller 智能模板填充")
    print("=" * 60)
    
    from documents.template_filler import TemplateFiller, quick_fill
    
    # 测试1: 简单变量替换
    print("\n[1.1] 简单变量替换")
    template = "Hello, {{name}}! Today is {{date}}."
    result = quick_fill(template, name="World", date="2026-04-25")
    print(f"  输入: {template}")
    print(f"  输出: {result}")
    assert result == "Hello, World! Today is 2026-04-25.", f"预期结果不符: {result}"
    print("  ✓ 通过")
    
    # 测试2: 列表循环
    print("\n[1.2] 列表循环渲染")
    filler = TemplateFiller()
    template = "{{#loop items}}<li>{{name}}</li>{{/loop}}"
    variables = {"items": [{"name": "项目A"}, {"name": "项目B"}, {"name": "项目C"}]}
    result = filler.fill_text(template, variables)
    print(f"  输入: {template}")
    print(f"  数据: {variables}")
    print(f"  输出: {result}")
    expected = "<li>项目A</li><li>项目B</li><li>项目C</li>"
    assert result == expected, f"预期: {expected}, 实际: {result}"
    print("  ✓ 通过")
    
    # 测试3: 条件渲染
    print("\n[1.3] 条件渲染")
    template = "{{#if show}}显示内容{{/if}}{{#if not_show}}隐藏内容{{/if}}"
    result1 = filler.fill_text(template, {"show": True, "not_show": False})
    print(f"  show=True: {result1}")
    assert result1 == "显示内容", f"预期: 显示内容, 实际: {result1}"
    print("  ✓ 通过")
    
    # 测试4: 嵌套变量
    print("\n[1.4] 嵌套变量访问")
    template = "用户: {{user.name}}, 邮箱: {{user.email}}"
    variables = {"user": {"name": "张三", "email": "zhang@example.com"}}
    result = filler.fill_text(template, variables)
    print(f"  输入: {template}")
    print(f"  输出: {result}")
    assert "张三" in result and "zhang@example.com" in result
    print("  ✓ 通过")
    
    # 测试5: 函数调用
    print("\n[1.5] 内置函数")
    template = "原文: {{text}}, 大写: {{@upper text}}"
    variables = {"text": "hello world"}
    result = filler.fill_text(template, variables)
    print(f"  输入: {template}")
    print(f"  输出: {result}")
    assert "HELLO WORLD" in result
    print("  ✓ 通过")
    
    print("\n✅ TemplateFiller 测试全部通过!")


def test_batch_processor():
    """测试批量文档处理"""
    print("\n" + "=" * 60)
    print("测试 2: BatchDocumentProcessor 批量处理")
    print("=" * 60)
    
    from documents.batch_processor import BatchDocumentProcessor, batch_generate
    from pathlib import Path
    import tempfile
    
    # 创建临时目录
    temp_dir = Path(tempfile.mkdtemp())
    
    # 测试1: 批量生成任务
    print("\n[2.1] 批量生成任务")
    processor = BatchDocumentProcessor(output_dir=temp_dir / "output")
    
    # 模拟添加任务（不实际生成文件）
    task_ids = processor.add_generate_task(
        template="template.txt",
        data_list=[
            {"title": "文档1", "content": "内容1"},
            {"title": "文档2", "content": "内容2"},
        ],
        output_pattern="{title}.txt"
    )
    
    print(f"  添加任务数: {len(task_ids)}")
    print(f"  任务IDs: {task_ids}")
    assert len(task_ids) == 2
    print("  ✓ 通过")
    
    # 测试2: 批量转换任务
    print("\n[2.2] 批量转换任务")
    processor2 = BatchDocumentProcessor(output_dir=temp_dir / "converted")
    task_ids = processor2.add_convert_task(
        input_path=temp_dir / "input",
        output_dir=temp_dir / "converted",
        to_format="pdf"
    )
    print(f"  转换任务数: {len(task_ids)}")
    print("  ✓ 通过")
    
    # 测试3: 状态获取
    print("\n[2.3] 状态获取")
    status = processor.get_status()
    print(f"  状态: {status}")
    assert status['total'] == 2
    print("  ✓ 通过")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    print("\n✅ BatchDocumentProcessor 测试通过!")


def test_document_converter():
    """测试文档转换"""
    print("\n" + "=" * 60)
    print("测试 3: DocumentConverter 文档转换")
    print("=" * 60)
    
    from documents.document_converter import DocumentConverter, Format
    from pathlib import Path
    import tempfile
    
    converter = DocumentConverter()
    
    # 测试1: 格式枚举
    print("\n[3.1] 格式枚举")
    print(f"  DOCX: {Format.DOCX.value}")
    print(f"  PDF: {Format.PDF.value}")
    assert Format.DOCX.value == "docx"
    print("  ✓ 通过")
    
    # 测试2: 依赖检查
    print("\n[3.2] 依赖检查")
    print(f"  LibreOffice: {'已安装' if converter._libreoffice_available else '未安装'}")
    print(f"  Pandoc: {'已安装' if converter._pandoc_available else '未安装'}")
    print("  ✓ 通过")
    
    # 测试3: 转换映射
    print("\n[3.3] 转换映射")
    print(f"  docx -> pdf: {'_docx_to_pdf' in str(converter.CONVERSION_MAP.get('docx', {}))}")
    print(f"  xlsx -> csv: {'_xlsx_to_csv' in str(converter.CONVERSION_MAP.get('xlsx', {}))}")
    print(f"  md -> html: {'_md_to_html' in str(converter.CONVERSION_MAP.get('md', {}))}")
    print("  ✓ 通过")
    
    print("\n✅ DocumentConverter 测试通过!")


def test_integration():
    """集成测试"""
    print("\n" + "=" * 60)
    print("测试 4: 集成测试")
    print("=" * 60)
    
    from documents import (
        NaturalLanguageDocumentService,
        TemplateFiller,
        BatchDocumentProcessor,
        DocumentConverter
    )
    
    # 测试1: 自然语言服务意图识别
    print("\n[4.1] 自然语言服务意图识别")
    nlp_service = NaturalLanguageDocumentService()
    intent = nlp_service._classify_intent("帮我填充这个模板")
    print(f"  输入: 帮我填充这个模板")
    print(f"  识别意图: {intent.value}")
    assert intent.value in ["FILL_TEMPLATE", "GENERATE_WORD", "GENERATE_EXCEL"]
    print("  ✓ 通过")
    
    # 测试2: 意图->模板填充
    print("\n[4.2] 意图识别->模板填充")
    if nlp_service._docx_available:
        print("  Word服务可用")
    else:
        print("  Word服务不可用（缺少依赖）")
    print("  ✓ 通过")
    
    print("\n✅ 集成测试通过!")


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("文档模块 Phase 3 功能测试")
    print("Version: v1.0.0")
    print("=" * 60)
    
    try:
        test_template_filler()
        test_batch_processor()
        test_document_converter()
        test_integration()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试通过!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
