#!/usr/bin/env python3
"""
Tesseract OCR 安装检查与配置脚本

使用方法:
    python tesseract_install_check.py

功能:
    1. 检查Tesseract是否已安装
    2. 验证语言包是否完整
    3. 配置Python OCR接口
"""

import sys
import os

def main():
    print("=" * 60)
    print("Tesseract OCR 安装检查")
    print("=" * 60)
    
    # 1. 检查Python包
    print("\n[1/3] 检查Python依赖...")
    try:
        import pytesseract
        print(f"    ✅ pytesseract 已安装: {pytesseract.__version__}")
    except ImportError:
        print("    ❌ pytesseract 未安装")
        print("    请运行: pip install pytesseract pillow")
        return False
    
    try:
        from PIL import Image
        print(f"    ✅ Pillow 已安装: {Image.__version__}")
    except ImportError:
        print("    ❌ Pillow 未安装")
        print("    请运行: pip install pillow")
        return False
    
    # 2. 检查Tesseract引擎
    print("\n[2/3] 检查Tesseract引擎...")
    try:
        version = pytesseract.get_tesseract_version()
        print(f"    ✅ Tesseract 已安装: v{version}")
    except Exception as e:
        print(f"    ❌ Tesseract引擎未找到: {e}")
        print()
        print("    请手动安装:")
        print("    1. 下载: https://github.com/UB-Mannheim/tesseract/releases")
        print("    2. 下载 tesseract-ocr-w64-setup-5.5.0.20241111.exe")
        print("    3. 运行安装，勾选中文语言包 (chi_sim)")
        print("    4. 重启此终端")
        return False
    
    # 3. 检查语言包
    print("\n[3/3] 检查语言包...")
    try:
        langs = pytesseract.get_languages()
        print(f"    已安装语言: {', '.join(langs)}")
        
        if 'chi_sim' in langs:
            print("    ✅ 中文简体语言包已安装")
        else:
            print("    ⚠️ 警告: 未检测到中文简体语言包 (chi_sim)")
            print("    图片中的中文可能无法识别")
    except Exception as e:
        print(f"    ⚠️ 无法获取语言包列表: {e}")
    
    print("\n" + "=" * 60)
    print("检查完成!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
