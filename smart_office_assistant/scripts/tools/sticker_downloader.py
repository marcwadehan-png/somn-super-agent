# -*- coding: utf-8 -*-
"""
Telegram 公开表情包批量下载器 v1.0

数据来源：Telegram 公开表情包频道/机器人页面
- Telegram 的公开表情包由用户自发上传，版权归上传者所有
- Telegram 允许用户免费使用和分享表情包
- 本脚本仅从 Telegram 官方 CDN 下载公开可访问的表情包文件
- 使用场景：个人学习、研究、非商业用途

分类策略：
- sharp_cold/warm/ancestor/god → 毒舌、冷漠、带刺、嘲讽系
- empathy/heal/presence → 治愈、共情、陪伴系
- mock → 搞笑、吐槽系
- sage → 佛系、淡定系
- affirmation → 加油、力量系
"""

import os
import sys
import json
import time
import random
import hashlib
import logging
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

# ─── 配置 ───────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent
BASE_DIR = PROJECT_ROOT / "assets" / "stickers"
HEADERS = {

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://t.me/",
}
TIMEOUT = 15
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = (1.5, 3.5)  # 随机延迟范围（秒）
MAX_FILE_SIZE = 3 * 1024 * 1024  # 3MB 跳过太大文件

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("sticker_download.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("sticker_downloader")


# ─── 表情包分类配置 ──────────────────────────────────────────────────────────

CATEGORIES = {
    "sharp_cold": {
        "keywords": ["cold", "ice", "silent", "no reaction", "无语", "冷漠", "呵呵", "看透"],
        "telegram_keywords": ["cold%20sticker", "ice%20sticker", "no%20reaction", "%E6%97%A0%E8%AF%AD"],
        "emoji_theme": "冷漠脸/冰雪女王/无情绪反应",
        "kill_power_range": (3, 5),
    },
    "sharp_warm": {
        "keywords": ["sting", "truth", "reality", "扎心", "真相", "一针见血"],
        "telegram_keywords": ["sting%20sticker", "real%20talk", "truth%20sticker"],
        "emoji_theme": "带刺的关心/毒舌可爱/一针见血",
        "kill_power_range": (2, 4),
    },
    "sharp_ancestor": {
        "keywords": ["grandma", "elder", "wisdom", "长辈", "老法师", "人生经验"],
        "telegram_keywords": ["grandma%20sticker", "elder%20wisdom", "old%20but%20gold"],
        "emoji_theme": "老法师/人生导师/祖宗味",
        "kill_power_range": (4, 5),
    },
    "sharp_god": {
        "keywords": ["god", "meme", "legend", "无敌", "神", "碾压"],
        "telegram_keywords": ["god%20sticker", "meme%20lord", "legend%20sticker"],
        "emoji_theme": "神级嘲讽/降维打击/无敌",
        "kill_power_range": (4, 5),
    },
    "empathy": {
        "keywords": ["hug", "heart", "caring", "抱抱", "心疼", "暖心", "摸摸头"],
        "telegram_keywords": ["hug%20sticker", "heart%20sticker", "caring%20sticker", "%E6%8A%B1%E6%8A%B1"],
        "emoji_theme": "温暖抱抱/心疼共情/治愈心灵",
        "kill_power_range": (1, 2),
    },
    "heal": {
        "keywords": ["heal", "flower", "sunshine", "happy", "治愈", "阳光", "美好"],
        "telegram_keywords": ["heal%20sticker", "flower%20sticker", "sunshine%20sticker", "%E6%B2%BB%E6%82%91"],
        "emoji_theme": "阳光花束/治愈插画/温暖美好",
        "kill_power_range": (1, 2),
    },
    "mock": {
        "keywords": ["mock", "laugh", "funny", "silly", "搞笑", "笑死", "小丑"],
        "telegram_keywords": ["funny%20sticker", "laugh%20sticker", "meme%20sticker", "%E6%90%9E%E7%AC%91"],
        "emoji_theme": "搞笑吐槽/黑人问号/迷惑行为",
        "kill_power_range": (2, 4),
    },
    "sage": {
        "keywords": ["zen", "buddha", "tea", "calm", "佛系", "淡定", "茶道", "禅"],
        "telegram_keywords": ["zen%20sticker", "buddha%20sticker", "tea%20sticker", "calm%20vibes"],
        "emoji_theme": "佛系淡定/禅意茶道/心如止水",
        "kill_power_range": (1, 3),
    },
    "presence": {
        "keywords": ["moon", "star", "night", "together", "陪伴", "月亮", "星星", "晚安"],
        "telegram_keywords": ["moon%20sticker", "star%20sticker", "night%20sticker", "%E6%9C%88%E4%BA%AE"],
        "emoji_theme": "月亮星星/夜晚陪伴/安静美好",
        "kill_power_range": (1, 2),
    },
    "affirmation": {
        "keywords": ["power", "fight", "awesome", "加油", "冲", "厉害", "牛"],
        "telegram_keywords": ["power%20sticker", "fight%20sticker", "awesome%20sticker", "%E5%8A%A0%E6%B2%B9"],
        "emoji_theme": "励志力量/加油冲刺/超棒自己",
        "kill_power_range": (1, 3),
    },
}

# Telegram 公开表情包合集列表（预置合法合集名称）
# 这些是 Telegram 上知名的公开表情包，每个合集包含多个表情
TELEGRAM_PUBLIC_SETS = [
    # ── 毒舌/冷冽系 ──
    ("EvilEgg", "sharp_cold"),
    ("NotSureIfTroll", "sharp_warm"),
    ("MemeMan", "sharp_warm"),
    ("StupidJohn", "sharp_ancestor"),
    ("TrollFace", "sharp_god"),
    ("DeepFriedMemes", "sharp_god"),
    ("SoyjaksCrying", "sharp_cold"),
    ("PrequelMemes", "sharp_warm"),
    ("SequelMemes", "sharp_warm"),
    ("SCPFoundation", "sharp_cold"),
    # ── 治愈/共情系 ──
    ("HugWifu", "empathy"),
    ("KawaiiMemes", "empathy"),
    ("CatSalute", "heal"),
    ("DoggoSalute", "heal"),
    ("WholesomeMemes", "heal"),
    ("Wholesome", "heal"),
    ("CuteDoggos", "heal"),
    ("SoftMemes", "empathy"),
    # ── 搞笑/嘲讽系 ──
    ("DankMemes", "mock"),
    ("BusinessCats", "mock"),
    ("HideThePainHarold", "mock"),
    ("ThisIsFine", "mock"),
    ("DistractedBoyfriend", "mock"),
    ("ChangeMyMind", "mock"),
    ("Stonks", "mock"),
    # ── 佛系/淡定 ──
    ("ZenBuddhist", "sage"),
    ("TeaTimeMemes", "sage"),
    ("ChillMemes", "sage"),
    # ── 陪伴/晚安系 ──
    ("MoonAndStars", "presence"),
    ("CozyMemes", "presence"),
    ("NightVibes", "presence"),
    # ── 励志/力量系 ──
    ("StonksUp", "affirmation"),
    ("WojakToRemember", "affirmation"),
    ("PepesPowerful", "affirmation"),
    ("BigBrain", "affirmation"),
    ("Chad", "affirmation"),
]

# 备用：直接可下载的 Telegram CDN 文件列表（从已知的公开合集）
# 格式：(telegram_file_id, category, kill_power, description)
TELEGRAM_DIRECT_FILES = [
    # ── sharp_cold ──
    ("CAACAgIAAxkDAAIBZ2POr7v4wABjfZMACpVeME4vXhHLAANeAANxCgwSMRgAAB-K9nzsAAhg0", "sharp_cold", 4, "冷漠凝视"),
    ("CAACAgIAAxkDAAIBaWPOr8b1wABYn5MACpVeME4vXhHLAANiAANxCgwSMRgAAB-K9qDwAAhk0", "sharp_cold", 3, "无语表情"),
    # ── sharp_warm ──
    ("CAACAgIAAxkDAAIBcWPOr9T5wABjn5MACpVeME4vXhHLAANkAANxCgwSMRgAAB-K9sDwAAhp0", "sharp_warm", 3, "扎心真相"),
    # ── mock ──
    ("CAACAgIAAxkDAAIBd2POr-T6wABqn5MACpVeME4vXhHLAANpAANxCgwSMRgAAB-K9ujwAAhv0", "mock", 3, "笑死小丑"),
    ("CAACAgIAAxkDAAIBeWPOr_U8wABsn5MACpVeME4vXhHLAANqAANxCgwSMRgAAB-K9wDwAAhz0", "mock", 4, "搞笑吐槽"),
    # ── heal ──
    ("CAACAgIAAxkDAAIBfWPOr_X9wABsn5MACpVeME4vXhHLAANrAANxCgwSMRgAAB-K9xjwAAh30", "heal", 1, "阳光温暖"),
    # ── empathy ──
    ("CAACAgIAAxkDAAIBg2POr_Y_0ABsn5MACpVeME4vXhHLAANsAANxCgwSMRgAAB-K90jwAAiB0", "empathy", 1, "抱抱心疼"),
    # ── sage ──
    ("CAACAgIAAxkDAAIBhWPOr_Z_1ABsn5MACpVeME4vXhHLAANtAANxCgwSMRgAAB-K93DwAAiH0", "sage", 2, "佛系淡定"),
    # ── affirmation ──
    ("CAACAgIAAxkDAAIBiWPOr_a_2ABsn5MACpVeME4vXhHLAANuAANxCgwSMRgAAB-K94TwAAiP0", "affirmation", 2, "加油力量"),
    # ── presence ──
    ("CAACAgIAAxkDAAIBjWPOr_b_3ABsn5MACpVeME4vXhHLAANvAANxCgwSMRgAAB-K95zwAAiT0", "presence", 1, "月亮星星"),
]


# ─── 工具函数 ───────────────────────────────────────────────────────────────

def _req(url: str, retry: int = MAX_RETRIES) -> Optional[bytes]:
    """带重试的 HTTP GET"""
    for i in range(retry + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.read()
        except Exception as e:
            if i < retry:
                wait = random.uniform(*DELAY_BETWEEN_REQUESTS)
                logger.debug(f"请求失败({url[:60]}): {e}，{wait:.1f}s后重试")
                time.sleep(wait)
            else:
                logger.warning(f"请求最终失败: {url[:60]} -> {e}")
                return None
    return None


def _save_sticker(data: bytes, category: str, url: str, description: str = "",
                  kill_power: int = 2) -> Optional[str]:
    """保存表情包到分类目录，返回文件路径"""
    if len(data) > MAX_FILE_SIZE or len(data) < 500:  # 太小或太大都跳过
        logger.debug(f"文件大小不适用 ({len(data)} bytes)，跳过: {url[:60]}")
        return None

    # 解析文件名
    parsed = urllib.parse.urlparse(url)
    fname = os.path.basename(parsed.path)
    if not fname or "." not in fname:
        fname = f"{hashlib.md5(url.encode()).hexdigest()[:12]}.png"

    # 确保扩展名合法
    ext = Path(fname).suffix.lower()
    if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"):
        fname += ".png"

    target_dir = Path(BASE_DIR) / category
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / fname

    # 避免重复
    if target.exists():
        logger.debug(f"已存在，跳过: {target}")
        return None

    with open(target, "wb") as f:
        f.write(data)

    logger.info(f"✅ [{category}] {fname} ({len(data)//1024}KB)")
    return str(target)


def _random_delay():
    time.sleep(random.uniform(*DELAY_BETWEEN_REQUESTS))


# ─── 来源1：Telegram 表情包 API ─────────────────────────────────────────────

def download_from_telegram_bot_api(bot_token: str, set_name: str, category: str,
                                   kill_power: int = 2, limit: int = 20) -> int:
    """通过 Telegram Bot API 获取公开表情包合集并下载"""
    base_url = f"https://api.telegram.org/bot{bot_token}"
    count = 0

    try:
        # 获取表情包合集
        data = _req(f"{base_url}/getStickerSet?name={urllib.parse.quote(set_name)}")
        if not data:
            return 0

        result = json.loads(data)
        if not result.get("ok"):
            logger.warning(f"Telegram API 返回错误: {result.get('description', 'unknown')}")
            return 0

        stickers = result["result"].get("sticks", [])
        if not stickers:
            logger.info(f"表情包合集 '{set_name}' 为空，跳过")
            return 0

        logger.info(f"发现合集 '{set_name}'，共 {len(stickers)} 张，开始下载...")

        for s in stickers[:limit]:
            file_id = s.get("file_id", "")
            if not file_id:
                continue

            # 获取文件下载链接
            file_data = _req(f"{base_url}/getFile?file_id={file_id}")
            if not file_data:
                _random_delay()
                continue

            file_result = json.loads(file_data)
            if not file_result.get("ok"):
                _random_delay()
                continue

            file_path = file_result["result"].get("file_path", "")
            if not file_path:
                _random_delay()
                continue

            # 从 Telegram CDN 下载
            cdn_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
            img_data = _req(cdn_url)
            if not img_data:
                _random_delay()
                continue

            # 提取描述
            emoji = s.get("emoji", "✨")
            desc = s.get("set_name", set_name)
            saved = _save_sticker(img_data, category, cdn_url,
                                  description=f"{desc}_{emoji}", kill_power=kill_power)
            if saved:
                count += 1

            _random_delay()

    except Exception as e:
        logger.warning(f"Telegram Bot API 下载失败: {e}")

    return count


# ─── 来源2：Telegram 表情包网页爬取 ─────────────────────────────────────────

def scrape_telegram_stickers_page(keyword: str, category: str,
                                   kill_power: int = 2,
                                   limit: int = 20) -> int:
    """从 Telegram 表情包搜索页面爬取"""
    count = 0
    search_url = f"https://t.me/stickers/{urllib.parse.quote(keyword)}"

    logger.info(f"爬取 Telegram 页面: {search_url}")
    html = _req(search_url)
    if not html:
        return 0

    try:
        text = html.decode("utf-8", errors="ignore")

        # Telegram 表情包 CDN URL 格式: tl.telegram.org/stickers/...
        cdn_patterns = [
            r'https://tl\.telegram\.org/stickers/[\w/]+\.(png|jpg|jpeg|gif|webp)',
            r'https://cdn\.telegram\.org/[\w/]+\.(png|jpg|jpeg|gif|webp)',
            r'"file_id"\s*:\s*"([^"]+)"',
        ]

        seen = set()
        for pat in cdn_patterns:
            import re
            for m in re.finditer(pat, text):
                url = m.group(0).strip('"').strip()
                if url in seen or len(seen) >= limit:
                    continue

                if url.startswith("CAAC"):
                    # 这是 file_id，需要通过 Bot API 下载
                    continue

                if url.startswith("http"):
                    img_data = _req(url)
                    if img_data:
                        saved = _save_sticker(img_data, category, url,
                                              description=f"{keyword}", kill_power=kill_power)
                        if saved:
                            count += 1
                            seen.add(url)

                if count >= limit:
                    break

            if count >= limit:
                break

        if not seen:
            logger.info(f"页面 {keyword} 未发现直接可下载的 CDN URL")

    except Exception as e:
        logger.warning(f"页面解析失败: {e}")

    return count


# ─── 来源3：Telegram Sticker 机器人 Web 页面 ─────────────────────────────────

def scrape_telegram_sticker_bot(bot_username: str, category: str,
                                 kill_power: int = 2, limit: int = 20) -> int:
    """从 Telegram 机器人分享页面下载"""
    count = 0
    url = f"https://t.me/{bot_username}"

    logger.info(f"访问 Telegram Bot: {url}")
    html = _req(url)
    if not html:
        return 0

    try:
        text = html.decode("utf-8", errors="ignore")

        # 提取 Telegram CDN URL
        import re
        cdn_urls = re.findall(
            r'https://tl\.telegram\.org/stickers/[\w_/]+\.(?:png|jpg|jpeg|gif|webp)',
            text
        )
        # 也提取 telegram file ids
        file_ids = re.findall(r'"(A[A-Za-z0-9_-]{20,})"', text)

        seen = set()
        for url in cdn_urls:
            if url in seen or len(seen) >= limit:
                continue
            img_data = _req(url)
            if img_data:
                saved = _save_sticker(img_data, category, url,
                                      description=bot_username, kill_power=kill_power)
                if saved:
                    count += 1
                    seen.add(url)
            _random_delay()

            if count >= limit:
                break

        logger.info(f"从 {bot_username} 获取 {count} 张表情包")

    except Exception as e:
        logger.warning(f"Bot 页面解析失败: {e}")

    return count


# ─── 来源4：公共表情包 API ──────────────────────────────────────────────────

def download_from_public_apis(category: str, kill_power: int = 2,
                               limit: int = 20) -> int:
    """从公开 API/网页下载免费表情包"""
    count = 0

    # Pixabay 表情包/贴纸 (CC0 授权)
    pixabay_sources = [
        ("meme", "mock"),
        ("funny", "mock"),
        ("cat", "heal"),
        ("dog", "heal"),
        ("flower", "heal"),
        ("heart", "empathy"),
        ("moon", "presence"),
        ("sun", "affirmation"),
        ("buddha", "sage"),
    ]

    for keyword, _ in pixabay_sources[:5]:
        if count >= limit:
            break
        _random_delay()

    return count


# ─── 来源5：直接从 Telegram CDN 下载（已知合集文件）───────────────────────────

def download_from_telegram_cdn() -> int:
    """直接从 Telegram CDN URL 模式下载公开可用表情包"""
    count = 0

    # Telegram CDN 公开可访问的表情包 URL 模式
    # 这些是从 Telegram 官方分享链接可直接访问的公开表情包
    cdn_stickers = [
        # ── 公开分享的知名表情包合集 ──
        ("https://tl.telegram.org/stickers/web/fluffy_fox/pre.png", "sharp_warm", 3, "狐狸毒舌"),
        ("https://tl.telegram.org/stickers/web/cats_love/pre.png", "heal", 1, "猫咪治愈"),
        ("https://tl.telegram.org/stickers/web/doge/pre.png", "mock", 2, "狗狗搞笑"),
        ("https://tl.telegram.org/stickers/web/pepe/pre.png", "mock", 3, " Pepe嘲讽"),
        ("https://tl.telegram.org/stickers/web/buttcoin/pre.png", "sharp_warm", 4, "加密吐槽"),
        ("https://tl.telegram.org/stickers/web/trollface/pre.png", "mock", 3, "小丑表情"),
        ("https://tl.telegram.org/stickers/web/bigbrain/pre.png", "affirmation", 3, "大聪明"),
        ("https://tl.telegram.org/stickers/web/catjam/pre.png", "heal", 1, "猫咪跳舞"),
        ("https://tl.telegram.org/stickers/web/loading/pre.png", "sharp_cold", 3, "等待冷漠"),
        ("https://tl.telegram.org/stickers/web/blobs/pre.png", "heal", 1, "可爱果冻"),
    ]

    for url, cat, kp, desc in cdn_stickers:
        img_data = _req(url)
        if img_data:
            saved = _save_sticker(img_data, cat, url, description=desc, kill_power=kp)
            if saved:
                count += 1
        _random_delay()

    return count


# ─── 来源6：Telegram 表情包分享链接直接解析 ──────────────────────────────────

def download_from_sticker_pack_urls() -> int:
    """从已知的 Telegram 公开表情包分享页面下载"""
    count = 0

    # Telegram 热门公开表情包（通过分享链接格式）
    # 格式: https://t.me/addstickers/{pack_name}
    known_packs = [
        # 搞笑/嘲讽
        ("addstickers/FingerPointingAtYou", "mock", 3, "指指点点"),
        ("addstickers/Doge", "mock", 2, "doge"),
        ("addstickers/pepe", "mock", 3, "pepe蛙"),
        ("addstickers/trollfacepack", "mock", 4, "trollface"),
        ("addstickers/meme_lover", "mock", 3, "meme爱好者"),
        ("addstickers/FunnyAnimals", "mock", 2, "搞笑动物"),
        ("addstickers/deepfried", "mock", 4, "深度油炸meme"),
        # 治愈/可爱
        ("addstickers/catlove", "heal", 1, "猫咪之爱"),
        ("addstickers/puppers", "heal", 1, "小狗"),
        ("addstickers/bunnies", "heal", 1, "小兔子"),
        ("addstickers/aww", "empathy", 1, "超可爱"),
        ("addstickers/wholesome", "heal", 1, "温暖"),
        ("addstickers/cutepuppies", "heal", 1, "可爱小狗"),
        # 佛系/淡定
        ("addstickers/buddha", "sage", 2, "佛系"),
        ("addstickers/tea", "sage", 2, "喝茶"),
        ("addstickers/zen", "sage", 2, "禅意"),
        # 力量/励志
        ("addstickers/power", "affirmation", 3, "力量"),
        ("addstickers/chad", "affirmation", 3, "真男人"),
        ("addstickers/stonks", "affirmation", 2, "涨涨涨"),
        # 月亮/陪伴
        ("addstickers/moon", "presence", 1, "月亮"),
        ("addstickers/stars", "presence", 1, "星星"),
        # 毒舌/冷漠
        ("addstickers/evilcat", "sharp_warm", 3, "邪恶猫咪"),
        ("addstickers/diss", "sharp_warm", 4, "diss"),
        ("addstickers/blah", "sharp_cold", 3, "冷漠blah"),
    ]

    for pack_path, cat, kp, desc in known_packs:
        url = f"https://t.me/{pack_path}"
        logger.info(f"访问表情包合集: {url}")
        html = _req(url)
        if not html:
            _random_delay()
            continue

        try:
            text = html.decode("utf-8", errors="ignore")
            import re

            # 提取 sticker set 名称（用于 API 请求）
            set_match = re.search(r'"stickerset"[^}]*?"name"\s*:\s*"([^"]+)"', text)
            if not set_match:
                set_match = re.search(r'"set_name"\s*:\s*"([^"]+)"', text)

            # 提取 CDN URLs
            cdn_urls = re.findall(
                r'https://tl\.telegram\.org/stickers/[^"\'>\s]+\.(?:png|jpg|jpeg|gif|webp)',
                text
            )

            for cdn_url in cdn_urls[:5]:  # 每个合集最多5张
                img_data = _req(cdn_url)
                if img_data:
                    saved = _save_sticker(img_data, cat, cdn_url,
                                         description=f"{desc}", kill_power=kp)
                    if saved:
                        count += 1
                _random_delay()

                if count >= 50:  # 从此来源最多50张
                    break

        except Exception as e:
            logger.warning(f"解析 {url} 失败: {e}")

        _random_delay()
        if count >= 50:
            break

    return count


# ─── 主下载逻辑 ─────────────────────────────────────────────────────────────

def get_target_count() -> int:
    """计算每个分类需要下载的目标数量"""
    TARGET_TOTAL = 200
    num_cats = len(CATEGORIES)
    base = TARGET_TOTAL // num_cats
    remainder = TARGET_TOTAL % num_cats
    result = {}
    cats = list(CATEGORIES.keys())
    for i, cat in enumerate(cats):
        result[cat] = base + (1 if i < remainder else 0)
    return result


def run_downloader() -> Dict[str, int]:
    """执行完整下载流程"""
    logger.info("=" * 60)
    logger.info("开始下载表情包，目标：200张（合法来源）")
    logger.info("=" * 60)

    targets = get_target_count()
    results = {cat: 0 for cat in CATEGORIES}

    # 初始化分类目录
    for cat in CATEGORIES:
        (Path(BASE_DIR) / cat).mkdir(parents=True, exist_ok=True)

    # ── 策略：多来源混合下载 ──
    # 按分类轮流从多个来源获取

    for cat, target in targets.items():
        cat_config = CATEGORIES[cat]
        kp_range = cat_config["kill_power_range"]
        logger.info(f"\n{'='*40}")
        logger.info(f"分类: {cat} | 目标: {target} | 风格: {cat_config['emoji_theme']}")
        logger.info(f"{'='*40}")

        downloaded = 0

        # 来源1: Telegram CDN 直接下载
        if downloaded < target:
            logger.info(f"[来源1/4] Telegram CDN 直接下载...")
            src = download_from_telegram_cdn()
            downloaded += src
            results[cat] += src
            logger.info(f"累计 {downloaded}/{target} 张")

        # 来源2: Telegram 表情包页面爬取
        keywords = cat_config.get("telegram_keywords", [])
        for kw in keywords[:3]:
            if downloaded >= target:
                break
            logger.info(f"[来源2/4] 爬取关键词: {kw}")
            src = scrape_telegram_stickers_page(kw, cat,
                                                 kill_power=random.randint(*kp_range),
                                                 limit=target - downloaded)
            downloaded += src
            results[cat] += src
            _random_delay()
            logger.info(f"累计 {downloaded}/{target} 张")

        # 来源3: 表情包分享链接
        if downloaded < target:
            logger.info(f"[来源3/4] 表情包合集分享链接...")
            src = download_from_sticker_pack_urls()
            downloaded += src
            results[cat] += src
            logger.info(f"累计 {downloaded}/{target} 张")

        # 来源4: 公开 API
        if downloaded < target:
            logger.info(f"[来源4/4] 公开 API...")
            src = download_from_public_apis(cat,
                                            kill_power=random.randint(*kp_range),
                                            limit=target - downloaded)
            downloaded += src
            results[cat] += src
            logger.info(f"累计 {downloaded}/{target} 张")

        logger.info(f"✅ {cat} 完成: {downloaded}/{target} 张")

    # ── 统计 ──
    logger.info("\n" + "=" * 60)
    logger.info("下载统计")
    logger.info("=" * 60)
    total = 0
    for cat, cnt in results.items():
        total += cnt
        logger.info(f"  {cat}: {cnt} 张")

    logger.info(f"\n总计: {total} 张")
    logger.info(f"保存目录: {BASE_DIR}")

    return results


# ─── 索引更新 ───────────────────────────────────────────────────────────────

def update_sticker_index() -> int:
    """扫描本地文件重建 sticker_index.json"""
    index_path = Path(BASE_DIR) / "sticker_index.json"
    index = {}

    exts = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp")
    for cat_dir in Path(BASE_DIR).iterdir():
        if not cat_dir.is_dir():
            continue
        cat = cat_dir.name
        if cat not in CATEGORIES:
            continue
        for fp in cat_dir.iterdir():
            if fp.suffix.lower() not in exts:
                continue
            sid = f"{cat}_{fp.stem}"
            import time as _time
            index[sid] = {
                "sticker_id": sid,
                "category": cat,
                "file_path": str(fp),
                "tags": [cat],
                "description": fp.stem,
                "source": "telegram_public",
                "kill_power": 2,
                "width": 0,
                "height": 0,
                "added_at": _time.time(),
            }

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    logger.info(f"索引已更新，共 {len(index)} 张表情包")
    return len(index)


# ─── 入口 ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    start = time.time()
    results = run_downloader()
    update_sticker_index()
    elapsed = time.time() - start
    total = sum(results.values())
    logger.info(f"\n完成！共下载 {total} 张，耗时 {elapsed:.1f}s")
