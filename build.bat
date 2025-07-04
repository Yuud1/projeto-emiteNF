@echo off
chcp 65001 >nul
echo ========================================
echo    Emite Nota - Build de Producao
echo ========================================
echo.

echo [1/5] Verificando ambiente Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado!
    echo Instale o Python 3.8+ e tente novamente
    pause
    exit /b 1
)
echo ✅ Python encontrado

echo.
echo [2/5] Verificando PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Falha ao instalar PyInstaller
        pause
        exit /b 1
    )
)
echo ✅ PyInstaller encontrado

echo.
echo [3/5] Verificando dependencias...
if not exist requirements.txt (
    echo ❌ Arquivo requirements.txt nao encontrado!
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Falha ao instalar dependencias
    pause
    exit /b 1
)
echo ✅ Dependencias instaladas

echo.
echo [4/5] Verificando arquivos necessarios...
if not exist app_producao.py (
    echo ❌ Arquivo app_producao.py nao encontrado!
    pause
    exit /b 1
)

if not exist build_producao.spec (
    echo ❌ Arquivo build_producao.spec nao encontrado!
    pause
    exit /b 1
)
echo ✅ Arquivos encontrados

echo.
echo [5/5] Compilando aplicacao...
echo ⏳ Isso pode demorar alguns minutos...
echo.

pyinstaller build_producao.spec --clean
if errorlevel 1 (
    echo ❌ Falha na compilacao!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ COMPILACAO CONCLUIDA COM SUCESSO!
echo ========================================
echo.
echo 📁 Executavel criado em: dist/EmiteNota_Producao.exe
echo.
echo 📋 Para distribuir:
echo    1. Copie a pasta 'dist' completa
echo    2. Configure o arquivo .env com as credenciais
echo    3. Execute EmiteNota_Producao.exe
echo.
echo 💡 Dica: Teste o executavel antes de distribuir!
echo.
pause 