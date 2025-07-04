#!/bin/bash

echo "========================================"
echo "   Emite Nota - Build de Producao (WSL)"
echo "========================================"
echo

# Caminho para o Python do Windows
PYTHON_PATH="/mnt/c/Users/yudim/AppData/Local/Programs/Python/Python313/python.exe"
PIP_PATH="/mnt/c/Users/yudim/AppData/Local/Programs/Python/Python313/Scripts/pip.exe"

echo "[1/5] Verificando ambiente Python..."
$PYTHON_PATH --version
if [ $? -ne 0 ]; then
    echo "❌ Python não encontrado!"
    exit 1
fi
echo "✅ Python encontrado"

echo
echo "[2/5] Verificando PyInstaller..."
$PYTHON_PATH -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Instalando PyInstaller..."
    $PIP_PATH install pyinstaller
    if [ $? -ne 0 ]; then
        echo "❌ Falha ao instalar PyInstaller"
        exit 1
    fi
fi
echo "✅ PyInstaller encontrado"

echo
echo "[3/5] Verificando dependências..."
if [ ! -f "requirements_producao.txt" ]; then
    echo "❌ Arquivo requirements_producao.txt não encontrado!"
    exit 1
fi

$PIP_PATH install -r requirements_producao.txt
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

$PYTHON_PATH -m PyInstaller build_producao.spec --clean
if [ $? -ne 0 ]; then
    echo "❌ Falha na compilação!"
    exit 1
fi

echo
echo "========================================"
echo "✅ COMPILAÇÃO CONCLUÍDA COM SUCESSO!"
echo "========================================"
echo
echo "📁 Executável criado em: dist/EmiteNota_Producao.exe"
echo
echo "📋 Para distribuir:"
echo "   1. Copie a pasta 'dist' completa"
echo "   2. Configure o arquivo .env com as credenciais"
echo "   3. Execute EmiteNota_Producao.exe"
echo
echo "💡 Dica: Teste o executável antes de distribuir!"
echo 