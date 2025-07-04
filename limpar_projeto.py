#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar o projeto removendo arquivos desnecessários
"""

import os
import shutil
import glob

def limpar_projeto():
    """Remove arquivos e pastas desnecessários do projeto"""
    
    # Pastas para remover
    pastas_para_remover = [
        'build',
        'dist', 
        '__pycache__',
        'logs',
        'installer',
        'boletos',
        'data'
    ]
    
    # Arquivos para remover
    arquivos_para_remover = [
        'nul',
        'teste_producao.py',
        'run.py',
        'run.bat',
        'run.sh',
        'boletos_extraidos.csv',
        'EmiteNota.spec',
        'build_simples.spec',
        'requirements_simple.txt',
        'app_simples.py'
    ]
    
    # Arquivos para remover da pasta dist
    arquivos_dist_para_remover = [
        'boletos_extraidos.csv',
        '*.log',
        '*.tmp'
    ]
    
    print("🧹 Iniciando limpeza do projeto...")
    
    # Remover pastas
    for pasta in pastas_para_remover:
        if os.path.exists(pasta):
            try:
                shutil.rmtree(pasta)
                print(f"✅ Pasta removida: {pasta}")
            except Exception as e:
                print(f"❌ Erro ao remover pasta {pasta}: {e}")
    
    # Remover arquivos
    for arquivo in arquivos_para_remover:
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
                print(f"✅ Arquivo removido: {arquivo}")
            except Exception as e:
                print(f"❌ Erro ao remover arquivo {arquivo}: {e}")
    
    # Remover arquivos da pasta dist
    if os.path.exists('dist'):
        print("🧹 Limpando pasta dist...")
        for arquivo in arquivos_dist_para_remover:
            if arquivo == 'boletos_extraidos.csv':
                csv_path = os.path.join('dist', arquivo)
                if os.path.exists(csv_path):
                    try:
                        os.remove(csv_path)
                        print(f"✅ Arquivo removido da dist: {arquivo}")
                    except Exception as e:
                        print(f"❌ Erro ao remover arquivo da dist {arquivo}: {e}")
            else:
                # Para padrões glob
                for file_path in glob.glob(os.path.join('dist', arquivo)):
                    try:
                        os.remove(file_path)
                        print(f"✅ Arquivo removido da dist: {os.path.basename(file_path)}")
                    except Exception as e:
                        print(f"❌ Erro ao remover arquivo da dist {file_path}: {e}")
    
    # Remover arquivos .pyc e __pycache__ em subpastas
    for root, dirs, files in os.walk('.'):
        # Remover __pycache__
        if '__pycache__' in dirs:
            try:
                shutil.rmtree(os.path.join(root, '__pycache__'))
                print(f"✅ __pycache__ removido em: {root}")
            except Exception as e:
                print(f"❌ Erro ao remover __pycache__ em {root}: {e}")
        
        # Remover arquivos .pyc
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                    print(f"✅ Arquivo .pyc removido: {os.path.join(root, file)}")
                except Exception as e:
                    print(f"❌ Erro ao remover {file}: {e}")
    
    print("\n🎉 Limpeza concluída!")
    print("📁 Arquivos mantidos:")
    print("   - app_producao.py (aplicação principal)")
    print("   - main.py (script de teste)")
    print("   - start_gui.py (interface gráfica)")
    print("   - webiss_automation.py (automação)")
    print("   - config/ (configurações)")
    print("   - gui/ (interface gráfica)")
    print("   - utils/ (utilitários)")
    print("   - build_producao.spec (build da produção)")
    print("   - requirements_producao.txt (dependências)")
    print("   - Scripts de build e instalação")

if __name__ == "__main__":
    limpar_projeto() 