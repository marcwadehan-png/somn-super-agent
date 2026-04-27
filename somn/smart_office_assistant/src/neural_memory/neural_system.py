"""
__all__ = [
    'create_neural_system',
    'discover_value_and_generate_dimensions',
    'evolve_system',
    'generate_core_strategy',
    'generate_system_report',
    'query_with_evidence',
    'record_research_finding',
]

[DEPRECATED] 神经记忆系统 V1 — 兼容层
Deprecated since: 2026-04-06
Replacement: neural_system.py (V3 主线，当前为 neural_memory_system_v3.py)
Removal target: 2026-07-06
Policy: file/系统文件/systems/VERSION_POLICY.md

此文件为向后兼容保留。新代码请使用 V3 主线版本（neural_memory_system_v3.py）。
Phase 1 版本切换完成后，此文件将重命名为 neural_system_v1.py。

--- 原始文档 ---
神经记忆系统 - 核心整合模块
Neural Memory System - Core Integration
"""

import logging
import json
import yaml
from pathlib import Path
from src.core.paths import LEARNING_DIR
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import uuid

from .memory_engine import MemoryEngine
from .knowledge_engine import KnowledgeEngine
from .reasoning_engine import ReasoningEngine, Premise, Conclusion, ReasoningType
from .learning_engine import LearningEngine, LearningType
from .validation_engine import ValidationEngine, ValidationType, ValidationStatus

