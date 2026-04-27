"""
__all__ = [
    'parse_image',
]

图片解析和OCR模块
"""

import io
from pathlib import Path
from typing import Dict
from ._dv_types import DocumentContent

def parse_image(viewer, path: Path, options: Dict) -> DocumentContent:
    """解析图片"""
    content = DocumentContent(metadata=None)
    
    # 直接读取图片信息
    try:
        from PIL import Image
        img = Image.open(path)
        content.images.append({
            'width': img.width,
            'height': img.height,
            'format': img.format,
            'mode': img.mode
        })
    except ImportError:
        content.warnings.append("未安装Pillow库")
    
    # 执行OCR
    if viewer.enable_ocr:
        ocr_text = _perform_ocr_on_image(viewer, path)
        if ocr_text:
            content.ocr_text = ocr_text
            content.text_content = ocr_text
    
    return content

def _perform_ocr_on_image(viewer, path: Path) -> str:
    """对图片执行OCR"""
    from loguru import logger
    
    ocr = viewer._get_ocr_engine()
    if not ocr:
        return ""
    
    try:
        pytesseract = ocr['pytesseract']
        PIL_Image = ocr['PIL']
        
        img = PIL_Image.open(path)
        # 转换为RGB(处理RGBA等模式)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        text = pytesseract.image_to_string(img, lang='+'.join(viewer.ocr_languages))
        return text
        
    except Exception as e:
        logger.warning(f"图片OCR失败: {e}")
        return ""
