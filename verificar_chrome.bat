@echo off
chcp 65001 >nul
title Verificar Chrome
color 0E

echo ========================================
echo    VERIFICANDO INSTALACAO DO CHROME
echo ========================================
echo.

echo [1/4] Verificando Chrome no PATH...
where chrome >nul 2>&1
if errorlevel 1 (
    echo ERRO - Chrome nao encontrado no PATH
) else (
    echo OK - Chrome encontrado no PATH
    chrome --version
)

echo.
echo [2/4] Verificando instalacoes comuns do Chrome...

set CHROME_FOUND=0

REM Verificar instalacoes comuns
set CHROME_PATHS=^
"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" ^
"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" ^
"%LOCALAPPDATA%\\Google\\Chrome\\Application\\chrome.exe" ^
"%PROGRAMFILES%\\Google\\Chrome\\Application\\chrome.exe" ^
"%PROGRAMFILES(X86)%\\Google\\Chrome\\Application\\chrome.exe"

for %%p in (%CHROME_PATHS%) do (
    if exist %%p (
        echo OK - Chrome encontrado em: %%p
        set CHROME_FOUND=1
        %%p --version
    )
)

if %CHROME_FOUND%==0 (
    echo ERRO - Chrome nao encontrado em nenhuma localizacao comum
)

echo.
echo [3/4] Verificando registros do Windows...
reg query "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe" /v "" 2>nul
if errorlevel 1 (
    echo ERRO - Chrome nao registrado no Windows
) else (
    echo OK - Chrome registrado no Windows
)

echo.
echo [4/4] Verificando outros navegadores...
echo.

REM Verificar Edge
where msedge >nul 2>&1
if errorlevel 1 (
    echo ERRO - Edge nao encontrado
) else (
    echo OK - Edge encontrado
    msedge --version
)

REM Verificar Firefox
where firefox >nul 2>&1
if errorlevel 1 (
    echo ERRO - Firefox nao encontrado
) else (
    echo OK - Firefox encontrado
    firefox --version
)

echo.
echo ========================================
echo    RESULTADO
echo ========================================
echo.

if %CHROME_FOUND%==1 (
    echo SUCESSO! Chrome esta instalado
    echo.
    echo Para corrigir o problema:
    echo 1. Adicione o Chrome ao PATH do sistema
    echo 2. Ou modifique o codigo para usar o caminho completo
    echo.
    echo Caminhos encontrados:
    for %%p in (%CHROME_PATHS%) do (
        if exist %%p echo - %%p
    )
) else (
    echo PROBLEMA! Chrome nao esta instalado
    echo.
    echo SOLUCAO:
    echo 1. Instale o Google Chrome
    echo 2. Download: https://www.google.com/chrome/
    echo 3. Ou use outro navegador (Edge/Firefox)
)

echo.
pause 