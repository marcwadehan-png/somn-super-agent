"""
行政之鞭引擎 v2.0.0
_whip_engine.py

神之架构v3.3 全局效能双向驱动机制。
执行主体：锦衣卫（厂卫）·效能司
数据源：大秦指标引擎（_daqin_metrics.py）

核心流程：
  1. 效能采集（从大秦指标读取进度数据）
  2. 信号灯评估（绿/黄/橙/红/黑）
  3. 双向鞭策（施压令下行 + 请命上行）
  4. 整改验证与闭环
"""

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════
#  枚举与类型
# ═══════════════════════════════════════════════════════════════

class WhipLevel(Enum):
    """鞭策等级（五级信号灯）"""
    GREEN = "绿灯"        # 正常运转，无干预
    YELLOW = "黄灯"       # 效能预警，下级请命
    ORANGE = "橙灯"       # 效能警告，双向鞭策
    RED = "红灯"          # 效能危机，全面施压
    BLACK = "黑灯"        # 效能崩塌，最高干预


class WhipDirection(Enum):
    """鞭策方向"""
    DOWNWARD = "施压令"       # 上级→下级
    UPWARD = "请命令"         # 下级→上级


class WhipStatus(Enum):
    """鞭策令状态"""
    PENDING = "待执行"
    EXECUTING = "执行中"
    RESOLVED = "已达标解除"
    ESCALATED = "已升级"
    ARCHIVED = "已归档"


class WhipTier(Enum):
    """鞭策层级"""
    HIGH = "高压层"       # 侯爵/伯爵/正一至三品，由七人代表大会施压
    MEDIUM = "中压层"     # 正四品至从七品，由各系统首脑施压
    BASE = "基层"         # 正八品至从九品/专员，由各司/处长官施压


# ═══════════════════════════════════════════════════════════════
#  数据结构
# ═══════════════════════════════════════════════════════════════

@dataclass
class WhipTarget:
    """被鞭策目标"""
    name: str                   # 姓名
    department: str             # 部门
    pin_rank: str               # 品秩（如"正三品"）
    tier: WhipTier              # 鞭策层级
    superior_name: str = ""     # 上级姓名
    is_innovation: bool = False # 是否从事创新工作


@dataclass
class KRProgress:
    """KR进度快照"""
    kr_id: str
    description: str
    target_value: float
    current_value: float
    score: float
    speed_ratio: float          # 进度速度比（当前速度 / 目标速度）
    days_in_quarter: int        # 季度已过天数


@dataclass
class WhipOrder:
    """鞭策令"""
    order_id: str = field(default_factory=lambda: f"WHIP-{uuid.uuid4().hex[:8]}")
    target_name: str = ""
    target_department: str = ""
    target_pin_rank: str = ""
    whip_level: WhipLevel = WhipLevel.GREEN
    direction: WhipDirection = WhipDirection.DOWNWARD
    status: WhipStatus = WhipStatus.PENDING

    # 内容
    target_kr_id: str = ""           # 关联的KR
    current_progress: float = 0      # 当前进度
    target_speed: float = 0          # 目标速度
    gap_analysis: str = ""           # 差距分析
    deadline_hours: int = 0          # 整改时限（小时）
    consequence_warning: str = ""    # 后果警告
    resource_allocation: str = ""    # 资源调配

    # 请命专用
    bottleneck: str = ""             # 瓶颈描述
    resource_request: str = ""       # 资源请求
    expected_effect: str = ""        # 预期效果

    # 时间线
    created_at: float = field(default_factory=time.time)
    updated_at: float = 0
    resolved_at: float = 0
    escalation_count: int = 0        # 升级次数

    # 闭环数据
    whip_history: List[Dict[str, Any]] = field(default_factory=list)

    def to_record(self) -> Dict[str, Any]:
        """转换为藏书阁档案格式"""
        return {
            "order_id": self.order_id,
            "target_name": self.target_name,
            "target_department": self.target_department,
            "target_pin_rank": self.target_pin_rank,
            "whip_level": self.whip_level.value,
            "direction": self.direction.value,
            "status": self.status.value,
            "target_kr_id": self.target_kr_id,
            "current_progress": round(self.current_progress, 3),
            "target_speed": round(self.target_speed, 3),
            "gap_analysis": self.gap_analysis,
            "deadline_hours": self.deadline_hours,
            "consequence_warning": self.consequence_warning,
            "bottleneck": self.bottleneck,
            "resource_request": self.resource_request,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at,
            "escalation_count": self.escalation_count,
            "whip_history": self.whip_history,
        }


