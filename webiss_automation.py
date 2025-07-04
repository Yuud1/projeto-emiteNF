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
    
    def get_logs_dir(self):
        """Retorna o diretório de logs baseado no local do executável"""
        import sys
        import os
        if getattr(sys, 'frozen', False):
            # Se é um executável PyInstaller
            base_path = os.path.dirname(sys.executable)
        else:
            # Se é executado como script Python
            base_path = os.getcwd()
        
        logs_dir = os.path.join(base_path, 'logs')
        # Criar pasta logs se não existir
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        return logs_dir
        
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

            # 3. Lidar com Inscrição Municipal e CEP
            cep_value = data.get('cep', '')
            logger.info(f"CEP recebido nos dados: '{cep_value}'")
            
            if not cep_value and 'endereco' in data:
                # Tentar extrair CEP do endereço com múltiplas estratégias
                import re
                
                # Estratégia 1: CEP no formato padrão
                cep_match = re.search(r'(\d{5})-?(\d{3})', data['endereco'])
                if cep_match:
                    cep_value = f"{cep_match.group(1)}-{cep_match.group(2)}"
                    logger.info(f"✅ CEP extraído do endereço (padrão): {cep_value}")
                else:
                    # Estratégia 2: CEP sem hífen
                    cep_match = re.search(r'(\d{8})', data['endereco'])
                    if cep_match:
                        cep = cep_match.group(1)
                        cep_value = f"{cep[:5]}-{cep[5:]}"
                        logger.info(f"✅ CEP extraído do endereço (sem hífen): {cep_value}")
                    else:
                        # Estratégia 3: Buscar CEP em qualquer lugar
                        cep_match = re.search(r'(\d{5})[.\-\s]*(\d{3})', data['endereco'])
                        if cep_match:
                            cep_value = f"{cep_match.group(1)}-{cep_match.group(2)}"
                            logger.info(f"✅ CEP extraído do endereço (alternativo): {cep_value}")
                        else:
                            logger.warning(f"❌ CEP não encontrado no endereço: {data['endereco']}")
                            # Tentar extrair da descrição
                            if 'descricao' in data and data['descricao']:
                                cep_match = re.search(r'(\d{5})-?(\d{3})', data['descricao'])
                                if cep_match:
                                    cep_value = f"{cep_match.group(1)}-{cep_match.group(2)}"
                                    logger.info(f"✅ CEP extraído da descrição: {cep_value}")
            else:
                if cep_value:
                    logger.info(f"✅ CEP já disponível nos dados: {cep_value}")
                else:
                    logger.warning(f"⚠️ CEP não disponível nos dados e endereço não encontrado")
            
            # Verificar se o campo Inscrição Municipal virou select ou select2
            logger.info("🔍 Verificando campo Inscrição Municipal...")
            inscricao_municipal_select = None
            inscricao_municipal_select2 = None
            
            try:
                # Primeiro tentar encontrar o select normal (comboInscricao)
                try:
                    inscricao_municipal_select = self.driver.find_element(By.ID, "comboInscricao")
                    if inscricao_municipal_select.is_displayed():
                        logger.info("✅ Select normal da Inscrição Municipal encontrado (comboInscricao)")
                except:
                    logger.info("ℹ️ Select comboInscricao não encontrado")
                
                # Se não encontrou select normal, tentar select2
                if not inscricao_municipal_select:
                    inscricao_selectors = [
                        "//div[@id='s2id_inscricao_municipal']",
                        "//div[contains(@id, 's2id') and contains(@id, 'inscricao')]",
                        "//div[contains(@id, 's2id') and contains(@id, 'municipal')]",
                        "//div[contains(@class, 'select2-container') and contains(@class, 'inscricao')]"
                    ]
                    
                    for selector in inscricao_selectors:
                        try:
                            inscricao_municipal_select2 = self.driver.find_element(By.XPATH, selector)
                            if inscricao_municipal_select2.is_displayed():
                                logger.info(f"✅ Select2 da Inscrição Municipal encontrado: {selector}")
                                break
                        except:
                            continue
                
                # Lidar com select normal
                if inscricao_municipal_select:
                    logger.info("🔄 Campo Inscrição Municipal é um select normal - tentando selecionar opção correta...")
                    
                    if cep_value:
                        success = self.tentar_selecionar_inscricao_select_por_cep(inscricao_municipal_select, cep_value)
                        if success:
                            logger.info("✅ Inscrição Municipal selecionada com sucesso pelo CEP")
                        else:
                            logger.warning("⚠️ Não foi possível encontrar inscrição municipal pelo CEP")
                    else:
                        logger.warning("⚠️ CEP não disponível para selecionar inscrição municipal")
                
                # Lidar com select2
                elif inscricao_municipal_select2:
                    logger.info("🔄 Campo Inscrição Municipal é um select2 - tentando selecionar opção correta...")
                    
                    if cep_value:
                        success = self.tentar_selecionar_inscricao_por_cep(inscricao_municipal_select2, cep_value)
                        if success:
                            logger.info("✅ Inscrição Municipal selecionada com sucesso pelo CEP")
                        else:
                            logger.warning("⚠️ Não foi possível encontrar inscrição municipal pelo CEP")
                    else:
                        logger.warning("⚠️ CEP não disponível para selecionar inscrição municipal")
                
                # Se não encontrou nenhum select, preencher CEP normalmente
                else:
                    logger.info("ℹ️ Campo Inscrição Municipal não é um select - preenchendo CEP normalmente")
                    # Preencher CEP normalmente
                    cep_xpaths = [
                        "//input[@name='cep']",
                        "//input[@id='cep']",
                        "//input[contains(@placeholder, 'CEP')]",
                        "//input[contains(@placeholder, 'cep')]"
                    ]
                    
                    logger.info(f"Tentando preencher CEP: '{cep_value}'")
                    if cep_value:
                        success = find_and_fill_field('cep', cep_xpaths, cep_value)
                        if success:
                            logger.info(f"✅ CEP preenchido com sucesso: {cep_value}")
                        else:
                            logger.error(f"❌ Falha ao preencher CEP: {cep_value}")
                    else:
                        logger.warning("⚠️ Nenhum CEP disponível para preencher")
                        
            except Exception as e:
                logger.error(f"❌ Erro ao verificar inscrição municipal: {e}")
                # Fallback: tentar preencher CEP normalmente
                cep_xpaths = [
                    "//input[@name='cep']",
                    "//input[@id='cep']",
                    "//input[contains(@placeholder, 'CEP')]",
                    "//input[contains(@placeholder, 'cep')]"
                ]
                
                if cep_value:
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
    

    


    def click_proximo(self) -> bool:
        """Clica no botão Próximo na etapa atual"""
        try:
            import time
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





    def selecionar_mes_competencia(self, mes_num):
        """Seleciona o mês de competência no select2 do mês com múltiplas estratégias e remoção de overlay."""
        try:
            import time
            import os
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.action_chains import ActionChains
            
            # Detectar mês atual automaticamente
            from datetime import datetime
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
                    debug_file = os.path.join(self.get_logs_dir(), 'select2_ul_debug.html')
                    with open(debug_file, 'w', encoding='utf-8') as f:
                        f.write(ul.get_attribute('outerHTML'))
                    logger.info(f"[DEBUG] HTML do ul salvo em {debug_file}")
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
                    debug_file = os.path.join(self.get_logs_dir(), 'select2_ul_debug.html')
                    with open(debug_file, 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                    logger.info(f"[DEBUG] HTML da página salvo em {debug_file}")
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
            import time
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

            # 4. Valor do serviço preenchido com sucesso
            logger.info("✅ Valor do serviço preenchido com sucesso no Step 4.")
            return True
        except Exception as e:
            logger.error(f"Erro ao preencher etapa Valores: {e}")
            return False

    def salvar_rascunho(self) -> bool:
        """Clica no botão Salvar rascunho"""
        try:
            import time
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
    
    def emitir_nota_fiscal(self) -> bool:
        """Clica no botão Emitir nota fiscal"""
        try:
            import time
            # Aguardar um pouco para a página carregar após salvar rascunho
            time.sleep(1)
            
            # Múltiplos seletores para o botão Emitir (ordenados por precisão)
            emitir_btn_xpaths = [
                "//button[@id='botao-emitir-nota-fiscal']",
                "//button[@data-loading-message='Emitindo Nota Fiscal']",
                "//button[contains(@class, 'btn-primary') and contains(@class, 'glyphicons') and contains(@class, 'circle_ok')]",
                "//button[contains(@class, 'btn-primary') and contains(text(), 'Emitir')]",
                "//button[contains(@class, 'glyphicons') and contains(@class, 'circle_ok')]",
                "//button[contains(text(), 'Emitir')]",
                "//input[@value='Emitir']",
                "//form//button[@type='submit' and contains(@class, 'btn-primary')]"
            ]
            
            emitir_btn = None
            
            # Primeiro tentar com seletor CSS mais específico
            try:
                emitir_btn = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button#botao-emitir-nota-fiscal"))
                )
                logger.info("Botão Emitir encontrado via CSS selector")
            except TimeoutException:
                # Se não encontrar, tentar com XPath
                for xpath in emitir_btn_xpaths:
                    try:
                        emitir_btn = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        logger.info(f"Botão Emitir encontrado: {xpath}")
                        break
                    except TimeoutException:
                        continue
            
            if not emitir_btn:
                logger.error("Botão Emitir não encontrado em nenhum seletor")
                self.take_screenshot("emitir_not_found.png")
                return False
            
            # Verificar se o botão está visível e habilitado
            if not emitir_btn.is_displayed():
                logger.warning("Botão Emitir não está visível")
            if not emitir_btn.is_enabled():
                logger.warning("Botão Emitir não está habilitado")
            
            # Verificar se o botão não está com loading
            if "page-loading" in emitir_btn.get_attribute("class"):
                logger.info("Aguardando botão sair do estado de loading...")
                time.sleep(2)
            
            # Clicar no botão via JavaScript para evitar problemas de scroll
            self.driver.execute_script("arguments[0].click();", emitir_btn)
            logger.info("Botão Emitir clicado via JavaScript")
            
            # Aguardar processamento da emissão
            time.sleep(3)
            
            # Verificar se a emissão foi bem-sucedida
            # Procurar por mensagens de sucesso ou redirecionamento
            success_indicators = [
                "nota fiscal emitida",
                "emissão concluída",
                "nota fiscal gerada",
                "sucesso",
                "emitida com sucesso"
            ]
            
            page_text = self.driver.page_source.lower()
            if any(indicator in page_text for indicator in success_indicators):
                logger.info("✅ Nota fiscal emitida com sucesso!")
                return True
            else:
                # Verificar se houve erro
                error_indicators = [
                    "erro",
                    "falha",
                    "não foi possível",
                    "tente novamente"
                ]
                
                if any(indicator in page_text for indicator in error_indicators):
                    logger.error("❌ Erro na emissão da nota fiscal")
                    self.take_screenshot("erro_emissao.png")
                    return False
                else:
                    # Se não encontrou indicadores claros, assumir sucesso
                    logger.info("✅ Emissão da nota fiscal concluída")
                    
                    # Aguardar um pouco para a página carregar completamente
                    time.sleep(2)
                    
                    return True
                    
        except Exception as e:
            logger.error(f"Erro ao emitir nota fiscal: {e}")
            self.take_screenshot("emitir_error.png")
            return False
    
    def navigate_to_new_nfse(self) -> bool:
        """
        Navega para formulário de nova NFSe (WebISS Palmas)
        """
        try:
            import time
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
        import os
        import time
        if not filename:
            filename = f"screenshot_{int(time.time())}.png"
        
        try:
            screenshot_path = os.path.join(self.get_logs_dir(), filename)
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot salvo: {screenshot_path}")
        except Exception as e:
            logger.error(f"Erro ao salvar screenshot: {e}") 

 

 

    def selecionar_tipo_atividade(self, arrow_down_count=1):
        """Seleciona o tipo de atividade no município usando JavaScript direto."""
        try:
            import time
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
            import time
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
            import time
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

    def tentar_selecionar_inscricao_select_por_cep(self, select_element, cep_desejado):
        """
        Tenta selecionar a inscrição municipal correta baseada no CEP desejado (select normal)
        
        Args:
            select_element: Elemento select da inscrição municipal
            cep_desejado: CEP que deve ser encontrado após seleção
            
        Returns:
            bool: True se encontrou e selecionou a inscrição correta
        """
        try:
            import time
            logger.info(f"🎯 Tentando encontrar inscrição municipal para CEP: {cep_desejado}")
            
            # Aguardar um pouco para o select carregar as opções
            time.sleep(2)
            
            # Verificar se o select está habilitado
            if select_element.get_attribute('disabled'):
                logger.warning("⚠️ Select está desabilitado, tentando habilitar...")
                self.driver.execute_script("arguments[0].removeAttribute('disabled');", select_element)
                time.sleep(1)
            
            # Obter todas as opções do select
            opcoes = select_element.find_elements(By.TAG_NAME, "option")
            logger.info(f"📋 Encontradas {len(opcoes)} opções de inscrição municipal")
            
            # Log das opções para debug
            for i, opcao in enumerate(opcoes):
                valor = opcao.get_attribute('value')
                texto = opcao.text
                logger.info(f"  Opção {i}: valor='{valor}', texto='{texto}'")
            
            if len(opcoes) <= 1:  # Apenas "Selecione uma inscrição..."
                logger.warning("⚠️ Nenhuma opção válida encontrada no select")
                
                # Tentar aguardar mais um pouco e verificar novamente
                logger.info("🔄 Aguardando carregamento das opções...")
                time.sleep(3)
                opcoes = select_element.find_elements(By.TAG_NAME, "option")
                logger.info(f"📋 Após aguardar: {len(opcoes)} opções encontradas")
                
                if len(opcoes) <= 1:
                    logger.warning("⚠️ Ainda não há opções válidas, tentando forçar carregamento...")
                    
                    # Tentar forçar carregamento clicando no select
                    try:
                        self.driver.execute_script("arguments[0].click();", select_element)
                        time.sleep(2)
                        opcoes = select_element.find_elements(By.TAG_NAME, "option")
                        logger.info(f"📋 Após clicar: {len(opcoes)} opções encontradas")
                    except Exception as e:
                        logger.warning(f"⚠️ Erro ao clicar no select: {e}")
                
                if len(opcoes) <= 1:
                    logger.error("❌ Não foi possível carregar opções do select")
                    return False
            
            # Tentar cada opção até encontrar o CEP correto
            for i, opcao in enumerate(opcoes):
                try:
                    # Pular a primeira opção (geralmente "Selecione uma inscrição...")
                    if i == 0:
                        continue
                    
                    valor_opcao = opcao.get_attribute('value')
                    texto_opcao = opcao.text
                    
                    # Pular opções vazias ou inválidas
                    if not valor_opcao or valor_opcao == '-1' or valor_opcao == '':
                        logger.info(f"⏭️ Pulando opção {i}: valor inválido '{valor_opcao}'")
                        continue
                    
                    logger.info(f"🔄 Testando opção {i}/{len(opcoes)}: {texto_opcao} (valor: {valor_opcao})")
                    
                    # Selecionar a opção
                    self.driver.execute_script("arguments[0].value = arguments[1];", select_element, valor_opcao)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", select_element)
                    self.driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", select_element)
                    
                    time.sleep(3)  # Aguardar carregamento
                    
                    # Verificar se o CEP foi preenchido automaticamente
                    cep_campos = [
                        "//input[@name='cep']",
                        "//input[@id='cep']",
                        "//input[contains(@placeholder, 'CEP')]",
                        "//input[contains(@placeholder, 'cep')]"
                    ]
                    
                    cep_preenchido = None
                    for cep_xpath in cep_campos:
                        try:
                            cep_field = self.driver.find_element(By.XPATH, cep_xpath)
                            if cep_field.is_displayed() and cep_field.get_attribute('value'):
                                cep_preenchido = cep_field.get_attribute('value')
                                break
                        except:
                            continue
                    
                    if cep_preenchido:
                        logger.info(f"📍 CEP preenchido automaticamente: {cep_preenchido}")
                        
                        # Comparar com o CEP desejado
                        if cep_preenchido == cep_desejado:
                            logger.info(f"✅ CEP correto encontrado! Opção {i} selecionada: {texto_opcao}")
                            return True
                        else:
                            logger.info(f"❌ CEP incorreto ({cep_preenchido} != {cep_desejado}) - tentando próxima opção")
                    else:
                        logger.warning(f"⚠️ Nenhum CEP foi preenchido automaticamente para opção {i}: {texto_opcao}")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao testar opção {i}: {e}")
                    continue
            
            logger.warning(f"❌ Nenhuma opção encontrou o CEP correto: {cep_desejado}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao tentar selecionar inscrição por CEP: {e}")
            return False

    def tentar_selecionar_inscricao_por_cep(self, select2_element, cep_desejado):
        """
        Tenta selecionar a inscrição municipal correta baseada no CEP desejado (select2)
        
        Args:
            select2_element: Elemento select2 da inscrição municipal
            cep_desejado: CEP que deve ser encontrado após seleção
            
        Returns:
            bool: True se encontrou e selecionou a inscrição correta
        """
        try:
            import time
            logger.info(f"🎯 Tentando encontrar inscrição municipal para CEP: {cep_desejado}")
            
            # Clicar no select2 para abrir as opções
            select2_choice = select2_element.find_element(By.CLASS_NAME, "select2-choice")
            self.driver.execute_script("arguments[0].click();", select2_choice)
            time.sleep(1)
            
            # Aguardar lista de opções aparecer
            try:
                ul = self.wait.until(
                    lambda d: d.find_element(By.XPATH, "//ul[contains(@class, 'select2-results') and not(contains(@style, 'display: none'))]")
                )
                logger.info("✅ Lista de opções do select2 aberta")
            except TimeoutException:
                logger.error("❌ Lista de opções não apareceu")
                return False
            
            # Obter todas as opções
            opcoes = ul.find_elements(By.XPATH, ".//li[@class='select2-result-selectable']")
            logger.info(f"📋 Encontradas {len(opcoes)} opções de inscrição municipal")
            
            if not opcoes:
                logger.warning("⚠️ Nenhuma opção encontrada no select2")
                return False
            
            # Tentar cada opção até encontrar o CEP correto
            for i, opcao in enumerate(opcoes):
                try:
                    logger.info(f"🔄 Testando opção {i+1}/{len(opcoes)}")
                    
                    # Clicar na opção
                    self.driver.execute_script("arguments[0].click();", opcao)
                    time.sleep(2)  # Aguardar carregamento
                    
                    # Verificar se o CEP foi preenchido automaticamente
                    cep_campos = [
                        "//input[@name='cep']",
                        "//input[@id='cep']",
                        "//input[contains(@placeholder, 'CEP')]",
                        "//input[contains(@placeholder, 'cep')]"
                    ]
                    
                    cep_preenchido = None
                    for cep_xpath in cep_campos:
                        try:
                            cep_field = self.driver.find_element(By.XPATH, cep_xpath)
                            if cep_field.is_displayed() and cep_field.get_attribute('value'):
                                cep_preenchido = cep_field.get_attribute('value')
                                break
                        except:
                            continue
                    
                    if cep_preenchido:
                        logger.info(f"📍 CEP preenchido automaticamente: {cep_preenchido}")
                        
                        # Comparar com o CEP desejado
                        if cep_preenchido == cep_desejado:
                            logger.info(f"✅ CEP correto encontrado! Opção {i+1} selecionada")
                            return True
                        else:
                            logger.info(f"❌ CEP incorreto ({cep_preenchido} != {cep_desejado}) - tentando próxima opção")
                            
                            # Abrir select2 novamente para próxima opção
                            if i < len(opcoes) - 1:  # Se não for a última opção
                                self.driver.execute_script("arguments[0].click();", select2_choice)
                                time.sleep(1)
                                
                                # Aguardar lista aparecer novamente
                                try:
                                    ul = self.wait.until(
                                        lambda d: d.find_element(By.XPATH, "//ul[contains(@class, 'select2-results') and not(contains(@style, 'display: none'))]")
                                    )
                                except TimeoutException:
                                    logger.error("❌ Não foi possível reabrir lista de opções")
                                    return False
                                
                                # Obter opções novamente (pode ter mudado)
                                opcoes = ul.find_elements(By.XPATH, ".//li[@class='select2-result-selectable']")
                                if i + 1 < len(opcoes):
                                    opcao = opcoes[i + 1]
                                else:
                                    break
                    else:
                        logger.warning(f"⚠️ Nenhum CEP foi preenchido automaticamente para opção {i+1}")
                        
                        # Tentar próxima opção mesmo assim
                        if i < len(opcoes) - 1:
                            self.driver.execute_script("arguments[0].click();", select2_choice)
                            time.sleep(1)
                            
                            try:
                                ul = self.wait.until(
                                    lambda d: d.find_element(By.XPATH, "//ul[contains(@class, 'select2-results') and not(contains(@style, 'display: none'))]")
                                )
                                opcoes = ul.find_elements(By.XPATH, ".//li[@class='select2-result-selectable']")
                                if i + 1 < len(opcoes):
                                    opcao = opcoes[i + 1]
                                else:
                                    break
                            except TimeoutException:
                                break
                        
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao testar opção {i+1}: {e}")
                    continue
            
            logger.warning(f"❌ Nenhuma opção encontrou o CEP correto: {cep_desejado}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao tentar selecionar inscrição por CEP: {e}")
            return False

    def navegar_para_proxima_nota(self) -> bool:
        """Navega para criar a próxima nota após emitir a atual"""
        try:
            import time
            logger.info("🔄 Navegando para próxima nota...")
            
            # Aguardar um pouco para a página carregar após emissão
            time.sleep(2)
            
            # Tentar diferentes estratégias para voltar ao menu de criação
            
            # Estratégia 1: Clicar em "Criar" no menu lateral
            try:
                criar_menu = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Criar')]"))
                )
                criar_menu.click()
                time.sleep(1.5)
                logger.info("✅ Menu Criar clicado")
                
                # Clicar no botão Próximo para avançar para o passo Tomador
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
                    logger.info("✅ Botão Próximo clicado - avançando para Tomador")
                    return True
                except TimeoutException:
                    logger.error("Botão Próximo não encontrado")
                    self.take_screenshot("proximo_btn_not_found.png")
                    return False
            except TimeoutException:
                logger.warning("Menu Criar não encontrado, tentando estratégia 2")
            
            # Estratégia 2: Voltar ao menu principal e navegar novamente
            try:
                # Tentar voltar ao menu ISSQN
                issqn_menu = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'ISSQN')]"))
                )
                issqn_menu.click()
                time.sleep(1)
                
                # Clicar em NFS-e
                nfse_menu = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'NFS-e')]"))
                )
                nfse_menu.click()
                time.sleep(1)
                
                # Clicar em Criar
                criar_menu = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Criar')]"))
                )
                criar_menu.click()
                time.sleep(1.5)
                logger.info("✅ Navegação para próxima nota via menu completo")
                return True
            except TimeoutException:
                logger.warning("Navegação via menu completo falhou, tentando estratégia 3")
            
            # Estratégia 3: Usar JavaScript para navegar
            try:
                self.driver.execute_script("""
                    // Tentar encontrar e clicar no menu Criar via JavaScript
                    var criarMenus = document.querySelectorAll('span');
                    for (var i = 0; i < criarMenus.length; i++) {
                        if (criarMenus[i].textContent && criarMenus[i].textContent.includes('Criar')) {
                            criarMenus[i].click();
                            break;
                        }
                    }
                """)
                time.sleep(1.5)
                logger.info("✅ Navegação para próxima nota via JavaScript")
                return True
            except Exception as e:
                logger.warning(f"Navegação via JavaScript falhou: {e}")
            
            logger.error("❌ Falha em todas as estratégias de navegação")
            self.take_screenshot("navegacao_proxima_nota_falhou.png")
            return False
            
        except Exception as e:
            logger.error(f"Erro ao navegar para próxima nota: {e}")
            self.take_screenshot("erro_navegacao_proxima_nota.png")
            return False

 

