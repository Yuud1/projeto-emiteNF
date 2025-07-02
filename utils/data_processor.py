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
    

    

    
 