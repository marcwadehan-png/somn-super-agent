"""
__all__ = [
    'execute_daily_learning',
    'run_daily_learning',
    'run_daily_learning_v2',
]

Somn - 每日自动学习执行脚本
Daily Learning Execution Script

Somn: 拉丁语 somnus(睡眠/梦境),隐喻神经记忆系统在休息中持续学习进化

遵循神经记忆系统的自主学习框架:
1. 实例学习 - 从新发现中提取模式
2. 验证学习 - 基于验证结果更新置信度
3. 错误学习 - 从失败中recognize错误假设
4. 关联学习 - 发现新的概念关联
5. 迁移学习 - 将知识应用到新场景
6. 强化学习 - 基于反馈调整行为

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  兼容层说明（v2.0 统一重构后）
本文件保留原始实现以确保现有调用链 100% 兼容。
新代码请使用：
    from .unified_learning_orchestrator import UnifiedLearningOrchestrator
    orchestrator = UnifiedLearningOrchestrator()
    report = orchestrator.execute_daily()
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import logging
import yaml
from pathlib import Path
from src.core.paths import LEARNING_DIR, PROJECT_ROOT
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sys

# 导入神经记忆系统组件
from .neural_system import NeuralMemorySystem, create_neural_system
from .learning_engine import LearningEngine, LearningType, LearningEvent
from .memory_engine import MemoryEngine
from .knowledge_engine import KnowledgeEngine
from .report_template import LearningReportTemplate

logger = logging.getLogger(__name__)

class LearningStage(Enum):
    """学习阶段"""
    DATA_SCAN = "数据扫描"
    INSTANCE_LEARNING = "实例学习"
    VALIDATION_LEARNING = "验证学习"
    ERROR_LEARNING = "错误学习"
    ASSOCIATION_LEARNING = "关联学习"
    FEEDBACK_INTEGRATION = "反馈整合"        # ⭐ 新增:强化学习反馈闭环
    TRANSFER_LEARNING = "迁移学习"           # ⭐ 新增:知识迁移与跨场景验证
    REPORT_GENERATION = "报告generate"

@dataclass
class DailyLearningReport:
    """每日学习报告"""
    report_id: str
    date: str
    execution_time: str
    
    # 数据扫描结果
    new_findings_count: int
    new_validations_count: int
    error_cases_count: int
    
    # 学习事件统计
    instance_learning_events: List[Dict]
    validation_learning_events: List[Dict]
    error_learning_events: List[Dict]
    association_learning_events: List[Dict]
    
    # 知识更新
    new_patterns: List[Dict]
    confidence_updates: List[Dict]
    new_associations: List[Dict]
    
    # ⭐ 强化学习(新增)
    rl_updates: List[Dict]          # Q-learning 更新记录
    q_table_snapshot: Dict          # 当前 Q 表快照
    
    # ⭐ 迁移学习(新增)
    transfer_hypotheses: List[Dict] # 新generate的迁移假设
    registered_knowledge: List[Dict] # 新注册的高置信度知识
    transfer_report: Dict           # 迁移学习状态报告

    # 系统状态
    system_health: Dict
    memory_stats: Dict
    knowledge_stats: Dict
    
    # 总结
    summary: str
    recommendations: List[str]

class DailyLearningExecutor:
    """每日学习执行器"""
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            base_path = str(PROJECT_ROOT)
        self.base_path = Path(base_path)
        self.neural_system = create_neural_system(base_path)
        self.learning_engine = self.neural_system.learning
        
        # 时间窗口(最近24小时)
        self.time_window = timedelta(hours=24)
        self.cutoff_time = datetime.now() - self.time_window
        
        # 学习结果存储
        self.learning_events: List[LearningEvent] = []
        self.new_patterns: List[Dict] = []
        self.confidence_updates: List[Dict] = []
        self.new_associations: List[Dict] = []

        # ⭐ 闭环组件(延迟init,避免循环导入)
        self._闭环_components_initialized = False
        self._feedback_pipeline = None
        self._roi_tracker = None
        self._rl_trigger = None
        self._transfer_learner = None
        
        # 报告路径
        self.reports_path = self.base_path / "daily_reports"
        self.reports_path.mkdir(parents=True, exist_ok=True)

        # ⭐ 跨天累积器: 将发现按场景累积,避免单日数据不足导致模式无法提取
        self._patterns_accumulator_path = self.base_path / "data" / "learning" / "_patterns_accumulator.yaml"
        self._patterns_accumulator: Dict[str, List[Dict]] = self._load_accumulator()

    def _load_accumulator(self) -> Dict[str, List[Dict]]:
        """加载跨天累积数据（有效期3天）"""
        if not self._patterns_accumulator_path.exists():
            return {}
        try:
            with open(self._patterns_accumulator_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            cutoff = datetime.now() - timedelta(days=3)
            valid = {
                scene: entries for scene, entries in data.items()
                if datetime.fromisoformat(entries[-1].get("_ts", "2000-01-01")) >= cutoff
            }
            return valid
        except Exception as e:
            logger.warning(f"加载累积数据失败: {e}")
            return {}

    def _save_accumulator(self):
        """保存跨天累积数据"""
        self._patterns_accumulator_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._patterns_accumulator_path, 'w', encoding='utf-8') as f:
            yaml.dump(self._patterns_accumulator, f, allow_unicode=True, default_flow_style=False)
    
    def execute_daily_learning(self) -> DailyLearningReport:
        """
        执行完整的每日学习流程
        
        Returns:
            DailyLearningReport: 学习报告
        """
        start_time = datetime.now()
        logger.info(f"[{start_time.strftime('%H:%M:%S')}] 开始每日学习流程...")
        
        # init新增组件
        self._init_闭环_components()

        # 1. 数据扫描
        logger.info("\n[1/8] 扫描新数据...")
        findings, validations, errors = self._scan_new_data()
        
        # 2. 实例学习
        logger.info("\n[2/8] 执行实例学习...")
        self._execute_instance_learning(findings)
        
        # 3. 验证学习
        logger.info("\n[3/8] 执行验证学习...")
        self._execute_validation_learning(validations)
        
        # 4. 错误学习
        logger.error("\n[4/8] 执行错误学习...")
        self._execute_error_learning(errors)
        
        # 5. 关联学习
        logger.info("\n[5/8] 执行关联学习...")
        self._execute_association_learning(findings)
        
        # ⭐ 6. 反馈整合(强化学习闭环)
        logger.info("\n[6/8] 执行反馈整合与强化学习...")
        self._execute_feedback_integration()
        
        # ⭐ 7. 迁移学习
        logger.info("\n[7/8] 执行迁移学习...")
        self._execute_transfer_learning()
        
        # 8. generate报告
        logger.info("\n[8/8] generate学习报告...")
        report = self._generate_report(
            start_time=start_time,
            findings_count=len(findings),
            validations_count=len(validations),
            errors_count=len(errors)
        )
        
        # 保存报告
        self._save_report(report)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"\n✅ 每日学习完成!耗时: {duration:.2f}秒")
        logger.info(f"📄 报告已保存: {self.reports_path / f'{report.report_id}.yaml'}")
        
        return report
    
    def _scan_new_data(self) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        扫描数据:网络学习优先,本地补充
        
        strategy:
        1. 首先执行网络研究(edGA),get最新领域知识
        2. 同时扫描本地新数据作为补充
        3. 合并两个来源,网络数据标记 source=network
        
        Returns:
            (新发现列表, 新验证结果列表, 错误案例列表)
        """
        findings = []
        validations = []
        errors = []

        # ── 1. 网络学习(edGA)始终执行 ──────────────────────────
        logger.info("  🌐 执行edGA网络研究学习...")
        net_findings = self._run_network_learning()
        if net_findings:
            findings.extend(net_findings)
            logger.info(f"  ✅ 网络学习get {len(net_findings)} 条新研究发现")
        else:
            logger.info("  ℹ️ 网络学习本次无新发现(已是最新)")

        # ── 2. 本地数据扫描(补充) ───────────────────────────────
        findings_path = self.base_path / "findings"
        local_count = 0
        if findings_path.exists():
            for file_path in findings_path.glob("*.yaml"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data and self._is_recent(data) and data.get("source") != "network":
                            data["source"] = "local"
                            findings.append(data)
                            local_count += 1
                except Exception as e:
                    logger.error(f"  ⚠️ 读取文件失败 {file_path}: {e}")
        if local_count:
            logger.info(f"  📁 本地补充 {local_count} 条研究发现")

        # ── 3. 验证结果扫描 ───────────────────────────────────────
        validation_path = self.base_path / "validation"
        if validation_path.exists():
            for file_path in validation_path.glob("*.yaml"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data and self._is_recent(data):
                            validations.append(data)
                            if not data.get("验证通过", True):
                                errors.append({
                                    "假设": data.get("假设内容", ""),
                                    "实际结果": "验证失败",
                                    "错误原因": data.get("失败原因", "未明确原因"),
                                    "验证ID": data.get("验证ID", ""),
                                    "时间": data.get("验证时间", "")
                                })
                except Exception as e:
                    logger.error(f"  ⚠️ 读取验证文件失败 {file_path}: {e}")

        # ── 4. 错误案例扫描 ───────────────────────────────────────
        learning_path = self.base_path / "learning"
        if learning_path.exists():
            for file_path in learning_path.glob("LE_*.yaml"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data and self._is_recent(data):
                            if data.get("学习类型") == "错误学习":
                                errors.append(data.get("输入数据", {}))
                except (yaml.YAMLError, IOError, KeyError):
                    pass

        logger.info(f"  📊 合计 {len(findings)} 条研究发现(网络+本地)")
        logger.error(f"  📊 {len(validations)} 条验证结果 | {len(errors)} 个错误案例")

        return findings, validations, errors

    def _run_network_learning(self) -> List[Dict]:
        """
        调度浏览器网络学习.
        
        - 若今日已有网络数据(NET_BROWSER_*)→ 直接加载,不重复抓取(幂等)
        - 否则 → 调用 _fetch_network_research() 启动浏览器学习
        
        Returns:
            网络学习发现列表(已写入磁盘)
        """
        today_str = datetime.now().strftime('%Y%m%d')
        findings_dir = self.base_path / "findings"
        findings_dir.mkdir(parents=True, exist_ok=True)

        # 幂等检查:今日已有浏览器网络数据
        today_files = list(findings_dir.glob(f"NET_BROWSER_*{today_str}*.yaml"))
        if today_files:
            result = []
            for fp in today_files:
                try:
                    with open(fp, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if data:
                            data["source"] = "network"
                            result.append(data)
                except (yaml.YAMLError, IOError):
                    pass
            logger.warning(f"    📂 今日浏览器网络数据已存在,加载 {len(result)} 条(跳过重复抓取)")
            return result

        # 首次执行:启动浏览器抓取
        return self._fetch_network_research(today_str)

    def _fetch_network_research(self, date_str: str) -> List[Dict]:
        """
        使用真实浏览器(Playwright)从网络抓取最新研究发现.
        
        支持 chromium / firefox / webkit 三种引擎.
        首选 chromium,若失败自动降级.
        
        抓取目标:
          - 知乎 AI/记忆/智能办公搜索结果
          - 搜狗微信公众号文章
          - 掘金技术文章
          - InfoQ 智能办公文章
        
        降级strategy:
          若浏览器全部不可用 → 返回空列表,由调用方处理
        """
        try:
            from src.neural_memory.browser_learning import BrowserNetworkLearner
        except ImportError:
            try:
                # 允许直接运行时的相对导入
                from .browser_learning import BrowserNetworkLearner
            except ImportError:
                logger.warning("    ⚠️ browser_learning 模块未找到,跳过浏览器学习")
                return []

        findings_dir = self.base_path / "findings"
        learner = BrowserNetworkLearner(findings_dir=findings_dir, browser_type="auto")
        results = learner.run()
        logger.info(f"    🌐 浏览器网络学习完成,get {len(results)} 条研究发现")
        return results
    
    def _is_recent(self, data: Dict) -> bool:
        """检查数据是否在时间窗口内"""
        # 尝试多种时间字段
        time_fields = ["创建时间", "验证时间", "时间", "created_at", "timestamp"]
        for field in time_fields:
            if field in data:
                try:
                    data_time = datetime.fromisoformat(str(data[field]).replace('Z', '+00:00'))
                    return data_time >= self.cutoff_time
                except Exception as e:
                    logger.debug(f"时间字段解析跳过: {e}")
                    continue
        # 如果没有时间字段,默认包含(可能是新文件)
        return True
    
    def _execute_instance_learning(self, findings: List[Dict]):
        """执行实例学习:从发现中提取模式（含跨天累积）"""
        # ── 1. 跨天累积当前发现 ──────────────────────────────
        for f in findings:
            raw_scenario = f.get("应用场景", "通用")
            if isinstance(raw_scenario, list):
                scenario = raw_scenario[0] if raw_scenario else "通用"
            else:
                scenario = str(raw_scenario) if raw_scenario else "通用"
            if scenario not in self._patterns_accumulator:
                self._patterns_accumulator[scenario] = []
            entry = dict(f)
            entry["_ts"] = datetime.now().isoformat()
            # 去重（按发现ID）
            existing_ids = {e.get("发现ID", "") for e in self._patterns_accumulator[scenario]}
            if entry.get("发现ID", "") not in existing_ids:
                self._patterns_accumulator[scenario].append(entry)
        self._save_accumulator()

        # ── 2. 用累积数据执行实例学习 ─────────────────────────
        total_accumulated = sum(len(v) for v in self._patterns_accumulator.values())
        logger.info(f"  📦 累积发现总数: {total_accumulated} 条 (跨 {len(self._patterns_accumulator)} 个场景)")

        if total_accumulated < 2:
            logger.warning(f"  ℹ️ 累积发现不足,跳过实例学习(需要≥2)")
            return
        
        # 按场景分组（使用累积器数据）
        findings_by_scenario = {}
        for scenario, accumulated in self._patterns_accumulator.items():
            if len(accumulated) >= 2:
                findings_by_scenario[scenario] = accumulated

        # 对每个场景执行实例学习
        for scenario, scenario_findings in findings_by_scenario.items():
                instances = [
                    {
                        "characteristics": f.get("发现标题", ""),
                        "场景": scenario,
                        "置信度": f.get("置信度评估", {}).get("置信度评分", 50) / 100
                    }
                    for f in scenario_findings
                ]
                
                pattern, event = self.learning_engine.learn_from_instance(
                    instances, 
                    f"{scenario}场景模式"
                )
                
                if event:
                    self.learning_events.append(event)
                    self.learning_engine.save_learning_event(event)
                    self.new_patterns.append({
                        "模式ID": pattern.get("模式ID", ""),
                        "场景": scenario,
                        "强度": pattern.get("模式强度", 0),
                        "支持实例": len(scenario_findings)
                    })
                    logger.info(f"  ✅ 从'{scenario}'场景提取模式: {pattern.get('模式ID', '')}")
    
    def _execute_validation_learning(self, validations: List[Dict]):
        """执行验证学习:基于验证结果更新置信度"""
        for validation in validations:
            hypothesis_id = validation.get("假设ID", "")
            if not hypothesis_id:
                continue
            
            validation_result = {
                "passed": validation.get("验证通过", False),
                "sample_size": validation.get("样本量", 0),
                "effect_size": validation.get("效应量", 0),
                "p_value": validation.get("p值", 1.0),
                "original_confidence": validation.get("原始置信度", 0.5)
            }
            
            event = self.learning_engine.learn_from_validation(
                hypothesis_id,
                validation_result
            )
            
            self.learning_events.append(event)
            self.learning_engine.save_learning_event(event)
            
            confidence_change = event.learning_result.get("置信度变化", 0)
            self.confidence_updates.append({
                "假设ID": hypothesis_id,
                "验证结果": "通过" if validation_result["passed"] else "失败",
                "置信度变化": f"{confidence_change:+.2f}",
                "新置信度": f"{event.learning_result.get('后验置信度', 0):.2f}"
            })
            
            status = "✅" if validation_result["passed"] else "❌"
            logger.info(f"  {status} 假设 {hypothesis_id}: 置信度变化 {confidence_change:+.2f}")
    
    def _execute_error_learning(self, errors: List[Dict]):
        """执行错误学习:从失败中recognize错误假设"""
        for error in errors:
            event = self.learning_engine.learn_from_error(error)
            
            self.learning_events.append(event)
            self.learning_engine.save_learning_event(event)
            
            error_type = event.learning_result.get("错误类型", "未知")
            logger.error(f"  ⚠️ recognize错误类型: {error_type}")
            logger.info(f"     改进建议: {event.learning_result.get('改进建议', '无')}")
    
    def _execute_association_learning(self, findings: List[Dict]):
        """执行关联学习:基于edGA语义概念提取发现概念关联"""
        # edGA语义概念mapping(与网络学习数据对齐)
        concept_keyword_map = {
            "记忆系统":   ["记忆", "Memory", "记忆库", "记忆增强", "长期记忆"],
            "AI智能体":   ["Agent", "智能体", "自主学习", "元认知"],
            "检索系统":   ["RAG", "检索", "HNSW", "向量检索"],
            "模块化架构": ["模块化", "分层", "架构", "框架"],
            "多Agent协作":["多Agent", "协作", "共享记忆", "一致性"],
            "系统安全":   ["安全", "治理", "隐私", "权限"],
            "智能办公":   ["办公", "助手", "企业应用", "知识管理"],
            "向量检索":   ["向量", "HNSW", "向量空间", "量化"],
            "市场规模":   ["市场", "规模", "增长率", "亿元", "亿美元"],
            "系统进化":   ["进化", "演化", "演进", "自适应"],
        }

        # 统计每条发现命中的概念
        concept_hits: Dict[str, List[Dict]] = {c: [] for c in concept_keyword_map}
        for f in findings:
            content = " ".join([
                str(f.get("发现标题", "")),
                str(f.get("核心洞察", "")),
                str(f.get("应用领域", "")),
                " ".join(f.get("关键词", []) if isinstance(f.get("关键词"), list) else [])
            ])
            for concept, keywords in concept_keyword_map.items():
                if any(kw in content for kw in keywords):
                    concept_hits[concept].append(f)

        # 只保留有命中的概念
        active_concepts = [c for c, hits in concept_hits.items() if hits]
        logger.info(f"  🧠 recognize到活跃概念: {active_concepts}")

        # edGA关联对:预定义高价值关联方向
        edga_concept_pairs = [
            ("记忆系统",   "AI智能体",    0.90, "正相关"),
            ("记忆系统",   "模块化架构",  0.88, "正相关"),
            ("AI智能体",   "多Agent协作", 0.85, "正相关"),
            ("检索系统",   "记忆系统",    0.82, "正相关"),
            ("向量检索",   "检索系统",    0.80, "正相关"),
            ("智能办公",   "AI智能体",    0.78, "正相关"),
            ("智能办公",   "市场规模",    0.72, "弱正相关"),
            ("AI智能体",   "系统安全",    0.70, "正相关"),
            ("系统进化",   "AI智能体",    0.68, "正相关"),
            ("记忆系统",   "向量检索",    0.75, "正相关"),
        ]

        for ca, cb, base_strength, rel_type in edga_concept_pairs:
            if ca not in active_concepts or cb not in active_concepts:
                continue

            # 构建共现证据
            evidence = []
            all_hits = concept_hits[ca] + concept_hits[cb]
            seen_ids = set()
            for f in all_hits:
                fid = f.get("发现ID", f.get("发现标题", ""))
                if fid in seen_ids:
                    continue
                seen_ids.add(fid)
                content = str(f.get("发现标题", "")) + str(f.get("核心洞察", ""))
                ca_hit = any(kw in content for kw in concept_keyword_map[ca])
                cb_hit = any(kw in content for kw in concept_keyword_map[cb])
                if ca_hit or cb_hit:
                    evidence.append({
                        "co_occurred": ca_hit and cb_hit,
                        "correlation": base_strength if (ca_hit and cb_hit) else base_strength * 0.6,
                        "source": f.get("发现ID", ""),
                    })

            if len(evidence) < 1:
                continue

            event = self.learning_engine.learn_from_association(ca, cb, evidence)

            if event.knowledge_updates:
                self.learning_events.append(event)
                self.learning_engine.save_learning_event(event)
                assoc_strength = event.learning_result.get("关联强度", base_strength)
                self.new_associations.append({
                    "概念A": ca,
                    "概念B": cb,
                    "关联类型": rel_type,
                    "关联强度": assoc_strength
                })
                logger.info(f"  🔗 edGA关联: {ca} ↔ {cb} [{rel_type} | 强度{assoc_strength:.3f}]")
                
                # 保存到知识库
                try:
                    # 确保概念存在
                    for concept in [ca, cb]:
                        try:
                            self.neural_system.knowledge.add_concept("价值概念", {
                                "概念名": concept,
                                "来源": "edGA关联学习",
                                "定义": f"从网络学习中发现的核心概念"
                            })
                        except Exception as e:
                            logger.debug(f"概念 '{concept}' 添加失败(可能已存在): {e}")
                    
                    # 添加关联关系
                    relation_type = "相关关系" if "相关" in rel_type else "因果关系"
                    self.neural_system.knowledge.add_relation(relation_type, {
                        "源概念": ca,
                        "目标概念": cb,
                        "关系类型": rel_type,
                        "强度": assoc_strength,
                        "来源": "edGA网络学习",
                        "证据数": len(evidence)
                    })
                    logger.info(f"     💾 已保存到知识库")
                except Exception as e:
                    logger.error(f"     ⚠️ 保存到知识库失败: {e}")

    # ==================== ⭐ 新增:闭环组件init ====================
    
    def _init_闭环_components(self):
        """延迟init闭环组件(避免循环导入)"""
        if self._闭环_components_initialized:
            return
        try:
            from .feedback_pipeline import FeedbackPipeline
            from .roi_tracker import ROITracker
            from .reinforcement_trigger import ReinforcementTrigger
            from .transfer_learner import TransferLearner
            
            self._feedback_pipeline = FeedbackPipeline(str(self.base_path / "learning"))
            self._roi_tracker = ROITracker(str(self.base_path))
            self._rl_trigger = ReinforcementTrigger(str(self.base_path))
            self._transfer_learner = TransferLearner(str(self.base_path))
            self._闭环_components_initialized = True
            logger.info("  ✅ 闭环组件加载成功(反馈管道/ROI追踪/强化学习/迁移学习)")
        except Exception as e:
            logger.error(f"  ⚠️ 闭环组件加载失败: {e},强化学习/迁移学习跳过")
            self._闭环_components_initialized = True  # 避免重复尝试

    # ==================== ⭐ 新增:反馈整合(强化学习闭环) ====================
    
    def _execute_feedback_integration(self):
        """执行反馈整合:同步反馈到ROI追踪器,触发Q-learning更新"""
        if not self._闭环_components_initialized:
            self._init_闭环_components()
        if self._feedback_pipeline is None or self._roi_tracker is None:
            logger.warning("  ℹ️ 反馈组件不可用,跳过")
            return
        
        # 1. 同步待处理反馈到ROI追踪器
        try:
            sync_stats = self._feedback_pipeline.sync_to_roi_tracker()
            if sync_stats["synced"] > 0:
                logger.info(f"  ✅ 同步 {sync_stats['synced']} 条反馈到ROI追踪器")
        except Exception as e:
            logger.error(f"  ⚠️ 反馈同步失败: {e}")
        
        # 2. 触发Q-learning更新(批量模式)
        try:
            if self._rl_trigger.should_trigger():
                updates = self._rl_trigger.trigger_update(force=False)
                for u in updates:
                    logger.info(f"  🧠 RL更新: {u.action} Q值 {u.q_value_before:.3f} → {u.q_value_after:.3f}")
            else:
                # 推送当前ROI数据作为被动反馈
                period_roi = self._roi_tracker.get_period_roi()
                for rec in self._roi_tracker._records[-5:]:
                    if rec.strategy_used:
                        self._rl_trigger.push_roi_feedback(rec.strategy_used, rec.output_metrics)
                logger.info(f"  📊 ROI追踪器当前记录: {len(self._roi_tracker._records)} 条")
        except Exception as e:
            logger.error(f"  ⚠️ 强化学习触发失败: {e}")
    
    # ==================== ⭐ 新增:迁移学习 ====================
    
    def _execute_transfer_learning(self):
        """执行迁移学习:将验证通过的高置信度知识注册,并寻找新场景"""
        if not self._闭环_components_initialized:
            self._init_闭环_components()
        if self._transfer_learner is None:
            logger.warning("  ℹ️ 迁移学习组件不可用,跳过")
            return
        
        new_hypotheses = []
        new_knowledge = []
        
        # 1. 从近期验证通过的假设中注册高质量知识
        try:
            for record in self._roi_tracker._records[-20:]:
                quality = record.output_metrics.get("quality_score", 0.5)
                adopted = record.output_metrics.get("adopted", 0)
                combined = quality * 0.6 + adopted * 0.4
                
                if combined >= 0.65 and record.strategy_used:
                    k_id = self._transfer_learner.register_knowledge(
                        concept=record.strategy_used,
                        domain="通用",
                        confidence=combined,
                        source_scenario=record.task_type,
                    )
                    if k_id:
                        new_knowledge.append({
                            "知识ID": k_id,
                            "概念": record.strategy_used,
                            "置信度": combined,
                            "场景": record.task_type,
                        })
        except Exception as e:
            logger.error(f"  ⚠️ 知识注册失败: {e}")
        
        # 2. 扫描场景,generate迁移假设
        try:
            # 注册已知场景
            for record in self._roi_tracker._records[-10:]:
                if not record.task_type:
                    continue
                from .transfer_learner import ScenarioProfile
                scene = ScenarioProfile(
                    scenario_id=f"SCENE_{record.task_type}",
                    name=record.task_type,
                    industry="通用",
                    keywords=[record.task_type],
                    features={},
                )
                self._transfer_learner.register_scenario(scene)
            
            # 查找可迁移知识
            for scene_id, scene in list(self._transfer_learner._scenarios.items())[:5]:
                candidates = self._transfer_learner.find_transferable_knowledge(scene, top_k=3)
                for knowledge, sim in candidates:
                    h = self._transfer_learner.create_transfer_hypothesis(knowledge, scene)
                    if h:
                        new_hypotheses.append({
                            "假设ID": h.hypothesis_id,
                            "源知识": knowledge.concept,
                            "目标场景": scene.name,
                            "迁移置信度": round(h.transfer_confidence, 3),
                            "状态": h.status,
                        })
        except Exception as e:
            logger.error(f"  ⚠️ 迁移假设generate失败: {e}")
        
        if new_knowledge:
            for k in new_knowledge:
                logger.info(f"  📚 注册知识: {k['概念']} (置信度={k['置信度']:.2f})")
        if new_hypotheses:
            for h in new_hypotheses[:3]:
                logger.info(f"  🔀 迁移假设: {h['源知识']} → {h['目标场景']} (置信度={h['迁移置信度']:.2f})")
        
        # 保存到实例,供报告使用
        self._new_hypotheses = new_hypotheses
        self._new_knowledge = new_knowledge
        if self._transfer_learner:
            self._transfer_report = self._transfer_learner.get_transfer_report()
        else:
            self._transfer_report = {}
    
    def _generate_report(self, start_time: datetime, 
                         findings_count: int,
                         validations_count: int,
                         errors_count: int) -> DailyLearningReport:
        """generate学习报告"""
        
        # 分类学习事件
        instance_events = [e for e in self.learning_events if e.event_type == LearningType.INSTANCE]
        validation_events = [e for e in self.learning_events if e.event_type == LearningType.VALIDATION]
        error_events = [e for e in self.learning_events if e.event_type == LearningType.ERROR]
        association_events = [e for e in self.learning_events if e.event_type == LearningType.ASSOCIATION]
        
        # get系统统计
        system_report = self.neural_system.generate_system_report()
        
        # generate总结(区分网络/本地来源)
        net_count = sum(1 for _ in range(findings_count))  # findings_count已是合并后总数
        if findings_count > 0:
            summary = f"今日网络+本地合计get {findings_count} 条研究发现(edGA网络学习优先)."
            if self.new_patterns:
                summary += f"提取 {len(self.new_patterns)} 个新模式."
            if self.confidence_updates:
                summary += f"更新 {len(self.confidence_updates)} 条置信度."
            if self.new_associations:
                summary += f"发现 {len(self.new_associations)} 个新概念关联."
            # ⭐ 闭环新增
            if hasattr(self, '_new_hypotheses') and self._new_hypotheses:
                summary += f"generate {len(self._new_hypotheses)} 个迁移假设."
            if hasattr(self, '_new_knowledge') and self._new_knowledge:
                summary += f"注册 {len(self._new_knowledge)} 条高置信度知识."
        elif self.learning_events:
            summary = f"今日学习活跃,产生 {len(self.learning_events)} 个学习事件."
            if self.new_patterns:
                summary += f"发现 {len(self.new_patterns)} 个新模式."
            if self.confidence_updates:
                summary += f"更新 {len(self.confidence_updates)} 条置信度."
        else:
            summary = "今日网络研究与本地数据均无新发现,系统保持现有知识状态."
        
        # generate建议
        recommendations = []
        if findings_count > 0 and findings_count < 5:
            recommendations.append(f"新发现数量({findings_count})接近实例学习阈值,建议继续积累数据")
        if errors_count > 3:
            recommendations.append(f"错误案例较多({errors_count}),建议审查验证流程")
        if not self.new_patterns and findings_count >= 5:
            recommendations.append("数据量充足但未提取到模式,建议检查数据质量")
        
        report = DailyLearningReport(
            report_id=f"DLR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            date=datetime.now().strftime('%Y-%m-%d'),
            execution_time=datetime.now().strftime('%H:%M:%S'),
            new_findings_count=findings_count,
            new_validations_count=validations_count,
            error_cases_count=errors_count,
            instance_learning_events=[{
                "事件ID": e.event_id,
                "触发": e.trigger,
                "置信度变化": e.confidence_change
            } for e in instance_events],
            validation_learning_events=[{
                "事件ID": e.event_id,
                "触发": e.trigger,
                "置信度变化": e.confidence_change
            } for e in validation_events],
            error_learning_events=[{
                "事件ID": e.event_id,
                "触发": e.trigger,
                "置信度变化": e.confidence_change
            } for e in error_events],
            association_learning_events=[{
                "事件ID": e.event_id,
                "触发": e.trigger,
                "置信度变化": e.confidence_change
            } for e in association_events],
            new_patterns=self.new_patterns,
            confidence_updates=self.confidence_updates,
            new_associations=self.new_associations,
            # ⭐ 强化学习
            rl_updates=getattr(self, '_rl_updates', []),
            q_table_snapshot=getattr(self, '_rl_trigger', None) and
                            hasattr(self._rl_trigger, 'get_q_values') and
                            self._rl_trigger.get_q_values() or {},
            # ⭐ 迁移学习
            transfer_hypotheses=getattr(self, '_new_hypotheses', []),
            registered_knowledge=getattr(self, '_new_knowledge', []),
            transfer_report=getattr(self, '_transfer_report', {}),
            system_health=system_report.get("系统健康度", {}),
            memory_stats=system_report.get("记忆系统", {}),
            knowledge_stats=system_report.get("知识系统", {}),
            summary=summary,
            recommendations=recommendations if recommendations else ["系统运行正常,继续保持数据录入"]
        )
        
        return report
    
    def _save_report(self, report: DailyLearningReport):
        """保存学习报告(YAML + JSON + HTML)"""
        # 转换为字典
        report_dict = asdict(report)
        
        # 保存为YAML
        report_file = self.reports_path / f"{report.report_id}.yaml"
        with open(report_file, 'w', encoding='utf-8') as f:
            yaml.dump(report_dict, f, allow_unicode=True, default_flow_style=False)
        
        # 同时保存为JSON(便于程序读取)
        json_file = self.reports_path / f"{report.report_id}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, ensure_ascii=False, indent=2)
        
        # 更新最新报告链接(复制而非symlink,兼容Windows)
        latest_link = self.reports_path / "latest.yaml"
        with open(report_file, 'r', encoding='utf-8') as src:
            with open(latest_link, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        
        # generateHTML可视化报告
        try:
            template = LearningReportTemplate(str(self.base_path))
            html_data = self._prepare_html_report_data(report)
            html_path = template.generate_html_report(html_data)
            logger.info(f"  📄 HTML报告已generate: {html_path.name}")
        except Exception as e:
            logger.error(f"  ⚠️ HTML报告generate失败: {e}")
    
    def _prepare_html_report_data(self, report: DailyLearningReport) -> Dict[str, Any]:
        """准备HTML报告所需的数据格式"""
        return {
            'date': report.date,
            'summary': {
                'total_events': len(report.instance_learning_events) + 
                               len(report.validation_learning_events) + 
                               len(report.error_learning_events) + 
                               len(report.association_learning_events),
                'instance_learning': len(report.instance_learning_events),
                'validation_learning': len(report.validation_learning_events),
                'error_learning': len(report.error_learning_events),
                'association_learning': len(report.association_learning_events),
                'knowledge_updates': len(report.new_patterns) + len(report.confidence_updates) + len(report.new_associations),
                'concept_growth': len(report.new_associations),
                'rule_growth': len(report.new_patterns),
                'relation_growth': len(report.new_associations),
                'pattern_growth': len(report.new_patterns)
            },
            'instance_events': [
                {
                    'pattern_name': p.get('模式ID', '新模式'),
                    'description': f"从{p.get('场景', '通用')}场景提取",
                    'confidence': '高' if p.get('强度', 0) > 0.7 else '中',
                    'scenario': p.get('场景', '通用')
                }
                for p in report.new_patterns
            ],
            'validation_events': [
                {
                    'hypothesis': c.get('假设ID', '假设'),
                    'old_confidence': 0.5,  # 默认值
                    'new_confidence': float(c.get('新置信度', '0.5')),
                    'method': '贝叶斯更新'
                }
                for c in report.confidence_updates
            ],
            'error_events': [
                {
                    'error_pattern': e.get('触发', '错误'),
                    'lesson': '从错误中学习改进',
                    'scope': '系统'
                }
                for e in report.error_learning_events
            ],
            'system_status': {
                'health_score': report.system_health.get('健康度评分', 0.8),
                'knowledge_base_size': f"{report.knowledge_stats.get('概念数量', 0)}概念",
                'memory_density': '0.72',
                'last_update': '刚刚'
            },
            'new_findings': report.new_findings_count,
            'patterns_extracted': len(report.new_patterns),
            'recommendations': report.recommendations
        }

def run_daily_learning():
    """运行每日学习的入口函数"""
    logger.info("=" * 60)
    logger.info("Somn 神经记忆系统 - 每日自动学习")
    logger.info("=" * 60)
    logger.info(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"扫描窗口: 最近24小时")
    logger.info("=" * 60)

    try:
        executor = DailyLearningExecutor()
        report = executor.execute_daily_learning()

        # 输出报告摘要
        logger.info("")
        logger.info("=" * 60)
        logger.info("学习报告摘要")
        logger.info("=" * 60)
        logger.info(f"报告ID: {report.report_id}")
        logger.info(f"新发现: {report.new_findings_count}")
        logger.info(f"新验证: {report.new_validations_count}")
        logger.info(f"错误案例: {report.error_cases_count}")
        logger.info("学习事件:")
        logger.info(f"  - 实例学习: {len(report.instance_learning_events)}")
        logger.info(f"  - 验证学习: {len(report.validation_learning_events)}")
        logger.info(f"  - 错误学习: {len(report.error_learning_events)}")
        logger.info(f"  - 关联学习: {len(report.association_learning_events)}")
        logger.info(f"  - 强化学习: {len(report.rl_updates)}")
        logger.info(f"  - 迁移学习: {len(report.transfer_hypotheses)} 假设 / {len(report.registered_knowledge)} 知识")
        logger.info("知识更新:")
        logger.info(f"  - 新模式: {len(report.new_patterns)}")
        logger.info(f"  - 置信度更新: {len(report.confidence_updates)}")
        logger.info(f"  - 新关联: {len(report.new_associations)}")
        logger.info(f"Q表状态: {len(report.q_table_snapshot)} 个strategy")
        logger.info(f"总结: {report.summary}")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.error(f"学习过程出错: {e}")
        import traceback
        traceback.print_exc()
        return 1

def run_daily_learning_v2(base_path: str = None):
    """
    新路由入口（推荐）：通过 UnifiedLearningOrchestrator 执行每日学习。
    保留 run_daily_learning() 原有接口不变。
    """
    try:
        from .unified_learning_orchestrator import UnifiedLearningOrchestrator
        from .learning_strategies import LearningStrategyType
        orchestrator = UnifiedLearningOrchestrator(base_path)
        report = orchestrator.execute_daily(strategy_types=[LearningStrategyType.DAILY])
        return report
    except Exception as e:
        logger.warning(f"v2路由失败，回退到原始执行器: {e}")
        return run_daily_learning()

# if __name__ == "__main__":
# #     raise RuntimeError("此入口已禁用 - 请使用 tests/ 目录")
