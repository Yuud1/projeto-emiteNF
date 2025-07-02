# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app_robust.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('boletos', 'boletos'),
        ('logs', 'logs'),
        ('.env', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.chrome',
        'selenium.webdriver.common',
        'selenium.webdriver.support',
        'pandas',
        'openpyxl',
        'python-dotenv',
        'webdriver_manager',
        'PIL',
        'lxml',
        'requests',
        'beautifulsoup4',
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
    name='EmiteNota',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sem console para aplicação GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
