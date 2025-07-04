#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples da interface para verificar logs
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time

class TesteInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Teste Interface")
        self.root.geometry("800x600")
        
        # Log text
        self.log_text = scrolledtext.ScrolledText(self.root, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botão de teste
        self.test_button = tk.Button(self.root, text="Testar Logs", command=self.testar_logs)
        self.test_button.pack(pady=10)
        
        # Botão de teste com thread
        self.test_thread_button = tk.Button(self.root, text="Testar Thread", command=self.testar_thread)
        self.test_thread_button.pack(pady=5)
    
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
        
        # Forçar atualização da interface
        self.root.update()
    
    def testar_logs(self):
        """Testa logs simples"""
        self.log_message("🚀 Iniciando teste de logs...", "INFO")
        self.log_message("📊 Testando diferentes níveis de log", "INFO")
        self.log_message("✅ Log de sucesso", "SUCCESS")
        self.log_message("⚠️ Log de aviso", "WARNING")
        self.log_message("❌ Log de erro", "ERROR")
        self.log_message("🏁 Teste de logs concluído", "SUCCESS")
    
    def testar_thread(self):
        """Testa logs em thread"""
        def thread_func():
            self.log_message("🔄 Iniciando thread de teste...", "INFO")
            time.sleep(1)
            self.log_message("📊 Processando dados...", "INFO")
            time.sleep(1)
            self.log_message("✅ Thread concluída com sucesso", "SUCCESS")
        
        self.log_message("🚀 Iniciando teste com thread...", "INFO")
        threading.Thread(target=thread_func, daemon=True).start()
    
    def run(self):
        self.log_message("✅ Interface de teste iniciada", "SUCCESS")
        self.log_message("💡 Clique nos botões para testar os logs", "INFO")
        self.root.mainloop()

if __name__ == "__main__":
    app = TesteInterface()
    app.run() 