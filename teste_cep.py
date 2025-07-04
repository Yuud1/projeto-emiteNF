#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar extração do CEP dos PDFs
"""

import os
import re
import pandas as pd
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def testar_extracao_cep():
    """Testa a extração do CEP dos dados extraídos"""
    
    # Verificar se existe o arquivo CSV
    csv_path = 'boletos_extraidos.csv'
    if not os.path.exists(csv_path):
        logger.error(f"❌ Arquivo {csv_path} não encontrado!")
        logger.info("Execute primeiro a extração de PDFs pela interface gráfica")
        return
    
    # Carregar dados
    try:
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
        logger.info(f"✅ Dados carregados: {len(df)} registros")
    except Exception as e:
        logger.error(f"❌ Erro ao carregar CSV: {e}")
        return
    
    # Testar extração do CEP para cada registro
    logger.info("\n=== TESTANDO EXTRAÇÃO DO CEP ===")
    
    for index, row in df.iterrows():
        logger.info(f"\n--- Registro {index + 1} ---")
        logger.info(f"Nome: {row.get('nome_cliente', 'N/A')}")
        logger.info(f"Endereço original: {row.get('endereco', 'N/A')}")
        
        # Testar extração do CEP
        endereco = row.get('endereco', '')
        cep_extraido = None
        
        if endereco:
            # Estratégia 1: CEP no formato padrão
            cep_match = re.search(r'(\d{5})-?(\d{3})', endereco)
            if cep_match:
                cep_extraido = f"{cep_match.group(1)}-{cep_match.group(2)}"
                logger.info(f"✅ CEP extraído (padrão): {cep_extraido}")
            else:
                # Estratégia 2: CEP sem hífen
                cep_match = re.search(r'(\d{8})', endereco)
                if cep_match:
                    cep = cep_match.group(1)
                    cep_extraido = f"{cep[:5]}-{cep[5:]}"
                    logger.info(f"✅ CEP extraído (sem hífen): {cep_extraido}")
                else:
                    # Estratégia 3: Buscar CEP em qualquer lugar
                    cep_match = re.search(r'(\d{5})[.\-\s]*(\d{3})', endereco)
                    if cep_match:
                        cep_extraido = f"{cep_match.group(1)}-{cep_match.group(2)}"
                        logger.info(f"✅ CEP extraído (alternativo): {cep_extraido}")
                    else:
                        logger.warning("❌ CEP não encontrado no endereço")
                        
                        # Tentar extrair da descrição
                        descricao = row.get('descricao', '')
                        if descricao:
                            cep_match = re.search(r'(\d{5})-?(\d{3})', descricao)
                            if cep_match:
                                cep_extraido = f"{cep_match.group(1)}-{cep_match.group(2)}"
                                logger.info(f"✅ CEP extraído da descrição: {cep_extraido}")
        else:
            logger.warning("⚠️ Endereço vazio")
        
        if cep_extraido:
            logger.info(f"🎯 CEP final: {cep_extraido}")
        else:
            logger.error("❌ Nenhum CEP foi extraído")
    
    logger.info("\n=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    testar_extracao_cep() 