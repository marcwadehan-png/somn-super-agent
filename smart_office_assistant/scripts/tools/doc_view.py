#!/usr/bin/env python
"""
文档查看器命令行工具
用法:
    python doc_view.py <file_path>              # 查看文档内容
    python doc_view.py <file_path> --info       # 仅显示元数据
    python doc_view.py <file_path> --ocr        # 对图片/PDF执行OCR
    python doc_view.py <file_path> --extract    # 解压压缩包
    python doc_view.py <file_path> --list       # 列出压缩包内容
    python doc_view.py <file_path> --pages 1-5 # 提取PDF指定页面
"""

import sys
import os
import argparse

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__)


from src.documents.document_viewer import (
    DocumentViewer, view_document, get_document_info,
    extract_text_from_pdf, ocr_image
)


def main():
    parser = argparse.ArgumentParser(
        description='通用文档查看器 - 支持多种格式',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('file_path', help='文件路径')
    parser.add_argument('--info', '-i', action='store_true', help='仅显示元数据')
    parser.add_argument('--ocr', '-o', action='store_true', help='对图片/PDF执行OCR')
    parser.add_argument('--extract', '-e', action='store_true', help='解压压缩包')
    parser.add_argument('--list', '-l', action='store_true', help='列出压缩包内容')
    parser.add_argument('--pages', '-p', help='PDF页面范围，如 1-5')
    parser.add_argument('--summary', '-s', action='store_true', help='显示摘要')
    parser.add_argument('--max-length', '-m', type=int, default=3000, help='摘要最大长度')
    
    args = parser.parse_args()
    
    file_path = args.file_path
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)
    
    viewer = DocumentViewer(enable_ocr=True)
    
    # 仅显示元数据
    if args.info:
        metadata = get_document_info(file_path)
        if metadata:
            print("=" * 60)
            print("📄 文档信息")
            print("=" * 60)
            print(f"文件名: {metadata.file_name}")
            print(f"路径: {metadata.file_path}")
            print(f"类型: {metadata.file_type.value}")
            print(f"MIME: {metadata.mime_type}")
            print(f"大小: {metadata.size_display}")
            if metadata.page_count:
                print(f"页数: {metadata.page_count}")
            if metadata.created_time:
                print(f"创建时间: {metadata.created_time}")
            if metadata.modified_time:
                print(f"修改时间: {metadata.modified_time}")
            print("=" * 60)
        else:
            print("❌ 无法获取文档信息")
        return
    
    # 列出压缩包内容
    if args.list:
        contents = viewer.list_archive_contents(file_path)
        if contents:
            print("=" * 60)
            print(f"📁 压缩包内容 (共 {len(contents)} 个文件)")
            print("=" * 60)
            for item in contents:
                size = item.get('size', 0)
                if size < 1024:
                    size_str = f"{size}B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f}KB"
                else:
                    size_str = f"{size/1024/1024:.1f}MB"
                print(f"  📄 {item['name']:<50} {size_str:>10}")
            print("=" * 60)
        return
    
    # 解压压缩包
    if args.extract:
        output_dir = viewer.extract_archive(file_path)
        if output_dir:
            print(f"✅ 已解压到: {output_dir}")
        else:
            print("❌ 解压失败")
        return
    
    # 提取PDF指定页面
    if args.pages:
        pages = []
        for part in args.pages.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(start, end + 1))
            else:
                pages.append(int(part))
        text = extract_text_from_pdf(file_path, pages)
        print(text)
        return
    
    # OCR模式
    if args.ocr:
        metadata = get_document_info(file_path)
        if metadata.file_type.value == 'image':
            text = ocr_image(file_path)
        elif metadata.file_type.value == 'pdf':
            content = view_document(file_path, {'max_pages': 100})
            text = content.ocr_text if content else ""
        else:
            print("❌ OCR仅支持图片和PDF格式")
            return
        
        if text:
            print("=" * 60)
            print("🔤 OCR识别结果")
            print("=" * 60)
            print(text)
            print("=" * 60)
        else:
            print("⚠️ 未识别到文字")
        return
    
    # 默认：显示完整内容
    content = view_document(file_path)
    
    if content:
        # 显示摘要
        if args.summary:
            print(viewer.get_summary(content, args.max_length))
            return
        
        print("=" * 60)
        print(f"📄 {content.metadata.file_name}")
        print(f"📦 类型: {content.metadata.file_type.value}")
        print(f"📏 大小: {content.metadata.size_display}")
        print("=" * 60)
        
        # 文本内容
        if content.text_content:
            print("\n📝 内容:\n")
            print(content.text_content)
        
        # OCR内容
        elif content.ocr_text:
            print("\n🔤 OCR识别内容:\n")
            print(content.ocr_text)
        
        # 表格
        if content.tables:
            print(f"\n📊 表格数: {len(content.tables)}")
        
        # 图片
        if content.images:
            print(f"\n🖼️ 图片数: {len(content.images)}")
        
        # 压缩包
        if content.attachments:
            print(f"\n📁 压缩包文件数: {len(content.attachments)}")
        
        # 警告
        if content.warnings:
            print("\n⚠️ 警告:")
            for w in content.warnings:
                print(f"  - {w}")
        
        print("\n" + "=" * 60)
    else:
        print("❌ 无法读取文档")


if __name__ == '__main__':
    main()
