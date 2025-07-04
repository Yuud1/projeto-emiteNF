@echo off
chcp 65001 >nul
echo ========================================
echo    Instalando Dependencias
echo ========================================
echo.

echo [1/4] Atualizando pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ❌ Falha ao atualizar pip
    pause
    exit /b 1
)
echo ✅ pip atualizado

echo.
echo [2/4] Instalando dependências básicas...
pip install wheel setuptools
if errorlevel 1 (
    echo ❌ Falha ao instalar wheel/setuptools
    pause
    exit /b 1
)
echo ✅ Dependências básicas instaladas

echo.
echo [3/4] Instalando pandas (versão mais recente)...
pip install pandas --no-cache-dir
if errorlevel 1 (
    echo ⚠️  Tentando instalar pandas via conda-forge...
    pip install pandas --index-url https://pypi.org/simple/ --no-cache-dir
    if errorlevel 1 (
        echo ❌ Falha ao instalar pandas
        echo 💡 Tente: conda install pandas
        pause
        exit /b 1
    )
)
echo ✅ pandas instalado

echo.
echo [4/4] Instalando outras dependências...
pip install selenium webdriver-manager openpyxl python-dotenv requests beautifulsoup4 lxml Pillow pyinstaller
if errorlevel 1 (
    echo ❌ Falha ao instalar algumas dependências
    pause
    exit /b 1
)
echo ✅ Todas as dependências instaladas

echo.
echo ========================================
echo ✅ INSTALAÇÃO CONCLUÍDA!
echo ========================================
echo.
echo 🧪 Execute: python teste_producao.py
echo 🔨 Execute: .\build_completo.bat
echo.
pause 