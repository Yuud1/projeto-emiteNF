# 🚀 Emite Nota - Aplicativo de Automação WebISS

Aplicativo desktop completo para automação de emissão de notas fiscais eletrônicas no sistema WebISS.

## ✨ Funcionalidades

- 🖥️ **Interface Gráfica Intuitiva**
- 📄 **Importação de PDFs de Boletos**
- 🔄 **Processamento Automático**
- 📊 **Logs em Tempo Real**
- ⚙️ **Configuração Visual**
- 🚀 **Automação Completa WebISS**

## 🛠️ Instalação

### Opção 1: Executável (Recomendado)
1. Baixe o arquivo `EmiteNota.exe`
2. Configure o arquivo `.env` com suas credenciais
3. Execute o aplicativo

### Opção 2: Código Fonte
```bash
# Clone o repositório
git clone [url-do-repositorio]

# Instale as dependências
pip install -r requirements.txt

# Execute o aplicativo
python app.py
```

## 📋 Pré-requisitos

- Windows 10/11
- Google Chrome instalado
- Credenciais do WebISS
- PDFs de boletos para processar

## ⚙️ Configuração

1. **Configure o arquivo `.env`:**
```env
WEBISS_URL=https://palmasto.webiss.com.br/
USERNAME=seu_usuario
PASSWORD=sua_senha
HEADLESS_MODE=false
TIMEOUT=30
```

2. **Coloque os PDFs na pasta `boletos/`**

## 🎯 Como Usar

### 1. Iniciar o Aplicativo
- Execute `EmiteNota.exe` ou `python app.py`

### 2. Configurar Conexão
- Clique em "Testar Conexão" para verificar acesso
- Clique em "Login WebISS" para autenticar

### 3. Importar Dados
- Clique em "Extrair PDFs da Pasta 'boletos'"
- Ou selecione um arquivo CSV existente

### 4. Mapear Campos
- Configure o mapeamento entre colunas e campos do WebISS
- Salve os mapeamentos

### 5. Processar Boletos
- Clique em "Processar Boletos"
- Acompanhe o progresso nos logs

## 📁 Estrutura do Projeto

```
emite-nota/
├── app.py                 # Aplicativo principal
├── gui/                   # Interface gráfica
│   └── main_window.py     # Janela principal
├── config/                # Configurações
│   └── settings.py        # Configurações do sistema
├── utils/                 # Utilitários
│   └── data_processor.py  # Processamento de dados
├── webiss_automation.py   # Automação WebISS
├── boletos/               # PDFs para processar
├── logs/                  # Logs da aplicação
└── requirements.txt       # Dependências
```

## 🔧 Build do Aplicativo

Para criar o executável:

```bash
# Instale o PyInstaller
pip install pyinstaller

# Execute o build
python build_app.py
```

O executável será criado em `dist/EmiteNota.exe`

## 📊 Logs

Os logs são salvos em:
- `logs/emite_nota.log` - Log principal
- `logs/automacao_webiss.log` - Log da automação
- Screenshots de debug em `logs/`

## 🚨 Solução de Problemas

### Erro de Conexão
- Verifique se o Chrome está instalado
- Confirme as credenciais no arquivo `.env`
- Teste a conexão com o WebISS

### Erro de Importação
- Instale as dependências: `pip install -r requirements.txt`
- Verifique se o Python 3.8+ está instalado

### Erro de Processamento
- Verifique os logs em `logs/`
- Confirme se os PDFs estão na pasta `boletos/`
- Valide os mapeamentos de campos

## 📞 Suporte

Para suporte técnico, consulte os logs em `logs/` ou entre em contato com a equipe de desenvolvimento.

## 📄 Licença

Este projeto é de uso interno da empresa. 