logger = logging.getLogger(__name__)
class NeuralMemorySystem:
    """
    神经记忆系统
    
    核心特性:
    1. 有记忆的演化 - 每次演化都基于历史记忆
    2. 有知识的推理 - 每次推理都调用知识库
    3. 有逻辑的结论 - 每个结论都有推理链和证据支撑
    4. 有basis的strategy - 每个strategy都基于验证过的数据
    5. 有验证的更新 - 每次知识更新都经过验证
    """
    
    def __init__(self, base_path: str = None):
        from src.core.paths import MEMORY_DIR, LEARNING_DIR, KNOWLEDGE_DIR
        # base_path 通常来自 daily_learning.py,值为 PROJECT_ROOT
        # 子引擎应使用 paths.py 定义的规范数据路径,而非 base_path 直接拼接
        self.base_path = Path(base_path) if base_path else MEMORY_DIR
        project_root = self.base_path  # DailyLearningExecutor 传入的 PROJECT_ROOT

        # init各子引擎 -- 使用正确的数据路径
        # MemoryEngine 实际记忆文件位于 data/learning/memory/(175+ 个 MEM_*.yaml)
        self.memory = MemoryEngine(str(LEARNING_DIR))
        # KnowledgeEngine 的知识文件应位于 data/knowledge/knowledge_base/
        self.knowledge = KnowledgeEngine(str(KNOWLEDGE_DIR))
        self.reasoning = ReasoningEngine(str(project_root))
        self.learning = LearningEngine(str(project_root))
        self.validation = ValidationEngine(str(project_root))
        
        # 系统状态
        self.system_state = {
            "version": "1.0.0",
            "initialized_at": datetime.now().isoformat(),
            "total_memories": 0,
            "total_knowledge": 0,
            "total_validations": 0,
            "evolution_count": 0
        }
        
        # 加载系统状态
        self._load_system_state()
    
    def _load_system_state(self):
        """加载系统状态"""
        state_file = self.base_path / "system_state.json"
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                self.system_state.update(json.load(f))
    
    def _save_system_state(self):
        """保存系统状态"""
        state_file = self.base_path / "system_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(self.system_state, f, ensure_ascii=False, indent=2)
    
    # ==================== 研究发现录入 ====================
    
    def record_research_finding(self, finding: Dict) -> Dict:
        """
        记录研究发现(完整流程)
        
        流程:
        1. 编码为记忆单元
        2. 提取关键概念
        3. 建立知识关联
        4. 触发学习机制
        5. 返回记忆ID和初步结论
        
        Args:
            finding: 研究发现 {title, description, evidence, confidence, scenarios, ...}
            
        Returns:
            {memory_id, concept_ids, initial_conclusion, suggestions}
        """
        # 1. 编码为记忆单元
        memory_id = self.memory.record_finding(finding)
        
        # 2. 提取关键概念
        concept_ids = self._extract_concepts(finding)
        
        # 3. 建立记忆关联
        self._establish_memory_associations(memory_id, finding)
        
        # 4. 触发学习机制
        learning_events = self._trigger_learning(finding, memory_id)
        
        # 5. generate初步结论
        initial_conclusion = self._generate_initial_conclusion(finding)
        
        # 6. generate验证建议
        validation_suggestions = self._suggest_validation(finding)
        
        # 更新系统状态
        self.system_state["total_memories"] += 1
        self._save_system_state()
        
        return {
            "memory_id": memory_id,
            "concept_ids": concept_ids,
            "initial_conclusion": initial_conclusion,
            "learning_events": [e.event_id for e in learning_events],
            "validation_suggestions": validation_suggestions
        }
    
    def _extract_concepts(self, finding: Dict) -> List[str]:
        """从发现中提取概念"""
        concepts = []
        
        # 简化的概念提取(实际应使用NLP)
        content = str(finding.get("title", "")) + str(finding.get("description", ""))
        
        # 预定义的概念关键词
        concept_keywords = {
            "情绪概念": ["情绪", "愉悦", "焦虑", "兴奋", "满意", "体验"],
            "价值概念": ["转化", "增长", "留存", "效率", "满意度"],
            "strategy概念": ["strategy", "设计", "方案", "措施", "干预"]
        }
        
        for concept_type, keywords in concept_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    # 添加到知识库
                    concept_id = self.knowledge.add_concept(concept_type, {
                        "概念名": f"{keyword}相关",
                        "来源": "研究发现",
                        "定义": f"从研究中发现与'{keyword}'相关的概念"
                    })
                    concepts.append(concept_id)
        
        return concepts
    
    def _establish_memory_associations(self, memory_id: str, finding: Dict):
        """建立记忆关联"""
        # 查找相关记忆
        related_memories = self.memory.query_memory(
            query_text=finding.get("title", ""),
            filters={"应用场景": finding.get("scenarios", [""])[0]} if finding.get("scenarios") else None
        )
        
        # 建立关联
        for related in related_memories[:5]:  # 最多关联5个
            if related.get("记忆ID") != memory_id:
                self.memory.add_association(
                    memory_id,
                    related["记忆ID"],
                    "相似",
                    0.5
                )
    
    def _trigger_learning(self, finding: Dict, memory_id: str) -> List:
        """触发学习机制"""
        events = []
        
        # 实例学习:收集相似发现,提取模式
        similar_findings = self.memory.query_memory(
            query_text=finding.get("title", "")
        )
        
        if len(similar_findings) >= 5:
            instances = [
                {"characteristics": f.get("内容层", {}).get("发现标题", ""), "置信度": f.get("内容层", {}).get("置信度评估", {}).get("置信度评分", 50) / 100}
                for f in similar_findings
            ]
            pattern, event = self.learning.learn_from_instance(instances, "研究发现模式")
            if event:
                events.append(event)
        
        return events
    
    def _generate_initial_conclusion(self, finding: Dict) -> Dict:
        """generate初步结论"""
        # 构建前提
        evidence_premise = Premise(
            content=finding.get("description", ""),
            confidence=finding.get("confidence_score", 50) / 100,
            source="研究发现",
            evidence_type="观察证据"
        )
        
        # 使用归纳推理generate结论
        conclusion = self.reasoning.induce(
            [evidence_premise],
            f"基于研究发现的假设:{finding.get('title', '')}"
        )
        
        if conclusion:
            self.reasoning.save_conclusion(conclusion)
        
        return {
            "content": conclusion.content if conclusion else "",
            "confidence": conclusion.confidence if conclusion else 0.5,
            "reasoning_type": "归纳推理"
        }
    
    def _suggest_validation(self, finding: Dict) -> Dict:
        """generate验证建议"""
        hypothesis = {
            "假设ID": "待定",
            "假设内容": finding.get("title", ""),
            "置信度": finding.get("confidence_score", 50) / 100
        }
        
        plan = self.validation.create_validation_plan(hypothesis)
        
        return {
            "验证类型": plan.validation_type.value,
            "建议样本量": plan.sample_size,
            "验证周期": plan.duration,
            "主要metrics": plan.metrics
        }
    
    # ==================== 价值发现与维度generate ====================
    
    def discover_value_and_generate_dimensions(self, research_data: Dict) -> Dict:
        """
        价值发现 → 数据维度generate
        
        流程:
        1. 分析研究数据,recognize潜在价值
        2. 基于价值类型,generate对应数据维度
        3. 为每个维度定义测量方法
        4. 建立维度与价值的关联
        
        Args:
            research_data: 研究数据
            
        Returns:
            {values, dimensions, relationships, confidence}
        """
        # 1. 价值recognize
        values = self._identify_values(research_data)
        
        # 2. 维度generate
        dimensions = self._generate_dimensions_from_values(values)
        
        # 3. 建立关联
        relationships = []
        for value in values:
            for dim in dimensions:
                if value.get("关联维度") == dim.get("维度ID"):
                    relationships.append({
                        "价值": value["价值ID"],
                        "维度": dim["维度ID"],
                        "关联强度": 0.8
                    })
        
        # 4. 置信度评估
        confidence = self._evaluate_value_confidence(values, dimensions)
        
        return {
            "values": values,
            "dimensions": dimensions,
            "relationships": relationships,
            "confidence": confidence,
            "evidence_chain": self._build_value_evidence_chain(values)
        }
    
    def _identify_values(self, data: Dict) -> List[Dict]:
        """recognize价值类型"""
        values = []
        
        # 预定义价值类型
        value_types = {
            "转化价值": ["转化率", "购买", "付费"],
            "增长价值": ["增长", "新用户", "流量"],
            "留存价值": ["留存", "复购", "忠诚"],
            "效率价值": ["效率", "成本", "时间"],
            "体验价值": ["体验", "满意度", "NPS"],
            "创新价值": ["创新", "新功能", "差异化"]
        }
        
        content = str(data).lower()
        value_id = 1
        
        for value_type, keywords in value_types.items():
            for keyword in keywords:
                if keyword in content:
                    values.append({
                        "价值ID": f"VAL_{value_id:03d}",
                        "价值类型": value_type,
                        "关键词": keyword,
                        "关联维度": f"DIM_{value_id:03d}",
                        "置信度": 0.7
                    })
                    value_id += 1
                    break  # 每种类型只recognize一次
        
        return values
    
    def _generate_dimensions_from_values(self, values: List[Dict]) -> List[Dict]:
        """基于价值generate数据维度"""
        dimensions = []
        
        dimension_templates = {
            "转化价值": {
                "测量metrics": ["转化率", "转化周期", "转化成本"],
                "数据来源": ["行为数据", "交易数据"],
                "分析方法": ["漏斗分析", "归因分析"]
            },
            "增长价值": {
                "测量metrics": ["增长率", "获客成本", "用户生命周期价值"],
                "数据来源": ["用户数据", "流量数据"],
                "分析方法": ["增长模型", "同期群分析"]
            },
            "留存价值": {
                "测量metrics": ["留存率", "复购率", "流失率"],
                "数据来源": ["行为数据", "用户数据"],
                "分析方法": ["留存曲线", "生存分析"]
            },
            "效率价值": {
                "测量metrics": ["效率metrics", "成本metrics", "时间metrics"],
                "数据来源": ["运营数据", "财务数据"],
                "分析方法": ["效率分析", "成本效益分析"]
            },
            "体验价值": {
                "测量metrics": ["满意度", "NPS", "体验评分"],
                "数据来源": ["调研数据", "反馈数据"],
                "分析方法": ["体验度量", "情感分析"]
            },
            "创新价值": {
                "测量metrics": ["创新metrics", "差异化metrics", "实验metrics"],
                "数据来源": ["实验数据", "市场数据"],
                "分析方法": ["创新评估", "对比分析"]
            }
        }
        
        for value in values:
            template = dimension_templates.get(value["价值类型"], {})
            if template:
                dimensions.append({
                    "维度ID": value["关联维度"],
                    "维度名称": f"{value['价值类型']}维度",
                    "关联价值": value["价值ID"],
                    "测量metrics": template.get("测量metrics", []),
                    "数据来源": template.get("数据来源", []),
                    "分析方法": template.get("分析方法", []),
                    "状态": "待验证",
                    "创建时间": datetime.now().isoformat()
                })
        
        return dimensions
    
    def _evaluate_value_confidence(self, values: List[Dict], dimensions: List[Dict]) -> float:
        """评估价值发现的置信度"""
        if not values:
            return 0.0
        
        # 基于价值数量和维度匹配度
        value_count_factor = min(1.0, len(values) / 3)
        dimension_match_factor = len(dimensions) / len(values) if values else 0
        
        return (value_count_factor + dimension_match_factor) / 2
    
    def _build_value_evidence_chain(self, values: List[Dict]) -> List[str]:
        """构建价值发现的证据链"""
        chain = []
        for value in values:
            chain.append(f"recognize价值类型: {value['价值类型']}")
            chain.append(f"证据关键词: {value['关键词']}")
            chain.append(f"初始置信度: {value['置信度']:.2f}")
        return chain
    
    # ==================== strategygenerate ====================
    
    def generate_core_strategy(self, research_findings: List[Dict], 
                               value_discoveries: List[Dict]) -> Dict:
        """
        generate核心strategy(完整流程)
        
        流程:
        1. 整合研究发现和价值发现
        2. 模式recognize和洞察提炼
        3. generatestrategy假设
        4. 设计验证方案
        5. 评估strategy置信度
        
        Args:
            research_findings: 研究发现列表
            value_discoveries: 价值发现列表
            
        Returns:
            {strategy_id, content, confidence, validation_plan, evidence_chain}
        """
        # 1. 数据整合
        integrated_data = self._integrate_research_data(research_findings, value_discoveries)
        
        # 2. 模式recognize
        patterns = self._identify_patterns(integrated_data)
        
        # 3. generatestrategy假设
        strategy = self._formulate_strategy(patterns, integrated_data)
        
        # 4. 设计验证方案
        validation_plan = self.validation.create_validation_plan({
            "假设ID": strategy["strategy_id"],
            "假设内容": strategy["content"],
            "置信度": strategy["confidence"]
        })
        
        # 5. 记录strategy
        self._record_strategy(strategy)
        
        return {
            "strategy_id": strategy["strategy_id"],
            "content": strategy["content"],
            "confidence": strategy["confidence"],
            "reasoning_process": strategy["reasoning_process"],
            "validation_plan": {
                "type": validation_plan.validation_type.value,
                "sample_size": validation_plan.sample_size,
                "duration": validation_plan.duration
            },
            "evidence_chain": strategy["evidence_chain"]
        }
    
    def _integrate_research_data(self, findings: List[Dict], values: List[Dict]) -> Dict:
        """整合研究数据"""
        return {
            "研究发现数": len(findings),
            "价值发现数": len(values),
            "平均置信度": sum(f.get("confidence_score", 50) for f in findings) / len(findings) if findings else 0,
            "价值类型": list(set(v.get("价值类型", "") for v in values))
        }
    
    def _identify_patterns(self, data: Dict) -> List[Dict]:
        """recognize模式"""
        patterns = []
        
        # 简化的模式recognize
        if data["研究发现数"] >= 3:
            patterns.append({
                "模式类型": "多源验证",
                "描述": "多个研究发现支持类似结论",
                "强度": min(1.0, data["研究发现数"] / 5)
            })
        
        if len(data["价值类型"]) >= 2:
            patterns.append({
                "模式类型": "多维价值",
                "描述": "研究发现涉及多个价值维度",
                "强度": min(1.0, len(data["价值类型"]) / 3)
            })
        
        return patterns
    
    def _formulate_strategy(self, patterns: List[Dict], data: Dict) -> Dict:
        """形成strategy"""
        strategy_id = f"STR_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 基于模式generatestrategy内容
        strategy_content = "基于研究发现,建议采取以下strategy:\n"
        for pattern in patterns:
            strategy_content += f"- {pattern['描述']}(强度: {pattern['强度']:.2f})\n"
        
        # 计算置信度
        confidence = data["平均置信度"] / 100 if data["平均置信度"] else 0.5
        for pattern in patterns:
            confidence = min(1.0, confidence + pattern["强度"] * 0.1)
        
        # 构建证据链
        evidence_chain = [
            f"研究数据整合: {data['研究发现数']}个发现, {data['价值发现数']}个价值",
            f"recognize模式: {len(patterns)}个",
            f"价值维度: {', '.join(data['价值类型'])}"
        ]
        
        return {
            "strategy_id": strategy_id,
            "content": strategy_content,
            "confidence": confidence,
            "reasoning_process": "数据整合 → 模式recognize → strategygenerate",
            "evidence_chain": evidence_chain
        }
    
    def _record_strategy(self, strategy: Dict):
        """记录strategy"""
        # 作为特殊类型的记忆存储
        self.memory.record_finding({
            "title": f"核心strategy: {strategy['strategy_id']}",
            "description": strategy["content"],
            "source_type": "strategygenerate",
            "source_detail": "神经记忆系统",
            "confidence_score": int(strategy["confidence"] * 100),
            "scenarios": ["核心strategy"]
        })
    
    # ==================== 系统演化 ====================
    
    def evolve_system(self, trigger: str, changes: Dict) -> Dict:
        """
        系统演化
        
        Args:
            trigger: 演化触发原因
            changes: 变更内容
            
        Returns:
            演化记录
        """
        evolution_id = f"EVO_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 记录演化历史
        evolution_record = {
            "演化ID": evolution_id,
            "触发原因": trigger,
            "变更内容": changes,
            "演化前状态": dict(self.system_state),
            "演化时间": datetime.now().isoformat()
        }
        
        # 应用变更
        self._apply_evolution(changes)
        
        # 更新系统状态
        self.system_state["evolution_count"] += 1
        self._save_system_state()
        
        # 保存演化记录
        self._save_evolution_record(evolution_record)
        
        return evolution_record
    
    def _apply_evolution(self, changes: Dict):
        """应用演化变更"""
        change_type = changes.get("类型", "")
        
        if change_type == "新增概念":
            self.knowledge.add_concept(
                changes.get("概念类型", "概念"),
                changes.get("概念数据", {})
            )
        elif change_type == "新增规则":
            self.knowledge.add_rule(
                changes.get("规则类型", "规则"),
                changes.get("规则数据", {})
            )
        elif change_type == "置信度更新":
            self.knowledge.update_confidence(
                changes.get("实体类型", "concept"),
                changes.get("实体ID", ""),
                changes.get("新置信度", 0.5),
                changes.get("证据", "")
            )
    
    def _save_evolution_record(self, record: Dict):
        """保存演化记录"""
        evolution_path = self.base_path / "evolution"
        evolution_path.mkdir(parents=True, exist_ok=True)
        
        file_path = evolution_path / f"{record['演化ID']}.yaml"
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(record, f, allow_unicode=True, default_flow_style=False)
    
    # ==================== 查询与报告 ====================
    
    def query_with_evidence(self, query: str) -> Dict:
        """
        带证据的查询
        
        Args:
            query: 查询内容
            
        Returns:
            {answer, confidence, evidence_chain, related_memories}
        """
        # 1. 检索相关记忆
        memories = self.memory.query_memory(query_text=query)
        
        # 2. 查询相关知识
        concepts = self.knowledge.query_concept(concept_name=query)
        rules = self.knowledge.query_rule(applicable_scenario=query)
        
        # 3. 整合信息generate回答
        answer = self._synthesize_answer(memories, concepts, rules, query)
        
        # 4. 构建证据链
        evidence_chain = self._build_query_evidence_chain(memories, concepts, rules)
        
        # 5. 计算置信度
        confidence = self._calculate_query_confidence(memories, concepts, rules)
        
        return {
            "answer": answer,
            "confidence": confidence,
            "evidence_chain": evidence_chain,
            "related_memories": [m.get("记忆ID") for m in memories[:5]],
            "related_concepts": [c.get("概念ID") for c in concepts[:5]]
        }
    
    def _synthesize_answer(self, memories: List, concepts: List, 
                           rules: List, query: str) -> str:
        """synthesizegenerate回答"""
        answer_parts = []
        
        if memories:
            answer_parts.append(f"基于{len(memories)}条相关记忆:")
            for m in memories[:3]:
                content = m.get("内容层", {})
                answer_parts.append(f"- {content.get('发现标题', '未知发现')}")
        
        if concepts:
            answer_parts.append(f"\n相关概念:{', '.join(c.get('概念名', '') for c in concepts[:3])}")
        
        if rules:
            answer_parts.append(f"\n相关规则:{rules[0].get('名称', '') if rules else '无'}")
        
        return "\n".join(answer_parts) if answer_parts else "未找到相关信息"
    
    def _build_query_evidence_chain(self, memories: List, concepts: List, 
                                     rules: List) -> List[str]:
        """构建查询证据链"""
        chain = []
        
        for m in memories[:3]:
            chain.append(f"记忆证据: {m.get('记忆ID', '')} (置信度: {m.get('内容层', {}).get('置信度评估', {}).get('置信度评分', 0)}%)")
        
        for c in concepts[:2]:
            chain.append(f"概念支撑: {c.get('概念名', '')}")
        
        for r in rules[:1]:
            chain.append(f"规则basis: {r.get('名称', '')} (置信度: {r.get('置信度', 0):.2f})")
        
        return chain
    
    def _calculate_query_confidence(self, memories: List, concepts: List, 
                                    rules: List) -> float:
        """计算查询置信度"""
        if not memories and not concepts and not rules:
            return 0.0
        
        # 记忆置信度
        memory_conf = sum(m.get("内容层", {}).get("置信度评估", {}).get("置信度评分", 50) for m in memories) / len(memories) / 100 if memories else 0
        
        # 规则置信度
        rule_conf = sum(r.get("置信度", 0.5) for r in rules) / len(rules) if rules else 0.5
        
        return (memory_conf * 0.6 + rule_conf * 0.4) if memories else rule_conf * 0.5
    
    def generate_system_report(self) -> Dict:
        """generate系统报告"""
        memory_stats = self.memory.get_memory_statistics()
        knowledge_stats = self.knowledge.get_statistics()
        
        return {
            "系统状态": self.system_state,
            "记忆系统": memory_stats,
            "知识系统": knowledge_stats,
            "系统健康度": self._assess_system_health(memory_stats, knowledge_stats)
        }
    
    def _count_today_learning_events(self) -> int:
        """统计今日学习事件数量"""
        from datetime import timedelta
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = 0

        # 统计 learning/LE_*.yaml 今日事件
        learning_path = self.base_path / "learning"
        if learning_path.exists():
            for fp in learning_path.glob("LE_*.yaml"):
                try:
                    mtime = datetime.fromtimestamp(fp.stat().st_mtime)
                    if mtime >= today_start:
                        count += 1
                except Exception as e:
                    logger.debug(f"神经记忆加载失败: {e}")

        # 统计 daily_reports 今日报告
        reports_path = self.base_path / "daily_reports"
        if reports_path.exists():
            today_str = datetime.now().strftime('%Y%m%d')
            for fp in reports_path.glob(f"DLR_{today_str}*.yaml"):
                count += 1

        return count

    def _assess_system_health(self, memory_stats: Dict, knowledge_stats: Dict) -> Dict:
        """评估系统健康度"""
        health = {
            "总体评分": 0,
            "记忆完整性": 0,
            "知识覆盖率": 0,
            "推理能力": 0,
            "学习活跃度": 0
        }
        
        # 记忆完整性（兼容两种键名）
        total_mem = memory_stats.get("总记忆数", 0) or memory_stats.get("total_memories", 0)
        if total_mem > 0:
            health["记忆完整性"] = min(1.0, total_mem / 50)
        
        # 知识覆盖率
        total_knowledge = knowledge_stats.get("总体统计", {}).get("概念总数", 0) + \
                         knowledge_stats.get("总体统计", {}).get("规则总数", 0)
        if total_knowledge > 0:
            health["知识覆盖率"] = min(1.0, total_knowledge / 100)
        
        # 推理能力(简化)
        health["推理能力"] = 0.7 if knowledge_stats.get("总体统计", {}).get("规则总数", 0) > 10 else 0.4
        
        # 学习活跃度: 基于实际学习事件数量（非仅演化计数）
        # 今日学习事件 > 0 → 1.0；否则基于演化计数平滑
        today_events = self._count_today_learning_events()
        if today_events > 0:
            health["学习活跃度"] = 1.0  # 今日有学习活动
        else:
            health["学习活跃度"] = min(1.0, self.system_state.get("evolution_count", 0) / 10)
        
        # 总体评分
        health["总体评分"] = sum(v for k, v in health.items() if k != "总体评分") / 4
        
        return health

# 便捷函数
def create_neural_system(base_path: str = None) -> NeuralMemorySystem:
    """创建神经记忆system_instance"""
    if base_path is None:
        base_path = None
    return NeuralMemorySystem(base_path)

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
