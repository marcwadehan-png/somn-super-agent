"""
============================================
        Learning Plan Engine v1.0
============================================

学习计划引擎 - 自动化深度学习系统

核心功能：
1. 扫描指定文件夹的所有文件
2. 调用大模型深度分析每个文件
3. 将知识存入 DomainNexus（知识域格子）
4. 将记忆存入 NeuralMemory（神经记忆系统）

状态机：
  PENDING → SCANNING → LEARNING → COMPLETED
                ↓           ↓
             PAUSED      PAUSED
                ↓           ↓
            RESUMING   RESUMING
                          ↓
                      CANCELLED

版本: 1.0.0
日期: 2026-04-30
"""

from __future__ import annotations

import json
import time
import uuid
import logging
import threading
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger("Somn.LearningPlan")

# ============================================================
#  数据结构
# ============================================================

class PlanStatus(Enum):
    """学习计划状态"""
    PENDING = "pending"        # 待启动
    SCANNING = "scanning"     # 扫描中
    LEARNING = "learning"     # 学习进行中
    COMPLETED = "completed"  # 已完成
    PAUSED = "paused"        # 已暂停
    CANCELLED = "cancelled"  # 已取消
    ERROR = "error"          # 错误


class FileCategory(Enum):
    """文件分类"""
    DOCUMENT = "document"  # 文档: pdf/doc/txt/md/csv
    CODE = "code"          # 代码: py/js/ts/html/css
    IMAGE = "image"        # 图片: jpg/png/gif
    OTHER = "other"        # 其他


@dataclass
class FileTask:
    """单个文件学习任务"""
    file_path: str
    file_name: str
    category: str
    size: int
    status: str = "pending"   # pending / learning / completed / error
    error: str = ""
    knowledge_stored: int = 0  # 存入 DomainNexus 的知识条数
    memory_stored: int = 0     # 存入 NeuralMemory 的记忆条数
    processed_at: float = 0


@dataclass
class LearningPlan:
    """学习计划"""
    id: str
    name: str
    folder_path: str
    status: str = "pending"
    created_at: float = 0
    updated_at: float = 0
    started_at: float = 0
    completed_at: float = 0
    
    # 配置
    config: Dict[str, Any] = field(default_factory=lambda: {
        "recursive": True,
        "max_file_size_mb": 50,
        "file_types": ["document", "code"],
        "depth": "standard",  # light / standard / deep
        "batch_size": 5,
        "parallel_workers": 2,
    })
    
    # 统计
    total_files: int = 0
    processed_files: int = 0
    success_files: int = 0
    failed_files: int = 0
    total_knowledge: int = 0  # 存入 DomainNexus 总数
    total_memory: int = 0     # 存入 NeuralMemory 总数
    
    # 文件队列
    files: List[Dict[str, Any]] = field(default_factory=list)
    
    # 错误信息
    error_message: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status
        return d
    
    @property
    def progress(self) -> float:
        """学习进度 (0.0 ~ 1.0)"""
        if self.total_files == 0:
            return 0.0
        return round(self.processed_files / self.total_files, 3)
    
    @property
    def progress_percent(self) -> str:
        """进度百分比"""
        return f"{self.progress * 100:.1f}%"


# ============================================================
#  提示词模板
# ============================================================

