# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('data/data.db', 'data'), ('styles/defaultLight/textStyle.qss', 'styles/defaultLight'), ('styles/defaultDark/widgetStyle.qss', 'styles/defaultDark'), ('styles/baseStyle.qss', 'styles'), ('styles/defaultDark/textStyle.qss', 'styles/defaultDark'), ('styles/defaultLight/widgetStyle.qss', 'styles/defaultLight'), ('styles/defaultLight/textStyle.qss', 'styles/defaultLight'), ('styles/defaultDark/widgetStyle.qss', 'styles/defaultDark'), ('styles/baseStyle.qss', 'styles'), ('styles/defaultDark/textStyle.qss', 'styles/defaultDark'), ('styles/defaultLight/widgetStyle.qss', 'styles/defaultLight')],
    hiddenimports=['settingsModel.py'],
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
    [],
    exclude_binaries=True,
    name='KeyTrainer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['data/keyIc.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='KeyTrainer',
)
