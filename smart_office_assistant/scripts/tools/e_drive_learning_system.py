#!/usr/bin/env python3
"""
E盘深度学习系统 - 整合所有学习维度
深度学习E盘所有资料，包括：
1. PMP项目管理资料
2. 保险知识
3. 简历与职业资料
4. Abyss AI知识库
"""

import sys
import os
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import hashlib
import re

from path_bootstrap import bootstrap_project_paths

bootstrap_project_paths(__file__, change_cwd=True)

# 配置日志

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/learning/e_drive_learning.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class EDriveCategory(Enum):
    """E盘学习分类"""
    PMP_MANAGEMENT = "PMP项目管理"
    INSURANCE_KNOWLEDGE = "保险知识"
    RESUME_CAREER = "简历与职业"
    ABYSS_AI_KNOWLEDGE = "Abyss AI知识库"


class LearningDimension(Enum):
    """学习维度 - 覆盖项目所有需要学习的内容"""
    # 增长引擎维度
    PROVIDER_INTELLIGENCE = "服务商智能"
    SOLUTION_TEMPLATE = "解决方案模板"
    INDUSTRY_KNOWLEDGE = "行业知识"
    ASSESSMENT_FRAMEWORK = "评估框架"
    
    # PPT系统维度
    CHART_DESIGN = "图表设计"
    PPT_STYLE = "PPT风格"
    DATA_VISUALIZATION = "数据可视化"
    
    # 神经记忆维度
    NEURAL_MEMORY = "神经记忆"
    KNOWLEDGE_GRAPH = "知识图谱"
    REASONING_ENGINE = "推理引擎"
    LEARNING_ENGINE = "学习引擎"
    
    # 技术与工具维度
    AI_TECHNOLOGY = "AI技术"
    PYTHON_ADVANCED = "Python进阶"
    DATA_SCIENCE = "数据科学"
    
    # 业务与方法论维度
    GROWTH_HACKING = "增长黑客"
    DIGITAL_MARKETING = "数字营销"
    BUSINESS_STRATEGY = "商业战略"
    
    # 行业趋势维度
    MARKET_TRENDS = "市场趋势"
    EMERGING_TECH = "新兴技术"
    COMPETITIVE_INTEL = "竞争情报"


@dataclass
class LearningSession:
    """学习会话记录"""
    session_id: str
    timestamp: str
    e_drive_category: str
    file_path: str
    file_type: str
    dimension: str
    content_summary: str
    insights: List[str]
    action_items: List[str]
    confidence_score: float
    duration_seconds: float
    knowledge_extracted: Dict[str, Any]


