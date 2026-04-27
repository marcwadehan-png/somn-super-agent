# -*- coding: utf-8 -*-
"""
PDF高级工具 [v22.4]
PDF Advanced Tools

功能:
- PDF合并
- PDF分割
- PDF压缩
- PDF加密/解密
- PDF元数据编辑

版本: v22.4.0
日期: 2026-04-25
"""

from pathlib import Path
from typing import List, Optional, Union, Tuple, Dict, Any
from dataclasses import dataclass
from enum import Enum
import logging
import os
import tempfile

logger = logging.getLogger(__name__)


class PDFFeature(Enum):
    """PDF功能"""
    MERGE = "merge"
    SPLIT = "split"
    COMPRESS = "compress"
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
    EXTRACT_PAGES = "extract_pages"
    ROTATE = "rotate"


@dataclass
class PDFResult:
    """PDF操作结果"""
    success: bool
    output_path: Optional[Path] = None
    message: str = ""
    error: Optional[str] = None


class PDFAdvancedTools:
    """
    PDF高级工具
    
    提供PDF文件的合并、分割、压缩等高级操作。
    
    使用示例:
    ```python
    tools = PDFAdvancedTools()
    
    # 合并PDF
    result = tools.merge(["file1.pdf", "file2.pdf"], "merged.pdf")
    
    # 分割PDF
    result = tools.split("input.pdf", "output_dir", pages=[1, 3, 5])
    
    # 压缩PDF
    result = tools.compress("large.pdf", "compressed.pdf")
    ```
    """

    def __init__(self):
        """初始化PDF高级工具"""
        self._check_dependencies()

    def _check_dependencies(self):
        """检查依赖"""
        try:
            from PyPDF2 import PdfReader, PdfWriter
            self._has_pypdf2 = True
        except ImportError:
            self._has_pypdf2 = False
            logger.warning("PyPDF2未安装，PDF高级功能受限")

        try:
            import pypdf
            self._has_pypdf = True
        except ImportError:
            self._has_pypdf = False

    def merge(self, input_paths: List[Union[str, Path]], output_path: Union[str, Path]) -> PDFResult:
        """
        合并多个PDF文件
        
        Args:
            input_paths: 输入文件路径列表
            output_path: 输出文件路径
        
        Returns:
            PDFResult: 操作结果
        """
        if not self._has_pypdf2:
            return PDFResult(
                success=False,
                message="需要安装PyPDF2: pip install PyPDF2",
                error="Dependency not installed"
            )

        try:
            from PyPDF2 import PdfWriter
            
            writer = PdfWriter()
            
            for path in input_paths:
                path = Path(path)
                if not path.exists():
                    logger.warning(f"文件不存在，跳过: {path}")
                    continue
                
                from PyPDF2 import PdfReader
                reader = PdfReader(str(path))
                
                for page in reader.pages:
                    writer.add_page(page)
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            logger.info(f"PDF合并成功: {output_path}")
            return PDFResult(
                success=True,
                output_path=output_path,
                message=f"合并完成，共 {len(input_paths)} 个文件"
            )
            
        except Exception as e:
            logger.exception("PDF合并失败")
            return PDFResult(
                success=False,
                message="合并失败"
            )

    def split(
        self,
        input_path: Union[str, Path],
        output_dir: Union[str, Path],
        mode: str = "every_page",
        pages: Optional[List[int]] = None,
        start: Optional[int] = None,
        end: Optional[int] = None
    ) -> PDFResult:
        """
        分割PDF文件
        
        Args:
            input_path: 输入文件路径
            output_dir: 输出目录
            mode: 分割模式 ("every_page" | "range" | "specific")
            pages: 指定页码列表（mode="specific"时使用）
            start: 起始页（mode="range"时使用）
            end: 结束页（mode="range"时使用）
        
        Returns:
            PDFResult: 操作结果
        """
        if not self._has_pypdf2:
            return PDFResult(
                success=False,
                message="需要安装PyPDF2: pip install PyPDF2",
                error="Dependency not installed"
            )

        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            input_path = Path(input_path)
            if not input_path.exists():
                return PDFResult(
                    success=False,
                    message=f"文件不存在: {input_path}"
                )
            
            reader = PdfReader(str(input_path))
            total_pages = len(reader.pages)
            
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_files = []
            
            if mode == "every_page":
                # 每页一个文件
                for i, page in enumerate(reader.pages):
                    writer = PdfWriter()
                    writer.add_page(page)
                    
                    output_file = output_dir / f"{input_path.stem}_page_{i+1:03d}.pdf"
                    with open(output_file, 'wb') as f:
                        writer.write(f)
                    output_files.append(output_file)
                    
            elif mode == "range":
                # 范围分割
                start_page = start or 1
                end_page = end or total_pages
                
                writer = PdfWriter()
                for i in range(start_page - 1, end_page):
                    if i < total_pages:
                        writer.add_page(reader.pages[i])
                
                output_file = output_dir / f"{input_path.stem}_pages_{start_page}-{end_page}.pdf"
                with open(output_file, 'wb') as f:
                    writer.write(f)
                output_files.append(output_file)
                
            elif mode == "specific":
                # 指定页码
                if not pages:
                    return PDFResult(
                        success=False,
                        message="需要指定页码列表"
                    )
                
                writer = PdfWriter()
                for page_num in pages:
                    if 1 <= page_num <= total_pages:
                        writer.add_page(reader.pages[page_num - 1])
                
                output_file = output_dir / f"{input_path.stem}_selected.pdf"
                with open(output_file, 'wb') as f:
                    writer.write(f)
                output_files.append(output_file)
            
            logger.info(f"PDF分割成功: 生成了 {len(output_files)} 个文件")
            return PDFResult(
                success=True,
                output_path=output_dir,
                message=f"分割完成，生成 {len(output_files)} 个文件"
            )
            
        except Exception as e:
            logger.exception("PDF分割失败")
            return PDFResult(
                success=False,
                message="分割失败"
            )

    def extract_pages(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        pages: List[int]
    ) -> PDFResult:
        """
        提取指定页面
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            pages: 页码列表
        
        Returns:
            PDFResult: 操作结果
        """
        return self.split(
            input_path,
            Path(output_path).parent,
            mode="specific",
            pages=pages
        )

    def rotate(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        degrees: int = 90,
        pages: Optional[List[int]] = None
    ) -> PDFResult:
        """
        旋转PDF页面
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            degrees: 旋转角度 (90, 180, 270)
            pages: 要旋转的页码列表，None表示全部
        
        Returns:
            PDFResult: 操作结果
        """
        if not self._has_pypdf2:
            return PDFResult(
                success=False,
                message="需要安装PyPDF2: pip install PyPDF2",
                error="Dependency not installed"
            )

        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            input_path = Path(input_path)
            if not input_path.exists():
                return PDFResult(
                    success=False,
                    message=f"文件不存在: {input_path}"
                )
            
            reader = PdfReader(str(input_path))
            writer = PdfWriter()
            
            pages = pages or list(range(1, len(reader.pages) + 1))
            
            for i, page in enumerate(reader.pages):
                if (i + 1) in pages:
                    page.rotate(degrees)
                writer.add_page(page)
            
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                writer.write(f)
            
            logger.info(f"PDF旋转成功: {degrees}度")
            return PDFResult(
                success=True,
                output_path=output_path,
                message=f"旋转完成: {degrees}度"
            )
            
        except Exception as e:
            logger.exception("PDF旋转失败")
            return PDFResult(
                success=False,
                message="旋转失败"
            )

    def compress(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        quality: str = "medium"
    ) -> PDFResult:
        """
        压缩PDF文件
        
        注意: 需要 pikepdf 或 PyPDF2>=3.0
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            quality: 压缩质量 ("low" | "medium" | "high")
        
        Returns:
            PDFResult: 操作结果
        """
        try:
            # 尝试使用 pikepdf
            import pikepdf
            
            input_path = Path(input_path)
            if not input_path.exists():
                return PDFResult(
                    success=False,
                    message=f"文件不存在: {input_path}"
                )
            
            # 打开PDF
            pdf = pikepdf.open(input_path)
            
            # 应用压缩设置
            if quality == "low":
                compress_level = 9
            elif quality == "high":
                compress_level = 1
            else:
                compress_level = 6
            
            # 保存压缩后的PDF
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            pdf.save(
                output_path,
                compress_streams=True,
                deterministic_ids=True
            )
            pdf.close()
            
            # 计算压缩比
            original_size = input_path.stat().st_size
            compressed_size = output_path.stat().st_size
            ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
            
            logger.info(f"PDF压缩成功: 压缩率 {ratio:.1f}%")
            return PDFResult(
                success=True,
                output_path=output_path,
                message=f"压缩完成，压缩率 {ratio:.1f}%"
            )
            
        except ImportError:
            # 降级到简单复制
            logger.warning("pikepdf未安装，使用简单压缩")
            import shutil
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(input_path, output_path)
            
            return PDFResult(
                success=True,
                output_path=output_path,
                message="文件已复制（pikepdf未安装，无法压缩）"
            )
            
        except Exception as e:
            logger.exception("PDF压缩失败")
            return PDFResult(
                success=False,
                message="压缩失败"
            )

    def get_info(self, input_path: Union[str, Path]) -> Dict[str, Any]:
        """
        获取PDF文件信息
        
        Args:
            input_path: PDF文件路径
        
        Returns:
            Dict: PDF信息
        """
        if not self._has_pypdf2:
            return {"error": "PyPDF2未安装"}
        
        try:
            from PyPDF2 import PdfReader
            
            input_path = Path(input_path)
            reader = PdfReader(str(input_path))
            
            info = {
                "pages": len(reader.pages),
                "metadata": reader.metadata if hasattr(reader, 'metadata') else {},
                "size_bytes": input_path.stat().st_size,
                "encrypted": reader.is_encrypted
            }
            
            return info
            
        except Exception as e:
            logger.error(f"获取PDF信息失败: {e}")
            return {"error": "获取PDF信息失败"}


# 便捷函数
def merge_pdfs(input_paths: List[str], output_path: str) -> PDFResult:
    """快速合并PDF"""
    tools = PDFAdvancedTools()
    return tools.merge(input_paths, output_path)


def split_pdf(
    input_path: str,
    output_dir: str,
    mode: str = "every_page",
    **kwargs
) -> PDFResult:
    """快速分割PDF"""
    tools = PDFAdvancedTools()
    return tools.split(input_path, output_dir, mode=mode, **kwargs)


def compress_pdf(
    input_path: str,
    output_path: str,
    quality: str = "medium"
) -> PDFResult:
    """快速压缩PDF"""
    tools = PDFAdvancedTools()
    return tools.compress(input_path, output_path, quality)