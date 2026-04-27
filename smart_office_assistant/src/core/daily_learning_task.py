"""
__all__ = [
    'add_source_directory',
    'create_daily_learning_task',
    'get_learning_summary',
    'learn_file',
    'run_daily_learning',
    'scan_source_directories',
    'select_files_to_learn',
]

每日学习任务
实现自动化的每日学习流程
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass

from loguru import logger

from .learning_system import LearningSystem, LearningEntry

@dataclass
class LearningFile:
    """待学习文件"""
    path: str
    name: str
    file_type: str
    size: int
    status: str = "pending"  # pending, learned, skipped, error

class DailyLearningTask:
    """
    每日学习任务
    
    功能:
    - 扫描学习目录
    - 选择待学习文件
    - 执行学习(调用AI解析)
    - 记录学习结果
    """
    
    def __init__(self, learning_system: LearningSystem, 
                 source_dirs: List[str] = None,
                 ai_callback: Callable = None):
        self.learning_system = learning_system
        self.source_dirs = source_dirs or []
        self.ai_callback = ai_callback
        
        # 待学习文件队列
        self.pending_files: List[LearningFile] = []
        self.today_learned: List[LearningFile] = []
        self.today_skipped: List[LearningFile] = []
        
        logger.info("每日学习任务init完成")
    
    def scan_source_directories(self) -> List[LearningFile]:
        """扫描源目录,发现待学习文件"""
        files = []
        config = self.learning_system.config
        allowed_types = config['daily_learning']['file_types']
        
        for source_dir in self.source_dirs:
            source_path = Path(source_dir)
            if not source_path.exists():
                logger.warning(f"源目录不存在: {source_dir}")
                continue
            
            for file_path in source_path.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in allowed_types:
                    # 检查是否已学习过(通过文件名哈希)
                    file_hash = self._get_file_hash(file_path)
                    if not self._is_already_learned(file_hash):
                        files.append(LearningFile(
                            path=str(file_path),
                            name=file_path.name,
                            file_type=file_path.suffix.lower(),
                            size=file_path.stat().st_size
                        ))
        
        # 按文件大小排序(先学小的)
        files.sort(key=lambda x: x.size)
        
        self.pending_files = files
        logger.info(f"扫描完成,发现 {len(files)} 个待学习文件")
        return files
    
    def _get_file_hash(self, file_path: Path) -> str:
        """get文件哈希(用于去重)"""
        stat = file_path.stat()
        content = f"{file_path.name}_{stat.st_size}_{stat.st_mtime}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _is_already_learned(self, file_hash: str) -> bool:
        """检查文件是否已学习过"""
        # 检查历史日志
        for log in self.learning_system.daily_logs:
            for file_info in log.files:
                if file_info.get('hash') == file_hash:
                    return True
        return False
    
    def select_files_to_learn(self, max_count: int = None) -> List[LearningFile]:
        """选择今日要学习的文件"""
        if max_count is None:
            max_count = self.learning_system.config['daily_learning']['max_files_per_day']
        
        # 优先选择小文件(< 10MB)
        small_files = [f for f in self.pending_files if f.size < 10 * 1024 * 1024]
        
        selected = small_files[:max_count]
        logger.info(f"选择 {len(selected)} 个文件今日学习")
        return selected
    
    def learn_file(self, file: LearningFile) -> Dict[str, Any]:
        """学习单个文件"""
        logger.info(f"开始学习: {file.name}")
        
        try:
            # 读取文件内容
            content = self._read_file_content(file.path)
            if not content:
                file.status = "error"
                return {'success': False, 'error': '无法读取文件内容'}
            
            # 调用AI解析(如果有回调)
            if self.ai_callback:
                learning_result = self.ai_callback(content, file.name)
            else:
                # 模拟学习结果
                learning_result = self._mock_learning(file.name)
            
            # 保存学习条目
            entry = self.learning_system.add_learning_entry(
                topic_id=learning_result.get('topic_id', 'general'),
                title=learning_result.get('title', file.name),
                discipline=learning_result.get('discipline', '通用'),
                summary=learning_result.get('summary', ''),
                key_sentences=learning_result.get('key_sentences', []),
                insights=learning_result.get('insights', []),
                sources=learning_result.get('sources', [{'title': file.name, 'url': ''}]),
                tags=learning_result.get('tags', [])
            )
            
            file.status = "learned"
            self.today_learned.append(file)
            
            logger.info(f"学习完成: {file.name} -> {entry.id}")
            return {
                'success': True,
                'entry_id': entry.id,
                'title': entry.title
            }
            
        except Exception as e:
            file.status = "error"
            logger.error(f"学习失败 {file.name}: {e}")
            return {'success': False, 'error': '学习失败'}
    
    def _read_file_content(self, file_path: str) -> str:
        """读取文件内容"""
        path = Path(file_path)
        
        try:
            if path.suffix.lower() == '.txt':
                return path.read_text(encoding='utf-8')
            elif path.suffix.lower() == '.md':
                return path.read_text(encoding='utf-8')
            elif path.suffix.lower() == '.json':
                data = json.loads(path.read_text(encoding='utf-8'))
                return json.dumps(data, ensure_ascii=False, indent=2)
            else:
                # 其他格式返回文件名作为标识
                return f"[File: {path.name}]"
        except Exception as e:
            logger.warning(f"读取文件失败 {file_path}: {e}")
            return ""
    
    def _mock_learning(self, file_name: str) -> Dict[str, Any]:
        """模拟学习结果(用于测试)"""
        return {
            'topic_id': f"topic_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'title': f"学习内容: {file_name}",
            'discipline': '通用知识',
            'summary': f'这是从文件 "{file_name}" 学习到的内容摘要.',
            'key_sentences': [
                '关键句子1:这是学习到的第一个要点',
                '关键句子2:这是学习到的第二个要点',
                '关键句子3:这是学习到的第三个要点'
            ],
            'insights': [
                '洞察1:这是对内容的深度理解',
                '洞察2:这是应用到实际场景的思考'
            ],
            'sources': [{'title': file_name, 'url': ''}],
            'tags': ['自动学习', '待分类']
        }
    
    def run_daily_learning(self) -> Dict[str, Any]:
        """执行每日学习任务"""
        logger.info("=" * 50)
        logger.info("开始每日学习任务")
        logger.info("=" * 50)
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 1. 扫描源目录
        self.scan_source_directories()
        
        # 2. 选择文件
        files_to_learn = self.select_files_to_learn()
        
        if not files_to_learn:
            logger.info("没有待学习文件")
            return {
                'date': today,
                'learned_count': 0,
                'skipped_count': 0,
                'message': '没有待学习文件'
            }
        
        # 3. 学习文件
        learned_files = []
        skipped_files = []
        error_files = []
        
        for file in files_to_learn:
            result = self.learn_file(file)
            
            file_info = {
                'file': file.name,
                'path': file.path,
                'hash': self._get_file_hash(Path(file.path)),
                'status': file.status
            }
            
            if result['success']:
                learned_files.append(file_info)
            else:
                error_files.append({**file_info, 'error': result.get('error', '')})
        
        # 4. 记录日志
        all_files = learned_files + skipped_files + error_files
        self.learning_system.log_daily_learning(
            date=today,
            files=all_files,
            learned_count=len(learned_files),
            skipped_count=len(skipped_files),
            error_count=len(error_files)
        )
        
        result = {
            'date': today,
            'learned_count': len(learned_files),
            'skipped_count': len(skipped_files),
            'error_count': len(error_files),
            'files': all_files
        }
        
        logger.info(f"每日学习完成: 学习 {result['learned_count']}, "
                   f"跳过 {result['skipped_count']}, 错误 {result['error_count']}")
        
        return result
    
    def add_source_directory(self, path: str):
        """添加源目录"""
        if path not in self.source_dirs:
            self.source_dirs.append(path)
            logger.info(f"添加源目录: {path}")
    
    def get_learning_summary(self) -> str:
        """get学习摘要"""
        stats = self.learning_system.get_learning_stats()
        
        lines = [
            "📚 学习系统摘要",
            "=" * 40,
            f"总学习条目: {stats['total_entries']}",
            f"学习主题: {stats['learned_topics']}/{stats['total_topics']}",
            f"今日学习: {stats['today_learned']} 个文件",
            f"累计学习: {stats['total_learned_files']} 个文件",
            "",
            "学科分布:",
        ]
        
        for discipline in stats['disciplines'][:5]:
            entries = self.learning_system.search_entries(discipline=discipline)
            lines.append(f"  - {discipline}: {len(entries)} 条目")
        
        if len(stats['disciplines']) > 5:
            lines.append(f"  ... 还有 {len(stats['disciplines']) - 5} 个学科")
        
        return "\n".join(lines)

# 便捷函数
def create_daily_learning_task(learning_system: LearningSystem,
                               source_dirs: List[str] = None,
                               ai_callback: Callable = None) -> DailyLearningTask:
    """创建每日学习任务"""
    return DailyLearningTask(learning_system, source_dirs, ai_callback)
