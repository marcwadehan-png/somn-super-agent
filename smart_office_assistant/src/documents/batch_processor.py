# -*- coding: utf-8 -*-
"""
批量文档处理器 [v22.0 Phase 3]
Batch Document Processor

功能:
- 多文件批量生成
- 多文件批量转换
- 批量文档处理任务队列
- 进度跟踪和错误处理

版本: v22.0.0
日期: 2026-04-25
"""

from __future__ import annotations

import os
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum, auto
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态"""
    PENDING = auto()     # 等待中
    RUNNING = auto()     # 执行中
    SUCCESS = auto()     # 成功
    FAILED = auto()       # 失败
    CANCELLED = auto()   # 已取消


@dataclass
class BatchTask:
    """批量任务定义"""
    task_id: str
    task_type: str                      # "generate", "convert", "process"
    input_path: Optional[Path] = None   # 输入文件/目录
    output_path: Optional[Path] = None  # 输出文件/目录
    parameters: Dict[str, Any] = field(default_factory=dict)  # 任务参数
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0               # 进度 0.0-1.0
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


@dataclass
class BatchResult:
    """批量处理结果"""
    total: int
    success: int
    failed: int
    cancelled: int
    results: List[BatchTask]
    duration: float  # 秒
    errors: List[str] = field(default_factory=list)


class BatchDocumentProcessor:
    """
    批量文档处理器
    
    示例:
    ```python
    processor = BatchDocumentProcessor(max_workers=4)
    
    # 批量生成PPT
    processor.add_generate_task(
        template="template.pptx",
        data_list=[
            {"title": "演示A", "content": "内容A"},
            {"title": "演示B", "content": "内容B"},
        ],
        output_dir="output/ppts"
    )
    
    # 批量转换文件
    processor.add_convert_task(
        input_dir="input/docs",
        output_dir="output/pdfs",
        from_format="docx",
        to_format="pdf"
    )
    
    # 执行批量任务
    result = processor.execute()
    print(f"成功: {result.success}/{result.total}")
    ```
    """

    def __init__(
        self,
        max_workers: int = 4,
        output_dir: Optional[Union[str, Path]] = None,
        preserve_structure: bool = True
    ):
        """
        初始化批量处理器
        
        Args:
            max_workers: 最大并发数
            output_dir: 默认输出目录
            preserve_structure: 是否保持目录结构
        """
        self.max_workers = max_workers
        self.default_output_dir = Path(output_dir) if output_dir else Path("output")
        self.preserve_structure = preserve_structure
        
        self.tasks: List[BatchTask] = []
        self._task_counter = 0
        self._callbacks: Dict[str, List[Callable]] = {
            'on_progress': [],
            'on_complete': [],
            'on_error': []
        }

    def _generate_id(self, prefix: str = "task") -> str:
        """生成任务ID"""
        self._task_counter += 1
        return f"{prefix}_{self._task_counter}_{datetime.now().strftime('%H%M%S')}"

    def on_progress(self, callback: Callable[[BatchTask, float], None]) -> None:
        """注册进度回调"""
        self._callbacks['on_progress'].append(callback)

    def on_complete(self, callback: Callable[[BatchTask], None]) -> None:
        """注册完成回调"""
        self._callbacks['on_complete'].append(callback)

    def on_error(self, callback: Callable[[BatchTask, Exception], None]) -> None:
        """注册错误回调"""
        self._callbacks['on_error'].append(callback)

    def _emit(self, event: str, *args) -> None:
        """触发事件"""
        for callback in self._callbacks.get(event, []):
            try:
                callback(*args)
            except Exception as e:
                logger.warning(f"回调执行失败: {e}")

    # ==================== 任务添加方法 ====================

    def add_generate_task(
        self,
        template: Union[str, Path],
        data_list: List[Dict[str, Any]],
        output_pattern: str = "{index}.{ext}",
        output_dir: Optional[Union[str, Path]] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        添加批量生成任务
        
        Args:
            template: 模板文件
            data_list: 数据列表
            output_pattern: 输出文件命名模式
            output_dir: 输出目录
            parameters: 额外参数
        
        Returns:
            任务ID列表
        """
        task_ids = []
        output_dir = Path(output_dir) if output_dir else self.default_output_dir
        
        for i, data in enumerate(data_list):
            task_id = self._generate_id("gen")
            
            # 格式化输出文件名
            ext = Path(template).suffix.lstrip('.')
            output_name = output_pattern.format(
                index=i + 1,
                ext=ext,
                **data
            )
            output_path = output_dir / output_name
            
            task = BatchTask(
                task_id=task_id,
                task_type="generate",
                input_path=Path(template),
                output_path=output_path,
                parameters={
                    'data': data,
                    'template': str(template),
                    **(parameters or {})
                }
            )
            
            self.tasks.append(task)
            task_ids.append(task_id)
        
        return task_ids

    def add_convert_task(
        self,
        input_path: Union[str, Path, List[Union[str, Path]]],
        output_dir: Optional[Union[str, Path]] = None,
        from_format: Optional[str] = None,
        to_format: str = "pdf",
        recursive: bool = False
    ) -> List[str]:
        """
        添加批量转换任务
        
        Args:
            input_path: 输入文件/目录/文件列表
            output_dir: 输出目录
            from_format: 源格式（扩展名，不含点）
            to_format: 目标格式
            recursive: 是否递归处理子目录
        
        Returns:
            任务ID列表
        """
        task_ids = []
        input_path = Path(input_path) if isinstance(input_path, str) else input_path
        output_dir = Path(output_dir) if output_dir else self.default_output_dir
        
        # 收集输入文件
        if isinstance(input_path, list):
            files = [Path(f) for f in input_path]
        elif input_path.is_dir():
            files = []
            pattern = f"**/*.{from_format}" if from_format else "**/*"
            for f in input_path.rglob(pattern) if recursive else input_path.glob(pattern):
                if f.is_file():
                    files.append(f)
        else:
            files = [input_path]
        
        for file_path in files:
            task_id = self._generate_id("conv")
            
            # 确定目标文件路径
            if self.preserve_structure and isinstance(input_path, Path) and input_path.is_dir():
                rel_path = file_path.relative_to(input_path)
                output_path = output_dir / rel_path.with_suffix(f".{to_format}")
            else:
                output_path = output_dir / file_path.with_suffix(f".{to_format}").name
            
            task = BatchTask(
                task_id=task_id,
                task_type="convert",
                input_path=file_path,
                output_path=output_path,
                parameters={
                    'from_format': from_format or file_path.suffix.lstrip('.'),
                    'to_format': to_format
                }
            )
            
            self.tasks.append(task)
            task_ids.append(task_id)
        
        return task_ids

    def add_process_task(
        self,
        input_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        processor_type: str = "analyze",
        parameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        添加文档处理任务
        
        Args:
            input_path: 输入文件
            output_path: 输出文件
            processor_type: 处理类型 (analyze, extract, merge, split)
            parameters: 处理参数
        
        Returns:
            任务ID
        """
        task_id = self._generate_id("proc")
        
        task = BatchTask(
            task_id=task_id,
            task_type="process",
            input_path=Path(input_path),
            output_path=Path(output_path) if output_path else None,
            parameters={
                'processor_type': processor_type,
                **(parameters or {})
            }
        )
        
        self.tasks.append(task)
        return task_id

    def add_copy_task(
        self,
        source: Union[str, Path, List[Union[str, Path]]],
        destination: Union[str, Path],
        overwrite: bool = False
    ) -> str:
        """添加复制任务"""
        task_id = self._generate_id("copy")
        
        task = BatchTask(
            task_id=task_id,
            task_type="copy",
            input_path=Path(source) if not isinstance(source, list) else None,
            output_path=Path(destination),
            parameters={
                'source_list': [str(s) for s in source] if isinstance(source, list) else [str(source)],
                'overwrite': overwrite
            }
        )
        
        self.tasks.append(task)
        return task_id

    def execute(self, stop_on_error: bool = False) -> BatchResult:
        """
        执行所有任务
        
        Args:
            stop_on_error: 遇到错误是否停止
        
        Returns:
            BatchResult: 执行结果
        """
        start_time = datetime.now()
        total = len(self.tasks)
        
        # 按类型分组执行
        for i, task in enumerate(self.tasks):
            task.status = TaskStatus.RUNNING
            task.progress = 0.0
            
            try:
                self._execute_task(task)
                task.status = TaskStatus.SUCCESS
                task.completed_at = datetime.now()
                self._emit('on_complete', task)
                
            except Exception as e:
                logger.error(f"任务 {task.task_id} 执行失败: {e}")
                task.status = TaskStatus.FAILED
                task.error = "操作失败"
                task.completed_at = datetime.now()
                self._emit('on_error', task, e)
                
                if stop_on_error:
                    # 取消剩余任务
                    for remaining in self.tasks[i + 1:]:
                        remaining.status = TaskStatus.CANCELLED
                    break
            
            task.progress = 1.0
        
        duration = (datetime.now() - start_time).total_seconds()
        
        return BatchResult(
            total=total,
            success=sum(1 for t in self.tasks if t.status == TaskStatus.SUCCESS),
            failed=sum(1 for t in self.tasks if t.status == TaskStatus.FAILED),
            cancelled=sum(1 for t in self.tasks if t.status == TaskStatus.CANCELLED),
            results=self.tasks,
            duration=duration
        )

    def _execute_task(self, task: BatchTask) -> None:
        """执行单个任务"""
        if task.task_type == "generate":
            self._execute_generate(task)
        elif task.task_type == "convert":
            self._execute_convert(task)
        elif task.task_type == "process":
            self._execute_process(task)
        elif task.task_type == "copy":
            self._execute_copy(task)

    def _execute_generate(self, task: BatchTask) -> None:
        """执行生成任务"""
        # 确保输出目录存在
        task.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 使用模板填充器
        from .template_filler import TemplateFiller
        filler = TemplateFiller()
        
        result = filler.fill_template_file(
            task.parameters['template'],
            task.parameters['data'],
            task.output_path
        )
        
        if not result.success:
            raise RuntimeError(result.error or "生成失败")

    def _execute_convert(self, task: BatchTask) -> None:
        """执行转换任务"""
        # 确保输出目录存在
        task.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        from_format = task.parameters['from_format']
        to_format = task.parameters['to_format']
        
        # 简单文件复制作为默认实现
        # 实际转换需要特定库支持
        if task.input_path.exists():
            if to_format == "pdf" and from_format in ("docx", "doc"):
                # 需要额外的PDF转换库
                logger.warning(f"格式转换 {from_format} -> {to_format} 需要额外依赖")
                raise NotImplementedError(f"不支持的转换: {from_format} -> {to_format}")
            else:
                # 简单的文件复制
                shutil.copy2(task.input_path, task.output_path)

    def _execute_process(self, task: BatchTask) -> None:
        """执行处理任务"""
        processor_type = task.parameters['processor_type']
        
        if processor_type == "analyze":
            self._analyze_document(task)
        elif processor_type == "extract":
            self._extract_content(task)
        else:
            raise ValueError(f"不支持的处理类型: {processor_type}")

    def _analyze_document(self, task: BatchTask) -> None:
        """分析文档"""
        if not task.input_path or not task.input_path.exists():
            raise FileNotFoundError(f"文件不存在: {task.input_path}")
        
        # 简单的文档分析
        analysis = {
            'file': str(task.input_path),
            'size': task.input_path.stat().st_size,
            'format': task.input_path.suffix,
            'analyzed_at': datetime.now().isoformat()
        }
        
        task.result = analysis
        
        # 如果有输出路径，保存分析结果
        if task.output_path:
            task.output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(task.output_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, ensure_ascii=False, indent=2)

    def _extract_content(self, task: BatchTask) -> None:
        """提取文档内容"""
        if not task.input_path or not task.input_path.exists():
            raise FileNotFoundError(f"文件不存在: {task.input_path}")
        
        # 使用文档查看器提取内容
        try:
            from .document_viewer import DocumentViewer
            viewer = DocumentViewer()
            content = viewer.read_document(task.input_path)
            task.result = content
        except ImportError:
            raise RuntimeError("文档查看器未安装")

    def _execute_copy(self, task: BatchTask) -> None:
        """执行复制任务"""
        for source in task.parameters['source_list']:
            source_path = Path(source)
            if source_path.exists():
                task.output_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, task.output_path / source_path.name)

    def clear(self) -> None:
        """清空所有任务"""
        self.tasks.clear()
        self._task_counter = 0

    def get_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            'total': len(self.tasks),
            'pending': sum(1 for t in self.tasks if t.status == TaskStatus.PENDING),
            'running': sum(1 for t in self.tasks if t.status == TaskStatus.RUNNING),
            'success': sum(1 for t in self.tasks if t.status == TaskStatus.SUCCESS),
            'failed': sum(1 for t in self.tasks if t.status == TaskStatus.FAILED),
            'cancelled': sum(1 for t in self.tasks if t.status == TaskStatus.CANCELLED)
        }


# 便捷函数
def batch_generate(
    template: Union[str, Path],
    data_list: List[Dict[str, Any]],
    output_dir: Union[str, Path] = "output"
) -> BatchResult:
    """快速批量生成"""
    processor = BatchDocumentProcessor(output_dir=output_dir)
    processor.add_generate_task(template, data_list, output_dir=output_dir)
    return processor.execute()


def batch_convert(
    input_path: Union[str, Path],
    output_dir: Union[str, Path] = "output",
    to_format: str = "pdf"
) -> BatchResult:
    """快速批量转换"""
    processor = BatchDocumentProcessor(output_dir=output_dir)
    processor.add_convert_task(input_path, output_dir, to_format=to_format)
    return processor.execute()
