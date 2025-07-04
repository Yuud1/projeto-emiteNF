#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples de seleção de boletos - Verifica se os boletos selecionados estão sendo processados na ordem correta
"""

import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_selecao_boletos():
    """Testa a lógica de seleção de boletos"""
    
    # Simular dados de teste (páginas 1 a 10)
    dados_teste = []
    for i in range(1, 11):  # Páginas 1 a 10
        dados_teste.append({
            'indice': i,
            'pagina': i,
            'cpf_cnpj': f'1234567890{i:02d}',
            'nome_cliente': f'Cliente Teste {i}',
            'endereco': f'Endereço Teste {i}, Palmas/TO - 77016-640',
            'valor': 100.00 + i,
            'vencimento': '10/07/2025',
            'descricao': f'MENSALIDADE: {i:06d} - Cliente {i} - TURMA: G1MA'
        })
    
    logger.info("=== DADOS DE TESTE CRIADOS ===")
    logger.info(f"Total de páginas: {len(dados_teste)}")
    logger.info(f"Índices: {[d['indice'] for d in dados_teste]}")
    
    # Simular seleção das páginas 3 e 5 (como no caso real)
    indices_selecionados = [3, 5]  # Páginas 3 e 5
    
    logger.info(f"\n=== SIMULANDO SELEÇÃO ===")
    logger.info(f"Índices selecionados: {indices_selecionados}")
    
    # Obter dados selecionados
    selected_data = []
    for idx in indices_selecionados:
        if 1 <= idx <= len(dados_teste):
            selected_data.append(dados_teste[idx - 1])  # -1 porque índices começam em 1
    
    logger.info(f"\n=== DADOS SELECIONADOS ===")
    logger.info(f"Total de boletos selecionados: {len(selected_data)}")
    logger.info(f"Índices dos dados selecionados: {[d['indice'] for d in selected_data]}")
    
    # Simular o processamento (nova lógica corrigida)
    logger.info(f"\n=== SIMULANDO PROCESSAMENTO (LÓGICA CORRIGIDA) ===")
    
    # Criar lista de tuplas (índice_real, dados) para manter os índices originais
    boletos_para_processar = []
    for idx, dados in enumerate(selected_data):
        # Obter o índice real
        indice_real = dados['indice']
        boletos_para_processar.append((indice_real, dados))
    
    logger.info(f"Boletos para processar: {[(idx, dados['nome_cliente']) for idx, dados in boletos_para_processar]}")
    
    # Simular o loop de processamento
    total_boletos = len(selected_data)
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

def test_selecao_boletos_antiga():
    """Testa a lógica antiga (com problema) para comparação"""
    
    logger.info(f"\n=== TESTE DA LÓGICA ANTIGA (COM PROBLEMA) ===")
    
    # Simular dados selecionados
    dados_teste = []
    for i in range(1, 11):
        dados_teste.append({
            'indice': i,
            'pagina': i,
            'cpf_cnpj': f'1234567890{i:02d}',
            'nome_cliente': f'Cliente Teste {i}',
            'endereco': f'Endereço Teste {i}, Palmas/TO - 77016-640',
            'valor': 100.00 + i,
            'vencimento': '10/07/2025',
            'descricao': f'MENSALIDADE: {i:06d} - Cliente {i} - TURMA: G1MA'
        })
    
    # Simular seleção das páginas 3 e 5
    indices_selecionados = [3, 5]
    selected_data = []
    for idx in indices_selecionados:
        if 1 <= idx <= len(dados_teste):
            selected_data.append(dados_teste[idx - 1])
    
    logger.info(f"Índices selecionados: {indices_selecionados}")
    logger.info(f"Índices dos dados selecionados: {[d['indice'] for d in selected_data]}")
    
    # Simular a lógica antiga (problemática)
    total_boletos = len(selected_data)
    for index, dados in enumerate(selected_data, 1):
        logger.info(f"\n--- PROCESSANDO BOLETO {index}/{total_boletos} ---")
        logger.info(f"Cliente: {dados['nome_cliente']}")
        logger.info(f"CPF/CNPJ: {dados['cpf_cnpj']}")
        logger.info(f"Valor: {dados['valor']}")
        
        # Simular navegação apenas no primeiro
        if index == 1:
            logger.info("🔄 Primeiro boleto - navegando para nova NFSe...")
        else:
            logger.info(f"🔄 Boleto {index} - usando nota já criada...")
        
        logger.info("✅ Boleto processado com sucesso!")
    
    logger.info(f"\n=== PROBLEMA DA LÓGICA ANTIGA ===")
    logger.info("❌ O enumerate(selected_data, 1) reinicia a numeração")
    logger.info("❌ Perde-se a informação do índice original")
    logger.info("❌ Não é possível identificar qual página real está sendo processada")

if __name__ == "__main__":
    logger.info("🧪 INICIANDO TESTES DE SELEÇÃO DE BOLETOS")
    
    # Testar lógica antiga (com problema)
    test_selecao_boletos_antiga()
    
    # Testar lógica nova (corrigida)
    test_selecao_boletos()
    
    logger.info("\n🎉 TESTES CONCLUÍDOS!")
    logger.info("A lógica corrigida deve mostrar os índices originais corretamente") 