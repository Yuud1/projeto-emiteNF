#!/bin/bash

echo "🔧 Recompilando aplicação..."

# Tentar fechar processo se estiver rodando
echo "📋 Fechando processos anteriores..."
taskkill /f /im EmiteNota_Producao.exe 2>/dev/null || true

# Limpar build anterior
echo "🧹 Limpando build anterior..."
rm -rf build/
rm -rf dist/

# Recompilar
echo "🔨 Compilando..."
pyinstaller build_producao.spec --clean

echo "✅ Recompilação concluída!"
echo "📁 Executável: dist/EmiteNota_Producao.exe" 