@dataclass
class WhipConfig:
    """鞭策参数配置"""
    check_interval_hours: float = 24.0       # 效能校验间隔
    yellow_threshold: float = 0.5            # 黄灯触发：进度速度比
    orange_threshold: float = 0.3            # 橙灯触发：进度速度比
    red_threshold: float = 0.15              # 红灯触发：进度速度比
    max_press_frequency_hours: float = 12.0  # 红灯期间最大施压频率
    appeal_deadline_hours: float = 24.0      # 申诉时限
    petition_response_hours: float = 24.0    # 上级响应请命时限
    innovation_protection: float = 1.5       # 创新保护系数
    consecutive_whip_threshold: int = 3      # 连续鞭策升级阈值
    yellow_duration_upgrade: float = 168.0   # 黄灯持续多久升级为橙灯（小时，默认7天）
    orange_duration_upgrade: float = 120.0   # 橙灯持续多久升级为红灯（小时，默认5天）
    red_duration_upgrade: float = 168.0      # 红灯持续多久升级为黑灯（小时，默认7天）


# ═══════════════════════════════════════════════════════════════
#  核心引擎
# ═══════════════════════════════════════════════════════════════

class WhipEngine:
    """
    行政之鞭引擎。

    由锦衣卫执行，对接大秦指标引擎数据，
    实现全系统效能双向驱动的强制督促机制。
    """

    def __init__(self, config: Optional[WhipConfig] = None):
        self.config = config or WhipConfig()
        # 存储所有鞭策令：order_id -> WhipOrder
        self._orders: Dict[str, WhipOrder] = {}
        # 存储目标当前信号灯：name -> WhipLevel
        self._target_levels: Dict[str, WhipLevel] = {}
        # 存储目标信号灯持续时间：name -> timestamp（信号灯变更时记录）
        self._level_since: Dict[str, float] = {}
        # 存储连续鞭策计数：name -> int（针对同一KR）
        self._consecutive_whips: Dict[str, int] = {}
        # 效能档案（供藏书阁收录）
        self._efficiency_archive: List[Dict[str, Any]] = []

    # ── 信号灯评估 ──

    def evaluate_signal(self, target: WhipTarget,
                        kr_progress: KRProgress) -> WhipLevel:
        """
        根据KR进度评估信号灯等级。

        参数:
            target: 被鞭策目标
            kr_progress: KR进度快照

        返回:
            WhipLevel 信号灯等级
        """
        speed = kr_progress.speed_ratio
        score = kr_progress.score

        # 创新保护：阈值放宽
        if target.is_innovation:
            speed *= self.config.innovation_protection

        # 基于进度速度比评估
        if speed >= 0.8:
            level = WhipLevel.GREEN
        elif speed >= self.config.orange_threshold:
            level = WhipLevel.YELLOW
        elif speed >= self.config.red_threshold:
            level = WhipLevel.ORANGE
        elif speed >= 0.05:
            level = WhipLevel.RED
        else:
            level = WhipLevel.BLACK

        # 基于大秦指标评分二次校验
        if score >= 0.7 and level in (WhipLevel.YELLOW,):
            # 评分达标但速度稍慢，降为绿灯
            level = WhipLevel.GREEN
        elif score < 0.4 and level == WhipLevel.GREEN:
            # 评分低但速度正常，至少黄灯关注
            level = WhipLevel.YELLOW

        return level

    def _check_duration_upgrade(self, target_name: str,
                                current_level: WhipLevel) -> Optional[WhipLevel]:
        """
        检查信号灯持续时间是否触发升级。
        """
        since = self._level_since.get(target_name, 0)
        if since == 0:
            return None

        duration = time.time() - since

        upgrades = {
            WhipLevel.YELLOW: (self.config.yellow_duration_upgrade, WhipLevel.ORANGE),
            WhipLevel.ORANGE: (self.config.orange_duration_upgrade, WhipLevel.RED),
            WhipLevel.RED: (self.config.red_duration_upgrade, WhipLevel.BLACK),
        }

        if current_level in upgrades:
            threshold, next_level = upgrades[current_level]
            if duration >= threshold:
                return next_level

        return None

    # ── 鞭策令生成 ──

    def generate_press_order(self, target: WhipTarget,
                             kr_progress: KRProgress,
                             level: WhipLevel) -> WhipOrder:
        """
        生成施压令（上级→下级）。
        """
        order = WhipOrder(
            target_name=target.name,
            target_department=target.department,
            target_pin_rank=target.pin_rank,
            whip_level=level,
            direction=WhipDirection.DOWNWARD,
            target_kr_id=kr_progress.kr_id,
            current_progress=kr_progress.score,
            target_speed=kr_progress.speed_ratio,
        )

        # 差距分析
        gap = kr_progress.speed_ratio - 0.8
        order.gap_analysis = (
            f"目标KR「{kr_progress.description}」当前进度速度为"
            f"{kr_progress.speed_ratio:.1%}目标速度，"
            f"落后{abs(gap):.1%}。"
        )

        # 整改时限
        deadlines = {
            WhipLevel.YELLOW: 168,    # 7天
            WhipLevel.ORANGE: 48,     # 48小时
            WhipLevel.RED: 72,        # 72小时
            WhipLevel.BLACK: 0,       # 立即
        }
        order.deadline_hours = deadlines.get(level, 168)

        # 后果警告
        warnings = {
            WhipLevel.YELLOW: "若7天内未改善，将升级为橙灯级施压。",
            WhipLevel.ORANGE: "冻结非核心权限，所有资源强制聚焦目标KR。",
            WhipLevel.RED: "记入藏书阁效能档案，影响品秩评定。",
            WhipLevel.BLACK: "上报七人代表大会，启动人员替换流程。",
        }
        order.consequence_warning = warnings.get(level, "")

        # 资源调配
        order.resource_allocation = self._allocate_resources(level, target)

        return order

    def generate_petition_order(self, target: WhipTarget,
                                kr_progress: KRProgress,
                                level: WhipLevel) -> WhipOrder:
        """
        生成请命令（下级→上级）。
        """
        order = WhipOrder(
            target_name=target.name,
            target_department=target.department,
            target_pin_rank=target.pin_rank,
            whip_level=level,
            direction=WhipDirection.UPWARD,
            target_kr_id=kr_progress.kr_id,
            current_progress=kr_progress.score,
            target_speed=kr_progress.speed_ratio,
        )

        # 瓶颈描述（基于进度数据生成）
        if kr_progress.speed_ratio < 0.3:
            order.bottleneck = (
                f"当前KR进度严重滞后，进度速度仅为目标的"
                f"{kr_progress.speed_ratio:.1%}，"
                f"可能存在资源不足或决策延迟。"
            )
        else:
            order.bottleneck = (
                f"KR进度略低于目标速度（{kr_progress.speed_ratio:.1%}），"
                f"需要额外支持以加速推进。"
            )

        # 资源请求
        if level in (WhipLevel.RED, WhipLevel.BLACK):
            order.resource_request = "请求双倍资源倾斜与优先调度权限。"
            order.expected_effect = "资源到位后预计72小时内进度达标。"
        elif level == WhipLevel.ORANGE:
            order.resource_request = "请求额外资源支持与决策加速。"
            order.expected_effect = "资源到位后预计48小时内恢复目标速度。"
        else:
            order.resource_request = "请求资源倾斜以加速推进。"
            order.expected_effect = "资源到位后预计7天内恢复目标速度。"

        # 传递上级姓名，供execute_whip生成请命令消息时使用
        order._superior_name = target.superior_name or ""

        return order

    def _allocate_resources(self, level: WhipLevel,
                            target: WhipTarget) -> str:
        """根据鞭策等级生成分配资源说明"""
        allocations = {
            WhipLevel.YELLOW: (
                f"向{target.name}所在部门调配10%额外算力，"
                f"优先保障目标KR执行。"
            ),
            WhipLevel.ORANGE: (
                f"冻结{target.name}所有非核心权限，"
                f"100%资源聚焦于目标KR。"
            ),
            WhipLevel.RED: (
                f"全系统资源优先保障{target.name}所在部门，"
                f"锦衣卫合规司启动效能审计，"
                f"每12小时一次进度检查。"
            ),
            WhipLevel.BLACK: (
                f"上报七人代表大会，"
                f"启动全面效能审计与人员评估。"
            ),
        }
        return allocations.get(level, "")

    # ── 鞭策执行 ──

    def execute_whip(self, order: WhipOrder) -> Dict[str, Any]:
        """
        执行鞭策令。
        """
        order.status = WhipStatus.EXECUTING
        order.updated_at = time.time()

        result = {
            "order_id": order.order_id,
            "target": order.target_name,
            "level": order.whip_level.value,
            "direction": order.direction.value,
            "executed_at": order.updated_at,
        }

        if order.direction == WhipDirection.DOWNWARD:
            result["message"] = (
                f"[锦衣卫·施压令] {order.target_name}（{order.target_pin_rank}）：\n"
                f"目标KR进度 {order.current_progress:.1%}，"
                f"目标速度 {order.target_speed:.1%}。\n"
                f"{order.gap_analysis}\n"
                f"整改时限：{order.deadline_hours}小时。\n"
                f"后果：{order.consequence_warning}\n"
                f"资源调配：{order.resource_allocation}"
            )
        else:
            # 优先使用上级姓名（从target传入），回退到默认表述
            superior = getattr(order, '_superior_name', '') or order.target_name
            result["message"] = (
                f"[锦衣卫·请命令] {order.target_name}→{superior}：\n"
                f"瓶颈：{order.bottleneck}\n"
                f"请求：{order.resource_request}\n"
                f"预期效果：{order.expected_effect}\n"
                f"请在{self.config.petition_response_hours}小时内响应。"
            )

        # 记录到历史
        order.whip_history.append(result)
        self._orders[order.order_id] = order
        return result

    # ── 整改验证 ──

    def verify_resolution(self, order_id: str,
                          new_progress: float) -> Dict[str, Any]:
        """
        验证整改是否达标。

        参数:
            order_id: 鞭策令ID
            new_progress: 新的KR进度分数

        返回:
            验证结果
        """
        order = self._orders.get(order_id)
        if not order:
            return {"error": f"鞭策令{order_id}不存在"}

        before = order.current_progress
        order.current_progress = new_progress
        order.updated_at = time.time()

        # 判断是否达标
        resolve_thresholds = {
            WhipLevel.YELLOW: 0.7,
            WhipLevel.ORANGE: 0.5,
            WhipLevel.RED: 0.4,
            WhipLevel.BLACK: 0.3,
        }

        threshold = resolve_thresholds.get(order.whip_level, 0.7)

        if new_progress >= threshold:
            order.status = WhipStatus.RESOLVED
            order.resolved_at = time.time()
            # 降级信号灯
            self._update_target_level(order.target_name, WhipLevel.GREEN)

            verify_result = {
                "order_id": order_id,
                "status": "resolved",
                "before": round(before, 3),
                "after": round(new_progress, 3),
                "improvement": round(new_progress - before, 3),
                "new_level": "绿灯",
                "message": f"整改达标，鞭策令已解除。效能提升{new_progress - before:.1%}。",
            }
            order.whip_history.append(verify_result)

            return verify_result
        else:
            # 未达标，检查是否升级
            next_levels = {
                WhipLevel.YELLOW: WhipLevel.ORANGE,
                WhipLevel.ORANGE: WhipLevel.RED,
                WhipLevel.RED: WhipLevel.BLACK,
                WhipLevel.BLACK: WhipLevel.BLACK,
            }
            next_level = next_levels.get(order.whip_level)
            order.escalation_count += 1

            return {
                "order_id": order_id,
                "status": "escalated",
                "before": round(before, 3),
                "after": round(new_progress, 3),
                "improvement": round(new_progress - before, 3),
                "current_level": order.whip_level.value,
                "next_level": next_level.value if next_level else "已最高",
                "escalation_count": order.escalation_count,
                "message": (
                    f"整改未达标（需>{threshold:.1%}，实际{new_progress:.1%}），"
                    f"鞭策升级为{next_level.value if next_level else '最高级'}。"
                ),
            }

    def _update_target_level(self, target_name: str,
                             level: WhipLevel) -> None:
        """更新目标信号灯"""
        self._target_levels[target_name] = level
        self._level_since[target_name] = time.time()

    # ── 批量效能扫描 ──

    def scan_all_targets(self, targets: List[WhipTarget],
                         metrics_data: Dict[str, List[KRProgress]]
                         ) -> List[Dict[str, Any]]:
        """
        批量扫描所有目标效能，生成鞭策令。

        参数:
            targets: 所有被鞭策目标列表
            metrics_data: {目标姓名: [KR进度列表]}（来自大秦指标引擎）

        返回:
            需要执行的鞭策令列表
        """
        results = []

        for target in targets:
            kr_list = metrics_data.get(target.name, [])
            if not kr_list:
                continue

            # 取最差的KR作为评估依据
            worst_kr = min(kr_list, key=lambda kr: kr.speed_ratio)

            # 评估信号灯
            new_level = self.evaluate_signal(target, worst_kr)

            # 检查持续时间升级
            duration_upgrade = self._check_duration_upgrade(target.name, new_level)
            if duration_upgrade:
                new_level = duration_upgrade

            old_level = self._target_levels.get(target.name, WhipLevel.GREEN)

            if new_level != old_level:
                self._update_target_level(target.name, new_level)

            # 绿灯不鞭策
            if new_level == WhipLevel.GREEN:
                # 连续鞭策计数归零
                self._consecutive_whips[target.name] = 0
                continue

            # 检查连续鞭策次数
            self._consecutive_whips[target.name] = \
                self._consecutive_whips.get(target.name, 0) + 1

            # 检查是否触发根因分析
            if (self._consecutive_whips[target.name]
                    >= self.config.consecutive_whip_threshold):
                results.append({
                    "type": "root_cause_analysis",
                    "target": target.name,
                    "message": (
                        f"{target.name}已连续{self._consecutive_whips[target.name]}次"
                        f"被鞭策，建议启动根因分析"
                        f"（KR设定是否合理？是否存在系统性瓶颈？）"
                    ),
                })

            # 生成鞭策令
            if new_level in (WhipLevel.YELLOW,):
                # 黄灯：请命上行
                petition = self.generate_petition_order(target, worst_kr, new_level)
                results.append({
                    "type": "whip_order",
                    "order": petition.to_record(),
                    "execution": self.execute_whip(petition),
                })
            elif new_level == WhipLevel.ORANGE:
                # 橙灯：双向
                press = self.generate_press_order(target, worst_kr, new_level)
                petition = self.generate_petition_order(target, worst_kr, new_level)
                results.append({
                    "type": "dual_whip",
                    "press_order": press.to_record(),
                    "petition_order": petition.to_record(),
                    "press_execution": self.execute_whip(press),
                    "petition_execution": self.execute_whip(petition),
                })
            else:
                # 红灯/黑灯：全面施压
                press = self.generate_press_order(target, worst_kr, new_level)
                results.append({
                    "type": "whip_order",
                    "order": press.to_record(),
                    "execution": self.execute_whip(press),
                })

        return results

    # ── 看板 ──

    def get_whip_dashboard(self) -> Dict[str, Any]:
        """
        获取鞭策看板数据。
        """
        level_counts = {level: 0 for level in WhipLevel}
        for level in self._target_levels.values():
            level_counts[level] += 1

        active_orders = [
            o.to_record() for o in self._orders.values()
            if o.status in (WhipStatus.PENDING, WhipStatus.EXECUTING)
        ]

        return {
            "total_targets": len(self._target_levels),
            "signal_distribution": {
                level.value: count
                for level, count in level_counts.items()
            },
            "active_orders": len(active_orders),
            "active_orders_detail": active_orders,
            "consecutive_whip_targets": {
                name: count
                for name, count in self._consecutive_whips.items()
                if count >= 2
            },
            "archive_size": len(self._efficiency_archive),
        }

    # ── 档案管理 ──

    def archive_order(self, order_id: str) -> Dict[str, Any]:
        """归档鞭策令到效能档案"""
        order = self._orders.get(order_id)
        if not order:
            return {"error": f"鞭策令{order_id}不存在"}

        order.status = WhipStatus.ARCHIVED
        record = order.to_record()
        self._efficiency_archive.append(record)

        return {
            "order_id": order_id,
            "status": "archived",
            "archive_size": len(self._efficiency_archive),
        }

    def export_efficiency_archive(self) -> List[Dict[str, Any]]:
        """导出全量效能档案（供藏书阁收录）"""
        return list(self._efficiency_archive)

    def get_target_whip_history(self, target_name: str) -> List[Dict[str, Any]]:
        """查询目标的鞭策历史"""
        return [
            o.to_record() for o in self._orders.values()
            if o.target_name == target_name
        ]

    # ── 统计 ──

    def get_statistics(self) -> Dict[str, Any]:
        """获取鞭策统计"""
        total = len(self._orders)
        if total == 0:
            return {"total_orders": 0}

        status_counts = {}
        for o in self._orders.values():
            s = o.status.value
            status_counts[s] = status_counts.get(s, 0) + 1

        level_counts = {}
        for o in self._orders.values():
            l = o.whip_level.value
            level_counts[l] = level_counts.get(l, 0) + 1

        resolved = [o for o in self._orders.values()
                    if o.status == WhipStatus.RESOLVED]

        avg_improvement = 0
        if resolved:
            # 从历史记录中推算改善幅度（简化：取最后一条记录的进度与初始对比）
            improvements = []
            for o in resolved:
                if o.whip_history:
                    first = o.whip_history[0].get("before", 0)
                    last = o.whip_history[-1].get("after", first)
                    improvements.append(last - first)
            if improvements:
                avg_improvement = sum(improvements) / len(improvements)

        return {
            "total_orders": total,
            "by_status": status_counts,
            "by_level": level_counts,
            "resolved_count": len(resolved),
            "resolution_rate": len(resolved) / total if total > 0 else 0,
            "avg_improvement": round(avg_improvement, 4),
            "archive_size": len(self._efficiency_archive),
        }


# ═══════════════════════════════════════════════════════════════
#  便捷函数
# ═══════════════════════════════════════════════════════════════

def create_whip_engine(config: Optional[WhipConfig] = None) -> WhipEngine:
    """创建行政之鞭引擎实例"""
    return WhipEngine(config=config)


def quick_evaluate(speed_ratio: float, score: float,
                   is_innovation: bool = False) -> str:
    """
    快速评估单个KR的信号灯等级。

    参数:
        speed_ratio: 进度速度比（当前速度/目标速度）
        score: KR评分（0~1）
        is_innovation: 是否创新类KR

    返回:
        信号灯等级字符串
    """
    config = WhipConfig()
    target = WhipTarget(
        name="quick", department="quick", pin_rank="quick",
        tier=WhipTier.BASE, is_innovation=is_innovation,
    )
    kr = KRProgress(
        kr_id="quick", description="quick",
        target_value=1.0, current_value=score,
        score=score, speed_ratio=speed_ratio, days_in_quarter=45,
    )

    engine = WhipEngine(config)
    return engine.evaluate_signal(target, kr).value
