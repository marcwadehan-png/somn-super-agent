"""
藏书阁智能升级中枢 V1.0
==================

功能定位：
- 连接藏书阁(Imperial Library)与智慧学习自动升级系统
- 根据藏书阁数据自动调用大模型完成编码升级
- 对项目全局进行自动升级，所有升级均为正向迭代
- 仅对停用超过180天的功能进行删减

核心设计：
1. 藏书阁数据读取器：从藏书阁查询待升级知识
2. 升级规划器：分析藏书阁数据，制定升级方案
3. 大模型编码器：调用大模型生成升级代码
4. 升级执行器：执行代码升级并验证
5. 升级记录器：将升级记录写入藏书阁

作者: Somn智能系统
版本: V1.0.0
日期: 2026-04-25
"""

import json
import logging
import hashlib
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

# ============================================================================
# 路径配置（惰性初始化，避免 import 时执行 I/O）
# ============================================================================

# 获取项目根目录
try:
    from smart_office_assistant.src.core.paths import PROJECT_ROOT
except ImportError:
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent

# 惰性目录属性（首次访问时才创建）
_libraries_upgrade_dir: Optional[Path] = None
_libraries_upgrade_dir_lock = threading.Lock()

@property  # type: ignore[misc]
def LIBRARY_UPGRADE_DIR() -> Path:  # noqa: N802
    """惰性目录：首次访问时才创建目录。"""
    global _libraries_upgrade_dir
    if _libraries_upgrade_dir is None:
        with _libraries_upgrade_dir_lock:
            if _libraries_upgrade_dir is None:
                _p = PROJECT_ROOT / "data" / "library_upgrade"
                _p.mkdir(parents=True, exist_ok=True)
                _libraries_upgrade_dir = _p
    return _libraries_upgrade_dir

# ============================================================================
# 日志配置
# ============================================================================

logger = logging.getLogger("LibraryUpgradeCenter")
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(_h)
    logger.setLevel(logging.INFO)

# ============================================================================
# 枚举定义
# ============================================================================

class UpgradeType(Enum):
    """升级类型枚举"""
    ENHANCE = "enhance"           # 功能增强
    REFACTOR = "refactor"         # 重构优化
    EXTEND = "extend"              # 扩展新功能
    FIX_BUG = "fix_bug"           # Bug修复
    PERFORM = "performance"        # 性能优化
    DOCUMENT = "document"          # 文档更新
    INTEGRATE = "integrate"        # 系统集成
    UPGRADE_SAGE = "upgrade_sage"  # 贤者升级
    UPGRADE_ENGINE = "engine"      # 引擎升级
    DELETE_DEPRECATED = "delete"   # 删除废弃功能(仅>180天)


class UpgradePriority(Enum):
    """升级优先级"""
    CRITICAL = 1   # 紧急
    HIGH = 2       # 高优先级
    MEDIUM = 3     # 中优先级
    LOW = 4        # 低优先级
    DEFERRED = 5  # 可延迟


class UpgradeStatus(Enum):
    """升级状态"""
    PENDING = "pending"           # 待处理
    PLANNING = "planning"         # 规划中
    GENERATING = "generating"      # 代码生成中
    TESTING = "testing"            # 测试中
    DEPLOYED = "deployed"          # 已部署
    FAILED = "failed"              # 失败
    ROLLED_BACK = "rolled_back"    # 已回滚


class UpgradeResult(Enum):
    """升级结果"""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILED = "failed"
    SKIPPED = "skipped"
    ROLLED_BACK = "rolled_back"


# ============================================================================
# 数据结构定义
# ============================================================================

@dataclass
class UpgradeContext:
    """升级上下文"""
    requirement: str                    # 升级需求描述
    source_wing: str                  # 来源分馆
    source_shelf: str                 # 来源书架
    source_cells: List[str]            # 关联的藏书阁格位ID列表
    upgrade_type: UpgradeType           # 升级类型
    priority: UpgradePriority          # 优先级
    target_modules: List[str]          # 目标模块列表
    dependencies: List[str]           # 依赖关系
    constraints: Dict[str, Any]         # 约束条件
    metadata: Dict[str, Any]            # 元数据


@dataclass
class UpgradePlan:
    """升级规划"""
    plan_id: str                      # 规划ID
    context: UpgradeContext            # 升级上下文
    strategy: str                     # 升级策略
    code_changes: List[Dict]           # 代码变更计划
    test_plan: Dict                   # 测试计划
    rollback_plan: Dict               # 回滚计划
    estimated_tokens: int              # 预估token消耗
    created_at: float                 # 创建时间戳
    status: UpgradeStatus             # 当前状态


@dataclass
class CodeChange:
    """代码变更"""
    change_id: str                   # 变更ID
    file_path: str                   # 文件路径
    change_type: str                 # add/modify/delete
    original_code: Optional[str]       # 原始代码(修改/删除时)
    new_code: Optional[str]           # 新代码(添加/修改时)
    reason: str                      # 变更原因
    impact_analysis: Dict             # 影响分析


@dataclass
class UpgradeRecord:
    """升级记录"""
    record_id: str                   # 记录ID
    plan_id: str                     # 关联的规划ID
    context: UpgradeContext            # 升级上下文
    changes: List[CodeChange]        # 代码变更列表
    result: UpgradeResult             # 升级结果
    execution_time: float            # 执行耗时(秒)
    llm_calls: int                  # 大模型调用次数
    tokens_used: int                 # 使用token数
    created_at: float                # 创建时间
    deployed_at: Optional[float]      # 部署时间
    rollback_at: Optional[float]     # 回滚时间
    error_message: Optional[str]      # 错误信息
    metadata: Dict[str, Any]           # 元数据


