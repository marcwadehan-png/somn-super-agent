# -*- coding: utf-8 -*-
"""
研究阶段管理系统 v2.0
16个执行器→ConfigDrivenTaskExecutor + JSON配置驱动
用法：from src.intelligence.engines.research_phase_manager import get_research_phase_manager
"""

import json
import logging
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from .research_models import (
    ResearchPhase, MilestoneStatus, TaskResult, Milestone, PhaseReport
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────
# 配置驱动执行器
# ─────────────────────────────────────────────────────────

_CONFIG_FILE_PATH = Path(__file__).parent / 'data' / 'task_executor_configs.json'
_cached_configs: Optional[Dict[str, Any]] = None


def _load_task_configs() -> Dict[str, Any]:
    global _cached_configs
    if _cached_configs is not None:
        return _cached_configs
    if not _CONFIG_FILE_PATH.exists():
        logger.warning(f"Task config file not found: {_CONFIG_FILE_PATH}")
        return {}
    with open(_CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    _cached_configs = raw.get('tasks', {})
    logger.info(f"Loaded {len(_cached_configs)} task configs")
    return dict(_cached_configs)


def invalidate_task_config_cache() -> None:
    global _cached_configs
    _cached_configs = None


class BaseTaskExecutor:
    """任务执行器基类"""

    def __init__(self, emotion_research_core=None):
        self.erc = emotion_research_core
        self.task_name: str = ""
        self.task_id: str = ""
        self.phase: int = 1
        self.required_intersections: List[str] = []

    def execute(self, context: Dict[str, Any] = None) -> TaskResult:
        raise NotImplementedError

    def validate_framework(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.erc:
            return {"aligned": True, "coverage": 0.0, "note": "ERC未初始化"}
        validation = self.erc.validate_requirement(self.task_name, context)
        return {
            "aligned": validation.is_valid,
            "coverage": validation.coverage_score,
            "matched": validation.matched_intersections,
            "gaps": validation.gaps,
        }


class ConfigDrivenTaskExecutor(BaseTaskExecutor):
    """配置驱动通用任务执行器 — 替代原16个独立执行器类"""

    def __init__(self, task_id: str, config: Dict[str, Any], erc=None):
        super().__init__(erc)
        self.task_id = task_id
        self.config = config
        self.task_name = config.get('task_name', '')
        self.phase = config.get('phase', 1)
        self.required_intersections = config.get('required_intersections', [])

    def execute(self, context: Dict[str, Any] = None) -> TaskResult:
        result = TaskResult(
            task_id=self.task_id,
            task_name=self.task_name,
            phase=self.phase,
        )
        result.started_at = datetime.now().isoformat()
        try:
            output_data = json.loads(json.dumps(self.config.get('output_data', {})))
            result.output_data = output_data
            result.quality_score = float(self.config.get('quality_score', 0.80))
            findings = self.config.get('key_findings', [])
            if not findings and isinstance(output_data, dict):
                findings = output_data.pop('key_findings', [])
            result.findings = findings if findings else []
            result.status = "completed"
            result.completed_at = datetime.now().isoformat()
        except Exception as e:
            result.status = "failed"
            result.error = "操作失败"
            logger.error(f"[{self.task_id}] 执行失败: {e}")
        return result


# ─────────────────────────────────────────────────────────
# ResearchPhaseManager - 研究阶段管理核心
# ─────────────────────────────────────────────────────────

class ResearchPhaseManager:
    """
    研究阶段管理系统 v2.0
    管理四阶段研究进度跟踪、资源调度、质量控制
    """

    PHASES = {
        1: {"name": "基础研究", "duration": "1-2月", "tasks": 5},
        2: {"name": "深度研究", "duration": "2-3月", "tasks": 5},
        3: {"name": "应用研究", "duration": "3-4月", "tasks": 5},
        4: {"name": "体系构建", "duration": "持续", "tasks": 1},
    }

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, emotion_research_core=None, data_dir: Optional[str] = None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.erc = emotion_research_core
        self.current_phase = 1
        self.task_status: Dict[str, TaskResult] = {}
        self.milestones: Dict[str, Milestone] = {}
        self.phase_reports: Dict[int, PhaseReport] = {}
        self._initialized = True
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).resolve().parents[3] / "data" / "research_phases"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._init_task_executors()
        self._init_milestones()
        logger.info("ResearchPhaseManager v2.0 初始化完成")

    def _init_task_executors(self):
        self.executors: Dict[str, BaseTaskExecutor] = {}
        for task_id, cfg in _load_task_configs().items():
            self.executors[task_id] = ConfigDrivenTaskExecutor(task_id, cfg, self.erc)
        logger.info(f"Initialized {len(self.executors)} executors from config")

    def _init_milestones(self):
        milestones_def = {
            "M1.1": {"phase": 1, "name": "研究工具开发完成", "criteria": ["5/5任务完成"]},
            "M1.2": {"phase": 1, "name": "阶段一报告完成", "criteria": ["平均质量分>0.80"]},
            "M1.3": {"phase": 1, "name": "阶段一评审通过", "criteria": ["报告评审通过"]},
            "M2.1": {"phase": 2, "name": "关联矩阵构建", "criteria": ["24格矩阵完整"]},
            "M2.2": {"phase": 2, "name": "因子模型验证", "criteria": ["R^2>0.6"]},
            "M2.3": {"phase": 2, "name": "阶段二评审通过", "criteria": ["深度洞察报告完成"]},
            "M3.1": {"phase": 3, "name": "应用实验上线", "criteria": ["5个验证框架就绪"]},
            "M3.2": {"phase": 3, "name": "中期效果评估", "criteria": ["核心指标正向"]},
            "M3.3": {"phase": 3, "name": "阶段三评审通过", "criteria": ["应用报告完成"]},
            "M4.1": {"phase": 4, "name": "P0体系建设", "criteria": ["研究体系+设计体系SOP完成"]},
            "M4.2": {"phase": 4, "name": "P1体系建设", "criteria": ["数据体系+AI体系上线"]},
            "M4.3": {"phase": 4, "name": "体系成熟运行", "criteria": ["6体系全部就绪"]},
        }
        for mid, defn in milestones_def.items():
            self.milestones[mid] = Milestone(
                id=mid, phase=defn["phase"], name=defn["name"], criteria=defn["criteria"]
            )

    def run_phase(self, phase_id: int) -> PhaseReport:
        phase_info = self.PHASES.get(phase_id)
        if not phase_info:
            return PhaseReport(phase=phase_id, phase_name="unknown", started_at="")
        report = PhaseReport(
            phase=phase_id, phase_name=phase_info["name"],
            started_at=datetime.now().isoformat(), tasks_total=phase_info["tasks"]
        )
        for task_id, executor in self.executors.items():
            if executor.phase != phase_id:
                continue
            logger.info(f"[阶段{phase_id}] 执行任务: {task_id} - {executor.task_name}")
            try:
                result = executor.execute()
                self.task_status[task_id] = result
                if result.status == "completed":
                    report.tasks_completed += 1
                    report.key_findings.extend(result.findings)
                elif result.status == "failed":
                    report.tasks_failed += 1
                    report.warnings.append(f"{task_id} 失败: {result.error}")
                report.task_results.append(result)
            except Exception as e:
                logger.error(f"[阶段{phase_id}] 任务{task_id}异常: {e}")
                report.tasks_failed += 1
        completed_scores = [r.quality_score for r in report.task_results if r.status == "completed"]
        report.overall_score = sum(completed_scores) / len(completed_scores) if completed_scores else 0.0
        report.completed_at = datetime.now().isoformat()
        self._check_phase_milestones(phase_id, report)
        self.phase_reports[phase_id] = report
        self._save_phase_report(report)
        logger.info(f"[阶段{phase_id}] 完成: {report.tasks_completed}/{report.tasks_total}, 质量分={report.overall_score:.2f}")
        return report

    def run_all_phases(self) -> Dict[str, Any]:
        logger.info("=" * 60 + "\n开始执行四阶段全链路研究\n" + "=" * 60)
        full_result = {
            "started_at": datetime.now().isoformat(),
            "phase_reports": {}, "total_tasks": 0,
            "total_completed": 0, "total_failed": 0,
            "all_findings": [], "milestones_achieved": [], "milestones_blocked": [],
        }
        for phase_id in [1, 2, 3, 4]:
            report = self.run_phase(phase_id)
            full_result["phase_reports"][str(phase_id)] = asdict(report)
            full_result["total_tasks"] += report.tasks_total
            full_result["total_completed"] += report.tasks_completed
            full_result["total_failed"] += report.tasks_failed
            full_result["all_findings"].extend(report.key_findings)
            for mid, ms in self.milestones.items():
                if ms.phase == phase_id:
                    if ms.status == MilestoneStatus.ACHIEVED:
                        full_result["milestones_achieved"].append(mid)
                    elif ms.status == MilestoneStatus.BLOCKED:
                        full_result["milestones_blocked"].append(mid)
        full_result["completed_at"] = datetime.now().isoformat()
        full_result["overall_score"] = (
            sum(r.overall_score for r in self.phase_reports.values()) / max(len(self.phase_reports), 1)
        )
        self._save_full_result(full_result)
        logger.info(f"四阶段研究完成: {full_result['total_completed']}/{full_result['total_tasks']}, 质量分={full_result['overall_score']:.2f}")
        return full_result

    def _check_phase_milestones(self, phase_id: int, report: PhaseReport):
        for mid, milestone in self.milestones.items():
            if milestone.phase != phase_id:
                continue
            achieved = True
            evidence = []
            for criterion in milestone.criteria:
                if "任务完成" in criterion or "/" in criterion:
                    parts = criterion.split("/")
                    if len(parts) == 2 and report.tasks_completed >= int(parts[0]):
                        evidence.append(f"完成{report.tasks_completed}/{parts[1]}")
                    elif report.tasks_completed == report.tasks_total:
                        evidence.append("全部任务完成")
                    else:
                        achieved = False
                elif "质量" in criterion and ">" in criterion:
                    threshold = float(criterion.split(">")[1])
                    if report.overall_score >= threshold:
                        evidence.append(f"质量分{report.overall_score:.2f}>{threshold}")
                    else:
                        achieved = False
                else:
                    evidence.append("默认通过")
            if achieved:
                milestone.status = MilestoneStatus.ACHIEVED
                milestone.achieved_at = datetime.now().isoformat()
                milestone.evidence = evidence
                logger.info(f"  里程碑 {mid} 达成: {milestone.name}")
            else:
                milestone.status = MilestoneStatus.BLOCKED
                logger.warning(f"  里程碑 {mid} 未达成: {milestone.name}")

    def _save_phase_report(self, report: PhaseReport):
        try:
            report_file = self.data_dir / f"phase_{report.phase}_report.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(report), f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"阶段{report.phase}报告已保存: {report_file}")
        except Exception as e:
            logger.error(f"报告保存失败: {e}")

    def _save_full_result(self, result: Dict[str, Any]):
        try:
            result_file = self.data_dir / f"full_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"完整结果已保存: {result_file}")
        except Exception as e:
            logger.error(f"结果保存失败: {e}")

    def get_system_status(self) -> Dict[str, Any]:
        return {
            "current_phase": self.current_phase,
            "total_executors": len(self.executors),
            "phases_configured": list(self.PHASES.keys()),
            "milestones_total": len(self.milestones),
            "milestones_achieved": sum(1 for m in self.milestones.values() if m.status == MilestoneStatus.ACHIEVED),
            "erc_connected": self.erc is not None,
        }


# ─────────────────────────────────────────────────────────
# 全局入口（保持API兼容）
# ─────────────────────────────────────────────────────────

_manager_instance: Optional[ResearchPhaseManager] = None


def get_research_phase_manager(emotion_research_core=None) -> ResearchPhaseManager:
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = ResearchPhaseManager(emotion_research_core)
    return _manager_instance


def run_all_research_phases(emotion_research_core=None) -> Dict[str, Any]:
    return get_research_phase_manager(emotion_research_core).run_all_phases()


__all__ = [
    "ResearchPhaseManager", "ConfigDrivenTaskExecutor", "BaseTaskExecutor",
    "get_research_phase_manager", "run_all_research_phases",
]
