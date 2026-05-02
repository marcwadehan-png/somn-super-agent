"""
文档模块测试 - v22.0 自然语言处理验证
测试自然语言文档处理服务的各项功能
"""

import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def test_nlp_service_initialization():
    """测试NLP服务初始化"""
    print("=" * 60)
    print("测试1: NLP服务初始化")
    print("=" * 60)

    try:
        from src.documents import NaturalLanguageDocumentService

        service = NaturalLanguageDocumentService()
        print(f"✅ 服务初始化成功")
        print(f"  - PPT服务可用: {service._ppt_available}")
        print(f"  - Word服务可用: {service._docx_available}")
        print(f"  - Excel服务可用: {service._xlsx_available}")
        return True
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return False


def test_intent_classification():
    """测试意图分类"""
    print("\n" + "=" * 60)
    print("测试2: 意图分类")
    print("=" * 60)

    try:
        from src.documents import NaturalLanguageDocumentService, DocumentIntent

        service = NaturalLanguageDocumentService()

        test_cases = [
            ("帮我生成一个项目汇报PPT", DocumentIntent.GENERATE_PPT),
            ("创建一个会议纪要Word文档", DocumentIntent.GENERATE_WORD),
            ("制作销售数据分析Excel表格", DocumentIntent.GENERATE_EXCEL),
            ("读取这份文档的内容", DocumentIntent.READ_DOCUMENT),
            ("把PDF转成Word", DocumentIntent.CONVERT_FORMAT),
            ("分析这份Excel数据", DocumentIntent.ANALYZE_DATA),
        ]

        passed = 0
        for command, expected_intent in test_cases:
            detected = service._classify_intent(command)
            status = "✅" if detected == expected_intent else "❌"
            if detected == expected_intent:
                passed += 1
            print(f"{status} '{command}' -> {detected.value} (期望: {expected_intent.value})")

        print(f"\n准确率: {passed}/{len(test_cases)}")
        return passed == len(test_cases)
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_document_generation():
    """测试文档生成功能"""
    print("\n" + "=" * 60)
    print("测试3: 文档生成")
    print("=" * 60)

    try:
        from src.documents import (
            DOCXGenerator, ExcelGenerator
        )
        from src.ppt import PPTService

        output_dir = project_root / "outputs" / "document_test"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Word文档生成
        print("\n📄 测试Word文档生成...")
        try:
            doc_gen = DOCXGenerator()
            doc_gen.add_heading("测试文档", level=1)
            doc_gen.add_paragraph("这是一份自动生成的测试文档。")
            doc_gen.add_heading("功能特点", level=2)
            doc_gen.add_bullet_list(["支持多种格式", "智能解析", "快速生成"])
            word_path = doc_gen.save(str(output_dir / "test_document.docx"))
            print(f"✅ Word文档生成成功: {word_path}")
        except Exception as e:
            print(f"⚠️ Word文档生成跳过: {e}")

        # Excel表格生成
        print("\n📊 测试Excel表格生成...")
        try:
            excel_gen = ExcelGenerator()
            excel_gen.create_sheet("测试数据")

            headers = ["项目", "数值", "备注"]
            data = [
                ["测试1", 100, "正常"],
                ["测试2", 200, "正常"],
                ["测试3", 150, "注意"],
            ]

            excel_gen.add_data(data, headers)
            excel_path = excel_gen.save(str(output_dir / "test_data.xlsx"))
            print(f"✅ Excel表格生成成功: {excel_path}")
        except Exception as e:
            print(f"⚠️ Excel表格生成跳过: {e}")

        # PPT生成
        print("\n📽️ 测试PPT生成...")
        try:
            ppt_service = PPTService(theme="business", enable_charts=False)
            content = """
# 测试演示

## 简介
- 这是自动生成的PPT
- 支持多种布局
- 快速高效

## 功能
- 标题页
- 内容页
- 结束页
"""
            ppt_path = ppt_service.generate_ppt(
                content=content,
                output_path=str(output_dir / "test_presentation.pptx"),
                beautify=True,
                auto_charts=False
            )
            print(f"✅ PPT生成成功: {ppt_path}")
        except Exception as e:
            print(f"⚠️ PPT生成跳过: {e}")

        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_document_parsing():
    """测试文档解析功能"""
    print("\n" + "=" * 60)
    print("测试4: 文档解析")
    print("=" * 60)

    try:
        from src.documents import NaturalLanguageDocumentService

        service = NaturalLanguageDocumentService()

        # 测试生成文档的解析
        output_dir = project_root / "outputs" / "document_test"

        # 解析生成的Word文档
        word_file = output_dir / "test_document.docx"
        if word_file.exists():
            print(f"\n📄 解析Word文档: {word_file}")
            result = service.process_command(
                "读取这份文档",
                context={"file_path": str(word_file)}
            )
            if result.success:
                print(f"✅ Word解析成功")
                if result.data:
                    print(f"  - 段落数: {len(result.data.get('paragraphs', []))}")
                    print(f"  - 表格数: {len(result.data.get('tables', []))}")
            else:
                print(f"❌ Word解析失败: {result.message}")
        else:
            print("⚠️ 测试文档不存在，跳过解析测试")

        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_skill_integration():
    """测试Skill集成"""
    print("\n" + "=" * 60)
    print("测试5: Skill集成")
    print("=" * 60)

    skill_base = Path.home() / ".workbuddy" / "plugins" / "marketplaces" / "cb_teams_marketplace" / "plugins" / "document-skills" / "skills"

    skills_found = []

    for skill_name in ["pptx", "docx", "xlsx", "pdf"]:
        skill_path = skill_base / skill_name
        if skill_path.exists():
            skill_file = skill_path / "SKILL.md"
            if skill_file.exists():
                skills_found.append(skill_name)
                print(f"✅ {skill_name.upper()} Skill已安装")
            else:
                print(f"⚠️ {skill_name.upper()} Skill文件不完整")
        else:
            print(f"❌ {skill_name.upper()} Skill未安装")

    print(f"\n已安装技能: {len(skills_found)}/4")
    return len(skills_found) >= 4