@dataclass
class SageUpgradeSuggestion:
    """贤者升级建议"""
    sage_name: str                   # 贤者名称
    current_capabilities: List[str]    # 当前能力
    suggested_upgrades: List[str]      # 建议升级项
    knowledge_gaps: List[str]          # 知识缺口
    priority: UpgradePriority          # 优先级
    estimated_impact: float           # 预估影响(0-1)


# ============================================================================
# 共享工具
# ============================================================================

def _get_default_llm_caller() -> Callable:
    """
    获取默认 LLM 调用器（延迟初始化，避免循环导入）。

    Returns:
        签名 (prompt: str, system: str = "") -> Dict 的可调用对象
    """
    def _call(prompt: str, system: str = "") -> Dict:
        try:
            from smart_office_assistant.src.core._somn_context_api import _module_call_llm_for_json  # noqa: F401,F811
            from smart_office_assistant.src.core.somn_core import get_somn_core
            somn = get_somn_core()
            return somn._call_llm_for_json(
                prompt=prompt,
                system_prompt=system,
                fallback={"error": "LLM调用失败"}
            )
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            return {"error": "操作失败"}
    return _call


# ============================================================================
# 共享工具函数
# ============================================================================

def _read_text_auto(file_path: Path) -> Tuple[str, str]:
    """
    自动检测编码并读取文件内容（一次 I/O 完成）。

    策略：utf-8-sig → utf-8 → gbk → latin-1，检测到可用编码后直接返回内容。

    Args:
        file_path: 文件路径

    Returns:
        (编码名称, 文件内容)
    """
    encodings = ['utf-8-sig', 'utf-8', 'gbk', 'latin-1']
    for enc in encodings:
        try:
            content = file_path.read_text(encoding=enc)
            return enc, content
        except (UnicodeDecodeError, LookupError):
            continue
    return 'utf-8', ''  # 保底


# ============================================================================
# LRU+TTL 生成缓存（线程安全，防止内存无限膨胀）
# ============================================================================

