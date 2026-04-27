"""
__all__ = [
    'get_data_source_breakdown',
    'scan',
    'scan_with_network',
]

统一数据扫描器 - Unified Data Scanner
合并 daily_learning._scan_new_data + three_tier_learning._scan_local_data
+ learning_scheduler.scan_data_sources/_load_* 的 4 处重复扫描逻辑。
"""

import logging
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

from .base_strategy import DataScanResult

class UnifiedDataScanner:
    """
    统一数据扫描器。

    消除 4 处重复：
    1. daily_learning._scan_new_data   （含网络学习触发）
    2. three_tier_learning._scan_local_data
    3. learning_scheduler.scan_data_sources / _load_*
    4. integrated_learning(通过 scheduler.plan_learning_data_selection)
    """

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.time_window = timedelta(hours=24)

    # ─────────────────────────────────────────────────
    # 公共入口
    # ─────────────────────────────────────────────────

    def scan(self, recent_only: bool = True) -> DataScanResult:
        """
        全量扫描，返回 DataScanResult。

        Args:
            recent_only: True → 仅扫描 24h 内数据；False → 全量
        """
        cutoff = datetime.now() - self.time_window if recent_only else None

        findings = self._load_local_findings(cutoff)
        validations, errors_from_val = self._load_validations(cutoff)
        learning_events = self._load_learning_events(cutoff)
        network_research = self._load_network_research()

        # 从错误案例里再补充 error 数据
        errors = list(errors_from_val)
        errors.extend(self._load_error_events(cutoff))

        result = DataScanResult(
            findings=findings,
            validations=validations,
            errors=errors,
            learning_events=learning_events,
            network_research=network_research,
        )
        return result

    def scan_with_network(self, trigger_fetch: bool = True) -> DataScanResult:
        """
        扫描 + 可选触发浏览器网络学习（幂等）。
        对应 daily_learning._run_network_learning + _fetch_network_research。
        """
        result = self.scan(recent_only=True)

        if trigger_fetch:
            net_findings = self._run_network_learning()
            # 避免重复（已在 network_research 里）
            existing_ids = {
                f.get("发现ID", f.get("发现标题", "")) for f in result.network_research
            }
            for f in net_findings:
                fid = f.get("发现ID", f.get("发现标题", ""))
                if fid not in existing_ids:
                    result.network_research.append(f)
                    existing_ids.add(fid)

        return result

    def get_data_source_breakdown(self, result: DataScanResult) -> Dict:
        """生成数据源分布统计（兼容 integrated_learning 输出格式）"""
        local_count = result.local_count
        net_count = result.network_count
        total = result.total
        return {
            "本地数据": local_count,
            "网络数据": net_count,
            "总计": total,
            "本地占比": f"{local_count / max(total, 1) * 100:.1f}%",
        }

    # ─────────────────────────────────────────────────
    # 内部加载方法（消除重复）
    # ─────────────────────────────────────────────────

    def _load_local_findings(self, cutoff: datetime = None) -> List[Dict]:
        """加载本地发现（非 NET_ 前缀）"""
        path = self.base_path / "findings"
        results = []
        if not path.exists():
            return results
        for fp in path.glob("*.yaml"):
            if fp.name.startswith("NET_"):
                continue
            data = self._safe_load(fp)
            if data and (cutoff is None or self._is_recent(data, cutoff)):
                data.setdefault("source", "local")
                data["_source"] = "local_finding"
                results.append(data)
        return results

    def _load_validations(self, cutoff: datetime = None) -> Tuple[List[Dict], List[Dict]]:
        """加载验证结果，同时提取失败案例为 errors"""
        path = self.base_path / "validation"
        validations, errors = [], []
        if not path.exists():
            return validations, errors
        for fp in path.glob("*.yaml"):
            data = self._safe_load(fp)
            if not data:
                continue
            if cutoff is None or self._is_recent(data, cutoff):
                data["_source"] = "local_validation"
                validations.append(data)
                if not data.get("验证通过", True):
                    errors.append({
                        "假设": data.get("假设内容", ""),
                        "实际结果": "验证失败",
                        "错误原因": data.get("失败原因", "未明确原因"),
                        "验证ID": data.get("验证ID", ""),
                        "时间": data.get("验证时间", ""),
                    })
        return validations, errors

    def _load_learning_events(self, cutoff: datetime = None) -> List[Dict]:
        """加载已保存的 LE_*.yaml 学习事件"""
        path = self.base_path / "learning"
        results = []
        if not path.exists():
            return results
        for fp in path.glob("LE_*.yaml"):
            data = self._safe_load(fp)
            if data and (cutoff is None or self._is_recent(data, cutoff)):
                data["_source"] = "local_learning"
                results.append(data)
        return results

    def _load_error_events(self, cutoff: datetime = None) -> List[Dict]:
        """从学习事件中提取错误类型"""
        path = self.base_path / "learning"
        results = []
        if not path.exists():
            return results
        for fp in path.glob("LE_*.yaml"):
            data = self._safe_load(fp)
            if data and data.get("学习类型") == "错误学习":
                if cutoff is None or self._is_recent(data, cutoff):
                    results.append(data.get("输入数据", {}))
        return results

    def _load_network_research(self) -> List[Dict]:
        """加载 NET_*.yaml 网络研究数据"""
        path = self.base_path / "findings"
        results = []
        if not path.exists():
            return results
        for fp in path.glob("NET_*.yaml"):
            data = self._safe_load(fp)
            if data:
                data["source"] = "network"
                data["_source"] = "network_research"
                results.append(data)
        return results

    # ─────────────────────────────────────────────────
    # 网络学习（幂等）
    # ─────────────────────────────────────────────────

    def _run_network_learning(self) -> List[Dict]:
        """触发浏览器网络学习（幂等：今日已有则直接加载）"""
        today_str = datetime.now().strftime("%Y%m%d")
        findings_dir = self.base_path / "findings"
        findings_dir.mkdir(parents=True, exist_ok=True)

        today_files = list(findings_dir.glob(f"NET_BROWSER_*{today_str}*.yaml"))
        if today_files:
            results = []
            for fp in today_files:
                data = self._safe_load(fp)
                if data:
                    data["source"] = "network"
                    results.append(data)
            logger.info(f"今日浏览器数据已存在，加载 {len(results)} 条（跳过重复抓取）")
            return results

        return self._fetch_network_research(today_str)

    def _fetch_network_research(self, date_str: str) -> List[Dict]:
        """调用 BrowserNetworkLearner 抓取网络数据"""
        try:
            from src.neural_memory.browser_learning import BrowserNetworkLearner
        except ImportError:
            try:
                from .browser_learning import BrowserNetworkLearner
            except ImportError:
                logger.warning("browser_learning 模块未找到，跳过浏览器学习")
                return []

        findings_dir = self.base_path / "findings"
        learner = BrowserNetworkLearner(findings_dir=findings_dir, browser_type="auto")
        results = learner.run()
        logger.info(f"浏览器网络学习完成，获取 {len(results)} 条研究发现")
        return results

    # ─────────────────────────────────────────────────
    # 工具方法
    # ─────────────────────────────────────────────────

    @staticmethod
    def _safe_load(fp: Path) -> Dict:
        """安全读取 YAML，失败返回 None"""
        try:
            with open(fp, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception:
            return None

    @staticmethod
    def _is_recent(data: Dict, cutoff: datetime) -> bool:
        """检查 data 是否在 cutoff 之后（尝试多种时间字段）"""
        for field in ("创建时间", "验证时间", "时间", "created_at", "timestamp"):
            if field in data:
                try:
                    t = datetime.fromisoformat(str(data[field]).replace("Z", "+00:00"))
                    return t >= cutoff
                except Exception:
                    continue
        return True  # 无时间字段默认包含