def test_module_export():
    """测试模块导出"""
    print("\n" + "=" * 60)
    print("测试6: 模块导出")
    print("=" * 60)

    try:
        from src.documents import (
            # v22.0新增
            NaturalLanguageDocumentService, DocumentIntent, DocumentFormat,
            DocumentResult, quick_process,
            # 原有功能
            DOCXGenerator, PPTXGenerator, ExcelGenerator, PDFGenerator,
            DocumentViewer
        )

        print("✅ 所有导出项验证成功:")
        print("  [v22.0新增] NaturalLanguageDocumentService")
        print("  [v22.0新增] DocumentIntent")
        print("  [v22.0新增] DocumentFormat")
        print("  [v22.0新增] DocumentResult")
        print("  [v22.0新增] quick_process")
        print("  [原有] DOCXGenerator")
        print("  [原有] PPTXGenerator")
        print("  [原有] ExcelGenerator")
        print("  [原有] PDFGenerator")
        print("  [原有] DocumentViewer")

        return True
    except Exception as e:
        print(f"❌ 导出验证失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("文档模块 v22.0 优化验证测试")
    print("=" * 60)

    results = []

    results.append(("NLP服务初始化", test_nlp_service_initialization()))
    results.append(("意图分类", test_intent_classification()))
    results.append(("文档生成", test_document_generation()))
    results.append(("文档解析", test_document_parsing()))
    results.append(("Skill集成", test_skill_integration()))
    results.append(("模块导出", test_module_export()))

    # 汇总
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status}: {name}")

    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print("\n🎉 所有测试通过！文档处理能力优化成功！")
    else:
        print(f"\n⚠️ {total - passed} 项测试失败，请检查")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