LEARNING_PROMPT_TEMPLATES = {
    "document": """你是一个专业的学习助手。请深度分析以下文档内容，提取知识和记忆。

## 分析要求

1. **核心知识提取**：
   - 文档的主题是什么？
   - 有哪些核心概念/原理/方法？
   - 有哪些关键要点（至少3条）？

2. **知识关联**：
   - 这些知识与其他领域有什么关联？
   - 可以用哪些标签来标记？（用逗号分隔）

3. **实战洞见**：
   - 有哪些实战案例或应用场景？
   - 有哪些值得记录的洞察？

4. **记忆摘要**：
   - 用一段话总结这份文档的核心价值（50字以内）

## 输出格式（严格按此格式）

```
[KNOWLEDGE]
标签: xxx, xxx
核心要点:
1. xxx
2. xxx
3. xxx
关联领域: xxx, xxx
实战案例: xxx（如果有）

[MEMORY]
摘要: xxx（50字以内）
关键洞察: xxx
```

## 文档内容（文件: {file_name}）
---
{content}
---
""",
    
    "code": """你是一个专业的代码分析助手。请深度分析以下代码，提取知识和记忆。

## 分析要求

1. **代码理解**：
   - 这个代码文件的功能是什么？
   - 使用了什么语言/框架/技术栈？
   - 核心逻辑和算法是什么？

2. **知识提取**：
   - 有哪些值得学习的编程模式/技巧？
   - 有哪些API或工具函数值得记录？
   - 标签标记（如：Python, FastAPI, 设计模式等）

3. **代码洞见**：
   - 代码有什么亮点或最佳实践？
   - 有什么潜在问题或改进建议？

4. **记忆摘要**：
   - 用一段话总结这段代码的价值

## 输出格式（严格按此格式）

```
[KNOWLEDGE]
标签: xxx, xxx
核心要点:
1. xxx（技术要点）
2. xxx
3. xxx
技术栈: xxx, xxx
最佳实践: xxx（如果有）

[MEMORY]
摘要: xxx（50字以内）
关键洞察: xxx
```

## 代码内容（文件: {file_name}）
---
{content}
---
""",
}


# ============================================================
#  核心引擎
# ============================================================

