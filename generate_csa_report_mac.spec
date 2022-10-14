# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['generate_csa_report.py'],
    pathex=[],
    binaries=[],
    datas=[],
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
a.datas += Tree("reports", "reports")
a.datas += Tree("graphics", "graphics")
a.datas += Tree("providers", "providers")
a.datas += Tree("transformers", "transformers")
a.datas += Tree("assets", "assets")
def get_datapane_path():
    import datapane
    datapane_path = datapane.__path__[0]
    return datapane_path


dict_tree = Tree(get_datapane_path(), prefix='datapane', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'datapane' not in x[0], a.binaries)
def get_orderedmultidict_path():
    import orderedmultidict
    orderedmultidict_path = orderedmultidict.__path__[0]
    return orderedmultidict_path


dict_tree = Tree(get_orderedmultidict_path(), prefix='orderedmultidict', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'orderedmultidict' not in x[0], a.binaries)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='generate_csa_report_mac',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
