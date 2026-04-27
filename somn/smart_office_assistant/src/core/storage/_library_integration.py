"""
藏书阁集成模块 v1.1
===================================
功能：
1. SomnStorageManager 与 Imperial Library 的桥接
2. 自动将高价值数据备份到藏书阁
3. 数据恢复与同步
4. 智能数据分类与自动备份策略
"""

import json
import threading
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from functools import wraps

# 路径配置
def _get_project_root() -> Path:
    """动态获取项目根目录"""
    try:
        from src.core.paths import PROJECT_ROOT
        return Path(PROJECT_ROOT)
    except ImportError:
        return Path(__file__).parent.parent.parent.parent.parent

PROJECT_ROOT = _get_project_root()
LIBRARY_DIR = PROJECT_ROOT / "data" / "imperial_library"


class DataPriority(Enum):
    """数据优先级"""
    CRITICAL = "critical"
    IMPORTANT = "important"
    NORMAL = "normal"
    TEMPORARY = "temp"


@dataclass
class AutoBackupRule:
    """自动备份规则"""
    data_type: str
    priority: DataPriority
    category: str
    enabled: bool = True
    max_age_hours: Optional[int] = None


@dataclass
class SyncStatus:
    """同步状态"""
    total_queued: int = 0
    total_synced: int = 0
    total_failed: int = 0
    last_sync: Optional[str] = None
    is_running: bool = False


def _get_manager_and_tier():
    """安全获取存储管理器和备份级别枚举"""
    # 首先尝试直接导入（作为包成员）
    try:
        from ._somn_storage_manager import get_storage_manager, BackupTier
        return get_storage_manager, BackupTier
    except ImportError:
        pass

    # 作为独立脚本运行时，设置路径后导入
    import sys
    from pathlib import Path

    # 获取正确的路径
    current_file = Path(__file__).resolve()
    if current_file.parent.name == "storage":
        # 作为包内模块运行
        project_root = current_file.parent.parent.parent.parent
    else:
        project_root = current_file.parent

    # 添加到路径
    src_path = project_root / "smart_office_assistant" / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    try:
        from _somn_storage_manager import get_storage_manager, BackupTier
        return get_storage_manager, BackupTier
    except ImportError:
        from smart_office_assistant.src.core.storage._somn_storage_manager import get_storage_manager, BackupTier
        return get_storage_manager, BackupTier


