# -*- mode: python ; coding: utf-8 -*-
# ClassMate.spec — PyInstaller 빌드 설정
#
# 사용법 (Windows, 빌드 PC에서):
#   python -m PyInstaller ClassMate.spec --noconfirm --clean
#
# 결과:
#   dist/ClassMate/ClassMate.exe
#
# 현재 설정: onedir 모드 (--onedir)
#   → dist/ClassMate/ 폴더째로 배포
#   → onefile보다 시작이 빠르고 WebEngine 호환성 좋음

from pathlib import Path
from PyInstaller.utils.hooks import (
    collect_data_files,
    collect_dynamic_libs,
    collect_submodules,
)

ROOT = Path(SPEC).parent  # spec 파일이 있는 폴더 = 앱 루트

# ── 번들에 포함할 데이터 파일 ─────────────────────────────────────────
datas = [
    # (원본 경로, 번들 내 대상 폴더)
    (str(ROOT / "ui"), "ui"),
    (str(ROOT / "ClassMate.ico"), "."),
    (str(ROOT / "ClassMate_Guide.html"), "."),
]

# PyQt6 / QtWebEngine 런타임 리소스 포함
# - resources/
# - translations/
# - qt.conf 등
# - WebEngine 관련 DLL/실행 파일
# 기존 hiddenimports만으로는 QtWebEngineWidgets import 단계에서 DLL 누락이 날 수 있다.
datas += collect_data_files("PyQt6")
binaries = collect_dynamic_libs("PyQt6")

# ── Hidden imports ─────────────────────────────────────────────────────
hidden_imports = [
    "PyQt6.QtCore",
    "PyQt6.QtGui",
    "PyQt6.QtWidgets",
    "PyQt6.QtWebChannel",
    "PyQt6.QtWebEngineCore",
    "PyQt6.QtWebEngineWidgets",
    "openpyxl",
    "openpyxl.cell._writer",
    "openpyxl.styles.stylesheet",
    "openpyxl.reader.excel",
    "openpyxl.writer.excel",
]

# WebEngine 내부 의존 모듈을 넉넉하게 포함
hidden_imports += collect_submodules("PyQt6.QtWebEngineCore")
hidden_imports += collect_submodules("PyQt6.QtWebEngineWidgets")
hidden_imports += collect_submodules("PyQt6.QtWebChannel")

# 중복 제거 + 정렬
hidden_imports = sorted(set(hidden_imports))


a = Analysis(
    [str(ROOT / "app.py")],
    pathex=[str(ROOT)],
    binaries=binaries,
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
