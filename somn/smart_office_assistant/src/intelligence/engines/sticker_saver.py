# -*- coding: utf-8 -*-
"""
__all__ = [
    'delete_sticker',
    'get_stats',
    'get_sticker_saver',
    'list_uploads',
    'save_from_base64',
    'save_from_bytes',
    'save_from_file',
    'to_dict',
]

StickerSaver - 聊天表情包存储服务

接收用户在聊天时发送的图片文件,保存到本地表情包库,
并注册到 StickerArsenal 索引,使后续聊天可以直接使用这些表情包.

功能:
1. 接收图片数据(bytes 或 base64)并保存
2. 自动分类(按文件名/描述词/默认分类)
3. 更新 sticker_index.json 索引
4. 支持 PIL 验证图片格式和尺寸

存储结构:
  assets/stickers/
    user_uploads/          # 用户上传的表情包(新增)
      xxx.png / xxx.jpg ...
    sticker_index.json      # 全量索引(含 user_uploads 条目)
"""

import os
import io
import json
import time
import hashlib
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict

logger = logging.getLogger("sticker_saver")

# ─── 配置 ───────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STICKER_BASE = PROJECT_ROOT / "assets" / "stickers"
UPLOAD_DIR = STICKER_BASE / "user_uploads"
INDEX_PATH = STICKER_BASE / "sticker_index.json"

# 支持的图片格式
IMAGE_FORMATS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# ─── 数据结构 ────────────────────────────────────────────────────────────────

@dataclass
class StickerSaveResult:
    success: bool
    sticker_id: str = ""
    file_path: str = ""
    message: str = ""
    info: Optional[Dict] = None

@dataclass
class StickerEntry:
    """表情包条目(与 StickerArsenal.StickerInfo 结构一致)"""
    sticker_id: str
    category: str          # 分类:user_uploads
    file_path: str
    url: str = ""
    char: str = ""         # emoji字符(用户上传时为空)
    tags: List[str] = field(default_factory=list)
    kill_power: int = 2   # 用户上传默认 2(中等杀伤力)
    description: str = ""
    source: str = "user_upload"
    width: int = 0
    height: int = 0
    added_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

# ─── StickerSaver 核心类 ──────────────────────────────────────────────────────