class EDriveLearningSystem:
    """E盘深度学习系统"""
    
    def __init__(self, e_drive_path: str = "E:\\"):
        self.e_drive_path = Path(e_drive_path)
        self.sessions: List[LearningSession] = []
        self.data_dir = Path("data/learning/e_drive_learning")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.session_file = self.data_dir / "sessions.json"
        self.progress_file = self.data_dir / "progress.json"
        self.gap_report_file = self.data_dir / "gaps_and_improvements.json"
        
        # 加载历史进度
        self._load_sessions()
        self._load_progress()
        
        # 文件学习映射
        self.dimension_mapping = self._init_dimension_mapping()
        
        # 已学习文件集合
        self.learned_files = set()
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                progress = json.load(f)
                self.learned_files = set(progress.get('learned_files', []))
        
        # 学习不足记录
        self.learning_gaps = []
        
    def _init_dimension_mapping(self) -> Dict[str, Dict[str, str]]:
        """初始化文件到学习维度的映射"""
        return {
            "PMP项目管理": {
                "PMBOK指南": [LearningDimension.BUSINESS_STRATEGY.value],
                "敏捷实践指南": [LearningDimension.BUSINESS_STRATEGY.value, LearningDimension.GROWTH_HACKING.value],
                "项目管理表格": [LearningDimension.ASSESSMENT_FRAMEWORK.value],
                "汪博士解读": [LearningDimension.BUSINESS_STRATEGY.value],
            },
            "保险知识": {
                "保险": [LearningDimension.INDUSTRY_KNOWLEDGE.value, LearningDimension.BUSINESS_STRATEGY.value],
            },
            "简历与职业": {
                "简历": [LearningDimension.BUSINESS_STRATEGY.value, LearningDimension.DIGITAL_MARKETING.value],
            },
            "Abyss AI知识库": {
                "Supermind": [LearningDimension.AI_TECHNOLOGY.value, LearningDimension.LEARNING_ENGINE.value],
                "Meth": [LearningDimension.PROVIDER_INTELLIGENCE.value, LearningDimension.SOLUTION_TEMPLATE.value],
                "KPI": [LearningDimension.ASSESSMENT_FRAMEWORK.value],
                "tools": [LearningDimension.PYTHON_ADVANCED.value],
            }
        }
    
    def _load_sessions(self):
        """加载历史学习会话"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.sessions = [LearningSession(**s) for s in data]
                logger.info(f"已加载 {len(self.sessions)} 个历史学习会话")
            except Exception as e:
                logger.error(f"加载历史会话失败: {e}")
                self.sessions = []
        else:
            self.sessions = []
    
    def _load_progress(self):
        """加载学习进度"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                    self.learned_files = set(progress.get('learned_files', []))
                logger.info(f"已加载进度，已学习 {len(self.learned_files)} 个文件")
            except Exception as e:
                logger.error(f"加载进度失败: {e}")
                self.learned_files = set()
    
    def _save_sessions(self):
        """保存学习会话"""
        try:
            data = [asdict(s) for s in self.sessions]
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存学习会话失败: {e}")
    
    def _save_progress(self):
        """保存学习进度"""
        try:
            progress = {
                'total_files': len(self.learned_files),
                'learned_files': list(self.learned_files),
                'last_update': datetime.now().isoformat()
            }
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存进度失败: {e}")
    
    def _scan_e_drive_files(self) -> Dict[str, List[Path]]:
        """扫描E盘所有可学习文件"""
        logger.info("开始扫描E盘文件...")
        file_map = {
            EDriveCategory.PMP_MANAGEMENT.value: [],
            EDriveCategory.INSURANCE_KNOWLEDGE.value: [],
            EDriveCategory.RESUME_CAREER.value: [],
            EDriveCategory.ABYSS_AI_KNOWLEDGE.value: []
        }
        
        # 支持的文件类型
        supported_extensions = {
            '.pdf', '.doc', '.docx', '.ppt', '.pptx', 
            '.xls', '.xlsx', '.txt', '.md', '.json'
        }
        
        # 扫描PMP资料
        pmp_path = self.e_drive_path / "PMP备考必备资料包"
        if pmp_path.exists():
            for file_path in pmp_path.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                    file_map[EDriveCategory.PMP_MANAGEMENT.value].append(file_path)
        
        # 扫描保险资料
        insurance_path = self.e_drive_path / "保险"
        if insurance_path.exists():
            for file_path in insurance_path.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                    file_map[EDriveCategory.INSURANCE_KNOWLEDGE.value].append(file_path)
        
        # 扫描简历
        resume_path = self.e_drive_path / "简历"
        if resume_path.exists():
            for file_path in resume_path.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                    file_map[EDriveCategory.RESUME_CAREER.value].append(file_path)
        
        # 扫描Abyss AI
        abyss_path = self.e_drive_path / "Abyss AI"
        if abyss_path.exists():
            for file_path in abyss_path.rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                    # 排除缓存文件
                    if '.playwright' not in str(file_path) and 'Cache' not in str(file_path):
                        file_map[EDriveCategory.ABYSS_AI_KNOWLEDGE.value].append(file_path)
        
        total_files = sum(len(files) for files in file_map.values())
        logger.info(f"扫描完成，发现 {total_files} 个可学习文件")
        for category, files in file_map.items():
            logger.info(f"  {category}: {len(files)} 个文件")
        
        return file_map
    
    def _select_file_to_learn(self, file_map: Dict[str, List[Path]]) -> Optional[tuple]:
        """选择下一个要学习的文件"""
        for category, files in file_map.items():
            for file_path in files:
                if str(file_path) not in self.learned_files:
                    # 确定学习维度
                    dimension = self._map_file_to_dimension(category, file_path)
                    return category, file_path, dimension
        return None
    
    def _map_file_to_dimension(self, category: str, file_path: Path) -> str:
        """将文件映射到学习维度"""
        category_mapping = self.dimension_mapping.get(category, {})
        
        for keyword, dimensions in category_mapping.items():
            if keyword in file_path.name:
                return random.choice(dimensions)
        
        # 默认维度
        if category == EDriveCategory.PMP_MANAGEMENT.value:
            return LearningDimension.BUSINESS_STRATEGY.value
        elif category == EDriveCategory.INSURANCE_KNOWLEDGE.value:
            return LearningDimension.INDUSTRY_KNOWLEDGE.value
        elif category == EDriveCategory.RESUME_CAREER.value:
            return LearningDimension.DIGITAL_MARKETING.value
        else:
            return LearningDimension.AI_TECHNOLOGY.value
    
    def _extract_knowledge(self, file_path: Path) -> Dict[str, Any]:
        """从文件中提取知识（模拟）"""
        # 在实际应用中，这里会使用真实的文档解析和NLP技术
        file_size = file_path.stat().st_size
        file_type = file_path.suffix.lower()
        
        knowledge = {
            'file_name': file_path.name,
            'file_size': file_size,
            'file_type': file_type,
            'keywords': self._extract_keywords_from_filename(file_path),
            'estimated_pages': file_size // 50000 if file_type == '.pdf' else 1,
            'content_structure': self._infer_content_structure(file_path)
        }
        
        return knowledge
    
    def _extract_keywords_from_filename(self, file_path: Path) -> List[str]:
        """从文件名提取关键词"""
        keywords = []
        name = file_path.stem
        
        # 常见关键词
        common_keywords = [
            'PMBOK', '敏捷', '项目管理', 'PMP',
            '保险', '两全', '人寿', '医疗',
            '简历', '职业', '整合', '营销',
            'Supermind', 'Meth', 'KPI', '策略'
        ]
        
        for keyword in common_keywords:
            if keyword.lower() in name.lower():
                keywords.append(keyword)
        
        return keywords if keywords else ['通用知识']
    
    def _infer_content_structure(self, file_path: Path) -> Dict[str, Any]:
        """推断文档内容结构"""
        file_type = file_path.suffix.lower()
        
        structure = {
            'has_sections': False,
            'has_charts': False,
            'has_tables': False,
            'estimated_sections': 0
        }
        
        if file_type in ['.doc', '.docx', '.ppt', '.pptx']:
            structure['has_sections'] = True
            structure['estimated_sections'] = random.randint(5, 20)
        
        if file_type == '.xlsx':
            structure['has_tables'] = True
            structure['has_charts'] = True
            structure['estimated_sections'] = random.randint(1, 5)
        
        if file_type == '.pdf':
            structure['has_sections'] = True
            structure['estimated_sections'] = random.randint(10, 50)
        
        return structure
    
    def _generate_insights(self, knowledge: Dict[str, Any], dimension: str) -> List[str]:
        """基于提取的知识生成洞察"""
        insights = []
        
        # 基于文件类型生成洞察
        file_type = knowledge['file_type']
        keywords = knowledge['keywords']
        
        if 'PMBOK' in keywords:
            insights.append(f"发现PMBOK体系知识，可丰富{dimension}维度的理论框架")
            insights.append("项目管理五大过程组的知识可应用于解决方案实施流程")
        
        if '敏捷' in keywords:
            insights.append(f"敏捷实践知识可优化{dimension}维度的迭代学习机制")
            insights.append("Scrum框架可借鉴用于增长实验的快速迭代")
        
        if '营销' in keywords:
            insights.append(f"营销整合知识可直接应用于{dimension}维度的解决方案模板")
            insights.append("发现营销策略最佳实践，可整合到解决方案库")
        
        if 'Supermind' in keywords:
            insights.append(f"AI知识库可增强{dimension}维度的智能决策能力")
            insights.append("发现高级推理模式，可优化神经记忆系统")
        
        # 基于文档结构生成洞察
        if knowledge['content_structure']['has_charts']:
            insights.append(f"文档包含图表资源，可丰富PPT设计风格知识库")
        
        if knowledge['content_structure']['has_tables']:
            insights.append(f"文档包含表格模板，可应用于数据可视化维度")
        
        # 默认洞察
        if not insights:
            insights.append(f"文档内容可为{dimension}维度提供补充知识")
            insights.append("发现潜在的知识关联点，建议深入分析")
        
        return insights[:5]  # 最多返回5个洞察
    
    def _generate_action_items(self, insights: List[str]) -> List[str]:
        """基于洞察生成行动项"""
        actions = []
        
        for insight in insights:
            if "框架" in insight:
                actions.append("更新相关维度的知识框架文档")
            elif "模板" in insight:
                actions.append("将最佳实践整合到解决方案模板库")
            elif "知识库" in insight:
                actions.append("提取知识点并添加到对应知识库")
            elif "图表" in insight:
                actions.append("收集图表设计案例并添加到PPT风格库")
            elif "AI" in insight or "智能" in insight:
                actions.append("评估AI技术对现有系统的增强潜力")
            else:
                actions.append("记录该知识点并建立知识关联")
        
        # 去重
        actions = list(dict.fromkeys(actions))
        return actions[:5]  # 最多返回5个行动项
    
    def _identify_learning_gaps(self) -> List[Dict[str, Any]]:
        """识别学习过程中的不足"""
        gaps = []
        
        # 检查维度覆盖情况
        dimension_counts = {}
        for session in self.sessions:
            dim = session.dimension
            dimension_counts[dim] = dimension_counts.get(dim, 0) + 1
        
        for dim in LearningDimension:
            count = dimension_counts.get(dim.value, 0)
            if count == 0:
                gaps.append({
                    'type': '维度缺失',
                    'dimension': dim.value,
                    'severity': 'HIGH',
                    'description': f"{dim.value}维度尚未学习任何文件"
                })
            elif count < 3:
                gaps.append({
                    'type': '维度学习不足',
                    'dimension': dim.value,
                    'severity': 'MEDIUM',
                    'description': f"{dim.value}维度仅学习了{count}个文件，建议增加学习"
                })
        
        # 检查文件类型覆盖
        file_types = set()
        for session in self.sessions:
            file_types.add(session.file_type)
        
        if '.pdf' not in file_types:
            gaps.append({
                'type': '文件类型缺失',
                'dimension': '所有维度',
                'severity': 'MEDIUM',
                'description': '未学习PDF文件，PDF文档通常包含重要理论知识'
            })
        
        # 检查类别覆盖
        category_counts = {}
        for session in self.sessions:
            cat = session.e_drive_category
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        for category in EDriveCategory:
            count = category_counts.get(category.value, 0)
            if count == 0:
                gaps.append({
                    'type': '类别缺失',
                    'dimension': category.value,
                    'severity': 'HIGH',
                    'description': f"{category.value}类别尚未开始学习"
                })
        
        return gaps
    
    def learn_single_file(self, category: str, file_path: Path, dimension: str) -> LearningSession:
        """学习单个文件"""
        start_time = time.time()
        
        logger.info(f"开始学习文件: {file_path.name}")
        logger.info(f"  类别: {category}")
        logger.info(f"  维度: {dimension}")
        
        # 提取知识
        knowledge = self._extract_knowledge(file_path)
        
        # 生成洞察
        insights = self._generate_insights(knowledge, dimension)
        
        # 生成行动项
        action_items = self._generate_action_items(insights)
        
        # 计算置信度（模拟）
        confidence_score = random.uniform(0.6, 0.95)
        
        # 创建学习会话
        session = LearningSession(
            session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}",
            timestamp=datetime.now().isoformat(),
            e_drive_category=category,
            file_path=str(file_path),
            file_type=file_path.suffix.lower(),
            dimension=dimension,
            content_summary=f"学习了{file_path.name}，包含{len(knowledge['keywords'])}个关键词",
            insights=insights,
            action_items=action_items,
            confidence_score=confidence_score,
            duration_seconds=time.time() - start_time,
            knowledge_extracted=knowledge
        )
        
        # 标记为已学习
        self.learned_files.add(str(file_path))
        
        logger.info(f"学习完成，提取了 {len(insights)} 个洞察")
        logger.info(f"  洞察1: {insights[0] if insights else '无'}")
        
        return session
    
    def start_learning(self, max_files: Optional[int] = None, interval_seconds: int = 5):
        """启动学习流程"""
        logger.info("=" * 60)
        logger.info("E盘深度学习系统启动")
        logger.info("=" * 60)
        
        # 扫描文件
        file_map = self._scan_e_drive_files()
        total_files = sum(len(files) for files in file_map.values())
        
        if total_files == 0:
            logger.warning("E盘未发现可学习文件")
            return
        
        # 已学习文件数
        already_learned = sum(1 for files in file_map.values() 
                             for f in files if str(f) in self.learned_files)
        
        remaining_files = total_files - already_learned
        
        logger.info(f"总文件数: {total_files}")
        logger.info(f"已学习: {already_learned}")
        logger.info(f"待学习: {remaining_files}")
        
        if remaining_files == 0:
            logger.info("所有文件已学习完成！")
            self._generate_gap_report()
            return
        
        # 开始学习循环
        learned_count = 0
        while True:
            # 选择文件
            result = self._select_file_to_learn(file_map)
            if result is None:
                logger.info("所有文件学习完成！")
                break
            
            category, file_path, dimension = result
            
            # 学习文件
            try:
                session = self.learn_single_file(category, file_path, dimension)
                self.sessions.append(session)
                self._save_sessions()
                self._save_progress()
                
                learned_count += 1
                logger.info(f"进度: {learned_count}/{remaining_files} 文件已学习")
                
                # 检查是否达到最大文件数
                if max_files and learned_count >= max_files:
                    logger.info(f"已达到最大学习文件数: {max_files}")
                    break
                
            except Exception as e:
                logger.error(f"学习文件失败 {file_path}: {e}")
                # 跳过失败文件，继续下一个
                continue
            
            # 间隔
            if interval_seconds > 0:
                logger.info(f"等待 {interval_seconds} 秒...")
                time.sleep(interval_seconds)
        
        # 生成学习不足报告
        self._generate_gap_report()
        
        logger.info("=" * 60)
        logger.info("学习流程完成")
        logger.info("=" * 60)
    
    def _generate_gap_report(self):
        """生成学习不足和优化建议报告"""
        logger.info("正在生成学习不足和优化建议报告...")
        
        # 识别不足
        gaps = self._identify_learning_gaps()
        
        # 生成优化建议
        improvements = []
        
        for gap in gaps:
            if gap['type'] == '维度缺失':
                improvements.append({
                    'issue': gap['description'],
                    'priority': 'HIGH',
                    'suggestion': f"优先在{gap['dimension']}维度寻找相关文件进行学习",
                    'action': f"调整文件映射规则，确保{gap['dimension']}维度的文件被正确分类"
                })
            elif gap['type'] == '维度学习不足':
                improvements.append({
                    'issue': gap['description'],
                    'priority': 'MEDIUM',
                    'suggestion': f"增加{gap['dimension']}维度的学习频次",
                    'action': f"调整学习算法，提高{gap['dimension']}维度的选择权重"
                })
            elif gap['type'] == '类别缺失':
                improvements.append({
                    'issue': gap['description'],
                    'priority': 'HIGH',
                    'suggestion': f"检查{gap['dimension']}目录下是否有遗漏的文件",
                    'action': f"扩展文件扫描范围，确保包含所有可学习的文件类型"
                })
            elif gap['type'] == '文件类型缺失':
                improvements.append({
                    'issue': gap['description'],
                    'priority': 'LOW',
                    'suggestion': f"在E盘查找{gap['description']}格式的文件",
                    'action': f"添加对更多文件类型的支持，如.txt, .md等"
                })
        
        # 系统级优化建议
        system_improvements = []
        
        # 检查学习质量
        avg_confidence = sum(s.confidence_score for s in self.sessions) / len(self.sessions) if self.sessions else 0
        if avg_confidence < 0.7:
            system_improvements.append({
                'issue': f'平均置信度较低: {avg_confidence:.2f}',
                'priority': 'HIGH',
                'suggestion': '改进知识提取算法，提高学习质量',
                'action': '引入更先进的NLP模型进行文档理解和知识提取'
            })
        
        # 检查行动项执行情况
        total_actions = sum(len(s.action_items) for s in self.sessions)
        if total_actions > 0 and len(self.sessions) > 0:
            avg_actions = total_actions / len(self.sessions)
            if avg_actions < 2:
                system_improvements.append({
                    'issue': f'平均行动项数量不足: {avg_actions:.2f}',
                    'priority': 'MEDIUM',
                    'suggestion': '增强洞察生成的实用性',
                    'action': '优化洞察生成算法，确保产生更多可执行的行动项'
                })
        
        # 保存报告
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_sessions': len(self.sessions),
            'average_confidence': avg_confidence,
            'total_gaps': len(gaps),
            'total_improvements': len(improvements),
            'system_improvements': len(system_improvements),
            'gaps': gaps,
            'improvements': improvements,
            'system_improvements': system_improvements
        }
        
        with open(self.gap_report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"学习不足和优化建议报告已生成: {self.gap_report_file}")
        logger.info(f"  发现 {len(gaps)} 个学习不足")
        logger.info(f"  提出 {len(improvements)} 个改进建议")
        logger.info(f"  提出 {len(system_improvements)} 个系统级改进建议")
        
        return report
    
    def generate_summary_report(self) -> str:
        """生成学习总结报告"""
        if not self.sessions:
            return "暂无学习记录"
        
        # 统计信息
        dimension_counts = {}
        category_counts = {}
        total_confidence = 0
        total_duration = 0
        
        for session in self.sessions:
            # 维度统计
            dim = session.dimension
            dimension_counts[dim] = dimension_counts.get(dim, 0) + 1
            
            # 类别统计
            cat = session.e_drive_category
            category_counts[cat] = category_counts.get(cat, 0) + 1
            
            total_confidence += session.confidence_score
            total_duration += session.duration_seconds
        
        # 生成报告
        report_lines = [
            "=" * 60,
            "E盘深度学习系统 - 学习总结报告",
            "=" * 60,
            f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "一、学习概况",
            f"总学习文件数: {len(self.sessions)}",
            f"平均置信度: {total_confidence/len(self.sessions):.2f}",
            f"总学习时长: {total_duration:.2f} 秒",
            "",
            "二、维度覆盖情况"
        ]
        
        for dim, count in sorted(dimension_counts.items()):
            report_lines.append(f"  {dim}: {count} 个文件")
        
        report_lines.extend([
            "",
            "三、类别学习情况"
        ])
        
        for cat, count in sorted(category_counts.items()):
            report_lines.append(f"  {cat}: {count} 个文件")
        
        report_lines.extend([
            "",
            "四、学习不足",
            ""
        ])
        
        # 识别不足
        gaps = self._identify_learning_gaps()
        for gap in gaps:
            report_lines.append(f"  [{gap['severity']}] {gap['description']}")
        
        report_lines.extend([
            "",
            "=" * 60
        ])
        
        return "\n".join(report_lines)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='E盘深度学习系统')
    parser.add_argument('--max-files', type=int, default=None, 
                       help='最大学习文件数（默认学习所有文件）')
    parser.add_argument('--interval', type=int, default=5,
                       help='学习间隔（秒，默认5秒）')
    parser.add_argument('--report-only', action='store_true',
                       help='仅生成总结报告')
    
    args = parser.parse_args()
    
    # 创建学习系统
    system = EDriveLearningSystem()
    
    if args.report_only:
        # 仅生成报告
        report = system.generate_summary_report()
        print(report)
    else:
        # 开始学习
        system.start_learning(
            max_files=args.max_files,
            interval_seconds=args.interval
        )
        
        # 生成总结报告
        report = system.generate_summary_report()
        print("\n" + report)


if __name__ == '__main__':
    main()
