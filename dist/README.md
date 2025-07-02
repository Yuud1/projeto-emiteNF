# Emite Nota - Automação WebISS

Sistema de automação para geração de notas fiscais no WebISS através da importação de dados de boletos.

## 🚀 Funcionalidades

- ✅ **Importação de dados** de boletos (CSV, Excel)
- ✅ **Login automático** no WebISS
- ✅ **Preenchimento automático** de campos
- ✅ **Geração de prévia** de notas fiscais
- ✅ **Interface gráfica** intuitiva
- ✅ **Validação de dados** (CPF/CNPJ, valores)
- ✅ **Logs detalhados** e screenshots
- ✅ **Mapeamento flexível** de campos
- ✅ **Modo headless** para execução em background

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Acesso ao WebISS da sua cidade

## 🛠️ Instalação

### 1. Clone ou baixe o projeto
```bash
git clone <url-do-repositorio>
cd emite-nota
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as credenciais
```bash
# Copie o arquivo de exemplo
cp env_example.txt .env

# Edite o arquivo .env com suas credenciais
```

### 4. Execute o programa
```bash
# No Windows
run.bat

# No Linux/Mac
python run.py
```

## 📊 Preparação dos Dados

### Formato Suportado
- **CSV** (.csv)
- **Excel** (.xlsx, .xls)

### Estrutura dos Dados
Seus dados devem conter colunas com as informações dos boletos:

| nome_cliente | cpf_cnpj | valor | descricao | endereco | telefone | email |
|--------------|----------|-------|-----------|----------|----------|-------|
| João Silva | 12345678901 | 150.00 | Prestação de serviços | Rua das Flores, 123 | 11987654321 | joao@email.com |

### Campos Obrigatórios
- `nome_cliente`: Nome ou razão social
- `cpf_cnpj`: CPF ou CNPJ do cliente
- `valor`: Valor do serviço

## 🖥️ Como Usar

### 1. Iniciar o Programa
Execute `run.bat` (Windows) ou `python run.py` (Linux/Mac)

### 2. Importar Dados
1. Clique em **"Procurar"** para selecionar seu arquivo
2. Clique em **"Carregar Dados"** para importar
3. Use **"Visualizar Dados"** para verificar

### 3. Mapear Campos
1. Para cada campo do WebISS, selecione a coluna correspondente
2. Clique em **"Salvar Mapeamentos"**
3. Os mapeamentos são salvos automaticamente

### 4. Configurar
- **URL do WebISS**: URL do sistema da sua cidade
- **Usuário e Senha**: Suas credenciais
- **Modo Headless**: Execute sem janela do navegador
- **Timeout**: Tempo de espera para carregamento

### 5. Processar
1. **Testar Conexão**: Verifica acesso ao WebISS
2. **Login WebISS**: Faz login no sistema
3. **Processar Boletos**: Inicia a automação

## 📁 Estrutura do Projeto

```
emite-nota/
├── main.py                 # Programa principal
├── run.py                  # Script de inicialização
├── run.bat                 # Executável Windows
├── requirements.txt        # Dependências Python
├── env_example.txt         # Exemplo de configuração
├── README.md              # Este arquivo
├── GUIA_USO.md            # Guia detalhado
├── data_processor.py      # Processamento de dados
├── webiss_automation.py   # Automação WebISS
├── config/
│   └── settings.py        # Configurações
├── gui/
│   └── main_window.py     # Interface gráfica
├── data/
│   └── exemplo_boletos.csv # Dados de exemplo
└── logs/                  # Logs do sistema
```

## ⚙️ Configurações

### Arquivo .env
```env
# Configurações do WebISS
WEBISS_USERNAME=seu_usuario
WEBISS_PASSWORD=sua_senha
WEBISS_URL=https://webiss.sua-cidade.gov.br

# Configurações de automação
HEADLESS_MODE=false
TIMEOUT=10
DELAY_BETWEEN_ACTIONS=2.0
```

### Configurações Avançadas
- **HEADLESS_MODE**: Execute sem interface gráfica
- **TIMEOUT**: Tempo máximo de espera (segundos)
- **DELAY_BETWEEN_ACTIONS**: Pausa entre ações (segundos)

## 🔧 Solução de Problemas

### Erro de Login
- Verifique credenciais no arquivo `.env`
- Confirme se a URL do WebISS está correta
- Teste o acesso manualmente

### Campos Não Encontrados
- O WebISS pode ter estrutura diferente
- Use "Testar Conexão" para verificar
- Verifique os seletores XPath no código

### Timeout
- Aumente o valor do timeout
- Verifique sua conexão com a internet
- Execute em horários de menor tráfego

## 📝 Logs e Monitoramento

- **Log em tempo real** na interface
- **Arquivo de log**: `logs/emite_nota.log`
- **Screenshots automáticos** em caso de erro
- **Salvar logs** manualmente através da interface

## 🔒 Segurança

- Credenciais armazenadas localmente no arquivo `.env`
- Dados processados localmente
- Não há envio de dados para servidores externos
- Nunca compartilhe o arquivo `.env`

## 📞 Suporte

### Informações Úteis para Suporte
- Versão do Python
- Versão do Chrome
- Sistema operacional
- URL do WebISS
- Logs de erro
- Screenshots de erro

### Logs de Erro
1. Verifique o log na interface
2. Consulte o arquivo `logs/emite_nota.log`
3. Verifique screenshots salvos automaticamente

## 🚀 Dicas de Uso

### Para Melhor Performance
- Use modo headless para processamentos grandes
- Ajuste timeout conforme sua conexão
- Processe em lotes menores se necessário
- Execute em horários de menor tráfego

### Para Maior Estabilidade
- Sempre teste com poucos registros primeiro
- Verifique os dados antes do processamento
- Monitore o log durante a execução
- Mantenha o navegador atualizado

## 📄 Licença

Este projeto é de uso livre para automação de processos internos.

## 🤝 Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

---

**Desenvolvido para automatizar a geração de notas fiscais no WebISS** 