class StickerSaver:
    """聊天表情包存储服务"""

    def __init__(self):
        self.base_dir = STICKER_BASE
        self.upload_dir = UPLOAD_DIR
        self.index_path = INDEX_PATH
        self._ensure_dirs()
        logger.info(f"[StickerSaver] init完成,上传目录: {self.upload_dir}")

    def _ensure_dirs(self):
        """确保必要目录存在"""
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        if not self.index_path.exists():
            # init空索引
            with open(self.index_path, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

    def _generate_id(self, data: bytes) -> str:
        """根据文件内容generate唯一 ID"""
        return hashlib.md5(data).hexdigest()[:12]

    def _validate_image(self, data: bytes) -> tuple[bool, Optional[tuple[int, int]]]:
        """
        验证图片数据,返回 (是否有效, (宽, 高))
        """
        try:
            from PIL import Image
            img = Image.open(io.BytesIO(data))
            width, height = img.size
            # 过滤极小或极大的图片
            if width < 20 or height < 20 or width > 4096 or height > 4096:
                return False, (width, height)
            return True, (width, height)
        except Exception as e:
            logger.warning(f"[StickerSaver] 图片验证失败: {e}")
            return False, None

    def _detect_format(self, data: bytes) -> Optional[str]:
        """检测图片格式"""
        try:
            from PIL import Image
            img = Image.open(io.BytesIO(data))
            fmt = img.format.lower()
            if fmt == "jpeg":
                return ".jpg"
            return f".{fmt}"
        except Exception:
            # fallback: 根据 magic bytes judge
            if data[:8] == b'\x89PNG\r\n\x1a\n':
                return ".png"
            if data[:2] in (b'\xff\xd8',):
                return ".jpg"
            if data[:6] in (b'GIF87a', b'GIF89a'):
                return ".gif"
            if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
                return ".webp"
            return None

    def _load_index(self) -> Dict[str, Dict]:
        """加载索引"""
        try:
            with open(self.index_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_index(self, data: Dict):
        """保存索引"""
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ── 核心 API ──────────────────────────────────────────────────────────

    def save_from_bytes(
        self,
        data: bytes,
        description: str = "",
        tags: Optional[List[str]] = None,
        kill_power: int = 2,
    ) -> StickerSaveResult:
        """
        从字节数据保存表情包.

        Args:
            data: 图片原始字节
            description: 可选描述(如用户指定了分类/用途)
            tags: 可选标签列表
            kill_power: 杀伤力 1-5,默认 2

        Returns:
            StickerSaveResult
        """
        # 1. 校验大小
        if len(data) > MAX_FILE_SIZE:
            return StickerSaveResult(
                success=False,
                message=f"文件过大({len(data)//1024}KB),最大支持 {MAX_FILE_SIZE//1024//1024}MB"
            )

        # 2. 检测格式
        fmt = self._detect_format(data)
        if not fmt or fmt not in IMAGE_FORMATS:
            return StickerSaveResult(
                success=False,
                message=f"不支持的图片格式: {fmt or '未知'}"
            )

        # 3. 验证图片
        valid, dims = self._validate_image(data)
        if not valid:
            if dims:
                return StickerSaveResult(
                    success=False,
                    message=f"图片尺寸异常: {dims[0]}x{dims[1]}(需在 20-4096 像素之间)"
                )
            return StickerSaveResult(
                success=False,
                message="无法解析为有效图片"
            )

        width, height = dims

        # 4. generate ID 和路径
        sid = self._generate_id(data)
        filename = f"{sid}{fmt}"
        save_path = self.upload_dir / filename

        # 5. 如果文件已存在(ID 碰撞),直接返回已有结果
        if save_path.exists():
            index = self._load_index()
            if sid in index:
                logger.info(f"[StickerSaver] 表情包已存在: {sid}")
                return StickerSaveResult(
                    success=True,
                    sticker_id=sid,
                    file_path=str(save_path),
                    message="该表情包已保存",
                    info=index[sid]
                )

        # 6. 写入文件
        try:
            with open(save_path, "wb") as f:
                f.write(data)
        except Exception as e:
            return StickerSaveResult(
                success=False,
                message=f"文件写入失败: {e}"
            )

        # 7. 构建索引条目
        entry = StickerEntry(
            sticker_id=sid,
            category="user_uploads",
            file_path=str(save_path),
            tags=tags or [],
            kill_power=kill_power,
            description=description,
            width=width,
            height=height,
        )

        # 8. 更新索引
        index = self._load_index()
        index[sid] = entry.to_dict()
        self._save_index(index)

        logger.info(
            f"[StickerSaver] 保存成功: {sid} -> {save_path} "
            f"({width}x{height}, {len(data)//1024}KB)"
        )

        return StickerSaveResult(
            success=True,
            sticker_id=sid,
            file_path=str(save_path),
            message=f"表情包已保存!尺寸 {width}x{height},ID: {sid}",
            info=entry.to_dict()
        )

    def save_from_file(
        self,
        file_path: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        kill_power: int = 2,
    ) -> StickerSaveResult:
        """从本地文件保存表情包"""
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            return self.save_from_bytes(data, description, tags, kill_power)
        except Exception as e:
            return StickerSaveResult(success=False, message=f"读取文件失败: {e}")

    def save_from_base64(
        self,
        b64_str: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        kill_power: int = 2,
    ) -> StickerSaveResult:
        """从 base64 字符串保存表情包(自动处理 data URI)"""
        import base64
        # 去掉 data URI 前缀
        if "," in b64_str:
            b64_str = b64_str.split(",", 1)[1]
        try:
            data = base64.b64decode(b64_str)
            return self.save_from_bytes(data, description, tags, kill_power)
        except Exception as e:
            return StickerSaveResult(success=False, message=f"base64 解析失败: {e}")

    def list_uploads(self) -> List[Dict]:
        """列出所有用户上传的表情包"""
        index = self._load_index()
        return [
            info for info in index.values()
            if info.get("source") == "user_upload" or "user_uploads" in info.get("file_path", "")
        ]

    def delete_sticker(self, sticker_id: str) -> bool:
        """删除指定表情包"""
        index = self._load_index()
        if sticker_id not in index:
            return False

        fpath = index[sticker_id].get("file_path")
        if fpath and Path(fpath).exists():
            try:
                Path(fpath).unlink()
            except Exception as e:
                logger.warning(f"[StickerSaver] 删除文件失败: {e}")

        del index[sticker_id]
        self._save_index(index)
        logger.info(f"[StickerSaver] 已删除: {sticker_id}")
        return True

    def get_stats(self) -> Dict[str, int]:
        """get统计信息"""
        uploads = self.list_uploads()
        return {
            "total_uploads": len(uploads),
            "upload_dir": str(self.upload_dir),
            "index_size": len(self._load_index()),
        }

# ─── 全局单例 ────────────────────────────────────────────────────────────────

_saver_instance: Optional[StickerSaver] = None

def get_sticker_saver() -> StickerSaver:
    global _saver_instance
    if _saver_instance is None:
        _saver_instance = StickerSaver()
    return _saver_instance
