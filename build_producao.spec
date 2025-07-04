# -*- mode: python ; coding: utf-8 -*-
"""
Especificação PyInstaller para versão de produção
"""

import os
from pathlib import Path

block_cipher = None

# Obter diretório atual
current_dir = Path.cwd()

# Dados a serem incluídos no executável
datas = [
    ('config', 'config'),
    ('gui', 'gui'),
    ('utils', 'utils'),
    ('boletos', 'boletos'),
    ('logs', 'logs'),
    ('env_exemplo.txt', '.'),
    ('config_exemplo.env', '.'),
    ('configurar.bat', '.'),
    ('README_CLIENTE.md', '.'),
    ('requirements.txt', '.'),
    ('README.md', '.'),
    ('README_GUI.md', '.'),
]

# Verificar se os arquivos existem antes de incluí-los
datas = [(src, dst) for src, dst in datas if Path(src).exists()]

# Excluir arquivos que não devem ser incluídos
excluded_files = [
    'boletos_extraidos.csv',
    '*.csv',
    '*.log',
    '*.tmp'
]

# Filtrar dados para excluir arquivos indesejados
filtered_datas = []
for src, dst in datas:
    should_include = True
    for excluded in excluded_files:
        if excluded in src or Path(src).name.endswith('.csv'):
            should_include = False
            break
    if should_include:
        filtered_datas.append((src, dst))

datas = filtered_datas

a = Analysis(
    ['app_producao.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        # Tkinter
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        
        # Selenium
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.chrome',
        'selenium.webdriver.chrome.service',
        'selenium.webdriver.common',
        'selenium.webdriver.common.by',
        'selenium.webdriver.common.keys',
        'selenium.webdriver.common.action_chains',
        'selenium.webdriver.support',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.support.expected_conditions',
        'selenium.webdriver.remote',
        'selenium.webdriver.remote.webdriver',
        'selenium.webdriver.remote.webelement',
        
        # WebDriver Manager
        'webdriver_manager',
        'webdriver_manager.chrome',
        'webdriver_manager.core',
        'webdriver_manager.core.download_manager',
        'webdriver_manager.core.os_manager',
        
        # Pandas e dependências
        'pandas',
        'pandas._libs',
        'pandas._libs.tslibs',
        'pandas.io',
        'pandas.io.excel',
        'pandas.io.excel._openpyxl',
        'pandas.core',
        'pandas.core.api',
        'pandas.core.arrays',
        'pandas.core.computation',
        'pandas.core.dtypes',
        'pandas.core.indexes',
        'pandas.core.internals',
        'pandas.core.reshape',
        'pandas.core.series',
        'pandas.core.window',
        'pandas.io.common',
        'pandas.io.formats',
        'pandas.io.parsers',
        'pandas.io.sql',
        'pandas.plotting',
        'pandas.util',
        
        # OpenPyXL
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.workbook',
        'openpyxl.worksheet',
        
        # Python-dotenv
        'dotenv',
        'dotenv.main',
        'dotenv.parser',
        'dotenv.variables',
        'python-dotenv',
        'dotenv.cli',
        'dotenv.compat',
        
        # PIL/Pillow
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        
        # Outros
        'lxml',
        'lxml.etree',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'beautifulsoup4',
        'bs4',
        'soupsieve',
        
        # Módulos locais
        'config',
        'config.settings',
        'utils',
        'utils.data_processor',
        'utils.license_checker',
        'gui',
        'gui.main_window',
        'webiss_automation',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'unittest',
        'doctest',
        'test',
        'tests',
    ],
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
    name='EmiteNota_Producao',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Com console para debug
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Adicione um ícone aqui se tiver: 'icon.ico'
) 