# Guia de Uso - Emite Nota

## 📋 Visão Geral

O **Emite Nota** é um sistema de automação para geração de notas fiscais no WebISS através da importação de dados de boletos. O sistema permite automatizar o processo de preenchimento de formulários e geração de prévias de notas fiscais.

## 🚀 Instalação

### 1. Pré-requisitos
- Python 3.8 ou superior
- Google Chrome instalado
- Acesso ao WebISS

### 2. Instalação das Dependências
```bash
pip install -r requirements.txt
```

### 3. Configuração
1. Copie o arquivo de exemplo de configurações:
```bash
cp env_example.txt .env
```

2. Edite o arquivo `.env` com suas credenciais:
```env
WEBISS_USERNAME=seu_usuario_webiss
WEBISS_PASSWORD=sua_senha_webiss
WEBISS_URL=https://webiss.sua-cidade.gov.br
```

## 📊 Preparação dos Dados

### Formato dos Arquivos
O sistema suporta os seguintes formatos:
- **CSV** (.csv)
- **Excel** (.xlsx, .xls)

### Estrutura dos Dados
Seus dados devem conter colunas com as informações dos boletos. Exemplo:

| nome_cliente | cpf_cnpj | valor | descricao | endereco | telefone | email |
|--------------|----------|-------|-----------|----------|----------|-------|
| João Silva | 12345678901 | 150.00 | Prestação de serviços | Rua das Flores, 123 | 11987654321 | joao@email.com |

### Campos Obrigatórios
- `nome_cliente`: Nome ou razão social do cliente
- `cpf_cnpj`: CPF ou CNPJ do cliente
- `valor`: Valor do serviço

### Campos Opcionais
- `descricao`: Descrição do serviço
- `endereco`: Endereço do cliente
- `telefone`: Telefone do cliente
- `email`: Email do cliente
- `observacoes`: Observações adicionais

## 🖥️ Uso da Interface

### 1. Iniciar o Programa
```bash
python run.py
```

### 2. Importação de Dados
1. Clique em **"Procurar"** para selecionar seu arquivo de boletos
2. Clique em **"Carregar Dados"** para importar os dados
3. Use **"Visualizar Dados"** para verificar se os dados foram carregados corretamente

### 3. Mapeamento de Campos
1. Para cada campo do WebISS, selecione a coluna correspondente nos seus dados
2. Clique em **"Salvar Mapeamentos"** para guardar as configurações
3. Os mapeamentos serão salvos automaticamente para uso futuro

### 4. Configurações
- **URL do WebISS**: URL do sistema WebISS da sua cidade
- **Usuário e Senha**: Suas credenciais de acesso
- **Modo Headless**: Execute sem abrir janela do navegador
- **Timeout**: Tempo máximo de espera para carregamento de páginas

### 5. Processamento
1. **Testar Conexão**: Verifica se consegue acessar o WebISS
2. **Login WebISS**: Faz login no sistema
3. **Processar Boletos**: Inicia a automação para todos os registros

## 🔧 Configurações Avançadas

### Modo Headless
Para executar sem interface gráfica do navegador, marque a opção "Modo Headless". Isso é útil para:
- Execução em servidores
- Maior velocidade de processamento
- Menor uso de recursos

### Timeout
Ajuste o timeout conforme a velocidade da sua conexão:
- **Conexão lenta**: 15-20 segundos
- **Conexão normal**: 10 segundos
- **Conexão rápida**: 5-8 segundos

### Delay entre Ações
Controla o tempo de espera entre cada ação da automação:
- **Valor baixo**: Processamento mais rápido, mas pode causar erros
- **Valor alto**: Processamento mais lento, mas mais estável

## 📝 Logs e Monitoramento

### Log de Atividades
A interface mostra um log em tempo real com:
- Status de cada operação
- Erros encontrados
- Progresso do processamento

### Salvando Logs
- Clique em **"Salvar Log"** para guardar o histórico
- Os logs também são salvos automaticamente em `logs/emite_nota.log`

### Screenshots
O sistema tira screenshots automaticamente em caso de erro para facilitar o diagnóstico.

## ⚠️ Solução de Problemas

### Erro de Login
- Verifique se as credenciais estão corretas
- Confirme se a URL do WebISS está correta
- Teste o acesso manualmente no navegador

### Campos Não Encontrados
- O WebISS pode ter estrutura diferente
- Verifique os seletores XPath no código
- Use a opção "Testar Conexão" para verificar

### Timeout
- Aumente o valor do timeout
- Verifique sua conexão com a internet
- Tente executar em horários de menor tráfego

### Dados Inválidos
- Verifique se os CPFs/CNPJs estão corretos
- Confirme se os valores são números válidos
- Use a validação de dados antes do processamento

## 🔒 Segurança

### Credenciais
- Nunca compartilhe seu arquivo `.env`
- Use senhas fortes
- Troque a senha regularmente

### Dados Sensíveis
- Os dados dos clientes são processados localmente
- Não há envio de dados para servidores externos
- Os logs podem conter informações sensíveis

## 📞 Suporte

### Logs de Erro
Em caso de problemas, verifique:
1. O log na interface
2. O arquivo `logs/emite_nota.log`
3. Screenshots salvos automaticamente

### Informações Úteis
- Versão do Python
- Versão do Chrome
- Sistema operacional
- URL do WebISS
- Exemplo dos dados que estão falhando

## 🚀 Dicas de Uso

### Para Melhor Performance
1. Use modo headless para processamentos grandes
2. Ajuste o timeout conforme sua conexão
3. Processe em lotes menores se necessário
4. Execute em horários de menor tráfego

### Para Maior Estabilidade
1. Sempre teste com poucos registros primeiro
2. Verifique os dados antes do processamento
3. Monitore o log durante a execução
4. Mantenha o navegador atualizado

### Backup e Recuperação
1. Salve os mapeamentos de campos
2. Mantenha backup dos dados originais
3. Guarde os logs de execução
4. Use controle de versão se possível 

## 🚀 Rodando o Programa

### No Windows
Clique duas vezes em `run.bat` ou execute no terminal:
```
run.bat
```

### No Linux/Mac
Dê permissão e execute:
```
./run.sh
``` 