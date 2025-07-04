@echo off
chcp 65001 >nul
echo ========================================
echo    Emite Nota - Configuração Inicial
echo ========================================
echo.

echo 📝 Verificando configurações...
echo.

if exist ".env" (
    echo ✅ Arquivo .env encontrado!
    echo.
    echo 📋 Configurações atuais:
    echo.
    findstr "WEBISS_USERNAME" .env
    findstr "WEBISS_PASSWORD" .env
    echo.
    echo 💡 Para alterar as configurações, edite o arquivo .env
    echo.
) else (
    echo ❌ Arquivo .env não encontrado!
    echo.
    echo 🔧 Criando arquivo de configuração...
    echo.
    if exist "env_exemplo.txt" (
        copy "env_exemplo.txt" ".env" >nul
        echo ✅ Arquivo .env criado a partir do exemplo!
        echo.
        echo 📝 INSTRUÇÕES:
        echo    1. Edite o arquivo .env com suas credenciais do WebISS
        echo    2. Salve o arquivo
        echo    3. Execute o aplicativo
        echo.
        echo 💡 Exemplo de configuração:
        echo    WEBISS_USERNAME=seu_usuario_aqui
        echo    WEBISS_PASSWORD=sua_senha_aqui
        echo.
        echo 🔓 Abrindo arquivo para edição...
        notepad .env
    ) else (
        echo ❌ Arquivo env_exemplo.txt não encontrado!
        echo.
        echo 📝 Crie manualmente um arquivo .env com:
        echo    WEBISS_USERNAME=seu_usuario_aqui
        echo    WEBISS_PASSWORD=sua_senha_aqui
        echo.
    )
)

echo.
echo ========================================
echo ✅ Configuração concluída!
echo ========================================
echo.
echo 🚀 Execute o aplicativo quando estiver pronto!
echo.
pause 