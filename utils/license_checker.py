#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Verificação de Licença - Emite Nota
"""

import hashlib
import json
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class LicenseChecker:
    """Sistema de verificação de licença"""
    
    def __init__(self):
        self.chave_secreta = "EmiteNota2024@#$%SecretKey"
        self.arquivo_licenca = "license.json"
    
    def gerar_hash(self, dados):
        """Gera hash SHA-256 dos dados"""
        texto = f"{dados}{self.chave_secreta}"
        return hashlib.sha256(texto.encode('utf-8')).hexdigest()
    
    def verificar_licenca(self):
        """Verifica se a licença é válida"""
        try:
            # Procurar arquivo de licença
            arquivo_licenca = self._encontrar_arquivo_licenca()
            
            if not arquivo_licenca:
                return False, "Arquivo de licença não encontrado. Entre em contato com o suporte."
            
            # Carregar licença
            with open(arquivo_licenca, 'r', encoding='utf-8') as f:
                licenca = json.load(f)
            
            # Verificar estrutura da licença
            if "dados" not in licenca or "hash" not in licenca:
                return False, "Estrutura da licença inválida"
            
            # Verificar hash
            hash_calculado = self.gerar_hash(json.dumps(licenca["dados"], sort_keys=True))
            if hash_calculado != licenca["hash"]:
                return False, "Licença inválida ou corrompida"
            
            # Verificar data de expiração
            data_expiracao = datetime.fromisoformat(licenca["dados"]["data_expiracao"])
            if datetime.now() > data_expiracao:
                dias_expirado = (datetime.now() - data_expiracao).days
                return False, f"Licença expirada há {dias_expirado} dias. Entre em contato para renovação."
            
            # Calcular dias restantes
            dias_restantes = (data_expiracao - datetime.now()).days
            
            # Log da verificação
            logger.info(f"Licença válida para {licenca['dados']['cliente']} - {dias_restantes} dias restantes")
            
            return True, f"Licença válida - {dias_restantes} dias restantes"
            
        except Exception as e:
            logger.error(f"Erro ao verificar licença: {e}")
            return False, f"Erro ao verificar licença: {e}"
    
    def _encontrar_arquivo_licenca(self):
        """Encontra o arquivo de licença"""
        # Procurar no diretório atual
        if os.path.exists(self.arquivo_licenca):
            return self.arquivo_licenca
        
        # Procurar no diretório do executável (quando empacotado)
        if getattr(sys, 'frozen', False):
            exe_dir = Path(sys.executable).parent
            licenca_path = exe_dir / self.arquivo_licenca
            if licenca_path.exists():
                return str(licenca_path)
        
        return None
    
    def obter_info_licenca(self):
        """Obtém informações da licença"""
        try:
            arquivo_licenca = self._encontrar_arquivo_licenca()
            
            if not arquivo_licenca:
                return None
            
            with open(arquivo_licenca, 'r', encoding='utf-8') as f:
                licenca = json.load(f)
            
            data_expiracao = datetime.fromisoformat(licenca["dados"]["data_expiracao"])
            dias_restantes = (data_expiracao - datetime.now()).days
            
            return {
                "cliente": licenca["dados"]["cliente"],
                "data_criacao": licenca["dados"]["data_criacao"][:10],
                "data_expiracao": licenca["dados"]["data_expiracao"][:10],
                "dias_restantes": dias_restantes,
                "versao": licenca["dados"]["versao"]
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter informações da licença: {e}")
            return None 