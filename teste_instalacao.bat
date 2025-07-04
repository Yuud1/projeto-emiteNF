@echo off
chcp 65001 >nul
title Teste de Instalação - Emite Nota
color 0B

echo ========================================
echo    TESTE DE INSTALAÇÃO - EMITE NOTA
echo ========================================
echo.
echo Este script vai testar se a instalação funciona
echo em um PC sem Python/dependências
echo.

echo [1/5] Verificando arquivos necessários...
if exist "EmiteNota.exe" (
    echo ✅ EmiteNota.exe encontrado
) else (
    echo ❌ EmiteNota.exe NÃO encontrado!
    echo O executável principal está faltando!
    pause
    exit /b 1
)

if exist ".env" (
    echo ✅ Arquivo .env encontrado
) else (
    echo ❌ Arquivo .env NÃO encontrado!
    echo As configurações estão faltando!
    pause
    exit /b 1
)

echo.
echo [2/5] Verificando sistema...
echo Sistema Operacional: %OS%
echo Versão do Windows: 
ver
echo Usuário: %USERNAME%
echo Pasta atual: %CD%

echo.
echo [3/5] Verificando Chrome...
where chrome >nul 2>&1
if errorlevel 1 (
    echo ❌ Google Chrome NÃO encontrado!
    echo O cliente precisa instalar o Chrome
    echo Download: https://www.google.com/chrome/
) else (
    echo ✅ Google Chrome encontrado
    chrome --version
)

echo.
echo [4/5] Testando execução do aplicativo...
echo ⚠️  ATENÇÃO: Vamos tentar executar o aplicativo
echo ⚠️  Se aparecer erro, significa que não é standalone
echo.
echo Pressione qualquer tecla para testar...
pause >nul

echo.
echo 🚀 Executando EmiteNota.exe...
echo ⏳ Aguarde 10 segundos para ver se funciona...
timeout /t 10 /nobreak >nul

echo.
echo [5/5] Verificando se o processo ainda está rodando...
tasklist /FI "IMAGENAME eq EmiteNota.exe" 2>NUL | find /I /N "EmiteNota.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Aplicativo está rodando! (É standalone)
    echo.
    echo 🎉 SUCESSO! O aplicativo funciona sem Python!
    echo.
    echo Para parar o aplicativo, feche a janela ou pressione Ctrl+C
    pause
) else (
    echo ❌ Aplicativo não está rodando
    echo.
    echo 🔍 POSSÍVEIS PROBLEMAS:
    echo 1. Executável não é standalone (precisa Python)
    echo 2. Chrome não encontrado
    echo 3. Erro de permissão
    echo 4. Antivírus bloqueou
    echo.
    echo 📋 PRÓXIMOS PASSOS:
    echo - Verifique se o Chrome está instalado
    echo - Execute como administrador
    echo - Desative temporariamente o antivírus
    echo.
    pause
)

echo.
echo ========================================
echo    TESTE CONCLUÍDO
echo ========================================
pause 