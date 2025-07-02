#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar arquivos não utilizados do projeto
"""

import os
import shutil
from pathlib import Path

def limpar_projeto():
    """Remove arquivos e pastas não utilizados"""
    
    # Lista de pastas para remover
    pastas_para_remover = [
        'gui',
        'automacao', 
        'data',
        'tests',
        '__pycache__',
        'gui/__pycache__',
        'utils/__pycache__',
        'config/__pycache__'
    ]
    
    # Lista de arquivos para remover
    arquivos_para_remover = [
        'test_step3_sem_scroll.py',
        'debug_step3.py', 
        'check_env.py',
        'start_gui.py',
        'data/exemplo_boletos.csv',
        'config/field_mappings.json',
        'config/cnae_mappings.json',
        'GUIA_USO.md',
        'STEP3_GUIDE.md'
    ]
    
    print("🧹 Iniciando limpeza do projeto...")
    
    # Remove pastas
    for pasta in pastas_para_remover:
        if os.path.exists(pasta):
            try:
                shutil.rmtree(pasta)
                print(f"✅ Removida pasta: {pasta}")
            except Exception as e:
                print(f"❌ Erro ao remover pasta {pasta}: {e}")
    
    # Remove arquivos
    for arquivo in arquivos_para_remover:
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
                print(f"✅ Removido arquivo: {arquivo}")
            except Exception as e:
                print(f"❌ Erro ao remover arquivo {arquivo}: {e}")
    
    print("\n🎉 Limpeza concluída!")
    print("📁 Estrutura final do projeto:")
    
    # Lista estrutura final
    for item in os.listdir('.'):
        if os.path.isdir(item):
            print(f"📁 {item}/")
        else:
            print(f"📄 {item}")

if __name__ == "__main__":
    limpar_projeto() 