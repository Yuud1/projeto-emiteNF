@echo off
chcp 65001 >nul
echo ========================================
echo    Emite Nota - Build Completo
echo ========================================
echo.

echo [1/6] Executando testes...
python teste_producao.py
if errorlevel 1 (
    echo ❌ Testes falharam! Corrija os problemas antes de continuar.
    pause
    exit /b 1
)
echo ✅ Testes passaram!

echo.
echo [2/6] Verificando ambiente Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo Instale o Python 3.8+ e tente novamente
    pause
    exit /b 1
)
echo ✅ Python encontrado

echo.
echo [3/6] Verificando PyInstaller...
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
echo [4/6] Instalando dependências de produção...
pip install -r requirements_producao.txt
if errorlevel 1 (
    echo ❌ Falha ao instalar dependências
    pause
    exit /b 1
)
echo ✅ Dependências instaladas

echo.
echo [5/6] Compilando aplicação...
echo ⏳ Isso pode demorar alguns minutos...
echo.

pyinstaller build_producao.spec --clean
if errorlevel 1 (
    echo ❌ Falha na compilação!
    pause
    exit /b 1
)

echo ✅ Compilação concluída!

echo.
echo [6/6] Criando instalador...
python installer_creator.py
if errorlevel 1 (
    echo ❌ Falha ao criar instalador!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ BUILD COMPLETO CONCLUÍDO!
echo ========================================
echo.
echo 📁 Arquivos gerados:
echo    - dist/EmiteNota_Producao.exe
echo    - installer/EmiteNota_Installer_*.zip
echo.
echo 📋 Próximos passos:
echo    1. Teste o executável: dist/EmiteNota_Producao.exe
echo    2. Distribua o instalador: installer/EmiteNota_Installer_*.zip
echo    3. Configure as credenciais no arquivo .env
echo.
echo 💡 Dica: Sempre teste antes de distribuir!
echo.
pause 