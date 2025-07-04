#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para verificar seleção de boletos
"""

print("=== VERIFICAÇÃO DE SELEÇÃO DE BOLETOS ===")

# Simular dados
dados = [
    {'pagina': 1, 'nome': 'Cliente 1'},
    {'pagina': 2, 'nome': 'Cliente 2'},
    {'pagina': 3, 'nome': 'Cliente 3'},
    {'pagina': 4, 'nome': 'Cliente 4'},
    {'pagina': 5, 'nome': 'Cliente 5'},
]

# Simular seleção (páginas 3 e 5)
selecionados = [2, 4]  # Índices 2 e 4 (páginas 3 e 5)

print(f"Dados: {len(dados)} registros")
print(f"Selecionados: {selecionados}")

# Simular processamento
boletos_para_processar = []
for idx in selecionados:
    boletos_para_processar.append((idx, dados[idx]))

print(f"Boletos para processar: {len(boletos_para_processar)}")

# Simular loop de processamento
for posicao, (indice, dados_boleto) in enumerate(boletos_para_processar, 1):
    print(f"\n--- PROCESSANDO BOLETO {posicao}/2 (Índice: {indice}) ---")
    print(f"Cliente: {dados_boleto['nome']}")
    
    if posicao == 1:
        print("🔄 Primeiro boleto - navegando para nova NFSe...")
    else:
        print("🔄 Boleto 2 - usando nota já criada...")
    
    print("✅ Boleto processado com sucesso!")

print("\n=== RESULTADO ===")
print("✅ Ambos os boletos devem ser processados")
print("✅ Primeiro: nova NFSe, Segundo: nota já criada") 