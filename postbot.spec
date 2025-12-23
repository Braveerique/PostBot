# -*- mode: python ; coding: utf-8 -*-

# PyInstaller spec file for PostBot
# This creates a standalone executable that includes all dependencies

block_cipher = None

a = Analysis(
    ['postbot.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env.example', '.'),
        ('README.md', '.'),
        ('QUICKSTART.md', '.'),
    ],
    hiddenimports=[
        'tweepy',
        'atproto',
        'requests', 
        'googleapiclient.discovery',
        'google.auth.transport.requests',
        'google.oauth2.credentials',
        'google_auth_oauthlib.flow',
        'psutil',
        'schedule',
        'python-dotenv',
        'colorama',
        'obsws_python',
        'websocket',
        'json',
        'os',
        'logging',
        'time',
        'datetime',
        'sys',
        'threading'
    ],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PostBot',
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
    icon='icon.ico'  # Optional: add an icon file
)