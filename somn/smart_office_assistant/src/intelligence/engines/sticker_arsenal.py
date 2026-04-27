# -*- coding: utf-8 -*-
"""
__all__ = [
    'add_sticker',
    'add_stickers_batch',
    'download_sticker',
    'format_sticker',
    'get_all_search_keywords',
    'get_search_urls',
    'get_seed_sticker_list',
    'get_stats',
    'get_sticker_output',
    'pick',
    'pick_for_context',
    'search_by_tags',
    'to_dict',
]

StickerArsenal v1.0.0 - 大图表情包弹药库

核心能力:
1. 本地表情包管理(按场景分类存储)
2. 在线搜索get(多来源)
3. 智能匹配:根据场景/情绪/轮次自动选图
4. 表情包标签系统:每个 sticker 带有情绪标签,场景标签,杀伤力等级

存储结构:
  assets/stickers/
    ├─ sharp_cold/      # 冷冽精准
    ├─ sharp_warm/      # 带刺的关心
    ├─ sharp_ancestor/  # 祖宗味
    ├─ sharp_god/       # 上帝味
    ├─ empathy/         # 共情
    ├─ heal/            # 治愈
    ├─ mock/            # 嘲讽
    ├─ sage/            # 智者不争
    ├─ presence/        # 陪伴
    ├─ affirmation/     # 肯定力量
    ├─ sticker_index.json  # 全量索引(标签+路径+杀伤力)
    └─ sticker_sources.json # 在线来源配置
"""

import os
import json
import time
import random
import hashlib
import logging
import urllib.request
import urllib.parse
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, field, asdict

# 导入熔断器（可选，如果导入失败则不使用熔断器）
try:
    from src.utils.retry_utils import get_circuit_breaker
    _HAS_CIRCUIT_BREAKER = True
except ImportError:
    _HAS_CIRCUIT_BREAKER = False

logger = logging.getLogger(__name__)

@dataclass
class StickerInfo:
    """单张表情包的元数据"""
    sticker_id: str           # 唯一ID(文件名或URL哈希)
    category: str             # 场景分类
    file_path: Optional[str] = None  # 本地路径(已下载时)
    url: Optional[str] = None        # 在线URL(远程引用时)
    tags: List[str] = field(default_factory=list)       # 情绪/场景标签
    kill_power: int = 1       # 杀伤力等级 1-5
    description: str = ""     # 文字描述(用于搜索匹配)
    source: str = ""          # 来源平台
    width: int = 0
    height: int = 0
    added_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict:
        return asdict(self)

