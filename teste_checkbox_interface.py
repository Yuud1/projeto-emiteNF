#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar checkboxes da interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import pandas as pd

class TesteCheckbox:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Teste Checkbox Interface")
        self.root.geometry("1000x700")
        
        # Dados de teste
        self.dados = [
            {'arquivo_pdf': 'boleto1.pdf', 'pagina': 1, 'nome_cliente': 'João Silva', 'valor': 100.00},
            {'arquivo_pdf': 'boleto1.pdf', 'pagina': 2, 'nome_cliente': 'Maria Santos', 'valor': 150.00},
            {'arquivo_pdf': 'boleto2.pdf', 'pagina': 1, 'nome_cliente': 'Pedro Costa', 'valor': 200.00},
            {'arquivo_pdf': 'boleto2.pdf', 'pagina': 2, 'nome_cliente': 'Ana Oliveira', 'valor': 120.00},
            {'arquivo_pdf': 'boleto3.pdf', 'pagina': 1, 'nome_cliente': 'Carlos Lima', 'valor': 180.00},
        ]
        
        self.df = pd.DataFrame(self.dados)
        self.checkbox_states = {}
        
        self.setup_ui()
        self.populate_tree()
    
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ('selecionado', 'arquivo', 'pagina', 'cliente', 'valor')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=10)
        
        # Configurar colunas
        self.tree.heading('selecionado', text='✓')
        self.tree.heading('arquivo', text='Arquivo')
        self.tree.heading('pagina', text='Página')
        self.tree.heading('cliente', text='Cliente')
        self.tree.heading('valor', text='Valor')
        
        self.tree.column('selecionado', width=50, anchor='center')
        self.tree.column('arquivo', width=150)
        self.tree.column('pagina', width=80, anchor='center')
        self.tree.column('cliente', width=200)
        self.tree.column('valor', width=100)
        
        # Configurar evento de clique
        self.tree.bind('<Button-1>', self.on_tree_click)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Log
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Botões
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(button_frame, text="Testar Seleção", command=self.testar_selecao).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Limpar Log", command=self.limpar_log).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Selecionar Todos", command=self.selecionar_todos).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Desmarcar Todos", command=self.desmarcar_todos).pack(side=tk.LEFT, padx=5)
    
    def log_message(self, message, level="INFO"):
        """Adiciona mensagem ao log"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        color_map = {
            "INFO": "#3498db",
            "SUCCESS": "#27ae60", 
            "WARNING": "#f39c12",
            "ERROR": "#e74c3c"
        }
        
        color = color_map.get(level, "#ecf0f1")
        
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
        # Colorir a última linha
        last_line_start = self.log_text.index("end-2c linestart")
        last_line_end = self.log_text.index("end-1c")
        self.log_text.tag_add(level, last_line_start, last_line_end)
        self.log_text.tag_config(level, foreground=color)
        
        # Forçar atualização
        self.root.update()
    
    def populate_tree(self):
        """Popula a árvore com dados"""
        for index, (_, row) in enumerate(self.df.iterrows()):
            item_id = self.tree.insert('', tk.END, values=(
                '☐',  # Checkbox vazio
                row.get('arquivo_pdf', ''),
                row.get('pagina', ''),
                row.get('nome_cliente', ''),
                f"R$ {row.get('valor', '0')}"
            ))
            self.checkbox_states[item_id] = False
        
        self.log_message(f"✅ Árvore populada com {len(self.df)} registros", "SUCCESS")
    
    def on_tree_click(self, event):
        """Manipula cliques no treeview"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            return
        
        item = self.tree.identify_row(event.y)
        if not item:
            return
        
        column = self.tree.identify_column(event.x)
        if column == '#1':  # Coluna do checkbox
            # Obter dados do item
            item_values = self.tree.item(item, 'values')
            nome_cliente = item_values[3] if len(item_values) > 3 else 'N/A'
            
            # Alternar estado
            current_state = self.checkbox_states.get(item, False)
            new_state = not current_state
            self.checkbox_states[item] = new_state
            
            # Atualizar visual
            values = list(self.tree.item(item, 'values'))
            values[0] = '☑' if new_state else '☐'
            self.tree.item(item, values=values)
            
            # Log
            self.log_message(f"🖱️ Clique: {nome_cliente} - {current_state} → {new_state}", "INFO")
            self.update_selection_count()
    
    def update_selection_count(self):
        """Atualiza contador de selecionados"""
        selected_count = sum(1 for state in self.checkbox_states.values() if state)
        total_count = len(self.checkbox_states)
        
        if selected_count > 0:
            selected_items = []
            for item, state in self.checkbox_states.items():
                if state:
                    item_values = self.tree.item(item, 'values')
                    nome_cliente = item_values[3] if len(item_values) > 3 else 'N/A'
                    selected_items.append(nome_cliente)
            
            self.log_message(f"📊 {selected_count}/{total_count} selecionados: {', '.join(selected_items)}", "INFO")
        else:
            self.log_message(f"📊 {selected_count}/{total_count} selecionados", "INFO")
    
    def testar_selecao(self):
        """Testa a função get_selected_data"""
        self.log_message("🔍 Testando função get_selected_data...", "INFO")
        
        selected_indices = []
        tree_items = self.tree.get_children()
        
        self.log_message(f"📋 Verificando {len(tree_items)} itens na árvore", "INFO")
        
        for i, item in enumerate(tree_items):
            checkbox_state = self.checkbox_states.get(item, False)
            
            # Obter dados do item
            item_values = self.tree.item(item, 'values')
            nome_cliente = item_values[3] if len(item_values) > 3 else ''
            arquivo = item_values[1] if len(item_values) > 1 else ''
            pagina = item_values[2] if len(item_values) > 2 else ''
            
            self.log_message(f"  Item {i}: {item} - {nome_cliente} - Selecionado: {checkbox_state}", "INFO")
            
            if checkbox_state:
                # Encontrar índice no DataFrame
                matching_indices = []
                for idx, (_, row) in enumerate(self.df.iterrows()):
                    if (row.get('nome_cliente', '') == nome_cliente and 
                        row.get('arquivo_pdf', '') == arquivo and 
                        str(row.get('pagina', '')) == str(pagina)):
                        matching_indices.append(idx)
                
                if matching_indices:
                    selected_indices.append(matching_indices[0])
                    self.log_message(f"  ✅ Adicionado índice {matching_indices[0]} para {nome_cliente}", "SUCCESS")
                else:
                    selected_indices.append(i)
                    self.log_message(f"  ⚠️ Usando índice fallback {i} para {nome_cliente}", "WARNING")
        
        if selected_indices:
            selected_data = self.df.iloc[selected_indices]
            self.log_message(f"✅ {len(selected_data)} boletos selecionados para processamento", "SUCCESS")
            for i, (_, row) in enumerate(selected_data.iterrows()):
                self.log_message(f"  Boleto {i+1}: {row.get('nome_cliente', 'N/A')}", "INFO")
        else:
            self.log_message("❌ Nenhum boleto selecionado!", "ERROR")
    
    def selecionar_todos(self):
        """Seleciona todos os itens"""
        for item in self.tree.get_children():
            self.checkbox_states[item] = True
            values = list(self.tree.item(item, 'values'))
            values[0] = '☑'
            self.tree.item(item, values=values)
        self.update_selection_count()
        self.log_message("✅ Todos os itens selecionados", "SUCCESS")
    
    def desmarcar_todos(self):
        """Desmarca todos os itens"""
        for item in self.tree.get_children():
            self.checkbox_states[item] = False
            values = list(self.tree.item(item, 'values'))
            values[0] = '☐'
            self.tree.item(item, values=values)
        self.update_selection_count()
        self.log_message("❌ Todos os itens desmarcados", "WARNING")
    
    def limpar_log(self):
        """Limpa o log"""
        self.log_text.delete(1.0, tk.END)
    
    def run(self):
        self.log_message("✅ Interface de teste iniciada", "SUCCESS")
        self.log_message("💡 Clique nos checkboxes para testar a seleção", "INFO")
        self.root.mainloop()

if __name__ == "__main__":
    app = TesteCheckbox()
    app.run() 