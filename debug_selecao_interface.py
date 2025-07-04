#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug da interface de seleção de boletos
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd

print("=== DEBUG DA INTERFACE DE SELEÇÃO ===")

# Criar dados de teste
dados = [
    {'arquivo_pdf': 'boleto1.pdf', 'pagina': 1, 'nome_cliente': 'João Silva', 'valor': 100.00},
    {'arquivo_pdf': 'boleto1.pdf', 'pagina': 2, 'nome_cliente': 'Maria Santos', 'valor': 150.00},
    {'arquivo_pdf': 'boleto2.pdf', 'pagina': 1, 'nome_cliente': 'Pedro Costa', 'valor': 200.00},
    {'arquivo_pdf': 'boleto2.pdf', 'pagina': 2, 'nome_cliente': 'Ana Oliveira', 'valor': 120.00},
    {'arquivo_pdf': 'boleto3.pdf', 'pagina': 1, 'nome_cliente': 'Carlos Lima', 'valor': 180.00},
]

df = pd.DataFrame(dados)
print(f"DataFrame criado com {len(df)} registros")

# Simular interface
root = tk.Tk()
root.title("Debug Seleção")
root.geometry("800x600")

# Criar treeview
columns = ('selecionado', 'arquivo', 'pagina', 'cliente', 'valor')
tree = ttk.Treeview(root, columns=columns, show='headings', height=10)

# Configurar colunas
tree.heading('selecionado', text='✓')
tree.heading('arquivo', text='Arquivo')
tree.heading('pagina', text='Página')
tree.heading('cliente', text='Cliente')
tree.heading('valor', text='Valor')

tree.column('selecionado', width=30, anchor='center')
tree.column('arquivo', width=150)
tree.column('pagina', width=60, anchor='center')
tree.column('cliente', width=200)
tree.column('valor', width=100)

# Dicionário para estados dos checkboxes
checkbox_states = {}

# Adicionar dados
for index, (_, row) in enumerate(df.iterrows()):
    item_id = tree.insert('', tk.END, values=(
        '☐',  # Checkbox vazio
        row.get('arquivo_pdf', ''),
        row.get('pagina', ''),
        row.get('nome_cliente', ''),
        f"R$ {row.get('valor', '0')}"
    ))
    checkbox_states[item_id] = False

print(f"Treeview criado com {len(checkbox_states)} itens")

# Função para simular seleção
def simular_selecao():
    print("\n=== SIMULANDO SELEÇÃO ===")
    
    # Simular seleção dos itens 1 e 3 (Maria Santos e Ana Oliveira)
    tree_items = tree.get_children()
    selecionados = [tree_items[1], tree_items[3]]  # Índices 1 e 3
    
    print(f"Itens a serem selecionados: {selecionados}")
    
    for item_id in selecionados:
        checkbox_states[item_id] = True
        values = list(tree.item(item_id, 'values'))
        values[0] = '☑'
        tree.item(item_id, values=values)
        print(f"✅ Item {item_id} selecionado")
    
    # Testar função get_selected_data
    selected_indices = []
    
    print(f"\n🔍 Verificando seleção: {len(tree_items)} itens na árvore")
    
    for i, item in enumerate(tree_items):
        checkbox_state = checkbox_states.get(item, False)
        
        # Obter dados do item da árvore
        item_values = tree.item(item, 'values')
        nome_cliente = item_values[3] if len(item_values) > 3 else ''
        arquivo = item_values[1] if len(item_values) > 1 else ''
        pagina = item_values[2] if len(item_values) > 2 else ''
        
        print(f"  Item {i}: {item} - Cliente: {nome_cliente} - Selecionado: {checkbox_state}")
        
        if checkbox_state:
            # Encontrar índice correto no DataFrame
            matching_indices = []
            for idx, (_, row) in enumerate(df.iterrows()):
                if (row.get('nome_cliente', '') == nome_cliente and 
                    row.get('arquivo_pdf', '') == arquivo and 
                    str(row.get('pagina', '')) == str(pagina)):
                    matching_indices.append(idx)
            
            if matching_indices:
                selected_indices.append(matching_indices[0])
                print(f"  ✅ Adicionado índice {matching_indices[0]} para cliente: {nome_cliente}")
            else:
                selected_indices.append(i)
                print(f"  ⚠️ Usando índice fallback {i} para cliente: {nome_cliente}")
    
    print(f"\n📋 Índices selecionados: {selected_indices}")
    
    if selected_indices:
        selected_data = df.iloc[selected_indices]
        print(f"✅ {len(selected_data)} boletos selecionados para processamento")
        
        for i, (_, row) in enumerate(selected_data.iterrows()):
            print(f"  Boleto {i+1}: {row.get('nome_cliente', 'N/A')}")
    else:
        print("❌ Nenhum boleto selecionado!")

# Botão para testar
test_button = tk.Button(root, text="Testar Seleção", command=simular_selecao)
test_button.pack(pady=10)

# Exibir treeview
tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

print("\nInterface criada. Clique em 'Testar Seleção' para ver o resultado.")
print("Pressione Ctrl+C para sair.")

try:
    root.mainloop()
except KeyboardInterrupt:
    print("\nSaindo...")
    root.destroy() 