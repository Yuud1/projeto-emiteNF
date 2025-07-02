@echo off
echo ========================================
echo    Emite Nota - Automação WebISS
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Instale o Python 3.8 ou superior
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verifica se o arquivo .env existe
if not exist ".env" (
    echo AVISO: Arquivo .env não encontrado!
    echo.
    echo Para configurar:
    echo 1. Copie o arquivo env_example.txt para .env
    echo 2. Edite o arquivo .env com suas credenciais
    echo.
    echo Exemplo:
    echo   copy env_example.txt .env
    echo.
    pause
    exit /b 1
)

REM Instala dependências se necessário
if not exist "venv" (
    echo Instalando dependências...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERRO: Falha ao instalar dependências
        pause
        exit /b 1
    )
)

REM Executa o programa
echo Iniciando Emite Nota...
python run.py

pause 