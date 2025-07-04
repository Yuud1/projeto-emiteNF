#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Licenças - Emite Nota
Use este script para gerar licenças para seus clientes
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class GeradorLicenca:
    """Gerador de licenças para clientes"""
    
    def __init__(self):
        self.chave_secreta = "EmiteNota2024@#$%SecretKey"
    
    def gerar_hash(self, dados):
        """Gera hash SHA-256 dos dados"""
        texto = f"{dados}{self.chave_secreta}"
        return hashlib.sha256(texto.encode('utf-8')).hexdigest()
    
    def criar_licenca(self, cliente, dias=30, versao="1.0"):
        """Cria uma nova licença"""
        data_criacao = datetime.now()
        data_expiracao = data_criacao + timedelta(days=dias)
        
        dados = {
            "cliente": cliente,
            "data_criacao": data_criacao.isoformat(),
            "data_expiracao": data_expiracao.isoformat(),
            "versao": versao,
            "dias_licenca": dias
        }
        
        # Gerar hash dos dados
        hash_licenca = self.gerar_hash(json.dumps(dados, sort_keys=True))
        
        licenca = {
            "dados": dados,
            "hash": hash_licenca
        }
        
        return licenca
    
    def salvar_licenca(self, licenca, nome_arquivo=None):
        """Salva a licença em arquivo JSON"""
        if nome_arquivo is None:
            cliente = licenca["dados"]["cliente"].replace(" ", "_")
            data = datetime.now().strftime("%Y%m%d")
            nome_arquivo = f"license_{cliente}_{data}.json"
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(licenca, f, indent=2, ensure_ascii=False)
        
        return nome_arquivo

def main():
    """Interface principal do gerador"""
    print("=" * 50)
    print("    GERADOR DE LICENÇAS - EMITE NOTA")
    print("=" * 50)
    print()
    
    gerador = GeradorLicenca()
    
    while True:
        print("📋 Opções:")
        print("1. Gerar nova licença")
        print("2. Verificar licença existente")
        print("3. Sair")
        print()
        
        opcao = input("Escolha uma opção (1-3): ").strip()
        
        if opcao == "1":
            print("\n" + "=" * 30)
            print("GERAR NOVA LICENÇA")
            print("=" * 30)
            
            cliente = input("Nome do cliente: ").strip()
            if not cliente:
                print("❌ Nome do cliente é obrigatório!")
                continue
            
            try:
                dias = int(input("Dias de validade (padrão: 30): ").strip() or "30")
            except ValueError:
                print("❌ Número de dias inválido! Usando 30 dias.")
                dias = 30
            
            versao = input("Versão (padrão: 1.0): ").strip() or "1.0"
            
            # Gerar licença
            licenca = gerador.criar_licenca(cliente, dias, versao)
            
            # Salvar licença
            nome_arquivo = gerador.salvar_licenca(licenca)
            
            print(f"\n✅ Licença gerada com sucesso!")
            print(f"📁 Arquivo: {nome_arquivo}")
            print(f"👤 Cliente: {cliente}")
            print(f"📅 Validade: {licenca['dados']['data_expiracao'][:10]}")
            print(f"⏰ Dias: {dias}")
            print(f"🔑 Hash: {licenca['hash'][:16]}...")
            
            # Perguntar se quer copiar para license.json
            copiar = input("\n📋 Copiar para license.json? (s/n): ").strip().lower()
            if copiar in ['s', 'sim', 'y', 'yes']:
                gerador.salvar_licenca(licenca, "license.json")
                print("✅ Copiado para license.json")
            
            print()
            
        elif opcao == "2":
            print("\n" + "=" * 30)
            print("VERIFICAR LICENÇA")
            print("=" * 30)
            
            arquivo = input("Arquivo da licença (license.json): ").strip() or "license.json"
            
            if not os.path.exists(arquivo):
                print(f"❌ Arquivo {arquivo} não encontrado!")
                continue
            
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    licenca = json.load(f)
                
                # Verificar hash
                hash_calculado = gerador.gerar_hash(json.dumps(licenca["dados"], sort_keys=True))
                hash_valido = hash_calculado == licenca["hash"]
                
                print(f"\n📋 Informações da licença:")
                print(f"👤 Cliente: {licenca['dados']['cliente']}")
                print(f"📅 Criação: {licenca['dados']['data_criacao'][:10]}")
                print(f"📅 Expiração: {licenca['dados']['data_expiracao'][:10]}")
                print(f"🔢 Versão: {licenca['dados']['versao']}")
                print(f"⏰ Dias: {licenca['dados']['dias_licenca']}")
                print(f"🔑 Hash válido: {'✅' if hash_valido else '❌'}")
                
                # Verificar se expirou
                data_expiracao = datetime.fromisoformat(licenca["dados"]["data_expiracao"])
                if datetime.now() > data_expiracao:
                    dias_expirado = (datetime.now() - data_expiracao).days
                    print(f"⚠️  EXPIRADA há {dias_expirado} dias!")
                else:
                    dias_restantes = (data_expiracao - datetime.now()).days
                    print(f"✅ VÁLIDA - {dias_restantes} dias restantes")
                
            except Exception as e:
                print(f"❌ Erro ao verificar licença: {e}")
            
            print()
            
        elif opcao == "3":
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida!")
            print()

if __name__ == "__main__":
    main() 