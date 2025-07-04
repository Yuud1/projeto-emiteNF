#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações do Sistema
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Settings:
    """Classe para gerenciar configurações do sistema"""
    
    def __init__(self):
        # Inicializar valores padrão
        self.username = ''
        self.password = ''
        self.webiss_url = 'https://palmasto.webiss.com.br'
        self.headless_mode = False
        self.timeout = 15
        self.delay_between_actions = 2.0
        self.data_directory = 'data'
        self.logs_directory = 'logs'
        
        # Carregar configurações do arquivo .env se existir
        self.load_from_env_file('.env')
        
        # Configurações do WebISS (com fallback para variáveis de ambiente)
        self.username = os.getenv('WEBISS_USERNAME', self.username)
        self.password = os.getenv('WEBISS_PASSWORD', self.password)
        self.webiss_url = os.getenv('WEBISS_URL', self.webiss_url)
        
        # Configurações de automação (com fallback para variáveis de ambiente)
        self.headless_mode = os.getenv('HEADLESS_MODE', str(self.headless_mode if hasattr(self, 'headless_mode') else False)).lower() == 'true'
        self.timeout = int(os.getenv('TIMEOUT', str(self.timeout if hasattr(self, 'timeout') else 15)))
        self.delay_between_actions = float(os.getenv('DELAY_BETWEEN_ACTIONS', str(self.delay_between_actions if hasattr(self, 'delay_between_actions') else 2.0)))
        
        # Configurações de arquivos (com fallback para variáveis de ambiente)
        self.data_directory = os.getenv('DATA_DIRECTORY', self.data_directory if hasattr(self, 'data_directory') else 'data')
        self.logs_directory = os.getenv('LOGS_DIRECTORY', self.logs_directory if hasattr(self, 'logs_directory') else 'logs')
        

        
        # Criar diretórios se não existirem
        self._create_directories()
    
    def _create_directories(self):
        """Cria diretórios necessários se não existirem"""
        directories = [self.data_directory, self.logs_directory]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Diretório criado: {directory}")
    

    

    
    def load_from_env_file(self, file_path: str = '.env'):
        """
        Carrega configurações de arquivo .env
        
        Args:
            file_path: Caminho do arquivo .env
        """
        try:
            # Sempre procurar o arquivo .env no diretório atual
            if not os.path.isabs(file_path):
                file_path = os.path.join(os.getcwd(), file_path)
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            if key == 'WEBISS_USERNAME':
                                self.username = value
                            elif key == 'WEBISS_PASSWORD':
                                self.password = value
                            elif key == 'WEBISS_URL':
                                self.webiss_url = value
                            elif key == 'HEADLESS_MODE':
                                self.headless_mode = value.lower() == 'true'
                            elif key == 'TIMEOUT':
                                self.timeout = int(value)
                            elif key == 'DELAY_BETWEEN_ACTIONS':
                                self.delay_between_actions = float(value)
                            elif key == 'DATA_DIRECTORY':
                                self.data_directory = value
                            elif key == 'LOGS_DIRECTORY':
                                self.logs_directory = value

                
                logger.info(f"Configurações carregadas de: {file_path}")
            else:
                logger.warning(f"Arquivo de configuração não encontrado: {file_path}")
                logger.info("📝 Para configurar suas credenciais:")
                logger.info("   1. Copie o arquivo 'env_exemplo.txt' para '.env'")
                logger.info("   2. Edite o arquivo '.env' com suas credenciais do WebISS")
                logger.info("   3. Execute o aplicativo novamente")
                
        except Exception as e:
            logger.error(f"Erro ao carregar configurações: {e}") 