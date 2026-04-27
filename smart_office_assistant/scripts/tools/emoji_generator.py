# -*- coding: utf-8 -*-
"""
Windows Emoji 表情包生成器 v1.0

数据来源：Windows 10/11 内置 Segoe UI Emoji 字体
- Windows emoji 字体是系统内置资源，随 OS 提供
- 渲染为 PNG 图片后存储到本地表情包库
- 无版权问题，可自由使用

分类策略（10分类 × 20张 = 200张）：
- sharp_cold/warm/ancestor/god → 冷漠脸/扎心真相/老法师/无敌神
- empathy/heal → 心疼抱抱/阳光治愈
- mock → 搞笑嘲讽
- sage → 佛系淡定
- presence → 月亮星星
- affirmation → 加油力量
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
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from dataclasses import dataclass, field, asdict

# ─── 配置 ───────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
BASE_DIR = PROJECT_ROOT / "assets" / "stickers"
FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\seguiemj.ttf"),
    Path(r"C:\Windows\Fonts\SegoeUIEmoji.ttf"),
    Path(r"C:\Windows\Fonts\seguiemj.ttf".lower()),
]
FONT_PATH = str(next((candidate for candidate in FONT_CANDIDATES if candidate.exists()), FONT_CANDIDATES[0]))
TARGET_TOTAL = 200


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("emoji_generator.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("emoji_generator")


# ─── Emoji 分类映射表 ────────────────────────────────────────────────────────

@dataclass
class EmojiEntry:
    char: str
    description: str
    kill_power: int


# 分类配置：每个分类20张 emoji
CATEGORY_EMOJIS: Dict[str, List[EmojiEntry]] = {
    # ── 冷冽精准 ──────────────────────────────────────────────────────────
    "sharp_cold": [
        EmojiEntry("😏", "意味深长微笑", 4),
        EmojiEntry("😐", "冷漠脸", 3),
        EmojiEntry("😑", "面无表情", 3),
        EmojiEntry("😶", "无话可说", 3),
        EmojiEntry("🤐", "闭嘴", 4),
        EmojiEntry("😒", "不感兴趣", 3),
        EmojiEntry("🙄", "翻白眼", 4),
        EmojiEntry("😬", "尴尬", 2),
        EmojiEntry("😮‍💨", "叹气", 2),
        EmojiEntry("😔", "失落", 2),
        EmojiEntry("🫤", "一般般", 3),
        EmojiEntry("🫥", "幽灵", 3),
        EmojiEntry("🥱", "无聊", 2),
        EmojiEntry("😴", "困了", 1),
        EmojiEntry("😶‍🌫️", "沉默", 3),
        EmojiEntry("🫃", "躺平", 3),
        EmojiEntry("😌", "释然", 2),
        EmojiEntry("🤫", "嘘", 4),
        EmojiEntry("🤭", "偷笑", 2),
        EmojiEntry("😈", "魔鬼微笑", 5),
    ],

    # ── 带刺的关心 ────────────────────────────────────────────────────────
    "sharp_warm": [
        EmojiEntry("😤", "气鼓鼓", 4),
        EmojiEntry("😠", "生气", 4),
        EmojiEntry("😡", "愤怒", 5),
        EmojiEntry("🤬", "骂人", 5),
        EmojiEntry("😾", "生气的猫", 4),
        EmojiEntry("🙀", "惊恐的猫", 3),
        EmojiEntry("😾", "嫌弃", 4),
        EmojiEntry("🫣", "不敢看", 2),
        EmojiEntry("😰", "焦虑", 2),
        EmojiEntry("😥", "失落", 2),
        EmojiEntry("😓", "累", 2),
        EmojiEntry("😩", "疲惫", 2),
        EmojiEntry("🥵", "热", 2),
        EmojiEntry("🥶", "冷", 2),
        EmojiEntry("😵‍💫", "晕", 2),
        EmojiEntry("😵", "懵了", 3),
        EmojiEntry("🤯", "头脑爆炸", 4),
        EmojiEntry("😱", "惊恐", 3),
        EmojiEntry("🙈", "不忍直视", 3),
        EmojiEntry("💀", "笑死", 4),
    ],

    # ── 祖宗味 ────────────────────────────────────────────────────────────
    "sharp_ancestor": [
        EmojiEntry("🧐", "审视", 4),
        EmojiEntry("🤓", "学霸", 3),
        EmojiEntry("🧙", "老法师", 4),
        EmojiEntry("🧛", "吸血鬼", 3),
        EmojiEntry("🧜", "人鱼", 2),
        EmojiEntry("🧚", "仙子", 2),
        EmojiEntry("👴", "老爷爷", 3),
        EmojiEntry("👵", "老奶奶", 3),
        EmojiEntry("🧓", "老人", 3),
        EmojiEntry("🤶", "圣诞奶奶", 2),
        EmojiEntry("🎅", "圣诞老人", 2),
        EmojiEntry("🦸", "超级英雄", 3),
        EmojiEntry("🦹", "反派英雄", 4),
        EmojiEntry("🧜‍♂️", "人鱼男", 2),
        EmojiEntry("🧞", "精灵", 3),
        EmojiEntry("🦊", "狐狸", 3),
        EmojiEntry("🦉", "猫头鹰", 3),
        EmojiEntry("🐉", "龙", 4),
        EmojiEntry("🦅", "老鹰", 4),
        EmojiEntry("🐺", "狼", 4),
    ],

    # ── 上帝味 ────────────────────────────────────────────────────────────
    "sharp_god": [
        EmojiEntry("🤴", "王子", 4),
        EmojiEntry("👸", "公主", 3),
        EmojiEntry("🫅", "王子", 4),
        EmojiEntry("🎩", "礼帽", 3),
        EmojiEntry("👑", "皇冠", 5),
        EmojiEntry("⚡", "闪电", 5),
        EmojiEntry("🔥", "火焰", 5),
        EmojiEntry("💥", "爆炸", 5),
        EmojiEntry("⭐", "星星", 3),
        EmojiEntry("🌟", "闪星", 4),
        EmojiEntry("✨", "发光", 3),
        EmojiEntry("💫", "旋转星", 3),
        EmojiEntry("🌈", "彩虹", 3),
        EmojiEntry("⚔️", "剑", 4),
        EmojiEntry("🏆", "奖杯", 4),
        EmojiEntry("🥇", "金牌", 4),
        EmojiEntry("💎", "钻石", 4),
        EmojiEntry("🗽", "自由女神", 4),
        EmojiEntry("⛩️", "神社", 3),
        EmojiEntry("🔱", "三叉戟", 5),
    ],

    # ── 共情心疼 ──────────────────────────────────────────────────────────
    "empathy": [
        EmojiEntry("🥺", "可怜巴巴", 1),
        EmojiEntry("😭", "大哭", 1),
        EmojiEntry("😢", "流泪", 1),
        EmojiEntry("🥹", "感动", 1),
        EmojiEntry("😢", "悲伤", 1),
        EmojiEntry("😿", "哭泣的猫", 1),
        EmojiEntry("🙎", "不开心的人", 2),
        EmojiEntry("😞", "失望", 2),
        EmojiEntry("😟", "担心", 2),
        EmojiEntry("😕", "困惑", 1),
        EmojiEntry("🫤", "无奈", 2),
        EmojiEntry("😣", "痛苦", 2),
        EmojiEntry("😖", "沮丧", 2),
        EmojiEntry("😫", "精疲力尽", 2),
        EmojiEntry("🥲", "强颜欢笑", 2),
        EmojiEntry("🤧", "感冒", 1),
        EmojiEntry("😷", "生病", 1),
        EmojiEntry("🤒", "发烧", 1),
        EmojiEntry("🩹", "创可贴", 1),
        EmojiEntry("🫂", "拥抱", 1),
    ],

    # ── 治愈美好 ──────────────────────────────────────────────────────────
    "heal": [
        EmojiEntry("😊", "微笑", 1),
        EmojiEntry("😄", "大笑", 1),
        EmojiEntry("🙂", "开心", 1),
        EmojiEntry("😇", "天使", 1),
        EmojiEntry("🥰", "爱心眼", 1),
        EmojiEntry("😍", "花痴", 1),
        EmojiEntry("🤩", "星星眼", 1),
        EmojiEntry("😋", "好吃", 1),
        EmojiEntry("😎", "酷", 2),
        EmojiEntry("🤗", "抱抱", 1),
        EmojiEntry("🤠", "牛仔", 2),
        EmojiEntry("🧸", "小熊", 1),
        EmojiEntry("🐶", "小狗", 1),
        EmojiEntry("🐱", "小猫", 1),
        EmojiEntry("🐰", "小兔子", 1),
        EmojiEntry("🦋", "蝴蝶", 1),
        EmojiEntry("🌸", "樱花", 1),
        EmojiEntry("🌷", "郁金香", 1),
        EmojiEntry("🌻", "向日葵", 1),
        EmojiEntry("🍀", "四叶草", 1),
    ],

    # ── 搞笑嘲讽 ──────────────────────────────────────────────────────────
    "mock": [
        EmojiEntry("😂", "笑哭", 2),
        EmojiEntry("🤣", "笑到窒息", 3),
        EmojiEntry("😹", "笑哭的猫", 2),
        EmojiEntry("😻", "惊艳的猫", 2),
        EmojiEntry("🙉", "不看", 3),
        EmojiEntry("🐵", "猴子", 2),
        EmojiEntry("🙊", "不说", 3),
        EmojiEntry("🤡", "小丑", 4),
        EmojiEntry("💩", "便便", 3),
        EmojiEntry("👻", "幽灵", 2),
        EmojiEntry("🤖", "机器人", 2),
        EmojiEntry("😈", "恶魔", 3),
        EmojiEntry("👹", "鬼", 3),
        EmojiEntry("👺", "天狗", 3),
        EmojiEntry("🎭", "面具", 3),
        EmojiEntry("🐸", "青蛙", 3),
        EmojiEntry("🐷", "猪", 2),
        EmojiEntry("🦁", "狮子", 3),
        EmojiEntry("🐻", "熊", 2),
        EmojiEntry("🦈", "鲨鱼", 3),
    ],

    # ── 佛系淡定 ──────────────────────────────────────────────────────────
    "sage": [
        EmojiEntry("🍵", "喝茶", 1),
        EmojiEntry("🧘", "冥想", 1),
        EmojiEntry("☸️", "法轮", 2),
        EmojiEntry("🕉️", "唵咒", 2),
        EmojiEntry("🪷", "莲花", 1),
        EmojiEntry("🙏", "祈祷", 1),
        EmojiEntry("💮", "白花", 1),
        EmojiEntry("🌿", "绿叶", 1),
        EmojiEntry("🍃", "清风", 1),
        EmojiEntry("🍂", "落叶", 1),
        EmojiEntry("🌊", "波浪", 1),
        EmojiEntry("⛩️", "神社", 1),
        EmojiEntry("🏮", "灯笼", 1),
        EmojiEntry("🎋", "七夕竹", 1),
        EmojiEntry("🎍", "门松", 1),
        EmojiEntry("🪭", "扇子", 1),
        EmojiEntry("🍱", "便当", 1),
        EmojiEntry("🦜", "鹦鹉", 1),
        EmojiEntry("🐢", "乌龟", 1),
        EmojiEntry("🦎", "蜥蜴", 1),
    ],

    # ── 陪伴月亮 ──────────────────────────────────────────────────────────
    "presence": [
        EmojiEntry("🌙", "月亮", 1),
        EmojiEntry("🌛", "上弦月", 1),
        EmojiEntry("🌜", "下弦月", 1),
        EmojiEntry("🌝", "满月", 1),
        EmojiEntry("🌚", "新月", 1),
        EmojiEntry("⭐", "星星", 1),
        EmojiEntry("🌟", "亮星", 1),
        EmojiEntry("✨", "闪光", 1),
        EmojiEntry("🌠", "流星", 1),
        EmojiEntry("💫", "星尘", 1),
        EmojiEntry("🌌", "银河", 1),
        EmojiEntry("🪐", "行星", 1),
        EmojiEntry("🔮", "水晶球", 1),
        EmojiEntry("🎠", "旋转木马", 1),
        EmojiEntry("🎈", "气球", 1),
        EmojiEntry("🕯️", "蜡烛", 1),
        EmojiEntry("🌸", "夜樱", 1),
        EmojiEntry("🦢", "天鹅", 1),
        EmojiEntry("🐚", "贝壳", 1),
        EmojiEntry("🏠", "家", 1),
    ],

    # ── 力量励志 ──────────────────────────────────────────────────────────
    "affirmation": [
        EmojiEntry("💪", "肌肉", 2),
        EmojiEntry("😤", "冲", 3),
        EmojiEntry("🔥", "火热", 3),
        EmojiEntry("⚡", "电力", 4),
        EmojiEntry("💥", "爆发", 4),
        EmojiEntry("🎯", "命中", 4),
        EmojiEntry("🚀", "火箭", 4),
        EmojiEntry("💎", "钻石", 3),
        EmojiEntry("🏆", "冠军", 3),
        EmojiEntry("🥇", "金牌", 3),
        EmojiEntry("🎖️", "奖章", 3),
        EmojiEntry("💯", "满分", 4),
        EmojiEntry("🙌", "欢呼", 2),
        EmojiEntry("👏", "鼓掌", 2),
        EmojiEntry("🤛", "左拳", 3),
        EmojiEntry("🤜", "右拳", 3),
        EmojiEntry("👊", "拳头", 3),
        EmojiEntry("✊", "握拳", 3),
        EmojiEntry("🫵", "指向自己", 4),
        EmojiEntry("💅", "从容", 2),
    ],
}

# ─── 背景样式配置 ───────────────────────────────────────────────────────────

@dataclass
class BackgroundStyle:
    bg_color: Tuple[int, int, int, int]       # RGBA
    border_color: Tuple[int, int, int, int]    # RGBA
    shadow_color: Tuple[int, int, int, int]   # RGBA
    radius: int = 40
    border_width: int = 3
    shadow_blur: int = 15

# 按分类设定背景风格
BG_STYLES = {
    "sharp_cold": BackgroundStyle(
        (52, 58, 71, 220), (99, 110, 125, 255), (30, 35, 45, 150),
        radius=40, border_width=3
    ),
    "sharp_warm": BackgroundStyle(
        (68, 51, 51, 220), (155, 99, 99, 255), (50, 30, 30, 150),
        radius=40, border_width=3
    ),
    "sharp_ancestor": BackgroundStyle(
        (74, 63, 53, 220), (140, 110, 80, 255), (50, 40, 25, 150),
        radius=50, border_width=4
    ),
    "sharp_god": BackgroundStyle(
        (60, 50, 80, 220), (150, 130, 200, 255), (40, 30, 60, 150),
        radius=50, border_width=4
    ),
    "empathy": BackgroundStyle(
        (255, 182, 193, 220), (255, 140, 160, 255), (220, 140, 160, 120),
        radius=50, border_width=3
    ),
    "heal": BackgroundStyle(
        (144, 238, 144, 220), (60, 200, 100, 255), (80, 200, 80, 120),
        radius=50, border_width=3
    ),
    "mock": BackgroundStyle(
        (255, 218, 185, 220), (200, 160, 100, 255), (180, 140, 80, 120),
        radius=40, border_width=3
    ),
    "sage": BackgroundStyle(
        (230, 214, 185, 220), (180, 160, 120, 255), (150, 130, 100, 120),
        radius=55, border_width=3
    ),
    "presence": BackgroundStyle(
        (30, 30, 80, 220), (100, 100, 200, 255), (20, 20, 70, 150),
        radius=55, border_width=3
    ),
    "affirmation": BackgroundStyle(
        (255, 215, 0, 220), (255, 180, 0, 255), (200, 160, 0, 150),
        radius=45, border_width=4
    ),
}

# ─── 渲染函数 ───────────────────────────────────────────────────────────────

def _load_font(size: int):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()


def _round_rect(img: Image.Image, radius: int) -> Image.Image:
    """圆角裁剪"""
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    r = radius
    mask_draw.rounded_rectangle([(0, 0), (w - 1, h - 1)], radius=r, fill=255)
    # 四个角再切圆
    result = img.copy()
    result.putalpha(mask)
    return result


def render_emoji_card(char: str, description: str, category: str,
                      kill_power: int, card_size: int = 200) -> Image.Image:
    """渲染单张 emoji 表情包卡片"""

    style = BG_STYLES.get(category, BG_STYLES["heal"])

    # 创建主图像（带 alpha）
    img = Image.new("RGBA", (card_size, card_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ── 绘制圆角背景 ──
    margin = 8
    r = style.radius
    bg_box = [margin, margin, card_size - margin - 1, card_size - margin - 1]

    # 画背景（先画一个大圆再裁）
    bg_img = Image.new("RGBA", (card_size, card_size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg_img)
    bg_draw.rounded_rectangle(bg_box, radius=r, fill=style.bg_color,
                               outline=style.border_color, width=style.border_width)

    # 软阴影效果
    shadow_offset = 6
    shadow_box = [m + shadow_offset for m in bg_box]
    shadow_img = Image.new("RGBA", (card_size, card_size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_draw.rounded_rectangle(shadow_box, radius=r, fill=style.shadow_color)
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=style.shadow_blur))

    # 合成阴影
    img = Image.alpha_composite(img, shadow_img)
    # 合成背景
    img = Image.alpha_composite(img, bg_img)

    draw = ImageDraw.Draw(img)

    # ── 渲染 emoji ──
    font_size = int(card_size * 0.65)
    font = _load_font(font_size)

    # 计算 emoji 位置（居中）
    try:
        bbox = draw.textbbox((0, 0), char, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (card_size - tw) // 2 - bbox[0]
        y = (card_size - th) // 2 - bbox[1] - 5  # 稍微偏上
    except Exception:
        x = y = 10
        tw = th = card_size - 20

    # emoji 放在中上部
    emoji_size = int(card_size * 0.58)
    emoji_font = _load_font(emoji_size)
    try:
        e_bbox = draw.textbbox((0, 0), char, font=emoji_font)
        e_tw = e_bbox[2] - e_bbox[0]
        e_th = e_bbox[3] - e_bbox[1]
        ex = (card_size - e_tw) // 2 - e_bbox[0]
        ey = (card_size - e_th) // 2 - e_bbox[1] - 10
    except Exception:
        ex, ey = 15, 15

    draw.text((ex, ey), char, font=emoji_font, embedded_color=True)

    # ── 底部标注（杀伤力星级）──
    star_text = "★" * kill_power + "☆" * (5 - kill_power)
    star_font = _load_font(20)
    star_bbox = draw.textbbox((0, 0), star_text, font=star_font)
    star_tw = star_bbox[2] - star_bbox[0]
    sx = (card_size - star_tw) // 2
    sy = card_size - 32
    draw.text((sx, sy), star_text, font=star_font, fill=(255, 255, 255, 200))

    return img


def save_emoji_card(img: Image.Image, category: str, char: str,
                     description: str, kill_power: int,
                     index: int) -> Tuple[str, str]:
    """保存 emoji 卡片，返回 (文件路径, sticker_id)"""
    cat_dir = Path(BASE_DIR) / category
    cat_dir.mkdir(parents=True, exist_ok=True)

    # 生成文件名
    hash_val = hashlib.md5(f"{category}{char}{time.time()}{random.random()}".encode()).hexdigest()[:8]
    fname = f"emoji_{category}_{index:03d}_{hash_val}.png"
    fpath = cat_dir / fname

    img.save(str(fpath), "PNG", optimize=True)
    sid = f"{category}_emoji_{index:03d}"

    return str(fpath), sid


# ─── 主生成函数 ─────────────────────────────────────────────────────────────

def generate_all_emojis() -> Tuple[int, Dict[str, int]]:
    """生成所有分类的 emoji 表情包"""
    logger.info("=" * 60)
    logger.info("开始生成 Emoji 表情包，目标：200张（Windows Segoe UI Emoji）")
    logger.info(f"字体文件: {FONT_PATH}")
    logger.info("=" * 60)

    results = {}
    total = 0
    all_stickers = []

    for category, emojis in CATEGORY_EMOJIS.items():
        logger.info(f"\n{'─' * 40}")
        logger.info(f"分类: {category} | 数量: {len(emojis)}")
        logger.info(f"{'─' * 40}")

        count = 0
        for i, entry in enumerate(emojis):
            try:
                img = render_emoji_card(
                    char=entry.char,
                    description=entry.description,
                    category=category,
                    kill_power=entry.kill_power,
                    card_size=200,
                )

                fpath, sid = save_emoji_card(
                    img=img,
                    category=category,
                    char=entry.char,
                    description=entry.description,
                    kill_power=entry.kill_power,
                    index=i + 1,
                )

                all_stickers.append({
                    "sticker_id": sid,
                    "category": category,
                    "file_path": fpath,
                    "char": entry.char,
                    "description": entry.description,
                    "kill_power": entry.kill_power,
                    "source": "windows_emoji",
                    "tags": [category],
                    "width": 200,
                    "height": 200,
                    "added_at": time.time(),
                })

                count += 1
                logger.info(f"  ✅ [{category}] #{i+1:02d} {entry.char} {entry.description} "
                            f"({'★' * entry.kill_power}) -> {Path(fpath).name}")

            except Exception as e:
                logger.warning(f"  ❌ [{category}] #{i+1:02d} {entry.char} 失败: {e}")

        results[category] = count
        total += count

    logger.info(f"\n{'=' * 60}")
    logger.info(f"生成完成！共 {total} 张")
    logger.info(f"保存目录: {BASE_DIR}")
    logger.info("=" * 60)

    return total, results, all_stickers


# ─── 索引更新 ────────────────────────────────────────────────────────────────

def update_sticker_index(all_stickers: List[Dict]) -> int:
    """更新 sticker_index.json"""
    index_path = Path(BASE_DIR) / "sticker_index.json"
    index = {s["sticker_id"]: s for s in all_stickers}

    # 也加载已有的索引（保留本地原有的记录）
    if index_path.exists():
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
            for sid, info in existing.items():
                if sid not in index:
                    index[sid] = info
        except Exception:
            pass

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    logger.info(f"索引已更新，共 {len(index)} 张表情包")
    return len(index)


# ─── 入口 ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    start = time.time()

    # 验证字体文件
    if not os.path.exists(FONT_PATH):
        logger.error(f"字体文件不存在: {FONT_PATH}")
        for candidate in FONT_CANDIDATES[1:]:
            if candidate.exists():
                FONT_PATH = str(candidate)
                logger.info(f"使用备选字体: {candidate}")
                break


    total, results, all_stickers = generate_all_emojis()
    update_sticker_index(all_stickers)

    elapsed = time.time() - start

    logger.info(f"\n🎉 完成！")
    logger.info(f"   生成: {total} 张")
    logger.info(f"   耗时: {elapsed:.1f}s")
    for cat, cnt in results.items():
        logger.info(f"   {cat}: {cnt} 张")
