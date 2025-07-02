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
        
        self.folder_var = tk.StringVar(value='boletos')
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
        
        # Treeview para dados
        columns = ('arquivo', 'cliente', 'valor', 'vencimento', 'turma')
        self.data_tree = ttk.Treeview(data_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        self.data_tree.heading('arquivo', text='Arquivo')
        self.data_tree.heading('cliente', text='Cliente')
        self.data_tree.heading('valor', text='Valor')
        self.data_tree.heading('vencimento', text='Vencimento')
        self.data_tree.heading('turma', text='Turma')
        
        self.data_tree.column('arquivo', width=200)
        self.data_tree.column('cliente', width=200)
        self.data_tree.column('valor', width=100)
        self.data_tree.column('vencimento', width=100)
        self.data_tree.column('turma', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=scrollbar.set)
        
        self.data_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
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
        folder_path = filedialog.askdirectory(
            title="Selecionar pasta com PDFs dos boletos",
            initialdir=os.getcwd()
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
                
                # Executar script de extração com a pasta personalizada
                import subprocess
                import sys
                
                # Criar um script temporário que usa a pasta selecionada
                temp_script = textwrap.dedent(f"""
import pdfplumber
import re
import pandas as pd
import os

def extrair_dados_boleto(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        texto = ""
        for page in pdf.pages:
            texto += page.extract_text() + "\\n"

    # Nome do cliente (Pagador) - removendo CPF/CNPJ que vem depois
    nome = re.search(r'Pagador:\\s*(.+?)(?:\\s+CPF\\s*/\\s*CNPJ|$)', texto)

    # CPF/CNPJ - padrão específico da instituição (no final da linha do endereço)
    cpf_cnpj = ''
    cpf_match = re.search(r'([\\d]{{3}}\\.[\\d]{{3}}\\.[\\d]{{3}}-[\\d]{{2}})', texto)
    if cpf_match:
        cpf_cnpj = cpf_match.group(1)

    # Endereço - extração separada
    endereco = ''
    endereco_match = re.search(r'CPF ?/ ?CNPJ[:\\s]*[\\d.\\-/]+\\s+(.+?PALMAS.*?)\\s*-?\\s*(\\d{{8}})', texto)
    if endereco_match:
        endereco = f"{{endereco_match.group(1)}} - {{endereco_match.group(2)}}"
    else:
        # Busca alternativa para endereço
        endereco_match = re.search(r'(.+?PALMAS.*?)\\s*-?\\s*(\\d{{8}})', texto)
        if endereco_match:
            endereco = f"{{endereco_match.group(1)}} - {{endereco_match.group(2)}}"

    valor = re.search(r'Valor do Documento.*?(\\d{{1,3}}(?:\\.\\d{{3}})*,\\d{{2}})', texto, re.DOTALL)

    vencimento = re.search(r'Local de Pagamento.*?(\\d{{2}}/\\d{{2}}/\\d{{4}})', texto, re.DOTALL)

    descricao = re.search(r'(MENSALIDADE:.*)', texto)

    linha_digitavel = re.search(r'(\\d{{5}}\\.\\d{{5}} \\d{{5}}\\.\\d{{6}} \\d{{5}}\\.\\d{{6}} \\d \\d{{13,14}}-?\\d)', texto)

    # Extrair turma
    turma_match = re.search(r'TURMA[:\\s]+([A-Z0-9]+)', texto)
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

    dados = {{
        'arquivo_pdf': os.path.basename(pdf_path),
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
    }}

    return dados

pasta = r'{folder_path}'

if not os.path.exists(pasta):
    os.makedirs(pasta)
    print(f'Pasta "{{pasta}}" criada. Coloque seus PDFs de boletos nela e rode o script novamente.')
    exit()

arquivos = [f for f in os.listdir(pasta) if f.lower().endswith('.pdf')]

if not arquivos:
    print(f'Nenhum PDF encontrado na pasta "{{pasta}}". Coloque seus boletos lá e rode novamente.')
    exit()

todos_dados = []

for arquivo in arquivos:
    caminho = os.path.join(pasta, arquivo)
    print(f'Extraindo dados de: {{arquivo}}')
    try:
        dados = extrair_dados_boleto(caminho)
        todos_dados.append(dados)
    except Exception as e:
        print(f'Erro ao processar {{arquivo}}: {{e}}')

if todos_dados:
    df = pd.DataFrame(todos_dados)
    df.to_csv('boletos_extraidos.csv', index=False, encoding='utf-8', sep=';')
    print(f'Dados extraídos de {{len(todos_dados)}} boletos e salvos em boletos_extraidos.csv')
else:
    print('Nenhum dado extraído.')
""")
                
                # Salvar script temporário
                temp_script_path = 'temp_extract.py'
                with open(temp_script_path, 'w', encoding='utf-8') as f:
                    f.write(temp_script)
                
                # Executar script temporário
                result = subprocess.run([sys.executable, temp_script_path], 
                                      capture_output=True, text=True, encoding='utf-8')
                
                # Remover script temporário
                try:
                    os.remove(temp_script_path)
                except:
                    pass
                
                if result.returncode == 0:
                    output = result.stdout.strip().splitlines() if result.stdout else []
                    if output:
                        # Log de debug para ver o output completo
                        self.log_message(f"Debug - Output completo: {output}", "INFO")
                        
                        # Procura por uma linha que contenha 'boletos' ou 'Dados extraídos'
                        linha_boletos = next((linha for linha in output if 'boletos' in linha or 'Dados extraídos' in linha), None)
                        if linha_boletos:
                            self.log_message(f"✅ {linha_boletos}", "SUCCESS")
                        else:
                            # Se não encontrar, mostra a última linha ou uma mensagem padrão
                            ultima_linha = output[-1] if output else "Extração concluída"
                            self.log_message(f"✅ {ultima_linha}", "SUCCESS")
                    else:
                        self.log_message("✅ Extração de PDFs concluída com sucesso!", "SUCCESS")
                    self.update_data_status(True)
                else:
                    self.log_message(f"❌ Erro na extração: {result.stderr}", "ERROR")
                    
            except Exception as e:
                self.log_message(f"❌ Erro durante extração: {e}", "ERROR")
        
        threading.Thread(target=extract_thread, daemon=True).start()
    
    def load_data(self):
        """Carrega dados do CSV"""
        try:
            if not os.path.exists('boletos_extraidos.csv'):
                self.log_message("❌ Arquivo boletos_extraidos.csv não encontrado!", "ERROR")
                self.log_message("Execute primeiro a extração de PDFs", "WARNING")
                return
            
            # Carregar dados
            df = pd.read_csv('boletos_extraidos.csv', sep=';', encoding='utf-8')
            
            if df.empty:
                self.log_message("❌ Nenhum dado encontrado no CSV!", "ERROR")
                return
            
            self.current_data = df
            self.update_data_display(df)
            self.update_data_status(True)
            
            self.log_message(f"✅ Dados carregados: {len(df)} registros", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"❌ Erro ao carregar dados: {e}", "ERROR")
        finally:
            self.log_message("📝 Ação de carregar dados finalizada.", "INFO")
    
    def update_data_display(self, df):
        """Atualiza a exibição dos dados"""
        # Limpar treeview
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # Adicionar dados
        for _, row in df.iterrows():
            self.data_tree.insert('', tk.END, values=(
                row.get('arquivo_pdf', ''),
                row.get('nome_cliente', ''),
                f"R$ {row.get('valor', '0')}",
                row.get('vencimento', ''),
                row.get('turma', '')
            ))
        

    
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
        if self.current_data is None:
            self.log_message("❌ Carregue os dados primeiro!", "ERROR")
            return
        if not self.automation:
            self.log_message("❌ Conecte ao WebISS primeiro!", "ERROR")
            return
        def automation_thread():
            try:
                self.processing = True
                self.update_ui_state()
                # Processar todos os boletos
                self.process_all_boletos()
            except Exception as e:
                self.log_message(f"❌ Erro durante a automação: {e}", "ERROR")
            finally:
                self.processing = False
                self.update_ui_state()
        threading.Thread(target=automation_thread, daemon=True).start()
    
    def process_all_boletos(self):
        """Processa todos os boletos de forma cíclica"""
        total_boletos = len(self.current_data)
        self.log_message(f"🚀 Iniciando processamento de {total_boletos} boletos", "INFO")
        self.is_primeiro_boleto = True
        
        for index, (_, row) in enumerate(self.current_data.iterrows(), 1):
            if not self.processing:  # Verificar se foi interrompido
                self.log_message("⏹️ Processamento interrompido", "WARNING")
                break
            
            self.log_message(f"=== PROCESSANDO BOLETO {index}/{total_boletos} ===", "INFO")
            
            # Processar um boleto
            success = self.process_single_boleto(row)
            
            if success:
                self.log_message(f"✅ Boleto {index} processado com sucesso!", "SUCCESS")
            else:
                self.log_message(f"❌ Erro ao processar boleto {index}", "ERROR")
                continue
        
        self.log_message("🎉 Processamento de todos os boletos concluído!", "SUCCESS")
    
    def process_single_boleto(self, row_data):
        """Processa um único boleto"""
        try:
            # Preparar dados do boleto
            test_data = row_data.to_dict()
            
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
            
            # Extrair CEP do endereço se disponível
            if 'endereco' in processed_data and processed_data['endereco']:
                import re
                cep_match = re.search(r'(\d{5})-?(\d{3})', processed_data['endereco'])
                if cep_match:
                    processed_data['cep'] = f"{cep_match.group(1)}-{cep_match.group(2)}"
            
            self.log_message(f"Processando: {processed_data['nome_cliente']}", "INFO")
            
            # Navegar para nova NFSe apenas no primeiro boleto
            if getattr(self, 'is_primeiro_boleto', False):
                if not self.automation.navigate_to_new_nfse():
                    self.log_message("❌ Falha ao navegar para nova NFSe", "ERROR")
                    return False
                self.is_primeiro_boleto = False
            else:
                # Para os demais boletos, clicar apenas em "Criar" no menu lateral
                self.log_message("🔄 Voltando para tela de criação de nota... (clicando apenas em Criar)", "INFO")
                try:
                    from selenium.webdriver.common.by import By
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC
                    criar_menu = WebDriverWait(self.automation.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Criar')]"))
                    )
                    criar_menu.click()
                    import time
                    time.sleep(1.5)
                except Exception as e:
                    self.log_message(f"❌ Falha ao clicar em Criar: {e}", "ERROR")
                    return False

            # Clicar em Próximo para ir ao Step 2
            if not self.automation.click_proximo():
                self.log_message("❌ Falha ao avançar para Step 2", "ERROR")
                return False

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
            import time
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

            self.log_message("✅ Boleto processado com sucesso!", "SUCCESS")
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
        self.log_message("🚀 Interface iniciada com sucesso!", "SUCCESS")
        self.log_message("Siga os passos: 1) Extrair PDFs 2) Carregar Dados 3) Conectar WebISS 4) Iniciar Automação", "INFO")
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