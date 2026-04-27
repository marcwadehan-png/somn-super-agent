"""
__all__ = [
    'execute',
    'get_description',
    'strategy_type',
]

每日学习策略 - Daily Learning Strategy
提取自 daily_learning.py 的差异化能力：
- 神经系统深度集成（NeuralMemorySystem + LearningEngine）
- 实例/验证/错误/关联 四类学习事件
- 强化学习闭环（FeedbackPipeline + ReinforcementTrigger）
- 迁移学习（TransferLearner）
- HTML 学习报告生成
"""

from __future__ import annotations

import logging

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .base_strategy import (
    BaseLearningStrategy,
    DataScanResult,
    LearningResult,
    LearningStrategyType,
)

logger = logging.getLogger(__name__)
class DailyLearningStrategy(BaseLearningStrategy):
    """
    每日学习策略。

    差异化能力（仅此策略独有）：
    1. 深度集成 NeuralMemorySystem（实例/验证/错误/关联学习）
    2. 强化学习闭环（FeedbackPipeline → ROITracker → ReinforcementTrigger）
    3. 迁移学习（TransferLearner 知识注册 + 迁移假设生成）
    4. HTML 学习报告（LearningReportTemplate）
    5. edGA 语义概念关联体系
    """

    # ── edGA 概念映射（仅本策略使用）──────────────────────────────────────────
    _CONCEPT_KEYWORD_MAP: Dict[str, List[str]] = {
        "记忆系统":   ["记忆", "Memory", "记忆库", "记忆增强", "长期记忆"],
        "AI智能体":   ["Agent", "智能体", "自主学习", "元认知"],
        "检索系统":   ["RAG", "检索", "HNSW", "向量检索"],
        "模块化架构": ["模块化", "分层", "架构", "框架"],
        "多Agent协作": ["多Agent", "协作", "共享记忆", "一致性"],
        "系统安全":   ["安全", "治理", "隐私", "权限"],
        "智能办公":   ["办公", "助手", "企业应用", "知识管理"],
        "向量检索":   ["向量", "HNSW", "向量空间", "量化"],
        "市场规模":   ["市场", "规模", "增长率", "亿元", "亿美元"],
        "系统进化":   ["进化", "演化", "演进", "自适应"],
    }

    _CONCEPT_PAIRS = [
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

    def __init__(self, base_path: str = None):
        super().__init__(base_path)
        self._閉環_initialized = False
        self._feedback_pipeline = None
        self._roi_tracker = None
        self._rl_trigger = None
        self._transfer_learner = None

    @property
    def strategy_type(self) -> LearningStrategyType:
        return LearningStrategyType.DAILY

    def get_description(self) -> str:
        return "每日完整学习策略：实例/验证/错误/关联学习 + 强化学习闭环 + 迁移学习 + HTML 报告"

    def execute(self, scan_result: DataScanResult, context: Dict[str, Any]) -> LearningResult:
        """
        执行每日学习策略。

        context 必须包含：
            neural_system: NeuralMemorySystem
            learning_engine: LearningEngine
        """
        import time
        t0 = time.time()

        neural_system = context.get("neural_system")
        learning_engine = context.get("learning_engine")
        if not neural_system or not learning_engine:
            result = LearningResult(success=False, strategy_type=self.strategy_type.value)
            result.error_messages.append("context 缺少 neural_system 或 learning_engine")
            return result

        result = LearningResult(strategy_type=self.strategy_type.value)

        # 1. 实例学习
        self._execute_instance_learning(scan_result.findings, learning_engine, result)

        # 2. 验证学习
        self._execute_validation_learning(scan_result.validations, learning_engine, result)

        # 3. 错误学习
        self._execute_error_learning(scan_result.errors, learning_engine, result)

        # 4. 关联学习（edGA）
        all_findings = scan_result.findings + scan_result.network_research
        self._execute_association_learning(all_findings, neural_system, learning_engine, result)

        # 5. 强化学习闭环
        self._execute_feedback_integration(result)

        # 6. 迁移学习
        self._execute_transfer_learning(result)

        result.duration_seconds = round(time.time() - t0, 2)
        result.phases_completed = [
            "实例学习", "验证学习", "错误学习", "关联学习",
            "反馈整合", "迁移学习",
        ]
        result.summary = self._build_summary(scan_result, result)
        return result

    # ─────────────────────────────────────────────────
    # 差异化：实例学习
    # ─────────────────────────────────────────────────

    def _execute_instance_learning(
        self,
        findings: List[Dict],
        learning_engine: Any,
        result: LearningResult,
    ):
        """从发现中按场景提取模式（≥5 条触发）"""
        if len(findings) < 5:
            logger.info(f"新发现数量({len(findings)})不足，跳过实例学习(需要≥5)")
            return

        findings_by_scenario: Dict[str, List[Dict]] = {}
        for f in findings:
            raw = f.get("应用场景", "通用")
            scenario = (raw[0] if isinstance(raw, list) and raw else
                        str(raw) if raw else "通用")
            findings_by_scenario.setdefault(scenario, []).append(f)

        for scenario, sf in findings_by_scenario.items():
            if len(sf) < 5:
                continue
            instances = [
                {
                    "characteristics": f.get("发现标题", ""),
                    "场景": scenario,
                    "置信度": f.get("置信度评估", {}).get("置信度评分", 50) / 100,
                }
                for f in sf
            ]
            pattern, event = learning_engine.learn_from_instance(instances, f"{scenario}场景模式")
            if event:
                result.learning_events.append({"event_id": event.event_id, "type": "instance"})
                learning_engine.save_learning_event(event)
                result.new_patterns.append({
                    "模式ID": pattern.get("模式ID", ""),
                    "场景": scenario,
                    "强度": pattern.get("模式强度", 0),
                    "支持实例": len(sf),
                })
                logger.info(f"从'{scenario}'场景提取模式: {pattern.get('模式ID', '')}")

    # ─────────────────────────────────────────────────
    # 差异化：验证学习
    # ─────────────────────────────────────────────────

    def _execute_validation_learning(
        self,
        validations: List[Dict],
        learning_engine: Any,
        result: LearningResult,
    ):
        """基于验证结果更新置信度（贝叶斯更新）"""
        for v in validations:
            hid = v.get("假设ID", "")
            if not hid:
                continue
            vr = {
                "passed": v.get("验证通过", False),
                "sample_size": v.get("样本量", 0),
                "effect_size": v.get("效应量", 0),
                "p_value": v.get("p值", 1.0),
                "original_confidence": v.get("原始置信度", 0.5),
            }
            event = learning_engine.learn_from_validation(hid, vr)
            result.learning_events.append({"event_id": event.event_id, "type": "validation"})
            learning_engine.save_learning_event(event)
            change = event.learning_result.get("置信度变化", 0)
            result.confidence_updates.append({
                "假设ID": hid,
                "验证结果": "通过" if vr["passed"] else "失败",
                "置信度变化": f"{change:+.2f}",
                "新置信度": f"{event.learning_result.get('后验置信度', 0):.2f}",
            })
            status = "✅" if vr["passed"] else "❌"
            logger.info(f"{status} 假设 {hid}: 置信度变化 {change:+.2f}")

    # ─────────────────────────────────────────────────
    # 差异化：错误学习
    # ─────────────────────────────────────────────────

    def _execute_error_learning(
        self,
        errors: List[Dict],
        learning_engine: Any,
        result: LearningResult,
    ):
        """从失败中识别错误假设"""
        for error in errors:
            event = learning_engine.learn_from_error(error)
            result.learning_events.append({"event_id": event.event_id, "type": "error"})
            learning_engine.save_learning_event(event)
            et = event.learning_result.get("错误类型", "未知")
            logger.warning(f"识别错误类型: {et}")
            logger.info(f"改进建议: {event.learning_result.get('改进建议', '无')}")

    # ─────────────────────────────────────────────────
    # 差异化：edGA 关联学习
    # ─────────────────────────────────────────────────

    def _execute_association_learning(
        self,
        findings: List[Dict],
        neural_system: Any,
        learning_engine: Any,
        result: LearningResult,
    ):
        """基于 edGA 语义概念提取关联"""
        concept_hits: Dict[str, List[Dict]] = {c: [] for c in self._CONCEPT_KEYWORD_MAP}
        for f in findings:
            content = " ".join([
                str(f.get("发现标题", "")),
                str(f.get("核心洞察", "")),
                str(f.get("应用领域", "")),
                " ".join(f.get("关键词", []) if isinstance(f.get("关键词"), list) else []),
            ])
            for concept, keywords in self._CONCEPT_KEYWORD_MAP.items():
                if any(kw in content for kw in keywords):
                    concept_hits[concept].append(f)

        active = [c for c, h in concept_hits.items() if h]
        if active:
            logger.info(f"识别到活跃概念: {active}")

        for ca, cb, base_str, rel_type in self._CONCEPT_PAIRS:
            if ca not in active or cb not in active:
                continue
            evidence = []
            seen = set()
            for f in concept_hits[ca] + concept_hits[cb]:
                fid = f.get("发现ID", f.get("发现标题", ""))
                if fid in seen:
                    continue
                seen.add(fid)
                content = str(f.get("发现标题", "")) + str(f.get("核心洞察", ""))
                ca_hit = any(kw in content for kw in self._CONCEPT_KEYWORD_MAP[ca])
                cb_hit = any(kw in content for kw in self._CONCEPT_KEYWORD_MAP[cb])
                if ca_hit or cb_hit:
                    evidence.append({
                        "co_occurred": ca_hit and cb_hit,
                        "correlation": base_str if (ca_hit and cb_hit) else base_str * 0.6,
                        "source": f.get("发现ID", ""),
                    })
            if not evidence:
                continue

            event = learning_engine.learn_from_association(ca, cb, evidence)
            if event.knowledge_updates:
                result.learning_events.append({"event_id": event.event_id, "type": "association"})
                learning_engine.save_learning_event(event)
                assoc_strength = event.learning_result.get("关联强度", base_str)
                result.new_associations.append({
                    "概念A": ca, "概念B": cb,
                    "关联类型": rel_type, "关联强度": assoc_strength,
                })
                logger.info(f"edGA关联: {ca} ↔ {cb} [{rel_type} | 强度{assoc_strength:.3f}]")
                # 写入知识库
                try:
                    for concept in [ca, cb]:
                        try:
                            neural_system.knowledge.add_concept("价值概念", {
                                "概念名": concept, "来源": "edGA关联学习",
                                "定义": "从网络学习中发现的核心概念",
                            })
                        except Exception as e:
                            logger.debug(f"每日策略保存失败: {e}")
                    rel = "相关关系" if "相关" in rel_type else "因果关系"
                    neural_system.knowledge.add_relation(rel, {
                        "源概念": ca, "目标概念": cb, "关系类型": rel_type,
                        "强度": assoc_strength, "来源": "edGA网络学习",
                        "证据数": len(evidence),
                    })
                    logger.debug("已保存到知识库")
                except Exception as e:
                    logger.warning(f"保存到知识库失败: {e}")

    # ─────────────────────────────────────────────────
    # 差异化：强化学习闭环
    # ─────────────────────────────────────────────────

    def _init_closed_loop(self):
        """延迟初始化闭环组件"""
        if self._閉環_initialized:
            return
        try:
            from ..feedback_pipeline import FeedbackPipeline
            from ..roi_tracker import ROITracker
            from ..reinforcement_trigger import ReinforcementTrigger
            from ..transfer_learner import TransferLearner

            bp = str(Path(self.base_path))
            self._feedback_pipeline = FeedbackPipeline(str(Path(bp) / "learning"))
            self._roi_tracker = ROITracker(bp)
            self._rl_trigger = ReinforcementTrigger(bp)
            self._transfer_learner = TransferLearner(bp)
            logger.info("闭环组件加载成功（反馈管道/ROI追踪/强化学习/迁移学习）")
        except Exception as e:
            logger.warning(f"闭环组件加载失败: {e}，强化学习/迁移学习跳过")
        self._閉環_initialized = True

    def _execute_feedback_integration(self, result: LearningResult):
        """同步反馈到 ROI 追踪器，触发 Q-learning 更新"""
        self._init_closed_loop()
        if not self._feedback_pipeline or not self._roi_tracker:
            logger.info("反馈组件不可用，跳过")
            return
        try:
            stats = self._feedback_pipeline.sync_to_roi_tracker()
            if stats.get("synced", 0) > 0:
                logger.info(f"同步 {stats['synced']} 条反馈到ROI追踪器")
        except Exception as e:
            logger.warning(f"反馈同步失败: {e}")
        try:
            if self._rl_trigger.should_trigger():
                updates = self._rl_trigger.trigger_update(force=False)
                for u in updates:
                    result.rl_updates.append({
                        "action": u.action,
                        "q_before": u.q_value_before,
                        "q_after": u.q_value_after,
                    })
                    logger.info(f"RL更新: {u.action} Q值 {u.q_value_before:.3f} → {u.q_value_after:.3f}")
            else:
                for rec in self._roi_tracker._records[-5:]:
                    if rec.strategy_used:
                        self._rl_trigger.push_roi_feedback(rec.strategy_used, rec.output_metrics)
                logger.info(f"ROI追踪器当前记录: {len(self._roi_tracker._records)} 条")
        except Exception as e:
            logger.warning(f"强化学习触发失败: {e}")

    # ─────────────────────────────────────────────────
    # 差异化：迁移学习
    # ─────────────────────────────────────────────────

    def _execute_transfer_learning(self, result: LearningResult):
        """将高置信度知识注册，寻找新迁移场景"""
        self._init_closed_loop()
        if not self._transfer_learner:
            logger.info("迁移学习组件不可用，跳过")
            return
        new_hypotheses: List[Dict] = []
        new_knowledge: List[Dict] = []

        try:
            for rec in self._roi_tracker._records[-20:]:
                quality = rec.output_metrics.get("quality_score", 0.5)
                adopted = rec.output_metrics.get("adopted", 0)
                combined = quality * 0.6 + adopted * 0.4
                if combined >= 0.65 and rec.strategy_used:
                    k_id = self._transfer_learner.register_knowledge(
                        concept=rec.strategy_used,
                        domain="通用",
                        confidence=combined,
                        source_scenario=rec.task_type,
                    )
                    if k_id:
                        new_knowledge.append({
                            "知识ID": k_id, "概念": rec.strategy_used,
                            "置信度": combined, "场景": rec.task_type,
                        })
        except Exception as e:
            logger.warning(f"知识注册失败: {e}")

        try:
            from ..transfer_learner import ScenarioProfile
            for rec in self._roi_tracker._records[-10:]:
                if not rec.task_type:
                    continue
                scene = ScenarioProfile(
                    scenario_id=f"SCENE_{rec.task_type}",
                    name=rec.task_type,
                    industry="通用",
                    keywords=[rec.task_type],
                    features={},
                )
                self._transfer_learner.register_scenario(scene)
            for scene_id, scene in list(self._transfer_learner._scenarios.items())[:5]:
                for knowledge, _ in self._transfer_learner.find_transferable_knowledge(scene, top_k=3):
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
            logger.warning(f"迁移假设生成失败: {e}")

        for k in new_knowledge:
            logger.info(f"注册知识: {k['概念']} (置信度={k['置信度']:.2f})")
        for h in new_hypotheses[:3]:
            logger.info(f"迁移假设: {h['源知识']} → {h['目标场景']} (置信度={h['迁移置信度']:.2f})")

        result.transfer_hypotheses.extend(new_hypotheses)
        result.registered_knowledge.extend(new_knowledge)

    # ─────────────────────────────────────────────────
    # 报告生成
    # ─────────────────────────────────────────────────

    @staticmethod
    def _build_summary(scan: DataScanResult, result: LearningResult) -> str:
        total = scan.total
        if total > 0:
            s = f"今日网络+本地合计获取 {total} 条研究发现(edGA网络学习优先)."
            if result.new_patterns:
                s += f"提取 {len(result.new_patterns)} 个新模式."
            if result.confidence_updates:
                s += f"更新 {len(result.confidence_updates)} 条置信度."
            if result.new_associations:
                s += f"发现 {len(result.new_associations)} 个新概念关联."
            if result.transfer_hypotheses:
                s += f"生成 {len(result.transfer_hypotheses)} 个迁移假设."
            if result.registered_knowledge:
                s += f"注册 {len(result.registered_knowledge)} 条高置信度知识."
        elif result.learning_events:
            s = f"今日学习活跃，产生 {len(result.learning_events)} 个学习事件."
        else:
            s = "今日网络研究与本地数据均无新发现，系统保持现有知识状态."
        return s
