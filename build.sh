#!/bin/bash

echo "========================================"
echo "   Emite Nota - Build de Producao"
echo "========================================"
echo

echo "[1/5] Verificando ambiente Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    echo "Instale o Python 3.8+ e tente novamente"
    exit 1
fi
echo "✅ Python encontrado"

echo
echo "[2/5] Verificando PyInstaller..."
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "📦 Instalando PyInstaller..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "❌ Falha ao instalar PyInstaller"
        exit 1
    fi
fi
echo "✅ PyInstaller encontrado"

echo
echo "[3/5] Verificando dependências..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ Arquivo requirements.txt não encontrado!"
    exit 1
fi

pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Falha ao instalar dependências"
    exit 1
fi
echo "✅ Dependências instaladas"

echo
echo "[4/5] Verificando arquivos necessários..."
if [ ! -f "app_producao.py" ]; then
    echo "❌ Arquivo app_producao.py não encontrado!"
    exit 1
fi

if [ ! -f "build_producao.spec" ]; then
    echo "❌ Arquivo build_producao.spec não encontrado!"
    exit 1
fi
echo "✅ Arquivos encontrados"

echo
echo "[5/5] Compilando aplicação..."
echo "⏳ Isso pode demorar alguns minutos..."
echo

pyinstaller build_producao.spec --clean
if [ $? -ne 0 ]; then
    echo "❌ Falha na compilação!"
    exit 1
fi

echo
echo "========================================"
echo "✅ COMPILAÇÃO CONCLUÍDA COM SUCESSO!"
echo "========================================"
echo
echo "📁 Executável criado em: dist/EmiteNota_Producao"
echo
echo "📋 Para distribuir:"
echo "   1. Copie a pasta 'dist' completa"
echo "   2. Configure o arquivo .env com as credenciais"
echo "   3. Execute ./EmiteNota_Producao"
echo
echo "💡 Dica: Teste o executável antes de distribuir!"
echo 