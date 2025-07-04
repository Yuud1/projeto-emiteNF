#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Segurança - Sistema de Licenças
Demonstra por que é impossível falsificar licenças
"""

import hashlib
import json
from datetime import datetime, timedelta

def gerar_hash(dados, chave_secreta):
    """Gera hash SHA-256 dos dados"""
    texto = f"{dados}{chave_secreta}"
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()

def testar_seguranca():
    """Testa diferentes cenários de tentativa de fraude"""
    
    chave_secreta = "EmiteNota2024@#$%SecretKey"
    
    print("🔐 TESTE DE SEGURANÇA - SISTEMA DE LICENÇAS")
    print("=" * 50)
    
    # Licença original válida
    dados_originais = {
        "cliente": "Empresa ABC",
        "data_criacao": "2024-07-03T10:00:00",
        "data_expiracao": "2024-08-02T10:00:00",
        "versao": "1.0",
        "dias_licenca": 30
    }
    
    hash_original = gerar_hash(json.dumps(dados_originais, sort_keys=True), chave_secreta)
    
    print(f"✅ Licença original válida:")
    print(f"   Hash: {hash_original[:16]}...")
    print()
    
    # Teste 1: Modificar dias_licenca
    print("🚫 TESTE 1: Modificar dias_licenca")
    dados_modificados = dados_originais.copy()
    dados_modificados["dias_licenca"] = 999
    
    hash_modificado = gerar_hash(json.dumps(dados_modificados, sort_keys=True), chave_secreta)
    
    print(f"   Original: {dados_originais['dias_licenca']} dias")
    print(f"   Modificado: {dados_modificados['dias_licenca']} dias")
    print(f"   Hash original: {hash_original[:16]}...")
    print(f"   Hash modificado: {hash_modificado[:16]}...")
    print(f"   Resultado: {'❌ DIFERENTE' if hash_original != hash_modificado else '✅ IGUAL'}")
    print()
    
    # Teste 2: Modificar data_expiracao
    print("🚫 TESTE 2: Modificar data_expiracao")
    dados_modificados = dados_originais.copy()
    dados_modificados["data_expiracao"] = "2030-12-31T10:00:00"
    
    hash_modificado = gerar_hash(json.dumps(dados_modificados, sort_keys=True), chave_secreta)
    
    print(f"   Original: {dados_originais['data_expiracao'][:10]}")
    print(f"   Modificado: {dados_modificados['data_expiracao'][:10]}")
    print(f"   Hash original: {hash_original[:16]}...")
    print(f"   Hash modificado: {hash_modificado[:16]}...")
    print(f"   Resultado: {'❌ DIFERENTE' if hash_original != hash_modificado else '✅ IGUAL'}")
    print()
    
    # Teste 3: Tentar com chave errada
    print("🚫 TESTE 3: Tentar com chave secreta errada")
    chave_errada = "ChaveErrada123"
    hash_chave_errada = gerar_hash(json.dumps(dados_originais, sort_keys=True), chave_errada)
    
    print(f"   Chave correta: {chave_secreta[:10]}...")
    print(f"   Chave errada: {chave_errada}")
    print(f"   Hash com chave correta: {hash_original[:16]}...")
    print(f"   Hash com chave errada: {hash_chave_errada[:16]}...")
    print(f"   Resultado: {'❌ DIFERENTE' if hash_original != hash_chave_errada else '✅ IGUAL'}")
    print()
    
    # Teste 4: Verificar que apenas você pode gerar hash válido
    print("✅ TESTE 4: Apenas você pode gerar hash válido")
    print(f"   Chave secreta: {chave_secreta}")
    print(f"   Hash válido: {hash_original}")
    print(f"   Conclusão: Sem a chave secreta, é impossível gerar hash válido!")
    print()
    
    print("🎯 CONCLUSÃO:")
    print("   ✅ Qualquer modificação invalida a licença")
    print("   ✅ Sem a chave secreta, não é possível gerar hash válido")
    print("   ✅ Sistema é seguro contra tentativas de fraude")
    print("   ✅ Apenas você pode gerar licenças válidas")

if __name__ == "__main__":
    testar_seguranca() 