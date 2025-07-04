#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emite Nota - Aplicação de Produção
Versão standalone para distribuição local
"""

import sys
import os
import logging
import traceback
from pathlib import Path
from datetime import datetime

# Configurar logging para produção
def setup_logging():
    """Configura o sistema de logging para produção"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def check_dependencies():
    """Verifica se todas as dependências estão disponíveis"""
    required_modules = [
        'tkinter', 'selenium', 'pandas', 'openpyxl', 
        'dotenv', 'webdriver_manager', 'PIL'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("❌ Módulos faltando:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\n📦 Instale as dependências:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_config_files():
    """Verifica se os arquivos de configuração existem"""
    # Sempre usar o diretório atual onde o executável está rodando
    base_dir = Path.cwd()
    
    # Para arquivos de configuração do sistema, usar o diretório do executável
    if getattr(sys, 'frozen', False):
        # Executando como executável
        config_dir = Path(sys._MEIPASS) / 'config'
    else:
        # Executando como script Python
        config_dir = base_dir / 'config'
    
    required_files = [
        base_dir / '.env',  # .env sempre no diretório atual
        config_dir / 'settings.py',
        config_dir / 'field_mappings.json',
        config_dir / 'cnae_mappings.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not file_path.exists():
            missing_files.append(str(file_path))
    
    if missing_files:
        print("❌ Arquivos de configuração faltando:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        
        # Criar arquivo .env se não existir
        if any('.env' in str(f) for f in missing_files):
            print("\n📝 Criando arquivo .env básico...")
            create_basic_env()
        
        return False
    
    return True

def create_basic_env():
    """Cria um arquivo .env básico se não existir"""
    env_content = """# ========================================
# CONFIGURAÇÕES DO EMITE NOTA
# ========================================
# 
# INSTRUÇÕES:
# 1. Configure suas credenciais do WebISS abaixo
# 2. Salve o arquivo
# 3. Execute o aplicativo novamente
#
# ========================================

# Credenciais do WebISS (OBRIGATÓRIO)
WEBISS_USERNAME=seu_usuario_aqui
WEBISS_PASSWORD=sua_senha_aqui

# Configurações de automação (OPCIONAL)
HEADLESS_MODE=false
TIMEOUT=10

# Configurações de arquivos (OPCIONAL)
DATA_DIRECTORY=data
LOGS_DIRECTORY=logs
MAPPINGS_FILE=config/field_mappings.json

# ========================================
# EXEMPLO DE CONFIGURAÇÃO:
# WEBISS_USERNAME=07912296964
# WEBISS_PASSWORD=minha_senha_segura
# ========================================
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado!")
    print("⚠️  Configure suas credenciais no arquivo .env antes de usar")
    print("💡 Execute 'configurar.bat' para facilitar a configuração")

def main():
    """Função principal da aplicação"""
    # Configurar stdin se necessário
    try:
        import sys
        if sys.stdin is None:
            sys.stdin = open('CONIN$', 'r')
    except:
        pass
    
    logger = setup_logging()
    
    try:
        print("🚀 Iniciando Emite Nota - Versão de Produção")
        print("=" * 50)
        
        # Verificar dependências
        print("📦 Verificando dependências...")
        if not check_dependencies():
            input("\nPressione Enter para sair...")
            return
        
        # Verificar arquivos de configuração
        print("⚙️  Verificando configurações...")
        if not check_config_files():
            print("\n⚠️  Configure os arquivos faltantes e execute novamente")
            input("Pressione Enter para sair...")
            return
        
        # Verificar licença
        print("🔑 Verificando licença...")
        from utils.license_checker import LicenseChecker
        license_checker = LicenseChecker()
        licenca_valida, mensagem = license_checker.verificar_licenca()
        
        if not licenca_valida:
            print(f"❌ {mensagem}")
            print("\n📞 Entre em contato com o suporte para renovar sua licença")
            input("Pressione Enter para sair...")
            return
        
        print(f"✅ {mensagem}")
        
        print("✅ Todas as verificações passaram!")
        print("\n🔄 Iniciando interface gráfica...")
        
        # Importar componentes da aplicação
        from config.settings import Settings
        from utils.data_processor import DataProcessor
        from webiss_automation import WebISSAutomation
        from gui.main_window import ModernMainWindow
        
        # Inicializar componentes
        settings = Settings()
        data_processor = DataProcessor()
        webiss_automation = WebISSAutomation
        
        # Criar e executar interface
        app = ModernMainWindow(data_processor, webiss_automation, settings)
        app.run()
        
    except KeyboardInterrupt:
        print("\n⏹️  Aplicação interrompida pelo usuário")
        logger.info("Aplicação interrompida pelo usuário")
    except Exception as e:
        error_msg = f"❌ Erro crítico na aplicação: {e}"
        print(error_msg)
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        
        print("\n📋 Detalhes do erro foram salvos no log")
        print("💡 Se o problema persistir, entre em contato com o suporte")
        
        input("\nPressione Enter para sair...")
    finally:
        logger.info("Aplicação finalizada")

if __name__ == "__main__":
    main() 