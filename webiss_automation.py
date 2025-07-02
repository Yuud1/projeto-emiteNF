#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automação WebISS - Login e preenchimento de campos
"""

import time
import logging
from typing import Dict, List, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime

logger = logging.getLogger(__name__)

class WebISSAutomation:
    """Classe para automação do WebISS"""
    
    def __init__(self, settings):
        self.settings = settings
        self.driver = None
        self.wait = None
        self.is_logged_in = False
        
    def setup_driver(self):
        """Configura o driver do Chrome"""
        try:
            logger.info(f"Configurando driver com URL: {self.settings.webiss_url}")
            
            chrome_options = Options()
            
            # Configurações para melhor performance e compatibilidade Windows
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            
            # Configurações específicas para Windows
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-software-rasterizer")
            
            # Descomente a linha abaixo para executar em modo headless
            if self.settings.headless_mode:
                chrome_options.add_argument("--headless")
            
            # Instala e configura o ChromeDriver com tratamento de erro
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as driver_error:
                logger.warning(f"Erro com ChromeDriverManager: {driver_error}")
                # Fallback: tenta usar ChromeDriver local
                try:
                    self.driver = webdriver.Chrome(options=chrome_options)
                except Exception as fallback_error:
                    logger.error(f"Erro no fallback: {fallback_error}")
                    return False
            
            self.wait = WebDriverWait(self.driver, self.settings.timeout)
            
            logger.info("Driver do Chrome configurado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao configurar driver: {e}")
            return False
    
    def login(self) -> bool:
        """
        Realiza login no WebISS (versão otimizada)
        
        Returns:
            bool: True se login realizado com sucesso
        """
        try:
            if not self.driver:
                if not self.setup_driver():
                    return False
            
            # Verifica se já está logado
            if self.is_logged_in:
                logger.info("Usuário já está logado")
                return True
            
            # Valida URL
            if not self.settings.webiss_url or self.settings.webiss_url.startswith('data:'):
                logger.error(f"URL inválida: {self.settings.webiss_url}")
                return False
            
            # Navega para a página de login
            logger.info(f"Navegando para: {self.settings.webiss_url}")
            self.driver.get(self.settings.webiss_url)
            
            # Aguarda carregamento da página (reduzido)
            time.sleep(0.5)
            
            # Log da URL atual para debug
            logger.info(f"URL atual: {self.driver.current_url}")
            logger.info(f"Título da página: {self.driver.title}")
            
            # Tenta diferentes seletores para campo de usuário (otimizado)
            username_selectors = [
                (By.XPATH, "//input[@type='text']"),  # Mais comum primeiro
                (By.NAME, "username"),
                (By.ID, "username"),
                (By.NAME, "user"),
                (By.ID, "user"),
                (By.NAME, "login"),
                (By.ID, "login"),
                (By.XPATH, "//input[@placeholder*='usuário' or @placeholder*='login' or @placeholder*='email']")
            ]
            
            username_field = None
            for selector_type, selector_value in username_selectors:
                try:
                    username_field = self.wait.until(
                        EC.presence_of_element_located((selector_type, selector_value))
                    )
                    logger.info(f"Campo de usuário encontrado: {selector_type}={selector_value}")
                    break
                except TimeoutException:
                    continue
            
            if not username_field:
                logger.error("Campo de usuário não encontrado")
                self.take_screenshot("login_page_debug.png")
                return False
            
            # Preenche campo de usuário via JavaScript (mais rápido)
            self.driver.execute_script("arguments[0].value = arguments[1];", username_field, self.settings.username)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", username_field)
            logger.info("Usuário preenchido via JavaScript")
            
            # Tenta diferentes seletores para campo de senha (otimizado)
            password_selectors = [
                (By.XPATH, "//input[@type='password']"),  # Mais comum primeiro
                (By.NAME, "password"),
                (By.ID, "password"),
                (By.NAME, "senha"),
                (By.ID, "senha")
            ]
            
            password_field = None
            for selector_type, selector_value in password_selectors:
                try:
                    password_field = self.driver.find_element(selector_type, selector_value)
                    logger.info(f"Campo de senha encontrado: {selector_type}={selector_value}")
                    break
                except NoSuchElementException:
                    continue
            
            if not password_field:
                logger.error("Campo de senha não encontrado")
                return False
            
            # Preenche campo de senha via JavaScript (mais rápido)
            self.driver.execute_script("arguments[0].value = arguments[1];", password_field, self.settings.password)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", password_field)
            logger.info("Senha preenchida via JavaScript")
            
            # Tenta diferentes seletores para botão de login (otimizado)
            login_button_selectors = [
                (By.XPATH, "//button[@type='submit']"),  # Mais comum primeiro
                (By.XPATH, "//input[@type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Login')]"),
                (By.XPATH, "//button[contains(text(), 'Entrar')]"),
                (By.XPATH, "//input[@value='Login']"),
                (By.XPATH, "//input[@value='Entrar']"),
                (By.ID, "login-button"),
                (By.NAME, "login-button")
            ]
            
            login_button = None
            for selector_type, selector_value in login_button_selectors:
                try:
                    login_button = self.driver.find_element(selector_type, selector_value)
                    logger.info(f"Botão de login encontrado: {selector_type}={selector_value}")
                    break
                except NoSuchElementException:
                    continue
            
            if not login_button:
                logger.error("Botão de login não encontrado")
                return False
            
            # Clica no botão de login via JavaScript (mais rápido)
            self.driver.execute_script("arguments[0].click();", login_button)
            logger.info("Botão de login clicado via JavaScript")
            
            # Aguarda redirecionamento após login (reduzido)
            time.sleep(0.5)
            
            # Log da URL após login para debug
            logger.info(f"URL após login: {self.driver.current_url}")
            logger.info(f"Título após login: {self.driver.title}")
            
            # Verifica se login foi bem-sucedido
            success_indicators = [
                "dashboard" in self.driver.current_url.lower(),
                "home" in self.driver.current_url.lower(),
                "main" in self.driver.current_url.lower(),
                "welcome" in self.driver.current_url.lower(),
                "painel" in self.driver.current_url.lower(),
                "menu" in self.driver.current_url.lower(),
                "inicio" in self.driver.current_url.lower()
            ]
            
            if any(success_indicators):
                self.is_logged_in = True
                logger.info("Login realizado com sucesso")
                return True
            else:
                # Verifica se há mensagem de erro
                error_messages = [
                    "//div[contains(text(), 'erro')]",
                    "//div[contains(text(), 'inválido')]",
                    "//div[contains(text(), 'incorreto')]",
                    "//span[contains(text(), 'erro')]",
                    "//p[contains(text(), 'erro')]"
                ]
                
                for error_xpath in error_messages:
                    try:
                        error_element = self.driver.find_element(By.XPATH, error_xpath)
                        logger.error(f"Erro de login: {error_element.text}")
                    except NoSuchElementException:
                        continue
                
                logger.error("Falha no login - URL não corresponde ao esperado")
                return False
                
        except TimeoutException:
            logger.error("Timeout ao tentar fazer login")
            return False
        except Exception as e:
            logger.error(f"Erro durante login: {e}")
            return False
    
    def navigate_to_nfse(self) -> bool:
        """
        Navega para a seção de emissão de NFSe
        
        Returns:
            bool: True se navegação bem-sucedida
        """
        try:
            if not self.is_logged_in:
                logger.error("Usuário não está logado")
                return False
            
            # Procura por link ou menu de NFSe
            nfse_links = [
                "//a[contains(text(), 'NFSe')]",
                "//a[contains(text(), 'Nota Fiscal')]",
                "//a[contains(text(), 'Emitir')]",
                "//li[contains(@class, 'nfse')]//a"
            ]
            
            for xpath in nfse_links:
                try:
                    nfse_link = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    nfse_link.click()
                    time.sleep(1)
                    logger.info("Navegação para NFSe realizada")
                    return True
                except TimeoutException:
                    continue
            
            logger.error("Não foi possível encontrar link para NFSe")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao navegar para NFSe: {e}")
            return False
    
    def fill_nfse_form(self, data: Dict[str, Any]) -> bool:
        """
        Preenche formulário de NFSe com os dados fornecidos (WebISS Palmas)
        """
        try:
            logger.info("=== PREENCHENDO FORMULÁRIO TOMADOR ===")
            logger.info(f"Dados recebidos: {data}")
            
            # Função auxiliar para encontrar e preencher campo
            def find_and_fill_field(field_name, xpath_list, value):
                """Encontra e preenche um campo usando múltiplos XPaths"""
                if not value:
                    logger.warning(f"Valor vazio para {field_name}")
                    return False
                
                for xpath in xpath_list:
                    try:
                        element = self.driver.find_element(By.XPATH, xpath)
                        if element.is_displayed() and element.is_enabled():
                            # Removido scrollIntoView para evitar bug na tela
                            time.sleep(0.1)  # OTIMIZADO: reduzido de 0.25 para 0.1
                            element.clear()
                            element.send_keys(str(value))
                            logger.info(f"✅ Campo {field_name} preenchido: {value} (usando: {xpath})")
                            return True
                    except Exception as e:
                        logger.debug(f"Falha no XPath {xpath} para {field_name}: {e}")
                        continue
                
                logger.warning(f"❌ Campo {field_name} não encontrado em nenhum XPath")
                return False

            # 1. Preencher CPF/CNPJ
            cpf_xpaths = [
                "//input[@placeholder='Número do documento do tomador']",
                "//input[@name='cpf_cnpj']",
                "//input[@id='cpf_cnpj']",
                "//input[contains(@placeholder, 'CPF')]",
                "//input[contains(@placeholder, 'CNPJ')]",
                "//input[contains(@placeholder, 'documento')]"
            ]
            find_and_fill_field('cpf_cnpj', cpf_xpaths, data.get('cpf_cnpj', ''))

            # 2. Preencher Nome/Razão Social
            nome_xpaths = [
                "//input[@placeholder='Razão social do tomador']",
                "//input[@name='nome']",
                "//input[@id='nome']",
                "//input[contains(@placeholder, 'nome')]",
                "//input[contains(@placeholder, 'razão')]",
                "//input[contains(@placeholder, 'social')]"
            ]
            find_and_fill_field('nome_cliente', nome_xpaths, data.get('nome_cliente', ''))

            # 3. Preencher CEP
            cep_xpaths = [
                "//input[@name='cep']",
                "//input[@id='cep']",
                "//input[contains(@placeholder, 'CEP')]",
                "//input[contains(@placeholder, 'cep')]"
            ]
            cep_value = data.get('cep', '')
            if not cep_value and 'endereco' in data:
                # Tentar extrair CEP do endereço
                import re
                cep_match = re.search(r'(\d{5})-?(\d{3})', data['endereco'])
                if cep_match:
                    cep_value = f"{cep_match.group(1)}-{cep_match.group(2)}"
                    logger.info(f"CEP extraído do endereço: {cep_value}")
            
            find_and_fill_field('cep', cep_xpaths, cep_value)

            # 4. Aguardar preenchimento automático do endereço (Município/UF) - REMOVIDO para otimização
            # logger.info("Aguardando preenchimento automático do município...")
            # try:
            #     municipio_xpaths = [
            #         "//input[@name='municipio']",
            #         "//input[contains(@placeholder, 'Município')]",
            #         "//input[contains(@placeholder, 'municipio')]"
            #     ]
            #     
            #     municipio_field = None
            #     for xpath in municipio_xpaths:
            #         try:
            #             municipio_field = self.wait.until(
            #                 EC.presence_of_element_located((By.XPATH, xpath))
            #             )
            #             break
            #         except TimeoutException:
            #             continue
            #     
            #     if municipio_field:
            #         for i in range(3):  # 1.5 segundos (3 x 0.5s) - OTIMIZADO
            #             if municipio_field.get_attribute('value'):
            #                 logger.info(f"✅ Município preenchido automaticamente: {municipio_field.get_attribute('value')}")
            #                 break
            #             time.sleep(0.5)
            #     else:
            #         logger.warning("⚠️ Município não preenchido automaticamente após 1.5s")
            # except Exception as e:
            #     logger.warning(f"⚠️ Erro ao aguardar município: {e}")

            logger.info("ℹ️ Pulando aguardo do município para otimização")

            # 5. Preencher campos adicionais se disponíveis
            campos_adicionais = {
                'numero': [
                    "//input[@name='numero']",
                    "//input[@id='numero']",
                    "//input[contains(@placeholder, 'número')]",
                    "//input[contains(@placeholder, 'numero')]"
                ],
                'complemento': [
                    "//input[@name='complemento']",
                    "//input[@id='complemento']",
                    "//input[contains(@placeholder, 'complemento')]"
                ],
                'bairro': [
                    "input[@name='bairro']",
                    "//input[@id='bairro']",
                    "//input[contains(@placeholder, 'bairro')]"
                ],
                'telefone': [
                    "//input[@name='telefone']",
                    "//input[@id='telefone']",
                    "//input[contains(@placeholder, 'telefone')]",
                    "//input[contains(@placeholder, 'fone')]"
                ],
                'email': [
                    "//input[@placeholder='Email principal de contato do tomador']",
                    "//input[@name='email']",
                    "//input[@id='email']",
                    "//input[contains(@placeholder, 'email')]"
                ]
            }
            
            for campo, xpaths in campos_adicionais.items():
                valor = data.get(campo, '')
                if valor:
                    find_and_fill_field(campo, xpaths, valor)

            # 6. Salvar screenshot para debug (REMOVIDO para otimização)
            # try:
            #     self.take_screenshot("step2_tomador_preenchido.png")
            #     logger.info("Screenshot da Step 2 salvo: step2_tomador_preenchido.png")
            # except Exception as e:
            #     logger.warning(f"Erro ao salvar screenshot: {e}")

            logger.info("✅ Formulário do tomador preenchido com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao preencher formulário: {e}")
            self.take_screenshot("step2_error.png")
            return False
    
    def generate_preview(self) -> bool:
        """
        Gera prévia da nota fiscal
        
        Returns:
            bool: True se prévia gerada com sucesso
        """
        try:
            # Procura por botão de prévia
            preview_buttons = [
                '//button[contains(text(), "Prévia")]',
                '//button[contains(text(), "Preview")]',
                '//input[@value="Prévia"]',
                '//button[@id="preview"]'
            ]
            
            for xpath in preview_buttons:
                try:
                    preview_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    preview_button.click()
                    time.sleep(1)
                    logger.info("Prévia gerada com sucesso")
                    return True
                except TimeoutException:
                    continue
            
            logger.error("Botão de prévia não encontrado")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao gerar prévia: {e}")
            return False
    
    def process_multiple_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processa múltiplos registros
        """
        results = {
            'success': 0,
            'errors': [],
            'total': len(records)
        }
        for i, record in enumerate(records):
            try:
                logger.info(f"Processando registro {i+1}/{len(records)}")
                # Navega para formulário de nova NFSe
                if not self.navigate_to_new_nfse():
                    results['errors'].append(f"Registro {i+1}: Erro ao navegar para formulário")
                    continue
                # Passo 2: Tomador
                if not self.fill_nfse_form(record):
                    results['errors'].append(f"Registro {i+1}: Erro ao preencher Tomador")
                    continue
                # Avança para Serviços
                if not self.click_proximo():
                    results['errors'].append(f"Registro {i+1}: Erro ao avançar para Serviços")
                    continue
                # Passo 3: Serviços
                if not self.fill_nfse_servicos(record):
                    results['errors'].append(f"Registro {i+1}: Erro ao preencher Serviços")
                    continue
                # Avança para Valores
                if not self.click_proximo():
                    results['errors'].append(f"Registro {i+1}: Erro ao avançar para Valores")
                    continue
                # Passo 4: Valores
                if not self.fill_nfse_valores(record):
                    results['errors'].append(f"Registro {i+1}: Erro ao preencher Valores")
                    continue
                # Salvar rascunho
                if not self.salvar_rascunho():
                    results['errors'].append(f"Registro {i+1}: Erro ao salvar rascunho")
                    continue
                results['success'] += 1
                logger.info(f"Registro {i+1} processado com sucesso")
                time.sleep(1)
            except Exception as e:
                error_msg = f"Registro {i+1}: Erro inesperado - {e}"
                results['errors'].append(error_msg)
                logger.error(error_msg)
        return results

    def click_proximo(self) -> bool:
        """Clica no botão Próximo na etapa atual"""
        try:
            logger.info("=== TENTANDO CLICAR EM PRÓXIMO ===")
            
            # Aguardar um pouco antes de procurar o botão (OTIMIZADO)
            time.sleep(0.5)
            
            # Lista de XPaths para o botão Próximo
            proximo_btn_xpaths = [
                "//a[@id='btnProximo']",
                "//button[@id='btnProximo']",
                "//a[contains(@class, 'btn') and contains(text(), 'Próximo')]",
                "//button[contains(@class, 'btn') and contains(text(), 'Próximo')]",
                "//a[contains(text(), 'Próximo')]",
                "//button[contains(text(), 'Próximo')]",
                "//input[@value='Próximo']",
                "//input[@value='Próximo']",
                "//*[contains(@class, 'btn') and contains(., 'Próximo')]",
                "//*[contains(@class, 'btn') and contains(., 'PROXIMO')]",
                "//*[contains(@class, 'btn') and contains(., 'proximo')]",
                "//a[contains(@onclick, 'proximo')]",
                "//button[contains(@onclick, 'proximo')]",
                "//a[contains(@onclick, 'Proximo')]",
                "//button[contains(@onclick, 'Proximo')]"
            ]
            
            # Tentar encontrar e clicar no botão
            proximo_btn = None
            xpath_usado = None
            
            for xpath in proximo_btn_xpaths:
                try:
                    logger.info(f"Tentando XPath: {xpath}")
                    proximo_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    xpath_usado = xpath
                    logger.info(f"✅ Botão Próximo encontrado: {xpath}")
                    break
                except TimeoutException:
                    logger.debug(f"XPath não encontrado: {xpath}")
                    continue
                except Exception as e:
                    logger.debug(f"Erro no XPath {xpath}: {e}")
                    continue
            
            if not proximo_btn:
                logger.error("❌ Botão Próximo não encontrado em nenhum seletor")
                
                # Tentar encontrar qualquer botão na página
                try:
                    todos_botoes = self.driver.find_elements(By.XPATH, "//button | //a[contains(@class, 'btn')] | //input[@type='submit']")
                    logger.info(f"Encontrados {len(todos_botoes)} botões na página:")
                    for i, btn in enumerate(todos_botoes[:10]):  # Mostrar apenas os primeiros 10
                        try:
                            texto = btn.text.strip()
                            classe = btn.get_attribute('class') or ''
                            id_btn = btn.get_attribute('id') or ''
                            logger.info(f"  Botão {i+1}: texto='{texto}', class='{classe}', id='{id_btn}'")
                        except Exception as e:
                            logger.info(f"  Botão {i+1}: erro ao obter informações - {e}")
                except Exception as e:
                    logger.warning(f"Erro ao listar botões: {e}")
                
                self.take_screenshot("proximo_btn_not_found.png")
                return False
            
            # Scroll para o botão
            try:
                # Removido scrollIntoView para evitar que o conteúdo seja empurrado para cima
                # O botão Próximo geralmente já está visível na parte inferior da tela
                time.sleep(1)
                logger.info("Aguardando botão Próximo (sem scroll)")
            except Exception as e:
                logger.warning(f"Erro no aguardo: {e}")
            
            # Verificar se o botão está visível e habilitado
            try:
                if not proximo_btn.is_displayed():
                    logger.warning("⚠️ Botão Próximo não está visível")
                if not proximo_btn.is_enabled():
                    logger.warning("⚠️ Botão Próximo não está habilitado")
            except Exception as e:
                logger.warning(f"Erro ao verificar estado do botão: {e}")
            
            # Tentar clicar no botão
            try:
                logger.info("Clicando no botão Próximo via JavaScript...")
                # Usar JavaScript diretamente para evitar scroll automático
                self.driver.execute_script("arguments[0].click();", proximo_btn)
                logger.info("✅ Botão Próximo clicado via JavaScript!")
                
                # Aguardar um pouco para a página carregar
                time.sleep(1)
                
                # Verificar se apareceu modal de confirmação
                try:
                    modal_sim = self.driver.find_element(By.XPATH, "//a[@data-handler='1' and contains(@class, 'btn-primary') and text()='Sim']")
                    if modal_sim.is_displayed():
                        logger.info("✅ Modal de confirmação detectado, clicando em 'Sim'...")
                        self.driver.execute_script("arguments[0].click();", modal_sim)
                        time.sleep(1)
                        logger.info("✅ Modal confirmado com 'Sim'")
                except:
                    logger.info("ℹ️ Nenhum modal de confirmação detectado")
                
                # Verificar se houve mudança na URL ou título
                url_atual = self.driver.current_url
                titulo_atual = self.driver.title
                logger.info(f"URL após clique: {url_atual}")
                logger.info(f"Título após clique: {titulo_atual}")
                
                # Salvar screenshot após o clique
                try:
                    self.take_screenshot("apos_proximo_click.png")
                    logger.info("Screenshot após clique salvo: apos_proximo_click.png")
                except Exception as e:
                    logger.warning(f"Erro ao salvar screenshot: {e}")
                
                return True
            except Exception as e:
                logger.error(f"❌ Erro ao clicar no botão via JavaScript: {e}")
                # Fallback: tentar clique normal
                try:
                    logger.info("Tentando clique normal como fallback...")
                    proximo_btn.click()
                    time.sleep(1)
                    
                    # Verificar modal novamente
                    try:
                        modal_sim = self.driver.find_element(By.XPATH, "//a[@data-handler='1' and contains(@class, 'btn-primary') and text()='Sim']")
                        if modal_sim.is_displayed():
                            logger.info("✅ Modal de confirmação detectado no fallback, clicando em 'Sim'...")
                            modal_sim.click()
                            time.sleep(1)
                            logger.info("✅ Modal confirmado com 'Sim' (fallback)")
                    except:
                        logger.info("ℹ️ Nenhum modal de confirmação detectado no fallback")
                    
                    logger.info("✅ Clique normal realizado como fallback!")
                    return True
                except Exception as normal_error:
                    logger.error(f"❌ Erro no clique normal: {normal_error}")
                    self.take_screenshot("proximo_btn_error.png")
                    return False
        except Exception as e:
            logger.error(f"❌ Erro geral ao clicar em Próximo: {e}")
            self.take_screenshot("proximo_btn_error.png")
            return False

    def find_servicos_select2_by_index(self, index):
        """
        Busca o select2 correto dentro do formulário de serviços, ignorando o select2 do topo.
        O index começa em 1 para o primeiro select2 do formulário de serviços.
        """
        try:
            # Estratégia 1: Buscar por formulário que contém label "Descrição"
            try:
                servicos_form = self.driver.find_element(
                    By.XPATH, "//form[.//label[contains(text(), 'Descrição')]]"
                )
                select2s = servicos_form.find_elements(By.XPATH, ".//a[contains(@class, 'select2-choice')]")
                if len(select2s) >= index:
                    logger.info(f"✅ Select2 {index} encontrado via formulário com label 'Descrição'")
                    return select2s[index-1]
            except Exception as e:
                logger.debug(f"Estratégia 1 falhou: {e}")
            
            # Estratégia 2: Buscar por formulário que contém textarea
            try:
                servicos_form = self.driver.find_element(
                    By.XPATH, "//form[.//textarea]"
                )
                select2s = servicos_form.find_elements(By.XPATH, ".//a[contains(@class, 'select2-choice')]")
                if len(select2s) >= index:
                    logger.info(f"✅ Select2 {index} encontrado via formulário com textarea")
                    return select2s[index-1]
            except Exception as e:
                logger.debug(f"Estratégia 2 falhou: {e}")
            
            # Estratégia 3: Buscar todos os select2 visíveis e usar os primeiros (excluindo o do topo)
            try:
                all_select2s = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'select2-choice')]")
                visible_select2s = [s for s in all_select2s if s.is_displayed()]
                
                # Filtrar select2s que não são do topo (geralmente o primeiro é o select de empresa)
                if len(visible_select2s) > 1:
                    # Pular o primeiro (select de empresa) e pegar os próximos
                    form_select2s = visible_select2s[1:]
                    if len(form_select2s) >= index:
                        logger.info(f"✅ Select2 {index} encontrado via filtro de visibilidade (pulando select do topo)")
                        return form_select2s[index-1]
            except Exception as e:
                logger.debug(f"Estratégia 3 falhou: {e}")
            
            # Estratégia 4: Fallback - usar todos os select2 visíveis
            try:
                all_select2s = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'select2-choice')]")
                visible_select2s = [s for s in all_select2s if s.is_displayed()]
                
                if len(visible_select2s) >= index:
                    logger.info(f"✅ Select2 {index} encontrado via fallback (todos visíveis)")
                    return visible_select2s[index-1]
            except Exception as e:
                logger.debug(f"Estratégia 4 falhou: {e}")
            
            logger.warning(f"Não encontrou select2 de índice {index} no formulário de serviços")
            logger.info(f"Total de select2 encontrados: {len(self.driver.find_elements(By.XPATH, '//a[contains(@class, \'select2-choice\')]'))}")
            logger.info(f"Select2 visíveis: {len([s for s in self.driver.find_elements(By.XPATH, '//a[contains(@class, \'select2-choice\')]') if s.is_displayed()])}")
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar select2 do formulário de serviços: {e}")
            return None

    def click_servicos_select2_and_navigate(self, index, arrow_down_count=1):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.action_chains import ActionChains
        
        # Limpar overlays antes de tentar
        self.limpar_overlays()
        
        select_field = self.find_servicos_select2_by_index(index)
        if select_field:
            try:
                # Estratégia 1: Tentar clicar normalmente
                # Removido scrollIntoView para evitar bug na tela
                time.sleep(0.15)
                select_field.click()
                time.sleep(0.15)
                
                try:
                    # Espera até o input de busca do select2 visível aparecer
                    wait = WebDriverWait(self.driver, 5)
                    # Busca todos os inputs de busca do select2
                    all_inputs = self.driver.find_elements(By.XPATH, "//input[contains(@class, 'select2-input') or contains(@class, 'select2-search__field')]")
                    search_input = None
                    for inp in all_inputs:
                        if inp.is_displayed():
                            search_input = inp
                            break
                    if not search_input:
                        raise Exception('Nenhum input de busca do select2 visível encontrado!')
                    # Foca explicitamente no input
                    self.driver.execute_script("arguments[0].focus();", search_input)
                    search_input.click()
                    time.sleep(0.1)
                    for _ in range(arrow_down_count):
                        search_input.send_keys(Keys.ARROW_DOWN)
                        time.sleep(0.1)
                    search_input.send_keys(Keys.ENTER)
                    time.sleep(0.15)
                    logger.info(f"✅ Select2 do formulário (índice {index}) clicado e navegado {arrow_down_count} vezes (input de busca visível)")
                    return True
                except Exception as e:
                    logger.warning(f"❌ Não encontrou input de busca do select2 visível após abrir: {e}")
                    # Logar HTML do select2 aberto para debug
                    try:
                        select2_html = select_field.get_attribute('outerHTML')
                        with open(f'logs/select2_debug_{index}.html', 'w', encoding='utf-8') as f:
                            f.write(select2_html)
                        logger.info(f"HTML do select2 (índice {index}) salvo em logs/select2_debug_{index}.html")
                    except Exception as ex:
                        logger.warning(f"Falha ao salvar HTML do select2: {ex}")
                    self.take_screenshot(f"select2_input_not_found_{index}.png")
                    
                    # Estratégia 2: Usar JavaScript direto (sem movimento da tela)
                    try:
                        logger.info(f"[DEBUG] Tentando JavaScript direto para select2 {index}")
                        # Clique direto via JavaScript para evitar movimento da tela
                        self.driver.execute_script("arguments[0].click();", select_field)
                        time.sleep(1)
                        
                        # Tentar encontrar input de busca
                        search_input = self.driver.find_element(By.XPATH, "//input[contains(@class, 'select2-input') and @type='text']")
                        search_input.clear()
                        for _ in range(arrow_down_count):
                            search_input.send_keys(Keys.ARROW_DOWN)
                            time.sleep(0.1)
                        search_input.send_keys(Keys.ENTER)
                        logger.info(f"✅ Select2 {index} selecionado via JavaScript direto")
                        return True
                    except Exception as e2:
                        logger.warning(f"[DEBUG] Erro ao clicar no select2 {index}: {e2}")
                        
                        # Estratégia 3: Usar ActionChains
                        try:
                            logger.info(f"[DEBUG] Tentando ActionChains para select2 {index}")
                            actions = ActionChains(self.driver)
                            actions.move_to_element(select_field).click().perform()
                            time.sleep(1)
                            
                            # Tentar encontrar input de busca
                            search_input = self.driver.find_element(By.XPATH, "//input[contains(@class, 'select2-input') and @type='text']")
                            search_input.clear()
                            for _ in range(arrow_down_count):
                                search_input.send_keys(Keys.ARROW_DOWN)
                                time.sleep(0.1)
                            search_input.send_keys(Keys.ENTER)
                            logger.info(f"✅ Select2 {index} selecionado via ActionChains")
                            return True
                        except Exception as e3:
                            logger.warning(f"[DEBUG] ActionChains falhou: {e3}")
                            
                            # Estratégia 4: JavaScript direto
                            try:
                                logger.info(f"[DEBUG] Tentando JavaScript direto para select2 {index}")
                                # Tentar simular a seleção via JavaScript
                                self.driver.execute_script("""
                                    var select2s = document.querySelectorAll('a.select2-choice');
                                    if (arguments[0] < select2s.length) {
                                        var select2 = select2s[arguments[0]];
                                        select2.click();
                                    }
                                """, index - 1)
                                time.sleep(1)
                                
                                # Tentar navegar com setas
                                search_input = self.driver.find_element(By.XPATH, "//input[contains(@class, 'select2-input') and @type='text']")
                                for _ in range(arrow_down_count):
                                    search_input.send_keys(Keys.ARROW_DOWN)
                                    time.sleep(0.1)
                                search_input.send_keys(Keys.ENTER)
                                logger.info(f"✅ Select2 {index} selecionado via JavaScript")
                                return True
                            except Exception as e4:
                                logger.warning(f"[DEBUG] JavaScript direto falhou: {e4}")
                                return False
            except Exception as e:
                logger.warning(f"❌ Erro ao clicar no select2 {index}: {e}")
                return False
        else:
            logger.warning(f"❌ Não foi possível clicar no select2 do formulário (índice {index})")
            return False

    def selecionar_mes_competencia(self, mes_num):
        """Seleciona o mês de competência no select2 do mês com múltiplas estratégias e remoção de overlay."""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.action_chains import ActionChains
            from datetime import datetime
            
            # Detectar mês atual automaticamente
            mes_atual = datetime.now().month
            logger.info(f"[DEBUG] Mês atual detectado: {mes_atual}")
            logger.info(f"[DEBUG] Mês solicitado: {mes_num}")
            
            # Se o mês solicitado for igual ao atual, usar o atual (evita modal)
            if mes_num == mes_atual:
                logger.info(f"[DEBUG] Usando mês atual ({mes_atual}) para evitar modal de confirmação")
                mes_para_usar = mes_atual
            else:
                logger.info(f"[DEBUG] Usando mês solicitado ({mes_num}) - pode aparecer modal")
                mes_para_usar = mes_num
            
            meses = [
                "Selecione", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]
            nome_mes = meses[mes_para_usar]
            logger.info(f"[DEBUG] Tentando selecionar mês: {nome_mes} (num: {mes_para_usar})")
            
            # Estratégia 1: Tentar remover overlay e clicar normalmente
            try:
                container = self.driver.find_element(By.ID, "s2id_MesDaCompetencia")
                select2_choice = container.find_element(By.CLASS_NAME, "select2-choice")
                # Removido scrollIntoView para evitar bug na tela
                
                # Tentar remover overlay se existir
                try:
                    overlay = self.driver.find_element(By.ID, "select2-drop-mask")
                    if overlay.is_displayed():
                        logger.info("[DEBUG] Removendo overlay select2-drop-mask")
                        self.driver.execute_script("arguments[0].remove();", overlay)
                except:
                    pass
                
                # Clicar no select2
                select2_choice.click()
                wait = WebDriverWait(self.driver, 10)
                
                # Aguardar lista aparecer
                ul = wait.until(lambda d: d.find_element(By.XPATH, "//ul[contains(@class, 'select2-results') and not(contains(@style, 'display: none'))]"))
                logger.info(f"[DEBUG] ul select2-results encontrado: {ul.get_attribute('outerHTML')[:300]}...")
                
                # Aguardar opções carregarem (máximo 10 segundos)
                max_wait = 10
                start_time = time.time()
                while time.time() - start_time < max_wait:
                    try:
                        # Tentar encontrar o item do mês
                        li_mes = ul.find_element(By.XPATH, f".//div[@class='select2-result-label' and normalize-space(text())='{nome_mes}']")
                        if li_mes.is_displayed():
                            logger.info(f"[DEBUG] li do mês encontrado: {li_mes.get_attribute('outerHTML')}")
                            break
                    except:
                        # Se não encontrou, aguardar um pouco e tentar novamente
                        time.sleep(0.5)
                        logger.info("[DEBUG] Aguardando opções carregarem...")
                        continue
                else:
                    # Se chegou aqui, não encontrou o item
                    logger.warning(f"[DEBUG] Não encontrou o li do mês após {max_wait}s")
                    with open('logs/select2_ul_debug.html', 'w', encoding='utf-8') as f:
                        f.write(ul.get_attribute('outerHTML'))
                    logger.info("[DEBUG] HTML do ul salvo em logs/select2_ul_debug.html")
                    raise Exception("Item do mês não encontrado na lista")
                
                # Aguardar item ficar visível
                wait.until(lambda d: li_mes.is_displayed())
                
                # Tentar clicar com JavaScript
                try:
                    self.driver.execute_script("arguments[0].click();", li_mes)
                    logger.info(f"[DEBUG] Clique no mês realizado com JavaScript")
                except Exception as e:
                    logger.warning(f"[DEBUG] Erro ao clicar com JavaScript: {e}")
                    # Tentar clicar normal
                    li_mes.click()
                    logger.info(f"[DEBUG] Clique no mês realizado normalmente")
                
                # Aguardar overlay sumir
                try:
                    wait.until(lambda d: not d.find_element(By.ID, "select2-drop-mask").is_displayed())
                    logger.info(f"[DEBUG] Overlay select2-drop-mask sumiu após clique")
                except:
                    logger.warning(f"[DEBUG] Overlay não sumiu, tentando remover")
                    try:
                        overlay = self.driver.find_element(By.ID, "select2-drop-mask")
                        self.driver.execute_script("arguments[0].remove();", overlay)
                    except:
                        pass
                
                logger.info(f"✅ Mês de competência selecionado clicando no item: {nome_mes}")
                return True
                
            except Exception as e:
                logger.warning(f"[DEBUG] Estratégia 1 falhou: {e}")
                
                # Salvar HTML para debug
                try:
                    with open('logs/select2_ul_debug.html', 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                    logger.info("[DEBUG] HTML da página salvo em logs/select2_ul_debug.html")
                except:
                    pass
                
                # Estratégia 2: Usar JavaScript para setar valor diretamente
                try:
                    logger.info("[DEBUG] Tentando estratégia 2: JavaScript direto")
                    select_element = self.driver.find_element(By.ID, "MesDaCompetencia")
                    self.driver.execute_script(f"arguments[0].value = '{mes_para_usar}';", select_element)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", select_element)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", select_element)
                    
                    # Forçar fechamento do select2 após setar valor
                    time.sleep(0.5)
                    self.driver.execute_script("""
                        // Forçar fechamento do select2
                        var select2Container = document.getElementById('s2id_MesDaCompetencia');
                        if (select2Container) {
                            var select2Choice = select2Container.querySelector('.select2-choice');
                            if (select2Choice) {
                                select2Choice.click(); // Fechar se estiver aberto
                            }
                        }
                        
                        // Remover overlay se existir
                        var overlay = document.getElementById('select2-drop-mask');
                        if (overlay) {
                            overlay.remove();
                        }
                        
                        // Remover dropdown se existir
                        var dropdowns = document.querySelectorAll('.select2-drop');
                        dropdowns.forEach(function(dropdown) {
                            if (dropdown.style.display !== 'none') {
                                dropdown.style.display = 'none';
                            }
                        });
                    """)
                    
                    logger.info(f"✅ Mês de competência selecionado via JavaScript: {nome_mes}")
                    return True
                except Exception as e2:
                    logger.warning(f"[DEBUG] Estratégia 2 falhou: {e2}")
                    
                    # Estratégia 3: Usar JavaScript direto (sem movimento da tela)
                    try:
                        logger.info("[DEBUG] Tentando estratégia 3: JavaScript direto")
                        container = self.driver.find_element(By.ID, "s2id_MesDaCompetencia")
                        select2_choice = container.find_element(By.CLASS_NAME, "select2-choice")
                        
                        # Clique direto via JavaScript para evitar movimento da tela
                        self.driver.execute_script("arguments[0].click();", select2_choice)
                        time.sleep(1)
                        
                        # Tentar digitar o nome do mês
                        search_input = self.driver.find_element(By.XPATH, "//input[contains(@class, 'select2-input') and @type='text']")
                        search_input.clear()
                        search_input.send_keys(nome_mes)
                        time.sleep(0.5)
                        search_input.send_keys(Keys.ENTER)
                        
                        logger.info(f"✅ Mês de competência selecionado via JavaScript direto: {nome_mes}")
                        return True
                    except Exception as e3:
                        logger.warning(f"[DEBUG] Erro ao clicar no select2 {index}: {e3}")
                        
                        # Estratégia 4: Forçar carregamento via JavaScript
                        try:
                            logger.info("[DEBUG] Tentando estratégia 4: Forçar carregamento")
                            # Forçar o select2 a abrir e carregar opções
                            self.driver.execute_script("""
                                var container = document.getElementById('s2id_MesDaCompetencia');
                                var select = document.getElementById('MesDaCompetencia');
                                if (select) {
                                    select.value = arguments[0];
                                    select.dispatchEvent(new Event('change'));
                                    select.dispatchEvent(new Event('input'));
                                }
                            """, mes_para_usar)
                            logger.info(f"✅ Mês de competência selecionado via JavaScript forçado: {nome_mes}")
                            return True
                        except Exception as e4:
                            logger.warning(f"[DEBUG] Estratégia 4 falhou: {e4}")
                            raise e  # Re-raise o erro original
        except Exception as e:
            logger.warning(f"❌ Erro ao selecionar mês de competência clicando no item: {e}")
            self.take_screenshot("erro_mes_competencia.png")
            return False

    def limpar_overlays(self):
        """Remove overlays que podem estar bloqueando interações."""
        try:
            # Remover select2-drop-mask se existir
            overlays = self.driver.find_elements(By.ID, "select2-drop-mask")
            for overlay in overlays:
                if overlay.is_displayed():
                    logger.info("[DEBUG] Removendo overlay select2-drop-mask")
                    self.driver.execute_script("arguments[0].remove();", overlay)
            
            # Remover outros overlays comuns
            overlay_selectors = [
                "//div[contains(@class, 'select2-drop-mask')]",
                "//div[contains(@class, 'modal-backdrop')]",
                "//div[contains(@class, 'overlay')]"
            ]
            
            for selector in overlay_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if element.is_displayed():
                            logger.info(f"[DEBUG] Removendo overlay: {selector}")
                            self.driver.execute_script("arguments[0].remove();", element)
                except:
                    pass
            
            # Fechar dropdowns do select2 que possam estar abertos
            try:
                self.driver.execute_script("""
                    // Fechar todos os dropdowns do select2
                    var dropdowns = document.querySelectorAll('.select2-drop');
                    dropdowns.forEach(function(dropdown) {
                        if (dropdown.style.display !== 'none') {
                            dropdown.style.display = 'none';
                        }
                    });
                    
                    // Remover overlays restantes
                    var overlays = document.querySelectorAll('.select2-drop-mask');
                    overlays.forEach(function(overlay) {
                        overlay.remove();
                    });
                    
                    // Forçar blur em inputs do select2
                    var inputs = document.querySelectorAll('.select2-input');
                    inputs.forEach(function(input) {
                        input.blur();
                    });
                """)
                logger.info("[DEBUG] Dropdowns do select2 fechados via JavaScript")
            except Exception as e:
                logger.warning(f"[DEBUG] Erro ao fechar dropdowns: {e}")
                    
            logger.info("[DEBUG] Limpeza de overlays concluída")
            return True
        except Exception as e:
            logger.warning(f"[DEBUG] Erro ao limpar overlays: {e}")
            return False

    def fill_nfse_servicos_sem_scroll(self, data: Dict[str, Any]) -> bool:
        """Preenche a etapa de Serviços usando apenas JavaScript para evitar scroll"""
        try:
            logger.info("=== PREENCHENDO STEP 3 - SERVIÇOS (SEM SCROLL) ===")
            logger.info(f"Dados recebidos: {data}")

            # 1. PREENCHER ANO via JavaScript
            try:
                if 'vencimento' in data and '/' in data['vencimento']:
                    ano = data['vencimento'].split('/')[2]
                    self.driver.execute_script("""
                        var inputs = document.querySelectorAll('input[placeholder*="ano"], input[placeholder*="Ano"], input[id*="ano"], input[name*="ano"]');
                        for (var i = 0; i < inputs.length; i++) {
                            if (inputs[i].style.display !== 'none' && inputs[i].disabled === false) {
                                inputs[i].value = arguments[0];
                                inputs[i].dispatchEvent(new Event('input'));
                                inputs[i].dispatchEvent(new Event('change'));
                                break;
                            }
                        }
                    """, ano)
                    logger.info(f"✅ Ano preenchido via JavaScript: {ano}")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao preencher ano: {e}")

            # 2. SELECIONAR MÊS via JavaScript
            try:
                if 'vencimento' in data and '/' in data['vencimento']:
                    mes_num = int(data['vencimento'].split('/')[1])
                    self.driver.execute_script("""
                        var select = document.getElementById('MesDaCompetencia');
                        if (select) {
                            select.value = arguments[0];
                            select.dispatchEvent(new Event('change'));
                            select.dispatchEvent(new Event('input'));
                        }
                    """, mes_num)
                    logger.info(f"✅ Mês selecionado via JavaScript: {mes_num}")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao selecionar mês: {e}")

            # 3. SELECIONAR TIPO DE ATIVIDADE via JavaScript
            try:
                self.driver.execute_script("""
                    var select = document.getElementById('lista-de-servicos-prestador');
                    if (select && select.options.length > 1) {
                        select.value = select.options[1].value;
                        select.dispatchEvent(new Event('change'));
                        select.dispatchEvent(new Event('input'));
                    }
                """)
                logger.info("✅ Tipo de atividade selecionado via JavaScript")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao selecionar tipo de atividade: {e}")

            # 4. SELECIONAR CNAE via JavaScript
            try:
                arrow_down_count = 1
                if 'turma' in data and data['turma']:
                    turma = data['turma'].upper()
                    if any(keyword in turma for keyword in ['G', 'MÉDIO', 'MEDIO']):
                        arrow_down_count = 2
                
                self.driver.execute_script("""
                    var select = document.getElementById('CnaeAtividade_Id');
                    if (select && select.options.length > arguments[0]) {
                        select.value = select.options[arguments[0]].value;
                        select.dispatchEvent(new Event('change'));
                        select.dispatchEvent(new Event('input'));
                    }
                """, arrow_down_count)
                logger.info(f"✅ CNAE selecionado via JavaScript (índice {arrow_down_count})")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao selecionar CNAE: {e}")

            # 5. PREENCHER VALOR DO SERVIÇO via JavaScript
            try:
                valor = str(data.get('valor', ''))
                if valor:
                    self.driver.execute_script("""
                        var inputs = document.querySelectorAll('input[name="valorServico"], input[placeholder*="Valor do serviço"]');
                        for (var i = 0; i < inputs.length; i++) {
                            if (inputs[i].style.display !== 'none' && inputs[i].disabled === false) {
                                inputs[i].value = arguments[0];
                                inputs[i].dispatchEvent(new Event('input'));
                                inputs[i].dispatchEvent(new Event('change'));
                                break;
                            }
                        }
                    """, valor)
                    logger.info(f"✅ Valor do serviço preenchido via JavaScript: {valor}")
                    time.sleep(1)
                else:
                    logger.warning("⚠️ Valor do serviço não informado nos dados")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao preencher valor do serviço: {e}")

            # 6. PREENCHER DESCRIÇÃO via JavaScript
            try:
                self.driver.execute_script("""
                    var textareas = document.querySelectorAll('textarea[id="discriminacao"], textarea[name="Discriminacao"], textarea[placeholder*="descrição"], textarea[placeholder*="Descrição"]');
                    for (var i = 0; i < textareas.length; i++) {
                        if (textareas[i].style.display !== 'none' && textareas[i].disabled === false) {
                            textareas[i].value = 'prestação de serviços educacionais';
                            textareas[i].dispatchEvent(new Event('input'));
                            textareas[i].dispatchEvent(new Event('change'));
                            break;
                        }
                    }
                """)
                logger.info("✅ Descrição preenchida via JavaScript")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao preencher descrição: {e}")

            # Screenshot final
            self.take_screenshot("step3_sem_scroll.png")
            logger.info("Screenshot final da Step 3 (sem scroll) salvo: step3_sem_scroll.png")
            logger.info("✅ [SERVIÇOS] Etapa de serviços preenchida com sucesso (sem scroll)!")
            return True

        except Exception as e:
            logger.error(f"❌ Erro geral ao preencher serviços (sem scroll): {e}")
            self.take_screenshot("erro_step3_sem_scroll.png")
            return False

    def fill_nfse_servicos(self, data: Dict[str, Any]) -> bool:
        """Preenche a etapa de Serviços com abordagem corrigida para WebISS Palmas-TO"""
        try:
            import time
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            wait = WebDriverWait(self.driver, 10)

            logger.info("=== PREENCHENDO STEP 3 - SERVIÇOS (VERSÃO CORRIGIDA) ===")
            logger.info(f"Dados recebidos: {data}")

            self.debug_listar_selects_visiveis()
            time.sleep(1)

            # 1. PREENCHER ANO (campo de texto)
            try:
                if 'vencimento' in data and '/' in data['vencimento']:
                    ano = data['vencimento'].split('/')[2]
                    ano_selectors = [
                        "//input[@id='ano-nfse']",
                        "//input[@name='ano']",
                        "//input[@placeholder*='ano' or @placeholder*='Ano']",
                        "//label[contains(text(), 'Ano')]/following-sibling::input",
                        "//label[contains(text(), 'Ano')]/parent::div//input"
                    ]
                    ano_input = None
                    for selector in ano_selectors:
                        try:
                            ano_input = self.driver.find_element(By.XPATH, selector)
                            if ano_input.is_displayed() and ano_input.is_enabled():
                                break
                        except:
                            continue
                    if ano_input:
                        # Usar JavaScript para preencher sem scroll automático
                        time.sleep(0.25)
                        self.driver.execute_script("arguments[0].value = arguments[1];", ano_input, ano)
                        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", ano_input)
                        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", ano_input)
                        logger.info(f"✅ Ano preenchido via JavaScript: {ano}")
                    else:
                        logger.warning("⚠️ Campo de ano não encontrado")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao preencher ano: {e}")

            # 2. SELECIONAR MÊS (usando função específica para o select2 do mês)
            try:
                if 'vencimento' in data and '/' in data['vencimento']:
                    mes_num = int(data['vencimento'].split('/')[1])
                    logger.info(f"[MÊS] Extraindo mês {mes_num} do vencimento {data['vencimento']}")
                    
                    # A função selecionar_mes_competencia agora detecta automaticamente
                    # se deve usar o mês atual ou o mês do vencimento
                    if self.selecionar_mes_competencia(mes_num):
                        logger.info(f"✅ Mês selecionado com sucesso (pode ter usado mês atual para evitar modal)")
                    else:
                        logger.warning("⚠️ Falha ao selecionar mês")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao selecionar mês: {e}")

            # 3. SELECIONAR TIPO DE ATIVIDADE (select2 do formulário de serviços)
            try:
                logger.info("[TIPO ATIVIDADE] Selecionando tipo de atividade (1 descida)")
                # Limpar overlays antes de tentar
                self.limpar_overlays()
                if self.selecionar_tipo_atividade(1):
                    logger.info("✅ Tipo de atividade selecionado com sucesso")
                else:
                    logger.warning("⚠️ Falha ao selecionar tipo de atividade")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao selecionar tipo de atividade: {e}")

            # 4. SELECIONAR CNAE (baseado na turma)
            try:
                # Determinar número de descidas baseado na turma
                arrow_down_count = 1  # padrão
                if 'turma' in data and data['turma']:
                    turma = data['turma'].upper()
                    if any(keyword in turma for keyword in ['G', 'MÉDIO', 'MEDIO']):
                        arrow_down_count = 2
                        logger.info("[CNAE] Detectado ensino médio (G) - 2 descidas")
                    elif any(keyword in turma for keyword in ['J', 'FUNDAMENTAL']):
                        arrow_down_count = 1
                        logger.info("[CNAE] Detectado ensino fundamental (J) - 1 descida")
                    else:
                        arrow_down_count = 1
                        logger.info(f"[CNAE] Turma não reconhecida ({turma}) - usando padrão (1 descida)")
                else:
                    logger.info("[CNAE] Sem informação de turma - usando padrão (1 descida)")
                
                logger.info(f"[CNAE] Selecionando CNAE com {arrow_down_count} descidas")
                # Limpar overlays antes de tentar
                self.limpar_overlays()
                if self.selecionar_cnae(arrow_down_count):
                    logger.info("✅ CNAE selecionado com sucesso")
                else:
                    logger.warning("⚠️ Falha ao selecionar CNAE")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao selecionar CNAE: {e}")

            # 5. PREENCHER VALOR DO SERVIÇO
            try:
                valor = str(data.get('valor', ''))
                if valor:
                    valor_input = self.driver.find_element(By.XPATH, "//input[@name='valorServico' or @placeholder='Valor do serviço']")
                    # Usar JavaScript para preencher sem scroll automático
                    self.driver.execute_script("arguments[0].value = arguments[1];", valor_input, valor)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", valor_input)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", valor_input)
                    logger.info(f"✅ Valor do serviço preenchido via JavaScript: {valor}")
                    time.sleep(1)  # Aguarda cálculo automático
                else:
                    logger.warning("⚠️ Valor do serviço não informado nos dados")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao preencher valor do serviço: {e}")

            # 6. PREENCHER DESCRIÇÃO (textarea) - ÚLTIMO CAMPO
            try:
                # Limpar overlays antes de tentar
                self.limpar_overlays()
                descricao_selectors = [
                    "//textarea[@id='discriminacao']",
                    "//textarea[@name='Discriminacao']",
                    "//label[contains(text(), 'Descrição')]/following-sibling::textarea",
                    "//label[contains(text(), 'Descrição')]/parent::div//textarea",
                    "//textarea[@placeholder*='descrição' or @placeholder*='Descrição']"
                ]
                descricao_textarea = None
                for selector in descricao_selectors:
                    try:
                        descricao_textarea = self.driver.find_element(By.XPATH, selector)
                        if descricao_textarea.is_displayed() and descricao_textarea.is_enabled():
                            break
                    except:
                        continue
                if descricao_textarea:
                    # Usar JavaScript para preencher o textarea sem scroll automático
                    time.sleep(0.25)
                    self.driver.execute_script("arguments[0].value = 'prestação de serviços educacionais';", descricao_textarea)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", descricao_textarea)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", descricao_textarea)
                    logger.info("✅ Descrição preenchida via JavaScript: prestação de serviços educacionais")
                else:
                    logger.warning("⚠️ Campo de descrição não encontrado")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao preencher descrição: {e}")

            # Screenshot final
            self.take_screenshot("step3_completa.png")
            logger.info("Screenshot final da Step 3 salvo: step3_completa.png")
            logger.info("✅ [SERVIÇOS] Etapa de serviços preenchida com sucesso!")
            return True

        except Exception as e:
            logger.error(f"❌ Erro geral ao preencher serviços: {e}")
            self.take_screenshot("erro_step3.png")
            return False

    def fill_nfse_valores(self, data: Dict[str, Any]) -> bool:
        """Preenche a etapa de Valores sem mover a tela."""
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            import time

            # 0. Ativar a aba 'Valores' se não estiver ativa
            try:
                aba_valores = self.driver.find_element(By.XPATH, "//a[@href='#tab4-4']")
                self.driver.execute_script("arguments[0].click();", aba_valores)
                time.sleep(0.5)
                logger.info("Aba 'Valores' ativada via JS.")
            except Exception as e:
                logger.warning(f"Não foi possível ativar a aba 'Valores': {e}")

            # 1. Esperar o campo de valor do serviço estar presente no DOM
            try:
                wait = WebDriverWait(self.driver, 10)
                valor_input = wait.until(
                    EC.presence_of_element_located((By.ID, "valores-servico"))
                )
                logger.info("Campo de valor do serviço presente no DOM.")
            except Exception as e:
                logger.warning(f"Campo de valor do serviço não apareceu: {e}")
                return False

            # 2. Verificar se o campo está habilitado
            if not valor_input.is_enabled() or valor_input.get_attribute('disabled'):
                logger.warning("Campo de valor do serviço está desabilitado. Tentando habilitar via JavaScript...")
                try:
                    self.driver.execute_script("arguments[0].removeAttribute('disabled');", valor_input)
                    time.sleep(0.2)
                except Exception as e:
                    logger.error(f"Não foi possível habilitar o campo via JS: {e}")
                    return False
                if not valor_input.is_enabled() or valor_input.get_attribute('disabled'):
                    logger.error("Mesmo após tentar habilitar, o campo continua desabilitado.")
                    return False

            # 3. Preencher o valor do serviço (testar vírgula e ponto)
            valor = str(data.get('valor', ''))
            if not valor:
                logger.warning("Valor do serviço não informado nos dados")
                return False
            formatos = [valor, valor.replace('.', ','), valor.replace(',', '.')]
            sucesso = False
            for v in formatos:
                try:
                    # Preencher via JavaScript para evitar movimento da tela
                    self.driver.execute_script("arguments[0].value = arguments[1];", valor_input, v)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", valor_input)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", valor_input)
                    logger.info(f"Tentando preencher valor do serviço via JS: {v}")
                    time.sleep(0.5)
                    # Verifica se o valor foi realmente inserido
                    valor_atual = valor_input.get_attribute('value')
                    logger.info(f"Valor no campo após envio: {valor_atual}")
                    if valor_atual and valor_atual != '0,00' and valor_atual != '0.00':
                        sucesso = True
                        break
                except Exception as e:
                    logger.warning(f"Erro ao tentar preencher valor '{v}' via JS: {e}")
                    # Fallback: tentar preenchimento normal
                    try:
                        valor_input.click()
                        valor_input.clear()
                        valor_input.send_keys(v)
                        logger.info(f"Tentando preencher valor do serviço normal: {v}")
                        time.sleep(0.5)
                        valor_atual = valor_input.get_attribute('value')
                        if valor_atual and valor_atual != '0,00' and valor_atual != '0.00':
                            sucesso = True
                            break
                    except Exception as e2:
                        logger.warning(f"Erro ao tentar preencher valor '{v}' normal: {e2}")
            if not sucesso:
                logger.error("Nenhum formato de valor foi aceito pelo campo.")
                return False

            # 4. Parar a automação aqui
            logger.info("Automação parada após preencher valor do serviço no Step 4.")
            return True
        except Exception as e:
            logger.error(f"Erro ao preencher etapa Valores: {e}")
            return False

    def salvar_rascunho(self) -> bool:
        """Clica no botão Salvar rascunho"""
        try:
            salvar_btn_xpaths = [
                "//a[contains(@class, 'salvar-rascunho')]",
                "//button[contains(., 'Salvar rascunho')]",
                "//input[@value='Salvar rascunho']"
            ]
            salvar_btn = None
            for xpath in salvar_btn_xpaths:
                try:
                    salvar_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    logger.info(f"Botão Salvar rascunho encontrado: {xpath}")
                    break
                except TimeoutException:
                    continue
            if not salvar_btn:
                logger.error("Botão Salvar rascunho não encontrado em nenhum seletor")
                self.take_screenshot("salvar_rascunho_not_found.png")
                return False
            salvar_btn.click()
            time.sleep(1)
            logger.info("Botão Salvar rascunho clicado")
            return True
        except Exception as e:
            logger.error(f"Erro ao clicar em Salvar rascunho: {e}")
            self.take_screenshot("salvar_rascunho_error.png")
            return False
    
    def navigate_to_new_nfse(self) -> bool:
        """
        Navega para formulário de nova NFSe (WebISS Palmas)
        """
        try:
            # 1. Clicar em ISSQN
            try:
                issqn_menu = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'ISSQN')]"))
                )
                issqn_menu.click()
                time.sleep(1)
                logger.info("Menu ISSQN clicado")
            except TimeoutException:
                logger.error("Menu ISSQN não encontrado")
                self.take_screenshot("issqn_menu_not_found.png")
                return False
            
            # 2. Clicar em NFS-e
            try:
                nfse_menu = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'NFS-e')]"))
                )
                nfse_menu.click()
                time.sleep(1)
                logger.info("Menu NFS-e clicado")
            except TimeoutException:
                logger.error("Menu NFS-e não encontrado")
                self.take_screenshot("nfse_menu_not_found.png")
                return False
            
            # 3. Clicar em Criar
            try:
                criar_menu = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Criar')]"))
                )
                criar_menu.click()
                time.sleep(1)
                logger.info("Menu Criar clicado - pronto para preencher a nota")
            except TimeoutException:
                logger.error("Menu Criar não encontrado")
                self.take_screenshot("criar_menu_not_found.png")
                return False
            
            # 4. Clicar no botão Próximo para avançar para o passo Tomador
            try:
                proximo_btn_xpaths = [
                    "//a[@id='btnProximo']",  # seletor direto por id
                    "//button[contains(., 'Próximo')]",
                    "//a[contains(., 'Próximo')]",
                    "//*[contains(@class, 'btn') and contains(., 'Próximo')]"
                ]
                proximo_btn = None
                for xpath in proximo_btn_xpaths:
                    try:
                        proximo_btn = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        logger.info(f"Botão Próximo encontrado: {xpath}")
                        break
                    except TimeoutException:
                        continue
                if not proximo_btn:
                    raise TimeoutException("Botão Próximo não encontrado em nenhum seletor")
                proximo_btn.click()
                time.sleep(1)
                logger.info("Botão Próximo clicado - avançando para Tomador")
                return True
            except TimeoutException:
                logger.error("Botão Próximo não encontrado")
                self.take_screenshot("proximo_btn_not_found.png")
                return False
        except Exception as e:
            logger.error(f"Erro ao navegar para nova NFSe: {e}")
            self.take_screenshot("navigate_to_new_nfse_error.png")
            return False
    
    def close(self):
        """Fecha o driver do navegador"""
        if self.driver:
            self.driver.quit()
            logger.info("Driver do navegador fechado")
    
    def take_screenshot(self, filename: str = None):
        """
        Tira screenshot da página atual
        
        Args:
            filename: Nome do arquivo (opcional)
        """
        if not filename:
            filename = f"screenshot_{int(time.time())}.png"
        
        try:
            self.driver.save_screenshot(f"logs/{filename}")
            logger.info(f"Screenshot salvo: {filename}")
        except Exception as e:
            logger.error(f"Erro ao salvar screenshot: {e}") 

    def analyze_page_structure(self) -> Dict[str, Any]:
        """
        Analisa a estrutura da página atual para debug e mapeamento de campos
        
        Returns:
            Dict com informações sobre a estrutura da página
        """
        try:
            analysis = {
                'url': self.driver.current_url,
                'title': self.driver.title,
                'select2_elements': [],
                'input_elements': [],
                'textarea_elements': [],
                'labels': [],
                'buttons': []
            }
            
            # Analisar select2 elements
            select2_elements = self.driver.find_elements(By.XPATH, "//a[contains(@class, 'select2-choice')]")
            for i, select2 in enumerate(select2_elements, 1):
                try:
                    # Tentar encontrar label associado
                    parent_div = select2.find_element(By.XPATH, "./ancestor::div[position()<=5]")
                    labels = parent_div.find_elements(By.XPATH, ".//label")
                    label_text = labels[0].text if labels else "Sem label"
                    
                    # Tentar encontrar placeholder ou name
                    inputs = parent_div.find_elements(By.XPATH, ".//input")
                    placeholder = inputs[0].get_attribute('placeholder') if inputs else None
                    name = inputs[0].get_attribute('name') if inputs else None
                    
                    analysis['select2_elements'].append({
                        'position': i,
                        'label': label_text,
                        'placeholder': placeholder,
                        'name': name,
                        'visible': select2.is_displayed(),
                        'enabled': select2.is_enabled()
                    })
                except Exception as e:
                    analysis['select2_elements'].append({
                        'position': i,
                        'label': 'Erro ao analisar',
                        'error': str(e)
                    })
            
            # Analisar input elements
            input_elements = self.driver.find_elements(By.XPATH, "//input[@type='text' or @type='number' or @type='email' or @type='tel']")
            for i, input_elem in enumerate(input_elements, 1):
                try:
                    analysis['input_elements'].append({
                        'position': i,
                        'type': input_elem.get_attribute('type'),
                        'name': input_elem.get_attribute('name'),
                        'placeholder': input_elem.get_attribute('placeholder'),
                        'id': input_elem.get_attribute('id'),
                        'visible': input_elem.is_displayed(),
                        'enabled': input_elem.is_enabled()
                    })
                except Exception as e:
                    analysis['input_elements'].append({
                        'position': i,
                        'error': str(e)
                    })
            
            # Analisar textarea elements
            textarea_elements = self.driver.find_elements(By.XPATH, "//textarea")
            for i, textarea in enumerate(textarea_elements, 1):
                try:
                    analysis['textarea_elements'].append({
                        'position': i,
                        'name': textarea.get_attribute('name'),
                        'placeholder': textarea.get_attribute('placeholder'),
                        'id': textarea.get_attribute('id'),
                        'visible': textarea.is_displayed(),
                        'enabled': textarea.is_enabled()
                    })
                except Exception as e:
                    analysis['textarea_elements'].append({
                        'position': i,
                        'error': str(e)
                    })
            
            # Analisar labels
            label_elements = self.driver.find_elements(By.XPATH, "//label")
            for i, label in enumerate(label_elements, 1):
                try:
                    analysis['labels'].append({
                        'position': i,
                        'text': label.text,
                        'for': label.get_attribute('for'),
                        'visible': label.is_displayed()
                    })
                except Exception as e:
                    analysis['labels'].append({
                        'position': i,
                        'error': str(e)
                    })
            
            # Analisar botões
            button_elements = self.driver.find_elements(By.XPATH, "//button | //a[contains(@class, 'btn')] | //input[@type='submit']")
            for i, button in enumerate(button_elements, 1):
                try:
                    analysis['buttons'].append({
                        'position': i,
                        'text': button.text,
                        'type': button.get_attribute('type'),
                        'class': button.get_attribute('class'),
                        'id': button.get_attribute('id'),
                        'visible': button.is_displayed(),
                        'enabled': button.is_enabled()
                    })
                except Exception as e:
                    analysis['buttons'].append({
                        'position': i,
                        'error': str(e)
                    })
            
            # Salvar análise em arquivo
            import json
            with open('logs/page_analysis.json', 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Análise da página salva em logs/page_analysis.json")
            logger.info(f"Encontrados: {len(select2_elements)} select2, {len(input_elements)} inputs, {len(textarea_elements)} textareas")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Erro ao analisar estrutura da página: {e}")
            return {} 

    def debug_listar_selects_visiveis(self):
        """Lista todos os selects visíveis na tela e seus principais atributos para debug."""
        try:
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            logger.info(f"=== DEBUG: {len(selects)} selects encontrados na página ===")
            for i, el in enumerate(selects):
                try:
                    visivel = el.is_displayed()
                    habilitado = el.is_enabled()
                    logger.info(
                        f"#{i+1} | name: {el.get_attribute('name')} | id: {el.get_attribute('id')} | class: {el.get_attribute('class')} | aria-label: {el.get_attribute('aria-label')} | placeholder: {el.get_attribute('placeholder')} | visível: {visivel} | habilitado: {habilitado}"
                    )
                except Exception as e:
                    logger.warning(f"Erro ao acessar select {i+1}: {e}")
        except Exception as e:
            logger.error(f"Erro ao listar selects visíveis: {e}") 

    def selecionar_tipo_atividade(self, arrow_down_count=1):
        """Seleciona o tipo de atividade no município usando JavaScript direto."""
        try:
            logger.info(f"[DEBUG] Tentando selecionar tipo de atividade com {arrow_down_count} descidas")
            
            # Estratégia 1: Usar JavaScript para setar valor diretamente
            try:
                logger.info("[DEBUG] Tentando estratégia 1: JavaScript direto para tipo de atividade")
                select_element = self.driver.find_element(By.ID, "lista-de-servicos-prestador")
                
                # Log das opções disponíveis para debug
                options = select_element.find_elements(By.TAG_NAME, "option")
                logger.info(f"[DEBUG] Opções disponíveis no tipo de atividade: {len(options)}")
                for i, option in enumerate(options):
                    logger.info(f"[DEBUG] Opção {i}: {option.get_attribute('value')} - {option.text}")
                
                # Setar valor baseado no número de descidas (índice começa em 1)
                if len(options) > arrow_down_count:
                    selected_value = options[arrow_down_count].get_attribute('value')
                    self.driver.execute_script(f"arguments[0].value = '{selected_value}';", select_element)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", select_element)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", select_element)
                    
                    # Forçar fechamento do select2 após setar valor
                    time.sleep(0.5)
                    self.driver.execute_script("""
                        // Forçar fechamento do select2
                        var select2Container = document.getElementById('s2id_lista-de-servicos-prestador');
                        if (select2Container) {
                            var select2Choice = select2Container.querySelector('.select2-choice');
                            if (select2Choice) {
                                select2Choice.click(); // Fechar se estiver aberto
                            }
                        }
                        
                        // Remover overlay se existir
                        var overlay = document.getElementById('select2-drop-mask');
                        if (overlay) {
                            overlay.remove();
                        }
                        
                        // Remover dropdown se existir
                        var dropdowns = document.querySelectorAll('.select2-drop');
                        dropdowns.forEach(function(dropdown) {
                            if (dropdown.style.display !== 'none') {
                                dropdown.style.display = 'none';
                            }
                        });
                    """)
                    
                    logger.info(f"✅ Tipo de atividade selecionado via JavaScript: {options[arrow_down_count].text}")
                    return True
                else:
                    logger.warning(f"[DEBUG] Não há opções suficientes no tipo de atividade")
                    return False
                    
            except Exception as e:
                logger.warning(f"[DEBUG] Estratégia 1 falhou: {e}")
                return False
                
        except Exception as e:
            logger.warning(f"❌ Erro ao selecionar tipo de atividade: {e}")
            return False

    def selecionar_cnae(self, arrow_down_count=1):
        """Seleciona o CNAE usando JavaScript direto."""
        try:
            logger.info(f"[DEBUG] Tentando selecionar CNAE com {arrow_down_count} descidas")
            
            # Estratégia 1: Usar JavaScript para setar valor diretamente
            try:
                logger.info("[DEBUG] Tentando estratégia 1: JavaScript direto para CNAE")
                select_element = self.driver.find_element(By.ID, "CnaeAtividade_Id")
                
                # Log das opções disponíveis para debug
                options = select_element.find_elements(By.TAG_NAME, "option")
                logger.info(f"[DEBUG] Opções disponíveis no CNAE: {len(options)}")
                for i, option in enumerate(options):
                    logger.info(f"[DEBUG] Opção {i}: {option.get_attribute('value')} - {option.text}")
                
                # Setar valor baseado no número de descidas (índice começa em 1)
                if len(options) > arrow_down_count:
                    selected_value = options[arrow_down_count].get_attribute('value')
                    self.driver.execute_script(f"arguments[0].value = '{selected_value}';", select_element)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", select_element)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", select_element)
                    
                    # Forçar fechamento do select2 após setar valor
                    time.sleep(0.5)
                    self.driver.execute_script("""
                        // Forçar fechamento do select2
                        var select2Container = document.getElementById('s2id_CnaeAtividade_Id');
                        if (select2Container) {
                            var select2Choice = select2Container.querySelector('.select2-choice');
                            if (select2Choice) {
                                select2Choice.click(); // Fechar se estiver aberto
                            }
                        }
                        
                        // Remover overlay se existir
                        var overlay = document.getElementById('select2-drop-mask');
                        if (overlay) {
                            overlay.remove();
                        }
                        
                        // Remover dropdown se existir
                        var dropdowns = document.querySelectorAll('.select2-drop');
                        dropdowns.forEach(function(dropdown) {
                            if (dropdown.style.display !== 'none') {
                                dropdown.style.display = 'none';
                            }
                        });
                    """)
                    
                    logger.info(f"✅ CNAE selecionado via JavaScript: {options[arrow_down_count].text}")
                    return True
                else:
                    logger.warning(f"[DEBUG] Não há opções suficientes no CNAE")
                    return False
                    
            except Exception as e:
                logger.warning(f"[DEBUG] Estratégia 1 falhou: {e}")
                return False
                
        except Exception as e:
            logger.warning(f"❌ Erro ao selecionar CNAE: {e}")
            return False

    def lidar_com_modal_competencia(self):
        """Lida com o modal de confirmação da competência que pode aparecer."""
        try:
            # Aguardar um pouco para o modal aparecer
            time.sleep(1)
            
            # Diferentes seletores para o botão "Sim"
            sim_selectors = [
                "//a[@data-handler='1' and contains(@class, 'btn-primary') and text()='Sim']",
                "//a[@data-handler='1' and contains(@class, 'btn-primary')]",
                "//a[contains(@class, 'btn-primary') and text()='Sim']",
                "//button[contains(@class, 'btn-primary') and text()='Sim']",
                "//a[text()='Sim']",
                "//button[text()='Sim']"
            ]
            
            for selector in sim_selectors:
                try:
                    sim_button = self.driver.find_element(By.XPATH, selector)
                    if sim_button.is_displayed():
                        logger.info(f"✅ Modal de confirmação encontrado com seletor: {selector}")
                        sim_button.click()
                        logger.info("✅ Clicado em 'Sim' no modal de confirmação")
                        time.sleep(1)
                        return True
                except:
                    continue
            
            logger.info("ℹ️ Modal de confirmação não encontrado")
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Erro ao lidar com modal: {e}")
            return False

    def avancar_para_step4(self):
        """Avança para o Step 4 após preencher o Step 3 com sucesso."""
        try:
            logger.info("=== AVANÇANDO PARA STEP 4 ===")
            
            # Limpar overlays antes de tentar clicar
            self.limpar_overlays()
            
            # Aguardar um pouco para garantir que tudo foi processado
            time.sleep(1)
            
            # Tentar encontrar e clicar no botão Próximo
            try:
                # Estratégia 1: Buscar pelo ID do botão Próximo
                proximo_button = self.driver.find_element(By.ID, "btnProximo")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", proximo_button)
                time.sleep(0.5)
                proximo_button.click()
                logger.info("✅ Botão Próximo clicado com sucesso (via ID)")
                
                # Lidar com modal de confirmação se aparecer
                self.lidar_com_modal_competencia()
                
                # Aguardar navegação
                time.sleep(2)
                
                # Verificar se avançou corretamente
                current_url = self.driver.current_url
                logger.info(f"URL após clique: {current_url}")
                
                if "criar" in current_url:
                    logger.info("✅ Permaneceu na página correta após Step 3")
                    return True
                else:
                    logger.warning("⚠️ URL mudou inesperadamente")
                    return False
                    
            except Exception as e:
                logger.warning(f"❌ Erro ao clicar no botão Próximo: {e}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro geral ao avançar para Step 4: {e}")
            return False 

    def voltar_para_criar_nfse(self):
        """Clica diretamente em 'Criar' e aguarda o container central do Step 1 estar pronto para interação."""
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC

            # Clica em Criar
            menu_criar = self.driver.find_element(By.XPATH, "//a[contains(., 'Criar') and contains(@href, '/nfse/criar')]")
            menu_criar.click()

            # Aguarda o título do Step 1 no container central
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h1[contains(., 'Criar nota fiscal eletrônica')]"))
            )
            # Aguarda o botão Próximo do Step 1 estar clicável
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Próximo')]"))
            )
            return True
        except Exception as e:
            import logging
            logging.error(f"Erro ao tentar voltar para tela de criar NFSe: {e}")
            return False