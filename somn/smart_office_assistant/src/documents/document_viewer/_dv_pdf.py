"""
__all__ = [
    'get_pdf_page_count',
    'parse_pdf',
]

PDF解析模块
"""

import io
from pathlib import Path
from typing import Dict, Optional
from ._dv_types import DocumentContent, DocumentMetadata, DocumentType

def parse_pdf(viewer, path: Path, options: Dict) -> DocumentContent:
    """解析PDF文档"""
    max_pages = options.get('max_pages', None)
    extract_images = options.get('extract_images', True)
    
    content = DocumentContent(metadata=None)
    
    try:
        # 尝试使用PyMuPDF (fitz)
        import fitz
        doc = fitz.open(path)
        
        for page_num in range(len(doc)):
            if max_pages and page_num >= max_pages:
                break
            
            page = doc[page_num]
            text = page.get_text()
            
            if text.strip():
                content.pages.append(text)
                content.text_content += text + "\n\n"
            
            # 提取图片
            if extract_images:
                image_list = page.get_images()
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    content.images.append({
                        'page': page_num + 1,
                        'index': img_index,
                        'ext': base_image['ext'],
                        'size': len(base_image['image']),
                        'width': base_image['width'],
                        'height': base_image['height']
                    })
            
            # 检查是否为扫描PDF(无文字)
            if not text.strip() and image_list:
                content.warnings.append(f"第{page_num + 1}页可能是扫描页,建议使用OCR")
        
        doc.close()
        
    except ImportError:
        # 回退到PyPDF2
        try:
            import PyPDF2
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                total_pages = len(reader.pages)
                
                for i in range(min(total_pages, max_pages or 9999)):
                    page = reader.pages[i]
                    text = page.extract_text()
                    content.pages.append(text)
                    content.text_content += text + "\n\n"
        except ImportError:
            content.warnings.append("未安装PDF解析库,建议安装PyMuPDF或PyPDF2")
    
    # 检测是否需要OCR (图片型PDF)
    if not content.text_content.strip() and content.images:
        content.warnings.append("此PDF可能是纯图片格式,已启用OCRrecognize")
        ocr_result = _perform_ocr_on_pdf(viewer, path)
        if ocr_result:
            content.ocr_text = ocr_result
    
    return content

def _perform_ocr_on_pdf(viewer, path: Path) -> str:
    """对PDF执行OCR"""
    from loguru import logger
    
    ocr = viewer._get_ocr_engine()
    if not ocr:
        return ""
    
    try:
        import fitz
        pytesseract = ocr['pytesseract']
        PIL_Image = ocr['PIL']
        
        doc = fitz.open(path)
        all_text = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            # 将页面渲染为图片
            mat = fitz.Matrix(2, 2)  # 2x放大以提高OCR精度
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")
            
            img = PIL_Image.open(io.BytesIO(img_bytes))
            text = pytesseract.image_to_string(img, lang='+'.join(viewer.ocr_languages))
            all_text.append(f"[第{page_num + 1}页]\n{text}")
        
        doc.close()
        return "\n\n".join(all_text)
        
    except Exception as e:
        logger.warning(f"OCR处理失败: {e}")
        return ""

def get_pdf_page_count(path: Path) -> int:
    """获取PDF页数"""
    try:
        import PyPDF2
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return len(reader.pages)
    except Exception:
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(path)
            count = len(doc)
            doc.close()
            return count
        except Exception:
            return 0
