#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de debug para verificar a seleção de boletos
"""

import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_selecao_debug():
    """Testa a lógica de seleção com logs detalhados"""
    
    # Simular dados de teste (como no DataFrame)
    dados_teste = [
        {'pagina': 1, 'nome_cliente': 'Cliente 1', 'valor': 100.00, 'cpf_cnpj': '12345678901'},
        {'pagina': 2, 'nome_cliente': 'Cliente 2', 'valor': 200.00, 'cpf_cnpj': '12345678902'},
        {'pagina': 3, 'nome_cliente': 'Cliente 3', 'valor': 300.00, 'cpf_cnpj': '12345678903'},
        {'pagina': 4, 'nome_cliente': 'Cliente 4', 'valor': 400.00, 'cpf_cnpj': '12345678904'},
        {'pagina': 5, 'nome_cliente': 'Cliente 5', 'valor': 500.00, 'cpf_cnpj': '12345678905'},
    ]
    
    # Simular tree_items (como na interface)
    tree_items = ['item_0', 'item_1', 'item_2', 'item_3', 'item_4']
    
    # Simular checkbox_states (selecionando páginas 3 e 5)
    checkbox_states = {
        'item_0': False,  # Página 1 - não selecionada
        'item_1': False,  # Página 2 - não selecionada
        'item_2': True,   # Página 3 - selecionada
        'item_3': False,  # Página 4 - não selecionada
        'item_4': True,   # Página 5 - selecionada
    }
    
    logger.info("=== TESTE DE DEBUG - SELEÇÃO DE BOLETOS ===")
    logger.info(f"Dados de teste: {len(dados_teste)} registros")
    logger.info(f"Tree items: {tree_items}")
    logger.info(f"Checkbox states: {checkbox_states}")
    
    # Simular a função get_selected_data() com logs detalhados
    def get_selected_data_debug():
        logger.info("🔄 Executando get_selected_data()...")
        
        selected_indices = []
        logger.info(f"Tree items: {tree_items}")
        
        # Criar mapeamento entre item da árvore e índice do DataFrame
        # Como os dados são inseridos na ordem do DataFrame, podemos usar enumerate
        for i, item in enumerate(tree_items):
            logger.info(f"Verificando item {i}: {item}")
            checkbox_state = checkbox_states.get(item, False)
            logger.info(f"  Checkbox state: {checkbox_state}")
            
            if checkbox_state:
                # O índice i corresponde ao índice do DataFrame
                selected_indices.append(i)
                logger.info(f"  ✅ Adicionado índice {i}")
            else:
                logger.info(f"  ❌ Não selecionado")
        
        logger.info(f"Índices selecionados: {selected_indices}")
        
        if not selected_indices:
            logger.error("❌ Nenhum boleto selecionado!")
            return None
        
        # Simular retorno dos dados selecionados
        selected_data = [dados_teste[i] for i in selected_indices]
        logger.info(f"✅ {len(selected_data)} boletos selecionados para processamento")
        
        # Log dos dados selecionados
        for i, data in enumerate(selected_data):
            logger.info(f"  Boleto {i+1}: {data}")
        
        return selected_data
    
    # Testar a função
    selected_data = get_selected_data_debug()
    
    if selected_data is None:
        logger.error("❌ Nenhum dado selecionado!")
        return
    
    # Simular o processamento com logs detalhados
    logger.info(f"\n=== SIMULANDO PROCESSAMENTO ===")
    total_boletos = len(selected_data)
    
    # Criar lista de tuplas (índice_real, dados) para manter os índices originais
    boletos_para_processar = []
    logger.info("🔧 Criando lista de boletos para processar...")
    for idx, dados in enumerate(selected_data):
        # Obter o índice real (simulando o índice do DataFrame)
        indice_real = idx  # Em um caso real, seria selected_data.index[idx]
        boletos_para_processar.append((indice_real, dados))
        logger.info(f"📋 Adicionado boleto {idx+1}: índice {indice_real}, cliente: {dados['nome_cliente']}")
    
    logger.info(f"✅ Lista criada com {len(boletos_para_processar)} boletos")
    
    # Simular o loop de processamento
    for posicao, (indice_real, dados) in enumerate(boletos_para_processar, 1):
        logger.info(f"\n--- PROCESSANDO BOLETO {posicao}/{total_boletos} (Índice original: {indice_real}) ---")
        logger.info(f"Cliente: {dados['nome_cliente']}")
        logger.info(f"CPF/CNPJ: {dados['cpf_cnpj']}")
        logger.info(f"Valor: {dados['valor']}")
        
        # Simular navegação apenas no primeiro
        if posicao == 1:
            logger.info("🔄 Primeiro boleto - navegando para nova NFSe...")
        else:
            logger.info(f"🔄 Boleto {posicao} - usando nota já criada...")
        
        # Simular processamento
        logger.info("✅ Boleto processado com sucesso!")
        
        # Simular preparação da próxima nota (se não for o último)
        if posicao < total_boletos:
            logger.info("🔄 Preparando próxima nota...")
    
    logger.info(f"\n=== RESULTADO ESPERADO ===")
    logger.info("✅ O primeiro boleto (página 3) deve navegar para nova NFSe")
    logger.info("✅ O segundo boleto (página 5) deve usar a nota já criada")
    logger.info("✅ Ambos os boletos devem ser processados na ordem correta")

def test_problema_potencial():
    """Testa um problema potencial na lógica"""
    
    logger.info(f"\n=== TESTE DE PROBLEMA POTENCIAL ===")
    
    # Simular que apenas um boleto está sendo selecionado
    checkbox_states_problema = {
        'item_0': False,  # Página 1 - não selecionada
        'item_1': False,  # Página 2 - não selecionada
        'item_2': True,   # Página 3 - selecionada
        'item_3': False,  # Página 4 - não selecionada
        'item_4': False,  # Página 5 - NÃO selecionada (PROBLEMA!)
    }
    
    logger.info(f"Checkbox states (PROBLEMA): {checkbox_states_problema}")
    
    # Simular a função get_selected_data() com problema
    def get_selected_data_problema():
        selected_indices = []
        tree_items = ['item_0', 'item_1', 'item_2', 'item_3', 'item_4']
        
        for i, item in enumerate(tree_items):
            if checkbox_states_problema.get(item, False):
                selected_indices.append(i)
        
        logger.info(f"Índices selecionados (PROBLEMA): {selected_indices}")
        return selected_indices
    
    indices = get_selected_data_problema()
    logger.info(f"Resultado: {len(indices)} boletos selecionados")
    
    if len(indices) == 1:
        logger.error("❌ PROBLEMA IDENTIFICADO: Apenas 1 boleto selecionado!")
        logger.error("❌ Verifique se o usuário realmente selecionou 2 boletos na interface")
    else:
        logger.info("✅ Nenhum problema identificado na lógica")

if __name__ == "__main__":
    logger.info("🧪 INICIANDO TESTE DE DEBUG DE SELEÇÃO")
    
    # Testar lógica normal
    test_selecao_debug()
    
    # Testar problema potencial
    test_problema_potencial()
    
    logger.info("\n🎉 TESTE DE DEBUG CONCLUÍDO!")
    logger.info("Verifique se o usuário realmente selecionou 2 boletos na interface") 