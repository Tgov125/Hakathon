# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Crazy_Blob.py'],
    pathex=[],
    binaries=[],
    datas=[('assets\\Icon.png', 'assets'), ('assets\\The_map.png', 'assets'), ('assets\\Lore_page.png', 'assets'), ('assets\\Victory_screen.png', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Crazy_Blob',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\Icon.ico'],
)