class LibraryIntegration:
    """藏书阁集成器 v1.1"""

    _instance: Optional["LibraryIntegration"] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, storage_manager=None):
        if getattr(self, '_initialized', False):
            return

        self.storage_manager = storage_manager
        self._sync_thread: Optional[threading.Thread] = None
        self._running = False
        self._sync_lock = threading.Lock()
        self._logger = logging.getLogger("LibraryIntegration")

        self._sync_queue: List[Dict[str, Any]] = []
        self._sync_status = SyncStatus()
        self.config = self._load_config()
        self._backup_rules = self._init_backup_rules()
        self._auto_sync_enabled = False

        self._initialized = True

    def _load_config(self) -> Dict[str, Any]:
        """加载集成配置"""
        config_file = PROJECT_ROOT / "config" / "storage_config.yaml"

        if config_file.exists():
            try:
                import yaml
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if config:
                        return config
            except Exception as e:
                self._logger.warning(f"加载存储配置失败: {e}")
                pass

        return {
            "imperial_library_backup": {"enabled": True, "auto_backup": {"enabled": True, "interval_minutes": 60}},
            "backup_tiers": {
                "JIA": {"priority": 1, "retention": None, "categories": ["system_config", "wisdom_encodings"]},
                "YI": {"priority": 2, "retention_days": 365, "categories": ["session_summaries"]},
                "BING": {"priority": 3, "retention_days": 30, "categories": ["operation_logs"]},
                "DING": {"priority": 4, "retention_days": 7, "categories": ["raw_logs"]}
            }
        }

    def _init_backup_rules(self) -> List[AutoBackupRule]:
        """初始化自动备份规则"""
        return [
            AutoBackupRule("system_config", DataPriority.CRITICAL, "system_config"),
            AutoBackupRule("wisdom_encoding", DataPriority.CRITICAL, "wisdom_encodings"),
            AutoBackupRule("learned_pattern", DataPriority.CRITICAL, "learned_patterns"),
            AutoBackupRule("critical_state", DataPriority.CRITICAL, "critical_states"),
            AutoBackupRule("roi_report", DataPriority.CRITICAL, "roi_reports"),
            AutoBackupRule("session_summary", DataPriority.IMPORTANT, "session_summaries"),
            AutoBackupRule("task_history", DataPriority.IMPORTANT, "task_histories"),
            AutoBackupRule("learning_result", DataPriority.IMPORTANT, "learning_results"),
            AutoBackupRule("research_output", DataPriority.IMPORTANT, "research_outputs"),
            AutoBackupRule("wisdom_document", DataPriority.IMPORTANT, "wisdom_documents"),
            AutoBackupRule("operation_log", DataPriority.NORMAL, "operation_logs"),
            AutoBackupRule("performance_summary", DataPriority.NORMAL, "performance_summaries"),
            AutoBackupRule("error_report", DataPriority.NORMAL, "error_reports"),
            AutoBackupRule("execution_record", DataPriority.NORMAL, "execution_records"),
            AutoBackupRule("raw_log", DataPriority.TEMPORARY, "raw_logs"),
            AutoBackupRule("temp_data", DataPriority.TEMPORARY, "temp_data"),
            AutoBackupRule("cache", DataPriority.TEMPORARY, "cache"),
            AutoBackupRule("intermediate", DataPriority.TEMPORARY, "intermediate_data"),
        ]

    def classify_for_backup(self, data: Any, source: str, metadata: Optional[Dict[str, Any]] = None) -> tuple:
        """分类数据确定备份级别"""
        data_type = metadata.get("type", source) if metadata else source

        for rule in self._backup_rules:
            if rule.data_type == data_type and rule.enabled:
                return self._priority_to_tier(rule.priority), rule.category

        return self._classify_by_name(data_type)

    def _priority_to_tier(self, priority: DataPriority) -> str:
        mapping = {DataPriority.CRITICAL: "甲", DataPriority.IMPORTANT: "乙", DataPriority.NORMAL: "丙", DataPriority.TEMPORARY: "丁"}
        return mapping.get(priority, "乙")

    def _classify_by_name(self, name: str) -> tuple:
        name_lower = name.lower()
        critical_keywords = ["config", "wisdom", "encoding", "pattern", "critical", "roi", "strategy"]
        if any(kw in name_lower for kw in critical_keywords):
            return "甲", name
        important_keywords = ["session", "task", "learn", "research", "output", "document", "result"]
        if any(kw in name_lower for kw in important_keywords):
            return "乙", name
        normal_keywords = ["log", "performance", "error", "execution", "record"]
        if any(kw in name_lower for kw in normal_keywords):
            return "丙", name
        return "乙", name

    def auto_backup_session(self, session_id: str, context_summary: str, session_data: Dict[str, Any]) -> Optional[str]:
        """自动备份会话数据到藏书阁"""
        if not self._is_backup_enabled():
            return None

        try:
            get_storage_manager, BackupTier = _get_manager_and_tier()
            manager = get_storage_manager()

            backup_data = {
                "session_id": session_id,
                "context_summary": context_summary,
                "session_data": session_data,
                "backed_up_at": datetime.now().isoformat()
            }

            tier, category = self.classify_for_backup(session_data, "session", {"type": "session_summary"})

            return manager.backup_to_library(
                data=backup_data,
                category=category,
                tier=BackupTier.from_string(tier),
                title=f"Session {session_id}",
                metadata={"source": "auto_backup", "session_id": session_id}
            )
        except Exception as e:
            self._logger.error(f"Failed to auto backup session: {e}")
            return None

    def auto_backup_task(self, task_id: str, task_result: Any, metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """自动备份任务结果到藏书阁"""
        if not self._is_backup_enabled():
            return None

        try:
            get_storage_manager, BackupTier = _get_manager_and_tier()
            manager = get_storage_manager()

            task_type = metadata.get("task_type", "general") if metadata else "general"
            tier, category = self.classify_for_backup(task_result, "task", {"type": "task_history", "task_type": task_type})

            backup_data = {
                "task_id": task_id,
                "task_type": task_type,
                "result": task_result,
                "metadata": metadata or {},
                "backed_up_at": datetime.now().isoformat()
            }

            return manager.backup_to_library(
                data=backup_data,
                category=category,
                tier=BackupTier.from_string(tier),
                title=f"Task {task_id} Result",
                metadata={"source": "auto_backup", "task_id": task_id}
            )
        except Exception as e:
            self._logger.error(f"Failed to auto backup task: {e}")
            return None

    def auto_backup_wisdom(self, wisdom_data: Dict[str, Any], wisdom_type: str) -> Optional[str]:
        """自动备份智慧数据到藏书阁"""
        if not self._is_backup_enabled():
            return None

        try:
            get_storage_manager, BackupTier = _get_manager_and_tier()
            manager = get_storage_manager()

            backup_data = {
                "wisdom_type": wisdom_type,
                "wisdom_data": wisdom_data,
                "backed_up_at": datetime.now().isoformat()
            }

            return manager.backup_to_library(
                data=backup_data,
                category="wisdom_encodings",
                tier=BackupTier.JIA,
                title=f"Wisdom {wisdom_type}",
                metadata={"source": "auto_backup", "wisdom_type": wisdom_type}
            )
        except Exception as e:
            self._logger.error(f"Failed to auto backup wisdom: {e}")
            return None

    def auto_backup_roi(self, roi_report: Dict[str, Any]) -> Optional[str]:
        """自动备份 ROI 报告到藏书阁"""
        if not self._is_backup_enabled():
            return None

        try:
            get_storage_manager, BackupTier = _get_manager_and_tier()
            manager = get_storage_manager()

            backup_data = {"roi_report": roi_report, "backed_up_at": datetime.now().isoformat()}

            return manager.backup_to_library(
                data=backup_data,
                category="roi_reports",
                tier=BackupTier.JIA,
                title=f"ROI Report {datetime.now().strftime('%Y%m%d')}",
                metadata={"source": "auto_backup", "type": "roi_report"}
            )
        except Exception as e:
            self._logger.error(f"Failed to auto backup ROI: {e}")
            return None

    def auto_backup_config(self, config_data: Dict[str, Any], config_name: str) -> Optional[str]:
        """自动备份配置到藏书阁"""
        if not self._is_backup_enabled():
            return None

        try:
            get_storage_manager, BackupTier = _get_manager_and_tier()
            manager = get_storage_manager()

            backup_data = {"config_name": config_name, "config_data": config_data, "backed_up_at": datetime.now().isoformat()}

            return manager.backup_to_library(
                data=backup_data,
                category="system_config",
                tier=BackupTier.JIA,
                title=f"Config {config_name}",
                metadata={"source": "auto_backup", "config_name": config_name}
            )
        except Exception as e:
            self._logger.error(f"Failed to auto backup config: {e}")
            return None

    def _is_backup_enabled(self) -> bool:
        """检查备份是否启用"""
        return self.config.get("imperial_library_backup", {}).get("enabled", True)

    def queue_for_sync(self, data: Any, source: str, priority: str = "normal", metadata: Optional[Dict[str, Any]] = None) -> None:
        """将数据加入同步队列"""
        tier, category = self.classify_for_backup(data, source, metadata)

        with self._sync_lock:
            self._sync_queue.append({
                "data": data,
                "source": source,
                "tier": tier,
                "category": category,
                "priority": priority,
                "queued_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            })
            self._sync_status.total_queued += 1

    def process_sync_queue(self, batch_size: int = 10, max_retries: int = 3) -> int:
        """处理同步队列"""
        get_storage_manager, BackupTier = _get_manager_and_tier()
        manager = get_storage_manager()
        processed = 0

        while self._sync_queue and processed < batch_size:
            item = self._sync_queue.pop(0)

            for attempt in range(max_retries):
                try:
                    tier_enum = BackupTier.from_string(item["tier"])
                    backup_id = manager.backup_to_library(
                        data=item["data"],
                        category=item["category"],
                        tier=tier_enum,
                        title=f"Synced {item['source']}",
                        metadata={"source": "sync_queue", "priority": item["priority"], "original_source": item["source"]}
                    )

                    if backup_id:
                        processed += 1
                        self._sync_status.total_synced += 1
                        self._sync_status.last_sync = datetime.now().isoformat()
                        break
                except Exception as e:
                    if attempt == max_retries - 1:
                        self._sync_status.total_failed += 1
                        self._logger.debug(f"同步队列处理失败（已重试{max_retries}次）: {e}")

        return processed

    def start_auto_sync(self, interval_seconds: int = 300, batch_size: int = 20) -> None:
        """启动自动同步线程"""
        if self._running:
            return

        self._running = True
        self._auto_sync_enabled = True
        self._sync_status.is_running = True

        def sync_worker():
            while self._running:
                try:
                    with self._sync_lock:
                        self.process_sync_queue(batch_size=batch_size)
                except Exception as e:
                    self._logger.error(f"Auto sync error: {e}")

                time.sleep(interval_seconds)

            self._sync_status.is_running = False

        self._sync_thread = threading.Thread(target=sync_worker, daemon=True)
        self._sync_thread.start()

        self._logger.info(f"Auto sync started (interval: {interval_seconds}s)")

    def stop_auto_sync(self) -> None:
        """停止自动同步"""
        self._running = False
        self._auto_sync_enabled = False

        if self._sync_thread:
            self._sync_thread.join(timeout=5)

        self._logger.info("Auto sync stopped")

    def get_sync_status(self) -> SyncStatus:
        """获取同步状态"""
        with self._sync_lock:
            self._sync_status.total_queued = len(self._sync_queue)
        return self._sync_status

    def clear_sync_queue(self) -> int:
        """清空同步队列"""
        with self._sync_lock:
            count = len(self._sync_queue)
            self._sync_queue.clear()
            return count

    def get_library_status(self) -> Dict[str, Any]:
        """获取藏书阁状态"""
        get_storage_manager, _ = _get_manager_and_tier()
        manager = get_storage_manager()
        backups = manager.get_library_backups()

        tier_stats = {"甲": 0, "乙": 0, "丙": 0, "丁": 0}
        category_stats: Dict[str, int] = {}
        total_size = 0

        for backup in backups:
            tier = backup.get("tier", "丁")
            tier_stats[tier] = tier_stats.get(tier, 0) + 1
            category = backup.get("category", "unknown")
            category_stats[category] = category_stats.get(category, 0) + 1

        for tier in ["甲", "乙", "丙", "丁"]:
            tier_dir = LIBRARY_DIR / tier
            if tier_dir.exists():
                total_size += sum(f.stat().st_size for f in tier_dir.rglob('*') if f.is_file())

        return {
            "total_backups": len(backups),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "tier_distribution": tier_stats,
            "category_distribution": category_stats,
            "sync_queue_size": len(self._sync_queue),
            "sync_status": {
                "total_synced": self._sync_status.total_synced,
                "total_failed": self._sync_status.total_failed,
                "last_sync": self._sync_status.last_sync,
                "is_running": self._sync_status.is_running
            },
            "auto_sync_enabled": self._auto_sync_enabled
        }

    def get_library_summary(self) -> Dict[str, Any]:
        """获取藏书阁摘要"""
        status = self.get_library_status()
        return {"total": status["total_backups"], "size_mb": status["total_size_mb"], "tiers": status["tier_distribution"], "health": "ok" if status["total_backups"] > 0 else "empty"}

    def restore_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """恢复会话数据"""
        get_storage_manager, _ = _get_manager_and_tier()
        manager = get_storage_manager()
        backups = manager.get_library_backups()

        for backup in backups:
            metadata = backup.get("metadata", {})
            if metadata.get("session_id") == session_id:
                return manager.restore_from_library(backup["backup_id"])
        return None

    def restore_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """恢复任务结果"""
        get_storage_manager, _ = _get_manager_and_tier()
        manager = get_storage_manager()
        backups = manager.get_library_backups()

        for backup in backups:
            metadata = backup.get("metadata", {})
            if metadata.get("task_id") == task_id:
                return manager.restore_from_library(backup["backup_id"])
        return None

    def restore_latest_by_category(self, category: str, tier: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """按类别恢复最新的备份"""
        get_storage_manager, _ = _get_manager_and_tier()
        manager = get_storage_manager()

        filters = {"category": category}
        if tier:
            filters["tier"] = tier

        backups = manager.get_library_backups(**filters)
        backups = sorted(backups, key=lambda x: x.get("created_at", ""), reverse=True)[:limit]

        results = []
        for backup in backups:
            data = manager.restore_from_library(backup["backup_id"])
            if data:
                results.append({"backup_id": backup["backup_id"], "title": backup.get("title"), "created_at": backup.get("created_at"), "data": data})
        return results

    def get_backup_rules(self) -> List[Dict[str, Any]]:
        """获取所有备份规则"""
        return [{"data_type": rule.data_type, "priority": rule.priority.value, "category": rule.category, "enabled": rule.enabled, "max_age_hours": rule.max_age_hours} for rule in self._backup_rules]

    def enable_backup_rule(self, data_type: str, enabled: bool = True) -> bool:
        """启用/禁用备份规则"""
        for rule in self._backup_rules:
            if rule.data_type == data_type:
                rule.enabled = enabled
                return True
        return False

    def add_backup_rule(self, data_type: str, priority: str, category: str, max_age_hours: Optional[int] = None) -> bool:
        """添加备份规则"""
        try:
            priority_enum = DataPriority(priority)
            rule = AutoBackupRule(data_type=data_type, priority=priority_enum, category=category, max_age_hours=max_age_hours)
            self._backup_rules.append(rule)
            return True
        except ValueError:
            return False

    def cleanup_expired_backups(self) -> Dict[str, int]:
        """清理过期备份"""
        get_storage_manager, BackupTier = _get_manager_and_tier()
        manager = get_storage_manager()
        result = {}

        for tier in ["乙", "丙", "丁"]:
            deleted = manager.cleanup_library_by_tier(BackupTier.from_string(tier))
            result[tier] = deleted
        return result

    def validate_library_integrity(self) -> Dict[str, Any]:
        """验证藏书阁完整性"""
        get_storage_manager, _ = _get_manager_and_tier()
        manager = get_storage_manager()
        backups = manager.get_library_backups()

        result = {"total_backups": len(backups), "orphaned_files": [], "missing_from_index": [], "corrupted_backups": []}

        for tier in ["甲", "乙", "丙", "丁"]:
            tier_dir = LIBRARY_DIR / tier
            if tier_dir.exists():
                for file in tier_dir.glob("*.json"):
                    backup_id = file.stem
                    if not any(b["backup_id"] == backup_id for b in backups):
                        result["orphaned_files"].append(str(file))

        for backup in backups:
            backup_id = backup["backup_id"]
            tier = backup.get("tier", "乙")
            file_path = LIBRARY_DIR / tier / f"{backup_id}.json"

            if not file_path.exists():
                result["missing_from_index"].append(backup_id)
            else:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json.load(f)
                except json.JSONDecodeError:
                    result["corrupted_backups"].append(backup_id)

        result["is_valid"] = len(result["orphaned_files"]) == 0 and len(result["missing_from_index"]) == 0 and len(result["corrupted_backups"]) == 0
        return result

    def repair_library_index(self) -> int:
        """修复藏书阁索引"""
        get_storage_manager, _ = _get_manager_and_tier()
        manager = get_storage_manager()
        repaired = 0

        index_file = LIBRARY_DIR / "library_index.json"
        new_index = {"backups": {}}

        for tier in ["甲", "乙", "丙", "丁"]:
            tier_dir = LIBRARY_DIR / tier
            if tier_dir.exists():
                for file in tier_dir.glob("*.json"):
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        metadata = data.get("metadata", {})
                        backup_id = metadata.get("backup_id", file.stem)

                        if backup_id not in new_index["backups"]:
                            new_index["backups"][backup_id] = metadata
                            repaired += 1
                    except Exception as e:
                        self._logger.debug(f"跳过损坏的备份文件 {file_path.name}: {e}")
                        continue

        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(new_index, f, ensure_ascii=False, indent=2)

        self._logger.info(f"Repaired {repaired} entries in library index")
        return repaired


_library_integration: Optional[LibraryIntegration] = None


def get_library_integration(storage_manager=None) -> LibraryIntegration:
    """获取藏书阁集成器单例"""
    global _library_integration
    if _library_integration is None:
        _library_integration = LibraryIntegration(storage_manager)
    return _library_integration


def auto_backup_to_library(category: str, tier: str = "乙"):
    """自动备份装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if result is not None:
                get_storage_manager, BackupTier = _get_manager_and_tier()

                def backup():
                    manager = get_storage_manager()
                    manager.backup_to_library(
                        data={"function": func.__name__, "result": result},
                        category=category,
                        tier=BackupTier.from_string(tier),
                        title=f"Auto backup: {func.__name__}"
                    )

                threading.Thread(target=backup, daemon=True).start()

            return result
        return wrapper
    return decorator


if __name__ == "__main__":
    import sys
    from pathlib import Path
    project_root = Path(__file__).parent.parent.parent.parent  # src/core/storage -> smart_office_assistant
    sys.path.insert(0, str(project_root.parent))
    sys.path.insert(0, str(project_root / "src"))

    print("Testing LibraryIntegration v1.1...")
    print("=" * 50)

    integration = get_library_integration()

    print("\n[1] Data Classification:")
    test_cases = [
        ({"test": "data"}, "test", {"type": "wisdom_encoding"}),
        ({"test": "data"}, "test", {"type": "session_summary"}),
        ({"test": "data"}, "test", {"type": "operation_log"}),
        ({"test": "data"}, "test", {"type": "raw_log"}),
    ]

    for data, source, metadata in test_cases:
        tier, category = integration.classify_for_backup(data, source, metadata)
        print(f"    {metadata.get('type')}: tier={tier}, category={category}")

    print("\n[2] Library Status:")
    status = integration.get_library_status()
    print(f"    Total backups: {status['total_backups']}")
    print(f"    Size: {status['total_size_mb']} MB")
    print(f"    Tiers: {status['tier_distribution']}")
    print(f"    Sync queue: {status['sync_queue_size']}")

    print("\n[3] Auto Backup:")
    backup_id = integration.auto_backup_session("test_session_001", "Test session", {"mode": "test", "data": "test"})
    print(f"    Session backup: {'OK' if backup_id else 'FAIL'}")

    print("\n[4] Library Integrity:")
    integrity = integration.validate_library_integrity()
    print(f"    Is valid: {integrity['is_valid']}")
    print(f"    Total backups: {integrity['total_backups']}")
    if integrity['orphaned_files']:
        print(f"    Orphaned files: {len(integrity['orphaned_files'])}")
    if integrity['corrupted_backups']:
        print(f"    Corrupted: {len(integrity['corrupted_backups'])}")

    print("\n" + "=" * 50)
    print("Library integration tests completed!")
