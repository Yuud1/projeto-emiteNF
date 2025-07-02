#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Inicialização - Emite Nota
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

def main():
    """Função principal simplificada"""
    try:
        # Verifica se o arquivo .env existe
        if not os.path.exists('.env'):
            print("⚠️  Arquivo .env não encontrado!")
            print("📝 Copie o arquivo env_example.txt para .env e configure suas credenciais")
            print("💡 Exemplo: cp env_example.txt .env")
            return
        
        # Importa e executa o programa principal
        from main import main as run_main
        run_main()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("📦 Instale as dependências: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main() 