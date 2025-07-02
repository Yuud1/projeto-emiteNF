#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processador de Dados - Importação e processamento de boletos
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import json

logger = logging.getLogger(__name__)

class DataProcessor:
    """Classe para processar dados de boletos"""
    
    def __init__(self):
        self.data = None
        self.field_mappings = {}
        self.processed_data = []
        
    def load_data(self, file_path: str) -> bool:
        """
        Carrega dados de um arquivo (CSV, Excel, etc.)
        
        Args:
            file_path: Caminho para o arquivo
            
        Returns:
            bool: True se carregado com sucesso
        """
        try:
            file_path = Path(file_path)
            
            if file_path.suffix.lower() == '.csv':
                # Tenta diferentes encodings e separadores
                encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
                separators = [';', ',']
                
                for encoding in encodings:
                    for sep in separators:
                        try:
                            self.data = pd.read_csv(file_path, encoding=encoding, sep=sep)
                            logger.info(f"CSV carregado com encoding {encoding} e separador '{sep}'")
                            break
                        except UnicodeDecodeError:
                            continue
                        except Exception:
                            continue
                    else:
                        continue
                    break
                else:
                    logger.error("Não foi possível carregar o CSV com nenhum encoding/separador")
                    return False
                    
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                self.data = pd.read_excel(file_path)
            else:
                logger.error(f"Formato de arquivo não suportado: {file_path.suffix}")
                return False
                
            logger.info(f"Dados carregados com sucesso: {len(self.data)} registros")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            return False
    
    def get_columns(self) -> List[str]:
        """Retorna lista de colunas disponíveis"""
        if self.data is not None:
            return self.data.columns.tolist()
        return []
    
    def set_field_mapping(self, webiss_field: str, data_column: str):
        """
        Define mapeamento entre campo do WebISS e coluna dos dados
        
        Args:
            webiss_field: Nome do campo no WebISS
            data_column: Nome da coluna nos dados
        """
        self.field_mappings[webiss_field] = data_column
        logger.info(f"Mapeamento definido: {webiss_field} -> {data_column}")
    
    def get_field_mappings(self) -> Dict[str, str]:
        """Retorna mapeamentos atuais"""
        return self.field_mappings.copy()
    
    def process_data(self) -> List[Dict[str, Any]]:
        """
        Processa os dados usando os mapeamentos definidos
        
        Returns:
            Lista de dicionários com dados processados
        """
        if self.data is None:
            logger.error("Nenhum dado carregado")
            return []
            
        if not self.field_mappings:
            logger.error("Nenhum mapeamento definido")
            return []
        
        try:
            processed = []
            
            for index, row in self.data.iterrows():
                record = {}
                for webiss_field, data_column in self.field_mappings.items():
                    if data_column in row:
                        record[webiss_field] = row[data_column]
                    else:
                        logger.warning(f"Coluna {data_column} não encontrada no registro {index}")
                        record[webiss_field] = ""
                
                processed.append(record)
            
            self.processed_data = processed
            logger.info(f"Dados processados: {len(processed)} registros")
            return processed
            
        except Exception as e:
            logger.error(f"Erro ao processar dados: {e}")
            return []
    
    def get_processed_data(self) -> List[Dict[str, Any]]:
        """Retorna dados processados"""
        return self.processed_data.copy()
    
    def save_mappings(self, file_path: str):
        """Salva mapeamentos em arquivo JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.field_mappings, f, indent=2, ensure_ascii=False)
            logger.info(f"Mapeamentos salvos em: {file_path}")
        except Exception as e:
            logger.error(f"Erro ao salvar mapeamentos: {e}")
    
    def load_mappings(self, file_path: str):
        """Carrega mapeamentos de arquivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.field_mappings = json.load(f)
            logger.info(f"Mapeamentos carregados de: {file_path}")
        except Exception as e:
            logger.error(f"Erro ao carregar mapeamentos: {e}")
    
    def validate_data(self) -> Dict[str, List[str]]:
        """
        Valida os dados processados
        
        Returns:
            Dicionário com erros encontrados
        """
        errors = {
            'missing_fields': [],
            'invalid_data': [],
            'empty_records': []
        }
        
        if not self.processed_data:
            errors['empty_records'].append("Nenhum dado processado")
            return errors
        
        required_fields = ['nome_cliente', 'cpf_cnpj', 'valor']
        
        for i, record in enumerate(self.processed_data):
            # Verifica campos obrigatórios
            for field in required_fields:
                if field not in record or not record[field]:
                    errors['missing_fields'].append(f"Registro {i+1}: Campo {field} vazio")
            
            # Validações específicas
            if 'cpf_cnpj' in record and record['cpf_cnpj']:
                if not self._validate_cpf_cnpj(record['cpf_cnpj']):
                    errors['invalid_data'].append(f"Registro {i+1}: CPF/CNPJ inválido")
            
            if 'valor' in record and record['valor']:
                try:
                    float(record['valor'])
                except ValueError:
                    errors['invalid_data'].append(f"Registro {i+1}: Valor inválido")
        
        return errors
    
    def _validate_cpf_cnpj(self, cpf_cnpj: str) -> bool:
        """Valida CPF ou CNPJ"""
        # Remove caracteres especiais
        cpf_cnpj = ''.join(filter(str.isdigit, str(cpf_cnpj)))
        
        if len(cpf_cnpj) == 11:  # CPF
            return self._validate_cpf(cpf_cnpj)
        elif len(cpf_cnpj) == 14:  # CNPJ
            return self._validate_cnpj(cpf_cnpj)
        else:
            return False
    
    def _validate_cpf(self, cpf: str) -> bool:
        """Valida CPF"""
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        # Validação dos dígitos verificadores
        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if int(cpf[i]) != digit:
                return False
        return True
    
    def _validate_cnpj(self, cnpj: str) -> bool:
        """Valida CNPJ"""
        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False
        
        # Validação dos dígitos verificadores
        for i in range(12, 14):
            value = sum((int(cnpj[num]) * (2 + (i - num) % 8) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if int(cnpj[i]) != digit:
                return False
        return True 