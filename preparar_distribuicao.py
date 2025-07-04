#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preparador de Distribuição - Emite Nota
Cria o pacote final para distribuição ao cliente
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def preparar_distribuicao():
    """Prepara o pacote final para distribuição"""
    
    print("📦 Preparando distribuição para o cliente...")
    
    # Verificar se o executável existe
    exe_path = Path("dist/EmiteNota_Simples.exe")
    if not exe_path.exists():
        # Tentar outros nomes possíveis
        exe_path = Path("dist/EmiteNota_Producao.exe")
    if not exe_path.exists():
        # Listar arquivos na pasta dist
        dist_files = list(Path("dist").glob("*.exe"))
        if dist_files:
            exe_path = dist_files[0]
            print(f"📁 Usando executável: {exe_path}")
        else:
            print("❌ Nenhum executável encontrado na pasta dist!")
            print("Execute primeiro: python -m PyInstaller build_simples.spec --clean")
            return False
    if not exe_path.exists():
        print("❌ Executável não encontrado!")
        print("Execute primeiro: python -m PyInstaller build_simples.spec --clean")
        return False
    
    # Criar pasta de distribuição
    dist_dir = Path("distribuicao_cliente")
    dist_dir.mkdir(exist_ok=True)
    
    # Nome do arquivo de distribuição
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"EmiteNota_Cliente_{timestamp}.zip"
    zip_path = dist_dir / zip_name
    
    print(f"📁 Criando: {zip_path}")
    
    # Criar arquivo ZIP de distribuição
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # Adicionar executável
        zipf.write(exe_path, "EmiteNota.exe")
        
        # Adicionar arquivo .env com URL correta
        env_content = """# Configurações do WebISS
WEBISS_URL=https://palmasto.webiss.com.br
WEBISS_USERNAME=seu_usuario_aqui
WEBISS_PASSWORD=sua_senha_aqui

# Configurações do Chrome
HEADLESS_MODE=False
CHROME_TIMEOUT=30
CHROME_IMPLICIT_WAIT=10

# Configurações da aplicação
DEBUG_MODE=False
LOG_LEVEL=INFO
"""
        zipf.writestr(".env", env_content)
        
        # Adicionar pastas necessárias
        pastas = ['boletos', 'logs', 'config']
        for pasta in pastas:
            if Path(pasta).exists():
                for root, dirs, files in os.walk(pasta):
                    for file in files:
                        file_path = Path(root) / file
                        arc_name = str(file_path)
                        zipf.write(file_path, arc_name)
        
        # Adicionar arquivo de instruções
        instrucoes = """EMITE NOTA - INSTRUÇÕES DE USO
===============================================

🚀 COMO USAR:
1. Extraia todos os arquivos desta pasta
2. Execute TESTAR.bat para verificar se tudo funciona
3. Configure suas credenciais no arquivo .env
4. Execute EmiteNota.exe
5. Siga os passos na interface

🧪 TESTE INICIAL:
- Execute TESTAR.bat primeiro
- Este script verifica se tudo está funcionando
- Se der erro, siga as instruções na tela

⚙️ CONFIGURAÇÃO:
- Abra o arquivo .env com o Bloco de Notas
- Configure suas credenciais do WebISS:
  WEBISS_USERNAME=seu_usuario_real
  WEBISS_PASSWORD=sua_senha_real

📁 PASTAS:
- boletos/    = Coloque os PDFs dos boletos aqui
- logs/       = Logs da aplicação (para suporte)
- config/     = Configurações do sistema

🔧 REQUISITOS:
- Windows 10 ou superior
- Google Chrome instalado
- Conexão com internet

❓ PROBLEMAS?
- Execute TESTAR.bat para diagnóstico
- Verifique se o Chrome está instalado
- Confirme suas credenciais no .env
- Verifique os logs na pasta logs/

📞 SUPORTE:
- Email: suporte@empresa.com
- Telefone: (11) 99999-9999

⚠️ IMPORTANTE:
- Não compartilhe o arquivo .env
- Faça backup dos dados importantes
- Mantenha o Chrome atualizado

© 2024 Empresa - Todos os direitos reservados
"""
        zipf.writestr("INSTRUCOES.txt", instrucoes)
        
        # Adicionar script de teste
        test_script = """@echo off
chcp 65001 >nul
title Teste de Instalacao - Emite Nota
color 0B

echo ========================================
echo    TESTE DE INSTALACAO - EMITE NOTA
echo ========================================
echo.
echo Este script vai testar se a instalacao funciona
echo em um PC sem Python/dependencias
echo.

echo [1/5] Verificando arquivos necessarios...
if exist "EmiteNota.exe" (
    echo OK - EmiteNota.exe encontrado
) else (
    echo ERRO - EmiteNota.exe NAO encontrado!
    echo O executavel principal esta faltando!
    pause
    exit /b 1
)

if exist ".env" (
    echo OK - Arquivo .env encontrado
) else (
    echo ERRO - Arquivo .env NAO encontrado!
    echo As configuracoes estao faltando!
    pause
    exit /b 1
)

echo.
echo [2/5] Verificando sistema...
echo Sistema Operacional: %OS%
echo Versao do Windows: 
ver
echo Usuario: %USERNAME%
echo Pasta atual: %CD%

echo.
echo [3/5] Verificando Chrome...
set CHROME_FOUND=0

REM Verificar Chrome no PATH
where chrome >nul 2>&1
if not errorlevel 1 (
    echo OK - Chrome encontrado no PATH
    chrome --version
    set CHROME_FOUND=1
)

REM Verificar instalacoes comuns se nao encontrou no PATH
if %CHROME_FOUND%==0 (
    if exist "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" (
        echo OK - Chrome encontrado em Program Files
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --version
        set CHROME_FOUND=1
    ) else if exist "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" (
        echo OK - Chrome encontrado em Program Files (x86)
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" --version
        set CHROME_FOUND=1
    ) else if exist "%LOCALAPPDATA%\\Google\\Chrome\\Application\\chrome.exe" (
        echo OK - Chrome encontrado em AppData
        "%LOCALAPPDATA%\\Google\\Chrome\\Application\\chrome.exe" --version
        set CHROME_FOUND=1
    )
)

if %CHROME_FOUND%==0 (
    echo ERRO - Google Chrome NAO encontrado!
    echo O cliente precisa instalar o Chrome
    echo Download: https://www.google.com/chrome/
) else (
    echo OK - Chrome esta disponivel para o aplicativo
)

echo.
echo [4/5] Testando execucao do aplicativo...
echo ATENCAO: Vamos tentar executar o aplicativo
echo Se aparecer erro, significa que nao e standalone
echo.
echo Pressione qualquer tecla para testar...
pause >nul

echo.
echo Executando EmiteNota.exe...
echo Aguarde 10 segundos para ver se funciona...
timeout /t 10 /nobreak >nul

echo.
echo [5/5] Verificando se o processo ainda esta rodando...
tasklist /FI "IMAGENAME eq EmiteNota.exe" 2>NUL | find /I /N "EmiteNota.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo OK - Aplicativo esta rodando! (E standalone)
    echo.
    echo SUCESSO! O aplicativo funciona sem Python!
    echo.
    echo Para parar o aplicativo, feche a janela ou pressione Ctrl+C
    pause
) else (
    echo ERRO - Aplicativo nao esta rodando
    echo.
    echo POSSIVEIS PROBLEMAS:
    echo 1. Executavel nao e standalone (precisa Python)
    echo 2. Chrome nao encontrado
    echo 3. Erro de permissao
    echo 4. Antivirus bloqueou
    echo.
    echo PROXIMOS PASSOS:
    echo - Verifique se o Chrome esta instalado
    echo - Execute como administrador
    echo - Desative temporariamente o antivirus
    echo.
    pause
)

echo.
echo ========================================
echo    TESTE CONCLUIDO
echo ========================================
pause
"""
        zipf.writestr("TESTAR.bat", test_script)
        
        # Adicionar script de instalação
        install_script = """@echo off
chcp 65001 >nul
title Emite Nota - Instalador
color 0A

echo ========================================
echo    Emite Nota - Instalador
echo ========================================
echo.

echo ATENCAO: Este instalador vai organizar os arquivos
echo Escolha a opcao:
echo.
echo 1. Desktop - Copia para uma nova pasta no Desktop
echo 2. Pasta atual - Organiza na pasta atual (mais seguro)
echo.
set /p choice="Digite 1 ou 2: "

if "%choice%"=="1" (
    echo.
    echo [1/4] Verificando sistema...
    if not exist "%USERPROFILE%\\Desktop" (
        echo AVISO - Desktop nao encontrado (OneDrive/WSL)
        echo Instalando na pasta atual...
        set INSTALL_DIR=%CD%
    ) else (
        echo OK - Desktop encontrado
        set INSTALL_DIR=%USERPROFILE%\\Desktop\\EmiteNota
        echo Pasta de destino: %INSTALL_DIR%
    )
) else (
    echo.
    echo [1/4] Instalando na pasta atual...
    set INSTALL_DIR=%CD%
    echo Pasta de destino: %INSTALL_DIR%
)

echo.
echo [2/4] Criando pasta de instalacao...
if exist "%INSTALL_DIR%" (
    if not "%INSTALL_DIR%"=="%CD%" (
        echo AVISO - Pasta ja existe no Desktop
        echo Instalando na pasta atual para evitar conflitos...
        set INSTALL_DIR=%CD%
    )
) else (
    if not "%INSTALL_DIR%"=="%CD%" (
        mkdir "%INSTALL_DIR%" 2>nul
        if errorlevel 1 (
            echo ERRO - Erro ao criar pasta no Desktop
            echo Instalando na pasta atual...
            set INSTALL_DIR=%CD%
        )
    )
)

echo OK - Pasta de instalacao: %INSTALL_DIR%

echo.
echo [3/4] Copiando arquivos...
echo Aguarde...

set FILES_COPIED=0
set TOTAL_FILES=0

REM Contar arquivos
for %%f in (*) do (
    if not "%%f"=="INSTALAR.bat" (
        if not "%%f"=="INSTRUCOES.txt" (
            set /a TOTAL_FILES+=1
        )
    )
)

REM Copiar arquivos
for %%f in (*) do (
    if not "%%f"=="INSTALAR.bat" (
        if not "%%f"=="INSTRUCOES.txt" (
            if not "%INSTALL_DIR%"=="%CD%" (
                copy "%%f" "%INSTALL_DIR%\\" >nul 2>&1
                if errorlevel 1 (
                    echo ERRO - Erro ao copiar: %%f
                ) else (
                    set /a FILES_COPIED+=1
                    echo OK - Copiado: %%f
                )
            ) else (
                echo OK - Arquivo ja esta no local correto: %%f
                set /a FILES_COPIED+=1
            )
        )
    )
)

echo.
echo [4/4] Criando pastas necessarias...

REM Criar pastas se nao existirem
if not exist "%INSTALL_DIR%\\config" (
    mkdir "%INSTALL_DIR%\\config" 2>nul
    echo OK - Pasta config criada
)
if not exist "%INSTALL_DIR%\\boletos" (
    mkdir "%INSTALL_DIR%\\boletos" 2>nul
    echo OK - Pasta boletos criada
)
if not exist "%INSTALL_DIR%\\logs" (
    mkdir "%INSTALL_DIR%\\logs" 2>nul
    echo OK - Pasta logs criada
)

echo.
echo ========================================
echo OK - INSTALACAO CONCLUIDA!
echo ========================================
echo.
if not "%INSTALL_DIR%"=="%CD%" (
    echo Aplicacao instalada em: %INSTALL_DIR%
    echo Arquivos copiados: %FILES_COPIED%/%TOTAL_FILES%
) else (
    echo Aplicacao pronta na pasta atual
    echo Arquivos verificados: %FILES_COPIED%/%TOTAL_FILES%
)
echo Para usar: Execute EmiteNota.exe
echo.
echo IMPORTANTE: Configure suas credenciais!
echo Abra o arquivo .env e configure:
echo    - WEBISS_USERNAME=seu_usuario
echo    - WEBISS_PASSWORD=sua_senha
echo.
echo Dica: Leia o arquivo INSTRUCOES.txt
echo.
echo Pressione qualquer tecla para abrir a pasta...
pause >nul

REM Abrir a pasta de instalacao
explorer "%INSTALL_DIR%"

echo.
echo Instalacao finalizada! Pasta aberta.
echo.
pause
"""
        zipf.writestr("INSTALAR.bat", install_script)
    
    print(f"✅ Distribuição criada: {zip_path}")
    print(f"📁 Tamanho: {zip_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    return True

def main():
    """Função principal"""
    try:
        if preparar_distribuicao():
            print("\n🎉 DISTRIBUIÇÃO PRONTA!")
            print("📦 Arquivo criado em: distribuicao_cliente/")
            print("\n📋 Para enviar ao cliente:")
            print("   1. Envie o arquivo ZIP por email/pendrive")
            print("   2. Instrua o cliente a extrair e executar INSTALAR.bat")
            print("   3. Configure as credenciais no arquivo .env")
            print("   4. Use a aplicação!")
        else:
            print("\n❌ Falha ao criar distribuição")
    except Exception as e:
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    main() 