class LearningPlanEngine:
    """
    学习计划引擎 v1.0
    
    使用方式::
    
        engine = LearningPlanEngine()
        
        # 创建计划
        plan = engine.create_plan(
            name="我的学习计划",
            folder_path="d:/文档/AI学习资料",
            config={"recursive": True, "depth": "standard"}
        )
        
        # 启动计划
        engine.start_plan(plan.id)
        
        # 查看进度
        status = engine.get_plan(plan.id)
        print(f"进度: {status.progress_percent}")
        
        # 暂停/恢复/取消
        engine.pause_plan(plan.id)
        engine.resume_plan(plan.id)
        engine.cancel_plan(plan.id)
    """
    
    _instance: Optional["LearningPlanEngine"] = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        
        self._initialized = True
        self._plans: Dict[str, LearningPlan] = {}
        self._running_plan_id: Optional[str] = None
        self._pause_event = threading.Event()
        self._cancel_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        self._executor: Optional[ThreadPoolExecutor] = None
        
        # 数据目录
        self._data_dir = Path(__file__).resolve().parent.parent.parent.parent / "data" / "learning_plans"
        self._data_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载已有计划
        self._load_all_plans()
        
        logger.info(f"[LearningPlanEngine] 初始化完成，共加载 {len(self._plans)} 个计划")

    # ============================================================
    #  计划管理 CRUD
    # ============================================================
    
    def create_plan(
        self,
        name: str,
        folder_path: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> LearningPlan:
        """
        创建学习计划
        
        Args:
            name: 计划名称
            folder_path: 学习文件夹路径
            config: 配置参数
            
        Returns:
            LearningPlan 对象
        """
        plan_id = f"lp_{uuid.uuid4().hex[:12]}"
        now = time.time()
        
        plan = LearningPlan(
            id=plan_id,
            name=name,
            folder_path=str(Path(folder_path).resolve()),
            status=PlanStatus.PENDING.value,
            created_at=now,
            updated_at=now,
            config=config or {},
        )
        
        self._plans[plan_id] = plan
        self._save_plan(plan)
        
        logger.info(f"[LearningPlanEngine] 创建计划: {name} ({plan_id})")
        return plan
    
    def get_plan(self, plan_id: str) -> Optional[LearningPlan]:
        """获取计划详情"""
        return self._plans.get(plan_id)
    
    def list_plans(self, status_filter: Optional[str] = None) -> List[LearningPlan]:
        """
        列出所有计划
        
        Args:
            status_filter: 按状态过滤（如 "running", "completed"）
        """
        plans = list(self._plans.values())
        if status_filter:
            plans = [p for p in plans if p.status == status_filter]
        # 按更新时间倒序
        plans.sort(key=lambda p: p.updated_at, reverse=True)
        return plans
    
    def update_plan(
        self,
        plan_id: str,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> Optional[LearningPlan]:
        """更新计划"""
        plan = self._plans.get(plan_id)
        if not plan:
            return None
        
        if name is not None:
            plan.name = name
        if config is not None:
            plan.config.update(config)
        
        plan.updated_at = time.time()
        self._save_plan(plan)
        return plan
    
    def delete_plan(self, plan_id: str) -> bool:
        """删除计划"""
        if plan_id not in self._plans:
            return False
        
        plan = self._plans[plan_id]
        # 不能删除运行中的计划
        if plan.status in (PlanStatus.SCANNING.value, PlanStatus.LEARNING.value):
            logger.warning(f"[LearningPlanEngine] 无法删除运行中的计划: {plan_id}")
            return False
        
        del self._plans[plan_id]
        self._delete_plan_file(plan_id)
        logger.info(f"[LearningPlanEngine] 删除计划: {plan_id}")
        return True
    
    # ============================================================
    #  计划执行控制
    # ============================================================
    
    def start_plan(self, plan_id: str) -> bool:
        """
        启动学习计划
        
        Args:
            plan_id: 计划ID
            
        Returns:
            是否成功启动
        """
        plan = self._plans.get(plan_id)
        if not plan:
            logger.error(f"[LearningPlanEngine] 计划不存在: {plan_id}")
            return False
        
        if plan.status not in (PlanStatus.PENDING.value, PlanStatus.PAUSED.value, PlanStatus.ERROR.value):
            logger.warning(f"[LearningPlanEngine] 计划状态不允许启动: {plan.status}")
            return False
        
        # 重置暂停/取消事件
        self._pause_event.set()
        self._cancel_event.clear()
        
        plan.status = PlanStatus.SCANNING.value
        plan.started_at = time.time()
        plan.updated_at = time.time()
        plan.error_message = ""
        self._save_plan(plan)
        
        # 启动工作线程
        self._worker_thread = threading.Thread(
            target=self._run_plan,
            args=(plan_id,),
            daemon=True,
            name=f"LearningPlan-{plan_id}"
        )
        self._worker_thread.start()
        
        logger.info(f"[LearningPlanEngine] 启动计划: {plan_id}")
        return True
    
    def pause_plan(self, plan_id: str) -> bool:
        """暂停计划"""
        plan = self._plans.get(plan_id)
        if not plan:
            return False
        
        if plan.status != PlanStatus.LEARNING.value:
            return False
        
        plan.status = PlanStatus.PAUSED.value
        plan.updated_at = time.time()
        self._pause_event.clear()  # 触发暂停
        self._save_plan(plan)
        
        logger.info(f"[LearningPlanEngine] 暂停计划: {plan_id}")
        return True
    
    def resume_plan(self, plan_id: str) -> bool:
        """恢复计划"""
        plan = self._plans.get(plan_id)
        if not plan:
            return False
        
        if plan.status != PlanStatus.PAUSED.value:
            return False
        
        plan.status = PlanStatus.LEARNING.value
        plan.updated_at = time.time()
        self._pause_event.set()  # 解除暂停
        self._save_plan(plan)
        
        logger.info(f"[LearningPlanEngine] 恢复计划: {plan_id}")
        return True
    
    def cancel_plan(self, plan_id: str) -> bool:
        """取消计划"""
        plan = self._plans.get(plan_id)
        if not plan:
            return False
        
        if plan.status in (PlanStatus.COMPLETED.value, PlanStatus.CANCELLED.value):
            return False
        
        plan.status = PlanStatus.CANCELLED.value
        plan.updated_at = time.time()
        self._cancel_event.set()  # 触发取消
        self._save_plan(plan)
        
        logger.info(f"[LearningPlanEngine] 取消计划: {plan_id}")
        return True
    
    # ============================================================
    #  内部执行逻辑
    # ============================================================
    
    def _run_plan(self, plan_id: str):
        """执行计划的内部线程"""
        plan = self._plans.get(plan_id)
        if not plan:
            return
        
        try:
            # 阶段1: 扫描文件
            self._scan_files(plan)
            
            if plan.total_files == 0:
                plan.status = PlanStatus.COMPLETED.value
                plan.error_message = "未找到符合条件的文件"
                self._save_plan(plan)
                return
            
            # 阶段2: 学习文件
            plan.status = PlanStatus.LEARNING.value
            self._save_plan(plan)
            
            self._learn_files(plan)
            
            # 完成
            plan.status = PlanStatus.COMPLETED.value
            plan.completed_at = time.time()
            plan.updated_at = time.time()
            self._save_plan(plan)
            
            logger.info(
                f"[LearningPlanEngine] 计划完成: {plan_id}, "
                f"知识={plan.total_knowledge}, 记忆={plan.total_memory}"
            )
            
        except Exception as e:
            logger.error(f"[LearningPlanEngine] 计划执行异常: {plan_id}, {e}", exc_info=True)
            plan.status = PlanStatus.ERROR.value
            plan.error_message = str(e)
            plan.updated_at = time.time()
            self._save_plan(plan)
    
    def _scan_files(self, plan: LearningPlan):
        """扫描文件夹，生成文件列表"""
        import os
        
        folder = Path(plan.folder_path)
        if not folder.exists():
            raise FileNotFoundError(f"文件夹不存在: {plan.folder_path}")
        
        plan.status = PlanStatus.SCANNING.value
        self._save_plan(plan)
        
        max_size = plan.config.get("max_file_size_mb", 50) * 1024 * 1024
        file_types = set(plan.config.get("file_types", ["document", "code"]))
        recursive = plan.config.get("recursive", True)
        
        # 文件扩展名映射
        ext_map = {
            "document": {".pdf", ".doc", ".docx", ".txt", ".md", ".csv", ".ppt", ".pptx", ".xls", ".xlsx"},
            "code": {".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".java", ".go", ".rs", ".cpp", ".c", ".h", ".rb", ".php", ".swift", ".kt"},
        }
        
        allowed_exts = set()
        if "document" in file_types:
            allowed_exts.update(ext_map["document"])
        if "code" in file_types:
            allowed_exts.update(ext_map["code"])
        
        plan.files = []
        scan_pattern = "**/*" if recursive else "*"
        
        for fpath in folder.glob(scan_pattern):
            if not fpath.is_file():
                continue
            
            ext = fpath.suffix.lower()
            if ext not in allowed_exts:
                continue
            
            size = fpath.stat().st_size
            if size > max_size or size == 0:
                continue
            
            # 分类
            category = FileCategory.OTHER.value
            for cat, exts in ext_map.items():
                if ext in exts:
                    category = cat
                    break
            
            plan.files.append(FileTask(
                file_path=str(fpath),
                file_name=fpath.name,
                category=category,
                size=size,
            ).__dict__)
        
        plan.total_files = len(plan.files)
        plan.processed_files = 0
        plan.success_files = 0
        plan.failed_files = 0
        plan.updated_at = time.time()
        
        logger.info(f"[LearningPlanEngine] 扫描完成: {plan.total_files} 个文件")
    
    def _learn_files(self, plan: LearningPlan):
        """学习所有文件"""
        batch_size = plan.config.get("batch_size", 5)
        parallel_workers = plan.config.get("parallel_workers", 2)
        depth = plan.config.get("depth", "standard")
        
        total = plan.total_files
        for idx, task_dict in enumerate(plan.files):
            # 检查暂停/取消
            if not self._pause_event.is_set():
                plan.status = PlanStatus.PAUSED.value
                self._save_plan(plan)
                self._pause_event.wait()  # 等待恢复
                if plan.status == PlanStatus.CANCELLED.value:
                    return
                plan.status = PlanStatus.LEARNING.value
                self._save_plan(plan)
            
            if self._cancel_event.is_set():
                plan.status = PlanStatus.CANCELLED.value
                self._save_plan(plan)
                return
            
            # 更新进度
            task_dict["status"] = "learning"
            plan.processed_files = idx + 1
            plan.updated_at = time.time()
            
            try:
                result = self._learn_single_file(task_dict, depth)
                task_dict["status"] = "completed"
                task_dict["knowledge_stored"] = result.get("knowledge_count", 0)
                task_dict["memory_stored"] = result.get("memory_count", 0)
                task_dict["processed_at"] = time.time()
                
                plan.success_files += 1
                plan.total_knowledge += result.get("knowledge_count", 0)
                plan.total_memory += result.get("memory_count", 0)
                
            except Exception as e:
                logger.warning(f"[LearningPlanEngine] 文件学习失败: {task_dict['file_path']}, {e}")
                task_dict["status"] = "error"
                task_dict["error"] = str(e)
                plan.failed_files += 1
            
            # 每5个文件保存一次
            if idx % 5 == 0:
                self._save_plan(plan)
        
        self._save_plan(plan)
    
    def _learn_single_file(self, task: Dict[str, Any], depth: str) -> Dict[str, Any]:
        """
        学习单个文件
        
        Returns:
            {"knowledge_count": int, "memory_count": int}
        """
        fpath = Path(task["file_path"])
        category = task["category"]
        file_name = task["file_name"]
        
        # 读取内容
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            raise IOError(f"无法读取文件: {e}")
        
        # 截断大文件（保留前 8000 字符）
        if len(content) > 8000:
            content = content[:8000] + "\n\n... [内容已截断] ..."
        
        # 调用 LLM 分析
        template = LEARNING_PROMPT_TEMPLATES.get(category, LEARNING_PROMPT_TEMPLATES["document"])
        prompt = template.format(file_name=file_name, content=content)
        
        llm_result = self._call_llm(prompt, depth)
        
        # 解析 LLM 结果
        parsed = self._parse_llm_result(llm_result, category)
        
        # 存入 DomainNexus 和 NeuralMemory
        knowledge_count = self._store_to_domain_nexus(parsed, file_name)
        memory_count = self._store_to_neural_memory(parsed, file_name, task["file_path"])
        
        return {
            "knowledge_count": knowledge_count,
            "memory_count": memory_count,
        }
    
    def _call_llm(self, prompt: str, depth: str) -> str:
        """调用大模型"""
        try:
            from llm_unified_config import get_unified_llm_service
            
            service = get_unified_llm_service()
            temp = 0.3 if depth == "light" else (0.7 if depth == "standard" else 0.9)
            
            response = service.chat(
                prompt=prompt,
                system_prompt="你是一个专业的学习助手，擅长深度分析各类文档和代码，提取核心知识和洞见。",
                temperature=temp,
            )
            
            return response.content
            
        except Exception as e:
            logger.warning(f"[LearningPlanEngine] LLM调用失败: {e}")
            raise RuntimeError(f"LLM服务不可用: {e}")
    
    def _parse_llm_result(self, content: str, category: str) -> Dict[str, Any]:
        """解析 LLM 返回内容"""
        result = {
            "tags": [],
            "points": [],
            "associations": [],
            "cases": [],
            "summary": "",
            "insight": "",
            "tech_stack": [],
            "best_practices": [],
        }
        
        if not content:
            return result
        
        # 解析 [KNOWLEDGE] 部分
        if "[KNOWLEDGE]" in content:
            knowledge_part = content.split("[KNOWLEDGE]")[1].split("[MEMORY]")[0] if "[MEMORY]" in content else content.split("[KNOWLEDGE]")[1]
            
            # 标签
            import re
            tag_match = re.search(r"标签[：:]\s*(.+?)(?:\n|$)", knowledge_part)
            if tag_match:
                tags_str = tag_match.group(1).strip()
                result["tags"] = [t.strip() for t in re.split(r"[,，、]", tags_str) if t.strip()]
            
            # 核心要点
            points_match = re.search(r"核心要点[：:]\s*\n((?:\d+\..+?\n?)+)", knowledge_part)
            if points_match:
                points_text = points_match.group(1)
                points = re.findall(r"\d+\.\s*(.+?)(?:\n|$)", points_text)
                result["points"] = [p.strip() for p in points if p.strip()]
            
            # 关联领域
            assoc_match = re.search(r"关联领域[：:]\s*(.+?)(?:\n|$)", knowledge_part)
            if assoc_match:
                result["associations"] = [a.strip() for a in re.split(r"[,，、]", assoc_match.group(1)) if a.strip()]
            
            # 实战案例
            case_match = re.search(r"实战案例[：:]\s*(.+?)(?:\n|$)", knowledge_part)
            if case_match:
                result["cases"] = [c.strip() for c in case_match.group(1).split("；") if c.strip()]
            
            # 技术栈
            tech_match = re.search(r"技术栈[：:]\s*(.+?)(?:\n|$)", knowledge_part)
            if tech_match:
                result["tech_stack"] = [t.strip() for t in re.split(r"[,，、]", tech_match.group(1)) if t.strip()]
            
            # 最佳实践
            bp_match = re.search(r"最佳实践[：:]\s*(.+?)(?:\n|$)", knowledge_part)
            if bp_match:
                result["best_practices"] = [b.strip() for b in bp_match.group(1).split("；") if b.strip()]
        
        # 解析 [MEMORY] 部分
        if "[MEMORY]" in content:
            memory_part = content.split("[MEMORY]")[1]
            
            import re
            # 摘要
            summary_match = re.search(r"摘要[：:]\s*(.+?)(?:\n|$)", memory_part)
            if summary_match:
                result["summary"] = summary_match.group(1).strip()
            
            # 关键洞察
            insight_match = re.search(r"关键洞察[：:]\s*(.+?)(?:\n|$)", memory_part)
            if insight_match:
                result["insight"] = insight_match.group(1).strip()
        
        return result
    
    def _store_to_domain_nexus(self, parsed: Dict[str, Any], source_file: str) -> int:
        """存入 DomainNexus"""
        count = 0
        try:
            from knowledge_cells import get_nexus
            
            nexus = get_nexus()
            
            # 构建知识内容
            points = parsed.get("points", [])
            tags = set(parsed.get("tags", []))
            tags.add("学习计划")
            tags.add(source_file.split(".")[-1])  # 添加文件类型标签
            
            if not points:
                return 0
            
            # 创建或更新格子
            cell_name = f"来自学习_{source_file[:30]}"
            
            # 尝试找到一个合适的格子来丰富
            cells = nexus.list_cells()
            target_cell_id = None
            
            # 找最相关的格子
            for cell in cells:
                cell_tags = set(cell.get("tags", []))
                overlap = tags & cell_tags
                if len(overlap) > 0:
                    target_cell_id = cell["cell_id"]
                    break
            
            enrichment = {
                "new_tags": tags,
                "new_analogies": parsed.get("cases", []),
                "new_metrics": [],
                "new_cases": [f"来源: {source_file}"] + parsed.get("cases", []),
                "new_insights": [parsed.get("insight", "")] if parsed.get("insight") else [],
                "summary": parsed.get("summary", ""),
            }
            
            if target_cell_id:
                nexus.cell_manager.enrich_cell(target_cell_id, enrichment)
                count = 1
            else:
                # 创建新格子
                cell_id = nexus.cell_manager.create_cell(
                    name=cell_name,
                    tags=tags,
                    summary=parsed.get("summary", ""),
                    associations={},
                )
                if cell_id:
                    nexus.cell_manager.enrich_cell(cell_id, enrichment)
                    count = 1
            
        except Exception as e:
            logger.warning(f"[LearningPlanEngine] DomainNexus存储失败: {e}")
        
        return count
    
    def _store_to_neural_memory(self, parsed: Dict[str, Any], source_file: str, file_path: str) -> int:
        """存入 NeuralMemory"""
        count = 0
        try:
            from neural_memory import get_neural_memory
            
            nm = get_neural_memory()
            
            # 摘要记忆
            if parsed.get("summary"):
                rec = nm.store(
                    content=parsed["summary"],
                    title=f"学习记忆: {source_file}",
                    tags=["学习计划", "文件记忆"] + parsed.get("tags", [])[:5],
                    source="LEARNING_PLAN",
                    category="LEARNING_INSIGHT",
                    metadata={
                        "source_file": file_path,
                        "file_type": source_file.split(".")[-1],
                    }
                )
                if rec:
                    count += 1
            
            # 核心要点记忆
            points = parsed.get("points", [])
            for i, point in enumerate(points[:3]):
                rec = nm.store(
                    content=point,
                    title=f"知识要点{i+1}: {source_file}",
                    tags=["学习计划", "知识要点"] + parsed.get("tags", [])[:3],
                    source="LEARNING_PLAN",
                    category="KNOWLEDGE_POINT",
                    metadata={
                        "source_file": file_path,
                        "index": i + 1,
                    }
                )
                if rec:
                    count += 1
            
            # 洞察记忆
            if parsed.get("insight"):
                rec = nm.store(
                    content=parsed["insight"],
                    title=f"学习洞察: {source_file}",
                    tags=["学习计划", "洞察"] + parsed.get("tags", [])[:3],
                    source="LEARNING_PLAN",
                    category="LEARNING_INSIGHT",
                    metadata={
                        "source_file": file_path,
                    }
                )
                if rec:
                    count += 1
            
        except Exception as e:
            logger.warning(f"[LearningPlanEngine] NeuralMemory存储失败: {e}")
        
        return count
    
    # ============================================================
    #  持久化
    # ============================================================
    
    def _get_plan_file(self, plan_id: str) -> Path:
        return self._data_dir / f"{plan_id}.json"
    
    def _save_plan(self, plan: LearningPlan):
        """保存计划到磁盘"""
        try:
            file_path = self._get_plan_file(plan.id)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(plan.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[LearningPlanEngine] 保存计划失败: {e}")
    
    def _load_all_plans(self):
        """加载所有计划"""
        if not self._data_dir.exists():
            return
        
        for fpath in self._data_dir.glob("lp_*.json"):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    plan = LearningPlan(**data)
                    # 忽略运行中的计划状态（重启后恢复为 pending）
                    if plan.status in (PlanStatus.SCANNING.value, PlanStatus.LEARNING.value):
                        plan.status = PlanStatus.PAUSED.value
                    self._plans[plan.id] = plan
            except Exception as e:
                logger.warning(f"[LearningPlanEngine] 加载计划失败: {fpath}, {e}")
    
    def _delete_plan_file(self, plan_id: str):
        """删除计划文件"""
        try:
            fpath = self._get_plan_file(plan_id)
            if fpath.exists():
                fpath.unlink()
        except Exception as e:
            logger.error(f"[LearningPlanEngine] 删除计划文件失败: {e}")
    
    # ============================================================
    #  统计
    # ============================================================
    
    def get_stats(self) -> Dict[str, Any]:
        """获取全局统计"""
        plans = list(self._plans.values())
        
        return {
            "total_plans": len(plans),
            "by_status": {
                "pending": sum(1 for p in plans if p.status == PlanStatus.PENDING.value),
                "scanning": sum(1 for p in plans if p.status == PlanStatus.SCANNING.value),
                "learning": sum(1 for p in plans if p.status == PlanStatus.LEARNING.value),
                "completed": sum(1 for p in plans if p.status == PlanStatus.COMPLETED.value),
                "paused": sum(1 for p in plans if p.status == PlanStatus.PAUSED.value),
                "cancelled": sum(1 for p in plans if p.status == PlanStatus.CANCELLED.value),
                "error": sum(1 for p in plans if p.status == PlanStatus.ERROR.value),
            },
            "total_files_processed": sum(p.processed_files for p in plans),
            "total_knowledge_stored": sum(p.total_knowledge for p in plans),
            "total_memory_stored": sum(p.total_memory for p in plans),
        }


# ============================================================
#  全局单例
# ============================================================

def get_learning_plan_engine() -> LearningPlanEngine:
    """获取学习计划引擎单例"""
    return LearningPlanEngine()


# ============================================================
#  CLI 入口
# ============================================================

if __name__ == "__main__":
    engine = get_learning_plan_engine()
    
    import argparse
    parser = argparse.ArgumentParser(description="学习计划引擎")
    sub = parser.add_subparsers(dest="cmd")
    
    # 创建计划
    create_p = sub.add_parser("create", help="创建学习计划")
    create_p.add_argument("--name", required=True, help="计划名称")
    create_p.add_argument("--path", required=True, help="文件夹路径")
    
    # 列表
    list_p = sub.add_parser("list", help="列出计划")
    list_p.add_argument("--status", help="状态过滤")
    
    # 启动
    start_p = sub.add_parser("start", help="启动计划")
    start_p.add_argument("plan_id", help="计划ID")
    
    args = parser.parse_args()
    
    if args.cmd == "create":
        plan = engine.create_plan(args.name, args.path)
        print(f"创建计划成功: {plan.id}")
        print(f"名称: {plan.name}")
        print(f"路径: {plan.folder_path}")
    
    elif args.cmd == "list":
        plans = engine.list_plans(status_filter=args.status)
        for p in plans:
            print(f"[{p.id}] {p.name} | {p.status} | 进度: {p.progress_percent} | 知识: {p.total_knowledge} | 记忆: {p.total_memory}")
    
    elif args.cmd == "start":
        ok = engine.start_plan(args.plan_id)
        print(f"启动{'成功' if ok else '失败'}")
    
    else:
        parser.print_help()
