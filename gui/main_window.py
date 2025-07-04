#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Gráfica Moderna - Emite Nota WebISS
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import logging
import time
import os
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import textwrap

logger = logging.getLogger(__name__)

class ModernMainWindow:
    """Janela principal moderna da aplicação"""
    
    def __init__(self, data_processor, webiss_automation, settings):
        self.data_processor = data_processor
        self.webiss_automation = webiss_automation
        self.settings = settings
        
        # Configuração da janela principal
        self.root = tk.Tk()
        self.root.title("Emite Nota - Automação WebISS")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Variáveis de controle
        self.processing = False
        self.current_data = None
        self.automation = None
        
        # Configurar interface
        self.setup_ui()
    
    def get_app_base_path(self):
        """Retorna o diretório base da aplicação (executável ou script)"""
        import sys
        if getattr(sys, 'frozen', False):
            # Se é um executável PyInstaller
            return os.path.dirname(sys.executable)
        else:
            # Se é executado como script Python
            return os.getcwd()
        
    def setup_ui(self):
        """Configura a interface do usuário moderna"""
        # Frame principal com gradiente
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Container principal
        content_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Painel esquerdo - Status e Controles
        left_panel = tk.Frame(content_frame, bg='#34495e', width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(20, 10), pady=20)
        left_panel.pack_propagate(False)
        
        # Painel direito - Log e Dados
        right_panel = tk.Frame(content_frame, bg='#34495e')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=20)
        
        # Configurar painéis
        self.create_left_panel(left_panel)
        self.create_right_panel(right_panel)
        
    def create_header(self, parent):
        """Cria o cabeçalho da aplicação"""
        header_frame = tk.Frame(parent, bg='#2c3e50')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título principal
        title_label = tk.Label(header_frame, 
                              text="Emite Nota - Automação WebISS", 
                              font=('Segoe UI', 24, 'bold'),
                              fg='#ecf0f1',
                              bg='#2c3e50')
        title_label.pack()
        
        # Subtítulo
        subtitle_label = tk.Label(header_frame,
                                 text="Processamento Automático de Boletos",
                                 font=('Segoe UI', 12),
                                 fg='#bdc3c7',
                                 bg='#2c3e50')
        subtitle_label.pack()
        
    def create_left_panel(self, parent):
        """Cria o painel esquerdo com status e controles"""
        # Status do Sistema
        status_frame = tk.LabelFrame(parent, text="Status do Sistema", 
                                   font=('Segoe UI', 12, 'bold'),
                                   fg='#ecf0f1', bg='#34495e',
                                   relief=tk.FLAT, bd=1)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Status dos dados
        self.data_status_label = tk.Label(status_frame, 
                                         text="❌ Dados não carregados",
                                         font=('Segoe UI', 10),
                                         fg='#e74c3c', bg='#34495e')
        self.data_status_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # Status do WebISS
        self.webiss_status_label = tk.Label(status_frame,
                                           text="❌ WebISS não conectado",
                                           font=('Segoe UI', 10),
                                           fg='#e74c3c', bg='#34495e')
        self.webiss_status_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # Controles Principais
        controls_frame = tk.LabelFrame(parent, text="Controles", 
                                     font=('Segoe UI', 12, 'bold'),
                                     fg='#ecf0f1', bg='#34495e',
                                     relief=tk.FLAT, bd=1)
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Seleção de pasta de PDFs
        pdf_folder_frame = tk.Frame(controls_frame, bg='#34495e')
        pdf_folder_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(pdf_folder_frame, text="Pasta com PDFs:", 
                 font=('Segoe UI', 10),
                 background='#34495e', foreground='#ecf0f1').pack(anchor=tk.W)
        
        folder_select_frame = tk.Frame(pdf_folder_frame, bg='#34495e')
        folder_select_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Usar caminho absoluto para a pasta boletos baseado no diretório do executável
        boletos_path = os.path.join(self.get_app_base_path(), 'boletos')
        self.folder_var = tk.StringVar(value=boletos_path)
        self.folder_entry = tk.Entry(folder_select_frame, 
                                   textvariable=self.folder_var,
                                   font=('Segoe UI', 10),
                                   bg='#2c3e50', fg='#ecf0f1',
                                   relief=tk.FLAT, bd=1)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        tk.Button(folder_select_frame,
                 text="📁 Procurar",
                 font=('Segoe UI', 9),
                 bg='#95a5a6', fg='white',
                 relief=tk.FLAT, padx=10, pady=5,
                 command=self.browse_folder).pack(side=tk.RIGHT)
        
        # Botão Extrair PDFs
        self.extract_button = tk.Button(controls_frame,
                                       text="📄 Extrair Boletos PDF",
                                       font=('Segoe UI', 11),
                                       bg='#3498db', fg='white',
                                       relief=tk.FLAT, padx=20, pady=10,
                                       command=self.extract_pdfs)
        self.extract_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Botão Carregar Dados
        self.load_button = tk.Button(controls_frame,
                                    text="📊 Carregar Dados",
                                    font=('Segoe UI', 11),
                                    bg='#27ae60', fg='white',
                                    relief=tk.FLAT, padx=20, pady=10,
                                    command=self.load_data)
        self.load_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Botão Conectar WebISS
        self.connect_button = tk.Button(controls_frame,
                                       text="🔗 Conectar WebISS",
                                       font=('Segoe UI', 11),
                                       bg='#f39c12', fg='white',
                                       relief=tk.FLAT, padx=20, pady=10,
                                       command=self.connect_webiss)
        self.connect_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Botão Iniciar Automação
        self.start_button = tk.Button(controls_frame,
                                     text="🚀 Iniciar Automação",
                                     font=('Segoe UI', 11, 'bold'),
                                     bg='#e74c3c', fg='white',
                                     relief=tk.FLAT, padx=20, pady=10,
                                     command=self.start_automation)
        self.start_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Botão Parar
        self.stop_button = tk.Button(controls_frame,
                                    text="⏹️ Parar Processamento",
                                    font=('Segoe UI', 11),
                                    bg='#95a5a6', fg='white',
                                    relief=tk.FLAT, padx=20, pady=10,
                                    command=self.stop_automation,
                                    state=tk.DISABLED)
        self.stop_button.pack(fill=tk.X, padx=10, pady=5)
        

        
        # Informações da Licença
        license_frame = tk.LabelFrame(parent, text="Licença", 
                                    font=('Segoe UI', 12, 'bold'),
                                    fg='#ecf0f1', bg='#34495e',
                                    relief=tk.FLAT, bd=1)
        license_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status da licença
        self.license_status_label = tk.Label(license_frame,
                                            text="🔑 Verificando licença...",
                                            font=('Segoe UI', 10),
                                            fg='#f39c12', bg='#34495e')
        self.license_status_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # Informações da licença
        self.license_info_label = tk.Label(license_frame,
                                          text="",
                                          font=('Segoe UI', 9),
                                          fg='#bdc3c7', bg='#34495e')
        self.license_info_label.pack(anchor=tk.W, padx=10, pady=2)
        
        # Configurações Rápidas
        config_frame = tk.LabelFrame(parent, text="Configurações", 
                                   font=('Segoe UI', 12, 'bold'),
                                   fg='#ecf0f1', bg='#34495e',
                                   relief=tk.FLAT, bd=1)
        config_frame.pack(fill=tk.X)
        
        # Modo Headless
        self.headless_var = tk.BooleanVar(value=self.settings.headless_mode)
        headless_check = tk.Checkbutton(config_frame,
                                       text="Modo Headless",
                                       font=('Segoe UI', 10),
                                       fg='#ecf0f1', bg='#34495e',
                                       selectcolor='#2c3e50',
                                       variable=self.headless_var)
        headless_check.pack(anchor=tk.W, padx=10, pady=5)
        
    def create_right_panel(self, parent):
        """Cria o painel direito com log e dados"""
        # Abas
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba de Log
        log_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(log_frame, text="Log de Execução")
        
        # Log principal
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                 font=('Consolas', 10),
                                                 bg='#2c3e50', fg='#ecf0f1',
                                                 relief=tk.FLAT, bd=0)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba de Dados
        data_frame = tk.Frame(notebook, bg='#2c3e50')
        notebook.add(data_frame, text="Dados Extraídos")
        
        # Treeview para dados com checkbox
        columns = ('selecionado', 'arquivo', 'pagina', 'cliente', 'valor', 'vencimento', 'turma')
        self.data_tree = ttk.Treeview(data_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        self.data_tree.heading('selecionado', text='✓')
        self.data_tree.heading('arquivo', text='Arquivo')
        self.data_tree.heading('pagina', text='Página')
        self.data_tree.heading('cliente', text='Cliente')
        self.data_tree.heading('valor', text='Valor')
        self.data_tree.heading('vencimento', text='Vencimento')
        self.data_tree.heading('turma', text='Turma')
        
        self.data_tree.column('selecionado', width=30, anchor='center')
        self.data_tree.column('arquivo', width=150)
        self.data_tree.column('pagina', width=60, anchor='center')
        self.data_tree.column('cliente', width=200)
        self.data_tree.column('valor', width=100)
        self.data_tree.column('vencimento', width=100)
        self.data_tree.column('turma', width=80)
        
        # Configurar evento de clique para alternar checkbox
        self.data_tree.bind('<Button-1>', self.on_tree_click)
        
        # Dicionário para armazenar estado dos checkboxes
        self.checkbox_states = {}
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=scrollbar.set)
        
        self.data_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Frame para botões de seleção
        selection_frame = tk.Frame(data_frame, bg='#2c3e50')
        selection_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Botões de seleção
        tk.Button(selection_frame,
                 text="✓ Selecionar Todos",
                 font=('Segoe UI', 9),
                 bg='#27ae60', fg='white',
                 relief=tk.FLAT, padx=10, pady=5,
                 command=self.select_all).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(selection_frame,
                 text="✗ Desmarcar Todos",
                 font=('Segoe UI', 9),
                 bg='#e74c3c', fg='white',
                 relief=tk.FLAT, padx=10, pady=5,
                 command=self.deselect_all).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(selection_frame,
                 text="🔄 Inverter Seleção",
                 font=('Segoe UI', 9),
                 bg='#f39c12', fg='white',
                 relief=tk.FLAT, padx=10, pady=5,
                 command=self.invert_selection).pack(side=tk.LEFT)
        
    def log_message(self, message, level="INFO"):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
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
        
    def browse_folder(self):
        """Abre diálogo para selecionar pasta com PDFs"""
        # Usar o diretório atual da pasta boletos como inicial
        initial_dir = self.folder_var.get()
        if not os.path.exists(initial_dir):
            # Se a pasta boletos não existe, usar o diretório do executável
            initial_dir = self.get_app_base_path()
        
        folder_path = filedialog.askdirectory(
            title="Selecionar pasta com PDFs dos boletos",
            initialdir=initial_dir
        )
        
        if folder_path:
            self.folder_var.set(folder_path)
            self.log_message(f"📁 Pasta selecionada: {folder_path}", "INFO")
    
    def extract_pdfs(self):
        """Extrai dados dos PDFs na pasta selecionada"""
        def extract_thread():
            try:
                folder_path = self.folder_var.get()
                self.log_message(f"Iniciando extração de PDFs da pasta: {folder_path}", "INFO")
                
                # Verificar se a pasta existe
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    self.log_message(f"Pasta '{folder_path}' criada. Adicione os PDFs e execute novamente.", "WARNING")
                    return
                
                # Importar dependências necessárias
                import pdfplumber
                import re
                
                def extrair_dados_boleto_pagina(pdf_path, pagina_num, texto_pagina):
                    """Extrai dados de uma página específica de um boleto PDF"""
                    # Nome do cliente (Pagador) - removendo CPF/CNPJ que vem depois
                    nome = re.search(r'Pagador:\s*(.+?)(?:\s+CPF\s*/\s*CNPJ|$)', texto_pagina)

                    # CPF/CNPJ - padrão específico da instituição
                    cpf_cnpj = ''
                    cpf_match = re.search(r'([\d]{3}\.[\d]{3}\.[\d]{3}-[\d]{2})', texto_pagina)
                    if cpf_match:
                        cpf_cnpj = cpf_match.group(1)

                    # Endereço - extração separada com múltiplas estratégias
                    endereco = ''
                    
                    # Estratégia 1: Padrão original
                    endereco_match = re.search(r'CPF ?/ ?CNPJ[:\s]*[\d.\-/]+\s+(.+?PALMAS.*?)\s*-?\s*(\d{8})', texto_pagina)
                    if endereco_match:
                        endereco = f"{endereco_match.group(1)} - {endereco_match.group(2)}"
                    else:
                        # Estratégia 2: Busca por PALMAS seguido de CEP
                        endereco_match = re.search(r'(.+?PALMAS.*?)\s*-?\s*(\d{5}-?\d{3})', texto_pagina)
                        if endereco_match:
                            endereco = f"{endereco_match.group(1)} - {endereco_match.group(2)}"
                        else:
                            # Estratégia 3: Busca por qualquer padrão de CEP após endereço
                            endereco_match = re.search(r'(.+?)\s*(\d{5}-?\d{3})', texto_pagina)
                            if endereco_match:
                                endereco = f"{endereco_match.group(1)} - {endereco_match.group(2)}"
                            else:
                                # Estratégia 4: Busca simples por CEP no texto
                                cep_match = re.search(r'(\d{5}-?\d{3})', texto_pagina)
                                if cep_match:
                                    endereco = f"Endereço - {cep_match.group(1)}"

                    valor = re.search(r'Valor do Documento.*?(\d{1,3}(?:\.\d{3})*,\d{2})', texto_pagina, re.DOTALL)
                    vencimento = re.search(r'Local de Pagamento.*?(\d{2}/\d{2}/\d{4})', texto_pagina, re.DOTALL)
                    descricao = re.search(r'(MENSALIDADE:.*)', texto_pagina)
                    linha_digitavel = re.search(r'(\d{5}\.\d{5} \d{5}\.\d{6} \d{5}\.\d{6} \d \d{13,14}-?\d)', texto_pagina)

                    # Extrair turma
                    turma_match = re.search(r'TURMA[:\s]+([A-Z0-9]+)', texto_pagina)
                    turma = turma_match.group(1) if turma_match else ''

                    # Mapeamento CNAE e atividade
                    if turma.startswith('J'):
                        cnae = '8513900'
                        atividade = '0801'
                    elif turma.startswith('G'):
                        cnae = '8520100'
                        atividade = '0801'
                    else:
                        cnae = ''
                        atividade = ''

                    dados = {
                        'arquivo_pdf': os.path.basename(pdf_path),
                        'pagina': pagina_num,
                        'nome_cliente': nome.group(1).strip() if nome else '',
                        'cpf_cnpj': cpf_cnpj,
                        'endereco': endereco.strip(),
                        'valor': valor.group(1).replace('.', '').replace(',', '.') if valor else '',
                        'vencimento': vencimento.group(1) if vencimento else '',
                        'descricao': descricao.group(1).strip() if descricao else 'serviços educacionais',
                        'linha_digitavel': linha_digitavel.group(1) if linha_digitavel else '',
                        'turma': turma,
                        'cnae': cnae,
                        'atividade': atividade
                    }

                    return dados

                def extrair_dados_boleto(pdf_path):
                    """Extrai dados de um boleto PDF, processando cada página separadamente"""
                    dados_paginas = []
                    
                    with pdfplumber.open(pdf_path) as pdf:
                        total_paginas = len(pdf.pages)
                        self.log_message(f"📄 Processando {total_paginas} página(s) do arquivo: {os.path.basename(pdf_path)}", "INFO")
                        
                        for pagina_num, page in enumerate(pdf.pages, 1):
                            try:
                                texto_pagina = page.extract_text()
                                
                                # Verificar se a página contém dados de boleto
                                if texto_pagina and ('Pagador:' in texto_pagina or 'Valor do Documento' in texto_pagina):
                                    dados = extrair_dados_boleto_pagina(pdf_path, pagina_num, texto_pagina)
                                    
                                    # Verificar se extraiu dados válidos
                                    if dados['nome_cliente'] or dados['valor']:
                                        dados_paginas.append(dados)
                                        self.log_message(f"  ✅ Página {pagina_num}: {dados['nome_cliente']} - R$ {dados['valor']}", "SUCCESS")
                                    else:
                                        self.log_message(f"  ⚠️ Página {pagina_num}: Dados insuficientes, ignorando", "WARNING")
                                else:
                                    self.log_message(f"  ⚠️ Página {pagina_num}: Não parece ser um boleto, ignorando", "WARNING")
                                    
                            except Exception as e:
                                self.log_message(f"  ❌ Erro ao processar página {pagina_num}: {e}", "ERROR")
                    
                    return dados_paginas

                # Processar PDFs
                arquivos = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]

                if not arquivos:
                    self.log_message(f"Nenhum PDF encontrado na pasta: {folder_path}", "WARNING")
                    return

                todos_dados = []
                total_boletos = 0

                for arquivo in arquivos:
                    caminho = os.path.join(folder_path, arquivo)
                    self.log_message(f"📄 Extraindo dados de: {arquivo}", "INFO")
                    try:
                        dados_paginas = extrair_dados_boleto(caminho)
                        todos_dados.extend(dados_paginas)
                        total_boletos += len(dados_paginas)
                        self.log_message(f"✅ {len(dados_paginas)} boleto(s) extraído(s) de {arquivo}", "SUCCESS")
                    except Exception as e:
                        self.log_message(f"❌ Erro ao processar {arquivo}: {e}", "ERROR")

                if todos_dados:
                    df = pd.DataFrame(todos_dados)
                    
                    # Gerar estatísticas
                    estatisticas = self.gerar_estatisticas_pdfs(df, arquivos)
                    
                    # Salvar no diretório do executável
                    csv_path = os.path.join(self.get_app_base_path(), 'boletos_extraidos.csv')
                    df.to_csv(csv_path, index=False, encoding='utf-8', sep=';')
                    
                    # Exibir estatísticas
                    self.log_message(f"✅ Dados extraídos de {total_boletos} boletos ({len(arquivos)} arquivos) e salvos em {csv_path}", "SUCCESS")
                    self.log_message(f"📊 Estatísticas: {estatisticas}", "INFO")
                    self.update_data_status(True)
                else:
                    self.log_message("❌ Nenhum dado extraído.", "WARNING")
                    
            except Exception as e:
                self.log_message(f"❌ Erro durante extração: {e}", "ERROR")
        
        threading.Thread(target=extract_thread, daemon=True).start()
    
    def gerar_estatisticas_pdfs(self, df, arquivos):
        """Gera estatísticas sobre os PDFs processados"""
        try:
            # Estatísticas por arquivo
            stats_por_arquivo = df.groupby('arquivo_pdf').agg({
                'pagina': ['count', 'min', 'max'],
                'valor': 'sum'
            }).round(2)
            
            # Contar arquivos com múltiplas páginas
            arquivos_multiplas_paginas = 0
            total_paginas_multiplas = 0
            
            for arquivo in arquivos:
                dados_arquivo = df[df['arquivo_pdf'] == arquivo]
                if len(dados_arquivo) > 1:
                    arquivos_multiplas_paginas += 1
                    total_paginas_multiplas += len(dados_arquivo)
            
            # Estatísticas gerais
            total_arquivos = len(arquivos)
            total_boletos = len(df)
            valor_total = df['valor'].astype(float).sum()
            
            estatisticas = {
                'total_arquivos': total_arquivos,
                'total_boletos': total_boletos,
                'arquivos_com_multiplas_paginas': arquivos_multiplas_paginas,
                'total_paginas_multiplas': total_paginas_multiplas,
                'valor_total': f"R$ {valor_total:,.2f}",
                'media_boletos_por_arquivo': round(total_boletos / total_arquivos, 2) if total_arquivos > 0 else 0
            }
            
            # Formatar mensagem
            msg = f"{total_arquivos} arquivo(s), {total_boletos} boleto(s) total"
            if arquivos_multiplas_paginas > 0:
                msg += f", {arquivos_multiplas_paginas} arquivo(s) com múltiplas páginas ({total_paginas_multiplas} páginas)"
            msg += f", valor total: {estatisticas['valor_total']}"
            
            return msg
            
        except Exception as e:
            return f"Erro ao gerar estatísticas: {e}"
    
    def load_data(self):
        """Carrega dados do CSV"""
        try:
            # Determinar o caminho do arquivo CSV baseado no diretório do executável
            csv_path = os.path.join(self.get_app_base_path(), 'boletos_extraidos.csv')
            
            if not os.path.exists(csv_path):
                self.log_message(f"❌ Arquivo boletos_extraidos.csv não encontrado em: {csv_path}", "ERROR")
                self.log_message("📄 Execute primeiro a extração de PDFs da pasta selecionada", "WARNING")
                return
            
            # Carregar dados
            df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
            
            if df.empty:
                self.log_message("❌ Nenhum dado encontrado no CSV!", "ERROR")
                return
            
            self.current_data = df
            self.update_data_display(df)
            self.update_data_status(True)
            
            self.log_message(f"✅ Dados carregados: {len(df)} registros", "SUCCESS")
            self.log_message("📋 Selecione os boletos que deseja processar clicando nos checkboxes", "INFO")
            self.log_message("💡 Use os botões 'Selecionar Todos', 'Desmarcar Todos' ou 'Inverter Seleção'", "INFO")
            
        except Exception as e:
            self.log_message(f"❌ Erro ao carregar dados: {e}", "ERROR")
        finally:
            self.log_message("📝 Ação de carregar dados finalizada.", "INFO")
    
    def update_data_display(self, df):
        """Atualiza a exibição dos dados"""
        # Limpar treeview e estados
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        self.checkbox_states.clear()
        
        # Adicionar dados com checkboxes
        for index, (_, row) in enumerate(df.iterrows()):
            item_id = self.data_tree.insert('', tk.END, values=(
                '☐',  # Checkbox vazio
                row.get('arquivo_pdf', ''),
                row.get('pagina', ''),
                row.get('nome_cliente', ''),
                f"R$ {row.get('valor', '0')}",
                row.get('vencimento', ''),
                row.get('turma', '')
            ))
            # Inicializar estado do checkbox como desmarcado
            self.checkbox_states[item_id] = False
    
    def on_tree_click(self, event):
        """Manipula cliques no treeview para alternar checkboxes"""
        region = self.data_tree.identify("region", event.x, event.y)
        if region == "heading":
            return
        
        item = self.data_tree.identify_row(event.y)
        if not item:
            return
        
        column = self.data_tree.identify_column(event.x)
        if column == '#1':  # Coluna do checkbox
            # Obter dados do item antes de alterar
            item_values = self.data_tree.item(item, 'values')
            nome_cliente = item_values[3] if len(item_values) > 3 else 'N/A'
            
            # Alternar estado do checkbox
            current_state = self.checkbox_states.get(item, False)
            new_state = not current_state
            self.checkbox_states[item] = new_state
            
            # Atualizar visual do checkbox
            values = list(self.data_tree.item(item, 'values'))
            values[0] = '☑' if new_state else '☐'
            self.data_tree.item(item, values=values)
            
            # Log detalhado do clique
            self.log_message(f"🖱️ Clique no checkbox: {nome_cliente} - Estado: {current_state} → {new_state}", "INFO")
            
            # Atualizar contador de selecionados
            self.update_selection_count()
    

    
    def select_all(self):
        """Seleciona todos os boletos"""
        for item in self.data_tree.get_children():
            self.checkbox_states[item] = True
            values = list(self.data_tree.item(item, 'values'))
            values[0] = '☑'
            self.data_tree.item(item, values=values)
        self.update_selection_count()
        self.log_message("✅ Todos os boletos selecionados", "SUCCESS")
    
    def deselect_all(self):
        """Desmarca todos os boletos"""
        for item in self.data_tree.get_children():
            self.checkbox_states[item] = False
            values = list(self.data_tree.item(item, 'values'))
            values[0] = '☐'
            self.data_tree.item(item, values=values)
        self.update_selection_count()
        self.log_message("❌ Todos os boletos desmarcados", "WARNING")
    
    def invert_selection(self):
        """Inverte a seleção atual"""
        for item in self.data_tree.get_children():
            current_state = self.checkbox_states.get(item, False)
            self.checkbox_states[item] = not current_state
            values = list(self.data_tree.item(item, 'values'))
            values[0] = '☑' if self.checkbox_states[item] else '☐'
            self.data_tree.item(item, values=values)
        self.update_selection_count()
        self.log_message("🔄 Seleção invertida", "INFO")
    
    def update_selection_count(self):
        """Atualiza o contador de boletos selecionados"""
        selected_count = sum(1 for state in self.checkbox_states.values() if state)
        total_count = len(self.checkbox_states)
        
        # Log detalhado dos itens selecionados
        if selected_count > 0:
            selected_items = []
            for item, state in self.checkbox_states.items():
                if state:
                    item_values = self.data_tree.item(item, 'values')
                    nome_cliente = item_values[3] if len(item_values) > 3 else 'N/A'
                    selected_items.append(nome_cliente)
            
            self.log_message(f"📊 {selected_count}/{total_count} boletos selecionados: {', '.join(selected_items)}", "INFO")
        else:
            self.log_message(f"📊 {selected_count}/{total_count} boletos selecionados", "INFO")
    
    def get_selected_data(self):
        """Retorna apenas os dados dos boletos selecionados"""
        if self.current_data is None:
            return None
        
        selected_indices = []
        tree_items = self.data_tree.get_children()
        
        # Log detalhado para debug
        self.log_message(f"🔍 Verificando seleção: {len(tree_items)} itens na árvore", "INFO")
        
        # Criar mapeamento entre item da árvore e índice do DataFrame
        # Usar os dados do item da árvore para encontrar o índice correto no DataFrame
        for i, item in enumerate(tree_items):
            checkbox_state = self.checkbox_states.get(item, False)
            
            # Obter dados do item da árvore
            item_values = self.data_tree.item(item, 'values')
            nome_cliente = item_values[3] if len(item_values) > 3 else ''
            arquivo = item_values[1] if len(item_values) > 1 else ''
            pagina = item_values[2] if len(item_values) > 2 else ''
            
            self.log_message(f"  Item {i}: {item} - Cliente: {nome_cliente} - Selecionado: {checkbox_state}", "INFO")
            
            if checkbox_state:
                # Encontrar o índice correto no DataFrame baseado nos dados
                # Procurar por correspondência exata
                matching_indices = []
                for idx, (_, row) in enumerate(self.current_data.iterrows()):
                    if (row.get('nome_cliente', '') == nome_cliente and 
                        row.get('arquivo_pdf', '') == arquivo and 
                        str(row.get('pagina', '')) == str(pagina)):
                        matching_indices.append(idx)
                
                if matching_indices:
                    # Usar o primeiro índice encontrado
                    selected_indices.append(matching_indices[0])
                    self.log_message(f"  ✅ Adicionado índice {matching_indices[0]} para cliente: {nome_cliente}", "INFO")
                else:
                    # Fallback: usar índice baseado na posição (comportamento anterior)
                    selected_indices.append(i)
                    self.log_message(f"  ⚠️ Usando índice fallback {i} para cliente: {nome_cliente}", "WARNING")
        
        if not selected_indices:
            self.log_message("❌ Nenhum boleto selecionado!", "ERROR")
            return None
        
        # Log para debug
        self.log_message(f"📋 Índices selecionados: {selected_indices}", "INFO")
        
        selected_data = self.current_data.iloc[selected_indices]
        self.log_message(f"✅ {len(selected_data)} boletos selecionados para processamento", "SUCCESS")
        
        # Log dos dados selecionados
        for i, (_, row) in enumerate(selected_data.iterrows()):
            self.log_message(f"  Boleto {i+1}: {row.get('nome_cliente', 'N/A')}", "INFO")
        
        return selected_data
        

    
    def update_data_status(self, loaded):
        """Atualiza status dos dados"""
        if loaded:
            self.data_status_label.config(text="✅ Dados carregados", fg='#27ae60')
        else:
            self.data_status_label.config(text="❌ Dados não carregados", fg='#e74c3c')
    
    def update_webiss_status(self, connected):
        """Atualiza status do WebISS"""
        if connected:
            self.webiss_status_label.config(text="✅ WebISS conectado", fg='#27ae60')
        else:
            self.webiss_status_label.config(text="❌ WebISS não conectado", fg='#e74c3c')
    
    def update_license_status(self):
        """Atualiza informações da licença"""
        try:
            from utils.license_checker import LicenseChecker
            license_checker = LicenseChecker()
            info = license_checker.obter_info_licenca()
            
            if info:
                self.license_status_label.config(
                    text=f"✅ Licença válida - {info['dias_restantes']} dias restantes",
                    fg='#27ae60'
                )
                self.license_info_label.config(
                    text=f"Cliente: {info['cliente']} | Expira: {info['data_expiracao']} | Versão: {info['versao']}"
                )
            else:
                self.license_status_label.config(
                    text="❌ Licença não encontrada",
                    fg='#e74c3c'
                )
                self.license_info_label.config(text="")
                
        except Exception as e:
            self.license_status_label.config(
                text="❌ Erro ao verificar licença",
                fg='#e74c3c'
            )
            self.license_info_label.config(text="")
    
    def connect_webiss(self):
        """Conecta ao WebISS"""
        def connect_thread():
            try:
                self.log_message("Conectando ao WebISS...", "INFO")
                self.automation = self.webiss_automation(self.settings)
                if not self.automation.setup_driver():
                    self.log_message("❌ Falha ao configurar driver", "ERROR")
                    return
                if not self.automation.login():
                    self.log_message("❌ Falha no login", "ERROR")
                    return
                self.update_webiss_status(True)
                self.log_message("✅ Conectado ao WebISS com sucesso!", "SUCCESS")
            except Exception as e:
                self.log_message(f"❌ Erro ao conectar: {e}", "ERROR")
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def start_automation(self):
        """Inicia a automação completa"""
        self.log_message("🚀 Iniciando automação...", "INFO")
        
        if self.current_data is None:
            self.log_message("❌ Carregue os dados primeiro!", "ERROR")
            return
        
        self.log_message(f"📊 Dados carregados: {len(self.current_data)} registros", "INFO")
        
        if not self.automation:
            self.log_message("❌ Conecte ao WebISS primeiro!", "ERROR")
            return
        
        self.log_message("✅ WebISS conectado", "INFO")
        
        # Verificar se há boletos selecionados
        self.log_message("🔍 Verificando boletos selecionados...", "INFO")
        
        # Log do estado dos checkboxes antes de chamar get_selected_data
        tree_items = self.data_tree.get_children()
        self.log_message(f"📋 Total de itens na árvore: {len(tree_items)}", "INFO")
        
        selected_count = 0
        for i, item in enumerate(tree_items):
            checkbox_state = self.checkbox_states.get(item, False)
            if checkbox_state:
                selected_count += 1
                item_values = self.data_tree.item(item, 'values')
                nome_cliente = item_values[3] if len(item_values) > 3 else 'N/A'
                self.log_message(f"  ✅ Item {i} selecionado: {nome_cliente}", "INFO")
        
        self.log_message(f"📊 Total de itens selecionados na interface: {selected_count}", "INFO")
        
        selected_data = self.get_selected_data()
        if selected_data is None:
            self.log_message("❌ Nenhum boleto selecionado!", "ERROR")
            return
        
        # Log adicional para debug
        self.log_message(f"📊 Dados selecionados: {len(selected_data)} boletos", "INFO")
        self.log_message(f"📋 Índices dos dados: {list(selected_data.index)}", "INFO")
        
        def automation_thread():
            try:
                self.log_message("🔄 Iniciando thread de automação...", "INFO")
                self.processing = True
                self.update_ui_state()
                # Processar todos os boletos
                self.process_all_boletos()
            except Exception as e:
                self.log_message(f"❌ Erro durante a automação: {e}", "ERROR")
                import traceback
                self.log_message(f"❌ Traceback: {traceback.format_exc()}", "ERROR")
            finally:
                self.processing = False
                self.update_ui_state()
                self.log_message("🏁 Thread de automação finalizada", "INFO")
        
        self.log_message("🔄 Iniciando thread de automação...", "INFO")
        threading.Thread(target=automation_thread, daemon=True).start()
    
    def process_all_boletos(self):
        """Processa apenas os boletos selecionados"""
        # Obter dados selecionados
        self.log_message("🔄 Obtendo dados selecionados em process_all_boletos...", "INFO")
        selected_data = self.get_selected_data()
        if selected_data is None:
            self.log_message("❌ Nenhum dado selecionado em process_all_boletos", "ERROR")
            return
        
        total_boletos = len(selected_data)
        self.log_message(f"🚀 Iniciando processamento de {total_boletos} boletos selecionados", "INFO")
        self.log_message(f"📋 Índices dos dados em process_all_boletos: {list(selected_data.index)}", "INFO")
        
        # Criar lista de tuplas (índice_real, row) para manter os índices originais
        boletos_para_processar = []
        self.log_message("🔧 Criando lista de boletos para processar...", "INFO")
        for idx, (_, row) in enumerate(selected_data.iterrows()):
            # Obter o índice real do DataFrame
            indice_real = selected_data.index[idx]
            boletos_para_processar.append((indice_real, row))
            self.log_message(f"📋 Adicionado boleto {idx+1}: índice {indice_real}, cliente: {row.get('nome_cliente', 'N/A')}", "INFO")
        
        self.log_message(f"✅ Lista criada com {len(boletos_para_processar)} boletos", "INFO")
        
        for posicao, (indice_real, row) in enumerate(boletos_para_processar, 1):
            if not self.processing:  # Verificar se foi interrompido
                self.log_message("⏹️ Processamento interrompido", "WARNING")
                break
            
            self.log_message(f"=== PROCESSANDO BOLETO {posicao}/{total_boletos} (Índice original: {indice_real}) ===", "INFO")
            
            # Processar um boleto
            success = self.process_single_boleto(row, posicao, total_boletos, indice_real)
            
            if success:
                self.log_message(f"✅ Boleto {posicao} processado com sucesso!", "SUCCESS")
            else:
                self.log_message(f"❌ Erro ao processar boleto {posicao}", "ERROR")
                continue
        
        self.log_message("🎉 Processamento dos boletos selecionados concluído!", "SUCCESS")
    
    def process_single_boleto(self, row_data, posicao, total_boletos, indice_real=None):
        """Processa um único boleto"""
        try:
            import time
            # Preparar dados do boleto
            test_data = row_data.to_dict()
            
            # Log do índice real para debug
            if indice_real is not None:
                self.log_message(f"📋 Processando boleto com índice original: {indice_real}", "INFO")
            
            # Extrair turma do campo descrição
            turma = ''
            if 'descricao' in test_data and test_data['descricao']:
                import re
                turma_match = re.search(r'TURMA:\s*([A-Z0-9]+)', test_data['descricao'])
                if turma_match:
                    turma = turma_match.group(1)
            
            # Preparar dados para o teste
            processed_data = {
                'cpf_cnpj': test_data.get('cpf_cnpj', '').replace('.', '').replace('-', ''),
                'nome_cliente': test_data.get('nome_cliente', ''),
                'endereco': test_data.get('endereco', ''),
                'valor': test_data.get('valor', ''),
                'vencimento': test_data.get('vencimento', ''),
                'descricao': test_data.get('descricao', ''),
                'turma': turma
            }
            
            # Extrair CEP do endereço se disponível (múltiplas estratégias)
            if 'endereco' in processed_data and processed_data['endereco']:
                import re
                
                # Estratégia 1: CEP no formato padrão (5 dígitos + hífen + 3 dígitos)
                cep_match = re.search(r'(\d{5})-?(\d{3})', processed_data['endereco'])
                if cep_match:
                    processed_data['cep'] = f"{cep_match.group(1)}-{cep_match.group(2)}"
                    self.log_message(f"✅ CEP extraído do endereço: {processed_data['cep']}", "INFO")
                else:
                    # Estratégia 2: CEP sem hífen (8 dígitos consecutivos)
                    cep_match = re.search(r'(\d{8})', processed_data['endereco'])
                    if cep_match:
                        cep = cep_match.group(1)
                        processed_data['cep'] = f"{cep[:5]}-{cep[5:]}"
                        self.log_message(f"✅ CEP extraído do endereço (sem hífen): {processed_data['cep']}", "INFO")
                    else:
                        # Estratégia 3: Buscar CEP em qualquer lugar do texto
                        cep_match = re.search(r'(\d{5})[.\-\s]*(\d{3})', processed_data['endereco'])
                        if cep_match:
                            processed_data['cep'] = f"{cep_match.group(1)}-{cep_match.group(2)}"
                            self.log_message(f"✅ CEP extraído do endereço (padrão alternativo): {processed_data['cep']}", "INFO")
                        else:
                            self.log_message(f"⚠️ CEP não encontrado no endereço: {processed_data['endereco']}", "WARNING")
                            # Tentar extrair do texto completo se disponível
                            if 'descricao' in processed_data and processed_data['descricao']:
                                cep_match = re.search(r'(\d{5})-?(\d{3})', processed_data['descricao'])
                                if cep_match:
                                    processed_data['cep'] = f"{cep_match.group(1)}-{cep_match.group(2)}"
                                    self.log_message(f"✅ CEP extraído da descrição: {processed_data['cep']}", "INFO")
            else:
                self.log_message("⚠️ Endereço não disponível para extrair CEP", "WARNING")
            
            # Log dos dados processados para debug
            self.log_message(f"Dados processados: {processed_data}", "INFO")
            
            self.log_message(f"Processando: {processed_data['nome_cliente']}", "INFO")
            
            # Navegar para nova NFSe apenas no primeiro boleto
            if posicao == 1:  # Primeiro boleto
                self.log_message("🔄 Primeiro boleto - navegando para nova NFSe...", "INFO")
                if not self.automation.navigate_to_new_nfse():
                    self.log_message("❌ Falha ao navegar para nova NFSe", "ERROR")
                    return False
                time.sleep(1)  # Aguardar carregamento completo
            else:
                self.log_message(f"🔄 Boleto {posicao} - usando nota já criada...", "INFO")
                # Para os demais boletos, não navegar aqui - apenas após emitir a nota anterior

            # Preencher formulário do tomador (Step 2)
            self.log_message("=== PREENCHENDO STEP 2 - TOMADOR ===", "INFO")
            if not self.automation.fill_nfse_form(processed_data):
                self.log_message("❌ Falha ao preencher formulário do tomador", "ERROR")
                return False
            
            # Avançar para Step 3
            self.log_message("=== AVANÇANDO PARA STEP 3 ===", "INFO")
            if not self.automation.click_proximo():
                self.log_message("❌ Falha ao avançar para Step 3", "ERROR")
                return False
            
            # Aguardar carregamento do Step 3
            time.sleep(1)
            
            # Preencher Step 3 usando a função sem scroll
            self.log_message("=== PREENCHENDO STEP 3 SEM SCROLL ===", "INFO")
            if not self.automation.fill_nfse_servicos_sem_scroll(processed_data):
                self.log_message("❌ Falha ao preencher Step 3 sem scroll", "ERROR")
                return False
            
            # Aguardar um pouco para garantir que tudo foi processado
            time.sleep(1)
            
            # Avançar para Step 4
            self.log_message("=== AVANÇANDO PARA STEP 4 ===", "INFO")
            if not self.automation.click_proximo():
                self.log_message("❌ Falha ao avançar para Step 4", "ERROR")
                return False
            
            # Aguardar carregamento do Step 4
            time.sleep(1)
            
            # Preencher Step 4 (valores)
            self.log_message("=== PREENCHENDO STEP 4 - VALORES ===", "INFO")
            if not self.automation.fill_nfse_valores(processed_data):
                self.log_message("❌ Falha ao preencher Step 4", "ERROR")
                return False

            # Clicar em Salvar rascunho
            self.log_message("💾 Salvando rascunho da nota...", "INFO")
            if not self.automation.salvar_rascunho():
                self.log_message("❌ Falha ao salvar rascunho", "ERROR")
                return False

            # Aguardar um pouco para o rascunho ser salvo
            time.sleep(2)

            # Clicar em Emitir nota fiscal
            self.log_message("🚀 Emitindo nota fiscal...", "INFO")
            if not self.automation.emitir_nota_fiscal():
                self.log_message("❌ Falha ao emitir nota fiscal", "ERROR")
                return False

            # Aguardar emissão da nota
            time.sleep(3)

            # Clicar em "Criar" para preparar a próxima nota (apenas se não for o último boleto)
            if posicao < total_boletos:  # Se não for o último boleto
                self.log_message("🔄 Preparando próxima nota...", "INFO")
                if not self.automation.navegar_para_proxima_nota():
                    self.log_message("❌ Falha ao preparar próxima nota", "ERROR")
                    return False  # Falhar se não conseguir preparar próxima nota
                self.log_message("✅ Próxima nota preparada", "SUCCESS")

            self.log_message("✅ Boleto processado e nota emitida com sucesso!", "SUCCESS")
            return True
        except Exception as e:
            self.log_message(f"❌ Erro durante processamento do boleto: {e}", "ERROR")
            return False

    
    def stop_automation(self):
        """Para a automação"""
        self.processing = False
        self.update_ui_state()
        self.log_message("⏹️ Processamento interrompido pelo usuário", "WARNING")
    
    def update_ui_state(self):
        """Atualiza estado da interface"""
        if self.processing:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.extract_button.config(state=tk.DISABLED)
            self.load_button.config(state=tk.DISABLED)
            self.connect_button.config(state=tk.DISABLED)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.extract_button.config(state=tk.NORMAL)
            self.load_button.config(state=tk.NORMAL)
            self.connect_button.config(state=tk.NORMAL)
    
    def run(self):
        """Executa a interface"""
        self.log_message("Interface iniciada com sucesso!", "SUCCESS")
        self.log_message("Siga os passos: 1) Extrair PDFs 2) Carregar Dados 3) Conectar WebISS 4) Iniciar Automação", "INFO")
        
        # Atualizar status da licença
        self.update_license_status()
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log_message("Interrompido pelo usuário", "WARNING")
        finally:
            if self.automation:
                try:
                    self.automation.close()
                    self.log_message("Navegador fechado", "INFO")
                except:
                    pass 