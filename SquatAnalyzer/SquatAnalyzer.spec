# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/app.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('src/gui/styles.qss', 'gui'),
        ('C:\Python311\Lib\site-packages\mediapipe\modules/pose_landmark', 'mediapipe/modules/pose_landmark'),
        ('C:/Python311/Lib/site-packages/mediapipe/modules/pose_detection', 'mediapipe/modules/pose_detection'),
    ],
    hiddenimports=[
        'mediapipe.python.solutions.pose'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SquatAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)