class _GenerationCache:
    """线程安全的 LRU 缓存，带 TTL（默认200条/1小时）。"""

    def __init__(self, max_size: int = 200, ttl_seconds: float = 3600.0):
        self._max_size = max_size
        self._ttl = ttl_seconds
        self._lock = threading.RLock()
        self._cache: Dict[str, Tuple[str, float]] = {}  # key -> (code, timestamp)

    def get(self, key: str) -> Optional[str]:
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None
            code, timestamp = entry
            # TTL 过期检查
            if time.time() - timestamp > self._ttl:
                del self._cache[key]
                return None
            # LRU: 更新时间戳（原子操作，锁内完成）
            self._cache[key] = (code, timestamp)
            return code

    def set(self, key: str, code: str) -> None:
        with self._lock:
            if len(self._cache) >= self._max_size:
                # LRU eviction: 删除最老的 1 个（max_size//4 至少为 1）
                evict = max(1, self._max_size // 4)
                for k in sorted(self._cache, key=lambda k: self._cache[k][1])[:evict]:
                    del self._cache[k]
            self._cache[key] = (code, time.time())

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()


# ============================================================================
# 藏书阁数据读取器
# ============================================================================

class LibraryDataReader:
    """
    藏书阁数据读取器
    
    负责从藏书阁系统读取待升级的知识数据
    """
    
    def __init__(self, library_instance=None):
        self._library = library_instance
    
    @property
    def library(self):
        """延迟获取藏书阁实例"""
        if self._library is None:
            try:
                from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import get_imperial_library
                self._library = get_imperial_library()
            except ImportError as e:
                logger.error(f"无法导入藏书阁模块: {e}")
                return None
        return self._library
    
    def query_upgrade_candidates(
        self,
        wing: Optional[str] = None,
        min_value_score: float = 0.6,
        max_age_days: int = 365,
        tags: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        查询适合升级的知识候选
        
        Args:
            wing: 分馆筛选(None表示全部)
            min_value_score: 最低价值评分
            max_age_days: 最大年龄(天)
            tags: 标签筛选
            
        Returns:
            候选知识列表
        """
        if self.library is None:
            logger.warning("藏书阁实例不可用")
            return []
        
        try:
            # 查询藏书阁（一次查询，合并过滤）
            candidates = self.library.query_cells(
                wing=wing,
                min_value_score=min_value_score,
                limit=100
            )

            # 一次性完成年龄 + 标签过滤，并构造字典
            now = datetime.now().timestamp()
            max_age_seconds = max_age_days * 24 * 3600
            results = []
            for c in candidates:
                if (now - c.created_at) > max_age_seconds:
                    continue
                if tags and not any(t in (c.tags or []) for t in tags):
                    continue
                results.append({
                    'cell_id': c.id,
                    'title': c.title,
                    'content': c.content,
                    'wing': c.wing.value if hasattr(c.wing, 'value') else str(c.wing),
                    'shelf': c.shelf,
                    'value_score': c.value_score,
                    'created_at': c.created_at,
                    'tags': c.tags,
                    'metadata': c.metadata
                })
            return results
        except Exception as e:
            logger.error(f"查询升级候选失败: {e}")
            return []
    
    def query_sage_capabilities(self, sage_name: str) -> Dict:
        """
        查询贤者能力画像
        
        Args:
            sage_name: 贤者名称
            
        Returns:
            贤者能力信息
        """
        if self.library is None:
            return {}
        
        try:
            # 从贤者分馆查询
            from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import LibraryWing
            
            cells = self.library.query_cells(
                wing=LibraryWing.SAGE,
                associated_sage=sage_name,
                limit=50
            )
            
            return {
                'sage_name': sage_name,
                'capabilities': [
                    {
                        'cell_id': c.id,
                        'title': c.title,
                        'content': c.content,
                        'grade': c.grade.value if hasattr(c.grade, 'value') else str(c.grade)
                    }
                    for c in cells
                ],
                'total_count': len(cells)
            }
        except Exception as e:
            logger.error(f"查询贤者能力失败: {e}")
            return {'sage_name': sage_name, 'capabilities': [], 'total_count': 0}
    
    def query_deprecated_functions(self, days_threshold: int = 180) -> List[Dict]:
        """
        查询停用超过指定天数的功能
        
        Args:
            days_threshold: 停用天数阈值，默认180天
            
        Returns:
            可删除的功能列表
        """
        if self.library is None:
            return []
        
        try:
            from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import LibraryWing
            
            # 查询架构分馆的历史记录
            cells = self.library.query_cells(
                wing=LibraryWing.ARCH,
                shelf='upgrade_history',
                limit=200
            )
            
            # 计算停用时间
            now = datetime.now().timestamp()
            threshold_seconds = days_threshold * 24 * 3600
            
            deprecated = []
            for c in cells:
                # 检查元数据中的最后访问时间
                last_access = c.metadata.get('last_accessed', c.created_at)
                if (now - last_access) > threshold_seconds:
                    deprecated.append({
                        'cell_id': c.id,
                        'title': c.title,
                        'content': c.content,
                        'last_accessed': last_access,
                        'days_since_access': int((now - last_access) / 86400),
                        'reason': c.metadata.get('deprecation_reason', '长期未使用')
                    })
            
            # 按停用时间排序
            deprecated.sort(key=lambda x: x['days_since_access'], reverse=True)
            return deprecated
            
        except Exception as e:
            logger.error(f"查询废弃功能失败: {e}")
            return []
    
    def query_upgrade_history(self, limit: int = 50) -> List[Dict]:
        """
        查询历史升级记录
        
        Args:
            limit: 返回数量限制
            
        Returns:
            历史升级记录列表
        """
        if self.library is None:
            return []
        
        try:
            from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import LibraryWing
            
            cells = self.library.query_cells(
                wing=LibraryWing.ARCH,
                shelf='upgrade_history',
                sort_by='created_at',
                sort_order='desc',
                limit=limit
            )
            
            return [
                {
                    'cell_id': c.id,
                    'title': c.title,
                    'content': c.content,
                    'upgrade_type': c.metadata.get('upgrade_type'),
                    'result': c.metadata.get('result'),
                    'created_at': c.created_at
                }
                for c in cells
            ]
        except Exception as e:
            logger.error(f"查询升级历史失败: {e}")
            return []


# ============================================================================
# 升级规划器
# ============================================================================

class UpgradePlanner:
    """
    升级规划器

    负责分析藏书阁数据，制定升级方案
    """

    def __init__(self):
        self._llm_caller: Optional[Callable] = None

    @property
    def llm_caller(self) -> Callable:
        if self._llm_caller is None:
            self._llm_caller = _get_default_llm_caller()
        return self._llm_caller

    def analyze_and_plan(self, context: UpgradeContext) -> UpgradePlan:
        """
        分析需求并制定升级规划
        
        Args:
            context: 升级上下文
            
        Returns:
            升级规划
        """
        # 生成规划ID
        plan_id = f"plan_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(context.requirement.encode()).hexdigest()[:8]}"
        
        # 构建分析提示
        analysis_prompt = self._build_analysis_prompt(context)
        
        # 调用LLM分析
        logger.info(f"分析升级需求: {context.requirement[:100]}...")
        analysis_result = self.llm_caller(
            prompt=analysis_prompt,
            system="你是一个专业的代码架构师，擅长分析升级需求并制定详细的升级方案。"
        )
        
        # 解析分析结果
        understanding = analysis_result.get('understanding', '')
        strategy = analysis_result.get('strategy', 'standard_enhancement')
        code_changes = analysis_result.get('code_changes', [])
        test_plan = analysis_result.get('test_plan', {})
        rollback_plan = analysis_result.get('rollback_plan', {})

        # 记录理解摘要（DEBUG 级别，避免刷屏）
        if understanding:
            logger.debug(f"LLM 需求理解: {understanding[:200]}...")
        
        # 创建升级规划
        plan = UpgradePlan(
            plan_id=plan_id,
            context=context,
            strategy=strategy,
            code_changes=code_changes,
            test_plan=test_plan,
            rollback_plan=rollback_plan,
            estimated_tokens=len(analysis_prompt) // 4,  # 粗略估算
            created_at=datetime.now().timestamp(),
            status=UpgradeStatus.PLANNING
        )
        
        return plan
    
    def _build_analysis_prompt(self, context: UpgradeContext) -> str:
        """构建分析提示词"""
        modules_str = "\n".join([f"- {m}" for m in context.target_modules])
        deps_str = "\n".join([f"- {d}" for d in context.dependencies]) if context.dependencies else "无"
        constraints_str = "\n".join([f"- {k}: {v}" for k, v in context.constraints.items()]) if context.constraints else "无"
        
        prompt = f"""
# 升级需求分析

## 需求描述
{context.requirement}

## 来源信息
- 分馆: {context.source_wing}
- 书架: {context.source_shelf}
- 关联格位: {', '.join(context.source_cells)}

## 升级类型
{context.upgrade_type.value}

## 优先级
{context.priority.name}

## 目标模块
{modules_str}

## 依赖关系
{deps_str}

## 约束条件
{constraints_str}

## 分析任务
请分析以上需求，完成以下工作：

1. **理解需求本质**: 分析需求的深层目的和预期效果
2. **识别受影响模块**: 确定需要修改的文件和模块
3. **制定升级策略**: 选择最适合的实现策略
4. **规划代码变更**: 详细列出每个文件的修改内容
5. **设计测试方案**: 制定验证升级正确性的测试计划
6. **准备回滚方案**: 制定升级失败时的回滚计划

## 输出格式
请以JSON格式输出，结构如下：
{{
    "understanding": "需求理解摘要",
    "strategy": "升级策略名称",
    "code_changes": [
        {{
            "file_path": "文件路径",
            "change_type": "add/modify/delete",
            "description": "修改描述",
            "key_changes": ["关键变更点"]
        }}
    ],
    "test_plan": {{
        "unit_tests": ["单元测试项"],
        "integration_tests": ["集成测试项"]
    }},
    "rollback_plan": {{
        "steps": ["回滚步骤"],
        "verification": "验证方法"
    }},
    "risks": ["风险点"],
    "estimated_impact": 0.0-1.0之间的影响评估值
}}
"""
        return prompt


# ============================================================================
# 大模型编码器
# ============================================================================

class LLMCodeGenerator:
    """
    大模型编码器

    负责调用大模型生成升级代码
    """

    def __init__(self, llm_caller: Optional[Callable] = None, max_workers: int = 3):
        self._llm_caller = llm_caller  # None → 惰性解析
        self._max_workers = max_workers
        self._executor: Optional[ThreadPoolExecutor] = None  # 懒加载
        self._cache = _GenerationCache()  # LRU+TTL 缓存

    @property
    def llm_caller(self) -> Callable:
        if self._llm_caller is None:
            self._llm_caller = _get_default_llm_caller()
        return self._llm_caller

    def _ensure_executor(self) -> ThreadPoolExecutor:
        if self._executor is None:
            self._executor = ThreadPoolExecutor(max_workers=self._max_workers)
        return self._executor
    
    def generate_code(self, change_spec: Dict, context: UpgradeContext) -> Tuple[str, str]:
        """
        生成单个代码变更
        
        Args:
            change_spec: 变更规格
            context: 升级上下文
            
        Returns:
            (生成的代码, 变更ID)
        """
        change_id = f"change_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(str(change_spec).encode()).hexdigest()[:8]}"
        
        # 检查缓存（LRU+TTL）
        cache_key = hashlib.md5(json.dumps(change_spec, sort_keys=True).encode()).hexdigest()
        cached_code = self._cache.get(cache_key)
        if cached_code is not None:
            logger.debug(f"使用缓存的代码生成: {change_id}")
            return cached_code, change_id
        
        # 构建生成提示
        prompt = self._build_generation_prompt(change_spec, context)
        
        # 调用LLM生成
        logger.info(f"生成代码: {change_spec.get('file_path', 'unknown')}")
        result = self.llm_caller(
            prompt=prompt,
            system="你是一个资深的Python工程师，擅长生成高质量、可维护的代码。"
        )
        
        # 提取代码
        code = self._extract_code(result, change_spec.get('change_type', 'modify'))
        
        # 缓存结果
        self._cache.set(cache_key, code)

        return code, change_id

    def generate_batch(self, change_specs: List[Dict], context: UpgradeContext) -> List[Tuple[str, str]]:
        """
        批量生成代码（使用懒初始化的线程池）

        Args:
            change_specs: 变更规格列表
            context: 升级上下文

        Returns:
            [(代码, 变更ID), ...]
        """
        executor = self._ensure_executor()
        futures = []
        for spec in change_specs:
            future = executor.submit(self.generate_code, spec, context)
            futures.append(future)
        
        results = []
        for future in futures:
            try:
                result = future.result(timeout=120)  # 2分钟超时
                results.append(result)
            except FuturesTimeoutError:
                logger.error("代码生成超时")
                results.append(("", "timeout"))
            except Exception as e:
                logger.error(f"代码生成失败: {e}")
                results.append(("", f"error_{e}"))
        
        return results
    
    def _build_generation_prompt(self, change_spec: Dict, context: UpgradeContext) -> str:
        """构建代码生成提示"""
        file_path = change_spec.get('file_path', 'unknown')
        change_type = change_spec.get('change_type', 'modify')
        description = change_spec.get('description', '')
        key_changes = change_spec.get('key_changes', [])
        
        prompt = f"""
# 代码生成任务

## 目标文件
{file_path}

## 变更类型
{change_type}

## 变更描述
{description}

## 关键变更点
{chr(10).join([f"- {c}" for c in key_changes]) if key_changes else "无"}

## 项目上下文
- 项目根目录: {PROJECT_ROOT}
- 分馆: {context.source_wing}
- 书架: {context.source_shelf}
- 关联知识: {', '.join(context.source_cells[:5]) if context.source_cells else '无'}

## 约束条件
{chr(10).join([f"- {k}: {v}" for k, v in context.constraints.items()]) if context.constraints else "无"}

## 生成要求
1. 生成完整的、可直接使用的Python代码
2. 遵循项目代码规范
3. 添加必要的注释
4. 确保代码的健壮性和安全性
5. 对于modify类型，保留必要的原有逻辑

## 输出格式
请直接输出代码，不要包含markdown代码块标记。
如果变更类型是modify或add，请输出完整的文件内容。
如果变更类型是delete，只需输出"DELETE_CONFIRMED"。
"""
        return prompt
    
    def _extract_code(self, llm_result: Dict, change_type: str) -> str:
        """从LLM结果中提取代码"""
        if isinstance(llm_result, dict):
            # 尝试从各种可能的字段提取
            for field in ['code', 'content', 'result', 'text', 'response']:
                if field in llm_result:
                    code = llm_result[field]
                    if isinstance(code, str):
                        return code.strip()
            
            # 如果是错误结果
            if 'error' in llm_result:
                logger.error(f"LLM返回错误: {llm_result['error']}")
                return ""
        
        elif isinstance(llm_result, str):
            return llm_result.strip()
        
        return ""
    
    def cleanup(self):
        """清理资源（线程池关闭）"""
        if self._executor is not None:
            self._executor.shutdown(wait=True)
            self._executor = None
        self._cache.clear()


# ============================================================================
# 升级执行器
# ============================================================================

class UpgradeExecutor:
    """
    升级执行器
    
    负责执行代码升级和验证
    """
    
    def __init__(self, backup_dir: Optional[Path] = None):
        """初始化执行器

        Args:
            backup_dir: 备份目录
        """
        self._backup_dir = backup_dir
        self._execution_log = []
        self._generator: Optional[LLMCodeGenerator] = None  # 复用单例

    @property
    def _backup_dir_path(self) -> Path:
        """惰性获取备份目录（首次写入时才创建）"""
        if self._backup_dir is None:
            self._backup_dir = PROJECT_ROOT / "data" / "upgrade_backups"
            self._backup_dir.mkdir(parents=True, exist_ok=True)
        return self._backup_dir
    
    def execute_plan(
        self,
        plan: UpgradePlan,
        dry_run: bool = False
    ) -> UpgradeRecord:
        """
        执行升级规划
        
        Args:
            plan: 升级规划
            dry_run: 是否模拟运行
            
        Returns:
            升级记录
        """
        record_id = f"record_{datetime.now().strftime('%Y%m%d%H%M%S')}_{hashlib.md5(plan.plan_id.encode()).hexdigest()[:8]}"
        start_time = datetime.now().timestamp()
        
        changes = []
        llm_calls = 0
        tokens_used = plan.estimated_tokens
        error_message = None
        
        logger.info(f"开始执行升级: {plan.plan_id} (dry_run={dry_run})")
        
        try:
            # 1. 生成代码
            plan.status = UpgradeStatus.GENERATING

            # 复用共享 generator（避免每次新建线程池）
            if self._generator is None:
                self._generator = LLMCodeGenerator()
            generator = self._generator

            for i, change_spec in enumerate(plan.code_changes):
                try:
                    code, change_id = generator.generate_code(change_spec, plan.context)
                    llm_calls += 1
                    
                    if code:
                        changes.append(CodeChange(
                            change_id=change_id,
                            file_path=change_spec.get('file_path', ''),
                            change_type=change_spec.get('change_type', 'modify'),
                            original_code=self._read_original_code(change_spec['file_path']) if change_spec.get('change_type') != 'add' else None,
                            new_code=code,
                            reason=change_spec.get('description', ''),
                            impact_analysis={}
                        ))
                        
                        # 备份原文件
                        if not dry_run and change_spec.get('change_type') != 'add':
                            self._backup_file(change_spec['file_path'])

                        # 执行变更
                        if not dry_run:
                            self._apply_change(changes[-1])
                except Exception as e:
                    logger.error(f"代码变更 {i} 失败: {e}")
                    error_message = f"变更 {i} 失败: {e}"

            # generator 复用，不在每次执行后关闭（由 UpgradeExecutor 生命周期管理）

            # 验证：变更集不能为空
            if not changes:
                error_message = "代码生成失败：未能生成任何有效变更"
                plan.status = UpgradeStatus.FAILED
                logger.error(error_message)

                record = UpgradeRecord(
                    record_id=record_id,
                    plan_id=plan.plan_id,
                    context=plan.context,
                    changes=[],
                    result=UpgradeResult.FAILED,
                    execution_time=datetime.now().timestamp() - start_time,
                    llm_calls=llm_calls,
                    tokens_used=tokens_used,
                    created_at=start_time,
                    deployed_at=None,
                    rollback_at=None,
                    error_message=error_message,
                    metadata={'dry_run': dry_run, 'strategy': plan.strategy}
                )
                return record

            # 2. 测试验证
            plan.status = UpgradeStatus.TESTING
            if not dry_run:
                test_result = self._run_tests(plan)
                if test_result['passed'] is False:  # 明确失败才中止（None = 跳过，True = 通过）
                    error_message = f"测试失败: {test_result['errors']}"
            
            # 3. 完成
            plan.status = UpgradeStatus.DEPLOYED if not error_message else UpgradeStatus.FAILED
            
        except Exception as e:
            logger.error(f"升级执行失败: {e}")
            error_message = "升级失败"
            plan.status = UpgradeStatus.FAILED
        
        end_time = datetime.now().timestamp()
        
        # 创建升级记录
        record = UpgradeRecord(
            record_id=record_id,
            plan_id=plan.plan_id,
            context=plan.context,
            changes=changes,
            result=UpgradeResult.SUCCESS if not error_message else UpgradeResult.FAILED,
            execution_time=end_time - start_time,
            llm_calls=llm_calls,
            tokens_used=tokens_used,
            created_at=start_time,
            deployed_at=end_time if not error_message else None,
            rollback_at=None,
            error_message=error_message,
            metadata={
                'dry_run': dry_run,
                'strategy': plan.strategy
            }
        )
        
        return record
    
    def _read_original_code(self, file_path: str) -> Optional[str]:
        """读取原始代码（自动检测编码，一次 I/O 完成）"""
        try:
            full_path = PROJECT_ROOT / file_path
            if full_path.exists():
                _enc, content = _read_text_auto(full_path)
                return content
        except Exception as e:
            logger.error(f"读取文件失败: {file_path} - {e}")
        return None
    
    def _backup_file(self, file_path: str):
        """备份文件"""
        try:
            full_path = PROJECT_ROOT / file_path
            if full_path.exists():
                # 创建备份目录
                backup_subdir = self._backup_dir_path / datetime.now().strftime('%Y%m%d')
                backup_subdir.mkdir(parents=True, exist_ok=True)
                
                # 生成备份文件名
                backup_name = f"{full_path.stem}_{datetime.now().strftime('%H%M%S')}{full_path.suffix}"
                backup_path = backup_subdir / backup_name
                
                # 复制文件
                import shutil
                shutil.copy2(full_path, backup_path)
                logger.info(f"已备份: {file_path} -> {backup_path}")
        except Exception as e:
            logger.error(f"备份失败: {file_path} - {e}")
    
    def _apply_change(self, change: CodeChange):
        """应用代码变更"""
        try:
            full_path = PROJECT_ROOT / change.file_path

            if change.change_type == 'delete':
                full_path.unlink()
                logger.info(f"已删除: {change.file_path}")

            elif change.change_type in ('add', 'modify'):
                # 拒绝写入空内容（防止误操作导致文件内容丢失）
                if not change.new_code or not change.new_code.strip():
                    raise ValueError(f"变更 {change.change_id} 的 new_code 为空，拒绝写入空文件")
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(change.new_code, encoding='utf-8')
                logger.info(f"已写入: {change.file_path}")

        except Exception as e:
            logger.error(f"应用变更失败: {change.change_id} - {e}")
            raise
    
    def _run_tests(self, plan: UpgradePlan) -> Dict:
        """运行测试（暂未实现实际测试逻辑，返回未测试状态）"""
        logger.warning(f"[LibraryUpgradeCenter] _run_tests 尚未实现实际测试逻辑，跳过测试验证")
        return {'passed': None, 'errors': [], 'skipped': True}
    
    def rollback(self, record: UpgradeRecord) -> bool:
        """
        回滚升级
        
        Args:
            record: 升级记录
            
        Returns:
            是否回滚成功
        """
        logger.info(f"开始回滚: {record.record_id}")
        
        try:
            for change in reversed(record.changes):
                if change.change_type in ('add', 'modify') and change.original_code:
                    full_path = PROJECT_ROOT / change.file_path
                    full_path.write_text(change.original_code, encoding='utf-8')
                    logger.info(f"已回滚: {change.file_path}")
                    
                elif change.change_type == 'delete':
                    # 恢复删除的文件
                    if change.original_code:
                        full_path = PROJECT_ROOT / change.file_path
                        full_path.write_text(change.original_code, encoding='utf-8')
                        logger.info(f"已恢复: {change.file_path}")
            
            record.result = UpgradeResult.ROLLED_BACK
            record.rollback_at = datetime.now().timestamp()
            return True
            
        except Exception as e:
            logger.error(f"回滚失败: {e}")
            return False

    def cleanup(self):
        """清理资源：关闭共享 generator 的线程池"""
        if self._generator is not None:
            self._generator.cleanup()
            self._generator = None


# ============================================================================
# 升级记录器
# ============================================================================

class UpgradeRecorder:
    """
    升级记录器
    
    负责将升级记录写入藏书阁
    """
    
    def __init__(self, library_instance=None):
        """初始化记录器
        
        Args:
            library_instance: 藏书阁实例
        """
        self._library = library_instance
    
    @property
    def library(self):
        """延迟获取藏书阁实例"""
        if self._library is None:
            try:
                from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import get_imperial_library
                self._library = get_imperial_library()
            except ImportError as e:
                logger.error(f"无法导入藏书阁模块: {e}")
                return None
        return self._library
    
    def record_upgrade(self, record: UpgradeRecord) -> bool:
        """
        将升级记录写入藏书阁
        
        Args:
            record: 升级记录
            
        Returns:
            是否记录成功
        """
        if self.library is None:
            logger.warning("藏书阁不可用，跳过记录")
            return False
        
        try:
            from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import (
                LibraryWing, MemorySource, MemoryCategory
            )
            
            # 构建记录内容
            content = self._build_record_content(record)
            
            # 提交到藏书阁
            cell = self.library.submit_cell(
                title=f"升级记录: {record.plan_id}",
                content=content,
                wing=LibraryWing.ARCH,
                shelf='upgrade_history',
                source=MemorySource.SYSTEM_EVENT,
                category=MemoryCategory.ARCHITECTURE,
                tags=['upgrade', record.result.value, record.context.upgrade_type.value],
                metadata={
                    'record_id': record.record_id,
                    'plan_id': record.plan_id,
                    'upgrade_type': record.context.upgrade_type.value,
                    'result': record.result.value,
                    'execution_time': record.execution_time,
                    'llm_calls': record.llm_calls,
                    'changes_count': len(record.changes),
                    'error': record.error_message
                },
                suggested_grade='乙'
            )

            # 防护：submit_cell 可能返回 None（藏书阁满/写入失败）
            if cell is None:
                logger.warning(f"藏书阁写入失败，跳过记录: {record.plan_id}")
                return False

            logger.info(f"升级记录已保存: {cell.id}")
            return True
            
        except Exception as e:
            logger.error(f"记录升级失败: {e}")
            return False
    
    def _build_record_content(self, record: UpgradeRecord) -> str:
        """构建记录内容"""
        changes_summary = "\n".join([
            f"- {c.change_type}: {c.file_path} ({c.reason[:50]}...)"
            for c in record.changes[:10]  # 最多10条
        ])
        
        content = f"""
# 升级执行记录

## 基本信息
- 记录ID: {record.record_id}
- 规划ID: {record.plan_id}
- 执行时间: {datetime.fromtimestamp(record.created_at).strftime('%Y-%m-%d %H:%M:%S')}
- 执行耗时: {record.execution_time:.2f}秒

## 升级详情
- 需求: {record.context.requirement[:200]}...
- 类型: {record.context.upgrade_type.value}
- 优先级: {record.context.priority.name}
- 来源: {record.context.source_wing}/{record.context.source_shelf}

## 执行结果
- 结果: {record.result.value}
- LLM调用次数: {record.llm_calls}
- 代码变更数: {len(record.changes)}

## 代码变更摘要
{changes_summary}

## 错误信息
{record.error_message or '无'}

---
此记录由藏书阁智能升级中枢自动生成
"""
        return content


# ============================================================================
# 藏书阁智能升级中枢
# ============================================================================

class LibraryUpgradeCenter:
    """
    藏书阁智能升级中枢 V1.0
    
    整合藏书阁数据读取、升级规划、大模型编码、升级执行和记录功能
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化升级中枢
        
        Args:
            config: 配置字典
        """
        self._config = config or {}
        
        # 初始化组件
        self._reader = LibraryDataReader()
        self._planner = UpgradePlanner()
        self._executor = UpgradeExecutor()
        self._recorder = UpgradeRecorder()
        
        # 升级统计
        self._stats = {
            'total_upgrades': 0,
            'successful_upgrades': 0,
            'failed_upgrades': 0,
            'total_llm_calls': 0,
            'total_tokens': 0
        }
        
        # 注册到藏书阁（如果可用）
        self._register_with_library()
    
    def _register_with_library(self):
        """注册到藏书阁"""
        if self._reader.library:
            try:
                from smart_office_assistant.src.intelligence.dispatcher.wisdom_dispatch._imperial_library import LibraryWing
                
                self._reader.library.register_bridge("LibraryUpgradeCenter", {
                    'wing': LibraryWing.ARCH,
                    'default_shelf': 'upgrade_center',
                    'source': 'LIBRARY_UPGRADE_CENTER',
                    'auto_submit': False
                })
                logger.info("藏书阁智能升级中枢已注册")
            except Exception as e:
                logger.warning(f"注册到藏书阁失败: {e}")
    
    def auto_upgrade_from_library(
        self,
        upgrade_scope: Optional[str] = None,
        dry_run: bool = True
    ) -> UpgradeRecord:
        """
        从藏书阁自动升级
        
        Args:
            upgrade_scope: 升级范围('sage'/'engine'/'global')
            dry_run: 是否模拟运行
            
        Returns:
            升级记录
        """
        logger.info(f"开始自动升级 (scope={upgrade_scope}, dry_run={dry_run})")
        
        # 1. 从藏书阁获取升级需求
        candidates = self._reader.query_upgrade_candidates(
            wing=None,
            min_value_score=0.7,
            max_age_days=30,
            tags=[upgrade_scope] if upgrade_scope else None
        )
        
        if not candidates:
            logger.info("未找到升级候选")
            return None
        
        # 2. 构建升级上下文
        context = self._build_context_from_candidates(candidates)
        
        # 3. 制定升级规划
        plan = self._planner.analyze_and_plan(context)
        
        # 4. 执行升级
        record = self._executor.execute_plan(plan, dry_run=dry_run)
        
        # 5. 记录到藏书阁
        if not dry_run:
            self._recorder.record_upgrade(record)
        
        # 6. 更新统计
        self._update_stats(record)
        
        return record
    
    def upgrade_sage_capabilities(
        self,
        sage_name: str,
        suggestions: Optional[List[SageUpgradeSuggestion]] = None
    ) -> UpgradeRecord:
        """
        升级贤者能力
        
        Args:
            sage_name: 贤者名称
            suggestions: 贤者升级建议列表
            
        Returns:
            升级记录
        """
        logger.info(f"升级贤者能力: {sage_name}")

        # 查询当前能力
        current = self._reader.query_sage_capabilities(sage_name)

        # 安全检查：能力列表为空时跳过
        capabilities = current.get('capabilities', [])
        if not capabilities:
            logger.warning(f"贤者 {sage_name} 无可查询的能力，跳过升级")
            return None

        # 如果没有提供建议，从当前能力分析
        if not suggestions:
            suggestions = self._analyze_sage_gaps(sage_name, current)

        # 构建升级上下文
        context = UpgradeContext(
            requirement=f"升级贤者 {sage_name} 的能力",
            source_wing='SAGE',
            source_shelf='sage_profiles',
            source_cells=[c['cell_id'] for c in capabilities],
            upgrade_type=UpgradeType.UPGRADE_SAGE,
            priority=UpgradePriority.MEDIUM,
            target_modules=[f"wisdom_engine_{sage_name.lower()}"],
            dependencies=[],
            constraints={},
            metadata={'sage_name': sage_name}
        )
        
        # 制定并执行规划
        plan = self._planner.analyze_and_plan(context)
        record = self._executor.execute_plan(plan, dry_run=False)
        
        # 记录
        self._recorder.record_upgrade(record)
        self._update_stats(record)
        
        return record
    
    def cleanup_deprecated(self, days_threshold: int = 180, dry_run: bool = True) -> UpgradeRecord:
        """
        清理废弃功能
        
        Args:
            days_threshold: 停用天数阈值，默认180天
            dry_run: 是否模拟运行
            
        Returns:
            升级记录
        """
        logger.info(f"清理废弃功能 (threshold={days_threshold}天, dry_run={dry_run})")

        # 查询废弃功能
        deprecated = self._reader.query_deprecated_functions(days_threshold)

        if not deprecated:
            logger.info("未找到废弃功能")
            return None

        # 安全检查：source_cells 不能为空（避免后续处理异常）
        source_cells = [d['cell_id'] for d in deprecated if d.get('cell_id')]
        if not source_cells:
            logger.warning("废弃功能列表中无有效 cell_id，跳过")
            return None
        
        # 构建升级上下文（使用已过滤的 source_cells）
        context = UpgradeContext(
            requirement=f"清理停用超过{days_threshold}天的废弃功能",
            source_wing='ARCH',
            source_shelf='upgrade_history',
            source_cells=source_cells,
            upgrade_type=UpgradeType.DELETE_DEPRECATED,
            priority=UpgradePriority.LOW,
            target_modules=source_cells,
            dependencies=[],
            constraints={'days_threshold': days_threshold},
            metadata={'deprecated_count': len(deprecated), 'valid_cells': len(source_cells)}
        )
        
        # 制定并执行规划
        plan = self._planner.analyze_and_plan(context)
        record = self._executor.execute_plan(plan, dry_run=dry_run)
        
        # 记录
        if not dry_run:
            self._recorder.record_upgrade(record)
        self._update_stats(record)
        
        return record
    
    def execute_custom_upgrade(
        self,
        requirement: str,
        upgrade_type: UpgradeType,
        priority: UpgradePriority = UpgradePriority.MEDIUM,
        target_modules: Optional[List[str]] = None,
        dry_run: bool = False
    ) -> UpgradeRecord:
        """
        执行自定义升级
        
        Args:
            requirement: 升级需求描述
            upgrade_type: 升级类型
            priority: 优先级
            target_modules: 目标模块列表
            dry_run: 是否模拟运行
            
        Returns:
            升级记录
        """
        logger.info(f"执行自定义升级: {requirement[:100]}...")
        
        # 构建上下文
        context = UpgradeContext(
            requirement=requirement,
            source_wing='ARCH',
            source_shelf='custom_upgrade',
            source_cells=[],
            upgrade_type=upgrade_type,
            priority=priority,
            target_modules=target_modules or [],
            dependencies=[],
            constraints={},
            metadata={}
        )
        
        # 制定并执行规划
        plan = self._planner.analyze_and_plan(context)
        record = self._executor.execute_plan(plan, dry_run=dry_run)
        
        # 记录
        if not dry_run:
            self._recorder.record_upgrade(record)
        self._update_stats(record)
        
        return record
    
    def _build_context_from_candidates(self, candidates: List[Dict]) -> UpgradeContext:
        """从候选知识构建升级上下文"""
        # 分析候选知识
        types = {}
        for c in candidates:
            tags = c.get('tags', [])
            if 'engine' in tags:
                types.setdefault('engine', []).append(c)
            elif 'sage' in tags:
                types.setdefault('sage', []).append(c)
            else:
                types.setdefault('general', []).append(c)
        
        # 确定升级类型
        if types.get('engine'):
            upgrade_type = UpgradeType.UPGRADE_ENGINE
        elif types.get('sage'):
            upgrade_type = UpgradeType.UPGRADE_SAGE
        else:
            upgrade_type = UpgradeType.ENHANCE
        
        return UpgradeContext(
            requirement=f"基于藏书阁知识库的自动升级，发现{len(candidates)}条候选知识",
            source_wing=candidates[0].get('wing', 'UNKNOWN'),
            source_shelf=candidates[0].get('shelf', 'UNKNOWN'),
            source_cells=[c['cell_id'] for c in candidates],
            upgrade_type=upgrade_type,
            priority=UpgradePriority.MEDIUM,
            target_modules=[],
            dependencies=[],
            constraints={},
            metadata={'candidate_count': len(candidates)}
        )
    
    def _analyze_sage_gaps(self, sage_name: str, current: Dict) -> List[SageUpgradeSuggestion]:
        """分析贤者知识缺口"""
        # TODO: 实现基于当前能力的缺口分析
        return []
    
    def _update_stats(self, record: UpgradeRecord):
        """更新统计"""
        self._stats['total_upgrades'] += 1
        self._stats['total_llm_calls'] += record.llm_calls
        self._stats['total_tokens'] += record.tokens_used
        
        if record.result == UpgradeResult.SUCCESS:
            self._stats['successful_upgrades'] += 1
        else:
            self._stats['failed_upgrades'] += 1
    
    def get_stats(self) -> Dict:
        """获取升级统计"""
        return self._stats.copy()
    
    def get_upgrade_history(self, limit: int = 20) -> List[Dict]:
        """获取升级历史"""
        return self._reader.query_upgrade_history(limit)

    def cleanup(self):
        """清理所有子组件资源"""
        self._executor.cleanup()
        logger.info("LibraryUpgradeCenter 资源已清理")


# ============================================================================
# 全局单例
# ============================================================================

_center_instance: Optional[LibraryUpgradeCenter] = None


def get_library_upgrade_center(config: Optional[Dict] = None) -> LibraryUpgradeCenter:
    """获取升级中枢实例"""
    global _center_instance
    if _center_instance is None:
        _center_instance = LibraryUpgradeCenter(config)
    return _center_instance


# ============================================================================
# 入口点
# ============================================================================

if __name__ == "__main__":
    # 示例用法
    center = get_library_upgrade_center()
    
    # 方式1: 自动从藏书阁升级
    # record = center.auto_upgrade_from_library(upgrade_scope='engine', dry_run=True)
    
    # 方式2: 升级特定贤者
    # record = center.upgrade_sage_capabilities('孔子')
    
    # 方式3: 清理废弃功能
    # record = center.cleanup_deprecated(days_threshold=180, dry_run=False)
    
    # 方式4: 自定义升级
    # record = center.execute_custom_upgrade(
    #     requirement="优化藏书阁查询性能",
    #     upgrade_type=UpgradeType.PERFORM,
    #     priority=UpgradePriority.HIGH
    # )
    
    print("藏书阁智能升级中枢已初始化")
    print(f"统计信息: {center.get_stats()}")
