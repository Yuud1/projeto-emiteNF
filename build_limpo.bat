@echo off
chcp 65001 >nul
echo ========================================
echo    Emite Nota - Build Limpo
echo ========================================
echo.

echo [1/5] Limpando arquivos desnecessários...
echo Removendo CSV antigo da pasta dist...
if exist "dist\boletos_extraidos.csv" (
    del "dist\boletos_extraidos.csv"
    echo ✅ CSV removido
) else (
    echo ℹ️ Nenhum CSV encontrado para remover
)

echo.
echo [2/5] Verificando ambiente Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo Instale o Python 3.8+ e tente novamente
    pause
    exit /b 1
)
echo ✅ Python encontrado

echo.
echo [3/5] Verificando PyInstaller...
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
echo [4/5] Instalando dependências de produção...
pip install -r requirements_producao.txt
if errorlevel 1 (
    echo ❌ Falha ao instalar dependências
    pause
    exit /b 1
)
echo ✅ Dependências instaladas

echo.
echo [5/5] Compilando aplicação...
echo ⏳ Isso pode demorar alguns minutos...
echo.

pyinstaller build_producao.spec --clean
if errorlevel 1 (
    echo ❌ Falha na compilação!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ BUILD LIMPO CONCLUÍDO!
echo ========================================
echo.
echo 📁 Arquivo gerado:
echo    - dist/EmiteNota_Producao.exe
echo.
echo 📋 Próximos passos:
echo    1. Teste o executável: dist/EmiteNota_Producao.exe
echo    2. Configure as credenciais no arquivo .env
echo.
echo 💡 Dica: Este build não inclui dados antigos!
echo.
pause 