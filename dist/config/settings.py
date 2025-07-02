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
        # Carregar configurações do arquivo .env se existir
        self.load_from_env_file('.env')
        
        # Configurações do WebISS (com fallback para variáveis de ambiente)
        self.username = os.getenv('WEBISS_USERNAME', self.username if hasattr(self, 'username') else '')
        self.password = os.getenv('WEBISS_PASSWORD', self.password if hasattr(self, 'password') else '')
        self.webiss_url = os.getenv('WEBISS_URL', self.webiss_url if hasattr(self, 'webiss_url') else 'https://webiss.exemplo.com')
        
        # Configurações de automação (com fallback para variáveis de ambiente)
        self.headless_mode = os.getenv('HEADLESS_MODE', str(self.headless_mode if hasattr(self, 'headless_mode') else False)).lower() == 'true'
        self.timeout = int(os.getenv('TIMEOUT', str(self.timeout if hasattr(self, 'timeout') else 15)))
        self.delay_between_actions = float(os.getenv('DELAY_BETWEEN_ACTIONS', str(self.delay_between_actions if hasattr(self, 'delay_between_actions') else 2.0)))
        
        # Configurações de arquivos (com fallback para variáveis de ambiente)
        self.data_directory = os.getenv('DATA_DIRECTORY', self.data_directory if hasattr(self, 'data_directory') else 'data')
        self.logs_directory = os.getenv('LOGS_DIRECTORY', self.logs_directory if hasattr(self, 'logs_directory') else 'logs')
        self.mappings_file = os.getenv('MAPPINGS_FILE', self.mappings_file if hasattr(self, 'mappings_file') else 'config/field_mappings.json')
        
        # Configurações de validação
        self.required_fields = [
            'nome_cliente',
            'cpf_cnpj', 
            'valor'
        ]
        
        # Campos opcionais do WebISS
        self.optional_fields = [
            'descricao',
            'endereco',
            'telefone',
            'email',
            'observacoes'
        ]
        
        # Criar diretórios se não existirem
        self._create_directories()
    
    def _create_directories(self):
        """Cria diretórios necessários se não existirem"""
        directories = [self.data_directory, self.logs_directory]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Diretório criado: {directory}")
    
    def validate(self) -> bool:
        """
        Valida se as configurações estão corretas
        
        Returns:
            bool: True se configurações válidas
        """
        errors = []
        
        # Verifica credenciais do WebISS
        if not self.username:
            errors.append("WEBISS_USERNAME não configurado")
        
        if not self.password:
            errors.append("WEBISS_PASSWORD não configurado")
        
        if not self.webiss_url or self.webiss_url == 'https://webiss.exemplo.com':
            errors.append("WEBISS_URL não configurado ou inválido")
        
        # Verifica valores numéricos
        if self.timeout <= 0:
            errors.append("TIMEOUT deve ser maior que zero")
        
        if self.delay_between_actions < 0:
            errors.append("DELAY_BETWEEN_ACTIONS deve ser maior ou igual a zero")
        
        if errors:
            for error in errors:
                logger.error(f"Erro de configuração: {error}")
            return False
        
        logger.info("Configurações validadas com sucesso")
        return True
    
    def get_all_fields(self) -> list:
        """Retorna todos os campos disponíveis"""
        return self.required_fields + self.optional_fields
    
    def get_webiss_config(self) -> dict:
        """Retorna configurações específicas do WebISS"""
        return {
            'username': self.username,
            'password': self.password,
            'url': self.webiss_url,
            'timeout': self.timeout,
            'headless': self.headless_mode
        }
    
    def get_automation_config(self) -> dict:
        """Retorna configurações de automação"""
        return {
            'delay_between_actions': self.delay_between_actions,
            'timeout': self.timeout,
            'headless_mode': self.headless_mode
        }
    
    def save_to_env_file(self, file_path: str = '.env'):
        """
        Salva configurações em arquivo .env
        
        Args:
            file_path: Caminho do arquivo .env
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"WEBISS_USERNAME={self.username}\n")
                f.write(f"WEBISS_PASSWORD={self.password}\n")
                f.write(f"WEBISS_URL={self.webiss_url}\n")
                f.write(f"HEADLESS_MODE={str(self.headless_mode).lower()}\n")
                f.write(f"TIMEOUT={self.timeout}\n")
                f.write(f"DELAY_BETWEEN_ACTIONS={self.delay_between_actions}\n")
                f.write(f"DATA_DIRECTORY={self.data_directory}\n")
                f.write(f"LOGS_DIRECTORY={self.logs_directory}\n")
                f.write(f"MAPPINGS_FILE={self.mappings_file}\n")
            
            logger.info(f"Configurações salvas em: {file_path}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar configurações: {e}")
    
    def load_from_env_file(self, file_path: str = '.env'):
        """
        Carrega configurações de arquivo .env
        
        Args:
            file_path: Caminho do arquivo .env
        """
        try:
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
                            elif key == 'MAPPINGS_FILE':
                                self.mappings_file = value
                
                logger.info(f"Configurações carregadas de: {file_path}")
            else:
                logger.warning(f"Arquivo de configuração não encontrado: {file_path}")
                
        except Exception as e:
            logger.error(f"Erro ao carregar configurações: {e}") 