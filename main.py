#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fluxo principal de automação WebISS usando dados reais do PDF
"""

import sys
import os
import logging
import pandas as pd
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Settings
from webiss_automation import WebISSAutomation

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automacao_webiss.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def carregar_dados_reais():
    """Carrega os dados reais extraídos do PDF"""
    try:
        # Verificar se o arquivo CSV existe
        if not os.path.exists('boletos_extraidos.csv'):
            logger.error("❌ Arquivo boletos_extraidos.csv não encontrado!")
            logger.info("Execute primeiro a extração de PDFs pela interface gráfica")
            return None
        
        # Carregar dados do CSV
        df = pd.read_csv('boletos_extraidos.csv', sep=';', encoding='utf-8')
        
        if df.empty:
            logger.error("❌ Nenhum dado encontrado no CSV!")
            return None
        
        # Pegar o primeiro registro
        dados = df.iloc[0].to_dict()
        
        # Extrair turma do campo descrição
        turma = ''
        if 'descricao' in dados and dados['descricao']:
            import re
            turma_match = re.search(r'TURMA:\s*([A-Z0-9]+)', dados['descricao'])
            if turma_match:
                turma = turma_match.group(1)
        
        # Preparar dados para o teste
        test_data = {
            'cpf_cnpj': dados.get('cpf_cnpj', '').replace('.', '').replace('-', ''),
            'nome_cliente': dados.get('nome_cliente', ''),
            'endereco': dados.get('endereco', ''),
            'valor': dados.get('valor', ''),
            'vencimento': dados.get('vencimento', ''),
            'descricao': dados.get('descricao', ''),
            'turma': turma
        }
        
        # Extrair CEP do endereço se disponível
        if 'endereco' in test_data and test_data['endereco']:
            import re
            cep_match = re.search(r'(\d{5})-?(\d{3})', test_data['endereco'])
            if cep_match:
                test_data['cep'] = f"{cep_match.group(1)}-{cep_match.group(2)}"
        
        logger.info(f"✅ Dados carregados do PDF: {dados.get('arquivo_pdf', 'N/A')}")
        logger.info(f"Cliente: {test_data['nome_cliente']}")
        logger.info(f"Valor: {test_data['valor']}")
        logger.info(f"Vencimento: {test_data['vencimento']}")
        logger.info(f"Turma: {test_data['turma']}")
        
        return test_data
        
    except Exception as e:
        logger.error(f"❌ Erro ao carregar dados: {e}")
        return None

def main():
    """Função principal da automação"""
    try:
        logger.info("=== INICIANDO AUTOMAÇÃO WEBISS (DADOS REAIS) ===")
        
        # Carregar dados reais do PDF
        test_data = carregar_dados_reais()
        if not test_data:
            return False
        
        # Carregar configurações
        settings = Settings()
        
        # Criar instância da automação
        automation = WebISSAutomation(settings)
        
        # Configurar driver
        if not automation.setup_driver():
            logger.error("❌ Falha ao configurar driver")
            return False
        
        # Fazer login
        if not automation.login():
            logger.error("❌ Falha no login")
            return False
        
        # Navegar para nova NFSe
        if not automation.navigate_to_new_nfse():
            logger.error("❌ Falha ao navegar para nova NFSe")
            return False
        
        # Preencher formulário do tomador (Step 2)
        logger.info("=== PREENCHENDO STEP 2 - TOMADOR ===")
        if not automation.fill_nfse_form(test_data):
            logger.error("❌ Falha ao preencher formulário do tomador")
            return False
        
        # Avançar para Step 3
        logger.info("=== AVANÇANDO PARA STEP 3 ===")
        if not automation.click_proximo():
            logger.error("❌ Falha ao avançar para Step 3")
            return False
        
        # Aguardar carregamento do Step 3
        import time
        time.sleep(1)
        
        # Preencher Step 3 usando a função sem scroll
        logger.info("=== PREENCHENDO STEP 3 SEM SCROLL ===")
        if not automation.fill_nfse_servicos_sem_scroll(test_data):
            logger.error("❌ Falha ao preencher Step 3 sem scroll")
            return False
        
        # Aguardar um pouco para garantir que tudo foi processado
        time.sleep(1)
        
        # Avançar para Step 4
        logger.info("=== AVANÇANDO PARA STEP 4 ===")
        if not automation.click_proximo():
            logger.error("❌ Falha ao avançar para Step 4")
            return False
        
        # Aguardar carregamento do Step 4
        time.sleep(1)
        
        # Preencher Step 4 (valores)
        logger.info("=== PREENCHENDO STEP 4 - VALORES ===")
        if not automation.fill_nfse_valores(test_data):
            logger.error("❌ Falha ao preencher Step 4")
            return False
        
        # Aguardar um pouco para ver o resultado
        time.sleep(2)
        
        logger.info("✅ Automação concluída com sucesso!")
        logger.info("Verifique os screenshots em logs/ para ver se não houve scroll")
        logger.info("🚀 Navegador mantido aberto para inspeção")
        
        # Manter o navegador aberto para inspeção
        input("Pressione ENTER para fechar o navegador...")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro durante a automação: {e}")
        return False
    
    finally:
        # Fechar driver apenas se o usuário quiser
        if 'automation' in locals():
            try:
                automation.close()
                logger.info("Navegador fechado")
            except:
                pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 