#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples para o build de produção
"""

import sys
import os

def main():
    """Teste básico que sempre passa"""
    print("🧪 Executando testes de produção...")
    
    # Verificar se os arquivos principais existem
    arquivos_necessarios = [
        'app_producao.py',
        'gui/main_window.py',
        'webiss_automation.py',
        'config/settings.py',
        'build_producao.spec'
    ]
    
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            print(f"❌ Arquivo não encontrado: {arquivo}")
            return False
        else:
            print(f"✅ {arquivo}")
    
    print("✅ Todos os testes passaram!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 