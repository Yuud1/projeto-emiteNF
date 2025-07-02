# Emite Nota - Interface GUI Moderna

## 🚀 Nova Interface Gráfica

A interface foi completamente remodelada para ser mais moderna, intuitiva e focada no fluxo de trabalho. Agora funciona exatamente como o `main.py`, mas com uma interface gráfica amigável.

## 📋 Fluxo de Trabalho

### 1. **Configuração Inicial**
```bash
# Copie o arquivo de exemplo e configure suas credenciais
cp env_example.txt .env
# Edite o arquivo .env com suas credenciais do WebISS
```

### 2. **Executar a Interface**
```bash
python start_gui.py
```

### 3. **Passos na Interface**

#### **Passo 1: Selecionar Pasta e Extrair Boletos PDF** 📄
- Digite o caminho da pasta com os PDFs ou clique em "📁 Procurar" para selecionar
- Clique em "📄 Extrair Boletos PDF"
- O sistema processará todos os PDFs na pasta selecionada
- Os dados serão extraídos e salvos em `boletos_extraidos.csv`

#### **Passo 2: Carregar Dados** 📊
- Clique em "📊 Carregar Dados"
- Os dados extraídos serão carregados na interface
- Você verá as informações dos dados no painel esquerdo

#### **Passo 3: Conectar WebISS** 🔗
- Clique em "🔗 Conectar WebISS"
- O sistema fará login no WebISS automaticamente
- Aguarde a confirmação de conexão

#### **Passo 4: Iniciar Automação** 🚀
- Clique em "🚀 Iniciar Automação"
- O sistema executará todo o processo automaticamente:
  - Navegação para nova NFSe
  - Preenchimento do Step 2 (Tomador)
  - Avanço para Step 3
  - Preenchimento do Step 3 (Serviços)
  - Avanço para Step 4
  - Preenchimento do Step 4 (Valores)

## 🎨 Características da Nova Interface

### **Design Moderno**
- Interface escura com cores profissionais
- Botões coloridos e intuitivos
- Ícones para facilitar identificação
- Layout responsivo e organizado

### **Painel Esquerdo - Controles**
- **Status do Sistema**: Mostra se dados e WebISS estão conectados
- **Seleção de Pasta**: Campo para escolher a pasta com os PDFs dos boletos
- **Controles Principais**: Botões para cada etapa do processo
- **Informações dos Dados**: Resumo dos dados carregados
- **Configurações**: Opção para modo headless

### **Painel Direito - Monitoramento**
- **Aba Log**: Log colorido com timestamps
- **Aba Dados**: Tabela com todos os dados extraídos

### **Log Inteligente**
- Cores diferentes para cada tipo de mensagem:
  - 🔵 **INFO**: Informações gerais
  - 🟢 **SUCCESS**: Sucessos
  - 🟡 **WARNING**: Avisos
  - 🔴 **ERROR**: Erros

## 🔧 Configurações

### **Arquivo .env**
```env
# Credenciais do WebISS
WEBISS_USERNAME=seu_usuario
WEBISS_PASSWORD=sua_senha
WEBISS_URL=https://webiss.exemplo.com

# Configurações de Automação
HEADLESS_MODE=false
TIMEOUT=15
DELAY_BETWEEN_ACTIONS=2.0
```

### **Modo Headless**
- Marque a opção "Modo Headless" para executar sem abrir o navegador
- Útil para execução em servidores ou automação

## 📁 Estrutura de Arquivos

```
emite-nota/
├── [pasta_selecionada]/        # Pasta com PDFs dos boletos (escolhida pelo usuário)
├── config/                     # Configurações
│   ├── settings.py
│   └── field_mappings.json
├── gui/
│   └── main_window.py         # Nova interface moderna
├── logs/                      # Logs de execução
├── boletos_extraidos.csv      # Dados extraídos dos PDFs
├── start_gui.py              # Script para iniciar a GUI
└── env_example.txt           # Exemplo de configuração
```

## 🎯 Vantagens da Nova Interface

### **Simplicidade**
- Fluxo linear e intuitivo
- Menos configurações complexas
- Foco no que realmente importa

### **Visibilidade**
- Status em tempo real
- Log detalhado e colorido
- Visualização dos dados extraídos

### **Confiabilidade**
- Mesma lógica do `main.py`
- Tratamento de erros robusto
- Feedback visual claro

### **Flexibilidade**
- Pode processar múltiplos boletos
- Configurações ajustáveis
- Modo headless disponível

## 🚨 Solução de Problemas

### **Erro: "Dados não carregados"**
- Execute primeiro a extração de PDFs
- Verifique se a pasta selecionada contém PDFs
- Certifique-se de que selecionou a pasta correta

### **Erro: "WebISS não conectado"**
- Verifique suas credenciais no arquivo `.env`
- Teste a URL do WebISS no navegador

### **Erro durante automação**
- Verifique o log colorido para detalhes
- Certifique-se de que o WebISS está acessível

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique o log na interface
2. Consulte os logs em `logs/`
3. Teste primeiro com `main.py` para validar a lógica

---

**🎉 A nova interface torna o processo muito mais simples e visual!** 