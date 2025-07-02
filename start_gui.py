#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para iniciar a Interface Gráfica - Emite Nota
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

def main():
    """Inicia a interface gráfica"""
    try:
        # Verifica se o arquivo .env existe
        if not os.path.exists('.env'):
            print("⚠️  Arquivo .env não encontrado!")
            print("📝 Copie o arquivo env_example.txt para .env e configure suas credenciais")
            print("💡 Exemplo: cp env_example.txt .env")
            return
        
        # Importa as dependências necessárias
        from config.settings import Settings
        from utils.data_processor import DataProcessor
        from webiss_automation import WebISSAutomation
        from gui.main_window import ModernMainWindow
        
        print("🚀 Iniciando Interface Gráfica Moderna...")
        
        # Inicializa os componentes
        settings = Settings()
        data_processor = DataProcessor()
        webiss_automation = WebISSAutomation
        
        # Cria e executa a interface
        app = ModernMainWindow(data_processor, webiss_automation, settings)
        app.run()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("📦 Instale as dependências: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 