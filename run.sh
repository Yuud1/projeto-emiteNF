#!/bin/bash

echo "========================================"
echo "   Emite Nota - Automação WebISS"
echo "========================================"
echo

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python 3 não encontrado!"
    echo "Instale o Python 3.8 ou superior"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "macOS: brew install python3"
    exit 1
fi

# Verifica se o arquivo .env existe
if [ ! -f ".env" ]; then
    echo "AVISO: Arquivo .env não encontrado!"
    echo
    echo "Para configurar:"
    echo "1. Copie o arquivo env_example.txt para .env"
    echo "2. Edite o arquivo .env com suas credenciais"
    echo
    echo "Exemplo:"
    echo "  cp env_example.txt .env"
    echo "  nano .env"
    echo
    exit 1
fi

# Verifica se as dependências estão instaladas
if [ ! -d "venv" ]; then
    echo "Instalando dependências..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERRO: Falha ao instalar dependências"
        exit 1
    fi
fi

# Executa o programa
echo "Iniciando Emite Nota..."
python3 run.py 