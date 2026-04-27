"""
__all__ = [
    'add_learning_entry',
    'add_topic',
    'create_learning_system',
    'daily_task',
    'get_entries_by_discipline',
    'get_learning_stats',
    'get_review_entries',
    'log_daily_learning',
    'review_entry',
    'run_scheduler',
    'search_entries',
    'start_daily_scheduler',
    'stop_scheduler',
    'to_dict',
]

SmartOffice 自主学习系统
基于 Solutions/Supermind 学习逻辑重构
独立于原项目,从零开始积累
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from collections import defaultdict
import threading
import time
import schedule

from loguru import logger

@dataclass
class LearningEntry:
    """学习条目"""
    id: str
    topic_id: str
    title: str
    discipline: str
    summary: str
    key_sentences: List[str]
    insights: List[str]
    sources: List[Dict[str, str]]
    tags: List[str]
    learned_at: datetime
    review_count: int = 0
    last_reviewed: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """将学习条目转换为字典
        
        Returns:
            Dict[str, Any]: 包含所有字段的字典，datetime字段转为ISO格式
        """
        return {
            'id': self.id,
            'topic_id': self.topic_id,
            'title': self.title,
            'discipline': self.discipline,
            'summary': self.summary,
            'key_sentences': self.key_sentences,
            'insights': self.insights,
            'sources': self.sources,
            'tags': self.tags,
            'learned_at': self.learned_at.isoformat(),
            'review_count': self.review_count,
            'last_reviewed': self.last_reviewed.isoformat() if self.last_reviewed else None
        }

@dataclass
class DailyLog:
    """每日学习日志"""
    date: str
    learned_count: int
    skipped_count: int
    error_count: int
    files: List[Dict[str, str]]
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """将每日日志转换为字典
        
        Returns:
            Dict[str, Any]: 包含所有字段的字典
        """
        return {
            'date': self.date,
            'learned_count': self.learned_count,
            'skipped_count': self.skipped_count,
            'error_count': self.error_count,
            'files': self.files,
            'timestamp': self.timestamp.isoformat()
        }

@dataclass
class LearningTopic:
    """学习主题定义"""
    id: str
    name: str
    description: str
    discipline: str
    priority: int = 5  # 1-10, 越高越优先
    status: str = "pending"  # pending, learning, learned
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class LearningSystem:
    """
    SmartOffice 自主学习系统
    
    功能:
    - 管理学习主题和条目
    - 记录每日学习日志
    - 支持定时学习任务
    - 知识检索和复习
    """
    
    def __init__(self, data_path: str = "data/learning"):
        self.data_path = Path(data_path)
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # 子目录
        self.entries_path = self.data_path / "entries"
        self.logs_path = self.data_path / "logs"
        self.topics_path = self.data_path / "topics"
        
        for p in [self.entries_path, self.logs_path, self.topics_path]:
            p.mkdir(exist_ok=True)
        
        # 数据存储
        self.entries: Dict[str, LearningEntry] = {}
        self.topics: Dict[str, LearningTopic] = {}
        self.daily_logs: List[DailyLog] = []
        
        # 学习配置
        self.config = self._load_config()
        
        # 线程锁
        self._lock = threading.RLock()
        
        # [P6] 脏标记延迟写：避免每次add_*都同步落盘
        self._dirty = False
        
        # 调度器
        self.scheduler = None
        self._stop_scheduler = threading.Event()
        
        # 加载已有数据
        self._load_data()
        
        logger.info(f"学习系统init完成,数据路径: {self.data_path}")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载学习配置"""
        config_file = self.data_path / "config.json"
        default_config = {
            "daily_learning": {
                "enabled": True,
                "time": "08:00",
                "max_files_per_day": 5,
                "file_types": [".pdf", ".docx", ".txt", ".md"]
            },
            "review": {
                "enabled": True,
                "interval_days": [1, 3, 7, 14, 30]
            },
            "disciplines": [
                "消费心理学",
                "行为经济学",
                "社会学",
                "文化人类学",
                "传播学",
                "营销学",
                "行为设计"
            ]
        }
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return {**default_config, **json.load(f)}
        
        # 保存默认配置
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        
        return default_config
    
    def _load_data(self):
        """加载学习数据"""
        # 加载学习条目
        for entry_file in self.entries_path.glob("*.json"):
            try:
                with open(entry_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    entry = LearningEntry(
                        id=data['id'],
                        topic_id=data['topic_id'],
                        title=data['title'],
                        discipline=data['discipline'],
                        summary=data['summary'],
                        key_sentences=data['key_sentences'],
                        insights=data['insights'],
                        sources=data['sources'],
                        tags=data['tags'],
                        learned_at=datetime.fromisoformat(data['learned_at']),
                        review_count=data.get('review_count', 0),
                        last_reviewed=datetime.fromisoformat(data['last_reviewed']) if data.get('last_reviewed') else None
                    )
                    self.entries[entry.id] = entry
            except Exception as e:
                logger.warning(f"加载学习条目失败 {entry_file}: {e}")
        
        # 加载主题
        topics_file = self.topics_path / "index.json"
        if topics_file.exists():
            with open(topics_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for t_data in data.get('topics', []):
                    topic = LearningTopic(
                        id=t_data['id'],
                        name=t_data['name'],
                        description=t_data.get('description', ''),
                        discipline=t_data.get('discipline', ''),
                        priority=t_data.get('priority', 5),
                        status=t_data.get('status', 'pending'),
                        created_at=datetime.fromisoformat(t_data['created_at']) if t_data.get('created_at') else datetime.now()
                    )
                    self.topics[topic.id] = topic
        
        # 加载日志
        logs_file = self.logs_path / "daily_logs.json"
        if logs_file.exists():
            with open(logs_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for log_data in data.get('logs', []):
                    log = DailyLog(
                        date=log_data['date'],
                        learned_count=log_data['learned_count'],
                        skipped_count=log_data['skipped_count'],
                        error_count=log_data['error_count'],
                        files=log_data['files'],
                        timestamp=datetime.fromisoformat(log_data['timestamp'])
                    )
                    self.daily_logs.append(log)
        
        logger.info(f"加载完成: {len(self.entries)} 条目, {len(self.topics)} 主题, {len(self.daily_logs)} 日志")
    
    def _save_entry(self, entry: LearningEntry):
        """保存学习条目"""
        entry_file = self.entries_path / f"{entry.id}.json"
        with open(entry_file, 'w', encoding='utf-8') as f:
            json.dump(entry.to_dict(), f, ensure_ascii=False, indent=2)
    
    def _save_topics(self):
        """保存主题索引"""
        topics_file = self.topics_path / "index.json"
        data = {
            'topics': [
                {
                    'id': t.id,
                    'name': t.name,
                    'description': t.description,
                    'discipline': t.discipline,
                    'priority': t.priority,
                    'status': t.status,
                    'created_at': t.created_at.isoformat()
                }
                for t in self.topics.values()
            ],
            'last_updated': datetime.now().isoformat()
        }
        with open(topics_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _save_daily_logs(self):
        """保存每日日志"""
        logs_file = self.logs_path / "daily_logs.json"
        data = {
            'logs': [log.to_dict() for log in self.daily_logs],
            'last_updated': datetime.now().isoformat()
        }
        with open(logs_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_topic(self, topic_id: str, name: str, description: str = "", 
                  discipline: str = "", priority: int = 5) -> LearningTopic:
        """添加学习主题"""
        with self._lock:
            topic = LearningTopic(
                id=topic_id,
                name=name,
                description=description,
                discipline=discipline,
                priority=priority
            )
            self.topics[topic_id] = topic
            self._dirty = True  # [P6] 标记脏
            # 不再立即调用 _save_topics()
            logger.info(f"添加学习主题: {name}")
            return topic
    
    def add_learning_entry(self, topic_id: str, title: str, discipline: str,
                          summary: str, key_sentences: List[str],
                          insights: List[str], sources: List[Dict[str, str]],
                          tags: List[str] = None) -> LearningEntry:
        """添加学习条目"""
        with self._lock:
            entry_id = f"entry_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            
            entry = LearningEntry(
                id=entry_id,
                topic_id=topic_id,
                title=title,
                discipline=discipline,
                summary=summary,
                key_sentences=key_sentences,
                insights=insights,
                sources=sources,
                tags=tags or [],
                learned_at=datetime.now()
            )
            
            self.entries[entry_id] = entry
            self._dirty = True  # [P6] 标记脏，延迟统一刷盘
            
            # 更新主题状态
            if topic_id in self.topics:
                self.topics[topic_id].status = "learned"
                # 不再立即调用 _save_topics()
            
            logger.info(f"添加学习条目: {title}")
            return entry
    
    def log_daily_learning(self, date: str, files: List[Dict[str, str]],
                          learned_count: int, skipped_count: int = 0,
                          error_count: int = 0):
        """记录每日学习日志"""
        with self._lock:
            log = DailyLog(
                date=date,
                learned_count=learned_count,
                skipped_count=skipped_count,
                error_count=error_count,
                files=files,
                timestamp=datetime.now()
            )
            
            # 检查是否已有当天的日志
            existing = next((l for l in self.daily_logs if l.date == date), None)
            if existing:
                existing.learned_count += learned_count
                existing.skipped_count += skipped_count
                existing.error_count += error_count
                existing.files.extend(files)
            else:
                self.daily_logs.append(log)
            
            self._dirty = True  # [P6] 标记脏
            # 不再立即调用 _save_daily_logs()
            logger.info(f"记录学习日志: {date}, 学习 {learned_count} 个文件")
    
    def search_entries(self, query: str = None, discipline: str = None,
                      tags: List[str] = None) -> List[LearningEntry]:
        """搜索学习条目"""
        results = list(self.entries.values())
        
        if query:
            query_lower = query.lower()
            results = [
                e for e in results
                if query_lower in e.title.lower()
                or query_lower in e.summary.lower()
                or any(query_lower in s.lower() for s in e.key_sentences)
            ]
        
        if discipline:
            results = [e for e in results if e.discipline == discipline]
        
        if tags:
            results = [e for e in results if any(t in e.tags for t in tags)]
        
        return sorted(results, key=lambda x: x.learned_at, reverse=True)
    
    def get_entries_by_discipline(self) -> Dict[str, List[LearningEntry]]:
        """按学科分组get学习条目"""
        groups = defaultdict(list)
        for entry in self.entries.values():
            groups[entry.discipline].append(entry)
        return dict(groups)
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """get学习统计"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_log = next((l for l in self.daily_logs if l.date == today), None)
        
        total_learned = sum(log.learned_count for log in self.daily_logs)
        
        return {
            'total_entries': len(self.entries),
            'total_topics': len(self.topics),
            'learned_topics': sum(1 for t in self.topics.values() if t.status == 'learned'),
            'today_learned': today_log.learned_count if today_log else 0,
            'total_learned_files': total_learned,
            'disciplines': list(set(e.discipline for e in self.entries.values())),
            'last_7_days': [
                {
                    'date': log.date,
                    'learned': log.learned_count,
                    'skipped': log.skipped_count
                }
                for log in sorted(self.daily_logs, key=lambda x: x.date, reverse=True)[:7]
            ]
        }
    
    def get_review_entries(self) -> List[LearningEntry]:
        """get需要复习的条目"""
        review_entries = []
        intervals = self.config['review']['interval_days']
        
        for entry in self.entries.values():
            if entry.review_count < len(intervals):
                next_review = entry.learned_at + timedelta(days=intervals[entry.review_count])
                if datetime.now() >= next_review:
                    review_entries.append(entry)
        
        return sorted(review_entries, key=lambda x: x.review_count)
    
    def review_entry(self, entry_id: str):
        """复习条目"""
        with self._lock:
            if entry_id in self.entries:
                entry = self.entries[entry_id]
                entry.review_count += 1
                entry.last_reviewed = datetime.now()
                self._dirty = True  # [P6] 标记脏
                # 不再立即调用 _save_entry(entry)
                logger.info(f"复习条目: {entry.title}, 第 {entry.review_count} 次")
    
    def start_daily_scheduler(self, learning_callback: Callable = None):
        """启动每日学习调度器"""
        if not self.config['daily_learning']['enabled']:
            logger.info("每日学习已禁用")
            return
        
        learning_time = self.config['daily_learning']['time']
        
        def daily_task():
            logger.info("执行每日学习任务...")
            if learning_callback:
                try:
                    learning_callback()
                except Exception as e:
                    logger.error(f"每日学习任务失败: {e}")
        
        schedule.every().day.at(learning_time).do(daily_task)
        
        def run_scheduler():
            while not self._stop_scheduler.is_set():
                schedule.run_pending()
                time.sleep(60)
        
        self.scheduler = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler.start()
        
        logger.info(f"每日学习调度器已启动,学习时间: {learning_time}")
    
    def stop_scheduler(self):
        """停止调度器"""
        if self.scheduler:
            self._stop_scheduler.set()
            self.scheduler.join(timeout=5)
            logger.info("学习调度器已停止")
    
    # ══════════════════════════════════════════════════════
    # [P6] 脏标记延迟写机制
    # ══════════════════════════════════════════════════════
    
    def flush(self) -> None:
        """将内存中所有脏数据同步落盘（P6脏标记机制）。
        
        可在以下场景手动调用：
        1. 程序退出前确保数据持久化
        2. 需要立即读取最新数据的场景
        3. 定时任务周期性刷盘
        """
        with self._lock:
            if not self._dirty:
                return
            # 批量保存所有entries
            for entry in self.entries.values():
                self._save_entry(entry)
            self._save_topics()
            self._save_daily_logs()
            self._dirty = False
            logger.debug("学习系统数据已flush到磁盘")
    
    def __enter__(self):
        """上下文管理器支持 — 进入时无操作"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器支持 — 退出时自动flush"""
        self.flush()
        return False

# 便捷函数
def create_learning_system(data_path: str = "data/learning") -> LearningSystem:
    """创建学习system_instance"""
    return LearningSystem(data_path)
