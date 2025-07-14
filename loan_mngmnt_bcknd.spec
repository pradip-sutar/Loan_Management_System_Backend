# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['build.py'],
    pathex=[],
    binaries=[],
    datas=[('template_db\\db.sqlite3', 'template_db'), ('Loan_Management_System_Backend', 'Loan_Management_System_Backend'), ('staticfiles', 'staticfiles')],
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
    name='loan_mngmnt_bcknd',
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
)
