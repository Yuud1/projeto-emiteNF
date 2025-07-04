#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar funcionalidade do CEP com select2 da inscrição municipal
"""

import os
import sys
import logging
import time

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Settings
from webiss_automation import WebISSAutomation

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def testar_cep_select2():
    """Testa a funcionalidade do CEP com select2 da inscrição municipal"""
    
    try:
        logger.info("=== TESTE CEP COM SELECT2 ===")
        
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
        
        # Dados de teste com CEP conhecido
        test_data = {
            'cpf_cnpj': '12345678901',
            'nome_cliente': 'Teste CEP Select Normal',
            'endereco': 'Rua Teste, 123 - Palmas - 77016-640',
            'valor': '100.00',
            'vencimento': '15/12/2024',
            'descricao': 'Teste de CEP com select normal (comboInscricao)',
            'turma': 'TESTE',
            'cep': '77016-640'  # CEP específico para teste
        }
        
        logger.info(f"🧪 Testando com CEP: {test_data['cep']}")
        
        # Preencher formulário do tomador (Step 2)
        logger.info("=== PREENCHENDO STEP 2 - TOMADOR ===")
        if not automation.fill_nfse_form(test_data):
            logger.error("❌ Falha ao preencher formulário do tomador")
            return False
        
        # Aguardar um pouco para ver o resultado
        time.sleep(3)
        
        logger.info("✅ Teste concluído! Verifique se o CEP foi preenchido corretamente.")
        logger.info("🚀 Navegador mantido aberto para inspeção")
        
        # Manter o navegador aberto para inspeção
        input("Pressione ENTER para fechar o navegador...")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro durante o teste: {e}")
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
    success = testar_cep_select2()
    sys.exit(0 if success else 1) 