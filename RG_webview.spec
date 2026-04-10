# -*- mode: python ; coding: utf-8 -*-
# RG_webview.spec — PyInstaller 빌드 설정 (호환용)
#
# 사용법 (Windows, 빌드 PC에서):
#   pip install pyinstaller
#   pyinstaller RG_webview.spec
#
# 결과:
#   dist/ClassMate/ClassMate.exe
#
# 현재 설정: onedir 모드 (--onedir)
#   → dist/ClassMate/ 폴더째로 배포
#   → onefile보다 시작이 빠르고 WebEngine 호환성 좋음

from pathlib import Path

ROOT = Path(SPEC).parent  # spec 파일이 있는 폴더 = 앱 루트

# ── 번들에 포함할 데이터 파일 ─────────────────────────────────────────
datas = [
    # (원본 경로,  번들 내 대상 폴더)
    (str(ROOT / "ui"), "ui"),                        # index.html, *.js, fonts/
    (str(ROOT / "ClassMate.ico"), "."),              # 런타임 window/taskbar icon 로드용
    (str(ROOT / "ClassMate_Guide.html"), "."),       # 사용자 가이드
]

# ── Hidden imports ─────────────────────────────────────────────────────
hidden_imports = [
    "PyQt6.QtWebEngineWidgets",
    "PyQt6.QtWebEngineCore",
    "PyQt6.QtWebChannel",
    "PyQt6.QtCore",
    "PyQt6.QtWidgets",
    "PyQt6.QtGui",
    "openpyxl",
    "openpyxl.cell._writer",
    "openpyxl.styles.stylesheet",
    "openpyxl.reader.excel",
    "openpyxl.writer.excel",
]

a = Analysis(
    [str(ROOT / "app.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter", "matplotlib", "numpy", "pandas",
        "scipy", "PIL", "cv2", "PyQt5",
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ClassMate",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="ClassMate.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="ClassMate",
)
