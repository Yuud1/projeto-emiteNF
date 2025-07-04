#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criador de Instalador para Emite Nota
Gera um instalador simples para Windows
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_installer():
    """Cria um instalador simples para Windows"""
    
    print("🔧 Criando instalador para Emite Nota...")
    
    # Verificar se o executável existe
    exe_path = Path("dist/EmiteNota_Producao.exe")
    if not exe_path.exists():
        print("❌ Executável não encontrado!")
        print("Execute primeiro: build.bat")
        return False
    
    # Criar pasta do instalador
    installer_dir = Path("installer")
    installer_dir.mkdir(exist_ok=True)
    
    # Nome do arquivo de instalação
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    installer_name = f"EmiteNota_Installer_{timestamp}.zip"
    installer_path = installer_dir / installer_name
    
    print(f"📦 Criando: {installer_path}")
    
    # Criar arquivo ZIP do instalador
    with zipfile.ZipFile(installer_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # Adicionar executável
        zipf.write(exe_path, "EmiteNota_Producao.exe")
        
        # Adicionar arquivos de configuração
        config_files = [
            "config/",
            "boletos/",
            "logs/",
            ".env",
            "env_example.txt",
            "README_PRODUCAO.md"
        ]
        
        for file_path in config_files:
            path = Path(file_path)
            if path.exists():
                if path.is_dir():
                    # Adicionar pasta completa
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            file_full_path = Path(root) / file
                            arc_name = str(file_full_path)
                            zipf.write(file_full_path, arc_name)
                else:
                    # Adicionar arquivo
                    zipf.write(path, path.name)
        
        # Adicionar script de instalação
        install_script = create_install_script()
        zipf.writestr("INSTALAR.bat", install_script)
        
        # Adicionar README do instalador
        readme_content = create_installer_readme()
        zipf.writestr("LEIA_PRIMEIRO.txt", readme_content)
    
    print(f"✅ Instalador criado: {installer_path}")
    print(f"📁 Tamanho: {installer_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    return True

def create_install_script():
    """Cria script de instalação para Windows"""
    
    script = """@echo off
chcp 65001 >nul
echo ========================================
echo    Emite Nota - Instalador
echo ========================================
echo.

echo [1/4] Verificando sistema...
if not exist "%USERPROFILE%\\Desktop" (
    echo ❌ Desktop não encontrado!
    pause
    exit /b 1
)
echo ✅ Sistema verificado

echo.
echo [2/4] Criando pasta de instalação...
set INSTALL_DIR=%USERPROFILE%\\Desktop\\EmiteNota
if exist "%INSTALL_DIR%" (
    echo ⚠️  Pasta já existe. Removendo...
    rmdir /s /q "%INSTALL_DIR%"
)
mkdir "%INSTALL_DIR%"
echo ✅ Pasta criada: %INSTALL_DIR%

echo.
echo [3/4] Extraindo arquivos...
echo ⏳ Aguarde...

REM Extrair todos os arquivos
for %%f in (*) do (
    if not "%%f"=="INSTALAR.bat" (
        if not "%%f"=="LEIA_PRIMEIRO.txt" (
            copy "%%f" "%INSTALL_DIR%\\" >nul
        )
    )
)

REM Criar pastas se não existirem
if not exist "%INSTALL_DIR%\\config" mkdir "%INSTALL_DIR%\\config"
if not exist "%INSTALL_DIR%\\boletos" mkdir "%INSTALL_DIR%\\boletos"
if not exist "%INSTALL_DIR%\\logs" mkdir "%INSTALL_DIR%\\logs"

echo ✅ Arquivos extraídos

echo.
echo [4/4] Configurando aplicação...
echo ⚠️  IMPORTANTE: Configure suas credenciais!
echo.
echo 📝 Abra o arquivo .env e configure:
echo    - WEBISS_USERNAME=seu_usuario
echo    - WEBISS_PASSWORD=sua_senha
echo.

echo ✅ Instalação concluída!
echo.
echo 📁 Aplicação instalada em: %INSTALL_DIR%
echo 🚀 Para usar: Execute EmiteNota_Producao.exe
echo.
echo 💡 Dica: Leia o arquivo LEIA_PRIMEIRO.txt
echo.
pause
"""
    
    return script

def create_installer_readme():
    """Cria README do instalador"""
    
    readme = """EMITE NOTA - INSTRUÇÕES DE INSTALAÇÃO
===============================================

🚀 COMO INSTALAR:
1. Execute o arquivo "INSTALAR.bat"
2. Aguarde a instalação terminar
3. Configure suas credenciais no arquivo .env
4. Execute EmiteNota_Producao.exe

⚙️ CONFIGURAÇÃO:
- Abra o arquivo .env com o Bloco de Notas
- Configure suas credenciais do WebISS:
  WEBISS_USERNAME=seu_usuario_aqui
  WEBISS_PASSWORD=sua_senha_aqui

📁 PASTAS CRIADAS:
- config/     = Configurações do sistema
- boletos/    = Coloque os PDFs aqui
- logs/       = Logs da aplicação

🔧 REQUISITOS:
- Windows 10 ou superior
- Google Chrome instalado
- Conexão com internet

❓ PROBLEMAS?
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
    
    return readme

def main():
    """Função principal"""
    try:
        if create_installer():
            print("\n🎉 Instalador criado com sucesso!")
            print("📦 Arquivo pronto para distribuição")
        else:
            print("\n❌ Falha ao criar instalador")
    except Exception as e:
        print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    main() 