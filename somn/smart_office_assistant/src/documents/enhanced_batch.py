"""
批量处理增强模块 - v1.0
扩展批量处理功能，支持更多操作类型
"""
from __future__ import annotations

import os
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class BatchOperationType(Enum):
    """批量操作类型"""
    GENERATE = "generate"      # 生成文档
    CONVERT = "convert"        # 格式转换
    MERGE = "merge"            # 合并文档
    SPLIT = "split"            # 拆分文档
    FILL = "fill"              # 填充模板
    EXTRACT = "extract"        # 提取内容
    COMPRESS = "compress"      # 压缩文档
    ENCRYPT = "encrypt"        # 加密文档
    WATERMARK = "watermark"    # 添加水印


@dataclass
class BatchOperation:
    """批量操作定义"""
    id: str
    operation_type: BatchOperationType
    source_files: List[Path]
    output_dir: Path
    options: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    progress: float = 0.0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class EnhancedBatchProcessor:
    """
    增强批量处理器

    支持更多批量操作类型：
    - 批量生成文档
    - 批量格式转换
    - 批量合并/拆分PDF
    - 批量填充模板
    - 批量添加水印
    """

    def __init__(self, max_workers: int = 4, output_dir: Optional[Path] = None):
        """
        初始化批量处理器

        Args:
            max_workers: 最大并发数
            output_dir: 默认输出目录
        """
        self.max_workers = max_workers
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "batch_output"
        self.operations: List[BatchOperation] = []
        self._operation_counter = 0

    def create_merge_operation(
        self,
        source_files: List[str],
        output_dir: Optional[str] = None,
        output_name: str = "merged.pdf",
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        创建批量合并操作

        Args:
            source_files: 源文件列表
            output_dir: 输出目录
            output_name: 输出文件名
            options: 附加选项

        Returns:
            操作ID
        """
        op_id = f"merge_{self._generate_id()}"
        output_path = Path(output_dir) if output_dir else self.output_dir

        operation = BatchOperation(
            id=op_id,
            operation_type=BatchOperationType.MERGE,
            source_files=[Path(f) for f in source_files],
            output_dir=output_path,
            options={
                "output_name": output_name,
                **(options or {})
            }
        )

        self.operations.append(operation)
        return op_id

    def create_split_operation(
        self,
        source_file: str,
        output_dir: Optional[str] = None,
        split_mode: str = "every_page",
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        创建批量拆分操作

        Args:
            source_file: 源文件
            output_dir: 输出目录
            split_mode: 拆分模式 (every_page, range, size)
            options: 附加选项

        Returns:
            操作ID
        """
        op_id = f"split_{self._generate_id()}"
        output_path = Path(output_dir) if output_dir else self.output_dir / "split"

        operation = BatchOperation(
            id=op_id,
            operation_type=BatchOperationType.SPLIT,
            source_files=[Path(source_file)],
            output_dir=output_path,
            options={
                "split_mode": split_mode,
                **(options or {})
            }
        )

        self.operations.append(operation)
        return op_id

    def create_fill_operation(
        self,
        template_file: str,
        data_list: List[Dict[str, Any]],
        output_dir: Optional[str] = None,
        naming_pattern: str = "{index}_{name}"
    ) -> str:
        """
        创建批量填充操作

        Args:
            template_file: 模板文件路径
            data_list: 数据列表，每个元素填充一份文档
            output_dir: 输出目录
            naming_pattern: 命名模式

        Returns:
            操作ID
        """
        op_id = f"fill_{self._generate_id()}"
        output_path = Path(output_dir) if output_dir else self.output_dir

        operation = BatchOperation(
            id=op_id,
            operation_type=BatchOperationType.FILL,
            source_files=[Path(template_file)],
            output_dir=output_path,
            options={
                "data_list": data_list,
                "naming_pattern": naming_pattern
            }
        )

        self.operations.append(operation)
        return op_id

    def create_watermark_operation(
        self,
        source_files: List[str],
        output_dir: Optional[str] = None,
        watermark_text: str = "CONFIDENTIAL",
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        创建批量添加水印操作

        Args:
            source_files: 源文件列表
            output_dir: 输出目录
            watermark_text: 水印文本
            options: 附加选项

        Returns:
            操作ID
        """
        op_id = f"watermark_{self._generate_id()}"
        output_path = Path(output_dir) if output_dir else self.output_dir

        operation = BatchOperation(
            id=op_id,
            operation_type=BatchOperationType.WATERMARK,
            source_files=[Path(f) for f in source_files],
            output_dir=output_path,
            options={
                "watermark_text": watermark_text,
                **(options or {})
            }
        )

        self.operations.append(operation)
        return op_id

    def create_compress_operation(
        self,
        source_files: List[str],
        output_dir: Optional[str] = None,
        quality: str = "medium"
    ) -> str:
        """
        创建批量压缩操作

        Args:
            source_files: 源文件列表
            output_dir: 输出目录
            quality: 压缩质量 (low, medium, high)

        Returns:
            操作ID
        """
        op_id = f"compress_{self._generate_id()}"
        output_path = Path(output_dir) if output_dir else self.output_dir

        operation = BatchOperation(
            id=op_id,
            operation_type=BatchOperationType.COMPRESS,
            source_files=[Path(f) for f in source_files],
            output_dir=output_path,
            options={
                "quality": quality
            }
        )

        self.operations.append(operation)
        return op_id

    def execute_operation(
        self,
        operation_id: str,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Dict[str, Any]:
        """
        执行批量操作

        Args:
            operation_id: 操作ID
            progress_callback: 进度回调函数

        Returns:
            执行结果
        """
        operation = self._get_operation(operation_id)
        if not operation:
            return {
                "success": False,
                "error": f"操作不存在: {operation_id}"
            }

        operation.status = "running"

        try:
            if operation.operation_type == BatchOperationType.MERGE:
                result = self._execute_merge(operation)
            elif operation.operation_type == BatchOperationType.SPLIT:
                result = self._execute_split(operation)
            elif operation.operation_type == BatchOperationType.FILL:
                result = self._execute_fill(operation, progress_callback)
            elif operation.operation_type == BatchOperationType.WATERMARK:
                result = self._execute_watermark(operation, progress_callback)
            elif operation.operation_type == BatchOperationType.COMPRESS:
                result = self._execute_compress(operation, progress_callback)
            else:
                result = {"success": False, "error": f"不支持的操作类型: {operation.operation_type}"}

            operation.result = result
            operation.status = "completed" if result.get("success") else "failed"

            return result

        except Exception as e:
            operation.status = "failed"
            operation.error = "批处理操作失败"
            return {
                "success": False,
                "error": "操作执行失败"
            }

    def execute_all(self, progress_callback: Optional[Callable[[str, float], None]] = None) -> List[Dict[str, Any]]:
        """
        执行所有待处理操作

        Args:
            progress_callback: 进度回调 (operation_id, progress)

        Returns:
            所有操作的结果列表
        """
        results = []

        for operation in self.operations:
            if operation.status == "pending":
                result = self.execute_operation(operation.id,
                    lambda p, op_id=operation.id: progress_callback(op_id, p) if progress_callback else None)
                results.append(result)

        return results

    def _execute_merge(self, operation: BatchOperation) -> Dict[str, Any]:
        """执行合并操作"""
        try:
            from .pdf_tools import PDFAdvancedTools

            tools = PDFAdvancedTools()
            input_files = [str(f) for f in operation.source_files]
            output_path = operation.output_dir / operation.options.get("output_name", "merged.pdf")

            # 确保输出目录存在
            operation.output_dir.mkdir(parents=True, exist_ok=True)

            merge_result = tools.merge(input_files, str(output_path))

            return {
                "success": merge_result.get("success", False),
                "output_path": str(output_path),
                "files_merged": len(input_files),
                "error": merge_result.get("error")
            }

        except ImportError:
            return {
                "success": False,
                "error": "PDF工具未安装"
            }
        except Exception as e:
            return {
                "success": False,
                "error": "操作执行失败"
            }

    def _execute_split(self, operation: BatchOperation) -> Dict[str, Any]:
        """执行拆分操作"""
        try:
            from .pdf_tools import PDFAdvancedTools

            tools = PDFAdvancedTools()
            source_file = str(operation.source_files[0])
            split_mode = operation.options.get("split_mode", "every_page")

            operation.output_dir.mkdir(parents=True, exist_ok=True)

            split_result = tools.split(
                source_file,
                str(operation.output_dir),
                mode=split_mode
            )

            return {
                "success": split_result.get("success", False),
                "output_dir": str(operation.output_dir),
                "pages_split": split_result.get("pages_split", 0),
                "error": split_result.get("error")
            }

        except ImportError:
            return {
                "success": False,
                "error": "PDF工具未安装"
            }
        except Exception as e:
            return {
                "success": False,
                "error": "操作执行失败"
            }

    def _execute_fill(
        self,
        operation: BatchOperation,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Dict[str, Any]:
        """执行批量填充操作"""
        try:
            from .template_filler import TemplateFiller

            filler = TemplateFiller()
            template_file = str(operation.source_files[0])
            data_list = operation.options.get("data_list", [])
            naming_pattern = operation.options.get("naming_pattern", "{index}_{name}")

            operation.output_dir.mkdir(parents=True, exist_ok=True)

            results = []
            for i, data in enumerate(data_list):
                try:
                    output_name = naming_pattern.format(
                        index=i + 1,
                        name=data.get("name", "document")
                    )

                    # 根据模板类型确定扩展名
                    ext = Path(template_file).suffix
                    output_path = operation.output_dir / f"{output_name}{ext}"

                    fill_result = filler.fill_template_file(
                        template_file,
                        data,
                        str(output_path)
                    )

                    results.append({
                        "index": i + 1,
                        "success": fill_result.get("success", False),
                        "output_path": str(output_path)
                    })

                    if progress_callback:
                        progress_callback((i + 1) / len(data_list), f"处理第{i + 1}项")

                except Exception as e:
                    results.append({
                        "index": i + 1,
                        "success": False,
                        "error": "操作执行失败"
                    })

            success_count = sum(1 for r in results if r.get("success"))

            return {
                "success": success_count > 0,
                "total": len(data_list),
                "success_count": success_count,
                "failed_count": len(data_list) - success_count,
                "results": results
            }

        except ImportError:
            return {
                "success": False,
                "error": "模板填充工具未安装"
            }
        except Exception as e:
            return {
                "success": False,
                "error": "操作执行失败"
            }

    def _execute_watermark(
        self,
        operation: BatchOperation,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Dict[str, Any]:
        """执行添加水印操作"""
        try:
            from .pdf_tools import PDFAdvancedTools

            tools = PDFAdvancedTools()
            watermark_text = operation.options.get("watermark_text", "CONFIDENTIAL")

            operation.output_dir.mkdir(parents=True, exist_ok=True)

            results = []
            for i, source_file in enumerate(operation.source_files):
                try:
                    output_path = operation.output_dir / source_file.name
                    add_result = tools.add_watermark(
                        str(source_file),
                        str(output_path),
                        watermark_text
                    )

                    results.append({
                        "file": str(source_file),
                        "success": add_result.get("success", False),
                        "output_path": str(output_path)
                    })

                    if progress_callback:
                        progress_callback((i + 1) / len(operation.source_files), f"处理第{i + 1}项")

                except Exception as e:
                    results.append({
                        "file": str(source_file),
                        "success": False,
                        "error": "操作执行失败"
                    })

            success_count = sum(1 for r in results if r.get("success"))

            return {
                "success": success_count > 0,
                "total": len(operation.source_files),
                "success_count": success_count,
                "failed_count": len(operation.source_files) - success_count,
                "results": results
            }

        except ImportError:
            return {
                "success": False,
                "error": "PDF工具未安装"
            }
        except Exception as e:
            return {
                "success": False,
                "error": "操作执行失败"
            }

    def _execute_compress(
        self,
        operation: BatchOperation,
        progress_callback: Optional[Callable[[float, str], None]] = None
    ) -> Dict[str, Any]:
        """执行压缩操作"""
        try:
            from .pdf_tools import PDFAdvancedTools

            tools = PDFAdvancedTools()
            quality = operation.options.get("quality", "medium")

            operation.output_dir.mkdir(parents=True, exist_ok=True)

            results = []
            original_total = 0
            compressed_total = 0

            for i, source_file in enumerate(operation.source_files):
                try:
                    output_path = operation.output_dir / source_file.name
                    original_size = source_file.stat().st_size

                    compress_result = tools.compress(
                        str(source_file),
                        str(output_path),
                        quality=quality
                    )

                    compressed_size = output_path.stat().st_size if output_path.exists() else 0
                    original_total += original_size
                    compressed_total += compressed_size

                    results.append({
                        "file": str(source_file),
                        "success": compress_result.get("success", False),
                        "original_size": original_size,
                        "compressed_size": compressed_size,
                        "ratio": f"{(1 - compressed_size / original_size) * 100:.1f}%" if original_size > 0 else "N/A"
                    })

                    if progress_callback:
                        progress_callback((i + 1) / len(operation.source_files), f"处理第{i + 1}项")

                except Exception as e:
                    results.append({
                        "file": str(source_file),
                        "success": False,
                        "error": "操作执行失败"
                    })

            success_count = sum(1 for r in results if r.get("success"))

            return {
                "success": success_count > 0,
                "total": len(operation.source_files),
                "success_count": success_count,
                "original_total": original_total,
                "compressed_total": compressed_total,
                "total_ratio": f"{(1 - compressed_total / original_total) * 100:.1f}%" if original_total > 0 else "N/A",
                "results": results
            }

        except ImportError:
            return {
                "success": False,
                "error": "PDF工具未安装"
            }
        except Exception as e:
            return {
                "success": False,
                "error": "操作执行失败"
            }

    def _get_operation(self, operation_id: str) -> Optional[BatchOperation]:
        """获取操作实例"""
        for op in self.operations:
            if op.id == operation_id:
                return op
        return None

    def _generate_id(self) -> str:
        """生成唯一ID"""
        self._operation_counter += 1
        return f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{self._operation_counter}"

    def get_operation_status(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """获取操作状态"""
        operation = self._get_operation(operation_id)
        if not operation:
            return None

        return {
            "id": operation.id,
            "type": operation.operation_type.value,
            "status": operation.status,
            "progress": operation.progress,
            "result": operation.result,
            "error": operation.error
        }

    def list_operations(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出所有操作"""
        operations = []

        for op in self.operations:
            if status_filter and op.status != status_filter:
                continue

            operations.append({
                "id": op.id,
                "type": op.operation_type.value,
                "status": op.status,
                "progress": op.progress,
                "source_count": len(op.source_files)
            })

        return operations

    def cancel_operation(self, operation_id: str) -> bool:
        """取消操作"""
        operation = self._get_operation(operation_id)
        if operation and operation.status == "pending":
            operation.status = "cancelled"
            return True
        return False

    def clear_completed(self) -> int:
        """清理已完成的操作"""
        original_count = len(self.operations)
        self.operations = [op for op in self.operations if op.status not in ("completed", "failed", "cancelled")]
        return original_count - len(self.operations)


# 导出便捷函数
def quick_merge(files: List[str], output_path: str) -> Dict[str, Any]:
    """
    快速合并文件

    Args:
        files: 文件列表
        output_path: 输出路径

    Returns:
        合并结果
    """
    processor = EnhancedBatchProcessor()
    op_id = processor.create_merge_operation(files, str(Path(output_path).parent), Path(output_path).name)
    return processor.execute_operation(op_id)


def quick_split(file: str, output_dir: str, mode: str = "every_page") -> Dict[str, Any]:
    """
    快速拆分文件

    Args:
        file: 源文件
        output_dir: 输出目录
        mode: 拆分模式

    Returns:
        拆分结果
    """
    processor = EnhancedBatchProcessor()
    op_id = processor.create_split_operation(file, output_dir, mode)
    return processor.execute_operation(op_id)


def batch_fill(template: str, data_list: List[Dict[str, Any]], output_dir: str) -> Dict[str, Any]:
    """
    批量填充模板

    Args:
        template: 模板文件
        data_list: 数据列表
        output_dir: 输出目录

    Returns:
        填充结果
    """
    processor = EnhancedBatchProcessor()
    op_id = processor.create_fill_operation(template, data_list, output_dir)
    return processor.execute_operation(op_id)