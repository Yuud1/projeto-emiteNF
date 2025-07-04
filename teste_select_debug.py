#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de debug para verificar o select da inscrição municipal
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

def debug_select_inscricao():
    """Debug do select da inscrição municipal"""
    
    try:
        logger.info("=== DEBUG SELECT INSCRIÇÃO MUNICIPAL ===")
        
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
        
        # Dados de teste
        test_data = {
            'cpf_cnpj': '12345678901',
            'nome_cliente': 'Teste Debug Select',
            'endereco': 'Rua Teste, 123 - Palmas - 77016-640',
            'valor': '100.00',
            'vencimento': '15/12/2024',
            'descricao': 'Teste de debug do select',
            'turma': 'TESTE',
            'cep': '77016-640'
        }
        
        logger.info(f"🧪 Testando com CEP: {test_data['cep']}")
        
        # Preencher apenas CPF e nome para ativar o select
        logger.info("=== PREENCHENDO APENAS CPF E NOME ===")
        
        # Preencher CPF
        cpf_xpaths = [
            "//input[@placeholder='Número do documento do tomador']",
            "//input[@name='cpf_cnpj']",
            "//input[@id='cpf_cnpj']"
        ]
        
        for xpath in cpf_xpaths:
            try:
                element = automation.driver.find_element(By.XPATH, xpath)
                if element.is_displayed() and element.is_enabled():
                    automation.driver.execute_script("arguments[0].value = arguments[1];", element, test_data['cpf_cnpj'])
                    automation.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", element)
                    logger.info(f"✅ CPF preenchido: {test_data['cpf_cnpj']}")
                    break
            except:
                continue
        
        # Preencher nome
        nome_xpaths = [
            "//input[@placeholder='Razão social do tomador']",
            "//input[@name='nome']",
            "//input[@id='nome']"
        ]
        
        for xpath in nome_xpaths:
            try:
                element = automation.driver.find_element(By.XPATH, xpath)
                if element.is_displayed() and element.is_enabled():
                    automation.driver.execute_script("arguments[0].value = arguments[1];", element, test_data['nome_cliente'])
                    automation.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", element)
                    logger.info(f"✅ Nome preenchido: {test_data['nome_cliente']}")
                    break
            except:
                continue
        
        # Aguardar um pouco para o select aparecer
        time.sleep(3)
        
        # Debug do select
        logger.info("=== DEBUG DO SELECT ===")
        
        try:
            # Tentar encontrar o select
            select_element = automation.driver.find_element(By.ID, "comboInscricao")
            logger.info("✅ Select encontrado por ID")
            
            # Verificar propriedades
            logger.info(f"Select visível: {select_element.is_displayed()}")
            logger.info(f"Select habilitado: {select_element.is_enabled()}")
            logger.info(f"Select disabled: {select_element.get_attribute('disabled')}")
            logger.info(f"Select style: {select_element.get_attribute('style')}")
            
            # Obter opções
            opcoes = select_element.find_elements(By.TAG_NAME, "option")
            logger.info(f"📋 Número de opções: {len(opcoes)}")
            
            for i, opcao in enumerate(opcoes):
                valor = opcao.get_attribute('value')
                texto = opcao.text
                logger.info(f"  Opção {i}: valor='{valor}', texto='{texto}'")
            
            # Tentar clicar no select
            logger.info("🔄 Tentando clicar no select...")
            automation.driver.execute_script("arguments[0].click();", select_element)
            time.sleep(2)
            
            # Verificar se apareceram mais opções
            opcoes_apos_click = select_element.find_elements(By.TAG_NAME, "option")
            logger.info(f"📋 Opções após clicar: {len(opcoes_apos_click)}")
            
            # Aguardar mais um pouco
            logger.info("🔄 Aguardando 5 segundos...")
            time.sleep(5)
            
            opcoes_final = select_element.find_elements(By.TAG_NAME, "option")
            logger.info(f"📋 Opções após aguardar: {len(opcoes_final)}")
            
            for i, opcao in enumerate(opcoes_final):
                valor = opcao.get_attribute('value')
                texto = opcao.text
                logger.info(f"  Opção {i}: valor='{valor}', texto='{texto}'")
            
        except Exception as e:
            logger.error(f"❌ Erro ao debug do select: {e}")
        
        logger.info("✅ Debug concluído! Verifique os logs acima.")
        logger.info("🚀 Navegador mantido aberto para inspeção")
        
        # Manter o navegador aberto para inspeção
        input("Pressione ENTER para fechar o navegador...")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro durante o debug: {e}")
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
    success = debug_select_inscricao()
    sys.exit(0 if success else 1) 