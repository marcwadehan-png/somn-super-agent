# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# 项目根目录
root_dir = Path(SPECPATH)
src_dir = root_dir / "src"

# 收集所有 Python 文件
added_files = [
    (str(root_dir / "config.yaml"), "."),
    (str(root_dir / "README.md"), "."),
]

# 数据文件
for pattern in ["*.yaml", "*.json", "*.txt", "*.md"]:
    for file in root_dir.glob(pattern):
        added_files.append((str(file), "."))

a = Analysis(
    ['main.py'],
    pathex=[str(root_dir), str(src_dir)],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'docx',
        'pptx',
        'reportlab',
        'chromadb',
        'sentence_transformers',
        'watchdog',
        'loguru',
        'pandas',
        'numpy',
        'sqlalchemy',
        'pydantic',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'tkinter',
        'unittest',
        'pytest',
        'pydoc',
        'email',
        'http',
        'xmlrpc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SmartOffice AI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(root_dir / 'assets' / 'icon.ico') if (root_dir / 'assets' / 'icon.ico').exists() else None,
)

# macOS 应用包
app = BUNDLE(
    exe,
    name='SmartOffice AI.app',
    icon=str(root_dir / 'assets' / 'icon.icns') if (root_dir / 'assets' / 'icon.icns').exists() else None,
    bundle_identifier='com.yourcompany.smartoffice',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': 'True',
    },
)
