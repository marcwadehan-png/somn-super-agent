"""
__all__ = [
    'export_user_data',
    'generate_memory_report',
    'get_current_user',
    'get_keyword_meaning',
    'get_stats',
    'get_user_profile',
    'learn_from_input',
    'list_users',
    'process_input',
    'record_feedback',
    'register_user',
    'switch_user',
    'unregister_user',
]

多用户语义记忆引擎 v1.0 - 核心引擎类
Multi-User Semantic Memory Engine - Core Engine Class

核心功能:
1. 用户隔离存储 - 每个用户独立的语义记忆空间
2. 语义理解 - fusion用户个性化与全局模式
3. 高频学习 - 每个用户独立的高频词记忆
4. 反馈学习 - 用户级别的反馈记录与学习
5. 用户画像 - 统计每个用户的语义characteristics
"""

import yaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
from loguru import logger
import threading

from .semantic_types import (
    KeywordMapping, UserSemanticProfile, SemanticContext, UserFeedback,
)
from .semantic_engine_utils import (
    tokenize, extract_keywords, match_mappings,
    infer_intent, classify_intent_from_text,
    check_vague_expression, build_reasoning_chain,
)

class MultiUserSemanticEngine:
    """
    多用户语义记忆引擎 v1.0

    核心功能:
    1. 用户隔离存储 - 每个用户独立的语义记忆空间
    2. 语义理解 - fusion用户个性化与全局模式
    3. 高频学习 - 每个用户独立的高频词记忆
    4. 反馈学习 - 用户级别的反馈记录与学习
    5. 用户画像 - 统计每个用户的语义characteristics

    使用方式:
    ```python
    engine = MultiUserSemanticEngine()

    # 方式1: 自动用户上下文(需要外部传入 user_id)
    ctx = engine.process_input("帮我分析报表", user_id="alice")
    ctx = engine.process_input("看看数据", user_id="alice")  # alice 学会"报表=数据"

    ctx = engine.process_input("帮我分析报表", user_id="bob")
    ctx = engine.process_input("看看数据", user_id="bob")    # bob 有自己的记忆
    ```
    """

    # 全局意图模式(所有用户共享)
    INTENT_PATTERNS = {
        'request': {
            'keywords': ['帮我', '请', '要', '需要', '能否', '能不能', '可以帮我', '麻烦'],
            'description': '请求执行某项任务'
        },
        'query': {
            'keywords': ['怎么', '如何', '是什么', '为什么', '多少', '哪里', '查询', '查找', '问问'],
            'description': '询问信息或知识'
        },
        'analysis': {
            'keywords': ['分析', '研究', '论证', '探讨', '对比', '评估', '研究一下', '深入研究'],
            'description': '需要深入分析或研究'
        },
        'creation': {
            'keywords': ['写', '创建', 'generate', '制作', '编写', '做一个', 'generate一个'],
            'description': '需要创建或generate内容'
        },
        'feedback': {
            'keywords': ['反馈', '意见', '建议', '觉得', '认为', '评价一下'],
            'description': '提供反馈或意见'
        },
        'modification': {
            'keywords': ['改', '修改', '调整', '优化', '完善', '升级', '改动'],
            'description': '修改或调整现有内容'
        },
        'explanation': {
            'keywords': ['解释', '说明', '讲讲', '介绍一下', '科普', '是什么东西'],
            'description': '需要解释或说明'
        },
        'chat': {
            'keywords': ['聊聊', '聊聊看', '随便说说', '随便聊聊'],
            'description': '闲聊'
        }
    }

    # 全局模糊词mapping(通用表达,所有用户共享)
    SYSTEM_VAGUE_MAPPINGS = {
        '这个': '指代当前上下文中的某个具体对象',
        '那个': '指代之前提到的某个对象',
        '这样': '按照刚才说明的方式',
        '那样': '按照之前描述的方式',
        '类似的': '与当前话题相关但有所不同的相似情况',
        '那件事': '需要根据上下文确定具体指代',
        '刚才': '最近发生的,与当前任务相关的事件',
        '上次': '上一次发生的相关事件',
        '这个/那个': '需要明确指代的对象'
    }

    # 默认系统用户ID
    SYSTEM_USER = "_system_"
    DEFAULT_USER = "default"

    def __init__(self, base_path: str = None):
        """
        init多用户语义记忆引擎 [v10.1 P1-6优化]

        所有I/O操作均在独立线程中执行，并带有10s总超时保护，
        避免在数据量大时初始化阻塞主线程。

        Args:
            base_path: 存储基础路径
        """
        import time as _time
        from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

        if base_path:
            self.base_path = Path(base_path)
        else:
            from src.core.paths import LEARNING_DIR
            self.base_path = Path(LEARNING_DIR) / "semantic_memory"

        self.base_path.mkdir(parents=True, exist_ok=True)

        # 目录结构
        self.shared_path = self.base_path / "_shared"
        self.analytics_path = self.base_path / "_analytics"
        self.shared_path.mkdir(exist_ok=True)
        self.analytics_path.mkdir(exist_ok=True)

        # 线程锁
        self.lock = threading.RLock()

        # 当前活跃用户上下文
        self._current_user_id: Optional[str] = None

        # 用户缓存(按需加载)
        self._user_profiles: Dict[str, UserSemanticProfile] = {}
        self._user_mappings: Dict[str, Dict[str, KeywordMapping]] = defaultdict(dict)
        self._user_high_freq: Dict[str, Dict[str, int]] = defaultdict(dict)
        self._user_feedbacks: Dict[str, List[UserFeedback]] = defaultdict(list)

        # [v10.1 P1-6] I/O密集操作使用独立线程+超时保护
        _INIT_TIMEOUT = 10.0  # 初始化总超时10s

        def _io_init():
            self._load_shared_data()
            self._load_global_stats()
            self.register_user(self.DEFAULT_USER)

        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_io_init)
                future.result(timeout=_INIT_TIMEOUT)
        except FuturesTimeout:
            logger.warning(
                f"[SemanticMemoryEngine] 初始化超时({_INIT_TIMEOUT}s)，"
                f"以最小化状态继续运行（共享数据/统计/默认用户可能未加载）"
            )
        except Exception as e:
            logger.warning(f"[SemanticMemoryEngine] 初始化异常: {e}，以最小化状态继续")

        logger.info(f"多用户语义记忆引擎init | 用户数: {len(self._user_profiles)} | 共享模式: {len(self.INTENT_PATTERNS)}")

    # ==================== 用户管理 ====================

    def register_user(self, user_id: str) -> bool:
        """
        注册新用户

        Args:
            user_id: 用户唯一标识

        Returns:
            是否成功
        """
        if not user_id or user_id.startswith("_"):
            logger.warning(f"无效用户ID: {user_id}")
            return False

        if user_id in self._user_profiles:
            logger.debug(f"用户已存在: {user_id}")
            return True

        with self.lock:
            # 创建用户目录
            user_path = self.base_path / user_id
            user_path.mkdir(exist_ok=True)

            # init画像
            profile = UserSemanticProfile(user_id=user_id)
            self._user_profiles[user_id] = profile
            self._save_user_profile(user_id)

            # 更新全局统计
            self._update_global_stats("register", user_id)

            logger.info(f"新用户注册: {user_id}")
            return True

    def unregister_user(self, user_id: str, delete_data: bool = False) -> bool:
        """
        注销用户

        Args:
            user_id: 用户ID
            delete_data: 是否删除用户数据(GDPR合规)

        Returns:
            是否成功
        """
        if user_id == self.DEFAULT_USER or user_id == self.SYSTEM_USER:
            logger.warning(f"不能删除系统用户: {user_id}")
            return False

        if user_id not in self._user_profiles:
            return False

        with self.lock:
            # 清除缓存
            self._user_profiles.pop(user_id, None)
            self._user_mappings.pop(user_id, None)
            self._user_high_freq.pop(user_id, None)
            self._user_feedbacks.pop(user_id, None)

            # 删除数据
            if delete_data:
                user_path = self.base_path / user_id
                if user_path.exists():
                    shutil.rmtree(user_path)
                logger.info(f"用户数据已删除: {user_id}")
            else:
                # 仅标记为未激活
                self._update_global_stats("unregister", user_id)

            return True

    def switch_user(self, user_id: str) -> bool:
        """
        切换当前活跃用户

        Args:
            user_id: 用户ID

        Returns:
            是否成功
        """
        if user_id not in self._user_profiles:
            self.register_user(user_id)

        self._current_user_id = user_id

        # 更新最后活跃时间
        profile = self._user_profiles[user_id]
        profile.last_active = datetime.now().isoformat()
        self._save_user_profile(user_id)

        return True

    def get_current_user(self) -> Optional[str]:
        """get当前活跃用户ID"""
        return self._current_user_id

    def list_users(self) -> List[Dict[str, Any]]:
        """列出所有用户及其状态"""
        return [
            {
                "user_id": uid,
                "created_at": p.created_at,
                "last_active": p.last_active,
                "total_inputs": p.total_inputs,
                "dominant_intent": max(p.dominant_intents.items(), key=lambda x: x[1])[0] if p.dominant_intents else "unknown"
            }
            for uid, p in self._user_profiles.items()
            if not uid.startswith("_")
        ]

    def export_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        导出用户所有数据(GDPR合规)

        Returns:
            用户完整数据
        """
        if user_id not in self._user_profiles:
            return None

        self._ensure_user_loaded(user_id)

        return {
            "profile": self._user_profiles[user_id].to_dict(),
            "mappings": {kw: m.to_dict() for kw, m in self._user_mappings[user_id].items()},
            "high_frequency": self._user_high_freq[user_id],
            "feedbacks": [f.to_dict() for f in self._user_feedbacks[user_id]]
        }

    # ==================== 核心语义处理 ====================

    def process_input(self, text: str, user_id: str = None, session_context: str = "") -> SemanticContext:
        """
        处理用户输入(多用户版本)

        Args:
            text: 用户输入
            user_id: 用户ID(如果为None,使用当前活跃用户)
            session_context: 会话上下文

        Returns:
            语义理解结果
        """
        # 确定用户
        effective_user_id = user_id or self._current_user_id or self.DEFAULT_USER

        # 确保用户已注册
        if effective_user_id not in self._user_profiles:
            self.register_user(effective_user_id)

        # 加载用户数据
        self._ensure_user_loaded(effective_user_id)

        # 更新用户活跃时间
        self._user_profiles[effective_user_id].last_active = datetime.now().isoformat()
        self._user_profiles[effective_user_id].total_inputs += 1

        # 分词
        tokens = tokenize(text)

        # 提取关键词
        keywords = extract_keywords(tokens)

        # 匹配已知mapping(先查用户个性化,再查全局)
        matched = match_mappings(keywords, self._user_mappings, self._shared_mappings, effective_user_id)

        # 推断意图
        inferred_intent, confidence = infer_intent(text, keywords, matched, self.INTENT_PATTERNS)

        # 检测模糊表达
        needs_clarification, clarification_question = check_vague_expression(text)

        # 构建推理链
        reasoning_chain = build_reasoning_chain(text, keywords, inferred_intent, matched)

        # 构建上下文
        ctx = SemanticContext(
            user_id=effective_user_id,
            raw_input=text,
            tokens=tokens,
            keywords_extracted=keywords,
            inferred_intent=inferred_intent,
            intent_confidence=confidence,
            reasoning_chain=reasoning_chain,
            needs_clarification=needs_clarification,
            clarification_question=clarification_question,
            matched_mappings=matched,
            personalization_applied=bool(matched)
        )

        # 更新用户画像
        self._update_profile_stats(effective_user_id, inferred_intent, confidence, matched)

        return ctx

    def learn_from_input(self, text: str, inferred_meaning: str, user_id: str = None) -> bool:
        """
        从用户输入学习(多用户版本)

        Args:
            text: 用户原始输入
            inferred_meaning: 推断的语义
            user_id: 用户ID

        Returns:
            是否学习成功
        """
        effective_user_id = user_id or self._current_user_id or self.DEFAULT_USER

        if effective_user_id not in self._user_profiles:
            return False

        self._ensure_user_loaded(effective_user_id)

        # 分词
        tokens = tokenize(text)
        keywords = extract_keywords(tokens)

        learned = False

        for kw in keywords:
            if len(kw) < 2:
                continue

            # 更新高频词统计
            high_freq = self._user_high_freq[effective_user_id]
            high_freq[kw] = high_freq.get(kw, 0) + 1

            # 达到阈值则创建mapping
            if high_freq[kw] >= 3:
                if kw not in self._user_mappings[effective_user_id]:
                    # 检查全局mapping,避免重复
                    if kw in self._shared_mappings:
                        # 用户覆盖全局
                        pass

                    mapping = KeywordMapping(
                        keyword=kw,
                        semantic_meanings=[inferred_meaning],
                        primary_meaning=inferred_meaning,
                        frequency=high_freq[kw],
                        source="learning"
                    )
                    self._user_mappings[effective_user_id][kw] = mapping
                    learned = True

                    # 更新画像
                    self._user_profiles[effective_user_id].total_learnings += 1

        # 持久化
        if learned:
            self._save_user_high_freq(effective_user_id)
            self._save_user_mappings(effective_user_id)

        return learned

    def record_feedback(self,
                        user_input: str,
                        system_understanding: str,
                        user_correction: str = "",
                        is_correct: bool = True,
                        user_id: str = None) -> bool:
        """
        记录用户反馈(多用户版本)

        Args:
            user_input: 用户原始输入
            system_understanding: 系统理解
            user_correction: 用户corrective
            is_correct: 系统理解是否正确
            user_id: 用户ID

        Returns:
            是否记录成功
        """
        effective_user_id = user_id or self._current_user_id or self.DEFAULT_USER

        if effective_user_id not in self._user_profiles:
            return False

        self._ensure_user_loaded(effective_user_id)

        # 分词get关键词
        tokens = tokenize(user_input)
        keywords = extract_keywords(tokens)

        # 推断意图
        intent_before, _ = infer_intent(user_input, keywords, [], self.INTENT_PATTERNS)

        # 意图corrective
        intent_after = intent_before
        if not is_correct and user_correction:
            intent_after = classify_intent_from_text(user_correction, self.INTENT_PATTERNS)

        # 创建反馈记录
        feedback = UserFeedback(
            user_id=effective_user_id,
            input_text=user_input,
            system_understanding=system_understanding,
            user_correction=user_correction,
            is_correct=is_correct,
            intent_before=intent_before,
            intent_after=intent_after
        )
        self._user_feedbacks[effective_user_id].append(feedback)

        # 更新mapping
        if not is_correct and user_correction:
            for kw in keywords:
                if len(kw) < 2:
                    continue

                if kw in self._user_mappings[effective_user_id]:
                    mapping = self._user_mappings[effective_user_id][kw]
                    mapping.source = "feedback"
                    mapping.confidence = max(0.1, mapping.confidence - 0.2)

                    # 添加新语义
                    if user_correction not in mapping.semantic_meanings:
                        mapping.semantic_meanings.append(user_correction)
                    mapping.primary_meaning = user_correction

                    mapping.last_updated = datetime.now().isoformat()
                    mapping.verified = True
                else:
                    # 新建mapping
                    mapping = KeywordMapping(
                        keyword=kw,
                        semantic_meanings=[user_correction],
                        primary_meaning=user_correction,
                        frequency=1,
                        source="feedback",
                        confidence=0.7,
                        verified=True
                    )
                    self._user_mappings[effective_user_id][kw] = mapping

        # 更新用户理解准确率
        profile = self._user_profiles[effective_user_id]
        feedbacks = self._user_feedbacks[effective_user_id]
        correct_count = sum(1 for f in feedbacks if f.is_correct)
        profile.understanding_accuracy = correct_count / len(feedbacks) if feedbacks else 0.0

        # 持久化
        self._save_user_feedbacks(effective_user_id)
        self._save_user_mappings(effective_user_id)

        # 更新全局统计
        self._update_global_stats("feedback", effective_user_id)

        return True

    # ==================== 查询接口 ====================

    def get_keyword_meaning(self, keyword: str, user_id: str = None) -> Optional[str]:
        """get关键词语义(多用户版本)"""
        effective_user_id = user_id or self._current_user_id or self.DEFAULT_USER

        if effective_user_id not in self._user_profiles:
            return None

        self._ensure_user_loaded(effective_user_id)

        # 先查用户mapping
        if keyword in self._user_mappings[effective_user_id]:
            return self._user_mappings[effective_user_id][keyword].primary_meaning

        # 再查全局mapping
        if keyword in self._shared_mappings:
            return self._shared_mappings[keyword].primary_meaning

        return None

    def get_user_profile(self, user_id: str = None) -> Optional[UserSemanticProfile]:
        """get用户语义画像"""
        effective_user_id = user_id or self._current_user_id or self.DEFAULT_USER
        return self._user_profiles.get(effective_user_id)

    def get_stats(self, user_id: str = None) -> Dict[str, Any]:
        """get统计信息"""
        if user_id:
            self._ensure_user_loaded(user_id)
            profile = self._user_profiles.get(user_id)
            if not profile:
                return {"enabled": False}

            return {
                "enabled": True,
                "user_id": user_id,
                "total_inputs": profile.total_inputs,
                "total_learnings": profile.total_learnings,
                "total_clarifications": profile.total_clarifications,
                "mappings_count": len(self._user_mappings.get(user_id, {})),
                "high_freq_count": len(self._user_high_freq.get(user_id, {})),
                "feedbacks_count": len(self._user_feedbacks.get(user_id, [])),
                "dominant_intent": max(profile.dominant_intents.items(), key=lambda x: x[1])[0] if profile.dominant_intents else "unknown",
                "understanding_accuracy": round(profile.understanding_accuracy, 2)
            }
        else:
            # 全局统计
            return {
                "enabled": True,
                "total_users": len([u for u in self._user_profiles if not u.startswith("_")]),
                "total_inputs_all": sum(p.total_inputs for p in self._user_profiles.values()),
                "total_mappings": len(self._shared_mappings),
                "global_stats": self._global_stats
            }

    def generate_memory_report(self, user_id: str = None) -> str:
        """generate记忆报告"""
        if user_id:
            profile = self.get_user_profile(user_id)
            if not profile:
                return f"用户 {user_id} 不存在"

            lines = [
                f"=== 用户语义画像: {user_id} ===",
                f"创建时间: {profile.created_at}",
                f"最后活跃: {profile.last_active}",
                f"总输入数: {profile.total_inputs}",
                f"学习次数: {profile.total_learnings}",
                f"理解准确率: {profile.understanding_accuracy:.1%}",
                "",
                f"高频意图分布:",
            ]

            for intent, count in sorted(profile.dominant_intents.items(), key=lambda x: -x[1]):
                lines.append(f"  - {intent}: {count}次")

            lines.append("")
            lines.append(f"个性化mapping数: {len(self._user_mappings.get(user_id, {}))}")

            return "\n".join(lines)
        else:
            return self.get_stats()

    # ==================== 内部方法 ====================

    def _ensure_user_loaded(self, user_id: str):
        """确保用户数据已加载"""
        if user_id not in self._user_profiles:
            return

        if user_id not in self._user_mappings:
            self._load_user_data(user_id)

    def _load_user_data(self, user_id: str):
        """加载单个用户的数据"""
        user_path = self.base_path / user_id

        # 加载画像
        profile_file = user_path / "profile.yaml"
        if profile_file.exists():
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data:
                        self._user_profiles[user_id] = UserSemanticProfile.from_dict(data)
            except Exception as e:
                logger.warning(f"加载用户画像失败 {user_id}: {e}")

        # 加载mapping
        mapping_file = user_path / "mappings.yaml"
        if mapping_file.exists():
            try:
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'mappings' in data:
                        for kw, mdata in data['mappings'].items():
                            self._user_mappings[user_id][kw] = KeywordMapping.from_dict(mdata)
            except Exception as e:
                logger.warning(f"加载用户mapping失败 {user_id}: {e}")

        # 加载高频词
        high_freq_file = user_path / "high_freq.yaml"
        if high_freq_file.exists():
            try:
                with open(high_freq_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'high_frequency' in data:
                        self._user_high_freq[user_id] = data['high_frequency']
            except Exception as e:
                logger.warning(f"加载高频词失败 {user_id}: {e}")

        # 加载反馈
        feedback_file = user_path / "feedback.yaml"
        if feedback_file.exists():
            try:
                with open(feedback_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'feedbacks' in data:
                        for fb in data['feedbacks']:
                            self._user_feedbacks[user_id].append(UserFeedback.from_dict(fb))
            except Exception as e:
                logger.warning(f"加载反馈失败 {user_id}: {e}")

    def _save_user_profile(self, user_id: str):
        """保存用户画像"""
        profile = self._user_profiles.get(user_id)
        if not profile:
            return

        user_path = self.base_path / user_id
        user_path.mkdir(exist_ok=True)

        with open(user_path / "profile.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(profile.to_dict(), f, allow_unicode=True, default_flow_style=False)

    def _save_user_mappings(self, user_id: str):
        """保存用户mapping"""
        mappings = self._user_mappings.get(user_id, {})
        user_path = self.base_path / user_id
        user_path.mkdir(exist_ok=True)

        with open(user_path / "mappings.yaml", 'w', encoding='utf-8') as f:
            yaml.dump({
                '元数据': {
                    '更新时间': datetime.now().isoformat(),
                    'mapping数': len(mappings)
                },
                'mappings': {kw: m.to_dict() for kw, m in mappings.items()}
            }, f, allow_unicode=True, default_flow_style=False)

    def _save_user_high_freq(self, user_id: str):
        """保存用户高频词"""
        high_freq = self._user_high_freq.get(user_id, {})
        user_path = self.base_path / user_id
        user_path.mkdir(exist_ok=True)

        with open(user_path / "high_freq.yaml", 'w', encoding='utf-8') as f:
            yaml.dump({
                '元数据': {'更新时间': datetime.now().isoformat()},
                'high_frequency': high_freq
            }, f, allow_unicode=True, default_flow_style=False)

    def _save_user_feedbacks(self, user_id: str):
        """保存用户反馈"""
        feedbacks = self._user_feedbacks.get(user_id, [])
        user_path = self.base_path / user_id
        user_path.mkdir(exist_ok=True)

        with open(user_path / "feedback.yaml", 'w', encoding='utf-8') as f:
            yaml.dump({
                '元数据': {'更新时间': datetime.now().isoformat(), '反馈数': len(feedbacks)},
                'feedbacks': [fb.to_dict() for fb in feedbacks[-100:]]  # 只保留最近100条
            }, f, allow_unicode=True, default_flow_style=False)

    def _load_shared_data(self):
        """加载全局共享数据"""
        # 加载全局意图模式
        intent_file = self.shared_path / "intent_patterns.yaml"
        if intent_file.exists():
            try:
                with open(intent_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data:
                        self.INTENT_PATTERNS.update(data.get('custom_patterns', {}))
            except Exception as e:
                logger.warning(f"加载意图模式失败: {e}")

        # 加载全局模糊词mapping
        vague_file = self.shared_path / "system_vague_mappings.yaml"
        if vague_file.exists():
            try:
                with open(vague_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data:
                        self.SYSTEM_VAGUE_MAPPINGS.update(data)
            except Exception as e:
                logger.warning(f"加载模糊词mapping失败: {e}")

        # 加载全局mapping
        shared_mapping_file = self.shared_path / "shared_mappings.yaml"
        self._shared_mappings: Dict[str, KeywordMapping] = {}
        if shared_mapping_file.exists():
            try:
                with open(shared_mapping_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'mappings' in data:
                        for kw, mdata in data['mappings'].items():
                            self._shared_mappings[kw] = KeywordMapping.from_dict(mdata)
            except Exception as e:
                logger.warning(f"加载全局mapping失败: {e}")

    def _load_global_stats(self):
        """加载全局统计"""
        stats_file = self.analytics_path / "global_stats.yaml"
        self._global_stats = {
            'total_registrations': 0,
            'total_inputs': 0,
            'total_feedbacks': 0,
            'active_users': []
        }
        if stats_file.exists():
            try:
                with open(stats_file, 'r', encoding='utf-8') as f:
                    self._global_stats = yaml.safe_load(f) or self._global_stats
            except Exception as e:
                logger.warning(f"加载全局统计失败: {e}")

    def _update_global_stats(self, action: str, user_id: str):
        """更新全局统计"""
        self._global_stats['total_registrations'] = len(self._user_profiles)
        self._global_stats['total_inputs'] = sum(p.total_inputs for p in self._user_profiles.values())
        self._global_stats['active_users'] = [
            uid for uid in self._user_profiles
            if not uid.startswith("_") and
            (datetime.now() - datetime.fromisoformat(self._user_profiles[uid].last_active)).days < 7
        ]

        stats_file = self.analytics_path / "global_stats.yaml"
        with open(stats_file, 'w', encoding='utf-8') as f:
            yaml.dump(self._global_stats, f, allow_unicode=True, default_flow_style=False)

    def _update_profile_stats(self, user_id: str, intent: str, confidence: float, matched: List):
        """更新用户画像统计"""
        profile = self._user_profiles.get(user_id)
        if not profile:
            return

        # 更新意图分布
        profile.dominant_intents[intent] = profile.dominant_intents.get(intent, 0) + 1

        # 更新平均置信度
        inputs = profile.total_inputs
        current_avg = profile.avg_confidence
        profile.avg_confidence = (current_avg * (inputs - 1) + confidence) / inputs if inputs > 0 else confidence
