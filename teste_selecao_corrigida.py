#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da correção da seleção de boletos
"""

import pandas as pd

print("=== TESTE DA CORREÇÃO DE SELEÇÃO ===")

# Simular dados do DataFrame
dados = [
    {'arquivo_pdf': 'boleto1.pdf', 'pagina': 1, 'nome_cliente': 'João Silva', 'valor': 100.00},
    {'arquivo_pdf': 'boleto1.pdf', 'pagina': 2, 'nome_cliente': 'Maria Santos', 'valor': 150.00},
    {'arquivo_pdf': 'boleto2.pdf', 'pagina': 1, 'nome_cliente': 'Pedro Costa', 'valor': 200.00},
    {'arquivo_pdf': 'boleto2.pdf', 'pagina': 2, 'nome_cliente': 'Ana Oliveira', 'valor': 120.00},
    {'arquivo_pdf': 'boleto3.pdf', 'pagina': 1, 'nome_cliente': 'Carlos Lima', 'valor': 180.00},
]

df = pd.DataFrame(dados)
print(f"DataFrame criado com {len(df)} registros:")
for i, (_, row) in enumerate(df.iterrows()):
    print(f"  Índice {i}: {row['nome_cliente']} - {row['arquivo_pdf']} p.{row['pagina']}")

# Simular itens da árvore (pode estar em ordem diferente)
tree_items = [
    {'item_id': 'I001', 'nome_cliente': 'João Silva', 'arquivo': 'boleto1.pdf', 'pagina': 1},
    {'item_id': 'I002', 'nome_cliente': 'Maria Santos', 'arquivo': 'boleto1.pdf', 'pagina': 2},
    {'item_id': 'I003', 'nome_cliente': 'Pedro Costa', 'arquivo': 'boleto2.pdf', 'pagina': 1},
    {'item_id': 'I004', 'nome_cliente': 'Ana Oliveira', 'arquivo': 'boleto2.pdf', 'pagina': 2},
    {'item_id': 'I005', 'nome_cliente': 'Carlos Lima', 'arquivo': 'boleto3.pdf', 'pagina': 1},
]

# Simular seleção (itens 1 e 3 selecionados - Maria Santos e Ana Oliveira)
selecionados = ['I002', 'I004']  # IDs dos itens selecionados

print(f"\nItens selecionados: {selecionados}")

# Simular a nova lógica de mapeamento
selected_indices = []

for item_id in selecionados:
    # Encontrar o item na árvore
    item_data = None
    for item in tree_items:
        if item['item_id'] == item_id:
            item_data = item
            break
    
    if item_data:
        nome_cliente = item_data['nome_cliente']
        arquivo = item_data['arquivo']
        pagina = item_data['pagina']
        
        print(f"\n🔍 Procurando por: {nome_cliente} - {arquivo} p.{pagina}")
        
        # Encontrar índice no DataFrame
        matching_indices = []
        for idx, (_, row) in enumerate(df.iterrows()):
            if (row.get('nome_cliente', '') == nome_cliente and 
                row.get('arquivo_pdf', '') == arquivo and 
                str(row.get('pagina', '')) == str(pagina)):
                matching_indices.append(idx)
                print(f"  ✅ Encontrado no índice {idx}")
        
        if matching_indices:
            selected_indices.append(matching_indices[0])
            print(f"  ✅ Adicionado índice {matching_indices[0]} para {nome_cliente}")
        else:
            print(f"  ❌ Não encontrado para {nome_cliente}")

print(f"\n📋 Índices selecionados: {selected_indices}")

# Obter dados selecionados
if selected_indices:
    selected_data = df.iloc[selected_indices]
    print(f"\n✅ {len(selected_data)} boletos selecionados:")
    for i, (_, row) in enumerate(selected_data.iterrows()):
        print(f"  Boleto {i+1}: {row['nome_cliente']} - R$ {row['valor']}")
else:
    print("\n❌ Nenhum boleto selecionado!")

print("\n=== RESULTADO ===")
if len(selected_indices) == 2:
    print("✅ Correção funcionando! 2 boletos selecionados corretamente.")
else:
    print("❌ Problema ainda existe!") 