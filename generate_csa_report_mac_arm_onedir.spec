# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata


block_cipher = None

added_files = [
    ( 'templates/*', 'templates' ),
    ( 'assets/*', 'assets' ),
    ( 'modules/*', 'modules' ),
    ( 'modules/reports/*', 'modules/reports' ),
    ( 'VERSION', '.')
    ]
added_files += copy_metadata("laceworksdk")

a = Analysis(
    ['lw_report_gen.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='lw_report_gen',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='lw_report_gen',
)