class StickerArsenal:
    """大图表情包弹药库"""

    # 场景分类 -> 对应目录
    CATEGORIES = [
        "sharp_cold", "sharp_warm", "sharp_ancestor", "sharp_god",
        "empathy", "heal", "mock", "sage", "presence", "affirmation",
    ]

    # 场景 -> 默认搜索关键词(用于在线搜索)
    SEARCH_KEYWORDS = {
        "sharp_cold": ["冷漠", "无语", "微笑", "看透", "呵", "你品", "经典"],
        "sharp_warm": ["扎心", "真实", "一针见血", "说的对", "暴击", "毒鸡汤"],
        "sharp_ancestor": ["老法师", "长辈", "爷爷", "说教", "我告诉你", "年轻人"],
        "sharp_god": ["天神", "降维", "碾压", "审判", "毁灭", "你看好了", "无敌"],
        "empathy": ["抱抱", "心疼", "摸头", "暖心", "懂你", "别哭", "陪伴"],
        "heal": ["治愈", "加油", "阳光", "花", "温暖", "希望", "美好"],
        "mock": ["嘲讽", "笑死", "搞笑", "小丑", "你在干嘛", "迷惑", "黑人问号"],
        "sage": ["禅", "佛系", "茶", "淡定", "无为", "超然", "佛祖"],
        "presence": ["在一起", "晚安", "月亮", "星星", "安静", "陪伴"],
        "affirmation": ["加油", "冲", "厉害", "牛", "满分", "最棒", "奋斗"],
    }

    # 斗图平台搜索API
    SOURCES = {
        "doutula": {
            "name": "斗图啦",
            "search_url": "https://www.doutula.com/search?keyword={keyword}",
            "type": "scrape",
        },
        "adoutu": {
            "name": "爱斗图",
            "search_url": "https://www.adoutu.com/search?keyword={keyword}",
            "type": "scrape",
        },
        "fabiaoqing": {
            "name": "发表情",
            "search_url": "https://www.fabiaoqing.com/search/query?keyword={keyword}",
            "type": "scrape",
        },
    }

    def __init__(self, base_dir: str = None):
        if base_dir is None:
            # 默认路径:项目根目录/assets/stickers/
            base_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "assets", "stickers"
            )
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # 确保所有分类目录存在
        for cat in self.CATEGORIES:
            (self.base_dir / cat).mkdir(exist_ok=True)

        self.index_path = self.base_dir / "sticker_index.json"
        self.sources_path = self.base_dir / "sticker_sources.json"
        self._index: Dict[str, StickerInfo] = {}
        self._load_index()

    # ═══════════════════════════════════════════
    # 索引管理
    # ═══════════════════════════════════════════

    def _load_index(self):
        """从 JSON 加载索引"""
        if self.index_path.exists():
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for sid, info in data.items():
                    self._index[sid] = StickerInfo(**info)
                logger.info(f"StickerArsenal: 已加载 {len(self._index)} 张表情包索引")
            except Exception as e:
                logger.warning(f"StickerArsenal: 索引加载失败 {e},将重建")
                self._rebuild_index()
        else:
            self._rebuild_index()

    def _save_index(self):
        """保存索引到 JSON"""
        data = {sid: info.to_dict() for sid, info in self._index.items()}
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _rebuild_index(self):
        """扫描本地文件重建索引"""
        self._index.clear()
        for cat in self.CATEGORIES:
            cat_dir = self.base_dir / cat
            if not cat_dir.exists():
                continue
            for ext in ("*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp", "*.bmp"):
                for fp in cat_dir.glob(ext):
                    sid = f"{cat}_{fp.stem}"
                    if sid not in self._index:
                        self._index[sid] = StickerInfo(
                            sticker_id=sid,
                            category=cat,
                            file_path=str(fp),
                            tags=[cat],
                            description=fp.stem,
                        )
        self._save_index()
        logger.info(f"StickerArsenal: 重建索引完成,共 {len(self._index)} 张")

    # ═══════════════════════════════════════════
    # 表情包添加
    # ═══════════════════════════════════════════

    def add_sticker(self, category: str, file_path: str = None, url: str = None,
                    tags: List[str] = None, kill_power: int = 1,
                    description: str = "", source: str = "manual") -> Optional[StickerInfo]:
        """手动添加一张表情包"""
        if category not in self.CATEGORIES:
            logger.warning(f"未知分类: {category}")
            return None

        if url:
            sid = f"{category}_{hashlib.md5(url.encode()).hexdigest()[:12]}"
            sticker = StickerInfo(
                sticker_id=sid, category=category, url=url,
                tags=tags or [category], kill_power=kill_power,
                description=description or category, source=source,
            )
        elif file_path:
            fp = Path(file_path)
            if not fp.exists():
                logger.warning(f"文件不存在: {file_path}")
                return None
            # 复制到分类目录
            target = self.base_dir / category / fp.name
            import shutil
            shutil.copy2(str(fp), str(target))
            sid = f"{category}_{fp.stem}"
            sticker = StickerInfo(
                sticker_id=sid, category=category, file_path=str(target),
                tags=tags or [category], kill_power=kill_power,
                description=description or fp.stem, source=source,
            )
        else:
            return None

        self._index[sid] = sticker
        self._save_index()
        logger.info(f"StickerArsenal: 添加表情包 {sid} -> {category}")
        return sticker

    def add_stickers_batch(self, stickers: List[Dict]) -> int:
        """批量添加表情包"""
        count = 0
        for s in stickers:
            result = self.add_sticker(
                category=s.get("category", "empathy"),
                file_path=s.get("file_path"),
                url=s.get("url"),
                tags=s.get("tags"),
                kill_power=s.get("kill_power", 1),
                description=s.get("description", ""),
                source=s.get("source", "batch"),
            )
            if result:
                count += 1
        return count

    # ═══════════════════════════════════════════
    # 表情包检索
    # ═══════════════════════════════════════════

    def pick(self, category: str, kill_power_min: int = 1,
             kill_power_max: int = 5, count: int = 1,
             prefer_recent: bool = True) -> List[StickerInfo]:
        """从指定分类中随机选取表情包
        
        Args:
            category: 场景分类
            kill_power_min: 最低杀伤力
            kill_power_max: 最高杀伤力
            count: 选取数量
            prefer_recent: 是否优先选最近添加的(避免重复)
        """
        candidates = [
            s for s in self._index.values()
            if s.category == category
            and kill_power_min <= s.kill_power <= kill_power_max
        ]
        if not candidates:
            # 回退:扩大到所有分类
            candidates = [
                s for s in self._index.values()
                if kill_power_min <= s.kill_power <= kill_power_max
            ]
        if not candidates:
            return []

        if prefer_recent:
            # 按 added_at 降序,优先选新的
            candidates.sort(key=lambda s: s.added_at, reverse=True)
            # 从前半部分随机选(避免太老的)
            pool = candidates[:max(len(candidates) // 2, 1)]
        else:
            pool = candidates

        return random.sample(pool, min(count, len(pool)))

    def pick_for_context(self, context_mode: str, confrontation_rounds: int = 0,
                         count: int = 1) -> List[StickerInfo]:
        """根据上下文模式和轮次智能选取"""
        # mapping context_mode -> category
        mode_to_cat = {
            "sharp": "sharp_cold",
            "tender": "empathy",
            "heal": "heal",
            "mock": "mock",
            "sage": "sage",
            "presence": "presence",
            "affirmation": "affirmation",
        }
        # SHARP 轮次升级分类
        if context_mode == "sharp":
            if confrontation_rounds >= 6:
                category = "sharp_god"
            elif confrontation_rounds >= 4:
                category = "sharp_ancestor"
            elif confrontation_rounds >= 2:
                category = "sharp_warm"
            else:
                category = "sharp_cold"
        else:
            category = mode_to_cat.get(context_mode, "empathy")

        # 杀伤力随轮次提升
        kill_min = min(1 + confrontation_rounds // 2, 3)
        kill_max = 5

        return self.pick(category, kill_min, kill_max, count)

    def search_by_tags(self, tags: List[str], count: int = 5) -> List[StickerInfo]:
        """按标签搜索"""
        results = []
        for s in self._index.values():
            if any(t in s.tags for t in tags):
                results.append(s)
        results.sort(key=lambda s: s.added_at, reverse=True)
        return results[:count]

    # ═══════════════════════════════════════════
    # 在线搜索get
    # ═══════════════════════════════════════════

    def get_search_urls(self, category: str, max_urls: int = 3) -> List[str]:
        """get指定分类的在线搜索URL(供浏览器/爬虫使用)"""
        keywords = self.SEARCH_KEYWORDS.get(category, [category])
        urls = []
        for source_info in self.SOURCES.values():
            for kw in keywords[:2]:  # 每个源最多2个关键词
                url = source_info["search_url"].format(keyword=urllib.parse.quote(kw))
                urls.append(url)
                if len(urls) >= max_urls:
                    return urls
        return urls

    def get_all_search_keywords(self) -> Dict[str, List[str]]:
        """get所有分类的搜索关键词"""
        return dict(self.SEARCH_KEYWORDS)

    def download_sticker(self, url: str, category: str, tags: List[str] = None,
                         kill_power: int = 1, description: str = "",
                         source: str = "download", timeout: int = 10) -> Optional[StickerInfo]:
        """下载表情包到本地 [v1.1 新增：熔断器保护]"""
        # 熔断器检查
        cb = None
        if _HAS_CIRCUIT_BREAKER:
            try:
                cb = get_circuit_breaker("sticker-arsenal-download")
                if not cb.is_available():
                    logger.warning("[熔断器] sticker_arsenal 熔断器打开，跳过下载")
                    return None
            except Exception as e:
                logger.debug(f"[熔断器] 获取熔断器失败: {e}")
                cb = None

        if category not in self.CATEGORIES:
            return None
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
                # 从URL提取文件名
                parsed = urllib.parse.urlparse(url)
                fname = os.path.basename(parsed.path)
                if not fname or "." not in fname:
                    ext = ".png"
                    fname = f"{hashlib.md5(url.encode()).hexdigest()[:12]}{ext}"
                # 确保 extension 合法
                ext = Path(fname).suffix.lower()
                if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"):
                    fname += ".png"

                # 检查大小(超过5MB跳过)
                if len(data) > 5 * 1024 * 1024:
                    logger.warning(f"表情包过大 ({len(data)//1024}KB),跳过: {url}")
                    return None

                target = self.base_dir / category / fname
                with open(target, "wb") as f:
                    f.write(data)

                sid = f"{category}_{target.stem}"
                sticker = StickerInfo(
                    sticker_id=sid, category=category, file_path=str(target),
                    url=url, tags=tags or [category], kill_power=kill_power,
                    description=description or category, source=source,
                )
                self._index[sid] = sticker
                self._save_index()
                logger.info(f"StickerArsenal: 下载 {sid} ({len(data)//1024}KB)")
                # 成功：记录成功
                if cb:
                    try:
                        cb.record_success()
                    except Exception:
                        pass
                return sticker
        except Exception as e:
            # 失败：记录失败
            if cb:
                try:
                    cb.record_failure()
                except Exception:
                    pass
            logger.warning(f"StickerArsenal: 下载失败 {url} -> {e}")
            return None

    # ═══════════════════════════════════════════
    # generate输出格式
    # ═══════════════════════════════════════════

    def format_sticker(self, sticker: StickerInfo, format: str = "markdown") -> str:
        """将表情包格式化为可发送的文本

        Args:
            format: "markdown"(图片链接), "path"(本地路径), "url"(在线URL)
        """
        src = sticker.file_path or sticker.url or ""
        if not src:
            return ""

        if format == "markdown":
            # Markdown 图片语法,聊天系统可直接渲染
            return f"![{sticker.description}]({src})"
        elif format == "path":
            return sticker.file_path or ""
        elif format == "url":
            return sticker.url or ""
        elif format == "html":
            return f'<img src="{src}" alt="{sticker.description}" style="max-width:200px">'
        return src

    def get_sticker_output(self, context_mode: str, confrontation_rounds: int = 0,
                           format: str = "markdown") -> Optional[str]:
        """一键get:选图 + 格式化输出"""
        stickers = self.pick_for_context(context_mode, confrontation_rounds, count=1)
        if not stickers:
            return None
        return self.format_sticker(stickers[0], format)

    # ═══════════════════════════════════════════
    # 统计与管理
    # ═══════════════════════════════════════════

    def get_stats(self) -> Dict:
        """统计信息"""
        cat_counts = {}
        for s in self._index.values():
            cat_counts[s.category] = cat_counts.get(s.category, 0) + 1
        local_count = sum(1 for s in self._index.values() if s.file_path)
        remote_count = sum(1 for s in self._index.values() if s.url and not s.file_path)
        return {
            "total": len(self._index),
            "local": local_count,
            "remote": remote_count,
            "by_category": cat_counts,
            "storage_dir": str(self.base_dir),
        }

    def get_seed_sticker_list(self) -> List[Dict]:
        """get初始种子表情包清单(用于批量填充)"""
        # 返回推荐的初始表情包,包含搜索关键词和分类
        seed_list = []
        for cat, keywords in self.SEARCH_KEYWORDS.items():
            for kw in keywords[:3]:
                seed_list.append({
                    "category": cat,
                    "keyword": kw,
                    "search_urls": self.get_search_urls(cat, max_urls=2),
                    "kill_power": 2 if cat.startswith("sharp") else 1,
                })
        return seed_list
